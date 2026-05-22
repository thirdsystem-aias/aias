"""Phase B validation - Confirm each v0.12 acquisition query returns a
usable Trends timeseries against the out-of-sample window.

Methodology QA, not data analysis. Uses an OUT-OF-SAMPLE window
(April 1-7, 2026) that does NOT overlap with the v0.12 wave windows
(t1: Apr 27 - May 3; t2: May 4 - May 10). Wave-window data remains
untouched until post-pre-reg-lock acquisition.

Scope: olive oil + running shoes only. PM software queries are inherited
verbatim from v0.11 §5.2.1 and were validated at v0.11 lock; no
re-validation at v0.12.

Phase A pivots (California Olive Ranch, Asics) already verified; skipped.

Reads:  ~/aias/osf/v12/registries/topic_id_resolution_log_v0.12.csv
Writes: ~/aias/osf/v12/data/phaseB_validation/<one-json-per-brand> + summary

Forked from scripts/validate_acquisition_queries.py (v0.11).

Run:
    export SERPAPI_KEY="your_serpapi_key"
    python scripts/validate_acquisition_queries_v0.12.py
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

CSV_PATH = Path.home() / "aias" / "osf" / "v12" / "registries" / "topic_id_resolution_log_v0.12.csv"
if not CSV_PATH.exists():
    sys.exit(f"ERROR: {CSV_PATH} not found.\n"
             f"Fill in topic_id_resolution_log_v0.12.csv after running\n"
             f"fetch_topic_suggestions_v0.12.py, then re-run this script.")

OUT_DIR = Path.home() / "aias" / "osf" / "v12" / "data" / "phaseB_validation"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Phase A pivots — already verified, skip here.
PHASE_A_VALIDATED = {"California Olive Ranch", "Asics"}

ENDPOINT = "https://serpapi.com/search"
VALIDATION_WINDOW = "2026-04-01 2026-04-07"  # out-of-sample, pre-analysis
fetched_at = datetime.now(timezone.utc).isoformat()

print(f"# Acquisition-query validation v0.12, fetched {fetched_at}")
print(f"# Validation window: {VALIDATION_WINDOW} (out-of-sample)")
print(f"# CSV: {CSV_PATH}")
print()

with CSV_PATH.open() as f:
    rows = list(csv.DictReader(f))

summary = []

for row in rows:
    brand = row["brand_canonical"]
    tier = row["final_query_tier"]
    query = row["acquisition_query"]
    category = row.get("category", "")

    if brand in PHASE_A_VALIDATED:
        print(f"[skip] {brand} - validated in Phase A")
        summary.append({"brand": brand, "category": category, "tier": tier, "status": "SKIP_PHASE_A"})
        continue

    if not query or not query.strip():
        print(f"[skip] {brand} - acquisition_query empty (not yet resolved)")
        summary.append({"brand": brand, "category": category, "tier": tier, "status": "SKIP_UNRESOLVED"})
        continue

    print(f"[{brand}] cat={category} tier={tier}  q={query!r}")

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
        summary.append({"brand": brand, "category": category, "tier": tier,
                        "status": "API_ERROR", "error": str(e)})
        time.sleep(2)
        continue

    safe_brand = brand.replace(" ", "_").replace("/", "_")
    out_path = OUT_DIR / f"validation_{safe_brand}.json"
    out_path.write_text(json.dumps(data, indent=2, ensure_ascii=False))

    if "error" in data:
        print(f"  FAIL: API error: {data['error']}")
        summary.append({"brand": brand, "category": category, "tier": tier,
                        "status": "FAIL_API", "error": data["error"]})
        time.sleep(2)
        continue

    timeline = data.get("interest_over_time", {}).get("timeline_data", [])
    if not timeline:
        print(f"  FAIL: empty timeline")
        summary.append({"brand": brand, "category": category, "tier": tier, "status": "FAIL_EMPTY"})
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
        summary.append({"brand": brand, "category": category, "tier": tier,
                        "status": "FAIL_NO_VALUES"})
    elif all(v == 0 for v in values):
        print(f"  FAIL: all values zero (n={len(values)})")
        summary.append({"brand": brand, "category": category, "tier": tier,
                        "status": "FAIL_ALL_ZERO", "n_points": len(values)})
    elif len(set(values)) == 1:
        print(f"  WARN: all values identical = {values[0]}")
        summary.append({"brand": brand, "category": category, "tier": tier,
                        "status": "WARN_FLAT", "constant_value": values[0]})
    else:
        nonzero = sum(1 for v in values if v > 0)
        mean_val = sum(values) / len(values)
        print(f"  PASS: n_pts={len(values)} nonzero={nonzero} range={min(values)}-{max(values)} mean={mean_val:.1f}")
        summary.append({
            "brand": brand, "category": category, "tier": tier, "status": "PASS",
            "n_points": len(values), "nonzero_points": nonzero,
            "min": min(values), "max": max(values),
            "mean": round(mean_val, 1),
        })

    time.sleep(2)

# Summary
summary_path = OUT_DIR / f"validation_summary_{fetched_at.replace(':', '-')}.json"
summary_path.write_text(json.dumps({
    "fetched_at": fetched_at,
    "validation_window": VALIDATION_WINDOW,
    "csv_source": str(CSV_PATH),
    "phase_a_validated_skipped": sorted(PHASE_A_VALIDATED),
    "results": summary,
}, indent=2, ensure_ascii=False))

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
n_skip = sum(len(v) for k, v in by_status.items() if k.startswith("SKIP"))
print()
print(f"Total: {len(summary)}  PASS: {n_pass}  WARN: {n_warn}  FAIL: {n_fail}  SKIP: {n_skip}")
print()
print("# E1a triggers: brands with FAIL_ALL_ZERO, FAIL_EMPTY, FAIL_NO_VALUES, FAIL_API, or WARN_FLAT.")
print("# Update final_query_tier to 'EXCLUDED_E1a' in the CSV for any failure or warn brand,")
print("# document in the pre-reg deviations log, and re-commit before tagging v0.12-prereg.")
print()
print("# Done. Paste the validation summary above to Claude.")
