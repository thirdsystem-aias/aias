"""v0.9 Hypothesis Analyzer

Formal scoring of the six pre-registered v0.9 hypotheses (longitudinal re-baseline
of v0.6 categories at t₂) against the locked pre-registration document
(PRE_REGISTRATION_v09_rebaseline_v1.0.md, commit f8cebbd, tag v0.9-prereg-locked).

Reads the mode-classified CSVs (which inherit all enriched columns plus mode
columns) and produces:
  - Console summary with CONFIRMED / PARTIALLY CONFIRMED / DISCONFIRMED labels
  - scoring_tables_v09_<ts>.csv compact summary
  - scoring_full_v09_<ts>.json full per-hypothesis result with all computed values

Hypotheses (per pre-reg §2):
  H1: Brand-level drift noise floor (matched subset, all 5 categories)
  H2: Top-of-leaderboard stability (matched subset, per category)
  H3: Pattern 1 replication — variance-rank Spearman ρ across categories
  H4: Mint phantom-brand decay in personal_finance (matched subset)
  H5: Pattern 4 discourse-language bias — Spanish olive oil + K-beauty
  H6: Cross-model spread stability — sonnet vs mini Pearson r per category

Mode-distribution stability is treated as exploratory observation (pre-reg §3),
not a formal hypothesis — reported separately at end of summary.

Usage:
  python analyze_v09.py
  python analyze_v09.py --spanish-olive-oil-brands "Castillo de Canena" "Hojiblanca" \\
                         --korean-skincare-brands "Sulwhasoo" "Laneige" "COSRX"

Without H5 brand annotations, H5 returns CANNOT EVALUATE (requires brand-list
input until lineage tags exist on the v0.6 registries).
"""

import argparse
import csv
import glob
import json
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from statistics import mean, pstdev


# ----- Constants ------------------------------------------------------------
CATEGORIES = ['pm', 'running', 'oliveoil', 'skincare', 'finance']
WAVES = ['v06', 'v09']
MATCHED_SUBSET = ['anthropic_sonnet', 'openai_mini']

# H4 phantom-brand spec (pre-reg §2.H4)
PHANTOM_BRAND = 'Mint'
PHANTOM_BRAND_CATEGORY = 'finance'

# H5 reference figures (pre-reg §2.H5)
# Spanish global olive oil production share per International Olive Council:
# Spain produces approximately 50% of global olive oil. Pre-reg threshold:
# Spanish brands' aggregate mention rate ≤ 25% of that share = ≤ 12.5pp.
SPANISH_OLIVE_OIL_PRODUCTION_SHARE_PCT = 50.0
SPANISH_OLIVE_OIL_THRESHOLD_PCT = 25.0 * SPANISH_OLIVE_OIL_PRODUCTION_SHARE_PCT / 100  # 12.5
KBEAUTY_THRESHOLD_PCT = 5.0


# ----- Data loading ---------------------------------------------------------
def load_registry(category):
    path = Path('registries') / f'brands_{category}.json'
    with open(path) as f:
        data = json.load(f)
    items = data if isinstance(data, list) else data['brands']
    return {
        'category': category,
        'all_brands': sorted(b['canonical'] for b in items),
        'brand_tiers': {b['canonical']: b.get('tier', 'unknown') for b in items},
    }


def load_wave(category, wave):
    """Load mode_classified CSV for a category × wave.

    Each mode_classified CSV came from one enriched CSV (one wave), so every
    row in a file shares the same wave value. We pick the latest timestamp
    where rows match the requested wave.
    """
    pattern = f'data/{category}/mode_classified_*.csv'
    candidates = sorted(glob.glob(pattern))
    for filepath in reversed(candidates):
        with open(filepath) as f:
            rows = list(csv.DictReader(f))
        if rows and rows[0].get('wave') == wave:
            return rows, filepath
    return [], None


def load_all_data():
    data = {}
    for cat in CATEGORIES:
        registry = load_registry(cat)
        for wave in WAVES:
            rows, filepath = load_wave(cat, wave)
            data[(cat, wave)] = {
                'rows': rows,
                'path': filepath,
                'registry': registry,
            }
    return data


# ----- Aggregation primitives -----------------------------------------------
def per_brand_presence(rows, registry):
    """Per-brand Presence: % of rows in which the brand surfaced.

    Operational unit: brands_canonical column non-empty counts as a surface.
    Mode classification not consulted (per v0.8 §6.5 reframe convention).
    """
    n = len(rows)
    if not n:
        return {b: 0.0 for b in registry['all_brands']}
    counts = Counter()
    for r in rows:
        if r.get('brands_canonical'):
            for b in r['brands_canonical'].split('|'):
                counts[b] += 1
    return {b: 100 * counts.get(b, 0) / n for b in registry['all_brands']}


def filter_matched(rows):
    """Filter to matched-subset model slots (sonnet + mini)."""
    return [r for r in rows if r.get('model_slot') in MATCHED_SUBSET]


def filter_slot(rows, slot):
    return [r for r in rows if r.get('model_slot') == slot]


def pearson_r(x, y):
    n = len(x)
    if n < 2:
        return 0.0
    mx, my = mean(x), mean(y)
    num = sum((xi - mx) * (yi - my) for xi, yi in zip(x, y))
    den_x = sum((xi - mx) ** 2 for xi in x) ** 0.5
    den_y = sum((yi - my) ** 2 for yi in y) ** 0.5
    if den_x == 0 or den_y == 0:
        return 0.0
    return num / (den_x * den_y)


def spearman_rho(rank_a, rank_b, items):
    """Spearman rank correlation given two rank dicts and a list of items."""
    n = len(items)
    if n < 2:
        return 0.0
    d2 = sum((rank_a[k] - rank_b[k]) ** 2 for k in items)
    return 1 - (6 * d2) / (n * (n ** 2 - 1))


# ----- Hypothesis scorers ---------------------------------------------------
def score_h1(data):
    """H1: Brand-level drift noise floor on matched subset.

    Across all 5 categories: ≥70% of registry brands within ±5pp;
    ≥90% within ±10pp.
    """
    deltas = {}
    for cat in CATEGORIES:
        v06 = filter_matched(data[(cat, 'v06')]['rows'])
        v09 = filter_matched(data[(cat, 'v09')]['rows'])
        registry = data[(cat, 'v09')]['registry']
        bp_v06 = per_brand_presence(v06, registry)
        bp_v09 = per_brand_presence(v09, registry)
        for b in registry['all_brands']:
            deltas[(cat, b)] = bp_v09[b] - bp_v06[b]

    n = len(deltas)
    within_5 = sum(1 for d in deltas.values() if abs(d) <= 5)
    within_10 = sum(1 for d in deltas.values() if abs(d) <= 10)
    pct_5 = 100 * within_5 / n if n else 0.0
    pct_10 = 100 * within_10 / n if n else 0.0

    if pct_5 >= 70 and pct_10 >= 90:    band = 'CONFIRMED'
    elif pct_5 >= 70 or pct_10 >= 90:   band = 'PARTIALLY CONFIRMED'
    else:                                band = 'DISCONFIRMED'

    sorted_by_abs = sorted(deltas.items(), key=lambda kv: abs(kv[1]), reverse=True)
    top_movers = [
        {'category': k[0], 'brand': k[1], 'delta_pp': round(v, 1)}
        for k, v in sorted_by_abs[:15]
    ]

    return {
        'hypothesis': 'H1',
        'claim': '≥70% of registry brands within ±5pp; ≥90% within ±10pp (matched subset, all 5 categories)',
        'thresholds': {
            'CONFIRMED': '≥70% within ±5pp AND ≥90% within ±10pp',
            'PARTIAL': 'one of the two thresholds met',
            'DISCONFIRMED': 'neither met',
        },
        'n_brand_deltas': n,
        'within_5pp_count': within_5,
        'within_5pp_pct': round(pct_5, 1),
        'within_10pp_count': within_10,
        'within_10pp_pct': round(pct_10, 1),
        'band': band,
        'top_movers_top15': top_movers,
    }


def score_h2(data):
    """H2: Top-3 brands at t₁ remain in top-5 at t₂ (per category, matched subset)."""
    per_cat = {}
    n_confirmed = 0
    for cat in CATEGORIES:
        v06 = filter_matched(data[(cat, 'v06')]['rows'])
        v09 = filter_matched(data[(cat, 'v09')]['rows'])
        registry = data[(cat, 'v09')]['registry']
        bp_v06 = per_brand_presence(v06, registry)
        bp_v09 = per_brand_presence(v09, registry)
        v06_top3 = sorted(bp_v06.items(), key=lambda kv: kv[1], reverse=True)[:3]
        v09_top5 = sorted(bp_v09.items(), key=lambda kv: kv[1], reverse=True)[:5]
        v09_top5_brands = {b for b, _ in v09_top5}
        all_in = all(b in v09_top5_brands for b, _ in v06_top3)
        if all_in:
            n_confirmed += 1
        per_cat[cat] = {
            'v06_top3': [{'brand': b, 'pct': round(p, 1)} for b, p in v06_top3],
            'v09_top5': [{'brand': b, 'pct': round(p, 1)} for b, p in v09_top5],
            'all_v06_top3_in_v09_top5': all_in,
        }

    if n_confirmed == 5:    band = 'CONFIRMED'
    elif n_confirmed >= 3:  band = 'PARTIALLY CONFIRMED'
    else:                   band = 'DISCONFIRMED'

    return {
        'hypothesis': 'H2',
        'claim': 'Top-3 brands at t₁ remain in top-5 at t₂ (per category, matched subset)',
        'thresholds': {'CONFIRMED': '5/5 categories', 'PARTIAL': '3-4/5', 'DISCONFIRMED': '≤2/5'},
        'categories_confirmed': n_confirmed,
        'per_category': per_cat,
        'band': band,
    }


def score_h3(data):
    """H3: Variance-rank-order Spearman ρ ≥ 0.7 between t₁ and t₂."""
    def variance(cat, wave):
        rows = filter_matched(data[(cat, wave)]['rows'])
        registry = data[(cat, wave)]['registry']
        bp = per_brand_presence(rows, registry)
        if len(bp) < 2:
            return 0.0
        return pstdev(bp.values())

    v06_var = {c: variance(c, 'v06') for c in CATEGORIES}
    v09_var = {c: variance(c, 'v09') for c in CATEGORIES}

    v06_sorted = sorted(CATEGORIES, key=lambda c: v06_var[c])
    v09_sorted = sorted(CATEGORIES, key=lambda c: v09_var[c])
    v06_rank = {c: r for r, c in enumerate(v06_sorted, 1)}
    v09_rank = {c: r for r, c in enumerate(v09_sorted, 1)}

    rho = spearman_rho(v06_rank, v09_rank, CATEGORIES)

    if rho >= 0.7:    band = 'CONFIRMED'
    elif rho >= 0.4:  band = 'PARTIALLY CONFIRMED'
    else:             band = 'DISCONFIRMED'

    return {
        'hypothesis': 'H3',
        'claim': 'Variance-rank-order across categories at t₂ has Spearman ρ ≥ 0.7 with t₁',
        'thresholds': {'CONFIRMED': 'ρ ≥ 0.7', 'PARTIAL': '0.4 ≤ ρ < 0.7', 'DISCONFIRMED': 'ρ < 0.4'},
        'spearman_rho': round(rho, 3),
        'v06_within_category_variance': {c: round(v06_var[c], 2) for c in CATEGORIES},
        'v09_within_category_variance': {c: round(v09_var[c], 2) for c in CATEGORIES},
        'v06_variance_rank_low_to_high': v06_sorted,
        'v09_variance_rank_low_to_high': v09_sorted,
        'band': band,
    }


def score_h4(data):
    """H4: Mint phantom-brand decay in personal_finance (matched subset)."""
    cat = PHANTOM_BRAND_CATEGORY
    brand = PHANTOM_BRAND
    v06 = filter_matched(data[(cat, 'v06')]['rows'])
    v09 = filter_matched(data[(cat, 'v09')]['rows'])
    registry = data[(cat, 'v09')]['registry']
    bp_v06 = per_brand_presence(v06, registry)
    bp_v09 = per_brand_presence(v09, registry)

    if brand not in bp_v06:
        return {
            'hypothesis': 'H4',
            'band': 'CANNOT EVALUATE',
            'note': f'{brand} not in {cat} registry',
        }

    t1 = bp_v06[brand]
    t2 = bp_v09[brand]
    delta = t2 - t1

    if delta <= -5:    band = 'DECAY CONFIRMED'
    elif delta < 5:    band = 'STABILITY (predicted)'
    else:              band = 'ANTI-DECAY'

    return {
        'hypothesis': 'H4',
        'claim': f'{brand} mention rate at t₂ vs t₁ in {cat}',
        'thresholds': {'DECAY': '≤ −5pp', 'STABILITY (predicted)': 'within ±5pp', 'ANTI-DECAY': '≥ +5pp'},
        'phantom_brand': brand,
        'category': cat,
        't1_presence_pct': round(t1, 1),
        't2_presence_pct': round(t2, 1),
        'delta_pp': round(delta, 1),
        'band': band,
        'note': 'Stability is the predicted outcome per pre-reg §2.H4 (corpus aging hypothesis).',
    }


def score_h5(data, spanish_brands, kbeauty_brands):
    """H5: Pattern 4 discourse-language bias replication."""
    if not spanish_brands and not kbeauty_brands:
        return {
            'hypothesis': 'H5',
            'claim': f'Spanish olive oil ≤ {SPANISH_OLIVE_OIL_THRESHOLD_PCT}pp AND K-beauty ≤ {KBEAUTY_THRESHOLD_PCT}pp (matched subset, t₂)',
            'thresholds': {
                'CONFIRMED': 'both met',
                'PARTIAL': 'one met',
                'DISCONFIRMED': 'neither met',
            },
            'band': 'CANNOT EVALUATE',
            'note': ('Spanish olive oil and K-beauty brand annotations not provided. '
                     'Pass --spanish-olive-oil-brands and --korean-skincare-brands '
                     'on the command line, or add lineage tags to the registries. '
                     f'Spanish threshold derived as 25% × {SPANISH_OLIVE_OIL_PRODUCTION_SHARE_PCT}% IOC global '
                     f'production share = {SPANISH_OLIVE_OIL_THRESHOLD_PCT}pp.'),
        }

    olive_rows = filter_matched(data[('oliveoil', 'v09')]['rows'])
    olive_reg = data[('oliveoil', 'v09')]['registry']
    olive_bp = per_brand_presence(olive_rows, olive_reg)
    spanish_in_reg = [b for b in spanish_brands if b in olive_bp]
    spanish_aggregate = mean([olive_bp[b] for b in spanish_in_reg]) if spanish_in_reg else 0.0
    spanish_passes = spanish_aggregate <= SPANISH_OLIVE_OIL_THRESHOLD_PCT

    skin_rows = filter_matched(data[('skincare', 'v09')]['rows'])
    skin_reg = data[('skincare', 'v09')]['registry']
    skin_bp = per_brand_presence(skin_rows, skin_reg)
    kbeauty_in_reg = [b for b in kbeauty_brands if b in skin_bp]
    kbeauty_aggregate = mean([skin_bp[b] for b in kbeauty_in_reg]) if kbeauty_in_reg else 0.0
    kbeauty_passes = kbeauty_aggregate <= KBEAUTY_THRESHOLD_PCT

    if spanish_passes and kbeauty_passes:    band = 'CONFIRMED'
    elif spanish_passes or kbeauty_passes:   band = 'PARTIALLY CONFIRMED'
    else:                                     band = 'DISCONFIRMED'

    return {
        'hypothesis': 'H5',
        'claim': f'Spanish olive oil ≤ {SPANISH_OLIVE_OIL_THRESHOLD_PCT}pp AND K-beauty ≤ {KBEAUTY_THRESHOLD_PCT}pp (matched subset, t₂)',
        'thresholds': {
            'CONFIRMED': 'both met',
            'PARTIAL': 'one met',
            'DISCONFIRMED': 'neither met',
        },
        'spanish_olive_oil_aggregate_pp': round(spanish_aggregate, 1),
        'spanish_olive_oil_threshold_pp': SPANISH_OLIVE_OIL_THRESHOLD_PCT,
        'spanish_olive_oil_brands_used': spanish_in_reg,
        'spanish_passes': spanish_passes,
        'kbeauty_aggregate_pp': round(kbeauty_aggregate, 1),
        'kbeauty_threshold_pp': KBEAUTY_THRESHOLD_PCT,
        'kbeauty_brands_used': kbeauty_in_reg,
        'kbeauty_passes': kbeauty_passes,
        'band': band,
        'note': (f'Spanish threshold = 25% × {SPANISH_OLIVE_OIL_PRODUCTION_SHARE_PCT}% IOC global '
                 f'production share. Brand lists supplied via CLI; move to registry lineage tags in future.'),
    }


def score_h6(data):
    """H6: Cross-model spread stability — sonnet vs mini Pearson r ≥ 0.7 per category."""
    per_cat = {}
    n_confirmed = 0
    for cat in CATEGORIES:
        v06 = data[(cat, 'v06')]['rows']
        v09 = data[(cat, 'v09')]['rows']
        registry = data[(cat, 'v09')]['registry']
        bp_sonnet_v06 = per_brand_presence(filter_slot(v06, 'anthropic_sonnet'), registry)
        bp_mini_v06 = per_brand_presence(filter_slot(v06, 'openai_mini'), registry)
        bp_sonnet_v09 = per_brand_presence(filter_slot(v09, 'anthropic_sonnet'), registry)
        bp_mini_v09 = per_brand_presence(filter_slot(v09, 'openai_mini'), registry)

        spread_v06 = [bp_sonnet_v06[b] - bp_mini_v06[b] for b in registry['all_brands']]
        spread_v09 = [bp_sonnet_v09[b] - bp_mini_v09[b] for b in registry['all_brands']]

        r = pearson_r(spread_v06, spread_v09)
        is_high = r >= 0.7
        if is_high:
            n_confirmed += 1
        per_cat[cat] = {
            'pearson_r': round(r, 3),
            'r_ge_0_7': is_high,
            'n_brands': len(registry['all_brands']),
        }

    if n_confirmed >= 4:    band = 'CONFIRMED'
    elif n_confirmed >= 2:  band = 'PARTIALLY CONFIRMED'
    else:                   band = 'DISCONFIRMED'

    return {
        'hypothesis': 'H6',
        'claim': 'Per-brand sonnet-vs-mini spread at t₂ correlates with t₁ at Pearson r ≥ 0.7 per category',
        'thresholds': {
            'CONFIRMED': '≥4/5 categories',
            'PARTIAL': '2–3/5',
            'DISCONFIRMED': '0–1/5',
        },
        'categories_confirmed': n_confirmed,
        'per_category': per_cat,
        'band': band,
    }


def exploratory_mode_distribution(data):
    """Pre-reg §3: mode-distribution stability as exploratory observation, not formal H."""
    obs = {}
    for cat in CATEGORIES:
        for wave in WAVES:
            rows = filter_matched(data[(cat, wave)]['rows'])
            modes = Counter(r.get('primary_mode', '') for r in rows)
            total = sum(modes.values())
            obs[(cat, wave)] = {
                'n_rows_matched_subset': total,
                'mode_share': {m: round(100 * c / total, 1) for m, c in modes.items()} if total else {},
            }
    # Pivot to per-category summary
    summary = {}
    for cat in CATEGORIES:
        v06 = obs[(cat, 'v06')]['mode_share']
        v09 = obs[(cat, 'v09')]['mode_share']
        all_modes = sorted(set(v06) | set(v09))
        summary[cat] = {
            m: {'v06_pct': v06.get(m, 0.0), 'v09_pct': v09.get(m, 0.0),
                'delta_pp': round(v09.get(m, 0.0) - v06.get(m, 0.0), 1)}
            for m in all_modes
        }
    return {
        'observation': 'mode_distribution',
        'note': ('Exploratory per pre-reg §3 — no thresholds. Provides v0.10 prior '
                 'for a calibrated mode-stability hypothesis.'),
        'per_category': summary,
    }


# ----- Output ---------------------------------------------------------------
def format_summary(results, exploratory):
    lines = []
    lines.append('=' * 80)
    lines.append('AIAS v0.9 Pre-Registration Outcomes')
    lines.append(f'Generated: {datetime.now().isoformat(timespec="seconds")}')
    lines.append('Pre-registration: PRE_REGISTRATION_v09_rebaseline_v1.0.md (tag v0.9-prereg-locked)')
    lines.append('=' * 80)
    band_counts = Counter()
    for r in results:
        band_counts[r.get('band', 'N/A')] += 1
        lines.append('')
        lines.append(f"{r['hypothesis']}: {r.get('claim', '')}")
        lines.append(f"  BAND: {r.get('band')}")
        for k, v in r.items():
            if k in ('hypothesis', 'claim', 'thresholds', 'band', 'note',
                     'top_movers_top15', 'per_category',
                     'v06_within_category_variance', 'v09_within_category_variance'):
                continue
            if isinstance(v, dict):
                continue
            if isinstance(v, list):
                continue
            lines.append(f"  {k}: {v}")
        if r.get('note'):
            lines.append(f"  note: {r['note']}")

    lines.append('')
    lines.append('-' * 80)
    lines.append(f'Hypothesis band totals: {dict(band_counts)}')
    lines.append('-' * 80)
    lines.append('')
    lines.append('Exploratory: mode_distribution per category (no formal threshold)')
    for cat, modes in exploratory['per_category'].items():
        biggest_shifts = sorted(
            [(m, d) for m, d in modes.items()],
            key=lambda kv: abs(kv[1].get('delta_pp', 0)), reverse=True
        )[:3]
        shifts_str = ', '.join(
            f"{m}: {d['v06_pct']}→{d['v09_pct']} ({d['delta_pp']:+.1f}pp)"
            for m, d in biggest_shifts
        )
        lines.append(f"  {cat}: {shifts_str}")

    lines.append('=' * 80)
    return '\n'.join(lines)


def write_compact_csv(results, output_path):
    rows = []
    for r in results:
        rows.append({
            'hypothesis': r.get('hypothesis', ''),
            'claim': r.get('claim', ''),
            'band': r.get('band', ''),
            'note': r.get('note', ''),
        })
    with open(output_path, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['hypothesis', 'claim', 'band', 'note'])
        w.writeheader()
        w.writerows(rows)


# ----- Main -----------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description='AIAS v0.9 hypothesis analyzer — scores H1–H6 from pre-reg.')
    parser.add_argument('--spanish-olive-oil-brands', nargs='*', default=[],
                        help='Spanish olive oil brand canonicals for H5 (e.g. "Castillo de Canena")')
    parser.add_argument('--korean-skincare-brands', nargs='*', default=[],
                        help='K-beauty / Korean skincare brand canonicals for H5')
    parser.add_argument('--output-dir', default='.',
                        help='Output directory for scoring tables and full JSON')
    args = parser.parse_args()

    print('Loading category × wave data...')
    data = load_all_data()

    missing = []
    for key, val in data.items():
        cat, wave = key
        n = len(val['rows'])
        n_matched = len(filter_matched(val['rows']))
        print(f'  {cat:10s} {wave}: {n:4d} rows ({n_matched} matched-subset) - {val["path"]}')
        if n == 0:
            missing.append(key)
    if missing:
        sys.exit(f'\nERROR: missing wave data for: {missing}')

    print('\nScoring hypotheses...\n')
    results = [
        score_h1(data),
        score_h2(data),
        score_h3(data),
        score_h4(data),
        score_h5(data, args.spanish_olive_oil_brands, args.korean_skincare_brands),
        score_h6(data),
    ]
    exploratory = exploratory_mode_distribution(data)

    summary = format_summary(results, exploratory)
    print(summary)

    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    csv_path = out_dir / f'scoring_tables_v09_{ts}.csv'
    write_compact_csv(results, csv_path)
    print(f'\nWrote compact scoring table: {csv_path}')

    json_path = out_dir / f'scoring_full_v09_{ts}.json'
    with open(json_path, 'w') as f:
        json.dump({'results': results, 'exploratory': exploratory}, f, indent=2, default=str)
    print(f'Wrote full results JSON:    {json_path}')


if __name__ == '__main__':
    main()
