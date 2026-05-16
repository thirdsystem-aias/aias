"""v0.16 Phase B — topic-ID resolution + solo/E5 validation (kitchen knives).

Carries forward v0.15 methodology (DEVIATIONS Entry 1: bare canonical
queries for all brands, not pytrends MIDs). v0.16 substrate is kitchen
knives — first knives phase under v1.2 protocol, lineage extension of
v0.8 Discourse-Language Knives (SSRN 6728000).

v0.16 vs v0.15:
  - Substrate: premium tea -> kitchen knives
  - Registry schema: v0.16 uses panel/alternates with display_name/brand_id/
    tradition_cell (not canonical/tradition). Schema adapter at Stage 0.
  - Pivot: Twinings -> Victorinox (chef-knife sub-category; Phase A
    pivot validation handles Swiss-Army-knife adjacency per pre-reg §3)
  - Tradition cells (5): japanese, german, french, american_specialty, chinese
  - Cell collapse rule (per v0.16 pre-reg §6): if any tradition cell falls
    below n_eligible = 3 after pre-registered alternate exhaustion, that
    cell is retained for descriptive reporting with underpower flag and
    excluded from inferential analysis.
  - High-risk brand subset flagged for §4 emphasis: Sabatier, Laguiole,
    Mac, ZHEN, Made In, Friedr. Dick, CCK, Global, Güde
    (per pre-reg §3 topic_id_notes and DEVIATIONS Entry 1).

Reads: ~/aias/registries/brands_kitchen_knives_v0.16.json
Writes:
  ~/aias/osf/v16/data/phaseB_suggestions/{brand}.json
  ~/aias/osf/v16/data/phaseB_validation/solo/{brand}.json
  ~/aias/osf/v16/data/phaseB_validation/bundled/*.json
  ~/aias/osf/v16/registries/topic_id_resolution_log_v0.16.csv  (UPDATED IN PLACE
    — skeleton already exists from b817a3e commit; this script fills the
    final_query_tier, acquisition_query, and topic_id_resolution_stage columns)

Pre-reg: v0.16-prereg (commit 511e339, locked 16 May 2026; corrected per
DEVIATIONS Entry 2)
Methodology base: AIAS Presence Measurement Protocol v1.2 (SSRN 6761698)

Run:
    pip3 install pytrends --break-system-packages   # if not already installed
    export SERPAPI_KEY="..."
    python3 ~/aias/scripts/phaseB_resolve_v16.py
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
# Configuration (locked at v0.16-prereg, commit 511e339)
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

AIAS_ROOT     = Path.home() / "aias"
V16_ROOT      = AIAS_ROOT / "osf" / "v16"
REGISTRY      = AIAS_ROOT / "registries" / "brands_kitchen_knives_v0.16.json"
SUGGEST_DIR   = V16_ROOT / "data" / "phaseB_suggestions"
SOLO_DIR      = V16_ROOT / "data" / "phaseB_validation" / "solo"
BUNDLED_DIR   = V16_ROOT / "data" / "phaseB_validation" / "bundled"
OUT_CSV       = V16_ROOT / "registries" / "topic_id_resolution_log_v0.16.csv"

for d in (SUGGEST_DIR, SOLO_DIR, BUNDLED_DIR):
    d.mkdir(parents=True, exist_ok=True)

if not REGISTRY.exists():
    sys.exit(f"ERROR: registry not found at {REGISTRY}\n"
             f"Brand registry must be in place before Phase B runs.")
if not OUT_CSV.exists():
    sys.exit(f"ERROR: topic-ID log skeleton not found at {OUT_CSV}\n"
             f"Expected from b817a3e commit; check git status.")

# Out-of-sample window per pre-reg §4 inheritance (v0.13/v0.14/v0.15 pattern).
# v0.16 default: one week before the acquisition window. Pablo confirms at run.
WINDOW = "2026-05-10 2026-05-16"   # TBD: confirm before run
GEO    = ""   # Worldwide

ENDPOINT             = "https://serpapi.com/search"
SERPAPI_DELAY_SEC    = 3
PYTRENDS_DELAY_SEC   = 5
MAX_RETRIES          = 3
RETRY_DELAY_SEC      = 5

# Audit-trail keyword set (Stage 1 only, per DEVIATIONS Entry 1).
# Kitchen-cutlery context keywords; not used to gate Stage 2 query selection.
CATEGORY_TYPE_KEYWORDS = {
    "kitchen_knives": ["knife", "knives", "cutlery", "blade", "kitchen",
                       "chef", "brand", "company", "manufacturer"],
}

PIVOTS_CANONICAL = {
    "kitchen_knives": "Victorinox",   # primary pivot per pre-reg §3
}

# High-risk subset (per pre-reg §3 topic_id_notes) — surfaced in summary
# for §4 5-stage emphasis. Substantive substitution decisions logged in
# DEVIATIONS as they occur.
HIGH_RISK_BRANDS = {
    "Sabatier", "Laguiole", "Mac", "ZHEN", "Made In",
    "Friedr. Dick", "CCK Chan Chi Kee", "Global", "Güde",
}

SESSION_TS = datetime.now(timezone.utc).isoformat()


# ============================================================================
# Helpers (unchanged from v0.15)
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


def parse_solo_timeline(data):
    if data is None:
        return {"daily": [], "n_days": 0, "max": None, "mean": None,
                "all_zero": True, "parse_error": "data is None"}
    timeline = data.get("interest_over_time", {}).get("timeline_data", [])
    daily = []
    for point in timeline:
        vlist = point.get("values", [])
        if not vlist:
            continue
        try:
            v = int(vlist[0]["extracted_value"])
        except (KeyError, ValueError, TypeError):
            continue
        daily.append({"date": point.get("date", ""), "value": v})
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
            result.append({"slot": i, "daily": vals,
                           "max": max(vals),
                           "mean": round(sum(vals) / len(vals), 2),
                           "all_zero": all(v == 0 for v in vals)})
    return result


def pick_best_suggestion(brand, suggestions, category):
    if not suggestions:
        return {"mid": "", "title": "", "type": "",
                "rationale": "pytrends returned no suggestions"}
    keywords = CATEGORY_TYPE_KEYWORDS.get(category, [])
    for s in suggestions:
        type_lower = (s.get("type") or "").lower()
        if any(kw in type_lower for kw in keywords):
            return {"mid": s.get("mid", ""), "title": s.get("title", ""),
                    "type": s.get("type", ""),
                    "rationale": (f"type={s.get('type')!r} matches category "
                                  f"keyword set (audit only; not used as query)")}
    s = suggestions[0]
    return {"mid": s.get("mid", ""), "title": s.get("title", ""),
            "type": s.get("type", ""),
            "rationale": (f"no category-keyword match; defaulted to first "
                          f"suggestion (type={s.get('type')!r}; audit only)")}


def chunk(seq, size):
    for i in range(0, len(seq), size):
        yield seq[i:i + size]


# ============================================================================
# Stage 0: Load registry (v0.16 schema adapter)
# ============================================================================

reg = json.loads(REGISTRY.read_text())
category = reg.get("category", "kitchen_knives")

# v0.16 schema: panel + alternates arrays; each entry has display_name,
# brand_id, tradition_cell, tier, founded. Translate to v15-shape internally
# for Phase B compatibility.
brands = []
for b in reg["panel"]:
    brands.append({
        "canonical":        b["display_name"],
        "brand_id":         b["brand_id"],
        "category":         category,
        "tradition_cell":   b["tradition_cell"],
        "tier":             b["tier"],
        "role":             "panel",
        "founded":          b.get("founded"),
        "topic_id_notes":   b.get("topic_id_notes"),
    })

# Alternates are loaded but marked TESTED_NOT_ACTIVATED by default.
# Activation triggers per pre-reg §6 substitution rule (manual swap into
# panel list and re-run; or in-place activation by editing notes).
for b in reg["alternates"]:
    brands.append({
        "canonical":        b["display_name"],
        "brand_id":         b["brand_id"],
        "category":         category,
        "tradition_cell":   b["tradition_cell"],
        "tier":             b["tier"],
        "role":             "alternate",
        "founded":          b.get("founded"),
        "alternate_priority": b.get("alternate_priority"),
        "topic_id_notes":   None,
    })

pivot_canon = PIVOTS_CANONICAL[category]

print("=" * 72)
print(f"v0.16 Phase B — kitchen knives (DEVIATIONS Entry 1 carry-forward)")
print(f"Session timestamp: {SESSION_TS}")
print(f"Pre-reg: v0.16-prereg (commit 511e339)")
print(f"Out-of-sample window: {WINDOW}, region=Worldwide")
print("=" * 72)
print()
print(f"Brands loaded: {len(brands)} ({sum(1 for b in brands if b['role']=='panel')} panel, "
      f"{sum(1 for b in brands if b['role']=='alternate')} alternates)")
print(f"Pivot: {pivot_canon} (Phase A validation required separately)")
print(f"High-risk subset (§4 emphasis): {sorted(HIGH_RISK_BRANDS)}")
print()


# ============================================================================
# Stage 1: pytrends.suggestions() per brand (audit trail only)
# ============================================================================

print("=" * 72)
print("STAGE 1 — pytrends.suggestions() per brand (audit trail only)")
print("=" * 72)

pytrends = TrendReq(hl="en-US", tz=0, timeout=(10, 25))

n_cached, n_called, n_failed = 0, 0, 0
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
        b["chosen"] = pick_best_suggestion(b["canonical"], suggestions, b["category"])
        print(f"{len(suggestions)} suggestions; "
              f"audit-chose: {b['chosen'].get('title') or '(none)'} "
              f"[{b['chosen'].get('type') or 'n/a'}]")
        n_called += 1
        suggest_path.write_text(json.dumps({
            "brand": b["canonical"], "category": b["category"],
            "suggestions": suggestions, "chosen": b["chosen"],
            "test_timestamp": datetime.now(timezone.utc).isoformat(),
        }, indent=2, ensure_ascii=False))
        time.sleep(PYTRENDS_DELAY_SEC)
    except Exception as e:
        print(f"FAILED ({e})")
        b["suggestions"] = []
        b["chosen"] = {"mid": "", "title": "", "type": "",
                       "rationale": f"pytrends failed: {e}"}
        n_failed += 1

print(f"Stage 1 complete: {n_cached} cached, {n_called} called, {n_failed} failed.")
print()


# ============================================================================
# Stage 2: Solo SerpAPI validation (bare canonical names per DEVIATIONS Entry 1)
# ============================================================================

print("=" * 72)
print("STAGE 2 — solo SerpAPI validation (bare canonical queries)")
print("=" * 72)

n_solo_pass, n_solo_e1a = 0, 0
for b in brands:
    # Alternates only tested if their alternate_priority is requested.
    # Default: test alternates too (per v0.15 convention; TESTED_NOT_ACTIVATED
    # captures the eligibility but flag in notes that they weren't promoted
    # to the panel).
    solo_query = b["canonical"]  # bare canonical per DEVIATIONS Entry 1
    b["solo_query"] = solo_query

    solo_path = SOLO_DIR / f"{safe_name(b['canonical'])}.json"
    if solo_path.exists():
        rec = json.loads(solo_path.read_text())
        b["solo_result"] = rec["solo_result"]
        b["solo_status"] = rec["solo_status"]
        if b["solo_status"] == "PASS":
            n_solo_pass += 1
        else:
            n_solo_e1a += 1
        continue

    print(f"  solo: {b['canonical']!r}", end=" ... ", flush=True)
    data, http_status, error, n_attempts = call_serpapi(solo_query)
    parsed = parse_solo_timeline(data)
    b["solo_result"] = parsed
    if parsed["all_zero"] or parsed["n_days"] == 0:
        b["solo_status"] = "EXCLUDED_E1a_pending_E5"
        n_solo_e1a += 1
        print(f"all_zero or empty — pending E5 bundled rescue")
    else:
        b["solo_status"] = "PASS"
        n_solo_pass += 1
        print(f"PASS (n_days={parsed['n_days']}, mean={parsed['mean']})")

    solo_path.write_text(json.dumps({
        "brand":            b["canonical"],
        "category":         b["category"],
        "tradition_cell":   b["tradition_cell"],
        "solo_query":       solo_query,
        "query_source":     "bare_canonical_per_DEVIATIONS_Entry_1",
        "window":           WINDOW,
        "geo":              GEO,
        "test_timestamp":   datetime.now(timezone.utc).isoformat(),
        "http_status":      http_status,
        "n_attempts":       n_attempts,
        "serpapi_error":    error,
        "solo_result":      parsed,
        "solo_status":      b["solo_status"],
    }, indent=2, ensure_ascii=False))
    time.sleep(SERPAPI_DELAY_SEC)

print(f"Stage 2 complete: {n_solo_pass} PASS, {n_solo_e1a} pending E5.")
print()


# ============================================================================
# Stage 3: E5 bundled rescue for E1a-pending brands
# ============================================================================

print("=" * 72)
print("STAGE 3 — E5 bundled rescue (4 brands + pivot per bundle)")
print("=" * 72)

e5_candidates = [b for b in brands if b["solo_status"] == "EXCLUDED_E1a_pending_E5"]
pivot_q = pivot_canon

total_e5_runs = 0
for bundle_id, brand_chunk in enumerate(chunk(e5_candidates, 4), start=1):
    bundle_path = BUNDLED_DIR / f"{category}_e5_bundle_{bundle_id}.json"
    member_names   = [pivot_canon] + [b["canonical"] for b in brand_chunk]
    member_queries = [pivot_q] + [b["solo_query"] for b in brand_chunk]

    if bundle_path.exists():
        rec = json.loads(bundle_path.read_text())
        parsed_slots = rec["slot_results"]
    else:
        print(f"  E5 bundle {bundle_id}: {', '.join(member_names)}",
              end=" ... ", flush=True)
        data, http_status, error, n_attempts = call_serpapi(",".join(member_queries))
        parsed_slots = parse_bundle_timeline(data, len(member_names))
        bundle_path.write_text(json.dumps({
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
        }, indent=2, ensure_ascii=False))
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
print(f"Stage 3 complete: {total_e5_runs} new bundle calls; "
      f"{n_passE5} PASS_E5, {n_excluded} EXCLUDED_E1a.")
print()


# ============================================================================
# Stage 4: Update topic_id_resolution_log_v0.16.csv in place
# ============================================================================

print("=" * 72)
print("STAGE 4 — update topic_id_resolution_log_v0.16.csv")
print("=" * 72)

# Read existing skeleton (committed at b817a3e)
existing_rows = list(csv.DictReader(OUT_CSV.open()))
brand_to_existing = {r["brand_canonical"]: r for r in existing_rows}

# Update each brand's row with Phase B outcome
updated_rows = []
for r in existing_rows:
    bname = r["brand_canonical"]
    matching = [b for b in brands if b["canonical"] == bname]
    if not matching:
        # Pivot or other row — leave as is, except mark pivot acquisition_query
        if bname == pivot_canon:
            r["final_query_tier"] = "PIVOT"
            r["acquisition_query"] = pivot_canon
            r["topic_id_resolution_stage"] = "Phase A (see DEVIATIONS)"
        updated_rows.append(r)
        continue

    b = matching[0]
    solo_status = b.get("solo_status", "")
    e5_status   = b.get("e5_status")

    if solo_status == "PASS":
        final_tier = "PASS"
        acq_query  = b["solo_query"]
        stage = "Stage 2 (solo)"
    elif e5_status == "PASS_E5":
        final_tier = "PASS_E5"
        acq_query  = b["solo_query"]
        stage = "Stage 3 (E5 bundle rescue)"
    else:
        final_tier = "EXCLUDED_E1a"
        acq_query  = ""
        stage = "Stage 3 (E5 all-zero)"

    # For alternates, prefix final_tier with TESTED_NOT_ACTIVATED unless
    # promoted to panel (handled by manual edit + re-run)
    notes_bits = ["DEVIATIONS Entry 1: bare canonical query"]
    if b["role"] == "alternate":
        notes_bits.append("TESTED_NOT_ACTIVATED")
    if b["chosen"].get("rationale"):
        notes_bits.append(f"pytrends audit: {b['chosen']['rationale']}")
    if b["canonical"] in HIGH_RISK_BRANDS:
        notes_bits.append("HIGH_RISK §4 emphasis applied")

    r["final_query_tier"] = final_tier
    r["acquisition_query"] = acq_query
    r["topic_id_resolution_stage"] = stage
    # Preserve existing notes content
    existing_notes = r.get("notes", "") or ""
    r["notes"] = " | ".join(notes_bits + ([existing_notes] if existing_notes else []))
    updated_rows.append(r)

with OUT_CSV.open("w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=list(updated_rows[0].keys()))
    writer.writeheader()
    writer.writerows(updated_rows)

print(f"Updated: {OUT_CSV}  ({len(updated_rows)} rows)")
print()


# ============================================================================
# Final summary
# ============================================================================

print("=" * 72)
print("Phase B v0.16 summary")
print("-" * 72)

# Panel only (alternates excluded from cell-eligibility unless activated)
panel_rows = [r for r in updated_rows
              if r["role"] == "panel" or r["role"] == "pivot_primary"]
panel_brand_rows = [r for r in panel_rows if r["role"] == "panel"]

n_pass   = sum(1 for r in panel_brand_rows if r["final_query_tier"] == "PASS")
n_passE5 = sum(1 for r in panel_brand_rows if r["final_query_tier"] == "PASS_E5")
n_excl   = sum(1 for r in panel_brand_rows if r["final_query_tier"] == "EXCLUDED_E1a")
print(f"  kitchen_knives panel  total={len(panel_brand_rows)}  "
      f"PASS={n_pass}  PASS_E5={n_passE5}  EXCLUDED_E1a={n_excl}")

print()
print("Per-cell breakdown (for §6 cell-collapse rule check):")
print("-" * 72)
cells = ["japanese", "german", "french", "american_specialty", "chinese"]
for cell in cells:
    cell_rows = [r for r in panel_brand_rows if r["tradition_cell"] == cell]
    cell_excl = sum(1 for r in cell_rows if r["final_query_tier"] == "EXCLUDED_E1a")
    cell_total = len(cell_rows)
    cell_eligible = cell_total - cell_excl
    flag = ""
    if cell_eligible < 3:
        flag = "  <-- CELL COLLAPSE TRIGGERED (pre-reg §6; descriptive-only)"
    elif cell_eligible < 4:
        flag = "  <-- UNDERPOWER WARNING (n < 4)"
    print(f"  {cell:<22} total={cell_total}  eligible={cell_eligible}  "
          f"excluded={cell_excl}{flag}")

print()
print(f"Total panel eligible: {n_pass + n_passE5}")
print(f"H_Regime4_replication_knives n-floor (n >= 12): "
      f"{'MET' if (n_pass + n_passE5) >= 12 else 'NOT MET'}")
print()
print("Next steps:")
print(f"  1. Review topic_id_resolution_log_v0.16.csv ({n_excl} EXCLUDED_E1a)")
print(f"  2. If any cell < 3 eligible after primary panel: activate "
      f"alternates per pre-reg §6 substitution order, log activation in")
print(f"     osf/v16/DEVIATIONS.md (Entry 3+), re-run Phase B for activated")
print(f"     alternates only.")
print(f"  3. Commit phaseB outputs to git")
print(f"  4. Run: python3 ~/aias/scripts/acquire_trends_v16.py")
