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
  CV=2.5.2; CJ="$(mktemp -d)/conscrypt.jar"
  curl -fsSL -o "$CJ" "https://repo1.maven.org/maven2/org/conscrypt/conscrypt-openjdk-uber/$CV/conscrypt-openjdk-uber-$CV.jar"
  javac -encoding UTF-8 -cp "$CJ" -d "$CLS" "$ROOT"/mobile/src/net/zherdyev/carkit/{AdbKey,AdbConn,AdbPair,B64,ConscryptTls,Data,Ed25519,Engine,Lang,Pat,Scan,Sh,Spake2,Tls}.java "$ROOT"/tests/mobile/{Cli,TestTls,PairServer,CryptoTest}.java
  DB="$(adb shell pm list packages -d | tr -d '\r' | sort)"
  adb kill-server; sleep 2
  java -cp "$CLS:$CJ" net.zherdyev.carkit.Cli --root "$ROOT" --adb 127.0.0.1:5555 --key "$HOME/.android/adbkey" --mode both --kinds anim,disable --journal "$LOGS/m_jvm.tsv" > "$LOGS/m_jvm.log" 2>&1
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
  for i in $(seq 1 30); do adb logcat -d -s CARKIT:I | grep -q 'AUTOTEST PUB ' && break; sleep 1; done
  adb logcat -d -s CARKIT:I | sed -n 's/.*AUTOTEST PUB //p' | tr -d '\r' | head -1 > "$LOGS/app_adbkey.pub"
  [ -s "$LOGS/app_adbkey.pub" ] && echo "PASS m_key: ключ приложения получен" || { echo "FAIL m_key: нет ключа приложения"; FAIL=1; }
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
  # 6. Беспроводная отладка Android 11+ на настоящем adbd (TLS 1.3): включаем, подключаемся с сертификатом ключа
  adb shell svc wifi enable > /dev/null 2>&1; sleep 3
  adb shell settings put global adb_wifi_enabled 1
  # Android 11 может спросить «Разрешить отладку по Wi-Fi в этой сети?» — нажимаем «Всегда» и «Разрешить»
  tapw() {
    adb shell uiautomator dump /sdcard/wq.xml > /dev/null 2>&1; adb pull /sdcard/wq.xml "$LOGS/wq.xml" > /dev/null 2>&1
    python3 - "$LOGS/wq.xml" "$1" <<'PY'
import re, sys
t = open(sys.argv[1], encoding='utf-8', errors='replace').read()
for m in re.finditer(r'<node [^>]*text="([^"]*)"[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"', t):
    if re.fullmatch(sys.argv[2], m.group(1).strip(), re.I):
        print((int(m.group(2)) + int(m.group(4))) // 2, (int(m.group(3)) + int(m.group(5))) // 2); break
PY
  }
  TP=""; for i in $(seq 1 30); do
    TP="$(adb shell getprop service.adb.tls.port | tr -d '\r')"; [ -n "$TP" ] && [ "$TP" != "0" ] && break
    if [ $((i % 5)) -eq 3 ]; then
      C="$(tapw 'Always allow.*')"; [ -n "$C" ] && adb shell input tap $C
      C="$(tapw 'Allow')"; [ -n "$C" ] && { echo "tapped Allow (wireless debugging network)"; adb shell input tap $C; }
    fi
    sleep 1
  done
  echo "wireless debugging tls port: [$TP]"
  if [ -n "$TP" ] && [ "$TP" != "0" ]; then
    adb push "$HOME/.android/adbkey.pub" /data/local/tmp/host.pub > /dev/null
    adb shell 'cat /data/local/tmp/host.pub >> /data/misc/adb/adb_keys' || true
    adb forward tcp:7102 tcp:$TP > /dev/null
    java -cp "$CLS:$CJ" net.zherdyev.carkit.Cli --root "$ROOT" --adb 127.0.0.1:7102 --tls conscrypt --key "$HOME/.android/adbkey" --mode diag > "$LOGS/m_tls_jvm.log" 2>&1
    expect m_tls_jvm 'tls=true'
    expect m_tls_jvm 'PLATFORM unknown'
    reject m_tls_jvm 'Exception'
    adb forward --remove tcp:7102 > /dev/null 2>&1
    # приложение на «телефоне» (Conscrypt из APK) -> TLS-порт adbd
    adb logcat -c
    adb shell am force-stop net.zherdyev.carkit
    adb shell am start -n net.zherdyev.carkit/.MainActivity --es autotest 127.0.0.1:$TP --es kinds anim --ei delay 2 > /dev/null
    sleep 45
    adb logcat -d -s CARKIT:I > "$LOGS/m_app_tls.log" 2>&1
    adb logcat -d | grep -iE 'carkit|AndroidRuntime|conscrypt|DEBUG  :|adbd' | tail -80 > "$LOGS/m_app_tls_full.log" 2>&1
    expect m_app_tls 'AUTOTEST TLS true'
    expect m_app_tls 'AUTOTEST OK'
    # сопряжение по коду с настоящим adbd: открыть «Беспроводная отладка» -> «Подключение по коду», прочитать код и порт с экрана
    adb shell am start -n com.android.settings/.SubSettings -e :settings:show_fragment com.android.settings.development.WirelessDebuggingFragment > /dev/null 2>&1
    sleep 4
    adb shell uiautomator dump /sdcard/w1.xml > /dev/null 2>&1; adb pull /sdcard/w1.xml "$LOGS/w1.xml" > /dev/null 2>&1
    XY="$(python3 - "$LOGS/w1.xml" <<'PY'
import re, sys
t = open(sys.argv[1], encoding='utf-8', errors='replace').read()
for m in re.finditer(r'<node [^>]*text="([^"]*)"[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"', t):
    if 'pairing code' in m.group(1).lower():
        print((int(m.group(2)) + int(m.group(4))) // 2, (int(m.group(3)) + int(m.group(5))) // 2); break
PY
)"
    if [ -n "$XY" ]; then
      adb shell input tap $XY; sleep 4
      adb shell uiautomator dump /sdcard/w2.xml > /dev/null 2>&1; adb pull /sdcard/w2.xml "$LOGS/w2.xml" > /dev/null 2>&1
      adb exec-out screencap -p > "$LOGS/pairing.png" 2>/dev/null || true
      read CODE PADDR <<< "$(python3 - "$LOGS/w2.xml" <<'PY'
import re, sys
t = open(sys.argv[1], encoding='utf-8', errors='replace').read()
texts = re.findall(r'text="([^"]*)"', t)
code = next((x for x in texts if re.fullmatch(r'\d{6}', x)), '')
addr = next((x for x in texts if re.fullmatch(r'\d+\.\d+\.\d+\.\d+:\d+', x)), '')
print(code, addr)
PY
)"
      echo "pairing code: [$CODE] address: [$PADDR]"
      if [ -n "$CODE" ] && [ -n "$PADDR" ]; then
        # сопрягаемся с ноутбука через adb forward: окно с кодом должно оставаться на экране
        # (приложение в том же эмуляторе закрыло бы его — на настоящей магнитоле телефон отдельно, окно не закрывается)
        adb forward tcp:7103 tcp:${PADDR##*:} > /dev/null
        adb forward tcp:7102 tcp:$TP > /dev/null
        java -cp "$CLS:$CJ" net.zherdyev.carkit.Cli --root "$ROOT" --pair 127.0.0.1:7103 --code "$CODE" --tls conscrypt --key "$LOGS/paired_adbkey" --adb 127.0.0.1:7102 --mode diag > "$LOGS/m_pair_real.log" 2>&1
        expect m_pair_real 'PAIRED guid=adb-'
        expect m_pair_real 'tls=true'
        reject m_pair_real 'Exception'
        adb shell ls /data/misc/adb/ > "$LOGS/adb_dir.txt" 2>&1
        adb forward --remove-all > /dev/null 2>&1
      else echo "SKIP сопряжение с настоящим adbd: код не прочитан с экрана"; fi
    else echo "SKIP сопряжение с настоящим adbd: нет кнопки «Pair device with pairing code»"; fi
    adb shell input keyevent 4; adb shell input keyevent 3
    adb shell settings put global adb_wifi_enabled 0
  else echo "SKIP беспроводная отладка: adbd не открыл TLS-порт (нет Wi-Fi в эмуляторе?)"; fi
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
