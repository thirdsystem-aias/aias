# AIAS v1.13 — Grounding, Paper A: deviations log, continued after the Part I lock

This file continues `osf/methodology/v1_13/anchor/DEVIATIONS.md` (Entries 0 and 0a, written before the Part I lock) under the pre-registration's deviations policy (§10: id, date, ex ante or ex post, what, why, effect on inference). It is a separate file because `anchor/DEVIATIONS.md` is listed in `prereg/LOCK_MANIFEST_v1_13.sha256`, and no locked file is edited after the lock. Entries 1–4 are clarifications of the Part II text (`website_audit_protocol_v1_13.md`, `audit_v1_13.py`), frozen at the Part I lock commit `b83efb2` and made before the Part II lock (tag `v1.13-audit-r1`). Entries 5–12 are ex-ante deviations of Part I, made before any $t_4$ search-on record was read or any v1.13 statistic computed. Entry 13 sets when Stage C2 runs. No entry changes a hypothesis, threshold, floor, seed, class list, D_b, panel, verdict rule or collected datum. No frozen file is changed; new code lives only in `osf/methodology/v1_13/postlock/` and imports the locked scripts read-only.

## Entry 1 (Part II clarification, ex ante, 2026-11-11, before the Part II lock): the SDRI_kg-only sensitivity of H7

- **Issue.** Protocol §5: a brand whose home page (P1) could not be fetched has SDRI_site and SDRI NOT RATED "and enters H7 only through sensitivity (SDRI_kg alone)". No such sensitivity is numbered in pre-registration §7, and no locked script computes it (`score_v1_13.stage_c2` reads the column `SDRI` only).
- **Resolution.** The sensitivity is $\rho_w(\text{SDRI}_{\text{kg}}, G^*)$, one-sided, on every non-defunct unit with an SDRI_kg value and a rated G\* (the units without SDRI included), with §3's conventions (centred within-category ranks, ≥ 5 units per category, n floor 30, 10,000 permutations, 2,000 bootstrap draws) and seed 113009 (§3: "S-sensitivities"). It is reported beside H7 with H7's band reading and never gives or changes a verdict. Code: `postlock/audit_checks_v1_13.py` (`S_KG`), using `score_v1_13.sep_leg` and `struct_gap_verdict`.
- **Effect on inference.** None: H7, its units, statistic, seed and verdict rule are unchanged.

## Entry 2 (Part II clarification, ex ante, 2026-11-11, before the Part II lock): checks AQ1–AQ4

- **Issue.** Protocol §6 specifies AQ1–AQ4, but no locked script computes AQ2, AQ3 or AQ4. AQ2 says "share of P1 fetched with status 200", while `audit_v1_13.py` records a page's outcome (`ok` for any final non-redirect status below 400 that is not 403/429, served as HTML) and the final status. AQ4 compares indicators (1)–(5) across passes, but pass 2 fetches P1 only, while pass 1's (2)–(5) use P1–P3.
- **Resolution.** `postlock/audit_checks_v1_13.py` computes, from the audit records: AQ1 (D_b rows, none UNRESOLVED). AQ2 = units with an own domain whose P1 final status is 200 with outcome `ok`, over the units with an own domain (defunct units excluded), flagged below 0.80, with the share of outcome `ok` beside it. AQ3 = the JSON-LD blocks that did not parse (`ld_errors`) summed over the pages of pass 1, with the block count beside it. AQ4 = among the units with P1 `ok` in both passes, the share whose indicators (1)–(5) computed from P1 alone differ; pass 1 is recomputed from its stored P1 record so both passes use P1 only. All are reported only.
- **Effect on inference.** None: AQ1–AQ4 are reported checks; no verdict reads them.

## Entry 3 (Part II clarification, ex ante, 2026-11-11, before the Part II lock): "not collected before Stage C2" and the SDRI table's hash

- **Issue.** §3 makes H7 UNDETERMINED (handed to Paper B) if Part II was "not collected before Stage C2", but neither text dates Stage C2, and the C2 record does not hold the SDRI table's SHA-256.
- **Resolution (operational meaning).** Stage C2 is the one run of `score_v1_13.py --stage C2`. Part II counts as collected before Stage C2 if and only if `audit/v1_13_sdri.csv` (written by `audit_v1_13.py --sdri` after pass 1 and the logged QID adjudications) exists when that run starts. That is the scorer's own test (`Path(--sdri).exists()`). Stage C2 is run through `postlock/run_stage_v1_13.py`, which records, before the scorer starts, the start time, whether the table exists, its SHA-256, and the SHA-256 of every other input in `v1_13_inputs_C2.json`. The **date** of Stage C2 is not set here (see "For the pre-registrant").
- **Effect on inference.** None: H7's rule, its inputs and the scorer's test are unchanged; the table is identified by hash.

## Entry 4 (Part II clarification, ex ante, 2026-11-11, before the Part II lock): stale status lines in frozen files

- **Issue.** The first line of `prereg/website_audit_protocol_v1_13.md` reads "(DRAFT r1, to be sent to Pablo for the 24-hour review, 2026-11-10)". The same status appears in the docstrings of `scripts/audit_v1_13.py` (line 5) and `scripts/score_v1_13.py` (line 4) and in the first line of `prereg/source_classes_v1_13.md`.
- **Resolution.** These lines describe the files' status when they were written. The locked status is given by the tags: Part I by `v1.13-prereg-r1`, Part II by `v1.13-audit-r1`. The pre-registration says "the tag, not this line, marks the lock". The files are not edited.
- **Effect on inference.** None.

## Entry 5 (Part I, ex ante, 2026-11-11, before any t4 search-on record was read): sensitivity S6 is not computed by the locked scorer

- **What.** §7 S6 (D_b as verified by Part II: aliases from the audit's final redirect domains and Wikidata P856 added). `score_v1_13.py` states "Not in this core: the S6 alias merge from Part II's verified aliases (Stage C2)" and computes nothing for S6.
- **Resolution.** `postlock/c2_extras_v1_13.py` computes S6 after Stage C2 with the scorer's own functions. Each RESOLVED unit's D_b gets the registrable domain of its P1 final URL (`verified_alias`) and those of the adjudicated QID's P856 values; NONE units stay without D_b. Answers are rebuilt and classified with the extended D_b, and H1–H3 are recomputed as `stage_c1`'s other sensitivities are (seed 113009, 10,000 permutations, no bootstrap). Verdict changes are listed next to the verdicts. Without Part II data S6 is reported as not computed.
- **Effect on inference.** None: a sensitivity, never a verdict.

## Entry 6 (Part I, ex ante, 2026-11-11): sensitivity S7 cannot be reached from the scorer's command line

- **What.** `stage_c1` computes S7 (P and C\* from AIAS 2.0 at $t_3$, `osf/aias_2_0/aias_2_0_profiles.csv`) only when its input holds `profiles`. `main()` never passes them, and there is no option to.
- **Resolution.** `postlock/c2_extras_v1_13.py --profiles osf/aias_2_0/aias_2_0_profiles.csv` computes S7 with `score_v1_13.legacy_t3` and `gate_statistics`, as `stage_c1` would (seed 113009).
- **Effect on inference.** None (cross-panel, descriptive sensitivity).

## Entry 7 (Part I, ex ante, 2026-11-11): the cited-set tables of §6

- **What.** §6: "The same tables for the cited set (`citations`) are reported beside them." The scorer writes the cited set only as MQ8 and sensitivity S2, not as baseline tables.
- **Resolution.** `postlock/c2_extras_v1_13.py` applies `score_v1_13.baseline` to the answers built from `search.citations` (all N3 models, like the primary baseline) and writes them as `baseline_cited_set_all_N3`.
- **Effect on inference.** None (descriptives).

## Entry 8 (Part I, ex ante, 2026-11-11): the Stage C1 gate note while H4 is pending

- **What.** When v1.14's Stage 1 output does not yet exist at Stage C1, `stage_c1` passes `gating = {"H4_Sep_Ranking": h4_gates(None)} = False`. `gate()` then adds the note "H4_Sep_Ranking (UNDETERMINED) reported, not downgrading: v1.14's Stage 1 verdict is not SEPARABLE (N19)", although no Stage 1 verdict exists. The notes also say "Paper B only on Pablo's recorded decision".
- **Resolution.** The gate's `notes` are not a statement about v1.14. A pending leg is identified by `reasons.H4_Sep_Ranking` beginning "PENDING" and by `H4_ranking_source.status == "PENDING"`. The paper reports from those fields and never prints the notes. The verdict is unaffected: an UNDETERMINED leg never downgrades.
- **Effect on inference.** None.

## Entry 9 (Part I, ex ante, 2026-11-11): the baseline includes models dropped from the primary score

- **What.** `stage_c1` computes the §6 baseline on all three N3 models (`baseline(answers_n3, …)`), including a model that MQ2 (< 0.10) or MQ4 (Gemini, > 0.20 unresolved) drops from the primary G\*. Its G\* distribution by category can therefore differ from the primary G\*. MQ2 asks for a dropped model to be "reported both ways", but only S5 does this, and only for Gemini.
- **Resolution.** The locked baseline is reported as written and labelled "all three N3 models". `postlock/c2_extras_v1_13.py` adds the baseline on the primary panel (`baseline_primary_panel`). When MQ2 drops a model, it also adds H1–H3 with that model kept (`MQ2_kept`; seed 113009).
- **Effect on inference.** None: the primary panel and the verdicts are as §4 and N14 define them.

## Entry 10 (Part I, ex ante, 2026-11-11): input hashes

- **What.** `v1_13_verdicts.json` records no hash of its inputs: the $t_4$ raw file, v0.42's coder tables and brand table, v1.14's Stage 1 output and v1.12's unit table. §0 asks for the raw file's SHA-256 "recorded in the anchor before the first read". The anchor field `t4_raw_sha256` is null, and the anchor is a file that is not edited.
- **Resolution.** Stages C1 and C2 are run through `postlock/run_stage_v1_13.py`. It hashes every input given to the scorer before the scorer starts (bytes only; nothing is parsed or scored), runs `score_v1_13.py` unchanged with the same arguments, hashes the verdict file after it, and writes `v1_13_inputs_C1.json` / `v1_13_inputs_C2.json` beside it. The $t_4$ raw file's SHA-256 is that record's `inputs.t4_raw.sha256`, taken before the scorer's first read.
- **Effect on inference.** None.

## Entry 11 (Part I, ex ante, 2026-11-11): lock time

- **What.** Entry 0a states "locked at 2026-11-11 02:50 UTC". Tag `v1.13-prereg-r1` carries tagger date 2026-11-10T20:48:25-06:00, i.e. 2026-11-11 02:48:25 UTC, as `anchor/git_anchor_v1_13.json` records (`tagger_date`, `commit_date`).
- **Resolution.** The tag marks the lock (pre-registration header: "the tag, not this line, marks the lock"): 2026-11-11 02:48 UTC. Entry 0a's time was written ex ante as an approximation.
- **Effect on inference.** None: both times precede any $t_4$ answer.

## Entry 12 (Part I, ex ante, 2026-11-11): a locked unit test after the lock

- **What.** `scripts/tests/test_score_v1_13.py::TestGuard::test_stage_c1_refused_without_lock` expects `main(["--stage", "C1"])` to be refused. Now that the tag and the anchor exist and MQ7 passes, the guard lets it through, and `main` stops with a TypeError on the missing `--coded`. The guard still runs before any input is read, and no $t_4$ file is opened. The suite reports 89 of 90 tests passing, 1 error.
- **Resolution.** Expected after the lock; the test is not edited. Locked-suite results after the lock are read as 89 passing plus this error.
- **Effect on inference.** None.

## Entry 13 (Part I and Part II clarification, ex ante, 2026-11-11, before the Part II lock): when Stage C2 runs

- **Issue.** Stage C2 decides H7 (Part II collected, or handed to Paper B) and whether H4/H6 are computed or UNDETERMINED, but neither text dates it.
- **Resolution (set by the AIAS runner on 2026-11-11, before any $t_4$ search-on record was read or any v1.13 statistic computed; the pre-registrant may overrule it before Stage C2 runs).** Stage C2 runs once, after the later of: v1.12's scored output, or its recorded unavailability; v1.14's Stage 1 output, or its recorded unavailability; and `audit/v1_13_sdri.csv` from pass 1, or Part II recorded as held. It runs no later than 2026-11-25 23:59 CST (2026-11-26 05:59 UTC) and is never re-run. An input that does not exist by then is recorded as unavailable, and the legs that need it are reported as the pre-registration states for an unavailable input.
- **Effect on inference.** None on any hypothesis, threshold, floor, seed or verdict rule: it fixes, before any data, the one point in time at which the existing rules are applied.

## Entry 14 (Part II note, 2026-11-12, recorded after pass 1 began): pass 1 started at 22:09 CT after the collection computer restarted

- **What.** Pass 1 had been scheduled for 2026-11-12 21:57 CT (the receipt + 24 h = 21:55 CT, plus a 2-minute margin) as a waiting script on the collection computer. The computer crashed and restarted at about 21:41 CT, and was restarted again at 22:01 CT. The waiting script ended with it before pass 1 began: no audit request had been made and no audit record existed.
- **Resolution.** Pass 1 was started at 2026-11-13 04:09:56 UTC (22:09:56 CT) with the command in `postlock/PART2_LOCK_STEPS.md` §7, inside the window (receipt + 24 h to 2026-11-14 00:00 UTC). `audit_v1_13.py`'s guard checked the tag, the anchor, the receipt time, the window and the domain list before the first request. The start time recorded in `audit/window_pass1.json` is the one that counts.
- **Effect on inference.** None. No protocol text, unit, rule, threshold or seed changed; only the clock time at which pass 1 began moved, by 13 minutes, within the window.

## Entry 15 (Part II note, 2026-11-12 23:20 CT, recorded before the re-run): pass 1 cut off by a third restart after 21 of 112 units; re-run from its start

- **What.** Pass 1, started at 2026-11-13 04:09:56 UTC (Entry 14), stopped without finishing when the collection computer restarted again at about 22:33 CT, its third restart that evening (after about 21:41 and 22:01 CT, Entry 14). It had written 21 of the 112 unit records (the last at 22:29:13 CT) and 50 raw pages; `audit/window_pass1.json`, written only when a pass ends, does not exist. The likely cause, not proven, is memory and disk pressure from an unrelated file-copy job on the same computer; the audit is one process with one connection, at most 1 request a second and at most 3 pages per brand, and it had written 32 MB under `audit/`.
- **Resolution.** The protocol covers this case (`prereg/website_audit_protocol_v1_13.md`, Mac load plan: "a stopped pass is re-run from its start inside its window"). Pass 1 is re-run from its first unit with the same command (`postlock/PART2_LOCK_STEPS.md` §7), inside the window (it must start before 2026-11-14 00:00 UTC). Before the re-run, the 21 cut-off records were copied unchanged to `audit/cutoff_2026-11-12/` (SHA-256 `cf416e13ade04055a9b5b226204d14417d23ccc16fe855c4a2faa91382f6d3ba`), with their raw pages beside them, which are not committed or deposited, like all raw HTML. The cut-off records are kept for the record and enter no statistic. The re-run is set to start at 2026-11-13 07:05 UTC (01:05 CT), after another study's short timed pull, as the only job of this program on the computer; while an unrelated heavy job is still running it waits, and it starts no later than 2026-11-13 21:30 UTC (15:30 CT). The start time recorded in `audit/window_pass1.json` is the one that counts.
- **Effect on inference.** None. No protocol text, unit, rule, threshold or seed changed; pass 1 runs once, complete, inside its window, and the cut-off records are not used.
