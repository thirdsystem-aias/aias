# v0.45 (t5) — lock, J1 and collection steps

Prepared 2026-11-11 (~9 am CT) by the runner with pre-registration r1. Templates: `osf/v44/LOCK_STEPS.md` (v0.44 @ c627f1b) and `osf/v42/LOCK_STEPS.md` (v0.42 @ 58d1891). Everything runs in the worktree `/Users/pablou/aias/_worktrees/v0.45` (branch `v0.45`). Never checkout, switch or commit in `/Users/pablou/aias` itself (another job). Each shell call is `zsh -ic '...'` (≤ 55 s; longer jobs with `nohup … &` and read back from their log); set `export PYTHONDONTWRITEBYTECODE=1`. Never print a key.

**Order:** r1 to Pablo (control panel) → lock no earlier than 24 hours after he received it (steps 0–7) → J1 judge parity (step 8, paid, < $1) → availability record on Wed Dec 2 (step 9) → collection from Thu Dec 3, 00:00 CT (step 10) → acquisition tag (step 12) → coding and scoring (step 13). One paid collection at a time on the Mac.

**State prepared on 2026-11-11 (r1 commits on branch `v0.45`, local only):** t4's locked code merged (tag `v0.42-prereg-r1` = `58d1891`; v0.42 C27/C28) and `acquire_v0_45.py` re-forked from it; `prereg/LOCK_MANIFEST_v0_45.sha256` built (`shasum -a 256 -c` 0 failures); 68 tests pass; the dry run equals `prereg/dry_run_v0_45.txt` (876 calls); `prereg/cost_estimate_v0_45_r1.txt` reproduces t4's recorded $67.4551 and gives t5 $72.90 central / $152.05 high with the $2.50 reserve; no tag, no push, no OSF upload. Lock helpers (not locked files): `lock/write_anchor_v0_45.py`, `lock/osf_verify_v0_45.py`. If any manifested file changes before the tag, rebuild the manifest (1b) and redo 1a–1e.

## 0. Preconditions (stop and report if any fails)

1. **Time:** now ≥ 24 hours after Pablo received r1 (the panel item's time). `date; date -u`
2. **Pablo:** no "hold v0.45" in the panel and no requested change. A change to §2 (hypotheses, thresholds, tests, seeds), the panel, the probes or a decision rule restarts the 24 hours: do not lock; report. His answers to the "Plan update suggested" items (§5.1 J1, §11) are recorded in §9 before the tag (a clarification; rebuild the manifest).
3. **Worktree clean, on v0.45, no t5 data:**
   ```
   cd /Users/pablou/aias/_worktrees/v0.45 && git branch --show-current && git status --short --untracked-files=no && git log --oneline -3 && ls osf/v45/data 2>&1
   ```
   Expect `v0.45`, no tracked changes, HEAD = the r1 commit (or a later lock commit), and no `osf/v45/data`.
4. **Remote refs (read-only):**
   ```
   cd /Users/pablou/aias/_worktrees/v0.45 && git ls-remote origin "refs/tags/v0.45*" "refs/heads/v0.45" && echo --- && git ls-remote origin "refs/tags/v0.42-prereg-r1*" "refs/tags/v0.42-acquisition-locked*"
   ```
   Expect nothing before `---` (no v0.45 tag or branch on origin yet), then four lines: `v0.42-prereg-r1^{}` = `58d1891bf2fa65b2a0f2f1e2adfcffc93fd56e0f`, `v0.42-acquisition-locked^{}` = `a790bb1ac552adfc6615b0bcb49430aa95e7bc16`. (Query with `refs/tags/<tag>*`: git 2.54 omits the `^{}` line for a bare tag name.)
5. **No paid collection running:** `pgrep -fl "acquire_v[0-9][0-9_.]*\.py.*--collect" || echo none` → `none`.
6. **Keys (names only):** `zsh -ic 'for v in ANTHROPIC_API_KEY OPENAI_API_KEY GOOGLE_API_KEY OSF_TOKEN; do [[ -n ${(P)v} ]] && echo "$v set" || echo "$v MISSING"; done'` → four `set`.
7. **Vendor pages (prereg §4.3, §4.5):** re-read the Anthropic pricing and model-deprecations pages, the OpenAI pricing, gpt-6-astra and deprecations pages, and the Vertex AI pricing page and Gemini API changelog/deprecations. If a t4 model shows a retirement before Dec 7, or a price differs from `budget_v0_45.py`: stop and report (prices: a §4.5 clarification before the lock; retirement: the replacement rule, §4.3). A newer flagship is only reported.

## 1. Verify the lock text (no writes)

a. Manifest:
   ```
   cd /Users/pablou/aias/_worktrees/v0.45 && M=osf/v45/prereg/LOCK_MANIFEST_v0_45.sha256 && shasum -a 256 -c $M | grep -vc ": OK$"; wc -l < $M; python3 osf/v45/scripts/lock_manifest_v0_45.py --check; cut -c1-8,65- $M | grep -E "PRE_REG|probes_v0_45|acquire_v0_45|code_t4|cost_estimate_v0_45_r1.txt"
   ```
   Expect `0` failures, the line count and spot values written at the end of this file ("Manifest at r1"), and `manifest up to date`.
b. (Only if a manifested file changed) rebuild, commit, then redo a.–e.:
   ```
   cd /Users/pablou/aias/_worktrees/v0.45 && python3 osf/v45/scripts/lock_manifest_v0_45.py
   ```
c. Tests (68; ~10 s):
   ```
   cd /Users/pablou/aias/_worktrees/v0.45 && PYTHONDONTWRITEBYTECODE=1 python3 osf/v45/scripts/tests/run_all_v0_45.py 2>&1 | tail -2
   ```
   Expect `RESULT OK 68`.
d. Dry run equals the record, and the fork reproduces the script:
   ```
   cd /Users/pablou/aias/_worktrees/v0.45 && diff <(PYTHONDONTWRITEBYTECODE=1 python3 osf/v45/scripts/acquire_v0_45.py --dry-run) osf/v45/prereg/dry_run_v0_45.txt && echo DRYRUN_SAME && PYTHONDONTWRITEBYTECODE=1 python3 osf/v45/scripts/_fork_v0_45.py && git status --short --untracked-files=no
   ```
   Expect `DRYRUN_SAME` (876 calls; the dry run prints r0's v0.39-basis figure, $67.27 / $142.60, kept for the record; §4.5 uses r1's) and no tracked change after regeneration.
e. The r1 re-estimate reproduces from t4's locked raw file (usage fields only):
   ```
   cd /Users/pablou/aias/_worktrees/v0.45 && PYTHONDONTWRITEBYTECODE=1 python3 osf/v45/scripts/reestimate_t4_v0_45.py | diff - osf/v45/prereg/cost_estimate_v0_45_r1.txt && echo REESTIMATE_SAME
   ```

## 2. Lock commit (only if 0.2 required a §9 line, or to record the lock time ex ante as v0.42/v0.44 did)

Edit §9 of the prereg (one dated line), rebuild the manifest (1b), redo 1a and 1c, commit with the session's attribution lines.

## 3. Tag (local)

```
cd /Users/pablou/aias/_worktrees/v0.45 && git tag -a v0.45-prereg-r1 -m "AIAS v0.45 (t5): pre-registration r1 locked (prereg/LOCK_MANIFEST_v0_45.sha256)" HEAD && git rev-parse v0.45-prereg-r1 v0.45-prereg-r1^{commit}
```
Record the tag object and the commit.

## 4. Push branch and tag (the first push of v0.45)

```
cd /Users/pablou/aias/_worktrees/v0.45 && git push -u origin v0.45 && git push origin refs/tags/v0.45-prereg-r1 && git ls-remote origin "refs/tags/v0.45-prereg-r1*"
```
Expect two lines (tag object; `^{}` = the commit of step 3).

## 5. Anchor file (`acquire_v0_45.py --collect` and `code_t5_v0_45.py --parity` refuse without the tag; collect also without this file)

```
cd /Users/pablou/aias/_worktrees/v0.45 && PYTHONDONTWRITEBYTECODE=1 python3 osf/v45/lock/write_anchor_v0_45.py --dry-run | head -14
cd /Users/pablou/aias/_worktrees/v0.45 && PYTHONDONTWRITEBYTECODE=1 python3 osf/v45/lock/write_anchor_v0_45.py
```
Writes `osf/v45/anchor/osf_anchor_v0_45.json`: tag, tag object, commit, tree, tagger date, remote refs, every locked file plus the manifest (SHA-256 on disk and at the tag, git blob), the coder pin `2d36735d…`, the fork source `58d1891…`, t4's J1 inputs (raw file at `v0.42-acquisition-locked`, SHA-256 `f3109091…`; `v23_phase_a.csv` at `c84f6fa`, SHA-256 `52a1c9d7…`), and that no t5 raw file exists. It refuses on any mismatch. Commit and push the anchor (the tag does not move):
```
cd /Users/pablou/aias/_worktrees/v0.45 && git add osf/v45/anchor/osf_anchor_v0_45.json && git commit -m "v0.45 anchor: osf_anchor_v0_45.json names v0.45-prereg-r1 (after the lock)" && git push origin v0.45
```
(Add the session's attribution lines to the commit message.)

## 6. OSF deposit (project ec6wh, osfstorage; `OSF_TOKEN` in the login shell)

Prereg §9: `osf/v45/prereg/` (incl. the manifest) → `v45/prereg/`; `osf/v45/scripts/` → `v45/prereg/scripts/` (as v0.42); `osf/v45/anchor/` (DEVIATIONS.md, osf_anchor_v0_45.json) → `v45/anchor/`. Not deposited: `osf/v45/lock/`, LOCK_STEPS.md, `__pycache__` (the uploader skips it). Check, dry run, upload:
```
cd /Users/pablou/aias/_worktrees/v0.45 && git status --short osf/v45 && ls osf/v45/prereg | wc -l && git ls-files osf/v45/scripts | wc -l && ls osf/v45/anchor
cd /Users/pablou/aias/_worktrees/v0.45 && python3 scripts/osf_upload.py osf/v45/prereg v45/prereg --dry-run && python3 scripts/osf_upload.py osf/v45/scripts v45/prereg/scripts --dry-run && python3 scripts/osf_upload.py osf/v45/anchor v45/anchor --dry-run
cd /Users/pablou/aias/_worktrees/v0.45 && python3 scripts/osf_upload.py osf/v45/prereg v45/prereg
cd /Users/pablou/aias/_worktrees/v0.45 && python3 scripts/osf_upload.py osf/v45/scripts v45/prereg/scripts
cd /Users/pablou/aias/_worktrees/v0.45 && python3 scripts/osf_upload.py osf/v45/anchor v45/anchor
```
Expect no `git status` output; the counts written at the end of this file ("Manifest at r1").

## 7. Verify the deposit by SHA-256 (read-only)

```
cd /Users/pablou/aias/_worktrees/v0.45 && PYTHONDONTWRITEBYTECODE=1 python3 osf/v45/lock/osf_verify_v0_45.py osf/v45/prereg v45/prereg --ignore scripts/ | tail -2
cd /Users/pablou/aias/_worktrees/v0.45 && PYTHONDONTWRITEBYTECODE=1 python3 osf/v45/lock/osf_verify_v0_45.py osf/v45/scripts v45/prereg/scripts | tail -1
cd /Users/pablou/aias/_worktrees/v0.45 && PYTHONDONTWRITEBYTECODE=1 python3 osf/v45/lock/osf_verify_v0_45.py osf/v45/anchor v45/anchor | tail -1
```
Expect three `PASS` lines. On a mismatch re-upload that folder and verify again; never edit a locked file to make it match. **The lock is complete here**: report tag object, commit, anchor commit and the three verifications.

## 8. J1 — successor judge parity (paid, < $1; after step 7; prereg §5.1)

Preconditions: step 7 passed; no paid collection running (0.5); `ANTHROPIC_API_KEY` is the program's current organization (`c1080353-9fa2-4ead-b596-e062dde7c70a`), which serves `claude-sonnet-5-5` and `claude-sonnet-4-6` (free models list, 2026-11-11 08:38 CT; it no longer serves `claude-sonnet-4-5`, which is not needed: its labels are already recorded). Run J1 before Dec 3 so that its result is known before the collection.

a. Extract t4's inputs at their commits and check them:
   ```
   rm -rf /tmp/v45_j1 && mkdir -p /tmp/v45_j1/coded && cd /Users/pablou/aias/_worktrees/v0.45 && git show v0.42-acquisition-locked:osf/v42/data/t4_raw.jsonl > /tmp/v45_j1/t4_raw.jsonl && for f in v19 v20 v21 v22 v23; do for p in a b; do git show c84f6fa:osf/v42/data/coded/${f}_phase_${p}.csv > /tmp/v45_j1/coded/${f}_phase_${p}.csv; done; done && shasum -a 256 /tmp/v45_j1/t4_raw.jsonl /tmp/v45_j1/coded/v23_phase_a.csv
   ```
   Expect `f3109091f51af7899098d83a1d7b2080a26a06824caa5f6fc0486f3d6196d4bf` and `52a1c9d7a32ab1bd176eb39af68559a3336ec0442bd2ba52a5ef4a464802358e`.
b. First candidate (216 requests: 144 t3 + 72 t4 v0.23 Phase A answers):
   ```
   cd /Users/pablou/aias/_worktrees/v0.45 && (PYTHONDONTWRITEBYTECODE=1 nohup python3 -u osf/v45/scripts/code_t5_v0_45.py --parity claude-sonnet-5-5 --t4-raw /tmp/v45_j1/t4_raw.jsonl --t4-coded /tmp/v45_j1/coded > /tmp/v45_j1.log 2>&1 &); sleep 50; tail -3 /tmp/v45_j1.log
   ```
   Read the log until the `J1 claude-sonnet-5-5: PASS|FAIL …` line. PASS = binary agreement with Sonnet 4.5 ≥ 0.95 over all answers judged (≥ 206 of 216) AND ≥ 0.90 on t4 (≥ 65 of 72), no R_ERR. The record is `osf/v45/data/judge_parity_J1_v0_45.json` (every run with its usage and cost; the winner's t4 codes).
c. **Void run** (prereg §5.1): if every request returned R_ERR (no label at all: a request-settings error such as HTTP 400, or thinking that used the 10-token budget), the run is void, not a FAIL. Stop and report; do not correct anything yourself. A correction of the request settings (prompt, template, truncation, rubric, parser and thresholds unchanged) needs a DEVIATIONS entry first; then re-run b. once; that run is final.
d. FAIL (any other run without a PASS): run b. with `--parity claude-sonnet-4-6`. If it also fails: v0.23 recognition is not coded at t5 and P is not computed for the 24 v0.23 units at either wave (prereg §5.1); tell Pablo.
e. Record it before any t5 answer is coded: a DEVIATIONS entry (ex ante; "pre-registered contingency used: successor judge = <model>, J1 <numbers>, cost $<x>"), then commit `osf/v45/data/judge_parity_J1_v0_45.json` and DEVIATIONS, and push.

## 9. Availability record (Wed Dec 2; prereg §4.3, MC_Available; `--collect` refuses without it)

Re-read the three vendors' model and deprecation pages (as 0.7) and write `osf/v45/data/t5_availability_v0_45.json`: `{"read_by": "...", "models": {"claude-fable-5-2": {"available": true, "page": "<url>", "read_utc": "<time>", "status_quoted": "<quote>"}, "gpt-6-astra": {...}, "gemini-4-argon": {...}}}`. A model retired, shut down or redirected by Dec 3: `"available": false`, then the replacement rule of §4.3 (DEVIATIONS entry ex ante, manifest refreshed and re-deposited, Pablo told before the first call). Commit the record.

## 10. Collection (paid; from Thu 2026-12-03 06:00 UTC = 00:00 CT; under caffeinate; one paid collection at a time)

Launch in the background, unbuffered, and keep the Mac awake with `caffeinate -w PID` (a separate process whose command line does not contain the collection command):
```
cd /Users/pablou/aias/_worktrees/v0.45 && mkdir -p osf/v45/data && (nohup python3 -u osf/v45/scripts/acquire_v0_45.py --collect >> osf/v45/data/collect_v0_45.log 2>&1 & echo $! > /tmp/v45_collect.pid) && P=$(cat /tmp/v45_collect.pid) && (nohup caffeinate -dimsu -w $P > /dev/null 2>&1 &) ; sleep 30; ps -p $P -o pid=,etime=,command=; pgrep -fl caffeinate; tail -6 osf/v45/data/collect_v0_45.log
```
Expect `prereg guard passed: v0.45-prereg-r1 -> <commit>`, the window line, `876 specs, 0 already done; budget {… 'spent_usd': 2.5 …}` (the $2.50 judge reserve), then `block 1 ('B', 'S0', 1): 90 calls to send`. The script refuses before the window, without the availability record, the anchor or the tag on origin, and while another paid collection runs. Watch with `PYTHONDONTWRITEBYTECODE=1 python3 osf/v45/lock/status_v0_45.py` (read-only; `--batch-status` adds Anthropic's metadata for open batches, not billed). The first Fable batch must show 30 lines `ok`, served `claude-fable-5-2`, sensible tokens and about $0.026 per answer (t4: $0.77 for block 1).

**Where the guard should act (prereg §4.5, r1):** central, no pause ($72.90 at the end); the $80 pause is reached only if t5 costs about 10% more than t4's usage at t5 prices; the projection pause after block 5 triggers only if block 5 costs more than about $27.10 (t4 at t5 prices: $17.44).
**Pauses and stops** (the runner never approves on its own): exit 5 (`>= $80` or `PAUSE (projection)`): send Pablo the status (spend, calls answered, what remains); only on his explicit OK relaunch the step-10 command with `--approve-past-80 "Pablo, <date time CT>, <channel>"` (or `--approve-projection "…"`) after `--collect`. Exit 6 (`$100` or window): the collection is over; unsent calls are missing cells (§5.4). Interrupted: relaunch the step-10 command (it records batches left in flight first, never re-sends an answered call, keeps the 72-hour window).

## 11. Re-run pass (once, logged, inside the window)

When the main pass exited 0 and fewer than 876 calls are answered:
```
cd /Users/pablou/aias/_worktrees/v0.45 && echo "=== re-run pass $(date -u +%FT%TZ) ===" >> osf/v45/data/collect_v0_45.log && <the step-10 command>
```

## 12. Acquisition lock: tag `v0.45-acquisition-locked` (v1.14 Stage 2 needs it)

After the last call (no collection process, no open batch, `status_v0_45.py` read and its numbers reported):
```
cd /Users/pablou/aias/_worktrees/v0.45 && git add osf/v45/data/t5_raw.jsonl osf/v45/data/t5_batches.jsonl osf/v45/data/collect_v0_45.log osf/v45/data/t5_availability_v0_45.json && (test -f osf/v45/data/t5_budget_state.json && git add osf/v45/data/t5_budget_state.json || true) && git commit -m "v0.45 t5 acquisition: <answered>/876 calls answered, <lines> raw lines, recorded spend \$<x> (t5_raw.jsonl sha256 <first 12>)" && git tag -a v0.45-acquisition-locked -m "AIAS v0.45 t5 raw answers locked (t5_raw.jsonl sha256 <full>)" HEAD && git push origin v0.45 && git push origin refs/tags/v0.45-acquisition-locked && git ls-remote origin "refs/tags/v0.45-acquisition-locked*"
```
From here on `osf/v45/data/t5_raw.jsonl` is never written again.

## 13. Coding and scoring (prereg §5.1–§5.3)

1. Coding with the J1 winner (refuses unless it passed J1): `cd /Users/pablou/aias/_worktrees/v0.45 && (PYTHONDONTWRITEBYTECODE=1 nohup python3 -u osf/v45/scripts/code_t5_v0_45.py --code osf/v45/data/t5_raw.jsonl osf/v45/data/coded --judge <winner> > osf/v45/data/code_v0_45.log 2>&1 &)`. Without a J1 winner, omit `--judge` (v0.23 recognition not coded). Commit the coded tables and the log.
2. Scoring once, after v0.42's scoring tag (`v0.42-scoring-locked`) exists: `score_v0_45.py --run --t4-dir <dir with t4_raw.jsonl from v0.42-acquisition-locked and coded/ from v0.42's scored commit> --t4-brand-table <v42_brand_table.csv> --j1 osf/v45/data/judge_parity_J1_v0_45.json [--ranking-stage2 …] [--component …]` (it refuses unless both v0.45 tags are on origin, and if it has scored once already); gates G1–G3 come first. Commit, tag `v0.45-scoring-locked`, push.

## Manifest at r1 (2026-11-11)

`prereg/LOCK_MANIFEST_v0_45.sha256`: **34 lines** (23 v0.45 files: DEVIATIONS.md, 9 prereg files, 8 scripts, 5 tests; and 11 files of earlier phases), manifest file SHA-256 `07dcfcf1c8f76aa7…`. Spot values (first 8 hex): prereg `cb2b9ec9`, probe file `7aa246ee` (= t₄'s), `acquire_v0_45.py` `5e0768b4`, `budget_v0_45.py` `b4524b3c`, `code_t5_v0_45.py` `4c54fc89`, `cost_estimate_v0_45_r1.txt` `9b5f4139`, `code_t4_v0_42.py` `d0e4e685` (git blob `2d36735d…`), `score_v0_42.py` `21ce0c35`, `acquire_v0_42.py` `50e52359` (= v0.42's locked manifest). OSF counts for step 6: `osf/v45/prereg` 10 files (incl. the manifest), `osf/v45/scripts` 13 tracked files, `osf/v45/anchor` 2 files after step 5 (DEVIATIONS.md, osf_anchor_v0_45.json). If the prereg changes before the tag (e.g. a §9 line from 0.2), these values change: rebuild (1b) and use the new ones.
