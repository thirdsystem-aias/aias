#!/usr/bin/env python3
"""Generate missing_cells_v16.csv — the (prompt_id, model_slot, run_idx)
tuples for v0.16 LLM acquisition cells that are not yet OK.

Reads the original + rerun CSVs, computes (prompt × model × run_idx)
coverage, and writes a CSV of the cells that still need acquisition.

Output drives run_aias_v2.py --missing-cells-file (after patcher applied
per patch_run_aias_missing_cells.py).

Run:
    cd ~/aias
    python3 scripts/derive_missing_cells_v16.py
"""
import csv
from pathlib import Path

AIAS = Path.home() / "aias"
KK = AIAS / "data" / "kitchen_knives"

# Source CSVs (add more here if more reruns happen)
SOURCES = [
    KK / "results_v2_kitchen_knives_20260516_212400.csv",
    KK / "results_v2_kitchen_knives_20260516_212400_rerun_20260518_085706.csv",
]

OUT = KK / "missing_cells_v16.csv"

# Panel definitions
MODELS = ["anthropic_sonnet", "anthropic_opus", "openai_mini",
          "openai_flagship", "google_flash", "xai_grok"]
RUNS_PER_PROMPT = 8

# Load all prompt IDs from the v0.16 prompts file (canonical authority)
import json
prompts_file = AIAS / "prompts" / "prompts_kitchen_knives.json"
PROMPT_IDS = [p["id"] for p in json.load(open(prompts_file))["prompts"]]

print(f"Source CSVs:")
for s in SOURCES:
    if not s.exists():
        print(f"  ⚠ MISSING: {s.name}")
        continue
    n = sum(1 for _ in csv.DictReader(open(s)))
    print(f"  ✓ {s.name} ({n} rows)")
print()

# Build (prompt_id, slot, run_idx) → status across all sources
# Last write wins (so rerun OK supersedes original failed)
cells = {}
for src in SOURCES:
    if not src.exists():
        continue
    for r in csv.DictReader(open(src)):
        key = (r["prompt_id"], r["model_slot"], int(r["run_idx"]))
        cells[key] = r["call_status"]

# Find cells that are missing OR not OK
missing = []
for pid in PROMPT_IDS:
    for slot in MODELS:
        for run_idx in range(1, RUNS_PER_PROMPT + 1):
            key = (pid, slot, run_idx)
            status = cells.get(key)
            if status != "ok":
                missing.append({
                    "prompt_id": pid,
                    "model_slot": slot,
                    "run_idx": run_idx,
                    "prior_status": status if status else "never_attempted",
                })

# Write
with OUT.open("w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["prompt_id", "model_slot",
                                            "run_idx", "prior_status"])
    writer.writeheader()
    writer.writerows(missing)

print(f"Wrote: {OUT}")
print(f"  Cells to fire: {len(missing)}")
print()

# Breakdown
from collections import Counter
by_status = Counter(c["prior_status"] for c in missing)
print("By prior status:")
for s, n in by_status.most_common():
    print(f"  {s:25s} {n}")
print()
by_prompt = Counter(c["prompt_id"] for c in missing)
print("By prompt_id:")
for pid in PROMPT_IDS:
    n = by_prompt[pid]
    if n > 0:
        print(f"  {pid:25s} {n}")
print()
print("=" * 60)
print("Next: fire run_aias_v2.py with --missing-cells-file")
print()
print(f"  python3 run_aias_v2.py --category kitchen_knives \\")
print(f"      --missing-cells-file {OUT}")
