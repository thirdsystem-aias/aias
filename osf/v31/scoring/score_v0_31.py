#!/usr/bin/env python3
"""
v0.31 — CPC Cross-Category Baseline scorer.
Locked against v0.31-prereg-r1. No new acquisition.

Channel-agnostic generalization of the v1.7 CPC instrument:
  per-model unit = total brand mentions summed across ALL Phase B frames
                   (irrespective of channel labelling); range 0..6 on the omnibus.
  On a two-channel substrate this == R_cat + R_cult == v1.7 combined_recall_count,
  by construction (channels partition the six frames).
  CPC = 1/(1+CV), CV = pop_sd/mean (ddof=0); floor mean < 1.0 -> UNDEFINED.

Reconciliation gate (STEP 0): generalized CPC on v0.20/21/22 must reproduce the
  v1.7-published per-brand values at EXACT zero difference. Any nonzero diff HALTS
  (regression test on the channel-agnostic scorer; a coding defect is the only way
  a definitional identity can fail).

Omnibus (confirmatory): v0.19, v0.20, v0.21, v0.22, v0.23 — canonical-6 x 6-frame.
Supplementary (descriptive, out of the omnibus): v0.17 (panel confirmed, brand-
  scoring deferred — raw text, no certified matcher), v0.18 (3-frame).
Excluded: v0.16 (14-model legacy), v0.24 (off-panel).
"""
import sys, json, csv, warnings
from pathlib import Path
import numpy as np
from scipy import stats

ROOT = Path.home() / "aias"
sys.path.insert(0, str(ROOT / "prereg"))
sys.path.insert(0, str(ROOT / "scripts"))

import v0_31_cpc_baseline_content as PRE   # the locked methodology
import score_v20, score_v21, score_v22     # certified matchers for raw-text substrates

PANEL = ["claude-opus-4-5", "claude-sonnet-4-5", "gpt-4o",
         "gpt-4o-mini", "gemini-2.5-flash", "gemini-2.5-flash-lite"]
FLOOR = 1.0     # PRE.FLOOR: mean combined recall < 1.0 -> UNDEFINED
DDOF = 0
SEED = 280400
N_BOOT = 10000


def cpc_from_counts(counts):
    """counts: per-model total recall counts (len 6). -> dict."""
    r = np.asarray(counts, float)
    mu = float(r.mean()); sd = float(np.std(r, ddof=DDOF))
    if mu < FLOOR:
        return {"cpc_score": None, "cpc_raw": None, "status": "undefined",
                "mean_r": mu, "sd_pop": sd, "panel_n": len(counts)}
    cv = (sd / mu) if mu > 0 else None
    cpc = (1.0 / (1.0 + cv)) if cv is not None else None
    return {"cpc_score": cpc, "cpc_raw": cv, "status": "defined",
            "mean_r": mu, "sd_pop": sd, "panel_n": len(counts)}


def read_csv(p):
    with open(p, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


# ---- per-substrate per-(brand,model) count extractors -> {brand: [c per PANEL model]}
def counts_raw_text(reg_kind, reg_path, mod, pb_path):
    """v0.20/21/22: count frames (any channel) per (brand,model) via certified matcher."""
    reg = mod.load_registry(reg_path) if reg_kind == "json" else mod.load_prereg_module(reg_path)
    brands = [(b.get("name") if isinstance(b, dict) else b, ck)
              for ck, cv in reg["cells"].items()
              for b in (cv.get("brands", []) if isinstance(cv, dict) else cv)]
    detect = mod.detect_mention
    pb = read_csv(pb_path)
    texts_by_model = {m: [] for m in PANEL}     # list of (frame response_text)
    for r in pb:
        if r["model"] in texts_by_model:
            texts_by_model[r["model"]].append(r["response_text"])
    out = {}
    cell_of = {}
    for name, ck in brands:
        out[name] = [sum(1 for t in texts_by_model[m] if detect(t, name)) for m in PANEL]
        cell_of[name] = ck
    return out, cell_of


def counts_v19(pb_path):
    """brand|panel_model|frame|mentioned: per (brand,model) sum mentioned==1 over frames."""
    pb = read_csv(pb_path)
    brands = sorted({r["brand"] for r in pb})
    agg = {b: {m: 0 for m in PANEL} for b in brands}
    for r in pb:
        b, m = r["brand"], r["panel_model"]
        if m in PANEL and str(r["mentioned"]).strip() == "1":
            agg[b][m] += 1
    return {b: [agg[b][m] for m in PANEL] for b in brands}, {b: "" for b in brands}


def counts_v23(pb_path):
    """coded brand_mentions {S01..}: per (brand,model) sum over 6 probes."""
    d = json.load(open(pb_path))
    brand_ids = sorted(d[0]["brand_mentions"].keys())
    agg = {b: {m: 0 for m in PANEL} for b in brand_ids}
    for rec in d:
        m = rec.get("model_id")
        if m in PANEL:
            for b, v in rec["brand_mentions"].items():
                if v:
                    agg[b][m] += 1
    return {b: [agg[b][m] for m in PANEL] for b in brand_ids}, {b: "" for b in brand_ids}


def counts_v18(pb_path):
    """per_frame_per_model bools (3 frames): per (brand,model) sum over frames (0..3)."""
    d = json.load(open(pb_path))
    out, cell_of = {}, {}
    for ck, cell in d["cells"].items():
        for pb in cell["per_brand"]:
            name = pb["brand"]
            agg = {m: 0 for m in PANEL}
            for frame, per_model in pb["per_frame_per_model"].items():
                for m, hit in per_model.items():
                    if m in PANEL and hit:
                        agg[m] += 1
            out[name] = [agg[m] for m in PANEL]
            cell_of[name] = ck
    return out, cell_of


def score_substrate(counts, cell_of, n_frames):
    recs = {}
    for b, c in counts.items():
        assert len(c) == 6, f"{b}: panel_n={len(c)} != 6"
        r = cpc_from_counts(c)
        r.update({"brand": b, "cell": cell_of.get(b, ""), "counts": c, "n_frames": n_frames})
        recs[b] = r
    defined = [r for r in recs.values() if r["status"] == "defined"]
    return {"records": recs, "n_brands": len(recs),
            "n_defined": len(defined), "n_undefined": len(recs) - len(defined),
            "undefined_brands": [b for b, r in recs.items() if r["status"] == "undefined"]}


# ----------------------------------------------------------------------------
def main():
    V = ROOT / "osf"
    # --- STEP 0: reconciliation gate -----------------------------------------
    print("=" * 78)
    print("STEP 0 — reconciliation gate (generalized CPC == v1.7, exact)")
    print("=" * 78)
    recon_cfg = {
        "v0.20": ("json",   ROOT / "prereg/v0_20_registry.json",          score_v20, V/"v20/phase_b_results.csv"),
        "v0.21": ("json",   ROOT / "prereg/v0_21_registry.json",          score_v21, V/"v21/phase_b_results.csv"),
        "v0.22": ("module", ROOT / "prereg/v0_22_automotive_content.py",  score_v22, V/"v22/phase_b_results.csv"),
    }
    v17_csv = {(r["substrate"], r["brand"]): r
               for r in read_csv(V / "methodology/v1_7/data/v1_7_cpc.csv")}
    # The exact identity is on the INTEGER per-model count vectors (the channel-
    # agnostic unit itself); v1.7 stores them as r_per_model. Derived CPC carries
    # ~1e-16 float-repr noise from the CSV round-trip, reported informationally.
    gate = {"checked": 0, "count_mismatches": [], "max_cpc_abs_diff": 0.0}
    recon_counts = {}
    for key, (rk, rp, mod, pb) in recon_cfg.items():
        counts, cell_of = counts_raw_text(rk, rp, mod, pb)
        recon_counts[key] = (counts, cell_of)
        for b, c in counts.items():
            ref = v17_csv.get((key, b))
            if ref is None:
                continue
            gate["checked"] += 1
            ref_counts = json.loads(ref["r_per_model"])
            # CV is order-invariant; v1.7 stored counts in sorted() model order, this
            # scorer in PANEL order. The identity is over the multiset -> sorted compare.
            if sorted(map(int, c)) != sorted(map(int, ref_counts)):
                gate["count_mismatches"].append({"brand": b, "substrate": key,
                                                 "v031": list(c), "v1_7": ref_counts})
            r = cpc_from_counts(c); ref_raw = ref.get("cpc_raw", "")
            if r["cpc_raw"] is not None and ref_raw not in ("", "None", None):
                gate["max_cpc_abs_diff"] = max(gate["max_cpc_abs_diff"], abs(r["cpc_raw"] - float(ref_raw)))
    gate_pass = not gate["count_mismatches"]   # exact integer-count identity
    gate["max_abs_diff"] = gate["max_cpc_abs_diff"]
    print(f"  checked {gate['checked']} brands across v0.20/21/22 | "
          f"per-model count mismatches={len(gate['count_mismatches'])} "
          f"| derived-CPC float noise max|Δ|={gate['max_cpc_abs_diff']:.2e}")
    if not gate_pass:
        print("  GATE FAILED — generalized scorer diverges from v1.7. HALTING; no scoring.")
        json.dump({"gate": gate, "gate_pass": False},
                  open(ROOT / "osf/v31/v31_gate_FAILED.json", "w"), indent=2)
        sys.exit(1)
    print("  GATE PASSED — exact identity to v1.7 confirmed.\n")

    # --- Omnibus + supplementary scoring -------------------------------------
    OMNIBUS = {}
    # v0.20/21/22 reuse the gate's counts (already computed)
    for key in ("v0.20", "v0.21", "v0.22"):
        counts, cell_of = recon_counts[key]
        OMNIBUS[key] = score_substrate(counts, cell_of, n_frames=6)
    OMNIBUS["v0.19"] = score_substrate(*counts_v19(V / "v19/phase_b_results.csv"), n_frames=6)
    OMNIBUS["v0.23"] = score_substrate(*counts_v23(V / "v23/data/v23_phase_b_scored.json"), n_frames=6)
    SUPP = {}
    SUPP["v0.18"] = score_substrate(*counts_v18(V / "v18/data/phase_b_results.json"), n_frames=3)
    SUPP["v0.17"] = {"deferred": True,
                     "reason": "raw-text Phase B (slot JSON), canonical-6 panel confirmed; "
                               "brand-scoring needs a kitchenware matcher/registry not present. "
                               "Descriptive-only; out of omnibus regardless."}

    OMNI_ORDER = ["v0.19", "v0.20", "v0.21", "v0.22", "v0.23"]
    CAT = {"v0.19": "audiophile headphones", "v0.20": "skincare", "v0.21": "cosmetics",
           "v0.22": "automotive", "v0.23": "premium spirits", "v0.18": "indie fragrance"}

    # --- H_CPC_Computable: within-substrate non-degenerate CPC variance -------
    h1 = {}
    for k in OMNI_ORDER:
        vals = [r["cpc_score"] for r in OMNIBUS[k]["records"].values() if r["status"] == "defined"]
        var = float(np.var(vals, ddof=0)) if len(vals) >= 2 else 0.0
        distinct = len(set(round(v, 9) for v in vals))
        non_degenerate = (len(vals) >= 2) and (var > 1e-9) and (distinct >= 2)
        h1[k] = {"n_defined": len(vals), "cpc_variance": var, "distinct_cpc": distinct,
                 "non_degenerate": bool(non_degenerate),
                 "cpc_min": (min(vals) if vals else None), "cpc_max": (max(vals) if vals else None)}
    H1 = "CONFIRM" if all(v["non_degenerate"] for v in h1.values()) else "FALSIFIED"

    # --- H_CPC_CrossCategory: Kruskal–Wallis across the 5 omnibus substrates ---
    groups = [[r["cpc_score"] for r in OMNIBUS[k]["records"].values() if r["status"] == "defined"]
              for k in OMNI_ORDER]
    kw = stats.kruskal(*groups)
    H2 = "CONFIRM" if kw.pvalue < 0.05 else "FALSIFIED"
    medians = {k: float(np.median(g)) for k, g in zip(OMNI_ORDER, groups)}

    # --- write per-brand CSV -------------------------------------------------
    out_dir = ROOT / "osf/v31"; (out_dir / "data").mkdir(parents=True, exist_ok=True)
    csv_path = out_dir / "data" / "v31_cpc.csv"
    cols = ["substrate", "brand", "cell", "set", "mean_r", "sd_pop", "cpc_raw",
            "cpc_score", "status", "panel_n", "n_frames"]
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader()
        for setname, group in (("omnibus", OMNIBUS), ("supplementary", {"v0.18": SUPP["v0.18"]})):
            for k, s in group.items():
                for b, r in s["records"].items():
                    w.writerow({"substrate": k, "brand": b, "cell": r["cell"], "set": setname,
                                "mean_r": r["mean_r"], "sd_pop": r["sd_pop"], "cpc_raw": r["cpc_raw"],
                                "cpc_score": r["cpc_score"], "status": r["status"],
                                "panel_n": r["panel_n"], "n_frames": r["n_frames"]})

    verdicts = {
        "phase": "v0.31", "lock": "v0.31-prereg-r1", "no_new_llm_calls": True,
        "instrument": "v1.7 CPC, channel-agnostic generalization (total per-model mentions across frames)",
        "reconciliation_gate": {"pass": True, "checked": gate["checked"],
                                "max_abs_diff": gate["max_abs_diff"], "tolerance": 0.0,
                                "reference": "osf/methodology/v1_7/data/v1_7_cpc.csv"},
        "omnibus": {k: {"category": CAT[k], "n_brands": OMNIBUS[k]["n_brands"],
                        "n_defined": OMNIBUS[k]["n_defined"], "n_undefined": OMNIBUS[k]["n_undefined"],
                        "undefined_brands": OMNIBUS[k]["undefined_brands"],
                        "cpc_median": medians[k]} for k in OMNI_ORDER},
        "supplementary": {"v0.18": {"category": CAT["v0.18"], "n_brands": SUPP["v0.18"]["n_brands"],
                                    "n_defined": SUPP["v0.18"]["n_defined"],
                                    "n_undefined": SUPP["v0.18"]["n_undefined"],
                                    "note": "3-frame (0..3); descriptive only, excluded from omnibus KW"},
                          "v0.17": SUPP["v0.17"]},
        "excluded": {"v0.16": "14-model legacy panel; Trends-validation Phase B (no per-model LLM recall)",
                     "v0.24": "off the locked six (opus-4-7 / sonnet-4-6)"},
        "H_CPC_Computable": {"verdict": H1, "per_substrate": h1},
        "H_CPC_CrossCategory": {"verdict": H2, "kruskal_H": float(kw.statistic),
                                "kruskal_p": float(kw.pvalue), "alpha": 0.05,
                                "n_groups": len(OMNI_ORDER), "medians": medians},
    }
    vpath = out_dir / "v31_cpc_verdicts.json"
    json.dump(verdicts, open(vpath, "w"), indent=2)

    # --- console summary -----------------------------------------------------
    print("=" * 78)
    print("v0.31 (CPC cross-category baseline) — lock v0.31-prereg-r1")
    print("=" * 78)
    print(f"  H_CPC_Computable    : {H1}")
    for k in OMNI_ORDER:
        v = h1[k]; s = OMNIBUS[k]
        print(f"      {k} {CAT[k]:<22} defined {v['n_defined']}/{s['n_brands']}  "
              f"undef {s['n_undefined']}  CPC[{v['cpc_min'] or 0:.2f},{v['cpc_max'] or 0:.2f}]  "
              f"var={v['cpc_variance']:.4f}  {'OK' if v['non_degenerate'] else 'DEGENERATE'}")
    print(f"  H_CPC_CrossCategory : {H2}   (Kruskal-Wallis H={kw.statistic:.3f}, p={kw.pvalue:.4g}, k=5)")
    print(f"      medians: " + "  ".join(f"{k}={medians[k]:.3f}" for k in OMNI_ORDER))
    print(f"  supplementary v0.18 : defined {SUPP['v0.18']['n_defined']}/{SUPP['v0.18']['n_brands']} (3-frame, descriptive)")
    print(f"  supplementary v0.17 : DEFERRED (raw-text; panel confirmed canonical-6)")
    print(f"\n  reconciliation gate : PASS (max|Δ|={gate['max_abs_diff']:.2e}, {gate['checked']} brands)")
    print(f"  wrote: {csv_path}")
    print(f"  wrote: {vpath}")
    return verdicts


if __name__ == "__main__":
    main()
