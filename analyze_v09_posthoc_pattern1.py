"""Post-hoc Pattern 1 replication test for v0.9.

v0.6's Pattern 1 (Cross-Model Variance and Discourse Coherence) claims that
fragmented-discourse categories produce wider cross-model spread than coherent-
discourse categories. The pre-registered H3 tests within-category brand-presence
variance preservation, which is a related but distinct statistic.

This script computes the cross-model spread test directly and reports the
longitudinal Spearman ρ.

Cross-model spread for a brand = |sonnet_presence - mini_presence|.
Cross-model spread for a category = mean across registered brands.

v0.6 reported (descriptively): personal finance > olive oil > PM software >
skincare > running shoes on cross-model spread magnitude. We compare ranking
at t1 vs t2.

Usage:
    cd ~/aias
    python3 analyze_v09_posthoc_pattern1.py
"""
import sys
from statistics import mean
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from analyze_v09 import (
    load_all_data,
    per_brand_presence,
    filter_slot,
    spearman_rho,
    CATEGORIES,
)


def cross_model_spread_per_category(rows, registry):
    """Mean absolute |sonnet - mini| across registered brands."""
    sonnet_rows = filter_slot(rows, "anthropic_sonnet")
    mini_rows = filter_slot(rows, "openai_mini")
    bp_sonnet = per_brand_presence(sonnet_rows, registry)
    bp_mini = per_brand_presence(mini_rows, registry)
    spreads = [abs(bp_sonnet[b] - bp_mini[b]) for b in registry["all_brands"]]
    if not spreads:
        return 0.0
    return mean(spreads)


def main():
    data = load_all_data()

    print("=" * 78)
    print("Post-hoc Pattern 1 replication: cross-model spread by category, t1 vs t2")
    print("=" * 78)

    spreads_t1 = {}
    spreads_t2 = {}
    print(f"\n{'Category':12s} | {'t1 spread':>10s} | {'t2 spread':>10s} | {'delta':>8s}")
    print("-" * 50)
    for cat in CATEGORIES:
        registry = data[(cat, "v09")]["registry"]
        s1 = cross_model_spread_per_category(data[(cat, "v06")]["rows"], registry)
        s2 = cross_model_spread_per_category(data[(cat, "v09")]["rows"], registry)
        spreads_t1[cat] = s1
        spreads_t2[cat] = s2
        delta = s2 - s1
        print(f"{cat:12s} | {s1:9.2f}pp | {s2:9.2f}pp | {delta:+7.2f}pp")

    # Rank by spread (higher spread = lower rank in fragmented-first order)
    t1_sorted = sorted(CATEGORIES, key=lambda c: spreads_t1[c], reverse=True)
    t2_sorted = sorted(CATEGORIES, key=lambda c: spreads_t2[c], reverse=True)

    print(f"\nt1 cross-model spread ranking (high to low): {t1_sorted}")
    print(f"t2 cross-model spread ranking (high to low): {t2_sorted}")

    t1_rank = {c: r for r, c in enumerate(t1_sorted, 1)}
    t2_rank = {c: r for r, c in enumerate(t2_sorted, 1)}
    rho = spearman_rho(t1_rank, t2_rank, CATEGORIES)
    print(f"\nSpearman ρ (cross-model spread ranking, t1 vs t2): {rho:.3f}")

    # v0.6 predicted ordering: pf > olive > pm > skin > running
    v06_predicted = ["finance", "oliveoil", "pm", "skincare", "running"]
    v06_rank = {c: r for r, c in enumerate(v06_predicted, 1)}
    rho_t1_v06 = spearman_rho(t1_rank, v06_rank, CATEGORIES)
    rho_t2_v06 = spearman_rho(t2_rank, v06_rank, CATEGORIES)
    print(f"\nSpearman ρ (t1 vs v0.6 narrative ordering): {rho_t1_v06:.3f}")
    print(f"Spearman ρ (t2 vs v0.6 narrative ordering): {rho_t2_v06:.3f}")
    print(f"\nv0.6 narrative ordering (high to low): {v06_predicted}")

    print("\n" + "=" * 78)
    print("Interpretation:")
    print("- ρ ≥ 0.7 between t1 and t2: cross-model spread ranking preserves")
    print("- ρ ≥ 0.7 between v0.9 and v0.6 narrative: original Pattern 1 ordering replicates")
    print("- This test is post-hoc; not pre-registered; reported as exploratory")
    print("=" * 78)


if __name__ == "__main__":
    main()
