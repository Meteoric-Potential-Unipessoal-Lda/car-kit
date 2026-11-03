# Тестирование car-kit / Testing car-kit

**RU** · Спасибо, что помогаете проверить набор на настоящих магнитолах. Это тестовая версия: она уже проверена на подставных магнитолах (FYT, Teyes, Topway TS10, PX5 MTCE, Reglink MTK, Android Automotive), но живых прогонов пока мало.

## Что нужно

- Ноутбук с Windows 8 / 10 / 11 или Mac.
- Android-магнитола и Wi-Fi, к которому подключены и ноутбук, и магнитола (проще всего — точка доступа на телефоне).
- 15–20 минут, машина стоит, зажигание включено (лучше с заведённым двигателем).

## Порядок

1. Скачайте `car-kit-<версия>.zip` из [Releases](https://github.com/Meteoric-Potential-Unipessoal-Lda/car-kit/releases/latest) и распакуйте.
2. Windows: один раз `prepare.bat` (скачает ADB и scrcpy), потом `start.bat`. Mac: `bash start.command`.
3. На магнитоле: Настройки → «Об устройстве» → 7 раз «Номер сборки» → «Для разработчиков» → «Отладка по USB».
4. Набор сам найдёт магнитолу в сети. На экране магнитолы нажмите «Разрешить». Не нашёл — кнопка «Как включить ADB» (там пароли заводского меню; **в заводском меню больше ничего не меняйте**).
5. **Сначала пункт 1 «Диагностика»** — он ничего не меняет. Пришлите результат (см. ниже).
6. Если хотите — пункт 2 «Оптимизация». Проверьте после неё: радио, Bluetooth (звонки и музыка), камеру заднего хода, кнопки руля, звук, CarPlay / Android Auto, навигацию. Что-то не так — пункт 3 «Откат».

## Без ноутбука: приложение car-kit Mobile

1. Скачайте `car-kit-mobile-<версия>.apk` из того же релиза на телефон и установите (разрешите установку из этого источника).
2. Включите на телефоне точку доступа, подключите к ней магнитолу, на магнитоле включите «Отладку по USB» (и «ADB по сети», если есть).
3. В приложении — «Найти магнитолу», на магнитоле — «Разрешить». Дальше так же: сначала только диагностика, потом по желанию план и проверка.
4. «Отправить отчёт» — текст отчёта в Telegram / WhatsApp / почту; приложите его к issue. Нужен порт 5555 — если приложение пишет «порт закрыт» или «беспроводная отладка», напишите, какая у вас магнитола.

## Что прислать

Создайте [issue «Отчёт о проверке»](https://github.com/Meteoric-Potential-Unipessoal-Lda/car-kit/issues/new?template=test-report.yml): модель магнитолы, что набор определил, что сработало, что нет.

Архив отчёта лежит в папке `reports` набора. В нём нет серийных номеров, IMEI и MAC-адресов, но есть список приложений и настроек магнитолы. Если не хотите выкладывать его публично — приложите только `report.txt` или пришлите архив автору лично.

Особенно полезно, если:
- набор написал «Платформа не распознана»;
- после оптимизации или перезагрузки что-то перестало работать;
- магнитола не нашлась в сети, хотя отладка включена (напишите, как в итоге включили ADB и какой пароль подошёл).

---

**EN** · Thanks for helping to test the kit on real head units. This is a test version: it passes scenarios on mock units (FYT, Teyes, Topway TS10, PX5 MTCE, Reglink MTK, Android Automotive), but there are few real runs yet.

1. Download `car-kit-<version>.zip` from Releases and unzip. Windows: run `prepare.bat` once (downloads ADB and scrcpy), then `start.bat`. Mac: `bash start.command`.
2. Head unit: Settings → About → tap *Build number* 7× → *Developer options* → *USB debugging*. Laptop and unit on the same Wi-Fi (a phone hotspot is easiest).
3. The kit finds the unit; tap *Allow* on its screen. **Start with option 1 (diagnostics)** — it changes nothing.
4. Optionally run option 2 (optimization) and check radio, Bluetooth, reverse camera, steering keys, sound, CarPlay / Android Auto. Option 3 rolls everything back.
5. No laptop? Install `car-kit-mobile-<version>.apk` from the same release on an Android phone, turn on its hotspot, connect the unit to it, tap «Find the head unit» and «Allow» on the unit. Network ADB on port 5555 is required.
6. Open a «Test report» issue with the unit model and results. The report archive (folder `reports`) has no serials / IMEI / MAC, but lists the unit's apps and settings — attach only `report.txt` if you prefer.
