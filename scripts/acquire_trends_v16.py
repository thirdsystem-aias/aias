"""v0.16 Trends acquisition (kitchen knives, fresh category).

Locked at v0.16-prereg (commit 511e339, 16 May 2026). Acquires Google Trends
data for the v0.16 kitchen knives panel at a single combined acquisition
window; per-wave slicing happens at rescale time (rescale_trends_v16.py).

v0.16 vs v0.15:
  - Substrate: premium tea -> kitchen knives (fresh category)
  - Pivot: Twinings -> Victorinox (chef-knife sub-category)
  - Bundle composition: 6 full bundles × 5 keywords (pivot + 4 brands)
    matching v0.13/v0.14/v0.15 bundle-size convention. No partial bundle.
  - Acquisition window: NEW (not carried forward from v0.15; v0.16 is a
    fresh category so cross-phase Trends comparability is not relevant).
    Pablo to confirm window at run; default below.

Bundle composition (6 bundles, 24 panel brands):
    Bundle 1 "japanese-1":     Shun, Global, Miyabi, Mac
    Bundle 2 "japanese-german": Tojiro, Yoshihiro, Wüsthof, Zwilling
    Bundle 3 "german-french":   Messermeister, Güde, Friedr. Dick, Sabatier
    Bundle 4 "french-american": Opinel, Laguiole, Nogent (Goyon-Chazeau), Cutco
    Bundle 5 "american":        Dalstrong, Misen, New West KnifeWorks, Made In
    Bundle 6 "chinese":         CCK Chan Chi Kee, Shibazi, Sunlong, ZHEN

Pivot: Victorinox (validated at Phase A; Swiss-Army-knife adjacency
    resolved per §4 5-stage; Wüsthof fallback if Victorinox fails §4
    per pre-reg §6).

Within-bundle balance principle (from v0.14 comment): bundles MIX
tradition cells where possible to prevent within-bundle Trends signal
homogeneity from biasing pivot normalization. Bundles 1 and 6 are
single-cell (Japanese-only, Chinese-only) — unavoidable given panel sizes.

Total: 6 bundles × 2 regions (worldwide + US) = 12 SerpAPI calls.

Reads queries from: ~/aias/osf/v16/registries/topic_id_resolution_log_v0.16.csv
    (produced by phaseB_resolve_v16.py; final_query_tier and
    acquisition_query columns must be populated before this script runs)

Pre-reg: v0.16-prereg (commit 511e339; corrected per DEVIATIONS Entry 2)

Run:
    export SERPAPI_KEY="your_serpapi_key"
    python3 ~/aias/scripts/acquire_trends_v16.py
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
# Configuration (locked at v0.16-prereg, commit 511e339)
# ============================================================================

API_KEY = os.environ.get("SERPAPI_KEY")
if not API_KEY:
    sys.exit("ERROR: SERPAPI_KEY not set. Run: export SERPAPI_KEY=your_key")

V16_ROOT = Path.home() / "aias" / "osf" / "v16"
CSV_PATH = V16_ROOT / "registries" / "topic_id_resolution_log_v0.16.csv"
RAW_ROOT = V16_ROOT / "data" / "trends_raw"
LOG_PATH = V16_ROOT / "data" / "trends_acquisition_log.csv"

RAW_ROOT.mkdir(parents=True, exist_ok=True)

if not CSV_PATH.exists():
    sys.exit(f"ERROR: locked CSV not found at {CSV_PATH}\n"
             f"Run phaseB_resolve_v16.py and commit before acquisition.")

ENDPOINT             = "https://serpapi.com/search"
SERPAPI_DELAY_SEC    = 3
MAX_RETRIES          = 3
RETRY_DELAY_SEC      = 5

# Acquisition window (TBD: Pablo confirms before run).
# v0.13/v0.14/v0.15 used 2026-04-27 to 2026-05-10 for tea cross-phase
# comparability. v0.16 is a fresh category; new window OK.
ACQUISITION_WINDOW = "2026-05-04 2026-05-17"   # TBD: confirm before run
REGIONS = [("worldwide", ""), ("US", "US")]

# Bundle composition — MUST mirror rescale_trends_v16.py exactly.
# 6 bundles × 5 keywords (pivot + 4 brands) = 6 SerpAPI calls per region.
PIVOT = "Victorinox"
BUNDLES = [
    {"id": 1, "label": "japanese-1",
     "members": ["Shun", "Global", "Miyabi", "Mac"]},
    {"id": 2, "label": "japanese-german",
     "members": ["Tojiro", "Yoshihiro", "Wüsthof", "Zwilling J.A. Henckels"]},
    {"id": 3, "label": "german-french",
     "members": ["Messermeister", "Güde", "Friedr. Dick", "Sabatier"]},
    {"id": 4, "label": "french-american",
     "members": ["Opinel", "Laguiole", "Nogent (Goyon-Chazeau)", "Cutco"]},
    {"id": 5, "label": "american",
     "members": ["Dalstrong", "Misen", "New West KnifeWorks", "Made In"]},
    {"id": 6, "label": "chinese",
     "members": ["CCK Chan Chi Kee", "Shibazi (Shi Ba Zi Zuo)", "Sunlong", "ZHEN"]},
]

CATEGORY = "kitchen_knives"

SESSION_TS = datetime.now(timezone.utc).isoformat()

# ============================================================================
# Read locked Phase B CSV — map brand -> acquisition_query
# ============================================================================

brand_to_query = {}
e1a_excluded = set()
not_activated = set()
pivot_found = False

with CSV_PATH.open() as f:
    for row in csv.DictReader(f):
        brand = row["brand_canonical"]
        tier = row["final_query_tier"]
        query = row["acquisition_query"]
        notes = row.get("notes", "")

        if brand == PIVOT and tier == "PIVOT":
            pivot_found = True
            brand_to_query[brand] = query or brand
            continue

        if tier == "EXCLUDED_E1a":
            e1a_excluded.add(brand)
            continue

        if "TESTED_NOT_ACTIVATED" in notes:
            not_activated.add(brand)
            continue

        if tier in ("PASS", "PASS_E5"):
            brand_to_query[brand] = query

if not pivot_found:
    sys.exit(f"ERROR: pivot {PIVOT!r} not found or not marked PIVOT in {CSV_PATH}.\n"
             f"Verify Phase A pivot validation completed and pivot row's "
             f"final_query_tier is set to PIVOT.")

print("=" * 72)
print(f"v0.16 acquire_trends — {CATEGORY}")
print(f"Pre-reg: v0.16-prereg (commit 511e339)")
print(f"Session timestamp: {SESSION_TS}")
print(f"Acquisition window: {ACQUISITION_WINDOW}")
print("=" * 72)
print()
print(f"Pivot: {PIVOT!r} -> {brand_to_query[PIVOT]!r}")
print(f"Eligible brands: {len(brand_to_query) - 1}")
print(f"E1a excluded: {len(e1a_excluded)} {sorted(e1a_excluded) if e1a_excluded else ''}")
print(f"Alternates not activated: {len(not_activated)}")
print()

# Verify all panel members are queryable
missing = []
for bundle in BUNDLES:
    for member in bundle["members"]:
        if member not in brand_to_query and member not in e1a_excluded:
            missing.append((bundle["id"], member))
if missing:
    print("WARNING: brands in bundles but not in Phase B output:")
    for bid, m in missing:
        print(f"  bundle {bid}: {m!r}")
    print("(These will be queried with bare canonical; check Phase B log)")
    print()


# ============================================================================
# SerpAPI helpers
# ============================================================================

def call_serpapi(query, geo, retries=MAX_RETRIES):
    params = {
        "engine":    "google_trends",
        "q":         query,
        "data_type": "TIMESERIES",
        "date":      ACQUISITION_WINDOW,
        "geo":       geo,
        "no_cache":  "true",
        "api_key":   API_KEY,
    }
    last_status, last_error = None, None
    for attempt in range(1, retries + 1):
        try:
            r = requests.get(ENDPOINT, params=params, timeout=60)
            last_status = r.status_code
            r.raise_for_status()
            data = r.json()
            if "error" in data:
                return data, last_status, data["error"], attempt
            return data, last_status, None, attempt
        except Exception as e:
            last_error = str(e)
            if attempt < retries:
                time.sleep(RETRY_DELAY_SEC)
    return None, last_status, last_error, retries


# ============================================================================
# Acquire bundles × regions
# ============================================================================

session_log = []
total_calls = 0
total_failures = 0

for region_name, geo in REGIONS:
    region_dir = RAW_ROOT / region_name
    region_dir.mkdir(parents=True, exist_ok=True)

    print(f"## Region: {region_name} ({geo or 'WORLDWIDE'})")
    print("-" * 72)

    for bundle in BUNDLES:
        bid = bundle["id"]
        label = bundle["label"]
        members = bundle["members"]

        # Build query: pivot + 4 brands, comma-separated
        query_terms = [brand_to_query[PIVOT]] + [
            brand_to_query.get(m, m) for m in members
        ]
        query_string = ",".join(query_terms)
        member_names = [PIVOT] + members

        out_path = region_dir / f"{CATEGORY}_bundle_{bid}_{SESSION_TS[:19].replace(':','-')}.json"

        # Pivot-anomaly check per v0.13 pre-reg §5.4 E2:
        # If pivot raw mean for this bundle deviates from Phase A baseline
        # by > 2 SD, log warning. Implementation: check after acquisition
        # via inspection of out_path; no per-call abort in this version.
        print(f"  bundle {bid} ({label}): {', '.join(member_names)}", end=" ... ", flush=True)
        data, http_status, error, n_attempts = call_serpapi(query_string, geo)

        rec = {
            "category":          CATEGORY,
            "bundle_id":         bid,
            "bundle_label":      label,
            "region":            region_name,
            "geo":               geo,
            "query_string":      query_string,
            "member_names":      member_names,
            "window":            ACQUISITION_WINDOW,
            "session_timestamp": SESSION_TS,
            "http_status":       http_status,
            "n_attempts":        n_attempts,
            "serpapi_error":     error,
            "interest_over_time": data.get("interest_over_time", {}) if data else {},
        }
        out_path.write_text(json.dumps(rec, indent=2, ensure_ascii=False))

        total_calls += 1
        status_label = "DONE" if data and not error else f"FAIL ({error})"
        if not data or error:
            total_failures += 1
        print(status_label)

        session_log.append({
            "session_timestamp": SESSION_TS,
            "region":            region_name,
            "bundle_id":         bid,
            "bundle_label":      label,
            "http_status":       http_status,
            "n_attempts":        n_attempts,
            "error":             error or "",
            "out_path":          str(out_path),
        })
        time.sleep(SERPAPI_DELAY_SEC)

    print()

# Write acquisition log
with LOG_PATH.open("w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=list(session_log[0].keys()))
    writer.writeheader()
    writer.writerows(session_log)

print("=" * 72)
print(f"Acquisition complete: {total_calls} calls, {total_failures} failures")
print(f"Raw JSONs: {RAW_ROOT}")
print(f"Acquisition log: {LOG_PATH}")
print()
print("Next: python3 ~/aias/scripts/rescale_trends_v16.py")
