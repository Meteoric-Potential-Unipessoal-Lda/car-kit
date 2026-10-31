# -*- coding: utf-8 -*-
# Тексты car-kit поверх языковых файлов phone-kit: NEW — новые ключи, OVR — переписанные под магнитолу.
# Языки: ru uk en (полностью вручную); pt es fr it de lv pl — новые ключи вручную + механическая замена «телефон» -> «магнитола».

NEW = {}
def n(k, en, ru, uk, pt=None, es=None, fr=None, it=None, de=None, lv=None, pl=None):
    NEW[k] = {'en': en, 'ru': ru, 'uk': uk, 'pt': pt, 'es': es, 'fr': fr, 'it': it, 'de': de, 'lv': lv, 'pl': pl}

OVR = {}
def o(k, en, ru, uk, **kw):
    d = {'en': en, 'ru': ru, 'uk': uk}; d.update(kw); OVR[k] = d

# ---------------------------------------------------------------- подключение
n('k001', '  S) find the head unit on the network (Wi-Fi, ADB port 5555)', '  S) найти магнитолу в сети (Wi-Fi, ADB порт 5555)', '  S) знайти магнітолу в мережі (Wi-Fi, ADB порт 5555)',
  pt='  S) procurar o autorrádio na rede (Wi-Fi, porta ADB 5555)', es='  S) buscar el autorradio en la red (Wi-Fi, puerto ADB 5555)', fr='  S) chercher l’autoradio sur le réseau (Wi-Fi, port ADB 5555)',
  it='  S) cerca lo stereo in rete (Wi-Fi, porta ADB 5555)', de='  S) Autoradio im Netzwerk suchen (WLAN, ADB-Port 5555)', lv='  S) atrast multivides bloku tīklā (Wi-Fi, ADB ports 5555)', pl='  S) znajdź radioodtwarzacz w sieci (Wi-Fi, port ADB 5555)')
n('k002', 'Car parked, ignition ON (ACC); better with the engine running, so the unit doesn\'t go to sleep and the car battery doesn\'t drain. Laptop and head unit on the same Wi-Fi (e.g. the client\'s phone hotspot).',
  'Машина стоит, зажигание включено (ACC); лучше с заведённым двигателем — чтобы магнитола не ушла в сон и не сел аккумулятор. Ноутбук и магнитола в одной сети Wi-Fi (например, точка доступа на телефоне клиента).',
  'Машина стоїть, запалювання увімкнене (ACC); краще з заведеним двигуном — щоб магнітола не заснула і не сів акумулятор. Ноутбук і магнітола в одній мережі Wi-Fi (наприклад, точка доступу на телефоні клієнта).',
  pt='Carro parado, ignição ligada (ACC); melhor com o motor a trabalhar, para o autorrádio não adormecer e a bateria não descarregar. Portátil e autorrádio na mesma rede Wi-Fi (p. ex. hotspot do telemóvel do cliente).',
  es='Coche parado, contacto puesto (ACC); mejor con el motor en marcha, para que el autorradio no se duerma y no se descargue la batería. Portátil y autorradio en la misma Wi-Fi (p. ej. el punto de acceso del móvil del cliente).',
  fr='Voiture à l’arrêt, contact mis (ACC) ; de préférence moteur tournant, pour que l’autoradio ne se mette pas en veille et que la batterie ne se vide pas. PC portable et autoradio sur le même Wi-Fi (p. ex. le partage de connexion du téléphone du client).',
  it='Auto ferma, quadro acceso (ACC); meglio con il motore acceso, così lo stereo non va in sospensione e la batteria non si scarica. Portatile e stereo sulla stessa Wi-Fi (ad es. l’hotspot del telefono del cliente).',
  de='Auto steht, Zündung an (ACC); besser mit laufendem Motor, damit das Autoradio nicht einschläft und die Batterie nicht leer wird. Laptop und Autoradio im selben WLAN (z. B. Hotspot des Kundenhandys).',
  lv='Auto stāv, aizdedze ieslēgta (ACC); labāk ar iedarbinātu dzinēju, lai multivides bloks neaizmigtu un akumulators neizlādētos. Klēpjdators un bloks vienā Wi-Fi tīklā (piemēram, klienta tālruņa tīklājs).',
  pl='Auto stoi, zapłon włączony (ACC); najlepiej z pracującym silnikiem, żeby radioodtwarzacz nie zasnął i nie rozładował akumulatora. Laptop i radioodtwarzacz w tej samej sieci Wi-Fi (np. hotspot telefonu klienta).')

# ---------------------------------------------------------------- как включить ADB
n('k010', 'How to enable ADB on the head unit:', 'Как включить ADB на магнитоле:', 'Як увімкнути ADB на магнітолі:',
  pt='Como ativar o ADB no autorrádio:', es='Cómo activar ADB en el autorradio:', fr='Comment activer ADB sur l’autoradio :', it='Come attivare ADB sullo stereo:', de='So schaltest du ADB am Autoradio ein:', lv='Kā ieslēgt ADB multivides blokā:', pl='Jak włączyć ADB w radioodtwarzaczu:')
n('k011', '  1) Settings -> About (device / system / info) -> tap «Build number» 7 times -> «Developer options» appear.',
  '  1) Настройки -> «Об устройстве» (О системе / Информация) -> 7 раз нажать «Номер сборки» -> появятся «Для разработчиков».',
  '  1) Налаштування -> «Про пристрій» (Про систему / Інформація) -> 7 разів натиснути «Номер збірки» -> з’являться «Для розробників».',
  pt='  1) Definições -> Acerca (dispositivo / sistema) -> tocar 7 vezes em «Número de compilação» -> aparecem as «Opções de programador».',
  es='  1) Ajustes -> Acerca de (dispositivo / sistema) -> tocar 7 veces «Número de compilación» -> aparecen las «Opciones de desarrollador».',
  fr='  1) Paramètres -> À propos (appareil / système) -> toucher 7 fois « Numéro de build » -> les « Options pour les développeurs » apparaissent.',
  it='  1) Impostazioni -> Info (dispositivo / sistema) -> tocca 7 volte «Numero build» -> compaiono le «Opzioni sviluppatore».',
  de='  1) Einstellungen -> Über (Gerät / System) -> 7× auf „Build-Nummer“ tippen -> „Entwickleroptionen“ erscheinen.',
  lv='  1) Iestatījumi -> Par ierīci (sistēmu) -> 7 reizes piesit «Būvējuma numurs» -> parādās «Izstrādātāja opcijas».',
  pl='  1) Ustawienia -> Informacje (o urządzeniu / systemie) -> 7 razy dotknij „Numer kompilacji” -> pojawią się „Opcje programisty”.')
n('k012', '  2) Developer options -> turn on «USB debugging». Connect the head unit to the same Wi-Fi as the laptop (the client\'s phone hotspot).',
  '  2) «Для разработчиков» -> включить «Отладку по USB». Подключить магнитолу к той же сети Wi-Fi, что и ноутбук (точка доступа телефона клиента).',
  '  2) «Для розробників» -> увімкнути «Налагодження USB». Підключити магнітолу до тієї ж мережі Wi-Fi, що й ноутбук (точка доступу телефона клієнта).',
  pt='  2) Opções de programador -> ativar «Depuração USB». Ligar o autorrádio ao mesmo Wi-Fi que o portátil (hotspot do telemóvel do cliente).',
  es='  2) Opciones de desarrollador -> activar «Depuración USB». Conectar el autorradio a la misma Wi-Fi que el portátil (punto de acceso del móvil del cliente).',
  fr='  2) Options pour les développeurs -> activer « Débogage USB ». Connecter l’autoradio au même Wi-Fi que le PC (partage de connexion du client).',
  it='  2) Opzioni sviluppatore -> attiva «Debug USB». Collega lo stereo alla stessa Wi-Fi del portatile (hotspot del telefono del cliente).',
  de='  2) Entwickleroptionen -> „USB-Debugging“ einschalten. Autoradio mit demselben WLAN wie der Laptop verbinden (Hotspot des Kunden).',
  lv='  2) Izstrādātāja opcijas -> ieslēgt «USB atkļūdošana». Pieslēgt bloku tam pašam Wi-Fi kā klēpjdatoru (klienta tālruņa tīklājs).',
  pl='  2) Opcje programisty -> włącz „Debugowanie USB”. Podłącz radioodtwarzacz do tej samej sieci Wi-Fi co laptop (hotspot telefonu klienta).')
n('k013', '  3) Then in the kit — S (search the network). Many head units open ADB over the network (port 5555) right after step 2.',
  '  3) Потом в наборе — S (поиск в сети). Многие магнитолы сразу после шага 2 открывают ADB по сети (порт 5555).',
  '  3) Потім у наборі — S (пошук у мережі). Багато магнітол одразу після кроку 2 відкривають ADB по мережі (порт 5555).',
  pt='  3) Depois, no kit — S (procurar na rede). Muitos autorrádios abrem o ADB pela rede (porta 5555) logo após o passo 2.',
  es='  3) Luego, en el kit — S (buscar en la red). Muchos autorradios abren ADB por red (puerto 5555) justo después del paso 2.',
  fr='  3) Puis dans le kit — S (recherche réseau). Beaucoup d’autoradios ouvrent ADB sur le réseau (port 5555) dès l’étape 2.',
  it='  3) Poi nel kit — S (cerca in rete). Molti stereo aprono ADB in rete (porta 5555) subito dopo il passo 2.',
  de='  3) Dann im Kit — S (Netzwerksuche). Viele Autoradios öffnen ADB übers Netzwerk (Port 5555) gleich nach Schritt 2.',
  lv='  3) Tad komplektā — S (meklēt tīklā). Daudzi bloki uzreiz pēc 2. soļa atver ADB tīklā (ports 5555).',
  pl='  3) Potem w zestawie — S (szukaj w sieci). Wiele radioodtwarzaczy od razu po kroku 2 otwiera ADB przez sieć (port 5555).')
n('k014', '  4) Android 11+ (UIS7870 and newer units): «Wireless debugging» -> «Pair device with pairing code» — option W.',
  '  4) Android 11+ (UIS7870 и новые магнитолы): «Беспроводная отладка» -> «Подключить устройство по коду» — пункт W.',
  '  4) Android 11+ (UIS7870 і нові магнітоли): «Бездротове налагодження» -> «Підключити пристрій за кодом» — пункт W.',
  pt='  4) Android 11+ (UIS7870 e unidades recentes): «Depuração sem fios» -> «Sincronizar dispositivo com código» — opção W.',
  es='  4) Android 11+ (UIS7870 y unidades nuevas): «Depuración inalámbrica» -> «Vincular dispositivo con código» — opción W.',
  fr='  4) Android 11+ (UIS7870 et modèles récents) : « Débogage sans fil » -> « Associer l’appareil avec un code » — option W.',
  it='  4) Android 11+ (UIS7870 e modelli recenti): «Debug wireless» -> «Accoppia dispositivo con codice» — opzione W.',
  de='  4) Android 11+ (UIS7870 und neuere Geräte): „Kabelloses Debugging“ -> „Gerät über Kopplungscode koppeln“ — Option W.',
  lv='  4) Android 11+ (UIS7870 un jaunāki bloki): «Bezvadu atkļūdošana» -> «Savienot ierīci ar kodu» — punkts W.',
  pl='  4) Android 11+ (UIS7870 i nowsze): „Debugowanie bezprzewodowe” -> „Sparuj urządzenie za pomocą kodu” — opcja W.')
n('k015', '  5) If S finds nothing: look in Developer options or in Factory settings for «ADB over network» / «Network debugging» / «ADB Wi-Fi» and turn it on.',
  '  5) Если S ничего не нашёл: поищите в «Для разработчиков» или в Заводских настройках «ADB по сети» / «Отладка по сети» / «ADB Wi-Fi» и включите.',
  '  5) Якщо S нічого не знайшов: пошукайте в «Для розробників» або в Заводських налаштуваннях «ADB по мережі» / «Налагодження по мережі» / «ADB Wi-Fi» і увімкніть.',
  pt='  5) Se o S não encontrar nada: procure nas Opções de programador ou nas Definições de fábrica «ADB pela rede» / «Depuração de rede» / «ADB Wi-Fi» e ative.',
  es='  5) Si S no encuentra nada: busque en Opciones de desarrollador o en Ajustes de fábrica «ADB por red» / «Depuración de red» / «ADB Wi-Fi» y actívelo.',
  fr='  5) Si S ne trouve rien : cherchez dans les Options développeurs ou les Réglages usine « ADB réseau » / « Débogage réseau » / « ADB Wi-Fi » et activez-le.',
  it='  5) Se S non trova nulla: cerca nelle Opzioni sviluppatore o nelle Impostazioni di fabbrica «ADB in rete» / «Debug di rete» / «ADB Wi-Fi» e attivalo.',
  de='  5) Findet S nichts: in den Entwickleroptionen oder Werkseinstellungen nach „ADB über Netzwerk“ / „Netzwerk-Debugging“ / „ADB WLAN“ suchen und einschalten.',
  lv='  5) Ja S neko neatrod: meklē Izstrādātāja opcijās vai Rūpnīcas iestatījumos «ADB tīklā» / «Tīkla atkļūdošana» / «ADB Wi-Fi» un ieslēdz.',
  pl='  5) Jeśli S nic nie znajdzie: poszukaj w Opcjach programisty lub Ustawieniach fabrycznych „ADB przez sieć” / „Debugowanie sieciowe” / „ADB Wi-Fi” i włącz.')
n('k016', '     Factory settings are usually in Settings -> Car settings (or About) and ask for a password. Common ones (to try by hand — the kit doesn\'t guess them):',
  '     Заводские настройки обычно в Настройки -> Настройки автомобиля (или «Об устройстве») и просят пароль. Частые (попробовать руками — набор их не подбирает):',
  '     Заводські налаштування зазвичай у Налаштування -> Налаштування авто (або «Про пристрій») і просять пароль. Поширені (спробувати вручну — набір їх не підбирає):',
  pt='     As definições de fábrica costumam estar em Definições -> Carro (ou Acerca) e pedem senha. Comuns (tentar à mão — o kit não as adivinha):',
  es='     Los ajustes de fábrica suelen estar en Ajustes -> Coche (o Acerca de) y piden contraseña. Habituales (probar a mano — el kit no las adivina):',
  fr='     Les réglages usine sont souvent dans Paramètres -> Voiture (ou À propos) et demandent un code. Courants (à essayer à la main — le kit ne les devine pas) :',
  it='     Le impostazioni di fabbrica di solito sono in Impostazioni -> Auto (o Info) e chiedono una password. Comuni (da provare a mano — il kit non le indovina):',
  de='     Werkseinstellungen liegen meist unter Einstellungen -> Fahrzeug (oder Über) und fragen ein Passwort ab. Häufige (von Hand probieren — das Kit rät sie nicht):',
  lv='     Rūpnīcas iestatījumi parasti ir Iestatījumi -> Auto (vai Par ierīci) un prasa paroli. Biežākās (izmēģināt ar roku — komplekts tās neuzmin):',
  pl='     Ustawienia fabryczne są zwykle w Ustawienia -> Samochód (lub Informacje) i pytają o hasło. Częste (spróbuj ręcznie — zestaw ich nie zgaduje):')
n('k017', '       FYT / Joying / Mekede / Teyes-like: 3368    QF / Hizpo: 8888    Topway TS10/TS18: 8888 (sometimes 3368)',
  '       FYT / Joying / Mekede / похожие на Teyes: 3368    QF / Hizpo: 8888    Topway TS10/TS18: 8888 (иногда 3368)',
  '       FYT / Joying / Mekede / схожі на Teyes: 3368    QF / Hizpo: 8888    Topway TS10/TS18: 8888 (іноді 3368)')
n('k018', '       Rockchip MTCD/MTCE (PX5/PX6): 126 (Malaysk etc.: 7890)    cheap MTK / Allwinner: 1234, 0000, 123456    others: 1617, 113266',
  '       Rockchip MTCD/MTCE (PX5/PX6): 126 (Malaysk и др.: 7890)    дешёвые MTK / Allwinner: 1234, 0000, 123456    другие: 1617, 113266',
  '       Rockchip MTCD/MTCE (PX5/PX6): 126 (Malaysk та ін.: 7890)    дешеві MTK / Allwinner: 1234, 0000, 123456    інші: 1617, 113266')
n('k019', '     Change nothing else in factory settings (car model, CAN protocol, screen, MCU) — the unit may stop seeing the car.',
  '     Больше в заводских настройках ничего не менять (модель машины, протокол CAN, экран, MCU) — магнитола может перестать видеть машину.',
  '     Більше в заводських налаштуваннях нічого не змінювати (модель авто, протокол CAN, екран, MCU) — магнітола може перестати бачити авто.',
  pt='     Não mude mais nada nas definições de fábrica (modelo do carro, protocolo CAN, ecrã, MCU) — o autorrádio pode deixar de ver o carro.',
  es='     No cambie nada más en los ajustes de fábrica (modelo de coche, protocolo CAN, pantalla, MCU): el autorradio puede dejar de ver el coche.',
  fr='     Ne changez rien d’autre dans les réglages usine (modèle de voiture, protocole CAN, écran, MCU) — l’autoradio pourrait ne plus voir la voiture.',
  it='     Non cambiare altro nelle impostazioni di fabbrica (modello auto, protocollo CAN, schermo, MCU): lo stereo potrebbe non vedere più l’auto.',
  de='     Sonst nichts in den Werkseinstellungen ändern (Fahrzeugmodell, CAN-Protokoll, Bildschirm, MCU) — sonst erkennt das Radio das Auto evtl. nicht mehr.',
  lv='     Neko citu rūpnīcas iestatījumos nemainīt (auto modelis, CAN protokols, ekrāns, MCU) — bloks var pārstāt redzēt auto.',
  pl='     Niczego więcej w ustawieniach fabrycznych nie zmieniaj (model auta, protokół CAN, ekran, MCU) — radio może przestać widzieć samochód.')
n('k020', '  6) No network ADB at all (often Android 10 and older): once connect the laptop by USB cable (if a port of the unit supports OTG/device mode)',
  '  6) ADB по сети нет совсем (часто Android 10 и старше): один раз подключить ноутбук кабелем USB (если порт магнитолы умеет OTG/режим устройства)',
  '  6) ADB по мережі немає зовсім (часто Android 10 і старші): один раз підключити ноутбук кабелем USB (якщо порт магнітоли вміє OTG/режим пристрою)',
  pt='  6) Sem ADB pela rede (muitas vezes Android 10 e anteriores): ligue o portátil uma vez por cabo USB (se uma porta do autorrádio suportar OTG/modo dispositivo)',
  es='  6) Sin ADB por red (a menudo Android 10 y anteriores): conecte una vez el portátil por cable USB (si un puerto del autorradio admite OTG/modo dispositivo)',
  fr='  6) Pas d’ADB réseau du tout (souvent Android 10 et antérieurs) : brancher une fois le PC en USB (si un port de l’autoradio gère l’OTG/mode appareil)',
  it='  6) Nessun ADB in rete (spesso Android 10 e precedenti): collega una volta il portatile via cavo USB (se una porta dello stereo supporta OTG/modalità dispositivo)',
  de='  6) Gar kein Netzwerk-ADB (oft Android 10 und älter): den Laptop einmal per USB-Kabel anschließen (wenn ein Port des Radios OTG/Gerätemodus kann)',
  lv='  6) ADB tīklā nav vispār (bieži Android 10 un vecāki): vienreiz pieslēgt klēpjdatoru ar USB kabeli (ja bloka ports atbalsta OTG/ierīces režīmu)',
  pl='  6) Brak ADB przez sieć (często Android 10 i starsze): raz podłącz laptopa kablem USB (jeśli port radia obsługuje OTG/tryb urządzenia)')
n('k021', '     and switch to network mode with  adb tcpip 5555  — it works until the next reboot.',
  '     и включить сетевой режим командой  adb tcpip 5555  — работает до следующей перезагрузки.',
  '     і увімкнути мережевий режим командою  adb tcpip 5555  — працює до наступного перезавантаження.',
  pt='     e ativar o modo de rede com  adb tcpip 5555  — funciona até ao próximo reinício.', es='     y activar el modo red con  adb tcpip 5555  — funciona hasta el próximo reinicio.',
  fr='     et passer en mode réseau avec  adb tcpip 5555  — valable jusqu’au prochain redémarrage.', it='     e attivare la modalità rete con  adb tcpip 5555  — funziona fino al prossimo riavvio.',
  de='     und mit  adb tcpip 5555  in den Netzwerkmodus schalten — gilt bis zum nächsten Neustart.', lv='     un ieslēgt tīkla režīmu ar  adb tcpip 5555  — darbojas līdz nākamajai restartēšanai.',
  pl='     i włącz tryb sieciowy poleceniem  adb tcpip 5555  — działa do następnego restartu.')
n('k022', '  7) ATOTO S8 / FYT without such an option: the open-source app atoto-adb-via-wifi (github.com/lrehmann/atoto-adb-via-wifi) turns on ADB over Wi-Fi.',
  '  7) ATOTO S8 / FYT без такого пункта: открытое приложение atoto-adb-via-wifi (github.com/lrehmann/atoto-adb-via-wifi) включает ADB по Wi-Fi.',
  '  7) ATOTO S8 / FYT без такого пункту: відкритий застосунок atoto-adb-via-wifi (github.com/lrehmann/atoto-adb-via-wifi) вмикає ADB по Wi-Fi.',
  pt='  7) ATOTO S8 / FYT sem essa opção: a app aberta atoto-adb-via-wifi (github.com/lrehmann/atoto-adb-via-wifi) ativa o ADB por Wi-Fi.',
  es='  7) ATOTO S8 / FYT sin esa opción: la app abierta atoto-adb-via-wifi (github.com/lrehmann/atoto-adb-via-wifi) activa ADB por Wi-Fi.',
  fr='  7) ATOTO S8 / FYT sans cette option : l’appli libre atoto-adb-via-wifi (github.com/lrehmann/atoto-adb-via-wifi) active ADB en Wi-Fi.',
  it='  7) ATOTO S8 / FYT senza questa opzione: l’app open source atoto-adb-via-wifi (github.com/lrehmann/atoto-adb-via-wifi) attiva ADB via Wi-Fi.',
  de='  7) ATOTO S8 / FYT ohne diese Option: die offene App atoto-adb-via-wifi (github.com/lrehmann/atoto-adb-via-wifi) schaltet ADB über WLAN ein.',
  lv='  7) ATOTO S8 / FYT bez šādas opcijas: atvērtā lietotne atoto-adb-via-wifi (github.com/lrehmann/atoto-adb-via-wifi) ieslēdz ADB caur Wi-Fi.',
  pl='  7) ATOTO S8 / FYT bez takiej opcji: otwarta aplikacja atoto-adb-via-wifi (github.com/lrehmann/atoto-adb-via-wifi) włącza ADB przez Wi-Fi.')
n('k023', '  The prompt «Allow USB debugging?» appears on the head unit screen — tap «Allow» (check «Always»).',
  '  На экране магнитолы появится запрос «Разрешить отладку по USB?» — нажать «Разрешить» (галочка «Всегда»).',
  '  На екрані магнітоли з’явиться запит «Дозволити налагодження USB?» — натиснути «Дозволити» (галочка «Завжди»).',
  pt='  No ecrã do autorrádio aparece «Permitir depuração USB?» — toque em «Permitir» (marque «Sempre»).', es='  En la pantalla del autorradio aparece «¿Permitir depuración USB?» — pulse «Permitir» (marque «Siempre»).',
  fr='  L’écran de l’autoradio affiche « Autoriser le débogage USB ? » — touchez « Autoriser » (cochez « Toujours »).', it='  Sullo schermo dello stereo compare «Consentire il debug USB?» — tocca «Consenti» (spunta «Sempre»).',
  de='  Auf dem Radio erscheint „USB-Debugging zulassen?“ — „Zulassen“ tippen („Immer“ anhaken).', lv='  Bloka ekrānā parādās «Atļaut USB atkļūdošanu?» — piesit «Atļaut» (atzīmē «Vienmēr»).',
  pl='  Na ekranie radia pojawi się „Zezwolić na debugowanie USB?” — dotknij „Zezwól” (zaznacz „Zawsze”).')
n('k024', '  Android Automotive cars (Volvo, Polestar, Renault with Google built-in): ADB is closed to owners, the kit can\'t help there.',
  '  Машины на Android Automotive (Volvo, Polestar, Renault с Google built-in): ADB владельцу закрыт, набор там не поможет.',
  '  Авто на Android Automotive (Volvo, Polestar, Renault з Google built-in): ADB власнику закритий, набір там не допоможе.',
  pt='  Carros com Android Automotive (Volvo, Polestar, Renault com Google integrado): o ADB está fechado ao dono, o kit não ajuda.',
  es='  Coches con Android Automotive (Volvo, Polestar, Renault con Google integrado): ADB está cerrado al dueño, el kit no ayuda ahí.',
  fr='  Voitures sous Android Automotive (Volvo, Polestar, Renault avec Google intégré) : ADB fermé au propriétaire, le kit n’y peut rien.',
  it='  Auto con Android Automotive (Volvo, Polestar, Renault con Google integrato): ADB è chiuso al proprietario, il kit non può aiutare.',
  de='  Autos mit Android Automotive (Volvo, Polestar, Renault mit Google integriert): ADB ist für Besitzer gesperrt, das Kit hilft dort nicht.',
  lv='  Auto ar Android Automotive (Volvo, Polestar, Renault ar Google iebūvētu): ADB īpašniekam slēgts, komplekts tur nepalīdzēs.',
  pl='  Auta z Android Automotive (Volvo, Polestar, Renault z Google): ADB jest zamknięte dla właściciela, zestaw tam nie pomoże.')
n('k025', '  Laptop and unit on different networks (guest Wi-Fi, client isolation on the router) won\'t see each other — use the phone hotspot.',
  '  Ноутбук и магнитола в разных сетях (гостевой Wi-Fi, изоляция клиентов на роутере) друг друга не видят — используйте точку доступа телефона.',
  '  Ноутбук і магнітола в різних мережах (гостьовий Wi-Fi, ізоляція клієнтів на роутері) одне одного не бачать — використайте точку доступу телефона.',
  pt='  Portátil e autorrádio em redes diferentes (Wi-Fi de convidados, isolamento no router) não se veem — use o hotspot do telemóvel.',
  es='  Portátil y autorradio en redes distintas (Wi-Fi de invitados, aislamiento en el router) no se ven — use el punto de acceso del móvil.',
  fr='  PC et autoradio sur des réseaux différents (Wi-Fi invité, isolation sur le routeur) ne se voient pas — utilisez le partage du téléphone.',
  it='  Portatile e stereo su reti diverse (Wi-Fi ospiti, isolamento client sul router) non si vedono — usa l’hotspot del telefono.',
  de='  Laptop und Radio in verschiedenen Netzen (Gast-WLAN, Client-Isolation am Router) sehen sich nicht — Handy-Hotspot benutzen.',
  lv='  Klēpjdators un bloks dažādos tīklos (viesu Wi-Fi, klientu izolācija maršrutētājā) viens otru neredz — izmanto tālruņa tīklāju.',
  pl='  Laptop i radio w różnych sieciach (Wi-Fi dla gości, izolacja klientów w routerze) się nie widzą — użyj hotspotu telefonu.')
for k in ('k017', 'k018'):
    for l in ('pt', 'es', 'fr', 'it', 'de', 'lv', 'pl'):
        NEW[k][l] = NEW[k]['en'].replace('(sometimes 3368)', '(3368)').replace('cheap', '').replace('others:', '…').replace('etc.', '…')

# ---------------------------------------------------------------- поиск в сети
n('k030', 'Looking for the head unit on the network (ADB, port 5555)...', 'Ищу магнитолу в сети (ADB, порт 5555)...', 'Шукаю магнітолу в мережі (ADB, порт 5555)...',
  pt='A procurar o autorrádio na rede (ADB, porta 5555)...', es='Buscando el autorradio en la red (ADB, puerto 5555)...', fr='Recherche de l’autoradio sur le réseau (ADB, port 5555)...',
  it='Cerco lo stereo in rete (ADB, porta 5555)...', de='Suche das Autoradio im Netzwerk (ADB, Port 5555)...', lv='Meklēju bloku tīklā (ADB, ports 5555)...', pl='Szukam radioodtwarzacza w sieci (ADB, port 5555)...')
n('k031', 'This computer has no local network (Wi-Fi / hotspot) — connect it to the same Wi-Fi as the head unit.',
  'У компьютера нет локальной сети (Wi-Fi / точки доступа) — подключи его к той же сети, что и магнитолу.',
  'У комп’ютера немає локальної мережі (Wi-Fi / точки доступу) — підключи його до тієї ж мережі, що й магнітолу.',
  pt='Este computador não tem rede local (Wi-Fi / hotspot) — ligue-o ao mesmo Wi-Fi do autorrádio.', es='Este ordenador no tiene red local (Wi-Fi / punto de acceso) — conéctelo a la misma Wi-Fi que el autorradio.',
  fr='Cet ordinateur n’a pas de réseau local (Wi-Fi / partage) — connectez-le au même Wi-Fi que l’autoradio.', it='Questo computer non ha una rete locale (Wi-Fi / hotspot) — collegalo alla stessa Wi-Fi dello stereo.',
  de='Dieser Computer hat kein lokales Netz (WLAN / Hotspot) — mit demselben WLAN wie das Autoradio verbinden.', lv='Datoram nav lokālā tīkla (Wi-Fi / tīklāja) — pieslēdz to tam pašam tīklam, kur bloks.',
  pl='Ten komputer nie ma sieci lokalnej (Wi-Fi / hotspot) — podłącz go do tej samej sieci co radio.')
n('k032', '  checking network {0} — a few seconds', '  проверяю сеть {0} — несколько секунд', '  перевіряю мережу {0} — кілька секунд',
  pt='  a verificar a rede {0} — alguns segundos', es='  comprobando la red {0} — unos segundos', fr='  vérification du réseau {0} — quelques secondes', it='  controllo la rete {0} — qualche secondo',
  de='  prüfe Netz {0} — ein paar Sekunden', lv='  pārbaudu tīklu {0} — dažas sekundes', pl='  sprawdzam sieć {0} — kilka sekund')
n('k033', 'No head unit with network ADB found.', 'Магнитолы с ADB по сети не нашлось.', 'Магнітоли з ADB по мережі не знайшлося.',
  pt='Nenhum autorrádio com ADB pela rede encontrado.', es='No se encontró ningún autorradio con ADB por red.', fr='Aucun autoradio avec ADB réseau trouvé.', it='Nessuno stereo con ADB in rete trovato.',
  de='Kein Autoradio mit Netzwerk-ADB gefunden.', lv='Bloks ar ADB tīklā netika atrasts.', pl='Nie znaleziono radia z ADB przez sieć.')
n('k034', '  Check: the unit is on the same Wi-Fi as the laptop; «USB debugging» is on; ADB over network is enabled (H — how).',
  '  Проверь: магнитола в той же сети Wi-Fi, что ноутбук; «Отладка по USB» включена; включён ADB по сети (H — как).',
  '  Перевір: магнітола в тій самій мережі Wi-Fi, що ноутбук; «Налагодження USB» увімкнене; увімкнено ADB по мережі (H — як).',
  pt='  Verifique: o autorrádio está no mesmo Wi-Fi que o portátil; «Depuração USB» ativa; ADB pela rede ativo (H — como).',
  es='  Compruebe: el autorradio está en la misma Wi-Fi que el portátil; «Depuración USB» activa; ADB por red activo (H — cómo).',
  fr='  Vérifiez : l’autoradio est sur le même Wi-Fi que le PC ; « Débogage USB » activé ; ADB réseau activé (H — comment).',
  it='  Controlla: lo stereo è sulla stessa Wi-Fi del portatile; «Debug USB» attivo; ADB in rete attivo (H — come).',
  de='  Prüfen: Radio im selben WLAN wie der Laptop; „USB-Debugging“ an; ADB über Netzwerk an (H — wie).',
  lv='  Pārbaudi: bloks tajā pašā Wi-Fi, kur klēpjdators; «USB atkļūdošana» ieslēgta; ADB tīklā ieslēgts (H — kā).',
  pl='  Sprawdź: radio w tej samej sieci Wi-Fi co laptop; „Debugowanie USB” włączone; ADB przez sieć włączone (H — jak).')
n('k035', '  Android 11+: pair by code — W. If you know the unit\'s IP (Settings -> Wi-Fi -> network details) — I.',
  '  Android 11+: сопряжение по коду — W. Знаешь IP магнитолы (Настройки -> Wi-Fi -> сведения о сети) — I.',
  '  Android 11+: сполучення за кодом — W. Знаєш IP магнітоли (Налаштування -> Wi-Fi -> відомості про мережу) — I.',
  pt='  Android 11+: sincronizar com código — W. Sabe o IP do autorrádio (Definições -> Wi-Fi -> detalhes) — I.', es='  Android 11+: vincular con código — W. Si sabe la IP del autorradio (Ajustes -> Wi-Fi -> detalles) — I.',
  fr='  Android 11+ : association par code — W. Vous connaissez l’IP (Paramètres -> Wi-Fi -> détails) — I.', it='  Android 11+: accoppiamento con codice — W. Conosci l’IP dello stereo (Impostazioni -> Wi-Fi -> dettagli) — I.',
  de='  Android 11+: Kopplung per Code — W. IP des Radios bekannt (Einstellungen -> WLAN -> Details) — I.', lv='  Android 11+: savienošana ar kodu — W. Zini bloka IP (Iestatījumi -> Wi-Fi -> tīkla informācija) — I.',
  pl='  Android 11+: parowanie kodem — W. Znasz IP radia (Ustawienia -> Wi-Fi -> szczegóły sieci) — I.')
n('k036', 'ADB found at: {0}', 'ADB найден: {0}', 'ADB знайдено: {0}', pt='ADB encontrado em: {0}', es='ADB encontrado en: {0}', fr='ADB trouvé sur : {0}', it='ADB trovato su: {0}', de='ADB gefunden: {0}', lv='ADB atrasts: {0}', pl='Znaleziono ADB: {0}')
n('k037', 'Several head units found — which one (number)', 'Нашлось несколько магнитол — какая (номер)', 'Знайшлося кілька магнітол — яка (номер)',
  pt='Vários autorrádios encontrados — qual (número)', es='Varios autorradios encontrados — cuál (número)', fr='Plusieurs autoradios trouvés — lequel (numéro)', it='Trovati più stereo — quale (numero)',
  de='Mehrere Autoradios gefunden — welches (Nummer)', lv='Atrasti vairāki bloki — kurš (numurs)', pl='Znaleziono kilka radioodtwarzaczy — który (numer)')
n('k038', '  The unit answers on the network, but its ADB port is closed: turn on «USB debugging» / ADB over network (H — how).',
  '  Магнитола в сети, но порт ADB закрыт: включи «Отладку по USB» / ADB по сети (H — как).',
  '  Магнітола в мережі, але порт ADB закритий: увімкни «Налагодження USB» / ADB по мережі (H — як).',
  pt='  O autorrádio responde na rede, mas a porta ADB está fechada: ative a «Depuração USB» / ADB pela rede (H — como).',
  es='  El autorradio responde en la red, pero su puerto ADB está cerrado: active «Depuración USB» / ADB por red (H — cómo).',
  fr='  L’autoradio répond sur le réseau, mais son port ADB est fermé : activez « Débogage USB » / ADB réseau (H — comment).',
  it='  Lo stereo risponde in rete, ma la porta ADB è chiusa: attiva «Debug USB» / ADB in rete (H — come).',
  de='  Das Radio ist im Netz, aber der ADB-Port ist zu: „USB-Debugging“ / ADB über Netzwerk einschalten (H — wie).',
  lv='  Bloks tīklā ir, bet ADB ports slēgts: ieslēdz «USB atkļūdošana» / ADB tīklā (H — kā).',
  pl='  Radio jest w sieci, ale port ADB jest zamknięty: włącz „Debugowanie USB” / ADB przez sieć (H — jak).')
n('k039', '  Look at the head unit screen: tap «Allow» in the «Allow USB debugging?» window (check «Always»).',
  '  Посмотри на экран магнитолы: нажми «Разрешить» в окне «Разрешить отладку по USB?» (галочка «Всегда»).',
  '  Подивись на екран магнітоли: натисни «Дозволити» у вікні «Дозволити налагодження USB?» (галочка «Завжди»).',
  pt='  Olhe para o ecrã do autorrádio: toque em «Permitir» na janela «Permitir depuração USB?» (marque «Sempre»).', es='  Mire la pantalla del autorradio: pulse «Permitir» en «¿Permitir depuración USB?» (marque «Siempre»).',
  fr='  Regardez l’écran de l’autoradio : touchez « Autoriser » dans « Autoriser le débogage USB ? » (cochez « Toujours »).', it='  Guarda lo schermo dello stereo: tocca «Consenti» in «Consentire il debug USB?» (spunta «Sempre»).',
  de='  Auf das Radio schauen: im Fenster „USB-Debugging zulassen?“ auf „Zulassen“ tippen („Immer“ anhaken).', lv='  Paskaties bloka ekrānā: logā «Atļaut USB atkļūdošanu?» piesit «Atļaut» (atzīmē «Vienmēr»).',
  pl='  Spójrz na ekran radia: dotknij „Zezwól” w oknie „Zezwolić na debugowanie USB?” (zaznacz „Zawsze”).')

# ---------------------------------------------------------------- проверки и «не усыплять»
n('k040', 'head unit service {0} stopped', 'остановилась служба магнитолы {0}', 'зупинилася служба магнітоли {0}', pt='o serviço do autorrádio {0} parou', es='se detuvo el servicio del autorradio {0}',
  fr='le service de l’autoradio {0} s’est arrêté', it='si è fermato il servizio dello stereo {0}', de='Dienst des Autoradios {0} ist gestoppt', lv='apstājās bloka serviss {0}', pl='zatrzymała się usługa radia {0}')
n('k041', 'won\'t be put to sleep in the background (battery optimization off): {0}', 'не будет усыпляться в фоне (оптимизация батареи выключена): {0}', 'не присинатиметься у фоні (оптимізацію батареї вимкнено): {0}',
  pt='não será adormecido em segundo plano (otimização de bateria desligada): {0}', es='no se dormirá en segundo plano (optimización de batería desactivada): {0}', fr='ne sera plus endormi en arrière-plan (optimisation batterie désactivée) : {0}',
  it='non verrà sospeso in background (ottimizzazione batteria disattivata): {0}', de='wird im Hintergrund nicht schlafen gelegt (Akku-Optimierung aus): {0}', lv='fonā netiks iemidzināts (akumulatora optimizācija izslēgta): {0}', pl='nie będzie usypiany w tle (optymalizacja baterii wyłączona): {0}')
n('k042', '{0}: already excluded from battery optimization', '{0}: уже исключён из оптимизации батареи', '{0}: вже виключено з оптимізації батареї', pt='{0}: já excluído da otimização de bateria', es='{0}: ya excluido de la optimización de batería',
  fr='{0} : déjà exclu de l’optimisation batterie', it='{0}: già escluso dall’ottimizzazione batteria', de='{0}: schon von der Akku-Optimierung ausgenommen', lv='{0}: jau izslēgts no akumulatora optimizācijas', pl='{0}: już wyłączony z optymalizacji baterii')
n('k043', '{0}: couldn\'t exclude from battery optimization', '{0}: не удалось исключить из оптимизации батареи', '{0}: не вдалося виключити з оптимізації батареї', pt='{0}: não foi possível excluir da otimização de bateria',
  es='{0}: no se pudo excluir de la optimización de batería', fr='{0} : impossible d’exclure de l’optimisation batterie', it='{0}: impossibile escludere dall’ottimizzazione batteria', de='{0}: konnte nicht von der Akku-Optimierung ausgenommen werden',
  lv='{0}: neizdevās izslēgt no akumulatora optimizācijas', pl='{0}: nie udało się wyłączyć z optymalizacji baterii')
n('k044', 'battery optimization back on: {0}', 'оптимизация батареи возвращена: {0}', 'оптимізацію батареї повернуто: {0}', pt='otimização de bateria reposta: {0}', es='optimización de batería restaurada: {0}',
  fr='optimisation batterie rétablie : {0}', it='ottimizzazione batteria ripristinata: {0}', de='Akku-Optimierung wieder an: {0}', lv='akumulatora optimizācija atjaunota: {0}', pl='przywrócono optymalizację baterii: {0}')
n('k045', '- {0}: return battery optimization', '- {0}: вернуть оптимизацию батареи', '- {0}: повернути оптимізацію батареї', pt='- {0}: repor a otimização de bateria', es='- {0}: restaurar la optimización de batería',
  fr='- {0} : rétablir l’optimisation batterie', it='- {0}: ripristinare l’ottimizzazione batteria', de='- {0}: Akku-Optimierung zurückgeben', lv='- {0}: atjaunot akumulatora optimizāciju', pl='- {0}: przywrócić optymalizację baterii')
n('k046', 'Navigation/music won\'t be unloaded in the background: {0}', 'Навигация/музыка не будет выгружаться в фоне: {0}', 'Навігація/музика не вивантажуватиметься у фоні: {0}',
  pt='Navegação/música não será descarregada em segundo plano: {0}', es='La navegación/música no se cerrará en segundo plano: {0}', fr='Navigation/musique ne sera plus déchargée en arrière-plan : {0}',
  it='Navigazione/musica non verrà chiusa in background: {0}', de='Navigation/Musik wird im Hintergrund nicht mehr entladen: {0}', lv='Navigācija/mūzika fonā netiks izlādēta: {0}', pl='Nawigacja/muzyka nie będzie zamykana w tle: {0}')
n('k047', 'Don\'t put to sleep in the background: {0} — {1}', 'Не усыплять в фоне: {0} — {1}', 'Не присипляти у фоні: {0} — {1}', pt='Não adormecer em segundo plano: {0} — {1}', es='No dormir en segundo plano: {0} — {1}',
  fr='Ne pas endormir en arrière-plan : {0} — {1}', it='Non sospendere in background: {0} — {1}', de='Im Hintergrund nicht schlafen legen: {0} — {1}', lv='Neiemidzināt fonā: {0} — {1}', pl='Nie usypiaj w tle: {0} — {1}')
n('k048', 'navigation, music, CarPlay / Android Auto — keep in the background', 'навигация, музыка, CarPlay / Android Auto — не выгружать', 'навігація, музика, CarPlay / Android Auto — не вивантажувати',
  pt='navegação, música, CarPlay / Android Auto — manter em segundo plano', es='navegación, música, CarPlay / Android Auto — mantener en segundo plano', fr='navigation, musique, CarPlay / Android Auto — garder en arrière-plan',
  it='navigazione, musica, CarPlay / Android Auto — tenere in background', de='Navigation, Musik, CarPlay / Android Auto — im Hintergrund halten', lv='navigācija, mūzika, CarPlay / Android Auto — paturēt fonā', pl='nawigacja, muzyka, CarPlay / Android Auto — trzymać w tle')
n('k049', 'runs as the system (part of the firmware)', 'работает от имени системы (часть прошивки)', 'працює від імені системи (частина прошивки)', pt='corre como sistema (parte do firmware)', es='se ejecuta como sistema (parte del firmware)',
  fr='s’exécute comme système (partie du firmware)', it='gira come sistema (parte del firmware)', de='läuft als System (Teil der Firmware)', lv='darbojas sistēmas vārdā (programmaparatūras daļa)', pl='działa jako system (część oprogramowania)')

# ---------------------------------------------------------------- перезагрузка
n('k050', '  The head unit is rebooting. After boot it reconnects to the same Wi-Fi by itself — the kit looks for it at the old address and across the network.',
  '  Магнитола перезагружается. После загрузки она сама подключится к той же сети Wi-Fi — набор ищет её по старому адресу и по всей сети.',
  '  Магнітола перезавантажується. Після завантаження вона сама підключиться до тієї ж мережі Wi-Fi — набір шукає її за старою адресою і по всій мережі.',
  pt='  O autorrádio está a reiniciar. Depois volta sozinho ao mesmo Wi-Fi — o kit procura-o no endereço antigo e em toda a rede.', es='  El autorradio se reinicia. Después vuelve solo a la misma Wi-Fi — el kit lo busca en la dirección anterior y en toda la red.',
  fr='  L’autoradio redémarre. Ensuite il se reconnecte seul au même Wi-Fi — le kit le cherche à l’ancienne adresse et sur tout le réseau.', it='  Lo stereo si riavvia. Poi si ricollega da solo alla stessa Wi-Fi — il kit lo cerca al vecchio indirizzo e in tutta la rete.',
  de='  Das Autoradio startet neu. Danach verbindet es sich selbst mit demselben WLAN — das Kit sucht es an der alten Adresse und im ganzen Netz.', lv='  Bloks restartējas. Pēc ielādes tas pats pieslēgsies tam pašam Wi-Fi — komplekts meklē to vecajā adresē un visā tīklā.',
  pl='  Radioodtwarzacz się restartuje. Po starcie sam połączy się z tą samą siecią Wi-Fi — zestaw szuka go pod starym adresem i w całej sieci.')
n('k051', '  Not seen in 3–4 minutes? On the unit check that Wi-Fi is connected and «USB debugging» / ADB over network is on (many units turn it off after a reboot).',
  '  Не видно 3–4 минуты? На магнитоле проверь, что Wi-Fi подключён и «Отладка по USB» / ADB по сети включены (многие магнитолы выключают их после перезагрузки).',
  '  Не видно 3–4 хвилини? На магнітолі перевір, що Wi-Fi підключено і «Налагодження USB» / ADB по мережі увімкнені (багато магнітол вимикають їх після перезавантаження).',
  pt='  Não aparece em 3–4 minutos? No autorrádio verifique se o Wi-Fi está ligado e a «Depuração USB» / ADB pela rede ativos (muitos desligam-nos ao reiniciar).',
  es='  ¿No aparece en 3–4 minutos? En el autorradio compruebe que la Wi-Fi está conectada y «Depuración USB» / ADB por red activos (muchos los apagan al reiniciar).',
  fr='  Pas visible après 3–4 minutes ? Sur l’autoradio, vérifiez le Wi-Fi et que « Débogage USB » / ADB réseau sont activés (beaucoup les coupent au redémarrage).',
  it='  Non si vede dopo 3–4 minuti? Sullo stereo controlla che la Wi-Fi sia collegata e «Debug USB» / ADB in rete attivi (molti li spengono al riavvio).',
  de='  Nach 3–4 Minuten nicht sichtbar? Am Radio prüfen, ob WLAN verbunden und „USB-Debugging“ / Netzwerk-ADB an sind (viele schalten es nach dem Neustart aus).',
  lv='  Nav redzams 3–4 minūtes? Blokā pārbaudi, vai Wi-Fi pieslēgts un «USB atkļūdošana» / ADB tīklā ieslēgti (daudzi tos pēc restartēšanas izslēdz).',
  pl='  Nie widać po 3–4 minutach? Na radiu sprawdź, czy Wi-Fi jest połączone i „Debugowanie USB” / ADB przez sieć są włączone (wiele radii wyłącza je po restarcie).')
n('k052', '  Then the kit picks it up itself. If network ADB is lost after every reboot, that\'s the firmware — then check the result by eye.',
  '  Набор подхватит её сам. Если ADB по сети пропадает после каждой перезагрузки — это прошивка; тогда проверь результат глазами.',
  '  Набір підхопить її сам. Якщо ADB по мережі зникає після кожного перезавантаження — це прошивка; тоді перевір результат очима.',
  pt='  O kit apanha-o sozinho. Se o ADB pela rede se perde a cada reinício, é do firmware — então verifique o resultado à vista.', es='  El kit lo recoge solo. Si el ADB por red se pierde en cada reinicio, es el firmware — compruebe el resultado a simple vista.',
  fr='  Le kit le reprendra tout seul. Si l’ADB réseau disparaît à chaque redémarrage, c’est le firmware — vérifiez alors le résultat à l’œil.', it='  Il kit lo riprende da solo. Se l’ADB in rete sparisce a ogni riavvio è il firmware — allora controlla il risultato a vista.',
  de='  Das Kit findet es dann selbst. Verschwindet Netzwerk-ADB nach jedem Neustart, liegt es an der Firmware — dann das Ergebnis per Auge prüfen.', lv='  Komplekts to uztvers pats. Ja ADB tīklā pazūd pēc katras restartēšanas — tā ir programmaparatūra; tad pārbaudi rezultātu ar aci.',
  pl='  Zestaw sam go wykryje. Jeśli ADB przez sieć znika po każdym restarcie — to wina oprogramowania; wtedy sprawdź wynik na oko.')
n('k053', '  After boot the head unit reconnects to the Wi-Fi by itself (up to a couple of minutes); keep the ignition on.', '  После загрузки магнитола сама подключится к Wi-Fi (до пары минут); зажигание не выключать.',
  '  Після завантаження магнітола сама підключиться до Wi-Fi (до кількох хвилин); запалювання не вимикати.', pt='  Após arrancar, o autorrádio volta ao Wi-Fi sozinho (até uns minutos); não desligue a ignição.',
  es='  Tras arrancar, el autorradio vuelve solo a la Wi-Fi (hasta un par de minutos); no quite el contacto.', fr='  Après le démarrage, l’autoradio se reconnecte seul au Wi-Fi (quelques minutes) ; ne coupez pas le contact.',
  it='  Dopo l’avvio lo stereo si ricollega da solo alla Wi-Fi (un paio di minuti); non spegnere il quadro.', de='  Nach dem Start verbindet sich das Radio selbst mit dem WLAN (bis zu ein paar Minuten); Zündung anlassen.',
  lv='  Pēc ielādes bloks pats pieslēgsies Wi-Fi (līdz pāris minūtēm); aizdedzi neizslēgt.', pl='  Po starcie radio samo połączy się z Wi-Fi (do kilku minut); nie wyłączaj zapłonu.')
n('k054', 'the head unit didn\'t come back over the network in 7 minutes. Usually the firmware turned network ADB off after the reboot. Check by eye: home screen, radio, Bluetooth calls, reverse camera, steering wheel buttons, sound. If something is wrong — enable debugging again, start the kit and choose 3 (rollback).',
  'магнитола не вернулась по сети за 7 минут. Обычно это прошивка выключила ADB по сети после перезагрузки. Проверь глазами: рабочий стол, радио, звонки по Bluetooth, камеру заднего хода, кнопки руля, звук. Если что-то не так — включи отладку снова, запусти набор и выбери 3 (откат).',
  'магнітола не повернулася по мережі за 7 хвилин. Зазвичай це прошивка вимкнула ADB по мережі після перезавантаження. Перевір очима: робочий стіл, радіо, дзвінки по Bluetooth, камеру заднього ходу, кнопки керма, звук. Якщо щось не так — увімкни налагодження знову, запусти набір і обери 3 (відкат).',
  pt='o autorrádio não voltou pela rede em 7 minutos. Normalmente o firmware desligou o ADB pela rede ao reiniciar. Verifique à vista: ecrã inicial, rádio, chamadas Bluetooth, câmara de marcha-atrás, botões do volante, som. Se algo falhar — reative a depuração, inicie o kit e escolha 3 (reverter).',
  es='el autorradio no volvió por la red en 7 minutos. Normalmente el firmware apagó el ADB por red al reiniciar. Compruebe a simple vista: pantalla de inicio, radio, llamadas Bluetooth, cámara de marcha atrás, botones del volante, sonido. Si algo falla — reactive la depuración, inicie el kit y elija 3 (deshacer).',
  fr='l’autoradio n’est pas revenu sur le réseau en 7 minutes. En général le firmware a coupé l’ADB réseau au redémarrage. Vérifiez à l’œil : écran d’accueil, radio, appels Bluetooth, caméra de recul, commandes au volant, son. En cas de problème — réactivez le débogage, lancez le kit et choisissez 3 (annuler).',
  it='lo stereo non è tornato in rete in 7 minuti. Di solito il firmware ha spento l’ADB in rete al riavvio. Controlla a vista: schermata home, radio, chiamate Bluetooth, retrocamera, comandi al volante, audio. Se qualcosa non va — riattiva il debug, avvia il kit e scegli 3 (ripristino).',
  de='das Autoradio ist nach 7 Minuten nicht über das Netz zurück. Meist hat die Firmware Netzwerk-ADB beim Neustart ausgeschaltet. Per Auge prüfen: Startbildschirm, Radio, Bluetooth-Anrufe, Rückfahrkamera, Lenkradtasten, Ton. Stimmt etwas nicht — Debugging wieder an, Kit starten und 3 (Rückgängig) wählen.',
  lv='bloks 7 minūtēs neatgriezās tīklā. Parasti programmaparatūra pēc restartēšanas izslēdz ADB tīklā. Pārbaudi ar aci: sākuma ekrāns, radio, Bluetooth zvani, atpakaļgaitas kamera, stūres pogas, skaņa. Ja kaut kas nav kārtībā — ieslēdz atkļūdošanu, palaid komplektu un izvēlies 3 (atsaukt).',
  pl='radio nie wróciło przez sieć w 7 minut. Zwykle oprogramowanie wyłączyło ADB przez sieć po restarcie. Sprawdź na oko: ekran główny, radio, rozmowy Bluetooth, kamerę cofania, przyciski na kierownicy, dźwięk. Jeśli coś nie działa — włącz debugowanie, uruchom zestaw i wybierz 3 (cofnięcie).')
n('k055', 'Network ADB here isn\'t permanent (persist.adb.tcp.port is empty): after a reboot the kit may not get the connection back — then check the result on the screen by eye.',
  'ADB по сети здесь не постоянный (persist.adb.tcp.port пуст): после перезагрузки набор может не вернуть связь — тогда результат проверяется глазами на экране.',
  'ADB по мережі тут не постійний (persist.adb.tcp.port порожній): після перезавантаження набір може не повернути зв’язок — тоді результат перевіряється очима на екрані.',
  pt='O ADB pela rede aqui não é permanente (persist.adb.tcp.port vazio): após reiniciar o kit pode não recuperar a ligação — então verifique o resultado no ecrã.',
  es='El ADB por red aquí no es permanente (persist.adb.tcp.port vacío): tras reiniciar el kit puede no recuperar la conexión — entonces compruebe el resultado en la pantalla.',
  fr='L’ADB réseau n’est pas permanent ici (persist.adb.tcp.port vide) : après redémarrage le kit peut ne pas retrouver la connexion — vérifiez alors le résultat à l’écran.',
  it='Qui l’ADB in rete non è permanente (persist.adb.tcp.port vuoto): dopo il riavvio il kit potrebbe non ricollegarsi — allora controlla il risultato sullo schermo.',
  de='Netzwerk-ADB ist hier nicht dauerhaft (persist.adb.tcp.port leer): nach dem Neustart bekommt das Kit evtl. keine Verbindung — dann das Ergebnis am Bildschirm prüfen.',
  lv='ADB tīklā šeit nav pastāvīgs (persist.adb.tcp.port tukšs): pēc restartēšanas komplekts var neatgūt savienojumu — tad rezultātu pārbauda ekrānā.',
  pl='ADB przez sieć nie jest tu stałe (persist.adb.tcp.port pusty): po restarcie zestaw może nie odzyskać połączenia — wtedy sprawdź wynik na ekranie.')
n('k056', 'Before a reboot: car parked, ignition ON; don\'t touch the unit while it boots.', 'Перед перезагрузкой: машина стоит, зажигание включено; пока грузится — магнитолу не трогать.',
  'Перед перезавантаженням: машина стоїть, запалювання увімкнене; поки вантажиться — магнітолу не чіпати.', pt='Antes de reiniciar: carro parado, ignição ligada; não toque no autorrádio enquanto arranca.',
  es='Antes de reiniciar: coche parado, contacto puesto; no toque el autorradio mientras arranca.', fr='Avant le redémarrage : voiture à l’arrêt, contact mis ; ne touchez pas l’autoradio pendant le démarrage.',
  it='Prima del riavvio: auto ferma, quadro acceso; non toccare lo stereo mentre si avvia.', de='Vor dem Neustart: Auto steht, Zündung an; das Radio beim Hochfahren nicht anfassen.',
  lv='Pirms restartēšanas: auto stāv, aizdedze ieslēgta; kamēr ielādējas — bloku neaiztikt.', pl='Przed restartem: auto stoi, zapłon włączony; nie dotykaj radia podczas uruchamiania.')
n('k057', 'used', 'пользуются', 'користуються', pt='em uso', es='en uso', fr='utilisé', it='in uso', de='wird benutzt', lv='lieto', pl='używane')
n('k058', 'installed by the owner', 'установлено владельцем', 'встановлено власником', pt='instalado pelo dono', es='instalado por el dueño', fr='installé par le propriétaire', it='installato dal proprietario', de='vom Besitzer installiert', lv='instalējis īpašnieks', pl='zainstalowane przez właściciela')

# ---------------------------------------------------------------- платформа
n('k060', 'Head unit: {0}, {1}', 'Магнитола: {0}, {1}', 'Магнітола: {0}, {1}', pt='Autorrádio: {0}, {1}', es='Autorradio: {0}, {1}', fr='Autoradio : {0}, {1}', it='Stereo: {0}, {1}', de='Autoradio: {0}, {1}', lv='Multivides bloks: {0}, {1}', pl='Radioodtwarzacz: {0}, {1}')
n('k061', 'Not recognized as a known head unit platform (chip: {0}). The kit works in careful general mode: only checked junk, vendor packages are not touched. For phones there\'s phone-kit, for TVs — tv-kit.',
  'Платформа магнитолы не распознана (чип: {0}). Набор работает в осторожном общем режиме: только проверенный мусор, пакеты производителя не трогаются. Для телефонов есть phone-kit, для ТВ — tv-kit.',
  'Платформу магнітоли не розпізнано (чип: {0}). Набір працює в обережному загальному режимі: лише перевірене сміття, пакети виробника не чіпаються. Для телефонів є phone-kit, для ТБ — tv-kit.',
  pt='Plataforma de autorrádio não reconhecida (chip: {0}). O kit trabalha em modo geral cuidadoso: só lixo verificado, pacotes do fabricante não são tocados. Para telemóveis há o phone-kit, para TV o tv-kit.',
  es='Plataforma de autorradio no reconocida (chip: {0}). El kit trabaja en modo general prudente: solo basura comprobada, no se tocan los paquetes del fabricante. Para móviles está phone-kit, para TV tv-kit.',
  fr='Plateforme d’autoradio non reconnue (puce : {0}). Le kit travaille en mode général prudent : seulement le superflu vérifié, les paquets du fabricant ne sont pas touchés. Pour les téléphones il y a phone-kit, pour les TV tv-kit.',
  it='Piattaforma dello stereo non riconosciuta (chip: {0}). Il kit lavora in modalità generale prudente: solo spazzatura verificata, i pacchetti del produttore non si toccano. Per i telefoni c’è phone-kit, per le TV tv-kit.',
  de='Autoradio-Plattform nicht erkannt (Chip: {0}). Das Kit arbeitet im vorsichtigen allgemeinen Modus: nur geprüfter Ballast, Herstellerpakete bleiben unberührt. Für Handys gibt es phone-kit, für TVs tv-kit.',
  lv='Bloka platforma nav atpazīta (mikroshēma: {0}). Komplekts strādā piesardzīgā vispārējā režīmā: tikai pārbaudīti lieki pakotnes, ražotāja pakotnes netiek aiztiktas. Tālruņiem ir phone-kit, TV — tv-kit.',
  pl='Nie rozpoznano platformy radia (układ: {0}). Zestaw działa w ostrożnym trybie ogólnym: tylko sprawdzone śmieci, pakiety producenta nie są ruszane. Do telefonów jest phone-kit, do TV — tv-kit.')
n('k062', 'This is Android Automotive OS (the car\'s factory system). Changes here are made only by the manufacturer or dealer.',
  'Это Android Automotive OS (заводская система машины). Изменения здесь делает только производитель или дилер.',
  'Це Android Automotive OS (заводська система авто). Зміни тут робить лише виробник або дилер.',
  pt='Isto é Android Automotive OS (sistema de fábrica do carro). Alterações aqui só pelo fabricante ou concessionário.', es='Esto es Android Automotive OS (sistema de fábrica del coche). Los cambios aquí solo los hace el fabricante o el concesionario.',
  fr='C’est Android Automotive OS (système d’origine de la voiture). Seuls le constructeur ou le concessionnaire y font des changements.', it='Questo è Android Automotive OS (sistema di fabbrica dell’auto). Le modifiche qui le fa solo il produttore o il concessionario.',
  de='Das ist Android Automotive OS (Werkssystem des Autos). Änderungen macht hier nur der Hersteller oder Händler.', lv='Tā ir Android Automotive OS (auto rūpnīcas sistēma). Izmaiņas šeit veic tikai ražotājs vai dīleris.',
  pl='To Android Automotive OS (fabryczny system auta). Zmiany robi tu tylko producent lub dealer.')
n('k063', 'Optimization is off for Android Automotive — doing diagnostics only.', 'Для Android Automotive оптимизация выключена — делаю только диагностику.', 'Для Android Automotive оптимізацію вимкнено — роблю лише діагностику.',
  pt='Otimização desligada para Android Automotive — só diagnóstico.', es='Optimización desactivada para Android Automotive — solo diagnóstico.', fr='Optimisation désactivée pour Android Automotive — diagnostic seulement.',
  it='Ottimizzazione disattivata per Android Automotive — solo diagnosi.', de='Optimierung für Android Automotive aus — nur Diagnose.', lv='Android Automotive optimizācija izslēgta — tikai diagnostika.', pl='Optymalizacja dla Android Automotive wyłączona — tylko diagnostyka.')
n('k064', 'Continue in careful general mode? (yes / Enter — exit)', 'Продолжить в осторожном общем режиме? (да / Enter — выход)', 'Продовжити в обережному загальному режимі? (так / Enter — вихід)',
  pt='Continuar em modo geral cuidadoso? (sim / Enter — sair)', es='¿Continuar en modo general prudente? (sí / Enter — salir)', fr='Continuer en mode général prudent ? (oui / Entrée — quitter)',
  it='Continuare in modalità generale prudente? (sì / Invio — esci)', de='Im vorsichtigen allgemeinen Modus weitermachen? (ja / Enter — Ende)', lv='Turpināt piesardzīgā vispārējā režīmā? (jā / Enter — iziet)', pl='Kontynuować w ostrożnym trybie ogólnym? (tak / Enter — wyjście)')
n('k065', 'Continue in careful general mode?', 'Продолжить в осторожном общем режиме?', 'Продовжити в обережному загальному режимі?', pt='Continuar em modo geral cuidadoso?', es='¿Continuar en modo general prudente?', fr='Continuer en mode général prudent ?',
  it='Continuare in modalità generale prudente?', de='Im vorsichtigen allgemeinen Modus weitermachen?', lv='Turpināt piesardzīgā vispārējā režīmā?', pl='Kontynuować w ostrożnym trybie ogólnym?')
n('k066', 'checking which candidate packages are part of the firmware (up to a minute)', 'проверяю, какие пакеты-кандидаты — часть прошивки (до минуты)', 'перевіряю, які пакети-кандидати — частина прошивки (до хвилини)',
  pt='a verificar que pacotes candidatos fazem parte do firmware (até um minuto)', es='comprobando qué paquetes candidatos son parte del firmware (hasta un minuto)', fr='vérification des paquets candidats qui font partie du firmware (jusqu’à une minute)',
  it='controllo quali pacchetti candidati fanno parte del firmware (fino a un minuto)', de='prüfe, welche Kandidaten Teil der Firmware sind (bis zu einer Minute)', lv='pārbaudu, kuras kandidātpakotnes ir programmaparatūras daļa (līdz minūtei)', pl='sprawdzam, które pakiety-kandydaci są częścią oprogramowania (do minuty)')
n('k067', 'Teyes / UIS7870: the firmware has a different layout, so only packages from the checked list are pre-selected.', 'Teyes / UIS7870: у прошивки другая разметка, поэтому заранее отмечено только проверенное по списку.',
  'Teyes / UIS7870: у прошивки інша розмітка, тому заздалегідь позначено лише перевірене за списком.', pt='Teyes / UIS7870: o firmware tem outra estrutura, por isso só vêm marcados os pacotes da lista verificada.',
  es='Teyes / UIS7870: el firmware tiene otra estructura, así que solo vienen marcados los paquetes de la lista comprobada.', fr='Teyes / UIS7870 : le firmware est organisé autrement, seuls les paquets de la liste vérifiée sont précochés.',
  it='Teyes / UIS7870: il firmware ha una struttura diversa, quindi sono preselezionati solo i pacchetti della lista verificata.', de='Teyes / UIS7870: andere Firmware-Aufteilung, daher sind nur Pakete aus der geprüften Liste vorausgewählt.',
  lv='Teyes / UIS7870: programmaparatūrai ir cits izkārtojums, tāpēc iepriekš atzīmētas tikai pārbaudītās pakotnes.', pl='Teyes / UIS7870: oprogramowanie ma inny układ, więc z góry zaznaczone są tylko pakiety ze sprawdzonej listy.')

# ---------------------------------------------------------------- наблюдения
n('k070', 'The unit shows Android {0}, but it\'s really Android {1} (SDK {2}) — a common trick on Chinese head units. Apps (and the kit) go by the real version.',
  'Магнитола показывает Android {0}, а на деле это Android {1} (SDK {2}) — частая подмена у китайских магнитол. Приложения (и набор) смотрят на настоящую версию.',
  'Магнітола показує Android {0}, а насправді це Android {1} (SDK {2}) — часта підміна в китайських магнітол. Застосунки (і набір) дивляться на справжню версію.',
  pt='O autorrádio mostra Android {0}, mas na verdade é Android {1} (SDK {2}) — truque comum nos autorrádios chineses. As apps (e o kit) seguem a versão real.',
  es='El autorradio muestra Android {0}, pero en realidad es Android {1} (SDK {2}) — truco habitual en autorradios chinos. Las apps (y el kit) se guían por la versión real.',
  fr='L’autoradio affiche Android {0}, mais c’est en réalité Android {1} (SDK {2}) — astuce fréquente sur les autoradios chinois. Les applis (et le kit) suivent la vraie version.',
  it='Lo stereo mostra Android {0}, ma in realtà è Android {1} (SDK {2}) — trucco comune negli stereo cinesi. Le app (e il kit) seguono la versione reale.',
  de='Das Radio zeigt Android {0}, ist aber in Wahrheit Android {1} (SDK {2}) — ein häufiger Trick bei chinesischen Autoradios. Apps (und das Kit) richten sich nach der echten Version.',
  lv='Bloks rāda Android {0}, bet patiesībā tas ir Android {1} (SDK {2}) — bieža viltība ķīniešu blokos. Lietotnes (un komplekts) skatās uz īsto versiju.',
  pl='Radio pokazuje Android {0}, ale naprawdę to Android {1} (SDK {2}) — częsta sztuczka w chińskich radiach. Aplikacje (i zestaw) patrzą na prawdziwą wersję.')
n('k071', 'MediaTek DuraSpeed is on: it closes background apps (navigation, music). Turn it off in Settings -> DuraSpeed (or allow only the needed apps there).',
  'Включён MediaTek DuraSpeed: он закрывает фоновые приложения (навигацию, музыку). Выключить: Настройки -> DuraSpeed (или оставить разрешёнными нужные приложения).',
  'Увімкнено MediaTek DuraSpeed: він закриває фонові застосунки (навігацію, музику). Вимкнути: Налаштування -> DuraSpeed (або залишити дозволеними потрібні застосунки).',
  pt='O MediaTek DuraSpeed está ligado: fecha apps em segundo plano (navegação, música). Desligue em Definições -> DuraSpeed (ou permita lá só as apps necessárias).',
  es='MediaTek DuraSpeed está activado: cierra apps en segundo plano (navegación, música). Desactívelo en Ajustes -> DuraSpeed (o permita solo las apps necesarias).',
  fr='MediaTek DuraSpeed est activé : il ferme les applis en arrière-plan (navigation, musique). Désactivez-le dans Paramètres -> DuraSpeed (ou n’y autorisez que les applis utiles).',
  it='MediaTek DuraSpeed è attivo: chiude le app in background (navigazione, musica). Disattivalo in Impostazioni -> DuraSpeed (o consenti solo le app necessarie).',
  de='MediaTek DuraSpeed ist an: es schließt Hintergrund-Apps (Navigation, Musik). Ausschalten unter Einstellungen -> DuraSpeed (oder dort nur nötige Apps erlauben).',
  lv='Ieslēgts MediaTek DuraSpeed: tas aizver fona lietotnes (navigāciju, mūziku). Izslēgt: Iestatījumi -> DuraSpeed (vai atļaut tur tikai vajadzīgās lietotnes).',
  pl='Włączony MediaTek DuraSpeed: zamyka aplikacje w tle (nawigację, muzykę). Wyłącz w Ustawienia -> DuraSpeed (lub zezwól tam tylko potrzebnym aplikacjom).')
n('k072', 'ADB here runs with root rights. The kit doesn\'t use them — only ordinary reversible commands.', 'ADB здесь с правами root. Набор их не использует — только обычные обратимые команды.',
  'ADB тут із правами root. Набір їх не використовує — лише звичайні оборотні команди.', pt='Aqui o ADB tem direitos de root. O kit não os usa — só comandos normais e reversíveis.',
  es='Aquí ADB tiene permisos de root. El kit no los usa — solo comandos normales y reversibles.', fr='Ici ADB tourne avec les droits root. Le kit ne s’en sert pas — seulement des commandes ordinaires et réversibles.',
  it='Qui ADB ha i permessi di root. Il kit non li usa — solo comandi normali e reversibili.', de='ADB läuft hier mit Root-Rechten. Das Kit nutzt sie nicht — nur normale, umkehrbare Befehle.',
  lv='ADB šeit ir ar root tiesībām. Komplekts tās neizmanto — tikai parastas atgriezeniskas komandas.', pl='ADB działa tu z prawami roota. Zestaw z nich nie korzysta — tylko zwykłe, odwracalne polecenia.')
n('k073', 'ADB over the network is permanently on (port {0}): anyone on the same Wi-Fi can connect. If the owner doesn\'t need it, turn off debugging after the work.',
  'ADB по сети включён постоянно (порт {0}): подключиться может любой в той же сети Wi-Fi. Если владельцу не нужно — после работы выключить отладку.',
  'ADB по мережі увімкнено постійно (порт {0}): підключитися може будь-хто в тій самій мережі Wi-Fi. Якщо власнику не потрібно — після роботи вимкнути налагодження.',
  pt='O ADB pela rede está sempre ligado (porta {0}): qualquer pessoa no mesmo Wi-Fi pode ligar-se. Se o dono não precisar, desligue a depuração no fim.',
  es='ADB por red está siempre activo (puerto {0}): cualquiera en la misma Wi-Fi puede conectarse. Si el dueño no lo necesita, desactive la depuración al terminar.',
  fr='ADB réseau est activé en permanence (port {0}) : n’importe qui sur le même Wi-Fi peut se connecter. Si le propriétaire n’en a pas besoin, coupez le débogage après.',
  it='ADB in rete è sempre attivo (porta {0}): chiunque sulla stessa Wi-Fi può collegarsi. Se al proprietario non serve, spegni il debug alla fine.',
  de='Netzwerk-ADB ist dauerhaft an (Port {0}): jeder im selben WLAN kann sich verbinden. Braucht der Besitzer es nicht, Debugging danach ausschalten.',
  lv='ADB tīklā ieslēgts pastāvīgi (ports {0}): pieslēgties var jebkurš tajā pašā Wi-Fi. Ja īpašniekam nevajag — pēc darba izslēgt atkļūdošanu.',
  pl='ADB przez sieć jest stale włączone (port {0}): każdy w tej samej sieci Wi-Fi może się połączyć. Jeśli właściciel tego nie potrzebuje, po pracy wyłącz debugowanie.')
n('k074', 'Google services take {0} MB of RAM on a unit with 2.5 GB or less. If Google Play isn\'t needed, disabling Google apps (YouTube, Chrome, the Google app) frees a lot.',
  'Сервисы Google занимают {0} МБ ОЗУ на магнитоле с 2,5 ГБ и меньше. Если Google Play не нужен, отключение приложений Google (YouTube, Chrome, приложение Google) освободит много.',
  'Сервіси Google займають {0} МБ ОЗП на магнітолі з 2,5 ГБ і менше. Якщо Google Play не потрібен, вимкнення застосунків Google (YouTube, Chrome, застосунок Google) звільнить багато.',
  pt='Os serviços Google ocupam {0} MB de RAM num autorrádio com 2,5 GB ou menos. Se o Google Play não for preciso, desativar apps Google (YouTube, Chrome, app Google) liberta muito.',
  es='Los servicios de Google ocupan {0} MB de RAM en un autorradio con 2,5 GB o menos. Si Google Play no hace falta, desactivar apps de Google (YouTube, Chrome, app de Google) libera mucho.',
  fr='Les services Google prennent {0} Mo de RAM sur un autoradio de 2,5 Go ou moins. Si Google Play n’est pas utile, désactiver les applis Google (YouTube, Chrome, appli Google) libère beaucoup.',
  it='I servizi Google occupano {0} MB di RAM su uno stereo con 2,5 GB o meno. Se Google Play non serve, disattivare le app Google (YouTube, Chrome, app Google) libera molto.',
  de='Google-Dienste belegen {0} MB RAM auf einem Radio mit 2,5 GB oder weniger. Wird Google Play nicht gebraucht, bringt das Deaktivieren von Google-Apps (YouTube, Chrome, Google-App) viel.',
  lv='Google pakalpojumi aizņem {0} MB RAM blokā ar 2,5 GB vai mazāk. Ja Google Play nav vajadzīgs, Google lietotņu (YouTube, Chrome, Google) atspējošana atbrīvos daudz.',
  pl='Usługi Google zajmują {0} MB RAM w radiu z 2,5 GB lub mniej. Jeśli Google Play nie jest potrzebny, wyłączenie aplikacji Google (YouTube, Chrome, aplikacja Google) zwolni dużo.')
n('k080', 'If navigation or music closes after the ignition goes off and on, the firmware\'s «sleep» app killer is to blame (not Android).',
  'Если навигация или музыка закрываются после выключения и включения зажигания — виноват «убийца приложений» прошивки при сне (не Android).',
  'Якщо навігація чи музика закриваються після вимкнення й увімкнення запалювання — винен «вбивця застосунків» прошивки під час сну (не Android).',
  pt='Se a navegação ou a música fecham depois de desligar e ligar a ignição, a culpa é do «matador de apps» do firmware no sono (não do Android).',
  es='Si la navegación o la música se cierran tras quitar y poner el contacto, la culpa es del «asesino de apps» del firmware al dormir (no de Android).',
  fr='Si la navigation ou la musique se ferment après avoir coupé puis remis le contact, c’est le « tueur d’applis » du firmware en veille (pas Android).',
  it='Se navigazione o musica si chiudono dopo aver spento e riacceso il quadro, la colpa è del «killer di app» del firmware in sospensione (non di Android).',
  de='Schließen sich Navigation oder Musik nach Zündung aus/an, ist der „App-Killer“ der Firmware beim Schlafen schuld (nicht Android).',
  lv='Ja navigācija vai mūzika aizveras pēc aizdedzes izslēgšanas un ieslēgšanas — vainīgs programmaparatūras «lietotņu slepkava» miega laikā (nevis Android).',
  pl='Jeśli nawigacja lub muzyka zamykają się po wyłączeniu i włączeniu zapłonu, winny jest „zabójca aplikacji” oprogramowania przy uśpieniu (nie Android).')
n('k081', 'FYT: some firmware has an app whitelist for sleep in Factory settings (look for «whitelist» / «background apps»); newer firmware (2024+) dropped it — then use a third-party tool (e.g. FYT Factory app) or set navigation to start after sleep.',
  'FYT: в части прошивок в Заводских настройках есть белый список приложений для сна (ищите «белый список» / «фоновые приложения»); в новых (2024+) его убрали — тогда сторонняя утилита (например, FYT Factory app) или автозапуск навигации после сна.',
  'FYT: у частині прошивок у Заводських налаштуваннях є білий список застосунків для сну (шукайте «білий список» / «фонові застосунки»); у нових (2024+) його прибрали — тоді стороння утиліта (наприклад, FYT Factory app) або автозапуск навігації після сну.',
  pt='FYT: alguns firmwares têm nas Definições de fábrica uma lista branca de apps para o sono (procure «lista branca» / «apps em segundo plano»); os novos (2024+) retiraram-na — use então uma ferramenta externa (p. ex. FYT Factory app) ou o arranque da navegação após o sono.',
  es='FYT: algunos firmwares tienen en Ajustes de fábrica una lista blanca de apps para el reposo (busque «lista blanca» / «apps en segundo plano»); los nuevos (2024+) la quitaron — use entonces una herramienta externa (p. ej. FYT Factory app) o el arranque de la navegación tras el reposo.',
  fr='FYT : certains firmwares ont dans les Réglages usine une liste blanche d’applis pour la veille (cherchez « liste blanche » / « applis en arrière-plan ») ; les récents (2024+) l’ont supprimée — utilisez alors un outil tiers (p. ex. FYT Factory app) ou le lancement de la navigation après la veille.',
  it='FYT: alcuni firmware hanno nelle Impostazioni di fabbrica una whitelist di app per la sospensione (cerca «whitelist» / «app in background»); i nuovi (2024+) l’hanno tolta — allora usa uno strumento esterno (ad es. FYT Factory app) o l’avvio della navigazione dopo la sospensione.',
  de='FYT: manche Firmware hat in den Werkseinstellungen eine App-Whitelist für den Schlafmodus (nach „Whitelist“ / „Hintergrund-Apps“ suchen); neuere (2024+) nicht mehr — dann ein Fremdtool (z. B. FYT Factory app) oder Navi-Autostart nach dem Schlaf.',
  lv='FYT: daļai programmaparatūru Rūpnīcas iestatījumos ir lietotņu baltais saraksts miegam (meklē «baltais saraksts» / «fona lietotnes»); jaunākajās (2024+) tā vairs nav — tad trešās puses rīks (piem., FYT Factory app) vai navigācijas automātiska palaišana pēc miega.',
  pl='FYT: część oprogramowań ma w Ustawieniach fabrycznych białą listę aplikacji na uśpienie (szukaj „biała lista” / „aplikacje w tle”); nowsze (2024+) jej nie mają — wtedy narzędzie zewnętrzne (np. FYT Factory app) lub autostart nawigacji po uśpieniu.')
n('k082', 'QF: after sleep the firmware keeps only the 2 latest apps; its whitelist is a system file — without root only the vendor or a firmware update can change it.',
  'QF: после сна прошивка оставляет только 2 последних приложения; её белый список — системный файл, без root его меняет только продавец или обновление прошивки.',
  'QF: після сну прошивка залишає лише 2 останні застосунки; її білий список — системний файл, без root його змінює лише продавець або оновлення прошивки.',
  pt='QF: após o sono o firmware mantém só as 2 últimas apps; a lista branca é um ficheiro de sistema — sem root só o vendedor ou uma atualização a mudam.',
  es='QF: tras el reposo el firmware solo mantiene las 2 últimas apps; su lista blanca es un archivo del sistema — sin root solo el vendedor o una actualización la cambian.',
  fr='QF : après la veille le firmware ne garde que les 2 dernières applis ; sa liste blanche est un fichier système — sans root seuls le vendeur ou une mise à jour la changent.',
  it='QF: dopo la sospensione il firmware tiene solo le ultime 2 app; la whitelist è un file di sistema — senza root la cambiano solo il venditore o un aggiornamento.',
  de='QF: nach dem Schlaf behält die Firmware nur die 2 letzten Apps; die Whitelist ist eine Systemdatei — ohne Root ändern sie nur Händler oder ein Firmware-Update.',
  lv='QF: pēc miega programmaparatūra patur tikai 2 pēdējās lietotnes; baltais saraksts ir sistēmas fails — bez root to maina tikai pārdevējs vai atjauninājums.',
  pl='QF: po uśpieniu oprogramowanie zostawia tylko 2 ostatnie aplikacje; biała lista to plik systemowy — bez roota zmieni ją tylko sprzedawca lub aktualizacja.')
n('k083', 'Reglink / MTK: about 20 s after ACC off it closes apps not on its list; turning off «Quick boot» in Factory settings helps (the unit then fully shuts down and boots in ~20–30 s).',
  'Reglink / MTK: примерно через 20 с после выключения ACC закрывает приложения не из своего списка; помогает выключить «Быстрый старт» (Quick boot) в Заводских настройках (магнитола будет полностью выключаться и грузиться ~20–30 с).',
  'Reglink / MTK: приблизно через 20 с після вимкнення ACC закриває застосунки не зі свого списку; допомагає вимкнути «Швидкий старт» (Quick boot) у Заводських налаштуваннях (магнітола повністю вимикатиметься й вантажитиметься ~20–30 с).',
  pt='Reglink / MTK: uns 20 s após desligar o ACC fecha as apps fora da sua lista; ajuda desligar «Arranque rápido» (Quick boot) nas Definições de fábrica (o autorrádio passa a desligar-se de vez e arranca em ~20–30 s).',
  es='Reglink / MTK: unos 20 s tras quitar el ACC cierra las apps que no están en su lista; ayuda desactivar «Arranque rápido» (Quick boot) en Ajustes de fábrica (el autorradio se apagará del todo y arrancará en ~20–30 s).',
  fr='Reglink / MTK : environ 20 s après coupure de l’ACC il ferme les applis hors de sa liste ; désactiver « Démarrage rapide » (Quick boot) dans les Réglages usine aide (l’autoradio s’éteint alors complètement et démarre en ~20–30 s).',
  it='Reglink / MTK: circa 20 s dopo lo spegnimento dell’ACC chiude le app non in lista; aiuta disattivare «Avvio rapido» (Quick boot) nelle Impostazioni di fabbrica (lo stereo si spegnerà del tutto e si avvierà in ~20–30 s).',
  de='Reglink / MTK: etwa 20 s nach ACC aus schließt es Apps, die nicht auf seiner Liste stehen; „Schnellstart“ (Quick boot) in den Werkseinstellungen ausschalten hilft (das Radio fährt dann ganz herunter und startet in ~20–30 s).',
  lv='Reglink / MTK: ~20 s pēc ACC izslēgšanas aizver lietotnes, kas nav tā sarakstā; palīdz izslēgt «Ātrā palaišana» (Quick boot) Rūpnīcas iestatījumos (bloks pilnībā izslēgsies un ielādēsies ~20–30 s).',
  pl='Reglink / MTK: ok. 20 s po wyłączeniu ACC zamyka aplikacje spoza swojej listy; pomaga wyłączenie „Szybkiego startu” (Quick boot) w Ustawieniach fabrycznych (radio będzie się całkiem wyłączać i startować ~20–30 s).')
n('k084', 'MTCD / MTCE: the list is built into the firmware; custom firmware (Malaysk and others) has a «Whitelist of programs to run after sleep».',
  'MTCD / MTCE: список зашит в прошивку; в пользовательских прошивках (Malaysk и др.) есть «Белый список программ для запуска после сна».',
  'MTCD / MTCE: список зашитий у прошивку; у користувацьких прошивках (Malaysk та ін.) є «Білий список програм для запуску після сну».',
  pt='MTCD / MTCE: a lista está no firmware; firmwares alternativos (Malaysk e outros) têm «Lista branca de programas após o sono».', es='MTCD / MTCE: la lista está en el firmware; los firmwares alternativos (Malaysk y otros) tienen «Lista blanca de programas tras el reposo».',
  fr='MTCD / MTCE : la liste est intégrée au firmware ; les firmwares alternatifs (Malaysk et autres) ont une « Liste blanche des programmes après la veille ».', it='MTCD / MTCE: la lista è nel firmware; i firmware alternativi (Malaysk e altri) hanno una «Whitelist dei programmi dopo la sospensione».',
  de='MTCD / MTCE: die Liste steckt in der Firmware; alternative Firmware (Malaysk u. a.) hat eine „Whitelist der Programme nach dem Schlaf“.', lv='MTCD / MTCE: saraksts ir programmaparatūrā; alternatīvajās (Malaysk u. c.) ir «Programmu baltais saraksts pēc miega».',
  pl='MTCD / MTCE: lista jest wbudowana w oprogramowanie; alternatywne oprogramowania (Malaysk i inne) mają „Białą listę programów po uśpieniu”.')
n('k085', 'Look in Car settings / Factory settings for «sleep», «fast boot», «whitelist»; the kit doesn\'t change these.', 'Ищите в Настройках автомобиля / Заводских настройках «сон», «быстрый старт», «белый список»; набор это не меняет.',
  'Шукайте в Налаштуваннях авто / Заводських налаштуваннях «сон», «швидкий старт», «білий список»; набір цього не змінює.', pt='Procure nas Definições do carro / de fábrica «sono», «arranque rápido», «lista branca»; o kit não muda isto.',
  es='Busque en Ajustes del coche / de fábrica «reposo», «arranque rápido», «lista blanca»; el kit no cambia esto.', fr='Cherchez dans les Réglages voiture / usine « veille », « démarrage rapide », « liste blanche » ; le kit n’y touche pas.',
  it='Cerca nelle Impostazioni auto / di fabbrica «sospensione», «avvio rapido», «whitelist»; il kit non le cambia.', de='In Fahrzeug- / Werkseinstellungen nach „Schlaf“, „Schnellstart“, „Whitelist“ suchen; das Kit ändert das nicht.',
  lv='Meklē Auto / Rūpnīcas iestatījumos «miegs», «ātrā palaišana», «baltais saraksts»; komplekts to nemaina.', pl='Szukaj w Ustawieniach auta / fabrycznych „uśpienie”, „szybki start”, „biała lista”; zestaw tego nie zmienia.')

# ---------------------------------------------------------------- отчёт
n('k090', '  Head unit platform: {0}; chip: {1}', '  Платформа магнитолы: {0}; чип: {1}', '  Платформа магнітоли: {0}; чип: {1}', pt='  Plataforma do autorrádio: {0}; chip: {1}', es='  Plataforma del autorradio: {0}; chip: {1}',
  fr='  Plateforme de l’autoradio : {0} ; puce : {1}', it='  Piattaforma dello stereo: {0}; chip: {1}', de='  Autoradio-Plattform: {0}; Chip: {1}', lv='  Bloka platforma: {0}; mikroshēma: {1}', pl='  Platforma radia: {0}; układ: {1}')
n('k091', 'not recognized', 'не распознана', 'не розпізнано', pt='não reconhecida', es='no reconocida', fr='non reconnue', it='non riconosciuta', de='nicht erkannt', lv='nav atpazīta', pl='nierozpoznana')
n('k092', '  Head unit services (checked after every batch): {0}', '  Службы магнитолы (проверяются после каждой партии): {0}', '  Служби магнітоли (перевіряються після кожної партії): {0}',
  pt='  Serviços do autorrádio (verificados após cada lote): {0}', es='  Servicios del autorradio (comprobados tras cada lote): {0}', fr='  Services de l’autoradio (vérifiés après chaque lot) : {0}',
  it='  Servizi dello stereo (controllati dopo ogni lotto): {0}', de='  Dienste des Autoradios (nach jedem Paket geprüft): {0}', lv='  Bloka servisi (pārbauda pēc katras partijas): {0}', pl='  Usługi radia (sprawdzane po każdej partii): {0}')
n('k093', '  ADB rights: {0}; permanent network ADB port: {1}', '  Права ADB: {0}; постоянный порт ADB по сети: {1}', '  Права ADB: {0}; постійний порт ADB по мережі: {1}', pt='  Direitos ADB: {0}; porta ADB de rede permanente: {1}',
  es='  Permisos ADB: {0}; puerto ADB de red permanente: {1}', fr='  Droits ADB : {0} ; port ADB réseau permanent : {1}', it='  Permessi ADB: {0}; porta ADB di rete permanente: {1}', de='  ADB-Rechte: {0}; dauerhafter Netzwerk-ADB-Port: {1}',
  lv='  ADB tiesības: {0}; pastāvīgais tīkla ADB ports: {1}', pl='  Prawa ADB: {0}; stały port ADB przez sieć: {1}')
n('k094', '  Vendor packages under protection ({0}): ', '  Пакеты производителя под защитой ({0}): ', '  Пакети виробника під захистом ({0}): ', pt='  Pacotes do fabricante protegidos ({0}): ', es='  Paquetes del fabricante protegidos ({0}): ',
  fr='  Paquets du fabricant protégés ({0}) : ', it='  Pacchetti del produttore protetti ({0}): ', de='  Geschützte Herstellerpakete ({0}): ', lv='  Aizsargātās ražotāja pakotnes ({0}): ', pl='  Chronione pakiety producenta ({0}): ')
n('k095', '10a. DON\'T PUT TO SLEEP (navigation, music, CarPlay):', '10а. НЕ УСЫПЛЯТЬ (навигация, музыка, CarPlay):', '10а. НЕ ПРИСИПЛЯТИ (навігація, музика, CarPlay):', pt='10a. NÃO ADORMECER (navegação, música, CarPlay):',
  es='10a. NO DORMIR (navegación, música, CarPlay):', fr='10a. NE PAS ENDORMIR (navigation, musique, CarPlay) :', it='10a. NON SOSPENDERE (navigazione, musica, CarPlay):', de='10a. NICHT SCHLAFEN LEGEN (Navigation, Musik, CarPlay):',
  lv='10a. NEIEMIDZINĀT (navigācija, mūzika, CarPlay):', pl='10a. NIE USYPIAĆ (nawigacja, muzyka, CarPlay):')
n('k096', 'Head unit', 'Магнитола', 'Магнітола', pt='Autorrádio', es='Autorradio', fr='Autoradio', it='Stereo', de='Autoradio', lv='Multivides bloks', pl='Radioodtwarzacz')
n('k097', 'RAM: {0} of {1} MB available; storage {2}% full; platform: {3}, {4}', 'ОЗУ: доступно {0} из {1} МБ; память занята на {2}%; платформа: {3}, {4}', 'ОЗП: доступно {0} з {1} МБ; пам’ять зайнята на {2}%; платформа: {3}, {4}',
  pt='RAM: {0} de {1} MB disponíveis; armazenamento {2}% cheio; plataforma: {3}, {4}', es='RAM: {0} de {1} MB disponibles; almacenamiento {2}% lleno; plataforma: {3}, {4}', fr='RAM : {0} sur {1} Mo disponibles ; stockage rempli à {2} % ; plateforme : {3}, {4}',
  it='RAM: {0} di {1} MB disponibili; memoria piena al {2}%; piattaforma: {3}, {4}', de='RAM: {0} von {1} MB frei; Speicher zu {2} % voll; Plattform: {3}, {4}', lv='RAM: pieejams {0} no {1} MB; atmiņa aizņemta {2}%; platforma: {3}, {4}', pl='RAM: dostępne {0} z {1} MB; pamięć zajęta w {2}%; platforma: {3}, {4}')

# ---------------------------------------------------------------- страница
n('ui_scan_t', 'Find on Wi-Fi', 'Найти в сети Wi-Fi', 'Знайти в мережі Wi-Fi', pt='Procurar no Wi-Fi', es='Buscar en la Wi-Fi', fr='Chercher sur le Wi-Fi', it='Cerca sulla Wi-Fi', de='Im WLAN suchen', lv='Atrast Wi-Fi tīklā', pl='Znajdź w sieci Wi-Fi')
n('ui_scan_d', 'Laptop and head unit on the same Wi-Fi (the phone hotspot), «USB debugging» on. The kit finds the unit by itself.', 'Ноутбук и магнитола в одной сети Wi-Fi (точка доступа телефона), «Отладка по USB» включена. Набор сам найдёт магнитолу.',
  'Ноутбук і магнітола в одній мережі Wi-Fi (точка доступу телефона), «Налагодження USB» увімкнене. Набір сам знайде магнітолу.', pt='Portátil e autorrádio no mesmo Wi-Fi (hotspot do telemóvel), «Depuração USB» ativa. O kit encontra o autorrádio sozinho.',
  es='Portátil y autorradio en la misma Wi-Fi (punto de acceso del móvil), «Depuración USB» activa. El kit encuentra el autorradio solo.', fr='PC et autoradio sur le même Wi-Fi (partage du téléphone), « Débogage USB » activé. Le kit trouve l’autoradio tout seul.',
  it='Portatile e stereo sulla stessa Wi-Fi (hotspot del telefono), «Debug USB» attivo. Il kit trova lo stereo da solo.', de='Laptop und Autoradio im selben WLAN (Handy-Hotspot), „USB-Debugging“ an. Das Kit findet das Radio selbst.',
  lv='Klēpjdators un bloks vienā Wi-Fi (tālruņa tīklājs), «USB atkļūdošana» ieslēgta. Komplekts pats atradīs bloku.', pl='Laptop i radio w tej samej sieci Wi-Fi (hotspot telefonu), „Debugowanie USB” włączone. Zestaw sam znajdzie radio.')
n('ui_scan_btn', 'Find head unit', 'Найти магнитолу', 'Знайти магнітолу', pt='Procurar autorrádio', es='Buscar autorradio', fr='Chercher l’autoradio', it='Cerca lo stereo', de='Autoradio suchen', lv='Atrast bloku', pl='Znajdź radio')
n('ui_ip_t', 'Enter the IP', 'Ввести IP', 'Ввести IP', pt='Introduzir IP', es='Introducir IP', fr='Saisir l’IP', it='Inserisci IP', de='IP eingeben', lv='Ievadīt IP', pl='Wpisz IP')
n('ui_ip_d', 'The unit\'s address: Settings -> Wi-Fi -> network details. Port 5555 is added automatically.', 'Адрес магнитолы: Настройки -> Wi-Fi -> сведения о сети. Порт 5555 подставится сам.',
  'Адреса магнітоли: Налаштування -> Wi-Fi -> відомості про мережу. Порт 5555 підставиться сам.', pt='Endereço do autorrádio: Definições -> Wi-Fi -> detalhes. A porta 5555 é adicionada sozinha.',
  es='Dirección del autorradio: Ajustes -> Wi-Fi -> detalles. El puerto 5555 se añade solo.', fr='Adresse de l’autoradio : Paramètres -> Wi-Fi -> détails. Le port 5555 est ajouté tout seul.',
  it='Indirizzo dello stereo: Impostazioni -> Wi-Fi -> dettagli. La porta 5555 si aggiunge da sola.', de='Adresse des Radios: Einstellungen -> WLAN -> Details. Port 5555 wird automatisch ergänzt.',
  lv='Bloka adrese: Iestatījumi -> Wi-Fi -> tīkla informācija. Ports 5555 tiek pievienots pats.', pl='Adres radia: Ustawienia -> Wi-Fi -> szczegóły sieci. Port 5555 dopisze się sam.')
n('ui_ip_btn', 'Enter address', 'Ввести адрес', 'Ввести адресу', pt='Introduzir endereço', es='Introducir dirección', fr='Saisir l’adresse', it='Inserisci indirizzo', de='Adresse eingeben', lv='Ievadīt adresi', pl='Wpisz adres')
n('ui_plat', 'Platform', 'Платформа', 'Платформа', pt='Plataforma', es='Plataforma', fr='Plateforme', it='Piattaforma', de='Plattform', lv='Platforma', pl='Platforma')
n('ui_plat_d', 'head unit services are protected', 'службы магнитолы под защитой', 'служби магнітоли під захистом', pt='serviços do autorrádio protegidos', es='servicios del autorradio protegidos', fr='services de l’autoradio protégés',
  it='servizi dello stereo protetti', de='Radio-Dienste geschützt', lv='bloka servisi aizsargāti', pl='usługi radia chronione')

# ---------------------------------------------------------------- 0.2: экран, снимок, проверки, свои APK
n('k100', '  Tip: the head unit screen can be shown on this laptop and controlled with the mouse — button «Unit screen» on the page (or start.bat -Mirror).',
  '  Подсказка: экран магнитолы можно показать на этом ноутбуке и управлять мышью — кнопка «Экран магнитолы» на странице (или start.bat -Mirror).',
  '  Підказка: екран магнітоли можна показати на цьому ноутбуці й керувати мишею — кнопка «Екран магнітоли» на сторінці (або start.bat -Mirror).',
  pt='  Dica: o ecrã do autorrádio pode ser mostrado neste portátil e controlado com o rato — botão «Ecrã do autorrádio» na página (ou start.bat -Mirror).',
  es='  Consejo: la pantalla del autorradio se puede ver en este portátil y manejar con el ratón — botón «Pantalla del autorradio» en la página (o start.bat -Mirror).',
  fr='  Astuce : l’écran de l’autoradio peut s’afficher sur ce PC et se piloter à la souris — bouton « Écran de l’autoradio » sur la page (ou start.bat -Mirror).',
  it='  Suggerimento: lo schermo dello stereo si può vedere su questo portatile e usare con il mouse — pulsante «Schermo dello stereo» nella pagina (o start.bat -Mirror).',
  de='  Tipp: Der Bildschirm des Autoradios lässt sich auf diesem Laptop zeigen und mit der Maus bedienen — Taste „Radio-Bildschirm“ auf der Seite (oder start.bat -Mirror).',
  lv='  Padoms: bloka ekrānu var parādīt šajā klēpjdatorā un vadīt ar peli — poga «Bloka ekrāns» lapā (vai start.bat -Mirror).',
  pl='  Wskazówka: ekran radia można pokazać na tym laptopie i sterować myszą — przycisk „Ekran radia” na stronie (lub start.bat -Mirror).')
n('k101', 'Downloading scrcpy for the screen ({0}, ~12 MB)...', 'Скачиваю scrcpy для экрана ({0}, ~12 МБ)...', 'Завантажую scrcpy для екрана ({0}, ~12 МБ)...', pt='A transferir o scrcpy para o ecrã ({0}, ~12 MB)...',
  es='Descargando scrcpy para la pantalla ({0}, ~12 MB)...', fr='Téléchargement de scrcpy pour l’écran ({0}, ~12 Mo)...', it='Scarico scrcpy per lo schermo ({0}, ~12 MB)...', de='Lade scrcpy für den Bildschirm ({0}, ~12 MB)...',
  lv='Lejupielādēju scrcpy ekrānam ({0}, ~12 MB)...', pl='Pobieram scrcpy do ekranu ({0}, ~12 MB)...')
n('k102', 'scrcpy: ', 'scrcpy: ', 'scrcpy: ')
n('k103', 'The head unit isn\'t connected yet — the screen will be available after connecting.', 'Магнитола ещё не подключена — экран будет доступен после подключения.', 'Магнітолу ще не підключено — екран буде доступний після підключення.',
  pt='O autorrádio ainda não está ligado — o ecrã fica disponível depois de ligar.', es='El autorradio aún no está conectado — la pantalla estará disponible tras conectar.', fr='L’autoradio n’est pas encore connecté — l’écran sera disponible après la connexion.',
  it='Lo stereo non è ancora collegato — lo schermo sarà disponibile dopo il collegamento.', de='Das Autoradio ist noch nicht verbunden — der Bildschirm geht nach dem Verbinden.', lv='Bloks vēl nav pieslēgts — ekrāns būs pieejams pēc pieslēgšanas.', pl='Radio nie jest jeszcze podłączone — ekran będzie dostępny po podłączeniu.')
n('k104', 'Couldn\'t open the head unit screen (scrcpy). Download it by hand: github.com/Genymobile/scrcpy/releases — unzip into tools\\scrcpy of the kit.',
  'Не получилось открыть экран магнитолы (scrcpy). Скачай вручную: github.com/Genymobile/scrcpy/releases — распакуй в tools\\scrcpy набора.',
  'Не вдалося відкрити екран магнітоли (scrcpy). Завантаж вручну: github.com/Genymobile/scrcpy/releases — розпакуй у tools\\scrcpy набору.',
  pt='Não foi possível abrir o ecrã (scrcpy). Transfira à mão: github.com/Genymobile/scrcpy/releases — extraia para tools\\scrcpy do kit.', es='No se pudo abrir la pantalla (scrcpy). Descárguelo a mano: github.com/Genymobile/scrcpy/releases — descomprima en tools\\scrcpy del kit.',
  fr='Impossible d’ouvrir l’écran (scrcpy). Téléchargez-le : github.com/Genymobile/scrcpy/releases — décompressez dans tools\\scrcpy du kit.', it='Impossibile aprire lo schermo (scrcpy). Scaricalo a mano: github.com/Genymobile/scrcpy/releases — estrai in tools\\scrcpy del kit.',
  de='Bildschirm (scrcpy) ließ sich nicht öffnen. Von Hand laden: github.com/Genymobile/scrcpy/releases — nach tools\\scrcpy des Kits entpacken.', lv='Neizdevās atvērt ekrānu (scrcpy). Lejupielādē ar roku: github.com/Genymobile/scrcpy/releases — izpako komplekta mapē tools\\scrcpy.',
  pl='Nie udało się otworzyć ekranu (scrcpy). Pobierz ręcznie: github.com/Genymobile/scrcpy/releases — rozpakuj do tools\\scrcpy zestawu.')
n('k105', 'The head unit screen is open in a separate window (mouse = finger, right click = Back). The car\'s sound stays in its speakers.',
  'Экран магнитолы открыт в отдельном окне (мышь = палец, правая кнопка = «Назад»). Звук остаётся в колонках машины.',
  'Екран магнітоли відкрито в окремому вікні (миша = палець, права кнопка = «Назад»). Звук лишається в колонках авто.',
  pt='O ecrã do autorrádio abriu numa janela à parte (rato = dedo, botão direito = Voltar). O som fica nas colunas do carro.', es='La pantalla del autorradio está abierta en otra ventana (ratón = dedo, clic derecho = Atrás). El sonido sigue en los altavoces del coche.',
  fr='L’écran de l’autoradio est ouvert dans une fenêtre séparée (souris = doigt, clic droit = Retour). Le son reste dans les haut-parleurs.', it='Lo schermo dello stereo è aperto in una finestra a parte (mouse = dito, tasto destro = Indietro). L’audio resta negli altoparlanti dell’auto.',
  de='Der Radio-Bildschirm ist in einem eigenen Fenster offen (Maus = Finger, Rechtsklick = Zurück). Der Ton bleibt in den Autolautsprechern.', lv='Bloka ekrāns atvērts atsevišķā logā (pele = pirksts, labā poga = Atpakaļ). Skaņa paliek auto skaļruņos.',
  pl='Ekran radia otwarto w osobnym oknie (mysz = palec, prawy przycisk = Wstecz). Dźwięk zostaje w głośnikach auta.')
n('k110', 'head unit settings snapshot (read-only: car model, CAN, buttons, screen)', 'снимок настроек магнитолы (только чтение: модель машины, CAN, кнопки, экран)', 'знімок налаштувань магнітоли (лише читання: модель авто, CAN, кнопки, екран)',
  pt='instantâneo das definições (só leitura: modelo do carro, CAN, botões, ecrã)', es='copia de los ajustes (solo lectura: modelo de coche, CAN, botones, pantalla)', fr='instantané des réglages (lecture seule : modèle, CAN, boutons, écran)',
  it='istantanea delle impostazioni (sola lettura: modello auto, CAN, tasti, schermo)', de='Schnappschuss der Einstellungen (nur lesen: Fahrzeug, CAN, Tasten, Bildschirm)', lv='iestatījumu momentuzņēmums (tikai lasīšana: auto modelis, CAN, pogas, ekrāns)',
  pl='kopia ustawień (tylko odczyt: model auta, CAN, przyciski, ekran)')
n('k111', 'The head unit clock is off by {0} min ({1}). Wrong time breaks HTTPS: Google Play, maps and music won\'t load.', 'Часы магнитолы сбиты на {0} мин ({1}). Из-за неверного времени не работает HTTPS: Google Play, карты и музыка не грузятся.',
  'Годинник магнітоли збитий на {0} хв ({1}). Через неправильний час не працює HTTPS: Google Play, карти й музика не вантажаться.', pt='O relógio do autorrádio está desviado {0} min ({1}). A hora errada estraga o HTTPS: Google Play, mapas e música não carregam.',
  es='El reloj del autorradio va desviado {0} min ({1}). La hora mal puesta rompe el HTTPS: Google Play, mapas y música no cargan.', fr='L’horloge de l’autoradio est décalée de {0} min ({1}). Une heure fausse casse le HTTPS : Google Play, cartes et musique ne chargent pas.',
  it='L’orologio dello stereo è sfasato di {0} min ({1}). L’ora sbagliata rompe l’HTTPS: Google Play, mappe e musica non si caricano.', de='Die Uhr des Radios geht {0} Min. falsch ({1}). Falsche Zeit bricht HTTPS: Google Play, Karten und Musik laden nicht.',
  lv='Bloka pulkstenis nobīdīts par {0} min ({1}). Nepareizs laiks salauž HTTPS: Google Play, kartes un mūzika neielādējas.', pl='Zegar radia jest przestawiony o {0} min ({1}). Zły czas psuje HTTPS: Google Play, mapy i muzyka się nie ładują.')
n('k112', 'automatic time is on — check the internet / GPS', 'автоматическое время включено — проверить интернет / GPS', 'автоматичний час увімкнено — перевірити інтернет / GPS', pt='hora automática ligada — verifique a internet / GPS',
  es='hora automática activada — compruebe internet / GPS', fr='heure automatique activée — vérifiez internet / GPS', it='ora automatica attiva — controlla internet / GPS', de='automatische Zeit an — Internet / GPS prüfen', lv='automātiskais laiks ieslēgts — pārbaudi internetu / GPS', pl='automatyczny czas włączony — sprawdź internet / GPS')
n('k113', 'turn on Settings -> Date & time -> «Automatic date & time»', 'включить Настройки -> Дата и время -> «Дата и время сети»', 'увімкнути Налаштування -> Дата й час -> «Дата й час мережі»', pt='ative Definições -> Data e hora -> «Automática»',
  es='active Ajustes -> Fecha y hora -> «Automática»', fr='activez Paramètres -> Date et heure -> « Automatique »', it='attiva Impostazioni -> Data e ora -> «Automatica»', de='Einstellungen -> Datum & Uhrzeit -> „Automatisch“ einschalten', lv='ieslēdz Iestatījumi -> Datums un laiks -> «Automātiski»', pl='włącz Ustawienia -> Data i godzina -> „Automatycznie”')
n('k114', 'Automatic date & time is off: after a battery disconnect the clock goes wrong and HTTPS (Google Play, maps) breaks. Better turn it on.', 'Автоматические дата и время выключены: после отключения АКБ часы собьются и HTTPS (Google Play, карты) перестанет работать. Лучше включить.',
  'Автоматичні дата й час вимкнені: після відключення АКБ годинник зіб’ється і HTTPS (Google Play, карти) перестане працювати. Краще увімкнути.', pt='Data e hora automáticas desligadas: depois de desligar a bateria o relógio desacerta e o HTTPS (Google Play, mapas) falha. Melhor ligar.',
  es='Fecha y hora automáticas desactivadas: tras desconectar la batería el reloj se desajusta y el HTTPS (Google Play, mapas) falla. Mejor activarlas.', fr='Date et heure automatiques désactivées : après débranchement de la batterie l’horloge se dérègle et le HTTPS (Google Play, cartes) casse. Mieux vaut l’activer.',
  it='Data e ora automatiche disattivate: dopo aver staccato la batteria l’orologio si sballa e l’HTTPS (Google Play, mappe) non va. Meglio attivarle.', de='Automatische Zeit ist aus: nach Abklemmen der Batterie geht die Uhr falsch und HTTPS (Google Play, Karten) bricht. Besser einschalten.',
  lv='Automātiskais datums un laiks izslēgts: pēc akumulatora atvienošanas pulkstenis nobīdās un HTTPS (Google Play, kartes) nedarbojas. Labāk ieslēgt.', pl='Automatyczna data i czas wyłączone: po odłączeniu akumulatora zegar się rozjedzie i HTTPS (Google Play, mapy) przestanie działać. Lepiej włączyć.')
n('k115', 'Location is off — navigation won\'t see GPS. Turn on Settings -> Location.', 'Геолокация выключена — навигация не увидит GPS. Включить Настройки -> Местоположение.', 'Геолокацію вимкнено — навігація не бачитиме GPS. Увімкнути Налаштування -> Місцезнаходження.',
  pt='A localização está desligada — a navegação não vê o GPS. Ative Definições -> Localização.', es='La ubicación está desactivada — la navegación no verá el GPS. Active Ajustes -> Ubicación.', fr='La localisation est désactivée — la navigation ne verra pas le GPS. Activez Paramètres -> Localisation.',
  it='La posizione è disattivata — la navigazione non vedrà il GPS. Attiva Impostazioni -> Posizione.', de='Standort ist aus — die Navigation sieht kein GPS. Einstellungen -> Standort einschalten.', lv='Atrašanās vieta izslēgta — navigācija neredzēs GPS. Ieslēdz Iestatījumi -> Atrašanās vieta.', pl='Lokalizacja jest wyłączona — nawigacja nie zobaczy GPS. Włącz Ustawienia -> Lokalizacja.')
n('k116', 'Weak Wi-Fi signal ({0} dBm): maps and music will stutter. Keep the phone (hotspot) closer to the dashboard.', 'Слабый сигнал Wi-Fi ({0} дБм): карты и музыка будут подтормаживать. Держать телефон (точку доступа) ближе к торпедо.',
  'Слабкий сигнал Wi-Fi ({0} дБм): карти й музика пригальмовуватимуть. Тримати телефон (точку доступу) ближче до торпедо.', pt='Sinal Wi-Fi fraco ({0} dBm): mapas e música vão falhar. Mantenha o telemóvel (hotspot) mais perto do tablier.',
  es='Señal Wi-Fi débil ({0} dBm): mapas y música irán a trompicones. Deje el móvil (punto de acceso) más cerca del salpicadero.', fr='Signal Wi-Fi faible ({0} dBm) : cartes et musique vont saccader. Rapprochez le téléphone (partage) du tableau de bord.',
  it='Segnale Wi-Fi debole ({0} dBm): mappe e musica andranno a scatti. Tieni il telefono (hotspot) più vicino al cruscotto.', de='Schwaches WLAN ({0} dBm): Karten und Musik ruckeln. Handy (Hotspot) näher ans Armaturenbrett legen.',
  lv='Vājš Wi-Fi signāls ({0} dBm): kartes un mūzika raustīsies. Turi tālruni (tīklāju) tuvāk panelim.', pl='Słaby sygnał Wi-Fi ({0} dBm): mapy i muzyka będą się zacinać. Trzymaj telefon (hotspot) bliżej deski rozdzielczej.')
n('k117', '  Clock vs this computer: {0} min; auto time: {1}; location mode: {2}; Wi-Fi signal: {3} dBm', '  Часы относительно компьютера: {0} мин; авто-время: {1}; геолокация: {2}; сигнал Wi-Fi: {3} дБм',
  '  Годинник відносно комп’ютера: {0} хв; авто-час: {1}; геолокація: {2}; сигнал Wi-Fi: {3} дБм', pt='  Relógio vs computador: {0} min; hora auto: {1}; localização: {2}; sinal Wi-Fi: {3} dBm',
  es='  Reloj vs ordenador: {0} min; hora auto: {1}; ubicación: {2}; señal Wi-Fi: {3} dBm', fr='  Horloge vs ordinateur : {0} min ; heure auto : {1} ; localisation : {2} ; signal Wi-Fi : {3} dBm',
  it='  Orologio vs computer: {0} min; ora auto: {1}; posizione: {2}; segnale Wi-Fi: {3} dBm', de='  Uhr vs. Computer: {0} Min.; Auto-Zeit: {1}; Standort: {2}; WLAN-Signal: {3} dBm', lv='  Pulkstenis pret datoru: {0} min; auto laiks: {1}; atrašanās vieta: {2}; Wi-Fi signāls: {3} dBm',
  pl='  Zegar względem komputera: {0} min; auto czas: {1}; lokalizacja: {2}; sygnał Wi-Fi: {3} dBm')
n('k118', '  Settings snapshot (raw/unit, to restore by hand after a reset or flashing): ', '  Снимок настроек (raw/unit — чтобы вернуть руками после сброса или прошивки): ', '  Знімок налаштувань (raw/unit — щоб повернути вручну після скидання чи прошивки): ',
  pt='  Instantâneo das definições (raw/unit — para repor à mão após reposição ou flash): ', es='  Copia de ajustes (raw/unit — para restaurar a mano tras un reset o flasheo): ', fr='  Instantané des réglages (raw/unit — pour restaurer à la main après une réinitialisation ou un flash) : ',
  it='  Istantanea impostazioni (raw/unit — per ripristinare a mano dopo reset o flash): ', de='  Einstellungs-Schnappschuss (raw/unit — zum manuellen Wiederherstellen nach Reset/Flash): ', lv='  Iestatījumu momentuzņēmums (raw/unit — lai atjaunotu ar roku pēc atiestatīšanas): ',
  pl='  Kopia ustawień (raw/unit — do ręcznego przywrócenia po resecie lub flashowaniu): ')
n('k120', 'Install {0} ({1} MB) from the kit\'s apk folder', 'Установить {0} ({1} МБ) из папки apk набора', 'Встановити {0} ({1} МБ) з папки apk набору', pt='Instalar {0} ({1} MB) da pasta apk do kit',
  es='Instalar {0} ({1} MB) de la carpeta apk del kit', fr='Installer {0} ({1} Mo) depuis le dossier apk du kit', it='Installa {0} ({1} MB) dalla cartella apk del kit', de='{0} ({1} MB) aus dem apk-Ordner des Kits installieren', lv='Instalēt {0} ({1} MB) no komplekta mapes apk', pl='Zainstaluj {0} ({1} MB) z folderu apk zestawu')
n('k121', 'your apps (apk folder) — only if the owner wants', 'свои приложения (папка apk) — только если владелец хочет', 'свої застосунки (папка apk) — лише якщо власник хоче', pt='as suas apps (pasta apk) — só se o dono quiser',
  es='sus apps (carpeta apk) — solo si el dueño quiere', fr='vos applis (dossier apk) — seulement si le propriétaire le veut', it='le tue app (cartella apk) — solo se il proprietario vuole', de='eigene Apps (apk-Ordner) — nur wenn der Besitzer will', lv='savas lietotnes (mape apk) — tikai ja īpašnieks vēlas', pl='własne aplikacje (folder apk) — tylko jeśli właściciel chce')
n('k122', 'installed {0}: {1}', 'установлено {0}: {1}', 'встановлено {0}: {1}', pt='instalado {0}: {1}', es='instalado {0}: {1}', fr='installé {0} : {1}', it='installato {0}: {1}', de='installiert {0}: {1}', lv='instalēts {0}: {1}', pl='zainstalowano {0}: {1}')
n('k123', '{0}: updated an app that was already there (an update can\'t be rolled back)', '{0}: обновлено уже стоявшее приложение (обновление не откатывается)', '{0}: оновлено вже наявний застосунок (оновлення не відкочується)', pt='{0}: atualizada uma app que já existia (a atualização não se reverte)',
  es='{0}: actualizada una app que ya estaba (la actualización no se deshace)', fr='{0} : mise à jour d’une appli déjà présente (non annulable)', it='{0}: aggiornata un’app già presente (l’aggiornamento non si annulla)', de='{0}: vorhandene App aktualisiert (Update nicht rückgängig zu machen)', lv='{0}: atjaunināta jau esoša lietotne (atjauninājumu nevar atsaukt)', pl='{0}: zaktualizowano istniejącą aplikację (aktualizacji nie da się cofnąć)')
n('k124', '{0}: not installed — {1}', '{0}: не установилось — {1}', '{0}: не встановилося — {1}', pt='{0}: não instalado — {1}', es='{0}: no se instaló — {1}', fr='{0} : non installé — {1}', it='{0}: non installato — {1}', de='{0}: nicht installiert — {1}', lv='{0}: neinstalējās — {1}', pl='{0}: nie zainstalowano — {1}')
n('k125', 'removed the app the kit had installed: {0}', 'удалено приложение, которое ставил набор: {0}', 'видалено застосунок, який ставив набір: {0}', pt='removida a app que o kit instalou: {0}', es='eliminada la app que instaló el kit: {0}',
  fr='supprimée l’appli installée par le kit : {0}', it='rimossa l’app installata dal kit: {0}', de='vom Kit installierte App entfernt: {0}', lv='izdzēsta komplekta instalētā lietotne: {0}', pl='usunięto aplikację zainstalowaną przez zestaw: {0}')
n('k126', '- {0}: remove the app the kit installed', '- {0}: удалить приложение, которое ставил набор', '- {0}: видалити застосунок, який ставив набір', pt='- {0}: remover a app instalada pelo kit', es='- {0}: eliminar la app instalada por el kit',
  fr='- {0} : supprimer l’appli installée par le kit', it='- {0}: rimuovere l’app installata dal kit', de='- {0}: vom Kit installierte App entfernen', lv='- {0}: izdzēst komplekta instalēto lietotni', pl='- {0}: usunąć aplikację zainstalowaną przez zestaw')
n('k127', 'App installed: {0}', 'Установлено приложение: {0}', 'Встановлено застосунок: {0}', pt='App instalada: {0}', es='App instalada: {0}', fr='Appli installée : {0}', it='App installata: {0}', de='App installiert: {0}', lv='Lietotne instalēta: {0}', pl='Zainstalowano aplikację: {0}')
n('k128', '  installing {0} (up to a few minutes, don\'t touch the unit)...', '  ставлю {0} (до нескольких минут, магнитолу не трогать)...', '  встановлюю {0} (до кількох хвилин, магнітолу не чіпати)...', pt='  a instalar {0} (até uns minutos, não toque no autorrádio)...',
  es='  instalando {0} (hasta unos minutos, no toque el autorradio)...', fr='  installation de {0} (quelques minutes, ne touchez pas l’autoradio)...', it='  installo {0} (qualche minuto, non toccare lo stereo)...', de='  installiere {0} (bis zu ein paar Minuten, Radio nicht anfassen)...', lv='  instalēju {0} (līdz dažām minūtēm, bloku neaiztikt)...', pl='  instaluję {0} (do kilku minut, nie dotykaj radia)...')
n('k136', 'couldn\'t remove {0}: {1}', 'не удалось удалить {0}: {1}', 'не вдалося видалити {0}: {1}', pt='não foi possível remover {0}: {1}', es='no se pudo eliminar {0}: {1}', fr='impossible de supprimer {0} : {1}', it='impossibile rimuovere {0}: {1}', de='{0} ließ sich nicht entfernen: {1}', lv='neizdevās izdzēst {0}: {1}', pl='nie udało się usunąć {0}: {1}')
n('ui_mirror', 'Unit screen', 'Экран магнитолы', 'Екран магнітоли', pt='Ecrã do autorrádio', es='Pantalla del autorradio', fr='Écran de l’autoradio', it='Schermo dello stereo', de='Radio-Bildschirm', lv='Bloka ekrāns', pl='Ekran radia')
