#!/bin/bash
# Тесты car-kit Mobile на обычной Java (без телефона и Android SDK):
#   логика (Engine) на подставных магнитолах tests/mock_adb.py, протокол ADB (AdbConn) через tests/mobile/fake_adbd.py,
#   совпадение плана с набором на ноутбуке (parity.sh, нужен pwsh) и правил защиты с carkit.ps1;
#   беспроводная отладка Android 11+: SPAKE2 (точки BoringSSL), сопряжение, TLS-порт.
#   CONSCRYPT_JAR=conscrypt-openjdk-uber.jar — настоящий TLS 1.3 с экспортом ключа; ADB_BIN=adb — проверка с настоящим «adb pair».
# bash tests/mobile/run.sh [--no-parity]
set -u
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
WORK="$(mktemp -d)"
FAIL=0
cd "$ROOT"
python3 dev/gen_mobile_patterns.py --check || FAIL=1
SRC=mobile/src/net/zherdyev/carkit
JSRC="$SRC/AdbKey.java $SRC/AdbConn.java $SRC/AdbPair.java $SRC/B64.java $SRC/ConscryptTls.java $SRC/Data.java $SRC/Ed25519.java $SRC/Engine.java $SRC/Lang.java $SRC/Pat.java $SRC/Scan.java $SRC/Sh.java $SRC/Spake2.java $SRC/Tls.java tests/mobile/Cli.java tests/mobile/CryptoTest.java tests/mobile/PairServer.java tests/mobile/TestTls.java"
if [ -n "${CONSCRYPT_JAR:-}" ]; then
  CP="$WORK/cls:$CONSCRYPT_JAR"
  javac -encoding UTF-8 -cp "$CONSCRYPT_JAR" -d "$WORK/cls" $JSRC || exit 1
else
  # без Conscrypt — заглушка только для компиляции (тесты с настоящим TLS пропускаются)
  mkdir -p "$WORK/stub/org/conscrypt"
  printf 'package org.conscrypt;\npublic final class Conscrypt {\n  public static java.security.Provider newProvider() { throw new UnsupportedOperationException("stub"); }\n  public static byte[] exportKeyingMaterial(javax.net.ssl.SSLSocket s, String l, byte[] c, int n) throws javax.net.ssl.SSLException { throw new UnsupportedOperationException("stub"); }\n}\n' > "$WORK/stub/org/conscrypt/Conscrypt.java"
  CP="$WORK/cls"
  javac -encoding UTF-8 -sourcepath "$WORK/stub" -d "$WORK/cls" $JSRC || exit 1
fi
cli() { local name=$1; shift; java -cp "$CP" net.zherdyev.carkit.Cli --root "$ROOT" "$@" > "$WORK/$name.log" 2>&1; }
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

# 8. Беспроводная отладка Android 11+: SPAKE2 как в BoringSSL (точки M, N из их seed), согласие ключей
java -cp "$CP" net.zherdyev.carkit.CryptoTest > "$WORK/crypto.log" 2>&1 || FAIL=1
grep '^FAIL' "$WORK/crypto.log"; echo "PASS crypto: $(grep -c '^PASS' "$WORK/crypto.log") проверок"
# 8б. Сопряжение по коду без шифрования (пакеты, HKDF, AES-GCM, обмен PeerInfo) и неверный код
P2=$((PORT + 1))
java -cp "$CP" net.zherdyev.carkit.PairServer $P2 482913 "$WORK/paired_keys" plain 2 > "$WORK/pairsrv.log" 2>&1 &
sleep 1
cli w_pair --pair 127.0.0.1:$P2 --code 482913 --tls plain --key "$WORK/wkey" --dump-cert "$WORK/wcert.pem"
expect w_pair 'PAIRED guid=adb-FAKEUNIT-test'
cli w_bad --pair 127.0.0.1:$P2 --code 000000 --tls plain --key "$WORK/wkey"
expect w_bad 'WrongCode'
sleep 1
grep -q "car-kit@phone" "$WORK/paired_keys" && echo "PASS w_pair: ключ телефона передан магнитоле" || { echo "FAIL w_pair: ключа нет"; FAIL=1; }
# 8в. TLS-порт: STLS -> TLS 1.3 с сертификатом сопряжённого ключа -> диагностика, применение, откат; чужой ключ — «не сопряжён»
P3=$((PORT + 2))
mock fyt
FAKE_TLSCA="$WORK/wcert.pem" python3 tests/mobile/fake_adbd.py $P3 2> "$WORK/tlsadbd.log" &
TLSD=$!
sleep 1
cli w_tls --adb 127.0.0.1:$P3 --tls jdk --key "$WORK/wkey" --mode both --journal "$WORK/w.tsv"
expect w_tls 'tls=true'
expect w_tls 'APPLIED 7'
expect w_tls 'ROLLED BACK, LEFT 0'
cli w_notpaired --adb 127.0.0.1:$P3 --tls jdk --key "$WORK/otherkey2" --mode diag
expect w_notpaired 'NotPaired'
cli w_notls --adb 127.0.0.1:$P3 --key "$WORK/wkey" --mode diag
expect w_notls 'TlsRequired'
if [ -n "${CONSCRYPT_JAR:-}" ]; then
  mock fyt
  cli w_tls_c --adb 127.0.0.1:$P3 --tls conscrypt --key "$WORK/wkey" --mode diag
  expect w_tls_c 'tls=true'
  expect w_tls_c 'PLATFORM fyt'
fi
kill $TLSD 2>/dev/null
# 8г. С настоящим TLS (Conscrypt): наш клиент <-> наш сервер, затем настоящий «adb pair» из Android SDK <-> наш сервер
if [ -n "${CONSCRYPT_JAR:-}" ]; then
  P4=$((PORT + 3))
  java -cp "$CP" net.zherdyev.carkit.PairServer $P4 735190 "$WORK/paired_keys2" conscrypt 2 > "$WORK/pairsrv2.log" 2>&1 &
  sleep 2
  cli w_pair_c --pair 127.0.0.1:$P4 --code 735190 --tls conscrypt --key "$WORK/wkey"
  expect w_pair_c 'PAIRED guid=adb-FAKEUNIT-test'
  if [ -n "${ADB_BIN:-}" ]; then
    "$ADB_BIN" start-server > /dev/null 2>&1
    "$ADB_BIN" pair 127.0.0.1:$P4 735190 > "$WORK/w_realadb.log" 2>&1
    expect w_realadb 'Successfully paired'
    expect w_realadb 'adb-FAKEUNIT-test'
    sleep 1
    HK="$(cut -d' ' -f1 "$HOME/.android/adbkey.pub")"
    grep -qF "$HK" "$WORK/paired_keys2" && echo "PASS w_realadb: ключ настоящего adb получен и расшифрован" || { echo "FAIL w_realadb: ключа adb нет"; cat "$WORK/pairsrv2.log"; FAIL=1; }
  else echo "SKIP настоящий adb pair (нет ADB_BIN)"; fi
else echo "SKIP TLS Conscrypt (нет CONSCRYPT_JAR)"; fi

# 9. План телефона = план ноутбука (нужен pwsh)
if [ "${1:-}" != "--no-parity" ] && command -v pwsh >/dev/null; then bash tests/mobile/parity.sh "$CP" || FAIL=1; fi

if [ $FAIL -ne 0 ]; then echo "=== logs: $WORK"; for f in "$WORK"/*.log; do echo "--- $f"; tail -25 "$f"; done; fi
exit $FAIL
