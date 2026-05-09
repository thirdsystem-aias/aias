---
documentclass: article
fontsize: 11pt
mainfont: Carlito
geometry: margin=1in
linkcolor: black
urlcolor: black
header-includes:
  - \usepackage{graphicx}
  - \usepackage{setspace}
  - \setstretch{1.36}
  - \setlength{\parskip}{8pt}
  - \setlength{\parindent}{0pt}
  - \usepackage{float}
  - \floatplacement{figure}{H}
  - \usepackage{caption}
  - \captionsetup{labelfont={bf,it},textfont=it,labelsep=period,justification=raggedright,singlelinecheck=false}
  - \usepackage{titlesec}
  - \titleformat{\section}{\normalfont\bfseries\large}{\thesection}{1em}{}
  - \titleformat{\subsection}{\normalfont\bfseries}{\thesubsection}{1em}{}
  - \usepackage{booktabs}
  - \usepackage{array}
---

\begin{center}
{\fontsize{16}{21.76}\selectfont\bfseries Naive-Phantom Rate Longitudinal Stability\par}
\vspace{0.4em}
{\itshape A Designed-for-Test Extension of the v0.7 Phantom-Brand Classifier to Mint, t\textsubscript{1} → t\textsubscript{2}\par}
\vspace{0.6em}
{Working Paper · Version 1 · Designed-for-Test (Personal Finance)\par}
\vspace{2em}
{\bfseries Pablo Ulpiano González Castro\par}
{\itshape School of Visual Arts, MPS Branding Program, New York, NY\par}
{\itshape (primary academic affiliation)\par}
{\itshape Third System\textsuperscript{TM} (research entity; data archive and methodology venue)\par}
{Correspondence: pablou@pablou.com · pablou.com\par}
{ORCID: \href{https://orcid.org/0009-0003-8968-9990}{0009-0003-8968-9990}\par}
\vspace{1.2em}
{9 May 2026\par}
\end{center}

\newpage

## Abstract

The AIAS measurement program's v0.7 (Phantom-Brand BBB) study introduced a designed-for-test reframe distinguishing naive-phantom presence (recommendation as live, no caveat) from caveated-phantom presence (recommendation acknowledging decommissioning). v0.7 BBB recorded a naive-phantom rate of 1.7% for Mint at the v0.6 baseline against a gross Presence rate of 38.2%. v0.9 (Longitudinal Re-Baseline) subsequently confirmed gross Presence stability for Mint (44.8% → 41.7% across t~1~→t~2~, |Δ|=3.1pp) but did not test whether the naive-phantom subset exhibits comparable stability. v0.10 applies the v0.7 caveat-classifier to the v0.9 raw response set, restricted to Mint within the matched two-model subset (Sonnet 4.6, gpt-5.4-mini), and tests three pre-registered hypotheses: H1 stability (±2pp band), H2 persistence (r~naive~ > 0 at both waves), and H3 co-movement diagnostic. An effective-n floor of 100 per wave was pre-specified for H1; matched-subset n at t~1~ and t~2~ was 43 and 40 respectively, breaching the floor and routing H1 to descriptive disclosure. $r_{\text{naive},t_1}$ = 0.00% (n~naive~ = 0/43); $r_{\text{naive},t_2}$ = 2.50% (n~naive~ = 1/40). H1 is **INDETERMINATE** (underpowered). H2 is **FALSIFIED** (n~naive~ = 0 at t~1~). H3 reports **DECOUPLED** directional movement (Δgross = −3.12pp; Δnaive = +2.50pp). The single t~2~ naive case — a Sonnet 4.6 response listing Mint at the top of "Free Options" with present-tense feature description and explicit recommendation as "the most common starting point for beginners" — constitutes existence proof that classifier-detectable naive-phantom presence is not yet fully extinguished from frontier-model substrates as of the May 2026 measurement window.

**Keywords:** AI-mediated commerce; phantom brands; longitudinal measurement; pre-registration; LLM evaluation; brand presence; Ehrenberg-Bass.

**JEL Classification:** M30 (Marketing — General); M37 (Advertising); C82 (Methodology for Collecting, Estimating, and Organizing Macroeconomic Data).

**Paper status.** Pre-registered. Pre-registration document locked at git commit `8767f44`, tag `v0.10-prereg`, on 2026-05-09, prior to any application of the classifier to the v0.9 Mint response subset. No analysis output existed at the moment of lock. Pre-registration document, inherited classifier configuration, all raw responses, classifier outputs, scoring outputs, adjudication log, and four deviations from pre-reg description are deposited at OSF project ec6wh, `/v10/`.

\newpage

## 1. Introduction

The AIAS Presence Measurement Protocol (v1.1) measures the rate at which AI systems surface specific brands in category-relevant decision contexts. The foundational paper (SSRN 6659000) introduces AI Availability as a theoretical layer above Mental and Physical Availability; the protocol document (SSRN 6722319) specifies the measurement methodology. The program's v0.7 study (Phantom-Brand BBB; SSRN 6721779) introduced a designed-for-test reframe distinguishing two qualitatively different phantom-brand presence types:

- **Naive-phantom presence.** The brand is recommended or described as if currently available — no caveat about decommissioning, sunset, or discontinuation appears anywhere in the response.
- **Caveated-phantom presence.** The brand is mentioned but accompanied by explicit acknowledgment of decommissioning or successor-product migration.

The two are mechanistically distinct. *Gross Presence* — the rate at which a brand is mentioned at all in category-relevant responses — indexes whether the retrieval system surfaces the brand. *Naive-phantom rate* indexes the subset of those surfacings delivered without classifier-detectable correction. The distinction matters because the two failure modes have different consequences for an AI-mediated consumer: gross presence as a defunct brand surfaces the brand to attention; naive presence delivers the brand as an actionable recommendation.

At the v0.7 BBB measurement window (4 May 2026), the naive-phantom rate for Mint, the personal-finance application that Intuit decommissioned in March 2024, was 1.7% against a gross Presence rate of 38.2%. The v0.7 result established the existence of the naive-phantom phenomenon at a measurable rate above zero in a frontier-model substrate two years post-decommissioning.

The v0.9 Longitudinal Re-Baseline study (SSRN 6736878) subsequently re-measured five categories at a second time point approximately seven days after the v0.6 cross-category baseline, on the same matched two-model subset (Anthropic Claude Sonnet 4.6 and OpenAI gpt-5.4-mini). H4 of v0.9 tested gross Presence stability for Mint specifically and confirmed stability within the pre-registered ±5pp band: 44.8% (t~1~, v0.6 baseline) → 41.7% (t~2~, v0.9 re-baseline), |Δ| = 3.1pp.

What v0.9 H4 did not test is whether the naive-phantom *subset* exhibits comparable stability — that is, whether AI systems' tendency to recommend Mint as if fully live persists at the same rate over the longitudinal interval, separately from the gross-mention rate. The substantive question matters for the program's theoretical framing. v0.7 framed the phantom mechanism in terms of two distinguishable failure modes — bare retrieval and recommendation-as-live. v0.9 demonstrated that gross retrieval is durable. The remaining question is whether the more consequential subset — recommendation slots delivered without caveat — is also durable, or whether classifier-detectable correction is propagating through the model substrate over the longitudinal window.

v0.10 tests this question. The study is a single-brand, designed-for-test extension. No new measurement is required; the v0.7 caveat-classifier is applied to the Mint-restricted subset of v0.9's deposited raw responses across the matched two-model subset.

## 2. Method

### 2.1 Hypotheses

Three hypotheses were pre-registered.

**H1 (Stability, primary, confirmatory).** The naive-phantom rate for Mint is stable t~1~→t~2~ within a ±2pp band. Confirmed if |$r_{\text{naive},t_2}$ − $r_{\text{naive},t_1}$| ≤ 2.0 pp; falsified if |Δr~naive~| > 2.0 pp.

**H2 (Persistence, secondary, confirmatory).** The naive-phantom rate is non-zero at both waves. Confirmed if $r_{\text{naive},t_1}$ > 0 AND $r_{\text{naive},t_2}$ > 0; falsified if r~naive~ = 0 at either wave.

**H3 (Co-movement, exploratory).** The directional change in naive-phantom rate is consistent with the directional change in gross Presence rate as reported in v0.9. Diagnostic only; no falsification status.

### 2.2 Effective-n floor

A floor of n ≥ 100 matched-subset Mint mentions per wave was pre-specified for H1. The floor is justified by the test's resolution against single-flip sampling noise: a single-response classification change moves r~naive~ by 1.0 pp at n = 100, which equals half the ±2pp stability band. If effective n falls below 100 at either wave, H1 is declared underpowered and routed to descriptive disclosure rather than relaxed.

### 2.3 Threshold justification

The ±2pp band for H1 is tighter than v0.9 H4's ±5pp band for gross Presence. Three considerations support the tighter band: proportional sensitivity to the small base rate (the v0.7 BBB naive rate of 1.7% would tolerate a 100% relative shift under a 5pp band, semantically inadequate for a stability test); symmetry preservation around a small base rate; and a deliberate preference for a tighter test where the substantive theory (recommendation-slot persistence) implies that meaningful drift should be detectable rather than absorbed into a wide band.

### 2.4 Data and subset

Source data: v0.9 raw responses, deposited at OSF project ec6wh, `/v09/data/responses/`, under git tag `v0.9-published`. No new prompting, no new model calls, no new wave windows. Brand: Mint only. Models: claude-sonnet-4-6 + gpt-5.4-mini, identical to the v0.9 H4 matched subset; other models present in the v0.9 deposit excluded. Waves: t~1~ (v0.6 baseline) and t~2~ (v0.9 re-baseline) as defined in v0.9 pre-registration. Brand registry `brands_pmtools_v0.6` frozen.

Mint-bearing rows were identified via exact-token match against the `brands_canonical` pipe-delimited field in v0.9's enriched results. The match yielded 43 rows at t~1~ and 40 rows at t~2~, against 96 matched-subset rows per wave — gross Presence rates of 44.79% and 41.67%, respectively, matching v0.9's published 44.8% and 41.7% to within rounding.

### 2.5 Classifier

Per pre-reg §5, the classifier inherits the v0.7 configuration unchanged. (The pre-registration described the classifier as "a keyword/phrase rule list and judge-LLM verification protocol"; inspection of v0.7's actual implementation revealed an LLM-only classifier with no rule list and no separate judge — see Deviations 1 and 2 in §Declarations.) The inherited configuration is a single call to gpt-5.4-mini at temperature 0, structured with a system prompt specifying the classification task and a function-calling tool schema constraining the output to three fields: `valence` (5-class), `entity_reference` (4-class), and `source_quote`.

The 5-class valence set — `live_recommendation`, `live_with_caveat`, `status_correction`, `historical_reference`, `ambiguous` — is brand-agnostic and inherited unchanged. The `entity_reference` 4-class set was parameterized for Mint→Credit Karma in place of v0.7's BBB→Beyond, Inc. parameterization; both sets are brand-specific by design and v0.7 already established the parameterization pattern. The system prompt was parameterized analogously, replacing v0.7's BBB framing with Mint framing. The full classifier configuration is reproduced verbatim in `/v10/registries/v07_caveat_classifier.json`.

### 2.6 Mapping from v0.7 5-class valence to v0.10 binary

v0.7's 5-class valence is mapped to v0.10's 2-class binary at first classification and locked thereafter. Table 1 specifies the mapping under both the primary analysis and the E3 sensitivity analysis.

\begin{table}[H]
\centering
\begin{tabular}{lll}
\toprule
\textbf{v0.7 valence} & \textbf{v0.10 binary (primary)} & \textbf{v0.10 binary (E3 sensitivity)} \\
\midrule
\texttt{live\_recommendation}    & naive    & naive    \\
\texttt{live\_with\_caveat}      & caveated & caveated \\
\texttt{status\_correction}      & caveated & caveated \\
\texttt{historical\_reference}   & caveated & caveated \\
\texttt{ambiguous}               & naive    & caveated \\
\bottomrule
\end{tabular}
\caption{v0.7 5-class valence to v0.10 2-class binary mapping. The mapping is consistent with pre-reg §5's verbal description of the binary criterion: caveated requires explicit acknowledgment of decommissioning, shutdown, sunset, discontinuation, end-of-life, migration to successor product, or historical-reference framing — which all three caveated valence classes satisfy. The treatment of \texttt{ambiguous} follows pre-reg E3 (light-hedging convention).}
\end{table}

### 2.7 Edge cases

Five edge cases were pre-specified in the registration document (E1–E5).

- **E1** governs zero-Mint-mention waves. Not triggered (Mint mentions occurred at both waves).
- **E2** governs zero-naive in one wave only. Triggered: $n_{\text{naive},t_1}$ = 0 (see §3).
- **E3** governs light-hedging classification. Not triggered: zero `ambiguous` classifications were produced by the classifier in this run; the E3 sensitivity analysis is therefore identical to the primary analysis.
- **E4** governs classifier-judge disagreement. Structurally inapplicable given Deviations 1 and 2 (v0.7 has no separate judge). The substantive safeguard — author oversight — is preserved as the manual-review procedure described in §2.8.
- **E5** governs successor-product framing for Mint→Credit Karma migrations. The post-classifier override (paragraph-proximity check) was triggered for 12 of 83 rows, all of which had already been classified as caveated by valence. The override therefore did not change any binary outcomes in the present sample.

### 2.8 Adjudication

The single naive classification produced by the classifier was reviewed against the v0.7 rule set as written. The author confirmed the classifier without override. The adjudication is logged in `/v10/data/adjudication_log.csv` per pre-reg E4 (residual safeguard), with timestamp, response identifiers, classifier output, author decision, and rationale.

## 3. Results

### 3.1 Per-wave metrics

Table 2 reports the per-wave matched-subset metrics under the primary mapping.

\begin{table}[H]
\centering
\begin{tabular}{lrrrrr}
\toprule
\textbf{Wave} & \textbf{n (matched, Mint)} & \textbf{n\textsubscript{naive}} & \textbf{n\textsubscript{caveated}} & \textbf{r\textsubscript{naive} (\%)} & \textbf{r\textsubscript{caveated} (\%)} \\
\midrule
t\textsubscript{1} & 43 & 0 & 43 & 0.00  & 100.00 \\
t\textsubscript{2} & 40 & 1 & 39 & 2.50  & 97.50  \\
\bottomrule
\end{tabular}
\caption{Per-wave matched-subset metrics for Mint, primary mapping. n\textsubscript{naive} is the count of responses classified as \texttt{live\_recommendation} (mapped to naive). E3 sensitivity mapping yielded identical metrics, since zero \texttt{ambiguous} classifications were produced by the classifier.}
\end{table}

\begin{figure}[H]
\centering
\includegraphics[width=\linewidth]{chart_v10_h2_naive_caveated.pdf}
\caption{Per-wave naive vs caveated phantom-presence breakdown for the matched two-model subset. At t\textsubscript{1}, all 43 Mint mentions carried some form of caveat; zero were naive. At t\textsubscript{2}, 39 of 40 carried caveats and one was naive. The single naive case is reproduced verbatim in §3.6.}
\end{figure}

\begin{figure}[H]
\centering
\includegraphics[width=\linewidth]{chart_v10_valence_distribution.pdf}
\caption{Distribution of the v0.7 5-class valence output across both waves before mapping to the v0.10 2-class binary. \texttt{status\_correction} (the strongest caveat type — explicit "Mint is decommissioned/closed/sunset" framing) dominates both waves. \texttt{historical\_reference} and \texttt{live\_with\_caveat} make up the remainder of the caveated cases. Zero \texttt{ambiguous} classifications were produced; the E3 sensitivity mapping is therefore identical to the primary mapping.}
\end{figure}

### 3.2 Pre-registered hypothesis evaluation

Table 3 summarises the pre-registered evaluation against the locked thresholds.

\begin{table}[H]
\centering
\renewcommand{\arraystretch}{1.15}
\begin{tabular}{p{0.18\textwidth}p{0.30\textwidth}p{0.20\textwidth}p{0.22\textwidth}}
\toprule
\textbf{Hypothesis} & \textbf{Pre-registered criterion} & \textbf{Status} & \textbf{Rationale} \\
\midrule
H1 (Stability) &
|Δr\textsubscript{naive}| ≤ 2.0 pp, conditional on n ≥ 100 floor at both waves &
INDETERMINATE &
Floor breached: n\textsubscript{t1}=43, n\textsubscript{t2}=40. Routed to descriptive disclosure path per §3.4 of pre-reg. \\
\addlinespace
H2 (Persistence) &
r\textsubscript{naive} > 0 at both waves &
FALSIFIED &
n\textsubscript{naive,t1}=0; n\textsubscript{naive,t2}=1. \\
\addlinespace
H3 (Co-movement) &
Diagnostic — no falsification status &
DECOUPLED &
Δgross = −3.12 pp; Δnaive = +2.50 pp. Magnitude ratio 0.80. \\
\bottomrule
\end{tabular}
\caption{Pre-registered hypothesis evaluation, primary mapping. The descriptive |Δr\textsubscript{naive}| under the primary mapping is +2.50 pp (t\textsubscript{2} − t\textsubscript{1}), marginally exceeding the ±2 pp band; the statistic is reported descriptively only and is not used for confirmatory inference under the floor breach.}
\end{table}

### 3.3 H1 — Stability

Status: **INDETERMINATE / underpowered.** The effective-n floor (§3.4 of pre-reg) was breached at both waves: t~1~ = 43, t~2~ = 40, both below the required n ≥ 100. H1 was routed to descriptive disclosure as pre-specified. Descriptive value: |Δr~naive~| = 2.50 pp (t~2~ − t~1~ = +2.50 pp); the magnitude marginally exceeds the ±2 pp band but the statistic is not used for confirmatory inference.

### 3.4 H2 — Persistence

Status: **FALSIFIED.** $n_{\text{naive},t_1}$ = 0; $n_{\text{naive},t_2}$ = 1. The pre-registered confirmation criterion (r~naive~ > 0 at both waves) is not met. The single naive case is in t~2~ exclusively, producing a one-sided directional asymmetry per pre-reg E2.

### 3.5 H3 — Co-movement diagnostic

Status: **DECOUPLED.** Δgross (v0.9-reported, t~2~ − t~1~) = −3.12 pp; Δnaive (v0.10, t~2~ − t~1~) = +2.50 pp. The directional change is opposite — gross declines while naive rises. The magnitude ratio |Δr~naive~| / |Δr~gross~| = 0.80. The diagnostic is reported per pre-reg without falsification status.

\begin{figure}[H]
\centering
\includegraphics[width=\linewidth]{chart_v10_h3_decoupling.pdf}
\caption{Directional decoupling of gross Presence and naive-phantom rate across t\textsubscript{1} → t\textsubscript{2}. Gross Presence falls from 44.79\% to 41.67\% (Δ = −3.12 pp) while the naive rate rises from 0.00\% to 2.50\% (Δ = +2.50 pp). The directions are opposite; the magnitudes are comparable in absolute terms. At the matched-subset n observed in this study (43 and 40), the pattern is noise-dominated and reported as diagnostic only per pre-reg §2 H3.}
\end{figure}

### 3.6 The single naive case

The single naive classification at t~2~ was generated by claude-sonnet-4-6, prompt `p1_functional`, run 3. The full response is reproduced verbatim below; emphasis is preserved from the model's output.

> There are several good options depending on your needs:
>
> **Popular Choices**
>
> **Free Options:**
>
> - **Mint** — Comprehensive, links to bank accounts, automatic categorization
> - **YNAB (free trial)** — Strong budgeting methodology, very popular
> - **Personal Capital** — Good for tracking net worth alongside spending
>
> **Paid Options:**
>
> - **YNAB (~$15/month)** — Many people find it worth the cost for the structured approach
> - **Copilot** — Clean interface, good for iPhone users
>
> **Simple/Basic:**
>
> - **Your bank's app** — Often underrated, already has your data
> - **Spreadsheet (Google Sheets/Excel)** — Free, fully customizable
>
> **Things to Consider**
>
> - **Privacy comfort** — Some apps require linking bank accounts
> - **Your budgeting style** — Zero-based vs. general tracking
> - **Platform** — iOS vs. Android availability
> - **How much effort** you want to put in
>
> **Honest Considerations**
>
> - The "best" app is the one **you'll actually use consistently**
> - Many people start with apps but find simple spreadsheets more sustainable
> - Free apps sometimes monetize your financial data
>
> **YNAB** tends to get the strongest loyal following, while **Mint** is the most common starting point for beginners.

The response treats Mint as a currently-available "Free Option," describes its features in present tense ("Comprehensive, links to bank accounts, automatic categorization"), and explicitly recommends it as "the most common starting point for beginners." No caveat about decommissioning, shutdown, sunset, or migration to Credit Karma appears anywhere in the response. The classifier valence (`live_recommendation`) and binary mapping (`naive`) were both confirmed without author override.

## 4. Discussion

### 4.1 Interpretation under the floor breach

The pre-registered floor at n ≥ 100 was breached substantially at both waves (43 and 40). H1 is therefore not evaluable as confirmatory. The descriptive value of |Δr~naive~| = 2.50 pp would, in a powered test, marginally exceed the ±2 pp band, but the small sample size renders the statistic noise-dominated. A single classification flip in either wave moves r~naive~ by 2.5 pp at n = 40 and by 2.3 pp at n = 43, both within the band's nominal width. No confirmatory inference about stability can be drawn from the present data; the result is informative only as a descriptive observation about the empirical magnitudes encountered.

The floor was specified in the pre-registration precisely to handle this case. Pre-registration discipline demands that the breach trigger the descriptive-disclosure path rather than a relaxation of the threshold; the path was engaged at scoring without modification.

### 4.2 H2 falsification and its substantive significance

H2 is empirically falsified in a binary sense: the pre-registered claim that r~naive~ > 0 at both waves is not met. $r_{\text{naive},t_1}$ = 0.00% — zero Mint-mentioning responses at t~1~ in the matched subset were classified as naive. Every Mint mention at t~1~ carried some form of caveat: `live_with_caveat`, `status_correction`, or `historical_reference` framing. At the v0.6 baseline measurement window, classifier-detectable correction had already propagated to 100% of Mint surfacings in the matched-subset two-model frontier substrate.

This is a stronger correction baseline than v0.7 BBB recorded for Mint at the v0.6 measurement window (1.7%). The discrepancy may reflect: (a) v0.7's classifier resolution against a sample subset that included models beyond the matched two; (b) genuine substrate evolution between v0.7's measurement window (4 May 2026) and the v0.10 measurement window (9 May 2026, applied to v0.9's t~1~ data which was collected at the earlier v0.6 baseline); or (c) sampling noise at small n. The three explanations are not mutually exclusive and the present data do not adjudicate among them.

The substantive interpretation — that the naive-phantom phenomenon for Mint may be approaching but has not reached zero under v0.7's classifier definition — is supported by the t~2~ measurement: $r_{\text{naive},t_2}$ = 2.50%, with one naive case identifiable. The single case (§3.6) is a clean instance of the phenomenon: a frontier model (Sonnet 4.6) recommends a decommissioned product (Mint, two years post-decommissioning at the time of the t~2~ measurement) as a top current option in its category, with present-tense feature description and explicit endorsement as a beginner's choice. The case constitutes existence proof that the phenomenon is not yet structurally extinguished at the substrate level.

### 4.3 H3 decoupling

The directional decoupling (gross down, naive up) at small n is striking but provisional. If sampling noise dominates, the direction is uninformative. If substantive, two readings are available: (a) as caveat coverage matures across the model substrate, the residual naive cases become structurally harder to correct, possibly because they arise from prompt formulations or response-generation paths that bypass the typical correction pipeline; (b) the naive subset and gross subset are governed by partly different mechanisms — gross presence by training-data prevalence and retrieval propensity, naive subset by the response-time decision to caveat or not. A higher-volume study at n ≥ 100 per wave would distinguish noise from signal; the same dataset cannot.

### 4.4 Comparison to v0.7 BBB

v0.7 BBB recorded a naive rate of 1.7% for BBB at the v0.6 baseline against gross Presence of 38.2%. v0.10 records a combined naive rate of 1.20% (1/83) for Mint across both waves against gross Presence of 41.67% – 44.79%. The two studies are not directly comparable: different brands, different categories (household goods vs. personal finance), different decommissioning ages and narrative complexities (BBB's bankruptcy and rebrand to Beyond, Inc. is structurally more complex than Mint's straightforward sunset and migration to Credit Karma). The general direction — naive rates in the low single-digit percentages, well below gross Presence — is consistent across both studies. Whether this is a stable property of phantom-brand phenomena across categories or coincidence at small n is the question a multi-brand replication (potentially v0.11 or later) would address.

### 4.5 The deviations

Four deviations from the pre-registration's descriptive language were discovered during analysis Step 2 setup, prior to first classifier run, and are documented in `/v10/DEVIATIONS.md` (full text) and summarised in §Declarations below. The deviations stem from a single root cause: the pre-registration's description of the v0.7 classifier ("keyword/phrase rule list and judge-LLM verification protocol") did not match the actual v0.7 implementation (LLM-only, single call, no rule list, no separate judge). The substantive pre-reg instruction — "inherit v0.7 unchanged" — is preserved by using v0.7's actual classifier configuration. The deviations affect the methodological description of the v0.10 study, not the empirical outcomes of its hypotheses.

## 5. Limitations

**Sample size.** The matched-subset n at both waves (43, 40) is below the pre-registered floor (100). The descriptive-disclosure path absorbs the analytical consequence of this breach for H1, but does not rescue the small-n problem for descriptive interpretation. The present results should be read as descriptive observations, not as evidence about the population-level naive-phantom rate for Mint or for phantom brands generally.

**Single-brand scope.** v0.10 measures Mint only. Generalisation to other phantom brands requires additional study. The v0.7 BBB result and the present v0.10 Mint result, taken together, suggest naive rates in the low single-digit percentages; this is consistent across the two brands but is a sample of two and warrants caution before claiming a regularity.

**Classifier validation.** The v0.7 classifier — a single gpt-5.4-mini call at temperature 0 — has not been independently calibrated for inter-rater agreement at the v0.10 measurement window. v0.7 reported classifier confidence diagnostics for BBB; those diagnostics are not directly transferable to Mint without additional validation work. The present study relies on the inherited classifier and reports the adjudication outcome (one author review, no override) as the residual quality signal.

**Substrate evolution.** AI model training and retrieval substrates evolve continuously. The present result is a snapshot within the v0.9 measurement windows (April–May 2026); it does not characterise the trajectory of the naive-phantom phenomenon across longer time scales. A v0.10-equivalent study at a substantially later window (six months, twelve months) would characterise the longer-interval trajectory.

**Cross-wave classifier consistency.** The classifier was applied to both waves at a single classification window (May 2026). Any variation in the underlying gpt-5.4-mini classifier across that window is not characterised. v0.7 used a similar single-window classification; this is an inherited property of the methodology rather than a v0.10-specific limitation.

## 6. Future research

**Higher-volume replication.** Re-running v0.10 against a larger pool of matched-subset Mint mentions would clear the n ≥ 100 floor and enable confirmatory inference on H1. The most natural source for higher-volume data is a deliberate v0.10b collection at a third time point t~3~ specifically scaled to clear the floor — for example, a higher prompt count per wave, or expansion of the matched subset to include additional models if methodologically defensible.

**Multi-brand replication.** Extending the v0.7/v0.10 protocol to additional phantom brands — Toys "R" Us, Circuit City, RadioShack, Pier 1, JCPenney post-bankruptcy, or comparable domain-specific phantoms — would establish whether the low-single-digit naive rate observed for both BBB and Mint is a category-general property of the phenomenon or specific to particular brands.

**Longer-interval longitudinal characterisation.** The present seven-day interval between t~1~ and t~2~ is short relative to typical model retraining cycles. Repeating the measurement at one-month, three-month, and twelve-month intervals — particularly across documented model-pipeline transitions or training-cutoff updates — would characterise the trajectory of the phenomenon at scales relevant to substrate evolution.

**Mechanism-level decomposition.** The H3 decoupling diagnostic, if substantively replicated at higher n, suggests the naive subset and gross subset may be governed by partly different mechanisms. Designed-for-test studies isolating the response-time decision to caveat (as opposed to the retrieval-time decision to surface) would clarify the mechanism. Candidate manipulations include prompt-level cues that force or suppress temporal context, and ablation of specific portions of the response generation context.

## 7. References

The AIAS measurement program publishes each phase as a separate working paper at SSRN; the present paper cross-cites prior phases. All abstract IDs link via `https://ssrn.com/abstract={id}`.

- AI Availability — A Theoretical Layer Above Mental and Physical Availability (foundational paper). SSRN 6659000.
- AIAS Presence Measurement Protocol v1.1 (methodology document). SSRN 6722319.
- v0.6 Cross-Category Findings. SSRN 6720959.
- v0.7 Phantom-Brand BBB. SSRN 6721779.
- v0.8 Discourse-Language Knives. SSRN 6728000.
- v0.9 Longitudinal Re-Baseline. SSRN 6736878.

External references invoked in framing or interpretation:

- Sharp, B. (2010). *How Brands Grow: What Marketers Don't Know.* Oxford University Press.
- Romaniuk, J. (2018). *Building Distinctive Brand Assets.* Oxford University Press.
- Sparrow, B., Liu, J., & Wegner, D. M. (2011). Google Effects on Memory: Cognitive Consequences of Having Information at Our Fingertips. *Science,* 333(6043), 776–778.
- Mosier, K. L., & Skitka, L. J. (1996). Human decision makers and automated decision aids: Made for each other? In R. Parasuraman & M. Mouloua (Eds.), *Automation and Human Performance: Theory and Applications* (pp. 201–220). Lawrence Erlbaum Associates.

## Declarations

**Conflict of interest.** The author is also Director of Corporate Brand Creative and Governance at Samsung Electronics America. The v0.10 study, like all AIAS program publications, is independent research developed outside the scope of that employment. Mint and Credit Karma are not Samsung properties. No Samsung resources were used in the design, conduct, analysis, or reporting of this study.

**Funding.** None.

**Data and code availability.** All raw responses (inherited from v0.9 deposit), classifier configuration, classification outputs, scoring outputs, registry files, adjudication log, deviations log, and build scripts are deposited at OSF project ec6wh, `/v10/`, prior to SSRN submission.

**Pre-registration.** The pre-registration document is locked at git commit `8767f44`, tag `v0.10-prereg`, on 2026-05-09, prior to any application of the v0.7 caveat-classifier to the v0.9 Mint response subset. No analysis output existed at the moment of lock.

**Deviations from pre-registration.** Four deviations from the pre-registration's descriptive language were discovered during analysis Step 2 setup, prior to first classifier run. The substantive pre-reg instruction ("inherit v0.7 unchanged") is preserved across all four. The deviations affect the methodological description of the v0.10 study, not the empirical outcomes of its hypotheses. Full deviation entries are committed to `/v10/DEVIATIONS.md`; the four are summarised here:

1. **Classifier description.** Pre-reg §5 described the classifier as "a keyword/phrase rule list and judge-LLM verification protocol." The actual v0.7 classifier is LLM-only, with no rule list and no separate judge. The substantive instruction ("inherit v0.7 unchanged") is preserved by using v0.7's actual configuration.
2. **No separate judge-LLM.** Pre-reg §6 listed "Apply v0.7 caveat-classifier" (step 2) and "Apply judge-LLM verification" (step 3) as separate steps. v0.7 has only one LLM call. Steps 2 and 3 are collapsed into a single step.
3. **5-class to 2-class mapping.** v0.7 outputs five valence classes; v0.10's hypotheses operate on a 2-class binary. The mapping (Table 1) was specified at first classification and locked thereafter.
4. **E4 inapplicability cascade.** E4 (classifier-judge disagreement adjudication) is structurally inapplicable given Deviations 1 and 2. The substantive safeguard (author oversight of edge cases) is preserved as a manual-review procedure, with all adjudications logged in `/v10/data/adjudication_log.csv`.

## Author information

**Pablo Ulpiano González Castro** is a faculty member in the MPS Branding programme at the School of Visual Arts (New York, NY) — primary academic affiliation. He is the founder of Third System^TM^, the independent research entity (data archive and methodology venue) under which the AIAS measurement programme is conducted and deposited. Correspondence: pablou@pablou.com · pablou.com. ORCID: [0009-0003-8968-9990](https://orcid.org/0009-0003-8968-9990).
