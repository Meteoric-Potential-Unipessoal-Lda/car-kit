#!/bin/bash
# Сборка car-kit Mobile без Gradle: aapt2 (ресурсы + манифест + assets) + javac + d8 + zipalign + apksigner из Android SDK.
# bash mobile/build.sh [выход.apk]
# В APK кладутся база и тексты набора: data/*.tsv, data/notes, data/lang (10 языков) и mobile/strings.tsv.
# Подпись — тем же ключом, что car-launcher: LAUNCHER_KEYSTORE (путь к .p12) + LAUNCHER_KS_PASS (alias carlauncher);
# без них — временный тестовый ключ.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(dirname "$HERE")"
OUT="${1:-$HERE/build/car-kit-mobile.apk}"
SDK="${ANDROID_HOME:-${ANDROID_SDK_ROOT:-}}"
[ -n "$SDK" ] || { echo "ANDROID_HOME is not set"; exit 1; }
BT="$(ls -d "$SDK"/build-tools/* | sort -V | tail -1)"
PLAT="$(ls -d "$SDK"/platforms/android-* | grep -E '/android-[0-9]+$' | sort -V | tail -1)"
JAR="$PLAT/android.jar"
VCODE="${MOBILE_VERSION_CODE:-400}"
VNAME="${MOBILE_VERSION_NAME:-0.4}"
echo "build-tools: $BT"; echo "platform: $PLAT"
python3 "$ROOT/dev/gen_mobile_patterns.py" --check
W="$HERE/build"; rm -rf "$W/obj" "$W/dex" "$W/assets" "$W/res.zip"; mkdir -p "$W/obj" "$W/dex" "$W/assets/lang" "$W/assets/notes"
cp "$ROOT"/data/uad.tsv "$ROOT"/data/ru.tsv "$ROOT"/data/car.tsv "$W/assets/"
cp "$ROOT"/data/notes/*.tsv "$W/assets/notes/"
cp "$ROOT"/data/lang/*.json "$W/assets/lang/"
cp "$HERE/strings.tsv" "$W/assets/"
"$BT/aapt2" compile --dir "$HERE/res" -o "$W/res.zip"
"$BT/aapt2" link -o "$W/base.apk" -I "$JAR" --manifest "$HERE/AndroidManifest.xml" "$W/res.zip" -A "$W/assets" \
  --min-sdk-version 21 --target-sdk-version 30 --version-code "$VCODE" --version-name "$VNAME"
javac -encoding UTF-8 -source 8 -target 8 -bootclasspath "$JAR" -classpath "$JAR" -d "$W/obj" -Xlint:-options $(find "$HERE/src" -name '*.java')
"$BT/d8" --min-api 21 --release --lib "$JAR" --output "$W/dex" $(find "$W/obj" -name '*.class')
cp "$W/base.apk" "$W/unsigned.apk"
(cd "$W/dex" && zip -q -X "$W/unsigned.apk" classes.dex)
"$BT/zipalign" -f -p 4 "$W/unsigned.apk" "$W/aligned.apk"
KS="${LAUNCHER_KEYSTORE:-}"; PASS="${LAUNCHER_KS_PASS:-}"
if [ -z "$KS" ] || [ ! -s "$KS" ]; then
  echo "WARNING: no LAUNCHER_KEYSTORE — signing with a throwaway test key"
  KS="$W/test.p12"; PASS="testtest"
  [ -f "$KS" ] || keytool -genkeypair -keystore "$KS" -storetype PKCS12 -storepass "$PASS" -keypass "$PASS" -alias carlauncher \
    -keyalg RSA -keysize 2048 -validity 10000 -dname "CN=car-kit test" >/dev/null 2>&1
fi
mkdir -p "$(dirname "$OUT")"
"$BT/apksigner" sign --ks "$KS" --ks-pass "pass:$PASS" --ks-key-alias carlauncher --out "$OUT" "$W/aligned.apk"
"$BT/apksigner" verify --print-certs "$OUT" | grep -E 'SHA-256 digest|Signer #1 certificate DN' || true
"$BT/aapt2" dump badging "$OUT" | head -3
ls -la "$OUT"
