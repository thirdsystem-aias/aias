#!/usr/bin/env python3
"""
v0.10 — Step 2 of Analysis Plan (pre-reg §6)

Apply v0.7 caveat-classifier (gpt-5.4-mini + tool schema) to the Mint subset
produced by filter_v10.py.

Honors pre-reg §5 "inherit v0.7 unchanged" via /v10/registries/v07_caveat_classifier.json.
See /v10/DEVIATIONS.md for the four mismatches between pre-reg description and
v0.7's actual implementation.

Source:
    /Users/pablou/aias/osf/v10/data/responses_mint.csv  (83 rows)
    /Users/pablou/aias/osf/v10/registries/v07_caveat_classifier.json (config)

Output:
    /Users/pablou/aias/osf/v10/data/classifications.csv
    /Users/pablou/aias/osf/v10/data/classifications_checkpoint.csv

Usage:
    python3 classify_v10.py --dry-run    # preview, no API calls
    python3 classify_v10.py              # live run

Robustness (inherited from v0.7 manual_review_bbb.py):
    - Saves checkpoint every 10 rows
    - 60s timeout per call
    - 1 retry on transient errors
    - Resumes from existing checkpoint
"""

import os
import csv
import json
import sys
import time
from datetime import datetime
from pathlib import Path

# --- Paths ---
V10_ROOT = Path('/Users/pablou/aias/osf/v10')
INPUT_CSV = V10_ROOT / 'data' / 'responses_mint.csv'
CONFIG_JSON = V10_ROOT / 'registries' / 'v07_caveat_classifier.json'
OUTPUT_CSV = V10_ROOT / 'data' / 'classifications.csv'
CHECKPOINT_CSV = V10_ROOT / 'data' / 'classifications_checkpoint.csv'

DRY_RUN = '--dry-run' in sys.argv

# --- Load config ---
with open(CONFIG_JSON) as f:
    config = json.load(f)

MODEL = config['model']
TEMPERATURE = config['temperature']
TIMEOUT = config['timeout_seconds']
MAX_RETRIES = config['max_retries']
SYSTEM_PROMPT = config['system_prompt']
TOOL = config['classification_tool']
PRIMARY_MAP = config['v0_10_binary_mapping']['primary_analysis']
SENSITIVITY_MAP = config['v0_10_binary_mapping']['e3_sensitivity_analysis']


def get_client():
    from dotenv import load_dotenv
    from openai import OpenAI
    load_dotenv()
    return OpenAI(api_key=os.getenv('OPENAI_API_KEY'), timeout=float(TIMEOUT))


def apply_e5_override(entity_reference, raw_response, base_class):
    """Pre-reg §5 E5: if entity_reference is successor_product/both AND
    Mint+Credit Karma appear in the same paragraph, override to caveated."""
    if entity_reference not in ('successor_product', 'both'):
        return base_class, False
    paragraphs = (raw_response or '').split('\n\n')
    for para in paragraphs:
        p_lower = para.lower()
        if 'mint' in p_lower and 'credit karma' in p_lower:
            return 'caveated', True
    return base_class, False


def classify_one(client, raw_response):
    """One classifier call with retry. Returns dict from tool-call arguments."""
    last_exc = None
    for attempt in range(MAX_RETRIES + 1):
        try:
            completion = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {'role': 'system', 'content': SYSTEM_PROMPT},
                    {'role': 'user', 'content': raw_response},
                ],
                tools=[TOOL],
                tool_choice={
                    'type': 'function',
                    'function': {'name': TOOL['function']['name']},
                },
                temperature=TEMPERATURE,
            )
            tool_call = completion.choices[0].message.tool_calls[0]
            return json.loads(tool_call.function.arguments)
        except Exception as e:
            last_exc = e
            if attempt < MAX_RETRIES:
                time.sleep(3)
    raise last_exc


def load_checkpoint():
    if not CHECKPOINT_CSV.exists():
        return []
    with open(CHECKPOINT_CSV, encoding='utf-8') as f:
        return list(csv.DictReader(f))


def save_rows(rows, path):
    if not rows:
        return
    with open(path, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def make_key(r):
    return (
        r.get('wave_v10', ''),
        r.get('prompt_id', ''),
        r.get('model_version', ''),
        str(r.get('run_idx', '')),
    )


def main():
    print('=' * 64)
    print(f'v0.10 — Apply v0.7 classifier to Mint subset')
    print(f'Mode: {"DRY RUN (no API calls)" if DRY_RUN else "LIVE (API calls)"}')
    print(f'Model: {MODEL} @ T={TEMPERATURE}, timeout={TIMEOUT}s')
    print('=' * 64)

    with open(INPUT_CSV, encoding='utf-8') as f:
        input_rows = list(csv.DictReader(f))
    print(f'Input rows: {len(input_rows)}')

    completed = load_checkpoint()
    completed_keys = {make_key(r) for r in completed}
    if completed:
        print(f'Resuming: {len(completed)} rows already classified in checkpoint')

    client = None
    if not DRY_RUN:
        client = get_client()

    output_rows = list(completed)
    valence_counts = {}
    primary_counts = {}
    sensitivity_counts = {}
    e5_triggered = 0
    failures = 0

    # Pre-tally completed
    for r in completed:
        valence_counts[r.get('valence', '')] = valence_counts.get(r.get('valence', ''), 0) + 1
        primary_counts[r.get('primary_class', '')] = primary_counts.get(r.get('primary_class', ''), 0) + 1
        sensitivity_counts[r.get('e3_sensitivity_class', '')] = sensitivity_counts.get(r.get('e3_sensitivity_class', ''), 0) + 1
        if r.get('e5_triggered') == 'True':
            e5_triggered += 1

    new_in_session = 0
    for i, row in enumerate(input_rows, 1):
        key = make_key(row)
        if key in completed_keys:
            continue

        wave = row.get('wave_v10', '?')
        prompt = row.get('prompt_id', '?')
        model = row.get('model_version', '?')
        raw = row.get('raw_response', '')

        print(f'  [{i:3d}/{len(input_rows)}] {wave} | {prompt:18s} | {model:20s}', end=' ', flush=True)

        if DRY_RUN:
            print('-> [dry run]')
            continue

        try:
            result = classify_one(client, raw)
            valence = result['valence']
            entity = result['entity_reference']
            quote = result['source_quote']
            primary = PRIMARY_MAP[valence]
            sensitivity = SENSITIVITY_MAP[valence]
            primary_after, e5_fired = apply_e5_override(entity, raw, primary)
            sensitivity_after, _ = apply_e5_override(entity, raw, sensitivity)
            if e5_fired:
                e5_triggered += 1

            valence_counts[valence] = valence_counts.get(valence, 0) + 1
            primary_counts[primary_after] = primary_counts.get(primary_after, 0) + 1
            sensitivity_counts[sensitivity_after] = sensitivity_counts.get(sensitivity_after, 0) + 1

            print(f'-> {valence:22s} | {entity:18s} | primary={primary_after}{"*" if e5_fired else ""}')
        except Exception as e:
            print(f'-> FAILED: {type(e).__name__}: {str(e)[:80]}')
            failures += 1
            valence = entity = quote = 'ERROR'
            primary_after = sensitivity_after = 'ERROR'
            e5_fired = False

        output_rows.append({
            'wave_v10': wave,
            'prompt_id': prompt,
            'cep': row.get('cep', ''),
            'model_version': model,
            'run_idx': row.get('run_idx', ''),
            'valence': valence,
            'entity_reference': entity,
            'primary_class': primary_after,
            'e3_sensitivity_class': sensitivity_after,
            'e5_triggered': str(e5_fired),
            'source_quote': quote,
            'raw_response_preview': (raw[:200] + '...') if len(raw) > 200 else raw,
        })
        new_in_session += 1
        if new_in_session % 10 == 0:
            save_rows(output_rows, CHECKPOINT_CSV)

    if not DRY_RUN:
        save_rows(output_rows, CHECKPOINT_CSV)
        save_rows(output_rows, OUTPUT_CSV)

    # --- Summary ---
    print()
    print('=' * 64)
    print(f'Classification complete{" [DRY RUN]" if DRY_RUN else ""}')
    print('=' * 64)
    print(f'Total rows: {len(output_rows)} (failures: {failures})')

    if not DRY_RUN:
        print(f'\nValence distribution (v0.7 5-class):')
        for v in ['live_recommendation', 'live_with_caveat', 'status_correction',
                  'historical_reference', 'ambiguous', 'ERROR']:
            n = valence_counts.get(v, 0)
            if n:
                print(f'  {v:25s} {n:4d}')

        print(f'\nPrimary binary class (v0.10):')
        for c in ['naive', 'caveated', 'ERROR']:
            n = primary_counts.get(c, 0)
            if n:
                print(f'  {c:25s} {n:4d}')

        print(f'\nE3 sensitivity binary class:')
        for c in ['naive', 'caveated', 'ERROR']:
            n = sensitivity_counts.get(c, 0)
            if n:
                print(f'  {c:25s} {n:4d}')

        print(f'\nE5 (successor-product framing) overrides: {e5_triggered}')
        print(f'\nOutput: {OUTPUT_CSV}')
        print(f'Checkpoint: {CHECKPOINT_CSV}')


if __name__ == '__main__':
    main()
