import csv, sys, json
from decimal import Decimal, ROUND_HALF_UP
exp_path, rep_path, out_path = sys.argv[1:4]
exp = list(csv.DictReader(open(exp_path, newline='')))
rep = {r['id']: r for r in csv.DictReader(open(rep_path, newline=''))}
WORDS = {'five': 5, 'six': 6}
def q(x, nd):
    return Decimal(repr(float(x))).quantize(Decimal(1).scaleb(-nd), rounding=ROUND_HALF_UP)
rows, fails, kinds = [], [], {}
for e in exp:
    i, pub, digits = e['id'], e['published_value_as_printed'].strip(), e['digits']
    r = rep.get(i)
    got = None if r is None else r['value'].strip()
    if got is None:
        ok, shown, rule = False, 'MISSING', 'present'
    elif pub == 'not rated' or got == 'not rated':
        ok, shown, rule = (pub == got), got, 'not rated must match'
    elif digits.startswith('exact'):
        p = WORDS.get(pub, None)
        p = int(pub) if p is None else p
        ok, shown, rule = (int(float(got)) == p and float(got) == int(float(got))), got, 'exact count'
    elif 'decimals' in digits:
        nd = int(digits.split()[0])
        shown = str(q(got, nd)); ok = (shown == pub); rule = f'rounded to {nd} decimals'
    elif 'percent' in digits:
        p = int(pub.rstrip('%'))
        shown = str(q(float(got) * (100 if float(got) <= 1 else 1), 0)); ok = (int(Decimal(shown)) == p); rule = 'whole percent'
    else:
        ok, shown, rule = False, got, 'UNKNOWN RULE ' + digits
    kinds[rule] = kinds.get(rule, 0) + 1
    rows.append({'id': i, 'quantity': e['quantity'], 'category': e['category'], 'brand': e['brand'],
                 'published': pub, 'reproduced_full': got if got is not None else '', 'reproduced_at_published_digits': shown,
                 'rule': rule, 'match': 'yes' if ok else 'NO'})
    if not ok: fails.append(rows[-1])
extra = sorted(set(rep) - {e['id'] for e in exp})
with open(out_path, 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print(json.dumps({'compared': len(rows), 'matches': len(rows) - len(fails), 'differences': len(fails),
                  'rules': kinds, 'extra_ids_in_reproduction': extra[:10], 'n_extra': len(extra)}, indent=1))
for x in fails[:40]: print('DIFF', x)
