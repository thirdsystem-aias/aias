# osf/aias_2_0 — AIAS™ 2.0 synthesis (staging for osf.io/ec6wh/aias_2_0/)

**Status (Nov 9, 2026): pre-t₃.** Outline r1 committed on branch `aias-2.0` and tagged locally
`aias-2-0-outline-locked`; its anchor (tag push + deposit of the outline to `aias_2_0/prereg/`)
waits for Pablo's go, together with the `v0.41-prereg-r1` / `v1.9-prereg-r1` push.

## Files

| File | What it is |
|---|---|
| `aias_2_0_synthesis_data.json` | output of `scripts/aias_2_0_synthesis_data.py`; `status: pre-t3` until the v0.41 and v1.9 Stage 2 verdicts exist and both prereg tags are on origin. Rebuilt, then tagged `aias-2-0-data-locked`, at the data lock. |
| `aias_2_0_profiles.csv` | per-brand P and C\* (C_phi rated at ≥ 6 total mentions) per wave; t₁ and t₂ now, t₃ after Stage 2 |
| `inputs/v36_verdicts.json` | frozen copy of `osf/v36/v36_verdicts.json` from branch `v0.36` (tip `cc36d7a`; file last changed in `053427d`), git blob `d790312`, SHA-256 `3c41f78a70f02df010c88d3611fb15deae10276bb217eb7a125ec90b90d2fb8b`; osf/v36 is not on the v0.37+ line |

## Rebuild and test

```
AIAS_ROOT=<tree> python3 scripts/aias_2_0_synthesis_data.py           # writes this folder
AIAS_ROOT=<tree> python3 scripts/test_aias_2_0_synthesis_data.py [--e2e SCRATCH]
python3 papers/aias_2_0/check_outline_numbers.py                         # outline numbers vs locked sources
```

The builder halts and writes nothing unless the v0.41 parity gates P1–P4 pass and its own
t₁/t₂ profiles reproduce the locked v1.9 Stage 1 values exactly (parity A1–A5).

## Deposit plan (each deposit is a gate)

- `prereg/` ← `papers/aias_2_0/aias_2_0_synthesis_outline.md` (at the outline anchor)
- `scoring/` ← `aias_2_0_synthesis_data.json`, `aias_2_0_profiles.csv`, `inputs/` (at the data lock)
- `figures/`, `paper/`, `report/` ← later locks
