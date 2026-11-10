---
title: "Where a Brand Sits in an AI Answer: A Reliable Ranking Instrument That Does Not Pass Its Separability Gate"
subtitle: "Ranking, Paper A: Pre-Registered Instrument Specification, Cross-Category Baseline and a MARGINAL Separability Gate (AIAS™ Methodology v1.10)"
date: "November 2026"
mainfont: "Carlito"
fontsize: 11pt
geometry: [letterpaper, margin=1in]
header-includes: |
  \usepackage{setspace}
  \usepackage{float}
  \usepackage{caption}
  \usepackage{titlesec}
  \usepackage{needspace}
  \setstretch{1.36}
  \setlength{\parskip}{8pt}
  \setlength{\parindent}{0pt}
  \renewcommand{\maketitle}{}
  \providecommand{\xmpquote}[1]{#1}
---

\begin{titlepage}
\setstretch{1.0}
\setlength{\parskip}{0pt}
\begin{center}

{\LARGE \textbf{Where a Brand Sits in an AI Answer: A Reliable Ranking\\ Instrument That Does Not Pass Its Separability Gate}}\\[8pt]

{\large Ranking, Paper A: Pre-Registered Instrument Specification, Cross-Category Baseline\\ and a MARGINAL Separability Gate (AIAS™ Methodology v1.10)}\\[28pt]

Pablo Ulpiano González Castro\\[4pt]
School of Visual Arts, MPS Branding Program, New York, NY \textit{(primary academic affiliation)}\\
Third System™ (research entity; data archive and methodology venue)\\[8pt]
Correspondence: pablou@pablou.com · pablou.com\\
ORCID: 0009-0003-8968-9990\\[20pt]

Pre-registration: \texttt{v1.10-prereg-r2} (deposited on OSF before any rank statistic was computed on confirmatory data)\\
Materials: OSF \texttt{ec6wh/methodology/v1\_10}\\

\end{center}
\end{titlepage}

# Abstract {-}

The AIAS™ program measures AI brand availability with two validated components, Presence (how often a fixed panel of language models names a brand) and Consistency (how evenly the models name it). This paper tests a third: Ranking, where a brand sits in an answer's list of brands, given that it is named. A deterministic extractor recovered positions from 3,766 archived answers with text (100% parsed; mention sets identical to the certified Presence detectors). A rank statistic was selected by a pre-registered rule on a separate panel, blind to Presence and Consistency: mean normalised position (MNP), with split-half reliability 0.951 over 138 brands in nine categories, which fell to $-0.017$ when brand order was shuffled within answers. The confirmatory gate ran on five categories and three waves of a six-model panel (52--55 rated brands per comparison). Ranking is separable from Consistency (pooled within-category $\rho$ = 0.252, 0.119, 0.142; CONFIRMED) and holds its brand order over three weeks far beyond what list composition produces ($\rho$ = 0.897, both nulls $p$ = 0.0001; CONFIRMED) and over five months ($\rho$ = 0.846). It is not cleanly separable from Presence: $\rho(R^*, P)$ = 0.275, 0.366 and 0.307, inside the confirmation band at the first wave only (MARGINAL). On the early panel, Ranking tracked recall share at $\rho$ = 0.663 (FALSIFIED). The gate is therefore MARGINAL: the program does not add Ranking as a component on this evidence, and a Paper B proceeds only on the author's recorded decision, with separability from Presence as its first confirmatory test. Brands that models name more often tend to be named earlier.

**Keywords:** AI availability; brand availability; AIAS; pre-registration; Ehrenberg-Bass; large language models; ranking; list position; separability; measurement reliability

**JEL codes:** M31; L86, L15, D83, M37

**Paper status:** Pre-registered methodology study (tag `v1.10-prereg-r2`). Re-analysis of archived answers: no new data collection and no model calls. The statistic was selected (Stage S) after the lock, blind to Presence and Consistency; the confirmatory gate (Stage C) ran once, after the conflict-of-interest re-check was logged and anchored (DEVIATIONS Entry 2). Gate verdict: MARGINAL (not passed). Part of the AIAS measurement program.

# 1. Introduction

AI Availability --- the discoverability and representation of a brand in the outputs of large language models --- has been proposed as a third measurable layer of brand availability (González Castro, 2026, SSRN 6659000), beside the Mental and Physical Availability of the Ehrenberg-Bass tradition (Sharp, 2010; Romaniuk & Sharp, 2022). The Tri-System framework describes the AI Availability Score (AIAS) as a 0--100 score built from several dimensions (MSI Working Paper 26-132). The program has validated two of them. Presence, how often a fixed panel of models recognizes and names a brand, was anchored across five product categories under the v1.6 protocol (SSRN 6816340; AIAS 1.0, SSRN 6817841). Consistency, whether the panel's models agree about a brand, reached a usable instrument only after its first version was falsified for moving with recall (v1.7, SSRN 6878818) and replaced by the mean-independent dispersion statistic $\varphi$ (v1.8, SSRN 6963359). The v1.9 calibration found that no composite of the two carried information Presence did not, and locked the reporting of two scores side by side (SSRN 7685126). The AIAS 2.0 synthesis reports them that way and shows them separable: within category, $|\rho(C^*, P)|$ = 0.073, 0.082 and 0.189 at the three waves, as published.

This paper opens the third component. Ranking is where a brand sits in an answer's ordered list of brands, *given that the brand is named*. Whether a brand is named at all is Presence's information; how evenly the models name it is Consistency's. A third component is worth adding only if it carries information neither of the first two carries, and the program's own record shows how easily that condition fails: the first Consistency instrument was reliable and looked plausible, yet it largely re-expressed recall (pooled $\rho$ = 0.766 against a 0.50 ceiling; v1.7). Ranking faces a specific version of that risk. In consumer markets, brands with more buyers also tend to score higher on loyalty and attitude measures (the Double Jeopardy pattern; Ehrenberg, Goodhardt & Barwise, 1990), and the brands a model names most often may also be the ones it names first. If so, a ranking score would add little to Presence.

The study is the first of two papers on Ranking, following the program's plan for each new component: Paper A specifies the instrument, describes it across categories and subjects it to a separability gate; Paper B, on robustness and structure, follows only if Paper A passes. Paper A has three parts. First, a deterministic, registry-based extractor recovers each named brand's position in archived long-form answers, lists and prose alike (§2). Second, a rank statistic is chosen from six candidates by a rule fixed in advance, on a separate panel and blind to Presence and Consistency (Stage S, §5). Third, a confirmatory gate tests whether the selected score is separable from Presence and from Consistency, and whether it holds its brand order over three weeks beyond what list composition alone produces (Stage C, §6).

All data already exist: 3,658 confirmatory-period answers on three model panels across fourteen category sets, collected between April and November 2026 for earlier studies. Because Presence and Consistency for the gate's units are published, the design fixes the order of operations in code: the scorer refuses to run before the pre-registration is tagged and anchored, it selects the statistic before it may open the Presence and Consistency table, and it halts on any change to a frozen input (§4).

The gate returned MARGINAL, and Ranking is not added to the program's reported components on this evidence. The instrument itself works: it extracts positions without discretion, its selected score is highly reliable, and that reliability is a property of position, not of which brands share a list. The score is separable from Consistency and stable over three weeks and five months. What it does not do is stay clear of Presence: at two of three waves its within-category correlation with Presence lies between the confirmation and falsification bands, and in the early panel it tracks recall share closely enough to be falsified there. The paper's contribution is that measured result, which locates the Double-Jeopardy-like risk the pre-registration named, together with a locked extractor, hashed rank tables and a cross-category description of where models place brands, which a redesign or a Paper B can build on.

# 2. The instrument

## 2.1 Construct and unit

The unit of extraction is one answer: one model's response to one prompt in one run (rule E0). Empty answers, API errors and rows without text are missing cells; they enter no denominator and are never read as "no brand named". The unit of scoring is the brand within a panel, wave and category.

## 2.2 Extraction rules E1--E7

The extractor is implemented in `scripts/score_v1_10.py` and covered by 61 unit tests. It applies the rules of the pre-registration (§4) without discretion:

- **E1 Normalisation.** Unicode NFKD, combining marks removed, lower case (the v1.4 canonical form). All offsets are taken on the normalised text.
- **E2 Detection.** Each phase's own registry supplies canonical names and aliases. The pattern is a word-bounded match of each alias, identical to the certified Presence detectors, including their known edge cases, so that the set of brands named in an answer is exactly the set Presence counted. Brands outside the registry are not ranked. No named-entity recognition and no model-based extraction are used.
- **E3 List items.** A list item is a line indented at most three spaces that starts with a number, a bullet, a Markdown heading or a bold run. Top-level items are headings plus the item lines at the smallest indentation; deeper lines belong to their parent item.
- **E4 Repeats.** Only a brand's first occurrence fixes its first-mention offset. A brand *leads* a list item when its earliest match in the item precedes every other registry brand's match in that item.
- **E5 Rankable answers.** An answer is rankable if it names at least two registry brands.
- **E6 Position (primary rule, "lead-item").** An answer is list-structured if at least two of its top-level items are led by a registry brand. In a list-structured answer, brands are ordered by the first item they lead, and brands that lead no item follow in first-mention order; otherwise brands are ordered by first mention. The first-mention rule in every answer is sensitivity S1.
- **E7 Ties.** Brands with equal sort keys receive the mid-rank $k_{\text{mid}}$ and the competition min-rank $k_{\min}$.

For each named brand in a rankable answer the extractor records $k_{\text{mid}}$, $k_{\min}$, the number $n$ of registry brands named, and the normalised position $q = (k_{\text{mid}} - 1)/(n - 1) \in [0, 1]$, where 0 is first.

## 2.3 Candidate statistics

For brand $b$ in category $c$, over its rankable answers $A_b$, six candidates were fixed in advance, each oriented so that higher means nearer the top:

| Id | Statistic | Definition |
|:-----|:-------------------------------|:----------------------------------------------|
| MNP | mean normalised position | $100\,(1 - \overline{q})$ over $A_b$; 100 = always first |
| IRW | inverse-rank weight | mean of $1/k_{\text{mid}}$ |
| TOP3 | top-3 share | share of $A_b$ with $k_{\min} \le 3$ |
| MR | mean rank | minus the mean of $k_{\text{mid}}$ |
| TOP1 | named-first share | share of $A_b$ with $k_{\min} = 1$ |
| MODE | modal rank | minus the smallest modal $k_{\min}$ |

A brand's Ranking score is rated ($R^*$) only with at least six rankable mentions in that panel, wave and category, the floor v1.9 fixed for Consistency. Brands never named are not rated: absence is Presence's information, not a position, and no penalty rank is imputed in any confirmatory statistic. A penalised variant that scores unnamed brands as last exists only as a positive control (MQ6), because it builds Presence into Ranking by construction.

# 3. Data

## 3.1 Frozen sets

Every file the scorer reads is pinned in an input manifest (111 files, each with its git blob and SHA-256; base commit `894ccee`), and the scorer halts on any mismatch.

**Gate set (OMNI).** The five omnibus categories of the program --- audiophile headphones (v0.19, 16 brands), skincare (v0.20), cosmetics (v0.21), automotive (v0.22) and premium spirits (v0.23), 24 brands each; 112 brand units --- measured on the six-model legacy panel (Claude Opus 4.5, Claude Sonnet 4.5, GPT-4o, GPT-4o mini, Gemini 2.5 Flash, Gemini 2.5 Flash Lite) at three waves: $t_1$ (20--26 May 2026), $t_2$ (10 June 2026, v0.34) and $t_3$ (9 November 2026, v0.41). Only the free-recall frames are used (three category and three cultural frames per model: 36 answers per category per wave, 540 in all). Presence ($P$) and Consistency ($C^*$) for these units are read from the published AIAS 2.0 profiles table (336 rows = 112 units $\times$ 3 waves).

**Selection and replication set (EARLY-6).** Nine early category studies on a second panel (Claude Sonnet 4.6, Claude Opus 4.7, GPT-5.4 mini, GPT-5.5, Gemini 2.5 Flash, Grok 4.1 Fast): PM software, personal finance, olive oil, running shoes and skincare (v0.9, SSRN 6736878), household retail (the v0.7 study, SSRN 6721779; registry v1.0) and knives (the v0.8 study, SSRN 6728000; registry v1.0), premium tea (v0.14, SSRN 6755621) and kitchen knives (v0.16, SSRN 6791999). The household and knives sets are labelled "v1.0" after their registry version, as in the pre-registration. Six prompt types $\times$ six models $\times$ eight runs give 288 answers per set; kitchen knives used 11 prompts in three groups and has 334 answers with text in 515 rows. In all, 2,638 answers with text. Each set is read with the registry its source phase's extraction applied.

**Other sets.** EARLY-2 (the v0.6 cross-category baseline: two of the EARLY-6 models, five categories, 480 answers) enters the early-stability test H6 and the baseline. The v0.28 technology answers (36) are pinned and parse-checked only, pending their own conflict-of-interest screen. The v0.32 model-version arms (72 answers) are frozen for Paper B and not analysed here. The development sample used for the declared parsing-feasibility note (v0.17 and v0.18, 36 answers) is excluded from every confirmatory analysis, as are the sets listed in pre-registration §2.5.

## 3.2 Data quality before Stage S

The checks MQ1--MQ5, MQ8 and MQ9 ran on the real files after the lock and before any statistic (`outputs/stage_s_v1_10.json`):

- **MQ1 parse completion.** The extractor completed on 100% of answers with text in every set. Rankable shares: OMNI 483 of 540 answers (0.894; lowest v0.23, 0.639--0.667 by wave); EARLY-6 2,388 of 2,638 (0.905; lowest v0.9 skincare, 0.760); EARLY-2 427 of 480 (0.890). No set fell below the 0.50 flag.
- **MQ2 mention parity.** The extractor's named sets matched the certified Presence detectors on 864 of 864 cells for each of v0.20--v0.22 at every wave, and the coded mention files on 576 of 576 (v0.19) and 864 of 864 (v0.23) at every wave: agreement 1.0000 throughout. No category left the gate.
- **MQ3 concordance.** On the five v0.9 sets, the EARLY-6 sets for which the archived model-extracted ranking was available to the check, the median per-answer Kendall $\tau$ between the lead-item order and the archived order was 1.0.
- **MQ4 missing cells.** None in OMNI (36 of 36 per category and wave) or in eight of the nine EARLY-6 sets. Kitchen knives (v0.16): 181 of 515 rows without text (final transient-error status) and 13 of its 528 design cells without a row; listed, never imputed.
- **MQ5 overlap and aliases.** Nested matches occur in v0.9 personal finance (81 events in 44 answers), v0.6 personal finance (19 in 13) and kitchen knives (21 in 21). The two knife registries carry ordinary-word aliases (*global*, *mac*, *made in*; the kitchen-knives adapter also *dick*, *kramer*, *new west*); two of the adapter's canonical names end in a parenthesis and cannot match; the v0.23 registry has two aliases ending in an apostrophe. All are listed, not fixed, so that Ranking counts exactly the mentions Presence counted.
- **MQ8 prompt parity.** v0.6 and v0.9 share identical prompt ids and texts in all five categories, so H6 runs.
- **MQ9 truncation.** No analysed set stores finish reasons or the token cap; positions before any cut are valid.

# 4. Pre-registration and order of operations

The pre-registration was drafted, its open questions settled on 10 November 2026, and its content locked at tag `v1.10-prereg-r1`, pushed and deposited on OSF. The first Stage S run halted at manifest verification because the input manifest pinned a documentation file at its hash from before the content lock; no extraction had run. The input manifest was rebuilt, the lock moved to tag `v1.10-prereg-r2` (commit `db93819`), the anchor record (`anchor/git_anchor_v1_10.json`: tag object, commit, tree, time and the SHA-256 of every locked file) was committed, and the deposit was repeated (DEVIATIONS Entry 1). No rule, threshold, seed, input file or analysis step changed.

The scorer enforces the order of operations: manifest verification; rank extraction on every frozen set, with each per-answer rank table written and hashed; the data-quality checks; Stage S on early-panel rank tables only, writing a hashed selection file; and only then Stage C, whose first act re-extracts every set, checks that the rank tables are byte-identical to the Stage S tables, and joins the gate's units 1:1 to the Presence and Consistency table. The function that reads $P$ and $C^*$ refuses to run before the selection file exists.

The deviations record has three entries. Entry 0, written before the lock, carries forward each category's source-phase conflict-of-interest handling and announces a re-check of registry-brand ownership. Entry 1 records the move from r1 to r2. Entry 2, written after Stage S and before Stage C, records the re-check's result (one flagged brand, Denon in the headphones registry; see Declarations), keeps the primary analysis unchanged, applies the pre-registered sensitivity S7 to the flagged brand, and adds, as descriptive, the report of every headphone result without it.

# 5. Stage S: selecting the statistic

## 5.1 Rule

Selection uses EARLY-6 rank tables only: no Presence, no Consistency, no OMNI data. For each candidate and category, brand scores are computed separately on odd and even runs (1, 3, 5, 7 against 2, 4, 6, 8). Units are brands rated in both halves, in categories with at least five such units. The split-half correlation is the pooled within-category Spearman correlation $\rho_w$ (§6.1), stepped up by Spearman--Brown, $2r/(1+r)$ (Spearman, 1910; Brown, 1910). Candidates with reliability of at least 0.50 are eligible; the most reliable is selected, and candidates within 0.02 of it are tied, the tie going to the first in the order MNP, IRW, TOP3, MR, TOP1, MODE (normalised before raw, continuous before coarse). Selecting on reliability can only make the separability gate harder to pass: a more reliable score is less attenuated against Presence.

## 5.2 Result

Stage S ran on 10 November 2026 (13:57 UTC), after the r2 lock and anchor. All nine categories entered, with 138 units (12 to 20 per category). Table 1 reports the reliabilities.

\needspace{14\baselineskip}

Table: Stage S split-half reliability (Spearman--Brown) of the six candidates on EARLY-6, odd against even runs, lead-item rule. S8 drops the two knife sets (ordinary-word aliases; 113 units); S9 uses the uncentred rank convention of v0.37--v0.41. Both are reported next to the selection and cannot change it.

| Candidate | Reliability | Units | S8 (without knife sets) | S9 (uncentred) |
|:---------------------|:-----:|:-----:|:-----:|:-----:|
| **MNP** (selected) | 0.9506 | 138 | 0.9468 | 0.9541 |
| IRW | 0.9655 | 138 | 0.9642 | 0.9680 |
| TOP3 | 0.9560 | 138 | 0.9574 | 0.9592 |
| MR | 0.9572 | 138 | 0.9537 | 0.9603 |
| TOP1 | 0.9364 | 138 | 0.9379 | 0.9417 |
| MODE | 0.8888 | 138 | 0.8863 | 0.8974 |

Every candidate cleared the 0.50 floor by a wide margin. IRW was the most reliable (0.9655); MNP, TOP3 and MR fell within the 0.02 window below it, and the tie went to MNP, the first in the pre-registered order. MNP is therefore the statistic of Stage C: $R^* = 100\,(1 - \overline{q})$, rated at six or more rankable mentions. Without the two knife sets (S8) and under the uncentred convention (S9) the rule would also have selected MNP.

**Negative control (MQ7).** With the order of the named brands shuffled at random within every answer (2,000 draws, seed 110030), the mean split-half reliability of MNP fell from 0.9506 to $-0.0170$, far below the 0.20 limit (S9: 0.1160). The reliability of the selected score is therefore a property of where the models place brands, not of which brands appear together in an answer or how long the lists are.

These figures were read from `outputs/selection_v1_10.json` and checked by recomputing the six reliabilities from the hashed rank tables, which reproduced them exactly; the selection file's hash matches the Stage S record.

# 6. Stage C: confirmatory methods

## 6.1 Conventions

All pooled statistics use $\rho_w$, the pooled within-category Spearman correlation: average ranks are computed within each category, centred on the category's mean rank $(m_c + 1)/2$, and $\rho_w$ is the Pearson correlation of the pooled centred ranks. Centring departs from the v0.37--v0.41 convention: when categories contribute different numbers of units, uncentred pooling adds a between-category component, so that the statistic is above zero in expectation even when no category shows any association. The uncentred values are reported as sensitivity S9. Only categories with at least five units in a comparison enter. Permutation $p$-values are $(h + 1)/(N + 1)$. Bootstrap intervals (units resampled within category, 2,000 draws, seed 110020, 90% percentile) are reported, not used for verdicts. Values are compared unrounded.

## 6.2 Hypotheses

\needspace{12\baselineskip}

Table: Stage C hypotheses. $R^*$ is rated MNP; OMNI waves $t_1$, $t_2$, $t_3$. Separability (H1, H2, H4): CONFIRMED iff $|\rho_w| \le 0.30$ (for H1 and H2 at every wave with at least 30 units), FALSIFIED iff $|\rho_w| \ge 0.50$ (at any such wave), MARGINAL otherwise; UNDETERMINED with fewer than two such waves (H1, H2) or fewer than 30 units (H4). Stability (H3, H5, H6): CONFIRMED iff $\rho_w \ge 0.50$ and both nulls give $p < .05$; FALSIFIED iff $\rho_w < 0.30$ or either null gives $p \ge .05$; MARGINAL otherwise; UNDETERMINED below 30 units.

| Tag | Tier | Statistic | Null (draws; seed) |
|:-------------------------|:-------------|:-----------------------------------|:-------------------------------|
| H1 Separable from Presence | primary (gate) | $\rho_w(R^*, P)$ per wave | $R^*$ permuted within category (10,000; 110001), two-sided |
| H2 Separable from Consistency | primary (gate) | $\rho_w(R^*, C^*)$ per wave, both rated | as H1 (110002) |
| H3 Rank stability, 3 weeks | primary (gate) | $\rho_w(R^*_{t_1}, R^*_{t_2})$, rated in both | (a) permutation (110003); (b) within-answer order shuffle (10,000; 110010); one-sided |
| H4 Separability, early panel | secondary (gate downgrade only) | $\rho_w(R^*, \hat\pi)$ on EARLY-6 | permutation (110004), two-sided |
| H5 Rank stability, 5 months | secondary | $\rho_w(R^*_{t_2}, R^*_{t_3})$; $t_1 \rightarrow t_3$ descriptive | as H3 (110005; 110010) |
| H6 Early stability, 8 days | secondary | $\rho_w$ between v0.6 and v0.9 $R^*$, two shared models | as H3 (110006; 110010) |

In H4, $\hat\pi$ is the share of a category's answers with text that name the brand, Presence's recall arm, because no recognition probes exist for the early studies. H3's second null is the decisive one: shuffling the order of the named brands within every answer keeps list composition and list length and destroys position, so a stability that survives it is a stability of position.

## 6.3 Gate

The gate FAILS if Stage S had found no reliable statistic or if any of H1--H3 is FALSIFIED; the result is then reported as a negative result and the instrument redesigned. Otherwise it is UNDETERMINED if any of H1--H3 is; PASS if all three are CONFIRMED, downgraded to MARGINAL if H4 is FALSIFIED; and MARGINAL otherwise, in which case Paper B proceeds only on the author's recorded decision. Secondary hypotheses never turn a FAIL into a PASS.

## 6.4 Controls, baseline and sensitivities

**MQ6 (positive control).** The penalised variant (unnamed brands at $q = 1$, a brand named alone at $q = 0$, all answers with text) must reach $|\rho_w(R_{\text{pen}}, P)| \ge 0.50$ at every wave; otherwise the gate's sensitivity is flagged. It shows that the gate can detect a Ranking score that carries Presence.

**Baseline (descriptive, by panel; never pooled across panels).** Per category and wave: answers, missing cells, rankable, list-structured and numbered-list shares; registry brands named per rankable answer; brands rated against registry size; per-model list length and style; the $R^*$ distribution; leader concentration (the share of rankable answers led by the most frequent first-named brand, and the Herfindahl index of first-named brands); the three highest-$R^*$ brands.

**Sensitivities (reported; never change a verdict).** S1 first-mention rule; S2 rating floors 3 and 10; S3 all six candidates through H1--H3; S4 leave one category out; S5 the recall arm ($\hat\pi$ and total mentions) next to $P$; S6 without models whose served snapshot v0.41 flagged (none, so S6 equals the primary analysis); S7 H1--H3 without the brands flagged by the conflict-of-interest re-check (one unit, Denon in headphones, removed from every correlation; answers not re-ranked); S8 and S9 as in §5. In addition (DEVIATIONS Entry 2, added after the lock and labelled descriptive), every headphone result is also reported without Denon on the S7 rule.

## 6.5 Files

Stage C reads the 31 hashed rank tables (`outputs/rank_tables/`, re-extracted and compared byte for byte), the selection file, the Stage S data-quality record, $P$ and $C^*$ from `osf/aias_2_0/aias_2_0_profiles.csv`, the v0.41 verdicts (S6) and `anchor/coi_flags_v1_10.json` (S7; not a frozen input, its SHA-256 is recorded). It writes `outputs/v1_10_verdicts.json`.

# 7. Results

Stage C ran once, on 10 November 2026, after DEVIATIONS Entry 2 and the flag file were anchored. Re-extraction reproduced all 31 rank tables byte for byte, and the gate's units joined the Presence and Consistency table 1:1 (112 of 112 per wave). Every number below is read from `outputs/v1_10_verdicts.json`; §7.6 reports the independent re-computation.

## 7.1 The gate

\needspace{14\baselineskip}

Table: Gate hypotheses. $\rho_w$ = pooled within-category Spearman correlation on centred ranks; $R^*$ = rated MNP. H1 and H2: two-sided permutation $p$ ($R^*$ permuted within category, 10,000 draws). H3: one-sided $p$ for both nulls (10,000 draws each; 0.0001 is the smallest value 10,000 draws can return). 90% intervals: units resampled within category (2,000 draws); reported, not used for verdicts.

| Hypothesis | Wave | $\rho_w$ | $n$ | $p$ | 90% interval | Verdict |
|:----------------------|:-------:|:-----:|:---:|:--------------|:------------------:|:----------:|
| H1 Separable from Presence | $t_1$ | 0.275 | 55 | 0.071 | [0.006, 0.510] | |
| | $t_2$ | 0.366 | 54 | 0.017 | [0.094, 0.603] | |
| | $t_3$ | 0.307 | 54 | 0.042 | [0.101, 0.487] | MARGINAL |
| H2 Separable from Consistency | $t_1$ | 0.252 | 55 | 0.094 | [0.008, 0.446] | |
| | $t_2$ | 0.119 | 54 | 0.460 | [$-0.124$, 0.348] | |
| | $t_3$ | 0.142 | 54 | 0.356 | [$-0.119$, 0.360] | CONFIRMED |
| H3 Rank stability, 3 weeks | $t_1 \rightarrow t_2$ | 0.897 | 53 | perm 0.0001; shuffle 0.0001 | [0.761, 0.943] | CONFIRMED |

**The gate is MARGINAL: it is not passed.** H2 and H3 are CONFIRMED; H1 is MARGINAL. Ranking's correlation with Presence is positive at every wave --- brands with higher Presence tend to be placed higher --- and it lies inside the confirmation band ($\le 0.30$) only at $t_1$. At $t_2$ (0.366) and $t_3$ (0.307, compared unrounded) it falls between the confirmation and falsification lines. The association is distinguishable from zero at $t_2$ and $t_3$ ($p$ = 0.017 and 0.042), and the 90% intervals reach 0.51 and 0.60 at $t_1$ and $t_2$, so values in the falsification band cannot be excluded at those waves.

Both controls behaved as designed. The positive control MQ6 passed: the penalised variant, which scores unnamed brands as last, tracked Presence at $|\rho_w|$ = 0.909, 0.901 and 0.918 ($n$ = 112 at each wave), so the gate can detect a Ranking score that carries Presence. The negative control MQ7 was not flagged (§5.2). Under the gate rule, a MARGINAL gate is reported as is, and Paper B proceeds only on the author's recorded decision, with the marginal leg, separability from Presence, as its first confirmatory test.

## 7.2 Secondary hypotheses

- **H4 (separability in the early panel): FALSIFIED.** On EARLY-6, $\rho_w(R^*, \hat\pi)$ = 0.663 ($n$ = 154 brands in nine categories; $p$ = 0.0001; 90% interval [0.527, 0.745]). Under the gate rule a FALSIFIED H4 downgrades a PASS to MARGINAL; the gate is already MARGINAL, so H4 does not change it, but it points the same way.
- **H5 (five-month stability): CONFIRMED.** $\rho_w(R^*_{t_2}, R^*_{t_3})$ = 0.846 ($n$ = 52; both nulls $p$ = 0.0001; 90% interval [0.651, 0.920]). Descriptively, $t_1 \rightarrow t_3$: 0.940 ($n$ = 52).
- **H6 (eight-day stability, early panel): CONFIRMED.** Between v0.6 and v0.9 on the two shared models, $\rho_w$ = 0.830 ($n$ = 65; both nulls $p$ = 0.0001; 90% interval [0.668, 0.919]).

The early panel's positions are first-mention positions. In every early answer file (all nine EARLY-6 sets and the five EARLY-2 sets) the archived text stores each response with its line breaks collapsed, so rule E3 finds no list items, no answer is list-structured, and E6 orders every early answer by first mention (the list-structured share is 0 in all fourteen early sets, against 0.64 to 1.00 in the OMNI sets). This is E6 applied as written, not an extraction error, and it agrees with MQ3's median $\tau$ of 1.0. It means that Stage S, H4 and H6 rest on first-mention order. It was noticed when the baseline was read, after Stage C; no rule or result was changed. On the gate set, where answers keep their line breaks, the first-mention rule (S1) gives almost the same gate statistics as the lead-item rule (Table 4).

## 7.3 Sensitivities

\needspace{16\baselineskip}

Table: Sensitivities of the gate statistics. $\rho_w$ for H1 and H2 at $t_1$ / $t_2$ / $t_3$; H3 = $t_1 \rightarrow t_2$. S3, S4 and S6--S9 use the primary H4 verdict (FALSIFIED) in the gate rule, so a sensitivity under which H1--H3 are all CONFIRMED still gives a MARGINAL gate. S6 and S7 are identical to the primary analysis (see text). S9 uses uncentred ranks.

| Analysis | H1 $\rho_w(R^*, P)$ | H2 $\rho_w(R^*, C^*)$ | H3 | Gate |
|:--------------------------|:-------------------:|:-------------------:|:-----:|:---------:|
| Primary (MNP, floor 6, lead-item) | 0.275 / 0.366 / 0.307 | 0.252 / 0.119 / 0.142 | 0.897 | MARGINAL |
| S1 first-mention rule | 0.270 / 0.366 / 0.307 | 0.242 / 0.119 / 0.142 | 0.893 | MARGINAL |
| S2 floor 3 | 0.352 / 0.326 / 0.434 | 0.252 / 0.119 / 0.142 | 0.907 | MARGINAL |
| S2 floor 10 | **0.558 / 0.635** / 0.219 | **0.411** / 0.126 / 0.253 | 0.883 | **FAIL** |
| S3 IRW | 0.293 / 0.351 / 0.379 | 0.175 / 0.034 / 0.137 | 0.942 | MARGINAL |
| S3 TOP3 | 0.364 / 0.289 / 0.261 | 0.153 / 0.127 / 0.160 | 0.822 | MARGINAL |
| S3 MR | 0.283 / 0.443 / 0.427 | 0.189 / 0.017 / 0.165 | 0.861 | MARGINAL |
| S3 TOP1 | 0.325 / 0.301 / 0.366 | 0.001 / $-0.063$ / 0.137 | 0.932 | MARGINAL |
| S3 MODE | **0.093 / 0.247 / 0.206** | 0.191 / 0.042 / 0.099 | 0.858 | MARGINAL |
| S4 range, leave one category out | 0.231--0.318 / 0.281--0.440 / 0.078--0.472 | 0.102--0.337 / 0.004--0.180 / $-0.072$--0.220 | 0.884--0.933 | MARGINAL (all five) |
| S9 uncentred ranks | 0.363 / 0.452 / 0.384 | **0.342** / 0.238 / 0.235 | 0.909 | MARGINAL |

Sensitivities never change a verdict; the scorer lists eight verdict changes under them (bold in Table 4). Raising the rating floor to ten rankable mentions (S2; 31--34 brands per wave) moves H1 into the falsification band at $t_1$ and $t_2$ (0.558 and 0.635), H2 to MARGINAL and the gate to FAIL. Among the candidate statistics (S3), only the coarse modal rank keeps H1 inside the confirmation band (0.093, 0.247, 0.206); every other candidate, including the one with the highest reliability (IRW), is MARGINAL on H1. Leaving out automotive (S4) brings H1 inside the band (0.261, 0.281, 0.280); leaving out headphones or spirits moves H2 to MARGINAL (0.306 and 0.337 at $t_1$), and so does the uncentred convention (S9; 0.342 at $t_1$). Under S9 every other verdict is unchanged (H4 0.681, H5 0.864, H6 0.846; MQ6 passes).

S5 places the recall arm next to Presence: $\rho_w(R^*, \hat\pi)$ = 0.291, 0.387 and 0.333, slightly above $\rho_w(R^*, P)$ at every wave (within a wave $\hat\pi$ is proportional to total mentions, so the two give the same values). The coupling therefore runs through how often a brand is named, not through recognition. S6 is identical to the primary analysis because v0.41 flagged no served model. S7 is identical to the primary analysis because Denon is never rated: it is named in no rankable answer at $t_1$ or $t_3$ and in two at $t_2$, below the floor of six, so removing it removes no unit from any correlation. At Stage S, S8 and S9 would also have selected MNP (§5.2).

## 7.4 Cross-category baseline

\needspace{14\baselineskip}

Table: Baseline, gate set (LEGACY-6), values at $t_1$ / $t_2$ / $t_3$. Rankable share = answers naming at least two registry brands, of 36. Brands named = median registry brands per rankable answer. Leader share = share of rankable answers led by the most frequent first-named brand. Highest $R^*$ = rated brand with the highest MNP.

| Category | Rankable share | Brands named | Rated / registry | Median $R^*$ | Leader share | Highest $R^*$ |
|:-------------|:-------------:|:-----------:|:-----------:|:-------------:|:-------------:|:-------------------|
| Headphones (v0.19) | 0.83 / 0.83 / 0.83 | 6 / 5.5 / 5 | 8 / 8 / 8 of 16 | 47.1 / 46.3 / 46.1 | 0.57 / 0.67 / 0.60 | Sennheiser at all three |
| Skincare (v0.20) | 1.00 / 1.00 / 1.00 | 6 / 6 / 6 | 10 / 9 / 9 of 24 | 53.2 / 56.6 / 58.1 | 0.42 / 0.47 / 0.39 | La Mer at all three |
| Cosmetics (v0.21) | 0.97 / 0.97 / 1.00 | 5 / 7 / 6 | 14 / 14 / 13 of 24 | 50.0 / 44.8 / 47.0 | 0.26 / 0.26 / 0.25 | Tom Ford Beauty; MAC Cosmetics at $t_3$ |
| Automotive (v0.22) | 1.00 / 1.00 / 1.00 | 6.5 / 6 / 6 | 14 / 14 / 14 of 24 | 51.1 / 50.0 / 50.0 | 0.44 / 0.44 / 0.47 | Toyota at all three |
| Spirits (v0.23) | 0.67 / 0.67 / 0.64 | 4 / 3.5 / 4 | 9 / 9 / 10 of 24 | 43.7 / 46.4 / 47.5 | 0.21 / 0.21 / 0.22 | Hendrick's; Nikka at $t_2$ |

\needspace{16\baselineskip}

Table: Baseline, early panels (EARLY-6, nine sets; EARLY-2, five sets). Columns as in Table 5; HHI = Herfindahl index of first-named brands. Every early answer is ordered by first mention (§7.2).

| Set | Rankable share | Brands named | Rated / registry | Median $R^*$ | Leader share | HHI | Highest $R^*$ |
|:------------------------|:-----:|:---:|:-------:|:-----:|:-----:|:-----:|:-----------------------|
| EARLY-6 PM software | 1.00 | 6 | 17 / 19 | 40.7 | 0.41 | 0.25 | Linear |
| EARLY-6 personal finance | 0.98 | 7 | 14 / 16 | 37.6 | 0.39 | 0.29 | YNAB |
| EARLY-6 olive oil | 0.85 | 4 | 16 / 20 | 44.2 | 0.39 | 0.20 | Frescobaldi Laudemio |
| EARLY-6 running shoes | 0.99 | 6 | 15 / 17 | 34.1 | 0.56 | 0.36 | Norda |
| EARLY-6 skincare | 0.76 | 7 | 22 / 31 | 37.1 | 0.65 | 0.46 | CeraVe |
| EARLY-6 household retail | 0.93 | 7 | 20 / 21 | 32.7 | 0.30 | 0.25 | IKEA |
| EARLY-6 knives | 0.83 | 6 | 16 / 21 | 41.0 | 0.35 | 0.27 | Wüsthof |
| EARLY-6 premium tea | 0.85 | 5 | 17 / 25 | 42.3 | 0.24 | 0.14 | Rishi Tea |
| EARLY-6 kitchen knives | 0.95 | 5 | 17 / 36 | 41.1 | 0.68 | 0.50 | Wüsthof |
| EARLY-2 PM software | 1.00 | 6 | 16 / 19 | 40.0 | 0.44 | 0.27 | Motion |
| EARLY-2 personal finance | 0.98 | 5 | 12 / 16 | 36.8 | 0.47 | 0.36 | YNAB |
| EARLY-2 olive oil | 0.76 | 4 | 11 / 20 | 44.4 | 0.56 | 0.36 | California Olive Ranch |
| EARLY-2 running shoes | 1.00 | 6 | 11 / 17 | 63.4 | 0.47 | 0.28 | Adidas |
| EARLY-2 skincare | 0.71 | 6 | 16 / 31 | 35.6 | 0.59 | 0.40 | CeraVe |

Rankable answers name a median of 3.5 to 7 registry brands, fewest in spirits and olive oil. How concentrated first place is varies by category: in headphones (0.57--0.67), kitchen knives (0.68) and skincare in the early panels (0.59--0.65) one brand opens more than half of all rankable answers, while in spirits, cosmetics and premium tea the most frequent leader opens about a quarter or fewer. The highest-ranked brand is the same at all three gate waves in three of five categories. Within the legacy panel, model style differs: the share of list-structured answers ranges from 0.63 (Gemini 2.5 Flash) to 1.00 (Claude Sonnet 4.5), and mean list length from 5.3 to 6.3 registry brands per rankable answer.

## 7.5 Headphone results without Denon (exploratory)

As recorded in DEVIATIONS Entry 2, every headphone result is also reported without Denon, on the S7 rule (the unit removed, answers not re-ranked). The table is descriptive, was added after the lock, is computed outside the locked scorer (`scripts/headphones_without_denon_v1_10.py`; output `outputs/exploratory/headphones_without_denon_v1_10.json`) and changes no verdict. Its with-Denon values reproduce the scorer's baseline rows.

\needspace{10\baselineskip}

Table: Headphones (v0.19) with and without Denon. Denon's positions at $t_2$: 9th of 10 and 6th of 6 registry brands named. Every quantity not listed (rankable answers, brands rated, the $R^*$ distribution, leader share, Herfindahl index, highest-ranked brands, and the H1--H3 inputs) is identical with and without Denon at every wave.

| Wave | Denon in rankable answers | Denon rated | Brands named, median (with / without) | Rated share of registry (with / without) |
|:-----:|:---:|:---:|:---:|:---:|
| $t_1$ | 0 | no | 6 / 6 | 8 of 16 / 8 of 15 |
| $t_2$ | 2 | no | 5.5 / 5 | 8 of 16 / 8 of 15 |
| $t_3$ | 0 | no | 5 / 5 | 8 of 16 / 8 of 15 |

## 7.6 Independent re-computation

H1, H2, H3 and S7 were recomputed with separate code, from the hashed rank tables and the profiles table, without the scorer. The correlations and unit counts agree exactly at every wave (H1 0.27503, 0.36594, 0.30731; H2 0.25167, 0.11927, 0.14153; H3 0.89676, $n$ = 53), as does S7. The permutation $p$-values, re-drawn with a different seed (10,000 draws), agree within Monte Carlo error (differences of at most 0.009, each under two Monte Carlo standard errors; the largest relative to its error is H2 at $t_1$, 0.102 against 0.094); no shuffled or permuted draw reached the observed H3 value in either computation.

# 8. Discussion

The gate answers the question it was built for, and the answer is not yet. Ranking, as measured here, is a reliable reading of where models place a brand: its split-half reliability is 0.95, it collapses to zero when position is shuffled, and brand order holds over three weeks and five months well beyond what list composition produces. It is also distinct from Consistency. But it is not cleanly distinct from Presence. The correlation is modest --- 0.27 to 0.37 within category, far from the 0.77 at which the first Consistency instrument was falsified --- yet it sits above the line the program drew for a separate component at two of the three waves.

The pattern is the one the pre-registration named as the main risk. Brands that the models name more often tend to be named earlier, and the link runs through recall, not recognition (S5). It is strongest in the early panel (0.663) and, at $t_1$ and $t_2$, among the brands named often enough to be rated at a floor of ten (0.558 and 0.635; 0.219 at $t_3$). The pre-registration expected a stricter floor to weaken the correlation by restricting the range of Presence; at two of three waves it strengthened it instead, which suggests that among frequently named brands position and frequency are not less tied than among the rest. A plausible mechanism, not tested here, is that models open an answer with the brands most typical of the category, and those are also the brands they name across most prompts. In marketing terms, this is a Double-Jeopardy-like regularity in AI answers: the brands with more presence also get the better positions.

The predictions written before Stage S fared as follows. Stage S was expected to select MNP or IRW: it selected MNP, with IRW tied. H1 was expected to be MARGINAL and was. H2 and H3 were expected to be CONFIRMED and were. H5 was expected to be MARGINAL over five months and was CONFIRMED (0.846). The positive control was expected to pass and did.

Three readings of the sensitivities limit how far the result should be pushed in either direction. First, the verdict depends partly on category: without automotive, H1 would have been CONFIRMED, and without headphones or spirits, H2 would have been MARGINAL. With 8 to 14 rated brands per category, single categories move pooled correlations. Second, only the coarse modal rank (MODE) stayed inside the confirmation band on H1, and it is the least reliable candidate (0.889); its separation may partly reflect its coarseness. Third, the early panel's positions are first-mention positions (§7.2), so H4 tests a simpler order than the gate does; its falsification is nonetheless consistent with the gate's direction.

For reporting, the consequence is direct. The program does not add Ranking to the reported AIAS components on this evidence, and Presence and Consistency remain the two reported scores. The rank tables and the baseline (§7.4) may be used as description, labelled as such. Whether Ranking proceeds to Paper B, with separability from Presence as its first confirmatory test, or is redesigned first is a decision the pre-registration reserves for the author.

# 9. Limitations

This is a re-analysis of answers already in the record, and Presence and Consistency for the gate's units were published before it; the lock, the order of operations enforced in code and the blind selection on a different panel are the protections. Archived position data exist (model-extracted rankings in the early files, a per-mention rank in the v0.19 coded files, slot positions in the v0.23 scored files); the scorer never reads them, except the early rankings for the MQ3 concordance check.

The early answer files store each response with its line breaks collapsed, so every early answer is ordered by first mention; Stage S, H4 and H6 therefore rest on first-mention order, while the gate rests on the lead-item rule. This was noticed after Stage C and is reported, not corrected; a redesign or Paper B that uses the early panel should restore line structure from the providers' raw responses, if they exist, under a new pre-registration.

The gate's precision is limited. Each comparison rests on 52 to 55 rated brands, 8 to 14 per category, and the 90% intervals for H1 are 0.39 to 0.51 wide. The $t_3$ value of H1 (0.307) lies just above the confirmation line, and single categories move the verdicts (S4). Ranking is rated only for brands with at least six rankable mentions, so about half of the brands in these categories have no Ranking score, much as v1.9 found for Consistency.

Rank is among registry brands only: in the development sample 51--66% of top-level list items carried no registry brand, so a brand's absolute position in a list and its registry rank differ. Position in text is not visual prominence, and the lead-item parser relies on Markdown conventions. One legacy panel, now retiring, carries the gate, and its models answer without web search; the newest models enter with the fourth wave. The audiophile-headphones registry contains one brand flagged by the conflict-of-interest re-check (Declarations); it is never rated, so it affects no statistic (S7, §7.5).

# 10. What follows

The gate is MARGINAL, so the pre-registered rule applies: the result is reported as it stands, Ranking is not added to the reported AIAS components, and Paper B proceeds only on the author's recorded decision, with separability from Presence (H1) as its first confirmatory test. Without that decision, the instrument is redesigned under a new pre-registration, as the program does with any component that does not pass its gate. Either way, the next study inherits the locked extractor and its tests, the selected statistic and floor, the hashed rank tables (including the frozen v0.32 arms for model-version stability), $R^*$ by wave beside $P$ and $C^*$, the null distributions and the verdict file. A redesign would need to address the coupling found here directly, for example by measuring position within strata of recall, and would have to show, as v1.8 did for Consistency, that the redesigned score is separable from recall by construction and not by adjustment. The fourth wave on the newest models will show whether the coupling is a property of the legacy panel or of AI answers generally.

# Declarations {-}

## Conflict of interest {-}

The author is Director, Corporate Brand Creative and Governance at Samsung Electronics America. This study re-analyses archived answers against brand registries fixed in earlier phases; it performs no new brand selection, and each registry carries its source-phase conflict-of-interest handling forward (v1.10 DEVIATIONS Entry 0). The program's technology-brand answers (v0.28) are pinned and parse-checked only, pending their own screen, and are not analysed. Two items of record apply to the analysed registries.

*Audiophile headphones (v0.19).* The v0.19 record states: "The panel substitution of AKG → Denon documented in §5 was made out of an abundance of caution given that Samsung's subsidiary Harman International owns AKG; the substitution occurred prior to pre-registration lock." (v0.19 paper, Declaration of interest; see also v0.19 pre-registration §2.3 and v0.19 DEVIATIONS Entry 1.) Correction (November 10, 2026): Denon, which replaced AKG in the v0.19 registry, has itself been owned by Harman International, a wholly owned subsidiary of Samsung Electronics, since September 23, 2025, when Harman completed its acquisition of Sound United from Masimo; the v0.19 headphones registry therefore includes one Samsung-group brand. The substitution did not achieve its purpose, and this was not noticed until November 10, 2026. Source: HARMAN, "HARMAN Completes Sound United Acquisition to Expand Premium Audio Leadership", press release, Business Wire, September 23, 2025. In this study Denon remains in the locked registry and in the primary analysis; the gate statistics are also reported without Denon (sensitivity S7), and every headphone result is also reported without it (v1.10 DEVIATIONS Entry 2, written before any confirmatory result).

*Automotive (v0.22).* The v0.22 record states: "Samsung subsidiaries hold tier-2/3 component supply relationships with several brands in the v0.22 registry: Harman International (audio systems) supplies Mercedes-Benz, BMW, and other premium automotive OEMs; Samsung SDI (battery cells) supplies BMW (i-series), Volkswagen Group brands including Bentley and Porsche (Stellantis-adjacent platforms), and others; Samsung Display (infotainment) supplies Mercedes-Benz and BMW. Tesla and Polestar also have tangential Samsung-component exposure at the parts level. These are non-competitive supply relationships; Samsung Electronics America does not produce or market passenger car brands and has no brand-level competitive overlap with any v0.22 registry entry. The COI was screened and documented in DEVIATIONS Entry 0 (Part B) of the pre-registration module; no operational restriction on registry composition was imposed." (v0.22 paper, Conflict of interest.) These are supply relationships, not ownership; no v0.22 brand is removed in this study.

Extraction, statistic selection and scoring are automated against the locked registries and the locked pre-registration, and the statistic was selected before the scorer could read Presence or Consistency. Apart from the AKG substitution and the handling recorded in DEVIATIONS Entry 2, the author's affiliation played no role in registry construction, selection, scoring or the verdicts. Samsung Electronics had no role in the design, conduct, analysis or reporting of this work.

## Funding {-}

Self-funded. No external funding supported this research.

## Ethics {-}

Not applicable; no human subjects. The study analyses archived responses of large language models queried under their public interfaces.

## Use of AI tools {-}

During the preparation of this work the author used AI tools (Anthropic's Claude) to assist with study design, analysis and writing. The author reviewed and edited all content and takes full responsibility for it.

## Data and code availability {-}

Materials are deposited at OSF, `ec6wh/methodology/v1_10`: the locked pre-registration with its parity record and feasibility note, the input manifest and registry inputs, the anchor record and the deviations record. The scorer (`scripts/score_v1_10.py`) and its tests (`scripts/test_score_v1_10.py`) are in the program repository at tag `v1.10-prereg-r2`. The Stage S outputs (`outputs/selection_v1_10.json`, `outputs/stage_s_v1_10.json` and the 31 hashed rank tables), the conflict-of-interest flag file (`anchor/coi_flags_v1_10.json`), the Stage C verdicts (`outputs/v1_10_verdicts.json`) and the exploratory headphone tables (`outputs/exploratory/headphones_without_denon_v1_10.json`, from `scripts/headphones_without_denon_v1_10.py`) join the deposit. The underlying answers are deposited with their source studies.

# References {-}

Brown, W. (1910). Some experimental results in the correlation of mental abilities. *British Journal of Psychology, 3*(3), 296--322.

Ehrenberg, A. S. C., Goodhardt, G. J., & Barwise, T. P. (1990). Double jeopardy revisited. *Journal of Marketing, 54*(3), 82--91.

González Castro, P. U. (2026). *AI Availability: Extending Mental and Physical Availability into Algorithmic Retrieval*. SSRN 6659000.

González Castro, P. U. (2026). *Tri-System Brand Growth: The AI Mediation Layer*. MSI Working Paper, Report No. 26-132. Marketing Science Institute.

González Castro, P. U. (2026). *The AIAS™ Presence Measurement Protocol: Methodological Notes on Construct Validity and the Four-Regime Taxonomy* (v1.2). SSRN 6761698.

González Castro, P. U. (2026). *The AIAS Presence Measurement Protocol: Phase A Pivot-Validation Specification* (v1.3). SSRN 6797679.

González Castro, P. U. (2026). *The AIAS Presence Measurement Protocol v1.4: Recognition × Recall Decomposition and Multi-Component AI Availability*. SSRN 6799479.

González Castro, P. U. (2026). *The AIAS™ Presence Measurement Protocol: Multi-Statistic C2 Specification and Two-Channel Recall Decomposition* (v1.5). SSRN 6810758.

González Castro, P. U. (2026). *Substrate Pre-Screening, Independent Moderator Pathway, and Phantom Brand Persistence Phase B Extension* (AIAS Methodology v1.6). SSRN 6816340.

González Castro, P. U. (2026). *The AIAS Presence Measurement Protocol: CPC Consistency --- A Pre-Registered Negative Result* (v1.7). SSRN 6878818.

González Castro, P. U. (2026). *A Mean-Independent Consistency Instrument for Cross-Model AI Presence: Redesigning CPC on a Quasi-Binomial Dispersion Basis* (AIAS Methodology v1.8). SSRN 6963359.

González Castro, P. U. (2026). *One Score or Two? Calibrating a Presence and Consistency Composite for AI Brand Availability* (AIAS Methodology v1.9). SSRN 7685126 (submitted).

González Castro, P. U. (2026). *AI Availability as a Third Measurable Layer of Brand Availability: Five-Substrate Empirical Anchoring of the AIAS™ Presence Measurement Protocol* (AIAS 1.0). SSRN 6817841.

González Castro, P. U. (2026). *Presence and Consistency: A Two-Component Measurement of AI Availability* (AIAS 2.0). Working paper; OSF `ec6wh/aias_2_0`.

González Castro, P. U. (2026). *Two-Wave Temporal Stability of an AI Brand-Recall Consistency Quantity: A Pre-Registered Longitudinal Re-Acquisition Across Five Product Categories* (v0.34). SSRN 6915458.

González Castro, P. U. (2026). *Identity Load Does Not Moderate Cross-Model Consistency: A Pre-Registered Component-Dissociation Null* (v0.37). SSRN 7685199 (submitted).

González Castro, P. U. (2026). *Five-Month Stability of AI Brand Consistency and Presence: A Pre-Registered Third Wave on a Retiring Six-Model Panel* (v0.41). SSRN 7685100 (submitted).

González Castro, P. U. (2026). *AI Presence Measurement Across Consumer Categories: A Cross-Category Baseline of Brand Visibility in Large Language Model Outputs* (v0.6). Working paper; copy at thirdsystem.ai and OSF `ec6wh`.

González Castro, P. U. (2026). *A Designed-for-Test Measurement of Phantom-Brand Presence in Large Language Model Outputs: Pre-Registered Evidence from Bed Bath & Beyond, with Pier 1 as Structural Comparator* (v0.7). SSRN 6721779.

González Castro, P. U. (2026). *A Designed-for-Test Measurement of Discourse-Language Bias in Large Language Model Brand Recommendations* (v0.8). SSRN 6728000.

González Castro, P. U. (2026). *AI Presence Drift: A Longitudinal Re-Baseline of Five Brand Categories* (v0.9). SSRN 6736878.

González Castro, P. U. (2026). *Premium Tea as the Third Regime 4 Datapoint: A Single-Category Replication of the v0.13 Covariate-Saturated Weak Finding* (v0.14). SSRN 6755621.

González Castro, P. U. (2026). *Regime 4 Boundary and Discourse-Language Carryforward on the Kitchen-Knives Substrate* (v0.16). SSRN 6791999.

González Castro, P. U. (2026). *AI Presence in Audiophile headphones: AIAS v0.19*. SSRN 6809182.

González Castro, P. U. (2026). *AI Presence in Skincare: AIAS v0.20*. SSRN 6811441.

González Castro, P. U. (2026). *AI Presence in Cosmetics: AIAS v0.21*. SSRN 6815378.

González Castro, P. U. (2026). *AIAS™ v0.22 --- Automotive Substrate: Phantom Brand Persistence on a Heritage-Saturated Category*. SSRN 6829118.

González Castro, P. U. (2026). *AIAS™ v0.23 --- Premium Spirits Substrate*. SSRN 6834298.

Romaniuk, J., & Sharp, B. (2022). *How Brands Grow, Part 2* (Revised ed.). Oxford University Press.

Sharp, B. (2010). *How Brands Grow: What Marketers Don't Know*. Oxford University Press.

Spearman, C. (1910). Correlation calculated from faulty data. *British Journal of Psychology, 3*(3), 271--295.
