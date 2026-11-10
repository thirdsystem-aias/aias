"""AIAS v0.44 (pre-registration r1, change C2): why rho_pw centres ranks within industry. No model is called.

On the 156 non-ghost H_Tier units (x = tier score), y drawn independently of x: the uncentred pooled-within statistic
(score_v41.pooled_within_rho: within-industry ranks, pooled Pearson) has a positive null mean because the eight
industries differ in size, so their mean ranks (n_i + 1) / 2 differ for x and y alike; the centred statistic
(score_v0_44.rho_pw) has null mean ~0. Also shown: the gap when y follows tier with noise.
Run: python3 osf/v44/scripts/rho_pw_check_v0_44.py  -> prints; seed 1; stdlib + numpy + scipy only.
"""
import csv
import os

import numpy as np
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
REG = os.path.normpath(os.path.join(HERE, "..", "registries"))


def units():
    inds = list(csv.DictReader(open(os.path.join(REG, "industries_v0_44.csv"), encoding="utf-8")))
    out = []
    for i in inds:
        with open(os.path.join(REG, os.path.basename(i["file"])), encoding="utf-8") as f:
            for r in csv.DictReader(f):
                if r["tier"] != "G":
                    out.append((r["industry"], {"L": 3, "C": 2, "S": 1}[r["tier"]]))
    return out


def within_ranks(v, g):
    out = np.empty(len(v))
    for k in dict.fromkeys(g):
        i = np.where(g == k)[0]
        out[i] = stats.rankdata(v[i])
    return out


def pearson(a, b):
    a, b = a - a.mean(), b - b.mean()
    return float((a * b).sum() / np.sqrt((a * a).sum() * (b * b).sum()))


def uncentred(x, y, g):
    return pearson(within_ranks(x, g), within_ranks(y, g))


def centred(x, y, g):
    rx, ry = within_ranks(x, g), within_ranks(y, g)
    for k in dict.fromkeys(g):
        i = g == k
        rx[i] -= rx[i].mean()
        ry[i] -= ry[i].mean()
    return pearson(rx, ry)


def main(n=4000, seed=1):
    u = units()
    g = np.array([a for a, _ in u])
    x = np.array([b for _, b in u], float)
    rng = np.random.default_rng(seed)
    print("units", len(u), {k: int((g == k).sum()) for k in dict.fromkeys(g)})
    nu = [uncentred(x, rng.random(len(x)), g) for _ in range(n)]
    nc = [centred(x, rng.random(len(x)), g) for _ in range(n)]
    print("null, y independent of tier (%d draws): uncentred mean %.4f (sd %.4f); centred mean %.4f (sd %.4f)"
          % (n, np.mean(nu), np.std(nu), np.mean(nc), np.std(nc)))
    for s in (0.5, 1.0, 2.0):
        du, dc = [], []
        for _ in range(n // 2):
            y = x + rng.normal(0, s, len(x))
            du.append(uncentred(x, y, g))
            dc.append(centred(x, y, g))
        print("y = tier + N(0, %.1f): uncentred %.4f, centred %.4f, difference %.4f"
              % (s, np.mean(du), np.mean(dc), np.mean(du) - np.mean(dc)))


if __name__ == "__main__":
    main()
