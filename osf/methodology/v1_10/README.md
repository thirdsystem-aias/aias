# AIAS v1.10 — Ranking, Paper A (instrument, cross-category baseline, separability gate)

Methodology lock and re-analysis of archived answers. No new data collection, no model calls. Status: pre-registration **r1** (2026-11-10), locked at tag `v1.10-prereg-r1` and deposited on OSF.

- `prereg/PRE_REGISTRATION_v1_10.md`: the pre-registration (inputs, extraction rules, candidates, selection rule, hypotheses H1–H6, gate, checks, decisions settled before the lock).
- `prereg/feasibility_v1_10.md`: declared parsing feasibility on the development sample (v0.17 and v0.18 phase B; excluded from every confirmatory analysis).
- `prereg/parity_v1_10.json`: pre-lock MQ1 parse completion, MQ2 mention parity and the OMNI unit join (key columns only); no rank position or rank statistic computed (`score_v1_10.py --parity`).
- `scoping/feasibility_v1_10.py` and `.json`: the script behind the feasibility note, and its output.
- `registries/INPUTS_MANIFEST_v1_10.json` (built by `build_inputs_manifest_v1_10.py` from the scorer's own set table): 111 frozen files, each with its git blob and SHA-256. Held studies v0.38 / v0.39 excluded.
- `registries/REGISTRY_CHOICES_v1_10.md`: which registry each set loads, with the code and git-history evidence, and the open points.
- `registries/v0_23_registry_v1_10.json` and `registries/v06_prompts/`: the v0.23 inline registry and the v0.6 prompt files, written by `build_registry_inputs_v1_10.py`.
- `dryrun/build_dryrun_v1_10.py`: synthetic replicas of every input format (`dryrun/replica/`, manifest `dryrun/INPUTS_MANIFEST_dryrun_v1_10.json`); `dryrun/outputs/` holds the dry-run outputs (synthetic, meaningless numbers).
- `anchor/DEVIATIONS.md`: Entry 0 (ex ante). `anchor/coi_flags_v1_10.json` (S7, not a frozen input) is written later by the runner.
- Scorer: `scripts/score_v1_10.py` (`--verify-manifest`, `--parity`, `--stage S`, `--stage C`, `--dry-run`; refuses `--stage` on real data until the tag `v1.10-prereg-r1` and `anchor/git_anchor_v1_10.json` exist). Tests: `scripts/test_score_v1_10.py` (synthetic data only).

Lock sequence: settle the open questions (§15) → content lock → commit → tag `v1.10-prereg-r1` → OSF deposit → verify both anchors → Stage S → Stage C.
