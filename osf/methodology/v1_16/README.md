# AIAS v1.16 — Ranking, the last measure: co-mention precedence

Status: pre-registration **r1** (2026-11-12), to be locked at tag `v1.16-prereg-r1` and deposited on OSF (`methodology/v1_16`). Re-analysis of archived answers (t1, t2, t3 omnibus waves; t4); no collection, no model call, no spend. If the gate does not PASS, Ranking is reported as part of Presence and not as a separate AIAS component, and there is no further Ranking redesign (pre-registration §8; Pablo, Nov 11, 2026, 11:22 pm).

- `prereg/PRE_REGISTRATION_v1_16.md`: diagnosis of v1.10 and v1.14, the measure (PREC, a Bradley–Terry strength from the order of brands named together), literature, inputs, hypotheses H1–H5, precision, gate and consequence clause, checks, exploratory moderators, sensitivities, dry run, Declarations.
- `prereg/LOCK_MANIFEST_v1_16.sha256`: SHA-256 of every locked file (`python3 scripts/score_v1_16.py --lock-manifest`; check with `--verify-lock`).
- `prereg/input_parity_v1_16.json`: input parity before the lock (counts and n's only; `--parity`).
- `prereg/precision_note_v1_16.json` (from `scripts/precision_note_v1_16.py`): analytic power of the verdict rules.
- `dryrun/dryrun_v1_16.json` and `dryrun_run_v1_16.log`: the full pipeline on synthetic data with known answers (`--dry-run`).
- `anchor/DEVIATIONS.md`: Entry 0 (ex ante). `anchor/git_anchor_v1_16.json` is written after the tag is pushed and the OSF deposit is verified (`--write-anchor --osf-note "<OSF location>"`).
- Scorer `scripts/score_v1_16.py` (imports `scripts/score_v1_10.py` and `scripts/score_v1_14.py` unchanged); tests `scripts/test_score_v1_16.py` (`python3 -m unittest scripts/test_score_v1_16.py`).
- `outputs/results_v1_16.json`: written once by `--run`, after the lock (the scorer refuses earlier).
