# v1.14 r2 — re-lock steps (before any t4 answer exists)

Prepared 2026-11-10, ~6 pm CT, by the runner (v1.14 r2 lane). Why: DEVIATIONS Entry 1 (r1's Stage 1 crashes when a brand is ranked only with search on; crash fix only, no statistic changed). Everything below runs in the worktree `/Users/pablou/aias/_worktrees/v1.14` (branch `v1.14`). Never checkout, switch or commit in `/Users/pablou/aias` itself (branch `v0.40`). Each shell call is `zsh -ic '...'` (≤ 55 s). Add the session's attribution lines to every commit message.

**Commit to tag:** `a5feb4b1c4b9e9d19979129afcfd616a50b88c64` (r2 content lock; parent `4643d56` = r1's anchor commit; tree `5979752ed0c21f9d11022c90c2d752c664d59774`).
Scorer `scripts/score_v1_14.py` at that commit: SHA-256 `b087fc818105710079e8fea3c8c279373f787efe48c62cbccdcfb0392e1484ce`, git blob `7aeb18316a23c699a0a6a4358e52ab09f9546ca9` (r1: `681257b8…`, blob `c479004c…`). `prereg/LOCK_MANIFEST_v1_14.sha256`: 16 files, SHA-256 `a5c30ae372fe989d155aa5cb8fc7f7ea60778de82b0dab83308cf0f295c960ae`. Pre-registration SHA-256 `b1d8d9d2f06a231ccf86325cd4f68bce8fbba7183a75a373587c4a7069e65f4d`. `calibration/calibration_v1_14.json` unchanged (`7a84cabc…`).

This file is **untracked on purpose**: `--write-anchor` refuses unless HEAD is the tagged commit, so nothing may be committed on top of `a5feb4b` before step 5. It is committed with the anchor in step 5.

## 0. Preconditions (stop if any fails)

1. **No t4 answer exists, and the v1.12 / v1.13 locks have not happened** (the r2 anchor must record the same component-leg activation as r1: Coverage and Grounding inactive):
   ```
   cd /Users/pablou/aias/_worktrees/v1.14 && git ls-remote --tags origin | grep -v "\^{}" | sed "s#.*refs/tags/##" | grep -E "^v(0\.42|1\.1[1-4])"
   ```
   Expect exactly `v1.11-prereg-r1` and `v1.14-prereg-r1` (a `v0.42-prereg-r1` alone is acceptable only if v0.42 has not started collecting; `v0.42-acquisition-locked` must not exist). If any `v1.12-prereg-r*` or `v1.13-prereg-r*` tag exists: **stop and report** (writing the r2 anchor now would mark a leg active that r1 recorded inactive). If `v1.14-prereg-r2` already exists: stop and report.
2. **Worktree and remote branch:**
   ```
   cd /Users/pablou/aias/_worktrees/v1.14 && git branch --show-current && git rev-parse HEAD && git status --short --untracked-files=no && git status --short | grep -v "^?? osf/methodology/v1_14/LOCK_STEPS_r2.md$"; git ls-remote origin refs/heads/v1.14
   ```
   Expect `v1.14`, `a5feb4b1c4b9e9d19979129afcfd616a50b88c64`, no tracked change, no other untracked file, and origin's `v1.14` at `4643d56aceabbe00c49ff68b31b16c8859dccc94` (the push in step 3 is a fast-forward).

## 1. Verify the content lock (no writes; never run `--calibration`)

```
cd /Users/pablou/aias/_worktrees/v1.14 && PYTHONDONTWRITEBYTECODE=1 python3 scripts/score_v1_14.py --verify-lock && shasum -a 256 -c osf/methodology/v1_14/prereg/LOCK_MANIFEST_v1_14.sha256 | grep -vc ": OK$"; wc -l < osf/methodology/v1_14/prereg/LOCK_MANIFEST_v1_14.sha256; shasum -a 256 osf/methodology/v1_14/prereg/LOCK_MANIFEST_v1_14.sha256; git rev-parse HEAD:scripts/score_v1_14.py
```
Expect `lock manifest OK`, `0`, `16`, manifest `a5c30ae3…`, blob `7aeb1831…`.

Tests (~30 s; temporary files in /tmp only):
```
cd /Users/pablou/aias/_worktrees/v1.14 && TMPDIR=/tmp PYTHONDONTWRITEBYTECODE=1 python3 -m unittest scripts/test_score_v1_14.py > /tmp/v114_r2_tests.log 2>&1; tail -3 /tmp/v114_r2_tests.log; git status --short --untracked-files=no
```
Expect `Ran 34 tests`, `OK`, and no tracked change.

## 2. Tag (local, annotated, at the r2 commit)

```
cd /Users/pablou/aias/_worktrees/v1.14 && git tag -a v1.14-prereg-r2 -m "AIAS v1.14 Ranking redesign (modal position), pre-registration r2. Locked Tue 2026-11-10 before v0.42 (t4) is locked: no t4 answer exists. Supersedes r1 (v1.14-prereg-r1, 20fbc342) by a crash fix in the Stage 1 unit listing only; no statistic changed (DEVIATIONS Entry 1)." a5feb4b1c4b9e9d19979129afcfd616a50b88c64 && git rev-parse v1.14-prereg-r2 "v1.14-prereg-r2^{commit}"
```
Record the tag object (first line). The second line must be `a5feb4b1c4b9e9d19979129afcfd616a50b88c64`.

## 3. Push branch and tag

```
cd /Users/pablou/aias/_worktrees/v1.14 && git push origin v1.14 && git push origin refs/tags/v1.14-prereg-r2 && git ls-remote --tags origin v1.14-prereg-r2
```
Expect two lines: the tag object of step 2, and `…refs/tags/v1.14-prereg-r2^{}` = `a5feb4b1c4b9e9d19979129afcfd616a50b88c64`. Tag `v1.14-prereg-r1` stays on origin as the record of r1.

## 4. OSF deposit of `prereg/` and `calibration/` (project ec6wh, osfstorage; r1's order)

r1's folders `methodology/v1_14/prereg`, `calibration`, `anchor` stay as they are. r2 goes to a new subfolder `methodology/v1_14/r2/`.
```
cd /Users/pablou/aias/_worktrees/v1.14 && git status --short osf/methodology/v1_14/prereg osf/methodology/v1_14/calibration && ls osf/methodology/v1_14/prereg osf/methodology/v1_14/calibration
```
Expect no `git status` output; prereg = `LOCK_MANIFEST_v1_14.sha256`, `PRE_REGISTRATION_v1_14.md`; calibration = `calibration_run_v1_14.log`, `calibration_v1_14.json`. Dry run, then upload (`OSF_TOKEN` is set in the login shell):
```
cd /Users/pablou/aias/_worktrees/v1.14 && python3 scripts/osf_upload.py osf/methodology/v1_14/prereg methodology/v1_14/r2/prereg --dry-run && python3 scripts/osf_upload.py osf/methodology/v1_14/calibration methodology/v1_14/r2/calibration --dry-run
cd /Users/pablou/aias/_worktrees/v1.14 && python3 scripts/osf_upload.py osf/methodology/v1_14/prereg methodology/v1_14/r2/prereg
cd /Users/pablou/aias/_worktrees/v1.14 && python3 scripts/osf_upload.py osf/methodology/v1_14/calibration methodology/v1_14/r2/calibration
```

## 5. Anchor (right after the push; before any v1.12 / v1.13 tag exists)

```
cd /Users/pablou/aias/_worktrees/v1.14 && PYTHONDONTWRITEBYTECODE=1 python3 scripts/score_v1_14.py --write-anchor --osf-note "https://osf.io/ec6wh/ (osfstorage: methodology/v1_14/r2/prereg, methodology/v1_14/r2/calibration, methodology/v1_14/r2/anchor)"
```
Writes `osf/methodology/v1_14/anchor/git_anchor_v1_14.json` (r1's anchor is kept as `anchor/git_anchor_v1_14_r1.json`). It refuses unless the manifest verifies, the tag is on origin and HEAD is the tagged commit. Check it against r1's activation record:
```
cd /Users/pablou/aias/_worktrees/v1.14 && python3 -c "import json, sys; a, b = (json.load(open(p)) for p in sys.argv[1:]); print(a[\"tag\"], a[\"commit\"], a[\"lock_manifest_sha256\"]); print(\"activation identical to r1:\", a[\"activation\"] == b[\"activation\"]); print({k: (v[\"latest\"], v[\"active\"]) for k, v in a[\"activation\"].items()})" osf/methodology/v1_14/anchor/git_anchor_v1_14.json osf/methodology/v1_14/anchor/git_anchor_v1_14_r1.json
```
Expect `v1.14-prereg-r2 a5feb4b1c4b9e9d19979129afcfd616a50b88c64 a5c30ae3…`, `activation identical to r1: True`, and `{'Coverage': (None, False), 'Grounding': (None, False), 'Sentiment': ('v1.11-prereg-r1', False)}`. If not identical: do not commit; move the new anchor out of the worktree (`mv osf/methodology/v1_14/anchor/git_anchor_v1_14.json /tmp/`) and report.

Commit and push the anchor with this file (the tag does not move):
```
cd /Users/pablou/aias/_worktrees/v1.14 && git add osf/methodology/v1_14/anchor/git_anchor_v1_14.json osf/methodology/v1_14/LOCK_STEPS_r2.md && git commit -m "v1.14: git anchor r2 (tag v1.14-prereg-r2; OSF r2 prereg + calibration deposited; component legs inactive)" && git push origin v1.14
```

## 6. OSF deposit of `anchor/`

```
cd /Users/pablou/aias/_worktrees/v1.14 && ls osf/methodology/v1_14/anchor && python3 scripts/osf_upload.py osf/methodology/v1_14/anchor methodology/v1_14/r2/anchor --dry-run
cd /Users/pablou/aias/_worktrees/v1.14 && python3 scripts/osf_upload.py osf/methodology/v1_14/anchor methodology/v1_14/r2/anchor
```
Expect three files: `DEVIATIONS.md` (Entries 0–1), `git_anchor_v1_14.json` (r2), `git_anchor_v1_14_r1.json` (r1's anchor, byte-identical to r1's deposited `git_anchor_v1_14.json`, SHA-256 `378c873f…`).

## 7. Verify the deposit by SHA-256 (read-only)

v1.12's generic verifier (read-only; lists the OSF folder, compares every local file's SHA-256, fails on a missing or extra file), taken from commit `5fd87f6` so the v1.12 worktree's state does not matter:
```
git -C /Users/pablou/aias/_worktrees/v1.12 show 5fd87f6:osf/methodology/v1_12/lock/osf_verify_v1_12.py > /tmp/osf_verify.py && cd /Users/pablou/aias/_worktrees/v1.14 && PYTHONDONTWRITEBYTECODE=1 python3 /tmp/osf_verify.py osf/methodology/v1_14/prereg methodology/v1_14/r2/prereg && PYTHONDONTWRITEBYTECODE=1 python3 /tmp/osf_verify.py osf/methodology/v1_14/calibration methodology/v1_14/r2/calibration && PYTHONDONTWRITEBYTECODE=1 python3 /tmp/osf_verify.py osf/methodology/v1_14/anchor methodology/v1_14/r2/anchor
```
Expect `2 of 2 local files match; 0 extra on OSF -> PASS`, `2 of 2 … PASS`, `3 of 3 … PASS`. On a mismatch: re-upload that folder and verify again; never edit a locked file to make it match.

Optional, r1's deposit untouched (read-only): `rm -rf /tmp/v114_r1 && mkdir -p /tmp/v114_r1 && git -C /Users/pablou/aias/_worktrees/v1.14 archive v1.14-prereg-r1 osf/methodology/v1_14/prereg | tar -x -C /tmp/v114_r1 && PYTHONDONTWRITEBYTECODE=1 python3 /tmp/osf_verify.py /tmp/v114_r1/osf/methodology/v1_14/prereg methodology/v1_14/prereg` → `2 of 2 … PASS`.

## 8. After the re-lock (not part of it)

- Report: tag object, commit `a5feb4b1…`, anchor commit, the three OSF verifications.
- The downstream branches were re-pointed locally on 2026-11-10 (commits not pushed; each logged in its own record): `v1.12` @ `0201cc112195acd311e660310c27ee574a81b1d2` (§12 (z); N1 re-run, PASS, identical statistics; manifest rebuilt), `v1.13` @ `4086851aa8becfd81ec0a0d8fb7a891318121bc0` (§12 (y); manifest rebuilt), `v0.42` @ `acebca95fbfac9560f10b882aaf219c0bad5ac1e` (`osf/v42/LOCK_STEPS.md` only), `aias-6.0-preview` @ `7fb886a024f45a3fc16d56fbab9d0d2b2cf7573b` (C3, `INPUTS["v1.14"]`). Their own lock steps check `v1.14-prereg-r2` → `a5feb4b1…` on origin, so this re-lock must be finished before the v1.12 lock. v1.13's `check_records_v1_13.py` shows one FAIL (`v1.14-prereg-r2 -> None`) until the tag of step 2 exists.
- Stage 1 (`--stage 1 --v042-scored-ref <ref>`) refuses without tag `v1.14-prereg-r2`, the r2 anchor, `v0.42-acquisition-locked` and an unchanged manifest, as before.
