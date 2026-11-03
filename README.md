# car-kit

**Download:** [latest release](https://github.com/Meteoric-Potential-Unipessoal-Lda/car-kit/releases/latest) · Windows: unzip → `prepare.bat` → `start.bat` · Mac: `bash start.command` · **Android phone:** `car-kit-mobile-X.Y.apk` from the same release ([mobile/](mobile/README.md)) · **Testers:** see [TESTING.md](TESTING.md)

**EN** · A repair technician's tool that safely checks, cleans up and speeds up **Android car head units** over ADB: FYT / UIS7862 / UIS8581 / UIS7870 (Teyes, Joying, Mekede, Hizpo), QF, Topway TS10 / TS18, Rockchip PX5 / PX6 MTCD / MTCE (Dasaita, Pumpkin, Xtrons, Eonon), cheap MediaTek (Reglink, HCN), Allwinner T3 / T5 / T8, ATOTO and other Android units. Runs on Windows or Mac and opens a local page in the browser (works offline). The head unit is found on the Wi-Fi network automatically (ADB port 5555), or connected by IP, by pairing code (Android 11+) or by USB.

Rule number one is **do no harm**. The whole vendor layer of the head unit is protected: MCU, CAN bus, radio, Bluetooth phone, reverse / 360 camera, steering wheel keys, sound / DSP, CarPlay / Android Auto, ACC sleep, launcher and factory settings. Vendor packages are touched only if they are in the curated list `data/car.tsv`; anything running as the system user is skipped; after every batch the kit checks that the head unit's core services are still alive and rolls the batch back if not.

Interface languages: Русский, Українська, English, Português, Español, Français, Italiano, Deutsch, Latviešu, Polski.

**RU** · Инструмент мастера, который безопасно проверяет, чистит и ускоряет **Android-магнитолы** по ADB. Ноутбук и магнитола в одной сети Wi-Fi (обычно точка доступа телефона клиента) — набор сам находит магнитолу. Главное правило — **не навредить**: слой производителя (MCU, CAN, радио, Bluetooth, камеры, кнопки руля, звук, CarPlay/Android Auto, сон по ACC) под защитой; диагностика — только чтение; изменения — после подтверждения, партиями с проверкой служб магнитолы, всё обратимо и записывается в журнал для отката.

Based on [phone-kit](https://github.com/Meteoric-Potential-Unipessoal-Lda/phone-kit) (same interface, plan, rollback and reports).

## Features / Что умеет

- **Finds the unit on Wi-Fi** — scans the laptop's local network for ADB on port 5555; IP without a port gets `:5555` automatically.
- **Platform detection** — FYT / Teyes / ATOTO, QF, Topway TS, MTCD / MTCE (HCT), Reglink, HCN, NWD, Allwinner, Android Automotive; chip (UIS7862 / UIS8581 / UIS7870, PX5 / PX6 / PX30, MediaTek, Qualcomm).
- **Head-unit diagnostics** — fake Android version (e.g. "Android 13" that is really SDK 29), MediaTek DuraSpeed, always-on network ADB, root ADB, heavy Google services on 2 GB units, the firmware's "app killer on sleep" with platform-specific advice.
- **Optimization** — junk from the [Universal Android Debloater](https://github.com/Universal-Debloater-Alliance/universal-android-debloater-next-generation) base and our list (ads / analytics, Adups FOTA, Chinese in-car services), animations 0.5x, *don't put navigation / music / CarPlay to sleep* (battery-optimization whitelist), background limits for unused apps, private DNS, cache cleanup.
- **Head unit screen on the laptop** — built-in [scrcpy](https://github.com/Genymobile/scrcpy): see and control the unit with the mouse (also through AnyDesk); car audio stays in the car.
- **Settings snapshot** (read-only) — all Android settings, platform properties, FYT `/oem/app/config.txt` (car model, CAN), to restore by hand after a reset or flashing.
- **Extra checks** — wrong clock (breaks HTTPS), auto time off, location off, weak Wi-Fi to the hotspot.
- **car-launcher** — our own lightweight home screen for head units (`launcher/`, plain Java, no Gradle; built and signed by GitHub Actions, shipped as `apk/car-launcher.apk`): Navigation / Music / Phone / Radio / All apps tiles, 6 favorites, clock, auto-start of navigation or music after power-on and after sleep. The kit can make it (or Agama, CarWebGuru…) the home screen, presses Home to verify and rolls back if the firmware intercepts the button; the stock launcher is never disabled.
- **car-kit Mobile (Android app)** — no laptop needed: install `car-kit-mobile-X.Y.apk` on the phone, share Wi-Fi from it, connect the head unit — the app finds the unit, runs the same diagnostics and the same safe plan (identical protection rules, checked by tests), applies in batches with core-service checks and rolls back from a log kept on the phone. See [mobile/README.md](mobile/README.md).
- **Your own APKs** — put `.apk` files into `apk/`; the plan offers to install them (unchecked), rollback removes what the kit installed.
- **Help for enabling ADB** — developer options, network ADB, common factory-menu passwords (shown, never guessed), `adb tcpip 5555`, Android 11+ pairing.
- **Reboot check** — finds the unit again on the network after reboot (address may change), warns when network ADB is not persistent.
- **Client report**, **before / after**, **rollback** (full or selective).
- **Android Automotive OS** (Volvo, Polestar, Renault…) — diagnostics only.

## How to use / Как пользоваться

1. Windows: unzip → `prepare.bat` once (downloads ADB) → `start.bat`. Mac: `bash start.command` (or `brew install powershell android-platform-tools`).
2. In the car: ignition on (engine running is better), head unit → Settings → About → tap *Build number* 7× → *Developer options* → *USB debugging*; connect the unit and the laptop to the same Wi-Fi.
3. The kit finds the unit; tap *Allow* on its screen. Choose 1 (diagnostics) or 2 (optimization), check the plan, confirm, test radio / Bluetooth / reverse camera / steering keys / CarPlay, reboot.
4. Option 3 rolls everything back from the log.

## Tests

`bash tests/run.sh` — scenarios on a mock adb; `bash tests/mobile/run.sh` — the phone app's logic, ADB protocol (fake adbd) and plan parity with the laptop kit; `tests/emu.sh` — the kit and car-launcher on a real Android 11 emulator in CI; (`tests/mock_adb.py`) for FYT, Teyes, Topway TS, MTCE, Reglink, Android Automotive and an unknown unit; `tests/webtest.py` — the browser interface; GitHub Actions also parse the script in Windows PowerShell 5.1.

## License

GPL-3.0 (the package base `data/uad.tsv` comes from UAD-ng, GPL-3.0).
