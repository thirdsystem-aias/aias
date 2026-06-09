#!/usr/bin/env python3
"""
v0.33 — Provider-Asymmetric CPC scorer.
Locked against v0.33-prereg-r1 (commit c8f2736). Re-analysis; NO new LLM acquisition.

Secondary analysis of v0.31's frozen per-model inputs. Tests whether the per-model
CV-CPC quantity carries systematic between-PROVIDER structure (PRIMARY), and — the
gating question — whether that structure exceeds the provider structure already
present in Presence/recognition (PRIMARY gate, H_Provider_Beyond_Presence).

Per-model values x_{b,m} (m in the canonical-6 panel; provider p(m) in 3 labeled
2-model groups):
  CV-CPC arm : x = per-model Phase B RECALL count (the CPC-generating values),
               recomputed by RE-USING v0.31's extraction functions verbatim
               (provenance lock; score_v0_31.counts_*).
  C_P arm    : x = per-model Phase A RECOGNITION (binary), recomputed here from the
               Phase A files named in PROVENANCE.presence_recovery.

eta^2_b = SS_between(provider) / SS_total over the 6 per-model values.
ZERO-VARIANCE CONVENTION (locked, SCORING): SS_total == 0  ->  eta^2 := 0 (NOT
excluded). A brand whose models do not differ shows zero provider asymmetry;
saturated-recognition brands (eta^2_CP = 0, eta^2_CVCPC > 0) are the purest
beyond-Presence signal.

PRIMARY null: per-brand label space is exactly enumerable — 6 models into 3 labeled
pairs = 6!/(2!2!2!) = 90 assignments. Population test = Monte Carlo over the per-brand
90-spaces, >= 10,000 draws, one-sided.
RECONCILIATION GATE: recomputed v0.20/0.21/0.22 per-model RECALL vectors must
reproduce osf/methodology/v1_7/data/v1_7_cpc.csv 'r_per_model' bit-for-bit, aligned
BY MODEL NAME (v1.7 stored sorted-model order; PANEL order differs). Mismatch =>
computational-reproducibility note (NOT a DEVIATIONS entry); HALT.
SCOPE: anchor covers v0.20/0.21/0.22 only. v0.19, v0.23 rest on v0.31 extraction
provenance alone (stated, not overclaimed).
"""
import sys, json, csv, itertools
from pathlib import Path
import numpy as np
from scipy import stats

ROOT = Path.home() / "aias"
sys.path.insert(0, str(ROOT / "prereg"))
sys.path.insert(0, str(ROOT / "scripts"))

import v0_33_provider_asymmetry_content as PRE      # the locked methodology
import score_v0_31 as S31                           # RECALL extractors (provenance lock)
import score_v20, score_v21, score_v22              # certified matchers (raw-text substrates)

PANEL = S31.PANEL                  # fixed canonical-6 order
# PANEL index -> provider (2 models each). Matches PRE.PROVIDER_GROUPS by construction.
PROVIDERS = {"Anthropic": (0, 1), "OpenAI": (2, 3), "Google": (4, 5)}
OBS_ASSIGNMENT = ((0, 1), (2, 3), (4, 5))
V17_MODEL_ORDER = sorted(PANEL)    # the order v1.7 (score_v1_7.py:107) stored r_per_model in
FLOOR = 1.0
N_MC = 10_000
SEED = 280400
OMNI_ORDER = ["v0.19", "v0.20", "v0.21", "v0.22", "v0.23"]
N_FRAMES = 6                       # omnibus geometry (range of per-model recall counts)
CAT = {"v0.19": "audiophile headphones", "v0.20": "skincare", "v0.21": "cosmetics",
       "v0.22": "automotive", "v0.23": "premium spirits", "v0.18": "indie fragrance"}

# sanity: the PANEL->provider map agrees with the locked PROVIDER_GROUPS sizes
assert len(PRE.PROVIDER_GROUPS) == 3 and all(len(v) == 2 for v in PRE.PROVIDER_GROUPS.values())


# --------------------------------------------------------------------------- #
# eta^2 over the labeled-pair partition of the six per-model values
# --------------------------------------------------------------------------- #
def gen_90():
    """All 90 ways to split 6 panel positions into 3 LABELED pairs (6!/(2!2!2!))."""
    pos = list(range(6)); out = []
    for a in itertools.combinations(pos, 2):
        rem = [p for p in pos if p not in a]
        for b in itertools.combinations(rem, 2):
            c = tuple(p for p in rem if p not in b)
            out.append((a, b, c))
    assert len(out) == 90
    return out

ASSIGN90 = gen_90()
OBS_IDX = ASSIGN90.index(OBS_ASSIGNMENT)    # == 0; the true grouping


def eta2_for(x, assignment):
    """SS_between(3 labeled pairs) / SS_total over the 6 values. Zero-variance -> 0."""
    x = np.asarray(x, float)
    grand = x.mean()
    ss_total = float(((x - grand) ** 2).sum())
    if ss_total <= 0.0:
        return 0.0                              # ZERO-VARIANCE CONVENTION (locked)
    ss_between = 0.0
    for pair in assignment:                     # 3 labeled pairs, 2 each
        pm = (x[pair[0]] + x[pair[1]]) / 2.0
        ss_between += 2.0 * (pm - grand) ** 2
    return ss_between / ss_total


def eta2_vector(x):
    """eta^2 under all 90 assignments for a single brand's 6-vector."""
    return np.array([eta2_for(x, a) for a in ASSIGN90], float)


# --------------------------------------------------------------------------- #
# RECALL recompute (CV-CPC arm) — reuse v0.31 extractors verbatim
# --------------------------------------------------------------------------- #
V = ROOT / "osf"
RECON_CFG = {
    "v0.20": ("json",   ROOT / "prereg/v0_20_registry.json",         score_v20, V / "v20/phase_b_results.csv"),
    "v0.21": ("json",   ROOT / "prereg/v0_21_registry.json",         score_v21, V / "v21/phase_b_results.csv"),
    "v0.22": ("module", ROOT / "prereg/v0_22_automotive_content.py", score_v22, V / "v22/phase_b_results.csv"),
}


def recall_counts():
    """{substrate: ({brand:[6 recall counts in PANEL order]}, {brand:cell})}."""
    out = {}
    for k, (rk, rp, mod, pb) in RECON_CFG.items():
        out[k] = S31.counts_raw_text(rk, rp, mod, pb)
    out["v0.19"] = S31.counts_v19(V / "v19/phase_b_results.csv")
    out["v0.23"] = S31.counts_v23(V / "v23/data/v23_phase_b_scored.json")
    return out


# --------------------------------------------------------------------------- #
# RECOGNITION recompute (C_P arm) — per-model Phase A, binary
# --------------------------------------------------------------------------- #
def _vec(agg):
    return {b: [agg[b].get(m, 0) for m in PANEL] for b in agg}


def recog_v19(path):
    """brand, panel_model, recognition_yes (0/1) — one row per (brand,model)."""
    agg = {}
    for r in S31.read_csv(path):
        m = r["panel_model"]
        if m in PANEL:
            agg.setdefault(r["brand"], {})[m] = 1 if str(r["recognition_yes"]).strip() == "1" else 0
    return _vec(agg)


def recog_raw(path):
    """v0.20/21/22 Phase A: brand, model, recognized in {yes,no} — 1 row per (brand,model)."""
    agg = {}
    for r in S31.read_csv(path):
        m = r["model"]
        if m in PANEL:
            agg.setdefault(r["brand"], {})[m] = 1 if str(r["recognized"]).strip().lower() == "yes" else 0
    return _vec(agg)


def recog_v23(path):
    """v23 Phase A scored: brand_id, model_id, r_level — normalize to binary (R0 -> 0, else 1)."""
    agg = {}
    levels = set()
    for r in json.load(open(path)):
        m = r.get("model_id")
        if m in PANEL:
            lvl = str(r.get("r_level", "")).strip().upper()
            levels.add(lvl)
            agg.setdefault(r["brand_id"], {})[m] = 0 if lvl in ("", "R0", "NONE") else 1
    return _vec(agg), sorted(levels)


def recognition_vectors():
    out = {}
    out["v0.19"] = recog_v19(V / "v19/phase_a_results.csv")
    out["v0.20"] = recog_raw(V / "v20/phase_a_results.csv")
    out["v0.21"] = recog_raw(V / "v21/phase_a_results.csv")
    out["v0.22"] = recog_raw(V / "v22/phase_a_results.csv")
    v23, v23_levels = recog_v23(V / "v23/data/v23_phase_a_scored.json")
    out["v0.23"] = v23
    return out, v23_levels


# --------------------------------------------------------------------------- #
# reconciliation gate — bit-for-bit per MODEL vs v1.7 r_per_model
# --------------------------------------------------------------------------- #
def reconciliation_gate(recall):
    ref = {(r["substrate"], r["brand"]): json.loads(r["r_per_model"])
           for r in S31.read_csv(V / "methodology/v1_7/data/v1_7_cpc.csv")}
    checked, mism = 0, []
    for k in ("v0.20", "v0.21", "v0.22"):
        counts, _ = recall[k]
        for b, c in counts.items():
            rk = ref.get((k, b))
            if rk is None:
                continue
            checked += 1
            mine = dict(zip(PANEL, [int(v) for v in c]))
            theirs = dict(zip(V17_MODEL_ORDER, [int(v) for v in rk]))
            if any(mine[m] != theirs[m] for m in PANEL):
                mism.append({"substrate": k, "brand": b, "mine_panel_order": list(c),
                             "v1_7_sorted_order": rk})
    return {"checked": checked, "mismatches": mism, "passed": not mism,
            "alignment": "by model name (v1.7 sorted-order vs PANEL order)",
            "scope": "v0.20/0.21/0.22 only; v0.19 & v0.23 have no external anchor (v0.31 provenance)",
            "reference": "osf/methodology/v1_7/data/v1_7_cpc.csv"}


# --------------------------------------------------------------------------- #
# population statistics
# --------------------------------------------------------------------------- #
def mc_pvalue_mean(E, obs_idx, rng):
    """E: (n_brands, 90) eta^2 matrix. Mean-eta^2 one-sided MC p over the per-brand 90-space."""
    n = E.shape[0]
    t_obs = float(E[:, obs_idx].mean())
    idx = rng.integers(0, 90, size=(N_MC, n))
    null_means = E[np.arange(n)[None, :], idx].mean(axis=1)
    p = (int((null_means >= t_obs).sum()) + 1) / (N_MC + 1)
    return t_obs, p, float(null_means.mean()), float(np.quantile(null_means, 0.95))


def mc_pvalue_delta(Ec, Ep, obs_idx, rng):
    """Paired delta = eta^2_CVCPC - eta^2_CP, SAME random assignment to both arms."""
    n = Ec.shape[0]
    d_obs = float((Ec[:, obs_idx] - Ep[:, obs_idx]).mean())
    idx = rng.integers(0, 90, size=(N_MC, n))
    cols = np.arange(n)[None, :]
    null = (Ec[cols, idx] - Ep[cols, idx]).mean(axis=1)
    p = (int((null >= d_obs).sum()) + 1) / (N_MC + 1)
    return d_obs, p, float(null.mean()), float(np.quantile(null, 0.95))


def kendalls_w(rank_matrix):
    """rank_matrix: (k judges/substrates, n items/providers). Ranks 1..n (avg for ties)."""
    k, n = rank_matrix.shape
    Rj = rank_matrix.sum(axis=0)
    S = float(((Rj - Rj.mean()) ** 2).sum())
    return 12.0 * S / (k ** 2 * (n ** 3 - n))


def kendalls_w_exact_p(rank_matrix):
    """Exact null: each of k substrates independently picks one of n! rank perms (6^5=7776)."""
    k, n = rank_matrix.shape
    w_obs = kendalls_w(rank_matrix)
    perms = [np.array(p, float) for p in itertools.permutations(range(1, n + 1))]
    ge = tot = 0
    for combo in itertools.product(perms, repeat=k):
        if kendalls_w(np.array(combo)) >= w_obs - 1e-12:
            ge += 1
        tot += 1
    return w_obs, ge / tot, tot


# --------------------------------------------------------------------------- #
def main():
    rng = np.random.default_rng(SEED)
    print("=" * 80)
    print("v0.33 — Provider-Asymmetric CPC — lock v0.33-prereg-r1 (re-analysis, no acquisition)")
    print("=" * 80)

    recall = recall_counts()
    recog, v23_levels = recognition_vectors()

    # ---- STEP 0: reconciliation gate ----------------------------------------
    gate = reconciliation_gate(recall)
    print(f"\nSTEP 0  reconciliation gate (v0.20/21/22 recall == v1.7 r_per_model, by model)")
    print(f"        checked {gate['checked']} brands | mismatches {len(gate['mismatches'])} | "
          f"{'PASS' if gate['passed'] else 'FAIL'}")
    if not gate["passed"]:
        out = ROOT / "osf/v33"; out.mkdir(parents=True, exist_ok=True)
        json.dump({"reconciliation_gate": gate}, open(out / "v33_gate_FAILED.json", "w"), indent=2)
        print("        GATE FAILED — computational-reproducibility issue. HALTING; no scoring.")
        sys.exit(1)

    # ---- assemble per-brand arms (align recall & recognition by brand key) --
    brands = []   # list of dicts: substrate, brand, cell, recall[6], recog[6], mean_r, defined
    for k in OMNI_ORDER:
        rc_counts, cell_of = recall[k]
        rg = recog[k]
        missing = [b for b in rc_counts if b not in rg]
        if missing:
            raise SystemExit(f"{k}: {len(missing)} recall brands absent from recognition "
                             f"({missing[:5]}). Phase A/B brand-key misalignment — resolve before scoring.")
        for b, c in rc_counts.items():
            mean_r = float(np.mean(c))
            brands.append({"substrate": k, "brand": b, "cell": cell_of.get(b, ""),
                           "recall": list(map(float, c)), "recog": list(map(float, rg[b])),
                           "mean_r": mean_r, "defined": mean_r >= FLOOR})
    assert len(brands) == 112, f"expected 112 brand units, got {len(brands)}"

    # per-brand eta^2 matrices over the 90-space
    Ec = np.array([eta2_vector(d["recall"]) for d in brands])     # CV-CPC arm
    Ep = np.array([eta2_vector(d["recog"]) for d in brands])      # C_P arm
    for d, ec, ep in zip(brands, Ec, Ep):
        d["eta2_cvcpc"] = float(ec[OBS_IDX]); d["eta2_cp"] = float(ep[OBS_IDX])

    # ---- H_Provider_Asymmetry (PRIMARY) — mean eta^2 over all 112 ------------
    t_obs, p_asym, null_mean, null_q95 = mc_pvalue_mean(Ec, OBS_IDX, rng)
    H_asym = "CONFIRMED" if p_asym < 0.05 else "FALSIFIED"
    per_sub_eta = {k: float(np.mean([d["eta2_cvcpc"] for d in brands if d["substrate"] == k]))
                   for k in OMNI_ORDER}

    # ---- H_Provider_Beyond_Presence (PRIMARY gate) — paired delta, above-floor
    af = [i for i, d in enumerate(brands) if d["defined"]]
    Ec_af, Ep_af = Ec[af], Ep[af]
    d_obs, p_delta, dnull_mean, dnull_q95 = mc_pvalue_delta(Ec_af, Ep_af, OBS_IDX, rng)
    H_beyond = "CONFIRMED" if (d_obs > 0 and p_delta < 0.05) else "FALSIFIED"
    mean_eta_cp_af = float(Ep_af[:, OBS_IDX].mean())
    mean_eta_cv_af = float(Ec_af[:, OBS_IDX].mean())

    # ---- LOSO robustness on PRIMARY (mean eta^2) ----------------------------
    loso = {}
    for k in OMNI_ORDER:
        keep = [i for i, d in enumerate(brands) if d["substrate"] != k]
        rng_l = np.random.default_rng(SEED + 1 + OMNI_ORDER.index(k))
        t, p, _, _ = mc_pvalue_mean(Ec[keep], OBS_IDX, rng_l)
        loso[k] = {"left_out": k, "n_brands": len(keep), "mean_eta2": t, "p": p,
                   "significant": p < 0.05}
    loso_survives = all(v["significant"] for v in loso.values())
    if H_asym == "CONFIRMED" and not loso_survives:
        H_asym_final = "UNDETERMINED (fragile under LOSO)"
    else:
        H_asym_final = H_asym

    # ---- H_Provider_Ordinal (SECONDARY) — within-pair consistency, Kendall W -
    def within_pair_consistency(substrate):
        rows = [d for d in brands if d["substrate"] == substrate]
        out = {}
        for prov, (i, j) in PROVIDERS.items():
            agree = np.mean([1.0 - abs(d["recall"][i] - d["recall"][j]) / N_FRAMES for d in rows])
            out[prov] = float(agree)
        return out
    cons = {k: within_pair_consistency(k) for k in OMNI_ORDER}
    provs = list(PROVIDERS.keys())
    # rank providers within each substrate (1 = most consistent); avg ranks for ties
    rank_mat = np.array([stats.rankdata([-cons[k][p] for p in provs], method="average")
                         for k in OMNI_ORDER])
    W_obs, W_p, W_tot = kendalls_w_exact_p(rank_mat)
    H_ord = "CONFIRMED" if W_p < 0.05 else "UNINFORMATIVE (n.s.; N=5 underpowered)"

    # ---- H_Provider_Phantom (TERTIARY, descriptive) -------------------------
    below = [d["eta2_cvcpc"] for d in brands if not d["defined"]]
    above = [d["eta2_cvcpc"] for d in brands if d["defined"]]
    phantom = {"n_below_floor": len(below), "n_above_floor": len(above),
               "mean_eta2_below": (float(np.mean(below)) if below else None),
               "mean_eta2_above": (float(np.mean(above)) if above else None),
               "note": "descriptive only; no confirmatory threshold (exploratory)"}
    if below and above:
        mw = stats.mannwhitneyu(below, above, alternative="two-sided")
        phantom["descriptive_mwu_p"] = float(mw.pvalue)

    # ---- v0.18 walled concordance aside (3-frame geometry) ------------------
    v18_counts, v18_cell = S31.counts_v18(V / "v18/data/phase_b_results.json")
    v18_eta = [eta2_for(c, OBS_ASSIGNMENT) for c in v18_counts.values()]
    v18_cons = {}
    for prov, (i, j) in PROVIDERS.items():
        v18_cons[prov] = float(np.mean([1.0 - abs(c[i] - c[j]) / 3.0 for c in v18_counts.values()]))
    omni_prov_order = sorted(provs, key=lambda p: np.mean([cons[k][p] for k in OMNI_ORDER]), reverse=True)
    v18_prov_order = sorted(provs, key=lambda p: v18_cons[p], reverse=True)
    v18 = {"n_brands": len(v18_counts), "mean_eta2_cvcpc_3frame": float(np.mean(v18_eta)),
           "provider_consistency_rank": v18_prov_order, "omnibus_provider_rank": omni_prov_order,
           "rank_order_agrees": v18_prov_order == omni_prov_order,
           "note": "WALLED — 3-frame geometry non-comparable; directional concordance only, "
                   "not pooled into PRIMARY/delta/Kendall"}

    # ---- write per-brand CSV ------------------------------------------------
    out_dir = ROOT / "osf/v33"; (out_dir / "data").mkdir(parents=True, exist_ok=True)
    with open(out_dir / "data" / "v33_eta2.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["substrate", "brand", "cell", "mean_r", "defined",
                    "recall_per_model", "recog_per_model", "eta2_cvcpc", "eta2_cp", "delta_eta2"])
        for d in brands:
            w.writerow([d["substrate"], d["brand"], d["cell"], f"{d['mean_r']:.6f}", d["defined"],
                        json.dumps([int(x) for x in d["recall"]]),
                        json.dumps([int(x) for x in d["recog"]]),
                        f"{d['eta2_cvcpc']:.6f}", f"{d['eta2_cp']:.6f}",
                        f"{d['eta2_cvcpc'] - d['eta2_cp']:.6f}"])

    # ---- verdicts JSON ------------------------------------------------------
    verdicts = {
        "phase": "v0.33", "title": "Provider-Asymmetric CPC", "lock": "v0.33-prereg-r1",
        "lock_commit": "c8f2736", "no_new_llm_calls": True, "seed": SEED, "mc_draws": N_MC,
        "panel": PANEL, "provider_groups": {k: [PANEL[i] for i in v] for k, v in PROVIDERS.items()},
        "n_brand_units": len(brands),
        "reconciliation_gate": gate,
        "computation_notes": [
            "Zero-variance convention applied: SS_total==0 -> eta^2:=0 (not excluded).",
            f"v0.23 Phase A recognition is fully saturated (r_level set = {v23_levels}); "
            "binarized all-recognized, so eta^2_CP==0 for all v0.23 brands (zero-variance).",
            "Ordinal within-pair consistency normalized by n_frames (=6 omnibus, =3 v0.18); "
            "SECONDARY/underpowered, reported descriptively.",
            "v0.19 & v0.23 recall recompute has no external anchor (v0.31 provenance only).",
        ],
        "H_Provider_Asymmetry": {
            "tier": "PRIMARY", "verdict": H_asym_final, "verdict_pre_loso": H_asym,
            "mean_eta2_observed": t_obs, "mc_p_onesided": p_asym,
            "null_mean": null_mean, "null_q95": null_q95,
            "per_substrate_mean_eta2": per_sub_eta, "n_brands": len(brands)},
        "H_Provider_Beyond_Presence": {
            "tier": "PRIMARY (gate)", "verdict": H_beyond,
            "delta_eta2_observed": d_obs, "mc_p_onesided": p_delta,
            "mean_eta2_cvcpc_abovefloor": mean_eta_cv_af, "mean_eta2_cp_abovefloor": mean_eta_cp_af,
            "null_mean": dnull_mean, "null_q95": dnull_q95, "n_abovefloor": len(af)},
        "H_Provider_Ordinal": {
            "tier": "SECONDARY (underpowered N=5)", "verdict": H_ord,
            "kendalls_w": W_obs, "exact_p": W_p, "exact_null_size": W_tot,
            "within_pair_consistency": cons,
            "provider_rank_table": {k: {p: int(r) for p, r in zip(provs, rank_mat[i])}
                                    for i, k in enumerate(OMNI_ORDER)}},
        "H_Provider_Phantom": {"tier": "TERTIARY (exploratory, walled)", **phantom},
        "v0_18_concordance_aside": v18,
        "loso": {"survives_all": loso_survives, "per_leftout": loso},
        "deviations": [],
    }
    json.dump(verdicts, open(out_dir / "v33_provider_asymmetry_verdicts.json", "w"), indent=2)

    # ---- console summary ----------------------------------------------------
    print(f"\nbrand units: {len(brands)} (v19=16, v20/21/22/23=24)  | above-floor: {len(af)}")
    print(f"\nPRIMARY  H_Provider_Asymmetry      : {H_asym_final}")
    print(f"         mean eta^2 = {t_obs:.4f}  (null mean {null_mean:.4f}, q95 {null_q95:.4f})  "
          f"MC p = {p_asym:.4g}")
    print("         per-substrate mean eta^2: " + "  ".join(f"{k}={per_sub_eta[k]:.3f}" for k in OMNI_ORDER))
    print(f"         LOSO survives all 5: {loso_survives}  " +
          " ".join(f"[{k}:p={loso[k]['p']:.3g}]" for k in OMNI_ORDER))
    print(f"\nPRIMARY  H_Provider_Beyond_Presence : {H_beyond}   (the substantive gate)")
    print(f"         delta_eta2 = {d_obs:+.4f}  (eta2_CVCPC {mean_eta_cv_af:.4f} - eta2_CP {mean_eta_cp_af:.4f})  "
          f"MC p = {p_delta:.4g}")
    print(f"\nSECONDARY H_Provider_Ordinal        : {H_ord}")
    print(f"         Kendall's W = {W_obs:.4f}  exact p = {W_p:.4g}  (null {W_tot})")
    for k in OMNI_ORDER:
        print(f"           {k} {CAT[k]:<22} " +
              "  ".join(f"{p}={cons[k][p]:.3f}(r{int(rank_mat[OMNI_ORDER.index(k)][provs.index(p)])})" for p in provs))
    print(f"\nTERTIARY H_Provider_Phantom (descr.): below-floor n={phantom['n_below_floor']} "
          f"mean_eta2={phantom['mean_eta2_below']}  | above n={phantom['n_above_floor']} "
          f"mean_eta2={phantom['mean_eta2_above']:.4f}")
    print(f"\nv0.18 aside (walled)               : mean eta^2(3-frame)={v18['mean_eta2_cvcpc_3frame']:.4f}  "
          f"rank agrees with omnibus: {v18['rank_order_agrees']}")
    print(f"\nreconciliation gate                : PASS ({gate['checked']} brands, bit-for-bit by model)")
    print(f"wrote: {out_dir/'v33_provider_asymmetry_verdicts.json'}")
    print(f"wrote: {out_dir/'data'/'v33_eta2.csv'}")
    return verdicts


if __name__ == "__main__":
    main()
