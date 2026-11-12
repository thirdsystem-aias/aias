# AIAS™ methodology v1.17 — How many runs are enough

Exploratory, pre-registered re-analysis of archived answers (Study B of the Nov 11, 2026 literature check). No API calls.

**Question.** How much does a brand's Presence move from run to run on the newest models, and how many runs per cell give a standard error below 0.10 and 0.05 (the benchmarks of Schulte, Bleeker and Kaufmann, arXiv 2604.07585)?

**Status (Nov 12, 2026).** Pre-registration r1 drafted; not locked. Nothing estimated on real data. Lock = tag `v1.17-prereg-r1` pushed + this folder deposited on OSF (`methodology/v1_17/`).

## Files

- `PRE_REGISTRATION_v1_17.md` — design, estimands E1–E6, outputs, reporting rule, v0.40 rule, pre-lock looks, dry run, limitations, Declarations.
- `DEVIATIONS.md` — Entry 0 (conflict-of-interest handling, ex ante).
- `LOCK_MANIFEST_v1_17.sha256` — SHA-256 of every input, script, test and document (regenerate with `scripts/make_manifest_v1_17.py` after the last edit).
- `scripts/v1_17_lib.py` — loaders and estimators.
- `scripts/analyze_v1_17.py` — `--loader-check` (counts + the published 49), `--synthetic OUT` (dry run), `--run` (real data, once; refuses before the anchor or if any input changed).
- `scripts/build_charts_v1_17.py` — the four charts; `scripts/write_note_v1_17.py` — the fixed-form results note.
- `tests/test_v1_17.py`, `tests/run_tests_v1_17.sh` — 18 tests; `tests/test_log_prelock.txt` — the pre-lock run.
- `outputs/prelock/loader_check_v1_17.json` — the only real-data output before the lock.
- `outputs/dry_run/` — synthetic dry run (known standard error), its charts and note, all marked SYNTHETIC.

## Inputs (repository root relative)

- `osf/v42/data/coded/v19_phase_b.csv` … `v23_phase_b.csv` — t4 (v0.42) coded recall answers, N3, S0/S1, 3 runs.
- `osf/v41/v41_three_wave_table.csv` — omnibus waves t1 (May 20–26), t2 (Jun 10), t3 (Nov 9, 2026), legacy six models.
- `osf/v42/v42_verdicts.json` — the published number reproduced by the loader check.
- `osf/v42/prereg/probes_v0_42.jsonl` — v0.23 code `S03` = Jack Daniel's (S-COI).

## After the lock (phase 2)

```
python3 osf/methodology/v1_17/scripts/analyze_v1_17.py --run
python3 osf/methodology/v1_17/scripts/build_charts_v1_17.py osf/methodology/v1_17/outputs/v1_17_results.json osf/methodology/v1_17/outputs/charts
python3 osf/methodology/v1_17/scripts/write_note_v1_17.py osf/methodology/v1_17/outputs/v1_17_results.json osf/methodology/v1_17/outputs/RESULTS_NOTE_v1_17.md --v040-runs R [--v040-brands N] [--v040-questions Q]
```
Python: the system `python3` (numpy, scipy, matplotlib).
