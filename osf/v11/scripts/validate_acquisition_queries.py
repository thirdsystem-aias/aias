"""Phase B validation - Confirm each brand's locked acquisition query
returns a usable Trends timeseries.

This is methodology QA, not data analysis. Uses an OUT-OF-SAMPLE window
(April 1-7, 2026) that does NOT overlap with the v0.11 wave windows
(t1: Apr 27 - May 3; t2: May 4 - May 10). The wave-window data remains
untouched until post-pre-reg-lock acquisition.

Reads: ~/aias/osf/v11/data/topic_id_resolution_log.csv
Writes: ~/aias/osf/v11/data/phaseB_validation/<one-json-per-brand> + summary

Asana already validated in Phase A; not re-tested here.

Run:
    export SERPAPI_KEY="your_serpapi_key"
    python scripts/validate_acquisition_queries.py
"""
import csv
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

API_KEY = os.environ.get("SERPAPI_KEY")
if not API_KEY:
    sys.exit("ERROR: SERPAPI_KEY not set.")

CSV_PATH = Path.home() / "aias" / "osf" / "v11" / "data" / "topic_id_resolution_log.csv"
if not CSV_PATH.exists():
    sys.exit(f"ERROR: {CSV_PATH} not found.")

OUT_DIR = Path.home() / "aias" / "osf" / "v11" / "data" / "phaseB_validation"
OUT_DIR.mkdir(parents=True, exist_ok=True)

ENDPOINT = "https://serpapi.com/search"
VALIDATION_WINDOW = "2026-04-01 2026-04-07"  # out-of-sample, pre-analysis
fetched_at = datetime.now(timezone.utc).isoformat()

print(f"# Acquisition-query validation, fetched {fetched_at}")
print(f"# Validation window: {VALIDATION_WINDOW} (out-of-sample)")
print()

with CSV_PATH.open() as f:
    rows = list(csv.DictReader(f))

summary = []

for row in rows:
    brand = row["brand_canonical"]
    tier = row["final_query_tier"]
    query = row["acquisition_query"]

    # Asana was Phase A test; skip.
    if brand == "Asana":
        print(f"[skip] Asana - validated in Phase A")
        summary.append({"brand": brand, "tier": tier, "status": "SKIP_PHASE_A"})
        continue

    print(f"[{brand}] tier={tier}  q={query!r}")

    params = {
        "engine": "google_trends",
        "q": query,
        "data_type": "TIMESERIES",
        "date": VALIDATION_WINDOW,
        "geo": "",
        "no_cache": "true",
        "api_key": API_KEY,
    }

    try:
        response = requests.get(ENDPOINT, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"  ERROR: {e}")
        summary.append({"brand": brand, "tier": tier, "status": "API_ERROR", "error": str(e)})
        time.sleep(2)
        continue

    safe_brand = brand.replace(" ", "_")
    out_path = OUT_DIR / f"validation_{safe_brand}.json"
    out_path.write_text(json.dumps(data, indent=2))

    if "error" in data:
        print(f"  FAIL: API error: {data['error']}")
        summary.append({"brand": brand, "tier": tier, "status": "FAIL_API", "error": data["error"]})
        time.sleep(2)
        continue

    timeline = data.get("interest_over_time", {}).get("timeline_data", [])
    if not timeline:
        print(f"  FAIL: empty timeline")
        summary.append({"brand": brand, "tier": tier, "status": "FAIL_EMPTY"})
        time.sleep(2)
        continue

    values = []
    for p in timeline:
        if p.get("values"):
            try:
                values.append(int(p["values"][0]["extracted_value"]))
            except (KeyError, ValueError, TypeError):
                pass

    if not values:
        print(f"  FAIL: no extractable values")
        summary.append({"brand": brand, "tier": tier, "status": "FAIL_NO_VALUES"})
    elif all(v == 0 for v in values):
        print(f"  FAIL: all values zero (n={len(values)})")
        summary.append({"brand": brand, "tier": tier, "status": "FAIL_ALL_ZERO", "n_points": len(values)})
    elif len(set(values)) == 1:
        print(f"  WARN: all values identical = {values[0]}")
        summary.append({"brand": brand, "tier": tier, "status": "WARN_FLAT", "constant_value": values[0]})
    else:
        nonzero = sum(1 for v in values if v > 0)
        print(f"  PASS: n_pts={len(values)} nonzero={nonzero} range={min(values)}-{max(values)} mean={sum(values)/len(values):.1f}")
        summary.append({
            "brand": brand, "tier": tier, "status": "PASS",
            "n_points": len(values), "nonzero_points": nonzero,
            "min": min(values), "max": max(values),
            "mean": round(sum(values)/len(values), 1),
        })

    time.sleep(2)

# Write summary.
summary_path = OUT_DIR / f"validation_summary_{fetched_at.replace(':', '-')}.json"
summary_path.write_text(json.dumps({
    "fetched_at": fetched_at,
    "validation_window": VALIDATION_WINDOW,
    "results": summary,
}, indent=2))

# Counts.
print()
print("=" * 60)
print(f"# Validation summary")
print(f"# Window: {VALIDATION_WINDOW}")
print(f"# Saved: {summary_path}")
print()

by_status = {}
for s in summary:
    by_status.setdefault(s["status"], []).append(s["brand"])

for status, brands in sorted(by_status.items()):
    print(f"{status} ({len(brands)}): {', '.join(brands)}")

n_pass = len(by_status.get("PASS", []))
n_fail = sum(len(v) for k, v in by_status.items() if k.startswith("FAIL"))
n_warn = sum(len(v) for k, v in by_status.items() if k.startswith("WARN"))
n_skip = len(by_status.get("SKIP_PHASE_A", []))
print()
print(f"Total: {len(summary)}  PASS: {n_pass}  WARN: {n_warn}  FAIL: {n_fail}  SKIP: {n_skip}")
print()
print("# Done. Paste the validation summary above to Claude.")
