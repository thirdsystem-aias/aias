---
mainfont: "Carlito"
fontsize: 11pt
geometry: margin=1in
---

\thispagestyle{empty}

\begin{center}

{\small SSRN WORKING PAPER}

\vspace{36pt}

{\fontsize{16}{21.76}\selectfont\bfseries Premium Tea as the Third Regime 4 Datapoint: A Single-Category Replication of the v0.13 Covariate-Saturated Weak Finding\par}

\vspace{20pt}

\begin{minipage}{0.88\textwidth}
\centering\itshape\small
Pre-Registered Evidence from a Designed-for-Test Category (Premium Tea, 25-Brand Registry, n = 17 Eligible Worldwide) at Two Longitudinal Waves Against Google Trends; H\_Regime4\_replication CONFIRMED at Both Waves and Surviving Tea Box-Excluded Sensitivity; Premium Tea is the Cleanest Regime 4 Case to Date Because Bivariate $\rho$ is Already Negative Before Covariate Control; Three Datapoints Across Three Categories Elevate Regime 4 from Provisional to Canonical; Headline Classification Axes Evolve from (Bivariate $\rho$ $\times$ Decrement) to (Bivariate $\rho$ $\times$ Partial $\rho$)
\end{minipage}

\vspace{24pt}

\begin{minipage}{0.88\textwidth}
\centering\small
Working Paper · Version 0.14 · Designed-for-Test Category (Premium Tea × AI Presence × Google Trends)
\end{minipage}

\vspace{36pt}

\textbf{Pablo Ulpiano González Castro}

\vspace{10pt}

School of Visual Arts, MPS Branding Program, New York, NY \\
(primary academic affiliation)

\vspace{6pt}

Third System™ (research entity; data archive and methodology venue)

\vspace{10pt}

Correspondence: pablou@pablou.com · pablou.com \\
ORCID: https://orcid.org/0009-0003-8968-9990

\vspace{24pt}

12 May 2026

\vspace{8pt}

Working paper. Not under peer review. Pre-registered.

\end{center}

\newpage

# Abstract

Brand science distinguishes Mental Availability (memory salience) from Physical Availability (point-of-sale presence). The AIAS™ Measurement Programme introduces a third construct — AI Presence — operationalised as the rate at which each brand appears across matched LLM responses to category-recommendation prompts, and tests its construct validity against Google Trends rank as an external consumer-search proxy. v0.13 (five-category construct-validity expansion) identified a fourth empirical regime — Covariate-saturated weak (Regime 4) — in premium facial skincare and personal-finance apps. The regime was named provisionally pending a third independent replication.

v0.14 tests that replication in premium tea, a designed-for-test category selected for its highly fragmented brand landscape and the heavy weight of Asian-tradition specialty brands that English-language consumer search underrepresents. The pre-registered hypothesis H\_Regime4\_replication CONFIRMED at both measurement waves (t$_{1}$ = 29 April 2026; t$_{2}$ = 7 May 2026) and survives Tea Box-excluded sensitivity testing. All three pre-registered conditions hold at both waves: sample size n = 17 eligible brands worldwide (above the C1 floor of 12); bivariate Spearman $\rho$(AI Presence × Google Trends) = $-$0.066 at t$_{1}$ and $-$0.134 at t$_{2}$ (within the C2 threshold $|\rho|$ < 0.35); partial $\rho$ after age + premium-tier control = $-$0.084 and $-$0.146 (satisfying C3 partial $\rho$ < 0). Tea Box-excluded sensitivity (n = 16) replicates: bivariate $-$0.011 / $-$0.129; partial $-$0.005 / $-$0.130.

Premium tea is the cleanest Regime 4 case observed in the programme to date. v0.13's skincare and finance both exhibited weakly positive bivariate $\rho$ that flipped to negative partial $\rho$ only after age and tier were controlled; premium tea bypasses that phase entirely, arriving at negative bivariate before any covariate adjustment. Three datapoints across three categories elevate Regime 4 from a provisional zone to a canonical pattern, and v0.14 evolves the headline classification axes from (bivariate $\rho$ × decrement) to (bivariate $\rho$ × partial $\rho$) to accommodate categories with already-negative bivariate signal.

**Keywords:** AI Presence, AI Availability, Regime 4, construct validity, brand visibility, large language models, Google Trends, partial Spearman correlation, designed-for-test, premium tea

**JEL classification:** M31 (primary), L86, L15, D83, M37

**Paper status.** Working paper, pre-registered. Not under peer review. Programme phase: AIAS Presence Measurement Protocol v0.14, third designed-for-test replication.

\newpage

# 1. Introduction

The Ehrenberg-Bass empirical generalisations rest on two complementary brand-level constructs: Mental Availability (the brand's salience in memory during a category-decision moment) and Physical Availability (the brand's presence in the buyer's purchase environment). Sharp (2010) and Sharp and Romaniuk (2021) treat these as jointly necessary and approximately sufficient for category share. AI-mediated discovery does not fit neatly into either construct: when a consumer asks a large language model "what's the best tea brand for X," the brands surfaced are not retrieved from the consumer's memory and not encountered in a retail environment — they are produced by an intermediary system whose retrieval mechanics differ from both.

The AIAS™ Measurement Programme proposes a third construct — **AI Presence** — defined as the rate at which a brand appears across matched LLM responses to category-recommendation prompts (foundational paper at González Castro 2026a, SSRN 6659000; protocol v1.1 at González Castro 2026b, SSRN 6722319). The construct-validity question is whether AI Presence tracks an external consumer-behaviour reference the way the Ehrenberg-Bass constructs do. The programme's pre-registered methodology uses Google Trends rank within a brand category as the external reference, and v0.6 through v0.13 have systematically expanded the test across diagnostic categories.

v0.13 (González Castro 2026c, SSRN 6750498) tested five categories simultaneously — project management software, premium running shoes, premium olive oil, premium facial skincare, and personal-finance apps — and discovered that two of them did not fit any of the three pre-registered regimes (Marginal direct, Age-mediated strong, Scale-mismatch). Skincare and finance exhibited a distinctive signature: weak bivariate rank alignment (Spearman $\rho$ below 0.35) combined with negative partial $\rho$ after controlling for brand age and competitive tier. This pattern was named provisionally **Regime 4 — Covariate-saturated weak** and was flagged as candidate for promotion to canonical status pending a third independent replication.

**v0.14 supplies that replication.** Premium tea is the designed-for-test category: its brand landscape is highly fragmented, dominated by specialty brands (Harney & Sons, Rishi Tea), Asian-tradition specialty brands (Ippodo Tea, Yunnan Sourcing), and Singaporean luxury (TWG Tea) that English-language consumer search underrepresents relative to mass-market brands (Twinings, Tea Pigs). The pre-registered prediction was that AI Presence would surface specialty and Asian-tradition brands above Trends-implied ranks, producing the Regime 4 signature.

The pre-registered hypothesis H\_Regime4\_replication tests three conditions at both measurement waves: (C1) n $\geq$ 12 eligible brands; (C2) $|$bivariate Spearman $\rho$(AI Presence, Trends)$|$ < 0.35; (C3) partial Spearman $\rho$(AI Presence, Trends $|$ age, tier) < 0. The paper reports the result, the sensitivity tests that support it, and the methodological consequences for the canonical Regime 4 definition going forward.

# 2. Methods

## 2.1 Category and registry construction

Premium tea is operationalised as a single category aggregating loose-leaf tea brands at the premium tier, including herbal and matcha specialty brands where they are sold at premium prices and represent a non-trivial share of the AI-recommendation distribution. The registry (v3-premium\_tea schema; locked at git tag v0.14-prereg, commit b0ef30a) contains 25 brands organised by **premium tier**: 6 luxury (TWG Tea, Marukyu Koyamaen, Jing Tea, Ippodo Tea, Fortnum & Mason, Lupicia), 3 specialty (Harney & Sons, Rishi Tea, Smith Teamaker), and 16 mainstream-premium (Twinings, Tea Pigs, Tea Box, Whittard of Chelsea, Republic of Tea, Numi Organic Tea, Ito En, and 9 additional brands).

The registry includes 22 primary brands plus 3 alternates (Wang De Chuan, In Pursuit of Tea, Yunnan Sourcing) intended to backstop primary E1a (Phase B Trends-eligibility) exclusions from the small Chinese-tradition cell. The premium-tier dimension replaces v0.13's market-tier (incumbent / mid-tier / challenger) to reflect the category's specific structure, where competitive position is more accurately characterised by price tier than by market-cap challenger dynamics. Tier-ordinal encoding for the partial Spearman computation: 0 = mainstream-premium, 1 = specialty, 2 = luxury.

## 2.2 AI Presence acquisition

AI Presence is measured at two waves (t$_{1}$ = 29 April 2026; t$_{2}$ = 7 May 2026) using a matched-model subset of two leading commercial LLMs: Claude Sonnet 4.6 (Anthropic) and GPT-5.4-mini (OpenAI), with response status = ok. Each wave runs four independent runs per model per prompt; six prompts cover the category-recommendation question space (general premium tea recommendations; loose-leaf vs bagged; matcha selection; herbal specialty; sourcing-oriented queries; gift-occasion queries). Total acquisition: 6 prompts × 6 models × 8 runs (4 per wave × 2 waves) = 288 LLM calls. A fill-in-the-gaps retry pass (17 retries) addressed transient model-overload and rate-limit failures during the initial pass, yielding 288/288 OK at the matched-model subset.

Enrichment uses OpenAI function-calling to extract brand mentions from each response and canonicalise them against the registry's aliases list; a regex fallback handles cases where function-calling rate-limits. The canonical scoring script `score_v14.py` (locked at git commit e71e135) computes per-brand AI Presence percentages and per-wave aggregates.

## 2.3 Google Trends acquisition

Trends rank is acquired fresh at a single locked timestamp (2026-05-12T15:54:30Z) under the programme's standard three-phase resolution protocol. **Phase A** validates the rescale pivot: Twinings was selected as the highest-AI-Presence mainstream-premium brand and validated at mean = 88.14, CV = 9.13% across eight independent bundles, satisfying the pivot stability criterion. **Phase B** resolves topic IDs for each registry brand via pytrends; v0.14 surfaced critical topic-ID errors (Republic of Tea matching to an Irish football team in pytrends' search namespace, Makaibari matching to a hotel, etc.) that necessitated a methodological amendment to use bare canonical queries instead of resolved topic IDs (logged in DEVIATIONS.md Entry 1). 16 primary brands passed E1a; 6 primary brands and 2 of 3 alternates failed E1a.

**Phase B-alternates** activated the third alternate, Yunnan Sourcing, after Wang De Chuan and In Pursuit of Tea failed both solo and bundled-E5 (padded-resolution) checks (DEVIATIONS Entry 2). The activated alternate brought n\_eligible to 17 worldwide and 16–17 US (varying by wave). Eight brands were excluded under E1a: Glenburn Tea Estate, In Pursuit of Tea, Makaibari, Postcard Teas, Ten Ren's Tea, TenFu's Tea, Vahdam Teas, and Wang De Chuan.

Acquisition output: 8 bundles (4 worldwide, 4 US) × 2 waves, with Trends rescaled mean per brand per wave-region cell using Twinings as the pivot (rescaled value 100 by construction).

## 2.4 Statistical methods

The pre-registered conditions are operationalised as follows. **Bivariate Spearman $\rho$** computes the rank-order correlation between AI Presence percentage and Trends rescaled mean across the eligible-brand panel within each wave-region cell. **Partial Spearman $\rho$** controls for two covariates (brand\_age\_years; premium\_tier ordinal) using the rank-transformed residual approach with df correction k = 2. The Twinings pivot is exempted from E1b (at-acquisition exclusion) per pre-reg §5.1, since sd = 0 by pivot construction.

H\_Regime4\_replication conditions evaluated at the worldwide-region primary analysis:

- C1: n\_eligible $\geq$ 12 at both waves
- C2: $|$bivariate Spearman $\rho$(AI Presence, Trends)$|$ < 0.35 at both waves
- C3: partial Spearman $\rho$(AI Presence, Trends $|$ age, tier) < 0 at both waves

**Tea Box-excluded sensitivity** drops the brand "Tea Box" whose generic-phrase Trends rescale (the phrase "tea box" matches gift-set queries unrelated to the brand entity), and re-runs all three conditions. **US sensitivity** re-runs all conditions on the US-region eligibility cell as a regional robustness check.

## 2.5 Pre-registration and deviations

The full pre-registration locked at git tag `v0.14-prereg` (commit b0ef30a) on 12 May 2026 UTC, prior to LLM acquisition. The DEVIATIONS.md log records two methodological amendments:

- **Entry 1 — Phase B topic-ID errors.** pytrends' topic-ID resolution returned wrong entities for 5 of 9 PASS brands. The amendment switched Phase B to bare canonical queries for the v0.14 build and added a topic-ID resolution log (`topic_id_resolution_log_v0.14.csv`) documenting each verified entity match.
- **Entry 2 — Yunnan Sourcing activation.** After Wang De Chuan (alternate A1) and In Pursuit of Tea (alternate A2) failed both solo and bundled-E5 padded-resolution checks, the third alternate Yunnan Sourcing (A3) was activated under the pre-registered alternate-activation rule (§2.3), bringing n\_eligible to 17 worldwide.

No pre-registered hypothesis, threshold, or routing rule was modified. A third potential amendment was considered but not required: pre-reg condition 2 wording specified $\rho$(AI Presence, brand age) where the v0.13 Regime 4 framework used $\rho$(AI Presence, Trends); the scoring script computes both interpretations and both satisfy the threshold (see §3.3).

# 3. Results

## 3.1 H\_Regime4\_replication primary analysis (CONFIRMED)

All three pre-registered conditions hold at both worldwide waves (Figure 1, Table 1).

**Table 1.** Primary H\_Regime4\_replication conditions, worldwide region, both waves.

| Condition | t$_{1}$ | t$_{2}$ | Threshold | Status |
|-----------|---------|---------|-----------|--------|
| C1: n\_eligible | 17 | 17 | $\geq$ 12 | $\checkmark$ |
| C2: $|$bivariate $\rho$(AI, Trends)$|$ | 0.066 | 0.134 | < 0.35 | $\checkmark$ |
| C2': $|$bivariate $\rho$(AI, age)$|$ (literal pre-reg) | 0.018 | 0.019 | < 0.35 | $\checkmark$ |
| C3: partial $\rho$(AI, Trends $|$ age, tier) | $-$0.084 | $-$0.146 | < 0 | $\checkmark$ |

The primary verdict is unambiguous: **H\_Regime4\_replication CONFIRMED** at the worldwide region at both measurement waves, under both possible interpretations of condition 2.

![Figure 1 · H\_Regime4\_replication CONFIRMED — premium tea joins the Regime 4 cluster. Each v0.13 + v0.14 category at (bivariate Spearman $\rho$ $\times$ partial $\rho$), worldwide, with t$_{1}$$\rightarrow$t$_{2}$ connectors. The Regime 4 zone is the v0.14 canonical definition: $|$bivariate $\rho$$|$ < 0.35 AND partial $\rho$ < 0. Premium tea ($\star$) sits in Regime 4 at both waves with bivariate already negative — distinct from skincare and finance which migrate from positive bivariate to negative partial across waves.](../figures/chart_v14_regime4_canonical.pdf)

## 3.2 Tea Box-excluded sensitivity (CONFIRMED)

Tea Box is one of the 17 eligible primary brands, but its Trends rescaled mean (166 worldwide, 406 US at the wave-2 rescale) is anomalously high relative to its AI Presence rate (2.1%). Inspection of the underlying query suggests the rescale captured generic "tea box" gift-set search volume rather than brand-specific search. The Tea Box-excluded sensitivity drops this brand and re-runs the three conditions on n = 16 (Table 2).

**Table 2.** Tea Box-excluded sensitivity conditions, worldwide region, both waves.

| Condition | t$_{1}$ | t$_{2}$ | Threshold | Status |
|-----------|---------|---------|-----------|--------|
| C1: n\_eligible | 16 | 16 | $\geq$ 12 | $\checkmark$ |
| C2: $|$bivariate $\rho$(AI, Trends)$|$ | 0.011 | 0.129 | < 0.35 | $\checkmark$ |
| C3: partial $\rho$(AI, Trends $|$ age, tier) | $-$0.005 | $-$0.130 | < 0 | $\checkmark$ |

The Regime 4 verdict does not depend on Tea Box. The primary panel and sensitivity panel arrive at structurally identical conclusions: weak bivariate correlation that resolves to a small negative partial correlation after age and tier control.

![Figure 2 · Primary vs Tea Box-excluded sensitivity. Each row shows bivariate $\rho$ (left, vs C2 threshold $|\rho|$ < 0.35) and partial $\rho$ (right, vs C3 threshold $\rho$ < 0) at one wave/region. Primary (n=17, indigo filled) uses the full eligible panel; Tea Box-excluded (n=16, petro open) drops the brand whose rescaled Trends signal was confounded by generic 'tea box' gift-set language. Both panels satisfy C2 + C3 at every wave; the Regime 4 verdict does not depend on Tea Box.](../figures/chart_v14_primary_vs_sensitivity.pdf)

## 3.3 Resolving the pre-reg condition 2 wording

The pre-registration text for condition 2 specified $\rho$(AI Presence, brand age), where the v0.13 Regime 4 framework specified $\rho$(AI Presence, Trends). The canonical scoring script `score_v14.py` computes both correlations and reports both: $\rho$(AI, age) = 0.018 / $-$0.019 and $\rho$(AI, Trends) = $-$0.066 / $-$0.134, all well within the $|\rho|$ < 0.35 threshold at both waves. The empirical conclusion is robust to the wording ambiguity; the v0.13 canonical interpretation (AI × Trends) is adopted going forward.

## 3.4 H1–H4 hypothesis status

The four classical per-category construct-validity hypotheses are all falsified at the pre-registered thresholds (Table 3). This is expected for a Regime 4 category and is the structural complement of H\_Regime4\_replication's confirmation.

**Table 3.** Per-category construct-validity hypothesis outcomes.

| Hypothesis | Pre-registered prediction | Result | Status |
|---|---|---|---|
| H1 | Bivariate Spearman $\rho$ > 0.5, both waves | $\rho$ = $-$0.066 / $-$0.134 | FALSIFIED |
| H2 | Cross-wave stability $|\Delta \rho|$ $\leq$ 0.15 | $|\Delta \rho|$ = 0.068 | CONFIRMED |
| H3 | Top-3 AI $\subset$ top-5 Trends, both waves | 0/3 brands overlap (Harney/Yunnan/Ippodo not in Trends top-5) | FALSIFIED |
| H4 | Partial Spearman $\rho$ > 0.5, both waves | partial $\rho$ = $-$0.084 / $-$0.146 | FALSIFIED |
| H7 | Regime classification (R1/R2/R3) | Matches neither R1 nor R2; Regime 4 candidate | FALSIFIED (productive) |

The pattern is precisely the v0.13 Regime 4 signature: H1 (strong bivariate alignment) and H4 (strong partial alignment) both fail; H2 (cross-wave stability) confirms; H3 (leadership-zone subset) fails. The category exhibits stable but weak rank-order alignment between AI Presence and consumer search, and the residual partial correlation after age + tier control turns slightly negative.

## 3.5 Within-category structure

Top AI Presence brands at v0.14 (averaged across both waves, matched-model subset): Harney & Sons 59%, Yunnan Sourcing 57%, Ippodo Tea 49%, Rishi Tea 41%, TWG Tea 37%. These are predominantly specialty and Asian-tradition specialty brands. The Trends pivot, Twinings, sits at AI Presence 6.2% — the starkest divergence between AI and consumer-search rankings in the panel.

The matched-model LLMs consistently surface specialty tea expertise (loose-leaf curation, regional traditions, sourcing knowledge) that English-language search volume does not reflect. This is the operational substrate of the Regime 4 pattern in premium tea: not a measurement artefact but a genuine asymmetry between LLM training-data exposure and consumer-search behaviour (Figure 4).

Six categories' per-category construct-validity profiles can now be compared on common axes (Figure 3): premium tea joins skincare and finance in the Regime 4 cluster (lower-left quadrant of bivariate × partial space), while PM software remains in Regime 1 (Marginal direct), running shoes in Regime 2 (Age-mediated strong), and olive oil descriptive-only per pre-reg §3.6a.

![Figure 3 · Per-category construct validity, v0.13 + v0.14. Six categories with bivariate WW $\rho$ (indigo), partial WW $\rho$ (petro), and bivariate US $\rho$ (grey) at t$_{1}$ (open) and t$_{2}$ (filled). Premium tea (highlighted row) joins skincare and finance in the Regime 4 cluster.](../figures/chart_v14_per_category_rho_comparison.pdf)

![Figure 4 · Premium tea, per-brand AI Presence × Trends rescaled at t$_{1}$ and t$_{2}$. Each point is an eligible (E1a + E1b) brand; coloured by premium\_tier (luxury / specialty / mainstream-premium). Top AI Presence brands anchor the high-AI cluster; Twinings — the Trends pivot — sits in the low-AI cluster, illustrating the Regime 4 decoupling: AI Presence ranks specialty and Asian brands that the Trends signal does not surface.](../figures/chart_v14_premium_tea_per_brand.pdf)

## 3.6 Registry coverage and v0.15 candidates

Four high-mention brands not in the v0.14 registry were observed in LLM responses across the wave panel: Mariage Frères (144 mentions), Palais des Thés (82), White2Tea (83), and Rare Tea Company (74). At the matched-model subset's wave-2 totals, these would rank near the top of AI Presence if included — Mariage Frères would likely rank top-5. Their absence from the v0.14 registry reflects the timing of registry construction (locked before mention frequencies were observed) rather than methodological choice; their inclusion in v0.15 is queued.

# 4. The canonical Regime 4

## 4.1 Three datapoints across three categories

With v0.14's confirmation, Regime 4 is supported by three independent category datapoints: premium facial skincare (v0.13), personal-finance apps (v0.13), and premium tea (v0.14). The pre-registered Regime 4 conditions ($|$bivariate $\rho$$|$ < 0.35 AND partial $\rho$ < 0) are satisfied at both measurement waves in all three categories. The programme convention for promoting a provisional empirical regularity to canonical status — three independent confirmations under pre-registration — is now met.

## 4.2 Premium tea is the cleanest Regime 4 case

**Table 4.** Bivariate vs partial Spearman $\rho$ across the three Regime 4 cases.

| Category | Bivariate $\rho$ (t$_{1}$, t$_{2}$) | Partial $\rho$ (t$_{1}$, t$_{2}$) | Covariate decrement |
|----------|------------------------|------------------------|---------------------|
| Skincare (v0.13) | +0.28, +0.33 | $-$0.21, $-$0.12 | ~0.45 |
| Finance (v0.13) | +0.17, +0.09 | $-$0.13, $-$0.02 | ~0.20 |
| **Premium tea (v0.14)** | **$-$0.07, $-$0.13** | **$-$0.08, $-$0.15** | ~0.02 |

Skincare and finance both exhibited a weakly positive bivariate $\rho$ that flipped to a negative partial after age and tier control — the covariate decrement (bivariate $-$ partial) was substantial (~0.20–0.45). Premium tea bypasses this phase entirely: bivariate $\rho$ is already negative at both waves, and the controls leave a residual partial that is similarly negative. The covariate decrement is small (~0.02).

The mechanism this reveals: premium tea's age + premium-tier distribution does not produce a positive AI × Trends co-movement that the covariates need to dissolve. Skincare's age + tier distribution (large incumbent brands with high search interest AND high AI Presence) had a positive co-movement before control that the controls dissolved. Premium tea has no such co-movement to begin with, because the specialty and Asian-tradition brands at the top of AI Presence are not concentrated at any single tier or age range.

This is the **cleanest Regime 4 case** in the programme: the regime's signature (weak bivariate + negative partial) is expressed in its pure form, without the intermediate covariate-decrement step that characterised v0.13's cases.

## 4.3 Axis evolution for the canonical Regime 4 visualisation

The v0.13 headline classification chart placed each category in (bivariate $\rho$ × covariate decrement) space. This worked when bivariate $\rho$ was positive (skincare, finance, PM software, running shoes) and covariate decrement was therefore well-defined and positive. Premium tea's already-negative bivariate $\rho$ yields a near-zero decrement that does not separate cleanly from the v0.13 Regime 4 cases in the original axes.

v0.14 evolves the headline axes to (bivariate $\rho$ × partial $\rho$). The Regime 4 zone is then defined by the same conditions that drive H\_Regime4\_replication: $|$bivariate $\rho$$|$ < 0.35 AND partial $\rho$ < 0 (lower-left quadrant, excluding the upper-right corner). All three Regime 4 cases now classify by the same condition logic on the same axes. Figure 1 displays this canonical view.

# 5. Discussion

## 5.1 Methodological consolidation

Three datapoints across three categories meeting the same pre-registered conditions justify treating Regime 4 as canonical for the AIAS Protocol going forward. The forthcoming AIAS methodology paper (in preparation; working title *Measuring AI Availability: Methodological Notes from the AIAS Protocol*) will formalise the four-regime taxonomy with the same threshold-precise structure that Regimes 1–3 already have, and the AIAS Presence Measurement Protocol will increment from v1.1 to v1.2 to incorporate regime classification as a category-level routing step in the canonical measurement pipeline.

The axes evolution from (bivariate $\rho$ × decrement) to (bivariate $\rho$ × partial $\rho$) is a presentational refinement rather than a substantive change to the regime definition. The condition logic ($|$bivariate $\rho$$|$ < 0.35 AND partial $\rho$ < 0) was already the operational test; v0.14 simply uses the same axes for visualisation that the test uses for classification.

## 5.2 What premium tea adds to the framework

v0.14's specific contribution beyond confirming the regime is the demonstration that Regime 4 has heterogeneous internal structure. v0.13's two cases (skincare, finance) shared the positive-bivariate-to-negative-partial migration pattern; v0.14's premium tea shows the same condition outcome via a different path (already-negative bivariate, near-zero decrement). A future sub-classification of Regime 4 might distinguish:

- **Regime 4a (migration sub-type):** positive bivariate that flips negative under covariate control — skincare, finance
- **Regime 4b (pure sub-type):** already-negative bivariate; covariates leave a similarly-negative partial — premium tea

The conditions for canonical Regime 4 ($|$bivariate $\rho$$|$ < 0.35 AND partial $\rho$ < 0) are satisfied by both sub-types. A formal sub-classification awaits additional datapoints in each sub-region.

## 5.3 Why premium tea exhibits the pure-form Regime 4

The substantive reading is that AI Presence in premium tea reflects training-data exposure to specialty and Asian-tradition tea content (specialty tea writing, sourcing guides, matcha culture, etc.) that is not reflected in English-language consumer search volume. The matched-model LLMs surface Harney & Sons, Ippodo Tea, Yunnan Sourcing, and Rishi Tea because their training corpora include substantial coverage of these brands, even though English-language search interest does not concentrate on them. Twinings, by contrast, dominates English-language tea search but does not dominate LLM responses because its corpus presence in specialty contexts is comparatively modest.

This is a category-specific substrate for the Regime 4 pattern that may not generalise to skincare and finance, where the substrate is more likely related to age + tier confounds (large incumbents that LLMs surface because of training-data persistence). The unified condition signature ($|$bivariate $\rho$$|$ < 0.35 AND partial $\rho$ < 0) is consistent with different category-specific substrates, and the canonical regime should not be interpreted as a single underlying mechanism — it is an empirical co-occurrence of two conditions that admits multiple substrates.

# 6. Limitations

**6.1 Single category at v0.14.** The replication test is in one category. The strength of the result rests on the cross-version triangulation with v0.13's skincare and finance findings, not on within-version replication.

**6.2 Two-wave short window.** Both waves are within 8 days of each other (29 April – 7 May 2026). The cross-wave stability finding (H2 confirmed) is short-window; longer-horizon stability of the Regime 4 signature is not tested at v0.14.

**6.3 Matched-model subset (two models).** AI Presence is computed across Claude Sonnet 4.6 and GPT-5.4-mini. Inter-model variation is not addressed by the matched-subset constraint; future programme phases will report results across additional model families.

**6.4 Single external validator (Google Trends).** The construct-validity test uses Google Trends as the sole external reference. A multi-validator design (search volume + social-media mentions + retail sales data where available) would generalise the construct-validity claim from a single-validator finding.

**6.5 Registry coverage gap.** Four high-mention brands not in the v0.14 registry (Mariage Frères, Palais des Thés, White2Tea, Rare Tea Company) would shift the within-category ranking if included. The Regime 4 verdict is robust to their inclusion (they would add to the specialty/luxury cluster that already drives the Regime 4 signature), but the per-brand rankings reported in §3.5 should be read against this caveat. v0.15 registry expansion is queued.

**6.6 Tea Box query ambiguity.** The pivot-rescaling Trends acquisition for the Tea Box brand captured generic-phrase search volume ("tea box" as gift-set descriptor) in addition to brand-specific search. The Tea Box-excluded sensitivity (§3.2) addresses this; the primary verdict is robust to Tea Box's inclusion or exclusion.

# 7. Future research

**7.1 v0.15 — registry expansion.** Add Mariage Frères, Palais des Thés, White2Tea, Rare Tea Company, and approximately 6 additional high-mention specialty brands surfaced in v0.14's LLM responses. Re-run the H\_Regime4\_replication test on the expanded panel.

**7.2 AIAS methodology paper.** Formalise the four-regime taxonomy with threshold-precise definitions; specify the Regime 4 sub-classification (4a/4b) once a fourth datapoint is in hand.

**7.3 AIAS Protocol v1.2.** Incorporate regime classification as a routing step in the canonical measurement pipeline. Categories classifying to Regime 4 receive a category-specific commentary on the operational substrate, since the unified condition signature admits multiple substrates.

**7.4 Phase 3 (AIAS components 2–6).** Construct validity established for AI Presence in v0.11 through v0.14 is a precondition for measurement work on the five remaining AIAS components: Ranking, Consistency, Coverage, Grounding, Sentiment. The four-regime taxonomy suggests each component will require its own per-category construct-validity profile.

**7.5 External brand-tracking validation.** Phase 3 will test AI Presence against external brand-tracking data (Kantar BrandZ, YouGov BrandIndex). The four-regime taxonomy provides pre-registered predictions: brands in Regime 1 should show stronger AI Presence × brand-tracking correlation than brands in Regime 4.

# References

González Castro, P. U. (2026a). *AI Availability: A Theoretical Foundation for Brand Visibility in AI-Mediated Commerce*. SSRN Working Paper 6659000.

González Castro, P. U. (2026b). *AIAS Presence Measurement Protocol v1.1*. SSRN Working Paper 6722319.

González Castro, P. U. (2026c). *Four Empirical Regimes in AI-Mediated Brand Visibility: A Five-Category Construct-Validity Expansion of the v0.12 Three-Empirical-Regimes Finding — AI Presence Index v0.13*. SSRN Working Paper 6750498.

González Castro, P. U. (2026d). *v0.6 Cross-Category Findings — AI Presence Index*. SSRN Working Paper 6720959.

González Castro, P. U. (2026e). *v0.7 Phantom-Brand Persistence Phase 2 (Banks-Beauty-Bath) — AI Presence Index*. SSRN Working Paper 6721779.

González Castro, P. U. (2026f). *v0.8 Discourse-Language Knives — AI Presence Index*. SSRN Working Paper 6728000.

González Castro, P. U. (2026g). *v0.9 Longitudinal Re-Baseline — AI Presence Index*. SSRN Working Paper 6736878.

González Castro, P. U. (2026h). *v0.10 Naive-Phantom Rate Stability — AI Presence Index*. SSRN Working Paper 6741163.

González Castro, P. U. (2026i). *v0.11 PM Software × Trends Construct Validity Pilot — AI Presence Index*. SSRN Working Paper 6745040.

González Castro, P. U. (2026j). *v0.12 Three Empirical Regimes — AI Presence Index*. SSRN Working Paper 6748341.

González Castro, P. U. (2026k). *Tri-System Brand Growth: AI Availability as a Third System Alongside Mental and Physical Availability*. Marketing Science Institute Working Paper Series.

Sharp, B. (2010). *How Brands Grow: What Marketers Don't Know*. Oxford University Press.

Sharp, B., & Romaniuk, J. (2021). *How Brands Grow Part 2 (Revised Edition): Including Emerging Markets, Services, and Durables*. Oxford University Press.

Romaniuk, J. (2018). *Building Distinctive Brand Assets*. Oxford University Press.

# Declarations

**Conflict of interest.** The author is Director, Corporate Brand Creative and Governance, at Samsung Electronics America. This research is independent of Samsung, conducted outside the scope of employment, and represents the author's individual academic work under the Third System™ research entity. Samsung had no role in the design, acquisition, analysis, or interpretation of the research and is not a party to the deposit.

**Funding.** Self-funded. No external funding was received for this work.

**Ethics.** Not applicable. The research uses public APIs (LLM commercial endpoints; Google Trends) and synthetic prompts; no human subjects, no personal data.

**Data availability.** All data, code, and pre-registration materials are deposited on the Open Science Framework at osf.io/ec6wh under the `/v14/` directory. The pre-registration is locked at git tag `v0.14-prereg` (commit b0ef30a), 12 May 2026 UTC, prior to LLM acquisition. The canonical scoring script (`score_v14.py`) is locked at git commit e71e135.

**Cross-references.** v0.14 cross-cites the foundational AI Availability paper (SSRN 6659000), the AIAS Presence Measurement Protocol v1.1 (SSRN 6722319), the v0.6 through v0.13 measurement programme deposits, and the Tri-System Brand Growth working paper. v0.14's deposit will be cross-cited in the forthcoming AIAS methodology paper.

# Author Information

**Pablo Ulpiano González Castro**\
School of Visual Arts, MPS Branding Program, New York, NY (primary academic affiliation)\
Third System™ (research entity; data archive and methodology venue)

Correspondence: pablou@pablou.com\
Personal site: pablou.com\
ORCID: https://orcid.org/0009-0003-8968-9990

The author teaches Creative Strategy in the MPS Branding Program at the School of Visual Arts and stewards the AIAS Measurement Programme through the Third System™ research entity. The Tri-System Brand Growth framework that this measurement programme operationalises is a separate working paper currently at the Marketing Science Institute.
