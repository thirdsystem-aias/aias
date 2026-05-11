"""v0.11 Trends acquisition.

Locked at v0.11-prereg (commit f20ade8). Acquires Google Trends data
for 18 brands across 5 pivot bundles x 2 regions (Worldwide primary;
US sensitivity). Single combined window 2026-04-27 to 2026-05-10
spans both wave windows; per-wave slicing happens at scoring.

Bundle composition per pre-reg sec.5.1.
Pivot-anomaly check per pre-reg sec.5.4 E2.
API-failure retry per pre-reg sec.5.4 E4 (up to 3 attempts).

Run:
    export SERPAPI_KEY="your_serpapi_key"
    python scripts/acquire_trends_v11.py
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
# Configuration (locked at v0.11-prereg)
# ============================================================================

API_KEY = os.environ.get("SERPAPI_KEY")
if not API_KEY:
    sys.exit("ERROR: SERPAPI_KEY not set. Run: export SERPAPI_KEY=your_key")

PIVOT = ("Asana", "/m/0c3z_p8", False)

# Each member tuple: (canonical_or_padding_label, acquisition_query, is_padding).
# Position 0 is always the pivot (Asana) for rescaling per sec.5.1.
BUNDLES = [
    {
        "id": 1, "label": "incumbents",
        "members": [
            PIVOT,
            ("Monday",     "/g/11h1m5p60w", False),
            ("Jira",       "/g/11bc5c0lmw", False),
            ("Trello",     "/m/0h665rh", False),
            ("Confluence", "/m/05nyz0", False),
        ],
    },
    {
        "id": 2, "label": "mid-tier-I",
        "members": [
            PIVOT,
            ("Notion",     "/g/11fd7dbddz", False),
            ("ClickUp",    "/g/11g9n26732", False),
            ("Smartsheet", "/m/010h7t67", False),
            ("Airtable",   "/g/11c3ypc1q3", False),
        ],
    },
    {
        "id": 3, "label": "mid-tier-II",
        "members": [
            PIVOT,
            ("Basecamp",  "/m/0d04n6", False),
            ("Coda",      "/g/11f3h7_jw9", False),
            ("Wrike",     "wrike", False),
            ("Workfront", "workfront", False),
        ],
    },
    {
        "id": 4, "label": "challengers",
        "members": [
            PIVOT,
            ("Linear",          "linear project management", False),
            ("Todoist",         "todoist", False),
            ("GitHub Projects", "github projects", False),
            ("Motion",          "motion project management", False),
        ],
    },
    {
        "id": 5, "label": "remainder-padding",
        "members": [
            PIVOT,
            ("Height",            "height project management", False),
            ("__padding_kanban",  "kanban", True),
            ("__padding_agile",   "agile",  True),
            ("__padding_scrum",   "scrum",  True),
        ],
    },
]

REGIONS = [
    ("worldwide", ""),     # geo="" = worldwide; primary
    ("US",        "US"),   # sensitivity per pre-reg sec.4
]

ENDPOINT = "https://serpapi.com/search"
WINDOW = "2026-04-27 2026-05-10"   # combined t1 + t2 window
MAX_RETRIES = 3
RETRY_DELAY_SEC = 5
INTER_CALL_DELAY_SEC = 3

V11_ROOT = Path.home() / "aias" / "osf" / "v11"
RAW_ROOT = V11_ROOT / "data" / "trends_raw"
LOG_PATH = V11_ROOT / "data" / "trends_acquisition_log.csv"

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
# Acquisition
# ============================================================================

print("=" * 72)
print(f"v0.11 Trends acquisition")
print(f"Locked acquisition timestamp: {LOCKED_TS}")
print(f"Window: {WINDOW}")
print(f"Bundles: {len(BUNDLES)} x Regions: {len(REGIONS)} = "
      f"{len(BUNDLES)*len(REGIONS)} calls")
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

    for bundle in BUNDLES:
        bundle_id = bundle["id"]
        bundle_label = bundle["label"]
        members = bundle["members"]
        member_names = [m[0] for m in members]
        queries = [m[1] for m in members]

        print(f"  Bundle {bundle_id} ({bundle_label}): {', '.join(member_names)}")
        data, http_status, error = call_serpapi(queries, geo_param)

        if data is None:
            log_rows.append({
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
            print(f"    HALT per E4 (API failure after {MAX_RETRIES} attempts)")
            halt = True
            break

        ts_safe = LOCKED_TS.replace(":", "-")
        raw_path = region_dir / f"bundle_{bundle_id}_{ts_safe}.json"
        raw_path.write_text(json.dumps(data, indent=2))

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
            print(f"    HALT per E2 (pivot anomaly: values={pivot_values})")
            halt = True
            break

        print(f"    PASS: {n_points} points; pivot range "
              f"{min(pivot_values)}-{max(pivot_values)} mean "
              f"{sum(pivot_values)/len(pivot_values):.1f}")

        log_rows.append({
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

# ============================================================================
# Write log + summary
# ============================================================================

LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
with LOG_PATH.open("w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "bundle_id", "bundle_label", "region", "members", "queries",
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
if halt:
    print()
    print("ACQUISITION HALTED. Investigate the failure before deciding whether")
    print("to (a) document the partial run and try again with a new locked")
    print("timestamp, or (b) treat the locked timestamp as final.")
    sys.exit(1)
elif n_fail == 0:
    print()
    print("Acquisition complete. Ready for pivot rescaling (sec.5.1) and scoring.")
