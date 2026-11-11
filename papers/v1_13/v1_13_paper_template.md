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

Pre-registration, Part I: \texttt{v1.13-prereg-r1} (commit \texttt{ {{PREREG_COMMIT}} }; deposited on OSF before any search record was read)\\
Pre-registration, Part II: {{PART2_TITLE_LINE}}\\
Data and code: OSF \texttt{ec6wh}, \texttt{methodology/v1\_13}\\

\end{center}
\end{titlepage}

# Abstract {-}

Presence records whether AI answers name a brand; it does not record what an answer rests on when the model searches the web. This pre-registered study specifies a Grounding instrument for the AIAS measurement programme and tests whether it is separable from Presence and Consistency. A fixed rule, frozen before any search-on answer existed, classifies every source returned by the search records of the programme's fourth omnibus wave ($t_4$: Claude Fable 5.2, GPT-6 Astra and Gemini 4 Argon, search on, six category questions per category in three runs, five categories, 112 brand units). The Grounding score G\* is the share of a brand's grounded answers whose retrieved sources include the brand's own domain. {{N_CAT_ANSWERS}} answered search-on category answers entered the score{% if ANY_DROPPED %} after {{DROPPED_NAMES}} left the primary score under the pre-registered quality checks{% endif %}, and {{RATED_N}} of {{UNITS_N}} brand units met the rating floor.
{% switch CASE_GATE %}
{% case PASS %}
Within category, G\* was separable from Presence and from Consistency in both search conditions and held across runs (rel3 = {{H3_REL3}}); the pre-registered gate returned PASS, and a second Grounding paper may be pre-registered on this instrument.
{% case FAIL %}
The pre-registered gate returned FAIL: {{FAIL_LEGS_PLAIN}} {{FAIL_VERB}} falsified. On this instrument G\* is not a separate component; the result is reported with the prominence of a pass, and Grounding returns to design under a new pre-registration.
{% case MARGINAL %}
No gate leg was falsified, but not every leg was confirmed ({{NOTCONF_LEGS_PLAIN}}); the pre-registered gate returned MARGINAL, and a second paper follows only on the pre-registrant's recorded decision.
{% case MARGINAL_DOWNGRADED %}
Every primary gate leg was confirmed, but separability against {{DOWN_LEGS_PLAIN}} was falsified, and under the pre-registered rule the gate's PASS was downgraded to MARGINAL; a second paper follows only on the pre-registrant's recorded decision.
{% case UNDETERMINED_MQ5 %}
The score was degenerate under the pre-registered check MQ5 ({{MQ5_ZERO_SHARE}} of rated brands at zero), so the separability legs could not be decided and the gate returned UNDETERMINED; the instrument goes back to design.
{% case UNDETERMINED %}
The gate returned UNDETERMINED because {{UNDET_LEGS_PLAIN}} fell below the pre-registered floor of 30 units; the instrument goes back to design.
{% endswitch %}
{% switch CASE_H7 %}
{% case CONFIRMED|MARGINAL|FALSIFIED %}
A structured-data audit of the brands' own websites and Wikidata records (Part II) gave a richness index whose within-category correlation with G\* was ρ = {{H7_RHO}} (H7 {{H7_WORD}}).
{% case UNDETERMINED_FLOOR %}
The structured-data audit (Part II) was collected, but too few brands had both scores for its test (H7 UNDETERMINED).
{% case NOT_COLLECTED %}
The structured-data audit (Part II) was not collected before the final analysis stage, so its test is handed to the second paper.
{% case PENDING %}
The structured-data audit (Part II) and the conditional legs are reported at the final analysis stage.
{% endswitch %}

**Keywords:** AI availability; brand availability; AIAS; pre-registration; Ehrenberg-Bass; large language models; web search; retrieval grounding; structured data; separability; measurement validity

**JEL codes:** M31; L86, L15, D83, M37

**Paper status:** Pre-registered methodology paper, re-analysis of stored $t_4$ answers (Part I) {% if PART2_COLLECTED %}and new public web data (Part II){% else %}without Part II data{% endif %}; no model was called and nothing was spent. Gate verdict {{GATE_FINAL}}{% if STAGE_C1_ONLY %} at Stage C1 (interim: Stage C2 not yet run){% endif %}; {{DEV_STATUS}} Part of the AIAS measurement programme.

# 1. Introduction

AI Availability --- the discoverability and representation of a brand in the outputs of large language models (LLMs) --- has been proposed as a third layer of brand availability (González Castro, 2026a) beside the Mental and Physical Availability of the Ehrenberg-Bass tradition (Sharp, 2010; Sharp & Romaniuk, 2021), within the Tri-System framework (González Castro, 2026c). The AIAS programme builds the components of an AI availability score one at a time, each pre-registered and locked before it is used (González Castro, 2026b). Presence is whether and how often models name a brand (Methodology v1.6). Consistency is how evenly the models of a panel name it, measured by the dispersion statistic $\varphi$ (v1.8) and scaled to $C^*$ (v1.9). The AIAS 2.0 synthesis showed Consistency separable from Presence: within category, $|\rho(C^*, P)|$ was 0.073, 0.082 and 0.189 at the three waves $t_1$--$t_3$, as published under the uncentred pooled-rank convention that this study replaces (pre-registration §0).

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

A brand's own domains $D_b$ come from a frozen offline list, one row per brand unit, each domain taken from a dated public record (Wikidata's official website, else the English Wikipedia infobox, else web-search results corroborated by a directory) under the decision rules D1--D6 of §2.3; nothing was looked up at analysis time. The list holds 107 resolved units and 5 with no own domain (the five defunct automotive brands of the v0.22 registry), and no unresolved unit. A unit without an own domain is not rated and is reported apart. Three units take a house or portal domain under rule D4 --- Dior Beauty (dior.com), Chanel Beauty (chanel.com) and Lagavulin (malts.com) --- so any source on those domains counts as their own; their G\* is reported with that flag (§2.3).

## 2.4 The Grounding score

Over the N3 search-on category answers of a brand's category, all three runs pooled (§2.4): $m_b$ is the number of answers naming brand $b$; $g_b$ the number of those with at least one source that resolves to a class other than unresolved (grounded answers); and $o_b$ the number of those whose resolved source domains include a domain in $D_b$. The own-domain source share is $G_b = o_b/g_b$, and

$$
G^*_b = 100\,G_b, \quad \text{rated iff } g_b \geq 6 \text{ and } b \text{ has a } D_b .
$$

The floor of six is the Consistency floor. For every rated brand the source mix (for each class, the mean over $b$'s grounded answers of the share of the answer's distinct resolved domains in that class) and the mean number of distinct resolved domains per grounded answer are reported; no verdict rests on them.

## 2.5 Structured-data audit (Part II)

Part II fetches at most three public pages of each brand's own site (home page, the first about page and the first product page linked from it), under `robots.txt`, at least ten seconds between requests to one host, and no request between 17 and 22 November 2026, and reads the brand's public Wikidata record (protocol §3--§4). The structured-data richness index is SDRI $= 100 \times$ (sum of eight binary indicators)/8: (1) a schema.org Organization or subtype on the home page; (2) a Brand node; (3) a Product or subtype; (4) at least one `sameAs` on an Organization or Brand node; (5) a `sameAs` to Wikidata or Wikipedia; (6) a Wikidata item (adjudicated QID); (7) that item's official website in $D_b$; (8) an English Wikipedia article linked from the item. $\text{SDRI}_{\text{site}}$ uses (1)--(5) and $\text{SDRI}_{\text{kg}}$ (6)--(8). A brand whose home page could not be fetched has SDRI not rated; the five defunct brands are audited for (6)--(8) only and never enter H7 (protocol §1, §5).

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

**Gate rule (§3).** PASS if and only if H1, H2 and H3 are all CONFIRMED --- downgraded to MARGINAL if an active secondary separability leg (H4--H6; H4 only as above) is FALSIFIED; a leg computed at Stage C2 re-issues the gate verdict with its own timestamp, downgrade only. FAIL if H1, H2 or H3 is FALSIFIED. UNDETERMINED if H1 or H2 is UNDETERMINED (published as such; the instrument goes back to design). Otherwise MARGINAL: the pre-registrant decides, on the record, whether the second paper proceeds. H7 never changes the gate.

## 2.8 Quality checks and sensitivity analyses

Eight checks were pre-registered (§4). MQ1: the parser completes on every answered search-on record, in both fields. MQ2: per model, the share of category answers with at least one source; below 0.25 the model is flagged "search rarely used", below 0.10 it leaves the primary G\*. MQ3: the share of distinct (answer, domain) pairs classed other or unresolved; above 0.40 flagged, above 0.60 the source-mix descriptives are labelled low coverage. MQ4: the share of Gemini sources whose domain is read from the title and the share left unresolved; above 0.20 unresolved, Gemini leaves the primary G\*. MQ5: the gate is UNDETERMINED if more than 80% of rated brands have G\* = 0 or the within-category spread of G\* is zero in three or more categories. MQ6: $\rho_w(g_b, \hat\pi_{S1})$ and $\rho_w(G^*, g_b)$ are reported, and $|\rho_w(G^*, g_b)| \geq 0.50$ is flagged (the share tracks the count). MQ7: the frozen lists and v0.42's coder and scorer equal their anchored hashes, else the run halts. MQ8: per provider, the share of answers with citations and the share of cited URLs also among the sources (reported only).

Sensitivities (§7) never change a verdict; any verdict that would differ is listed beside it: S1 denominator $m_b$ instead of $g_b$; S2 the cited set; S4 rating floors 3 and 10; S5 Gemini kept or dropped against the MQ4 decision; S6 $D_b$ as verified by Part II; S7 P and $C^*$ from AIAS 2.0 at $t_3$ (cross-panel); S8 leave one category out; S9 URLs written in the answer text added; S10 the uncentred convention; S11 every gate statistic without the Denon unit (Declarations). S3 was removed because $t_4$ collected no second Claude model.

## 2.9 Pre-registration and lock

Part I was locked at git tag `v1.13-prereg-r1` (commit `{{PREREG_COMMIT}}`, tagged {{PREREG_TAG_UTC}} UTC) and deposited on OSF (`ec6wh`, `methodology/v1_13/`: `prereg/`, `registries/`, `anchor/`) with the SHA-256 of every locked file; its anchor record names the tag's commit and the activation of H4--H6. The text states that Part I would lock no earlier than 11 November 2026 at about 3 pm CT; it was locked earlier because the pre-registrant waived the 24-hour review on 10 November 2026 at 20:26 CT, as the deviations record states in an entry made before the tag (Entry 0a). The locked text is unchanged by it. {{PART2_LOCK_SENTENCE}} The scorer (`score_v1_13.py`) and the audit (`audit_v1_13.py`) were written and unit-tested on synthetic data before the lock; Stage C1 refuses to run without the tag, the anchor and matching hashes. Choices the text leaves open are listed in the scorers' notes and in the pre-registration's change log (§12). {{DEV_SENTENCE}}

# 3. Results

## 3.1 Data and quality checks

{% if STAGE_C1_ONLY %}[Interim: only Stage C1 has run; the conditional legs and H7 are reported at Stage C2.] {% endif %}{{MQ1_N}} answered search-on records were parsed in both fields without error (MQ1), and MQ7 passed (Stage C1 halts otherwise). {{N_CAT_ANSWERS}} answered category answers of the primary panel entered G\*. {% if ANY_DROPPED %}{{DROPPED_SENTENCE}}{% else %}No model left the primary score: every model's search returned sources often enough (MQ2) and Gemini's redirect sources were resolved (MQ4; unresolved share {{MQ4_UNRES}}).{% endif %} {% if MQ2_ANY_FLAG %}MQ2 flagged {{MQ2_FLAGGED}} as "search rarely used" (below 0.25); every result is read with that flag.{% else %}No model was flagged as using search rarely (MQ2).{% endif %} Of the distinct (answer, domain) source pairs, {{MQ3_SHARE}} were classed other or unresolved (MQ3){% if MQ3_LOW %}, above 0.60, so the source-mix descriptives below are labelled **low coverage**{% else %}{% if MQ3_FLAG %}, above the 0.40 flag{% else %}, within the 0.40 flag{% endif %}{% endif %}. {% if MQ6_FLAG %}MQ6 was flagged: $\rho_w(G^*, g_b) = {{MQ6_GSTAR_G}}$, so the share partly tracks the number of grounded answers.{% else %}G\* did not track the number of grounded answers ($\rho_w(G^*, g_b) = {{MQ6_GSTAR_G}}$, MQ6), while $\rho_w(g_b, \hat\pi_{S1}) = {{MQ6_G_PI}}$.{% endif %} {% if MQ5_FAILED %}MQ5 failed: {{MQ5_ZERO_SHARE}} of rated brands had G\* = 0 (limit 80%){{MQ5_FLAT_CLAUSE}}.{% else %}{{MQ5_ZERO_SHARE}} of rated brands had G\* = 0 (MQ5 limit 80%){{MQ5_FLAT_CLAUSE}}, so MQ5 passed.{% endif %}

Table: Search use and source checks per model (MQ2, MQ4) and citations per provider (MQ8).

{{TABLE_MQ}}

## 3.2 The instrument and the cross-category baseline

{{RATED_N}} of {{UNITS_N}} brand units were rated ({{NOTRATED_FLOOR_N}} below the floor of six grounded answers; {{NOTRATED_NODB_N}} without an own domain, reported apart). {{BASE_SENTENCE}} Figure 1 shows how often each model's search returned sources, Figure 2 what the sources were, and Figure 3 the distribution of G\*. {% if MQ3_LOW %}The source-mix descriptives are labelled low coverage (MQ3).{% endif %} {{HOUSE_SENTENCE}}

![Share of search-on category answers whose search record holds at least one source, per category and model. {{FIG_CAPTION}}]({{FIG_DIR}}/chart_01_search_use.pdf){#fig:search width=92%}

![Mean source-type mix of search-on category answers per category and model: each answer's distinct resolved domains split by class, each answer weighing one. {{FIG_CAPTION}}]({{FIG_DIR}}/chart_02_source_mix.pdf){#fig:mix width=100%}

Table: G\* per category, computed on all three N3 models as the baseline of §6 is defined: units, rated units, median and interquartile range of G\*, and the share of rated units at zero.

{{TABLE_GSTAR}}

![G\* per rated brand by category (box: median and interquartile range). {{FIG_CAPTION}}]({{FIG_DIR}}/chart_03_gstar_by_category.pdf){#fig:gstar width=92%}

The 20 most-retrieved domains across all category answers (number of answers whose sources include the domain) were: {{TOP_DOMAINS}}.

## 3.3 Separability and reliability (the gate legs)

**Presence (H1).** {% switch CASE_H1 %}{% case CONFIRMED|MARGINAL|FALSIFIED %}Across {{H1_S1_N}} rated brands, $\rho_w(G^*, P_{S1}) = {{H1_S1_RHO}}$ (90% interval {{H1_S1_LO}} to {{H1_S1_HI}}; two-sided $p = {{H1_S1_P}}$), and across {{H1_S0_N}}, $\rho_w(G^*, P_{S0}) = {{H1_S0_RHO}}$ (90% interval {{H1_S0_LO}} to {{H1_S0_HI}}; $p = {{H1_S0_P}}$).{% case UNDETERMINED_FLOOR %}The legs had {{H1_S1_N}} and {{H1_S0_N}} units in categories with at least five entered, and at least one is below the floor of 30.{% case UNDETERMINED_MQ5 %}MQ5 failed, so H1 is not decided; the statistics are reported for the record: $\rho_w(G^*, P_{S1}) = {{H1_S1_RHO}}$ and $\rho_w(G^*, P_{S0}) = {{H1_S0_RHO}}$.{% endswitch %}
{% switch CASE_H1 %}
{% case CONFIRMED %}
Both $|\rho_w|$ are at most 0.30, and H1 is **CONFIRMED**: how often a brand's own site is among the sources of the answers that name it does not follow how present the brand is.
{% case MARGINAL %}
Neither leg reaches 0.50, but not both are at most 0.30, and H1 is **MARGINAL**.
{% case FALSIFIED %}
At least one $|\rho_w|$ is 0.50 or more, and H1 is **FALSIFIED**: G\* moves with Presence.
{% case UNDETERMINED_FLOOR|UNDETERMINED_MQ5 %}
H1 is **UNDETERMINED**.
{% endswitch %}
Figure 4 shows both legs under every pre-registered analysis.

![$\rho_w$ of G\* with Presence in each condition, for the primary analysis (with its 90% interval) and each sensitivity analysis and left-out category; shaded: $|\rho_w| \leq 0.30$. {{FIG_CAPTION}}]({{FIG_DIR}}/chart_04_presence_legs.pdf){#fig:h1 width=100%}

**Consistency (H2).** {% switch CASE_H2 %}{% case CONFIRMED|MARGINAL|FALSIFIED %}Across {{H2_S1_N}} brands rated on both scores, $\rho_w(G^*, C^*_{S1}) = {{H2_S1_RHO}}$ (90% interval {{H2_S1_LO}} to {{H2_S1_HI}}; $p = {{H2_S1_P}}$), and across {{H2_S0_N}}, $\rho_w(G^*, C^*_{S0}) = {{H2_S0_RHO}}$ (90% interval {{H2_S0_LO}} to {{H2_S0_HI}}; $p = {{H2_S0_P}}$).{% case UNDETERMINED_FLOOR %}The legs had {{H2_S1_N}} and {{H2_S0_N}} units in categories with at least five entered, and at least one is below the floor of 30.{% case UNDETERMINED_MQ5 %}MQ5 failed, so H2 is not decided; the statistics are reported for the record: $\rho_w(G^*, C^*_{S1}) = {{H2_S1_RHO}}$ and $\rho_w(G^*, C^*_{S0}) = {{H2_S0_RHO}}$.{% endswitch %}
{% switch CASE_H2 %}
{% case CONFIRMED %}
Both $|\rho_w|$ are at most 0.30, and H2 is **CONFIRMED**.
{% case MARGINAL %}
Neither leg reaches 0.50, but not both are at most 0.30, and H2 is **MARGINAL**.
{% case FALSIFIED %}
At least one $|\rho_w|$ is 0.50 or more, and H2 is **FALSIFIED**: G\* moves with Consistency.
{% case UNDETERMINED_FLOOR|UNDETERMINED_MQ5 %}
H2 is **UNDETERMINED**.
{% endswitch %}
Figure 5 shows both legs under every pre-registered analysis.

![$\rho_w$ of G\* with Consistency $C^*$ in each condition, for the primary analysis (with its 90% interval) and each sensitivity analysis and left-out category; shaded: $|\rho_w| \leq 0.30$. {{FIG_CAPTION}}]({{FIG_DIR}}/chart_05_consistency_legs.pdf){#fig:h2 width=100%}

**Run reliability (H3).** {% switch CASE_H3 %}{% case CONFIRMED|MARGINAL|FALSIFIED %}With G\* computed per run (floor three grounded answers), {{H3_NQ}} of the three run pairs had at least 30 units rated in both runs; their mean $\rho_w$ was rel1 = {{H3_REL1}}, so rel3 = {{H3_REL3}} (one-sided $p = {{H3_P}}$).{% case UNDETERMINED_PAIRS %}With G\* computed per run (floor three grounded answers), only {{H3_NQ}} of the three run pairs had at least 30 units rated in both runs.{% endswitch %}
{% switch CASE_H3 %}
{% case CONFIRMED %}
That meets rel3 $\geq 0.50$ with $p < 0.05$, and H3 is **CONFIRMED**: G\* orders brands alike from run to run, so its separability is not the separability of noise.
{% case MARGINAL %}
That is not below 0.30 and does not meet rel3 $\geq 0.50$ with $p < 0.05$, and H3 is **MARGINAL**.
{% case FALSIFIED %}
That is below 0.30, and H3 is **FALSIFIED**: G\* does not order brands reproducibly across runs, so whatever separability it shows cannot be read as a property of the brands.
{% case UNDETERMINED_PAIRS %}
Two qualifying pairs are needed, and H3 is **UNDETERMINED**.
{% endswitch %}
The pairs are tabulated below and shown in Figure 6.

Table: Agreement of per-run G\* between runs (H3): units rated in both runs, $\rho_w$, and whether the pair qualifies (at least 30 units).

{{TABLE_H3}}

![$\rho_w$ of per-run G\* between each pair of runs, with the number of brands rated in both runs; the dotted lines mark the rel3 bars of 0.50 and 0.30 converted to the scale of one pair. {{FIG_CAPTION}}]({{FIG_DIR}}/chart_06_run_pairs.pdf){#fig:h3 width=88%}

## 3.4 Conditional legs: Ranking, Sentiment and Coverage

**Ranking (H4).** {% switch CASE_H4 %}{% case INACTIVE %}H4 is INACTIVE: its activation condition was not met at the lock.{% case PENDING %}H4 is pending: v1.14's Stage 1 output did not exist at Stage C1, and the leg does not run before it.{% case UNAVAILABLE %}v1.14's Stage 1 output, which supplies $R^*_{S1}$, did not exist by Stage C2 ({{H4_WHY}}); H4 is **UNDETERMINED** (score not available) and is handed to the second paper.{% case GATING %}H4 was computed at Stage {{H4_STAGE}} from v1.14's Stage 1 output, whose interim verdict was {{H4_STAGE1}}, so H4 is gating. Across {{H4_N}} brands rated on both, $\rho_w(G^*, R^*_{S1}) = {{H4_RHO}}$ (90% interval {{H4_LO}} to {{H4_HI}}; $p = {{H4_P}}$), and H4 is **{{H4_WORD}}**.{% case REPORTED %}H4 was computed at Stage {{H4_STAGE}} from v1.14's Stage 1 output, whose interim verdict was {{H4_STAGE1}}, not SEPARABLE, so under the pre-registered rule H4 neither gates nor downgrades. Across {{H4_N}} brands rated on both, $\rho_w(G^*, R^*_{S1}) = {{H4_RHO}}$ (90% interval {{H4_LO}} to {{H4_HI}}; $p = {{H4_P}}$), which reads **{{H4_WORD}}** under the separability bands.{% endswitch %}{% if H4_BELOW_FLOOR %} The leg had fewer than 30 units in categories with at least five.{% endif %}

**Sentiment (H5).** {% switch CASE_H5 %}{% case INACTIVE %}H5 is INACTIVE: no locked Sentiment score on the $t_4$ answers was tagged before the lock, so it has no verdict and may be tested only under a later pre-registration.{% case ACTIVE %}H5 was active, and its verdict is **{{H5_WORD}}**.{% endswitch %}

**Coverage (H6).** {% switch CASE_H6 %}{% case INACTIVE %}H6 is INACTIVE: its activation condition was not met at the lock.{% case PENDING %}H6 is pending: v1.12's scored Coverage output did not exist at Stage C1.{% case UNAVAILABLE %}v1.12's Cov\* output did not exist by Stage C2 ({{H6_WHY}}); H6 is **UNDETERMINED** (score not available) and is handed to the second paper.{% case COMPUTED %}H6 was computed at Stage {{H6_STAGE}} from v1.12's locked Cov\* (N3, search off). Across {{H6_N}} brands rated on both, $\rho_w(G^*, \text{Cov}^*) = {{H6_RHO}}$ (90% interval {{H6_LO}} to {{H6_HI}}; $p = {{H6_P}}$), and H6 is **{{H6_WORD}}**.{% endswitch %}{% if H6_BELOW_FLOOR %} The leg had fewer than 30 units in categories with at least five.{% endif %}

## 3.5 The gate verdict

{% switch CASE_GATE %}
{% case PASS %}
H1, H2 and H3 were CONFIRMED, and no active gating secondary leg was FALSIFIED. The gate verdict is **PASS**.
{% case FAIL %}
{{FAIL_LEGS}} {{FAIL_VERB}} FALSIFIED. The gate verdict is **FAIL**: a negative result, reported with the same prominence as a pass.
{% case MARGINAL %}
No gate leg was FALSIFIED and neither H1 nor H2 was UNDETERMINED, but {{NOTCONF_LEGS_WORDS}}. The gate verdict is **MARGINAL**.
{% case MARGINAL_DOWNGRADED %}
H1, H2 and H3 were CONFIRMED, but {{DOWN_LEGS}} {{DOWN_VERB}} FALSIFIED, and under the pre-registered rule the PASS is downgraded. The gate verdict is **MARGINAL**.
{% case UNDETERMINED_MQ5 %}
MQ5 failed, so H1 and H2 are UNDETERMINED, and the gate verdict is **UNDETERMINED**.
{% case UNDETERMINED %}
{{UNDET_LEGS}} {{UNDET_VERB}} UNDETERMINED (below the floor), and the gate verdict is **UNDETERMINED**.
{% endswitch %}
{{GATE_HISTORY}} Figure 7 shows every computed leg against its bands.

Table: Every pre-registered leg: the comparator, its role, the number of units, $\rho_w$ (H3: rel3) with its 90% interval, the permutation $p$ and the verdict, in the scorer's words.

{{TABLE_LEGS}}

![All computed legs against their bands: separability legs (H1, H2, H4, H6) with the band $|\rho_w| \leq 0.30$ shaded and $|\rho_w| = 0.50$ dotted; H3's rel3 against 0.50 and 0.30; H7 against 0.30 and 0.10. Indigo: legs that can decide or downgrade the gate; gray: reported only. {{FIG_CAPTION}}]({{FIG_DIR}}/chart_07_legs_bands.pdf){#fig:legs width=100%}

## 3.6 Structured data (Part II) and H7

{% switch CASE_PART2 %}
{% case COLLECTED %}
{{SDRI_SENTENCE}}
{% case LOCKED_NOT_COLLECTED %}
Part II was locked, but its audit had not been collected when Stage C2 ran, so no website data enter this paper.
{% case NOT_LOCKED %}
Part II was not locked before Stage C2 (tag `v1.13-audit-r1` does not exist), so no website was fetched and no structured data enter this paper.
{% case PENDING %}
Part II is reported at Stage C2.
{% endswitch %}
{% switch CASE_H7 %}
{% case CONFIRMED|MARGINAL|FALSIFIED %}
Across {{H7_N}} brands with both scores, $\rho_w(\text{SDRI}, G^*) = {{H7_RHO}}$ (90% interval {{H7_LO}} to {{H7_HI}}; one-sided $p = {{H7_P}}$), and H7 is **{{H7_WORD}}**{% if H7_IS_CONFIRMED %}: brands with richer structured data had higher own-domain source shares{% endif %}{% if H7_IS_FALSIFIED %}: richer structured data did not go with a higher own-domain source share{% endif %}. Beside it, $\rho_w(\text{SDRI}, P_{S0}) = {{H7_RHO_P}}$ and the partial $\rho_w(\text{SDRI}, G^* \mid P_{S0}) = {{H7_PARTIAL}}$. H7 never changes the gate (Figure 8).
{% case UNDETERMINED_FLOOR %}
Only {{H7_N}} brands had both an SDRI and a rated G\* in categories with at least five, below the floor of 30, and H7 is **UNDETERMINED** (Figure 8).
{% case NOT_COLLECTED %}
H7 is **UNDETERMINED**: Part II was not collected before Stage C2, and the test is handed to the second paper (§8).
{% case PENDING %}
H7 is tested at Stage C2.
{% endswitch %}

{% if PART2_COLLECTED %}
Table: Structured-data audit per category: brands audited (defunct brands excluded), home pages fetched, median SDRI and the share of brands with each indicator.

{{TABLE_SDRI}}

![SDRI and G\* per brand with both, by category. {{FIG_CAPTION}}]({{FIG_DIR}}/chart_08_sdri_gstar.pdf){#fig:h7 width=88%}
{% endif %}

## 3.7 Sensitivity analyses

The table below gives the gate statistics under each pre-registered sensitivity. {{SENS_CHANGES_SENTENCE}} {{S11_SENTENCE}} Leaving one category out (S8), $\rho_w(G^*, P_{S1})$ ranged from {{S8_H1_LO}} to {{S8_H1_HI}} and rel3 from {{S8_REL_LO}} to {{S8_REL_HI}} (Appendix). {{S7_SENTENCE}} Sensitivity S6 ($D_b$ as verified by Part II) is not computed by the locked scorer's core and is not reported here.

Table: Pre-registered sensitivity analyses (§7): $\rho_w$ of G\* with P and $C^*$ in each condition, rel3, and the gate verdict each would give; a leg verdict different from the primary one is marked with its word. Sensitivities never change a verdict.

{{TABLE_SENS}}

# 4. Discussion

{% switch CASE_GATE %}
{% case PASS %}
Grounding, measured as the share of a brand's grounded answers whose retrieved sources include its own site, passed its separability gate on $t_4$: it is separable from Presence and from Consistency in both search conditions, and it orders brands reproducibly across runs. Under the plan of record a second Grounding paper may now be pre-registered; it inherits the frozen parser, class lists, $D_b$, scorer and tests (§8) and studies source coverage over waves, phantom-brand grounding, identity load and a typology. Whether G\* enters a combined score is decided in the component calibration that follows the second papers, not here.
{% case FAIL %}
On this instrument Grounding did not pass its gate: {{FAIL_LEGS_PLAIN}} {{FAIL_VERB}} falsified. The pre-registered consequence is that no second Grounding paper follows on G\*; the instrument goes back to design, and a redesigned score needs its own pre-registration and its own gate. The result does not show that what answers retrieve is irrelevant to AI Availability; it shows that this share, on these categories and models, does not carry information separate from {{FAIL_LEGS_PLAIN}}. The parts of the instrument that do not depend on the score --- the source classification, the domain list and the baseline of §3.2 --- remain available to a redesign.
{% case MARGINAL|MARGINAL_DOWNGRADED %}
The gate's result is intermediate: no primary leg was falsified, but not every condition for a pass was met. Under the pre-registered rule a second paper proceeds only on the pre-registrant's recorded decision, with the condition that was not met as its first confirmatory test. Until then G\* is a candidate measure reported beside Presence and Consistency, not combined with them.
{% case UNDETERMINED_MQ5|UNDETERMINED %}
The gate could not decide, and under the pre-registered rule the result is published as such and the instrument goes back to design. No second paper follows on this instrument until the cause reported in §3 is addressed under a new pre-registration.
{% endswitch %}

{% switch CASE_H7 %}
{% case CONFIRMED|MARGINAL|FALSIFIED|UNDETERMINED_FLOOR %}
The structured-data audit describes, for the same brands, whether their own sites and public knowledge-graph records carry the markup that search systems can read; H7 relates it to G\* and changes no gate verdict.
{% case NOT_COLLECTED|PENDING %}
The structured-data question (RQ5) is not answered here; it passes to the second paper with the audit protocol unchanged.
{% endswitch %}
The baseline of §3.2 describes, on the newest models, what category answers retrieve when search is on; it carries no verdict.

# 5. Limitations

Recognition (the $C_P$ part of P) rests on one search-off brand answer per model. Search-on answers depend on the web on the day and on each provider's search back-end; they are reproducible only as recorded. The retrieved set includes results an answer did not use, and what it holds differs by provider, so model differences mix model and tool; the cited set (S2) is what the answer attributes. Own-domain retrieval needs the brand's site to be indexed and open to crawlers, so a low G\* can reflect robots policies as much as model behaviour. $D_b$ is a declared list and can miss regional or campaign domains. The study covers five categories, one market and one language (US English). The audit reads static HTML only, so structured data injected by JavaScript is missed (§9). The verdict file does not record the hashes of its inputs ($t_4$ raw file, coder tables, brand table); they are recorded in the deposit beside it.{% if MQ6_FLAG %} MQ6 was flagged (§3.1).{% endif %}{% if MQ3_LOW %} The source mix is labelled low coverage (MQ3).{% endif %}

# 6. What a second paper inherits

Pre-registered separately, only after PASS or after MARGINAL with the pre-registrant's recorded decision (§8): the locked parser, `source_classes_v1_13.md`, $D_b$, the scorer and its tests; the per-answer source tables; source-coverage stability over waves ($t_4$, v0.40's search-on arm, $t_5$, $t_6$, each re-classified with the frozen lists); phantom-brand grounding; identity load; a typology of G\* with P, $C^*$ and $R^*$; H7 if Part II was not collected in time; any active conditional leg whose score did not exist by Stage C2; and re-audits of structured data at $t_5$ and $t_6$.

# Declarations {-}

## Conflict of interest {-}

The author is Director, Corporate Brand Creative and Governance at Samsung Electronics America. This study performs no new brand selection: it re-uses the five omnibus registries (v0.19--v0.23) and carries forward each registry's source-phase COI handling unchanged. Part II fetches public pages of the registry brands' own websites; it contacts no brand and buys nothing. Two items of record apply, quoted from their source records. *v0.19 audiophile headphones* (`osf/v19/PRE_REGISTRATION_v0_19.md` §2.3): "AKG removed from Cell A short-list; Denon substituted. AKG is Samsung-owned since 2016. The author's COI declaration names Samsung; including AKG would invite the kind of reviewer suspicion AIAS™ 1.0 does not need to absorb. Denon carries comparable heritage stature (founded 1910; AH-D7000 → D9200 audiophile line) and removes the question. Decision rationale recorded here for audit trail." *v0.22 automotive* (v0.22 Declarations §COI): "Samsung subsidiaries hold tier-2/3 component supply relationships with several brands in the v0.22 registry: Harman International (audio systems) supplies Mercedes-Benz, BMW, and other premium automotive OEMs; Samsung SDI (battery cells) supplies BMW (i-series), Volkswagen Group brands including Bentley and Porsche (Stellantis-adjacent platforms), and others; Samsung Display (infotainment) supplies Mercedes-Benz and BMW. Tesla and Polestar also have tangential Samsung-component exposure at the parts level. These are non-competitive supply relationships; Samsung Electronics America does not produce or market passenger car brands and has no brand-level competitive overlap with any v0.22 registry entry. The COI was screened and documented in DEVIATIONS Entry 0 (Part B) of the pre-registration module; no operational restriction on registry composition was imposed." Correction (November 10, 2026): Denon, which replaced AKG in the v0.19 registry, has itself been owned by Harman International, a wholly owned subsidiary of Samsung Electronics, since September 23, 2025, when Harman completed its acquisition of Sound United from Masimo; the v0.19 headphones registry therefore includes one Samsung-group brand. The substitution did not achieve its purpose, and this was not noticed until November 10, 2026. Source: HARMAN press release, Business Wire, September 23, 2025. Handling here: Denon stays in the registry; every gate statistic is also reported without the Denon unit (sensitivity S11), with any verdict change listed next to the verdict; Part II audits Denon's website under the same rules as every other brand's.{% if COI_CHEIL %} {{CHEIL_SENTENCE}}{% endif %} Samsung Electronics had no role in the design, conduct, analysis or reporting of this work.

## Funding {-}

Self-funded. No external funding supported this research.

## Ethics {-}

No human subjects. Part II reads public web pages under the protocol's robots and rate rules.

## Use of AI tools {-}

During the preparation of this work the author used AI tools (Anthropic's Claude) to assist with study design, analysis and writing. The author reviewed and edited all content and takes full responsibility for it.

## Data and code availability {-}

Materials are deposited at OSF (osf.io/ec6wh), `methodology/v1_13/`: the locked pre-registration with the source-classification rule, the audit protocol and its dry-run record, the brand-domain list and the Wikidata word list, the scorer and audit scripts with their tests and synthetic fixtures, the lock manifest, the deviations record and the anchor records (`prereg/`, `registries/`, `anchor/`; the locked Part I text is at <https://osf.io/ec6wh/files/osfstorage/6af3d7c5ca45e46a8b9d8d42>). At publication the deposit adds the verdict file (`v1_13_verdicts.json`){% if PART2_COLLECTED %}, the audit's structured-data records and SDRI table (`audit/`; raw HTML is not deposited){% endif %} and the figure sources. The code is also in the programme's GitHub repository (github.com/thirdsystem-aias/aias) at tag `v1.13-prereg-r1`.

# References {-}

González Castro, P. U. (2026a). *AI Availability: A Theoretical Framework for Brand Surfacing in the Age of LLM-Mediated Discovery*. SSRN Working Paper 6659000. Third System.

González Castro, P. U. (2026b). *The AIAS Presence Measurement Protocol: Methodological Notes on Construct Validity and the Four-Regime Taxonomy, v1.2*. SSRN Working Paper 6761698. Third System.

González Castro, P. U. (2026c). *Tri-System Brand Growth: Mental, Physical, and AI Availability in Brand Architecture*. MSI Working Paper. Marketing Science Institute.

Sharp, B. (2010). *How Brands Grow: What Marketers Don't Know*. Oxford University Press.

Sharp, B., & Romaniuk, J. (2021). *How Brands Grow Part 2: Including Emerging Markets, Services, Durables, New and Luxury Brands* (revised ed.). Oxford University Press.

Programme records cited by version, as the locked pre-registration names them (OSF `ec6wh`; github.com/thirdsystem-aias/aias): AIAS Methodology v1.6 (Presence), v1.8 (Consistency $\varphi$), v1.9 ($C^*$ scaling), v1.10 (Ranking, tag `v1.10-prereg-r2`), v1.11 (Sentiment, tag `v1.11-prereg-r1`), v1.12 (Coverage, tag `v1.12-prereg-r1`) and v1.14 (Ranking redesign, tag `v1.14-prereg-r2`); the AIAS 2.0 synthesis (tag `aias-2-0-paper-locked`); the $t_4$ wave, v0.42 (pre-registration r2); the omnibus registries v0.19--v0.23. HARMAN press release, Business Wire, September 23, 2025, <https://www.businesswire.com/news/home/20250923135384/en/HARMAN-Completes-Sound-United-Acquisition-to-Expand-Premium-Audio-Leadership>.

\clearpage

# Appendix A: per-brand results {-}

Brand units rated on G\*, by category: answers naming the brand ($m_b$), grounded answers ($g_b$), answers retrieving the brand's own domain ($o_b$), G\*, the mean number of distinct resolved domains per grounded answer ($d_b$) and the source mix (shares of brand-owned, reference, review/editorial, retailer, news, forum/UGC and other domains). A dagger marks a house or portal domain (§2.3).

\begingroup\small\setstretch{1.0}

{{TABLE_BRANDS}}

\endgroup

{{NOTRATED_SENTENCE}}

# Appendix B: sensitivity details {-}

Table: Leave one category out (S8): $\rho_w$ of G\* with P and $C^*$ in each condition, and rel3, with the category named left out.

{{TABLE_S8}}

Table: Citations against sources per provider (MQ8; reported only).

{{TABLE_MQ8}}
