# v1.12 Coverage Paper A — lock steps (Wednesday 2026-11-11)

Prepared 2026-11-10 by the runner (lane 8). Everything below runs in the worktree `/Users/pablou/aias/_worktrees/v1.12` (branch `v1.12`). Never checkout, switch or commit in `/Users/pablou/aias` itself (branch `v0.40`, another job). No paid call, no data, no `--collect` at the lock. Each shell call is `zsh -ic '...'` (≤ 55 s).

State prepared on 2026-11-10: §12 clarifications (i)–(y) logged; N1 re-run with the current scorer (PASS, statistics identical, record names scorer SHA-256 `7fd288bf…`); evening update §12 (z) (v1.14 re-locked as r2: H5 names `v1.14-prereg-r2` → `a5feb4b1`; N1 re-run again, PASS, statistics identical, record names scorer SHA-256 `f7689898…`; manifest rebuilt); MC_BrandFree written to `anchor/mc_brandfree_v1_12.json` (0 hits); `anchor/DEVIATIONS.md` created; `prereg/LOCK_MANIFEST_v1_12.sha256` built (38 files, paths from the repository root); 118 tests pass. If any manifested file changes before the tag, redo steps 1–2 (and rebuild the manifest with the command in step 1b).

## 0. Preconditions (stop if any fails)

1. **Time:** now ≥ **2026-11-11 21:00 UTC** (3 pm CST). `date -u`
2. **Pablo:** he has not held the lock or asked for changes since the 3 pm CT Nov 10 text. If he typed `coverage one flagship` (drop Claude Opus 5.5), that changes the panel and design (C3, H8, A4, 900 → 675 calls): it restarts the 24 hours — do not lock; report.
3. **Worktree clean and on v1.12:**
   ```
   cd /Users/pablou/aias/_worktrees/v1.12 && git branch --show-current && git status --short --untracked-files=no && git log --oneline -3
   ```
   Expect `v1.12`, no tracked changes, HEAD = the lane-8 lock-prep commit (or a later commit made for the lock). `osf/methodology/v1_12/_osf_stage_draft/` is untracked (an earlier draft staging copy, with a stale $120 dry run): leave it, never upload it.
4. **Remote tags (read-only):**
   ```
   cd /Users/pablou/aias/_worktrees/v1.12 && git ls-remote --tags origin v1.12-prereg-r1 v1.14-prereg-r2 v0.42-prereg-r1 v1.11-prereg-r1
   ```
   Expect: no `v1.12-prereg-r1`; `v1.14-prereg-r2` present with peeled commit `a5feb4b1c4b9e9d19979129afcfd616a50b88c64` (H5 active, gating only if v1.14's Stage 1 is SEPARABLE; §12 (z): r2 superseded `v1.14-prereg-r1` → `20fbc342`). If `v1.14-prereg-r2` is absent or peels to another commit: stop and report (v1.14's `LOCK_STEPS_r2.md` must run first). `v0.42-prereg-r1` may or may not exist yet; either is fine (the coder is re-checked before coding).
5. **H6 stays inactive:** list all remote tags and compare with the 2026-11-10 baseline below. If a new tag pre-registers a **Sentiment score on the t4 answers**, H6's activation must be recorded before the lock (§3): stop and report; do not lock.
   ```
   cd /Users/pablou/aias/_worktrees/v1.12 && git ls-remote --tags origin | grep -v "\^{}" | sed "s#.*refs/tags/##" | grep -E "^v(0\.4|1\.)"
   ```
   Baseline (2026-11-10, ~2:50 pm CT): `v0.41-acquisition-locked v0.41-prereg-r1 v0.41-scoring-locked v1.10-prereg-r1 v1.10-prereg-r2 v1.11-prereg-r1 v1.14-prereg-r1` (plus older v1.3–v1.9 tags); `v1.14-prereg-r2` (the v1.14 re-lock, §12 (z)) is expected new. A new `v0.42-prereg-r1` is expected and does not affect H6.

## 1. Verify the lock text (no writes)

a. Manifest:
   ```
   cd /Users/pablou/aias/_worktrees/v1.12 && shasum -a 256 -c osf/methodology/v1_12/prereg/LOCK_MANIFEST_v1_12.sha256 | grep -vc ": OK$"; wc -l < osf/methodology/v1_12/prereg/LOCK_MANIFEST_v1_12.sha256
   ```
   Expect `0` failures and `38` lines. Spot values (after §12 (z), 2026-11-10 evening): prereg `d5d14083…`, `score_v1_12.py` `f7689898…`, `calibration_N1_v1_12.json` `aa4f0b5f…`, `code_t4_v0_42.py` `d0e4e685…`.

b. (Only if a manifested file changed) rebuild, then re-check with a.:
   ```
   cd /Users/pablou/aias/_worktrees/v1.12 && shasum -a 256 $(sed "s/^[0-9a-f]*  //" osf/methodology/v1_12/prereg/LOCK_MANIFEST_v1_12.sha256) > /tmp/v112_m && mv /tmp/v112_m osf/methodology/v1_12/prereg/LOCK_MANIFEST_v1_12.sha256
   ```
   If `score_v1_12.py` changed, N1 must be re-run first (`python3 osf/methodology/v1_12/scripts/score_v1_12.py --calibrate-n1`, ~45 s, must print PASS) and logged in §12.

c. Tests (~35 s, fits one call):
   ```
   cd /Users/pablou/aias/_worktrees/v1.12 && PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s osf/methodology/v1_12/scripts/tests -p "test_*.py" > /tmp/v112_tests.log 2>&1; tail -3 /tmp/v112_tests.log
   ```
   Expect `Ran 118 tests` and `OK`.

d. Records agree with the files:
   ```
   cd /Users/pablou/aias/_worktrees/v1.12 && PYTHONDONTWRITEBYTECODE=1 python3 osf/methodology/v1_12/lock/check_records_v1_12.py; echo EXIT $?
   ```
   Expect seven `OK` lines (N1 PASS and naming the current scorer; MC_BrandFree 0 hits on the current probes with the coder pin matching; coder blob `2d36735d`; 0 manifest mismatches) and `EXIT 0`.

## 2. Tag (local)

```
cd /Users/pablou/aias/_worktrees/v1.12 && git tag -a v1.12-prereg-r1 -m "AIAS v1.12 Coverage Paper A: pre-registration r1 locked (prereg/LOCK_MANIFEST_v1_12.sha256, 38 files)" HEAD && git rev-parse v1.12-prereg-r1 v1.12-prereg-r1^{commit}
```
Record the tag object and the commit.

## 3. Push branch and tag

```
cd /Users/pablou/aias/_worktrees/v1.12 && git push origin v1.12 && git push origin refs/tags/v1.12-prereg-r1 && git ls-remote --tags origin v1.12-prereg-r1
```
Expect two lines (tag object, and `^{}` = the commit of step 2).

## 4. Anchor file (names the tag's commit; `acquire_v1_12.py --collect` refuses without it)

If step 0.4 showed `v0.42-prereg-r1` on origin, first fetch it so the anchor records the coder's blob at that tag (it must be `2d36735d…`; if not, stop and report before writing the anchor): `cd /Users/pablou/aias/_worktrees/v1.12 && git fetch origin refs/tags/v0.42-prereg-r1:refs/tags/v0.42-prereg-r1 && git rev-parse v0.42-prereg-r1:osf/v42/scripts/code_t4_v0_42.py`. (Tested 2026-11-10 with `--dry-run --ref HEAD`: 39 files with blobs, H5/H6/coder blocks as described; without the tag on origin it refuses.)

```
cd /Users/pablou/aias/_worktrees/v1.12 && PYTHONDONTWRITEBYTECODE=1 python3 osf/methodology/v1_12/lock/write_anchor_v1_12.py
```
Writes `osf/methodology/v1_12/anchor/osf_anchor_v1_12.json`: tag, tag object, commit, tree, remote ref, the 38 locked files plus the manifest (SHA-256 and git blob at the tag), H5 (v1.14-prereg-r2 → `a5feb4b1`, score-defining files and their blobs, gates only if Stage 1 is SEPARABLE), H6 INACTIVE, the coder pin (and its blob at `v0.42-prereg-r1` if that tag exists locally), MC_BrandFree hits. It refuses if the tag is not on origin, a file differs from the manifest, or v1.14's tag moved. Then commit and push the anchor (the tag does not move):
```
cd /Users/pablou/aias/_worktrees/v1.12 && git add osf/methodology/v1_12/anchor/osf_anchor_v1_12.json && git commit -m "v1.12 anchor: osf_anchor_v1_12.json names v1.12-prereg-r1 (after the lock)" && git push origin v1.12
```
(Add the session's attribution lines to the commit message as instructed in that session.)

## 5. OSF deposit (project ec6wh, osfstorage)

`methodology/v1_12/` already holds `draft_r1/` (the draft of Nov 10); leave it. Upload only `prereg/` and `anchor/`:
```
cd /Users/pablou/aias/_worktrees/v1.12 && git status --short osf/methodology/v1_12/prereg osf/methodology/v1_12/anchor && ls osf/methodology/v1_12/prereg osf/methodology/v1_12/anchor
```
Expect no output from `git status` and exactly: prereg = 8 files + `LOCK_MANIFEST_v1_12.sha256`; anchor = `DEVIATIONS.md`, `mc_brandfree_v1_12.json`, `osf_anchor_v1_12.json`. Then (dry run first, then upload; `OSF_TOKEN` is set in the login shell):
```
cd /Users/pablou/aias/_worktrees/v1.12 && python3 scripts/osf_upload.py osf/methodology/v1_12/prereg methodology/v1_12/prereg --dry-run && python3 scripts/osf_upload.py osf/methodology/v1_12/anchor methodology/v1_12/anchor --dry-run
cd /Users/pablou/aias/_worktrees/v1.12 && python3 scripts/osf_upload.py osf/methodology/v1_12/prereg methodology/v1_12/prereg
cd /Users/pablou/aias/_worktrees/v1.12 && python3 scripts/osf_upload.py osf/methodology/v1_12/anchor methodology/v1_12/anchor
```

## 6. Verify the deposit by SHA-256 (read-only)

```
cd /Users/pablou/aias/_worktrees/v1.12 && PYTHONDONTWRITEBYTECODE=1 python3 osf/methodology/v1_12/lock/osf_verify_v1_12.py osf/methodology/v1_12/prereg methodology/v1_12/prereg && PYTHONDONTWRITEBYTECODE=1 python3 osf/methodology/v1_12/lock/osf_verify_v1_12.py osf/methodology/v1_12/anchor methodology/v1_12/anchor
```
Expect `9 of 9 local files match; 0 extra on OSF -> PASS` and `3 of 3 … PASS`. (The verifier was checked on 2026-11-10 against the existing `methodology/v1_14/prereg` deposit: 2 of 2, PASS.) On a mismatch: re-upload that folder and verify again; never edit a locked file to make it match.

## 7. After the lock (not part of the lock)

- Report: tag object, commit, anchor commit, the two OSF verifications.
- **Do not collect.** `acquire_v1_12.py --collect` refuses until (i) the tag is on origin and the anchor names its commit, (ii) `anchor/t4_complete_v1_12.json` records t4's raw file, its SHA-256 and its last call (written by the run that confirms t4 finished; not at the lock), (iii) no other `acquire_v*.py --collect` runs, and (iv) the clock is inside 2026-11-14 00:00–11-16 23:59:59 UTC or 11-22 12:00–11-29 23:59:59 UTC (checked again before every request). Budget: expected $26.38, hard cap $100, pause at $80.
- Before any v1.12 answer is coded: the vendored coder's blob must equal `git rev-parse v0.42-prereg-r1:osf/v42/scripts/code_t4_v0_42.py` (else log in `anchor/DEVIATIONS.md` first), and P1 must pass.
