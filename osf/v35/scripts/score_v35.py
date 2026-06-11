#!/usr/bin/env python3
"""
score_v35.py -- v0.35 Naive-Phantom x CPC Omnibus scorer.

Locked against v0.35-prereg-r1 (commit 8b254f2). Re-analysis; NO new LLM acquisition.

Question: do phantom-flagged brands carry a distinct CV-CPC consistency signature
beyond mere Presence/recall? The phase's inferential weight rests ENTIRELY on the
gating hypothesis (H_Phantom_Beyond_Presence, co-primary C_P and recall-mean controls
with a flip rule). The raw arm (H_Phantom_CPC_Signature) is a MANIPULATION CHECK only:
both sides are recall-coupled by construction (flag from recall-floor; metric from
recall-mean), so a raw CONFIRMED merely shows the pipeline reproduces the known
mechanical coupling.

Inputs (frozen t1; recomputed via the identical locked extraction v0.33/v0.34 use):
  CV-CPC = 1/(1+CV), CV = sd_pop/mean of the 6-model per-brand RECALL vector (ddof=0,
           per score_v0_31). Characterization quantity, NOT an adopted instrument:
           computed for EVERY non-all-zero unit (incl. below the v1.7 FLOOR=1.0, which
           governs adoption only). All-zero recall (mean==0 -> CV undefined) excluded.
  C_P    = recognition count (sum of 6-model binary recognition), 0..6.
  Phantom flag = status=="undefined" in osf/v31/data/v31_cpc.csv == mean_r < FLOOR
           (frozen v0.31 archive flags; identical to v0.33 H_Provider_Phantom and the
           v0.34 t1 phantom set). Provenance only; v1.6 method anchor.

STEP 1 reconciliation gate (binding; HALT on any mismatch):
  (a) re-extracted recall/recog reproduce the v0.33 deposit (osf/v33/data/v33_eta2.csv)
      bit-for-bit (sha256, per substrate);
  (b) v0.20/0.21/0.22 recall reconcile to v1.7 r_per_model by model name (reused from
      score_v33; scope = those three phases only);
  (c) phantom flag (status=="undefined") == (mean_r < FLOOR) for every unit.

Estimand resolutions (genuine judgment calls -> contemporaneous DEVIATIONS; see
osf/v35/scripts/v35_scoring_methods_log.md):
  D1 pooled Cliff's delta = stratum-pooled over WITHIN-substrate cross pairs only
     (pair-count weighted); the observed statistic respects strata (permutation
     exchangeability). Not strata-ignoring all-pairs.
  D2 rank-residualization fit over ALL analyzable units (phantom + non-phantom), so the
     residual carries the contrast.
  D3 cross-substrate per-substrate delta = the RAW arm (CV-CPC), not residualized.
"""
import sys, json, csv, hashlib
from pathlib import Path

import numpy as np
from scipy import stats

ROOT = Path.home() / "aias"
sys.path.insert(0, str(ROOT / "prereg"))
sys.path.insert(0, str(ROOT / "scripts"))

import v0_35_phantom_cpc_omnibus_content as PRE   # locked methodology (+ commit guard)
import score_v0_31 as S31                         # RECALL extractors (provenance lock)
import score_v33 as S33                           # recall_counts/recognition_vectors + v1.7 gate
import score_v34 as S34                           # wave_t2 (t2 inputs)

PANEL = S31.PANEL
FLOOR = 1.0
N_MC = 10_000
SEED = 280400
OMNI = ["v0.19", "v0.20", "v0.21", "v0.22", "v0.23"]
V = ROOT / "osf"
OUT = ROOT / "osf" / "v35"
LOCK_COMMIT = "8b254f2"

# Derived RNG seeds (documented in the methods log) -- one per statistic so each null is
# independent of execution order / future reordering.
RNG = {"raw": SEED, "gate_cp": SEED + 10, "gate_rm": SEED + 20, "t2": SEED + 30}
LOSO_RAW_BASE = SEED + 1          # + substrate index  (score_v33 LOSO idiom)
LOSO_GATE_BASE = SEED + 40        # + substrate index


# --------------------------------------------------------------------------- #
# metrics
# --------------------------------------------------------------------------- #
def cv_cpc(recall):
    """1/(1+CV), CV = sd_pop/mean (ddof=0). None iff all-zero (mean==0)."""
    x = np.asarray(recall, float)
    m = x.mean()
    if m <= 0.0:
        return None
    return 1.0 / (1.0 + x.std(ddof=0) / m)


def c_p(recog):
    return int(sum(int(v) for v in recog))


# --------------------------------------------------------------------------- #
# STEP 1 -- reconciliation gate
# --------------------------------------------------------------------------- #
def _hash_vectors(vmap):
    """Deterministic sha256 over brand-sorted (brand, int-vector) pairs."""
    h = hashlib.sha256()
    for b in sorted(vmap):
        h.update(b.encode("utf-8"))
        h.update(b"|")
        h.update(",".join(str(int(x)) for x in vmap[b]).encode("utf-8"))
        h.update(b";")
    return h.hexdigest()


def reconciliation_gate(recall, recog):
    dep_recall, dep_recog = {}, {}
    for r in S31.read_csv(V / "v33/data/v33_eta2.csv"):
        dep_recall.setdefault(r["substrate"], {})[r["brand"]] = json.loads(r["recall_per_model"])
        dep_recog.setdefault(r["substrate"], {})[r["brand"]] = json.loads(r["recog_per_model"])

    per_sub, all_pass = {}, True
    for s in OMNI:
        counts, _ = recall[s]
        rg = recog[s]
        mine_recall = {b: [int(x) for x in counts[b]] for b in counts}
        mine_recog = {b: [int(x) for x in rg[b]] for b in counts}
        dep_r = {b: [int(x) for x in dep_recall[s][b]] for b in dep_recall.get(s, {})}
        dep_g = {b: [int(x) for x in dep_recog[s][b]] for b in dep_recog.get(s, {})}
        hr_m, hr_d = _hash_vectors(mine_recall), _hash_vectors(dep_r)
        hg_m, hg_d = _hash_vectors(mine_recog), _hash_vectors(dep_g)
        mism = []
        for b in mine_recall:
            if mine_recall[b] != dep_r.get(b):
                mism.append({"brand": b, "arm": "recall", "mine": mine_recall[b], "deposit": dep_r.get(b)})
            if mine_recog[b] != dep_g.get(b):
                mism.append({"brand": b, "arm": "recog", "mine": mine_recog[b], "deposit": dep_g.get(b)})
        rmatch, gmatch = (hr_m == hr_d), (hg_m == hg_d)
        per_sub[s] = {"n": len(counts),
                      "recall_sha256_consumed": hr_m, "recall_sha256_deposit": hr_d, "recall_match": rmatch,
                      "recog_sha256_consumed": hg_m, "recog_sha256_deposit": hg_d, "recog_match": gmatch,
                      "mismatches": mism}
        all_pass = all_pass and rmatch and gmatch

    v17 = S33.reconciliation_gate(recall)            # v0.20/21/22 vs v1.7 r_per_model, by model
    all_pass = all_pass and v17["passed"]
    return {"v33_deposit": per_sub, "v17_anchor": v17, "passed": all_pass}, all_pass


def write_reconciliation_log(gate, flag_check):
    OUT.joinpath("data").mkdir(parents=True, exist_ok=True)
    lines = []
    lines.append("v0.35 RECONCILIATION GATE LOG  (lock v0.35-prereg-r1 @ %s)" % LOCK_COMMIT)
    lines.append("=" * 78)
    lines.append("Binding gate; run after lock and before any contrast. ANY mismatch halts the phase.")
    lines.append("")
    lines.append("(a) Bit-for-bit vs v0.33 deposit (osf/v33/data/v33_eta2.csv), sha256 per substrate")
    lines.append("    over brand-sorted consumed per-model RECALL and RECOGNITION vectors.")
    lines.append("-" * 78)
    for s in OMNI:
        d = gate["v33_deposit"][s]
        lines.append(f"  {s}  n={d['n']}")
        lines.append(f"    recall  consumed {d['recall_sha256_consumed']}")
        lines.append(f"            deposit  {d['recall_sha256_deposit']}   match={d['recall_match']}")
        lines.append(f"    recog   consumed {d['recog_sha256_consumed']}")
        lines.append(f"            deposit  {d['recog_sha256_deposit']}   match={d['recog_match']}")
        if d["mismatches"]:
            for m in d["mismatches"]:
                lines.append(f"    MISMATCH {m}")
    lines.append("")
    lines.append("(b) v1.7 anchor: v0.20/0.21/0.22 recall == v1.7 r_per_model (by model name).")
    lines.append("    scope = those three phases only; v0.19 & v0.23 rest on v0.31 provenance.")
    lines.append("-" * 78)
    v17 = gate["v17_anchor"]
    lines.append(f"    checked={v17['checked']}  mismatches={len(v17['mismatches'])}  passed={v17['passed']}")
    lines.append(f"    reference={v17['reference']}")
    for m in v17["mismatches"]:
        lines.append(f"    MISMATCH {m}")
    lines.append("")
    lines.append("(c) Phantom-flag consistency: status=='undefined' (v31_cpc.csv) == (mean_r < FLOOR).")
    lines.append("-" * 78)
    lines.append(f"    units checked={flag_check['checked']}  disagreements={len(flag_check['disagreements'])}")
    for m in flag_check["disagreements"]:
        lines.append(f"    DISAGREE {m}")
    lines.append("")
    lines.append("=" * 78)
    lines.append("RESULT: %s" % ("PASS" if (gate["passed"] and not flag_check["disagreements"]) else "HALT"))
    OUT.joinpath("data", "v35_reconciliation_log.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


# --------------------------------------------------------------------------- #
# STEP 2 -- units + phantom enumeration
# --------------------------------------------------------------------------- #
def load_v31():
    """Frozen v0.31 archive: (substrate,brand) -> {mean_r, sd_pop, status, cpc_score}."""
    out = {}
    for r in S31.read_csv(V / "v31/data/v31_cpc.csv"):
        if r["set"] != "omnibus" or r["substrate"] not in OMNI:
            continue
        cps = r["cpc_score"].strip()
        out[(r["substrate"], r["brand"])] = {
            "mean_r": float(r["mean_r"]), "sd_pop": float(r["sd_pop"]), "status": r["status"],
            "cpc_score": (float(cps) if cps else None)}
    return out


def build_units(recall, recog, v31):
    """112 per-unit dicts with metric, phantom flag, analyzability. Asserts provenance."""
    units = []
    flag_check = {"checked": 0, "disagreements": []}
    cpc_xcheck = {"checked": 0, "max_abs_err": 0.0}
    for s in OMNI:
        counts, cell = recall[s]
        rg = recog[s]
        for b in counts:
            rv = [int(x) for x in counts[b]]
            gv = [int(x) for x in rg[b]]
            mean_r = float(np.mean(rv))
            key = (s, b)
            if key not in v31:
                raise SystemExit(f"v0.35 HALT: {key} absent from v31_cpc.csv (provenance gap).")
            status = v31[key]["status"]
            phantom = (status == "undefined")
            flag_check["checked"] += 1
            if phantom != (mean_r < FLOOR):
                flag_check["disagreements"].append(
                    {"key": list(key), "status": status, "mean_r": mean_r})
            cc = cv_cpc(rv)
            # cross-check: defined-unit CV-CPC reproduces the frozen cpc_score
            if v31[key]["cpc_score"] is not None and cc is not None:
                cpc_xcheck["checked"] += 1
                cpc_xcheck["max_abs_err"] = max(cpc_xcheck["max_abs_err"],
                                                abs(cc - v31[key]["cpc_score"]))
            units.append({
                "substrate": s, "brand": b, "cell": cell.get(b, ""),
                "recall": rv, "recog": gv, "mean_r": mean_r,
                "sd_pop": float(np.std(rv, ddof=0)), "cv_cpc": cc, "c_p": c_p(gv),
                "status": status, "phantom": phantom,
                "all_zero": mean_r <= 0.0, "analyzable": phantom and mean_r > 0.0})
    assert len(units) == 112, f"expected 112 units, got {len(units)}"
    return units, flag_check, cpc_xcheck


def enumerate_roster(units):
    """Per-substrate flagged/analyzable/excluded counts + eligibility; writes roster CSV."""
    roster = {s: {"flagged": 0, "analyzable": 0, "excluded_allzero": 0, "non_phantom": 0} for s in OMNI}
    rows = []
    for u in units:
        s = u["substrate"]
        if u["phantom"]:
            roster[s]["flagged"] += 1
            if u["analyzable"]:
                roster[s]["analyzable"] += 1
                grp, reason = "phantom_analyzable", ""
            else:
                roster[s]["excluded_allzero"] += 1
                grp, reason = "phantom_excluded", "all_zero_recall_undefined_cv"
        else:
            roster[s]["non_phantom"] += 1
            grp, reason = "non_phantom", "comparison_group"
        rows.append({"brand": u["brand"], "substrate": s,
                     "mean_r": f"{u['mean_r']:.6f}",
                     "cv_cpc": ("" if u["cv_cpc"] is None else f"{u['cv_cpc']:.6f}"),
                     "c_p": u["c_p"], "status": u["status"],
                     "flagged": u["phantom"], "analyzable": u["analyzable"],
                     "group": grp, "exclusion_reason": reason})
    for s in OMNI:
        roster[s]["eligible_ge4"] = roster[s]["analyzable"] >= 4
        roster[s]["brands"] = sum((roster[s][k] for k in ("flagged", "non_phantom")))
    OUT.joinpath("data").mkdir(parents=True, exist_ok=True)
    with open(OUT / "data" / "v35_phantom_roster.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["brand", "substrate", "mean_r", "cv_cpc", "c_p", "status",
                                          "flagged", "analyzable", "group", "exclusion_reason"])
        w.writeheader()
        for r in sorted(rows, key=lambda r: (OMNI.index(r["substrate"]), not r["flagged"], r["brand"])):
            w.writerow(r)
    return roster


# --------------------------------------------------------------------------- #
# STEP 3 -- Cliff's delta + within-substrate stratified permutation
# --------------------------------------------------------------------------- #
def cliffs_delta_obs(values, labels, strata):
    """Pooled delta over WITHIN-substrate cross pairs (D1). label True == phantom (group1).
    Returns (pooled_delta, denominator, {substrate: per_substrate_delta})."""
    vals = np.asarray(values, float)
    num = den = 0
    per = {}
    for s in OMNI:
        idx = [i for i in range(len(vals)) if strata[i] == s]
        p = vals[[i for i in idx if labels[i]]]
        n = vals[[i for i in idx if not labels[i]]]
        if len(p) == 0 or len(n) == 0:
            per[s] = None
            continue
        g = int((p[:, None] > n[None, :]).sum() - (p[:, None] < n[None, :]).sum())
        num += g
        den += len(p) * len(n)
        per[s] = g / (len(p) * len(n))
    return (num / den if den else float("nan")), den, per


def stratified_perm_p(values, labels, strata, delta_obs, rng, n_mc=N_MC):
    """Two-sided p. Each draw: permute labels within each substrate (fixed per-stratum
    phantom count), recompute pooled delta. p = (1 + #{|d_perm| >= |d_obs|}) / (n_mc+1)."""
    vals = np.asarray(values, float)
    by_sub = {s: [i for i in range(len(vals)) if strata[i] == s] for s in OMNI}
    nph = {s: sum(1 for i in by_sub[s] if labels[i]) for s in OMNI}
    # constant denominator (fixed per-stratum counts)
    den = sum(nph[s] * (len(by_sub[s]) - nph[s]) for s in OMNI)
    if den == 0 or not np.isfinite(delta_obs):
        return float("nan"), np.array([])
    abs_obs = abs(delta_obs)
    null = np.empty(n_mc)
    ge = 0
    for d in range(n_mc):
        num = 0
        for s in OMNI:
            idx = by_sub[s]
            k = nph[s]
            if k == 0 or k == len(idx):
                continue
            perm = rng.permutation(idx)
            p = vals[perm[:k]]
            n = vals[perm[k:]]
            num += int((p[:, None] > n[None, :]).sum() - (p[:, None] < n[None, :]).sum())
        dd = num / den
        null[d] = dd
        if abs(dd) >= abs_obs - 1e-12:
            ge += 1
    return (ge + 1) / (n_mc + 1), null


def verdict(delta, p, lo=0.15, hi=0.30, mech_sign=-1):
    """Mechanism predicts phantoms LOWER CV-CPC -> delta<0 (mech_sign=-1).
    Opposite-direction significance falsifies the mechanism-signature claim (checked first)."""
    if not np.isfinite(delta) or not np.isfinite(p):
        return "UNDEFINED"
    opposite = (delta * mech_sign < 0)          # delta>0 == phantoms HIGHER
    if opposite and p < 0.05:
        return "FALSIFIED"
    if abs(delta) < lo:
        return "FALSIFIED"
    if abs(delta) >= hi and p < 0.05:
        return "CONFIRMED"
    return "MARGINAL"


def rank_residualize(subset, covariate_key):
    """Within each substrate: residuals of rank(CV-CPC) ~ rank(covariate) (avg-tie ranks,
    OLS). Zero rank-variance covariate or n<3 -> centered ranks (no-op). Order-aligned list."""
    resid = [None] * len(subset)
    by_sub = {}
    for i, u in enumerate(subset):
        by_sub.setdefault(u["substrate"], []).append(i)
    for s, idxs in by_sub.items():
        y = np.array([subset[i]["cv_cpc"] for i in idxs], float)
        x = np.array([subset[i][covariate_key] for i in idxs], float)
        ry = stats.rankdata(y, method="average")
        rx = stats.rankdata(x, method="average")
        if len(idxs) < 3 or np.ptp(rx) == 0:
            r = ry - ry.mean()
        else:
            A = np.vstack([rx, np.ones_like(rx)]).T
            coef, *_ = np.linalg.lstsq(A, ry, rcond=None)
            r = ry - A @ coef
        for j, i in enumerate(idxs):
            resid[i] = float(r[j])
    return resid


def analyzable_subset(units):
    """Analyzable contrast set: non-phantoms (all have CV-CPC) + analyzable phantoms."""
    return [u for u in units if (not u["phantom"]) or u["analyzable"]]


def run_contrast(subset, values, rng, lo=0.15, hi=0.30):
    labels = [u["phantom"] for u in subset]
    strata = [u["substrate"] for u in subset]
    d, den, per = cliffs_delta_obs(values, labels, strata)
    p, _ = stratified_perm_p(values, labels, strata, d, rng)
    return {"delta": d, "p": p, "verdict": verdict(d, p, lo, hi),
            "n": len(subset), "n_pairs": den, "per_substrate_delta": per}


def gate_arm(subset, covariate_key, rng):
    resid = rank_residualize(subset, covariate_key)
    res = run_contrast(subset, resid, rng)
    # saturation diagnostics per substrate (evidence for collapse of the C_P control)
    sat = {}
    for s in OMNI:
        cov = [u[covariate_key] for u in subset if u["substrate"] == s]
        sat[s] = {"n": len(cov), "covariate_constant": (len(set(cov)) <= 1)}
    res["covariate"] = covariate_key
    res["per_substrate_covariate_constant"] = {s: sat[s]["covariate_constant"] for s in OMNI}
    res["delta_resid"] = res.pop("delta")
    return res


# --------------------------------------------------------------------------- #
# hypotheses
# --------------------------------------------------------------------------- #
def h_raw(units):
    rng = np.random.default_rng(RNG["raw"])
    sub = analyzable_subset(units)
    vals = [u["cv_cpc"] for u in sub]
    r = run_contrast(sub, vals, rng)
    n_ph = sum(1 for u in sub if u["phantom"])
    return {
        "tier": "PRIMARY (raw arm; manipulation check)",
        "verdict": r["verdict"],
        "cliffs_delta": r["delta"], "mc_p_twosided": r["p"],
        "n_phantom_analyzable": n_ph, "n_nonphantom": len(sub) - n_ph,
        "n_within_substrate_pairs": r["n_pairs"],
        "per_substrate_delta": r["per_substrate_delta"],
        "mechanistic_annotation": "mechanism predicts phantoms LOWER CV-CPC (delta<0); descriptive only",
        "inferential_weight": "manipulation check only -- both arms recall-coupled by construction; "
                              "the phase's inferential claim rests on the gate",
        "_per_sub_delta": r["per_substrate_delta"], "_subset": sub,
    }


def h_gate(units):
    sub = analyzable_subset(units)
    cp = gate_arm(sub, "c_p", np.random.default_rng(RNG["gate_cp"]))
    rm = gate_arm(sub, "mean_r", np.random.default_rng(RNG["gate_rm"]))
    flip = cp["verdict"] != rm["verdict"]
    gate_verdict = "UNDETERMINED (control flip)" if flip else cp["verdict"]
    return {
        "tier": "PRIMARY (gating)",
        "verdict": gate_verdict,
        "control_flip": flip,
        "directional_lean": "FALSIFIED-or-marginal (rho=0.77 Presence-coupling, v1.7)",
        "control_C_P": {"verdict": cp["verdict"], "delta_resid": cp["delta_resid"], "mc_p_twosided": cp["p"],
                        "per_substrate_delta": cp["per_substrate_delta"],
                        "per_substrate_covariate_constant": cp["per_substrate_covariate_constant"]},
        "control_recall_mean": {"verdict": rm["verdict"], "delta_resid": rm["delta_resid"], "mc_p_twosided": rm["p"],
                                "per_substrate_delta": rm["per_substrate_delta"],
                                "per_substrate_covariate_constant": rm["per_substrate_covariate_constant"]},
        "n": cp["n"],
        "finding_note": ("control flip IS the finding; gate UNDETERMINED, routed to v1.8" if flip
                         else "both controls agree; gate verdict stable across C_P and recall-mean"),
        "_subset": sub,
    }


def h_cross_substrate(units, raw_per_sub, roster):
    eligible = [s for s in OMNI if roster[s]["analyzable"] >= 4]
    signs = []
    for s in eligible:
        d = raw_per_sub.get(s)
        signs.append(0 if (d is None or d == 0) else (1 if d > 0 else -1))
    neg = sum(1 for x in signs if x < 0)
    pos = sum(1 for x in signs if x > 0)
    n = neg + pos
    k = max(neg, pos)
    if n > 0:
        bt = stats.binomtest(k, n, 0.5, alternative="two-sided")
        p = float(bt.pvalue)
    else:
        p = float("nan")
    if np.isfinite(p) and p < 0.05:
        v = "CONFIRMED"
    else:
        v = f"UNINFORMATIVE (n.s.; underpowered N={len(eligible)}; {k}/{n} concordant, p={p:.3f})"
    return {
        "tier": "SECONDARY (underpowered; per spec)",
        "verdict": v,
        "eligible_substrates": eligible,
        "per_substrate_delta_all": {s: raw_per_sub.get(s) for s in OMNI},
        "signs_eligible": {s: sg for s, sg in zip(eligible, signs)},
        "n_negative": neg, "n_positive": pos, "binomial_p_twosided": p,
        "note": "raw-arm (CV-CPC) per-substrate delta (D3). Exact binomial sign test on eligible "
                "(>=4 analyzable) substrates only; full 5-substrate table reported regardless. "
                "4 substrates cannot reach p<0.05 even at 4/4 (structural underpower).",
    }


def h_t2_stability(units):
    """TERTIARY, walled, descriptive. Same pooled contrasts on the v0.34 t2 wave; phantom
    membership FROZEN at t1; CV-CPC recomputed from t2 recall. No verdict thresholds."""
    rng = np.random.default_rng(RNG["t2"])
    t2 = S34.wave_t2()
    t2u = []
    missing = 0
    for u in units:
        s, b = u["substrate"], u["brand"]
        if b not in t2[s]:
            missing += 1
            continue
        rv = [int(x) for x in t2[s][b]["recall"]]
        gv = [int(x) for x in t2[s][b]["recog"]]
        mean_r = float(np.mean(rv))
        t2u.append({"substrate": s, "brand": b, "phantom": u["phantom"],
                    "cv_cpc": cv_cpc(rv), "mean_r": mean_r, "c_p": c_p(gv),
                    "all_zero": mean_r <= 0.0,
                    "analyzable": u["phantom"] and mean_r > 0.0})
    sub = [u for u in t2u if u["cv_cpc"] is not None and ((not u["phantom"]) or u["analyzable"])]
    vals = [u["cv_cpc"] for u in sub]
    raw = run_contrast(sub, vals, rng)
    cp = gate_arm(sub, "c_p", rng)
    rm = gate_arm(sub, "mean_r", rng)
    n_ph = sum(1 for u in sub if u["phantom"])
    return {
        "tier": "TERTIARY (exploratory; WALLED; descriptive only)",
        "verdict": "DESCRIPTIVE",
        "wall_note": "test-retest stability check on the v0.34 t2 near-replica panel "
                     "(0.98 phantom persistence); NO independence claimed; quarantined from all "
                     "PRIMARY/SECONDARY verdict logic; no confirmatory thresholds applied.",
        "membership": "phantom flag frozen at t1; CV-CPC recomputed from t2 recall",
        "raw_arm": {"cliffs_delta": raw["delta"], "mc_p_twosided": raw["p"],
                    "n_phantom_analyzable": n_ph, "n_nonphantom": len(sub) - n_ph,
                    "per_substrate_delta": raw["per_substrate_delta"]},
        "gate_control_C_P": {"delta_resid": cp["delta_resid"], "mc_p_twosided": cp["p"]},
        "gate_control_recall_mean": {"delta_resid": rm["delta_resid"], "mc_p_twosided": rm["p"]},
        "t1_units_absent_from_t2": missing,
    }


# --------------------------------------------------------------------------- #
# sensitivity
# --------------------------------------------------------------------------- #
def loso_raw(units, full_verdict):
    sub_all = analyzable_subset(units)
    out = {}
    for i, s in enumerate(OMNI):
        keep = [u for u in sub_all if u["substrate"] != s]
        vals = [u["cv_cpc"] for u in keep]
        r = run_contrast(keep, vals, np.random.default_rng(LOSO_RAW_BASE + i))
        out[s] = {"left_out": s, "delta": r["delta"], "p": r["p"], "verdict": r["verdict"], "n": len(keep)}
    survives = all(v["verdict"] == full_verdict for v in out.values())
    return {"survives_all": survives, "per_leftout": out,
            "full_verdict": full_verdict,
            "fragile": (full_verdict == "CONFIRMED" and not survives)}


def loso_gate(units, full_gate_verdict):
    sub_all = analyzable_subset(units)
    out = {}
    for i, s in enumerate(OMNI):
        keep = [u for u in sub_all if u["substrate"] != s]
        cp = gate_arm(keep, "c_p", np.random.default_rng(LOSO_GATE_BASE + i))
        rm = gate_arm(keep, "mean_r", np.random.default_rng(LOSO_GATE_BASE + 100 + i))
        flip = cp["verdict"] != rm["verdict"]
        gv = "UNDETERMINED (control flip)" if flip else cp["verdict"]
        out[s] = {"left_out": s, "verdict": gv, "control_flip": flip,
                  "delta_resid_C_P": cp["delta_resid"], "p_C_P": cp["p"],
                  "delta_resid_recall_mean": rm["delta_resid"], "p_recall_mean": rm["p"], "n": len(keep)}
    survives = all(v["verdict"] == full_gate_verdict for v in out.values())
    return {"survives_all": survives, "per_leftout": out, "full_verdict": full_gate_verdict,
            "fragile": not survives}


def threshold_reruns(raw, gate):
    """Descriptive: re-decide PRIMARY verdicts at CONFIRMED magnitude thresholds 0.20 and 0.40
    (FALSIFIED threshold lo and p held). Statistic/null unchanged."""
    out = {}
    for hi in (0.20, 0.40):
        raw_v = verdict(raw["cliffs_delta"], raw["mc_p_twosided"], lo=0.15, hi=hi)
        cp_v = verdict(gate["control_C_P"]["delta_resid"], gate["control_C_P"]["mc_p_twosided"], lo=0.15, hi=hi)
        rm_v = verdict(gate["control_recall_mean"]["delta_resid"], gate["control_recall_mean"]["mc_p_twosided"],
                       lo=0.15, hi=hi)
        gate_v = "UNDETERMINED (control flip)" if cp_v != rm_v else cp_v
        out[f"hi_{hi}"] = {"confirmed_threshold": hi, "falsified_threshold": 0.15,
                           "H_Phantom_CPC_Signature": raw_v,
                           "H_Phantom_Beyond_Presence": gate_v,
                           "gate_control_C_P": cp_v, "gate_control_recall_mean": rm_v}
    return out


# --------------------------------------------------------------------------- #
def main():
    print("=" * 80)
    print("v0.35 -- Naive-Phantom x CPC Omnibus -- lock v0.35-prereg-r1 @ %s (re-analysis)" % LOCK_COMMIT)
    print("=" * 80)

    recall = S33.recall_counts()
    recog, v23_levels = S33.recognition_vectors()
    v31 = load_v31()

    # ---- STEP 1: reconciliation gate (build units first for the flag check) -----------
    units, flag_check, cpc_xcheck = build_units(recall, recog, v31)
    gate, passed = reconciliation_gate(recall, recog)
    write_reconciliation_log(gate, flag_check)
    flag_ok = not flag_check["disagreements"]
    print("\nSTEP 1  reconciliation gate")
    print("        v0.33 deposit bit-for-bit: %s" %
          ("PASS" if all(gate["v33_deposit"][s]["recall_match"] and gate["v33_deposit"][s]["recog_match"]
                         for s in OMNI) else "FAIL"))
    print("        v1.7 anchor (v20/21/22):   checked=%d mismatches=%d %s" %
          (gate["v17_anchor"]["checked"], len(gate["v17_anchor"]["mismatches"]),
           "PASS" if gate["v17_anchor"]["passed"] else "FAIL"))
    print("        phantom-flag consistency:  checked=%d disagreements=%d %s" %
          (flag_check["checked"], len(flag_check["disagreements"]), "PASS" if flag_ok else "FAIL"))
    print("        cpc_score cross-check:     defined-unit max|err|=%.2e over %d units" %
          (cpc_xcheck["max_abs_err"], cpc_xcheck["checked"]))
    if not (passed and flag_ok):
        print("        GATE FAILED -- HALTING; no scoring, no roster, no verdicts.")
        sys.exit(1)
    print("        RESULT: PASS")

    # ---- STEP 2: phantom enumeration --------------------------------------------------
    roster = enumerate_roster(units)
    tot_flag = sum(roster[s]["flagged"] for s in OMNI)
    tot_anal = sum(roster[s]["analyzable"] for s in OMNI)
    tot_excl = sum(roster[s]["excluded_allzero"] for s in OMNI)
    tot_non = sum(roster[s]["non_phantom"] for s in OMNI)
    assert (tot_flag, tot_anal, tot_excl, tot_non) == (57, 29, 28, 55), \
        (tot_flag, tot_anal, tot_excl, tot_non)
    eligible = [s for s in OMNI if roster[s]["eligible_ge4"]]
    print("\nSTEP 2  phantom enumeration  (flagged=%d analyzable=%d excluded_allzero=%d non_phantom=%d)"
          % (tot_flag, tot_anal, tot_excl, tot_non))
    for s in OMNI:
        r = roster[s]
        print("        %-6s flagged=%2d analyzable=%2d excluded=%2d non_phantom=%2d  eligible(>=4)=%s"
              % (s, r["flagged"], r["analyzable"], r["excluded_allzero"], r["non_phantom"], r["eligible_ge4"]))
    print("        eligible per-substrate substrates: %s   (v0.22 pooled-only)" % eligible)

    # ---- STEP 3: scoring --------------------------------------------------------------
    raw = h_raw(units)
    gate_h = h_gate(units)
    cross = h_cross_substrate(units, raw["_per_sub_delta"], roster)
    t2 = h_t2_stability(units)

    loso_r = loso_raw(units, raw["verdict"])
    loso_g = loso_gate(units, gate_h["verdict"])
    thr = threshold_reruns(raw, gate_h)

    # raw arm fragility folded into reported verdict
    raw_final = raw["verdict"]
    if loso_r["fragile"]:
        raw_final = "UNDETERMINED (fragile under LOSO)"
    gate_final = gate_h["verdict"]
    if gate_h["verdict"] != "UNDETERMINED (control flip)" and loso_g["fragile"]:
        gate_final = "UNDETERMINED (fragile under LOSO)"

    # strip internal keys
    for h in (raw, gate_h):
        for k in [k for k in h if k.startswith("_")]:
            h.pop(k)
    raw["verdict_pre_loso"] = raw["verdict"]
    raw["verdict"] = raw_final
    gate_h["verdict_pre_loso"] = gate_h["verdict"]
    gate_h["verdict"] = gate_final

    verdicts = {
        "phase": "v0.35", "title": PRE.PHASE_TITLE, "lock": "v0.35-prereg-r1",
        "lock_commit": LOCK_COMMIT, "no_new_llm_calls": True,
        "seed": SEED, "rng_seeds": RNG,
        "loso_seed_base": {"raw": LOSO_RAW_BASE, "gate": LOSO_GATE_BASE},
        "mc_draws": N_MC, "panel": PANEL, "n_brand_units": len(units),
        "metric": "CV-CPC = 1/(1+CV), CV=sd_pop/mean of 6-model recall (ddof=0); characterization "
                  "quantity computed below floor; all-zero recall excluded (CV undefined)",
        "phantom_flag": "status=='undefined' in v31_cpc.csv == mean_r<1.0 (frozen v0.31 archive)",
        "reconciliation_gate": gate,
        "phantom_flag_consistency": {"checked": flag_check["checked"],
                                     "disagreements": flag_check["disagreements"]},
        "cpc_score_cross_check": cpc_xcheck,
        "enumeration": {s: roster[s] for s in OMNI},
        "eligible_substrates": eligible,
        "attrition": {"flagged": tot_flag, "analyzable_phantom": tot_anal,
                      "excluded_all_zero": tot_excl, "non_phantom": tot_non,
                      "analysis_set_n": tot_anal + tot_non},
        "verdicts": {
            "H_Phantom_CPC_Signature": raw,
            "H_Phantom_Beyond_Presence": gate_h,
            "H_Phantom_Cross_Substrate": cross,
            "H_Phantom_t2_Stability": t2,
        },
        "sensitivity": {
            "loso_raw": loso_r, "loso_gate": loso_g, "threshold_reruns": thr,
        },
        "deviations": [
            {"id": "D1", "title": "Pooled Cliff's delta = within-substrate cross-pair pooling",
             "resolution": "Observed pooled delta = sum_s[#ph>non - #ph<non] / sum_s(n_ph,s*n_non,s); "
                           "observed statistic respects strata; null permutes labels within substrate. "
                           "Not strata-ignoring all-pairs (would break exchangeability)."},
            {"id": "D2", "title": "Rank-residualization fit population",
             "resolution": "Fit over ALL analyzable units (phantom + non-phantom) within substrate so the "
                           "residual carries the phantom contrast; not non-phantom-only."},
            {"id": "D3", "title": "Cross-substrate per-substrate delta arm",
             "resolution": "Raw arm (CV-CPC), not residualized; binomial sign test on eligible (>=4) substrates."},
        ],
        "computation_notes": [
            "Phantom CV-CPC recomputed as 1/(1+sd_pop/mean) from re-extracted recall (cpc_score blank "
            "for undefined rows in v31_cpc.csv); defined-unit CV-CPC reproduces frozen cpc_score "
            f"(max|err|={cpc_xcheck['max_abs_err']:.2e}).",
            "Population SD (ddof=0), CV=sd_pop/mean, per score_v0_31 convention.",
            "Cliff's delta ties contribute 0; two-sided permutation p=(1+#{|d_perm|>=|d_obs|})/(N+1).",
            "Opposite-direction significance falsifies the mechanism-signature claim (checked before the "
            "magnitude-CONFIRMED branch).",
            "Rank residualization: OLS of avg-tie ranks; zero rank-variance covariate or n<3 -> centered "
            "ranks (no-op), mirroring score_v34.residualize. Recognition saturation -> C_P control near "
            "no-op; recall-mean control attenuates strongly (phantom flag IS low recall-mean) -> flip plausible.",
            "v0.22 enters pooled analysis only (1 analyzable phantom < 4-floor); stratum min-cell=1, "
            "coarsely quantized null (15 within-stratum states) but valid.",
            "Cross-substrate exact binomial on 4 eligible substrates cannot reach p<0.05 even at 4/4 "
            "(structural underpower; pre-acknowledged in the lock).",
            f"v0.23 Phase A recognition r_levels={v23_levels} (binarized all-recognized; C_P saturated).",
            "H_Phantom_t2_Stability is WALLED: descriptive only, no thresholds, quarantined from verdicts.",
        ],
    }

    OUT.mkdir(parents=True, exist_ok=True)
    json.dump(S34._clean(verdicts), open(OUT / "v35_verdicts.json", "w"), indent=2, allow_nan=False)

    # ---- console summary (gate-first) -------------------------------------------------
    print("\nSTEP 3  scoring  (seed %d, %d draws)" % (SEED, N_MC))
    print("\nPRIMARY GATE  H_Phantom_Beyond_Presence : %s" % gate_h["verdict"])
    print("        control C_P        : delta_resid=%+.4f  p=%.4g  -> %s" %
          (gate_h["control_C_P"]["delta_resid"], gate_h["control_C_P"]["mc_p_twosided"],
           gate_h["control_C_P"]["verdict"]))
    print("        control recall-mean: delta_resid=%+.4f  p=%.4g  -> %s" %
          (gate_h["control_recall_mean"]["delta_resid"], gate_h["control_recall_mean"]["mc_p_twosided"],
           gate_h["control_recall_mean"]["verdict"]))
    print("        control_flip=%s  | LOSO survives=%s" % (gate_h["control_flip"], loso_g["survives_all"]))
    print("\nPRIMARY RAW   H_Phantom_CPC_Signature (manipulation check) : %s" % raw["verdict"])
    print("        cliffs_delta=%+.4f  p=%.4g  (n_ph=%d vs n_non=%d, %d pairs)  LOSO survives=%s" %
          (raw["cliffs_delta"], raw["mc_p_twosided"], raw["n_phantom_analyzable"],
           raw["n_nonphantom"], raw["n_within_substrate_pairs"], loso_r["survives_all"]))
    print("\nSECONDARY     H_Phantom_Cross_Substrate : %s" % cross["verdict"])
    print("        per-substrate raw delta: " +
          "  ".join("%s=%s" % (s, ("na" if cross["per_substrate_delta_all"][s] is None
                                   else "%+.3f" % cross["per_substrate_delta_all"][s])) for s in OMNI))
    print("\nTERTIARY      H_Phantom_t2_Stability (WALLED, descriptive): raw delta=%+.4f p=%.4g" %
          (t2["raw_arm"]["cliffs_delta"], t2["raw_arm"]["mc_p_twosided"]))
    print("\nthreshold reruns (hi=0.20 / 0.40): raw %s / %s ; gate %s / %s" %
          (thr["hi_0.2"]["H_Phantom_CPC_Signature"], thr["hi_0.4"]["H_Phantom_CPC_Signature"],
           thr["hi_0.2"]["H_Phantom_Beyond_Presence"], thr["hi_0.4"]["H_Phantom_Beyond_Presence"]))
    print("\nwrote: %s" % (OUT / "v35_verdicts.json"))
    print("wrote: %s" % (OUT / "data" / "v35_phantom_roster.csv"))
    print("wrote: %s" % (OUT / "data" / "v35_reconciliation_log.txt"))
    return verdicts


if __name__ == "__main__":
    main()
