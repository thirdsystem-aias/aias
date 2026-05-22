"""Phase A - SerpAPI topic-ID pass-through verification.

Run:
    export SERPAPI_KEY="your_serpapi_key_here"
    python scripts/test_serpapi_topic.py
"""
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests

API_KEY = os.environ.get("SERPAPI_KEY")
if not API_KEY:
    sys.exit("ERROR: SERPAPI_KEY not set. Run: export SERPAPI_KEY=your_key")

# Asana topic mid, decoded from Trends URL.
# /m/0c3z_p8 = "Asana, Inc. - Software" entity.
ASANA_TOPIC_MID = "/m/0c3z_p8"

ENDPOINT = "https://serpapi.com/search"
params = {
    "engine": "google_trends",
    "q": ASANA_TOPIC_MID,
    "data_type": "TIMESERIES",
    "date": "2026-04-27 2026-05-10",  # spans both v0.11 wave windows
    "geo": "",  # worldwide
    "no_cache": "true",
    "api_key": API_KEY,
}

fetched_at = datetime.now(timezone.utc).isoformat()
print(f"Hitting SerpAPI at {fetched_at}...")
print(f"Topic mid: {ASANA_TOPIC_MID}")
print()

try:
    response = requests.get(ENDPOINT, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()
except requests.HTTPError as e:
    print(f"ERROR: HTTP {response.status_code}")
    try:
        print(f"Response body: {response.text[:500]}")
    except Exception:
        pass
    sys.exit(1)
except Exception as e:
    sys.exit(f"ERROR: API call failed: {e}")

# Capture raw response for the OSF deposit.
out_dir = Path.home() / "aias" / "osf" / "v11" / "data" / "phaseA_test"
out_dir.mkdir(parents=True, exist_ok=True)
safe_ts = fetched_at.replace(":", "-")
out_path = out_dir / f"asana_topic_test_{safe_ts}.json"
out_path.write_text(json.dumps(data, indent=2))
print(f"Raw response saved: {out_path}")
print()

if "error" in data:
    sys.exit(f"FAIL: SerpAPI returned error: {data['error']}")

if "interest_over_time" not in data:
    print(f"FAIL: 'interest_over_time' missing. Top-level keys: {list(data.keys())}")
    sys.exit(1)

timeline = data["interest_over_time"].get("timeline_data", [])
if not timeline:
    sys.exit("FAIL: timeline_data is empty")

search_params = data.get("search_parameters", {})
print(f"Engine echoed:    {search_params.get('engine')}")
print(f"Query echoed:     {search_params.get('q')}")
print(f"Data type:        {search_params.get('data_type')}")
print(f"Geo:              {search_params.get('geo') or '(worldwide)'}")
print(f"Timeline points:  {len(timeline)}")
print()

values = []
for p in timeline:
    if p.get("values"):
        try:
            values.append(int(p["values"][0]["extracted_value"]))
        except (KeyError, ValueError, TypeError):
            pass

if not values:
    sys.exit("FAIL: no extractable values in timeline")

print(f"First point: date={timeline[0].get('date')}, value={values[0]}")
print(f"Last point:  date={timeline[-1].get('date')}, value={values[-1]}")
print(f"Value range: min={min(values)}, max={max(values)}, mean={sum(values)/len(values):.1f}")
print()

if all(v == 0 for v in values):
    print("FAIL: all values are zero - topic mid may be treated as literal string.")
    sys.exit(1)
elif len(set(values)) == 1:
    print(f"WARN: all values identical ({values[0]}). Suspicious; investigate.")
    sys.exit(1)
else:
    print("PASS - SerpAPI accepts topic mid; daily timeseries returned.")
