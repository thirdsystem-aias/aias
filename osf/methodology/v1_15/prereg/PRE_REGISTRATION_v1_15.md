# AIAS v1.15 — Sentiment on t4: v1.11's locked instrument applied to the newest models' answers

AIAS™ Measurement Program — Third System™. **Status: r0 draft (2026-11-10, evening CT), not locked.** Branch `v1.15` (from `v1.11` @ 95c3fa1, which holds v1.11's locked files). Lock target: tag `v1.15-prereg-r1`, pushed, with `anchor/git_anchor_v1_15.json` and the OSF deposit of `osf/methodology/v1_15/prereg/` and `anchor/` **before the first judge call**, and no earlier than 24 hours after Pablo receives this text (the program's 24-hour rule).

Commissioned by Pablo on Tue 2026-11-10, 5:12 pm CT ("AIAS 6.0 Preview plan: all defaults, including the small Sentiment study on t4's answers"): Preview choice 1, default (a) (`osf/aias_6_0_preview/prereg/PRE_REGISTRATION_aias_6_0_preview.md` §3.4, §12, §17, branch `aias-6.0-preview` @ f59d4d4).

## 0. Phase identity

| Field | Value |
|---|---|
| PHASE_ID | v1.15 |
| PHASE_TITLE | Sentiment on t4: the v1.11 instrument on the N3 search-off category answers |
| PHASE_TYPE | methodology extension (scoring of collected answers; paid judge calls only; no new answer collection) |
| PREREG_TAG | v1.15-prereg-r1 (at lock) |
| INSTRUMENT | v1.11, tag `v1.11-prereg-r1` (commit 62e2d38; anchor 97c26be), applied unchanged |
| ANSWERS | t4 = v0.42 (tag `v0.42-prereg-r1` → 58d1891, locked 2026-11-10 20:52 CT); raw answers read at tag `v0.42-acquisition-locked` |
| OUTPUT FOR THE PREVIEW | `osf/methodology/v1_15/outputs/s_t4_v1_15.csv` (S_t4 per unit, rated flag) and `v1_15_verdicts.json` (§9) |
| LABEL | AI-judged; provisional until Sentiment Paper B (human labels on archived windows) |

**Number.** v1.15 is free: no branch, local or remote, and no tag named `v1.15*` (`git branch -a`, `git tag -l`, `git ls-remote --heads --tags origin`, 2026-11-11 ~02:45 UTC), and no folder `methodology/v1_15` on OSF (read-only listing of node ec6wh, `lock/osf_list_v1_15.py`, same time; the root folder `v15` is phase v0.15). A legacy roadmap copy in `kickoffs/aias_roadmap_ssot.md` (line 86 on every current branch) names "v1.15 — Four-component composite calibration methodology"; that numbering is already superseded (its v1.12–v1.14 lines are not the studies now carrying those numbers), as v1.11 §0 recorded for v1.9's forward reference. The calibration keeps its own, not yet numbered, pre-registration.

## 1. Why this study exists

The AIAS 6.0 Preview shows up to six labelled scores per brand on panel N3 (Claude Fable 5.2, GPT-6 Astra, Gemini 4 Argon) in the t4 week. v1.11 scores Sentiment on the archived legacy-panel waves only, and v1.14's anchor records `"score_defined_on_N3_at_t4": false` for Sentiment (Preview §3.4). The Preview therefore needs "a separate, small pre-registration that applies v1.11's locked instrument unchanged (window rule, judge, prompt, scale, rating floor) to the t4 N3 S0 category answers, locked before its first judge call" (Preview §3.4). If S_t4 is not scored by the Preview's data lock (Dec 11), the Preview falls back to v1.11's legacy-panel reading (Preview §3.4, Rule; §17 choice 1 (b)).

This study adds no instrument, threshold or rule of its own beyond what one wave on a new panel requires (§5.2), and those additions are stated as such.

## 2. Which t4 answers are judged, and why

**Judged: the S0 category answers (Phase B, search off) of N3: 3 models × 30 questions (6 per omnibus category) × 3 runs = 270 answers, 54 per category, after v0.42's own analysis-set rules.**

- **S0 only.** The Preview's Sentiment input is "t4 category answers S0" (Preview §3, table row Sentiment; §2 Condition: search off for Presence, Consistency, Ranking, Sentiment and Coverage). Its search-on sensitivity SH replaces only P, C\* and R\* (Preview §10), so no S1 Sentiment score is used anywhere. S1 answers are not judged (it would roughly double the cost for no pre-registered use).
- **Category answers only.** The t4 brand questions (Phase A) of v0.19–v0.22 are yes/no recognition probes, which v1.11 excludes by rule (v1.11 §2, "yes/no recognition probes"). The 24 v0.23 Phase A answers per model are open recognition texts (v1.11's block R); the Preview does not use a recognition score, and H8 (the only test on R) is SECONDARY in v1.11; they are not judged (open question O5).
- **Analysis set** (v0.42's rules, copied verbatim from tag `v0.42-prereg-r1` and checked by test): one record per call (`code_t4_v0_42.dedupe_calls`: the last answered attempt); answered = status ok, non-empty text, no error (`is_answered`); calls outside the r2 design excluded (`score_v0_42.in_design`); an answered call whose served model is neither the requested ID nor a dated snapshot of it excluded (`served_ok`); **drop rule:** a model whose answered S0 calls (Phase A + B) are below 90% of its 202 expected is dropped from S0 (`DROP_SHARE = 0.90`, `EXPECTED_PER_MODEL_COND["S0"] = 30 * 3 + 112`). The drop rule's outcome is recorded in `u0_v1_15.json`; a dropped model's answers are not judged (the Preview's MQ_Panel reads the same rule).
- **Exclusions (COI).** No brand is removed, consistent with v1.11 (§14 and sensitivity SD there) and the Preview (sensitivity SA): Denon (v0.19; owned by Harman International since 2025-09-23; §13) stays in the registry and in the primary analysis, and every statistic of §5 is also reported without the Denon unit (sensitivity SD). The string screen of v1.11 DEVIATIONS Entry 0 (same 22 terms) run on the five omnibus registries that t4 codes (`scripts/coi_screen_v1_15.py` → `prereg/coi_screen_v1_15.json`; 112 brands: 16 + 4 × 24) matches **Denon (v0.19) only**: t4's registries contain no Harman brand (scope as stated in v1.11 DEVIATIONS Entry 0). The v0.22 supply relationships are declared (§13), not exclusions.

## 3. Units (v1.11 §4.1, F rules, unchanged)

- **Mention record:** the certified one. For every judged answer, the brands it names are those coded `mentioned = 1` in v0.42's coded Phase B table (`osf/v42/data/coded/<sub>_phase_b.csv`, written by `code_t4_v0_42.py` with each substrate's certified t1 functions), exactly as v1.11 uses the certified record for its F block. A judged answer without a complete row set (one row per registry brand) halts; a coded brand outside the registry halts.
- **Window:** v1.11's brand-block window (`score_v1_11.build_window`, aliases from v1.10's registry loader, matching on the whole answer, cap 1,500 characters), one per (answer, brand). Extraction misses are counted; above 5% of a category's mentions the run halts before any judge call.
- **Cap:** at most 36 windows per brand × answer set × wave (seed 111001, round-robin over answering models; `score_v1_11.cap_windows`). On t4 each category has 54 answers, so the cap can bind (on v1.11's archive it could not for F); the Preview's own cost scenarios assume it (§12).
- **Judge coverage:** J1 and J2 judge every judged window (v1.11's F rule). Self-consistency: a fixed 5% sample (seed 111003, `selfcon_sample`), judged twice by each judge. No Paper B sample is drawn (Paper B validates on archived windows; Preview §13 item 6).
- **U0** (`score_v1_15.py --build-units --raw-ref v0.42-acquisition-locked --coded-ref <v0.42 coded commit>`) is run after t4's acquisition lock and before any judge call; every input is read from the git object store and logged with its git blob and SHA-256. The unit table's SHA-256 is fixed in `u0_v1_15.json` and checked by the judge script before every run. U0 is pre-judge data handling, not a model call; if it is run after the lock it is logged in DEVIATIONS as an ex ante step (no valence exists then).

## 4. Judge (v1.11 §4.2, unchanged) and availability

J1 **Claude Opus 5.5** (`claude-opus-5-5`, Anthropic Message Batches API), J2 **GPT-6.1 Sol** (`gpt-6.1-sol`, OpenAI Batch API, `/v1/responses`), alternate Gemini 4 Argon (`gemini-4-argon`, synchronous). The judge prompt (`osf/methodology/v1_11/prereg/judge_prompt_v1_11.md`), request, call parameters (no sampling parameter; effort "low"; output cap 4,096 tokens including reasoning; prompt-only JSON; no tools), served-model check, blinding, parsing, invalid-output retries (2), JUDGE_FAIL (> 2% of a category's units per judge halts before scoring), UNJUDGED and the phase order (A = all t4 windows, J1 and J2 in parallel, shuffled with seed 111000; A2 = repeats) are v1.11's code, imported unchanged (`scripts/score_v1_11.py`, `scripts/judge_v1_11.py`, git blobs 5e46e863… and 85ad069c…, equal to tag `v1.11-prereg-r1`; asserted by test).

**Availability, re-verified on the vendors' pages (2026-11-11, ~02:50 UTC = Nov 10 evening CT):**
- Claude Opus 5.5: Anthropic's model-deprecations page lists `claude-opus-5-5` as **Active**, deprecated N/A, "Tentative retirement date: Not sooner than September 22, 2027" (https://platform.claude.com/docs/en/about-claude/model-deprecations). Pricing page: base $4 / $20, **Batch $2 / $10** per MTok; not marked deprecated (https://platform.claude.com/docs/en/about-claude/pricing).
- GPT-6.1 Sol: OpenAI's model page lists Batch (`v1/batch`) among the endpoints, reasoning effort low, medium (default), high, xhigh, max, Standard $2 / $10 with batch "50% lower" (= $1 / $5), no deprecation date (https://developers.openai.com/api/docs/models/gpt-6.1-sol). OpenAI's deprecations page (latest entry dated 2026-11-10) lists no gpt-6 model as deprecated (https://developers.openai.com/api/docs/deprecations).
- Both judges are available; **no replacement is needed.** v1.11's own replacement rule stands: the alternate replaces J1 or J2 only if that judge cannot be used (unavailable or retired before its run ends, or a served-ID failure on its calibration calls), recorded before any further call; it judges all of the replaced judge's units; the replaced outputs are kept, never scored (v1.11 §4.2, `judge_v1_11.replace`).
- These checks are repeated on the lock day and on the first run day; a change is a DEVIATIONS entry before any call.

## 5. Tests, thresholds and verdict rules (v1.11 §5 re-applied to t4)

### 5.1 What is unchanged
Unit score u = 25·(valence + 2); S = mean u over a brand's valid J1 units in the category; **rated only with n ≥ 6** (v1.11 §4.3–4.4). ρ_w = pooled within-category Spearman on centred ranks (v1.10's function). A category enters with ≥ 4 units; a statistic is UNDETERMINED with < 20 units or < 3 categories. Bands: |ρ| ≤ 0.30 CONFIRMED, ≥ 0.50 FALSIFIED, between MARGINAL. Noise guard: H1 or H4 FALSIFIED → H2, H3, H5 reported as UNDETERMINED. 95% bootstrap intervals (units resampled within category, 10,000 draws; seed 115020, new for v1.15).

### 5.2 The five main tests on one wave
| Tag | Statistic (t4, N3, S0) | CONFIRMED | FALSIFIED |
|---|---|---|---|
| H1_t4 Judge agreement | Krippendorff α (ordinal) on valence over every window with valid J1 and J2 outputs; brand ρ_w(S_J1, S_J2), groups = category | α ≥ 0.667 AND ρ ≥ 0.80 | α < 0.50 OR ρ < 0.60 |
| H2_t4 Sep. Presence | \|ρ_w(S, P_S0)\| | ≤ 0.30 | ≥ 0.50 |
| H3_t4 Sep. Consistency | \|ρ_w(S, C\*_S0)\| | ≤ 0.30 | ≥ 0.50 |
| H4 Stability | — | not testable: t4 is one wave | — |
| H5_t4 Sep. Ranking | \|ρ_w(S, R\*)\|, R\* = v1.11's definition: v1.10's selected statistic MNP, lead-item extractor, floor 6, computed with v1.10's code on the same answers | ≤ 0.30 | ≥ 0.50 |

- **Single wave.** v1.11's three-wave rule (≥ 2 determined waves) cannot apply to one wave; H2_t4, H3_t4 and H5_t4 use v1.11's per-wave statistic, floors and bands at the t4 wave (a "single-wave" verdict; the rule's literal output would be UNDETERMINED by construction).
- **H4** has no t4 analogue: v1.11's H4 is t1 → t2 on the legacy panel. Judging t5's answers to test t4 → t5 is not in this design (open question O2).
- **P_S0, C\*_S0** are the Preview's shared N3 definitions, read from v1.14's Stage 1 units (`stage1_v1_14.json`, `units[]`: `P_S0`, `C_star_S0`), the values the Preview's MQ_Parity checks; a unit-key mismatch with the 112 units halts. **R\*** (MNP) is computed only after v1.14's Stage 1 output exists (the program's rule: no Ranking statistic on a t4 answer before v1.14 Stage 1); until then H5_t4 is PENDING. The Preview's Ranking score is v1.14's modal position; its R\* × S pair is the Preview's own S-test (seed 600006), not this one.
- **Relation to the Preview.** The Preview tests P × S, C\* × S and R\* × S as its own PRIMARY S-tests on its own floors (≥ 5 units per category, ≥ 30 pooled; Preview §2, §6.2) and reads Sentiment's gate from v1.11's archived H1–H5 (Preview §4.1; choice 6: all five CONFIRMED = PASS). This study's H2_t4, H3_t4 and H5_t4 are reported as v1.11's tests on t4; **the Preview's verdicts govern the profile**, and both are printed where both exist.

### 5.3 The study's own checks (the condition of Preview §4.1)
**OK** if no halt fired (extraction misses ≤ 5%, JUDGE_FAIL ≤ 2%, every frozen-input hash matches) and H1_t4 is CONFIRMED; **FLAGGED** if H1_t4 is MARGINAL (all S_t4 values carry the flag, v1.11 §5 H1 consequence); **FAILED** if H1_t4 is FALSIFIED or UNDETERMINED or a halt fired (S_t4 is then delivered with that label and the Preview applies its own rule).

### 5.4 Gate reading on t4 (for information)
The Preview's §4.1 rule applied to (H1_t4, H2_t4, H3_t4, H4, H5_t4) is written to the output; with H4 not testable it reads UNDETERMINED at best. It never changes the Preview's gate, which uses v1.11's archive verdicts.

### 5.5 Sensitivities and descriptives (never change a verdict)
SD: every statistic of §5.2 without Denon (v0.19). SU: uncentred ranks. α over windows both judges say refer to the brand; κ on `evaluative`; confusion J1 × J2; self-consistency (exact agreement per judge, flagged below 0.90); served-model and finish-reason counts; S distribution per category; mean u by answering model; E (evaluative share) and NV.
**Comparison with v1.11's archive (descriptive; the Preview defines none beyond its sensitivity SG):** H1 α and brand ρ on t4 beside v1.11's H1; S_t4 against v1.11's S at t3 for units rated in both (ρ_w, cross-panel, legacy six vs N3); median S per category on both panels. Labelled exploratory, never a verdict.

## 6. Window rule (paid calls)

One paid collection at a time on the collection machine; never November 17–21. A batch is submitted only if its whole 24-hour processing window lies inside an allowed window (v1.11's batch rule, `judge_v1_11.blackout_within`):
- **(a)** from t4's completion (tag `v0.42-acquisition-locked` on origin; its U0 and this study's lock anchored) to **2026-11-14 00:00 UTC**, when Coverage's collection starts — so the last batch is submitted by 2026-11-13 00:00 UTC;
- **otherwise (b)** from t5's completion (its acquisition tag on origin) and not before **2026-12-06 00:00 UTC**, to **2026-12-10 00:00 UTC** — last batch submitted by 2026-12-09 00:00 UTC, so that S_t4 exists before the Preview starts on Dec 11.
A run not finished when (a) closes stops and resumes in (b) with the same unit table and plan. The script also refuses while any other collection or judge process runs (including `judge_v1_11.py`, whose own run starts no earlier than 2026-11-22 06:00 UTC) and requires the operator's attestation (`--no-other-collection "<who, when>"`). If neither window is reached, S_t4 does not exist at the data lock and the Preview's fallback (b) applies.

## 7. Cost, cap and pause

**Planning estimate** (`score_v1_15.py --cost` → `prereg/cost_estimate_v1_15.json`), from v1.11's locked model: batch prices Claude Opus 5.5 $2 / $10, GPT-6.1 Sol $1 / $5 per million tokens in / out (read 2026-11-10; re-read 2026-11-11, §4); o200k request tokens × 1.30 (Anthropic) and × 1.10 (OpenAI); output 100 visible + r reasoning tokens; both judges on every window plus the 5% repeat; × 1.15 overhead. Inputs from locked files: F windows 2,781 over 540 answers = 5.15 per answer (`u0_v1_11.json` → `units.by_block.F`); F mean request 768.0 o200k tokens, max 1,009 (`token_counts_v1_11.json` → `by_block.F.tokens_mean`, `tokens_max`).

| Scenario | Windows | Calls per judge | Tokens in | r = 0 | 176 | **270** | 375 |
|---|---|---|---|---|---|---|---|
| archived density (270 × 5.15) | 1,390 | 1,460 | 768 | 7.29 | 11.72 | **14.09** | 16.73 |
| same, request at the 1,050 bound | 1,390 | 1,460 | 1,050 | 9.04 | 13.47 | 15.84 | 18.49 |
| cap binds for all 112 units (112 × 36) | 4,032 | 4,234 | 768 | 21.14 | 33.99 | **40.86** | 48.53 |
| same, request at the 1,050 bound | 4,032 | 4,234 | 1,050 | 26.22 | 39.07 | 45.94 | **53.61** |

US$ with overhead. The four Preview rows (§12: $14.09, $18.49, $40.86, $53.61) are reproduced exactly (tested). In the largest scenario the projection stays under the $80 pause while mean reasoning is ≤ about 806 tokens per call and under $100 while ≤ about 1,080.

**Hard cap US$100 and pause at US$80, from recorded usage, for v1.15 alone** (its own raw file), enforced by v1.11's guard unchanged: worst case of every call and batch reserved before sending (input bounded by the request's UTF-8 bytes, output at the 4,096-token cap, batch price); spend = the tokens each response reports at list batch price, cache discounts not counted; a timed-out call counts at its worst case; at $80 nothing more is sent until `--approve-past-pause "<who, when>"`; 30,000 calls at most. Binding projection after the first 200 calls per judge: v1.11's reductions touch only early-category units, which t4 does not have, so none applies; if the projection passes $80 the run continues under the guard and pauses at $80 of recorded spend.

## 8. Run order and lock
Content lock → `score_v1_15.py --lock-manifest` → commit → tag `v1.15-prereg-r1` → push → `lock/write_anchor_v1_15.py --osf-deposit "<OSF path>"` → commit the anchor → OSF deposit of `prereg/` and `anchor/`, SHA-256 verified (`LOCK_STEPS.md`). After t4's acquisition lock and v0.42's coded tables: U0 → `judge_v1_15.py --dry-run` → `--run` in window (a) or (b) → `--freeze` → Stage J (JUDGE_FAIL, S_t4, H1_t4, self-consistency; reads no P, C\* or R) → Stage C (after v1.14 Stage 1: H2_t4, H3_t4, H5_t4, SD, descriptives) → outputs. One-shot scoring.

## 9. Outputs (for the Preview's data lock, its §11.2 item 6)
`outputs/s_t4_v1_15.csv`: substrate, brand (unit key as in v1.14's `units[]`), S_t4, rated (n ≥ 6), n_valid, E, NV, n_refers_false, n_judge_fail, n_unjudged; one row per 112 units (NOT RATED rows included). `outputs/v1_15_verdicts.json`: own checks (§5.3), H1_t4–H5_t4 with statistics, gate reading (§5.4), sensitivities, descriptives, and the SHA-256 of the CSV.

## 10. Limitations
AI-judged and provisional; Paper B validates the instrument on archived windows, not the t4 scores. One wave: no stability test on N3. Three answering models, one per provider; every judge provider also supplied an answering model (self-preference is a v1.11 SECONDARY test, H9, reported descriptively here). The window cap can bind on t4 (54 answers per category), so S for the most-named brands rests on a seeded 36 of their windows. Judges run up to four weeks after the answers were collected (window (b)); the judge models are the same.

## 11. Deviations policy
`anchor/DEVIATIONS.md` opens with Entry 0 (ex ante). After the lock, every change gets an entry (id, date, ex ante / ex post, what, why, effect); a frozen-input hash mismatch halts; a scorer fix only restores a rule as written, with results before and after; judges, parameters, thresholds, floors, seeds, the unit rule and the window rule do not change; a failed check is published with the same prominence as a pass.

## 12. Open items before the lock (r0 → r1)
O1 Stage J / Stage C command-line glue and the output writers (§9) on top of the tested library functions; a replica dry run. O2 H4 on N3: not testable (default) vs judging t5's S0 answers in window (b) for a t4 → t5 test (roughly doubles the cost; would need its own scenario under $100). O3 t5's acquisition tag name (`v0.45-acquisition-locked` assumed; t5's numbering is pending in the roadmap) and its start date (this text uses Dec 6 as given by the runner; STATUS records a v0.45 r0 window from Thu Dec 3). O4 The coded-table commit of v0.42 to pass as `--coded-ref`. O5 Judging the 72 v0.23 open-recognition t4 answers (block R; not needed by the Preview).

## 13. Declarations

### Conflict of interest {-}

The author is Director, Corporate Brand Creative and Governance at Samsung Electronics America. This study judges answers collected against brand registries fixed in earlier phases (v0.19–v0.23); it performs no new brand selection, and each registry carries its source-phase conflict-of-interest handling forward unchanged. Two items of record apply, quoted from the latest locked pre-registration, v0.42 (`osf/v42/prereg/PRE_REGISTRATION_v0_42.md`, Declarations, tag `v0.42-prereg-r1`): "In the automotive registry, Samsung subsidiaries hold tier-2/3 component supply relationships with several registry brands — Harman International (audio systems), Samsung SDI (battery cells), and Samsung Display (infotainment) — characterized in the source phase as non-competitive, with no brand-level overlap, and imposing no operational restriction on registry composition (v0.22 Declarations; screened in v0.22 DEVIATIONS Entry 0, Part B). In the audiophile-headphones registry, AKG was substituted with Denon before the v0.19 pre-registration lock because AKG's parent, Harman International, is a Samsung subsidiary. Correction (November 10, 2026): Denon, which replaced AKG in the v0.19 registry, has itself been owned by Harman International, a wholly owned subsidiary of Samsung Electronics, since September 23, 2025, when Harman completed its acquisition of Sound United from Masimo; the v0.19 headphones registry therefore includes one Samsung-group brand. The substitution did not achieve its purpose, and this was not noticed until November 10, 2026." In this study Denon remains in the registry and in the primary analysis, and every statistic is also reported without the Denon unit (sensitivity SD). A string screen of the five registries (§2) matched Denon only. Valence judging is fully automated against the locked registries and units, and this pre-registration is locked and deposited before any judge call. Samsung Electronics had no role in the design, conduct, analysis or reporting of this work.

### Funding {-}

Self-funded.

### Ethics {-}

Not applicable; no human subjects (answers of large language models judged by large language models).

## Use of AI tools {-}

During the preparation of this work the author used AI tools (Anthropic's Claude) to assist with study design, analysis and writing. The author reviewed and edited all content and takes full responsibility for it.
