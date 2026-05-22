---
mainfont: "Carlito"
fontsize: 11pt
geometry: margin=1in
---

\thispagestyle{empty}

\begin{center}

{\small SSRN WORKING PAPER}

\vspace{36pt}

{\fontsize{16}{21.76}\selectfont\bfseries AI Availability and Mental Availability Across Five Categories: A Construct-Validity Expansion of the v0.12 Three-Empirical-Regimes Finding\par}

\vspace{20pt}

\begin{minipage}{0.88\textwidth}
\centering\itshape\small
Pre-Registered Evidence from Project Management Software, Premium Running Shoes, Premium Olive Oil, Premium Facial Skincare, and Personal Finance Apps at Two Longitudinal Waves Against Google Trends; The v0.12 Three-Regime Taxonomy Under-Covers the Five-Category Panel, with Skincare and Personal Finance Defining a Provisional Fourth Empirical Regime (Covariate-Saturated Weak); Mint Anchors the Cleanest Phantom-Brand Persistence Signature in the Programme to Date; v0.12's Marginal Direct Signature and Linear/Todoist Co-Presence Are Both Project-Management-Specific
\end{minipage}

\vspace{24pt}

\begin{minipage}{0.88\textwidth}
\centering\small
Working Paper · Version 0.13 · Construct-Validity Expansion (Project Management Software × Premium Running Shoes × Premium Olive Oil × Premium Facial Skincare × Personal Finance Apps × Google Trends)
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

The AI Availability Score (AIAS) Measurement Programme's Phase 2 construct-validity arc tests whether the three-regime taxonomy of AI Presence × consumer-search rank alignment inferred from a three-category panel (v0.12) generalises to a wider panel. This paper reports the v0.13 expansion to five categories — three reuse-arm carry-forwards (project management software, premium running shoes, premium olive oil) plus two fresh-arm acquisitions (premium facial skincare, personal finance apps) — with eight pre-registered hypotheses (H1–H8) evaluated against an immutable acquisition.

Three of five categories classify cleanly into the pre-registered regimes (PM software → Regime 1 Marginal direct; running → Regime 2 Age-mediated strong; olive oil → Regime 3 Scale-mismatch via the n-floor descriptive route). The two new categories — skincare and finance — fall outside all three: both show sufficient n_eligible, weak bivariate ρ (0.09–0.33), and negative residual partial ρ after controlling for brand age and tier. H7 is consequently falsified at 3-of-5 clean classifications. A fourth empirical regime is provisionally named *Covariate-saturated weak*.

H8 confirms canonically: Mint (Intuit, shutdown announced September 2025) retains 44.79% / 41.67% AI Presence across the two May 2026 waves, ranks fifth by AI Presence in personal finance at both waves, and registers zero Trends signal at both — the cleanest phantom-persistence anchor observed in the programme to date. H5 (the v0.12 marginal signature) and H6 (the Linear-style + Todoist-style co-presence) both falsify at 1-of-4 — what looked like cross-category regularities in the three-category panel turn out to be project-management-software-specific. The cross-category pooled rank-within-category alignment is ρ ≈ 0.46–0.48 (n ≈ 70, p < 0.0001) at both waves: AI Presence and Trends rank-orders do co-vary moderately across categories despite per-category heterogeneity.

**Keywords:** AI-mediated brand visibility · construct validity · phantom-persistence · partial-Spearman correlation · four-regime taxonomy · AI Availability · AIAS Measurement Programme

**JEL Codes:** M31 (Marketing); L86 (Information and Internet Services); L15 (Information and Product Quality); D83 (Search, Learning, and Information); M37 (Advertising)

**Paper status:** Working paper · v0.13 · Five-category construct-validity expansion · Pre-registration locked at git commit 1a6294d (v0.13-prereg tag), 11 May 2026, prior to data collection.

\vspace{8pt}

---

# 1. Introduction

The AIAS (AI Availability Score) Measurement Programme has been collecting per-brand AI Presence rates across selected categories at versioned waves since v0.6 (April 2026), with the operational measurement methodology specified in the AIAS Presence Measurement Protocol v1.1 [@gonzalezcastro2026protocol]. Each phase builds incrementally — sometimes adding waves to the same registry (v0.7 Phantom-Brand BBB, v0.8 Discourse-Language Knives, v0.9 Longitudinal Re-Baseline, v0.10 Naive-Phantom Rate Stability), sometimes adding cross-category comparison structure (v0.6 Cross-Category Findings, v0.11 PM×Trends Construct Validity Pilot, v0.12 Three-Empirical-Regimes Cross-Category Construct Validity).

v0.12 produced a three-regime classification of the AI Presence × consumer-search rank-alignment phenomenon, inferred from a three-category panel: project management software showed a *marginal direct* pattern (ρ ≈ 0.50, low covariate decrement); premium running shoes showed an *age-mediated strong* pattern (ρ ≈ 0.81, large covariate decrement); premium olive oil routed to a *scale-mismatch* description via pre-registration §3.6a (n_eligible = 8 below the n=10 hard floor, descriptive-only). The three regimes were specified ex post from the v0.12 data and lifted into v0.13 as a pre-registered hypothesis structure to test against a wider panel.

The v0.13 study is a five-category construct-validity expansion. It adds two new categories not measured in v0.12: premium facial skincare (31 brands; pivot CeraVe) and personal finance apps (16 brands; pivot YNAB). These categories were selected against three criteria specified at pre-registration §1.3: (a) sufficient brand density at the global scale to permit a 13–35 brand registry; (b) substantive AI Presence signal observed in the v0.9 deposit's matched-model subset; (c) presence of at least one *phantom candidate* — a brand with known operational closure or pre-closure status — to enable a separate phantom-persistence test (Mint, in finance, shut down by Intuit in September 2025).

The five-category panel design tests the v0.12 regime taxonomy by construct-validity expansion rather than longitudinal extension. The pre-registration locked at git commit 1a6294d on 11 May 2026, prior to any v0.13 data collection. Eight pre-registered hypotheses evaluate (H1–H4) per-category construct validity, (H5–H6) cross-category v0.12-pattern generalisation, (H7) clean classification across the three pre-registered regimes, and (H8) the Mint phantom-persistence diagnostic.

The principal v0.13 finding is structural: H7 is falsified at 3-of-5 clean classifications. The two new categories — skincare and finance — occupy an empirical position that the pre-registered three-regime taxonomy does not anticipate. This is presented as a *productive falsification*: the strict all-categories-clean rule for H7 was chosen precisely so that taxonomy under-coverage could be detected, and the construct-validity test functioned as designed. A provisional fourth regime is named *Covariate-saturated weak*, characterised in §5.

A secondary finding: H8 confirms with the cleanest phantom-persistence signature observed in the programme to date. Mint's AI Presence and Trends signatures are documented in §4.5 and Figure 3. Two further findings — that v0.12's marginal signature (H5) and Linear-style / Todoist-style brand co-presence (H6) are both PM-software-specific rather than general — are reported in §4.3 and §4.4.

\vspace{6pt}

# 2. Methods

## 2.1 Categories and registries

Five categories are evaluated in v0.13:

- **Project management software** (reuse arm; 18 registry brands; pivot Asana; data carry-forward from v0.12 deposit).
- **Premium running shoes** (reuse arm; 17 registry brands; pivot Asics; data carry-forward).
- **Premium olive oil** (reuse arm; 20 registry brands; pivot California Olive Ranch; data carry-forward; descriptive-only routing inherited from v0.12 per pre-reg §3.6a).
- **Premium facial skincare** (fresh arm; 31 registry brands; pivot CeraVe; new acquisition).
- **Personal finance apps** (fresh arm; 16 registry brands; pivot YNAB; new acquisition; includes phantom candidate Mint).

Each registry encodes per-brand canonical name, market tier (incumbent / mid-tier / challenger), and brand age (founding year). The v0.12 brand-age registry was extended to 93 brands for v0.13 (46 v0.12 carry-forward entries + 47 new entries for skincare and finance; the 47 new entries carry DRAFT founding years marked for source-URL verification per the post-acquisition methodological note in DEVIATIONS Entry 3 §3.7.2).

## 2.2 AI Presence inputs

Per-brand AI Presence rates are drawn from the v0.9 Longitudinal Re-Baseline deposit (SSRN 6736878), matched-model subset (Claude Sonnet 4.6 + GPT-5.4-mini). t₁ corresponds to the v0.6 collection window (29–30 April 2026, n = 80 responses per category per matched model); t₂ corresponds to the v0.9 collection window (7 May 2026, n = 80 responses per category per matched model). Per-brand AI Presence is computed as the fraction of matched-model responses in which the brand canonical name appears in the response, expressed as a percentage.

The v0.9 deposit includes AI Presence data for all five v0.13 categories, including the two new fresh-arm categories (skincare and finance were added to the v0.6 measurement panel and have been recorded at every wave since). No new AI Presence data is collected for v0.13; the construct-validity work is entirely on the AI-Presence × Trends rank-alignment side.

## 2.3 Google Trends acquisition

Worldwide and US Google Trends signal is acquired via SerpAPI for both waves (29 April 2026 = t₁; 7 May 2026 = t₂) within the same 30-day rolling window for each wave. A multi-stage Phase B resolution protocol (specified at pre-reg §5.2) handles brand-name disambiguation: stage 1 pytrends suggestions, stage 2 solo SerpAPI validation, stage 3 bundled E5 rescue for sparse brands, stage 4 disambiguation queries for ambiguous canonicals (e.g., `mint personal finance` vs. bare `Mint`). One finance brand (Quicken Simplifi) was excluded at E1a (pre-acquisition exclusion) due to no resolvable topic ID; the post-acquisition methodological note is in DEVIATIONS Entry 2.

All raw Trends bundles are then rescaled against the per-category pivot (pivot ≡ 100 within each region) using a wave-window rescaling pipeline. The rescaled per-brand means for each (category, region, wave) cell are the inputs to all subsequent rank-correlation work.

## 2.4 Statistical methods

Eight pre-registered hypotheses (H1–H8) are evaluated against the locked registry. Per-category construct validity is tested via:

- **H1** — Bivariate Spearman ρ > 0.5, p₁ₜ < 0.05 at both waves on Worldwide (primary).
- **H2** — Cross-wave stability: |Δρ| ≤ 0.15.
- **H3** — AI top-3 ⊆ Trends top-5 at both waves (rank concentration at the leadership zone).
- **H4** — Partial Spearman ρ > 0.5 controlling for brand age (years) and market tier (ordinal), p₁ₜ < 0.05 at both waves.

Cross-category integrators are:

- **H5** — v0.12 marginal signature (ρ ∈ [0.35, 0.65] both waves AND H3 falsified at 1 or 2 of 3 at both waves AND ≥1 Linear-style brand surfaces) replicates in 3+ of effective-N categories.
- **H6** — Linear-style + Todoist-style brand co-presence at both waves in 4+ of effective-N categories.
- **H7** — Every category classifies cleanly into exactly one regime (Marginal direct / Age-mediated strong / Scale-mismatch). "Cleanly" means: no boundary flag (within 0.05 of any regime threshold) and no unclassifiable-position label.

The phantom-persistence diagnostic is:

- **H8** — Mint AI Presence ≥ 5% at both waves AND Mint top-5 by AI Presence at both waves AND Mint not top-5 by Trends rescaled mean at either wave. Per pre-reg §11, if Mint is not E1b-eligible (no Trends signal at all), Condition 3 is trivially satisfied.

Partial-Spearman correlation is computed as Pearson on rank-transformed residuals after OLS on rank-transformed covariates (brand_age_years, tier_ordinal), with df correction k = 2 for the two-covariate adjustment. The n-floor structure is hard 10 (descriptive-only routing below) with an alignment floor of 12 per pre-reg §3.4. Pivots are exempted from E1b (Phase B at-acquisition exclusion) per pre-reg §5.1.

All hypothesis evaluation runs on the canonical scoring script `score_v13.py`, locked at git commit `e8f3694` and reproducible from the v0.13 OSF deposit.

## 2.5 Pre-registration and OSF deposit

The v0.13 pre-registration is locked at git commit `1a6294d` (tag `v0.13-prereg`), 11 May 2026, prior to data collection. Two pre-lock amendments and one post-acquisition methodological observation are documented in `DEVIATIONS.md` Entries 1, 2, and 3 (Entry 1 = YNAB query disambiguation correction pre-lock; Entry 2 = Quicken Simplifi E1a exclusion + B2 padding amendment; Entry 3 = the empirical four-regime finding documented in §5 of this paper).

All raw acquisition logs, processed Trends data, scoring outputs, and figures are deposited at OSF project ec6wh under the `/v13/` folder. The deposit is structured per the AIAS programme's standard manifest (README, MANIFEST, data/, registries/, figures/, analysis/, DEVIATIONS.md, PRE_REGISTRATION_v0_13.md).

\vspace{6pt}

# 3. Results

## 3.1 Per-category construct validity (H1–H4)

Table 1 reports the eight pre-registered hypothesis outcomes. Per-category H1–H4 results vary structurally across the five categories, which is the principal substantive observation driving the H7 falsification reported in §3.2.

Per-category bivariate Spearman ρ at t₁ / t₂ on Worldwide:

- PM software: ρ = 0.506 / 0.482 (n = 17 / 18; p₁ₜ = 0.019 / 0.022)
- Premium olive oil: ρ = 0.168 / −0.095 (n = 8 / 8; descriptive-only)
- Premium running shoes: ρ = 0.808 / 0.786 (n = 12 / 12; p₁ₜ = 0.0007 / 0.0012)
- Premium facial skincare: ρ = 0.282 / 0.332 (n = 28 / 28; p₁ₜ = 0.073 / 0.042)
- Personal finance apps: ρ = 0.168 / 0.094 (n = 13 / 13; p₁ₜ = 0.292 / 0.380)

H1 confirms decisively for running (both waves above 0.5 and below p = 0.05). H1 misses marginally for PM software (t₂ ρ = 0.482, just below the 0.5 threshold; the v0.12 result was ρ = 0.476, also just below at one wave — the marginal-direct pattern reproduces across versions). H1 falsifies for skincare and finance: both have bivariate ρ well below 0.5 at both waves. H2 (cross-wave stability) confirms across all four confirmatory categories: |Δρ| is 0.024 (PM), 0.022 (running), 0.050 (skincare), 0.074 (finance) — all under the 0.15 threshold.

H3 (AI top-3 ⊆ Trends top-5) falsifies in every confirmatory category. The intersection size is 1 of 3 at both waves for PM and finance, 2 of 3 at both waves for running and skincare. This is the pattern noted in v0.12 PM software analysis ("rank concentration at the leadership zone is divergent across the two measurement layers") and now appears as a cross-category regularity.

H4 (partial-Spearman with age + tier control) falsifies in every confirmatory category, but the residual structure differs dramatically. PM partial ρ at t₁ / t₂ = 0.417 / 0.434; the covariate decrement is small (0.089 / 0.048) — the bivariate signal survives controlling for age and tier. Running partial ρ = 0.466 / 0.488; the decrement is large (0.342 / 0.298) — much of the bivariate signal is attributable to age and tier joint variation. Skincare partial ρ = −0.205 / −0.117 — *negative*; the covariates absorb more than the bivariate signal. Finance partial ρ = −0.159 / −0.287 — also negative. The four confirmatory categories produce four structurally distinct covariate-decrement profiles.

## 3.2 H7 — Three-regimes clean classification

H7 is the cross-category integrator that asks whether every category classifies cleanly into one of the three pre-registered regimes. Per the pre-registration §2 H7 decision tree:

- **Regime 1 — Marginal direct**: bivariate ρ ∈ [0.35, 0.65] at both waves, decrement ≤ 0.15 at both waves, n ≥ 10. PM software classifies here cleanly (no boundary flag).
- **Regime 2 — Age-mediated strong**: bivariate ρ > 0.65 at both waves, decrement > 0.25 at both waves, n ≥ 10. Running classifies here; with a boundary flag at t₂ (decrement_t₂ = 0.298 against the 0.25 floor — within the 0.05 tolerance).
- **Regime 3 — Scale-mismatch**: n_eligible < 0.6 × n_matched_subset at either wave OR descriptive-only routing via §3.6a. Olive oil classifies here cleanly via the §3.6a descriptive-only route (n = 8 below the n = 10 hard floor).

The two new categories — skincare and finance — do not classify into any of these. Skincare's bivariate ρ at t₁ / t₂ = 0.282 / 0.332 sits below the Regime 1 lower bound of 0.35 (t₂ within 0.05 — boundary-flagged). Finance's bivariate ρ at t₁ / t₂ = 0.168 / 0.094 sits well below 0.35 at both waves. Neither category meets the Regime 3 n-fraction criterion (skincare n_eligible = 28 of 31 = 90.3%; finance n_eligible = 13 of 15 live brands = 86.7%; both well above the 0.6 × matched-subset threshold).

Per the strict all-categories-clean rule, H7 is **falsified at 3-of-5 clean classifications**. Two of five categories occupy an empirical position outside the pre-registered three-regime taxonomy.

Figure 1 plots the five categories in (bivariate ρ × covariate decrement) space, with pre-registered regime zones shown as background bands. Skincare and finance sit in the unfilled region of the diagram — sufficient n_eligible, weak bivariate ρ, large covariate decrement (because the residual is so heavily absorbed that the partial ρ goes negative).

![Four-regime classification of v0.13 categories. Each category at bivariate ρ × covariate decrement. Three regimes pre-registered (background zones); skincare and finance fall outside all three, defining a provisional fourth pattern (Covariate-saturated weak). Olive oil routes to Regime 3 descriptive-only per §3.6a (n=8, below n=10 floor) and is not plotted. Points colored by H7 classification.](../figures/chart_v13_h7_fourregime_classification.pdf){#fig:fourregime}

## 3.3 H5 — v0.12 marginal signature replication

The v0.12 marginal signature is defined at pre-reg §2 H5 as: bivariate ρ ∈ [0.35, 0.65] at both waves AND H3 falsified at 1 or 2 of 3 at both waves AND at least one Linear-style brand (AI ≥ 50%, Trends ≤ 5) surfaces in the category. H5 confirms if 3 or more of the effective-N categories show this signature.

Per the v0.13 measurement, the signature is present in PM software (ρ in range; H3 at 1 of 3 both waves; Linear-style brand present = Linear), absent in running (ρ at 0.81 outside the [0.35, 0.65] band), absent in skincare (ρ at 0.28–0.33, partly in range but no Linear-style brand surfaces), and absent in finance (ρ well below 0.35; no Linear-style brand). H5 is falsified at 1-of-4 against a 3-of-effective-N threshold.

The substantive interpretation is that what looked like a candidate cross-category regularity in the three-category panel is in fact PM-software-specific. The marginal-direct pattern at ρ ≈ 0.5 with Linear-style brands surfacing is a structural property of project management software's brand ecology, not a generalisable feature of AI-mediated visibility in general.

## 3.4 H6 — Linear-style + Todoist-style co-presence

H6 tests whether Linear-style brands (AI ≥ 50%, Trends ≤ 5) AND Todoist-style brands (AI ≤ 5%, Trends ≥ 20) both appear in the category at both waves, in 4+ of effective-N categories.

Only PM software shows both: Linear-style = {Linear} at both waves; Todoist-style = {Todoist} at t₁, {Basecamp, Todoist} at t₂. Running shows Linear-style brands ({Brooks, Hoka}) but no Todoist-style brand at either wave (the asymmetric boundary mismatch noted in v0.12). Skincare and finance both show Todoist-style brands ({Clinique, Olay, Beauty of Joseon} in skincare; {Origin, Cleo} in finance) but no Linear-style brand at either wave — neither category has any brand with sufficient AI Presence to clear the 50% Linear-style threshold.

H6 is falsified at 1-of-4 against a 4-of-effective-N threshold. The Linear / Todoist bidirectional pattern is, like the marginal-direct signature, PM-software-specific.

## 3.5 H8 — Mint phantom-persistence canonical confirmation

The H8 phantom-persistence diagnostic evaluates three pre-registered conditions:

- **C1** — Mint AI Presence ≥ 5% at both waves. Mint t₁ = 44.79%; t₂ = 41.67%. Both ≥ 5%. ✓
- **C2** — Mint top-5 by AI Presence at both waves. Mint rank t₁ = 5; t₂ = 5. ✓
- **C3** — Mint NOT top-5 by Trends rescaled mean at either wave. Mint is not E1b-eligible at either wave (Worldwide rescaled mean = 0.0; US rescaled mean = 0.0). Per pre-reg §11, when the phantom candidate has no Trends signal at all, Condition 3 is trivially satisfied (being outside the top-5 by Trends rank is logically guaranteed). ✓

All three conditions satisfied — **H8 confirmed**. Figure 3 shows the Mint anchor configuration.

This is the cleanest phantom-persistence signature observed across the AIAS programme. Intuit announced Mint's shutdown in October 2023 and completed the discontinuation in September 2025; the v0.13 measurement is approximately seven to nine months post-completion. Mint retains AI Presence virtually unchanged from a year-prior measurement (the v0.7 wave reported 41% AI Presence in personal finance — within 0.8 percentage points of the v0.13 t₂ value). The Trends signal across the same span is uniformly zero. The phantom-persistence regularity, first observed in v0.7's beauty-and-cosmetics Banks-Beauty-Bath panel, replicates at strength in personal finance.

![Mint phantom-persistence canonical confirmation. Mint retains substantial AI Presence (44.79% t₁ / 41.67% t₂) with no measurable Trends signal at either wave. All three pre-registered conditions hold (C1: AI ≥ 5% both waves ✓; C2: AI rank 5 / 5 ✓; C3: not Trends top-5 either wave ✓, trivially satisfied per §11 since Mint has no Trends signal).](../figures/chart_v13_h8_mint_phantom.pdf){#fig:mint}

## 3.6 Pooled cross-category sensitivity

Despite the per-category heterogeneity reported in §3.1, the pooled rank-within-category alignment across the four confirmatory categories is moderately strong and stable across waves. Stacking eligible non-E1a brands by within-category rank produces n = 70 at t₁, n = 71 at t₂. The pooled Spearman ρ on this stacked dataset is 0.459 (p = 0.0001) at t₁ and 0.475 (p < 0.0001) at t₂.

The interpretation is that AI Presence and consumer-search rank orders co-vary moderately when assessed at the rank-within-category level across the wider panel — but the strength of the within-category correlation varies dramatically by regime, from Regime 2's ρ ≈ 0.8 down to the provisional Regime 4 categories' ρ ≈ 0.1–0.3. The pooled signal exists; it is structurally heterogeneous beneath the aggregate.

![Pooled cross-category rank alignment. Rank-within-category, stacked across the four confirmatory categories (PM software, running, skincare, finance). Despite heterogeneous within-category outcomes, the pooled rank-order alignment is moderately strong and stable across waves.](../figures/chart_v13_pooled_rank_scatter.pdf){#fig:pooled}

\vspace{6pt}

# 4. The fourth empirical regime

## 4.1 Empirical signature

Skincare and finance share a distinctive empirical pattern not anticipated by Regimes 1, 2, or 3. The pattern's three diagnostic features:

1. **n_eligible above the hard floor.** Both categories have eligible-brand counts well above the n = 10 floor and the n = 12 alignment floor. Skincare n = 28 (28/31 = 90.3% of registry); finance n = 13 (13/15 live = 86.7%). Neither qualifies for Regime 3's scale-mismatch n-fraction route.
2. **Positive but weak bivariate ρ.** Both categories register a positive Spearman ρ that is well below the Regime 1 lower bound of 0.35. The signal is detectably present (skincare ρ_t₁ = 0.282 has p₁ₜ = 0.073; ρ_t₂ = 0.332 reaches p < 0.05) but at less than half the magnitude required for Regime 1.
3. **Negative residual partial ρ.** After controlling for brand age and market tier, the residual partial-Spearman correlation goes negative in both categories. Skincare: −0.205 / −0.117. Finance: −0.159 / −0.287. The covariates absorb the entire bivariate signal and then some.

The bivariate-minus-partial decrement is large in absolute terms — 0.487 / 0.449 for skincare; 0.327 / 0.381 for finance. But the *starting* bivariate ρ is so low that the absorbed quantity is small, and the residual partial ρ ends up below zero. This is structurally distinct from Regime 2's pattern (large bivariate, large decrement, residual partial still positive at ≈ 0.5) and from Regime 1's pattern (moderate bivariate, small decrement, residual partial still positive at ≈ 0.4).

## 4.2 Provisional naming

The provisional name for this regime is **Covariate-saturated weak**: moderate-to-large n, positive but weak bivariate ρ, fully covariate-absorbed with negative residual partial ρ. The theoretical interpretation is that in these categories, AI mediation surfaces brands that match the underlying maturity / tier gradient but does not produce a Trends rank co-movement beyond what age and tier alone would predict. Whatever bivariate signal exists is essentially an artefact of the age + tier joint distribution.

The naming is provisional pending formal definition in a forthcoming AIAS methodology paper. Until then, the regime is recorded in the canonical scoring output as "Unclassifiable against the v0.12 three-regime taxonomy" and in the brand-format report as the fourth empirical regime.

## 4.3 What distinguishes the two regimes provisionally classified as Regime 4

Skincare and finance both occupy the provisional fourth regime, but they sit at different positions within it. Skincare's bivariate ρ at t₂ = 0.332 — only 0.018 below the Regime 1 floor of 0.35. With slightly cleaner Trends measurement (or a small model-mix shift), skincare could enter Regime 1. The H7 boundary flag on skincare's t₂ ρ acknowledges this proximity.

Finance, by contrast, is unambiguously inside Regime 4 territory. Its bivariate ρ at both waves (0.168 and 0.094) is well below 0.35 — not boundary-flagged at any regime threshold. Finance has only 13 eligible brands of 15 live (after the Quicken Simplifi E1a exclusion and the Mint and Lunch Money Worldwide-non-eligibility), and the smaller n combines with the genuinely low rank alignment to produce a confident Regime 4 classification.

The provisional Regime 4 may thus require further sub-classification in future programme phases. Two structurally similar categories at different positions within the same regime suggest the regime is not yet fully characterised. A formal Regime 4 definition would specify both the threshold structure and (likely) a sub-classification into "boundary-of-Regime-1" and "stable-Regime-4" sub-regions.

\vspace{6pt}

# 5. Secondary findings

## 5.1 Within-category scale mismatch — Lunch Money

The finance category exhibits a sub-category scale-mismatch case: Lunch Money is Worldwide-ineligible (rescaled mean 0.0 at both waves) but US-eligible at both waves (rescaled mean rises slightly from t₁ to t₂). AI Presence is low but rising (1.0% → 6.2%). Phase B disposition was PASS_E5 (E5 bundled rescue at the diagnostic worldwide window), but the wave-window rescaling subsequently returned 0.0 worldwide. The brand appears operationally active, with detectable AI Presence and detectable US Trends signal, but Worldwide Trends signal below the platform's display threshold.

The pattern is structurally analogous to Mint's phantom-persistence on the AI-Presence side and to the olive-oil scale-mismatch on the Trends side, but operates at a single brand within a confirmatory category rather than at category aggregate level. The descriptive observation is not pre-registered as a separate hypothesis; it is documented for cross-version programme continuity.

## 5.2 Within-category scale mismatch — SK-II, Vanicream

Two skincare brands show the same Worldwide-vs-US asymmetry as Lunch Money: SK-II (Worldwide 0.0 / 0.0; US 0.30 / 0.62) and Vanicream (Worldwide 0.0 / 0.0; US 1.13 / 1.55). SK-II is a J&J / P&G premium brand historically concentrated in East Asia; Vanicream is a niche US-domestic dermatologist-recommended brand. Both have substantive AI Presence (not reported in detail here; see canonical scoring output) but Worldwide Trends signal below the platform's display threshold.

The presence of intra-category scale mismatch in two of the four confirmatory categories (finance: Lunch Money; skincare: SK-II, Vanicream) suggests scale mismatch is not exclusively a between-category phenomenon (as in olive oil's §3.6a routing) but operates at the brand level within categories too. Region-specific subset analyses may be warranted in future phases.

## 5.3 First observed inter-wave eligibility transition — Height

The PM software brand Height (a challenger-tier project management tool) crosses the eligibility floor between t₁ and t₂: Worldwide t₁ mean = 0.0 (eligible False), Worldwide t₂ mean = 1.97 (eligible True). The brand's Worldwide Trends signal lifted from below-display to above-display across the eight-day inter-wave interval.

This is the first inter-wave eligibility transition observed across the AIAS programme (v0.6 through v0.13). The transition does not affect H1–H4 evaluation logic — per-wave correlations are computed on each wave's eligible set independently — but the increment in n_eligible (PM software t₁ n = 17 → t₂ n = 18) is recorded for programme continuity. Future versions may want to track eligibility transitions as a separate descriptive measure.

\vspace{6pt}

# 6. Discussion

## 6.1 Construct-validity test outcome

The v0.13 study was designed as a construct-validity expansion to test whether the v0.12 three-regime taxonomy generalises to a wider panel. It does not. The taxonomy under-covers the five-category panel: two of five categories occupy a position the taxonomy does not anticipate. This is a *successful construct-validity test* — the strict all-categories-clean rule for H7 was chosen precisely so that taxonomy under-coverage could be detected. It was detected; the framework's three-regime structure was found to be incomplete.

This is presented as a productive falsification rather than a methodological failure. The pre-registered hypothesis was specified ex ante from a smaller panel; the wider panel revealed structural variety the smaller panel could not have surfaced; the framework now requires a fourth empirical regime to absorb the new variety. The v0.12 paper's three-regime taxonomy is not refuted in its original scope — it correctly describes the three-category panel from which it was inferred. v0.13 establishes that the taxonomy *under-covers* the wider 5-category panel.

## 6.2 The PM-specificity of v0.12's cross-category signature

H5 (the v0.12 marginal signature) and H6 (the Linear-style + Todoist-style co-presence) both falsify at 1-of-4 in the v0.13 panel — only PM software replicates either pattern. The substantive conclusion is that what looked like a candidate cross-category regularity in the three-category panel turns out to be project-management-software-specific.

The marginal-direct pattern (ρ ≈ 0.5 with rank-concentration divergence at the leadership zone) and the Linear-style / Todoist-style brand co-presence both appear to be structural properties of project management software's specific brand ecology — likely related to PM software's combination of (a) sub-category scale heterogeneity (consumer task-management apps like Todoist sit in the same registry as enterprise platforms like Jira), (b) a high-AI-Presence challenger brand (Linear) operating from a small-Trends base, and (c) the discontinuity between conversational AI's recommendation pattern and consumer search query distribution.

The narrowing of the v0.12 claim's scope is not a refutation of v0.12's substantive analysis; it is a sharper specification of which categories the v0.12 paper actually describes. The v0.13 results would have been impossible to obtain without v0.12's prior characterisation.

## 6.3 Mint phantom-persistence and the Phantom Brand Persistence regularity

The H8 Mint confirmation is the cleanest phantom-persistence anchor observed in the AIAS programme. Mint sustains 41–45% AI Presence at v0.13, with zero Trends signal in both regions at both waves, approximately seven to nine months after Intuit's announced shutdown completed. The AI Presence value is essentially unchanged from a year-prior measurement (v0.7 reported 41% in the same matched-model subset for the same category).

The Phantom Brand Persistence regularity — first surfaced in v0.7 in the cosmetics-and-personal-care category (Banks-Beauty-Bath panel) and reconfirmed across v0.8, v0.9, v0.10, and now v0.13 — is now sufficiently well-documented across categories and time to be classified as a programme-level empirical regularity. AI Presence values can be sustained at substantial magnitudes for brands operating in pre-AI-training-window markets long after the brand has formally exited the market. The regularity is methodologically important for any system that uses AI Presence as a brand-tracking signal: the signal does not decay in step with operational reality.

## 6.4 The provisional Regime 4 and methodological implications for the AIAS Protocol

The provisional Regime 4 finding has implications for the AIAS Presence Measurement Protocol v1.1 [@gonzalezcastro2026protocol]. The protocol governs measurement; the regime taxonomy is downstream. The Regime 4 finding does not require any change to v1.1's measurement methodology — the AI Presence values themselves are not in question.

The finding does suggest two action items for the programme: (a) a methodology note formalising Regime 4 with threshold-precise definitions analogous to those for Regimes 1–3, slated for the AIAS methodology paper following Tri-System paper clearance; (b) future cross-category phases sampling at least one Regime 4 candidate (high brand-age dispersion, weak prima-facie AI Presence × Trends alignment) to verify regime stability beyond skincare and finance. Premium tea remains a Phase 3 candidate; whether premium tea sits in Regime 3 (descriptive-only) or Regime 4 (covariate-saturated weak) is empirically open until measured.

\vspace{6pt}

# 7. Limitations

**Matched-model subset.** AI Presence is measured against a two-model matched subset (Claude Sonnet 4.6 + GPT-5.4-mini). The Tri-System framework's three-mode response taxonomy (Brand mode / Component mode / Authority mode) suggests inter-model variation in AI Presence may be substantial; the matched-subset constraint factors out this variation but does not address it. Future programme phases will report results across additional model families.

**Single-vendor Trends signal.** Consumer-search signal is sourced exclusively from Google Trends via SerpAPI. The validity of Trends as a Mental Availability proxy is established at scale (Mehrotra and others 2023) but no programme phase has cross-validated against an independent consumer-search vendor. Bing, Baidu, and Yandex Trends are not measured.

**Brand-age draft values.** 47 of 93 brand-age entries (the v0.13-new entries for skincare and finance) carry DRAFT founding years pending source-URL verification. The H1–H8 results in this paper compute on the DRAFT values. The author commits to source-verifying each entry before subsequent programme deposits; founding-year corrections will be applied via a future amendment per DEVIATIONS Entry 3 §3.7.2.

**Two-wave design.** v0.13 measures at two waves (t₁ = 29 April 2026; t₂ = 7 May 2026), separated by eight days. The cross-wave stability that H2 confirms is therefore short-window. The H8 phantom-persistence finding is longer-horizon (Mint's AI Presence is approximately unchanged from a year-prior v0.7 measurement) but is a single-brand observation rather than a population-level longitudinal design.

**Five-category panel.** Five categories is wider than v0.12's three but still small relative to the total category space. The provisional Regime 4 finding rests on two categories. Future phases will sample additional candidates to test regime stability.

**No incumbent-tier phantoms.** v0.13's phantom test is restricted to a single phantom candidate (Mint) in a single category (finance). The Phantom Brand Persistence regularity in v0.7 was observed across multiple challenger-tier brands in cosmetics. v0.13 does not address whether the regularity differs across market tiers or across categories with different operational-closure timing patterns.

\vspace{6pt}

# 8. Future research

**v0.14 candidate pool.** Two cross-lingual candidates remain on the programme's Phase 3 list: premium tea (a likely Regime 4 candidate — high brand-age dispersion, Latin-script and CJK-script registries) and traditional spirits (a likely Regime 2 or Regime 4 candidate — strong age-mediation expected, with cross-region Trends asymmetry possible).

**AIAS methodology paper.** A short methodology note formalising Regime 4 with threshold-precise definitions is queued behind the Tri-System Brand Growth paper [@gonzalezcastro2026tri]. The AIAS Presence Measurement Protocol v1.1 will incrementally version to v1.2 to incorporate the regime taxonomy as a category-classification step in the canonical measurement pipeline.

**Construct-validity validation against external brand tracking.** Phase 3 of the AIAS programme — contingent on Phase 2 completion — will study construct validity through correlation with external brand-tracking data (Kantar BrandZ, YouGov BrandIndex, Brand Health Tracker panels). The four-regime taxonomy provides a structured set of pre-registered predictions: brands in Regime 1 should show stronger AI Presence × brand-tracking correlation than brands in Regimes 3 or 4.

**Extension to AIAS components beyond Presence.** Phase 4 of the AIAS programme will release the five additional AIAS components (Ranking, Consistency, Coverage, Grounding, Sentiment). The four-regime classification may extend to these components or may produce different regime structures for different components. Cross-component validity of the regime taxonomy is open empirically.

\vspace{12pt}

# References

González Castro, P. U. (2026a). *AI Availability and the Architecture of Brand Growth*. SSRN Working Paper. SSRN: 6659000.

González Castro, P. U. (2026b). *AIAS Presence Measurement Protocol, Version 1.1*. Third System Methodology Brief. SSRN: 6722319.

González Castro, P. U. (2026c). *Cross-Category Findings: AI Presence Index v0.6*. Third System. SSRN: 6720959.

González Castro, P. U. (2026d). *Phantom-Brand Persistence in Banks, Beauty, and Bath: AI Presence Index v0.7*. Third System. SSRN: 6721779.

González Castro, P. U. (2026e). *Discourse-Language Knives: AI Presence Index v0.8*. Third System. SSRN: 6728000.

González Castro, P. U. (2026f). *Longitudinal Re-Baseline: AI Presence Index v0.9*. Third System. SSRN: 6736878.

González Castro, P. U. (2026g). *Naive-Phantom Rate Stability: AI Presence Index v0.10*. Third System. SSRN: 6741163.

González Castro, P. U. (2026h). *PM × Trends Construct Validity Pilot: AI Presence Index v0.11*. Third System. SSRN: 6745040.

González Castro, P. U. (2026i). *Three Empirical Regimes: AI Presence Index v0.12*. Third System. SSRN: 6748341.

Ehrenberg, A. S. C. (1959). *The Pattern of Consumer Purchases*. Applied Statistics, 8(1): 26–41.

Romaniuk, J., and Sharp, B. (2022). *How Brands Grow Part 2 (revised edition)*. Oxford University Press.

Sharp, B. (2010). *How Brands Grow: What Marketers Don't Know*. Oxford University Press.

Sharp, B., and Romaniuk, J. (2018). *Building Distinctive Brand Assets*. Oxford University Press.

\vspace{12pt}

# Declarations

**Conflict of interest.** The author is employed in brand strategy at Samsung Electronics SEA and teaches at the School of Visual Arts MPS Branding Program. The author's opinions are his own and do not represent the position of Samsung Electronics or any other organization. This research is independent and unrelated to that employment.

**Funding.** This research received no external funding. The AIAS Measurement Programme is operated independently under the Third System research entity.

**Data availability.** All raw acquisition logs, processed Trends data, scoring outputs, registries, figures, pre-registration document, and deviations log are deposited at the OSF project ec6wh under the `/v13/` folder. Acquisition scripts (`acquire_trends_v13.py`, `rescale_trends_v13.py`, `phaseA_validate_v13.py`, `phaseB_resolve_v13.py`, `score_v13.py`, `build_charts_v13.py`) are available at the same deposit. The pre-registration is locked at git commit `1a6294d` (tag `v0.13-prereg`).

**Replication.** The canonical analysis can be reproduced from the OSF deposit by checkout-and-run of the `score_v13.py` script against the deposit's processed-Trends and registry files. Expected runtime: under 30 seconds on a modern laptop.

\vspace{12pt}

# Author Information

**Pablo Ulpiano González Castro** is Principal Researcher at Third System and Faculty in the MPS Branding Program at the School of Visual Arts (New York). His research extends Ehrenberg-Bass brand growth science into AI-mediated commerce through the AI Availability framework — operationalised as the AI Availability Score (AIAS), a 0–100 composite across six measurable dimensions (Presence, Ranking, Consistency, Coverage, Grounding, Sentiment). The AIAS Measurement Programme publishes methodology, datasets, and findings openly at thirdsystem.ai.

**Correspondence:** pablou@pablou.com · pablou.com

**ORCID:** [0009-0003-8968-9990](https://orcid.org/0009-0003-8968-9990)

**Citation format:** González Castro, P. U. (2026). *AI Availability and Mental Availability Across Five Categories: A Construct-Validity Expansion of the v0.12 Three-Empirical-Regimes Finding*. Third System. AI Presence Index v0.13. SSRN: https://ssrn.com/abstract=6750498.
