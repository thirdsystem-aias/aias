---
title: "Situation Sampling, Phantom Brands, Identity Load and Brand Profiles in AI Coverage Answers"
subtitle: "A Pre-Registered Confirmatory Re-Analysis of Coverage Paper A (AIAS™ Methodology v1.19)"
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
  \widowpenalty=10000
  \clubpenalty=10000
  \renewcommand{\topfraction}{0.9}
  \renewcommand{\bottomfraction}{0.8}
  \makeatletter\def\fps@figure{tbp}\makeatother
  \usepackage{booktabs}
  \usepackage{array}
  \renewcommand{\textfraction}{0.07}
  \renewcommand{\floatpagefraction}{0.8}
  \makeatletter\setlength{\@fptop}{0pt}\setlength{\@fpsep}{14pt}\makeatother
---

\begin{titlepage}
\setstretch{1.0}
\setlength{\parskip}{0pt}
\begin{center}

{\LARGE \textbf{Situation Sampling, Phantom Brands, Identity Load\\ and Brand Profiles in AI Coverage Answers}}\\[8pt]

{\large A Pre-Registered Confirmatory Re-Analysis of Coverage Paper A\\ (AIAS™ Methodology v1.19)}\\[28pt]

Pablo Ulpiano González Castro\\[4pt]
School of Visual Arts, MPS Branding Program, New York, NY \textit{(primary academic affiliation)}\\
Third System™ (research entity; data archive and methodology venue)\\[8pt]
Correspondence: pablou@pablou.com · pablou.com\\
ORCID: \href{https://orcid.org/0009-0003-8968-9990}{0009-0003-8968-9990}\\[20pt]

Pre-registration: \texttt{ v1.19-prereg-r1 } (commit \texttt{ 4bc4ce4f85 })\\
locked and deposited on OSF before Coverage Paper A's first call\\[4pt]
Data and code: OSF \texttt{ec6wh}, \texttt{methodology/v1\_19}\\

\end{center}
\end{titlepage}

# Abstract {-}

Coverage Paper A (AIAS Methodology v1.12) introduced Cov*, the rate-adjusted breadth with which AI answers name a brand across 14 buying situations per category, and found it separable from Presence and Consistency. This pre-registered re-analysis of Paper A's answers, locked before Paper A's first model call, tests four further questions on the same 51 rated brands in five categories and the same three models (Claude Fable 5.2, GPT-6 Astra, Gemini 4 Argon), with no new model call.
Situation sampling: over the 64 balanced ways of splitting the 14 situations into two halves, the split-half reliability of Cov* from the median correlation of the halves was 0.459 and the 10th percentile of the per-split reliabilities 0.172, short of the pre-registered 0.50 and 0.30; the set-sampling test is MARGINAL. Dropping the two situations of one cue type moved the brand order beyond the reference range for one of the seven cue types ("with what"; ρ = 0.780 against a 5th percentile of 0.809); the pre-registered rule allows at most one, so the cue-type test is CONFIRMED.
Phantom brands: brands below the programme's recall floor did not differ in Cov* from the other brands (Cliff's δ = -0.062, p = 0.8309), nor after Presence was removed (δ = 0.062, p = 0.8345); both floor tests are FALSIFIED. None of the 126 automotive answers named a defunct brand, so their situation occupancy is UNDETERMINED.
Identity load: 26 brands of the two-channel categories were rated and eligible, below the pre-registered floor of 45, so all three identity-load tests are UNDETERMINED.
Brand profiles: a brand's lean towards a cue type did not repeat in the other situation of the same cue type (mean ρ = -0.022, p = 0.6144); the replication test is FALSIFIED, and under the pre-registered rule no typology is reported. No rated brand had Cov* above 50.
Sensitivity analyses, which never change a verdict, leave both floor tests UNDETERMINED whenever they remove one of the ten rated phantom-flagged brands (the conflict-of-interest variant and four of the five leave-one-category-out variants); at a rating floor of 6 the floor-signature test reads MARGINAL, and the set-sampling test reads FALSIFIED with a mid-p version of the score and UNDETERMINED without the spirits category.

**Keywords:** AI availability; brand availability; AIAS; pre-registration; Ehrenberg-Bass; category entry points; large language models; Coverage; phantom brands; identity load; replication; Double Jeopardy

**JEL codes:** M31; L86, L15, D83, M37

**Paper status:** Pre-registered confirmatory re-analysis, no new model call (tag `v1.19-prereg-r1`, locked and deposited on OSF before Paper A's first call); run once on Paper A's verdict PASS; deviations recorded in `osf/methodology/v1_19/anchor/DEVIATIONS.md` (2 dated entries). Part of the AIAS measurement programme.

# 1. Introduction

AI Availability --- the discoverability and representation of a brand in the outputs of large language models (LLMs) --- has been proposed as a third measurable layer of brand availability (González Castro, 2026, SSRN 6659000), beside the Mental and Physical Availability of the Ehrenberg-Bass tradition (Sharp, 2010; Romaniuk & Sharp, 2016), within the Tri-System framework (González Castro, 2026, MSI Working Paper 26-132). The AIAS programme builds its components one at a time. Presence is whether and how often models name a brand (Methodology v1.6, SSRN 6816340); Consistency is whether the models of a panel agree about a brand (Methodology v1.8, SSRN 6963359; v1.9, *One Score or Two?*).

Coverage asks in how many of a category's buying situations, or category entry points (CEPs; Romaniuk & Sharp, 2016), an AI answer names the brand. Coverage Paper A (Methodology v1.12) fixed 14 brand-free situation questions per category, two for each of seven cue types, asked them to the newest model of each of three providers, and defined the component score Cov*: within each model, the number of situations a brand's mentions touch against the number expected if the brand were named without regard to the situation, given the same number of mentions. Paper A's gate returned PASS: Cov* was separable from Presence, from Consistency and from the brand's naming rate, and orders brands alike on Paper A's two halves of the situations.

Paper A left four questions that its own answers can settle, and its plan of record assigned them to a second paper. Does the brand order depend on which situations happen to be paired (#32)? Are phantom brands --- brands the models rarely name in general questions, and defunct brands --- tied to particular situations (#34)? Are brands that AI names mostly for cultural reasons named across fewer situations (#35, identity load)? And do brands have situation profiles that repeat across situations of the same kind, so that a typology of brands could be built (#36)? This paper reports the four studies under one pre-registration, locked before any Paper A answer existed, and run once after Paper A passed its gate. A fifth question, stability across question wordings (#33), needs a new collection and is not part of this study.

# 2. Method

## 2.1 Data

The study uses Paper A's answers and no new collection: one answer per category, model, situation and run, the set of registry brands it names, rebuilt with Paper A's own locked functions (`load_probes`, `probe_design`, `dedupe_calls`, `build_analysis`), imported from Paper A's locked scorer and not copied. The units are Paper A's 112 brands in five categories (v0.19 audiophile headphones, 16 brands; v0.20 skincare, v0.21 cosmetics, v0.22 automotive and v0.23 premium spirits, 24 each). The panel is Paper A's primary panel, recorded as N3 (Claude Fable 5.2, GPT-6 Astra, Gemini 4 Argon), search off. Cov*, its rating floor (at least 14 mentions by the panel, named by at least two models), the split-half rule and the pooled within-category Spearman $\rho_w$ are Paper A's definitions by import (v1.12 §2.4 and §2.6). 51 brands were rated. Presence $P$ is Paper A's comparator column, computed from the same models' $t_4$ answers (v0.42).

The **excess situation profile** of brand $b$ sets, for each cue type $W$, the observed mentions of $b$ in $W$'s situations against their expectation under Paper A's situation-blind null with the same number of mentions, summed over the panel's models and divided by the brand's mentions: seven numbers that sum to zero; a positive value means the brand is named in that cue type's situations more than situation-blind naming would give. It is computed on all 14 situations and on each half (one situation per cue type).

Identity load (#35) is computed on the $t_4$ Phase B answers of the same three models (v0.42): $\text{IL}_b = k_{b,\text{cult}}/n_{\text{cult}} - k_{b,\text{cat}}/n_{\text{cat}}$, the difference between the shares of cultural-channel and category-channel answers naming $b$, on the two-channel categories (skincare, cosmetics, automotive) only, eligible when the brand is named in some but not all answers. Phantom brands (#34) are, for the main test, the programme's frozen recall-floor flags (mean $t_1$ recall below 1.0 on the legacy six-model panel; 57 of the 112 units, frozen in the pre-registration's roster), and for the occupancy test the five defunct automotive brands of the v0.22 registry (Pontiac, Oldsmobile, Plymouth, Mercury, Saturn), with Fisker reported beside them.

## 2.2 Order of lock and data

Pre-registration §9 makes the confirmatory label conditional on order: if Paper A's answers had been coded or scored before this study locked, every test would be labelled exploratory. The git record and `anchor/DEVIATIONS.md` give the order. The pre-registration was locked at tag `v1.19-prereg-r1` on commit `4bc4ce4f85`, committed on 13 November 2026 at 10:17 CT (16:17 UTC); DEVIATIONS Entry 1, written at the lock and before the tag, records the lock time ex ante and its cause (a service outage delayed it past its planned time; nothing in the text changed). The OSF deposit was verified and the anchor record naming the tag's commit was committed on 13 November 2026 at 11:01 CT (17:01 UTC) (commit `5974fcc`). Paper A's collection window opened on 14 November 2026 at 00:00 UTC, as the anchor record states; Paper A's answers were committed on 13 November 2026 at 20:00 CT (02:00 UTC, 14 November) (commit `b89ff1f`), and its coding and scoring were committed on 14 November 2026 at 06:25 CT (12:25 UTC) (commit `949be61`). This study was therefore locked before Paper A's first call and before its coding and scoring, and its tests are **confirmatory**. The scorer ran once, after Paper A's verdict existed, and its output was committed on 14 November 2026 at 13:45 CT (19:45 UTC) (commit `6e8f157`).

## 2.3 Tests

Every test was fixed in the pre-registration with its statistic, bands and seed (Table 1). Permutation tests use 10,000 draws; the gap statistic uses 500 reference sets. $\alpha = 0.05$ per test with no multiplicity correction (programme convention); every test is reported as it fell.

Table: Pre-registered tests (pre-registration §3, §5--§7). $\widetilde{\text{rel}}$: split-half reliability $2\tilde r/(1+\tilde r)$ of the median correlation over splits; P10: 10th percentile of the per-split reliabilities.

| Test | Tier | Statistic | Rule |
|:----------------------|:---------|:-----------------------------------|:----------------------------------|
| H32_SetSampling | primary | $\widetilde{\text{rel}}$ and P10 over the 64 balanced half splits | CONFIRMED: $\widetilde{\text{rel}} \geq 0.50$, $p < .05$, P10 $\geq 0.30$; FALSIFIED: $\widetilde{\text{rel}} < 0.30$ or $p \geq .05$ |
| H32_CueType | secondary | $\rho_w(\text{Cov}^*, \text{Cov}^*_{-W})$ against 84 reference drops | CONFIRMED: at most 1 of 7 cue types below the reference 5th percentile; MARGINAL: 2; FALSIFIED: 3 or more |
| H34_Floor_Signature | primary | Cliff's $\delta$ of Cov*, flagged against other brands, within category | CONFIRMED: $|\delta| \geq 0.30$, $p < .05$ (sign named); FALSIFIED: $|\delta| < 0.15$; at least 10 flagged and 10 other rated brands |
| H34_Floor_BeyondPresence | secondary | the same on Cov* residualised on $P$ | as above |
| H34_Defunct_Occupancy | secondary | largest cue-type share of automotive answers naming a defunct brand | CONFIRMED: $p < .05$ and share $\geq 0.40$; UNDETERMINED below 10 answers |
| H35_IL_Coverage | primary | $\rho_w(\text{IL}, \text{Cov}^*)$ | CONFIRMED: $|\rho_w| \geq 0.30$, $p < .05$; FALSIFIED: $|\rho_w| < 0.15$; UNDETERMINED below 45 units |
| H35_IL_Robust | secondary | partial $\rho$ of IL and Cov* given $P$ | cell matrix (pre-registration §6.4) |
| H35_IL_CueType | secondary | $\rho_w$(IL, excess in with whom + how feeling) | as H35_IL_Coverage, sign reversed |
| H36_Profile_Replication | primary | $R$: mean over cue types of $\rho_w$ of the half-A and half-B excess profiles | CONFIRMED: $R \geq 0.20$, $p < .05$; FALSIFIED: $R < 0.10$ or $p \geq .05$ |
| H36_Structure | secondary | Ward clusters of the profiles, gap statistic, silhouette, ARI with Presence tiers | NO TYPOLOGY if H36_Profile_Replication is FALSIFIED or UNDETERMINED; otherwise an exhaustive cell matrix |

The splits of H32_SetSampling put one situation of each cue type in each half; split 0 is Paper A's own split (all A-labelled situations against all B). Cliff's $\delta$ (Cliff, 1993) is pooled over within-category pairs; the residualised arm regresses centred within-category ranks of Cov* on those of $P$. The typology arm follows the Consistency arc's v0.36 criteria, with the number of types chosen by the gap statistic and its one-standard-error rule (Tibshirani, Walther & Hastie, 2001).

## 2.4 Sensitivity analyses

Eight sensitivity analyses were pre-registered; they are reported beside each verdict and never change one (pre-registration §8): S-COI, every test without Denon and without Chevrolet, BMW, Bentley, Jack Daniel's and Eucerin (pre-registration §8 and §14; Declarations); S-Floor6, Cov* at a rating floor of 6; S-C3, the continuity panel with Claude Opus 5.5 in place of Claude Fable 5.2; S-Equal, Paper A's equal-weight null; S-LOCO, leaving out one category at a time (five variants); S-IL-t1, the published $t_1$ identity load in place of the $t_4$ one; S-F-noD, the flagged set without the five defunct brands; and S-Mid, Paper A's mid-$p$ $\beta$.

## 2.5 Pre-registration and deviations

The pre-registration (revision r1) was locked at tag `v1.19-prereg-r1` with a lock manifest of 21 files, and deposited on OSF (`ec6wh`, `methodology/v1_19/`) with the SHA-256 of every locked file verified there before the anchor record was written. The scorer (`score_v1_19.py`) was written and tested on synthetic data before the lock; it refuses to run unless the tag is public, the anchor names its commit and Paper A's scored outputs exist, and it ran once. Before any statistic it checked that the imported Paper A scorer carries Paper A's locked SHA-256 (B-P0, passed) and that Cov* recomputed with the imported code equals Paper A's unit table for all 112 units (B-P1, passed). Deviations are recorded in `osf/methodology/v1_19/anchor/DEVIATIONS.md` (2 dated entries, both ex ante): Entry 0 records what was read while drafting and the conflict-of-interest handling; Entry 1 records the lock time (§2.2). One discrepancy found after the run is reported in §5; it changes no verdict, and the pre-registration is unchanged.

# 3. Results

## 3.1 The run

Paper A's verdict was PASS, so the study ran (pre-registration §1). The run read Paper A's verdict file (SHA-256 `0c70bde1`…) and unit table (`06b78750`…), and the $t_4$ answers of v0.42 for identity load; both parity gates passed. Table 2 gives every verdict as the scorer wrote it.

Table: Verdicts on the primary panel, as written by the scorer (`outputs/v119_verdicts.json`).

| Study | Test | Tier | Result | Verdict |
|:------|:--------------------------|:----------|:-----------------------------------------|:---------------|
| #32 | H32_SetSampling | primary | $\widetilde{\text{rel}}$ = 0.459, P10 = 0.172, $p$ = 0.0001 | **MARGINAL** |
| #32 | H32_CueType | secondary | 1 of 7 cue types below the reference 5th percentile | **CONFIRMED** |
| #34 | H34_Floor_Signature | primary | $\delta$ = -0.062, $p$ = 0.8309 (10 flagged, 41 other) | **FALSIFIED** |
| #34 | H34_Floor_BeyondPresence | secondary | $\delta$ = 0.062, $p$ = 0.8345 ($n$ = 51) | **FALSIFIED** |
| #34 | H34_Defunct_Occupancy | secondary | 0 of 126 answers name a defunct brand | **UNDETERMINED** |
| #35 | H35_IL_Coverage | primary | $n$ = 26 (floor 45) | **UNDETERMINED** |
| #35 | H35_IL_Robust | secondary | not computed below the floor | **UNDETERMINED** |
| #35 | H35_IL_CueType | secondary | not computed below the floor | **UNDETERMINED** |
| #36 | H36_Profile_Replication | primary | $R$ = -0.022, $p$ = 0.6144 ($n$ = 44) | **FALSIFIED** |
| #36 | H36_Structure | secondary | $k$ = 1; matrix cell | **NO TYPOLOGY** |

## 3.2 Sensitivity to the choice of situations (#32)

**Set sampling (H32_SetSampling).** All 64 of the 64 balanced splits met Paper A's floor, with 33 to 47 brands rated on both halves. The correlation of the halves' Cov* ranged from -0.074 to 0.544 across splits; its median was $\tilde r$ = 0.298, a split-half reliability of $\widetilde{\text{rel}}$ = 0.459 (one-sided $p_{\text{perm}}$ = 0.0001), and the 10th percentile of the per-split reliabilities was P10 = 0.172. $\widetilde{\text{rel}}$ is below 0.50 but not below 0.30, $p < .05$, and P10 is below 0.30, so H32_SetSampling is **MARGINAL**: Cov* orders brands alike on disjoint halves of the situations more than chance would, but less strongly than Paper A's reliability band asks, and in at least a tenth of the splits the reliability is below 0.30, the band in which Paper A's reliability leg would have been falsified. Paper A's own split (split 0, reliability 0.646 on 42 brands) lies at the 93.75th percentile of the 64 splits (Figure 1).

![Split-half reliability of Cov* for each of the 64 balanced splits of the 14 situations, sorted; split 0 is Paper A's split. ](../../reports/figs/v119/chart_01_split_reliability.pdf){#fig:split width=94%}

**Cue type (H32_CueType).** Over the 84 reference drops of two situations of different cue types, $\rho_w(\text{Cov}^*, \text{Cov}^*_{\text{drop}})$ had a median of 0.908 and a 5th percentile of 0.809. Dropping the two situations of one cue type gave correlations from 0.780 to 0.941 (Table 3); only "with what" fell below the reference 5th percentile (0.780 against 0.809). The pre-registered rule allows at most one cue type below it, so H32_CueType is **CONFIRMED**, the outcome the pre-registration labels "no single cue type carries the order" (Figure 2).

![Rank correlation of Cov* on all 14 situations with Cov* after dropping the two situations of each cue type, against the reference distribution of drops across cue types. ](../../reports/figs/v119/chart_02_cue_type_drop.pdf){#fig:cue width=90%}

Table: Per cue type: rank correlation of Cov* with Cov* after dropping the cue type's two situations (H32_CueType; reference 5th percentile 0.809), and the half-A to half-B correlation of the excess profile (H36_Profile_Replication).

| Cue type | $\rho_w(\text{Cov}^*, \text{Cov}^*_{-W})$ | $n$ | Below reference | Profile replication $\rho_w$ |
|:--------------|-----------:|----:|:----------|-----------:|
| why | 0.910 | 49 | no | -0.117 |
| when | 0.930 | 49 | no | 0.056 |
| where | 0.845 | 49 | no | 0.063 |
| while | 0.833 | 49 | no | 0.071 |
| with whom | 0.941 | 49 | no | -0.205 |
| with what | 0.780 | 47 | yes | -0.037 |
| how feeling | 0.937 | 48 | no | 0.016 |

## 3.3 Phantom brands (#34)

**Recall-floor brands (H34_Floor_Signature).** 10 of the rated brands carry the recall-floor flag and 41 do not; the flagged brands are 3 headphone brands, 1 skincare brand, 1 cosmetics brand and 5 spirits brands, so the contrast is pooled over four categories (v0.19, v0.20, v0.21 and v0.23). Cliff's $\delta$ of Cov* between flagged and other brands within category was -0.062 (two-sided $p_{\text{perm}}$ = 0.8309). $|\delta|$ is below 0.15, and H34_Floor_Signature is **FALSIFIED**: by Cov*, brands below the recall floor are not more situation-bound than other brands (Figure 3).

**Beyond Presence (H34_Floor_BeyondPresence).** On Cov* residualised on Presence within category, over 51 brands, $\delta$ = 0.062 ($p_{\text{perm}}$ = 0.8345); H34_Floor_BeyondPresence is **FALSIFIED**. The two arms fall in the same band, so the primary is not labelled Presence-sensitive.

![Cov* of rated brands with and without the recall-floor flag, by category (left), and against Presence $P$ (right). ](../../reports/figs/v119/chart_03_floor_flag.pdf){#fig:floor width=100%}

**Defunct brands (H34_Defunct_Occupancy).** Of the 126 answers of the primary panel to automotive situations, 0 named Pontiac, Oldsmobile, Plymouth, Mercury or Saturn, and 0 named Fisker. With fewer than 10 such answers the test is **UNDETERMINED** (the scorer's reason: "fewer than 10 answers name a defunct brand"); the descriptive naive and caveated mention counts (D34) sum to 0. The automotive questions ask for brands to buy new, and on these answers the models did not name a defunct brand.

## 3.4 Identity load (#35)

26 brands of the two-channel categories were rated and had an eligible identity load (6 skincare, 12 cosmetics and 8 automotive). The pre-registered floor is 45 units, set by v0.37's power analysis, and none of the three tests was computed: H35_IL_Coverage, H35_IL_Robust and H35_IL_CueType are **UNDETERMINED** (the scorer's reason: "n < 45 or fewer than 3 trio categories"). Under S-IL-t1, the published $t_1$ identity load, they are UNDETERMINED as well. The study therefore says nothing about whether culture-led brands are named across fewer situations.

## 3.5 Brand profiles and typology (#36)

**Profile replication (H36_Profile_Replication).** Over 44 brands in 5 categories rated on all 14 situations with at least seven mentions in each half, the correlation of the half-A and half-B excess profiles ranged by cue type from -0.205 to 0.071 (Table 3, Figure 4); their mean was $R$ = -0.022 (one-sided $p_{\text{perm}}$ = 0.6144). $R$ is below 0.10, and H36_Profile_Replication is **FALSIFIED**: a brand's lean towards a kind of situation, measured in one situation, does not repeat in the other situation of the same kind.

![Correlation of each brand's excess profile between the two halves of the situation set, by cue type, against the replication bands. ](../../reports/figs/v119/chart_04_profile_replication.pdf){#fig:rep width=90%}

**Structure (H36_Structure).** Because profile replication was falsified, the pre-registered matrix assigns the cell "NO TYPOLOGY (profiles do not replicate); structure reported descriptively". For the record: on the 14-situation profiles of 51 brands the gap statistic chose $k$ = 1 type, and on the profiles residualised on Presence $k$ = 1, so no silhouette was computed; the adjusted Rand index between the single cluster and the Presence tiers was 0.000 ($p$ = 1.000).

**Double Jeopardy map and category profiles (D36, descriptive).** No rated brand had Cov* above 50, the value of situation-blind naming: of the 51 brands, 23 with Presence above the category median and 28 below it are all situation-bound, and none is broad. Category mean excess profiles stayed small, from -0.040 to 0.071 of a brand's mentions per cue type (Figure 5). These descriptives carry no verdict.

![Mean excess situation profile per category and cue type: observed share of a brand's mentions in the cue type's situations minus the share expected under situation-blind naming, averaged over rated brands. ](../../reports/figs/v119/chart_05_category_profiles.pdf){#fig:prof width=92%}

## 3.6 Sensitivity analyses

Table 4 lists, for each pre-registered sensitivity, the tests it re-ran and every verdict that differs from the primary one; sensitivities never change a verdict. S-C3, S-Equal, S-LOCO without automotive, S-IL-t1 and S-F-noD change no verdict. Both floor tests become UNDETERMINED whenever a variant removes one of the ten rated flagged brands, because the test needs at least 10: S-COI removes Eucerin, and leaving out headphones, skincare, cosmetics or spirits removes that category's flagged brands (automotive holds none). At a rating floor of 6, H34_Floor_Signature is MARGINAL. With Paper A's mid-$p$ $\beta$, H32_SetSampling is FALSIFIED, and without the spirits category it is UNDETERMINED.

Table: Pre-registered sensitivity analyses (§2.4): the studies each re-ran and every verdict that differs from the primary one (primary $\rightarrow$ sensitivity). Sensitivities never change a verdict.

| Sensitivity | Studies | Verdicts that differ from the primary |
|:----------------------------|:--------------|:--------------------------------------------------|
| S-COI (six brands out) | #32, #34, #35, #36 | H34_Floor_Signature: FALSIFIED → UNDETERMINED; H34_Floor_BeyondPresence: FALSIFIED → UNDETERMINED |
| S-Floor6 (floor 6) | #34, #35, #36 | H34_Floor_Signature: FALSIFIED → MARGINAL |
| S-C3 (panel C3) | #32, #34, #35, #36 | none |
| S-Equal (equal-weight null) | #32, #36 | none |
| S-LOCO without headphones | #32, #34, #35, #36 | H34_Floor_Signature: FALSIFIED → UNDETERMINED; H34_Floor_BeyondPresence: FALSIFIED → UNDETERMINED |
| S-LOCO without skincare | #32, #34, #35, #36 | H34_Floor_Signature: FALSIFIED → UNDETERMINED; H34_Floor_BeyondPresence: FALSIFIED → UNDETERMINED |
| S-LOCO without cosmetics | #32, #34, #35, #36 | H34_Floor_Signature: FALSIFIED → UNDETERMINED; H34_Floor_BeyondPresence: FALSIFIED → UNDETERMINED |
| S-LOCO without automotive | #32, #34, #35, #36 | none |
| S-LOCO without spirits | #32, #34, #35, #36 | H32_SetSampling: MARGINAL → UNDETERMINED; H34_Floor_Signature: FALSIFIED → UNDETERMINED; H34_Floor_BeyondPresence: FALSIFIED → UNDETERMINED |
| S-IL-t1 ($t_1$ identity load) | #35 | none |
| S-F-noD (flags without defunct) | #34 | none |
| S-Mid (mid-$p$ $\beta$) | #32, #34 | H32_SetSampling: MARGINAL → FALSIFIED |

# 4. Discussion

The four studies give a mixed and mostly negative result for the structure of Coverage beyond its scalar score. First, Cov* is less reliable across samples of situations than Paper A's single split suggested. Paper A's split-half reliability (0.646) lies at the 93.75th percentile of the 64 ways in which the same 14 situations could have been halved; the reliability from the median correlation over the splits (0.459) is marginal, and at least a tenth of the splits fall below 0.30 (0.172). Dropping a cue type moved the order beyond the reference range only for "with what", within the pre-registered allowance of one (CONFIRMED). Paper A's verdict is not re-decided here; the reading for the programme is that Cov* on 14 situations orders brands with moderate stability, and that a larger or independently written set of situations (#32b) is needed before brand-level differences in Cov* are read as precise.

Second, on these data Coverage carries no phantom-brand signature: brands the legacy models rarely named are not more situation-bound by Cov* than others, raw or after Presence is removed. The falsification rests on ten rated flagged brands and turns UNDETERMINED when any of them is removed, and at a floor of 6 the primary test is MARGINAL; it is no evidence of a signature at this size, not evidence of its absence in larger panels. The defunct-brand question could not be asked: no automotive answer named a defunct brand.

Third, the identity-load questions were not answered: only 26 rated brands of the two-channel categories had an eligible identity load, against a floor of 45. Fourth, brands showed no replicable situation profile ($R$ = -0.022), so the study reports no typology; every rated brand was situation-bound by Cov*, so the Double Jeopardy map has no broad brands to contrast. Together with Paper A, the result supports Cov* as a single breadth score with moderate reliability and gives no support, on 14 situations, three runs and three models, for finer situation profiles or brand types.

# 5. Limitations

All four studies re-use Paper A's single set of 14 situations per category, drafted by one procedure and by a model that is also a panel model; #32 measures sensitivity within that design, not across authoring procedures. Half profiles rest on one situation per cue type, which makes the replication test conservative, and the cluster test is weak at about 50 rated brands. Fewer brands were rated than the identity-load floor needs, and the floor tests rest on ten flagged brands. The recall-floor flags come from the legacy six-model panel at $t_1$, while Cov* comes from the newest models; brands may have moved since. The study covers one market and language (US English), search off only, and registry brands only. No multiplicity correction is applied; every one of the ten verdicts is reported.

One discrepancy was found after the run. Pre-registration §6.2 says that the sensitivity S-IL-t1 reads v0.37's $t_1$ identity load "with v0.37's hash check"; the scorer reads the same file and columns but records the file's SHA-256 (`45009bce`…) instead of running v0.37's check. It cannot change a verdict: the three identity-load tests are UNDETERMINED under the primary identity load and under S-IL-t1 alike, because too few brands are eligible. It is reported here; the pre-registration is unchanged.

# 6. Future Research

A parallel, independently written set of situations with buyer weights (#32b) and question wordings (#33) need new collections under their own pre-registrations; the re-asked original wording in #33 would also re-test the reliability of Cov* on new answers. More situations per cue type, or more runs, would raise the number of rated brands, which identity load (#35) and the floor tests need, and would give half profiles more than one situation per cue type.

# Declarations {-}

## Conflict of interest {-}

The author is Director, Corporate Brand Creative and Governance at Samsung Electronics America. Samsung does not market brands in skincare, cosmetics, passenger cars or premium spirits. In audiophile headphones, Samsung's subsidiary Harman International owns brands in the category; v0.19 substituted Denon for AKG before its pre-registration lock because AKG's parent, Harman International, is a Samsung subsidiary. This study performs no new brand selection: it uses the registries fixed in v0.19--v0.23 (in Paper A's answers and in the $t_4$ answers of v0.42 that supply identity load), and each keeps its source-phase handling. In the automotive registry, Samsung subsidiaries hold tier-2/3 component supply relationships with several registry brands --- Harman International (audio systems), Samsung SDI (battery cells) and Samsung Display (infotainment) --- characterized in the source phase as non-competitive, with no brand-level overlap, and imposing no operational restriction on registry composition (v0.22 Declarations; screened in v0.22 DEVIATIONS Entry 0, Part B). Correction (November 10, 2026): Denon, which replaced AKG in the v0.19 registry, has itself been owned by Harman International, a wholly owned subsidiary of Samsung Electronics, since September 23, 2025, when Harman completed its acquisition of Sound United from Masimo; the v0.19 headphones registry therefore includes one Samsung-group brand. The substitution did not achieve its purpose, and this was not noticed until November 10, 2026. Source: HARMAN press release, Business Wire, September 23, 2025. Cheil Worldwide, a marketing company of the Samsung group in which Samsung Electronics holds 28.43%, or its agency Iris has done advertising, public-relations or search-marketing work for five registry brands: Chevrolet (for GM Korea, 2017), BMW (UK consumer public relations, 2018), Bentley (experiential agency of record in the Americas from 2021), Jack Daniel's (UK digital agency from 2022, since replaced) and Eucerin (search marketing for Beiersdorf from 2024). (Conflict-of-interest screen of v0.62, DEVIATIONS Entry 0, Part F.) As Denon, these five brands stay in every analysis, and every test is also reported without them and Denon (sensitivity S-COI). The situation questions of Paper A, whose answers this study re-analyses, name no brand; headphone situations stay inside audiophile listening, because consumer, sport and true-wireless uses are where Samsung-owned brands compete. Brands outside the registries named in answers, which may include Samsung-owned brands, are not scored and their mentions are not counted. This study makes no model call; its scoring is automated against the locked registries, and its pre-registration was locked and deposited before Paper A's first call. Samsung Electronics had no role in the design, conduct, analysis or reporting of this work.

## Funding {-}

Self-funded. No external funding supported this research.

## Ethics {-}

Not applicable; no human subjects. The study re-analyses answers that large language models gave under their public interfaces (Paper A and v0.42); it makes no new query.

## Use of AI tools {-}

During the preparation of this work the author used AI tools (Anthropic's Claude) to assist with study design, analysis and writing. The author reviewed and edited all content and takes full responsibility for it.

## Data and code availability {-}

Materials are deposited at OSF (osf.io/ec6wh), `methodology/v1_19/`: the locked pre-registration with its phantom roster and its builder, the scorer and its tests, the dry-run records, the lock manifest and the anchor record (`prereg/`, `scripts/`, `dryrun/`, `anchor/`); the verdict file (`v119_verdicts.json`) and the run log (`outputs/`, deposited on 14 November 2026); and this paper's PDF and its Markdown source (`paper/`). Paper A's answers, coded mention tables, verdict file and unit table are in Paper A's deposit (`methodology/v1_12/`). The pre-registered code is in the programme's GitHub repository (github.com/thirdsystem-aias/aias) at tag `v1.19-prereg-r1`; the scripts that fill this paper and draw its figures are on the branch `v1.19-paper`.

# References {-}

Cliff, N. (1993). Dominance statistics: Ordinal analyses to answer ordinal questions. *Psychological Bulletin*, 114(3), 494--509.

González Castro, P. U. (2026). *AI Availability: Extending Mental and Physical Availability into Algorithmic Retrieval*. SSRN 6659000.

González Castro, P. U. (2026). *Tri-System Brand Growth: The AI Mediation Layer*. MSI Working Paper, Report No. 26-132. Marketing Science Institute.

González Castro, P. U. (2026). *The AIAS™ Presence Measurement Protocol: Methodological Notes on Construct Validity and the Four-Regime Taxonomy* (v1.2). SSRN 6761698.

González Castro, P. U. (2026). *The AIAS Presence Measurement Protocol: Phase A Pivot-Validation Specification (v1.3)*. SSRN 6797679.

González Castro, P. U. (2026). *The AIAS Presence Measurement Protocol v1.4: Recognition × Recall Decomposition and Multi-Component AI Availability*. SSRN 6799479.

González Castro, P. U. (2026). *The AIAS™ Presence Measurement Protocol: Multi-Statistic C2 Specification and Two-Channel Recall Decomposition* (v1.5). SSRN 6810758.

González Castro, P. U. (2026). *Substrate Pre-Screening, Independent Moderator Pathway, and Phantom Brand Persistence Phase B Extension* (AIAS Methodology v1.6). SSRN 6816340.

González Castro, P. U. (2026). *Consistency without Independence: A Pre-Registered Test of Coefficient-of-Variation as the Consistency Component of AIAS™* (v1.7). SSRN 6878818.

González Castro, P. U. (2026). *A Mean-Independent Consistency Instrument for Cross-Model AI Presence: Redesigning CPC on a Quasi-Binomial Dispersion Basis* (AIAS Methodology v1.8). SSRN 6963359.

González Castro, P. U. (2026). *One Score or Two? Calibrating a Presence and Consistency Composite for AI Brand Availability: A Pre-Registered Calibration with Blind Five-Month Confirmation (AIAS™ Methodology v1.9)*. Third System, <https://thirdsystem.ai/studies/v1-9/> (PDF: <https://thirdsystem.ai/files/papers/v1_9_ssrn_paper.pdf>); OSF, <https://osf.io/ec6wh/files/osfstorage/6af1fd459966c813ee53ba87>.

González Castro, P. U. (2026). *Coverage of Buying Situations in AI Answers about Brands: Instrument, Cross-Category Baseline and Separability Gate for a Third Component of AI Availability (AIAS™ Methodology v1.12)*. Third System, <https://thirdsystem.ai/studies/v1-12/> (PDF: <https://thirdsystem.ai/files/papers/v1_12_ssrn_paper.pdf>); OSF, <https://osf.io/ec6wh/> (methodology/v1_12/paper).

González Castro, P. U. (2026). *AI Availability as a Third Measurable Layer of Brand Availability: Five-Substrate Empirical Anchoring of the AIAS™ Presence Measurement Protocol --- Synthesis under Locked v1.6 Methodology* (AIAS 1.0). SSRN 6817841.

González Castro, P. U. (2026). *Presence and Consistency: A Two-Component Measurement of AI Availability. The AIAS™ 2.0 Synthesis*. OSF `ec6wh/aias_2_0`.

Programme records cited by version, as the locked pre-registration names them (OSF `ec6wh`; github.com/thirdsystem-aias/aias): the omnibus registries of v0.19--v0.23; the $t_1$ recall-floor flags of v0.31; the Consistency re-analyses v0.35 (phantom brands), v0.36 (regime emergence) and v0.37 (identity load), whose bands and criteria are reused; and the $t_4$ wave v0.42.

Romaniuk, J., & Sharp, B. (2016). *How Brands Grow: Part 2*. Oxford University Press.

Sharp, B. (2010). *How Brands Grow: What Marketers Don't Know*. Oxford University Press.

Tibshirani, R., Walther, G., & Hastie, T. (2001). Estimating the number of clusters in a data set via the gap statistic. *Journal of the Royal Statistical Society: Series B*, 63(2), 411--423.
