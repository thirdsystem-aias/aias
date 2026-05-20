"""v0.17 Premium Kitchenware — chart data definitions.

Pure-data module. No matplotlib, no rendering. Defines the data structures
that scripts/build_charts_v17.py consumes to render the three figures for
both the SSRN academic paper (papers/v0_17/figures/) and any future
Third System brand-format report.

Data sources:
    - Phase A C_P scores: osf/v17/classification_ledger.csv
    - Phase B mention rates: osf/v17/registries/topic_id_resolution_log_v0.17.csv
    - Cell counts: hardcoded from the locked phase_b_lock.md

If the CSV files are missing or unparseable, the loaders fall back to
hardcoded values that match the v0.17-phase-b-locked verdicts. This keeps
the chart pipeline reproducible from any clone, even before re-running
acquisition.
"""

import csv
from pathlib import Path

ROOT = Path.home() / "aias"
V17_ROOT = ROOT / "osf" / "v17"
LEDGER = V17_ROOT / "classification_ledger.csv"
PHASE_B_LOG = V17_ROOT / "registries" / "topic_id_resolution_log_v0.17.csv"

# ============================================================================
# Hardcoded fallback data — matches verdicts at tag v0.17-phase-b-locked
# ============================================================================

# Phase A anchoring counts (only the 4 pivots received Phase A measurement;
# non-pivot cell members are not represented here).
PHASE_A_SCORES_FALLBACK = {
    "Le Creuset": 6,
    "All-Clad":   6,
    "Vermicular": 4,  # FAILED supermajority; descoped before Phase B
    "Iwachu":     6,
}

# Phase B mention rates, sorted descending. Tuples: (brand, cell, rate, tier).
PHASE_B_MENTION_RATES_FALLBACK = [
    ("Le Creuset",    "european", 1.000, "PASS"),
    ("Mauviel",       "european", 1.000, "PASS"),
    ("All-Clad",      "american", 1.000, "PASS"),
    ("Staub",         "european", 0.944, "PASS"),
    ("Demeyere",      "european", 0.833, "PASS"),
    ("Lodge",         "american", 0.389, "PASS"),
    ("de Buyer",      "european", 0.333, "PASS"),
    ("Hestan",        "american", 0.333, "PASS"),
    ("Made In",       "american", 0.222, "PASS"),
    ("Fissler",       "european", 0.111, "PASS_E5"),
    ("Field Company", "american", 0.000, "EXCLUDED_E1a"),
    ("Smithey",       "american", 0.000, "EXCLUDED_E1a"),
    ("Iwachu",        "japanese", 0.000, "EXCLUDED_E1a"),
    ("Sori Yanagi",   "japanese", 0.000, "EXCLUDED_E1a"),
    ("Noda Horo",     "japanese", 0.000, "EXCLUDED_E1a"),
]

# Cell-level brand counts: pre-Phase-A (registered) vs post-Phase-B (operational)
CELL_COUNTS = {
    "european": {"pre": 6, "post": 6},
    "american": {"pre": 6, "post": 4},
    "japanese": {"pre": 4, "post": 0},  # Vermicular descoped at A; others at B
}

# Pre-registered constants
C1_FLOOR = 12
TOTAL_PRE = 16
TOTAL_POST = 10


# ============================================================================
# Loaders
# ============================================================================

def _slug_to_canonical(slug: str) -> str:
    """Map a brand slug from the classification ledger to canonical brand name."""
    mapping = {
        "le-creuset": "Le Creuset",
        "all-clad":   "All-Clad",
        "vermicular": "Vermicular",
        "iwachu":     "Iwachu",
    }
    return mapping.get(slug.lower(), slug)


def load_phase_a_scores() -> dict:
    """Sum per-brand `anchored` indicators from the classification ledger.
    Returns dict of {brand_canonical: count_0_to_6}.
    Falls back to PHASE_A_SCORES_FALLBACK if ledger absent or unparseable."""
    if not LEDGER.exists():
        return PHASE_A_SCORES_FALLBACK
    try:
        rows = list(csv.DictReader(LEDGER.open(encoding="utf-8")))
        scores: dict = {}
        for row in rows:
            brand = _slug_to_canonical(row["brand"])
            scores.setdefault(brand, 0)
            if row["anchored"].strip() == "1":
                scores[brand] += 1
        return scores if scores else PHASE_A_SCORES_FALLBACK
    except Exception:
        return PHASE_A_SCORES_FALLBACK


def load_phase_b_mention_rates() -> list:
    """Read per-brand mention rates from Phase B resolution log CSV.
    Returns list of (brand, cell, rate, tier) tuples, sorted descending by rate.
    Falls back to PHASE_B_MENTION_RATES_FALLBACK if CSV absent or unparseable."""
    if not PHASE_B_LOG.exists():
        return PHASE_B_MENTION_RATES_FALLBACK
    try:
        rows = list(csv.DictReader(PHASE_B_LOG.open(encoding="utf-8")))
        data = []
        for row in rows:
            data.append((
                row["brand_canonical"],
                row["cell"],
                float(row["mention_rate"]),
                row["final_query_tier"],
            ))
        data.sort(key=lambda x: -x[2])
        return data if data else PHASE_B_MENTION_RATES_FALLBACK
    except Exception:
        return PHASE_B_MENTION_RATES_FALLBACK
