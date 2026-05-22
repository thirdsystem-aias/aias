"""Phase B validation - Single-brand retry for Shortcut.

Hits SerpAPI once with the locked T3 compound query for Shortcut against
the same out-of-sample validation window used in the batch run.

Run:
    python scripts/validate_shortcut.py
"""
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

ENDPOINT = "https://serpapi.com/search"
QUERY = "shortcut project management"
WINDOW = "2026-04-01 2026-04-07"

params = {
    "engine": "google_trends",
    "q": QUERY,
    "data_type": "TIMESERIES",
    "date": WINDOW,
    "geo": "",
    "no_cache": "true",
    "api_key": API_KEY,
}

fetched_at = datetime.now(timezone.utc).isoformat()
print(f"# Shortcut retry, fetched {fetched_at}")
print(f"# q = {QUERY!r}, window = {WINDOW}")
print()

try:
    response = requests.get(ENDPOINT, params=params, timeout=30)
    print(f"HTTP status: {response.status_code}")
    response.raise_for_status()
    data = response.json()
except requests.HTTPError:
    print(f"HTTPError. Body: {response.text[:500]}")
    sys.exit(1)
except Exception as e:
    print(f"ERROR: {type(e).__name__}: {e}")
    sys.exit(1)

out_dir = Path.home() / "aias" / "osf" / "v11" / "data" / "phaseB_validation"
out_dir.mkdir(parents=True, exist_ok=True)
out_path = out_dir / "validation_Shortcut.json"
out_path.write_text(json.dumps(data, indent=2))
print(f"Saved: {out_path}")
print()

if "error" in data:
    print(f"FAIL: API error: {data['error']}")
    sys.exit(1)

timeline = data.get("interest_over_time", {}).get("timeline_data", [])
if not timeline:
    print("FAIL: empty timeline")
    sys.exit(1)

values = []
for p in timeline:
    if p.get("values"):
        try:
            values.append(int(p["values"][0]["extracted_value"]))
        except (KeyError, ValueError, TypeError):
            pass

if not values:
    print("FAIL: no extractable values")
elif all(v == 0 for v in values):
    print(f"FAIL: all values zero (n={len(values)}). Compound query has no signal.")
elif len(set(values)) == 1:
    print(f"WARN: all values identical = {values[0]}")
else:
    nonzero = sum(1 for v in values if v > 0)
    print(f"PASS: n_pts={len(values)} nonzero={nonzero} range={min(values)}-{max(values)} mean={sum(values)/len(values):.1f}")
