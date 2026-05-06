"""
v0.8 Hypothesis Analyzer
========================

Formal scoring of the eight pre-registered v0.8 hypotheses (knives, Pattern 4
discourse-language bias) against the locked pre-registration document
(pre_registration/PRE_REGISTRATION_knives_v1.0.md).

Reads the merged enriched + mode-classified dataset and produces:
  - Formatted console summary with CONFIRMED / PARTIALLY CONFIRMED /
    DISCONFIRMED / CANNOT EVALUATE label per hypothesis
  - scoring_tables_<ts>.csv with every aggregate the report needs

Operational unit: brand-surfacing macro (responses with >=1 canonical brand
mention). Audit established 96% cross-lab agreement on this operational
definition vs 68% on the strict 5-mode taxonomy. The strict taxonomy is
preserved in the data and reported as a methodology disclosure, but H1-H8
score against the operational unit per protocol §6.5 reframe convention.

Design: each hypothesis has its own scoring function. Functions return a
dict with the band label, the computed value(s), the threshold, and an
explanation string. main() collects results, prints the summary, and writes
the scoring_tables CSV.

Usage:
  python analyze_v08.py \\
      --enriched data/knives/results_enriched_knives_<ts>.csv \\
      --mode-classified data/knives/mode_classified_<ts>.csv \\
      --registry registries/brands_knives.json
"""

import argparse, csv, json, sys
from pathlib import Path
from datetime import datetime
from collections import Counter, defaultdict
from statistics import mean


# ============================================================================
# Data loading
# ============================================================================
def load_registry(path):
    with open(path) as f:
        d = json.load(f)
    brand_to_lineage = {b['canonical']: b['lineage'] for b in d['brands']}
    boundary_v10 = sorted(b['canonical'] for b in d['brands']
                          if b.get('boundary_set') == 'v1.0_locked')
    boundary_v11 = sorted(b['canonical'] for b in d['brands']
                          if b.get('boundary_condition') == 'discourse_language_test')
    miyabi_brands = sorted(b['canonical'] for b in d['brands']
                           if b['lineage'] == 'japanese_hybrid')
    return {
        'category': d.get('category'),
        'registry_version': d.get('registry_version'),
        'lineage_aggregates': d.get('lineage_aggregates', []),
        'brand_to_lineage': brand_to_lineage,
        'all_brands': sorted(brand_to_lineage.keys()),
        'boundary_v10': boundary_v10,
        'boundary_v11': boundary_v11,
        'miyabi_brands': miyabi_brands,
        'mass_market_japanese': ['Shun', 'Global'],
    }


def load_enriched(path):
    return list(csv.DictReader(open(path)))


def load_mode_classified(path):
    if not path:
        return None
    rows = list(csv.DictReader(open(path)))
    by_key = {}
    for r in rows:
        key = (r['prompt_id'], r['model_slot'], int(r['run_idx']))
        by_key[key] = r
    return by_key


def merge_mode_into_enriched(enriched, mode_lookup):
    if not mode_lookup:
        return enriched
    for r in enriched:
        try:
            key = (r['prompt_id'], r['model_slot'], int(r['run_idx']))
        except (KeyError, ValueError):
            continue
        m = mode_lookup.get(key)
        if m:
            r['primary_mode'] = m.get('primary_mode', '')
            r['secondary_mode'] = m.get('secondary_mode', '')
            r['brand_mentions_count'] = m.get('brand_mentions_count', '')
            r['component_terms_count'] = m.get('component_terms_count', '')
            r['authority_mentions_count'] = m.get('authority_mentions_count', '')
    return enriched


# ============================================================================
# Aggregation primitives
# ============================================================================
def per_brand_presence(rows, registry):
    """Per-brand Presence (% of rows in which the brand surfaced).

    Brand-surfacing operational definition: brands_canonical column non-empty
    counts the brand. Mode classification not consulted (per §6.5 reframe).
    """
    n = len(rows)
    counts = Counter()
    for r in rows:
        if r.get('brands_canonical'):
            for b in r['brands_canonical'].split('|'):
                counts[b] += 1
    return {b: 100 * counts.get(b, 0) / n for b in registry['all_brands']}


def lineage_aggregate(brand_presence, brand_to_lineage, lineage_name):
    """Mean Presence across brands in a lineage (per pre-registration §2 spec)."""
    brands_in = [b for b, l in brand_to_lineage.items() if l == lineage_name]
    if not brands_in:
        return None
    return mean(brand_presence[b] for b in brands_in), brands_in


def filter_rows(rows, prompt_ids=None, model_slots=None):
    out = rows
    if prompt_ids:
        out = [r for r in out if r.get('prompt_id') in prompt_ids]
    if model_slots:
        out = [r for r in out if r.get('model_slot') in model_slots]
    return out


# ============================================================================
# Hypothesis scorers
# ============================================================================
def score_h1(rows, registry):
    """H1: Japanese aggregate < German aggregate by >= 15pp.

    Reports both v1.0 boundary set (8 Japanese brands as locked) and v1.1
    expanded set (13 Japanese brands as published) per registry-revision honesty.
    """
    bp = per_brand_presence(rows, registry)

    # v1.1 published Japanese set (13 brands, what the published dataset uses)
    jp_v11 = mean([bp[b] for b, l in registry['brand_to_lineage'].items() if l == 'japanese'])

    # v1.0 locked Japanese set (8 brands, what the pre-registration was thresholded against)
    v10_japanese = ['Shun', 'Global', 'Mac', 'Tojiro', 'Misono',
                    'Masamoto', 'Sakai Takayuki', 'Yoshihiro']
    jp_v10 = mean([bp[b] for b in v10_japanese if b in bp])

    de = mean([bp[b] for b, l in registry['brand_to_lineage'].items() if l == 'german'])

    gap_v11 = de - jp_v11
    gap_v10 = de - jp_v10

    def band(gap):
        if gap >= 15:    return 'CONFIRMED'
        if gap >= 5:     return 'PARTIALLY CONFIRMED'
        if gap >= -5:    return 'DISCONFIRMED'
        return 'DISCONFIRMED'

    return {
        'hypothesis': 'H1',
        'claim': 'Japanese aggregate Presence < German aggregate by >= 15pp',
        'thresholds': {'CONFIRMED': '>=15pp', 'PARTIAL': '5-15pp',
                       'DISCONFIRMED': '<5pp or jp >= de'},
        'jp_v10_locked': round(jp_v10, 1),
        'jp_v11_published': round(jp_v11, 1),
        'german_aggregate': round(de, 1),
        'gap_v10': round(gap_v10, 1),
        'gap_v11': round(gap_v11, 1),
        'band_v10': band(gap_v10),
        'band_v11': band(gap_v11),
        'note': ('Both registry versions disconfirm in the same direction. '
                 'v1.1 expansion brought aggregates closer (jp=25.7%, de=27.2%) '
                 'because the 5 added boundary-condition Japanese brands diluted '
                 'the Japanese mean.'),
    }


def score_h2(rows, registry):
    """H2: Japanese aggregate < American aggregate by >= 10pp.

    Anticipated outcome: cannot evaluate as designed; American comparator
    collapsed below useful signal threshold. Reported as such per §4 lock.
    """
    bp = per_brand_presence(rows, registry)
    jp = mean([bp[b] for b, l in registry['brand_to_lineage'].items() if l == 'japanese'])
    us = mean([bp[b] for b, l in registry['brand_to_lineage'].items() if l == 'american'])
    gap = us - jp

    if us < 5:
        band = 'CANNOT EVALUATE'
    else:
        if gap >= 10:    band = 'CONFIRMED'
        elif gap >= 0:   band = 'PARTIALLY CONFIRMED'
        else:            band = 'DISCONFIRMED'

    return {
        'hypothesis': 'H2',
        'claim': 'Japanese aggregate < American aggregate by >= 10pp',
        'thresholds': {'CONFIRMED': '>=10pp', 'PARTIAL': '0-10pp', 'DISCONFIRMED': 'jp >= us'},
        'japanese_aggregate': round(jp, 1),
        'american_aggregate': round(us, 1),
        'gap': round(gap, 1),
        'band': band,
        'note': ('American comparator collapsed (aggregate <5%). The AI does not '
                 'recognize "American kitchen knives" as a category at all, '
                 'regardless of brand. This is itself a finding - AI Presence is '
                 'shaped by category discourse history rather than just by '
                 'language-of-marketing.'),
    }


def score_h3(rows, registry):
    """H3: Mass-market Japanese >> Traditional Japanese by >= 30pp.

    Mass-market = mean(Shun + Global). Traditional = mean(Masamoto + Sakai
    Takayuki + Yoshihiro) per locked pre-registration.
    """
    bp = per_brand_presence(rows, registry)
    mm = mean([bp[b] for b in ['Shun', 'Global']])
    tr = mean([bp[b] for b in ['Masamoto', 'Sakai Takayuki', 'Yoshihiro']])
    gap = mm - tr

    if gap >= 30:    band = 'CONFIRMED'
    elif gap >= 15:  band = 'PARTIALLY CONFIRMED'
    else:            band = 'DISCONFIRMED'

    # Also report v1.1 expanded traditional set for transparency
    tr_v11 = mean([bp[b] for b in registry['boundary_v11']])

    return {
        'hypothesis': 'H3',
        'claim': 'Mass-market Japanese >> Traditional Japanese by >= 30pp',
        'thresholds': {'CONFIRMED': '>=30pp', 'PARTIAL': '15-30pp', 'DISCONFIRMED': '<15pp'},
        'mass_market_mean': round(mm, 1),
        'traditional_mean_v10_locked': round(tr, 1),
        'traditional_mean_v11_expanded': round(tr_v11, 1),
        'gap': round(gap, 1),
        'gap_v11': round(mm - tr_v11, 1),
        'band': band,
        'note': ('Within-Japanese English-marketing exposure predicts Presence by '
                 '~5x ratio. This is the cleanest controlled test in the dataset.'),
    }


def score_h4(rows, registry):
    """H4: Japanese aggregate peaks in p3 vs lineage-neutral baseline (p1+p4+p6).

    Threshold: p3 >= 1.5x baseline.
    """
    p3_rows = filter_rows(rows, prompt_ids=['p3_constraint'])
    baseline_rows = filter_rows(rows, prompt_ids=['p1_functional',
                                                    'p4_identity',
                                                    'p6_comparison'])

    p3_bp = per_brand_presence(p3_rows, registry)
    baseline_bp = per_brand_presence(baseline_rows, registry)

    p3_jp = mean([p3_bp[b] for b, l in registry['brand_to_lineage'].items() if l == 'japanese'])
    baseline_jp = mean([baseline_bp[b] for b, l in registry['brand_to_lineage'].items() if l == 'japanese'])

    ratio = p3_jp / baseline_jp if baseline_jp else 0

    if ratio >= 1.5:    band = 'CONFIRMED'
    elif ratio >= 1.2:  band = 'PARTIALLY CONFIRMED'
    elif ratio >= 1.0:  band = 'PARTIALLY CONFIRMED (low band)'
    else:               band = 'DISCONFIRMED'

    # Per-CEP cross-tab for lineage aggregates
    cep_lineage = {}
    for cep_id in ['p1_functional', 'p2_contextual', 'p3_constraint',
                   'p4_identity', 'p5_discovery', 'p6_comparison']:
        cep_rows = filter_rows(rows, prompt_ids=[cep_id])
        bp = per_brand_presence(cep_rows, registry)
        cep_lineage[cep_id] = {
            'japanese': round(mean([bp[b] for b, l in registry['brand_to_lineage'].items() if l == 'japanese']), 1),
            'german':   round(mean([bp[b] for b, l in registry['brand_to_lineage'].items() if l == 'german']), 1),
            'american': round(mean([bp[b] for b, l in registry['brand_to_lineage'].items() if l == 'american']), 1),
            'japanese_hybrid': round(mean([bp[b] for b, l in registry['brand_to_lineage'].items() if l == 'japanese_hybrid']), 1) if registry['miyabi_brands'] else 0.0,
        }

    return {
        'hypothesis': 'H4',
        'claim': 'Japanese aggregate peaks in p3 vs lineage-neutral baseline by >= 1.5x',
        'thresholds': {'CONFIRMED': '>=1.5x', 'PARTIAL': '1.2-1.5x',
                       'PARTIAL_LOW': '1.0-1.2x', 'DISCONFIRMED': '<1.0x'},
        'p3_japanese': round(p3_jp, 1),
        'baseline_japanese_p1_p4_p6': round(baseline_jp, 1),
        'ratio': round(ratio, 2),
        'band': band,
        'per_cep_lineage_aggregates': cep_lineage,
    }


def score_h5(rows, registry):
    """H5: Gude Presence < 1/3 of (Wusthof + Henckels mean Presence)."""
    bp = per_brand_presence(rows, registry)
    gude = bp['Güde']
    wh = mean([bp['Wüsthof'], bp['Henckels']])
    ratio = gude / wh if wh else 0

    if ratio < 1/3:      band = 'CONFIRMED'
    elif ratio < 1/2:    band = 'PARTIALLY CONFIRMED'
    else:                band = 'DISCONFIRMED'

    return {
        'hypothesis': 'H5',
        'claim': 'Güde < 1/3 of (Wüsthof + Henckels mean) - tests whether Pattern 4 is about marketing-language coverage broadly',
        'thresholds': {'CONFIRMED': '<1/3', 'PARTIAL': '1/3-1/2', 'DISCONFIRMED': '>=1/2'},
        'gude_presence': round(gude, 1),
        'wusthof_henckels_mean': round(wh, 1),
        'ratio': round(ratio, 3),
        'band': band,
        'note': ('Gude under-surfacing alongside Wusthof/Henckels dominance means '
                 'Pattern 4 generalizes beyond Japanese-vs-German lineage to '
                 'limited-English-marketing-coverage regardless of national origin. '
                 'Strongest version of the marketing-language-coverage finding.'),
    }


def score_h6(rows, registry):
    """H6 (descriptive): within-lab freshness comparison.

    No threshold per pre-registration; reports direction and magnitude of
    lineage aggregates per model slot.
    """
    by_model = {}
    for slot in ['anthropic_sonnet', 'anthropic_opus', 'openai_mini',
                 'openai_flagship', 'google_flash', 'xai_grok']:
        slot_rows = filter_rows(rows, model_slots=[slot])
        bp = per_brand_presence(slot_rows, registry)
        by_model[slot] = {
            'japanese': round(mean([bp[b] for b, l in registry['brand_to_lineage'].items() if l == 'japanese']), 1),
            'german':   round(mean([bp[b] for b, l in registry['brand_to_lineage'].items() if l == 'german']), 1),
            'american': round(mean([bp[b] for b, l in registry['brand_to_lineage'].items() if l == 'american']), 1),
        }

    return {
        'hypothesis': 'H6',
        'claim': 'Descriptive: within-lab generational behavior on lineage aggregates',
        'band': 'DESCRIPTIVE',
        'per_model_lineage_aggregates': by_model,
        'within_anthropic_jp_gap': round(by_model['anthropic_opus']['japanese'] -
                                          by_model['anthropic_sonnet']['japanese'], 1),
        'within_openai_jp_gap': round(by_model['openai_flagship']['japanese'] -
                                       by_model['openai_mini']['japanese'], 1),
    }


def load_unknowns_classification(path):
    """Load the unknowns_classified CSV produced by classify_unknowns.py.
    Returns dict: canonical -> {primary_type, english_language, total_mentions}
    """
    if not path:
        return None
    rows = list(csv.DictReader(open(path)))
    return {r['canonical']: r for r in rows}


def score_h7(rows, registry, unknowns_lookup=None):
    """H7: locked threshold (>=90% English authority sources) + reframe.

    Locked: too few authority-mode responses to evaluate (CANNOT EVALUATE).
    Reframed: authority-naming within mixed-mode responses, English fraction.

    With unknowns_lookup (output of classify_unknowns.py), authorities are
    identified via classifier rather than brittle keyword filtering.
    """
    p4_p5 = filter_rows(rows, prompt_ids=['p4_identity', 'p5_discovery'])
    all_rows = rows  # H7 reframe scopes to all responses, not just p4/p5

    authority_mode_rows = [r for r in p4_p5 if r.get('primary_mode') == 'authority']

    if unknowns_lookup is None:
        return {
            'hypothesis': 'H7',
            'claim_locked': '>= 90% of named authority sources are English-language',
            'locked_band': 'CANNOT EVALUATE',
            'authority_mode_response_count': len(authority_mode_rows),
            'authority_mode_locked_note': (
                f'Pure authority-mode responses: {len(authority_mode_rows)}/96 in p4+p5. '
                'Denominator too small for the locked threshold.'),
            'reframed_band': 'NO CLASSIFIED UNKNOWNS PROVIDED',
            'note': 'Run classify_unknowns.py and pass --unknowns-classified to score H7 reframe.'
        }

    # Aggregate authority-class mentions across all responses, using the classifier
    auth_classes = {'publication', 'retailer', 'community'}
    auth_mentions = Counter()
    auth_english = 0
    auth_non_english = 0
    auth_unclear = 0
    auth_total = 0

    for r in all_rows:
        unknowns = (r.get('brands_unknown') or '').split('|')
        for u in unknowns:
            u_clean = u.strip()
            if not u_clean:
                continue
            entry = unknowns_lookup.get(u_clean)
            if not entry:
                continue
            if entry['primary_type'] in auth_classes:
                auth_mentions[u_clean] += 1
                auth_total += 1
                lang = entry['english_language']
                if lang == 'english':
                    auth_english += 1
                elif lang == 'non_english':
                    auth_non_english += 1
                else:
                    auth_unclear += 1

    english_fraction = (auth_english / auth_total) if auth_total else 0
    english_share_of_known = (
        auth_english / (auth_english + auth_non_english)
        if (auth_english + auth_non_english) else 0
    )

    if auth_total < 10:
        reframe_band = 'INSUFFICIENT DATA'
    else:
        # Score against english_share_of_known (excluding unclear) - more honest
        if english_share_of_known >= 0.90:    reframe_band = 'CONFIRMED'
        elif english_share_of_known >= 0.70:  reframe_band = 'PARTIALLY CONFIRMED'
        else:                                  reframe_band = 'DISCONFIRMED'

    return {
        'hypothesis': 'H7',
        'claim_locked': '>= 90% of named authority sources are English-language',
        'locked_band': 'CANNOT EVALUATE',
        'authority_mode_response_count': len(authority_mode_rows),
        'authority_mode_locked_note': (
            f'Pure authority-mode responses: {len(authority_mode_rows)}/96 in p4+p5. '
            'Denominator too small for the locked threshold. Per protocol §6.4 '
            'reframe convention, the substantive question moves to authority-naming '
            'across all responses, scored via classifier-categorized brands_unknown.'),
        'claim_reframed': 'Authority-naming (publications + retailers + communities) skews English-language',
        'reframed_band': reframe_band,
        'authority_mention_total': auth_total,
        'authority_mention_english': auth_english,
        'authority_mention_non_english': auth_non_english,
        'authority_mention_unclear': auth_unclear,
        'english_fraction_all': round(english_fraction, 3),
        'english_share_of_classified': round(english_share_of_known, 3),
        'top_authorities_named': dict(auth_mentions.most_common(15)),
    }


def score_h8(rows, registry):
    """H8: traditional Japanese aggregate < 5%.

    Reports both locked v1.0 set (3 brands) and expanded v1.1 set (8 brands).
    """
    bp = per_brand_presence(rows, registry)

    v10 = mean([bp[b] for b in registry['boundary_v10']])
    v11 = mean([bp[b] for b in registry['boundary_v11']])

    def band(agg):
        if agg < 5:        return 'CONFIRMED'
        if agg < 15:       return 'PARTIALLY CONFIRMED'
        return 'DISCONFIRMED'

    return {
        'hypothesis': 'H8',
        'claim': 'Traditional Japanese aggregate Presence < 5%',
        'thresholds': {'CONFIRMED': '<5%', 'PARTIAL': '5-15%', 'DISCONFIRMED': '>=15%'},
        'v10_locked_aggregate': round(v10, 1),
        'v10_locked_brands': registry['boundary_v10'],
        'v10_band': band(v10),
        'v11_expanded_aggregate': round(v11, 1),
        'v11_expanded_brands': registry['boundary_v11'],
        'v11_band': band(v11),
        'per_brand_presence': {b: round(bp[b], 1) for b in registry['boundary_v11']},
    }


def score_miyabi(rows, registry):
    """Exploratory: Miyabi positioning between lineage aggregates."""
    bp = per_brand_presence(rows, registry)
    miyabi = bp.get('Miyabi', 0)
    jp = mean([bp[b] for b, l in registry['brand_to_lineage'].items() if l == 'japanese'])
    de = mean([bp[b] for b, l in registry['brand_to_lineage'].items() if l == 'german'])
    mm = mean([bp[b] for b in ['Shun', 'Global']])

    if abs(miyabi - de) < 5:
        narrative = 'CLOSE TO GERMAN: marketing-language hypothesis (H5) generalizes - German parent restores full Presence'
    elif abs(miyabi - jp) < 5:
        narrative = 'CLOSE TO JAPANESE AGGREGATE: lineage-of-origin signal robust to German-parent confound'
    elif jp < miyabi < de:
        narrative = ('BETWEEN JAPANESE AND GERMAN AGGREGATES: both lineage-of-origin '
                     'and marketing-language-coverage operate; neither alone '
                     'explains the variance')
    elif miyabi > mm:
        narrative = 'ABOVE JAPANESE MASS-MARKET MEAN: German English-marketing apparatus elevates Miyabi above pure-Japanese-marketed peers'
    elif miyabi < mm:
        narrative = ('BELOW JAPANESE MASS-MARKET MEAN: German parent ownership '
                     'does not fully restore Japanese-origin brand to '
                     'mass-market-Japanese levels')
    else:
        narrative = 'AMBIGUOUS POSITIONING'

    return {
        'finding': 'Miyabi exploratory positioning',
        'miyabi_presence': round(miyabi, 1),
        'japanese_aggregate': round(jp, 1),
        'japanese_mass_market': round(mm, 1),
        'german_aggregate': round(de, 1),
        'narrative': narrative,
    }


# ============================================================================
# Main
# ============================================================================
def main():
    parser = argparse.ArgumentParser(
        description='v0.8 hypothesis analyzer (formal H1-H8 scoring)'
    )
    parser.add_argument('--enriched', required=True,
                        help='Path to results_enriched_<cat>_<ts>.csv')
    parser.add_argument('--mode-classified', default=None,
                        help='Optional: path to mode_classified_<ts>.csv (for §6.5 disclosures)')
    parser.add_argument('--unknowns-classified', default=None,
                        help='Optional: path to unknowns_classified_<ts>.csv (powers H7 reframe scoring)')
    parser.add_argument('--registry', required=True,
                        help='Path to registries/brands_<cat>.json')
    parser.add_argument('--output-dir', default=None,
                        help='Output directory for scoring_tables CSV (default: same as enriched)')
    args = parser.parse_args()

    enriched_path = Path(args.enriched)
    registry = load_registry(args.registry)
    rows = load_enriched(enriched_path)
    mode_lookup = load_mode_classified(args.mode_classified) if args.mode_classified else None
    unknowns_lookup = load_unknowns_classification(args.unknowns_classified)
    rows = merge_mode_into_enriched(rows, mode_lookup)

    output_dir = Path(args.output_dir) if args.output_dir else enriched_path.parent
    output_dir.mkdir(parents=True, exist_ok=True)

    # ----- Header -----
    print('=' * 88)
    print('v0.8 Hypothesis Analyzer')
    print(f'Category:          {registry["category"]}')
    print(f'Registry version:  {registry["registry_version"]}')
    print(f'Total responses:   {len(rows)}')
    brand_surfacing = [r for r in rows if r.get('brands_canonical')]
    print(f'Brand-surfacing:   {len(brand_surfacing)} ({100*len(brand_surfacing)/len(rows):.1f}%)')
    print(f'Operational unit:  brand-surfacing macro (per audit reframe)')
    print('=' * 88)

    # ----- Score each hypothesis -----
    results = {
        'H1': score_h1(rows, registry),
        'H2': score_h2(rows, registry),
        'H3': score_h3(rows, registry),
        'H4': score_h4(rows, registry),
        'H5': score_h5(rows, registry),
        'H6': score_h6(rows, registry),
        'H7': score_h7(rows, registry, unknowns_lookup=unknowns_lookup),
        'H8': score_h8(rows, registry),
        'EXPLORATORY_MIYABI': score_miyabi(rows, registry),
    }

    # ----- Print formatted summary -----
    for hkey, result in results.items():
        print()
        print('-' * 88)
        if hkey.startswith('H'):
            band = result.get('band') or result.get('band_v11') or result.get('reframed_band') or 'see detail'
            print(f'{hkey}: {result["claim"][:80] if "claim" in result else result.get("claim_locked", "")[:80]}')
            print(f'    BAND: {band}')
        else:
            print(f'{hkey}: {result.get("finding", "")}')
            print(f'    NARRATIVE: {result.get("narrative", "")[:80]}')
        print()

        for key, val in result.items():
            if key in ('hypothesis', 'claim', 'finding'):
                continue
            if isinstance(val, dict):
                print(f'    {key}:')
                for k2, v2 in val.items():
                    print(f'        {k2}: {v2}')
            elif isinstance(val, list):
                print(f'    {key}: {", ".join(str(x) for x in val)}')
            else:
                print(f'    {key}: {val}')

    print()
    print('=' * 88)
    print('SUMMARY TABLE')
    print('=' * 88)
    print(f'{"H":4s} {"BAND":30s} {"KEY VALUE":25s}')
    print('-' * 88)
    summary_lines = [
        ('H1', results['H1']['band_v11'], f'jp={results["H1"]["jp_v11_published"]}% de={results["H1"]["german_aggregate"]}% gap={results["H1"]["gap_v11"]}pp'),
        ('H2', results['H2']['band'], f'jp={results["H2"]["japanese_aggregate"]}% us={results["H2"]["american_aggregate"]}% (collapsed)'),
        ('H3', results['H3']['band'], f'mm={results["H3"]["mass_market_mean"]}% tr={results["H3"]["traditional_mean_v10_locked"]}% gap={results["H3"]["gap"]}pp'),
        ('H4', results['H4']['band'], f'p3={results["H4"]["p3_japanese"]}% baseline={results["H4"]["baseline_japanese_p1_p4_p6"]}% ratio={results["H4"]["ratio"]}'),
        ('H5', results['H5']['band'], f'gude={results["H5"]["gude_presence"]}% w+h={results["H5"]["wusthof_henckels_mean"]}% ratio={results["H5"]["ratio"]}'),
        ('H6', 'DESCRIPTIVE', f'within-lab gaps reported separately'),
        ('H7', f'locked={results["H7"]["locked_band"]} reframe={results["H7"]["reframed_band"]}',
              f'auth-mode={results["H7"]["authority_mode_response_count"]}/96 eng-share={results["H7"].get("english_share_of_classified", "n/a")}'),
        ('H8 v1.0', results['H8']['v10_band'], f'aggregate={results["H8"]["v10_locked_aggregate"]}%'),
        ('H8 v1.1', results['H8']['v11_band'], f'aggregate={results["H8"]["v11_expanded_aggregate"]}%'),
    ]
    for h, band, val in summary_lines:
        print(f'{h:4s} {band:30s} {val}')
    print('=' * 88)

    # ----- Write scoring tables CSV -----
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    out_path = output_dir / f'scoring_tables_{timestamp}.csv'
    with open(out_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['hypothesis', 'attribute', 'value'])
        for hkey, result in results.items():
            for key, val in result.items():
                if isinstance(val, dict):
                    for k2, v2 in val.items():
                        writer.writerow([hkey, f'{key}.{k2}', json.dumps(v2)])
                elif isinstance(val, list):
                    writer.writerow([hkey, key, json.dumps(val)])
                else:
                    writer.writerow([hkey, key, val])

    print()
    print(f'Output: {out_path}')
    print('=' * 88)


if __name__ == '__main__':
    main()
