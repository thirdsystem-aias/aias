# DEVIATIONS

## Entry 1 — lock anchored on OSF before the GitHub push (2026-11-09, before the first t3 call)

**Type:** procedural; ex ante (recorded before any t3 study call).

**Locked sequence:** content lock → commit → tag `v0.41-prereg-r1` → `git push` → OSF deposit → verify both remotes → first t3 call.

**What happened:** the content was locked, committed and tagged, and the pre-registration was deposited on OSF and verified byte for byte (2026-11-09, ~06:40 UTC). The push to GitHub could not be made: no GitHub credentials are available on the acquisition machine, and the session's GitHub access does not include write access to `thirdsystem-aias/aias` (push refused, HTTP 403).

**Handling (Pablo's decision, 2026-11-09 07:31 CT):** proceed with OSF as the external anchor. Before the first t3 call, this file and `git_anchor_*.json` (tag object, commit and tree hashes, and the SHA-256 of every locked file) were deposited on OSF, which timestamps them. The tag is pushed to GitHub as soon as access exists; the pushed tag must resolve to the recorded hashes, which anyone can check.

**Effect on inference:** none. The pre-registration content and its timestamp precede all t3 data; only the order of the two external anchors changes.

## Entry 2 — collection interrupted by a restart of the acquisition Mac (recorded 2026-11-09T14:30:22Z, before resuming)

**Type:** procedural; contemporaneous.

**What happened:** the Mac restarted at about 14:26 UTC on 2026-11-09, during v0.23 Phase A (132 of 144 recognition calls done, all ok, checkpointed). v0.20, v0.21 and v0.22 had completed before it (chain log: exit 0 at 13:34:57, 13:36:06 and 13:37:19 UTC). v0.19 had not started.

**Handling:** the v0.23 runner (byte-locked) checkpoints but cannot resume, and editing it is not permitted. The 132 interrupted v0.23 answers are archived unchanged in `osf/v41/data/_interrupted_v23_2026-11-09/` and are NOT used. v0.23 is re-run in full (Phase A 144 + Phase B 36) with the locked runner, then v0.19, by the same chain (`run_t3_chain.sh v23 v19`), probe parity re-checked before each. The provenance sidecar keeps the interrupted calls' rows (their timestamps precede the restart). The t3 date is unchanged (2026-11-09).

**Effect on inference:** none expected; the analysed v0.23 wave is one complete, uninterrupted run. Same-day re-asking of the same probes is noted as a limitation (the models were asked 132 of the v0.23 recognition questions twice on the same day; answers from the first, interrupted pass are not analysed).

## Entry 3 — coding environment for v0.23 (recorded 2026-11-09T16:15:14Z, before scoring)

**Type:** procedural; coding, not acquisition.

The t3 collection finished at 15:36:40 UTC (chain log: v23 exit 0 at 15:31:04, v19 exit 0 at 15:36:40): 852 of 852 study calls returned (v0.20–v0.22 540, v0.23 180, v0.19 132). v0.19 parsing ran under the phase venv (~/aias/.venv-v41). The v0.23 coding script (`scripts/score_v0_23.py`, unchanged) imports numpy, which that venv lacks, so v0.23 coding (deterministic Phase B mention scan; Phase A recognition judge, alias `claude-sonnet-4-5`, as at t1 and t2) ran under the main venv (~/aias/venv: Python 3.14.4, anthropic 0.97.0, the same SDK version as the phase venv). Judge calls are logged in the provenance sidecar (phase A_judge). No coding rule, prompt or model changed.
