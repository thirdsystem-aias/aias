"""
acquire_phase_b_v18.py — v0.18 Phase B Acquisition Driver

Three-frame query battery × six-slot reference panel = 18 queries total.
Probe and parse implementations imported from protocol/.

Pre-reg lock:     v0.18-prereg-r1 @ commit 183386c
Branch:           v0.18-il-gradient
Protocol version: v1.4

Output schema documented in score_v18.py header; do not deviate from
that shape without updating both files in the same commit.
"""

import json
from pathlib import Path
from datetime import datetime, timezone

# Bootstrap: make protocol/ importable when running from project root
import _path  # noqa: F401

from protocol import PROTOCOL_VERSION
from protocol.probe import probe_frame
from protocol.parse import parse_brand_mentions


# ============================================================
# Phase-specific configuration — LOCKED per v0.18-prereg-r1 §1.7
# ============================================================

PHASE = "v0.18"
PRE_REG_TAG = "v0.18-prereg-r1"
LOCK_COMMIT = "183386c"

FRAMES = {
    "q1_niche": (
        "What are the best niche fragrances? List several with descriptions."
    ),
    "q2_independent": (
        "Recommend high-quality independent fragrance brands. Name several brands."
    ),
    "q3_perfumistas": (
        "What fragrances do industry insiders and perfumistas recommend? "
        "List several."
    ),
}

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

# Alias seed for mention detection. The canonical alias map (case-folding
# rules, accent stripping, possessive handling) is in protocol/parse.py.
# This dict adds v0.18-panel-specific surface variants.
BRAND_ALIASES = {
    "Maison Francis Kurkdjian": ["MFK", "Francis Kurkdjian"],
    "Frederic Malle": ["Frédéric Malle", "Editions de Parfums Frédéric Malle"],
    "Comme des Garçons Parfums": ["CdG Parfums", "Comme des Garçons", "CDG Parfums"],
    "Etat Libre d'Orange": ["État Libre d'Orange", "ELO"],
    "D.S. & Durga": ["DS & Durga", "D.S. and Durga"],
    "Heretic Parfum": ["Heretic"],
    "YSL": ["Yves Saint Laurent", "Saint Laurent"],
    "Dior": ["Christian Dior"],
    "Calvin Klein": ["CK"],
}


def all_canonical_brands() -> list[str]:
    return [brand for brands in REGISTRY.values() for brand in brands]


def run_phase_b() -> dict:
    canonical_brands = all_canonical_brands()

    # 18 queries: each (frame, model) pair → one response → scanned for all 24 brands
    per_query_records = {}
    for frame_key, frame_query in FRAMES.items():
        for model in REFERENCE_PANEL:
            print(f"[{PHASE}] Probing {frame_key} @ {model}")
            response = probe_frame(frame_query, model)
            mentions = parse_brand_mentions(
                response["raw_response"], canonical_brands, BRAND_ALIASES,
            )
            per_query_records[(frame_key, model)] = {
                "response": response,
                "mentions": mentions,
            }

    # Invert: per-brand records conforming to score_v18.py schema
    cells_output = {}
    for cell_name, cell_brands in REGISTRY.items():
        per_brand = []
        for brand in cell_brands:
            per_frame_per_model = {fk: {} for fk in FRAMES}
            rank_per_frame = {fk: {} for fk in FRAMES}
            mention_count = 0

            for (frame_key, model), record in per_query_records.items():
                hit = next(
                    (m for m in record["mentions"] if m["canonical"] == brand),
                    None,
                )
                present = hit is not None
                per_frame_per_model[frame_key][model] = present
                rank_per_frame[frame_key][model] = hit["rank_in_response"] if hit else None
                if present:
                    mention_count += 1

            per_brand.append({
                "brand": brand,
                "mention_count": mention_count,
                "per_frame_per_model": per_frame_per_model,
                "rank_per_frame": rank_per_frame,
            })

        cells_output[cell_name] = {"per_brand": per_brand}

    return {
        "phase": PHASE,
        "pre_reg_tag": PRE_REG_TAG,
        "lock_commit": LOCK_COMMIT,
        "protocol_version": PROTOCOL_VERSION,
        "acquired_at_utc": datetime.now(timezone.utc).isoformat(),
        "frames": list(FRAMES.keys()),
        "reference_panel": REFERENCE_PANEL,
        "cells": cells_output,
        "_raw_query_records": {
            f"{fk}__{model}": v for (fk, model), v in per_query_records.items()
        },
    }


def main():
    out_dir = Path(f"data/phase_b/{PHASE}")
    out_dir.mkdir(parents=True, exist_ok=True)

    results = run_phase_b()
    out_path = out_dir / "phase_b_results.json"
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\nPhase B results: {out_path}")

    zero_mention = [
        (cell, rec["brand"])
        for cell, c in results["cells"].items()
        for rec in c["per_brand"] if rec["mention_count"] == 0
    ]
    if zero_mention:
        print(f"\nZero-mention brands ({len(zero_mention)}):")
        for cell, brand in zero_mention:
            print(f"  - {cell}: {brand}")
    else:
        print("\nAll registry brands received ≥1 mention.")

    print("\nReady: python scripts/score_v18.py")


if __name__ == "__main__":
    main()
