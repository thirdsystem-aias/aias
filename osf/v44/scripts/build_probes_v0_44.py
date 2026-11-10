"""AIAS v0.44: build the probe file from the registries (DRAFT r0).

Reads osf/v44/registries/industries_v0_44.csv and the eight industry CSVs and writes
osf/v44/prereg/probes_v0_44.jsonl (one JSON object per line) plus a Markdown view.
Templates are the v0.20-v0.22 omnibus templates (osf/v42/prereg/probes_v0_42.jsonl):
Phase A  "Is the brand {B} commonly recognized as a {category} brand? Answer yes or no."
Phase B  six category questions, q1-q3 channel R_cat, q4-q6 channel R_cult, with the
category noun and the expert group filled per industry and "in the US" added because
the registries are US-market registries (PRE_REGISTRATION_v0_44 §4.1).
No system prompt. Probe order: Phase B by industry then frame; Phase A by industry
then unit. Run: python3 build_probes_v0_44.py  (stdlib only; deterministic)
"""
import csv, hashlib, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
REG = os.path.normpath(os.path.join(HERE, '..', 'registries'))
PRE = os.path.normpath(os.path.join(HERE, '..', 'prereg'))

PHASE_A = 'Is the brand {brand} commonly recognized as {art} {cat} brand? Answer yes or no.'
# (frame_id, channel, template, omnibus template it follows)
PHASE_B = [
    ('q1', 'R_cat', 'What are the best {noun} in the US? List several with descriptions.',
     'v20/v21/v22 q1 "What are the best {cat} brands? List several with descriptions."'),
    ('q2', 'R_cat', 'What {noun} do {experts} recommend in the US? Name several.',
     'v22 q2 "What car brands do automotive experts and reviewers recommend? Name several."'),
    ('q3', 'R_cat', 'What {noun} in the US are highest quality and most reliable? Name several with descriptions.',
     'v21/v22 q3 "What {cat} brands are highest quality and most reliable? Name several brands with descriptions."'),
    ('q4', 'R_cult', 'What {noun} are popular in the US right now? List several.',
     'v20/v21 q4 "What {cat} brands are popular right now? List several."'),
    ('q5', 'R_cult', 'What {noun} in the US have the most loyal customers? Name several.',
     'v20-v22 q5 slot (celebrity / affluent-buyer frame) generalised to customer loyalty'),
    ('q6', 'R_cult', 'Which {noun} in the US have the most iconic or storied identity in popular culture? Name several.',
     'v22 q6 "Which car brands have the most iconic or storied identity in popular culture? Name several."'),
]


def main():
    inds = list(csv.DictReader(open(os.path.join(REG, 'industries_v0_44.csv'), encoding='utf-8')))
    probes = []
    for ind in inds:
        for fid, ch, tpl, origin in PHASE_B:
            p = tpl.format(noun=ind['phase_b_noun'], experts=ind['phase_b_experts'])
            probes.append({'substrate': ind['industry'], 'phase': 'B', 'probe_id': '%s_B_%s' % (ind['industry'], fid),
                           'frame_id': fid, 'channel': ch, 'system': None, 'prompt': p,
                           'template_origin': origin, 'source_script': 'osf/v44/scripts/build_probes_v0_44.py'})
    for ind in inds:
        units = list(csv.DictReader(open(os.path.join(REG, os.path.basename(ind['file'])), encoding='utf-8')))
        for u in units:
            p = PHASE_A.format(brand=u['brand'], art=ind['phase_a_article'], cat=ind['phase_a_category'])
            probes.append({'substrate': ind['industry'], 'phase': 'A', 'probe_id': '%s_A_%s' % (ind['industry'], u['unit_id']),
                           'brand_id': u['unit_id'], 'brand': u['brand'], 'tier': u['tier'], 'system': None, 'prompt': p,
                           'template_origin': 'v20/v21/v22 Phase A "Is the brand {B} commonly recognized as a {cat} brand? Answer yes or no."',
                           'source_script': 'osf/v44/scripts/build_probes_v0_44.py'})
    ids = [p['probe_id'] for p in probes]
    assert len(ids) == len(set(ids))
    os.makedirs(PRE, exist_ok=True)
    out = os.path.join(PRE, 'probes_v0_44.jsonl')
    with open(out, 'w', encoding='utf-8') as f:
        for p in probes:
            f.write(json.dumps(p, ensure_ascii=False) + '\n')
    sha = hashlib.sha256(open(out, 'rb').read()).hexdigest()
    nA = sum(p['phase'] == 'A' for p in probes)
    nB = sum(p['phase'] == 'B' for p in probes)
    md = ['# AIAS v0.44 probe set (DRAFT r0, not locked)', '',
          'Built by `osf/v44/scripts/build_probes_v0_44.py` from `osf/v44/registries/`. %d probes: Phase B %d (6 per industry), Phase A %d (one per unit). SHA-256 of `probes_v0_44.jsonl`: `%s`.' % (len(probes), nB, nA, sha), '']
    for ind in inds:
        md += ['## %s: %s' % (ind['industry'], ind['label']), '', '| ID | Channel | Prompt |', '|---|---|---|']
        md += ['| %s | %s | %s |' % (p['probe_id'], p['channel'], p['prompt']) for p in probes if p['substrate'] == ind['industry'] and p['phase'] == 'B']
        ex = [p for p in probes if p['substrate'] == ind['industry'] and p['phase'] == 'A'][0]
        md += ['', 'Phase A (%d units), e.g. %s: "%s"' % (sum(1 for p in probes if p['substrate'] == ind['industry'] and p['phase'] == 'A'), ex['probe_id'], ex['prompt']), '']
    open(os.path.join(PRE, 'probes_v0_44.md'), 'w', encoding='utf-8').write('\n'.join(md) + '\n')
    print('probes:', len(probes), 'phase B:', nB, 'phase A:', nA)
    print('sha256:', sha)


if __name__ == '__main__':
    main()
