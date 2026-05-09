#!/usr/bin/env python3
"""
v0.10 — Step 5–8 of Analysis Plan (pre-reg §6)

Compute r_naive,t1; r_naive,t2; |Δr_naive|; r_caveated rates; effective n per wave.
Verify n ≥ 100 floor (§3.4). Evaluate H1, H2 against pre-registered thresholds.
Compute H3 diagnostic against v0.9-reported gross Presence values.
Produce E3 sensitivity analysis. Generate canonical scoring documents.

Input:
    /Users/pablou/aias/osf/v10/data/classifications.csv

Output:
    /Users/pablou/aias/osf/v10/analysis/canonical_scoring.csv
    /Users/pablou/aias/osf/v10/analysis/canonical_scoring.json
    /Users/pablou/aias/osf/v10/analysis/sensitivity_E3.csv
    /Users/pablou/aias/osf/v10/analysis/borderline_review.csv  (rows flagged for author inspection)

Usage:
    python3 score_v10.py
"""

import csv
import json
from pathlib import Path
from datetime import datetime

V10_ROOT = Path('/Users/pablou/aias/osf/v10')
INPUT = V10_ROOT / 'data' / 'classifications.csv'
OUT_DIR = V10_ROOT / 'analysis'

# Pre-reg parameters (locked at git tag v0.10-prereg, commit 8767f44)
N_FLOOR = 100              # §3.4
H1_BAND_PP = 2.0           # §2 (H1)
WAVES = ['t1', 't2']

# v0.9-published gross Presence values for H3 diagnostic
V09_GROSS_PRESENCE = {
    't1': 44.79,  # 43/96
    't2': 41.67,  # 40/96
}


def per_wave_metrics(rows, mapping_field):
    """Compute n, n_naive, n_caveated, r_naive, r_caveated for each wave under
    the given mapping field (primary_class or e3_sensitivity_class)."""
    metrics = {}
    for w in WAVES:
        wave_rows = [r for r in rows if r['wave_v10'] == w]
        n = len(wave_rows)
        n_naive = sum(1 for r in wave_rows if r[mapping_field] == 'naive')
        n_caveated = sum(1 for r in wave_rows if r[mapping_field] == 'caveated')
        n_error = sum(1 for r in wave_rows if r[mapping_field] == 'ERROR')
        r_naive = (n_naive / n * 100) if n else None
        r_caveated = (n_caveated / n * 100) if n else None
        metrics[w] = {
            'n_matched_mint': n,
            'n_naive': n_naive,
            'n_caveated': n_caveated,
            'n_error': n_error,
            'r_naive_pct': round(r_naive, 4) if r_naive is not None else None,
            'r_caveated_pct': round(r_caveated, 4) if r_caveated is not None else None,
        }
    return metrics


def evaluate_h1(metrics, label):
    """H1: |Δr_naive| ≤ 2.0 pp at both waves, conditional on n ≥ 100 floor."""
    n_t1 = metrics['t1']['n_matched_mint']
    n_t2 = metrics['t2']['n_matched_mint']
    floor_clear = (n_t1 >= N_FLOOR and n_t2 >= N_FLOOR)
    r_t1 = metrics['t1']['r_naive_pct']
    r_t2 = metrics['t2']['r_naive_pct']
    delta = abs(r_t2 - r_t1) if (r_t1 is not None and r_t2 is not None) else None
    if not floor_clear:
        status = 'INDETERMINATE'
        rationale = (
            f'Effective-n floor (§3.4) breached: t1={n_t1}, t2={n_t2}, '
            f'required ≥ {N_FLOOR} at both waves. H1 routed to descriptive disclosure path.'
        )
    elif delta is None:
        status = 'INDETERMINATE'
        rationale = 'r_naive undefined at one or both waves (E1).'
    elif delta <= H1_BAND_PP:
        status = 'CONFIRMED'
        rationale = f'|Δr_naive| = {delta:.2f}pp ≤ {H1_BAND_PP}pp band'
    else:
        status = 'FALSIFIED'
        rationale = f'|Δr_naive| = {delta:.2f}pp > {H1_BAND_PP}pp band'
    return {
        'mapping': label,
        'r_naive_t1_pct': r_t1,
        'r_naive_t2_pct': r_t2,
        'abs_delta_pp': round(delta, 4) if delta is not None else None,
        'band_pp': H1_BAND_PP,
        'n_floor_required': N_FLOOR,
        'n_t1': n_t1,
        'n_t2': n_t2,
        'floor_cleared': floor_clear,
        'status': status,
        'rationale': rationale,
    }


def evaluate_h2(metrics, label):
    """H2: r_naive > 0 at both waves."""
    nv_t1 = metrics['t1']['n_naive']
    nv_t2 = metrics['t2']['n_naive']
    if nv_t1 > 0 and nv_t2 > 0:
        status = 'CONFIRMED'
        rationale = f'n_naive,t1={nv_t1}; n_naive,t2={nv_t2}; both > 0'
    elif nv_t1 == 0 and nv_t2 == 0:
        status = 'FALSIFIED'
        rationale = 'n_naive = 0 at both waves'
    else:
        zero_wave = 't1' if nv_t1 == 0 else 't2'
        status = 'FALSIFIED'
        rationale = f'n_naive = 0 at {zero_wave} (n_naive,t1={nv_t1}, n_naive,t2={nv_t2})'
    return {
        'mapping': label,
        'n_naive_t1': nv_t1,
        'n_naive_t2': nv_t2,
        'status': status,
        'rationale': rationale,
    }


def evaluate_h3(metrics):
    """H3 diagnostic: directional concordance with v0.9 gross Presence + magnitude ratio."""
    r_naive_t1 = metrics['t1']['r_naive_pct']
    r_naive_t2 = metrics['t2']['r_naive_pct']
    delta_naive = (r_naive_t2 - r_naive_t1) if (r_naive_t1 is not None and r_naive_t2 is not None) else None
    delta_gross = V09_GROSS_PRESENCE['t2'] - V09_GROSS_PRESENCE['t1']

    if delta_naive is None or delta_naive == 0:
        concordance = 'undefined' if delta_naive is None else 'naive_flat'
    else:
        if (delta_naive < 0) == (delta_gross < 0):
            concordance = 'concordant'
        else:
            concordance = 'decoupled'

    ratio = None
    if delta_naive is not None and delta_gross != 0:
        ratio = round(abs(delta_naive) / abs(delta_gross), 4)

    return {
        'gross_presence_t1_pct': V09_GROSS_PRESENCE['t1'],
        'gross_presence_t2_pct': V09_GROSS_PRESENCE['t2'],
        'delta_gross_pp': round(delta_gross, 4),
        'delta_naive_pp': round(delta_naive, 4) if delta_naive is not None else None,
        'directional_concordance': concordance,
        'magnitude_ratio_naive_over_gross': ratio,
        'note': 'Diagnostic only per §2 H3. No falsification status.',
    }


def surface_borderline(rows):
    """Flag rows for author inspection: ambiguous, naive (low base rate),
    or where source_quote does not contain 'mint' / 'credit karma'."""
    borderline = []
    for r in rows:
        flags = []
        if r['valence'] == 'ambiguous':
            flags.append('ambiguous_valence')
        if r['primary_class'] == 'naive':
            flags.append('naive_classification_low_base_rate')
        sq = (r.get('source_quote', '') or '').lower()
        if sq and 'mint' not in sq and 'credit karma' not in sq:
            flags.append('source_quote_lacks_target_brand')
        if r['valence'] == 'ERROR':
            flags.append('classifier_error')
        if flags:
            r2 = dict(r)
            r2['_flags'] = '|'.join(flags)
            borderline.append(r2)
    return borderline


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    with open(INPUT, encoding='utf-8') as f:
        rows = list(csv.DictReader(f))

    print('=' * 64)
    print(f'v0.10 — Score classifications')
    print(f'Generated: {datetime.now().isoformat(timespec="seconds")}')
    print('=' * 64)
    print(f'Input: {INPUT}')
    print(f'Total rows: {len(rows)}\n')

    # --- Primary mapping ---
    primary_metrics = per_wave_metrics(rows, 'primary_class')
    h1_primary = evaluate_h1(primary_metrics, 'primary')
    h2_primary = evaluate_h2(primary_metrics, 'primary')
    h3 = evaluate_h3(primary_metrics)

    # --- E3 sensitivity ---
    sensitivity_metrics = per_wave_metrics(rows, 'e3_sensitivity_class')
    h1_sensitivity = evaluate_h1(sensitivity_metrics, 'e3_sensitivity')
    h2_sensitivity = evaluate_h2(sensitivity_metrics, 'e3_sensitivity')

    # --- Per-wave summary print ---
    print('PER-WAVE METRICS (PRIMARY MAPPING):')
    print(f'{"wave":<6} {"n":>6} {"n_naive":>8} {"n_cav":>6} {"r_naive":>10} {"r_caveated":>12}')
    for w in WAVES:
        m = primary_metrics[w]
        print(f'{w:<6} {m["n_matched_mint"]:>6} {m["n_naive"]:>8} {m["n_caveated"]:>6} '
              f'{(str(m["r_naive_pct"])+"%"):>10} {(str(m["r_caveated_pct"])+"%"):>12}')

    print('\nPER-WAVE METRICS (E3 SENSITIVITY MAPPING):')
    print(f'{"wave":<6} {"n":>6} {"n_naive":>8} {"n_cav":>6} {"r_naive":>10} {"r_caveated":>12}')
    for w in WAVES:
        m = sensitivity_metrics[w]
        print(f'{w:<6} {m["n_matched_mint"]:>6} {m["n_naive"]:>8} {m["n_caveated"]:>6} '
              f'{(str(m["r_naive_pct"])+"%"):>10} {(str(m["r_caveated_pct"])+"%"):>12}')

    # --- Hypothesis outcomes ---
    print('\n' + '=' * 64)
    print('HYPOTHESIS EVALUATION')
    print('=' * 64)

    print(f'\nH1 (Stability, ±{H1_BAND_PP}pp band) — primary:')
    print(f'  status   : {h1_primary["status"]}')
    print(f'  rationale: {h1_primary["rationale"]}')

    print(f'\nH1 — E3 sensitivity:')
    print(f'  status   : {h1_sensitivity["status"]}')
    print(f'  rationale: {h1_sensitivity["rationale"]}')

    print(f'\nH2 (Persistence, r_naive > 0 at both waves) — primary:')
    print(f'  status   : {h2_primary["status"]}')
    print(f'  rationale: {h2_primary["rationale"]}')

    print(f'\nH2 — E3 sensitivity:')
    print(f'  status   : {h2_sensitivity["status"]}')
    print(f'  rationale: {h2_sensitivity["rationale"]}')

    print(f'\nH3 (Co-movement diagnostic):')
    print(f'  Δgross (v0.9): {h3["delta_gross_pp"]}pp')
    print(f'  Δnaive (v0.10 primary): {h3["delta_naive_pp"]}pp')
    print(f'  concordance  : {h3["directional_concordance"]}')
    print(f'  ratio        : {h3["magnitude_ratio_naive_over_gross"]}')

    # --- Borderline cases ---
    borderline = surface_borderline(rows)
    print(f'\n{len(borderline)} response(s) flagged for author review (see borderline_review.csv)')
    for r in borderline:
        print(f'  - {r["wave_v10"]} | {r["model_version"]} | {r["prompt_id"]} | run {r.get("run_idx","?")} | flags: {r["_flags"]}')

    # --- Write outputs ---
    canonical = {
        'meta': {
            'generated_at': datetime.now().isoformat(timespec='seconds'),
            'input_file': str(INPUT),
            'total_rows': len(rows),
            'pre_reg_lock': 'git tag v0.10-prereg, commit 8767f44, 2026-05-09',
            'deviations_log': str(V10_ROOT / 'DEVIATIONS.md'),
        },
        'metrics_primary': primary_metrics,
        'metrics_e3_sensitivity': sensitivity_metrics,
        'hypotheses': {
            'H1_primary': h1_primary,
            'H1_e3_sensitivity': h1_sensitivity,
            'H2_primary': h2_primary,
            'H2_e3_sensitivity': h2_sensitivity,
            'H3_diagnostic': h3,
        },
        'borderline_count': len(borderline),
    }

    json_out = OUT_DIR / 'canonical_scoring.json'
    with open(json_out, 'w') as f:
        json.dump(canonical, f, indent=2)

    # CSV summary (one row per hypothesis × mapping)
    csv_out = OUT_DIR / 'canonical_scoring.csv'
    csv_rows = []
    for label, h in [('H1_primary', h1_primary), ('H1_e3_sensitivity', h1_sensitivity)]:
        csv_rows.append({
            'hypothesis': 'H1', 'mapping': h['mapping'],
            'r_naive_t1_pct': h['r_naive_t1_pct'], 'r_naive_t2_pct': h['r_naive_t2_pct'],
            'abs_delta_pp': h['abs_delta_pp'], 'band_pp': h['band_pp'],
            'n_t1': h['n_t1'], 'n_t2': h['n_t2'], 'floor_cleared': h['floor_cleared'],
            'status': h['status'], 'rationale': h['rationale'],
        })
    for label, h in [('H2_primary', h2_primary), ('H2_e3_sensitivity', h2_sensitivity)]:
        csv_rows.append({
            'hypothesis': 'H2', 'mapping': h['mapping'],
            'r_naive_t1_pct': primary_metrics['t1']['r_naive_pct'] if h['mapping']=='primary' else sensitivity_metrics['t1']['r_naive_pct'],
            'r_naive_t2_pct': primary_metrics['t2']['r_naive_pct'] if h['mapping']=='primary' else sensitivity_metrics['t2']['r_naive_pct'],
            'abs_delta_pp': '', 'band_pp': '',
            'n_t1': h['n_naive_t1'], 'n_t2': h['n_naive_t2'], 'floor_cleared': '',
            'status': h['status'], 'rationale': h['rationale'],
        })
    with open(csv_out, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(csv_rows[0].keys()))
        w.writeheader()
        w.writerows(csv_rows)

    # E3 sensitivity CSV (per-wave)
    sensitivity_out = OUT_DIR / 'sensitivity_E3.csv'
    sens_rows = []
    for w in WAVES:
        sens_rows.append({
            'wave': w,
            'n_total': primary_metrics[w]['n_matched_mint'],
            'r_naive_primary_pct': primary_metrics[w]['r_naive_pct'],
            'r_naive_e3_sensitivity_pct': sensitivity_metrics[w]['r_naive_pct'],
            'delta_pp': round((sensitivity_metrics[w]['r_naive_pct'] or 0) - (primary_metrics[w]['r_naive_pct'] or 0), 4),
        })
    with open(sensitivity_out, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(sens_rows[0].keys()))
        w.writeheader()
        w.writerows(sens_rows)

    # Borderline CSV
    borderline_out = OUT_DIR / 'borderline_review.csv'
    if borderline:
        with open(borderline_out, 'w', newline='') as f:
            w = csv.DictWriter(f, fieldnames=list(borderline[0].keys()))
            w.writeheader()
            w.writerows(borderline)

    print(f'\nOutputs written:')
    print(f'  {json_out}')
    print(f'  {csv_out}')
    print(f'  {sensitivity_out}')
    if borderline:
        print(f'  {borderline_out}')


if __name__ == '__main__':
    main()
