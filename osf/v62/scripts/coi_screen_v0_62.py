"""AIAS v0.62: registry string screen for DEVIATIONS Entry 0 (r0 terms; r3 adds terms). No model is called.

Checks the 112 registry brand names (column 'brand' of the alias table, which the build script checks against the brand
strings of the t4 probe file) for Samsung-group names. Whole-word, case-sensitive string match on names only: it does
not establish ownership, distribution, licensing or agency relationships of brands whose owner is not named (Entry 0,
Parts A and F, method limits). r0 terms: the Samsung-group names of v0.44 DEVIATIONS Entry 0 and v1.11 DEVIATIONS
Entry 0. r3 (2026-11-11) adds the Samsung-group companies, agencies, shops and brands met in the r3 screen (Entry 0,
Part F) and prints params_v0_62.COI_FLAGGED (the units with a tie found by the sources, not by this string screen).

Run: python3 osf/v62/scripts/coi_screen_v0_62.py -> osf/v62/prereg/coi_screen_v0_62_r3.txt (r0 output kept)
"""
import csv
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
V62 = os.path.normpath(os.path.join(HERE, '..'))
sys.path.insert(0, HERE)
import params_v0_62 as P  # noqa: E402

TERMS = ['Samsung', 'Harman', 'Harman Kardon', 'JBL', 'AKG', 'Infinity', 'Mark Levinson', 'Revel', 'Arcam', 'Lexicon',
         'Roon', 'Sound United', 'Masimo', 'Denon', 'Marantz', 'Bowers & Wilkins', 'B&W', 'Polk', 'Definitive Technology',
         'Boston Acoustics', 'Classé', 'HEOS', 'Cheil', 'Shilla', 'Bioepis', 'Samsung C&T', 'Ami', 'Maison Kitsuné',
         'Lemaire', 'Thom Browne']
TERMS_R3 = ['Samsung Electronics', 'Samsung SDI', 'Samsung Display', 'Samsung Electro-Mechanics', 'Samsung Biologics',
            'Samsung SDS', 'Samsung Life', 'Hotel Shilla', 'DFASS', 'Iris', 'McKinney', 'Barbarian', 'BMB', 'Pengtai',
            'Founded', 'LABEL C', 'Label C', 'BEAKER', '10 Corso Como', 'Ellis Brooklyn', 'Bamford', 'Maison Louis Marie',
            'J.Hannah', 'Absolution', 'Le Fournier', 'Sundays', 'Christophe Robin', 'Astier de Villatte', 'Margaret Howell',
            'Fitflop', 'Sandro', 'Maje', 'Claudie Pierlot', 'Fursac', 'Ganni', 'Studio Nicholson', 'Beanpole', '8Seconds',
            'Kuho', 'Galaxy']
TABLE = os.path.join(V62, 'translations', 'brand_aliases_v0_62_r2.csv')


def screen(names, terms):
    hits = []
    for sub, brand in names:
        for t in terms:
            if re.search(r'(?<![A-Za-z])' + re.escape(t) + r'(?![A-Za-z])', brand):
                hits.append((sub, brand, t))
    return hits


def main():
    rows = list(csv.DictReader(open(TABLE, encoding='utf-8')))
    names = [(r['substrate'], r['brand']) for r in rows]
    terms = TERMS + TERMS_R3
    hits = screen(names, terms)
    lines = ['v0.62 registry string screen (r3): %d registry units x %d terms (%d r0 + %d r3)'
             % (len(names), len(terms), len(TERMS), len(TERMS_R3)),
             'terms r0: ' + '; '.join(TERMS), 'terms r3: ' + '; '.join(TERMS_R3), 'matches: %d' % len(hits)]
    lines += ['  %s %s (term: %s)' % h for h in hits]
    lines += ['units with a tie found by the r3 sources (params_v0_62.COI_FLAGGED; Entry 0, Part F): '
              + '; '.join('%s %s' % u for u in P.COI_FLAGGED)]
    out = os.path.join(V62, 'prereg', 'coi_screen_v0_62_r3.txt')
    open(out, 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
    print('\n'.join(lines))


if __name__ == '__main__':
    main()
