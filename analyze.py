"""
AIAS Day 2 — Analysis
"""
import csv
import glob
import json
from collections import defaultdict
from datetime import datetime

csv_files = sorted(glob.glob("results_*.csv"))
if not csv_files:
    print("ERROR: no results_*.csv file found.")
    raise SystemExit(1)

latest_csv = csv_files[-1]
print(f"Reading: {latest_csv}\n")

with open(latest_csv, newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

with open("brands.json") as f:
    BRANDS = json.load(f)

ALL_BRANDS = [b["canonical"] for b in BRANDS]
TIER_OF = {b["canonical"]: b["tier"] for b in BRANDS}

mentions_by_model_brand = defaultdict(lambda: defaultdict(int))
runs_by_model = defaultdict(int)
mentions_overall_by_brand = defaultdict(int)
runs_overall = 0
mentions_by_cep_brand = defaultdict(lambda: defaultdict(int))
runs_by_cep = defaultdict(int)

for row in rows:
    if not row["raw_response"].strip():
        continue
    model = row["model"]
    cep = row["cep"]
    brands = [b for b in row["brands_found"].split("|") if b]
    runs_by_model[model] += 1
    runs_overall += 1
    runs_by_cep[cep] += 1
    for brand in brands:
        mentions_by_model_brand[model][brand] += 1
        mentions_overall_by_brand[brand] += 1
        mentions_by_cep_brand[cep][brand] += 1

def mention_rate(brand, model=None):
    if model:
        n_runs = runs_by_model[model]
        n_mentions = mentions_by_model_brand[model][brand]
    else:
        n_runs = runs_overall
        n_mentions = mentions_overall_by_brand[brand]
    return (n_mentions / n_runs * 100) if n_runs > 0 else 0.0

overall_rates = {b: mention_rate(b) for b in ALL_BRANDS}
max_rate = max(overall_rates.values()) if overall_rates else 0
aias = {b: (r / max_rate * 100) if max_rate > 0 else 0 for b, r in overall_rates.items()}

print("=" * 78)
print(f"AIAS Day 2 — Project Management Software")
print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
print("=" * 78)

print(f"\nSuccessful runs by model:")
for m in ["openai", "anthropic", "google"]:
    print(f"  {m:10s}  {runs_by_model[m]:3d} runs")
print(f"  {'TOTAL':10s}  {runs_overall:3d} runs")

print("\n" + "-" * 78)
print("AGGREGATE LEADERBOARD (all models)")
print("-" * 78)
print(f"{'Rank':<5}{'Brand':<14}{'Tier':<13}{'Mention%':>10}{'AIAS':>8}")
print("-" * 78)

ranked = sorted(ALL_BRANDS, key=lambda b: overall_rates[b], reverse=True)
for i, b in enumerate(ranked, 1):
    print(f"{i:<5}{b:<14}{TIER_OF[b]:<13}{overall_rates[b]:>9.1f}%{aias[b]:>8.1f}")

print("\n" + "-" * 78)
print("PER-MODEL MENTION RATES (top 10)")
print("-" * 78)
print(f"{'Brand':<14}{'OpenAI':>10}{'Anthropic':>12}{'Google':>10}")
print("-" * 78)
for b in ranked[:10]:
    o = mention_rate(b, "openai")
    a = mention_rate(b, "anthropic")
    g = mention_rate(b, "google")
    print(f"{b:<14}{o:>9.1f}%{a:>11.1f}%{g:>9.1f}%")

print("\n" + "-" * 78)
print("TOP BRAND BY CATEGORY ENTRY POINT")
print("-" * 78)
print(f"{'CEP':<22}{'Top Brand':<14}{'Mention %':>12}")
print("-" * 78)
for cep in sorted(runs_by_cep.keys()):
    cep_runs = runs_by_cep[cep]
    cep_top = max(ALL_BRANDS, key=lambda b: mentions_by_cep_brand[cep][b])
    cep_rate = mentions_by_cep_brand[cep][cep_top] / cep_runs * 100
    print(f"{cep:<22}{cep_top:<14}{cep_rate:>11.1f}%")

out_path = latest_csv.replace("results_", "leaderboard_")
with open(out_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["rank", "brand", "tier", "mention_rate_pct", "aias_score",
                     "openai_pct", "anthropic_pct", "google_pct"])
    for i, b in enumerate(ranked, 1):
        writer.writerow([
            i, b, TIER_OF[b],
            round(overall_rates[b], 1),
            round(aias[b], 1),
            round(mention_rate(b, "openai"), 1),
            round(mention_rate(b, "anthropic"), 1),
            round(mention_rate(b, "google"), 1),
        ])

print("\n" + "=" * 78)
print(f"Saved leaderboard to: {out_path}")
print("=" * 78)
