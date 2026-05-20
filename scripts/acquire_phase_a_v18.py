"""
acquire_phase_a_v18.py — v0.18 Phase A C_P Acquisition Driver

Imports the canonical probe implementation from protocol/. This script
is pure phase-specific configuration plus orchestration; the probe
logic lives in protocol/probe.py.

Pre-reg lock:     v0.18-prereg-r1 @ commit 183386c
Branch:           v0.18-il-gradient
Protocol version: v1.4 (pinned via protocol/__init__.py)
"""

import json
from pathlib import Path
from datetime import datetime, timezone

# Canonical implementations from the shared protocol layer
from protocol import PROTOCOL_VERSION
from protocol.probe import probe_brand
from protocol.thresholds import PIVOT_C_P_THRESHOLD, DISSOCIATION_C_P_FLOOR


# ============================================================
# Phase-specific configuration — LOCKED per v0.18-prereg-r1
# ============================================================

PHASE = "v0.18"
PRE_REG_TAG = "v0.18-prereg-r1"
LOCK_COMMIT = "183386c"
SUBSTRATE = "indie_fragrance_il_gradient"
CATEGORY = "niche fragrance"

REFERENCE_PANEL = [
    "claude-opus-4-5", "claude-sonnet-4-5",
    "gpt-4o", "gpt-4o-mini",
    "gemini-2.5-flash", "gemini-2.5-flash-lite",
]

REGISTRY = {
    "cell_a_designer_niche": [
        "Maison Francis Kurkdjian", "Le Labo", "Diptyque", "Frederic Malle",
        "Byredo", "Comme des Garçons Parfums", "Memo Paris", "Etat Libre d'Orange",
    ],
    "cell_b_indie_artisan": [
        "D.S. & Durga", "Boy Smells", "Heretic Parfum", "Ellis Brooklyn",
        "Vyrao", "Henry Rose", "Phlur", "Snif",
    ],
    "cell_c_mass_prestige": [
        "Chanel", "Dior", "YSL", "Tom Ford",
        "Givenchy", "Versace", "Marc Jacobs", "Calvin Klein",
    ],
}


def acquire_brand_phase_a(brand: str) -> dict:
    """Probe a single brand across the 6-slot panel; return C_P score."""
    per_model = {model: probe_brand(brand, model, CATEGORY) for model in REFERENCE_PANEL}
    c_p_score = sum(1 for r in per_model.values() if r["recognized"])
    return {
        "brand": brand,
        "c_p_score": c_p_score,
        "per_model_responses": per_model,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    }


def run_phase_a_with_cascade(cell_name: str, brands_in_order: list[str]) -> dict:
    """
    Execute Phase A for one cell. Pivot = first brand achieving
    C_P == PIVOT_C_P_THRESHOLD (6/6). Continue probing remaining brands
    for the dissociation analysis and descriptive sensitivities.
    """
    pivot = None
    per_brand_results = []
    cascade_log = []

    for brand in brands_in_order:
        result = acquire_brand_phase_a(brand)
        per_brand_results.append(result)
        entry = {"brand": brand, "c_p_score": result["c_p_score"]}
        if pivot is None and result["c_p_score"] == PIVOT_C_P_THRESHOLD:
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
        print(f"[{PHASE}] Phase A: {cell_name} (n={len(brands)})")
        cell_results[cell_name] = run_phase_a_with_cascade(cell_name, brands)

    out_path = out_dir / "phase_a_results.json"
    with out_path.open("w", encoding="utf-8") as f:
        json.dump({
            "phase": PHASE,
            "substrate": SUBSTRATE,
            "pre_reg_tag": PRE_REG_TAG,
            "lock_commit": LOCK_COMMIT,
            "protocol_version": PROTOCOL_VERSION,
            "acquired_at_utc": datetime.now(timezone.utc).isoformat(),
            "category_anchor": CATEGORY,
            "reference_panel": REFERENCE_PANEL,
            "thresholds": {
                "pivot": PIVOT_C_P_THRESHOLD,
                "dissociation_c_p_floor": DISSOCIATION_C_P_FLOOR,
            },
            "cells": cell_results,
        }, f, indent=2, ensure_ascii=False)

    print(f"\nPhase A results: {out_path}")
    exhausted = [n for n, r in cell_results.items() if r["pivot_cascade_exhausted"]]
    if exhausted:
        print("\n⚠ PIVOT CASCADE EXHAUSTED:")
        for cell in exhausted:
            print(f"  - {cell}: open DEVIATIONS entry before alternates")
    else:
        print("\n✓ All cells anchored. Ready: python scripts/acquire_phase_b_v18.py")


if __name__ == "__main__":
    main()
