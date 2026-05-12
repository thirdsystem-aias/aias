"""v0.14 Trends rescaling and per-wave aggregation (premium tea).

Reads bundle raw responses from v0.14's locked acquisition session
(/v14/data/trends_raw/{region}/), applies pivot rescaling per v0.13 pre-reg
sec.5.1, slices into t1 and t2 wave windows, applies E1b eligibility and E5
sparsity flags. Mirrors v0.13's rescale logic verbatim — only the input
data and bundle composition change.

Scope: v0.14 fresh-acquisition only. Premium tea is a new category in the
programme; no reuse-arm.

Single category. Bundle composition matches acquire_trends_v14.py exactly:
    premium_tea: Twinings pivot (4 bundles)

Pivot appears in every bundle. To avoid double-counting, its per-day row is
sourced from bundle 1 only.

No padding entries in v0.14 (16 non-pivot eligible brands divide exactly
into 4 bundles of 4). The padding mechanism is retained in code shape for
v0.13 compatibility but not exercised.

Outputs:
    /v14/data/trends_processed/per_brand_per_day.csv
    /v14/data/trends_processed/per_brand_within_window.csv
    (summary tables printed to stdout)

No SerpAPI calls. Pure post-processing on locked acquisition data.

Run:
    python3 ~/aias/scripts/rescale_trends_v14.py
"""
import csv
import json
import statistics
from datetime import datetime
from pathlib import Path

# ============================================================================
# Bundle composition (must match acquire_trends_v14.py exactly)
# ============================================================================

CATEGORIES = {
    "premium_tea": {
        "pivot": "Twinings",
        "bundles": [
            {"id": 1, "members": [
                ("Twinings", False), ("TWG Tea", False), ("Jing Tea", False),
                ("Yunnan Sourcing", False), ("Ippodo Tea", False)]},
            {"id": 2, "members": [
                ("Twinings", False), ("Marukyu Koyamaen", False), ("Lupicia", False),
                ("Ito En", False), ("Fortnum & Mason", False)]},
            {"id": 3, "members": [
                ("Twinings", False), ("Whittard of Chelsea", False), ("Tea Pigs", False),
                ("Tea Box", False), ("Harney & Sons", False)]},
            {"id": 4, "members": [
                ("Twinings", False), ("Rishi Tea", False), ("Numi Organic Tea", False),
                ("Smith Teamaker", False), ("Republic of Tea", False)]},
        ],
    },
}

REGIONS = ["worldwide", "US"]

# Wave windows per v0.13 §6 (inclusive on both ends; v0.14 inherits same
# wave windows for cross-phase comparability).
T1_START = datetime(2026, 4, 27)
T1_END   = datetime(2026, 5,  3)
T2_START = datetime(2026, 5,  4)
T2_END   = datetime(2026, 5, 10)

# n-floor per v0.13 §3.6a; v0.14 also references via pre-reg inheritance
N_FLOOR_HARD  = 10
N_FLOOR_ALIGN = 12

V14_ROOT = Path.home() / "aias" / "osf" / "v14"
RAW_ROOT = V14_ROOT / "data" / "trends_raw"
OUT_DIR  = V14_ROOT / "data" / "trends_processed"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def load_bundle_raw(region, category, bundle_id):
    region_dir = RAW_ROOT / region
    candidates = sorted(region_dir.glob(f"{category}_bundle_{bundle_id}_*.json"))
    if not candidates:
        raise FileNotFoundError(f"No raw file for {category} bundle {bundle_id} in {region}")
    if len(candidates) > 1:
        print(f"  WARN: multiple raw files for {category} bundle {bundle_id}/{region}; using latest")
    return json.loads(candidates[-1].read_text())


def parse_serpapi_date(date_str):
    """Parse SerpAPI date string like 'Apr 27, 2026'."""
    return datetime.strptime(date_str, "%b %d, %Y")


def assign_wave(date):
    if T1_START <= date <= T1_END:
        return "t1"
    if T2_START <= date <= T2_END:
        return "t2"
    return None


# ============================================================================
# Build per-day rescaled values
# ============================================================================

per_day_rows = []

for region in REGIONS:
    for category, cat_spec in CATEGORIES.items():
        pivot_name = cat_spec["pivot"]
        for bundle in cat_spec["bundles"]:
            bundle_id = bundle["id"]
            members = bundle["members"]
            raw = load_bundle_raw(region, category, bundle_id)
            timeline = raw.get("interest_over_time", {}).get("timeline_data", [])

            for point in timeline:
                date_str = point.get("date", "")
                try:
                    date = parse_serpapi_date(date_str)
                except ValueError:
                    continue
                wave = assign_wave(date)
                if wave is None:
                    continue

                values = point.get("values", [])
                if len(values) != len(members):
                    print(f"  WARN: {category}/bundle{bundle_id}/{region} on {date_str}: "
                          f"got {len(values)} values, expected {len(members)}")
                    continue

                try:
                    pivot_raw = int(values[0]["extracted_value"])
                except (KeyError, ValueError, TypeError):
                    continue

                for i, (member_name, is_padding) in enumerate(members):
                    if is_padding:
                        continue
                    # Pivot is in every bundle for its category. Record its
                    # per-day row only from bundle 1 to avoid duplication.
                    if i == 0 and member_name == pivot_name:
                        if bundle_id != 1:
                            continue
                        raw_val = pivot_raw
                        rescaled = 100.0
                    else:
                        try:
                            raw_val = int(values[i]["extracted_value"])
                        except (KeyError, ValueError, TypeError):
                            raw_val = None
                        if raw_val is None or pivot_raw == 0:
                            rescaled = None
                        else:
                            rescaled = raw_val / pivot_raw * 100.0

                    per_day_rows.append({
                        "brand": member_name,
                        "category": category,
                        "region": region,
                        "bundle_id": bundle_id,
                        "date": date.strftime("%Y-%m-%d"),
                        "wave": wave,
                        "raw_value": raw_val if raw_val is not None else "",
                        "pivot_raw_value": pivot_raw,
                        "rescaled_value": (round(rescaled, 2) if rescaled is not None else ""),
                    })

per_day_path = OUT_DIR / "per_brand_per_day.csv"
with per_day_path.open("w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "brand", "category", "region", "bundle_id", "date", "wave",
        "raw_value", "pivot_raw_value", "rescaled_value",
    ])
    writer.writeheader()
    writer.writerows(per_day_rows)
print(f"Per-day file: {per_day_path}  ({len(per_day_rows)} rows)")

# ============================================================================
# Per-brand within-window aggregation
# ============================================================================

groups = {}
for r in per_day_rows:
    if r["rescaled_value"] == "":
        continue
    key = (r["brand"], r["category"], r["region"], r["wave"])
    groups.setdefault(key, []).append(r["rescaled_value"])

# Also track raw-value statistics for E1b documentation
raw_groups = {}
for r in per_day_rows:
    if r["raw_value"] == "":
        continue
    key = (r["brand"], r["category"], r["region"], r["wave"])
    raw_groups.setdefault(key, []).append(r["raw_value"])

brands_seen = sorted({(r["brand"], r["category"]) for r in per_day_rows})
agg_rows = []

for brand, category in brands_seen:
    for region in REGIONS:
        row = {"brand": brand, "category": category, "region": region}
        for wave in ("t1", "t2"):
            key = (brand, category, region, wave)
            vals = groups.get(key, [])
            raws = raw_groups.get(key, [])
            row[f"{wave}_n_days_total"] = len(raws)
            row[f"{wave}_n_nonzero_days"] = sum(1 for v in vals if v > 0)
            if vals:
                m = statistics.mean(vals)
                sd = statistics.stdev(vals) if len(vals) > 1 else 0.0
                raw_mean = statistics.mean(raws) if raws else 0
                raw_sd = statistics.stdev(raws) if len(raws) > 1 else 0.0
                row[f"{wave}_mean"] = round(m, 2)
                row[f"{wave}_sd"] = round(sd, 2)
                row[f"{wave}_min"] = round(min(vals), 2)
                row[f"{wave}_max"] = round(max(vals), 2)
                row[f"{wave}_raw_mean"] = round(raw_mean, 2)
                row[f"{wave}_raw_sd"] = round(raw_sd, 2)
                # E1b strict: rescaled mean > 0 AND rescaled stdev > 0
                row[f"{wave}_eligible_E1b"] = m > 0 and sd > 0
                # E1b strict on raw: catches constant-raw-value cases
                row[f"{wave}_raw_eligible"] = raw_mean > 0 and raw_sd > 0
            else:
                row[f"{wave}_mean"] = ""
                row[f"{wave}_sd"] = ""
                row[f"{wave}_min"] = ""
                row[f"{wave}_max"] = ""
                row[f"{wave}_raw_mean"] = ""
                row[f"{wave}_raw_sd"] = ""
                row[f"{wave}_eligible_E1b"] = False
                row[f"{wave}_raw_eligible"] = False
            row[f"{wave}_sparse_E5"] = row[f"{wave}_n_nonzero_days"] < 4

        agg_rows.append(row)

agg_path = OUT_DIR / "per_brand_within_window.csv"
with agg_path.open("w", newline="") as f:
    fieldnames = ["brand", "category", "region"]
    for wave in ("t1", "t2"):
        fieldnames += [
            f"{wave}_n_days_total", f"{wave}_n_nonzero_days",
            f"{wave}_mean", f"{wave}_sd", f"{wave}_min", f"{wave}_max",
            f"{wave}_raw_mean", f"{wave}_raw_sd",
            f"{wave}_eligible_E1b", f"{wave}_raw_eligible", f"{wave}_sparse_E5",
        ]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(agg_rows)
print(f"Within-window file: {agg_path}  ({len(agg_rows)} rows)")
print()

# ============================================================================
# Per-region per-category summary tables
# ============================================================================

def floor_status(n):
    if n >= N_FLOOR_ALIGN:
        return f"PASS (>= alignment {N_FLOOR_ALIGN})"
    elif n >= N_FLOOR_HARD:
        return f"PASS hard floor (>= {N_FLOOR_HARD}), magnitude binding"
    else:
        return f"BREACH (< hard floor {N_FLOOR_HARD}) — descriptive-only"


for region in REGIONS:
    for category in CATEGORIES.keys():
        cat_rows = [r for r in agg_rows if r["region"] == region and r["category"] == category]
        if not cat_rows:
            continue

        print("=" * 110)
        print(f"### {region} / {category}")
        print("=" * 110)
        print(f"{'Brand':<26} {'t1_mean':>10} {'t1_sd':>8} {'t2_mean':>10} {'t2_sd':>8} "
              f"{'E1b_t1':>7} {'E1b_t2':>7} {'rawOK_t1':>9} {'rawOK_t2':>9} {'sparse':>7}")
        print("-" * 110)

        def sort_key(r):
            m = r["t1_mean"]
            return -m if isinstance(m, (int, float)) else 0

        for row in sorted(cat_rows, key=sort_key):
            sparse = "Y" if (row["t1_sparse_E5"] or row["t2_sparse_E5"]) else ""
            print(f"{row['brand']:<26} {row['t1_mean']!s:>10} {row['t1_sd']!s:>8} "
                  f"{row['t2_mean']!s:>10} {row['t2_sd']!s:>8} "
                  f"{'Y' if row['t1_eligible_E1b'] else 'N':>7} "
                  f"{'Y' if row['t2_eligible_E1b'] else 'N':>7} "
                  f"{'Y' if row['t1_raw_eligible'] else 'N':>9} "
                  f"{'Y' if row['t2_raw_eligible'] else 'N':>9} "
                  f"{sparse:>7}")

        n_t1_eligible = sum(1 for r in cat_rows if r["t1_eligible_E1b"])
        n_t2_eligible = sum(1 for r in cat_rows if r["t2_eligible_E1b"])
        print()
        print(f"E1b eligible: t1 n={n_t1_eligible}, t2 n={n_t2_eligible}")
        print(f"n-floor (hard {N_FLOOR_HARD}, alignment {N_FLOOR_ALIGN}):")
        print(f"  t1: {floor_status(n_t1_eligible)}")
        print(f"  t2: {floor_status(n_t2_eligible)}")
        print()

print("=" * 110)
print("Rescaling complete. Next step: canonical scoring (H1-H8 per category,")
print("H7 four-regime classification, H_Regime4_replication for premium tea).")
print()
print("Next: python3 ~/aias/scripts/score_v14.py")
