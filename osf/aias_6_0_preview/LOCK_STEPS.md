# AIAS™ 6.0 Preview — lock steps (Wed 2026-11-11 evening or Thu 2026-11-12)

Prepared 2026-11-10 (about 5:45 pm CT) by the runner (Preview r1 lane). Everything below runs in the worktree `/Users/pablou/aias/_worktrees/aias-6.0-preview` (branch `aias-6.0-preview`). Never checkout, switch or commit in `/Users/pablou/aias` itself (branch `v0.40`) or in another worktree. Each shell call is `zsh -ic '...'` (≤ 55 s); the commands below use only double quotes so they fit inside it. Add the session's attribution lines to each commit message (`-m "<attribution>"`).

**Tag name.** The pre-registration (§0, §11.2, §11.4), DEVIATIONS Entry 0 and the scorer (`PREREG_TAG`, checked by MQ_Lock and MQ_Blind) name the tag **`aias-6-0-preview-prereg-r1`** (dashes, as `aias-2-0-*`). The brief of 2026-11-10 wrote `aias-6.0-preview-prereg-r1`; use the dashed name, or `--run` will refuse at the data lock.

**Order.** v1.12 lock → v1.13 Part I lock → v0.42 lock (each with its own `LOCK_STEPS.md`) → these steps. Recommended: Wed evening or Thu. Latest safe: the earlier of Sat 2026-11-14 (end of day CT) and the first run of v0.42's scorer on t4 (pre-registration §11.1).

## 0. Preconditions (stop if any fails)

1. **Pablo:** his 24 hours on r0 ended (about 5 pm CT Wed Nov 11) with no change requested, and the coordinator has decided whether the ex-ante clarifications C1–C2 (`anchor/DEVIATIONS.md`; §2, §11.2 rows MQ_Lock and MQ_Join) restart them. A change to a hypothesis, test, band, threshold or decision rule restarts the 24 hours: do not lock; report.
2. **Component tags on origin** (v0.42, v1.12, v1.13 new; v1.14, v1.11, AIAS 2.0 already locked):
   ```
   cd /Users/pablou/aias/_worktrees/aias-6.0-preview && git fetch -q origin --tags && git fetch -q origin && git ls-remote --tags origin v0.42-prereg-r1 v1.12-prereg-r1 v1.13-prereg-r1 v1.14-prereg-r1 v1.11-prereg-r1 aias-2-0-data-locked
   ```
   Expect one line per tag, six in all.
3. **No t4-based component score exists anywhere in the repository** (§11.1):
   ```
   cd /Users/pablou/aias/_worktrees/aias-6.0-preview && for p in osf/v42/v42_brand_table.csv osf/methodology/v1_14/outputs/stage1/stage1_v1_14.json osf/methodology/v1_12/v112_unit_table.csv osf/methodology/v1_13/v1_13_verdicts.json; do echo "$p $(git log --all --oneline --diff-filter=A -- $p | wc -l)"; done
   ```
   Expect four lines ending in `0`. (`--write-anchor` re-checks and refuses otherwise.)
4. **Worktree clean, on the branch:**
   ```
   cd /Users/pablou/aias/_worktrees/aias-6.0-preview && git branch --show-current && git status --short && git log --oneline -3
   ```
   Expect `aias-6.0-preview`, no status output, HEAD = the r1 commit (or a later re-pin commit of step 2).

## 1. Pin report (read-only)

```
cd /Users/pablou/aias/_worktrees/aias-6.0-preview && PYTHONDONTWRITEBYTECODE=1 python3 -I osf/aias_6_0_preview/scripts/score_aias_6_0_preview.py --pin-report
```
Expect exit 1 with `"problems"` listing exactly six PENDING values: `v0.42.lock_commit`, `v1.12.lock_commit`, `v1.12.h5_active_at_lock`, `v1.13.lock_commit`, `v1.13.h4_active_at_lock`, `v1.13.h6_active_at_lock` (no "lock tag … not found", no blob line). For each of v0.42, v1.12, v1.13 the report shows `tag_commit` (40 hex), every `*_blob` with `at_tag` equal to `pinned`, every `output_names_in_tagged_scorer` true; for v1.12 `h5_active_at_lock` and for v1.13 `h4_active_at_lock`, `h6_active_at_lock` (true or false, read from their anchors on origin: `osf/methodology/v1_12/anchor/osf_anchor_v1_12.json`, `osf/methodology/v1_13/anchor/git_anchor_v1_13.json`). If a report shows `"activation": "anchor not found yet"`, wait for that component's anchor commit to be pushed, `git fetch -q origin`, and repeat.

(At r1, on 2026-11-10, the report listed these six values plus "lock tag … not found" for v0.42, v1.12 and v1.13, as expected before their locks; v1.14 and v1.11 matched their pins.)

## 2. Pin: edit the `INPUTS` block only (the one configuration block)

In `osf/aias_6_0_preview/scripts/score_aias_6_0_preview.py` replace, with the values of step 1:

| Find (exact text) | Replace with |
|---|---|
| `"lock_tag": "v0.42-prereg-r1", "lock_commit": PENDING,` | `"lock_tag": "v0.42-prereg-r1", "lock_commit": "<v0.42 tag_commit>",` |
| `"lock_tag": "v1.12-prereg-r1", "lock_commit": PENDING,` | `"lock_tag": "v1.12-prereg-r1", "lock_commit": "<v1.12 tag_commit>",` |
| `"h5_active_at_lock": PENDING},` | `"h5_active_at_lock": True},` (or `False`) |
| `"lock_tag": "v1.13-prereg-r1", "lock_commit": PENDING,` | `"lock_tag": "v1.13-prereg-r1", "lock_commit": "<v1.13 tag_commit>",` |
| `"h4_active_at_lock": PENDING, "h6_active_at_lock": PENDING},` | `"h4_active_at_lock": True, "h6_active_at_lock": True},` (each True or False) |

**If anything else is in `problems`** (a blob whose `at_tag` differs from `pinned`, an output name false, a tag missing): that component changed at its lock. Set the pinned blob to `at_tag`; read the component's scorer at its tag (`git show <tag>:<scorer path>`) for the new output path or column and update that entry of `INPUTS`; append a dated ex-ante entry to `anchor/DEVIATIONS.md` (what moved, old → new). **If a component did not lock:** replace its entry by `{"status": NOT_LOCKED}` (NOT RUN for the Preview), log it in DEVIATIONS and tell Pablo. Then:
```
cd /Users/pablou/aias/_worktrees/aias-6.0-preview && PYTHONDONTWRITEBYTECODE=1 python3 -I osf/aias_6_0_preview/scripts/score_aias_6_0_preview.py --pin-report | tail -3 && git diff --stat
```
Expect `"problems": []` and a diff of the scorer only (plus DEVIATIONS if an entry was logged).

## 3. Tests (about 30 s; in the background)

```
cd /Users/pablou/aias/_worktrees/aias-6.0-preview && (PYTHONDONTWRITEBYTECODE=1 nohup python3 -I osf/aias_6_0_preview/scripts/tests/test_score_aias_6_0_preview.py > /tmp/aias6_tests.log 2>&1 &); sleep 45; tail -4 /tmp/aias6_tests.log
```
Expect `Ran 57 tests`, `OK` and the dry-run line (if not yet there: `sleep 15; tail -4 /tmp/aias6_tests.log`). Every test uses scratch repositories and temporary directories; none reads program data.

## 4. Lock manifest (9 files)

```
cd /Users/pablou/aias/_worktrees/aias-6.0-preview && PYTHONDONTWRITEBYTECODE=1 python3 -I osf/aias_6_0_preview/scripts/score_aias_6_0_preview.py --lock-manifest && shasum -a 256 -c osf/aias_6_0_preview/prereg/LOCK_MANIFEST_aias_6_0_preview.sha256 && PYTHONDONTWRITEBYTECODE=1 python3 -I osf/aias_6_0_preview/scripts/score_aias_6_0_preview.py --verify-lock
```
Expect nine `: OK` lines (pre-registration, precision record and script, scorer and tests, DEVIATIONS, README, `scripts/score_v1_10.py`, `scripts/score_v1_14.py`) and `lock manifest OK (on disk; the tag does not exist yet)`. If any listed file changes after this step, run step 4 again.

## 5. Commit

```
cd /Users/pablou/aias/_worktrees/aias-6.0-preview && git add osf/aias_6_0_preview && git status --short && git commit -q -m "AIAS 6.0 Preview r1: content lock (component pins after the Nov 11 locks; lock manifest, 9 files)" -m "<attribution>" && git log --oneline -1
```

## 6. Tag (local)

```
cd /Users/pablou/aias/_worktrees/aias-6.0-preview && git tag -a aias-6-0-preview-prereg-r1 -m "AIAS 6.0 Preview: pre-registration r1 locked (prereg/LOCK_MANIFEST_aias_6_0_preview.sha256, 9 files)" HEAD && git rev-parse aias-6-0-preview-prereg-r1 "aias-6-0-preview-prereg-r1^{commit}"
```
Record the tag object and the commit.

## 7. Push branch and tag

```
cd /Users/pablou/aias/_worktrees/aias-6.0-preview && git push origin aias-6.0-preview && git push origin refs/tags/aias-6-0-preview-prereg-r1 && git ls-remote --tags origin aias-6-0-preview-prereg-r1
```
Expect the tag line with step 6's tag object.

## 8. Anchor JSON (`--run` refuses without it: MQ_Lock)

```
cd /Users/pablou/aias/_worktrees/aias-6.0-preview && PYTHONDONTWRITEBYTECODE=1 python3 -I osf/aias_6_0_preview/scripts/score_aias_6_0_preview.py --write-anchor --osf-note "https://osf.io/ec6wh/ (osfstorage: aias_6_0_preview/prereg, aias_6_0_preview/scoping, aias_6_0_preview/anchor)"
```
Writes `osf/aias_6_0_preview/anchor/git_anchor_aias_6_0_preview.json`: tag, tag object, commit, tree, tagger date, remote tag ref, repository URL, every locked file (SHA-256 checked on disk and at the tag, git blob at the tag), the manifest's SHA-256 and blob, the pinned `INPUTS`, each component lock tag's object, commit and tagger date, and the t4-based score files present in the repository (must be none). It refuses if the anchor exists, a pin is PENDING or wrong, the manifest does not verify on disk and at the tag, the tag is not on origin or differs from the local tag, HEAD is not the tagged commit, or a t4-based score file exists (then stop and report: the lock is late, §11.1; `--late-reason "..."` records it only on Pablo's decision, and MQ_Blind then applies). Commit and push the anchor (the tag does not move), then check MQ_Lock:
```
cd /Users/pablou/aias/_worktrees/aias-6.0-preview && git add osf/aias_6_0_preview/anchor/git_anchor_aias_6_0_preview.json && git commit -q -m "AIAS 6.0 Preview anchor: git_anchor_aias_6_0_preview.json names aias-6-0-preview-prereg-r1 (after the lock)" -m "<attribution>" && git push origin aias-6.0-preview && PYTHONDONTWRITEBYTECODE=1 python3 -I osf/aias_6_0_preview/scripts/score_aias_6_0_preview.py --verify-lock
```
Expect `lock manifest OK (on disk and at tag aias-6-0-preview-prereg-r1)` and `MQ_Lock OK (tag, anchor, manifest)`.

## 9. OSF deposit (project ec6wh, osfstorage) and SHA-256 verification

OSF `aias_6_0_preview/prereg/` holds `draft_r0/` (r0): leave it. Per §0 the deposit is `prereg/`, `scoping/` and `anchor/`; the scripts are fixed by the tag and by their SHA-256 in the manifest and the anchor. Check, dry run, upload, verify:
```
cd /Users/pablou/aias/_worktrees/aias-6.0-preview && ls osf/aias_6_0_preview/prereg osf/aias_6_0_preview/scoping osf/aias_6_0_preview/anchor
cd /Users/pablou/aias/_worktrees/aias-6.0-preview && python3 scripts/osf_upload.py osf/aias_6_0_preview/prereg aias_6_0_preview/prereg --dry-run && python3 scripts/osf_upload.py osf/aias_6_0_preview/scoping aias_6_0_preview/scoping --dry-run && python3 scripts/osf_upload.py osf/aias_6_0_preview/anchor aias_6_0_preview/anchor --dry-run
cd /Users/pablou/aias/_worktrees/aias-6.0-preview && python3 scripts/osf_upload.py osf/aias_6_0_preview/prereg aias_6_0_preview/prereg
cd /Users/pablou/aias/_worktrees/aias-6.0-preview && python3 scripts/osf_upload.py osf/aias_6_0_preview/scoping aias_6_0_preview/scoping
cd /Users/pablou/aias/_worktrees/aias-6.0-preview && python3 scripts/osf_upload.py osf/aias_6_0_preview/anchor aias_6_0_preview/anchor
cd /Users/pablou/aias/_worktrees/aias-6.0-preview && python3 osf/aias_6_0_preview/lock/osf_verify_aias_6_0_preview.py osf/aias_6_0_preview/prereg aias_6_0_preview/prereg --ignore draft_r0/ | tail -1
cd /Users/pablou/aias/_worktrees/aias-6.0-preview && python3 osf/aias_6_0_preview/lock/osf_verify_aias_6_0_preview.py osf/aias_6_0_preview/scoping aias_6_0_preview/scoping | tail -1
cd /Users/pablou/aias/_worktrees/aias-6.0-preview && python3 osf/aias_6_0_preview/lock/osf_verify_aias_6_0_preview.py osf/aias_6_0_preview/anchor aias_6_0_preview/anchor | tail -1
```
Expect `prereg` = 3 files (pre-registration, precision record, manifest), `scoping` = 1, `anchor` = 2 (`DEVIATIONS.md`, `git_anchor_aias_6_0_preview.json`), and `3 of 3 local files match; 0 extra on OSF -> PASS`, `1 of 1 … PASS`, `2 of 2 … PASS`. On a mismatch: re-upload that folder and verify again; never edit a locked file to make it match. `--list aias_6_0_preview` shows the folder read-only. **The lock is complete here:** report the tag object, the commit, the anchor commit and the three verifications.

## 10. Later: the data lock (§11.4), for reference

After v1.14 Stage 2 if its output exists by Fri 2026-12-11, otherwise on Dec 11: fetch every component ref, tag `aias-6-0-preview-data-locked`, then score once:
```
cd /Users/pablou/aias/_worktrees/aias-6.0-preview && PYTHONDONTWRITEBYTECODE=1 python3 -I osf/aias_6_0_preview/scripts/score_aias_6_0_preview.py --run --ref v0.42=v0.42-scoring-locked --ref v1.14=<ref holding v1.14's Stage 1/2 outputs> --ref v1.12=<ref holding v112_verdicts.json and v112_unit_table.csv> --ref v1.13=<ref holding v1_13_verdicts.json> --ref v1.11=<ref holding v1.11's Stage C outputs>
```
(add `--s-t4 REF:PATH:COLUMN[:RATED_COL] --s-t4-lock-tag TAG` only if a t4 Sentiment study is locked and scored, §3.4). A component given no `--ref` is NOT RUN. `--run` refuses without MQ_Lock, with a PENDING or non-matching pin, or when `outputs/` already holds its files, and halts on MQ_Join, MQ_Parity, a scorer blob at a ref that differs from its pin, or a cross-record SHA-256 that differs (v1.14 read another v0.42 brand table; v1.12's H5 or v1.13's H4 read another Stage 1 file; v1.13's H6 another v1.12 table). It writes `outputs/gates_aias_6_0_preview.json` first (MQ_Gate), then the results, the per-unit profile and `inputs_read_aias_6_0_preview.json`.
