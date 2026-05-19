#!/usr/bin/env python3
"""
classify_phase_a_auto_v1_4.py — Automated C_P anchoring classifier (provisional v1.4 §6.4.2)

Substitutes the v1.3 §6.4.2 operator-judgement Phase A classification step with
a locked LLM classifier. Reads unfilled rows from a Phase A classification ledger,
sends each row's `first_100_tokens` to Claude Opus 4.7 at temperature 0 with a
locked classification prompt, writes back `anchored` (0/1) and `anchoring_note`
(the model's one-sentence rationale).

DEVIATION FROM v1.3 § 6.4.2: v1.3 as published specifies operator-judgement only.
This script implements the provisional v1.4 §6.4.2 revision (LLM-classifier-based
C_P). See osf/v17/DEVIATIONS.md Entry 4 for the full methodological record.

Usage:
    # v0.17 default ledger + substrate:
    python scripts/classify_phase_a_auto_v1_4.py

    # Other phases (substrate-parameterised):
    python scripts/classify_phase_a_auto_v1_4.py \\
        --ledger osf/v18/classification_ledger.csv \\
        --substrate "indie-fragrance substrate"

    # Dry-run (lists what would be classified, no API calls):
    python scripts/classify_phase_a_auto_v1_4.py --dry-run

Idempotency:
    Rows with `anchored` already set to "0" or "1" are skipped. To re-classify
    a row, blank its `anchored` cell and re-run. This makes recovery from
    partial-failure mid-run safe and predictable.

Pre-requisites:
    - ANTHROPIC_API_KEY in environment
    - anthropic Python package (pip install --upgrade anthropic)
"""

import argparse
import csv
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path.home() / "aias"
DEFAULT_LEDGER = ROOT / "osf" / "v17" / "classification_ledger.csv"
DEFAULT_SUBSTRATE = "premium-cookware substrate"

# ---------------------------------------------------------------------------
# Locked classifier configuration per provisional v1.4 §6.4.2
# ---------------------------------------------------------------------------
# These three constants define the C_P classification function. Any change to
# any of them constitutes a DEVIATIONS entry under v1.4 protocol discipline.
# ---------------------------------------------------------------------------

CLASSIFIER_MODEL = "claude-opus-4-7"
CLASSIFIER_TEMPERATURE = 0
CLASSIFIER_MAX_TOKENS = 200

CLASSIFIER_PROMPT_TEMPLATE = """You are scoring an entry in an AIAS Phase A anchoring ledger per Protocol v1.4 § 6.4.2.

Below is the first 100 whitespace-tokenized words of an LLM's response to the query "Who or what is {brand}?".

Task: classify whether the PRIMARY REFERENT in this text identifies the brand as a product, line, or attribute within the {substrate_prompt}.

Criterion:
- The PRIMARY REFERENT is the first definitional identity stated in the text — the first thing the text says the brand IS.
- Output 1 if the primary referent places the brand within the substrate (e.g., "X is a cookware manufacturer", "X is a French enameled cast iron brand", "X is a saucepan line by Y").
- Output 0 if the primary referent places the brand elsewhere (a different industry, an etymology, an unrelated namesake, an adjective, a person, a fictional character, etc.).
- Substrate-relevant content appearing LATER in the 100 tokens does not override a non-substrate primary referent. The test is about what the text leads with, not what it eventually mentions.

Text to classify:
\"\"\"
{first_100_tokens}
\"\"\"

Output exactly two lines, no preamble:
ANCHORED: <0 or 1>
RATIONALE: <one short sentence, max 25 words>
"""


def classify_one(client, brand: str, first_100_tokens: str, substrate_prompt: str) -> tuple:
    """Run one classification. Returns (anchored: str, rationale: str)."""
    prompt = CLASSIFIER_PROMPT_TEMPLATE.format(
        brand=brand,
        substrate_prompt=substrate_prompt,
        first_100_tokens=first_100_tokens,
    )
    resp = client.messages.create(
        model=CLASSIFIER_MODEL,
        max_tokens=CLASSIFIER_MAX_TOKENS,
        temperature=CLASSIFIER_TEMPERATURE,
        messages=[{"role": "user", "content": prompt}],
    )
    text = resp.content[0].text

    anchored = None
    rationale = ""
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("ANCHORED:"):
            val = line.split(":", 1)[1].strip()
            if val in ("0", "1"):
                anchored = val
        elif line.startswith("RATIONALE:"):
            rationale = line.split(":", 1)[1].strip()

    if anchored is None:
        raise ValueError(
            f"Could not parse ANCHORED line from classifier output:\n{text!r}"
        )
    return anchored, rationale


def main():
    parser = argparse.ArgumentParser(
        description="Automated Phase A C_P anchoring classifier (provisional v1.4 §6.4.2)",
    )
    parser.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER,
                        help=f"Phase A ledger CSV path (default: {DEFAULT_LEDGER.relative_to(ROOT)})")
    parser.add_argument("--substrate", default=DEFAULT_SUBSTRATE,
                        help=f"Substrate descriptor used in classifier prompt (default: '{DEFAULT_SUBSTRATE}')")
    parser.add_argument("--dry-run", action="store_true",
                        help="List what would be classified; no API calls")
    parser.add_argument("--force", action="store_true",
                        help="Re-classify rows even if already filled (overwrites existing anchored values)")
    args = parser.parse_args()

    if not args.ledger.exists():
        sys.exit(f"ERROR: ledger not found at {args.ledger}")

    rows = list(csv.DictReader(args.ledger.open(encoding="utf-8")))
    if not rows:
        sys.exit(f"ERROR: ledger empty at {args.ledger}")

    needed_cols = {"brand", "slot", "model_id", "query", "first_100_tokens", "anchored", "anchoring_note"}
    missing = needed_cols - set(rows[0].keys())
    if missing:
        sys.exit(f"ERROR: ledger missing columns: {missing}")

    # Identify rows to classify
    to_classify = []
    for i, row in enumerate(rows):
        if args.force or row["anchored"].strip() not in ("0", "1"):
            to_classify.append(i)

    n_total = len(rows)
    n_to_do = len(to_classify)
    print(f"Phase A auto-classifier (provisional v1.4 §6.4.2)")
    print(f"  Classifier: {CLASSIFIER_MODEL}, temperature={CLASSIFIER_TEMPERATURE}")
    print(f"  Ledger:     {args.ledger}")
    print(f"  Substrate:  {args.substrate}")
    print(f"  Rows total: {n_total}")
    print(f"  To classify: {n_to_do} ({'all (--force)' if args.force else 'unfilled only'})")
    print(f"  Mode:       {'DRY-RUN' if args.dry_run else 'LIVE (will consume API quota)'}")

    if n_to_do == 0:
        print("\nAll rows already filled. Use --force to re-classify.")
        return

    if not args.dry_run:
        if not os.environ.get("ANTHROPIC_API_KEY"):
            sys.exit("ERROR: ANTHROPIC_API_KEY not set. Source your env file and retry.")
        from anthropic import Anthropic
        client = Anthropic()

    # Classify
    print()
    for idx in to_classify:
        row = rows[idx]
        label = f"  [{row['brand']:14s} slot {row['slot']:>2}]"
        if args.dry_run:
            print(f"{label}  DRY-RUN (would classify)")
            continue
        try:
            anchored, rationale = classify_one(
                client,
                brand=row["brand"],
                first_100_tokens=row["first_100_tokens"],
                substrate_prompt=args.substrate,
            )
            row["anchored"] = anchored
            tag = f"[auto-classified by {CLASSIFIER_MODEL} @ T={CLASSIFIER_TEMPERATURE}]"
            row["anchoring_note"] = f"{tag} {rationale}"
            print(f"{label}  anchored={anchored}  — {rationale}")
        except Exception as exc:
            print(f"{label}  FAIL: {type(exc).__name__}: {exc}")
            # Don't write partial state; abort
            sys.exit("\nAborted on classifier failure. No changes written to ledger.")

    # Write back
    if not args.dry_run:
        fieldnames = list(rows[0].keys())
        with args.ledger.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fieldnames)
            w.writeheader()
            w.writerows(rows)
        print(f"\nClassified {n_to_do} rows. Ledger saved: {args.ledger}")
        print(f"Next: python scripts/classify_phase_a_v17.py  (auto-detects filled ledger, prints C_P tally)")
    else:
        print(f"\nDry-run complete. {n_to_do} rows would be classified.")


if __name__ == "__main__":
    main()
