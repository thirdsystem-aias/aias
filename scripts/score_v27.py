#!/usr/bin/env python3
"""
v0.27 (CV.03) scorer - convergent validity vs third-party AI-visibility instruments.
Cloned in spirit from score_v0_25.py (correlation study), NOT v0.26 (BSR).

Sources canonical scoring from the LOCKED pre-reg module
(prereg/v0_27_b2b_saas_convergent_validity_content.py): hypothesis ids, primary
family, thresholds, sensitivity rule. Numeric cutoffs are implemented here and
echoed alongside the locked threshold STRINGS at runtime so any drift between
the lock and the implementation is visible. Hypothesis-id set and primary_family
are asserted against the module.

Reads:
  osf/v27/data/v0.27_aias_side.csv         (AIAS side; join key brand_id)
  osf/v27/data/v0.27_I1_normalized.csv     (HubSpot; optional)
  osf/v27/data/v0.27_I2_normalized.csv     (Profound; optional -> NOT_RUN if absent)
  osf/v27/data/v0.27_I3_normalized.csv     (Brandwatch; optional)

Normalized instrument schemas (produced by acquire_v27_instruments.py):
  I1: brand_id, I1_sov, I1_sentiment, I1_presence_quality, I1_brand_recognition,
      I1_market_competition, I1_composite_100, null_flag
  I2: brand_id, I2_visibility, I2_som, null_flag
  I3: brand_id, I3_mention_volume, null_flag

Writes: osf/v27/v0.27_verdicts.json

Run with no instrument CSVs present -> smoke test: Recognition_Null resolves from
the AIAS CSV alone; all instrument-dependent hypotheses report NOT_RUN.
"""
import csv, json, os, sys, importlib.util, datetime
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser("~/aias")
DATA = os.path.join(ROOT, "osf/v27/data")
PREREG = os.path.join(ROOT, "prereg/v0_27_b2b_saas_convergent_validity_content.py")
OUT = os.path.join(ROOT, "osf/v27/v0.27_verdicts.json")

AIAS_CSV = os.path.join(DATA, "v0.27_aias_side.csv")
I1_CSV = os.path.join(DATA, "v0.27_I1_normalized.csv")
I2_CSV = os.path.join(DATA, "v0.27_I2_normalized.csv")
I3_CSV = os.path.join(DATA, "v0.27_I3_normalized.csv")

MIN_N = 12          # SCORING.min_n_for_valid_rho -> below -> UNDETERMINED
N_BOOT = 10000      # SCORING.bootstrap_resamples
RNG = np.random.default_rng(20270527)   # fixed seed -> reproducible CIs


# ---------------------------------------------------------------- load lock
def load_lock(path):
    spec = importlib.util.spec_from_file_location("prereg_v27", path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


# ---------------------------------------------------------------- stats
def spearman_block(x, y):
    """Pairwise-complete Spearman with bootstrap 95% CI. Returns dict or None."""
    df = pd.DataFrame({"x": x, "y": y}).dropna()
    n = len(df)
    if n < MIN_N:
        return {"n": n, "rho": None, "p": None, "ci": None, "undetermined": True}
    rho, p = spearmanr(df["x"], df["y"])
    boots = []
    xv, yv = df["x"].to_numpy(), df["y"].to_numpy()
    for _ in range(N_BOOT):
        idx = RNG.integers(0, n, n)
        if np.std(xv[idx]) == 0 or np.std(yv[idx]) == 0:
            continue
        boots.append(spearmanr(xv[idx], yv[idx])[0])
    ci = (float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))) if boots else None
    return {"n": int(n), "rho": float(rho), "p": float(p), "ci": ci, "undetermined": False}


def holm(pvals):
    """Holm-Bonferroni adjusted p-values, preserving input order."""
    items = [(i, p) for i, p in enumerate(pvals) if p is not None]
    out = [None] * len(pvals)
    m = len(items)
    items.sort(key=lambda t: t[1])
    prev = 0.0
    for rank, (i, p) in enumerate(items):
        adj = min(1.0, max(prev, (m - rank) * p))
        out[i] = adj
        prev = adj
    return out


# ---------------------------------------------------------------- verdicts
def v_convergent(block, conf, strong, fals, p_adj=None):
    """Band logic shared by the convergent hypotheses."""
    if block is None:
        return "NOT_RUN"
    if block["undetermined"]:
        return "UNDETERMINED"
    rho = block["rho"]
    p = p_adj if p_adj is not None else block["p"]
    sig = (p is not None and p < 0.05)
    if rho >= strong:
        return "STRONG"
    if rho >= conf and sig:
        return "CONFIRMED"
    if rho < fals or not sig:
        return "FALSIFIED"
    return "PARTIAL"


def main():
    lock = load_lock(PREREG)
    aias = pd.read_csv(AIAS_CSV)

    # provenance / integrity guards against the locked module
    assert set(lock.HYPOTHESES) == {
        "H_CV3_Primary", "H_CV3_Profound", "H_CV3_SOM",
        "H_CV3_Discriminant", "H_CV3_Component", "H_CV3_Recognition_Null"
    }, "hypothesis id set drifted from lock"
    assert lock.SCORING["primary_family"] == ["H_CV3_Primary", "H_CV3_Profound", "H_CV3_SOM"]

    def opt(path):
        return pd.read_csv(path) if os.path.exists(path) else None
    I1, I2, I3 = opt(I1_CSV), opt(I2_CSV), opt(I3_CSV)

    def merged(inst, col):
        if inst is None or col not in inst.columns:
            return None, None
        m = aias.merge(inst[["brand_id", col]], on="brand_id", how="inner")
        return m["recall_channel_som"], m[col]

    res = {}

    # --- primary family (raw blocks; Holm applied after) ---
    bx1 = spearman_block(*merged(I1, "I1_sov")) if I1 is not None else None
    bx2 = spearman_block(*merged(I2, "I2_visibility")) if I2 is not None else None
    bxs = spearman_block(*merged(I2, "I2_som")) if I2 is not None else None
    fam_p = [b["p"] if (b and not b["undetermined"]) else None for b in (bx1, bx2, bxs)]
    padj = holm(fam_p)

    res["H_CV3_Primary"] = {"block": bx1, "p_adj": padj[0],
        "status": v_convergent(bx1, 0.60, 0.74, 0.30, padj[0]),
        "locked_threshold": lock.HYPOTHESES["H_CV3_Primary"]["thresholds"],
        "implemented": "STRONG>=0.74 | CONFIRMED>=0.60&p_adj<.05 | FALSIFIED<0.30 or n.s. | else PARTIAL"}
    res["H_CV3_Profound"] = {"block": bx2, "p_adj": padj[1],
        "status": v_convergent(bx2, 0.60, 0.74, 0.30, padj[1]),
        "locked_threshold": lock.HYPOTHESES["H_CV3_Profound"]["thresholds"],
        "implemented": "STRONG>=0.74 | CONFIRMED>=0.60 | FALSIFIED<0.30 | else PARTIAL ; NOT_RUN if no Profound"}
    res["H_CV3_SOM"] = {"block": bxs, "p_adj": padj[2],
        "status": v_convergent(bxs, 0.70, 0.80, 0.40, padj[2]),
        "locked_threshold": lock.HYPOTHESES["H_CV3_SOM"]["thresholds"],
        "implemented": "STRONG>=0.80 | CONFIRMED>=0.70 | FALSIFIED<0.40 | else PARTIAL ; NOT_RUN if no Profound"}

    # --- discriminant: rho(AIAS,I3) vs rho(AIAS,I1) ---
    if I3 is not None and I1 is not None:
        b_i3 = spearman_block(*merged(I3, "I3_mention_volume"))
        r_i1 = bx1["rho"] if (bx1 and not bx1["undetermined"]) else None
        r_i3 = b_i3["rho"] if (b_i3 and not b_i3["undetermined"]) else None
        if r_i3 is None or r_i1 is None:
            disc = "UNDETERMINED"
        elif r_i3 >= r_i1:
            disc = "FALSIFIED"
        elif r_i3 < 0.50 and (r_i1 - r_i3) >= 0.20:
            disc = "CONFIRMED"
        else:
            disc = "PARTIAL"
        res["H_CV3_Discriminant"] = {"block": b_i3, "rho_I1": r_i1, "rho_I3": r_i3,
            "status": disc, "locked_threshold": lock.HYPOTHESES["H_CV3_Discriminant"]["thresholds"]}
    else:
        res["H_CV3_Discriminant"] = {"status": "NOT_RUN", "block": None}

    # --- component MTMM block (exploratory): emit matrix, no hard pass/fail ---
    if I1 is not None:
        aias_vars = [c for c in ["recall_channel_som", "aias_composite", "identity_load"]
                     if c in aias.columns]
        i1_dims = [c for c in ["I1_sov", "I1_sentiment", "I1_presence_quality",
                               "I1_brand_recognition", "I1_market_competition"] if c in I1.columns]
        mm = aias.merge(I1[["brand_id"] + i1_dims], on="brand_id", how="inner")
        matrix = {}
        for a in aias_vars:
            matrix[a] = {}
            for d in i1_dims:
                blk = spearman_block(mm[a], mm[d])
                matrix[a][d] = None if (blk is None or blk["undetermined"]) else round(blk["rho"], 3)
        res["H_CV3_Component"] = {"status": "EXPLORATORY", "matrix": matrix,
            "note": "inspect convergent (visibility-type) vs discriminant (sentiment) block structure manually"}
    else:
        res["H_CV3_Component"] = {"status": "NOT_RUN", "matrix": None}

    # --- recognition null control (AIAS-only) ---
    cp_sd = float(np.std(aias["C_P"]))
    res["H_CV3_Recognition_Null"] = {
        "status": "CONFIRMED" if cp_sd < 0.01 else "UNDETERMINED",
        "C_P_sd": cp_sd, "C_P_mean": float(np.mean(aias["C_P"])),
        "note": "ceiling -> zero variance -> excluded from primary (replicates v0.25)"}

    # --- type-2 sensitivity (convergent hypotheses only) ---
    t2_mask = (aias["R_cat"] == 0) & (aias["R_cult"] > 0)
    t2_ids = aias.loc[t2_mask, "brand_id"].tolist()
    keep = aias.loc[~t2_mask].copy()
    sens = {"rule": "exclude R_cat==0 & R_cult>0", "excluded_brand_ids": t2_ids, "n_excluded": len(t2_ids)}
    def sens_block(inst, col):
        if inst is None or col not in inst.columns:
            return None
        m = keep.merge(inst[["brand_id", col]], on="brand_id", how="inner")
        return spearman_block(m["recall_channel_som"], m[col])
    for hid, inst, col in [("H_CV3_Primary", I1, "I1_sov"),
                           ("H_CV3_Profound", I2, "I2_visibility"),
                           ("H_CV3_SOM", I2, "I2_som")]:
        sb = sens_block(inst, col)
        prim = res[hid]["block"]
        delta = (round(sb["rho"] - prim["rho"], 3)
                 if sb and prim and not sb["undetermined"] and not prim["undetermined"] else None)
        sens[hid] = {"rho": (sb["rho"] if sb and not sb["undetermined"] else None),
                     "n": (sb["n"] if sb else None), "delta_vs_primary": delta}
    res["_sensitivity_type2_construct_gap"] = sens

    meta = {"generated": datetime.datetime.now().isoformat(timespec="seconds"),
            "prereg": "v0.27-prereg-r3 (instruments may force r4)",
            "instruments_present": {"I1": I1 is not None, "I2": I2 is not None, "I3": I3 is not None},
            "min_n": MIN_N, "n_boot": N_BOOT, "aias_brands": int(len(aias))}
    out = {"_meta": meta, "verdicts": res}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(out, f, indent=2)

    # console summary
    print(f"=== v0.27 scoring  (instruments: "
          f"I1={'y' if I1 is not None else '-'} "
          f"I2={'y' if I2 is not None else '-'} "
          f"I3={'y' if I3 is not None else '-'}) ===")
    for hid in ["H_CV3_Primary", "H_CV3_Profound", "H_CV3_SOM",
                "H_CV3_Discriminant", "H_CV3_Component", "H_CV3_Recognition_Null"]:
        r = res[hid]
        b = r.get("block")
        extra = ""
        if b and not b.get("undetermined") and b.get("rho") is not None:
            extra = f"  rho={b['rho']:.3f} n={b['n']}"
            if r.get("p_adj") is not None:
                extra += f" p_adj={r['p_adj']:.4f}"
        print(f"  {hid:26s} {r['status']:12s}{extra}")
    print(f"  type-2 excluded: {sens['n_excluded']} brands {sens['excluded_brand_ids']}")
    print(f"  Recognition_Null C_P sd={res['H_CV3_Recognition_Null']['C_P_sd']:.4f}")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
