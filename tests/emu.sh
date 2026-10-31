#!/bin/bash
# Проверка на НАСТОЯЩЕМ Android (эмулятор в GitHub Actions): диагностика набора, установка car-launcher,
# назначение домашним с проверкой кнопкой «Домой», интерфейс лаунчера, откат. bash tests/emu.sh путь/car-launcher.apk
set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
APK="$1"
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
homepkg() { adb shell cmd package resolve-activity --brief -a android.intent.action.MAIN -c android.intent.category.HOME | tr -d '\r' | grep -E '^[A-Za-z0-9_.]+/' | tail -1 | cut -d/ -f1; }
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

if [ $FAIL -ne 0 ]; then for f in "$LOGS"/*.log; do echo "----- $f"; tail -60 "$f"; done; exit 1; fi
echo "=== ЭМУЛЯТОР: ВСЁ ПРОШЛО"
