"""AIAS v0.62 (non-English wave, draft r0): calls, cost estimate and design trade-off. No model is called.

Per-call basis: the t4 wave's measured-basis figures (v0.42 r2, design "r2 (adopted)"), read from
osf/v62/inputs/cost_estimate_v0_42_r2.json (byte copy of v0.42 commit 527899e, SHA-256 checked below).
They are US$ per call, central / high, with the re-send allowance included (+2% / +10%), for an English
prompt: Phase B = category question, A_yn = yes/no brand question (v0.19-v0.22), A_open = open brand
question (v0.23). Prices are the programme list of 2026-11-10 (CLAUDE.md, Collection budget): Claude Fable
5.2 via the Message Batches API 4/20 per 1M tokens in/out; GPT-6 Astra standard 10/50; Gemini 4 Argon
standard 2/10 through 2026-11-30 (rows 't4') and 4/20 from 2026-12-01 (rows 't5' of the same file).

LANGUAGE FACTOR (planning assumption, NOT measured): a French or Japanese prompt and answer are assumed to
use more tokens than the English ones. No study-type French or Japanese answer from these models is on
record and no tokenizer is installed on the collection machine, so the factors below are declared
assumptions, replaced at the final pre-registration by t4's recorded usage and checked during collection
by the projection pause (actual usage after block 1). Central: FR 1.25, JA 1.50; high: FR 1.50, JA 2.00.
The script also reports the break-even factor (uniform over both languages) at which the design reaches
the $80 pause and the $100 cap.

Judge reserve (v0.23 open recognition answers, coding not acquisition): 24 answers x 3 models x 2 languages
= 144 calls on Claude Sonnet 4.5 (3/15 standard), at v0.42 r2's per-answer bound (1,500 input and 10 output
tokens) times the high JA factor (2.00) for input.

Run: python3 osf/v62/scripts/cost_estimate_v0_62.py -> osf/v62/prereg/cost_estimate_v0_62_r0.json and .txt
"""
import hashlib
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
V62 = os.path.normpath(os.path.join(HERE, '..'))
SRC = os.path.join(V62, 'inputs', 'cost_estimate_v0_42_r2.json')
SRC_SHA = '79831e64e7d5bf43c68d19797f86be8dd8d183925dc00577f8b3b7c23d2aa8d1'
PRE = os.path.join(V62, 'prereg')
SRC_DESIGN = 'r2 (adopted): N3, Fable via Batch API; B S0x3, B S1x3, A S0x1'
MODELS = ['claude-fable-5-2', 'gpt-6-astra', 'gemini-4-argon']
LANGS = ['fr', 'ja']
CAP, PAUSE = 100.0, 80.0
N_B, N_AYN, N_AOPEN = 30, 88, 24                      # per language, from the t4 probe file (142 = 30 + 112)
FACTOR = {'central': {'fr': 1.25, 'ja': 1.50}, 'high': {'fr': 1.50, 'ja': 2.00}, 'english': {'fr': 1.0, 'ja': 1.0}}
GEM_ROWS = {'nov': 't4', 'dec': 't5'}
JUDGE = {'calls': 144, 'in_tokens': 1500 * 2.00, 'out_tokens': 10, 'usd_in_per_m': 3.0, 'usd_out_per_m': 15.0}


def sha(path):
    return hashlib.sha256(open(path, 'rb').read()).hexdigest()


def per_call():
    j = json.load(open(SRC, encoding='utf-8'))
    pc = {}
    for wave in ('t4', 't5'):
        for r in j['designs'][SRC_DESIGN][wave]['rows']:
            pc[(wave, r['model'], r['phase'], r['condition'])] = (r['usd_per_call_central'], r['usd_per_call_high'])
    return pc


def judge_reserve():
    j = JUDGE
    return j['calls'] * (j['in_tokens'] * j['usd_in_per_m'] + j['out_tokens'] * j['usd_out_per_m']) / 1e6


def design(pc, month, langs=LANGS, b_runs=3, a_runs=1, s1_runs=0, factor='planning', judge=True):
    """factor='planning' -> central basis x central factor, high basis x high factor; 'english' -> factor 1."""
    rows, tc, th, calls = [], 0.0, 0.0, 0
    for lg in langs:
        fc = FACTOR['english' if factor == 'english' else 'central'][lg]
        fh = FACTOR['english' if factor == 'english' else 'high'][lg]
        for m in MODELS:
            wave = GEM_ROWS[month] if m == 'gemini-4-argon' else 't4'
            for phase, cond, n in (('B', 'S0', N_B * b_runs), ('A_yn', 'S0', N_AYN * a_runs),
                                   ('A_open', 'S0', N_AOPEN * a_runs), ('B', 'S1', N_B * s1_runs)):
                if n == 0:
                    continue
                c, h = pc[(wave, m, phase, cond)]
                rows.append({'language': lg, 'model': m, 'phase': phase, 'condition': cond, 'calls': n,
                             'usd_central': c * fc * n, 'usd_high': h * fh * n})
                tc += c * fc * n
                th += h * fh * n
                calls += n
    jr = judge_reserve() * (len(langs) / 2.0) if (judge and a_runs) else 0.0
    return {'calls': calls, 'central': tc + jr, 'high': th + jr, 'judge_reserve': jr, 'month': month, 'rows': rows}


def break_even(pc, month, target):
    """Uniform language factor f (both languages, applied to the HIGH basis) at which the adopted design reaches target."""
    d1 = design(pc, month, factor='english', judge=False)
    return (target - judge_reserve()) / d1['high']


def main():
    s = sha(SRC)
    assert s == SRC_SHA, 'per-call source changed: %s' % s
    pc = per_call()
    spec = [
        ('adopted_nov', 'ADOPTED: FR+JA, Phase B S0 x3, Phase A S0 x1, November prices', dict(month='nov')),
        ('adopted_dec', 'ADOPTED, December prices (Gemini 4 Argon 4/20)', dict(month='dec')),
        ('english_equiv_nov', 'adopted at language factor 1.0 (English token counts), November', dict(month='nov', factor='english')),
        ('fr_only_nov', 'French only, November', dict(month='nov', langs=['fr'])),
        ('ja_only_nov', 'Japanese only, November', dict(month='nov', langs=['ja'])),
        ('block1_nov', 'block 1 only: Phase B S0 run 1, FR+JA, November', dict(month='nov', b_runs=1, a_runs=0)),
        ('block1_dec', 'block 1 only: Phase B S0 run 1, FR+JA, December', dict(month='dec', b_runs=1, a_runs=0)),
        ('phase_b_only_nov', 'blocks 1-3 only: Phase B S0 x3, no Phase A, November (fallback F1)', dict(month='nov', a_runs=0)),
        ('phase_b_only_dec', 'blocks 1-3 only: Phase B S0 x3, no Phase A, December', dict(month='dec', a_runs=0)),
        ('no_run3_nov', 'Phase B S0 x2 + Phase A x1, November (fallback F2)', dict(month='nov', b_runs=2)),
        ('b_x1_nov', 'Phase B S0 x1 + Phase A x1, November (not adopted: no phi, no run noise)', dict(month='nov', b_runs=1)),
        ('a_x3_nov', 'Phase B S0 x3 + Phase A x3, November (not adopted)', dict(month='nov', a_runs=3)),
        ('plus_s1_x1_nov', 'adopted + Phase B S1 x1, November (not adopted)', dict(month='nov', s1_runs=1)),
        ('plus_s1_x3_nov', 'adopted + Phase B S1 x3 (the full t4 design), November (not adopted)', dict(month='nov', s1_runs=3)),
    ]
    designs = {}
    for key, label, kw in spec:
        d = design(pc, **kw)
        d['label'] = label
        designs[key] = d
    proj = {m: designs['adopted_' + m]['central'] / designs['block1_' + m]['central'] for m in ('nov', 'dec')}
    be = {m: {'pause_80': break_even(pc, m, PAUSE), 'cap_100': break_even(pc, m, CAP)} for m in ('nov', 'dec')}
    out = {'accessed': '2026-11-10', 'per_call_source': 'osf/v62/inputs/cost_estimate_v0_42_r2.json [' + SRC_DESIGN + '] sha256 ' + s,
           'language_factor_assumption': FACTOR, 'judge': dict(JUDGE, reserve_usd=judge_reserve()),
           'cap_usd': CAP, 'pause_usd': PAUSE, 'designs': designs,
           'projection_ratio_adopted_to_block1_central': proj, 'break_even_uniform_factor_on_high_basis': be}
    L = ['AIAS v0.62 cost estimate (draft r0; no model called). Per language: 30 category questions x 3 runs + 112 brand '
         'questions x 1 run, 3 models (N3), search off (S0).',
         'Language factor (assumption, not measured): central FR %.2f JA %.2f; high FR %.2f JA %.2f.'
         % (FACTOR['central']['fr'], FACTOR['central']['ja'], FACTOR['high']['fr'], FACTOR['high']['ja']),
         'Judge reserve (144 v0.23 recognition codings, Claude Sonnet 4.5): $%.2f, included where Phase A is collected.' % judge_reserve(), '',
         '%-78s %6s %10s %10s' % ('design', 'calls', 'expected', 'high')]
    for k, d in designs.items():
        L.append('%-78s %6d %10.2f %10.2f' % (d['label'], d['calls'], d['central'], d['high']))
    L += ['', 'Projection-pause ratio (adopted / block 1, central): November %.4f, December %.4f' % (proj['nov'], proj['dec']),
          'Block-1 spend above which the projection pause triggers ($80 / ratio): November $%.2f, December $%.2f'
          % (PAUSE / proj['nov'], PAUSE / proj['dec']),
          'Break-even uniform language factor on the HIGH per-call basis: November %.2f ($80) / %.2f ($100); '
          'December %.2f ($80) / %.2f ($100)' % (be['nov']['pause_80'], be['nov']['cap_100'], be['dec']['pause_80'], be['dec']['cap_100'])]
    for key in ('adopted_nov', 'adopted_dec'):
        d = designs[key]
        L += ['', '%s, by language x model (US$ expected / high):' % d['label']]
        for lg in LANGS:
            for m in MODELS:
                rs = [r for r in d['rows'] if r['language'] == lg and r['model'] == m]
                L.append('  %-3s %-18s calls %4d  %6.2f / %6.2f' % (lg, m, sum(r['calls'] for r in rs),
                                                                  sum(r['usd_central'] for r in rs), sum(r['usd_high'] for r in rs)))
        for ph in ('B', 'A_yn', 'A_open'):
            rs = [r for r in d['rows'] if r['phase'] == ph]
            L.append('  phase %-7s calls %4d  %6.2f / %6.2f' % (ph, sum(r['calls'] for r in rs),
                                                             sum(r['usd_central'] for r in rs), sum(r['usd_high'] for r in rs)))
    os.makedirs(PRE, exist_ok=True)
    json.dump(out, open(os.path.join(PRE, 'cost_estimate_v0_62_r0.json'), 'w', encoding='utf-8'), indent=1)
    open(os.path.join(PRE, 'cost_estimate_v0_62_r0.txt'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    print('\n'.join(L))


if __name__ == '__main__':
    main()
