#!/usr/bin/env python3
"""
score_v1_12.py -- AIAS(TM) v1.12 Coverage Paper A: scorer CORE (pre-registration draft r1).

Transcribes PRE_REGISTRATION_v1_12.md section 2.3 (model coverage, raw Cov, pi_cov), 2.4 (beta, Cov*,
rating floors, the exact Rasch-type null of r1 and the equal-weight null of S3), 2.5 (rho_w,
permutation p, bootstrap, n floor), 3 (verdict and gate rules) and 4 (MC_Situation), and runs calibration
N1 (section 2.4). THE PRE-REGISTRATION PROSE IS AUTHORITATIVE; where it is silent the simplest faithful
option is taken and listed in SCORER_NOTES.

Not in this core (written before the lock and added to the lock manifest): reading the v1.12 raw record and
coding it with v0.42's coder, the comparators P_N3, C*_N3 and pi_N3 from v0.42's locked outputs, parity
gates P1-P3, the other section 4 checks, the section 5 descriptives, the section 7.4 sensitivities and a
--run mode. Nothing here reads v1.12 or t4 answers, and nothing here calls any API.

SCORER_NOTES (choices where the pre-registration is silent)
 N1  Input unit: one answered CEP call = (substrate, model, CEP probe ID, run, set of registry brands named).
     A missing call is absent (it enters no denominator). One answer per (substrate, model, probe, run).
 N2  Null (r1): situation-blind Rasch-type model per panel model and category: logit P(y_b,s = 1) =
     theta_b + delta_j(s), no brand x CEP interaction. delta^(-b) = the joint maximum-likelihood fit (brand
     fixed effects and CEP effects on the binomial counts brand x CEP) on the OTHER registry brands of b's
     category in that model's answered CEP calls; brands named in none or all of the slots are left out;
     deterministic Newton steps with step halving, started from the fit on all informative brands; delta
     centred to sum to zero over the answered CEPs. A fit that does not converge within 100 steps, whose
     parameters pass |25|, or that has no informative brand: delta = 0 for that (b, m), counted. Given n,
     the named slots follow the conditional Bernoulli law P(Y) ~ prod_s exp(delta_j(s))^y_s; the exact null
     pmf of C is the x^n coefficient of prod_j [1 + z((1 + e^delta_j x)^s_j - 1)], normalised over z.
     No random draws: seed 112100 is no longer used by Cov*. S3 = equal weights (delta = 0).
 N3  c_max = min(n, number of CEPs with >= 1 answered run); c_min = the fewest CEPs that can hold n mentions,
     filling CEPs with the most answered runs first. r1: beta = (c - E) / (c_max - c_min) if c_max > c_min,
     else 0 (one linear normalisation: its null mean is 0 at every n).
 N4  Rating floor: n_b over the panel's models >= floor (14; 7 per half) and >= 2 panel models with n >= 1.
 N5  rho_w (r1): within-category average ranks centred on the category mean rank, r - (m_c + 1) / 2, then
     Pearson over all units pooled. S9 = the uncentred v0.37-v0.41 convention: _pearson, within_ranks and
     pooled_within_rho transcribed from osf/v41/scripts/score_v41.py (a unit test checks equality with that
     file). Categories with fewer than 5 units in the comparison are dropped before ranking. n floor:
     UNDETERMINED if pooled n < 30 or fewer than 3 categories retained.
 N6  Permutation: the within-category ranks of y are permuted within category (identical to re-ranking a
     within-category permutation of y); two-sided hit if |rho_perm| >= |rho_obs| - 1e-12, one-sided hit if
     rho_perm >= rho_obs - 1e-12; p = (1 + hits) / (draws + 1); seed = the hypothesis seed (112001-112008).
 N7  Bootstrap: units resampled with replacement within category (retained categories), ranks recomputed
     on each resample, percentile 95% interval; seed 112020, a fresh generator per test; non-finite
     resamples are dropped and counted.
 N8  H4: p is computed on r (rel = 2r / (1 + r) is monotone in r).
 N9  MC_Situation on the answered calls of the named panel (N3 for the gate). Per (model, run, category):
     J_between = mean Jaccard over pairs of different CEPs answered in that run; J_within = mean over that
     run's CEP answers of the Jaccard with the same CEP's other answered runs (same model). Pairs whose union
     is empty (neither answer names a registry brand) are skipped and counted. Pooled = mean over the
     (model, run, category) cells where both are defined. The C0 Jaccard is reported, not gated.
 N10 Gate: a two-model panel (drop rule, section 7.3) caps PASS at MARGINAL; inactive H5/H6 are ignored.
 N11 Calibration N1 (restated in r1): design and rule in calibrate_n1's docstring.
 N12 S8 mid-p variant: beta_mid = 2 [P0(C < c) + 0.5 P0(C = c)] - 1, P0 = the null distribution of C given n
     from the same Monte Carlo draws (weighted) or exact (equal weights: P(C = k) = [x^n y^k]
     prod_j (1 + y((1 + x)^s_j - 1)) / C(S, n)). Cov*_mid = 50 (1 + mean beta_mid), same floors.

Modes:  --calibrate-n1   run N1 exactly as section 2.4 states; writes prereg/calibration_N1_v1_12.json
"""
import argparse
import collections
import functools
import hashlib
import itertools
import json
import math
import platform
import sys
import time
from pathlib import Path

import numpy as np
from scipy import stats

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]                       # <repo>/osf/methodology/v1_12/scripts -> <repo>
N1_PATH = ROOT / "osf/methodology/v1_12/prereg/calibration_N1_v1_12.json"

PHASE_ID = "v1.12"
CATS = ["v0.19", "v0.20", "v0.21", "v0.22", "v0.23"]
W_TYPES = ["why", "when", "where", "while", "with whom", "with what", "how feeling"]
RUNS = (1, 2, 3)
FLOOR_FULL, FLOOR_HALF, MIN_MODELS_NAMED = 14, 7, 2          # section 2.4; H4
FLOOR_SENS = (6, 28)                                          # S2
RASCH_MAX_ITER, RASCH_TOL, RASCH_BOUND = 100, 1e-9, 25.0       # SCORER_NOTES N2
SEED_N1, SEED_BOOT = 112200, 112020                           # section 2.5 (112100 no longer used, N2)
SEEDS = {"H1_Sep_Presence": 112001, "H2_Sep_Consistency": 112002, "H3_Sep_NamingRate": 112003,
         "H4_Reliability": 112004, "H5_Sep_Ranking": 112005, "H6_Sep_Sentiment": 112006,
         "H7_Sep_Presence_Legacy": 112007, "H8_Panel_Replication": 112008}
N_PERM, N_BOOT = 10_000, 10_000
SEP_CONF, SEP_FALS = 0.30, 0.50                               # section 3 bands
REL_CONF, REL_FALS, ALPHA = 0.50, 0.30, 0.05                  # H4
REP_CONF, REP_FALS = 0.70, 0.50                               # H8
N_FLOOR_UNITS, N_FLOOR_CATS, MIN_UNITS_PER_CAT = 30, 3, 5     # section 2.5
MCS_DIFF_MIN, MCS_JB_MAX = 0.10, 0.60                         # MC_Situation
N1_RULE_RHO, N1_RULE_DECILE = 0.05, 2.5                       # calibration N1 (r1)
TOL = 1e-12
NAN = float("nan")

FABLE, OPUS55, GPT6, GEM4 = "claude-fable-5-2", "claude-opus-5-5", "gpt-6-astra", "gemini-4-argon"
PANELS = {"N3": [FABLE, GPT6, GEM4], "C3": [OPUS55, GPT6, GEM4], "A4": [FABLE, OPUS55, GPT6, GEM4]}
PRIMARY_LEGS = ["H1_Sep_Presence", "H2_Sep_Consistency", "H3_Sep_NamingRate", "H4_Reliability"]
CONDITIONAL_LEGS = ["H5_Sep_Ranking", "H6_Sep_Sentiment"]
VERDICTS = {"CONFIRMED", "MARGINAL", "FALSIFIED", "UNDETERMINED", "INACTIVE"}


def _finite(v):
    return v is not None and isinstance(v, (int, float, np.floating, np.integer)) and math.isfinite(float(v))


# =========================================================================== rho_w (v0.41 convention)
# _pearson, within_ranks, pooled_within_rho and _group_index: transcribed from osf/v41/scripts/score_v41.py.
def _pearson(a, b):
    a = np.asarray(a, float) - np.mean(a)
    b = np.asarray(b, float) - np.mean(b)
    d = np.sqrt((a * a).sum() * (b * b).sum())
    return float((a * b).sum() / d) if d > 0 else float("nan")


def within_ranks(values, groups):
    """Average ranks computed WITHIN each group (v0.37 convention)."""
    values = np.asarray(values, float)
    groups = np.asarray(groups)
    out = np.empty(len(values))
    for g in dict.fromkeys(groups):
        idx = np.where(groups == g)[0]
        out[idx] = stats.rankdata(values[idx])
    return out


def pooled_within_rho(x, y, groups):
    if len(x) < 3:
        return float("nan")
    return _pearson(within_ranks(x, groups), within_ranks(y, groups))


def _group_index(groups):
    groups = np.asarray(groups)
    return [np.where(groups == g)[0] for g in dict.fromkeys(groups)]


def centred_within_ranks(values, groups):
    """r1: within-category average ranks centred on the category mean rank, r - (m_c + 1) / 2."""
    groups = np.asarray(groups)
    r = within_ranks(values, groups)
    for g in dict.fromkeys(groups):
        idx = np.where(groups == g)[0]
        r[idx] -= (len(idx) + 1) / 2.0
    return r


def rho_w(x, y, groups, centred=True):
    """Section 2.5 rho_w: centred within-category ranks, Pearson pooled (r1 primary). centred=False: the
    uncentred v0.37-v0.41 convention (sensitivity S9; equals score_v41.pooled_within_rho)."""
    if not centred:
        return pooled_within_rho(x, y, groups)
    if len(x) < 3:
        return float("nan")
    return _pearson(centred_within_ranks(x, groups), centred_within_ranks(y, groups))


def paired(xd, yd, min_per_cat=MIN_UNITS_PER_CAT):
    """Units (substrate, brand) with both values finite; categories with fewer than `min_per_cat` such units
    are dropped (section 2.5). Returns keys, x, y, groups, info."""
    keys = sorted(k for k in xd if k in yd and _finite(xd[k]) and _finite(yd[k]))
    per = collections.Counter(k[0] for k in keys)
    keep = {c for c, n in per.items() if n >= min_per_cat}
    keys = [k for k in keys if k[0] in keep]
    x = np.array([float(xd[k]) for k in keys], float)
    y = np.array([float(yd[k]) for k in keys], float)
    g = np.array([k[0] for k in keys])
    info = {"n": len(keys), "n_categories": len(keep),
            "per_category": {c: per[c] for c in sorted(keep)},
            "dropped_categories": {c: n for c, n in sorted(per.items()) if c not in keep}}
    return keys, x, y, g, info


def below_n_floor(info):
    return info["n"] < N_FLOOR_UNITS or info["n_categories"] < N_FLOOR_CATS


def perm_p(x, y, g, obs, seed, sided, n_draws=N_PERM, centred=True):
    """Permutation p for rho_w: y permuted within category (section 2.5); see SCORER_NOTES N6."""
    if sided not in ("one", "two"):
        raise ValueError(sided)
    if not _finite(obs):
        return NAN
    rng = np.random.default_rng(seed)
    rk = centred_within_ranks if centred else within_ranks
    rx, ry = rk(x, g), rk(y, g)
    gidx = _group_index(g)
    idx = np.arange(len(y))
    hits = 0
    for _ in range(n_draws):
        for gi in gidx:
            idx[gi] = rng.permutation(gi)
        r = _pearson(rx, ry[idx])
        hits += bool(abs(r) >= abs(obs) - TOL) if sided == "two" else bool(r >= obs - TOL)
    return (1 + hits) / (n_draws + 1)


def bootstrap(g, seed, n_boot, fn):
    """Units resampled with replacement within category; fn(idx) -> {name: value}; percentile 95% per name."""
    rng = np.random.default_rng(seed)
    gidx = _group_index(g)
    store, dropped, names = collections.defaultdict(list), collections.Counter(), None
    for _ in range(n_boot):
        idx = np.concatenate([rng.choice(gi, size=len(gi), replace=True) for gi in gidx])
        res = fn(idx)
        names = names or list(res)
        for k, v in res.items():
            if _finite(v):
                store[k].append(v)
            else:
                dropped[k] += 1
    out = {}
    for k in names or []:
        ci = [float(q) for q in np.percentile(store[k], [2.5, 97.5])] if store[k] else None
        out[k] = {"ci95": ci, "n_draws": len(store[k]), "dropped_nonfinite": int(dropped[k])}
    return out


def rho_test(xd, yd, seed, sided, n_perm=N_PERM, n_boot=N_BOOT, transform=None, centred=True):
    """rho_w(x, y) with the n floor, permutation p (hypothesis seed) and bootstrap interval (seed 112020).
    transform: optional f(rho) reported with its own interval (H4: rel = 2r / (1 + r))."""
    keys, x, y, g, info = paired(xd, yd)
    out = dict(info, sided=sided, seed=seed, below_n_floor=below_n_floor(info))
    rho = rho_w(x, y, g, centred) if info["n"] >= 3 else NAN
    out["rho_w"] = rho
    out["centred"] = centred
    if transform is not None:
        out["transformed"] = transform(rho) if _finite(rho) else NAN
    if info["n"] < 3 or not _finite(rho):
        out["p_perm"] = NAN
        return out
    out["p_perm"] = perm_p(x, y, g, rho, seed, sided, n_perm, centred)
    out["n_perm"] = n_perm

    def fn(i):
        r = rho_w(x[i], y[i], g[i], centred)
        res = {"rho_w": r}
        if transform is not None:
            res["transformed"] = transform(r) if _finite(r) else NAN
        return res
    b = bootstrap(g, SEED_BOOT, n_boot, fn)
    out["ci95_rho_w"] = b["rho_w"]["ci95"]
    if transform is not None:
        out["ci95_transformed"] = b["transformed"]["ci95"]
    out["bootstrap"] = {k: {kk: vv for kk, vv in v.items() if kk != "ci95"} for k, v in b.items()}
    out["n_boot"] = n_boot
    return out


def spearman_brown_half(r):
    """rel = 2r / (1 + r) (H4)."""
    return 2 * r / (1 + r) if _finite(r) and r > -1 else NAN


# =========================================================================== verdicts (section 3)
def verdict_separability(t):
    """CONFIRMED iff |rho_w| <= 0.30; FALSIFIED iff |rho_w| >= 0.50; MARGINAL otherwise;
    UNDETERMINED below the n floor (or rho not finite)."""
    rho = t.get("rho_w", NAN)
    if t.get("below_n_floor", True) or not _finite(rho):
        return "UNDETERMINED"
    a = abs(rho)
    if a <= SEP_CONF:
        return "CONFIRMED"
    if a >= SEP_FALS:
        return "FALSIFIED"
    return "MARGINAL"


def verdict_reliability(t):
    """H4: rel = 2r / (1 + r). CONFIRMED iff rel >= 0.50 and one-sided p < 0.05; FALSIFIED iff rel < 0.30
    or p >= 0.05; MARGINAL otherwise; UNDETERMINED below the n floor."""
    r, p = t.get("rho_w", NAN), t.get("p_perm", NAN)
    if t.get("below_n_floor", True) or not _finite(r) or not _finite(p):
        return "UNDETERMINED"
    rel = spearman_brown_half(r)
    if not _finite(rel):
        return "UNDETERMINED"
    if rel >= REL_CONF and p < ALPHA:
        return "CONFIRMED"
    if rel < REL_FALS or p >= ALPHA:
        return "FALSIFIED"
    return "MARGINAL"


def verdict_replication(t):
    """H8: CONFIRMED iff rho >= 0.70 and one-sided p < 0.05; FALSIFIED iff rho < 0.50; MARGINAL otherwise."""
    rho, p = t.get("rho_w", NAN), t.get("p_perm", NAN)
    if t.get("below_n_floor", True) or not _finite(rho) or not _finite(p):
        return "UNDETERMINED"
    if rho >= REP_CONF and p < ALPHA:
        return "CONFIRMED"
    if rho < REP_FALS:
        return "FALSIFIED"
    return "MARGINAL"


def gate(mc_situation_pass, verdicts, active=None, h6_cross_panel=False, two_model=False):
    """Paper A verdict (section 3, GATE; section 7.3 two-model cap).
    verdicts: {tag: verdict} for H1-H8; active: {"H5_Sep_Ranking": bool, "H6_Sep_Sentiment": bool}."""
    active = active or {}
    for k, v in verdicts.items():
        if v not in VERDICTS:
            raise ValueError(f"{k}: unknown verdict {v!r}")
    legs = PRIMARY_LEGS + [h for h in CONDITIONAL_LEGS if active.get(h)]
    leg_v = {h: verdicts.get(h, "UNDETERMINED") for h in legs}
    for h in legs:
        if leg_v[h] == "INACTIVE":
            raise ValueError(f"{h} is declared active but its verdict is INACTIVE")
    notes = []
    if not mc_situation_pass:
        verdict = "INSTRUMENT FAIL"
        notes.append("MC_Situation failed: reported as a negative result; H1-H8 still computed for the record")
    elif any(v == "FALSIFIED" for v in leg_v.values()):
        verdict = "FAIL"
    elif any(v == "UNDETERMINED" for v in leg_v.values()):
        verdict = "UNDETERMINED"
    elif all(v == "CONFIRMED" for v in leg_v.values()):
        verdict = "PASS"
        if verdicts.get("H7_Sep_Presence_Legacy") == "FALSIFIED":
            verdict = "MARGINAL"
            notes.append("PASS downgraded to MARGINAL: H7_Sep_Presence_Legacy FALSIFIED")
    else:
        verdict = "MARGINAL"
    if two_model and verdict == "PASS":
        verdict = "MARGINAL"
        notes.append("two-model panel (section 7.3): gate at most MARGINAL")
    label = verdict
    if h6_cross_panel and leg_v.get("H6_Sep_Sentiment") == "CONFIRMED":
        label += " (H6 CONFIRMED cross-panel)"
    if verdict == "MARGINAL":
        notes.append("Paper B only on Pablo's recorded decision, the marginal leg as its first confirmatory test")
    return {"verdict": verdict, "label": label, "legs": leg_v,
            "inactive": [h for h in CONDITIONAL_LEGS if not active.get(h)], "notes": notes}


# =========================================================================== MC_Situation (section 4)
def jaccard(a, b):
    u = set(a) | set(b)
    if not u:
        return None
    return len(set(a) & set(b)) / len(u)


def mc_situation(cep_sets, control_sets, models):
    """cep_sets: {(substrate, model, cep_id, run): set of registry brands named} (answered CEP calls);
    control_sets: {(substrate, model, run): set} (answered C0 calls). SCORER_NOTES N9."""
    models = set(models)
    by_cell = collections.defaultdict(dict)            # (sub, model, run) -> {cep: set}
    by_cep = collections.defaultdict(dict)             # (sub, model, cep) -> {run: set}
    for (sub, m, cep, r), s in cep_sets.items():
        if m in models:
            by_cell[(sub, m, r)][cep] = s
            by_cep[(sub, m, cep)][r] = s
    cells, skipped_empty, c0_vals = [], 0, []
    for (sub, m, r) in sorted(by_cell):
        answers = by_cell[(sub, m, r)]
        ceps = sorted(answers)
        jb = []
        for a, b in itertools.combinations(ceps, 2):
            v = jaccard(answers[a], answers[b])
            if v is None:
                skipped_empty += 1
            else:
                jb.append(v)
        jw = []
        for cep in ceps:
            for r2, s2 in sorted(by_cep[(sub, m, cep)].items()):
                if r2 == r:
                    continue
                v = jaccard(answers[cep], s2)
                if v is None:
                    skipped_empty += 1
                else:
                    jw.append(v)
        c0 = control_sets.get((sub, m, r))
        c0j = []
        if c0 is not None:
            for cep in ceps:
                v = jaccard(answers[cep], c0)
                if v is not None:
                    c0j.append(v)
        c0_vals += c0j
        cells.append({"substrate": sub, "model": m, "run": r, "n_ceps": len(ceps),
                      "J_between": float(np.mean(jb)) if jb else None,
                      "J_within": float(np.mean(jw)) if jw else None,
                      "J_with_C0": float(np.mean(c0j)) if c0j else None})
    both = [c for c in cells if c["J_between"] is not None and c["J_within"] is not None]
    diff = float(np.mean([c["J_within"] - c["J_between"] for c in both])) if both else NAN
    jbm = float(np.mean([c["J_between"] for c in both])) if both else NAN
    passed = bool(_finite(diff) and _finite(jbm) and diff >= MCS_DIFF_MIN and jbm <= MCS_JB_MAX)
    return {"passed": passed, "pooled_mean_J_within_minus_J_between": diff, "pooled_mean_J_between": jbm,
            "pooled_mean_J_within": float(np.mean([c["J_within"] for c in both])) if both else NAN,
            "mean_J_with_C0": float(np.mean(c0_vals)) if c0_vals else NAN,
            "cells_used": len(both), "cells": cells, "pairs_skipped_empty_union": skipped_empty,
            "rule": f"pass iff pooled mean (J_within - J_between) >= {MCS_DIFF_MIN} and pooled mean J_between <= {MCS_JB_MAX}"}


# =========================================================================== Coverage core (sections 2.3-2.4)
def c_max_of(s_counts, n):
    """c_max = min(n, number of CEPs with >= 1 answered run) (normally min(14, n))."""
    return int(min(int(n), int(np.count_nonzero(np.asarray(s_counts)))))


def c_min_of(s_counts, n):
    """The fewest CEPs that can hold n mentions, filling CEPs with the most answered runs first."""
    if n <= 0:
        return 0
    cs = np.cumsum(np.sort(np.asarray(s_counts, int))[::-1])
    if n > cs[-1]:
        raise ValueError("n exceeds the answered slots")
    return int(np.searchsorted(cs, n, side="left") + 1)


def e_equal(s_counts, n):
    """S3 equal-weight null: E = sum_j [1 - C(S - s_j, n) / C(S, n)] (exact integers)."""
    s_counts = [int(s) for s in s_counts]
    S = sum(s_counts)
    if n <= 0:
        return 0.0
    tot = math.comb(S, n)
    return float(sum(1 - math.comb(S - s, n) / tot for s in s_counts if s > 0))


def beta_of(c, E, cmax, cmin):
    """r1: beta = (c - E) / (c_max - c_min) if c_max > c_min, else 0. One linear normalisation, so its null
    mean is (E0[c] - E) / (c_max - c_min) = 0 at every n."""
    if cmax <= cmin:
        return 0.0
    return float((c - E) / (cmax - cmin))


def null_pmf_equal(s_counts, n):
    """Exact equal-weight null distribution of C (CEPs touched) given n (SCORER_NOTES N12): {k: P(C = k)}."""
    return dict(_null_pmf_equal(tuple(int(s) for s in s_counts if s > 0), int(n)))


@functools.lru_cache(maxsize=None)
def _null_pmf_equal(s_counts, n):
    S = sum(s_counts)
    poly = [[1] + [0] * S]
    for s in s_counts:
        g = [0] + [math.comb(s, i) for i in range(1, s + 1)]          # (1 + x)^s - 1
        new = [[0] * (S + 1) for _ in range(len(poly) + 1)]
        for k, row in enumerate(poly):
            for i, a in enumerate(row):
                if a:
                    new[k][i] += a
                    for j, gc in enumerate(g):
                        if gc and i + j <= S:
                            new[k + 1][i + j] += a * gc
        poly = new
    tot = math.comb(S, n)
    return tuple((k, poly[k][n] / tot) for k in range(len(poly)) if poly[k][n])


def beta_mid(c, null_counts=None, null_pmf=None):
    """S8: beta_mid = 2 [P0(C < c) + 0.5 P0(C = c)] - 1 from Monte Carlo null counts or an exact pmf."""
    if null_pmf is not None:
        lt = sum(p for k, p in null_pmf.items() if k < c)
        eq = null_pmf.get(c, 0.0)
    else:
        counts = np.asarray(null_counts)
        lt, eq = float(np.mean(counts < c)), float(np.mean(counts == c))
    return float(2.0 * (lt + 0.5 * eq) - 1.0)


def fit_delta_rasch(K, s, theta0=None, delta0=None):
    """Joint ML fit of logit P = theta_b + delta_j on binomial counts K (brands x CEPs) out of s (answered slots per
    CEP; all > 0; every brand 0 < sum_j K < sum_j s). Newton steps with step halving; delta_0 = 0 during the fit.
    Returns (theta, delta, converged)."""
    K, s = np.asarray(K, float), np.asarray(s, float)
    B, J = K.shape
    theta = np.array(theta0, float) if theta0 is not None else _logit((K.sum(1) + 0.5) / (s.sum() + 1.0))
    delta = np.array(delta0, float) - float(delta0[0]) if delta0 is not None else np.zeros(J)
    if J == 1:
        return theta, delta, True

    def loglik(t, d):
        eta = t[:, None] + d[None, :]
        return float(np.sum(K * eta - s[None, :] * np.logaddexp(0.0, eta)))
    cur = loglik(theta, delta)
    for _ in range(RASCH_MAX_ITER):
        p = _expit(theta[:, None] + delta[None, :])
        r = K - s[None, :] * p
        w = s[None, :] * p * (1.0 - p)
        A = w.sum(1)
        if np.any(A <= 0):
            return theta, delta, False
        g_t, g_d, Bm = r.sum(1), r.sum(0)[1:], w[:, 1:]
        try:
            step_d = np.linalg.solve(np.diag(w.sum(0)[1:]) - Bm.T @ (Bm / A[:, None]), g_d - Bm.T @ (g_t / A))
        except np.linalg.LinAlgError:
            return theta, delta, False
        step_t = (g_t - Bm @ step_d) / A
        lam = 1.0
        while True:
            t_new, d_new = theta + lam * step_t, delta + lam * np.r_[0.0, step_d]
            new = loglik(t_new, d_new)
            if new >= cur - 1e-12 or lam < 1e-8:
                break
            lam /= 2.0
        theta, delta, cur = t_new, d_new, new
        if max(np.abs(theta).max(), np.abs(delta).max()) > RASCH_BOUND:
            return theta, delta, False
        if lam * max(np.abs(step_t).max(), np.abs(step_d).max()) < RASCH_TOL:
            return theta, delta, True
    return theta, delta, False


def rasch_deltas(slot_cep, Y, n_ceps):
    """Leave-b-out CEP effects delta^(-b) for every brand column of one model's answered CEP calls in one category
    (SCORER_NOTES N2). Returns (deltas (B, n_ceps), status per brand: ok / not_converged / no_informative_brands)."""
    slot_cep = np.asarray(slot_cep, int)
    Y = np.asarray(Y, float)
    B = Y.shape[1]
    s = np.bincount(slot_cep, minlength=n_ceps).astype(float) if len(slot_cep) else np.zeros(n_ceps)
    Kjb = np.zeros((n_ceps, B))
    np.add.at(Kjb, slot_cep, Y)
    K, S_tot = Kjb.T, s.sum()
    cols = np.where(s > 0)[0]
    tot = K.sum(1)
    info = (tot > 0) & (tot < S_tot)
    deltas = np.zeros((B, n_ceps))
    if len(cols) <= 1:
        return deltas, ["ok"] * B
    th_all, d_all, ok_all = (fit_delta_rasch(K[info][:, cols], s[cols]) if info.sum() else (None, None, False))
    status = []
    for b in range(B):
        keep = info.copy()
        keep[b] = False
        if not keep.any():
            status.append("no_informative_brands")
            continue
        th0 = th_all[keep[info]] if ok_all else None
        _th, d, ok = fit_delta_rasch(K[keep][:, cols], s[cols], th0, d_all if ok_all else None)
        if not ok:
            status.append("not_converged")
            continue
        deltas[b, cols] = d - d.mean()
        status.append("ok")
    return deltas, status


def null_pmf_rasch(s_counts, delta, n):
    """Exact null pmf of C (CEPs touched) given n when the named slots follow the conditional Bernoulli law with CEP
    weights exp(delta_j): x^n coefficient of prod_j [1 + z((1 + e^delta_j x)^s_j - 1)], normalised over z."""
    s_counts = np.asarray(s_counts, int)
    delta = np.asarray(delta, float)
    S, J = int(s_counts.sum()), len(s_counts)
    if not 0 <= n <= S:
        raise ValueError("n outside 0..answered slots")
    used = s_counts > 0
    a = float(delta[used].max()) if used.any() else 0.0           # rescaling x: cancels in the normalisation
    P = np.zeros((J + 1, S + 1))
    P[0, 0] = 1.0
    for sj, dj in zip(s_counts, delta):
        if sj == 0:
            continue
        t = [math.comb(int(sj), k) * math.exp(k * (dj - a)) for k in range(sj + 1)]
        new = P * t[0]
        for k in range(1, sj + 1):
            new[1:, k:] += P[:-1, :-k] * t[k]
        P = new
    coef = P[:, n]
    tot = coef.sum()
    return {int(c): float(v / tot) for c, v in enumerate(coef) if v > 0}


def beta_bm(slot_cep, Y, bi, n_ceps, delta=None):
    """beta (and S8 beta_mid) for brand column bi of one model's answered CEP calls in one category, against the exact
    conditional-Bernoulli null with CEP effects delta (r1 primary: delta^(-b); S3: delta None = 0).
    slot_cep: (S,) CEP index of each answered call; Y: (S, B) 0/1 registry-brand mentions."""
    slot_cep = np.asarray(slot_cep, int)
    Y = np.asarray(Y)
    S = len(slot_cep)
    s_counts = np.bincount(slot_cep, minlength=n_ceps) if S else np.zeros(n_ceps, int)
    y = Y[:, bi].astype(int) if S else np.zeros(0, int)
    n = int(y.sum())
    rec = {"slots": S, "n": n}
    if n == 0:
        rec.update(c=0, E=None, cmax=0, cmin=0, beta=None, beta_mid=None)
        return rec
    c = int(np.count_nonzero(np.bincount(slot_cep[y == 1], minlength=n_ceps)))
    cmax, cmin = c_max_of(s_counts, n), c_min_of(s_counts, n)
    pmf = null_pmf_rasch(s_counts, np.zeros(n_ceps) if delta is None else delta, n)
    E = float(sum(k * p for k, p in pmf.items()))
    rec.update(c=c, E=E, cmax=cmax, cmin=cmin, beta=beta_of(c, E, cmax, cmin), beta_mid=beta_mid(c, null_pmf=pmf))
    return rec


def index_answers(answers):
    """{(substrate, model, probe_id, run): frozenset(brands)}; one answer per key (SCORER_NOTES N1)."""
    out = {}
    for a in answers:
        k = (a["substrate"], a["model"], a["probe_id"], int(a["run"]))
        if k in out:
            raise ValueError(f"duplicate answer {k}: deduplicate calls before scoring")
        out[k] = frozenset(a["brands"])
    return out


def coverage_table(ans_index, brands_by_sub, ceps_by_sub, models, null="rasch"):
    """beta record per (substrate, brand, model) for every model in `models`. null="rasch": the primary null
    (leave-b-out delta, SCORER_NOTES N2); null="equal": S3 (delta = 0). ceps_by_sub: {substrate: [CEP probe
    IDs]} (14, or a half's 7). Deterministic: no random draws."""
    if null not in ("rasch", "equal"):
        raise ValueError(null)
    out = {}
    for sub in sorted(ceps_by_sub):
        ceps = list(ceps_by_sub[sub])
        cidx = {p: i for i, p in enumerate(ceps)}
        brands = sorted(brands_by_sub[sub])
        bidx = {b: i for i, b in enumerate(brands)}
        for m in sorted(models):
            keys = sorted(k for k in ans_index if k[0] == sub and k[1] == m and k[2] in cidx)
            slot_cep = np.array([cidx[k[2]] for k in keys], int)
            Y = np.zeros((len(keys), len(brands)), np.int8)
            for i, k in enumerate(keys):
                for b in ans_index[k]:
                    if b in bidx:
                        Y[i, bidx[b]] = 1
            if null == "rasch":
                deltas, status = rasch_deltas(slot_cep, Y, len(ceps))
            for b in brands:
                bi = bidx[b]
                rec = beta_bm(slot_cep, Y, bi, len(ceps), deltas[bi] if null == "rasch" else None)
                rec["delta_status"] = status[bi] if null == "rasch" else "equal"
                out[(sub, b, m)] = rec
    return out


def cov_star(tab, sub, b, panel, floor=FLOOR_FULL, min_models=MIN_MODELS_NAMED, key="beta"):
    """Cov*_b = 50 * (1 + mean beta over the panel's models with n >= 1); rated iff n_b >= floor and at least
    `min_models` panel models have n >= 1; otherwise NOT RATED (None). key="beta_mid": sensitivity S8."""
    recs = [tab.get((sub, b, m)) for m in panel]
    ns = [r["n"] if r else 0 for r in recs]
    n_b, named = int(sum(ns)), int(sum(1 for x in ns if x >= 1))
    rated = n_b >= floor and named >= min_models
    betas = [r[key] for r in recs if r and r["n"] >= 1]
    val = 50.0 * (1.0 + float(np.mean(betas))) if rated and betas else None
    return {"cov_star": val, "rated": bool(rated), "n_b": n_b, "models_naming": named,
            "mean_beta": float(np.mean(betas)) if betas else None}


def cov_star_map(tab, panel, floor=FLOOR_FULL, min_models=MIN_MODELS_NAMED, key="beta"):
    units = sorted({(s, b) for (s, b, _m) in tab})
    return {u: cov_star(tab, u[0], u[1], panel, floor, min_models, key)["cov_star"] for u in units}


def pi_cov(tab, sub, b, panel):
    """Share of the panel's answered CEP answers in b's category that name b (section 2.3)."""
    recs = [tab.get((sub, b, m)) for m in panel]
    n = sum(r["n"] for r in recs if r)
    S = sum(r["slots"] for r in recs if r)
    return n / S if S else NAN


def pi_cov_map(tab, panel):
    units = sorted({(s, b) for (s, b, _m) in tab})
    return {u: pi_cov(tab, u[0], u[1], panel) for u in units}


def model_covers(ans_index, sub, m, cep, b):
    """m covers (b, j): named in a majority of its answered runs of CEP j (2 of 3 when complete)."""
    ys = [int(b in ans_index[(sub, m, cep, r)]) for r in RUNS if (sub, m, cep, r) in ans_index]
    return bool(ys) and sum(ys) > len(ys) / 2


def raw_cov(ans_index, sub, b, panel, ceps, k=2):
    """Cov_b = share (0-100) of the category's CEPs in which at least k panel models cover b."""
    hits = sum(1 for j in ceps if sum(model_covers(ans_index, sub, m, j, b) for m in panel) >= k)
    return 100.0 * hits / len(ceps)


# =========================================================================== calibration N1 (section 2.4)
def _expit(x):
    return 1.0 / (1.0 + np.exp(-x))


def _logit(p):
    return np.log(p / (1.0 - p))


def exact_equal_weight_beta(n_ceps=14, runs=3):
    """Diagnostic: complete data (n_ceps x runs slots), equal weights. Exact distribution of c for every n
    (P(c = k) = C(J, k) [x^n]((1 + x)^runs - 1)^k / C(S, n)), E and the expectation of beta."""
    S = n_ceps * runs
    base = [0] + [math.comb(runs, i) for i in range(1, runs + 1)]      # (1 + x)^runs - 1
    polys = [[1]]
    for _k in range(1, n_ceps + 1):
        prev, new = polys[-1], [0] * (len(polys[-1]) + runs)
        for i, a in enumerate(prev):
            if a:
                for j, bc in enumerate(base):
                    if bc:
                        new[i + j] += a * bc
        polys.append(new)
    s_counts, rows = [runs] * n_ceps, []
    for n in range(1, S + 1):
        tot = math.comb(S, n)
        probs = {k: math.comb(n_ceps, k) * polys[k][n] / tot
                 for k in range(1, n_ceps + 1) if n < len(polys[k]) and polys[k][n]}
        E = sum(k * p for k, p in probs.items())
        cmax, cmin = c_max_of(s_counts, n), c_min_of(s_counts, n)
        eb = sum(p * beta_of(k, E, cmax, cmin) for k, p in probs.items())
        rows.append({"n": n, "E": round(E, 6), "E_closed_form": round(e_equal(s_counts, n), 6), "c_min": cmin,
                     "c_max": cmax, "E_beta_under_null": round(eb, 6), "sum_p": round(sum(probs.values()), 12)})
    return rows


def _bins_0p1(pis, vals):
    """Mean Cov* by naming-rate decile: 0.1-wide bins of pi_cov holding rated units (the r0 record's binning)."""
    out = collections.defaultdict(list)
    for p, v in zip(pis, vals):
        out[min(int(p * 10), 9)].append(v)
    return {f"{d / 10:.1f}-{(d + 1) / 10:.1f}": {"mean": float(np.mean(v)), "count": len(v)}
            for d, v in sorted(out.items())}


def _quantile_deciles(pis, vals):
    pis, vals = np.asarray(pis), np.asarray(vals)
    order = np.argsort(pis, kind="stable")
    return [{"pi_cov_range": [float(pis[c].min()), float(pis[c].max())], "mean": float(np.mean(vals[c])),
             "count": int(len(c))} for c in np.array_split(order, 10)]


def calibrate_n1(n_cats=1000, n_brands=24, n_models=3, n_ceps=14, n_runs=3, seed=SEED_N1,
                 rate_lo=0.02, rate_hi=0.98, cep_shift=1.0, n_ref_perm=20, log=None):
    """Calibration N1 (section 2.4; restated in r1). Synthetic design, unchanged from the r0 run:
      - each synthetic category has 24 brands with naming rates p_b ~ Uniform(0.02, 0.98), independent;
      - unequal list lengths across CEPs: CEP j carries a shift d_j ~ Uniform(-1, 1) on the logit scale, the same
        for every brand (no brand x situation association), model and run; brand b is named in an answer to CEP
        j with probability expit(logit(p_b) + d_j), independently across brands, models and runs;
      - 3 panel models, 14 CEPs x 3 runs, no missing cells;
      - Cov* as section 2.4 (r1: Rasch-type null, leave-b-out delta by deterministic ML and the exact conditional-
        Bernoulli pmf of C; floor 14 and >= 2 models naming) and pi_cov as section 2.3; one generator
        default_rng(112200), consumed per category in the order: rates, CEP shifts, the three models' answers (the r1
        null makes no random draws, so after the first category the synthetic realisation differs from the r0 run).
    Rule (r1): PASS iff |pooled centred rho_w(Cov*, pi_cov)| <= 0.05 over all rated units (categories with >= 5
    rated) AND every naming-rate decile (0.1-wide bin of pi_cov holding rated units) has mean Cov* within
    50 +/- 2.5. Reported beside it: the mean signed per-category rho, the per-category mean |rho| with its
    independence reference (Cov* permuted within category, 20 permutations, default_rng([112200, 1])), and,
    from the same data and draws, S8 (mid-p), S3 (equal weights, exact) and S9 (uncentred rho_w)."""
    log = log or (lambda *a: None)
    t0 = time.time()
    rng = np.random.default_rng(seed)
    ref_rng = np.random.default_rng([seed, 1])
    slot_cep = np.repeat(np.arange(n_ceps), n_runs)
    S = len(slot_cep)
    panel = list(range(n_models))
    variants = {"primary": ("rasch", "beta"), "S8_mid_p": ("rasch", "beta_mid"), "S3_equal_weights": ("eq", "beta")}
    fit_status, delta_err = collections.Counter(), []
    pool = {v: ([], [], []) for v in variants}
    rho_c, ref_abs, skipped = [], [], {"fewer_than_5_rated": 0, "rho_not_finite": 0}
    beta_by_n = collections.defaultdict(list)
    len_ratio, rated_total, units_total = [], 0, 0
    for k in range(n_cats):
        p = rng.uniform(rate_lo, rate_hi, n_brands)
        d = rng.uniform(-cep_shift, cep_shift, n_ceps)
        prob = _expit(_logit(p)[None, :] + d[:, None])
        Ys = [(rng.random((S, n_brands)) < prob[slot_cep]).astype(np.int8) for _ in panel]
        cep_len = np.mean([np.bincount(slot_cep, weights=Y.sum(axis=1), minlength=n_ceps) / n_runs for Y in Ys], axis=0)
        len_ratio.append(float(cep_len.max() / max(cep_len.min(), 1e-9)))
        tabs = {"rasch": {}, "eq": {}}
        fits = [rasch_deltas(slot_cep, Ys[m], n_ceps) for m in panel]
        for m in panel:
            fit_status.update(fits[m][1])
            for bi in range(n_brands):
                if fits[m][1][bi] == "ok":
                    delta_err.append(float(np.sqrt(np.mean((fits[m][0][bi] - (d - d.mean())) ** 2))))
        for bi in range(n_brands):
            for m in panel:
                tabs["rasch"][("N1", bi, m)] = beta_bm(slot_cep, Ys[m], bi, n_ceps, fits[m][0][bi])
                tabs["eq"][("N1", bi, m)] = beta_bm(slot_cep, Ys[m], bi, n_ceps, None)
        pi = np.array([pi_cov(tabs["rasch"], "N1", bi, panel) for bi in range(n_brands)])
        units_total += n_brands
        for v, (t, key) in variants.items():
            cov = np.array([np.nan if (c := cov_star(tabs[t], "N1", bi, panel, key=key)["cov_star"]) is None else c
                            for bi in range(n_brands)], float)
            rated = np.isfinite(cov)
            if v == "primary":
                rated_total += int(rated.sum())
                for bi in range(n_brands):
                    for m in panel:
                        rec = tabs["rasch"][("N1", bi, m)]
                        if rec["n"] >= 1:
                            beta_by_n[rec["n"]].append(rec["beta"])
            if rated.sum() < MIN_UNITS_PER_CAT:
                if v == "primary":
                    skipped["fewer_than_5_rated"] += 1
                continue
            x, y = cov[rated], pi[rated]
            pool[v][0].extend(x.tolist())
            pool[v][1].extend(y.tolist())
            pool[v][2].extend([k] * len(x))
            if v == "primary":
                r = rho_w(x, y, np.zeros(len(x), int))
                if not _finite(r):
                    skipped["rho_not_finite"] += 1
                else:
                    rho_c.append(r)
                    ref_abs.append(float(np.mean([abs(_pearson(stats.rankdata(ref_rng.permutation(x)),
                                                                stats.rankdata(y))) for _ in range(n_ref_perm)])))
        if (k + 1) % 100 == 0:
            xs, ys, gs = (np.array(a) for a in pool["primary"])
            log(f"N1: {k + 1}/{n_cats} categories, {time.time() - t0:.0f} s, running pooled centred rho_w = "
                f"{rho_w(xs, ys, gs):.4f}")
    res = {}
    for v in variants:
        xs, ys, gs = (np.array(a) for a in pool[v])
        bins = _bins_0p1(ys, xs)
        res[v] = {"pooled_centred_rho_w": float(rho_w(xs, ys, gs)),
                  "pooled_uncentred_rho_w_S9": float(rho_w(xs, ys, gs, centred=False)),
                  "n_units": int(len(xs)), "n_categories": int(len(set(gs.tolist()))),
                  "mean_cov_star": float(np.mean(xs)), "decile_means": bins,
                  "max_abs_decile_deviation_from_50": float(max(abs(b["mean"] - 50.0) for b in bins.values())),
                  "quantile_deciles": _quantile_deciles(ys, xs)}
    prim = res["primary"]
    ok_rho = abs(prim["pooled_centred_rho_w"]) <= N1_RULE_RHO
    ok_dec = prim["max_abs_decile_deviation_from_50"] <= N1_RULE_DECILE
    rho_c = np.array(rho_c)
    qs = [0, 2.5, 10, 25, 50, 75, 90, 97.5, 100]
    return {
        "statistic_r1": {
            "definition": "pooled centred rho_w(Cov*, pi_cov) over all rated synthetic units (categories with >= 5 "
                          "rated units), and the mean Cov* of every naming-rate decile (0.1-wide bin of pi_cov "
                          "holding rated units)",
            "pooled_centred_rho_w": prim["pooled_centred_rho_w"],
            "max_abs_decile_deviation_from_50": prim["max_abs_decile_deviation_from_50"],
            "rule": f"PASS iff |rho_w| <= {N1_RULE_RHO} and every decile mean Cov* within 50 +/- {N1_RULE_DECILE}",
            "rho_criterion_met": bool(ok_rho), "decile_criterion_met": bool(ok_dec),
            "result": "PASS" if ok_rho and ok_dec else "FAIL",
            "n_units": prim["n_units"], "n_categories": prim["n_categories"], "categories_skipped": skipped},
        "variants": res,
        "per_category_rho": {
            "mean_signed": float(rho_c.mean()), "sd": float(rho_c.std(ddof=1)),
            "se_of_mean": float(rho_c.std(ddof=1) / math.sqrt(len(rho_c))),
            "mean_abs": float(np.mean(np.abs(rho_c))),
            "mean_abs_under_independence_reference": float(np.mean(ref_abs)),
            "quantiles": {f"q{q}": float(np.percentile(rho_c, q)) for q in qs},
            "n_categories": int(len(rho_c))},
        "delta_fit": {"status_counts": dict(fit_status),
                      "failures_set_to_zero": int(sum(v for k, v in fit_status.items() if k != "ok")),
                      "rmse_delta_hat_vs_true_centred_shift": {"mean": float(np.mean(delta_err)),
                                                               "q90": float(np.percentile(delta_err, 90))}},
        "diagnostics": {
            "rated_units": rated_total, "units": units_total,
            "cep_mean_list_length_max_over_min": {"median": float(np.median(len_ratio)),
                                                  "q10": float(np.percentile(len_ratio, 10)),
                                                  "q90": float(np.percentile(len_ratio, 90))},
            "mean_beta_by_n": {str(n): {"mean": float(np.mean(v)), "count": len(v)}
                               for n, v in sorted(beta_by_n.items())},
            "exact_equal_weight_complete_data": exact_equal_weight_beta(n_ceps, n_runs)},
        "runtime_seconds": round(time.time() - t0, 1)}


def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


R0_HISTORY = {
    "draft": "r0", "result": "FAIL",
    "beta": "(c - E) / (c_max - E) if c > E; (c - E) / (E - c_min) if c < E; 0 if c = E or c_max = c_min",
    "statistic": "mean over the 1,000 synthetic categories of |per-category rho_w(Cov*, pi_cov)|; rule <= 0.10",
    "mean_abs_rho_w": 0.5234236620662217, "pooled_rho_w_uncentred": 0.5282886254248434,
    "independence_reference_mean_abs_rho": 0.17572540107353307, "runtime_seconds": 109.8,
    "run_utc": "2026-11-10T12:32:53Z to 2026-11-10T12:34:43Z",
    "code_sha256": "4447d27d387179cec2619b903674034d95de68e943103d8eca708897db0be2fe",
    "record_sha256": "45ffe381a09e270542956dae8acaa62f16a93e063de4df20d9db18273b3e92cf",
    "why_restated": "r0's two-sided normalisation has a non-zero null mean; the per-category mean |rho| has a noise "
                    "floor of about 0.18 (0.1757 in that run)"}
R1_ATTEMPT_1_HISTORY = {
    "draft": "r1, first attempt (not sent)", "result": "FAIL",
    "beta": "(c - E) / (c_max - c_min); E from the length-weighted Monte Carlo null (w = 1 + L(-b), 2,000 draws, "
            "seed 112100)",
    "statistic": "pooled centred rho_w(Cov*, pi_cov) over all rated units; rule |rho_w| <= 0.05 and every decile "
                 "mean Cov* within 50 +/- 2.5",
    "pooled_centred_rho_w": 0.1732249193760613, "max_abs_decile_deviation_from_50": 2.2300664511714032,
    "mean_signed_per_category_rho": 0.17299646090928472, "runtime_seconds": 112.9,
    "run_utc": "2026-11-10T13:16:35Z to 2026-11-10T13:18:28Z",
    "code_sha256": "b3b6e5275022e9614f0f25ce4adf2afe2352432a13b96a4c08f982f7a4fa2606",
    "record_sha256": "4427f46d5c494826877884a5f42da44638b38f37295a9f1df1ce415b816c7305",
    "why_replaced": "the length weights (about 1.9-fold across CEPs) do not reproduce how a situation-blind brand "
                    "spreads (CEP odds exp(d_j), up to 7.4-fold): E too high, mean beta -0.03 to -0.05 at n = 5-25"}


def run_n1(out_path=N1_PATH, **kw):
    from datetime import datetime, timezone
    started = datetime.now(timezone.utc).isoformat()
    res = calibrate_n1(log=lambda s: print(s, flush=True), **kw)
    rec = {
        "phase": PHASE_ID, "check": "calibration N1 (PRE_REGISTRATION_v1_12.md section 2.4), as restated in draft r1",
        "rule_r1": "on the synthetic situation-blind design below, |pooled centred rho_w(Cov*, pi_cov)| <= 0.05 over all "
                   "rated synthetic units and every naming-rate decile's mean Cov* within 50 +/- 2.5; otherwise Cov* "
                   "is revised before the lock (logged)",
        "design": {"categories": kw.get("n_cats", 1000), "brands_per_category": kw.get("n_brands", 24),
                   "models": 3, "ceps": 14, "runs": 3, "naming_rates": "Uniform(0.02, 0.98) per brand",
                   "unequal_list_lengths": "CEP shift d_j ~ Uniform(-1, 1) on the logit scale, common to all "
                                           "brands, models and runs",
                   "seed": SEED_N1, "rating_floor": FLOOR_FULL, "min_models_naming": MIN_MODELS_NAMED,
                   "beta": "r1: (c - E) / (c_max - c_min) if c_max > c_min, else 0",
                   "null": "r1: Rasch-type (leave-b-out delta, deterministic ML; exact conditional-Bernoulli pmf)",
                   "details": "calibrate_n1 docstring in score_v1_12.py"},
        **res,
        "history": {"r0": R0_HISTORY, "r1_attempt_1": R1_ATTEMPT_1_HISTORY},
        "run_started_utc": started, "run_finished_utc": datetime.now(timezone.utc).isoformat(),
        "code": {"file": "osf/methodology/v1_12/scripts/score_v1_12.py", "sha256": sha256_file(__file__)},
        "environment": {"python": platform.python_version(), "numpy": np.__version__,
                        "scipy": __import__("scipy").__version__}}
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    Path(out_path).write_text(json.dumps(rec, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return rec


def main():
    ap = argparse.ArgumentParser(description="AIAS v1.12 Coverage Paper A scorer (core)")
    ap.add_argument("--calibrate-n1", action="store_true", help="run calibration N1 (section 2.4)")
    ap.add_argument("--out", default=str(N1_PATH))
    a = ap.parse_args()
    if not a.calibrate_n1:
        ap.print_help()
        return 1
    rec = run_n1(a.out)
    s = rec["statistic_r1"]
    print(f"N1 {s['result']}: pooled centred rho_w(Cov*, pi_cov) = {s['pooled_centred_rho_w']:.4f} (rule |rho_w| <= "
          f"{N1_RULE_RHO}); max |decile mean Cov* - 50| = {s['max_abs_decile_deviation_from_50']:.2f} (rule <= "
          f"{N1_RULE_DECILE}); mean signed per-category rho = {rec['per_category_rho']['mean_signed']:.4f}; "
          f"{s['n_units']} rated units; delta fits set to 0: {rec['delta_fit']['failures_set_to_zero']}; "
          f"runtime {rec['runtime_seconds']} s -> {a.out}")
    return 0 if s["result"] == "PASS" else 2


if __name__ == "__main__":
    sys.exit(main())
