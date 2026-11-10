# osf/aias_6_0_preview — AIAS™ 6.0 Preview (staging for osf.io/ec6wh/aias_6_0_preview/)

**Status (2026-11-10): pre-registration r1, lock candidate, not locked.** Branch `aias-6.0-preview` (from `4643d56`, the v1.14 anchor commit). r0 was deposited as a draft (`aias_6_0_preview/prereg/draft_r0/`). No t4 answer exists; nothing here reads one. The lock follows the locks of v0.42, v1.12 and v1.13 (Wed 2026-11-11): `LOCK_STEPS.md`.

The Preview is the provisional six-part synthesis (Presence, Consistency, Ranking, Sentiment, Coverage, Grounding) on the newest models (t4 week). It reads each component's locked unit-level score, applies the gate-status rules, and runs its own structure tests (pairwise S-tests, incremental I-tests, H_Structure: CONFIRMED / PARTIAL / UNDETERMINED / FALSIFIED). No model call, no spend.

## Files

| File | What it is |
|---|---|
| `prereg/PRE_REGISTRATION_aias_6_0_preview.md` | the pre-registration (analysis plan), r1 |
| `prereg/precision_aias_6_0_preview.json` | synthetic operating characteristics of the I-test (seed 600900); no program data |
| `scoping/precision_aias_6_0_preview.py` | the script that wrote it |
| `scripts/score_aias_6_0_preview.py` | the scorer: pinned inputs (`INPUTS`, the one configuration block), hashed readers, MQ checks, structure tests, verdicts, descriptives D1–D9, sensitivities SA–SH, `--run`, lock tooling |
| `scripts/tests/test_score_aias_6_0_preview.py` | synthetic-data tests (scratch git repositories and temporary directories only) |
| `anchor/DEVIATIONS.md` | Entry 0 (ex ante) and clarifications C1–C2 (ex ante, r1) |
| `LOCK_STEPS.md` | the coordinator's lock commands, in order (lock helper; not locked) |
| `lock/osf_verify_aias_6_0_preview.py` | SHA-256 check of an OSF deposit against local files (lock helper; not locked) |
| `PLAIN_SUMMARY_aias_6_0_preview_r0.md` | plain-language summary and choices for Pablo (not deposited) |

Written at the lock: `prereg/LOCK_MANIFEST_aias_6_0_preview.sha256` (`--lock-manifest`) and `anchor/git_anchor_aias_6_0_preview.json` (`--write-anchor`). Written once at the data lock (`--run`): `outputs/` (inputs read with their hashes, gate states, results, the per-unit profile table).

## Run the tests (outputs go to temporary directories)

```
python3 -I osf/aias_6_0_preview/scripts/tests/test_score_aias_6_0_preview.py
python3 -I osf/aias_6_0_preview/scripts/score_aias_6_0_preview.py --dry-run --out /tmp/aias6_dry
python3 -I osf/aias_6_0_preview/scripts/score_aias_6_0_preview.py --pin-report
```

## Deposit plan (each deposit is a gate)

- `prereg/`, `scoping/`, `anchor/` — at the lock, before any t4-based component score exists (pre-registration §11.1).
- `outputs/` — at the data lock (tag `aias-6-0-preview-data-locked`).
