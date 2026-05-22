"""Phase A - SerpAPI pivot-brand verification for v0.12.

Verifies that a pivot brand's topic mid returns a non-zero, non-flat
Trends timeseries across the combined v0.11/v0.12 14-day wave window
(2026-04-27 to 2026-05-10).

Forked from scripts/test_serpapi_topic.py (v0.11) with:
  - CLI args (brand name positional + --mid)
  - --resolve mode: print pytrends.suggestions() candidates and exit
  - CV-based stability check (>50% CV invokes secondary-pivot rule per
    v0.12 PRE_REGISTRATION.md §5.1)
  - Output to ~/aias/osf/v12/data/phaseA_test/

Two-step workflow per pivot:

    # Step 1: resolve topic mid candidates
    python scripts/phaseA_pivot_check_v0.12.py "California Olive Ranch" --resolve

    # Step 2: run Phase A with the chosen mid
    export SERPAPI_KEY="your_serpapi_key_here"
    python scripts/phaseA_pivot_check_v0.12.py "California Olive Ranch" --mid /m/XXXXXX

Repeat for Asics. (Asana already verified at v0.11; no re-run needed.)
"""
import argparse
import json
import os
import re
import statistics
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

import requests

# v0.11 / v0.12 combined wave window
WINDOW_START = "2026-04-27"
WINDOW_END = "2026-05-10"
WINDOW_LITERAL = f"{WINDOW_START} {WINDOW_END}"

# Pre-reg §5.1: pivot stability threshold
MAX_CV_PCT = 50.0

# SerpAPI
ENDPOINT = "https://serpapi.com/search"

OUT_DIR = Path.home() / "aias" / "osf" / "v12" / "data" / "phaseA_test"


def slugify(name: str) -> str:
    """Brand name -> filesystem-safe slug."""
    normalised = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "_", normalised.lower()).strip("_")


def resolve_mid(brand: str) -> None:
    """Print pytrends.suggestions() candidates for the brand and exit."""
    try:
        from pytrends.request import TrendReq
    except ImportError:
        sys.exit("ERROR: pytrends not installed. Run: pip install pytrends")
    pytrends = TrendReq(hl="en-US", tz=420)
    suggestions = pytrends.suggestions(keyword=brand)
    if not suggestions:
        sys.exit(f"No suggestions returned for {brand!r}.")
    print(f"\npytrends.suggestions() candidates for {brand!r}:\n")
    for i, s in enumerate(suggestions, 1):
        print(f"  {i}. mid={s.get('mid')}")
        print(f"     title={s.get('title')}")
        print(f"     type={s.get('type')}")
        print()
    print("Pick the candidate that matches the brand-as-marketed entity in the")
    print("relevant category, then re-run with --mid <chosen-mid>.\n")


def phaseA_test(brand: str, mid: str) -> None:
    api_key = os.environ.get("SERPAPI_KEY")
    if not api_key:
        sys.exit("ERROR: SERPAPI_KEY not set. Run: export SERPAPI_KEY=your_key")

    params = {
        "engine": "google_trends",
        "q": mid,
        "data_type": "TIMESERIES",
        "date": WINDOW_LITERAL,
        "geo": "",  # worldwide
        "no_cache": "true",
        "api_key": api_key,
    }

    fetched_at = datetime.now(timezone.utc).isoformat()
    print(f"Hitting SerpAPI at {fetched_at}...")
    print(f"Brand:     {brand}")
    print(f"Topic mid: {mid}")
    print(f"Window:    {WINDOW_LITERAL}")
    print()

    try:
        response = requests.get(ENDPOINT, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
    except requests.HTTPError:
        print(f"ERROR: HTTP {response.status_code}")
        try:
            print(f"Response body: {response.text[:500]}")
        except Exception:
            pass
        sys.exit(1)
    except Exception as e:
        sys.exit(f"ERROR: API call failed: {e}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    safe_ts = fetched_at.replace(":", "-")
    out_path = OUT_DIR / f"{slugify(brand)}_topic_test_{safe_ts}.json"
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

    sp = data.get("search_parameters", {})
    print(f"Engine echoed:    {sp.get('engine')}")
    print(f"Query echoed:     {sp.get('q')}")
    print(f"Data type:        {sp.get('data_type')}")
    print(f"Geo:              {sp.get('geo') or '(worldwide)'}")
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

    mean = sum(values) / len(values)
    stdev = statistics.stdev(values) if len(values) > 1 else 0.0
    cv_pct = (stdev / mean * 100.0) if mean > 0 else float("inf")

    print(f"First point: date={timeline[0].get('date')}, value={values[0]}")
    print(f"Last point:  date={timeline[-1].get('date')}, value={values[-1]}")
    print(f"Range: min={min(values)}, max={max(values)}")
    print(f"Mean:  {mean:.1f}")
    print(f"Stdev: {stdev:.1f}")
    print(f"CV:    {cv_pct:.1f}%  (threshold for secondary-pivot rule: {MAX_CV_PCT}%)")
    print()

    if all(v == 0 for v in values):
        print("FAIL: all values are zero - topic mid may be treated as literal string.")
        sys.exit(1)
    elif len(set(values)) == 1:
        print(f"FAIL: all values identical ({values[0]}). Suspicious; investigate.")
        sys.exit(1)
    elif cv_pct > MAX_CV_PCT:
        print(f"FAIL: CV {cv_pct:.1f}% exceeds {MAX_CV_PCT}% threshold.")
        print("Per v0.12 PRE_REGISTRATION.md §5.1, invoke secondary-pivot-selection rule")
        print("and document in /v12/DEVIATIONS.md before re-running.")
        sys.exit(1)
    else:
        print("PASS - pivot is non-zero, non-flat, and within stability threshold.")


def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("brand", help="Brand name (e.g. 'California Olive Ranch')")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--mid", help="Topic mid (e.g. '/m/0c3z_p8') to run Phase A with")
    g.add_argument("--resolve", action="store_true",
                   help="Print pytrends.suggestions() candidates and exit")
    args = p.parse_args()

    if args.resolve:
        resolve_mid(args.brand)
    else:
        phaseA_test(args.brand, args.mid)


if __name__ == "__main__":
    main()
