# AIAS v1.11 — Sentiment, Paper A: instrument, cross-category baseline, separability gate

**Status: DRAFT r0 (Nov 10, 2026). NOT LOCKED.** Branch `v1.11` (from `aias-2.0` @ 894ccee). Planned tag at lock: `v1.11-prereg-r1`, pushed and OSF-deposited (`osf/methodology/v1_11/prereg/`) **before the first judge call**. Items marked **TODO** or **TO VERIFY** must be settled by the main runner before the lock (§12).

Methodology lock, re-analysis only: no new answer collection. The only paid model calls are the judge calls of §4, run after the lock, under the hard cap of §8. Structure follows `osf/methodology/v1_9/prereg/` (content module: lineage, data, components, scoping look, fixed rules, hypotheses, descriptives, predictions, limitations, deviations).

Files: this document; `judge_prompt_v1_11.md` (exact prompt and output schema); `feasibility_v1_11.md` (development-sample parsing count); `../registries/INPUTS_MANIFEST_v1_11.json` (frozen inputs with git blobs); `scripts/score_v1_11.py` (+ `scripts/test_score_v1_11.py`).

## 0. Phase identity

| Field | Value |
|---|---|
| PHASE_ID | v1.11 |
| PHASE_TITLE | Sentiment Paper A: AI-judged valence instrument, cross-category baseline, separability from Presence, Consistency and Ranking |
| PHASE_TYPE | methodology_lock (re-analysis of archived answers) |
| PREREG_TAG | v1.11-prereg-r1 (at lock) |
| PRESENCE_LOCK | v1.6 (P = 100·(1/3)(C_P/6 + 2·π̂), π̂ = recall mentions/36) |
| CONSISTENCY_LOCK | v1.8 φ; v1.9 C* = 100(1 − φ/7.2), rated only with ≥ 6 total mentions |
| RANKING | "the Ranking score locked in v1.10" — leg active only if v1.10 locks first (§5, H5) |
| LABEL | Sentiment is **provisional** (AI-judged) until Paper B's human-label validation (SVA MPS Branding students, labels due ~Jan 22, 2027) |
| FEEDS_FORWARD | Paper B (human validation; stability and phrasing studies); the component-calibration step after Ranking and Sentiment |

**Naming reconciliation (TODO, runner).** v1.9's locked content module lists `FEEDS_FORWARD: "v1.11 (two -> three-component calibration, after RS)"`. Pablo's Nov 9 queue and the Nov 10 archive inventory assign v1.11 to Sentiment Paper A (v1.10 = Ranking Paper A). This draft follows the queue; the lock record must state that v1.9's forward reference is superseded and name the version that now carries the component calibration.

## 1. Lineage

Presence: v1.2–v1.6 (SSRN 6761698, 6797679, 6799479, 6810758, 6816340); AIAS 1.0 synthesis 6817841; construct validity v0.29 6870778. Consistency: v1.7 6878818 (CV-CPC falsified — the instrument moved with how often a brand is named), v1.8 6963359 (φ), v1.9 (C*; tag v1.9-prereg-r1), v0.34 6915458 (t1→t2), v0.41 (t3). AIAS 2.0 (Nov 10, 2026; branch `aias-2.0`): Consistency separable from Presence. Ranking: v1.10 (drafted in parallel; not locked at this draft).

**Prior valence material in the record (declared).** (a) The early-category enriched files carry a v0.8 extractor column `sentiment_summary` (answer-level counts `pos|neu|neg`, all brands of the answer pooled; `enrich.py`/`extractor.py`). It is not brand-level, is not the v1.11 instrument, and was not used to design anything here. (b) `cross_tab_valence.py` (Phase 2) codes a different construct (phantom-brand reference type: live recommendation, status correction, …). (c) The v0.34 recognition judge (claude-sonnet-4-5, 144 calls) coded v0.23 recognition answers for recognition, not valence (the same holds for any v0.41 coding of t3; runner to confirm). **TODO (runner):** confirm no brand-level analysis of `sentiment_summary` was ever reported; if one was, cite it here.

## 2. Data (frozen; full list with blobs in INPUTS_MANIFEST_v1_11.json)

All inputs are tracked files on `aias-2.0` @ 894ccee; each is pinned by git blob and sha256. Counts are from `archive_inventory_scan.csv` (Nov 10, 2026) and are re-asserted by the loader at lock.

| Block | Sets | Panel | Answers with text | Unit |
|---|---|---|---|---|
| R — v0.23 open recognition ("what do you know about X") | t1 `osf/v23/data/v23_phase_a_raw.json`; t2 `osf/v34/data/v23/…`; t3 `osf/v41/data/v23/…` | legacy six | 144 × 3 = 432 (24 brands × 6 models × 3 waves) | whole answer |
| F — omnibus frames, five substrates (v0.19 headphones, v0.20 skincare, v0.21 cosmetics, v0.22 automotive, v0.23 premium spirits) | Phase B files at t1 (`osf/v19..v23`), t2 (`osf/v34/data/…`), t3 (`osf/v41/data/…`) | legacy six: Opus 4.5, Sonnet 4.5, GPT-4o, GPT-4o mini, Gemini 2.5 Flash, Flash Lite | 36 × 5 × 3 = 540 | mention window |
| E — early category studies, six-model sets | v0.9 PM software, personal finance, olive oil, running shoes, skincare (288 each); v1.0 household retail (250 of 288 with text); v1.0 kitchen knives (288); v0.14 premium tea (288) | claude-sonnet-4-6, claude-opus-4-7, gpt-5.4-mini, gpt-5.5, gemini-2.5-flash, grok-4-1-fast | 2,266 | mention window |

Units on which P and C* exist: the 112 omnibus brand units × 3 waves, from `osf/methodology/v1_9/v1_9_unit_table.csv` (columns `wave, substrate, brand, mentions, P, C_star, …`; 112 rows per wave t1, t2, t3) — LOCKED INPUT, read only after all judge outputs are frozen (§8).

**Excluded, with reason (fixed):** v0.24 recognition (cut at 300 characters); `sandbox/tcl_prep` (not a program study; TVs are a Samsung-competing category); yes/no recognition probes (v0.18–v0.22, v0.26, v0.28, v0.32 A); the interrupted v0.23 t3 partial (`osf/v41/data/_interrupted_v23_2026-11-09/`, superseded by the complete rerun); v0.10 Mint subset (duplicates v0.6/v0.9 text); v0.17, v0.18 and the v0.5 archive (**development sample**, used for the parsing-only feasibility count; never in a confirmatory statistic). **Reserved for Paper B / later pre-registrations (not analysed in v1.11):** v0.6 two-model first pass and v0.16 kitchen knives (second kitchen-knives design, 181 of 515 cells empty); v0.24 B, v0.28 B frames; v0.32 arms A/B (model-version pair); v0.38, v0.39 (newest models, search on/off).

Missing cells carried as recorded: household retail 250 of 288 with text (38 empty, no filled file); no Paper A input has any other recorded gap.

## 3. Scoping look (development sample only; declared)

`osf/methodology/v1_11/scoping/feasibility_v1_11.py` (Nov 10, 2026) ran the §4 window rule on the development sample (v0.17 A/B, v0.18 B, v0.5 archive; 127 answers). Parsing only: no model call, no valence, nothing on P, C*, Ranking, separability or stability, and no confirmatory input was parsed. Results in `feasibility_v1_11.md`: 4.0–6.2 windows per frame or early-design answer; median window 159–271 characters (~50–85 tokens); 1 of 557 windows at the 1,500-character cap; 2–9% "bare" windows (the brand's segments carry fewer than 4 other words — list-only mentions, expected to judge as neutral). The first window rule (naming sentences only) was revised on this sample because list formats put descriptors in sub-bullets that do not repeat the brand name; the revision (brand block, §4.1) is the rule locked here.

## 4. Fixed rules

### 4.1 Unit

- **R (recognition):** the whole answer, one unit per (brand, model, wave); cut at 16,000 characters (flagged; the development sample's maximum was 2,707).
- **F and E (long-form):** one **mention window** per (answer, brand) for every registry brand the answer names. Which brands an answer names is taken from the program's certified mention record, not re-extracted: for F, `osf/v41/scripts/score_v41.load_wave` (the extraction behind v1.9's `mentions`; so n here equals v1.9's `mentions` for every omnibus unit); for E, the `brands_canonical` column of each enriched file.
- **Window (brand block):** the answer is split into segments (newline or two or more spaces; inline headings, bullets and numbered items; then sentences). The window is every segment naming the brand (registry aliases; case-insensitive, accent-folded, word-bounded), each followed by up to 4 continuation segments, stopping at a heading or list label or at a segment naming another registry brand; gaps are marked `[...]`; capped at 1,500 characters (whole segments; a first segment longer than the cap is cut at it).
- **Extraction miss:** a certified mention with no locatable window is not judged and is counted. If misses exceed 5% of a set's mentions, the run halts before scoring and the runner reports.
- **Cap per brand:** at most 36 windows per brand × answer set × wave (seed 111001, round-robin over answering models). A no-op for F (maximum 36 by design); it limits cost for brands named in most of an early set's 288 answers.

### 4.2 Judge

- **J1 (primary):** the newest generally available flagship of provider A. **J2 (reliability):** the newest generally available flagship of provider B. Candidate IDs, **TO VERIFY at lock from the vendors' current model documentation** (availability, GA status, dated snapshot ID, support for temperature 0 and JSON schema output): J1 Anthropic — `claude-opus-5-5` (the ID recorded in v0.39 arm C, Nov 8, 2026); J2 OpenAI — `gpt-6-astra` (recorded in v0.39 arm C); alternate Google — `gemini-4-argon` (recorded in v0.39 arm C). This draft does not assert that any of these is available or is the flagship.
- **Call parameters (fixed):** temperature 0; maximum output 200 tokens; no tools, no web search; extended reasoning off (if a model cannot switch it off, the vendor's minimum, recorded); schema-constrained JSON output where the vendor supports it, otherwise prompt-only; the prompt text is identical either way (`judge_prompt_v1_11.md`). The exact model ID returned by each call is recorded with the output.
- **Blinding:** the judge sees brand, category, the question, the text type and the text; never the answering model, the wave, the answer set, or any P, C* or Ranking value. Call order is shuffled (seed 111000).
- **Scale:** valence −2…+2 with the anchors in the prompt, plus `refers_to_brand`, `evaluative`, `mixed` and a ≤ 20-word evidence quote.
- **Invalid output:** up to 2 retries with identical input; then JUDGE_FAIL (excluded, counted). JUDGE_FAIL above 2% of any set's units halts the run before scoring.
- **Coverage:** J1 judges every unit. J2 judges every R and F unit and a 10% stratified random sample of E windows (by category × answering model; seed 111002). J1 re-judges a 2% random sample (seed 111003) for a determinism check (exact valence agreement ≥ 0.90; below it, flagged in Paper A, not a halt).

### 4.3 Near-neutral text

Being named, listed or recommended by inclusion is not evaluation; plain facts are neutral; reported third-party judgements (awards, ratings, recalls, controversies) count as evaluation (prompt rules 2–4). Non-evaluative units are scored **0 (= 50 on the 0–100 unit scale) and kept in the score** — a neutral description is an outcome, not missing data; dropping it would make S rest on the few evaluative units. Units with `refers_to_brand = false` are excluded and counted. Two descriptives travel with S but are not the score: E = evaluative share; NV = mean unit score among evaluative units (reported only with ≥ 3 evaluative units).

### 4.4 Score and n floor

Unit score u = 25·(valence + 2) ∈ {0, 25, 50, 75, 100}. **S(brand, set, wave) = mean u over the brand's valid units**, each unit weight 1; scored on J1's outputs (J2 is for reliability only). **S is rated only if n ≥ 6 valid units; otherwise NOT RATED** (no shrinkage). Justification: (i) mirrors v1.9's C* rule, and because F windows are counted exactly as v1.9's `mentions`, S and C* are rated on the same omnibus units — like is compared with like; (ii) six units is one model's full frame set; (iii) v1.9 showed that shrinking toward a midpoint by mention count ties a component to Presence (SHRINK failed K1), so the floor, not shrinkage, is used. For R, n = 6 means all six models described the brand in that wave.

The **AIAS Sentiment score is the long-form S** (F for the omnibus, E for the early categories). The recognition score S_rec (block R) is a second elicitation for one category, used for a floor-free separability check, a convergence check and Paper B's sample.

## 5. Hypotheses and decision rules

Statistic convention (as v1.9): ρ = rank correlation on **within-substrate (within-category) ranks, pooled** across substrates; units = brand × wave. Band verdicts use the program bands: **|ρ| ≤ 0.30 CONFIRMED separable; |ρ| ≥ 0.50 FALSIFIED; between MARGINAL.** Three-wave rule for omnibus separability: **CONFIRMED iff |ρ| ≤ 0.30 at all of t1, t2, t3; FALSIFIED iff |ρ| ≥ 0.50 at two or more waves; MARGINAL otherwise.** Minimum n: a wave is UNDETERMINED with fewer than 20 rated units pooled or fewer than 3 substrates with ≥ 4 rated units. A 95% bootstrap interval (brands resampled within substrate, 10,000 draws, seed 111020) is reported with every ρ; verdicts use the point estimate.

**Noise guard.** A noisy instrument is separable from everything. If H1 or H4 is FALSIFIED, H2, H3, H5, H7 and H8 are reported as UNDETERMINED (statistics shown as descriptive only).

| Tag | Tier | Statement | Statistic | CONFIRMED iff | FALSIFIED iff |
|---|---|---|---|---|---|
| H1_Judge_Agreement | PRIMARY (instrument gate) | Two flagship judges from different providers agree on valence. | Krippendorff α (ordinal) on valence, all units judged by J1 and J2; and ρ(S_J1, S_J2) on F units rated under both, waves pooled | α ≥ 0.667 AND brand ρ ≥ 0.80 | α < 0.50 OR brand ρ < 0.60 |
| H2_Sep_Presence | PRIMARY | Sentiment is separable from Presence (the v1.7 lesson: it must not move with how often a brand is named). | \|ρ(S, P)\|, F units with S rated, per wave | three-wave rule ≤ 0.30 | three-wave rule ≥ 0.50 |
| H3_Sep_Consistency | PRIMARY | Sentiment is separable from Consistency. | \|ρ(S, C*)\|, units with S and C* rated, per wave | three-wave rule ≤ 0.30 | three-wave rule ≥ 0.50 |
| H4_Stability_Short | PRIMARY | S keeps its brand order over ~3 weeks (t1 May 20–26 → t2 Jun 10). | ρ(S_t1, S_t2), F units rated in both; one-sided stratified permutation (t2 ranks permuted within substrate), 10,000 draws, seed 111011 | ρ ≥ 0.50 AND p < .05 | ρ < 0.30 OR p ≥ .05 |
| H5_Sep_Ranking | PRIMARY, **conditional** | Sentiment is separable from Ranking. | \|ρ(S, R)\|, R = the Ranking score locked in v1.10, F units rated under both, per wave | three-wave rule ≤ 0.30 | three-wave rule ≥ 0.50 |
| H6_Stability_Long | SECONDARY | S keeps its brand order over ~5 months (t2 → t3 Nov 9). | as H4, t2 → t3, seed 111012 | ρ ≥ 0.50 AND p < .05 | ρ < 0.30 OR p ≥ .05 |
| H7_Naming_Frequency | SECONDARY | In the eight early categories, S does not track how often a brand is named. | \|ρ(S, n_named)\|, n_named = answers in the set naming the brand (`brands_canonical`); rated brands, within-category ranks pooled | ≤ 0.30 | ≥ 0.50 |
| H8_Recognition_Sep | SECONDARY | The floor-free recognition score is separable from Presence (v0.23, 24 brands). | \|ρ(S_rec, P)\| per wave | three-wave rule ≤ 0.30 | three-wave rule ≥ 0.50 |
| H9_Self_Preference | SECONDARY | J1 does not favour answers written by its own provider's models. | Δ = mean(u_J1 − u_J2) on J1-provider answers − the same on other answers (R + F) | \|Δ\| ≤ 5 points | \|Δ\| ≥ 10 points (then S is also reported without J1-provider answers) |

MARGINAL = otherwise, for every row. **H5 activation rule:** H5 is active only if tag `v1.10-prereg-r1` (or a later v1.10 prereg revision) is pushed **before** the v1.11 lock commit; the v1.11 lock then records the v1.10 tag, commit and the file defining R, and R is used exactly as v1.10 locks it (its own unit, floor and rated set). If v1.10 has not locked first, H5 is INACTIVE in v1.11 (no verdict) and the Ranking leg may only be tested under a later pre-registration. As an active H5's secondary row, |ρ(S, R)| is also reported within the eight early categories (band verdict), if v1.10 rates R there.

H1 consequence: FALSIFIED → Paper A reports the AI-judged instrument as not reliable; MARGINAL → all verdicts carry the flag. H4 is a reliability floor, not a claim that Sentiment is fixed; H6 allows real change over five months.

## 6. Descriptives (pre-specified, no verdicts)

1. Cross-category baseline: per category (13: 5 omnibus × 3 waves, 8 early) and per panel — brands rated, S median/IQR/min/max, E, NV; shares of non-evaluative, mixed, `refers_to_brand = false`, extraction misses, JUDGE_FAIL, bare windows.
2. Convergence: ρ(S_rec, S) in v0.23 per wave (rated in both).
3. Mean u by answering model, by frame / prompt type, by panel.
4. Sensitivity for H2/H3: NV in place of S; model-balanced S (mean of per-model means); J2-scored S.
5. Agreement detail: α per block (R, F, E); κ on `evaluative`; confusion matrix J1 × J2; determinism exact-agreement rate.
6. Exploratory only: answer-level agreement of J1 with the legacy `sentiment_summary` (early sets).

## 7. Judge calls, cost and the hard cap

Planning counts (exact counts are fixed at lock step U0 by the deterministic unit build; tokens estimated at 4 characters per token; fixed prompt ≈ 850 tokens; output ≤ 100 tokens):

| Block | Units (J1) | Input tokens per call | J2 |
|---|---|---|---|
| R | 432 | ≈ 2,100 (prompt + median 4,765-character answer) | all 432 |
| F | ≈ 3,350 (540 answers × 6.2 windows, the higher development rate) | ≈ 1,000 | all ≈ 3,350 |
| E | ≤ 12,700 (2,266 × 5.6, upper bound before the 36-window cap) | ≈ 1,000 | 10% ≈ 1,270 |
| Determinism | 2% of J1 ≈ 330 | as source | — |

Totals: ≈ 21,900 calls, ≈ 22.8 M input and ≈ 2.2 M output tokens; with 15% overhead for retries and estimate error, ≈ 25,100 calls, 26.3 M input, 2.5 M output. Cost (prices **TO VERIFY at lock**; the two judges are priced separately): ≈ **USD 195** at a planning price of USD 5 / 25 per million input / output tokens; ≈ USD 580 at a stress price of USD 15 / 75.

**Hard cap: USD 250 and 30,000 judge calls in total for v1.11** (J1 + J2 + retries + determinism). At lock the runner computes the projection at verified prices (`CostGuard.project`). If it exceeds the cap, reductions apply in this fixed order until it fits: (1) the E window cap 36 → 24; (2) J2's E sample 10% → 5%; (3) E judged on a seeded 50% of each set's answers (seed 111004). R and F are never reduced. During the run `CostGuard.charge` stops before any call that would pass the cap; unjudged units are reported as such and no further spending is authorised under this pre-registration. Vendor batch endpoints may be used if they return the same model and parameters (cost can only fall).

## 8. Run order

Before the lock: settle §12; fill J1/J2 IDs and prices; U0 — `score_v1_11.py --build-units` builds the unit table from the manifest inputs (deterministic, no model calls, no valence; the window count overlaps the Presence information already published, but no statistic is computed on it), records unit counts and the unit-table sha256 in the manifest, and draws the Paper B human-label sample (§9); `--dry-run` confirms the projection is under the cap; tests pass; content lock → commit → tag `v1.11-prereg-r1` → push → OSF deposit → both remotes verified.

After the lock: J1 and J2 runs → outputs frozen (hashes recorded) → H1 → only then `v1_9_unit_table.csv` (P, C*) and, if H5 is active, v1.10's R are joined → H2–H9 → descriptives → report. One-shot scoring; any change after the lock is a DEVIATIONS entry.

## 9. Paper B hand-off: human-label sample (design only; not executed in v1.11)

- **Draw at U0, before any judge call** (seed 111022), from the frozen unit table; file `prereg/human_sample_v1_11.csv` (TODO at U0), hashed in the manifest.
- **Size:** 40 units per category for the 13 categories (5 omnibus, F windows, t1/t2/t3 in equal thirds; 8 early, E windows) = 520 windows, plus 48 v0.23 recognition answers (2 per brand, different models and waves) = **568 units**.
- **Stratification:** within each category, equal allocation across the six answering models; across frames / prompt types as evenly as the cell counts allow; at most 3 units per brand per category; bare windows kept at their natural share.
- **Labelling:** the judge's instructions and scale verbatim (`judge_prompt_v1_11.md`, rules 1–7); each unit by two students independently, a third on valence disagreement; students blind to judge outputs, answering model, wave and any AIAS score. Estimated effort ≈ 14 labeller-hours (windows ≈ 30 s, recognition answers ≈ 3 min, two passes).
- **Hand-off:** the sample file, the instructions and a blank label sheet go to the SVA MPS Branding coordinator; labels due ~Jan 22, 2027. Validation thresholds are fixed in Paper B's own pre-registration before the labels are read; v1.11 Sentiment stays "provisional" until Paper B confirms it.

## 10. Predictions (written before any judge call)

H1 lean MARGINAL-to-CONFIRMED (valence with explicit neutral anchors; disagreement concentrated at 0 vs +1 on descriptive text). H2 lean MARGINAL: brands named often are also described more warmly in recommendation frames — this is the risk the gate exists for. H3 lean CONFIRMED (no mechanism links valence to between-model dispersion). H4 lean MARGINAL: R and F scores cluster at 50–75, which limits rank stability. H8 lean CONFIRMED. Most recognition units will be non-evaluative or +1.

## 11. Limitations

AI-judged and provisional until Paper B. The F rated set (n ≥ 6) restricts the Presence range, which can understate |ρ(S, P)|; H8 (floor-free) and H7 (early panel) are the checks. One judge pair; self-preference is tested (H9), not removed — every judge provider also supplied answering models. Two answering panels that are not the newest models; early sets have one wave each. S measures description in answers, not consumer sentiment; no behavioural validity is claimed. The window rule can miss evaluations far from the brand name and can carry a neighbouring sentence; Paper B's labels test the unit as well as the judge.

## 12. Open before the lock (runner)

1. Judge IDs: verify J1/J2 (and the alternate) against the vendors' documentation — GA flagship status, dated snapshot ID, temperature 0, JSON schema, reasoning off — and record them; verify per-token prices and rerun the projection against the USD 250 / 30,000-call cap.
2. v1.10: has `v1.10-prereg-r1` been pushed before this lock? If not, H5 is INACTIVE (§5). Record v1.10's R definition file if active.
3. v1.9 forward reference: v1.9 names v1.11 "two → three-component calibration"; record the supersession and the new version number for that step.
4. Loaders (TODO in `score_v1_11.py`): F mentions via `osf/v41/scripts/score_v41.load_wave`; E mentions via `brands_canonical`; registry alias lists per set (manifest); run U0 and record counts and the unit-table hash. **Three E files have no `brands_canonical` column** (household `results_v2_household_v1.0_merged.csv`, knives `results_v2_knives_v1.0_final.csv`, premium tea `results_v2_premium_tea_20260512_161817_filled.csv`): name the program's certified mention record for them (an enriched sibling file or the phase's derived mention table) and pin it in the manifest; if none exists, decide between dropping those sets and a registry string match fixed now.
5. Rank convention: align `rho_within` with v1.9's implementation (`osf/methodology/v1_9/scripts/score_v1_9.py`) so "within-substrate ranks pooled" is computed identically.
6. Confirm no earlier brand-level analysis of the legacy `sentiment_summary` exists (§1).
7. COI (Entry 0): carry forward the source phases' locked COI language verbatim from the source records; complete the screen of the eight early registries (draft string screen for "Samsung", "Harman", "JBL", "AKG": no match in any of the eight files; the runner confirms against the full subsidiary list and the source phases' own COI records).
8. Paper B: confirm the SVA sample size (568 units, ≈ 14 labeller-hours) with the coordinator; the date ~Jan 22, 2027 is the planning date.

## 13. Deviations

Entry 0 (ex-ante, COI + anchor). **COI screen:** no new brand selection; v1.11 re-uses the source phases' registries unchanged and carries their COI handling as recorded: v0.19 audiophile headphones — AKG was substituted with Denon before the v0.19 pre-registration lock (AKG owned by Harman International, a Samsung subsidiary, since 2016) (v0.19 DEVIATIONS Entry 1); v0.22 automotive — Samsung subsidiaries hold tier-2/3 component supply relationships with several registry brands: Harman International (audio systems), Samsung SDI (battery cells), Samsung Display (infotainment); characterized as non-competitive with no brand-level overlap; no operational restriction on registry composition was imposed (v0.22 DEVIATIONS Entry 0, Part B). Valence judging adds no brand choice; only registry brands are scored. `sandbox/tcl_prep` is excluded (TVs: a Samsung-competing category). Early-category registries: draft string screen found no Samsung, Harman, JBL or AKG entry; full screen before lock (§12.7). Samsung is disclosed only in the Declarations §COI of the paper. **Anchor preamble:** §12 settled → U0 → content lock → commit → tag `v1.11-prereg-r1` → push → OSF deposit → both remotes verified → only then the first judge call. Lock state: DRAFT r0 (not locked).
