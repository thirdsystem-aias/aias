#!/usr/bin/env python3
"""AIAS v0.62: alias table r1 (draft) = r0 + the changes below + the check record of check_aliases_v0_62.py.

Changes (each logged in the pre-registration's 'Changes from r0'):
  parity with the certified English matchers (v0.20-v0.22 detect_mention matches the FULL registry string, e.g.
  "Mercedes-Benz", "Milani Cosmetics", "Clé de Peau Beauté"; an alias may not be looser than the English rule):
    Mercedes-Benz       drop bare ベンツ (= "Benz", not counted in English)
    Clé de Peau Beauté  drop bare クレ・ド・ポー (= "Clé de Peau", not counted in English)
    Milani Cosmetics    ミラニ -> ミラニ・コスメティックス (= "Milani Cosmetics")
  forms shown by a dated source:
    Nikka   add ニッカウヰスキー|ニッカウイスキー (company name; the katakana-boundary rule would otherwise reject
            ニッカ inside it, while v0.23's English rule \\bnikka\\b counts "Nikka Whisky")
    Lucid   add ルシード (Japanese Wikipedia title ルシード・モータース, via en "Lucid Motors")
Run: python3 osf/v62/scripts/make_alias_table_r1_v0_62.py -> osf/v62/translations/brand_aliases_v0_62_r1.csv
"""
import csv
import os

HERE = os.path.dirname(os.path.abspath(__file__))
T = os.path.join(HERE, '..', 'translations')
CHANGES = {
    'Mercedes-Benz': ('メルセデス・ベンツ', 'parity: bare ベンツ dropped (English rule needs "Mercedes-Benz")'),
    'Clé de Peau Beauté': ('クレ・ド・ポー・ボーテ', 'parity: bare クレ・ド・ポー dropped (English rule needs the full name)'),
    'Milani Cosmetics': ('ミラニ・コスメティックス', 'parity: bare ミラニ replaced by the full name (English rule needs "Milani Cosmetics")'),
    'Nikka': ('ニッカ|ニッカウヰスキー|ニッカウイスキー', 'added company name forms (katakana-boundary rule)'),
    'Lucid': ('ルーシッド|ルシード', 'added ルシード (ja Wikipedia: ルシード・モータース)'),
}


def main():
    r0 = list(csv.DictReader(open(os.path.join(T, 'brand_aliases_v0_62_r0.csv'), encoding='utf-8')))
    chk = {(r['substrate'], r['brand']): r for r in csv.DictReader(open(os.path.join(T, 'alias_check_v0_62_r1.csv'), encoding='utf-8'))}
    out = []
    for r in r0:
        c = chk[(r['substrate'], r['brand'])]
        row = dict(r)
        ch = CHANGES.get(r['brand'])
        row['r1_change'] = ''
        if ch:
            row['ja_aliases'], row['r1_change'] = ch
        status = c['status']
        if status == 'CHANGED?':
            status = 'CHANGED' if r['brand'] == 'Lucid' else 'UNCONFIRMED'
        src = []
        if c['found_official']:
            src.append(c['official_url'])
        if c['found_wikipedia'] or r['brand'] == 'Lucid':
            src.append('ja.wikipedia "%s" via %s' % (c['ja_wikipedia_title'], c['wikipedia_via']))
        row.update({'check_status': status, 'check_sources': ' ; '.join(src), 'check_accessed_utc': c['accessed_utc'],
                    'check_note': ('source shows "%s"' % c['ja_wikipedia_title']) if c['status'] == 'CHANGED?' else ''})
        out.append(row)
    with open(os.path.join(T, 'brand_aliases_v0_62_r1.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(out[0]))
        w.writeheader()
        w.writerows(out)
    from collections import Counter
    print(Counter(r['check_status'] for r in out), 'changed rows:', sum(bool(r['r1_change']) for r in out))


if __name__ == '__main__':
    main()
