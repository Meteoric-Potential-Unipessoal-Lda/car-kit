#!/bin/bash
# План car-kit Mobile должен совпадать с планом набора на ноутбуке (carkit.ps1) на тех же подставных магнитолах.
# bash tests/mobile/parity.sh <папка с классами Cli>   (нужны pwsh и java)
set -u
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
CP="$1"
WORK="$(mktemp -d)"
FAIL=0
export CARKIT_TEST_SCAN=192.168.43.120
for brand in fyt teyes ts mtc reglink generic; do
  kit="$WORK/kit-$brand"; mkdir -p "$kit/data/lang"
  cp "$ROOT/carkit.ps1" "$kit/"; cp "$ROOT"/data/*.tsv "$kit/data/"; cp "$ROOT"/data/lang/*.json "$kit/data/lang/"
  export MOCK_BRAND=$brand MOCK_STATE="$WORK/$brand.json"
  rm -f "$MOCK_STATE"
  # неизвестная магнитола: набор спрашивает «продолжить?» — отвечаем «да»
  if [ $brand = generic ]; then IN='2\nТ\nда\nq\n'; else IN='2\nТ\nq\n'; fi
  printf "$IN" | timeout 600 pwsh -NoProfile -File "$kit/carkit.ps1" -AdbPath "$ROOT/tests/mock_adb.py" -Lang ru -NoUpdateCheck -NoPause > "$WORK/pc-$brand.log" 2>&1
  rm -f "$MOCK_STATE"
  java -cp "$CP" net.zherdyev.carkit.Cli --root "$ROOT" --mock --mode diag > "$WORK/mob-$brand.log" 2>&1
  python3 - "$WORK/pc-$brand.log" "$WORK/mob-$brand.log" "$brand" <<'PY' || FAIL=1
import re, sys
pc, mob, brand = sys.argv[1:]
def norm(t):
    t = re.sub(r'\s+\(база: можно.*?\)$', '', t.strip())
    t = re.sub(r'\s+\(по желанию\)$', '', t)
    return re.sub(r'\s+', ' ', t)
a = []
for l in open(pc, encoding='utf-8', errors='replace'):
    m = re.search(r'\[(x| )\]\s+\d+\. (.*)$', l.rstrip())
    if m: a.append((m.group(1), norm(m.group(2))))
skip = ('Установить ', 'Сделать домашним')
a = [x for x in a if not x[1].startswith(skip) and '…сделать домашним' not in x[1]]
b = []
for l in open(mob, encoding='utf-8', errors='replace'):
    m = re.match(r'ITEM \[(x| )\] \S+ \S* \| .*? \| (.*)$', l.rstrip())
    if m: b.append((m.group(1), norm(m.group(2))))
if a == b:
    print('PASS parity %s: %d пунктов совпадают' % (brand, len(a)))
else:
    print('FAIL parity %s: ноутбук %d, телефон %d' % (brand, len(a), len(b)))
    sa, sb = set(a), set(b)
    for x in a:
        if x not in sb: print('   только ноутбук:', x)
    for x in b:
        if x not in sa: print('   только телефон:', x)
    if sa == sb: print('   (тот же набор, другой порядок)')
    sys.exit(1)
PY
done
exit $FAIL
