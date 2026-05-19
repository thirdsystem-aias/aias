#!/usr/bin/env python3
"""
acquire_phase_a_v1_3.py — Fresh LLM acquisition for Phase A canonical disambiguation

Hits 6 LLM model slots per Protocol v1.2 §5.2 reference set with a single canonical
disambiguation query per brand. Writes per-slot response JSON files in the schema
expected by classify_phase_a_v1_3.py:
    {"model_id": str, "query": str, "response": str, ...}

Usage:
    # Dry-run (default — prints plan, no API calls):
    python scripts/acquire_phase_a_v1_3.py

    # Acquire only primary pivots from registry (default behaviour):
    python scripts/acquire_phase_a_v1_3.py --live

    # Acquire specific brands:
    python scripts/acquire_phase_a_v1_3.py --brands "Le Creuset" "All-Clad" "Vermicular" --live

    # Acquire ALL panel brands (e.g., for cascade-ready archive):
    python scripts/acquire_phase_a_v1_3.py --all-brands --live

Pre-requisites:
    - ANTHROPIC_API_KEY, OPENAI_API_KEY, GOOGLE_API_KEY in environment
      (loaded via: source ~/.aias_env after fixing to export KEY=value format)
    - Python packages: anthropic, openai, google-genai
      Install with: pip install --upgrade anthropic openai google-genai
      (NOTE: google-genai supersedes google-generativeai, which was sunset 2025-11-30)

Output layout:
    osf/v17/data/phase_a/<brand-slug>/slot_<N>.json

Slot-skip behaviour:
    On re-run, any slot_<N>.json that already exists on disk is skipped. This makes
    the script idempotent and recovery-safe: a partial-failure first pass (e.g.,
    Google slots down) can be completed by a second pass after patching the
    affected provider, without re-billing the slots that already succeeded.

OPERATOR REVIEW POINTS (search for "OPERATOR REVIEW"):
    1. SLOTS list — confirm models match v1.2 §5.2 canonical reference set
    2. CANONICAL_QUERY_TEMPLATE — confirm matches v0.16 canonical query form
"""

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ARCHIVE_DIR = ROOT / "osf" / "v17" / "data" / "phase_a"
DEFAULT_REGISTRY = ROOT / "registries" / "brands_kitchenware_v0.17.json"

# ---------------------------------------------------------------------------
# Reference model slots
# ---------------------------------------------------------------------------
# OPERATOR REVIEW: 3-provider × 2-tier balance. Slot 5 and 6 updated post v0.17
# first-run acquisition: original gemini-1.5-pro / gemini-1.5-flash returned 404
# on current GOOGLE_API_KEY (model IDs sunset by Google). Replacement IDs are
# current production-GA Gemini variants. See osf/v17/DEVIATIONS.md Entry 2.
# If billing is enabled on GOOGLE_API_KEY, slot 5 can be upgraded to
# "gemini-3.1-pro-preview" for a closer-to-original high+mid tier pairing.
# ---------------------------------------------------------------------------
SLOTS = [
    {"slot": 1, "provider": "anthropic", "model_id": "claude-opus-4-5"},
    {"slot": 2, "provider": "anthropic", "model_id": "claude-sonnet-4-5"},
    {"slot": 3, "provider": "openai",    "model_id": "gpt-4o"},
    {"slot": 4, "provider": "openai",    "model_id": "gpt-4o-mini"},
    {"slot": 5, "provider": "google",    "model_id": "gemini-2.5-flash"},
    {"slot": 6, "provider": "google",    "model_id": "gemini-2.5-flash-lite"},
]

# OPERATOR REVIEW: Confirm this matches the v0.16 canonical disambiguation
# query form. The query must be substrate-neutral so the LLM's first 100 tokens
# reveal natural anchoring (substrate vs not), not prompted anchoring.
CANONICAL_QUERY_TEMPLATE = "Who or what is {brand}?"

MAX_TOKENS_OUT = 500          # Generous; first-100-tokens truncation at classify time
INTER_CALL_DELAY_S = 2.0      # Rate-limit cushion
RETRY_ATTEMPTS = 2
RETRY_DELAY_S = 5.0


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def slugify(name: str) -> str:
    """Brand name → kebab-case filesystem slug."""
    s = name.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def brands_from_registry(registry_path: Path, mode: str) -> list:
    """Extract brand names from registry. mode ∈ {'primaries', 'all'}."""
    data = json.loads(registry_path.read_text())
    brands = []
    for cell_name, cell in data["cells"].items():
        for brand in cell["brands"]:
            if mode == "all":
                brands.append(brand["name"])
            elif mode == "primaries" and brand.get("phase_a_role") == "primary_pivot":
                brands.append(brand["name"])
    return brands


# ---------------------------------------------------------------------------
# Provider dispatch
# ---------------------------------------------------------------------------

def call_anthropic(model_id: str, query: str) -> str:
    from anthropic import Anthropic
    client = Anthropic()
    resp = client.messages.create(
        model=model_id,
        max_tokens=MAX_TOKENS_OUT,
        messages=[{"role": "user", "content": query}],
    )
    return resp.content[0].text


def call_openai(model_id: str, query: str) -> str:
    from openai import OpenAI
    client = OpenAI()
    resp = client.chat.completions.create(
        model=model_id,
        max_tokens=MAX_TOKENS_OUT,
        messages=[{"role": "user", "content": query}],
    )
    return resp.choices[0].message.content


def call_google(model_id: str, query: str) -> str:
    """
    Google GenAI SDK call. Migrated from the sunset google.generativeai package
    to the current google.genai SDK (per Google's 2025-11-30 deprecation). The
    new client auto-detects GOOGLE_API_KEY or GEMINI_API_KEY from environment.
    """
    from google import genai
    client = genai.Client()  # auto-picks GOOGLE_API_KEY / GEMINI_API_KEY
    response = client.models.generate_content(
        model=model_id,
        contents=query,
    )
    return response.text


DISPATCH = {
    "anthropic": call_anthropic,
    "openai":    call_openai,
    "google":    call_google,
}


# ---------------------------------------------------------------------------
# Acquisition
# ---------------------------------------------------------------------------

def call_with_retry(slot: dict, query: str) -> str:
    """Call a slot's LLM with bounded retry on transient failure."""
    last_exc = None
    for attempt in range(1, RETRY_ATTEMPTS + 1):
        try:
            return DISPATCH[slot["provider"]](slot["model_id"], query)
        except Exception as exc:
            last_exc = exc
            if attempt < RETRY_ATTEMPTS:
                time.sleep(RETRY_DELAY_S)
    raise last_exc


def acquire_for_brand(brand: str, live: bool) -> dict:
    """Run 6-slot acquisition for one brand. Returns per-slot outcome dict."""
    slug = slugify(brand)
    brand_dir = ARCHIVE_DIR / slug
    brand_dir.mkdir(parents=True, exist_ok=True)
    query = CANONICAL_QUERY_TEMPLATE.format(brand=brand)
    outcomes = []

    print(f"\n=== Brand: {brand} (slug: {slug}) ===")
    print(f"Query: {query!r}")

    for slot in SLOTS:
        slot_path = brand_dir / f"slot_{slot['slot']}.json"
        label = f"  [{slot['slot']}] {slot['model_id']:32s}"

        if slot_path.exists():
            print(f"{label}  SKIP (already exists)")
            outcomes.append({"slot": slot["slot"], "status": "skipped", "model_id": slot["model_id"]})
            continue

        if not live:
            print(f"{label}  DRY-RUN (would call)")
            outcomes.append({"slot": slot["slot"], "status": "dry_run", "model_id": slot["model_id"]})
            continue

        print(f"{label}  CALLING...", end=" ", flush=True)
        try:
            response = call_with_retry(slot, query)
            slot_path.write_text(json.dumps({
                "model_id": slot["model_id"],
                "provider": slot["provider"],
                "query": query,
                "response": response,
                "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            }, indent=2, ensure_ascii=False))
            n_tokens = len(response.split())
            print(f"OK ({n_tokens} ws-tokens)")
            outcomes.append({"slot": slot["slot"], "status": "ok", "model_id": slot["model_id"], "n_tokens": n_tokens})
        except Exception as exc:
            print(f"FAIL: {type(exc).__name__}: {exc}")
            outcomes.append({"slot": slot["slot"], "status": "failed", "model_id": slot["model_id"], "error": str(exc)})

        time.sleep(INTER_CALL_DELAY_S)

    return {"brand": brand, "slug": slug, "outcomes": outcomes}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Phase A canonical disambiguation acquisition per v1.3 §6.4.2",
    )
    parser.add_argument("--brands", nargs="+", help="Explicit brand names (overrides --registry)")
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY,
                        help=f"Registry JSON (default: {DEFAULT_REGISTRY.relative_to(ROOT)})")
    parser.add_argument("--all-brands", action="store_true",
                        help="Acquire all panel brands (default: primary pivots only)")
    parser.add_argument("--live", action="store_true",
                        help="Actually call APIs (default: dry-run, no API consumption)")
    args = parser.parse_args()

    # Resolve brand list
    if args.brands:
        brands = args.brands
        source = "--brands"
    else:
        if not args.registry.exists():
            sys.exit(f"ERROR: registry not found: {args.registry}")
        mode = "all" if args.all_brands else "primaries"
        brands = brands_from_registry(args.registry, mode)
        source = f"{args.registry.name} ({mode})"

    if not brands:
        sys.exit("ERROR: no brands to acquire.")

    # Plan summary
    n_calls = len(brands) * len(SLOTS)
    print(f"Phase A acquisition per v1.3 §6.4.2")
    print(f"Brands ({len(brands)}) from {source}: {brands}")
    print(f"Slots ({len(SLOTS)}): {[s['model_id'] for s in SLOTS]}")
    print(f"Plan: {len(brands)} × {len(SLOTS)} = {n_calls} API calls (worst case; skips existing slot files)")
    print(f"Archive: {ARCHIVE_DIR}")
    print(f"Mode: {'LIVE — will consume API quota' if args.live else 'DRY-RUN — no API calls'}")

    if args.live:
        for env_key in ("ANTHROPIC_API_KEY", "OPENAI_API_KEY", "GOOGLE_API_KEY"):
            if not os.environ.get(env_key):
                sys.exit(f"ERROR: {env_key} not set. Source your env file and retry.")
        confirm = input("\nProceed with LIVE acquisition? [y/N] ").strip().lower()
        if confirm != "y":
            sys.exit("Aborted.")

    # Acquire
    all_outcomes = [acquire_for_brand(brand, live=args.live) for brand in brands]

    # Summary
    print(f"\n=== Acquisition summary ===")
    for brand_result in all_outcomes:
        ok = sum(1 for o in brand_result["outcomes"] if o["status"] == "ok")
        skipped = sum(1 for o in brand_result["outcomes"] if o["status"] == "skipped")
        failed = sum(1 for o in brand_result["outcomes"] if o["status"] == "failed")
        dry = sum(1 for o in brand_result["outcomes"] if o["status"] == "dry_run")
        print(f"  {brand_result['brand']:20s}  ok={ok}  skipped={skipped}  failed={failed}  dry_run={dry}")

    if args.live:
        print(f"\nNext: edit classify_phase_a_v1_3.py constants for v0.17:")
        print(f"  V16_PHASE_A_DIR → {ARCHIVE_DIR}")
        print(f"  BRANDS → {[slugify(b) for b in brands]}")
        print(f"  LEDGER_PATH → ~/aias/osf/v17/classification_ledger.csv")
        print(f"Then: python scripts/classify_phase_a_v1_3.py  (generates ledger)")
    else:
        print(f"\nDry-run complete. Add --live to acquire.")


if __name__ == "__main__":
    main()
