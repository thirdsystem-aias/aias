"""Phase B retry - Re-fetch Trends entity suggestions for 5 brands using
domain-style search inputs.

Run after fetch_topic_suggestions.py for the 5 brands where the first pass
returned only noise. Domain-style inputs (e.g. 'linear.app', 'coda.io')
often surface entities the bare brand name doesn't.

Run:
    python scripts/fetch_topic_suggestions_retry.py
"""
import json
import time
from datetime import datetime, timezone
from pathlib import Path

from pytrends.request import TrendReq

# (canonical_name, market_tier, retry_search_input).
BRANDS_RETRY = [
    ("Coda",      "mid-tier",   "coda.io"),
    ("Linear",    "challenger", "linear.app"),
    ("Height",    "challenger", "height.app"),
    ("Motion",    "challenger", "usemotion"),
    ("Shortcut",  "challenger", "shortcut.com"),
]

pytrends = TrendReq(hl="en-US", tz=0)
fetched_at = datetime.now(timezone.utc).isoformat()

results = {}
print(f"# Trends entity suggestions (RETRY), fetched {fetched_at}")
print()

for canonical, market_tier, search_input in BRANDS_RETRY:
    print(f"=== {canonical} ({market_tier}) [retry] ===")
    print(f"Search input: {search_input!r}")
    try:
        suggestions = pytrends.suggestions(keyword=search_input)
        results[canonical] = {
            "market_tier": market_tier,
            "search_input": search_input,
            "suggestions": suggestions,
        }
        if not suggestions:
            print("(no suggestions returned)")
        else:
            for i, s in enumerate(suggestions, 1):
                mid = s.get("mid", "")
                title = s.get("title", "")
                stype = s.get("type", "")
                print(f"  {i}. {mid}  -  {title}  -  {stype}")
    except Exception as e:
        print(f"ERROR: {e}")
        results[canonical] = {
            "market_tier": market_tier,
            "search_input": search_input,
            "error": str(e),
        }
    print()
    time.sleep(2)

out_dir = Path.home() / "aias" / "osf" / "v11" / "data" / "phaseB_suggestions"
out_dir.mkdir(parents=True, exist_ok=True)
safe_ts = fetched_at.replace(":", "-")
out_path = out_dir / f"trends_suggestions_retry_{safe_ts}.json"
out_path.write_text(json.dumps({"fetched_at": fetched_at, "results": results}, indent=2))
print(f"# Raw saved to: {out_path}")
print("# Done. Paste the output above to Claude.")
