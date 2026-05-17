#!/usr/bin/env python3
"""Derive prompts/prompts_kitchen_knives.json (legacy schema) from
prompts_knives_v0.16.json (new schema).

run_aias_v2.py expects each prompt to have keys:
    {"id": "...", "cep": "...", "prompt": "..."}

prompts_knives_v0.16.json has:
    {"prompt_id": "...", "intent": "...", "prompt_text": "...",
     "block": "...", "language": "...", "tradition_anchor": ...,
     "use_case_anchor": ..., "discourse_language_pair_id": ...}

This adapter:
  - Maps prompt_id → id
  - Maps prompt_text → prompt
  - Maps intent → cep (closest semantic analog; both classify the
    prompt's conceptual function for downstream grouping)
  - Wraps in {"category": ..., "prompt_set_version": ..., "prompts": [...]}

The v0.16 file remains canonical; this is a regenerable build artifact.

Other v0.16 fields (block, language, tradition_anchor, use_case_anchor,
discourse_language_pair_id) are preserved as additional keys for any
downstream consumer that wants them; run_aias_v2.py ignores extra keys.

Run:
    cd ~/aias
    python3 scripts/derive_prompts_kitchen_knives_legacy.py
"""
import json
import sys
from pathlib import Path

AIAS = Path.home() / "aias"
SRC = AIAS / "prompts" / "prompts_knives_v0.16.json"
DST = AIAS / "prompts" / "prompts_kitchen_knives.json"

if not SRC.exists():
    sys.exit(f"ERROR: {SRC} not found")

with SRC.open() as f:
    v16 = json.load(f)

print(f"Source: {SRC.name}")
print(f"  schema_version: {v16.get('schema_version')}")
print(f"  category: {v16.get('category')}")
print(f"  prompts: {len(v16['prompts'])}")
print()

# Convert each prompt
prompts_out = []
intent_counts = {}

for p in v16["prompts"]:
    # Required fields per run_aias_v2.py
    if "prompt_id" not in p or "prompt_text" not in p:
        sys.exit(f"ERROR: prompt missing required field: {p}")

    # intent → cep mapping
    cep = p.get("intent", "UNKNOWN_INTENT").upper()
    intent_counts[cep] = intent_counts.get(cep, 0) + 1

    legacy_prompt = {
        "id": p["prompt_id"],
        "cep": cep,
        "prompt": p["prompt_text"],
        # Preserve v0.16 fields for any downstream consumer
        "block": p.get("block"),
        "language": p.get("language"),
        "tradition_anchor": p.get("tradition_anchor"),
        "use_case_anchor": p.get("use_case_anchor"),
        "discourse_language_pair_id": p.get("discourse_language_pair_id"),
    }
    prompts_out.append(legacy_prompt)

# Construct legacy-schema output
legacy = {
    "category": "kitchen_knives",
    "prompt_set_version": "kitchen_knives_v0.16_legacy_adapter_v1",
    "source_canonical": "prompts_knives_v0.16.json",
    "adapter_note": ("Derived from prompts_knives_v0.16.json (new schema "
                     "with prompt_id/intent/prompt_text) for compatibility "
                     "with run_aias_v2.py's prompt['id'], prompt['cep'], "
                     "prompt['prompt'] access pattern. v0.16 file remains "
                     "canonical; this is a regenerable build artifact."),
    "prompts": prompts_out,
}

# If the symlink exists at DST, remove it first
if DST.is_symlink():
    DST.unlink()
    print(f"Removed existing symlink at {DST}")

with DST.open("w") as f:
    json.dump(legacy, f, indent=2, ensure_ascii=False)
    f.write("\n")

print(f"Wrote: {DST}")
print(f"  prompts: {len(prompts_out)}")
print()
print(f"CEP distribution (from intent):")
for cep, count in sorted(intent_counts.items()):
    print(f"  {cep:30s} {count}")
print()
print("Verification — first 2 prompts:")
for p in prompts_out[:2]:
    print(f"  {p['id']:25s} | {p['cep']:30s} | {p['prompt'][:60]}...")

print()
print("=" * 60)
print("Adapter run complete. Next: re-fire run_aias_v2.py.")
