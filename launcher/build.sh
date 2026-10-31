#!/bin/bash
# Сборка car-launcher без Gradle: aapt2 (манифест) + javac + d8 + zipalign + apksigner из Android SDK.
# bash launcher/build.sh [выход.apk]
# Подпись: LAUNCHER_KEYSTORE (путь к .p12/.jks) + LAUNCHER_KS_PASS (пароль, alias carlauncher);
# без них — временный тестовый ключ (такой APK поверх подписанного нашим ключом не встанет).
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
OUT="${1:-$HERE/build/car-launcher.apk}"
SDK="${ANDROID_HOME:-${ANDROID_SDK_ROOT:-}}"
[ -n "$SDK" ] || { echo "ANDROID_HOME is not set"; exit 1; }
BT="$(ls -d "$SDK"/build-tools/* | sort -V | tail -1)"
# только стабильные платформы (android-35), без бета-версий вроде android-37.2-beta3
PLAT="$(ls -d "$SDK"/platforms/android-* | grep -E '/android-[0-9]+$' | sort -V | tail -1)"
JAR="$PLAT/android.jar"
VCODE="${LAUNCHER_VERSION_CODE:-3}"
VNAME="${LAUNCHER_VERSION_NAME:-0.3}"
echo "build-tools: $BT"; echo "platform: $PLAT"
W="$HERE/build"; rm -rf "$W/obj" "$W/dex"; mkdir -p "$W/obj" "$W/dex"
"$BT/aapt2" link -o "$W/base.apk" -I "$JAR" --manifest "$HERE/AndroidManifest.xml" \
  --min-sdk-version 21 --target-sdk-version 30 --version-code "$VCODE" --version-name "$VNAME"
javac -source 8 -target 8 -bootclasspath "$JAR" -classpath "$JAR" -d "$W/obj" -Xlint:-options $(find "$HERE/src" -name '*.java')
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
