# AIAS v1.19 — Coverage, Paper B (re-analysis): situation-set sensitivity, phantom brands, identity load and typology on Paper A's answers

AIAS™ Measurement Program — Third System™. Pre-registration **DRAFT r1** (2026-11-12). r0 (the same day, written by the AIAS runner's lane H) reached Pablo on Thu 2026-11-12 at about 7:40 am CT and was deposited by the runner on OSF in `methodology/v1_19/draft_r0` (both as reported by the runner, not checked by the lane that wrote r1); r0 stays unchanged beside this file. r1 adds the items r0 listed as missing (§17 item 7) and changes no hypothesis, threshold, estimand, seed, exclusion or decision rule (§18). **Not locked.** No Coverage answer exists: Paper A (v1.12) collects from Fri 2026-11-13, 6 pm CT (2026-11-14 00:00 UTC) at the earliest. No model was called and no statistic of this study was computed on real data while drafting (§9.4 lists everything that was read).

---

## For Pablo: what this is, in plain words

Coverage asks in how many buying situations AI models name a brand. Paper A (v1.12, locked Nov 10) builds the instrument (14 situations per category, three runs, three newest models) and decides whether Coverage is a separate part of the score. If Paper A passes, Paper B asks whether the result holds up and what structure it has. Five studies were planned for Paper B; four of them need no new model calls, because they can be computed from Paper A's own answers. This draft fixes those four in advance, so that they are real tests and not after-the-fact readings:

- **#32 Does the brand order depend on which situations we picked?** We re-split Paper A's 14 situations in all 64 balanced ways and check that brands keep their order, and that no single kind of situation (for example "with whom", which holds the gift situations) drives it.
- **#34 Phantom brands: which situations do they occupy?** Brands the models rarely name in general questions (the program's frozen "below the recall floor" list, 57 of 112) — are they tied to a few situations? And the five defunct car brands (Pontiac, Oldsmobile, Plymouth, Mercury, Saturn) — when a model names one anyway, in which situations?
- **#35 Identity load.** Brands that AI names mostly for cultural reasons ("popular", "iconic") rather than category reasons — are they named across fewer buying situations, and more in social and emotional ones?
- **#36 Typology.** Do brands have stable situation profiles (a "gift brand", a "budget brand") that repeat across different situations of the same kind, and do these profiles form types beyond big versus small?

**#33 (different question wordings) is not in this draft:** Paper A asks every situation in one wording, so wording stability needs a new paid collection and its own pre-registration (§4).

**If Paper A does not pass, none of this runs.** On PASS it runs; on MARGINAL it runs only if you say so in writing; on FAIL, UNDETERMINED or INSTRUMENT FAIL it is reported as "not run" (§1).

**Timing.** r0 reached you on Thu Nov 12 at about 7:40 am CT; under D10 it locks 24 hours later, Fri Nov 13 at about 7:45 am CT, before Paper A's first call (Fri 6 pm CT). Even if the lock slips, the tests stay confirmatory as long as it locks before Paper A's answers are coded and scored; the scorer refuses to run without this study's tag, and Paper A's scorer computes none of these statistics (§9).

### Decisions for you (each has a default; silence = default)

| # | Decision | Default | Alternative |
|---|---|---|---|
| D1 | Study number | **v1.19** (next free methodology number; §0) | `v1.12-paperB`, the v1.11-paperB naming precedent |
| D2 | If Paper A is MARGINAL | B runs only on your recorded decision; every verdict labelled "conditional on a MARGINAL gate"; the marginal leg's confirmatory re-test goes to #33's new collection, because the same answers cannot re-test it | B never runs on MARGINAL |
| D3 | #32 scope | Within-set sensitivity on Paper A's 14 situations now; the human-authored parallel set and buyer-weighted situations later, with a new collection (#32b) | Hold all of #32 for the parallel set |
| D4 | Fisker (car registry, "disruptor" cell) | Not counted as defunct; reported beside the five defunct brands | Count as defunct (Paper A §10 names it beside them) |
| D5 | Phantom definition for the main test | The frozen recall-floor flags (v0.31 archive; used by v0.33, v0.34, v0.35) | Defunct brands only (5 units; too few for a contrast) |
| D6 | Identity-load source | Newest-model (t4) identity load, same models as Coverage, v0.65 draft's formula; the published t1 IL-Direct as a sensitivity | t1 IL-Direct as primary |
| D7 | "Social and emotional" situations for #35's second test | with whom + how feeling | how feeling only |
| D8 | #36 main claim | Profile replication is the primary test; the cluster typology is secondary (the dry run's clustering missed three built-in types at this size) | Clustering primary, as v0.36 |
| D9 | #36 replication bands | CONFIRMED ≥ 0.20, FALSIFIED < 0.10 (set on synthetic data, §7.2) | v0.37's 0.30 / 0.15 |
| D10 | Lock time | 24 h after you receive it (r0 received Thu ~7:40 am CT, so Fri ~7:45 am CT), and in any case before Paper A's `--code` step | Lock now (the roadmap's "re-analyses lock immediately") |

---

## 0. Status, scope and lineage

| Field | Value |
|---|---|
| PHASE_ID | **v1.19** (proposed; D1) |
| PHASE_TYPE | methodology re-analysis, **no new model calls**, no spend; conditional on v1.12's gate (§1) |
| Branch | `v1.19`, from `v1.12` @ `a57f590` (v1.12's last commit, on origin; the way v1.16 was based on v1.14 @ `3129674` and v1.18 on v1.13 @ `1b58837`, the study whose code each reuses) |
| Status | DRAFT r1, local commits only; not pushed. r0 was sent to Pablo (Thu 2026-11-12, ~7:40 am CT) and deposited on OSF in `methodology/v1_19/draft_r0` by the runner (as reported by the runner) |
| Locks on | Pablo receives it → 24 h (D10) → r1 content lock → `prereg/LOCK_MANIFEST_v1_19.sha256` → commit → tag `v1.19-prereg-r1` → push → OSF deposit of `osf/methodology/v1_19/prereg/` and `anchor/` (SHA-256 verified) → `anchor/osf_anchor_v1_19.json` → only then may `score_v1_19.py --run` start, and only after Paper A's scored output exists (§9) |
| Inputs (all Paper A's, imported) | v1.12's locked scorer `osf/methodology/v1_12/scripts/score_v1_12.py` (SHA-256 `f7689898…` in v1.12's lock manifest; imported, not copied); Paper A's raw record, coded mention rows, `v112_verdicts.json` and `v112_unit_table.csv` once they exist; the probe file `prereg/probes_v1_12.jsonl` as locked |
| Other inputs (archived, frozen) | `osf/v31/data/v31_cpc.csv` (recall-floor flags, #34); `prereg/v0_22_registry.json` (cell D, #34); v0.42's coded t4 Phase B rows and `osf/v42/prereg/probes_v0_42.jsonl` channel labels (identity load, #35); `osf/methodology/v1_7/data/v1_7_cpc.csv` (t1 IL-Direct, #35 sensitivity) |
| Studies | #32, #34, #35, #36 of the Full study list (numbers as given in the runner's brief; the roadmap's Phase Q lists them as "CEP × CEP-set sensitivity", "CEP × Phantom Brand CEP-occupancy signature", "CEP × Identity Load moderator", "CEP regime / typology emergence"); #33 "CEP × prompt-phrasing variation" is deferred (§4) |

**Number.** v1.18 is the latest methodology number used. On 2026-11-12 at about 6:40 am CT no local or remote branch or tag matched `v1.19*` or `v1.2*` (`git branch -a`, `git tag`, `git ls-remote --heads --tags origin`), and neither the roadmap, `STATUS.md` nor `CLAUDE.md` mentions v1.19. Not checked: whether OSF node ec6wh has a folder `methodology/v1_19` (this lane makes no OSF call); check at r1. At r1: the runner reports that the folder exists and holds `draft_r0`, deposited Thu 2026-11-12 by the runner (not checked by the lane that wrote r1, which made no OSF call; §17 item 2). Precedent for the other name (D1): Sentiment's Paper B is `v1.11-paperB` (tag `v1.11-paperB-prereg-r1`), a human-labelling study.

**Lineage.** v1.12 §10 ("What Paper B inherits") lists, only after PASS or MARGINAL with Pablo's recorded decision: the frozen CEP sets, probe files, coder and scorer; per-answer mention tables; Cov and Cov\* per unit next to P and C\*; and the studies "CEP-set sensitivity (an independently, human-authored parallel set; leave-one-W-out; CEP weights from buyer data), phrasing (fixed list length, 'best for…' wording, second person, a market cue), phantom (v0.22 cell D and Fisker in situation answers; phantom-brand bands), identity load (situations by cue type against the registries' identity cells)", S1 Coverage, model-version stability and re-asks at t5/t6. This draft pre-registers the parts that need no new answer. The Consistency arc ran the same three questions as re-analyses: v0.35 (phantom × CPC), v0.36 (regime emergence) and v0.37 (identity load × CPC); their machinery and bands are reused where they fit (§5–§7).

## 1. Conditionality on Paper A's gate (binding)

Paper A's verdict is the field `paper_A_verdict.verdict` of `osf/methodology/v1_12/v112_verdicts.json`, written once by v1.12's scorer (v1.12 §3, GATE). This study reads it and nothing else decides:

| Paper A verdict | v1.19 |
|---|---|
| **PASS** (all of H1–H4 and any active, gating H5/H6 CONFIRMED; not downgraded) | **Runs.** |
| **MARGINAL** (including PASS downgraded by H7, or a two-model panel) | **Runs only on Pablo's recorded decision** (v1.12 §3 rule 5): a dated written decision, logged in `anchor/DEVIATIONS.md` and recorded for the scorer in `anchor/pablo_decision_paper_B.json` (`{"go": true, "date": …, "text": …}`; an undated or unworded record does not count). Every v1.19 verdict then carries the label "conditional on a MARGINAL Paper A gate (legs …)". The marginal leg's confirmatory re-test, which v1.12 rule 5 asks for, cannot be made on the same answers; under D2 it is assigned to #33's new collection (§4). Without the decision: NOT RUN (pending). |
| **FAIL**, **UNDETERMINED**, **INSTRUMENT FAIL** | **Not run.** The scorer writes `outputs/v119_not_run.json` (the verdict read, the SHA-256 of Paper A's verdict file, no statistic) and the record is deposited on OSF and cited in the Coverage write-up as "Paper B pre-registered, not run because Paper A returned X". |
| anything else, or no verdict file | Refused (no output). |

Paper A's own labels are used as written: its primary panel (`primary_panel`: N3, or C3 if Claude Fable 5.2 dropped), its rated set, floors and comparators. v1.19 repeats nothing of Paper A's gate and changes none of it.

## 2. Data and shared definitions (all from Paper A unless stated)

- **Units.** Paper A's 112 brand units in five categories (v0.19 audiophile headphones 16; v0.20 skincare, v0.21 cosmetics, v0.22 automotive, v0.23 premium spirits 24 each), keyed as in Paper A's coder (v0.23 by S01–S24). Rare Beauty is two units, as in Paper A.
- **Answers.** Paper A's analysis set, rebuilt by Paper A's own functions (`load_probes`, `probe_design`, `dedupe_calls`, `build_analysis` on its raw record and coded mention rows): one answer per (category, model, CEP, run), the set of registry brands it names. Control answers (C0) are not used. Missing cells stay missing (v1.12 §2.3).
- **Panel.** Paper A's primary panel as recorded (N3: Claude Fable 5.2, GPT-6 Astra, Gemini 4 Argon; C3 under v1.12 §7.3). S0 only.
- **β, Cov\*, floors.** Exactly v1.12 §2.4 by import (`coverage_table`, `cov_star_map`): leave-b-out Rasch-type null, β = (c − E)/(c_max − c_min), Cov\* = 50(1 + mean β), rated iff n_b ≥ 14 and at least 2 panel models name b; on a 7-CEP part the H4 rule (own δ on the part's CEPs, floor 7).
- **P.** Paper A's comparator column `P_comparator` of `v112_unit_table.csv` (P_N3, v1.12 §2.6; the AIAS 2.0 t3 value, labelled cross-panel, if Paper A used its fallback).
- **ρ_w, permutation p, n floor.** v1.12 §2.5 by import: within-category average ranks centred on the category mean rank, Pearson pooled; permutation within category; UNDETERMINED below 30 pooled units or fewer than 3 categories with ≥ 5 units. α = 0.05 per test, no multiplicity correction (programme convention), every test reported.
- **Excess situation profile** (#35 secondary, #36). For unit b and panel model m with n_{b,m} ≥ 1: observed mentions of b in the CEPs of each cue type W, minus their expectation under Paper A's situation-blind null given n_{b,m} (each answered slot's exact inclusion probability under the conditional Bernoulli law with weights exp(δ̂^(−b)_j), the same δ̂ as β; scorer note B6). Summed over the panel models and divided by Σ_m n_{b,m}: x_b = (x_{b,why}, …, x_{b,how feeling}), seven numbers that sum to 0. x_{b,W} > 0: b is named in W's situations more than situation-blind naming with the same mentions would give. Computed on the 14 CEPs (one profile) and on each half A and B (one CEP per W each).
- **Draws and seeds.** 10,000 permutations (or Monte Carlo draws) per test unless stated; seeds 119321 (H32_SetSampling), 119322 (H32_CueType, unused: deterministic), 119341 (H34_Floor_Signature), 119342 (H34_Floor_BeyondPresence), 119343 (H34_Defunct_Occupancy), 119351 (H35_IL_Coverage), 119352 (H35_IL_Robust), 119353 (H35_IL_CueType), 119361 (H36_Profile_Replication), 119362 (H36 structure on the full profiles: gap references, silhouette null and ARI null, one stream in that order), 119363 (H36 residual arm: its gap references and silhouette null), 119390 (dry-run worlds).

## 3. #32 Sensitivity to the choice of situation set

**Question.** Paper A measures Cov\* on one set of 14 situations drafted by one procedure. Does the brand order depend on which situations of that design are in the set (situation sampling), or on one cue type?

### 3.1 H32_SetSampling — PRIMARY

- **Splits.** Each category's 14 CEPs hold two per cue type W (labelled A and B). A balanced split puts one CEP of each W in part 1 and the other in part 2; there are 2^7 = 128 ordered and **64 unordered complementary splits**, applied to all categories alike (code = which W take their B-labelled CEP into part 1; scorer note B2). Split 0 is Paper A's H4 split (all A vs all B).
- **Per split.** Cov\* on each part by Paper A's H4 rule; r_s = ρ_w(Cov\*_part1, Cov\*_part2) over units rated on both parts; rel_s = 2r_s/(1 + r_s). A split enters if it meets Paper A's n floor.
- **Statistic.** r̃ = median of r_s over entering splits; rel̃ = 2r̃/(1 + r̃); P10 = the 10th percentile of rel_s. One-sided p: in each of 10,000 draws, part 2's values are permuted within category, independently per split, and the median recomputed; p = (1 + #{median_draw ≥ r̃})/10,001. Seed 119321.
- **Verdict.** **CONFIRMED iff rel̃ ≥ 0.50, p < 0.05 and P10 ≥ 0.30; FALSIFIED iff rel̃ < 0.30 or p ≥ 0.05; MARGINAL otherwise; UNDETERMINED if fewer than 32 splits meet the n floor.** (0.50 and 0.30 are Paper A's H4 bands; P10 ≥ 0.30 asks that no tenth of the splits falls into Paper A's FALSIFIED band.)
- **Reported beside it.** Where Paper A's own split (split 0) falls in the distribution (percentile), so a reader sees whether H4's split was typical.
- **Relation to Paper A.** Paper A's H4 is one of the 64 splits; its verdict is not re-decided. H32_SetSampling asks a different question: whether the order generalises over the other 63 ways the same situations could have been paired.

### 3.2 H32_CueType — SECONDARY

- **Statistic.** For each W: ρ_{−W} = ρ_w(Cov\*, Cov\*_{−W}), Cov\*_{−W} on the 12 CEPs left after dropping W's two (floor 14, as Paper A's S6). Reference: the same ρ after dropping two CEPs of **different** cue types, over all 84 such pairs of (W, label) positions, applied to every category alike. A cue type "carries" the order if ρ_{−W} is below the 5th percentile of the 84 reference values.
- **Verdict.** **CONFIRMED (no single cue type carries the order) iff at most 1 of the 7 W carries it; MARGINAL iff 2; FALSIFIED iff 3 or more; UNDETERMINED if any ρ_{−W} misses the n floor.** Deterministic (no draws).
- **Relation to Paper A.** Paper A's S6 recomputes its separability legs without each W; it does not compare Cov\* with Cov\*_{−W}. That comparison is new here.

### 3.3 Not in this study (needs new answers; D3)

The independently, human-authored parallel set of situations and situation weights from buyer data (v1.12 §10) need new answers and buyer data. They are deferred to a later pre-registration (#32b) with its own collection under the $100 rule; this study states no result about a different authoring procedure.

## 4. #33 Stability across question wording — deferred: what it needs

Paper A collects one wording only: every CEP probe is `<situation> Which <noun> brands would you suggest? Name several brands.` (automotive: "…would you suggest buying new?…"), 70 CEP probes + 5 controls, 3 runs, 4 models, 900 calls (v1.12 §6.1–6.2; `probes_v1_12.jsonl`). No wording variant is collected, so #33 cannot run on Paper A's data and gets its own pre-registration later. It would need:

1. **Wording variants** fixed before any call, from v1.12 §10's list: fixed list length ("Name five brands"), "best for…" wording, second person, a market cue. Each keeps R1–R10 of `cep_sets_v1_12.md` and changes only the question sentence.
2. **Design.** The same 70 situations, the same three N3 models, three runs (Cov\* uses runs as replicates), S0; an arm re-asking Paper A's own wording in the same session, so wording is not confounded with time since Paper A.
3. **Cost under the $100 rule.** Arithmetic on Paper A's per-model estimates (v1.12 §6.6: 225 calls each; expected $9.14 Fable, $7.14 Astra, $2.66 Argon; p90 $22.64, $10.43, $3.59), not a quote: one N3 call triple costs about $0.084 expected and $0.163 at p90. Two variants plus the re-asked original (3 × 70 × 3 = 630 triples, 1,890 calls) ≈ $53 expected, ≈ $103 at p90, so it must be cut (for example two arms only: ≈ $35 / $69) or use batch prices; four variants plus the original (5 × 210 = 1,050 triples) ≈ $88 / $171 does not fit. Prices to be re-verified at that pre-registration (Argon's price rises Dec 1).
4. **Tests** (to be fixed there): ρ_w(Cov\*_original, Cov\*_variant) per variant against a re-ask (test–retest) benchmark; MC_Situation per variant.
5. **Role under D2.** If Paper A is MARGINAL and Pablo lets Paper B run, the re-asked original arm is where the marginal leg gets its confirmatory re-test on new answers.

## 5. #34 Phantom brands: which situations they occupy

### 5.1 Definitions found in the programme (read 2026-11-12) and the choice made

The programme uses "phantom" in three senses; this study names which one each test uses.

1. **Defunct-brand phantom** (v0.6 Mint, v0.7 Bed Bath & Beyond, v0.10, v0.38 D7): a brand that no longer exists in the market but is still named. v0.10 splits it into *naive-phantom* presence ("recommended or described as if currently available — no caveat about decommissioning, sunset, or discontinuation", `osf/v10/PRE_REGISTRATION.md`) and *caveated-phantom* presence; v0.38 D7 reads a caveat "within ±150 characters". In Paper A's panel: the v0.22 registry's `Cell_D_Defunct` = **Pontiac, Oldsmobile, Plymouth, Mercury, Saturn** (set **D**), Paper A's MC_Defunct list. Fisker is in `Cell_B_Disruptor`; v1.12 §10 names it beside cell D; under D4 it is reported beside D, not in it.
2. **Recall-floor phantom flag** (v0.31 archive, consumed by v0.33 H_Provider_Phantom, the v0.34 t1 phantom set and v0.35 "Naive-Phantom × CPC"): `status == "undefined"` in `osf/v31/data/v31_cpc.csv`, i.e. mean recall below 1.0 across the six legacy models at t1 (v0.35 scorer, `FLOOR = 1.0`). On the 112 omnibus units: **57 flagged** (v0.19 8, v0.20 14, v0.21 10, v0.22 10 including the five of D, v0.23 15) — set **F**, frozen in `prereg/phantom_roster_v1_19.csv` by `build_roster_v1_19.py` (source SHA-256 `d38a3676…`, roster `9b67e892…`).
3. **v1.6 Phantom Brand Persistence**: an *off-panel* brand of a reference vocabulary named ≥ 6 times in 36 Phase B answers (Glossier, v0.21). Not used: Paper A has no detector for brands outside the registries (v1.12 §12 (v)), and only the cosmetics vocabulary exists (`osf/methodology/v1_6/reference_vocabs/cosmetics_v021.json`).

D5 (default): F for the signature test (it has enough units for a contrast and is the Consistency arc's phantom set), D for the occupancy test.

### 5.2 H34_Floor_Signature — PRIMARY

- **Statistic.** Pooled within-category Cliff's δ of Cov\* between F and non-F units (v0.35 D1: within-category cross pairs only, pair-count weighted), over units with Cov\* rated in categories with ≥ 5 rated units; two-sided permutation p with F labels shuffled within category (counts fixed), 10,000 draws, seed 119341.
- **Verdict (v0.35 bands, v0.37 sign split).** **|δ| ≥ 0.30 and p < 0.05: CONFIRMED if δ < 0 (flagged brands are more situation-bound, the prediction) or CONFIRMED_REVERSED if δ > 0; |δ| < 0.15: FALSIFIED; otherwise MARGINAL; UNDETERMINED with fewer than 10 rated F units, fewer than 10 rated non-F units, or fewer than 3 categories holding both.**
- **Why it is not a Presence artefact by construction.** Unlike v0.35's CV-CPC, Cov\* is built to be independent of the naming rate (v1.12 §2.4; Paper A's H3 tests it), so the raw contrast is the inferential test; the residualised arm below checks Presence.

### 5.3 H34_Floor_BeyondPresence — SECONDARY

Same contrast on the within-category rank residuals of Cov\* on P (v0.35 D2: OLS of centred within-category ranks, fitted over all analysable units), seed 119342; same bands. If the primary and this arm fall in different bands, both are reported and the primary is labelled "Presence-sensitive".

### 5.4 H34_Defunct_Occupancy — SECONDARY

- **Count.** Answers of the primary panel to automotive CEPs naming at least one D brand, by cue type W.
- **Null.** The W shares of all other registry-brand mentions in the same answers (what a defunct mention would look like if it followed the category's general situation mix); multinomial Monte Carlo, 10,000 draws, seed 119343.
- **Statistic.** The largest W share of defunct answers; p = (1 + #{draw ≥ observed})/10,001.
- **Verdict.** **CONFIRMED (defunct brands occupy particular situations) iff p < 0.05 and the largest share ≥ 0.40; MARGINAL iff p < 0.05 and the share < 0.40; FALSIFIED iff p ≥ 0.05; UNDETERMINED with fewer than 10 such answers.** The automotive question asks for brands to buy **new** (v1.12 R8a), so every such answer is an error; Paper A's MC_Defunct flags the category above 5%.
- **Descriptive D34.** Per W: naive versus caveated defunct mentions by a deterministic rule (one of `discontinued, defunct, no longer, ceased, phased out, out of production, shut down, was retired, folded, used market, used car, pre-owned, bankrupt` within 150 characters of the brand name, case-insensitive; v0.38 D7's window); per-brand counts; Fisker's counts beside D (D4). *(r1: in the scorer, scorer note B12: for D and, beside it, Fisker, the answers naming the brand by W, per brand in total and by W, and naive and caveated mentions by W and per brand, by the rule above. Fisker stays outside D and inside this test's reference mentions, as at r0; its counts enter no verdict.)*

## 6. #35 Identity-load moderator

### 6.1 Definition found and its validity limits

The programme's identity load is **IL-Direct**, v0.37's per-brand form of v1.6's Increment 2 (H_IdentityLoad_Direct, δ = mean R_cult − mean R_cat): "IL-Direct(b) = R_cult(b) − R_cat(b) … a CONTINUOUS per-brand covariate … Higher IL-Direct = more cultural-channel-led surfacing = higher Identity Load" (`osf/v37/prereg/v0_37_cpc_identity_load_moderator_content.py`, MODERATOR_DEFINITION). Limits stated by v0.37 and the #55 draft (`_worktrees/v0.65/osf/v65/prereg/PRE_REGISTRATION_v0_65_DRAFT_r0.md` §1, §2.1, §8): it is construct-valid only on the two-channel trio **v0.20, v0.21, v0.22** (72 units; v0.19 is single-channel and v0.23 a walled extension); a unit never named or named in every answer has IL = 0 by construction (eligibility 0 < π̂ < 1); v1.6 confirmed the pattern at cell level in cosmetics and partly in skincare; every measurement so far is US English; v0.37's power floor is n = 45 ("critical Spearman rho at p=.05 crosses 0.30 near n≈44"); and at t4 nobody has computed it yet (#55 draft §3, item 2).

### 6.2 Identity load used here (D6)

**IL_b (primary)** on the t4 N3 S0 Phase B answers of v0.42 (the same three models as Coverage): IL_b = k_{b,cult}/n_{cult} − k_{b,cat}/n_{cat}, the channel of each question being its `channel` field in `osf/v42/prereg/probes_v0_42.jsonl` (R_cat or R_cult), k the answered calls naming b (v0.42's coded rows), n the answered calls of the channel; π̂_b over the six questions; eligible iff 0 < π̂_b < 1. This is the #55 draft's English definition (its §2.1), so the two studies share one definition. **Sensitivity S-IL-t1:** v0.37's t1 IL-Direct (R_cult_total − R_cat_total from `v1_7_cpc.csv`, read as `score_v0_37.load_il_direct` reads it, with v0.37's hash check).

### 6.3 H35_IL_Coverage — PRIMARY

ρ_w(IL, Cov\*) on trio units eligible and rated; two-sided permutation p (IL's partner permuted within category), 10,000 draws, seed 119351. **Verdict (v0.37 bands): |ρ_w| ≥ 0.30 and p < 0.05: CONFIRMED if ρ_w < 0 (culture-led brands are named across fewer buying situations, the prediction), CONFIRMED_REVERSED if ρ_w > 0; |ρ_w| < 0.15: FALSIFIED; otherwise MARGINAL; UNDETERMINED below 45 units or with a trio category under 5 units.**

### 6.4 H35_IL_Robust — SECONDARY (v0.37's partial and matrix)

Partial ρ of IL and Cov\* given P on centred within-category ranks; p by permuting IL within category (10,000, seed 119352). Partial band: CONFIRMED |partial| ≥ 0.30 and p < 0.05; NULL |partial| < 0.15; MIDDLE otherwise. Cell (exhaustive): primary CONFIRMED (either sign) × |partial| ≥ 0.15 → "moderation beyond Presence"; × |partial| < 0.15 → "moderation carried by Presence"; primary FALSIFIED × partial NULL → "CLEAN NULL"; FALSIFIED × partial CONFIRMED or MIDDLE → "null on the raw arm, not clean"; primary MARGINAL → MARGINAL.

### 6.5 H35_IL_CueType — SECONDARY

ρ_w(IL, x_{b,with whom} + x_{b,how feeling}) (the excess profile of §2 on the 14 CEPs; D7), same units, two-sided p, seed 119353. Prediction: positive. Same bands with the sign split reversed (CONFIRMED if ρ_w > 0).

## 7. #36 Coverage typology / regimes

### 7.1 "Regime" in the programme, and what this study tests

v0.36 (CPC regime emergence) found "regime" overloaded across three constructs and recorded it (v0.36 pre-registration, REGIME_DISAMBIGUATION, DEVIATIONS Entry 0 (b)): (1) **v1.2's Four-Regime Taxonomy** (SSRN 6761698) is *per category*, defined by the correlation of AI Presence with Google Trends (Regime 1 marginal direct, 2 age-mediated strong, 3 scale mismatch, 4 covariate-saturated weak; v0.13–v0.14); it needs Trends data, is not a per-brand label and is unassigned for the omnibus categories; (2) **v0.23's per-brand regime** (Dominant / Established / Emerging / Absent) is within-category Presence quartiles (`score_v0_23.py` lines 332–356); (3) H_Regime4_\* are hypothesis labels. v0.36 tested whether Consistency clusters inherit (2), carry their own structure, survive residualisation on Presence, or collapse; it landed in "Cell D, unstructured", and its r3 entry recorded that its matrix was non-exhaustive (autonomy + no residual structure had no cell). The roadmap's Phase Q line asks the same of Coverage, and v1.12 §10 names the Coverage typology as "broad vs situation-bound brands; deviations from Double Jeopardy".

This study therefore does **not** assign v1.2's Trends regimes (that needs a Trends collection; out of scope, as in v0.36). It tests (a) whether brands have **situation profiles that replicate** across different situations of the same cue type, and (b) whether those profiles form types that inherit Presence tiers, stand on their own or survive removing Presence, with an exhaustive matrix.

### 7.2 H36_Profile_Replication — PRIMARY (D8)

- **Units.** Cov\* rated on the 14 CEPs, and n ≥ 7 in each half, in categories with ≥ 5 such units; Paper A's n floor.
- **Statistic.** R = mean over the seven W of ρ_w(x^A_{b,W}, x^B_{b,W}), where x^A and x^B are the excess profiles (§2) on half A and half B; in each half every W has exactly one CEP, so a positive R means a brand's lean towards a kind of situation repeats in a *different* situation of that kind. One-sided p: half B's profiles permuted across units within category (one permutation for all seven W), 10,000 draws, seed 119361.
- **Verdict.** **CONFIRMED iff R ≥ 0.20 and p < 0.05; FALSIFIED iff R < 0.10 or p ≥ 0.05; MARGINAL otherwise; UNDETERMINED below the n floor.** (D9: the bands were set on synthetic data before any real answer exists: in the dry run's first world, where 60% of brands carried a real lean towards one cue type, R was 0.14, because the mean runs over cue types that carry no brand-specific lean; the v0.37 bands 0.30 / 0.15 would have called that world FALSIFIED. The first world's record is kept, §11.)
- Per-W replication values are reported beside R.

### 7.3 H36_Structure — SECONDARY (the cluster typology; v0.36's criteria)

On the 14-CEP excess profiles of rated units: Ward linkage, Euclidean distance on the raw profiles; number of types k by the gap statistic over k = 1…8 (500 uniform references over the bounding box, Tibshirani 1-SE rule); silhouette at k; its null from 10,000 draws permuting each profile coordinate within category (one random stream, seed 119362, for the full profiles; seed 119363 for the residual arm).
- **Autonomy (A):** k ≥ 2, silhouette ≥ 0.25 and above the null's 95th percentile, and ARI with the Presence tiers < 0.30.
- **Inheritance (I):** ARI(types, Presence tiers) ≥ 0.30 and p < 0.01 (tiers permuted within category, 10,000 draws, seed 119362). **Presence tiers:** v0.23's rule applied within category to P (≥ q75 Dominant, ≥ q50 Established, ≥ q25 Emerging, else Absent; scorer note B8).
- **Residual structure (R):** each profile coordinate regressed on P within category (OLS), the residual profiles clustered by the same procedure; R holds if k ≥ 2, silhouette ≥ 0.25 and above its null's 95th percentile.
- **Matrix (exhaustive).** If H36_Profile_Replication is FALSIFIED or UNDETERMINED: **NO TYPOLOGY** (structure reported descriptively only). Otherwise (MARGINAL adds "provisional"): I and R → **LAYERED**; I, not R → **BORROWED**; not I, A and R → **AUTONOMOUS**; not I, A, not R → **PRESENCE-DEPENDENT**; not I, not A, R → **RESIDUAL-ONLY**; not I, not A, not R → **UNSTRUCTURED**. Every combination has one cell (unit test).
- **Power note.** In the dry run's strong world (three built types) the gap rule chose k = 1 (UNSTRUCTURED) at about 100 units: the cluster test is weak at this size, which is why D8 makes replication the primary claim.

### 7.4 Descriptive D36 (no verdict)

The Double Jeopardy map: units by P above or below the category median × Cov\* above or below 50 (broad / situation-bound); per-W mean excess profile per category; per-type mean profiles if k ≥ 2. *(r1: in the scorer, scorer note B13: over the units that enter H36_Structure; each type's mean profile, size and units per category from the full-profile clustering at its k.)*

## 8. Sensitivities (reported beside each verdict; never change one; changes listed)

- **S-COI:** every test without Denon (v0.19) and without the five brands with Cheil Worldwide / Iris work (Chevrolet, BMW, Bentley, Jack Daniel's (v0.23 S03), Eucerin) (§14).
- **S-Floor6:** Cov\* at floor 6 (Paper A's S2) for #34, #35, #36.
- **S-C3:** the C3 panel (Claude Opus 5.5 in place of Claude Fable 5.2) for every test.
- **S-Equal:** Paper A's equal-weight null (S3) for #32 and #36.
- **S-LOCO:** leave one category out (five variants; each one's verdicts and statistics reported).
- **S-IL-t1:** t1 IL-Direct for #35 (§6.2).
- **S-F-noD:** #34's F set without the five defunct brands.
- **S-Mid:** Paper A's mid-p β (S8) for #32 and #34.

All eight are in the scorer (`sensitivities`, scorer note B11): same seeds as the primary tests; exclusions drop units after Cov\* and the profiles are computed, as Paper A's S10 does; S-Floor6 changes the full floor only; S-C3 runs only if Paper A's answers hold every C3 model, and its panel is Paper A's C3 panel as recorded in `v112_verdicts.json` (a model dropped under v1.12 §7.3 stays out, as for the primary panel, §2 and §10; S-C3 is not run if Claude Opus 5.5 is not in it; r1, scorer note B15); S-IL-t1 takes v0.37's eligibility as 0 < mean_r/6 < 1; S-LOCO does not re-run H34_Defunct_Occupancy (a one-category test). The output lists, per variant, every verdict that differs from the primary one.

## 9. No peeking: how the order is enforced

1. **Lock target.** Pablo received r0 on Thu Nov 12 at about 7:40 am CT; it locks 24 h later (D10), Fri Nov 13 at about 7:45 am CT, before Paper A's earliest first call (Fri 6 pm CT, 2026-11-14 00:00 UTC). If it cannot lock by then, it locks later, but **before Paper A's coding step** (`score_v1_12.py --code`) and before anyone reads Paper A's answers for any purpose but Paper A's locked collection; the lock record states which of these came first. If Paper A's answers have been coded or scored before v1.19 locks, every v1.19 test is labelled exploratory in the lock record and the paper.
2. **The scorer refuses without the lock.** `score_v1_19.py --run` refuses unless tag `v1.19-prereg-r1` is on origin, `anchor/osf_anchor_v1_19.json` exists and names the tag's commit (OSF deposit verified), Paper A's `v112_verdicts.json` and `v112_unit_table.csv` exist, and `outputs/` is empty (one run). It then checks B-P0 (the imported Paper A scorer has v1.12's locked SHA-256 `f7689898…`) and B-P1 (Cov\* recomputed with the imported code equals Paper A's unit table for every unit) before any statistic; a failed gate stops it, and the fix is logged in `anchor/DEVIATIONS.md` first.
3. **Paper A's outputs hold no v1.19 statistic.** Checked on Paper A's locked scorer (blob at `v1.12-prereg-r1`, unchanged at `a57f590`): it writes `v112_verdicts.json` (gate, legs, MC checks, S1–S10, §5 descriptives) and `v112_unit_table.csv` (Cov\*, half Cov\*, raw Cov, π_cov, comparators); it contains no Cliff's δ, ARI, silhouette, identity-load, phantom-flag, excess-profile or split-distribution code (unit test `test_paper_A_scorer_computes_no_paper_B_statistic`). What Paper A's outputs *do* reveal, and v1.19 therefore cannot treat as unseen once Paper A is scored: per-unit Cov\* and P (the inputs of every test); Paper A's H4 split value (one of #32's 64); S6's separability legs without each W (not #32's comparison); MC_Defunct's share of automotive answers naming each defunct brand (the count behind H34_Defunct_Occupancy's floor, not its W distribution); and §5's per-unit count of covered CEPs per W (a coarse cousin of #36's profile, without the null expectation). This is why the lock must precede Paper A's scoring.
4. **What was read while drafting (ex ante).** No Coverage answer exists. Read: v1.12's pre-registration, CEP sets, probe file header lines and scorer source; v1.12's anchor files; the roadmap, `CLAUDE.md` sections named in the brief; v0.35, v0.36 and v0.37 pre-registration modules; v0.35's scorer (phantom flag lines); v1.6's outline and scorer (phantom lines); v0.10's pre-registration (phantom definitions); v0.13 / v0.14 pre-registration lines on regimes; the #55 draft; v1.18 §13; v0.42's coded-table **header lines** and the first data line's brand key of two files (to confirm unit keys), v0.42's brand-table header; `v31_cpc.csv` (to freeze the roster: flags and t1 recall means, which v0.35 published); the v0.22 registry cells; v0.23's brand list line for Jack Daniel's. No identity-load value, Cov\*, β or other study statistic was computed on real data. **At r1** (same day): read this draft's r0, v1.19's scorer, tests and dry-run records, lines of Paper A's scorer (panels, `select_panels`, `build_analysis`, the defunct list), and the roster's Fisker row and a text search of the v0.22 registry file for "Fisker" (to confirm the unit key); no v0.42 coded file or probe file, no Paper A data (none exists) and no other real answer; nothing computed on real data.

## 10. Exclusions and missing data

Units and answers: Paper A's analysis set and rated set, unchanged; NOT RATED units leave each test that needs Cov\*; no imputation. #35 excludes ineligible IL units (π̂ = 0 or 1) and non-trio units. #34's defunct test uses all automotive CEP answers of the primary panel. A category with fewer than 5 analysable units leaves a pooled test (Paper A's rule). Two-model panels (v1.12 §7.3): tests computed and labelled two-model.

## 11. Dry run and tests (synthetic only)

`python3 osf/methodology/v1_19/scripts/score_v1_19.py --dry-run osf/methodology/v1_19/dryrun --draws 10000 --gap-b 500` (about 2 minutes on the Mac, 2026-11-12; the record carries the scorer's SHA-256 and the B-P0 check) scores three synthetic worlds shaped like Paper A's analysis set (Paper A's real probe design; 112 units in 16/24/24/24/24; three N3 models × 14 CEPs × 3 runs; seeds 119390–119392) plus the two not-run paths. **Effects world** (flagged brands situation-bound; identity load lowers breadth and raises with-whom / how-feeling occupancy; 60% of brands lean to one cue type; defunct brands concentrated in "when"): every built-in verdict came out as built (H32_SetSampling CONFIRMED, rel̃ 0.580; H34_Floor_Signature CONFIRMED, δ = −0.715; H34_Defunct_Occupancy CONFIRMED, 13 answers, max share 0.85; H35_IL_Coverage CONFIRMED, ρ_w = −0.456, n = 63; H35_IL_CueType CONFIRMED, ρ_w = 0.415; H36_Profile_Replication CONFIRMED, R = 0.231); the cluster cell was UNSTRUCTURED (k = 1; §7.3 power note). **Null world** (situation-blind naming): H32_SetSampling FALSIFIED (rel̃ 0.035), H32_CueType CONFIRMED, H34 FALSIFIED (δ = 0.112), H34_Defunct FALSIFIED (p = 0.80), H35 FALSIFIED (ρ_w = −0.094; robust cell CLEAN NULL), H36 replication FALSIFIED (R = 0.010; NO TYPOLOGY); H35_IL_CueType came out MARGINAL by chance (ρ_w = −0.257, p = 0.065), reported as it fell. **Weak world** (the first effects world's strengths): H32 and H34 as built; H35 MARGINAL and H36 replication MARGINAL (power illustration). **Not-run paths:** FAIL → NOT RUN with no statistic; MARGINAL without a decision → NOT RUN (pending). Earlier attempts are kept: `dryrun/dry_run_v1_19_attempt1_weak_world.json` (first world, 300 draws; H35 MARGINAL, H36 replication FALSIFIED at R = 0.141 under the then 0.30 / 0.15 bands) and `dry_run_v1_19_attempt2.json` (300 draws; type lean 2.5, identity-load spread 1.6, flag spread 1.0: H32_SetSampling MARGINAL at rel̃ 0.488, H36 replication MARGINAL at R = 0.170 under the then 0.30 / 0.15 bands). After them both the strong world (type lean 3.0, flag spread 1.4; `STRENGTH` in the scorer) and D9's bands were set; the bands change is a design decision on synthetic data, listed for Pablo (D9), not a reading of real data. Tests: `scripts/tests/test_score_v1_19.py` (20 unit tests: conditionality, import-not-fork, the 64 splits, Cliff's δ against brute force, exact inclusion probabilities against enumeration, profile sums, ARI and silhouette, verdict bands, both matrices exhaustive, IL arithmetic, the defunct floor, guards, B-P1) and `scripts/tests/test_loader_v1_19.py` (5 tests: 4 integration tests of the real-data path on synthetic files laid out as Paper A's scorer writes them: the loader rebuilds the answer index exactly, one PASS run writes its verdict file with B-P0 and B-P1 passed, a tampered unit table is refused by B-P1 with no output, a FAIL verdict writes the not-run record with no statistic; and 1 test of the sensitivity options: exclusion, floor 6, equal-weight null) and `scripts/tests/test_e2e_paperA_v1_19.py` (2 tests: Paper A's own test helpers and Paper A's own `score_coverage` / `write_outputs`, imported unchanged, write a synthetic `v112_verdicts.json` and `v112_unit_table.csv`; v1.19 routes on Paper A's synthetic verdict as §1 says, and, on a copy of that verdict set to PASS for the test only, B-P1 reproduces Paper A's unit table for all 112 units) and `scripts/tests/test_e2e_coder_v1_19.py` (2 tests: the same with Paper A's coder in the loop, step by step as v1.12's `test_end_to_end_synthetic`: `--brandfree`, `--code`, the t4 synthetic coder, `--synthetic`; B-P1 passes on all 112 units and v1.19 routes on Paper A's own synthetic verdict); 29 tests, all pass. Paper A's own suite, unchanged, was re-run in this worktree on 2026-11-12: 118 tests, all pass (its acquisition tests run `--collect` against fake providers, with no network; they leave no file in the tree).

**r1 (2026-11-12).** `python3 osf/methodology/v1_19/scripts/score_v1_19.py --dry-run osf/methodology/v1_19/dryrun --draws 10000 --gap-b 500 --out-name dry_run_v1_19_r1.json` re-scored the same three worlds with the same seeds (119390–119392) and the two not-run paths into `dryrun/dry_run_v1_19_r1.json`; r0's records are kept unchanged. Every primary and secondary verdict, both matrix cells and both not-run statuses are identical to r0's dry run, and so is every statistic in the record apart from the new descriptive keys (D34, D36). In the synthetic worlds no unit is called Fisker, so the dry run counts a synthetic brand (`v0.22-b00`) in Fisker's place to exercise the path (`fisker_stand_in` in the record); every synthetic world chose k = 1, so its per-type profiles are empty and the per-type path is covered by a unit test. **S-C3** was exercised on a synthetic world holding Paper A's four models (`synthetic_world_a4`, dry-run seed 119390; primary panel N3): at 10,000 draws (the timing run below) S-C3 ran on Paper A's C3 panel (Claude Opus 5.5, GPT-6 Astra, Gemini 4 Argon) and returned every verdict; against the N3 primary scoring of the same world it differs in H36_Profile_Replication (CONFIRMED there, MARGINAL under S-C3) and therefore in the typology cell's label (UNSTRUCTURED, provisional under S-C3), which a sensitivity reports and never acts on. Exercising it exposed one bug, fixed (§18 item 4). **Timing:** `python3 osf/methodology/v1_19/scripts/score_v1_19.py --draws 10000 --gap-b 500 --time-sensitivities osf/methodology/v1_19/dryrun/sensitivity_timing_v1_19_r1.json` (the Mac, 2026-11-12, no other scoring running) scored that four-model world once (primary, 40.4 s) and then every §8 variant, twelve runs (S-COI, S-Floor6, S-Equal, S-Mid, S-F-noD, the five S-LOCO, S-C3, and S-IL-t1 on a copy of the world's synthetic identity load), 4.3 to 40.5 s each: **373.3 s in all (about 6.2 minutes), measured**, recorded step by step in `dryrun/sensitivity_timing_v1_19_r1.json`. Silhouette nulls run only where a clustering arm picks k ≥ 2, and the record does not show in how many steps that happened; measured separately, 500 draws of Ward clustering plus silhouette on a 103 × 7 matrix took 0.76 s, so each such arm would add roughly 15 s at 10,000 draws (an estimate, not a measured run). The real run's loading and parity gates are not included. The r1 dry run itself took 120.74 s. **Tests at r1:** 36 v1.19 tests, all pass (r0's 29 plus 7: the classes `R1Descriptives` (4) and `SC3` (2) in `test_score_v1_19.py`, now 26 tests, and `test_s_c3_on_the_real_path` in `test_loader_v1_19.py`, now 6); Paper A's own suite, unchanged, re-run in this worktree: 118 tests, all pass.

## 12. Predictions (before any Paper A answer exists)

H32_SetSampling lean MARGINAL (Paper A predicted its own H4 lean MARGINAL). H32_CueType lean CONFIRMED. H34_Floor_Signature lean UNDETERMINED or CONFIRMED: many flagged brands may not reach 14 mentions. H34_Defunct_Occupancy lean UNDETERMINED (fewer than 10 answers if MC_Defunct stays under 5%). H35_IL_Coverage lean MARGINAL or FALSIFIED (identity load did not moderate Consistency, v0.37). H36_Profile_Replication lean MARGINAL; cluster cell lean UNSTRUCTURED (v0.36's outcome; §7.3 power note).

## 13. Limitations

1. All four studies re-use Paper A's single set of 14 situations per category, drafted by one procedure and by a model that is also a panel arm (v1.12 R10). #32 measures sensitivity *within* that design; a different authoring procedure is #32b's question (D3).
2. Half profiles rest on one situation per cue type; #36's replication is conservative, and its cluster test is weak at about 100 units (§7.3).
3. Identity load is defined on the trio only (72 units, fewer after eligibility and rating); the t4 version has no published benchmark yet (#55).
4. The recall-floor flags come from the legacy six-model panel at t1, while Cov\* comes from the newest models; brands may have moved since (S-F-noD and S-C3 do not remove this).
5. Defunct brands are five units in one category, asked for brands to buy new; their occupancy test will often be UNDETERMINED.
6. The caveat rule is a keyword window; in short answers it can catch another brand's caveat (seen in the dry run's synthetic texts). It is descriptive only.
7. No multiplicity correction (programme convention); 10 verdicts are reported (5 primary, 5 secondary), and every one is reported whatever it is.

## 14. Declarations

**Conflict of interest.** The author is Director, Corporate Brand Creative and Governance at Samsung Electronics America. This study re-analyses answers scored against brand registries fixed in earlier phases; it performs no new brand selection, and each registry carries its source-phase conflict-of-interest handling forward (v1.12 §8). Three items of record apply, quoted verbatim from their source records as v1.12 §8 quotes them. *Audiophile headphones (v0.19)* — `osf/v19/PRE_REGISTRATION_v0_19.md` §2.3: "**AKG removed from Cell A short-list; Denon substituted.** AKG is Samsung-owned since 2016. The author's COI declaration names Samsung; including AKG would invite the kind of reviewer suspicion AIAS™ 1.0 does not need to absorb. Denon carries comparable heritage stature (founded 1910; AH-D7000 → D9200 audiophile line) and removes the question. Decision rationale recorded here for audit trail." Correction (November 10, 2026): Denon, which replaced AKG in the v0.19 registry, has itself been owned by Harman International, a wholly owned subsidiary of Samsung Electronics, since September 23, 2025, when Harman completed its acquisition of Sound United from Masimo; the v0.19 headphones registry therefore includes one Samsung-group brand. The substitution did not achieve its purpose, and this was not noticed until November 10, 2026. Source: HARMAN press release, Business Wire, September 23, 2025. Denon stays in every analysis (sensitivity S-COI). *Automotive (v0.22)* — `prereg/v0_22_mega_prompt.md`, DEVIATIONS Entry 0, Part B — COI screen: "**Screen result:** Three of the 24 brands in the locked v0.22 registry have tier-2/3 supply relationships with Samsung Electronics America (author's primary employer) via Samsung subsidiaries: BMW (Harman audio + Samsung SDI batteries + Samsung Display infotainment), Mercedes-Benz (Harman audio + Samsung Display infotainment), and Volkswagen Group brands including Bentley and Porsche (Samsung SDI battery supply to Stellantis-adjacent platforms). Tesla and Polestar also have tangential Samsung-component exposure at the parts level. These are all tier-2/3 non-competitive supply relationships, not brand-level competition. Samsung Electronics America does not produce or market passenger car brands. The COI relationship does not affect brand recognition or recall measurement by LLM panel and does not impose operational restriction on registry composition."

*Agency work (Cheil Worldwide and Iris).* Cheil Worldwide, a marketing company of the Samsung group in which Samsung Electronics holds 28.43%, or its agency Iris has done advertising, public-relations or search-marketing work for five registry brands: Chevrolet (for GM Korea, 2017), BMW (UK consumer public relations, 2018), Bentley (experiential agency of record in the Americas from 2021), Jack Daniel's (UK digital agency from 2022, since replaced) and Eucerin (search marketing for Beiersdorf from 2024). (Conflict-of-interest screen of v0.62, DEVIATIONS Entry 0, Part F.) As Denon, these five brands stay in every analysis, and every test is also reported without them and Denon (sensitivity S-COI).

Non-registry brands named in answers (which may include Samsung-owned brands) are not scored, as in Paper A. Samsung Electronics had no role in the design, conduct, analysis or reporting of this work.

**Funding.** Self-funded. No paid model call. **Ethics.** Not applicable; no human subjects.

**Use of AI tools.** During the preparation of this work the author used AI tools (Anthropic's Claude) to assist with study design, analysis and writing. The author reviewed and edited all content and takes full responsibility for it.

## 15. Lock procedure and change log

Between sending and lock, clarifications that change no hypothesis, threshold, estimand, seed, exclusion or decision rule are logged here; any other change restarts the 24 hours (D10). Lock (r1): settle D1–D10 and the open questions (§17); check OSF for `methodology/v1_19`; re-run the unit tests and the dry run; rebuild `prereg/LOCK_MANIFEST_v1_19.sha256` (this file, the roster and its builder, the scorer, its tests, the dry-run records, `anchor/DEVIATIONS.md`, and v1.12's scorer as imported); commit; tag `v1.19-prereg-r1`; push; deposit `prereg/`, `anchor/`, `scripts/` and `dryrun/` on OSF (`methodology/v1_19`) and verify their SHA-256 there; write `anchor/osf_anchor_v1_19.json`. Run once, after Paper A's scored output exists and its gate allows (§1).

**Change log.**
- 2026-11-12: r0 drafted by the runner's lane H (not sent, not locked).
- 2026-11-12, ~7:40 am CT: r0 sent to Pablo and deposited on OSF (`methodology/v1_19/draft_r0`) by the runner (as reported by the runner).
- 2026-11-12: r1, a clarification under the rule above: every change is listed in §18 with whether it touches a hypothesis, threshold, estimand, seed, exclusion or decision rule; none does, so the 24 hours are not restarted.

## 16. Files

`prereg/PRE_REGISTRATION_v1_19_DRAFT_r1.md` (this file) and `prereg/PRE_REGISTRATION_v1_19_DRAFT_r0.md` (r0 as sent, unchanged); `prereg/build_roster_v1_19.py` and `prereg/phantom_roster_v1_19.csv` (§5.1); `prereg/LOCK_MANIFEST_v1_19_DRAFT.sha256` (draft manifest, rebuilt at lock); `scripts/score_v1_19.py` (scorer skeleton; imports `osf/methodology/v1_12/scripts/score_v1_12.py`); `scripts/tests/test_score_v1_19.py` (26 tests at r1; 20 at r0), `scripts/tests/test_loader_v1_19.py` (6 tests at r1; 5 at r0), `scripts/tests/test_e2e_paperA_v1_19.py` (2 tests) and `scripts/tests/test_e2e_coder_v1_19.py` (2 tests); Paper A's own suite (`osf/methodology/v1_12/scripts/tests/`), unchanged, re-run in this worktree; `dryrun/dry_run_v1_19.json` and the two earlier attempts (§11); r1's `dryrun/dry_run_v1_19_r1.json` and `dryrun/sensitivity_timing_v1_19_r1.json` (§11); `anchor/DEVIATIONS.md` (Entry 0). At r1 the scorer gained the D34 and D36 descriptives, `synthetic_world_a4`, `time_sensitivities` and the S-C3 panel fix (scorer notes B12–B15), and the tests gained the classes `R1Descriptives` and `SC3` (`test_score_v1_19.py`) and `test_s_c3_on_the_real_path` (`test_loader_v1_19.py`).

## 17. Open questions (for r1)

1. **#55 coordination (settled by the order of the locks; schedule as reported by the runner).** #55 (v0.65) locks first, Fri 2026-11-13 at about 6:45 am CT, an hour before v1.19 (§9.1). v1.19 computes t4 identity load (§6.2) only in its single run, which needs v1.19's own lock (§9.2) and Paper A's gate (§1; Paper A's gate is expected around Dec 7), so no t4 identity-load value exists before #55 locks and #55 has no look to declare. D6 is unchanged. (r0's text: "The #55 draft (v0.65) says nobody has computed t4 identity load. v1.19's run would compute it on the English t4 answers that #55 uses as its baseline; if v1.19 runs before #55 locks, #55 must declare that look.")
2. **OSF folder** `methodology/v1_19`: exists and holds `draft_r0`, deposited Thu 2026-11-12 by the runner (as reported by the runner; the lane that wrote r1 made no OSF call and did not check it).
3. **Study list numbers** #32–#36 come from the runner's brief; the repository's roadmap lists the studies without numbers.
4. **MARGINAL route** (D2): the marginal leg's re-test needs #33's collection; until #33 is pre-registered, a MARGINAL Paper A leaves that leg without its re-test.
5. **The real-data path** is written and tested on synthetic files end to end through Paper A's coder and scorer (§11). Not tested: the real v0.42 coded files and probe file (read at the run only, to keep #55's input unlooked-at, open question 1).
6. **Fisker** (D4): whether it is defunct is a factual question this draft does not settle from a source; it stays outside D unless Pablo decides otherwise with a source.
7. **Done at r1** (r0 listed these as not yet in the scorer): Fisker's descriptive counts beside D (scorer note B12) and D36's per-category mean profiles and per-type profiles (B13), each with unit tests; S-C3 exercised end to end on a synthetic world holding Paper A's four models (B14), with a unit test and a real-path test, which exposed one bug in S-C3's panel, fixed (B15; §18); the full sensitivity run timed at 10,000 draws (§11): 373.3 s (about 6.2 minutes) for the primary scoring and all twelve variant runs on a synthetic four-model world, measured. Nothing of r0's list remains open.

## 18. Changes from r0 to r1

Under §15, only clarifications that change no hypothesis, threshold, estimand, seed, exclusion or decision rule may enter between sending and lock without restarting the 24 hours. Each r1 change is listed with that check. r0 (`PRE_REGISTRATION_v1_19_DRAFT_r0.md`, as sent and as deposited) is unchanged.

| # | Where | Change | Changes a hypothesis, threshold, estimand, seed, exclusion or decision rule? |
|---|---|---|---|
| 1 | Header; "Timing"; D10's row; §0 Status and Number; §9.1; §15 change log | Records that r0 reached Pablo Thu 2026-11-12 ~7:40 am CT and was deposited on OSF (`methodology/v1_19/draft_r0`) by the runner (as reported by the runner), and fills in the lock's clock time that follows (Fri ~7:45 am CT) | **No.** D10's rule (24 h after receipt, and before Paper A's `--code` step) is unchanged; only the clock time it gives is filled in. |
| 2 | §5.4, Descriptive D34; scorer note B12 | Fisker's counts beside D and the per-brand naive / caveated split are now in the scorer, by the rule r0 states; unit tests added | **No.** Descriptive only (no verdict); D4 unchanged (Fisker outside D, and inside H34_Defunct_Occupancy's reference mentions as at r0); a unit test checks that H34_Defunct_Occupancy's statistics and verdict are the same with and without Fisker's counts. |
| 3 | §7.4, Descriptive D36; scorer note B13 | Per-category mean profiles and per-type mean profiles are now in the scorer, over the units that enter H36_Structure; unit tests added | **No.** Descriptive only (no verdict); no change to the profiles, the clustering or the matrix. |
| 4 | §8, S-C3; scorer note B15 | **Bug fix.** r0's scorer took S-C3's panel from v1.12's fixed C3 list and ran it whenever each C3 model had any answer, so a model dropped by Paper A under v1.12 §7.3 (below 90% answered) would have stayed in S-C3's panel. S-C3 now uses Paper A's C3 panel as recorded in `v112_verdicts.json`, and is not run if Claude Opus 5.5 is not in it | **No.** A sensitivity never changes a verdict (§8); no hypothesis, band, estimand or seed is touched; the unit set is unchanged; the model drop is Paper A's own rule, which §2 and §10 already apply to the primary panel. With all four models answering, S-C3's panel is the same as at r0. The fix is in its own commit, so it can be reverted alone if it is judged otherwise. |
| 5 | §9.4 | Lists what was read at r1 | **No.** |
| 6 | §11 | Adds r1's dry run (same worlds, same seeds; verdicts and statistics identical to r0's), S-C3's synthetic run, the timing of the full sensitivity run at 10,000 draws, and the test counts | **No.** Synthetic data only. |
| 7 | §16 | Lists r1's files | **No.** |
| 8 | §17 items 1, 2, 7 | Item 1: #55 locks before v1.19, and v1.19 computes t4 identity load only after its own lock and Paper A's gate (r0's text kept in quotation); item 2: the OSF folder, as reported by the runner; item 7: what r1 did | **No.** D6 (t4 identity load primary, t1 as sensitivity) is unchanged. |
| 9 | Scorer test tooling (scorer note B14) | `synthetic_world_a4`, `time_sensitivities`, the dry run's `--out-name`, and a synthetic stand-in for Fisker in the dry run | **No.** Used on synthetic data only; the dry-run seeds are r0's. |
