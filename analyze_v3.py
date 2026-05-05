"""AI Presence Index v0.3 - first of six AIAS components."""
import csv
import glob
import json
from collections import defaultdict
from datetime import datetime
from statistics import mean, stdev

csv_files = sorted(glob.glob("results_enriched_household_v1.0_*.csv"))
latest_csv = csv_files[-1]
print(f"Reading: {latest_csv}\n")

with open(latest_csv, newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

with open("brands.json") as f:
    raw = json.load(f)
    if isinstance(raw, list):
        BRANDS = raw
        CATEGORY = "Unknown Category"
    else:
        BRANDS = raw["brands"]
        CATEGORY = raw.get("category", "Unknown Category")

ALL_BRANDS = [b["canonical"] for b in BRANDS]
TIER_OF = {b["canonical"]: b["tier"] for b in BRANDS}
SLOT_KEY = "model_slot" if rows and "model_slot" in rows[0] else "model"
MODELS_PRESENT = sorted({r[SLOT_KEY] for r in rows if r.get(SLOT_KEY)})

mention_mb = defaultdict(lambda: defaultdict(int))
ranksum_mb = defaultdict(lambda: defaultdict(float))
primary_mb = defaultdict(lambda: defaultdict(int))
runs_m = defaultdict(int)
mention_o = defaultdict(int)
ranksum_o = defaultdict(float)
primary_o = defaultdict(int)
runs_o = 0
mention_cb = defaultdict(lambda: defaultdict(int))
runs_c = defaultdict(int)
unknowns = defaultdict(int)
mention_csb = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
runs_cs = defaultdict(lambda: defaultdict(int))

for row in rows:
    if not row.get("brands_canonical") and not row.get("brands_unknown"):
        continue
    m = row[SLOT_KEY]
    c = row["cep"]
    runs_m[m] += 1
    runs_o += 1
    runs_c[c] += 1
    runs_cs[c][m] += 1
    pairs = []
    if row.get("brands_ranked"):
        for p in row["brands_ranked"].split("|"):
            if "@" in p:
                n, r = p.rsplit("@", 1)
                try: pairs.append((n, int(r)))
                except: pass
    primary = set(row.get("primary_recommendation", "").split("|")) if row.get("primary_recommendation") else set()
    seen = set()
    for b, r in pairs:
        if b in seen: continue
        seen.add(b)
        mention_mb[m][b] += 1
        ranksum_mb[m][b] += 1.0 / r
        mention_o[b] += 1
        ranksum_o[b] += 1.0 / r
        mention_cb[c][b] += 1
        mention_csb[c][m][b] += 1
        if b in primary:
            primary_mb[m][b] += 1
            primary_o[b] += 1
    if row.get("brands_unknown"):
        for u in row["brands_unknown"].split("|"):
            if u.strip(): unknowns[u.strip()] += 1

def pres(b, m=None):
    if m: return (mention_mb[m][b]/runs_m[m]*100) if runs_m[m] else 0.0
    return (mention_o[b]/runs_o*100) if runs_o else 0.0

def rsom(b):
    return (ranksum_o[b]/runs_o*100) if runs_o else 0.0

def prate(b):
    return (primary_o[b]/runs_o*100) if runs_o else 0.0

def consist(b):
    vals = [pres(b, m) for m in MODELS_PRESENT]
    avg = mean(vals)
    if avg == 0 or len(vals) < 2: return 0.0
    return max(0.0, (1.0 - stdev(vals)/avg) * 100)

print("=" * 110)
print(f"AI PRESENCE INDEX v0.3 - {CATEGORY}")
print("First of six AIAS components per the Tri-System framework")
print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
print("=" * 110)
print(f"\nMethodology: Presence-only. Other columns are descriptive transparency only.")
print(f"Runs: " + " | ".join(f"{m}={runs_m[m]}" for m in MODELS_PRESENT) + f" | total={runs_o}\n")

print("-" * 110)
print("LEADERBOARD (sorted by Presence)")
print("-" * 110)
print(f"{'#':<3}{'Brand':<22}{'Tier':<13}{'Presence':>10}{'Consist':>10}{'RankSOM':>10}{'Primary%':>10}")
print("-" * 110)
ranked = sorted(ALL_BRANDS, key=lambda b: pres(b), reverse=True)
for i, b in enumerate(ranked, 1):
    print(f"{i:<3}{b:<22}{TIER_OF[b]:<13}{pres(b):>9.1f} {consist(b):>9.1f} {rsom(b):>9.1f} {prate(b):>9.1f}")

print("\n" + "-" * 110)
print("PER-MODEL PRESENCE (top 10)")
print("-" * 110)
print(f"{'Brand':<22}" + "".join(f"{m[:14]:>16}" for m in MODELS_PRESENT) + f"{'Spread':>10}")
print("-" * 110)
for b in ranked[:10]:
    vals = [pres(b, m) for m in MODELS_PRESENT]
    line = f"{b:<22}" + "".join(f"{v:>15.1f}" for v in vals) + f"{(max(vals)-min(vals)):>10.1f}"
    print(line)

print("\n" + "-" * 110)
print("TOP BRANDS BY CEP")
print("-" * 110)
for cep in sorted(runs_c.keys()):
    cr = runs_c[cep]
    top = sorted(ALL_BRANDS, key=lambda b: mention_cb[cep][b], reverse=True)[:3]
    parts = [f"{b} ({mention_cb[cep][b]/cr*100:.0f}%)" for b in top if mention_cb[cep][b] > 0]
    print(f"  {cep:<22} " + " | ".join(parts))

print("\n" + "-" * 110)
print("BBB & Pier 1 - per-CEP, per-slot detail (phantom-relevant)")
print("-" * 110)
print(f"{'CEP':<22}" + "".join(f"{m[:14]:>16}" for m in MODELS_PRESENT))
print("-" * 110)
for tracked_brand in ["Bed Bath & Beyond", "Pier 1"]:
    print(f"\n  {tracked_brand}:")
    for cep in sorted(runs_c.keys()):
        line = f"  {cep:<22}"
        for m in MODELS_PRESENT:
            n = mention_csb[cep][m][tracked_brand]
            r = runs_cs[cep][m]
            v = (n/r*100) if r else 0.0
            line += f"{v:>15.1f}"
        print(line)

print("\n" + "-" * 110)
print("UNKNOWN BRANDS (top 15)")
print("-" * 110)
for n, c in sorted(unknowns.items(), key=lambda x: x[1], reverse=True)[:15]:
    print(f"  {n:<40} {c} mentions")

out = latest_csv.replace("results_enriched_", "presence_index_v0.3_")
with open(out, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    hdr = ["rank","brand","tier","presence","consistency","rank_som","primary_pct"]
    hdr += [f"presence_{m}" for m in MODELS_PRESENT]
    w.writerow(hdr)
    for i, b in enumerate(ranked, 1):
        row = [i, b, TIER_OF[b], round(pres(b),1), round(consist(b),1), round(rsom(b),1), round(prate(b),1)]
        for m in MODELS_PRESENT: row.append(round(pres(b,m),1))
        w.writerow(row)

print(f"\n{'='*110}")
print(f"Saved: {out}")
print("Headline metric: Presence (raw mention rate, NOT normalized).")
print("=" * 110)
