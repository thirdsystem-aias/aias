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

{\fontsize{16}{20}\selectfont\bfseries A Construct-Validity Pilot for AI Presence Against External Behavioural Data\par}

\vspace{0.8em}

\textit{Pre-Registered Evidence from 18 Project Management Software Brands at Two Longitudinal Waves Against Google Trends; the Linear Paradox and the Todoist Inverse Anchor a Tighter Category Boundary in AI Mediation than in Consumer Search}

\vspace{2em}

\textit{Working Paper · Version 0.11 · Construct-Validity Pilot (Project Management Software × Google Trends)}

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

10 May 2026

\vspace{2.5em}

\textit{Working paper. Not under peer review. Pre-registered.}

\end{center}

\newpage

\setlength{\parskip}{8pt}
\setlength{\parindent}{0pt}

## Abstract

This paper reports the first construct-validity test in the AIAS measurement programme: a single-category pre-registered pilot comparing per-brand AI Presence rates against per-brand Google Trends search interest for eighteen project management software brands, measured at two longitudinal waves seven days apart. The study opens Phase 3 of the AIAS programme by establishing whether the LLM-side measurement instrument developed across versions v0.6 through v0.10 corresponds to observable consumer behaviour at the brand level. Four hypotheses with explicit numerical thresholds were committed to a pre-registration document locked at git commit f20ade8 (tag *v0.11-prereg*) prior to any Google Trends acquisition call against the wave windows.

The result is informative in a way that a clean confirmation or a hard rejection would not be. AI Presence and Google Trends search interest are positively correlated (Spearman ρ = 0.496 at t₁, 0.476 at t₂; one-tailed *p* < 0.05 at both waves) and stably so across the seven-day longitudinal interval (|Δρ| = 0.020 — H2 confirmed with almost an order of magnitude of margin against the pre-registered 0.15 tolerance). But the correlation narrowly misses the pre-registered moderate-to-strong threshold (ρ > 0.5) at t₁ by 0.004 and weakens further under covariate control (partial ρ ≈ 0.41 after brand age and competitive density adjustment — H4 falsified). The leaderboard test (H3) localises where the construct fails: at both waves, only one of three AI-top-three brands appears in the Trends top-five. The construct's divergence is concentrated at the top of the AI Presence distribution.

Two diagnostic cases anchor the substantive interpretation. Linear has the highest AI Presence in the registry (86.5 percent) and a Google Trends rescaled mean of 1.88 with Asana indexed to 100 — AI's number-one PM-software recommendation despite negligible consumer search interest. Todoist has the inverse profile: 1.04 percent AI Presence with a Trends value of 28, comparable to GitHub Projects, which receives forty times more AI Presence. Both cases support the same finding: AI applies a tighter and partly-different category boundary than consumer search does. Linear is inside AI's PM-software category but barely inside consumers' search-revealed one; Todoist is outside AI's PM-software category but well inside consumers'. The construct of AI Availability is correlated but not equivalent to Mental Availability — consistent with the theoretical position articulated in the Tri-System Brand Growth framework.

The combined result set is interpreted as a partial validity argument for AI Presence as a distinct construct. AI Presence behaves like a real, structured property at the brand level — it covaries with consumer search interest at moderate strength, reproduces across waves at near-identity, and diverges from consumer search in identifiable, theoretically-predictable places. It is not, however, interchangeable with Mental Availability at the level of practical inference, and the practical question of whether AI Presence predicts purchase behaviour remains the object of the Phase 3 expansion programme.

## Keywords

AI Availability; AI Presence; Mental Availability; brand mediation; construct validity; AIAS; Google Trends; pre-registered measurement; longitudinal replication; project management software; LLM brand recommendations

## JEL Classification

M31 (Marketing) — primary; L86 (Information and Internet Services; Computer Software); L15 (Information and Product Quality); D83 (Search; Learning; Information and Knowledge; Communication; Belief; Unawareness); M37 (Advertising)

## Paper status

Working paper. Not under peer review. Pre-registered. Opens Phase 3 of the AIAS measurement programme. Builds directly on the AI Presence input deposited in *AI Presence Drift: A Longitudinal Re-Baseline of Five Brand Categories* ([SSRN ID 6736878](https://ssrn.com/abstract=6736878)), which established one-week stability of the gross-Presence variable on the matched two-model subset used here. Cross-references the foundational theoretical paper *AI Availability: Extending Mental and Physical Availability into Algorithmic Retrieval* ([SSRN ID 6659000](https://ssrn.com/abstract=6659000)). Methodological reference: *AIAS Presence Measurement Protocol v1.1* ([SSRN ID 6722319](https://ssrn.com/abstract=6722319)). Prior empirical papers in the programme: cross-category baseline ([SSRN ID 6720959](https://ssrn.com/abstract=6720959)); phantom-brand persistence designed-for-test ([SSRN ID 6721779](https://ssrn.com/abstract=6721779)); discourse-language bias designed-for-test ([SSRN ID 6728000](https://ssrn.com/abstract=6728000)); naive-phantom rate longitudinal stability ([SSRN ID 6741163](https://ssrn.com/abstract=6741163)). Pre-registration document (PRE_REGISTRATION.md, locked at git commit f20ade8, tag *v0.11-prereg*) and underlying datasets released alongside this paper at osf.io/ec6wh/.

\newpage

## 1. Introduction

Brand growth research in the Ehrenberg-Bass tradition rests on two empirical regularities of market structure: Mental Availability (the propensity of a brand to be retrieved in buying situations) and Physical Availability (the ease with which it can be found, recognised, and bought) (Sharp 2010; Romaniuk 2018; Sharp and Romaniuk 2021). The introduction of AI intermediaries between consumer and brand — large language models that produce direct brand recommendations in response to consumer queries — is the substrate change the Tri-System Brand Growth framework addresses by adding a third layer, AI Availability, defined as the brand-level property governing whether a brand is retrieved, recommended, or selected by an AI intermediary in a category-relevant decision context (González Castro 2026a).

The AIAS Presence Measurement Programme has, through versions v0.6 through v0.10, established a methodologically rigorous LLM-side measurement of brand presence in AI-generated category recommendations. v0.6 measured baseline presence rates across five consumer categories using six contemporary models (González Castro 2026c). v0.7 introduced and tested phantom-brand persistence as a designed-for-test diagnostic (González Castro 2026d). v0.8 isolated discourse-language bias in cross-lingual categories (González Castro 2026e). v0.9 re-measured the v0.6 baseline at t₂ on a matched two-model subset, establishing one-week stability of the gross-Presence variable (González Castro 2026f). v0.10 extended phantom-brand persistence into the v0.9 longitudinal frame (González Castro 2026g).

What none of these prior studies tests is the question on which the programme's external validity ultimately rests: does LLM-measured AI Presence correspond to observable consumer behaviour? A measurement that perfectly captures what AI systems do in their recommendations — but that has no relationship with what consumers actually search, consider, or buy — would be a methodologically clean but practically inert construct. The Tri-System Brand Growth manuscript states this gap explicitly: AI Presence has unverified consumer-level predictive value (González Castro 2026a, §1).

v0.11 is the first construct-validity test in the programme. It is positioned as the Phase 3 pilot: a single-category test against an external behavioural validator (Google Trends search interest), sized for *whether the methodology yields a defensible test*, not for definitive resolution of the construct-validity question. The pilot result determines the design of Phase 3 expansion — v0.12 to three categories, v0.13 to the full five-category panel — and constrains the substantive claims the Tri-System framework can make about the empirical separability of AI Availability from Mental Availability.

Project management software was selected as the pilot category for three converging reasons. The discourse is English-only across the registry, removing the language-bias confounds isolated in v0.8. Every brand has a public web presence and a Google Trends signal available. Among the five v0.6 baseline categories, PM software showed the most stable cross-model agreement, providing the cleanest input distribution for a correlation test (González Castro 2026c, §4.1).

The test specification was conservative. Four hypotheses with explicit numerical thresholds were committed to a pre-registration document (PRE_REGISTRATION.md) locked at git commit f20ade8 (tag *v0.11-prereg*) prior to any Google Trends acquisition call against the wave windows (Nosek et al. 2018). The hypotheses isolated specific candidate properties of the construct: cross-sectional construct validity at moderate-to-strong strength (H1, primary); cross-wave stability (H2, secondary); leaderboard directional consistency (H3, secondary, rank-categorical); covariate-controlled construct validity (H4, secondary, against brand age and competitive density). The both-waves conjunction in H1 and H4 provides built-in family-wise error rate control: under the null, joint probability ≈ 0.05² = 0.0025, more stringent than the conventional 0.05 family-wise rate.

The headline result is mixed in a way that turns out to be informative. The H1 cross-sectional correlation is positive and significant at both waves (Spearman ρ = 0.496 at t₁, 0.476 at t₂; one-tailed *p* < 0.05) but misses the moderate-to-strong threshold by 0.004 at t₁. H2 confirms with almost an order of magnitude of margin: |Δρ| = 0.020 against a 0.15 tolerance. H3 falsifies decisively: only one of three AI-top-three brands appears in the Trends top-five at each wave. H4 falsifies at the magnitude bar: partial ρ ≈ 0.41 after covariate control, missing the 0.5 threshold by approximately 0.09. The four outcomes together describe a relationship that is real, reproducible, and structurally distinct from consumer search — but not interchangeable with it at the level of practical inference.

The substantive contribution of this paper, beyond the empirical findings themselves, is the identification of a structural locus where the construct diverges. Two diagnostic cases anchor the interpretation. Linear, the AI-top brand in PM software at both waves, has the second-lowest Trends value across the eighteen-brand registry — high AI Presence with negligible consumer search interest. Todoist has the inverse profile — non-trivial consumer search interest with effectively zero AI Presence. Both cases support a single substantive finding: AI applies a tighter and partly-different category boundary than consumer search does. Linear sits inside AI's PM-software category but only marginally inside consumers' search-revealed one; Todoist sits outside AI's PM-software category but well inside consumers'. The construct of AI Availability is correlated but not equivalent to Mental Availability — the position the Tri-System framework articulates theoretically, now supported empirically in a single category.

The remainder of the paper is organised as follows. Section 2 describes the pre-registered method, including the construct-validity question, the AI Presence and Google Trends inputs, the pivot-rescaling protocol used to make Trends indices cross-brand comparable, the longitudinal wave structure, the four hypothesis specifications, and the n-floor for confirmatory inference. Section 3 reports the four findings in narrative form, each anchored to a pre-registered hypothesis. Section 4 reports pre-registered hypothesis outcomes in tabular form. Section 5 develops the substantive interpretation: that AI applies a tighter and partly-different category boundary than consumer search does, and that this structural difference is the candidate mechanism underlying the construct's divergence from Mental Availability. Section 6 addresses limitations, including single-category scope, the single-validator design, small-n constraints, and the open question of practical predictive validity for purchase behaviour. Section 7 outlines Phase 3 expansion work.

## 2. Method

The measurement followed the AIAS Presence Measurement Protocol v1.1 (González Castro 2026b), unchanged from v0.9. The longitudinal frame and matched-subset framing developed in v0.9 (González Castro 2026f, §2.1) are adopted directly; the AI Presence input used in v0.11 is the same matched-subset measurement deposited at the v0.9 publication.

### 2.1 Pre-registration

Four hypotheses with explicit numerical thresholds were locked in PRE_REGISTRATION.md at git commit f20ade8, with tag *v0.11-prereg*, on 10 May 2026 UTC prior to any Google Trends acquisition call against the wave windows. The pre-registration document specifies hypotheses; the brand registry; topic-mid lookups and locked per-brand acquisition queries; t₁ and t₂ wave windows; pivot-bundle composition; pre-acquisition exclusions (rule E1a); at-acquisition decision rules (E1b through E5); the n-floor for confirmatory inference; the brand age covariate sources for H4; and the analysis steps. The pre-registration document, the registry that obtained at lock time, the locked query specifications, and a pre-acquisition validation pass against an out-of-sample window (1–7 April 2026) were committed to a public git repository before t₁ or t₂ data collection began.

Pre-acquisition activity completed and deposited prior to lock: SerpAPI topic-mid pass-through verification on Asana; topic-mid resolution via the `pytrends` library's `suggestions()` endpoint for fourteen candidate brands (eleven resolved to topic mids; four descended to T3 brand-plus-category compound queries); per-brand validation against the out-of-sample window returning seventeen PASS, one SKIP (Asana, validated in the pass-through phase), one FAIL (Shortcut, excluded under rule E1a). No analysis output existed at the moment of lock.

### 2.2 Design overview

v0.11 measures the cross-sectional correlation between two independent brand-level signals: per-brand AI Presence rate (drawn from the v0.9 deposited matched-subset LLM measurements) and per-brand Google Trends search interest (acquired fresh at v0.11 under the pre-registered protocol). The two signals are compared at two longitudinal waves (t₁, t₂) seven days apart. The cross-sectional correlation at each wave operationalises H1; the cross-wave delta operationalises H2; the rank-categorical top-three-in-top-five test operationalises H3; the partial-correlation after age and tier control operationalises H4.

The two signals are independent in the sense that AI Presence is an LLM-side measurement of model recommendation behaviour while Google Trends is a Google-side measurement of consumer search activity. A positive correlation between the two indicates that whatever the LLM tier captures at the brand level is at least partly tracking the consumer-search tier at the brand level. The strength, stability, and structure of that correlation are the empirical content of the construct-validity question.

### 2.3 AI Presence input

Per-brand AI Presence rates were drawn from the v0.9 deposited canonical scoring (González Castro 2026f) at the matched two-model subset (Anthropic Claude Sonnet 4.6 and OpenAI gpt-5.4-mini), restricted to the project management software category. Wave t₁ corresponds to the v0.6 collection window (29–30 April 2026); wave t₂ corresponds to the v0.9 re-baseline collection window (7 May 2026). Both waves measure ninety-six responses each per wave: six prompts × two models × eight runs. For each brand B in the registry, AI Presence at wave w is computed as the fraction of the ninety-six responses at wave w in which brand B appears in the canonical brand-mention extraction.

The matched-subset restriction is methodological: the longitudinal claim is that AI behaviour reproduces across the seven-day interval, and the only models present at both waves are Sonnet 4.6 and gpt-5.4-mini. The four additional models present at t₂ only (Anthropic Opus 4.7, OpenAI gpt-5.5, Google Gemini 2.5 Flash, xAI Grok 4.1 Fast) are parallel new baselines for those models' own future longitudinal work and do not contribute to v0.11's correlation tests. The framing preserves clean t₁/t₂ attribution: any t₁ to t₂ delta in the matched-subset measurement is attributable to AI behaviour change rather than to model-set expansion.

### 2.4 Google Trends validator and pivot-rescaling

Daily search-interest indices for the same eighteen brands were acquired in a single locked session on 10 May 2026 UTC via SerpAPI's Google Trends engine (engine=`google_trends`, data_type=`TIMESERIES`). Per-brand acquisition queries follow the pre-registered tiered specification: T1 (topic mid where Google Trends has an entity ID corresponding unambiguously to the PM-software brand, used for eleven brands); T2 (distinctive bare brand name, four brands); T3 (brand-plus-category compound `<brand> project management`, three brands). The full per-brand specification table is committed to /v11/registries/brands_pm_query_spec.csv.

Google Trends exposes only the bundle-normalised 0–100 search-interest index, not raw query volume. To make daily indices cross-brand comparable across the eighteen-brand analysis set, the acquisition uses overlapping pivot bundles. Each bundle contains the pivot brand (Asana, topic mid /m/0c3z\_p8) plus four other brands. With seventeen non-pivot brands, this requires five bundles. The fifth bundle pads with the high-volume non-PM term "kanban" plus "agile" and "scrum" to anchor the bundle composition without contaminating the rescaling. For each brand B at each day d, the rescaled index is:

$$\text{rescaled}_B(d) = \frac{\text{raw}_B(d)}{\text{raw}_{\text{Pivot}}(d)} \times 100$$

The pivot's own rescaled value is by construction 100 every day, with within-window standard deviation zero. Pre-registration §5.1 explicitly retains the pivot in the correlation analyses as a brand on equal footing with the others, exempting it from the at-acquisition E1b decision rule (which excludes brands with zero or constant within-window means). The exemption is mechanical: the pivot's standard deviation of zero is structural by construction, not a measurement failure.

### 2.5 Wave windows

The t₁ Trends window is 27 April through 3 May 2026 (centred on the v0.6 collection window of 29–30 April). The t₂ Trends window is 4 May through 10 May 2026 (centred on the v0.9 collection day of 7 May). Windows are fully disjoint at the 3/4 May boundary with identical Monday–Sunday composition (one of each weekday in each window). Each window's seven daily rescaled values per brand are aggregated as the arithmetic mean to produce the per-brand within-window mean used in the correlation analyses.

### 2.6 Hypothesis specifications

**H1 (primary).** Spearman rank correlation computed across the eligible brand set between per-brand AI Presence rate and per-brand within-window Trends mean (pivot-rescaled, Worldwide region). Confirmed if ρ > 0.5 AND one-tailed *p* < 0.05 at both waves; falsified otherwise. The Pearson coefficient is reported as a sensitivity. The US-only region is reported as a separate sensitivity. Spearman is the primary statistic because rank-based methods are less sensitive to the saturation present at the top of the AI Presence distribution and to leverage effects from any single high-magnitude observation in the Trends distribution.

**H2 (secondary).** |ρ at t₂ − ρ at t₁|, computed against the t₁ and t₂ Spearman values from H1. Confirmed if ≤ 0.15. The threshold is calibrated against test-retest stability typical of behavioural correlation measures over a one-week interval.

**H3 (secondary).** At each wave, identify the top-three brands by AI Presence and the top-five brands by Trends. Confirmed if all three of the AI-top-three appear in the Trends top-five, at both waves. Provides a rank-categorical check robust to small variations in the correlation magnitude.

**H4 (secondary).** Spearman partial correlation between AI Presence and Trends, controlling for brand age (years since product launch) and competitive density (market tier from the v0.6 registry, treated as ordinal: incumbent = 1, mid-tier = 2, challenger = 3). Computed as Pearson on rank residuals after OLS on rank-transformed covariates; degrees of freedom corrected for *k* = 2 covariates. Confirmed if partial ρ > 0.5 AND one-tailed *p* < 0.05 at both waves.

### 2.7 Sample composition and n-floor

The brand registry contains nineteen brands across three market tiers (five incumbent, eight mid-tier, six challenger), frozen at the v0.6 lock and identical to the registry used in v0.6, v0.9, and v0.10. Two pre-registered modifications to the analysis sample: Shortcut excluded pre-acquisition under rule E1a (the locked T3 compound query returned the SerpAPI response "Google Trends hasn't returned any results for this query" at the out-of-sample validation window); Height retained as a phantom brand following the rebrand-period convention from v0.7 and v0.10 (Height shut down operations on 24 September 2025, approximately seven months before the v0.11 measurement windows, but its locked T3 compound query returns non-zero residual Trends signal).

The n-floor for confirmatory inference is sixteen of the nineteen registry brands. H1, H2, and H4 are evaluated only if this floor is cleared at both waves; otherwise the hypotheses route to descriptive disclosure. H3 is computable per-wave from whatever brands are present. At the actual acquisition, Height registered zero pivot-rescaled signal at t₁ (mean = 0, standard deviation = 0) and qualified for exclusion under E1b for the t₁ wave only; at t₂ Height returned a single-day spike (within-window mean = 1.02, standard deviation = 2.7) and was retained with the E5 sparsity flag. Effective sample size: t₁ *n* = 17 (Asana via §5.1 pivot exemption plus sixteen others; Height excluded); t₂ *n* = 18 (Asana plus seventeen others including Height). Both clear the sixteen-of-nineteen n-floor.

\newpage

## 3. Results

### 3.1 Finding 1 — AI Presence and Trends correlate positively but just-miss the moderate-to-strong threshold.

Per-brand AI Presence rates correlate positively with per-brand Google Trends rescaled means at t₁: Spearman ρ = 0.496, one-tailed *p* = 0.0214, *n* = 17. At t₂: Spearman ρ = 0.476, one-tailed *p* = 0.0228, *n* = 18. The significance bar is cleared at both waves; the magnitude bar (ρ > 0.5) is missed at t₁ by 0.004 and at t₂ by 0.024. **H1 is falsified at the locked threshold.** The directional claim of the construct — that AI Presence and consumer search interest co-vary at the brand level — is statistically supported. The strength claim is not.

The pre-registered threshold of ρ > 0.5 was calibrated against the conventional moderate-to-strong correlation benchmark in behavioural research. v0.11 misses this bar by 0.004 at the primary wave. The pre-registration discipline gives this near-miss its weight: a post-hoc adjustment of the threshold to ρ ≥ 0.49 would convert the result, but the bar is what it is. The miss is small enough to be informative about the underlying relationship; the relationship is present and consistent in direction but weaker than the construct's distance from a noise-only null suggests.

![Per-brand AI Presence (matched subset, Sonnet 4.6 + gpt-5.4-mini, PM software) against Google Trends rescaled mean at t₁. Worldwide region. Log-y axis. Pivot brand Asana indexed to 100 by construction. Spearman ρ = 0.496 (*p* = 0.021 one-tailed); Pearson *r* = 0.544. *n* = 17. Linear at top-left and Notion at top-right are the t₁ outliers driving the Pearson-versus-Spearman gap discussed in this section.](../figures/chart_v11_h1_scatter_t1_6col.pdf){width=100%}

The Pearson sensitivity clears the same magnitude bar at both waves (*r* = 0.544 at t₁; *r* = 0.533 at t₂). The Pearson-versus-Spearman disagreement is informative rather than methodologically problematic. Pearson weights large absolute differences. Notion's pivot-rescaled mean at t₁ is 591.95 — approximately six times Asana's structurally-fixed value of 100 — and is by far the largest single value in the Trends distribution. Pearson treats this magnitude directly; the linear fit is anchored by Notion's position high on both axes and pulled up accordingly. Spearman treats Notion as a single high rank and is therefore unaffected by its absolute magnitude, but is pulled down by the rank-1-AI to rank-low-Trends inversions at the top of the AI Presence distribution (driven by Linear; see §3.3). The two statistics tell different parts of the same story: real positive covariation exists, and localised rank inversions at the leadership zone matter for the construct in a way the rank-based statistic registers more sensitively.

The US-only sensitivity replicates the Worldwide pattern at both waves. Spearman ρ = 0.489 at t₁; ρ = 0.455 at t₂. Both miss the magnitude bar; both clear *p* < 0.05. Nothing region-specific is driving the result, and the within-wave US-versus-Worldwide difference is itself smaller than the H2 stability tolerance reported next.

### 3.2 Finding 2 — The relationship reproduces across the seven-day longitudinal interval.

|ρ at t₂ − ρ at t₁| = |0.476 − 0.496| = 0.020. The pre-registered tolerance is 0.15. **H2 is confirmed** with almost an order of magnitude of margin against the threshold. The Pearson statistic shows the same pattern at near-identity: |Δr| = 0.011. The US-only sensitivity is similarly stable across waves at |Δρ| = 0.034. Whatever H1 captured at t₁ was captured again at t₂; the just-miss is not a sampling artefact.

![Per-brand AI Presence against Google Trends rescaled mean at t₂. Same axes and scale as the t₁ figure. The cross-wave visual stability is the H2 finding: Spearman ρ = 0.476; |Δρ| from t₁ = 0.020 — far below the pre-registered tolerance.](../figures/chart_v11_h1_scatter_t2_6col.pdf){width=100%}

The H2 confirmation is the load-bearing positive finding in v0.11. It rules out the interpretation that the H1 near-miss is wave-specific noise. The ρ-statistic's standard error at *n* = 17 is approximately 0.20; a 0.02-magnitude reproducibility against a 0.20-magnitude sampling-error baseline is striking evidence that the relationship being measured is stable across the interval rather than that the test happened to land on the same noise twice. The result extends the longitudinal stability claim from v0.9's within-subject AI Presence stability (gross-Presence variable) to the cross-subject construct-validity correlation between two independent measurements taken at the same waves.

### 3.3 Finding 3 — AI applies a tighter category boundary than consumer search does.

At t₁, the top-three brands by AI Presence are Linear, Asana, and Notion. The top-five brands by Trends are Notion, Jira, Trello, ClickUp, and Confluence. Overlap: Notion (one of three). At t₂, the top-three by AI Presence is Linear, Asana, and Jira; the Trends top-five is unchanged from t₁. Overlap: Jira (one of three). **H3 is falsified at both waves.** The leaderboard divergence concentrates at the top of the AI Presence distribution — the zone where AI mediation carries the most predictive weight for purchase decisions, since AI systems surface their top recommendations first and most prominently.

Two diagnostic cases anchor the substantive interpretation, bracketing the construct divergence from opposite ends:

**The Linear paradox.** Linear has the highest AI Presence in the registry across both waves (86.5 percent at t₁, 89.6 percent at t₂) and the second-lowest Trends value across both waves (rescaled mean 1.88 at t₁; Asana indexed to 100 by construction). AI systems strongly recommend Linear despite the brand's negligible consumer search interest. The bare query *"Linear"* returns Google Trends results dominated by linear-algebra textbooks; the brand-disambiguated query *"linear project management"* returns the small residual signal reported here. From the perspective of consumer search behaviour, Linear is a small brand. From the perspective of AI Presence in PM-software recommendations, Linear is the largest brand in the registry.

**The Todoist inverse.** Todoist has the inverse profile: 1.04 percent AI Presence at t₁ (effectively zero at t₂) with Trends rescaled mean 28.38. The comparison brand GitHub Projects has comparable Trends value (28.01) but receives 42.7 percent AI Presence — forty times more than Todoist at similar consumer search interest. The mechanism is plausibly category-boundary: AI systems frame Todoist as a personal task manager rather than a project management tool and exclude it from PM-software recommendations.

![Slope chart: each brand's rank by AI Presence (left) connected to its rank by Trends (right) at t₁. Steep slopes indicate construct divergence. Extreme cases (|Δrank| ≥ 8) highlighted in copper. Linear (top-left of the AI column) and Todoist (mid-right of the Trends column) bracket the divergence diagnostic discussed in this section from opposite ends.](../figures/chart_v11_h3_rank_shift_t1_6col.pdf){width=100%}

Both cases support a single substantive finding: AI applies a tighter and partly-different category boundary than consumers do. Linear is inside AI's PM-software category but barely inside consumers' search-revealed PM-software category. Todoist is outside AI's PM-software category but well inside consumers' search-revealed one. Both are real PM tools by ordinary consumer reasoning — Linear has been widely adopted in technology companies and has a substantial commercial trajectory; Todoist is a well-recognised productivity application used by individuals and teams alike. The construct of AI Availability is empirically distinct from Mental Availability at the level of the cases that drive the leaderboard, and the distinction is structural rather than noise.

### 3.4 Finding 4 — Brand age and tier covariation absorbs meaningful signal.

Partial Spearman ρ at t₁ = 0.407, one-tailed *p* = 0.0663. Partial Spearman ρ at t₂ = 0.428, one-tailed *p* = 0.0489. **H4 is falsified.** Both waves miss the magnitude bar (ρ > 0.5); t₁ also misses the significance bar. The H1 correlation falls from 0.496 to 0.407 at t₁ (a decrement of 0.089) and from 0.476 to 0.428 at t₂ (a decrement of 0.048) under covariate control.

The pattern indicates that age-and-tier covariation between AI Presence and consumer search interest accounts for a non-trivial portion of the H1 signal. Older brands tend to have more consumer search interest (long accumulated brand history) and may have accumulated more AI training-data presence (long history of web content, news coverage, documentation); the two move together for reasons that are independent of either's direct measurement relevance. Per-row inspection confirms the pattern. Workfront (twenty-four years old, mid-tier) has AI Presence 1.04 percent and Trends 6.67. Wrike (twenty years, mid-tier) has AI 8.33 percent and Trends 12.14. Linear and Motion (both seven years old, challenger tier) over-perform their search-implied AI Presence; older mid-tier brands under-perform. The covariate control removes this systematic drift, exposing the partial relationship below it.

![H4 partial correlation visualisation. Rank residuals on both axes after OLS on rank-transformed brand age and tier ordinal. Partial Spearman ρ = 0.407 (*p* = 0.066 one-tailed), missing both the moderate-to-strong threshold and (at t₁) the significance bar. The relationship remains positive and recognisable but is meaningfully attenuated relative to the raw H1 scatter.](../figures/chart_v11_h4_partial_residual_t1_6col.pdf){width=100%}

The covariate-controlled correlation remains positive at both waves and (just) crosses *p* < 0.05 at t₂, supporting the directional claim of the construct under control. The magnitude is firmly below the moderate-to-strong threshold. A meaningful portion of the raw H1 signal was age-and-tier covariation, not the direct AI-Presence-to-search-interest relationship the construct's substantive claim concerns.

\newpage

## 4. Pre-Registration Outcomes

The four pre-registered hypotheses plus two pre-registered sensitivities are reported in Table 1.

*Table 1. v0.11 construct-validity pilot pre-registration outcomes.*

\begin{table}[H]
\centering
\small
\begin{tabular}{@{}p{0.07\textwidth}p{0.30\textwidth}p{0.15\textwidth}p{0.27\textwidth}p{0.15\textwidth}@{}}
\toprule
\textbf{Hyp.} & \textbf{Claim (matched subset, t\textsubscript{1} → t\textsubscript{2})} & \textbf{Threshold} & \textbf{Outcome} & \textbf{Band} \\
\midrule
H1 & Cross-sectional construct validity (Spearman, Worldwide) & $\rho > 0.5$ AND $p_{1t} < 0.05$ at both waves & $\rho_{t1} = 0.496$ ($p = 0.021$); $\rho_{t2} = 0.476$ ($p = 0.023$) & \textbf{FALSIFIED} \\
\addlinespace
H2 & Cross-wave stability of H1 correlation & $|\Delta\rho| \leq 0.15$ & $|\Delta\rho| = 0.020$ & \textbf{CONFIRMED} \\
\addlinespace
H3 & Leaderboard directional consistency & AI top-3 $\subseteq$ Trends top-5 at both waves & 1 of 3 at both waves (Notion at t\textsubscript{1}; Jira at t\textsubscript{2}) & \textbf{FALSIFIED} \\
\addlinespace
H4 & Covariate-controlled construct validity (age + tier) & Partial $\rho > 0.5$ AND $p_{1t} < 0.05$ at both waves & Partial $\rho_{t1} = 0.41$ ($p = 0.066$); partial $\rho_{t2} = 0.43$ ($p = 0.049$) & \textbf{FALSIFIED} \\
\addlinespace
H1$_r$ & H1 with Pearson statistic (sensitivity) & $r > 0.5$ AND $p < 0.05$ at both waves & $r_{t1} = 0.544$; $r_{t2} = 0.533$ & \textit{Confirmed (sensitivity)} \\
\addlinespace
H1$_{US}$ & H1 on US-only region (sensitivity) & $\rho > 0.5$ AND $p < 0.05$ at both waves & $\rho_{t1} = 0.489$; $\rho_{t2} = 0.455$ & \textit{Falsified (sensitivity)} \\
\bottomrule
\end{tabular}
\end{table}

The result set is mixed in a way that turns out to be informative. The primary hypothesis (H1) is falsified, but the falsification is by 0.004 at the primary wave — the smallest possible quantum of a miss against a threshold expressed at one decimal place. The stability hypothesis (H2) is confirmed with almost an order of magnitude of margin. The leaderboard hypothesis (H3) is decisively falsified in a pattern that, on inspection, localises the construct divergence at exactly the most economically consequential zone of the distribution. The covariate-controlled hypothesis (H4) is falsified by a margin that quantifies the contribution of age-and-tier covariation to the raw H1 signal. The combined pattern is not a clean confirmation of the construct nor a clean rejection of it. It is a structurally informative falsification: H1 falsifies, but the way H1 falsifies — narrowly, stably, with the divergence concentrated at the leadership zone — supports a substantive reading of what AI Presence actually measures.

\newpage

## 5. Discussion: AI Applies a Tighter Category Boundary than Consumer Search

The v0.11 result is more informative than either a clean confirmation or a hard rejection of the construct-validity hypothesis would be. The correlation is positive, statistically significant, stable across waves, and concentrated. Its concentration is at the top of the AI Presence distribution. The pattern across the four pre-registered tests is internally consistent: H1's near-miss, H2's tight stability, H3's leaderboard divergence, and H4's covariate absorption tell the same story from different angles. The substantive interpretation developed here is that AI applies a tighter and partly-different category boundary than consumer search does, and that this category-boundary difference is the structural mechanism underlying the construct's divergence from Mental Availability.

The interpretation has three legs.

First, the construct is real and reproducible. H1's significance at both waves and H2's near-identical reproducibility together rule out the interpretation that the AI-Presence-to-search-interest relationship is noise. The two waves measure the same thing. Whatever AI behaviour produced ρ = 0.496 at t₁ produced ρ = 0.476 at t₂ — a stability margin (|Δρ| = 0.020) far smaller than the standard error of either measurement individually. The Pearson sensitivity confirms the same picture from a different angle: the linear-magnitude relationship is also stable across waves (|Δr| = 0.011). The relationship between AI Presence and consumer search interest is a real property of the brand level in this category.

Second, the divergence is structural, not noise. H3's leaderboard falsification at both waves — one of three rather than three of three — is not the result of small-n sampling variability. The divergence reproduces. The brands that drive the divergence are identifiable and theoretically tractable: Linear and Asana sit at the top of AI Presence at both waves but fall outside the Trends top-five at both waves. The cases at the opposite extreme of the distribution behave symmetrically: Todoist sits well inside the Trends middle band but receives near-zero AI Presence at both waves. The construct divergence concentrates in identifiable cases and reproduces longitudinally, which together rule out interpretation as measurement noise.

Third, the divergence isn't fully explained by confounds. H4's partial-correlation result quantifies the magnitude of the age-and-tier confound and shows that controlling for it weakens but does not eliminate the H1 relationship. After control, the partial correlation remains positive at both waves and clears statistical significance at one of them. The residual relationship is real but weaker than the moderate-to-strong threshold. The substantive interpretation is that age-and-tier covariation accounts for some of the raw H1 signal but not all of it; a meaningful direct AI-Presence-to-search-interest relationship remains under control.

The substantive claim that emerges from the three legs together is the central interpretive contribution of this paper. Linear and Todoist, the two diagnostic cases anchoring the H3 falsification, bracket the same diagnostic from opposite ends. Linear is, by any conventional measure, a real brand: a project management tool widely adopted in technology companies, with a documented commercial trajectory and a public web presence. Its consumer search interest, however, is structurally low — the brand name *Linear* collides with mathematics, statistics, and general-purpose adjective usage. From the perspective of consumer search behaviour Linear is a small brand; from the perspective of AI Presence in PM-software recommendations Linear is the largest brand in the registry. Todoist is the symmetric inverse — moderate consumer search interest comparable to GitHub Projects (Trends value approximately 28 for both), but Todoist receives one-fortieth the AI Presence GitHub Projects receives.

Both cases support a single substantive finding: AI applies a tighter and partly-different category boundary than consumers do. Linear sits inside AI's PM-software category but barely inside consumers' search-revealed PM-software category. Todoist sits outside AI's PM-software category — AI systems frame it as a personal task manager rather than a project management tool — but well inside consumers' search-revealed one, because consumers searching for personal productivity tools routinely surface Todoist. The construct of AI Availability is correlated but not equivalent to Mental Availability — the position the Tri-System Brand Growth framework articulates theoretically (González Castro 2026a, §4–5) and which v0.11 now supports empirically in a single category.

The category-boundary mechanism is structurally distinct from the empirical regularities the AIAS programme has documented in prior versions. Phantom-Brand Persistence (Pattern 6 in the v0.6 framework, designed-for-test in v0.7 and v0.10) addresses brands that persist in AI recommendations after operational decommissioning. Discourse-Language Bias (Pattern 4, designed-for-test in v0.8) addresses brands whose AI Presence is mediated by English-language marketing coverage rather than country of origin. The category-boundary mechanism addresses neither of these but something adjacent: the structural difference between the category as AI systems represent it (likely shaped by training-data clustering, recommendation-system priors, and tool-documentation neighbourhoods) and the category as consumers search it (shaped by use case, problem framing, and naming conventions). The Linear paradox and the Todoist inverse are candidate empirical anchors for this mechanism, awaiting cross-category replication in v0.12 and v0.13.

The interpretation has bounded claims. v0.11 supports the following at the locked confidence level. AI Presence and consumer search interest are positively correlated at the brand level in project management software. The correlation is reproducible across a one-week longitudinal interval. The correlation is partly attributable to age-and-tier covariation; a meaningful direct relationship remains under control, at weaker magnitude than the raw signal. The correlation does not meet the moderate-to-strong threshold; the construct is not interchangeable with consumer search interest at the level of practical inference. The construct's divergence from search is concentrated at the top of the AI Presence distribution.

v0.11 does not support the following claims, which require further evidence. Generalisation to other categories: project management software is one of five v0.6 baseline categories; v0.11 makes no claim about running shoes, premium olive oil, premium facial skincare, or personal finance. Causal direction: v0.11 establishes covariation, not whether AI Presence shapes consumer search, consumer search shapes AI Presence (via training-data updates that reflect prior search-derived prominence), or both depend on a common cause. Practical predictive validity for purchase decisions: Google Trends search interest is one behavioural proxy; purchase data is the validator of ultimate practical interest, and v0.11 is upstream of the purchase-prediction question.

## 6. Limitations

Six caveats apply to the findings reported here.

**Single category.** v0.11 tests one of the five v0.6 baseline categories. The substantive PM-software findings — the Linear paradox, the Todoist inverse, the H3 leadership-zone divergence — are not yet known to generalise. The v0.12 expansion to three categories will test this directly, with running shoes and premium olive oil as the two added categories. Premium olive oil's leadership zone is stable across both AI and consumer search (Brightland, Graza, Castillo de Canena lead in both per González Castro 2026c and 2026f) and is the cleanest replication candidate; running shoes will test the pattern under high-brand-density competitive conditions.

**Single validator.** Google Trends search interest is one behavioural proxy for brand mindshare. A construct that doesn't correlate with one external proxy may correlate with another — purchase data, brand-tracker survey measures, social-media share-of-voice were not measured at v0.11. The result is specifically about the AI-Presence-to-search-interest relationship; the broader construct-validity claim requires multi-validator evidence not collected here.

**Small *n*.** Seventeen to eighteen brands per wave. The pre-registered floor of sixteen was cleared with margin, but the small-*n* constraint is real. The ρ-statistic's standard error is approximately 0.20 at *n* = 17, which is why the H2 stability finding (|Δρ| = 0.020) carries weight: a 0.02-magnitude reproducibility against a 0.20-magnitude sampling-error baseline is striking evidence that the relationship being measured is stable rather than that the test happened to land on the same noise twice.

**Trends index, not raw volume.** Google Trends exposes only the bundle-normalised 0–100 search-interest index, not raw query counts. The pivot-rescaling protocol makes the indices cross-brand comparable but does not recover absolute query volumes. The Asana ≡ 100 baseline is structural by construction. Any interpretation that depends on absolute brand search volumes — for example, an estimate of total category search demand — cannot be drawn from the v0.11 measurement.

**Two waves seven days apart.** H2's stability claim is about the same construct measured twice across one week; it is not a long-horizon stability claim. The v0.12 timing decision will partly determine how far the H2 finding extrapolates. Whether the AI-Presence-to-search-interest relationship is stable across one-month, three-month, or twelve-month intervals — particularly across LLM model releases and Google Trends seasonality cycles — is a separable question the v0.12 design will need to address.

**Phantom-brand effect within Height.** Height shut down operations on 24 September 2025, approximately seven months before the v0.11 measurement windows. The brand returns non-zero residual AI Presence (thirteen to sixteen percent across waves on the matched subset) and zero-to-sparse Trends signal. Per the registry-frozen-ness convention from v0.7 and v0.10, Height is retained in the analysis; the AI Presence is meaningful as phantom-brand persistence, and the small residual Trends signal qualifies under the E5 sparsity flag. The brand's behaviour is not anomalous within the AIAS programme's framework but is worth flagging for readers comparing to brand-set composition in other domains.

## 7. Future Research

The Phase 3 programme will address four priorities surfaced by the v0.11 findings.

**v0.12 — Three-category Phase 3 expansion.** Add running shoes and premium olive oil to the PM-software protocol. The sharpened question: does the H1 just-miss plus H3 leadership-zone divergence pattern generalise, or is it specific to PM-software's category-boundary structure? Premium olive oil's leadership zone is stable across both AI and consumer search and is the cleanest replication candidate. Running shoes will test the pattern under high-brand-density competitive conditions where the registry contains twelve or more active brands. The v0.12 measurement will use the same pivot-rescaling protocol with category-appropriate pivot selection.

**v0.13 — Full-category construct-validity panel.** Extend to the remaining two v0.6 baseline categories (premium facial skincare; personal finance). Personal finance carries the Mint phantom-brand effect documented in v0.7 and v0.10 (González Castro 2026d; 2026g) and is expected on theoretical grounds to show the largest construct divergence — phantom brands with high AI Presence and effectively zero consumer search interest sit at one tail of the AI-to-search-interest relationship.

**Causal-mechanism studies.** v0.11 establishes covariation. The next-step question is mechanism: does AI Presence shape consumer search (via answer-engine surfacing of AI-recommended brands in user-facing UIs); does consumer search shape AI Presence (via training-data updates that reflect prior search-derived prominence); or do both depend on a structural common cause such as brand age, marketing investment, or competitive density? The Tri-System framework's Conditional Reweighting and Default Reinforcement laws (González Castro 2026a, §6) specify falsification conditions for causal claims; mechanism studies operationalising those conditions are the medium-term research path.

**AIAS Phase 4 (components 2–6).** v0.11 through v0.13 establish construct validity for the Presence component of the full AIAS framework. The remaining five components — Ranking, Consistency, Coverage, Grounding, Sentiment — operationalise in Phase 4 and will require their own construct-validity tests against component-appropriate validators. The v0.11 result, if it generalises in v0.12 and v0.13, suggests that the construct-validity bar for each AIAS component is unlikely to be a clean moderate-to-strong correlation with any single external proxy. The Phase 4 design will need to accommodate the empirical reality that AI-mediated brand presence is partly distinct from consumer-tier signals by construction.

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

Nosek, B. A., Ebersole, C. R., DeHaven, A. C., & Mellor, D. T. (2018). The preregistration revolution. *Proceedings of the National Academy of Sciences*, 115(11), 2600–2606.

Romaniuk, J. (2018). *Building Distinctive Brand Assets.* Oxford University Press.

Sharp, B. (2010). *How Brands Grow: What Marketers Don't Know.* Oxford University Press.

Sharp, B., & Romaniuk, J. (2021). *How Brands Grow: Part 2 — Including Emerging Markets, Services, Durables, New and Luxury Brands.* Revised edition. Oxford University Press.

\newpage

## Declarations

### Conflict of Interest

The author serves as Director, Corporate Brand Creative and Governance at Samsung Electronics America. The research presented here is independent of Samsung Electronics America and does not constitute Samsung research. No Samsung Electronics America data, personnel, or commercial interests influenced the design, conduct, analysis, or reporting of this study. Samsung Electronics America did not review the manuscript prior to posting. The brand population evaluated in this study (project management software) does not include Samsung product lines.

### Funding

Self-funded. No external funding sources contributed to this research.

### Data Availability

Underlying datasets, the locked pre-registration document (PRE_REGISTRATION.md, locked at git commit f20ade8e3e04bde86edafb1180a1f6c6429c145f, tag *v0.11-prereg*, lock date 10 May 2026 UTC prior to any Google Trends acquisition call against the wave windows), the v0.9 AI Presence rates input, the Google Trends raw responses (ten pivot-bundle JSON files across two regions), topic-mid suggestion logs, pre-acquisition validation outputs against the out-of-sample window, the brand age source table, the registry files (frozen at v0.6's final state and unchanged across v0.7 through v0.11), the canonical scoring tables, the build-pipeline source code, and the matching brand-format report are deposited in an Open Science Framework project at <https://osf.io/ec6wh/>. The deposit contains row-level CSV outputs throughout; the v0.11 measurement was conducted within a git-tracked repository from methodology lock through publication, and no provenance gaps obtain. The OSF MANIFEST documents the file inventory, the lineage between raw measurements and derived analyses, and the cryptographic git-commit anchor for the locked pre-registration.

## Author Information

Pablo Ulpiano González Castro is faculty in the MPS Branding Program at the School of Visual Arts, New York, where he teaches Creative Strategy. He maintains Third System™ (research entity; data archive and methodology venue) as the publication venue for the AIAS measurement programme. Correspondence: pablou@pablou.com · pablou.com.
