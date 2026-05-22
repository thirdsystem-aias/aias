"""v0.12 Trends acquisition.

Locked at v0.12-prereg. Acquires Google Trends data across three categories
in a single session: PM software (5 bundles), Olive oil (2 bundles), Running
shoes (3 bundles) x 2 regions (Worldwide primary, US sensitivity) = 20 calls.
Single combined window 2026-04-27 to 2026-05-10 spans both wave windows;
per-wave slicing happens at scoring.

Bundle composition per pre-reg sec.5.1. PM software bundles replicate v0.11
exactly to preserve pooled-sensitivity consistency. Olive oil bundle 2 and
PM software bundle 5 use padding queries to fill the 5-slot bundle.

E1a-excluded brands (7 olive oil + 1 PM Shortcut inherited from v0.11)
are NOT acquired. Frantoio Muraglia included per E1a bundled-rescue
amendment (PASS_E5).

Pivot-anomaly check per pre-reg sec.5.4 E2.
API-failure retry per pre-reg sec.5.4 E4 (up to 3 attempts).

Reads queries from: ~/aias/osf/v12/registries/topic_id_resolution_log_v0.12.csv

Run:
    export SERPAPI_KEY="your_serpapi_key"
    python scripts/acquire_trends_v12.py
"""
import csv
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

# ============================================================================
# Configuration (locked at v0.12-prereg)
# ============================================================================

API_KEY = os.environ.get("SERPAPI_KEY")
if not API_KEY:
    sys.exit("ERROR: SERPAPI_KEY not set. Run: export SERPAPI_KEY=your_key")

V12_ROOT = Path.home() / "aias" / "osf" / "v12"
CSV_PATH = V12_ROOT / "registries" / "topic_id_resolution_log_v0.12.csv"
RAW_ROOT = V12_ROOT / "data" / "trends_raw"
LOG_PATH = V12_ROOT / "data" / "trends_acquisition_log.csv"

if not CSV_PATH.exists():
    sys.exit(f"ERROR: locked CSV not found at {CSV_PATH}")

# ============================================================================
# Read locked Phase B CSV - build brand -> acquisition_query map
# ============================================================================

brand_to_query = {}
e1a_excluded = set()
with CSV_PATH.open() as f:
    for row in csv.DictReader(f):
        brand = row["brand_canonical"]
        tier = row["final_query_tier"]
        query = row["acquisition_query"]
        if tier == "EXCLUDED_E1a":
            e1a_excluded.add(brand)
        else:
            brand_to_query[brand] = query

print(f"# CSV: {CSV_PATH.name}")
print(f"# Brands acquired:   {len(brand_to_query)}")
print(f"# Brands E1a-excluded: {len(e1a_excluded)} ({', '.join(sorted(e1a_excluded))})")
print()

# ============================================================================
# Bundle structure (locked composition per category)
# ============================================================================

# Pivot per category: (canonical_name, query)
PIVOTS = {
    "pmsoftware": ("Asana", "/m/0c3z_p8"),
    "oliveoil":   ("California Olive Ranch", "/g/11cn92g97s"),
    "running":    ("Asics", "/m/04xxy1"),
}

# Padding queries (used to fill 5-slot bundles when remainder < 4 brands).
# These are NOT brand mentions; their Trends values are not used at scoring.
PAD_PM_KANBAN = ("__pad_kanban", "kanban")
PAD_PM_AGILE  = ("__pad_agile",  "agile")
PAD_PM_SCRUM  = ("__pad_scrum",  "scrum")
PAD_OIL_GENERIC = ("__pad_olive_oil", "extra virgin olive oil")

# Bundle definitions per category. Each member is either a brand canonical
# (string) or a (label, query) tuple for padding. Pivot is prepended at runtime.
BUNDLE_DEFS = {
    "pmsoftware": [
        {"id": 1, "label": "pm-incumbents",
         "members": ["Monday", "Jira", "Trello", "Confluence"]},
        {"id": 2, "label": "pm-mid-tier-I",
         "members": ["Notion", "ClickUp", "Smartsheet", "Airtable"]},
        {"id": 3, "label": "pm-mid-tier-II",
         "members": ["Basecamp", "Coda", "Wrike", "Workfront"]},
        {"id": 4, "label": "pm-challengers",
         "members": ["Linear", "Todoist", "GitHub Projects", "Motion"]},
        {"id": 5, "label": "pm-remainder-padding",
         "members": ["Height", PAD_PM_KANBAN, PAD_PM_AGILE, PAD_PM_SCRUM]},
    ],
    "oliveoil": [
        {"id": 1, "label": "oil-mixed-tier",
         "members": ["Bertolli", "Cobram Estate", "Castillo de Canena", "Frantoio Muraglia"]},
        {"id": 2, "label": "oil-challengers-padding",
         "members": ["Brightland", "Graza", "Kosterina", PAD_OIL_GENERIC]},
    ],
    "running": [
        {"id": 1, "label": "run-incumbents",
         "members": ["Adidas", "Brooks", "New Balance", "Nike"]},
        {"id": 2, "label": "run-mid-tier-mixed",
         "members": ["Puma", "Saucony", "Altra", "Hoka"]},
        {"id": 3, "label": "run-challengers",
         "members": ["Norda", "On", "Salomon", "Topo Athletic"]},
    ],
}

REGIONS = [
    ("worldwide", ""),     # geo="" = worldwide; primary
    ("US",        "US"),   # sensitivity per pre-reg sec.4
]

ENDPOINT = "https://serpapi.com/search"
WINDOW = "2026-04-27 2026-05-10"   # combined t1 + t2 window
MAX_RETRIES = 3
RETRY_DELAY_SEC = 5
INTER_CALL_DELAY_SEC = 3

# Single locked UTC timestamp for the entire acquisition session.
LOCKED_TS = datetime.now(timezone.utc).isoformat()

# ============================================================================
# Pre-flight: prevent accidental re-run (pre-reg locks the timestamp)
# ============================================================================

if LOG_PATH.exists() and LOG_PATH.stat().st_size > 0:
    sys.exit(
        f"ERROR: {LOG_PATH} already exists.\n"
        f"Re-running would create a deviation from the pre-reg's locked\n"
        f"acquisition timestamp. If intentional, delete the log + raw_dir\n"
        f"first and document in DEVIATIONS.md:\n"
        f"  rm -rf {RAW_ROOT}\n"
        f"  rm {LOG_PATH}\n"
    )

# ============================================================================
# Resolve member -> (display_name, query, is_padding)
# ============================================================================

def resolve_member(m):
    """Resolve a bundle member to (display_name, query, is_padding)."""
    if isinstance(m, tuple):
        return m[0], m[1], True
    elif isinstance(m, str):
        if m not in brand_to_query:
            sys.exit(f"ERROR: bundle references brand {m!r} but no query "
                     f"found in CSV. Check E1a status or registry.")
        return m, brand_to_query[m], False
    else:
        sys.exit(f"ERROR: bundle member type {type(m)} not supported.")

# Verify bundle composition before any acquisition call
print("=" * 72)
print("Bundle composition verification:")
print()
for category, bundles in BUNDLE_DEFS.items():
    pivot_name, pivot_query = PIVOTS[category]
    print(f"### {category} (pivot: {pivot_name} = {pivot_query})")
    for bundle in bundles:
        members_resolved = [resolve_member(m) for m in bundle["members"]]
        names = [pivot_name] + [m[0] for m in members_resolved]
        queries = [pivot_query] + [m[1] for m in members_resolved]
        n_padding = sum(1 for m in members_resolved if m[2])
        print(f"  Bundle {bundle['id']} ({bundle['label']}):")
        print(f"    Members: {', '.join(names)}")
        if n_padding > 0:
            print(f"    Padding slots: {n_padding}")
    print()

# Final tally
total_brand_slots = 0
for category, bundles in BUNDLE_DEFS.items():
    for bundle in bundles:
        for m in bundle["members"]:
            _, _, is_pad = resolve_member(m)
            if not is_pad:
                total_brand_slots += 1
print(f"# Unique non-pivot brand acquisitions: {total_brand_slots} (excl. pivots in each bundle)")
print(f"# Brands in CSV not E1a: {len(brand_to_query)}")
n_bundles = sum(len(b) for b in BUNDLE_DEFS.values())
n_calls = n_bundles * len(REGIONS)
print(f"# Bundles: {n_bundles} x Regions: {len(REGIONS)} = {n_calls} SerpAPI calls")
print()

# ============================================================================
# Acquisition
# ============================================================================

print("=" * 72)
print(f"v0.12 Trends acquisition")
print(f"Locked acquisition timestamp: {LOCKED_TS}")
print(f"Window: {WINDOW}")
print("=" * 72)
print()


def call_serpapi(queries, geo):
    """Call SerpAPI with retry per pre-reg sec.5.4 E4. Returns (data, http_status, error)."""
    q_str = ",".join(queries)
    params = {
        "engine": "google_trends",
        "q": q_str,
        "data_type": "TIMESERIES",
        "date": WINDOW,
        "geo": geo,
        "no_cache": "true",
        "api_key": API_KEY,
    }
    last_status = None
    last_error = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            r = requests.get(ENDPOINT, params=params, timeout=60)
            last_status = r.status_code
            r.raise_for_status()
            data = r.json()
            if "error" in data:
                raise RuntimeError(f"SerpAPI error: {data['error']}")
            return data, last_status, None
        except Exception as e:
            last_error = str(e)
            if attempt < MAX_RETRIES:
                print(f"    Attempt {attempt} failed ({e}); "
                      f"retrying in {RETRY_DELAY_SEC}s")
                time.sleep(RETRY_DELAY_SEC)
            else:
                print(f"    Attempt {attempt} failed ({e}); no retries left")
    return None, last_status, last_error


log_rows = []
halt = False

for region_label, geo_param in REGIONS:
    if halt:
        break
    region_dir = RAW_ROOT / region_label
    region_dir.mkdir(parents=True, exist_ok=True)
    print(f"### Region: {region_label} (geo={geo_param!r})")

    for category, bundles in BUNDLE_DEFS.items():
        if halt:
            break
        pivot_name, pivot_query = PIVOTS[category]
        print(f"  Category: {category} (pivot: {pivot_name})")

        for bundle in bundles:
            bundle_id = bundle["id"]
            bundle_label = bundle["label"]
            members_resolved = [resolve_member(m) for m in bundle["members"]]
            member_names = [pivot_name] + [m[0] for m in members_resolved]
            queries = [pivot_query] + [m[1] for m in members_resolved]

            print(f"    Bundle {bundle_id} ({bundle_label}): "
                  f"{', '.join(member_names)}")
            data, http_status, error = call_serpapi(queries, geo_param)

            if data is None:
                log_rows.append({
                    "category": category,
                    "bundle_id": bundle_id, "bundle_label": bundle_label,
                    "region": region_label, "members": "|".join(member_names),
                    "queries": "|".join(queries),
                    "pull_timestamp_utc": LOCKED_TS,
                    "http_status": http_status or "",
                    "timeline_points": 0,
                    "status": "FAIL_API",
                    "raw_path": "",
                    "notes": (error or "")[:300],
                })
                print(f"      HALT per E4 (API failure after {MAX_RETRIES} attempts)")
                halt = True
                break

            ts_safe = LOCKED_TS.replace(":", "-")
            raw_path = region_dir / f"{category}_bundle_{bundle_id}_{ts_safe}.json"
            raw_path.write_text(json.dumps(data, indent=2, ensure_ascii=False))

            # E2 pivot anomaly check.
            timeline = data.get("interest_over_time", {}).get("timeline_data", [])
            n_points = len(timeline)
            pivot_values = []
            for p in timeline:
                vlist = p.get("values", [])
                if len(vlist) >= 1:
                    try:
                        pivot_values.append(int(vlist[0]["extracted_value"]))
                    except (KeyError, ValueError, TypeError):
                        pass

            pivot_anomaly = (
                not pivot_values
                or all(v == 0 for v in pivot_values)
                or len(set(pivot_values)) == 1
            )
            if pivot_anomaly:
                log_rows.append({
                    "category": category,
                    "bundle_id": bundle_id, "bundle_label": bundle_label,
                    "region": region_label, "members": "|".join(member_names),
                    "queries": "|".join(queries),
                    "pull_timestamp_utc": LOCKED_TS,
                    "http_status": http_status,
                    "timeline_points": n_points,
                    "status": "FAIL_PIVOT_ANOMALY",
                    "raw_path": str(raw_path),
                    "notes": f"pivot_values={pivot_values}"[:300],
                })
                print(f"      HALT per E2 (pivot anomaly: values={pivot_values})")
                halt = True
                break

            print(f"      PASS: {n_points} points; pivot range "
                  f"{min(pivot_values)}-{max(pivot_values)} mean "
                  f"{sum(pivot_values)/len(pivot_values):.1f}")

            log_rows.append({
                "category": category,
                "bundle_id": bundle_id, "bundle_label": bundle_label,
                "region": region_label, "members": "|".join(member_names),
                "queries": "|".join(queries),
                "pull_timestamp_utc": LOCKED_TS,
                "http_status": http_status,
                "timeline_points": n_points,
                "status": "PASS",
                "raw_path": str(raw_path),
                "notes": (
                    f"pivot_min={min(pivot_values)} "
                    f"pivot_max={max(pivot_values)} "
                    f"pivot_mean={sum(pivot_values)/len(pivot_values):.1f}"
                ),
            })

            time.sleep(INTER_CALL_DELAY_SEC)
        print()
    print()

# ============================================================================
# Write log + summary
# ============================================================================

LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
with LOG_PATH.open("w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "category", "bundle_id", "bundle_label", "region", "members", "queries",
        "pull_timestamp_utc", "http_status", "timeline_points",
        "status", "raw_path", "notes",
    ])
    writer.writeheader()
    writer.writerows(log_rows)

print("=" * 72)
n_pass = sum(1 for r in log_rows if r["status"] == "PASS")
n_fail = sum(1 for r in log_rows if r["status"] != "PASS")
print(f"Acquisition log: {LOG_PATH}")
print(f"PASS: {n_pass}  FAIL: {n_fail}")
print(f"Locked timestamp: {LOCKED_TS}")
print(f"Raw bundles at: {RAW_ROOT}")
if halt:
    print()
    print("ACQUISITION HALTED. Investigate the failure before deciding whether")
    print("to (a) document the partial run and try again with a new locked")
    print("timestamp (E4), or (b) treat the locked timestamp as final.")
    sys.exit(1)
elif n_fail == 0:
    print()
    print("Acquisition complete. Ready for pivot rescaling (sec.5.1) and scoring.")
