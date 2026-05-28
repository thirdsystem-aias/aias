#!/usr/bin/env python3
"""
v0.26 — BSR × C_P Scoring and Hypothesis Testing
AIAS Presence × Amazon Best Sellers Rank: Cross-Substrate Predictive Validity

Reads BSR acquisition CSVs + C_P verdicts from source phases.
Runs all four pre-registered hypothesis tests.
Outputs verdicts JSON + summary report.

Usage:
    python3 scripts/score_v26.py [--verbose]

Requires: scipy, numpy (pip install scipy numpy --break-system-packages)
"""

import csv
import json
import sys
from pathlib import Path

import numpy as np
from scipy import stats

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

AIAS_ROOT = Path(__file__).resolve().parent.parent
BSR_DATA_DIR = AIAS_ROOT / "osf" / "v26" / "data"
VERDICTS_OUT = AIAS_ROOT / "osf" / "v26" / "v26_verdicts.json"

SUBSTRATES = {
    "kitchen_knives": {
        "bsr_csv": "v26_bsr_kitchen_knives.csv",
        "cp_source": AIAS_ROOT / "osf" / "v16" / "v16_verdicts.json",
        "source_phase": "v0.16",
    },
    "premium_kitchenware": {
        "bsr_csv": "v26_bsr_premium_kitchenware.csv",
        "cp_source": AIAS_ROOT / "osf" / "v17" / "v17_verdicts.json",
        "source_phase": "v0.17",
    },
    "audiophile_headphones": {
        "bsr_csv": "v26_bsr_audiophile_headphones.csv",
        "cp_source": AIAS_ROOT / "osf" / "v19" / "v19_verdicts.json",
        "source_phase": "v0.19",
    },
    "skincare": {
        "bsr_csv": "v26_bsr_skincare.csv",
        "cp_source": AIAS_ROOT / "osf" / "v20" / "v20_verdicts.json",
        "source_phase": "v0.20",
    },
    "cosmetics": {
        "bsr_csv": "v26_bsr_cosmetics.csv",
        "cp_source": AIAS_ROOT / "osf" / "v21" / "v21_verdicts.json",
        "source_phase": "v0.21",
    },
}


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_bsr_data(substrate_key: str) -> list[dict]:
    """Load BSR acquisition CSV for a substrate."""
    cfg = SUBSTRATES[substrate_key]
    csv_path = BSR_DATA_DIR / cfg["bsr_csv"]
    if not csv_path.exists():
        print(f"  ERROR: BSR CSV not found: {csv_path}")
        sys.exit(1)

    with open(csv_path) as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # Parse bsr_rank to int where present
    for row in rows:
        if row.get("bsr_rank") and row["bsr_rank"].strip():
            try:
                row["bsr_rank"] = int(row["bsr_rank"])
            except ValueError:
                row["bsr_rank"] = None
        else:
            row["bsr_rank"] = None

    return rows


def load_cp_scores(substrate_key: str) -> dict[str, int]:
    """Load C_P scores from source phase verdicts.

    Returns dict of {brand_name: C_P_score}.
    Handles multiple verdict JSON formats.
    """
    cfg = SUBSTRATES[substrate_key]
    vpath = cfg["cp_source"]
    if not vpath.exists():
        print(f"  ERROR: Verdicts file not found: {vpath}")
        sys.exit(1)

    with open(vpath) as f:
        data = json.load(f)

    # Extract C_P per brand — handle common verdict formats
    cp_scores = {}

    if "brands" in data:
        for brand_entry in data["brands"]:
            name = brand_entry.get("brand") or brand_entry.get("name", "")
            cp = brand_entry.get("C_P") or brand_entry.get("cp") or brand_entry.get("presence_index")
            if name and cp is not None:
                cp_scores[name] = int(cp)
    elif isinstance(data, dict):
        # Try direct brand→score mapping
        for key, val in data.items():
            if isinstance(val, dict) and ("C_P" in val or "cp" in val):
                cp_scores[key] = int(val.get("C_P") or val.get("cp"))
            elif isinstance(val, (int, float)):
                cp_scores[key] = int(val)

    return cp_scores


def merge_data(substrate_key: str) -> tuple[list[dict], list[dict]]:
    """Merge BSR + C_P data. Returns (listed_brands, absent_brands)."""
    bsr_rows = load_bsr_data(substrate_key)
    cp_scores = load_cp_scores(substrate_key)

    listed = []
    absent = []

    for row in bsr_rows:
        brand = row["brand"]
        cp = cp_scores.get(brand)

        if cp is None:
            # Try fuzzy match (case-insensitive)
            for cp_brand, cp_val in cp_scores.items():
                if cp_brand.lower() == brand.lower():
                    cp = cp_val
                    break

        if cp is None:
            print(f"    WARNING: No C_P score found for '{brand}' in {substrate_key}")
            continue

        merged = {
            "brand": brand,
            "C_P": cp,
            "amazon_status": row.get("amazon_status", "absent"),
            "bsr_rank": row.get("bsr_rank"),
            "asin": row.get("asin", ""),
        }

        if merged["amazon_status"] == "listed" and merged["bsr_rank"] is not None:
            listed.append(merged)
        else:
            absent.append(merged)

    return listed, absent


# ---------------------------------------------------------------------------
# Hypothesis tests
# ---------------------------------------------------------------------------

def test_h_pv_primary(all_substrate_results: dict) -> dict:
    """H_PV_Primary: Per-substrate Spearman ρ ≤ −0.40, p < 0.05, in ≥ 3/5."""
    passing = 0
    details = {}

    for sub, res in all_substrate_results.items():
        rho = res["spearman_rho"]
        p = res["spearman_p"]
        n = res["n_listed"]
        meets = rho <= -0.40 and p < 0.05

        details[sub] = {
            "rho": round(rho, 4),
            "p": round(p, 6),
            "n": n,
            "meets_threshold": meets,
        }
        if meets:
            passing += 1

    if passing >= 3:
        verdict = "CONFIRMED"
    elif passing >= 1:
        verdict = "PARTIAL"
    else:
        verdict = "FALSIFIED"

    return {
        "hypothesis": "H_PV_Primary",
        "label": "Per-substrate predictive validity",
        "verdict": verdict,
        "passing_substrates": passing,
        "total_substrates": 5,
        "thresholds": {"rho": -0.40, "p": 0.05, "min_substrates": 3},
        "details": details,
    }


def test_h_pv_pooled(all_listed: list[dict]) -> dict:
    """H_PV_Pooled: Pooled Spearman ρ ≤ −0.30, p < 0.01 on percentile-normalized BSR."""
    if len(all_listed) < 10:
        return {
            "hypothesis": "H_PV_Pooled",
            "verdict": "UNDETERMINED",
            "reason": f"Insufficient pooled data ({len(all_listed)} listed brands)",
        }

    cp_vals = np.array([r["C_P"] for r in all_listed])
    pctile_vals = np.array([r["bsr_pctile"] for r in all_listed])

    rho, p = stats.spearmanr(cp_vals, pctile_vals)

    if rho <= -0.30 and p < 0.01:
        verdict = "CONFIRMED"
    else:
        verdict = "FALSIFIED"

    return {
        "hypothesis": "H_PV_Pooled",
        "label": "Cross-substrate pooled correlation",
        "verdict": verdict,
        "rho": round(rho, 4),
        "p": round(p, 6),
        "n": len(all_listed),
        "thresholds": {"rho": -0.30, "p": 0.01},
    }


def test_h_pv_cell_a(all_listed: list[dict]) -> dict:
    """H_PV_CellA: C_P ≥ 4 brands have better BSR than C_P < 4, Mann-Whitney U."""
    cell_a = [r["bsr_pctile"] for r in all_listed if r["C_P"] >= 4]
    cell_other = [r["bsr_pctile"] for r in all_listed if r["C_P"] < 4]

    if len(cell_a) < 3 or len(cell_other) < 3:
        return {
            "hypothesis": "H_PV_CellA",
            "verdict": "UNDETERMINED",
            "reason": f"Insufficient split (Cell A: {len(cell_a)}, Other: {len(cell_other)})",
        }

    u_stat, p = stats.mannwhitneyu(cell_a, cell_other, alternative="less")
    median_a = float(np.median(cell_a))
    median_other = float(np.median(cell_other))
    correct_direction = median_a < median_other  # Lower pctile = better

    if p < 0.05 and correct_direction:
        verdict = "CONFIRMED"
    else:
        verdict = "FALSIFIED"

    return {
        "hypothesis": "H_PV_CellA",
        "label": "Cell A separation",
        "verdict": verdict,
        "U": float(u_stat),
        "p": round(p, 6),
        "median_cell_a": round(median_a, 2),
        "median_other": round(median_other, 2),
        "n_cell_a": len(cell_a),
        "n_other": len(cell_other),
        "correct_direction": correct_direction,
        "thresholds": {"p": 0.05},
    }


def test_h_pv_absent(all_listed: list[dict], all_absent: list[dict]) -> dict:
    """H_PV_Absent: Absent brands have lower C_P than listed brands."""
    if len(all_absent) < 5:
        return {
            "hypothesis": "H_PV_Absent",
            "verdict": "UNDETERMINED",
            "reason": f"Fewer than 5 absent brands ({len(all_absent)})",
            "n_absent": len(all_absent),
        }

    cp_listed = [r["C_P"] for r in all_listed]
    cp_absent = [r["C_P"] for r in all_absent]

    u_stat, p = stats.mannwhitneyu(cp_absent, cp_listed, alternative="less")
    mean_listed = float(np.mean(cp_listed))
    mean_absent = float(np.mean(cp_absent))
    correct_direction = mean_absent < mean_listed

    if correct_direction and p < 0.05:
        verdict = "CONFIRMED"
    elif correct_direction and p < 0.10:
        verdict = "PARTIAL"
    else:
        verdict = "FALSIFIED"

    return {
        "hypothesis": "H_PV_Absent",
        "label": "Absence-Presence alignment",
        "verdict": verdict,
        "U": float(u_stat),
        "p": round(p, 6),
        "mean_cp_listed": round(mean_listed, 2),
        "mean_cp_absent": round(mean_absent, 2),
        "n_listed": len(cp_listed),
        "n_absent": len(cp_absent),
        "correct_direction": correct_direction,
        "thresholds": {"p": 0.05, "min_absent": 5},
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="v0.26 BSR × C_P scoring")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    print("v0.26 Scoring: AIAS Presence × Amazon BSR")
    print("=" * 60)

    # Per-substrate analysis
    all_substrate_results = {}
    all_listed = []
    all_absent = []

    for sub_key in SUBSTRATES:
        print(f"\n--- {sub_key} ---")
        listed, absent = merge_data(sub_key)
        print(f"  Listed: {len(listed)} | Absent: {len(absent)}")

        if len(listed) >= 5:
            cp_vals = np.array([r["C_P"] for r in listed])
            bsr_vals = np.array([r["bsr_rank"] for r in listed])
            rho, p = stats.spearmanr(cp_vals, bsr_vals)

            print(f"  Spearman ρ = {rho:.4f}, p = {p:.6f}")

            all_substrate_results[sub_key] = {
                "spearman_rho": rho,
                "spearman_p": p,
                "n_listed": len(listed),
            }

            # Compute within-substrate percentile rank for pooling
            ranks = stats.rankdata(bsr_vals, method="average")
            pctiles = (ranks / len(ranks)) * 100
            for i, rec in enumerate(listed):
                rec["bsr_pctile"] = pctiles[i]

            all_listed.extend(listed)
        else:
            print(f"  Skipping correlation — too few listed brands ({len(listed)})")
            all_substrate_results[sub_key] = {
                "spearman_rho": float("nan"),
                "spearman_p": float("nan"),
                "n_listed": len(listed),
                "note": "insufficient data",
            }

        all_absent.extend(absent)

    # Run hypothesis tests
    print("\n" + "=" * 60)
    print("HYPOTHESIS TESTS")
    print("=" * 60)

    results = {
        "study": "v0.26 — AIAS Presence × Amazon BSR Predictive Validity",
        "protocol_lock": "v1.6",
        "n_substrates": 5,
        "n_brands_total": len(all_listed) + len(all_absent),
        "n_listed": len(all_listed),
        "n_absent": len(all_absent),
        "per_substrate": all_substrate_results,
        "hypotheses": {},
    }

    # H_PV_Primary
    h1 = test_h_pv_primary(all_substrate_results)
    results["hypotheses"]["H_PV_Primary"] = h1
    print(f"\nH_PV_Primary: {h1['verdict']} ({h1['passing_substrates']}/5 substrates)")

    # H_PV_Pooled
    h2 = test_h_pv_pooled(all_listed)
    results["hypotheses"]["H_PV_Pooled"] = h2
    print(f"H_PV_Pooled:  {h2['verdict']} (ρ={h2.get('rho', '—')}, p={h2.get('p', '—')})")

    # H_PV_CellA
    h3 = test_h_pv_cell_a(all_listed)
    results["hypotheses"]["H_PV_CellA"] = h3
    print(f"H_PV_CellA:   {h3['verdict']}")

    # H_PV_Absent
    h4 = test_h_pv_absent(all_listed, all_absent)
    results["hypotheses"]["H_PV_Absent"] = h4
    print(f"H_PV_Absent:  {h4['verdict']} (n_absent={h4.get('n_absent', len(all_absent))})")

    # Write verdicts
    VERDICTS_OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(VERDICTS_OUT, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nVerdicts written → {VERDICTS_OUT}")


if __name__ == "__main__":
    import argparse
    main()
