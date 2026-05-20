"""
score_v18.py — v0.18 canonical scoring + verdict driver

Consumes:
  - data/phase_a/v0.18/phase_a_results.json   (from acquire_phase_a_v18.py)
  - data/phase_b/v0.18/phase_b_results.json   (from acquire_phase_b_v18.py — TBD)

Produces:
  - data/verdicts/v0_18_verdict.json          (machine-readable)
  - data/verdicts/v0_18_verdict.md            (human-readable, paper Results §)

Verdict scope per v0.18-prereg-r1 §2 (three orthogonal hypotheses):
  H_Regime4_indie_fragrance                       — within-phase substantive
  H_IdentityLoad_moderator                        — three-leg joint v0.16/v0.17/v0.18
  H_Recognition_Recall_dissociation_generalization — methodological generalization

Pre-reg lock:     v0.18-prereg-r1
Branch:           v0.18-il-gradient
Predecessor:      scripts/score_v17.py (Premium Kitchenware)

==============================================================
PRE-REG GAP CLOSED IN R3 — SCRIPT NOW LOCKED-CONSISTENT
==============================================================
§5.2 DISSOCIATION_NARROWED routing operationalized per pre-reg r3
§2.3 (Recognition–Recall correlation threshold). The script enforces:
  - Spearman ρ between Phase A C_P and Phase B mention count, pooled
    across all anchored brands
  - Threshold: ρ ≥ 0.5 AND bootstrap 95% CI lower bound > 0.3
  - Bootstrap: 10,000 brand-level resamples, percentile-method CI
  - Failure mode: ρ ≥ 0.5 ∧ CI lower ≤ 0.3 → DISSOCIATION_UNDETERMINED
    (NOT _NARROWED), guarding against small-n inflation
==============================================================
"""

import json
import random
from pathlib import Path
from datetime import datetime, timezone
from statistics import mean


# ============================================================
# Configuration — LOCKED per v0.18-prereg-r1
# ============================================================

PHASE = "v0.18"
PRE_REG_TAG = "v0.18-prereg-r1"

# Decision rule thresholds — carry-forward from v0.17 protocol
# (cite v0.17 score_v17.py for canonical values; do not redefine here)
C1_PANEL_ADEQUACY_FLOOR = 12              # worldwide n post-attrition ≥ 12, §4
C2_REGIME4_MENTION_THRESHOLD = None       # CITE FROM v17 score_v17.py
C3_RANKING_COHERENCE_THRESHOLD = None     # CITE FROM v17 score_v17.py

# Phase B output schema contract — script reads against this
PHASE_B_FRAMES = ("q1_niche", "q2_independent", "q3_perfumistas")
PHASE_B_OBS_PER_BRAND = 18                # 6 models × 3 frames

# Dissociation pattern thresholds — per pre-reg §2.3
DISSOCIATION_C_P_FLOOR = 5                # C_P ≥ 5/6
DISSOCIATION_MENTION_CEILING = 2          # Phase B mention rate ≤ 2/18

# Phase D ρ — planned from start per §4.1
PHASE_D_RHO_MIN_CELL_N = 5                # ρ computed when post-attrition n ≥ 5

# Recognition–Recall correlation parameters — locked in pre-reg r3 §2.3
RECOGNITION_RECALL_CORRELATION_THRESHOLD = 0.5    # ρ ≥ 0.5 strong-effect floor
RECOGNITION_RECALL_CI_LOWER_FLOOR = 0.3           # bootstrap 95% CI lower > 0.3
BOOTSTRAP_N_RESAMPLES = 10_000                    # brand-level resampling
BOOTSTRAP_RNG_SEED = 20260520                     # deterministic per pre-reg lock date

# Three-leg joint H_IdentityLoad_moderator inputs — predecessor verdicts
PREDECESSOR_VERDICTS = {
    "v0.16": "PARTIAL",      # SSRN 6791999
    "v0.17": "FALSIFIED",    # SSRN 6802261 — falsified on panel inadequacy
}


# ============================================================
# Phase B output schema contract
# ============================================================
# acquire_phase_b_v18.py must produce phase_b_results.json with shape:
#
# {
#   "phase": "v0.18",
#   "pre_reg_tag": "v0.18-prereg-r1",
#   "acquired_at_utc": "...",
#   "frames": ["q1_niche", "q2_independent", "q3_perfumistas"],
#   "reference_panel": [...],
#   "cells": {
#     "cell_a_designer_niche": {
#       "per_brand": [
#         {
#           "brand": "Maison Francis Kurkdjian",
#           "mention_count": 14,                          # of 18 = 6 × 3
#           "per_frame_per_model": {
#             "q1_niche": {"claude-opus-4-5": True, ...},
#             "q2_independent": {...},
#             "q3_perfumistas": {...}
#           },
#           "rank_per_frame": {...}                       # ranking within frame
#         }, ...
#       ]
#     }, ...
#   }
# }


# ============================================================
# Loaders
# ============================================================

def load_phase_a(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def load_phase_b(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


# ============================================================
# Per-brand metric computation
# ============================================================

def brand_mention_rate(brand_record: dict) -> int:
    """Phase B mention count for a brand (0..18)."""
    return brand_record["mention_count"]


def brand_c_p_score(phase_a_cell: dict, brand_name: str) -> int:
    """Phase A C_P score for a brand within its cell."""
    for rec in phase_a_cell["per_brand"]:
        if rec["brand"] == brand_name:
            return rec["c_p_score"]
    raise ValueError(f"Brand not in Phase A cell: {brand_name}")


def is_dissociation_case(c_p_score: int, mention_count: int) -> bool:
    """Iwachu-pattern check per §2.3."""
    return (c_p_score >= DISSOCIATION_C_P_FLOOR
            and mention_count <= DISSOCIATION_MENTION_CEILING)


# ============================================================
# Per-cell aggregates
# ============================================================

def cell_panel_n(phase_a_cell: dict, phase_b_cell: dict) -> int:
    """Post-attrition n for a cell — brands present in BOTH phases."""
    a_brands = {r["brand"] for r in phase_a_cell["per_brand"]}
    b_brands = {r["brand"] for r in phase_b_cell["per_brand"]}
    return len(a_brands & b_brands)


def cell_mention_concentration(phase_b_cell: dict) -> float:
    """
    Regime 4 signature input per C2 — Top-2-brand mention share
    over total cell mentions. [CARRY-FORWARD from v17 score_v17.py;
    confirm exact formulation before lock.]
    """
    counts = sorted([r["mention_count"] for r in phase_b_cell["per_brand"]],
                    reverse=True)
    total = sum(counts)
    if total == 0:
        return 0.0
    top_share = sum(counts[:2]) / total
    return top_share


def cell_phase_d_rho(phase_a_cell: dict, phase_b_cell: dict) -> float | None:
    """
    Phase D ρ per §4.1: Spearman rank correlation between
    Phase A C_P (per brand) and Phase B mention count (per brand)
    within the cell. Requires post-attrition n ≥ 5.

    Returns None if n < 5 (per PHASE_D_RHO_MIN_CELL_N).
    """
    paired = []
    for b_rec in phase_b_cell["per_brand"]:
        brand = b_rec["brand"]
        try:
            cp = brand_c_p_score(phase_a_cell, brand)
        except ValueError:
            continue
        paired.append((cp, b_rec["mention_count"]))

    n = len(paired)
    if n < PHASE_D_RHO_MIN_CELL_N:
        return None

    # Spearman ρ via rank transform + Pearson
    return _spearman(paired)


def _spearman(pairs: list[tuple[float, float]]) -> float:
    """Spearman ρ from raw (x, y) pairs."""
    xs = _ranks([p[0] for p in pairs])
    ys = _ranks([p[1] for p in pairs])
    n = len(pairs)
    mx, my = mean(xs), mean(ys)
    num = sum((xs[i] - mx) * (ys[i] - my) for i in range(n))
    dx = sum((xs[i] - mx) ** 2 for i in range(n)) ** 0.5
    dy = sum((ys[i] - my) ** 2 for i in range(n)) ** 0.5
    if dx == 0 or dy == 0:
        return 0.0
    return num / (dx * dy)


def _ranks(values: list[float]) -> list[float]:
    """Average-rank assignment for ties."""
    sorted_pairs = sorted(enumerate(values), key=lambda p: p[1])
    ranks = [0.0] * len(values)
    i = 0
    while i < len(sorted_pairs):
        j = i
        while j + 1 < len(sorted_pairs) and sorted_pairs[j + 1][1] == sorted_pairs[i][1]:
            j += 1
        avg_rank = (i + j) / 2 + 1
        for k in range(i, j + 1):
            ranks[sorted_pairs[k][0]] = avg_rank
        i = j + 1
    return ranks


def _bootstrap_spearman_ci(
    pairs: list[tuple[float, float]],
    n_resamples: int = BOOTSTRAP_N_RESAMPLES,
    seed: int = BOOTSTRAP_RNG_SEED,
    ci_level: float = 0.95,
) -> tuple[float, float, float]:
    """
    Bootstrap 95% CI for Spearman ρ via brand-level resampling (percentile method).
    Per pre-reg r3 §2.3.

    Returns (rho_point, ci_lower, ci_upper).
    """
    if len(pairs) < 5:
        return (0.0, 0.0, 0.0)
    rho_point = _spearman(pairs)
    rng = random.Random(seed)
    n = len(pairs)
    resampled_rhos = []
    for _ in range(n_resamples):
        sample = [pairs[rng.randrange(n)] for _ in range(n)]
        # Guard degenerate resamples (all-identical x or y) → ρ = 0
        if len({p[0] for p in sample}) < 2 or len({p[1] for p in sample}) < 2:
            resampled_rhos.append(0.0)
            continue
        resampled_rhos.append(_spearman(sample))
    resampled_rhos.sort()
    alpha = (1 - ci_level) / 2
    lower_idx = int(alpha * n_resamples)
    upper_idx = int((1 - alpha) * n_resamples) - 1
    return (rho_point, resampled_rhos[lower_idx], resampled_rhos[upper_idx])


# ============================================================
# Verdict logic
# ============================================================

def verdict_h_regime4(phase_a: dict, phase_b: dict) -> dict:
    """
    Within-phase Regime 4 verdict per pre-reg §2.1 (C1 → C2 → C3 cascade).
    """
    cell_diagnostics = {}
    total_n = 0
    for cell_name, a_cell in phase_a["cells"].items():
        b_cell = phase_b["cells"][cell_name]
        n = cell_panel_n(a_cell, b_cell)
        total_n += n
        cell_diagnostics[cell_name] = {
            "n_post_attrition": n,
            "mention_concentration_top2": cell_mention_concentration(b_cell),
            "phase_d_rho": cell_phase_d_rho(a_cell, b_cell),
        }

    # C1 — panel adequacy
    if total_n < C1_PANEL_ADEQUACY_FLOOR:
        return {
            "verdict": "NULL",
            "resolved_at": "C1",
            "reason": f"Panel inadequacy: worldwide n={total_n} < {C1_PANEL_ADEQUACY_FLOOR}",
            "cell_diagnostics": cell_diagnostics,
        }

    # C2 — Regime 4 signature (monotonic strengthening C → A → B)
    if C2_REGIME4_MENTION_THRESHOLD is None:
        return {
            "verdict": "BLOCKED",
            "resolved_at": "C2",
            "reason": "C2_REGIME4_MENTION_THRESHOLD not pinned — cite v17 score_v17.py value",
            "cell_diagnostics": cell_diagnostics,
        }
    # ... C2 logic invoking the threshold lifts from score_v17.py

    # C3 — ranking coherence
    # ... [parallel structure to v17]

    # Placeholder return until C2/C3 lifted from v17 source
    return {
        "verdict": "PENDING_V17_THRESHOLD_LIFT",
        "cell_diagnostics": cell_diagnostics,
    }


def verdict_h_il_moderator(v0_18_verdict: str) -> dict:
    """
    Three-leg joint H_IdentityLoad_moderator verdict per pre-reg §5.1.
    Predecessor legs: v0.16 PARTIAL, v0.17 FALSIFIED.
    """
    matrix = {
        "CONFIRMED": ("CONFIRMED",
                      "Higher-IL substrate produces stronger Regime 4 signature; "
                      "v0.17 reread as panel inadequacy artifact"),
        "PARTIAL":   ("PARTIAL",
                      "Moderator operates but bounded; substrate-specific qualifications"),
        "FALSIFIED": ("FALSIFIED",
                      "Identity Load does not moderate AI Availability across this gradient"),
        "NULL":      ("AMBIGUOUS-deferred",
                      "v0.18 panel inadequate; route to v0.19 with further substrate refinement"),
    }
    if v0_18_verdict not in matrix:
        return {
            "joint_verdict": "ERROR",
            "reason": f"Unexpected v0.18 leg verdict: {v0_18_verdict}",
        }
    joint, narrative = matrix[v0_18_verdict]
    return {
        "joint_verdict": joint,
        "predecessor_legs": PREDECESSOR_VERDICTS,
        "v0_18_leg": v0_18_verdict,
        "narrative": narrative,
    }


def verdict_h_dissociation(phase_a: dict, phase_b: dict) -> dict:
    """
    Methodological verdict per pre-reg §5.2.
    """
    # Identify dissociation cases per cell (Iwachu-pattern)
    cases_per_cell = {}
    all_paired_for_correlation = []

    for cell_name, a_cell in phase_a["cells"].items():
        b_cell = phase_b["cells"][cell_name]
        cell_cases = []
        for b_rec in b_cell["per_brand"]:
            brand = b_rec["brand"]
            try:
                cp = brand_c_p_score(a_cell, brand)
            except ValueError:
                continue
            all_paired_for_correlation.append((cp, b_rec["mention_count"]))
            if is_dissociation_case(cp, b_rec["mention_count"]):
                cell_cases.append({
                    "brand": brand,
                    "c_p_score": cp,
                    "mention_count": b_rec["mention_count"],
                })
        cases_per_cell[cell_name] = cell_cases

    cells_with_cases = sum(1 for cases in cases_per_cell.values() if len(cases) > 0)
    n_cells = len(cases_per_cell)
    total_cases = sum(len(cases) for cases in cases_per_cell.values())

    # Routing per §5.2 matrix (r3-locked thresholds)
    if total_cases == 0:
        if len(all_paired_for_correlation) < 5:
            return {
                "verdict": "DISSOCIATION_UNDETERMINED",
                "reason": "Insufficient anchored brands for correlation test (n < 5)",
                "cases_per_cell": cases_per_cell,
                "total_cases": 0,
            }
        rho, ci_lower, ci_upper = _bootstrap_spearman_ci(all_paired_for_correlation)
        correlation_strong = (
            rho >= RECOGNITION_RECALL_CORRELATION_THRESHOLD
            and ci_lower > RECOGNITION_RECALL_CI_LOWER_FLOOR
        )
        if correlation_strong:
            return {
                "verdict": "DISSOCIATION_NARROWED",
                "reason": "0 Iwachu-pattern cases; Recognition–Recall correlation strong per r3 §2.3",
                "spearman_rho_pooled": rho,
                "bootstrap_ci_95": [ci_lower, ci_upper],
                "n_brands_pooled": len(all_paired_for_correlation),
                "cases_per_cell": cases_per_cell,
            }
        return {
            "verdict": "DISSOCIATION_UNDETERMINED",
            "reason": (
                "0 cases; correlation not strong "
                f"(ρ={rho:.3f}, CI lower={ci_lower:.3f}; "
                f"requires ρ ≥ {RECOGNITION_RECALL_CORRELATION_THRESHOLD} "
                f"AND CI lower > {RECOGNITION_RECALL_CI_LOWER_FLOOR})"
            ),
            "spearman_rho_pooled": rho,
            "bootstrap_ci_95": [ci_lower, ci_upper],
            "n_brands_pooled": len(all_paired_for_correlation),
            "cases_per_cell": cases_per_cell,
        }

    if cells_with_cases == n_cells:
        return {
            "verdict": "DISSOCIATION_GENERALIZED",
            "narrative": "≥1 case in every cell; v1.4 multi-component claim strengthened across substrates",
            "cases_per_cell": cases_per_cell,
            "total_cases": total_cases,
        }

    return {
        "verdict": "DISSOCIATION_PARTIAL",
        "narrative": f"Cases present but cell-clustered ({cells_with_cases}/{n_cells} cells)",
        "cases_per_cell": cases_per_cell,
        "total_cases": total_cases,
    }


# ============================================================
# Emitters
# ============================================================

def emit_verdict_json(verdicts: dict, out_path: Path) -> None:
    payload = {
        "phase": PHASE,
        "pre_reg_tag": PRE_REG_TAG,
        "scored_at_utc": datetime.now(timezone.utc).isoformat(),
        "verdicts": verdicts,
    }
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)


def emit_verdict_md(verdicts: dict, out_path: Path) -> None:
    """Human-readable verdict for paper Results §."""
    h_r4 = verdicts["H_Regime4_indie_fragrance"]
    h_il = verdicts["H_IdentityLoad_moderator"]
    h_di = verdicts["H_Recognition_Recall_dissociation_generalization"]

    lines = [
        f"# v0.18 Verdict — Indie Fragrance / IL-Gradient",
        f"",
        f"**Pre-reg tag:** `{PRE_REG_TAG}`",
        f"**Scored:** {datetime.now(timezone.utc).isoformat()}",
        f"",
        f"## H_Regime4_indie_fragrance (within-phase)",
        f"**Verdict:** `{h_r4.get('verdict')}`",
        f"",
        f"## H_IdentityLoad_moderator (three-leg joint v0.16 × v0.17 × v0.18)",
        f"**Joint verdict:** `{h_il.get('joint_verdict')}`",
        f"",
        f"- v0.16: {PREDECESSOR_VERDICTS['v0.16']}",
        f"- v0.17: {PREDECESSOR_VERDICTS['v0.17']}",
        f"- v0.18: {h_il.get('v0_18_leg')}",
        f"",
        f"{h_il.get('narrative', '')}",
        f"",
        f"## H_Recognition_Recall_dissociation_generalization (methodological)",
        f"**Verdict:** `{h_di.get('verdict')}`",
        f"",
        f"Cases per cell: {sum(len(c) for c in h_di.get('cases_per_cell', {}).values())} total",
    ]
    with out_path.open("w", encoding="utf-8") as f:
        f.write("\n".join(lines))


# ============================================================
# Main
# ============================================================

def main():
    phase_a_path = Path(f"data/phase_a/{PHASE}/phase_a_results.json")
    phase_b_path = Path(f"data/phase_b/{PHASE}/phase_b_results.json")
    out_dir = Path("data/verdicts")
    out_dir.mkdir(parents=True, exist_ok=True)

    phase_a = load_phase_a(phase_a_path)
    phase_b = load_phase_b(phase_b_path)

    h_regime4 = verdict_h_regime4(phase_a, phase_b)
    h_il_moderator = verdict_h_il_moderator(h_regime4["verdict"])
    h_dissociation = verdict_h_dissociation(phase_a, phase_b)

    verdicts = {
        "H_Regime4_indie_fragrance": h_regime4,
        "H_IdentityLoad_moderator": h_il_moderator,
        "H_Recognition_Recall_dissociation_generalization": h_dissociation,
    }

    emit_verdict_json(verdicts, out_dir / "v0_18_verdict.json")
    emit_verdict_md(verdicts, out_dir / "v0_18_verdict.md")
    print(f"Verdicts emitted to {out_dir}/")

    # Surface BLOCKED states
    blocked = [k for k, v in verdicts.items()
               if str(v.get("verdict", "")).startswith("BLOCKED")
               or str(v.get("joint_verdict", "")).startswith("BLOCKED")]
    if blocked:
        print(f"\n⚠ BLOCKED verdicts pending pre-reg r3 closure: {blocked}")


if __name__ == "__main__":
    main()
