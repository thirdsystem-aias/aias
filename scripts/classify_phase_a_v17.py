#!/usr/bin/env python3
"""
classify_phase_a_v17.py — v0.17 Phase A C_P scoring per v1.3 §6.4.2

Phase-versioned copy of classify_phase_a_v1_3.py adapted for v0.17 premium
kitchenware. Loads canonical disambiguation responses for the v0.17 primary
pivots (Le Creuset, All-Clad, Vermicular) from osf/v17/data/phase_a/,
truncates each response to first 100 tokens per the §6.4.2 anchoring rule,
generates a classification ledger for operator anchoring decisions, and
tallies per-brand C_P counts once filled.

Single entry point, behaviour auto-detects from ledger state:
  - Ledger absent  → extract responses, generate ledger
  - Ledger present, rows unfilled → instruct to fill
  - Ledger fully filled → tally and print C_P verdict per brand

If a primary pivot returns C_P FAILED, the cascade per v1.3 §6.4.7 fires:
acquire the cell's first alternate via acquire_phase_a_v1_3.py, add its slug
to BRANDS, delete the ledger to regenerate, re-fill, re-tally.

Usage:
    python scripts/classify_phase_a_v17.py
"""

import csv
import json
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths — v0.17 substrate (premium kitchenware)
# ---------------------------------------------------------------------------

ROOT = Path.home() / "aias"
PHASE_A_DIR = ROOT / "osf" / "v17" / "data" / "phase_a"
LEDGER_PATH = ROOT / "osf" / "v17" / "classification_ledger.csv"

# v0.17 primary pivots per pre-reg §3.2 (commits 3ebe426 / v0.17-prereg-r1).
# As cascade fires (any primary C_P FAILED), append the cell's first alternate
# slug here, delete the ledger CSV, and re-run to extend. Alternates per cell:
#   european alternate 1: staub
#   american alternate 1: lodge
#   japanese alternate 1: iwachu
BRANDS = ["le-creuset", "all-clad", "vermicular"]

TARGET_SLOTS = 6           # Reference model set size per Protocol v1.2 §5.2
TOKEN_LIMIT = 100          # Per §6.4.2 anchoring decision rule
PASS_THRESHOLD = 5         # Per §6.4.2 supermajority (5/6)

# Substrate-anchoring criterion text shown to operator at ledger generation.
SUBSTRATE_PROMPT = "premium-cookware substrate"


# ---------------------------------------------------------------------------
# Phase A response loader
# ---------------------------------------------------------------------------

def load_phase_a_responses(brand: str) -> list:
    """
    Load canonical disambiguation responses for a brand from v0.17 archive.

    Expected file layout (written by acquire_phase_a_v1_3.py):
        osf/v17/data/phase_a/<brand>/slot_<N>.json
        each JSON contains {"model_id": str, "query": str, "response": str, ...}
    """
    brand_dir = PHASE_A_DIR / brand
    if not brand_dir.exists():
        sys.exit(
            f"\nERROR: Phase A archive not found at {brand_dir}\n"
            f"  Expected slot files at osf/v17/data/phase_a/{brand}/slot_<N>.json.\n"
            f"  If archive is missing for this brand, run:\n"
            f"    python scripts/acquire_phase_a_v1_3.py --brands \"{brand.replace('-', ' ').title()}\" --live\n"
        )

    responses = []
    for slot_n in range(1, TARGET_SLOTS + 1):
        slot_file = brand_dir / f"slot_{slot_n}.json"
        if not slot_file.exists():
            print(f"WARNING: missing slot file {slot_file}", file=sys.stderr)
            continue
        data = json.loads(slot_file.read_text(encoding="utf-8"))
        responses.append({
            "brand": brand,
            "slot": slot_n,
            "model_id": data.get("model_id", "unknown"),
            "query": data.get("query", ""),
            "response": data.get("response", ""),
        })
    return responses


# ---------------------------------------------------------------------------
# Token truncation per §6.4.2 anchoring rule
# ---------------------------------------------------------------------------

def first_n_tokens(text: str, n: int = TOKEN_LIMIT) -> str:
    """
    Whitespace tokenization per §6.4.2. This is the human-readable first-N-words
    slice used for classification, not LLM-tokenization.
    """
    tokens = text.split()
    return " ".join(tokens[:n])


# ---------------------------------------------------------------------------
# Ledger generation
# ---------------------------------------------------------------------------

def generate_ledger() -> None:
    LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)

    rows = []
    for brand in BRANDS:
        for r in load_phase_a_responses(brand):
            rows.append({
                "brand": r["brand"],
                "slot": r["slot"],
                "model_id": r["model_id"],
                "query": r["query"],
                "first_100_tokens": first_n_tokens(r["response"], TOKEN_LIMIT),
                "anchored": "",         # MANUAL FILL: 1 if substrate-anchored, 0 if not
                "anchoring_note": "",   # MANUAL: optional reason for the classification
            })

    if not rows:
        sys.exit("ERROR: no responses loaded. Check PHASE_A_DIR path and slot files.")

    with LEDGER_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nLedger written: {LEDGER_PATH}")
    print(f"  Rows: {len(rows)} (expected: {len(BRANDS) * TARGET_SLOTS})")
    print(f"\nNext steps:")
    print(f"  1. Open ledger in spreadsheet or editor")
    print(f"  2. For each row, read `first_100_tokens` and judge:")
    print(f"     - Does the primary referent name a product, line, or attribute")
    print(f"       within the {SUBSTRATE_PROMPT}?")
    print(f"  3. Fill `anchored` column: 1 if substrate-anchored, 0 if not")
    print(f"  4. Optionally note reason in `anchoring_note`")
    print(f"  5. Re-run this script to tally")


# ---------------------------------------------------------------------------
# Tally
# ---------------------------------------------------------------------------

def tally(rows: list) -> None:
    counts = {brand: {"anchored": 0, "total": 0} for brand in BRANDS}

    for row in rows:
        brand = row["brand"]
        if brand not in counts:
            counts[brand] = {"anchored": 0, "total": 0}
        counts[brand]["total"] += 1
        if row["anchored"].strip() == "1":
            counts[brand]["anchored"] += 1

    print(f"\nPhase A C_P scoring per v1.3 §6.4.2:")
    print(f"  Threshold: anchoring count >= {PASS_THRESHOLD}/{TARGET_SLOTS} passes; "
          f"<= {PASS_THRESHOLD - 1}/{TARGET_SLOTS} fails\n")

    for brand in counts:
        c = counts[brand]
        if c["anchored"] >= PASS_THRESHOLD:
            verdict = "C_P PASSED"
        else:
            verdict = "C_P FAILED"
        print(f"  {brand:14s} anchoring count: {c['anchored']}/{c['total']}  ->  {verdict}")
    print()


# ---------------------------------------------------------------------------
# Main — auto-detect state
# ---------------------------------------------------------------------------

def main() -> None:
    if not LEDGER_PATH.exists():
        generate_ledger()
        return

    with LEDGER_PATH.open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    unfilled = [r for r in rows if r["anchored"].strip() not in ("0", "1")]
    if unfilled:
        print(f"\nLedger present at {LEDGER_PATH} with {len(unfilled)} unfilled rows.")
        print(f"Fill `anchored` column (1=substrate-anchored, 0=not), then re-run.")
        return

    tally(rows)


if __name__ == "__main__":
    main()
