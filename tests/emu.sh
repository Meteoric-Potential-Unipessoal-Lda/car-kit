#!/bin/bash
# Проверка на НАСТОЯЩЕМ Android (эмулятор в GitHub Actions): диагностика набора, установка car-launcher,
# назначение домашним с проверкой кнопкой «Домой», интерфейс лаунчера, откат; car-kit Mobile — протокол ADB и приложение на телефоне.
# bash tests/emu.sh путь/car-launcher.apk [путь/car-kit-mobile.apk]
set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
APK="$1"
MAPK="${2:-}"
LOGS="$ROOT/emu-logs"; mkdir -p "$LOGS"
FAIL=0
ADB="$(command -v adb)"
adb wait-for-device
for i in $(seq 1 90); do [ "$(adb shell getprop sys.boot_completed | tr -d '\r')" = "1" ] && break; sleep 2; done
adb shell input keyevent 82 || true
KIT="$(mktemp -d)/kit"; mkdir -p "$KIT"
cp -r "$ROOT/carkit.ps1" "$ROOT/data" "$ROOT/ui" "$KIT/"; mkdir -p "$KIT/apk"; cp "$APK" "$KIT/apk/car-launcher.apk"
export CARKIT_TEST_SCAN=,
run() { local name=$1 input=$2; printf "$input" | timeout 900 pwsh -NoProfile -File "$KIT/carkit.ps1" -AdbPath "$ADB" -Lang ru -NoUpdateCheck -NoPause -Console > "$LOGS/$name.log" 2>&1; }
expect() { if grep -qF -- "$2" "$LOGS/$1.log"; then echo "PASS $1: $2"; else echo "FAIL $1: нет «$2»"; FAIL=1; fi; }
reject() { if grep -qF -- "$2" "$LOGS/$1.log"; then echo "FAIL $1: есть «$2»"; FAIL=1; else echo "PASS $1: нет «$2»"; fi; }

# Android 11: «cmd role get-role-holders» ещё нет — домашний смотрим через resolve-activity
homepkg() { adb wait-for-device; adb shell cmd package resolve-activity --brief -a android.intent.action.MAIN -c android.intent.category.HOME | tr -d '\r' | grep -E '^[A-Za-z0-9_.]+/' | tail -1 | cut -d/ -f1; }
HOME0="$(homepkg)"
echo "stock home: $HOME0"

# 1. Диагностика на живом Android: всё разбирается, ничего не меняется
run e_diag '1\nЭмулятор\n'
expect e_diag 'Архив:'
reject e_diag 'Exception'
reject e_diag 'не найден'

# 2. Оптимизация: только «установить car-launcher» + «сделать домашним»; неизвестная платформа -> «да» осторожному режиму
CARKIT_TEST_KINDS=apk,apkhome run e_home '2\nЭмулятор\nда\n\nда\n\n\n'
expect e_home 'установлено car-launcher.apk: net.zherdyev.carlauncher'
expect e_home 'домашний экран теперь: net.zherdyev.carlauncher'
H1="$(homepkg)"
[ "$H1" = "net.zherdyev.carlauncher" ] && echo "PASS role HOME = carlauncher" || { echo "FAIL role HOME = $H1"; FAIL=1; }
adb shell input keyevent 3; sleep 4
adb shell uiautomator dump /sdcard/ui.xml >/dev/null 2>&1; adb pull /sdcard/ui.xml "$LOGS/ui.xml" >/dev/null 2>&1
adb exec-out screencap -p > "$LOGS/launcher.png" 2>/dev/null || true
grep -qE 'Navigation|Навигация' "$LOGS/ui.xml" && echo "PASS launcher UI: плитки на экране" || { echo "FAIL launcher UI"; FAIL=1; }
adb shell dumpsys meminfo net.zherdyev.carlauncher | grep -E 'TOTAL( PSS)?:' | head -1 | tee "$LOGS/meminfo.txt"

# 3. Откат: вернуть штатный рабочий стол и удалить лаунчер
run e_rest '3\n\n\nда\n'
expect e_rest 'домашний экран возвращён'
H2="$(homepkg)"
[ "$H2" = "$HOME0" ] && echo "PASS role HOME вернулся: $H2" || { echo "FAIL role HOME после отката: $H2 (было $HOME0)"; FAIL=1; }
adb shell pm list packages | grep -q net.zherdyev.carlauncher && { echo "FAIL лаунчер не удалён"; FAIL=1; } || echo "PASS лаунчер удалён"

# 4. car-kit Mobile, протокол: наш клиент ADB (Java) подключается к эмулятору напрямую (порт 5555), как телефон к магнитоле.
#    adb-сервер на это время останавливаем — эмулятор держит одно подключение.
if [ -n "$MAPK" ]; then
  CLS="$(mktemp -d)"
  javac -encoding UTF-8 -d "$CLS" "$ROOT"/mobile/src/net/zherdyev/carkit/{AdbKey,AdbConn,B64,Data,Engine,Lang,Pat,Scan,Sh}.java "$ROOT/tests/mobile/Cli.java"
  DB="$(adb shell pm list packages -d | tr -d '\r' | sort)"
  adb kill-server; sleep 2
  java -cp "$CLS" net.zherdyev.carkit.Cli --root "$ROOT" --adb 127.0.0.1:5555 --key "$HOME/.android/adbkey" --mode both --kinds anim,disable --journal "$LOGS/m_jvm.tsv" > "$LOGS/m_jvm.log" 2>&1
  adb start-server; adb wait-for-device
  expect m_jvm 'CONNECTED device::'
  expect m_jvm 'PLATFORM unknown'
  expect m_jvm 'APPLIED'
  expect m_jvm 'ROLLED BACK, LEFT 0'
  reject m_jvm 'Exception'
  D0="$(adb shell pm list packages -d | tr -d '\r' | sort)"
  [ "$D0" = "$DB" ] && echo "PASS m_jvm: после отката отключённые пакеты как были" || { echo "FAIL m_jvm: отключённые до: [$DB] после: [$D0]"; FAIL=1; }

  # 5. car-kit Mobile, приложение: ставим APK, ключ приложения кладём в разрешённые (adb root), приложение само
  #    подключается к 10.0.2.2:5555 (это сам эмулятор), делает диагностику, применяет и откатывает. Только на эмуляторе.
  adb install -r "$MAPK" > "$LOGS/m_install.log" 2>&1
  expect m_install 'Success'
  adb logcat -c
  adb shell am start -n net.zherdyev.carkit/.MainActivity --es autotest key > /dev/null
  for i in $(seq 1 30); do adb shell ls /sdcard/Android/data/net.zherdyev.carkit/files/adbkey.pub >/dev/null 2>&1 && break; sleep 1; done
  adb pull /sdcard/Android/data/net.zherdyev.carkit/files/adbkey.pub "$LOGS/app_adbkey.pub" > /dev/null 2>&1
  adb root > /dev/null; sleep 3; adb wait-for-device
  adb push "$LOGS/app_adbkey.pub" /data/local/tmp/app.pub > /dev/null
  adb shell 'cat /data/local/tmp/app.pub >> /data/misc/adb/adb_keys; chmod 640 /data/misc/adb/adb_keys; chown system:shell /data/misc/adb/adb_keys' || true
  adb shell setprop ctl.restart adbd || true; sleep 3; adb wait-for-device
  adb shell am force-stop net.zherdyev.carkit
  adb shell am start -n net.zherdyev.carkit/.MainActivity --es autotest 10.0.2.2:5555 --es kinds anim,disable --ei delay 8 > /dev/null
  adb kill-server
  sleep 150
  adb start-server; adb wait-for-device
  adb logcat -d -s CARKIT:I > "$LOGS/m_app.log" 2>&1
  expect m_app 'AUTOTEST CONNECTED'
  expect m_app 'AUTOTEST DIAG'
  expect m_app 'AUTOTEST APPLIED'
  expect m_app 'AUTOTEST ROLLBACK 0'
  expect m_app 'AUTOTEST OK'
  adb unroot > /dev/null 2>&1; sleep 3; adb wait-for-device
  # обычный запуск: главный экран нарисован
  adb shell am force-stop net.zherdyev.carkit
  adb shell am start -n net.zherdyev.carkit/.MainActivity > /dev/null; sleep 5
  adb shell uiautomator dump /sdcard/m_ui.xml >/dev/null 2>&1; adb pull /sdcard/m_ui.xml "$LOGS/m_ui.xml" >/dev/null 2>&1
  adb exec-out screencap -p > "$LOGS/mobile.png" 2>/dev/null || true
  grep -qE 'Find the head unit|Найти магнитолу' "$LOGS/m_ui.xml" && echo "PASS mobile UI: главный экран" || { echo "FAIL mobile UI"; FAIL=1; }
fi

if [ $FAIL -ne 0 ]; then for f in "$LOGS"/*.log; do echo "----- $f"; tail -60 "$f"; done; exit 1; fi
echo "=== ЭМУЛЯТОР: ВСЁ ПРОШЛО"
