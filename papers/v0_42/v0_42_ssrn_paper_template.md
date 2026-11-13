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

Pre-registration: \texttt{ {{PREREG_TAG}} } (commit \texttt{ {{PREREG_COMMIT}} }; deposited on OSF before the first t\textsubscript{4} call)\\
Data and code: OSF \texttt{ec6wh/v42}\\

\end{center}
\end{titlepage}

# Abstract {-}

Brand measures read from the answers of large language models (LLMs) can serve as a tracking metric only if they survive the replacement of the models that produce them. This pre-registered study is the fourth wave (t₄) of the AIAS measurement programme's five-category omnibus (audiophile headphones, skincare, cosmetics, automotive and premium spirits; 112 brands) and the first on the newest generally available flagship model of each provider: Claude Fable 5.2, GPT-6 Astra and Gemini 4 Argon. The 30 category questions were asked verbatim with web search off and on, in three runs each, and the 112 brand questions once with search off (876 calls); the answers were compared with the third wave (t₃), collected on 9 November 2026 on a retiring six-model panel. {{MC_ANSWERED}} of the 876 calls were answered.
{% switch CASE_GEN %}
{% case CONFIRMED %}
Recall Presence ordered brands on the newest models as it had on the retiring panel (`H_Gen_Presence` CONFIRMED: pooled within-category ρ = {{GEN_RHO}}, 95% interval {{GEN_CI_LO}} to {{GEN_CI_HI}}, p = {{GEN_P}}, n = {{GEN_N}}).
{% case MARGINAL %}
The newest models' Presence ordering fell between the pre-registered bars (`H_Gen_Presence` MARGINAL: pooled within-category ρ = {{GEN_RHO}}, 95% interval {{GEN_CI_LO}} to {{GEN_CI_HI}}, p = {{GEN_P}}, n = {{GEN_N}}): related to the retiring panel's ordering, but not meeting the confirmation rule of ρ ≥ 0.70 with p < .05.
{% case FALSIFIED %}
The newest models did not reproduce the retiring panel's Presence ordering (`H_Gen_Presence` FALSIFIED: pooled within-category ρ = {{GEN_RHO}}, 95% interval {{GEN_CI_LO}} to {{GEN_CI_HI}}, n = {{GEN_N}}, below the pre-registered falsification bar of 0.50); under the pre-registered rationale the new panel starts its own series.
{% case UNDETERMINED_EXCLUDED %}
`H_Gen_Presence` was UNDETERMINED because {{EXCL_S0_NAMES}} answered fewer than 90% of its search-off calls; the pre-registered drop rule leaves no fallback panel.
{% case UNDETERMINED_DEGENERATE %}
`H_Gen_Presence` was UNDETERMINED because its statistic was undefined on the data.
{% endswitch %}
{% switch CASE_PHI %}
{% case CONFIRMED %}
The Consistency instrument φ kept its brand order across the change of generation (`H_Gen_Phi` CONFIRMED: ρ = {{PHI_RHO}}, p = {{PHI_P}}, n = {{PHI_N}}).
{% case MARGINAL %}
The brand order of the Consistency instrument φ fell between the pre-registered bars (`H_Gen_Phi` MARGINAL: ρ = {{PHI_RHO}}, p = {{PHI_P}}, n = {{PHI_N}}).
{% case FALSIFIED %}
The Consistency instrument φ did not keep its brand order across the change of generation (`H_Gen_Phi` FALSIFIED: ρ = {{PHI_RHO}}, below the bar of 0.30, n = {{PHI_N}}).
{% case UNDETERMINED_FLOOR %}
`H_Gen_Phi` was UNDETERMINED: φ was defined on both panels for {{PHI_N}} brands, below the pre-registered floor of 40.
{% case UNDETERMINED_EXCLUDED %}
`H_Gen_Phi` was UNDETERMINED under the same drop rule.
{% case UNDETERMINED_DEGENERATE %}
`H_Gen_Phi` was UNDETERMINED because its statistic was undefined on the data.
{% endswitch %}
{% switch CASE_SEARCH %}
{% case ROBUST %}
Turning on each provider's web search left the Presence ordering intact (search-robust: ρ = {{S_RHO}}, 95% interval {{S_CI_LO}} to {{S_CI_HI}}).
{% case SENSITIVE %}
Web search changed the Presence ordering in part (search-sensitive: ρ = {{S_RHO}}, 95% interval {{S_CI_LO}} to {{S_CI_HI}}).
{% case DOMINATED %}
Web search reordered brands by Presence (search-dominated: ρ = {{S_RHO}}, 95% interval {{S_CI_LO}} to {{S_CI_HI}}).
{% case UNDETERMINED|NOT_COMPUTED %}
The search contrast could not be read: {{S_WHY}}.
{% endswitch %}
Run-to-run reliability of recall, the noise floor for the planned t₅ and t₆ waves, ranged from {{REL1_MIN}} to {{REL1_MAX}} (one run against another) across models and conditions. Ranking, Sentiment, Coverage and Grounding analyses of the same answers are pre-registered separately and are not reported here.

**Keywords:** AI availability; brand availability; AIAS; pre-registration; Ehrenberg-Bass; large language models; model generations; cross-generation stability; web search; test--retest reliability; brand recall; consistency

**JEL codes:** M31; L86, L15, D83, M37

**Paper status:** Pre-registered prospective re-acquisition (tag `{{PREREG_TAG}}`; revision r2 with clarifications C1--C28, deposited on OSF before the first $t_4$ call); {{MC_ANSWERED}} of 876 design calls answered; {{DEV_STATUS}} Part of the AIAS measurement programme.

# 1. Introduction

AI Availability --- the discoverability and representation of a brand in the outputs of large language models --- has been proposed as a third measurable layer of brand availability (González Castro, 2026, SSRN 6659000), alongside the Mental and Physical Availability of the Ehrenberg-Bass tradition (Sharp, 2010; Romaniuk & Sharp, 2022). The AIAS programme measures it under a versioned protocol with two locked components. Presence is whether and how often models name a brand (Methodology v1.6, SSRN 6816340; AIAS 1.0, SSRN 6817841). Consistency is whether the models of a panel agree about a brand, measured by the mean-independent dispersion statistic $\varphi$ (Methodology v1.8, SSRN 6963359), which replaced a coefficient-of-variation quantity falsified as a Consistency instrument (Methodology v1.7, SSRN 6878818).

Since its v0.17 phase the programme has measured on one fixed panel of six models: Claude Opus 4.5, Claude Sonnet 4.5, GPT-4o, GPT-4o mini, Gemini 2.5 Flash and Gemini 2.5 Flash-Lite. That panel is retiring: Claude Opus 4.5 not sooner than 24 November 2026, Claude Sonnet 4.5 on 30 November 2026, and the GPT-4o and GPT-4o mini snapshots on 14 January 2027. Its last wave, $t_3$ (v0.41, SSRN 7685100), was collected on 9 November 2026 on the five-category omnibus first measured in May 2026 (v0.19--v0.23). Over the 152 days from $t_2$ to $t_3$ both components held on that panel: recall Presence kept its brand order in every category (per-category Spearman $\rho$ from {{V41_PI_MIN}} to {{V41_PI_MAX}}), and $\varphi$ kept its order across {{V41_PHI_N}} brands ($\rho = {{V41_PHI_RHO}}$). These are single-category and all-brand Spearman correlations, not the pooled within-category statistic of this study (§2.7), and are given as background rather than as comparators. From now on every new collection of the programme runs on current models.

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

Mentions in Phase B answers were coded by each substrate's certified function, unchanged: for v0.20--v0.22 the content module's `detect_mention`, for v0.19 the parser of `acquire_v0_19`, and for v0.23 the deterministic brand matching of `score_v0_23.score_phase_b` (its optional language-model elaboration step enters no statistic and was not run). Coding applies to the visible answer text. In both conditions URLs are removed before matching (`https?://` addresses and the targets of Markdown links; link text is kept), so a brand counts only when the answer names it, not when a cited address contains it. Recognition (Phase A, S0, run 1) was coded by the same yes/no parsers as at $t_1$--$t_3$ for v0.19--v0.22 and, for v0.23, by the $t_1$--$t_3$ recognition judge (Claude Sonnet 4.5; 72 judge calls, which are coding, not acquisition). The coder (`code_t4_v0_42.py`, git blob `2d36735d`) was fixed before the lock.

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

The pre-registration (revision r2, with clarifications C1--C28) was locked at git tag `{{PREREG_TAG}}` (commit `{{PREREG_COMMIT}}`) and deposited on OSF (`ec6wh`, `v42/prereg/`) with an anchor record naming the tag's commit before any study probe was sent; the collection script refused to run until the tag was on the remote repository and the anchor existed. The lock procedure provided a 24-hour review period after the last change to a decision rule (C25); the pre-registrant waived it on 10 November 2026 (20:26 US Central time), and the tag was set on 11 November 2026 at 02:52 UTC. OSF's file records date the deposit of the locked files to 02:53--02:55 UTC and that of the anchor record to 02:55 UTC, before the first call ({{WIN_FIRST}} UTC; §3.1). Revision r2 replaced the first draft under the programme's collection budget rule (at most US\$100 of paid model calls per paper): one flagship per provider, Phase A in S0 with one run, and the removal of `H_Version_Presence` (clarifications C10--C24). Clarification C25, made before the lock, changed the decision statistic to the centred $\rho_{\text{pw}}$ of §2.7: v0.41's uncentred version is inflated by between-substrate differences in mean rank when substrates differ in size (16 against 24 brands), with a mean of +0.0464 under independence on the 112 brands; thresholds, rules and seeds were unchanged. Clarification C26 made the collection script enforce the one-collection rule and the window and record every billed batch request. Clarifications C27 and C28, made before the lock after a dry run of the whole chain on simulated provider responses, made the brand table's columns for panel N3 always use all three models (the component papers recompute them on all three), made descriptive 5 name the source of a Gemini grounding redirect by its host name instead of counting the redirect address as one domain, and made the budget guard and descriptive 6 count billed usage they had missed (OpenAI page-open and find-in-page actions, Gemini search-result tokens), in the conservative direction; neither changed a hypothesis, threshold or decision rule. The scorer (`score_v0_42.py`) and the coder were written and tested on synthetic data before the lock, and the scorer was run once, after the parity gates. {{DEV_SENTENCE}}

# 3. Results

## 3.1 Parity gates and manipulation checks

{% switch CASE_PARITY %}
{% case PASSED %}
All three parity gates passed before any $t_4$ statistic was computed (P1, P2 and P3).
{% case SYNTHETIC %}
[Synthetic test run: the scorer's synthetic mode skips the parity gates.]
{% endswitch %}
{{MC_ANSWERED}} of the {{MC_EXPECTED}} design calls were answered ({{MC_SHARE}}), and `MC_Complete` {% if MC_COMPLETE_PASS %}passed{% else %}failed its 98% threshold{% endif %}. Table 2 gives the counts per model and condition. {% if ANY_EXCLUDED %}{{EXCLUDED_SENTENCE}}{% else %}No model × condition fell below the 90% floor, so no model was dropped.{% endif %} {% if MC_SERVED_PASS %}`MC_Served` passed: every answered call was served by the requested model or a dated snapshot of it.{% else %}`MC_Served` failed: {{MC_SERVED_N}} answered calls were served by another model and were excluded from the analysis.{% endif %} {{MC_NOID_SENTENCE}} {% if MC_OUTSIDE_ANY %}{{MC_OUTSIDE}} raw lines fell outside the design and were not analysed.{% endif %}

{% if MCS_ANY_FLAG %}`MC_Search` flagged {{MCS_FLAGGED}}: search was used in fewer than 25% of its S1 calls, and its S1 results are marked "search rarely used" throughout (by $^{\dagger}$ in the tables, and in the captions of the tables and figures whose search-on values include it).{% else %}Every model used web search in at least 25% of its answered S1 calls (`MC_Search`; Table 2).{% endif %} {% if MCT_ANY_FLAG %}`MC_Truncation` flagged {{MCT_FLAGGED}}, which ended more than 5% of calls at the output cap.{% else %}No model × condition ended more than 5% of its calls at the output cap (`MC_Truncation`).{% endif %} The first call started at {{WIN_FIRST}} and the last ended at {{WIN_LAST}} (UTC), a span of {{WIN_SPAN}} hours, and `MC_Window` {% if WIN_PASS %}passed{% else %}failed{% endif %}. Recorded spend on all billed requests, at the list prices of the pre-registration, was {{COST_TOTAL}}, or {{BUDGET_SPEND}} with the {{BUDGET_RESERVE}} reserve for the recognition judge, and `MC_Budget` {% if BUDGET_PASS %}passed{% else %}failed{% endif %}. {{BUDGET_APPROVALS}}

Table: Calls answered, output-cap endings and search use, by model and condition. Answered: status ok, non-empty text and an accepted served ID; expected: 202 (S0) and 90 (S1) per model.{{FLAG_ROW_NOTE}}

{{TABLE_MC}}

## 3.2 Cross-generation stability of Presence (`H_Gen_Presence`)

{% switch CASE_GEN %}
{% case CONFIRMED|MARGINAL|FALSIFIED %}
Across the {{GEN_N}} brands, recall Presence on the newest models with search off correlated with recall Presence on the retiring panel at $\rho_{\text{pw}} = {{GEN_RHO}}$ (95% interval {{GEN_CI_LO}} to {{GEN_CI_HI}}; one-sided $p_{\text{perm}} = {{GEN_P}}$ from {{GEN_NPERM}} draws); v0.41's uncentred statistic gives {{GEN_RHO_UNC}}. The level shift was $\Delta = {{GEN_DELTA}}$ (95% interval {{GEN_D_LO}} to {{GEN_D_HI}}){% switch GEN_DELTA_DIR %}{% case ABOVE %}: on average the newest models named a brand in a larger share of category answers than the retiring panel.{% case BELOW %}: on average the newest models named a brand in a smaller share of category answers than the retiring panel.{% case SPANS %}; its interval includes zero.{% endswitch %}
{% case UNDETERMINED_EXCLUDED|UNDETERMINED_DEGENERATE %}
No pooled correlation is reported for the primary test.
{% endswitch %}
{% switch CASE_GEN %}
{% case CONFIRMED %}
The correlation meets both conditions of the confirmation rule ($\rho_{\text{gen}} \geq 0.70$ and $p < .05$), and the verdict is **CONFIRMED**.
{% case MARGINAL %}
The correlation does not meet the confirmation rule ($\rho_{\text{gen}} \geq 0.70$ with $p < .05$) and is not below the falsification bar of 0.50, and the verdict is **MARGINAL**.
{% case FALSIFIED %}
The correlation is below the falsification bar of 0.50, and the verdict is **FALSIFIED**.
{% case UNDETERMINED_EXCLUDED %}
{{EXCL_S0_NAMES}} answered fewer than 90% of its search-off calls, so under the drop rule (§2.9) the primary test is **UNDETERMINED**; revision r2 has no fallback panel.
{% case UNDETERMINED_DEGENERATE %}
The statistic was undefined on the data, and the verdict is **UNDETERMINED**.
{% endswitch %}

{% if GEN_S1_PRESENT %}With search on in place of search off, the same comparison gives $\rho_{\text{pw}} = {{GEN_S1_RHO}}$ (95% interval {{GEN_S1_CI_LO}} to {{GEN_S1_CI_HI}}; $p_{\text{perm}} = {{GEN_S1_P}}$){% if GEN_S1_REDUCED %} on a reduced panel ({{GEN_S1_MODELS}}){% endif %}, which would read {{GEN_S1_VERDICT}} under the primary rule; this variant is reported alongside and decides nothing.{% else %}The search-on variant was not computed: no model was retained in S1.{% endif %} Per provider, the legacy pair pooled against its new model gives {{PAIRS_SENTENCE}}. Table 3 gives the per-substrate correlations and Figure 1 the per-brand values.

Table: Recall Presence, $t_3$ (retiring panel) against $t_4$ (newest models), Spearman $\rho$ within each substrate, search off (primary test) and search on (reported alongside).{{FLAG_POOLED_NOTE}}

{{TABLE_GEN_SUB}}

![Per-brand recall Presence on the retiring panel at $t_3$ against the newest models with search off at $t_4$ (mean of three runs), coloured by substrate; dashed line = equal values. {{FIG1_CAPTION}}]({{FIG_DIR}}/chart_01_presence_t3_t4.pdf){#fig:gen width=100%}

## 3.3 Cross-generation stability of Consistency (`H_Gen_Phi`)

{% switch CASE_PHI %}
{% case CONFIRMED|MARGINAL|FALSIFIED|UNDETERMINED_FLOOR %}
{{PHI_N}} brands had $\varphi$ defined on both panels{{PHI_N_BY_SUB}}.
{% case UNDETERMINED_EXCLUDED|UNDETERMINED_DEGENERATE %}
No pooled correlation is reported for this test.
{% endswitch %}
{% switch CASE_PHI %}
{% case CONFIRMED|MARGINAL|FALSIFIED %}
Their $\varphi$ values on the newest models with search off correlated with their $t_3$ values at $\rho_{\text{pw}} = {{PHI_RHO}}$ (95% interval {{PHI_CI_LO}} to {{PHI_CI_HI}}; one-sided $p_{\text{perm}} = {{PHI_P}}$); v0.41's uncentred statistic gives {{PHI_RHO_UNC}}.
{% case UNDETERMINED_FLOOR|UNDETERMINED_EXCLUDED|UNDETERMINED_DEGENERATE %}
{% endswitch %}
{% switch CASE_PHI %}
{% case CONFIRMED %}
The correlation meets the confirmation rule ($\rho \geq 0.50$ with $p < .05$ and $n \geq 40$), and the verdict is **CONFIRMED**.
{% case MARGINAL %}
The correlation does not meet the confirmation rule ($\rho \geq 0.50$ with $p < .05$) and is not below the falsification bar of 0.30, and the verdict is **MARGINAL**.
{% case FALSIFIED %}
The correlation is below the falsification bar of 0.30, and the verdict is **FALSIFIED**.
{% case UNDETERMINED_FLOOR %}
This is below the pre-registered floor of 40 brands, and the verdict is **UNDETERMINED**.
{% case UNDETERMINED_EXCLUDED %}
Under the drop rule (§2.9), with {{EXCL_S0_NAMES}} excluded in S0, the verdict is **UNDETERMINED**.
{% case UNDETERMINED_DEGENERATE %}
The statistic was undefined on the data, and the verdict is **UNDETERMINED**.
{% endswitch %}

{{PARTITION_SENTENCE}} {% if MI_PRESENT %}On N3 with search off, $|\rho_{\text{pw}}(\varphi, \hat\pi)| = {{MI_ABS}}$ ($n = {{MI_N}}$; uncentred {{MI_UNC}}), {% if MI_FLAG %}at or above the v1.7 ceiling of 0.50: on this panel $\varphi$ is flagged as not mean-independent.{% else %}below the v1.7 ceiling of 0.50, so the mean-independence flag is not raised.{% endif %}{% else %}Mean-independence was not computed (no N3 model retained in S0).{% endif %} Table 4 gives the per-substrate correlations and Figure 2 the per-brand values.

Table: Consistency $\varphi$, $t_3$ against $t_4$ (newest models, search off), Spearman $\rho$ within each substrate, over brands with $\varphi$ defined on both panels.

{{TABLE_PHI_SUB}}

![Per-brand $\varphi$ on the retiring panel at $t_3$ against the newest models with search off at $t_4$ (mean over defined runs), brands with $\varphi$ defined on both; dashed line = equal values. {{FIG2_CAPTION}}]({{FIG_DIR}}/chart_02_phi_t3_t4.pdf){#fig:phi width=100%}

## 3.4 Web search and Presence (`H_Search_Presence`)

{% switch CASE_SEARCH %}
{% case ROBUST|SENSITIVE|DOMINATED %}
On {{S_MODELS}}{% if S_REDUCED %} (a reduced panel){% endif %}, recall Presence with search on correlated with recall Presence with search off at $\rho_S = {{S_RHO}}$ across {{S_N}} brands (95% interval {{S_CI_LO}} to {{S_CI_HI}}; uncentred {{S_RHO_UNC}}). The level shift was $\Delta = {{S_DELTA}}$ (95% interval {{S_D_LO}} to {{S_D_HI}}).
{% case UNDETERMINED|NOT_COMPUTED %}
The search contrast could not be read: {{S_WHY}}.
{% endswitch %}
{% switch CASE_SEARCH %}
{% case ROBUST %}
The interval's lower bound is at least 0.80, and the pre-declared label is **search-robust**.
{% case SENSITIVE %}
The interval's lower bound is below 0.80 and its upper bound is not below 0.50, and the pre-declared label is **search-sensitive**.
{% case DOMINATED %}
The interval's upper bound is below 0.50, and the pre-declared label is **search-dominated**.
{% case UNDETERMINED|NOT_COMPUTED %}
No label applies.
{% endswitch %}
{% if MCS_ANY_FLAG %}The search-on answers of {{MCS_FLAGGED}} are flagged "search rarely used" (§3.1).{% endif %} Table 5 gives the result per model. {{S_PER_SUB_SENTENCE}} Figure 3 shows the per-brand values.

Table: Recall Presence with search off against search on, per model (newest models, three runs each).{{FLAG_ROW_NOTE}}

{{TABLE_SEARCH_MODEL}}

![Left: per-brand recall Presence on the newest models with search off and on (mean of three runs each). Right: $\rho_S$ with its 95% interval and the correlation per model and per substrate, against the pre-declared zones. {{FIG3_CAPTION}}{{FLAG_POOLED_NOTE}}]({{FIG_DIR}}/chart_03_search_s0_s1.pdf){#fig:search width=100%}

## 3.5 Pre-registered descriptives

**Run-to-run reliability.** Table 6 and Figure 4 give rel1 and rel3 per model and condition: {{REL_SENTENCE}} Recognition agreement across runs is not computed, because Phase A has one run in revision r2.

Table: Run-to-run reliability of recall per model and condition (descriptive 1). rel1: mean $\rho_{\text{pw}}$ over the three run pairs; rel3: the reliability of the three-run mean.{{FLAG_ROW_NOTE}}

{{TABLE_REL}}

![rel1 (one run against another) and rel3 (mean of three runs) per model and condition. {{FIG4_CAPTION}}{{FLAG_POOLED_NOTE}}]({{FIG_DIR}}/chart_04_run_reliability.pdf){#fig:rel width=100%}

**Recognition.** Table 7 gives the share of brands coded as recognized by each model with search off at $t_4$, beside each legacy model at $t_3$. {{RECOG_NOTE}}

Table: Share of the 112 brands coded as recognized (descriptive 2): newest models at $t_4$ (search off, one run) and legacy models at $t_3$.

{{TABLE_RECOG}}

**Floor persistence.** {{FLOOR_SENTENCE}}

![Brands below the recall floor at $t_3$ (mean $k$ per model below 1) and at $t_4$ (newest models, search off; mean $k$ per model-run below 1). {{FIG5_CAPTION}}]({{FIG_DIR}}/chart_05_floor.pdf){#fig:floor width=100%}

**Answer form, search records and cost.** Tables 8 to 10 report the remaining descriptives: words per answer, registry brands named per Phase B answer, finish reasons and non-answers (descriptive 4); searches, sources and citations per S1 call (descriptive 5, with the 20 most-cited domains per model in Appendix Table 11); and tokens, searches and spend per model and condition from the recorded usage (descriptive 6).

Table: Answer form per model and condition (descriptive 4). Words: mean words per Phase A and Phase B answer; brands per B: registry brands named per Phase B answer; non-answers: Phase A answers (v0.19--v0.22) with no yes or no; refusals: by finish reason; unanswered: error or empty after the retry policy.{{FLAG_ROW_NOTE}}

{{TABLE_FORM}}

Table: Search records per model, answered S1 calls (descriptive 5).{{FLAG_ROW_NOTE}}

{{TABLE_SEARCHDESC}}

Table: Recorded usage and spend per model and condition (descriptive 6), all billed requests at the list prices of the pre-registration; the v0.23 recognition judge is not in the raw file and is covered by its reserve.{{FLAG_ROW_NOTE}}

{{TABLE_COST}}

# 4. Discussion

{% switch CASE_GEN %}
{% case CONFIRMED %}
The primary result is that the ordering of brands by recall Presence carried over from the retiring model generation to the newest flagship models. Under the pre-registered rationale, the programme's record on the legacy panel can therefore be bridged to the new panel for Presence: the brand standings measured since May 2026 remain interpretable on current models. The bridge is an ordering, not a level. The level shift of §3.2 belongs to the new panel and its serving settings, and comparisons of absolute Presence across the change of panel would need to account for it.
{% case MARGINAL %}
The primary result is intermediate. The newest models order brands by Presence in a way related to the retiring panel's ordering, but not at the bar the programme uses for the stability of one panel over time. Under the pre-registered rationale, a value below 0.70 across a few days is attributable to the change of model generation rather than to time. The legacy record can be read beside the new panel's but not bridged to it at the programme's stability standard, and the new panel's series should be read on its own terms, with the legacy series as context.
{% case FALSIFIED %}
The primary result is that the two model generations order brands too differently for the legacy record to be bridged quantitatively. Under the pre-registered rationale, the new panel starts its own series, with this wave as its baseline. The record on the legacy panel remains a valid description of that panel; it does not transfer to current models.
{% case UNDETERMINED_EXCLUDED|UNDETERMINED_DEGENERATE %}
The primary question is not answered by this wave: the pre-registered rules leave `H_Gen_Presence` undetermined (§3.2). Whether the legacy record can be bridged to current models remains open; the wave still provides the run-to-run baseline of the new panel's series.
{% endswitch %}

{% switch CASE_PHI %}
{% case CONFIRMED %}
For Consistency, measured on three models rather than six, the brand order carried over as well: which brands the models of a panel agree about is not specific to the retiring generation. Together with the Presence result, this supports carrying both components onto the new panel.
{% case MARGINAL %}
For Consistency the result is intermediate. With three models $\varphi$ carries less information per brand than with six (§2.8), so part of the shortfall from the confirmation bar may reflect the smaller panel rather than the change of generation; the design cannot separate the two.
{% case FALSIFIED %}
For Consistency the brand order did not carry over. Because $\varphi$ on three models is noisier than on six (§2.8), the design cannot attribute the change to the generation alone; it does show that the legacy panel's Consistency scores cannot be carried to the new panel.
{% case UNDETERMINED_FLOOR|UNDETERMINED_EXCLUDED|UNDETERMINED_DEGENERATE %}
The Consistency comparison is undetermined (§3.3), so whether Consistency carries across the change of generation remains open.
{% endswitch %}

{% switch CASE_SEARCH %}
{% case ROBUST %}
Web search left the Presence ordering intact: on these models, what each provider's search adds to an answer does not reorder which brands are named most. Presence measured with search on and with search off rank brands alike; any difference in level between the two conditions is the shift reported in §3.4.
{% case SENSITIVE %}
Web search changed the Presence ordering in part. Presence measured with search on is therefore not interchangeable with Presence measured without it, and the condition has to be stated with every score.
{% case DOMINATED %}
Web search reordered brands by Presence. With search on, the ordering reflects what the search returns more than what the model names unaided; on these models, Presence with and without search are different measurements.
{% case UNDETERMINED|NOT_COMPUTED %}
The search contrast is not decided (§3.4).
{% endswitch %}

The run-to-run reliabilities of §3.5 set the noise floor of the new panel's series: a change in brand order at $t_5$ or $t_6$ is interpretable only beyond the variation recorded here between runs of the same model on the same questions.

# 5. Limitations

Model generation is confounded with serving settings (temperature, output cap, thinking) and with knowledge cut-off, so `H_Gen_Presence` tests the bundle as a user meets it. There is one model per provider and therefore no within-provider replication at $t_4$. Three runs estimate run-to-run noise only coarsely, and $\varphi$ on three models is noisier than on six. Search-on answers depend on the web on the day and are reproducible only as recorded. The study covers one market and language (US English) and five categories chosen in May 2026. $t_3$ and $t_4$ are a few days apart, not simultaneous. Claude Fable 5.2 was sent through Anthropic's Message Batches API and the other two models synchronously; the batch requests carried the same parameters as the synchronous calls, but the serving path differs. Recognition rests on one Phase A run per model, in S0 only. Claude Fable 5.2's cost per call was estimated from another model's before collection, which is why the budget guard could have ended the collection before the second and third search-on runs; {{BUDGET_LIMIT_SENTENCE}}{% if MCS_ANY_FLAG %} The search-on results of {{MCS_FLAGGED}} rest on calls that rarely searched.{% endif %}{% if MCT_ANY_FLAG %} Calls ending at the output cap ({{MCT_FLAGGED}}) may truncate recall lists.{% endif %}

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

Table: The 20 most-cited domains per model in the answered search-on calls (descriptive 5), with citation counts.{{FLAG_ROW_NOTE}}

{{TABLE_DOMAINS}}
