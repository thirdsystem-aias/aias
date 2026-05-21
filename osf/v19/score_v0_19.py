"""
score_v0_19.py — AIAS v0.19 Canonical Scoring Pipeline

Pre-registered scoring script. Locked at pre-reg commit alongside:
  - PRE_REGISTRATION_v0_19.md
  - panel_registry_v0_19.csv
  - thresholds_v0_19.json

Implements the analysis plan ex-ante. Run AFTER Phase A and Phase B
acquisition completes.

Outputs:
  - Per-cell C1, C2, C3 status
  - H_C3_Within_Cell_Variance verdict (PASS / PARTIAL / FALSIFIED / UNDETERMINED)
  - H_Recognition_Recall_Dissociation_Replication verdict
    (REPLICATED / PARTIAL / NOT_REPLICATED)
  - Cross-cultural robustness Δρ + bounded/substantive routing
  - H_CulturalFootprint_Dissociation_Sensitivity Type 1 / Type 2 case lists
    (descriptive, no verdict)

Author: Pablo Ulpiano González Castro
Pre-reg revision: r1
Pre-reg tag: v0.19-prereg-r1
"""

import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr


# ---------------------------------------------------------------------------
# Paths (locked relative to script location)
# ---------------------------------------------------------------------------

SCRIPT_DIR = Path(__file__).parent
REGISTRY_PATH    = SCRIPT_DIR / "panel_registry_v0_19.csv"
THRESHOLDS_PATH  = SCRIPT_DIR / "thresholds_v0_19.json"
PHASE_A_PATH     = SCRIPT_DIR / "phase_a_results.csv"
PHASE_B_PATH     = SCRIPT_DIR / "phase_b_results.csv"

# Bootstrap RNG seed — locked for reproducibility
RNG_SEED = 42


# ---------------------------------------------------------------------------
# Loading
# ---------------------------------------------------------------------------

def load_registry(path):
    """Load the locked panel registry."""
    with open(path) as f:
        return list(csv.DictReader(f))


def load_thresholds(path):
    """Load the locked decision-rule thresholds."""
    with open(path) as f:
        return json.load(f)


def load_phase_a(path, registry):
    """
    Expected acquisition schema: brand,panel_model,recognition_yes (1|0)

    Returns dict: {brand: cp_score (0..6)}.
    Brands present in registry but absent from Phase A are defaulted to C_P=0.
    """
    cp = defaultdict(int)
    with open(path) as f:
        for row in csv.DictReader(f):
            if int(row["recognition_yes"]) == 1:
                cp[row["brand"]] += 1
    for r in registry:
        cp.setdefault(r["brand"], 0)
    return dict(cp)


def load_phase_b(path, registry):
    """
    Expected acquisition schema: brand,panel_model,frame,mentioned (1|0),rank (int|"")

    Frame identifiers expected: q1_audiophile, q2_enthusiast, q3_reference
    (load-bearing); q4_famous, q5_popular, q6_iconic (sensitivity).

    Returns (load_bearing_mentions, sensitivity_mentions) — two dicts
    keyed by brand with mention counts 0..18.
    """
    LOAD_BEARING = {"q1_audiophile", "q2_enthusiast", "q3_reference"}
    SENSITIVITY  = {"q4_famous", "q5_popular", "q6_iconic"}

    lb   = defaultdict(int)
    sens = defaultdict(int)
    with open(path) as f:
        for row in csv.DictReader(f):
            if int(row["mentioned"]) != 1:
                continue
            frame = row["frame"]
            if frame in LOAD_BEARING:
                lb[row["brand"]] += 1
            elif frame in SENSITIVITY:
                sens[row["brand"]] += 1
            else:
                raise ValueError(f"Unrecognized frame in Phase B: {frame}")

    for r in registry:
        lb.setdefault(r["brand"], 0)
        sens.setdefault(r["brand"], 0)
    return dict(lb), dict(sens)


# ---------------------------------------------------------------------------
# C1 — Panel adequacy
# ---------------------------------------------------------------------------

def check_c1(registry, thresholds):
    """
    C1 = panel adequacy.
      - worldwide n >= thresholds.c1_panel_adequacy.worldwide_min_post_attrition
      - per-cell n >= thresholds.c1_panel_adequacy.per_cell_min_post_attrition

    For v0.19, post-attrition n equals the acquired n (no brands are filtered
    by signal-strength; a brand with C_P=0 and zero mentions remains in panel
    and contributes to verdict per Rule 1 of DEVIATIONS).
    """
    t = thresholds["c1_panel_adequacy"]
    worldwide_n = len(registry)
    per_cell = Counter(r["cell"] for r in registry)

    worldwide_pass = worldwide_n >= t["worldwide_min_post_attrition"]
    per_cell_pass = {cell: n >= t["per_cell_min_post_attrition"]
                     for cell, n in per_cell.items()}

    overall_pass = worldwide_pass and all(per_cell_pass.values())
    return {
        "pass": overall_pass,
        "worldwide_n": worldwide_n,
        "worldwide_floor": t["worldwide_min_post_attrition"],
        "worldwide_pass": worldwide_pass,
        "per_cell_n": dict(per_cell),
        "per_cell_floor": t["per_cell_min_post_attrition"],
        "per_cell_pass": per_cell_pass,
    }


# ---------------------------------------------------------------------------
# C2 — Within-cell variance adequacy
# ---------------------------------------------------------------------------

def modal_share(values):
    """Modal share = count of most common value / total count."""
    if not values:
        return 0.0
    counts = Counter(values)
    return counts.most_common(1)[0][1] / len(values)


def check_c2(registry, phase_a, phase_b_lb, thresholds):
    """
    C2 = within-cell variance adequacy.
    For each cell, modal share of C_P distribution AND modal share of
    load-bearing mention-count distribution must both be strictly below
    the threshold (default 0.50).
    """
    t = thresholds["c2_within_cell_variance"]
    cp_max = t["cp_modal_share_max"]
    mc_max = t["mention_count_modal_share_max"]

    cells = defaultdict(list)
    for r in registry:
        cells[r["cell"]].append(r["brand"])

    results = {}
    for cell, brands in cells.items():
        cp_values = [phase_a[b] for b in brands]
        mc_values = [phase_b_lb[b] for b in brands]
        cp_share = modal_share(cp_values)
        mc_share = modal_share(mc_values)
        cp_pass = cp_share < cp_max
        mc_pass = mc_share < mc_max
        results[cell] = {
            "pass": cp_pass and mc_pass,
            "cp_modal_share": cp_share,
            "cp_modal_share_pass": cp_pass,
            "mention_count_modal_share": mc_share,
            "mention_count_modal_share_pass": mc_pass,
            "cp_distribution": Counter(cp_values),
            "mention_count_distribution": Counter(mc_values),
        }
    return results


# ---------------------------------------------------------------------------
# C3 — Ranking coherence (Spearman ρ + percentile bootstrap CI)
# ---------------------------------------------------------------------------

def bootstrap_spearman_ci(x, y, n_resamples=10000, ci_level=0.95, seed=RNG_SEED):
    """
    Percentile bootstrap on Spearman ρ.
    Resampling unit: paired (x_i, y_i) tuples — brand-level.
    Returns (lower, upper) at the requested CI level, or (None, None)
    if too few non-degenerate resamples (n < 3 effective).
    """
    n = len(x)
    if n < 3:
        return None, None
    rng = np.random.default_rng(seed)
    rhos = []
    for _ in range(n_resamples):
        idx = rng.integers(0, n, size=n)
        x_s = [x[i] for i in idx]
        y_s = [y[i] for i in idx]
        # Degenerate samples (all-tied) produce undefined ρ — skip them.
        if len(set(x_s)) < 2 or len(set(y_s)) < 2:
            continue
        rho, _ = spearmanr(x_s, y_s)
        if np.isnan(rho):
            continue
        rhos.append(rho)
    if len(rhos) < 100:  # too few non-degenerate resamples to support a CI
        return None, None
    rhos.sort()
    alpha = (1.0 - ci_level) / 2.0
    lower = rhos[int(len(rhos) * alpha)]
    upper = rhos[int(len(rhos) * (1.0 - alpha)) - 1]
    return lower, upper


def compute_c3_for_cell(brands, phase_a, phase_b_lb, thresholds):
    """
    C3 for a single cell.
    Returns dict with rho, CI bounds, and CLEAR/FAIL status.
    """
    t = thresholds["c3_ranking_coherence"]
    cp = [phase_a[b] for b in brands]
    mc = [phase_b_lb[b] for b in brands]

    rho, _ = spearmanr(cp, mc)
    if np.isnan(rho):
        return {"status": "DEGENERATE", "rho": None, "ci_lower": None,
                "ci_upper": None, "n": len(brands)}

    ci_lower, ci_upper = bootstrap_spearman_ci(
        cp, mc,
        n_resamples=t["bootstrap_n_resamples"],
        ci_level=0.95,
        seed=RNG_SEED,
    )

    rho_pass = rho >= t["spearman_rho_min"]
    ci_pass = (ci_lower is not None) and (ci_lower > t["bootstrap_ci_lower_bound_min"])
    status = "CLEAR" if (rho_pass and ci_pass) else "FAIL"

    return {
        "status": status,
        "rho": rho,
        "rho_threshold": t["spearman_rho_min"],
        "rho_pass": rho_pass,
        "ci_lower": ci_lower,
        "ci_upper": ci_upper,
        "ci_lower_threshold": t["bootstrap_ci_lower_bound_min"],
        "ci_pass": ci_pass,
        "n": len(brands),
    }


def check_c3(registry, phase_a, phase_b_lb, c2_results, thresholds):
    """Compute C3 for each cell that cleared C2."""
    cells = defaultdict(list)
    for r in registry:
        cells[r["cell"]].append(r["brand"])

    out = {}
    for cell, brands in cells.items():
        if not c2_results[cell]["pass"]:
            out[cell] = {"status": "SKIPPED_C2_FAIL", "rho": None}
            continue
        out[cell] = compute_c3_for_cell(brands, phase_a, phase_b_lb, thresholds)
    return out


# ---------------------------------------------------------------------------
# Iwachu-pattern dissociation cases
# ---------------------------------------------------------------------------

def identify_iwachu_cases(registry, phase_a, phase_b_lb, thresholds):
    """
    Iwachu pattern: C_P >= 5/6 AND category-anchored mentions <= 2/18.
    """
    t = thresholds["iwachu_pattern"]
    cp_min = t["cp_min"]
    mc_max = t["category_anchored_mentions_max"]

    cases = []
    for r in registry:
        b = r["brand"]
        cp = phase_a[b]
        mc = phase_b_lb[b]
        if cp >= cp_min and mc <= mc_max:
            cases.append({
                "brand": b,
                "cell": r["cell"],
                "cp": cp,
                "mention_count_load_bearing": mc,
            })
    return cases


def route_dissociation_verdict(cases, thresholds):
    """Route to REPLICATED / PARTIAL / NOT_REPLICATED per matrix."""
    t = thresholds["dissociation_replication_verdict"]
    n = len(cases)
    if n >= t["replicated_min_cases"]:
        return "REPLICATED"
    if n >= t["partial_range_min"]:
        return "PARTIAL"
    return "NOT_REPLICATED"


# ---------------------------------------------------------------------------
# Cross-cultural robustness (DEVIATIONS Rule 6)
# ---------------------------------------------------------------------------

def cross_cultural_robustness(registry, phase_a, phase_b_lb, c2_results, thresholds):
    """
    For each cell, recompute C3 ρ excluding the pre-flagged cross-cultural
    brand(s). Δρ = primary_rho - robustness_rho.
    Routing: |Δρ| < 0.10 → bounded; |Δρ| >= 0.10 → substantive.
    """
    t = thresholds["cross_cultural_robustness"]
    flagged = set(t["exclusion_brands"])
    delta_threshold = t["delta_rho_bounded_threshold"]

    cells = defaultdict(list)
    for r in registry:
        cells[r["cell"]].append(r["brand"])

    out = {}
    for cell, brands in cells.items():
        flagged_in_cell = [b for b in brands if b in flagged]
        if not flagged_in_cell:
            out[cell] = {"flagged_brands": [], "applicable": False}
            continue
        if not c2_results[cell]["pass"]:
            out[cell] = {
                "flagged_brands": flagged_in_cell,
                "applicable": False,
                "note": "Cell failed C2; robustness not computed",
            }
            continue

        # Primary ρ
        primary = compute_c3_for_cell(brands, phase_a, phase_b_lb, thresholds)
        # Robustness ρ (exclude flagged brand[s])
        retained = [b for b in brands if b not in flagged]
        robustness = compute_c3_for_cell(retained, phase_a, phase_b_lb, thresholds)

        primary_rho = primary["rho"]
        rob_rho = robustness["rho"]
        if primary_rho is None or rob_rho is None:
            out[cell] = {
                "flagged_brands": flagged_in_cell,
                "applicable": True,
                "primary_rho": primary_rho,
                "robustness_rho": rob_rho,
                "delta_rho": None,
                "verdict": "DEGENERATE",
            }
            continue

        delta = primary_rho - rob_rho
        verdict = "BOUNDED" if abs(delta) < delta_threshold else "SUBSTANTIVE"
        out[cell] = {
            "flagged_brands": flagged_in_cell,
            "applicable": True,
            "primary_rho": primary_rho,
            "robustness_rho": rob_rho,
            "delta_rho": delta,
            "delta_threshold": delta_threshold,
            "verdict": verdict,
        }
    return out


# ---------------------------------------------------------------------------
# Cultural-footprint sensitivity (descriptive, no verdict)
# ---------------------------------------------------------------------------

def identify_cultural_footprint_cases(registry, phase_b_lb, phase_b_sens, thresholds):
    """
    Type 1 (category-channel-preferred): mentions_lb >= K AND mentions_sens <= 2
    Type 2 (cultural-channel-preferred): mentions_lb <= 2 AND mentions_sens >= K
    """
    t = thresholds["cultural_footprint_sensitivity"]
    t1 = t["type1_category_channel_preferred"]
    t2 = t["type2_cultural_channel_preferred"]

    type1, type2 = [], []
    for r in registry:
        b = r["brand"]
        lb = phase_b_lb[b]
        sens = phase_b_sens[b]
        if lb >= t1["category_anchored_mentions_min"] and sens <= t1["cultural_footprint_mentions_max"]:
            type1.append({"brand": b, "cell": r["cell"],
                          "mentions_category_anchored": lb,
                          "mentions_cultural_footprint": sens})
        if lb <= t2["category_anchored_mentions_max"] and sens >= t2["cultural_footprint_mentions_min"]:
            type2.append({"brand": b, "cell": r["cell"],
                          "mentions_category_anchored": lb,
                          "mentions_cultural_footprint": sens})
    return type1, type2


# ---------------------------------------------------------------------------
# H_C3 verdict routing
# ---------------------------------------------------------------------------

def route_h_c3_verdict(c1_result, c2_results, c3_results):
    """
    Route H_C3 per the ex-ante verdict matrix:
      UNDETERMINED if C1 fails OR C2 fails in either cell
      PASS         if both cells CLEAR C3
      PARTIAL      if exactly one cell CLEAR C3
      FALSIFIED    if both cells FAIL C3 (with both passing C2)
    """
    if not c1_result["pass"]:
        return "UNDETERMINED"
    if not all(c["pass"] for c in c2_results.values()):
        return "UNDETERMINED"

    statuses = [v["status"] for v in c3_results.values()]
    n_clear = statuses.count("CLEAR")
    if n_clear == len(statuses):
        return "PASS"
    if n_clear == 0:
        return "FALSIFIED"
    return "PARTIAL"


# ---------------------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------------------

def fmt_float(x, digits=3):
    return f"{x:.{digits}f}" if isinstance(x, (int, float)) and x is not None else "—"


def emit_report(c1, c2, c3, h_c3, iwachu, dissociation_verdict,
                cross_cultural, type1, type2):
    sep = "=" * 72
    print(sep)
    print("AIAS v0.19 — Canonical Scoring Output")
    print("Pre-reg tag: v0.19-prereg-r1")
    print(sep)

    print("\n[C1 — Panel Adequacy]")
    print(f"  Worldwide n = {c1['worldwide_n']} (floor {c1['worldwide_floor']}): "
          f"{'PASS' if c1['worldwide_pass'] else 'FAIL'}")
    for cell, n in c1["per_cell_n"].items():
        status = "PASS" if c1["per_cell_pass"][cell] else "FAIL"
        print(f"  {cell} n = {n} (floor {c1['per_cell_floor']}): {status}")

    print("\n[C2 — Within-cell variance adequacy]")
    for cell, r in c2.items():
        print(f"  {cell}:")
        print(f"    C_P modal share = {fmt_float(r['cp_modal_share'])} "
              f"({'PASS' if r['cp_modal_share_pass'] else 'FAIL'})")
        print(f"    Mention-count modal share = {fmt_float(r['mention_count_modal_share'])} "
              f"({'PASS' if r['mention_count_modal_share_pass'] else 'FAIL'})")
        print(f"    Cell C2: {'PASS' if r['pass'] else 'FAIL'}")

    print("\n[C3 — Ranking coherence (Spearman ρ + 95% bootstrap CI)]")
    for cell, r in c3.items():
        if r["status"] == "SKIPPED_C2_FAIL":
            print(f"  {cell}: SKIPPED (C2 failed)")
            continue
        print(f"  {cell}: ρ = {fmt_float(r['rho'])} "
              f"(threshold ≥ {fmt_float(r['rho_threshold'])}, "
              f"{'PASS' if r['rho_pass'] else 'FAIL'})")
        print(f"           CI [{fmt_float(r['ci_lower'])}, {fmt_float(r['ci_upper'])}] "
              f"(LB threshold > {fmt_float(r['ci_lower_threshold'])}, "
              f"{'PASS' if r['ci_pass'] else 'FAIL'})")
        print(f"           Cell C3: {r['status']}")

    print(f"\n[H_C3_Within_Cell_Variance verdict] → {h_c3}")

    print(f"\n[H_Recognition_Recall_Dissociation_Replication]")
    print(f"  Iwachu-pattern cases identified: {len(iwachu)}")
    for c in iwachu:
        print(f"    {c['brand']} ({c['cell']}): C_P={c['cp']}/6, "
              f"mentions={c['mention_count_load_bearing']}/18")
    print(f"  Verdict: {dissociation_verdict}")

    print(f"\n[Cross-cultural robustness (DEVIATIONS Rule 6)]")
    for cell, r in cross_cultural.items():
        if not r.get("applicable"):
            note = r.get("note", "No flagged brand in cell")
            print(f"  {cell}: not applicable ({note})")
            continue
        print(f"  {cell} (excluded: {', '.join(r['flagged_brands'])}):")
        print(f"    primary ρ = {fmt_float(r['primary_rho'])}, "
              f"robustness ρ = {fmt_float(r['robustness_rho'])}, "
              f"Δρ = {fmt_float(r['delta_rho'])}")
        print(f"    Routing: {r['verdict']}")

    print(f"\n[H_CulturalFootprint_Dissociation_Sensitivity — descriptive]")
    print(f"  Type 1 (category-channel-preferred): {len(type1)} cases")
    for c in type1:
        print(f"    {c['brand']} ({c['cell']}): "
              f"category={c['mentions_category_anchored']}/18, "
              f"cultural={c['mentions_cultural_footprint']}/18")
    print(f"  Type 2 (cultural-channel-preferred): {len(type2)} cases")
    for c in type2:
        print(f"    {c['brand']} ({c['cell']}): "
              f"category={c['mentions_category_anchored']}/18, "
              f"cultural={c['mentions_cultural_footprint']}/18")

    print("\n" + sep)


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def main():
    registry = load_registry(REGISTRY_PATH)
    thresholds = load_thresholds(THRESHOLDS_PATH)

    if not PHASE_A_PATH.exists() or not PHASE_B_PATH.exists():
        print("Phase A or Phase B acquisition data not found.")
        print(f"  Expected: {PHASE_A_PATH}")
        print(f"  Expected: {PHASE_B_PATH}")
        print("\nScoring requires post-acquisition data.")
        print("Configuration validated; registry loaded; thresholds loaded.")
        sys.exit(0)

    phase_a = load_phase_a(PHASE_A_PATH, registry)
    phase_b_lb, phase_b_sens = load_phase_b(PHASE_B_PATH, registry)

    c1 = check_c1(registry, thresholds)
    c2 = check_c2(registry, phase_a, phase_b_lb, thresholds)
    c3 = check_c3(registry, phase_a, phase_b_lb, c2, thresholds)
    h_c3 = route_h_c3_verdict(c1, c2, c3)

    iwachu = identify_iwachu_cases(registry, phase_a, phase_b_lb, thresholds)
    dissociation = route_dissociation_verdict(iwachu, thresholds)

    cross_cultural = cross_cultural_robustness(
        registry, phase_a, phase_b_lb, c2, thresholds
    )

    type1, type2 = identify_cultural_footprint_cases(
        registry, phase_b_lb, phase_b_sens, thresholds
    )

    emit_report(c1, c2, c3, h_c3, iwachu, dissociation,
                cross_cultural, type1, type2)


if __name__ == "__main__":
    main()
