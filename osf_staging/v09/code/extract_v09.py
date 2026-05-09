"""v0.9 extraction wrapper.

Re-extracts v0.6 raw CSVs and extracts v0.9 raw CSVs using extractor.py's
function-calling brand extraction. Output is two enriched CSVs per category
(v06 + v09) ready for mode classification and analysis.

Per Decision #2 (mode classifier retroactive on t₁), we re-extract both waves
with the current extractor and current registry so t₁/t₂ are apples-to-apples
on the extraction step.

Schema normalization: v0.6 raw CSVs use (model=provider, model_version=string),
while v0.9 raw CSVs use model_slot. This wrapper derives model_slot for v0.6
rows from (model, model_version) so mode_classifier.py and analyze_v09.py see
a consistent schema across both waves. A 'wave' column is added to every row.

Usage:
    cd ~/aias
    python3 extract_v09.py                       # all 5 categories, both waves
    python3 extract_v09.py --category pm         # one category, both waves
    python3 extract_v09.py --wave v09            # all categories, one wave
    python3 extract_v09.py --category pm --wave v06  # smoke-test single combo
"""
import argparse
import csv
import glob
import json
import os
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from extractor import extract_brands

load_dotenv()

CATEGORY_DESCRIPTIONS = {
    'pm': 'project management software',
    'running': 'running shoes',
    'oliveoil': 'premium olive oil',
    'skincare': 'premium facial skincare',
    'finance': 'personal finance apps',
}

# Map (provider, model_version) -> slot_key. Mirrors MODELS dict in run_aias_v2.py.
PROVIDER_VERSION_TO_SLOT = {
    ('anthropic', 'claude-sonnet-4-6'): 'anthropic_sonnet',
    ('anthropic', 'claude-opus-4-7'):   'anthropic_opus',
    ('openai',    'gpt-5.4-mini'):      'openai_mini',
    ('openai',    'gpt-5.5'):           'openai_flagship',
    ('google',    'gemini-2.5-flash'):  'google_flash',
    ('xai',       'grok-4-1-fast'):     'xai_grok',
}

ENRICHED_COLS = [
    'brands_canonical', 'brands_unknown', 'brands_ranked',
    'primary_recommendation', 'sentiment_summary', 'extraction_method',
]


def load_registry(category):
    path = Path('registries') / f'brands_{category}.json'
    with open(path) as f:
        data = json.load(f)
    return data if isinstance(data, list) else data['brands']


def normalize_v06_row(row):
    """Add model_slot to v0.6 rows derived from (model, model_version)."""
    if 'model_slot' in row and row['model_slot']:
        return row
    key = (row.get('model', ''), row.get('model_version', ''))
    slot = PROVIDER_VERSION_TO_SLOT.get(key)
    if slot is None:
        slot = f"unknown_{key[0]}_{key[1]}"
    row['model_slot'] = slot
    return row


def find_v06_raw(category):
    """v0.6 raw CSV: results_v2_<ts>.csv (no category in filename)."""
    candidates = sorted(glob.glob(f'data/{category}/results_v2_2026*.csv'))
    candidates = [c for c in candidates if 'rerun' not in c and 'enriched' not in c]
    return candidates[-1] if candidates else None


def find_v09_raw(category):
    """v0.9 raw + reruns: results_v2_<cat>_<ts>.csv plus _rerun_*.csv."""
    pattern = f'data/{category}/results_v2_{category}_2026*.csv'
    csvs = sorted(glob.glob(pattern))
    csvs = [c for c in csvs if 'enriched' not in c]
    if not csvs:
        return []
    originals = [c for c in csvs if 'rerun' not in c]
    reruns = [c for c in csvs if 'rerun' in c]
    if not originals:
        return []
    return [originals[-1]] + reruns


def merge_v09_csvs(paths):
    """Merge primary CSV with reruns; reruns overwrite when call_status == 'ok'."""
    primary, *reruns = paths
    with open(primary) as f:
        merged = {(r['prompt_id'], r['model_slot'], r['run_idx']): r
                  for r in csv.DictReader(f)}
    for rp in reruns:
        with open(rp) as f:
            for r in csv.DictReader(f):
                if r.get('call_status') == 'ok':
                    merged[(r['prompt_id'], r['model_slot'], r['run_idx'])] = r
    return list(merged.values())


def extract_wave(category, raw_rows, wave, output_path, openai_client, brands, category_description):
    """Run extraction over raw_rows. Adds wave column. Writes enriched CSV."""
    n_total = len(raw_rows)
    enriched_rows = []
    n_extracted = 0
    n_skipped_empty = 0
    n_failed = 0

    for i, row in enumerate(raw_rows, 1):
        if wave == 'v06':
            row = normalize_v06_row(row)
        row['wave'] = wave

        slot = row.get('model_slot', '?')
        prompt_id = row.get('prompt_id', '?')
        run_idx = row.get('run_idx', '?')

        for col in ENRICHED_COLS:
            row.setdefault(col, '')

        # Skip empty / failed responses
        if not row.get('raw_response', '').strip() or row.get('call_status') != 'ok':
            row['extraction_method'] = 'skipped_empty_or_failed'
            enriched_rows.append(row)
            n_skipped_empty += 1
            print(f'  [{i:4d}/{n_total}] {prompt_id:14s} | {slot:18s} | run {run_idx} -> SKIP (empty/failed)')
            continue

        try:
            extracted = extract_brands(row['raw_response'], brands, openai_client, category_description)
            seen = set()
            deduped = []
            for e in extracted:
                key = e.get('canonical') or f"UNK:{e.get('raw_mention', '').lower()}"
                if key in seen:
                    continue
                seen.add(key)
                deduped.append(e)

            canonicals = [e['canonical'] for e in deduped if e.get('canonical')]
            unknowns = [e.get('raw_mention', '') for e in deduped if not e.get('canonical')]
            ranked = sorted(deduped, key=lambda x: x.get('rank', 999))
            ranked_names = [
                e.get('canonical') or f"[unk]{e.get('raw_mention', '')}"
                for e in ranked
            ]
            primary = next(
                (e.get('canonical') for e in deduped if e.get('is_primary_recommendation')),
                ''
            )
            sentiments = [
                f"{e.get('canonical') or e.get('raw_mention', '')}:{e.get('sentiment', '')}"
                for e in deduped
            ]

            row['brands_canonical'] = '|'.join(canonicals)
            row['brands_unknown'] = '|'.join(unknowns)
            row['brands_ranked'] = '|'.join(ranked_names)
            row['primary_recommendation'] = primary
            row['sentiment_summary'] = '|'.join(sentiments)
            row['extraction_method'] = 'function_calling'

            n_extracted += 1
            print(f'  [{i:4d}/{n_total}] {prompt_id:14s} | {slot:18s} | run {run_idx} -> {len(canonicals)} canon, {len(unknowns)} unk')

        except Exception as e:
            row['extraction_method'] = f'error:{type(e).__name__}'
            n_failed += 1
            print(f'  [{i:4d}/{n_total}] {prompt_id:14s} | {slot:18s} | run {run_idx} -> EXTRACTION FAILED: {type(e).__name__}: {str(e)[:60]}')

        enriched_rows.append(row)

    # Write enriched CSV — union of all keys to handle schema drift cleanly
    if enriched_rows:
        all_cols = []
        seen_cols = set()
        for r in enriched_rows:
            for k in r.keys():
                if k not in seen_cols:
                    seen_cols.add(k)
                    all_cols.append(k)
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, fieldnames=all_cols, extrasaction='ignore')
            w.writeheader()
            for r in enriched_rows:
                w.writerow(r)

    print(f'\n  Summary: {n_extracted} extracted, {n_skipped_empty} skipped, {n_failed} failed')
    print(f'  Wrote {len(enriched_rows)} rows to {output_path}')


def main():
    parser = argparse.ArgumentParser(description='v0.9 extraction wrapper')
    parser.add_argument('--category', choices=list(CATEGORY_DESCRIPTIONS.keys()),
                        help='Process only this category (default: all 5)')
    parser.add_argument('--wave', choices=['v06', 'v09'],
                        help='Process only this wave (default: both)')
    args = parser.parse_args()

    categories = [args.category] if args.category else list(CATEGORY_DESCRIPTIONS.keys())
    waves = [args.wave] if args.wave else ['v06', 'v09']

    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        sys.exit('ERROR: OPENAI_API_KEY not in environment.')
    client = OpenAI(api_key=api_key)
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')

    print('=' * 78)
    print(f'v0.9 Extraction Wrapper')
    print(f'Categories: {categories}')
    print(f'Waves:      {waves}')
    print(f'Started:    {datetime.now().isoformat(timespec="seconds")}')
    print('=' * 78)

    for cat in categories:
        cat_desc = CATEGORY_DESCRIPTIONS[cat]
        brands = load_registry(cat)
        print(f'\n{"=" * 78}')
        print(f'Category: {cat} ({cat_desc}) — registry: {len(brands)} brands')
        print('=' * 78)

        for wave in waves:
            if wave == 'v06':
                raw_path = find_v06_raw(cat)
                if not raw_path:
                    print(f'\n  v0.6 ({cat}): no raw CSV found, skipping')
                    continue
                with open(raw_path) as f:
                    rows = list(csv.DictReader(f))
                output_path = f'data/{cat}/results_enriched_v06_{ts}.csv'
                print(f'\n  Wave: v0.6 (t₁) — re-extracting {len(rows)} rows from {raw_path}')
            else:  # v09
                paths = find_v09_raw(cat)
                if not paths:
                    print(f'\n  v0.9 ({cat}): no raw CSV found, skipping')
                    continue
                rows = merge_v09_csvs(paths)
                output_path = f'data/{cat}/results_enriched_v09_{ts}.csv'
                print(f'\n  Wave: v0.9 (t₂) — extracting {len(rows)} rows from {len(paths)} CSVs (merged)')

            extract_wave(cat, rows, wave, output_path, client, brands, cat_desc)

    print(f'\n{"=" * 78}')
    print(f'Extraction complete at {datetime.now().isoformat(timespec="seconds")}')
    print('=' * 78)


if __name__ == '__main__':
    main()
