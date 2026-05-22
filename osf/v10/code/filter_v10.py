#!/usr/bin/env python3
"""
v0.10 — Step 1 of Analysis Plan (pre-reg §6)

Filter v0.9 raw responses to Mint × matched-subset across both waves.

Source files (v0.9 deposit):
    /Users/pablou/aias/osf_staging/v09/data/finance/
        results_enriched_v06_*.csv  → t1 (baseline wave)
        results_enriched_v09_*.csv  → t2 (re-baseline wave)

Output:
    /Users/pablou/aias/osf/v10/data/responses_mint.csv
        One row per matched-subset response containing a Mint mention,
        with wave_v10 ∈ {t1, t2} added for clarity.

Inclusion criteria (per pre-reg §4):
    - brand:  Mint (matched as exact token in brands_canonical pipe-delimited field)
    - models: claude-sonnet-4-6, gpt-5.4-mini
    - waves:  v06 → t1, v09 → t2

Floor check (pre-reg §3.4):
    H1 evaluable only if n_mint ≥ 100 at both waves.
    Sub-floor n routes to descriptive disclosure path.
"""

import csv
from pathlib import Path
from datetime import datetime

# --- Configuration ---
SRC_DIR = Path('/Users/pablou/aias/osf_staging/v09/data/finance')
OUT_DIR = Path('/Users/pablou/aias/osf/v10/data')
OUT_FILE = OUT_DIR / 'responses_mint.csv'

WAVE_FILES = {
    't1': SRC_DIR / 'results_enriched_v06_20260507_190816.csv',
    't2': SRC_DIR / 'results_enriched_v09_20260507_190816.csv',
}
MATCHED_MODELS = {'claude-sonnet-4-6', 'gpt-5.4-mini'}
TARGET_BRAND_TOKEN = 'mint'      # case-insensitive exact-token match
N_FLOOR = 100                    # pre-reg §3.4

# --- Logic ---

def has_mint(brands_canonical_str):
    """Exact-token match on pipe-delimited brands_canonical field. Case-insensitive."""
    if not brands_canonical_str:
        return False
    tokens = [t.strip().lower() for t in brands_canonical_str.split('|')]
    return TARGET_BRAND_TOKEN in tokens


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    out_rows = []
    summary = {}

    for wave_label, path in WAVE_FILES.items():
        if not path.exists():
            raise FileNotFoundError(f'Source file missing: {path}')
        with open(path) as f:
            rows = list(csv.DictReader(f))

        matched = [r for r in rows if r.get('model_version') in MATCHED_MODELS]
        mint_rows = [r for r in matched if has_mint(r.get('brands_canonical', ''))]

        for r in mint_rows:
            r['wave_v10'] = wave_label
            r['source_file'] = path.name
            out_rows.append(r)

        summary[wave_label] = {
            'source_file': path.name,
            'matched_subset_n': len(matched),
            'mint_n': len(mint_rows),
            'gross_presence_pct': (
                round(100 * len(mint_rows) / len(matched), 2) if matched else None
            ),
        }

    # Write filtered output
    if out_rows:
        # Use ordered union of field names from both files
        seen_fields = []
        for r in out_rows:
            for k in r.keys():
                if k not in seen_fields:
                    seen_fields.append(k)
        with open(OUT_FILE, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=seen_fields)
            writer.writeheader()
            writer.writerows(out_rows)

    # --- Summary ---
    print('=' * 64)
    print(f'v0.10 Mint subset filter — {datetime.now().isoformat(timespec="seconds")}')
    print('=' * 64)
    for wave, s in summary.items():
        print(f'\n  {wave}: {s["source_file"]}')
        print(f'    matched-subset n .... {s["matched_subset_n"]}')
        print(f'    Mint-mention n ...... {s["mint_n"]}')
        print(f'    gross presence ...... {s["gross_presence_pct"]}%')

    n_t1 = summary['t1']['mint_n']
    n_t2 = summary['t2']['mint_n']
    print('\n  --- Pre-reg §3.4 floor check ---')
    print(f'    required: n ≥ {N_FLOOR} at both waves')
    print(f'    observed: t1 = {n_t1}, t2 = {n_t2}')
    if n_t1 >= N_FLOOR and n_t2 >= N_FLOOR:
        print('    status:   FLOOR CLEARED → H1 evaluable as confirmatory')
    else:
        print('    status:   FLOOR BREACHED → H1 routed to underpowered/descriptive disclosure path')

    print(f'\n  Output: {OUT_FILE}')
    print(f'  Total Mint-bearing rows: {len(out_rows)}')


if __name__ == '__main__':
    main()
