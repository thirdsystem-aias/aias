"""
acquire_phase_a_v18.py — v0.18 Indie Fragrance / IL-Gradient

Phase A C_P (Category-Probe) acquisition driver. Per AIAS Presence Measurement
Protocol v1.4 (SSRN 6799479) §[Phase A spec]:
  - Probes each registry brand against the 6-slot reference panel
  - Scores recognition (C_P ∈ {0,1,...,6})
  - Applies cascade rule: first brand achieving C_P=6/6 becomes the cell pivot;
    remaining brands probed for dissociation-analysis coverage

Pre-reg lock:     v0.18-prereg-r1
Commit:           [TBD — backfill at lock]
Branch:           v0.18-il-gradient
Predecessor:      scripts/acquire_phase_a_v17.py (Premium Kitchenware)

NOTE: This file is the v0.18 skeleton — registry, cascade, thresholds, and
output schema are locked here per pre-reg r2. The probe_brand() API-call layer
is stubbed and should be wired to the v17 implementation, which already
handles the 3-provider (Anthropic / OpenAI / Google) panel and the v1.4
C_P probe template.
"""

import json
from pathlib import Path
from datetime import datetime, timezone


# ============================================================
# Configuration block — LOCKED per v0.18-prereg-r1 §1
# ============================================================

PHASE = "v0.18"
SUBSTRATE = "indie_fragrance_il_gradient"
CATEGORY = "niche fragrance"  # per Phase B q1 anchor wording, §1.7

# Reference panel — locked six-slot per pre-reg §1.6
# (Provider model substitutions: document in DEVIATIONS, do not edit here)
REFERENCE_PANEL = [
    "claude-opus-4-5",
    "claude-sonnet-4-5",
    "gpt-4o",
    "gpt-4o-mini",
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
]

# Cell registries — per pre-reg §1.3
# Ordering within each cell IS the cascade order per §1.4.
# Do not reorder without a new pre-reg revision.
REGISTRY = {
    "cell_a_designer_niche": [
        "Maison Francis Kurkdjian",
        "Le Labo",                       # borderline: EL 2014
        "Diptyque",
        "Frederic Malle",                # borderline: EL 2014
        "Byredo",                        # borderline: LVMH 2022
        "Comme des Garçons Parfums",     # lower-prominence stress test
        "Memo Paris",                    # lower-prominence stress test
        "Etat Libre d'Orange",           # r2 swap-in (was Nasomatto)
    ],
    "cell_b_indie_artisan": [
        "D.S. & Durga",
        "Boy Smells",
        "Heretic Parfum",
        "Ellis Brooklyn",
        "Vyrao",
        "Henry Rose",
        "Phlur",                         # lower-prominence stress test
        "Snif",                          # r2 swap-in (was Régime des Fleurs)
    ],
    "cell_c_mass_prestige": [
        "Chanel",
        "Dior",
        "YSL",
        "Tom Ford",                      # house-level; Private Blend NOT split
        "Givenchy",
        "Versace",
        "Marc Jacobs",
        "Calvin Klein",
    ],
}

# Alternates — invoked ONLY if a full cell cascade fails Phase A.
# Invocation requires a DEVIATIONS entry; alternates are not automatic.
ALTERNATES = {
    "cell_a_designer_niche": [
        "Atelier Cologne",
        "Acqua di Parma",                # LVMH-owned
        "Nasomatto",                     # r2: moved from registry
        "Editions de Parfums Frédéric Malle",  # same-house caution vs registry #4
        "Maison Margiela Replica",
    ],
    "cell_b_indie_artisan": [
        "Sana Jardin",
        "Floral Street",
        "Imaginary Authors",
        "Juliette Has a Gun",
        "Régime des Fleurs",             # r2: moved from registry
    ],
    "cell_c_mass_prestige": [
        "Hugo Boss",
        "Lancôme",
        "Carolina Herrera",
        "Paco Rabanne",
        "Burberry",
    ],
}

# Borderline classifications — pre-registered per §1.5
# Resolution rule: Phase B retrieval-frame disposition determines final Cell A
# canonical status. No registry change here.
BORDERLINE = {
    "Le Labo": {
        "reason": "EL ownership since 2014",
        "resolution_at": "phase_b_topic_id",
    },
    "Frederic Malle": {
        "reason": "EL ownership since 2014",
        "resolution_at": "phase_b_topic_id",
    },
    "Byredo": {
        "reason": "LVMH ownership since 2022",
        "resolution_at": "phase_b_topic_id",
    },
}

# Decision thresholds — per pre-reg §2
PIVOT_THRESHOLD = 6        # 6/6 required for pivot anchor (per v1.4)
DISSOCIATION_C_P_FLOOR = 5 # C_P ≥ 5/6 for Iwachu-pattern eligibility, per §2.3


# ============================================================
# Probe layer — WIRE TO v17 IMPLEMENTATION
# ============================================================

def probe_brand(brand: str, model: str) -> dict:
    """
    Send the v1.4 C_P probe for `brand` to `model`. Parse yes/no response.

    Returns:
        {
            "model": str,
            "recognized": bool,
            "raw_response": str,
            "probe_template_version": str,   # e.g. "v1.4"
            "latency_ms": int,
        }

    [IMPLEMENTATION NOTE]
    Lift directly from scripts/acquire_phase_a_v17.py probe_brand().
    The C_P probe template is sourced from the v1.4 protocol artifact at
    aias/protocol/v1_4/c_p_probe_template.txt — DO NOT redefine the
    template here; loading from protocol artifact preserves traceability
    across phases.
    """
    raise NotImplementedError(
        "Wire to acquire_phase_a_v17.py probe_brand() — "
        "preserves provider auth, retry logic, and v1.4 probe template loading."
    )


# ============================================================
# Acquisition logic — locked per pre-reg §1.4 cascade rule
# ============================================================

def acquire_brand_phase_a(brand: str) -> dict:
    """Probe a single brand across the full 6-slot panel; return C_P score."""
    per_model = {}
    for model in REFERENCE_PANEL:
        per_model[model] = probe_brand(brand, model)
    c_p_score = sum(1 for r in per_model.values() if r["recognized"])
    return {
        "brand": brand,
        "c_p_score": c_p_score,
        "per_model_responses": per_model,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    }


def run_phase_a_with_cascade(cell_name: str, brands_in_order: list[str]) -> dict:
    """
    Execute Phase A for a cell with cascade pivot-determination.

    Cascade logic (per pre-reg §1.4):
      1. Probe brands in cascade order.
      2. First brand achieving C_P == PIVOT_THRESHOLD (6/6) → cell pivot.
      3. Continue probing remaining brands regardless (needed for §3
         descriptive sensitivities and §2.3 dissociation analysis).
      4. If no brand achieves 6/6 across the full cascade → cell flagged
         for alternates invocation; requires DEVIATIONS entry before proceeding.
    """
    pivot = None
    per_brand_results = []
    cascade_log = []

    for brand in brands_in_order:
        result = acquire_brand_phase_a(brand)
        per_brand_results.append(result)
        entry = {
            "brand": brand,
            "c_p_score": result["c_p_score"],
        }
        if pivot is None and result["c_p_score"] == PIVOT_THRESHOLD:
            pivot = brand
            entry["status"] = "PIVOT_ANCHORED"
        elif pivot is None:
            entry["status"] = "PIVOT_CASCADE_FAIL"
        else:
            entry["status"] = "REGISTRY_PROBE"
        cascade_log.append(entry)

    return {
        "cell": cell_name,
        "pivot": pivot,
        "pivot_cascade_exhausted": pivot is None,
        "per_brand": per_brand_results,
        "cascade_log": cascade_log,
    }


def main():
    out_dir = Path(f"data/phase_a/{PHASE}")
    out_dir.mkdir(parents=True, exist_ok=True)

    cell_results = {}
    for cell_name, brands in REGISTRY.items():
        print(f"[{PHASE}] Phase A acquisition: {cell_name} (n={len(brands)})")
        cell_results[cell_name] = run_phase_a_with_cascade(cell_name, brands)

    out_path = out_dir / "phase_a_results.json"
    with out_path.open("w", encoding="utf-8") as f:
        json.dump({
            "phase": PHASE,
            "substrate": SUBSTRATE,
            "pre_reg_tag": "v0.18-prereg-r1",
            "pre_reg_revision": "r2",
            "acquired_at_utc": datetime.now(timezone.utc).isoformat(),
            "category_anchor": CATEGORY,
            "reference_panel": REFERENCE_PANEL,
            "thresholds": {
                "pivot": PIVOT_THRESHOLD,
                "dissociation_c_p_floor": DISSOCIATION_C_P_FLOOR,
            },
            "borderline_classifications": BORDERLINE,
            "cells": cell_results,
        }, f, indent=2, ensure_ascii=False)

    print(f"\nPhase A results written: {out_path}")

    # Flag cells where pivot cascade exhausted — triggers alternates DEVIATIONS path
    exhausted = [name for name, r in cell_results.items() if r["pivot_cascade_exhausted"]]
    if exhausted:
        print("\n⚠ PIVOT CASCADE EXHAUSTED:")
        for cell in exhausted:
            print(f"  - {cell}: open DEVIATIONS entry before invoking alternates")
        print("\nPhase A NOT locked; do not proceed to Phase B until alternates resolved.")
    else:
        print("\n✓ All cells anchored. Ready to tag v0.18-phase-a-locked.")


if __name__ == "__main__":
    main()
