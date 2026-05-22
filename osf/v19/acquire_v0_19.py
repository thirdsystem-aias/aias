"""
acquire_v0_19.py — AIAS v0.19 Acquisition Pipeline

Single unified acquisition script for v0.19. Four operations:

  gen-phase-a            → phase_a_queries.jsonl (96 queries: 16 brands × 6 models)
  gen-phase-b            → phase_b_queries.jsonl (36 queries: 6 frames × 6 models)
  parse-phase-a <file>   → phase_a_results.csv  (from raw model responses)
  parse-phase-b <file>   → phase_b_results.csv  (from raw model responses;
                                                  applies v1.4 brand-mention
                                                  detection rules)

Pre-registered tooling. Locked at pre-reg commit alongside score_v0_19.py.

Inputs (locked):
  panel_registry_v0_19.csv
  thresholds_v0_19.json

Raw-response schema (JSONL, one query per line):
  Phase A:
    {"query_id": "...", "brand": "Sennheiser", "panel_model": "claude-opus-4-5",
     "response": "Yes."}
  Phase B:
    {"query_id": "...", "frame": "q1_audiophile", "panel_model": "gpt-4o",
     "response": "Some of the best audiophile headphones include..."}

Author: Pablo Ulpiano González Castro
Pre-reg revision: r1
Pre-reg tag: v0.19-prereg-r1
"""

import csv
import json
import re
import sys
import unicodedata
from pathlib import Path

SCRIPT_DIR       = Path(__file__).parent
REGISTRY_PATH    = SCRIPT_DIR / "panel_registry_v0_19.csv"
THRESHOLDS_PATH  = SCRIPT_DIR / "thresholds_v0_19.json"
PHASE_A_QUERIES  = SCRIPT_DIR / "phase_a_queries.jsonl"
PHASE_B_QUERIES  = SCRIPT_DIR / "phase_b_queries.jsonl"
PHASE_A_RESULTS  = SCRIPT_DIR / "phase_a_results.csv"
PHASE_B_RESULTS  = SCRIPT_DIR / "phase_b_results.csv"


# ---------------------------------------------------------------------------
# Loading (matched to score_v0_19.py)
# ---------------------------------------------------------------------------

def load_registry():
    with open(REGISTRY_PATH) as f:
        return list(csv.DictReader(f))


def load_thresholds():
    with open(THRESHOLDS_PATH) as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# Query batch generation
# ---------------------------------------------------------------------------

def gen_phase_a():
    """
    Generate Phase A query batch: 16 brands × 6 models = 96 queries.
    Probe template loaded verbatim from thresholds_v0_19.json (locked).
    """
    registry = load_registry()
    thresholds = load_thresholds()
    template = thresholds["phase_a"]["probe_template"]
    models = thresholds["reference_panel"]

    queries = []
    for r in registry:
        brand = r["brand"]
        probe = template.replace("[BRAND_NAME]", brand)
        for model in models:
            queries.append({
                "query_id": f"phase_a__{slug(brand)}__{model}",
                "phase": "A",
                "brand": brand,
                "panel_model": model,
                "probe": probe,
            })

    with open(PHASE_A_QUERIES, "w") as f:
        for q in queries:
            f.write(json.dumps(q) + "\n")

    print(f"Wrote {len(queries)} Phase A queries to {PHASE_A_QUERIES}")
    return queries


def gen_phase_b():
    """
    Generate Phase B query batch: 6 frames × 6 models = 36 queries.
    Frames loaded verbatim from thresholds_v0_19.json (locked).
    Note: Phase B queries are NOT brand-specific; brand mentions are detected
    in responses during parse-phase-b.
    """
    thresholds = load_thresholds()
    frames = thresholds["phase_b"]["frames"]
    models = thresholds["reference_panel"]

    queries = []
    for frame_id, frame in frames.items():
        prompt = frame["prompt"]
        for model in models:
            queries.append({
                "query_id": f"phase_b__{frame_id}__{model}",
                "phase": "B",
                "frame": frame_id,
                "frame_channel": frame["channel"],
                "frame_load_bearing": frame["load_bearing"],
                "panel_model": model,
                "prompt": prompt,
            })

    with open(PHASE_B_QUERIES, "w") as f:
        for q in queries:
            f.write(json.dumps(q) + "\n")

    print(f"Wrote {len(queries)} Phase B queries to {PHASE_B_QUERIES}")
    return queries


def slug(s):
    """Lower-cased ASCII slug for query_id construction."""
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"[^a-zA-Z0-9]+", "_", s).strip("_").lower()
    return s


# ---------------------------------------------------------------------------
# v1.4 canonical brand-mention detection
# ---------------------------------------------------------------------------

def normalize_for_matching(text):
    """Accent-strip and lowercase. Used in case-insensitive matching."""
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    return text.lower()


def build_brand_patterns(registry):
    """
    Precompile per-brand regex patterns under v1.4 detection rules:
      - case-insensitive (applied via normalization)
      - accent-stripped (applied via normalization)
      - possessive-aware (matches "Brand", "Brand's", "Brands'")
      - word-boundary aware (no infix matching)

    Returns dict: {brand: compiled_regex}
    """
    patterns = {}
    for r in registry:
        brand_norm = normalize_for_matching(r["brand"])
        # Escape regex metacharacters in brand name; tolerate '&', '.', spaces
        escaped = re.escape(brand_norm)
        # Possessive-aware suffix (optional 's or s')
        pattern = re.compile(
            r"(?<![a-z0-9])" + escaped + r"(?:'s|s')?(?![a-z0-9])"
        )
        patterns[r["brand"]] = pattern
    return patterns


def detect_mentions_in_response(response_text, brand_patterns):
    """
    Scan a Phase B response for brand mentions.

    Returns list of dicts: [{"brand": str, "rank": int|None}, ...] in
    response order. First-occurrence-wins de-duplication: each brand is
    counted at most once per response.
    """
    norm_response = normalize_for_matching(response_text)

    # Detect enumerated-list rank context (numbered lists or bulleted)
    rank_map = build_rank_map(response_text)

    found = []
    seen = set()
    for brand, pattern in brand_patterns.items():
        match = pattern.search(norm_response)
        if not match:
            continue
        if brand in seen:
            continue
        seen.add(brand)
        # Map match position to enumerated rank (if any)
        rank = lookup_rank(match.start(), rank_map)
        found.append({"brand": brand, "rank": rank, "position": match.start()})

    # Order by position to preserve response-order presentation
    found.sort(key=lambda x: x["position"])
    return [{"brand": x["brand"], "rank": x["rank"]} for x in found]


def build_rank_map(response_text):
    """
    Build a character-position → list-rank map for enumerated lists in the
    response. Supports numbered (1., 2., 1), 2)) and bulleted (-, *, •) lists.
    Returns sorted list of (start_pos, end_pos, rank) tuples.
    """
    norm = normalize_for_matching(response_text)

    # Numbered list patterns
    numbered = list(re.finditer(r"(?m)^\s*(\d{1,2})[.)]\s+", norm))
    if numbered:
        spans = []
        for i, m in enumerate(numbered):
            start = m.start()
            end = numbered[i + 1].start() if i + 1 < len(numbered) else len(norm)
            rank = int(m.group(1))
            spans.append((start, end, rank))
        return spans

    # Bulleted list — rank by occurrence order
    bulleted = list(re.finditer(r"(?m)^\s*[-*•]\s+", norm))
    if bulleted:
        spans = []
        for i, m in enumerate(bulleted):
            start = m.start()
            end = bulleted[i + 1].start() if i + 1 < len(bulleted) else len(norm)
            spans.append((start, end, i + 1))
        return spans

    return []


def lookup_rank(pos, rank_map):
    """Find which enumerated item (if any) contains the given char position."""
    for start, end, rank in rank_map:
        if start <= pos < end:
            return rank
    return None


# ---------------------------------------------------------------------------
# Phase A response parsing
# ---------------------------------------------------------------------------

YES_RE = re.compile(r"\b(yes|yeah|yep|correct|affirmative|indeed)\b", re.I)
NO_RE  = re.compile(r"\b(no|nope|not\s+(?:commonly\s+)?recognized|incorrect|negative)\b", re.I)


def parse_phase_a_response(response_text):
    """
    Extract yes/no from a Phase A response.
    Returns 1 (yes-recognized), 0 (no-or-not-recognized), or None (ambiguous).
    Heuristic: first yes/no signal wins; if both present, the one earlier
    in the response wins.
    """
    yes_match = YES_RE.search(response_text)
    no_match = NO_RE.search(response_text)

    if yes_match and no_match:
        return 1 if yes_match.start() < no_match.start() else 0
    if yes_match:
        return 1
    if no_match:
        return 0
    return None  # ambiguous; flagged in DEVIATIONS if non-trivial count


def parse_phase_a(responses_path):
    """
    Parse a JSONL responses file into phase_a_results.csv.
    Output columns: brand,panel_model,recognition_yes
    """
    out_rows = []
    ambiguous = []
    with open(responses_path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            if r.get("phase") != "A" and not r.get("brand"):
                continue
            yn = parse_phase_a_response(r["response"])
            if yn is None:
                ambiguous.append(r)
                continue
            out_rows.append({
                "brand": r["brand"],
                "panel_model": r["panel_model"],
                "recognition_yes": yn,
            })

    with open(PHASE_A_RESULTS, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["brand", "panel_model", "recognition_yes"])
        writer.writeheader()
        writer.writerows(out_rows)

    print(f"Wrote {len(out_rows)} Phase A result rows to {PHASE_A_RESULTS}")
    if ambiguous:
        print(f"WARNING: {len(ambiguous)} ambiguous responses (no yes/no signal detected).")
        print("  These are excluded from results. Review and consider opening a DEVIATIONS entry.")
        for r in ambiguous[:5]:
            print(f"  - query_id={r.get('query_id')} response={r['response'][:80]!r}")
        if len(ambiguous) > 5:
            print(f"  ... ({len(ambiguous) - 5} more)")


# ---------------------------------------------------------------------------
# Phase B response parsing
# ---------------------------------------------------------------------------

def parse_phase_b(responses_path):
    """
    Parse a JSONL responses file into phase_b_results.csv.
    For each (frame, model) response, scan for all 16 registry brands using
    v1.4 canonical brand-mention detection. Emit one row per (brand, frame,
    model) tuple with mentioned ∈ {0, 1} and rank (int|empty).
    """
    registry = load_registry()
    brand_patterns = build_brand_patterns(registry)
    all_brands = [r["brand"] for r in registry]

    out_rows = []
    with open(responses_path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            if r.get("phase") != "B" and not r.get("frame"):
                continue

            mentions = detect_mentions_in_response(r["response"], brand_patterns)
            mentioned_brands = {m["brand"]: m["rank"] for m in mentions}

            for brand in all_brands:
                if brand in mentioned_brands:
                    out_rows.append({
                        "brand": brand,
                        "panel_model": r["panel_model"],
                        "frame": r["frame"],
                        "mentioned": 1,
                        "rank": mentioned_brands[brand] if mentioned_brands[brand] is not None else "",
                    })
                else:
                    out_rows.append({
                        "brand": brand,
                        "panel_model": r["panel_model"],
                        "frame": r["frame"],
                        "mentioned": 0,
                        "rank": "",
                    })

    with open(PHASE_B_RESULTS, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["brand", "panel_model", "frame", "mentioned", "rank"])
        writer.writeheader()
        writer.writerows(out_rows)

    total_mentioned = sum(1 for r in out_rows if r["mentioned"] == 1)
    print(f"Wrote {len(out_rows)} Phase B result rows to {PHASE_B_RESULTS}")
    print(f"  ({total_mentioned} mentions across {len(out_rows)} brand × frame × model observations)")


# ---------------------------------------------------------------------------
# CLI dispatch
# ---------------------------------------------------------------------------

USAGE = """\
Usage:
  python acquire_v0_19.py gen-phase-a
  python acquire_v0_19.py gen-phase-b
  python acquire_v0_19.py parse-phase-a <responses.jsonl>
  python acquire_v0_19.py parse-phase-b <responses.jsonl>
"""


def main():
    if len(sys.argv) < 2:
        print(USAGE)
        sys.exit(1)

    op = sys.argv[1]

    if op == "gen-phase-a":
        gen_phase_a()
    elif op == "gen-phase-b":
        gen_phase_b()
    elif op == "parse-phase-a":
        if len(sys.argv) < 3:
            print(USAGE)
            sys.exit(1)
        parse_phase_a(Path(sys.argv[2]))
    elif op == "parse-phase-b":
        if len(sys.argv) < 3:
            print(USAGE)
            sys.exit(1)
        parse_phase_b(Path(sys.argv[2]))
    else:
        print(USAGE)
        sys.exit(1)


if __name__ == "__main__":
    main()
