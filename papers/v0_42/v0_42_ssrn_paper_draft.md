---
title: "Cross-Generation Stability of AI Brand Presence and Consistency"
subtitle: "A Pre-Registered Fourth Wave on the Newest Flagship Model of Each Provider (AIAS™ v0.42)"
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

{\LARGE \textbf{Cross-Generation Stability of AI Brand Presence and Consistency}}\\[8pt]

{\large A Pre-Registered Fourth Wave on the Newest Flagship Model of Each Provider\\ (AIAS™ v0.42)}\\[28pt]

Pablo Ulpiano González Castro\\[4pt]
School of Visual Arts, MPS Branding Program, New York, NY \textit{(primary academic affiliation)}\\
Third System™ (research entity; data archive and methodology venue)\\[8pt]
Correspondence: pablou@pablou.com · pablou.com\\
ORCID: \href{https://orcid.org/0009-0003-8968-9990}{0009-0003-8968-9990}\\[20pt]

Pre-registration: \texttt{ v0.42-prereg-r1 } (commit \texttt{ 58d1891bf2 }; deposited on OSF before the first t\textsubscript{4} call)\\
Data and code: OSF \texttt{ec6wh/v42}\\

\end{center}
\end{titlepage}

# Abstract {-}

Brand measures read from the answers of large language models (LLMs) can serve as a tracking metric only if they survive the replacement of the models that produce them. This pre-registered study is the fourth wave (t₄) of the AIAS measurement programme's five-category omnibus (audiophile headphones, skincare, cosmetics, automotive and premium spirits; 112 brands) and the first on the newest generally available flagship model of each provider: Claude Fable 5.2, GPT-6 Astra and Gemini 4 Argon. The 30 category questions were asked verbatim with web search off and on, in three runs each, and the 112 brand questions once with search off (876 calls); the answers were compared with the third wave (t₃), collected on 9 November 2026 on a retiring six-model panel. 876 of the 876 calls were answered.
Recall Presence ordered brands on the newest models as it had on the retiring panel (`H_Gen_Presence` CONFIRMED: pooled within-category ρ = 0.828, 95% interval 0.722 to 0.890, p = 0.0001, n = 112).
The brand order of the Consistency instrument φ fell between the pre-registered bars (`H_Gen_Phi` MARGINAL: ρ = 0.310, just above the falsification bar of 0.30, 95% interval 0.051 to 0.520, p = 0.0056, n = 73).
Turning on each provider's web search left the Presence ordering of the three-model panel intact (search-robust: ρ = 0.909, 95% interval 0.827 to 0.945), although per model the correlation ranged from 0.710 to 0.909 and Gemini 4 Argon searched in only 17.8% of its search-on calls.
Run-to-run reliability of recall, the noise floor for the planned t₅ and t₆ waves, ranged from 0.845 to 0.915 (one run against another) across models and conditions. Ranking, Sentiment, Coverage and Grounding analyses of the same answers are pre-registered separately and are not reported here.

**Keywords:** AI availability; brand availability; AIAS; pre-registration; Ehrenberg-Bass; large language models; model generations; cross-generation stability; web search; test--retest reliability; brand recall; consistency

**JEL codes:** M31; L86, L15, D83, M37

**Paper status:** Pre-registered prospective re-acquisition (tag `v0.42-prereg-r1`; revision r2 with clarifications C1--C28, deposited on OSF before the first $t_4$ call); 876 of 876 design calls answered; deviations recorded in `osf/v42/DEVIATIONS.md` (1 entry). Part of the AIAS measurement programme.

# 1. Introduction

AI Availability --- the discoverability and representation of a brand in the outputs of large language models --- has been proposed as a third measurable layer of brand availability (González Castro, 2026, SSRN 6659000), alongside the Mental and Physical Availability of the Ehrenberg-Bass tradition (Sharp, 2010; Romaniuk & Sharp, 2022). The AIAS programme measures it under a versioned protocol with two locked components. Presence is whether and how often models name a brand (Methodology v1.6, SSRN 6816340; AIAS 1.0, SSRN 6817841). Consistency is whether the models of a panel agree about a brand, measured by the mean-independent dispersion statistic $\varphi$ (Methodology v1.8, SSRN 6963359), which replaced a coefficient-of-variation quantity falsified as a Consistency instrument (Methodology v1.7, SSRN 6878818).

Since its v0.17 phase the programme has measured on one fixed panel of six models: Claude Opus 4.5, Claude Sonnet 4.5, GPT-4o, GPT-4o mini, Gemini 2.5 Flash and Gemini 2.5 Flash-Lite. That panel is retiring: Claude Opus 4.5 not sooner than 24 November 2026, Claude Sonnet 4.5 on 30 November 2026, and the GPT-4o and GPT-4o mini snapshots on 14 January 2027. Its last wave, $t_3$ (v0.41, SSRN 7685100), was collected on 9 November 2026 on the five-category omnibus first measured in May 2026 (v0.19--v0.23). Over the 152 days from $t_2$ to $t_3$ both components held on that panel: recall Presence kept its brand order in every category (per-category Spearman $\rho$ from 0.93 to 0.98), and $\varphi$ kept its order across 80 brands ($\rho = 0.681$). These are single-category and all-brand Spearman correlations, not the pooled within-category statistic of this study (§2.7), and are given as background rather than as comparators. From now on every new collection of the programme runs on current models.

Two questions follow before the programme builds its next components on current models. The first concerns generation: does the ordering of brands by AI availability carry over from the 2024--25 model generation to the 2026 generation? If it does, the programme's record on the legacy panel can be bridged to the new panel; if it does not, the new panel starts its own series. The second concerns the series: how much do the new models' answers vary from run to run? That noise floor is what the planned short-term ($t_5$) and three-month ($t_6$) stability waves will be judged against.

This study answers both with one pre-registered collection on the newest generally available flagship model of each provider. It contributes a primary test of cross-generation stability for Presence, a secondary test for Consistency, a two-sided test of what each provider's own web search does to Presence, and the run-to-run reliability of the new panel. A draft that also compared two current flagships of one provider was withdrawn before its lock under the programme's collection budget rule (§2.10). The answers are stored as the $t_4$ corpus for the programme's Ranking, Sentiment, Coverage and Grounding components; those analyses are pre-registered in their own papers and are not part of this one.

# 2. Method

## 2.1 Design

The study is a prospective re-acquisition. It re-asks, verbatim, the questions of the five-substrate omnibus --- v0.19 audiophile headphones (16 brands), v0.20 skincare, v0.21 cosmetics, v0.22 automotive and v0.23 premium spirits (24 brands each), 112 brand units --- to the three models of panel N3 (§2.2). Phase B (recall) asks six category questions per substrate (30 in all); Phase A (recognition) asks one question per brand (112). Phase B was collected without tools (S0) and with the provider's own web search (S1), in three independent runs each; Phase A once, in S0. The design therefore has 3 models × (30 × 2 conditions × 3 runs + 112) = 876 calls: 202 per model in S0 and 90 per model in S1. Each call is independent, with no conversation state carried between calls. Calls were sent in seven blocks in a fixed order --- Phase B S0 runs 1 to 3, Phase A S0, then Phase B S1 runs 1 to 3 --- with the three models in parallel within a block, so that the answers of the primary test and the recognition answers would be complete before the costlier search-on answers began.

The comparison wave, $t_3$, is the v0.41 collection of 9 November 2026 on the six legacy models (panel L6), with one run and no tools. $t_4$ was collected after the lock. The collection script enforced the window: no new request after the earlier of 72 hours from the first recorded call and 16 November 2026, 23:59:59 UTC, and no other paid collection running on the collection machine. The brand registries and their probe artefacts are unchanged from $t_1$--$t_3$: no brand was added, removed or renamed, and each registry carries its source-phase conflict-of-interest handling forward unchanged.

## 2.2 Panel

The panel rule selects the newest generally available flagship model of each provider (Anthropic, OpenAI, Google), verified from the vendor's own model documentation when the pre-registration was written; restricted or pre-release models are excluded. Table 1 records the verification. Claude Mythos 5.2, with the same capabilities as Claude Fable 5.2, is available only to organizations verified through Anthropic's verification programs and is therefore excluded. The programme's plan had named GPT-6.1 Terra as OpenAI's candidate; OpenAI's documentation places it two tiers below GPT-6 Astra, so the rule selects GPT-6 Astra. The budget rule allows one flagship per provider: Claude Fable 5.2 and Claude Opus 5.5 are both active, the rule selects the newer, Claude Fable 5.2, and Claude Opus 5.5 was not collected. Cheaper tiers were not used, because every question of the study concerns the newest flagship models.

Table: Panel N3, as verified on 10 November 2026 from each vendor's documentation (pre-registration §4.3).

| Provider | Model (requested ID) | Verification |
|:--------|:------------------|:-----------------------------------------|
| Anthropic | Claude Fable 5.2 (`claude-fable-5-2`) | Model page: "Active (latest)", released 9 November 2026, retirement not sooner than 9 November 2027 |
| OpenAI | GPT-6 Astra (`gpt-6-astra`) | Model page: "Our most capable model for the most demanding work"; no dated snapshot listed |
| Google | Gemini 4 Argon (`gemini-4-argon`) | Changelog: generally available on 13 October 2026; listed as stable; no newer stable model listed |

The legacy panel L6 at $t_3$ comprises Claude Opus 4.5, Claude Sonnet 4.5, GPT-4o, GPT-4o mini, Gemini 2.5 Flash and Gemini 2.5 Flash-Lite.

## 2.3 Probes

The probe file (`osf/v42/prereg/probes_v0_42.jsonl`, 142 lines: Phase A 112, Phase B 30) was built by running each legacy runner's own prompt-building code with the provider call stubbed out, so that no probe was retyped; no probe carries a system prompt. Phase A for v0.19--v0.22 asks whether a named brand is commonly recognized as a brand of the category and asks for yes or no; Phase A for v0.23 asks an open question about the brand. Phase B asks six category questions per substrate; v0.23 uses three expert-acclaim and three cultural-community frames. Parity with $t_3$ was verified before the lock (gate P3): for v0.20--v0.23 every prompt recorded at $t_3$ (720 of 720 records) equals the exported prompt byte for byte; v0.19 recorded no prompt text at $t_3$, and its parity rests on the artefact checksums (8 of 8 match) and on the query identifiers (the 132 recorded identifiers equal the artefact's).

## 2.4 Conditions, decoding and call policy

In S1 each provider's own web search was configured as follows (Anthropic `web_search_20250305`, at most 5 uses; OpenAI Responses API `web_search`, search context size medium, sources included; Google Search grounding), and every search query, consulted source and citation was recorded. Temperature, top-p and reasoning effort were left at provider defaults; Claude Fable 5.2 accepts no temperature, top-p or top-k, and its adaptive thinking is always on. The maximum output was 16,384 tokens. Claude Fable 5.2 was sent through Anthropic's Message Batches API with exactly the parameters of the synchronous call; GPT-6 Astra and Gemini 4 Argon were called synchronously. Synchronous calls with transient errors or empty answers were retried under the programme's standing retry policy; batched requests that ended with a transient error type or expired were re-sent, up to 3 attempts in all, and an empty answer was re-sent once. An Anthropic `pause_turn` was continued once with identical tools, and calls still failing after the main pass received one logged re-run pass inside the window.

The legacy runners used temperature 0.0 where they set it, output caps of 64 to 2,048 tokens, no tools and, for v0.19--v0.22, a now-deprecated Google SDK. Those settings do not carry over. The generation contrast is therefore a contrast of model generation together with its default serving settings, as a user meets it.

## 2.5 Budget and its guard

The programme caps paid model calls at US\$100 per paper, including re-sends and the v0.23 recognition judge. The pre-registration estimated the design at US\$64 (central) and US\$136 (high) at the list prices read on 10 November 2026. A guard computed spend from the recorded usage of every billed request. No request was sent if spend, open reservations and its own worst case would exceed US\$100; once spend reached US\$80, no new request started without the pre-registrant's recorded approval; and after the first search-on run, if spend plus twice that block's cost exceeded US\$100, collection paused before the second and third search-on runs for the pre-registrant's decision.

## 2.6 Coding

Mentions in Phase B answers were coded by each substrate's certified function, unchanged: for v0.20--v0.22 the content module's `detect_mention`, for v0.19 the parser of `acquire_v0_19`, and for v0.23 the deterministic brand matching of `score_v0_23.score_phase_b` (its optional language-model elaboration step enters no statistic and was not run). Coding applies to the visible answer text. In both conditions URLs are removed before matching (`https?://` addresses and the targets of Markdown links; link text is kept), so a brand counts only when the answer names it, not when a cited address contains it. Recognition (Phase A, S0, run 1) was coded by the same yes/no parsers as at $t_1$--$t_3$ for v0.19--v0.22 and, for v0.23, by the $t_1$--$t_3$ recognition judge (Claude Sonnet 4.5; 72 judge calls, which are coding, not acquisition). Claude Sonnet 4.5 is not served to the Anthropic organization the study used from its re-run pass on (§3.1): a first coding attempt on 11 November 2026 returned a not-found error for every judge call, none of them billed, and its tables were set aside. With the pre-registrant's decision, the judge was called through the Anthropic organization that coded $t_1$--$t_3$ and had served the first six Claude Fable 5.2 batches, with the same model, code and prompts, and coded 72 of 72 answers. The coder (`code_t4_v0_42.py`, git blob `2d36735d`) was fixed before the lock.

## 2.7 Measures and statistics

$k_{b,m,r}$ is the number of the six Phase B questions of brand $b$'s substrate in which model $m$'s answer in run $r$ mentions $b$; at $t_3$ it is the locked v0.41 count (one run). Recall Presence of brand $b$ on panel $P$ is

$$
\hat\pi_{b,P} = \frac{\sum_{m \in P}\sum_{r} k_{b,m,r}}{6\,|P|\,R},
$$

with $R$ runs and the answered calls as the denominator. Consistency is the v1.8 statistic, computed per run,

$$
\varphi_{b,P,r} = \frac{1}{M-1}\sum_{m \in P} \frac{\left(k_{b,m,r} - 6\hat\pi\right)^2}{6\hat\pi(1-\hat\pi)}, \qquad M = |P|,
$$

with $\hat\pi$ the run's recall rate and the locked partitions ($\hat\pi = 0$: zero; $\hat\pi = 1$: saturated; otherwise defined); higher $\varphi$ means less agreement between models. At $t_4$, $\varphi_{b,N3}$ is the mean of $\varphi_{b,N3,r}$ over the runs whose partition is defined, and is undefined if fewer than 2 of the 3 runs are defined. At $t_3$ it is the locked v0.41 value on the defined partition.

Every test uses the pooled within-substrate Spearman correlation $\rho_{\text{pw}}(x, y)$: values are ranked within substrate (average ranks for ties), each substrate's ranks are centred on that substrate's mean rank, and Pearson's $r$ is taken over all brands pooled. v0.41's uncentred version is reported beside every $\rho_{\text{pw}}$ for comparability and gates nothing; the two coincide when all substrates have the same number of brands. Permutation $p$-values are one-sided: $y$ is shuffled within substrate and $\rho_{\text{pw}}$ is recomputed exactly as observed on each of 10,000 draws, with $p = (1 + \#\{\rho_{\text{perm}} \geq \rho_{\text{obs}}\}) / 10{,}001$. Intervals are percentile 95% intervals from 10,000 bootstrap resamples of brands within substrate. Seeds were fixed in the pre-registration (420041, 420043, 420044 and 420045; 420042 belonged to the removed hypothesis and is retired). Each test uses $\alpha = .05$ without multiplicity correction; verdicts rest on pre-set effect-size thresholds, and every test is reported.

## 2.8 Hypotheses and decision rules

`H_Gen_Presence` (primary). On the newest models (N3, S0, $t_4$), recall Presence orders brands as it did on the retiring panel (L6, $t_3$). $x = \hat\pi_{b,L6}$ at $t_3$ and $y = \hat\pi_{b,N3,S0}$ at $t_4$ (three runs), over all 112 brands; $\rho_{\text{gen}} = \rho_{\text{pw}}(x, y)$. CONFIRMED if $\rho_{\text{gen}} \geq 0.70$ and $p < .05$; FALSIFIED if $\rho_{\text{gen}} < 0.50$; MARGINAL otherwise. The bar of 0.70 is the programme's stability bar (v0.34). Because the legacy panel held 0.93--0.98 over five months (v0.41), a value below 0.70 across a few days is attributable to the change of model generation, not to time; below 0.50 the two generations order brands too differently for the legacy record to be bridged quantitatively, and the new panel starts its own series. Reported alongside: per-substrate $\rho$; the same test with S1 in place of S0; per-provider generation pairs, each the $\rho_{\text{pw}}$ between the provider's two legacy models pooled and its new model; and the level shift $\Delta = \text{mean}(y - x)$ with its interval.

`H_Gen_Phi` (secondary). On N3 in S0, $\varphi$ orders brands as it did on L6 at $t_3$, over the brands with $\varphi$ defined on both. UNDETERMINED if $n < 40$; CONFIRMED if $\rho \geq 0.50$ and $p < .05$; FALSIFIED if $\rho < 0.30$; MARGINAL otherwise (the thresholds and $n$ floor of v0.41's long-horizon Consistency test). $\varphi$ on three models carries less information per brand than on six, which is why the test is secondary. Reported alongside: mean-independence on N3, $|\rho_{\text{pw}}(\varphi, \hat\pi)|$, flagged if at least 0.50 (the v1.7 ceiling), and the partition counts per condition.

`H_Search_Presence` (secondary, two-sided). Turning on each provider's web search leaves the Presence ordering of brands intact. On N3, $x = \hat\pi_{b,N3,S0}$ and $y = \hat\pi_{b,N3,S1}$ (three runs each); $\rho_S = \rho_{\text{pw}}(x, y)$ with its bootstrap interval, and the level shift $\Delta = \text{mean}(y - x)$ with its interval. The pre-declared labels carry no confirmation or falsification: search-robust if the interval's lower bound is at least 0.80, search-dominated if its upper bound is below 0.50, search-sensitive otherwise. Reported alongside: per model and per substrate.

The first draft of the pre-registration (r1) carried a second primary hypothesis, `H_Version_Presence` (Claude Fable 5.2 against Claude Opus 5.5). It needs both models side by side, which the budget rule excludes; revision r2 removed it before the lock, and no other hypothesis depends on it.

Six descriptives were pre-registered without verdicts: (1) run-to-run reliability per model and condition, rel1 (the mean of $\rho_{\text{pw}}$ over the three run pairs of $k_{b,m,r}/6$) and rel3 $= 3\,\text{rel1}/(1 + 2\,\text{rel1})$; (2) the share of brands coded as recognized, per model in S0, beside each legacy model at $t_3$; (3) floor persistence: of the brands below v0.41's recall floor at $t_3$ (mean $k$ per model below 1), the share still below it on N3 in S0 at $t_4$ (mean $k$ per model-run below 1), and the reverse; (4) answer form; (5) search records in S1; (6) tokens, searches and spend from the recorded usage of every billed request.

## 2.9 Manipulation checks, parity gates and missing data

`MC_Complete` requires at least 98% of the 876 calls to end with non-empty answer text after the retry policy. `MC_Served` requires every served model ID to equal the requested ID, a dated snapshot of it being accepted; any other call is excluded. `MC_Search` is the share of S1 calls with at least one web search, per model; below 25% flags that model's S1 as "search rarely used" in every S1 result. `MC_Truncation` is the share of calls ending at the output cap, per model and condition; above 5% is flagged. `MC_Window` requires all calls within 72 hours. `MC_Budget` requires spend from recorded usage, including the judge reserve, to stay at or below US\$100. `MC_Parity` requires three gates to pass before any $t_4$ statistic is computed: P1, the scorer, run on the locked $t_3$ data, reproduces v0.41's $k$, $\hat\pi$ and $\varphi$ for all 112 brands exactly; P2, the $t_4$ coder, applied to the $t_3$ raw answers, reproduces the locked $t_3$ mention and recognition codes exactly; and P3, probe parity (§2.3). A failed gate stops scoring.

A model × condition with fewer than 90% of its calls answered after the re-run pass (S0: 202 calls per model; S1: 90) is excluded from that condition's panel statistics. `H_Gen_Presence` and `H_Gen_Phi` need all three N3 models in S0; if any is excluded, both are UNDETERMINED. Their S1 variant and `H_Search_Presence` use the N3 models retained in the conditions concerned, flagged as a reduced panel. Calls not sent because of a budget stop count as unanswered, rates use the answered calls as the denominator, and a model-run missing a Phase B answer in a substrate yields no $\varphi$ for that substrate's brands in that run. There is no imputation.

## 2.10 Pre-registration

The pre-registration (revision r2, with clarifications C1--C28) was locked at git tag `v0.42-prereg-r1` (commit `58d1891bf2`) and deposited on OSF (`ec6wh`, `v42/prereg/`) with an anchor record naming the tag's commit before any study probe was sent; the collection script refused to run until the tag was on the remote repository and the anchor existed. The lock procedure provided a 24-hour review period after the last change to a decision rule (C25); the pre-registrant waived it on 10 November 2026 (20:26 US Central time), and the tag was set on 11 November 2026 at 02:52 UTC. OSF's file records date the deposit of the locked files to 02:53--02:55 UTC and that of the anchor record to 02:55 UTC, before the first call (2026-11-11 02:57 UTC; §3.1). Revision r2 replaced the first draft under the programme's collection budget rule (at most US\$100 of paid model calls per paper): one flagship per provider, Phase A in S0 with one run, and the removal of `H_Version_Presence` (clarifications C10--C24). Clarification C25, made before the lock, changed the decision statistic to the centred $\rho_{\text{pw}}$ of §2.7: v0.41's uncentred version is inflated by between-substrate differences in mean rank when substrates differ in size (16 against 24 brands), with a mean of +0.0464 under independence on the 112 brands; thresholds, rules and seeds were unchanged. Clarification C26 made the collection script enforce the one-collection rule and the window and record every billed batch request. Clarifications C27 and C28, made before the lock after a dry run of the whole chain on simulated provider responses, made the brand table's columns for panel N3 always use all three models (the component papers recompute them on all three), made descriptive 5 name the source of a Gemini grounding redirect by its host name instead of counting the redirect address as one domain, and made the budget guard and descriptive 6 count billed usage they had missed (OpenAI page-open and find-in-page actions, Gemini search-result tokens), in the conservative direction; neither changed a hypothesis, threshold or decision rule. The scorer (`score_v0_42.py`) and the coder were written and tested on synthetic data before the lock, and the scorer was run once, after the parity gates. Deviations are recorded in `osf/v42/DEVIATIONS.md` (1 entry), each before the step it concerns.

# 3. Results

## 3.1 Parity gates and manipulation checks

All three parity gates passed before any $t_4$ statistic was computed (P1, P2 and P3).
876 of the 876 design calls were answered (100.0%), and `MC_Complete` passed. Table 2 gives the counts per model and condition. No model × condition fell below the 90% floor, so no model was dropped. `MC_Served` passed: every answered call was served by the requested model or a dated snapshot of it.  

`MC_Search` flagged Gemini 4 Argon: search was used in fewer than 25% of its S1 calls, and its S1 results are marked "search rarely used" throughout (by $^{\dagger}$ in the tables, and in the captions of the tables and figures whose search-on values include it). No model × condition ended more than 5% of its calls at the output cap (`MC_Truncation`). The first call started at 2026-11-11 02:57 and the last ended at 2026-11-11 09:50 (UTC), a span of 6.9 hours, and `MC_Window` passed. Recorded spend on all billed requests, at the list prices of the pre-registration, was \$67.46, or \$67.96 with the \$0.50 reserve for the recognition judge, and `MC_Budget` passed. No pause approval was recorded by the budget guard. The raw file holds one record per attempt: 990 records for the 876 calls. The 114 additional records (30 for Claude Fable 5.2 with search on, 6 for Gemini 4 Argon with search off and 78 for Gemini 4 Argon with search on) are attempts that the providers refused, without an answer and without billed usage, when an account balance ran out: Anthropic declined to create the seventh Claude Fable 5.2 batch (the 30 calls of the third search-on run) for insufficient credit, and Google refused 84 Gemini 4 Argon calls because the prepaid credits were depleted. The main pass ended in block 7 with these calls unanswered. After the balances were restored, and with the study's Anthropic requests moved to a new organization, the one logged re-run pass (§2.4) answered all 114 between 09:05 and 09:50 UTC, so six Gemini 4 Argon recognition answers were completed after the search-on blocks had begun (§2.1). Each call is analysed once, from its answered attempt.

Table: Calls answered, output-cap endings and search use, by model and condition. Answered: status ok, non-empty text and an accepted served ID; expected: 202 (S0) and 90 (S1) per model. $^{\dagger}$ Search rarely used (`MC_Search`, §3.1).

| Model | Cond. | Answered / expected | Share | Drop rule | At output cap | With search |
|:--------------------|:-----|-------------------:|------:|:---------|-------------:|-----------:|
| Claude Fable 5.2 | S0 | 202 / 202 | 100.0% | retained | 0.0% | n/a |
| Claude Fable 5.2 | S1 | 90 / 90 | 100.0% | retained | 0.0% | 83.3% |
| GPT-6 Astra | S0 | 202 / 202 | 100.0% | retained | 0.0% | n/a |
| GPT-6 Astra | S1 | 90 / 90 | 100.0% | retained | 0.0% | 95.6% |
| Gemini 4 Argon | S0 | 202 / 202 | 100.0% | retained | 0.0% | n/a |
| Gemini 4 Argon$^{\dagger}$ | S1 | 90 / 90 | 100.0% | retained | 0.0% | 17.8% |

## 3.2 Cross-generation stability of Presence (`H_Gen_Presence`)

Across the 112 brands, recall Presence on the newest models with search off correlated with recall Presence on the retiring panel at $\rho_{\text{pw}} = 0.828$ (95% interval 0.722 to 0.890; one-sided $p_{\text{perm}} = 0.0001$ from 10,000 draws); v0.41's uncentred statistic gives 0.836. The level shift was $\Delta = +0.046$ (95% interval +0.023 to +0.071): on average the newest models named a brand in a larger share of category answers than the retiring panel.
The correlation meets both conditions of the confirmation rule ($\rho_{\text{gen}} \geq 0.70$ and $p < .05$), and the verdict is **CONFIRMED**.

With search on in place of search off, the same comparison gives $\rho_{\text{pw}} = 0.796$ (95% interval 0.669 to 0.861; $p_{\text{perm}} = 0.0001$), which would read CONFIRMED under the primary rule; this variant is reported alongside and decides nothing. Per provider, the legacy pair pooled against its new model gives $\rho_{\text{pw}} = 0.848$ for Anthropic (Claude Opus 4.5 + Claude Sonnet 4.5 against Claude Fable 5.2); $\rho_{\text{pw}} = 0.566$ for OpenAI (GPT-4o + GPT-4o mini against GPT-6 Astra); and $\rho_{\text{pw}} = 0.715$ for Google (Gemini 2.5 Flash + Flash-Lite against Gemini 4 Argon). Table 3 gives the per-substrate correlations and Figure 1 the per-brand values.

Table: Recall Presence, $t_3$ (retiring panel) against $t_4$ (newest models), Spearman $\rho$ within each substrate, search off (primary test) and search on (reported alongside). Search-on values include the answers of Gemini 4 Argon, marked "search rarely used" (§3.1).

| Substrate | Brands | $\rho$, search off | $\rho$, search on |
|:----------------------|------:|-------------:|------------:|
| Headphones (v0.19) | 16 | 0.911 | 0.949 |
| Skincare (v0.20) | 24 | 0.888 | 0.878 |
| Cosmetics (v0.21) | 24 | 0.855 | 0.801 |
| Automotive (v0.22) | 24 | 0.943 | 0.923 |
| Spirits (v0.23) | 24 | 0.607 | 0.540 |

![Per-brand recall Presence on the retiring panel at $t_3$ against the newest models with search off at $t_4$ (mean of three runs), coloured by substrate; dashed line = equal values. Test statistics in §3.2.](../../reports/figs/v42/chart_01_presence_t3_t4.pdf){#fig:gen width=100%}

## 3.3 Cross-generation stability of Consistency (`H_Gen_Phi`)

73 brands had $\varphi$ defined on both panels (10 headphones, 14 skincare, 17 cosmetics, 15 automotive and 17 spirits).
Their $\varphi$ values on the newest models with search off correlated with their $t_3$ values at $\rho_{\text{pw}} = 0.310$ (95% interval 0.051 to 0.520; one-sided $p_{\text{perm}} = 0.0056$); v0.41's uncentred statistic gives 0.355.
The correlation does not meet the confirmation rule ($\rho \geq 0.50$ with $p < .05$) and is not below the falsification bar of 0.30, and the verdict is **MARGINAL**.

On the newest models with search off, 79 brands had $\varphi$ defined, 25 were in the zero partition in every run, 2 in the saturated partition in every run and 6 were undefined (fewer than two defined runs); with search on, 83 brands had $\varphi$ defined, 22 were in the zero partition in every run, 0 in the saturated partition in every run and 7 were undefined (fewer than two defined runs); at $t_3$, 83 of the 112 brands had $\varphi$ defined on the retiring panel. On N3 with search off, $|\rho_{\text{pw}}(\varphi, \hat\pi)| = 0.101$ ($n = 79$; uncentred -0.014), below the v1.7 ceiling of 0.50, so the mean-independence flag is not raised. Table 4 gives the per-substrate correlations and Figure 2 the per-brand values.

Table: Consistency $\varphi$, $t_3$ against $t_4$ (newest models, search off), Spearman $\rho$ within each substrate, over brands with $\varphi$ defined on both panels.

| Substrate | Brands ($\varphi$ defined on both) | $\rho$ |
|:----------------------|--------------------------:|-----:|
| Headphones (v0.19) | 10 | 0.492 |
| Skincare (v0.20) | 14 | 0.075 |
| Cosmetics (v0.21) | 17 | 0.058 |
| Automotive (v0.22) | 15 | 0.809 |
| Spirits (v0.23) | 17 | 0.312 |

![Per-brand $\varphi$ on the retiring panel at $t_3$ against the newest models with search off at $t_4$ (mean over defined runs), brands with $\varphi$ defined on both; dashed line = equal values. Test statistics in §3.3.](../../reports/figs/v42/chart_02_phi_t3_t4.pdf){#fig:phi width=100%}

## 3.4 Web search and Presence (`H_Search_Presence`)

On Claude Fable 5.2, GPT-6 Astra and Gemini 4 Argon, recall Presence with search on correlated with recall Presence with search off at $\rho_S = 0.909$ across 112 brands (95% interval 0.827 to 0.945; uncentred 0.913). The level shift was $\Delta = -0.041$ (95% interval -0.057 to -0.025).
The interval's lower bound is at least 0.80, and the pre-declared label is **search-robust**.
The search-on answers of Gemini 4 Argon are flagged "search rarely used" (§3.1). Table 5 gives the result per model. Within substrate, the Spearman correlation between search off and search on was headphones 0.956, skincare 0.930, cosmetics 0.932, automotive 0.976 and spirits 0.785. Figure 3 shows the per-brand values.

Table: Recall Presence with search off against search on, per model (newest models, three runs each). $^{\dagger}$ Search rarely used (`MC_Search`, §3.1).

| Model | Brands | $\rho_{\text{pw}}$ | Uncentred (v0.41) | $\Delta$ (on minus off) |
|:--------------------|------:|-----:|-----------------:|----------------:|
| Claude Fable 5.2 | 112 | 0.710 | 0.723 | -0.052 |
| GPT-6 Astra | 112 | 0.858 | 0.865 | -0.058 |
| Gemini 4 Argon$^{\dagger}$ | 112 | 0.909 | 0.913 | -0.012 |

![Left: per-brand recall Presence on the newest models with search off and on (mean of three runs each). Right: $\rho_S$ with its 95% interval and the correlation per model and per substrate, against the pre-declared zones. Statistics in §3.4. Search-on values include the answers of Gemini 4 Argon, marked "search rarely used" (§3.1).](../../reports/figs/v42/chart_03_search_s0_s1.pdf){#fig:search width=100%}

## 3.5 Pre-registered descriptives

**Run-to-run reliability.** Table 6 and Figure 4 give rel1 and rel3 per model and condition: rel1 ranged from 0.845 to 0.915 and rel3 from 0.942 to 0.970. Recognition agreement across runs is not computed, because Phase A has one run in revision r2.

Table: Run-to-run reliability of recall per model and condition (descriptive 1). rel1: mean $\rho_{\text{pw}}$ over the three run pairs; rel3: the reliability of the three-run mean. $^{\dagger}$ Search rarely used (`MC_Search`, §3.1).

| Model | Cond. | rel1 | rel3 | rel1, uncentred (v0.41) |
|:--------------------|:-----|-----:|-----:|-----------------------:|
| Claude Fable 5.2 | S0 | 0.912 | 0.969 | 0.916 |
| Claude Fable 5.2 | S1 | 0.897 | 0.963 | 0.902 |
| GPT-6 Astra | S0 | 0.904 | 0.966 | 0.909 |
| GPT-6 Astra | S1 | 0.845 | 0.942 | 0.853 |
| Gemini 4 Argon | S0 | 0.880 | 0.956 | 0.885 |
| Gemini 4 Argon$^{\dagger}$ | S1 | 0.915 | 0.970 | 0.919 |

![rel1 (one run against another) and rel3 (mean of three runs) per model and condition. Descriptive; no verdict. Search-on values include the answers of Gemini 4 Argon, marked "search rarely used" (§3.1).](../../reports/figs/v42/chart_04_run_reliability.pdf){#fig:rel width=100%}

**Recognition.** Table 7 gives the share of brands coded as recognized by each model with search off at $t_4$, beside each legacy model at $t_3$. Shares use the answers that could be coded as the denominator; recognition is not computed for search on, which r2 does not collect.

Table: Share of the 112 brands coded as recognized (descriptive 2): newest models at $t_4$ (search off, one run) and legacy models at $t_3$.

| Model | Wave | Recognized | Coded | Share |
|:-------------------------|:-------------|----------:|-----:|-----:|
| Claude Fable 5.2 | $t_4$, search off | 109 | 112 | 97.3% |
| GPT-6 Astra | $t_4$, search off | 111 | 112 | 99.1% |
| Gemini 4 Argon | $t_4$, search off | 111 | 112 | 99.1% |
| Claude Opus 4.5 | $t_3$ | 108 | 112 | 96.4% |
| Claude Sonnet 4.5 | $t_3$ | 103 | 112 | 92.0% |
| GPT-4o | $t_3$ | 108 | 112 | 96.4% |
| GPT-4o mini | $t_3$ | 110 | 112 | 98.2% |
| Gemini 2.5 Flash | $t_3$ | 104 | 112 | 92.9% |
| Gemini 2.5 Flash-Lite | $t_3$ | 106 | 112 | 94.6% |

**Floor persistence.** Of the 58 brands below the recall floor at $t_3$, 43 were still below it on the newest models with search off at $t_4$ (74%). Of the 49 brands below the floor at $t_4$, 43 had been below it at $t_3$ (88%), and 11% of the brands above the floor at $t_3$ fell below it at $t_4$ (Figure 5; clarification C2).

![Brands below the recall floor at $t_3$ (mean $k$ per model below 1) and at $t_4$ (newest models, search off; mean $k$ per model-run below 1). Counts in §3.5.](../../reports/figs/v42/chart_05_floor.pdf){#fig:floor width=100%}

**Answer form, search records and cost.** Tables 8 to 10 report the remaining descriptives: words per answer, registry brands named per Phase B answer, finish reasons and non-answers (descriptive 4); searches, sources and citations per S1 call (descriptive 5, with the 20 most-cited domains per model in Appendix Table 11); and tokens, searches and spend per model and condition from the recorded usage (descriptive 6). Every v0.19--v0.22 Phase A answer contained a yes or a no, no answered call ended with a refusal finish reason, and no call ended unanswered, so the two categories into which `osf/v42/DEVIATIONS.md` (Entry 1) splits unanswered calls (a GPT-6 Astra answer that is empty, refusal or blank; a Gemini 4 Argon call with no candidate) are both empty. Refusal counts are lower bounds (Entry 1).

Table: Answer form per model and condition (descriptive 4). Words: mean words per Phase A and Phase B answer; brands per B: registry brands named per Phase B answer; non-answers: Phase A answers (v0.19--v0.22) with no yes or no; refusals: by finish reason; unanswered: error or empty after the retry policy. $^{\dagger}$ Search rarely used (`MC_Search`, §3.1).

| Model | Cond. | Words (A) | Words (B) | Brands per B | Finish reasons | Non-answers / refusals / unanswered |
|:--------------------|:-----|---------:|---------:|------------:|:---------------------|-----------------------------------:|
| Claude Fable 5.2 | S0 | 160.8 | 290.8 | 6.2 | end\_turn 202 | 0 / 0 / 0 |
| Claude Fable 5.2 | S1 | -- | 282.3 | 5.0 | end\_turn 90 | 0 / 0 / 0 |
| GPT-6 Astra | S0 | 490.5 | 431.1 | 5.5 | completed 202 | 0 / 0 / 0 |
| GPT-6 Astra | S1 | -- | 380.7 | 4.2 | completed 90 | 0 / 0 / 0 |
| Gemini 4 Argon | S0 | 258.3 | 820.7 | 6.6 | FinishReason.STOP 202 | 0 / 0 / 0 |
| Gemini 4 Argon$^{\dagger}$ | S1 | -- | 858.1 | 6.3 | FinishReason.STOP 90 | 0 / 0 / 0 |

Table: Search records per model, answered S1 calls (descriptive 5). $^{\dagger}$ Search rarely used (`MC_Search`, §3.1).

| Model | S1 calls | Searches per call | Sources per call | Citations per call | With a citation |
|:--------------------|--------:|-----------------:|----------------:|------------------:|---------------:|
| Claude Fable 5.2 | 90 | 1.7 | 15.6 | 11.1 | 83% |
| GPT-6 Astra | 90 | 2.6 | 92.5 | 8.2 | 96% |
| Gemini 4 Argon$^{\dagger}$ | 90 | 0.4 | 1.7 | 3.9 | 18% |

Table: Recorded usage and spend per model and condition (descriptive 6), all billed requests at the list prices of the pre-registration; the v0.23 recognition judge is not in the raw file and is covered by its reserve. $^{\dagger}$ Search rarely used (`MC_Search`, §3.1).

| Model | Cond. | Billed requests | Input tokens | Output tokens | Searches | US\$ |
|:--------------------|:-----|---------------:|------------:|-------------:|--------:|-------:|
| Claude Fable 5.2 | S0 | 202 | 9,473 | 220,552 | 0 | \$4.45 |
| Claude Fable 5.2 | S1 | 90 | 1,989,632 | 312,023 | 153 | \$15.73 |
| GPT-6 Astra | S0 | 202 | 5,705 | 167,855 | 0 | \$8.45 |
| GPT-6 Astra | S1 | 90 | 2,740,428 | 100,167 | 297 | \$35.38 |
| Gemini 4 Argon | S0 | 202 | 10,813 | 162,569 | 0 | \$1.65 |
| Gemini 4 Argon$^{\dagger}$ | S1 | 90 | 21,360 | 125,075 | 36 | \$1.80 |
| All |  |  |  |  |  | \$67.46 |

# 4. Discussion

The primary result is that the ordering of brands by recall Presence carried over from the retiring model generation to the newest flagship models ($\rho_{\text{pw}} = 0.828$, 95% interval 0.722 to 0.890). Under the pre-registered rationale, the programme's record on the legacy panel can therefore be bridged to the new panel for Presence: the brand standings measured since May 2026 remain interpretable on current models. The bridge is an ordering, not a level. The newest models named the average brand in a larger share of category answers ($\Delta = +0.046$), so comparisons of absolute Presence across the change of panel would need to account for the shift. The study does not explain it: answer length is a descriptive of the $t_4$ answers only (Table 8), not of the legacy answers.

The bridge is not uniform. Four substrates kept their order closely (per-substrate $\rho$ from 0.855 to 0.943 with search off), while premium spirits reached 0.607. The spirits substrate is also the only one whose category questions include no direct request for the best (the other four each open with "What are the best ...?"): its six questions ask which brands critics, competitions, bartenders and enthusiast communities favour, which have become cultural phenomena and which are hidden gems not yet mainstream (§2.3). Such frames may leave a new generation more room to choose differently; the design does not test this. Per provider, the legacy pair against its new model gave $\rho_{\text{pw}} = 0.848$ for Anthropic, 0.715 for Google and 0.566 for OpenAI. These single-model comparisons are reported alongside and decide nothing, and one model's Presence rests on fewer answers than the panel's. Still, for OpenAI and Google a user of the provider's newest model meets a brand order that departs further from that provider's legacy models (0.566 and 0.715) than the three-model panel departs from the six-model panel (0.828), most of all for OpenAI; for Anthropic the pair agrees slightly more closely than the panels (0.848).

For Consistency the result is intermediate and close to the falsification bar: $\rho_{\text{pw}} = 0.310$ against a bar of 0.30, with a 95% interval (0.051 to 0.520) that reaches below the falsification bar and above the confirmation bar. The permutation $p$-value (0.0056) indicates more agreement between the two generations' $\varphi$ orderings than chance would give, but the pre-registered effect-size rule decides, and the data neither support nor rule out a quantitative bridge for $\varphi$. The per-substrate correlations range widely, from 0.058 (cosmetics) and 0.075 (skincare) to 0.809 (automotive), each on 10 to 17 brands. With three models $\varphi$ carries less information per brand than with six (§2.8), so part of the shortfall may reflect the smaller panel rather than the change of generation; the design cannot separate the two. On the new panel $\varphi$ did not track Presence ($|\rho_{\text{pw}}(\varphi, \hat\pi)| = 0.101$), so the weak carry-over is not a by-product of the Presence result.

Web search left the panel's Presence ordering intact ($\rho_S = 0.909$; the interval's lower bound, 0.827, clears the 0.80 bar). Two qualifications bound this reading. First, it describes the three-model mean. Per model, the correlation between search off and search on was 0.909 for Gemini 4 Argon, 0.858 for GPT-6 Astra and 0.710 for Claude Fable 5.2. For Claude Fable 5.2 this is well below the reliability of a three-run mean in either condition (rel3 0.969 with search off and 0.963 with search on), which suggests that its search reorders brands beyond run-to-run noise. Second, Gemini 4 Argon searched in 17.8% of its search-on calls, so most of its search-on answers are close to a further search-off run; it contributes the highest per-model correlation and the smallest level shift ($\Delta = -0.012$). Where search was used on most calls, it lowered Presence ($\Delta = -0.052$ for Claude Fable 5.2 and $-0.058$ for GPT-6 Astra) and the number of registry brands named per category answer (from 6.2 to 5.0 and from 5.5 to 4.2). The pre-registered label therefore holds for the panel as collected, not for every model's use of search.

The run-to-run reliabilities of §3.5 set the noise floor of the new panel's series: rel1 from 0.845 to 0.915 and rel3 from 0.942 to 0.970 across models and conditions. A correlation between the three-run means of two waves in the range of rel3 would be consistent with no change in brand order beyond the variation recorded here between runs of the same model on the same questions; the $t_5$ and $t_6$ waves are to be read against these values.

Brands with little Presence mostly stayed so: of the 58 brands below the recall floor on the retiring panel, 43 (74%) were still below it on the newest models, and 11% of the brands above the floor fell below it. Fewer brands were below the floor at $t_4$ (49) than at $t_3$ (58), in line with the upward level shift.

# 5. Limitations

Model generation is confounded with serving settings (temperature, output cap, thinking) and with knowledge cut-off, so `H_Gen_Presence` tests the bundle as a user meets it. There is one model per provider and therefore no within-provider replication at $t_4$. Three runs estimate run-to-run noise only coarsely, and $\varphi$ on three models is noisier than on six. Search-on answers depend on the web on the day and are reproducible only as recorded. The study covers one market and language (US English) and five categories chosen in May 2026. $t_3$ and $t_4$ are a few days apart, not simultaneous. Claude Fable 5.2 was sent through Anthropic's Message Batches API and the other two models synchronously; the batch requests carried the same parameters as the synchronous calls, but the serving path differs. Recognition rests on one Phase A run per model, in S0 only. Claude Fable 5.2's cost per call was estimated from another model's before collection, which is why the budget guard could have ended the collection before the second and third search-on runs; in the event, every search-on call was answered. The search-on results of Gemini 4 Argon rest on calls that rarely searched, so the search-on condition tests search mainly through Claude Fable 5.2 and GPT-6 Astra. The per-provider generation pairs and the per-model search correlations are single-model figures reported alongside, without verdicts, and the pooled results can hide differences between models. Refusal counts are lower bounds: the raw record cannot distinguish a GPT-6 Astra refusal from a blank answer, nor record why a Gemini 4 Argon prompt was blocked (`osf/v42/DEVIATIONS.md`, Entry 1). The study's Anthropic requests went through two organizations: the first six Claude Fable 5.2 batches and the v0.23 recognition judge through the organization that had coded $t_1$--$t_3$, and the seventh batch, the 30 calls of the third search-on run, through a new one, with the same model, parameters, code and prompts (§2.6, §3.1).

# 6. Future Research

The $t_5$ (target 3 December 2026) and $t_6$ (target 12 February 2027) waves re-ask the same probes to the same three model IDs with the same design, conditions, runs, call modes, call policy and budget guard, each under its own pre-registration and its own budget; the run-to-run reliabilities reported here are the noise floor they will be read against. Claude Sonnet 4.5, the v0.23 recognition judge, retires on 30 November 2026, so $t_5$ needs a successor judge with a parity check against the $t_4$ codes. The stored $t_4$ answers and search records are the corpus of the programme's Ranking, Sentiment, Coverage and Grounding components, each of which declares its use of them in its own pre-registration before computing anything from them.

# Declarations {-}

## Conflict of interest {-}

The author is Director, Corporate Brand Creative and Governance at Samsung Electronics America. This study re-asks questions against brand registries fixed in earlier phases (v0.19--v0.23); it performs no new brand selection, and each registry carries its source-phase conflict-of-interest handling forward unchanged. Two items of record apply. In the automotive registry, Samsung subsidiaries hold tier-2/3 component supply relationships with several registry brands --- Harman International (audio systems), Samsung SDI (battery cells), and Samsung Display (infotainment) --- characterized in the source phase as non-competitive, with no brand-level overlap, and imposing no operational restriction on registry composition (v0.22 Declarations; screened in v0.22 DEVIATIONS Entry 0, Part B). In the audiophile-headphones registry, AKG was substituted with Denon before the v0.19 pre-registration lock because AKG's parent, Harman International, is a Samsung subsidiary. Correction (November 10, 2026): Harman International, a Samsung subsidiary since March 2017, completed its acquisition of Masimo's Sound United brands, Denon included, on September 23, 2025. Denon, substituted for AKG before the v0.19 lock, was therefore already a Samsung-group brand, and the v0.19 headphones registry includes one Samsung-group brand. The substitution did not achieve its purpose, and this was not noticed until November 10, 2026. Cheil Worldwide, a marketing company of the Samsung group in which Samsung Electronics holds 28.43%, or its agency Iris has done advertising, public-relations or search-marketing work for five registry brands: Chevrolet (for GM Korea, 2017), BMW (UK consumer public relations, 2018), Bentley (experiential agency of record in the Americas from 2021), Jack Daniel's (UK digital agency from 2022, since replaced) and Eucerin (search marketing for Beiersdorf from 2024) (conflict-of-interest screen of v0.62, DEVIATIONS Entry 0, Part F). Acquisition, coding and scoring are fully automated against the locked registries, and the pre-registration was locked and deposited before any $t_4$ call. Samsung Electronics had no role in the design, conduct, analysis or reporting of this work.

## Funding {-}

Self-funded. No external funding supported this research.

## Ethics {-}

Not applicable; no human subjects. The study queries large language models under their public interfaces.

## Use of AI tools {-}

During the preparation of this work the author used AI tools (Anthropic's Claude) to assist with study design, analysis and writing. The author reviewed and edited all content and takes full responsibility for it.

## Data and code availability {-}

Materials are deposited at OSF, `ec6wh/v42`: the locked pre-registration and its anchor record, the probe file, the parity, feasibility and cost-estimate records, the scripts and the lock manifest (`v42/prereg/`, `v42/anchor/`), and the deviations record (`v42/DEVIATIONS.md`). At publication the deposit adds the $t_4$ raw answers with their search records and usage, the coded tables, the verdicts (`v42_verdicts.json`), the brand table (`v42_brand_table.csv`) and the figure sources.

# References {-}

González Castro, P. U. (2026). *AI Availability: Extending Mental and Physical Availability into Algorithmic Retrieval*. SSRN 6659000.

González Castro, P. U. (2026). *The AIAS™ Presence Measurement Protocol: Methodological Notes on Construct Validity and the Four-Regime Taxonomy* (v1.2). SSRN 6761698.

González Castro, P. U. (2026). *The AIAS Presence Measurement Protocol: Phase A Pivot-Validation Specification* (v1.3). SSRN 6797679.

González Castro, P. U. (2026). *The AIAS Presence Measurement Protocol v1.4: Recognition × Recall Decomposition and Multi-Component AI Availability*. SSRN 6799479.

González Castro, P. U. (2026). *The AIAS™ Presence Measurement Protocol: Multi-Statistic C2 Specification and Two-Channel Recall Decomposition* (v1.5). SSRN 6810758.

González Castro, P. U. (2026). *Substrate Pre-Screening, Independent Moderator Pathway, and Phantom Brand Persistence Phase B Extension* (AIAS Methodology v1.6). SSRN 6816340.

González Castro, P. U. (2026). *Consistency without Independence: A Pre-Registered Test of Coefficient-of-Variation as the Consistency Component of AIAS™* (v1.7). SSRN 6878818.

González Castro, P. U. (2026). *A Mean-Independent Consistency Instrument for Cross-Model AI Presence: Redesigning CPC on a Quasi-Binomial Dispersion Basis* (AIAS Methodology v1.8). SSRN 6963359.

González Castro, P. U. (2026). *AI Availability as a Third Measurable Layer of Brand Availability: Five-Substrate Empirical Anchoring of the AIAS™ Presence Measurement Protocol* (AIAS 1.0). SSRN 6817841.

González Castro, P. U. (2026). *Two-Wave Temporal Stability of an AI Brand-Recall Consistency Quantity: A Pre-Registered Longitudinal Re-Acquisition Across Five Product Categories* (v0.34). SSRN 6915458.

González Castro, P. U. (2026). *Five-Month Stability of AI Brand Consistency and Presence: A Pre-Registered Third Wave on a Retiring Six-Model Panel* (AIAS v0.41). SSRN 7685100 (submitted November 2026); OSF `ec6wh/v41`.

González Castro, P. U. (2026). *Recognition Ceiling, Dissociation Replication, and Cultural-Channel Asymmetry on an Audiophile Headphones Substrate* (v0.19). SSRN 6809182.

González Castro, P. U. (2026). *Type 2 Emergence and First Prospective v1.5 C2 Calibration on a Skincare IL-Gradient Substrate* (v0.20). SSRN 6811441.

González Castro, P. U. (2026). *Type 2 Confirmation, Recognition Ceiling, and Phantom Brand Persistence on a Cosmetics IL-Gradient Substrate* (v0.21). SSRN 6815378.

González Castro, P. U. (2026). *Phantom Brand Persistence on a Heritage-Saturated Automotive Substrate: Cell D\_Defunct as Pure-Phantom Upper-Bound Test* (v0.22). SSRN 6829118.

González Castro, P. U. (2026). *AIAS Presence Index v0.23: Premium Spirits --- Recognition Ceiling, Recall-Driven Regime Classification, and the Conglomerate Ownership Hypothesis Across 24 Brands and Six Large Language Models*. SSRN 6834298.

Romaniuk, J., & Sharp, B. (2022). *How Brands Grow, Part 2* (Revised ed.). Oxford University Press.

Sharp, B. (2010). *How Brands Grow: What Marketers Don't Know*. Oxford University Press.

\clearpage

# Appendix {-}

Table: The 20 most-cited domains per model in the answered search-on calls (descriptive 5), with citation counts. $^{\dagger}$ Search rarely used (`MC_Search`, §3.1).

| Model | Domain (citations) |
|:--------------------|:------------------------------------------------------------|
| Claude Fable 5.2 | drinksint.com (69), ringly.io (42), thewhiskeywash.com (29), americansalon.com (28), crutchfield.com (27), globalbrandsmagazine.com (24), consumerreports.org (24), carcody.com (23), ecoustics.com (22), marieclaire.com (22), thedermdigest.com (20), rd.com (17), en.wikipedia.org (17), autoblog.com (17), wineenthusiast.com (15), vinepair.com (14), whowhatwear.com (13), cosmetify.com (13), roadethos.com (13), gobrandwave.com (12) |
| GPT-6 Astra | consumerreports.org (42), vogue.com (39), allure.com (36), vinepair.com (35), rtings.com (23), wineenthusiast.com (17), statista.com (16), stereophile.com (15), cosmetify.com (15), cosmeticsbusiness.com (14), whowhatwear.com (13), caranddriver.com (13), beautymatter.com (12), thespiritsbusiness.com (12), iwsc.net (12), aad.org (11), diarydirectory.com (10), glamour.com (10), bustle.com (10), subaru.com (10) |
| Gemini 4 Argon$^{\dagger}$ | youtube.com (65), forbes.com (21), thewhiskeywash.com (16), beautypackaging.com (16), prnewswire.com (13), hernogin.com (12), suntoryglobalspirits.com (10), newsnationnow.com (10), qz.com (8), dermstore.com (7), iwsc.net (7), ecoustics.com (7), carpro.com (7), jdpower.com (6), gravelai.com (5), artofskincare.com (5), cluboenologique.com (5), wine-searcher.com (5), suntory.com (5), theautochannel.com (5) |
