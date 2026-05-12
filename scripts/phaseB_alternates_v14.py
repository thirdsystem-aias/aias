"""v0.14 Phase B alternates — Chinese-cell alternate activation per pre-reg §2.

Triggered when Chinese-cell EXCLUDED_E1a count >= 2 from main Phase B run.
Tests the 3 pre-registered alternates from brands_premium_tea.json:
    A1. Wang De Chuan / 王德傳 — 1862
    A2. In Pursuit of Tea — 2002
    A3. Yunnan Sourcing — 2004

Per pre-reg §2: "alternates are activated in order until the cell returns to
four eligible brands". This script tests all 3 alternates through the same
Phase B pipeline (Stage 1 pytrends audit, Stage 2 bare canonical solo per
DEVIATIONS Entry 1, Stage 3 E5 if needed), then applies the activation rule:
the first N alternates that PASS or PASS_E5, taken in pre-reg order, are
"ACTIVATED" up to the gap-fill count. Any remaining alternates that pass
are recorded as "TESTED_NOT_ACTIVATED" — their data exists but is not used
in primary analysis. Alternates that fail are recorded as EXCLUDED_E1a.

This script reads the existing topic_id_resolution_log_v0.14.csv to determine
the Chinese-cell gap, then APPENDS new rows for the tested alternates with
the `notes` column reflecting activation status.

Outputs:
    ~/aias/osf/v14/data/phaseB_suggestions/{alternate}.json
    ~/aias/osf/v14/data/phaseB_validation/solo/{alternate}.json
    ~/aias/osf/v14/data/phaseB_validation/bundled/*.json  (if E5 triggered)
    ~/aias/osf/v14/registries/topic_id_resolution_log_v0.14.csv  (appended)

DEVIATIONS Entry 2 records the activation outcome.

Run:
    export SERPAPI_KEY="..."
    python3 ~/aias/scripts/phaseB_alternates_v14.py
"""
import csv
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

try:
    from pytrends.request import TrendReq
    HAVE_PYTRENDS = True
except ImportError:
    HAVE_PYTRENDS = False

# ============================================================================
# Configuration
# ============================================================================

API_KEY = os.environ.get("SERPAPI_KEY")
if not API_KEY:
    sys.exit("ERROR: SERPAPI_KEY not set. Run: export SERPAPI_KEY=your_key")

if not HAVE_PYTRENDS:
    sys.exit("ERROR: pytrends not installed.")

V14_ROOT      = Path.home() / "aias" / "osf" / "v14"
REGISTRY_TEA  = V14_ROOT / "registries" / "brands_premium_tea.json"
SUGGEST_DIR   = V14_ROOT / "data" / "phaseB_suggestions"
SOLO_DIR      = V14_ROOT / "data" / "phaseB_validation" / "solo"
BUNDLED_DIR   = V14_ROOT / "data" / "phaseB_validation" / "bundled"
OUT_CSV       = V14_ROOT / "registries" / "topic_id_resolution_log_v0.14.csv"

for d in (SUGGEST_DIR, SOLO_DIR, BUNDLED_DIR):
    d.mkdir(parents=True, exist_ok=True)

for f in (REGISTRY_TEA, OUT_CSV):
    if not f.exists():
        sys.exit(f"ERROR: required file not found at {f}")

WINDOW = "2026-04-13 2026-04-19"
GEO    = ""

ENDPOINT             = "https://serpapi.com/search"
SERPAPI_DELAY_SEC    = 3
PYTRENDS_DELAY_SEC   = 5
MAX_RETRIES          = 3
RETRY_DELAY_SEC      = 5

CATEGORY_TYPE_KEYWORDS = {
    "premium_tea": ["tea", "brand", "beverage", "drink", "food", "company",
                    "specialty", "retail", "store"],
}

PIVOT_CANONICAL = "Twinings"
TARGET_CHINESE_ELIGIBLE = 4

SESSION_TS = datetime.now(timezone.utc).isoformat()


# ============================================================================
# Helpers (mirrored from phaseB_resolve_v14.py)
# ============================================================================

def safe_name(name):
    s = re.sub(r"[^a-zA-Z0-9_-]", "_", name)
    return re.sub(r"_+", "_", s).strip("_")


def call_serpapi(query, geo=GEO, retries=MAX_RETRIES):
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


def parse_solo_timeline(data):
    if data is None:
        return {"daily": [], "n_days": 0, "max": None, "mean": None,
                "all_zero": True, "parse_error": "data is None"}
    timeline = data.get("interest_over_time", {}).get("timeline_data", [])
    daily = []
    for point in timeline:
        date_str = point.get("date", "")
        vlist = point.get("values", [])
        if not vlist:
            continue
        try:
            v = int(vlist[0]["extracted_value"])
        except (KeyError, ValueError, TypeError):
            continue
        daily.append({"date": date_str, "value": v})
    if not daily:
        return {"daily": [], "n_days": 0, "max": None, "mean": None,
                "all_zero": True, "parse_error": "no daily points"}
    vals = [p["value"] for p in daily]
    return {
        "daily":    daily,
        "n_days":   len(daily),
        "max":      max(vals),
        "mean":     round(sum(vals) / len(vals), 2),
        "all_zero": all(v == 0 for v in vals),
    }


def parse_bundle_timeline(data, n_slots):
    if data is None:
        return [{"slot": i, "daily": [], "max": None, "mean": None,
                 "all_zero": True} for i in range(n_slots)]
    timeline = data.get("interest_over_time", {}).get("timeline_data", [])
    per_slot = [[] for _ in range(n_slots)]
    for point in timeline:
        vlist = point.get("values", [])
        for i in range(min(len(vlist), n_slots)):
            try:
                v = int(vlist[i]["extracted_value"])
                per_slot[i].append(v)
            except (KeyError, ValueError, TypeError):
                pass
    result = []
    for i, vals in enumerate(per_slot):
        if not vals:
            result.append({"slot": i, "daily": [], "max": None, "mean": None,
                           "all_zero": True})
        else:
            result.append({
                "slot":     i,
                "daily":    vals,
                "max":      max(vals),
                "mean":     round(sum(vals) / len(vals), 2),
                "all_zero": all(v == 0 for v in vals),
            })
    return result


def pick_best_suggestion(brand, suggestions, category):
    if not suggestions:
        return {"mid": "", "title": "", "type": "",
                "rationale": "pytrends returned no suggestions"}
    keywords = CATEGORY_TYPE_KEYWORDS.get(category, [])
    for s in suggestions:
        type_lower = (s.get("type") or "").lower()
        if any(kw in type_lower for kw in keywords):
            return {
                "mid":       s.get("mid", ""),
                "title":     s.get("title", ""),
                "type":      s.get("type", ""),
                "rationale": (f"type={s.get('type')!r} matches category "
                              f"keyword set (audit only; not used as query)"),
            }
    s = suggestions[0]
    return {
        "mid":       s.get("mid", ""),
        "title":     s.get("title", ""),
        "type":      s.get("type", ""),
        "rationale": (f"no category-keyword match; defaulted to first "
                      f"suggestion (type={s.get('type')!r}; audit only)"),
    }


# ============================================================================
# Stage 0: Determine Chinese-cell gap from existing CSV
# ============================================================================

with OUT_CSV.open() as f:
    existing_rows = list(csv.DictReader(f))

chinese_primary_eligible = sum(
    1 for r in existing_rows
    if r["tier_in_registry"] == "chinese"
    and r["final_query_tier"] in ("PASS", "PASS_E5")
)
chinese_gap = TARGET_CHINESE_ELIGIBLE - chinese_primary_eligible

print("=" * 72)
print("v0.14 Phase B alternates — Chinese-cell alternate activation")
print(f"Session timestamp: {SESSION_TS}")
print(f"Pre-reg: §2 (activation rule), commit b0ef30a")
print("=" * 72)
print()
print(f"Chinese primary cell eligible: {chinese_primary_eligible}")
print(f"Target eligible: {TARGET_CHINESE_ELIGIBLE}")
print(f"Gap to fill: {chinese_gap}")
print()

if chinese_gap <= 0:
    print("Chinese cell already at or above target. No activation needed.")
    sys.exit(0)

# ============================================================================
# Stage 0.5: Load alternates from registry, preserve pre-reg activation order
# ============================================================================

reg = json.loads(REGISTRY_TEA.read_text())
alternates_raw = reg.get("alternates", [])
if not alternates_raw:
    sys.exit("ERROR: no `alternates` array in brands_premium_tea.json")

alternates = []
for a in sorted(alternates_raw, key=lambda x: x["activation_order"]):
    alternates.append({
        "canonical":          a["brand"],
        "category":           reg.get("category", "premium_tea"),
        "tier_in_registry":   a.get("tradition", "chinese"),
        "aliases":            a.get("aliases", []),
        "activation_order":   a["activation_order"],
    })

print(f"Alternates loaded (in pre-reg activation order):")
for a in alternates:
    print(f"  A{a['activation_order']}. {a['canonical']}")
print()

# ============================================================================
# Stage 1: pytrends.suggestions() per alternate (audit trail only)
# ============================================================================

print("=" * 72)
print("STAGE 1 — pytrends.suggestions() per alternate (audit trail only)")
print("=" * 72)

pytrends = TrendReq(hl="en-US", tz=0, timeout=(10, 25))

for b in alternates:
    suggest_path = SUGGEST_DIR / f"{safe_name(b['canonical'])}.json"
    if suggest_path.exists():
        rec = json.loads(suggest_path.read_text())
        b["suggestions"] = rec["suggestions"]
        b["chosen"]      = rec.get("chosen", {})
        print(f"  pytrends: {b['canonical']!r} (cached)")
        continue

    print(f"  pytrends: {b['canonical']!r}", end=" ... ", flush=True)
    try:
        suggestions = pytrends.suggestions(keyword=b["canonical"])
        suggestions = [s for s in suggestions if s.get("type") not in (None, "")]
        b["suggestions"] = suggestions
        b["chosen"] = pick_best_suggestion(b["canonical"], suggestions, b["category"])
        print(f"{len(suggestions)} suggestions; "
              f"audit-chose: {b['chosen'].get('title') or '(none)'} "
              f"[{b['chosen'].get('type') or 'n/a'}]")
    except Exception as e:
        print(f"FAILED ({e})")
        b["suggestions"] = []
        b["chosen"] = {"mid": "", "title": "", "type": "",
                       "rationale": f"pytrends exception: {e}"}

    suggest_path.write_text(json.dumps({
        "brand_canonical":     b["canonical"],
        "category":            b["category"],
        "tier_in_registry":    b["tier_in_registry"],
        "pytrends_timestamp":  datetime.now(timezone.utc).isoformat(),
        "suggestions":         b["suggestions"],
        "chosen":              b["chosen"],
        "note": ("DEVIATIONS Entry 1: 'chosen' field is audit only; "
                 "solo_query uses bare canonical brand name. "
                 "Pre-reg §2 alternate."),
    }, indent=2, ensure_ascii=False))

    time.sleep(PYTRENDS_DELAY_SEC)
print()

# ============================================================================
# Stage 2: Solo SerpAPI validation per alternate (bare canonical)
# ============================================================================

print("=" * 72)
print("STAGE 2 — solo SerpAPI validation (bare canonical per DEVIATIONS Entry 1)")
print("=" * 72)

for b in alternates:
    candidate = b["canonical"]
    b["solo_query"] = candidate

    solo_path = SOLO_DIR / f"{safe_name(b['canonical'])}.json"
    if solo_path.exists():
        rec = json.loads(solo_path.read_text())
        b["solo_result"] = rec["serpapi_result"]
        b["solo_status"] = rec["solo_status"]
        print(f"  solo: {b['canonical']!r} (cached, status={b['solo_status']})")
        continue

    print(f"  solo: {b['canonical']!r} (q={candidate!r})", end=" ... ", flush=True)
    data, http_status, error, n_attempts = call_serpapi(candidate)
    parsed = parse_solo_timeline(data)

    if data is None:
        solo_status = "FAIL_API"
    elif error is not None:
        if any(s in error.lower() for s in ("no results", "not enough", "noresults")):
            solo_status = "FAIL_NO_SIGNAL"
        else:
            solo_status = "FAIL_API"
    elif parsed["all_zero"]:
        solo_status = "FAIL_NO_SIGNAL"
    else:
        solo_status = "PASS"

    rec = {
        "brand_canonical":   b["canonical"],
        "category":          b["category"],
        "query":             candidate,
        "query_source":      "bare_canonical_per_DEVIATIONS_Entry_1",
        "window":            WINDOW,
        "geo":               GEO,
        "test_timestamp":    datetime.now(timezone.utc).isoformat(),
        "http_status":       http_status,
        "n_attempts":        n_attempts,
        "serpapi_error":     error,
        "serpapi_result":    parsed,
        "solo_status":       solo_status,
        "is_alternate":      True,
        "activation_order":  b["activation_order"],
    }
    solo_path.write_text(json.dumps(rec, indent=2, ensure_ascii=False))

    b["solo_result"] = parsed
    b["solo_status"] = solo_status

    if solo_status == "PASS":
        print(f"PASS (mean={parsed['mean']}, max={parsed['max']})")
    else:
        print(f"{solo_status} ({error or 'all-zero / empty timeline'})")
    time.sleep(SERPAPI_DELAY_SEC)
print()

# ============================================================================
# Stage 3: E5 bundled rescue for solo-FAILed alternates
# ============================================================================

e5_alternates = [b for b in alternates
                 if b.get("solo_status", "").startswith("FAIL")]

if e5_alternates:
    print("=" * 72)
    print("STAGE 3 — E5 bundled rescue (bare canonical)")
    print("=" * 72)

    pivot_q = PIVOT_CANONICAL
    member_names   = [PIVOT_CANONICAL] + [b["canonical"] for b in e5_alternates]
    member_queries = [pivot_q] + [b["solo_query"] for b in e5_alternates]

    bundle_path = BUNDLED_DIR / "premium_tea_e5_alternates.json"
    if bundle_path.exists():
        rec = json.loads(bundle_path.read_text())
        parsed_slots = rec["slot_results"]
        print(f"  E5 alternates bundle: cached")
    else:
        print(f"  E5 alternates bundle: {', '.join(member_names)}",
              end=" ... ", flush=True)
        data, http_status, error, n_attempts = call_serpapi(",".join(member_queries))
        parsed_slots = parse_bundle_timeline(data, len(member_names))
        rec = {
            "category":          "premium_tea",
            "bundle_label":      "alternates",
            "queries":           member_queries,
            "query_source":      "bare_canonical_per_DEVIATIONS_Entry_1",
            "member_names":      member_names,
            "window":            WINDOW,
            "geo":               GEO,
            "test_timestamp":    datetime.now(timezone.utc).isoformat(),
            "http_status":       http_status,
            "n_attempts":        n_attempts,
            "serpapi_error":     error,
            "slot_results":      parsed_slots,
        }
        bundle_path.write_text(json.dumps(rec, indent=2, ensure_ascii=False))
        print("DONE" if data is not None else f"FAIL_API ({error})")
        time.sleep(SERPAPI_DELAY_SEC)

    for slot_idx, b in enumerate(e5_alternates, start=1):
        slot = parsed_slots[slot_idx]
        if slot["all_zero"]:
            b["e5_status"] = "ALL_ZERO"
        else:
            b["e5_status"] = "PASS_E5"
        b["e5_slot_max"]  = slot["max"]
        b["e5_slot_mean"] = slot["mean"]
    print()
else:
    print("STAGE 3 skipped (no E5 candidates among alternates).")
    print()

# ============================================================================
# Stage 4: Apply activation rule, append to CSV
# ============================================================================

print("=" * 72)
print("STAGE 4 — apply activation rule + append to CSV")
print("=" * 72)

# Compute final_query_tier for each alternate
for b in alternates:
    solo_status = b.get("solo_status", "")
    e5_status   = b.get("e5_status")
    if solo_status == "PASS":
        b["final_query_tier"] = "PASS"
        b["acquisition_query"] = b["solo_query"]
    elif e5_status == "PASS_E5":
        b["final_query_tier"] = "PASS_E5"
        b["acquisition_query"] = b["solo_query"]
    else:
        b["final_query_tier"] = "EXCLUDED_E1a"
        b["acquisition_query"] = ""

# Activation rule: take alternates in pre-reg order; first N that PASS/PASS_E5
# (up to chinese_gap) are ACTIVATED; rest are TESTED_NOT_ACTIVATED
n_activated_so_far = 0
for b in alternates:
    eligible = b["final_query_tier"] in ("PASS", "PASS_E5")
    if eligible and n_activated_so_far < chinese_gap:
        b["activation_status"] = "ACTIVATED"
        n_activated_so_far += 1
    elif eligible:
        b["activation_status"] = "TESTED_NOT_ACTIVATED"
    else:
        b["activation_status"] = "TESTED_NOT_ACTIVATED"  # failed alternate

print(f"Activation rule applied (pre-reg §2 order, up to gap={chinese_gap}):")
print("-" * 72)
for b in alternates:
    solo_mean = (b.get("solo_result") or {}).get("mean")
    e5_mean   = b.get("e5_slot_mean")
    mean_str  = f"mean={solo_mean}" if solo_mean else (f"e5_mean={e5_mean}" if e5_mean else "no data")
    print(f"  A{b['activation_order']}. {b['canonical']:<22} "
          f"{b['final_query_tier']:<14} {b['activation_status']:<22} {mean_str}")
print()

# Append new rows to CSV
existing_headers = list(existing_rows[0].keys()) if existing_rows else []
new_rows = []
for b in alternates:
    note_bits = [
        f"Chinese-cell alternate A{b['activation_order']} ({b['activation_status']}) per pre-reg §2",
        "DEVIATIONS Entry 1: bare canonical query",
    ]
    if b["chosen"].get("rationale"):
        note_bits.append(f"pytrends audit: {b['chosen']['rationale']}")

    solo = b.get("solo_result") or {}
    new_rows.append({
        "brand_canonical":          b["canonical"],
        "category":                 b["category"],
        "tier_in_registry":         b["tier_in_registry"],
        "pytrends_chosen_mid":      b["chosen"].get("mid", ""),
        "pytrends_chosen_title":    b["chosen"].get("title", ""),
        "pytrends_chosen_type":     b["chosen"].get("type", ""),
        "solo_query":               b.get("solo_query", "") or "",
        "solo_phase_b_result":      b.get("solo_status", ""),
        "solo_max_value":           solo.get("max") if solo else "",
        "solo_mean_value":          solo.get("mean") if solo else "",
        "e5_bundled_result":        b.get("e5_status") or "NOT_TESTED",
        "e5_slot_max":              b.get("e5_slot_max") or "",
        "e5_slot_mean":             b.get("e5_slot_mean") or "",
        "final_query_tier":         b["final_query_tier"],
        "acquisition_query":        b["acquisition_query"],
        "notes":                    " | ".join(note_bits),
    })

# Re-write CSV with existing + new rows
with OUT_CSV.open("w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=existing_headers)
    writer.writeheader()
    writer.writerows(existing_rows)
    writer.writerows(new_rows)

print(f"Appended {len(new_rows)} alternate rows to {OUT_CSV.name}")
print()

# ============================================================================
# Final summary
# ============================================================================

print("=" * 72)
print("Final eligibility after alternate activation")
print("-" * 72)

# Re-load CSV to get final picture
with OUT_CSV.open() as f:
    final_rows = list(csv.DictReader(f))

traditions = ["chinese", "japanese", "british", "indian", "us_specialty"]
total_eligible = 0
total_excluded = 0
total_not_activated = 0

for trad in traditions:
    trad_rows = [r for r in final_rows if r["tier_in_registry"] == trad]
    # Count ACTIVATED (or non-alternate PASS/PASS_E5) toward eligibility
    n_activated = 0
    n_tested_not_activated = 0
    n_excluded = 0
    for r in trad_rows:
        is_alternate = "alternate" in r.get("notes", "").lower()
        is_eligible = r["final_query_tier"] in ("PASS", "PASS_E5")
        is_not_activated = "TESTED_NOT_ACTIVATED" in r.get("notes", "")
        if is_eligible and not is_not_activated:
            n_activated += 1
        elif is_eligible and is_not_activated:
            n_tested_not_activated += 1
        else:
            n_excluded += 1

    total_eligible += n_activated
    total_excluded += n_excluded
    total_not_activated += n_tested_not_activated

    extra = ""
    if n_tested_not_activated > 0:
        extra = f"  (+ {n_tested_not_activated} tested not activated)"
    print(f"  {trad:<14}  eligible={n_activated}  excluded={n_excluded}{extra}")

print("-" * 72)
print(f"  TOTAL         eligible={total_eligible}  excluded={total_excluded}  "
      f"tested_not_activated={total_not_activated}")
print()

print(f"H_Regime4_replication condition 1 (n_eligible >= 12): "
      f"{total_eligible} eligible, threshold "
      f"{'MET' if total_eligible >= 12 else 'NOT MET'}")
print()

print("Next steps:")
print("  1. Append activation outcome to osf/v14/DEVIATIONS.md as Entry 2")
print("  2. Commit Phase B v2 + alternate activation outputs:")
print("       git add osf/v14/data/phaseB_validation/ osf/v14/data/phaseB_suggestions/")
print("       git add osf/v14/registries/topic_id_resolution_log_v0.14.csv")
print("       git add osf/v14/registries/topic_id_resolution_log_v0.14_v1.csv")
print("       git add osf/v14/DEVIATIONS.md")
print("  3. The locked CSV is ready for the full acquisition.")
