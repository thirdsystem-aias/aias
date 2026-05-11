---
mainfont: "Carlito"
fontsize: 11pt
documentclass: article
geometry: margin=1in
linkcolor: black
urlcolor: black
---

\thispagestyle{empty}

\begin{center}

\textbf{SSRN WORKING PAPER}

\vspace{2em}

{\fontsize{16}{20}\selectfont\bfseries AI Availability and Mental Availability Across Three Categories: A Cross-Category Construct-Validity Expansion of the v0.11 Boundary-Mismatch Finding\par}

\vspace{0.8em}

\textit{Pre-Registered Evidence from Project Management Software, Premium Running Shoes, and Premium Olive Oil at Two Longitudinal Waves Against Google Trends; v0.11 Replicates Precisely in PM Software, Running Shoes Show a Strong Age-Mediated Correlation with Asymmetric Boundary Mismatch, and Olive Oil Reveals a Category-Scale Mismatch Where Half the Matched Subset Cannot Be Placed on the Same Scale}

\vspace{2em}

\textit{Working Paper · Version 0.12 · Cross-Category Construct-Validity Expansion (Project Management Software × Premium Running Shoes × Premium Olive Oil × Google Trends)}

\vspace{2.5em}

\textbf{Pablo Ulpiano González Castro}

\vspace{0.8em}

School of Visual Arts, MPS Branding Program, New York, NY\\
\textit{(primary academic affiliation)}

\vspace{0.8em}

Third System™ (research entity; data archive and methodology venue)

\vspace{0.8em}

Correspondence: pablou@pablou.com · pablou.com

ORCID: \url{https://orcid.org/0009-0003-8968-9990}

\vspace{2.5em}

11 May 2026

\vspace{2.5em}

\textit{Working paper. Not under peer review. Pre-registered.}

\end{center}

\newpage

\setlength{\parskip}{8pt}
\setlength{\parindent}{0pt}

## Abstract

This paper reports the v0.12 construct-validity expansion in the AIAS measurement programme: a pre-registered three-category test extending the v0.11 single-category pilot to project management software (replication), premium running shoes (new), and premium olive oil (new). The test design adds two cross-category hypotheses (H5 cross-category generalisation; H6 cross-category Linear-style + Todoist-style detection) and a descriptive-only route for categories where the n-floor is breached, formalised in pre-reg §3.4a. Six per-category and two cross-category hypotheses with explicit numerical thresholds were committed to a pre-registration document locked at git commit ae4bd3a (tag *v0.12-prereg*) prior to any Google Trends acquisition call against the wave windows.

The result set is informative in a way that the original generalisation prediction would not have been. v0.11's PM-software finding replicates with high precision (Spearman ρ = 0.506 at t₁, 0.482 at t₂ — within 0.010 of v0.11's 0.496 and 0.476; H3 falsifies identically at 1 of 3 both waves; H6 confirms with Linear and Todoist surfacing as the same diagnostic cases). Premium running shoes shows a structurally different empirical regime: Spearman ρ = 0.808 at t₁ and 0.786 at t₂, both well above the moderate-to-strong threshold and significant at *p* < 0.002 — H1 confirmed; but H3 falsifies (2 of 3 both waves) and the partial Spearman ρ after age + tier control drops to 0.466 and 0.488, indicating that brand age and competitive density mediate approximately 40 percent of the bivariate correlation; H6 falsifies asymmetrically (Linear-style brands present — Brooks at t₁, Hoka at t₂ — but no Todoist-style brand surfaces in either wave). Premium olive oil routes to descriptive-only per pre-reg §3.4a (n = 8 at Worldwide, n = 7 at US, both below the hard floor of 10) and reveals a third empirical regime: a Category-Scale Mismatch where 7 of 15 matched-subset brands (46.7 percent) have non-trivial AI Presence rates (≥ 5 percent) but Trends signal below display threshold. The cross-category hypotheses H5 and H6 are both falsified, but for asymmetric reasons: H5 because running's ρ is substantially above the v0.11 signature threshold rather than below it; H6 because running lacks any Todoist-style brand.

The substantive interpretation that emerges is sharper than the pre-registered generalisation prediction would have been. The empirical relationship between AI Availability and Mental Availability is category-dependent, supporting the Tri-System Brand Growth framework's separability claim across three distinct empirical regimes. What unifies them is the persistence of category-boundary mismatch (H3 falsified in both confirmatory-eligible categories): AI applies a tighter and partly-different category boundary than consumer search does, even when the bivariate correlation between the two systems is strong. What differentiates them is magnitude and structure: low-volume B2B SaaS shows marginal correlation with bidirectional mismatch; high-volume B2C consumer durables show strong correlation substantially mediated by brand age with asymmetric mismatch; premium consumer packaged goods show scale mismatch where the constructs cannot be placed on the same scale at all. The headline finding is that AI Availability is not a "tighter boundary on the same scale" everywhere — it is a constructively distinct layer whose empirical relationship to Mental Availability varies systematically with category structure.

## Keywords

AI Availability; AI Presence; Mental Availability; brand mediation; construct validity; AIAS; Google Trends; pre-registered measurement; longitudinal replication; cross-category generalisation; project management software; premium running shoes; premium olive oil; LLM brand recommendations; Category-Scale Mismatch; boundary mismatch

## JEL Classification

M31 (Marketing) — primary; L86 (Information and Internet Services; Computer Software); L15 (Information and Product Quality); D83 (Search; Learning; Information and Knowledge; Communication; Belief; Unawareness); M37 (Advertising)

## Paper status

Working paper. Not under peer review. Pre-registered. Continues Phase 3 of the AIAS measurement programme. Builds directly on the v0.11 construct-validity pilot deposited in *A Construct-Validity Pilot for AI Presence Against External Behavioural Data* ([SSRN ID 6745040](https://ssrn.com/abstract=6745040)), which established the methodology in the project management software category. The v0.9 AI Presence rates input for all three categories is the matched-subset measurement deposited in *AI Presence Drift: A Longitudinal Re-Baseline of Five Brand Categories* ([SSRN ID 6736878](https://ssrn.com/abstract=6736878)). Methodological reference: *AIAS Presence Measurement Protocol v1.1* ([SSRN ID 6722319](https://ssrn.com/abstract=6722319)). Cross-references the foundational theoretical paper *AI Availability: Extending Mental and Physical Availability into Algorithmic Retrieval* ([SSRN ID 6659000](https://ssrn.com/abstract=6659000)). Prior empirical papers in the programme: cross-category baseline ([SSRN ID 6720959](https://ssrn.com/abstract=6720959)); phantom-brand persistence designed-for-test ([SSRN ID 6721779](https://ssrn.com/abstract=6721779)); discourse-language bias designed-for-test ([SSRN ID 6728000](https://ssrn.com/abstract=6728000)); naive-phantom rate longitudinal stability ([SSRN ID 6741163](https://ssrn.com/abstract=6741163)). Pre-registration document (PRE_REGISTRATION.md, locked at git commit ae4bd3a, tag *v0.12-prereg*) and underlying datasets released alongside this paper at <https://osf.io/ec6wh/>.

\newpage

## 1. Introduction

The v0.11 construct-validity pilot established that AI Presence, the LLM-side measurement of brand visibility in AI-generated category recommendations developed across versions v0.6 through v0.10 of the AIAS programme, is correlated with but distinct from Google Trends search interest in a single category (project management software) at moderate strength (Spearman ρ ≈ 0.49 across two waves), stably across a seven-day longitudinal interval (|Δρ| = 0.020), with the leadership zone of the AI Presence distribution diverging from the leadership zone of the Trends distribution at both waves (González Castro 2026i). The substantive interpretation developed in v0.11 was that AI applies a tighter and partly-different category boundary than consumer search does, anchored by two diagnostic cases — the Linear paradox (high AI Presence with negligible Trends signal) and the Todoist inverse (moderate Trends signal with near-zero AI Presence).

v0.12 is the cross-category expansion the v0.11 paper preannounced (González Castro 2026i, §7). It extends the construct-validity test from one category to three: PM software (replication test of v0.11), premium running shoes (a new high-volume B2C category structurally different from B2B SaaS), and premium olive oil (a new premium consumer packaged goods category structurally different from both). The three-category design serves two purposes simultaneously. It tests whether the v0.11 category-boundary mismatch reproduces under independent acquisition seven days later in the same category (test-retest validity), and it tests whether the boundary-mismatch mechanism generalises across categories with structurally different consumer search and AI recommendation patterns (cross-category generalisation).

Two new pre-registered hypotheses operationalise the cross-category generalisation question. H5 specifies cross-category generalisation of the v0.11 signature: ρ < 0.5 with *p* < 0.05 AND H3 falsified at both waves, in 2 of 3 evaluable categories. H6 specifies cross-category replication of the v0.11 diagnostic cases: both Linear-style brands (AI Presence ≥ 50 percent AND Trends ≤ 5) and Todoist-style brands (AI Presence ≤ 5 percent AND Trends ≥ 20) surface in 2 of 3 evaluable categories. The design accommodates the realistic possibility that not all three categories yield enough usable Trends signal for confirmatory inference by introducing a routing rule (pre-reg §3.4a): categories with fewer than 10 brands clearing the at-acquisition eligibility filter (E1b) at either wave route to a descriptive-only arm; categories with at least 10 brands route to the confirmatory arm. The cross-category hypotheses become 2-of-2 effective if exactly one of the three categories routes descriptive.

A pre-registered Category-Scale Mismatch Finding (pre-reg §10.2) operationalises the descriptive-only arm. For descriptive-route categories, the paper reports the proportion of matched-subset brands with AI Presence rates above a threshold (5 percent) and Trends signal below the platform's display threshold, alongside a per-brand table with each matched-subset brand's AI Presence and Phase B Trends acquisition disposition. The Category-Scale Mismatch Finding does not provide confirmatory inference on H1–H4 in the descriptive category, but it provides directly relevant evidence for the theoretical claim that AI Availability and Mental Availability are empirically separable constructs.

Category selection followed three criteria. PM software is retained as the replication category. Running shoes was selected as the second category for its structural contrast with PM software: high consumer search volume, mostly English-language discourse, well-known incumbents with long brand histories alongside DTC challengers, and a mix of category framings (athletic performance, fashion, casual lifestyle). Premium olive oil was selected as the third category for its structural contrast with both: low individual-brand search volume relative to category-generic search ("extra virgin olive oil"), mostly non-English production origins with English-language discourse, and a known asymmetry where premium artisanal brands often have strong specialist visibility but limited mass-market search interest. The three-category selection deliberately samples three different positions on the cross-cutting dimensions of category volume, B2B vs B2C, and English vs multi-lingual production.

The empirical result is more informative than the pre-registered generalisation prediction would have been. v0.11 replicates in PM software with high precision (within 0.010 of v0.11's ρ values at both waves; H3 falsifies identically at 1 of 3 both waves; H6 confirms with the same diagnostic brands surfacing). Running shoes shows a structurally different regime: bivariate ρ is well above the v0.11 magnitude (ρ ≈ 0.8 vs v0.11's ρ ≈ 0.5) but the partial ρ after age + tier control drops to a magnitude comparable to v0.11's partial ρ (≈ 0.47 vs v0.11's ≈ 0.42), and H6 falsifies asymmetrically (Linear-style brands surface; no Todoist-style brand surfaces). Premium olive oil routes to descriptive-only and reveals a Category-Scale Mismatch: 7 of 15 matched-subset brands have non-trivial AI Presence but Trends signal below display threshold. The cross-category hypotheses H5 and H6 are both falsified, but the falsifications carry distinct substantive content rather than indicating either non-generalisation in the simple sense or measurement failure.

The remainder of the paper is organised as follows. Section 2 describes the pre-registered method, including the three-category design, the routing rule for descriptive vs confirmatory inference, the eight hypothesis specifications, the brand-age and tier covariates, and the pivot-rescaling protocol applied independently per category. Section 3 reports findings per category and across categories: §3.1 PM software replication; §3.2 running shoes; §3.3 premium olive oil descriptive arm and Category-Scale Mismatch Finding; §3.4 cross-category integration (H5 and H6) and pooled sensitivity ρ. Section 4 reports pre-registered hypothesis outcomes in tabular form. Section 5 develops the substantive interpretation: the three-empirical-regimes framing, the persistence of category-boundary mismatch across regimes, and the implications for the Tri-System Brand Growth framework's separability claim. Section 6 addresses limitations, including the single-acquisition design, small olive oil n, an acquisition-side bundle-padding methodology lesson logged in DEVIATIONS.md, and the open question of practical predictive validity for purchase behaviour. Section 7 outlines v0.13 expansion work.

![Cross-category H1 scatter at t₁. Three panels showing per-category AI Presence × Google Trends rescaled mean (log-scale; pivot ≡ 100). PM software (left) replicates v0.11's marginal correlation with bidirectional boundary mismatch; running shoes (centre) shows strong correlation with age-mediated structure; premium olive oil (right) shows scale mismatch with E1a-excluded brands plotted at the "below display threshold" band with × markers.](../figures/chart_v12_h1_cross_category_scatter_t1.pdf){width=100%}

## 2. Method

The measurement followed the AIAS Presence Measurement Protocol v1.1 (González Castro 2026b), unchanged from v0.9 through v0.11. The pivot-rescaling protocol developed in v0.11 (González Castro 2026i, §2.4) is applied independently per category. The brand registries are frozen at v0.6's final state and unchanged across v0.7 through v0.12.

### 2.1 Pre-registration

A pre-registration document (PRE_REGISTRATION.md, fourteen sections) was committed and tagged at git commit ae4bd3a (tag *v0.12-prereg*) prior to any Google Trends acquisition call against the wave windows. The pre-registration specifies the wave window dates (t₁ = 27 April – 3 May 2026; t₂ = 4 – 10 May 2026, Monday-to-Sunday calendar weeks), the three per-category pivot brands (Asana /m/0c3z_p8 for PM software; California Olive Ranch /g/11cn92g97s for olive oil; Asics /m/04xxy1 for running shoes — each validated for stability against the out-of-sample window prior to lock per pre-reg §6.A), the matched-subset brand definitions per category, the eight hypothesis specifications with numerical thresholds, the n-floor (hard 10; alignment 12) and routing rules, the at-acquisition exclusion rules E1a (pre-acquisition validation failure) and E1b (rescaled mean = 0 OR rescaled stdev = 0), and the canonical scoring procedure. Six per-category and two cross-category hypotheses plus pre-registered sensitivity analyses (US-only region; Pearson statistic; raw-strict E1b for running) were locked at the same commit.

The both-waves conjunction in H1 and H4 provides built-in family-wise error rate control: under the null, joint probability ≈ 0.05² = 0.0025, more stringent than the conventional 0.05 family-wise rate. The pre-registration also locks Phase A pivot validation and Phase B brand-by-brand acquisition query resolution: California Olive Ranch passed Phase A at mean 83.5 (CV 12.4 percent) and Asics passed at mean 84.5 (CV 7.9 percent) against the out-of-sample window prior to acquisition.

### 2.2 Categories and matched subsets

Three categories with 17–19 brands each in the v0.6 registry. After pre-acquisition E1a validation, eight brands were excluded across the three categories (one PM software brand — Shortcut — inherited from v0.11; seven olive oil brands — Colonna, Frescobaldi Laudemio, Lucini, Manni, McEvoy Ranch, Núñez de Prado, Olio Verde — which failed solo Phase B validation by returning the platform message "Google Trends hasn't returned any results for this query" against the out-of-sample window and failed bundled-validation E5 rescue). The PM software analysis subset is 18 brands. The olive oil analysis subset is 15 matched-subset brands of which 8 cleared Phase B (the 7 E1a-excluded brands are retained in the Category-Scale Mismatch table as "below display threshold" descriptive evidence; pre-reg §10.2). The running shoes analysis subset is 13 brands; all 13 cleared Phase B.

### 2.3 AI Presence input

The AI Presence rates at t₁ and t₂ are taken directly from the v0.9 matched-subset measurement (González Castro 2026f), filtered to the two-model matched subset (Claude Sonnet 4.6 + GPT-5.4-mini, response status = ok). The matched subset definitions are reproduced from the v0.9 publication unchanged. The v0.9 collection produced AI Presence rates at two waves seven days apart (t₁ at the original v0.6 baseline collection date; t₂ at the v0.9 re-baseline collection date). The v0.12 design uses these as the AI Presence inputs to the construct-validity test rather than collecting a fresh AI Presence measurement, holding the AI Presence measurement constant while running the Trends acquisition under v0.12 wave windows.

### 2.4 Google Trends acquisition

The Trends acquisition was executed at a single locked timestamp (2026-05-11T10:33:22Z) covering 14 days × 10 bundles × 2 regions = 280 (brand, day) cells. Bundle composition per category: PM software (5 bundles); olive oil (2 bundles, the second padded with the generic term "extra virgin olive oil" to fill the fifth bundle slot — this padding choice produced quantization noise in the second olive oil bundle and is documented in DEVIATIONS.md Entry 1); running shoes (3 bundles). Each bundle is a 5-term query containing the category pivot in the first slot and four non-pivot category members (or padding) in the remaining slots; pivot-rescaling per §5.1 converts each non-pivot brand's bundle-relative 0–100 daily value to a pivot-normalised daily value (rescaled = raw\textsubscript{brand}(d) / raw\textsubscript{pivot}(d) × 100). The pivot is fixed at 100 every day by construction (eligibility-flag pivot exemption per §5.1 applies at scoring).

### 2.5 Eligibility, routing, and hypothesis design

Brands clearing both E1a (pre-acquisition) and E1b (at-acquisition) checks at a given wave are eligible for that wave's confirmatory analysis. The pivot is always eligible by construction (§5.1). The n-floor is hard at 10 brands per category per wave (descriptive routing below; confirmatory at or above) with an alignment threshold of 12 (full hypothesis evaluation). Categories routing to confirmatory carry H1 (cross-sectional construct validity, Spearman ρ > 0.5 AND *p* < 0.05 at both waves), H2 (cross-wave stability, |Δρ| ≤ 0.15), H3 (leaderboard directional consistency, AI top-3 ⊆ Trends top-5 at both waves), and H4 (covariate-controlled construct validity, partial ρ on rank residuals after age + tier control > 0.5 AND *p* < 0.05 at both waves). Categories routing to descriptive carry only the Category-Scale Mismatch reporting (§10.2). Two cross-category hypotheses span all confirmatory-route categories: H5 (v0.11 signature generalisation, defined as ρ < 0.5 AND *p* < 0.05 AND H3 falsified at both waves, in 2 of 3 categories — effective 2-of-2 if one category routes descriptive); H6 (Linear-style + Todoist-style detection at both waves, in 2 of 3 — same effective rule).

Pre-registered sensitivity analyses: H1 evaluated on US-only Trends region; H1 evaluated with Pearson statistic instead of Spearman; for running specifically, H1 evaluated under raw-strict E1b (excluding the floor-constant brands whose raw Trends value is invariant across days even though the pivot-rescaled stdev > 0 — a category-specific concern noted in pre-reg §3.4b).

### 2.6 Covariates and brand age

Brand-age data follow the brand-as-marketed founding-year convention (pre-reg §6.B): the year the consumer-facing brand-as-marketed entity began trading under its current brand identity, regardless of subsequent ownership transfers. This convention was applied uniformly across the three categories. Specific cases requiring the rule: Castillo de Canena (olive oil, founded 2003); Asics (running shoes, founded 1977); Nike (1971); Núñez de Prado (1986). Tier (incumbent / mid-tier / challenger) is taken directly from the v0.6 registry, ordinal-coded for the partial-correlation analysis.

\newpage

## 3. Results

### 3.1 PM software replicates v0.11 with high precision.

The v0.11 PM software finding reproduces under independent Google Trends acquisition seven days after the v0.11 locked acquisition. Spearman ρ at t₁ = 0.506 (Worldwide; *p*\textsubscript{1t} = 0.019), and at t₂ = 0.482 (*p*\textsubscript{1t} = 0.022). Both values are within 0.010 of v0.11's reported ρ\textsubscript{t1} = 0.496 and ρ\textsubscript{t2} = 0.476. **H1 falsifies at the magnitude threshold at t₂** (ρ = 0.482 < 0.5) and confirms it narrowly at t₁ (ρ = 0.506 > 0.5 by 0.006). The both-waves conjunction requires both to clear, so H1 is falsified overall. The replication is most informative when read against the v0.11 magnitude: the test correctly identifies that the PM software construct-validity relationship is at the marginal boundary near ρ = 0.5, with the wave-to-wave direction of the miss not reproducing (v0.11 missed at t₁ by 0.004; v0.12 misses at t₂ by 0.018) but the overall magnitude pattern reproducing within sampling error.

**H2 is confirmed** with |Δρ| = 0.024 (against the 0.15 pre-registered tolerance). The cross-wave stability is itself stable across versions: v0.11 reported |Δρ| = 0.020, v0.12 reports |Δρ| = 0.024 — almost identical reproducibility. **H3 is falsified at both waves at exactly 1 of 3**, identical to v0.11's pattern at both waves: at t₁ the AI top-three (Linear, Asana, Notion) contains one brand (Notion) in the Trends top-five; at t₂ the AI top-three (Linear, Asana, Jira) contains one brand (Jira). **H4 falsifies** with partial Spearman ρ at t₁ = 0.417 and at t₂ = 0.434 — both below the 0.5 magnitude threshold. The v0.11 paper reported partial ρ at t₁ = 0.407 and at t₂ = 0.428; the cross-version difference is within 0.01 at both waves.

![PM software rank-shift slope at t₁. Lines connect each brand's rank by AI Presence (left) to its rank by Trends (right). Steep slopes indicate construct divergence. The Linear and Todoist diagnostic cases (extreme |Δrank|) bracket the leadership-zone divergence from opposite ends, replicating v0.11's pattern.](../figures/chart_v12_h3_rank_shift_pmsoftware_t1.pdf){width=100%}

**H6 diagnostic-case detection in PM software confirms.** At t₁, Linear is the unique Linear-style brand (AI Presence 86.5 percent, Trends rescaled 1.88) and Todoist is the unique Todoist-style brand (AI Presence 1.04 percent, Trends rescaled 28). At t₂, Linear remains Linear-style; the Todoist-style category contains Todoist and Basecamp (the latter at AI Presence 2.08 percent, Trends rescaled 22.25). The v0.11 diagnostic cases reproduce in v0.12 PM software as the same brands with the same structural positions.

The PM software replication establishes test-retest validity at the category level: the v0.11 measurement is not a single-collection artefact. The construct-validity correlation between AI Presence and Google Trends search interest in PM software is structurally near ρ ≈ 0.5, reproducibly so across versions, with the leadership-zone divergence concentrated in Linear (high AI, low Trends) and Todoist (low AI, moderate Trends) as the same diagnostic cases.

### 3.2 Premium running shoes shows a structurally different regime.

The pre-registered H5 prediction was that the v0.11 signature would generalise to running shoes: ρ < 0.5 with the leadership-zone divergence persisting. The actual running shoes result is **structurally different from the prediction at both the magnitude bar and the diagnostic-case bar**. Spearman ρ at t₁ = 0.808 (Worldwide; *p*\textsubscript{1t} = 0.0007); at t₂ = 0.786 (*p*\textsubscript{1t} = 0.0012). Both values are well above the moderate-to-strong threshold of 0.5 — by approximately 0.3 magnitude. **H1 confirms** decisively in running shoes; the test is not in tension with the data and the magnitude is well outside the v0.11 magnitude band. **H2 confirms** at |Δρ| = 0.022, within the cross-wave stability range observed across v0.11 and v0.12 PM software (≈ 0.020–0.024 across three measurements now).

The strong bivariate correlation does not, however, indicate that running shoes show a structurally different mechanism from PM software. **H3 falsifies** in running shoes at 2 of 3 at both waves: at t₁ the AI top-three (Asics, Brooks, New Balance) contains two brands in the Trends top-five (Asics and New Balance); Brooks is sixth in Trends despite being top-three in AI Presence. At t₂ the AI top-three (Asics, Brooks, Hoka) contains two in the Trends top-five (Asics and Hoka); Brooks again falls outside. **H4 falsifies** by a substantial margin: partial Spearman ρ at t₁ = 0.466 and at t₂ = 0.488 — both below the 0.5 magnitude threshold, with one-tailed *p* = 0.087 at t₁ and *p* = 0.076 at t₂ also missing the significance bar.

The partial-correlation result quantifies the structural reading of running shoes. Brand age and tier together mediate approximately 40 percent of the bivariate H1 correlation (bivariate ρ ≈ 0.80 → partial ρ ≈ 0.47, a decrement of approximately 0.34; the corresponding decrement in v0.11 PM software was 0.09 at t₁ and 0.05 at t₂). The strongest bivariate signal in running shoes is driven by older incumbents (Asics, Nike, Adidas, New Balance, Brooks) showing high AI Presence and high Trends signal jointly, with brand age as the structural confound. Once age + tier is controlled, the residual AI-to-Trends correlation in running shoes is comparable in magnitude to v0.11's partial ρ in PM software.

![Running shoes partial-correlation residual scatter at t₁. Rank residuals after OLS on rank-transformed brand age and tier ordinal. Bivariate ρ = 0.808 → partial ρ = 0.466 — age + tier mediates approximately 40 percent of the bivariate signal. The residual correlation is comparable to v0.11 PM software's partial correlation, suggesting the direct AI-to-Trends construct-validity relationship is structurally similar across the two categories once the age-of-brand confound is removed.](../figures/chart_v12_h4_partial_residual_running_t1.pdf){width=100%}

**H6 diagnostic-case detection falsifies asymmetrically in running shoes.** Linear-style brands surface at both waves: Brooks at t₁ (AI Presence 56 percent, Trends rescaled 4.69) and Hoka at t₂ (AI Presence 51 percent, Trends rescaled 3.23). No Todoist-style brand surfaces in either wave — no running brand combines AI Presence below 5 percent with Trends rescaled above 20. The pattern is consistent with a single-directional category-boundary effect in running shoes: AI does over-recommend certain brands relative to consumer search (Brooks, Hoka — both performance-running incumbents with strong narratives in athletic discourse), but the inverse pattern (brands well-known to consumers but absent from AI recommendations) does not surface in this category.

Two pre-registered sensitivities qualify the running shoes finding. The US-only sensitivity confirms H1 across both waves (US ρ\textsubscript{t1} = 0.779, ρ\textsubscript{t2} = 0.526; both clear *p* < 0.05). The Pearson sensitivity falsifies (Pearson r\textsubscript{t1} = 0.483, r\textsubscript{t2} = 0.491), indicating that the Spearman-Pearson divergence in running shoes reflects a rank-monotonic but non-linear relationship between the two systems (Asics anchors at 100 by construction; other brands cluster at low rescaled values). The raw-strict E1b sensitivity (excluding the five running brands whose raw Trends value is constant 1 across the window: Altra, Norda, On, Salomon, Topo Athletic) is indeterminate (n = 7 at both waves, below the hard floor of 10) — the raw-strict subset retains the seven robustly-differentiated running brands (Asics + Adidas + Brooks + Hoka + Nike + New Balance + Puma) and is too small for confirmatory inference under v0.12's n-floor rule.

The substantive reading of running shoes is that it occupies a different empirical regime from v0.11 PM software despite sharing the boundary-mismatch mechanism. The bivariate AI-to-Trends correlation is strong, the magnitude is well above the v0.11 signature, but the direct construct-validity relationship after age and tier control is comparable to PM software's, and the boundary mismatch persists in the leadership zone (H3 falsified) and in the diagnostic-case detection (H6 asymmetric — Linear-style present, Todoist-style absent). The category's mechanism is not "no boundary mismatch" but "asymmetric boundary mismatch with age-driven bivariate covariance."

### 3.3 Premium olive oil reveals a Category-Scale Mismatch.

The premium olive oil category routes to descriptive-only at both regions per pre-reg §3.4a: n = 8 at Worldwide and n = 7 at US, both below the hard floor of 10. The Spearman ρ across the 8 PASS subset at Worldwide is 0.168 at t₁ and −0.095 at t₂; the US 7-subset is 0.036 at t₁ and −0.357 at t₂. The bivariate correlation is essentially zero or weakly negative — informative on its own as evidence that the PASS subset of olive oil brands does not show the construct-validity correlation observed in PM software or running shoes, but small-n constraints prevent confirmatory inference.

The substantive olive oil finding is the **Category-Scale Mismatch** documented per pre-reg §10.2 in the matched-subset table reproduced as Figure 4: 7 of 15 matched-subset olive oil brands (46.7 percent) have AI Presence rates of at least 5 percent at either wave but Trends signal below the platform's display threshold (returning the message "Google Trends hasn't returned any results for this query" at solo Phase B validation against the out-of-sample window). The seven scale-mismatch brands are Frescobaldi Laudemio (AI Presence 22 percent at both waves; Trends below threshold), Olio Verde (16–22 percent; below threshold), Lucini (17–19 percent; below threshold), McEvoy Ranch (5–9 percent; below threshold), Manni (3–5 percent; below threshold), Colonna (4–5 percent; below threshold), and Núñez de Prado (4–5 percent; below threshold).

![Premium olive oil Category-Scale Mismatch matched-subset bar visualisation. Horizontal bars showing per-brand AI Presence at t₁ (longer bar = higher AI Presence); green circles indicate brands with measurable Trends signal at t₁ (PASS or PASS\_E5); copper × indicates brands with Trends signal below the platform's display threshold (EXCLUDED\_E1a). The seven scale-mismatch cases (AI Presence ≥ 5 percent AND Trends below display threshold) are flagged with ▶. Scale-mismatch index: 7 / 15 = 46.7 percent of the matched subset.](../figures/chart_v12_scale_mismatch_olive_oil.pdf){width=100%}

The Category-Scale Mismatch is the strongest possible evidence for the empirical separability of AI Availability and Mental Availability in this category. The two constructs cannot be placed on the same scale at all for nearly half of the matched-subset brands: AI systems treat these brands as having meaningful presence in the premium olive oil category (returning them by name in 5–22 percent of category-recommendation responses across the two-model matched subset at both waves), while Google's consumer-search measurement infrastructure returns no signal at the platform's display threshold for the same brand names at the same wave windows. The non-trivial AI Presence rates are not measurement noise — they are stable across waves and consistent across the two models in the matched subset.

The mechanism candidate for the Category-Scale Mismatch is asymmetric specialist-vs-mass surface area. Premium artisanal olive oil brands have strong presence in food-publication discourse, restaurant recommendations, gift-guide listings, and direct-to-consumer marketing channels that LLM training data captures, but limited mass-market consumer-search interest under brand-name queries because the typical consumer of premium olive oil discovers brands through curation rather than direct search. The asymmetry is structurally different from the v0.11 boundary mismatch — which was about category framing (Linear inside AI's PM-software but barely inside consumers') — and from running shoes' age-mediated structure. It is about the relative size of the specialist-recommendation surface versus the mass-search surface for the same brand.

### 3.4 Cross-category integration: H5 and H6 both falsify.

**H5 (v0.11 signature generalisation across confirmatory-route categories) falsifies at 0 of 2 applicable categories.** PM software does not meet the full v0.11 signature definition at v0.12 because ρ\textsubscript{t1} = 0.506 just clears the 0.5 threshold (failing the "ρ < 0.5" component); running shoes is substantially above 0.5 throughout. The H5 falsification is asymmetric in substantive content: PM fails by 0.006 (within sampling error of the v0.11 signature), while running shoes fails by 0.3 (a different empirical regime). The two falsifications are different kinds.

**H6 (cross-category diagnostic-case detection) falsifies at 1 of 2 applicable categories.** PM software confirms H6a (Linear-style and Todoist-style brands both surface at both waves). Running shoes falsifies H6a (Linear-style brands surface — Brooks at t₁, Hoka at t₂ — but no Todoist-style brand surfaces in either wave). The 2-of-2 effective rule (with olive oil routed descriptive) requires both PM and running to confirm; the H6 cross-category result is FALSIFIED.

![Cross-category H6 diagnostic zones at t₁. Linear-style region (top-left: AI Presence ≥ 50 percent AND Trends ≤ 5) and Todoist-style region (bottom-right: AI Presence ≤ 5 percent AND Trends ≥ 20) shaded in copper. PM software (left) shows Linear and Todoist as the diagnostic cases in their respective zones, replicating v0.11. Running shoes (right) shows Brooks in the Linear-style zone but no brand in the Todoist-style zone — the asymmetric boundary mismatch.](../figures/chart_v12_h6_zones_t1.pdf){width=100%}

A pre-registered pooled sensitivity ρ stacking rank-within-category data across PM and running (olive oil excluded for descriptive routing) yields ρ = 0.624 at t₁ (n = 29, *p* = 0.0003) and ρ = 0.580 at t₂ (n = 30, *p* = 0.0008). The pooled correlation is stronger than v0.11's per-category ρ ≈ 0.5 — driven largely by running shoes' strong bivariate signal — and confirms that within-category brand-ranking by AI Presence is positively associated with within-category brand-ranking by Trends across both confirmatory categories.

The combined cross-category result is that the v0.11 single-category finding does not generalise in the simple sense (H5 / H6 falsified) but the substantive content of the falsifications is theoretically constructive: PM software replicates v0.11 with near-identical magnitudes, running shoes shows a different magnitude regime with similar boundary-mismatch structure, and olive oil shows a third regime where the constructs cannot be placed on the same scale at all. The three regimes are the discussion's organising frame.

\newpage

## 4. Pre-Registration Outcomes

The eight pre-registered hypotheses plus pre-registered sensitivities are reported in Table 1.

*Table 1. v0.12 cross-category construct-validity expansion pre-registration outcomes.*

\begin{table}[H]
\centering
\small
\begin{tabular}{@{}p{0.06\textwidth}p{0.12\textwidth}p{0.22\textwidth}p{0.13\textwidth}p{0.27\textwidth}p{0.12\textwidth}@{}}
\toprule
\textbf{Hyp.} & \textbf{Cat.} & \textbf{Claim} & \textbf{Threshold} & \textbf{Outcome} & \textbf{Band} \\
\midrule
H1 & PM software & Cross-sectional ρ (Worldwide) & $\rho > 0.5$ AND $p_{1t} < 0.05$ both waves & $\rho_{t1}$ = 0.506 ($p$ = 0.019); $\rho_{t2}$ = 0.482 ($p$ = 0.022) & \textbf{FALSIFIED} \\
\addlinespace
H2 & PM software & Cross-wave stability & $|\Delta\rho| \leq 0.15$ & $|\Delta\rho|$ = 0.024 & \textbf{CONFIRMED} \\
\addlinespace
H3 & PM software & AI top-3 $\subseteq$ Trends top-5 both waves & — & 1 of 3 at $t_1$; 1 of 3 at $t_2$ & \textbf{FALSIFIED} \\
\addlinespace
H4 & PM software & Partial $\rho$ (age + tier) both waves & $\rho > 0.5$ AND $p_{1t} < 0.05$ both waves & partial $\rho_{t1}$ = 0.417 ($p$ = 0.061); partial $\rho_{t2}$ = 0.434 ($p$ = 0.046) & \textbf{FALSIFIED} \\
\addlinespace
H1 & Running & Cross-sectional ρ (Worldwide) & $\rho > 0.5$ AND $p_{1t} < 0.05$ both waves & $\rho_{t1}$ = 0.808 ($p$ < 0.001); $\rho_{t2}$ = 0.786 ($p$ = 0.001) & \textbf{CONFIRMED} \\
\addlinespace
H2 & Running & Cross-wave stability & $|\Delta\rho| \leq 0.15$ & $|\Delta\rho|$ = 0.022 & \textbf{CONFIRMED} \\
\addlinespace
H3 & Running & AI top-3 $\subseteq$ Trends top-5 both waves & — & 2 of 3 at $t_1$; 2 of 3 at $t_2$ & \textbf{FALSIFIED} \\
\addlinespace
H4 & Running & Partial $\rho$ (age + tier) both waves & $\rho > 0.5$ AND $p_{1t} < 0.05$ both waves & partial $\rho_{t1}$ = 0.466 ($p$ = 0.087); partial $\rho_{t2}$ = 0.488 ($p$ = 0.076) & \textbf{FALSIFIED} \\
\addlinespace
H1–H4 & Olive oil & — & n-floor & $n$ = 8 (WW), $n$ = 7 (US); below hard floor 10 & \textit{Descriptive-only per §3.4a} \\
\addlinespace
\multicolumn{3}{l}{\textbf{Category-Scale Mismatch index (olive oil, §10.2)}} & 7 / 15 = 46.7\% & 7 brands AI $\geq$ 5\% AND Trends below display threshold & \textit{Descriptive finding} \\
\addlinespace
H5 & Cross-cat. & v0.11 signature in 2 of 2 applicable cats & — & 0 of 2 show v0.11 signature & \textbf{FALSIFIED} \\
\addlinespace
H6 & Cross-cat. & Linear-style + Todoist-style in 2 of 2 applicable cats & — & 1 of 2 (PM confirms; running lacks Todoist-style) & \textbf{FALSIFIED} \\
\addlinespace
\multicolumn{6}{c}{\textit{Sensitivities (per pre-reg §6 step 11)}} \\
\addlinespace
H1$_{US}$ & PM software & US-only & $\rho > 0.5$ AND $p < 0.05$ both waves & $\rho_{t1}$ = 0.482; $\rho_{t2}$ = 0.417 & \textit{Falsified} \\
\addlinespace
H1$_r$ & PM software & Pearson $r$ & $r > 0.5$ AND $p < 0.05$ both waves & $r_{t1}$ = 0.546; $r_{t2}$ = 0.533 & \textit{Confirmed} \\
\addlinespace
H1$_{US}$ & Running & US-only & $\rho > 0.5$ AND $p < 0.05$ both waves & $\rho_{t1}$ = 0.779; $\rho_{t2}$ = 0.526 & \textit{Confirmed} \\
\addlinespace
H1$_r$ & Running & Pearson $r$ & $r > 0.5$ AND $p < 0.05$ both waves & $r_{t1}$ = 0.483; $r_{t2}$ = 0.491 & \textit{Falsified} \\
\addlinespace
H1$_{raw}$ & Running & Raw-strict E1b & $\rho > 0.5$ AND $p < 0.05$ both waves & $n_{t1}$ = $n_{t2}$ = 7 (below floor) & \textit{Indeterminate} \\
\addlinespace
\multicolumn{6}{l}{Pooled rank-within-category ρ (PM + running): $\rho_{t1}$ = 0.624 ($n$ = 29, $p$ = 0.0003); $\rho_{t2}$ = 0.580 ($n$ = 30, $p$ = 0.0008)} \\
\bottomrule
\end{tabular}
\end{table}

The result set is mixed in a way that is theoretically informative. The cross-category generalisation hypotheses H5 and H6 are both falsified, but the falsifications carry distinct substantive content: H5 falsifies for asymmetric reasons (PM ρ is within sampling error of v0.11's signature; running ρ is in a different magnitude regime); H6 falsifies for asymmetric reasons (PM confirms; running shows only Linear-style without the symmetric Todoist-style brand). Within categories, PM software replicates v0.11 with high precision (within 0.01 ρ at both waves, identical H3 pattern, same diagnostic cases). Running shoes shows a structurally different empirical regime: bivariate ρ near 0.8, age + tier mediates approximately 40 percent, residual partial ρ ≈ 0.47 (comparable to v0.11 PM software's partial ρ ≈ 0.42). Premium olive oil reveals a Category-Scale Mismatch where 7 of 15 matched-subset brands have non-trivial AI Presence but Trends signal below display threshold — the constructs cannot be placed on the same scale at all for nearly half the matched subset.

\newpage

## 5. Discussion: Three Empirical Regimes of AI Availability and Mental Availability

The pre-registered prediction underlying v0.12 was that the v0.11 boundary-mismatch finding would generalise across categories — that AI Presence and Google Trends search interest would correlate at marginal-to-moderate strength (ρ ≈ 0.5) with the H3 leadership-zone divergence persisting and Linear-style and Todoist-style diagnostic cases surfacing in 2 of 3 categories. The pre-registered prediction is falsified at both the H5 magnitude-band level (only 0 of 2 applicable categories meet the full v0.11 signature) and the H6 diagnostic-case level (only 1 of 2 applicable categories show both styles). The falsifications, however, organise into a sharper substantive finding: the empirical relationship between AI Availability and Mental Availability is category-dependent, with three distinct empirical regimes observable in the v0.12 sample. What unifies the regimes is the persistence of category-boundary mismatch across all evaluable categories (H3 falsified in both PM software and running shoes). What differentiates them is magnitude and structure.

### 5.1 Regime 1 — Marginal correlation with bidirectional boundary mismatch (PM software).

The v0.11 finding reproduces at v0.12 PM software with ρ\textsubscript{t1} = 0.506 and ρ\textsubscript{t2} = 0.482 (within 0.010 of v0.11's 0.496 and 0.476 at both waves), |Δρ| = 0.024, H3 at 1 of 3 both waves, partial ρ ≈ 0.42, and Linear and Todoist as the same diagnostic cases. The replication is a load-bearing finding on its own: the v0.11 measurement is not a single-collection artefact, and the methodology underlying the v0.11 pilot now has direct test-retest validity at the category level. The substantive interpretation developed in v0.11 holds at v0.12: AI applies a tighter and partly-different category boundary than consumer search does in PM software, with the divergence bracketed by Linear (high AI, near-zero Trends) at one end and Todoist (low AI, moderate Trends) at the other.

The marginal correlation magnitude is itself substantively meaningful. ρ near 0.5 with H3 decisively falsified at 1 of 3 indicates that the AI-Trends relationship in PM software is sub-categorically structured: AI and consumer search agree on the general ordering of large brands but disagree on which specific brands occupy the top of each system's leadership zone. The agreement is enough to produce a moderate bivariate correlation; the disagreement is enough to drive the H3 falsification. Both findings together describe a relationship that is real, reproducible, and not interchangeable at the level of practical inference.

### 5.2 Regime 2 — Strong age-mediated correlation with asymmetric boundary mismatch (running shoes).

Running shoes shows a structurally different empirical regime from PM software. The bivariate ρ is near 0.8 at both waves — well above the v0.11 magnitude — but the partial ρ after age + tier control drops to approximately 0.47 at both waves (a decrement of approximately 0.34, against PM software's decrement of approximately 0.07). The strong bivariate correlation is substantially driven by older incumbents (Asics, Nike, Adidas, Brooks, New Balance) having jointly high AI Presence and high Trends signal: brand age and tier together explain approximately 40 percent of the bivariate correlation. Once this confound is removed, the residual partial-correlation magnitude in running shoes is comparable to v0.11 / v0.12 PM software's partial-correlation magnitude.

The H3 leaderboard test falsifies at 2 of 3 both waves — Brooks is in the AI top-three at both waves but ranks sixth in Trends. The Linear-style diagnostic surfaces in running shoes (Brooks at t₁, Hoka at t₂ — both performance-running incumbents with strong narratives in athletic discourse that LLM training data captures with high salience), but no Todoist-style brand surfaces: no running brand combines low AI Presence with moderate-to-high Trends signal. The asymmetric H6 result is a substantive finding on its own. Running shoes' boundary mismatch is unidirectional rather than bidirectional: AI over-recommends specific incumbents relative to their consumer-search interest, but does not under-recommend brands well-known in consumer search.

The substantive reading of running shoes is that it occupies an empirical regime where the bivariate correlation is high but largely age-driven, and the residual direct construct-validity relationship is comparable in magnitude to PM software's. The category-boundary mismatch mechanism remains active (H3 falsified, Linear-style diagnostic surfaces) but in asymmetric form. The age-mediation finding is itself theoretically substantive: in categories with long-established incumbents that have accumulated decades of brand-name presence in both training-data corpora and consumer-search histories, brand age is a structural common cause of joint variation in AI Presence and Mental Availability, and any cross-sectional construct-validity test in such categories should be expected to show inflated bivariate correlations relative to the direct AI-to-search-interest relationship.

### 5.3 Regime 3 — Category-Scale Mismatch (premium olive oil).

Premium olive oil routes to descriptive-only per pre-reg §3.4a and reveals a third empirical regime. The Spearman ρ across the 8-brand PASS subset at Worldwide is 0.168 at t₁ and −0.095 at t₂ — essentially zero correlation, with the wave-to-wave drift across the small subset itself uninformative. The substantive olive oil finding is the Category-Scale Mismatch: 7 of 15 matched-subset brands (46.7 percent) have AI Presence rates of at least 5 percent at either wave but Trends signal below the platform's display threshold. The brands cannot be placed on the same scale at all for nearly half of the matched subset.

The Category-Scale Mismatch is the strongest possible evidence for the empirical separability of AI Availability and Mental Availability in this category. The two constructs are not "correlated but distinct" (PM software's framing) or "highly correlated with shared age confound" (running shoes' framing). The two constructs are operating on different scales entirely: AI systems treat seven matched-subset olive oil brands as having meaningful category presence (returning them by name in 5–22 percent of category-recommendation responses across the two-model matched subset at both waves), while Google's consumer-search measurement infrastructure returns no signal at the platform's display threshold for the same brand names at the same wave windows. The non-trivial AI Presence rates are stable across waves and consistent across the two models in the matched subset — they are not measurement noise.

The mechanism candidate is asymmetric specialist-vs-mass surface area. Premium artisanal olive oil brands have strong presence in food-publication discourse, restaurant recommendations, gift-guide listings, sommelier-style curation, and direct-to-consumer marketing channels that LLM training data captures, but limited mass-market consumer-search interest under brand-name queries because the typical consumer of premium olive oil discovers brands through curation rather than direct search. The asymmetry is structurally different from the boundary mismatches in PM software (about category framing) and running shoes (about age-driven joint visibility); it is about the relative size of the specialist-recommendation surface versus the mass-search surface.

### 5.4 What unifies the three regimes and what differentiates them.

The three regimes share one mechanism and differ on two dimensions. The shared mechanism is category-boundary mismatch: AI's category boundary is structurally different from consumer search's in all three categories. In PM software the mismatch is bidirectional (Linear inside AI but barely inside consumers'; Todoist outside AI but well inside consumers'). In running shoes the mismatch is unidirectional (Brooks and Hoka inside AI's leadership but lower in Trends rankings; no symmetric brand absent from AI but well-known in search). In olive oil the mismatch is scale-level (seven matched-subset brands inside AI's category but absent from consumer-search detection entirely).

The two differentiating dimensions are magnitude of bivariate correlation and structural source of correlation. The bivariate ρ ranges from near-zero in olive oil's PASS subset to marginal in PM software (≈ 0.5) to strong in running shoes (≈ 0.8). The structural source ranges from direct construct relation (PM software, where partial ρ ≈ 0.42 is comparable in magnitude to bivariate ρ) to age-mediated joint variation (running shoes, where bivariate ρ ≈ 0.8 drops to partial ρ ≈ 0.47) to scale incommensurability (olive oil, where Trends signal is absent for nearly half the matched subset).

The substantive contribution of v0.12 is the identification of these three regimes as distinct empirical manifestations of the same theoretical separability claim. The Tri-System Brand Growth framework's central claim is that AI Availability is empirically separable from Mental Availability — not equivalent at the level of practical inference (González Castro 2026a). v0.11 supported this claim through a single-category boundary-mismatch finding. v0.12 supports the same claim more broadly: AI Availability is separable from Mental Availability in three distinct empirical ways across three structurally different categories. The framework's separability claim does not require a uniform mechanism of separation across categories; it requires that separability obtain, and v0.12 demonstrates that it does, with the structural form of the separation varying with category characteristics.

### 5.5 Implications for the AI Availability construct.

The three-regime finding has three implications for the AI Availability construct as it is operationalised in the AIAS programme. First, no single external validator (consumer search interest, or any other single behavioural proxy) is likely to produce a clean moderate-to-strong correlation with AI Presence across all categories: the relationship is category-dependent in both magnitude and structure. Construct validity for AI Presence must therefore be established through the kind of multi-category pattern this paper documents, rather than through any single high-power within-category test. Second, brand age and tier are non-trivial covariates that should be reported alongside any cross-sectional AI-Presence-to-external-validator correlation in categories with long-established incumbents: the partial correlation is the more interpretable statistic in such categories. Third, the Category-Scale Mismatch regime is operationally consequential: in categories where the validator's display threshold excludes a substantial portion of brands that are present in AI recommendations, the cross-sectional correlation is structurally unable to capture the construct's full operational structure, and a different empirical strategy (descriptive Scale-Mismatch reporting, or a different validator selection) is required.

The three implications converge on a single methodological recommendation for the AIAS programme's Phase 3 expansion: each category requires its own routing decision (confirmatory vs descriptive) based on pre-acquisition Phase B validation, and the cross-category integration (H5 / H6 effective thresholds) must be specified in advance with the routing distribution in mind. The v0.12 pre-registration implemented this rule (§3.4a), and the v0.12 result demonstrates that the rule is both operationally workable and theoretically necessary.

\newpage

## 6. Limitations

**Single-acquisition design.** The v0.12 Trends acquisition was executed at a single locked timestamp covering both waves. The replication evidence for v0.11 PM software is therefore between-version (v0.11 collection 10 May 2026; v0.12 collection 11 May 2026, one day apart) rather than within-version. A future v0.13 design with multiple independent acquisitions within the same pre-registered category would strengthen the test-retest validity claim at the methodology level.

**Small olive oil n.** The olive oil descriptive-only route is methodologically defensible per pre-reg §3.4a, but the n = 8 PASS subset is below the threshold for any meaningful correlation inference, and the Category-Scale Mismatch index (7 / 15 = 46.7 percent) is computed against a small matched subset. The substantive interpretation of olive oil rests on the absolute fact of scale mismatch — that 7 brands have AI Presence ≥ 5 percent with Trends below display threshold — rather than on any precise quantitative claim about the magnitude of the mismatch. A larger olive oil registry (50+ brands, ideally spanning the full premium-to-mass spectrum) would clarify whether the scale-mismatch index converges to a stable population value or reflects a registry-specific selection.

**Bundle-padding methodology lesson (DEVIATIONS.md Entry 1).** The olive oil Bundle 2 padding term ("extra virgin olive oil") is a generic category-level search query with absolute search volume orders of magnitude higher than any individual brand in the bundle. This swamped the bundle's 0–100 relative-scaling reference at acquisition and produced quantization noise in the pivot-rescaled values for Brightland, Graza, and Kosterina. The DEVIATIONS.md entry documents the methodology lesson for v0.13 design: bundle padding must be brand-volume-comparable, not category-generic. The PM software Bundle 5 used kanban / agile / scrum padding — concept terms in the same volume order as brand searches — which produced no quantization issue. The lesson does not modify any pre-registered hypothesis or routing rule and does not affect the categorical conclusion that olive oil routes to descriptive-only.

**Open question of practical predictive validity for purchase behaviour.** v0.12 establishes construct validity at the category level for AI Presence against Google Trends search interest as the external behavioural validator. The relationship between AI Presence and actual purchase behaviour at the brand level — the question that ultimately matters for the Tri-System Brand Growth framework's practical claims — remains the object of future Phase 3 work. Google Trends search interest is a directionally useful but imperfect proxy for purchase intent, and the category-dependent nature of the AI-Presence-to-Trends relationship documented in this paper suggests that the AI-Presence-to-purchase relationship is likely to be category-dependent as well.

**Single external validator (Google Trends).** v0.12 tests construct validity against one external behavioural validator (Google Trends search interest), as was the v0.11 design. A multi-validator approach — testing AI Presence simultaneously against search interest, social-media mention rates, retail sales data where available, and consumer-survey aided-recall measures — would generalise the construct-validity claim from a single-validator finding to a multi-validator finding. Such a design is beyond the scope of v0.12 but is the medium-term goal of the AIAS programme.

**Category-specific generalisability of the three regimes.** The three regimes documented in this paper are observable in the three v0.12 categories. The substantive claim — that AI Availability and Mental Availability have a category-dependent empirical relationship — is supported by the v0.12 evidence, but a stronger version of the claim (that exactly three regimes exist across the full population of consumer categories) is not established. The v0.13 expansion to five categories (extending to premium facial skincare and personal finance) will test whether additional regimes emerge or whether the v0.12 three-regime taxonomy is comprehensive.

## 7. Future Research

v0.13 expands the construct-validity panel to five categories, adding premium facial skincare and personal finance to the v0.12 three-category set. Personal finance carries the Mint phantom-brand effect documented in v0.7 and v0.10 (González Castro 2026d; 2026g) and is expected on theoretical grounds to show a fourth empirical regime distinct from the three documented here — phantom brands with non-zero AI Presence and exactly zero Trends signal sit at one tail of the construct-validity distribution and may constitute their own regime if multiple phantom cases reproduce. Premium facial skincare is structurally similar to premium olive oil (B2C consumer packaged goods with specialist-vs-mass surface asymmetry) and is expected to test whether the Category-Scale Mismatch regime documented in olive oil reproduces in a structurally adjacent category.

Cross-lingual replication of the v0.12 three-regime finding is the medium-term complement to v0.13. The v0.8 designed-for-test paper documented discourse-language bias in cross-lingual categories (González Castro 2026e); the construct-validity question in cross-lingual categories is whether the AI-Presence-to-Trends correlation depends on the language of the AI query, the language of the Trends acquisition, or both. Premium tea and traditional spirits are pre-identified candidate categories for the cross-lingual construct-validity test (per the v0.12 author's prior pre-registration sequence).

Causal-mechanism studies for the boundary-mismatch finding. v0.12 establishes covariation across three regimes; the next-step question is what specifically about each category produces its regime. The Tri-System Brand Growth framework's Conditional Reweighting and Default Reinforcement laws (González Castro 2026a, §6) specify falsification conditions for causal claims; the v0.12 result identifies brand age, category-discourse surface asymmetry, and category-framing tightness as candidate mechanisms in the three regimes documented here. Mechanism studies operationalising those candidates are the medium-term research path.

AIAS Phase 4 — components 2 through 6. v0.11 through v0.13 establish construct validity for the Presence component of the full AIAS framework. The remaining five components — Ranking, Consistency, Coverage, Grounding, Sentiment — operationalise in Phase 4 and will require their own construct-validity tests against component-appropriate validators. The v0.12 three-regime finding suggests that the construct-validity bar for each AIAS component is unlikely to be a clean uniform correlation with any single external proxy across all categories; the Phase 4 design will need to accommodate the empirical reality that AI-mediated brand presence is category-dependent in both magnitude and structure.

\newpage

## References

González Castro, P. U. (2026a). *Tri-System Brand Growth: The AI Mediation Layer.* Working paper, Third System.

González Castro, P. U. (2026b). *AIAS Presence Measurement Protocol v1.1.* SSRN Working Paper. <https://ssrn.com/abstract=6722319>

González Castro, P. U. (2026c). *AI Presence Measurement Across Consumer Categories: A Cross-Category Baseline of Brand Visibility in Large Language Model Outputs.* SSRN Working Paper. <https://ssrn.com/abstract=6720959>

González Castro, P. U. (2026d). *A Designed-for-Test Measurement of Phantom-Brand Presence in Large Language Model Outputs: Pre-Registered Evidence from Bed Bath & Beyond, with Pier 1 as Structural Comparator.* SSRN Working Paper. <https://ssrn.com/abstract=6721779>

González Castro, P. U. (2026e). *A Designed-for-Test Measurement of Discourse-Language Bias in Large Language Model Brand Recommendations: Pre-Registered Evidence from Premium Kitchen Knives, with Marketing-Language Coverage as the Candidate Mechanism.* SSRN Working Paper. <https://ssrn.com/abstract=6728000>

González Castro, P. U. (2026f). *AI Presence Drift: A Longitudinal Re-Baseline of Five Brand Categories.* SSRN Working Paper. <https://ssrn.com/abstract=6736878>

González Castro, P. U. (2026g). *Naive-Phantom Rate Longitudinal Stability: AI Presence Index v0.10.* SSRN Working Paper. <https://ssrn.com/abstract=6741163>

González Castro, P. U. (2026h). *AI Availability: Extending Mental and Physical Availability into Algorithmic Retrieval.* SSRN Working Paper. <https://ssrn.com/abstract=6659000>

González Castro, P. U. (2026i). *A Construct-Validity Pilot for AI Presence Against External Behavioural Data: Pre-Registered Evidence from 18 Project Management Software Brands at Two Longitudinal Waves Against Google Trends.* SSRN Working Paper. <https://ssrn.com/abstract=6745040>

Nosek, B. A., Ebersole, C. R., DeHaven, A. C., & Mellor, D. T. (2018). The preregistration revolution. *Proceedings of the National Academy of Sciences*, 115(11), 2600–2606.

Romaniuk, J. (2018). *Building Distinctive Brand Assets.* Oxford University Press.

Sharp, B. (2010). *How Brands Grow: What Marketers Don't Know.* Oxford University Press.

Sharp, B., & Romaniuk, J. (2021). *How Brands Grow: Part 2 — Including Emerging Markets, Services, Durables, New and Luxury Brands.* Revised edition. Oxford University Press.

\newpage

## Declarations

### Conflict of Interest

The author serves as Director, Corporate Brand Creative and Governance at Samsung Electronics America. The research presented here is independent of Samsung Electronics America and does not constitute Samsung research. No Samsung Electronics America data, personnel, or commercial interests influenced the design, conduct, analysis, or reporting of this study. Samsung Electronics America did not review the manuscript prior to posting. The brand populations evaluated in this study (project management software, premium running shoes, premium olive oil) do not include Samsung product lines.

### Funding

Self-funded. No external funding sources contributed to this research.

### Data Availability

Underlying datasets, the locked pre-registration document (PRE_REGISTRATION.md, locked at git commit ae4bd3a, tag *v0.12-prereg*, lock date 11 May 2026 UTC prior to any Google Trends acquisition call against the wave windows), the v0.9 AI Presence rates input (matched subset across all three categories), the Google Trends raw responses (twenty pivot-bundle JSON files across two regions covering ten bundles), topic-mid suggestion logs, pre-acquisition validation outputs (solo and bundled E1a checks) against the out-of-sample window, the brand age source table (forty-six rows across three categories), the registry files (frozen at v0.6's final state and unchanged across v0.7 through v0.12), the canonical scoring tables, the Category-Scale Mismatch table, the build-pipeline source code, and the matching brand-format report are deposited in an Open Science Framework project at <https://osf.io/ec6wh/>. The deposit contains row-level CSV outputs throughout; the v0.12 measurement was conducted within a git-tracked repository from methodology lock through publication, and no provenance gaps obtain. DEVIATIONS.md documents the olive oil Bundle 2 padding methodology lesson as a non-design-altering observation. The OSF MANIFEST documents the file inventory, the lineage between raw measurements and derived analyses, and the cryptographic git-commit anchor for the locked pre-registration.

## Author Information

Pablo Ulpiano González Castro is faculty in the MPS Branding Program at the School of Visual Arts, New York, where he teaches Creative Strategy. He maintains Third System™ (research entity; data archive and methodology venue) as the publication venue for the AIAS measurement programme. Correspondence: pablou@pablou.com · pablou.com.
