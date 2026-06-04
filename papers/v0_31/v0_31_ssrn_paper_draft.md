---
title: "Consistency Across Categories: A Cross-Category Baseline for the AIAS™ Consistency Component (CPC)"
mainfont: "Carlito"
fontsize: 11pt
geometry: margin=1in
linkcolor: black
urlcolor: black
header-includes:
  - \usepackage{setspace}
  - \usepackage{float}
  - \usepackage{caption}
  - \usepackage{titlesec}
  - \setstretch{1.36}
  - \setlength{\parskip}{8pt}
  - \setlength{\parindent}{0pt}
  - \renewcommand{\maketitle}{}
  - \providecommand{\xmpquote}[1]{#1}
---

\begin{titlepage}
\setstretch{1.0}
\setlength{\parskip}{0pt}
\begin{center}

{\large\textbf{Consistency Across Categories:}}\\[0.3em]
{\large\textbf{A Cross-Category Baseline for the AIAS™ Consistency Component (CPC)}}

\vspace{2em}

Pablo Ulpiano González Castro

\vspace{0.8em}

SVA, MPS Branding Program, New York, NY \textit{(primary academic affiliation)}\\[0.3em]
Third System™ (research entity; data archive and methodology venue)

\vspace{0.8em}

Correspondence: pablou@pablou.com · pablou.com\\[0.2em]
ORCID: 0009-0003-8968-9990

\vspace{2em}

\textit{Working paper. Pre-registered at} \texttt{v0.31-prereg-r1}.\\[0.2em]
\textit{Retroactive rescore; no new data collection.}

\end{center}
\end{titlepage}

# Abstract {-}

Brand-growth theory locates demand in two coordinates, mental and physical availability. As discovery migrates to generative systems, a third coordinate becomes measurable: the availability of a brand inside AI outputs. The AI Availability Score (AIAS) operationalizes this coordinate as a multi-component construct. Following the Presence component (AIAS 1.0), this study establishes a cross-category baseline for Consistency (CPC), defined as the stability of a brand's cross-model recall and scored as 1 / (1 + CV). CPC is computed retroactively across five anchored substrates by rescoring committed recall data under an instrument locked in advance, generalized to a channel-agnostic per-model unit and validated by exact reconciliation against the prior methodology. Two pre-registered hypotheses, computability and cross-category difference, are both supported (Kruskal–Wallis H = 21.51, p < 0.001). Consistency varies systematically by category, lowest in premium spirits and highest in skincare, and a recognition–recall inversion in spirits places several category-dominant brands below the recall floor.

**Keywords:** AI availability; brand consistency; large language models; recall stability; coefficient of variation; cross-category measurement; Ehrenberg-Bass

**JEL:** M31 (primary); L86; L15; D83; M37

**Paper status:** Working paper. Pre-registered at `v0.31-prereg-r1`; retroactive rescore, no new data collection.

# 1. Introduction

Ehrenberg-Bass brand science explains growth through two forms of availability. Mental availability is the probability that a brand comes to mind in a buying situation; physical availability is the ease of finding and buying it. Both presuppose a human searcher moving through memory and shelf space. Generative AI systems insert a new intermediary into that path. When a category question is posed to a large language model, the model returns a bounded set of brands, and those brands are the ones a buyer is likely to consider. The availability of a brand inside these outputs is therefore a third coordinate of growth, distinct from what a buyer already recalls and from what a buyer can physically reach.

The AI Availability Score (AIAS) measures this coordinate as a multi-component construct. Its first component, Presence, asks whether a brand appears at all, and was established as a cross-category instrument in AIAS 1.0. Presence alone is incomplete. A brand that appears for one model and not another is available in a weaker sense than a brand that appears uniformly across the panel. Consistency (CPC) captures this property: the stability of a brand's recall across models, scored so that uniform recall approaches one and erratic recall approaches zero.

Before Consistency can support comparison or diagnosis it requires a baseline, and two questions precede any substantive use. First, is CPC computable on real category data, or does it collapse to a near-constant that distinguishes nothing? Second, does it vary across product categories, or is consistency an artifact of measurement rather than a property of the market? This study answers both by rescoring committed recall data from prior AIAS phases under the locked Consistency instrument. No new model queries are issued; the contribution is the first cross-category reading of an instrument whose definition was fixed in advance.

# 2. Method

This phase is a retroactive rescore. It introduces no new acquisition and draws entirely on recall data committed in earlier phases (v0.16 through v0.24), each probing twenty-four brands across a fixed model panel, with the exception of the headphone substrate, whose locked registry carries sixteen. The reference panel is the six-model set held fixed from v0.17 onward (Claude Opus 4.5, Claude Sonnet 4.5, GPT-4o, GPT-4o-mini, Gemini 2.5 Flash, and Gemini 2.5 Flash Lite).

The Consistency instrument was locked at methodology version 1.7. The signal is Phase B recall only; recognition data play no part. For each brand a per-model recall count is formed, and consistency is the reciprocal one-plus coefficient of variation of those counts, CPC = 1 / (1 + CV), with CV the standard deviation over the mean. The coefficient is taken over the panel as a whole rather than a sample, so its population form applies. A floor governs sparse signal: brands whose mean recall falls below one mention are recorded as undefined rather than zero, and the count of undefined brands is reported for each category.

Substrates differ in channel structure, which the baseline reconciles through a channel-agnostic per-model unit: the total mentions a model returns across all recall frames, irrespective of channel labeling. On a two-channel substrate this total equals the sum of the category and cultural channels, which is the locked v1.7 unit by construction, since the channels partition the frames without loss or duplication. The generalization therefore contains the locked unit as a special case rather than replacing it. A reconciliation gate enforces this identity as a precondition: recomputing consistency for the three two-channel substrates under the generalized unit reproduced the v1.7 values at exact integer-count identity across all seventy-two brands, confirming that the generalization introduces no instrument drift.

Comparability rests on measurement geometry rather than channel count. Five substrates share the same geometry, the canonical six-model panel observed over six recall frames, yielding a per-model unit on a common zero-to-six range: audiophile headphones, skincare, cosmetics, automotive, and premium spirits. These form the confirmatory set. Two further substrates, kitchenware and indie fragrance, were observed over three frames and are reported descriptively only; mixing three-frame and six-frame substrates would confound category differences with measurement granularity, so they are excluded from the cross-category test. Two substrates are excluded outright as non-comparable: kitchen knives, which used a fourteen-model legacy panel with no clean per-model recall, and B2B SaaS, which ran off the locked panel.

Two hypotheses were pre-registered. H_CPC_Computable holds that brand-level CPC exhibits non-degenerate variance within each confirmatory substrate. H_CPC_CrossCategory holds that CPC differs systematically across the five, tested by Kruskal–Wallis at the 0.05 level. A reporting rule was committed in advance: a significant or large effect is reported as scored, with no post-hoc reframing toward the null and no re-narration of direction after the result is seen. The methodology, registry, and falsification criteria were locked at git tag `v0.31-prereg-r1` before any scoring.

# 3. Results

The reconciliation gate cleared before any substantive scoring. Recomputing consistency for the three two-channel substrates (skincare, cosmetics, and automotive) under the channel-agnostic unit reproduced the locked v1.7 values at exact integer-count identity across all seventy-two brands; the only residual was negligible floating-point representation noise in the derived score. The generalization therefore carries no instrument drift, and the cross-category readings rest on the same definition fixed in the prior methodology (Figure 1).

![Reconciliation of the channel-agnostic unit against the locked v1.7 instrument across the three two-channel substrates. All seventy-two brands fall on the identity line.](../../reports/figs/v31/chart_01_reconciliation_gate.pdf){#fig:gate width=100%}

**H_CPC_Computable is supported.** Every confirmatory substrate returns a non-degenerate distribution of brand-level consistency among defined brands (Figure 2). Median CPC ranges from 0.601 in premium spirits to 0.797 in skincare, with intermediate medians of 0.667 for audiophile headphones, 0.739 for cosmetics, and 0.759 for automotive. Within-substrate spread is real rather than nominal: skincare spans 0.52 to 0.94 and automotive 0.64 to 1.00, while the tightest substrate, headphones, still spans 0.57 to 0.69. The instrument discriminates among brands in each category rather than collapsing to a constant.

![Brand-level CPC within each confirmatory substrate, defined brands only, with substrate medians and per-substrate N.](../../reports/figs/v31/chart_02_cpc_within_substrate.pdf){#fig:within width=100%}

**H_CPC_CrossCategory is supported.** A Kruskal–Wallis test across the five confirmatory substrates returns H = 21.51 at p = 0.00025, well inside the pre-registered threshold (Figure 3). Consistency varies systematically by category. Ordered by median, the categories run from premium spirits at the low end (0.601), through headphones (0.667), cosmetics (0.739), and automotive (0.759), to skincare at the high end (0.797). The editorially and culturally dense category is the least consistent and the two utilitarian categories among the most, in line with the second pre-registered prediction, reported here as scored.

![Cross-category CPC distributions across the five confirmatory substrates, with the Kruskal–Wallis statistic annotated.](../../reports/figs/v31/chart_03_cpc_cross_category.pdf){#fig:cross width=100%}

The recall floor removed a substantial share of brands in every category, and the pattern of removal is itself informative (Figure 4). Defined brands number eight of sixteen in headphones, ten of twenty-four in skincare, fourteen of twenty-four in cosmetics and in automotive, and nine of twenty-four in spirits. The composition of the spirits result departs from the first pre-registered prediction. Several of the most category-dominant brands fall below the recall floor and are undefined, including Johnnie Walker, whose mean recall is 0.17, along with Jack Daniel's, Bacardi, and Jameson. The defined set instead mixes large premium houses (Hennessy, Patrón, Grey Goose) with critically salient and craft labels (Del Maguey, Nikka, Fortaleza, Monkey 47, Hendrick's). Market dominance and recall do not coincide in this category. The supplementary substrates are reported descriptively and excluded from the test: indie fragrance returns six defined brands of twenty-four under its three-frame geometry, and kitchenware is deferred pending a category-specific brand matcher, with its panel confirmed as canonical.

![Defined and undefined brand counts per substrate under the mean-recall floor.](../../reports/figs/v31/chart_04_defined_undefined_floor.pdf){#fig:floor width=100%}

# 4. Discussion

The cross-category result establishes consistency as a property of the category rather than an artifact of the instrument. CPC separates brands within every substrate examined and separates substrates from one another, which is the minimum a measurement must do before it can support diagnosis. That the ordering follows category structure, with editorial and cultural density depressing consistency and utilitarian categories raising it, indicates that the score tracks something about how a category is discussed rather than noise in the panel.

The spirits finding is the more consequential one. The first prediction assumed that consistent recall would concentrate in the brands a category buyer would name first, that is, in the dominant incumbents. Spirits inverts this assumption at the top of the distribution. Johnnie Walker is by volume the leading Scotch in the world, yet its mean recall across the panel sits near zero in the editorial-authority and cultural-cult channels that supply the spirits signal, and it has no defined consistency at all. The same holds for Jack Daniel's, Bacardi, and Jameson. The brands that clear the floor are those the relevant discourse surfaces, whether large premium houses or smaller critical favorites, not those that lead the category by sales.

This is a recognition–recall dissociation, and it is not new to the program. The Presence work at v1.7 found the same gap in prestige skincare, where brands with high recognition were nonetheless recalled erratically. Its appearance in a second and structurally different substrate suggests the pattern is a feature of recall-based measurement rather than a quirk of one category. Recognition asks whether a model knows a brand exists; recall asks whether the model produces the brand when prompted with a category task. A brand can be universally recognized and still go unstated when the operative discourse, here the language of critics and enthusiasts, organizes itself around other names. Consistency, built on recall, registers that structure where a recognition-based reading would not. The caution is to read the result as a decoupling of dominance from recall rather than as a clean reversal of rank, since several dominant brands do clear the floor.

# 5. Limitations

This baseline is a retroactive rescore, and its reach is bounded by data gathered for other purposes. Frame counts and channel structures were set by each source phase rather than designed for a consistency reading, which is why the comparable set resolves to five substrates rather than the full anchored base; two substrates fall outside a common measurement geometry and two more carry a coarser three-frame grid. The reading is also cross-model only. Consistency across platforms, as distinct from across models within a panel, cannot be recovered from data that never observed a platform axis.

The recall floor shapes what the distributions describe. Because consistency is defined only for brands with sufficient recall, each substrate's distribution characterizes its recalled subset, not its full registry, and the defined counts are small in places, nine brands in spirits and eight in headphones. Kruskal–Wallis is robust to the unequal group sizes, but within-substrate claims rest on modest samples. Finally, the reciprocal one-plus transform is one operationalization among several; it is bounded and well behaved, but it compresses differences among high-variability brands, and a single measurement wave cannot speak to stability over time.

# 6. Future Research

Three extensions follow directly. The first is longitudinal: a second measurement wave would convert this static baseline into a test of whether consistency holds across time and across model-version transitions, which is the property a diagnostic instrument ultimately needs. The second is cross-platform consistency, measured once platform-level acquisition exists, to separate consistency within a model family from consistency across the systems a buyer actually encounters. The third is the recognition–recall dissociation surfaced here and previously in prestige skincare. Its recurrence in spirits argues for treating it as a construct in its own right rather than a category anomaly, and for mapping where in a category's discourse the gap opens.

Further work also includes the interaction of consistency with the program's existing moderators, identity load and phantom-brand persistence, and the first dissociation study pairing Presence against Consistency, which would show where a brand is present but erratically recalled, or recalled uniformly despite thin presence. Extending the instrument to the deferred and excluded substrates, under acquisition built for the purpose, would close the gap between the nominal anchored base and the comparable set.

# Declarations {-}

**Conflict of interest.** The author is employed by Samsung Electronics America in a corporate brand-creative and governance role. The research reported here is conducted independently through Third System and is self-funded; Samsung Electronics America had no role in the study's design, data, analysis, or reporting. Where an examined category includes brands owned by or affiliated with Samsung Electronics America, this is disclosed as a competing interest; a single pre-registered instrument is applied uniformly across all brands, and no brand is singled out for differential treatment.

**Funding.** Self-funded.

**Ethics.** Not applicable; no human subjects. The study uses public APIs and large-language-model prompts only.

**Data and code availability.** Pre-registration, recall data, scoring code, and figures are deposited at the Open Science Framework (osf.io/ec6wh, v31 component). The methodology was locked at git tag `v0.31-prereg-r1` prior to scoring.
