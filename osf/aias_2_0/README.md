# osf/aias_2_0 — AIAS™ 2.0 synthesis (staging for osf.io/ec6wh/aias_2_0/)

**Status (Nov 10, 2026): data locked (local tag `aias-2-0-data-locked`).** The outline r1 (commit `f97db70`, 13:27:44 UTC Nov 9, before the first t₃ call) was deposited on OSF on Nov 9 at 15:11–15:12 UTC (`aias_2_0/prereg/`, `aias_2_0/anchor/`; SHA-256 match the locked files), before any t₃ score existed. After merging v0.41 and v1.9 (whose prereg tags are on GitHub and resolve to the OSF-anchored hashes), the builder's status is `complete` and the outline §5 outcome class is **A** with no rule flags: Consistency stays separable from Presence at t₃ (ρ(C\*, P) = 0.190, n = 54) and keeps its brand order over about five months beyond frame structure (ρ = 0.647, n = 52, p_frame = 0.008); the Presence score keeps its order (ρ = 0.954, n = 112).

## Files

| File | What it is |
|---|---|
| `aias_2_0_synthesis_data.json` | output of `scripts/aias_2_0_synthesis_data.py`; `status: pre-t3` until the v0.41 and v1.9 Stage 2 verdicts exist and both prereg tags are on origin. Rebuilt, then tagged `aias-2-0-data-locked`, at the data lock. |
| `aias_2_0_profiles.csv` | per-brand P and C\* (C_phi rated at ≥ 6 total mentions) per wave (t₁, t₂, t₃) |
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

- `prereg/` and `anchor/` — deposited Nov 9, 15:11–15:12 UTC (Pablo's go), 3/3 SHA-256 verified.
- `scoring/` ← `aias_2_0_synthesis_data.json`, `aias_2_0_profiles.csv`, `inputs/` — ready now (data lock); waits for Pablo's go
- `figures/`, `paper/`, `report/` ← later locks
