"""AIAS v0.44: cost estimate and design trade-off (pre-registration draft r1). No model is called.

Per-call costs are the t4 wave's measured-basis figures (v0.42 r2,
osf/v42/prereg/cost_estimate_v0_42_r2.json, design "r2 (adopted)"): US$ per call,
central / high, already including the re-send allowance (+2% central, +10% high).
Phase B uses the v0.42 'B' rows; Phase A (yes/no recognition) uses the 'A_yn' rows.
Prices (v0.42 r2 section 4.5 = programme list of 2026-11-10): Claude Fable 5.2 via the
Message Batches API (4/20 per 1M tokens in/out); GPT-6 Astra standard (10/50); Gemini 4
Argon standard, 2/10 through 2026-11-30 (the 't4' rows) and 4/20 from 2026-12-01 (the
't5' rows of the same file).

r1 change: the planning estimate uses NOVEMBER prices (the collection window is
2026-11-24 to 2026-11-28); the December prices are reported alongside as the check that
a collection slipping past 2026-11-30 still fits under the $100 cap. Also new in r1: the
pharmacies-dropped variant (section 3.4) and the projection-pause ratio used by
acquire_v0_44.py (central estimate of the design / central estimate of block 1).

Run: python3 osf/v44/scripts/cost_estimate_v0_44.py -> osf/v44/prereg/cost_estimate_v0_44.json and .txt
"""
import csv
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
SRC = os.path.join(ROOT, 'osf', 'v42', 'prereg', 'cost_estimate_v0_42_r2.json')
PRE = os.path.normpath(os.path.join(HERE, '..', 'prereg'))
REG = os.path.normpath(os.path.join(HERE, '..', 'registries'))
MODELS = ['claude-fable-5-2', 'gpt-6-astra', 'gemini-4-argon']
CAP, PAUSE = 100.0, 80.0
SRC_DESIGN = 'r2 (adopted): N3, Fable via Batch API; B S0x3, B S1x3, A S0x1'
GEM_BASIS = {'nov': 't4', 'dec': 't5'}       # Gemini price rows: November list price / December list price


def per_call(src=SRC):
    j = json.load(open(src, encoding='utf-8'))
    d = j['designs'][SRC_DESIGN]
    pc = {}
    for wave in ('t4', 't5'):
        for r in d[wave]['rows']:
            pc[(wave, r['model'], r['phase'], r['condition'])] = (r['usd_per_call_central'], r['usd_per_call_high'])
    return pc


def design(pc, n_b, n_a, b_s0_runs, b_s1_runs, a_runs, month):
    rows, tc, th, calls = [], 0.0, 0.0, 0
    for m in MODELS:
        wave = GEM_BASIS[month] if m == 'gemini-4-argon' else 't4'
        for phase, cond, n in (('B', 'S0', n_b * b_s0_runs), ('B', 'S1', n_b * b_s1_runs), ('A_yn', 'S0', n_a * a_runs)):
            if n == 0:
                continue
            c, h = pc[(wave, m, phase, cond)]
            rows.append({'model': m, 'phase': phase, 'condition': cond, 'calls': n,
                         'usd_per_call_central': c, 'usd_per_call_high': h,
                         'usd_central': c * n, 'usd_high': h * n, 'price_basis': wave})
            tc += c * n
            th += h * n
            calls += n
    return {'calls': calls, 'central': tc, 'high': th, 'month': month, 'rows': rows}


def by_industry(inds, pc):
    """Calls and cost per industry for the adopted design (6 x 3 Phase B + units x 1 Phase A, per model)."""
    out = {}
    for i in inds:
        u = int(i['units'])
        row = {'phase_b_probes': 6, 'phase_a_probes': u, 'calls_per_model': 6 * 3 + u, 'calls': 3 * (6 * 3 + u)}
        for mo in ('nov', 'dec'):
            d = design(pc, 6, u, 3, 0, 1, mo)
            row['central_' + mo], row['high_' + mo] = d['central'], d['high']
        out[i['industry']] = row
    return out


def build(inds, pc):
    n_b = 6 * len(inds)
    n_a = sum(int(i['units']) for i in inds)
    no_pha = [i for i in inds if i['industry'] != 'PHA']
    nb2, na2 = 6 * len(no_pha), sum(int(i['units']) for i in no_pha)
    spec = {   # key: (label, n_b, n_a, B S0 runs, B S1 runs, A runs, month)
        'adopted': ('ADOPTED: N3, Phase B S0 x3, Phase A S0 x1, November prices (planning)', n_b, n_a, 3, 0, 1, 'nov'),
        'adopted_december': ('adopted, December prices (collection slips past 2026-11-30)', n_b, n_a, 3, 0, 1, 'dec'),
        'block1': ('block 1 only (Phase B S0 run 1), November prices', n_b, n_a, 1, 0, 0, 'nov'),
        'block1_december': ('block 1 only (Phase B S0 run 1), December prices', n_b, n_a, 1, 0, 0, 'dec'),
        'adopted_no_run3': ('adopted without Phase B run 3 (projection fallback), Nov', n_b, n_a, 2, 0, 1, 'nov'),
        'adopted_no_run3_december': ('adopted without Phase B run 3, December prices', n_b, n_a, 2, 0, 1, 'dec'),
        'pharmacies_dropped': ('pharmacies dropped (7 industries), November prices', nb2, na2, 3, 0, 1, 'nov'),
        'pharmacies_dropped_december': ('pharmacies dropped (7 industries), December prices', nb2, na2, 3, 0, 1, 'dec'),
        'plus_s1_x1': ('adopted + Phase B S1 x1, November prices', n_b, n_a, 3, 1, 1, 'nov'),
        'plus_s1_x3': ('adopted + Phase B S1 x3, November prices', n_b, n_a, 3, 3, 1, 'nov'),
        'b_s0_x2': ('Phase B S0 x2 (instead of x3), November prices', n_b, n_a, 2, 0, 1, 'nov'),
        'b_s0_x1': ('Phase B S0 x1 (instead of x3), November prices', n_b, n_a, 1, 0, 1, 'nov'),
        'a_s0_x3': ('Phase A S0 x3 (instead of x1), November prices', n_b, n_a, 3, 0, 3, 'nov'),
    }
    designs = {}
    for k, (label, b, a, s0, s1, ar, mo) in spec.items():
        d = design(pc, b, a, s0, s1, ar, mo)
        d['label'] = label
        designs[k] = d
    proj = {'ratio_design_to_block1_central': designs['adopted']['central'] / designs['block1']['central'],
            'ratio_design_to_block1_central_december':
                designs['adopted_december']['central'] / designs['block1_december']['central'],
            'rule': 'after block 1: pause if actual spend x ratio > $80 (December ratio if block 1 started on or '
                    'after 2026-12-01)'}
    return {'accessed': '2026-11-10', 'per_call_source': 'osf/v42/prereg/cost_estimate_v0_42_r2.json [' + SRC_DESIGN + ']',
            'n_phase_b_probes': n_b, 'n_phase_a_probes': n_a, 'by_industry': by_industry(inds, pc),
            'cap_usd': CAP, 'pause_usd': PAUSE, 'designs': designs, 'projection': proj}


def flag(d):
    return 'over $100 at high' if d['high'] > CAP else ('over $80 pause at high' if d['high'] > PAUSE else 'within pause at high')


def report(out):
    lines = ['AIAS v0.44 cost estimate (pre-registration draft r1; no model called). Phase B probes %d, Phase A probes %d; '
             '3 models.' % (out['n_phase_b_probes'], out['n_phase_a_probes']), '']
    for k, d in out['designs'].items():
        lines.append('%-62s calls %5d   central $%7.2f   high $%7.2f   (%s)' % (d['label'], d['calls'], d['central'],
                                                                             d['high'], flag(d)))
    p = out['projection']
    lines += ['', 'Projection pause ratio (adopted / block 1, central): November %.4f, December %.4f'
              % (p['ratio_design_to_block1_central'], p['ratio_design_to_block1_central_december']),
              'Block-1 spend above which the projection pause triggers ($80 / ratio): November $%.2f, December $%.2f'
              % (PAUSE / p['ratio_design_to_block1_central'], PAUSE / p['ratio_design_to_block1_central_december'])]
    for key in ('adopted', 'adopted_december'):
        d = out['designs'][key]
        lines += ['', 'Totals by model and by phase, %s (US$ central / high):' % d['label']]
        for m in MODELS:
            rs = [r for r in d['rows'] if r['model'] == m]
            lines.append('  %-18s calls %4d  %6.2f / %6.2f' % (m, sum(r['calls'] for r in rs),
                                                              sum(r['usd_central'] for r in rs), sum(r['usd_high'] for r in rs)))
        for ph in ('B', 'A_yn'):
            rs = [r for r in d['rows'] if r['phase'] == ph]
            lines.append('  phase %-12s calls %4d  %6.2f / %6.2f' % (ph, sum(r['calls'] for r in rs),
                                                                    sum(r['usd_central'] for r in rs), sum(r['usd_high'] for r in rs)))
    lines += ['', 'By industry, adopted design (calls; US$ central / high, November | December):']
    for k, r in out['by_industry'].items():
        lines.append('  %-4s calls %4d  %6.2f / %6.2f | %6.2f / %6.2f' % (k, r['calls'], r['central_nov'], r['high_nov'],
                                                                       r['central_dec'], r['high_dec']))
    for key in ('adopted', 'adopted_december'):
        lines += ['', 'Adopted design by model and block, %s (US$ central / high):' % out['designs'][key]['label']]
        for r in out['designs'][key]['rows']:
            lines.append('  %-18s %-4s %-3s calls %4d  per call %.4f / %.4f  total %6.2f / %6.2f  [%s rows]' % (
                r['model'], r['phase'], r['condition'], r['calls'], r['usd_per_call_central'], r['usd_per_call_high'],
                r['usd_central'], r['usd_high'], r['price_basis']))
    return lines


def main():
    inds = list(csv.DictReader(open(os.path.join(REG, 'industries_v0_44.csv'), encoding='utf-8')))
    out = build(inds, per_call())
    lines = report(out)
    json.dump(out, open(os.path.join(PRE, 'cost_estimate_v0_44.json'), 'w', encoding='utf-8'), indent=1)
    open(os.path.join(PRE, 'cost_estimate_v0_44.txt'), 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
    print('\n'.join(lines))


if __name__ == '__main__':
    main()
