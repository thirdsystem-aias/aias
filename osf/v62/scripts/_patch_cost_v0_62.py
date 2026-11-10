"""One-off: patch cost_estimate_v0_62.py from r0 to r1 (see its docstring). Run once."""
p = "cost_estimate_v0_62.py"
s = open(p, encoding="utf-8").read()


def sub1(old, new):
    global s
    assert s.count(old) == 1, (old[:50], s.count(old))
    s = s.replace(old, new)


sub1('''"""AIAS v0.62 (non-English wave, draft r0): calls, cost estimate and design trade-off. No model is called.''',
'''"""AIAS v0.62 (non-English wave, r1 draft): calls, cost estimate and design trade-off. No model is called.

r1 changes (from r0): (1) the by-phase lines now list the judge reserve as its own line and print the sum check, so
that the phase lines add up to the adopted total (r0 printed the phase lines without the $1.32 reserve: $58.74 +
$1.32 = $60.06 December); (2) designs and projection ratios for the three headphones options (params_v0_62);
(3) the spend as the budget guard counts it (calls + judge reserve) at the end of blocks 1-3; (4) outputs
cost_estimate_v0_62_r1.json/.txt (the r0 files are kept unchanged).''')
sub1("import os\n", "import os\nimport sys\n\nsys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))\nimport params_v0_62 as P  # noqa: E402\n")
sub1('''def design(pc, month, langs=LANGS, b_runs=3, a_runs=1, s1_runs=0, factor='planning', judge=True):''',
'''def n_probes(option='A'):
    """(Phase B, A yes/no, A open) probes per language under a headphones option (A: 30/88/24; B: 30/87/24;
    C: 24/72/24)."""
    return (N_B - (6 if option == 'C' else 0), N_AYN - {'A': 0, 'B': 1, 'C': 16}[option], N_AOPEN)


def design(pc, month, langs=LANGS, b_runs=3, a_runs=1, s1_runs=0, factor='planning', judge=True, option='A'):''')
sub1('''            for phase, cond, n in (('B', 'S0', N_B * b_runs), ('A_yn', 'S0', N_AYN * a_runs),
                                   ('A_open', 'S0', N_AOPEN * a_runs), ('B', 'S1', N_B * s1_runs)):''',
'''            nb, nyn, nop = n_probes(option)
            for phase, cond, n in (('B', 'S0', nb * b_runs), ('A_yn', 'S0', nyn * a_runs),
                                   ('A_open', 'S0', nop * a_runs), ('B', 'S1', nb * s1_runs)):''')
sub1('''        ('plus_s1_x3_nov', 'adopted + Phase B S1 x3 (the full t4 design), November (not adopted)', dict(month='nov', s1_runs=3)),
    ]''', '''        ('plus_s1_x3_nov', 'adopted + Phase B S1 x3 (the full t4 design), November (not adopted)', dict(month='nov', s1_runs=3)),
    ]
    for o in ('A', 'B', 'C'):
        for mo, mname in (('nov', 'November'), ('dec', 'December')):
            spec.append(('option_%s_%s' % (o, mo), 'headphones option %s, %s prices' % (o, mname), dict(month=mo, option=o)))
            spec.append(('option_%s_block1_%s' % (o, mo), 'headphones option %s, block 1 only, %s' % (o, mname),
                         dict(month=mo, option=o, b_runs=1, a_runs=0)))''')
sub1('''    proj = {m: designs['adopted_' + m]['central'] / designs['block1_' + m]['central'] for m in ('nov', 'dec')}''',
'''    proj = {m: designs['adopted_' + m]['central'] / designs['block1_' + m]['central'] for m in ('nov', 'dec')}
    proj_opt = {o: {m: designs['option_%s_%s' % (o, m)]['central'] / designs['option_%s_block1_%s' % (o, m)]['central']
                    for m in ('nov', 'dec')} for o in ('A', 'B', 'C')}''')
sub1('''           'projection_ratio_adopted_to_block1_central': proj, 'break_even_uniform_factor_on_high_basis': be}''',
'''           'projection_ratio_adopted_to_block1_central': proj, 'projection': proj_opt,
           'headphones_option_in_params': P.HEADPHONES_OPTION, 'break_even_uniform_factor_on_high_basis': be}''')
sub1("""    L = ['AIAS v0.62 cost estimate (draft r0; no model called).""", """    L = ['AIAS v0.62 cost estimate (r1 draft; no model called).""")
sub1('''        for ph in ('B', 'A_yn', 'A_open'):
            rs = [r for r in d['rows'] if r['phase'] == ph]
            L.append('  phase %-7s calls %4d  %6.2f / %6.2f' % (ph, sum(r['calls'] for r in rs),
                                                             sum(r['usd_central'] for r in rs), sum(r['usd_high'] for r in rs)))''',
'''        sc, sh = 0.0, 0.0
        for ph in ('B', 'A_yn', 'A_open'):
            rs = [r for r in d['rows'] if r['phase'] == ph]
            c, h = sum(r['usd_central'] for r in rs), sum(r['usd_high'] for r in rs)
            sc, sh = sc + c, sh + h
            L.append('  phase %-7s calls %4d  %6.2f / %6.2f' % (ph, sum(r['calls'] for r in rs), c, h))
        L.append('  judge reserve      (144)  %6.2f / %6.2f' % (d['judge_reserve'], d['judge_reserve']))
        L.append('  sum of the lines above    %6.2f / %6.2f  (= total %6.2f / %6.2f)' % (
            sc + d['judge_reserve'], sh + d['judge_reserve'], d['central'], d['high']))
        b = [r for r in d['rows'] if r['phase'] == 'B']
        bc, bh = sum(r['usd_central'] for r in b), sum(r['usd_high'] for r in b)
        L.append('  spend as the guard counts it at the end of blocks 1-3 (Phase B + judge reserve): %6.2f / %6.2f'
                 '  (pause at $%.0f)' % (bc + d['judge_reserve'], bh + d['judge_reserve'], PAUSE))
    L += ['', 'Headphones options (params_v0_62.HEADPHONES_OPTION = %s):' % P.HEADPHONES_OPTION]
    for o in ('A', 'B', 'C'):
        n, d = designs['option_%s_nov' % o], designs['option_%s_dec' % o]
        L.append('  option %s: %4d calls; November %6.2f / %6.2f; December %6.2f / %6.2f; projection ratio Nov %.4f Dec %.4f'
                 % (o, n['calls'], n['central'], n['high'], d['central'], d['high'], proj_opt[o]['nov'], proj_opt[o]['dec']))''')
sub1("cost_estimate_v0_62_r0.json'), 'w'", "cost_estimate_v0_62_r1.json'), 'w'")
sub1("cost_estimate_v0_62_r0.txt'), 'w'", "cost_estimate_v0_62_r1.txt'), 'w'")
s = s.replace("osf/v62/prereg/cost_estimate_v0_62_r0.json and .txt", "osf/v62/prereg/cost_estimate_v0_62_r1.json and .txt")
open(p, "w", encoding="utf-8").write(s)
print("patched")
