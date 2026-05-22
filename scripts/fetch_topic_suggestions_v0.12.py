"""Phase B - Fetch Google Trends entity suggestions for v0.12.

Resolves pytrends.suggestions() candidates for the 26 non-pivot matched-subset
brands across olive oil and running shoes. The two pivots (California Olive
Ranch /g/11cn92g97s and Asics /m/04xxy1) are already validated in Phase A and
are skipped here.

PM software brands are not re-resolved: their tier assignments and topic-mids
are replicated verbatim from v0.11 PRE_REGISTRATION.md §5.2.1.

Forked from scripts/fetch_topic_suggestions.py (v0.11).

Run:
    pip install pytrends
    python scripts/fetch_topic_suggestions_v0.12.py
"""
import json
import time
from datetime import datetime, timezone
from pathlib import Path

from pytrends.request import TrendReq

# (canonical_name, category, market_tier, search_input).
# search_input includes disambiguating hints for high-noise brands (matches
# the fallback_query_term in trends_query_strings_v0.12.json).
BRANDS = [
    # Olive oil — 14 non-pivot brands (California Olive Ranch excluded as Phase A pivot)
    ("Bertolli",              "oliveoil", "incumbent",  "Bertolli olive oil"),
    ("Brightland",            "oliveoil", "challenger", "Brightland"),
    ("Castillo de Canena",    "oliveoil", "mid-tier",   "Castillo de Canena"),
    ("Cobram Estate",         "oliveoil", "incumbent",  "Cobram Estate"),
    ("Colonna",               "oliveoil", "mid-tier",   "Marina Colonna olive oil"),
    ("Frantoio Muraglia",     "oliveoil", "mid-tier",   "Frantoio Muraglia"),
    ("Frescobaldi Laudemio",  "oliveoil", "challenger", "Frescobaldi Laudemio"),
    ("Graza",                 "oliveoil", "challenger", "Graza"),
    ("Kosterina",             "oliveoil", "challenger", "Kosterina"),
    ("Lucini",                "oliveoil", "mid-tier",   "Lucini olive oil"),
    ("Manni",                 "oliveoil", "mid-tier",   "Manni olive oil"),
    ("McEvoy Ranch",          "oliveoil", "mid-tier",   "McEvoy Ranch"),
    ("Núñez de Prado",        "oliveoil", "challenger", "Nunez de Prado"),
    ("Olio Verde",            "oliveoil", "challenger", "Olio Verde Becchina"),
    # Running — 12 non-pivot brands (Asics excluded as Phase A pivot)
    ("Adidas",                "running",  "incumbent",  "Adidas running shoes"),
    ("Altra",                 "running",  "challenger", "Altra running shoes"),
    ("Brooks",                "running",  "incumbent",  "Brooks running shoes"),
    ("Hoka",                  "running",  "challenger", "Hoka"),
    ("New Balance",           "running",  "incumbent",  "New Balance shoes"),
    ("Nike",                  "running",  "incumbent",  "Nike running shoes"),
    ("Norda",                 "running",  "challenger", "Norda"),
    ("On",                    "running",  "challenger", "On Cloud running shoes"),
    ("Puma",                  "running",  "mid-tier",   "Puma running shoes"),
    ("Salomon",               "running",  "challenger", "Salomon running shoes"),
    ("Saucony",               "running",  "mid-tier",   "Saucony"),
    ("Topo Athletic",         "running",  "challenger", "Topo Athletic"),
]

pytrends = TrendReq(hl="en-US", tz=0)
fetched_at = datetime.now(timezone.utc).isoformat()

results = {}
print(f"# Trends entity suggestions for v0.12, fetched {fetched_at}")
print(f"# {len(BRANDS)} brands across 2 categories (pivots excluded)")
print()

for canonical, category, market_tier, search_input in BRANDS:
    print(f"=== {canonical} [{category}] ({market_tier}) ===")
    print(f"Search input: {search_input!r}")
    try:
        suggestions = pytrends.suggestions(keyword=search_input)
        results[canonical] = {
            "category": category,
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
            "category": category,
            "market_tier": market_tier,
            "search_input": search_input,
            "error": str(e),
        }
    print()
    time.sleep(2)  # avoid rate limits

# Save raw results for the deposit.
out_dir = Path.home() / "aias" / "osf" / "v12" / "data" / "phaseB_suggestions"
out_dir.mkdir(parents=True, exist_ok=True)
safe_ts = fetched_at.replace(":", "-")
out_path = out_dir / f"trends_suggestions_v0.12_{safe_ts}.json"
out_path.write_text(json.dumps({"fetched_at": fetched_at, "results": results}, indent=2,
                                ensure_ascii=False))
print(f"# Raw saved to: {out_path}")
print()
print("# Done. Paste the suggestions output above to Claude, who will help")
print("# you fill in topic_id_resolution_log_v0.12.csv with the chosen mids.")
