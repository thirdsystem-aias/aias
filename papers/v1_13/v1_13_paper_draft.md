---
title: "Grounding: What Search-On AI Answers about Brands Retrieve"
subtitle: "Instrument, Cross-Category Baseline and Separability Gate for a Grounding Component of AI Availability (AIAS™ Methodology v1.13)"
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
  \usepackage{longtable}
  \renewcommand{\textfraction}{0.07}
  \renewcommand{\floatpagefraction}{0.8}
  \makeatletter\setlength{\@fptop}{0pt}\setlength{\@fpsep}{14pt}\makeatother
---

\begin{titlepage}
\setstretch{1.0}
\setlength{\parskip}{0pt}
\begin{center}

{\LARGE \textbf{Grounding: What Search-On AI Answers about Brands Retrieve}}\\[8pt]

{\large Instrument, Cross-Category Baseline and Separability Gate\\ for a Grounding Component of AI Availability (AIAS™ Methodology v1.13)}\\[28pt]

Pablo Ulpiano González Castro\\[4pt]
School of Visual Arts, MPS Branding Program, New York, NY \textit{(primary academic affiliation)}\\
Third System™ (research entity; data archive and methodology venue)\\[8pt]
Correspondence: pablou@pablou.com · pablou.com\\
ORCID: \href{https://orcid.org/0009-0003-8968-9990}{0009-0003-8968-9990}\\[20pt]

Pre-registration, Part I: \texttt{v1.13-prereg-r1} (commit \texttt{\ignorespaces b83efb25a3\unskip}; deposited on OSF before any search record was read)\\
Pre-registration, Part II: \texttt{v1.13-audit-r1} (commit \texttt{5e12e0da93})\\
Data and code: OSF \texttt{ec6wh}, \texttt{methodology/v1\_13}\\

\end{center}
\end{titlepage}

# Abstract {-}

Presence records whether AI answers name a brand; it does not record what an answer rests on when the model searches the web. This pre-registered study specifies a Grounding instrument for the AIAS measurement programme and tests whether it is separable from Presence and Consistency. A fixed rule, frozen before any search-on answer existed, classifies every source returned by the search records of the programme's fourth omnibus wave ($t_4$: Claude Fable 5.2, GPT-6 Astra and Gemini 4 Argon, search on, six category questions per category in three runs, five categories, 112 brand units). The Grounding score G\* is the share of a brand's grounded answers whose retrieved sources include the brand's own domain. 270 answered search-on category answers entered the score, and 42 of 112 brand units met the rating floor.
No gate leg was falsified, but not every leg was confirmed (Presence (H1) MARGINAL and run reliability (H3) UNDETERMINED); the pre-registered gate returned MARGINAL, and a second paper follows only on the pre-registrant's recorded decision.
The structured-data audit (Part II) was collected, but too few brands had both scores for its test (H7 UNDETERMINED).

**Keywords:** AI availability; brand availability; AIAS; pre-registration; Ehrenberg-Bass; large language models; web search; retrieval grounding; structured data; separability; measurement validity

**JEL codes:** M31; L86, L15, D83, M37

**Paper status:** Pre-registered methodology paper, re-analysis of stored $t_4$ answers (Part I) and new public web data (Part II); no model was called and nothing was spent. Gate verdict MARGINAL; deviations recorded in the deviations log under `osf/methodology/v1_13/` (17 entries after the lock). Part of the AIAS measurement programme.

# 1. Introduction

AI Availability, the discoverability and representation of a brand in the outputs of large language models (LLMs), has been proposed as a third layer of brand availability (González Castro, 2026a) beside the Mental and Physical Availability of the Ehrenberg-Bass tradition (Sharp, 2010; Sharp & Romaniuk, 2021), within the Tri-System framework (González Castro, 2026l). The AIAS programme builds the components of an AI availability score one at a time, each pre-registered and locked before it is used, on the Presence measurement protocol (González Castro, 2026b, 2026c, 2026d, 2026e). Presence is whether and how often models name a brand (Methodology v1.6: González Castro, 2026f), anchored across five categories in AIAS 1.0 (González Castro, 2026j). Consistency is how evenly the models of a panel name it: the first Consistency instrument failed its separability test because it moved with Presence (v1.7: González Castro, 2026g); its replacement measures the dispersion statistic $\varphi$ (v1.8: González Castro, 2026h), scaled to $C^*$ (v1.9: González Castro, 2026i). The AIAS 2.0 synthesis (González Castro, 2026k) showed Consistency separable from Presence: within category, $|\rho(C^*, P)|$ was 0.073, 0.082 and 0.189 at the three waves $t_1$--$t_3$, as published under the uncentred pooled-rank convention that this study replaces (pre-registration §0).

When search is on, an AI answer about a category rests on what the model's search brings back. This study names that **retrieved grounding**: which sources the search record of an answer holds, and in particular whether they include the brand's own website. A second aspect, **structured grounding**, is whether the brand's own structured data (schema.org markup on its site, a Wikidata item) is in place for those systems to find. Whether a brand is named is Presence; how evenly models name it is Consistency; where it sits in a list is Ranking. Grounding must add information none of them carries, or it is not a component (§0).

The programme's plan of record sets each new component's first paper to three parts: an instrument specification, a cross-category baseline, and a separability gate against Presence, Consistency and the other components. This paper reports all three under one pre-registration in two parts. Part I [RE-ANALYSIS: $t_4$] defines the source instrument and the Grounding score G\* on the stored search-on answers of the $t_4$ wave and decides the gate. Part II [NEW WEB DATA: audit] audits the brands' own websites and Wikidata records and tests whether richer structured data goes with a higher own-domain share. The research questions are fixed in §1 of the pre-registration: whether a fixed rule can classify the sources at coverage high enough to score brands in all five categories (RQ1); what category answers rest on, per category and model (RQ2); whether G\* is separable from P and $C^*$ within category (RQ3) and holds across runs (RQ4); and whether brands with richer structured data have higher own-domain shares (RQ5). The gate decides whether a second Grounding paper follows on this instrument; a component that fails its gate is reported and redesigned, not carried forward.

# 2. Method

## 2.1 Answers

The source file is v0.42's raw record of the $t_4$ wave, one line per call (pre-registration §2.1). An answered search-on answer is a record with condition S1, status ok, non-empty text, no error and an accepted served model ID, one per call (the last answered attempt, else the last attempt). Category answers are v0.42's Phase B questions: six per category, asked in search-off (S0) and search-on (S1) conditions, three runs each. Panel N3 comprises the newest flagship model of each provider: Claude Fable 5.2, GPT-6 Astra and Gemini 4 Argon, giving 54 search-on category answers per category and 270 in all by design. $t_4$ asked its brand-recognition questions in S0 only, so there are no search-on brand answers. Whether an answer names a brand is decided by v0.42's certified coder on the visible text with URLs removed, used unchanged and pinned by its git blob; a brand reached only through a URL is not named.

The evidence field is the search record's `sources` list for every provider: all results of every search for Anthropic, the search action's sources and opened pages for OpenAI, and the grounding chunks for Google, whose URLs are redirects whose domain is read from the title. The subset an answer cites (`citations`) is sensitivity S2. One rule applies to all providers (§2.1).

## 2.2 Comparators

Presence and Consistency at $t_4$ are read from v0.42's certified scorer, not re-weighted (§2.2). $P_c = 100\,(C_P/3 + 2\hat\pi_c)/3$ for condition $c \in \{\text{S0}, \text{S1}\}$, where $\hat\pi_c$ is v0.42's recall Presence on N3 over its three Phase B runs and $C_P/3$ the share of N3 models whose one search-off recognition answer recognizes the brand (the same share enters $P_{S0}$ and $P_{S1}$). $C^*_c = 100\,(1 - \varphi_c/9)$ when v0.42's partition for the brand is defined, 100 when it is saturated, and not rated otherwise or with fewer than six Phase B mentions; 9 is $\varphi_{\max} = FM/(M-1)$ for six frames and three models, v1.9's own scaling on a reduced panel. Separability is required against P in both conditions: G\* is computed from search-on answers, whose own Presence $P_{S1}$ is its most direct rival, while $P_{S0}$ is Presence as the programme measures it at $t_4$ (§3, rationale).

## 2.3 Source classification and brand domains

Each source URL is normalised to a host and a registrable domain (rules U1--U6 of the frozen file `source_classes_v1_13.md`) and assigned one class by a fixed precedence: brand-owned (the domain belongs to a registry brand of the same category), Wikipedia/reference, forum/UGC, news, review/editorial, retailer, host-pattern rules, other; an unparseable source is unresolved (§2.3). The domain lists were written before any $t_4$ answer existed and were not extended after any search record was read.

A brand's own domains $D_b$ come from a frozen offline list, one row per brand unit, each domain taken from a dated public record (Wikidata's official website, else the English Wikipedia infobox, else web-search results corroborated by a directory) under the decision rules D1--D6 of §2.3; nothing was looked up at analysis time. The list holds 107 resolved units and 5 with no own domain (the five defunct automotive brands of the v0.22 registry), and no unresolved unit. A unit without an own domain is not rated and is reported apart. Three units take a house or portal domain under rule D4: Dior Beauty (dior.com), Chanel Beauty (chanel.com) and Lagavulin (malts.com); any source on those domains counts as their own; their G\* is reported with that flag (§2.3).

## 2.4 The Grounding score

Over the N3 search-on category answers of a brand's category, all three runs pooled (§2.4): $m_b$ is the number of answers naming brand $b$; $g_b$ the number of those with at least one source that resolves to a class other than unresolved (grounded answers); and $o_b$ the number of those whose resolved source domains include a domain in $D_b$. The own-domain source share is $G_b = o_b/g_b$, and

$$
G^*_b = 100\,G_b, \quad \text{rated iff } g_b \geq 6 \text{ and } b \text{ has a } D_b .
$$

The floor of six is the Consistency floor. For every rated brand the source mix (for each class, the mean over $b$'s grounded answers of the share of the answer's distinct resolved domains in that class) and the mean number of distinct resolved domains per grounded answer are reported; no verdict rests on them.

## 2.5 Structured-data audit (Part II)

Part II fetches at most three public pages of each brand's own site (home page, the first about page and the first product page linked from it), under `robots.txt`, at least ten seconds between requests to one host, and no request between 17 and 22 November 2026, and reads the brand's public Wikidata record (protocol §3--§4). The structured-data richness index is SDRI $= 100 \times$ (sum of eight binary indicators)/8: (1) a schema.org Organization or subtype on the home page; (2) a Brand node; (3) a Product or subtype; (4) at least one `sameAs` on an Organization or Brand node; (5) a `sameAs` to Wikidata or Wikipedia; (6) a Wikidata item (adjudicated QID); (7) that item's official website in $D_b$; (8) an English Wikipedia article linked from the item. $\text{SDRI}_{\text{site}}$ uses (1)--(5) and $\text{SDRI}_{\text{kg}}$ (6)--(8). A brand whose home page could not be fetched has SDRI not rated; the five defunct brands are audited for (6)--(8) only and never enter H7 (protocol §1, §5). Such brands enter H7 only through a sensitivity on $\text{SDRI}_{\text{kg}}$ alone, reported beside H7 and never a verdict, and their share is reported (flagged above 0.20). A second pass re-fetches the home page only, 7 days after the first began, or at the end of the period without requests if that date falls inside it; it is a stability descriptive and enters no verdict. Four checks are reported, none of which gates (protocol §6): AQ1, every brand has a domain row and none is unresolved; AQ2, the share of home pages fetched with status 200 (flagged below 0.80); AQ3, JSON-LD blocks that do not parse; AQ4, the share of brands whose indicators (1)--(5), read from the home page alone, changed between the passes.

## 2.6 Statistics

Every correlation is the pooled within-category Spearman $\rho_w$: average ranks are computed within each category, centred on the category's mean rank, and Pearson's $r$ is taken over the pooled centred ranks; only categories with at least five units in the comparison enter, and the floor is 30 units (§3). Values are compared unrounded. Permutation $p$-values permute the first variable within category (10,000 draws; two-sided for separability, one-sided for H3 and H7). Intervals are 90% percentile intervals from 2,000 bootstrap resamples of units within category; they are reported and enter no verdict. Seeds 113001--113010 were fixed in the pre-registration.

## 2.7 Hypotheses and gate

The table below quotes the pre-registered tests (§3). A two-leg hypothesis (H1, H2) is decided in this order: MQ5 failed, UNDETERMINED; a leg with at least 30 units and $|\rho| \geq 0.50$, FALSIFIED; a leg below 30 units, UNDETERMINED; both $|\rho| \leq 0.30$, CONFIRMED; otherwise MARGINAL.

Table: Pre-registered hypotheses, quoted from the pre-registration (§3); $\rho_w$ as §2.6.

| ID | Role | Statistic | CONFIRMED | FALSIFIED |
|:--------------|:--------------|:-------------------------------------|:-------------------|:---------------|
| H1 Presence | gate | $\rho_w(G^*, P_{S1})$, $\rho_w(G^*, P_{S0})$; rated units | both $\lvert\rho\rvert \leq 0.30$ | either $\lvert\rho\rvert \geq 0.50$ |
| H2 Consistency | gate | $\rho_w(G^*, C^*_{S1})$, $\rho_w(G^*, C^*_{S0})$; both rated | both $\lvert\rho\rvert \leq 0.30$ | either $\lvert\rho\rvert \geq 0.50$ |
| H3 Reliability | gate | rel3 from per-run $G^*_r$ (see below) | rel3 $\geq 0.50$, $p < 0.05$ | rel3 $< 0.30$ |
| H4 Ranking | conditional | $\rho_w(G^*, R^*_{S1})$ (v1.14, Stage 1) | $\lvert\rho\rvert \leq 0.30$ | $\lvert\rho\rvert \geq 0.50$ |
| H5 Sentiment | conditional | $\rho_w(G^*, S)$ (a locked $t_4$ score) | as H4 | as H4 |
| H6 Coverage | conditional | $\rho_w(G^*, \text{Cov}^*)$ (v1.12; N3, S0) | as H4 | as H4 |
| H7 Structured data | secondary | $\rho_w(\text{SDRI}, G^*)$, one-sided | $\rho \geq 0.30$, $p < 0.05$ | $\rho \leq 0.10$ |

H3 computes $G^*_r$ per run with a floor of three grounded answers ($g_{b,r} \geq 3$); for each run pair with at least 30 units rated in both runs it takes $\rho_w$, averages them to rel1 and steps up to three runs: rel3 $= 3\,\text{rel1}/(1 + 2\,\text{rel1})$; the permutation is one-sided. Otherwise a leg is MARGINAL. H1, H2 and H4--H7 are UNDETERMINED below 30 units; H3 is UNDETERMINED with fewer than 30 units in two or more of the three run pairs; H7 is also UNDETERMINED if Part II was not collected before Stage C2 (then handed to the second paper, §8).

**Activation of H4--H6 (§3).** A conditional leg is active only if the pre-registration of its score was tagged and pushed before the v1.13 lock commit; it is computed at Stage C1 if its score exists then, otherwise at Stage C2, and is UNDETERMINED (score not available, handed to the second paper) if the score does not exist by Stage C2. The lock record marks H4 active (v1.14-prereg-r2, the redesigned Ranking measure), H5 inactive (no locked Sentiment score on the $t_4$ answers was tagged before the lock; v1.11's score is defined on the archived waves only) and H6 active (v1.12-prereg-r1). H4 may downgrade the gate only when v1.14's Stage 1 interim verdict is SEPARABLE; otherwise it is computed where possible and reported, and neither gates nor downgrades (§12 (g)).

**Gate rule (§3).** PASS if and only if H1, H2 and H3 are all CONFIRMED, downgraded to MARGINAL if an active secondary separability leg (H4--H6; H4 only as above) is FALSIFIED; a leg computed at Stage C2 re-issues the gate verdict with its own timestamp, downgrade only. FAIL if H1, H2 or H3 is FALSIFIED. UNDETERMINED if H1 or H2 is UNDETERMINED (published as such; the instrument goes back to design). Otherwise MARGINAL: the pre-registrant decides, on the record, whether the second paper proceeds. H7 never changes the gate.

## 2.8 Quality checks and sensitivity analyses

Eight checks were pre-registered (§4). MQ1: the parser completes on every answered search-on record, in both fields. MQ2: per model, the share of category answers with at least one source; below 0.25 the model is flagged "search rarely used", below 0.10 it leaves the primary G\*. MQ3: the share of distinct (answer, domain) pairs classed other or unresolved; above 0.40 flagged, above 0.60 the source-mix descriptives are labelled low coverage. MQ4: the share of Gemini sources whose domain is read from the title and the share left unresolved; above 0.20 unresolved, Gemini leaves the primary G\*. MQ5: the gate is UNDETERMINED if more than 80% of rated brands have G\* = 0 or the within-category spread of G\* is zero in three or more categories. MQ6: $\rho_w(g_b, \hat\pi_{S1})$ and $\rho_w(G^*, g_b)$ are reported, and $|\rho_w(G^*, g_b)| \geq 0.50$ is flagged (the share tracks the count). MQ7: the frozen lists and v0.42's coder and scorer equal their anchored hashes, else the run halts. MQ8: per provider, the share of answers with citations and the share of cited URLs also among the sources (reported only).

Sensitivities (§7) never change a verdict; any verdict that would differ is listed beside it: S1 denominator $m_b$ instead of $g_b$; S2 the cited set; S4 rating floors 3 and 10; S5 Gemini kept or dropped against the MQ4 decision; S6 $D_b$ as verified by Part II; S7 P and $C^*$ from AIAS 2.0 at $t_3$ (cross-panel); S8 leave one category out; S9 URLs written in the answer text added; S10 the uncentred convention; S11 every gate statistic without the Denon unit (Declarations). S3 was removed because $t_4$ collected no second Claude model.

## 2.9 Pre-registration and lock

Part I was locked at git tag `v1.13-prereg-r1` (commit `b83efb25a3`, tagged 2026-11-11 02:48 UTC) and deposited on OSF (`ec6wh`, `methodology/v1_13/`: `prereg/`, `registries/`, `anchor/`) with the SHA-256 of every locked file; its anchor record names the tag's commit and the activation of H4--H6. The text states that Part I would lock no earlier than 11 November 2026 at about 3 pm CT; it was locked earlier because the pre-registrant waived the 24-hour review on 10 November 2026 at 20:26 CT, as the deviations record states in an entry made before the tag (Entry 0a). The locked text is unchanged by it. Part II was locked separately at tag `v1.13-audit-r1` (commit `5e12e0da93`) with its own anchor record; its audit could start only 24 hours after the pre-registrant received the locked text (received 2026-11-12 03:55 UTC) and never between 17 and 22 November 2026 (protocol §4, §8). The scorer (`score_v1_13.py`) and the audit (`audit_v1_13.py`) were written and unit-tested on synthetic data before the lock; Stage C1 refuses to run without the tag, the anchor and matching hashes. Choices the text leaves open are listed in the scorers' notes and in the pre-registration's change log (§12). Deviations are recorded in `osf/methodology/v1_13/anchor/DEVIATIONS.md` and `osf/methodology/v1_13/postlock/DEVIATIONS_continued_v1_13.md` (17 entries after the lock), each with the date it was recorded.

# 3. Results

## 3.1 Data and quality checks

270 answered search-on records were parsed in both fields without error (MQ1), and MQ7 passed (Stage C1 halts otherwise). 270 answered category answers of the primary panel entered G\*. No model left the primary score: every model's search returned sources often enough (MQ2) and Gemini's redirect sources were resolved (MQ4; unresolved share 0.0%). MQ2 flagged Gemini 4 Argon as "search rarely used" (below 0.25); every result is read with that flag. Of the distinct (answer, domain) source pairs, 71.8% were classed other or unresolved (MQ3), above 0.60, so the source-mix descriptives below are labelled **low coverage**. G\* did not track the number of grounded answers ($\rho_w(G^*, g_b) = 0.210$, MQ6), while $\rho_w(g_b, \hat\pi_{S1}) = 0.863$. 40% of rated brands had G\* = 0 (MQ5 limit 80%), and no category had a single G\* value, so MQ5 passed.

Table: Search use and source checks per model (MQ2, MQ4); citations (MQ8) are in Appendix B.

| Model | Category answers | With a source | Share (MQ2) | Domain from title (MQ4) | Unresolved (MQ4) | Primary G\* |
|:--------------------|----------------:|-------------:|-----------:|-----------------------:|----------------:|:------------------|
| Claude Fable 5.2 | 90 | 75 | 83.3% | -- | -- | kept |
| GPT-6 Astra | 90 | 86 | 95.6% | -- | -- | kept |
| Gemini 4 Argon | 90 | 16 | 17.8% | 100.0% | 0.0% | search rarely used |

## 3.2 The instrument and the cross-category baseline

42 of 112 brand units were rated (65 below the floor of six grounded answers; 5 without an own domain, reported apart). Across categories and models (all three N3 models, as the baseline of §6 is defined), the share of category answers whose search returned at least one source ranged from 11% to 100%, grounded answers held a mean of 0.5 to 78.6 distinct resolved domains, and the share of answers retrieving any registry brand's own domain ranged from 0% to 56%. Figure 1 shows how often each model's search returned sources, Figure 2 what the sources were, and Figure 3 the distribution of G\*. The source-mix descriptives are labelled low coverage (MQ3). The three units with a house or portal domain (§2.3) are reported with that flag: Dior Beauty (not rated); Chanel Beauty (not rated); Lagavulin (not rated).

![Share of search-on category answers whose search record holds at least one source, per category and model. ](../../reports/figs/v113/chart_01_search_use.pdf){#fig:search width=92%}

![Mean source-type mix of search-on category answers per category and model: each answer's distinct resolved domains split by class, each answer weighing one. ](../../reports/figs/v113/chart_02_source_mix.pdf){#fig:mix width=100%}

Table: G\* per category, computed on all three N3 models as the baseline of §6 is defined: units, rated units, median and interquartile range of G\*, and the share of rated units at zero.

| Category | Units | Rated | G\* median | G\* IQR | Share at 0 |
|:--------------|-----:|-----:|----------:|----------:|----------:|
| Headphones | 16 | 10 | 12.2 | 0.0--23.9 | 40% |
| Skincare | 24 | 8 | 8.0 | 0.0--16.1 | 38% |
| Cosmetics | 24 | 11 | 0.0 | 0.0--6.5 | 55% |
| Automotive | 24 | 6 | 0.0 | 0.0--6.8 | 67% |
| Spirits | 24 | 7 | 28.6 | 16.2--31.0 | 0% |

![G\* per rated brand by category (box: median and interquartile range). ](../../reports/figs/v113/chart_03_gstar_by_category.pdf){#fig:gstar width=92%}

The 20 most-retrieved domains across all category answers (number of answers whose sources include the domain) were: wikipedia.org (119); reddit.com (82); whowhatwear.com (51); yahoo.com (49); youtube.com (46); marieclaire.com (45); amazonaws.com (35); apnews.com (35); womanandhome.com (35); tomsguide.com (29); globalbrandsmagazine.com (28); gobrandwave.com (27); time.com (27); whathifi.com (27); forbes.com (25); marieclaire.co.uk (23); yougov.com (23); axios.com (22); creativebloq.com (22); statista.com (20).

## 3.3 Separability and reliability (the gate legs)

**Presence (H1).** Across 42 rated brands, $\rho_w(G^*, P_{S1}) = 0.307$ (90% interval 0.008 to 0.543; two-sided $p = 0.0819$), and across 42, $\rho_w(G^*, P_{S0}) = 0.395$ (90% interval 0.095 to 0.629; $p = 0.0250$).
Neither leg reaches 0.50, but not both are at most 0.30, and H1 is **MARGINAL**.
Figure 4 shows both legs under every pre-registered analysis.

![$\rho_w$ of G\* with Presence in each condition, for the primary analysis (with its 90% interval), the sensitivity analyses plotted (S1, S2, S4, S5, S9, S10 and S11) and each left-out category (S8); S6 and S7, computed after Stage C2, are not plotted and are given in the table of §3.7; shaded: $|\rho_w| \leq 0.30$. ](../../reports/figs/v113/chart_04_presence_legs.pdf){#fig:h1 width=100%}

**Consistency (H2).** Across 42 brands rated on both scores, $\rho_w(G^*, C^*_{S1}) = -0.087$ (90% interval -0.370 to 0.214; $p = 0.6285$), and across 40, $\rho_w(G^*, C^*_{S0}) = 0.049$ (90% interval -0.256 to 0.353; $p = 0.7944$).
Both $|\rho_w|$ are at most 0.30, and H2 is **CONFIRMED**.
Figure 5 shows both legs under every pre-registered analysis.

![$\rho_w$ of G\* with Consistency $C^*$ in each condition, for the primary analysis (with its 90% interval), the sensitivity analyses plotted (S1, S2, S4, S5, S9, S10 and S11) and each left-out category (S8); S6 and S7, computed after Stage C2, are not plotted and are given in the table of §3.7; shaded: $|\rho_w| \leq 0.30$. ](../../reports/figs/v113/chart_05_consistency_legs.pdf){#fig:h2 width=100%}

**Run reliability (H3).** With G\* computed per run (floor three grounded answers), only 0 of the three run pairs had at least 30 units rated in both runs.
Two qualifying pairs are needed, and H3 is **UNDETERMINED**.
The pairs are tabulated below and shown in Figure 6.

Table: Agreement of per-run G\* between runs (H3): units rated in both runs, $\rho_w$, and whether the pair qualifies (at least 30 units).

| Run pair | Units rated in both | $\rho_w$ | Qualifies |
|:----------------|-------------------:|-----:|---------:|
| Runs 1 and 2 | 23 | 0.300 | no |
| Runs 1 and 3 | 27 | 0.604 | no |
| Runs 2 and 3 | 24 | 0.415 | no |

![$\rho_w$ of per-run G\* between each pair of runs, with the number of brands rated in both runs; the dotted lines mark the rel3 bars of 0.50 and 0.30 converted to the scale of one pair. ](../../reports/figs/v113/chart_06_run_pairs.pdf){#fig:h3 width=88%}

## 3.4 Conditional legs: Ranking, Sentiment and Coverage

**Ranking (H4).** H4 was computed at Stage C1 from v1.14's Stage 1 output, whose interim verdict was MARGINAL, not SEPARABLE, so under the pre-registered rule H4 neither gates nor downgrades. Across 42 brands rated on both, $\rho_w(G^*, R^*_{S1}) = 0.292$ (90% interval -0.048 to 0.574; $p = 0.0928$), which reads **CONFIRMED** under the separability bands.

**Sentiment (H5).** H5 is INACTIVE: no locked Sentiment score on the $t_4$ answers was tagged before the lock, so it has no verdict and may be tested only under a later pre-registration.

**Coverage (H6).** H6 was computed at Stage C2 from v1.12's locked Cov\* (N3, search off). Across 33 brands rated on both, $\rho_w(G^*, \text{Cov}^*) = -0.304$ (90% interval -0.645 to 0.071; $p = 0.1637$), and H6 is **MARGINAL**.

## 3.5 The gate verdict

No gate leg was FALSIFIED and neither H1 nor H2 was UNDETERMINED, but H1 was MARGINAL and H3 was UNDETERMINED. The gate verdict is **MARGINAL**.
Stage C2 (appended 2026-11-22 18:09 UTC) re-issued the gate after H6 without changing it (MARGINAL). Figure 7 shows every computed leg against its bands.

Table: Every pre-registered leg: the comparator, its role, the number of units, $\rho_w$ (H3: rel3) with its 90% interval, the permutation $p$ and the verdict, in the scorer's words.

| Leg | G\* against | Role | $n$ | $\rho_w$ | 90% interval | $p$ | Verdict |
|:-----------|:-----------------|:---------------------|-------:|---------:|---------------:|------:|:----------------|
| H1 (S1) | Presence $P$, S1 | gate | 42 | 0.307 | [0.008, 0.543] | 0.0819 | **MARGINAL** |
| H1 (S0) | Presence $P$, S0 | gate | 42 | 0.395 | [0.095, 0.629] | 0.0250 | **MARGINAL** |
| H2 (S1) | Consistency $C^*$, S1 | gate | 42 | -0.087 | [-0.370, 0.214] | 0.6285 | **CONFIRMED** |
| H2 (S0) | Consistency $C^*$, S0 | gate | 40 | 0.049 | [-0.256, 0.353] | 0.7944 | **CONFIRMED** |
| H3 | run against run | gate | 0 pairs | -- (rel3) | -- | -- | **UNDETERMINED** |
| H4 | Ranking $R^*_{S1}$ | conditional, reported | 42 | 0.292 | [-0.048, 0.574] | 0.0928 | **CONFIRMED** |
| H5 | Sentiment $S$ | conditional | -- | -- | -- | -- | **INACTIVE** |
| H6 | Coverage Cov\* | conditional, gating | 33 | -0.304 | [-0.645, 0.071] | 0.1637 | **MARGINAL** |
| H7 | SDRI (one-sided) | secondary | 26 | 0.081 | [-0.309, 0.439] | 0.3507 | **UNDETERMINED** |

![All computed legs against their bands: separability legs (H1, H2, H4, H6) with the band $|\rho_w| \leq 0.30$ shaded and $|\rho_w| = 0.50$ dotted; H3's rel3 against 0.50 and 0.30; H7 against 0.30 and 0.10. Indigo: legs that can decide or downgrade the gate; gray: reported only. ](../../reports/figs/v113/chart_07_legs_bands.pdf){#fig:legs width=100%}

## 3.6 Structured data (Part II) and H7

Part II's first pass recorded 107 brands with an own domain; SDRI was rated for 77, and the median SDRI was 37.5. The table gives the indicators per category.

**Audit checks (protocol §6; reported only, DEVIATIONS Entry 2).** AQ1 passed: each of the 112 brand units had a row in the domain list; 0 were unresolved and 5 had no own domain (the defunct brands). AQ2: the home page returned status 200 for 77 of the 107 brands with an own domain (0.720), **below 0.80, so the audit is flagged**; of the other home pages, 23 were blocked by the site and 7 were not requested because the site's `robots.txt` could not be read (server error or timeout). SDRI was therefore not rated for 30 of the 107 (28%), above the 0.20 at which protocol §5 flags this share (flagged); they enter H7 only through the SDRI$_{\text{kg}}$ sensitivity below. AQ3: pass 1 parsed 195 pages holding 233 JSON-LD blocks, of which 0 failed to parse. AQ4: pass 2 re-fetched the home page only, once, starting 2026-11-22 18:11 UTC, 9 days 11 hours after pass 1 began. The date the protocol sets (7 days after pass 1 began) fell inside the period without requests, so pass 2 ran after that period ended (DEVIATIONS Entry 16). Of the 77 brands whose home page was fetched in both passes, 0 (0%) changed in indicators (1)--(5) read from the home page alone. Pass 2 enters no verdict: Stage C2 had already run on pass 1.

Only 26 brands had both an SDRI and a rated G\* in categories with at least five, below the floor of 30, and H7 is **UNDETERMINED** (Figure 8).

Beside H7, the sensitivity named in protocol §5 (DEVIATIONS Entry 1) correlates SDRI$_{\text{kg}}$ (indicators (6)--(8) alone) with G\*, including brands whose home page could not be fetched: across 42 brands in 5 categories, $\rho_w(\text{SDRI}_{\text{kg}}, G^*) = -0.035$ (90% interval -0.304 to 0.261; one-sided $p = 0.5844$). Under H7's bands this reads FALSIFIED; it is a sensitivity, reported beside H7 and never a verdict, and H7 stays **UNDETERMINED**.

Table: Structured-data audit per category: brands audited (defunct brands excluded), home pages fetched, median SDRI and the share of brands with each indicator.

| Category | Audited | Home page | Median SDRI | (1) | (2) | (3) | (4) | (5) | (6) | (7) | (8) |
|:--------------|-------:|---------:|-----------:|----:|----:|----:|----:|----:|----:|----:|----:|
| Headphones | 16 | 12 | 18.8 | 58% | 25% | 25% | 25% | 0% | 25% | 25% | 25% |
| Skincare | 24 | 15 | 50.0 | 80% | 40% | 27% | 67% | 0% | 58% | 50% | 46% |
| Cosmetics | 24 | 21 | 37.5 | 86% | 19% | 24% | 76% | 0% | 50% | 46% | 50% |
| Automotive | 19 | 11 | 37.5 | 18% | 27% | 0% | 18% | 9% | 79% | 74% | 74% |
| Spirits | 24 | 18 | 31.2 | 61% | 11% | 6% | 33% | 6% | 42% | 38% | 42% |

![SDRI and G\* per brand with both, by category. ](../../reports/figs/v113/chart_08_sdri_gstar.pdf){#fig:h7 width=88%}

## 3.7 Sensitivity analyses

The table below gives the gate statistics under each pre-registered sensitivity. A verdict would differ under S1, S4 and S10 (listed in the table); the primary verdicts stand. Without the Denon unit (S11) no verdict changes. Leaving one category out (S8), $\rho_w(G^*, P_{S1})$ ranged from 0.211 to 0.405 while rel3 could not be computed with any category left out (Appendix). Sensitivity S7 (P and $C^*$ from AIAS 2.0 at $t_3$, cross-panel) was computed after Stage C2 by `postlock/c2_extras_v1_13.py` with the scorer's own functions (continued deviations log, Entry 6) and is reported in the table beside the verdicts; it changes no verdict. Sensitivity S6 ($D_b$ as verified by Part II) was computed after Stage C2 by the same script (Entry 5): the $D_b$ of 11 units gained the registrable domains of their home pages' final URLs and of their Wikidata P856 values, and it changes no verdict. Among the added aliases were 25 bare country suffixes (`co.id`, `co.th`, `co.zm` and others, in 5 units), which S6 treated as brand aliases although they are not in the frozen alias list; no verdict changed, and S6 was not re-run without them (a deviation recorded on 2026-11-22, continued deviations log, Entry 17).

Table: Pre-registered sensitivity analyses (§7): $\rho_w$ of G\* with P and $C^*$ in each condition, rel3, and the gate verdict each would give; a leg verdict different from the primary one is marked with its word. Sensitivities never change a verdict.

| Sensitivity | H1 S1 | H1 S0 | H2 S1 | H2 S0 | rel3 | Gate | Verdicts that differ |
|:-----------------------------|-----:|-----:|------:|------:|----:|:------------|:-----------------------|
| S1 denominator $m_b$ | 0.278 | 0.404 | -0.094 | 0.064 | -- | MARGINAL | H4 MARGINAL |
| S2 cited set | 0.196 | 0.315 | -0.039 | -0.075 | -- | MARGINAL | none |
| S4 floor 3 | 0.489 | 0.516 | 0.114 | 0.108 | -- | FAIL | H1 FALSIFIED |
| S4 floor 10 | 0.328 | 0.342 | -0.288 | 0.041 | -- | UNDETERMINED | H1, H2, H4 UNDETERMINED |
| S5 Gemini dropped | 0.318 | 0.395 | -0.113 | 0.033 | -- | MARGINAL | none |
| S6 $D_b$ verified by Part II | 0.307 | 0.395 | -0.087 | 0.049 | -- | MARGINAL | none |
| S7 AIAS 2.0 $t_3$ comparators | 0.341 | 0.341 | 0.035 | 0.035 | -- | MARGINAL | none |
| S9 URLs in the text | 0.286 | 0.380 | -0.083 | 0.073 | -- | MARGINAL | none |
| S10 uncentred ranks | 0.390 | 0.467 | 0.042 | 0.126 | -- | MARGINAL | H4 MARGINAL |
| S11 without Denon | 0.307 | 0.395 | -0.087 | 0.049 | -- | MARGINAL | none |

## 3.8 Exploratory: four definitions of a brand's own share of cited sources (v1.18)

This section is exploratory. It reports Methodology v1.18 (pre-registration tag `v1.18-prereg-r1`), which reads the cited set of the same $t_4$ answers under four competing definitions of how much of what an answer cites "belongs" to the brand. It gates nothing, and none of v1.13's rules, hypotheses or verdicts changes because of it. For each answer and each brand it names, every distinct cited domain is labelled relative to that brand through v1.13's frozen $D_b$ and v1.18's domain table, and the share is computed under each definition:

- **K, own domain:** only the brand's own domains ($D_b$) count.
- **P, any company:** the brand's own domains and any other company's site count.
- **Y, own plus listings:** the brand's own domains and listing sites (directories, marketplaces and retailers) count.
- **M, not owned:** every cited domain the brand does not own counts; with a common denominator M = 100 minus K for every answer and brand.

Over 270 category answers and 754 answer--brand pairs (42 rated brands), the pair-weighted program share was 0.73 (90% interval 0.32 to 1.20) under K, 11.30 (7.34 to 15.57) under P, 14.55 (10.54 to 18.93) under Y and 99.27 (98.80 to 99.68) under M, in per cent of cited domains (intervals from a cluster bootstrap over cells, 2,000 draws). By v1.18's reporting rule (definitions whose 90% intervals do not overlap are called different), the program share differs between K and P, K and Y, K and M, P and M and Y and M; P and Y are not distinguishable at this sample size.

Brand-level readings move between definitions as well as the level. Among K, P and Y, the within-category rank correlation of brands' shares, $\rho_w$, ranged from -0.300 to 0.428, and between 7% and 24% of rated brands moved by more than 25 percentage points. Pairs with M mirror the pairs with K, because M sits at 100 minus K. One rated brand had a value in fewer than half of the bootstrap draws, and its brand-level interval is flagged: Johnnie Walker (994 of 2,000 draws).

Table: v1.18: agreement between definitions over rated brands: $\rho_w$ and the share of brands whose share differs by more than 25 points, each with its 90% interval.

| Pair | $\rho_w$ | 90% interval | Brands moving > 25 points | 90% interval |
|:------------------------------------|------:|----------------:|-------------------------:|------------:|
| K--P | 0.428 | 0.157 to 0.598 | 7% | 2% to 22% |
| K--Y | 0.315 | 0.052 to 0.563 | 24% | 5% to 38% |
| K--M (identity: M = 100 minus K) | -1.000 | -1.000 to -1.000 | 100% | 100% to 100% |
| P--Y | -0.300 | -0.483 to 0.250 | 12% | 7% to 36% |
| P--M | -0.428 | -0.598 to -0.157 | 100% | 93% to 100% |
| Y--M | -0.315 | -0.563 to -0.052 | 100% | 100% to 100% |

Domains the table left UNRESOLVED leave the primary denominator. Their pair-weighted share of the cited domains was 13.5% (per rated brand 0.0% to 23.5%); in the retrieved set (S5) it was 37.2% (per brand 17.1% to 63.9%), because v1.18 did not classify domains that were retrieved but never cited. These shares were added after v1.18's run by a descriptive that changes no locked result (v1.18 DEVIATIONS Entry 1). The domain table's classes were checked by a second coder that was itself an AI model (an independent Claude session), not a person, so the audit shows agreement between two AI coders only; this is a limitation of every number in this section.

Table: v1.18 sensitivities S1--S7: pair-weighted program share under each definition (per cent of cited domains), with the number of answer--brand pairs and of rated brands.

| Analysis | K | P | Y | M | Pairs | Rated |
|:----------------------------------------------------------------|----:|-----:|-----:|-----:|-----:|-----:|
| Primary | 0.73 | 11.30 | 14.55 | 99.27 | 754 | 42 |
| S1 unresolved domains in the denominator, outside every class | 0.72 | 10.48 | 12.15 | 99.28 | 754 | 42 |
| S1 unresolved domains inside P's and Y's classes | 0.72 | 24.02 | 25.68 | 99.28 | 754 | 42 |
| S2 retailers counted as company | 0.73 | 24.10 | 1.75 | 99.27 | 754 | 42 |
| S3 alias domains counted as own | 0.97 | 11.30 | 14.79 | 99.03 | 754 | 42 |
| S4 floor of 3 grounded answers | 0.73 | 11.30 | 14.55 | 99.27 | 754 | 62 |
| S4 floor of 10 grounded answers | 0.73 | 11.30 | 14.55 | 99.27 | 754 | 28 |
| S5 retrieved set (sources) instead of citations | 0.55 | 9.88 | 13.51 | 99.45 | 754 | 42 |
| S6 without Denon | 0.73 | 11.35 | 14.47 | 99.27 | 751 | 42 |
| S6-COI without Denon and the five agency-tie brands | 0.74 | 11.38 | 15.19 | 99.26 | 714 | 41 |
| S7 without Gemini 4 Argon | 0.81 | 11.91 | 12.54 | 99.19 | 669 | 41 |

![Program share under each definition, with its 90% interval. ](../../reports/figs/v113/chart_09_v118_definitions.pdf){#fig:v118 width=88%}

Inputs: v1.18's `v1_18_results.json` (SHA-256 `6fa5502d5d5f`…) and `descriptive_v1_18.json` (`1a7778313fca`…), copied into `papers/v1_13/inputs/v1_18/` with their full SHA-256 recorded.

# 4. Discussion

The gate's result is intermediate: no primary leg was falsified, but not every condition for a pass was met. Under the pre-registered rule a second paper proceeds only on the pre-registrant's recorded decision, with the condition that was not met as its first confirmatory test. Until then G\* is a candidate measure reported beside Presence and Consistency, not combined with them.

The structured-data audit describes, for the same brands, whether their own sites and public knowledge-graph records carry the markup that search systems can read; H7 relates it to G\* and changes no gate verdict.
The baseline of §3.2 describes, on the newest models, what category answers retrieve when search is on; it carries no verdict.

# 5. Limitations

Recognition (the $C_P$ part of P) rests on one search-off brand answer per model. Search-on answers depend on the web on the day and on each provider's search back-end; they are reproducible only as recorded. The retrieved set includes results an answer did not use, and what it holds differs by provider, so model differences mix model and tool; the cited set (S2) is what the answer attributes. Own-domain retrieval needs the brand's site to be indexed and open to crawlers, so a low G\* can reflect robots policies as much as model behaviour. $D_b$ is a declared list and can miss regional or campaign domains. The study covers five categories, one market and one language (US English). The audit reads static HTML only, so structured data injected by JavaScript is missed (§9). The audit fetched fewer than 80% of the brands' home pages (AQ2 flagged, §3.6); the others were blocked or had an unreadable `robots.txt`, so SDRI is missing more often for sites that refuse automated requests, and H7 rests on fewer brands than it would otherwise. The verdict file does not record the hashes of its inputs ($t_4$ raw file, coder tables, brand table); they are recorded in the deposit beside it. The exploratory v1.18 section (§3.8) rests on a domain table audited by two AI coders, not by a person. The source mix is labelled low coverage (MQ3).

# 6. What a second paper inherits

Pre-registered separately, only after PASS or after MARGINAL with the pre-registrant's recorded decision (§8): the locked parser, `source_classes_v1_13.md`, $D_b$, the scorer and its tests; the per-answer source tables; source-coverage stability over waves ($t_4$, v0.40's search-on arm, $t_5$, $t_6$, each re-classified with the frozen lists); phantom-brand grounding; identity load; a typology of G\* with P, $C^*$ and $R^*$; H7 if Part II was not collected in time; any active conditional leg whose score did not exist by Stage C2; and re-audits of structured data at $t_5$ and $t_6$.

# Declarations {-}

## Conflict of interest {-}

The author is Director, Corporate Brand Creative and Governance at Samsung Electronics America. This study performs no new brand selection: it re-uses the five omnibus registries (v0.19--v0.23) and carries forward each registry's source-phase COI handling unchanged. Part II fetches public pages of the registry brands' own websites; it contacts no brand and buys nothing. Two items of record apply, quoted from their source records. *v0.19 audiophile headphones* (`osf/v19/PRE_REGISTRATION_v0_19.md` §2.3): "AKG removed from Cell A short-list; Denon substituted. AKG is Samsung-owned since 2016. The author's COI declaration names Samsung; including AKG would invite the kind of reviewer suspicion AIAS™ 1.0 does not need to absorb. Denon carries comparable heritage stature (founded 1910; AH-D7000 → D9200 audiophile line) and removes the question. Decision rationale recorded here for audit trail." *v0.22 automotive* (v0.22 Declarations §COI): "Samsung subsidiaries hold tier-2/3 component supply relationships with several brands in the v0.22 registry: Harman International (audio systems) supplies Mercedes-Benz, BMW, and other premium automotive OEMs; Samsung SDI (battery cells) supplies BMW (i-series), Volkswagen Group brands including Bentley and Porsche (Stellantis-adjacent platforms), and others; Samsung Display (infotainment) supplies Mercedes-Benz and BMW. Tesla and Polestar also have tangential Samsung-component exposure at the parts level. These are non-competitive supply relationships; Samsung Electronics America does not produce or market passenger car brands and has no brand-level competitive overlap with any v0.22 registry entry. The COI was screened and documented in DEVIATIONS Entry 0 (Part B) of the pre-registration module; no operational restriction on registry composition was imposed." Correction (November 10, 2026): Denon, which replaced AKG in the v0.19 registry, has itself been owned by Harman International, a wholly owned subsidiary of Samsung Electronics, since September 23, 2025, when Harman completed its acquisition of Sound United from Masimo; the v0.19 headphones registry therefore includes one Samsung-group brand. The substitution did not achieve its purpose, and this was not noticed until November 10, 2026. Source: HARMAN press release, Business Wire, September 23, 2025. Handling here: Denon stays in the registry; every gate statistic is also reported without the Denon unit (sensitivity S11), with any verdict change listed next to the verdict; Part II audits Denon's website under the same rules as every other brand's. Samsung Electronics had no role in the design, conduct, analysis or reporting of this work.

## Funding {-}

Self-funded. No external funding supported this research.

## Ethics {-}

No human subjects. Part II reads public web pages under the protocol's robots and rate rules.

## Use of AI tools {-}

During the preparation of this work the author used AI tools (Anthropic's Claude) to assist with study design, analysis and writing. The author reviewed and edited all content and takes full responsibility for it.

## Data and code availability {-}

Materials are deposited at OSF (osf.io/ec6wh), `methodology/v1_13/`: the locked pre-registration with the source-classification rule, the audit protocol and its dry-run record, the brand-domain list and the Wikidata word list, the scorer and audit scripts with their tests and synthetic fixtures, the lock manifest, the deviations record and the anchor records (`prereg/`, `registries/`, `anchor/`; the locked Part I text is at <https://osf.io/ec6wh/files/osfstorage/6af3d7c5ca45e46a8b9d8d42>). At publication the deposit adds the verdict file (`v1_13_verdicts.json`), the audit's structured-data records of both passes, the SDRI table and the audit checks (`audit/`, with `v1_13_audit_checks.json`; raw HTML is not deposited) and the figure sources. The code is also in the programme's GitHub repository (github.com/thirdsystem-aias/aias) at tag `v1.13-prereg-r1`.

# References {-}

\begingroup\small\setstretch{1.15}\setlength{\parskip}{5pt}

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

Programme records cited by version, as the locked pre-registration names them (OSF `ec6wh`; github.com/thirdsystem-aias/aias): the pre-registrations of Methodology v1.10 (Ranking, tag `v1.10-prereg-r2`), v1.11 (Sentiment, tag `v1.11-prereg-r1`), v1.12 (Coverage, tag `v1.12-prereg-r1`) and v1.14 (Ranking redesign, tag `v1.14-prereg-r2`); the $t_4$ wave, v0.42 (pre-registration r2, tag `v0.42-prereg-r1`); the omnibus registries of v0.19 (audiophile headphones, SSRN 6809182), v0.20 (skincare, SSRN 6811441), v0.21 (cosmetics, SSRN 6815378), v0.22 (automotive, SSRN 6829118) and v0.23 (premium spirits, SSRN 6834298). HARMAN press release, Business Wire, September 23, 2025, <https://www.businesswire.com/news/home/20250923135384/en/HARMAN-Completes-Sound-United-Acquisition-to-Expand-Premium-Audio-Leadership>.

\endgroup

\clearpage

# Appendix A: per-brand results {-}

Brand units rated on G\*, by category: answers naming the brand ($m_b$), grounded answers ($g_b$), answers retrieving the brand's own domain ($o_b$), G\*, the mean number of distinct resolved domains per grounded answer ($d_b$) and the source mix (shares of brand-owned, reference, review/editorial, retailer, news, forum/UGC and other domains). A dagger marks a house or portal domain (§2.3).

\begingroup\small\setstretch{1.0}\renewcommand{\arraystretch}{0.95}

| Category | Brand | $m$ | $g$ | $o$ | G\* | $d$ | own | ref | rev | ret | news | UGC | other |
|:--------------|:-----------------------|----:|----:|----:|----:|----:|----:|----:|----:|----:|----:|----:|-----:|
| Headphones | Meze | 11 | 8 | 3 | 37.5 | 16.1 | 5% | 1% | 21% | 20% | 1% | 5% | 46% |
| Headphones | Audeze | 32 | 19 | 5 | 26.3 | 19.9 | 4% | 2% | 21% | 12% | 1% | 4% | 57% |
| Headphones | HiFiMan | 28 | 16 | 4 | 25.0 | 20.0 | 4% | 2% | 21% | 14% | 1% | 5% | 53% |
| Headphones | Sennheiser | 48 | 29 | 6 | 20.7 | 17.2 | 3% | 4% | 18% | 8% | 3% | 3% | 61% |
| Headphones | Focal | 34 | 20 | 4 | 20.0 | 20.1 | 4% | 2% | 21% | 12% | 1% | 4% | 57% |
| Headphones | Sony | 39 | 23 | 1 | 4.3 | 16.0 | 0% | 6% | 17% | 7% | 6% | 2% | 61% |
| Headphones | Beyerdynamic | 25 | 10 | 0 | 0.0 | 14.7 | 2% | 5% | 18% | 3% | 5% | 1% | 66% |
| Headphones | Dan Clark Audio | 13 | 9 | 0 | 0.0 | 18.8 | 2% | 2% | 21% | 16% | 2% | 5% | 53% |
| Headphones | Grado | 13 | 6 | 0 | 0.0 | 13.7 | 0% | 0% | 27% | 5% | 1% | 0% | 67% |
| Headphones | Stax | 10 | 6 | 0 | 0.0 | 22.5 | 2% | 2% | 20% | 9% | 1% | 5% | 61% |
| Skincare | CeraVe | 48 | 33 | 6 | 18.2 | 17.1 | 2% | 6% | 5% | 4% | 6% | 6% | 70% |
| Skincare | The Ordinary | 34 | 22 | 4 | 18.2 | 16.9 | 3% | 6% | 5% | 4% | 6% | 6% | 69% |
| Skincare | SkinCeuticals | 28 | 13 | 2 | 15.4 | 14.8 | 3% | 5% | 2% | 6% | 2% | 10% | 72% |
| Skincare | Cetaphil | 14 | 8 | 1 | 12.5 | 14.8 | 0% | 11% | 5% | 2% | 4% | 5% | 72% |
| Skincare | La Roche-Posay | 42 | 29 | 1 | 3.4 | 16.0 | 3% | 8% | 5% | 4% | 4% | 6% | 71% |
| Skincare | Rhode | 26 | 20 | 0 | 0.0 | 14.3 | 0% | 6% | 3% | 3% | 8% | 6% | 74% |
| Skincare | Drunk Elephant | 15 | 9 | 0 | 0.0 | 11.8 | 0% | 7% | 1% | 4% | 11% | 2% | 76% |
| Skincare | Augustinus Bader | 18 | 12 | 0 | 0.0 | 12.8 | 0% | 9% | 6% | 2% | 7% | 3% | 74% |
| Cosmetics | e.l.f. Cosmetics | 28 | 20 | 3 | 15.0 | 16.1 | 2% | 7% | 5% | 8% | 1% | 5% | 72% |
| Cosmetics | Charlotte Tilbury | 38 | 23 | 2 | 8.7 | 14.3 | 1% | 8% | 7% | 5% | 2% | 4% | 73% |
| Cosmetics | NARS | 27 | 15 | 1 | 6.7 | 20.3 | 2% | 9% | 11% | 5% | 3% | 6% | 64% |
| Cosmetics | MAC Cosmetics | 28 | 16 | 1 | 6.2 | 18.1 | 1% | 6% | 6% | 3% | 1% | 6% | 77% |
| Cosmetics | Rare Beauty | 35 | 26 | 1 | 3.8 | 13.6 | 1% | 8% | 7% | 5% | 2% | 4% | 73% |
| Cosmetics | Fenty Beauty | 38 | 26 | 0 | 0.0 | 13.7 | 1% | 8% | 6% | 5% | 2% | 4% | 75% |
| Cosmetics | Haus Labs | 18 | 9 | 0 | 0.0 | 10.6 | 1% | 11% | 9% | 7% | 6% | 2% | 64% |
| Cosmetics | Huda Beauty | 23 | 22 | 0 | 0.0 | 12.8 | 1% | 7% | 6% | 5% | 1% | 4% | 76% |
| Cosmetics | Kylie Cosmetics | 7 | 7 | 0 | 0.0 | 12.9 | 1% | 7% | 3% | 1% | 2% | 3% | 83% |
| Cosmetics | Maybelline | 28 | 17 | 0 | 0.0 | 14.1 | 1% | 10% | 9% | 3% | 4% | 3% | 71% |
| Cosmetics | NYX Professional Makeup | 22 | 12 | 0 | 0.0 | 18.8 | 1% | 5% | 4% | 11% | 1% | 6% | 73% |
| Automotive | Mercedes-Benz | 28 | 6 | 2 | 33.3 | 18.0 | 6% | 3% | 6% | 1% | 5% | 6% | 72% |
| Automotive | Porsche | 48 | 22 | 2 | 9.1 | 14.9 | 2% | 3% | 15% | 0% | 12% | 8% | 60% |
| Automotive | BMW | 40 | 26 | 0 | 0.0 | 13.5 | 0% | 3% | 18% | 0% | 13% | 8% | 58% |
| Automotive | Toyota | 35 | 24 | 0 | 0.0 | 13.4 | 0% | 3% | 18% | 0% | 13% | 8% | 57% |
| Automotive | Honda | 31 | 23 | 0 | 0.0 | 13.3 | 0% | 3% | 19% | 0% | 14% | 9% | 56% |
| Automotive | Hyundai | 12 | 9 | 0 | 0.0 | 12.8 | 0% | 2% | 14% | 0% | 19% | 6% | 59% |
| Spirits | Del Maguey | 16 | 10 | 6 | 60.0 | 53.1 | 1% | 3% | 8% | 2% | 3% | 1% | 81% |
| Spirits | Johnnie Walker | 10 | 6 | 2 | 33.3 | 37.7 | 2% | 7% | 7% | 1% | 5% | 1% | 78% |
| Spirits | Hennessy | 22 | 7 | 2 | 28.6 | 51.3 | 2% | 7% | 6% | 1% | 6% | 1% | 77% |
| Spirits | Patrón | 14 | 7 | 2 | 28.6 | 51.3 | 2% | 7% | 6% | 1% | 6% | 1% | 77% |
| Spirits | Redbreast | 13 | 10 | 2 | 20.0 | 65.7 | 2% | 2% | 7% | 2% | 6% | 2% | 80% |
| Spirits | Rémy Martin | 17 | 8 | 1 | 12.5 | 54.1 | 1% | 3% | 7% | 2% | 4% | 1% | 81% |
| Spirits | Fortaleza | 23 | 14 | 1 | 7.1 | 42.8 | 0% | 3% | 8% | 1% | 3% | 2% | 81% |

\endgroup

Without an own domain (not rated; reported apart): Pontiac ($m$ = 0, $g$ = 0); Oldsmobile ($m$ = 0, $g$ = 0); Plymouth ($m$ = 0, $g$ = 0); Mercury ($m$ = 0, $g$ = 0); Saturn ($m$ = 0, $g$ = 0). Below the floor of six grounded answers: Audio-Technica ($g$ = 4); Denon ($g$ = 3); Final Audio ($g$ = 0); Koss ($g$ = 0); Spirit Torino ($g$ = 0); ZMF Headphones ($g$ = 1); Estée Lauder ($g$ = 2); Lancôme ($g$ = 0); La Mer ($g$ = 4); Sisley ($g$ = 0); Dior Beauty ($g$ = 1); Chanel Beauty ($g$ = 0); La Prairie ($g$ = 0); Clé de Peau Beauté ($g$ = 0); Rare Beauty ($g$ = 0); Fenty Skin ($g$ = 3); Goop ($g$ = 1); Glossier ($g$ = 1); Tower 28 ($g$ = 3); Paula's Choice ($g$ = 4); Eucerin ($g$ = 2); Bioderma ($g$ = 1); Bobbi Brown ($g$ = 0); Tom Ford Beauty ($g$ = 0); Giorgio Armani Beauty ($g$ = 0); Hourglass ($g$ = 5); Chantecaille ($g$ = 0); Laura Mercier ($g$ = 2); Pat McGrath Labs ($g$ = 2); Anastasia Beverly Hills ($g$ = 1); L'Oréal Paris ($g$ = 2); CoverGirl ($g$ = 0); Revlon ($g$ = 0); Wet n Wild ($g$ = 3); Milani Cosmetics ($g$ = 0); Jaguar ($g$ = 0); Cadillac ($g$ = 3); Rolls-Royce ($g$ = 5); Bentley ($g$ = 5); Tesla ($g$ = 5); Rivian ($g$ = 1); Lucid ($g$ = 0); Polestar ($g$ = 0); Fisker ($g$ = 0); Ford ($g$ = 0); Chevrolet ($g$ = 1); Volkswagen ($g$ = 0); Nissan ($g$ = 0); Jack Daniel's ($g$ = 3); Grey Goose ($g$ = 4); Bacardi ($g$ = 3); Bombay Sapphire ($g$ = 0); Jameson ($g$ = 0); Lagavulin ($g$ = 3); Clase Azul ($g$ = 0); Hendrick's ($g$ = 2); Woodford Reserve ($g$ = 1); Monkey 47 ($g$ = 1); The Balvenie ($g$ = 3); Casamigos ($g$ = 0); Compass Box ($g$ = 3); Nikka ($g$ = 1); Fernet-Branca ($g$ = 3); St. George Spirits ($g$ = 2); Mezcal Vago ($g$ = 3).

# Appendix B: sensitivity details {-}

Table: Leave one category out (S8): $\rho_w$ of G\* with P and $C^*$ in each condition, and rel3, with the category named left out.

| Left out | H1 S1 | H1 S0 | H2 S1 | H2 S0 | rel3 | Verdicts |
|:--------------|-----:|-----:|------:|-----:|----:|:------------------------------------------|
| Headphones | 0.310 | 0.409 | -0.258 | 0.036 | -- | H1 MARGINAL, H2 CONFIRMED, H3 UNDETERMINED |
| Skincare | 0.255 | 0.346 | 0.011 | 0.036 | -- | H1 MARGINAL, H2 CONFIRMED, H3 UNDETERMINED |
| Cosmetics | 0.211 | 0.333 | 0.058 | 0.069 | -- | H1 MARGINAL, H2 CONFIRMED, H3 UNDETERMINED |
| Automotive | 0.322 | 0.400 | -0.112 | 0.080 | -- | H1 MARGINAL, H2 CONFIRMED, H3 UNDETERMINED |
| Spirits | 0.405 | 0.466 | -0.120 | 0.025 | -- | H1 MARGINAL, H2 CONFIRMED, H3 UNDETERMINED |

Table: Citations against sources per provider (MQ8; reported only).

| Provider | Answers | With citations | Share | Cited URLs | Also in sources |
|:-------------|-------:|--------------:|-----:|----------:|---------------:|
| Anthropic | 90 | 75 | 83.3% | 557 | 100.0% |
| OpenAI | 90 | 86 | 95.6% | 516 | 98.6% |
| Google | 90 | 16 | 17.8% | 122 | 100.0% |
