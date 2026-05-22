"""v0.14 Phase A — Pivot validation for premium tea (Regime 4 third datapoint).

Per pre-reg §3 (pivot):
- Out-of-sample window: 2026-04-13 to 2026-04-19 (7 days; disjoint from t1/t2).
  Inherited from v0.13 protocol for cross-phase comparability.
- Region: Worldwide.
- Primary pivot: Twinings (premium tea).
- Fallback pivot: Fortnum & Mason (premium tea).
- PASS criteria: daily values mean >= 25 AND CV (sd/mean × 100) < 25%.
- Fallback is tested ONLY if the primary fails either criterion.
- Hard fail (both primary and fallback fail) routes the category to the
  literature-grounded pivot decision logged in DEVIATIONS.md.

NOTE — pre-reg lock workflow:
This Phase A runs AFTER v0.14 pre-reg lock (tag v0.14-prereg, commit b0ef30a).
The pre-reg explicitly names primary (Twinings) AND fallback (Fortnum & Mason)
in §3, so fallback activation is pre-registered. If both fail, that becomes
a DEVIATIONS entry citing the v0.13 protocol's literature-grounded routing.
This is a workflow deviation from v0.13 (which ran Phase A before pre-reg
lock); the substantive validation logic is unchanged.

Outputs:
    ~/aias/osf/v14/data/phaseA_test/{cat}_{role}_{pivot}_{ts}.json
    ~/aias/osf/v14/data/phaseA_summary.csv

Re-running is permitted (per-invocation timestamped outputs; nothing
overwritten). The summary CSV reflects the most recent run only.

Run:
    export SERPAPI_KEY="your_serpapi_key"
    python ~/aias/scripts/phaseA_validate_v14.py
"""
import csv
import json
import os
import statistics
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

# ============================================================================
# Configuration (locked at v0.14 pre-reg §3, tag v0.14-prereg)
# ============================================================================

API_KEY = os.environ.get("SERPAPI_KEY")
if not API_KEY:
    sys.exit("ERROR: SERPAPI_KEY not set. Run: export SERPAPI_KEY=your_key")

V14_ROOT    = Path.home() / "aias" / "osf" / "v14"
OUT_DIR     = V14_ROOT / "data" / "phaseA_test"
SUMMARY_CSV = V14_ROOT / "data" / "phaseA_summary.csv"
OUT_DIR.mkdir(parents=True, exist_ok=True)

ENDPOINT             = "https://serpapi.com/search"
WINDOW               = "2026-04-13 2026-04-19"
GEO                  = ""          # Worldwide
MAX_RETRIES          = 3           # per v0.12 sec.5.4 E4 convention
RETRY_DELAY_SEC      = 5
INTER_CALL_DELAY_SEC = 3
EXPECTED_N_DAYS      = 7

# PASS criteria per pre-reg §3 (inherited from v0.13 protocol)
MEAN_FLOOR     = 25.0
CV_CEILING_PCT = 25.0

# Pivot test plan. Order matters: primary first, fallback second per category.
PIVOTS = [
    ("premium_tea", "primary",  "Twinings",        "Twinings"),
    ("premium_tea", "fallback", "Fortnum & Mason", "Fortnum & Mason"),
]

# ============================================================================
# SerpAPI call (retry per v0.12 sec.5.4 E4)
# ============================================================================

def call_serpapi(query, geo):
    """Call SerpAPI google_trends TIMESERIES with retry.

    Returns (data, http_status, error, n_attempts).
    """
    params = {
        "engine":    "google_trends",
        "q":         query,
        "data_type": "TIMESERIES",
        "date":      WINDOW,
        "geo":       geo,
        "no_cache":  "true",
        "api_key":   API_KEY,
    }
    last_status = None
    last_error  = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            r = requests.get(ENDPOINT, params=params, timeout=60)
            last_status = r.status_code
            r.raise_for_status()
            data = r.json()
            if "error" in data:
                raise RuntimeError(f"SerpAPI error: {data['error']}")
            return data, last_status, None, attempt
        except Exception as e:
            last_error = str(e)
            if attempt < MAX_RETRIES:
                print(f"      Attempt {attempt} failed ({e}); "
                      f"retrying in {RETRY_DELAY_SEC}s")
                time.sleep(RETRY_DELAY_SEC)
            else:
                print(f"      Attempt {attempt} failed ({e}); no retries left")
    return None, last_status, last_error, MAX_RETRIES


# ============================================================================
# Per-pivot validation
# ============================================================================

def parse_serpapi_date(s):
    return datetime.strptime(s, "%b %d, %Y")


def sanitize_filename_part(s):
    """Sanitize a string for use in a filename (preserve readability).

    v0.14 addition: replaces '&' with 'and' to handle 'Fortnum & Mason'.
    """
    return s.replace(" ", "_").replace("&", "and")


def test_pivot(category, role, canonical, query):
    print(f"  Testing {category} {role}: {canonical!r}  (query: {query!r})")
    ts_utc = datetime.now(timezone.utc).isoformat()
    data, status, error, n_attempts = call_serpapi(query, GEO)

    result = {
        "pre_reg":          "v0.14-prereg",
        "pre_reg_section":  "§3",
        "category":         category,
        "pivot_role":       role,
        "pivot_canonical":  canonical,
        "query":            query,
        "geo":              GEO,
        "region_label":     "worldwide",
        "window":           WINDOW,
        "test_timestamp_utc": ts_utc,
        "n_attempts":       n_attempts,
        "http_status":      status,
        "criteria": {
            "mean_floor":     MEAN_FLOOR,
            "cv_ceiling_pct": CV_CEILING_PCT,
        },
    }

    if data is None:
        result.update({
            "phase_a_status": "FAIL_API",
            "error":          error,
            "daily_values":   [],
        })
        print(f"      FAIL_API: {error}")
        return result

    timeline = data.get("interest_over_time", {}).get("timeline_data", [])
    daily = []
    for point in timeline:
        date_str = point.get("date", "")
        try:
            d = parse_serpapi_date(date_str)
        except ValueError:
            continue
        vlist = point.get("values", [])
        if not vlist:
            continue
        try:
            v = int(vlist[0]["extracted_value"])
        except (KeyError, ValueError, TypeError):
            continue
        daily.append({"date": d.strftime("%Y-%m-%d"), "value": v})

    result["daily_values"] = daily
    result["n_days"]       = len(daily)

    if len(daily) < 2:
        result.update({
            "phase_a_status": "FAIL_INSUFFICIENT_DAYS",
            "error":          f"got {len(daily)} daily points; need >= 2 for sd",
        })
        print(f"      FAIL: {result['error']}")
        return result

    if len(daily) != EXPECTED_N_DAYS:
        print(f"      WARN: got {len(daily)} daily points, expected {EXPECTED_N_DAYS}")

    vals = [p["value"] for p in daily]
    mean = statistics.mean(vals)
    sd   = statistics.stdev(vals)
    cv_pct = (sd / mean * 100) if mean > 0 else float("inf")

    mean_pass = mean >= MEAN_FLOOR
    cv_pass   = cv_pct < CV_CEILING_PCT
    status_str = "PASS" if (mean_pass and cv_pass) else "FAIL_CRITERIA"

    result.update({
        "mean":   round(mean, 2),
        "sd":     round(sd, 2),
        "cv_pct": round(cv_pct, 2),
        "min":    min(vals),
        "max":    max(vals),
        "mean_pass": mean_pass,
        "cv_pass":   cv_pass,
        "phase_a_status": status_str,
    })

    print(f"      mean={mean:.2f} (floor {MEAN_FLOOR}: "
          f"{'PASS' if mean_pass else 'FAIL'})  "
          f"sd={sd:.2f}  CV={cv_pct:.2f}% "
          f"(ceiling {CV_CEILING_PCT}%: {'PASS' if cv_pass else 'FAIL'})")
    print(f"      -> {status_str}")
    return result


def write_pivot_json(result):
    ts_safe = result["test_timestamp_utc"].replace(":", "-")
    pivot_safe = sanitize_filename_part(result["pivot_canonical"])
    fname = f"{result['category']}_{result['pivot_role']}_{pivot_safe}_{ts_safe}.json"
    path = OUT_DIR / fname
    path.write_text(json.dumps(result, indent=2, ensure_ascii=False))
    return path


# ============================================================================
# Main: primary -> fallback routing per category
# ============================================================================

print("=" * 72)
print("v0.14 Phase A pivot validation")
print(f"Pre-reg §3 (tag v0.14-prereg, commit b0ef30a)")
print(f"Out-of-sample window {WINDOW}, region=Worldwide")
print(f"PASS criteria: mean >= {MEAN_FLOOR} AND CV < {CV_CEILING_PCT}%")
print("=" * 72)
print()

results = []
category_outcome = {}

# Preserve original ordering of categories from PIVOTS
categories_in_order = []
for cat, _, _, _ in PIVOTS:
    if cat not in categories_in_order:
        categories_in_order.append(cat)

for category in categories_in_order:
    print(f"### Category: {category}")

    primary  = next((p for p in PIVOTS if p[0] == category and p[1] == "primary"))
    fallback = next((p for p in PIVOTS if p[0] == category and p[1] == "fallback"), None)

    p_result = test_pivot(*primary)
    p_path = write_pivot_json(p_result)
    print(f"      Written: {p_path.name}")
    results.append(p_result)
    time.sleep(INTER_CALL_DELAY_SEC)

    if p_result["phase_a_status"] == "PASS":
        category_outcome[category] = {
            "selected_pivot":  primary[2],
            "selected_role":   "primary",
            "primary_status":  "PASS",
            "fallback_status": "NOT_TESTED",
        }
        print(f"  -> Category pivot locked: {primary[2]} (primary PASS)")
        print()
        continue

    print(f"  Primary did not PASS ({p_result['phase_a_status']}) — testing fallback")
    if fallback is None:
        category_outcome[category] = {
            "selected_pivot":  None,
            "selected_role":   None,
            "primary_status":  p_result["phase_a_status"],
            "fallback_status": "NONE_DEFINED",
        }
        print(f"  -> Category HARD FAIL: no fallback defined")
        print()
        continue

    f_result = test_pivot(*fallback)
    f_path = write_pivot_json(f_result)
    print(f"      Written: {f_path.name}")
    results.append(f_result)
    time.sleep(INTER_CALL_DELAY_SEC)

    if f_result["phase_a_status"] == "PASS":
        category_outcome[category] = {
            "selected_pivot":  fallback[2],
            "selected_role":   "fallback",
            "primary_status":  p_result["phase_a_status"],
            "fallback_status": "PASS",
        }
        print(f"  -> Category pivot locked: {fallback[2]} (fallback PASS)")
    else:
        category_outcome[category] = {
            "selected_pivot":  None,
            "selected_role":   None,
            "primary_status":  p_result["phase_a_status"],
            "fallback_status": f_result["phase_a_status"],
        }
        print(f"  -> Category HARD FAIL: both primary and fallback failed; "
              f"per v0.13 protocol default to literature-grounded pivot in DEVIATIONS.md")
    print()


# ============================================================================
# Summary CSV
# ============================================================================

with SUMMARY_CSV.open("w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "category", "pivot_role", "pivot_canonical", "query",
        "test_timestamp_utc", "n_days", "mean", "sd", "cv_pct",
        "min", "max", "mean_pass", "cv_pass", "phase_a_status",
    ])
    writer.writeheader()
    for r in results:
        writer.writerow({
            "category":           r["category"],
            "pivot_role":         r["pivot_role"],
            "pivot_canonical":    r["pivot_canonical"],
            "query":              r["query"],
            "test_timestamp_utc": r["test_timestamp_utc"],
            "n_days":             r.get("n_days", 0),
            "mean":               r.get("mean", ""),
            "sd":                 r.get("sd", ""),
            "cv_pct":             r.get("cv_pct", ""),
            "min":                r.get("min", ""),
            "max":                r.get("max", ""),
            "mean_pass":          r.get("mean_pass", ""),
            "cv_pass":            r.get("cv_pass", ""),
            "phase_a_status":     r["phase_a_status"],
        })

print("=" * 72)
print("Phase A complete.")
print(f"Summary CSV:    {SUMMARY_CSV}")
print(f"Per-pivot JSONs: {OUT_DIR}")
print()
print("Outcome per category:")
print("-" * 72)
for category, outcome in category_outcome.items():
    if outcome["selected_pivot"]:
        print(f"  {category:<12}  PASS  -> pivot = {outcome['selected_pivot']} "
              f"({outcome['selected_role']}; "
              f"primary={outcome['primary_status']}, "
              f"fallback={outcome['fallback_status']})")
    else:
        print(f"  {category:<12}  HARD FAIL  "
              f"(primary={outcome['primary_status']}, "
              f"fallback={outcome['fallback_status']})")
print()

n_hard_fail = sum(1 for o in category_outcome.values() if o["selected_pivot"] is None)
if n_hard_fail > 0:
    print(f"WARNING: {n_hard_fail} category/categories have no validated pivot.")
    print("Document hard fails in osf/v14/DEVIATIONS.md before proceeding to acquisition.")
    sys.exit(1)
else:
    print("All categories have a validated pivot. Next steps:")
    print("  1. If fallback was activated, log activation in osf/v14/DEVIATIONS.md")
    print("  2. Commit: git add osf/v14/data/phaseA_*")
    print("  3. Run fresh-acquisition session for premium tea panel.")
