#!/usr/bin/env python3
"""
v0.26 — BSR × C_P Scoring and Hypothesis Testing
AIAS Presence × Amazon Best Sellers Rank: Cross-Substrate Predictive Validity

Re-authored against verified per-phase data shapes:
  v0.16: osf/v26/data/v16_cp_retrofit_aggregated.csv (brand, cp)
  v0.19: osf/v19/phase_a_results.csv → aggregate recognition_yes per brand
  v0.20: osf/v20/v20_verdicts.json → phase_a.per_brand.<brand>.cp
  v0.21: osf/v21/v21_verdicts.json → phase_a.per_brand.<brand>.cp (ceiling: all 6)

BSR data: osf/v26/data/v26_bsr_{substrate}.csv

Usage:
    python3 scripts/score_v26.py [--verbose]
"""

import argparse
import csv
import json
import sys
from pathlib import Path

import numpy as np
from scipy import stats

AIAS_ROOT = Path(__file__).resolve().parent.parent
BSR_DATA_DIR = AIAS_ROOT / "osf" / "v26" / "data"
VERDICTS_OUT = AIAS_ROOT / "osf" / "v26" / "v26_verdicts.json"

# ---------------------------------------------------------------------------
# Substrate config — verified data shapes
# ---------------------------------------------------------------------------

SUBSTRATES = {
    "kitchen_knives": {
        "bsr_csv": "v26_bsr_kitchen_knives.csv",
        "cp_loader": "retrofit_csv",
        "cp_path": "osf/v26/data/v16_cp_retrofit_aggregated.csv",
        "source_phase": "v0.16",
        "testable": True,  # within-substrate correlation possible
    },
    "audiophile_headphones": {
        "bsr_csv": "v26_bsr_audiophile_headphones.csv",
        "cp_loader": "phase_a_csv",
        "cp_path": "osf/v19/phase_a_results.csv",
        "source_phase": "v0.19",
        "testable": True,
    },
    "skincare": {
        "bsr_csv": "v26_bsr_skincare.csv",
        "cp_loader": "verdicts_json",
        "cp_path": "osf/v20/v20_verdicts.json",
        "source_phase": "v0.20",
        "testable": True,
    },
    "cosmetics": {
        "bsr_csv": "v26_bsr_cosmetics.csv",
        "cp_loader": "verdicts_json",
        "cp_path": "osf/v21/v21_verdicts.json",
        "source_phase": "v0.21",
        "testable": False,  # ceiling effect: all C_P=6
    },
}

# Note: premium_kitchenware (v0.17) dropped — phase halted, no C_P data


# ---------------------------------------------------------------------------
# C_P loaders — one per data shape
# ---------------------------------------------------------------------------

def load_cp_retrofit_csv(path: Path) -> dict[str, int]:
    """v0.16 retrofit: brand,cp,n_models CSV."""
    scores = {}
    with open(path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            brand = row["brand"].strip()
            cp = int(row["cp"])
            scores[brand] = cp
    return scores


def load_cp_phase_a_csv(path: Path) -> dict[str, int]:
    """v0.19: aggregate recognition_yes per brand from raw Phase A CSV."""
    brand_counts = {}
    with open(path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            brand = row["brand"].strip()
            rec = int(row["recognition_yes"])
            if brand not in brand_counts:
                brand_counts[brand] = 0
            brand_counts[brand] += rec
    return brand_counts


def load_cp_verdicts_json(path: Path) -> dict[str, int]:
    """v0.20/v0.21: phase_a.per_brand.<brand>.cp from verdicts JSON."""
    with open(path) as f:
        data = json.load(f)
    per_brand = data.get("phase_a", {}).get("per_brand", {})
    scores = {}
    for brand, info in per_brand.items():
        scores[brand] = int(info["cp"])
    return scores


def load_cp_scores(substrate_key: str) -> dict[str, int]:
    """Dispatch to correct loader."""
    cfg = SUBSTRATES[substrate_key]
    path = AIAS_ROOT / cfg["cp_path"]
    if not path.exists():
        print(f"  ERROR: C_P source not found: {path}")
        sys.exit(1)

    loader = cfg["cp_loader"]
    if loader == "retrofit_csv":
        return load_cp_retrofit_csv(path)
    elif loader == "phase_a_csv":
        return load_cp_phase_a_csv(path)
    elif loader == "verdicts_json":
        return load_cp_verdicts_json(path)
    else:
        raise ValueError(f"Unknown loader: {loader}")


# ---------------------------------------------------------------------------
# BSR loader
# ---------------------------------------------------------------------------

def load_bsr_data(substrate_key: str) -> list[dict]:
    """Load BSR CSV for a substrate."""
    cfg = SUBSTRATES[substrate_key]
    csv_path = BSR_DATA_DIR / cfg["bsr_csv"]
    if not csv_path.exists():
        print(f"  ERROR: BSR CSV not found: {csv_path}")
        sys.exit(1)

    rows = []
    with open(csv_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            bsr = row.get("bsr_rank", "").strip()
            row["bsr_rank"] = int(bsr) if bsr and bsr.isdigit() else None
            rows.append(row)
    return rows


# ---------------------------------------------------------------------------
# Merge
# ---------------------------------------------------------------------------

def merge_data(substrate_key: str) -> tuple[list[dict], list[dict]]:
    """Merge BSR + C_P. Returns (listed, absent)."""
    bsr_rows = load_bsr_data(substrate_key)
    cp_scores = load_cp_scores(substrate_key)

    listed = []
    absent = []

    for row in bsr_rows:
        brand = row["brand"].strip()

        # Find C_P — try exact match, then case-insensitive
        cp = cp_scores.get(brand)
        if cp is None:
            for cp_brand, cp_val in cp_scores.items():
                if cp_brand.lower().strip() == brand.lower().strip():
                    cp = cp_val
                    break

        if cp is None:
            print(f"    WARNING: No C_P for '{brand}' in {substrate_key}")
            continue

        merged = {
            "brand": brand,
            "C_P": cp,
            "amazon_status": row.get("amazon_status", "absent"),
            "bsr_rank": row.get("bsr_rank"),
        }

        if merged["amazon_status"] == "listed" and merged["bsr_rank"] is not None:
            listed.append(merged)
        else:
            absent.append(merged)

    return listed, absent


# ---------------------------------------------------------------------------
# Hypothesis tests
# ---------------------------------------------------------------------------

def test_h_pv_primary(substrate_results: dict) -> dict:
    """H_PV_Primary: Per-substrate Spearman rho <= -0.40, p < 0.05.
    Amended r2: 3 testable substrates, threshold >= 2/3."""
    testable = {k: v for k, v in substrate_results.items()
                if SUBSTRATES[k]["testable"]}
    passing = 0
    details = {}

    for sub, res in testable.items():
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

    n_testable = len(testable)
    if passing >= 2:
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
        "testable_substrates": n_testable,
        "thresholds": {"rho": -0.40, "p": 0.05, "min_substrates": 2},
        "amendment": "r2: reduced from 5 to 3 testable substrates; threshold 2/3",
        "details": details,
    }


def test_h_pv_pooled(all_listed: list[dict]) -> dict:
    """H_PV_Pooled: Pooled Spearman rho <= -0.30, p < 0.01."""
    if len(all_listed) < 10:
        return {
            "hypothesis": "H_PV_Pooled",
            "verdict": "UNDETERMINED",
            "reason": f"Insufficient pooled data ({len(all_listed)})",
        }

    cp_vals = np.array([r["C_P"] for r in all_listed])
    pctile_vals = np.array([r["bsr_pctile"] for r in all_listed])

    rho, p = stats.spearmanr(cp_vals, pctile_vals)

    verdict = "CONFIRMED" if (rho <= -0.30 and p < 0.01) else "FALSIFIED"

    return {
        "hypothesis": "H_PV_Pooled",
        "label": "Cross-substrate pooled correlation",
        "verdict": verdict,
        "rho": round(float(rho), 4),
        "p": round(float(p), 6),
        "n": len(all_listed),
        "thresholds": {"rho": -0.30, "p": 0.01},
        "note": "Includes v0.21 ceiling brands in pooled set",
    }


def test_h_pv_cell_a(all_listed: list[dict]) -> dict:
    """H_PV_CellA: C_P >= 4 brands have better BSR than C_P < 4."""
    cell_a = [r["bsr_pctile"] for r in all_listed if r["C_P"] >= 4]
    cell_other = [r["bsr_pctile"] for r in all_listed if r["C_P"] < 4]

    if len(cell_a) < 3 or len(cell_other) < 3:
        return {
            "hypothesis": "H_PV_CellA",
            "verdict": "UNDETERMINED",
            "reason": f"Insufficient split (A: {len(cell_a)}, Other: {len(cell_other)})",
        }

    u_stat, p = stats.mannwhitneyu(cell_a, cell_other, alternative="less")
    median_a = float(np.median(cell_a))
    median_other = float(np.median(cell_other))
    correct_direction = median_a < median_other

    verdict = "CONFIRMED" if (p < 0.05 and correct_direction) else "FALSIFIED"

    return {
        "hypothesis": "H_PV_CellA",
        "label": "Cell A separation",
        "verdict": verdict,
        "U": float(u_stat),
        "p": round(float(p), 6),
        "median_cell_a": round(median_a, 2),
        "median_other": round(median_other, 2),
        "n_cell_a": len(cell_a),
        "n_other": len(cell_other),
        "correct_direction": correct_direction,
    }


def test_h_pv_absent(all_listed: list[dict], all_absent: list[dict]) -> dict:
    """H_PV_Absent: Absent brands have lower C_P than listed."""
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
        "p": round(float(p), 6),
        "mean_cp_listed": round(mean_listed, 2),
        "mean_cp_absent": round(mean_absent, 2),
        "n_listed": len(cp_listed),
        "n_absent": len(cp_absent),
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="v0.26 BSR x C_P scoring")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    print("v0.26 Scoring: AIAS Presence x Amazon BSR")
    print("=" * 60)

    substrate_results = {}
    all_listed = []
    all_absent = []

    for sub_key, cfg in SUBSTRATES.items():
        print(f"\n--- {sub_key} ({cfg['source_phase']}) ---")
        listed, absent = merge_data(sub_key)
        print(f"  Listed: {len(listed)} | Absent: {len(absent)}")

        if args.verbose:
            for r in sorted(listed, key=lambda x: x["bsr_rank"]):
                print(f"    {r['brand']:30s}  C_P={r['C_P']}  BSR={r['bsr_rank']}")

        if cfg["testable"] and len(listed) >= 5:
            cp_vals = np.array([r["C_P"] for r in listed])
            bsr_vals = np.array([r["bsr_rank"] for r in listed])
            rho, p = stats.spearmanr(cp_vals, bsr_vals)
            print(f"  Spearman rho = {rho:.4f}, p = {p:.6f}")

            substrate_results[sub_key] = {
                "spearman_rho": float(rho),
                "spearman_p": float(p),
                "n_listed": len(listed),
            }
        elif not cfg["testable"]:
            print(f"  [ceiling] All C_P identical — no within-substrate rho")
            substrate_results[sub_key] = {
                "spearman_rho": float("nan"),
                "spearman_p": float("nan"),
                "n_listed": len(listed),
                "note": "ceiling effect — zero C_P variance",
            }
        else:
            print(f"  Insufficient listed brands ({len(listed)})")
            substrate_results[sub_key] = {
                "spearman_rho": float("nan"),
                "spearman_p": float("nan"),
                "n_listed": len(listed),
                "note": "insufficient data",
            }

        # Percentile rank for pooling (all substrates including ceiling)
        listed_with_bsr = [r for r in listed if r["bsr_rank"] is not None]
        if listed_with_bsr:
            bsr_vals = np.array([r["bsr_rank"] for r in listed_with_bsr])
            ranks = stats.rankdata(bsr_vals, method="average")
            pctiles = (ranks / len(ranks)) * 100
            for i, rec in enumerate(listed_with_bsr):
                rec["bsr_pctile"] = float(pctiles[i])
                rec["substrate"] = sub_key

        all_listed.extend(listed_with_bsr)
        all_absent.extend(absent)

    # Hypothesis tests
    print(f"\n{'=' * 60}")
    print("HYPOTHESIS TESTS")
    print(f"{'=' * 60}")

    results = {
        "study": "v0.26 — AIAS Presence x Amazon BSR Predictive Validity",
        "protocol_lock": "v1.6",
        "amendment": "r2 — v0.17 dropped, v0.21 ceiling-only, v0.16 retrofitted",
        "n_substrates_testable": 3,
        "n_substrates_ceiling": 1,
        "n_substrates_dropped": 1,
        "n_brands_total": len(all_listed) + len(all_absent),
        "n_listed": len(all_listed),
        "n_absent": len(all_absent),
        "per_substrate": substrate_results,
        "hypotheses": {},
    }

    h1 = test_h_pv_primary(substrate_results)
    results["hypotheses"]["H_PV_Primary"] = h1
    print(f"\nH_PV_Primary: {h1['verdict']} ({h1['passing_substrates']}/{h1['testable_substrates']} substrates)")

    h2 = test_h_pv_pooled(all_listed)
    results["hypotheses"]["H_PV_Pooled"] = h2
    print(f"H_PV_Pooled:  {h2['verdict']} (rho={h2.get('rho', '—')}, p={h2.get('p', '—')}, n={h2.get('n', '—')})")

    h3 = test_h_pv_cell_a(all_listed)
    results["hypotheses"]["H_PV_CellA"] = h3
    print(f"H_PV_CellA:   {h3['verdict']} (median A={h3.get('median_cell_a','—')} vs Other={h3.get('median_other','—')})")

    h4 = test_h_pv_absent(all_listed, all_absent)
    results["hypotheses"]["H_PV_Absent"] = h4
    print(f"H_PV_Absent:  {h4['verdict']} (n_absent={h4.get('n_absent', len(all_absent))})")

    # Write verdicts
    VERDICTS_OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(VERDICTS_OUT, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nVerdicts written -> {VERDICTS_OUT}")


if __name__ == "__main__":
    main()
