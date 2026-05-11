"""Phase B bundled-validation diagnostic for v0.12.

Replicates the pivot-rescaling acquisition methodology against the out-of-sample
window (2026-04-01 to 2026-04-07) for the 8 olive oil brands that returned
FAIL_API in solo validation. Confirms whether bundling with the California
Olive Ranch pivot surfaces signal (rescues to E5 with sparsity flag) or
returns ALL_ZERO (E1a-excluded).

Outcomes captured at lock per PRE_REGISTRATION.md §3.4a and §5.4 (E1a amendment).

Run:
    export SERPAPI_KEY="your_serpapi_key"
    python scripts/phaseB_bundled_validation_v0.12.py
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

PIVOT_MID = "/g/11cn92g97s"  # California Olive Ranch (Phase A pivot)
WINDOW = "2026-04-01 2026-04-07"

# Two bundles of 5 (pivot + 4 brands each) for the 8 solo-failed olive oil brands.
BUNDLES = [
    {
        "bundle_id": "bundle1",
        "brands": [
            ("Colonna", "Marina Colonna olive oil"),
            ("Frantoio Muraglia", "/g/11s888kbqf"),
            ("Frescobaldi Laudemio", "/g/11zb38xh15"),
            ("Lucini", "Lucini olive oil"),
        ],
    },
    {
        "bundle_id": "bundle2",
        "brands": [
            ("Manni", "Manni olive oil"),
            ("McEvoy Ranch", "/g/11rcbll42v"),
            ("Núñez de Prado", "/g/11g6qkzkv3"),
            ("Olio Verde", "Olio Verde Becchina"),
        ],
    },
]

OUT_DIR = Path.home() / "aias" / "osf" / "v12" / "data" / "phaseB_bundled"
OUT_DIR.mkdir(parents=True, exist_ok=True)
ENDPOINT = "https://serpapi.com/search"
fetched_at = datetime.now(timezone.utc).isoformat()

print(f"# Phase B bundled-validation diagnostic v0.12, fetched {fetched_at}")
print(f"# Pivot: California Olive Ranch ({PIVOT_MID})")
print(f"# Window: {WINDOW} (out-of-sample)")
print()

summary = []

for bundle in BUNDLES:
    bid = bundle["bundle_id"]
    bundle_brand_queries = bundle["brands"]
    queries = [PIVOT_MID] + [q for _, q in bundle_brand_queries]
    q_param = ",".join(queries)

    print(f"=== {bid}: California Olive Ranch + {', '.join(b for b, _ in bundle_brand_queries)} ===")

    params = {
        "engine": "google_trends",
        "q": q_param,
        "data_type": "TIMESERIES",
        "date": WINDOW,
        "geo": "",
        "no_cache": "true",
        "api_key": API_KEY,
    }

    try:
        response = requests.get(ENDPOINT, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"  BUNDLE FAIL: {e}")
        summary.append({"bundle_id": bid, "status": "API_ERROR", "error": str(e)})
        time.sleep(2)
        continue

    safe_ts = fetched_at.replace(":", "-")
    out_path = OUT_DIR / f"{bid}_{safe_ts}.json"
    out_path.write_text(json.dumps(data, indent=2, ensure_ascii=False))
    print(f"  Saved: {out_path.name}")

    if "error" in data:
        print(f"  BUNDLE FAIL: {data['error']}")
        summary.append({"bundle_id": bid, "status": "BUNDLE_FAIL", "error": data["error"]})
        time.sleep(2)
        continue

    timeline = data.get("interest_over_time", {}).get("timeline_data", [])
    if not timeline:
        print(f"  BUNDLE FAIL: empty timeline")
        summary.append({"bundle_id": bid, "status": "BUNDLE_EMPTY"})
        time.sleep(2)
        continue

    # Extract per-term timeseries
    series = {}
    for p in timeline:
        for v in p.get("values", []):
            series.setdefault(v.get("query", "?"), []).append(int(v.get("extracted_value", 0)))

    name_map = {PIVOT_MID: "California Olive Ranch (pivot)"}
    for brand, q in bundle_brand_queries:
        name_map[q] = brand

    print(f"  {'Term':35s}  mean   nz/n   range   disposition")
    for q, vals in series.items():
        name = name_map.get(q, q)
        nz = sum(1 for v in vals if v > 0)
        mn, mx = (min(vals), max(vals)) if vals else (0, 0)
        m = sum(vals) / len(vals) if vals else 0
        if all(v == 0 for v in vals):
            disp = "ALL_ZERO → E1a"
        elif nz < 4:
            disp = f"sparse ({nz}/7) → PASS_E5"
        else:
            disp = "PASS"
        print(f"  {name:35s}  {m:5.1f}  {nz}/{len(vals)}    {mn}-{mx}   {disp}")
        summary.append({
            "bundle_id": bid, "brand": name, "query": q,
            "mean": round(m, 1), "nonzero_days": nz, "total_days": len(vals),
            "min": mn, "max": mx, "disposition": disp,
        })

    time.sleep(2)
    print()

# Write summary
summary_path = OUT_DIR / f"bundled_summary_{fetched_at.replace(':', '-')}.json"
summary_path.write_text(json.dumps({
    "fetched_at": fetched_at,
    "pivot_mid": PIVOT_MID,
    "validation_window": WINDOW,
    "purpose": "Phase B bundled-validation diagnostic per PRE_REGISTRATION.md §3.4a and §5.4 E1a amendment",
    "results": summary,
}, indent=2, ensure_ascii=False))

print(f"# Summary saved: {summary_path}")
print("# Bundled-validation deposit complete. Proceed to git commit + tag.")
