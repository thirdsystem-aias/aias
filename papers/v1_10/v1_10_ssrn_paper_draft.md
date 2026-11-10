---
title: "Where a Brand Sits in an AI Answer: A Ranking Instrument and Its Separability from Presence and Consistency"
subtitle: "Ranking, Paper A: Pre-Registered Instrument Specification, Cross-Category Baseline and Separability Gate (AIAS™ Methodology v1.10)"
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

{\LARGE \textbf{Where a Brand Sits in an AI Answer: A Ranking Instrument\\ and Its Separability from Presence and Consistency}}\\[8pt]

{\large Ranking, Paper A: Pre-Registered Instrument Specification, Cross-Category Baseline\\ and Separability Gate (AIAS™ Methodology v1.10)}\\[28pt]

Pablo Ulpiano González Castro\\[4pt]
School of Visual Arts, MPS Branding Program, New York, NY \textit{(primary academic affiliation)}\\
Third System™ (research entity; data archive and methodology venue)\\[8pt]
Correspondence: pablou@pablou.com · pablou.com\\
ORCID: 0009-0003-8968-9990\\[20pt]

Pre-registration: \texttt{v1.10-prereg-r2} (deposited on OSF before any rank statistic was computed on confirmatory data)\\
Materials: OSF \texttt{ec6wh/methodology/v1\_10}\\[20pt]

\textit{Working draft, November 10, 2026: Stage C results pending.}

\end{center}
\end{titlepage}

# Abstract {-}

**TODO-STAGE-C.** The abstract is written after Stage C and reports the gate verdict (PASS, MARGINAL, UNDETERMINED or FAIL) with H1--H3 at every wave, H4--H6, the controls MQ6 and MQ7, and the S7 values without the conflict-of-interest-flagged brand. Facts already fixed: the instrument (rules E0--E7) parses 100% of the 3,766 archived answers with text in the 32 pinned sets; Stage S selected mean normalised position (MNP) on the early panel (Spearman--Brown split-half reliability 0.9506, 138 brand units, nine categories; best candidate 0.9655, within the 0.02 tie window), and shuffling the order of brands within answers brought its reliability to $-0.0170$.

**Keywords:** AI availability; brand availability; AIAS; pre-registration; Ehrenberg-Bass; large language models; ranking; list position; separability; measurement reliability

**JEL codes:** M31; L86, L15, D83, M37

**Paper status:** Pre-registered methodology study (tag `v1.10-prereg-r2`). Re-analysis of archived answers: no new data collection and no model calls. The statistic was selected (Stage S) after the lock, blind to Presence and Consistency; the confirmatory gate (Stage C) runs after the conflict-of-interest re-check is logged (DEVIATIONS Entry 2). Part of the AIAS measurement program.

# 1. Introduction

AI Availability --- the discoverability and representation of a brand in the outputs of large language models --- has been proposed as a third measurable layer of brand availability (González Castro, 2026, SSRN 6659000), beside the Mental and Physical Availability of the Ehrenberg-Bass tradition (Sharp, 2010; Romaniuk & Sharp, 2022). The Tri-System framework describes the AI Availability Score (AIAS) as a 0--100 score built from several dimensions (MSI Working Paper 26-132). The program has validated two of them. Presence, how often a fixed panel of models recognizes and names a brand, was anchored across five product categories under the v1.6 protocol (SSRN 6816340; AIAS 1.0, SSRN 6817841). Consistency, whether the panel's models agree about a brand, reached a usable instrument only after its first version was falsified for moving with recall (v1.7, SSRN 6878818) and replaced by the mean-independent dispersion statistic $\varphi$ (v1.8, SSRN 6963359). The v1.9 calibration found that no composite of the two carried information Presence did not, and locked the reporting of two scores side by side (SSRN 7685126). The AIAS 2.0 synthesis reports them that way and shows them separable: within category, $|\rho(C^*, P)|$ = 0.073, 0.082 and 0.189 at the three waves, as published.

This paper opens the third component. Ranking is where a brand sits in an answer's ordered list of brands, *given that the brand is named*. Whether a brand is named at all is Presence's information; how evenly the models name it is Consistency's. A third component is worth adding only if it carries information neither of the first two carries, and the program's own record shows how easily that condition fails: the first Consistency instrument was reliable and looked plausible, yet it largely re-expressed recall (pooled $\rho$ = 0.766 against a 0.50 ceiling; v1.7). Ranking faces a specific version of that risk. In consumer markets, brands with more buyers also tend to score higher on loyalty and attitude measures (the Double Jeopardy pattern; Ehrenberg, Goodhardt & Barwise, 1990), and the brands a model names most often may also be the ones it names first. If so, a ranking score would add little to Presence.

The study is the first of two papers on Ranking, following the program's plan for each new component: Paper A specifies the instrument, describes it across categories and subjects it to a separability gate; Paper B, on robustness and structure, follows only if Paper A passes. Paper A has three parts. First, a deterministic, registry-based extractor recovers each named brand's position in archived long-form answers, lists and prose alike (§2). Second, a rank statistic is chosen from six candidates by a rule fixed in advance, on a separate panel and blind to Presence and Consistency (Stage S, §5). Third, a confirmatory gate tests whether the selected score is separable from Presence and from Consistency, and whether it holds its brand order over three weeks beyond what list composition alone produces (Stage C, §6).

All data already exist: 3,658 confirmatory-period answers on three model panels across fourteen category sets, collected between April and November 2026 for earlier studies. Because Presence and Consistency for the gate's units are published, the design fixes the order of operations in code: the scorer refuses to run before the pre-registration is tagged and anchored, it selects the statistic before it may open the Presence and Consistency table, and it halts on any change to a frozen input (§4).

**TODO-STAGE-C:** one paragraph stating the result and the contribution.

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

**Selection and replication set (EARLY-6).** Nine early category studies on a second panel (Claude Sonnet 4.6, Claude Opus 4.7, GPT-5.4 mini, GPT-5.5, Gemini 2.5 Flash, Grok 4.1 Fast): PM software, personal finance, olive oil, running shoes and skincare (v0.9), household retail and knives (v1.0), premium tea (v0.14) and kitchen knives (v0.16). Six prompt types $\times$ six models $\times$ eight runs give 288 answers per set; kitchen knives used 11 prompts in three groups and has 334 answers with text in 515 rows. In all, 2,638 answers with text. Each set is read with the registry its source phase's extraction applied.

**Other sets.** EARLY-2 (v0.6: two of the EARLY-6 models, five categories, 480 answers) enters the early-stability test H6 and the baseline. The v0.28 technology answers (36) are pinned and parse-checked only, pending their own conflict-of-interest screen. The v0.32 model-version arms (72 answers) are frozen for Paper B and not analysed here. The development sample used for the declared parsing-feasibility note (v0.17 and v0.18, 36 answers) is excluded from every confirmatory analysis, as are the sets listed in pre-registration §2.5.

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

**TODO-STAGE-C.** §7.1 the gate (H1--H3 by wave, with $n$, $p$ and 90% intervals; verdicts; MQ6 and MQ7 flags); §7.2 secondary hypotheses H4--H6 and $t_1 \rightarrow t_3$; §7.3 sensitivities S1--S9, with every verdict change listed and the S7 values without Denon next to the primary values; §7.4 the cross-category baseline by panel (table and figure); §7.5 headphone results without Denon (descriptive; DEVIATIONS Entry 2).

# 8. Discussion

**TODO-STAGE-C.** Interpretation of the gate outcome against the predictions written before Stage S (pre-registration §11: Stage S lean MNP or IRW, borne out; H1 lean MARGINAL, the Double-Jeopardy-like risk; H2 lean CONFIRMED; H3 lean CONFIRMED; H5 lean MARGINAL; MQ6 lean passes); what Paper B inherits, or the redesign if the gate fails.

# 9. Limitations

**Draft, to be revised after Stage C.** This is a re-analysis of answers already in the record, and Presence and Consistency for the gate's units are published; the lock, the order enforced in code and the blind selection on a different panel are the protections. Archived position data exist (model-extracted rankings in the early files, a per-mention rank in the v0.19 coded files, slot positions in the v0.23 scored files); the scorer never reads them, except the early rankings for the MQ3 concordance check. Rank is among registry brands only: in the development sample 51--66% of top-level list items carried no registry brand, so a brand's absolute position in a list and its registry rank differ. The rating floor restricts the range of Presence among rated brands, which can lower $|\rho|$; MQ6 and S2 address this. OMNI is small per category (16--24 brand units, 36 answers per wave), and the early sets have one wave each. Position in text is not visual prominence, and the lead-item parser relies on Markdown conventions. One legacy panel, now retiring, carries the gate.

# 10. What follows

**TODO-STAGE-C.** If the gate passes (or is MARGINAL with the author's recorded decision), Paper B is pre-registered separately and inherits the locked extractor, the selected statistic and floor, the hashed rank tables (including the frozen v0.32 arms for model-version stability), $R^*$ by wave beside $P$ and $C^*$, and the null distributions. If it fails, the result is published as a negative result with the same prominence, and the instrument is redesigned under a new pre-registration.

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

Materials are deposited at OSF, `ec6wh/methodology/v1_10`: the locked pre-registration with its parity record and feasibility note, the input manifest and registry inputs, the anchor record and the deviations record. The scorer (`scripts/score_v1_10.py`) and its tests (`scripts/test_score_v1_10.py`) are in the program repository at tag `v1.10-prereg-r2`. The Stage S outputs (`outputs/selection_v1_10.json`, `outputs/stage_s_v1_10.json` and the 31 hashed rank tables) and the conflict-of-interest flag file (`anchor/coi_flags_v1_10.json`) join the deposit with the Stage C verdicts (`outputs/v1_10_verdicts.json`). The underlying answers are deposited with their source studies.

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

González Castro, P. U. (2026). *AI Presence in Audiophile headphones: AIAS v0.19*. SSRN 6809182.

González Castro, P. U. (2026). *AI Presence in Skincare: AIAS v0.20*. SSRN 6811441.

González Castro, P. U. (2026). *AI Presence in Cosmetics: AIAS v0.21*. SSRN 6815378.

González Castro, P. U. (2026). *AIAS™ v0.22 --- Automotive Substrate: Phantom Brand Persistence on a Heritage-Saturated Category*. SSRN 6829118.

González Castro, P. U. (2026). *AIAS™ v0.23 --- Premium Spirits Substrate*. SSRN 6834298.

Romaniuk, J., & Sharp, B. (2022). *How Brands Grow, Part 2* (Revised ed.). Oxford University Press.

Sharp, B. (2010). *How Brands Grow: What Marketers Don't Know*. Oxford University Press.

Spearman, C. (1910). Correlation calculated from faulty data. *British Journal of Psychology, 3*(3), 271--295.

**TODO (before lock):** cite the early studies (v0.6, v0.9, v0.14, v0.16, v1.0) by their SSRN IDs or OSF copies, checking each against the declined list.
