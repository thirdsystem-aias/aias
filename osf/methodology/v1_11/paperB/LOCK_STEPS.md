# v1.11 Sentiment Paper B (human labels) — lock steps (for the coordinator)

Prepared 2026-11-11 by the runner (Paper B lane). Run only after Pablo says **"guide final"**, and before the first invitation (Fri 2026-11-13). Everything runs in the worktree `/Users/pablou/aias/_worktrees/v1.11-paperB` (branch `v1.11-paperB`, from `v1.11` @ `95c3fa1`). Never checkout, switch or commit in `/Users/pablou/aias` itself (branch `v0.40`); never move `v1.11`. Each shell call is `zsh -ic '...'` (≤ 55 s). Add the session's attribution lines to every commit message. `H=osf/methodology/v1_11/paperB/lock/paperB_lock_v1_11.py`.

## 0. Preconditions (stop if any fails)

1. Tag free, locally and on origin:
   ```
   cd /Users/pablou/aias/_worktrees/v1.11-paperB && git tag -l "v1.11-paperB*"; git ls-remote --tags origin | grep -c "v1.11-paperB"
   ```
   Expect no line, then `0`.
2. Worktree clean, on the branch: `git branch --show-current && git status --short` → `v1.11-paperB`, nothing listed.
3. **The guide has not changed since it was read (2026-11-11, version `1794364205-6bca`).** Re-read https://claude.ai/artifact/4sCt6DcfA4RD6h4TdvUdZZ (Artifact tool, read action, paths `project/Main.dc.html`, `project/Rules.dc.html`; never a web fetch). The SHA-256 the read reports must be `fc577e17…4c1744` (page 1) and `5179a1d1…2ffb` (page 2). If either differs, Pablo edited the guide after this branch was written: save both files byte for byte over `osf/methodology/v1_11/paperB/guide/source/`, then run `python3 $H --guide-md --diff-guide --sync` (the diff must report 0 differences) and update the two SHA-256 in the pre-registration §5 and in `test_paperB_lock_v1_11.py`.
4. **The statement agrees with the guide.** As read on 2026-11-11 (exercise doc, revision 8) the statement still says about 50 answers, about an hour, by January 22 and until February 1; guide page 1 says about 55, about 45 minutes, Dec 4 and December 18. Pablo revises the statement in the exercise doc (https://claude.ai/artifact/QHkHLwkqZHAaHs7pTrFTH2). Then read the doc (Claude Docs connector), write its seven paragraphs word for word, bold as `**…**`, over `osf/methodology/v1_11/paperB/statement/statement_exercise_doc.md`, update `doc_revision` and `read` in `statement_source.json`, and run `python3 $H --sync`.

## 1. Readiness check and tests (no writes outside the worktree's tracked files; temporary files in /tmp)

```
cd /Users/pablou/aias/_worktrees/v1.11-paperB && PYTHONDONTWRITEBYTECODE=1 python3 $H --check
cd /Users/pablou/aias/_worktrees/v1.11-paperB && TMPDIR=/tmp PYTHONDONTWRITEBYTECODE=1 python3 -m unittest osf/methodology/v1_11/paperB/lock/test_paperB_lock_v1_11.py 2>&1 | tail -3
```
Expect `12 of 12 checks pass` and `Ran 22 tests`, `OK`. On 2026-11-11 the check gave 11 of 12: only "statement agrees with guide page 1" failed (precondition 4). `--check` rebuilds the N = 19 variant-b packets in /tmp and compares them byte for byte with `packets/packet_design_N19_b.json`.

## 2. Content lock

```
cd /Users/pablou/aias/_worktrees/v1.11-paperB && PYTHONDONTWRITEBYTECODE=1 python3 $H --lock-manifest && PYTHONDONTWRITEBYTECODE=1 python3 $H --verify-lock && wc -l < osf/methodology/v1_11/paperB/prereg/LOCK_MANIFEST_v1_11_paperB.sha256
```
Expect `lock manifest OK` and `20`. Then change the pre-registration's status line from "r1, lock-ready, not locked (2026-11-11)" to "r1, locked (<date>)" **before** `--lock-manifest` if you want the locked text to say so (re-run step 2 after any edit). Commit:
```
cd /Users/pablou/aias/_worktrees/v1.11-paperB && git add osf/methodology/v1_11 && git commit -m "v1.11 Paper B prereg r1 content lock (guide final; statement <rev>)"
```

## 3. Tag (annotated, at the content-lock commit)

```
cd /Users/pablou/aias/_worktrees/v1.11-paperB && git tag -a v1.11-paperB-prereg-r1 -m "AIAS v1.11 Sentiment Paper B (human labels, SVA MPS Branding Class of 2027), pre-registration r1. Locked before the first invitation; no label collected, no judge call made." && git rev-parse v1.11-paperB-prereg-r1 "v1.11-paperB-prereg-r1^{commit}" HEAD
```
The second and third lines must be equal.

## 4. Push branch and tag

```
cd /Users/pablou/aias/_worktrees/v1.11-paperB && git push origin v1.11-paperB && git push origin refs/tags/v1.11-paperB-prereg-r1 && git ls-remote --tags origin v1.11-paperB-prereg-r1
```
Expect the tag object and `…^{}` = the content-lock commit.

## 5. OSF deposit (project ec6wh, osfstorage; new folder `methodology/v1_11/paperB/`)

Deposit the pre-registration and what it pins, not the student-facing packets (packets are rebuilt with the real N after Nov 20; the item key is deposited after scoring, §9) and not the 566-unit sample's text twice (it is already in v1.11's record; deposit it only if `methodology/v1_11/paperB/` on OSF lacks it).
```
cd /Users/pablou/aias/_worktrees/v1.11-paperB && for d in prereg guide statement forms packets lock; do python3 scripts/osf_upload.py osf/methodology/v1_11/paperB/$d methodology/v1_11/paperB/$d --dry-run; done
cd /Users/pablou/aias/_worktrees/v1.11-paperB && for d in prereg guide statement forms packets lock; do python3 scripts/osf_upload.py osf/methodology/v1_11/paperB/$d methodology/v1_11/paperB/$d; done
cd /Users/pablou/aias/_worktrees/v1.11-paperB && python3 scripts/osf_upload.py osf/methodology/v1_11/anchor methodology/v1_11/paperB/anchor --dry-run
```
`osf_upload.py` uploads folders: put `LOCK_STEPS.md` and `human_sample_v1_11_paperB_r1.csv` in a staging folder (`mkdir -p /tmp/pb_top && cp osf/methodology/v1_11/paperB/LOCK_STEPS.md osf/methodology/v1_11/paperB/human_sample_v1_11_paperB_r1.csv /tmp/pb_top/`) and upload it to `methodology/v1_11/paperB`. Upload `anchor/DEVIATIONS.md` (Entries 0–2) the same way to `methodology/v1_11/paperB/anchor` (v1.11's own `methodology/v1_11/anchor` keeps its deposited version).

## 6. Anchor (right after the push and the deposit)

```
cd /Users/pablou/aias/_worktrees/v1.11-paperB && PYTHONDONTWRITEBYTECODE=1 python3 $H --write-anchor --osf-note "https://osf.io/ec6wh/ (osfstorage: methodology/v1_11/paperB/ prereg, guide, statement, forms, packets, lock, anchor) deposited <UTC time>"
```
Writes `osf/methodology/v1_11/anchor/git_anchor_v1_11_paperB.json`. It refuses unless the manifest verifies, the tag is on origin and HEAD is the tagged commit. Commit and push it (the tag does not move), then deposit it to `methodology/v1_11/paperB/anchor`:
```
cd /Users/pablou/aias/_worktrees/v1.11-paperB && git add osf/methodology/v1_11/anchor/git_anchor_v1_11_paperB.json && git commit -m "v1.11 Paper B: git anchor (tag v1.11-paperB-prereg-r1; OSF deposited)" && git push origin v1.11-paperB
```

## 7. Verify the deposit by SHA-256 (read-only)

With v1.12's verifier, as in v1.14's lock steps:
```
git -C /Users/pablou/aias/_worktrees/v1.12 show 5fd87f6:osf/methodology/v1_12/lock/osf_verify_v1_12.py > /tmp/osf_verify.py && cd /Users/pablou/aias/_worktrees/v1.11-paperB && for d in prereg guide statement forms packets lock; do PYTHONDONTWRITEBYTECODE=1 python3 /tmp/osf_verify.py osf/methodology/v1_11/paperB/$d methodology/v1_11/paperB/$d; done
```
Expect PASS for each folder. On a mismatch: re-upload that folder and verify again; never edit a locked file to make it match.

## 8. After the lock (not part of it)

- Invitations go out with the statement exactly as locked; the sign-up form is built by `buildSignupForm()` from the locked `Code.gs`.
- After sign-up closes (Fri 11-20): `python3 osf/methodology/v1_11/paperB/packets/make_packets_v1_11_paperB.py --n <N> --variant b --out <dir>` (seed 111023), then `forms/mock_run.sh <dir>` before Pablo imports `packets/packets_all.csv`. A different N changes the packets, not the rule; record N and the new `packet_design.json` hashes.
- Merge note: this branch appends DEVIATIONS Entry 2 to `osf/methodology/v1_11/anchor/DEVIATIONS.md`; `v1.11` itself is not moved.
