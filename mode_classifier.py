"""
v0.8 Mode Classifier
====================

Classifies each AI response in the v0.8 knives dataset along the response-mode
axis defined in AIAS Presence Measurement Protocol v1.1 §3.4 (the three modes
of AI response).

Methodologically parallel to v0.7's manual_review_bbb.py (which classified
phantom-brand mentions on the valence + entity-reference axes). v0.8 needs a
different taxonomy because Pattern 4 (discourse-language bias) is not about
how the AI handles a brand it knows, but about whether the AI surfaces brands
at all vs falling back to component or authority framings.

Modes:
  - brand      AI names brands within the category as the answer
  - component  AI names materials/steel types/blade properties instead of brands
  - authority  AI names publications/retailers/communities instead of brands
  - mixed      meaningful blend of two or more modes
  - refusal    AI declines to recommend specific brands

The mode classification is required for scoring two pre-registered hypotheses:
  - H4 (Japanese aggregate peaks in p3) is uninterpretable if p3 goes
    component-mode. Conditioning on brand-mode-only p3 responses is the
    pre-registered mitigation.
  - H7 (English-language authority dominance) requires explicit identification
    of authority-mode responses for the denominator.

Usage:
  python mode_classifier.py --input data/knives/results_enriched_<ts>.csv
  python mode_classifier.py --input <path> --limit 10            # smoke test
  python mode_classifier.py --input <path> --audit-sample 25     # default
"""

import os, sys, json, csv, argparse, random
from pathlib import Path
from datetime import datetime
from collections import Counter
from dotenv import load_dotenv

load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

CLASSIFIER_MODEL = "gpt-5.4-mini"
CLASSIFIER_TEMPERATURE = 0

# ---------------------------------------------------------------------------
# Function-calling schema
# ---------------------------------------------------------------------------
CLASSIFY_TOOL = {
    "type": "function",
    "function": {
        "name": "classify_response_mode",
        "description": "Classify the dominant response mode of an AI response to a category-relevant question. Mode taxonomy per AIAS Presence Measurement Protocol v1.1 §3.4.",
        "parameters": {
            "type": "object",
            "properties": {
                "primary_mode": {
                    "type": "string",
                    "enum": ["brand", "component", "authority", "mixed", "refusal"],
                    "description": "The dominant mode of the response."
                },
                "secondary_mode": {
                    "type": "string",
                    "enum": ["brand", "component", "authority", "none"],
                    "description": "Secondary mode if primary_mode is 'mixed', else 'none'."
                },
                "brand_mentions_count": {
                    "type": "integer",
                    "description": "Approximate count of distinct knife brands named in the response (e.g., Wüsthof, Henckels, Shun, Global)."
                },
                "component_terms_count": {
                    "type": "integer",
                    "description": "Approximate count of distinct material/property/specification terms named (e.g., 'VG-10 steel', 'high-carbon', 'full tang', 'single bevel', 'Damascus', 'Rockwell hardness')."
                },
                "authority_mentions_count": {
                    "type": "integer",
                    "description": "Approximate count of distinct publications, retailers, online communities, or competitions named (e.g., \"Cook's Illustrated\", 'Williams-Sonoma', 'r/chefknives', \"America's Test Kitchen\")."
                },
                "rationale": {
                    "type": "string",
                    "description": "Brief explanation (1-2 sentences) of why this classification was chosen."
                }
            },
            "required": ["primary_mode", "secondary_mode", "brand_mentions_count",
                         "component_terms_count", "authority_mentions_count", "rationale"]
        }
    }
}

CLASSIFIER_SYSTEM_PROMPT = """You are classifying the dominant response mode of an AI's reply to a question about premium kitchen knives.

The three modes per the AIAS Presence Measurement Protocol §3.4:

1. **brand** — the AI names knife brands as the answer (e.g., Wüsthof, Henckels, Shun, Global, Mac, Tojiro, Misono, Cutco, Misen, Lamson, Victorinox).

2. **component** — the AI names materials, steel types, blade properties, or specifications instead of brands (e.g., "high-carbon stainless steel", "VG-10", "Damascus", "single bevel", "full tang", "Rockwell hardness 60+", "AUS-10", "Aogami"). The answer is in the form of what to LOOK FOR, not which BRAND to buy.

3. **authority** — the AI names publications, retailers, online communities, or competitions instead of brands (e.g., "Cook's Illustrated recommends...", "Williams-Sonoma carries...", "r/chefknives", "America's Test Kitchen", "Serious Eats"). The answer redirects to where to look rather than what to buy.

Use **mixed** when the response substantively combines two or more modes with no clear dominance (e.g., a paragraph naming brands AND a paragraph describing steel properties, with neither dominating).

Use **refusal** when the AI explicitly declines to recommend specific knives without redirecting to component or authority frames (e.g., "I can't recommend specific brands without more information").

Important: brief mentions of one mode within an answer dominated by another do NOT make the response mixed. A primarily-brand answer that briefly mentions "VG-10 steel" or "Williams-Sonoma carries it" is still primary_mode='brand'. Only classify as mixed if the modes are substantively co-equal.

Output the structured classification using the classify_response_mode function."""


# ---------------------------------------------------------------------------
# Classifier
# ---------------------------------------------------------------------------
def classify_one(client, raw_response: str, prompt_id: str, cep: str) -> dict:
    """Classify a single response. Returns the classification dict, or raises."""
    user_msg = (
        f"PROMPT_ID: {prompt_id}\n"
        f"CEP: {cep}\n\n"
        f"RESPONSE TO CLASSIFY:\n{raw_response}"
    )
    completion = client.chat.completions.create(
        model=CLASSIFIER_MODEL,
        temperature=CLASSIFIER_TEMPERATURE,
        messages=[
            {"role": "system", "content": CLASSIFIER_SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
        ],
        tools=[CLASSIFY_TOOL],
        tool_choice={"type": "function", "function": {"name": "classify_response_mode"}},
    )
    tool_call = completion.choices[0].message.tool_calls[0]
    return json.loads(tool_call.function.arguments)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="v0.8 Mode Classifier — assigns response-mode labels per protocol §3.4.",
        epilog="Example: python mode_classifier.py --input data/knives/results_enriched_<ts>.csv"
    )
    parser.add_argument("--input", required=True, help="Path to enriched CSV (results_enriched_*.csv)")
    parser.add_argument("--output-dir", default=None, help="Output directory (default: same as input)")
    parser.add_argument("--audit-sample", type=int, default=25, help="Stratified sample size for spot-check audit (default 25, matches v0.7)")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for stratified sampling")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of rows to classify (for testing)")
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

    with open(input_path) as f:
        rows = list(csv.DictReader(f))
    if args.limit:
        rows = rows[:args.limit]

    print("=" * 78)
    print("v0.8 Mode Classifier")
    print(f"Input:        {input_path}")
    print(f"Rows:         {len(rows)}")
    print(f"Model:        {CLASSIFIER_MODEL} (temperature={CLASSIFIER_TEMPERATURE})")
    print(f"Audit sample: {args.audit_sample} stratified rows (seed={args.seed})")
    print("=" * 78)

    classified = []
    for i, row in enumerate(rows, 1):
        prompt_id = row.get("prompt_id", "?")
        cep = row.get("cep", "?")
        slot = row.get("model_slot") or row.get("model", "?")
        raw = (row.get("raw_response") or "").strip()

        if not raw:
            row.update({
                "primary_mode": "refusal",
                "secondary_mode": "none",
                "brand_mentions_count": 0,
                "component_terms_count": 0,
                "authority_mentions_count": 0,
                "mode_rationale": "Empty raw_response — likely failed API call (see call_status)",
            })
            print(f"  [{i:3d}/{len(rows)}] {prompt_id:18s} | {slot:18s} -> empty, marked refusal")
        else:
            try:
                result = classify_one(client, raw, prompt_id, cep)
                row.update({
                    "primary_mode": result["primary_mode"],
                    "secondary_mode": result["secondary_mode"],
                    "brand_mentions_count": result["brand_mentions_count"],
                    "component_terms_count": result["component_terms_count"],
                    "authority_mentions_count": result["authority_mentions_count"],
                    "mode_rationale": result["rationale"],
                })
                print(f"  [{i:3d}/{len(rows)}] {prompt_id:18s} | {slot:18s} -> "
                      f"{result['primary_mode']:10s} (br={result['brand_mentions_count']}, "
                      f"cp={result['component_terms_count']}, au={result['authority_mentions_count']})")
            except Exception as e:
                row.update({
                    "primary_mode": "ERROR",
                    "secondary_mode": "none",
                    "brand_mentions_count": 0,
                    "component_terms_count": 0,
                    "authority_mentions_count": 0,
                    "mode_rationale": f"Classifier failed: {type(e).__name__}: {str(e)[:120]}",
                })
                print(f"  [{i:3d}/{len(rows)}] ERROR: {type(e).__name__}: {e}")

        classified.append(row)

    # ----- Write classified CSV -----
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = output_dir / f"mode_classified_{timestamp}.csv"
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(classified[0].keys()))
        writer.writeheader()
        writer.writerows(classified)

    # ----- Distribution summaries -----
    mode_dist = Counter(r["primary_mode"] for r in classified)
    print()
    print("=" * 78)
    print(f"Mode distribution across {len(classified)} responses:")
    for m, n in sorted(mode_dist.items(), key=lambda kv: -kv[1]):
        pct = 100 * n / len(classified)
        print(f"  {m:12s} n={n:4d} ({pct:5.1f}%)")

    print()
    print("Per-CEP mode distribution:")
    cep_modes = {}
    for r in classified:
        cep_modes.setdefault(r.get("cep", "UNKNOWN"), Counter())[r["primary_mode"]] += 1
    for cep in sorted(cep_modes.keys()):
        modes = cep_modes[cep]
        total = sum(modes.values())
        parts = "  ".join(f"{m}={n}" for m, n in sorted(modes.items(), key=lambda kv: -kv[1]))
        print(f"  {cep:25s} (n={total}):  {parts}")

    print()
    print("Per-model mode distribution:")
    model_modes = {}
    for r in classified:
        slot = r.get("model_slot") or r.get("model", "UNKNOWN")
        model_modes.setdefault(slot, Counter())[r["primary_mode"]] += 1
    for slot in sorted(model_modes.keys()):
        modes = model_modes[slot]
        total = sum(modes.values())
        parts = "  ".join(f"{m}={n}" for m, n in sorted(modes.items(), key=lambda kv: -kv[1]))
        print(f"  {slot:20s} (n={total}):  {parts}")

    print()
    print(f"Output: {out_path}")
    print("=" * 78)

    # ----- Stratified audit sample -----
    print()
    print(f"Generating stratified spot-check audit sample (n={args.audit_sample})...")
    random.seed(args.seed)

    strata = {}
    for r in classified:
        key = (r.get("cep", "UNKNOWN"), r["primary_mode"])
        strata.setdefault(key, []).append(r)

    audit = []
    for stratum_rows in strata.values():
        n_in_stratum = len(stratum_rows)
        target = max(1, round(args.audit_sample * n_in_stratum / max(len(classified), 1)))
        target = min(target, n_in_stratum)
        audit.extend(random.sample(stratum_rows, target))
    audit = audit[:args.audit_sample]

    audit_path = output_dir / f"audit_sample_mode_{timestamp}.csv"
    audit_keys = ["timestamp", "category", "prompt_id", "cep", "model_slot", "model_version",
                  "primary_mode", "secondary_mode",
                  "brand_mentions_count", "component_terms_count", "authority_mentions_count",
                  "mode_rationale", "raw_response"]
    if audit:
        audit_keys = [k for k in audit_keys if k in audit[0].keys()]
        with open(audit_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=audit_keys, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(audit)

    print(f"Audit sample: {audit_path}")
    print("  Manually classify each row's primary_mode independently in a separate column,")
    print("  then compute strict inter-rater agreement against the AI classifier.")
    print("  Target: ≥85% strict agreement (v0.7 reference: 88%).")
    print("=" * 78)


if __name__ == "__main__":
    main()
