---
title: "From Named to Chosen: Does a Brand's AI Presence Predict the Brand an AI Model Chooses for a Buyer? A Stage 1 Registered Report"
author: "Pablo Ulpiano González Castro"
date: "Stage 1 draft r2, 22 November 2026"
---

> **DRAFT r2 FOR PABLO — NOT SUBMITTED.** r1 was written 2026-11-21 by a runner lane from pre-registration r1 of v0.46 (#76; branch `named-to-chosen`, head e4bc95c), Pablo's decisions of 2026-11-14 (D1–D8) and 2026-11-17 (venue plan, item 4). r2 (2026-11-22) applies Pablo's answers of 2026-11-22, 8:17 am, to r1's open questions (Appendix B records them) and brings Sections 5.1–5.7 into line with the Stage 1 code (code r1–r3, branch `v0.46-stage1`). No model has been called, nothing is locked, pushed, deposited or posted. Bracketed **[DRAFT NOTE]** blocks are for Pablo and are removed before submission. Target: PCI Registered Reports, standard track, submission about 2027-01-15; destination journal Peer Community Journal. The submission PDF will carry numbered lines, as PCI RR recommends.

Pablo Ulpiano González Castro
School of Visual Arts, MPS Branding Program, New York, NY (primary academic affiliation)
Third System™ (research entity; data archive and methodology venue)
Correspondence: pablou@pablou.com · pablou.com
ORCID: 0009-0003-8968-9990 (linked: https://orcid.org/0009-0003-8968-9990)

**Type of submission.** Stage 1 Registered Report (PCI RR, standard track). Quantitative, hypothesis-testing. No human participants.

**Requested bias-control level.** Level 6: none of the data that will answer the research questions exists at submission. Both the outcome (the models' choices) and the predictors (Presence and Ranking) are collected after in-principle acceptance (IPA), in one collection (Section 8).

**Estimated Stage 2 submission.** July 2027 (estimate; Section 9.3).

## Abstract

Buyers have begun to ask AI assistants not only which brands are good but to pick one for them. The Tri-System Brand Growth framework proposes that one mechanism, training-corpus prominence meeting single-recommendation output, produces what AI systems surface, and that the modal outcome is reinforcement of brands that are already prominent. The AIAS™ programme measures that prominence as AI Presence: how often models name a brand when asked about its category, and whether they recognise it. Whether the brand a model names is also the brand it chooses when a buyer hands it the decision has not been tested. This Registered Report tests that link, named → chosen, for the newest generally available flagship model of each of three providers, selected by a fixed rule at collection. In four categories (skincare, cosmetics, cars, premium spirits; 91 brands on sale), each model receives three neutral buyer briefs, either with no list (it may name any brand) or with the category's full list of brands in an order balanced by Latin squares. In the same collection, the same models answer the programme's Presence and Ranking questions, so that predictors and outcome are measured together and neither exists before acceptance. The primary test asks whether the brands chosen from the list have high Presence, measured as a choice-weighted area under the curve, Ū_P, with a within-category permutation test (confirmed if Ū_P ≥ 0.70 and p < .05; falsified if Ū_P < 0.60). Secondary tests address free choice, the Ranking score and whether it adds to Presence, and list-position effects. The study measures a model's stated choice for a hypothetical buyer: nothing is bought, no agent or checkout tool is used, and no brand, seller or retailer is contacted. The collection costs an estimated US$44 (high estimate US$86) under a US$100 hard cap.

**Keywords:** AI Availability; AI Presence; agentic choice; large language models; brand choice; Registered Report; Tri-System Brand Growth; position effects; Latin square

---

## 1. Introduction

### 1.1 From naming to choosing

The AIAS programme measures what AI models say about brands. Its first published component, Presence, records whether and how often a model names a brand when asked about the brand's category, and whether the model recognises the brand when asked about it directly (González Castro 2026g, SSRN 6816340; González Castro 2026h, SSRN 6817841). A second published component, Consistency, records how evenly different models name the brand (v1.8, SSRN 6963359). A third candidate, Ranking, records where in a model's list a brand tends to appear; after three pre-registered tests it is reported as part of Presence rather than as a separate score (v1.10, v1.14, v1.16; Section 1.3).

Each of these is a measure of what a model *names*. A buyer who asks an assistant to make the decision receives something different: one brand. Whether the brand a model names often is the brand it chooses when it must choose one is an empirical question, and it is the link between two parts of a chain the programme studies: what AI says (Presence), what AI chooses (this study), and what people search for and buy (separate studies of search interest and, from a licensed source only, sales rank). This study measures the middle link, **named → chosen**, and leaves **chosen → bought** to those studies.

Agentic buying is early. On its third-quarter 2026 earnings call, Uber's chief financial officer said that "only four rides were ordered through an AI agent during its busiest week in October" and "only 500 Uber Eats orders were placed by an AI agent", against "around 320 million trips and orders across Uber and Uber Eats during the week of Halloween" (Perez 2026). Real agent purchases are therefore too rare to study as an outcome, and this study does not try. It asks models to state a choice, which is the decision an agent would act on. Its results say how a model chooses when asked to choose; they do not say that anyone bought anything, or that sales follow.

### 1.2 Theoretical basis: the Tri-System propositions

Tri-System Brand Growth (González Castro 2026, MSI Working Paper Report No. 26-132) proposes AI mediation as a third system beside Mental Availability and Physical Availability (Sharp 2010; Romaniuk and Sharp 2016), and states five propositions. Three bear on this study.

- **P0, unified mechanism.** One mechanism, training-corpus prominence interacting with single-recommendation output, produces both of the outcomes in P1 and P2; they are the same mechanism under different conditions.
- **P1, reinforcement (the modal outcome).** "In most categories most of the time, AI-surfaced brand distributions track prior market shares more closely than they reorder them, and AI mediation amplifies rather than disrupts existing brand hierarchies."
- **P2, selective suspension (the conditional outcome).** When five conditions hold together (a utilitarian category, low identity load, low involvement, a single-recommendation interface and a consumer who trusts AI), the same mechanism reweights choice, so that brands with weaker prior mental availability enter consideration sets they would otherwise not enter. The conditions are jointly necessary.

The remaining propositions, P3 (identity-load moderation) and P4 (brand-familiarity moderation, an inverted U), are moderators of P2's reweighting in human choice and are not tested here.

The programme's Presence measure is an observable of the first half of P0's mechanism: it records how prominent a brand is in what a model produces when asked about a category. This study supplies the second half, the single-recommendation output, and asks whether the first predicts the second. Two readings of P0 and P1 lead to the hypotheses of Section 2.

1. **If one prominence drives both naming and choosing** (P0), the brand a model chooses for a buyer should be, more often than chance and by a margin that matters, a brand the same model names prominently. If P1's reinforcement is the modal outcome, the margin should be large: choice should concentrate on high-Presence brands, not reorder them. A weak or absent link would mean that single-recommendation output runs on something other than the prominence Presence records, which is a direct challenge to P0 at the model step.
2. **Single-recommendation output is the top slot of an implicit list.** If what decides the single pick is where a brand sits in the model's lists rather than how often it is named, the Ranking score should predict choice and should add to Presence. The programme's own measurement result points the other way: Ranking did not separate from Presence in three pre-registered tests and is reported as part of it (Section 1.3). The two predictions compete, and the study decides between them for choice.

The study tests the model side of the framework only. P2's five conditions include properties of the consumer (trust in AI) and of the category as experienced by people (involvement, identity load); none of these is observed when the "buyer" is a fixed text brief. The study's interface is, by construction, single-recommendation: every prompt asks for exactly one brand. Its results therefore bear on P0 and P1 as statements about what AI systems produce, and say nothing about P2's consumer-side conditions, which the MSI paper tests with people (n = 208; González Castro 2026, Section 5.1).

> **[DRAFT NOTE]** The proposition wording above is taken from the project doc claude/book-aias-alignment.md, section 1b, which was checked on 2026-11-14 against the May 6 submission manuscript; the version MSI posted on 2026-10-15 "may differ in small ways". Decided 2026-11-22 (Appendix B, item 14): before submission the quotation of P1 is checked against the posted working paper by an AI check against the PDF (not a manual one), and the paper's public URL is added to the reference. The check is planned and has not been run (it needs a model call).

### 1.3 Presence and Ranking as measured by the programme

**Presence.** The Presence score used here is the definition the programme's methodology papers v1.12, v1.13 and v1.14 share on the t₄ wave (v0.42): P = 100 · (C_P/3 + 2 · π̂)/3, where π̂ is recall Presence (v0.42's `pi_N3_S0`: recall across the three models, three runs and the category's questions, search off) and C_P/3 is the share of the three models whose recognition code for the brand is "recognized". Presence carries the methodology lock of v1.6 (SSRN 6816340). Per-brand Presence has been stable across waves where stability could be measured (v0.34, SSRN 6915458: Spearman ρ = 0.81, 0.99 and 1.00 in the categories where it was defined).

**Ranking.** The Ranking statistic used here is v1.14's modal position, R\* = −(the smallest modal competition rank of the brand over its rankable mentions), higher meaning nearer the top of the models' lists, defined only for brands with at least six rankable mentions (v1.14, `scripts/score_v1_14.py`, `modal_position`; identical to v1.10's MODE). v1.14's Stage 1 test on t₄ was MARGINAL (separable from Consistency, ρ_w = 0.132, n = 70; not clearly separable from Presence, ρ_w = 0.369, n = 71, against a 0.30 bar). The last pre-registered Ranking redesign, v1.16, was also MARGINAL (2026-11-12), and under the consequence clause fixed before that run Ranking is reported as part of Presence, with no further redesign. Every Ranking result in this study is therefore a result about the MODE statistic as a behavioural predictor; none of them changes Ranking's status in the AIAS score.

### 1.4 What published work on AI shopping agents leads us to control

Two experimental studies of AI shopping agents shape the design.

- Allouah, Besbes, Figueroa, Kanoria and Kumar (2025) report that agents "exhibit strong position biases", that agents "can exhibit choice homogeneity, often concentrating demand on a few" products, that they "consistently penalize sponsored tags while rewarding platform endorsements", that sensitivity to price, ratings and reviews differs sharply across models, and that "model updates can drastically reshuffle market shares".
- Cherep, Ma, Xu, Shaked, Maes and Singh (2025) "vary prices, ratings, and psychological nudges", find that "agent decisions shift predictably and substantially in response", and conclude that "agents are strongly biased choosers even without being subject to the cognitive constraints that shape human biases". (Its abstract does not mention position effects; position rests on Allouah et al.)

Four design consequences follow. (i) List order is randomised and balanced, and position effects are estimated, not ignored (H5; Section 5.5). (ii) No price, rating, review, sponsorship or endorsement cue appears in any prompt, so a choice can reflect only what the model brings to it: the brief, the brand names and, in the list condition, their order. (iii) Concentration of choices on a few brands is expected, and the primary statistic and its test are built to stay valid under it (Section 5.1). (iv) Results are reported per model, because model dependence is itself a published finding, and the models are chosen by a rule fixed now (Section 3.3), because model updates may reshuffle choices.

### 1.5 What this study is not

It is not a study of purchases, of shopping agents acting on real stores, of what any person would choose, or of AI search. The models answer from what they bring to the prompt, with web search and every other tool off (Section 3.7). Whether models with search and browsing choose differently is a separate question, not included in this protocol (Section 3.12).

---

## 2. Research questions and hypotheses

Every hypothesis below follows from Section 1.2 and is stated with its test, its verdict rule and the outcome that would count against it. Definitions are in Section 5.1. All thresholds were fixed on 2026-11-11 in the study's first pre-registration draft, before any choice existed, and are unchanged.

**RQ1 (primary). Presence → choice from a list.** When a model chooses one brand for a buyer from the full list of a category's brands, shown in a balanced random order, does it choose brands with high Presence?

> **H1 `H_Presence_Choice_List` (PRIMARY).** The chosen brand tends to have high Presence in its category. *Test:* Ū_P over valid LIST choices, one-sided within-category permutation p (Section 5.2). *Verdict:* CONFIRMED if Ū_P ≥ 0.70 and p < .05; FALSIFIED if Ū_P < 0.60; MARGINAL otherwise; UNDETERMINED under the conditions of Section 5.4. *Follows from:* P0 and P1 (Section 1.2, reading 1). *Counts against it:* Ū_P < 0.60, i.e. the chosen brand outranks a randomly drawn listed brand on Presence fewer than six times in ten.

**RQ2. Named → chosen without a list.** When a model chooses freely, do its choices land on high-Presence brands of the registry, and how often outside it?

> **H2 `H_Presence_Choice_Open` (SECONDARY).** Free choices that land on registry brands tend to have high Presence. *Test and verdict:* as H1, on valid OPEN choices. *Declared:* the test is partly mechanical (a model cannot choose freely a brand it does not bring to mind, and Presence measures exactly that); a CONFIRMED is expected and weaker evidence than H1. Its value is in the realistic setting and in the share of choices outside the registry (Section 5.7, descriptive 2).

**RQ3. Ranking → choice, and beyond Presence.** Does the Ranking score predict which listed brand is chosen, and does it add anything to Presence?

> **H3 `H_Ranking_Choice_List` (SECONDARY).** In LIST, the chosen brand tends to have a high Ranking score. *Test:* Ū_R over valid LIST choices that fall on rated brands; permutation p; verdict as H1. *Declared:* conditional on the brand being named often enough to be rated; because R\* and P correlate, a CONFIRMED here can be Presence in another form; H4 separates them.
>
> **H4 `H_Ranking_Beyond_Presence` (SECONDARY).** Among rated brands, Ranking predicts choice beyond Presence. *Test:* conditional logit with Presence, Ranking and position terms; one-sided Freedman–Lane permutation p for β_R; effect size OR_R = exp(β_R), the odds multiplier per standard deviation of Ranking at fixed Presence. *Verdict:* CONFIRMED (Ranking adds) if OR_R ≥ 1.25 and p < .05; FALSIFIED (adds nothing) if OR_R < 1.05; MARGINAL otherwise. *Follows from:* Section 1.2, reading 2; the programme's measurement result (Ranking reported as part of Presence) predicts FALSIFIED, the top-slot reading of P0 predicts CONFIRMED.

**RQ4. Order.** How much does a brand's position in the list change how often it is chosen?

> **H5 `H_Position_List` (SECONDARY; labels, no confirm or falsify).** *Statistic:* d̄, the mean normalised position of the chosen brand (0 = first, 1 = last; 0.5 expected without an order effect, by the balanced design). *Test:* randomisation test, two-sided. *Labels:* order-sensitive if p < .05; order-robust if p ≥ .05 and the 90% bootstrap interval of d̄ lies within [0.45, 0.55]; inconclusive otherwise. *Follows from:* Allouah et al. (2025) on position bias; and from P2's interface condition, since the order of a list is an interface property that, if it moves choice, competes with prominence.

**α and multiplicity.** α = .05 per test, one-sided for H1–H4 (each predicts a direction), two-sided for H5. No correction for multiplicity: there is one primary hypothesis, verdicts rest on pre-set effect sizes as well as p, and every test is reported whatever its result.

---

## 3. Methods

### 3.1 Design overview

One collection, after IPA, in which the same three models (Section 3.3) answer two sets of questions, each call independent of every other (no conversation state, no system prompt, search and all tools off):

1. **Predictor questions** (Section 3.4): the programme's Presence and Ranking questions for the four categories, exactly as asked at t₄ (v0.42): 168 calls per model, 504 in all.
2. **Choice questions** (Sections 3.5–3.6): three buyer briefs per category in two conditions, OPEN (no list) and LIST (the category's live brands in a Latin-square order): 254 calls per model, 762 in all.

| Block (collection order) | Content per model | Calls per model | Calls (3 models) |
|---|---|---|---|
| P1 | Presence/Ranking category questions (Phase B), search off, run 1 | 24 | 72 |
| P2 | Brand questions (Phase A), search off | 96 | 288 |
| P3 | Phase B, run 2 | 24 | 72 |
| P4 | Phase B, run 3 | 24 | 72 |
| C1 | LIST, Latin square 1 in each category | 91 | 273 |
| C2 | OPEN, 4 categories × 3 briefs × 6 runs | 72 | 216 |
| C3 | LIST, Latin square 2 in each category | 91 | 273 |
| **Total** | | **422** | **1,266** |

Plus the v0.23 recognition judge on the 72 open Phase A answers in premium spirits (24 per model; Section 3.4). If the D7 check (Section 3.2) moves Fisker to Cell D, blocks C1 and C3 have 90 calls per model (270 each), the choice blocks 756 calls and the whole collection 1,260 (probe builder, `build_probes_v0_46.py --check --fisker-defunct`); the counts above and the acquisition script's expected count are then redone before the lock. Predictors come first so that a budget stop (Section 3.9) can never leave choices without predictors, and the primary test's first complete Latin square comes before the OPEN block.

### 3.2 Categories, registries and units

**Requirement.** Categories whose brand registries are fixed and whose Presence and Ranking questions are already in use, so that the predictors can be re-measured with an unchanged instrument. The programme's five omnibus registries (v0.19–v0.23, 112 units) meet it; four are used.

| Category (registry) | Units | Live units in LIST | Brief noun |
|---|---|---|---|
| Skincare (v0.20) | 24 | 24 | "a skincare product for my daily routine" |
| Cosmetics (v0.21) | 24 | 24 | "a makeup product" |
| Cars (v0.22) | 24 | 19 | "a new car" |
| Premium spirits (v0.23) | 24 | 24 | "a bottle of premium spirits" |
| **Total** | **96** | **91** | |

**Headphones (v0.19) are excluded** on the programme's conflict-of-interest rule: categories in which the author's employer's group competes stay out (facts in Declarations, Conflict of interest). A study whose outcome is which brand an AI picks for a buyer must not have such a brand among the possible winners. The exclusion also removes the smallest registry (16 units).

**Units not on sale.** The five units v0.22 classes as Cell D "Defunct" (Pontiac, Oldsmobile, Plymouth, Mercury, Saturn; `osf/v22/v22_verdicts.json`, phase_a per_cell D) are not shown in LIST and are not analysis units: a buyer cannot buy a new car of a brand no longer made, and keeping them would inflate the Presence–choice link mechanically. They stay in the coder so that an OPEN choice of one is caught (MC_Defunct), and they are asked in the Phase A recognition questions as at t₄, so the predictor instrument is unchanged. **Fisker** stays as v0.22 classed it unless a dated check finds that it sells no new cars in the US; it is then treated like Cell D (decision D7, 2026-11-14). The check is made before the revision of this manuscript planned for 2027-01-08 by an AI check with a dated source, not a manual one, and logged as a record (`osf/v46/prereg/d7_fisker_v0_46.json`: the question, the time of the check, method `ai_check_dated_source`, the checking model, at least one source with its URL and date, the finding and the decision `live` or `cell_d`). A missing or invalid record counts as pending, and the acquisition script then refuses to start, so no call is made before D7 is settled; the probe file must match the record, and the check must be dated before the first request. If Fisker moves to Cell D: the cars LIST has 18 brands (rows 6, 6, 6 per brief in each square), there are 90 live units, 180 LIST calls per model (540 in all), 756 choice calls and 1,260 calls in all (Section 3.1); the expected call count, the cost estimate and every count below that depends on it are redone for that design before the lock.

> **[DRAFT NOTE]** D7's check has not been made (it needs a model call). The record schema, the rule and the run guard are in the Stage 1 code (code r3); until the record exists every count in this draft is for Fisker live.

**Industry breadth.** The four categories span three industries (beauty, cars, spirits). Breadth is the main weakness of a study confined to the programme's repeat registries; a follow-up on the eight service and retail industries of v0.44, after they have Presence, takes its own protocol and budget (decision D6, 2026-11-14).

**A unit** is (category, brand): Rare Beauty is a unit of skincare and of cosmetics, scored separately. L_g is the number of live units of category g.

**Registry files and coding functions.** Unchanged, read from git: the v0.20–v0.22 content modules' `detect_mention` and the v0.23 brand patterns (`score_v0_23`), exactly as v0.42's coder calls them (`osf/v42/scripts/code_t4_v0_42.py`, git blob 2d36735d), and the v0.23 registry pinned by v1.10 (`osf/methodology/v1_10/registries/v0_23_registry_v1_10.json`). LIST shows each brand by the registry's canonical name.

### 3.3 Model selection: a rule, applied at collection

**Rule (fixed now).** One model per provider, for Anthropic, OpenAI and Google: the provider's newest generally available flagship model, served through the provider's public API, as the provider's own pages state it on the day the rule is applied. *Flagship* means the model the provider's own documentation presents as its most capable generally available model (for example "Latest models", listed first; "Our most capable model"; the top of the provider's "flagship" pricing group). *Generally available* means stated as such, or listed without qualification on the provider's models and pricing pages; restricted (available only to verified organisations), preview, experimental and pre-release models are excluded, and "available on the paid tier" alone does not count as generally available. One flagship per provider (the programme's budget rule; no two models of one provider side by side).

**When and how it is applied.** In the seven days before the collection window opens, by an automated check of each provider's models overview, model page, changelog and pricing page, with the URL, date, time and the wording relied on recorded in the deposit (`osf/v46/data/v46_panel_verification.json`). No step of the check is manual. The rule is applied again on the first day of the window; if the result differs, the second result is used and the change is logged before the first call.

**The rule's result on 2026-11-14** (pre-registration r1, Section 4.3; for orientation only, not a commitment): Claude Fable 5.2 (`claude-fable-5-2`), GPT-6 Astra (`gpt-6-astra`) and Gemini 4 Argon (`gemini-4-argon`); Gemini 4 Carbon was checked and was not shown as generally available in the Gemini API on Google's own pages that day. Collection is several months later (Section 9.3), so the panel will be whatever the rule gives then.

**Why a rule and not names.** The study asks how the models buyers would meet choose; models change between Stage 1 and collection; and because the predictors are re-measured on the same models in the same collection (Section 3.4), whichever models the rule gives, predictor and choice come from the same models at the same time. No comparison in this study needs a particular model name.

**Contingencies (fixed now).**
- If the rule model of any of the three providers cannot be called (no API access, or every request refused), the collection does not start; the change of panel goes to the PCI RR recommender as a Stage 1 amendment before any data exist. (A model lost *during* the collection is handled by the drop rules of Section 5.4.)
- If the rule's models make the high cost estimate of the whole design exceed US$100 (Section 3.9), the design is reduced in this order before any call, by a logged change: (a) the second Latin square (block C3) is dropped (design E, Section 4.4); (b) OPEN runs fall from six to four per brief. Nothing else changes.
- Every served model identifier must equal the requested identifier (a dated snapshot of it is accepted); otherwise the answer is excluded, re-sent and logged (MC_Served).

### 3.4 Predictors, re-measured in the same collection

**Why re-measure.** Presence and Ranking for these four categories were measured on the t₄ wave (v0.42, collected 2026-11-11) and have been seen by the author. PCI RR grades a study by the lowest bias-control level of its parts and treats a key variable as observed once its raw data have been seen. Measuring the predictors again, after IPA and in the same collection as the choices, means that no predictor value used in any confirmatory test exists at submission (Section 8). It also removes the gap in time between predictor and outcome, and lets the panel follow the selection rule without breaking the link between predictor and chooser.

**Instrument (unchanged from t₄).** The probe file is t₄'s, byte for byte, restricted to the four categories: v0.45's `osf/v45/prereg/probes_v0_45.jsonl` reproduces t₄'s probe file and its parity record; the v0.46 builder copies the rows of substrates v20–v23 and asserts their SHA-256 against it.
- **Phase B (category questions), 24 per run:** six per category (for example, for premium spirits, a question about "hidden gems or insider picks among serious spirits enthusiasts"); search off; three runs.
- **Phase A (brand questions), 96:** the 72 yes/no recognition questions of v0.20–v0.22 ("Is the brand X commonly recognized as a brand of …? Answer yes or no.") and the 24 open v0.23 questions ("What do you know about X? …"); search off; one run.

**Coding.** v0.42's locked coder (`osf/v42/scripts/code_t4_v0_42.py`, blob 2d36735d), unchanged, for Phase B mentions and the yes/no recognition codes; the v0.23 recognition judge for the open spirits answers (v0.23's system prompt, user template, 3,000-character truncation, R0–R3 rubric and label parser, unchanged; recognised = R1–R3). **Judge model:** the successor judge that passed v0.45's pre-registered parity check J1 against the Claude Sonnet 4.5 codes of t₃ and t₄ (first candidate Claude Sonnet 5.5, fallback Claude Sonnet 4.6; v0.45 Section 5.1). If that model is not available at collection, J1 is run again, unchanged, on the same t₄ and t₃ answers with the next available Anthropic Sonnet model, before any v0.46 answer is coded; its cost is inside the judge reserve (Section 3.9). If no candidate passes, C_P cannot be computed for premium spirits, the 24 spirits units are left out of every test, and the call thresholds of Section 5.4 are scaled to the remaining categories (from 546 to 402 designed LIST calls). The judge is an instrument with a validated rule; no human codes anything.

**Presence P** of each unit: P = 100 · (C_P/3 + 2 · π̂)/3, computed from the new answers by the functions v1.14 Stage 1 used on t₄ (commit 3129674), unchanged, with the three models of Section 3.3 in place of t₄'s N3.

**Ranking R\*** of each unit: v1.14's `modal_position` on the new Phase B answers, search off, with v1.14's extraction (`extract_wave`, rule `lead_item`) and rating floor (six rankable mentions), unchanged. Units below the floor are unrated.

**Code parity before collection (outcome-neutral, uses only already-public t₄ files).** G1: the v0.46 scorer's P function, run on t₄'s files at `v0.42-scoring-locked`, reproduces v1.14 Stage 1's P_S0 for every unit. G2: its R\* function reproduces Stage 1's stored R\* for every rated unit and asserts the orientation (higher = nearer the top). These gates test code only; the t₄ values they reproduce play no part in any test of H1–H5.

### 3.5 Choice probes (fixed; the probe file reproduces them byte for byte)

Each prompt is a single user message, no system prompt. `{item}` is the brief noun of Section 3.2; `{need}` is one of three briefs; `{options}` is the LIST block.

Briefs:
- **N (no preference):** "I don't have any particular preference."
- **V (value):** "I want good value for my money."
- **Q (quality):** "I want the best quality, and price is not a concern."

OPEN:

> I'm buying {item} and I want you to make the decision for me. {need} Pick one brand. I'll buy whatever you pick, so please choose exactly one brand, not a list. Explain your choice in one or two sentences, then end your reply with a final line in this form:
> CHOICE: <brand name>

LIST (identical, with the options block before the last sentence):

> I'm buying {item} and I want you to make the decision for me. {need} Pick one brand from these options:
> - {brand at position 1}
> - …
> - {brand at position L_g}
>
> I'll buy whatever you pick, so please choose exactly one brand from the options, not a list. Explain your choice in one or two sentences, then end your reply with a final line in this form:
> CHOICE: <brand name>

**Wording choices (declared).** (i) "I'll buy whatever you pick" hands over the decision while leaving the purchase with the buyer; no model is asked to do what it cannot (decision D3, 2026-11-14). (ii) No price, rating, review, sponsorship, retailer or product detail appears (Section 1.4). (iii) Options are plain bullet lines, not numbers, so position is visible as order only, as in a product listing. (iv) The final-line format makes the outcome machine-codable; the short explanation is kept for descriptives and keeps answers short. (v) The buyer is implicitly a US English speaker; the study makes no claim beyond that.

### 3.6 Conditions, design and randomisation

**OPEN.** Six independent calls of the identical prompt per (category, brief, model): 4 × 3 × 6 = 72 per model. Run-to-run variation comes only from each provider's default sampling.

**LIST.** For each (category, model) two independent cyclic Latin squares of side L_g are drawn (seed 460010): the live units are mapped to symbols at random, rows are cyclic shifts, and the rows are shuffled. Each row is one LIST order; across one square every live unit appears exactly once at every position (MC_Design). Rows are assigned to briefs in rotation after a random shuffle (L_g = 24: 8 rows per brief per square; L_g = 19: 7, 6, 6, rotating which brief gets 7 across categories and squares). Each model gets its own squares, so no order is shared across models. Per model 2 × 91 = 182 LIST calls; 546 in all.

The probe file, with every order and its seed, is built and tested before submission and deposited with the Stage 1 manuscript; the seeds are those of r1 (Section 5.1).

### 3.7 Call settings

Search off and no tools of any kind; no system prompt; temperature, top-p and effort at provider defaults, none sent; maximum output 16,384 tokens (not lowered for cost, so that a long deliberation is recorded rather than cut). Anthropic's model through the Message Batches API (same request parameters, 50% token price); the OpenAI and Google models synchronously, as at t₄, with v0.42's retry policy (transient errors retried; an empty answer re-sent once; batched transient errors re-sent up to three attempts; one logged re-run pass inside the window). The acquisition script is a fork of v0.45's `acquire_v0_45.py` (itself forked from t₄'s locked code), with the v0.46 matrix, the guard of Section 3.9 and the stop rule of Section 3.10. The raw file keeps t₄'s schema (`osf/v46/data/v46_raw.jsonl`), plus the fields block, condition, category, brief, square, row and the order shown.

### 3.8 Collection window

All calls within 72 hours, in block order (Section 3.1), alone on the collection computer (no other paid collection of the programme during the window). The window opens at the first free 72-hour slot after both IPA and the close of the programme's AIAS 6.0 path (final synthesis, target about 2027-04-02); its dates are recorded in the budget state file before the first call. The window is short so that every answer reflects one state of each model.

### 3.9 Budget and guard

**Cap.** At most US$100 of paid model calls for this study, re-sends and the judge included; pause at US$80; both computed from the recorded usage of every billed request (programme rule, 2026-11-10).

**Estimate.** From t₄'s recorded token usage, re-priced at the vendors' list prices read on 2026-11-14 (the price table of `osf/v45/scripts/budget_v0_45.py`), every call priced at the price in force from 2026-12-01: Claude Fable 5.2 batch US$4 / US$20 per million input / output tokens; GPT-6 Astra US$10 / US$50; Gemini 4 Argon US$4 / US$20 (its price from 2026-12-01); judge Claude Sonnet 5.5 US$2 / US$10. Choice blocks: central = the mean cost of t₄'s search-off category answers (longer than a one-brand choice, so conservative), +2% for re-sends; high = their 90th percentile, +10% (`cost_estimate_v0_46_r1.py`). Predictor blocks: the recorded cost of exactly the same t₄ calls in these four categories, +2% (central), and the 90th-percentile cost of each call class, +10% (high) (`cost_estimate_v0_46_stage1_r1.py`, written for this manuscript).

| Part | Calls | Central, US$ | High, US$ |
|---|---|---|---|
| Predictor blocks P1–P4 | 504 | 15.11 | 25.77 |
| v0.23 judge (72 answers; reserve counted as spent) | 72 | 2.50 | 2.50 |
| Choice blocks C1–C3 | 762 | 26.53 | 58.11 |
| **Total** | **1,266 + 72** | **44.14** | **86.38** |

Cumulative by block (central / high): after P1–P4 and the judge reserve 17.61 / 28.27; after C1 27.28 / 49.27; after C2 34.47 / 65.39; after C3 44.14 / 86.38 (block sums rounded separately). At the central estimate the US$80 pause is not reached; at the high estimate it is reached during C3, after the primary test's first Latin square and the OPEN block are complete.

**Guard (computed from actual usage).** v0.45's `budget_v0_45.Ledger` with the prices in force on each request's date: spend = the judge reserve + the cost of every raw line already written. Before a request is sent its worst case is reserved (2,000 input tokens, output at the 16,384-token cap; a synchronous request reserves two, since an empty answer is re-sent once; a batch is cut to the requests whose worst cases fit). (i) **Hard stop:** no request is sent if spend + reservations + its worst case would exceed US$100. (ii) **Pause at US$80:** once spend reaches US$80, no new request until the author's approval is recorded (an approval, not a check). (iii) **Projection pause:** after block C1, if spend + (C1's actual cost) × 489/273 (the remaining OPEN and LIST calls) exceeds US$100, collection pauses before C2 and the author decides; the hard stop still applies. At the high estimate the projection is 49.27 + 21.00 × 489/273 = US$86.89, so (iii) is not reached. **Prices are re-read at collection**, and the estimate is recomputed with them and with the rule's models before the first call; if the high estimate then exceeds US$100, the contingency of Section 3.3 applies.

### 3.10 Length-limit stop rule

No answer may stop at the output-token limit before it gives the outcome the block measures (programme rule, 2026-11-12). *At the limit* means the provider's finish reason is its length stop (Anthropic `max_tokens`; OpenAI `length` or `incomplete:max_output_tokens`; Google `MAX_TOKENS`) or, without a finish reason, output tokens (Google: plus thinking tokens) reach 16,384. *Cut before the outcome* means, in a choice block, at the limit with no `CHOICE:` line; in a predictor block, at the limit with no complete answer text. **Trigger:** one such answer from any model. **Action:** that model is paused at once (no further request for it); the others go on; the trigger is written to `osf/v46/data/v46_stoprule.jsonl` with the call ID, finish reason and token counts; the pause holds until the author decides, and the decision is a DEVIATIONS entry. A cut answer stays in the raw file and is treated as missing, never as NONE. No call setting changes during the collection; answers under a changed setting would form a separate arm, reported apart. Evidence so far: the expected models under these settings passed the programme's pre-lock length check of 2026-11-13 (largest thinking 2,252 of 16,384 tokens), and none of t₄'s 876 answers stopped at the limit.

### 3.11 Three roles of AI in this study

AI appears in three roles, kept apart. (1) **The object measured:** the three chooser models, which answer the Presence, Ranking and choice questions. (2) **An instrument:** the v0.23 recognition judge, used only with its pre-registered rubric and only after passing its parity check (Section 3.4). (3) **The author's assistant:** design, analysis code and drafting (Declarations, Use of AI tools). No choice is coded by a model; coding is deterministic (Section 5.3).

### 3.12 Scope: search and tools are not part of this protocol

The models answer with search and every tool off. On 2026-11-14 the author decided that #76 has no search-on arm (decision D4), and on 2026-11-21 kept that decision when a draft tools arm (provider web search on) was proposed. A tools arm is not part of this study; it is left to a separate future study.

---

## 4. Sampling plan and a priori power analysis

### 4.1 What limits precision

The sample is fixed by the design: 91 live brands in four categories, three models, 546 LIST choices and 216 OPEN calls. Published agent experiments report that choices concentrate on a few items (Allouah et al. 2025). Under concentration, the effective sample of the primary test is the number of distinct brands chosen per category, not the number of calls: a model that picks the same brand in every row of a Latin square contributes one brand's worth of information however many rows there are. The permutation test of Section 5.2 is built for that case, because it holds the observed pattern of choices fixed and breaks only its link to the predictor. Power is therefore set by the number of brands and categories and by how concentrated the choices are, and the budget is best spent on the predictors, on balance across positions, and on three providers, not on more repetitions.

### 4.2 Method and assumptions

A simulation, written for this manuscript (`osf/v46/scripts/power_analysis_v0_46_stage1.py`; output `osf/v46/prereg/power_analysis_v0_46_stage1_r1.json` and `.txt`; seed 46760; 400 simulated studies per scenario for H1, H2; 100 for H3, H4; 200 for H5; 1,000 permutation draws per study, 200 Freedman–Lane draws for H4; the pre-registered analysis uses 10,000 and 2,000). It extends the precision simulation of the study's first draft (`precision_sim_v0_46.py`, whose unit values and generator it imports unchanged). Assumptions:

- **A1 Units.** The four categories' brands with the relative prominence they had at t₄ (recall Presence π̂ from v0.42's brand table at `v0.42-scoring-locked`; cars without Cell D), standardised within category. The t₄ values serve only as a realistic spread of prominence across brands; they are not used in any test.
- **A2 Choice.** Each of three models chooses by a multinomial logit on scale × (β · z + a brand appeal shared by the models, SD 1, + a model-specific appeal, SD 0.5). Scale 2 gives *concentrated* choices (about 70–84% of choices on the top three brands of a category), scale 0.7 *diffuse* choices (about 36–46%).
- **A3 Re-measurement.** The re-measured predictor equals r · z + √(1 − r²) · e, with r = 1 (no noise) or r = 0.81, the lowest per-brand Presence stability the programme has measured where it was defined (v0.34, SSRN 6915458).
- **A4 Effect sizes are set on the test statistic.** β is calibrated so that the expected Ū on the re-measured predictor equals the target: 0.60 (the FALSIFIED bound), 0.65, 0.70 (the CONFIRMED bar, which is the smallest effect of interest for the verdict) and 0.75; and 0.50 for the null.
- **A5 OPEN.** 30% of OPEN answers name a brand outside the registry. This is an assumption, not a measured value; no OPEN answer exists.
- **A6 Ranking.** Rated brands are the most prominent n per category (n = 13, 15, 14, 18, the t₄ counts); their R\* correlates 0.369 with prominence (the t₄ within-category value, v1.14 Stage 1). Ranking's added effect is varied (generating log-odds 0, 0.15, 0.30, 0.45 per SD at fixed Presence).
- **A7 Position.** A linear order effect, calibrated so that the expected d̄ = 0.45, the edge of the pre-declared order-robust band.

### 4.3 Results

**H1 (primary; 546 LIST choices, two squares per model).**

| True Ū_P | Choices | r | P(p < .05) | P(CONFIRMED) | P(MARGINAL) | P(FALSIFIED) |
|---|---|---|---|---|---|---|
| 0.50 (null) | concentrated | 0.81 | 0.048 | 0.000 | 0.068 | 0.932 |
| 0.50 (null) | diffuse | 0.81 | 0.075 | 0.000 | 0.000 | 1.000 |
| 0.60 | concentrated | 0.81 | 0.487 | 0.098 | 0.497 | 0.405 |
| 0.60 | diffuse | 0.81 | 0.988 | 0.000 | 0.540 | 0.460 |
| 0.65 | concentrated | 0.81 | 0.718 | 0.200 | 0.578 | 0.223 |
| 0.65 | diffuse | 0.81 | 1.000 | 0.043 | 0.922 | 0.035 |
| **0.70** | **concentrated** | **0.81** | **0.892** | 0.507 | 0.435 | 0.058 |
| 0.70 | concentrated | 1.00 | 0.938 | 0.480 | 0.465 | 0.055 |
| **0.70** | **diffuse** | **0.81** | **1.000** | 0.475 | 0.525 | 0.000 |
| 0.75 | concentrated | 0.81 | 0.985 | 0.833 | 0.165 | 0.003 |
| 0.75 | diffuse | 0.81 | 1.000 | 0.970 | 0.030 | 0.000 |

Readings. (i) The test holds its nominal false-positive rate under the null (0.040–0.075 across the four null scenarios of this design, 400 studies each; 0.028–0.075 across all twelve, with one, two or four squares). (ii) **At the smallest effect of interest, Ū_P = 0.70, the power of the significance test at α = .05 is 0.89 with concentrated choices and a noisy re-measured predictor (r = 0.81), 0.94 without the noise, and 1.00 with diffuse choices.** (iii) The verdict CONFIRMED needs both p < .05 and an observed Ū_P ≥ 0.70; when the true value sits exactly at the bar, the observed value falls on either side about equally often, so CONFIRMED comes out about half the time and MARGINAL otherwise. This is a property of a verdict that uses an effect-size bar, stated here so that a MARGINAL at a true value near 0.70 is not read as a failure of the design. At a true Ū_P of 0.75, CONFIRMED comes out 83–97% of the time. (iv) A true value at the FALSIFIED bound (0.60) is called FALSIFIED 40–46% of the time and CONFIRMED at most 10%; a false CONFIRMED under the null did not occur in any of the 1,600 null studies of this design (it occurred in 2 of 400 with one square, concentrated, r = 1).

**Number of Latin squares.** One, two or four squares give the same H1 power (true Ū_P = 0.70, concentrated, r = 0.81: P(p < .05) = 0.853, 0.892 and 0.902 for 273, 546 and 1,092 choices; P(CONFIRMED) = 0.525, 0.507, 0.482). This confirms Section 4.1: precision comes from brands, not calls.

**H2 (OPEN; 216 calls, 30% outside the registry assumed).** Null: P(p < .05) = 0.055 (concentrated), 0.037 (diffuse). At true Ū_P = 0.70: power 0.88 (concentrated), 1.00 (diffuse); CONFIRMED 0.52 and 0.48. UNDETERMINED (fewer than 120 valid OPEN choices) at most 0.7% of studies.

**H3 (Ranking, choices on rated brands).** With no added Ranking effect, H3 reaches p < .05 in 19% of studies, because R\* carries part of Presence (correlation 0.369) and Presence drives choice; this is the reason H3 is declared conditional and H4 is the separating test. With an added effect of 0.15, 0.30 and 0.45 per SD: 24%, 36% and 49%.

**H4 (Ranking beyond Presence; concentrated, r = 0.81).**

| Generating effect | Mean fitted OR_R | P(p < .05) | P(CONFIRMED) | P(FALSIFIED) |
|---|---|---|---|---|
| 0 (none) | 1.16 | 0.10 | 0.10 | 0.48 |
| 0.15 | 1.25 | 0.15 | 0.15 | 0.35 |
| 0.30 | 1.35 | 0.17 | 0.17 | 0.23 |
| 0.45 | 1.49 | 0.30 | 0.30 | 0.14 |

Readings. **H4 has low power: about 0.15 at its smallest effect of interest (OR_R = 1.25).** Only rated brands enter (about 60), and a brand appeal shared across models adds variance that calls cannot average away. A second finding matters more for interpretation: with a noisy re-measured Presence (r = 0.81), Ranking absorbs part of the Presence it is correlated with, so OR_R is biased upward under no true Ranking effect (mean 1.16) and the test rejects in 10% of null studies (100 studies; simulation standard error about 0.03). A CONFIRMED H4 is therefore weak evidence that Ranking adds to Presence, and it is reported with this caveat; a FALSIFIED H4 is the more informative outcome. H4 stays secondary for both reasons. No design within US$100 changes this, because the number of rated brands, not the number of calls, sets it.

**H5 (position).** Null: P(p < .05) = 0.055–0.065. At d̄ = 0.45: power 0.99 (concentrated) and 0.97 (diffuse) with two squares; 0.82 and 0.70 with one. The second square is what makes the position analysis well powered, and it is the main reason for design A over design E below.

### 4.4 Design under the budget

| Design | Calls (choice + predictor) | Central, US$ | High, US$ | H1 power at Ū_P = 0.70 (conc., r = 0.81) | H5 power at d̄ = 0.45 (conc.) |
|---|---|---|---|---|---|
| **A adopted (2026-11-22): 2 squares + OPEN 6 runs** | **762 + 504** | **44.14** | **86.38** | **0.89** | **0.99** |
| E: 1 square + OPEN 6 runs | 489 + 504 | 34.47 | 65.38 | 0.85 | 0.82 |
| F: 4 squares + OPEN 12 runs | 1,524 + 504 | 70.66 | 144.50 | 0.90 | not simulated |

Costs include the predictor blocks and the US$2.50 judge reserve (`cost_estimate_v0_46_stage1_r1.txt`). Design F does not fit the cap at the high estimate and buys nothing for H1. Design A fits at both estimates; at the high estimate it reaches the US$80 pause in its last block, after the primary test's first square and the OPEN block (Section 3.9). Design E is the pre-specified fallback if prices at collection push A's high estimate above US$100 (Section 3.3).

**Smallest effect of interest, stated.** Ū_P = 0.70 for H1–H3 (the chosen brand outranks a randomly drawn listed brand on the predictor seven times in ten, the conventional floor of "acceptable" discrimination for a predictor); OR_R = 1.25 per SD for H4; d̄ = 0.45 for H5. These bars were fixed before any choice existed. PCI RR sets no minimum power; Peer Community Journal lists none. H1's power at its smallest effect of interest is 0.89 or more in every scenario simulated; H4's is low and is declared as such.

---

## 5. Analysis plan

All statistics are computed by `osf/v46/scripts/score_v0_46.py`, written and tested on synthetic data before submission, deposited with the Stage 1 manuscript (its SHA-256 recorded), and run once after collection and coding.

### 5.1 Definitions

- **Calls.** OPEN call = (category, brief, model, run); LIST call = (category, brief, model, square, row). Every call is independent.
- **Choice.** The brand on the answer's final `CHOICE:` line, coded to the category's registry (Section 5.3): a live unit (valid choice); OTHER (OPEN only: the choice line names something that is no registry unit, a written refusal included); OFF_LIST (LIST only: the choice line names something that is not a unit on the list shown, a written refusal to choose included); DEFUNCT (a Cell D brand); AMBIGUOUS (two or more registry brands); NONE (a refusal flagged by the provider, or a choice line with nothing on it). Answers that are not outcomes (unanswered, served by another model, or cut at the output limit before a `CHOICE:` line) are coded MISSING and treated as missing (Section 3.10).
- **Predictors.** P and R\* of each unit, from the collection's own predictor blocks (Section 3.4). R\* is defined only for rated units (at least six rankable mentions).
- **Within-category percentile.** For a predictor X and a unit b of category g: u_X(b) = (rank of X_b among the live units of g − 0.5) / L_g, average ranks for ties; u ∈ (0, 1). For R\*, ranks are among the rated live units of g and L_g is their number.
- **Choice percentile Ū_X.** The mean of u_X(chosen unit) over the valid choices of a condition. Ū_X = 0.5 when choice is unrelated to X; Ū_X = 1 − 0.5/L_g when every choice goes to the top unit. Ū_X equals the choice-weighted probability that the chosen brand outranks a randomly drawn listed brand on X (ties counted half), i.e. a choice-weighted area under the ROC curve.
- **Permutation p (H1–H3).** One-sided. X permuted among the live (for R\*: rated) units within each category, the same permutation for every choice in that category; Ū_X recomputed exactly as observed; 10,000 draws; p = (1 + #{Ū_perm ≥ Ū_obs}) / 10,001, a draw counting as a hit if Ū_perm ≥ Ū_obs − 10⁻¹². This null keeps the observed concentration of choices and breaks only their link to X.
- **Bootstrap interval.** 90% percentile interval from 10,000 resamples of calls within (category, model) strata; reported beside every statistic, never a verdict input (except H5's order-robust label, Section 2).
- **Seeds.** 460001 (H1), 460002 (H2), 460003 (H3), 460004 (H4), 460005 (bootstrap), 460006 (H5), 460010 (Latin squares and their assignment to calls).

### 5.2 Tests

- **H1.** LIST, all valid choices, X = P: Ū_P, permutation p (seed 460001), bootstrap interval. Verdict as Section 2.
- **H2.** OPEN, valid choices (live units), X = P: Ū_P, permutation p (seed 460002).
- **H3.** LIST, valid choices on rated units, X = R\*: Ū_R, permutation p among rated units (seed 460003). Categories with at least five rated units enter.
- **H4.** LIST calls whose valid choice is a rated unit; choice set = the rated live units of that list (unrated options dropped; the independence-of-irrelevant-alternatives assumption of the conditional logit is declared). Conditional logit: utility of option b in call i = β_P · z(u_P(b)) + β_R · z(u_R(b)) + γ₁ · [b shown first] + γ_L · [b shown last] + γ_d · (position − 1)/(L_g − 1), z standardised within category over rated live units; as in H3, categories with at least five rated units enter. One-sided Freedman–Lane permutation p for β_R (seed 460004): within each category, u_R regressed on u_P over rated units (ordinary least squares), residuals permuted among those units and added back to the fitted values, the model refitted; 2,000 draws. OR_R = exp(β_R).
- **H5.** d̄ = mean normalised position (position − 1)/(L_g − 1) of the chosen unit over valid LIST choices. Randomisation test (seed 460006, 10,000 draws): within each (category, model, brief), the orders actually used are reassigned at random to that stratum's calls, the chosen unit of each call held fixed and its position read from the reassigned order; two-sided p. Also: primacy ratio PR₁ = share of valid choices at position 1 × mean L_g; shares by position tercile, with bootstrap intervals; the position terms γ₁, γ_L, γ_d of H4's model fitted on all valid LIST choices with P only.

### 5.3 Coding the choice

- **The choice line.** The last line of the visible answer that begins with `CHOICE:` (case-insensitive, after Markdown emphasis is removed); if none, the answer's last non-empty line. URLs are removed before matching.
- **Brand matching.** The category's certified function (v0.20–v0.22 `detect_mention`; v0.23 `score_v0_23` patterns) applied to the choice line only: exactly one registry unit → that unit (DEFUNCT if Cell D; OFF_LIST if LIST and the unit is not on the list shown); two or more → AMBIGUOUS; none → if the line names something (at least one letter or digit), OFF_LIST in LIST and OTHER in OPEN, else NONE. A brand outside the registry is therefore OFF_LIST in LIST and OTHER in OPEN, as Section 5.1 defines them. For OTHER and OFF_LIST, the line's text is kept verbatim for descriptives; no attempt is made to map it to a registry.
- **Refusals.** A refusal flagged by the provider (Anthropic `refusal`, OpenAI refusal content, Google `SAFETY` or a blocked prompt) is coded NONE and counted. A refusal written in the answer text is coded like any other answer: in LIST, an answer with no `CHOICE:` line whose text matches the coder's fixed explicit-refusal pattern (first person with can't, won't, unable to or decline, followed by choose, pick, select, recommend, decide or make a choice; set before any data) and whose last line names no registry unit is OFF_LIST, because the model was shown the list and did not choose from it; in OPEN, a written refusal is OTHER under the rule above.
- **Coder.** `osf/v46/scripts/code_v0_46.py`, deterministic, written and tested on synthetic answers before submission, with adversarial cases fixed in its tests: a choice line naming two brands; a brand in the reason but not on the choice line; "Estée Lauder" against "Estee Lauder"; "Dior" (skincare unit "Dior Beauty"); a Cell D car; an answer without a choice line.
- **Blinding.** The coder sees answers and registries only; it never reads P or R\*. The scorer joins them after coding. No person codes any answer.

### 5.4 Exclusions, drop rules, missing data, UNDETERMINED

- Excluded from every test: calls not answered after the re-run pass; calls served by another model; calls outside the window; answers cut before the outcome (Section 3.10); choices coded NONE, AMBIGUOUS, OTHER, OFF_LIST and DEFUNCT. Every exclusion is counted per model × condition × category.
- **Model drop.** A model × condition with fewer than 90% of its calls answered (of 182 LIST and 72 OPEN calls per model; 134 and 54 if premium spirits is left out) or fewer than 70% of its answered calls codable is dropped. *Codable* counts every answer coded to a choice outcome: VALID, OTHER, OFF_LIST (written refusals in LIST included) or DEFUNCT; AMBIGUOUS and NONE are not codable. A model × condition so dropped is removed from that condition's tests, which become UNDETERMINED (H1–H5 need the three choosers; a reduced panel is reported as a sensitivity). A model whose predictor blocks are below 90% answered is dropped from every test.
- **Minimum valid choices.** H1 UNDETERMINED if fewer than 450 valid LIST choices remain; H2 if fewer than 120 valid OPEN choices; H3 and H4 if fewer than 200 valid LIST choices fall on rated units. If premium spirits is left out (Section 3.4), 450 becomes 331 and 200 becomes 147 (scaled by 402/546), and 120 becomes 90 (scaled by 3/4).
- Calls not sent because of a budget stop or a stop-rule pause count as unanswered. No imputation. Rates use valid choices as the denominator.

### 5.5 Position and order

Besides H5: every Ū (H1–H3) is also computed with the first and the last position of each list excluded (S-Pos-a), and H1's link is re-estimated in the conditional logit of H4 with P and the position terms only (S-Pos-b: the odds ratio of P per standard deviation, controlling position). If H5 reads order-sensitive, H1 is reported with S-Pos-a and S-Pos-b beside it in the same table.

### 5.6 Outcome-neutral checks (positive controls and manipulation checks)

Each is checked before the hypotheses are read, and its result is reported first.
- **MC_Design (before submission).** The probe file shows every live unit at every position exactly once per Latin square, per (category, model); the builder's test asserts it.
- **G1, G2 (before collection).** Code parity on t₄'s public files (Section 3.4).
- **MC_Probes.** The predictor probes equal t₄'s byte for byte (SHA-256).
- **MC_Complete.** At least 98% of the 1,266 calls end with non-empty answer text after the retry policy.
- **MC_Codable.** Share of answered choice calls with a valid choice, per model × condition; below 85% flagged. The drop rule uses the codable share instead (below 70% drops the model × condition; Section 5.4).
- **MC_OnList.** Share of LIST choices coded OFF_LIST; above 5% flagged.
- **MC_Defunct (positive control on the outcome side).** Share of OPEN choices coded DEFUNCT. Expected near 0; above 2% flags the coding or the briefs, and the paper reports it before any test.
- **MC_Predictor (positive control on the predictor side).** The re-measured P separates the brands: in every category, the within-category spread of P (interquartile range) is at least 10 points on the 0–100 scale, and at least one brand per category is recalled by every model. A category that fails is flagged and every test is also reported without it; the flag never changes a verdict, which is computed on all categories as Sections 5.2 and 5.4 define. Reason: a predictor with no spread cannot predict anything, whatever the models choose. (New in this protocol; approved 2026-11-22, Appendix B, item 5.)
- **MC_Judge.** The v0.23 judge used is the J1 winner (or passes J1 again; Section 3.4).
- **MC_Served, MC_Truncation, MC_Window, MC_Budget.** As Sections 3.3, 3.10, 3.8 and 3.9; MC_Truncation flags a model × condition with more than 5% of calls ending at the output cap.

### 5.7 Pre-registered descriptives (no verdicts)

1. Choice shares per unit, condition, brief and model; the five most chosen brands per category and model.
2. OPEN: share OTHER, and the OTHER brands named (top 10 per category); share of OPEN choices equal to the same model's modal LIST choice for the same brief (a tie for the mode goes to the unit first in alphabetical order).
3. Model agreement: share of (category, brief) cells in which all three models' modal choices coincide.
4. Brief effects: Ū_P per brief.
5. Own-model link: for each chooser, Ū with its own recall π̂_m from the same collection.
6. Refusals and hedges: share of answered choice calls that decline to choose, or choose while saying the model cannot buy. A decline is an answer coded NONE (provider-flagged refusals among them, counted separately); written refusals coded OFF_LIST (LIST) or OTHER (OPEN) are not counted as declines. A hedge is an answer with a coded choice whose text matches the coder's fixed cannot-buy pattern (the model says it cannot itself buy, purchase or order).
7. Concentration: share of choices on the top three units per category; Herfindahl index; distinct units chosen.
8. Answer form and cost: words per answer, output and thinking tokens, spend per model × block.

### 5.8 Sensitivities (each reported beside its test; a verdict change is listed next to the verdict)

- **S-COI.** Every test without the five units named in the conflict-of-interest declaration (Chevrolet, BMW, Bentley, Jack Daniel's, Eucerin; Declarations).
- **S-Recall.** π̂ (recall only) in place of P.
- **S-LOCO.** Leave one category out, each in turn.
- **S-Model.** Each test per chooser.
- **S-Pos-a, S-Pos-b.** Section 5.5.
- **S-Panel.** If a model is dropped (Section 5.4), the tests on the remaining models.

In the sensitivities the effect-size and p rules of Section 2 apply, the minimum-valid-choice rule of Section 5.4 does not (a single model or three categories could never reach 450 choices). There is no search-on Presence sensitivity: re-measuring Presence with search on would need search-on calls, which this study does not make, and t₄'s search-on values are already observed (decided 2026-11-22, Appendix B, item 4).

### 5.9 Exploratory analyses, declared as such

These use data already observed (t₄, v0.42) and are never verdict inputs: (i) stability of P and R\* between t₄ and this collection (within-category Spearman), where the models are the same; (ii) Ū_P with t₄'s P in place of the re-measured P, to show how much a predictor measured months earlier loses. Any other analysis not listed in Sections 5.2–5.8 is reported as exploratory, in a separate section of the Stage 2 report.

### 5.10 Reporting

Every test, including failures and undetermined results, per model, category and brief. The Stage 2 title or abstract states that the outcome is a model's stated choice, not a purchase. The data (raw answers, coded choices, predictors), the code, the probe file and the deposit manifest go to OSF (project ec6wh). Any deviation from this protocol after IPA is a dated entry in `osf/v46/DEVIATIONS.md`, written before the affected data are analysed where possible, and reported in Stage 2 with its effect on every test; no deviation turns a computed verdict.

---

## 6. Study design summary table

| Question | Hypothesis | Sampling plan | Analysis plan | Rationale for the sensitivity of the test | Interpretation given different outcomes | Theory that could be shown wrong |
|---|---|---|---|---|---|---|
| RQ1. Does a model choosing from the full list pick high-Presence brands? (PRIMARY) | H1: the chosen brand tends to have high Presence (P re-measured in the same collection). | 3 models (rule, Section 3.3) × 4 categories × 2 Latin squares: 546 LIST calls; P from 504 predictor calls in the same 72-hour window. | Ū_P over valid LIST choices; one-sided within-category permutation p, 10,000 draws; 90% bootstrap interval. CONFIRMED Ū_P ≥ 0.70 and p < .05; FALSIFIED Ū_P < 0.60; MARGINAL otherwise; UNDETERMINED if a model is dropped or < 450 valid choices. | SESOI Ū_P = 0.70. Simulated power of the test at SESOI 0.89 (concentrated choices, noisy predictor r = 0.81) to 1.00; false-positive rate 0.040–0.075 (Section 4.3). | CONFIRMED: Presence predicts what a model chooses when a buyer delegates; named → chosen holds. FALSIFIED: the single pick does not follow the prominence Presence records. MARGINAL: a link weaker than the bar, or a true value near it; reported with its interval. | P0 (one mechanism behind naming and single-recommendation output) and P1 (reinforcement as the modal outcome), at the model step. |
| RQ2. Do free choices land on high-Presence registry brands, and how often outside the registry? | H2: free choices on registry brands tend to have high Presence. | 3 models × 4 categories × 3 briefs × 6 runs: 216 OPEN calls. | As H1 on valid OPEN choices; UNDETERMINED if < 120 valid choices. Share OTHER reported. | Power at SESOI 0.88–1.00 assuming 30% OTHER (Section 4.3). Declared partly mechanical. | CONFIRMED is expected and weaker evidence than H1. FALSIFIED would mean free choice departs from Presence even within the registry. A large OTHER share shows how much choice falls outside the measured brands. | P1 in the realistic setting; mainly descriptive. |
| RQ3a. Does the Ranking score predict the listed brand chosen? | H3: the chosen brand tends to have high R\*. | As H1; choices on rated units (≥ 6 rankable mentions in the same collection). | Ū_R; permutation among rated units; verdict as H1; UNDETERMINED if < 200 valid choices on rated units. | Declared: R\* correlates with P (0.369 at t₄), so H3 can reject through Presence alone (19% of null-Ranking studies). | CONFIRMED is not evidence that Ranking adds to Presence (H4 decides). FALSIFIED: position in lists does not predict the pick even unconditionally. | The top-slot reading of P0 (Section 1.2, reading 2). |
| RQ3b. Does Ranking add to Presence? | H4: among rated brands, Ranking predicts choice beyond Presence. | As H3. | Conditional logit with P, R\* and position terms; one-sided Freedman–Lane p for β_R, 2,000 draws. CONFIRMED OR_R ≥ 1.25 and p < .05; FALSIFIED OR_R < 1.05; MARGINAL otherwise. | SESOI OR_R = 1.25. Power about 0.15 at SESOI; OR_R biased upward (mean 1.16) under no effect when P is noisy (Section 4.3). Declared low power. | CONFIRMED: weak evidence that the MODE statistic carries information Presence lacks; does not change Ranking's status. FALSIFIED: for choice, Ranking adds nothing to Presence, as v1.16's result predicts. | The programme's measurement claim that Ranking is part of Presence (v1.16), against the top-slot reading of P0. |
| RQ4. Does list position change the choice? | H5 (labels): position changes how often a brand is chosen. | As H1; every unit at every position twice per model and category. | d̄; two-sided randomisation test within (category, model, brief); order-sensitive if p < .05; order-robust if p ≥ .05 and the 90% interval of d̄ is within [0.45, 0.55]; inconclusive otherwise. | SESOI d̄ = 0.45; power 0.97–0.99 with two squares (0.70–0.82 with one). | Order-sensitive: list order moves AI choice, and H1 is read with its position-controlled versions (S-Pos-a, S-Pos-b). Order-robust: choice follows the brands, not their place. | Position bias in AI agents (Allouah et al. 2025) for these models; P2's interface condition. |

---

## 7. What the results will mean, and what they will not

- **The study measures** which brand a model says it would choose for a hypothetical US buyer, from a neutral brief, without web search or tools, in one 72-hour window, and whether that choice follows the brand's Presence and Ranking measured on the same models in the same window.
- **It does not measure** purchases, sales, market share, agent behaviour on a real store, or what any person would choose. A CONFIRMED H1 says that AI Presence predicts AI choice; whether AI choice predicts demand is the next link, tested elsewhere.
- **Component decision.** Whether "chosen" becomes a part of the AIAS score is not decided by any verdict here. Three readings are fixed now: (a) H1 CONFIRMED and H4 not CONFIRMED → choice is behavioural evidence for Presence's validity, not a new component; (b) H1 MARGINAL or FALSIFIED with stable, model-consistent choices (high model agreement, H5 not order-sensitive) → choice carries information Presence lacks and is a candidate component, to be specified in its own instrument paper; (c) choices unstable across models, briefs or orders (H5 order-sensitive, low model agreement) → choice is reported as a property of the models, not of brands, and is not proposed as a component.
- **Ranking.** H3–H4 are behavioural evidence on the MODE statistic. Ranking stays reported as part of Presence whatever they show; a CONFIRMED H4 would be a reason to revisit that, not a revision.
- **Theory.** H1 FALSIFIED would be evidence against P0 and P1 as statements about AI output at the step from naming to a single recommendation, for these categories and models. H1 CONFIRMED is consistent with them but does not test P2–P4, which concern human choice.

### 7.1 Limitations

1. Stated choice, not behaviour: an answer to a prompt, without a store, prices, stock, ratings or a budget; real agents act on far richer pages (Allouah et al. 2025; Cherep et al. 2025).
2. Four categories in three industries (beauty, cars, spirits), one market and language (US English); headphones excluded for conflict-of-interest reasons.
3. Predictor and outcome come from the same models, so a link can partly reflect a model's agreement with itself rather than a property of the brands; descriptive 5 reports the own-model link, and the design cannot separate the two.
4. Search off only; agents that shop usually search (Section 3.12).
5. The list mixes price tiers (a drugstore moisturiser beside La Prairie; Kia-class cars beside Bentley); briefs V and Q let tier matter, brief N leaves it to the model.
6. R\* exists only for rated brands, and Ranking's validity as a separate score is not established (Section 1.3); H4 has low power and an upward bias when Presence is measured with noise (Section 4.3).
7. Provider-default sampling: OPEN runs vary only as much as each provider's defaults let them.
8. The Anthropic model runs through the Message Batches API, the others synchronously.
9. The panel is fixed by a rule at collection, so the models are not known at Stage 1; the study answers its questions for whatever models the rule gives, and generalises to other models only as far as model dependence allows.

---

## 8. Bias-control statement

**Level requested: 6.** PCI RR's Level 6 requires that no part of the data or evidence that will be used to answer the research question yet exists. At submission:

- **No outcome data exist.** No model has been asked any choice question of this study, and no probe file has been sent.
- **No predictor data used in any confirmatory test exist.** Presence and Ranking enter every hypothesis test only as re-measured in the post-IPA collection (Section 3.4). Earlier values for these brands (t₄, v0.42, 2026-11-11) exist and have been seen by the author; they are used only (i) to test that the scoring code reproduces the published definitions (gates G1, G2; code only), (ii) as a realistic spread of brand prominence in the power simulation (Section 4.2), and (iii) in two exploratory analyses declared in Section 5.9, which are never verdict inputs.
- **What the author knows.** The author knows the t₄ Presence and Ranking values of these brands and the published results of the programme. This is prior knowledge of the predictor's past values, not of the outcome, and it shaped the choice of categories and the power assumptions, which are stated. All hypotheses, thresholds and seeds were fixed on 2026-11-11, before any choice existed.
- **Countermeasures kept from the first draft** in case the recommender grades the study below Level 6: thresholds fixed in advance; a coder that never reads the predictors (Section 5.3); a scorer tested on synthetic data and run once; the predictor instrument unchanged from t₄ and verified by SHA-256.

PCI RR decides the level; this statement gives it the facts.

> **[DRAFT NOTE]** Pablo's decision of 2026-11-17 (item 4) is to re-measure inside #76 "to keep Level 6", confirmed on 2026-11-22 (Appendix B, item 13: request Level 6 and state the facts). Whether PCI RR accepts Level 6 when earlier values of the same predictors have been seen is PCI RR's call and was not verified; the venue plan (claude/venue-plan.md, section c) flags it as the main risk. The statement above is written to give the recommender the facts plainly.

---

## 9. Ethics, data availability and timeline

### 9.1 Ethics

No human participants, no personal data and no animals: the subjects are AI models reached through their providers' public APIs under the providers' terms. No purchase is made; no seller, retailer or brand is contacted; no web page is browsed or scraped. No ethics approval is required for this design, and none has been sought: with no participants and no personal data, no institutional review applies. PCI RR asks that approvals be in place before Stage 1; none applies, and this statement is given in place of an institutional letter.

### 9.2 Data and code

Before submission: the probe file, the builder, coder, scorer and acquisition code with their tests, the cost and power scripts and their outputs, and `osf/v46/DEVIATIONS.md` with Entry 0 (the ex-ante conflict-of-interest screen), deposited with the Stage 1 manuscript on OSF (project ec6wh, a component of its own). At IPA, PCI RR registers the approved Stage 1. After collection: the raw answers, coded choices, re-measured predictors, budget state and stop-rule logs, deposited with the Stage 2 report.

### 9.3 Timeline (estimates)

| Step | Date (estimate) |
|---|---|
| Stage 1 submitted to PCI RR (standard track) | about 2027-01-15 |
| First Stage 1 decision (standard track, about 4–8 weeks) | about mid-February to mid-March 2027 |
| In-principle acceptance | about March–April 2027 |
| Collection (72 hours) | first free slot after IPA and after the programme's final synthesis (target about 2027-04-02) |
| Coding and scoring (deterministic; run once) | within two weeks of collection |
| **Stage 2 submitted** | **about July 2027** |

If IPA comes later, only this study moves.

---

## Declarations

### Conflict of interest

The author is Director, Corporate Brand Creative and Governance at Samsung Electronics America. This study re-uses brand registries fixed in earlier phases (v0.20–v0.23) and performs no new brand selection; each registry carries its source-phase conflict-of-interest handling forward unchanged, and the screen of this study's registries is recorded ex ante as DEVIATIONS Entry 0 (`osf/v46/DEVIATIONS.md`). The audiophile-headphones category (v0.19) is not used, because the Samsung group sells headphones through Harman International, a Samsung subsidiary since March 2017 (deal agreed November 2016), which owns AKG, JBL and, since September 23, 2025, the Sound United brands, Denon among them (What Hi-Fi, 2025-09-23, https://www.whathifi.com/hi-fi/harman-now-owns-bowers-and-wilkins-marantz-and-denon-as-masimo-deal-completes). Denon, which v0.19 chose in place of AKG, was therefore already a Samsung-group brand. In the automotive registry, Samsung subsidiaries hold tier-2/3 component supply relationships with several registry brands — Harman International (audio systems), Samsung SDI (battery cells), and Samsung Display (infotainment) — characterized in the source phase as non-competitive, with no brand-level overlap, and imposing no operational restriction on registry composition (v0.22 Declarations; screened in v0.22 DEVIATIONS Entry 0, Part B). Samsung's affiliate Cheil Worldwide, or its Iris agency, has done agency work for five registry brands used here (Chevrolet, BMW, Bentley, Jack Daniel's, Eucerin; v0.62 DEVIATIONS Entry 0, Part F); every result is also reported without them (S-COI). Acquisition, coding and scoring are automated against the locked registries, and this protocol is reviewed and registered at in-principle acceptance before any data are collected. Samsung Electronics had no role in the design, conduct, analysis or reporting of this work.

### Funding

Self-funded.

### Ethics

Not applicable; no human subjects. No purchase is made and no seller, retailer or brand is contacted.

## Use of AI tools {-}

During the preparation of this work the author used AI tools (Anthropic's Claude) to assist with study design, analysis and writing. The author reviewed and edited all content and takes full responsibility for it.

### Data availability

Section 9.2. OSF project ec6wh (https://osf.io/ec6wh).

---

## References

Allouah, Besbes, Figueroa, Kanoria and Kumar. 2025. "What Is Your AI Agent Buying? Evaluation, Biases, Model Dependence, & Emerging Implications for Agentic E-Commerce." arXiv:2508.02630 (v1 2025-08-04; v3 2025-12-17). https://arxiv.org/abs/2508.02630

Cherep, Ma, Xu, Shaked, Maes and Singh. 2025. "A Framework for Studying AI Agent Behavior: Evidence from Consumer Choice Experiments." arXiv:2509.25609 (v1 2025-09-30; v2 2026-02-24). https://arxiv.org/abs/2509.25609

González Castro, P. U. 2026. *Tri-System Brand Growth: The AI Mediation Layer. Five Propositions, an Experiment, and a Measurement Framework for Brand Growth in AI-Mediated Choice.* Marketing Science Institute Working Paper, Report No. 26-132 (posted 2026-10-15).

González Castro, P. U. 2026g. "The AIAS Presence Measurement Protocol: Substrate Pre-Screening, Independent Moderator Pathway, and Phantom Brand Persistence Phase B Extension (v1.6)." SSRN Working Paper 6816340. https://ssrn.com/abstract=6816340

González Castro, P. U. 2026h. "AI Availability as a Third Measurable Layer of Brand Availability: Five-Substrate Empirical Anchoring of the AIAS Presence Measurement Protocol (AIAS 1.0)." SSRN Working Paper 6817841. https://ssrn.com/abstract=6817841

González Castro, P. U. 2026. "CPC Longitudinal t₁→t₂ Stability (v0.34)." SSRN 6915458.

González Castro, P. U. 2026. "CPC Consistency Instrument Redesign (v1.8)." SSRN 6963359.

González Castro, P. U. 2026. Ranking closing paper (v1.14 + v1.16). OSF project ec6wh and thirdsystem.ai.

González Castro, P. U. 2026. t₄ wave (v0.42): pre-registration, data and scoring, tag `v0.42-scoring-locked`. OSF project ec6wh.

Peer Community In Registered Reports. Full policies. https://rr.peercommunityin.org/about/full_policies (opened 2026-11-11).

Perez, Sarah. 2026. TechCrunch, 2026-11-04. https://techcrunch.com/2026/11/04/almost-no-one-uses-ai-agents-to-book-their-uber-company-says/ (opened 2026-11-11).

Romaniuk, J., and B. Sharp. 2016. *How Brands Grow Part 2: Including Emerging Markets, Services and Durables, New Brands and Luxury Brands.* Melbourne: Oxford University Press.

Sharp, B. 2010. *How Brands Grow: What Marketers Don't Know.* Melbourne: Oxford University Press.

> **[DRAFT NOTE]** References are limited to sources present in the repository or project docs. Three programme references (v0.34, v1.8, the Ranking closing paper) are given in short form; their full titles are to be copied from the papers before submission. Author first names (Allouah et al.; Cherep et al.) and the TechCrunch headline are not in the sources read (r1 gives surnames and the URL only); add them from the arXiv and TechCrunch pages before submission.

---

## Appendix A. Relation to pre-registration r1 of v0.46 (for the record; kept in the submission)

This protocol was first drafted as a direct pre-registration (v0.46 r0, 2026-11-11; r1, 2026-11-14; never locked). On 2026-11-17 the author chose the PCI RR route (standard track, Peer Community Journal) and decided that Presence and Ranking are re-measured inside the study to keep bias-control Level 6. IPA's registration takes the place of the programme's usual lock. Changes from r1:

1. **Predictors re-measured** in the same post-IPA collection (blocks P1–P4; Section 3.4) instead of read from t₄ (v0.42) and v1.14 Stage 1. t₄ values move to code-parity gates, power-simulation inputs and two declared exploratory analyses (Sections 3.4, 4.2, 5.9).
2. **Model selection by rule at collection** (Section 3.3) instead of named models; r1's verification of 2026-11-14 kept as orientation. Contingencies added (provider unavailable → Stage 1 amendment; cost above US$100 → design E first).
3. **Cost** recomputed with the predictor blocks and the judge reserve: US$44.14 central, US$86.38 high (r1: US$26.53 / US$58.11 for the choice blocks alone). Block order, cumulative costs and the projection rule updated (Section 3.9).
4. **Power analysis** recast as an a priori analysis on the smallest effects of interest, with re-measurement noise, for H1–H5 (Section 4); r0's precision table kept in substance.
5. **Sensitivities:** S-Search (search-on Presence at t₄) and S-t5 (t₅ Presence) removed: the confirmatory predictors are measured in the collection, search off (D4). S-Panel added.
6. **Checks:** MC_Probes, MC_Predictor (new; approved 2026-11-22) and MC_Judge added; MC_Complete counts all 1,266 calls.
7. **Descriptive 3** (model agreement) defined on modal choices per (category, brief), because each model has its own Latin squares and no order is shared across models.
8. **Ranking status** updated: v1.16 (2026-11-12) closed Ranking as part of Presence; H3–H4 unchanged and read as tests of the MODE statistic.
9. **Choice coding made explicit** as the Stage 1 code does it (Sections 5.1, 5.3, 5.4, 5.7): in LIST anything off the list, a written refusal included, is OFF_LIST; in OPEN a written refusal is OTHER; provider-flagged refusals are NONE; *codable* in the drop rule counts every answer coded to a choice outcome.
10. **Unchanged:** research questions, hypotheses, verdict rules and thresholds, seeds, briefs and prompt wording, the choice design (762 calls; 182 LIST and 72 OPEN per model), the certified brand matchers, the length-limit stop rule, the US$100 cap with the US$80 pause, the conflict-of-interest declaration and the AI-use statement.

**Decisions of 2026-11-14 (D1–D8), as applied here.** D1 phase number v0.46 (folder `osf/v46/`). D2 Google chooser: the rule of Section 3.3, which on 2026-11-14 gave Gemini 4 Argon. D3 prompt "I'll buy whatever you pick" (Section 3.5). D4 no search-on arm (Section 3.12). D5 route: PCI RR, settled 2026-11-17. D6 industry breadth: a follow-up on v0.44's eight industries with its own budget (Section 3.2). D7 Fisker: a dated, sourced AI check before the 2027-01-08 revision (pending); treated like Cell D if it sells no new cars in the US (Section 3.2). D8 headphones excluded (Section 3.2; Declarations).

---

## Appendix B. [DRAFT NOTE — FOR PABLO; REMOVED BEFORE SUBMISSION] Decisions on r1's open questions

r1 (2026-11-21) listed fourteen open questions, each with one recommended answer. Item 1 was settled before r2, on 2026-11-21. Pablo answered items 2–14 on Sunday 2026-11-22 at 8:17 am with "ok to all", which takes every recommended answer. r2 applies them as follows.

| # | Question | Decision (who, when) | Where in r2 |
|---|---|---|---|
| 1 | Tools arm (search on) | Kept out of #76; D4 (no search-on arm) stands; the tools arm is a separate future study (Pablo, 2026-11-21, about 11:35 am, "Ok to all" on the recommended answers of the tools-arm draft, project doc claude/named-to-chosen-tools-arm-v1.md) | Section 3.12 |
| 2 | Design A (two Latin squares) or E (one) | A, two Latin squares (Pablo, 2026-11-22, 8:17 am) | Sections 3.6, 4.4 |
| 3 | Fisker (D7) | A dated, sourced AI check before the 2027-01-08 revision, logged as a record with method `ai_check_dated_source`; a missing record counts as pending and blocks acquisition; if Fisker moves to Cell D, the expected call count (1,266) is redone for the 756-choice design (1,260 calls) before the lock (Pablo, 2026-11-22, 8:17 am). Check not yet made | Sections 3.1, 3.2 |
| 4 | Search-on Presence sensitivity (S-Search) | Dropped (Pablo, 2026-11-22, 8:17 am) | Section 5.8; Appendix A, item 5 |
| 5 | MC_Predictor, the predictor-side positive control | Added; it can flag a category and never changes a verdict (Pablo, 2026-11-22, 8:17 am) | Section 5.6 |
| 6 | Ethics | An in-text "no approval needed" statement, no institutional letter (Pablo, 2026-11-22, 8:17 am) | Section 9.1 |
| 7 | The five Cheil/Iris-tied units | Kept, with the S-COI sensitivity (Pablo, 2026-11-22, 8:17 am) | Section 5.8; Declarations |
| 8 | The v0.23 recognition judge | v0.45's J1 parity-check winner; J1 re-run if it is retired; premium spirits left out if no candidate passes; no hand coding (Pablo, 2026-11-22, 8:17 am) | Section 3.4 |
| 9 | Ranking statistic | v1.14's MODE kept (Pablo, 2026-11-22, 8:17 am) | Sections 1.3, 3.4 |
| 10 | Verdict rules | The rules fixed on 2026-11-11 kept unchanged (Pablo, 2026-11-22, 8:17 am) | Section 2 |
| 11 | H4 | Kept as a secondary test, its low power stated (Pablo, 2026-11-22, 8:17 am) | Sections 2, 4.3, 6 |
| 12 | Re-measure cost | Paid from #76's US$100 cap (Pablo, 2026-11-22, 8:17 am) | Section 3.9 |
| 13 | Bias-control level | Request Level 6 and state the facts (Pablo, 2026-11-22, 8:17 am) | Section 8 |
| 14 | P1 quotation | Checked against the posted MSI working paper by an AI check before submission (Pablo, 2026-11-22, 8:17 am). Planned, not yet run | Section 1.2 |

**Text brought into line with the Stage 1 code (code r1–r3; no decision of Pablo's needed).** (a) In LIST, a brand that is not on the list shown codes OFF_LIST, not OTHER; Sections 5.1 and 5.3 now say the same. (b) *Codable* in the 70% model-drop rule counts every answer coded to a choice outcome (VALID, OTHER, OFF_LIST, DEFUNCT), not only valid choices (Section 5.4). (c) The code-r3 defaults: in LIST, a written refusal matching the coder's fixed explicit-refusal pattern codes OFF_LIST; refusals flagged by the provider stay NONE; descriptive 6 counts declines only among answers coded NONE; in OPEN, written refusals stay OTHER (Sections 5.1, 5.3, 5.7). Also stated as the code does them: the designed call counts without premium spirits (Section 5.4), the five-rated-unit floor for H4 as for H3 (Section 5.2), the minimum-valid-choice rule not applied in sensitivities (Section 5.8), and the tie rule for modal choices (Section 5.7).

**Numbers.** No number of r1 changed: the design is r1's design A, Fisker is still live, and the cost (central US$44.14, high US$86.38) and power figures are those the unchanged scripts give (acquisition dry run and `power_analysis_v0_46_stage1_r1.txt`). The Fisker-in-Cell-D counts (756 choice calls, 1,260 in all) are from the probe builder's check mode.

**Still open before the lock (each needs a model call, so none was made in r2).** The D7 check (item 3) and the P1 quotation check (item 14).
