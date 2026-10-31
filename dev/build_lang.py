# Собирает data/lang/*.json car-kit: языковые файлы phone-kit (папка-источник) + замены + новые ключи.
# python3 dev/build_lang.py <папка data/lang phone-kit> <папка data/lang car-kit>
import json, sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lang_car_base import NEW
from lang_car_ovr import OVR, MECH
src, dst = sys.argv[1], sys.argv[2]
LANGS = ['ru', 'uk', 'en', 'pt', 'es', 'fr', 'it', 'de', 'lv', 'pl']
MECH['en'] = [('phone-kit', 'car-kit')]
MECH['ru'] = [('phone-kit', 'car-kit')]
MECH['uk'] = [('phone-kit', 'car-kit')]
for l in LANGS:
    d = json.load(open(os.path.join(src, l + '.json'), encoding='utf-8-sig'))
    for k in d:
        for a, b in MECH[l]: d[k] = d[k].replace(a, b)
    for k, v in OVR.items():
        if v.get(l) is not None and k in d: d[k] = v[l]
        elif v.get(l) is not None: d[k] = v[l]
    for k, v in NEW.items():
        t = v.get(l)
        if t is None and l in ('ru', 'uk', 'en'): raise SystemExit('no %s for %s' % (l, k))
        if t is not None: d[k] = t
    with open(os.path.join(dst, l + '.json'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(json.dumps(d, ensure_ascii=False, indent=1))
    left = [k for k, v in d.items() if re.search(r'телефон|смартфон|\bphone\b|Telefon|telefon|téléphone|teléfono|telemóvel|tālru', v, re.I) and k not in ('m067','m068','m069','m070','m071','m072','m073','m074','m075','m076','m077','m078','m079','m080')]
    print(l, len(d), 'left:', ' '.join(left))
