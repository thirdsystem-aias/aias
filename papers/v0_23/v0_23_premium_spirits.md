---
title: "AIAS Presence Index v0.23: Premium Spirits"
subtitle: "Recognition Ceiling, Recall-Driven Regime Classification, and the Conglomerate Ownership Hypothesis Across 24 Brands and Six Large Language Models"
author: "Pablo Ulpiano González Castro"
date: "May 2026"
mainfont: "Carlito"
fontsize: 11pt
geometry: margin=1in
linkcolor: black
urlcolor: black
citecolor: black
header-includes:
  - \usepackage{setspace}
  - \usepackage{float}
  - \usepackage{caption}
  - \usepackage{titlesec}
  - \usepackage{booktabs}
  - \usepackage{longtable}
  - \usepackage{graphicx}
  - \setstretch{1.36}
  - \setlength{\parskip}{8pt}
  - \setlength{\parindent}{0pt}
  - \renewcommand{\maketitle}{}
  - \providecommand{\xmpquote}[1]{#1}
  - \captionsetup{font=small,labelfont=bf,skip=6pt}
  - \titleformat{\section}{\large\bfseries}{\thesection}{1em}{}
  - \titleformat{\subsection}{\normalsize\bfseries}{\thesubsection}{1em}{}
---

\begin{titlepage}
\setstretch{1.0}
\setlength{\parskip}{0pt}
\centering

\vspace*{2cm}

{\LARGE\bfseries AIAS Presence Index v0.23: Premium Spirits}

\vspace{0.6cm}

{\large Recognition Ceiling, Recall-Driven Regime Classification, and the Conglomerate Ownership Hypothesis Across 24 Brands and Six Large Language Models}

\vspace{1.5cm}

{\large\bfseries Pablo Ulpiano Gonz\'{a}lez Castro}

\vspace{0.4cm}

{\normalsize
SVA, MPS Branding Program, New York, NY\\
Third System$^{\text{TM}}$ (research entity; data archive and methodology venue)\\[6pt]
Correspondence: pablou@pablou.com $\cdot$ pablou.com\\
ORCID: 0009-0003-8968-9990
}

\vspace{1.5cm}

{\normalsize\bfseries Working Paper}

\vspace{0.3cm}

{\normalsize May 2026}

\vspace{1.5cm}

{\small
This paper is part of the AIAS (AI Availability Score) Measurement Program operated by Third System. The program measures brand visibility within large language model outputs using a standardized, pre-registered protocol. This is the seventh substrate-level Presence phase (v0.23), examining 24 premium spirits brands under Protocol v1.6.
}

\end{titlepage}

# Abstract {-}

This paper reports AIAS Presence Index v0.23, measuring AI Presence for 24 premium spirits brands across six large language models under Protocol v1.6. Premium spirits is the seventh substrate family in the AIAS measurement program and the first to exhibit a universal recognition ceiling: all 144 Phase A probes return R3 (rich recognition), eliminating recognition variance from the composite entirely. The Presence distribution is driven exclusively by Recall --- which brands AI systems recommend, not which they can describe. Composite scores range from 40.0 (perfect recognition, zero recall) to 71.19, distributing evenly across four regimes (6 Dominant, 6 Established, 6 Emerging, 6 Absent). Six brands that LLMs characterize in expert detail --- Bombay Sapphire, The Balvenie, Casamigos, Compass Box, Fernet-Branca, and Jameson --- are never or rarely surfaced in recommendation contexts, exposing a recognition--recall gap invisible to traditional brand-tracking methods. The substrate-specific hypothesis H_ConglomeratePortfolio is falsified: conglomerate-owned brands (n = 14) average 60.75 on the Presence composite versus 58.05 for independents (n = 10), a non-significant 4.6\% lift (t = 0.59, p = 0.28). The two-channel recall architecture (editorial-authority, cultural-cult) yields an overlap coefficient of 0.80, the highest across seven substrates, indicating channel convergence in high-familiarity categories. Pre-registration, data, and scoring code are deposited at OSF (osf.io/ec6wh/v23/).

**Keywords:** AI availability, brand measurement, large language models, premium spirits, brand presence, recognition--recall gap, conglomerate ownership, AIAS

**JEL Codes:** M31 (primary); L86, L15, D83, M37 (secondary)

**Paper status:** Working paper. Pre-registered at git tag v0.23-prereg-r1 prior to data acquisition.

# 1. Introduction

The AI Availability Score (AIAS) measurement program quantifies brand visibility within large language model (LLM) outputs through a standardized two-phase protocol. Phase A measures Recognition --- whether an LLM can identify and describe a brand --- while Phase B measures Recall --- whether an LLM surfaces a brand in category-level recommendation contexts. Prior phases have examined six substrate families: kitchen knives (v0.17; Gonz\'{a}lez Castro, 2026g), kitchenware (v0.18; Gonz\'{a}lez Castro, 2026h), indie fragrance (v0.19; Gonz\'{a}lez Castro, 2026i), audiophile headphones (v0.20; Gonz\'{a}lez Castro, 2026j), skincare (v0.21; Gonz\'{a}lez Castro, 2026k), and cosmetics (v0.22; Gonz\'{a}lez Castro, 2026l). Each substrate revealed characteristic Presence distributions shaped by the interaction of training-corpus density, editorial coverage, and enthusiast-community attention.

This paper reports v0.23, which introduces premium spirits as the seventh substrate family. The selection is motivated by two structural properties of the category. First, premium spirits brands span a wide ownership spectrum --- from global conglomerates (Diageo, Pernod Ricard, Bacardi Ltd., LVMH, Brown-Forman) to independent craft producers --- enabling a direct test of whether conglomerate-scale media coverage translates into higher AI Presence. Second, the category is expected to populate both editorial-authority and cultural-cult recall channels densely, given the coexistence of a mature professional review ecosystem (Whisky Advocate, the San Francisco World Spirits Competition) and active enthusiast communities (bourbon collectors, mezcal aficionados, bartender culture).

The phase tests six hypotheses under Protocol v1.6 (Gonz\'{a}lez Castro, 2026f). Five are standard across all Presence phases: four-regime classification (H\_Regime4), recognition pre-screen gate (H\_RecognitionPrescreen), phantom brand persistence (H\_Phantom), recognition--recall correlation (H\_ILDirect), and two-channel recall divergence (H\_C2\_TwoChannel). One is substrate-specific: H\_ConglomeratePortfolio, which predicts that brands owned by top-five global spirits conglomerates exhibit higher mean AI Presence composite scores than independent brands, driven by training-corpus density from conglomerate-level media coverage.

The principal finding is structural: premium spirits is the first AIAS substrate where all 24 registry brands achieve rich recognition (R3) across all six LLMs, collapsing the Recognition axis entirely. The Presence distribution is driven exclusively by Recall --- which brands AI systems recommend, not which they can describe. This recognition ceiling exposes a recognition--recall gap with direct implications for brand strategy: six brands that LLMs can characterize in expert detail are never surfaced in recommendation contexts.

# 2. Methodology

## 2.1 Protocol and Instrument

Measurement follows AIAS Protocol v1.6 (Gonz\'{a}lez Castro, 2026f), which specifies a two-phase architecture. Phase A (Recognition) issues single-shot probes at temperature 0.0 to each model in the reference panel, requesting detailed information about a named brand within its spirit-type category. Each response is scored on a four-level scale (R0--R3) by an LLM judge (Claude Sonnet 4.5) using a standardized rubric. The substrate Recognition pre-screen gate (introduced in v1.6) flags brands scoring R0 across five or more of six models for exclusion from the composite denominator.

Phase B (Recall) issues six category-level probes --- three framed through editorial authority (critical consensus, awards authority, professional authority) and three through cultural-cult channels (enthusiast community, cultural resonance, insider discovery) --- to each model. Responses are scored for brand mention (binary), slot position (ordinal rank of first mention), and elaboration (whether the model provides at least one specific claim beyond bare mention). The two-channel architecture enables measurement of channel overlap via the C2 statistic.

## 2.2 Model Panel

The six-model reference panel has been fixed since v0.17: Claude Opus 4.5 and Claude Sonnet 4.5 (Anthropic), GPT-4o and GPT-4o-mini (OpenAI), Gemini 2.5 Flash and Gemini 2.5 Flash Lite (Google). All probes use temperature 0.0 with no conversation history carried between queries.

## 2.3 Registry

The 24-brand registry samples across 12 spirit types (Scotch, cognac, Tennessee whiskey, tequila, vodka, rum, gin, Irish whiskey, bourbon, Japanese whisky, mezcal, amaro) in three tiers: Global-dominant (8 brands), Premium-enthusiast (8 brands), and Craft-cult-emerging (8 brands). Conglomerate ownership is coded binary: brands owned by the top-five global spirits groups (Diageo, Pernod Ricard, Bacardi Ltd., LVMH/Mo\"{e}t Hennessy, Brown-Forman) are coded 1 (n = 14); all others are coded 0 (n = 10).

## 2.4 Cell Architecture

Phase A: 24 brands $\times$ 6 LLMs = 144 probes. Phase B: 6 probes $\times$ 6 LLMs = 36 queries, each scored against all 24 brands. Total measurement cells: 180.

## 2.5 Composite Scoring and Regime Classification

The composite Presence score weights three components: Recognition (0.4 $\times$ normalized mean R-level), Recall rate (0.4 $\times$ proportion of Phase B probes mentioning the brand), and inverse mean slot position (0.2 $\times$ normalized positional priority). Regime classification uses quartile thresholds on composite scores: Dominant ($\geq$ Q75), Established ($\geq$ Q50), Emerging ($\geq$ Q25), Absent (< Q25).

## 2.6 Pre-registration

Hypotheses, registry, scoring rules, and falsification criteria were pre-registered at git tag `v0.23-prereg-r1` prior to data acquisition. The pre-registration artifact is deposited at OSF (osf.io/ec6wh/v23/prereg/).

# 3. Results

## 3.1 Recognition Ceiling

All 144 Phase A probes returned R3 (rich recognition). Every brand in the 24-brand registry --- from Johnnie Walker (S01) to Mezcal Vago (S24) --- was identified with three or more accurate, specific claims by all six models. No brand triggered the pre-screen exclusion gate; zero brands were excluded from the composite denominator. This is the first AIAS substrate to exhibit a universal recognition ceiling.

The ceiling has a direct methodological consequence: with recognition mean = 3.0 for all 24 brands, the Recognition axis contributes zero discriminating variance to the composite. H\_ILDirect, which predicts a positive correlation between Recognition richness and Recall frequency (r $\geq$ 0.40, p < .05), is structurally untestable --- the Pearson correlation returns NaN on a zero-variance input. H\_ILDirect is recorded as falsified by ceiling constraint rather than by directional disconfirmation.

## 3.2 Recall Distribution and Regime Classification

Phase B generated 110 brand mentions across 36 queries. Composite Presence scores range from 40.0 (the floor value representing R3 recognition with zero recall) to 71.19. Quartile thresholds fall at Q25 = 58.28, Q50 = 64.22, and Q75 = 67.50, producing a perfectly balanced regime distribution: six brands in each of Dominant, Established, Emerging, and Absent (Figure 1).

![AI Presence Composite Score by Brand. Protocol v1.6, Premium Spirits (v0.23). All four regimes populated (6/6/6/6). Recognition at ceiling; recall drives the distribution.](../../reports/figs/v23/chart_23_composite_bar.pdf){#fig:composite width=100%}

The Dominant regime comprises Patr\'{o}n (71.19), Hendrick's (69.23), Hennessy (68.85), Fortaleza (68.84), R\'{e}my Martin (68.76), and Grey Goose (67.78). Notably, two of six Dominant brands --- Fortaleza and Hendrick's --- are coded independent under the conglomerate rule. Fortaleza, a Craft-cult-emerging tier brand, outranks every Bacardi Ltd. brand in the registry.

The Absent regime contains Bombay Sapphire, The Balvenie, Casamigos, Compass Box, Fernet-Branca, and Jameson --- all scoring composite values of 40.0 (the first five) or 57.63 (Jameson, with a single cultural-cult mention). These brands are fully characterized in AI knowledge but invisible in AI recommendation behavior.

## 3.3 Two-Channel Recall Structure

The editorial-authority channel surfaced 15 unique brands; the cultural-cult channel surfaced 16. Twelve brands appear in both channels, yielding an overlap coefficient of 0.80 --- the upper boundary of the pre-registered support range [0.30, 0.80]. H\_C2\_TwoChannel is supported, though the borderline result indicates greater channel convergence in this substrate than in prior phases.

![Recall Mentions by Channel and Brand. Editorial-Authority vs Cultural-Cult. Overlap = 0.80; channel-exclusive brands (red outlines) are exceptions.](../../reports/figs/v23/chart_23_channel_heatmap.pdf){#fig:heatmap width=100%}

Channel-exclusive patterns are the exception rather than the rule but are empirically informative. R\'{e}my Martin exhibits pure editorial-authority recall (10 EA mentions, 0 CC), consistent with the brand's prominence in spirits competition circuits and critical review publications. Jack Daniel's exhibits pure cultural-cult recall (0 EA, 5 CC), consistent with its position as a cultural icon whose recommendation pathway runs through community association rather than expert endorsement. Del Maguey skews heavily editorial (8 EA, 1 CC), suggesting that mezcal's AI recommendation pathway is mediated primarily through professional and critical channels rather than enthusiast community discussion.

## 3.4 Recall Frequency and Slot Position

Among the 18 brands with at least one recall mention, Patr\'{o}n leads on recall frequency (mentioned in 30.6\% of Phase B probes), followed by Hennessy (27.8\%), R\'{e}my Martin (27.8\%), Grey Goose (25.0\%), Hendrick's (25.0\%), Fortaleza (25.0\%), and Del Maguey (25.0\%). Slot position --- the ordinal rank at which a brand first appears in a model's response --- provides a secondary measure of recommendation priority. Lagavulin and Redbreast achieve a mean slot position of 1.0, indicating that when mentioned, they are consistently the first brand named (Figure 3).

![Recall Frequency vs Mean Slot Position. Brands with zero recall excluded (n = 18 plotted). Bubble size indicates elaboration count.](../../reports/figs/v23/chart_23_recall_scatter.pdf){#fig:scatter width=100%}

The combination of high recall frequency and early slot position characterizes the strongest AI Presence profiles: Patr\'{o}n (recall rate 0.306, mean slot 2.18) and Hendrick's (recall rate 0.250, mean slot 1.89) occupy the upper-left quadrant of the frequency--position space.

## 3.5 Conglomerate Ownership and AI Presence

H\_ConglomeratePortfolio predicted that conglomerate-owned brands (n = 14) would exhibit higher mean composite scores than independent brands (n = 10). The directional prediction holds --- conglomerate mean 60.75 versus independent mean 58.05, a 4.6\% lift --- but the difference does not reach statistical significance (t = 0.59, p = 0.28; Mann-Whitney U = 72.0, p = 0.46). The hypothesis is falsified (Figure 4).

![Composite Presence by Ownership Structure. Conglomerate (n = 14) vs Independent (n = 10). H\_ConglomeratePortfolio falsified; 4.6\% lift, not significant (p = 0.28).](../../reports/figs/v23/chart_23_conglomerate_box.pdf){#fig:conglomerate width=100%}

The result is driven in part by independent brands at the top of the distribution: Fortaleza (68.84, independent) and Hendrick's (69.23, independent) both exceed the conglomerate mean. Conversely, several conglomerate-owned brands score at or near the floor: Bombay Sapphire (40.0, Bacardi Ltd.) and Casamigos (40.0, Diageo). Conglomerate media density --- press releases, annual reports, portfolio-level coverage --- does not translate mechanically into AI recommendation behavior.

## 3.6 Hypothesis Verdicts Summary

Table 1 summarizes hypothesis outcomes for v0.23.

| Hypothesis | Verdict | Key Statistic |
|:---|:---|:---|
| H\_Regime4 | Supported | 6/6/6/6 regime split |
| H\_RecognitionPrescreen | Supported | 0 brands excluded |
| H\_Phantom | Not testable | No defunct brands in registry |
| H\_ILDirect | Falsified | r = NaN (zero recognition variance) |
| H\_C2\_TwoChannel | Supported (borderline) | Overlap = 0.80 |
| H\_ConglomeratePortfolio | Falsified | 4.6\% lift, p = 0.28 |

Table: Hypothesis verdicts, AIAS v0.23 Premium Spirits.

# 4. Discussion

## 4.1 The Recognition Ceiling as Substrate Property

The universal R3 ceiling in premium spirits marks a qualitative boundary in the AIAS measurement program. In prior substrates, recognition variance contributed meaningfully to composite discrimination --- some brands were well-known to LLMs while others were poorly characterized or confused with competitors. Premium spirits eliminates this axis entirely. The finding is best interpreted as a property of the substrate rather than a limitation of the protocol: categories with decades of editorial coverage, established competition circuits, and dense web-indexed content produce training corpora sufficient for LLMs to achieve ceiling-level knowledge of every commercially significant brand.

The methodological implication is that the AIAS composite weighting scheme --- which allocates 0.4 to Recognition --- loses discriminating power in high-familiarity substrates. Future work should evaluate whether an adaptive weighting scheme or a recall-only composite is appropriate when recognition variance falls below a predefined threshold.

## 4.2 The Recognition--Recall Gap

The most strategically consequential finding is the gap between recognition and recall. Six brands that LLMs describe in expert detail --- The Balvenie, Bombay Sapphire, Casamigos, Compass Box, Fernet-Branca, and (marginally) Jameson --- are absent from recommendation outputs. This gap is invisible to traditional brand-tracking methods that measure awareness as a unitary construct. The AIAS two-phase architecture surfaces it by design.

The Balvenie is a particularly instructive case: a highly regarded Scotch single malt with strong critic endorsement and collector following, yet it generates zero recall across both channels and all six models. The absence is unlikely to reflect low training-corpus representation --- The Balvenie is widely discussed in spirits media. A more plausible explanation is that the brand's mention context in training data is predominantly descriptive (tasting notes, distillery history) rather than recommendatory, such that LLMs encode the brand as an object of knowledge rather than an object of recommendation.

For brand strategists, this distinction reframes the competitive question: AI Presence is not a function of how much an LLM knows about a brand but of whether the brand's training-corpus footprint includes recommendation-context language --- endorsement, comparison, and category-exemplar positioning.

## 4.3 Conglomerate Scale Does Not Predict AI Recommendation

The falsification of H\_ConglomeratePortfolio challenges a plausible prior: that brands owned by global spirits conglomerates, which generate disproportionate volumes of press coverage, financial reporting, and cross-brand portfolio mentions, would accumulate greater AI Presence. The data show that this corpus-density mechanism does not operate at the recommendation layer. Conglomerate brands are recognized identically to independents (all R3), and their recall performance is statistically indistinguishable.

The finding parallels a broader pattern in the AIAS program: brand scale metrics (market share, media spend, distribution breadth) are unreliable predictors of AI Presence. What predicts recall is not volume of mentions but the recommendation valence of those mentions --- whether the brand appears in contexts where it is endorsed, recommended, or positioned as a category exemplar.

## 4.4 Channel Convergence in High-Familiarity Categories

The overlap coefficient of 0.80 --- the highest observed across seven substrates --- suggests that editorial-authority and cultural-cult channels converge when LLMs have dense training data across both. In lower-familiarity substrates, the two channels tend to surface distinct brand sets, reflecting genuine differences in which brands benefit from expert endorsement versus community enthusiasm. In premium spirits, both channels draw from the same well-documented brand universe, reducing channel-specific differentiation.

The borderline support for H\_C2\_TwoChannel raises a design question for future AIAS phases: whether high-familiarity substrates require a third recall channel (e.g., commerce-framed or availability-framed) to restore discriminating variance between recommendation pathways.

# 5. Limitations

The recognition ceiling collapses the Recognition axis and renders H\_ILDirect structurally untestable. This is a substrate property, not a protocol deficiency, but it limits the composite's discriminating power to a single component.

H\_C2\_TwoChannel's overlap coefficient of 0.80 falls at the exact upper boundary of the pre-registered support range. A threshold of 0.75 would flip the verdict from supported to falsified. The result should be interpreted as borderline.

Conglomerate coding uses a binary top-five rule. William Grant \& Sons (Hendrick's, The Balvenie), R\'{e}my Cointreau (R\'{e}my Martin), and Asahi Group (Nikka) are coded independent despite being multinational producers. Alternative coding schemes could shift H\_ConglomeratePortfolio's outcome.

The 24-brand registry is a purposive sample spanning 12 spirit types. Some types have one or two representatives, limiting subcategory-level inference. Pan-spirits breadth is purchased at the cost of within-type depth.

Recall probes name specific publications and competitions (Whisky Advocate, the San Francisco World Spirits Competition), which may anchor model responses toward brands prominent in those circuits.

LLM-as-judge scoring introduces a model-dependent layer. Recognition scoring (R0--R3) and elaboration flags are assessed by Claude Sonnet 4.5; a different judge model could produce different marginal classifications, particularly at the R2/R3 boundary where the rubric requires a count of specific claims.

# 6. Future Research

The recognition ceiling motivates a cross-substrate comparison as the AIAS program accumulates sufficient phases: which product families exhibit ceiling effects and which retain recognition variance? The boundary between these regimes --- likely related to category maturity, web-content density, and the depth of critical and editorial infrastructure --- is itself an empirical question with implications for composite design.

The recognition--recall gap invites intervention-design work. If a brand is perfectly known but never recommended, what changes in its digital content footprint --- recommendation-context language, comparison framings, category-exemplar list placements --- would shift AI recall behavior? The gap identified in this phase provides a measurement baseline against which intervention effects could be assessed in longitudinal follow-up.

Channel convergence at 0.80 overlap raises the question of whether high-familiarity substrates require additional recall channels. A commerce-framed channel or an occasion-framed channel could introduce discriminating variance that the current two-channel architecture does not capture.

The falsification of H\_ConglomeratePortfolio in a single substrate does not generalize. The hypothesis warrants testing in other substrates where ownership concentration is high (e.g., cosmetics, automotive), and where the conglomerate media-density mechanism may operate differently.

# 7. Declarations

## Conflict of Interest

The author is employed as Director, Corporate Brand Creative \& Governance at Samsung Electronics America. Samsung has no commercial relationship with any brand in the premium spirits registry. The research was conducted independently of the author's employer. The employer exercised no influence over research design, data collection, analysis, interpretation, or the decision to publish.

## Data and Code Availability

All data, pre-registration artifacts, scoring code, and the brand-format report are deposited at OSF (osf.io/ec6wh/v23/). The acquisition and scoring pipelines are available in the deposit.

## Ethics

Not applicable. The study involves no human subjects. All measurements are derived from publicly accessible LLM API outputs using standardized prompts.

## Funding

Self-funded.

# References

Gonz\'{a}lez Castro, P. U. (2026a). AI Availability: Extending Mental and Physical Availability into Algorithmic Retrieval. Working Paper. Available at SSRN: https://ssrn.com/abstract=6659000

Gonz\'{a}lez Castro, P. U. (2026b). AIAS Protocol v1.2: A Four-Regime Taxonomy for AI Brand Presence. Working Paper. Available at SSRN: https://ssrn.com/abstract=6761698

Gonz\'{a}lez Castro, P. U. (2026c). AIAS Protocol v1.3: Phase A Pivot-Validation. Working Paper. Available at SSRN: https://ssrn.com/abstract=6797679

Gonz\'{a}lez Castro, P. U. (2026d). AIAS Protocol v1.4: Multi-Component Construct. Working Paper. Available at SSRN: https://ssrn.com/abstract=6799479

Gonz\'{a}lez Castro, P. U. (2026e). AIAS Protocol v1.5: Multi-Statistic C2 and Two-Channel Recall. Working Paper. Available at SSRN: https://ssrn.com/abstract=6810758

Gonz\'{a}lez Castro, P. U. (2026f). AIAS Protocol v1.6: Substrate Recognition Pre-Screen, IL Direct, and Phantom Brand Persistence. Working Paper. Available at SSRN: https://ssrn.com/abstract=6816340

Gonz\'{a}lez Castro, P. U. (2026g). AIAS Presence Index v0.17: Kitchen Knives. Working Paper. Available at SSRN: https://ssrn.com/abstract=6802261

Gonz\'{a}lez Castro, P. U. (2026h). AIAS Presence Index v0.18: Kitchenware. Working Paper. Available at SSRN: https://ssrn.com/abstract=6806558

Gonz\'{a}lez Castro, P. U. (2026i). AIAS Presence Index v0.19: Indie Fragrance. Working Paper. Available at SSRN: https://ssrn.com/abstract=6809182

Gonz\'{a}lez Castro, P. U. (2026j). AIAS Presence Index v0.20: Audiophile Headphones. Working Paper. Available at SSRN: https://ssrn.com/abstract=6811441

Gonz\'{a}lez Castro, P. U. (2026k). AIAS Presence Index v0.21: Skincare. Working Paper. Available at SSRN: https://ssrn.com/abstract=6815378

Gonz\'{a}lez Castro, P. U. (2026l). AIAS Presence Index v0.22: Cosmetics. Working Paper. Available at SSRN: https://ssrn.com/abstract=6829118

Gonz\'{a}lez Castro, P. U. (2026m). AIAS 1.0: AI Availability Score --- Presence Component. Working Paper. Available at SSRN: https://ssrn.com/abstract=6817841
