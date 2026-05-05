"""
AIAS Phase 2 — Spot-check sampler for human audit of valence classifications.

Reads manual_review_bbb_*.csv, selects a stratified sample for human review,
prints quotes + AI labels in a readable format, and saves a CSV with empty
columns for human verdicts.

Stratification:
  - All live_recommendation rows (5)
  - All status_correction rows (7)
  - All ambiguous rows (1)
  - 6 random live_with_caveat rows
  - 6 random historical_reference rows
  Total: ~25 rows
"""
import csv
import glob
import random
from datetime import datetime

random.seed(42)  # reproducible sample

manual_review_files = sorted([f for f in glob.glob("manual_review_bbb_*.csv") if "checkpoint" not in f])
INPUT_CSV = manual_review_files[-1]

with open(INPUT_CSV, newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

# Stratify
by_valence = {}
for r in rows:
    by_valence.setdefault(r["valence"], []).append(r)

sample = []
sample.extend(by_valence.get("live_recommendation", []))     # ALL
sample.extend(by_valence.get("status_correction", []))       # ALL
sample.extend(by_valence.get("ambiguous", []))               # ALL

caveats = by_valence.get("live_with_caveat", [])
random.shuffle(caveats)
sample.extend(caveats[:6])

historical = by_valence.get("historical_reference", [])
random.shuffle(historical)
sample.extend(historical[:6])

# Print
print("=" * 110)
print(f"AIAS PHASE 2 - SPOT-CHECK SAMPLE FOR HUMAN AUDIT")
print(f"Source: {INPUT_CSV}")
print(f"Sample size: {len(sample)} of {len(rows)} ({100*len(sample)/len(rows):.0f}%)")
print(f"Stratification:")
for v in ["live_recommendation", "live_with_caveat", "status_correction", "historical_reference", "ambiguous"]:
    in_sample = sum(1 for s in sample if s["valence"] == v)
    in_total = len(by_valence.get(v, []))
    print(f"  {v:25s}  {in_sample:>2d} of {in_total} ({100*in_sample/in_total:.0f}% of category)")
print("=" * 110)
print()
print("INSTRUCTIONS:")
print("  Read each quote below. The AI assigned a valence label. Decide:")
print("  - AGREE: AI's label is correct")
print("  - DISAGREE: AI's label is wrong (note what the correct label would be)")
print("  - UNCLEAR: too ambiguous to decide")
print()
print("Categories reminder:")
print("  live_recommendation  = AI presents BBB as fully live, no caveat")
print("  live_with_caveat     = AI surfaces BBB but discloses closure/rebrand")
print("  status_correction    = AI explicitly says BBB is closed, does NOT recommend")
print("  historical_reference = AI mentions BBB only in past tense, not as current option")
print("  ambiguous            = cannot determine")
print()
print("=" * 110)
print()

for i, r in enumerate(sample, 1):
    print(f"#{i} ─────────────────────────────────────────────────────────────────────")
    print(f"   Slot: {r['model_slot']:20s}  CEP: {r['cep']:22s}  Run: {r['run_idx']}")
    print(f"   AI valence: {r['valence']}")
    print(f"   AI entity:  {r['entity_reference']}")
    print()
    print(f"   QUOTE:")
    quote = r['source_quote'].strip()
    # Wrap quote at ~95 chars per line for readability
    line = ""
    for word in quote.split():
        if len(line) + len(word) + 1 > 95:
            print(f"     {line}")
            line = word
        else:
            line = f"{line} {word}".strip()
    if line:
        print(f"     {line}")
    print()

# Save CSV with empty verdict column for the human reviewer
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
out_path = f"spot_check_audit_{timestamp}.csv"
with open(out_path, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["item_num", "slot", "cep", "run_idx", "ai_valence", "ai_entity", "quote",
                "human_verdict", "human_correct_label", "notes"])
    for i, r in enumerate(sample, 1):
        w.writerow([i, r["model_slot"], r["cep"], r["run_idx"],
                    r["valence"], r["entity_reference"], r["source_quote"],
                    "", "", ""])

print(f"Saved blank audit CSV: {out_path}")
print()
print("After reading, you can either:")
print("  - Tell me the item numbers you disagree on (faster)")
print("  - Open the CSV in Excel/Numbers and fill in the verdict columns")
