# v0.63 DEVIATIONS

## Entry 0 (ex ante, 2026-11-11)

1. **Number and base.** v0.63 is the next free number in Phase P (v0.62 taken by the non-English wave). Branch `v0.63` from `v1.14` @ `ceb706d`, a strict superset of `v1.10` @ `bad8c41`.
2. **What was read before the lock.** The five omnibus registries (to write `registries/panel_rules_v0_63.json`), and the archived answers through the certified loader for the pre-lock parity only (`prereg/parity_v0_63.json`): per-brand C_P and recall at t1–t3 compared with the published three-wave table, the published t1 per-brand values, the published t1 verdicts and the v1.6 Increment 1 table. No alternative-panel verdict, regime or §6 statistic was computed on the archive. Synthetic data only for the tests and the power check.
3. **Conflict of interest carried forward.** The handling of the v0.19 and v0.22 registries is carried from their source records as quoted in the pre-registration's Declarations (copied from `osf/methodology/v1_14/prereg/PRE_REGISTRATION_v1_14.md`, tag `v1.14-prereg-r2`), including the November 10, 2026 Denon correction. Denon stays in the canonical panel; rule R2 and sensitivity S1 remove it. No brand selection is made in this study.
4. **Anchor sequence.** Content lock → manifest → commit → tag `v0.63-prereg-r1` → push → OSF deposit → anchor file → `--run` once (`LOCK_STEPS.md`).
