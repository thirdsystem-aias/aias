# v1.13 Grounding Paper A — lock steps (Wednesday 2026-11-11)

Prepared 2026-11-10 by the runner (lane 10). Everything below runs in the worktree `/Users/pablou/aias/_worktrees/v1.13` (branch `v1.13`). Never checkout, switch or commit in `/Users/pablou/aias` itself (branch `v0.40`, another job). No paid call, no data, no web fetch, no `--stage C1`, no `--collect` at the lock. Each shell call is `zsh -ic '...'` (≤ 55 s); the commands below use only double quotes so they fit inside it.

**Order on Wednesday:** v1.12 (its own `LOCK_STEPS.md`) → **v1.13 (this file)** → v0.42 (t4), whose collection starts right after its lock. Do not start v1.13 until v1.12's tag is on origin; do not let v0.42 tag before v1.13's step 4 is done.

State prepared on 2026-11-10: §12 (j)–(w) logged (SCORER_NOTES N1–N7, N10–N12, N14; AUDIT_NOTES A1–A6; v0.42 scorer pin refreshed to blob `3bbe58db…` at `17dd6f5`; lock records); §12 (x) by lane 13 (H6's Cov\* reader, `--h6-cov`, N21; `write_anchor_v1_13.py` records v1.12's scorer SHA-256 at its tag); §12 (y) on Nov 10 evening (H4 names `v1.14-prereg-r2` → `a5feb4b1`, the v1.14 re-lock; manifest rebuilt); `anchor/DEVIATIONS.md` with Entry 0; `prereg/LOCK_MANIFEST_v1_13.sha256` rebuilt (21 files, both parts, paths from the repository root); 90 tests pass; dry run reproduced; `lock/` helpers (check_records, check_guards, write_anchor, osf_verify). If any manifested file changes before the tag, redo step 1 (rebuild with 1b).

## 0. Preconditions (stop if any fails)

1. **Time:** now ≥ **2026-11-11 21:00 UTC** (3 pm CST). `date -u`
2. **Pablo:** he has not typed `hold grounding` and has not asked for changes since the 3 pm CT Nov 10 text. Any change other than a §12-type clarification restarts the 24 hours: do not lock; report.
3. **Worktree clean and on v1.13:**
   ```
   cd /Users/pablou/aias/_worktrees/v1.13 && git branch --show-current && git status --short --untracked-files=no && git log --oneline -3
   ```
   Expect `v1.13`, no tracked changes, HEAD = the v1.14-r2 reference commit (§12 (y), Nov 10 evening) on top of the lane-13 commit (H6 reader, §12 (x)) and the lane-10 lock-prep commit `9a003b6`. `osf/methodology/v1_13/_osf_stage_draft/` and `_osf_stage_draft_r1/` are untracked earlier staging copies: leave them, never upload them.
4. **Remote tags (read-only):**
   ```
   cd /Users/pablou/aias/_worktrees/v1.13 && git ls-remote --tags origin v1.13-prereg-r1 v1.13-audit-r1 v1.12-prereg-r1 v1.14-prereg-r2 v0.42-prereg-r1
   ```
   Expect: no `v1.13-*`; `v1.14-prereg-r2` with peeled commit `a5feb4b1c4b9e9d19979129afcfd616a50b88c64` (H4 active, downgrading only if v1.14's Stage 1 is SEPARABLE; §12 (y): r2 superseded `v1.14-prereg-r1` → `20fbc342`; if `v1.14-prereg-r2` is absent or peels to another commit, stop and report); **`v1.12-prereg-r1` present** (pushed by the v1.12 lock minutes earlier; H6 activation, step 2); `v0.42-prereg-r1` absent (v0.42 locks after v1.13; its pins are re-checked in step 9).
5. **H5 stays inactive:** compare the tag list with the 2026-11-10 baseline. If a new tag pre-registers a **Sentiment score on the t4 answers**, H5's activation must be decided before the lock (§3, §12 (i)): stop and report.
   ```
   cd /Users/pablou/aias/_worktrees/v1.13 && git ls-remote --tags origin | grep -v "\^{}" | sed "s#.*refs/tags/##" | grep -E "^v(0\.4|1\.)"
   ```
   Baseline (2026-11-10, ~3:15 pm CT): `v0.41-acquisition-locked v0.41-prereg-r1 v0.41-scoring-locked v1.10-prereg-r1 v1.10-prereg-r2 v1.11-prereg-r1 v1.14-prereg-r1` (plus older v1.3–v1.9 tags). Expected new: `v1.14-prereg-r2` (the v1.14 re-lock, §12 (y)) and `v1.12-prereg-r1` only.
6. **v0.42 pins:** fetch v0.42 (read-only for this worktree), then step 1d checks the blobs.
   ```
   cd /Users/pablou/aias/_worktrees/v1.13 && git fetch origin v0.42 && git log --oneline -1 origin/v0.42 && git rev-parse "origin/v0.42:osf/v42/scripts/code_t4_v0_42.py" "origin/v0.42:osf/v42/scripts/score_v0_42.py"
   ```
   Expect `2d36735d…` (coder) and `3bbe58db…` (scorer; origin/v0.42 was `17dd6f5` on Nov 10). If the scorer blob differs, v0.42 changed again: stop and report. (A refresh needs the diff shown to touch none of `pi_N3_<c>`, `phi_N3_<c>`, `phi_partition_N3_<c>`, a §12 entry as (v), the pin in §0, `V042_PINS` and its test, `lock/write_anchor_v1_13.py`, and a rebuilt manifest, all before the tag.) If the coder blob differs: stop.

## 1. Verify the lock text (no writes)

a. Manifest:
   ```
   cd /Users/pablou/aias/_worktrees/v1.13 && shasum -a 256 -c osf/methodology/v1_13/prereg/LOCK_MANIFEST_v1_13.sha256 | grep -vc ": OK$"; wc -l < osf/methodology/v1_13/prereg/LOCK_MANIFEST_v1_13.sha256
   ```
   Expect `0` failures and `21` lines. Spot values (after §12 (y), 2026-11-10 evening): prereg `eb6dd7e6…`, `brand_domains_v1_13.csv` `38198fdf…`, `score_v1_13.py` `e2bf8542…`, `test_clarification_v1_13.py` `cd49b42e…`, `audit_v1_13.py` `37ed8830…`, `DEVIATIONS.md` `bc1e5509…`.

b. (Only if a manifested file changed) rebuild, then re-check with a.:
   ```
   cd /Users/pablou/aias/_worktrees/v1.13 && shasum -a 256 $(sed "s/^[0-9a-f]*  //" osf/methodology/v1_13/prereg/LOCK_MANIFEST_v1_13.sha256) > /tmp/v113_m && mv /tmp/v113_m osf/methodology/v1_13/prereg/LOCK_MANIFEST_v1_13.sha256
   ```
   If `audit_v1_13.py` or a fixture changed, re-run the dry run first (`python3 osf/methodology/v1_13/scripts/audit_v1_13.py --dry-run`, a few seconds, every check PASS) and log it in §12.

c. Tests (under 1 s):
   ```
   cd /Users/pablou/aias/_worktrees/v1.13 && PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s osf/methodology/v1_13/scripts/tests -p "test_*.py" > /tmp/v113_tests.log 2>&1; tail -3 /tmp/v113_tests.log
   ```
   Expect `Ran 90 tests` and `OK` (43 scorer, 19 clarification, 28 audit).

d. Records agree with the files:
   ```
   cd /Users/pablou/aias/_worktrees/v1.13 && PYTHONDONTWRITEBYTECODE=1 python3 osf/methodology/v1_13/lock/check_records_v1_13.py; echo EXIT $?
   ```
   Expect nine `OK` lines (0 manifest mismatches; 112 units, 0 UNRESOLVED; D_b SHA-256 = the §2.3 pin; coder and scorer pins = origin/v0.42; v1.14-prereg-r2 → `a5feb4b1` (FAIL until that tag exists locally: run v1.14's `LOCK_STEPS_r2.md` and `git fetch origin --tags` first); dry-run record names the current audit script and fixture manifest; activation constants) and `EXIT 0`.

e. Audit guard (simulated; no network, no write):
   ```
   cd /Users/pablou/aias/_worktrees/v1.13 && PYTHONDONTWRITEBYTECODE=1 python3 osf/methodology/v1_13/lock/check_guards_v1_13.py; echo EXIT $?
   ```
   Expect 16 `OK` lines and `EXIT 0`.

## 2. Lock commit (empty; fixes H6's activation order)

§3: a conditional leg is active if its tag "is pushed **before** the v1.13 lock commit". The lane-10 commit was made on Nov 10, before v1.12's tag, so the tag goes on a new empty commit made **after** step 0.4 showed `v1.12-prereg-r1` on origin. `write_anchor_v1_13.py` refuses if v1.12's tag is on origin but the tagged commit is older than it. (If the runner decides instead that H6 stays INACTIVE, log that decision in §12 before tagging, rebuild the manifest, skip this step, and pass `--h6-inactive "REASON"` to the Part I anchor command in step 5.)
```
cd /Users/pablou/aias/_worktrees/v1.13 && git commit --allow-empty -m "v1.13 lock commit (Nov 11): text as in LOCK_MANIFEST_v1_13.sha256 (21 files); v1.12-prereg-r1 on origin before this commit (H6 activation, section 3)" && git log --oneline -2
```
(Add the session's attribution lines to the message as instructed in that session.)

## 3. Tags (local, on the lock commit)

Part I:
```
cd /Users/pablou/aias/_worktrees/v1.13 && git tag -a v1.13-prereg-r1 -m "AIAS v1.13 Grounding Paper A, Part I: pre-registration r1 locked (prereg/LOCK_MANIFEST_v1_13.sha256, 21 files)" HEAD && git rev-parse v1.13-prereg-r1 "v1.13-prereg-r1^{commit}"
```
Part II (same commit; the audit's `--collect` refuses without this tag, protocol §8; §0 and §12 give Part II its own tag and anchor). **Only if the coordinator confirms Part II locks on Wednesday too**; otherwise skip 3b, the `--audit` anchor and the receipt, and report that the audit cannot start:
```
cd /Users/pablou/aias/_worktrees/v1.13 && git tag -a v1.13-audit-r1 -m "AIAS v1.13 Grounding Paper A, Part II: structured-data audit protocol r1 locked (same commit and manifest as v1.13-prereg-r1)" HEAD && git rev-parse v1.13-audit-r1 "v1.13-audit-r1^{commit}"
```
Record the tag objects and the commit.

## 4. Push branch and tags

```
cd /Users/pablou/aias/_worktrees/v1.13 && git push origin v1.13 && git push origin refs/tags/v1.13-prereg-r1 refs/tags/v1.13-audit-r1 && git ls-remote --tags origin "v1.13-*"
```
Expect two lines per tag (tag object, and `^{}` = the lock commit); without Part II, drop `refs/tags/v1.13-audit-r1` from the push. Then v0.42 may lock.

## 5. Anchors

Part I (`score_v1_13.py --stage C1` refuses without it; MQ7 reads its `locked_files`; `conditional_legs` sets H4–H6):
```
cd /Users/pablou/aias/_worktrees/v1.13 && PYTHONDONTWRITEBYTECODE=1 python3 osf/methodology/v1_13/lock/write_anchor_v1_13.py
```
Writes `anchor/git_anchor_v1_13.json`: tag, tag object, commit, tree, the 21 files plus the manifest (SHA-256 and git blob at the tag), H4 ACTIVE (v1.14-prereg-r2 → `a5feb4b1`, its score files' blobs), H5 INACTIVE, H6 ACTIVE (v1.12's tag, commit, tagger date before the lock commit, its prereg and scorer blobs, the scorer's SHA-256 at the tag, which `--h6-cov` checks), the v0.42 pins (tag absent at this lock: re-checked in step 9 and by MQ7), `t4_raw_sha256` null (recorded before the first read). It refuses if the tag is not on origin, a file differs from the manifest, v1.14's tag moved, or the H6 order fails.

Part II (if 3b was done; `--collect` reads `commit` and `brand_domains_sha256`):
```
cd /Users/pablou/aias/_worktrees/v1.13 && PYTHONDONTWRITEBYTECODE=1 python3 osf/methodology/v1_13/lock/write_anchor_v1_13.py --audit
```
Test before (any time, no write): add `--dry-run --ref HEAD` to either command. Then commit and push the anchors (the tags do not move; without Part II, leave `audit_anchor_v1_13.json` out of `git add`):
```
cd /Users/pablou/aias/_worktrees/v1.13 && git add osf/methodology/v1_13/anchor/git_anchor_v1_13.json osf/methodology/v1_13/anchor/audit_anchor_v1_13.json && git commit -m "v1.13 anchors: git_anchor and audit_anchor name the lock commit (after the lock)" && git push origin v1.13
```

## 6. OSF deposit (project ec6wh, osfstorage)

`methodology/v1_13/` holds only `draft_r1/` (checked 2026-11-10); leave it. Upload `prereg/`, `registries/` and `anchor/` (§0 names all three):
```
cd /Users/pablou/aias/_worktrees/v1.13 && git status --short osf/methodology/v1_13/prereg osf/methodology/v1_13/registries osf/methodology/v1_13/anchor && ls osf/methodology/v1_13/prereg osf/methodology/v1_13/registries osf/methodology/v1_13/anchor
```
Expect no `git status` output and exactly: prereg = 4 files + `LOCK_MANIFEST_v1_13.sha256`; registries = 2; anchor = `DEVIATIONS.md`, `git_anchor_v1_13.json` (+ `audit_anchor_v1_13.json`). Then (dry run first; `OSF_TOKEN` is set in the login shell):
```
cd /Users/pablou/aias/_worktrees/v1.13 && for d in prereg registries anchor; do python3 scripts/osf_upload.py osf/methodology/v1_13/$d methodology/v1_13/$d --dry-run; done
cd /Users/pablou/aias/_worktrees/v1.13 && python3 scripts/osf_upload.py osf/methodology/v1_13/prereg methodology/v1_13/prereg
cd /Users/pablou/aias/_worktrees/v1.13 && python3 scripts/osf_upload.py osf/methodology/v1_13/registries methodology/v1_13/registries
cd /Users/pablou/aias/_worktrees/v1.13 && python3 scripts/osf_upload.py osf/methodology/v1_13/anchor methodology/v1_13/anchor
```

## 7. Verify the deposit by SHA-256 (read-only)

```
cd /Users/pablou/aias/_worktrees/v1.13 && for d in prereg registries anchor; do PYTHONDONTWRITEBYTECODE=1 python3 osf/methodology/v1_13/lock/osf_verify_v1_13.py osf/methodology/v1_13/$d methodology/v1_13/$d; done
```
Expect `5 of 5 … PASS`, `2 of 2 … PASS`, `3 of 3 … PASS` (2 of 2 without Part II). On a mismatch: re-upload that folder and verify again; never edit a locked file to make it match.

## 8. Send the locked text; Part II receipt

Send Pablo the locked text (tag, commit, OSF links). The time he receives it starts Part II's 24 hours. Record it (ISO 8601 **with** a UTC offset; the helper refuses a time without one, because the audit guard would crash on it):
```
cd /Users/pablou/aias/_worktrees/v1.13 && PYTHONDONTWRITEBYTECODE=1 python3 osf/methodology/v1_13/lock/write_anchor_v1_13.py --receipt 2026-11-11T22:05:00+00:00
```
(replace the time with the real one), then commit and push it, upload `anchor/` again and verify (`4 of 4 … PASS`), as in steps 5–7.

## 9. After the lock (not part of the lock)

- Report: tag objects, lock commit, anchor commit(s), the OSF verifications, the receipt time.
- **v0.42 pins:** after v0.42 tags, `git fetch origin refs/tags/v0.42-prereg-r1:refs/tags/v0.42-prereg-r1` and run step 1d again: it adds two lines comparing the pins with the blobs at the tag. A difference is logged in `anchor/DEVIATIONS.md` before Stage C1 (§0); MQ7 halts Stage C1 on it.
- **Stage C1** only after t4 is complete and its raw file's SHA-256 is recorded; H4 waits for v1.14's Stage 1 output (PENDING at C1); H6 waits for v1.12's scored output (Coverage collects Nov 14–16): pass `--h6-cov osf/methodology/v1_12/v112_unit_table.csv` (path on the v1.12 worktree; `v112_verdicts.json` beside it) at C1 if it exists, else at C2; without it by C2, `--h6-unavailable "REASON"` (UNDETERMINED, Paper B; §12 (x), N21). The reader refuses output whose scorer SHA-256 differs from `score_v1_12.py` at v1.12's tag, so a post-lock change to v1.12's scorer makes H6 UNDETERMINED unless logged as a deviation.
- **Part II audit:** `audit_v1_13.py --collect --pass 1` refuses until tag `v1.13-audit-r1` is local and on origin, `audit_anchor_v1_13.json` names its commit and the D_b SHA-256, `audit_receipt_v1_13.json` is at least 24 h old, and the clock is outside 2026-11-17 00:00Z–2026-11-22 12:00Z with pass 1's 72 h ending before 2026-11-17 00:00Z (so pass 1 must start between receipt + 24 h and 2026-11-14 00:00Z, else from 2026-11-22 12:00Z). It runs longer than one shell call: launch it detached with `nice -n 10` (protocol §4). Pass 2 (P1 only) 7 days after pass 1 started, outside the blocked period.
