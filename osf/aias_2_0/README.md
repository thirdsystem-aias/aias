# osf/aias_2_0 — AIAS™ 2.0 synthesis (staging for osf.io/ec6wh/aias_2_0/)

**Status (Nov 9, 2026): pre-t₃ results.** Outline r1 committed on branch `aias-2.0` and tagged
locally `aias-2-0-outline-locked` (13:27:44 UTC, before the first t₃ call). GitHub push is
unavailable, so the anchor is an OSF deposit of `prereg/` and `anchor/` (see
`anchor/DEVIATIONS.md`, Entry 1); the deposit waits for Pablo's go.

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

- **Now, on Pablo's go:** `prereg/` (byte-identical copy of the locked outline) and `anchor/`
  (`DEVIATIONS.md`, `git_anchor_aias_2_0_outline.json`), on the Mac:
  `zsh -ic 'cd ~/aias && python3 scripts/osf_upload.py <tree>/osf/aias_2_0/prereg aias_2_0/prereg && python3 scripts/osf_upload.py <tree>/osf/aias_2_0/anchor aias_2_0/anchor'`
  (`<tree>` = a checkout of branch `aias-2.0`), then confirm each file's SHA-256 on OSF equals
  the one in `git_anchor_aias_2_0_outline.json`. Claim "deposited" only after that check.
- `scoring/` ← `aias_2_0_synthesis_data.json`, `aias_2_0_profiles.csv`, `inputs/` (at the data lock)
- `figures/`, `paper/`, `report/` ← later locks
