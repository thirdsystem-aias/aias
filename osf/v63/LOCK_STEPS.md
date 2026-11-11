# v0.63 lock steps (for the coordinator)

Re-analysis: it locks as soon as the coordinator has checked it. Run from the worktree `~/aias/_worktrees/v0.63` (branch `v0.63`). `S=osf/v63/scripts/score_v0_63.py`.

Before the lock (already done on 2026-11-11 by the drafting lane; repeat to confirm):

1. `python3 $S --rules` — rule applications from the registries only (`registries/panel_rules_v0_63.json`).
2. `python3 $S --parity` — must print `parity passed=True` (writes `prereg/parity_v0_63.json`).
3. `python3 $S --power` — synthetic only (`prereg/power_v0_63.json`).
4. `python3 osf/v63/scripts/test_score_v0_63.py` — all tests pass.
5. Check that nothing exists in `osf/v63/outputs/` (no statistic has been computed on the archive).

Lock:

6. Content lock: no further edit to any file listed in the manifest. `python3 $S --lock-manifest`, then `python3 $S --verify-lock` → `lock manifest OK`.
7. `git add osf/v63 && git commit` (message: "v0.63 prereg r1 content lock").
8. `git tag -a v0.63-prereg-r1 -m "v0.63 pre-registration r1"`.
9. `git push origin v0.63 && git push origin v0.63-prereg-r1`.
10. OSF deposit: `python3 scripts/osf_upload.py osf/v63/prereg v63/prereg`, the same for `osf/v63/registries`, `osf/v63/scripts`, `osf/v63/anchor` (DEVIATIONS), `LOCK_STEPS.md` and `README.md` (to `v63`); verify the SHA-256 of each deposited file against `prereg/LOCK_MANIFEST_v0_63.sha256`.
11. `python3 $S --write-anchor --osf-note "osf.io/ec6wh/v63/ deposited <UTC time>"` → `anchor/git_anchor_v0_63.json`; commit it ("v0.63: git anchor") and push; deposit it to `v63/anchor`.

Scoring (once):

12. `python3 $S --run` → `osf/v63/outputs/v0_63_verdicts.json` and `v0_63_comparisons.csv`. It refuses without the tag, the anchor, a verifying manifest and a passing parity file, and refuses a second time once outputs exist. A HALT (MC1–MC4) is a DEVIATIONS entry, not a retry.

Note: the anchor commit changes no locked file, so `--verify-lock` still passes after step 11.
