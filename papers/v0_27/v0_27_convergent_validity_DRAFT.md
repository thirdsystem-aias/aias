---
title: "When AI Visibility Diverges from AI Availability"
subtitle: "A Pre-Registered Null in Convergent Validity — Brand-Absolute AI Share-of-Voice versus Category-Competitive Recall (B2B SaaS, n = 24)"
author: "Pablo Ulpiano González Castro"
date: "May 2026"
documentclass: article
fontsize: 11pt
geometry: "margin=1in"
mainfont: "Carlito"
linestretch: 1.15
colorlinks: true
linkcolor: black
urlcolor: black
header-includes:
  - \usepackage{setspace}
  - \usepackage{booktabs}
  - \usepackage{titlesec}
  - \titleformat{\section}{\normalfont\large\bfseries}{\thesection}{0.6em}{}
---

<!--
BUILD NOTE (delete before submission): YAML preamble + titlepage block below are
reconstructed from the v0.20+ canonical conventions, not copied from v0.26's literal
source. DIFF this preamble and the titlepage block against papers/v0.26/*.md before
running build_paper_v27.py — keep v0.26's exact pandoc keys / header-includes if they
differ. Content body (Abstract onward) is the deliverable.

DATA SLOTS still to fill from CC's outputs (marked [[SLOT: ...]] inline):
  1. Bootstrap 95% CI on primary rho (CI population bug fix first).
  2. Table 2 — per-brand (R_cat_scaled, I1_sov) pairs + rank disagreements.
  3. Table 3 — H_CV3_Component exploratory cross-correlations (AIAS x I1 subscores).
  4. I1 collection date window (Method).
  5. Pre-reg commit IDs are filled where known; verify against git log.
-->

\begin{titlepage}
\setstretch{1.0}
\setlength{\parskip}{0pt}
\centering
\vspace*{2cm}
{\LARGE\bfseries When AI Visibility Diverges from AI Availability\par}
\vspace{0.8em}
{\large\itshape A Pre-Registered Null in Convergent Validity\par}
{\large\itshape Brand-Absolute AI Share-of-Voice versus Category-Competitive Recall\par}
\vspace{1.2em}
{\normalsize Working Paper $\cdot$ Version 0.27 $\cdot$ Designed-for-Test (B2B SaaS)\par}
\vspace{2.5em}
{\large Pablo Ulpiano González Castro\par}
\vspace{0.4em}
{\normalsize SVA MPS Branding Program, New York, NY\par}
{\normalsize Third System\textsuperscript{TM} — research entity\par}
\vspace{1.5em}
{\normalsize May 2026\par}
\vfill
{\small Pre-registered before data acquisition. Hypotheses, thresholds, and exclusions locked at git commit prior to instrument pull. Data and code: OSF \texttt{osf.io/ec6wh}.\par}
\end{titlepage}

# Abstract {-}

This study tests the convergent validity of AIAS\textsuperscript{TM} Presence — an AI-availability measure operationalized as category-competitive recall share (recall-SOM) — against a third-party AI brand-visibility instrument. It extends a construct-validity program in which the same measure converged with Google Trends category-prominence (ρ = 0.74) and stood orthogonal to Amazon sales rank. Across 24 B2B SaaS brands, pre-registered before acquisition, AIAS recall-SOM was correlated (Spearman; 10,000-sample bootstrap; Holm) with Share-of-Voice from the HubSpot AEO Grader — the brand-absolute instrument pre-committed as the convergent floor. The primary hypothesis was falsified: ρ = 0.29 (n = 24, n.s.). The non-convergence was patterned rather than random. The largest violations came from "type-2" brands — visible under a brand-absolute prompt but absent from category-leadership recall — and a pre-specified sensitivity excluding them left the correlation below threshold (ρ = 0.36). A recognition-null control held: brand recognition sat at ceiling across all 24 brands and was orthogonal to the presence measure. The construct-matched instrument (share-of-model) was deferred on access and remains an open, pre-registered test. The result bounds the convergent domain of AIAS Presence and supports a reading in which it captures category-competitive AI presence — distinct from brand-absolute AI visibility, a distinction with direct consequences for how brands read the commercial "AI visibility" scores now entering the market.

# Keywords {-}

AI availability; answer engine optimization; convergent validity; construct validity; share of voice; share of model; large language models; brand measurement; pre-registration; B2B SaaS.

# JEL Classification {-}

M31 (Marketing) — primary; L86 (Information and Internet Services); L15 (Information and Product Quality); D83 (Search, Learning, Information, Knowledge); M37 (Advertising).

# Paper Status {-}

Pre-registered working paper. The pre-registration was locked across five revisions (tags `v0.27-prereg-r1` through `v0.27-prereg-r5`) before any instrument data was acquired; revisions r4 and r5 record two pre-results amendments documented below. The AIAS-side measure is inherited verbatim from the v0.25 scorer to preserve comparability with that study's convergent anchor. One pre-registered instrument (HubSpot AEO Grader, I1) was collected; the construct-matched instrument (Profound, I2) was deferred on access at r4; the discriminant instrument (Brandwatch, I3) was not run. Data, code, and pre-registration history are deposited at OSF (`osf.io/ec6wh`).

# 1. Introduction

The Ehrenberg-Bass account of brand growth rests on two measurable layers: mental availability — the brand's propensity to come to mind in buying situations — and physical availability — the ease of finding and buying it [@sharp2010; @romaniuk2016]. The Tri-System program proposes a third layer for an environment in which a growing share of category research and shortlisting happens inside large language models: **AI availability**, the brand's propensity to be surfaced, ranked, and recommended when a buyer poses a category question to a generative model. Third System\textsuperscript{TM} operationalizes this layer as the AIAS\textsuperscript{TM} measurement program, of which the present study is one phase.

AIAS Presence is the program's first published component. It is measured as **recall-SOM** — a brand's share of category-leadership recall across a fixed panel of models, given a generic "leading platforms in this category" prompt. The measure is deliberately *category-competitive*: it asks whether a brand surfaces when a buyer asks about the category, not whether a model can produce text about the brand when named. That framing is the construct under test.

A measure earns its place by validating against external criteria. Two prior phases established the bracket. In v0.25, AIAS recall-SOM converged with Google Trends category-prominence at ρ = 0.74 — strong convergent validity against an established real-world demand signal. In v0.26, the same presence family stood orthogonal to Amazon Best-Sellers Rank — discriminant validity against a sales-rank criterion the construct should *not* reduce to. Together these are the convergent and discriminant arms of a Campbell-Fiske validation [@campbell1959; @cronbach1955].

This phase asks a question that is now commercially live. A class of "AI visibility" or "answer engine optimization" (AEO) tools has appeared, selling brands a score for how present they are inside ChatGPT, Perplexity, and Gemini. If AIAS Presence and these commercial instruments measure the same thing, the program gains a cheap external criterion and practitioners gain a bridge between the two. We pre-registered a convergent test of AIAS recall-SOM against the most accessible such instrument — the HubSpot AEO Grader — and pre-committed it as the convergent *floor*: a brand-absolute, un-category-scopeable, free-tier instrument whose construct match to recall-SOM we rated, in advance, as loose.

The test failed. AIAS recall-SOM did not converge with the Grader's Share-of-Voice (ρ = 0.29, n.s.). We report that null as the result. The remainder of the paper does two things: it documents the failure under pre-registration discipline, and it examines the *structure* of the failure — which is not random, and which points toward a construct distinction with practical stakes.

# 2. Method

## 2.1 Sample

The sample is the v0.24 registry of 24 B2B SaaS brands, organized into four pre-defined cells: **A** — enterprise incumbents (Salesforce, HubSpot, ServiceNow, Workday, SAP, Oracle, Zendesk); **B** — high-identity challengers (Notion, Figma, Linear, Airtable, Slack, Miro); **C** — infrastructure/developer platforms (Datadog, Snowflake, Stripe, Twilio, Cloudflare, MongoDB); **D** — phantom candidates, defunct or absorbed products (Quip, Yammer, Wunderlist, HipChat, Stride). Cell membership is sourced from the registry, which is the single source of truth for the `cell` field.

## 2.2 AIAS-side measure

The AIAS-side variable is **recall_channel_som** = R_cat_scaled = (R_cat / 36) × 100, pooled across a six-model panel (Claude Opus 4.7, Claude Sonnet 4.6, GPT-4o, GPT-4o-mini, Gemini 2.5 Flash, Gemini 2.5 Flash-Lite). R_cat is the brand's category-leadership recall count under the generic-leadership prompt frame. The scoring code is reused verbatim from the v0.25 scorer (`score_v0_25.load_v24_presence`), so the measure is identical to the one that produced the ρ = 0.74 Trends anchor; this is a deliberate comparability constraint, not a fresh operationalization.

Brand recognition (C_P) sits at ceiling: every brand scored 6/6 across the panel. C_P therefore has zero variance and enters only as a recognition-null control (§3.4), not as a convergent variable.

## 2.3 Instrument I1 — HubSpot AEO Grader

I1 is the HubSpot AEO Grader (free tier), which returns, for a queried brand, a perception profile across three engines (labeled as powering ChatGPT, Perplexity, and Gemini) on five dimensions: Brand Sentiment (/40), Presence Quality (/20), Brand Recognition (/20), Market Competition (/10), and Share of Voice (/10). The convergent variable is **I1_sov**, the mean of the three engines' Share-of-Voice subscore (0–10).

Every brand was queried under a uniform frame — geography "United States," products/services "B2B SaaS," industry "Technology" — to hold the query context constant across the registry. This frame is logged as the r3 operational instantiation and matches the generic-leadership framing of R_cat. Collection ran within a single window [[SLOT 4: I1 collection date window]].

A pre-registered construct-match rating flagged I1 as **loose**: the Grader is *brand-absolute* — it scores how an engine characterizes a named brand in isolation — and cannot be category-scoped on the free tier. recall-SOM is *category-competitive*. The instrument was pre-committed as the convergent floor precisely because of this gap; a tight-match instrument (share-of-model) was specified separately as I2.

## 2.4 Deferred and unrun instruments

**I2 (Profound)** — the construct-matched instrument, reporting category-scoped share-of-model — was deferred at amendment r4. Profound is enterprise-only (sales-led, multi-thousand-dollar monthly contract); access was declined as disproportionate to a single phase. H_CV3_Profound and H_CV3_SOM are therefore NOT_RUN. **I3 (Brandwatch)** — the discriminant instrument — was not run; H_CV3_Discriminant is NOT_RUN. The convergent claim in this paper consequently rests on I1 alone, a limitation we take up in §5.

## 2.5 Analysis and pre-registered decisions

Correlations are Spearman rank, with 10,000-sample bootstrap and Holm correction across the primary family; minimum coverage n = 12. The primary hypothesis **H_CV3_Primary** predicted ρ ≥ 0.60 (confirm) between recall-SOM and I1_sov, with ρ ≥ 0.74 the "strong" benchmark carried from v0.25.

Two sensitivities were pre-specified, both pre-results:

- **type2_construct_gap** — drop the four "type-2" brands (R_cat = 0 but specialist-salient R_cult > 0: Linear, Airtable, Miro, Cloudflare), which are category-competitively invisible yet visible to a brand-absolute instrument. Pre-registered as the locus where a brand-absolute instrument should most diverge from recall-SOM.
- **stride_confound** — drop Stride (brand_id D5). The Grader cannot category-scope, and "Stride" is name-ambiguous (Stride gum, Stride Inc., Stride Bank), so its score may aggregate non-target entities rather than the defunct Atlassian product. Distinct threat from the construct gap (name ambiguity, not construct misalignment); added at r5 with rationale and timing on record, before scoring.

Cell-D true-zeros (R_cat = 0 and R_cult = 0: Quip, Yammer, Wunderlist, HipChat, Stride) are retained in the primary as genuine concordant absence, not artifact. The recognition-null control (**H_CV3_Recognition_Null**) predicted that C_P, at ceiling, carries no convergent signal. An exploratory component analysis (**H_CV3_Component**) cross-correlates AIAS Presence with the five I1 subscores.

# 3. Results

## 3.1 Primary convergent test — FALSIFIED

AIAS recall-SOM did not converge with I1_sov: **ρ = 0.294, n = 24, p_adj = 0.164** (Holm), 95% CI [[SLOT 1: bootstrap CI]]. The correlation is below the confirm threshold (0.60) and not significant. **H_CV3_Primary is falsified.**

The I1_sov distribution is informative on its own. Live brands cluster tightly between 5.67 and 8.33, with most between 7.0 and 8.0; the defunct Cell-D brands fall well below this band (Wunderlist and HipChat at 0.33, Yammer at 2.0). Much of the rank agreement that does exist is carried by this live/defunct separation — both measures rank dead brands low. Above that floor, the Grader's compressed live-brand range leaves little variance to track recall-SOM against. Per-brand pairs and rank disagreements are reported in Table 2.

[[SLOT 2: Table 2 — per-brand (R_cat_scaled, I1_sov) pairs and rank-disagreement column, from CC dump]]

## 3.2 Type-2 sensitivity

Excluding the four type-2 brands raised the correlation only to **ρ = 0.359 (n = 20, Δ = +0.065)** — still well below threshold. The direction matches the pre-registered prediction: the brand-absolute-visible / category-invisible cases do attenuate convergence, and removing them helps. But the lift is small, which means the non-convergence is broader than the type-2 cases alone. Even among ordinary brands, category-competitive recall and brand-absolute Share-of-Voice do not co-rank well.

## 3.3 Stride-confound sensitivity

Excluding Stride moved the correlation to **ρ = 0.223 (n = 23, Δ = −0.071)** — the estimate is *sensitive* to Stride, and in the awkward direction: the possibly-confounded Stride point was propping up an already-weak correlation rather than depressing it. The convergent estimate is therefore not robust to a plausible name-collision artifact. We report the result both ways; the limitation stands as "sensitive," not "robust."

## 3.4 Recognition-null control — CONFIRMED

Brand recognition (C_P) was at ceiling for all 24 brands (standard deviation = 0). With no variance, it carries no convergent signal by construction. **H_CV3_Recognition_Null is confirmed** — the ceiling is a property of this substrate, recorded here so that recognition is not mistaken for a live convergent dimension.

## 3.5 Exploratory component analysis

AIAS Presence was cross-correlated with the five I1 subscores (Sentiment, Presence Quality, Brand Recognition, Market Competition, Share of Voice) as an exploratory probe of where, if anywhere, the two instruments touch.

[[SLOT 3: Table 3 — H_CV3_Component exploratory cross-correlations]]

## 3.6 Pre-registered outcomes

**Table 1. Pre-registered hypothesis outcomes.**

| Hypothesis | Verdict | Detail |
|---|---|---|
| H_CV3_Primary (recall-SOM × I1_sov) | FALSIFIED | ρ = 0.294, n = 24, p_adj = 0.164 (n.s.) |
| H_CV3_Profound | NOT_RUN | I2 access declined (r4) |
| H_CV3_SOM | NOT_RUN | I2 access declined (r4) |
| H_CV3_Discriminant | NOT_RUN | I3 not run |
| H_CV3_Component | EXPLORATORY | cross-correlated vs I1 subscores |
| H_CV3_Recognition_Null | CONFIRMED | C_P sd = 0 (ceiling, all 24) |
| — type2_construct_gap sensitivity | — | ρ = 0.359, n = 20 (Δ +0.065) |
| — stride_confound sensitivity | — | ρ = 0.223, n = 23 (Δ −0.071) |

# 4. Discussion

The pre-registered convergent test failed. AIAS recall-SOM and the HubSpot AEO Grader's Share-of-Voice do not co-rank (ρ = 0.29, n.s.), and the estimate is neither lifted to threshold by removing the predicted construct-gap cases nor robust to a plausible name confound. Taken at face value, this bounds the convergent domain of AIAS Presence: it does not converge with this instrument.

The structure of the failure is the interesting part. We flag the following as **post-hoc**. The pre-registered prediction was convergence; it failed. The interpretation below is motivated by the patterning of that failure, not by a pre-registered discriminant hypothesis, and we advance it as a hypothesis for confirmatory test — not a conclusion, and emphatically not a relabeling of the null as a discriminant success.

With that flag in place: the brands that break convergence hardest are exactly the type-2 cases — high brand-absolute Share-of-Voice, zero category-leadership recall. A brand-absolute instrument sees Linear, Airtable, Miro, and Cloudflare clearly; a category-competitive measure does not surface them when asked for category leaders. That is not measurement error in either instrument. It is the two instruments measuring different things. recall-SOM asks *does the brand win the category question?* The Grader asks *can the engine talk about the brand?* A brand can score well on the second while scoring zero on the first.

This reading sits coherently beside the program's other two criterion tests. The *same* AIAS variable converged with Google Trends category-prominence (ρ = 0.74) and diverged from Amazon sales rank. The apparent tension — converges with Trends, not with the Grader, though both are brand-level external signals — resolves if the operative distinction is category-prominence versus brand-isolation. Google Trends tracks real-world search prominence, which moves with a brand's actual standing in its category; that is close to what recall-SOM captures. The Grader's brand-absolute Share-of-Voice tracks how much an engine will say about a brand in isolation, which is closer to training-document volume than to competitive standing. On that account, AIAS Presence aligns with category-prominence signals and diverges from brand-isolation signals and from sales rank — convergent where it should converge, discriminant where it should discriminate. The present null does not establish that arc, but it is consistent with it, and it sharpens the claim by showing where AIAS Presence stops tracking.

The practitioner consequence is direct. Commercial AEO and "AI visibility" scores of the brand-absolute kind measure something real — but not category-competitive AI presence. A brand can post a strong Grader score while being absent from the category-leadership answers its buyers actually receive. Read as "AI availability," these scores can mislead. The two should be read as complementary signals, not substitutes.

# 5. Limitations

The convergent claim rests on a single instrument that was pre-registered as a *loose* construct match. The strongest available test — convergence against a category-scoped, construct-matched instrument (share-of-model) — was never run. A loose-instrument null cannot distinguish "AIAS Presence converges with nothing" from "AIAS Presence does not converge with *brand-absolute* instruments." The tight-instrument test is the one that would separate these, and it is deferred, not answered (§6).

The Grader is brand-absolute and un-scopeable on the free tier. One brand, Stride (D5), carries a name-collision confound; its score may reflect non-target "Stride" entities. Stride is retained in the primary, and the pre-specified `stride_confound` sensitivity excludes it; the convergent estimate is *sensitive* to that exclusion (§3.3) — a real weakness, reported rather than smoothed.

Other bounds: n = 24 is modest, though pre-registered and adequate for the planned correlation; brand recognition is at ceiling on this substrate, so recognition convergence cannot be tested here; the instruments were collected within a bounded window, and brand-level drift over any gap is a residual threat, mitigated but not removed by rank-based correlation; and the six-model panel reflects a particular set of model versions whose behavior will change.

# 6. Future Research

The pre-registered, deferred test stands as the immediate next step: convergence of AIAS recall-SOM against a category-scoped share-of-model instrument (Profound, or a self-serve instrument with equivalent category scoping). That test is decisive in a way this one is not. If recall-SOM converges with a construct-matched instrument, the present null is itself evidence of construct specificity — AIAS Presence converges with category-competitive measures and diverges from brand-absolute ones — and the I1 failure becomes part of the validity story rather than a threat to it. If it fails to converge even with a tight instrument, AIAS Presence has a convergent-validity problem that this study could not, on its own, surface. Either outcome is informative; neither is reachable without the tight instrument.

Beyond that: replication of the category-competitive / brand-absolute distinction across the program's other substrate families; completion of the discriminant arm (I3) for a full Campbell-Fiske matrix paired with v0.26; and, gated on construct-validity consolidation, extension from the Presence component to the full multi-component AIAS composite.

# References {-}

Campbell, D. T., & Fiske, D. W. (1959). Convergent and discriminant validation by the multitrait-multimethod matrix. *Psychological Bulletin*, 56(2), 81–105.

Cronbach, L. J., & Meehl, P. E. (1955). Construct validity in psychological tests. *Psychological Bulletin*, 52(4), 281–302.

González Castro, P. U. (2026). *AIAS Presence Measurement Protocol: Convergent Validity against Search-Interest Criteria* (v0.25). Working paper, Third System / SSRN.

González Castro, P. U. (2026). *AIAS Presence and Amazon Best-Sellers Rank: A Discriminant-Validity Test* (v0.26). Working paper, SSRN 6847678.

Holm, S. (1979). A simple sequentially rejective multiple test procedure. *Scandinavian Journal of Statistics*, 6(2), 65–70.

Nosek, B. A., Ebersole, C. R., DeHaven, A. C., & Mellor, D. T. (2018). The preregistration revolution. *Proceedings of the National Academy of Sciences*, 115(11), 2600–2606.

Romaniuk, J., & Sharp, B. (2016). *Building Distinctive Brand Assets*. Oxford University Press.

Sharp, B. (2010). *How Brands Grow: What Marketers Don't Know*. Oxford University Press.

Spearman, C. (1904). The proof and measurement of association between two things. *American Journal of Psychology*, 15(1), 72–101.

# Declarations {-}

**Competing interests.** The author is employed by Samsung Electronics America. This research is conducted independently through Third System\textsuperscript{TM} and is unrelated to that employment; no Samsung products appear in the study substrate. The author declares no other competing interests.

**Funding.** Self-funded.

**Ethics.** Not applicable. The study involves no human subjects; data derive from public APIs and large-language-model prompts.

**Data and code availability.** Pre-registration history, data, and analysis code are deposited at OSF (`osf.io/ec6wh`), versioned under `v0.27`.

# Author Information {-}

**Pablo Ulpiano González Castro**
SVA MPS Branding Program, New York, NY (primary academic affiliation)
Third System\textsuperscript{TM} (research entity; data archive and methodology venue)
Correspondence: pablou@pablou.com · pablou.com
ORCID: 0009-0003-8968-9990
