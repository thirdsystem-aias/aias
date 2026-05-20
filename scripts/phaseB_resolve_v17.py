#!/usr/bin/env python3
"""
phaseB_resolve_v17.py — v0.17 Phase B mentionability validation (LLM substrate).

LLM-substrate analog of v0.15 Phase B (which was Trends-substrate). For each of
the 15 panel brands locked by Phase A (per osf/v17/phase_a_lock.md), validates
that the brand is MENTIONABLE in unprompted category queries against the locked
6-slot LLM reference set. Produces osf/v17/registries/topic_id_resolution_log_v0.17.csv
with PASS / PASS_E5 / EXCLUDED_E1a tier per brand. Phase D scoring uses this
log as the locked acquisition specification.

DEVIATION FROM v1.3 PROTOCOL — see osf/v17/DEVIATIONS.md Entry 7.
v1.3 §5.2 inherits v0.15's Phase B as Trends-substrate (pytrends + SerpAPI). v0.16+
pivoted to LLM-mediated measurement per the Methodology paper (SSRN 6761698) and
its v1.3 update (6797679). This script implements the provisional v1.4 §5.2 LLM-
substrate Phase B; v1.4 Methodology paper will formalize it as canonical.

Substrate rationale:
    v0.17 Phase A is fully LLM-substrate (C_P rule against 6-slot reference set).
    Mixing substrates between Phase A (LLM) and Phase B (Trends) would create a
    methodologically incoherent pipeline. Phase B in v0.17 is the LLM-substrate
    analog: validates that each panel brand surfaces in unprompted category
    queries with measurable mention rate — the Phase D measurement substrate.

Stages:
    Stage 1. For each (category_query, llm_slot), query LLM. Cache response at
             osf/v17/data/phaseB_queries/{query_id}/{slot_N}.json.
    Stage 2. For each brand × (query, slot) cell, detect mention via case-
             insensitive word-boundary regex against generated aliases.
    Stage 3. Determine per-brand tier:
                PASS:          mention_rate >= 1/6 (≥1 mention per LLM on average)
                PASS_E5:       0 < mention_rate < 1/6 (marginal but present)
                EXCLUDED_E1a:  mention_rate = 0 (not measurable)
    Stage 4. Write registries/topic_id_resolution_log_v0.17.csv (canonical).

Special Phase B handling:
    NODA HORO is pre-registered as borderline_classification with
    borderline_resolution_at="phase_b_topic_id" in registries/brands_kitchenware_v0.17.json.
    The tier verdict at Phase B *is* the protocol-mandated borderline resolution:
        PASS or PASS_E5  →  in-scope (cookware)
        EXCLUDED_E1a     →  out-of-scope (enamelware-only)
    A dedicated callout is printed in the summary.

Phase A descope applied programmatically:
    Vermicular C_P FAILED at Phase A (4/6 anchoring; see osf/v17/phase_a_lock.md).
    Brand remains in the registry (registry is locked at pre-reg time);
    descope is applied at panel-load time without mutating the registry.

Inputs (must exist before run):
    ~/aias/registries/brands_kitchenware_v0.17.json
    ~/aias/osf/v17/phase_a_lock.md  (referenced for descope list)
    
    Environment:
        ANTHROPIC_API_KEY, OPENAI_API_KEY, GOOGLE_API_KEY

Outputs:
    ~/aias/osf/v17/data/phaseB_queries/{query_id}/{slot_N}.json   (3 × 6 = 18 files)
    ~/aias/osf/v17/registries/topic_id_resolution_log_v0.17.csv   (canonical, 15 rows)

Usage:
    # Dry-run (no API calls; lists what would be queried):
    python scripts/phaseB_resolve_v17.py --dry-run

    # Live (consumes API quota; idempotent — skips already-cached responses):
    python scripts/phaseB_resolve_v17.py

    # Force re-query (overwrites cached responses):
    python scripts/phaseB_resolve_v17.py --force
"""

import argparse
import csv
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# ============================================================================
# Configuration — locked at script commit
# ============================================================================

ROOT = Path.home() / "aias"
V17_ROOT = ROOT / "osf" / "v17"
BRAND_REGISTRY = ROOT / "registries" / "brands_kitchenware_v0.17.json"
PHASE_A_LOCK = V17_ROOT / "phase_a_lock.md"

QUERIES_DIR = V17_ROOT / "data" / "phaseB_queries"
OUT_CSV = V17_ROOT / "registries" / "topic_id_resolution_log_v0.17.csv"

# Locked 6-slot LLM reference set (matches Phase A; see DEVIATIONS Entries 2-3
# for the Google-tier degradation history).
REFERENCE_SET = [
    {"slot": 1, "provider": "anthropic", "model_id": "claude-opus-4-5"},
    {"slot": 2, "provider": "anthropic", "model_id": "claude-sonnet-4-5"},
    {"slot": 3, "provider": "openai",    "model_id": "gpt-4o"},
    {"slot": 4, "provider": "openai",    "model_id": "gpt-4o-mini"},
    {"slot": 5, "provider": "google",    "model_id": "gemini-2.5-flash"},
    {"slot": 6, "provider": "google",    "model_id": "gemini-2.5-flash-lite"},
]

# Category queries — unprompted, tradition-agnostic, consumer-realistic.
# Hardcoded here = locked at script commit. Any modification = new pre-reg event.
CATEGORY_QUERIES = [
    {
        "id": "q1_best_brands",
        "text": "What are the best premium cookware brands? Please list several with brief descriptions.",
    },
    {
        "id": "q2_serious_cooks",
        "text": "Recommend high-quality cookware brands for serious home cooks. Name several specific brands.",
    },
    {
        "id": "q3_pro_chefs",
        "text": "What cookware brands do professional chefs use? List several.",
    },
]

# Phase A descope set (per phase_a_lock.md).
PHASE_A_DESCOPED = {"Vermicular"}

# Tier thresholds.
N_QUERIES = len(CATEGORY_QUERIES)   # 3
N_SLOTS = len(REFERENCE_SET)         # 6
N_CELLS = N_QUERIES * N_SLOTS        # 18
PASS_THRESHOLD = 1 / N_SLOTS         # 1/6 ~= 16.7% (~≥3/18 mentions)

# Response token budget — generous enough that LLMs can name multiple brands
# but bounded so no single response dominates.
MAX_RESPONSE_TOKENS = 1500
CALL_DELAY_SEC = 1   # gentle pacing between API calls


# ============================================================================
# Brand registry loader (applies Phase A descope; mechanical alias generation)
# ============================================================================

def generate_aliases(canonical: str) -> list:
    """
    Generate mechanical canonical-name variants for mention detection.

    Hyphen/space/concatenation variants only — semantic aliases (e.g.,
    "Field & Company" for "Field Company") are NOT generated; those would
    require registry-level alias entries. Documented for future registry-
    schema upgrade.
    """
    variants = {canonical, canonical.lower()}
    if "-" in canonical:
        variants.add(canonical.replace("-", " "))
        variants.add(canonical.replace("-", ""))
    if " " in canonical:
        variants.add(canonical.replace(" ", "-"))
        variants.add(canonical.replace(" ", ""))
    return sorted(v for v in variants if v.strip())


def slugify(name: str) -> str:
    """Filename-safe slug."""
    s = re.sub(r"[^a-zA-Z0-9]+", "-", name.lower()).strip("-")
    return s or "unknown"


def load_panel() -> list:
    """Load 16-brand registry; filter to 15 brands post-Phase-A-descope."""
    if not BRAND_REGISTRY.exists():
        sys.exit(f"ERROR: brand registry not found at {BRAND_REGISTRY}")

    reg = json.loads(BRAND_REGISTRY.read_text())
    panel = []
    descoped = []
    for cell_name, cell_data in reg["cells"].items():
        for b in cell_data["brands"]:
            if b["name"] in PHASE_A_DESCOPED:
                descoped.append(b["name"])
                continue
            panel.append({
                "canonical":      b["name"],
                "slug":           slugify(b["name"]),
                "cell":           cell_name,
                "pivot_ordinal":  b["pivot_ordinal"],
                "is_pivot":       b["pivot_ordinal"] == 1,
                "phase_a_role":   b["phase_a_role"],
                "sub_tradition":  b["substrate_sub_tradition"],
                "borderline":     b.get("borderline_classification", False),
                "borderline_resolution_at": b.get("borderline_resolution_at"),
                "aliases":        generate_aliases(b["name"]),
            })

    print(f"Panel loaded from {BRAND_REGISTRY.name}")
    print(f"  Total in registry: {len(panel) + len(descoped)}")
    print(f"  Descoped (Phase A): {descoped or '(none)'}")
    print(f"  Operational panel for Phase B: {len(panel)}")
    return panel


# ============================================================================
# LLM dispatcher
# ============================================================================

def query_llm(provider: str, model_id: str, prompt: str) -> str:
    """Dispatch a single-shot query to the appropriate LLM provider."""
    if provider == "anthropic":
        from anthropic import Anthropic
        client = Anthropic()
        resp = client.messages.create(
            model=model_id,
            max_tokens=MAX_RESPONSE_TOKENS,
            messages=[{"role": "user", "content": prompt}],
        )
        return resp.content[0].text

    if provider == "openai":
        from openai import OpenAI
        client = OpenAI()
        resp = client.chat.completions.create(
            model=model_id,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=MAX_RESPONSE_TOKENS,
        )
        return resp.choices[0].message.content or ""

    if provider == "google":
        from google import genai
        client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))
        resp = client.models.generate_content(
            model=model_id,
            contents=prompt,
        )
        return resp.text or ""

    raise ValueError(f"unknown provider: {provider!r}")


# ============================================================================
# Stage 1 — Acquire (query, slot) response matrix; cache to disk
# ============================================================================

def acquire_responses(force: bool, dry_run: bool) -> dict:
    """
    Returns dict keyed by (query_id, slot) -> response_text.
    Cached at osf/v17/data/phaseB_queries/{query_id}/{slot_N}.json.
    """
    responses = {}
    api_calls_planned = 0
    api_calls_skipped = 0

    print(f"\nStage 1 — acquiring {N_CELLS} (query, slot) cells")
    print(f"  Reference set: 6-slot panel (Phase A locked)")
    print(f"  Queries: {N_QUERIES} tradition-agnostic category prompts")
    if dry_run:
        print(f"  Mode: DRY-RUN (no API calls)")
    print()

    for q in CATEGORY_QUERIES:
        q_dir = QUERIES_DIR / q["id"]
        q_dir.mkdir(parents=True, exist_ok=True)

        for slot in REFERENCE_SET:
            cache_path = q_dir / f"slot_{slot['slot']}.json"
            key = (q["id"], slot["slot"])

            if cache_path.exists() and not force:
                rec = json.loads(cache_path.read_text())
                responses[key] = rec["response_text"]
                api_calls_skipped += 1
                continue

            label = f"  [{q['id']:18s} slot {slot['slot']} {slot['model_id']:30s}]"

            if dry_run:
                print(f"{label}  DRY-RUN (would call)")
                api_calls_planned += 1
                continue

            print(f"{label}  CALLING ... ", end="", flush=True)
            try:
                response_text = query_llm(
                    slot["provider"], slot["model_id"], q["text"]
                )
                rec = {
                    "query_id":      q["id"],
                    "query_text":    q["text"],
                    "slot":          slot["slot"],
                    "provider":      slot["provider"],
                    "model_id":      slot["model_id"],
                    "response_text": response_text,
                    "timestamp":     datetime.now(timezone.utc).isoformat(),
                    "response_tokens_approx": len(response_text.split()),
                }
                cache_path.write_text(json.dumps(rec, indent=2, ensure_ascii=False))
                responses[key] = response_text
                print(f"OK ({len(response_text.split())} ws-tokens)")
                api_calls_planned += 1
                time.sleep(CALL_DELAY_SEC)
            except Exception as exc:
                print(f"FAIL: {type(exc).__name__}: {exc}")
                sys.exit(f"Aborted on Stage 1 failure at {q['id']}/slot_{slot['slot']}.")

    print(f"\nStage 1 complete: {api_calls_planned} calls "
          f"({'planned' if dry_run else 'made'}), {api_calls_skipped} cached.")
    return responses


# ============================================================================
# Stage 2 — Mention detection per brand × (query, slot) cell
# ============================================================================

def detect_mention(response_text: str, aliases: list) -> bool:
    """
    Returns True if any alias appears in response (case-insensitive,
    word-boundary respecting). Aliases mechanically generated from canonical.
    """
    if not response_text:
        return False
    text_lower = response_text.lower()
    for alias in aliases:
        if not alias:
            continue
        pattern = r"\b" + re.escape(alias.lower()) + r"\b"
        if re.search(pattern, text_lower):
            return True
    return False


def tally_per_brand(panel: list, responses: dict) -> list:
    """
    For each brand, compute per-query, per-slot, total mention counts.
    Returns list of brand records enriched with mention diagnostics.
    """
    print(f"\nStage 2 — mention detection across {len(panel)} brands × {N_CELLS} cells")
    enriched = []

    for b in panel:
        # Mention matrix: rows = queries, cols = slots
        matrix = {q["id"]: {slot["slot"]: 0 for slot in REFERENCE_SET}
                  for q in CATEGORY_QUERIES}
        for q in CATEGORY_QUERIES:
            for slot in REFERENCE_SET:
                key = (q["id"], slot["slot"])
                if key not in responses:
                    continue
                if detect_mention(responses[key], b["aliases"]):
                    matrix[q["id"]][slot["slot"]] = 1

        # Per-query mention counts (max 6 each)
        per_query = {q_id: sum(slot_counts.values())
                     for q_id, slot_counts in matrix.items()}
        # Per-slot mention counts (max 3 each)
        per_slot = {s: sum(matrix[q_id][s] for q_id in matrix)
                    for s in (slot["slot"] for slot in REFERENCE_SET)}

        total_mentions = sum(per_query.values())
        mention_rate = total_mentions / N_CELLS

        enriched.append({
            **b,
            "matrix":         matrix,
            "per_query":      per_query,
            "per_slot":       per_slot,
            "total_mentions": total_mentions,
            "mention_rate":   mention_rate,
        })

    return enriched


# ============================================================================
# Stage 3 — Tier determination
# ============================================================================

def determine_tier(mention_rate: float) -> str:
    if mention_rate >= PASS_THRESHOLD:
        return "PASS"
    if mention_rate > 0:
        return "PASS_E5"
    return "EXCLUDED_E1a"


# ============================================================================
# Stage 4 — Write canonical CSV
# ============================================================================

CSV_COLS = [
    "brand_canonical", "cell", "phase_a_role", "sub_tradition", "is_pivot",
    "borderline_at_phase_b_in",
    "q1_mentions_of_6", "q2_mentions_of_6", "q3_mentions_of_6",
    "slot_1_mentions_of_3", "slot_2_mentions_of_3", "slot_3_mentions_of_3",
    "slot_4_mentions_of_3", "slot_5_mentions_of_3", "slot_6_mentions_of_3",
    "total_mentions_of_18", "mention_rate",
    "final_query_tier",
    "acquisition_query_set",
    "borderline_resolution",
    "notes",
]


def write_csv(enriched: list) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    acq_query_set = "|".join(q["id"] for q in CATEGORY_QUERIES)

    for b in enriched:
        tier = determine_tier(b["mention_rate"])

        # Noda Horo borderline resolution per pre-reg
        if b["borderline"] and b["borderline_resolution_at"] == "phase_b_topic_id":
            if tier in ("PASS", "PASS_E5"):
                resolution = "IN_SCOPE (mentionable as cookware)"
            else:
                resolution = "OUT_OF_SCOPE (not mentionable as cookware)"
        else:
            resolution = ""

        rows.append({
            "brand_canonical":          b["canonical"],
            "cell":                     b["cell"],
            "phase_a_role":             b["phase_a_role"],
            "sub_tradition":            b["sub_tradition"],
            "is_pivot":                 b["is_pivot"],
            "borderline_at_phase_b_in": b["borderline"],
            "q1_mentions_of_6":         b["per_query"]["q1_best_brands"],
            "q2_mentions_of_6":         b["per_query"]["q2_serious_cooks"],
            "q3_mentions_of_6":         b["per_query"]["q3_pro_chefs"],
            "slot_1_mentions_of_3":     b["per_slot"][1],
            "slot_2_mentions_of_3":     b["per_slot"][2],
            "slot_3_mentions_of_3":     b["per_slot"][3],
            "slot_4_mentions_of_3":     b["per_slot"][4],
            "slot_5_mentions_of_3":     b["per_slot"][5],
            "slot_6_mentions_of_3":     b["per_slot"][6],
            "total_mentions_of_18":     b["total_mentions"],
            "mention_rate":             round(b["mention_rate"], 4),
            "final_query_tier":         tier,
            "acquisition_query_set":    acq_query_set,
            "borderline_resolution":    resolution,
            "notes":                    "DEVIATIONS Entry 7: LLM-substrate Phase B; aliases mechanically generated",
        })

    with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CSV_COLS)
        w.writeheader()
        w.writerows(rows)

    print(f"\nWrote: {OUT_CSV}  ({len(rows)} rows)")
    return rows


# ============================================================================
# Stage 5 — Print summary
# ============================================================================

def print_summary(rows: list) -> None:
    print(f"\n{'=' * 72}")
    print(f"Phase B v0.17 summary")
    print(f"{'=' * 72}")

    n_pass = sum(1 for r in rows if r["final_query_tier"] == "PASS")
    n_pass_e5 = sum(1 for r in rows if r["final_query_tier"] == "PASS_E5")
    n_excl = sum(1 for r in rows if r["final_query_tier"] == "EXCLUDED_E1a")
    n_total = len(rows)
    n_eligible = n_pass + n_pass_e5

    print(f"  Total panel:    {n_total}")
    print(f"  PASS:           {n_pass}")
    print(f"  PASS_E5:        {n_pass_e5}")
    print(f"  EXCLUDED_E1a:   {n_excl}")
    print(f"  Eligible (PASS+PASS_E5): {n_eligible}")
    print(f"  C1 floor (worldwide n ≥ 12): {'HOLDS' if n_eligible >= 12 else 'BREACHED'} (n={n_eligible})")
    print()

    print(f"Per-cell breakdown:")
    for cell in ("european", "american", "japanese"):
        cell_rows = [r for r in rows if r["cell"] == cell]
        if not cell_rows:
            continue
        cell_eligible = sum(1 for r in cell_rows
                            if r["final_query_tier"] in ("PASS", "PASS_E5"))
        print(f"  {cell:<10}  total={len(cell_rows)}  eligible={cell_eligible}")

    print()
    print(f"Per-brand mention rates (sorted by rate, descending):")
    rows_sorted = sorted(rows, key=lambda r: -r["mention_rate"])
    for r in rows_sorted:
        marker = "★" if r["is_pivot"] else " "
        print(f"  {marker} {r['brand_canonical']:18s} "
              f"{r['cell']:<10}  rate={r['mention_rate']:.3f}  "
              f"({r['total_mentions_of_18']:>2}/18)  {r['final_query_tier']}")

    # Noda Horo borderline resolution callout (per pre-reg §3.2)
    noda = next((r for r in rows if r["brand_canonical"] == "Noda Horo"), None)
    if noda:
        print()
        print(f"{'=' * 72}")
        print(f"NODA HORO borderline-classification resolution at Phase B "
              f"(per pre-reg §3.2 'borderline_resolution_at')")
        print(f"{'=' * 72}")
        print(f"  Tier:       {noda['final_query_tier']}")
        print(f"  Mentions:   {noda['total_mentions_of_18']}/18  (rate={noda['mention_rate']:.3f})")
        print(f"  Resolution: {noda['borderline_resolution']}")
        if noda["final_query_tier"] == "EXCLUDED_E1a":
            print(f"\n  Noda Horo descoped from operational panel — record in DEVIATIONS.")

    print()
    print(f"Next steps:")
    print(f"  1. Review topic_id_resolution_log_v0.17.csv")
    print(f"  2. If C1 floor holds and pivot brands all PASS, lock Phase B (DEVIATIONS Entry 7).")
    print(f"  3. Proceed to Phase D acquisition + scoring on the eligible panel.")


# ============================================================================
# Main
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="v0.17 Phase B mentionability validation (LLM substrate)",
    )
    parser.add_argument("--dry-run", action="store_true",
                        help="Plan API calls without making them")
    parser.add_argument("--force", action="store_true",
                        help="Re-query all cells, overwriting cached responses")
    args = parser.parse_args()

    print(f"v0.17 Phase B (LLM-substrate) — mentionability validation")
    print(f"  Brand registry: {BRAND_REGISTRY.relative_to(ROOT)}")
    print(f"  Phase A lock:   {PHASE_A_LOCK.relative_to(ROOT)} (referenced)")
    print(f"  Reference set:  {N_SLOTS} slots (Phase A locked)")
    print(f"  Category Qs:    {N_QUERIES} tradition-agnostic prompts")
    print(f"  Tier thresholds: PASS ≥ {PASS_THRESHOLD:.3f}; "
          f"PASS_E5 (0, {PASS_THRESHOLD:.3f}); EXCLUDED_E1a = 0")
    print(f"  Session ts:     {datetime.now(timezone.utc).isoformat()}")
    print()

    if not args.dry_run:
        for env_var in ("ANTHROPIC_API_KEY", "OPENAI_API_KEY", "GOOGLE_API_KEY"):
            if not os.environ.get(env_var):
                sys.exit(f"ERROR: {env_var} not set. Source your env file and retry.")

    panel = load_panel()
    responses = acquire_responses(force=args.force, dry_run=args.dry_run)

    if args.dry_run:
        print(f"\nDry-run complete. No mention detection or CSV write.")
        return

    enriched = tally_per_brand(panel, responses)
    rows = write_csv(enriched)
    print_summary(rows)


if __name__ == "__main__":
    main()
