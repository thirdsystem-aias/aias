# osf/aias_6_0_preview — AIAS™ 6.0 Preview (staging for osf.io/ec6wh/aias_6_0_preview/)

**Status (2026-11-10): pre-registration draft r0, not locked.** Branch `aias-6.0-preview` (from `4643d56`, the v1.14 anchor commit). No t4 answer exists; nothing here reads one.

The Preview is the provisional six-part synthesis (Presence, Consistency, Ranking, Sentiment, Coverage, Grounding) on the newest models (t4 week). It reads each component's locked unit-level score, applies the gate-status rules, and runs its own structure tests (pairwise S-tests, incremental I-tests, H_Structure: CONFIRMED / PARTIAL / UNDETERMINED / FALSIFIED). No model call, no spend.

## Files

| File | What it is |
|---|---|
| `prereg/PRE_REGISTRATION_aias_6_0_preview.md` | the pre-registration (analysis plan), r0 |
| `prereg/precision_aias_6_0_preview.json` | synthetic operating characteristics of the I-test (seed 600900); no program data |
| `scoping/precision_aias_6_0_preview.py` | the script that wrote it |
| `scripts/score_aias_6_0_preview.py` | scorer skeleton: statistics, verdict rules, wording class, synthetic dry run |
| `scripts/tests/test_score_aias_6_0_preview.py` | synthetic-data tests |
| `anchor/DEVIATIONS.md` | Entry 0 (ex ante) |
| `PLAIN_SUMMARY_aias_6_0_preview_r0.md` | plain-language summary and choices for Pablo (not deposited) |

## Run the tests (outputs go to a temporary directory)

```
python3 -I osf/aias_6_0_preview/scripts/tests/test_score_aias_6_0_preview.py
python3 -I osf/aias_6_0_preview/scripts/score_aias_6_0_preview.py --dry-run --out /tmp/aias6_dry
```

## Deposit plan (each deposit is a gate)

- `prereg/`, `scoping/`, `anchor/` — at the lock, before any t4-based component score exists (pre-registration §11.1).
- `outputs/` — at the data lock (tag `aias-6-0-preview-data-locked`).
