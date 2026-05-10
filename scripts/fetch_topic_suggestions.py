"""Phase B - Fetch Google Trends entity suggestions for all 14 v0.11 brands.

Uses pytrends.suggestions(), which queries Google's own autocomplete/entity
endpoint. Output is the structured equivalent of the Trends UI dropdown.

Run:
    pip install pytrends
    python scripts/fetch_topic_suggestions.py
"""
import json
import time
from datetime import datetime, timezone
from pathlib import Path

from pytrends.request import TrendReq

# (canonical_name, market_tier, search_input).
# Search input includes disambiguating hints for high-noise brands.
BRANDS = [
    ("Monday",          "incumbent",  "Monday.com"),
    ("Jira",            "incumbent",  "Jira"),
    ("Trello",          "incumbent",  "Trello"),
    ("Confluence",      "incumbent",  "Confluence"),
    ("Notion",          "mid-tier",   "Notion"),
    ("ClickUp",         "mid-tier",   "ClickUp"),
    ("Smartsheet",      "mid-tier",   "Smartsheet"),
    ("Airtable",        "mid-tier",   "Airtable"),
    ("Basecamp",        "mid-tier",   "Basecamp"),
    ("Coda",            "mid-tier",   "Coda"),
    ("Linear",          "challenger", "Linear app"),
    ("Height",          "challenger", "Height app"),
    ("Motion",          "challenger", "Motion app"),
    ("Shortcut",        "challenger", "Shortcut"),
]

pytrends = TrendReq(hl="en-US", tz=0)
fetched_at = datetime.now(timezone.utc).isoformat()

results = {}
print(f"# Trends entity suggestions, fetched {fetched_at}")
print()

for canonical, market_tier, search_input in BRANDS:
    print(f"=== {canonical} ({market_tier}) ===")
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
    time.sleep(2)  # avoid rate limits

# Save raw results for the deposit.
out_dir = Path.home() / "aias" / "osf" / "v11" / "data" / "phaseB_suggestions"
out_dir.mkdir(parents=True, exist_ok=True)
safe_ts = fetched_at.replace(":", "-")
out_path = out_dir / f"trends_suggestions_{safe_ts}.json"
out_path.write_text(json.dumps({"fetched_at": fetched_at, "results": results}, indent=2))
print(f"# Raw saved to: {out_path}")
print("# Done. Paste the output above (from the first '===' to here) to Claude.")
