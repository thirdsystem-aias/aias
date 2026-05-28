---
title: "What AI Presence Does Not Predict"
subtitle: "Amazon Best Sellers Rank as Discriminant Validity Evidence for the AIAS Construct"
author: "Pablo Ulpiano González Castro"
date: "May 2026"
mainfont: "Carlito"
fontsize: 11pt
geometry: margin=1in
linestretch: 1.36
urlcolor: "blue"
linkcolor: "blue"
header-includes:
  - \usepackage{setspace}
  - \usepackage{float}
  - \usepackage{caption}
  - \usepackage{titlesec}
  - \usepackage{booktabs}
  - \setstretch{1.36}
  - \setlength{\parskip}{8pt}
  - \setlength{\parindent}{0pt}
  - \renewcommand{\maketitle}{}
  - \providecommand{\xmpquote}[1]{#1}
  - \captionsetup{font=small,labelfont=bf}
  - \titleformat{\section}{\large\bfseries}{\thesection}{1em}{}
  - \titleformat{\subsection}{\normalsize\bfseries}{\thesubsection}{1em}{}
---

\begin{titlepage}
\setstretch{1.0}
\setlength{\parskip}{0pt}
\centering

\vspace*{1cm}

{\LARGE\bfseries What AI Presence Does Not Predict}

\vspace{0.3cm}

{\large\itshape Amazon Best Sellers Rank as Discriminant Validity Evidence for the AIAS Construct}

\vspace{0.5cm}

Working Paper $\cdot$ Version 26 $\cdot$ Designed-for-Test (Cross-Substrate Construct Validity)

\vspace{1.0cm}

{\large Pablo Ulpiano Gonz\'alez Castro}

\vspace{0.3cm}

School of Visual Arts, MPS Branding Program, New York, NY\\
{\small (primary academic affiliation)}

\vspace{0.2cm}

Third System\texttrademark{} (research entity; data archive and methodology venue)

\vspace{0.2cm}

{\small Correspondence: pablou@pablou.com $\cdot$ pablou.com}\\
{\small ORCID: 0009-0003-8968-9990}

\vspace{1.5cm}

{\small This paper is part of the AIAS\texttrademark{} (AI Availability Score) Measurement Program, a pre-registered study series operationalizing the AI Availability construct introduced in Gonz\'alez Castro (2025). Each phase tests specific hypotheses on a distinct product substrate under a locked measurement protocol. Protocol version: v1.6 (SSRN 6816340). Pre-registration: commit v0.26-prereg-r1, amended r2.}

\vspace{0.5cm}

{\small May 2026}

\end{titlepage}

# Abstract {-}

This study tests whether the AIAS Presence Index ($C_P$) predicts Amazon Best Sellers Rank (BSR) across consumer-goods substrates. Four hypotheses were pre-registered under Protocol v1.6, testing per-substrate Spearman correlations, pooled cross-substrate correlation, Cell A separation, and absent-brand alignment. Three substrates (kitchen knives, audiophile headphones, skincare; N = 64 listed brands) provided within-substrate variance in $C_P$; one substrate (cosmetics; N = 24) exhibited a ceiling effect (all $C_P$ = 6). A fifth substrate (premium kitchenware) was excluded post-registration due to incomplete Phase A data. Results were uniformly null: within-substrate Spearman correlations ranged from -0.116 to +0.049 (all p > 0.65); the pooled correlation across 88 brands was -0.0002 (p = 0.998). All testable hypotheses were falsified. The null result constitutes discriminant validity evidence for the AIAS construct. Combined with convergent validity evidence from v0.25 (Google Trends; $\rho$ = 0.74), the findings support a Campbell-Fiske interpretation: AI Presence captures brand salience within large language model knowledge systems, a dimension that is independent of retail market performance. This distinction is foundational to the Tri-System claim that AI Availability constitutes a third measurable system alongside Mental and Physical Availability.

**Keywords:** AI Availability; AIAS; construct validity; discriminant validity; convergent validity; Amazon Best Sellers Rank; brand presence; large language models; predictive validity; Campbell-Fiske

**JEL Codes:** M31 (primary); L86, L15, D83, M37

**Paper status:** Working paper, designed-for-test. Part of the AIAS Measurement Program (pre-registered study series). Protocol v1.6. Pre-registration commit v0.26-prereg-r1, amended r2.

# 1. Introduction

## 1.1 Construct Validity and the AIAS Program

The AIAS (AI Availability Score) Measurement Program has established the Presence Index ($C_P$) as a reliable measure of brand recognition across large language model knowledge systems (Gonzalez Castro, 2026a). Across eight substrate families and over 180 brands, $C_P$ discriminates between brands that language models recognize and those they do not, with systematic patterns of dissociation, phantom persistence, and identity load moderation (Gonzalez Castro, 2026b).

Measurement reliability, however, is necessary but insufficient for construct validity. A well-specified construct must also demonstrate that it measures what it claims to measure and does not merely proxy for existing constructs. The Campbell and Fiske (1959) multitrait-multimethod framework operationalizes this requirement through two conditions: convergent validity (the measure correlates with theoretically related measures) and discriminant validity (the measure does not correlate with theoretically unrelated measures).

## 1.2 Prior Convergent Evidence

The AIAS v0.25 study (Gonzalez Castro, 2026c) tested convergent validity by correlating $C_P$ with Google Trends search interest across a B2B SaaS substrate. The result was strongly positive ($\rho$ = 0.74, p < 0.001), confirming that AI Presence tracks a related dimension of brand salience. Brands that are well-known in consumer search behavior are also well-recognized by language models, as expected if both measures tap an underlying brand-salience construct.

## 1.3 The Discriminant Validity Gap

Convergent validity alone leaves open the possibility that $C_P$ is simply a noisy proxy for brand popularity, market share, or commercial success. If AI Presence merely reflects how well a brand sells, it would not warrant treatment as a distinct construct in the Tri-System framework (Gonzalez Castro, 2025). Discriminant validity requires demonstrating that $C_P$ does *not* correlate with theoretically distant measures --- specifically, measures of brand commercial performance in retail channels.

Amazon Best Sellers Rank (BSR) provides a natural test. BSR reflects short-term sales velocity within the Amazon marketplace --- a dimension of Physical Availability (ease of purchase) rather than AI Availability (recognition in language model knowledge systems). The two signals originate in fundamentally different data-generating processes: BSR is driven by pricing, distribution logistics, Prime eligibility, and advertising spend; $C_P$ is driven by the breadth of editorial, journalistic, and enthusiast discourse in LLM training corpora.

## 1.4 Study Overview

This study pre-registered four hypotheses testing whether $C_P$ predicts Amazon BSR across five consumer-goods substrates. Post-registration amendments excluded one substrate (premium kitchenware, no $C_P$ data) and reclassified another (cosmetics, ceiling effect). The study tests whether AI Presence has predictive validity for retail sales rank --- with the expectation, informed by the convergent validity results, that it does not.

# 2. Method

## 2.1 Design

Cross-sectional correlational study testing whether AIAS Presence Index scores ($C_P$) predict Amazon Best Sellers Rank across consumer-goods substrates. Pre-registered at commit v0.26-prereg-r1; amended at v0.26-prereg-r2 to reflect substrate exclusions and a C_P retrofit discovered during data integration.

## 2.2 Substrates and Brand Panels

Five substrates were drawn from the AIAS 1.0 base (Gonzalez Castro, 2026b). Post-registration, two exclusions and one retrofit were documented in DEVIATIONS Entry 0.

*Testable substrates (within-substrate correlation):*

Kitchen knives (v0.16): 26 brands. $C_P$ retrofitted under the v1.4+ protocol because v0.16 originally ran under v1.2 methodology, which did not produce per-model integer $C_P$ scores. The retrofit comprised 156 Recognition probes (26 brands $\times$ 6 panel models) using the canonical v0.19+ probe template.

Audiophile headphones (v0.19): 16 brands. $C_P$ derived from existing Phase A results by summing recognition responses across the 6-model panel.

Skincare (v0.20): 24 brands. $C_P$ from canonical verdicts.

*Ceiling substrate (pooled analysis only):*

Cosmetics (v0.21): 24 brands. All 24 scored $C_P$ = 6 (ceiling effect); within-substrate Spearman $\rho$ undefined due to zero predictor variance. Contributes to pooled cross-substrate and Cell A analyses only.

*Excluded:*

Premium kitchenware (v0.17): Phase A halted at C1 inadequacy; per-brand $C_P$ never computed.

## 2.3 AI Presence Index

$C_P$ is the count of panel models (0--6) that recognize a brand in its substrate category. The six-model reference panel (locked v0.17 onward): Claude Opus 4.5, Claude Sonnet 4.5, GPT-4o, GPT-4o-mini, Gemini 2.5 Flash, Gemini 2.5 Flash Lite. Recognition probe: *"Is the brand [BRAND] commonly recognized as a brand of [category]? Answer yes or no."* Binary parse follows v0.19 convention (yes-signal-wins, ties broken by position).

## 2.4 Amazon Best Sellers Rank

BSR was acquired via automated browser extraction (Playwright headless browser) within a single 48-hour acquisition window. For each brand, the script searched Amazon.com with the query `[brand] [category keyword]`, extracted ASINs from search result card attributes, navigated to product detail pages via canonical `/dp/{ASIN}` URLs, and recorded BSR from the product information section via regex extraction from page HTML.

The best-of-N rule retained the single lowest (best) BSR among all products attributed to the brand. Brands with zero Amazon listings in the relevant category were coded as *absent*.

Coverage: 104 of 106 brands listed (98.1%); 2 absent (Nogent/Goyon-Chazeau, kitchen knives; Cle de Peau Beaute, skincare).

## 2.5 Statistical Analysis

Per-substrate: Spearman rank correlation between $C_P$ and raw BSR among listed brands. Negative $\rho$ indicates higher Presence predicts better (lower) BSR rank.

Pooled: Within-substrate percentile normalization of BSR (0--100, lower = better seller), pooled across all listed brands including the ceiling substrate. Spearman $\rho$ on pooled percentile-normalized BSR.

Cell A test: Mann-Whitney U on BSR percentile, split at $C_P \geq 4$ versus $C_P < 4$.

Absent test: Mann-Whitney U on $C_P$, split by Amazon listing status. Pre-registered minimum of 5 absent brands was not met (n = 2); test not conducted.

## 2.6 Pre-Registration Amendments

DEVIATIONS Entry 0 documents three amendments between r1 and r2:

1. Premium kitchenware (v0.17) excluded: Phase A halted at C1 inadequacy; no per-brand $C_P$ artifact exists.
2. Cosmetics (v0.21) reclassified: ceiling effect (all $C_P$ = 6) prevents within-substrate correlation; substrate contributes to pooled analysis only.
3. Kitchen knives (v0.16) $C_P$ retrofitted: original v1.2 methodology did not produce the v1.4+ $C_P$ metric; 156 Recognition probes run under the standard protocol to align the metric.

H_PV_Primary threshold adjusted from "3 of 5 substrates" to "2 of 3 testable substrates."

# 3. Results

## 3.1 C_P Distributions

Kitchen knives (v0.16 retrofit): $C_P$ ranged from 0 to 6, with 15 brands at the ceiling ($C_P$ = 6) and 11 brands distributed across lower values. Mean = 4.73, SD = 1.97.

Audiophile headphones (v0.19): $C_P$ ranged from 2 to 6, with 10 of 16 brands at $C_P$ = 6. Mean = 5.19, SD = 1.17.

Skincare (v0.20): $C_P$ ranged from 0 to 6, with 14 of 24 brands at $C_P$ = 6 and notable outliers at 0 (Rare Beauty), 2 (Goop, Tower 28), and 3 (Chanel Beauty, Dior Beauty). Mean = 4.92, SD = 1.77.

Cosmetics (v0.21): All 24 brands at $C_P$ = 6. Zero variance.

## 3.2 BSR Distributions

BSR varied substantially within each substrate, spanning multiple orders of magnitude. Kitchen knives: 963 to 422,730. Audiophile headphones: 56 to 200,101. Skincare: 18 to 237,462. Cosmetics: 12 to 29,364.

## 3.3 Per-Substrate Correlations

No substrate approached the pre-registered threshold of $\rho \leq -0.40$ (p < 0.05).

| Substrate | n | $C_P$ range | Spearman $\rho$ | p | Threshold met |
|---|---|---|---|---|---|
| Kitchen knives (v0.16) | 25 | 0--6 | +0.048 | 0.819 | No |
| Audiophile headphones (v0.19) | 16 | 2--6 | -0.116 | 0.668 | No |
| Skincare (v0.20) | 23 | 0--6 | +0.049 | 0.823 | No |
| Cosmetics (v0.21) | 24 | 6 (ceiling) | --- | --- | N/A |

**H_PV_Primary verdict: FALSIFIED** (0/3 testable substrates meet threshold).

![C_P versus Amazon BSR by substrate. Each panel shows listed brands with Spearman $\rho$ annotated. No substrate shows a significant relationship.](../../reports/figs/v26/chart_26_cp_vs_bsr_scatter.pdf){#fig:scatter width=100%}

## 3.4 Pooled Cross-Substrate Correlation

Across 88 listed brands with percentile-normalized BSR, the pooled Spearman $\rho$ was -0.0002 (p = 0.998). The correlation is indistinguishable from zero.

**H_PV_Pooled verdict: FALSIFIED** ($\rho$ > -0.30).

## 3.5 Cell A Separation

Brands with $C_P \geq 4$ (n = 78) had a median BSR percentile of 51.09; brands with $C_P < 4$ (n = 10) had a median of 54.00. The difference was not significant and the magnitudes were substantively negligible.

**H_PV_CellA verdict: FALSIFIED.**

## 3.6 Absent-Brand Analysis

Only 2 brands were Amazon-absent (Nogent/Goyon-Chazeau, $C_P$ = 6; Cle de Peau Beaute, $C_P$ = 0). The pre-registered minimum of 5 absent brands was not met.

**H_PV_Absent verdict: UNDETERMINED** (insufficient sample).

## 3.7 Pre-Registration Outcomes

| Hypothesis | Pre-registered claim | Verdict | Key statistic |
|---|---|---|---|
| H_PV_Primary | $\rho \leq -0.40$ in $\geq$ 2/3 substrates | FALSIFIED | 0/3 substrates |
| H_PV_Pooled | Pooled $\rho \leq -0.30$, p < 0.01 | FALSIFIED | $\rho$ = -0.0002, p = 0.998 |
| H_PV_CellA | Cell A median BSR < Other | FALSIFIED | 51.09 vs 54.00, n.s. |
| H_PV_Absent | Absent brands lower $C_P$ | UNDETERMINED | n = 2 absent |

# 4. Discussion

## 4.1 The Null as Signal

The uniform null across three substrates and the pooled analysis is not ambiguous. The Spearman correlations are not merely non-significant --- they are effectively zero ($\rho$ range: -0.116 to +0.049; pooled $\rho$ = -0.0002). This is not a power problem: the study had sufficient range in both variables ($C_P$: 0--6 across substrates; BSR: 18 to 422,730), and the sample sizes, while modest, would have detected even moderate effects. The absence of a relationship is the finding.

## 4.2 Discriminant Validity Interpretation

The Campbell and Fiske (1959) multitrait-multimethod framework requires that a construct demonstrate both convergent validity (correlation with theoretically related measures) and discriminant validity (non-correlation with theoretically unrelated measures). The AIAS Presence component now satisfies both requirements.

Convergent: $C_P$ correlates strongly with Google Trends search interest (v0.25; $\rho$ = 0.74, p < 0.001 on B2B SaaS substrate). Both measures capture a dimension of brand salience --- one in AI knowledge systems, the other in consumer search behavior.

Discriminant: $C_P$ shows zero correlation with Amazon Best Sellers Rank (this study; pooled $\rho$ = 0.000 across three consumer-goods substrates). BSR captures short-term retail purchasing velocity in a specific commercial channel --- a dimension of Physical Availability that is theoretically independent of brand representation in language models.

The convergent-discriminant pair supports the claim that AI Presence measures something specific and novel: the breadth of a brand's recognition across large language model knowledge systems, distinct from both search-engine salience and retail market performance.

## 4.3 Why AI Presence Should Not Predict Retail Sales

The null result is theoretically coherent. LLM training corpora overrepresent editorial, journalistic, and enthusiast discourse relative to transactional content. A brand can be extensively discussed in food media, knife forums, and product-review publications (producing high $C_P$) without necessarily dominating Amazon sales volume, which reflects pricing, distribution logistics, Prime eligibility, advertising spend, and consumer purchasing inertia --- none of which are well-represented in LLM pretraining data.

Conversely, a brand can achieve strong Amazon sales through aggressive pricing and marketplace optimization (producing low BSR) without generating the editorial coverage that feeds LLM knowledge. The two signals originate in fundamentally different data-generating processes.

## 4.4 The Ceiling Effect as Corroborating Evidence

The cosmetics substrate (v0.21) presented a ceiling where all 24 brands achieved $C_P$ = 6, yet BSR varied from 12 (Maybelline) to 29,364 (Anastasia Beverly Hills). This is a natural experiment in which AI Presence is held constant while retail performance varies by three orders of magnitude. The ceiling effect does not merely prevent within-substrate correlation --- it demonstrates the independence of the two constructs. Full AI recognition is compatible with any level of retail performance.

## 4.5 Implications for the Tri-System Framework

The Tri-System Brand Growth framework (Gonzalez Castro, 2025) positions AI Availability as a third measurable system alongside Mental Availability (brand salience in consumer memory) and Physical Availability (ease of purchase). This study's results are consistent with that architecture. If AI Presence were simply a proxy for Physical Availability, it would correlate with BSR --- a proxy for Physical Availability in the Amazon channel. It does not. The two systems measure independent facets of brand market access.

This supports the framework's claim that AI Availability captures a genuinely new dimension of the brand-growth landscape, not a redundant repackaging of existing constructs.

# 5. Limitations

1. *Temporal gap.* $C_P$ scores for v0.19 and v0.20 were measured months before BSR acquisition. LLM knowledge is relatively stable across this interval, but brand market conditions may have shifted. The v0.16 retrofit was contemporaneous with BSR acquisition, and the null result held there as well, mitigating this concern.

2. *BSR as a Physical Availability proxy.* BSR reflects sales rank within Amazon, one retail channel among many. Brands with strong retail presence outside Amazon (e.g., department-store-exclusive prestige skincare) may appear to have weak Physical Availability when measured through BSR alone. A multi-channel sales metric would provide a stronger test.

3. *Single-channel retail signal.* Amazon's marketplace mechanics (advertising, Prime eligibility, Buy Box algorithms) introduce noise that is unrelated to either AI Presence or brand salience. BSR is a noisy proxy for genuine purchase popularity.

4. *Substrate scope.* Three testable substrates is the minimum for cross-substrate generalization. The v0.17 exclusion and v0.21 ceiling effect were not anticipated at pre-registration, reducing the originally planned five-substrate design. Future studies should verify substrate $C_P$ variance before inclusion.

5. *v0.16 retrofit provenance.* The kitchen knives $C_P$ was acquired under a different temporal context than the original v0.16 measurement. The retrofit aligns the metric to the v1.4+ protocol but introduces a provenance asymmetry relative to v0.19 and v0.20 data.

6. *Absent-brand test untestable.* Only 2 of 90 brands across testable substrates were Amazon-absent, far below the pre-registered minimum of 5. The H_PV_Absent hypothesis remains open.

# 6. Future Research

1. *Multi-channel validity.* Extend the discriminant validity test to retail channels beyond Amazon --- Sephora rankings for beauty, B\&H Photo for electronics, specialty retailer data for kitchenware --- to confirm the null generalizes beyond a single marketplace.

2. *Behavioral correlates.* The Phase 3 construct validity agenda should prioritize click-through and recommendation-acceptance metrics, which sit closer to the theorized mechanism of AI Availability than retail sales volume.

3. *Longitudinal BSR tracking.* A repeated-measures design comparing BSR change over time with $C_P$ stability would address whether AI Presence predicts *changes* in retail performance even if it does not predict *levels*.

4. *Pre-screen $C_P$ variance.* Future cross-substrate validity studies should verify $C_P$ distributional properties before inclusion, adding a minimum-variance inclusion criterion to the protocol.

5. *Convergent-discriminant matrix expansion.* The current evidence covers one convergent pair (Google Trends) and one discriminant pair (Amazon BSR). A full Campbell-Fiske matrix would include additional convergent measures (e.g., Wikipedia pageviews, brand-mention frequency in news corpora) and discriminant measures (e.g., brand equity survey scores, stock price) to map the nomological network comprehensively.

# References

Campbell, D. T., \& Fiske, D. W. (1959). Convergent and discriminant validation by the multitrait-multimethod matrix. *Psychological Bulletin*, 56(2), 81--105.

Cronbach, L. J., \& Meehl, P. E. (1955). Construct validity in psychological tests. *Psychological Bulletin*, 52(4), 281--302.

Gonzalez Castro, P. U. (2025). Tri-System Brand Growth: AI Availability as a third measurable system. MSI Working Paper.

Gonzalez Castro, P. U. (2026a). AIAS 1.0 Synthesis: AI Availability as a third measurable layer of brand access. SSRN 6817841.

Gonzalez Castro, P. U. (2026b). AIAS Measurement Program, study series v0.6--v0.22. SSRN.

Gonzalez Castro, P. U. (2026c). AIAS Presence and Google Trends: Construct validity on the B2B SaaS substrate (v0.25). SSRN.

Gonzalez Castro, P. U. (2026d). AIAS Measurement Protocol v1.6. SSRN 6816340.

# Declarations

## Conflict of Interest

The author is Director, Corporate Brand Creative and Governance, at Samsung Electronics America. Samsung products do not appear in any substrate panel in this study. This disclosure is provided for transparency; no Samsung data, resources, or direction influenced the study design, execution, or interpretation.

## Data and Code Availability

All data, pre-registration artifacts, acquisition scripts, scoring code, and analysis outputs are deposited at OSF (osf.io/ec6wh/v26/). The v0.16 $C_P$ retrofit raw responses and provenance sidecar are included in the deposit.

## Funding

Self-funded.

## Ethics

Not applicable. No human subjects. Data sources: public LLM APIs (Recognition probes) and public Amazon product pages (BSR extraction).

# Author Information

**Pablo Ulpiano González Castro**\
School of Visual Arts, MPS Branding Program, New York, NY (primary academic affiliation)\
Third System\texttrademark{} (research entity; data archive and methodology venue for the AIAS Measurement Program)\
Correspondence: pablou@pablou.com $\cdot$ pablou.com\
ORCID: 0009-0003-8968-9990
