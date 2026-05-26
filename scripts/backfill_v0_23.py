#!/usr/bin/env python3
"""
AIAS v0.23 — Backfill failed probes
Re-runs only records with status="error" in the raw JSON files,
using corrected model IDs. Merges results in place.

Usage (via Claude Code):
  cd /Users/pablou/aias
  python3 scripts/backfill_v0_23.py --dry-run
  python3 scripts/backfill_v0_23.py
"""

import json
import os
import sys
import time
import argparse
from datetime import datetime, timezone
from pathlib import Path

import anthropic
import openai
from google import genai
from google.genai import types

PIPELINE_ROOT = Path("/Users/pablou/aias")
DATA_DIR = PIPELINE_ROOT / "osf" / "v23" / "data"

# Corrected model IDs (no date suffixes for Anthropic)
MODEL_ID_MAP = {
    "M1": {"model_id": "claude-opus-4-5",       "provider": "anthropic"},
    "M2": {"model_id": "claude-sonnet-4-5",     "provider": "anthropic"},
    "M3": {"model_id": "gpt-4o",                "provider": "openai"},
    "M4": {"model_id": "gpt-4o-mini",           "provider": "openai"},
    "M5": {"model_id": "gemini-2.5-flash",      "provider": "google"},
    "M6": {"model_id": "gemini-2.5-flash-lite", "provider": "google"},
}

PAUSE = {"anthropic": 2.0, "openai": 1.0, "google": 1.0}


def call_anthropic(model_id, prompt):
    client = anthropic.Anthropic()
    msg = client.messages.create(
        model=model_id, max_tokens=2048, temperature=0.0,
        messages=[{"role": "user", "content": prompt}],
    )
    return msg.content[0].text


def call_openai(model_id, prompt):
    client = openai.OpenAI()
    resp = client.chat.completions.create(
        model=model_id, max_tokens=2048, temperature=0.0,
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.choices[0].message.content


def call_google(model_id, prompt):
    client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
    response = client.models.generate_content(
        model=model_id,
        contents=prompt,
        config=types.GenerateContentConfig(temperature=0.0, max_output_tokens=2048),
    )
    return response.text


DISPATCH = {
    "anthropic": call_anthropic,
    "openai":    call_openai,
    "google":    call_google,
}


def retry_record(record):
    """Re-send a single failed probe with corrected model ID."""
    slot = record["model_slot"]
    corrected = MODEL_ID_MAP[slot]
    model_id = corrected["model_id"]
    provider = corrected["provider"]
    prompt = record["prompt"]

    ts_start = datetime.now(timezone.utc).isoformat()
    try:
        response_text = DISPATCH[provider](model_id, prompt)
        status = "ok"
        error_msg = None
    except Exception as e:
        response_text = ""
        status = "error"
        error_msg = str(e)
    ts_end = datetime.now(timezone.utc).isoformat()

    time.sleep(PAUSE[provider])

    # Update record in place
    record["model_id"] = model_id
    record["response"] = response_text
    record["status"] = status
    record["error"] = error_msg
    record["ts_start"] = ts_start
    record["ts_end"] = ts_end
    record["backfill"] = True
    return record


def backfill_file(path, label, dry_run=False):
    """Find error records in a JSON file, retry them, save."""
    if not path.exists():
        print(f"  {label}: file not found at {path}")
        return

    with open(path, "r", encoding="utf-8") as f:
        records = json.load(f)

    errors = [(i, r) for i, r in enumerate(records) if r["status"] == "error"]
    total_errors = len(errors)

    if total_errors == 0:
        print(f"  {label}: no errors — nothing to backfill")
        return

    print(f"  {label}: {total_errors} errors to backfill")

    # Show error breakdown
    by_slot = {}
    for _, r in errors:
        slot = r["model_slot"]
        by_slot[slot] = by_slot.get(slot, 0) + 1
    for slot, count in sorted(by_slot.items()):
        mid = MODEL_ID_MAP[slot]["model_id"]
        print(f"    {slot} ({mid}): {count} probes")

    if dry_run:
        print(f"  DRY RUN — would retry {total_errors} probes")
        return

    success = 0
    still_failed = 0
    for idx, (i, record) in enumerate(errors, 1):
        brand_tag = record.get("brand_name") or record.get("probe_id", "?")
        slot = record["model_slot"]
        print(f"    [{idx}/{total_errors}] {brand_tag} → {slot} {MODEL_ID_MAP[slot]['model_id']}")

        retry_record(record)
        records[i] = record

        if record["status"] == "ok":
            success += 1
        else:
            still_failed += 1
            print(f"      ⚠ Still failing: {record['error']}")

        # Checkpoint every 10
        if idx % 10 == 0:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(records, f, ensure_ascii=False, indent=2)
            print(f"    ✓ Checkpoint: {idx}/{total_errors}")

    # Final save
    with open(path, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

    print(f"  ✓ {label} backfill done: {success} fixed, {still_failed} still failing")


def main():
    parser = argparse.ArgumentParser(description="AIAS v0.23 backfill — retry failed probes")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if not args.dry_run:
        missing = [v for v in ["ANTHROPIC_API_KEY", "OPENAI_API_KEY", "GOOGLE_API_KEY"] if not os.environ.get(v)]
        if missing:
            print(f"ERROR: Missing env vars: {', '.join(missing)}")
            sys.exit(1)

    print("=" * 60)
    print("AIAS v0.23 — Backfill failed probes")
    print("=" * 60)

    backfill_file(DATA_DIR / "v23_phase_a_raw.json", "Phase A", dry_run=args.dry_run)
    backfill_file(DATA_DIR / "v23_phase_b_raw.json", "Phase B", dry_run=args.dry_run)

    if not args.dry_run:
        # Verification pass
        print("\n" + "=" * 60)
        print("Verification")
        print("=" * 60)
        for fname, expected in [("v23_phase_a_raw.json", 144), ("v23_phase_b_raw.json", 36)]:
            p = DATA_DIR / fname
            if p.exists():
                data = json.load(open(p))
                ok = sum(1 for r in data if r["status"] == "ok")
                err = sum(1 for r in data if r["status"] == "error")
                print(f"  {fname}: {len(data)} total, {ok} ok, {err} errors")


if __name__ == "__main__":
    main()
