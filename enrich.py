"""
v0.8 Enrichment Orchestrator
============================

Reads a raw measurement CSV (results_v2_*.csv) and writes the canonical
enriched CSV (results_enriched_*.csv) with brand-mention extraction applied.

Schema follows protocol §4.4 (v0.6 canonical 20-column convention):
    timestamp, [category,] methodology_version, prompt_set_version,
    brand_registry_version, prompt_id, cep, model_slot, provider,
    model_version, temperature, run_idx, call_status, attempts,
    elapsed_sec, raw_response, brands_canonical, brands_unknown,
    brands_ranked, primary_recommendation, sentiment_summary,
    extraction_method

Pipe-separated formats per protocol §4.4:
    brands_canonical:        "Wüsthof|Henckels|Shun"
    brands_unknown:          "Mizuno Pro|Hattori"   (mentions whose canonical mapping is None)
    brands_ranked:           "Wüsthof@1|Henckels@2|Shun@3"
    sentiment_summary:       "pos:7|neu:3|neg:1"

Closes the protocol §5.1 known artifact. The extractor library
(extractor.py) was always category-agnostic — what was hardcoded was
the calling pattern. This orchestrator passes the per-category
description sourced from the registry's category field, so the
extractor's system prompt is correctly scoped per run.

Usage:
  python enrich.py --input data/knives/results_v2_knives_v1.0_final.csv --category knives
  python enrich.py --input <path> --category <cat> --limit 10            # smoke test
"""

import os, sys, csv, json, argparse, time
from pathlib import Path
from datetime import datetime
from collections import Counter
from dotenv import load_dotenv

from extractor import extract_brands
from run_aias_v2 import load_category_files

load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_API_KEY")


def category_to_description(category_field: str) -> str:
    """Convert canonical category field to human-readable description for the extractor system prompt.

    The registry's `category` field is canonical snake_case (v1.1 schema) or
    Title Case display strings (v0.6 schema). Both convert cleanly to a
    natural-language description by lowercasing and replacing underscores.

    Examples:
      'premium_kitchen_knives'    -> 'premium kitchen knives'
      'household_goods_retail'    -> 'household goods retail'
      'Premium Olive Oil'         -> 'premium olive oil'
      'premium_facial_skincare'   -> 'premium facial skincare'
    """
    return category_field.lower().replace("_", " ").strip()


def aggregate_extractions(extractions: list) -> dict:
    """Roll the per-mention extraction list up into the v0.6 enriched-CSV columns.

    Dedupe by canonical name (a response naming "Shun" twice counts as one mention).
    Preserve order of first appearance.
    """
    if not extractions:
        return {
            "brands_canonical": "",
            "brands_unknown": "",
            "brands_ranked": "",
            "primary_recommendation": "",
            "sentiment_summary": "pos:0|neu:0|neg:0",
            "extraction_method": "",
        }

    seen_canonical = set()
    canonical_ordered = []
    ranked = []
    unknown_ordered = []
    primary = ""
    sentiment_counts = Counter()
    methods = set()

    for item in extractions:
        canon = item.get("canonical")
        raw = item.get("raw_mention", "")
        sent = item.get("sentiment", "neutral") or "neutral"
        rank = item.get("rank")
        is_primary = item.get("is_primary_recommendation", False)
        method = item.get("extraction_method", "")

        methods.add(method)

        if canon:
            if canon not in seen_canonical:
                seen_canonical.add(canon)
                canonical_ordered.append(canon)
                if rank is not None:
                    ranked.append(f"{canon}@{rank}")
                if is_primary and not primary:
                    primary = canon
            sentiment_counts[sent] += 1
        else:
            if raw and raw not in unknown_ordered:
                unknown_ordered.append(raw)

    return {
        "brands_canonical": "|".join(canonical_ordered),
        "brands_unknown": "|".join(unknown_ordered),
        "brands_ranked": "|".join(ranked),
        "primary_recommendation": primary,
        "sentiment_summary": (
            f"pos:{sentiment_counts.get('positive', 0)}|"
            f"neu:{sentiment_counts.get('neutral', 0)}|"
            f"neg:{sentiment_counts.get('negative', 0)}"
        ),
        "extraction_method": "|".join(sorted(methods)) if methods else "",
    }


def main():
    parser = argparse.ArgumentParser(
        description="v0.8 enrichment orchestrator — applies brand extraction to raw measurement CSVs.",
        epilog="Example: python enrich.py --input data/knives/results_v2_knives_v1.0_final.csv --category knives"
    )
    parser.add_argument("--input", required=True,
                        help="Path to raw CSV (results_v2_*.csv) from a measurement run")
    parser.add_argument("--category", required=True,
                        help="Category short name (must match registries/brands_<cat>.json)")
    parser.add_argument("--output-dir", default=None,
                        help="Override output directory (default: same dir as input)")
    parser.add_argument("--limit", type=int, default=None,
                        help="Limit number of rows to enrich (for smoke testing)")
    args = parser.parse_args()

    if not OPENAI_KEY:
        sys.exit("ERROR: OPENAI_API_KEY not set in .env")

    from openai import OpenAI
    client = OpenAI(api_key=OPENAI_KEY)

    input_path = Path(args.input)
    if not input_path.exists():
        sys.exit(f"ERROR: input file not found: {input_path}")

    output_dir = Path(args.output_dir) if args.output_dir else input_path.parent
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load category registry to get the category description string and the brand list
    brands, _, registry_version, _ = load_category_files(args.category)

    # Resolve category description from the registry's category field
    registry_path = Path("registries") / f"brands_{args.category}.json"
    with open(registry_path) as f:
        registry_raw = json.load(f)
    if isinstance(registry_raw, dict) and registry_raw.get("category"):
        category_desc = category_to_description(registry_raw["category"])
    else:
        category_desc = category_to_description(args.category)

    # Read raw CSV
    with open(input_path) as f:
        rows = list(csv.DictReader(f))
    if args.limit:
        rows = rows[:args.limit]

    print("=" * 78)
    print("v0.8 Enrichment Orchestrator")
    print(f"Input:               {input_path}")
    print(f"Rows:                {len(rows)}")
    print(f"Category:            {args.category}")
    print(f"Description (ext.):  '{category_desc}'")
    print(f"Registry version:    {registry_version}")
    print(f"Brands in registry:  {len(brands)}")
    print("=" * 78)

    enriched_rows = []
    extraction_method_counts = Counter()
    enrichment_errors = 0
    t_start = time.time()

    for i, row in enumerate(rows, 1):
        prompt_id = row.get("prompt_id", "?")
        slot = row.get("model_slot") or row.get("model", "?")
        call_status = row.get("call_status", "?")
        raw_response = (row.get("raw_response") or "").strip()

        if call_status != "ok" or not raw_response:
            agg = aggregate_extractions([])
            print(f"  [{i:3d}/{len(rows)}] {prompt_id:18s} | {slot:18s} -> skipped (status={call_status})")
        else:
            try:
                extractions = extract_brands(raw_response, brands, client, category_desc)
                agg = aggregate_extractions(extractions)
                method = agg["extraction_method"] or "unknown"
                extraction_method_counts[method] += 1
                n_brands = len(agg["brands_canonical"].split("|")) if agg["brands_canonical"] else 0
                n_unknown = len(agg["brands_unknown"].split("|")) if agg["brands_unknown"] else 0
                print(f"  [{i:3d}/{len(rows)}] {prompt_id:18s} | {slot:18s} -> "
                      f"brands={n_brands}, unknown={n_unknown} ({method})")
            except Exception as e:
                enrichment_errors += 1
                agg = aggregate_extractions([])
                agg["extraction_method"] = f"error: {type(e).__name__}"
                print(f"  [{i:3d}/{len(rows)}] {prompt_id:18s} | {slot:18s} -> ERROR: {type(e).__name__}: {str(e)[:80]}")

        # Merge raw row + enriched columns
        enriched_row = dict(row)
        enriched_row.update(agg)
        enriched_rows.append(enriched_row)

    elapsed = time.time() - t_start

    # Write enriched CSV
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = output_dir / f"results_enriched_{args.category}_{timestamp}.csv"

    # Column order: original CSV columns + new enrichment columns
    base_cols = list(rows[0].keys()) if rows else []
    new_cols = ["brands_canonical", "brands_unknown", "brands_ranked",
                "primary_recommendation", "sentiment_summary", "extraction_method"]
    # Avoid duplicates if an old enriched CSV is being re-enriched
    final_cols = base_cols + [c for c in new_cols if c not in base_cols]

    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=final_cols, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(enriched_rows)

    # ----- Summary -----
    rows_with_brands = sum(1 for r in enriched_rows if r.get("brands_canonical"))
    rows_with_unknowns = sum(1 for r in enriched_rows if r.get("brands_unknown"))
    rows_with_primary = sum(1 for r in enriched_rows if r.get("primary_recommendation"))

    # Aggregate brand-mention counts across the dataset
    all_canonical = []
    all_unknown = []
    for r in enriched_rows:
        if r.get("brands_canonical"):
            all_canonical.extend(r["brands_canonical"].split("|"))
        if r.get("brands_unknown"):
            all_unknown.extend(r["brands_unknown"].split("|"))

    canonical_freq = Counter(all_canonical)
    unknown_freq = Counter(all_unknown)

    print()
    print("=" * 78)
    print(f"Enrichment complete in {elapsed:.1f}s")
    print(f"Output: {out_path}")
    print()
    print(f"Per-row stats:")
    print(f"  Rows with at least one canonical brand: {rows_with_brands}/{len(enriched_rows)}")
    print(f"  Rows with at least one unknown mention: {rows_with_unknowns}/{len(enriched_rows)}")
    print(f"  Rows with a primary recommendation:     {rows_with_primary}/{len(enriched_rows)}")
    print(f"  Enrichment errors:                      {enrichment_errors}")
    print()
    print(f"Extraction method usage:")
    for method, n in extraction_method_counts.most_common():
        print(f"  {method:25s}  n={n}")
    print()
    print(f"Top 15 canonical brands surfaced (mention count, deduped per response):")
    for brand, n in canonical_freq.most_common(15):
        pct = 100 * n / len(enriched_rows) if enriched_rows else 0
        print(f"  {brand:30s}  n={n:4d}  ({pct:5.1f}% of responses)")
    print()
    if unknown_freq:
        print(f"Top 15 unknown mentions (review for §2.4 registry-revision protocol):")
        for raw, n in unknown_freq.most_common(15):
            print(f"  {raw:40s}  n={n}")
    else:
        print("No unknown mentions surfaced — registry coverage looks complete.")
    print("=" * 78)


if __name__ == "__main__":
    main()
