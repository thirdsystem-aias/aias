"""v0.13 Trends acquisition (fresh-acquisition arm only).

Locked at v0.13-prereg. Acquires Google Trends data for the two NEW categories
under v0.13: premium facial skincare (8 bundles) and personal finance apps
(4 bundles), at the same wave windows v0.12 used. The reuse-arm categories
(PM software, running shoes, olive oil) are not acquired here; their v0.12
trends_processed CSVs are loaded directly at the scoring stage per pre-reg §5.3.

Single combined window 2026-04-27 to 2026-05-10 spans both t1 and t2 wave
windows; per-wave slicing happens at scoring (rescale_trends_v13.py mirrors
v0.12's rescale step). Back-fill design per pre-reg §5.3: the windows are now
historical, but SerpAPI returns historical daily values identically; the
disclosure is in the v0.13 manuscript and DEVIATIONS.md if material.

Bundle composition per pre-reg §5.2:
    skincare:  8 bundles, pivot CeraVe (Phase A validated mean 89.43, CV 7.77%)
    finance:   4 bundles, pivot YNAB    (Phase A validated mean 82.00, CV 13.51%)
Total: 12 bundles × 2 regions = 24 SerpAPI calls in a single locked session.

Padding (per pre-reg §5.2 + DEVIATIONS.md v0.12 Entry 1 lesson):
    Padding slots are filled with incumbent-tier brand canonicals from the
    same category registry — NOT category-generic terms. The padding brand's
    query is looked up from the same CSV the canonical entries use, so any
    Phase B topic-ID resolution flows through to padding queries verbatim.

Padding choices (see DEVIATIONS.md v0.13 Entry 2 if these change post-Phase-B):
    skincare B8: Cetaphil + Neutrogena  (highest-volume mass-market incumbents;
                                         scale anchors for Glossier and
                                         Beauty of Joseon measurements)
    finance B4:  Empower                 (incumbent-tier; selected over Mint
                                         to avoid phantom-brand interaction,
                                         over NerdWallet for within-week
                                         volume stability)

Pivot-anomaly check per pre-reg sec.5.4 E2.
API-failure retry per pre-reg sec.5.4 E4 (up to 3 attempts).

Reads queries from: ~/aias/osf/v13/registries/topic_id_resolution_log_v0.13.csv
    (produced by Phase B; must exist and be committed at v0.13-prereg before
    this script runs)

Run:
    export SERPAPI_KEY="your_serpapi_key"
    python3 ~/aias/scripts/acquire_trends_v13.py
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
# Configuration (locked at v0.13-prereg)
# ============================================================================

API_KEY = os.environ.get("SERPAPI_KEY")
if not API_KEY:
    sys.exit("ERROR: SERPAPI_KEY not set. Run: export SERPAPI_KEY=your_key")

V13_ROOT = Path.home() / "aias" / "osf" / "v13"
CSV_PATH = V13_ROOT / "registries" / "topic_id_resolution_log_v0.13.csv"
RAW_ROOT = V13_ROOT / "data" / "trends_raw"
LOG_PATH = V13_ROOT / "data" / "trends_acquisition_log.csv"

if not CSV_PATH.exists():
    sys.exit(f"ERROR: locked CSV not found at {CSV_PATH}\n"
             f"Run Phase B and commit the topic-ID resolution log before "
             f"acquisition.")

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
print(f"# Brands E1a-excluded: {len(e1a_excluded)} "
      f"({', '.join(sorted(e1a_excluded)) if e1a_excluded else '(none)'})")
print()

# ============================================================================
# Bundle structure (locked composition per category, per pre-reg §5.2)
# ============================================================================

# Pivot canonical per category. Pivot query is looked up from CSV at runtime
# so any Phase B topic-ID resolution flows through.
PIVOT_CANONICALS = {
    "skincare": "CeraVe",  # Phase A primary; bare query per DEVIATIONS.md v0.13 Entry 1
    "finance":  "YNAB",    # Phase A primary; bare query per DEVIATIONS.md v0.13 Entry 1
}

# Padding members per pre-reg §5.2 incumbent-tier brand-volume-comparable rule.
# Each tuple is (display_name, brand_canonical_to_lookup). The display_name
# is namespaced with `__pad_` for clarity in logs and to be skipped by
# rescale_trends_v13.py per is_padding flag. The brand_canonical_to_lookup
# is resolved against brand_to_query at resolve_member() time.
PAD_SKIN_CETAPHIL    = ("__pad_Cetaphil",    "Cetaphil")
PAD_SKIN_NEUTROGENA  = ("__pad_Neutrogena",  "Neutrogena")
PAD_FIN_EMPOWER      = ("__pad_Empower",     "Empower")
PAD_FIN_NERDWALLET   = ("__pad_NerdWallet",  "NerdWallet")

# Bundle definitions. Each member is either:
#   - a brand canonical (string) -> canonical entry, query looked up from CSV
#   - a (display, brand_canonical) tuple -> padding entry, query looked up from CSV
# Pivot is prepended at runtime (not in members list).
BUNDLE_DEFS = {
    "skincare": [
        {"id": 1, "label": "skin-incumbents-I",
         "members": ["Cetaphil", "Neutrogena", "La Roche-Posay", "Vanicream"]},
        {"id": 2, "label": "skin-incumbents-mid-I",
         "members": ["Skinceuticals", "Eucerin", "Paula's Choice", "Drunk Elephant"]},
        {"id": 3, "label": "skin-mid-tier-I",
         "members": ["Tatcha", "The Ordinary", "EltaMD", "Bioderma"]},
        {"id": 4, "label": "skin-mid-tier-II",
         "members": ["Avène", "Aveeno", "First Aid Beauty", "Augustinus Bader"]},
        {"id": 5, "label": "skin-challengers-luxury-I",
         "members": ["Youth to the People", "La Mer", "Estée Lauder", "Lancôme"]},
        {"id": 6, "label": "skin-challengers-luxury-II",
         "members": ["Clinique", "Kiehl's", "Sunday Riley", "SK-II"]},
        {"id": 7, "label": "skin-challengers-III",
         "members": ["Olay", "Origins", "Dermalogica", "Murad"]},
        {"id": 8, "label": "skin-remainder-padding",
         "members": ["Glossier", "Beauty of Joseon",
                     PAD_SKIN_CETAPHIL, PAD_SKIN_NEUTROGENA]},
    ],
    "finance": [
        {"id": 1, "label": "fin-incumbents",
         "members": ["Mint", "Quicken", "Empower", "NerdWallet"]},
        {"id": 2, "label": "fin-incumbents-mid",
         "members": ["Rocket Money", "PocketGuard", "Goodbudget",
                     PAD_FIN_NERDWALLET]},
        {"id": 3, "label": "fin-mid-tier-challengers",
         "members": ["EveryDollar", "Monarch Money", "Copilot", "Lunch Money"]},
        {"id": 4, "label": "fin-challengers-padding",
         "members": ["Origin", "Cleo", "Tiller", PAD_FIN_EMPOWER]},
    ],
}

REGIONS = [
    ("worldwide", ""),     # geo="" = worldwide; primary per pre-reg §6
    ("US",        "US"),   # sensitivity per pre-reg §13
]

ENDPOINT = "https://serpapi.com/search"
WINDOW = "2026-04-27 2026-05-10"   # combined t1 + t2 window per pre-reg §6
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
    """Resolve a bundle member to (display_name, query, is_padding).

    String member: canonical brand entry; query looked up from CSV.
    Tuple member: (display, brand_canonical) padding entry; query looked up
                  from CSV via the brand_canonical (v0.13 padding rule —
                  see DEVIATIONS.md v0.12 Entry 1 for the prior generic-
                  padding pattern's failure mode).
    """
    if isinstance(m, tuple):
        display, brand_ref = m
        if brand_ref not in brand_to_query:
            sys.exit(f"ERROR: padding {display!r} refers to brand "
                     f"{brand_ref!r} but no query found in CSV. "
                     f"Check E1a status or registry.")
        return display, brand_to_query[brand_ref], True
    elif isinstance(m, str):
        if m not in brand_to_query:
            sys.exit(f"ERROR: bundle references brand {m!r} but no query "
                     f"found in CSV. Check E1a status or registry.")
        return m, brand_to_query[m], False
    else:
        sys.exit(f"ERROR: bundle member type {type(m)} not supported.")


# Resolve pivot queries from CSV at runtime
PIVOTS = {}
for category, canonical in PIVOT_CANONICALS.items():
    if canonical not in brand_to_query:
        sys.exit(f"ERROR: pivot {canonical!r} for category {category!r} "
                 f"not found in CSV. Phase A validated this pivot; Phase B "
                 f"must have produced its acquisition_query.")
    PIVOTS[category] = (canonical, brand_to_query[canonical])

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
        n_padding = sum(1 for m in members_resolved if m[2])
        print(f"  Bundle {bundle['id']} ({bundle['label']}):")
        print(f"    Members: {', '.join(names)}")
        if n_padding > 0:
            print(f"    Padding slots: {n_padding}")
    print()

# Final tally
total_brand_slots = 0
total_padding_slots = 0
for category, bundles in BUNDLE_DEFS.items():
    for bundle in bundles:
        for m in bundle["members"]:
            _, _, is_pad = resolve_member(m)
            if is_pad:
                total_padding_slots += 1
            else:
                total_brand_slots += 1
print(f"# Unique non-pivot brand acquisitions: {total_brand_slots} "
      f"(excl. pivots in each bundle)")
print(f"# Brand-as-padding slots: {total_padding_slots}")
print(f"# Brands in CSV not E1a: {len(brand_to_query)}")
n_bundles = sum(len(b) for b in BUNDLE_DEFS.values())
n_calls = n_bundles * len(REGIONS)
print(f"# Bundles: {n_bundles} x Regions: {len(REGIONS)} = {n_calls} SerpAPI calls")
print()

# ============================================================================
# Acquisition
# ============================================================================

print("=" * 72)
print(f"v0.13 Trends acquisition (fresh-acquisition arm)")
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
    print("Next: python3 ~/aias/scripts/rescale_trends_v13.py")
