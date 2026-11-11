# v0.42 (t4) — lock and collection steps (Wednesday 2026-11-11 onward)

Prepared 2026-11-10 (~3:15 pm CT) by the runner (lane 11). Everything below runs in the worktree `/Users/pablou/aias/_worktrees/v0.42` (branch `v0.42`). Never checkout, switch or commit in `/Users/pablou/aias` itself (branch `v0.40`, another job). Each shell call is `zsh -ic '...'` (≤ 55 s); anything longer is started with `nohup ... &` and read back from its log. This file replaces the stale "Tue Nov 10, from 11:30 pm CT" time in STATUS.md.

**Wednesday order:** v1.12 lock → v1.13 Part I lock → **v0.42 lock (steps 0–6, no earlier than 2026-11-11 21:00 UTC = 3 pm CST)** → v0.42 collection (step 7). One paid collection at a time on the Mac.

**State prepared on 2026-11-10** (lane-11 commit "v0.42 lock prep"): clarification C26 logged (§9; collection guards; no hypothesis, threshold, panel, probe, design, budget rule or decision rule changed); `acquire_v0_42.py` regenerated with the guards; `prereg/LOCK_MANIFEST_v0_42.sha256` built (24 files, paths from the repository root; `shasum -a 256 -c` 0 failures); 84 tests pass (C27, Nov 11: 78 + 2; C28: + 4); the dry run equals `prereg/dry_run_v0_42.txt` (876 calls); the rehearsal on local fakes passes 28 of 28 checks (step R). Lock helpers (not locked files): `lock/write_anchor_v0_42.py`, `lock/osf_verify_v0_42.py`, `lock/status_v0_42.py`, `lock/write_t4_complete_v0_42.py`, `lock/fake_collect_e2e_v0_42.py` with `lock/fakes/`. If any manifested file changes before the tag, rebuild the manifest (1b) and re-run 1a–1d.

## 0. Preconditions (stop if any fails)

1. **Time:** now ≥ **2026-11-11 21:00 UTC**. `date -u`
   Clarification (Nov 11, 2026, ex ante, before the tag; lock steps only): Lock time: the pre-registrant waived the 24-hour review on 2026-11-10 at 20:26 CT (control panel, 'LOCK NOW'); locked at 2026-11-11 02:53 UTC (tag `v0.42-prereg-r1` on the commit that adds this line). The locked files (manifest, 24 files) are unchanged by this line.
2. **Pablo:** no "hold t4" in the panel and no requested change since the r2 + C25 text of Nov 10 (~3 pm CT). A change to a hypothesis, threshold, panel, probe or decision rule restarts the 24 hours: do not lock; report.
3. **v1.12 and v1.13 locks are done** (or explicitly skipped for today); none of their collections is running.
4. **Worktree clean, on v0.42, no t4 data:**
   ```
   cd /Users/pablou/aias/_worktrees/v0.42 && git branch --show-current && git status --short --untracked-files=no && git log --oneline -2 && ls osf/v42/data osf/v42/anchor 2>&1
   ```
   Expect `v0.42`, no tracked changes, HEAD = the lane-11 "v0.42 lock prep" commit (or a later lock commit), `osf/v42/data` empty and no `osf/v42/anchor`. `osf/v42/_osf_stage_draft*/` are untracked staging copies of the drafts: leave them, never upload them.
5. **Remote tags (read-only):**
   ```
   cd /Users/pablou/aias/_worktrees/v0.42 && git ls-remote --tags origin v0.42-prereg-r1 v0.42-acquisition-locked v1.14-prereg-r2
   ```
   Expect no `v0.42-*` tag; `v1.14-prereg-r2` present with peeled commit `a5feb4b1c4b9e9d19979129afcfd616a50b88c64`. If it is absent: stop (v1.14's `osf/methodology/v1_14/LOCK_STEPS_r2.md` must be completed before any t4 answer exists).
   Clarification (Nov 10, 2026, evening, ex ante; lock steps only): v1.14 re-locked as r2 before any t4 answer: crash fix only; no statistic changed (v1.14 DEVIATIONS Entry 1). `v1.14-prereg-r1` (→ `20fbc342`) stays on origin as the record of r1; v1.14's Stage 1 now requires `v1.14-prereg-r2`. Nothing in v0.42's pre-registration or scripts names a v1.14 tag.
6. **No paid collection running:** `pgrep -fl "acquire_v[0-9][0-9_.]*\.py.*--collect" || echo none` → `none`.
7. **Keys in the login shell (names only):** `zsh -ic 'for v in ANTHROPIC_API_KEY OPENAI_API_KEY GOOGLE_API_KEY OSF_TOKEN; do [[ -n ${(P)v} ]] && echo "$v set" || echo "$v MISSING"; done'` → four `set` (checked Nov 10: all set; `GEMINI_API_KEY` is not needed when `GOOGLE_API_KEY` is set).

## 1. Verify the lock text (no writes)

a. Manifest:
   ```
   cd /Users/pablou/aias/_worktrees/v0.42 && shasum -a 256 -c osf/v42/prereg/LOCK_MANIFEST_v0_42.sha256 | grep -vc ": OK$"; wc -l < osf/v42/prereg/LOCK_MANIFEST_v0_42.sha256; cut -c1-8,65- osf/v42/prereg/LOCK_MANIFEST_v0_42.sha256 | grep -E "PRE_REG|acquire_v0_42.py|code_t4|score_v0_42.py"
   ```
   Expect `0` failures, `24` lines; prereg `b82585ed`, `acquire_v0_42.py` `bedf4d50`, `code_t4_v0_42.py` `d0e4e685` (= the pin of v1.12/v1.13/v1.14; git blob `2d36735d`), `score_v0_42.py` `644b50ef` (= v1.13's pin).

b. (Only if a manifested file changed) rebuild, then redo a.:
   ```
   cd /Users/pablou/aias/_worktrees/v0.42 && M=osf/v42/prereg/LOCK_MANIFEST_v0_42.sha256 && shasum -a 256 $(sed "s/^[0-9a-f]*  //" $M) > /tmp/v42_m && mv /tmp/v42_m $M
   ```

c. Tests (84; ~51 s, so in the background):
   ```
   cd /Users/pablou/aias/_worktrees/v0.42 && (PYTHONDONTWRITEBYTECODE=1 nohup python3 osf/v42/scripts/tests/run_all_v0_42.py > /tmp/v42_tests.log 2>&1 &); sleep 54; tail -1 /tmp/v42_tests.log
   ```
   Expect `RESULT OK 84` (if not yet there, `sleep 10; tail -1 /tmp/v42_tests.log`).

d. Dry run equals the record, and the generator reproduces the script:
   ```
   cd /Users/pablou/aias/_worktrees/v0.42 && diff <(PYTHONDONTWRITEBYTECODE=1 python3 osf/v42/scripts/acquire_v0_42.py --dry-run) osf/v42/prereg/dry_run_v0_42.txt && echo DRYRUN_SAME && python3 osf/v42/scripts/_assemble_acquire_v0_42.py && git status --short --untracked-files=no
   ```
   Expect `DRYRUN_SAME` (876 calls, `OK`; central $63.97) and no tracked change after regeneration.

## 2. Tag (local)

```
cd /Users/pablou/aias/_worktrees/v0.42 && git tag -a v0.42-prereg-r1 -m "AIAS v0.42 (t4): pre-registration r2 + clarifications C25, C26 locked (prereg/LOCK_MANIFEST_v0_42.sha256, 24 files)" HEAD && git rev-parse v0.42-prereg-r1 v0.42-prereg-r1^{commit}
```
Record the tag object and the commit.

## 3. Push branch and tag

```
cd /Users/pablou/aias/_worktrees/v0.42 && git push origin v0.42 && git push origin refs/tags/v0.42-prereg-r1 && git ls-remote --tags origin v0.42-prereg-r1
```
Expect two lines (tag object; `^{}` = the commit of step 2).

## 4. Anchor file (`acquire_v0_42.py --collect` refuses without it)

Dry run first, then write:
```
cd /Users/pablou/aias/_worktrees/v0.42 && PYTHONDONTWRITEBYTECODE=1 python3 osf/v42/lock/write_anchor_v0_42.py --dry-run | head -12
cd /Users/pablou/aias/_worktrees/v0.42 && PYTHONDONTWRITEBYTECODE=1 python3 osf/v42/lock/write_anchor_v0_42.py
```
Writes `osf/v42/anchor/osf_anchor_v0_42.json`: tag, tag object, commit, tree, tagger date, remote ref, the 24 locked files plus the manifest (SHA-256 checked on disk and at the tag, git blob at the tag), the coder pin (`2d36735d…`), and that no t4 raw file exists. It refuses if the tag is not on origin or differs from the local tag, a file differs from the manifest on disk or at the tag, the coder blob is not the pin, or `osf/v42/data/t4_raw.jsonl` exists. (Rehearsed on a scratch repository with a local bare origin: step R.) Commit and push the anchor (the tag does not move):
```
cd /Users/pablou/aias/_worktrees/v0.42 && git add osf/v42/anchor/osf_anchor_v0_42.json && git commit -m "v0.42 anchor: osf_anchor_v0_42.json names v0.42-prereg-r1 (after the lock)" && git push origin v0.42
```
(Add the session's attribution lines to the commit message.)

## 5. OSF deposit (project ec6wh, osfstorage)

OSF `v42/prereg/` already holds `draft/` (r1) and `draft_r2/` (r2 draft): leave both. The header of the pre-registration names the scripts in the deposit, so they go to `v42/prereg/scripts/`. Check, dry run, upload:
```
cd /Users/pablou/aias/_worktrees/v0.42 && git status --short osf/v42/prereg osf/v42/scripts osf/v42/anchor && ls osf/v42/prereg | wc -l && git ls-files osf/v42/scripts | wc -l && ls osf/v42/anchor
cd /Users/pablou/aias/_worktrees/v0.42 && python3 scripts/osf_upload.py osf/v42/prereg v42/prereg --dry-run && python3 scripts/osf_upload.py osf/v42/scripts v42/prereg/scripts --dry-run && python3 scripts/osf_upload.py osf/v42/anchor v42/anchor --dry-run
cd /Users/pablou/aias/_worktrees/v0.42 && python3 scripts/osf_upload.py osf/v42/prereg v42/prereg
cd /Users/pablou/aias/_worktrees/v0.42 && python3 scripts/osf_upload.py osf/v42/scripts v42/prereg/scripts
cd /Users/pablou/aias/_worktrees/v0.42 && python3 scripts/osf_upload.py osf/v42/anchor v42/anchor
```
Expect no `git status` output; prereg = 11 files (10 + `LOCK_MANIFEST_v0_42.sha256`); scripts = 14 tracked files (plus `__pycache__`, which the uploader skips); anchor = `osf_anchor_v0_42.json`.

## 6. Verify the deposit by SHA-256 (read-only)

```
cd /Users/pablou/aias/_worktrees/v0.42 && PYTHONDONTWRITEBYTECODE=1 python3 osf/v42/lock/osf_verify_v0_42.py osf/v42/prereg v42/prereg --ignore draft/ --ignore draft_r2/ --ignore scripts/ | tail -2
cd /Users/pablou/aias/_worktrees/v0.42 && PYTHONDONTWRITEBYTECODE=1 python3 osf/v42/lock/osf_verify_v0_42.py osf/v42/scripts v42/prereg/scripts | tail -1
cd /Users/pablou/aias/_worktrees/v0.42 && PYTHONDONTWRITEBYTECODE=1 python3 osf/v42/lock/osf_verify_v0_42.py osf/v42/anchor v42/anchor | tail -1
```
Expect `11 of 11 local files match; 0 extra on OSF -> PASS`, `14 of 14 … PASS`, `1 of 1 … PASS`. (`--list v42` shows the folder read-only; on Nov 10 it held only `prereg/draft/` (4 files) and `prereg/draft_r2/` (10 files).) On a mismatch: re-upload that folder and verify again; never edit a locked file to make it match. The lock is complete here; report tag object, commit, anchor commit and the three verifications.

## 7. Collection (paid; under caffeinate; one paid collection at a time)

Launch in the background, unbuffered, and keep the Mac awake with `caffeinate -w PID` (a separate process whose command line does not contain the collection command):
```
cd /Users/pablou/aias/_worktrees/v0.42 && mkdir -p osf/v42/data && (nohup python3 -u osf/v42/scripts/acquire_v0_42.py --collect >> osf/v42/data/collect_v0_42.log 2>&1 & echo $! > /tmp/v42_collect.pid) && P=$(cat /tmp/v42_collect.pid) && (nohup caffeinate -dimsu -w $P > /dev/null 2>&1 &) ; sleep 30; ps -p $P -o pid=,etime=,command=; pgrep -fl caffeinate; tail -6 osf/v42/data/collect_v0_42.log
```
Expect in the log: `prereg guard passed: v0.42-prereg-r1 -> <commit>; no other paid collection running`, `collection window: no new request after <now + 72 h>`, `876 specs, 0 already done; budget {… 'spent_usd': 0.5 …}` (the $0.50 is the reserve for the v0.23 judge), then `block 1 ('B', 'S0', 1): 90 calls to send`. What the script enforces (rehearsed on fakes, step R): anchor + tag on origin; no other `acquire_v*.py --collect` on the Mac (its own shell, ancestors and descendants excluded); Claude Fable 5.2 via Message Batches (one batch per block: 30, 30, 30, 112, 30, 30, 30), GPT-6 Astra and Gemini 4 Argon synchronously, one worker per model (3 in parallel; STATUS.md's "4 workers" predates r2); every request's worst case reserved before it is sent; **no new request once recorded spend ≥ $80** (exit 5); **projection pause after block 5 (B-S1 run 1)** if spend + 2 × that block's cost > $100 (exit 5); **hard stop** before any request whose worst case would pass $100 (exit 6); **window**: no new request after the earlier of 72 h from the first call and 2026-11-16 23:59:59 UTC (exit 6); exit 0 when every block has been reached.

**Watch the first batch** (the Batches path was only tested on fakes). Every ~10 minutes until the first Fable batch is recorded (Anthropic: most batches end within an hour, at most 24 h):
```
cd /Users/pablou/aias/_worktrees/v0.42 && PYTHONDONTWRITEBYTECODE=1 python3 osf/v42/lock/status_v0_42.py
```
(`--batch-status` adds Anthropic's own status of the open batch: metadata only, not billed.) The first batch must show 30 lines, status `ok`, served `claude-fable-5-2` (or a dated snapshot), finish `end_turn`, sensible tokens and a cost per answer near `prereg/cost_estimate_v0_42_r2.txt`. If it shows errors (e.g. `invalid_request_error`), stop the run before more batches go out: `kill $(cat /tmp/v42_collect.pid)` (SIGTERM; an in-flight batch is journaled and recorded at the next start), and report; do not edit any locked file.

**Pauses and stops** (the runner never approves on its own):
- Exit 5 with `>= $80` in the log, or `PAUSE (projection)`: send Pablo the status (spend, calls answered, what remains). Only on his explicit OK, relaunch the step-7 command with `--approve-past-80 "Pablo, <date time CT>, <channel>"` (or `--approve-projection "…"`) added after `--collect`. The approval is stored in `osf/v42/data/t4_budget_state.json` with the spend at approval. A resumed run re-applies the projection rule only if no line of block 6 or 7 exists yet.
- Exit 6 (`$100` or `window`): the collection is over; unsent calls are missing cells (§5.4 drop rule). Go to step 9.
- Interrupted (crash, restart, kill): relaunch the step-7 command. It first fetches and records any batch left in flight (`recovering batch …`), never re-sends an answered call, and keeps the original 72-hour window. A synchronous request killed mid-call can be billed but unrecorded (at most one per synchronous model; none in the rehearsal).

## 8. Re-run pass (once, logged, inside the window)

When the main pass has exited 0 (every block reached), check `status_v0_42.py`: calls answered of 876, errors/empties per block × model, `MC_Served`. If fewer than 876 are answered and the window is open, run the re-run pass once:
```
cd /Users/pablou/aias/_worktrees/v0.42 && echo "=== re-run pass $(date -u +%FT%TZ) ===" >> osf/v42/data/collect_v0_42.log && <the step-7 command>
```
It sends only the unanswered calls (attempt lines are appended; nothing is overwritten). Calls answered by a served model other than the requested ID are not re-sent by the script; they are listed by `MC_Served` and excluded by the scorer (§2.6, C5): report their number.

## 9. Acquisition lock: tag `v0.42-acquisition-locked` (v1.14's Stage 1 refuses without it)

After t4's last call (main pass and re-run pass done, or the cap/window ended it). Preconditions: no collection process, no open batch, `status_v0_42.py` read and its numbers reported.
```
cd /Users/pablou/aias/_worktrees/v0.42 && pgrep -fl "acquire_v[0-9][0-9_.]*\.py.*--collect" || echo none; PYTHONDONTWRITEBYTECODE=1 python3 osf/v42/lock/status_v0_42.py | grep -E "processes|answered:|budget|open|MC_Served"; ls -la osf/v42/data; shasum -a 256 osf/v42/data/t4_raw.jsonl
cd /Users/pablou/aias/_worktrees/v0.42 && git add osf/v42/data/t4_raw.jsonl osf/v42/data/t4_batches.jsonl osf/v42/data/collect_v0_42.log && (test -f osf/v42/data/t4_budget_state.json && git add osf/v42/data/t4_budget_state.json || true) && git commit -m "v0.42 t4 acquisition: <answered>/876 calls answered, <lines> raw lines, recorded spend \$<x> (t4_raw.jsonl sha256 <first 12>)" && git tag -a v0.42-acquisition-locked -m "AIAS v0.42 t4 raw answers locked (t4_raw.jsonl sha256 <full>)" HEAD && git push origin v0.42 && git push origin refs/tags/v0.42-acquisition-locked && git ls-remote --tags origin v0.42-acquisition-locked
```
From here on `osf/v42/data/t4_raw.jsonl` is never written again (no further `--collect`).

## 10. v1.12's record that t4 is complete: `anchor/t4_complete_v1_12.json` (Coverage's collection guard needs it)

Nothing else writes this file. v1.12's `acquire_v1_12.t4_guard` reads `t4_raw_path` (absolute), `t4_raw_sha256`, `t4_last_call_utc`, `recorded_by`, and refuses `--collect` unless the raw file still has that SHA-256, no raw line finished after `t4_last_call_utc`, and that time is in the past. The helper refuses while any collection runs, while a batch is open, before `v0.42-acquisition-locked` is on origin, or if the raw file differs from the file at that tag; it sets `t4_last_call_utc` to the latest `started_utc`/`finished_utc` in the raw file, adds the tag, commit, blob and call counts, writes into the v1.12 worktree and then runs v1.12's own `t4_guard` on the record (rehearsed on fake data: PASS; after one more raw line: REFUSED):
```
cd /Users/pablou/aias/_worktrees/v0.42 && PYTHONDONTWRITEBYTECODE=1 python3 osf/v42/lock/write_t4_complete_v0_42.py --dry-run
cd /Users/pablou/aias/_worktrees/v0.42 && PYTHONDONTWRITEBYTECODE=1 python3 osf/v42/lock/write_t4_complete_v0_42.py
cd /Users/pablou/aias/_worktrees/v1.12 && git branch --show-current && git add osf/methodology/v1_12/anchor/t4_complete_v1_12.json && git commit -m "v1.12 anchor: t4_complete_v1_12.json (t4 = v0.42 complete; v0.42-acquisition-locked)" && git push origin v1.12
cd /Users/pablou/aias/_worktrees/v1.12 && python3 scripts/osf_upload.py osf/methodology/v1_12/anchor methodology/v1_12/anchor && PYTHONDONTWRITEBYTECODE=1 python3 osf/methodology/v1_12/lock/osf_verify_v1_12.py osf/methodology/v1_12/anchor methodology/v1_12/anchor | tail -1
```
Expect `v1.12 t4_guard on this record: PASS`; on OSF the v1.12 anchor folder then holds 4 files (`4 of 4 … PASS`). Do this before v1.12's first window (2026-11-14 00:00 UTC). **For v1.12's collection:** launch it with the step-7 pattern (`nohup python3 -u … --collect … &` then `caffeinate -dimsu -w PID`), **not** `caffeinate python3 acquire_v1_12.py --collect`: on macOS caffeinate then runs as a child of the collection with the same command line, and v1.12's `other_collection_guard` (which excludes only itself and its parent) refuses itself (checked Nov 10 with v1.12's own function: plain and `-w` pass; `caffeinate <cmd>` is REFUSED).

## 11. After t4's last call: the order of the downstream records

No Ranking statistic (rank position, MNP, MODE) on any t4 answer before v1.14's Stage 1 (v1.14 §9 step 2; this includes v1.12's H5 and v1.13's H4).

1. **Coding** (paid: the v0.23 Phase A recognition judge, Claude Sonnet 4.5, inside the $100 through the $0.50 reserve; must finish before 2026-11-30):
   ```
   cd /Users/pablou/aias/_worktrees/v0.42 && (PYTHONDONTWRITEBYTECODE=1 nohup python3 -u osf/v42/scripts/code_t4_v0_42.py --judge > osf/v42/data/code_v0_42.log 2>&1 &); sleep 50; tail -3 osf/v42/data/code_v0_42.log
   ```
   Writes `osf/v42/data/coded/{v19..v23}_phase_{a,b}.csv` (refuses unless `v0.42-prereg-r1` is on origin). Commit the coded tables and the log.
2. **v0.42 scoring, once:** `cd /Users/pablou/aias/_worktrees/v0.42 && (PYTHONDONTWRITEBYTECODE=1 nohup python3 -u osf/v42/scripts/score_v0_42.py --run > osf/v42/data/score_v0_42.log 2>&1 &)`; read the log until `wrote …`. Writes `osf/v42/v42_verdicts.json` and `osf/v42/v42_brand_table.csv`. Commit them, tag `v0.42-scoring-locked` (as v0.41), push branch and tag. This tag is the `--v042-scored-ref` of step 3; the raw file in it must equal the acquisition-locked file (v1.14 halts otherwise).
3. **v1.14 Stage 1, once** (in the v1.14 worktree; refuses without `v1.14-prereg-r2`, its r2 anchor `osf/methodology/v1_14/anchor/git_anchor_v1_14.json`, `v0.42-acquisition-locked`, an unchanged lock manifest, and the coder blob `2d36735d…` at the acquisition tag; runs once):
   ```
   cd /Users/pablou/aias/_worktrees/v1.14 && git fetch origin --tags && (PYTHONDONTWRITEBYTECODE=1 nohup python3 -u scripts/score_v1_14.py --stage 1 --v042-scored-ref v0.42-scoring-locked > /tmp/v114_stage1.log 2>&1 &); sleep 50; tail -5 /tmp/v114_stage1.log
   ```
4. **Then** the Ranking legs of v1.12 (H5, gating only if Stage 1 is SEPARABLE; reads R*_S0 from `osf/methodology/v1_14/outputs/stage1/stage1_v1_14.json`) and v1.13 (H4); v1.12's collection itself needs only step 10 and its window.

## R. Rehearsal on local fakes (re-runnable; no request leaves the machine)

```
cd /Users/pablou/aias/_worktrees/v0.42 && rm -rf /tmp/v42_e2e && (PYTHONDONTWRITEBYTECODE=1 nohup python3 osf/v42/lock/fake_collect_e2e_v0_42.py --scratch /tmp/v42_e2e > /tmp/v42_e2e.log 2>&1 &); sleep 54; tail -3 /tmp/v42_e2e.log
```
Copies `osf/v42/{prereg,scripts,lock}` into a scratch repository with a local bare origin and runs the real `--collect` with `PYTHONPATH=osf/v42/lock/fakes` (fake `anthropic`, `openai`, `google.genai` that bill to a file; fake keys; proxies and SDK base URLs pointed at 127.0.0.1:9). Result on 2026-11-10: **28 of 28 checks PASS**:
- anchor: refused before the tag is on origin, with no anchor file, and with an anchor naming another commit; `write_anchor_v0_42.py` writes one naming the tag's commit; nothing sent by the refused runs;
- normal (≈ the central estimate): exit 0; 876 calls answered, one line each; Fable in 7 batches (30, 30, 30, 112, 30, 30, 30); recorded cost = fake bill ($64.69; $65.19 with the judge reserve); no pause; journal 7 created / 7 recorded; a second `--collect` sends nothing;
- pause80 (tokens × 1.5): exit 5 at recorded spend $80.10 (in block 7; in-flight requests finish); recorded = billed; a re-run without approval sends nothing; with `--approve-past-80` it finishes (exit 0, $92.94 with reserve, ≤ $100);
- projection (S1 tokens × 2.2): exit 5 after block 5 at $49.95, before any S1 run-2 call; a re-run without approval sends nothing; with `--approve-projection` it continues until the $80 pause (at $84.26: a 30-request batch already sent finishes);
- interrupt: killed with the first Fable batch in flight (billed $3.16, recorded $2.26); the resumed run recovers that batch first, creates 7 batches in all (nothing re-sent), ends with recorded = billed ($64.69), 876 billed requests for 876 calls;
- one collection: a collection launched as `exec caffeinate -dimsu python3 … --collect` does not refuse itself; a second v0.42 `--collect` is refused; v1.12's own guard also sees it;
- window: a raw file whose first call is > 72 h old → exit 6, nothing sent.
