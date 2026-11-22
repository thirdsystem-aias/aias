# v1.13 Part II lock (Wednesday 2026-11-11, from about 9:30 pm CT): steps

Supplements `osf/methodology/v1_13/LOCK_STEPS.md` steps 3b, 4, 5 (`--audit`), 6–8 for Part II, which assumed the Part II tag would go on the Part I lock commit. Part II's text was frozen at the Part I lock commit `b83efb2` (manifest of 21 files plus the manifest itself). Clarifications 1–4 (`postlock/DEVIATIONS_continued_v1_13.md`) were logged after that commit, together with the Part I ex-ante entries 5–12 and the modules in `postlock/`. **Recommended: tag `v1.13-audit-r1` on the commit that adds `postlock/`** (named in step 2 below), so that the locked Part II record contains its clarifications. That commit changes no frozen file; step 3 proves it. Every command runs in `/Users/pablou/aias/_worktrees/v1.13`, inside `zsh -ic '...'`; nothing runs in `/Users/pablou/aias` itself.

## 0. Preconditions (stop if any fails)

1. Now ≥ 2026-11-12 03:30 UTC (9:30 pm CST): `date -u`. Pablo has not typed `hold grounding audit`.
2. `git status --short --untracked-files=no` is empty. `git log --oneline -1` shows the postlock commit, whose parent is `232cf64`.
3. `git ls-remote --tags origin v1.13-audit-r1` prints nothing.

## 1. Frozen text unchanged; tests

```
shasum -a 256 -c osf/methodology/v1_13/prereg/LOCK_MANIFEST_v1_13.sha256 | grep -vc ": OK$"
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s osf/methodology/v1_13/scripts/tests -p "test_*.py" 2>&1 | grep -E "^Ran|^OK|^FAILED"
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s osf/methodology/v1_13/postlock/tests 2>&1 | grep -E "^Ran|^OK|^FAILED"
PYTHONDONTWRITEBYTECODE=1 python3 osf/methodology/v1_13/lock/check_guards_v1_13.py; echo EXIT $?
```

Expect `0` mismatches. The locked suite reports `Ran 90`, `FAILED (errors=1)`: the one error is `test_stage_c1_refused_without_lock`, expected after the Part I lock (Entry 12). The postlock suite reports `Ran 17 … OK`. `check_guards` should print 16 `OK` lines and `EXIT 0`.

## 2. Frozen-text proof at the commit to be tagged (no write)

```
PYTHONDONTWRITEBYTECODE=1 python3 osf/methodology/v1_13/postlock/write_part2_addendum_v1_13.py --ref HEAD --dry-run | head -12
```

Expect `"differ_from_lock_commit": []` over 22 files, and the `postlock/` files listed.

## 3. Tag (local), push

```
git tag -a v1.13-audit-r1 -m "AIAS v1.13 Grounding Paper A, Part II: structured-data audit protocol r1 locked (text frozen at b83efb2, LOCK_MANIFEST_v1_13.sha256; clarifications 1-4 in postlock/DEVIATIONS_continued_v1_13.md)" HEAD && git rev-parse v1.13-audit-r1 "v1.13-audit-r1^{commit}"
git push origin v1.13 && git push origin refs/tags/v1.13-audit-r1 && git ls-remote --tags origin "v1.13-*"
```

Alternative, only if the coordinator decides it: tag `b83efb2` itself, as LOCK_STEPS.md assumed. Then step 4's `--audit` anchor names `b83efb2`, and the clarifications are dated after the Part II tag.

## 4. Anchors

```
PYTHONDONTWRITEBYTECODE=1 python3 osf/methodology/v1_13/lock/write_anchor_v1_13.py --audit
PYTHONDONTWRITEBYTECODE=1 python3 osf/methodology/v1_13/postlock/write_part2_addendum_v1_13.py
git add osf/methodology/v1_13/anchor/audit_anchor_v1_13.json osf/methodology/v1_13/postlock/part2_addendum_v1_13.json && git commit -m "v1.13 Part II anchors: audit_anchor and postlock addendum name v1.13-audit-r1 (after the lock)" && git push origin v1.13
```

`audit_anchor_v1_13.json`, read by `audit_v1_13.py --collect`, records the tag's commit, the Part II files frozen at `b83efb2` and the D_b SHA-256. `part2_addendum_v1_13.json` records the same commit, the proof that all 22 frozen files are unchanged, and the SHA-256 and git blob of every `postlock/` file at the tag (clarification log, modules, tests).

## 5. OSF (project ec6wh): deposit both

```
python3 scripts/osf_upload.py osf/methodology/v1_13/anchor methodology/v1_13/anchor --dry-run
python3 scripts/osf_upload.py osf/methodology/v1_13/anchor methodology/v1_13/anchor
python3 scripts/osf_upload.py osf/methodology/v1_13/postlock methodology/v1_13/postlock
for d in anchor postlock; do PYTHONDONTWRITEBYTECODE=1 python3 osf/methodology/v1_13/lock/osf_verify_v1_13.py osf/methodology/v1_13/$d methodology/v1_13/$d; done
```

## 6. Send the locked Part II text; receipt

Send Pablo the protocol, the clarifications (Entries 1–4) and the tag/OSF links. Then record when he received them, then commit, push, re-upload `anchor/` and verify:

```
PYTHONDONTWRITEBYTECODE=1 python3 osf/methodology/v1_13/lock/write_anchor_v1_13.py --receipt <ISO time with offset>
```

## 7. After the lock (not part of it)

- **Pass 1** must start between receipt + 24 h and **2026-11-14 00:00 UTC (Fri 6 pm CT)**. The guard refuses later starts until 2026-11-22 12:00 UTC. Command: `nice -n 10 nohup python3 osf/methodology/v1_13/scripts/audit_v1_13.py --collect --pass 1 > /tmp/v113_pass1.log 2>&1 &`. Then log the QID adjudications and run `audit_v1_13.py --sdri`. Pass 2 runs 7 days after pass 1 started, outside the blocked period.
- **Scoring** through the input-hash wrapper (Entry 10): `python3 osf/methodology/v1_13/postlock/run_stage_v1_13.py -- --stage C1 --t4 … --coded … --brand-table … [--h4-stage1 …] [--h6-cov …]`, and the same with `--stage C2`. The C2 record says whether `audit/v1_13_sdri.csv` existed when C2 started, and gives its SHA-256 (Entry 3).
- **After Stage C2:** `postlock/c2_extras_v1_13.py` (S6, S7 with `--profiles osf/aias_2_0/aias_2_0_profiles.csv`, the cited-set and primary-panel baselines, MQ2 kept). After pass 2: `postlock/audit_checks_v1_13.py --pass2 --verdicts osf/methodology/v1_13/v1_13_verdicts.json` (AQ1–AQ4, S-KG). Each writes once.
