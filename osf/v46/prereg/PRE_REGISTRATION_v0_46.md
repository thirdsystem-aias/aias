# AIAS™ Presence Measurement Protocol — Pre-Registration v0.46 (proposed number), study #76 "From named to chosen"

**r1 — NOT LOCKED; THE LOCK IS HELD.** The lock waits for the pre-registrant's answer at the venue-plan review on Monday 2026-11-16: lock this pre-registration directly, or take the study through a PCI Registered Report first (§10, D5). Until he answers, the 24-hour lock rule does not run, and nothing is tagged, pushed or deposited. r1 was written 2026-11-14, about 6:30–8:00 pm US Central, by the programme runner, applying the pre-registrant's decisions of 2026-11-14, 8:54 am ("#76 GO") to draft r0 (written 2026-11-11 from his brief of that evening); every change is in the change log (§11). No model has been called for this study, and no probe file exists yet.

Pablo Ulpiano González Castro
School of Visual Arts, MPS Branding Program, New York, NY (primary academic affiliation)
Third System™ (research entity; data archive and methodology venue)
Correspondence: pablou@pablou.com · pablou.com
ORCID: 0009-0003-8968-9990 (linked: https://orcid.org/0009-0003-8968-9990)

**Study:** From named to chosen. When a buyer asks an AI model to make the final choice for them, does the brand the model chooses follow the brand's AI Presence (and its Ranking score) in the same category?
**Design:** Four categories already measured on the newest models in the t₄ wave (v0.42, collected 2026-11-11): skincare (v0.20 registry), cosmetics (v0.21), cars (v0.22) and premium spirits (v0.23); 91 brands on sale. Three neutral buyer briefs per category (no preference, value for money, best quality), fixed below. Two conditions: **OPEN** (the model names any brand) and **LIST** (the model chooses from the category's registry brands, shown in an order randomised by Latin squares so that every brand appears in every position equally often). The newest generally available flagship of each provider (Claude Fable 5.2, GPT-6 Astra, Gemini 4 Argon; §4.3: Gemini 4 Carbon is not shown as generally available in the Gemini API on Google's own pages on 2026-11-14), search off: per model 182 LIST calls and 72 OPEN calls; **762 calls** in all.
**What it measures:** a model's **stated** choice for a hypothetical buyer. Nothing is bought; no agent, browser, checkout or payment tool is used; no retailer, seller or brand is contacted. It does not measure purchases, sales or market share.
**Budget:** at most US$100 of paid model calls, hard cap; pause at $80; both computed from the recorded usage of every billed request (programme rule, 2026-11-10). **Estimate $26.53 expected (central), $58.11 high** (floor $2.92), from t₄'s recorded token usage at December prices (§4.5; r0's estimate with Gemini 4 Carbon was $33.24 / $78.26).
**Predictors (already measured, frozen):** Presence P_S0 on t₄ (the definition v1.12, v1.13 and v1.14 share on v0.42's analysis set), read from git at `v0.42-scoring-locked` (31c64c6); Ranking R\* (v1.14's modal position, MODE) from v1.14 Stage 1 on t₄ (commit 3129674). **Ranking's own validity is unsettled:** v1.14 Stage 1 came out MARGINAL on 2026-11-11 (separable from Consistency, ρ_w = 0.132, n = 70; not clearly from Presence, ρ_w = 0.369, n = 71, against a 0.30 bar). Ranking therefore enters this study as a predictor whose construct status is open, and every Ranking result here is read as a result about the MODE statistic, not about a validated component (§2.4–§2.5).
**Status:** exploratory study with pre-registered tests. Whether choice becomes a component of AIAS is decided on its results, with the pre-registrant (§7); no result of this study changes any locked score.
**Phase id:** v0.46 (D1, default applied 2026-11-14; §11). **Branch:** `named-to-chosen` (local), from v0.45's head 96c887c (§11). **Lock target (if the direct route is chosen):** tag `v0.46-prereg-rN`, N being the revision that locks (r1 does not lock; §11), pushed, with this file, the probe file, the cost estimate, the scripts and the lock manifest deposited at OSF `ec6wh` → `v46/prereg/` and `v46/anchor/` before the first call.
**Collection window:** after the lock (under the Registered Report route, after in-principle acceptance instead, §10), all calls within 72 hours, and **not before 2026-11-21**, after v0.40's collection window (2026-11-17 to 11-21) has closed. The collection runs **alone on the collection Mac**: no other paid collection runs during any part of v0.46's 72 hours (scheduled: v0.44 2026-11-24 to 11-28; v0.45 t₅ about 2026-12-03). The window is the first free slot after the lock that holds all 72 hours, and is recorded in the budget state file before the first call.

---

## §0 Plain summary for Pablo

AI assistants are starting to be asked not only "what are the good brands?" but "just pick one for me." This study asks the newest model from each of Anthropic, OpenAI and Google to make that final pick for an ordinary buyer, in four categories we measured on the same models this week (skincare, makeup, cars, premium spirits). Each model is asked two ways: with no list (it names any brand) and with a list of the category's brands in a shuffled order (balanced so every brand appears first, last and everywhere in between equally often, because published experiments show shopping agents favour items by their position on the page). We then test whether the brands a model picks are the brands with high AI Presence, and whether the Ranking score adds anything on top. It is the missing middle step between what AI says about brands (Presence) and what people search for and buy (v0.43's search interest; Amazon sales rank in March, if Keepa is approved): named → chosen → bought. Google's newest generally available model is still Gemini 4 Argon (Gemini 4 Carbon is not listed as generally available in Google's Gemini API pages on 2026-11-14), so the three choosers are the same three models that produced the Presence scores. It costs about $27 (at most about $58 even if every answer runs long) under the $100 cap, uses no shopping agent and buys nothing: it records what a model says it would choose, not sales. It starts as an exploratory study; whether "chosen" ever becomes part of the AIAS score is your call once the results are in. Your decisions of 2026-11-14 are applied and marked in §11; the lock waits for your choice of route on Monday.

---

## §1 Context and question

**The chain.** The programme measures what AI models say about brands: Presence (whether and how often a model names a brand, v1.6; SSRN 6816340), Consistency (v1.8; SSRN 6963359) and, provisionally, Ranking (v1.14). Separately it tracks demand: v0.43 tests whether Presence leads Google search interest, and Amazon sales rank is planned for March 2027 from a licensed source only (Keepa, pending the pre-registrant's go; no scripted Amazon browsing). Between the two sits an untested link: when a buyer hands the decision to a model, does the model choose the brands it names? This study measures that link — **named → chosen** — and leaves **chosen → bought** to the demand studies.

**Why now, and why only a stated choice.** Agentic buying is early. On its third-quarter 2026 earnings call, Uber's CFO Balaji Krishnamurthy said that "only four rides were ordered through an AI agent during its busiest week in October", and "only 500 Uber Eats orders were placed by an AI agent", against "around 320 million trips and orders across Uber and Uber Eats during the week of Halloween" (TechCrunch, Sarah Perez, 2026-11-04, https://techcrunch.com/2026/11/04/almost-no-one-uses-ai-agents-to-book-their-uber-company-says/, opened 2026-11-11). Real agent purchases are therefore too rare to study as an outcome, and this study does not try: it asks models to state a choice, which is the decision an agent would act on. Its result says how a model chooses when asked; it does not say that anyone bought anything, or that sales follow.

**What published work leads us to control.** Two experimental studies of AI shopping agents motivate the design:
- Allouah, Besbes, Figueroa, Kanoria and Kumar, "What Is Your AI Agent Buying? Evaluation, Biases, Model Dependence, & Emerging Implications for Agentic E-Commerce", arXiv:2508.02630 (v1 2025-08-04; v3 2025-12-17; https://arxiv.org/abs/2508.02630, opened 2026-11-11). The abstract reports that agents "exhibit strong position biases", that agents "can exhibit choice homogeneity, often concentrating demand on a few" products, that they "consistently penalize sponsored tags while rewarding platform endorsements", that sensitivity to price, ratings and reviews differs sharply across models, and that "model updates can drastically reshuffle market shares".
- Cherep, Ma, Xu, Shaked, Maes and Singh, "A Framework for Studying AI Agent Behavior: Evidence from Consumer Choice Experiments", arXiv:2509.25609 (v1 2025-09-30; v2 2026-02-24; https://arxiv.org/abs/2509.25609, opened 2026-11-11). The authors "vary prices, ratings, and psychological nudges", find that "agent decisions shift predictably and substantially in response", and conclude that "agents are strongly biased choosers even without being subject to the cognitive constraints that shape human biases". (Its abstract does not mention position effects; position rests on Allouah et al.)

Consequences for this design: (i) list order is randomised and balanced, and position effects are estimated, not ignored (§2.6, §5.5); (ii) no price, rating, review, sponsorship or endorsement cue appears in any prompt, so the choice can reflect only what the model brings to it — the brief, the brand names, and in LIST the order; (iii) concentration of choices on few brands is expected and the primary statistic is built to stay valid under it (§2.2, §6); (iv) results are reported per model, since model dependence is itself a published finding.

**Questions.**
1. **Presence → choice.** When a model chooses from the full list of a category's brands, does it pick brands with high Presence? (PRIMARY, §2.2.)
2. **Named → chosen without a list.** When it chooses freely, do its choices land on high-Presence registry brands, and how often outside the registry? (SECONDARY, §2.3.)
3. **Ranking → choice.** Does the Ranking score predict choice, and does it add anything beyond Presence? (SECONDARY, §2.4–§2.5.)
4. **Order.** How much does the position of a brand in the list move the choice? (SECONDARY, labels only, §2.6.)

---

## §2 Pre-registered hypotheses

### §2.1 Definitions (used by every test)

- **Categories g and live brands.** The four registries of §3 with the units not on sale removed: skincare 24, cosmetics 24, cars 19 (v0.22's five Cell D "Defunct" units removed: Pontiac, Oldsmobile, Plymouth, Mercury, Saturn), premium spirits 24; **91 live units**. L_g = number of live units in g. A unit is (category, brand): Rare Beauty is a unit of skincare and of cosmetics, scored separately.
- **Calls.** OPEN call = (category, brief, model, run); LIST call = (category, brief, model, order). Every call is independent (no conversation state), search off (S0).
- **Choice.** The brand on the answer's final `CHOICE:` line, coded to the category's registry (§5.1): a live unit (valid choice), OTHER (a brand outside the registry; OPEN only), OFF_LIST (LIST: a brand not on the list), DEFUNCT (a Cell D brand), AMBIGUOUS (two or more registry brands), NONE (no codable choice, a refusal, or no answer).
- **Presence P.** P_S0 of a unit on t₄, as v1.14 §5.2 defines it on v0.42's analysis set: P = 100 · (C_P/3 + 2 · π̂)/3, with π̂ = v0.42's recall Presence on N3 (Claude Fable 5.2, GPT-6 Astra, Gemini 4 Argon) search off (`pi_N3_S0`) and C_P/3 = the share of N3 models whose t₄ recognition code is "recognized". Read from git at `v0.42-scoring-locked` (brand table and coded files); never recomputed from new answers.
- **Ranking R\*.** v1.14's modal position on t₄, search off, rated units only (≥ 6 rankable mentions), as stored by v1.14 Stage 1 (`osf/methodology/v1_14/outputs/stage1/`, commit 3129674, rank table SHA-256 recorded there). Higher = nearer the top of the models' lists: R\* = −(the smallest modal position) (`scripts/score_v1_14.py`, `modal_position`: "Higher = nearer the top"; identical to v1.10's MODE, `float(-vals[cnt == cnt.max()].min())`); the stored t₄ values run from −9 to −1. The scorer asserts this orientation before use and halts otherwise. In the four categories 60 units are rated (skincare 13, cosmetics 15, cars 14, spirits 18).
- **Within-category percentile.** For a predictor X and a unit b of g: u_X(b) = (rank of X_b among the live units of g − 0.5) / L_g, average ranks for ties; u ∈ (0, 1). For R\*, ranks are among the rated live units of g and L_g is their number.
- **Choice percentile Ū_X.** The mean of u_X(chosen unit) over the valid choices of a condition. Ū_X = 0.5 when choice is unrelated to X; Ū_X = 1 − 0.5/L_g when every choice goes to the top unit. Ū_X equals the choice-weighted probability that the chosen brand outranks a randomly drawn listed brand on X (ties counted half), i.e. a choice-weighted area under the ROC curve.
- **Permutation p.** One-sided unless stated. X permuted among the live units within each category (the same permutation for every choice in that category), Ū_X recomputed exactly as observed; 10,000 draws; p = (1 + #{Ū_perm ≥ Ū_obs}) / 10,001; a draw counts as a hit if Ū_perm ≥ Ū_obs − 10⁻¹². This null keeps the observed concentration of choices (which brands were chosen how often) and breaks only their link to X, so it stays valid when choices pile onto a few brands (§6).
- **Bootstrap interval.** 90% percentile interval from 10,000 resamples of calls within (category, model) strata; reported, never a verdict input.
- **ρ_pw.** v0.42's pooled within-category Spearman with centred ranks (v0.42 §2.1, C25), used for brand-level figures reported alongside.
- **Seeds.** 460001 (H1), 460002 (H2), 460003 (H3), 460004 (H4), 460005 (bootstrap), 460006 (H5), 460010 (Latin squares and their assignment to calls; §4.2).
- **α.** 0.05 per test, no multiplicity correction; verdicts rest on pre-set effect sizes, and every test is reported.

### §2.2 PRIMARY: `H_Presence_Choice_List` — models choose high-Presence brands when shown the full list

**Statement.** When a model chooses one brand for a buyer from the full list of a category's live brands, in a balanced random order, the chosen brand tends to have high Presence in that category.

**Operationalisation.** LIST condition; all valid choices (546 LIST calls by design); X = P.

**Test.** Ū_P; permutation p (seed 460001); bootstrap interval.

**Verdict rule.** UNDETERMINED if a model is dropped from LIST (§5.4) or fewer than 450 valid LIST choices remain · CONFIRMED if Ū_P ≥ 0.70 and p < 0.05 · FALSIFIED if Ū_P < 0.60 · MARGINAL otherwise.

**Rationale.** Ū_P is a choice-weighted AUC: 0.70 means the chosen brand outranks a randomly drawn listed brand on Presence seven times in ten, the conventional floor of "acceptable" discrimination for a predictor; below 0.60 Presence carries little information about the pick. With Presence measured on the same model generation (t₄, about three weeks earlier) and every brand in front of the model, a weaker link than 0.60 would mean the named → chosen step is largely broken. Thresholds are fixed before any choice exists; the Presence values are already published inside the programme.

**Reported alongside.** Per model, per category, per brief; ρ_pw(P, c) with c = a unit's LIST choice share; Ū with π̂ (recall only) in place of P; Ū with P_S1 (search-on Presence); S-COI and S-Pos (§5.6); concentration (share of choices on the top 3 units per category; Herfindahl index; distinct units chosen); agreement across the three models.

### §2.3 SECONDARY: `H_Presence_Choice_Open` — free choices land on high-Presence brands

**Statement.** When a model chooses freely (no list), the registry brands it chooses tend to have high Presence.

**Operationalisation.** OPEN condition (216 calls by design); valid choices = choices coded to a live unit; X = P.

**Test.** Ū_P over valid OPEN choices; permutation p (seed 460002); bootstrap interval.

**Verdict rule.** UNDETERMINED if a model is dropped from OPEN or fewer than 120 valid OPEN choices remain · otherwise as §2.2 (CONFIRMED Ū_P ≥ 0.70 and p < 0.05; FALSIFIED Ū_P < 0.60; MARGINAL otherwise).

**Declared.** This test is partly mechanical: a model cannot freely choose a brand it does not bring to mind, and Presence measures exactly that. A CONFIRMED here is expected and weaker evidence than §2.2; its value is in the realistic setting and in the descriptives: the share of OPEN choices that fall **outside** the registry (OTHER), which brands those are, and whether the model's OPEN choice for a brief is also its LIST choice for the same brief.

### §2.4 SECONDARY: `H_Ranking_Choice_List` — the Ranking score predicts choice

**Statement.** In LIST, the chosen brand tends to have a high Ranking score (a brand the models place early in their lists).

**Operationalisation.** LIST; valid choices whose chosen unit is rated (R\* defined); X = R\*, percentiles among rated live units; categories with ≥ 5 rated units (all four qualify).

**Test.** Ū_R; permutation p (seed 460003); bootstrap interval.

**Verdict rule.** UNDETERMINED if fewer than 200 valid LIST choices fall on rated units or a model is dropped · otherwise as §2.2.

**Declared.** Choices of unrated brands (brands the models rarely name) are excluded from this test, so it is conditional on being named often enough to be ranked. Because R\* and P correlate (ρ_w = 0.369 at t₄), a CONFIRMED here can be Presence in another form; §2.5 is the test that separates them.

### §2.5 SECONDARY: `H_Ranking_Beyond_Presence` — Ranking adds to Presence

**Statement.** Among rated brands, Ranking predicts which brand is chosen beyond what Presence predicts.

**Operationalisation.** LIST calls whose valid choice is a rated unit; choice set = the rated live units of that list (unrated options dropped; the conditional-logit independence assumption is declared). Conditional logit: utility of option b in call i = β_P · z(u_P(b)) + β_R · z(u_R(b)) + γ₁ · [b shown first] + γ_L · [b shown last] + γ_d · (position − 1)/(L_g − 1), with z = standardised within category over rated live units.

**Test.** β_R; one-sided Freedman–Lane permutation p (seed 460004): within each category, u_R regressed on u_P over rated units (OLS), residuals permuted among those units and added back to the fitted values, model refitted; 2,000 draws. Effect size OR_R = exp(β_R), the odds multiplier per standard deviation of Ranking at fixed Presence.

**Verdict rule.** UNDETERMINED as §2.4 · CONFIRMED (Ranking adds) if OR_R ≥ 1.25 and p < 0.05 · FALSIFIED (adds nothing) if OR_R < 1.05 · MARGINAL otherwise.

**Reading.** CONFIRMED would be the first behavioural evidence that the MODE statistic carries information Presence does not; it would not settle v1.14's gate, which is about separability and retest reliability (t₅). FALSIFIED would say that, for choice, the MODE statistic adds nothing to Presence, which is consistent with v1.14's MARGINAL separability. Either result goes to the Ranking decision with the pre-registrant; neither is a Ranking verdict.

### §2.6 SECONDARY (labels, no confirm or falsify): `H_Position_List` — what list order does

**Statement (two-sided question).** The position at which a brand is shown changes how often it is chosen.

**Statistic.** d̄ = the mean normalised position, (position − 1)/(L_g − 1), of the chosen unit over valid LIST choices (0 = first, 1 = last; 0.5 expected without an order effect, because the design shows every unit in every position equally often per model and category). Randomisation test (seed 460006, 10,000 draws): within each (category, model, brief), the orders actually used are reassigned at random to that stratum's calls, the chosen unit of each call held fixed and its position read from the reassigned order; two-sided p. Also: primacy ratio PR₁ = share of valid choices at position 1 × mean L_g, and the shares by position tercile, with bootstrap intervals; position terms γ₁, γ_L, γ_d of §2.5's model fitted on all valid LIST choices with P only.

**Reading (pre-declared labels).** Order-sensitive if p < 0.05 · order-robust if p ≥ 0.05 and the bootstrap interval of d̄ lies within [0.45, 0.55] · inconclusive otherwise. Reported per model, since Allouah et al. report that position bias varies across providers and model versions.

### §2.7 Manipulation and outcome-neutral checks

- **MC_Design (before any call).** The probe file shows every live unit at every position exactly once per Latin square, per (category, model); the builder's test asserts it.
- **MC_Complete.** At least 98% of the 762 calls end with non-empty answer text after the retry policy. A model × condition below 90% of its calls (LIST 182, OPEN 72) is dropped from that condition's tests (§5.4).
- **MC_Codable.** Share of answered calls with a valid choice, per model × condition; below 85% is flagged; below 70% drops the model from that condition's tests (a model that will not choose cannot test the hypotheses).
- **MC_OnList.** Share of LIST choices that are OFF_LIST; above 5% is flagged.
- **MC_Defunct (positive control).** Share of OPEN choices coded DEFUNCT (a car brand that is no longer sold, Cell D). Expected near 0; above 2% flags the coding or the briefs, and the study reports it before any test.
- **MC_Served.** Every served model ID equals the requested ID (a dated snapshot of it is accepted); otherwise excluded, re-run and logged.
- **MC_Truncation.** Share of calls ending at the output cap, per model × condition; above 5% flagged. An answer cut before the choice also triggers the stop rule of §4.6.
- **MC_Window.** All calls within 72 hours.
- **MC_Budget.** Spend from recorded usage stays at or below $100; every pause, approval and stop logged (`osf/v46/data/v46_budget_state.json`), with the calls not sent.

### §2.8 Pre-registered descriptives (no verdicts)

1. Choice shares per unit, condition, brief and model; the five most chosen brands per category and model.
2. OPEN: share OTHER, and the OTHER brands named (top 10 per category); share of OPEN choices that equal the same model's modal LIST choice for the same brief.
3. Model agreement: share of (category, brief, order) cells in which all three models choose the same unit.
4. Brief effects: Ū_P per brief (no preference, value, quality).
5. Own-model link: for each chooser (Claude Fable 5.2, GPT-6 Astra and Gemini 4 Argon, the three models that also produced t₄'s Presence), Ū with the model's own t₄ recall π̂_m.
6. Refusals and hedges: share of answers that decline to choose, or choose while stating that the model cannot buy.
7. Answer form and cost: words per answer, output and thinking tokens, spend per model × condition.

---

## §3 Categories and registries

### §3.1 Choice of categories

Requirement: categories already measured on the newest models, so that Presence and Ranking exist for every brand before any choice is asked. On 2026-11-11 only the t₄ wave meets it: the five omnibus registries (v0.19–v0.23, 112 units) on N3, collected and scored once (`v0.42-scoring-locked`). v0.44's eight new industries (159 units) are locked but collect only on 2026-11-24 to 11-28, so they have no Presence yet (option G of §4.5 and decision D6 of §11).

Of the five omnibus categories four are used:

| Category (registry) | Units | Live units in LIST | Brief noun | COI handling carried forward (Entry 0) |
|---|---|---|---|---|
| Skincare (v0.20) | 24 | 24 | "a skincare product for my daily routine" | none of record at v0.20; Eucerin: Iris/Cheil search work (v0.62 Part F) |
| Cosmetics (v0.21) | 24 | 24 | "a makeup product" | none of record |
| Cars (v0.22) | 24 | 19 | "a new car" | tier-2/3 component supply (§9, COI); Chevrolet, BMW, Bentley: Cheil/Iris agency work (v0.62 Part F) |
| Premium spirits (v0.23) | 24 | 24 | "a bottle of premium spirits" | Jack Daniel's: Iris agency work (v0.62 Part F) |

**Headphones (v0.19) are excluded** on the programme's conflict-of-interest rule (categories in which the author's employer's group competes stay out; the facts are in §9, COI). Harman International owns AKG and JBL and, since completing its purchase of Masimo's Sound United in September 2025, Bowers & Wilkins, Denon, Marantz and Polk Audio, among others. The v0.19 registry includes Denon, and an OPEN choice could name any Harman brand. A study whose outcome is which brand an AI picks for a buyer must not have such a brand among the possible winners. The exclusion also removes the smallest registry (16 units).

**Industry breadth.** The four categories are three industries the programme has measured many times (beauty, cars, spirits); breadth is the main weakness of a study confined to categories already measured on the newest models. The remedy is option G (§4.5): repeat the design on v0.44's eight service and retail industries after v0.44 is scored, which is also where buyers already hand choices to agents (food orders, hotels). It does not fit in this study's $100 at the high estimate; it is decision D6.

### §3.2 Units not on sale

The five units v0.22 itself classes as Cell D "Defunct" (Pontiac, Oldsmobile, Plymouth, Mercury, Saturn; `osf/v22/v22_verdicts.json`, phase_a per_cell D) are not shown in LIST and are not analysis units: a buyer cannot buy a new car of a brand that is no longer made, and keeping them would inflate the Presence–choice link mechanically (they have π̂ = 0 at t₄ and would never be chosen). They stay in the coder so that an OPEN choice of them is caught (MC_Defunct). Fisker stays as v0.22 classed it; its market status is to be checked before the lock and, if it sells no new cars in the US, it is treated like Cell D by a logged clarification before any call (decision D7).

### §3.3 Registry files and coding functions

Unchanged, read from git: the v0.20–v0.22 content modules' `detect_mention` and the v0.23 brand patterns (`score_v0_23`), exactly as v0.42's coder calls them (`osf/v42/scripts/code_t4_v0_42.py`, git blob 2d36735d), and the v0.23 inline registry pinned by v1.10 (`osf/methodology/v1_10/registries/v0_23_registry_v1_10.json`). LIST shows each brand by the registry's canonical name.

---

## §4 Probes and collection

### §4.1 Buyer briefs (fixed; the probe file will reproduce them byte for byte)

Each prompt is a single user message, no system prompt. `{item}` is the brief noun of §3.1; `{need}` is one of the three briefs; `{options}` is the LIST block.

Needs (one per brief):
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

Wording choices (declared): (i) The pre-registrant's brief reads "pick one and buy it for me". Because no model in this study can buy anything, the prompt says "I'll buy whatever you pick": the decision is handed over, the purchase stays with the buyer, and no model is asked to do something it cannot (which would invite refusals and hedges unrelated to brand choice). The literal phrase is decision D3. (ii) No price, rating, review, sponsorship, retailer or product detail appears (§1). (iii) Options are plain bullet lines, not numbers, so the position is visible as order only, as in a product listing. (iv) The final-line format makes the outcome machine-codable; the one-to-two-sentence explanation is kept for the descriptives and keeps the answer short.

### §4.2 Design

| Block (collection order) | Condition | Content per model | Calls per model | Calls (3 models) |
|---|---|---|---|---|
| 1 | LIST | Latin square 1 in each category: L_g orders, spread over the 3 briefs | 91 | 273 |
| 2 | OPEN | 4 categories × 3 briefs × 6 runs | 72 | 216 |
| 3 | LIST | Latin square 2 in each category | 91 | 273 |
| **Total** | | | **254** | **762** |

**Orders.** For each (category, model) two independent cyclic Latin squares of side L_g are drawn (seed 460010): the units are mapped to symbols at random, rows are cyclic shifts, and the rows are shuffled. Each row is one LIST order; across one square every live unit appears exactly once at every position (MC_Design). Rows are assigned to briefs in rotation after a random shuffle (L_g = 24: 8 rows per brief per square; L_g = 19: 7, 6, 6, rotating which brief gets 7 across categories and squares). Each model gets its own squares, so no order is shared across models by construction. **OPEN runs** are six independent calls of the identical prompt per (category, brief, model); run-to-run variation comes from each provider's default sampling.

**Why these numbers.** The precision of the primary test is limited by the number of brands and categories, not by the number of calls, once choices concentrate on a few brands (§6): one square per model already gives H1 its full precision. The second square is for the position analysis (every unit seen twice at every position per model) and for per-model results; six OPEN runs per brief give each model 72 free choices, enough for its OPEN choice shares and the OTHER descriptive. More calls (option F) buy almost nothing for H1 (§6); more categories would (option G).

### §4.3 Panel (newest generally available flagship per provider; verified from each vendor's own pages on 2026-11-11 and again for r1 on 2026-11-14)

Rule (pre-registrant, 2026-11-14): the newest generally available flagship of each provider, as at t₄; restricted, preview, experimental and pre-release models are out; for Google, Gemini 4 Argon unless Gemini 4 Carbon is generally available in the Gemini API.

| Provider | Model (ID) | Verification (r1: opened 2026-11-14, about 6:40–6:55 pm US Central; r0: 2026-11-11) |
|---|---|---|
| Anthropic | Claude Fable 5.2 (`claude-fable-5-2`) | Model page https://platform.claude.com/docs/en/models/fable-5-2/overview (2026-11-14, unchanged since r0): Status "Active (latest)", Released "November 9, 2026", Retirement "Not sooner than November 9, 2027"; default effort `high`. "Claude Mythos 5.2 offers the same capabilities only to organizations verified through Anthropic's verification programs": restricted, excluded. Models overview (https://platform.claude.com/docs/en/about-claude/models/overview, 2026-11-14) lists Claude Fable 5.2 first among "Latest models", then Claude Opus 5.5, Claude Sonnet 5.5 and Claude Haiku 5.5; no newer model is listed (the page gives no release dates). One flagship per provider (budget rule): Fable 5.2, as at t₄. |
| OpenAI | GPT-6 Astra (`gpt-6-astra`) | Model page https://developers.openai.com/docs/models/gpt-6-astra (2026-11-14, unchanged since r0): "Our most capable model for the most demanding work"; the only snapshot listed is `gpt-6-astra`; Responses (`v1/responses`) and Batch (`v1/batch`) endpoints. Pricing page (https://developers.openai.com/api/docs/pricing, 2026-11-14): `gpt-6-astra` first and highest priced under "Flagship models" ($10.00 / $50.00); `gpt-6.1-sol` ($2.00 / $10.00) and `gpt-6.1-terra` ($1.00 / $5.00) are lower-priced tiers that no OpenAI page describes as more capable; no GPT-7. |
| Google | **Gemini 4 Argon (`gemini-4-argon`)** | Gemini API changelog (https://ai.google.dev/gemini-api/docs/changelog, redirects to https://aistudio.google.com/docs/changelog), entry of 2026-10-13: "Gemini 4 Argon (`gemini-4-argon`) generally available (GA)", "our most capable model". Models page (https://ai.google.dev/gemini-api/docs/models, redirects to https://aistudio.google.com/docs/models): Gemini 4 Argon is the only Gemini 4 model listed. Pricing page (https://aistudio.google.com/docs/pricing): Argon listed, paid tier. The model of t₄ (v0.42) and of v0.40's current arm. Gemini 4 Carbon: checked and not used (below). |

**Google: Gemini 4 Carbon checked on 2026-11-14 and not used.** The pre-registrant's rule of 2026-11-14 takes Carbon only if it is generally available in the Gemini API; preview or experimental status does not count. Google's own pages, opened 2026-11-14, about 6:40–6:55 pm US Central:
- Gemini API changelog (https://ai.google.dev/gemini-api/docs/changelog → https://aistudio.google.com/docs/changelog): **no entry mentions Gemini 4 Carbon.** The newest entry is dated 2026-10-26; the only Gemini 4 entry is Argon's of 2026-10-13, "Gemini 4 Argon (`gemini-4-argon`) generally available (GA)". r0's statement that this changelog listed "Gemini 4 Carbon (`gemini-4-carbon`) generally available (GA)" on 2026-11-10 is not borne out by the page and is withdrawn.
- Models page (https://aistudio.google.com/docs/models): Carbon is not listed.
- Pricing page (https://aistudio.google.com/docs/pricing): Carbon is not listed.
- What's new page (https://aistudio.google.com/docs/whats-new-gemini-4-carbon): "Gemini 4 Carbon is available on the paid tier of the Gemini API and in Google AI Studio"; the page does not say generally available, GA, preview or experimental.
- Google blog, 2026-11-10 (https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-carbon-now-available/): "Gemini 4 Carbon is now available"; "available via the API in Google AI Studio and Gemini for business for all paying developers and enterprises"; no GA wording.
- Carbon's model page (https://aistudio.google.com/docs/models/gemini-4-carbon) could not be read (client error, twice).

Reading: Google's Gemini API documentation does not record Carbon as generally available: no changelog GA entry, and it is absent from the models and pricing pages. "Available on the paid tier" is not the GA status the rule requires. The Google chooser is therefore **Gemini 4 Argon**, the model of t₄. (v0.40 §4.3 had already excluded Carbon on 2026-11-12, for another reason: its Google Cloud page read "available to verified enterprise customers in select regions".) Consequences: the predictor and the chooser are the same three models (N3) for every provider; r0's choice "Carbon alone or an Argon arm too" (D2) falls away, and no extra arm is added; descriptive 5 covers all three choosers. This check fixes the panel of r1. A later change in Carbon's status does not change r1; whether to repeat the check before a later lock (for example under the Registered Report route) is the pre-registrant's call (§11).

### §4.4 Conditions, decoding and call policy

As v0.42 r2 §4.4 and v0.45, search off only: no tools; temperature, top-p and effort at provider defaults, none of them sent (Claude Fable 5.2 accepts none of them), as at t₄; maximum output 16,384 tokens (the current-arm cap since v0.38; not lowered for cost, so that a long deliberation is recorded, not truncated). Claude Fable 5.2 through Anthropic's Message Batches API (50% token price; same request parameters); GPT-6 Astra and Gemini 4 Argon synchronously, as at t₄, with v0.42's retry policy (transient errors retried; an empty answer re-sent once; batched transient errors re-sent up to 3 attempts; one logged re-run pass inside the window). The acquisition script is a fork of v0.45's `acquire_v0_45.py` (itself forked from t₄'s locked code with C27–C28), with the v0.46 matrix, the guard of §4.5 and the stop rule of §4.6 (Gemini 4 Argon's price row is already in `budget_v0_45.py`); the raw file keeps t₄'s schema (`osf/v46/data/v46_raw.jsonl`), plus the fields condition (LIST/OPEN), category, brief, square, row and the order shown.

### §4.5 Budget

**Cap.** At most $100 of paid model calls for this paper, including re-sends; pause at $80; both computed from actual recorded usage (programme rule, 2026-11-10). No judge model is needed (choices are coded deterministically, §5.1).

**Prices** (vendors' own pages, opened 2026-11-11 and again for r1 on 2026-11-14, about 6:45–6:55 pm US Central; machine copy: `osf/v45/scripts/budget_v0_45.py`, read there 2026-11-11 08:36–08:38 US Central):

| Model | Standard, US$ per 1M tokens in / out | Batch | Source |
|---|---|---|---|
| Claude Fable 5.2 | 8 / 40 | 4 / 20 (used) | https://platform.claude.com/docs/about-claude/pricing (re-read 2026-11-14) |
| Claude Opus 5.5 (alternative D only) | 4 / 20 | 2 / 10 | same |
| GPT-6 Astra | 10 / 50 (used) | 5 / 25 (not used; option) | https://developers.openai.com/api/docs/pricing (re-read 2026-11-14); model page |
| Gemini 4 Argon | 2 / 10 through 2026-11-30; 4 / 20 from 2026-12-01 (output including thinking; used) | 1 / 5; 2 / 10 from 2026-12-01 (not used; called synchronously as at t₄) | https://aistudio.google.com/docs/pricing (re-read 2026-11-14) |
| Gemini 4 Carbon (r0 only; not used in r1) | 2 / 10 through 2026-11-30; 4 / 20 from 2026-12-01 | not listed | https://aistudio.google.com/docs/whats-new-gemini-4-carbon (Carbon is not on the pricing page, 2026-11-14) |

On 2026-11-14 the prices of the three choosers (Claude Fable 5.2 batch, GPT-6 Astra standard, Gemini 4 Argon standard) were unchanged from the programme's table read on 2026-11-10 (CLAUDE.md, collection budget); Google also lists a batch price for Gemini 4 Argon, which this study does not use. The estimate prices all calls on 2026-12-01 (Gemini at its December price), which is conservative if collection is earlier: if every call falls before 2026-12-01 (Argon at 2 / 10), the adopted design costs $22.91 expected and $52.80 high. No search fee arises (search off).

**Token basis — measured, not assumed.** `osf/v46/scripts/cost_estimate_v0_46.py` reads t₄'s recorded usage from git (`v0.42-scoring-locked:osf/v42/data/t4_raw.jsonl`; 876 answered calls) and re-prices it per call: **central** = the mean cost of t₄'s search-off Phase B answers (a described list of several brands, longer than a one-brand choice with one or two sentences of reason, so conservative for this study), +2% for re-sends; **high** = their 90th percentile, +10%; **floor** = the mean of t₄'s yes/no brand answers (a very short answer). Input tokens are replaced by 600 per LIST prompt and 250 per OPEN prompt (the prompts of §4.1 are about 350 and 120). Output tokens are taken as recorded per t₄ call (search off, Phase B, 90 calls per model; mean / 90th percentile of billed output tokens): Claude Fable 5.2 1,279 / 3,536; GPT-6 Astra 837 / 1,844; Gemini 4 Argon, output plus thinking, 1,296 / 1,803. Gemini 4 Argon, the Google chooser in r1, has its own t₄ records, so r0's Carbon multipliers (× 2 central, × 3 high) no longer apply. r1 script: `osf/v46/scripts/cost_estimate_v0_46_r1.py` (it imports r0's functions unchanged); output `osf/v46/prereg/cost_estimate_v0_46_r1.json` and `.txt`; r0's script and output are kept.

Per call (central / high, US$; LIST prompt, then OPEN prompt): Claude Fable 5.2 (batch) 0.0285 / 0.0804 and 0.0271 / 0.0789; GPT-6 Astra 0.0488 / 0.1080 and 0.0453 / 0.1042; Gemini 4 Argon 0.0289 / 0.0423 and 0.0275 / 0.0408.

**Estimate of the adopted design (762 calls; prices of 2026-12-01):**

| Model | LIST calls | OPEN calls | Expected (central), US$ | High, US$ |
|---|---|---|---|---|
| Claude Fable 5.2 (batch) | 182 | 72 | 7.14 | 20.32 |
| GPT-6 Astra | 182 | 72 | 12.15 | 27.16 |
| Gemini 4 Argon | 182 | 72 | 7.24 | 10.63 |
| **Total** | **546** | **216** | **26.53** | **58.11** |
| Pause (spend from recorded usage) | | | 80.00 | 80.00 |
| Hard stop | | | 100.00 | 100.00 |

Floor $2.92. Cumulative by block (central / high): after block 1 $9.67 / $21.00; after block 2 $16.86 / $37.12; after block 3 $26.53 / $58.12 (block sums rounded separately). The $80 pause is not reached even at the high estimate.

**Design trade-off** (same basis, US$; `cost_estimate_v0_46_r1.txt`):

| Design | Calls | Central | High | What it adds or loses |
|---|---|---|---|---|
| **A adopted (r1)** | **762** | **26.53** | **58.11** | — |
| B r0's design, Gemini 4 Carbon in place of Argon | 762 | 33.24 | 78.26 | not used: Carbon is not generally available in the Gemini API (§4.3) |
| C A + OPEN with web search (S1), 6 runs | 978 | 71.09 | 155.44 | the realistic agent setting; not adopted (pre-registrant, 2026-11-14, D4); does not fit at the high estimate |
| D Claude Opus 5.5 (batch) in place of Fable 5.2 | 762 | 22.95 | 47.95 | breaks the "newest flagship" rule and the same-model link to t₄ |
| E LIST one square + OPEN 6 runs | 489 | 16.86 | 37.11 | same H1 precision (§6); weaker position and per-model results |
| F LIST four squares + OPEN 12 runs | 1,524 | 53.05 | 116.23 | almost no gain for H1 (§6) |
| G A + v0.44's eight industries, after v0.44 is scored | 2,130 | 74.05 | 162.34 | industry breadth and the categories where agents already buy; needs its own budget or a smaller design (D6) |

What the adopted design gives up, in order: search-on choice (C, D4); industry breadth beyond beauty, cars and spirits (G, D6); Batch pricing for GPT-6 Astra and Gemini 4 Argon (each would halve that model's token price; it needs batch paths in the acquisition code that t₄ did not use). What it keeps: the primary test with full precision, both conditions, the balanced position design, three providers, and the same three models as t₄'s Presence.

**Guard (computed from actual usage).** v0.45's `budget_v0_45.Ledger` with v0.46's prices: spend = the cost of every raw line already written (its recorded usage at the prices above); before any request is sent its worst case is reserved (2,000 input tokens, output at the 16,384-token cap; a synchronous request reserves two, since an empty answer is re-sent once; a batch is cut to the requests whose worst cases fit). (i) **Hard stop:** no request is sent if spend + reservations + its worst case would exceed $100. (ii) **Pause at $80:** once spend reaches $80, no new request until the pre-registrant's OK is recorded (`--approve-past-80 "<who, when>"`). (iii) **Projection pause:** after block 1, if spend × 762/273 exceeds $100, collection pauses before block 2 and the pre-registrant decides (`--approve-projection`); the hard stop still applies. At the central and high estimates neither (ii) nor (iii) is reached (projection after block 1: $27.0 central, $58.6 high). If collection stops early, block order guarantees that the primary test has at least one complete Latin square per model.

### §4.6 Length-limit stop rule inside the collection (added in r1)

Programme rule of 2026-11-12 (the pre-registrant, 11:36 pm CT), carried here from v0.40 §4.7 under the learn-across-studies rule: no answer may stop at the output-token limit before it gives the study's outcome. In this study the outcome is the choice.
- **What is checked, and when.** Every answer, as soon as its raw line is written: for GPT-6 Astra and Gemini 4 Argon before that model's next request; for Claude Fable 5.2 when each Message Batch's results are written, so the rule acts from its next batch. *At the limit* means the provider's finish reason is its length stop (Anthropic `max_tokens`; OpenAI `length` or `incomplete:max_output_tokens`; Google `MAX_TOKENS`) or, when no finish reason is recorded, output tokens (Google: plus thinking tokens) reach 16,384. *Cut before the choice* means at the limit with no `CHOICE:` line in the visible answer (§5.1). An empty first answer that stopped at the limit and was re-sent (§4.4) also counts; its finish reason is kept in the raw line.
- **Trigger.** One answer cut before the choice, from any model, in any block or condition.
- **Action.** That model is paused at once: no further request for it in any block or condition; the other models go on. The trigger is written to `osf/v46/data/v46_stoprule.jsonl` and reported to the pre-registrant the same day with the call ID, finish reason and token counts. The pause holds across restarts until the pre-registrant decides; his decision is journaled and is a DEVIATIONS entry.
- **Handling, declared now.** The cut answer, and any other answer cut before the choice, stays in the raw file and is treated as missing in every test and descriptive, never as NONE. If the pre-registrant leaves a model paused, its unsent calls count as unanswered (§5.4), and the drop rules of §2.7 and §5.4 apply. No call setting is changed during the collection (no higher limit, no new thinking setting); answers under a changed setting would form a separate arm, reported apart and never pooled.
- **Evidence before the lock.** The same three models under the same settings (16,384-token cap, provider defaults, search off, Fable 5.2 through Message Batches) passed v0.40's pre-lock check on 2026-11-13: no answer stopped at its limit before naming a brand; the largest thinking was Claude Fable 5.2's, 2,252 of 16,384 tokens search off (v0.40 pre-registration §4.8). No answer of t₄'s 876 or v0.39's 180 current-arm answers stopped at the limit. A v0.46-specific paid pre-lock check is therefore not added in r1 (§11, left open).
- **Implementation.** A fork of v0.40's `stoprule_v0_40.py`, called by the writer of `acquire_v0_46.py` and tested with fake providers (no call sent); written with the other scripts before the lock (§11).

---

## §5 Analysis plan

### §5.1 Coding

- **The choice line.** The last line of the visible answer that begins with `CHOICE:` (case-insensitive, after Markdown emphasis is removed); if none, the answer's last non-empty line. URLs are removed before matching, as in v0.42 §5.1.
- **Brand matching.** The category's certified function (v0.20–v0.22 `detect_mention`; v0.23 `score_v0_23` patterns) applied to the choice line only: exactly one registry unit of the category → that unit (DEFUNCT if a Cell D unit; OFF_LIST if LIST and the unit is not live); two or more → AMBIGUOUS; none → OTHER if the line names something, else NONE. For OTHER, the line's text is kept verbatim for descriptive 2 and no attempt is made to map it to a registry.
- **Refusals.** As v0.42 C6 (Anthropic `refusal`; OpenAI refusal content; Google `SAFETY` or a blocked prompt), coded NONE and counted.
- **Coder.** `osf/v46/scripts/code_v0_46.py`, written and tested on synthetic answers before the lock (r1), including adversarial cases: a choice line naming two brands, a brand in the reason but not on the choice line, "Estée Lauder" vs "Estee Lauder", "Dior" (skincare unit "Dior Beauty"), a choice of a Cell D car, and an answer without a choice line. Its tests fix the expected code of each.
- **Blinding of the coder.** The coder sees answers and registries only; it never reads P or R\*. The scorer joins them after coding.

### §5.2 Computation

All statistics by `osf/v46/scripts/score_v0_46.py`, written and tested on synthetic data before the lock (its SHA-256 in the lock manifest), run once after collection and coding. Inputs pinned by git object: P from `v0.42-scoring-locked` (brand table, coded recognition), R\* from v1.14 Stage 1 at 3129674 (the scorer recomputes R\* from the pinned rank table with v1.14's own function and halts if any unit differs from the stored Stage 1 value).

### §5.3 Parity gates (before any v0.46 statistic)

- **G1.** P recomputed by the scorer from the pinned v0.42 files equals P_S0 as v1.14's own Stage 1 code computes it from the same files, for every unit.
- **G2.** R\* recomputed equals Stage 1's stored R\* for every rated unit; orientation asserted (higher = nearer the top).
- **G3.** MC_Design passes on the probe file.

A failed gate stops scoring; the fix is logged in `osf/v46/DEVIATIONS.md` before scoring resumes.

### §5.4 Exclusions, model drop rule, missing data

- Excluded from every test: calls not answered after the re-run pass; calls served by another model; calls outside the window; choices coded NONE, AMBIGUOUS, OTHER (LIST), OFF_LIST and DEFUNCT. Every exclusion is counted per model × condition × category.
- A model × condition below 90% answered (MC_Complete) or below 70% codable (MC_Codable) is dropped from that condition's tests, which become UNDETERMINED (H1–H5 need the three choosers; a reduced panel is reported as a sensitivity).
- Calls not sent because of a budget stop, or because a model was left paused under the stop rule (§4.6), count as unanswered; answers cut before the choice are missing (§4.6). No imputation. Rates use valid choices as the denominator.

### §5.5 Position and order

Besides H5: every Ū (H1–H3) is also computed with the first and the last position of each list excluded (S-Pos-a), and H1's link is re-estimated in the conditional logit of §2.5 with P and the position terms only (S-Pos-b: the odds ratio of P per standard deviation, controlling position). If H5 reads order-sensitive, the paper reports H1 with S-Pos-a and S-Pos-b beside it in the same table.

### §5.6 Sensitivities (each reported beside the test; a verdict change is listed next to the verdict)

- **S-COI.** All tests without the five Cheil/Iris-tied units (Chevrolet, BMW, Bentley, Jack Daniel's, Eucerin; v0.62 DEVIATIONS Entry 0, Part F), as v0.62 does. Kept as drafted in r0: the programme's handling of these units beyond v0.62 awaits the pre-registrant's call (§11, left open).
- **S-Recall.** π̂_N3_S0 in place of P (recall only; recognition is near saturation at t₄).
- **S-Search.** P_S1 (search-on Presence at t₄) in place of P.
- **S-t5.** If v0.45's t₅ is scored before v0.46's scoring, P from t₅ (closer in time to the choices); otherwise not computed.
- **S-LOCO.** Leave one category out.
- **S-Model.** Each test per chooser.

### §5.7 Reporting

Every test, including failures and undetermined results, per model, category and brief. The paper states in its title or abstract that the outcome is a model's stated choice, not a purchase. Results go to the v0.46 paper and its OSF deposit; the choice table (unit × condition × model shares) is deposited for the demand studies (v0.43; sales rank, March 2027).

---

## §6 Power and precision

**What limits precision.** Published agent experiments report that choices concentrate on few items (Allouah et al.). Under concentration, the effective sample of the primary test is the number of distinct brands chosen per category, not the number of calls. The permutation null of §2.1 is built for that: it holds the observed concentration fixed.

**Simulation (draft r0; `osf/v46/scripts/precision_sim_v0_46.py` reproduces it).** Units and t₄ recall values of the four categories (cars without Cell D); each of three models chooses by a logit on β · z(π̂) plus a brand appeal shared across models (SD 1) and a model-specific appeal (SD 0.5), times a concentration scale; 546 LIST choices (two squares); 200 simulated studies per scenario, 1,000 permutation draws each.

| Scenario | Mean Ū_P | SD | Share of choices on top 3 units | P(p < .05) | P(CONFIRMED) | P(FALSIFIED) |
|---|---|---|---|---|---|---|
| No link, concentrated (scale 2) | 0.495 | 0.065 | 0.70 | 0.05 | 0.00 | 0.94 |
| No link, diffuse (scale 0.7) | 0.496 | 0.027 | 0.36 | 0.04 | 0.00 | 1.00 |
| Weak link (β 0.5, concentrated) | 0.708 | 0.063 | 0.75 | 0.92 | 0.57 | 0.07 |
| Moderate link (β 1, concentrated) | 0.846 | 0.039 | 0.84 | 1.00 | 1.00 | 0.00 |
| Moderate link (β 1, diffuse) | 0.696 | 0.026 | 0.46 | 1.00 | 0.47 | 0.00 |
| Strong link (β 2, concentrated) | 0.932 | 0.018 | 0.95 | 1.00 | 1.00 | 0.00 |

Reading: (i) the test's false-positive rate is at its nominal level under the concentrated null; (ii) a CONFIRMED needs a true Ū near or above 0.70, and a true link at the bar comes out CONFIRMED about half the time and MARGINAL otherwise — the verdict bands are wide on purpose and the paper will say so; (iii) one, two or four Latin squares give the same precision (SD of Ū under the concentrated null 0.068 / 0.060 / 0.068; P(CONFIRMED) under the weak link 0.51 / 0.42 / 0.47, 150 simulated studies each): precision comes from brands and categories, so the design spends calls on balance and per-model results, not on repetitions. PCI RR sets no minimum power; a Registered Report would state these figures as the sampling plan (§10).

**H5.** With 546 LIST choices and mean L_g ≈ 23, about 24 choices are expected at position 1 without an order effect; a doubling (PR₁ = 2) is detectable with a randomisation p well below 0.05.

**H3–H4.** Restricted to the 60 rated units and to choices that land on them; with concentration on high-Presence brands, most choices are expected to land on rated units (rated units are the frequently named ones). Their precision is lower than H1's and they are secondary for that reason.

---

## §7 What the result means, and what it does not

- **It measures** which brand a model says it would choose for a hypothetical US buyer, from a neutral brief, without web search, at one point in time.
- **It does not measure** purchases, sales, market share, agent behaviour on a real store, or what any person would choose. A CONFIRMED H1 says that AI Presence predicts AI choice; whether AI choice predicts demand is the next link (v0.43's search interest; sales rank in March 2027), tested elsewhere.
- **Component decision.** Whether choice becomes an AIAS component is not decided by any verdict here. The results go to the pre-registrant with three readings pre-declared: (a) H1 CONFIRMED and choice adds little beyond Presence → choice is evidence for Presence's validity (a behavioural correlate), not a new component; (b) H1 MARGINAL or FALSIFIED with stable, model-consistent choices → choice carries information Presence lacks and is a candidate component, to be specified in its own Paper A; (c) choices unstable across models, briefs or orders (H5 order-sensitive, low model agreement) → choice is reported as a property of the models, not of brands, and is not proposed as a component.
- **Ranking.** H3–H4 feed the pending Ranking decision (v1.14 MARGINAL) as behavioural evidence on the MODE statistic; they do not change v1.14's gate.

---

## §8 Limitations

1. Stated choice, not behaviour: a model's answer to a prompt, without a store, prices, stock, ratings or a budget; real agents act on far richer pages (Allouah et al.; Cherep et al.).
2. Three categories of industry (beauty, cars, spirits) and one market and language (US English); headphones excluded for COI reasons; v0.44's industries not yet measured.
3. Predictor and outcome come from the same three models (Presence and Ranking from their t₄ answers, choice from their new answers), so a link can partly reflect a model's agreement with itself rather than a property of the brands; descriptive 5 reports the own-model link.
4. Presence was measured about three weeks before the choices (t₄, 2026-11-11); S-t5 narrows the gap if t₅ is scored in time.
5. Search off only: agents that shop usually search; option C costs it out.
6. LIST shows the registry, which mixes price tiers (a drugstore moisturiser beside La Prairie; Kia-class cars beside Bentley); briefs V and Q let the tier matter, brief N leaves it to the model.
7. Ranking's validity is unsettled (v1.14 MARGINAL), and R\* exists only for the 60 rated units.
8. Provider-default sampling: OPEN runs vary only as much as each provider's defaults let them.
9. Claude Fable 5.2 runs through the Message Batches API, the others synchronously (as at t₄).

---

## §9 Declarations

**Conflict of interest.** The author is Director, Corporate Brand Creative and Governance at Samsung Electronics America. This study re-uses brand registries fixed in earlier phases (v0.20–v0.23) and performs no new brand selection; each registry carries its source-phase conflict-of-interest handling forward unchanged, and the screen of this study's registries is recorded ex ante as DEVIATIONS Entry 0 (`osf/v46/DEVIATIONS.md`). The audiophile-headphones category (v0.19) is not used, because the Samsung group sells headphones through Harman International, a Samsung subsidiary since March 2017 (deal agreed November 2016), which owns AKG, JBL and, since September 23, 2025, the Sound United brands, Denon among them (What Hi-Fi, 2025-09-23, https://www.whathifi.com/hi-fi/harman-now-owns-bowers-and-wilkins-marantz-and-denon-as-masimo-deal-completes). Denon, which v0.19 chose in place of AKG, was therefore already a Samsung-group brand. In the automotive registry, Samsung subsidiaries hold tier-2/3 component supply relationships with several registry brands — Harman International (audio systems), Samsung SDI (battery cells), and Samsung Display (infotainment) — characterized in the source phase as non-competitive, with no brand-level overlap, and imposing no operational restriction on registry composition (v0.22 Declarations; screened in v0.22 DEVIATIONS Entry 0, Part B). Samsung's affiliate Cheil Worldwide, or its Iris agency, has done agency work for five registry brands used here (Chevrolet, BMW, Bentley, Jack Daniel's, Eucerin; v0.62 DEVIATIONS Entry 0, Part F); every result is also reported without them (S-COI). Acquisition, coding and scoring are automated against the locked registries, and this pre-registration is locked and deposited before any choice is collected. Samsung Electronics had no role in the design, conduct, analysis or reporting of this work.

**Funding.** Self-funded.

**Ethics.** Not applicable; no human subjects. No purchase is made and no seller, retailer or brand is contacted.

**Use of AI tools.** During the preparation of this work the author used AI tools (Anthropic's Claude) to assist with study design, analysis and writing. The author reviewed and edited all content and takes full responsibility for it.

---

## §10 Registered Report route (PCI RR), for the pre-registrant's decision

Source: PCI Registered Reports policies (https://rr.peercommunityin.org/about/full_policies), practical help (https://rr.peercommunityin.org/PCIRegisteredReports/help/help_practical) and the list of PCI RR-friendly journals (https://rr.peercommunityin.org/about/pci_rr_friendly_journals), all opened 2026-11-11. The author guide itself was not opened (the help page links to it without giving its address).

**What a Stage 1 submission would need.**
1. **A Stage 1 manuscript**, not this file: introduction and research questions, hypotheses, methods "significantly longer and more detailed than in a regular manuscript", the sampling plan, the analysis plan, and the interpretation of each possible outcome (§7 is the seed). No set format; numbered lines recommended; tables and figures in the text.
2. **A study design template (table)**: "a mandatory requirement" for quantitative hypothesis-testing Stage 1 manuscripts (one row per hypothesis: question, hypothesis, sampling plan, analysis, rationale for the test's sensitivity, interpretation given different outcomes, theory that could be shown wrong). §2 maps onto it directly.
3. **Sampling plan.** PCI RR "sets no minimum requirement for statistical power"; it asks for a justified plan (a priori power on the lowest meaningful effect, or Bayes factor or equivalence designs). §6 would need recasting as a formal power or precision analysis (the simulation, with the smallest effect of interest stated as Ū = 0.70). Individual journals may set their own minimum.
4. **Outcome-neutral checks** (criterion 1E): pre-specified checks that the design can answer the question. MC_Design, MC_Defunct (positive control) and MC_Codable serve; a reviewer may ask for a positive control on the predictor side as well.
5. **Bias control level.** The outcome data (choices) do not exist, but the predictors (Presence, Ranking) have been observed: "If a submission mixes data at different levels, the lowest level applies". The study would most likely be **Level 2** ("authors have observed some but not all key variables"), eligible but usually requiring countermeasures such as conservative thresholds or a blinded analyst. This draft's countermeasures: thresholds fixed before any choice exists; a coder that never reads the predictors (§5.1); a scorer tested on synthetic data and run once. PCI RR "will not consider studies where the authors already know the outcomes", which this study does not.
6. **Deposit.** The Stage 1 manuscript must be on a recognised preprint server or repository (OSF qualifies; an embargoed track with a view-only link exists). At in-principle acceptance (IPA), PCI RR registers the approved Stage 1 on OSF on the authors' behalf, publicly or under an embargo of up to four years.
7. **Timing.** Standard first-round Stage 1 review takes about 4–8 weeks; the scheduled-review track (a one-page snapshot on PCI RR's template, reviewers booked for a one-week window at least six weeks ahead) speeds up only the first round. Collection would wait for IPA, so choices would be collected in about January–February 2027, two to three months after t₄'s Presence: S-t5 would become the main predictor, or the predictor would be re-specified as t₆ (target 2027-02-12) — a change the Stage 1 manuscript must state.
8. **Journals.** PCI RR recommends; it does not publish. Of the 35 PCI RR-friendly journals listed, none is a marketing, consumer-research, business or information-systems journal; broad-scope options include Peer Community Journal (all STEM, medicine, social sciences and humanities; listed with Level 1 bias control) and PeerJ (social sciences among its scopes). A marketing journal that accepts Registered Reports outside PCI RR would be a separate route (not checked).
9. **Programme rules that would change.** The 24-hour lock and the direct OSF deposit would be replaced by IPA; the AI-use statement and the COI declaration stay as in §9 (the employer disclosure stays in the COI section only).

**Runner's view (for the decision, not a recommendation of record).** The direct route gives a result in December and keeps the predictors fresh; the RR route gives the study external review before any data, at the cost of two to three months, a re-specified predictor and a Level 2 classification. A middle path is to lock and run this study directly as the exploratory study it is, and to take the confirmatory follow-up (new industries, search on, the component question) through PCI RR.

---

## §11 Phase number, base, lock procedure and change log

**Phase number.** v0.46 (D1, default applied 2026-11-14). The roadmap gives each new phase "the next free number when it is scaffolded" (aias_roadmap_ssot.md, v2.1, "Forward v0.NN sequence"). Checked 2026-11-11 against every branch's `osf/` tree and every tag: v0.41–v0.45, v0.62 and v0.63 are taken; v0.46 is free. The roadmap lists v0.46 provisionally for "RS × prompt-phrasing stability", which is not scaffolded and is on hold under v1.14's MARGINAL gate (no Ranking Paper B until a measure passes). If the pre-registrant prefers to keep v0.46 for the Ranking arc, the next number outside the reserved v0.46–v0.61 range is v0.64 (decision D1). "#76" is the study's number in the pre-registrant's study list; the folder and tag use the phase number.

**Base.** Branch `named-to-chosen` from v0.45's head 96c887c, the newest pre-registration draft on the newest-model line: it carries t₄'s locked acquisition code as forked for t₅ (with v0.42's C27–C28) and the price table re-read on 2026-11-11 (`budget_v0_45.py`), which this study's acquisition and guard fork. t₄'s data and v1.14's Stage 1 are not merged; they are read by git object at `v0.42-scoring-locked` and 3129674, as v1.14 itself reads t₄. If v0.45 changes before its lock, the fork is refreshed by a logged clarification. Not v0.42's 7be316c: that commit predates t₄'s collection and scoring.

**Lock procedure (direct route).** **The lock is held** until the pre-registrant chooses the route at the venue-plan review (Monday 2026-11-16, D5); r1 does not lock on its own and no 24-hour clock runs. r1 changes the text, the panel and the cost estimate only. Still to be written before any lock, in a revision that changes no rule: the probe builder (`build_probes_v0_46.py`, seeded Latin squares, MC_Design test), the acquisition fork with the guard (§4.5) and the stop rule (§4.6), the coder and the scorer with tests on synthetic data, `DEVIATIONS.md` with Entry 0 completed, and the lock manifest. If the direct route is chosen, that revision goes to the pre-registrant and locks 24 hours after he receives it unless he objects, or on his "lock now". Lock: refresh `LOCK_MANIFEST_v0_46.sha256`; commit; tag `v0.46-prereg-rN` (the locking revision); push branch and tag; deposit `osf/v46/prereg/` and `osf/v46/anchor/` at OSF `v46/` and verify their SHA-256 there. Only then `acquire_v0_46.py --collect`, which refuses to run until the tag is on `origin` and the anchor exists.

**Deviations policy.** Before the lock: clarifications that change no hypothesis, threshold, panel, prompt, design or decision rule are logged in this section; any other change restarts the 24 hours. After the lock: every deviation is an entry in `osf/v46/DEVIATIONS.md` (Entry 0 = the ex-ante COI screen), dated, written before the affected data are analysed where possible, with its effect on every test; no deviation turns a verdict that has been computed.

**Decisions (D1–D8).** The pre-registrant decided on 2026-11-14, 8:54 am ("#76 GO"): finish r1 with this section's defaults; Google model Gemini 4 Argon unless Gemini 4 Carbon is generally available in the Gemini API; no search-on arm; total within the $100 cap; other models, the newest generally available flagship per provider. Status of each item:
- D1. Phase number: **v0.46. Default applied** (2026-11-14). The alternative was v0.64.
- D2. Google chooser: **decided 2026-11-14.** Gemini 4 Argon unless Gemini 4 Carbon is generally available in the Gemini API; checked 2026-11-14 (§4.3): Carbon not GA, so **Gemini 4 Argon**. The r0 choice between Carbon alone and Carbon plus an Argon arm falls away; no extra arm.
- D3. Prompt: **"I'll buy whatever you pick". Default applied** (2026-11-14). The alternative was the literal "pick one and buy it for me".
- D4. Search-on choice (option C): **decided 2026-11-14: no search-on arm.**
- D5. Route: **open; the lock is held** until the pre-registrant answers at the venue-plan review, Monday 2026-11-16: direct lock, or PCI RR Stage 1 first (§10).
- D6. Industry breadth: **default applied** (2026-11-14): a follow-up on v0.44's eight industries after v0.44 is scored (option G), with its own $100 budget; not folded into this study.
- D7. Fisker: **default applied** (2026-11-14): its US market status is checked before the lock; if it sells no new cars in the US, it is treated like Cell D by a logged clarification before any call. Not yet checked.
- D8. Headphones: **exclusion kept, default applied** (2026-11-14). The alternative was to keep headphones with Denon and every Harman brand treated as excluded choices.

**Left open for the pre-registrant (besides the route, D5).**
- S-COI and the five Cheil/Iris-tied units: kept exactly as r0 drafted them (§5.6, §9). The programme's handling beyond v0.62 awaits his call.
- Model status re-check: whether to repeat the §4.3 check (Carbon's status included) before a later lock, for example under the Registered Report route.
- Length-limit pre-lock check: r1 relies on v0.40's check of 2026-11-13 for the same three models and settings (§4.6). A v0.46-specific paid check would need his OK.
- Fisker (D7): the check is still to be done before the lock.

**Change log.**
- 2026-11-11, r0. Design, hypotheses, verdict rules, cost estimate (`cost_estimate_v0_46.py` run on t₄'s recorded usage), precision simulation, Registered Report notes. No probe file, no acquisition, coding or scoring code yet; no model called.
- **r1 (Nov 14, 2026).** Runner, applying the pre-registrant's decisions of 2026-11-14, 8:54 am ("#76 GO"). No model called; nothing locked, tagged, pushed or deposited. Changes from r0:
  1. Status line: r1, not locked; the lock is held until the pre-registrant's answer at the venue-plan review on Monday 2026-11-16 (direct lock or PCI Registered Report route).
  2. Google chooser: Gemini 4 Carbon → **Gemini 4 Argon** (`gemini-4-argon`). Carbon was checked on Google's own pages on 2026-11-14 and is not generally available in the Gemini API (§4.3; URLs, date and wording recorded there). r0's claim of a changelog GA entry for Carbon on 2026-11-10 is withdrawn: the changelog has no Carbon entry.
  3. §4.3: rule stated; Claude Fable 5.2 and GPT-6 Astra re-verified as the newest generally available flagships on 2026-11-14, URLs and wording recorded; Google row rewritten for Argon; r0's paragraph on the predictor and chooser differing for Google replaced by the Carbon check.
  4. §4.4: Argon called synchronously, as at t₄; the Carbon price row and Carbon's ignored sampling parameters removed.
  5. §4.5: prices re-read 2026-11-14; price table, token assumptions, per-call costs, adopted-design cost table (expected $26.53, high $58.11, pause $80, stop $100; r0 $33.24 / $78.26), block totals, design trade-off table and block-1 projection ($27.0 / $58.6) recomputed by the new `cost_estimate_v0_46_r1.py` (output `cost_estimate_v0_46_r1.json` / `.txt`); November-price variant added ($22.91 / $52.80). Option B (a Gemini 4 Argon arm) replaced by r0's Carbon design for reference.
  6. New §4.6: the length-limit stop rule (programme rule of 2026-11-12, from v0.40 §4.7), adapted to the choice line; MC_Truncation (§2.7) and §5.4 point to it.
  7. Collection window: not before 2026-11-21 (after v0.40's window), alone on the collection Mac (no other paid collection during its 72 hours), first free slot after the lock; r0's proposed target after v0.45's t₅ (from 2026-12-04) dropped.
  8. Descriptive 5 (own-model link) extended to all three choosers; limitation 3 rewritten (predictor and chooser are now the same three models).
  9. Header, §0 summary, budget and design lines updated to the Argon panel and the r1 cost.
  10. COI: the author's employer is now named only in §9 (Declarations, COI): the §3.1 table and headphones paragraph and §10 item 9 point to §9 instead; §9 now gives the date from which Harman has belonged to the employer's group (March 2017) and states that Denon, chosen for v0.19 in place of AKG, was therefore already a group brand (the Denon/Harman correction approved 2026-11-10), with the What Hi-Fi source moved there. S-COI (Cheil/Iris) unchanged and flagged as awaiting the pre-registrant's call.
  11. §11: each decision D1–D8 marked as decided on 2026-11-14 or as default applied; D5 open (lock held); a list of items left open; lock procedure rewritten (the scripts are still to be written, in a revision that changes no rule); the lock tag is now `v0.46-prereg-rN` for the revision that locks (r0 named `v0.46-prereg-r1`).
  12. Unchanged: hypotheses, verdict rules, thresholds, seeds, briefs and prompts, design (762 calls: per model 182 LIST, 72 OPEN), predictors, coding and analysis plan, the AI-use statement, and the statement that the study measures a model's stated choice, not purchases or sales.
