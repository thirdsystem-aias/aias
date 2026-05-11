"""v0.13 Phase B — topic-ID resolution + solo/E5 validation.

Resolves Google Trends acquisition queries for the 47 brands in the two NEW
v0.13 categories (31 skincare + 16 finance), validates each against the
out-of-sample window via SerpAPI, and produces the locked CSV that
acquire_trends_v13.py reads at acquisition time.

Per pre-reg §5.4 eligibility rules:
    E1a (pre-acquisition exclusion): brand returns notEnoughSearchVolume
        or noResults from solo SerpAPI validation against the out-of-sample
        window 2026-04-13 to 2026-04-19.
    E5 (rescue): bundled SerpAPI rescue (4 brands + pivot in a 5-slot bundle).
        PASS_E5 if nonzero in bundle; EXCLUDED_E1a if all-zero in bundle.

Per pre-reg §3.5 Mint disambiguation strategy:
    Mint requires strict disambiguation from herb / colour / mint condition /
    MINT MOBILE / etc. Phase B tries query strategies in order until one
    PASSes solo or E5:
        1. pytrends.suggestions('Mint') — accept only if type clearly
           identifies as Personal finance / Intuit / Software / Service.
        2. 'mint personal finance'
        3. 'mint intuit'
        4. bare 'Mint'
    If none yield signal, route to EXCLUDED_E1a (per pre-reg §11, this is
    operationally treated as Condition 3 satisfied trivially in H8 evaluation).

Stages (each stage's outputs are cached to disk; re-runs skip completed
brand-level work, making the script idempotent and crash-safe):
    Stage 1. pytrends.suggestions() per brand. Per-brand JSON at
        data/phaseB_suggestions/{brand}.json.
    Stage 2. Solo SerpAPI validation per pytrends-derived candidate query.
        Per-brand JSON at data/phaseB_validation/solo/{brand}.json.
    Stage 3. E5 bundled rescue for E1a-flagged brands. Per-bundle JSON at
        data/phaseB_validation/bundled/{category}_e5_bundle_{id}.json.
    Stage 4. Mint disambiguation pass (always runs, regardless of Stages 1-3
        outcome for Mint). Per-strategy JSONs at
        data/phaseB_validation/solo/Mint_strategy_{N}.json.
    Stage 5. Write registries/topic_id_resolution_log_v0.13.csv with the
        canonical decisions, plus diagnostic columns for reviewer audit.

Inputs (must exist before run):
    ~/aias/osf/v13/registries/brands_skincare.json
    ~/aias/osf/v13/registries/brands_finance.json

Outputs:
    ~/aias/osf/v13/data/phaseB_suggestions/{brand}.json          (47 files)
    ~/aias/osf/v13/data/phaseB_validation/solo/{brand}.json      (47+ files)
    ~/aias/osf/v13/data/phaseB_validation/bundled/*.json         (varies)
    ~/aias/osf/v13/registries/topic_id_resolution_log_v0.13.csv  (canonical)

Run:
    pip3 install pytrends --break-system-packages   # if not already installed
    export SERPAPI_KEY="..."
    python3 ~/aias/scripts/phaseB_resolve_v13.py
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
# Configuration (locked at v0.13-prereg)
# ============================================================================

API_KEY = os.environ.get("SERPAPI_KEY")
if not API_KEY:
    sys.exit("ERROR: SERPAPI_KEY not set. Run: export SERPAPI_KEY=your_key")

if not HAVE_PYTRENDS:
    sys.exit(
        "ERROR: pytrends not installed. Run:\n"
        "    pip3 install pytrends --break-system-packages\n"
        "Phase B requires pytrends.suggestions() for topic-ID resolution."
    )

V13_ROOT      = Path.home() / "aias" / "osf" / "v13"
REGISTRY_SKIN = V13_ROOT / "registries" / "brands_skincare.json"
REGISTRY_FIN  = V13_ROOT / "registries" / "brands_finance.json"
SUGGEST_DIR   = V13_ROOT / "data" / "phaseB_suggestions"
SOLO_DIR      = V13_ROOT / "data" / "phaseB_validation" / "solo"
BUNDLED_DIR   = V13_ROOT / "data" / "phaseB_validation" / "bundled"
OUT_CSV       = V13_ROOT / "registries" / "topic_id_resolution_log_v0.13.csv"

for d in (SUGGEST_DIR, SOLO_DIR, BUNDLED_DIR):
    d.mkdir(parents=True, exist_ok=True)

for f in (REGISTRY_SKIN, REGISTRY_FIN):
    if not f.exists():
        sys.exit(f"ERROR: registry not found at {f}\n"
                 f"Brand registries must be in place before Phase B runs.")

# Out-of-sample window per pre-reg §4.2 / §5.4
WINDOW = "2026-04-13 2026-04-19"
GEO    = ""   # Worldwide

ENDPOINT             = "https://serpapi.com/search"
SERPAPI_DELAY_SEC    = 3
PYTRENDS_DELAY_SEC   = 5
MAX_RETRIES          = 3
RETRY_DELAY_SEC      = 5

# Type-string keywords used to pick the best pytrends suggestion per category.
# pytrends suggestion.type is a short label like "Brand", "Personal finance
# software", "Mobile app", etc. We accept suggestions whose type contains any
# of these keywords (case-insensitive).
CATEGORY_TYPE_KEYWORDS = {
    "skincare": ["brand", "skincare", "skin care", "cosmetic", "beauty",
                 "company", "skin"],
    "finance":  ["personal finance", "finance", "financial", "software",
                 "mobile app", "app", "intuit", "service", "company",
                 "budgeting"],
}

# Pivots per category (used in E5 bundle composition). Pivot canonical names
# must match Phase A's validated pivots (DEVIATIONS.md Entry 1).
PIVOTS_CANONICAL = {
    "skincare": "CeraVe",
    "finance":  "YNAB",
}

# Mint string-disambiguation strategies, ordered by pre-reg §3.5.
MINT_STRATEGIES = [
    ("mint_personal_finance", "mint personal finance"),
    ("mint_intuit",           "mint intuit"),
    ("Mint_bare",             "Mint"),
]

# Negative-keyword filter for Mint pytrends suggestions: reject suggestions
# whose type or title contains any of these (case-insensitive) — they identify
# non-finance Mint entities per pre-reg §3.5.
MINT_REJECT_KEYWORDS = [
    "mobile", "carrier", "wireless", "color", "colour", "herb", "plant",
    "leaf", "candy", "flavor", "condition",
]
# Positive-keyword filter for Mint pytrends suggestions: accept only if type
# or title contains one of these.
MINT_ACCEPT_KEYWORDS = [
    "personal finance", "intuit", "budgeting", "financial software",
    "personal-finance",
]

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
    """Extract daily values from a SerpAPI TIMESERIES response (solo query).

    Returns dict with 'daily', 'n_days', 'max', 'mean', 'all_zero'.
    """
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
    """Extract per-slot daily values from a SerpAPI TIMESERIES bundle response.

    Returns list of slot-level summaries: [{slot_idx, daily, max, mean, all_zero}, ...]
    """
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
    """Pick the most category-appropriate pytrends suggestion for `brand`.

    Returns dict with {mid, title, type, rationale} or empty dict if no good
    match found. The rationale is human-readable for audit.
    """
    if not suggestions:
        return {"mid": "", "title": "", "type": "",
                "rationale": "pytrends returned no suggestions"}

    # Special-case Mint: strict accept + reject filtering
    if brand == "Mint" and category == "finance":
        for s in suggestions:
            type_lower  = (s.get("type") or "").lower()
            title_lower = (s.get("title") or "").lower()
            combined    = f"{type_lower} {title_lower}"

            if any(bad in combined for bad in MINT_REJECT_KEYWORDS):
                continue
            if any(good in combined for good in MINT_ACCEPT_KEYWORDS):
                return {
                    "mid":       s.get("mid", ""),
                    "title":     s.get("title", ""),
                    "type":      s.get("type", ""),
                    "rationale": (f"strict Mint filter: accepted "
                                  f"type={s.get('type')!r}"),
                }
        return {"mid": "", "title": "", "type": "",
                "rationale": ("strict Mint filter: no suggestion matched "
                              "accept-keywords; falling through to "
                              "string-strategy disambiguation")}

    # Standard brand: prefer category-matching type, fall back to first
    keywords = CATEGORY_TYPE_KEYWORDS.get(category, [])
    for s in suggestions:
        type_lower = (s.get("type") or "").lower()
        if any(kw in type_lower for kw in keywords):
            return {
                "mid":       s.get("mid", ""),
                "title":     s.get("title", ""),
                "type":      s.get("type", ""),
                "rationale": (f"type={s.get('type')!r} matches category "
                              f"keyword set"),
            }

    # Fallback: first suggestion
    s = suggestions[0]
    return {
        "mid":       s.get("mid", ""),
        "title":     s.get("title", ""),
        "type":      s.get("type", ""),
        "rationale": (f"no category-keyword match; defaulted to first "
                      f"suggestion (type={s.get('type')!r})"),
    }


# ============================================================================
# Stage 0: Load registries
# ============================================================================

brands = []
for cat, path in (("skincare", REGISTRY_SKIN), ("finance", REGISTRY_FIN)):
    reg = json.loads(path.read_text())
    for b in reg["brands"]:
        brands.append({
            "canonical":         b["canonical"],
            "category":          cat,
            "tier_in_registry":  b["tier"],
        })

print("=" * 72)
print("v0.13 Phase B — topic-ID resolution + solo/E5 validation")
print(f"Session timestamp: {SESSION_TS}")
print(f"Out-of-sample window: {WINDOW}, region=Worldwide")
print("=" * 72)
print()
print(f"Brands loaded: {len(brands)} total "
      f"({sum(1 for b in brands if b['category'] == 'skincare')} skincare + "
      f"{sum(1 for b in brands if b['category'] == 'finance')} finance)")
print()

# ============================================================================
# Stage 1: pytrends.suggestions() per brand
# ============================================================================

print("=" * 72)
print("STAGE 1 — pytrends.suggestions() per brand")
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
        # pytrends sometimes appends its own "Search term" row; filter
        suggestions = [s for s in suggestions if s.get("type") not in (None, "")]
        b["suggestions"] = suggestions
        b["chosen"] = pick_best_suggestion(b["canonical"], suggestions,
                                           b["category"])
        print(f"{len(suggestions)} suggestions; "
              f"chose: {b['chosen'].get('title') or '(none)'} "
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
    }, indent=2, ensure_ascii=False))

    time.sleep(PYTRENDS_DELAY_SEC)

print()
print(f"Stage 1 complete: {n_called} new calls, {n_cached} cached, "
      f"{n_failed} failures.")
print()

# ============================================================================
# Stage 2: Solo SerpAPI validation per brand
# ============================================================================

print("=" * 72)
print("STAGE 2 — solo SerpAPI validation")
print(f"Window {WINDOW}, region=Worldwide")
print("=" * 72)

for b in brands:
    # Mint is handled separately in Stage 4 — record a placeholder solo result
    if b["canonical"] == "Mint":
        b["solo_query"]        = None
        b["solo_status"]       = "DEFERRED_TO_STAGE_4"
        b["solo_result"]       = None
        continue

    # Pivots: always use bare canonical (Phase A validated this query;
    # overriding any pytrends-derived mid to guarantee consistency between
    # Phase A's outcome and the locked acquisition's pivot query).
    if b["canonical"] in PIVOTS_CANONICAL.values():
        candidate = b["canonical"]
    else:
        # Standard brand: pytrends mid if present, else bare canonical
        candidate = b["chosen"].get("mid") or b["canonical"]
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
        # SerpAPI's notEnoughSearchVolume / noResults arrives as error key
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
print(f"Stage 2 complete: {n_pass} PASS, {n_fail} FAIL (-> E5 rescue), "
      f"1 deferred (Mint).")
print()

# ============================================================================
# Stage 3: E5 bundled rescue for solo-FAILed brands
# ============================================================================

print("=" * 72)
print("STAGE 3 — E5 bundled rescue")
print("=" * 72)

# Collect E5 candidates per category; bundle into chunks of 4 + pivot
e5_per_category = {}
for cat in PIVOTS_CANONICAL:
    e5_per_category[cat] = [b for b in brands
                            if b["category"] == cat
                            and b.get("solo_status", "").startswith("FAIL")]

# Build pivot query lookup (use canonical-name query as fallback if no Stage 1
# chosen mid). For E5 bundles, pivot uses the same query candidate as in
# acquire_trends_v13.py.
pivot_query = {}
for cat, pivot_canon in PIVOTS_CANONICAL.items():
    pivot_brand = next((b for b in brands if b["canonical"] == pivot_canon), None)
    if pivot_brand is None:
        sys.exit(f"ERROR: pivot {pivot_canon!r} not found in brand registry "
                 f"for category {cat!r}.")
    pivot_query[cat] = pivot_brand["chosen"].get("mid") or pivot_canon


def chunk(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


total_e5_runs = 0
for cat, candidates in e5_per_category.items():
    if not candidates:
        print(f"  {cat}: no E5 candidates.")
        continue

    print(f"  {cat}: {len(candidates)} E5 candidates "
          f"({', '.join(b['canonical'] for b in candidates)})")
    pivot_q = pivot_query[cat]
    for bundle_id, brand_chunk in enumerate(chunk(candidates, 4), start=1):
        bundle_path = BUNDLED_DIR / f"{cat}_e5_bundle_{bundle_id}.json"
        member_names   = [PIVOTS_CANONICAL[cat]] + [b["canonical"] for b in brand_chunk]
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
                "category":          cat,
                "bundle_id":         bundle_id,
                "queries":           member_queries,
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

        # Attribute per-brand E5 status from slot results
        # slot 0 = pivot, slots 1..N = candidate brands
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
# Stage 4: Mint disambiguation
# ============================================================================

print("=" * 72)
print("STAGE 4 — Mint disambiguation (string strategies)")
print("=" * 72)

mint = next(b for b in brands if b["canonical"] == "Mint")
mint_strategy_results = []
mint_winning_strategy = None
mint_winning_query    = None
mint_winning_result   = None

# Test the pytrends-derived strategy first if Mint had a clean Stage 1 chosen
mint_pytrends_mid = mint["chosen"].get("mid", "")
strategies_to_try = []
if mint_pytrends_mid:
    strategies_to_try.append(
        ("pytrends_mid", mint_pytrends_mid,
         f"pytrends-derived topic-ID matching strict Mint filter "
         f"(title={mint['chosen'].get('title')!r}, "
         f"type={mint['chosen'].get('type')!r})")
    )
for label, query in MINT_STRATEGIES:
    strategies_to_try.append((label, query, "pre-reg §3.5 string strategy"))

for label, query, rationale in strategies_to_try:
    strategy_path = SOLO_DIR / f"Mint_strategy_{label}.json"
    if strategy_path.exists():
        rec = json.loads(strategy_path.read_text())
        parsed     = rec["serpapi_result"]
        solo_status = rec["solo_status"]
        error      = rec.get("serpapi_error")
    else:
        print(f"  Mint strategy {label!r}: q={query!r}", end=" ... ",
              flush=True)
        data, http_status, error, n_attempts = call_serpapi(query)
        parsed = parse_solo_timeline(data)
        if data is None:
            solo_status = "FAIL_API"
        elif error is not None and any(
                s in error.lower() for s in ("no results", "not enough", "noresults")):
            solo_status = "FAIL_NO_SIGNAL"
        elif parsed["all_zero"]:
            solo_status = "FAIL_NO_SIGNAL"
        else:
            solo_status = "PASS"
        rec = {
            "brand_canonical":   "Mint",
            "strategy_label":    label,
            "rationale":         rationale,
            "query":             query,
            "window":            WINDOW,
            "geo":               GEO,
            "test_timestamp":    datetime.now(timezone.utc).isoformat(),
            "http_status":       http_status,
            "n_attempts":        n_attempts,
            "serpapi_error":     error,
            "serpapi_result":    parsed,
            "solo_status":       solo_status,
        }
        strategy_path.write_text(json.dumps(rec, indent=2, ensure_ascii=False))
        print(f"{solo_status} "
              f"(mean={parsed['mean']}, max={parsed['max']})"
              if solo_status == "PASS"
              else f"{solo_status} ({error or 'all-zero / empty'})")
        time.sleep(SERPAPI_DELAY_SEC)

    mint_strategy_results.append({
        "label":        label,
        "query":        query,
        "rationale":    rationale,
        "solo_status":  solo_status,
        "mean":         parsed.get("mean"),
        "max":          parsed.get("max"),
        "error":        error,
    })
    if solo_status == "PASS" and mint_winning_strategy is None:
        mint_winning_strategy = label
        mint_winning_query    = query
        mint_winning_result   = parsed

mint["mint_strategy_results"] = mint_strategy_results
mint["mint_winning_strategy"] = mint_winning_strategy
mint["mint_winning_query"]    = mint_winning_query
mint["mint_winning_result"]   = mint_winning_result

if mint_winning_strategy:
    mint["solo_query"]  = mint_winning_query
    mint["solo_status"] = "PASS"
    mint["solo_result"] = mint_winning_result
    print()
    print(f"Mint Stage 4 outcome: PASS via strategy {mint_winning_strategy!r} "
          f"(query={mint_winning_query!r}, mean={mint_winning_result['mean']})")
else:
    # All strategies failed solo. Try E5 rescue using the last (broadest)
    # strategy: bare "Mint". Bundle Mint with YNAB pivot + 3 other finance
    # brands (using already-validated PASS brands as bundle padding).
    print()
    print("Mint Stage 4 outcome: all strategies FAILED solo. "
          "Attempting E5 rescue with bare 'Mint' query.")

    fin_pass = [b for b in brands
                if b["category"] == "finance"
                and b["canonical"] != "Mint"
                and b.get("solo_status") == "PASS"]
    # Take up to 3 PASS brands as bundle padding
    bundle_pad = fin_pass[:3]
    if len(bundle_pad) < 3:
        # Not enough PASS brands for a full bundle; pad with the pivot
        # repeated (any 5-slot composition works for E5 attribution)
        bundle_pad = bundle_pad + [next(b for b in brands
                                        if b["canonical"] == "YNAB")] * (3 - len(bundle_pad))

    member_names   = ["YNAB"] + [b["canonical"] for b in bundle_pad] + ["Mint"]
    member_queries = [pivot_query["finance"]] + \
                     [b["solo_query"] for b in bundle_pad] + ["Mint"]

    bundle_path = BUNDLED_DIR / "finance_e5_mint_rescue.json"
    if bundle_path.exists():
        rec = json.loads(bundle_path.read_text())
        parsed_slots = rec["slot_results"]
    else:
        print(f"  E5 Mint-rescue bundle: {', '.join(member_names)}",
              end=" ... ", flush=True)
        data, http_status, error, n_attempts = call_serpapi(
            ",".join(member_queries))
        parsed_slots = parse_bundle_timeline(data, len(member_names))
        rec = {
            "category":          "finance",
            "bundle_label":      "mint_rescue",
            "queries":           member_queries,
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

    mint_slot = parsed_slots[-1]  # Mint is the last slot
    if mint_slot["all_zero"]:
        mint["e5_status"] = "ALL_ZERO"
        print(f"Mint E5 rescue: ALL_ZERO -> EXCLUDED_E1a "
              f"(phantom-no-Trends-signal; H8 Condition 3 trivially satisfied)")
    else:
        mint["e5_status"]   = "PASS_E5"
        mint["solo_query"]  = "Mint"   # bare query, since this is what the
                                       # bundle actually used
        print(f"Mint E5 rescue: PASS_E5 with bare 'Mint' "
              f"(mean={mint_slot['mean']}, max={mint_slot['max']})")

print()

# ============================================================================
# Stage 5: Write final CSV
# ============================================================================

print("=" * 72)
print("STAGE 5 — write topic_id_resolution_log_v0.13.csv")
print("=" * 72)

rows = []
for b in brands:
    # Determine final_query_tier and acquisition_query
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

    # Build a notes string with audit detail
    note_bits = []
    if b["canonical"] == "Mint":
        winning = b.get("mint_winning_strategy")
        if winning:
            note_bits.append(f"Mint disambiguation PASS via {winning!r}")
        else:
            note_bits.append(
                "Mint disambiguation: all string strategies failed solo; "
                + (f"E5 rescue: {e5_status}" if e5_status
                   else "no E5 rescue attempted")
            )
    if b["chosen"].get("rationale"):
        note_bits.append(f"pytrends: {b['chosen']['rationale']}")

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
print("Phase B summary")
print("-" * 72)
for cat in ("skincare", "finance"):
    cat_rows = [r for r in rows if r["category"] == cat]
    n_pass   = sum(1 for r in cat_rows if r["final_query_tier"] == "PASS")
    n_passE5 = sum(1 for r in cat_rows if r["final_query_tier"] == "PASS_E5")
    n_excl   = sum(1 for r in cat_rows if r["final_query_tier"] == "EXCLUDED_E1a")
    print(f"  {cat:<10}  total={len(cat_rows)}  "
          f"PASS={n_pass}  PASS_E5={n_passE5}  EXCLUDED_E1a={n_excl}")

print()
print("Mint outcome:")
mint_row = next(r for r in rows if r["brand_canonical"] == "Mint")
print(f"  final_query_tier: {mint_row['final_query_tier']}")
print(f"  acquisition_query: {mint_row['acquisition_query']!r}")
print(f"  notes: {mint_row['notes']}")
print()

n_e1a_excluded = sum(1 for r in rows if r["final_query_tier"] == "EXCLUDED_E1a")

# Safety check: pivots MUST be PASS or PASS_E5, otherwise acquisition will fail
pivot_problems = []
for cat, pivot_canon in PIVOTS_CANONICAL.items():
    pivot_row = next(r for r in rows if r["brand_canonical"] == pivot_canon)
    if pivot_row["final_query_tier"] not in ("PASS", "PASS_E5"):
        pivot_problems.append(
            f"{cat} pivot {pivot_canon!r}: tier={pivot_row['final_query_tier']}"
        )

if pivot_problems:
    print("=" * 72)
    print("CRITICAL: pivot(s) failed Phase B validation:")
    for p in pivot_problems:
        print(f"  {p}")
    print()
    print("Both pivots were validated at Phase A; a Phase B failure here means")
    print("the pytrends or SerpAPI path produced inconsistent results. Inspect")
    print("the per-brand JSONs in phaseB_validation/solo/ before locking the")
    print("acquisition. Do NOT run acquire_trends_v13.py until resolved.")
    sys.exit(1)

print("Next steps:")
print(f"  1. Review topic_id_resolution_log_v0.13.csv "
      f"({n_e1a_excluded} EXCLUDED_E1a brands; verify against registries)")
print(f"  2. Commit Phase B outputs to git")
print(f"  3. If satisfied, the locked CSV is ready for "
      f"`python3 ~/aias/scripts/acquire_trends_v13.py`")
