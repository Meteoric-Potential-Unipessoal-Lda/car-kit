# car-launcher

Лёгкий рабочий стол для Android-магнитол — часть [car-kit](../README.md). Java без Gradle и без ресурсов (интерфейс в коде), minSdk 21, targetSdk 30.

- Плитки «Навигация / Музыка / Телефон / Радио / Все приложения», 6 избранных, часы и дата; тёмный фон, без анимаций и виджетов.
- Плитки заполняются сами (Waze, Яндекс Навигатор, 2ГИС, OsmAnd, Google Карты, Spotify, Яндекс Музыка, Poweramp, штатные плееры/радио/Bluetooth FYT, MTCD, Topway, HCN); долгое нажатие — выбрать другое приложение.
- Шестерёнка: что открывать при включении (навигацию, музыку, любое приложение) и после сна (когда магнитола включает экран).
- Кнопка «Домой» всегда возвращает на главный экран, «Назад» рабочий стол не закрывает.

Сборка: `ANDROID_HOME=... bash launcher/build.sh out/car-launcher.apk` (aapt2 + javac + d8 + zipalign + apksigner). Подпись — `LAUNCHER_KEYSTORE` + `LAUNCHER_KS_PASS` (alias `carlauncher`); в GitHub — секреты `LAUNCHER_KEYSTORE_B64` и `LAUNCHER_KS_PASS`, без них — временный тестовый ключ.
