#!/bin/bash
# Тесты car-kit Mobile на обычной Java (без телефона и Android SDK):
#   логика (Engine) на подставных магнитолах tests/mock_adb.py, протокол ADB (AdbConn) через tests/mobile/fake_adbd.py,
#   совпадение плана с набором на ноутбуке (parity.sh, нужен pwsh) и правил защиты с carkit.ps1.
# bash tests/mobile/run.sh [--no-parity]
set -u
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
WORK="$(mktemp -d)"
FAIL=0
cd "$ROOT"
python3 dev/gen_mobile_patterns.py --check || FAIL=1
SRC=mobile/src/net/zherdyev/carkit
javac -encoding UTF-8 -d "$WORK/cls" $SRC/AdbKey.java $SRC/AdbConn.java $SRC/B64.java $SRC/Data.java $SRC/Engine.java $SRC/Lang.java $SRC/Pat.java $SRC/Scan.java $SRC/Sh.java tests/mobile/Cli.java || exit 1
cli() { local name=$1; shift; java -cp "$WORK/cls" net.zherdyev.carkit.Cli --root "$ROOT" "$@" > "$WORK/$name.log" 2>&1; }
expect() { if grep -qF -- "$2" "$WORK/$1.log"; then echo "PASS $1: $2"; else echo "FAIL $1: нет «$2»"; FAIL=1; fi; }
reject() { if grep -qF -- "$2" "$WORK/$1.log"; then echo "FAIL $1: есть «$2»"; FAIL=1; else echo "PASS $1: нет «$2»"; fi; }
mock() { export MOCK_BRAND=$1 MOCK_STATE="$WORK/$1.json"; rm -f "$MOCK_STATE"; }

# 1. FYT: диагностика, план, применение и откат по журналу
mock fyt
cli m_fyt --mock --mode both --journal "$WORK/fyt.tsv"
expect m_fyt 'PLATFORM fyt | FYT (SYU) | Unisoc UIS7862'
expect m_fyt 'на деле это Android 10 (SDK 29)'
expect m_fyt 'ITEM [x] disable com.adups.fota'
expect m_fyt 'ITEM [x] idle com.waze'
expect m_fyt 'отключён com.adups.fota'
expect m_fyt 'партия 1:'
expect m_fyt 'APPLIED 7'
expect m_fyt 'включён обратно com.adups.fota'
expect m_fyt 'ROLLED BACK, LEFT 0'
reject m_fyt 'ITEM [x] disable com.syu'
reject m_fyt 'ITEM [ ] disable com.syu.ms'
reject m_fyt 'Exception'
python3 -c "import json,sys; s=json.load(open('$WORK/fyt.json')); sys.exit(1 if s['disabled'] else 0)" && echo "PASS m_fyt: после отката отключённых нет" || { echo "FAIL m_fyt: после отката остались отключённые"; FAIL=1; }

# 2. Служба магнитолы падает после партии -> партия откатывается, дальше не идём
mock fyt
MOCK_BREAKCORE=com.facebook.appmanager cli m_core --mock --mode apply --journal "$WORK/core.tsv"
expect m_core 'остановилась служба магнитолы com.syu.ms'
expect m_core 'откатываю партию'
expect m_core 'APPLIED 3'
reject m_core 'JOURNAL отключить com.facebook.appmanager'

# 3. Teyes: заранее отмечено только проверенное
mock teyes
cli m_teyes --mock --mode diag
expect m_teyes 'PLATFORM teyes'
expect m_teyes 'Teyes / UIS7870'

# 4. Android Automotive: только диагностика
mock aaos
cli m_aaos --mock --mode diag
expect m_aaos 'PLATFORM aaos'
reject m_aaos 'ITEM '

# 5. Остальные платформы распознаются
for b in ts:ts mtc:mtc reglink:reglink generic:unknown; do
  mock ${b%%:*}; cli m_${b%%:*} --mock --mode diag; expect m_${b%%:*} "PLATFORM ${b##*:}"; reject m_${b%%:*} 'Exception'
done
expect m_reglink 'DuraSpeed'

# 6. Языки: украинский и английский из языковых файлов набора
mock fyt; cli m_uk --mock --mode diag --lang uk; expect m_uk 'Платформа'
mock fyt; cli m_en --mock --mode diag --lang en; expect m_en 'Disable com.adups.fota'

# 7. Протокол ADB: новый ключ -> «Разрешить» на магнитоле -> CNXN; ответы многими кусками WRTE
PORT=$((20000 + RANDOM % 20000))
export FAKE_KEYS="$WORK/adb_keys" FAKE_ALLOW=1
mock fyt
python3 tests/mobile/fake_adbd.py $PORT 2> "$WORK/adbd.log" &
ADBD=$!
sleep 1
cli p_new --adb 127.0.0.1:$PORT --key "$WORK/phonekey" --mode both --journal "$WORK/p.tsv"
expect p_new 'ALLOW?'
expect p_new 'CONNECTED device::ro.product.name=fake'
expect p_new 'PLATFORM fyt'
expect p_new 'APPLIED 7'
expect p_new 'ROLLED BACK, LEFT 0'
# тот же ключ уже разрешён -> подключение без вопроса
unset FAKE_ALLOW
kill $ADBD; python3 tests/mobile/fake_adbd.py $PORT 2>> "$WORK/adbd.log" & ADBD=$!; sleep 1
mock fyt
cli p_known --adb 127.0.0.1:$PORT --key "$WORK/phonekey" --mode diag
expect p_known 'CONNECTED'
reject p_known 'ALLOW?'
# чужой ключ, «Разрешить» никто не нажал -> NotAllowed
cli p_deny --adb 127.0.0.1:$PORT --key "$WORK/otherkey" --mode diag
expect p_deny 'NotAllowed'
kill $ADBD
# порт беспроводной отладки (TLS)
FAKE_TLS=1 python3 tests/mobile/fake_adbd.py $PORT 2>> "$WORK/adbd.log" & ADBD=$!; sleep 1
cli p_tls --adb 127.0.0.1:$PORT --key "$WORK/phonekey" --mode diag
expect p_tls 'TlsRequired'
kill $ADBD
# закрытый порт
cli p_refused --adb 127.0.0.1:$PORT --key "$WORK/phonekey" --mode diag
expect p_refused 'ConnectException'
grep -q 'bad checksum\|bad magic\|error' "$WORK/adbd.log" && { echo "FAIL adbd: ошибки протокола"; cat "$WORK/adbd.log"; FAIL=1; } || echo "PASS adbd: протокол без ошибок"

# 8. План телефона = план ноутбука (нужен pwsh)
if [ "${1:-}" != "--no-parity" ] && command -v pwsh >/dev/null; then bash tests/mobile/parity.sh "$WORK/cls" || FAIL=1; fi

if [ $FAIL -ne 0 ]; then echo "=== logs: $WORK"; for f in "$WORK"/*.log; do echo "--- $f"; tail -25 "$f"; done; fi
exit $FAIL
