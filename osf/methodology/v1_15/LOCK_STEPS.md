# v1.15 Sentiment on t4 — lock steps

Prepared 2026-11-10/11 (r0). Everything runs in the worktree `/Users/pablou/aias/_worktrees/v1.15` (branch `v1.15`). Never checkout, switch or commit in `/Users/pablou/aias` (branch `v0.40`) or another lane's worktree. No paid call at the lock. Each shell call is `zsh -ic '...'` (≤ 55 s), system Python 3.14.

## 0. Preconditions (stop if any fails)
1. Pablo received the r1 text ≥ 24 hours ago and typed no hold or change.
2. r1 items done (PRE_REGISTRATION §12, O1–O5 answered or carried as stated).
3. `git branch --show-current` = `v1.15`; `git status --short --untracked-files=no` empty.
4. Remote tags: `git ls-remote --tags origin v1.15-prereg-r1 v1.11-prereg-r1 v0.42-prereg-r1` → no `v1.15-prereg-r1`; `v1.11-prereg-r1` peels to `62e2d38…`; `v0.42-prereg-r1` peels to `58d1891…`. Otherwise stop and report.
5. Vendor pages re-read the same day (PRE_REGISTRATION §4 URLs): `claude-opus-5-5` Active; `gpt-6.1-sol` with the Batch endpoint; batch prices $2/$10 and $1/$5. A change → DEVIATIONS entry first, then report.

## 1. Verify (no writes)
```
python3 -m unittest osf/methodology/v1_15/scripts/tests/test_v1_15.py
python3 osf/methodology/v1_15/scripts/score_v1_15.py --cost      # must print the four Preview values 14.09 / 18.49 / 40.86 / 53.61
python3 osf/methodology/v1_15/scripts/coi_screen_v1_15.py       # Denon (v0.19) only
```

## 2. Content lock
```
python3 osf/methodology/v1_15/scripts/score_v1_15.py --lock-manifest
shasum -a 256 -c osf/methodology/v1_15/prereg/LOCK_MANIFEST_v1_15.sha256 | grep -vc ": OK$"    # expect 0
git add osf/methodology/v1_15 && git commit -m "v1.15: content lock (LOCK_MANIFEST)"
git tag -a v1.15-prereg-r1 -m "v1.15 Sentiment on t4: pre-registration r1"
git push origin v1.15 v1.15-prereg-r1
```

## 3. Anchor and OSF
```
python3 osf/methodology/v1_15/lock/write_anchor_v1_15.py --osf-deposit "osf.io/ec6wh methodology/v1_15/{prereg,anchor}"
git add osf/methodology/v1_15/anchor/git_anchor_v1_15.json && git commit -m "v1.15: anchor record" && git push origin v1.15
```
Upload `prereg/` and `anchor/` to OSF `methodology/v1_15/`; verify every SHA-256 against the manifest (`lock/osf_list_v1_15.py methodology/v1_15` lists the folder).

## 4. After the lock (not part of the lock)
After tag `v0.42-acquisition-locked` and v0.42's coded tables: `score_v1_15.py --build-units --coded-ref <commit>` → `judge_v1_15.py --dry-run` → `judge_v1_15.py --run --no-other-collection "<who, when>"` (refuses outside windows (a)/(b), §6) under `caffeinate -w <pid>` → `--freeze` → Stage J → Stage C (after v1.14 Stage 1) → outputs for the Preview.
