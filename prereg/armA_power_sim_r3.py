#!/usr/bin/env python3
"""Arm A (SEO) r3 power/size simulation for H_A2 (decision D12 option b). No data, no API calls.

r3 test (Pablo, Tue 2026-11-24 8:13 am US Central, "As you suggest", D12 b):
  H_A2 statistic = Pearson partial correlation of r with s given gs, where r, s, gs are the natural-log
  shares centred within competitive group (log share minus the group's mean log share; groups 7/7/4,
  n = 18). One-sided Freedman-Lane permutation test: reduced model r ~ gs (one intercept, one slope),
  residuals permuted within group, r* = fitted + permuted residuals, the same partial recomputed.
  CONFIRMED needs partial >= 0.30 and Holm p < alpha (first Holm step .025, second .05).
  Declared sensitivities (no verdict): (i) the r2 test, FL on within-group normalised ranks;
  (ii) FL on the centred log values with an intercept and slope per group.

Data-generating model: as r1/r2 (armA_power_sim.gen_a2): latent normal Gs, S, R with corr(Gs,S) and
corr(R,Gs) per scenario and latent partial of R with S given Gs = 2 sin(pi rho_p / 6). The latent values
are read as LOG values of the raw quantities (etv, sales, mentions), i.e. raw values log-normal (skewed).
Because a share is the raw value divided by the group total, log share centred within group equals the
log raw value centred within group, so the centred latent values are exactly the r3 variables.
Extra r3 scenario ("R from counts"): mentions m ~ Poisson(lambda * exp(latent R)) with lambda set so the
mean is 4 mentions per brand (Shift: 18 answers per brand, zeros occur), R = (m + 0.5) / (M + 0.5 n_g)
before logs (the r3 zero rule), so r has ties and a floor at ln 0.5; S and Gs stay continuous.

Same scenarios, replicate counts and permutation count as r2's FL section; seed 20261124 (outside the
610001+ range proposed for the analysis); one fresh stream, run order fixed in main().
Usage: armA_power_sim_r3.py [NULL_REPS] [POWER_REPS]; r3 output armA_power_sim_out_r3.txt
(run with 20000 4000).
"""
import sys, time
import numpy as np
from armA_power_sim import (GROUPS, PERMS_A2, EFFECTS, gen_a2, lat, norm_ranks, partial_r,
                            within_group_perms, fl_null, pval_perm)

SEED = 20261124
NULL_REPS = int(sys.argv[1]) if len(sys.argv) > 1 else 20000
POWER_REPS = int(sys.argv[2]) if len(sys.argv) > 2 else 4000
SCEN = [(0.6, 0.5, "base"), (0.3, 0.3, "weak size link"), (0.8, 0.7, "strong size link"),
        (0.9, 0.85, "size drives all three (very strong)")]
MEAN_MENTIONS = 4.0


def centre(v, groups):
    out = v.astype(float).copy(); i = 0
    for g in groups:
        out[i:i + g] -= out[i:i + g].mean(); i += g
    return out


def counts_to_logshare(rng, r_lat, groups):
    """R from counts (extra scenario): Poisson mentions, +0.5 zero rule, log share."""
    m = rng.poisson(MEAN_MENTIONS * np.exp(r_lat - 0.5))  # E exp(N(0,1)) = e^0.5
    out = np.empty(len(m)); i = 0
    for g in groups:
        seg = m[i:i + g].astype(float)
        out[i:i + g] = np.log((seg + 0.5) / (seg.sum() + 0.5 * g)); i += g
    return out, m


def one_rep(rng, rho_p, rgs, rrg, counts=False):
    r, s, g = gen_a2(rng, sum(GROUPS), rho_p, rgs, rrg)
    zeros = 0
    if counts:
        r, m = counts_to_logshare(rng, r, GROUPS); zeros = int((m == 0).sum())
    idx = within_group_perms(rng, PERMS_A2, GROUPS)
    rc, sc, gc = centre(r, GROUPS), centre(s, GROUPS), centre(g, GROUPS)
    obs_c = partial_r(rc, sc, gc)
    p_c = pval_perm(obs_c, fl_null(rc, sc, gc, idx, GROUPS, "pooled"))
    p_cg = pval_perm(obs_c, fl_null(rc, sc, gc, idx, GROUPS, "group"))
    rn, sn, gn = norm_ranks(r, GROUPS), norm_ranks(s, GROUPS), norm_ranks(g, GROUPS)
    obs_r = partial_r(rn, sn, gn)
    p_r = pval_perm(obs_r, fl_null(rn, sn, gn, idx, GROUPS, "pooled"))
    return obs_c, p_c, p_cg, obs_r, p_r, zeros


def size_block(rng, label, rgs, rrg, counts):
    a = np.empty((NULL_REPS, 5)); z = 0
    for i in range(NULL_REPS):
        *vals, zr = one_rep(rng, 0.0, rgs, rrg, counts); a[i] = vals; z += zr
    oc, pc, pcg, orr, pr = a.T
    rows = (("FL centred log (r3 confirmatory)", pc, oc), ("FL centred log, per-group slopes", pcg, oc),
            ("FL within-group ranks (r2; sens.)", pr, orr))
    for nm, ps, es in rows:
        big = es >= 0.30
        print(f"{label:45s}  {nm:34s}  {np.mean(ps<.025):9.4f}  {np.mean(ps<.05):8.4f}"
              f"  {np.mean((ps<.025)&big):14.4f}  {np.mean((ps<.05)&big):13.4f}  {np.nanmean(es):12.3f}"
              f"  {int(np.isnan(es).sum())}")
    if counts:
        print(f"{'':45s}  [mean zero-mention brands per replicate: {z / NULL_REPS:.2f} of 18]")
    sys.stdout.flush()


def main():
    t0 = time.time()
    rng = np.random.default_rng(SEED)
    print(f"seed={SEED} null_reps={NULL_REPS} power_reps={POWER_REPS} perms={PERMS_A2} groups={GROUPS}")
    print("Same simulated data and permutation indices for every test within a replicate (paired).")
    print("\n=== H_A2 size under H0 (true partial 0). MC SE ~0.0011 at .025, ~0.0015 at .05 (20,000 reps) ===")
    hdr = (f"{'scenario':45s}  {'test':34s}  P(p<.025)  P(p<.05)  CONFIRMED@.025  CONFIRMED@.05  mean_partial"
           "  undefined")
    print(hdr)
    for rgs, rrg, lab in SCEN:
        size_block(rng, lab, rgs, rrg, counts=False)
    print("\n--- extra r3 scenario: R from Poisson counts (mean 4), +0.5 zero rule; S, Gs continuous ---")
    print(hdr)
    for rgs, rrg, lab in SCEN:
        size_block(rng, "counts: " + lab, rgs, rrg, counts=True)
    print(f"[size runtime {time.time() - t0:.1f} s]")

    print(f"\n=== H_A2 power (reps={POWER_REPS}); rho_p = r2's true effect, latent Pearson partial = "
          f"2 sin(pi rho_p/6) ===")
    print(f"{'scenario':37s}  rho_p  latent  test     P(p<.025)  P(p<.05)  CONFIRMED@.025  CONFIRMED@.05"
          "  mean_partial")
    for rgs, rrg, lab in SCEN:
        for e in EFFECTS[1:]:
            a = np.array([one_rep(rng, e, rgs, rrg)[:5] for _ in range(POWER_REPS)])
            oc, pc, _, orr, pr = a.T
            for nm, ps, es in (("FL-log", pc, oc), ("FL-rank", pr, orr)):
                big = es >= 0.30
                print(f"{lab:37s}  {e:5.2f}  {lat(e):6.3f}  {nm:7s}  {np.mean(ps<.025):9.3f}  {np.mean(ps<.05):8.3f}"
                      f"  {np.mean((ps<.025)&big):14.3f}  {np.mean((ps<.05)&big):13.3f}  {np.nanmean(es):12.3f}")
            sys.stdout.flush()
    print(f"\n[total runtime {time.time() - t0:.1f} s]")


if __name__ == "__main__":
    main()
