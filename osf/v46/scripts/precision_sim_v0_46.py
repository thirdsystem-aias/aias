#!/usr/bin/env python3
"""Precision simulation for v0.46 (DRAFT r0), section 6. No model is called; synthetic choices only.

Units: the four categories' t4 recall values pi_N3_S0 (v42_brand_table.csv at v0.42-scoring-locked; cars without
v0.22's Cell D units), in registry order. Each of three models chooses by a multinomial logit on
scale * (beta * z(pi) + shared brand appeal (SD sigma) + model-specific appeal (SD sigma/2)).
Statistic: U = mean within-category percentile of the chosen unit; null: pi permuted within category.
Draft r0 ran it in the runner's scratch space (numpy, scipy) with seeds 76 (main table) and 761 (squares check).
Usage: python3 precision_sim_v0_46.py [n_studies] [n_draws]
"""
import sys
import numpy as np
from scipy.stats import rankdata

PI = {
    "skincare": [0.22, 0.09, 1.00, 0.44, 0.00, 0.00, 0.00, 0.52, 0.00, 0.22, 0.17, 0.11, 0.06, 0.17, 0.02, 0.91,
                 0.00, 0.31, 0.00, 0.50, 0.00, 0.69, 0.78, 0.04],
    "cosmetics": [0.04, 0.19, 0.00, 0.91, 0.00, 0.67, 0.24, 0.28, 0.13, 0.30, 0.02, 0.09, 0.19, 0.48, 0.78, 0.00,
                  0.72, 0.46, 0.54, 0.67, 0.00, 0.00, 0.00, 0.65],
    "cars": [0.74, 0.33, 0.37, 0.24, 0.00, 0.41, 0.54, 0.44, 0.15, 0.09, 0.65, 0.94, 0.07, 0.48, 0.28, 0.67, 0.20,
             0.00, 0.00],
    "spirits": [0.17, 0.43, 0.19, 0.20, 0.17, 0.07, 0.00, 0.02, 0.19, 0.07, 0.11, 0.00, 0.30, 0.13, 0.39, 0.24, 0.52,
                0.02, 0.24, 0.52, 0.19, 0.44, 0.04, 0.15],
}
CATS = list(PI)
U = {c: (rankdata(PI[c]) - 0.5) / len(PI[c]) for c in CATS}
Z = {c: (np.asarray(PI[c]) - np.mean(PI[c])) / np.std(PI[c]) for c in CATS}
SCENARIOS = [(0, 2, "no link, concentrated"), (0, 0.7, "no link, diffuse"), (0.5, 2, "weak link"),
             (1, 2, "moderate link"), (2, 2, "strong link"), (1, 0.7, "moderate link, diffuse")]


def simulate(beta, scale, rng, squares=2, sigma=1.0, models=3):
    counts = {}
    for c in CATS:
        L = len(PI[c])
        tot, shared = np.zeros(L), rng.normal(0, sigma, L)
        for _ in range(models):
            u = scale * (beta * Z[c] + shared + rng.normal(0, sigma * 0.5, L))
            p = np.exp(u - u.max())
            tot += rng.multinomial(squares * L, p / p.sum())
        counts[c] = tot
    return counts


def ubar(counts, uu):
    return sum((counts[c] * uu[c]).sum() for c in CATS) / sum(counts[c].sum() for c in CATS)


def test(counts, rng, draws):
    obs = ubar(counts, U)
    null = np.array([ubar(counts, {c: rng.permutation(U[c]) for c in CATS}) for _ in range(draws)])
    top3 = np.mean([np.sort(counts[c])[::-1][:3].sum() / counts[c].sum() for c in CATS])
    return obs, (1 + (null >= obs - 1e-12).sum()) / (draws + 1), top3


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    draws = int(sys.argv[2]) if len(sys.argv) > 2 else 1000
    rng = np.random.default_rng(76)
    for beta, scale, label in SCENARIOS:
        res = [test(simulate(beta, scale, rng), rng, draws) for _ in range(n)]
        obs, p = np.array([r[0] for r in res]), np.array([r[1] for r in res])
        conf, fals = np.mean((obs >= 0.70) & (p < 0.05)), np.mean(obs < 0.60)
        print(f"{label:24s} meanU {obs.mean():.3f} sd {obs.std():.3f} top3 {np.mean([r[2] for r in res]):.2f} "
              f"P(p<.05) {np.mean(p < .05):.2f} P(CONF) {conf:.2f} P(FALS) {fals:.2f}")


if __name__ == "__main__":
    main()
