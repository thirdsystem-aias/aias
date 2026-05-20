"""
acquire_phase_b_v18.py — v0.18 Phase B Acquisition Driver

Three-frame query battery × six-slot reference panel = 18 queries total.
For each response, scan for all registry brand mentions and record:
  - presence/absence per (brand, frame, model)
  - in-response rank per brand per (frame, model)

Pre-reg lock:     v0.18-prereg-r1 @ commit 183386c
Branch:           v0.18-il-gradient
Predecessor:      scripts/acquire_phase_b_v17.py (Premium Kitchenware)

Output conforms to the schema contract documented in score_v18.py header
(under "Phase B output schema contract"). Do not deviate from that shape
without updating both this file and score_v18.py in the same commit.
"""

import json
from pathlib import Path
from datetime import datetime, timezone


# ============================================================
# Configuration — LOCKED per v0.18-prereg-r1 §1.6 / §1.7
# ============================================================

PHASE = "v0.18"
PRE_REG_TAG = "v0.18-prereg-r1"
LOCK_COMMIT = "183386c"

# Phase B query frames — verbatim from pre-reg §1.7
# Frame keys MUST match the FRAMES tuple in score_v18.py:
#   ("q1_niche", "q2_independent", "q3_perfumistas")
FRAMES = {
    "q1_niche": (
        "What are the best niche fragrances? "
        "List several with descriptions."
    ),
    "q2_independent": (
        "Recommend high-quality independent fragrance brands. "
        "Name several brands."
    ),
    "q3_perfumistas": (
        "What fragrances do industry insiders and perfumistas recommend? "
        "List several."
    ),
}

# Reference panel — locked six-slot per pre-reg §1.6
REFERENCE_PANEL = [
    "claude-opus-4-5",
    "claude-sonnet-4-5",
    "gpt-4o",
    "gpt-4o-mini",
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
]

# Registry — same brand set as acquire_phase_a_v18.py
# Used as the canonical-name pool for mention detection
REGISTRY = {
    "cell_a_designer_niche": [
        "Maison Francis Kurkdjian",
        "Le Labo",
        "Diptyque",
        "Frederic Malle",
        "Byredo",
        "Comme des Garçons Parfums",
        "Memo Paris",
        "Etat Libre d'Orange",
    ],
    "cell_b_indie_artisan": [
        "D.S. & Durga",
        "Boy Smells",
        "Heretic Parfum",
        "Ellis Brooklyn",
        "Vyrao",
        "Henry Rose",
        "Phlur",
        "Snif",
    ],
    "cell_c_mass_prestige": [
        "Chanel",
        "Dior",
        "YSL",
        "Tom Ford",
        "Givenchy",
        "Versace",
        "Marc Jacobs",
        "Calvin Klein",
    ],
}

# Alias map for mention detection — extend from v17 alias map
# at wire-up time. Below is a minimal seed; v17 has the full
# canonicalization rules including case folding, accent stripping,
# and possessive handling.
BRAND_ALIASES_SEED = {
    "Maison Francis Kurkdjian": ["MFK", "Francis Kurkdjian"],
    "Frederic Malle": ["Frédéric Malle", "Editions de Parfums Frédéric Malle"],
    "Comme des Garçons Parfums": ["CdG Parfums", "Comme des Garçons", "CDG Parfums"],
    "Etat Libre d'Orange": ["État Libre d'Orange", "ELO"],
    "D.S. & Durga": ["DS & Durga", "D.S. and Durga"],
    "Heretic Parfum": ["Heretic"],
    "YSL": ["Yves Saint Laurent", "Saint Laurent"],
    "Dior": ["Christian Dior"],
    "Calvin Klein": ["CK"],
    # Wire-up: import the full v17 alias map + extend for v0.18 new brands
}


# ============================================================
# Probe + parse layer — WIRE TO v17 IMPLEMENTATION
# ============================================================

def probe_frame(frame_query: str, model: str) -> dict:
    """
    Send a frame query to a model; return parsed response payload.

    Returns:
        {
            "model": str,
            "frame_query": str,
            "raw_response": str,
            "response_received_at_utc": str,
            "latency_ms": int,
            "tokens_in": int,
            "tokens_out": int,
        }

    [WIRE TO v17] Lift from scripts/acquire_phase_b_v17.py probe_frame().
    Preserves provider auth, retry/backoff logic, and rate-limit handling
    across the 3-provider panel (Anthropic / OpenAI / Google).
    """
    raise NotImplementedError(
        "Wire to acquire_phase_b_v17.py probe_frame() — "
        "preserves provider auth, retry logic, and response normalization."
    )


def parse_brand_mentions(
    response_text: str,
    registry_canonical: list[str],
    aliases: dict[str, list[str]],
) -> list[dict]:
    """
    Scan a response for brand mentions across the full registry.

    Returns a list of mention records:
        [
            {
                "canonical": "Maison Francis Kurkdjian",
                "matched_surface": "MFK",
                "rank_in_response": 3,        # 1-indexed list position; None if prose-only
                "first_char_offset": 142,     # for de-duplication and rank tie-breaking
            }, ...
        ]

    Mention detection rules (canonical from v17):
      - Case-insensitive match
      - Accent-insensitive match (é → e, ç → c, etc.)
      - Possessive-stripping ("MFK's" → "MFK")
      - First-occurrence-wins for de-duplication
      - Rank derived from enumerated list position when present;
        prose-only mentions get rank None

    [WIRE TO v17] Lift from scripts/acquire_phase_b_v17.py
    parse_brand_mentions(). Detection rules are protocol-canonical and
    must not diverge across phases.
    """
    raise NotImplementedError(
        "Wire to acquire_phase_b_v17.py parse_brand_mentions() — "
        "detection rules are protocol-canonical, do not redefine."
    )


# ============================================================
# Acquisition orchestration
# ============================================================

def all_canonical_brands() -> list[str]:
    """Flatten the registry to a single canonical-name list."""
    return [brand for brands in REGISTRY.values() for brand in brands]


def cell_for_brand(canonical: str) -> str:
    """Reverse-lookup the cell a canonical brand belongs to."""
    for cell, brands in REGISTRY.items():
        if canonical in brands:
            return cell
    raise ValueError(f"Brand not in registry: {canonical}")


def run_phase_b() -> dict:
    """
    Execute the 18 queries (3 frames × 6 models) and aggregate per-brand
    mention records into the schema score_v18.py expects.
    """
    canonical_brands = all_canonical_brands()

    # Step 1: send all 18 queries, collect responses + per-response mentions
    per_query_records = {}  # (frame_key, model) → response + mentions
    for frame_key, frame_query in FRAMES.items():
        for model in REFERENCE_PANEL:
            print(f"[{PHASE}] Probing {frame_key} @ {model}")
            response = probe_frame(frame_query, model)
            mentions = parse_brand_mentions(
                response["raw_response"],
                canonical_brands,
                BRAND_ALIASES_SEED,
            )
            per_query_records[(frame_key, model)] = {
                "response": response,
                "mentions": mentions,
            }

    # Step 2: invert to per-brand records per the schema contract
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
                rank_per_frame[frame_key][model] = (
                    hit["rank_in_response"] if hit else None
                )
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
        "acquired_at_utc": datetime.now(timezone.utc).isoformat(),
        "frames": list(FRAMES.keys()),
        "reference_panel": REFERENCE_PANEL,
        "cells": cells_output,
        # Raw query-level records preserved for transparency / OSF deposit
        "_raw_query_records": {
            f"{fk}__{model}": v
            for (fk, model), v in per_query_records.items()
        },
    }


def main():
    out_dir = Path(f"data/phase_b/{PHASE}")
    out_dir.mkdir(parents=True, exist_ok=True)

    results = run_phase_b()

    out_path = out_dir / "phase_b_results.json"
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\nPhase B results written: {out_path}")

    # Surface attrition diagnostic — brands with 0 mentions across all 18 obs
    zero_mention_brands = []
    for cell_name, cell in results["cells"].items():
        for rec in cell["per_brand"]:
            if rec["mention_count"] == 0:
                zero_mention_brands.append((cell_name, rec["brand"]))

    if zero_mention_brands:
        print(f"\nZero-mention brands ({len(zero_mention_brands)}):")
        for cell, brand in zero_mention_brands:
            print(f"  - {cell}: {brand}")
        print("\nThese feed §3 attrition diagnostics in score_v18.py")
    else:
        print("\nAll registry brands received ≥1 mention across the 18-observation panel.")

    print("\nReady to run: python scripts/score_v18.py")


if __name__ == "__main__":
    main()
