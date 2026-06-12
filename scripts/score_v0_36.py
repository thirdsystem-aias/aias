#!/usr/bin/env python3
"""
AIAS(TM) v0.36 -- CPC Regime Emergence -- Canonical Scoring

Source of truth for ALL thresholds, scopes, seed, and clustering parameters:
    prereg/v0_36_cpc_regime_emergence_content.py   (imported; never restated)
Locked at git tag v0.36-prereg-r2 BEFORE this run.

Phase type: re-analysis; no new LLM acquisition. Frozen inputs only:
    osf/v33/data/v33_eta2.csv        -- per-brand 6-dim per-model recall/recog
    osf/v23/v23_verdicts.json        -- v0.23 brand_details[].regime / composite_presence

Feature note (documented in metadata): the locked "6-dim per-model CPC vector"
primary feature is the per-model recall vector (recall_per_model) -- the
per-model components from which CV-CPC = 1/(1+CV) is formed -- z-scored within
substrate per model. Scalar CV-CPC is the sensitivity arm.

Determinism: single fixed seed (SEED) from the prereg module; all stochastic
steps (gap reference draws, permutation nulls, k-means restarts) seed from it.

Outputs:
    osf/v36/v36_verdicts.json
    reports/figs/v36/data/*.csv   (cluster assignments, linkage, gap curves,
                                    ARI null, silhouette summaries, variance table)

Usage:  cd /Users/pablou/aias && python3 scripts/score_v0_36.py
"""

import csv
import json
import importlib.util
from pathlib import Path

import numpy as np
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import pdist, squareform
from scipy import stats

ROOT = Path("/Users/pablou/aias")
PREREG = ROOT / "prereg" / "v0_36_cpc_regime_emergence_content.py"
V33_CSV = ROOT / "osf" / "v33" / "data" / "v33_eta2.csv"
V23_JSON = ROOT / "osf" / "v23" / "v23_verdicts.json"
OUT_JSON = ROOT / "osf" / "v36" / "v36_verdicts.json"
CSV_DIR = ROOT / "reports" / "figs" / "v36" / "data"

SUBSTRATES = ["v0.19", "v0.20", "v0.21", "v0.22", "v0.23"]
FLOOR = 1.0  # mean recall >= 1.0 for computable CV-CPC (v1.7 floor)


# ---------------------------------------------------------------------------
# Load locked spec (source of truth)
# ---------------------------------------------------------------------------
def load_spec():
    spec = importlib.util.spec_from_file_location("v36_prereg", PREREG)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


# ---------------------------------------------------------------------------
# Metrics (numpy; no sklearn) -- deterministic
# ---------------------------------------------------------------------------
def adjusted_rand_index(a, b):
    a = np.asarray(a); b = np.asarray(b)
    ua = {v: i for i, v in enumerate(np.unique(a))}
    ub = {v: i for i, v in enumerate(np.unique(b))}
    n = len(a)
    cont = np.zeros((len(ua), len(ub)), dtype=float)
    for x, y in zip(a, b):
        cont[ua[x], ub[y]] += 1
    def comb2(x):
        return x * (x - 1) / 2.0
    sum_ij = comb2(cont).sum()
    ai = comb2(cont.sum(axis=1)).sum()
    bj = comb2(cont.sum(axis=0)).sum()
    expected = ai * bj / comb2(n) if n > 1 else 0.0
    maxidx = (ai + bj) / 2.0
    denom = maxidx - expected
    if denom == 0:
        return 1.0 if sum_ij == expected else 0.0
    return float((sum_ij - expected) / denom)


def silhouette_from_dist(D, labels):
    """Mean silhouette from a precomputed square distance matrix D."""
    labels = np.asarray(labels)
    uniq = np.unique(labels)
    n = len(labels)
    if len(uniq) < 2 or len(uniq) >= n:
        return 0.0
    sil = np.zeros(n)
    for i in range(n):
        same = labels == labels[i]
        same[i] = False
        if same.sum() == 0:
            sil[i] = 0.0
            continue
        a_i = D[i, same].mean()
        b_i = np.inf
        for c in uniq:
            if c == labels[i]:
                continue
            mask = labels == c
            if mask.sum() == 0:
                continue
            b_i = min(b_i, D[i, mask].mean())
        denom = max(a_i, b_i)
        sil[i] = 0.0 if denom == 0 else (b_i - a_i) / denom
    return float(sil.mean())


def ward_labels(X, k):
    n = X.shape[0]
    if k <= 1:
        return np.ones(n, dtype=int)
    if k >= n:
        return np.arange(1, n + 1)
    Z = linkage(X, method="ward", metric="euclidean")
    return fcluster(Z, t=k, criterion="maxclust")


def within_dispersion(X, labels):
    """Pooled within-cluster sum of squared distances to centroid (W_k)."""
    W = 0.0
    for c in np.unique(labels):
        pts = X[labels == c]
        if len(pts) <= 1:
            continue
        centroid = pts.mean(axis=0)
        W += ((pts - centroid) ** 2).sum()
    return W


def gap_statistic(X, k_min, k_max, B, rng):
    """Tibshirani gap with uniform reference over the feature bounding box.
    Returns (selected_k, gap[], s[], logW[]) using the 1-SE selection rule."""
    n, d = X.shape
    k_max = min(k_max, n)
    ks = list(range(k_min, k_max + 1))
    logW = []
    gaps = []
    sks = []
    mins = X.min(axis=0)
    maxs = X.max(axis=0)
    for k in ks:
        lab = ward_labels(X, k)
        Wk = within_dispersion(X, lab)
        logW.append(np.log(Wk) if Wk > 0 else 0.0)
        ref_logs = np.empty(B)
        for b in range(B):
            Xb = rng.uniform(mins, maxs, size=(n, d))
            lb = ward_labels(Xb, k)
            Wb = within_dispersion(Xb, lb)
            ref_logs[b] = np.log(Wb) if Wb > 0 else 0.0
        gaps.append(ref_logs.mean() - logW[-1])
        sks.append(ref_logs.std() * np.sqrt(1.0 + 1.0 / B))
    # Tibshirani 1-SE: smallest k with gap[k] >= gap[k+1] - s[k+1]
    sel = ks[-1]
    for i in range(len(ks) - 1):
        if gaps[i] >= gaps[i + 1] - sks[i + 1]:
            sel = ks[i]
            break
    return sel, ks, gaps, sks, logW


def kmeans_best(X, k, restarts, rng):
    """Lloyd's k-means, best of `restarts` seeded restarts. Returns (labels, inertia)."""
    n = X.shape[0]
    if k <= 1:
        return np.ones(n, dtype=int), float(((X - X.mean(0)) ** 2).sum())
    if k >= n:
        return np.arange(n), 0.0
    best_lab, best_in = None, np.inf
    for _ in range(restarts):
        idx = rng.choice(n, k, replace=False)
        cent = X[idx].copy()
        lab = np.zeros(n, dtype=int)
        for _it in range(100):
            d = ((X[:, None, :] - cent[None, :, :]) ** 2).sum(axis=2)
            new = d.argmin(axis=1)
            if np.array_equal(new, lab) and _it > 0:
                break
            lab = new
            for c in range(k):
                m = lab == c
                if m.any():
                    cent[c] = X[m].mean(axis=0)
        inertia = sum(((X[lab == c] - cent[c]) ** 2).sum() for c in range(k))
        if inertia < best_in:
            best_in, best_lab = inertia, lab.copy()
    return best_lab, float(best_in)


# ---------------------------------------------------------------------------
# Data assembly (frozen artifacts only)
# ---------------------------------------------------------------------------
def load_units():
    """Return list of dicts: substrate, brand, recall6 (np[6]), mean_r, cvcpc, defined."""
    units = []
    with open(V33_CSV) as f:
        for r in csv.DictReader(f):
            recall = np.array(json.loads(r["recall_per_model"]), dtype=float)
            mean_r = recall.mean()
            if mean_r >= FLOOR:
                cv = recall.std(ddof=0) / mean_r
                cvcpc = 1.0 / (1.0 + cv)
                defined = True
            else:
                cvcpc = None
                defined = True if False else False
            units.append({
                "substrate": r["substrate"], "brand": r["brand"],
                "recall6": recall, "mean_r": float(mean_r),
                "cvcpc": cvcpc, "defined": mean_r >= FLOOR,
            })
    return units


def load_v23_regime():
    # v33_eta2.csv keys v0.23 brands by ID (S01..S24); other substrates by name.
    # Key by BOTH brand_id and brand_name for robust matching.
    d = json.load(open(V23_JSON))["brand_details"]
    regime, comp = {}, {}
    for b in d:
        for key in (b["brand_id"], b["brand_name"]):
            regime[key] = b["regime"]
            comp[key] = b["composite_presence"]
    return regime, comp


def zscore_within_substrate(units_sub):
    """Stack recall6 of a substrate's units, z-score each model column (ddof=0)."""
    M = np.vstack([u["recall6"] for u in units_sub])
    mu = M.mean(axis=0)
    sd = M.std(axis=0, ddof=0)
    sd_safe = np.where(sd == 0, 1.0, sd)
    Z = (M - mu) / sd_safe
    Z[:, sd == 0] = 0.0
    return Z


def build_feature_matrix(units, restrict_substrates=None):
    """Z-score within substrate per model; return (X, meta list) over DEFINED units."""
    rows, meta = [], []
    subs = restrict_substrates or SUBSTRATES
    for s in subs:
        us = [u for u in units if u["substrate"] == s and u["defined"]]
        if not us:
            continue
        Z = zscore_within_substrate(us)
        for i, u in enumerate(us):
            rows.append(Z[i])
            meta.append(u)
    return np.vstack(rows), meta


def residualize_within_substrate(X, meta, covariate_fn):
    """OLS residualize each column of X on a per-brand covariate, within substrate."""
    Xr = X.copy()
    meta_subs = np.array([m["substrate"] for m in meta])
    for s in np.unique(meta_subs):
        idx = np.where(meta_subs == s)[0]
        cov = np.array([covariate_fn(meta[i]) for i in idx], dtype=float)
        if np.all(np.isnan(cov)) or np.nanstd(cov) == 0:
            continue
        A = np.column_stack([np.ones(len(idx)), cov])
        for col in range(X.shape[1]):
            y = X[idx, col]
            beta, *_ = np.linalg.lstsq(A, y, rcond=None)
            Xr[idx, col] = y - A @ beta
    return Xr


# ---------------------------------------------------------------------------
# Analyses
# ---------------------------------------------------------------------------
def internal_structure(X, meta, spec, rng, perm_n, label="omnibus"):
    """Gap-select k, silhouette at k, within-substrate-shuffle silhouette null."""
    cl = spec.CLUSTERING
    sel_k, ks, gaps, sks, logW = gap_statistic(
        X, cl["k_selection"]["k_min"], cl["k_selection"]["k_max"],
        cl["k_selection"]["reference_samples_B"], rng)
    labels = ward_labels(X, sel_k)
    D = squareform(pdist(X, metric="euclidean"))
    sil = silhouette_from_dist(D, labels)
    # within-substrate permutation null on silhouette (shuffle cluster labels within substrate)
    subs = np.array([m["substrate"] for m in meta])
    sub_idx = {s: np.where(subs == s)[0] for s in np.unique(subs)}
    null = np.empty(perm_n)
    for p in range(perm_n):
        perm = labels.copy()
        for s, idx in sub_idx.items():
            perm[idx] = rng.permutation(perm[idx])
        null[p] = silhouette_from_dist(D, perm)
    pct = float((null < sil).mean() * 100.0)
    p_val = float((1 + (null >= sil).sum()) / (perm_n + 1))
    return {
        "label": label, "n": int(X.shape[0]), "selected_k": int(sel_k),
        "silhouette": round(sil, 4), "silhouette_null_pct": round(pct, 2),
        "silhouette_p": round(p_val, 5),
        "gap_k_range": [ks[0], ks[-1]],
        "gaps": [round(g, 4) for g in gaps], "gap_s": [round(s, 4) for s in sks],
        "labels": labels.tolist(),
    }


def inheritance_v23(X23, meta23, spec, rng):
    """ARI(CPC clusters, v0.23 regime) + within-substrate permutation null."""
    cl = spec.CLUSTERING
    sel_k, ks, gaps, sks, _ = gap_statistic(
        X23, cl["k_selection"]["k_min"], cl["k_selection"]["k_max"],
        cl["k_selection"]["reference_samples_B"], rng)
    labels = ward_labels(X23, sel_k)
    regime = np.array([m["regime"] for m in meta23])
    ari = adjusted_rand_index(labels, regime)
    perm_n = cl["permutation_null_n"]
    null = np.empty(perm_n)
    for p in range(perm_n):
        null[p] = adjusted_rand_index(labels, rng.permutation(regime))
    pct = float((null < ari).mean() * 100.0)
    p_val = float((1 + (null >= ari).sum()) / (perm_n + 1))
    return {
        "n": int(X23.shape[0]), "selected_k": int(sel_k),
        "ari": round(ari, 4), "ari_null_pct": round(pct, 2), "ari_p": round(p_val, 5),
        "gaps": [round(g, 4) for g in gaps],
        "labels": labels.tolist(), "regime": regime.tolist(),
        "null_sample": [round(float(x), 4) for x in null[:200]],
    }


def saturation_degeneracy(units, spec, rng):
    """(a) Brown-Forsythe directional CV-CPC variance saturated<unsaturated;
       (b) per-substrate gap k=1 majority saturated vs k>=2 majority unsaturated."""
    sat = spec.ANALYSIS_SET_SPEC["saturated_substrate_list"]["operative"]
    sat_subs = set(sat["saturated"].keys())
    uns_subs = set(sat["unsaturated"].keys())
    cl = spec.CLUSTERING

    # per-substrate CV-CPC values (defined units) + variance
    per_sub_cvcpc, per_sub_var = {}, {}
    for s in SUBSTRATES:
        vals = [u["cvcpc"] for u in units if u["substrate"] == s and u["defined"]]
        per_sub_cvcpc[s] = vals
        per_sub_var[s] = float(np.var(vals, ddof=0)) if vals else None

    # Brown-Forsythe transform: |x - within-substrate median|, grouped sat vs unsat
    def bf_dev(subset):
        dev = []
        for s in subset:
            v = np.array(per_sub_cvcpc[s], dtype=float)
            if len(v):
                dev.extend(np.abs(v - np.median(v)).tolist())
        return np.array(dev)
    dev_sat = bf_dev(sat_subs)
    dev_uns = bf_dev(uns_subs)
    # two-sided Levene (BF, median-centered) for reference
    sat_pool = np.concatenate([np.array(per_sub_cvcpc[s]) for s in sat_subs if per_sub_cvcpc[s]])
    uns_pool = np.concatenate([np.array(per_sub_cvcpc[s]) for s in uns_subs if per_sub_cvcpc[s]])
    lev_W, lev_p = stats.levene(sat_pool, uns_pool, center="median")
    # directional one-sided (saturated dispersion < unsaturated) on BF deviations
    t_stat, t_p_two = stats.ttest_ind(dev_sat, dev_uns, equal_var=False)
    bf_dir_p = t_p_two / 2.0 if dev_sat.mean() < dev_uns.mean() else 1.0 - t_p_two / 2.0
    crit_a = bf_dir_p < spec.HYPOTHESES["H_SaturationDegeneracy"]["criteria"]["bf_alpha"]

    # per-substrate gap k
    per_sub_k = {}
    for s in SUBSTRATES:
        us = [u for u in units if u["substrate"] == s and u["defined"]]
        if len(us) < 2:
            per_sub_k[s] = None
            continue
        Z = zscore_within_substrate(us)
        sel_k, *_ = gap_statistic(Z, cl["k_selection"]["k_min"],
                                  cl["k_selection"]["k_max"],
                                  cl["k_selection"]["reference_samples_B"], rng)
        per_sub_k[s] = int(sel_k)
    sat_k1 = sum(1 for s in sat_subs if per_sub_k[s] == 1)
    uns_k2 = sum(1 for s in uns_subs if per_sub_k[s] is not None and per_sub_k[s] >= 2)
    crit_b = (sat_k1 > len(sat_subs) / 2.0) and (uns_k2 > len(uns_subs) / 2.0)

    supported = bool(crit_a and crit_b)
    return {
        "per_substrate_cvcpc_variance": {k: (round(v, 5) if v is not None else None)
                                         for k, v in per_sub_var.items()},
        "per_substrate_gap_k": per_sub_k,
        "bf_levene_W": round(float(lev_W), 4), "bf_levene_p_two_sided": round(float(lev_p), 5),
        "bf_directional_p": round(float(bf_dir_p), 5),
        "dev_mean_saturated": round(float(dev_sat.mean()), 4),
        "dev_mean_unsaturated": round(float(dev_uns.mean()), 4),
        "criterion_a_variance": bool(crit_a),
        "criterion_b_gap_majority": bool(crit_b),
        "sat_substrates_k1": int(sat_k1), "uns_substrates_k2plus": int(uns_k2),
        "verdict": "SUPPORTED" if supported else "NOT SUPPORTED",
    }


# ---------------------------------------------------------------------------
# Verdict composition
# ---------------------------------------------------------------------------
def verdict_inheritance(inh, crit):
    return "SUPPORTED" if (inh["ari"] >= crit["ari_min"]
                           and inh["ari_null_pct"] >= crit["ari_null_pct"]
                           and inh["ari_p"] < crit["p_max"]) else "NOT SUPPORTED"


def verdict_internal(struct, crit):
    return (struct["selected_k"] >= crit["k_min"]
            and struct["silhouette"] >= crit["silhouette_min"]
            and struct["silhouette_null_pct"] >= crit["silhouette_null_pct"])


def _compose_cell(v_inh, v_aut, v_res):
    if v_inh == "SUPPORTED" and v_res == "NOT SUPPORTED":
        return "Cell A"
    if v_inh == "SUPPORTED" and v_res == "SUPPORTED":
        return "Cell B"
    if v_aut == "SUPPORTED" and v_res == "SUPPORTED":
        return "Cell C"
    if v_inh == "NOT SUPPORTED" and v_aut == "NOT SUPPORTED" and v_res == "NOT SUPPORTED":
        return "Cell D"
    return "unmapped"


# ---------------------------------------------------------------------------
# Sensitivity / robustness pass (locked in CLUSTERING/SENSITIVITY; executed in a
# second deterministic pass AFTER the primary run -- fresh rng off SEED so the
# primary verdicts stay bit-for-bit identical).
# ---------------------------------------------------------------------------
def sensitivity_pass(spec, seed, units, X_omni, meta_omni, omni_labels, primary_cell):
    H = spec.HYPOTHESES
    cl = spec.CLUSTERING
    omni_labels = np.asarray(omni_labels)
    omni_k = int(len(np.unique(omni_labels)))
    out = {}

    # (1) Scalar CV-CPC feature arm: 1-dim scalar, z-scored within substrate;
    #     gap-select k; agreement (ARI) with the 6-dim primary omnibus clustering.
    subs = np.array([m["substrate"] for m in meta_omni])
    scalar = np.array([m["cvcpc"] for m in meta_omni], dtype=float)
    Xs = np.zeros((len(scalar), 1))
    for s in np.unique(subs):
        idx = np.where(subs == s)[0]
        v = scalar[idx]; sd = v.std(ddof=0)
        Xs[idx, 0] = (v - v.mean()) / sd if sd > 0 else 0.0
    rng = np.random.default_rng(seed + 10)
    k_scalar, *_ = gap_statistic(Xs, cl["k_selection"]["k_min"], cl["k_selection"]["k_max"],
                                 cl["k_selection"]["reference_samples_B"], rng)
    scalar_labels = ward_labels(Xs, k_scalar)
    out["scalar_cvcpc_arm"] = {
        "feature": "scalar CV-CPC, z-scored within substrate",
        "selected_k": int(k_scalar),
        "ari_vs_6dim_primary": round(adjusted_rand_index(scalar_labels, omni_labels), 4),
        "n": int(len(scalar)),
    }

    # (2) K-means (50 restarts at the gap-selected k) concordance with Ward primary.
    rng = np.random.default_rng(seed + 11)
    km_labels, _ = kmeans_best(X_omni, omni_k, cl["kmeans_restarts"], rng)
    out["kmeans_arm"] = {
        "k": omni_k, "restarts": cl["kmeans_restarts"],
        "ari_vs_ward_primary": round(adjusted_rand_index(km_labels, omni_labels), 4),
    }

    # (3) v0.35 frozen 84-unit set (mean recall > 0 -- v0.35's floor) verdict concordance.
    units84 = []
    for u in units:
        m = float(u["recall6"].mean())
        if m > 0.0:
            u2 = dict(u)
            u2["defined"] = True
            u2["cvcpc"] = 1.0 / (1.0 + u["recall6"].std(ddof=0) / m)
            units84.append(u2)
    X84, meta84 = build_feature_matrix(units84)
    rng = np.random.default_rng(seed + 12)
    omni84 = internal_structure(X84, meta84, spec, rng, cl["permutation_null_n"], "v35_84_omnibus")
    X23_84, meta23_84 = build_feature_matrix(units84, restrict_substrates=["v0.23"])
    keep = [i for i, mm in enumerate(meta23_84) if mm.get("regime")]
    X23_84 = X23_84[keep]; meta23_84 = [meta23_84[i] for i in keep]
    rng = np.random.default_rng(seed + 13)
    inh84 = inheritance_v23(X23_84, meta23_84, spec, rng)
    X23_84r = residualize_within_substrate(X23_84, meta23_84, lambda mm: mm["composite"])
    rng = np.random.default_rng(seed + 14)
    res84 = internal_structure(X23_84r, meta23_84, spec, rng, cl["permutation_null_n"], "v35_84_v23_residual")
    rng = np.random.default_rng(seed + 15)
    sat84 = saturation_degeneracy(units84, spec, rng)
    ac = H["H_RegimeAutonomy"]["criteria"]
    v_inh84 = verdict_inheritance(inh84, H["H_RegimeInheritance"]["criteria"])
    aut84 = (omni84["selected_k"] >= ac["k_min"] and omni84["silhouette"] >= ac["silhouette_min"]
             and omni84["silhouette_null_pct"] >= ac["silhouette_null_pct"])
    v_aut84 = "SUPPORTED" if (aut84 and inh84["ari"] < ac["ari_max"] and v_inh84 == "NOT SUPPORTED") else "NOT SUPPORTED"
    v_res84 = "SUPPORTED" if verdict_internal(res84, H["H_ResidualStructure"]["criteria"]) else "NOT SUPPORTED"
    cell84 = _compose_cell(v_inh84, v_aut84, v_res84)
    out["v35_84unit_concordance"] = {
        "set": "v0.35 frozen 84-unit analysis set (mean recall > 0; v0.35 floor)",
        "n_units": int(len(meta84)), "n_v23_defined": int(len(meta23_84)),
        "verdict_cell": cell84, "concordant_with_primary": bool(cell84 == primary_cell),
        "inheritance": v_inh84, "autonomy": v_aut84, "residual": v_res84,
        "saturation": sat84["verdict"],
        "omnibus_k": omni84["selected_k"], "omnibus_silhouette": omni84["silhouette"],
        "inheritance_ari": inh84["ari"], "inheritance_k": inh84["selected_k"],
        "inheritance_n": inh84["n"],
    }
    return out


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    spec = load_spec()
    CSV_DIR.mkdir(parents=True, exist_ok=True)
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    seed = spec.SEED

    print("=" * 64)
    print("AIAS v0.36 -- CPC Regime Emergence -- scoring (lock v0.36-prereg-r2)")
    print("=" * 64)

    # ---- VALIDATION GATE (step 0) ----
    print("\n[gate] step 0: validation gate")
    regime, comp = load_v23_regime()
    _bd = json.load(open(V23_JSON))["brand_details"]
    gate_labels_ok = (len(_bd) == 24
                      and len({b["regime"] for b in _bd}) == 4
                      and all(b["composite_presence"] is not None for b in _bd))
    # determinism: identical stochastic output under the same seed
    r1 = np.random.default_rng(seed).uniform(size=2000).sum()
    r2 = np.random.default_rng(seed).uniform(size=2000).sum()
    Xg, mg = build_feature_matrix(load_units(), restrict_substrates=["v0.23"])
    k1, _ = kmeans_best(Xg, 3, spec.CLUSTERING["kmeans_restarts"], np.random.default_rng(seed))
    k2, _ = kmeans_best(Xg, 3, spec.CLUSTERING["kmeans_restarts"], np.random.default_rng(seed))
    determinism_ok = (r1 == r2) and np.array_equal(k1, k2)
    gate_pass = bool(gate_labels_ok and determinism_ok)
    print(f"        v0.23 frozen labels: {'OK' if gate_labels_ok else 'FAIL'} "
          f"(24 brands, 4 regimes, composites present)")
    print(f"        determinism (seed={seed}): {'OK' if determinism_ok else 'FAIL'}")
    if not gate_pass:
        print("\nHARD STOP: validation gate failed. No scoring. Escalate for r3.")
        raise SystemExit(1)
    print("        GATE PASSED")

    units = load_units()
    n_defined = {s: sum(1 for u in units if u["substrate"] == s and u["defined"])
                 for s in SUBSTRATES}
    print(f"\n[data] defined units per substrate: {n_defined} "
          f"(total {sum(n_defined.values())} / 112)")

    # attach v0.23 regime + composite to meta
    for u in units:
        if u["substrate"] == "v0.23":
            u["regime"] = regime.get(u["brand"])
            u["composite"] = comp.get(u["brand"])

    # ---- OMNIBUS internal structure (6-dim primary) ----
    print("\n[omnibus] internal structure (6-dim per-model, 112-defined)")
    X_omni, meta_omni = build_feature_matrix(units)
    rng = np.random.default_rng(seed)
    omni = internal_structure(X_omni, meta_omni, spec, rng,
                              spec.CLUSTERING["permutation_null_n"], "omnibus_raw")
    print(f"        k={omni['selected_k']} sil={omni['silhouette']} "
          f"null_pct={omni['silhouette_null_pct']} p={omni['silhouette_p']}")

    # ---- OMNIBUS mean-recall residual (sensitivity) ----
    print("\n[omnibus] mean-recall residual (sensitivity-only)")
    X_omni_res = residualize_within_substrate(X_omni, meta_omni, lambda m: m["mean_r"])
    rng = np.random.default_rng(seed + 1)
    omni_res = internal_structure(X_omni_res, meta_omni, spec, rng,
                                  spec.CLUSTERING["permutation_null_n"],
                                  "omnibus_mean_recall_residual")
    print(f"        k={omni_res['selected_k']} sil={omni_res['silhouette']} "
          f"null_pct={omni_res['silhouette_null_pct']}")

    # ---- v0.23 raw: inheritance (ARI) ----
    print("\n[v0.23] inheritance ARI vs Presence-quartile regime (n=defined)")
    X23, meta23 = build_feature_matrix(units, restrict_substrates=["v0.23"])
    # keep only units with a regime label (all defined v0.23 have one)
    keep = [i for i, m in enumerate(meta23) if m.get("regime")]
    X23 = X23[keep]; meta23 = [meta23[i] for i in keep]
    rng = np.random.default_rng(seed + 2)
    inh = inheritance_v23(X23, meta23, spec, rng)
    print(f"        n={inh['n']} k={inh['selected_k']} ARI={inh['ari']} "
          f"null_pct={inh['ari_null_pct']} p={inh['ari_p']}")

    # ---- v0.23 raw internal structure (for autonomy/residual baseline) ----
    rng = np.random.default_rng(seed + 3)
    v23_raw = internal_structure(X23, meta23, spec, rng,
                                 spec.CLUSTERING["permutation_null_n"], "v23_raw")

    # ---- v0.23 residual on composite_presence (H_ResidualStructure primary) ----
    print("\n[v0.23] residual structure on composite_presence")
    X23_res = residualize_within_substrate(X23, meta23, lambda m: m["composite"])
    rng = np.random.default_rng(seed + 4)
    v23_res = internal_structure(X23_res, meta23, spec, rng,
                                 spec.CLUSTERING["permutation_null_n"], "v23_residual")
    print(f"        k={v23_res['selected_k']} sil={v23_res['silhouette']} "
          f"null_pct={v23_res['silhouette_null_pct']}")

    # ---- Saturation degeneracy (omnibus) ----
    print("\n[omnibus] saturation degeneracy (BF + per-substrate gap)")
    rng = np.random.default_rng(seed + 5)
    sat = saturation_degeneracy(units, spec, rng)
    print(f"        per-substrate gap k: {sat['per_substrate_gap_k']}")
    print(f"        BF directional p={sat['bf_directional_p']} (a={sat['criterion_a_variance']}) "
          f"| crit_b={sat['criterion_b_gap_majority']} -> {sat['verdict']}")

    # ---- Compose hypothesis verdicts ----
    H = spec.HYPOTHESES
    v_inh = verdict_inheritance(inh, H["H_RegimeInheritance"]["criteria"])
    # autonomy: omnibus internal-structure criteria + v0.23 ARI<0.30 leg
    aut_crit = H["H_RegimeAutonomy"]["criteria"]
    aut_internal = (omni["selected_k"] >= aut_crit["k_min"]
                    and omni["silhouette"] >= aut_crit["silhouette_min"]
                    and omni["silhouette_null_pct"] >= aut_crit["silhouette_null_pct"])
    aut_ari_leg = inh["ari"] < aut_crit["ari_max"]
    v_aut = "SUPPORTED" if (aut_internal and aut_ari_leg and v_inh == "NOT SUPPORTED") else "NOT SUPPORTED"
    v_res = "SUPPORTED" if verdict_internal(v23_res, H["H_ResidualStructure"]["criteria"]) else "NOT SUPPORTED"
    v_res_sens = "SUPPORTED" if verdict_internal(omni_res, H["H_ResidualStructure"]["criteria"]) else "NOT SUPPORTED"
    v_sat = sat["verdict"]

    # verdict-matrix cell (per locked matrix: inheritance/autonomy + residual structure)
    if v_inh == "SUPPORTED" and v_res == "NOT SUPPORTED":
        cell = "Cell A"
    elif v_inh == "SUPPORTED" and v_res == "SUPPORTED":
        cell = "Cell B"
    elif v_aut == "SUPPORTED" and v_res == "SUPPORTED":
        cell = "Cell C"
    elif v_inh == "NOT SUPPORTED" and v_aut == "NOT SUPPORTED" and v_res == "NOT SUPPORTED":
        cell = "Cell D"
    else:
        cell = "unmapped"

    # ---- Write intermediate CSVs ----
    with open(CSV_DIR / "cluster_assignments_omnibus.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["substrate", "brand", "cluster", "mean_r", "cvcpc"])
        for m, lab in zip(meta_omni, omni["labels"]):
            w.writerow([m["substrate"], m["brand"], lab, round(m["mean_r"], 3),
                        round(m["cvcpc"], 4)])
    with open(CSV_DIR / "cluster_assignments_v23.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["brand", "cluster", "regime", "composite", "cvcpc"])
        for m, lab in zip(meta23, inh["labels"]):
            w.writerow([m["brand"], lab, m["regime"], m["composite"], round(m["cvcpc"], 4)])
    with open(CSV_DIR / "gap_curves.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["analysis", "k", "gap", "gap_s"])
        for name, st in [("omnibus_raw", omni), ("omnibus_mean_recall_residual", omni_res),
                         ("v23_raw", v23_raw), ("v23_residual", v23_res)]:
            ks = list(range(st["gap_k_range"][0], st["gap_k_range"][1] + 1))
            for k, g, s in zip(ks, st["gaps"], st["gap_s"]):
                w.writerow([name, k, g, s])
    with open(CSV_DIR / "ari_null_distribution.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["ari_null"]); [w.writerow([x]) for x in inh["null_sample"]]
    with open(CSV_DIR / "per_substrate_variance_table.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["substrate", "cvcpc_variance", "gap_k", "saturated"])
        sat_set = set(spec.ANALYSIS_SET_SPEC["saturated_substrate_list"]["operative"]["saturated"])
        for s in SUBSTRATES:
            w.writerow([s, sat["per_substrate_cvcpc_variance"][s],
                        sat["per_substrate_gap_k"][s], s in sat_set])
    with open(CSV_DIR / "silhouette_summary.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["analysis", "n", "k", "silhouette", "null_pct", "p"])
        for st in [omni, omni_res, v23_raw, v23_res]:
            w.writerow([st["label"], st["n"], st["selected_k"], st["silhouette"],
                        st["silhouette_null_pct"], st["silhouette_p"]])
    # dendrogram linkage (omnibus) for chart builds
    Zlink = linkage(X_omni, method="ward", metric="euclidean")
    np.savetxt(CSV_DIR / "linkage_omnibus.csv", Zlink, delimiter=",",
               header="c1,c2,dist,n", comments="")

    # ---- Assemble verdicts JSON ----
    verdicts = {
        "phase": "v0.36", "title": spec.PHASE_TITLE,
        "lock_tag": "v0.36-prereg-r2",
        "metadata": {
            "seed": seed,
            "feature_note": ("6-dim per-model feature = recall_per_model "
                             "(per-model components of CV-CPC), z-scored within "
                             "substrate per model; scalar CV-CPC = sensitivity arm."),
            "clustering": "Ward/Euclidean; gap (Tibshirani 1-SE, uniform bbox ref, "
                          "B=%d, k in {%d..%d}); within-substrate permutation null n=%d; "
                          "k-means %d restarts (sensitivity)." % (
                              spec.CLUSTERING["k_selection"]["reference_samples_B"],
                              spec.CLUSTERING["k_selection"]["k_min"],
                              spec.CLUSTERING["k_selection"]["k_max"],
                              spec.CLUSTERING["permutation_null_n"],
                              spec.CLUSTERING["kmeans_restarts"]),
            "n_defined_per_substrate": n_defined,
            "gate": {"v23_labels_ok": gate_labels_ok, "determinism_ok": determinism_ok,
                     "passed": gate_pass},
            "no_sklearn": "ARI/silhouette/k-means implemented in-script (deterministic).",
        },
        "selected_k": {
            "omnibus_raw": omni["selected_k"],
            "omnibus_mean_recall_residual": omni_res["selected_k"],
            "v23_raw": inh["selected_k"],
            "v23_residual": v23_res["selected_k"],
        },
        "hypotheses": {
            "H_RegimeInheritance": {
                "scope": H["H_RegimeInheritance"]["scope"], "verdict": v_inh,
                "ari": inh["ari"], "ari_null_pct": inh["ari_null_pct"],
                "ari_p": inh["ari_p"], "n": inh["n"], "selected_k": inh["selected_k"],
                "prediction": spec.PREDICTIONS["H_RegimeInheritance"]["prediction"],
            },
            "H_RegimeAutonomy": {
                "scope": H["H_RegimeAutonomy"]["scope"], "verdict": v_aut,
                "omnibus_internal": {"k": omni["selected_k"], "silhouette": omni["silhouette"],
                                     "null_pct": omni["silhouette_null_pct"]},
                "v23_ari_below_0.30": bool(aut_ari_leg),
                "mutually_exclusive_note": "moot if inheritance SUPPORTED",
            },
            "H_ResidualStructure": {
                "scope": H["H_ResidualStructure"]["scope"], "verdict": v_res,
                "v23_residual": {"k": v23_res["selected_k"], "silhouette": v23_res["silhouette"],
                                 "null_pct": v23_res["silhouette_null_pct"]},
                "omnibus_mean_recall_sensitivity": {
                    "verdict_sensitivity_only": v_res_sens,
                    "k": omni_res["selected_k"], "silhouette": omni_res["silhouette"],
                    "null_pct": omni_res["silhouette_null_pct"]},
                "prediction": spec.PREDICTIONS["H_ResidualStructure"]["prediction"],
            },
            "H_SaturationDegeneracy": {
                "scope": H["H_SaturationDegeneracy"]["scope"], "verdict": v_sat,
                "prediction": spec.PREDICTIONS["H_SaturationDegeneracy"]["prediction"],
                **sat,
            },
        },
        "verdict_matrix_cell": cell,
        "verdict_matrix_cell_verdict": spec.VERDICT_MATRIX.get(cell, {}).get("verdict"),
        "omnibus_internal_structure_descriptor": {
            "k": omni["selected_k"], "silhouette": omni["silhouette"],
            "null_pct": omni["silhouette_null_pct"], "p": omni["silhouette_p"]},
        "predicted_net": spec.PREDICTIONS["net"],
    }

    # ---- Sensitivity / robustness pass (post-primary, deterministic) ----
    print("\n[sensitivity] scalar arm · k-means concordance · v0.35 84-unit concordance")
    sens = sensitivity_pass(spec, seed, units, X_omni, meta_omni, omni["labels"], cell)
    verdicts["metadata"]["sensitivity"] = sens
    verdicts["metadata"]["deviations"] = [{
        "entry": "DEV-S1 (post-primary sensitivity execution)",
        "text": ("The locked sensitivity/robustness arms — scalar CV-CPC feature, "
                 "k-means concordance at the gap-selected k, and the v0.35 84-unit "
                 "verdict-concordance check — were executed in a second deterministic "
                 "pass AFTER the primary scoring run (same thresholds, same seed=%d, "
                 "frozen inputs; pre-publication). They are robustness checks and do "
                 "NOT alter any locked primary verdict (Cell D stands). The r2 scorer "
                 "omitted them at the primary run; logged here for transparency. A "
                 "canonical prereg DEVIATIONS amendment (v0.36-prereg-r3) is "
                 "recommended to mirror this in the deposited pre-registration." % seed)
    }]
    with open(CSV_DIR / "sensitivity_summary.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["arm", "key", "value"])
        w.writerow(["scalar_cvcpc", "selected_k", sens["scalar_cvcpc_arm"]["selected_k"]])
        w.writerow(["scalar_cvcpc", "ari_vs_6dim_primary", sens["scalar_cvcpc_arm"]["ari_vs_6dim_primary"]])
        w.writerow(["kmeans", "ari_vs_ward_primary", sens["kmeans_arm"]["ari_vs_ward_primary"]])
        w.writerow(["v35_84unit", "verdict_cell", sens["v35_84unit_concordance"]["verdict_cell"]])
        w.writerow(["v35_84unit", "concordant_with_primary", sens["v35_84unit_concordance"]["concordant_with_primary"]])
        w.writerow(["v35_84unit", "n_units", sens["v35_84unit_concordance"]["n_units"]])
    print(f"        scalar arm: k={sens['scalar_cvcpc_arm']['selected_k']} "
          f"ARI_vs_primary={sens['scalar_cvcpc_arm']['ari_vs_6dim_primary']}")
    print(f"        k-means(k={sens['kmeans_arm']['k']},{sens['kmeans_arm']['restarts']}x): "
          f"ARI_vs_ward={sens['kmeans_arm']['ari_vs_ward_primary']}")
    print(f"        v35 84-unit ({sens['v35_84unit_concordance']['n_units']}u): "
          f"cell={sens['v35_84unit_concordance']['verdict_cell']} "
          f"concordant={sens['v35_84unit_concordance']['concordant_with_primary']}")

    with open(OUT_JSON, "w") as f:
        json.dump(verdicts, f, indent=2)

    # ---- Summary ----
    print("\n" + "=" * 64)
    print("VERDICTS")
    print("=" * 64)
    print(f"  H_RegimeInheritance   [{H['H_RegimeInheritance']['scope'][:18]}...]: {v_inh} "
          f"(ARI={inh['ari']}, null_pct={inh['ari_null_pct']}, p={inh['ari_p']}, n={inh['n']})")
    print(f"  H_RegimeAutonomy      [composed]: {v_aut} "
          f"(omni k={omni['selected_k']} sil={omni['silhouette']} null%={omni['silhouette_null_pct']}; "
          f"v23 ARI<0.30={aut_ari_leg})")
    print(f"  H_ResidualStructure   [v0.23]: {v_res} "
          f"(k={v23_res['selected_k']} sil={v23_res['silhouette']} null%={v23_res['silhouette_null_pct']}) "
          f"| omnibus mean-recall sensitivity: {v_res_sens}")
    print(f"  H_SaturationDegeneracy [omnibus]: {v_sat} "
          f"(BF dir p={sat['bf_directional_p']}, crit_a={sat['criterion_a_variance']}, "
          f"crit_b={sat['criterion_b_gap_majority']})")
    print(f"\n  VERDICT-MATRIX CELL: {cell} -> {verdicts['verdict_matrix_cell_verdict']}")
    print(f"  selected k: omni_raw={omni['selected_k']}, "
          f"omni_mean_recall_resid={omni_res['selected_k']}, "
          f"v23_raw={inh['selected_k']}, v23_resid={v23_res['selected_k']}")
    print(f"  per-substrate gap k: {sat['per_substrate_gap_k']}")
    print(f"\n  verdicts -> {OUT_JSON}")
    print(f"  intermediate CSVs -> {CSV_DIR}")


if __name__ == "__main__":
    main()
