"""AIAS 6.0 Preview, pre-registration draft r0: synthetic operating characteristics of the
incremental-separability test (I-tests, PRE_REGISTRATION section 6.3). SYNTHETIC DATA ONLY:
no program file is read, no answer, score or verdict of any study is used.

Model: 5 categories; n units split as evenly as possible; k predecessor scores (independent
standard normals); X = sqrt(R2) * (sum of predecessors)/sqrt(k) + sqrt(1 - R2) * noise.
Statistic (as the scorer computes it): centred within-category ranks of every variable;
OLS of X's ranks on the k predecessors' ranks (no intercept: ranks are centred within
category); R2_adj = 1 - (1 - R2)(n - C)/(n - C - k), C = categories entering;
R_adj = sqrt(max(0, R2_adj)).

Usage: python3 -I precision_aias_6_0_preview.py OUT.json   (seed 600900; 4,000 reps per cell)
"""
import json
import sys

import numpy as np
from scipy.stats import rankdata

SEED = 600900
C = 5
REPS = 4000


def centred_ranks(v, cat):
    out = np.empty(len(v))
    for c in np.unique(cat):
        m = cat == c
        out[m] = rankdata(v[m]) - (m.sum() + 1) / 2.0
    return out


def r_adj_once(rng, n, k, r2_true):
    sizes = [n // C + (1 if i < n % C else 0) for i in range(C)]
    cat = np.repeat(np.arange(C), sizes)
    z = rng.standard_normal((n, k))
    s = z.sum(axis=1) / np.sqrt(k)
    x = np.sqrt(r2_true) * s + np.sqrt(1.0 - r2_true) * rng.standard_normal(n)
    y = centred_ranks(x, cat)
    xp = np.column_stack([centred_ranks(z[:, j], cat) for j in range(k)])
    beta, *_ = np.linalg.lstsq(xp, y, rcond=None)
    resid = y - xp @ beta
    r2 = 1.0 - (resid @ resid) / (y @ y)
    r2a = 1.0 - (1.0 - r2) * (n - C) / (n - C - k)
    return float(np.sqrt(max(0.0, r2a)))


def main(out_path):
    rng = np.random.default_rng(SEED)
    rows = []
    for n in (30, 40, 55, 70):
        for k in (1, 2, 3, 4, 5):
            for r2 in (0.0, 0.04, 0.09, 0.25, 0.49):
                v = np.array([r_adj_once(rng, n, k, r2) for _ in range(REPS)])
                rows.append({
                    "n": n, "k_predecessors": k, "true_R2": r2,
                    "P_CONFIRMED_bands_030_050": float((v <= 0.30).mean()),
                    "P_FALSIFIED_bands_030_050": float((v >= 0.50).mean()),
                    "P_CONFIRMED_bands_050_070": float((v <= 0.50).mean()),
                    "P_FALSIFIED_bands_050_070": float((v >= 0.70).mean()),
                    "median_R_adj": float(np.median(v)),
                })
    json.dump({"what": "synthetic operating characteristics of the I-test (no program data)",
               "seed": SEED, "reps_per_cell": REPS, "categories": C, "rows": rows},
              open(out_path, "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1])
