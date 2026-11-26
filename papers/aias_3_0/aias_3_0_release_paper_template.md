---
title: "Presence, Consistency and Coverage: A Three-Component Measurement of AI Availability"
subtitle: "The AIAS™ 3.0 Release: Coverage of Buying Situations Added to the Measurement"
date: "{{P:MONTH}}"
mainfont: "Carlito"
fontsize: 11pt
geometry: [letterpaper, margin=1in]
header-includes: |
  \usepackage{setspace}
  \usepackage{float}
  \usepackage{caption}
  \usepackage{titlesec}
  \usepackage{needspace}
  \usepackage{xcolor}
  \setstretch{1.36}
  \setlength{\parskip}{8pt}
  \setlength{\parindent}{0pt}
  \renewcommand{\maketitle}{}
  \widowpenalty=10000
  \clubpenalty=10000
  \usepackage{booktabs}
  \usepackage{array}
---

\begin{titlepage}
\setstretch{1.0}
\setlength{\parskip}{0pt}
\begin{center}

{\LARGE \textbf{Presence, Consistency and Coverage}}\\[6pt]
{\Large \textbf{A Three-Component Measurement of AI Availability}}\\[8pt]

{\large The AIAS™ 3.0 Release: Coverage of Buying Situations Added to the Measurement}\\[28pt]

Pablo Ulpiano González Castro\\[4pt]
School of Visual Arts, MPS Branding Program, New York, NY \textit{(primary academic affiliation)}\\
Third System™ (research entity; data archive and methodology venue)\\[8pt]
Correspondence: pablou@pablou.com · pablou.com\\
ORCID: \href{https://orcid.org/0009-0003-8968-9990}{0009-0003-8968-9990}\\[20pt]

Release pre-registration: \texttt{ {{P:PREREG_TAG}} } (commit \texttt{ {{P:PREREG_COMMIT}} }; locked {{P:PREREG_DATE}})\\
Data and code: {{P:DEPOSIT}}\\

\end{center}
\end{titlepage}

# Abstract {-}

AIAS 1.0 established Presence, how often a panel of large language models names a brand, as a measurable component of AI Availability, and AIAS 2.0 added Consistency, how evenly the models name it, reporting the two scores side by side. This release adds a third component, Coverage: in how many of a category's buying situations AI answers name the brand. Coverage Paper A (Methodology v1.12) asked {{L:a.cep_per_cat}} brand-free situation questions per category to the newest flagship model of each of three providers and defined a rate-adjusted breadth score, Cov\*; its pre-registered separability gate returned {{L:a.verdict}} (within category, ρ = {{L:a.h1.rho}} with Presence, {{L:a.h2.rho}} with Consistency, {{L:a.h3.rho}} with the brand's naming rate; split-half reliability {{L:a.h4.rel}}). Coverage Paper B (Methodology v1.19) found the score's reliability across samples of situations marginal ({{L:b.h32.rel}}), no phantom-brand signature and no replicable brand profiles, so no typology is reported. {{P:CAL_COMPOSITE_SENTENCE}} {{P:DIS_PREVIEW_SENTENCE}} {{P:RETEST_SENTENCE}} {{P:PRED_SENTENCE}} {{P:HEADLINE}} The results bind to one panel of three models, five categories and US English.

**Keywords:** AI availability; brand availability; AIAS; pre-registration; Ehrenberg-Bass; category entry points; large language models; Coverage; Double Jeopardy; measurement synthesis

**JEL codes:** M31; L86, L15, D83, M37

**Paper status:** DRAFT, pre-data (branch `aias-3.0-draft`). Synthesis of locked records plus the release's calibration and dissociation analyses under the release pre-registration {{P:PREREG_TAG}}; every statistic is taken from a locked verdict file or from the release's own outputs at its data lock ({{P:DATA_LOCK_TAG}}); deviations recorded in `anchor/DEVIATIONS.md` ({{P:DEVIATIONS_COUNT}} dated entries). Part of the AIAS measurement programme.

# 1. Introduction

AI Availability --- the discoverability and representation of a brand in the outputs of large language models (LLMs) --- has been proposed as a third measurable layer of brand availability (González Castro, 2026, SSRN 6659000), beside the Mental and Physical Availability of the Ehrenberg-Bass tradition (Sharp, 2010; Romaniuk & Sharp, 2016), within the Tri-System framework (González Castro, 2026, MSI Working Paper 26-132). The AIAS programme adds components one at a time and releases a component only after it has passed a pre-registered separability gate, a second paper of robustness and structure tests, and a calibration that decides how it is reported beside the components already released. AIAS 1.0 (SSRN 6817841) released Presence. AIAS 2.0 (SSRN 7717659) released Consistency and reported the two scores side by side, because no combined score both added information to Presence and kept Consistency separate from it.

The programme's release rule, set on 12 November 2026, gives each remaining part the next release number when it passes its gate. Ranking did not pass (it is reported as part of Presence; Methodology v1.14 and v1.16). Coverage passed its gate on 14 November 2026 and is the third component released.

Coverage carries the Ehrenberg-Bass idea of category entry points into AI answers. A buyer meets a category in situations, and the number of situations a brand is linked to is a core part of its Mental Availability (Romaniuk & Sharp, 2016). The analogue for AI answers is whether a brand is named across a category's buying situations or only in a few. The difficulty, known before any data, is Double Jeopardy: bigger brands are linked to more situations, so a raw count of situations would follow Presence, and a component built on it would repeat the failure of the programme's first Consistency instrument (Methodology v1.7). Coverage Paper A therefore defined a rate-adjusted breadth, Cov\*, and tested it against Presence, Consistency and the brand's own naming rate.

This paper reports the release. Section 3 sets out the corpus, the three scores and the tests; Section 4 gives the evidence: the gate (Paper A), robustness and structure (Paper B), the calibration of three scores, the dissociation of the three, Coverage over time and predictive validity; Section 5 states the AIAS 3.0 construct; Sections 6 and 7 discuss it and its limits.

# 2. Theoretical positioning

Category entry points are the cues that bring a category, and then a brand, to mind in a buying situation (Romaniuk & Sharp, 2016). Their count per brand follows Double Jeopardy, so a brand's linkage is best read against what its size predicts rather than as a raw count. Cov\* follows the same logic inside each model's answers: a brand's breadth across situations is read against the breadth expected from its number of mentions alone (Section 3.3).

AIAS reports each component as its own score and adds a combined score only if one passes its pre-registered tests (AIAS 2.0). The Tri-System framework (MSI Working Paper 26-132) treats AI answers as a route by which brands come to mind and to hand; Coverage asks whether that route opens across a category's situations or only in some.

# 3. Corpus, scores and tests

## 3.1 Corpus and panel

The corpus is the programme's five-category omnibus: audiophile headphones, skincare, cosmetics, automotive and premium spirits, with the brand registries fixed in v0.19--v0.23, unchanged. The panel is N3, the newest generally available flagship of each of three providers (Claude Fable 5.2, GPT-6 Astra, Gemini 4 Argon), search off. Presence and Consistency on N3 come from the fourth omnibus wave, $t_4$ (v0.42); Coverage comes from Paper A's own situation questions to the same models in the same week (Paper A: {{L:a.answered}} of {{L:a.expected}} calls answered, Claude Opus 5.5 included for continuity).

## 3.2 Presence and Consistency, and the bridge from AIAS 2.0

AIAS 2.0's scores were measured on a six-model panel that is retiring. On the newest models (v0.42), recall Presence kept the brand order of the older panel (ρ = {{L:g.p.rho}}, n = {{L:g.p.n}}, {{L:g.p.v}}), while the order by Consistency held only partly (ρ = {{L:g.phi.rho}}, n = {{L:g.phi.n}}, {{L:g.phi.v}}). After the coding correction of 25 November 2026, which read the typographic apostrophe in two brand names ({{L:g.err.cells}} answer cells), these values are {{L:g.p.rho_corr}} and {{L:g.phi.rho_corr}}, with both verdicts unchanged (v0.42 erratum). {{P:CAL_BRIDGE_SENTENCE}}

## 3.3 Coverage

Coverage Paper A fixed {{L:a.cep_per_cat}} buying situations per category, two for each of seven cue types, each asked as a brand-free question. For each brand and model, Cov\* compares the number of situations in which the brand is named with the number expected if the brand were named without regard to the situation, given the same number of mentions, and scales the difference so that situation-blind naming scores 50. Cov\* is rated only when the panel's mentions of a brand total at least {{L:a.floor}} and at least two models name it; {{L:a.rated}} brands met the floor. {{P:CAL_RULE}}

## 3.4 The release's analyses

Three analyses complete the release; each is pre-registered in {{P:PREREG_TAG}}, locked before its inputs were read.

*Calibration of three scores.* As Methodology v1.9 did for two scores, the calibration asks whether Cov\* keeps its scale and rating rule beside Presence and Consistency, and whether any combination of the three both adds information to Presence and keeps each component separate. The candidates ({{P:CAL_N_CANDIDATES}}) and the rules are those of the release pre-registration.

*Dissociation of the three scores.* Presence, Consistency and Coverage are compared on the same brands, models and week, pair by pair and each against the other two together. {{P:DIS_PREVIEW_SENTENCE}}

*Predictive validity.* Under the rule of the programme's predictive-validity study (v0.43, §2.6), a component that passed its gate enters that study's prospective stage by a dated amendment, with the outcome, windows, statistic and verdict rule unchanged. The outcome is the change in each brand's US search interest to the four weeks ending {{L:pv.s2.window_end}}, measured from pulls no earlier than {{L:pv.s2.first_pull}}. {{P:PRED_SENTENCE}}

## 3.5 Pre-registration chain

Coverage Paper A was locked at tag `v1.12-prereg-r1` and deposited on OSF before its first call; Paper B at `v1.19-prereg-r1`, before Paper A's first call. The release pre-registration {{P:PREREG_TAG}} (commit {{P:PREREG_COMMIT}}, {{P:PREREG_DATE}}) fixes the calibration and dissociation analyses and the wording of this paper's headline for every possible outcome, in the form of the AIAS 2.0 outline; the outcome set the wording class {{P:CLASS}}. Deviations: {{P:DEVIATIONS_COUNT}} dated entries.

# 4. Evidence

## 4.1 Coverage passes its gate (Paper A)

The situations changed which brands were named: brand sets overlapped more between runs of one question than between questions by {{L:a.msit}} in Jaccard similarity, so the instrument check passed. Every gate leg was confirmed (Table 1), and the gate returned {{L:a.verdict}}. Raw coverage, the unadjusted share of situations, followed the naming rate as Double Jeopardy predicts; Cov\* did not.

Table: Coverage Paper A gate legs on panel N3, search off (v1.12 verdict file; pooled within-category Spearman $\rho_w$; bands: separate at $|\rho_w| \leq$ {{L:a.band.conf}}, overlapping at $\geq$ {{L:a.band.fals}}).

| Cov\* against | $n$ | $\rho_w$ | Verdict |
|:--------------------------|----:|-------:|:------------|
| Presence $P_{N3}$ | {{L:a.h1.n}} | {{L:a.h1.rho}} | {{L:a.h1.v}} |
| Consistency $C^*_{N3}$ | {{L:a.h2.n}} | {{L:a.h2.rho}} | {{L:a.h2.v}} |
| the brand's naming rate | {{L:a.h3.n}} | {{L:a.h3.rho}} | {{L:a.h3.v}} |
| the other half of the situations (reliability) | {{L:a.h4.n}} | {{L:a.h4.rel}} | {{L:a.h4.v}} |
| Cov\* on a second panel (replication) | {{L:a.h8.n}} | {{L:a.h8.rho}} | {{L:a.h8.v}} |

![Pooled within-category $\rho_w$ of Cov\* with each comparator, with bootstrap intervals and the separability bands (Coverage Paper A, Figure 2, unchanged). ](../../reports/figs/v112/chart_02_legs_bands.pdf){#fig:gate width=96%}

Against the published AIAS 2.0 Presence of the older panel, Cov\* correlated at {{L:a.h7.rho}}; against Ranking, which is reported as part of Presence, at {{L:a.h5.rho}}.

## 4.2 Robustness and structure (Paper B)

Over the {{L:b.h32.splits}} balanced ways of halving the situations, the split-half reliability of Cov\* from the median correlation was {{L:b.h32.rel}}, and the tenth percentile of the per-split reliabilities {{L:b.h32.p10}}; the set-sampling test was {{L:b.h32.v}}. Paper A's own split lies at the {{L:b.h32.pct}}th percentile of the splits. Dropping one cue type moved the order beyond the reference range for {{L:b.cue.count}} of seven cue types ({{L:b.cue.v}}).

![Split-half reliability of Cov\* for each balanced split of the situations, sorted (Coverage Paper B, Figure 1, unchanged). ](../../reports/figs/v119/chart_01_split_reliability.pdf){#fig:split width=92%}

## 4.3 What Coverage is not

Brands below the programme's recall floor were not more situation-bound by Cov\* (Cliff's δ = {{L:b.floor.delta}}; {{L:b.floor.resid}} after Presence; {{L:b.floor.v}}), and no automotive answer named a defunct brand ({{L:b.defunct.naming}} of {{L:b.defunct.answers}}). Identity load could not be tested ({{L:b.il.n}} eligible brands against a floor of {{L:b.il.floor}}; {{L:b.il.v}}). A brand's lean towards a kind of situation did not repeat in the other situation of the same kind (mean ρ = {{L:b.prof.R}}, n = {{L:b.prof.n}}; {{L:b.prof.v}}), so no typology is reported: {{L:b.typology}}. Coverage is released as a single breadth score.

## 4.4 Calibration of three scores

{{P:CAL_COMPOSITE_SENTENCE}} The best candidate ranked brands with a correlation of {{P:CAL_RHO_AP}} to Presence. Cov\* is rated for a share of {{P:CAL_SHARE_RATED}} of the brands under the selected rule. AIAS 2.0's no-composite result is the reference: on the older panel the descriptive combined score ranked brands at {{L:z.nocomp.rho}} to Presence, against a line of {{L:z.nocomp.k2}}.

{{P:FIG_CALIBRATION}}

## 4.5 Three scores on the same brands

{{P:DIS_PREVIEW_SENTENCE}} Pairwise, Presence and Coverage correlated at {{P:DIS_RHO_P_COV}} and Consistency and Coverage at {{P:DIS_RHO_C_COV}}; against Presence and Consistency together, Coverage gave {{P:DIS_JOINT}} ({{P:DIS_N}} brands rated on all three). Verdict: {{P:DIS_VERDICT}}. For reference, AIAS 2.0 kept Consistency separate from Presence on the older panel (ρ = {{L:z.dis.rho}}, n = {{L:z.dis.n}}).

{{P:FIG_DISSOCIATION}}

## 4.6 Coverage over time

{{P:RETEST_SENTENCE}} AIAS 2.0 tested both of its scores over five months (Presence ρ = {{L:z.prel.rho}}, n = {{L:z.prel.n}}; Consistency ρ = {{L:z.crel.rho}}, n = {{L:z.crel.n}}). Coverage has one wave: the programme's three-week retest wave ($t_5$, from {{L:t5.window}}) carries {{L:t5.no_cov}}, and the next wave ($t_6$) is targeted for {{L:t6.target}}.

## 4.7 Predictive validity

The programme's first predictive test, on past data, read Presence and Consistency against later change in search interest: the Presence hypothesis was {{L:pv.s1.presence}} and the Consistency hypothesis {{L:pv.s1.consistency}} (v0.43, Stage 1). The Coverage amendment to the prospective stage was deposited on {{P:PRED_AMENDMENT_DATE}}. {{P:PRED_SENTENCE}}

# 5. The AIAS 3.0 construct

*Claim 1 --- three components, reported as a profile.* {{P:HEADLINE}}

*Claim 2 --- Coverage is breadth across buying situations, read against size.* Cov\* measures how widely a brand's naming spreads over a category's situations against situation-blind naming with the same number of mentions; it is rated only where there are enough mentions to rate.

*Claim 3 --- Coverage is separable from Presence and Consistency.* Governed by the Paper A gate ({{L:a.verdict}}) and the release's dissociation study ({{P:DIS_VERDICT}}).

*Claim 4 --- reliability.* Across halves of the situations Paper A's split gave {{L:a.h4.rel}}; across all splits, Paper B's median gave {{L:b.h32.rel}} ({{L:b.h32.v}}). {{P:RETEST_SENTENCE}}

*Claim 5 --- no typology and no phantom signature.* Paper B (Section 4.3).

*Claim 6 --- combined score.* {{P:CAL_COMPOSITE_SENTENCE}}

# 6. Discussion

Coverage adds a reading that Presence cannot give: two brands named equally often can differ in whether that naming spreads across buying situations. The release's evidence that Cov\* is separate is strong on one week of answers; its evidence of precision is moderate, because the score's reliability depends on which situations are sampled (Paper B). {{P:CAL_BRIDGE_SENTENCE}} {{P:APOS_SENTENCE}}

# 7. Limitations

One set of situations per category, drafted by one procedure and by a model that is also a panel model; reliability across samples of situations was marginal (Paper B). Coverage is measured on registry brands only, in US English, search off, on one panel of three models. {{P:RETEST_SENTENCE}} Behavioural validity: {{P:PRED_SENTENCE}} {{P:APOS_SENTENCE}}

# 8. Future research

An independently written parallel set of situations with buyer weights and a test of question wording (Coverage studies #32b and #33) need their own collections; Coverage with search on belongs with the programme's Grounding component; the AIAS 4.0 and 5.0 releases add the remaining parts in the order their gates pass.

# Declarations {-}

## Conflict of interest {-}

This release selects no brands and makes no new collection of its own beyond what its pre-registration states; it reads the records of Coverage Papers A and B, whose conflict-of-interest declaration applies unchanged and is reproduced here from Paper A (Methodology v1.12, revision of November 2026).

{{L:coi.v112}}

## Funding {-}

Self-funded. No external funding supported this research.

## Ethics {-}

Not applicable; no human subjects. The study queries large language models under their public interfaces.

## Use of AI tools {-}

During the preparation of this work the author used AI tools (Anthropic's Claude) to assist with study design, analysis and writing. The author reviewed and edited all content and takes full responsibility for it.

## Data and code availability {-}

Release pre-registration, outputs, data lock and deviations record: {{P:DEPOSIT}}. Coverage Paper A: OSF `ec6wh`, `methodology/v1_12/`; Paper B: OSF `ec6wh`, `methodology/v1_19/`. Code: github.com/thirdsystem-aias/aias, tag {{P:PREREG_TAG}}.

# References {-}

González Castro, P. U. (2026). *AI Availability: Extending Mental and Physical Availability into Algorithmic Retrieval*. SSRN 6659000.

González Castro, P. U. (2026). *Tri-System Brand Growth: The AI Mediation Layer*. MSI Working Paper, Report No. 26-132. Marketing Science Institute.

González Castro, P. U. (2026). *The AIAS™ Presence Measurement Protocol: Methodological Notes on Construct Validity and the Four-Regime Taxonomy* (v1.2). SSRN 6761698.

González Castro, P. U. (2026). *The AIAS Presence Measurement Protocol: Phase A Pivot-Validation Specification (v1.3)*. SSRN 6797679.

González Castro, P. U. (2026). *The AIAS Presence Measurement Protocol v1.4: Recognition × Recall Decomposition and Multi-Component AI Availability*. SSRN 6799479.

González Castro, P. U. (2026). *The AIAS™ Presence Measurement Protocol: Multi-Statistic C2 Specification and Two-Channel Recall Decomposition* (v1.5). SSRN 6810758.

González Castro, P. U. (2026). *Substrate Pre-Screening, Independent Moderator Pathway, and Phantom Brand Persistence Phase B Extension* (AIAS Methodology v1.6). SSRN 6816340.

González Castro, P. U. (2026). *Consistency without Independence: A Pre-Registered Test of Coefficient-of-Variation as the Consistency Component of AIAS™* (v1.7). SSRN 6878818.

González Castro, P. U. (2026). *A Mean-Independent Consistency Instrument for Cross-Model AI Presence: Redesigning CPC on a Quasi-Binomial Dispersion Basis* (AIAS Methodology v1.8). SSRN 6963359.

González Castro, P. U. (2026). *One Score or Two? Calibrating a Presence and Consistency Composite for AI Brand Availability: A Pre-Registered Calibration with Blind Five-Month Confirmation (AIAS™ Methodology v1.9)*. Third System, <https://thirdsystem.ai/studies/v1-9/>; OSF, <https://osf.io/ec6wh/files/osfstorage/6af1fd459966c813ee53ba87>.

González Castro, P. U. (2026). *Coverage of Buying Situations in AI Answers about Brands: Instrument, Cross-Category Baseline and Separability Gate for a Third Component of AI Availability* (AIAS™ Methodology v1.12). Third System, <https://thirdsystem.ai/studies/v1-12/>; OSF `ec6wh/methodology/v1_12`.

González Castro, P. U. (2026). *Situation Sampling, Phantom Brands, Identity Load and Brand Profiles in AI Coverage Answers* (AIAS™ Methodology v1.19). Third System, <https://thirdsystem.ai/studies/v1-19/>; OSF `ec6wh/methodology/v1_19`.

González Castro, P. U. (2026). *Precedence Without Separation* (AIAS Methodology v1.14 and v1.16). Third System; OSF `ec6wh/methodology/v1_14_16`.

González Castro, P. U. (2026). *Cross-Generation Stability of AI Brand Presence and Consistency* (v0.42). Third System; OSF `ec6wh/v42`.

González Castro, P. U. (2026). *AI Availability Scores and Later Change in Brand Search Interest* (v0.43). Third System; OSF `ec6wh/v43`.

González Castro, P. U. (2026). *AI Availability as a Third Measurable Layer of Brand Availability: Five-Substrate Empirical Anchoring of the AIAS™ Presence Measurement Protocol --- Synthesis under Locked v1.6 Methodology* (AIAS 1.0). SSRN 6817841.

González Castro, P. U. (2026). *Presence and Consistency: A Two-Component Measurement of AI Availability. The AIAS™ 2.0 Synthesis*. SSRN 7717659.

Romaniuk, J., & Sharp, B. (2016). *How Brands Grow: Part 2*. Oxford University Press.

Sharp, B. (2010). *How Brands Grow: What Marketers Don't Know*. Oxford University Press.
