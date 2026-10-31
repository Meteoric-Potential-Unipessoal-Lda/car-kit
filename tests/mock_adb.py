#!/usr/bin/env python3
# Подставной adb для тестов car-kit: эмулирует Android-магнитолы.
# MOCK_BRAND = fyt (UIS7862, Joying) | teyes | ts (Topway TS10) | mtc (PX5 MTCE) | reglink (MTK) | aaos (Volvo) | generic (неизвестная)
# Подключение: по сети IP:5555 (adb connect), как у большинства магнитол. Флаги:
#   MOCK_USB=1         магнитола видна сразу (как по кабелю), без connect
#   MOCK_REFUSE=1      порт 5555 закрыт (connection refused)
#   MOCK_UNAUTH=1      первый connect -> failed to authenticate (ждём «Разрешить»)
#   MOCK_NONET_AFTER_REBOOT=1   после перезагрузки ADB по сети не возвращается
#   MOCK_BREAKCORE=<пакет>      если этот пакет отключён — служба магнитолы (com.syu.ms) падает
#   MOCK_BREAK=<пакет>          если этот пакет отключён — ломается рабочий стол
import sys, os, json
brand = os.environ.get('MOCK_BRAND', 'fyt')
SF = os.environ.get('MOCK_STATE', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mockstate.json'))
IP = '192.168.43.120'
ADDR = IP + ':5555'
st = {'disabled': [], 'uninst': [], 'settings': {}, 'appops': {}, 'idle': [], 'boot': 1, 'conn': 0, 'auth': 0, 'rebooted': 0}
if os.path.exists(SF):
    st = json.load(open(SF))
def save(): json.dump(st, open(SF, 'w'))

google = ['com.google.android.gms', 'com.google.android.gsf', 'com.android.vending', 'com.google.android.youtube', 'com.android.chrome', 'com.google.android.googlequicksearchbox',
  'com.google.android.apps.maps', 'com.google.android.feedback', 'com.google.android.music', 'com.google.android.videos', 'com.google.android.inputmethod.latin', 'com.google.android.apps.giant']
aosp = ['android', 'com.android.systemui', 'com.android.settings', 'com.android.egg', 'com.android.bips', 'com.android.printspooler', 'com.android.dreams.basic', 'com.facebook.appmanager',
  'com.android.providers.settings', 'com.android.shell', 'com.android.bluetooth']
props = {'ro.build.version.sdk': '29', 'ro.build.version.release': '10', 'ro.build.version.security_patch': '2021-05-05', 'ro.build.characteristics': 'tablet',
  'ro.serialno': '0123456789ABCDEF', 'ro.boot.verifiedbootstate': 'orange', 'ro.product.cpu.abilist': 'arm64-v8a,armeabi-v7a,armeabi'}
apkdir = {}
core = []
features = 'feature:android.hardware.wifi\nfeature:android.hardware.bluetooth\nfeature:android.hardware.location.gps'
home = 'com.android.launcher3/com.android.launcher3.Launcher'
if brand in ('fyt', 'teyes'):
    vend = ['com.syu.ms', 'com.syu.canbus', 'com.syu.bt', 'com.syu.ps', 'com.syu.radio', 'com.syu.music', 'com.syu.video', 'com.syu.eq', 'com.syu.steer', 'com.syu.settings',
      'com.syu.window', 'com.syu.mystery', 'com.fyt.boot', 'com.android.launcher6', 'com.zjinnova.zlink', 'com.adups.fota', 'cn.kuwo.kwmusicauto', 'com.txznet.smartadapter', 'com.sprd.systemupdate']
    props.update({'ro.product.model': 'UIS7862', 'ro.product.brand': 'Joying' if brand == 'fyt' else 'TEYES', 'ro.product.manufacturer': 'alps', 'ro.product.device': 'ums512_1h10',
      'ro.board.platform': 'ums512', 'ro.hardware': 'ums512_1h10', 'ro.build.version.release': '13', 'ro.fyt.platform': '6315', 'ro.build.fytmanufacturer': '14' if brand == 'fyt' else '95',
      'ro.fota.platform': 'SC7862', 'ro.build.fingerprint': 'alps/ums512_1h10/ums512_1h10:10/QP1A.190711.020/1:user/release-keys'})
    for p in vend: apkdir[p] = '/oem/app/190000000_%s/%s.apk' % (p, p)
    core = ['com.syu.ms', 'com.syu.canbus', 'com.syu.bt']
    home = 'com.android.launcher6/com.android.launcher6.Launcher'
elif brand == 'ts':
    vend = ['com.tw.car', 'com.tw.carchoose', 'com.tv.carinfoservice', 'com.tw.music', 'com.tw.radio', 'com.zjinnova.zlink', 'com.android.launcher3', 'cn.kuwo.kwmusicauto']
    props.update({'ro.product.model': 'ums512_1h10_Natv', 'ro.product.brand': 'alps', 'ro.product.manufacturer': 'alps', 'ro.board.platform': 'ums512', 'ro.hardware': 'ums512_1h10',
      'ro.build.display.id': 'TS10.20230401', 'ro.build.fingerprint': 'alps/ums512/ums512:10/QP1A/1:user/release-keys', 'persist.adb.tcp.port': '5555'})
    core = ['com.tw.car']
elif brand == 'mtc':
    vend = ['android.microntek.service', 'android.microntek.mtcser', 'com.microntek.music', 'com.microntek.radio', 'com.microntek.controlsettings', 'com.android.launcher3', 'com.rock.gota']
    props.update({'ro.product.model': 'px5', 'ro.product.brand': 'Android', 'ro.product.manufacturer': 'rockchip', 'ro.board.platform': 'rk3368', 'ro.hardware': 'rk30board',
      'ro.build.version.sdk': '28', 'ro.build.version.release': '9', 'ro.build.fingerprint': 'rockchip/px5/px5:9/PQ2A/1:user/release-keys', 'ro.serialno': 'MTCE12345'})
    apkdir['android.microntek.service'] = '/system/priv-app/MTCManager/MTCManager.apk'
    core = ['android.microntek.service', 'android.microntek.mtcser']
elif brand == 'reglink':
    vend = ['com.reglink.services', 'com.reglink.launcher4', 'com.baony.avm360', 'com.adups.fota', 'com.adups.fota.sysoper', 'com.mediatek.duraspeed']
    props.update({'ro.product.model': 'AC8257', 'ro.product.brand': 'alps', 'ro.product.manufacturer': 'alps', 'ro.board.platform': 'mt6765', 'ro.hardware': 'mt6765',
      'ro.build.version.sdk': '30', 'ro.build.version.release': '11', 'persist.duraspeed.support': '1'})
    core = ['com.reglink.services']
    home = 'com.reglink.launcher4/.Launcher'
elif brand == 'aaos':
    vend = ['com.volvocars.carsettings', 'com.android.car.settings']
    props.update({'ro.product.model': 'IHU', 'ro.product.brand': 'volvo', 'ro.product.manufacturer': 'Aptiv', 'ro.board.platform': 'msmnile', 'ro.build.version.sdk': '30', 'ro.build.version.release': '11'})
    features += '\nfeature:android.hardware.type.automotive'
else:
    vend = ['com.car.launcher', 'com.vendor.canbox', 'com.android.launcher3']
    props.update({'ro.product.model': 'Car Android', 'ro.product.brand': 'generic', 'ro.product.manufacturer': 'unknown', 'ro.board.platform': 'mt8163', 'ro.hardware': 'mt8163',
      'ro.build.version.sdk': '27', 'ro.build.version.release': '8.1.0'})
sysp = aosp + google + vend
third = {'com.waze': 'com.android.vending', 'com.spotify.music': 'com.android.vending', 'ru.yandex.yandexnavi': 'com.android.vending', 'com.oldgame.idle': 'com.android.vending'}
launch = ['com.waze', 'com.spotify.music', 'ru.yandex.yandexnavi', 'com.oldgame.idle', 'com.google.android.youtube', 'com.android.chrome', 'com.android.settings',
  'com.syu.radio', 'com.syu.music', 'com.syu.video', 'cn.kuwo.kwmusicauto', 'com.tw.music', 'com.microntek.music', 'com.google.android.apps.maps']
allp = sysp + list(third)
for _p in st.get('installed', []):
    third[_p] = 'com.android.shell'; allp.append(_p)

def installed(): return [p for p in allp if p not in st['uninst']]
def plist(ps): return '\n'.join('package:' + p for p in ps)

def shell(cmd):
    a = cmd.split()
    if cmd == 'getprop':
        return '\n'.join('[%s]: [%s]' % kv for kv in props.items()) + '\n[sys.boot_completed]: [1]'
    if a[0] == 'getprop':
        if a[1] == 'sys.boot_completed': return '1' if st['boot'] else ''
        return props.get(a[1], '')
    if cmd == 'id': return 'uid=0(root) gid=0(root) groups=0(root) context=u:r:su:s0' if brand == 'fyt' else 'uid=2000(shell) gid=2000(shell)'
    if cmd == 'cat /proc/meminfo': return 'MemTotal:        1900000 kB\nMemFree:          100000 kB\nMemAvailable:     350000 kB\nSwapTotal:       900000 kB\nSwapFree:         300000 kB'
    if cmd == 'cat /proc/uptime': return '2300000.5 2000000.1'
    if cmd == 'cat /proc/loadavg': return '8.10 7.80 7.50 2/1500 12345'
    if cmd == 'cat /sys/devices/system/cpu/present': return '0-7'
    if cmd.startswith('cat /sys/devices/system/cpu/cpu'): return '1800000' if 'max' in cmd else '1200000'
    if cmd == 'df -k /data': return 'Filesystem     1K-blocks     Used Available Use% Mounted on\n/dev/block/dm-2 25000000 12500000 12500000  50% /data'
    if cmd == 'ps -A -o RSS,NAME':
        r = 'RSS NAME\n250000 system_server\n150000 com.android.systemui\n320000 com.google.android.gms\n90000 com.oldgame.idle\n120000 com.waze\n60000 cn.kuwo.kwmusicauto\n'
        for c in core:
            if not (os.environ.get('MOCK_BREAKCORE') in st['disabled'] and c == core[0]): r += '80000 %s\n' % c
        return r
    if a[0] == 'pidof':
        p = a[1]
        if p in core and os.environ.get('MOCK_BREAKCORE') in st['disabled'] and p == core[0]: return ''
        if p in core or p == 'com.android.systemui': return '1234'
        return ''
    if cmd == 'dumpsys cpuinfo': return 'Load: 8.1 / 7.8 / 7.5\n  25% 1000/system_server: 10% user\n  18% 2000/com.google.android.gms: 8% user\n52% TOTAL: 30% user + 22% kernel'
    if cmd == 'dumpsys battery': return 'Current Battery Service state:\n  AC powered: true\n  level: 100\n  temperature: 350\n  health: 2'
    if cmd == 'dumpsys thermalservice': return 'Thermal Status: 0\n'
    if cmd == 'dumpsys diskstats': return 'Data-Free: 12500000K / 25000000K total = 50% free\nApp Package Names: ["com.waze"]\nApp Sizes: [200000000]\nApp Data Sizes: [300000000]\nCache Sizes: [100000000]'
    if a[:4] == ['du', '-s', '-k', '/sdcard/Android/media/com.whatsapp/WhatsApp/Media']: return '300000\t/sdcard/DCIM'
    if cmd == 'pm list packages -f':
        return '\n'.join('package:%s=%s' % (apkdir.get(p, '/system/app/%s/%s.apk' % (p.split('.')[-1], p.split('.')[-1])), p) for p in installed())
    if cmd == 'pm list features': return features
    if a[:3] == ['pm', 'list', 'packages']:
        fl = ''.join(x.strip('-') for x in a[3:])
        base = allp if 'u' in fl else installed()
        if 's' in fl: base = [p for p in base if p in sysp]
        if '3' in fl: base = [p for p in base if p in third]
        if 'd' in fl: base = [p for p in base if p in st['disabled']]
        if 'i' in fl: return '\n'.join('package:%s  installer=%s' % (p, third.get(p, 'null')) for p in base)
        return plist(base)
    if cmd == 'pm list users': return 'Users:\n\tUserInfo{0:Owner:13} running'
    if a[:2] == ['dumpsys', 'package']:
        p = a[2]
        if p == 'com.google.android.videos': return 'Packages:\n  Package [%s] (abc):\n    userId=1000\n    sharedUser=SharedUserSetting{1a2b android.uid.system/1000}' % p
        return 'Packages:\n  Package [%s] (abc):\n    userId=10%03d' % (p, len(p))
    if cmd.startswith('cmd package resolve-activity') and 'HOME' in cmd and os.environ.get('MOCK_BREAK') in st['disabled']: return 'android/com.android.internal.app.ResolverActivity'
    if cmd.startswith('cmd package resolve-activity') and 'HOME' in cmd: return 'priority=0 isDefault=true\n' + home
    if cmd.startswith('cmd package resolve-activity') and 'SETTINGS' in cmd: return 'priority=0\ncom.android.settings/.Settings'
    if cmd.startswith('cmd package query-activities') and 'LAUNCHER' in cmd: return '\n'.join(p + '/.Main' for p in launch if p in installed() and p not in st['disabled'])
    if cmd == 'dumpsys role': return 'Role Manager:\n  user_id=0\n    roles=[\n      {\n        name=android.app.role.HOME\n        holders=%s\n      }\n    ]' % home.split('/')[0]
    if cmd == 'settings get secure default_input_method': return 'com.google.android.inputmethod.latin/com.android.inputmethod.latin.LatinIME'
    if cmd == 'settings get secure enabled_accessibility_services': return 'null'
    if cmd == 'settings get secure enabled_notification_listeners': return 'null'
    if cmd == 'settings get secure android_id': return 'a1b2c3d4e5f60718'
    if a[:2] == ['settings', 'get']:
        dflt = {'window_animation_scale': '1.0', 'package_verifier_enable': '1', 'private_dns_mode': 'opportunistic'}
        if brand == 'reglink' and a[3] == 'setting.duraspeed.enabled': return '1'
        return st['settings'].get(a[3], dflt.get(a[3], 'null'))
    if a[:2] == ['settings', 'put']: st['settings'][a[3]] = a[4]; save(); return ''
    if a[:2] == ['settings', 'delete']: st['settings'].pop(a[3], None); save(); return 'Deleted 1 rows'
    if cmd == 'dumpsys usagestats':
        return ('  packages\n    package=com.waze totalTimeUsed="22:01:02" lastTimeUsed="2026-10-30 10:00:00"\n'
          '    package=com.spotify.music totalTimeUsed="11:01:02" lastTimeUsed="2026-10-30 10:00:00"\n'
          '    package=com.syu.radio totalTimeUsed="3:01:02" lastTimeUsed="2026-10-29 10:00:00"\n'
          '    package=com.android.launcher6 totalTimeUsed="2:01:02" lastTimeUsed="2026-10-30 10:00:00"\n'
          '    package=com.android.launcher3 totalTimeUsed="2:01:02" lastTimeUsed="2026-10-30 10:00:00"\n'
          '    package=com.android.settings totalTimeUsed="00:10:00" lastTimeUsed="2026-10-27 10:00:00"\n'
          '    package=com.oldgame.idle totalTimeUsed="00:00:20" lastTimeUsed="2026-04-01 10:00:00"\n')
    if cmd == 'dumpsys device_policy': return ''
    if cmd.startswith('cmd appops query-op'): return ''
    if a[:2] == ['cmd', 'appops'] and a[2] == 'get':
        m = st['appops'].get(a[3]); return ('RUN_ANY_IN_BACKGROUND: %s' % m) if m else 'No operations.'
    if a[:2] == ['cmd', 'appops'] and a[2] == 'set': st['appops'][a[3]] = a[5]; save(); return ''
    if cmd == 'dumpsys deviceidle whitelist':
        return 'system-excidle,com.android.shell,2000\nsystem,com.google.android.gms,10013\n' + ''.join('user,%s,10%03d\n' % (p, len(p)) for p in st['idle'])
    if a[:3] == ['dumpsys', 'deviceidle', 'whitelist'] and len(a) == 4:
        p = a[3][1:]
        if a[3][0] == '+':
            if p not in st['idle']: st['idle'].append(p)
            save(); return 'Added: ' + p
        if p in st['idle']: st['idle'].remove(p)
        save(); return 'Removed: ' + p
    if a[:2] == ['settings', 'list']: return '\n'.join('%s=%s' % kv for kv in {'screen_brightness': '120', 'bluetooth_name': 'CAR', 'auto_time': st['settings'].get('auto_time', '0')}.items())
    if cmd == 'cat /oem/app/config.txt': return 'car_type=Toyota_Camry_2018\ncanbus=raise_toyota\nsteer_key=1' if brand in ('fyt', 'teyes') else 'cat: /oem/app/config.txt: No such file or directory'
    if a[0] == 'cat' and a[1].startswith(('/oem', '/great', '/system/etc')): return 'cat: %s: No such file or directory' % a[1]
    if cmd == 'ls -l /oem/app': return 'drwxr-xr-x 2 root root 4096 2023-01-01 00:00 190000000_com.syu.ms'
    if cmd == 'date +%s':
        import time as _t
        return str(int(_t.time()) - (3600 if brand == 'fyt' else 0))
    if cmd == 'dumpsys wifi': return 'Wi-Fi is enabled\nmWifiInfo SSID: "Phone", BSSID: 02:00:00:00:00:00, RSSI: %d, Link speed: 72Mbps' % (-82 if brand == 'fyt' else -50)
    if cmd == 'dumpsys connectivity': return 'Active default network: 100\n  NetworkAgentInfo{network{100}  ni{WIFI CONNECTED} ... VALIDATED}'
    if cmd.startswith('logcat'): return '--------- beginning of crash'
    if a[:2] == ['pm', 'disable-user']:
        p = a[-1]
        if p not in st['disabled']: st['disabled'].append(p)
        save(); return 'Package %s new state: disabled-user' % p
    if a[:2] == ['pm', 'enable']:
        p = a[-1]
        if p in st['disabled']: st['disabled'].remove(p)
        save(); return 'Package %s new state: enabled' % p
    if a[:2] == ['pm', 'uninstall']:
        p = a[-1]
        if p not in st['uninst']: st['uninst'].append(p)
        save(); return 'Success'
    if 'install-existing' in cmd:
        p = a[-1]
        if p in st['uninst']: st['uninst'].remove(p)
        save(); return 'Package %s installed for user: 0' % p
    if cmd.startswith('pm trim-caches'): return ''
    if cmd in ('svc power reboot', 'reboot'):
        st['conn'] = 0; st['rebooted'] = 1; save(); return ''
    return '/system/bin/sh: unknown mock: ' + cmd

args = sys.argv[1:]
if args and args[0] == '-s': args = args[2:]
if not args: sys.exit(0)
c = args[0]
if c in ('start-server', 'kill-server', 'reconnect'): sys.exit(0)
if c == 'version': print('Android Debug Bridge version 1.0.41 (mock)'); sys.exit(0)
USB = os.environ.get('MOCK_USB')
if c == 'connect':
    t = args[1]
    if not t.startswith(IP):
        print('failed to connect to %s: No route to host' % t); sys.exit(1)
    if os.environ.get('MOCK_REFUSE') or (st.get('rebooted') and os.environ.get('MOCK_NONET_AFTER_REBOOT')):
        print('cannot connect to %s: Connection refused (111)' % t); sys.exit(1)
    if os.environ.get('MOCK_UNAUTH') and not st.get('auth'):
        st['auth'] = 1; st['conn'] = 1; save(); print('failed to authenticate to %s' % t); sys.exit(1)
    st['conn'] = 1; save(); print('connected to %s' % ADDR); sys.exit(0)
if c == 'install':
    apk = args[-1]
    p = 'com.example.' + os.path.basename(apk).split('.')[0].lower().replace('-', '')
    if p not in third: third[p] = 'com.android.shell'
    st.setdefault('installed', [])
    if p not in st['installed']: st['installed'].append(p)
    save(); print('Performing Streamed Install\nSuccess'); sys.exit(0)
if c == 'uninstall':
    p = args[-1]
    if p in st.get('installed', []): st['installed'].remove(p); save(); print('Success')
    else: print('Failure [DELETE_FAILED_INTERNAL_ERROR]')
    sys.exit(0)
if c == 'disconnect': st['conn'] = 0; save(); sys.exit(0)
if c == 'devices':
    print('List of devices attached')
    if USB: print('%s\tdevice' % 'USB123')
    elif st.get('conn'): print('%s\t%s' % (ADDR, 'device'))
    print(''); sys.exit(0)
if c == 'mdns': print('List of discovered mdns services'); sys.exit(0)
if c == 'shell':
    print(shell(' '.join(args[1:]))); sys.exit(0)
print('mock: unknown ' + ' '.join(args)); sys.exit(1)
