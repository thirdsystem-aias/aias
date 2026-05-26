#!/usr/bin/env python3
"""
AIAS v0.23 — Canonical Scoring
Protocol v1.6 | Substrate: Premium Spirits

Reads:
  osf/v23/data/v23_phase_a_raw.json
  osf/v23/data/v23_phase_b_raw.json

Outputs:
  osf/v23/data/v23_phase_a_scored.json    (144 records + R-level scores)
  osf/v23/data/v23_phase_b_scored.json    (36 records + per-brand mention matrices)
  osf/v23/v23_verdicts.json               (hypothesis verdicts + composite scores)

Scoring approach:
  Phase A: LLM-as-judge (Claude Sonnet 4.5) classifies each response → R0/R1/R2/R3
  Phase B: Automated string matching for brand mentions + slot position;
           LLM-as-judge for elaboration flag

Usage:
  cd /Users/pablou/aias
  python3 scripts/score_v0_23.py --dry-run
  python3 scripts/score_v0_23.py
  python3 scripts/score_v0_23.py --skip-judge   # recompute composites from existing scored files

Requires: ANTHROPIC_API_KEY
"""

import json
import os
import re
import sys
import time
import argparse
from pathlib import Path
from datetime import datetime, timezone

import anthropic
import numpy as np
from scipy import stats

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PIPELINE_ROOT = Path("/Users/pablou/aias")
DATA_DIR = PIPELINE_ROOT / "osf" / "v23" / "data"
VERDICTS_PATH = PIPELINE_ROOT / "osf" / "v23" / "v23_verdicts.json"

PHASE_A_RAW = DATA_DIR / "v23_phase_a_raw.json"
PHASE_B_RAW = DATA_DIR / "v23_phase_b_raw.json"
PHASE_A_SCORED = DATA_DIR / "v23_phase_a_scored.json"
PHASE_B_SCORED = DATA_DIR / "v23_phase_b_scored.json"

JUDGE_MODEL = "claude-sonnet-4-5"
JUDGE_PAUSE = 1.5  # seconds between judge calls

# ---------------------------------------------------------------------------
# Registry (must match mega-prompt exactly)
# ---------------------------------------------------------------------------
REGISTRY = [
    {"id": "S01", "brand": "Johnnie Walker",     "conglomerate": 1},
    {"id": "S02", "brand": "Hennessy",           "conglomerate": 1},
    {"id": "S03", "brand": "Jack Daniel's",      "conglomerate": 1},
    {"id": "S04", "brand": "Patrón",             "conglomerate": 1},
    {"id": "S05", "brand": "Grey Goose",         "conglomerate": 1},
    {"id": "S06", "brand": "Bacardi",            "conglomerate": 1},
    {"id": "S07", "brand": "Bombay Sapphire",    "conglomerate": 1},
    {"id": "S08", "brand": "Jameson",            "conglomerate": 1},
    {"id": "S09", "brand": "Lagavulin",          "conglomerate": 1},
    {"id": "S10", "brand": "Clase Azul",         "conglomerate": 0},
    {"id": "S11", "brand": "Hendrick's",         "conglomerate": 0},
    {"id": "S12", "brand": "Woodford Reserve",   "conglomerate": 1},
    {"id": "S13", "brand": "Monkey 47",          "conglomerate": 1},
    {"id": "S14", "brand": "The Balvenie",       "conglomerate": 0},
    {"id": "S15", "brand": "Rémy Martin",        "conglomerate": 0},
    {"id": "S16", "brand": "Casamigos",          "conglomerate": 1},
    {"id": "S17", "brand": "Fortaleza",          "conglomerate": 0},
    {"id": "S18", "brand": "Compass Box",        "conglomerate": 0},
    {"id": "S19", "brand": "Nikka",              "conglomerate": 0},
    {"id": "S20", "brand": "Del Maguey",         "conglomerate": 1},
    {"id": "S21", "brand": "Fernet-Branca",      "conglomerate": 0},
    {"id": "S22", "brand": "Redbreast",          "conglomerate": 1},
    {"id": "S23", "brand": "St. George Spirits", "conglomerate": 0},
    {"id": "S24", "brand": "Mezcal Vago",        "conglomerate": 0},
]

# Brand name variants for string matching (lowercased)
BRAND_PATTERNS = {
    "S01": [r"\bjohnnie\s+walker\b"],
    "S02": [r"\bhennessy\b"],
    "S03": [r"\bjack\s+daniel'?s?\b"],
    "S04": [r"\bpatr[oó]n\b"],
    "S05": [r"\bgrey\s+goose\b"],
    "S06": [r"\bbacardi\b"],
    "S07": [r"\bbombay\s+sapphire\b"],
    "S08": [r"\bjameson\b"],
    "S09": [r"\blagavulin\b"],
    "S10": [r"\bclase\s+azul\b"],
    "S11": [r"\bhendrick'?s?\b"],
    "S12": [r"\bwoodford\s+reserve\b"],
    "S13": [r"\bmonkey\s+47\b"],
    "S14": [r"\b(the\s+)?balvenie\b"],
    "S15": [r"\br[eé]my\s+martin\b"],
    "S16": [r"\bcasamigos\b"],
    "S17": [r"\bfortaleza\b"],
    "S18": [r"\bcompass\s+box\b"],
    "S19": [r"\bnikka\b"],
    "S20": [r"\bdel\s+maguey\b"],
    "S21": [r"\bfernet[\s-]*branca\b"],
    "S22": [r"\bredbreast\b"],
    "S23": [r"\bst\.?\s+george\s+spirits?\b"],
    "S24": [r"\bmezcal\s+vago\b"],
}


# ---------------------------------------------------------------------------
# LLM Judge — Phase A Recognition scoring
# ---------------------------------------------------------------------------

JUDGE_SYSTEM_PROMPT = """You are a scoring judge for a brand recognition measurement study. 
You will be shown an LLM's response about a spirits brand and must classify the recognition level.

Score ONLY based on the response content. Use this rubric:

R3 (Rich recognition): The response contains ≥3 accurate, specific claims about the brand. 
Examples of specific claims: distillery location, flagship product/expression names, ownership/parent company, founding date, tasting notes, production method, price positioning, awards won.

R2 (Basic recognition): The response contains 1–2 accurate, specific claims. The rest may be generic, hedged, or vague.

R1 (Shallow recognition): The response acknowledges the brand exists but provides no specific factual claims. May contain only generic category information or heavily hedged statements.

R0 (Non-recognition): The response fails to identify the brand, confuses it with another entity, states it doesn't know the brand, or declines to answer.

Respond with ONLY the score label: R0, R1, R2, or R3. Nothing else."""

JUDGE_USER_TEMPLATE = """Brand: {brand_name}
Spirit type: {spirit_type}

LLM Response:
{response}

Score (R0/R1/R2/R3):"""


def judge_recognition(client, brand_name, spirit_type, response_text):
    """Use Claude as judge to score a Phase A response."""
    user_msg = JUDGE_USER_TEMPLATE.format(
        brand_name=brand_name,
        spirit_type=spirit_type,
        response=response_text[:3000],  # truncate to avoid token overflow
    )
    try:
        msg = client.messages.create(
            model=JUDGE_MODEL,
            max_tokens=10,
            temperature=0.0,
            system=JUDGE_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_msg}],
        )
        raw = msg.content[0].text.strip().upper()
        # Extract R-level from response
        match = re.search(r"R[0-3]", raw)
        if match:
            return match.group()
        return "R_ERR"
    except Exception as e:
        print(f"      Judge error: {e}")
        return "R_ERR"


# ---------------------------------------------------------------------------
# Phase B — automated brand mention detection
# ---------------------------------------------------------------------------

def find_brand_mentions(response_text):
    """Scan response for brand mentions. Returns dict {brand_id: first_char_position}."""
    text_lower = response_text.lower()
    mentions = {}
    for brand_id, patterns in BRAND_PATTERNS.items():
        for pattern in patterns:
            m = re.search(pattern, text_lower)
            if m:
                mentions[brand_id] = m.start()
                break
    return mentions


def compute_slot_positions(mentions):
    """Convert char positions to ordinal slot ranks (1-indexed)."""
    if not mentions:
        return {}
    sorted_brands = sorted(mentions.items(), key=lambda x: x[1])
    return {brand_id: rank + 1 for rank, (brand_id, _) in enumerate(sorted_brands)}


# ---------------------------------------------------------------------------
# Phase B — LLM judge for elaboration flag
# ---------------------------------------------------------------------------

ELABORATION_SYSTEM = """You are a scoring judge. Given an LLM response about spirits brands, determine whether a specific brand received elaboration beyond bare mention.

Elaboration = at least one specific factual claim about the brand (tasting notes, origin, production method, price, awards, cultural significance, etc.), not just naming it in a list.

Respond with ONLY: 1 (elaborated) or 0 (bare mention or not mentioned)."""

ELABORATION_USER = """Response:
{response}

Brand to check: {brand_name}

Elaboration (1 or 0):"""


def judge_elaboration(client, response_text, brand_name):
    """Check if a brand mention includes elaboration."""
    try:
        msg = client.messages.create(
            model=JUDGE_MODEL,
            max_tokens=5,
            temperature=0.0,
            system=ELABORATION_SYSTEM,
            messages=[{"role": "user", "content": ELABORATION_USER.format(
                response=response_text[:3000],
                brand_name=brand_name,
            )}],
        )
        raw = msg.content[0].text.strip()
        return 1 if "1" in raw else 0
    except Exception:
        return 0


# ---------------------------------------------------------------------------
# Composite scoring + hypothesis tests
# ---------------------------------------------------------------------------

R_NUMERIC = {"R0": 0, "R1": 1, "R2": 2, "R3": 3, "R_ERR": None}


def compute_composites(phase_a_scored, phase_b_scored):
    """Compute per-brand composite Presence scores and test hypotheses."""
    brand_ids = [b["id"] for b in REGISTRY]
    brand_map = {b["id"]: b for b in REGISTRY}

    # --- Phase A: mean Recognition score per brand ---
    recognition = {bid: [] for bid in brand_ids}
    for rec in phase_a_scored:
        r_val = R_NUMERIC.get(rec.get("r_level"), None)
        if r_val is not None:
            recognition[rec["brand_id"]].append(r_val)

    recog_mean = {}
    for bid in brand_ids:
        vals = recognition[bid]
        recog_mean[bid] = float(np.mean(vals)) if vals else 0.0

    # --- Pre-screen gate: R0 across ≥5 of 6 models ---
    prescreen_excluded = []
    for bid in brand_ids:
        vals = recognition[bid]
        r0_count = sum(1 for v in vals if v == 0)
        if r0_count >= 5:
            prescreen_excluded.append(bid)

    # --- Phase B: recall frequency + mean slot position per brand ---
    recall_freq = {bid: {"EA": 0, "CC": 0, "total": 0} for bid in brand_ids}
    recall_slots = {bid: [] for bid in brand_ids}
    elaboration_counts = {bid: 0 for bid in brand_ids}
    total_probes_ea = 0
    total_probes_cc = 0

    for rec in phase_b_scored:
        channel = "EA" if rec["channel"] == "editorial-authority" else "CC"
        if channel == "EA":
            total_probes_ea += 1
        else:
            total_probes_cc += 1

        mentions = rec.get("brand_mentions", {})
        slots = rec.get("slot_positions", {})
        elaborations = rec.get("elaborations", {})

        for bid in brand_ids:
            if mentions.get(bid, 0) == 1:
                recall_freq[bid][channel] += 1
                recall_freq[bid]["total"] += 1
                if bid in slots:
                    recall_slots[bid].append(slots[bid])
                if elaborations.get(bid, 0) == 1:
                    elaboration_counts[bid] += 1

    # Recall rate (proportion of probes mentioning brand)
    total_b_probes = len(phase_b_scored)
    recall_rate = {}
    for bid in brand_ids:
        recall_rate[bid] = recall_freq[bid]["total"] / total_b_probes if total_b_probes > 0 else 0.0

    mean_slot = {}
    for bid in brand_ids:
        s = recall_slots[bid]
        mean_slot[bid] = float(np.mean(s)) if s else 0.0

    # --- Composite Presence score ---
    # Weighted: Recognition (0.4) + Recall rate (0.4) + Inverse mean slot (0.2)
    # Normalize each component to 0-100 before combining
    max_recog = 3.0  # R3 is max
    max_recall = 1.0  # mentioned in every probe

    composites = {}
    for bid in brand_ids:
        if bid in prescreen_excluded:
            composites[bid] = None  # excluded from composite
            continue

        recog_norm = (recog_mean[bid] / max_recog) * 100 if max_recog > 0 else 0
        recall_norm = (recall_rate[bid] / max_recall) * 100 if max_recall > 0 else 0

        # Inverse slot: lower slot = better; normalize against max possible
        # If not mentioned, slot contribution = 0
        if mean_slot[bid] > 0:
            # Assume max brands per response ~24; slot 1 = best
            slot_norm = max(0, (1 - (mean_slot[bid] - 1) / 23)) * 100
        else:
            slot_norm = 0.0

        composites[bid] = round(
            0.4 * recog_norm + 0.4 * recall_norm + 0.2 * slot_norm, 2
        )

    # --- Regime classification ---
    # Quartile-based on composite scores (excluding pre-screened)
    active_scores = {bid: s for bid, s in composites.items() if s is not None}
    sorted_scores = sorted(active_scores.values())
    n = len(sorted_scores)

    if n >= 4:
        q25 = float(np.percentile(sorted_scores, 25))
        q50 = float(np.percentile(sorted_scores, 50))
        q75 = float(np.percentile(sorted_scores, 75))
    else:
        q25 = q50 = q75 = 0

    regimes = {}
    for bid in brand_ids:
        if bid in prescreen_excluded:
            regimes[bid] = "Absent"
        elif composites[bid] is None:
            regimes[bid] = "Absent"
        elif composites[bid] >= q75:
            regimes[bid] = "Dominant"
        elif composites[bid] >= q50:
            regimes[bid] = "Established"
        elif composites[bid] >= q25:
            regimes[bid] = "Emerging"
        else:
            regimes[bid] = "Absent"

    # --- Hypothesis tests ---
    hypotheses = {}

    # H_Regime4: no regime is empty
    regime_counts = {}
    for r in ["Dominant", "Established", "Emerging", "Absent"]:
        regime_counts[r] = sum(1 for v in regimes.values() if v == r)
    h_regime4_pass = all(c > 0 for c in regime_counts.values())
    hypotheses["H_Regime4"] = {
        "verdict": "supported" if h_regime4_pass else "falsified",
        "regime_counts": regime_counts,
        "criterion": "No regime is empty",
    }

    # H_RecognitionPrescreen: ≤3 brands excluded
    h_prescreen_pass = len(prescreen_excluded) <= 3
    hypotheses["H_RecognitionPrescreen"] = {
        "verdict": "supported" if h_prescreen_pass else "falsified",
        "excluded_count": len(prescreen_excluded),
        "excluded_brands": prescreen_excluded,
        "criterion": "≤3 brands excluded at R0 gate",
    }

    # H_Phantom: no phantom brands (structural — always supported in v0.23)
    hypotheses["H_Phantom"] = {
        "verdict": "not_testable",
        "note": "No defunct brands in registry; carried for protocol completeness",
    }

    # H_ILDirect: correlation between Recognition richness and Recall frequency
    recog_vals = []
    recall_vals = []
    for bid in brand_ids:
        if bid not in prescreen_excluded:
            recog_vals.append(recog_mean[bid])
            recall_vals.append(recall_rate[bid])

    if len(recog_vals) >= 5:
        r_corr, p_val = stats.pearsonr(recog_vals, recall_vals)
        h_il_pass = r_corr >= 0.40 and p_val < 0.05
        hypotheses["H_ILDirect"] = {
            "verdict": "supported" if h_il_pass else "falsified",
            "r": round(float(r_corr), 4),
            "p": round(float(p_val), 6),
            "n": len(recog_vals),
            "criterion": "r ≥ 0.40 and p < .05",
        }
    else:
        hypotheses["H_ILDirect"] = {
            "verdict": "insufficient_data",
            "n": len(recog_vals),
        }

    # H_C2_TwoChannel: overlap coefficient 0.30–0.80
    ea_set = set()
    cc_set = set()
    for bid in brand_ids:
        if recall_freq[bid]["EA"] > 0:
            ea_set.add(bid)
        if recall_freq[bid]["CC"] > 0:
            cc_set.add(bid)

    if len(ea_set) > 0 and len(cc_set) > 0:
        overlap = len(ea_set & cc_set) / min(len(ea_set), len(cc_set))
        h_c2_pass = 0.30 <= overlap <= 0.80
        hypotheses["H_C2_TwoChannel"] = {
            "verdict": "supported" if h_c2_pass else "falsified",
            "overlap_coefficient": round(overlap, 4),
            "ea_brands": len(ea_set),
            "cc_brands": len(cc_set),
            "intersection": len(ea_set & cc_set),
            "criterion": "Overlap coefficient in [0.30, 0.80]",
        }
    else:
        hypotheses["H_C2_TwoChannel"] = {
            "verdict": "insufficient_data",
            "ea_brands": len(ea_set),
            "cc_brands": len(cc_set),
        }

    # H_ConglomeratePortfolio: conglomerate > independent on composite
    conglom_scores = [composites[bid] for bid in brand_ids
                      if brand_map[bid]["conglomerate"] == 1 and composites[bid] is not None]
    indep_scores = [composites[bid] for bid in brand_ids
                    if brand_map[bid]["conglomerate"] == 0 and composites[bid] is not None]

    if len(conglom_scores) >= 2 and len(indep_scores) >= 2:
        u_stat, u_p = stats.mannwhitneyu(conglom_scores, indep_scores, alternative="greater")
        t_stat, t_p = stats.ttest_ind(conglom_scores, indep_scores, alternative="greater")
        conglom_mean = float(np.mean(conglom_scores))
        indep_mean = float(np.mean(indep_scores))
        lift_pct = ((conglom_mean - indep_mean) / indep_mean * 100) if indep_mean > 0 else 0

        h_cong_pass = t_p < 0.05 and conglom_mean > indep_mean
        hypotheses["H_ConglomeratePortfolio"] = {
            "verdict": "supported" if h_cong_pass else "falsified",
            "conglomerate_mean": round(conglom_mean, 2),
            "independent_mean": round(indep_mean, 2),
            "lift_pct": round(lift_pct, 1),
            "t_stat": round(float(t_stat), 4),
            "t_p": round(float(t_p), 6),
            "mann_whitney_u": round(float(u_stat), 4),
            "mann_whitney_p": round(float(u_p), 6),
            "n_conglomerate": len(conglom_scores),
            "n_independent": len(indep_scores),
            "criterion": "p < .05 and conglomerate > independent",
        }
    else:
        hypotheses["H_ConglomeratePortfolio"] = {
            "verdict": "insufficient_data",
            "n_conglomerate": len(conglom_scores),
            "n_independent": len(indep_scores),
        }

    # --- Assemble per-brand detail table ---
    brand_details = []
    for bid in brand_ids:
        b = brand_map[bid]
        brand_details.append({
            "brand_id": bid,
            "brand_name": b["brand"],
            "conglomerate": b["conglomerate"],
            "recognition_mean": round(recog_mean[bid], 3),
            "recall_rate": round(recall_rate[bid], 3),
            "recall_ea": recall_freq[bid]["EA"],
            "recall_cc": recall_freq[bid]["CC"],
            "recall_total": recall_freq[bid]["total"],
            "mean_slot_position": round(mean_slot[bid], 2),
            "elaboration_count": elaboration_counts[bid],
            "composite_presence": composites[bid],
            "regime": regimes[bid],
            "prescreen_excluded": bid in prescreen_excluded,
        })

    # --- Verdicts output ---
    verdicts = {
        "phase": "v0.23",
        "substrate": "premium spirits",
        "protocol": "v1.6",
        "scored_at": datetime.now(timezone.utc).isoformat(),
        "phase_a_records": len(phase_a_scored),
        "phase_b_records": len(phase_b_scored),
        "prescreen_excluded": prescreen_excluded,
        "regime_thresholds": {"q25": q25, "q50": q50, "q75": q75},
        "hypotheses": hypotheses,
        "brand_details": brand_details,
    }

    return verdicts


# ---------------------------------------------------------------------------
# Main orchestration
# ---------------------------------------------------------------------------

def score_phase_a(client, dry_run=False):
    """Score all Phase A responses via LLM judge."""
    with open(PHASE_A_RAW, "r", encoding="utf-8") as f:
        records = json.load(f)

    total = len(records)
    print(f"\n  Phase A: {total} records to score")

    for i, rec in enumerate(records, 1):
        if rec["status"] != "ok":
            rec["r_level"] = "R_ERR"
            continue

        tag = f"[{i}/{total}] {rec['brand_id']} {rec['brand_name']} → {rec['model_slot']}"

        if dry_run:
            print(f"    DRY RUN: {tag}")
            rec["r_level"] = "R_DRY"
            continue

        print(f"    Scoring: {tag}", end="", flush=True)
        r_level = judge_recognition(
            client,
            rec["brand_name"],
            rec["spirit_type"],
            rec["response"],
        )
        rec["r_level"] = r_level
        print(f" → {r_level}")
        time.sleep(JUDGE_PAUSE)

        # Checkpoint every 24
        if i % 24 == 0:
            with open(PHASE_A_SCORED, "w", encoding="utf-8") as f:
                json.dump(records, f, ensure_ascii=False, indent=2)
            print(f"    ✓ Checkpoint: {i}/{total}")

    # Final save
    with open(PHASE_A_SCORED, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

    # Summary
    levels = {}
    for rec in records:
        lvl = rec.get("r_level", "?")
        levels[lvl] = levels.get(lvl, 0) + 1
    print(f"\n  Phase A scoring complete: {levels}")

    return records


def score_phase_b(client, dry_run=False):
    """Score all Phase B responses for brand mentions + elaboration."""
    with open(PHASE_B_RAW, "r", encoding="utf-8") as f:
        records = json.load(f)

    total = len(records)
    print(f"\n  Phase B: {total} records to score")

    for i, rec in enumerate(records, 1):
        if rec["status"] != "ok":
            rec["brand_mentions"] = {}
            rec["slot_positions"] = {}
            rec["elaborations"] = {}
            continue

        tag = f"[{i}/{total}] {rec['probe_id']} → {rec['model_slot']}"
        response_text = rec["response"]

        # Automated: brand mentions + slot positions
        mentions_raw = find_brand_mentions(response_text)
        slot_positions = compute_slot_positions(mentions_raw)

        # Binary mention dict
        brand_mentions = {}
        for b in REGISTRY:
            bid = b["id"]
            brand_mentions[bid] = 1 if bid in mentions_raw else 0

        rec["brand_mentions"] = brand_mentions
        rec["slot_positions"] = slot_positions

        # LLM judge: elaboration for each mentioned brand
        mentioned_brands = [b for b in REGISTRY if b["id"] in mentions_raw]
        elaborations = {}

        if dry_run:
            print(f"    DRY RUN: {tag} — {len(mentioned_brands)} brands mentioned")
            for b in mentioned_brands:
                elaborations[b["id"]] = 0
        else:
            n_mentioned = len(mentioned_brands)
            print(f"    Scoring: {tag} — {n_mentioned} brands mentioned", flush=True)

            # Batch elaboration check: send one judge call with all brands
            if n_mentioned > 0:
                elab_result = judge_elaboration_batch(client, response_text, mentioned_brands)
                elaborations = elab_result
            print(f"      Elaborations: {sum(elaborations.values())}/{n_mentioned}")

        rec["elaborations"] = elaborations

    # Final save
    with open(PHASE_B_SCORED, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

    # Summary
    total_mentions = sum(
        sum(rec.get("brand_mentions", {}).values())
        for rec in records if rec["status"] == "ok"
    )
    print(f"\n  Phase B scoring complete: {total_mentions} total brand mentions across {total} responses")

    return records


ELABORATION_BATCH_SYSTEM = """You are a scoring judge. Given an LLM response about spirits brands, determine which brands received elaboration beyond bare mention.

Elaboration = at least one specific factual claim about the brand (tasting notes, origin, production method, price, awards, cultural significance, etc.), not just naming it in a list.

For each brand listed, respond with the brand name followed by 1 (elaborated) or 0 (bare mention).
Format: one brand per line, e.g.:
Johnnie Walker: 1
Grey Goose: 0"""


def judge_elaboration_batch(client, response_text, mentioned_brands):
    """Check elaboration for multiple brands in one judge call."""
    brand_list = "\n".join(f"- {b['brand']}" for b in mentioned_brands)
    try:
        msg = client.messages.create(
            model=JUDGE_MODEL,
            max_tokens=200,
            temperature=0.0,
            system=ELABORATION_BATCH_SYSTEM,
            messages=[{"role": "user", "content": f"Response:\n{response_text[:3000]}\n\nBrands to check:\n{brand_list}"}],
        )
        raw = msg.content[0].text.strip()
        time.sleep(JUDGE_PAUSE)

        # Parse results
        result = {}
        for b in mentioned_brands:
            bid = b["id"]
            bname = b["brand"].lower()
            # Look for "brand_name: 1" or "brand_name: 0" pattern
            for line in raw.lower().split("\n"):
                if bname in line:
                    result[bid] = 1 if "1" in line.split(":")[-1] else 0
                    break
            else:
                result[bid] = 0  # default if not found in judge output

        return result
    except Exception as e:
        print(f"      Elaboration judge error: {e}")
        return {b["id"]: 0 for b in mentioned_brands}


def main():
    parser = argparse.ArgumentParser(description="AIAS v0.23 canonical scoring")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--skip-judge", action="store_true",
                        help="Skip LLM judge; recompute composites from existing scored files")
    args = parser.parse_args()

    # Check inputs exist
    for p in [PHASE_A_RAW, PHASE_B_RAW]:
        if not p.exists():
            print(f"ERROR: {p} not found. Run acquisition first.")
            sys.exit(1)

    client = None
    if not args.dry_run and not args.skip_judge:
        if not os.environ.get("ANTHROPIC_API_KEY"):
            print("ERROR: ANTHROPIC_API_KEY not set")
            sys.exit(1)
        client = anthropic.Anthropic()

    print("=" * 60)
    print("AIAS v0.23 — Canonical Scoring (Protocol v1.6)")
    print("=" * 60)

    if args.skip_judge:
        print("\n  --skip-judge: loading existing scored files")
        if not PHASE_A_SCORED.exists() or not PHASE_B_SCORED.exists():
            print("ERROR: Scored files not found. Run without --skip-judge first.")
            sys.exit(1)
        with open(PHASE_A_SCORED) as f:
            phase_a_scored = json.load(f)
        with open(PHASE_B_SCORED) as f:
            phase_b_scored = json.load(f)
    else:
        phase_a_scored = score_phase_a(client, dry_run=args.dry_run)
        phase_b_scored = score_phase_b(client, dry_run=args.dry_run)

    if args.dry_run:
        print("\n  Dry run complete — no composites computed")
        return

    # Compute composites + hypothesis tests
    print("\n" + "=" * 60)
    print("Computing composites + hypothesis tests")
    print("=" * 60)

    verdicts = compute_composites(phase_a_scored, phase_b_scored)

    with open(VERDICTS_PATH, "w", encoding="utf-8") as f:
        json.dump(verdicts, f, ensure_ascii=False, indent=2)

    # Print summary
    print(f"\n  Verdicts written to {VERDICTS_PATH}")
    print(f"\n  Pre-screen excluded: {verdicts['prescreen_excluded']}")
    print(f"\n  Hypothesis verdicts:")
    for h, v in verdicts["hypotheses"].items():
        print(f"    {h}: {v['verdict']}")

    print(f"\n  Regime distribution:")
    for regime, count in verdicts["hypotheses"]["H_Regime4"]["regime_counts"].items():
        brands_in_regime = [b["brand_name"] for b in verdicts["brand_details"] if b["regime"] == regime]
        print(f"    {regime} ({count}): {', '.join(brands_in_regime)}")

    print(f"\n  Top 5 by composite:")
    sorted_brands = sorted(
        [b for b in verdicts["brand_details"] if b["composite_presence"] is not None],
        key=lambda x: x["composite_presence"],
        reverse=True,
    )
    for b in sorted_brands[:5]:
        print(f"    {b['brand_name']}: {b['composite_presence']}")

    print("\n✓ Scoring complete.")


if __name__ == "__main__":
    main()
