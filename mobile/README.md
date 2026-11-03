# car-kit Mobile

**RU** · Приложение для телефона вместо ноутбука: телефон раздаёт Wi-Fi, магнитола подключена к нему, приложение находит её (порт ADB 5555), делает диагностику и безопасную оптимизацию с откатом. Логика и правила защиты — те же, что у набора `carkit.ps1` (правила переносятся в `Pat.java` скриптом `dev/gen_mobile_patterns.py`; тест `tests/mobile/parity.sh` проверяет, что план телефона совпадает с планом ноутбука на всех подставных магнитолах).

- Подключение: свой клиент протокола ADB (`AdbConn.java`, RSA-ключ телефона, «Разрешить» на экране магнитолы). Беспроводная отладка Android 11+ с кодом сопряжения (TLS) пока не поддерживается — нужен обычный ADB по сети на порту 5555.
- Что делает: диагностика (только чтение) → план с галочками (лишнее системное, фон, «не усыплять» навигацию и музыку, анимации, частный DNS, кэш) → применение партиями по 5 пакетов с проверкой служб магнитолы (MCU, CAN, Bluetooth…) и откатом партии → журнал на телефоне → откат (весь или выборочно), даже через месяц.
- Чего нет по сравнению с ноутбуком: экран магнитолы (scrcpy), установка APK и смена рабочего стола, проверка после перезагрузки, архив отчёта (есть короткий текстовый отчёт — «Отправить отчёт»).
- Языки: 10, как у набора (тексты сообщений — из `data/lang`, свои строки — `strings.tsv`; нет перевода — английский).
- Android 5.0+ на телефоне, магнитола — любая с ADB по сети.

Сборка: `bash mobile/build.sh` (нужен Android SDK: build-tools, platforms; Gradle не нужен). В GitHub Actions собирается и подписывается тем же ключом, что car-launcher, и прикладывается к релизу как `car-kit-mobile-X.Y.apk`.

Тесты: `bash tests/mobile/run.sh` — логика на подставных магнитолах, протокол ADB через `tests/mobile/fake_adbd.py`, совпадение плана с набором; `tests/emu.sh` — приложение на настоящем Android 11 (эмулятор) подключается к нему же по ADB, применяет и откатывает.

**EN** · A phone app instead of the laptop: the phone shares Wi-Fi, the head unit joins it, the app finds the unit (ADB port 5555), runs diagnostics and the same safe, reversible optimization as `carkit.ps1` (same protection rules, generated into `Pat.java`; `tests/mobile/parity.sh` checks the phone plan equals the laptop plan). Own ADB protocol client; Android 11+ TLS wireless debugging is not supported yet. Build: `bash mobile/build.sh`; CI signs it with the car-launcher key and attaches `car-kit-mobile-X.Y.apk` to releases.
