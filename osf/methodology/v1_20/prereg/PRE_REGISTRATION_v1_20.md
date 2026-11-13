# AIAS v1.20 (proposed id) — Sentiment Paper A, successor re-scoring: v1.11's judge replies under a one-object JSON rule

AIAS™ Measurement Program — Third System™. **Status: DRAFT r0 (2026-11-13), not locked.** Branch `sentiment-successor`, cut from tag `v1.11-prereg-r1` (commit `62e2d38`, v1.11's content lock). The id v1.20 is proposed, not claimed (§0). Lock target: tag `v1.20-prereg-r1`, pushed, with `anchor/git_anchor_v1_20.json` and the OSF deposit of `osf/methodology/v1_20/prereg/`, `scoping/` and `anchor/`, **before v1.11's first judge call** (v1.11 §8: no batch before 2026-11-22 06:00 UTC). Draft to Pablo by Fri 2026-11-20 (the coordinator sends it).

Re-analysis only, **US$0**: no model call, no new answer, no new judge reply. v1.20 reads v1.11's own stored judge replies and changes one rule, the rule that decides which replies count. Every other rule, threshold, seed and statistic is v1.11's, run with v1.11's code (§6).

Files: this document; `../anchor/DEVIATIONS.md` (Entry 0, ex ante); `scripts/score_v1_20.py` (the rule: `parse_reply`, `record_judgement`, `outcomes`; `classify` for format counts) and `scripts/test_score_v1_20.py`; `../scoping/format_counts_v1_15.py` and its output `../scoping/format_counts_v1_15.json` (the parser demonstration of §10). Still to be added before the lock: §16.

## 0. Phase identity

| Field | Value |
|---|---|
| PHASE_ID | v1.20 (proposed; §0 note) |
| PHASE_TITLE | Sentiment Paper A, successor re-scoring: v1.11's judge replies under a one-object JSON rule |
| PHASE_TYPE | methodology re-analysis (re-scoring of stored judge replies; no model call) |
| SUCCESSOR_OF | v1.11 (tag `v1.11-prereg-r1`, locked 2026-11-10; anchor commit `97c26be`; DEVIATIONS Entry 1 at `95c3fa1`) |
| PREREG_TAG | v1.20-prereg-r1 (at lock) |
| DECISION | Pablo, Thu 2026-11-12, 6:57 am CT, control panel: "Sentiment (b)" — a successor re-scoring rule locked before 2026-11-22 06:00 UTC, US$0 (STATUS.md, Nov 12 runner entries) |
| CHANGED RULE | which judge replies count (§3) and, as a consequence, which stored attempt is a unit's judgement (§4) |
| UNCHANGED | everything else in v1.11 (§6) |
| COST | US$0 (§11) |
| LABEL | Sentiment stays **provisional** (AI-judged) until Paper B's human-label validation, as in v1.11 |

**Id.** Methodology studies take the next v1.N id (CLAUDE.md, pre-registration discipline: tag `v1.N-prereg-rN`). On 2026-11-13 at about 1:30 am CT the repository had branches `v1.10` to `v1.19` (plus `v1.19-r2-truncation-aside`), tags up to `v1.18-prereg-r1`, and no ref, commit subject since 2026-11-01, master document (`Try system book/`: CLAUDE.md, STATUS.md, roadmap, kickoff prompt) or claude.ai project document naming v1.20. v1.20 is therefore the next free id. The program's naming registry (`claude/naming-registry.md`, v1.1) governs product and score names, not study ids, and has no entry to update. Alternative, if the coordinator prefers to keep the tie to v1.11 visible in the id: a suffix in the style of `v1.11-paperB` (e.g. `v1.11-successor`, tag `v1.11-successor-prereg-r1`). The coordinator claims the id; this draft does not.

## 1. Purpose and the evidence behind it

v1.11 (Sentiment Paper A) has Claude Opus 5.5 (J1) and GPT-6.1 Sol (J2) rate the valence of 7,578 archived units with a prompt-only JSON reply. Its locked validity rule (v1.11 §4.2; `judge_prompt_v1_11.md`, "Validation applied to every output"; `score_v1_11.parse_judge_output`) accepts a reply only if the **whole reply** is one JSON object (a code fence is stripped only when the reply begins with it). An invalid reply is retried twice with identical input; three invalid replies make the unit JUDGE_FAIL, and JUDGE_FAIL above 2% of any set's units, per judge, halts the study before scoring.

v1.15 (Sentiment on t4) ran v1.11's instrument unchanged on 1,547 t4 windows (judge run 2026-11-12 03:37–04:10 UTC, US$7.51). Its Stage J halted: J1 put a short prose sentence before a complete JSON object on 65 of 1,547 first tries; identical retries left 35 and then 25 such replies; 25 units became JUDGE_FAIL, 8 of 374 in the cosmetics set (2.14% > 2%); J2 had none (v1.15 `postlock/DEVIATIONS_continued_v1_15.md`, Entry 2). No Sentiment score exists for t4. Every failed reply still held a complete JSON object with the five required keys.

v1.11 uses the same judges, prompt, call parameters and rule over 26 J1 sets (3 R, 15 F, 8 E), from 2026-11-22. Under its rule it is likely to halt the same way (runner's risk memo, STATUS.md Nov 12: model estimate P(at least one set above 2%) ≈ 0.99 at the v1.15 rate). v1.11's locked text gives no lever (v1.11 §4.2, §13.3–13.4), and a locked pre-registration never changes. v1.20 is the option Pablo chose: a second pre-registration, locked before any v1.11 judge reply exists, that re-scores v1.11's replies under one extraction rule declared now. The program's rule since 2026-11-12 (CLAUDE.md, "LLM judges and strict JSON") is the same for studies not yet locked: state the extraction rule in advance and test it on recorded replies.

**What v1.20 is not.** It does not replace v1.11, change any locked v1.11 file, re-send any request, or re-score v1.15 (v1.15's halt stands; its replies are used here only to test the parser, §10).

## 2. Scope: v1.11's raw replies only, as stored

- **Replies.** The call records of v1.11's judge run, `osf/methodology/v1_11/data/judge_raw_v1_11.jsonl`, exactly as `judge_v1_11.py --freeze` froze them; v1.20 stops unless the file's SHA-256 equals `raw_sha256` in `osf/methodology/v1_11/outputs/judge_outputs_frozen_v1_11.json`. The reply of a record is its `text` field: the concatenated text blocks of an Anthropic message or the `output_text` of an OpenAI response (`judge_v1_11.parse_anthropic_message`, `parse_openai_response`); reasoning and thinking content is not part of it. The record's `status`, `served_ok`, `finish_reason`, `role`, `judge_model`, `unit_id`, `pass`, `attempt` and `started_utc` are read as stored. Nothing is re-sent, edited or re-parsed by hand.
- **Units, plan and roles.** v1.11's unit table (`prereg/units_v1_11.csv`, SHA-256 `1243e8e15e2dc6afc894197de9819d149d934e3883bc9f504e8fdfbbbb9c08b8`, checked against `u0_v1_11.json`), the plan parameters and roles in v1.11's frozen record (`effective_units`, any reduction of v1.11 §7, and any alternate judge that replaced J1 or J2 under v1.11 §4.2), all as frozen. v1.20 judges nothing and reduces nothing.
- **Other inputs.** For Stage C, the P, C\* and Ranking inputs v1.11 §2 pins, read by v1.11's code with v1.11's manifest check.
- **When.** v1.20 reads v1.11's replies only after v1.11's `--freeze` and v1.11's own Stage J have run (§7), so that v1.11's result under its own rule exists first.
- **Out of scope.** v1.15's t4 replies (used only for §10's format counts), any other study's judge replies, the Paper B labels.

## 3. The rule (the only rule that changes)

**A reply counts when it holds exactly one complete JSON object and that object passes v1.11's checks; any text around the object is ignored.** Defined exactly, and implemented in `scripts/score_v1_20.py`:

1. **Complete JSON object.** The reply is scanned from its first character. At each `{` that is not inside an object already found, Python's standard JSON decoder (`json.JSONDecoder().raw_decode`, the decoder behind the `json.loads` call in v1.11's parser, with the same defaults) is tried from that character. If it decodes a JSON object, that is one complete object, and the scan resumes after its closing `}` (objects nested inside it and braces inside its strings are never counted again). If it does not (invalid JSON from that point, including an object cut off before its closing brace), the scan moves to the next `{`. Text that is not JSON (prose, markdown, code-fence markers, arrays' brackets, a wrapper that does not itself decode) is surrounding text.
2. **Exactly one.** Zero complete objects: invalid. Two or more complete top-level objects: invalid, whatever they contain and even if identical (no rule picks one).
3. **The required keys and every other check are v1.11's, unchanged.** The object's own text is passed to `score_v1_11.parse_judge_output` (tag `v1.11-prereg-r1`): exactly the five keys `refers_to_brand`, `evaluative`, `mixed`, `valence`, `evidence` (no key missing, none added); the three flags are JSON booleans; `valence` is a JSON integer in −2…2 (not a string, boolean or float); `evidence` is a string; `refers_to_brand` false requires valence 0 and the two other flags false; `evaluative` false requires valence 0 and `mixed` false; an evidence quote over 20 words is flagged, not rejected. A single object that fails any check makes the reply invalid; there is no repair.
4. **Text around the object is ignored**, whatever it is: a sentence before it, a remark after it, a code fence around it, whitespace.
5. **Cut-off replies.** An object cut off by the output limit is not complete (item 1) and does not count. In addition, a reply whose recorded `finish_reason` shows the output cap (Anthropic `max_tokens`; OpenAI `incomplete:max_output_tokens`; Gemini `MAX_TOKENS`, also after an enum prefix; `length`) is invalid even if it holds a complete object, as v1.11 §4.2 states ("a reply cut by the cap is invalid output"). v1.11's code never reads the finish reason; v1.20 applies v1.11's written rule. (Answers cut off at the *answering* models' limit are a different matter: §8.)
6. **Code-fenced JSON** counts: the fence is surrounding text. (v1.11 accepted a fenced reply only when the reply began with the fence.)
7. **Unchanged from v1.11:** an empty reply is invalid; a served model that is neither the requested ID nor a dated snapshot of it makes the reply invalid (MC_Served); only records with status `ok` can yield a judgement; API errors are not invalid replies (v1.11 `outcomes`).

| Reply | v1.11 rule | v1.20 rule |
|---|---|---|
| the object alone (whitespace around it) | valid | valid |
| ```` ```json ```` fence, object, fence | valid | valid |
| sentence(s), then the object (fenced or not) | invalid | valid |
| the object, then text | invalid | valid |
| text, object, text | invalid | valid |
| a broken wrapper around a complete object, e.g. `{"rating": {…five keys…}` with the wrapper unclosed | invalid | valid (the wrapper does not decode; the inner object is the one complete object) |
| `[ {…} ]` (one object inside an array) | invalid | valid (brackets are surrounding text) |
| a complete wrapper object, e.g. `{"rating": {…}}` | invalid | invalid (one top-level object with the wrong keys) |
| two complete objects (copies, a draft and a final, an example in the preamble, or two inside an array) | invalid | invalid |
| no complete object (prose only; object cut off; single quotes or Python literals) | invalid | invalid |
| one object with a key missing or added, a wrong type, or inconsistent flags | invalid | invalid |
| finish reason shows the output cap | valid only if the whole reply parsed (code) | invalid |
| empty reply; served-model mismatch | invalid | invalid |

**Every reply valid under v1.11's code is valid under v1.20** except one corner case: a reply cut at the cap whose visible text is exactly one complete object (item 5; none occurred among v1.15's 3,353 records, §10). Tested (`test_superset_of_v111`; §10's demonstration found no reply valid under v1.11's rule and invalid under v1.20's).

**Tests** (`python3 -m unittest scripts/test_score_v1_20.py`, synthetic replies only; 33 tests, all pass on 2026-11-13): sentence + JSON; JSON + trailing text; text on both sides; two objects (copies, different, an example object in the preamble, two in an array); missing key; extra key; truncated at four cut points; code-fenced (alone, after prose, unclosed); braces inside strings; a non-JSON brace in the prose; a nested wrapper; a broken wrapper; one object in an array; each of v1.11's checks (consistency, string/boolean/float/out-of-range valence, string flag, null evidence, the 20-word flag); Python literals and single quotes; empty and whitespace replies; v1.11-valid replies stay valid with identical parsed output; the finish-reason set; a cap-cut reply with a complete object; a served-model mismatch; the per-unit outcome rule (§4); and the 2% rule re-evaluated with v1.11's own `fail_check` (§5).

## 4. Which stored reply is a unit's judgement

`score_v1_20.outcomes` is v1.11's `outcomes` with the rule of §3 in place of v1.11's parser; nothing else changes. For each (judge role, unit, pass) — passes `main` and `repeat` (the self-consistency sample) — the records of the model assigned to the role are read in v1.11's order (attempt, then start time); API errors are skipped; **the first stored reply that counts under §3 is the unit's judgement**; if none counts and at least 3 replies were received (1 + 2 retries, v1.11's `MAX_PARSE_RETRIES`), the unit is JUDGE_FAIL; otherwise it is UNJUDGED (v1.11's definitions). Consequences, declared now:

- v1.11 sends a retry only after a reply that fails v1.11's rule. Where an earlier attempt counts under §3, v1.20 scores that attempt, not the later retry that v1.11 scores (in v1.15's records: 40 of 1,547 J1 main-pass units, §10). This is the rule applied as if it had been in force during the run, and it is the primary analysis.
- A unit that v1.11 leaves UNJUDGED with one or two invalid replies stored (e.g. a run stopped at the US$80 pause) becomes VALID if one of those replies counts under §3. Counted and reported.
- **Sensitivity S-ATT** (v1.11 first): each unit takes v1.11's own judgement where v1.11's rule yields one, and the §3 rule only where v1.11 has JUDGE_FAIL or UNJUDGED. Every statistic of §5 is reported under S-ATT next to the primary; verdict changes are listed, never substituted.

## 5. The 2% rule and Stage J under the new parse

1. **JUDGE_FAIL check, re-evaluated.** v1.11's `fail_check` runs unchanged on the v1.20 outcomes: JUDGE_FAIL share per judge × set, over the units sent (VALID + JUDGE_FAIL), for J1's 26 sets and J2's sets as v1.11 defines them (effective units after any v1.11 reduction). **Above 2% in any set (per judge), v1.20 halts before scoring**, exactly as v1.11 §4.2 would; the halt is reported as v1.20's result with the per-set table, and no further rule is tried. Self-consistency repeats are not part of the check (as in v1.11).
2. **Stage J** (v1.11 §8, `score_v1_11.run_stage_j` logic with `outcomes` replaced): S per score unit from J1 (v1.11 §4.3–4.4: near-neutral rule, n ≥ 6, refers-to-brand exclusions), H1_Judge_Agreement (ordinal α and brand ρ_w, thresholds of v1.11 §5), the self-consistency block (5% sample, 0.90 flag), outcome counts and the per-unit outcomes file. No P, C\* or Ranking value is read at Stage J.
3. **Stage C** (v1.11 §8): P and C\* opened only after Stage J is written; H2–H9 with v1.11's statistics, floors, bands, three-wave rule, noise guard, permutation and bootstrap settings, and H5's PENDING rule (R\* computed only after v1.10's Stage C verdicts exist, with v1.10's code and Stage S hash check); sensitivities SU, SD, NV, model-balanced S, J2-scored S, α over refers-true units, and the H9 conditional (v1.11 §5.1); descriptives 1–6 (v1.11 §6).
4. **Outputs** under `osf/methodology/v1_20/outputs/`: `stage_j_v1_20.json`, `unit_outcomes_v1_20.csv`, `v1_20_verdicts.json`, and `comparison_v1_11_v1_20.json` (per judge × set JUDGE_FAIL under both rules; units whose judgement comes from a different attempt; unit status transitions; v1.11's and v1.20's verdicts side by side when both exist). One-shot: each stage runs once; a re-run needs a DEVIATIONS entry.

## 6. Everything else is v1.11's, unchanged

Cited, not restated; v1.11's locked text governs: data and exclusions (v1.11 §2); units and windows, extraction-miss rule, window cap (§4.1); judges, call parameters, served-model rule, blinding, call order, scale, invalid-output retries, J2 coverage and samples, self-consistency (§4.2); near-neutral text (§4.3); score and n floor (§4.4); hypotheses H1–H9, decision rules, bands, three-wave rule, noise guard, H5 activation and PENDING rule (§5); sensitivities (§5.1); descriptives (§6); the binding projection and reductions as applied by v1.11's run (§7); run order (§8); the Paper B sample and its DEVIATIONS Entry 1 replacement (§9; Entry 1); limitations (§11). Seeds as locked (`score_v1_11.SEEDS`): unit order 111000, window cap 111001, J2 sample 111002, self-consistency 111003, E half 111004, H4 111011, H6 111012, bootstrap 111020, Paper B sample 111022 (and 111025 for Entry 1's replacement). v1.11's predictions (§10) stand; v1.20 adds none, except one about the rule itself: J1 JUDGE_FAIL under §3 below 0.5% in every set (v1.15's records: 0 of 1,547).

## 7. Relation to v1.11, and which result counts

- **Order.** v1.11 runs exactly as locked: judge run, `--freeze`, its own Stage J under its own rule, and, if Stage J passes, its Stage C. v1.20 then runs Stage J and, if its JUDGE_FAIL check passes, Stage C, on the same frozen replies. v1.20 runs in both cases below; it costs nothing.
- **Case A — v1.11 completes** (no halt): **v1.11 is the confirmatory record** (Pablo's decision). v1.20's results are reported beside it as a pre-registered re-scoring (agreement of verdicts, of S per unit, of JUDGE_FAIL counts). Where a verdict differs, both are reported and v1.11's stands for every program decision.
- **Case B — v1.11's Stage J halts on JUDGE_FAIL above 2%:** v1.11's record is the halt (no Sentiment scores, as for v1.15). **v1.20's verdicts are then Sentiment Paper A's result**: H1 (the instrument gate) and the separability gates H2, H3 and H5 decide whether Sentiment passes its Paper A gate. In the release plan (roadmap, FAST TRACK note of Pablo, 2026-11-12, 6:57 am), AIAS 3.0, 4.0 and 5.0 go to whichever remaining part next passes its gate; the control panel's milestones (as read on 2026-11-12, `claude/versioning-convention.md`) have AIAS 3.0 about mid-January 2027 if Coverage passes, and AIAS 4.0 about 2027-02-05, the release a Sentiment pass would feed if Sentiment is the next part to pass. That release and its own calibration pre-registration cite v1.20's verdicts, not v1.11's, in case B. Release numbers are never attached to Sentiment before it passes (messaging standard).
- **Case C — v1.11 stops for any other pre-registered reason** (frozen-input hash mismatch, anchor failure, a judge with no replacement): v1.20 meets the same stop, because it reads the same files and runs v1.11's checks; it is reported as not run. A run that ended at the US$80 pause without approval is analysed on the units judged, as v1.11 §7 says, by both studies.
- **v1.11's records** are never edited by v1.20. The note that v1.11's continued DEVIATIONS should carry before v1.11's run (pointing to v1.20 as the locked successor) is the coordinator's step, not part of this file.
- **Label.** In case B, Paper A says plainly that v1.11's locked rule halted and that the reported scores come from the successor rule locked before any v1.11 reply existed; the halt is reported with the same prominence as the scores (v1.11 §13.5).

## 8. Answers cut off at the output length limit (Pablo, 2026-11-12, 11:36 pm: "OK CHECK")

Pre-registrations not yet locked must say how archived answers that ended at the answering model's output limit are handled. **v1.11 judges such answers**, so v1.20 declares their handling here. Evidence (read-only; branch `truncation-audit` at `ea2b787`, `analysis/truncation_audit/README.md` and `results/`; the E files at tag `v1.11-prereg-r1`):

- **R block (v0.23 open recognition, cap 2,048 for all models).** t3: **35 of 144** answers ended at the cap by recorded finish reason — claude-opus-4-5 9 of 24 (`max_tokens`), gemini-2.5-flash 24 of 24 (`MAX_TOKENS`), gemini-2.5-flash-lite 2 of 24 (`results/phase_a_t3.csv`). t1 and t2 recorded no finish reason and no token count. v1.11 judges all 432 R answers as whole units.
- **F block (omnibus category answers; caps: v0.19 1,024 for all models; v0.20–v0.22 2,048 for Claude and GPT, none sent to Gemini; v0.23 2,048 for all).** Of the 540 answers, 27 are known to have ended at the cap (`results/omnibus_table.csv`): **11 before naming any registry brand** (t3: v0.19 gemini-2.5-flash 6, v0.23 gemini-2.5-flash 5), which yield no mention window and so no v1.11 unit; and **16 after naming at least one brand**, whose windows are v1.11 F units: t1 4 (v0.19 gemini-2.5-flash-lite 2, output tokens at the cap; v0.23 gemini-2.5-flash-lite 2, text byte-identical to a t3 answer that ended at the cap), t2 5 (3 and 2, same evidence), t3 7 (v0.19 gemini-2.5-flash-lite 4, v0.23 gemini-2.5-flash-lite 2 and gemini-2.5-flash 1, finish reason). t1 and t2 recorded no finish reason in any substrate; only v0.19 recorded output tokens there (not for gemini-2.5-flash), so the cut status of 288 of the 360 t1/t2 answers is not recorded (144 per wave, `omnibus_table.csv`); at t3 no v0.20–v0.22 answer ended at a cap. The v0.19 gemini-2.5-flash answers name no brand in any wave (t3: all 6 cut before the first brand), so they add no unit.
- **E block (eight early sets).** None of the eight answer files records a finish reason or token count (columns read; `call_status` is `ok` in all 2,304 rows). The runner in the repository (`run_aias_v2.py` at the tag, and its pre-refactor copy) sends `max_tokens` 1,024 to Anthropic models and no output limit to OpenAI, Google or xAI models. Answer lengths by code (characters; no text printed): claude-opus-4-7 at most 2,759 (none ≥ 3,000); claude-sonnet-4-6 12 of 384 at ≥ 3,000 and 2 at ≥ 4,000 (maximum 4,011). Whether any E answer ended at the cap is not recorded; a few claude-sonnet-4-6 answers are long enough to have reached it.

**Handling (fixed now):**

1. **Primary analysis:** every unit as v1.11 defines it, cut answers included (v1.11's locked design; a cut answer is judged on the text that exists). v1.20 changes only the reply rule.
2. **Sensitivity S-CUT (known or likely cut).** Every statistic that v1.11's SD sensitivity recomputes (H1 α and brand ρ, H2–H6, H9), plus H7 and H8, is recomputed without the units whose answer is flagged as cut, and the verdict changes are listed (never substituted). The flag list `prereg/cut_units_v1_20.csv` (unit_id, block, wave, model, evidence) is built before the lock by this fixed rule, from recorded fields only: (a) recorded finish reason in the cap set of §3 item 5 (t3 records and the v0.41 call sidecar, as the audit matched them); (b) recorded output tokens (visible plus thinking) at or above the cap; (c) answer text byte-identical to a t3 answer of the same model and question that ended at the cap, from a model without thinking tokens (the audit's `identical_to_t3`); (d) E: answers from Anthropic models whose offline token estimate (o200k_base count × 1.30, v1.11 §7's Anthropic factor; tiktoken as in v1.11's scoping) is at least 90% of the 1,024-token cap. In S-CUT, R's floor is n ≥ 4 instead of 6, because at t3 every brand loses its gemini-2.5-flash answer and the six-answer floor would leave no brand rated; F and E floors are unchanged.
3. **Sensitivity S-CUT-M (unrecorded waves).** Because t1 and t2 recorded no finish reason for most answers, R and F are also reported without every unit of the model × block × substrate cells in which at least half of the t3 answers ended at the cap, at every wave: R v0.23 gemini-2.5-flash (24 of 24); F v0.19 gemini-2.5-flash-lite (4 of 6); F v0.23 gemini-2.5-flash (6 of 6). (F v0.19 gemini-2.5-flash, 6 of 6, contributes no unit.) R floor n ≥ 4 as in S-CUT.
4. **Counts reported** with the descriptives: flagged units per block × wave × model, and how many of them are judged, in J2's sample and in the Paper B sample.
5. If the list's build finds evidence that differs from the counts above (e.g. a different number of cut answers once the per-answer join is made), the list follows the rule, and the difference is written in DEVIATIONS Entry 0 before the lock.

## 9. Timing and anchoring

- Draft r0 (this file): 2026-11-13. To Pablo by Fri 2026-11-20 (coordinator). Lock after the program's usual 24 hours with Pablo, and in any case **before 2026-11-22 06:00 UTC**: content lock → `LOCK_MANIFEST_v1_20.sha256` → commit → tag `v1.20-prereg-r1` → push → anchor record → OSF deposit of `prereg/`, `scoping/`, `anchor/` (SHA-256 verified). The coordinator does every step; no date moves.
- **If v1.11's first judge batch is submitted before v1.20's anchor exists**, v1.20 is not a pre-registration: it is reported only as an exploratory re-analysis under this text, and case B of §7 does not apply (declared now).
- v1.20's Stage J and Stage C run only after v1.11's `--freeze` and v1.11's own Stage J (§7). v1.20's scripts refuse to run without the v1.20 tag and anchor (to be added, §16).

## 10. Pre-lock record and the parser demonstration on v1.15's replies

**No v1.11 judge reply exists** (2026-11-13: no `osf/methodology/v1_11/data/` in any worktree; v1.11's first batch cannot be sent before 2026-11-22 06:00 UTC). The rule was written after seeing the *format* of v1.15's replies (DEVIATIONS Entry 2 of v1.15, and the counts below), never a valence; v1.15 judged t4 answers, which are not v1.11 units.

**Demonstration** (`scoping/format_counts_v1_15.py` → `scoping/format_counts_v1_15.json`, run 2026-11-13; read-only; the raw file matched v1.15's frozen SHA-256 `926ed9b0…` before counting; 3,353 records; no valence, quote, reply text or score read out or computed). "v1.15 rule" = v1.11's locked `outcomes` + `parse_judge_output`, which v1.15 imported unchanged.

| Judge, pass | Replies | Valid, v1.15 rule | Valid, v1.20 rule | Formats (all replies) |
|---|---|---|---|---|
| J1 Claude Opus 5.5, main | 1,647 (1,547 first tries, 65 second, 35 third) | 1,522 | 1,647 | 1,498 bare; 24 bare in a code fence; 77 prose before the object; 47 prose before a fenced object; 1 text after the object |
| J1, self-consistency repeat | 82 | 75 | 82 | 73 bare; 2 fenced; 5 prose before; 2 prose before a fenced object |
| J2 GPT-6.1 Sol, main | 1,547 | 1,547 | 1,547 | 1,547 bare |
| J2, repeat | 77 | 77 | 77 | 77 bare |

J1 first tries: 1,482 valid under both rules (1,459 bare, 23 fenced); the other 65 (39 prose before, 25 prose before a fenced object, 1 text after) fail v1.15's rule and count under v1.20's — v1.15's DEVIATIONS Entry 2 count of 65 is reproduced. No reply held zero or several objects, none failed v1.11's key or consistency checks once extracted, none ended at the output cap (consistent with the truncation audit's `coding_calls.csv`: 0 of 1,729 and 0 of 1,624), every served model passed, and no reply valid under v1.15's rule was invalid under v1.20's. **Units:** J1 main pass, v1.15 rule 1,522 VALID + 25 JUDGE_FAIL, v1.20 rule 1,547 VALID + 0 JUDGE_FAIL, every unit's judgement taken from its first try (40 units that v1.15's rule scores from a retry, 25 rescued). J1 JUDGE_FAIL per set, v1.15 → v1.20 rule: v0.19 1/277 → 0; v0.20 5/299 → 0; v0.21 8/374 (2.14%, the halt) → 0; v0.22 6/339 → 0; v0.23 5/258 → 0. J1 repeats 75 + 2 JUDGE_FAIL → 77 VALID. J2 unchanged (0 JUDGE_FAIL). **This is a parser demonstration only: v1.15's locked result (halt, no S_t4) stands and is not re-scored.**

Other reads before this draft, all disclosed in DEVIATIONS Entry 0: v1.11's pre-registration, judge prompt, DEVIATIONS (Entries 0–1) and scorer code; v1.15's DEVIATIONS and frozen records; the truncation audit's README and result tables; the E answer files' column names, `call_status` values and per-model character lengths (computed by code; no answer text printed).

## 11. Cost

US$0. No model call of any kind; v1.11's US$100 cap is untouched by v1.20.

## 12. Deviations policy

`osf/methodology/v1_20/anchor/DEVIATIONS.md` opens with Entry 0 (ex ante). After the lock, as v1.11 §13: every change gets an entry (id, date, ex ante or ex post, what, why, effect on inference); a frozen-input hash mismatch halts; a code fix is allowed only if it restores a rule as written here, with results before and after; the rule of §3, the attempt rule of §4, the 2% threshold, the sensitivities of §4 and §8 and everything v1.11 fixes do not change after the lock; anything added later is exploratory; a halt or a failed gate is published with the same prominence as a pass.

## 13. Limitations

The rule is chosen after one study (v1.15) showed how the judge fails; it is fixed before any v1.11 reply exists, and it removes a failure of format, not of content, but it is still a rule picked with knowledge of a failure mode. Extracting one object from text around it assumes the object is the judge's answer: a reply that argues for one valence in prose and gives another in the object is scored on the object (v1.11's checks still apply to the object). Under §4 the judgement for a few units comes from a different call than v1.11 would use; S-ATT reports the effect. Answers cut at the answering models' limit stay in the primary analysis (§8); S-CUT relies on recorded evidence, which is missing for most t1/t2 answers and for every E answer (estimated for E). All of v1.11's limitations (§11) apply.

## 14. Declarations

**Conflict of interest.** This study re-scores the judge replies of v1.11 and makes no brand selection of its own; v1.11's conflict-of-interest statement (v1.11 PRE_REGISTRATION §14, tag `v1.11-prereg-r1`; the source records quoted verbatim in v1.11 DEVIATIONS Entry 0) applies unchanged and is quoted verbatim: "The author is Director, Corporate Brand Creative and Governance, at Samsung Electronics America. This study re-analyses answers collected against brand registries fixed in earlier phases; it performs no new brand selection, and each registry carries its source phase's conflict-of-interest handling forward unchanged (the source records are quoted verbatim in DEVIATIONS Entry 0). Two items of record apply. In the automotive registry (v0.22), Samsung subsidiaries hold tier-2/3 component supply relationships with several registry brands — Harman International (audio systems), Samsung SDI (battery cells) and Samsung Display (infotainment) — characterized in the source phase as non-competitive, with no brand-level overlap, and imposing no operational restriction on registry composition (v0.22 Declarations; screened in v0.22 DEVIATIONS Entry 0, Part B). In the audiophile-headphones registry (v0.19), AKG was substituted with Denon before the v0.19 pre-registration lock because AKG's parent, Harman International, is a Samsung subsidiary (v0.19 PRE_REGISTRATION §2.3; v0.19 paper, DEVIATIONS Entry 1). Correction (November 10, 2026): Denon, which replaced AKG in the v0.19 registry, has itself been owned by Harman International, a wholly owned subsidiary of Samsung Electronics, since September 23, 2025, when Harman completed its acquisition of Sound United from Masimo; the v0.19 headphones registry therefore includes one Samsung-group brand. The substitution did not achieve its purpose, and this was not noticed until November 10, 2026. Every gate statistic is therefore also reported without Denon (sensitivity SD, §5.1). A string screen of all thirteen registries on 2026-11-10, for Samsung, Harman and the Harman and Sound United brand names listed in DEVIATIONS Entry 0, matched Denon (v0.19) only. Valence judging adds no brand choice and is fully automated against the locked registries and units, and this pre-registration is locked and deposited before any judge call. Samsung Electronics had no role in the design, conduct, analysis or reporting of this work." v1.20 keeps sensitivity SD and adds no brand, judge call or registry. Samsung Electronics had no role in the design, conduct, analysis or reporting of this work.

**Funding.** Self-funded.

**Ethics.** Not applicable: no human subjects (stored AI judge replies about archived AI answers).

**Use of AI tools.** During the preparation of this work the author used AI tools (Anthropic's Claude) to assist with study design, analysis and writing. The author reviewed and edited all content and takes full responsibility for it.

## 15. Open questions for Pablo (r0)

1. **Id:** v1.20 (next free methodology id) or a suffix that keeps v1.11 in the name (e.g. `v1.11-successor`)?
2. **Which attempt is scored (§4):** the first stored reply that counts (primary, "as if the rule had been in force") with v1.11-first as sensitivity S-ATT — or the reverse?
3. **Cap-cut judge replies (§3 item 5):** keep v1.11's written rule (invalid even with a complete object), or count a complete object whatever the finish reason (v1.11's code)? No v1.15 reply was affected.
4. **Two or more complete objects (§3 item 2):** invalid even when identical (draft), or accept identical copies?
5. **Cut-off answers (§8):** are S-CUT and S-CUT-M the handling you want, including the R floor of n ≥ 4 in both and the E estimate rule (o200k × 1.30 ≥ 90% of 1,024)? Or should the primary analysis itself drop known-cut answers?
6. **Case B (§7):** confirm that, if v1.11 halts on JUDGE_FAIL, v1.20's verdicts are Sentiment Paper A's result for the release decision.

## 16. Still to do before the lock (not done in r0)

1. Stage J/C wiring: `score_v1_20.py --stage J` and `--stage C` (v1.11's stage functions with `outcomes` replaced, outputs under `v1_20/outputs/`, the comparison file, S-ATT, S-CUT, S-CUT-M), refusing to run without tag `v1.20-prereg-r1`, the v1.20 anchor, v1.11's frozen record and v1.11's Stage J output; an end-to-end dry run on v1.11's synthetic replicas (`dryrun/`, fake judge with prose-before-JSON replies) and tests.
2. `prereg/cut_units_v1_20.csv` built by the §8 rule (per-answer join of the audit's evidence with v1.11's unit table; E token estimate), its counts written into §8, with a test.
3. `LOCK_MANIFEST_v1_20.sha256`, the anchor writer (as v1.11's `--write-anchor`), the lock steps, and the coordinator's ex-ante note in v1.11's continued DEVIATIONS.
4. Pablo's answers to §15.

## 17. Change log

- r0, 2026-11-13: first draft (lane C of the runner), not locked.
