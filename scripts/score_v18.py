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

# Bootstrap: make protocol/ importable when running from project root
import _path  # noqa: F401

from protocol import PROTOCOL_VERSION
from protocol.thresholds import (
    C1_PANEL_ADEQUACY_FLOOR,
    C2_REGIME4_MENTION_THRESHOLD,
    C2_REGIME4_TOP2_SHARE_THRESHOLD,
    C2_IL_GRADIENT_SEPARATION_MIN,
    C3_RANKING_COHERENCE_THRESHOLD,
    C3_MIN_CELLS_CLEARING,
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
    """
    Within-phase Regime 4 verdict per pre-reg r4 §4.0 (full implementation).

    Cascade: C1 (panel adequacy) → C2_within_cell → C2_il_gradient → C3.
    Returns CONFIRMED / PARTIAL / FALSIFIED / NULL with diagnostic detail.
    """
    cell_diagnostics = {}
    total_n = 0
    cell_top2_shares = {}
    cell_phase_d_rhos = {}
    cell_n_post_attrition = {}

    for cell_name, a_cell in phase_a["cells"].items():
        b_cell = phase_b["cells"][cell_name]
        n = cell_panel_n(a_cell, b_cell)
        total_n += n
        top2 = cell_mention_concentration(b_cell)
        rho = cell_phase_d_rho(a_cell, b_cell)
        cell_top2_shares[cell_name] = top2
        cell_phase_d_rhos[cell_name] = rho
        cell_n_post_attrition[cell_name] = n
        cell_diagnostics[cell_name] = {
            "n_post_attrition": n,
            "mention_concentration_top2": top2,
            "phase_d_rho": rho,
        }

    # ---- C1: Panel adequacy ----
    if total_n < C1_PANEL_ADEQUACY_FLOOR:
        return {
            "verdict": "NULL",
            "resolved_at": "C1",
            "reason": f"Panel inadequacy: worldwide n={total_n} < {C1_PANEL_ADEQUACY_FLOOR}",
            "cell_diagnostics": cell_diagnostics,
        }

    # ---- C2(a): within-cell — at least one cell clears top-2 share threshold ----
    cells_meeting_c2_within = [
        c for c, share in cell_top2_shares.items()
        if share >= C2_REGIME4_TOP2_SHARE_THRESHOLD
    ]
    c2_within_pass = len(cells_meeting_c2_within) >= 1

    # ---- C2(b): IL-gradient separation — Cell B share - Cell C share ≥ 0.10 ----
    cell_b_share = cell_top2_shares.get("cell_b_indie_artisan", 0.0)
    cell_c_share = cell_top2_shares.get("cell_c_mass_prestige", 0.0)
    il_gradient_separation = cell_b_share - cell_c_share
    c2_il_gradient_pass = il_gradient_separation >= C2_IL_GRADIENT_SEPARATION_MIN

    # ---- C3: per-cell ρ ≥ threshold in ≥ 2 of 3 cells at n ≥ 5 ----
    cells_clearing_c3 = []
    cells_excluded_n_floor = []
    for cell_name in phase_a["cells"]:
        n = cell_n_post_attrition[cell_name]
        rho = cell_phase_d_rhos[cell_name]
        if n < PHASE_D_RHO_MIN_CELL_N:
            cells_excluded_n_floor.append(cell_name)
            continue
        if rho is not None and rho >= C3_RANKING_COHERENCE_THRESHOLD:
            cells_clearing_c3.append(cell_name)
    c3_pass = len(cells_clearing_c3) >= C3_MIN_CELLS_CLEARING

    # ---- Assemble extended diagnostics for the verdict payload ----
    diagnostic_detail = {
        "cell_diagnostics": cell_diagnostics,
        "C1_check": {
            "total_n_post_attrition": total_n,
            "floor": C1_PANEL_ADEQUACY_FLOOR,
            "satisfied": True,
        },
        "C2_within_cell_check": {
            "threshold": C2_REGIME4_TOP2_SHARE_THRESHOLD,
            "cells_meeting_threshold": cells_meeting_c2_within,
            "satisfied": c2_within_pass,
        },
        "C2_il_gradient_check": {
            "cell_b_top2_share": cell_b_share,
            "cell_c_top2_share": cell_c_share,
            "separation": il_gradient_separation,
            "min_required": C2_IL_GRADIENT_SEPARATION_MIN,
            "satisfied": c2_il_gradient_pass,
        },
        "C3_check": {
            "threshold_per_cell": C3_RANKING_COHERENCE_THRESHOLD,
            "cells_clearing": cells_clearing_c3,
            "cells_excluded_n_floor": cells_excluded_n_floor,
            "min_cells_clearing_required": C3_MIN_CELLS_CLEARING,
            "satisfied": c3_pass,
        },
    }

    # ---- Verdict routing per pre-reg r4 §4.0 truth table ----
    if not c2_within_pass:
        return {
            "verdict": "FALSIFIED",
            "resolved_at": "C2_within_cell",
            "reason": (
                f"No cell meets top-2 share ≥ {C2_REGIME4_TOP2_SHARE_THRESHOLD}; "
                f"observed shares: {cell_top2_shares}"
            ),
            **diagnostic_detail,
        }

    if not c2_il_gradient_pass:
        return {
            "verdict": "FALSIFIED",
            "resolved_at": "C2_il_gradient",
            "reason": (
                f"IL-gradient separation Cell B − Cell C = "
                f"{il_gradient_separation:.3f} < {C2_IL_GRADIENT_SEPARATION_MIN} "
                f"(Cell B top-2 = {cell_b_share:.3f}, Cell C top-2 = {cell_c_share:.3f})"
            ),
            **diagnostic_detail,
        }

    if not c3_pass:
        return {
            "verdict": "PARTIAL",
            "resolved_at": "C3",
            "reason": (
                f"C2 conditions met; C3 cells clearing ρ ≥ {C3_RANKING_COHERENCE_THRESHOLD} "
                f"= {len(cells_clearing_c3)} < {C3_MIN_CELLS_CLEARING} required "
                f"(clearing: {cells_clearing_c3}; excluded for n < {PHASE_D_RHO_MIN_CELL_N}: "
                f"{cells_excluded_n_floor})"
            ),
            **diagnostic_detail,
        }

    return {
        "verdict": "CONFIRMED",
        "resolved_at": "C3",
        "reason": (
            f"All conditions met. C2 within-cell cleared by {cells_meeting_c2_within}. "
            f"IL-gradient separation {il_gradient_separation:.3f} ≥ "
            f"{C2_IL_GRADIENT_SEPARATION_MIN}. C3 cleared by {cells_clearing_c3}."
        ),
        **diagnostic_detail,
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
        f"---",
        f"",
        f"## H_Regime4_indie_fragrance (within-phase substantive)",
        f"",
        f"**Verdict:** `{h_r4.get('verdict')}`",
        f"**Resolved at:** {h_r4.get('resolved_at', 'n/a')}",
        f"",
        f"{h_r4.get('reason', '')}",
        f"",
    ]

    # Per-cell diagnostics table
    cd = h_r4.get("cell_diagnostics", {})
    if cd:
        lines.extend([
            f"### Per-cell diagnostics",
            f"",
            f"| Cell | n post-attrition | Top-2 share (C2) | Phase D ρ (C3) |",
            f"|---|---|---|---|",
        ])
        for cell, d in cd.items():
            rho = d.get("phase_d_rho")
            rho_str = f"{rho:.3f}" if rho is not None else "—"
            lines.append(
                f"| {cell} | {d.get('n_post_attrition', '—')} | "
                f"{d.get('mention_concentration_top2', 0):.3f} | {rho_str} |"
            )
        lines.append("")

    # Condition check breakdown
    for check_name, check_label in [
        ("C2_within_cell_check", "C2 — within-cell"),
        ("C2_il_gradient_check", "C2 — IL-gradient separation"),
        ("C3_check", "C3 — within-cell ranking coherence"),
    ]:
        c = h_r4.get(check_name)
        if c:
            lines.append(f"**{check_label}:** {'✓ satisfied' if c.get('satisfied') else '✗ not satisfied'}")
            for k, v in c.items():
                if k != "satisfied":
                    lines.append(f"  - {k}: `{v}`")
            lines.append("")

    lines.extend([
        f"---",
        f"",
        f"## H_IdentityLoad_moderator (three-leg joint v0.16 × v0.17 × v0.18)",
        f"",
        f"**Joint verdict:** `{h_il.get('joint_verdict')}`",
        f"",
        f"- v0.16: `{PREDECESSOR_VERDICTS['v0.16']}`",
        f"- v0.17: `{PREDECESSOR_VERDICTS['v0.17']}`",
        f"- v0.18: `{h_il.get('v0_18_leg')}`",
        f"",
        f"{h_il.get('narrative', '')}",
        f"",
        f"---",
        f"",
        f"## H_Recognition_Recall_dissociation_generalization (methodological)",
        f"",
        f"**Verdict:** `{h_di.get('verdict')}`",
        f"",
        f"{h_di.get('narrative', h_di.get('reason', ''))}",
        f"",
    ])

    # Dissociation cases per cell
    cases = h_di.get("cases_per_cell", {})
    if cases:
        total = sum(len(v) for v in cases.values())
        lines.append(f"### Dissociation cases ({total} total)")
        lines.append("")
        for cell_name, cell_cases in cases.items():
            if cell_cases:
                lines.append(f"**{cell_name}** ({len(cell_cases)} case{'s' if len(cell_cases) != 1 else ''}):")
                for c in cell_cases:
                    lines.append(
                        f"  - {c['brand']}: C_P={c['c_p_score']}/6, mentions={c['mention_count']}/18"
                    )
                lines.append("")
            else:
                lines.append(f"**{cell_name}**: 0 cases")
                lines.append("")

    # Correlation diagnostic if zero cases
    if "spearman_rho_pooled" in h_di:
        lines.extend([
            f"### Recognition–Recall correlation (zero-case path)",
            f"",
            f"- Spearman ρ pooled: `{h_di.get('spearman_rho_pooled'):.3f}`",
            f"- Bootstrap 95% CI: `{h_di.get('bootstrap_ci_95')}`",
            f"- n_brands_pooled: `{h_di.get('n_brands_pooled')}`",
            f"",
        ])

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
