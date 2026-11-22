---
title: "AI Brand Presence against a Commercial Visibility Score and Human Brand Norms"
subtitle: 'Two pre-registered construct-validity tests of the AIAS™ Presence component'
author: "Pablo Ulpiano González Castro"
date: "November 2026"
mainfont: "Carlito"
fontsize: 11pt
geometry: [letterpaper, margin=1in]
linkcolor: "black"
urlcolor: "black"
subparagraph: true
header-includes: |
  \usepackage{setspace}
  \usepackage{booktabs}
  \usepackage{graphicx}
  \usepackage{float}
  \usepackage{caption}
  \usepackage{titlesec}
  \usepackage{needspace}
  \usepackage{tabularx}
  \captionsetup{font=small,labelfont=bf}
  \titlespacing*{\section}{0pt}{14pt}{4pt}
  \titlespacing*{\subsection}{0pt}{10pt}{2pt}
  \setstretch{1.36}
  \widowpenalty=10000
  \clubpenalty=10000
  \setlength{\parskip}{8pt}
  \setlength{\parindent}{0pt}
  \renewcommand{\maketitle}{}
---

<!--
  Program study 67: the v0.27 (CV.03) and v0.28 (CV.04) legs reported together.
  Build: python3 papers/v0_27_28/build_paper_v0_27_28.py (pandoc -> xelatex, Carlito).
  Every number is taken from a locked record; the number-by-number source map is
  papers/v0_27_28/NUMBERS_PROVENANCE_v0_27_28.md. No statistic in this paper is new.
-->

\begin{titlepage}
\setstretch{1.0}
\setlength{\parskip}{0pt}
\centering
\vspace*{1.6cm}

{\LARGE\bfseries AI Brand Presence against a Commercial\\[4pt] Visibility Score and Human Brand Norms\par}

\vspace{0.6cm}
{\large\itshape Two pre-registered construct-validity tests of the AIAS\texttrademark{} Presence component\par}

\vspace{0.5cm}
{\normalsize Working Paper \textperiodcentered{} November 2026\par}
{\normalsize AIAS Presence Measurement Protocol v1.6 \textperiodcentered{} construct-validity legs CV.03 (v0.27) and CV.04 (v0.28)\par}

\vspace{1.4cm}
{\large Pablo Ulpiano González Castro\par}

\vspace{0.3cm}
{\normalsize School of Visual Arts, MPS Branding Program, New York, NY\\(primary academic affiliation)\par}
\vspace{0.15cm}
{\normalsize Third System\texttrademark{} (research entity; data archive and methodology venue)\par}

\vspace{0.4cm}
{\small Correspondence: pablou@pablou.com \textperiodcentered{} pablou.com\par}
{\small ORCID: \href{https://orcid.org/0009-0003-8968-9990}{0009-0003-8968-9990}\par}

\vfill
{\small Pre-registrations at git tags \texttt{v0.27-prereg-r1} to \texttt{v0.27-prereg-r5} and \texttt{v0.28-prereg-r1}, \texttt{v0.28-prereg-r2};\\
locked results at \texttt{v0.27-report-locked} and \texttt{v0.28-results-locked}.\\
Data, code and verdicts: OSF \texttt{osf.io/ec6wh} (folders v27 and v28).\par}
\end{titlepage}

# Abstract {-}

AI availability, the propensity of a brand to be surfaced when people ask large language models about its category, is measured in the AIAS program by a Presence component built from model recognition and two recall channels. This paper reports two pre-registered construct-validity tests of Presence, first written up separately, with every hypothesis and verdict as locked and no new analysis. Study 1 (convergent; 24 B2B SaaS brands) correlated a recall-share form of Presence with the Share-of-Voice score of a commercial AI-visibility instrument, the HubSpot AEO Grader. The primary hypothesis was falsified (Spearman ρ = 0.29, 95% CI [−0.17, 0.64]); neither pre-specified sensitivity changed that. Model recognition sat at ceiling for every brand, confirming the recognition-null control. An exploratory scan found recall share tracking the instrument's presence-quality (ρ = 0.80) and brand-recognition (ρ = 0.75) subscores; the Share-of-Voice gap is one of rank alignment, not restricted range. Study 2 (discriminant; 24 Technology brands drawn by seeded stratified sampling) correlated blind-acquired Presence with human brand norms from the BRAND database. Presence was discriminant from recognition sensitivity d′ (ρ = 0.38; the BCa interval stays below the 0.74 reducibility threshold), so that hypothesis was confirmed. Against familiarity the point estimate (ρ = 0.59) fell in the partial band, but the BCa interval [0.18, 0.83] spanned all three pre-registered bands, and the locked rule returned undetermined. Because recognition was saturated in Study 1 and recall floored for most brands in Study 2, the two studies tested different facets of Presence: recall in the first, recognition in the second. Convergence with a commercial visibility score was not established, and the familiarity question remains open at n = 24.

**Keywords:** AI availability; brand availability; AIAS; pre-registration; Ehrenberg-Bass; construct validity; convergent validity; discriminant validity; large language models; AI visibility tools; brand familiarity; recognition memory

**JEL codes:** M31 (primary); L86; L15; D83; M37

**Paper status:** Both studies were pre-registered at git tags and scored once. Study 1's design was locked before the criterion instrument was queried, and two amendments were tagged after collection and before scoring; Study 2 was locked before any model was queried. They were first written up as separate working papers (Study 1 as program version v0.27, Study 2 as v0.28), which remain available at OSF. This paper reports the two studies together under a common frame. It adds no data, no analysis and no statistic: every number below is taken from the locked records of the two studies (pre-registrations, data and verdict files, figures and the earlier papers) or of the program's earlier v0.25 study, and pre-registered labels and verdicts are reported as recorded.

# 1. Introduction

Ehrenberg-Bass accounts of brand growth rest on two measurable forms of availability: mental availability, the propensity of a brand to come to mind in buying situations, and physical availability, the ease of finding and buying it (Sharp, 2010). The Tri-System framework adds a third layer for a setting in which category questions are increasingly put to large language models: AI availability, the propensity of a brand to be surfaced when a model is asked about its category (González Castro, 2026a, 2026b). The AIAS (AI Availability Score) program measures the first component of that layer, Presence, from two kinds of model output: whether models recognize a brand as belonging to its category, and how often they name it when asked open category questions.

A new measure earns its place through construct validation. It should correlate with measures of the same trait taken by other methods, and correlate less with measures of different traits (Cronbach & Meehl, 1955; Campbell & Fiske, 1959). Two earlier legs of the program supplied one cell of each kind. In v0.25, the Presence composite converged with Google Trends search interest across 24 B2B SaaS brands (ρ = 0.74; González Castro, 2026h); in v0.26, Presence stood orthogonal to Amazon Best Sellers Rank (González Castro, 2026i). The combination of those two legs into a Campbell–Fiske baseline is reported separately (González Castro, 2026j) and is not repeated here.

This paper reports the next two legs. Study 1 (program version v0.27, construct-validity leg CV.03) asked whether Presence converges with a commercial AI-visibility score, the kind of instrument now offered to brands as a reading of how present they are in ChatGPT, Perplexity or Gemini. Study 2 (v0.28, CV.04) asked the opposite question of human memory: whether Presence is reducible to how familiar people are with a brand, or to how reliably they recognize it. Each study was pre-registered, locked and scored once, and each was first written up on its own (González Castro, 2026k, 2026l).

Reporting the two together does two things. It places a failed convergent test and a partly resolved discriminant test side by side, as a construct-validity record should be read. And it shows that the studies, run on different categories, tested different parts of the Presence score: recognition was saturated in the first, so only recall varied, while recall was sparse in the second, so Presence moved mostly with recognition. Section 2 sets out what the studies share. Sections 3 and 4 report each study as pre-registered. Section 5 reads them together, and Section 6 states the limitations.

# 2. Common frame

## 2.1 Presence and its components

Under the AIAS Presence Measurement Protocol, version 1.6 (González Castro, 2026c, 2026d, 2026e, 2026f, 2026g), Presence is built from three counts over a fixed panel of six models. Recognition, $C_P$, is the number of models (0–6) that answer yes when asked whether the brand belongs to the category. Category recall, $R_{cat}$, counts the times the brand is named across leadership- or quality-framed category questions; cultural recall, $R_{cult}$, counts the same across salience-framed questions. The Presence composite is the equal-weight mean of the three components, each expressed as a fraction of its maximum and scaled to 0–100.

## 2.2 Two operationalizations, each fixed in advance

The two studies test different AIAS-side variables, each fixed by its own pre-registration (Table 1). Study 1 reuses the AIAS-side data of the v0.24 B2B SaaS acquisition (González Castro, 2026m). Recognition was at ceiling on that substrate, so the study tests the variance-bearing recall share, recall-SOM = ($R_{cat}$ / 36) × 100, computed with the v0.25 scorer. Study 2 acquired new data on a Technology panel and tests the three-component composite, with recall normalized to the v1.6 maximum of 18 per channel.

One consequence bears on the thresholds. Both studies carry ρ = 0.74 from v0.25 as a benchmark. In v0.25 that value belongs to the Presence composite (H_CV_Primary, ρ = 0.7411); the recall-only metric that Study 1 reuses converged with Google Trends at ρ = 0.67 in the same study (H_CV_Recall). Study 2's composite is the like-for-like comparison; for Study 1 the benchmark is a fixed, pre-registered decision boundary rather than the value its own metric reached in v0.25.

## 2.3 Verdict discipline

Both studies follow the program's pre-registration discipline (Nosek et al., 2018). Hypotheses, thresholds and decision rules, and in Study 2 also the panel, the validator values and the probe wording, were committed to git and tagged before the relevant data existed; all tags are pushed to the program's remote repository. Verdict labels are the pre-registered ones: CONFIRMED, STRONG, PARTIAL, FALSIFIED, UNDETERMINED and NOT_RUN for the tests, EXPLORATORY for a scan registered as secondary and exploratory, and FULL, PARTIAL or ABSENT for Study 2's descriptive dissociation count. Study 1 inherited its AIAS-side data, so its lock preceded the criterion pull; Study 2 acquired Presence blind to the validator and joined the two in a single scoring run.

\begin{table}[!htb]
\centering
\caption{The two studies at a glance.}
\setstretch{1.0}\small
\begin{tabularx}{\textwidth}{@{}>{\raggedright\arraybackslash}p{0.16\textwidth}>{\raggedright\arraybackslash}X>{\raggedright\arraybackslash}X@{}}
\toprule
 & Study 1 (v0.27, CV.03) & Study 2 (v0.28, CV.04) \\
\midrule
Question & Convergent: does Presence track a commercial AI-visibility score? & Discriminant: is Presence reducible to human familiarity or recognition? \\
Brands & 24 B2B SaaS brands, v0.24 registry, four pre-defined cells & 24 Technology brands from the BRAND database, seeded draw of 8 per familiarity tertile \\
AIAS-side variable & recall-SOM = ($R_{cat}$ / 36) × 100 & Presence = ($C_P$/6 + $R_{cat}$/18 + $R_{cult}$/18) / 3 × 100 \\
Model panel & Claude Opus 4.7, Claude Sonnet 4.6, GPT-4o, GPT-4o mini, Gemini 2.5 Flash, Gemini 2.5 Flash-Lite (v0.24 corpus) & Claude Opus 4.5, Claude Sonnet 4.5, GPT-4o, GPT-4o mini, Gemini 2.5 Flash, Gemini 2.5 Flash-Lite \\
Criterion & HubSpot AEO Grader Share of Voice (0–10) & BRAND familiarity (1–7) and recognition sensitivity d′ \\
Test & Spearman ρ, percentile bootstrap 95\% CI, Holm correction & Spearman ρ banded on its absolute value, BCa bootstrap 95\% CI \\
Pre-registration & v0.27-prereg-r1 to r5 & v0.28-prereg-r1, r2 \\
Gating verdicts & FALSIFIED (primary) & UNDETERMINED (familiarity, primary); CONFIRMED (recognition, secondary) \\
\bottomrule
\end{tabularx}
\end{table}

# 3. Study 1: convergence with a commercial AI-visibility score (v0.27)

## 3.1 Design and pre-registration

The design was locked at tags v0.27-prereg-r1 to r3 before the criterion instrument was queried. Two later revisions, tagged after collection and before scoring, recorded the deferral of the construct-matched instrument (r4) and a name-ambiguity sensitivity (r5). The pre-registration logs six numbered entries: Entry 0, the deferral; Entry 1, the decision to compute the AIAS side from the inherited v0.24 corpus, with instrument pulls timed against each other rather than against the AIAS acquisition; Entry 2, the correction of the model-panel listing to the models actually present in that corpus; Entry 3, the pinning of the recall denominator; Entry 4, the alignment of instrument queries to the category-competitive frame of $R_{cat}$, with a type-2 sensitivity; and Entry 5, the Stride sensitivity. No hypothesis or threshold changed across the revisions.

## 3.2 Brands and the AIAS-side measure

The sample is the v0.24 registry of 24 B2B SaaS brands in four pre-defined cells: A, enterprise incumbents (Salesforce, HubSpot, ServiceNow, Workday, SAP, Oracle, Zendesk); B, high-identity challengers (Notion, Figma, Linear, Airtable, Slack, Miro); C, infrastructure and developer platforms (Datadog, Snowflake, Stripe, Twilio, Cloudflare, MongoDB); and D, defunct or absorbed products (Quip, Yammer, Wunderlist, HipChat, Stride). The AIAS-side variable is recall-SOM = ($R_{cat}$ / 36) × 100, the pooled count of mentions across six category-leadership prompts (for example, "What are the leading B2B SaaS platforms?") put to each of the six models, computed by the v0.25 scorer without change. Recognition $C_P$ was 6 of 6 for every brand, so it enters only as a control (Section 3.6).

## 3.3 The criterion instrument

Instrument I1 is the free tier of the HubSpot AEO Grader. For a named brand it returns a profile across three engines on five dimensions: Brand Sentiment (out of 40), Presence Quality (20), Brand Recognition (20), Market Competition (10) and Share of Voice (10), together with an overall score out of 100. All 24 brands were queried in one session under a uniform frame (geography "United States", products and services "B2B SaaS", industry "Technology"), and each dimension was averaged over the three engines.

The pre-registration rated I1 a loose construct match: the Grader scores a named brand in isolation and cannot be scoped to a category on the free tier, whereas recall-SOM is category-competitive. It was committed in advance as the convergent floor. The hypothesis text names the Grader's visibility composite, but the construct-alignment rule pinned at r3 (Entry 4) directs convergent tests to the within-category Share of Voice dimension rather than the brand-absolute overall grade, and the locked scorer tests H_CV3_Primary on Share of Voice (I1_sov). The overall score enters only the exploratory scan.

## 3.4 Deferred and unrun instruments

The construct-matched instrument, I2 (Profound, category-scoped share of model), is enterprise-only; access was declined as disproportionate at r4 (Entry 0), so H_CV3_Profound and H_CV3_SOM are NOT_RUN. The discriminant contrast, I3 (Brandwatch web-mention volume), was not run, so H_CV3_Discriminant is NOT_RUN. The convergent claim therefore rests on I1 alone.

## 3.5 Hypotheses and analysis

Correlations are Spearman ρ at the brand level with a 10,000-resample percentile bootstrap 95% CI (fixed seed 20270527) and Holm (1979) correction across the primary family; a covered n below 12 returns UNDETERMINED. H_CV3_Primary predicted convergence of recall-SOM with I1_sov: CONFIRMED if ρ ≥ 0.60 with adjusted p < 0.05, STRONG if ρ ≥ 0.74, FALSIFIED if ρ < 0.30 or not significant, PARTIAL otherwise. Two sensitivities were registered for the primary test. The type-2 construct gap drops the four brands with $R_{cat}$ = 0 but $R_{cult}$ > 0 (Linear, Airtable, Miro, Cloudflare), which a brand-absolute instrument can see while category recall cannot. The Stride confound drops Stride, whose name is shared by unrelated entities that the Grader cannot exclude. The five Cell D brands with zero recall on both channels stay in the primary test as genuine concordant absence. H_CV3_Recognition_Null predicted that $C_P$ carries no usable variance. H_CV3_Component cross-correlates the AIAS-side variables with the Grader's dimensions as an exploratory scan.

## 3.6 Results

Table 4 lists every pre-registered outcome of Study 1; the findings follow in order.

### Primary convergent hypothesis (H_CV3_Primary): FALSIFIED

Recall-SOM did not converge with Share of Voice: ρ = 0.294, n = 24, Holm-adjusted p = 0.164, 95% CI [−0.171, 0.638] (Figure 1). The estimate is below the 0.30 falsification line and not significant, so the locked rule returns FALSIFIED. Excluding the four type-2 brands raised the correlation to ρ = 0.359 (n = 20, change +0.065); excluding Stride lowered it to ρ = 0.223 (n = 23, change −0.071). Neither sensitivity approaches the 0.60 confirmation threshold, and the second shows that the weak positive estimate partly rests on a brand whose Share of Voice may not refer to the intended product. Much of the rank agreement that exists comes from the defunct brands, which both measures place low (Share of Voice 0.33 for Wunderlist and HipChat, 2.00 for Yammer); Table 2 lists every brand.

\begin{figure}[!htb]
\centering
\includegraphics[width=0.86\textwidth]{papers/v0_27/figs/v0_27_scatter_recall_sov.pdf}
\caption{Recall-SOM (horizontal, 0--100) against HubSpot AEO Grader Share of Voice (vertical, mean of three engines, 0--10) for the 24 B2B SaaS brands, marked by type: live, type-2, defunct, and Stride. Locked v0.27 figure, reproduced unchanged.}
\end{figure}

\begin{table}[!htb]
\centering
\caption{Study 1 brand-level data (v0.24 recall counts; I1 pulled in one session). Ranks are competition ranks; the rank gap is the recall rank minus the Share of Voice rank.}
\setstretch{1.0}\small
\begin{tabular}{@{}lcrrrrrrr@{}}
\toprule
Brand & Cell & $R_{cat}$ & $R_{cult}$ & Recall-SOM & Share of Voice & Recall rank & SoV rank & Rank gap \\
\midrule
Salesforce & A & 36 & 25 & 100.0 & 7.67 & 1 & 4 & −3 \\
Workday & A & 34 & 7 & 94.4 & 7.33 & 2 & 7 & −5 \\
Slack & B & 33 & 30 & 91.7 & 5.67 & 3 & 18 & −15 \\
HubSpot & A & 33 & 21 & 91.7 & 7.00 & 3 & 14 & −11 \\
Oracle & A & 26 & 8 & 72.2 & 6.00 & 5 & 17 & −12 \\
SAP & A & 25 & 8 & 69.4 & 7.00 & 6 & 14 & −8 \\
Zendesk & A & 18 & 4 & 50.0 & 7.33 & 7 & 7 & 0 \\
ServiceNow & A & 17 & 8 & 47.2 & 7.67 & 8 & 4 & +4 \\
Snowflake & C & 10 & 13 & 27.8 & 7.33 & 9 & 7 & +2 \\
Datadog & C & 7 & 8 & 19.4 & 7.00 & 10 & 14 & −4 \\
Stripe & C & 4 & 6 & 11.1 & 8.00 & 11 & 2 & +9 \\
Notion & B & 2 & 27 & 5.6 & 7.33 & 12 & 7 & +5 \\
Twilio & C & 2 & 2 & 5.6 & 7.33 & 12 & 7 & +5 \\
MongoDB & C & 1 & 4 & 2.8 & 8.00 & 14 & 2 & +12 \\
Figma & B & 1 & 23 & 2.8 & 8.33 & 14 & 1 & +13 \\
Wunderlist & D & 0 & 0 & 0.0 & 0.33 & 16 & 23 & −7 \\
Quip & D & 0 & 0 & 0.0 & 4.67 & 16 & 19 & −3 \\
Yammer & D & 0 & 0 & 0.0 & 2.00 & 16 & 22 & −6 \\
HipChat & D & 0 & 0 & 0.0 & 0.33 & 16 & 23 & −7 \\
Miro & B & 0 & 8 & 0.0 & 7.33 & 16 & 7 & +9 \\
Cloudflare & C & 0 & 3 & 0.0 & 7.67 & 16 & 4 & +12 \\
Airtable & B & 0 & 10 & 0.0 & 7.33 & 16 & 7 & +9 \\
Linear & B & 0 & 12 & 0.0 & 4.67 & 16 & 19 & −3 \\
Stride & D & 0 & 0 & 0.0 & 3.00 & 16 & 21 & −5 \\
\bottomrule
\end{tabular}
\end{table}

### Recognition-null control (H_CV3_Recognition_Null): CONFIRMED

Every brand scored $C_P$ = 6 of 6 (mean 6.0, standard deviation 0), as in v0.24 and v0.25 (Figure 2). With no variance, recognition cannot carry a convergent signal on this substrate, and the control is CONFIRMED. The practical consequence is that Study 1 tested the recall part of Presence only.

\begin{figure}[!htb]
\centering
\includegraphics[width=0.80\textwidth]{papers/v0_27/figs/v0_27_recognition_ceiling.pdf}
\caption{AIAS recognition $C_P$ (rescaled to 0--100) and recall-SOM for the 24 B2B SaaS brands, plotted on one 0--100 axis. Locked v0.27 figure, reproduced unchanged.}
\end{figure}

### Exploratory component scan (H_CV3_Component)

The registered scan cross-correlates three AIAS-side variables (recall-SOM; the v0.25 Presence composite on the same corpus; and identity load, $R_{cult}$ − $R_{cat}$) with the five Grader dimensions (Table 3). For recall-SOM, presence quality (ρ = 0.798) and brand recognition (ρ = 0.748) are the strongest matches and exceed the 0.74 benchmark, while Share of Voice (0.294), market competition (0.297) and sentiment (0.133) are weak (Figure 3, which also shows the Grader's overall score at 0.44). The composite shows the same ordering. The scorer records the scan as EXPLORATORY and does not adjudicate the registered block structure; neither does this paper. These correlations do not bear on H_CV3_Primary, which is fixed to Share of Voice and falsified; nominating a better-correlating dimension after the fact is not available under the pre-registration.

\begin{table}[!htb]
\centering
\caption{Study 1 exploratory scan: Spearman ρ between AIAS-side variables and HubSpot AEO Grader dimensions (n = 24; locked v0.27 verdicts).}
\setstretch{1.0}\small
\begin{tabularx}{\textwidth}{@{}l*{5}{>{\raggedleft\arraybackslash}X}@{}}
\toprule
AIAS-side variable & Share of Voice & Sentiment & Presence Quality & Brand Recognition & Market Competition \\
\midrule
Recall-SOM & 0.294 & 0.133 & 0.798 & 0.748 & 0.297 \\
Presence composite & 0.326 & 0.383 & 0.842 & 0.792 & 0.354 \\
Identity load & 0.250 & 0.536 & −0.317 & −0.252 & 0.264 \\
\bottomrule
\end{tabularx}
\end{table}

\begin{figure}[!htb]
\centering
\includegraphics[width=0.86\textwidth]{papers/v0_27/figs/v0_27_component_rho.pdf}
\caption{Spearman ρ of recall-SOM with each HubSpot AEO Grader dimension and with the Grader's overall score (n = 24), with the 0.60 and 0.74 reference lines; the pre-registered metric is marked separately. Locked v0.27 figure, reproduced unchanged.}
\end{figure}

### Corrected account of the Share of Voice null

An early reading of this null took it as evidence that Presence is category-competitive and therefore diverges from brand-absolute visibility. The scan rules that out: presence quality and brand recognition are brand-absolute subscores, computed on a single named brand exactly as Share of Voice is, and recall-SOM tracks them. Range restriction does not fit either. Across the 19 live brands, the sample standard deviation of Share of Voice is 8.7% of its scale, larger than that of presence quality (5.6%) or brand recognition (4.8%). Share of Voice varies; its order does not follow recall (Figure 4). Two features of the data are consistent with this. Share of Voice is tie-heavy among live brands, with 7 of the 19 at exactly 7.33 out of 10, so it orders salient brands coarsely. And the subscores that converge describe what the engines know about a brand, which is closer to what recall-SOM counts than a competitive share is; the Grader's brand-recognition subscore tracks recall-SOM even though AIAS's own recognition count is at ceiling here. This account was corrected before the v0.27 deposit. It explains a falsified test and is exploratory; it does not substitute presence quality or brand recognition for the pre-registered metric.

\begin{figure}[!htb]
\centering
\includegraphics[width=0.86\textwidth]{papers/v0_27/figs/v0_27_recall_tracking.pdf}
\caption{Rank--rank plots of recall-SOM rank against the rank on two HubSpot AEO Grader dimensions, presence quality (left) and Share of Voice (right), with the line of perfect rank agreement (n = 24). Locked v0.27 figure, reproduced unchanged.}
\end{figure}

\begin{table}[!htb]
\centering
\caption{Study 1 pre-registered outcomes (locked v0.27 verdicts, tag v0.27-prereg-r5).}
\setstretch{1.0}\small
\begin{tabularx}{\textwidth}{@{}>{\raggedright\arraybackslash}p{0.27\textwidth}>{\raggedright\arraybackslash}p{0.17\textwidth}>{\raggedright\arraybackslash}X>{\raggedright\arraybackslash}p{0.14\textwidth}@{}}
\toprule
Hypothesis & Role & Result & Verdict \\
\midrule
H\_CV3\_Primary (recall-SOM × Share of Voice) & Primary & ρ = 0.294, n = 24, adjusted p = 0.164, CI [−0.171, 0.638] & FALSIFIED \\
H\_CV3\_Profound & Primary family & I2 not acquired (Entry 0, r4) & NOT\_RUN \\
H\_CV3\_SOM & Primary family & I2 not acquired (Entry 0, r4) & NOT\_RUN \\
H\_CV3\_Discriminant & Discriminant contrast & I3 not run & NOT\_RUN \\
H\_CV3\_Recognition\_Null & Control & $C_P$ mean 6.0, standard deviation 0 & CONFIRMED \\
H\_CV3\_Component & Exploratory scan & Table 3 & EXPLORATORY \\
Type-2 construct gap & Registered sensitivity & ρ = 0.359, n = 20 (change +0.065) & (none) \\
Stride confound & Registered sensitivity & ρ = 0.223, n = 23 (change −0.071) & (none) \\
\bottomrule
\end{tabularx}
\end{table}

\clearpage

# 4. Study 2: discriminance from human brand norms (v0.28)

## 4.1 Design and pre-registration

The design was locked at tag v0.28-prereg-r1 before any model was queried; one amendment (r2) was also committed before acquisition. The pre-registration logs three entries. Entry 0 is the conflict-of-interest screen, applied to the sampling frame before the draw (see Declarations). Entry 1, logged before any data collection, retargeted CV.04 from a mental-availability comparison to discriminant validity against open human norms, because the licensed survey data and the human-subjects collection the original plan required were not available. Entry 2 (r2) pinned the recall denominator of the Presence calculation to the v1.6 maximum of 18 per channel, instead of the 36 used on v0.25's six-frame-per-channel battery. Acquisition was completed and tagged (v0.28-acquisition-locked) before the single scoring run (v0.28-results-locked).

## 4.2 Validator and panel

The validator is the BRAND database (Raffaelli et al., 2025), which reports for brands of the Brand Finance US 500 list a mean familiarity rating on a 1–7 scale and a recognition-memory sensitivity, d′, from a signal-detection task. Its Technology category holds 80 brands, of which 70 have both measures. One of the 70, Harman International, was removed by the pre-registered conflict-of-interest screen before sampling, leaving a frame of 69. The frame was split into familiarity tertiles of 23, and eight brands were drawn at random from each with a fixed seed (280400). The panel (Table 5) spans familiarity from 1.00 to 6.83 and mixes consumer-facing brands with enterprise and industrial ones. The validator values were frozen in the pre-registration before acquisition. Technology was chosen as an adversarial substrate: it has the widest familiarity variance in BRAND, so it is where Presence was most likely to track familiarity.

\begin{table}[!htb]
\centering
\caption{Study 2 brand-level data, in descending order of familiarity. Familiarity and d′ are the frozen BRAND validator values; $C_P$, $R_{cat}$, $R_{cult}$ and Presence are the locked acquisition outputs.}
\setstretch{1.0}\small
\begin{tabular}{@{}lrrrrrr@{}}
\toprule
Brand & Familiarity (1–7) & d′ & $C_P$ (0–6) & $R_{cat}$ (0–18) & $R_{cult}$ (0–18) & Presence (0–100) \\
\midrule
Google & 6.83 & 3.08 & 6 & 12 & 16 & 85.2 \\
Apple & 6.73 & 3.21 & 6 & 18 & 18 & 100.0 \\
Netflix & 6.70 & 2.35 & 6 & 0 & 5 & 42.6 \\
Microsoft & 6.41 & 2.18 & 6 & 15 & 18 & 94.4 \\
Instagram & 6.39 & 2.75 & 5 & 0 & 6 & 38.9 \\
Uber & 6.34 & 1.95 & 6 & 0 & 0 & 33.3 \\
Airbnb & 5.90 & 1.91 & 6 & 0 & 0 & 33.3 \\
Dell Technologies & 5.71 & 2.21 & 6 & 3 & 0 & 38.9 \\
Whirlpool & 4.90 & 2.58 & 1 & 0 & 0 & 5.6 \\
3M & 4.86 & 1.66 & 4 & 0 & 0 & 22.2 \\
QVC & 4.07 & 1.43 & 0 & 0 & 0 & 0.0 \\
Motorola Solutions & 4.03 & 2.20 & 6 & 0 & 0 & 33.3 \\
Seagate Technology & 2.83 & 2.08 & 6 & 0 & 0 & 33.3 \\
Corning & 2.13 & 1.41 & 6 & 0 & 0 & 33.3 \\
VMware & 2.10 & 2.07 & 6 & 2 & 0 & 37.0 \\
Pitney Bowes & 1.67 & 1.11 & 3 & 0 & 0 & 16.7 \\
Thermo Fisher Scientific & 1.63 & 2.35 & 3 & 0 & 0 & 16.7 \\
Flex & 1.40 & 1.65 & 1 & 0 & 0 & 5.6 \\
HPE & 1.33 & 1.17 & 6 & 1 & 0 & 35.2 \\
CDW & 1.32 & 0.61 & 6 & 0 & 0 & 33.3 \\
NetApp & 1.17 & 0.79 & 6 & 0 & 0 & 33.3 \\
Jabil & 1.17 & 2.11 & 2 & 0 & 0 & 11.1 \\
Lam Research & 1.00 & 2.75 & 5 & 0 & 0 & 27.8 \\
Parker-Hannifin & 1.00 & 1.46 & 3 & 0 & 0 & 16.7 \\
\bottomrule
\end{tabular}
\end{table}

## 4.3 Presence acquisition

Presence was acquired on June 1, 2026, from the program's six-model reference panel (Table 1); its two Claude models differ from those in the v0.24 corpus behind Study 1. Phase A put one recognition probe to each model for each brand ("Is the brand *X* commonly recognized as a technology brand? Answer yes or no."), 144 probes in all; $C_P$ is the number of yes answers. Phase B put six category questions to each model, 36 queries in all: three for category recall (the best technology brands; those industry experts and analysts recommend; the highest-quality and most reliable) and three for cultural recall (the most talked about right now; the biggest cultural footprint; the most iconic or storied identity in popular culture). A brand scores a recall point each time it is named in a question-by-model response, up to 18 per channel. Presence is the equal-weight composite of v0.25 at the v1.6 recall maximum:

$$\text{Presence} = \frac{1}{3}\left(\frac{C_P}{6} + \frac{R_{cat}}{18} + \frac{R_{cult}}{18}\right)\times 100.$$

The validator was not consulted during acquisition.

## 4.4 Hypotheses and decision rule

Two gating hypotheses test reducibility with Spearman ρ, banded on its absolute value: H_Disc_Familiarity (primary; Presence against familiarity) and H_Disc_Recognition (secondary; Presence against d′). An absolute value below 0.50 is CONFIRMED (discriminant); from 0.50 to below 0.74, PARTIAL; 0.74 or above, FALSIFIED (reducible). The 0.74 ceiling is the v0.25 convergent benchmark: a discriminant correlation as high as the measure's own convergent correlation would indicate redundancy. Verdicts are gated on the point estimate. A BCa bootstrap 95% CI (Efron, 1987; 10,000 resamples, seed 280400) is reported as non-gating context with two flags: ci_excludes_reducibility, set when the upper bound of the absolute-value interval is below 0.74, and provisional, set for a CONFIRMED verdict whose interval does not exclude reducibility. A locked override returns UNDETERMINED when n is below 12 or the interval spans all three bands. Pearson r is reported alongside and does not gate. The registered prediction was ρ between 0.30 and 0.60, with PARTIAL the modal outcome.

A third hypothesis, H_Dissociation, is descriptive and does not gate. Presence and familiarity are standardized within the panel (population standard deviation); a brand is amplified if z(Presence) − z(familiarity) exceeds +1.0 and suppressed if it falls below −1.0. FULL requires at least four such brands with both directions present. The count shares its data with the primary correlation and is reported as texture, not as independent evidence.

## 4.5 Results

All 24 panel brands joined the validator by name. Presence ranged from 0.0 (QVC) to 100.0 (Apple), with Microsoft at 94.4 and Google at 85.2, and recognition $C_P$ ranged across the panel from 0 to 6 (Table 5). Table 6 lists the pre-registered outcomes.

\begin{table}[!htb]
\centering
\caption{Study 2 pre-registered outcomes (locked v0.28 verdicts, tag v0.28-results-locked). The two correlation hypotheses gate on the point estimate; the UNDETERMINED override fires when the BCa interval spans all three bands; the dissociation count is descriptive.}
\setstretch{1.0}\small
\begin{tabularx}{\textwidth}{@{}llrll>{\raggedright\arraybackslash}X@{}}
\toprule
Hypothesis & Role & Spearman ρ & Point band & BCa 95\% CI & Verdict \\
\midrule
H\_Disc\_Familiarity & Primary & 0.593 & PARTIAL & [0.179, 0.832] & UNDETERMINED \\
H\_Disc\_Recognition & Secondary & 0.379 & CONFIRMED & [−0.076, 0.714] & CONFIRMED \\
H\_Dissociation & Tertiary & n/a & n/a & n/a & FULL (11 of 24) \\
\bottomrule
\end{tabularx}
\end{table}

### Recognition sensitivity: CONFIRMED; familiarity: UNDETERMINED

Presence correlated with recognition sensitivity at ρ = 0.379 (p = 0.068; Pearson r = 0.461, p = 0.024), inside the discriminant band. The BCa interval is [−0.076, 0.714]; on the absolute scale it runs from 0 to 0.713, below 0.74, so ci_excludes_reducibility holds and the CONFIRMED verdict is not provisional (Figure 5). The interval is wide and reaches into the partial band: the locked rule establishes discriminance, but the estimate is imprecise.

Against familiarity the point estimate is ρ = 0.593 (p = 0.002; Pearson r = 0.569, p = 0.004), inside the partial band and within the registered prediction. The BCa interval [0.179, 0.832] begins in the CONFIRMED band and ends in the FALSIFIED band, so it spans all three; the override fires and the verdict is UNDETERMINED in place of the PARTIAL point verdict. At n = 24 the data cannot distinguish a discriminant Presence from one reducible to familiarity.

\begin{figure}[!htb]
\centering
\includegraphics[width=0.92\textwidth]{reports/figs/chart_28_verdict_bands.pdf}
\caption{Point estimate of the absolute Spearman ρ with its BCa 95\% interval for each gating hypothesis, drawn over the three pre-registered bands (n = 24, seed 280400). Locked v0.28 figure, reproduced unchanged.}
\end{figure}

### H_Dissociation (descriptive): FULL

\begin{figure}[!htb]
\centering
\includegraphics[width=0.66\textwidth]{reports/figs/chart_28_dissociation.pdf}
\caption{Within-panel standardized difference z(Presence) − z(familiarity) for each of the 24 Technology brands, with the ±1.0 thresholds. Locked v0.28 figure, reproduced unchanged.}
\end{figure}

Eleven of the 24 brands cross the ±1.0 threshold, in both directions (Figure 6). Four are amplified, with Presence above familiarity: Apple (+1.228), Microsoft (+1.150), HPE (+1.066) and NetApp (+1.065). Seven are suppressed: Netflix (−1.043), Instagram (−1.050), Uber (−1.253), Airbnb (−1.052), Whirlpool (−1.711), 3M (−1.031) and QVC (−1.559). The amplified brands are core technology brands. The suppressed set combines consumer-famous services that are not technology brands in the narrow sense (Netflix, Instagram, Uber, Airbnb) with familiar brands that no model named under the recall questions (Whirlpool, 3M, QVC; Table 5).

### What the discriminant tests measured in practice

\begin{figure}[!htb]
\centering
\includegraphics[width=0.80\textwidth]{reports/figs/chart_28_presence_composition.pdf}
\caption{Presence for each of the 24 Technology brands, stacked by the contribution of recognition $C_P$, category recall $R_{cat}$ and cultural recall $R_{cult}$ (0--100). Locked v0.28 figure, reproduced unchanged.}
\end{figure}

Recall was concentrated in a few consumer-facing leaders. Apple, Microsoft and Google were named on both channels, Netflix and Instagram only under the cultural questions, and Dell Technologies, VMware and HPE a few times under the category questions; every other brand scored zero on both channels (Table 5, Figure 7). Where both recall channels are zero, Presence equals one third of the recognition fraction, so across most of the panel Presence moved with $C_P$ alone. The familiarity-stratified draw, from a category whose mass is enterprise and industrial, met consumer-oriented recall questions that do not surface brands such as Jabil, Pitney Bowes or Parker-Hannifin. For most brands, then, Study 2 compared AI recognition, whether a model classes a brand as a technology brand, with the two human norms.

\clearpage

# 5. Discussion

## 5.1 Two studies, two facets of Presence

Read together, the studies tested different parts of one score. In Study 1 every brand was recognized by all six models, so recall was the only source of variance, and the falsified convergent test is a statement about category recall against a commercial Share of Voice score. In Study 2 recall was absent for most brands, so Presence moved mostly with recognition: the confirmed discriminant test is largely a statement about AI recognition against human recognition sensitivity, and the undetermined familiarity test is, for most of the panel, a statement about AI recognition against familiarity. Neither study tested the three-component score under conditions in which all three components vary. That is the main reason this paper does not pool them, and the main thing a later leg needs to supply.

## 5.2 Study 1: the headline score and the subscores

The pre-registered convergent test failed, and the strong exploratory correlations do not change that verdict. They do locate the failure. Recall-SOM tracked the two Grader subscores that describe what the engines know about a brand and did not track the Grader's headline Share of Voice, whose values are heavily tied among live brands and not ordered like recall. The exploratory pattern is consistent with v0.25, where the same program's Presence measure converged with search interest, which is also a prominence signal; it remains a hypothesis for a confirmatory test on a fresh substrate. For readers of commercial AI-visibility dashboards, the result is a caution rather than a verdict on any tool: on this substrate the headline Share of Voice figure was the dimension least aligned with category recall.

## 5.3 Study 2: recognition and familiarity

Presence, which for most of this panel reduces to AI recognition (whether a model classes a brand within its category), was only moderately related to human recognition sensitivity, and the locked rule classes that relationship as discriminant. The familiarity test behaved as an underpowered adversarial test should under a pre-registered override: the point estimate leaned toward partial overlap, as predicted, but the interval was too wide to exclude either a distinct or a reducible Presence, and the rule returned UNDETERMINED rather than a finding. The dissociation adds texture: the models favored core technology identity and under-weighted brands that are famous without being technology brands in the narrow sense. That pattern is what one would expect if Presence indexes something other than fame, but it shares its data with the familiarity correlation and is not separate evidence.

## 5.4 Place in the construct-validity record

With the v0.25 and v0.26 legs synthesized in v0.29 (González Castro, 2026j), the record for Presence now holds four cells: convergence with search interest (v0.25); no association with Amazon sales rank, which v0.29 reads as discriminant evidence (v0.26); a convergent test against a commercial visibility score, falsified on its pre-registered metric (Study 1); and a discriminant test against human norms, resolved for recognition sensitivity and unresolved for familiarity (Study 2). This paper computes no statistic across the two studies. They differ in category, brand set, model versions and AIAS-side variable, so a convergent–discriminant contrast computed across them would mix those differences with the trait comparison it is meant to isolate.

# 6. Limitations

*Sample size.* Each study has 24 brands. That was enough to falsify Study 1's primary hypothesis and to confirm Study 2's recognition hypothesis on the locked rules, but not to resolve the familiarity question, and every interval in both studies is wide.

*One loose-match instrument.* Study 1's convergent claim rests on a single instrument that was rated a loose construct match in advance. The construct-matched, category-scoped instrument and the discriminant contrast were not run, so the study cannot separate a failure of convergence from a mismatch between metrics. The estimate is also sensitive to one name-ambiguous brand (Stride).

*Facet coverage.* Recognition was saturated in Study 1 and recall was sparse for most brands in Study 2, so neither study tested the full three-component Presence score with all components varying (Section 5.1).

*Benchmark commensurability.* The 0.74 benchmark comes from the v0.25 composite, which normalized recall over six cues per channel; Study 2 uses the canonical three cues per channel, so its comparison with the benchmark is approximate on cue breadth. Study 1's recall-only metric converged with search interest at 0.67 in v0.25, so its 0.74 "strong" line is a pre-registered boundary, not a like-for-like value.

*Timing.* Study 1's AIAS side is a single measurement from the v0.24 acquisition, taken in the same calendar month as the instrument pull, compared against an instrument that refreshes continuously; residual drift is mitigated, not removed, by the rank-based test. Study 2's human norms were collected from US-resident consumers in 2020 and 2024 (Raffaelli et al., 2025), while Presence was measured in June 2026.

*Models and categories.* The two studies used different Claude model versions within six-model panels whose behavior will change, and each covers one category. Study 2's familiarity-stratified draw was enterprise-heavy, and its recall questions were consumer-oriented.

# 7. Further research

Four tests follow directly. The first is the deferred test against a category-scoped share-of-model instrument, which could show either that Presence converges with construct-matched measures, making Study 1's null evidence of specificity, or that it does not. The second is a confirmatory pre-registration of the presence-quality and brand-recognition convergence on a fresh substrate, with those dimensions fixed in advance. The third is a higher-powered familiarity test on a consumer category where recall does not floor, so that the full Presence score, not its recognition component alone, confronts familiarity. The fourth is the mental-availability leg deferred in Study 2, which needs brand-level category-entry-point data that are not available in open form.

# References {-}

Campbell, D. T., & Fiske, D. W. (1959). Convergent and discriminant validation by the multitrait-multimethod matrix. *Psychological Bulletin*, 56(2), 81–105.

Cronbach, L. J., & Meehl, P. E. (1955). Construct validity in psychological tests. *Psychological Bulletin*, 52(4), 281–302.

Efron, B. (1987). Better bootstrap confidence intervals. *Journal of the American Statistical Association*, 82(397), 171–185.

González Castro, P. U. (2026a). *AI Availability: Extending Mental and Physical Availability into Algorithmic Retrieval*. SSRN Working Paper 6659000. <https://ssrn.com/abstract=6659000>

González Castro, P. U. (2026b). *Tri-System Brand Growth: The AI Mediation Layer*. Marketing Science Institute Working Paper Series, Report No. 26-132.

González Castro, P. U. (2026c). *The AIAS Presence Measurement Protocol: Methodological Notes on Construct Validity and the Four-Regime Taxonomy* (v1.2). SSRN Working Paper 6761698. <https://ssrn.com/abstract=6761698>

González Castro, P. U. (2026d). *The AIAS Presence Measurement Protocol: Phase A Pivot-Validation Specification (v1.3)*. SSRN Working Paper 6797679. <https://ssrn.com/abstract=6797679>

González Castro, P. U. (2026e). *The AIAS Presence Measurement Protocol v1.4: Recognition × Recall Decomposition and Multi-Component AI Availability*. SSRN Working Paper 6799479. <https://ssrn.com/abstract=6799479>

González Castro, P. U. (2026f). *The AIAS Presence Measurement Protocol: Multi-Statistic C2 Specification and Two-Channel Recall Decomposition* (v1.5). SSRN Working Paper 6810758. <https://ssrn.com/abstract=6810758>

González Castro, P. U. (2026g). *Substrate Pre-Screening, Independent Moderator Pathway, and Phantom Brand Persistence Phase B Extension* (v1.6). SSRN Working Paper 6816340. <https://ssrn.com/abstract=6816340>

González Castro, P. U. (2026h). *Predictive Validity of AI Presence Index Against Google Trends Search Interest on the B2B SaaS Substrate: Construct Validity Pilot Under Protocol v1.6* (v0.25). Working paper. OSF, osf.io/ec6wh (folder v25).

González Castro, P. U. (2026i). *What AI Presence Does Not Predict: Amazon Best Sellers Rank as Discriminant Validity Evidence for the AIAS Construct* (v0.26). SSRN Working Paper 6847678. <https://ssrn.com/abstract=6847678>

González Castro, P. U. (2026j). *The Presence Component Is Construct-Valid: A Convergent–Discriminant (Campbell–Fiske) Baseline for AI Availability* (v0.29). SSRN Working Paper 6870778. <https://ssrn.com/abstract=6870778>

González Castro, P. U. (2026k). *A Pre-Registered Null on AI Share-of-Voice* (v0.27). Working paper. OSF, osf.io/ec6wh (folder v27).

González Castro, P. U. (2026l). *AI Availability is Not Reducible to Recognition Memory — and is Underpowered Against Familiarity at n = 24* (v0.28). Working paper. OSF, osf.io/ec6wh (folder v28).

González Castro, P. U. (2026m). *AI Presence in B2B SaaS: Marketing-Language Absorption, Identity Load Separation, and Phantom Brand Persistence in the Eighth Substrate Family* (v0.24). SSRN Working Paper 6838802. <https://ssrn.com/abstract=6838802>

Holm, S. (1979). A simple sequentially rejective multiple test procedure. *Scandinavian Journal of Statistics*, 6(2), 65–70.

Nosek, B. A., Ebersole, C. R., DeHaven, A. C., & Mellor, D. T. (2018). The preregistration revolution. *Proceedings of the National Academy of Sciences*, 115(11), 2600–2606.

Raffaelli, C., Bocchi, E., Estes, Z., & Adelman, J. S. (2025). BRAND: Brand recognition and attitude norms database. *Behavior Research Methods*, 57, Article 17. <https://doi.org/10.3758/s13428-024-02525-x>

Sharp, B. (2010). *How Brands Grow: What Marketers Don't Know*. Oxford University Press.

# Declarations {-}

## Conflict of interest {-}

The author is employed by Samsung Electronics America. Samsung had no role in the design, conduct, analysis or reporting of either study. Neither panel contains a Samsung-group brand: in Study 2, Harman International, a Samsung subsidiary, was removed from the eligible sampling frame by a pre-registered screen before the seeded draw. The Study 2 Technology panel includes brands that compete with Samsung in some product categories (Apple, Dell Technologies, Google, Microsoft, Seagate Technology, Whirlpool) and one brand in which a Samsung subsidiary holds a significant minority equity stake (Corning, in which Samsung Display is a shareholder); other panel brands may have supplier, customer or channel relationships with Samsung group companies. The panel was drawn by a fixed random seed within familiarity tertiles, and no brand was selected or excluded by the author after the screen. Study 1 evaluates commercial AI-visibility instruments; Cheil Worldwide, a Samsung affiliate, sells AI-visibility services. The author develops the AIAS measurement program through Third System. The author declares no other competing interests.

## Funding {-}

Self-funded.

## Ethics {-}

Not applicable; no human subjects. No data were collected from people for this paper. Study 2 uses published, aggregated, brand-level norms from the BRAND database, whose collection was approved by the institutional review boards of Bocconi University and City University of London (Raffaelli et al., 2025). Otherwise both studies use model outputs obtained through provider APIs and the outputs of a public web tool.

## Use of AI tools {-}

During the preparation of this work the author used AI tools (Anthropic's Claude) to assist with study design, analysis and writing. The author reviewed and edited all content and takes full responsibility for it.

## Data and code availability {-}

Data, scoring code and verdict files for both studies are deposited at OSF (osf.io/ec6wh). Study 1 is under v27: instrument and AIAS-side data, the 24-brand registry, scoring and figure code, the verdict file, the report and the earlier paper. Study 2 is under v28: the pre-registration content module and prompt, panel and validator files, raw and composed acquisition data, scoring code, the verdict file, the report and the earlier paper. Study 1's pre-registration content module and its revisions r1 to r5 are held in the program's git repository at tags v0.27-prereg-r1 to v0.27-prereg-r5; copies are deposited in the OSF v27 folder (v27/prereg). The Study 2 validator file reproduces 24 brands' familiarity and d′ values from the BRAND database (ResearchBox 1892, https://researchbox.org/1892), which is distributed under a CC BY 4.0 licence; reuse requires attribution to Raffaelli et al. (2025).
