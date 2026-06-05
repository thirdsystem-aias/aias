#!/usr/bin/env python3
"""
score_v32.py -- v0.32 two-arm CPC version-stability scorer.

Brand-mention coder reused VERBATIM from score_v22.py (v1.4 canonical
detect_mention) -- same instrument, applied symmetrically to both arms.
Per (brand, model) recall 0..6 = mentions across that model's 6 Phase B frames
(= v1.7 r_{b,k}). CPC = 1/(1+CV), floor mean<1.0 -> N/A, per arm independently.

Emits osf/v32/v32_verdicts.json with PRIMARY rho, SECONDARY mean|dCPC| vs
0.5*SD(CPC_A), TERTIARY Cell-B flip rate, leave-one-provider-out rho, and the
denominators (pairwise-complete n, per-arm N/A counts, directional/by-cell flip
table) as first-class fields. No minimum-n rule (small n -> read via flips).
"""
from __future__ import annotations

import csv
import json
import re
import unicodedata
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr

ROOT = Path.home() / "aias"
DATA = ROOT / "osf" / "v32" / "data"
REGISTRY = ROOT / "registries" / "v0_32_registry.json"
OUT = ROOT / "osf" / "v32" / "v32_verdicts.json"

SLOTS = ["claude_opus", "claude_sonnet", "gpt_4o", "gpt_4o_mini",
         "gemini_flash", "gemini_flash_lite"]
PROVIDERS = {"anthropic": ["claude_opus", "claude_sonnet"],
             "openai": ["gpt_4o", "gpt_4o_mini"],
             "google": ["gemini_flash", "gemini_flash_lite"]}
MU_FLOOR = 1.0


# --- v1.4 canonical brand-mention detection (VERBATIM from score_v22.py) ------
def _normalize(s: str) -> str:
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return s.lower()


def detect_mention(response_text: str, brand_name: str) -> bool:
    if not response_text or not brand_name:
        return False
    pattern = r"\b" + re.escape(_normalize(brand_name)) + r"\b"
    return bool(re.search(pattern, _normalize(response_text)))


# --- per-(brand, model) recall and CPC ---------------------------------------
def per_model_counts(phase_b_rows, brand, slots=SLOTS):
    """0..6 recall per model = mentions across that model's 6 frames."""
    counts = []
    for slot in slots:
        c = sum(detect_mention(r["response_text"], brand)
                for r in phase_b_rows if r["slot"] == slot)
        counts.append(c)
    return counts  # len == len(slots)


def cpc(counts):
    """v1.7: CPC = 1/(1+CV); floor mean<1.0 -> None (N/A)."""
    arr = np.asarray(counts, float)
    mu = arr.mean()
    if mu < MU_FLOOR:
        return None
    cv = arr.std(ddof=0) / mu
    return 1.0 / (1.0 + cv)


def cpc_by_brand(rows, brands, slots=SLOTS):
    return {b: cpc(per_model_counts(rows, b, slots)) for b in brands}


def rho_pairwise(cpc_a, cpc_b, brands):
    pairs = [(cpc_a[b], cpc_b[b]) for b in brands
             if cpc_a[b] is not None and cpc_b[b] is not None]
    n = len(pairs)
    if n < 3:
        return None, n
    a, b = zip(*pairs)
    r, _ = spearmanr(a, b)
    return float(r), n


def band(r):
    if r is None:
        return "undetermined (n<3)"
    if r >= 0.70:
        return "rank-stable"
    if r >= 0.50:
        return "partially version-sensitive"
    return "version-dominated"


def main():
    reg = json.load(open(REGISTRY))
    brands, cell_of = [], {}
    for cid, cell in reg["cells"].items():
        for br in cell["brands"]:
            brands.append(br["name"]); cell_of[br["name"]] = cid

    A = list(csv.DictReader(open(DATA / "phase_b_A.csv")))
    B = list(csv.DictReader(open(DATA / "phase_b_B.csv")))
    cpc_a = cpc_by_brand(A, brands)
    cpc_b = cpc_by_brand(B, brands)

    # --- PRIMARY: rho (pairwise-complete) ---
    r, n_pc = rho_pairwise(cpc_a, cpc_b, brands)

    # --- SECONDARY: mean|dCPC| vs 0.5*SD(CPC_A over defined-A brands) ---
    defined_a = [cpc_a[b] for b in brands if cpc_a[b] is not None]
    sd_a = float(np.std(defined_a, ddof=0)) if len(defined_a) >= 2 else None
    pc = [b for b in brands if cpc_a[b] is not None and cpc_b[b] is not None]
    dcpc = [cpc_b[b] - cpc_a[b] for b in pc]
    mean_abs_dcpc = float(np.mean([abs(x) for x in dcpc])) if dcpc else None
    mean_signed_dcpc = float(np.mean(dcpc)) if dcpc else None
    sec_threshold = 0.5 * sd_a if sd_a is not None else None

    # --- flip table (directional + by cell) ---
    flips = {"A_def_to_B_NA": [], "B_def_to_A_NA": []}  # B_def_to_A_NA == A-N/A -> B-defined
    na_a = [b for b in brands if cpc_a[b] is None]
    na_b = [b for b in brands if cpc_b[b] is None]
    for b in brands:
        da, db = cpc_a[b] is not None, cpc_b[b] is not None
        if da and not db:
            flips["A_def_to_B_NA"].append(b)
        if db and not da:
            flips["B_def_to_A_NA"].append(b)
    def by_cell(blist):
        out = {}
        for b in blist:
            out.setdefault(cell_of[b], []).append(b)
        return out

    # --- TERTIARY: Cell-B emerging-instability flip rate (N/A in A -> defined in B) ---
    # flip rate per cell = (# brands N/A in A that become defined in B) / (# brands N/A in A)
    cell_flip_rate = {}
    for cid in reg["cells"]:
        cell_brands = [b for b in brands if cell_of[b] == cid]
        na_in_a = [b for b in cell_brands if cpc_a[b] is None]
        flipped = [b for b in na_in_a if cpc_b[b] is not None]
        cell_flip_rate[cid] = {
            "na_in_A": len(na_in_a), "flipped_to_defined_in_B": len(flipped),
            "flip_rate": (len(flipped) / len(na_in_a)) if na_in_a else None,
            "flipped_brands": flipped,
        }
    rates = {c: v["flip_rate"] for c, v in cell_flip_rate.items() if v["flip_rate"] is not None}
    total_na_to_def = sum(v["flipped_to_defined_in_B"] for v in cell_flip_rate.values())
    # Cell-B confirmed only if it is the UNIQUE, NONZERO highest flip rate.
    # All-zero (no flips anywhere) -> prediction not observed -> not confirmed.
    if total_na_to_def == 0 or not rates:
        cellB_highest = False
        tertiary_note = ("no N/A->defined flips in any cell; the emerging-instability "
                         "prediction (Cell-B brands e.g. Rivian/Fisker flipping N/A->defined "
                         "under Arm B) was not observed.")
    else:
        maxv = max(rates.values())
        cellB_highest = (rates.get("B", 0) == maxv
                         and sum(1 for v in rates.values() if v == maxv) == 1)
        tertiary_note = f"flip rates by cell: {rates}; total N/A->defined flips: {total_na_to_def}."

    # --- leave-one-provider-out rho ---
    loo = {}
    for prov, prov_slots in PROVIDERS.items():
        keep = [s for s in SLOTS if s not in prov_slots]
        ca = cpc_by_brand(A, brands, keep)
        cb = cpc_by_brand(B, brands, keep)
        rr, nn = rho_pairwise(ca, cb, brands)
        loo[f"drop_{prov}"] = {"rho": rr, "n_pairwise": nn, "band": band(rr)}

    verdicts = {
        "phase": "v0.32", "prereg_tag": "v0.32-prereg-r2",
        "coder": "v1.4 canonical detect_mention, verbatim from score_v22.py (symmetric across arms)",
        "per_brand_cpc": {b: {"cell": cell_of[b], "cpc_A": cpc_a[b], "cpc_B": cpc_b[b],
                              "counts_A": per_model_counts(A, b), "counts_B": per_model_counts(B, b)}
                          for b in brands},
        "PRIMARY_H_ScoreRankStable": {
            "rho": r, "n_pairwise_complete": n_pc, "threshold": 0.70,
            "verdict": (None if r is None else ("CONFIRMED" if r >= 0.70 else "FALSIFIED")),
            "interpretive_band": band(r),
        },
        "SECONDARY_H_ScoreMagnitudeStable": {
            "mean_abs_dCPC": mean_abs_dcpc, "mean_signed_dCPC": mean_signed_dcpc,
            "sd_cpc_A": sd_a, "threshold_0.5xSD": sec_threshold,
            "n_pairwise_complete": len(pc),
            "verdict": (None if (mean_abs_dcpc is None or sec_threshold is None)
                        else ("STABLE" if mean_abs_dcpc <= sec_threshold else "FALSIFIED")),
        },
        "TERTIARY_H_EmergingInstability": {
            "cell_flip_rate": cell_flip_rate,
            "cellB_highest_flip_rate": cellB_highest,
            "total_NA_to_defined_flips": total_na_to_def,
            "note": tertiary_note,
            "primary_read": "Cell-B N/A->defined flip rate vs other cells",
            "verdict": ("CONFIRMED" if cellB_highest else "FALSIFIED"),
        },
        "DENOMINATORS": {
            "n_pairwise_complete": n_pc,
            "na_count_A": len(na_a), "na_brands_A": na_a,
            "na_count_B": len(na_b), "na_brands_B": na_b,
            "flips": {"A_def_to_B_NA": {"n": len(flips["A_def_to_B_NA"]),
                                        "brands": flips["A_def_to_B_NA"], "by_cell": by_cell(flips["A_def_to_B_NA"])},
                      "B_def_to_A_NA": {"n": len(flips["B_def_to_A_NA"]),
                                        "brands": flips["B_def_to_A_NA"], "by_cell": by_cell(flips["B_def_to_A_NA"])}},
            "flip_guardrail": ("High flip count materially qualifies any stability narrative "
                               "regardless of rho (pre-reg NA_AND_FLIP_RULE)."),
        },
        "SENSITIVITY_leave_one_provider_out": loo,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    json.dump(verdicts, open(OUT, "w"), indent=2)

    # console summary
    p = verdicts["PRIMARY_H_ScoreRankStable"]; s = verdicts["SECONDARY_H_ScoreMagnitudeStable"]
    print(f"PRIMARY  rho={p['rho']}  (n_pc={p['n_pairwise_complete']})  -> {p['verdict']} [{p['interpretive_band']}]")
    print(f"SECONDARY mean|dCPC|={s['mean_abs_dCPC']}  thr(0.5*SD={s['sd_cpc_A']})={s['threshold_0.5xSD']}  -> {s['verdict']}")
    print(f"TERTIARY cellB_highest_flip={cellB_highest}  rates={rates}  -> {verdicts['TERTIARY_H_EmergingInstability']['verdict']}")
    d = verdicts["DENOMINATORS"]
    print(f"DENOM   n_pc={d['n_pairwise_complete']}  NA_A={d['na_count_A']}  NA_B={d['na_count_B']}  "
          f"flips A->B_NA={d['flips']['A_def_to_B_NA']['n']}  A_NA->B_def={d['flips']['B_def_to_A_NA']['n']}")
    print("LOO     " + "  ".join(f"{k}:{v['rho']}" for k, v in loo.items()))
    print(f"\nwrote {OUT}")


if __name__ == "__main__":
    main()
