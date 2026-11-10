# AIAS v1.14 — Ranking, redesigned measure (modal position), confirmed blind on t4 and t5

Status: pre-registration **r1 draft** (2026-11-10), not yet locked. Methodology lock with no collection of its own and no model call.

- `prereg/PRE_REGISTRATION_v1_14.md`: selection history, the statistic, calibration, Stage 1 (t4 separability), Stage 2 (t4 → t5 retest), precision note, gate, order of operations, Declarations.
- `prereg/LOCK_MANIFEST_v1_14.sha256`: SHA-256 of every locked file (`python3 scripts/score_v1_14.py --lock-manifest`; check with `--verify-lock`).
- `calibration/calibration_v1_14.json` and `calibration_run_v1_14.log`: the archived waves (calibration only), from v1.10's hashed rank tables; reproduces v1.10's sensitivity check S3 for MODE exactly (`python3 scripts/score_v1_14.py --calibration`).
- `anchor/DEVIATIONS.md`: Entry 0 (ex ante). `anchor/git_anchor_v1_14.json` is written after the tag is pushed.
- Scorer `scripts/score_v1_14.py` (imports `scripts/score_v1_10.py` unchanged); tests `scripts/test_score_v1_14.py` (`python3 -m unittest scripts/test_score_v1_14.py`).
- `outputs/stage1/`, `outputs/stage2/`: written once each, after the lock (the scorer refuses earlier).
