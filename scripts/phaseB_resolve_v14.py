"""v0.14 Phase B — topic-ID resolution + solo/E5 validation (v2 per DEVIATIONS Entry 1).

Resolves Google Trends acquisition queries for the 22-brand premium tea panel,
validates each against the out-of-sample window via SerpAPI, and produces the
locked CSV that acquire_trends_v14.py reads at acquisition time.

DEVIATIONS Entry 1 (2026-05-12) amendment:
    Stage 2 solo_query and Stage 3 E5 pivot query now use **bare canonical
    brand names** for ALL brands, not pytrends-derived MIDs. Phase B v1
    results showed pytrends frequently surfaced product-variant or
    physical-location entities rather than brand-level entities for tea
    brands (e.g., "Republic of Ireland national football team" returned
    for Republic of Tea; "Diamond Jubilee Tea Salon" for Fortnum & Mason;
    specific product MIDs for Vahdam, Rishi, Smith Teamaker, etc.).
    Canonical-name queries aggregate Trends signal across all products
    and avoid this failure mode.

    Stage 1 pytrends.suggestions() continues to run unchanged. Its output
    is preserved as audit trail in the suggestions JSON and the
    pytrends_chosen_{mid,title,type} columns of the resolution log,
    but does not gate solo testing.

    See osf/v14/DEVIATIONS.md §1 for full rationale, root cause, and
    pre-registration scope justification.

Per pre-reg §6 (Methods, inherited from v0.13 §5.4 eligibility rules):
    E1a (pre-acquisition exclusion): brand returns notEnoughSearchVolume
        or noResults from solo SerpAPI validation against the out-of-sample
        window 2026-04-13 to 2026-04-19.
    E5 (rescue): bundled SerpAPI rescue (4 brands + pivot in a 5-slot bundle).
        PASS_E5 if nonzero in bundle; EXCLUDED_E1a if all-zero in bundle.

Pre-reg §2 Chinese-cell alternate activation rule (handled OUTSIDE this
script): if two or more Chinese-cell primary brands fail topic-ID (i.e.,
final_query_tier == EXCLUDED_E1a after Stage 4 here), the alternates in
brands_premium_tea.json `alternates` list are activated in order. To handle
this, re-run this script after manually swapping failed Chinese brands for
alternates in a working copy of brands_premium_tea.json. The activation event
is logged in osf/v14/DEVIATIONS.md.

Stages:
    Stage 1. pytrends.suggestions() per brand. Per-brand JSON at
        data/phaseB_suggestions/{brand}.json. Audit trail only — does not
        drive solo_query selection.
    Stage 2. Solo SerpAPI validation using bare canonical brand name.
        Per-brand JSON at data/phaseB_validation/solo/{brand}.json.
    Stage 3. E5 bundled rescue for E1a-flagged brands using bare canonical
        names. Per-bundle JSON at
        data/phaseB_validation/bundled/{category}_e5_bundle_{id}.json.
    Stage 4. Write registries/topic_id_resolution_log_v0.14.csv with the
        canonical decisions, plus diagnostic columns for reviewer audit.

Inputs (must exist before run):
    ~/aias/osf/v14/registries/brands_premium_tea.json

Outputs:
    ~/aias/osf/v14/data/phaseB_suggestions/{brand}.json          (22 files)
    ~/aias/osf/v14/data/phaseB_validation/solo/{brand}.json      (22 files)
    ~/aias/osf/v14/data/phaseB_validation/bundled/*.json         (varies)
    ~/aias/osf/v14/registries/topic_id_resolution_log_v0.14.csv  (canonical)

Run:
    pip3 install pytrends --break-system-packages   # if not already installed
    export SERPAPI_KEY="..."
    python3 ~/aias/scripts/phaseB_resolve_v14.py
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
# Configuration (locked at v0.14-prereg, commit b0ef30a; DEVIATIONS Entry 1)
# ============================================================================

API_KEY = os.environ.get("SERPAPI_KEY")
if not API_KEY:
    sys.exit("ERROR: SERPAPI_KEY not set. Run: export SERPAPI_KEY=your_key")

if not HAVE_PYTRENDS:
    sys.exit(
        "ERROR: pytrends not installed. Run:\n"
        "    pip3 install pytrends --break-system-packages\n"
        "Phase B requires pytrends.suggestions() for Stage 1 audit trail."
    )

V14_ROOT      = Path.home() / "aias" / "osf" / "v14"
REGISTRY_TEA  = V14_ROOT / "registries" / "brands_premium_tea.json"
SUGGEST_DIR   = V14_ROOT / "data" / "phaseB_suggestions"
SOLO_DIR      = V14_ROOT / "data" / "phaseB_validation" / "solo"
BUNDLED_DIR   = V14_ROOT / "data" / "phaseB_validation" / "bundled"
OUT_CSV       = V14_ROOT / "registries" / "topic_id_resolution_log_v0.14.csv"

for d in (SUGGEST_DIR, SOLO_DIR, BUNDLED_DIR):
    d.mkdir(parents=True, exist_ok=True)

if not REGISTRY_TEA.exists():
    sys.exit(f"ERROR: registry not found at {REGISTRY_TEA}\n"
             f"Brand registry must be in place before Phase B runs.")

# Out-of-sample window per pre-reg §3 (inherited from v0.13 protocol)
WINDOW = "2026-04-13 2026-04-19"
GEO    = ""   # Worldwide

ENDPOINT             = "https://serpapi.com/search"
SERPAPI_DELAY_SEC    = 3
PYTRENDS_DELAY_SEC   = 5
MAX_RETRIES          = 3
RETRY_DELAY_SEC      = 5

# Stage 1 audit-trail keyword set. NOT used to gate Stage 2 candidate
# selection per DEVIATIONS Entry 1 — retained so pick_best_suggestion()
# still records a "chosen" annotation for review.
CATEGORY_TYPE_KEYWORDS = {
    "premium_tea": ["tea", "brand", "beverage", "drink", "food", "company",
                    "specialty", "retail", "store"],
}

# Pivot per category (used in E5 bundle composition). Pivot canonical name
# must match Phase A's validated pivot.
PIVOTS_CANONICAL = {
    "premium_tea": "Twinings",
}

SESSION_TS = datetime.now(timezone.utc).isoformat()

# ============================================================================
# Helpers
# ============================================================================

def safe_name(name):
    """Slugify a brand canonical to a filename-safe form."""
    s = re.sub(r"[^a-zA-Z0-9_-]", "_", name)
    return re.sub(r"_+", "_", s).strip("_")


def call_serpapi(query, geo=GEO, retries=MAX_RETRIES):
    """Call SerpAPI google_trends TIMESERIES. Returns (data, status, error, n_attempts)."""
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
                # SerpAPI's "no results" comes back as 200 + error key
                return data, last_status, data["error"], attempt
            return data, last_status, None, attempt
        except Exception as e:
            last_error = str(e)
            if attempt < retries:
                time.sleep(RETRY_DELAY_SEC)
    return None, last_status, last_error, retries


def parse_solo_timeline(data):
    """Extract daily values from a SerpAPI TIMESERIES response (solo query)."""
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
    """Extract per-slot daily values from a SerpAPI TIMESERIES bundle response."""
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
    """Audit-trail helper: pick the most category-appropriate pytrends suggestion.

    Per DEVIATIONS Entry 1, the chosen suggestion is NOT used to drive
    solo_query selection. Function retained so the suggestions JSON records
    which suggestion the v0.13-style keyword filter would have picked, for
    cross-phase comparability and audit.
    """
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
# Stage 0: Load registry
# ============================================================================

brands = []
reg = json.loads(REGISTRY_TEA.read_text())
category = reg.get("category", "premium_tea")

for b in reg["brands"]:
    brands.append({
        "canonical":        b["brand"],          # v0.14 schema: 'brand' key
        "category":         category,
        "tier_in_registry": b.get("tradition", "premium"),  # mapped from tradition
        "aliases":          b.get("aliases", []),
    })

print("=" * 72)
print("v0.14 Phase B — topic-ID resolution + solo/E5 validation (v2)")
print(f"DEVIATIONS Entry 1: bare canonical queries for all brands")
print(f"Session timestamp: {SESSION_TS}")
print(f"Pre-reg: v0.14-prereg (commit b0ef30a)")
print(f"Out-of-sample window: {WINDOW}, region=Worldwide")
print("=" * 72)
print()
print(f"Brands loaded: {len(brands)} total premium tea brands")
print(f"Pivot: {PIVOTS_CANONICAL['premium_tea']} (validated PASS in Phase A)")
print()

# ============================================================================
# Stage 1: pytrends.suggestions() per brand (AUDIT TRAIL ONLY per DEVIATIONS Entry 1)
# ============================================================================

print("=" * 72)
print("STAGE 1 — pytrends.suggestions() per brand (audit trail only)")
print("=" * 72)

pytrends = TrendReq(hl="en-US", tz=0, timeout=(10, 25))

n_cached = 0
n_called = 0
n_failed = 0
for b in brands:
    suggest_path = SUGGEST_DIR / f"{safe_name(b['canonical'])}.json"

    if suggest_path.exists():
        rec = json.loads(suggest_path.read_text())
        b["suggestions"] = rec["suggestions"]
        b["chosen"]      = rec.get("chosen", {})
        n_cached += 1
        continue

    print(f"  pytrends: {b['canonical']!r}", end=" ... ", flush=True)
    try:
        suggestions = pytrends.suggestions(keyword=b["canonical"])
        suggestions = [s for s in suggestions if s.get("type") not in (None, "")]
        b["suggestions"] = suggestions
        b["chosen"] = pick_best_suggestion(b["canonical"], suggestions,
                                           b["category"])
        print(f"{len(suggestions)} suggestions; "
              f"audit-chose: {b['chosen'].get('title') or '(none)'} "
              f"[{b['chosen'].get('type') or 'n/a'}]")
        n_called += 1
    except Exception as e:
        print(f"FAILED ({e})")
        b["suggestions"] = []
        b["chosen"] = {"mid": "", "title": "", "type": "",
                       "rationale": f"pytrends exception: {e}"}
        n_failed += 1

    suggest_path.write_text(json.dumps({
        "brand_canonical":     b["canonical"],
        "category":            b["category"],
        "tier_in_registry":    b["tier_in_registry"],
        "pytrends_timestamp":  datetime.now(timezone.utc).isoformat(),
        "suggestions":         b["suggestions"],
        "chosen":              b["chosen"],
        "note": ("DEVIATIONS Entry 1: 'chosen' field is audit only; "
                 "solo_query uses bare canonical brand name."),
    }, indent=2, ensure_ascii=False))

    time.sleep(PYTRENDS_DELAY_SEC)

print()
print(f"Stage 1 complete: {n_called} new calls, {n_cached} cached, "
      f"{n_failed} failures.")
print()

# ============================================================================
# Stage 2: Solo SerpAPI validation per brand (bare canonical per DEVIATIONS Entry 1)
# ============================================================================

print("=" * 72)
print("STAGE 2 — solo SerpAPI validation (bare canonical queries)")
print(f"Window {WINDOW}, region=Worldwide")
print("=" * 72)

for b in brands:
    # DEVIATIONS Entry 1: bare canonical brand name for ALL brands, not just
    # the pivot. v1 results showed pytrends-derived MIDs frequently pointed
    # to product variants, location entities, or completely unrelated
    # Knowledge Graph adjacencies (e.g., Irish football team for Republic
    # of Tea). Canonical-name queries aggregate Trends signal across all
    # products and avoid this failure mode.
    candidate = b["canonical"]
    b["solo_query"] = candidate

    solo_path = SOLO_DIR / f"{safe_name(b['canonical'])}.json"
    if solo_path.exists():
        rec = json.loads(solo_path.read_text())
        b["solo_result"] = rec["serpapi_result"]
        b["solo_status"] = rec["solo_status"]
        continue

    print(f"  solo: {b['canonical']!r} (q={candidate!r})", end=" ... ",
          flush=True)
    data, http_status, error, n_attempts = call_serpapi(candidate)
    parsed = parse_solo_timeline(data)

    # E1a determination: solo fails if SerpAPI returned no-results error
    # OR if the parsed timeline is empty / all-zero.
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
    }
    solo_path.write_text(json.dumps(rec, indent=2, ensure_ascii=False))

    b["solo_result"] = parsed
    b["solo_status"] = solo_status

    if solo_status == "PASS":
        print(f"PASS (mean={parsed['mean']}, max={parsed['max']})")
    else:
        print(f"{solo_status} ({error or 'all-zero / empty timeline'})")

    time.sleep(SERPAPI_DELAY_SEC)

n_pass = sum(1 for b in brands if b.get("solo_status") == "PASS")
n_fail = sum(1 for b in brands if b.get("solo_status", "").startswith("FAIL"))
print()
print(f"Stage 2 complete: {n_pass} PASS, {n_fail} FAIL (-> E5 rescue).")
print()

# ============================================================================
# Stage 3: E5 bundled rescue for solo-FAILed brands
# ============================================================================

print("=" * 72)
print("STAGE 3 — E5 bundled rescue (bare canonical queries)")
print("=" * 72)

e5_candidates = [b for b in brands
                 if b.get("solo_status", "").startswith("FAIL")]

# DEVIATIONS Entry 1: pivot query is bare canonical, not pytrends MID.
pivot_canon = PIVOTS_CANONICAL[category]
pivot_brand = next((b for b in brands if b["canonical"] == pivot_canon), None)
if pivot_brand is None:
    sys.exit(f"ERROR: pivot {pivot_canon!r} not found in brand registry "
             f"for category {category!r}.")
pivot_q = pivot_canon  # bare canonical per DEVIATIONS Entry 1


def chunk(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


total_e5_runs = 0
if not e5_candidates:
    print(f"  {category}: no E5 candidates (all solo PASS).")
else:
    print(f"  {category}: {len(e5_candidates)} E5 candidates "
          f"({', '.join(b['canonical'] for b in e5_candidates)})")

    for bundle_id, brand_chunk in enumerate(chunk(e5_candidates, 4), start=1):
        bundle_path = BUNDLED_DIR / f"{category}_e5_bundle_{bundle_id}.json"
        member_names   = [pivot_canon] + [b["canonical"] for b in brand_chunk]
        member_queries = [pivot_q] + [b["solo_query"] for b in brand_chunk]

        if bundle_path.exists():
            rec = json.loads(bundle_path.read_text())
            parsed_slots = rec["slot_results"]
        else:
            print(f"    E5 bundle {bundle_id}: "
                  f"{', '.join(member_names)}", end=" ... ", flush=True)
            data, http_status, error, n_attempts = call_serpapi(
                ",".join(member_queries))
            parsed_slots = parse_bundle_timeline(data, len(member_names))
            rec = {
                "category":          category,
                "bundle_id":         bundle_id,
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
            total_e5_runs += 1
            time.sleep(SERPAPI_DELAY_SEC)

        for slot_idx, b in enumerate(brand_chunk, start=1):
            slot = parsed_slots[slot_idx]
            if slot["all_zero"]:
                b["e5_status"] = "ALL_ZERO"
            else:
                b["e5_status"] = "PASS_E5"
            b["e5_slot_max"]  = slot["max"]
            b["e5_slot_mean"] = slot["mean"]

n_passE5 = sum(1 for b in brands if b.get("e5_status") == "PASS_E5")
n_excluded = sum(1 for b in brands if b.get("e5_status") == "ALL_ZERO")
print()
print(f"Stage 3 complete: {total_e5_runs} new bundle calls; "
      f"{n_passE5} PASS_E5, {n_excluded} EXCLUDED_E1a.")
print()

# ============================================================================
# Stage 4: Write final CSV
# ============================================================================

print("=" * 72)
print("STAGE 4 — write topic_id_resolution_log_v0.14.csv")
print("=" * 72)

rows = []
for b in brands:
    solo_status = b.get("solo_status", "")
    e5_status   = b.get("e5_status")

    if solo_status == "PASS":
        final_tier = "PASS"
        acq_query  = b["solo_query"]
    elif e5_status == "PASS_E5":
        final_tier = "PASS_E5"
        acq_query  = b["solo_query"]
    else:
        final_tier = "EXCLUDED_E1a"
        acq_query  = ""

    note_bits = ["DEVIATIONS Entry 1: bare canonical query"]
    if b["chosen"].get("rationale"):
        note_bits.append(f"pytrends audit: {b['chosen']['rationale']}")

    solo = b.get("solo_result") or {}
    rows.append({
        "brand_canonical":          b["canonical"],
        "category":                 b["category"],
        "tier_in_registry":         b["tier_in_registry"],
        "pytrends_chosen_mid":      b["chosen"].get("mid", ""),
        "pytrends_chosen_title":    b["chosen"].get("title", ""),
        "pytrends_chosen_type":     b["chosen"].get("type", ""),
        "solo_query":               b.get("solo_query", "") or "",
        "solo_phase_b_result":      solo_status,
        "solo_max_value":           solo.get("max") if solo else "",
        "solo_mean_value":          solo.get("mean") if solo else "",
        "e5_bundled_result":        e5_status or "NOT_TESTED",
        "e5_slot_max":              b.get("e5_slot_max") or "",
        "e5_slot_mean":             b.get("e5_slot_mean") or "",
        "final_query_tier":         final_tier,
        "acquisition_query":        acq_query,
        "notes":                    " | ".join(note_bits),
    })

OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
with OUT_CSV.open("w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    writer.writeheader()
    writer.writerows(rows)

print(f"Wrote: {OUT_CSV}  ({len(rows)} rows)")
print()

# ============================================================================
# Final summary
# ============================================================================

print("=" * 72)
print("Phase B v2 summary")
print("-" * 72)
n_pass   = sum(1 for r in rows if r["final_query_tier"] == "PASS")
n_passE5 = sum(1 for r in rows if r["final_query_tier"] == "PASS_E5")
n_excl   = sum(1 for r in rows if r["final_query_tier"] == "EXCLUDED_E1a")
print(f"  {category:<12}  total={len(rows)}  "
      f"PASS={n_pass}  PASS_E5={n_passE5}  EXCLUDED_E1a={n_excl}")

print()
print("Per-tradition breakdown (for Chinese-cell alternate activation rule):")
print("-" * 72)
traditions = ["chinese", "japanese", "british", "indian", "us_specialty"]
for trad in traditions:
    trad_rows = [r for r in rows if r["tier_in_registry"] == trad]
    trad_excl = sum(1 for r in trad_rows if r["final_query_tier"] == "EXCLUDED_E1a")
    trad_total = len(trad_rows)
    trad_eligible = trad_total - trad_excl
    flag = ""
    if trad == "chinese" and trad_excl >= 2:
        flag = "  <-- ALTERNATE ACTIVATION TRIGGERED (pre-reg §2)"
    print(f"  {trad:<14}  total={trad_total}  "
          f"eligible={trad_eligible}  excluded={trad_excl}{flag}")

print()
n_e1a_excluded = n_excl

pivot_problems = []
pivot_row = next(r for r in rows if r["brand_canonical"] == pivot_canon)
if pivot_row["final_query_tier"] not in ("PASS", "PASS_E5"):
    pivot_problems.append(
        f"{category} pivot {pivot_canon!r}: tier={pivot_row['final_query_tier']}"
    )

if pivot_problems:
    print("=" * 72)
    print("CRITICAL: pivot failed Phase B validation:")
    for p in pivot_problems:
        print(f"  {p}")
    print()
    print("Twinings was validated at Phase A; a Phase B failure here means")
    print("the SerpAPI path produced inconsistent results. Inspect the")
    print("per-brand JSON in phaseB_validation/solo/ before locking the")
    print("acquisition. Do NOT run acquire_trends_v14.py until resolved.")
    sys.exit(1)

chinese_excl = sum(1 for r in rows
                   if r["tier_in_registry"] == "chinese"
                   and r["final_query_tier"] == "EXCLUDED_E1a")
chinese_alternate_needed = chinese_excl >= 2

print("Next steps:")
print(f"  1. Review topic_id_resolution_log_v0.14.csv "
      f"({n_e1a_excluded} EXCLUDED_E1a brands)")
if chinese_alternate_needed:
    print(f"  2. Chinese-cell alternate activation triggered "
          f"({chinese_excl} failures >= 2 threshold).")
    print(f"     Per pre-reg §2: activate alternates from brands_premium_tea.json")
    print(f"     `alternates` list in order until Chinese cell returns to 4 eligible.")
    print(f"     Log activation in osf/v14/DEVIATIONS.md, then re-run Phase B")
    print(f"     for the activated alternates.")
else:
    print(f"  2. Chinese-cell alternate activation NOT triggered "
          f"({chinese_excl} failures < 2 threshold).")
print(f"  3. Total eligible vs. H_Regime4_replication threshold "
      f"(n_eligible >= 12): {n_pass + n_passE5} eligible, "
      f"threshold {'MET' if (n_pass + n_passE5) >= 12 else 'NOT MET'}")
print(f"  4. Commit Phase B v2 outputs to git")
print(f"  5. If eligible >= 12 and pivot validated, the locked CSV is ready "
      f"for `python3 ~/aias/scripts/acquire_trends_v14.py`")
