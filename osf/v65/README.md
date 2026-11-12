# AIAS v0.65 — Cross-cultural identity load (study #55)

OSF staging for roadmap study #55 (Phase P). Pre-registered re-analysis of v0.62's Spanish, Korean and Chinese category answers against t₄'s English answers (v0.42). No collection, no model call, no spend. **Draft r0: not locked.**

- `prereg/PRE_REGISTRATION_v0_65_DRAFT_r0.md` — the pre-registration draft (plain-language summary and decisions for the pre-registrant at the top).
- `prereg/dry_run_v0_65_r0.txt` — scorer run end to end on five synthetic v0.62-shaped worlds.
- `prereg/power_v0_65_r0.json` — operating characteristics of H1 and H3 over 500 synthetic worlds per condition.
- `prereg/LOCK_MANIFEST_v0_65_DRAFT_r0.sha256` — draft manifest (SHA-256 of every file to be locked; rebuilt at the lock).
- `scripts/score_v0_65.py` — scorer skeleton (`--dry-run`, `--power`, `--lock-manifest PATH`, `--verify-lock PATH`, `--run`); `scripts/test_score_v0_65.py` — unit tests.
- `anchor/DEVIATIONS.md` — deviations log (Entry 0 ex ante).

Run from the worktree root: `python3 osf/v65/scripts/test_score_v0_65.py`; `python3 osf/v65/scripts/score_v0_65.py --dry-run`.
