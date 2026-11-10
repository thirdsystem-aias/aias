"""AIAS v0.62 (draft r0): registry string screen for DEVIATIONS Entry 0. No model is called.

Checks the 112 registry brand names (osf/v62/translations/brand_aliases_v0_62_r0.csv, column 'brand', which the
build script checks against the brand strings of the t4 probe file) for the Samsung-group names listed in
v0.44 DEVIATIONS Entry 0 and v1.11 DEVIATIONS Entry 0. Whole-word, case-sensitive string match on names only:
it does not establish ownership of brands whose owner is not named (see Entry 0, method limit).

Run: python3 osf/v62/scripts/coi_screen_v0_62.py -> osf/v62/prereg/coi_screen_v0_62_r0.txt
"""
import csv
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
V62 = os.path.normpath(os.path.join(HERE, '..'))
TERMS = ['Samsung', 'Harman', 'Harman Kardon', 'JBL', 'AKG', 'Infinity', 'Mark Levinson', 'Revel', 'Arcam', 'Lexicon',
         'Roon', 'Sound United', 'Masimo', 'Denon', 'Marantz', 'Bowers & Wilkins', 'B&W', 'Polk', 'Definitive Technology',
         'Boston Acoustics', 'Classé', 'HEOS', 'Cheil', 'Shilla', 'Bioepis', 'Samsung C&T', 'Ami', 'Maison Kitsuné',
         'Lemaire', 'Thom Browne']


def main():
    rows = list(csv.DictReader(open(os.path.join(V62, 'translations', 'brand_aliases_v0_62_r0.csv'), encoding='utf-8')))
    hits = []
    for r in rows:
        for t in TERMS:
            if re.search(r'(?<![A-Za-z])' + re.escape(t) + r'(?![A-Za-z])', r['brand']):
                hits.append((r['substrate'], r['brand'], t))
    lines = ['v0.62 registry string screen (r0): %d registry units x %d terms' % (len(rows), len(TERMS)),
             'terms: ' + '; '.join(TERMS), 'matches: %d' % len(hits)]
    lines += ['  %s %s (term: %s)' % h for h in hits]
    out = os.path.join(V62, 'prereg', 'coi_screen_v0_62_r0.txt')
    open(out, 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
    print('\n'.join(lines))


if __name__ == '__main__':
    main()
