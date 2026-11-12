---
title: "AI Availability Scores and Later Change in Brand Search Interest"
subtitle: "A Pre-Registered Test of Predictive Validity on Past Data, June to November 2026 (AIAS™ v0.43, Stage 1)"
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

{\LARGE \textbf{AI Availability Scores and Later Change\\ in Brand Search Interest}}\\[8pt]

{\large A Pre-Registered Test of Predictive Validity on Past Data,\\ June to November 2026 (AIAS™ v0.43, Stage 1)}\\[28pt]

Pablo Ulpiano González Castro\\[4pt]
School of Visual Arts, MPS Branding Program, New York, NY \textit{(primary academic affiliation)}\\
Third System™ (research entity; data archive and methodology venue)\\[8pt]
Correspondence: pablou@pablou.com · pablou.com\\
ORCID: \href{https://orcid.org/0009-0003-8968-9990}{0009-0003-8968-9990}\\[20pt]

Pre-registration: \texttt{ {{PREREG_TAG}} } (commit \texttt{ {{PREREG_COMMIT}} }; deposited on OSF before any search-interest request)\\
Data and code: OSF \texttt{ec6wh}, \texttt{v43}\\

\end{center}
\end{titlepage}

# Abstract {-}

The AIAS programme measures how available brands are in the answers of large language models. Its Presence score has convergent and discriminant evidence but no predictive evidence. This pre-registered study asks whether the Presence and Consistency scores of 112 brands in five categories, collected on six models in June 2026, say anything about how each brand's US Google search interest changed between May--June and October--November 2026, among brands of the same category and the same June search level. The search data were requested only after the pre-registration was locked, in three pulls of {{MCW_REQ_PER_PULL}} size-matched requests each; {{Y_DEF_TOTAL}} of {{UNITS_TOTAL}} brands had a defined change. The statistic is a pooled within-category partial Spearman correlation with permutation $p$-values and bootstrap intervals.
{% switch CASE_PRES %}
{% case CONFIRMED %}
Brands with higher June Presence gained more search interest than comparable brands ($\rho = {{PRES_RHO}}$, one-sided $p = {{PRES_P1}}$, $n = {{PRES_N}}$), and the primary hypothesis is CONFIRMED.
{% case MARGINAL %}
The association between June Presence and the later change was positive but did not meet the confirmation rule ($\rho = {{PRES_RHO}}$, one-sided $p = {{PRES_P1}}$, $n = {{PRES_N}}$); the primary hypothesis is MARGINAL.
{% case FALSIFIED %}
The data exclude a partial correlation of 0.10 between June Presence and the later change ($\rho = {{PRES_RHO}}$, 90% interval {{PRES_CI90_LO}} to {{PRES_CI90_HI}}, $n = {{PRES_N}}$), and the primary hypothesis is FALSIFIED{% if PRES_REVERSED %}; the association is negative and significant (two-sided $p = {{PRES_P2}}$), so the test also carries the label REVERSED, support for the account in which AI availability lags demand{% endif %}.
{% case UNDETERMINED %}
The association between June Presence and the later change ($\rho = {{PRES_RHO}}$, 90% interval {{PRES_CI90_LO}} to {{PRES_CI90_HI}}, $n = {{PRES_N}}$) neither met the confirmation rule nor excluded 0.10, and the primary hypothesis is UNDETERMINED{% if PRES_REVERSED %}; the association is negative and significant (two-sided $p = {{PRES_P2}}$), so the test carries the label REVERSED{% endif %}.
{% case UNDETERMINED_N %}
Only {{PRES_N}} brands had a defined change, fewer than the pre-registered minimum of {{PRES_MINN}}, and the primary hypothesis is UNDETERMINED.
{% case UNDETERMINED_RHO %}
The primary statistic was undefined on the data, and the primary hypothesis is UNDETERMINED.
{% endswitch %}
The three secondary tests returned {{SA_WORD}} (seasonally adjusted change), {{MOM_WORD}} (controlling the February--June trend) and {{CONS_WORD}} (Consistency at equal Presence).{% if ANY_FLAG %} Under the pre-registered checks every verdict carries the flag{{FLAG_PLURAL}} {{FLAG_LIST}}.{% endif %} Search interest is a trace of people looking for a brand, not of buying it, and this is a test on past data; the confirmatory test, on outcome weeks that had not happened when it was locked, is Stage 2 (March 2027).

**Keywords:** AI availability; brand availability; AIAS; pre-registration; Ehrenberg-Bass; predictive validity; Google Trends; search interest; large language models; partial correlation

**JEL codes:** M31; L86, L15, D83, M37

**Paper status:** Pre-registered validity study on existing scores and newly requested search data (tag `{{PREREG_TAG}}`, deposited on OSF before the first search-interest request); Stage 1 of two; {{DEV_STATUS}} Part of the AIAS measurement programme.

{{SYN_NOTE}}

# 1. Introduction

AI Availability --- the discoverability and representation of a brand in the outputs of large language models --- has been proposed as a third measurable layer of brand availability (González Castro, 2026a), beside the Mental and Physical Availability of the Ehrenberg-Bass tradition (Sharp, 2010), within the Tri-System framework (González Castro, 2026l). The AIAS programme now reports two scores side by side, Presence and Consistency, separable from each other and stable over five months on the legacy six-model panel (Methodology v1.9: González Castro, 2026i; v0.41: González Castro, 2026p). The AIAS programme builds its components one at a time, each pre-registered and locked before it is used, on the Presence measurement protocol (González Castro, 2026b, 2026c, 2026d, 2026e, 2026f), anchored across five categories in AIAS 1.0 (González Castro, 2026j); the first Consistency instrument failed its separability test (v1.7: González Castro, 2026g) and was replaced by the dispersion statistic of v1.8 (González Castro, 2026h); the AIAS 2.0 synthesis (González Castro, 2026k) reports the two scores together. Presence has convergent evidence (same-week search interest, $\rho = 0.74$, $n = 24$, the v0.25 leg of the v0.29 baseline: González Castro, 2026m, 2026o), discriminant evidence (Amazon sales rank, v0.26: González Castro, 2026n) and a baseline that binds them (v0.29: González Castro, 2026o), which left predictive validity open for want of a longitudinal criterion. Presence has no predictive evidence: no study has yet asked whether a brand's AI availability says anything about where its demand goes next.

Two accounts predict opposite answers (pre-registration §1).

1. **AI availability leads.** If AI answers are a third route by which brands come to mind and to hand, a brand that AI assistants name more than its current search level would suggest should gain search interest relative to comparable brands.
2. **AI availability lags.** If model answers mostly echo training data and web text that trail the market, AI presence beyond a brand's current search level marks a brand whose popularity peaked earlier, and search momentum carries it further down, while rising brands are under-named. This predicts the opposite sign.

The tests are directional (account 1); a result of the opposite sign is reported as support for account 2. The criterion is Google search interest: the programme's established external signal, available weekly for any brand in the US, and a behavioural trace of people looking for a brand. It is not sales. Sales rank is not collected in this study (Section 2.4).

This paper reports Stage 1, which uses past data: the Presence and Consistency scores of June 2026 and the search interest of June to November 2026. It could run as soon as the study was locked because both the June scores and the June-to-November search history already existed; it was pre-registered because those search data had not been looked at. Stage 2 repeats the test forward, from the scores of November 2026 to search interest in March 2027, and was locked at the same time, before any of its outcome weeks had happened. Stage 1 is retrospective evidence; Stage 2 is the confirmatory test.

# 2. Method

Section signs (§) refer to the pre-registration; sections of this paper are named as sections.

## 2.1 Brands and scores

The study uses the 112 brand units of the programme's five omnibus registries, unchanged: v0.19 audiophile headphones (16 units), v0.20 skincare, v0.21 cosmetics, v0.22 automotive and v0.23 premium spirits (24 each). Rare Beauty is a unit in both skincare and cosmetics and is requested within each category's bundles. Spirits brands keep their codes (S01--S24) in every output. Each registry is an analysis stratum.

The predictors were locked and published before this study. The Presence score is $P = 100\,(C_P/6 + 2\hat\pi)/3$, the AIAS 2.0 Presence score as locked by Methodology v1.9 (González Castro, 2026i), with $C_P$ the number of the six legacy models that recognise the brand and $\hat\pi$ its recall rate. The Consistency score is $C^* = 100\,(1 - \varphi/7.2)$ for brands with at least six mentions in the wave, not rated otherwise (v1.9's locked rule; $\varphi$ from Methodology v1.8: González Castro, 2026h). Stage 1 uses the scores of the second wave ($t_2$), collected by 10 June 2026; recall $\hat\pi$ is as locked by v0.41 (González Castro, 2026p). A parity check before the lock confirmed that the study's units file reproduces the frozen sources exactly (pre-registration §3.1).

## 2.2 Outcome, level and windows

A week is a Google Trends week, Sunday to Saturday; $W(e)$ is the four complete weeks ending on Saturday $e$, and $S_b(W)$ the sum of brand $b$'s four weekly index values in $W$ within one request. The outcome is the change $Y_b = \ln[(S_b(W_{\text{end}}) + 1) / (S_b(W_{\text{base}}) + 1)]$, computed inside one request so that it does not depend on the request's scale. The control $L_b$ is the brand's search level over $W_{\text{base}}$ on its category's chained scale, as a within-category rank averaged over pulls. Momentum is $M_b = \ln[(S_b(W_{\text{base}}) + 1)/(S_b(W_{\text{prior}}) + 1)]$, and the seasonally adjusted change is $Y^{SA}_b = Y_b - Y'_b$, where $Y'_b$ is the same change over the same calendar weeks one year earlier.

Table: Stage 1 windows (pre-registration §2.1). $W_{\text{base}}$ ends on the last Saturday before the predictors' wave began; every category's first $t_2$ call was on 10 June 2026 (clarification C2).

| Window | Four weeks ending | Role |
|:----------------------|:---------------------|:------------------------------------------|
| $W_{\text{prior}}$ | Sat 7 February 2026 | momentum control |
| $W_{\text{base}}$ | Sat 6 June 2026 | level control; start of the change |
| $W_{\text{end}}$ | Sat 7 November 2026 | end of the change |
| one year earlier | Sat 7 June 2025 and Sat 8 November 2025 | seasonal adjustment |

A brand's change is defined in a pull if $S(W_{\text{base}}) + S(W_{\text{end}}) \geq 4$ in at least one of its bundles (for a brand in two bundles, the mean of the values that meet the condition), and $Y_b$ is the mean over the pulls in which it is defined; it is undefined if defined in fewer than two of the three pulls. $Y'$ and $M$ follow the same rule. There is no imputation: a brand without a defined outcome leaves the test and is counted per category (§5.5).

## 2.3 Search terms

For each of the 111 distinct search names, one Google Trends autocomplete look-up (SerpAPI) returned entity suggestions, never interest values. The term is the first suggestion, in returned order, whose normalised title begins with the normalised search name and whose type contains, at the start of a word, one of the category's words (company, brand, corporation, manufacturer, business, and category words such as audio, beauty, car or vodka); the term is then that suggestion's topic ID. If no suggestion qualifies, the term is the search name itself, as a plain search term. There is no manual correction (§3.2).

## 2.4 Requests, bundles and pulls

Every request was a SerpAPI `google_trends` time series for the United States, all categories, web search, with up to five terms. A sizing pull of 28 requests over 7 September 2025 to 6 June 2026 fixed each brand's size; no week after 6 June 2026 was requested before the bundles were fixed. Within each category, brands were then sorted by size, and each request held the previous request's last brand and the next four (16 brands, 4 requests; 24 brands, 6), so that every request compares brands of similar size and the requests chain through the shared brand. Three main pulls of the same 28 bundles over 4 May 2025 to 7 November 2026 followed, at least 24 hours apart (§4.3). A request that erred, returned no time line or failed the weekly-points check was re-sent up to twice the same day and otherwise recorded as missing for that pull (§4.4). Levels are chained within a pull and category through the shared brands: $f_1 = 1$ and $f_{j+1} = f_j T_j / T_{j+1}$, with $T$ the shared brand's sum over the full range in the two bundles; a link with a zero sum or a missing request fails, and the later bundles then form a new segment that ranks below every brand of the earlier ones (§5.2, clarification C4). Sales rank is not collected (§4.6). No model was called; the budget was 223 SerpAPI requests for Stage 1, within the provider's free plan.

## 2.5 Statistic

Every test uses the pooled within-category partial Spearman correlation $\rho_{\text{pw}\mid Z}$: within each category the outcome, the predictor and each control in $Z$ are ranked (average ranks), the ranks of the outcome and of the predictor are each regressed by ordinary least squares on an intercept and the control ranks, the residuals are pooled over categories, and $\rho_{\text{pw}\mid Z}$ is Pearson's $r$ of the pooled residuals. The one-sided permutation $p$ shuffles the predictor's residuals within category (10,000 draws; $p = (1 + \#\{\rho_{\text{perm}} \geq \rho_{\text{obs}}\})/10{,}001$); the two-sided $p$ (on $|\rho|$) is reported beside it. Bootstrap intervals resample brands with replacement within category and recompute ranks, residuals and $\rho$ on each of 10,000 resamples (percentile 90% and 95% intervals; a resample with undefined $\rho$ is dropped and counted). Seeds were fixed in advance: 430041 to 430044 for the four Stage 1 tests, 430049 for the checks and 430050 for the descriptives.

## 2.6 Hypotheses and verdict rule

Table: Stage 1 hypotheses (pre-registration §2.2 and §2.3). $X$: predictor at $t_2$; $Y$: change from $W$(6 June 2026) to $W$(7 November 2026); $Z$: controls.

| Test | Tier | $X$ | Outcome | $Z$ | Seed |
|:---------------------------|:----------|:------------|:-----------------------------|:------------|:-------|
| H_Pred_Presence (§2.2) | primary | $P$ | $Y$ | $L$ | 430041 |
| H_Pred_Presence_SA (§2.3) | secondary | $P$ | $Y^{SA}$ | $L$ | 430042 |
| H_Pred_Presence_Momentum (§2.3) | secondary | $P$ | $Y$ | $L$, $M$ | 430043 |
| H_Pred_Consistency (§2.3) | secondary | $C^*$ (rated) | $Y$ | $L$, $P$ | 430044 |

**H_Pred_Presence (§2.2, primary).** “Among brands of the same category and the same June search level, those with a higher AIAS Presence score in June 2026 gained more US search interest by November 2026.” The level control is there because Presence and current search level are correlated and brands with high search levels tend to fall back; without it, a negative association could be regression to the mean alone.

**H_Pred_Presence_SA (§2.3).** The same test with the seasonally adjusted change, on brands with both years defined: comparing a brand with its own previous year removes its own seasonal pattern, which within-category ranks remove only in part.

**H_Pred_Presence_Momentum (§2.3).** The same test with the February-to-June change as a second control: it asks whether Presence adds anything beyond the trend search had already shown, the pattern the lag account predicts.

**H_Pred_Consistency (§2.3).** “Among rated brands, those named more consistently across models gained more, at equal Presence and June search level.”

The verdict rule applies to every test (§2.1). CONFIRMED if $\rho_{\text{pw}\mid Z} \geq 0.15$ and $p < 0.05$; FALSIFIED if the upper end of the 90% bootstrap interval is below 0.10; MARGINAL if $\rho_{\text{pw}\mid Z} > 0$ and $p < 0.10$, and neither of the above; UNDETERMINED otherwise. A test with fewer than 60 brands with a defined outcome (30 for the Consistency test) is UNDETERMINED. A test whose $\rho$ is negative with two-sided $p < 0.05$ also carries the label REVERSED (support for the lag account); the label adds to the verdict and changes none. $\alpha$ is 0.05 per test with no multiplicity correction, and every test is reported. The pre-registration states why: “A brand's search level is mostly stable from month to month, so a score that predicts its change explains a small part of a small variance; partial correlations of 0.1 to 0.3 are what a useful leading indicator would show.” It also states the power: “With about 105 units in five strata a test has about 80% power for $\rho$ = 0.25 and about 40% for $\rho$ = 0.15: a true effect near 0.15 may well come out MARGINAL or UNDETERMINED”.

## 2.7 Checks and descriptives

Five checks were pre-registered (§2.7). `MC_Concurrent` asks for the same-time link of v0.25 (González Castro, 2026m) in these five categories: $\rho_{\text{pw}}(P, L) \geq 0.30$ with one-sided $p < 0.05$; if it fails, every verdict carries the flag "criterion doubtful". `MC_PullReliability` asks that the mean, over the three pairs of pulls, of the pooled within-category Spearman correlation of per-pull changes be at least 0.70; below it, verdicts carry the flag "outcome unreliable". `MC_Weekly` requires weekly points starting on Sundays that cover each request's range, with no partial point inside a window. `MC_Terms` reports the share of brands searched by topic; below 50% verdicts carry the flag "mostly plain search terms". `MC_Chain` reports the chain links that held in each pull.

The pre-registered descriptives carry no verdicts (§2.8): every test per category (single-stratum $\rho$ with a permutation $p$); the Presence tests without the five defunct automotive brands (Mercury, Oldsmobile, Plymouth, Pontiac, Saturn); recall $\hat\pi$ in place of $P$; brands searched by topic only; a longer lead, with $P$ at $t_1$ (May 2026); and an exploratory cross-lagged comparison of AI $\rightarrow$ search, $\rho_{\text{pw}}(P_{t_2}, L_{\text{end}} \mid L_{\text{base}})$, against search $\rightarrow$ AI, $\rho_{\text{pw}}(L_{\text{base}}, P_{t_3} \mid P_{t_2})$, with a bootstrap interval for their difference.

## 2.8 Pre-registration and deviations

The pre-registration (revision r1 with clarifications C1--C10, all logged before the lock and changing no hypothesis, threshold, window, term rule or decision rule) was locked at git tag `{{PREREG_TAG}}` (commit `{{PREREG_COMMIT}}`) on 11 November 2026 at 00:31 CT, 24 hours after it reached the pre-registrant, and deposited on OSF (`ec6wh`, `v43/prereg/`, `v43/registries/` and `v43/anchor/`) before any search-interest request; the anchor record names the tag's commit, and the acquisition script refused to run without the tag and the anchor. The scorer (`score_v0_43.py`) and the acquisition script were written and unit-tested on synthetic responses before the lock, and the scorer was run once on the three complete pulls. {{DEV_SENTENCE}}

# 3. Results

## 3.1 Collection and checks

{{PULLS_SENTENCE}} Of the {{MCW_REQ}} main requests, {{MCW_OK}} returned a valid weekly series; {{MCW_MISSING_SENTENCE}} (`MC_Weekly`). {{CHAIN_HELD}} of the {{CHAIN_TOTAL}} chain links held across the three pulls (`MC_Chain`; Appendix). {{TERMS_RESULT}}

{% if CONC_PASS %}Within category, June Presence and June search level correlated at $\rho_{\text{pw}} = {{CONC_RHO}}$ (one-sided $p = {{CONC_P}}$, $n = {{CONC_N}}$), so `MC_Concurrent` passed: in these five categories, as in v0.25 (González Castro, 2026m), brands that AI answers name more are also searched more at the same time.{% else %}Within category, June Presence and June search level correlated at $\rho_{\text{pw}} = {{CONC_RHO}}$ (one-sided $p = {{CONC_P}}$, $n = {{CONC_N}}$), short of the pre-registered 0.30 with $p < 0.05$, so `MC_Concurrent` failed and every verdict carries the flag "criterion doubtful".{% endif %} {% if REL_PASS %}The three pulls agreed on the change: the pooled within-category Spearman correlation of per-pull changes was {{REL_PAIRS}} for the three pairs of pulls, a mean of {{REL_MEAN}}, and `MC_PullReliability` passed.{% else %}The three pulls agreed less than required on the change: the pooled within-category Spearman correlation of per-pull changes was {{REL_PAIRS}} for the pairs of pulls (mean {{REL_MEAN}}, against a minimum of 0.70), so `MC_PullReliability` failed and every verdict carries the flag "outcome unreliable".{% endif %} Figure 1 shows both checks.

![Left: June Presence and June search level per brand, as ranks centred within category. Right: agreement of the per-pull change between pairs of pulls, against the pre-registered 0.70. {{FIG_CAPTION}}]({{FIG_DIR}}/chart_01_checks.pdf){#fig:checks width=100%}

{% if ANY_FLAG %}**Flags.** Under §2.7 every Stage 1 verdict below carries the flag{{FLAG_PLURAL}} {{FLAG_LIST}}. The verdicts are reported as the rule gives them; the flags say how far they can be read.{% else %}No check raised a flag, so the verdicts below carry none.{% endif %}

{{Y_DEF_TOTAL}} of the {{UNITS_TOTAL}} brands had a defined change (Table 3); the others leave every test that needs it. The Consistency test uses only brands with a rated $C^*$.

Table: Brands per category: units, brands with a defined change $Y$, and the number of brands entering each test.

{{TABLE_DEFINED}}

## 3.2 June Presence and the change to November (primary)

{% switch CASE_PRES %}
{% case CONFIRMED %}
Across {{PRES_N}} brands with a defined change, $\rho_{\text{pw}\mid L} = {{PRES_RHO}}$ (90% interval {{PRES_CI90_LO}} to {{PRES_CI90_HI}}; 95% interval {{PRES_CI95_LO}} to {{PRES_CI95_HI}}; one-sided $p = {{PRES_P1}}$). This meets $\rho \geq 0.15$ with $p < 0.05$, and H_Pred_Presence is **CONFIRMED**: among brands of the same category and the same June search level, those with higher June Presence gained more search interest by November.
{% case MARGINAL %}
Across {{PRES_N}} brands with a defined change, $\rho_{\text{pw}\mid L} = {{PRES_RHO}}$ (90% interval {{PRES_CI90_LO}} to {{PRES_CI90_HI}}; 95% interval {{PRES_CI95_LO}} to {{PRES_CI95_HI}}; one-sided $p = {{PRES_P1}}$). The association is positive with $p < 0.10$ but does not meet $\rho \geq 0.15$ with $p < 0.05$, and the data do not exclude 0.10, so H_Pred_Presence is **MARGINAL**.
{% case FALSIFIED %}
Across {{PRES_N}} brands with a defined change, $\rho_{\text{pw}\mid L} = {{PRES_RHO}}$ (90% interval {{PRES_CI90_LO}} to {{PRES_CI90_HI}}; 95% interval {{PRES_CI95_LO}} to {{PRES_CI95_HI}}; one-sided $p = {{PRES_P1}}$). The upper end of the 90% interval is below 0.10, and H_Pred_Presence is **FALSIFIED**: the data exclude even a small positive partial association between June Presence and the change to November.
{% case UNDETERMINED %}
Across {{PRES_N}} brands with a defined change, $\rho_{\text{pw}\mid L} = {{PRES_RHO}}$ (90% interval {{PRES_CI90_LO}} to {{PRES_CI90_HI}}; 95% interval {{PRES_CI95_LO}} to {{PRES_CI95_HI}}; one-sided $p = {{PRES_P1}}$). This neither meets the confirmation rule nor excludes 0.10, and H_Pred_Presence is **UNDETERMINED**: the data cannot tell a small positive association from none.
{% case UNDETERMINED_N %}
Only {{PRES_N}} brands had a defined change, fewer than the pre-registered minimum of {{PRES_MINN}}, and H_Pred_Presence is **UNDETERMINED**.{% if PRES_HAS_CI %} For the record, $\rho_{\text{pw}\mid L} = {{PRES_RHO}}$ (90% interval {{PRES_CI90_LO}} to {{PRES_CI90_HI}}; one-sided $p = {{PRES_P1}}$); under the rule it carries no verdict.{% endif %}
{% case UNDETERMINED_RHO %}
The statistic was undefined on the data ({{PRES_N}} brands), and H_Pred_Presence is **UNDETERMINED**.
{% endswitch %}
{% if PRES_REVERSED %}The correlation is negative with two-sided $p = {{PRES_P2}}$, below 0.05, so the test also carries the label **REVERSED**: under §1 of the pre-registration this is support for the account in which AI availability lags demand.{% endif %}
{% if ANY_FLAG %}The verdict carries the flag{{FLAG_PLURAL}} {{FLAG_LIST}} (Section 3.1).{% endif %} Figure 2 shows the brands and Figure 3 all four tests against the verdict thresholds.

![June Presence against the change in search interest to November, both as residual ranks after the June search level, pooled over the five categories (one point per brand with a defined change). {{FIG_CAPTION}}]({{FIG_DIR}}/chart_02_presence_change.pdf){#fig:primary width=92%}

![Partial rank correlation of each June score with the later change, with 90% and 95% bootstrap intervals, against the confirmation threshold (0.15) and the falsification bound (0.10). {{FIG_CAPTION}}]({{FIG_DIR}}/chart_03_tests_intervals.pdf){#fig:tests width=100%}

## 3.3 Secondary tests

**Seasonally adjusted change (H_Pred_Presence_SA).** {% switch CASE_SA %}{% case CONFIRMED %}Across {{SA_N}} brands with both years defined, $\rho_{\text{pw}\mid L} = {{SA_RHO}}$ (90% interval {{SA_CI90_LO}} to {{SA_CI90_HI}}; one-sided $p = {{SA_P1}}$), and the test is **CONFIRMED**: the association holds when each brand's change is compared with its own change a year earlier.{% case MARGINAL %}Across {{SA_N}} brands with both years defined, $\rho_{\text{pw}\mid L} = {{SA_RHO}}$ (90% interval {{SA_CI90_LO}} to {{SA_CI90_HI}}; one-sided $p = {{SA_P1}}$), and the test is **MARGINAL**.{% case FALSIFIED %}Across {{SA_N}} brands with both years defined, $\rho_{\text{pw}\mid L} = {{SA_RHO}}$ (90% interval {{SA_CI90_LO}} to {{SA_CI90_HI}}; one-sided $p = {{SA_P1}}$); the interval excludes 0.10, and the test is **FALSIFIED**.{% case UNDETERMINED %}Across {{SA_N}} brands with both years defined, $\rho_{\text{pw}\mid L} = {{SA_RHO}}$ (90% interval {{SA_CI90_LO}} to {{SA_CI90_HI}}; one-sided $p = {{SA_P1}}$), and the test is **UNDETERMINED**.{% case UNDETERMINED_N %}Only {{SA_N}} brands had both years defined, fewer than {{SA_MINN}}, and the test is **UNDETERMINED**.{% case UNDETERMINED_RHO %}The statistic was undefined on the data, and the test is **UNDETERMINED**.{% endswitch %}{% if SA_REVERSED %} It also carries the label **REVERSED** (two-sided $p = {{SA_P2}}$).{% endif %} Figure 4.

![June Presence against the year-on-year-adjusted change, both as residual ranks after the June search level. {{FIG_CAPTION}}]({{FIG_DIR}}/chart_04_presence_change_sa.pdf){#fig:sa width=92%}

**Momentum control (H_Pred_Presence_Momentum).** {% switch CASE_MOM %}{% case CONFIRMED %}Controlling both the June level and the February-to-June change, $\rho_{\text{pw}\mid L,M} = {{MOM_RHO}}$ across {{MOM_N}} brands (90% interval {{MOM_CI90_LO}} to {{MOM_CI90_HI}}; one-sided $p = {{MOM_P1}}$), and the test is **CONFIRMED**: Presence adds to the trend search had already shown.{% case MARGINAL %}Controlling both the June level and the February-to-June change, $\rho_{\text{pw}\mid L,M} = {{MOM_RHO}}$ across {{MOM_N}} brands (90% interval {{MOM_CI90_LO}} to {{MOM_CI90_HI}}; one-sided $p = {{MOM_P1}}$), and the test is **MARGINAL**.{% case FALSIFIED %}Controlling both the June level and the February-to-June change, $\rho_{\text{pw}\mid L,M} = {{MOM_RHO}}$ across {{MOM_N}} brands (90% interval {{MOM_CI90_LO}} to {{MOM_CI90_HI}}; one-sided $p = {{MOM_P1}}$); the interval excludes 0.10, and the test is **FALSIFIED**.{% case UNDETERMINED %}Controlling both the June level and the February-to-June change, $\rho_{\text{pw}\mid L,M} = {{MOM_RHO}}$ across {{MOM_N}} brands (90% interval {{MOM_CI90_LO}} to {{MOM_CI90_HI}}; one-sided $p = {{MOM_P1}}$), and the test is **UNDETERMINED**.{% case UNDETERMINED_N %}Only {{MOM_N}} brands had both changes defined, fewer than {{MOM_MINN}}, and the test is **UNDETERMINED**.{% case UNDETERMINED_RHO %}The statistic was undefined on the data, and the test is **UNDETERMINED**.{% endswitch %}{% if MOM_REVERSED %} It also carries the label **REVERSED** (two-sided $p = {{MOM_P2}}$).{% endif %} Figure 5.

![June Presence against the change to November, both as residual ranks after the June level and the February-to-June change. {{FIG_CAPTION}}]({{FIG_DIR}}/chart_05_presence_change_momentum.pdf){#fig:mom width=92%}

**Consistency (H_Pred_Consistency).** {% switch CASE_CONS %}{% case CONFIRMED %}Among {{CONS_N}} brands with a rated $C^*$, controlling the June level and Presence, $\rho_{\text{pw}\mid L,P} = {{CONS_RHO}}$ (90% interval {{CONS_CI90_LO}} to {{CONS_CI90_HI}}; one-sided $p = {{CONS_P1}}$), and the test is **CONFIRMED**: Consistency carries information about the later change that Presence does not.{% case MARGINAL %}Among {{CONS_N}} brands with a rated $C^*$, controlling the June level and Presence, $\rho_{\text{pw}\mid L,P} = {{CONS_RHO}}$ (90% interval {{CONS_CI90_LO}} to {{CONS_CI90_HI}}; one-sided $p = {{CONS_P1}}$), and the test is **MARGINAL**.{% case FALSIFIED %}Among {{CONS_N}} brands with a rated $C^*$, controlling the June level and Presence, $\rho_{\text{pw}\mid L,P} = {{CONS_RHO}}$ (90% interval {{CONS_CI90_LO}} to {{CONS_CI90_HI}}; one-sided $p = {{CONS_P1}}$); the interval excludes 0.10, and the test is **FALSIFIED**.{% case UNDETERMINED %}Among {{CONS_N}} brands with a rated $C^*$, controlling the June level and Presence, $\rho_{\text{pw}\mid L,P} = {{CONS_RHO}}$ (90% interval {{CONS_CI90_LO}} to {{CONS_CI90_HI}}; one-sided $p = {{CONS_P1}}$), and the test is **UNDETERMINED**.{% case UNDETERMINED_N %}Only {{CONS_N}} rated brands had a defined change, fewer than {{CONS_MINN}}, and the test is **UNDETERMINED**.{% case UNDETERMINED_RHO %}The statistic was undefined on the data, and the test is **UNDETERMINED**.{% endswitch %}{% if CONS_REVERSED %} It also carries the label **REVERSED** (two-sided $p = {{CONS_P2}}$).{% endif %} Figure 6.

![June Consistency $C^*$ against the change to November, both as residual ranks after the June level and June Presence (brands with a rated $C^*$). {{FIG_CAPTION}}]({{FIG_DIR}}/chart_06_consistency_change.pdf){#fig:cons width=92%}

Table: The four Stage 1 tests: brands, $\rho_{\text{pw}\mid Z}$, bootstrap intervals, one- and two-sided permutation $p$ and the scorer's verdict and label.

{{TABLE_TESTS}}

{{BOOT_SENTENCE}}

## 3.4 Descriptives (no verdicts)

Table 5 and Figure 7 give every test per category; with 16 to 24 brands per category these single-stratum correlations are noisy and carry no verdict. Table 6 and Figure 8 give the other pre-registered descriptives.

Table: Every test per category (pre-registration §2.8, item 1): single-stratum $\rho$ with $n$ and one-sided permutation $p$ in brackets.

{{TABLE_PERSUB}}

![Single-category partial rank correlations of each test, with the number of brands. {{FIG_CAPTION}}]({{FIG_DIR}}/chart_07_per_category.pdf){#fig:persub width=100%}

Table: Pre-registered descriptives 2 to 5 (§2.8): $\rho_{\text{pw}\mid Z}$, 90% bootstrap interval and one-sided permutation $p$.

{{TABLE_DESC}}

{% if XL_HAS %}**Cross-lagged comparison (exploratory).** Across {{XL_N}} brands, June Presence correlated with November search level at equal June level at $\rho = {{XL_A}}$ (AI $\rightarrow$ search), and June search level with November Presence at equal June Presence at $\rho = {{XL_B}}$ (search $\rightarrow$ AI); the difference was {{XL_DIFF}} (90% interval {{XL_CI90_LO}} to {{XL_CI90_HI}}; 95% interval {{XL_CI95_LO}} to {{XL_CI95_HI}}). The comparison is only suggestive (pre-registration §6, limitation 5).{% else %}The cross-lagged comparison could not be computed on these data.{% endif %}

![Descriptive variants of the Presence test and the cross-lagged comparison: partial rank correlations with 90% bootstrap intervals. {{FIG_CAPTION}}]({{FIG_DIR}}/chart_08_descriptives.pdf){#fig:desc width=100%}

# 4. Discussion

{% switch CASE_PRES %}
{% case CONFIRMED %}
On past data, June AI availability predicted the direction of the next five months of search interest beyond what search itself showed in June: among brands of the same category and search level, those the six models named more gained more search interest. This fits the account in which AI availability leads demand. It is retrospective evidence and a correlation; a common cause, such as advertising or a launch that reaches both the web and search, could produce it, and the cross-lagged comparison is only suggestive. The claim that Presence has predictive validity rests on Stage 2, the same test forward on outcome weeks that had not happened when it was locked.
{% case MARGINAL %}
On past data the association between June AI availability and the later change in search interest pointed in the predicted direction but was too small, or too uncertain, to meet the pre-registered rule. The pre-registration anticipated this outcome: with about 105 brands a true partial correlation near 0.15 has about 40% power. The result neither supports nor rejects a leading role for AI availability; Stage 2 repeats the test forward.
{% case FALSIFIED %}
{% if PRES_REVERSED %}
On past data, AI availability did not lead demand: brands that the six models named more than their June search level would suggest lost search interest relative to comparable brands. Under the pre-registration this is support for the account in which model answers echo a market that has already moved, so AI presence beyond search marks brands past their peak. It is a correlation on past data, and Stage 2 tests it forward.
{% else %}
On past data, June AI availability carried no useful information about the next five months of search interest beyond June search level: the data exclude even a small positive partial association, and the negative direction that would support the lag account was not significant. For the programme, Presence is a measure of current availability, with convergent and discriminant evidence, and not, on this evidence, a leading indicator of search demand. Stage 2 repeats the test forward.
{% endif %}
{% case UNDETERMINED %}
On past data the test could not tell a small association between June AI availability and the later change in search interest from none. The pre-registration anticipated this outcome: partial correlations of 0.1 to 0.3 are what a useful leading indicator would show, and with about 105 brands such effects may come out UNDETERMINED. The question stays open for Stage 2, which repeats the test forward.
{% case UNDETERMINED_N|UNDETERMINED_RHO %}
The primary test could not be decided on these data, for the cause given in Section 3.2, and the question stays open. Stage 2 repeats the test forward on the same bundles.
{% endswitch %}

{% if ANY_FLAG %}The verdicts carry the flag{{FLAG_PLURAL}} {{FLAG_LIST}}: {{FLAG_MEANING}} {% endif %}The secondary tests returned {{SA_WORD}} for the seasonally adjusted change, {{MOM_WORD}} with the momentum control and {{CONS_WORD}} for Consistency at equal Presence; under the pre-registration none of them changes the primary verdict.

# 5. Limitations

Search interest is a trace of people looking for a brand, not of buying it; it comes from one search engine in one country. Google Trends values are sampled and rounded; size-matched bundles and three pulls reduce that noise and do not remove it. The term rule is mechanical: some names fall back to plain terms that also catch other meanings, and a topic can be the wrong entity of the same name; descriptive 4 shows the topic-only result, and the full look-up record is published. Brand-level search mixes categories for brands that sell in many, while Presence is measured in one category. The design is correlational: a positive partial association fits AI availability leading demand, but a common cause could produce it. Stage 1's scores come from the retiring legacy six-model panel. There are five categories of 16 to 24 brands, so the strata are small. This is a test on past data: the scores and the search history both existed before the study was locked, although the search data had not been looked at. Sales are not measured.

# 6. Stage 2

Stage 2 is locked in the same pre-registration (§2.4, §2.5 and §4.5). Its predictors are the Presence and Consistency scores of November 2026 on the legacy panel ($t_3$) and Presence on the newest models ($t_4$); its outcome is the change from the four weeks ending 7 November 2026 to the four weeks ending 6 March 2027, from three pulls of the same bundles, the first no earlier than 10 March 2027, with the same statistic and verdict rule. Between the stages, one pull of the 28 bundles is stored on the first day of each month and not analysed for Stage 2. The four newer components (Ranking, Sentiment, Coverage and Grounding) can join Stage 2 only by dated amendments deposited before its first outcome pull, and sales rank only by a dated amendment with its own hypotheses (§2.6, §4.6). A predictive-validity claim for Presence rests on Stage 2.

# Declarations {-}

## Conflict of interest {-}

The author is Director, Corporate Brand Creative and Governance at Samsung Electronics America. This study measures search interest for the brands of registries fixed in earlier phases (v0.19--v0.23); it performs no new brand selection, and each registry carries its source-phase conflict-of-interest handling forward unchanged. Two items of record apply. In the automotive registry, Samsung subsidiaries hold tier-2/3 component supply relationships with several registry brands --- Harman International (audio systems), Samsung SDI (battery cells), and Samsung Display (infotainment) --- characterized in the source phase as non-competitive, with no brand-level overlap, and imposing no operational restriction on registry composition (v0.22 Declarations; screened in v0.22 DEVIATIONS Entry 0, Part B). In the audiophile-headphones registry, AKG was substituted with Denon before the v0.19 pre-registration lock because AKG's parent, Harman International, is a Samsung subsidiary. Correction (November 10, 2026): Denon, which replaced AKG in the v0.19 registry, has itself been owned by Harman International, a wholly owned subsidiary of Samsung Electronics, since September 23, 2025, when Harman completed its acquisition of Sound United from Masimo; the v0.19 headphones registry therefore includes one Samsung-group brand. The substitution did not achieve its purpose, and this was not noticed until November 10, 2026.{% if COI_CHEIL %} Cheil Worldwide, a Samsung affiliate, or its Iris unit has worked for five brands of these registries: Chevrolet (GM Korea advertising, 2017), BMW (BMW Group UK consumer PR, 2018), Bentley (Americas experiential, 2021), Jack Daniel's (UK digital, 2022) and Eucerin (Beiersdorf search marketing, 2024), as recorded in v0.62 DEVIATIONS Entry 0, Part F; they stay in the registries and the analysis as locked.{% endif %} Data collection and scoring are fully automated against the locked registries, and the pre-registration was locked and deposited before any search-interest request. Samsung Electronics had no role in the design, conduct, analysis or reporting of this work.

## Funding {-}

Self-funded.

## Ethics {-}

Not applicable; no human subjects.

## Use of AI tools {-}

During the preparation of this work the author used AI tools (Anthropic's Claude) to assist with study design, analysis and writing. The author reviewed and edited all content and takes full responsibility for it.

## Data and code availability {-}

The locked pre-registration, the frozen inputs, the units file, the acquisition and scoring scripts with their tests, the lock manifest and the anchor record are deposited at OSF (osf.io/ec6wh), `v43/prereg/`, `v43/registries/` and `v43/anchor/`. At publication the deposit adds the term look-ups and bundles, the raw search-interest responses of the sizing and main pulls (`data/trends_raw/`), the verdict file (`v43_stage1_verdicts.json`) and the figure sources. The code is also in the programme's GitHub repository (github.com/thirdsystem-aias/aias) at tag `{{PREREG_TAG}}`.

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

González Castro, P. U. (2026m). *Predictive Validity of AI Presence Index Against Google Trends Search Interest on the B2B SaaS Substrate: Construct Validity Pilot Under Protocol v1.6* (v0.25). Third System, <https://thirdsystem.ai/studies/v0-25/> (PDF: <https://thirdsystem.ai/files/papers/v0_25_b2b_saas_construct_validity.pdf>).

González Castro, P. U. (2026n). *What AI Presence Does Not Predict: Amazon Best Sellers Rank as Discriminant Validity Evidence for the AIAS Construct* (v0.26). SSRN 6847678.

González Castro, P. U. (2026o). *The Presence Component Is Construct-Valid: A Convergent--Discriminant (Campbell--Fiske) Baseline for AI Availability* (v0.29). SSRN 6870778.

González Castro, P. U. (2026p). *Five-Month Stability of AI Brand Consistency and Presence: A Pre-Registered Third Wave on a Retiring Six-Model Panel* (AIAS™ v0.41). Third System, <https://thirdsystem.ai/studies/v0-41/> (PDF: <https://thirdsystem.ai/files/papers/v0_41_ssrn_paper.pdf>); OSF `ec6wh/v41`.

Sharp, B. (2010). *How Brands Grow: What Marketers Don't Know*. Oxford University Press.

Programme records cited by version, as the locked pre-registration names them (OSF `ec6wh`; github.com/thirdsystem-aias/aias): the omnibus registries of v0.19 (audiophile headphones, SSRN 6809182), v0.20 (skincare, SSRN 6811441), v0.21 (cosmetics, SSRN 6815378), v0.22 (automotive, SSRN 6829118) and v0.23 (premium spirits, SSRN 6834298){% if COI_CHEIL %}; v0.62{% endif %}.

\clearpage

# Appendix: collection records {-}

Table: Chain links held per pull and category (`MC_Chain`; held of links).

{{TABLE_CHAIN}}

Table: Requests per pull, from the stored records: time of the first and last request (UTC), valid and missing requests, re-sends.

{{TABLE_PULLS}}
