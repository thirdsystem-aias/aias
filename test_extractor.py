"""Smoke test the extractor on a small sample of existing responses."""
import os
import csv
import json
import glob
from dotenv import load_dotenv
from openai import OpenAI
from extractor import extract_brands

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

with open("brands.json") as f:
    _raw = json.load(f)
    BRANDS = _raw["brands"] if isinstance(_raw, dict) else _raw

latest_csv = sorted(glob.glob("results_*.csv"))[-1]
print(f"Loading sample from: {latest_csv}\n")

with open(latest_csv, newline="", encoding="utf-8") as f:
    rows = [r for r in csv.DictReader(f) if r["raw_response"].strip()]

sample_indices = [0, len(rows)//2, len(rows)-1]
for i in sample_indices:
    row = rows[i]
    print("=" * 70)
    print(f"Sample: {row['prompt_id']} | {row['model']} | run {row['run_idx']}")
    print(f"Response (first 200 chars): {row['raw_response'][:200]}...")
    print(f"\nOLD method (regex) found: {row['brands_found']}")
    print(f"\nNEW method (function calling) extracts:")
    extracted = extract_brands(row["raw_response"], BRANDS, client)
    for e in extracted:
        canonical = e["canonical"] or f"[UNKNOWN: {e['raw_mention']}]"
        rank = e.get("rank", "-")
        sent = e.get("sentiment", "-")
        primary = "*" if e.get("is_primary_recommendation") else " "
        print(f"   {primary} #{rank}  {canonical:20s}  sentiment={sent}")
    print()

