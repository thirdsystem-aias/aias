#!/usr/bin/env python3
"""
classify_phase_a_v17.py — v0.17 Phase A C_P scoring per v1.3 §6.4.2

Phase-versioned ledger-management + C_P tally script for v0.17 premium kitchenware.
Loads canonical disambiguation responses from osf/v17/data/phase_a/, truncates each
response to first 100 tokens per §6.4.2, manages the classification ledger, and
tallies per-brand C_P counts.

Behaviour auto-detects from ledger state and BRANDS list:
  - Ledger absent           → generate fresh ledger (all rows empty `anchored`)
  - Ledger present, missing
    brand-slot pairs        → EXTEND ledger; preserve existing fills; add new rows
  - Ledger present, all
    rows present but some
    unfilled                → instruct to fill (manually or via auto-classifier)
  - Ledger present, all
    rows present and filled → tally and print C_P verdict per brand

Cascade workflow: when a primary pivot returns C_P FAILED, append the cell's
first alternate slug to BRANDS below, run this script (extends ledger with the
alternate's 6 rows), then run scripts/classify_phase_a_auto_v1_4.py (fills only
the new rows via idempotent skip-existing), then re-run this script to re-tally.

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

# v0.17 panel per pre-reg §3.2 (commits 3ebe426 / v0.17-prereg-r1).
# Starts with the three primary pivots. As cascade fires (any C_P FAILED),
# append the failing cell's next alternate slug to this list. Alternates per
# cell, in ordinal order:
#   European: staub → mauviel → demeyere → fissler → de-buyer
#   American: lodge → made-in → field-company → smithey → hestan
#   Japanese: iwachu → sori-yanagi → noda-horo
BRANDS = ["le-creuset", "all-clad", "vermicular", "iwachu"]

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
# Ledger read / generate / extend
# ---------------------------------------------------------------------------

LEDGER_COLUMNS = ["brand", "slot", "model_id", "query", "first_100_tokens",
                  "anchored", "anchoring_note"]


def read_existing_ledger() -> list:
    """Return list of existing ledger rows, or [] if ledger does not exist."""
    if not LEDGER_PATH.exists():
        return []
    with LEDGER_PATH.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def existing_key_set(rows: list) -> set:
    """Set of (brand, slot:int) pairs present in ledger rows."""
    return {(r["brand"], int(r["slot"])) for r in rows}


def build_new_rows_for_brand(brand: str, existing_keys: set) -> list:
    """Build rows for any (brand, slot) pairs not in existing_keys."""
    new = []
    for r in load_phase_a_responses(brand):
        key = (r["brand"], r["slot"])
        if key in existing_keys:
            continue
        new.append({
            "brand": r["brand"],
            "slot": str(r["slot"]),
            "model_id": r["model_id"],
            "query": r["query"],
            "first_100_tokens": first_n_tokens(r["response"], TOKEN_LIMIT),
            "anchored": "",
            "anchoring_note": "",
        })
    return new


def write_ledger(rows: list) -> None:
    """Write rows to the ledger CSV, preserving the canonical column order."""
    LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LEDGER_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=LEDGER_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def generate_or_extend_ledger(existing_rows: list, new_rows_by_brand: dict) -> None:
    """
    Write the ledger with existing rows preserved (with their fills intact) plus
    any new rows appended (with empty `anchored` / `anchoring_note`).
    """
    new_rows = [r for brand_rows in new_rows_by_brand.values() for r in brand_rows]
    all_rows = existing_rows + new_rows
    if not all_rows:
        sys.exit("ERROR: no responses loaded. Check PHASE_A_DIR path and slot files.")

    write_ledger(all_rows)

    is_fresh = not existing_rows
    print(f"\nLedger {'written' if is_fresh else 'extended'}: {LEDGER_PATH}")
    if is_fresh:
        print(f"  Rows: {len(all_rows)} (expected: {len(BRANDS) * TARGET_SLOTS})")
    else:
        print(f"  Existing rows preserved: {len(existing_rows)}")
        for brand, brand_rows in new_rows_by_brand.items():
            if brand_rows:
                print(f"  + {brand}: {len(brand_rows)} new rows")
        print(f"  Total rows: {len(all_rows)}")

    print(f"\nNext steps:")
    print(f"  1. Auto-classify unfilled rows:")
    print(f"       python scripts/classify_phase_a_auto_v1_4.py")
    print(f"     (idempotent — skips already-classified rows; only fills new ones)")
    print(f"  2. Or fill manually: for each new row, read `first_100_tokens` and judge")
    print(f"     - Does the primary referent name a product, line, or attribute")
    print(f"       within the {SUBSTRATE_PROMPT}?")
    print(f"     - Set `anchored` = 1 if yes, 0 if not")
    print(f"  3. Re-run this script to tally")


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
        if c["total"] == 0:
            print(f"  {brand:14s} (no rows in ledger)")
            continue
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
    existing_rows = read_existing_ledger()
    existing_keys = existing_key_set(existing_rows)

    # Determine which brands need new rows added (cascade extension)
    new_rows_by_brand = {}
    any_new = False
    for brand in BRANDS:
        new = build_new_rows_for_brand(brand, existing_keys)
        new_rows_by_brand[brand] = new
        if new:
            any_new = True

    if any_new or not existing_rows:
        # Generate or extend
        generate_or_extend_ledger(existing_rows, new_rows_by_brand)
        return

    # All expected (brand, slot) pairs present in ledger — check fill state
    unfilled = [r for r in existing_rows if r["anchored"].strip() not in ("0", "1")]
    if unfilled:
        print(f"\nLedger present at {LEDGER_PATH} with {len(unfilled)} unfilled rows.")
        print(f"Fill `anchored` column via auto-classifier:")
        print(f"  python scripts/classify_phase_a_auto_v1_4.py")
        print(f"Or fill manually (1=substrate-anchored, 0=not), then re-run.")
        return

    # All filled — tally
    tally(existing_rows)


if __name__ == "__main__":
    main()
