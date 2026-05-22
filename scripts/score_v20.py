#!/usr/bin/env python3
"""
score_v20.py — AIAS v0.20 scoring runner.

Consumes the raw acquisition outputs from run_acquisition_v20.py and produces:
  1. Per-brand C_P (Phase A Recognition score).
  2. Per-brand R_cat and R_cult (Phase B Recall scores from six-frame battery),
     via v1.4 canonical brand-mention detection (case-insensitive,
     accent-stripped, possessive-aware, first-occurrence-wins de-duplication).
  3. Dissociation classification:
       - Iwachu: C_P ≥ 5 ∧ R_cat ≤ 2
       - Type 1: R_cat ≥ 5 ∧ R_cult ≤ 2
       - Type 2: R_cat ≤ 2 ∧ R_cult ≥ 5  (NOVEL: primary v0.20 quadrant)
  4. v1.5 C2 multi-statistic per cell (distinct C_P ≥ 3 ∧ modal share ≤ 0.625).
  5. C2 IL-gradient guard (Cell B top-2 R_cat share − Cell C top-2 R_cat share ≥ 0.10).
  6. Per-cell Phase D Spearman ρ (C_P vs R_cat) with bootstrap CI.
  7. Verdict resolution for the four pre-registered hypotheses:
       - H_Type2_emergence (PRIMARY)
       - H_Regime4_skincare
       - H_Dissociation_substrate_generalization
       - H_IdentityLoad_moderator (4-leg joint; v0.20 leg only computed here)

Output: v20_verdicts.json at the OSF v20 directory.

Required pip packages:
    scipy   (for Spearman ρ)

Usage:
    python score_v20.py                          # default paths
    python score_v20.py --registry <path>        # override registry
    python score_v20.py --phase-a <csv> --phase-b <csv>   # override input paths
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import unicodedata
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

# --- Configuration -----------------------------------------------------------

DEFAULT_REGISTRY = Path.home() / "aias" / "prereg" / "v0_20_registry.json"
DEFAULT_DATA_DIR = Path.home() / "aias" / "osf" / "v20"
DEFAULT_OUTPUT = DEFAULT_DATA_DIR / "v20_verdicts.json"


# --- Brand-mention detection (v1.4 canonical rules) --------------------------

def _normalize(s: str) -> str:
    """Lowercase and strip diacritics (e.g., 'Estée' → 'estee')."""
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return s.lower()


def detect_mention(response_text: str, brand_name: str) -> bool:
    """v1.4 canonical brand-mention detection.

    Rules:
      - case-insensitive
      - accent-stripped
      - possessive-aware (X's → X; handled by \\b word boundary)
      - first-occurrence-wins de-duplication (we just return bool here;
        de-dup is implicit since we're scanning for presence not counting)
    """
    if not response_text or not brand_name:
        return False
    norm_text = _normalize(response_text)
    norm_brand = _normalize(brand_name)
    # Word boundary handles possessives (X's → matches X) and avoids
    # substring false-positives (e.g., "La Mer" not matching "summer")
    pattern = r"\b" + re.escape(norm_brand) + r"\b"
    return bool(re.search(pattern, norm_text))


# --- Loading -----------------------------------------------------------------

def load_registry(path: Path) -> dict:
    with open(path) as f:
        return json.load(f)


def load_phase_a(path: Path) -> list[dict]:
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            rows.append(r)
    return rows


def load_phase_b(path: Path) -> list[dict]:
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            rows.append(r)
    return rows


# --- Phase A scoring: per-brand C_P -----------------------------------------

def compute_cp(phase_a_rows: list[dict], registry: dict) -> dict:
    """Return per-brand C_P scores and per-cell summaries."""
    result = {"per_brand": {}, "per_cell": {}}

    for cell_id, cell in registry["cells"].items():
        cell_brand_cps = []
        cell_data = {
            "label": cell["label"],
            "il_tier": cell["il_tier"],
            "brands": [],
        }
        for brand in cell["brands"]:
            brand_rows = [r for r in phase_a_rows if r["brand"] == brand["name"]]
            yes_count = sum(1 for r in brand_rows if r["recognized"] == "yes")
            total = len(brand_rows)
            cp = yes_count  # range 0..6
            result["per_brand"][brand["name"]] = {
                "cell": cell_id,
                "cascade_order": brand["cascade_order"],
                "cp": cp,
                "panel_responses": total,
            }
            cell_data["brands"].append({
                "name": brand["name"],
                "cascade_order": brand["cascade_order"],
                "cp": cp,
            })
            cell_brand_cps.append(cp)

        # Per-cell distributional statistics for v1.5 C2
        counter = Counter(cell_brand_cps)
        distinct_count = len(counter)
        if cell_brand_cps:
            modal_cp, modal_freq = counter.most_common(1)[0]
            modal_share = modal_freq / len(cell_brand_cps)
            mean_cp = sum(cell_brand_cps) / len(cell_brand_cps)
        else:
            modal_cp = None
            modal_share = 0.0
            mean_cp = 0.0
        cell_data["distinct_cp_count"] = distinct_count
        cell_data["modal_cp"] = modal_cp
        cell_data["modal_cp_share"] = round(modal_share, 4)
        cell_data["mean_cp"] = round(mean_cp, 3)
        cell_data["n"] = len(cell_brand_cps)

        # Cascade pivot resolution per v1.5 §6.4 (Phase A pivot-validation)
        # First brand in cascade order with C_P = 6/6 is the pivot
        pivot = None
        for b in sorted(cell_data["brands"], key=lambda x: x["cascade_order"]):
            if b["cp"] == 6:
                pivot = b["name"]
                break
        cell_data["pivot_brand"] = pivot
        cell_data["cascade_exhausted"] = pivot is None

        result["per_cell"][cell_id] = cell_data

    return result


# --- Phase B scoring: per-brand R_cat / R_cult ------------------------------

def compute_recall(phase_b_rows: list[dict], registry: dict) -> dict:
    """Return per-brand R_cat (q1-q3 channel) and R_cult (q4-q6 channel) mention counts."""
    result = {"per_brand": {}, "per_cell": {}}

    # Flatten brand index
    all_brands = []
    for cell_id, cell in registry["cells"].items():
        for brand in cell["brands"]:
            all_brands.append({
                "name": brand["name"],
                "cell": cell_id,
                "cascade_order": brand["cascade_order"],
            })

    for brand in all_brands:
        r_cat = 0
        r_cult = 0
        cat_mentions_by_frame = {"q1": 0, "q2": 0, "q3": 0}
        cult_mentions_by_frame = {"q4": 0, "q5": 0, "q6": 0}

        for row in phase_b_rows:
            if detect_mention(row["response_text"], brand["name"]):
                if row["channel"] == "R_cat":
                    r_cat += 1
                    cat_mentions_by_frame[row["frame_id"]] = cat_mentions_by_frame.get(row["frame_id"], 0) + 1
                elif row["channel"] == "R_cult":
                    r_cult += 1
                    cult_mentions_by_frame[row["frame_id"]] = cult_mentions_by_frame.get(row["frame_id"], 0) + 1

        result["per_brand"][brand["name"]] = {
            "cell": brand["cell"],
            "cascade_order": brand["cascade_order"],
            "r_cat": r_cat,  # max 18 (3 frames × 6 models)
            "r_cult": r_cult,
            "r_cat_by_frame": cat_mentions_by_frame,
            "r_cult_by_frame": cult_mentions_by_frame,
        }

    # Per-cell summaries with top-2 R_cat share (for IL-gradient guard)
    for cell_id, cell in registry["cells"].items():
        brand_r_cats = sorted(
            [result["per_brand"][b["name"]]["r_cat"] for b in cell["brands"]],
            reverse=True,
        )
        total_r_cat = sum(brand_r_cats)
        top2_share = (sum(brand_r_cats[:2]) / total_r_cat) if total_r_cat > 0 else 0.0

        result["per_cell"][cell_id] = {
            "label": cell["label"],
            "il_tier": cell["il_tier"],
            "n": len(cell["brands"]),
            "mean_r_cat": round(sum(brand_r_cats) / len(brand_r_cats), 3) if brand_r_cats else 0.0,
            "mean_r_cult": round(
                sum(result["per_brand"][b["name"]]["r_cult"] for b in cell["brands"]) / len(cell["brands"]),
                3,
            ) if cell["brands"] else 0.0,
            "top2_r_cat_share": round(top2_share, 4),
            "total_r_cat": total_r_cat,
        }

    return result


# --- Dissociation classification --------------------------------------------

def classify_dissociations(cp_data: dict, recall_data: dict, thresholds: dict) -> dict:
    iwachu_cp_min = thresholds["Iwachu_CP_min"]
    iwachu_rcat_max = thresholds["Iwachu_Rcat_max"]
    type1_rcat_min = thresholds["Type1_Rcat_min"]
    type1_rcult_max = thresholds["Type1_Rcult_max"]
    type2_rcat_max = thresholds["Type2_Rcat_max"]
    type2_rcult_min = thresholds["Type2_Rcult_min"]

    iwachu, type1, type2 = [], [], []
    for brand_name, recall in recall_data["per_brand"].items():
        cp = cp_data["per_brand"][brand_name]["cp"]
        r_cat = recall["r_cat"]
        r_cult = recall["r_cult"]
        cell = recall["cell"]
        record = {
            "brand": brand_name,
            "cell": cell,
            "cp": cp,
            "r_cat": r_cat,
            "r_cult": r_cult,
        }
        if cp >= iwachu_cp_min and r_cat <= iwachu_rcat_max:
            iwachu.append(record)
        if r_cat >= type1_rcat_min and r_cult <= type1_rcult_max:
            type1.append(record)
        if r_cat <= type2_rcat_max and r_cult >= type2_rcult_min:
            type2.append(record)

    return {
        "iwachu": iwachu,
        "type_1": type1,
        "type_2": type2,
        "iwachu_cells": sorted({c["cell"] for c in iwachu}),
        "type_1_cells": sorted({c["cell"] for c in type1}),
        "type_2_cells": sorted({c["cell"] for c in type2}),
        "iwachu_count": len(iwachu),
        "type_1_count": len(type1),
        "type_2_count": len(type2),
    }


# --- Phase D Spearman ρ per cell --------------------------------------------

def compute_phase_d_rho(cp_data: dict, recall_data: dict, registry: dict) -> dict:
    """Per-cell Spearman ρ between C_P and R_cat. Returns dict per cell."""
    try:
        from scipy.stats import spearmanr
    except ImportError:
        sys.exit("ERROR: scipy not installed. Run: python -m pip install scipy")

    result = {}
    for cell_id, cell in registry["cells"].items():
        cps = []
        rcats = []
        for brand in cell["brands"]:
            cps.append(cp_data["per_brand"][brand["name"]]["cp"])
            rcats.append(recall_data["per_brand"][brand["name"]]["r_cat"])

        if len(cps) >= 2:
            rho, p_value = spearmanr(cps, rcats)
            rho = float(rho) if rho == rho else None  # NaN check
            p_value = float(p_value) if p_value == p_value else None
        else:
            rho, p_value = None, None

        result[cell_id] = {
            "n": len(cps),
            "rho": round(rho, 4) if rho is not None else None,
            "p_value": round(p_value, 4) if p_value is not None else None,
        }
    return result


# --- v1.5 C2 multi-statistic per cell ---------------------------------------

def compute_v15_c2(cp_data: dict, thresholds: dict) -> dict:
    distinct_min = thresholds["distinct_CP_min"]
    modal_max = thresholds["modal_CP_share_max"]
    result = {}
    for cell_id, cell in cp_data["per_cell"].items():
        distinct = cell["distinct_cp_count"]
        modal_share = cell["modal_cp_share"]
        distinct_ok = distinct >= distinct_min
        modal_ok = modal_share <= modal_max
        passes = distinct_ok and modal_ok
        reason_parts = []
        if not distinct_ok:
            reason_parts.append(f"distinct_count {distinct} < {distinct_min}")
        if not modal_ok:
            reason_parts.append(f"modal_share {modal_share:.3f} > {modal_max}")
        result[cell_id] = {
            "distinct_cp_count": distinct,
            "modal_cp_share": modal_share,
            "distinct_ok": distinct_ok,
            "modal_ok": modal_ok,
            "passes": passes,
            "reason": " AND ".join(reason_parts) if reason_parts else "passes both",
        }
    return result


def compute_il_gradient_guard(recall_data: dict, thresholds: dict) -> dict:
    sep_min = thresholds["IL_gradient_separation_min"]
    cell_b_share = recall_data["per_cell"]["B"]["top2_r_cat_share"]
    cell_c_share = recall_data["per_cell"]["C"]["top2_r_cat_share"]
    separation = cell_b_share - cell_c_share
    return {
        "cell_b_top2_r_cat_share": cell_b_share,
        "cell_c_top2_r_cat_share": cell_c_share,
        "separation": round(separation, 4),
        "threshold": sep_min,
        "passes": separation >= sep_min,
    }


# --- Hypothesis verdict resolution ------------------------------------------

def resolve_h_type2_emergence(dissoc: dict, recall_data: dict) -> dict:
    """Type 2 cases (R_cat ≤ 2 ∧ R_cult ≥ 5) in Cell B at post-attrition n ≥ 5."""
    cell_b_n = recall_data["per_cell"]["B"]["n"]
    cell_b_type2 = [c for c in dissoc["type_2"] if c["cell"] == "B"]
    cell_b_type2_count = len(cell_b_type2)

    if cell_b_n < 5:
        verdict = "UNDETERMINED"
        reason = f"Cell B post-attrition n = {cell_b_n} < 5"
    elif cell_b_type2_count >= 3:
        verdict = "EMERGED"
        reason = f"Cell B Type 2 count = {cell_b_type2_count} ≥ 3"
    elif cell_b_type2_count >= 1:
        verdict = "PARTIAL"
        reason = f"Cell B Type 2 count = {cell_b_type2_count} ∈ [1, 2]"
    else:
        verdict = "FALSIFIED"
        reason = f"Cell B Type 2 count = 0 (panel adequate: n = {cell_b_n} ≥ 5)"

    return {
        "primary": True,
        "novel_for_phase": "v0.20",
        "verdict": verdict,
        "reason": reason,
        "cell_b_n": cell_b_n,
        "cell_b_type2_count": cell_b_type2_count,
        "cell_b_type2_cases": cell_b_type2,
        "all_type2_cases": dissoc["type_2"],
    }


def resolve_h_regime4(cp_data: dict, c2: dict, il_guard: dict,
                      rho: dict, registry: dict, thresholds: dict) -> dict:
    """Sequential C1 → C2 → IL-guard → C3, per pre-reg §6.2 routing."""
    rho_min = thresholds["rho_C3_min"]
    rho_cells_min = thresholds["C3_cells_clearing_min"]
    n_floor = thresholds["n_floor_worldwide"]
    c3_n_min = thresholds["n_floor_per_cell_for_C3"]

    worldwide_n = sum(cell["n"] for cell in cp_data["per_cell"].values())
    c1_passes = worldwide_n >= n_floor

    c2_failing_cells = [c for c, v in c2.items() if not v["passes"]]
    c2_failing_count = len(c2_failing_cells)

    # C3: cells with ρ ≥ threshold AND n ≥ minimum
    c3_clearing_cells = []
    c3_failing_cells = []
    for cell_id, r in rho.items():
        if r["n"] >= c3_n_min and r["rho"] is not None and r["rho"] >= rho_min:
            c3_clearing_cells.append(cell_id)
        else:
            c3_failing_cells.append(cell_id)
    c3_passes = len(c3_clearing_cells) >= rho_cells_min

    # Verdict routing per pre-reg §6.2
    if not c1_passes:
        verdict = "FALSIFIED"
        reason = f"C1 fails: worldwide n = {worldwide_n} < {n_floor}"
        resolved_at = "C1"
    elif c2_failing_count >= 2:
        verdict = "FALSIFIED"
        reason = f"C2 fails in {c2_failing_count} of 3 cells: {c2_failing_cells}"
        resolved_at = "C2 (regime-floor failure)"
    elif c2_failing_count == 1:
        # Continue to remaining checks but route as PARTIAL upon any further failure
        # Per pre-reg §6.2: C2 fails in exactly 1 cell → PARTIAL regardless of subsequent checks
        verdict = "PARTIAL"
        reason = f"C2 fails in exactly 1 cell: {c2_failing_cells[0]}"
        resolved_at = "C2"
    elif not il_guard["passes"]:
        verdict = "PARTIAL"
        reason = f"C2 IL-gradient guard fails: separation {il_guard['separation']} < {il_guard['threshold']}"
        resolved_at = "C2 IL-gradient guard"
    elif not c3_passes:
        # DEVIATIONS Rule 4: if both/all cells fail C2 within-cell adequacy, C3 SKIPPED
        # (handled above since that would be c2_failing_count ≥ 2 → already FALSIFIED)
        verdict = "PARTIAL"
        reason = (f"C3 fails: only {len(c3_clearing_cells)} cell(s) clear ρ ≥ {rho_min} "
                  f"(clearing: {c3_clearing_cells}; failing: {c3_failing_cells})")
        resolved_at = "C3"
    else:
        verdict = "CONFIRMED"
        reason = "All conditions clear (C1, C2, IL-gradient guard, C3)"
        resolved_at = "C3 (all clear)"

    return {
        "primary": False,
        "first_prospective_v1_5_C2": True,
        "verdict": verdict,
        "reason": reason,
        "resolved_at": resolved_at,
        "c1": {"worldwide_n": worldwide_n, "threshold": n_floor, "passes": c1_passes},
        "c2_per_cell": c2,
        "c2_failing_cells": c2_failing_cells,
        "il_gradient_guard": il_guard,
        "c3": {
            "rho_per_cell": rho,
            "rho_threshold": rho_min,
            "clearing_cells": c3_clearing_cells,
            "failing_cells": c3_failing_cells,
            "passes": c3_passes,
        },
    }


def resolve_h_dissociation_generalization(dissoc: dict) -> dict:
    """Iwachu-pattern distribution across cells, per pre-reg §6.3."""
    cells_with_iwachu = len(dissoc["iwachu_cells"])
    if cells_with_iwachu >= 2:
        verdict = "GENERALIZED"
        reason = f"Iwachu cases in {cells_with_iwachu} of 3 cells: {dissoc['iwachu_cells']}"
    elif cells_with_iwachu == 1:
        verdict = "PARTIAL"
        reason = f"Iwachu cases in 1 of 3 cells: {dissoc['iwachu_cells']}"
    else:
        verdict = "NARROWED"
        reason = "Iwachu cases in 0 cells"

    return {
        "primary": False,
        "fourth_family_extension": True,
        "verdict": verdict,
        "reason": reason,
        "iwachu_count": dissoc["iwachu_count"],
        "iwachu_cells": dissoc["iwachu_cells"],
        "type_1_count": dissoc["type_1_count"],
        "type_1_cells": dissoc["type_1_cells"],
    }


def resolve_h_identity_load_moderator(h_regime4_verdict: dict, cp_data: dict) -> dict:
    """v0.20 leg of the 4-leg joint. Joint matrix uses prior legs from v0.16/v0.17/v0.18."""
    # v0.20 leg outcome shape
    v20_verdict = h_regime4_verdict["verdict"]

    # Check IL monotonicity at Recognition layer (descriptive)
    cell_c_mean_cp = cp_data["per_cell"]["C"]["mean_cp"]
    cell_a_mean_cp = cp_data["per_cell"]["A"]["mean_cp"]
    cell_b_mean_cp = cp_data["per_cell"]["B"]["mean_cp"]
    monotonic = cell_c_mean_cp <= cell_a_mean_cp <= cell_b_mean_cp

    # Per pre-reg §6.4 verdict matrix
    if v20_verdict == "CONFIRMED" and monotonic:
        joint_verdict = "CONFIRMED-bounded"
        reason = "v0.20 CONFIRMED with monotonic IL signature C→A→B"
    elif v20_verdict == "PARTIAL":
        joint_verdict = "PARTIAL"
        reason = "v0.20 PARTIAL (joint with v0.16 PARTIAL × v0.17 FALSIFIED-on-panel-inadequacy × v0.18 PARTIAL)"
    elif v20_verdict == "FALSIFIED" and "panel inadequacy" in h_regime4_verdict.get("reason", "").lower():
        joint_verdict = "INDETERMINATE"
        reason = "v0.20 FALSIFIED on panel inadequacy; rerun on adequate panel"
    elif v20_verdict == "FALSIFIED":
        joint_verdict = "NARROWED"
        reason = "v0.20 FALSIFIED (not on panel inadequacy)"
    else:
        joint_verdict = "UNRESOLVED"
        reason = f"v0.20 returned {v20_verdict}; joint not classifiable"

    return {
        "primary": False,
        "joint_legs": ["v0.16 PARTIAL", "v0.17 FALSIFIED-on-panel-inadequacy", "v0.18 PARTIAL", f"v0.20 {v20_verdict}"],
        "v0_19_excluded_rationale": "uniform-IL design; no contribution to moderator",
        "verdict": joint_verdict,
        "reason": reason,
        "v0_20_leg_verdict": v20_verdict,
        "il_signature": {
            "cell_c_mean_cp": cell_c_mean_cp,
            "cell_a_mean_cp": cell_a_mean_cp,
            "cell_b_mean_cp": cell_b_mean_cp,
            "monotonic_c_a_b": monotonic,
        },
    }


# --- Main --------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description="AIAS v0.20 scoring runner")
    parser.add_argument("--registry", default=str(DEFAULT_REGISTRY))
    parser.add_argument("--phase-a", default=str(DEFAULT_DATA_DIR / "phase_a_results.csv"))
    parser.add_argument("--phase-b", default=str(DEFAULT_DATA_DIR / "phase_b_results.csv"))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args()

    registry_path = Path(args.registry).expanduser()
    phase_a_path = Path(args.phase_a).expanduser()
    phase_b_path = Path(args.phase_b).expanduser()
    output_path = Path(args.output).expanduser()

    for p, label in [(registry_path, "registry"), (phase_a_path, "Phase A CSV"),
                     (phase_b_path, "Phase B CSV")]:
        if not p.exists():
            print(f"ERROR: {label} not found at {p}", file=sys.stderr)
            return 2

    registry = load_registry(registry_path)
    phase_a_rows = load_phase_a(phase_a_path)
    phase_b_rows = load_phase_b(phase_b_path)
    thresholds = registry["thresholds"]

    print("AIAS v0.20 scoring runner")
    print(f"  Registry:    {registry_path}")
    print(f"  Phase A CSV: {phase_a_path}  ({len(phase_a_rows)} rows)")
    print(f"  Phase B CSV: {phase_b_path}  ({len(phase_b_rows)} rows)")
    print(f"  Lock state:  {registry.get('lock_state')}")

    # --- Phase A: C_P ---
    print("\n1/6  Computing Phase A C_P scores...")
    cp_data = compute_cp(phase_a_rows, registry)
    for cell_id, cell in cp_data["per_cell"].items():
        print(f"     Cell {cell_id} ({cell['label']:30s}) "
              f"mean C_P = {cell['mean_cp']:.2f}, "
              f"distinct = {cell['distinct_cp_count']}, "
              f"modal_share = {cell['modal_cp_share']:.3f}, "
              f"pivot = {cell['pivot_brand'] or '⚠ cascade exhausted'}")

    # --- Phase B: Recall ---
    print("\n2/6  Computing Phase B R_cat/R_cult via v1.4 mention detection...")
    recall_data = compute_recall(phase_b_rows, registry)
    for cell_id, cell in recall_data["per_cell"].items():
        print(f"     Cell {cell_id}: mean R_cat = {cell['mean_r_cat']:.2f}, "
              f"mean R_cult = {cell['mean_r_cult']:.2f}, "
              f"top-2 R_cat share = {cell['top2_r_cat_share']:.3f}")

    # --- Dissociation classification ---
    print("\n3/6  Classifying dissociation cases...")
    dissoc = classify_dissociations(cp_data, recall_data, thresholds)
    print(f"     Iwachu:  {dissoc['iwachu_count']} case(s) across cells {dissoc['iwachu_cells']}")
    print(f"     Type 1:  {dissoc['type_1_count']} case(s) across cells {dissoc['type_1_cells']}")
    print(f"     Type 2:  {dissoc['type_2_count']} case(s) across cells {dissoc['type_2_cells']}  ← PRIMARY HYPOTHESIS")

    # --- v1.5 C2 ---
    print("\n4/6  v1.5 C2 multi-statistic per cell...")
    c2 = compute_v15_c2(cp_data, thresholds)
    for cell_id, c in c2.items():
        status = "✓ pass" if c["passes"] else "✗ fail"
        print(f"     Cell {cell_id}: {status} ({c['reason']})")

    il_guard = compute_il_gradient_guard(recall_data, thresholds)
    print(f"\n     IL-gradient guard: Cell B {il_guard['cell_b_top2_r_cat_share']:.3f} − "
          f"Cell C {il_guard['cell_c_top2_r_cat_share']:.3f} = {il_guard['separation']:.3f} "
          f"({'✓ pass' if il_guard['passes'] else '✗ fail'})")

    # --- Phase D ρ ---
    print("\n5/6  Phase D Spearman ρ per cell (C_P × R_cat)...")
    rho = compute_phase_d_rho(cp_data, recall_data, registry)
    for cell_id, r in rho.items():
        rho_str = f"{r['rho']:.3f}" if r["rho"] is not None else "n/a"
        print(f"     Cell {cell_id}: ρ = {rho_str}  (n = {r['n']})")

    # --- Hypothesis resolution ---
    print("\n6/6  Resolving pre-registered hypotheses...")
    h_type2 = resolve_h_type2_emergence(dissoc, recall_data)
    h_regime4 = resolve_h_regime4(cp_data, c2, il_guard, rho, registry, thresholds)
    h_dissoc = resolve_h_dissociation_generalization(dissoc)
    h_il = resolve_h_identity_load_moderator(h_regime4, cp_data)

    print(f"\n     H_Type2_emergence (PRIMARY):                    {h_type2['verdict']}")
    print(f"       └─ {h_type2['reason']}")
    print(f"     H_Regime4_skincare:                              {h_regime4['verdict']}")
    print(f"       └─ {h_regime4['reason']}")
    print(f"     H_Dissociation_substrate_generalization:         {h_dissoc['verdict']}")
    print(f"       └─ {h_dissoc['reason']}")
    print(f"     H_IdentityLoad_moderator (4-leg joint):          {h_il['verdict']}")
    print(f"       └─ {h_il['reason']}")

    # --- Write verdicts JSON ---
    verdicts = {
        "phase": "v0.20",
        "scoring_timestamp": datetime.now(timezone.utc).isoformat(),
        "lock_state": registry.get("lock_state"),
        "registry_path": str(registry_path),
        "phase_a_source": str(phase_a_path),
        "phase_b_source": str(phase_b_path),
        "phase_a": cp_data,
        "phase_b": recall_data,
        "phase_d_rho_per_cell": rho,
        "v1_5_c2_per_cell": c2,
        "il_gradient_guard": il_guard,
        "dissociation": dissoc,
        "hypotheses": {
            "H_Type2_emergence": h_type2,
            "H_Regime4_skincare": h_regime4,
            "H_Dissociation_substrate_generalization": h_dissoc,
            "H_IdentityLoad_moderator": h_il,
        },
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(verdicts, f, indent=2, default=str)
    print(f"\n✓ Verdicts written: {output_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
