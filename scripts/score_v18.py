"""
score_v18.py — v0.18 canonical scoring + verdict driver

Consumes:
  - data/phase_a/v0.18/phase_a_results.json
  - data/phase_b/v0.18/phase_b_results.json

Produces:
  - data/verdicts/v0_18_verdict.json
  - data/verdicts/v0_18_verdict.md

Three orthogonal verdicts per pre-reg §2:
  H_Regime4_indie_fragrance                       — within-phase substantive
  H_IdentityLoad_moderator                        — three-leg joint v0.16/v0.17/v0.18
  H_Recognition_Recall_dissociation_generalization — methodological generalization

Pre-reg lock:     v0.18-prereg-r1 @ commit 183386c
Protocol version: v1.4

All thresholds imported from protocol/thresholds.py.
If C2/C3 thresholds are still None when this runs, score_v18.py will
emit a clear instruction telling you to lift them once into the
protocol layer (NOT into this file).

Phase B output schema contract (acquire_phase_b_v18.py must produce):
  {
    "phase": "v0.18",
    "frames": ["q1_niche", "q2_independent", "q3_perfumistas"],
    "cells": {
      "cell_<name>": {
        "per_brand": [
          {"brand": str, "mention_count": int (0..18),
           "per_frame_per_model": {frame: {model: bool}},
           "rank_per_frame": {frame: {model: int|None}}}, ...
        ]
      }, ...
    }
  }
"""

import json
import random
from pathlib import Path
from datetime import datetime, timezone
from statistics import mean

from protocol import PROTOCOL_VERSION
from protocol.thresholds import (
    C1_PANEL_ADEQUACY_FLOOR,
    C2_REGIME4_MENTION_THRESHOLD,
    C3_RANKING_COHERENCE_THRESHOLD,
    DISSOCIATION_C_P_FLOOR,
    DISSOCIATION_MENTION_CEILING,
    RECOGNITION_RECALL_CORRELATION_THRESHOLD,
    RECOGNITION_RECALL_CI_LOWER_FLOOR,
    BOOTSTRAP_N_RESAMPLES,
    BOOTSTRAP_RNG_SEED,
    PHASE_D_RHO_MIN_CELL_N,
)


PHASE = "v0.18"
PRE_REG_TAG = "v0.18-prereg-r1"

PHASE_B_FRAMES = ("q1_niche", "q2_independent", "q3_perfumistas")
PHASE_B_OBS_PER_BRAND = 18

PREDECESSOR_VERDICTS = {
    "v0.16": "PARTIAL",
    "v0.17": "FALSIFIED",
}


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
# Per-brand & per-cell helpers
# ============================================================

def brand_c_p_score(phase_a_cell: dict, brand_name: str) -> int:
    for rec in phase_a_cell["per_brand"]:
        if rec["brand"] == brand_name:
            return rec["c_p_score"]
    raise ValueError(f"Brand not in Phase A cell: {brand_name}")


def is_dissociation_case(c_p_score: int, mention_count: int) -> bool:
    return (c_p_score >= DISSOCIATION_C_P_FLOOR
            and mention_count <= DISSOCIATION_MENTION_CEILING)


def cell_panel_n(phase_a_cell: dict, phase_b_cell: dict) -> int:
    a_brands = {r["brand"] for r in phase_a_cell["per_brand"]}
    b_brands = {r["brand"] for r in phase_b_cell["per_brand"]}
    return len(a_brands & b_brands)


def cell_mention_concentration(phase_b_cell: dict) -> float:
    counts = sorted([r["mention_count"] for r in phase_b_cell["per_brand"]], reverse=True)
    total = sum(counts)
    return sum(counts[:2]) / total if total > 0 else 0.0


def cell_phase_d_rho(phase_a_cell: dict, phase_b_cell: dict) -> float | None:
    paired = []
    for b_rec in phase_b_cell["per_brand"]:
        try:
            cp = brand_c_p_score(phase_a_cell, b_rec["brand"])
        except ValueError:
            continue
        paired.append((cp, b_rec["mention_count"]))
    return _spearman(paired) if len(paired) >= PHASE_D_RHO_MIN_CELL_N else None


# ============================================================
# Spearman + bootstrap
# ============================================================

def _spearman(pairs: list[tuple[float, float]]) -> float:
    xs = _ranks([p[0] for p in pairs])
    ys = _ranks([p[1] for p in pairs])
    n = len(pairs)
    mx, my = mean(xs), mean(ys)
    num = sum((xs[i] - mx) * (ys[i] - my) for i in range(n))
    dx = sum((xs[i] - mx) ** 2 for i in range(n)) ** 0.5
    dy = sum((ys[i] - my) ** 2 for i in range(n)) ** 0.5
    return num / (dx * dy) if dx and dy else 0.0


def _ranks(values: list[float]) -> list[float]:
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
    if len(pairs) < 5:
        return (0.0, 0.0, 0.0)
    rho_point = _spearman(pairs)
    rng = random.Random(seed)
    n = len(pairs)
    resampled = []
    for _ in range(n_resamples):
        sample = [pairs[rng.randrange(n)] for _ in range(n)]
        if len({p[0] for p in sample}) < 2 or len({p[1] for p in sample}) < 2:
            resampled.append(0.0)
            continue
        resampled.append(_spearman(sample))
    resampled.sort()
    alpha = (1 - ci_level) / 2
    return (rho_point, resampled[int(alpha * n_resamples)], resampled[int((1 - alpha) * n_resamples) - 1])


# ============================================================
# Verdict logic
# ============================================================

def verdict_h_regime4(phase_a: dict, phase_b: dict) -> dict:
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

    if total_n < C1_PANEL_ADEQUACY_FLOOR:
        return {
            "verdict": "NULL",
            "resolved_at": "C1",
            "reason": f"Panel inadequacy: worldwide n={total_n} < {C1_PANEL_ADEQUACY_FLOOR}",
            "cell_diagnostics": cell_diagnostics,
        }

    if C2_REGIME4_MENTION_THRESHOLD is None or C3_RANKING_COHERENCE_THRESHOLD is None:
        return {
            "verdict": "BLOCKED",
            "resolved_at": "C2/C3",
            "reason": (
                "C2 and/or C3 thresholds still None in protocol/thresholds.py. "
                "ONE-TIME LIFT needed: open your existing v17 score script, "
                "find the C2 and C3 threshold constants, and copy the values "
                "into protocol/thresholds.py. After that, all future phases "
                "inherit. Do NOT add the values to this file."
            ),
            "cell_diagnostics": cell_diagnostics,
        }
    # C2/C3 evaluation lifts from v17 logic post-protocol-fill
    return {
        "verdict": "PENDING_PROTOCOL_FILL",
        "cell_diagnostics": cell_diagnostics,
    }


def verdict_h_il_moderator(v0_18_verdict: str) -> dict:
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
        return {"joint_verdict": "PENDING", "v0_18_leg": v0_18_verdict}
    joint, narrative = matrix[v0_18_verdict]
    return {
        "joint_verdict": joint,
        "predecessor_legs": PREDECESSOR_VERDICTS,
        "v0_18_leg": v0_18_verdict,
        "narrative": narrative,
    }


def verdict_h_dissociation(phase_a: dict, phase_b: dict) -> dict:
    cases_per_cell = {}
    all_paired = []

    for cell_name, a_cell in phase_a["cells"].items():
        b_cell = phase_b["cells"][cell_name]
        cell_cases = []
        for b_rec in b_cell["per_brand"]:
            try:
                cp = brand_c_p_score(a_cell, b_rec["brand"])
            except ValueError:
                continue
            all_paired.append((cp, b_rec["mention_count"]))
            if is_dissociation_case(cp, b_rec["mention_count"]):
                cell_cases.append({
                    "brand": b_rec["brand"], "c_p_score": cp,
                    "mention_count": b_rec["mention_count"],
                })
        cases_per_cell[cell_name] = cell_cases

    cells_with_cases = sum(1 for cases in cases_per_cell.values() if len(cases) > 0)
    n_cells = len(cases_per_cell)
    total_cases = sum(len(cases) for cases in cases_per_cell.values())

    if total_cases == 0:
        if len(all_paired) < 5:
            return {"verdict": "DISSOCIATION_UNDETERMINED",
                    "reason": "Insufficient anchored brands for correlation test (n < 5)",
                    "cases_per_cell": cases_per_cell, "total_cases": 0}
        rho, ci_lower, ci_upper = _bootstrap_spearman_ci(all_paired)
        strong = (rho >= RECOGNITION_RECALL_CORRELATION_THRESHOLD
                  and ci_lower > RECOGNITION_RECALL_CI_LOWER_FLOOR)
        return {
            "verdict": "DISSOCIATION_NARROWED" if strong else "DISSOCIATION_UNDETERMINED",
            "reason": (
                "0 Iwachu-pattern cases; correlation strong per r3 §2.3" if strong
                else f"0 cases; correlation not strong (ρ={rho:.3f}, CI lower={ci_lower:.3f})"
            ),
            "spearman_rho_pooled": rho,
            "bootstrap_ci_95": [ci_lower, ci_upper],
            "n_brands_pooled": len(all_paired),
            "cases_per_cell": cases_per_cell,
        }

    if cells_with_cases == n_cells:
        return {"verdict": "DISSOCIATION_GENERALIZED",
                "narrative": "≥1 case in every cell; v1.4 multi-component claim strengthened",
                "cases_per_cell": cases_per_cell, "total_cases": total_cases}

    return {"verdict": "DISSOCIATION_PARTIAL",
            "narrative": f"Cases present but cell-clustered ({cells_with_cases}/{n_cells} cells)",
            "cases_per_cell": cases_per_cell, "total_cases": total_cases}


# ============================================================
# Emitters
# ============================================================

def emit_verdict_json(verdicts: dict, out_path: Path) -> None:
    payload = {
        "phase": PHASE,
        "pre_reg_tag": PRE_REG_TAG,
        "protocol_version": PROTOCOL_VERSION,
        "scored_at_utc": datetime.now(timezone.utc).isoformat(),
        "verdicts": verdicts,
    }
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)


def emit_verdict_md(verdicts: dict, out_path: Path) -> None:
    h_r4 = verdicts["H_Regime4_indie_fragrance"]
    h_il = verdicts["H_IdentityLoad_moderator"]
    h_di = verdicts["H_Recognition_Recall_dissociation_generalization"]

    lines = [
        f"# v0.18 Verdict — Indie Fragrance / IL-Gradient",
        f"",
        f"**Pre-reg tag:** `{PRE_REG_TAG}`",
        f"**Protocol version:** `{PROTOCOL_VERSION}`",
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
    ]
    with out_path.open("w", encoding="utf-8") as f:
        f.write("\n".join(lines))


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

    blocked = [k for k, v in verdicts.items()
               if str(v.get("verdict", "")).startswith("BLOCKED")
               or str(v.get("verdict", "")).startswith("PENDING")]
    if blocked:
        print(f"\n⚠ BLOCKED/PENDING verdicts: {blocked}")
        print("See protocol/thresholds.py for one-time-lift instructions.")


if __name__ == "__main__":
    main()
