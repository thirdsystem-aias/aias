#!/usr/bin/env python3
"""Arm A r2 diagnostic (no data, no API): why Freedman-Lane does not restore H_A2's size.

Same data-generating model and null scenarios as armA_power_sim.py (latent normal; Gs drives S and R; true
partial 0). Compares, on the SAME simulated data and permutation indices, the FL test of the r1/r2 statistic
(partial correlation on within-group normalised ranks) with the FL test of the same partial computed on the
latent values centred within group (no rank transform). If only the ranked version over-rejects, the excess
comes from the statistic (ranks of Gs within groups of 7/7/4 do not remove Gs's linear effect, so the rank
partial is above 0 when the latent partial is 0), not from the permutation scheme.
Seed 20261124 (same as the main simulation; separate run). Usage: armA_power_sim_fl_diag.py [REPS]
"""
import sys, time
import numpy as np
from armA_power_sim import (GROUPS, PERMS_A2, SEED, gen_a2, norm_ranks, partial_r, within_group_perms,
                            fl_null, pval_perm)

REPS = int(sys.argv[1]) if len(sys.argv) > 1 else 10000


def centre(v, groups):
    out = v.astype(float).copy(); i = 0
    for g in groups:
        out[i:i + g] -= out[i:i + g].mean(); i += g
    return out


def main():
    t0 = time.time()
    rng = np.random.default_rng(SEED)
    n = sum(GROUPS)
    print(f"seed={SEED} reps={REPS} perms={PERMS_A2}; FL with pooled reduced model R ~ Gs")
    print("scenario                               version             P(p<.025)  P(p<.05)  mean_partial")
    for rgs, rrg, lab in [(0.6, 0.5, "base"), (0.3, 0.3, "weak size link"), (0.8, 0.7, "strong size link"),
                          (0.9, 0.85, "size drives all three (very strong)")]:
        pr, pl, er, el = (np.empty(REPS) for _ in range(4))
        for i in range(REPS):
            r, s, g = gen_a2(rng, n, 0.0, rgs, rrg)
            idx = within_group_perms(rng, PERMS_A2, GROUPS)
            rn, sn, gn = norm_ranks(r, GROUPS), norm_ranks(s, GROUPS), norm_ranks(g, GROUPS)
            er[i] = partial_r(rn, sn, gn); pr[i] = pval_perm(er[i], fl_null(rn, sn, gn, idx, GROUPS))
            rc, sc, gc = centre(r, GROUPS), centre(s, GROUPS), centre(g, GROUPS)
            el[i] = partial_r(rc, sc, gc); pl[i] = pval_perm(el[i], fl_null(rc, sc, gc, idx, GROUPS))
        for nm, ps, es in (("within-group ranks", pr, er), ("latent, centred", pl, el)):
            print(f"{lab:37s}  {nm:18s}  {np.mean(ps<.025):9.4f}  {np.mean(ps<.05):8.4f}  {np.nanmean(es):12.3f}")
        sys.stdout.flush()
    print(f"[runtime {time.time() - t0:.1f} s]")


if __name__ == "__main__":
    main()
