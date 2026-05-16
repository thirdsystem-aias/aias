"""v0.16 Phase A — pivot validation (Victorinox; Wüsthof fallback).

Runs BEFORE phaseB_resolve_v16.py. Validates that the primary pivot
(Victorinox) satisfies the v1.2 §4 5-stage protocol with particular
attention to Swiss-Army-knife adjacency confusion (the topic-ID risk
flagged in pre-reg §3).

Per pre-reg §3:
  Primary pivot: Victorinox (Swiss, founded 1884) — chef-knife line
    (Swiss Classic / Fibrox).
  Fallback: Wüsthof (German, 1814) — activated only if Victorinox fails
    §4 confusion threshold.

Per pre-reg §6 (pivot failure contingency):
  If Victorinox topic-ID resolution exceeds v1.2 §4 confusion threshold
  at lock, Wüsthof inherits the pivot role; Wüsthof exits the German
  tradition cell (cell collapses to n=4, no within-cell alternate
  substitution).

§4 5-stage protocol (applied to pivot in addition to Phase B's per-brand
application):
  Stage 1: pytrends.suggestions() — audit trail (DEVIATIONS Entry 1)
  Stage 2: Out-of-sample baseline (12-month SerpAPI TIMESERIES);
           compute mean, SD, CV. Per pre-reg §3 "stable search interest"
           requirement.
  Stage 3: Bundle position test (pivot + 4 knife brands). Check pivot
           relative position is reasonable (not dominating, not dwarfed).
  Stage 4: Adjacency confusion test. Bundle with Swiss-Army-knife terms.
           Quantify chef-knife sub-category proportion vs Swiss-Army
           adjacency.
  Stage 5: Combined verdict. PASS -> pivot holds; FAIL -> Wüsthof fallback.

Outputs:
  ~/aias/osf/v16/data/phaseA/stage1_suggestions.json
  ~/aias/osf/v16/data/phaseA/stage2_baseline.json
  ~/aias/osf/v16/data/phaseA/stage3_bundle_position.json
  ~/aias/osf/v16/data/phaseA/stage4_adjacency.json
  ~/aias/osf/v16/data/phaseA/stage5_verdict.json
  ~/aias/osf/v16/registries/topic_id_resolution_log_v0.16.csv  (pivot row updated)

Pre-reg: v0.16-prereg (commit 511e339; corrected per DEVIATIONS Entry 2)
Methodology base: AIAS Presence Measurement Protocol v1.2 (SSRN 6761698)

Run:
    pip3 install pytrends --break-system-packages  # if needed
    export SERPAPI_KEY="..."
    python3 ~/aias/scripts/phaseA_pivot_v16.py
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
    sys.exit("ERROR: pytrends not installed.\n"
             "Run: pip3 install pytrends --break-system-packages")

V16_ROOT     = Path.home() / "aias" / "osf" / "v16"
PHASEA_DIR   = V16_ROOT / "data" / "phaseA"
TOPIC_ID_CSV = V16_ROOT / "registries" / "topic_id_resolution_log_v0.16.csv"

PHASEA_DIR.mkdir(parents=True, exist_ok=True)

if not TOPIC_ID_CSV.exists():
    sys.exit(f"ERROR: topic-ID log skeleton not found at {TOPIC_ID_CSV}\n"
             f"Expected from b817a3e commit; check git status.")

# Pivot candidates per pre-reg §3
PRIMARY_PIVOT  = "Victorinox"
FALLBACK_PIVOT = "Wüsthof"

# Stage 3 reference panel (top knife brands; subset of acquire_trends_v16
# bundle 1+2 members). Used to check pivot's relative bundle position.
STAGE3_REFERENCE_BRANDS = ["Shun", "Global", "Miyabi", "Wüsthof", "Zwilling J.A. Henckels"]

# Stage 4 adjacency terms. Victorinox-specific topic-ID risks per pre-reg §3.
# These are the competing-context terms that, if dominant, indicate the
# pivot signal is reading Swiss-Army-knife rather than chef-knife traffic.
STAGE4_CHEF_KNIFE_TERM    = "Victorinox chef knife"
STAGE4_SWISS_ARMY_TERM    = "Swiss Army knife"

# Stability window (Stage 2) — 12 months ending before Phase B out-of-sample.
# Pablo confirms before run.
STABILITY_WINDOW = "2025-05-01 2026-04-30"   # TBD: confirm before run
GEO              = ""   # Worldwide

# Thresholds — PLACEHOLDER values. Pablo confirms based on protocol §4
# canonical specification. The script surfaces raw values regardless;
# thresholds gate the auto-verdict but Pablo reviews the structured
# outputs and can override.
CV_THRESHOLD_PCT          = 30.0  # Stage 2: CV must be < this for stability
PIVOT_REL_MIN             = 0.5   # Stage 3: pivot mean >= 0.5x median ref brand
PIVOT_REL_MAX             = 5.0   # Stage 3: pivot mean <= 5.0x median ref brand
CHEF_KNIFE_PROP_MIN       = 0.20  # Stage 4: chef-knife sub-context proportion >= 20%
SWISS_ARMY_PROP_MAX       = 0.70  # Stage 4: Swiss-Army adjacency <= 70%

ENDPOINT          = "https://serpapi.com/search"
SERPAPI_DELAY_SEC = 3
MAX_RETRIES       = 3
RETRY_DELAY_SEC   = 5
PYTRENDS_DELAY_SEC = 5

SESSION_TS = datetime.now(timezone.utc).isoformat()


# ============================================================================
# SerpAPI / pytrends helpers (carry-forward from phaseB_resolve_v15)
# ============================================================================

def call_serpapi(query, window=STABILITY_WINDOW, geo=GEO, retries=MAX_RETRIES):
    """Call SerpAPI google_trends TIMESERIES. Returns (data, status, error, n_attempts)."""
    params = {
        "engine":    "google_trends",
        "q":         query,
        "data_type": "TIMESERIES",
        "date":      window,
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
    """Parse SerpAPI TIMESERIES solo response. Returns list of (date, value) tuples."""
    if data is None:
        return []
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
    return daily


def parse_bundle_timeline(data, n_slots):
    """Parse SerpAPI TIMESERIES bundle response. Returns per-slot daily values."""
    if data is None:
        return [{"slot": i, "daily": [], "mean": None, "all_zero": True}
                for i in range(n_slots)]
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
            result.append({"slot": i, "daily": [], "mean": None,
                           "max": None, "all_zero": True})
        else:
            result.append({"slot": i,
                           "daily": vals,
                           "n_days": len(vals),
                           "mean": round(statistics.mean(vals), 2),
                           "max": max(vals),
                           "sd": round(statistics.stdev(vals), 2) if len(vals) > 1 else 0.0,
                           "all_zero": all(v == 0 for v in vals)})
    return result


# ============================================================================
# Stage 1: pytrends.suggestions() — audit trail
# ============================================================================

def run_stage1(pivot_name):
    print("=" * 72)
    print(f"STAGE 1 — pytrends.suggestions() for {pivot_name!r} (audit trail)")
    print("=" * 72)

    pytrends = TrendReq(hl="en-US", tz=0, timeout=(10, 25))

    out_path = PHASEA_DIR / "stage1_suggestions.json"
    if out_path.exists():
        rec = json.loads(out_path.read_text())
        print(f"  Cached at {out_path}")
        print(f"  {len(rec['suggestions'])} suggestions found.")
        return rec

    print(f"  Querying pytrends.suggestions({pivot_name!r}) ...")
    try:
        suggestions = pytrends.suggestions(keyword=pivot_name)
        suggestions = [s for s in suggestions if s.get("type") not in (None, "")]
    except Exception as e:
        print(f"  FAILED ({e})")
        suggestions = []

    rec = {
        "pivot_canonical":      pivot_name,
        "session_timestamp":    datetime.now(timezone.utc).isoformat(),
        "query_source":         "bare_canonical_per_DEVIATIONS_Entry_1",
        "n_suggestions":        len(suggestions),
        "suggestions":          suggestions,
        "audit_note":           ("Per DEVIATIONS Entry 1: suggestions are "
                                 "AUDIT-ONLY. Do NOT gate Stage 2 query "
                                 "selection on this output."),
    }
    out_path.write_text(json.dumps(rec, indent=2, ensure_ascii=False))
    print(f"  {len(suggestions)} suggestions. Top 5:")
    for s in suggestions[:5]:
        print(f"    title={s.get('title')!r}  type={s.get('type')!r}  mid={s.get('mid')!r}")
    print(f"  Written to {out_path}")
    time.sleep(PYTRENDS_DELAY_SEC)
    return rec


# ============================================================================
# Stage 2: Out-of-sample baseline (12-month TIMESERIES)
# ============================================================================

def run_stage2(pivot_name):
    print()
    print("=" * 72)
    print(f"STAGE 2 — out-of-sample baseline for {pivot_name!r}")
    print(f"  Window: {STABILITY_WINDOW}, Geo: WORLDWIDE")
    print("=" * 72)

    out_path = PHASEA_DIR / "stage2_baseline.json"
    if out_path.exists():
        rec = json.loads(out_path.read_text())
        print(f"  Cached at {out_path}")
        print(f"  mean={rec['mean']}, sd={rec['sd']}, CV={rec['cv_pct']:.2f}%")
        return rec

    print(f"  Querying SerpAPI TIMESERIES ...")
    data, http_status, error, n_attempts = call_serpapi(pivot_name)

    daily = parse_solo_timeline(data)
    if not daily:
        rec = {
            "pivot_canonical":      pivot_name,
            "session_timestamp":    datetime.now(timezone.utc).isoformat(),
            "window":               STABILITY_WINDOW,
            "geo":                  GEO,
            "http_status":          http_status,
            "serpapi_error":        error or "no_daily_points",
            "n_days":               0,
            "mean":                 None,
            "sd":                   None,
            "cv_pct":               None,
            "stability_pass":       False,
            "stability_rationale":  "No daily points returned by SerpAPI",
        }
    else:
        vals = [p["value"] for p in daily]
        mean = statistics.mean(vals)
        sd = statistics.stdev(vals) if len(vals) > 1 else 0.0
        cv_pct = (sd / mean * 100.0) if mean > 0 else float("inf")
        stability_pass = cv_pct < CV_THRESHOLD_PCT

        rec = {
            "pivot_canonical":      pivot_name,
            "session_timestamp":    datetime.now(timezone.utc).isoformat(),
            "window":               STABILITY_WINDOW,
            "geo":                  GEO,
            "http_status":          http_status,
            "serpapi_error":        error,
            "n_days":               len(vals),
            "mean":                 round(mean, 2),
            "sd":                   round(sd, 2),
            "min":                  min(vals),
            "max":                  max(vals),
            "cv_pct":               round(cv_pct, 2),
            "cv_threshold_pct":     CV_THRESHOLD_PCT,
            "stability_pass":       bool(stability_pass),
            "stability_rationale":  (f"CV={cv_pct:.2f}% < {CV_THRESHOLD_PCT}% threshold: PASS"
                                     if stability_pass else
                                     f"CV={cv_pct:.2f}% >= {CV_THRESHOLD_PCT}% threshold: FAIL"),
            "daily":                daily,
        }
    out_path.write_text(json.dumps(rec, indent=2, ensure_ascii=False))
    print(f"  n_days={rec['n_days']}, mean={rec['mean']}, sd={rec['sd']}, "
          f"CV={rec['cv_pct']}%")
    print(f"  Verdict: {rec['stability_rationale']}")
    time.sleep(SERPAPI_DELAY_SEC)
    return rec


# ============================================================================
# Stage 3: Bundle position test
# ============================================================================

def run_stage3(pivot_name, reference_brands):
    print()
    print("=" * 72)
    print(f"STAGE 3 — bundle position test")
    print(f"  Pivot: {pivot_name}")
    print(f"  Reference brands: {reference_brands}")
    print("=" * 72)

    out_path = PHASEA_DIR / "stage3_bundle_position.json"
    if out_path.exists():
        rec = json.loads(out_path.read_text())
        print(f"  Cached at {out_path}")
        return rec

    query = ",".join([pivot_name] + reference_brands)
    n_slots = 1 + len(reference_brands)
    print(f"  Querying SerpAPI bundle: {query!r}")
    data, http_status, error, n_attempts = call_serpapi(query)
    parsed = parse_bundle_timeline(data, n_slots)

    pivot_slot = parsed[0]
    ref_slots = parsed[1:]
    ref_means = [s["mean"] for s in ref_slots if s["mean"] is not None]

    if pivot_slot["mean"] is None or not ref_means:
        rec = {
            "pivot_canonical":     pivot_name,
            "session_timestamp":   datetime.now(timezone.utc).isoformat(),
            "window":              STABILITY_WINDOW,
            "query":               query,
            "http_status":         http_status,
            "serpapi_error":       error,
            "pivot_mean":          pivot_slot["mean"],
            "ref_means":           {b: s["mean"] for b, s in zip(reference_brands, ref_slots)},
            "position_pass":       False,
            "position_rationale":  "Insufficient data to evaluate bundle position",
        }
    else:
        ref_median = statistics.median(ref_means)
        rel_ratio = pivot_slot["mean"] / ref_median if ref_median > 0 else float("inf")
        position_pass = PIVOT_REL_MIN <= rel_ratio <= PIVOT_REL_MAX
        rec = {
            "pivot_canonical":      pivot_name,
            "session_timestamp":    datetime.now(timezone.utc).isoformat(),
            "window":               STABILITY_WINDOW,
            "query":                query,
            "http_status":          http_status,
            "serpapi_error":        error,
            "pivot_mean":           pivot_slot["mean"],
            "pivot_max":            pivot_slot.get("max"),
            "ref_means":            {b: s["mean"] for b, s in zip(reference_brands, ref_slots)},
            "ref_median":           round(ref_median, 2),
            "pivot_to_ref_ratio":   round(rel_ratio, 3),
            "ratio_band":           [PIVOT_REL_MIN, PIVOT_REL_MAX],
            "position_pass":        bool(position_pass),
            "position_rationale":   (
                f"pivot/median(ref)={rel_ratio:.2f} ∈ "
                f"[{PIVOT_REL_MIN}, {PIVOT_REL_MAX}]: PASS"
                if position_pass else
                f"pivot/median(ref)={rel_ratio:.2f} OUT OF "
                f"[{PIVOT_REL_MIN}, {PIVOT_REL_MAX}]: FAIL"
            ),
        }
    out_path.write_text(json.dumps(rec, indent=2, ensure_ascii=False))
    print(f"  pivot_mean={rec.get('pivot_mean')}, ref_median={rec.get('ref_median')}")
    print(f"  Ratio: {rec.get('pivot_to_ref_ratio')} (band: "
          f"{rec.get('ratio_band')})")
    print(f"  Verdict: {rec['position_rationale']}")
    time.sleep(SERPAPI_DELAY_SEC)
    return rec


# ============================================================================
# Stage 4: Adjacency confusion test
# ============================================================================

def run_stage4(pivot_name, chef_term, swiss_army_term):
    print()
    print("=" * 72)
    print(f"STAGE 4 — adjacency confusion test")
    print(f"  Pivot: {pivot_name}")
    print(f"  Chef-knife sub-context: {chef_term!r}")
    print(f"  Swiss-Army adjacency: {swiss_army_term!r}")
    print("=" * 72)

    out_path = PHASEA_DIR / "stage4_adjacency.json"
    if out_path.exists():
        rec = json.loads(out_path.read_text())
        print(f"  Cached at {out_path}")
        return rec

    query = ",".join([pivot_name, chef_term, swiss_army_term])
    n_slots = 3
    print(f"  Querying SerpAPI bundle: {query!r}")
    data, http_status, error, n_attempts = call_serpapi(query)
    parsed = parse_bundle_timeline(data, n_slots)

    pivot_slot, chef_slot, sa_slot = parsed[0], parsed[1], parsed[2]
    pivot_mean = pivot_slot.get("mean")
    chef_mean  = chef_slot.get("mean")
    sa_mean    = sa_slot.get("mean")

    if any(v is None for v in (pivot_mean, chef_mean, sa_mean)):
        rec = {
            "pivot_canonical":      pivot_name,
            "session_timestamp":    datetime.now(timezone.utc).isoformat(),
            "window":               STABILITY_WINDOW,
            "query":                query,
            "http_status":          http_status,
            "serpapi_error":        error,
            "pivot_mean":           pivot_mean,
            "chef_mean":            chef_mean,
            "swiss_army_mean":      sa_mean,
            "adjacency_pass":       False,
            "adjacency_rationale":  "Insufficient data",
        }
    else:
        total = chef_mean + sa_mean
        chef_prop = chef_mean / total if total > 0 else 0.0
        sa_prop   = sa_mean / total if total > 0 else 0.0
        adjacency_pass = (
            chef_prop >= CHEF_KNIFE_PROP_MIN and
            sa_prop   <= SWISS_ARMY_PROP_MAX
        )
        rec = {
            "pivot_canonical":         pivot_name,
            "session_timestamp":       datetime.now(timezone.utc).isoformat(),
            "window":                  STABILITY_WINDOW,
            "query":                   query,
            "http_status":             http_status,
            "serpapi_error":           error,
            "pivot_mean":              round(pivot_mean, 2),
            "chef_mean":               round(chef_mean, 2),
            "swiss_army_mean":         round(sa_mean, 2),
            "chef_proportion":         round(chef_prop, 3),
            "swiss_army_proportion":   round(sa_prop, 3),
            "chef_prop_min":           CHEF_KNIFE_PROP_MIN,
            "swiss_army_prop_max":     SWISS_ARMY_PROP_MAX,
            "adjacency_pass":          bool(adjacency_pass),
            "adjacency_rationale":     (
                f"chef_prop={chef_prop:.2f} >= {CHEF_KNIFE_PROP_MIN} AND "
                f"sa_prop={sa_prop:.2f} <= {SWISS_ARMY_PROP_MAX}: PASS"
                if adjacency_pass else
                f"chef_prop={chef_prop:.2f} (need >= {CHEF_KNIFE_PROP_MIN}), "
                f"sa_prop={sa_prop:.2f} (need <= {SWISS_ARMY_PROP_MAX}): FAIL"
            ),
        }
    out_path.write_text(json.dumps(rec, indent=2, ensure_ascii=False))
    print(f"  pivot_mean={rec.get('pivot_mean')}, chef_mean={rec.get('chef_mean')}, "
          f"sa_mean={rec.get('swiss_army_mean')}")
    print(f"  chef_prop={rec.get('chef_proportion')}, "
          f"sa_prop={rec.get('swiss_army_proportion')}")
    print(f"  Verdict: {rec['adjacency_rationale']}")
    time.sleep(SERPAPI_DELAY_SEC)
    return rec


# ============================================================================
# Stage 5: Combined verdict
# ============================================================================

def run_stage5(stage1, stage2, stage3, stage4):
    print()
    print("=" * 72)
    print("STAGE 5 — combined verdict")
    print("=" * 72)

    # Conditions per pre-reg §3 + §6 + protocol §4
    stability_ok = stage2.get("stability_pass", False)
    position_ok  = stage3.get("position_pass", False)
    adjacency_ok = stage4.get("adjacency_pass", False)

    all_pass = stability_ok and position_ok and adjacency_ok

    if all_pass:
        verdict = "PASS"
        action = "Victorinox holds primary pivot role"
        cell_impact = "German tradition cell unchanged (n=5)"
    else:
        verdict = "FAIL"
        action = "Activate Wüsthof fallback pivot per pre-reg §6"
        cell_impact = ("German tradition cell collapses to n=4 (Wüsthof "
                       "exits panel; no within-cell alternate substitution "
                       "per pre-reg §6)")

    rec = {
        "session_timestamp":  datetime.now(timezone.utc).isoformat(),
        "pivot_canonical":    PRIMARY_PIVOT,
        "stage_results": {
            "stage1_audit_n_suggestions": stage1.get("n_suggestions"),
            "stage2_stability_pass":      stability_ok,
            "stage2_cv_pct":              stage2.get("cv_pct"),
            "stage3_position_pass":       position_ok,
            "stage3_pivot_to_ref_ratio":  stage3.get("pivot_to_ref_ratio"),
            "stage4_adjacency_pass":      adjacency_ok,
            "stage4_chef_proportion":     stage4.get("chef_proportion"),
            "stage4_swiss_army_proportion": stage4.get("swiss_army_proportion"),
        },
        "verdict":            verdict,
        "action":             action,
        "panel_cell_impact":  cell_impact,
        "thresholds_applied": {
            "stage2_cv_threshold_pct": CV_THRESHOLD_PCT,
            "stage3_pivot_to_ref_band": [PIVOT_REL_MIN, PIVOT_REL_MAX],
            "stage4_chef_prop_min":    CHEF_KNIFE_PROP_MIN,
            "stage4_swiss_army_prop_max": SWISS_ARMY_PROP_MAX,
        },
        "next_steps": (
            ["Proceed to phaseB_resolve_v16.py with Victorinox as pivot",
             "Update topic_id_resolution_log_v0.16.csv Victorinox row: "
             "final_query_tier=PIVOT, acquisition_query=Victorinox, "
             "topic_id_resolution_stage='Phase A complete (PASS)'"]
            if all_pass else
            ["MANUAL INTERVENTION REQUIRED — see fallback steps below"]
        ),
    }

    out_path = PHASEA_DIR / "stage5_verdict.json"
    out_path.write_text(json.dumps(rec, indent=2, ensure_ascii=False))

    print()
    print(f"  Stage 2 stability:   {'PASS' if stability_ok else 'FAIL'}")
    print(f"  Stage 3 position:    {'PASS' if position_ok else 'FAIL'}")
    print(f"  Stage 4 adjacency:   {'PASS' if adjacency_ok else 'FAIL'}")
    print()
    print(f"  VERDICT: {verdict}")
    print(f"  Action:  {action}")
    print(f"  Panel impact: {cell_impact}")
    print()
    return rec


# ============================================================================
# Update topic_id_resolution_log_v0.16.csv pivot row
# ============================================================================

def update_topic_id_log(verdict_rec):
    if verdict_rec["verdict"] != "PASS":
        print("⚠️  FAIL verdict: NOT updating topic-ID log automatically.")
        print()
        print("Manual fallback steps (per pre-reg §6):")
        print(f"  1. Document Phase A failure in osf/v16/DEVIATIONS.md as Entry 3")
        print(f"     (cite stage1-5 JSON outputs in osf/v16/data/phaseA/)")
        print(f"  2. Edit topic_id_resolution_log_v0.16.csv:")
        print(f"     - Victorinox row: set role='pivot_failed', "
              f"final_query_tier='PIVOT_FAILED', notes append failure rationale")
        print(f"     - Wüsthof row: change role='panel' to role='pivot_primary', "
              f"final_query_tier='PIVOT'")
        print(f"  3. Update bundle composition in acquire_trends_v16.py "
              f"AND rescale_trends_v16.py:")
        print(f"     - Replace all 'Victorinox' with 'Wüsthof'")
        print(f"     - Remove Wüsthof from bundle 2 (it can't be both pivot and member)")
        print(f"     - Re-shuffle bundle 2 to fit remaining 4 German+ brands")
        print(f"  4. Update score_v16.py PIVOT constant: 'Victorinox' -> 'Wüsthof'")
        print(f"  5. Update phaseB_resolve_v16.py PIVOTS_CANONICAL")
        print(f"  6. Commit fallback activation with DEVIATIONS Entry 3")
        print(f"  7. Re-run Phase A with PRIMARY_PIVOT='Wüsthof' to validate fallback")
        print()
        return False

    print(f"Updating topic_id_resolution_log_v0.16.csv pivot row ({PRIMARY_PIVOT})...")
    rows = list(csv.DictReader(TOPIC_ID_CSV.open()))
    fieldnames = list(rows[0].keys())

    updated = False
    for r in rows:
        if r["brand_canonical"] == PRIMARY_PIVOT and r["role"] == "pivot_primary":
            r["final_query_tier"] = "PIVOT"
            r["acquisition_query"] = PRIMARY_PIVOT
            r["topic_id_resolution_stage"] = "Phase A complete (PASS)"
            existing_notes = r.get("notes", "") or ""
            verdict_note = (f"Phase A PASS: stability CV={verdict_rec['stage_results']['stage2_cv_pct']}%, "
                            f"position ratio={verdict_rec['stage_results']['stage3_pivot_to_ref_ratio']}, "
                            f"chef_prop={verdict_rec['stage_results']['stage4_chef_proportion']}")
            r["notes"] = f"{existing_notes} | {verdict_note}" if existing_notes else verdict_note
            updated = True
            break

    if not updated:
        print(f"  WARNING: pivot row not found in topic-ID log. Manual check needed.")
        return False

    with TOPIC_ID_CSV.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"  Updated: {TOPIC_ID_CSV}")
    return True


# ============================================================================
# Main
# ============================================================================

print("=" * 72)
print(f"v0.16 Phase A — Pivot Validation ({PRIMARY_PIVOT})")
print(f"Pre-reg: v0.16-prereg (commit 511e339)")
print(f"Session timestamp: {SESSION_TS}")
print(f"Stability window: {STABILITY_WINDOW}")
print("=" * 72)
print()

stage1 = run_stage1(PRIMARY_PIVOT)
stage2 = run_stage2(PRIMARY_PIVOT)
stage3 = run_stage3(PRIMARY_PIVOT, STAGE3_REFERENCE_BRANDS)
stage4 = run_stage4(PRIMARY_PIVOT, STAGE4_CHEF_KNIFE_TERM, STAGE4_SWISS_ARMY_TERM)
stage5 = run_stage5(stage1, stage2, stage3, stage4)

print()
update_ok = update_topic_id_log(stage5)
print()

print("=" * 72)
print("Phase A complete.")
print(f"  Outputs: {PHASEA_DIR}/")
print(f"  stage1_suggestions.json, stage2_baseline.json,")
print(f"  stage3_bundle_position.json, stage4_adjacency.json,")
print(f"  stage5_verdict.json")
print()
if stage5["verdict"] == "PASS":
    print("Next: python3 ~/aias/scripts/phaseB_resolve_v16.py")
else:
    print("BLOCKED on manual fallback activation. See instructions above.")
    print("DO NOT run phaseB_resolve_v16.py until Wüsthof fallback is activated.")
print("=" * 72)
