#!/usr/bin/env python3
"""Arm A (SEO) r1 pre-lock power simulation. No data, no API calls.

Simulates the r1 draft's tests as written (prereg/arm_a_seo_prereg_draft_r1.md):
  H_A1: within-category Spearman, pooled Fisher-z mean weighted by n_c - 3,
        one-sided permutation test (P permuted within category).
        n_c = 18, 11, 26, 12 (draft s2.11). CONFIRMED needs rho_bar >= 0.30 and p < alpha.
  H_A2: partial correlation of R with S given Gs on within-group normalised
        ranks (groups 7, 7, 4; n = 18), one-sided permutation, R permuted within group.
        CONFIRMED needs partial >= 0.30 and p < alpha.
  H_A5 / H_A7: Spearman, n = 18, one-sided permutation.
Holm with two primary tests: the first step uses alpha 0.025, the second 0.05;
both are reported (bounds on the Holm-adjusted outcome).

ASSUMPTIONS (not in the draft; labelled): data are latent bivariate/trivariate
normal, no ties; the true Spearman rho_s is mapped to the latent Pearson
r = 2 sin(pi rho_s / 6); every brand is analysable; for H_A2 the latent
corr(Gs, S) and corr(R, Gs) are 0.6 and 0.5 (base case), with 0.3/0.3 and
0.8/0.7 as sensitivities; the true effect is the same in every category.
The within-category permutation null of a rank statistic without ties does
not depend on the data, so H_A1/H_A5/H_A7 use one precomputed null.
Simulation seed 20261124 (deliberately not in the 610001+ range proposed for
the analysis).

r2 (2026-11-24): adds the Freedman-Lane version of H_A2 (Pablo, Tue 11/24 7:29 am CT,
"ok Freedman-Lane"); see fl_null / fl_section. Usage: armA_power_sim.py [REPS] [FL_NULL_REPS]
[FL_POWER_REPS]; r2 output: armA_power_sim_out_r2.txt (run with 16000 20000 4000).
The r1 sections run first on the same stream, so their rows match armA_power_sim_out.txt.
"""
import sys, time
import numpy as np

SEED = 20261124
REPS = int(sys.argv[1]) if len(sys.argv) > 1 else 4000
NULL_DRAWS = 100_000
PERMS_A2 = 2000
EFFECTS = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]
NC = [18, 11, 26, 12]
GROUPS = [7, 7, 4]


def lat(rho_s):
    return 2 * np.sin(np.pi * rho_s / 6)


def spearman_rows(x, y):
    # x, y: (..., n) arrays; rank along last axis; Pearson of ranks
    rx = x.argsort(-1).argsort(-1).astype(float)
    ry = y.argsort(-1).argsort(-1).astype(float)
    rx -= rx.mean(-1, keepdims=True); ry -= ry.mean(-1, keepdims=True)
    return (rx * ry).sum(-1) / np.sqrt((rx ** 2).sum(-1) * (ry ** 2).sum(-1))


def pooled(rhos, ns):
    w = np.array(ns, float) - 3
    z = np.arctanh(np.clip(rhos, -0.999999, 0.999999))
    return np.tanh((z * w).sum(-1) / w.sum())


def null_spearman(rng, n, draws):
    base = np.tile(np.arange(n, dtype=float), (draws, 1))
    perm = rng.permuted(base, axis=1)
    return spearman_rows(base, perm)


def pval_upper(stat, null_sorted):
    # one-sided: share of null >= stat, with the +1 correction
    k = len(null_sorted) - np.searchsorted(null_sorted, stat, side="left")
    return (k + 1) / (len(null_sorted) + 1)


def gen_pair(rng, reps, n, rho_s):
    r = lat(rho_s)
    x = rng.standard_normal((reps, n))
    y = r * x + np.sqrt(1 - r * r) * rng.standard_normal((reps, n))
    return x, y


def norm_ranks(v, groups):
    out = np.empty_like(v, dtype=float); i = 0
    for g in groups:
        seg = v[..., i:i + g]
        out[..., i:i + g] = seg.argsort(-1).argsort(-1) / (g - 1)
        i += g
    return out


def partial_r(r_, s_, g_):
    def c(a, b):
        a = a - a.mean(-1, keepdims=True); b = b - b.mean(-1, keepdims=True)
        return (a * b).sum(-1) / np.sqrt((a * a).sum(-1) * (b * b).sum(-1))
    rs, rg, sg = c(r_, s_), c(r_, g_), c(s_, g_)
    # undefined (nan) when S or R ranks equal Gs ranks exactly; counted, never a pass
    with np.errstate(invalid="ignore", divide="ignore"):
        return (rs - rg * sg) / np.sqrt((1 - rg ** 2) * (1 - sg ** 2))


def gen_a2(rng, n, rho_p, r_gs, r_rg):
    gs = rng.standard_normal(n)
    e1, e2 = rng.standard_normal(n), rng.standard_normal(n)
    s = r_gs * gs + np.sqrt(1 - r_gs ** 2) * e1
    rp = lat(rho_p)
    r = r_rg * gs + np.sqrt(1 - r_rg ** 2) * (rp * e1 + np.sqrt(1 - rp ** 2) * e2)
    return r, s, gs


def within_group_perms(rng, k, groups):
    idx = []; i = 0
    for g in groups:
        base = np.tile(np.arange(i, i + g), (k, 1))
        idx.append(rng.permuted(base, axis=1)); i += g
    return np.concatenate(idx, axis=1)


def fl_null(rn, sn, gn, idx, groups, slopes="pooled"):
    """Freedman-Lane null of the H_A2 statistic (r2, Pablo 2026-11-24 7:29 am CT).
    Reduced model R ~ Gs on the within-group normalised ranks: 'pooled' = one intercept and one slope (the
    model the partial correlation itself conditions on; group means of normalised ranks are equal by
    construction); 'group' = intercept and slope per competitive group (sensitivity). Residuals of the
    reduced model are permuted within group (idx), added back to the fitted values, and the same statistic
    (partial correlation of R with S given Gs) is recomputed on each permuted R*. R* is not re-ranked."""
    n = len(rn)
    if slopes == "pooled":
        X = np.column_stack([np.ones(n), gn])
    else:
        cols, i = [], 0
        for g in groups:
            d = np.zeros(n); d[i:i + g] = 1.0
            cols += [d, d * gn]; i += g
        X = np.column_stack(cols)
    beta, *_ = np.linalg.lstsq(X, rn, rcond=None)
    fit = X @ beta
    res = rn - fit
    rstar = fit[None, :] + res[idx]
    return partial_r(rstar, sn[None, :], gn[None, :])


def pval_perm(obs, nul):
    if np.isnan(obs):
        return np.nan
    return (np.sum(nul >= obs - 1e-12) + 1) / (nul.shape[-1] + 1)


def fl_section(rng, t0):
    """r2 addition: size of the r1 within-group test and of Freedman-Lane, on the SAME simulated data and the
    SAME within-group permutation indices (paired), under every null scenario; then FL power."""
    n = sum(GROUPS)
    null_reps = int(sys.argv[2]) if len(sys.argv) > 2 else 20000
    pow_reps = int(sys.argv[3]) if len(sys.argv) > 3 else 4000
    scen = [(0.6, 0.5, "base"), (0.3, 0.3, "weak size link"), (0.8, 0.7, "strong size link"),
            (0.9, 0.85, "size drives all three (very strong)")]
    print(f"\n=== r2: H_A2 Freedman-Lane (FL) vs r1 within-group permutation (WG); null reps={null_reps}, "
          f"perms={PERMS_A2}, paired data and permutation indices ===")
    print("FL = reduced model R ~ Gs (one intercept, one slope); FLg = intercept and slope per group (sensitivity)")
    print("Size under H0 (true partial 0). MC SE at .025 with 20,000 reps ~ 0.0011; at .05 ~ 0.0015")
    print("scenario                               test  P(p<.025)  P(p<.05)  CONFIRMED@.025  CONFIRMED@.05  mean_partial  undefined")
    for rgs, rrg, lab in scen:
        p_wg, p_fl, p_flg, ests = (np.empty(null_reps) for _ in range(4))
        for i in range(null_reps):
            r, s, g = gen_a2(rng, n, 0.0, rgs, rrg)
            rn, sn, gn = norm_ranks(r, GROUPS), norm_ranks(s, GROUPS), norm_ranks(g, GROUPS)
            obs = partial_r(rn, sn, gn)
            idx = within_group_perms(rng, PERMS_A2, GROUPS)
            p_wg[i] = pval_perm(obs, partial_r(rn[idx], sn[None, :], gn[None, :]))
            p_fl[i] = pval_perm(obs, fl_null(rn, sn, gn, idx, GROUPS, "pooled"))
            p_flg[i] = pval_perm(obs, fl_null(rn, sn, gn, idx, GROUPS, "group"))
            ests[i] = obs
        big = ests >= 0.30
        for nm, ps in (("WG", p_wg), ("FL", p_fl), ("FLg", p_flg)):
            print(f"{lab:37s}  {nm:4s}  {np.mean(ps<.025):9.4f}  {np.mean(ps<.05):8.4f}"
                  f"  {np.mean((ps<.025)&big):14.4f}  {np.mean((ps<.05)&big):13.4f}  {np.nanmean(ests):12.3f}"
                  f"  {int(np.isnan(ests).sum())}")
        sys.stdout.flush()
    print(f"[FL size runtime {time.time() - t0:.1f} s]")
    print(f"\nH_A2 power with FL (pooled reduced model; reps={pow_reps})")
    print("scenario                               rho_p  P(p<.025)  P(p<.05)  CONFIRMED@.025  CONFIRMED@.05  mean_partial")
    for rgs, rrg, lab in scen:
        for e in EFFECTS[1:]:
            ps, ests = np.empty(pow_reps), np.empty(pow_reps)
            for i in range(pow_reps):
                r, s, g = gen_a2(rng, n, e, rgs, rrg)
                rn, sn, gn = norm_ranks(r, GROUPS), norm_ranks(s, GROUPS), norm_ranks(g, GROUPS)
                obs = partial_r(rn, sn, gn)
                idx = within_group_perms(rng, PERMS_A2, GROUPS)
                ps[i] = pval_perm(obs, fl_null(rn, sn, gn, idx, GROUPS, "pooled"))
                ests[i] = obs
            big = ests >= 0.30
            print(f"{lab:37s}  {e:5.2f}  {np.mean(ps<.025):9.3f}  {np.mean(ps<.05):8.3f}"
                  f"  {np.mean((ps<.025)&big):14.3f}  {np.mean((ps<.05)&big):13.3f}  {np.nanmean(ests):12.3f}")
            sys.stdout.flush()


def main():
    t0 = time.time()
    rng = np.random.default_rng(SEED)
    print(f"seed={SEED} reps={REPS} null_draws={NULL_DRAWS} perms_A2={PERMS_A2}")
    # H_A1 null of the pooled statistic
    null_c = [null_spearman(rng, n, NULL_DRAWS) for n in NC]
    null_a1 = np.sort(pooled(np.stack(null_c, -1), NC))
    null_18 = np.sort(null_spearman(rng, 18, NULL_DRAWS))
    print("\nH_A1 (n_c=18,11,26,12; pooled Fisher-z; within-category permutation)")
    print("rho_s  P(p<.025)  P(p<.05)  P(rho_bar>=.30)  CONFIRMED@.025  CONFIRMED@.05  mean_rho_bar")
    for e in EFFECTS:
        rc = []
        for n in NC:
            x, y = gen_pair(rng, REPS, n, e)
            rc.append(spearman_rows(x, y))
        rb = pooled(np.stack(rc, -1), NC)
        p = pval_upper(rb, null_a1)
        big = rb >= 0.30
        print(f"{e:4.2f}  {np.mean(p<.025):9.3f}  {np.mean(p<.05):8.3f}  {np.mean(big):15.3f}"
              f"  {np.mean((p<.025)&big):14.3f}  {np.mean((p<.05)&big):13.3f}  {rb.mean():12.3f}")
    print("\nH_A5 / H_A7 (Spearman n=18, one-sided permutation; verdict needs rho>0 and Holm p<.05)")
    print("rho_s  P(p<.0125)  P(p<.025)  P(p<.05)   [secondary family: Holm first step for 4-6 tests ~ .0083-.0125]")
    for e in EFFECTS:
        x, y = gen_pair(rng, REPS, 18, e)
        r = spearman_rows(x, y); p = pval_upper(r, null_18)
        print(f"{e:4.2f}  {np.mean(p<.0125):10.3f}  {np.mean(p<.025):9.3f}  {np.mean(p<.05):8.3f}")
    t1 = time.time()
    print(f"\n[H_A1/H_A5/H_A7 runtime {t1 - t0:.1f} s]")

    # H_A2
    reps2 = max(REPS // 4, 250)
    scen = [(0.6, 0.5, "base"), (0.3, 0.3, "weak size link"), (0.8, 0.7, "strong size link")]
    print(f"\nH_A2 (partial of R with S | Gs, within-group normalised ranks, groups 7/7/4; reps={reps2})")
    print("scenario           rho_p  P(p<.025)  P(p<.05)  CONFIRMED@.025  CONFIRMED@.05  mean_partial")
    n = sum(GROUPS)
    for rgs, rrg, lab in scen:
        for e in EFFECTS:
            ps, ests = np.empty(reps2), np.empty(reps2)
            for i in range(reps2):
                r, s, g = gen_a2(rng, n, e, rgs, rrg)
                rn, sn, gn = norm_ranks(r, GROUPS), norm_ranks(s, GROUPS), norm_ranks(g, GROUPS)
                obs = partial_r(rn, sn, gn)
                idx = within_group_perms(rng, PERMS_A2, GROUPS)
                nul = partial_r(rn[idx], sn[None, :], gn[None, :])
                ps[i] = np.nan if np.isnan(obs) else (np.sum(nul >= obs - 1e-12) + 1) / (PERMS_A2 + 1)
                ests[i] = obs
            big = ests >= 0.30
            print(f"{lab:17s}  {e:5.2f}  {np.mean(ps<.025):9.3f}  {np.mean(ps<.05):8.3f}"
                  f"  {np.mean((ps<.025)&big):14.3f}  {np.mean((ps<.05)&big):13.3f}  {np.nanmean(ests):12.3f}"
                  f"  undefined={int(np.isnan(ests).sum())}")
            sys.stdout.flush()
    print(f"\n[r1 sections runtime {time.time() - t0:.1f} s]")
    # r2: continues the same seeded stream after the r1 sections, so the r1 rows above reproduce unchanged
    fl_section(rng, t0)
    print(f"\n[total runtime {time.time() - t0:.1f} s]")


if __name__ == "__main__":
    main()
