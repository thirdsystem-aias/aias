"""
v0.8 Unknowns Classifier
========================

Categorizes each unique entry in the brands_unknown column of the enriched
CSV into a structured taxonomy. Powers the H7 reframed scoring (authority-
naming within mixed-mode responses) and produces a registry-revision
diagnostic for future iterations.

Taxonomy:
  - knife_brand           Kitchen / EDC / outdoor knife maker not in registry
  - publication           Magazine, blog, review site (Cook's Illustrated, Wirecutter)
  - retailer              Store or e-commerce site (Williams-Sonoma, Sur La Table)
  - community             Forum, subreddit, YouTube channel, social network
  - product_term          Steel type, technique, knife type (VG-10, Gyuto, Damascus)
  - other                 Anything else (countries, materials, etc.)

Plus per-entry:
  - english_language      true | false | unclear
  - description           1-line gloss

Usage:
  python classify_unknowns.py --input data/knives/results_enriched_<ts>.csv

Output:
  data/knives/unknowns_classified_<ts>.csv with one row per UNIQUE unknown:
    canonical, primary_type, english_language, total_mentions, description
"""

import os, sys, csv, json, argparse
from pathlib import Path
from datetime import datetime
from collections import Counter
from dotenv import load_dotenv

load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

CLASSIFIER_MODEL = "gpt-5.4-mini"
CLASSIFIER_TEMPERATURE = 0


CLASSIFY_TOOL = {
    "type": "function",
    "function": {
        "name": "classify_unknown_mention",
        "description": "Classify an entity name from a kitchen-knife discussion context.",
        "parameters": {
            "type": "object",
            "properties": {
                "primary_type": {
                    "type": "string",
                    "enum": ["knife_brand", "publication", "retailer", "community",
                             "smith", "product_term", "other"],
                    "description": (
                        "knife_brand: kitchen/EDC/outdoor knife maker; "
                        "publication: magazine/blog/review site; "
                        "retailer: store or e-commerce site; "
                        "community: forum, subreddit, YouTube channel, social network; "
                        "smith: individual bladesmith (rather than a brand); "
                        "product_term: steel type, blade style, technique, technical term; "
                        "other: anything else (country, material, person, etc.)"
                    )
                },
                "english_language": {
                    "type": "string",
                    "enum": ["english", "non_english", "unclear"],
                    "description": (
                        "Is this entity primarily English-language in its outward marketing/branding? "
                        "Cook's Illustrated = english. Williams-Sonoma = english. "
                        "A Japanese knife maker with no major English presence = non_english. "
                        "Use 'unclear' only when the entity name is generic or you don't recognize it."
                    )
                },
                "description": {
                    "type": "string",
                    "description": "One-line gloss of what this entity is. Helps audit the classification."
                }
            },
            "required": ["primary_type", "english_language", "description"]
        }
    }
}


SYSTEM_PROMPT = """You are classifying entity names that surfaced in AI-generated text about premium kitchen knives.

Each name is a string the AI mentioned in a knife-discussion context. Your job is to identify what kind of entity it refers to and whether it is primarily English-language.

Examples for calibration:

ENTITIES:
  "Wirecutter" -> publication, english, "NYT product review site"
  "Williams-Sonoma" -> retailer, english, "US kitchen retailer"
  "r/chefknives" -> community, english, "Reddit knife community"
  "America's Test Kitchen" -> publication, english, "US cooking media brand"
  "Korin" -> retailer, english, "NYC Japanese knife retailer (English-language operations)"
  "Takeda" -> knife_brand, non_english, "Japanese knife maker (Niimi)"
  "Yoshikane" -> knife_brand, non_english, "Japanese knife maker (Sanjo)"
  "Bestech" -> knife_brand, english, "Chinese knife brand with English marketing"
  "VG-10" -> product_term, english, "Japanese stainless steel grade"
  "Gyuto" -> product_term, english, "Japanese chef knife style"
  "Bob Kramer" -> smith, english, "American bladesmith (now distributed by Zwilling)"
  "Damascus" -> product_term, english, "Pattern-welded steel finish"

If a known knife brand has both Japanese identity and meaningful English-language marketing/distribution presence (e.g., Shun, Global, Miyabi), classify as knife_brand with english_language=english. If its outward marketing is primarily Japanese-language even though the brand is known to enthusiasts, classify as non_english.

Be honest about uncertainty: use 'unclear' for english_language only when you genuinely cannot tell.

Output the classification using the classify_unknown_mention function."""


def classify_one(client, name):
    completion = client.chat.completions.create(
        model=CLASSIFIER_MODEL,
        temperature=CLASSIFIER_TEMPERATURE,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Classify: {name}"},
        ],
        tools=[CLASSIFY_TOOL],
        tool_choice={"type": "function", "function": {"name": "classify_unknown_mention"}},
    )
    tool_call = completion.choices[0].message.tool_calls[0]
    return json.loads(tool_call.function.arguments)


def main():
    parser = argparse.ArgumentParser(description="Classify brands_unknown entries from enriched CSV")
    parser.add_argument("--input", required=True, help="Path to enriched CSV (results_enriched_*.csv)")
    parser.add_argument("--output-dir", default=None, help="Output directory (default: same as input)")
    parser.add_argument("--min-count", type=int, default=1,
                        help="Only classify unknowns with >= this many mentions (default 1, all)")
    args = parser.parse_args()

    if not OPENAI_KEY:
        sys.exit("ERROR: OPENAI_API_KEY not set in .env")

    from openai import OpenAI
    client = OpenAI(api_key=OPENAI_KEY)

    input_path = Path(args.input)
    if not input_path.exists():
        sys.exit(f"ERROR: input not found: {input_path}")

    output_dir = Path(args.output_dir) if args.output_dir else input_path.parent
    output_dir.mkdir(parents=True, exist_ok=True)

    rows = list(csv.DictReader(open(input_path)))

    # Aggregate brands_unknown across all rows
    counts = Counter()
    for r in rows:
        unknowns = (r.get("brands_unknown") or "").split("|")
        for u in unknowns:
            u_clean = u.strip()
            if u_clean:
                counts[u_clean] += 1

    # Filter by min-count
    targets = [(name, n) for name, n in counts.most_common() if n >= args.min_count]

    print("=" * 78)
    print("v0.8 Unknowns Classifier")
    print(f"Input:           {input_path}")
    print(f"Total rows:      {len(rows)}")
    print(f"Unique unknowns: {len(counts)}")
    print(f"Targets (>= {args.min_count} mentions): {len(targets)}")
    print(f"Model:           {CLASSIFIER_MODEL} (temperature={CLASSIFIER_TEMPERATURE})")
    print("=" * 78)

    classified = []
    for i, (name, n) in enumerate(targets, 1):
        try:
            result = classify_one(client, name)
            classified.append({
                "canonical": name,
                "total_mentions": n,
                "primary_type": result["primary_type"],
                "english_language": result["english_language"],
                "description": result["description"],
            })
            print(f"  [{i:3d}/{len(targets)}] {name:30s} n={n:4d} -> "
                  f"{result['primary_type']:14s} {result['english_language']:11s} | {result['description'][:60]}")
        except Exception as e:
            classified.append({
                "canonical": name,
                "total_mentions": n,
                "primary_type": "ERROR",
                "english_language": "unclear",
                "description": f"Classifier failed: {type(e).__name__}: {str(e)[:100]}",
            })
            print(f"  [{i:3d}/{len(targets)}] {name:30s} n={n:4d} -> ERROR: {e}")

    # Output
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = output_dir / f"unknowns_classified_{timestamp}.csv"
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["canonical", "total_mentions", "primary_type",
                        "english_language", "description"]
        )
        writer.writeheader()
        writer.writerows(classified)

    # Summary tables
    print()
    print("=" * 78)
    print("Distribution by primary_type:")
    type_counts = Counter()
    type_mentions = Counter()
    for c in classified:
        type_counts[c["primary_type"]] += 1
        type_mentions[c["primary_type"]] += c["total_mentions"]
    for t in sorted(type_counts.keys()):
        print(f"  {t:14s}  unique={type_counts[t]:4d}  total_mentions={type_mentions[t]:5d}")

    print()
    print("Authority-class entities (publication + retailer + community):")
    auth_classes = {"publication", "retailer", "community"}
    auth_total = sum(c["total_mentions"] for c in classified if c["primary_type"] in auth_classes)
    auth_english = sum(c["total_mentions"] for c in classified
                       if c["primary_type"] in auth_classes and c["english_language"] == "english")
    auth_non_english = sum(c["total_mentions"] for c in classified
                           if c["primary_type"] in auth_classes and c["english_language"] == "non_english")
    auth_unclear = sum(c["total_mentions"] for c in classified
                       if c["primary_type"] in auth_classes and c["english_language"] == "unclear")
    print(f"  Total authority mentions:    {auth_total}")
    print(f"    english:                   {auth_english} ({100*auth_english/auth_total:.1f}%)" if auth_total else "    no authorities found")
    print(f"    non_english:               {auth_non_english} ({100*auth_non_english/auth_total:.1f}%)" if auth_total else "")
    print(f"    unclear:                   {auth_unclear} ({100*auth_unclear/auth_total:.1f}%)" if auth_total else "")

    print()
    print("Top 15 authority-class entities:")
    auth_entities = sorted(
        [c for c in classified if c["primary_type"] in auth_classes],
        key=lambda c: -c["total_mentions"]
    )
    for c in auth_entities[:15]:
        print(f"  {c['canonical']:35s}  n={c['total_mentions']:3d}  {c['primary_type']:12s}  {c['english_language']}")

    print()
    print("Top 15 knife_brand unknowns (registry-revision candidates):")
    brand_unknowns = sorted(
        [c for c in classified if c["primary_type"] == "knife_brand"],
        key=lambda c: -c["total_mentions"]
    )
    for c in brand_unknowns[:15]:
        print(f"  {c['canonical']:35s}  n={c['total_mentions']:3d}  {c['english_language']}")

    print()
    print(f"Output: {out_path}")
    print("=" * 78)


if __name__ == "__main__":
    main()
