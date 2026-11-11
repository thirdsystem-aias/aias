# v1.15 Sentiment on t4 — lock steps

Prepared 2026-11-10/11 (r0; r1 = clarification C1, code only, 2026-11-11). Lock no earlier than **Wed 2026-11-11 ~9:30 pm CT (2026-11-12 03:30 UTC)**: the r0 text reached Pablo on the panel at ~9:15 pm CT Nov 10, and C1 does not restart the 24 hours. Everything runs in the worktree `/Users/pablou/aias/_worktrees/v1.15` (branch `v1.15`). Never checkout, switch or commit in `/Users/pablou/aias` (branch `v0.40`) or another lane's worktree. No paid call and no t4 answer read at the lock. Each shell call is `zsh -ic '...'` (≤ 55 s), system Python 3.14 (`/Library/Frameworks/Python.framework/Versions/3.14/bin/python3`). Remote tags are always queried with the pattern form `git ls-remote origin "refs/tags/TAG*"` (the `--tags origin TAG` form loses the `^{}` line under git 2.54).

## 0. Preconditions (stop if any fails)
1. `date -u` ≥ 2026-11-12 03:30 UTC; Pablo typed no hold or change.
2. `git branch --show-current` = `v1.15`; `git status --short --untracked-files=no` empty; HEAD = the C1 commit (or a later lock-prep commit).
3. Remote tags:
   ```
   git ls-remote origin "refs/tags/v1.15-prereg-r1*" "refs/tags/v1.11-prereg-r1*" "refs/tags/v0.42-prereg-r1*"
   ```
   Expect: no `v1.15-prereg-r1` lines; `v1.11-prereg-r1^{}` = `62e2d3828cec…`; `v0.42-prereg-r1^{}` = `58d1891bf2fa…`. Otherwise stop and report.
4. Vendor pages re-read the same day (PRE_REGISTRATION §4 URLs): `claude-opus-5-5` Active; `gpt-6.1-sol` lists the Batch endpoint; batch prices $2/$10 and $1/$5. A change → DEVIATIONS entry first, then report.

## 1. Verify (no writes)
```
python3 -m unittest osf/methodology/v1_15/scripts/tests/test_v1_15.py      # 36 tests, OK (~30 s; includes the Preview-reader check under /tmp)
python3 osf/methodology/v1_15/scripts/score_v1_15.py --cost                 # rewrites cost_estimate_v1_15.json; values 14.09 / 18.49 / 40.86 / 53.61; git diff must be empty
python3 osf/methodology/v1_15/scripts/coi_screen_v1_15.py                   # Denon (v0.19) only
shasum -a 256 -c osf/methodology/v1_15/prereg/LOCK_MANIFEST_v1_15.sha256 | grep -vc ": OK$"   # expect 0 (15 lines)
```
If a manifested file changed after C1, rebuild the manifest (step 2, first line) and re-check.

## 2. Content lock
```
python3 osf/methodology/v1_15/scripts/score_v1_15.py --lock-manifest
git add osf/methodology/v1_15 && git commit -m "v1.15: content lock (LOCK_MANIFEST)"      # skip if nothing changed
git tag -a v1.15-prereg-r1 -m "v1.15 Sentiment on t4: pre-registration r1"
git push origin v1.15 v1.15-prereg-r1
git ls-remote origin "refs/tags/v1.15-prereg-r1*"                                       # two lines: the tag and its ^{}
```

## 3. Anchor and OSF
```
python3 osf/methodology/v1_15/lock/write_anchor_v1_15.py --osf-deposit "osf.io/ec6wh methodology/v1_15/{prereg,anchor}"
git add osf/methodology/v1_15/anchor/git_anchor_v1_15.json && git commit -m "v1.15: anchor record" && git push origin v1.15
```
Upload `prereg/` and `anchor/` to OSF `methodology/v1_15/`; verify every SHA-256 against the manifest (`lock/osf_list_v1_15.py methodology/v1_15` lists the folder). The anchor helper refuses unless origin lists both the tag and its peeled line and every locked file on disk equals the tag's tree.

## 4. After the lock (not part of the lock)
1. After tag `v0.42-acquisition-locked` and v0.42's coded tables: `score_v1_15.py --build-units --coded-ref <commit>` (the ref and its commit are written to `u0_v1_15.json` → `refs`).
2. `judge_v1_15.py --dry-run`; then `judge_v1_15.py --run --no-other-collection "<who, when>"` under `caffeinate -w <pid>` (refuses outside windows (a)/(b), PRE_REGISTRATION §6); `--approve-past-pause "<who, when>"` only with Pablo's recorded approval; `--freeze`.
3. `score_v1_15.py --stage J` → `outputs/stage_j_v1_15.json`, `outputs/s_t4_v1_15.csv` (none if a halt fired). Check with `lock/preview_reader_check_v1_15.py osf/methodology/v1_15/outputs/s_t4_v1_15.csv`.
4. After v1.14's Stage 1: `score_v1_15.py --stage C --v114-ref <ref>` → `outputs/v1_15_verdicts.json`.
5. Commit the outputs (the Preview's MQ_Blind compares this commit's date with the Preview's tag). The Preview reads: `--s-t4 <commit>:osf/methodology/v1_15/outputs/s_t4_v1_15.csv:S_t4:rated --s-t4-lock-tag v1.15-prereg-r1`.
