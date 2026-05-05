"""
AIAS — Re-extraction
Reads the merged household_v1.0 final CSV, runs the function-calling extractor on
every successful response, deduplicates by canonical brand within each response,
and saves an enriched CSV with rank, sentiment, and is_primary_recommendation columns.
"""
import os
import csv
import json
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI
from extractor import extract_brands

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ----- INPUTS -----
INPUT_CSV = "results_v2_household_v1.0_final.csv"
CATEGORY_DESCRIPTION = "household goods retailers"

with open("brands.json") as f:
    _raw = json.load(f)
    BRANDS = _raw["brands"] if isinstance(_raw, dict) else _raw

print(f"Reading: {INPUT_CSV}")
print(f"Category: {CATEGORY_DESCRIPTION}")
print(f"Registry: {len(BRANDS)} brands")

with open(INPUT_CSV, newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

successful = [r for r in rows if r["raw_response"].strip()]
print(f"Re-extracting {len(successful)} successful responses...\n")

enriched_rows = []
for i, row in enumerate(rows, 1):
    if not row["raw_response"].strip():
        row["brands_canonical"] = ""
        row["brands_unknown"] = ""
        row["brands_ranked"] = ""
        row["primary_recommendation"] = ""
        row["sentiment_summary"] = ""
        row["extraction_method"] = ""
        enriched_rows.append(row)
        continue

    slot = row.get("model_slot", row.get("model", "?"))
    print(f"  [{i:3d}/{len(rows)}] {row['prompt_id']:18s} | {slot:18s} | run {row['run_idx']}", end=" ", flush=True)
    try:
        extracted = extract_brands(row["raw_response"], BRANDS, client, CATEGORY_DESCRIPTION)

        seen = set()
        deduped = []
        for e in extracted:
            key = e["canonical"] or f"UNK:{e['raw_mention'].lower()}"
            if key in seen:
                continue
            seen.add(key)
            deduped.append(e)

        canonicals = [e["canonical"] for e in deduped if e["canonical"]]
        unknowns = [e["raw_mention"] for e in deduped if not e["canonical"]]
        ranked = [f"{e['canonical']}@{e['rank']}" for e in deduped if e["canonical"]]
        primary = [e["canonical"] for e in deduped if e.get("is_primary_recommendation") and e["canonical"]]
        sentiments = [e["sentiment"] for e in deduped if e["canonical"]]
        sent_summary = f"pos:{sentiments.count('positive')}|neu:{sentiments.count('neutral')}|neg:{sentiments.count('negative')}"
        method = deduped[0]["extraction_method"] if deduped else "none"

        row["brands_canonical"] = "|".join(canonicals)
        row["brands_unknown"] = "|".join(unknowns)
        row["brands_ranked"] = "|".join(ranked)
        row["primary_recommendation"] = "|".join(primary)
        row["sentiment_summary"] = sent_summary
        row["extraction_method"] = method
        print(f"-> {len(canonicals)} known, {len(unknowns)} unknown")
    except Exception as e:
        print(f"-> FAILED: {type(e).__name__}: {e}")
        row["brands_canonical"] = ""
        row["brands_unknown"] = ""
        row["brands_ranked"] = ""
        row["primary_recommendation"] = ""
        row["sentiment_summary"] = ""
        row["extraction_method"] = "failed"

    enriched_rows.append(row)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
out_path = f"results_enriched_household_v1.0_{timestamp}.csv"
fieldnames = list(enriched_rows[0].keys())
with open(out_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(enriched_rows)

print()
print("=" * 70)
print(f"Saved {len(enriched_rows)} rows to {out_path}")
print("=" * 70)