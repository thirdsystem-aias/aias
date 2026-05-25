#!/usr/bin/env python3
"""
score_v22.py — AIAS v0.22 scoring runner.

Consumes the raw acquisition outputs from run_acquisition_v22.py and produces:
  1. Per-brand C_P (Phase A Recognition score, 0–6).
  2. Per-brand R_cat and R_cult (Phase B Recall scores from six-frame battery),
     via v1.4 canonical brand-mention detection.
  3. NEW for v0.22: Per-brand R_phantom_defunct on Cell D — count of
     unprompted Cell D appearances in R_cat responses across the 6-model
     panel × 3 R_cat probes (max 18). For Cell D brands this is identical
     to R_cat; tracked separately for hypothesis-resolver clarity.
  4. NEW for v0.22: R_phantom on Cell A_Heritage — operationally identical
     to R_cat for Cell A brands; tracked separately per v1.6 Inc3 framing
     for H_Phantom_Brand_Persistence_heritage resolution.
  5. Dissociation classification:
       - Iwachu: C_P ≥ 5 ∧ R_cat ≤ 2
       - Type 1: R_cat ≥ 5 ∧ R_cult ≤ 2
       - Type 2: R_cat ≤ 2 ∧ R_cult ≥ 5
  6. v1.5 C2 multi-statistic per cell (distinct C_P ≥ 3 ∧ modal share ≤ 0.625).
  7. C2 IL-gradient guard (Cell B top-2 R_cat share − Cell C top-2 R_cat share ≥ 0.10).
  8. Per-cell Phase D Spearman ρ (C_P vs R_cat) with bootstrap CI.
  9. v1.6 Inc1 substrate Recognition pre-screen (uniform vs differential).
 10. v1.6 Inc2 IL Direct (R4-independent; Cell A vs Cell B Recall-channel ratio).
 11. Verdict resolution for the six pre-registered hypotheses:
       - H_Phantom_Defunct (LEAD, v1.6 Inc3 on Cell D)
       - H_Phantom_Brand_Persistence_heritage (PRIMARY SUPPORTING, v1.6 Inc3 on Cell A)
       - H_Regime4_automotive
       - H_Dissoc_substrate_generalization (6th substrate family extension)
       - H_IdentityLoad_direct (v1.6 Inc2)
       - H_SubstrateRecognition_PreScreen (v1.6 Inc1)

Output: v22_verdicts.json at the OSF v22 directory.

Forked from score_v21.py with the following deltas:
  - Reads pre-reg from Python module (prereg/v0_22_automotive_content.py).
  - 4-cell iteration (A/B/C/D) throughout; Cell D added.
  - Embedded methodology thresholds (the v21 JSON registry had a "thresholds"
    block; v22's Python module does not, so canonical thresholds from v1.5
    and v1.6 are embedded as METHODOLOGY_THRESHOLDS constant).
  - NEW R_phantom_defunct measurement on Cell D.
  - NEW H_Phantom_Defunct (LEAD) verdict resolution per pre-reg r2 N=4 floor.
  - NEW H_Phantom_Brand_Persistence_heritage verdict resolution.
  - NEW H_IdentityLoad_direct (v1.6 Inc2) replaces v21's H_IdentityLoad_moderator.
  - NEW H_SubstrateRecognition_PreScreen (v1.6 Inc1) classification.
  - Verdicts JSON output schema includes phantom_brand_persistence block,
    h_phantom_defunct_status, h_phantom_defunct_threshold, panel_n, and
    max_r_channel for downstream chart pipeline (build_charts_v22.py).

Required pip packages:
    scipy   (for Spearman ρ)

Usage:
    python score_v22.py                          # default paths
    python score_v22.py --prereg <path>          # override pre-reg module path
    python score_v22.py --phase-a <csv> --phase-b <csv>   # override input paths
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

DEFAULT_PREREG_MODULE = (
    Path.home() / "aias" / "prereg" / "v0_22_automotive_content.py"
)
DEFAULT_DATA_DIR = Path.home() / "aias" / "osf" / "v22"
DEFAULT_OUTPUT = DEFAULT_DATA_DIR / "v22_verdicts.json"

# Canonical methodology thresholds embedded (v21's JSON registry held these
# in a "thresholds" block; v22's Python pre-reg module does not, so the
# canonical v1.5 / v1.6 constants live here as the program-level lock.)
METHODOLOGY_THRESHOLDS = {
    # Dissociation classifiers (v1.4 canonical)
    "Iwachu_CP_min":   5,
    "Iwachu_Rcat_max": 2,
    "Type1_Rcat_min":  5,
    "Type1_Rcult_max": 2,
    "Type2_Rcat_max":  2,
    "Type2_Rcult_min": 5,
    # v1.5 C2 multi-statistic per cell
    "distinct_CP_min":    3,
    "modal_CP_share_max": 0.625,
    # Regime 4 routing
    "n_floor_worldwide":     12,
    "n_floor_per_cell_for_C3": 5,
    "rho_C3_min":            0.50,
    "C3_cells_clearing_min": 2,
    "IL_gradient_separation_min": 0.10,
    # v1.6 Inc1 substrate Recognition pre-screen
    "substrate_recog_uniform_modal_CP_min": 5,
    # v0.22 Phantom Brand Persistence (v1.6 Inc3) — locked at v0.22-prereg-r2
    "H_Phantom_Defunct_CONFIRMED_min": 4,   # max-18 scale
    "H_Phantom_Defunct_PARTIAL_min":   1,
    "H_Phantom_BrandPersistence_heritage_CONFIRMED_min": 8,
    "H_Phantom_BrandPersistence_heritage_PARTIAL_min":   4,
}

# Cell ID mapping: pre-reg module uses long-form keys ("Cell_A_Heritage")
# but the rest of the pipeline (chart + report) expects single-letter IDs.
CELL_KEY_TO_ID = {
    "Cell_A_Heritage":    "A",
    "Cell_B_Disruptor":   "B",
    "Cell_C_Mass_Legacy": "C",
    "Cell_D_Defunct":     "D",
}

CELL_LABELS = {
    "A": "Heritage",
    "B": "Disruptor",
    "C": "Mass-Legacy",
    "D": "Defunct",
}


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

def load_prereg_module(path: Path) -> dict:
    """Import the v0.22 pre-reg Python module and construct a registry dict
    matching the shape the scoring functions expect.

    Returns a dict with: phase, substrate, lock_state, reference_panel, cells.
    Each cell has: label, brands (list of {name, cascade_order}).
    """
    import importlib.util
    spec = importlib.util.spec_from_file_location("v22_prereg", str(path))
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load pre-reg module at {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    cells = {}
    for cell_key, brand_names in mod.REGISTRY.items():
        cell_id = CELL_KEY_TO_ID.get(cell_key)
        if cell_id is None:
            raise ValueError(f"Unknown cell key in registry: {cell_key}")
        cells[cell_id] = {
            "label":    CELL_LABELS[cell_id],
            "long_key": cell_key,
            "brands": [
                {"name": name, "cascade_order": i + 1}
                for i, name in enumerate(brand_names)
            ],
        }

    return {
        "phase":            "v0.22",
        "substrate":        "Automotive",
        "lock_state":       "v0.22-prereg-r2",
        "reference_panel":  mod.INSTRUMENT["panel_models"],
        "panel_n":          mod.INSTRUMENT["panel_n"],
        "max_c_p":          mod.INSTRUMENT["max_c_p"],
        "max_r_channel":    mod.INSTRUMENT["max_r_channel"],
        "cells":            cells,
    }


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
            "label":  cell["label"],
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


# --- Phantom Brand Persistence (v1.6 Inc3) — NEW for v0.22 -------------------

def compute_phantom_brand_persistence(recall_data: dict, registry: dict) -> dict:
    """v1.6 Inc3 Phantom Brand Persistence measurement.

    For each Cell A_Heritage and Cell D_Defunct brand, R_phantom is
    operationally identical to R_cat (count of unprompted mentions in
    R_cat channel responses across the n=6 panel × 3 R_cat probes, max 18).
    The 'phantom' framing differs from R_cat by interpretation, not
    measurement: R_phantom asks whether the AI mediation layer surfaces
    these brands unprompted at elevated rates (for heritage) or at all
    (for defunct).

    R_phantom_defunct on Cell D is the lead measurement for v0.22.
    R_phantom on Cell A supports H_Phantom_Brand_Persistence_heritage.
    """
    cell_a_phantom = {}
    cell_d_phantom = {}

    for brand_name, recall in recall_data["per_brand"].items():
        cell = recall["cell"]
        # R_phantom and R_phantom_defunct are R_cat per the operationalization
        # in pre-reg v0.22-prereg-r2. The naming preserves hypothesis semantics.
        if cell == "A":
            cell_a_phantom[brand_name] = recall["r_cat"]
        elif cell == "D":
            cell_d_phantom[brand_name] = recall["r_cat"]

    return {
        "cell_a":         cell_a_phantom,
        "cell_d":         cell_d_phantom,
        "cell_a_max":     max(cell_a_phantom.values()) if cell_a_phantom else 0,
        "cell_d_max":     max(cell_d_phantom.values()) if cell_d_phantom else 0,
        "cell_a_brands_above_8": [b for b, n in cell_a_phantom.items() if n >= 8],
        "cell_a_brands_4_to_7":  [b for b, n in cell_a_phantom.items() if 4 <= n < 8],
        "cell_d_brands_above_4": [b for b, n in cell_d_phantom.items() if n >= 4],
        "cell_d_brands_1_to_3":  [b for b, n in cell_d_phantom.items() if 1 <= n < 4],
    }


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
        # Status strings used by build_charts_v22.py for bottom-of-chart labels
        "h_status":          "TBD",  # populated by main() after H_Dissoc verdict
        "type_2_status":     "TBD",  # populated by main() (descriptive — v22 has no H_Type2)
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

def resolve_h_phantom_defunct(phantom: dict) -> dict:
    """LEAD hypothesis for v0.22.

    CONFIRMED  any Cell D brand R_phantom_defunct >= 4   (locked at r2)
    PARTIAL    >=1 Cell D brand with 1 <= R_phantom_defunct < 4
    FALSIFIED  all Cell D brands R_phantom_defunct = 0
    """
    confirmed_min = METHODOLOGY_THRESHOLDS["H_Phantom_Defunct_CONFIRMED_min"]
    partial_min   = METHODOLOGY_THRESHOLDS["H_Phantom_Defunct_PARTIAL_min"]

    cell_d = phantom["cell_d"]
    if not cell_d:
        return {"primary": True, "lead": True, "verdict": "INDETERMINATE",
                "reason": "Cell D is empty", "panel_size": 0}

    max_phantom = max(cell_d.values())
    brands_at_confirmed = [b for b, n in cell_d.items() if n >= confirmed_min]
    brands_at_partial   = [b for b, n in cell_d.items() if partial_min <= n < confirmed_min]
    brands_at_zero      = [b for b, n in cell_d.items() if n == 0]

    if brands_at_confirmed:
        verdict = "CONFIRMED"
        reason = (f"Cell D brand(s) {brands_at_confirmed} reached "
                  f"R_phantom_defunct >= {confirmed_min}")
    elif brands_at_partial:
        verdict = "PARTIAL"
        reason = (f"Cell D brand(s) {brands_at_partial} surfaced "
                  f"with 1 <= R_phantom_defunct < {confirmed_min}; "
                  f"no brand reached the CONFIRMED floor")
    elif len(brands_at_zero) == len(cell_d):
        verdict = "FALSIFIED"
        reason = "All Cell D brands R_phantom_defunct = 0"
    else:
        verdict = "INDETERMINATE"
        reason = "Mixed Cell D state did not match any locked verdict bucket"

    return {
        "primary": True,
        "lead": True,
        "verdict": verdict,
        "reason": reason,
        "max_r_phantom_defunct": max_phantom,
        "cell_d_per_brand": cell_d,
        "brands_above_confirmed_floor": brands_at_confirmed,
        "brands_in_partial_band":        brands_at_partial,
        "threshold_history": {
            "r1": "CONFIRMED >= 3 on assumed max-12 scale (single-model error)",
            "r2": f"CONFIRMED >= {confirmed_min} on corrected max-18 scale (6-model panel)",
        },
    }


def resolve_h_phantom_brand_persistence_heritage(phantom: dict) -> dict:
    """PRIMARY SUPPORTING hypothesis for v0.22.

    CONFIRMED  any Cell A brand R_phantom >= 8
    PARTIAL    >=1 Cell A brand with 4 <= R_phantom < 8
    FALSIFIED  all Cell A R_phantom < 4
    """
    confirmed_min = METHODOLOGY_THRESHOLDS["H_Phantom_BrandPersistence_heritage_CONFIRMED_min"]
    partial_min   = METHODOLOGY_THRESHOLDS["H_Phantom_BrandPersistence_heritage_PARTIAL_min"]

    cell_a = phantom["cell_a"]
    if not cell_a:
        return {"primary": False, "verdict": "INDETERMINATE",
                "reason": "Cell A is empty"}

    max_phantom = max(cell_a.values())
    brands_at_confirmed = [b for b, n in cell_a.items() if n >= confirmed_min]
    brands_at_partial   = [b for b, n in cell_a.items() if partial_min <= n < confirmed_min]

    if brands_at_confirmed:
        verdict = "CONFIRMED"
        reason = (f"Cell A brand(s) {brands_at_confirmed} reached "
                  f"R_phantom >= {confirmed_min}")
    elif brands_at_partial:
        verdict = "PARTIAL"
        reason = (f"Cell A brand(s) {brands_at_partial} surfaced "
                  f"with {partial_min} <= R_phantom < {confirmed_min}")
    else:
        verdict = "FALSIFIED"
        reason = f"All Cell A R_phantom < {partial_min}"

    return {
        "primary": False,
        "verdict": verdict,
        "reason": reason,
        "max_r_phantom": max_phantom,
        "cell_a_per_brand": cell_a,
        "brands_above_confirmed_floor": brands_at_confirmed,
        "brands_in_partial_band":        brands_at_partial,
        "benchmark": "v0.21 Glossier R_phantom = 12",
    }


def resolve_h_regime4_automotive(cp_data: dict, c2: dict, il_guard: dict,
                                  rho: dict, registry: dict) -> dict:
    """Sequential C1 → C2 → IL-guard → C3, adapted for 4-cell automotive.

    Routing inherits v21 pattern: C2 failure in >= 2 cells → FALSIFIED;
    1 cell → PARTIAL; subsequent failures → PARTIAL; all clear → CONFIRMED.
    Iterates the four cells (A/B/C/D). Cell D enters C2 but does not enter
    the IL-gradient guard (which stays Cell B vs Cell C per pre-reg).
    """
    rho_min        = METHODOLOGY_THRESHOLDS["rho_C3_min"]
    rho_cells_min  = METHODOLOGY_THRESHOLDS["C3_cells_clearing_min"]
    n_floor        = METHODOLOGY_THRESHOLDS["n_floor_worldwide"]
    c3_n_min       = METHODOLOGY_THRESHOLDS["n_floor_per_cell_for_C3"]

    worldwide_n = sum(cell["n"] for cell in cp_data["per_cell"].values())
    c1_passes = worldwide_n >= n_floor

    c2_failing_cells = [c for c, v in c2.items() if not v["passes"]]
    c2_failing_count = len(c2_failing_cells)

    c3_clearing_cells = []
    c3_failing_cells = []
    for cell_id, r in rho.items():
        if r["n"] >= c3_n_min and r["rho"] is not None and r["rho"] >= rho_min:
            c3_clearing_cells.append(cell_id)
        else:
            c3_failing_cells.append(cell_id)
    c3_passes = len(c3_clearing_cells) >= rho_cells_min

    if not c1_passes:
        verdict = "FALSIFIED"
        reason = f"C1 fails: worldwide n = {worldwide_n} < {n_floor}"
        resolved_at = "C1"
    elif c2_failing_count >= 2:
        verdict = "FALSIFIED"
        reason = f"C2 fails in {c2_failing_count} of 4 cells: {c2_failing_cells}"
        resolved_at = "C2 (regime-floor failure)"
    elif c2_failing_count == 1:
        verdict = "PARTIAL"
        reason = f"C2 fails in exactly 1 cell: {c2_failing_cells[0]}"
        resolved_at = "C2"
    elif not il_guard["passes"]:
        verdict = "PARTIAL"
        reason = (f"C2 IL-gradient guard fails: separation "
                  f"{il_guard['separation']} < {il_guard['threshold']}")
        resolved_at = "C2 IL-gradient guard"
    elif not c3_passes:
        verdict = "PARTIAL"
        reason = (f"C3 fails: only {len(c3_clearing_cells)} cell(s) clear "
                  f"ρ >= {rho_min} (clearing: {c3_clearing_cells}; "
                  f"failing: {c3_failing_cells})")
        resolved_at = "C3"
    else:
        verdict = "CONFIRMED"
        reason = "All conditions clear (C1, C2, IL-gradient guard, C3)"
        resolved_at = "C3 (all clear)"

    return {
        "primary": False,
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


def resolve_h_dissoc_substrate_generalization(dissoc: dict) -> dict:
    """Iwachu-pattern extension to 6th substrate family.

    Per pre-reg v0.22-prereg-r2:
      GENERALIZED  >= 1 dissociation case in Cell A or B
      PARTIAL      cases exist but in one cell only (and not A or B)
      FALSIFIED    no dissociation cases
    """
    iwachu_cells = set(dissoc["iwachu_cells"])
    iwachu_in_a_or_b = bool(iwachu_cells & {"A", "B"})
    iwachu_count = dissoc["iwachu_count"]

    if iwachu_in_a_or_b:
        verdict = "GENERALIZED"
        reason = (f"Iwachu cases in {sorted(iwachu_cells)} of 4 cells "
                  f"(includes Cell A or B); 6th substrate family")
    elif iwachu_count > 0 and len(iwachu_cells) == 1:
        verdict = "PARTIAL"
        reason = f"Iwachu cases in 1 cell only ({sorted(iwachu_cells)}); not A or B"
    elif iwachu_count > 0:
        verdict = "PARTIAL"
        reason = (f"Iwachu cases in {sorted(iwachu_cells)} (non-substantive cells); "
                  f"no Cell A or B presence")
    else:
        verdict = "FALSIFIED"
        reason = "No Iwachu cases in any cell"

    return {
        "primary": False,
        "sixth_family_extension": True,
        "verdict": verdict,
        "reason": reason,
        "iwachu_count": iwachu_count,
        "iwachu_cells": dissoc["iwachu_cells"],
        "type_1_count": dissoc["type_1_count"],
        "type_1_cells": dissoc["type_1_cells"],
        "type_2_count": dissoc["type_2_count"],
        "type_2_cells": dissoc["type_2_cells"],
    }


def resolve_h_identity_load_direct(recall_data: dict) -> dict:
    """v1.6 Inc2 R4-independent IL Direct.

    Operationalization (interim — pending v1.6 Inc2 methodology paper detail):
      Cell-level IL signature = mean R_cult / mean R_cat (R4-independent
      because both quantities are Phase B Recall, not Phase A Recognition).
      Cell A high IL ⇒ cult-channel dominance ⇒ higher R_cult / R_cat ratio.
      Cell B compared to Cell A per pre-reg ('Cell A vs Cell B comparison').

    Verdict:
      CONFIRMED  IL_A > IL_B
      FALSIFIED  IL_A <= IL_B (reversed or null)
    """
    def cell_il(cell_id: str) -> float | None:
        cell = recall_data["per_cell"].get(cell_id)
        if cell is None:
            return None
        cat = cell.get("mean_r_cat", 0.0)
        cult = cell.get("mean_r_cult", 0.0)
        if cat <= 0:
            # Define IL as cult magnitude if cat is zero (avoids div-by-zero
            # while preserving cult-channel signal as the IL signature)
            return cult if cult > 0 else None
        return cult / cat

    il_a = cell_il("A")
    il_b = cell_il("B")
    il_c = cell_il("C")
    il_d = cell_il("D")

    if il_a is None or il_b is None:
        verdict = "INDETERMINATE"
        reason = "Cell A or Cell B IL signal undefined (insufficient data)"
    elif il_a > il_b:
        verdict = "CONFIRMED"
        reason = (f"Cell A IL = {il_a:.3f} > Cell B IL = {il_b:.3f} "
                  f"(cult/cat ratio; R4-independent)")
    else:
        verdict = "FALSIFIED"
        reason = (f"Cell A IL = {il_a:.3f} <= Cell B IL = {il_b:.3f} "
                  f"(reversed or null)")

    return {
        "primary": False,
        "verdict": verdict,
        "reason": reason,
        "operationalization": "mean R_cult / mean R_cat per cell (R4-independent)",
        "operationalization_note": (
            "v1.6 Inc2 specifies 'R4-independent bootstrap'; bootstrap CI not "
            "implemented in this scoring runner pending v1.6 methodology paper "
            "detail. Interim sign-of-difference test on raw ratio."
        ),
        "il_per_cell": {
            "A": round(il_a, 4) if il_a is not None else None,
            "B": round(il_b, 4) if il_b is not None else None,
            "C": round(il_c, 4) if il_c is not None else None,
            "D": round(il_d, 4) if il_d is not None else None,
        },
        "predicted": "CONFIRMED (high IL: A, D; low IL: B)",
    }


def resolve_h_substrate_recognition_prescreen(cp_data: dict) -> dict:
    """v1.6 Inc1 substrate Recognition pre-screen.

    Non-directional classification probe. Tests whether the substrate
    produces uniform Recognition saturation across cells, or differential.

    UNIFORM SATURATION: all cells modal_cp >= 5 (program-typical for
                       culturally pervasive substrates)
    DIFFERENTIAL:       any cell modal_cp < 5
    """
    modal_min = METHODOLOGY_THRESHOLDS["substrate_recog_uniform_modal_CP_min"]

    modal_per_cell = {}
    saturated_cells = []
    differential_cells = []
    for cell_id, cell in cp_data["per_cell"].items():
        modal = cell.get("modal_cp")
        modal_per_cell[cell_id] = modal
        if modal is not None and modal >= modal_min:
            saturated_cells.append(cell_id)
        else:
            differential_cells.append(cell_id)

    if not differential_cells:
        classification = "UNIFORM SATURATION"
        reason = f"All cells modal C_P >= {modal_min}: {modal_per_cell}"
    else:
        classification = "DIFFERENTIAL"
        reason = (f"Cells with modal C_P < {modal_min}: {differential_cells}; "
                  f"all-cell modal: {modal_per_cell}")

    return {
        "primary":        False,
        "classification": classification,
        "verdict":        classification,  # alias for downstream consistency
        "reason":         reason,
        "modal_per_cell": modal_per_cell,
        "saturated_cells":    saturated_cells,
        "differential_cells": differential_cells,
        "predicted":      "UNIFORM SATURATION (program-typical for culturally pervasive substrates)",
        "note":           "Non-directional classification probe.",
    }


# --- Main --------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description="AIAS v0.22 scoring runner")
    parser.add_argument("--prereg", default=str(DEFAULT_PREREG_MODULE),
                        help="Path to v0_22_automotive_content.py pre-reg module")
    parser.add_argument("--phase-a", default=str(DEFAULT_DATA_DIR / "phase_a_results.csv"))
    parser.add_argument("--phase-b", default=str(DEFAULT_DATA_DIR / "phase_b_results.csv"))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args()

    prereg_path = Path(args.prereg).expanduser()
    phase_a_path = Path(args.phase_a).expanduser()
    phase_b_path = Path(args.phase_b).expanduser()
    output_path = Path(args.output).expanduser()

    for p, label in [(prereg_path, "pre-reg module"),
                     (phase_a_path, "Phase A CSV"),
                     (phase_b_path, "Phase B CSV")]:
        if not p.exists():
            print(f"ERROR: {label} not found at {p}", file=sys.stderr)
            return 2

    registry = load_prereg_module(prereg_path)
    phase_a_rows = load_phase_a(phase_a_path)
    phase_b_rows = load_phase_b(phase_b_path)

    print("AIAS v0.22 scoring runner")
    print(f"  Pre-reg:     {prereg_path}")
    print(f"  Phase A CSV: {phase_a_path}  ({len(phase_a_rows)} rows)")
    print(f"  Phase B CSV: {phase_b_path}  ({len(phase_b_rows)} rows)")
    print(f"  Lock state:  {registry.get('lock_state')}")
    print(f"  Panel:       {registry.get('panel_n')} models; max C_P = "
          f"{registry.get('max_c_p')}; max R = {registry.get('max_r_channel')}")

    # --- Phase A: C_P ---
    print("\n1/8  Computing Phase A C_P scores...")
    cp_data = compute_cp(phase_a_rows, registry)
    for cell_id, cell in cp_data["per_cell"].items():
        print(f"     Cell {cell_id} ({cell['label']:14s}) "
              f"mean C_P = {cell['mean_cp']:.2f}, "
              f"distinct = {cell['distinct_cp_count']}, "
              f"modal_share = {cell['modal_cp_share']:.3f}, "
              f"pivot = {cell['pivot_brand'] or '⚠ cascade exhausted'}")

    # --- Phase B: Recall ---
    print("\n2/8  Computing Phase B R_cat/R_cult via v1.4 mention detection...")
    recall_data = compute_recall(phase_b_rows, registry)
    for cell_id, cell in recall_data["per_cell"].items():
        print(f"     Cell {cell_id}: mean R_cat = {cell['mean_r_cat']:.2f}, "
              f"mean R_cult = {cell['mean_r_cult']:.2f}, "
              f"top-2 R_cat share = {cell['top2_r_cat_share']:.3f}")

    # --- Phantom Brand Persistence (v1.6 Inc3) — NEW for v0.22 ---
    print("\n3/8  Computing Phantom Brand Persistence (v1.6 Inc3)...")
    phantom = compute_phantom_brand_persistence(recall_data, registry)
    print(f"     Cell A max R_phantom:         {phantom['cell_a_max']}")
    print(f"     Cell A brands >= 8:           {phantom['cell_a_brands_above_8']}")
    print(f"     Cell D max R_phantom_defunct: {phantom['cell_d_max']}")
    print(f"     Cell D brands >= 4:           {phantom['cell_d_brands_above_4']}  ← LEAD")
    print(f"     Cell D brands 1-3:            {phantom['cell_d_brands_1_to_3']}")

    # --- Dissociation classification ---
    print("\n4/8  Classifying dissociation cases...")
    dissoc = classify_dissociations(cp_data, recall_data, METHODOLOGY_THRESHOLDS)
    print(f"     Iwachu:  {dissoc['iwachu_count']} case(s) across cells {dissoc['iwachu_cells']}")
    print(f"     Type 1:  {dissoc['type_1_count']} case(s) across cells {dissoc['type_1_cells']}")
    print(f"     Type 2:  {dissoc['type_2_count']} case(s) across cells {dissoc['type_2_cells']}")

    # --- v1.5 C2 ---
    print("\n5/8  v1.5 C2 multi-statistic per cell...")
    c2 = compute_v15_c2(cp_data, METHODOLOGY_THRESHOLDS)
    for cell_id, c in c2.items():
        status = "✓ pass" if c["passes"] else "✗ fail"
        print(f"     Cell {cell_id}: {status} ({c['reason']})")

    il_guard = compute_il_gradient_guard(recall_data, METHODOLOGY_THRESHOLDS)
    print(f"\n     IL-gradient guard: Cell B {il_guard['cell_b_top2_r_cat_share']:.3f} − "
          f"Cell C {il_guard['cell_c_top2_r_cat_share']:.3f} = {il_guard['separation']:.3f} "
          f"({'✓ pass' if il_guard['passes'] else '✗ fail'})")

    # --- Phase D ρ ---
    print("\n6/8  Phase D Spearman ρ per cell (C_P × R_cat)...")
    rho = compute_phase_d_rho(cp_data, recall_data, registry)
    for cell_id, r in rho.items():
        rho_str = f"{r['rho']:.3f}" if r["rho"] is not None else "n/a"
        print(f"     Cell {cell_id}: ρ = {rho_str}  (n = {r['n']})")

    # --- Hypothesis resolution ---
    print("\n7/8  Resolving pre-registered hypotheses...")
    h_phantom_defunct = resolve_h_phantom_defunct(phantom)
    h_phantom_heritage = resolve_h_phantom_brand_persistence_heritage(phantom)
    h_regime4 = resolve_h_regime4_automotive(cp_data, c2, il_guard, rho, registry)
    h_dissoc = resolve_h_dissoc_substrate_generalization(dissoc)
    h_il_direct = resolve_h_identity_load_direct(recall_data)
    h_prescreen = resolve_h_substrate_recognition_prescreen(cp_data)

    print(f"\n     H_Phantom_Defunct (LEAD):                          {h_phantom_defunct['verdict']}")
    print(f"       └─ {h_phantom_defunct['reason']}")
    print(f"     H_Phantom_Brand_Persistence_heritage (SUPPORTING): {h_phantom_heritage['verdict']}")
    print(f"       └─ {h_phantom_heritage['reason']}")
    print(f"     H_Regime4_automotive:                              {h_regime4['verdict']}")
    print(f"       └─ {h_regime4['reason']}")
    print(f"     H_Dissoc_substrate_generalization (6th family):    {h_dissoc['verdict']}")
    print(f"       └─ {h_dissoc['reason']}")
    print(f"     H_IdentityLoad_direct (v1.6 Inc2):                 {h_il_direct['verdict']}")
    print(f"       └─ {h_il_direct['reason']}")
    print(f"     H_SubstrateRecognition_PreScreen (v1.6 Inc1):      {h_prescreen['classification']}")
    print(f"       └─ {h_prescreen['reason']}")

    # Backfill status strings on the dissoc dict for chart pipeline consumption
    dissoc["h_status"] = h_dissoc["verdict"]
    dissoc["type_2_status"] = (
        "EMERGED" if dissoc["type_2_count"] >= 3 else
        "PARTIAL" if dissoc["type_2_count"] >= 1 else
        "FALSIFIED"
    )

    # --- Write verdicts JSON ---
    print("\n8/8  Writing verdicts JSON...")
    verdicts = {
        "phase": "v0.22",
        "scoring_timestamp": datetime.now(timezone.utc).isoformat(),
        "lock_state": registry.get("lock_state"),
        "prereg_path": str(prereg_path),
        "phase_a_source": str(phase_a_path),
        "phase_b_source": str(phase_b_path),
        # Panel parameters for chart pipeline
        "panel_n":       registry.get("panel_n"),
        "max_c_p":       registry.get("max_c_p"),
        "max_r_channel": registry.get("max_r_channel"),
        # Phantom thresholds for chart pipeline
        "h_phantom_defunct_threshold": METHODOLOGY_THRESHOLDS["H_Phantom_Defunct_CONFIRMED_min"],
        "h_phantom_defunct_status":    h_phantom_defunct["verdict"],
        # Core scoring blocks (consumed by build_charts_v22 + build_report_v22)
        "phase_a": cp_data,
        "phase_b": recall_data,
        "phase_d_rho_per_cell": rho,
        "v1_5_c2_per_cell": c2,
        "il_gradient_guard": il_guard,
        "dissociation": dissoc,
        "phantom_brand_persistence": phantom,
        # Hypothesis verdicts (six locked in v0.22-prereg-r2)
        "hypotheses": {
            "H_Phantom_Defunct":                   h_phantom_defunct,
            "H_Phantom_Brand_Persistence_heritage": h_phantom_heritage,
            "H_Regime4_automotive":                h_regime4,
            "H_Dissoc_substrate_generalization":   h_dissoc,
            "H_IdentityLoad_direct":               h_il_direct,
            "H_SubstrateRecognition_PreScreen":    h_prescreen,
        },
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(verdicts, f, indent=2, default=str)
    print(f"\n✓ Verdicts written: {output_path}")
    print(f"\n  Next: python ~/aias/scripts/build_charts_v22.py")
    print(f"         python ~/aias/reports/build_report_v22.py")

    return 0


if __name__ == "__main__":
    sys.exit(main())
