#!/bin/bash
# Сценарные тесты car-kit на подставном adb (tests/mock_adb.py) в PowerShell 7 (pwsh).
# Запуск из корня репозитория: bash tests/run.sh   Код выхода 1 — если какой-то сценарий не прошёл.
set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
WORK="$(mktemp -d)"
ADB="$ROOT/tests/mock_adb.py"
chmod +x "$ADB"
FAIL=0
export CARKIT_TEST_SCAN=192.168.43.120   # «поиск в сети» без настоящего сканирования

# run NAME BRAND INPUT [keep] -> вывод в $WORK/NAME.log
run() {
  local name=$1 brand=$2 input=$3 keep=${4:-}
  local kit="$WORK/kit-$brand"   # один набор на платформу: откат находит журнал предыдущего прогона
  mkdir -p "$kit/data/lang"
  cp "$ROOT/carkit.ps1" "$kit/"; cp "$ROOT"/data/*.tsv "$kit/data/"; cp "$ROOT"/data/lang/*.json "$kit/data/lang/"
  if [ -n "${TEST_APK:-}" ]; then mkdir -p "$kit/apk"; head -c 4096 /dev/urandom > "$kit/apk/navi-test.apk"; fi
  export MOCK_BRAND=$brand MOCK_STATE="$WORK/$brand.json"
  [ -z "$keep" ] && rm -f "$MOCK_STATE"
  printf "$input" | timeout 900 pwsh -NoProfile -File "$kit/carkit.ps1" -AdbPath "$ADB" -Lang ru -NoUpdateCheck -NoPause > "$WORK/$name.log" 2>&1
}
expect() { if grep -qF -- "$2" "$WORK/$1.log"; then echo "PASS $1: $2"; else echo "FAIL $1: нет «$2»"; FAIL=1; fi; }
reject() { if grep -qF -- "$2" "$WORK/$1.log"; then echo "FAIL $1: есть «$2»"; FAIL=1; else echo "PASS $1: нет «$2»"; fi; }
state() { if grep -qF -- "$2" "$WORK/$1.json"; then echo "PASS state $1: $2"; else echo "FAIL state $1: нет $2"; cat "$WORK/$1.json"; FAIL=1; fi; }
nostate() { if [ ! -f "$WORK/$1.json" ] || ! grep -qF -- "$2" "$WORK/$1.json"; then echo "PASS state $1: нет $2"; else echo "FAIL state $1: есть $2"; cat "$WORK/$1.json"; FAIL=1; fi; }
report() { if grep -qF -- "$2" "$WORK"/kit-$1/reports/*/report.txt; then echo "PASS report $1: $2"; else echo "FAIL report $1: нет «$2»"; FAIL=1; fi; }

# 1. FYT (UIS7862, Joying): поиск в сети, диагностика — только чтение
run f_diag fyt '1\nТест\n'
expect f_diag 'ADB найден: 192.168.43.120'
expect f_diag 'Магнитола: FYT (SYU), Unisoc UIS7862'
expect f_diag 'на деле это Android 10 (SDK 29)'
expect f_diag 'убийца приложений'
expect f_diag 'Архив:'
reject f_diag 'Exception'
report fyt 'Платформа магнитолы: FYT (SYU)'
report fyt "$(printf '%-50s %s' com.google.android.apps.giant auto)"
report fyt 'com.syu.ms                                         защищён правилами набора'
report fyt 'com.google.android.videos                          работает от имени системы'
nostate fyt '"disabled": ["'
expect f_diag 'Часы магнитолы сбиты на 60 мин'
expect f_diag 'Слабый сигнал Wi-Fi (-82 дБм)'
expect f_diag 'экран магнитолы можно показать на этом ноутбуке'
report fyt 'Снимок настроек (raw/unit'
ls "$WORK"/kit-fyt/reports/*/raw/unit/oem_app_config.txt >/dev/null 2>&1 && echo "PASS f_diag: снимок config.txt" || { echo "FAIL f_diag: нет raw/unit/oem_app_config.txt"; FAIL=1; }

# 2. FYT: оптимизация по умолчанию + перезагрузка (магнитола вернулась в сеть), затем откат
run f_opt fyt '2\nТест\n\nда\n\nда\n'
expect f_opt 'отключён com.adups.fota'
expect f_opt 'не будет усыпляться в фоне (оптимизация батареи выключена): com.waze'
expect f_opt 'партия 1: проверка рабочего стола'
expect f_opt 'после перезагрузки всё отключённое осталось отключённым'
reject f_opt 'отключён com.syu'
reject f_opt 'Exception'
state fyt 'com.adups.fota'
state fyt '"idle": ["com.spotify.music"'
nostate fyt 'com.syu.ms'
nostate fyt 'com.syu.radio'
run f_rest fyt '3\n\n\nда\n' keep
expect f_rest 'включён обратно com.adups.fota'
expect f_rest 'оптимизация батареи возвращена: com.waze'
nostate fyt 'adups'
nostate fyt 'com.waze'

# 3. Служба магнитолы (com.syu.ms) упала после партии -> откат партии и стоп
MOCK_BREAKCORE=com.facebook.appmanager run f_core fyt '2\nТ\n\nда\n\n\n'
expect f_core 'остановилась служба магнитолы com.syu.ms'
expect f_core 'откатываю партию и останавливаюсь'
nostate fyt 'com.facebook.appmanager'

# 4. Teyes (FYT, fytmanufacturer=95): осторожнее — сами отмечаются только проверенные
run t_diag teyes '1\nТ\n'
expect t_diag 'Магнитола: Teyes (FYT)'
report teyes 'Teyes / UIS7870'
report teyes "$(printf '%-50s %s' com.google.android.apps.giant base)"

# 5. Topway TS10: постоянный ADB по сети -> предупреждение
run ts_diag ts '1\nТ\n'
expect ts_diag 'Магнитола: Topway TS, Unisoc UIS7862'
expect ts_diag 'ADB по сети включён постоянно (порт 5555)'
report ts 'Пакеты производителя под защитой (4): com.tw.car, com.tw.carchoose, com.tw.music, com.tw.radio'

# 6. MTCE (PX5): по пути MTCManager.apk
run m_opt mtc '2\nТ\n\nда\n\n\n'
expect m_opt 'Магнитола: Microntek MTCD/MTCE (HCT), Rockchip PX5 (RK3368)'
reject m_opt 'отключён com.microntek'
reject m_opt 'отключён android.microntek'
state mtc 'com.google.android.feedback'

# 6б. Свой APK из папки apk: установка по галочке (A — отметить всё), затем откат удаляет только поставленное набором
TEST_APK=1 run m_apk mtc '2\nТ\nA\n\nда\n\n\n'
expect m_apk 'Установить navi-test.apk'
expect m_apk 'установлено navi-test.apk: com.example.navitest'
state mtc 'com.example.navitest'
run m_apkr mtc '3\n\n\nда\n' keep
expect m_apkr 'удалено приложение, которое ставил набор: com.example.navitest'
nostate mtc 'navitest'

# 7. Reglink (MTK): DuraSpeed, Adups
run r_diag reglink '1\nТ\n'
expect r_diag 'Магнитола: Reglink (MTK), MediaTek MT6765'
expect r_diag 'MediaTek DuraSpeed'
report reglink 'com.adups.fota.sysoper'

# 8. Android Automotive (Volvo): оптимизация выключена, только диагностика
run a_opt aaos '2\nТ\n'
expect a_opt 'Это Android Automotive OS'
expect a_opt 'делаю только диагностику'
reject a_opt 'План оптимизации'
nostate aaos 'disabled": ["'

# 9. Неизвестная магнитола: спрашивает, работать ли в осторожном режиме; «нет» в плане -> ничего не менялось
run g_opt generic '2\nТ\nда\n\nнет\n'
expect g_opt 'Платформа магнитолы не распознана'
expect g_opt 'Отменено — ничего не менялось'
reject g_opt 'отключён com.vendor'

# 10. Порт закрыт: подсказка, как включить ADB
MOCK_REFUSE=1 run x_refuse fyt '1\nТ\nh\nq\n'
expect x_refuse 'порт ADB закрыт'
expect x_refuse 'Частые (попробовать руками'
expect x_refuse '3368'

# 11. Первое подключение не разрешено на экране -> подсказка «Разрешить», потом работает
MOCK_UNAUTH=1 run x_auth fyt '1\nТ\n'
expect x_auth 'нажми «Разрешить» в окне «Разрешить отладку по USB?»'
expect x_auth 'Архив:'

# 12. IP вручную без порта -> :5555
CARKIT_TEST_SCAN=, run x_ip fyt '1\nТ\ni\n192.168.43.120\n'
expect x_ip 'подключаюсь к 192.168.43.120:5555'
expect x_ip 'Архив:'

# 13. Пункт U на подставных данных Windows
if pwsh -NoProfile -File "$ROOT/tests/usbtest.ps1"; then echo "PASS usbtest"; else echo "FAIL usbtest"; FAIL=1; fi

# 14. Веб-интерфейс: сервер, ответы по HTTP, смена языка на ходу, отчёт
if python3 "$ROOT/tests/webtest.py" pwsh; then :; else FAIL=1; fi

if [ $FAIL -ne 0 ]; then echo "=== ЕСТЬ ОШИБКИ, логи: $WORK"; for f in "$WORK"/*.log; do echo "----- $f"; tail -40 "$f"; done; exit 1; fi
echo "=== ВСЕ ТЕСТЫ ПРОШЛИ"
