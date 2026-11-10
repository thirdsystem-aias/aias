"""AIAS v0.44: cost estimate and design trade-off (DRAFT r0). No model is called.

Per-call costs are the t4 wave's measured-basis figures (v0.42 r2,
osf/v42/prereg/cost_estimate_v0_42_r2.json, design "r2 (adopted)"): US$ per call,
central / high, already including the re-send allowance (+2% central, +10% high).
Phase B uses the v0.42 'B' rows; Phase A (yes/no recognition) uses the 'A_yn' rows.
Gemini 4 Argon: the planning figures use the t5 rows of that file (Google's list price
from 2026-12-01, double the November price), as instructed for this wave; the November
figures are shown alongside. Claude Fable 5.2 via the Message Batches API; GPT-6 Astra
and Gemini 4 Argon synchronous (as in v0.42 r2).
Run: python3 cost_estimate_v0_44.py  -> ../prereg/cost_estimate_v0_44.json and .txt
"""
import csv, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
SRC = os.path.join(ROOT, 'osf', 'v42', 'prereg', 'cost_estimate_v0_42_r2.json')
PRE = os.path.normpath(os.path.join(HERE, '..', 'prereg'))
REG = os.path.normpath(os.path.join(HERE, '..', 'registries'))
MODELS = ['claude-fable-5-2', 'gpt-6-astra', 'gemini-4-argon']
CAP, PAUSE = 100.0, 80.0


def per_call():
    j = json.load(open(SRC, encoding='utf-8'))
    d = j['designs']['r2 (adopted): N3, Fable via Batch API; B S0x3, B S1x3, A S0x1']
    pc = {}
    for wave in ('t4', 't5'):
        for r in d[wave]['rows']:
            pc[(wave, r['model'], r['phase'], r['condition'])] = (r['usd_per_call_central'], r['usd_per_call_high'])
    return pc


def design(pc, n_b, n_a, b_s0_runs, b_s1_runs, a_runs, gem_wave):
    rows, tc, th, calls = [], 0.0, 0.0, 0
    for m in MODELS:
        wave = gem_wave if m == 'gemini-4-argon' else 't4'
        for phase, cond, n in (('B', 'S0', n_b * b_s0_runs), ('B', 'S1', n_b * b_s1_runs), ('A_yn', 'S0', n_a * a_runs)):
            if n == 0:
                continue
            c, h = pc[(wave, m, phase, cond)]
            rows.append({'model': m, 'phase': phase, 'condition': cond, 'calls': n,
                         'usd_per_call_central': c, 'usd_per_call_high': h,
                         'usd_central': c * n, 'usd_high': h * n, 'price_basis': wave})
            tc += c * n; th += h * n; calls += n
    return {'calls': calls, 'central': tc, 'high': th, 'rows': rows}


def main():
    pc = per_call()
    inds = list(csv.DictReader(open(os.path.join(REG, 'industries_v0_44.csv'), encoding='utf-8')))
    n_b = 6 * len(inds)
    n_a = sum(int(i['units']) for i in inds)
    designs = {
        'adopted: N3, Phase B S0 x3, Phase A S0 x1 (Gemini at Dec-1 price)': (3, 0, 1, 't5'),
        'adopted, Gemini at November price': (3, 0, 1, 't4'),
        'adopted + Phase B S1 x1': (3, 1, 1, 't5'),
        'adopted + Phase B S1 x3': (3, 3, 1, 't5'),
        'Phase B S0 x2 (instead of x3)': (2, 0, 1, 't5'),
        'Phase B S0 x1 (instead of x3)': (1, 0, 1, 't5'),
        'Phase A S0 x3 (instead of x1)': (3, 0, 3, 't5'),
    }
    out = {'accessed': '2026-11-10', 'per_call_source': 'osf/v42/prereg/cost_estimate_v0_42_r2.json',
           'n_phase_b_probes': n_b, 'n_phase_a_probes': n_a, 'cap_usd': CAP, 'pause_usd': PAUSE, 'designs': {}}
    lines = ['AIAS v0.44 cost estimate (DRAFT r0; no model called). Phase B probes %d, Phase A probes %d; 3 models.' % (n_b, n_a), '']
    for name, (s0, s1, a, gw) in designs.items():
        d = design(pc, n_b, n_a, s0, s1, a, gw)
        out['designs'][name] = d
        flag = 'over $100 at high' if d['high'] > CAP else ('over $80 pause at high' if d['high'] > PAUSE else 'within pause at high')
        lines.append('%-66s calls %5d   central $%7.2f   high $%7.2f   (%s)' % (name, d['calls'], d['central'], d['high'], flag))
    lines += ['', 'Adopted design by model and block (US$ central / high):']
    for r in out['designs']['adopted: N3, Phase B S0 x3, Phase A S0 x1 (Gemini at Dec-1 price)']['rows']:
        lines.append('  %-18s %-4s %-3s calls %4d  per call %.4f / %.4f  total %6.2f / %6.2f  [%s prices]' % (
            r['model'], r['phase'], r['condition'], r['calls'], r['usd_per_call_central'], r['usd_per_call_high'],
            r['usd_central'], r['usd_high'], r['price_basis']))
    json.dump(out, open(os.path.join(PRE, 'cost_estimate_v0_44.json'), 'w', encoding='utf-8'), indent=1)
    open(os.path.join(PRE, 'cost_estimate_v0_44.txt'), 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
    print('\n'.join(lines))


if __name__ == '__main__':
    main()
