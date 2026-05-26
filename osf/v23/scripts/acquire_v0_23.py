#!/usr/bin/env python3
"""
AIAS v0.23 — Premium Spirits Acquisition Script
Protocol v1.6 | Pre-reg tag: v0.23-prereg-r1

Sends:
  Phase A: 24 brands × 6 LLMs = 144 recognition probes
  Phase B: 6 recall probes × 6 LLMs = 36 recall queries
  Total: 180 API calls

Outputs:
  osf/v23/data/v23_phase_a_raw.json   (144 records)
  osf/v23/data/v23_phase_b_raw.json   (36 records)

Environment variables required:
  ANTHROPIC_API_KEY
  OPENAI_API_KEY
  GOOGLE_API_KEY

Usage (via Claude Code):
  cd /Users/pablou/aias
  python3 scripts/acquire_v0_23.py
  python3 scripts/acquire_v0_23.py --phase-a-only
  python3 scripts/acquire_v0_23.py --phase-b-only
  python3 scripts/acquire_v0_23.py --dry-run
"""

import json
import os
import sys
import time
import argparse
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Provider SDKs
# ---------------------------------------------------------------------------
import anthropic
import openai
from google import genai
from google.genai import types

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
PIPELINE_ROOT = Path("/Users/pablou/aias")
OUTPUT_DIR = PIPELINE_ROOT / "osf" / "v23" / "data"

# Model panel (fixed from v0.17)
MODELS = [
    {"slot": "M1", "name": "Claude Opus 4.5",       "provider": "anthropic", "model_id": "claude-opus-4-5"},
    {"slot": "M2", "name": "Claude Sonnet 4.5",     "provider": "anthropic", "model_id": "claude-sonnet-4-5"},
    {"slot": "M3", "name": "GPT-4o",                "provider": "openai",    "model_id": "gpt-4o"},
    {"slot": "M4", "name": "GPT-4o-mini",           "provider": "openai",    "model_id": "gpt-4o-mini"},
    {"slot": "M5", "name": "Gemini 2.5 Flash",      "provider": "google",    "model_id": "gemini-2.5-flash"},
    {"slot": "M6", "name": "Gemini 2.5 Flash Lite", "provider": "google",    "model_id": "gemini-2.5-flash-lite"},
]

# 24-brand registry
REGISTRY = [
    {"id": "S01", "brand": "Johnnie Walker",     "spirit_type": "Scotch blend",          "tier": "Global-dominant",      "parent": "Diageo",              "conglomerate": 1},
    {"id": "S02", "brand": "Hennessy",           "spirit_type": "Cognac",                "tier": "Global-dominant",      "parent": "LVMH",                "conglomerate": 1},
    {"id": "S03", "brand": "Jack Daniel's",      "spirit_type": "Tennessee whiskey",     "tier": "Global-dominant",      "parent": "Brown-Forman",        "conglomerate": 1},
    {"id": "S04", "brand": "Patrón",             "spirit_type": "Tequila",               "tier": "Global-dominant",      "parent": "Bacardi Ltd.",        "conglomerate": 1},
    {"id": "S05", "brand": "Grey Goose",         "spirit_type": "Vodka",                 "tier": "Global-dominant",      "parent": "Bacardi Ltd.",        "conglomerate": 1},
    {"id": "S06", "brand": "Bacardi",            "spirit_type": "Rum",                   "tier": "Global-dominant",      "parent": "Bacardi Ltd.",        "conglomerate": 1},
    {"id": "S07", "brand": "Bombay Sapphire",    "spirit_type": "Gin",                   "tier": "Global-dominant",      "parent": "Bacardi Ltd.",        "conglomerate": 1},
    {"id": "S08", "brand": "Jameson",            "spirit_type": "Irish whiskey",         "tier": "Global-dominant",      "parent": "Pernod Ricard",       "conglomerate": 1},
    {"id": "S09", "brand": "Lagavulin",          "spirit_type": "Scotch single malt",    "tier": "Premium-enthusiast",   "parent": "Diageo",              "conglomerate": 1},
    {"id": "S10", "brand": "Clase Azul",         "spirit_type": "Tequila",               "tier": "Premium-enthusiast",   "parent": "Independent",         "conglomerate": 0},
    {"id": "S11", "brand": "Hendrick's",         "spirit_type": "Gin",                   "tier": "Premium-enthusiast",   "parent": "William Grant & Sons","conglomerate": 0},
    {"id": "S12", "brand": "Woodford Reserve",   "spirit_type": "Bourbon",               "tier": "Premium-enthusiast",   "parent": "Brown-Forman",        "conglomerate": 1},
    {"id": "S13", "brand": "Monkey 47",          "spirit_type": "Gin",                   "tier": "Premium-enthusiast",   "parent": "Pernod Ricard",       "conglomerate": 1},
    {"id": "S14", "brand": "The Balvenie",       "spirit_type": "Scotch single malt",    "tier": "Premium-enthusiast",   "parent": "William Grant & Sons","conglomerate": 0},
    {"id": "S15", "brand": "Rémy Martin",        "spirit_type": "Cognac",                "tier": "Premium-enthusiast",   "parent": "Rémy Cointreau",      "conglomerate": 0},
    {"id": "S16", "brand": "Casamigos",          "spirit_type": "Tequila",               "tier": "Premium-enthusiast",   "parent": "Diageo",              "conglomerate": 1},
    {"id": "S17", "brand": "Fortaleza",          "spirit_type": "Tequila",               "tier": "Craft-cult-emerging",  "parent": "Independent",         "conglomerate": 0},
    {"id": "S18", "brand": "Compass Box",        "spirit_type": "Scotch blend (craft)",  "tier": "Craft-cult-emerging",  "parent": "Independent",         "conglomerate": 0},
    {"id": "S19", "brand": "Nikka",              "spirit_type": "Japanese whisky",       "tier": "Craft-cult-emerging",  "parent": "Asahi Group",         "conglomerate": 0},
    {"id": "S20", "brand": "Del Maguey",         "spirit_type": "Mezcal",                "tier": "Craft-cult-emerging",  "parent": "Pernod Ricard",       "conglomerate": 1},
    {"id": "S21", "brand": "Fernet-Branca",      "spirit_type": "Amaro",                 "tier": "Craft-cult-emerging",  "parent": "Branca family",       "conglomerate": 0},
    {"id": "S22", "brand": "Redbreast",          "spirit_type": "Irish whiskey",         "tier": "Craft-cult-emerging",  "parent": "Pernod Ricard",       "conglomerate": 1},
    {"id": "S23", "brand": "St. George Spirits", "spirit_type": "Multi-spirit craft",    "tier": "Craft-cult-emerging",  "parent": "Independent",         "conglomerate": 0},
    {"id": "S24", "brand": "Mezcal Vago",        "spirit_type": "Mezcal",                "tier": "Craft-cult-emerging",  "parent": "Independent",         "conglomerate": 0},
]

# Phase A probe template
PHASE_A_TEMPLATE = """What do you know about {BRAND_NAME}? Specifically, I'm interested in it as a premium spirits brand — its positioning, reputation, product range, and how it fits within the broader {SPIRIT_TYPE} category. Please be detailed and specific."""

# Phase B recall probes
PHASE_B_PROBES = [
    {
        "probe_id": "EA-1",
        "channel": "editorial-authority",
        "label": "Critical consensus",
        "prompt": "Which premium spirits brands are most highly regarded by leading spirits critics and publications such as Whisky Advocate, Wine Enthusiast, or The Spirits Business? I'm looking for brands that consistently receive top ratings and critical acclaim across spirit categories. List specific brands and explain why each is well-regarded.",
    },
    {
        "probe_id": "EA-2",
        "channel": "editorial-authority",
        "label": "Awards authority",
        "prompt": "What spirits brands have the strongest track record at major international competitions — San Francisco World Spirits Competition, International Wine & Spirit Competition (IWSC), International Spirits Challenge? Name specific brands and describe their competitive record.",
    },
    {
        "probe_id": "EA-3",
        "channel": "editorial-authority",
        "label": "Professional authority",
        "prompt": "If I asked a professional bartender or spirits sommelier to recommend premium spirits across categories — whisky, gin, tequila, vodka, rum, cognac, mezcal — which brands would they most likely name? Give me specific brand recommendations with reasoning.",
    },
    {
        "probe_id": "CC-1",
        "channel": "cultural-cult",
        "label": "Enthusiast community",
        "prompt": "Which premium spirits brands have the most passionate and dedicated enthusiast communities? I'm thinking of brands that inspire collector behavior, bottle hunting, online forums, tasting groups, or cult-like followings. Name specific brands and describe their community appeal.",
    },
    {
        "probe_id": "CC-2",
        "channel": "cultural-cult",
        "label": "Cultural resonance",
        "prompt": "Which spirits brands have transcended their product category to become cultural phenomena — appearing in cocktail culture, media, lifestyle contexts, or achieving iconic status? Name specific brands and explain what makes them culturally significant beyond just being a good product.",
    },
    {
        "probe_id": "CC-3",
        "channel": "cultural-cult",
        "label": "Insider discovery",
        "prompt": "What premium spirits brands are considered hidden gems or insider picks among serious spirits enthusiasts — the brands that knowledgeable drinkers seek out but that aren't yet mainstream? Name specific brands and explain what makes them special to those in the know.",
    },
]

# Rate-limit pause between calls (seconds) — conservative to avoid throttling
PAUSE_ANTHROPIC = 2.0
PAUSE_OPENAI = 1.0
PAUSE_GOOGLE = 1.0


# ---------------------------------------------------------------------------
# API call wrappers
# ---------------------------------------------------------------------------

def call_anthropic(model_id: str, prompt: str) -> str:
    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from env
    message = client.messages.create(
        model=model_id,
        max_tokens=2048,
        temperature=0.0,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


def call_openai(model_id: str, prompt: str) -> str:
    client = openai.OpenAI()  # reads OPENAI_API_KEY from env
    response = client.chat.completions.create(
        model=model_id,
        max_tokens=2048,
        temperature=0.0,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


def call_google(model_id: str, prompt: str) -> str:
    client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
    response = client.models.generate_content(
        model=model_id,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.0,
            max_output_tokens=2048,
        ),
    )
    return response.text


PROVIDER_DISPATCH = {
    "anthropic": (call_anthropic, PAUSE_ANTHROPIC),
    "openai":    (call_openai,    PAUSE_OPENAI),
    "google":    (call_google,    PAUSE_GOOGLE),
}


def send_probe(model: dict, prompt: str) -> dict:
    """Send a single probe and return metadata + response."""
    provider = model["provider"]
    call_fn, pause = PROVIDER_DISPATCH[provider]
    ts_start = datetime.now(timezone.utc).isoformat()

    try:
        response_text = call_fn(model["model_id"], prompt)
        status = "ok"
        error_msg = None
    except Exception as e:
        response_text = ""
        status = "error"
        error_msg = str(e)

    ts_end = datetime.now(timezone.utc).isoformat()
    time.sleep(pause)

    return {
        "model_slot": model["slot"],
        "model_name": model["name"],
        "model_id": model["model_id"],
        "provider": provider,
        "prompt": prompt,
        "response": response_text,
        "status": status,
        "error": error_msg,
        "ts_start": ts_start,
        "ts_end": ts_end,
    }


# ---------------------------------------------------------------------------
# Phase runners
# ---------------------------------------------------------------------------

def run_phase_a(dry_run: bool = False) -> list[dict]:
    """Phase A: Recognition — 24 brands × 6 models = 144 probes."""
    records = []
    total = len(REGISTRY) * len(MODELS)
    count = 0

    for brand in REGISTRY:
        prompt = PHASE_A_TEMPLATE.format(
            BRAND_NAME=brand["brand"],
            SPIRIT_TYPE=brand["spirit_type"],
        )
        for model in MODELS:
            count += 1
            tag = f"[Phase A {count}/{total}] {brand['id']} {brand['brand']} → {model['slot']} {model['name']}"

            if dry_run:
                print(f"  DRY RUN: {tag}")
                continue

            print(f"  Sending: {tag}")
            result = send_probe(model, prompt)
            result["phase"] = "A"
            result["brand_id"] = brand["id"]
            result["brand_name"] = brand["brand"]
            result["spirit_type"] = brand["spirit_type"]
            result["tier"] = brand["tier"]
            result["conglomerate"] = brand["conglomerate"]
            records.append(result)

            # Checkpoint every 12 probes (two full brand sweeps)
            if count % 12 == 0 and records:
                _checkpoint(records, OUTPUT_DIR / "v23_phase_a_raw.json", count, total)

    return records


def run_phase_b(dry_run: bool = False) -> list[dict]:
    """Phase B: Two-channel Recall — 6 probes × 6 models = 36 queries."""
    records = []
    total = len(PHASE_B_PROBES) * len(MODELS)
    count = 0

    for probe in PHASE_B_PROBES:
        for model in MODELS:
            count += 1
            tag = f"[Phase B {count}/{total}] {probe['probe_id']} {probe['label']} → {model['slot']} {model['name']}"

            if dry_run:
                print(f"  DRY RUN: {tag}")
                continue

            print(f"  Sending: {tag}")
            result = send_probe(model, probe["prompt"])
            result["phase"] = "B"
            result["probe_id"] = probe["probe_id"]
            result["channel"] = probe["channel"]
            result["probe_label"] = probe["label"]
            records.append(result)

    return records


def _checkpoint(records, path, count, total):
    """Incremental save — guards against mid-run failures."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)
    print(f"  ✓ Checkpoint: {count}/{total} saved to {path.name}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="AIAS v0.23 acquisition — premium spirits")
    parser.add_argument("--dry-run", action="store_true", help="Print probe plan without sending API calls")
    parser.add_argument("--phase-a-only", action="store_true", help="Run Phase A recognition only")
    parser.add_argument("--phase-b-only", action="store_true", help="Run Phase B recall only")
    args = parser.parse_args()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    run_a = not args.phase_b_only
    run_b = not args.phase_a_only

    if args.dry_run:
        print("=" * 60)
        print("DRY RUN — no API calls will be made")
        print("=" * 60)

    # --- Env check (skip on dry run) ---
    if not args.dry_run:
        missing = []
        if run_a or run_b:
            for var in ["ANTHROPIC_API_KEY", "OPENAI_API_KEY", "GOOGLE_API_KEY"]:
                if not os.environ.get(var):
                    missing.append(var)
        if missing:
            print(f"ERROR: Missing environment variables: {', '.join(missing)}")
            sys.exit(1)

    # --- Phase A ---
    if run_a:
        print("\n" + "=" * 60)
        print("PHASE A — Recognition (24 brands × 6 models = 144 probes)")
        print("=" * 60)
        phase_a = run_phase_a(dry_run=args.dry_run)
        if phase_a:
            out_a = OUTPUT_DIR / "v23_phase_a_raw.json"
            with open(out_a, "w", encoding="utf-8") as f:
                json.dump(phase_a, f, ensure_ascii=False, indent=2)
            ok = sum(1 for r in phase_a if r["status"] == "ok")
            err = sum(1 for r in phase_a if r["status"] == "error")
            print(f"\n✓ Phase A complete: {ok} ok, {err} errors → {out_a}")

    # --- Phase B ---
    if run_b:
        print("\n" + "=" * 60)
        print("PHASE B — Two-channel Recall (6 probes × 6 models = 36 queries)")
        print("=" * 60)
        phase_b = run_phase_b(dry_run=args.dry_run)
        if phase_b:
            out_b = OUTPUT_DIR / "v23_phase_b_raw.json"
            with open(out_b, "w", encoding="utf-8") as f:
                json.dump(phase_b, f, ensure_ascii=False, indent=2)
            ok = sum(1 for r in phase_b if r["status"] == "ok")
            err = sum(1 for r in phase_b if r["status"] == "error")
            print(f"\n✓ Phase B complete: {ok} ok, {err} errors → {out_b}")

    if args.dry_run:
        probe_count = (len(REGISTRY) * len(MODELS) if run_a else 0) + (len(PHASE_B_PROBES) * len(MODELS) if run_b else 0)
        print(f"\nDry run complete. {probe_count} probes would be sent.")
    else:
        print("\n✓ Acquisition complete. Raw data in osf/v23/data/")


if __name__ == "__main__":
    main()
