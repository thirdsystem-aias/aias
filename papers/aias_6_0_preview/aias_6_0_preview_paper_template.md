---
title: "AIAS™ 6.0 Preview (provisional): Are the Six Parts of AI Availability Separate Readings of a Brand?"
subtitle: "A Pre-Registered Structure Test of Six Provisional Components on the Newest Models"
date: "{{PAPER_DATE}}"
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
  \usepackage{longtable}
  \usepackage{graphicx}
  \renewcommand{\textfraction}{0.07}
  \renewcommand{\floatpagefraction}{0.8}
  \makeatletter\setlength{\@fptop}{0pt}\setlength{\@fpsep}{14pt}\makeatother
---

\begin{titlepage}
\setstretch{1.0}
\setlength{\parskip}{0pt}
\begin{center}

{\LARGE \textbf{AIAS™ 6.0 Preview (provisional)}}\\[8pt]

{\large Are the Six Parts of AI Availability Separate Readings of a Brand?\\ A Pre-Registered Structure Test of Six Provisional Components on the Newest Models}\\[28pt]

Pablo Ulpiano González Castro\\[4pt]
School of Visual Arts, MPS Branding Program, New York, NY \textit{(primary academic affiliation)}\\
Third System™ (research entity; data archive and methodology venue)\\[8pt]
Correspondence: pablou@pablou.com · pablou.com\\
ORCID: \href{https://orcid.org/0009-0003-8968-9990}{0009-0003-8968-9990}\\[20pt]

Pre-registration: \texttt{ {{PREREG_TAG}} } (commit \texttt{ {{PREREG_COMMIT}} }; deposited on OSF before any $t_4$-based component score existed)\\
Data and code: OSF \texttt{ec6wh}, \texttt{aias\_6\_0\_preview}\\
{% if SYNTHETIC %}
\vspace{14pt}\textbf{SYNTHETIC TEST BUILD: every number in this document comes from synthetic files. Not results.}\\
{% endif %}
{% if CLASS_C_DRAFT %}
\vspace{8pt}\textbf{Class C (H\_Structure FALSIFIED): drafting paused under the pre-registration (§6.6); internal draft for the options memo, not for release.}\\
{% endif %}

\end{center}
\end{titlepage}

# Abstract {-}

The AIAS programme describes a brand's AI Availability in six parts: whether AI answers name the brand (Presence), how evenly models name it (Consistency), where it sits in an answer's list (Ranking), how answers describe it (Sentiment), across how many buying situations it is named (Coverage) and what search-on answers rest on (Grounding). Each part is first tested on its own, against Presence and Consistency, in its own pre-registered Paper A. This provisional synthesis asks the question no Paper A can: on one panel and one wave, are the parts that passed their own gates still separate from each other when all of them are measured on the same brands? Its analysis plan was locked before any score on the newest models existed. It reads each part's locked score for the 112 brand units of five categories on the newest flagship model of each of three providers in the week of the fourth omnibus wave, includes a part only in the state its own gate gives it, and tests every pair of included parts (pairwise separability) and every part against all earlier parts together (incremental separability). {{K_SENTENCE}}
{{HEADLINE}} {{W1_SENTENCE}}{% if W2 %} {{W2_SENTENCE}}{% endif %}{% if RANK_SHOWN %} {{RANK_ABSTRACT}}{% endif %}
No composite score is computed: the parts are reported side by side, and every part other than Presence and Consistency stays provisional until its own validation.

**Keywords:** AI availability; brand measurement; large language models; construct structure; discriminant validity; pre-registration

\clearpage

# 1. Introduction

AI Availability --- the discoverability and representation of a brand in the outputs of large language models (LLMs) --- has been proposed as a third layer of brand availability (González Castro, 2026a) beside the Mental and Physical Availability of the Ehrenberg-Bass tradition (Sharp, 2010; Sharp & Romaniuk, 2021), within the Tri-System framework (González Castro, 2026l). The AIAS™ programme builds the score one part at a time, each pre-registered and locked before it is used, on the Presence measurement protocol (González Castro, 2026b, 2026c, 2026d, 2026e). Presence is whether and how often models name a brand (Methodology v1.6: González Castro, 2026f), anchored across five categories in AIAS 1.0 (González Castro, 2026j). Consistency is how evenly the models of a panel name it: the first Consistency instrument failed its separability test because it moved with how often a brand is named (v1.7: González Castro, 2026g); its replacement measures the dispersion statistic $\varphi$ (v1.8: González Castro, 2026h), scaled to $C^*$ without a composite (v1.9: González Castro, 2026i). The AIAS 2.0 synthesis reported Presence and Consistency side by side and showed them separable on the retiring six-model panel (González Castro, 2026k).

Four further parts are in their first tests: Ranking (where a brand sits in an answer's list; Methodology v1.10, whose statistic did not clear separability from Presence, and its redesign v1.14), Sentiment (how answers describe a brand; v1.11, AI-judged), Coverage (across how many buying situations a brand is named; v1.12) and Grounding (what search-on answers rest on; v1.13). Each Paper A tests its part against Presence and Consistency. None can test the parts against one another on the same brands, models and week, because no archived panel carries all six: the retiring panel never answered buying-situation questions and never searched.

This Preview does that test, provisionally. It comes before any Paper B and before the validated releases, and it says so in every result. It asks whether the parts that passed their own gates are separate readings of a brand on the newest models (the structure question), whether AIAS 2.0's Presence--Consistency separability holds off the retiring panel, which brands carry a full profile, and whether any equal-weight composite would pass the constraints v1.9 set (descriptive only). Its unfavourable outcomes are pre-specified with the same prominence as its favourable ones, including a class in which drafting pauses and the author decides the direction.

# 2. Method

The method is the locked pre-registration (§2.9); section numbers in parentheses refer to it. The Preview collects nothing and makes no model call: it reads each part's locked score and computes statistics locally.

## 2.1 Units, panel, wave and condition

The units are the 112 brand units of the five omnibus registries (v0.19 audiophile headphones, 16; v0.20 skincare, v0.21 cosmetics, v0.22 automotive and v0.23 premium spirits, 24 each), unchanged since the first wave; a brand named in two registries is two units (§2). The panel, N3, is the newest generally available flagship of each of three providers: Claude Fable 5.2, GPT-6 Astra and Gemini 4 Argon. The wave is $t_4$, the fourth omnibus wave (v0.42); Coverage comes from v1.12's own collection on the same three models in the same week, and the two are treated as one wave ("the $t_4$ week"). Presence, Consistency, Ranking, Sentiment and Coverage are read from search-off answers; Grounding is defined on search-on answers. Every score is oriented so that higher means more of the reading; signs are reported and separability verdicts use $\lvert\rho\rvert$.

## 2.2 The six parts and where they are read

The Preview computes no part's score; it reads each unit-level score, its rated flag and its gate verdict from the part's locked output, checks the file's hash against the part's own record, and never imputes a unit a part leaves unrated (§3).

Table: The six parts as the Preview reads them (§3).

| Part | Score | Read from |
|:------------|:--------------------------------------------------------|:--------------------------|
| Presence | $P = 100\,(C_P/3 + 2\hat\pi)/3$ on N3, search off | v0.42 brand and coded tables; recomputed with v1.14's locked function as a parity check |
| Consistency | $C^* = 100\,(1 - \varphi/9)$ on N3, rated with at least six mentions | as Presence |
| Ranking | $R^*$, v1.14's modal position (higher = nearer the top), rated at six rankable mentions | v1.14 Stage 1 (and Stage 2 when it exists) |
| Sentiment | $S$, v1.11's AI-judged score applied to the $t_4$ answers, only if that application is separately pre-registered, locked and scored | the $t_4$ Sentiment study's output |
| Coverage | Cov\*, v1.12's breadth across 14 buying situations against a situation-blind null | v1.12's unit table and verdicts |
| Grounding | $G^* = 100 \times$ own-domain share of grounded search-on answers, rated at six | v1.13's verdict file |

## 2.3 Reading each part's gate and the included set

Each part enters in the state its own gate gives it (§4.1). Ranking: v1.14's final gate after its retest (Stage 2) if it exists; otherwise its Stage 1 interim verdict, read as SEPARABLE → PASS, retest pending; MARGINAL → MARGINAL; FAIL → FAIL; UNDETERMINED → UNDETERMINED. Sentiment: FAIL if any of v1.11's primary hypotheses H1--H5 is FALSIFIED, else UNDETERMINED if any is UNDETERMINED, else PASS (AI-judged, human-label check pending) if all are CONFIRMED (a pending H5 does not block), else MARGINAL; without a locked and scored Sentiment score on the $t_4$ answers the part is not on the Preview's panel and is reported beside the profile from the legacy panel. Coverage and Grounding: their Paper A gate as last issued.

Table: What the Preview does with each gate state (§4.2).

| Gate state | In the profile | Label | Structure tests |
|:---------------------|:------------------|:------------------------------------|:--------------------------------------|
| PASS | shown | provisional | included |
| PASS, retest pending | shown | provisional; retest pending | included |
| PASS, AI-judged | shown | provisional; AI-judged, human-label check pending | included |
| MARGINAL | separate band below the profile | under review: the marginal leg named | computed and printed as descriptive; not counted in any verdict |
| FAIL | not shown | none (a sentence: negative result) | excluded |
| UNDETERMINED | not shown | not determined, with the cause | excluded |
| NOT RUN | not shown | pending | completed in a dated addendum when the score exists |

The included set $K$ is Presence and Consistency plus every part in a PASS row; $k = \lvert K\rvert \le 6$. If v0.42's drop rule removes any N3 model in the search-off condition, no structure test is run (§4.3). A gate that changes before the paper lock (v1.14's final gate, a v1.13 re-issue, Sentiment Paper B, a first score of a part not run) produces a dated addendum by the same rules (§4.4). Where a rule needs an order it is the programme order: Presence, Consistency, Ranking, Sentiment, Coverage, Grounding (§4.5).

## 2.4 Structure tests

**Pairwise separability (S-tests, §6.2).** Every pair of $K$ is tested with the within-category rank correlation $\rho_w$ on the units rated on both. Where a part's Paper A has already tested exactly the same statistic on the same units, its verdict is carried and the Preview's recomputation must equal it within $10^{-9}$; every other pair is the Preview's own primary test. The Presence--Consistency pair is named H\_PC\_N3. Verdicts use the programme's bands: $\lvert\rho_w\rvert \le 0.30$ CONFIRMED, $\ge 0.50$ FALSIFIED, MARGINAL between, UNDETERMINED below the floor.

**Incremental separability (I-tests, §6.3).** For each part $X$ of $K$ after Presence, on the units rated on $X$ and on every earlier member of $K$, the centred within-category ranks of $X$ are regressed on those of the earlier members; $R^2_{\text{adj}} = 1 - (1 - R^2)(n - c)/(n - c - j)$ with $c$ categories and $j$ predecessors, and $R_{\text{adj}} = \sqrt{\max(0, R^2_{\text{adj}})}$ is read with the same bands. A one-sided permutation $p$ is reported. The pairwise tests catch a single overlap; the incremental test catches a combination of earlier parts.

**Component status (§6.4).** A part is NOT DISTINCT if an S-test with an earlier member of $K$ or its I-test is FALSIFIED (a falsified pair marks only its later member); DISTINCT if all of them are CONFIRMED; UNDETERMINED if neither and at least one is UNDETERMINED; PARTLY DISTINCT otherwise. Presence is the anchor.

**H\_Structure (§6.5, the headline test).** With $d$ the number of members of $K$ that are DISTINCT or PARTLY DISTINCT (Presence counted DISTINCT) and $u$ the number UNDETERMINED: UNDETERMINED if the panel is incomplete, $k < 3$ or $k - u < 3$; CONFIRMED if every member after Presence is DISTINCT; FALSIFIED if $d \le 2$ and $u = 0$; PARTIAL otherwise. The headline wording of each outcome was fixed before any $t_4$ score existed (§6.6): class A (CONFIRMED, $k = 6$), A$_k$ (CONFIRMED, $k < 6$), B (PARTIAL), C (FALSIFIED: drafting pauses and the author decides the direction) and U (UNDETERMINED).

## 2.5 Conventions

$\rho_w$ is the pooled within-category Spearman correlation with ranks centred on each category's mean rank, computed with v1.10's locked function. A category enters a statistic only with at least five units; a statistic is UNDETERMINED with fewer than 30 units pooled or fewer than three categories. Permutation $p$ values use 10,000 within-category draws (two-sided for S-tests, one-sided for I-tests); 90% bootstrap intervals (units resampled within category, 2,000 draws) are reported and never enter a verdict. There is no multiplicity correction: verdicts rest on fixed effect-size bands (§13).

## 2.6 No composite; the descriptive composite check and the bridge

Following AIAS 2.0, the parts are reported side by side and no 0--100 composite is computed (§7). As a descriptive check only, the mean of each brand's rated parts in $K$ is tested against v1.9's constraints: separation (H\_Structure and H\_PC\_N3 not FALSIFIED), added information ($\lvert\rho_w(A_K, P)\rvert \le 0.95$) and no windfall for barely named brands (5-point margin). Nothing is adopted. The AIAS 2.0 legacy profile ($t_3$, six-model panel) is printed beside the N3 profile, never pooled with it; only rank statistics bridge the two, because $C^*$ on three models is scaled differently (§7.3).

## 2.7 Descriptives and sensitivity analyses

Descriptives (§10): score distributions per part (D1), the full matrix of $\rho_w$ on pairwise-complete sets and on the complete-profile set (D2), the eigenvalues and effective number of dimensions of that matrix with a parallel analysis (D3), the per-unit profile table (D4), the bridge (D5), retests where $t_5$ allows (D6), the search-on profile (D7), the composite check (D8) and the coverage tables (D9). Sensitivities, which never change a verdict: SA without the conflict-of-interest-flagged unit (Declarations), SB uncentred ranks, SC leave one category out, SD every S-test on the complete-profile set, SE without Sentiment, SF Ranking by v1.10's mean normalised position, SG Sentiment from the legacy panel, SH the search-on variants.

## 2.8 Pre-registration, order of operations and deviations

The analysis plan, its scorer and tests were locked at tag `{{PREREG_TAG}}` ({{PREREG_DATE}}) and deposited on OSF before any $t_4$-based component score existed; the scorer checks at run time that every $t_4$-based input was committed after that tag (MQ\_Blind) and labels the Preview's own tests on a late input exploratory. The scorer runs once, after the data lock, and refuses without the lock record. {{DEV_SENTENCE}}

# 3. Results

{% if SYNTHETIC %}
**Synthetic test build.** Every number, state and verdict in this section comes from synthetic outputs of the locked scorer (its own test fixture, or a scenario derived from it with its own functions). They are not results.

{% endif %}
## 3.1 Inputs and checks

{{MQ_SENTENCE}} {{BLIND_SENTENCE}}
{% switch CASE_PANEL %}
{% case COMPLETE %}
All three N3 models passed v0.42's drop rule in the search-off condition (MQ\_Panel).
{% case REDUCED %}
An N3 model failed v0.42's drop rule in the search-off condition (MQ\_Panel: {{DROPPED}}). Under §4.3 no structure test is run (§3.3), and the gate states, labels and descriptives below are reported without a structure claim.
{% endswitch %}

## 3.2 The state of each part

{{VALIDATION_LINE}} The table below gives each part's gate as its own study issued it and the state the Preview reads from it.

Table: Gate states read at the data lock (§4.1--4.2). {{K_CAPTION}}

{{TABLE_GATES}}

{% switch CASE_R %}
{% case PASS %}
Ranking passed its final gate after its retest and is in the profile as provisional.
{% case PASS_RETEST_PENDING %}
Ranking passed its Stage 1 gate (SEPARABLE) and is in the profile as provisional, retest pending: its final gate needs the $t_5$ retest (v1.14 Stage 2), which enters by dated addendum.
{% case MARGINAL %}
Ranking{{R_RETEST}} is MARGINAL: v1.14's {{R_GATE_SOURCE}} was MARGINAL ({{R_LEGS}}). Under §4.2 Ranking is shown in a separate band below the profile, labelled under review, and is not in $K$: its correlations with the members of $K$ are printed as descriptive rows (§3.6) and count in no verdict, and it is excluded from the composite check.{% if R_PENDING %} A final gate after v1.14's retest enters by dated addendum.{% endif %}
{% case FAIL %}
Ranking did not pass its gate (v1.14: {{R_GATE_SOURCE_WORD}}); it is not shown in the profile and enters no test.
{% case UNDETERMINED %}
Ranking's gate was UNDETERMINED (v1.14: {{R_GATE_SOURCE_WORD}}); it is not shown in the profile and enters no test.
{% case NOT_RUN %}
No Ranking output existed at the data lock; Ranking is pending and enters by dated addendum when it does.
{% endswitch %}
{% switch CASE_S %}
{% case PASS %}
Sentiment passed its gate and its human-label check and is in the profile as provisional.
{% case PASS_AI_JUDGED %}
Sentiment on the $t_4$ answers was locked and scored, and v1.11's primary hypotheses read as PASS: it is in the profile as provisional, AI-judged, human-label check pending.
{% case MARGINAL %}
Sentiment's gate read as MARGINAL from v1.11's primary hypotheses; it is shown in the band below the profile, under review, and enters no verdict.
{% case FAIL %}
Sentiment's gate read as FAIL (a primary hypothesis of v1.11 was FALSIFIED); it is not shown in the profile.
{% case UNDETERMINED %}
Sentiment's gate read as UNDETERMINED from v1.11's primary hypotheses; it is not shown in the profile.
{% case NOT_RUN %}
No Sentiment score on the $t_4$ answers was locked and scored by the data lock, so Sentiment is not on the Preview's panel: it is reported beside the profile as a separate reading on the legacy panel (v1.11's score at $t_3$; sensitivity SG) and enters no structure test.
{% endswitch %}
{% switch CASE_COV %}
{% case PASS %}
Coverage passed its Paper A gate and is in the profile as provisional{% if COV_REDUCED %} (reduced panel){% endif %}.
{% case MARGINAL %}
Coverage's Paper A gate was MARGINAL ({{COV_LEGS}}); it is shown in the band below the profile, under review, and enters no verdict.
{% case FAIL %}
Coverage did not pass its Paper A gate; it is not shown in the profile.
{% case UNDETERMINED %}
Coverage's Paper A gate was UNDETERMINED; it is not shown in the profile.
{% case NOT_RUN %}
No Coverage output existed at the data lock; Coverage is pending.
{% endswitch %}
{% switch CASE_G %}
{% case PASS %}
Grounding passed its Paper A gate and is in the profile as provisional{% if G_REDUCED %} (reduced panel){% endif %}.
{% case MARGINAL %}
Grounding's Paper A gate was MARGINAL ({{G_LEGS}}); it is shown in the band below the profile, under review, and enters no verdict.
{% case FAIL %}
Grounding did not pass its Paper A gate; it is not shown in the profile.
{% case UNDETERMINED %}
Grounding's Paper A gate was UNDETERMINED; it is not shown in the profile.
{% case NOT_RUN %}
No Grounding output existed at the data lock; Grounding is pending.
{% endswitch %}
Presence {{BRIDGE_P}} (v0.42's bridge test on $\hat\pi$); Consistency {{BRIDGE_C}} (on $\varphi$).

{% if STRUCT %}
## 3.3 Presence and Consistency on the newest models (H\_PC\_N3)

Over {{HPC_N}} units rated on both, $\rho_w(P, C^*)$ was {{HPC_RHO}} (90% interval {{HPC_LO}} to {{HPC_HI}}): H\_PC\_N3 is {{HPC_V}}. {{W1_SENTENCE}}

## 3.4 Pairwise and incremental separability

The two tables below give every S-test and every I-test of $K$, and Figure 1 the pairwise correlations against the bands.{% if ANY_EXPLORATORY %} Tests marked exploratory used an input committed after the pre-registration tag (MQ\_Blind) and do not count as confirmatory.{% endif %}

Table: Pairwise separability (S-tests) among the members of $K$: $\rho_w$, 90% bootstrap interval, units, categories, two-sided permutation $p$, verdict and its source (a Paper A's carried verdict or the Preview's own test).

{{TABLE_S}}

Table: Incremental separability (I-tests): each part against all earlier members of $K$ together.

{{TABLE_I}}

![Within-category rank correlation of every pair of included parts, with the separability bands; parts under review in the lower band. {{FIG_CAPTION}}]({{FIG_DIR}}/chart_01_pairwise.pdf){#fig:pairs width=100%}

## 3.5 Component status and H\_Structure

{{STATUS_SENTENCE}}
{% switch CASE_HS %}
{% case CONFIRMED %}
Every member of $K$ after Presence is DISTINCT: H\_Structure is CONFIRMED ($k$ = {{HS_K}}, $d$ = {{HS_D}}).
{% case PARTIAL %}
Not every member after Presence is DISTINCT, and the parts do not reduce to two readings: H\_Structure is PARTIAL ($k$ = {{HS_K}}, $d$ = {{HS_D}}, undetermined {{HS_U}}).
{% case FALSIFIED %}
At most two members of $K$ are distinct or partly distinct and none is undetermined: H\_Structure is FALSIFIED ($k$ = {{HS_K}}, $d$ = {{HS_D}}).
{% case UNDETERMINED %}
H\_Structure is UNDETERMINED ($k$ = {{HS_K}}, undetermined {{HS_U}}): {{U_CAUSE}}.
{% endswitch %}

Table: Component status (§6.4).

{{TABLE_STATUS}}

**Headline (wording fixed in §6.6, class {{CLASS}}).** {{HEADLINE}}
{% if ANY_MARGINAL_PART %}

## 3.6 Parts under review

Parts in the MARGINAL row are outside $K$ and outside every verdict. Their correlations with the members of $K$ are printed here as descriptive (§4.2, §6.5).

Table: Descriptive correlations of the parts under review with the members of $K$ (no verdict counts).

{{TABLE_MARGINAL}}
{% endif %}

## 3.7 The composite check (descriptive)

{{COMPOSITE_SENTENCE}}

## 3.8 Dimensions, bridge and coverage of the profile (descriptive)

{{D3_SENTENCE}} {{BRIDGE_SENTENCE}} {{UK_SENTENCE}}

![Number of included parts rated per unit, by category. {{FIG_CAPTION}}]({{FIG_DIR}}/chart_02_profile_coverage.pdf){#fig:cov width=88%}

## 3.9 Sensitivity analyses

{{SENS_SENTENCE}}

Table: H\_Structure and H\_PC\_N3 under the sensitivity analyses (they never change a verdict).

{{TABLE_SENS}}
{% else %}
## 3.3 Structure

No structure test was run (§4.3): {{U_CAUSE}}. H\_Structure is UNDETERMINED and H\_PC\_N3 is not tested. **Headline (wording fixed in §6.6, class U).** {{HEADLINE}}

{{BRIDGE_SENTENCE}}
{% endif %}

# 4. Discussion

{% switch CLASS %}
{% case A %}
On the newest models, the six provisional parts behaved as six separate readings of a brand: no part could be predicted from the others, singly or together, within category. This is the structure the framework assumes, measured once, on one panel and one week. It does not validate any part: four of the six remain provisional until their Paper B and release calibration, and separability says nothing about what a part predicts.
{% case A_k %}
The parts measured so far behaved as separate readings of a brand on the newest models. The claim is limited to $K$: the parts outside it are pending, under review or did not pass their own gate, and the structure question for them stays open until a dated addendum or the validated releases. Separability is not validity, and every part other than Presence and Consistency remains provisional.
{% case B %}
The parts did not all behave as separate readings. Every included part stays in the profile with its status, and the overlaps named in the headline become the first question of the next release calibration. A partial result was anticipated (§6.7): with several tests that must all fall in the confirmed band, a small true overlap is enough to move a part to PARTLY DISTINCT, which is why the overlaps are printed with their values.
{% case C %}
The parts reduced to at most two separable readings on the newest models. Under the pre-registration this is a change of direction: drafting pauses, an options memo (for example a qualified Preview, a hold for $t_5$, or the overlapping parts back to redesign) goes to the author, and the author decides. This draft exists only to support that memo.
{% case U %}
How the parts relate could not be determined on these data, so the Preview makes no structure claim. The profile is shown with its labels, and the structure test is completed by dated addendum if the cause is removed before the paper lock.
{% endswitch %}
{% if RANK_SHOWN %}
{{RANK_DISCUSSION}}
{% endif %}

The Preview has two features that bound its reading. It is one wave on three models, and the profile mixes two collections and two search conditions within one week. And every rating floor requires a brand to be named, so the brands that carry a full profile lean to well-named brands; the correlations with Presence are computed on a restricted range (sensitivity SD shows the effect).

# 5. Limitations

One wave carries the structure tests; $t_5$ adds only Ranking's retest and descriptive retests. Three models, one per provider, at provider-default settings: model generation and serving settings are confounded. Five categories, 112 units, US English, registries fixed in May 2026. Every rating floor requires a brand to be named, so the complete-profile set leans to well-named brands and correlations with Presence are computed on a restricted Presence range. Coverage comes from its own collection a few days after the $t_4$ answers on the same models, and Grounding from search-on answers, the others from search-off answers. Sentiment is AI-judged, and its human-label check uses archived legacy-panel windows, so it validates the instrument, not the $t_4$ scores. Ranking's statistic was chosen after its archived values were seen; $t_4$ and $t_5$ are its first confirmatory data. The incremental test's bands are new and could be calibrated only on synthetic data. Fifteen pairs and five incremental tests are read with fixed bands and no multiplicity correction, so CONFIRMED is demanding. Separability is not validity: no part is tested against behaviour here. The Preview inherits every source's limitations and cannot repair a component.

# 6. Future Research

The validated releases, AIAS 3.0 to 6.0 (2027), each calibrate their component under their own pre-registration with a blind confirmation wave, as v1.9 had $t_3$; they may cite the Preview's structure results but are not bound by them. Ranking's final gate needs the $t_5$ retest; Sentiment's validation needs the human labels of its Paper B; a composite, if any, is a decision for those releases.

# Declarations {-}

## Conflict of interest {-}

The author is Director, Corporate Brand Creative and Governance at Samsung Electronics America. This synthesis performs no brand selection and no collection: it reads scores that locked component studies compute on the five omnibus registries fixed in earlier phases, and each registry carries its source-phase conflict-of-interest handling forward unchanged. Two items of record apply to the registries used. *Audiophile headphones (v0.19).* The v0.19 record states: "The panel substitution of AKG → Denon documented in §5 was made out of an abundance of caution given that Samsung's subsidiary Harman International owns AKG; the substitution occurred prior to pre-registration lock." (v0.19 paper, Declaration of interest; v0.19 pre-registration §2.3; v0.19 DEVIATIONS Entry 1.) Correction (November 10, 2026): Harman International, a Samsung subsidiary since March 2017, completed its acquisition of Masimo's Sound United brands, Denon included, on September 23, 2025, so Denon, substituted for AKG before the v0.19 lock, was already a Samsung-group brand; the v0.19 headphones registry therefore includes one Samsung-group brand. The substitution did not achieve its purpose, and this was not noticed until November 10, 2026. In this synthesis Denon remains in the registry and in the primary analysis, as in every component study; every structure statistic is also reported without the Denon unit (sensitivity SA). *Automotive (v0.22).* Samsung subsidiaries hold tier-2/3 component supply relationships with several registry brands --- Harman International (audio systems), Samsung SDI (battery cells) and Samsung Display (infotainment) --- characterized in the source phase as non-competitive, with no brand-level competitive overlap, and imposing no operational restriction on registry composition (v0.22 Declarations; screened in v0.22 DEVIATIONS Entry 0, Part B). These are supply relationships, not ownership; no v0.22 brand is removed. All statistics are computed automatically from locked inputs under the pre-registration. Samsung Electronics had no role in the design, conduct, analysis or reporting of this work.

## Funding {-}

Self-funded. No external funding supported this research.

## Ethics {-}

Not applicable; no human subjects. The Preview analyses scores computed from responses of large language models queried under their public interfaces. The human labelling that validates Sentiment is governed by Sentiment Paper B's own pre-registration.

## Use of AI tools {-}

During the preparation of this work the author used AI tools (Anthropic's Claude) to assist with study design, analysis and writing. The author reviewed and edited all content and takes full responsibility for it.

## Data and code availability {-}

Materials are deposited at OSF (osf.io/ec6wh), `aias_6_0_preview/`: the locked pre-registration, the scorer and its tests, the synthetic precision note, the lock manifest, the deviations record and the anchor record. At publication the deposit adds the scorer's outputs (`results_aias_6_0_preview.json`, `gates_aias_6_0_preview.json`, the per-unit profile `profile_aias_6_0_preview.csv` and the input log `inputs_read_aias_6_0_preview.json`) and the figure sources. The code is also in the programme's GitHub repository (github.com/thirdsystem-aias/aias) at tag `{{PREREG_TAG}}`.

# References {-}

González Castro, P. U. (2026a). *AI Availability: Extending Mental and Physical Availability into Algorithmic Retrieval*. SSRN 6659000.

González Castro, P. U. (2026b). *The AIAS™ Presence Measurement Protocol: Methodological Notes on Construct Validity and the Four-Regime Taxonomy* (v1.2). SSRN 6761698.

González Castro, P. U. (2026c). *The AIAS Presence Measurement Protocol: Phase A Pivot-Validation Specification (v1.3)*. SSRN 6797679.

González Castro, P. U. (2026d). *The AIAS Presence Measurement Protocol v1.4: Recognition × Recall Decomposition and Multi-Component AI Availability*. SSRN 6799479.

González Castro, P. U. (2026e). *The AIAS™ Presence Measurement Protocol: Multi-Statistic C2 Specification and Two-Channel Recall Decomposition* (v1.5). SSRN 6810758.

González Castro, P. U. (2026f). *Substrate Pre-Screening, Independent Moderator Pathway, and Phantom Brand Persistence Phase B Extension* (AIAS Methodology v1.6). SSRN 6816340.

González Castro, P. U. (2026g). *Consistency without Independence: A Pre-Registered Test of Coefficient-of-Variation as the Consistency Component of AIAS™* (v1.7). SSRN 6878818.

González Castro, P. U. (2026h). *A Mean-Independent Consistency Instrument for Cross-Model AI Presence: Redesigning CPC on a Quasi-Binomial Dispersion Basis* (AIAS Methodology v1.8). SSRN 6963359.

González Castro, P. U. (2026i). *One Score or Two? Calibrating a Presence and Consistency Composite for AI Brand Availability: A Pre-Registered Calibration with Blind Five-Month Confirmation (AIAS™ Methodology v1.9)*. Third System, <https://thirdsystem.ai/studies/v1-9/> (PDF: <https://thirdsystem.ai/files/papers/v1_9_ssrn_paper.pdf>); OSF, <https://osf.io/ec6wh/files/osfstorage/6af1fd459966c813ee53ba87>.

González Castro, P. U. (2026j). *AI Availability as a Third Measurable Layer of Brand Availability: Five-Substrate Empirical Anchoring of the AIAS™ Presence Measurement Protocol --- Synthesis under Locked v1.6 Methodology* (AIAS 1.0). SSRN 6817841.

González Castro, P. U. (2026k). *Presence and Consistency: A Two-Component Measurement of AI Availability. The AIAS™ 2.0 Synthesis*. OSF `ec6wh/aias_2_0`.

González Castro, P. U. (2026l). *Tri-System Brand Growth: Mental, Physical, and AI Availability in Brand Architecture*. MSI Working Paper, Report No. 26-132. Marketing Science Institute.

Sharp, B. (2010). *How Brands Grow: What Marketers Don't Know*. Oxford University Press.

Sharp, B., & Romaniuk, J. (2021). *How Brands Grow Part 2: Including Emerging Markets, Services, Durables, New and Luxury Brands* (revised ed.). Oxford University Press.

Programme records cited by version, as the locked pre-registration names them (OSF `ec6wh`; github.com/thirdsystem-aias/aias): the pre-registrations of Methodology v1.10 (Ranking, tag `v1.10-prereg-r2`), v1.11 (Sentiment, tag `v1.11-prereg-r1`), v1.12 (Coverage, tag `v1.12-prereg-r1`), v1.13 (Grounding, tag `v1.13-prereg-r1`) and v1.14 (Ranking redesign, tag `v1.14-prereg-r1`); the $t_4$ wave, v0.42 (tag `v0.42-prereg-r1`); the omnibus registries of v0.19 (audiophile headphones, SSRN 6809182), v0.20 (skincare, SSRN 6811441), v0.21 (cosmetics, SSRN 6815378), v0.22 (automotive, SSRN 6829118) and v0.23 (premium spirits, SSRN 6834298). HARMAN, "HARMAN Completes Sound United Acquisition to Expand Premium Audio Leadership", press release, Business Wire, September 23, 2025, <https://www.businesswire.com/news/home/20250923135384/en/HARMAN-Completes-Sound-United-Acquisition-to-Expand-Premium-Audio-Leadership>.

\clearpage

# Appendix: pre-registered descriptives {-}

Table: Score distributions per part over the 112 units (D1): rated units, median, interquartile range, range.

{{TABLE_D1}}

Table: Units by the number of included parts on which they are rated (0 to $k$), by category (D9).

{{TABLE_D9}}
