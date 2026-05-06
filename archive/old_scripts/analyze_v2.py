"""AIAS v0.2 — Rank-weighted analysis."""
import csv, glob, json
from collections import defaultdict
from datetime import datetime

csv_files = sorted(glob.glob("results_enriched_*.csv"))
latest_csv = csv_files[-1]
print(f"Reading: {latest_csv}\n")

with open(latest_csv, newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

with open("brands.json") as f:
    BRANDS = json.load(f)

ALL_BRANDS = [b["canonical"] for b in BRANDS]
TIER_OF = {b["canonical"]: b["tier"] for b in BRANDS}

mention_by_mb = defaultdict(lambda: defaultdict(int))
ranksum_by_mb = defaultdict(lambda: defaultdict(float))
primary_by_mb = defaultdict(lambda: defaultdict(int))
runs_by_model = defaultdict(int)
mention_overall = defaultdict(int)
ranksum_overall = defaultdict(float)
primary_overall = defaultdict(int)
runs_overall = 0
mention_by_cb = defaultdict(lambda: defaultdict(int))
runs_by_cep = defaultdict(int)
unknown_counter = defaultdict(int)

for row in rows:
    if not row.get("brands_canonical") and not row.get("brands_unknown"):
        continue
    model = row["model"]
    cep = row["cep"]
    runs_by_model[model] += 1
    runs_overall += 1
    runs_by_cep[cep] += 1
    ranked_pairs = []
    if row.get("brands_ranked"):
        for pair in row["brands_ranked"].split("|"):
            if "@" in pair:
                name, r = pair.rsplit("@", 1)
                try:
                    ranked_pairs.append((name, int(r)))
                except ValueError:
                    pass
    primary_set = set(row.get("primary_recommendation", "").split("|")) if row.get("primary_recommendation") else set()
    seen = set()
    for brand, rank in ranked_pairs:
        if brand in seen:
            continue
        seen.add(brand)
        mention_by_mb[model][brand] += 1
        ranksum_by_mb[model][brand] += 1.0 / rank
        mention_overall[brand] += 1
        ranksum_overall[brand] += 1.0 / rank
        mention_by_cb[cep][brand] += 1
        if brand in primary_set:
            primary_by_mb[model][brand] += 1
            primary_overall[brand] += 1
    if row.get("brands_unknown"):
        for u in row["brands_unknown"].split("|"):
            if u.strip():
                unknown_counter[u.strip()] += 1

def mr(b, m=None):
    if m: return (mention_by_mb[m][b]/runs_by_model[m]*100) if runs_by_model[m] else 0
    return (mention_overall[b]/runs_overall*100) if runs_overall else 0

def rs(b, m=None):
    if m: return (ranksum_by_mb[m][b]/runs_by_model[m]*100) if runs_by_model[m] else 0
    return (ranksum_overall[b]/runs_overall*100) if runs_overall else 0

def pr(b, m=None):
    if m: return (primary_by_mb[m][b]/runs_by_model[m]*100) if runs_by_model[m] else 0
    return (primary_overall[b]/runs_overall*100) if runs_overall else 0

raw = {b: 0.4*mr(b) + 0.4*rs(b) + 0.2*pr(b) for b in ALL_BRANDS}
mx = max(raw.values()) if raw else 0
aias = {b: (raw[b]/mx*100) if mx else 0 for b in ALL_BRANDS}

print("=" * 80)
print(f"AIAS v0.2 — Project Management Software")
print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
print("=" * 80)
print(f"\nRuns: openai={runs_by_model['openai']} | anthropic={runs_by_model['anthropic']} | google={runs_by_model['google']} | total={runs_overall}\n")

print("-" * 80)
print("AGGREGATE LEADERBOARD")
print("-" * 80)
print(f"{'#':<3}{'Brand':<13}{'Tier':<13}{'Mention%':>10}{'RankSOM':>10}{'Primary%':>10}{'AIAS':>8}")
print("-" * 80)
ranked = sorted(ALL_BRANDS, key=lambda b: aias[b], reverse=True)
for i, b in enumerate(ranked, 1):
    print(f"{i:<3}{b:<13}{TIER_OF[b]:<13}{mr(b):>9.1f}%{rs(b):>9.1f}%{pr(b):>9.1f}%{aias[b]:>8.1f}")

print()
print("-" * 80)
print("PER-MODEL AIAS (top 8)")
print("-" * 80)
print(f"{'Brand':<14}{'OpenAI':>14}{'Anthropic':>14}{'Google':>14}")
print("-" * 80)
for b in ranked[:8]:
    vals = []
    for m in ["openai", "anthropic", "google"]:
        c = 0.4*mr(b,m) + 0.4*rs(b,m) + 0.2*pr(b,m)
        v = (c/mx*100) if mx else 0
        vals.append(f"{v:>13.1f}")
    print(f"{b:<14}" + "".join(vals))

print()
print("-" * 80)
print("TOP BRANDS BY CEP")
print("-" * 80)
for cep in sorted(runs_by_cep.keys()):
    cr = runs_by_cep[cep]
    top3 = sorted(ALL_BRANDS, key=lambda b: mention_by_cb[cep][b], reverse=True)[:3]
    pct_strs = []
    for b in top3:
        if mention_by_cb[cep][b] > 0:
            pct = mention_by_cb[cep][b]/cr*100
            pct_strs.append(f"{b} ({pct:.0f}%)")
    print(f"  {cep:<22} {' | '.join(pct_strs)}")

print()
print("-" * 80)
print("UNKNOWN BRANDS (top 10)")
print("-" * 80)
for name, count in sorted(unknown_counter.items(), key=lambda x: x[1], reverse=True)[:10]:
    print(f"  {name:<30} {count} mentions")

out_path = latest_csv.replace("results_enriched_", "leaderboard_v2_")
with open(out_path, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["rank","brand","tier","mention_pct","rank_som","primary_pct","aias","openai_aias","anthropic_aias","google_aias"])
    for i, b in enumerate(ranked, 1):
        pma = {}
        for m in ["openai","anthropic","google"]:
            c = 0.4*mr(b,m) + 0.4*rs(b,m) + 0.2*pr(b,m)
            pma[m] = round((c/mx*100) if mx else 0, 1)
        w.writerow([i, b, TIER_OF[b], round(mr(b),1), round(rs(b),1), round(pr(b),1), round(aias[b],1),
                    pma["openai"], pma["anthropic"], pma["google"]])

print()
print("=" * 80)
print(f"Saved: {out_path}")
print("=" * 80)
