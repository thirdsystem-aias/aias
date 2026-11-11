"""AIAS v0.62 (non-English wave, draft r2): build the Spanish, Korean and Chinese probe files. No model is called.

Inputs  osf/v62/inputs/probes_v0_42.jsonl            (t4 English probes; byte copy of v0.42 commit 527899e)
        osf/v62/translations/translations_v0_62_r2.json (hand-authored forward and back translations)
        osf/v62/translations/brand_aliases_v0_62_r2.csv (coding aliases, one row per brand unit)
Outputs osf/v62/translations/probes_{es,ko,zh}_v0_62_r2.jsonl (142 lines each, same order and IDs)
        osf/v62/translations/translation_review_v0_62_r2.md (side-by-side table with back-translations)
        osf/v62/translations/build_check_v0_62_r2.txt (checks and SHA-256)

Phase B prompts come from the translation file by (substrate, probe_id). Phase A prompts are built from
the language's template with the brand string cut out of the English prompt (never retyped), and for
v0.23 the category label cut out of the English prompt and mapped through the translation file.

Run: python3 osf/v62/scripts/build_translated_probes_v0_62.py
"""
import csv
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
V62 = os.path.normpath(os.path.join(HERE, '..'))
SRC = os.path.join(V62, 'inputs', 'probes_v0_42.jsonl')
SRC_SHA = '7aa246ee1b28a9bf4f55b8a5c124f099a75bb4ca029c0e42bf2ba1459c6323aa'
REV = 'r2'
TR = os.path.join(V62, 'translations', 'translations_v0_62_%s.json' % REV)
AL = os.path.join(V62, 'translations', 'brand_aliases_v0_62_%s.csv' % REV)
OUT = os.path.join(V62, 'translations')
LANGS = ('es', 'ko', 'zh')
RX_YN = {
    'v19': re.compile(r'^Is the brand (.+) commonly recognized as a brand of audiophile headphones\? Answer yes or no\.$'),
    'v20': re.compile(r'^Is the brand (.+) commonly recognized as a skincare brand\? Answer yes or no\.$'),
    'v21': re.compile(r'^Is the brand (.+) commonly recognized as a cosmetics brand\? Answer yes or no\.$'),
    'v22': re.compile(r'^Is the brand (.+) commonly recognized as a car brand\? Answer yes or no\.$'),
}
RX_V23 = re.compile(r"^What do you know about (.+)\? Specifically, I'm interested in it as a premium spirits brand "
                    r"— its positioning, reputation, product range, and how it fits within the broader (.+) "
                    r"category\. Please be detailed and specific\.$")


def sha(path):
    return hashlib.sha256(open(path, 'rb').read()).hexdigest()


def brand_and_cat(p):
    if p['substrate'] == 'v23':
        m = RX_V23.match(p['prompt'])
        return (m.group(1), m.group(2)) if m else (None, None)
    m = RX_YN[p['substrate']].match(p['prompt'])
    return (m.group(1), None) if m else (None, None)


def main():
    checks, fail = [], False
    s = sha(SRC)
    checks.append('source %s sha256 %s (%s)' % (os.path.relpath(SRC, V62), s, 'OK' if s == SRC_SHA else 'MISMATCH'))
    fail |= s != SRC_SHA
    src = [json.loads(line) for line in open(SRC, encoding='utf-8')]
    tr = json.load(open(TR, encoding='utf-8'))
    pb = {(r['substrate'], r['probe_id']): r for r in tr['phase_b']}
    tpl, cats = tr['phase_a_templates'], tr['v23_categories']
    aliases = list(csv.DictReader(open(AL, encoding='utf-8')))
    out = {lg: [] for lg in LANGS}
    brands = []
    for p in src:
        for lg in LANGS:
            q = dict(p)
            q['language'] = lg
            q['source_prompt_en'] = p['prompt']
            if p['phase'] == 'B':
                r = pb.get((p['substrate'], p['probe_id']))
                if r is None or r['en'] != p['prompt']:
                    checks.append('FAIL phase B %s %s: English text in translation file differs from source'
                                  % (p['substrate'], p['probe_id']))
                    fail = True
                    continue
                q['prompt'] = r[lg]
            else:
                b, c = brand_and_cat(p)
                if b is None:
                    checks.append('FAIL phase A %s %s: template did not match' % (p['substrate'], p['probe_id']))
                    fail = True
                    continue
                t = tpl[p['substrate']][lg].replace('{BRAND}', b)
                if c is not None:
                    if c not in cats:
                        checks.append('FAIL v23 category %r not in translation file' % c)
                        fail = True
                        continue
                    t = t.replace('{CATEGORY}', cats[c][lg])
                q['prompt'] = t
                q['brand_name'] = b
                if lg == LANGS[0]:
                    brands.append((p['substrate'], b))
            out[lg].append(q)
    for lg in LANGS:
        n = len(out[lg])
        nb = sum(1 for q in out[lg] if q['phase'] == 'B')
        checks.append('%s: %d probes (Phase B %d, Phase A %d)' % (lg, n, nb, n - nb))
        fail |= (n, nb) != (142, 30)
        left = [q['probe_id'] for q in out[lg] if '{' in q['prompt'] or '}' in q['prompt']]
        checks.append('%s: unfilled placeholders %d' % (lg, len(left)))
        fail |= bool(left)
        miss = [q['brand_name'] for q in out[lg] if q['phase'] == 'A' and q['brand_name'] not in q['prompt']]
        checks.append('%s: Phase A prompts carrying the registry brand string verbatim %d of %d'
                      % (lg, sum(1 for q in out[lg] if q['phase'] == 'A') - len(miss),
                         sum(1 for q in out[lg] if q['phase'] == 'A')))
        fail |= bool(miss)
        nbsp = sum(1 for q in out[lg] if ' ' in q['prompt'] or ' ' in q['prompt'])
        checks.append('%s: prompts containing no-break spaces %d' % (lg, nbsp))
        fail |= nbsp > 0
    al = {(a['substrate'], a['brand']) for a in aliases}
    checks.append('alias table rows %d; registry units %d; units without a row %d; rows without a unit %d'
                  % (len(aliases), len(brands), len(set(brands) - al), len(al - set(brands))))
    fail |= set(brands) != al
    NAMES = {'es': 'ES', 'ko': 'KO', 'zh': 'ZH'}
    for lg in ('ko', 'zh'):
        seen = {}
        for a in aliases:
            for x in filter(None, a[lg + '_aliases'].split('|')):
                key = (a['substrate'], x.replace(' ', '').replace('-', ''))
                if key in seen and seen[key] != a['brand']:
                    checks.append('FAIL %s alias %s shared by %s and %s' % (lg, x, seen[key], a['brand']))
                    fail = True
                seen[key] = a['brand']
        checks.append('%s aliases %d over %d units; collision-prone units %d (%s)' % (
            NAMES[lg], sum(len(list(filter(None, a[lg + '_aliases'].split('|')))) for a in aliases),
            sum(1 for a in aliases if a[lg + '_aliases']),
            sum(1 for a in aliases if a[lg + '_collision_prone'] == 'yes'),
            ', '.join(a['brand'] for a in aliases if a[lg + '_collision_prone'] == 'yes')))
    drift = {}
    for r in list(tr['phase_b']) + list(tpl.values()):
        for lg in LANGS:
            k = (lg, r.get(lg + '_drift'))
            drift[k] = drift.get(k, 0) + 1
    for lg in LANGS:
        checks.append('%s back-translation codes (30 Phase B + 5 templates): %s; meaning change %d' % (
            NAMES[lg], ', '.join('%s %d' % (k[1], v) for k, v in sorted(drift.items()) if k[0] == lg),
            drift.get((lg, 'meaning change'), 0)))
        fail |= drift.get((lg, 'meaning change'), 0) > 0
        fail |= sum(v for k, v in drift.items() if k[0] == lg) != 35
    zh_space = [q['probe_id'] for q in out.get('zh', []) if q['phase'] == 'B' and
                re.search(r'[一-鿿][A-Za-z]|[A-Za-z][一-鿿]', q['prompt'])]
    checks.append('ZH Phase B prompts with Han/Latin contact without a space: %d' % len(zh_space))
    fail |= bool(zh_space)
    for lg in LANGS:
        path = os.path.join(OUT, 'probes_%s_v0_62_%s.jsonl' % (lg, REV))
        with open(path, 'w', encoding='utf-8') as f:
            for q in out[lg]:
                f.write(json.dumps(q, ensure_ascii=False) + '\n')
        checks.append('wrote %s sha256 %s' % (os.path.relpath(path, V62), sha(path)))
    md = ['# v0.62 translation review table (%s draft)' % REV, '',
          'Forward and back translations by Claude Opus 5.5 in two passes (not independent; see the pre-registration, '
          'section 3). Phase B: all 30 items. Phase A: the five templates and the 15 v0.23 category labels (brand names '
          'are inserted unchanged). Codes: equivalent / minor drift / meaning change.', '']
    for r in list(tr['phase_b']) + [dict(t, substrate='Phase A template', probe_id=k) for k, t in tpl.items()]:
        md += ['## %s %s' % (r['substrate'], r['probe_id']), '', '- **EN** ' + r['en']]
        for lg in LANGS:
            md += ['- **%s** %s' % (NAMES[lg], r[lg]), '- %s back (%s): %s' % (NAMES[lg], r[lg + '_drift'], r[lg + '_back'])]
        if r.get('notes'):
            md.append('- Note: ' + r['notes'])
        md.append('')
    md += ['## v0.23 category labels', '', '| English | ES | ES back | KO | KO back | ZH | ZH back |',
           '|---|---|---|---|---|---|---|']
    for k, c in cats.items():
        md.append('| %s | %s |' % (k, ' | '.join('%s | %s' % (c[lg], c[lg + '_back']) for lg in LANGS)))
    open(os.path.join(OUT, 'translation_review_v0_62_%s.md' % REV), 'w', encoding='utf-8').write('\n'.join(md) + '\n')
    checks.append('RESULT ' + ('FAIL' if fail else 'PASS'))
    open(os.path.join(OUT, 'build_check_v0_62_%s.txt' % REV), 'w', encoding='utf-8').write('\n'.join(checks) + '\n')
    print('\n'.join(checks))
    sys.exit(1 if fail else 0)


if __name__ == '__main__':
    main()
