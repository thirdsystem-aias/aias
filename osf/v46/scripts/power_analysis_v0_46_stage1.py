#!/usr/bin/env python3
"""A priori power analysis for v0.46 (#76) Stage 1 Registered Report, draft r1 (2026-11-21). Synthetic data only.

No model is called. Extends the r0 precision simulation (precision_sim_v0_46.py, whose unit values and
generator it imports unchanged) to the Stage 1 design, in which Presence (P) and Ranking (R*) are
re-measured in the same collection as the choices.

Assumptions (all stated in the manuscript, section 6):
  A1 Units and their relative prominence: t4 recall values pi_N3_S0 of the four categories (r0's PI table;
     cars without Cell D), standardised within category = the latent prominence z that drives choice.
  A2 Choice generator (r0): each of 3 models chooses by a multinomial logit on
     scale * (beta * z + shared brand appeal (SD 1) + model-specific appeal (SD 0.5)).
     scale 2 = concentrated (about 70-75% of choices on the top 3 units), 0.7 = diffuse.
  A3 Re-measurement noise: the re-measured predictor is r * z + sqrt(1 - r^2) * e, e ~ N(0, 1), with
     r = 1 (no noise) or r = 0.81 (the lowest per-brand Presence stability the programme has measured where
     measurable, v0.34: rho 0.81 / 0.99 / 1.00).
  A4 Effect sizes are set on the statistic itself: beta is calibrated so that the expected U-bar on the
     re-measured predictor equals the target (0.60 = FALSIFIED bound, 0.70 = CONFIRMED bar = smallest
     effect of interest for the verdict, plus 0.65 and 0.75).
  A5 OPEN: 30% of answers fall outside the registry (OTHER); an assumption, not a measured value.
  A6 Ranking: rated units = the top-n units by z per category (n = 13, 15, 14, 18, the t4 counts of r1);
     z_R correlates 0.369 with z among rated units (t4, v1.14 Stage 1); H4's SESOI is OR_R = 1.25.
  A7 Position: a linear order effect gamma * (1 - d), d = normalised position; SESOI d-bar = 0.45 (edge of
     the pre-declared order-robust band [0.45, 0.55]).
Tests exactly as pre-registered: within-category permutation of the predictor (H1-H3), Freedman-Lane
permutation of the residualised R* (H4), reassignment of orders within (category, model, brief) (H5).
Draw counts are reduced for the simulation (stated in the output). Seed 46760 (power analysis only).
Usage: python3 power_analysis_v0_46_stage1.py [n_sims] [n_draws]
Writes osf/v46/prereg/power_analysis_v0_46_stage1_r1.json and .txt.
"""
import json
import sys
import time
from pathlib import Path

import numpy as np
from scipy.optimize import minimize
from scipy.stats import rankdata

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import precision_sim_v0_46 as P0  # noqa: E402

CATS = P0.CATS
Z = P0.Z
L = {c: len(P0.PI[c]) for c in CATS}
N_RATED = {"skincare": 13, "cosmetics": 15, "cars": 14, "spirits": 18}
RHO_RP = 0.369
SEED = 46760
MODELS = 3


def pct(x):
    return (rankdata(x) - 0.5) / len(x)


def measured(rng, r):
    return {c: r * Z[c] + np.sqrt(max(0.0, 1 - r * r)) * rng.normal(0, 1, L[c]) for c in CATS}


def choose_counts(rng, beta, scale, n_per_model, zdrive=None, extra=None):
    """Counts per unit per category (summed over models). n_per_model[c] choices per model."""
    out = {}
    for c in CATS:
        zc = Z[c] if zdrive is None else zdrive[c]
        shared = rng.normal(0, 1, L[c])
        tot = np.zeros(L[c])
        for _ in range(MODELS):
            u = scale * (beta * zc + shared + rng.normal(0, 0.5, L[c]))
            if extra is not None:
                u = u + extra[c]
            p = np.exp(u - u.max())
            tot += rng.multinomial(n_per_model[c], p / p.sum())
        out[c] = tot
    return out


def ubar(counts, uu):
    return sum((counts[c] * uu[c]).sum() for c in CATS) / max(1.0, sum(counts[c].sum() for c in CATS))


def perm_p(counts, uu, rng, draws):
    """Within-category permutation of the predictor percentiles (r1 section 2.1), one-sided."""
    obs = ubar(counts, uu)
    n = sum(counts[c].sum() for c in CATS)
    null = np.zeros(draws)
    for c in CATS:
        idx = np.argsort(rng.random((draws, len(uu[c]))), axis=1)
        null += uu[c][idx] @ counts[c]
    null /= max(1.0, n)
    return obs, (1 + (null >= obs - 1e-12).sum()) / (draws + 1)


def verdict(u, p, n_valid, n_min):
    if n_valid < n_min:
        return "UNDETERMINED"
    if u >= 0.70 and p < 0.05:
        return "CONFIRMED"
    if u < 0.60:
        return "FALSIFIED"
    return "MARGINAL"


def calibrate(target, scale, r, rng, n_per_model, sims=150, lo=-1.0, hi=6.0):
    """beta such that E[U-bar on the re-measured predictor] = target (bisection; U-bar rises with beta)."""
    for _ in range(14):
        mid = (lo + hi) / 2
        us = []
        for _ in range(sims):
            m = measured(rng, r)
            us.append(ubar(choose_counts(rng, mid, scale, n_per_model), {c: pct(m[c]) for c in CATS}))
        if np.mean(us) < target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def summarise(rows):
    u = np.array([x[0] for x in rows])
    p = np.array([x[1] for x in rows])
    v = [x[2] for x in rows]
    return {"mean_U": round(float(u.mean()), 3), "sd_U": round(float(u.std()), 3),
            "P_p_below_05": round(float(np.mean(p < 0.05)), 3),
            **{f"P_{k}": round(v.count(k) / len(v), 3) for k in ("CONFIRMED", "MARGINAL", "FALSIFIED", "UNDETERMINED")}}


def h1(rng, sims, draws, out):
    for scale in (2.0, 0.7):
        for r in (1.0, 0.81):
            for target in (0.5, 0.6, 0.65, 0.7, 0.75):
                npm2 = {c: 2 * L[c] for c in CATS}
                beta = 0.0 if target == 0.5 else calibrate(target, scale, r, rng, npm2)
                for sq in (1, 2, 4):
                    npm = {c: sq * L[c] for c in CATS}
                    rows = []
                    for _ in range(sims):
                        m = measured(rng, r)
                        cnt = choose_counts(rng, beta, scale, npm)
                        u, p = perm_p(cnt, {c: pct(m[c]) for c in CATS}, rng, draws)
                        n = sum(cnt[c].sum() for c in CATS)
                        rows.append((u, p, verdict(u, p, n, 450 * sq / 2)))
                    key = f"H1 scale={scale} r={r} target={target} squares={sq} N={3 * sum(npm.values())}"
                    out[key] = {"beta": round(beta, 3), **summarise(rows)}
                    print(key, out[key], flush=True)


def h2(rng, sims, draws, out, other=0.30):
    for scale in (2.0, 0.7):
        for target in (0.5, 0.6, 0.7):
            r = 0.81
            beta = 0.0 if target == 0.5 else calibrate(target, scale, r, rng, {c: 13 for c in CATS})
            rows = []
            for _ in range(sims):
                m = measured(rng, r)
                npm = {c: int(rng.binomial(18, 1 - other)) for c in CATS}
                cnt = choose_counts(rng, beta, scale, npm)
                u, p = perm_p(cnt, {c: pct(m[c]) for c in CATS}, rng, draws)
                n = sum(cnt[c].sum() for c in CATS)
                rows.append((u, p, verdict(u, p, n, 120)))
            key = f"H2 OPEN scale={scale} r={r} target={target} OTHER={other}"
            out[key] = {"beta": round(beta, 3), **summarise(rows)}
            print(key, out[key], flush=True)


def zs(x):
    s = np.std(x)
    return (x - np.mean(x)) / (s if s > 0 else 1.0)


def clogit_beta(nc, xs):
    """Conditional logit on counts: options = rated units; returns (beta_P, beta_R)."""
    def nll(b):
        tot = 0.0
        for c in CATS:
            v = xs[c] @ b
            vmax = v.max()
            tot -= (nc[c] * v).sum() - nc[c].sum() * (vmax + np.log(np.exp(v - vmax).sum()))
        return tot
    return minimize(nll, np.zeros(2), method="BFGS").x


def h34(rng, sims, draws_u, draws_fl, out, scale=2.0, r=0.81):
    npm = {c: 2 * L[c] for c in CATS}
    beta_p = calibrate(0.70, scale, r, rng, npm)
    rated = {c: np.argsort(-Z[c])[:N_RATED[c]] for c in CATS}
    for g in (0.0, 0.15, 0.30, 0.45):          # generating log-odds per SD of R* (times scale), at fixed P
        rows3, rows4, ors = [], [], []
        for _ in range(sims):
            zr_true = {}
            for c in CATS:
                zp = zs(Z[c][rated[c]])
                zr_true[c] = zs(RHO_RP * zp + np.sqrt(1 - RHO_RP ** 2) * rng.normal(0, 1, len(zp)))
            extra = {}
            for c in CATS:
                e = np.zeros(L[c])
                e[rated[c]] = g * zr_true[c]
                extra[c] = e
            cnt = choose_counts(rng, beta_p, scale, npm, extra=extra)
            mp = measured(rng, r)
            ur = {c: pct(r * zr_true[c] + np.sqrt(1 - r * r) * rng.normal(0, 1, N_RATED[c])) for c in CATS}
            nc = {c: cnt[c][rated[c]] for c in CATS}
            # H3: U-bar of R* over choices on rated units
            u3, p3 = perm_p(nc, ur, rng, draws_u)
            n3 = sum(nc[c].sum() for c in CATS)
            rows3.append((u3, p3, verdict(u3, p3, n3, 200)))
            # H4: conditional logit, Freedman-Lane permutation of residualised u_R on u_P
            up = {c: pct(mp[c])[rated[c]] for c in CATS}
            xs = {c: np.column_stack([zs(up[c]), zs(ur[c])]) for c in CATS}
            b_obs = clogit_beta(nc, xs)[1]
            fit, res = {}, {}
            for c in CATS:
                A = np.column_stack([np.ones(N_RATED[c]), up[c]])
                coef = np.linalg.lstsq(A, ur[c], rcond=None)[0]
                fit[c], res[c] = A @ coef, ur[c] - A @ coef
            hits = 0
            for _ in range(draws_fl):
                xp = {c: np.column_stack([zs(up[c]), zs(fit[c] + rng.permutation(res[c]))]) for c in CATS}
                hits += clogit_beta(nc, xp)[1] >= b_obs - 1e-12
            p4 = (1 + hits) / (draws_fl + 1)
            orr = float(np.exp(b_obs))
            ors.append(orr)
            v4 = "UNDETERMINED" if n3 < 200 else ("CONFIRMED" if orr >= 1.25 and p4 < 0.05 else
                                                ("FALSIFIED" if orr < 1.05 else "MARGINAL"))
            rows4.append((orr, p4, v4))
        out[f"H3 Ranking U-bar, g={g}, scale={scale}, r={r}"] = summarise(rows3)
        s4 = summarise(rows4)
        s4["mean_OR_R"] = s4.pop("mean_U")
        s4["sd_OR_R"] = s4.pop("sd_U")
        s4["median_OR_R"] = round(float(np.median(ors)), 3)
        out[f"H4 OR_R beyond P, g={g}, scale={scale}, r={r}"] = s4
        print(f"g={g}", out[f"H3 Ranking U-bar, g={g}, scale={scale}, r={r}"], s4, flush=True)


def latin_orders(rng, n):
    """Rows of a cyclic Latin square of side n, symbols mapped at random, rows shuffled (r1 section 4.2).
    Returns pos[row, unit] = 0-based position of unit in that row's order."""
    sym = rng.permutation(n)
    rows = np.array([[sym[(i + j) % n] for j in range(n)] for i in range(n)])[rng.permutation(n)]
    pos = np.empty_like(rows)
    for i in range(n):
        pos[i, rows[i]] = np.arange(n)
    return pos


def h5_once(rng, beta, gamma, scale, squares, draws):
    d_obs, strata = [], []
    for c in CATS:
        n = L[c]
        shared = rng.normal(0, 1, n)
        for m in range(MODELS):
            base = scale * (beta * Z[c] + shared + rng.normal(0, 0.5, n))
            pos = np.vstack([latin_orders(rng, n) for _ in range(squares)])
            brief = np.arange(len(pos)) % 3
            u = base[None, :] + gamma * (1 - pos / (n - 1))
            p = np.exp(u - u.max(axis=1, keepdims=True))
            p /= p.sum(axis=1, keepdims=True)
            ch = np.array([rng.choice(n, p=row) for row in p])
            for b in range(3):
                idx = np.where(brief == b)[0]
                strata.append((pos[idx] / (n - 1), ch[idx]))
                d_obs.extend(pos[idx, ch[idx]] / (n - 1))
    obs = float(np.mean(d_obs))
    tot = sum(len(ch) for _, ch in strata)
    null = np.zeros(draws)
    for posn, ch in strata:
        k = len(ch)
        perm = np.argsort(rng.random((draws, k)), axis=1)
        null += posn[perm, ch[None, :]].sum(axis=1)
    null /= tot
    centre = null.mean()
    p = (1 + (np.abs(null - centre) >= abs(obs - centre) - 1e-12).sum()) / (draws + 1)
    return obs, p


def h5(rng, sims, draws, out, r=0.81):
    for scale in (2.0, 0.7):
        beta = calibrate(0.70, scale, r, rng, {c: 2 * L[c] for c in CATS})
        # calibrate gamma so that E[d-bar] = 0.45 (two squares)
        lo, hi = 0.0, 4.0
        for _ in range(10):
            mid = (lo + hi) / 2
            dm = np.mean([h5_once(rng, beta, mid, scale, 2, 1)[0] for _ in range(20)])
            lo, hi = (mid, hi) if dm > 0.45 else (lo, mid)
        gam = (lo + hi) / 2
        for g in (0.0, gam):
            for sq in (1, 2):
                res = [h5_once(rng, beta, g, scale, sq, draws) for _ in range(sims)]
                d = np.array([x[0] for x in res])
                pv = np.array([x[1] for x in res])
                key = f"H5 position scale={scale} gamma={g:.3f} squares={sq}"
                out[key] = {"mean_dbar": round(float(d.mean()), 3), "sd_dbar": round(float(d.std()), 3),
                            "P_p_below_05": round(float(np.mean(pv < 0.05)), 3)}
                print(key, out[key], flush=True)


def main():
    sims = int(sys.argv[1]) if len(sys.argv) > 1 else 400
    draws = int(sys.argv[2]) if len(sys.argv) > 2 else 1000
    rng = np.random.default_rng(SEED)
    t0 = time.time()
    out = {"seed": SEED, "sims": sims, "permutation_draws": draws,
           "note": "draws reduced from the pre-registered 10,000 (H1-H3, H5) and 2,000 (H4) for simulation",
           "results": {}}
    h1(rng, sims, draws, out["results"])
    h2(rng, sims, draws, out["results"])
    h34(rng, max(100, sims // 4), draws, 200, out["results"])
    h5(rng, max(100, sims // 2), draws, out["results"])
    out["seconds"] = round(time.time() - t0, 1)
    path = HERE.parent / "prereg" / "power_analysis_v0_46_stage1_r1.json"
    path.write_text(json.dumps(out, indent=1) + "\n")
    path.with_suffix(".txt").write_text("\n".join(f"{k}: {v}" for k, v in out["results"].items()) + "\n")
    print("done", out["seconds"], "s")


if __name__ == "__main__":
    main()
