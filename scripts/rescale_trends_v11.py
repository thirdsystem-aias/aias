"""v0.11 Trends rescaling and per-wave aggregation.

Reads bundle raw responses from /v11/data/trends_raw/{region}/, applies
pivot rescaling per pre-reg sec.5.1, slices into t1 and t2 wave windows,
applies E1b eligibility and E5 sparsity flags.

Outputs:
    /v11/data/trends_processed/per_brand_per_day.csv
    /v11/data/trends_processed/per_brand_within_window.csv

No SerpAPI calls. Pure post-processing on locked acquisition data.

Run:
    python scripts/rescale_trends_v11.py
"""
import csv
import json
import statistics
from datetime import datetime
from pathlib import Path

# ============================================================================
# Bundle composition (must match acquire_trends_v11.py)
# ============================================================================

# Each member: (name, is_padding). Position 0 is always pivot (Asana).
BUNDLES = [
    {"id": 1, "members": [
        ("Asana", False), ("Monday", False), ("Jira", False),
        ("Trello", False), ("Confluence", False),
    ]},
    {"id": 2, "members": [
        ("Asana", False), ("Notion", False), ("ClickUp", False),
        ("Smartsheet", False), ("Airtable", False),
    ]},
    {"id": 3, "members": [
        ("Asana", False), ("Basecamp", False), ("Coda", False),
        ("Wrike", False), ("Workfront", False),
    ]},
    {"id": 4, "members": [
        ("Asana", False), ("Linear", False), ("Todoist", False),
        ("GitHub Projects", False), ("Motion", False),
    ]},
    {"id": 5, "members": [
        ("Asana", False), ("Height", False),
        ("__padding_kanban", True), ("__padding_agile", True), ("__padding_scrum", True),
    ]},
]

REGIONS = ["worldwide", "US"]

# Wave windows per pre-reg sec.4 (inclusive on both ends).
T1_START = datetime(2026, 4, 27)
T1_END   = datetime(2026, 5, 3)
T2_START = datetime(2026, 5, 4)
T2_END   = datetime(2026, 5, 10)

V11_ROOT = Path.home() / "aias" / "osf" / "v11"
RAW_ROOT = V11_ROOT / "data" / "trends_raw"
OUT_DIR  = V11_ROOT / "data" / "trends_processed"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def load_bundle_raw(region, bundle_id):
    region_dir = RAW_ROOT / region
    candidates = sorted(region_dir.glob(f"bundle_{bundle_id}_*.json"))
    if not candidates:
        raise FileNotFoundError(f"No raw file for bundle {bundle_id} in {region}")
    if len(candidates) > 1:
        print(f"  WARN: multiple raw files for bundle {bundle_id}/{region}; using latest")
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
    for bundle in BUNDLES:
        bundle_id = bundle["id"]
        members = bundle["members"]
        raw = load_bundle_raw(region, bundle_id)

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
                print(f"  WARN: bundle {bundle_id}/{region} on {date_str}: "
                      f"got {len(values)} values, expected {len(members)}")
                continue

            try:
                pivot_raw = int(values[0]["extracted_value"])
            except (KeyError, ValueError, TypeError):
                continue

            for i, (member_name, is_padding) in enumerate(members):
                if is_padding:
                    continue
                # Asana is in every bundle as pivot; record its row only once
                # per (region, day) by scoping to bundle 1.
                if i == 0 and member_name == "Asana":
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
                    "region": region,
                    "bundle_id": bundle_id,
                    "date": date.strftime("%Y-%m-%d"),
                    "wave": wave,
                    "raw_value": raw_val if raw_val is not None else "",
                    "pivot_raw_value": pivot_raw,
                    "rescaled_value": (
                        round(rescaled, 2) if rescaled is not None else ""
                    ),
                })

per_day_path = OUT_DIR / "per_brand_per_day.csv"
with per_day_path.open("w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "brand", "region", "bundle_id", "date", "wave",
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
    key = (r["brand"], r["region"], r["wave"])
    groups.setdefault(key, []).append(r["rescaled_value"])

brands_seen = sorted({r["brand"] for r in per_day_rows})
agg_rows = []

for brand in brands_seen:
    for region in REGIONS:
        row = {"brand": brand, "region": region}
        for wave in ("t1", "t2"):
            vals = groups.get((brand, region, wave), [])
            row[f"{wave}_n_days_total"] = sum(
                1 for r in per_day_rows
                if r["brand"] == brand and r["region"] == region and r["wave"] == wave
            )
            row[f"{wave}_n_nonzero_days"] = sum(1 for v in vals if v > 0)
            if vals:
                m = statistics.mean(vals)
                sd = statistics.stdev(vals) if len(vals) > 1 else 0.0
                row[f"{wave}_mean"] = round(m, 2)
                row[f"{wave}_sd"] = round(sd, 2)
                row[f"{wave}_min"] = round(min(vals), 2)
                row[f"{wave}_max"] = round(max(vals), 2)
                row[f"{wave}_eligible_E1b"] = m > 0 and sd > 0
            else:
                row[f"{wave}_mean"] = ""
                row[f"{wave}_sd"] = ""
                row[f"{wave}_min"] = ""
                row[f"{wave}_max"] = ""
                row[f"{wave}_eligible_E1b"] = False

            row[f"{wave}_sparse_E5"] = row[f"{wave}_n_nonzero_days"] < 4

        agg_rows.append(row)

agg_path = OUT_DIR / "per_brand_within_window.csv"
with agg_path.open("w", newline="") as f:
    fieldnames = ["brand", "region"]
    for wave in ("t1", "t2"):
        fieldnames += [
            f"{wave}_n_days_total", f"{wave}_n_nonzero_days",
            f"{wave}_mean", f"{wave}_sd", f"{wave}_min", f"{wave}_max",
            f"{wave}_eligible_E1b", f"{wave}_sparse_E5",
        ]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(agg_rows)
print(f"Within-window file: {agg_path}  ({len(agg_rows)} rows)")
print()

# ============================================================================
# Print summary table for primary (worldwide) region
# ============================================================================

print("=" * 96)
print(f"{'Brand':<18} {'t1_mean':>10} {'t1_sd':>8} {'t2_mean':>10} {'t2_sd':>8} "
      f"{'E1b_t1':>7} {'E1b_t2':>7} {'sparse':>7}")
print("-" * 96)

# Sort by t1_mean descending for leaderboard preview.
def sort_key(r):
    m = r["t1_mean"]
    return -m if isinstance(m, (int, float)) else 0

ww_rows = [r for r in agg_rows if r["region"] == "worldwide"]
for row in sorted(ww_rows, key=sort_key):
    sparse = "Y" if (row["t1_sparse_E5"] or row["t2_sparse_E5"]) else ""
    print(f"{row['brand']:<18} {row['t1_mean']!s:>10} {row['t1_sd']!s:>8} "
          f"{row['t2_mean']!s:>10} {row['t2_sd']!s:>8} "
          f"{'Y' if row['t1_eligible_E1b'] else 'N':>7} "
          f"{'Y' if row['t2_eligible_E1b'] else 'N':>7} "
          f"{sparse:>7}")

n_t1_eligible = sum(1 for r in ww_rows if r["t1_eligible_E1b"])
n_t2_eligible = sum(1 for r in ww_rows if r["t2_eligible_E1b"])
print()
print(f"E1b eligible (worldwide): t1 n={n_t1_eligible}, t2 n={n_t2_eligible}")
floor_status = lambda n: "PASS" if n >= 16 else "BREACH"
print(f"n-floor (16): t1 {floor_status(n_t1_eligible)}, t2 {floor_status(n_t2_eligible)}")
