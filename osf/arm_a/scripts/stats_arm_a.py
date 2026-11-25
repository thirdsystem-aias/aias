"""Arm A statistics (pre-registration r4, sections 2.1-2.10, 6.7). numpy only; every function is unit-tested."""
import math

import numpy as np


def rankdata(x):
    """Ranks 1..n, ties at the average rank."""
    x = np.asarray(x, dtype=float)
    order = np.argsort(x, kind="mergesort")
    ranks = np.empty(len(x), dtype=float)
    xs = x[order]
    i = 0
    while i < len(x):
        j = i
        while j + 1 < len(x) and xs[j + 1] == xs[i]:
            j += 1
        ranks[order[i:j + 1]] = (i + j) / 2.0 + 1.0
        i = j + 1
    return ranks


def pearson(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    xc, yc = x - x.mean(), y - y.mean()
    d = math.sqrt(float((xc * xc).sum() * (yc * yc).sum()))
    return float((xc * yc).sum() / d) if d > 0 else float("nan")


def spearman(x, y):
    return pearson(rankdata(x), rankdata(y))


def weighted_pearson(x, y, w):
    x, y, w = (np.asarray(v, float) for v in (x, y, w))
    w = w / w.sum()
    mx, my = (w * x).sum(), (w * y).sum()
    cov = (w * (x - mx) * (y - my)).sum()
    d = math.sqrt(float((w * (x - mx) ** 2).sum() * (w * (y - my) ** 2).sum()))
    return float(cov / d) if d > 0 else float("nan")


def weighted_spearman(x, y, w):
    return weighted_pearson(rankdata(x), rankdata(y), w)


def residuals(y, X):
    """Least-squares residuals and fitted values of y on design matrix X (columns include the intercept)."""
    y = np.asarray(y, float)
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    fit = X @ beta
    return y - fit, fit


def design(z, groups=None, per_group=False):
    z = np.asarray(z, float)
    if not per_group:
        return np.column_stack([np.ones(len(z)), z])
    gs = sorted(set(groups))
    cols = []
    for g in gs:
        ind = np.array([1.0 if gg == g else 0.0 for gg in groups])
        cols += [ind, ind * z]
    return np.column_stack(cols)


def partial_corr(x, y, z):
    """Pearson correlation of x and y after removing a linear effect of z (intercept + slope) from each."""
    X = design(z)
    ex, _ = residuals(x, X)
    ey, _ = residuals(y, X)
    return pearson(ex, ey)


def fisher_pool(rhos, ns):
    """Fisher-z mean weighted by n - 3, back-transformed."""
    z = [math.atanh(max(min(r, 0.999999), -0.999999)) for r in rhos]
    w = [n - 3 for n in ns]
    return math.tanh(sum(a * b for a, b in zip(z, w)) / sum(w))


def perm_p(observed, null, tail="greater"):
    null = np.asarray([v for v in null if not math.isnan(v)])
    n = len(null)
    if tail == "greater":
        k = int((null >= observed - 1e-12).sum())
    else:
        k = int((null <= observed + 1e-12).sum())
    return (1 + k) / (1 + n)


def holm(pvals):
    """Holm step-down adjusted p-values, same order as the input; None entries stay None."""
    idx = [i for i, p in enumerate(pvals) if p is not None]
    order = sorted(idx, key=lambda i: pvals[i])
    m = len(order)
    adj, running = [None] * len(pvals), 0.0
    for k, i in enumerate(order):
        running = max(running, min(1.0, (m - k) * pvals[i]))
        adj[i] = running
    return adj


def percentile_ci(vals, level=0.95):
    v = np.sort(np.asarray([x for x in vals if not math.isnan(x)]))
    if len(v) == 0:
        return (float("nan"), float("nan"))
    lo, hi = (1 - level) / 2, 1 - (1 - level) / 2
    return (float(np.quantile(v, lo)), float(np.quantile(v, hi)))


def jonckheere(values_by_band):
    """Jonckheere-Terpstra J for the ordered alternative band 0 < band 1 < ... (ties count one half)."""
    J = 0.0
    for i in range(len(values_by_band)):
        for j in range(i + 1, len(values_by_band)):
            for a in values_by_band[i]:
                for b in values_by_band[j]:
                    J += 1.0 if b > a else (0.5 if b == a else 0.0)
    return J


def within_group_permutation(rng, groups):
    """Index permutation that shuffles positions only within each group."""
    groups = list(groups)
    idx = np.arange(len(groups))
    out = idx.copy()
    for g in set(groups):
        pos = idx[[gg == g for gg in groups]]
        out[pos] = rng.permutation(pos)
    return out


def norm_ranks_within(values, groups):
    """(rank - 1) / (n_g - 1) within each group, ties at the average rank."""
    values, out = np.asarray(values, float), np.zeros(len(values))
    for g in set(groups):
        pos = [i for i, gg in enumerate(groups) if gg == g]
        r = rankdata(values[pos])
        out[pos] = (r - 1) / (len(pos) - 1) if len(pos) > 1 else 0.0
    return out


def centre_within(values, groups):
    values, out = np.asarray(values, float), np.zeros(len(values))
    for g in set(groups):
        pos = [i for i, gg in enumerate(groups) if gg == g]
        out[pos] = values[pos] - values[pos].mean()
    return out
