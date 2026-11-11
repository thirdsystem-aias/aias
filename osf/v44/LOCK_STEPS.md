# v0.44 industry-breadth wave: lock steps (Wednesday 2026-11-11, not before ~3 pm CT)

Prepared 2026-11-10 (lane 12). Template: `_worktrees/v1.12` commit 5fd87f6 (`osf/methodology/v1_12/LOCK_STEPS.md`). Everything runs in the worktree `/Users/pablou/aias/_worktrees/v0.44` (branch `v0.44`). Never checkout, switch or commit in `/Users/pablou/aias` itself (branch `v0.40`, another job). No paid call and no `--collect` at the lock. Each shell call is `zsh -ic '...'` (55 s or less). Set `export PYTHONDONTWRITEBYTECODE=1` in each call.

State prepared on 2026-11-10: `LOCK_MANIFEST_v0_44.sha256` built for the **eight-industry** design (43 files, identical to the draft manifest; `shasum -a 256 -c` all OK); 62 tests pass; the dry run equals `prereg/dry_run_v0_44.txt`; no tag, no push, no OSF upload. Updated 2026-11-11 (clarification C11, pre-lock dry run on fake SDKs): the manifest was rebuilt (43 files; it now differs from the draft manifest in six files: the prereg, `tests_v0_44.txt`, `acquire_v0_44.py`, `score_v0_44.py` and the two test files); 68 tests pass; the dry run still equals `prereg/dry_run_v0_44.txt`; P1 PASS. If Pablo typed "drop pharmacies", the manifest must be rebuilt (step 1). If any manifested file changes otherwise, redo steps 2-3.

## 0. Preconditions (stop and report if any fails)

1. Time: now >= 2026-11-11 21:00 UTC (3 pm CST) and 24 hours after Pablo received r1 (announced ~2:45 pm CT Nov 10; use the later of the two). `date -u`
2. Pablo has not typed "hold v0.44". Any other change to the industry list or text restarts the 24 hours: do not lock.
3. Worktree clean on v0.44:
   ```
   cd /Users/pablou/aias/_worktrees/v0.44 && git branch --show-current && git status --short --untracked-files=no && git log --oneline -3
   ```
   Expect `v0.44`, no tracked changes, HEAD = the lane-12 lock-prep commit (or a later one made for the lock). `osf/v44/_osf_stage_draft/` is untracked: leave it, never upload it.
4. No v0.44 tag yet, and the booked collections are not touched:
   ```
   cd /Users/pablou/aias/_worktrees/v0.44 && git ls-remote --tags origin v0.44-prereg-r1
   ```
   Expect no output.
5. Re-read the vendor model and price pages (prereg §9 lock step). If a model ID or a price changed, stop and report; a newer flagship is not substituted, only reported.

## 1. Pharmacies-drop variant (ONLY if Pablo typed "drop pharmacies"; otherwise skip to step 2)

Exactly prereg §3.4; it does not restart the 24 hours. Touch nothing else.
```
cd /Users/pablou/aias/_worktrees/v0.44 && grep -n "^PHA" osf/v44/registries/industries_v0_44.csv
```
a. Remove the `PHA` row from `osf/v44/registries/industries_v0_44.csv` (edit; leave `pha_pharmacies.csv` in place).
b. In `osf/v44/registries/excluded_v0_44.csv` mark the pharmacy registry as "industry dropped before the lock (COI)" in the form that file already uses for exclusions.
c. Re-run the two generators, then tests, P1, dry run:
```
cd /Users/pablou/aias/_worktrees/v0.44 && python3 osf/v44/scripts/build_probes_v0_44.py && python3 osf/v44/scripts/cost_estimate_v0_44.py
cd /Users/pablou/aias/_worktrees/v0.44 && python3 osf/v44/scripts/tests/run_all_v0_44.py 2>&1 | tail -4
cd /Users/pablou/aias/_worktrees/v0.44 && python3 osf/v44/scripts/score_v0_44.py --parity-p1 && python3 osf/v44/scripts/acquire_v0_44.py > osf/v44/prereg/dry_run_v0_44.txt 2>&1; tail -15 osf/v44/prereg/dry_run_v0_44.txt
```
Expect 68 tests OK, 807 calls (42 Phase B + 143 Phase A questions), $24.06 central / $46.36 high at November prices, P1 PASS. Check `git diff --stat`: only the registry list, the probe file and its md view, the cost files, the dry run (and `tests_v0_44.txt` if you refresh it with the runner's output) change.
d. Prereg text: use the seven-industry COI sentence of §8, and log the change in prereg §9 and in `osf/v44/DEVIATIONS.md` (dated, "pre-lock option §3.4, not a deviation"). The probe SHA-256 quoted in the prereg (its section on the probe file; the P2 gate reads the manifest) must equal the new `shasum -a 256 osf/v44/prereg/probes_v0_44.jsonl`; update the quoted hash.
e. Use `--pharmacies-dropped` in step 4. Continue with step 2.

## 2. Verify, then write the lock manifest (no tag)

```
cd /Users/pablou/aias/_worktrees/v0.44 && python3 osf/v44/scripts/tests/run_all_v0_44.py 2>&1 | tail -4
cd /Users/pablou/aias/_worktrees/v0.44 && python3 osf/v44/scripts/score_v0_44.py --parity-p1 | tail -3; python3 osf/v44/scripts/acquire_v0_44.py > /tmp/v044_dry.txt 2>&1; diff /tmp/v044_dry.txt osf/v44/prereg/dry_run_v0_44.txt && echo DRY_SAME
cd /Users/pablou/aias/_worktrees/v0.44 && python3 osf/v44/scripts/lock_manifest_v0_44.py && shasum -a 256 -c osf/v44/LOCK_MANIFEST_v0_44.sha256 | grep -vc ": OK$"; wc -l < osf/v44/LOCK_MANIFEST_v0_44.sha256
```
Expect `RESULT OK 68 failures 0 errors 0`, `DRY_SAME`, `0` failures, `43` lines (eight-industry run: since C11 the `diff` against `LOCK_MANIFEST_v0_44_DRAFT.sha256` shows exactly the six files C11 changed). Spot value: prereg `caa072aedfe9b8523a1586a1a1b73825d1e43a6cc892e57aa682a96ac7b3737b` and probe file `107d9401c18d9ee00ee4d5d717642aaeac7eb812ce843ff559947fe8525c2bb6` (these change only in the pharmacies variant).

## 3. Commit (local), then tag (local)

```
cd /Users/pablou/aias/_worktrees/v0.44 && git add osf/v44/LOCK_MANIFEST_v0_44.sha256 osf/v44/LOCK_STEPS.md osf/v44/lock && git status --short --untracked-files=no
```
(In the pharmacies variant also `git add` the changed registry, probe, cost, dry-run, prereg and DEVIATIONS files.) Commit with the session's attribution lines, then:
```
cd /Users/pablou/aias/_worktrees/v0.44 && git tag -a v0.44-prereg-r1 -m "AIAS v0.44 industry-breadth wave: pre-registration r1 locked (LOCK_MANIFEST_v0_44.sha256, 43 files)" HEAD && git rev-parse v0.44-prereg-r1 v0.44-prereg-r1^{commit}
```

## 4. Push branch and tag (this is the first push of the lock)

```
cd /Users/pablou/aias/_worktrees/v0.44 && git push origin v0.44 && git push origin refs/tags/v0.44-prereg-r1 && git ls-remote --tags origin v0.44-prereg-r1
```
Expect two lines (tag object and `^{}` = the commit of step 3).

## 5. Anchor file

```
cd /Users/pablou/aias/_worktrees/v0.44 && python3 osf/v44/lock/write_anchor_v0_44.py            # add --pharmacies-dropped in the variant
```
Writes `osf/v44/anchor/osf_anchor_v0_44.json` (tag object, commit, tree, the 43 files with SHA-256 and blob at the tag, OSF paths). It refuses if the tag is not on origin or any file differs from the manifest in the tree or at the tag. Commit and push the anchor (the tag does not move):
```
cd /Users/pablou/aias/_worktrees/v0.44 && git add osf/v44/anchor/osf_anchor_v0_44.json && git commit -m "v0.44 anchor: osf_anchor_v0_44.json names v0.44-prereg-r1 (after the lock)" && git push origin v0.44
```
(Add the attribution lines to the commit message.)

## 6. OSF deposit (project ec6wh; `OSF_TOKEN` is set in the login shell)

`v44/prereg/draft_r1/` already holds the draft of Nov 10: leave it. Prereg §9 deposits prereg, registries, scripts, DEVIATIONS.md and the manifest. Stage the two loose files with the anchor (untracked temp dir, outside the repo):
```
rm -rf /tmp/v044_anchor_stage && mkdir /tmp/v044_anchor_stage && cd /Users/pablou/aias/_worktrees/v0.44 && cp osf/v44/anchor/osf_anchor_v0_44.json osf/v44/LOCK_MANIFEST_v0_44.sha256 osf/v44/DEVIATIONS.md /tmp/v044_anchor_stage/ && ls /tmp/v044_anchor_stage
```
Dry run first, then upload:
```
cd /Users/pablou/aias/_worktrees/v0.44 && for p in "osf/v44/prereg v44/prereg" "osf/v44/registries v44/registries" "osf/v44/scripts v44/scripts" "/tmp/v044_anchor_stage v44/anchor"; do python3 scripts/osf_upload.py ${=p} --dry-run | tail -3; done
cd /Users/pablou/aias/_worktrees/v0.44 && python3 scripts/osf_upload.py osf/v44/prereg v44/prereg && python3 scripts/osf_upload.py osf/v44/registries v44/registries
cd /Users/pablou/aias/_worktrees/v0.44 && python3 scripts/osf_upload.py osf/v44/scripts v44/scripts && python3 scripts/osf_upload.py /tmp/v044_anchor_stage v44/anchor
```
Do not upload `_osf_stage_draft`, `data`, or `lock/`.

## 7. Verify the deposit by SHA-256 (read-only)

```
cd /Users/pablou/aias/_worktrees/v0.44 && for p in "osf/v44/prereg v44/prereg" "osf/v44/registries v44/registries" "osf/v44/scripts v44/scripts" "/tmp/v044_anchor_stage v44/anchor"; do python3 osf/v44/lock/osf_verify_v0_44.py ${=p} | tail -4; done
```
Expect every local file `OK`. `v44/prereg` will also print `EXTRA on OSF only: draft_r1/...` lines (the Nov 10 draft): those, and only those, are expected, and make that folder's final line read FAIL; check by eye that no `BAD` line appears and every EXTRA starts with `draft_r1/`. On a mismatch re-upload that folder and verify again; never edit a locked file to make it match.

## 8. Collection (Nov 24-28; NOT part of the lock)

Do not collect before 2026-11-24 00:00 US Central; never 2026-11-17 to 11-21 (v0.40's collection; the machine is booked 11-11 to 11-23). Only one paid collection at a time: before starting, `pgrep -fl "acquire_v.*--collect"` must be empty. Gemini 4 Argon is at November prices until Nov 30; the window is inside them (planning $27.24 central / $52.44 high; $24.06 / $46.36 without pharmacies; $80 pause, $100 hard stop). The script itself refuses unless the anchor exists, the tag is on origin and names the commit, the date is in the window, and no other paid collection runs. All calls must fall within 72 hours of the first.
```
cd /Users/pablou/aias/_worktrees/v0.44 && git fetch origin && git status -sb | head -2 && date && python3 osf/v44/scripts/acquire_v0_44.py | tail -12     # dry run, sends nothing
cd /Users/pablou/aias/_worktrees/v0.44 && mkdir -p osf/v44/data && nohup caffeinate -i python3 osf/v44/scripts/acquire_v0_44.py --collect > osf/v44/data/collect_v0_44.log 2>&1 &
```
Resume or re-run pass: the same `--collect` command (calls with an answer are skipped). Approvals only on Pablo's word: `--approve-past-80 "<who, when>"`, `--approve-projection "<who, when>"`, `--drop-run-3 "<who, when>"`. Then code and score per prereg §4.7 (`code_v0_44.py`, then `score_v0_44.py --run`, once).

## 9. After the lock

Report: tag object, commit, anchor commit, the four OSF verifications. Do not collect. Do not push or tag anything else.
