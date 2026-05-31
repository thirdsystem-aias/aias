---
title: "A Pre-Registered Null on AI Share-of-Voice"
subtitle: "AIAS Presence does not converge with the headline metric — an exploratory scan finds strong convergence on recognition and presence-quality (B2B SaaS, n = 24)"
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
  - \renewcommand{\maketitle}{}
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
{\LARGE\bfseries A Pre-Registered Null on AI Share-of-Voice\par}
\vspace{0.8em}
{\large\itshape AIAS Presence does not converge with the headline metric\par}
{\large\itshape An exploratory scan finds strong convergence on recognition and presence-quality (B2B SaaS, n = 24)\par}
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

This study tests the convergent validity of AIAS\textsuperscript{TM} Presence — an AI-availability measure operationalized as category-competitive recall share (recall-SOM) — against a third-party AI brand-visibility instrument, extending a construct-validity program in which the same measure converged with Google Trends category-prominence (ρ = 0.74) and stood orthogonal to Amazon sales rank. Across 24 B2B SaaS brands, pre-registered before acquisition, AIAS recall-SOM was correlated (Spearman; 10,000-sample bootstrap; Holm) with Share-of-Voice from the HubSpot AEO Grader — the brand-absolute instrument pre-committed as the convergent floor. The primary hypothesis was falsified: ρ = 0.29 (n = 24, n.s.; 95% CI [−0.17, 0.64]). A pre-specified sensitivity excluding the four "type-2" brands — visible to a brand-absolute prompt, absent from category-leadership recall — left the correlation below threshold (ρ = 0.36). A recognition-null control held: brand recognition sat at ceiling across all 24 brands and was orthogonal to the presence measure. An exploratory scan of the instrument's remaining dimensions found strong convergence with its presence-quality (ρ = 0.80) and brand-recognition (ρ = 0.75) subscores but not its headline Share-of-Voice — suggesting the pre-registered metric is range-restricted and a weak convergent proxy, while AIAS recall tracks brand-knowledge facets of AI representation, of a piece with its prior convergence with search-interest prominence. These are flagged exploratory and pre-specified for confirmatory test. The construct-matched instrument (share-of-model) was deferred on access and remains an open, pre-registered test. The result cautions against reading the commercial "Share of Voice" scores now entering the market as AI availability.

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

The test failed. AIAS recall-SOM did not converge with the Grader's Share-of-Voice (ρ = 0.29, n.s.). We report that null as the result. The remainder of the paper does two things: it documents the failure under pre-registration discipline, and it examines the structure of the failure — which is not random: the pre-registered metric is the weakest of the instrument's dimensions while others converge strongly, an exploratory result with practical stakes for how these scores are read.

# 2. Method

## 2.1 Sample

The sample is the v0.24 registry of 24 B2B SaaS brands, organized into four pre-defined cells: **A** — enterprise incumbents (Salesforce, HubSpot, ServiceNow, Workday, SAP, Oracle, Zendesk); **B** — high-identity challengers (Notion, Figma, Linear, Airtable, Slack, Miro); **C** — infrastructure/developer platforms (Datadog, Snowflake, Stripe, Twilio, Cloudflare, MongoDB); **D** — phantom candidates, defunct or absorbed products (Quip, Yammer, Wunderlist, HipChat, Stride). Cell membership is sourced from the registry, which is the single source of truth for the `cell` field.

## 2.2 AIAS-side measure

The AIAS-side variable is **recall_channel_som** = R_cat_scaled = (R_cat / 36) × 100, pooled across a six-model panel (Claude Opus 4.7, Claude Sonnet 4.6, GPT-4o, GPT-4o-mini, Gemini 2.5 Flash, Gemini 2.5 Flash-Lite). R_cat is the brand's category-leadership recall count under the generic-leadership prompt frame. The scoring code is reused verbatim from the v0.25 scorer (`score_v0_25.load_v24_presence`), so the measure is identical to the one that produced the ρ = 0.74 Trends anchor; this is a deliberate comparability constraint, not a fresh operationalization.

Brand recognition (C_P) sits at ceiling: every brand scored 6/6 across the panel. C_P therefore has zero variance and enters only as a recognition-null control (§3.4), not as a convergent variable.

## 2.3 Instrument I1 — HubSpot AEO Grader

I1 is the HubSpot AEO Grader (free tier), which returns, for a queried brand, a perception profile across three engines (labeled as powering ChatGPT, Perplexity, and Gemini) on five dimensions: Brand Sentiment (/40), Presence Quality (/20), Brand Recognition (/20), Market Competition (/10), and Share of Voice (/10). The convergent variable is **I1_sov**, the mean of the three engines' Share-of-Voice subscore (0–10).

Every brand was queried under a uniform frame — geography "United States," products/services "B2B SaaS," industry "Technology" — to hold the query context constant across the registry. This frame is logged as the r3 operational instantiation and matches the generic-leadership framing of R_cat. Collection ran in a single session on 2026-05-29.

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

AIAS recall-SOM did not converge with I1_sov: **ρ = 0.294, n = 24, p_adj = 0.164** (Holm), 95% CI [−0.171, 0.638]. The correlation is below the confirm threshold (0.60) and not significant. **H_CV3_Primary is falsified.**

The I1_sov distribution is informative on its own. Live brands cluster tightly between 5.67 and 8.33, with most between 7.0 and 8.0; the defunct Cell-D brands fall well below this band (Wunderlist and HipChat at 0.33, Yammer at 2.0). Much of the rank agreement that does exist is carried by this live/defunct separation — both measures rank dead brands low. Above that floor, the Grader's compressed live-brand range leaves little variance to track recall-SOM against. Per-brand pairs and rank disagreements are reported in Table 2.

**Table 2. Per-brand AIAS recall-SOM and I1 Share-of-Voice, with rank disagreement (sorted by recall-SOM).**

| Brand | recall-SOM | I1 SoV | AIAS rank | I1 rank | Δrank |
|---|---|---|---|---|---|
| Salesforce | 100.0 | 7.67 | 1 | 4 | −3 |
| Workday | 94.4 | 7.33 | 2 | 7 | −5 |
| Slack | 91.7 | 5.67 | 3 | 18 | −15 |
| HubSpot | 91.7 | 7.00 | 3 | 14 | −11 |
| Oracle | 72.2 | 6.00 | 5 | 17 | −12 |
| SAP | 69.4 | 7.00 | 6 | 14 | −8 |
| Zendesk | 50.0 | 7.33 | 7 | 7 | +0 |
| ServiceNow | 47.2 | 7.67 | 8 | 4 | +4 |
| Snowflake | 27.8 | 7.33 | 9 | 7 | +2 |
| Datadog | 19.4 | 7.00 | 10 | 14 | −4 |
| Stripe | 11.1 | 8.00 | 11 | 2 | +9 |
| Notion | 5.6 | 7.33 | 12 | 7 | +5 |
| Twilio | 5.6 | 7.33 | 12 | 7 | +5 |
| MongoDB | 2.8 | 8.00 | 14 | 2 | +12 |
| Figma | 2.8 | 8.33 | 14 | 1 | +13 |
| Wunderlist | 0.0 | 0.33 | 16 | 23 | −7 |
| Quip | 0.0 | 4.67 | 16 | 19 | −3 |
| Yammer | 0.0 | 2.00 | 16 | 22 | −6 |
| HipChat | 0.0 | 0.33 | 16 | 23 | −7 |
| Miro | 0.0 | 7.33 | 16 | 7 | +9 |
| Cloudflare | 0.0 | 7.67 | 16 | 4 | +12 |
| Airtable | 0.0 | 7.33 | 16 | 7 | +9 |
| Linear | 0.0 | 4.67 | 16 | 19 | −3 |
| Stride | 0.0 | 3.00 | 16 | 21 | −5 |

## 3.2 Type-2 sensitivity

Excluding the four type-2 brands raised the correlation only to **ρ = 0.359 (n = 20, Δ = +0.065)** — still well below threshold. The direction matches the pre-registered prediction: the brand-absolute-visible / category-invisible cases do attenuate convergence, and removing them helps. But the lift is small, which means the non-convergence is broader than the type-2 cases alone. Even among ordinary brands, category-competitive recall and brand-absolute Share-of-Voice do not co-rank well.

## 3.3 Stride-confound sensitivity

Excluding Stride moved the correlation to **ρ = 0.223 (n = 23, Δ = −0.071)** — the estimate is *sensitive* to Stride, and in the awkward direction: the possibly-confounded Stride point was propping up an already-weak correlation rather than depressing it. The convergent estimate is therefore not robust to a plausible name-collision artifact. We report the result both ways; the limitation stands as "sensitive," not "robust."

## 3.4 Recognition-null control — CONFIRMED

Brand recognition (C_P) was at ceiling for all 24 brands (standard deviation = 0). With no variance, it carries no convergent signal by construction. **H_CV3_Recognition_Null is confirmed** — the ceiling is a property of this substrate, recorded here so that recognition is not mistaken for a live convergent dimension.

## 3.5 Exploratory component analysis

AIAS Presence was cross-correlated (Spearman) with all six I1 dimensions as an exploratory probe of where the two instruments touch. The pattern is uneven (Table 3): the pre-registered Share-of-Voice metric is among the weakest matches, while presence quality and brand recognition converge strongly.

**Table 3. AIAS recall-SOM × I1 dimensions (exploratory; n = 24).**

| I1 dimension | ρ | p |
|---|---|---|
| Presence Quality | +0.798 | < 0.001 |
| Brand Recognition | +0.748 | < 0.001 |
| Composite (/100) | +0.443 | 0.030 |
| Market Competition | +0.297 | 0.159 |
| Share of Voice (pre-registered) | +0.294 | 0.164 (n.s.) |
| Sentiment | +0.133 | 0.536 |

These correlations are exploratory under H_CV3_Component. They do not bear on H_CV3_Primary, which is fixed to Share-of-Voice and falsified; re-nominating a better-correlating dimension post-hoc is not available. The implications are taken up in §4 and pre-specified for confirmatory test in §6.

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

The pre-registered convergent test failed. AIAS recall-SOM did not co-rank with the HubSpot AEO Grader's Share-of-Voice — the metric named in advance as the convergent variable — at ρ = 0.29 (n.s.), with a 95% CI that straddles zero. That is the result, and the strong correlations below do not change it.

They are worth stating plainly because they are striking. The exploratory scan (§3.5) found AIAS recall-SOM converging with two other dimensions of the same instrument — presence quality (ρ = 0.80) and brand recognition (ρ = 0.75), both above the program's 0.74 "strong" benchmark — while the headline Share-of-Voice it was tested against carried almost no rank information. The discipline here runs one way and we hold it: Share-of-Voice was the pre-registered metric, it failed, and re-nominating presence quality or brand recognition as "the" convergent variable after seeing which one worked is the forking-paths move pre-registration exists to prevent. These correlations are hypothesis-generating, not confirmatory.

The same discipline forces a second move, against an interpretation an earlier framing of this work reached for. It is tempting to read the Share-of-Voice null as evidence that AIAS Presence measures category-competitive presence and therefore diverges from brand-absolute AI visibility. The data refute that. Presence quality and brand recognition are brand-absolute subscores — computed on a single named brand in isolation, exactly like Share-of-Voice — and recall-SOM converges with them. AIAS Presence does not broadly diverge from brand-absolute measurement; it converges with most of this instrument's facets and fails on one. The category-versus-brand-absolute axis does not explain the pattern, so we drop it.

What explains it is the metric, not the construct. The most likely mechanism is range restriction in Share-of-Voice: among live brands the subscore compresses into 4.67–8.33, most of them tied near 7.33, so nearly all its rank information is the live-versus-defunct split, leaving little to track category standing among salient brands. Presence quality and brand recognition spread across the live brands and move with recall. One detail sharpens this — the Grader's brand-recognition subscore carries real variance and tracks recall-SOM, even though AIAS's own recognition measure (C_P) is at ceiling on this substrate (§3.4); the two instruments operationalize "recognition" differently, and the Grader's graded version behaves like a prominence measure, which is what recall-SOM is.

Read against the program's prior confirmatory results, the exploratory pattern is coherent. The same AIAS variable converged with Google Trends category-prominence (ρ = 0.74) and stood orthogonal to Amazon sales rank. The dimensions it converges with here — presence quality, brand recognition — are prominence and knowledge facets, of a piece with the Trends result; the range-restricted competitive-share score it fails on, and the sales-rank criterion it correctly diverges from, are the exceptions the construct predicts. We advance this as a reading, not a finding: it rests on an exploratory scan and is offered to motivate a confirmatory pre-registration, not to claim convergent validity the pre-registered test did not deliver.

The practitioner consequence is sharper than a clean convergence would have given. The "Share of Voice" headline these tools sell as AI visibility is, on this evidence, the weakest available proxy for category-competitive AI presence — compressed, tied across salient brands, and the one dimension that did not track recall. The recognition and presence-quality signals beneath it aligned far better. A brand managing to its Share-of-Voice number may be managing the least informative dial on the dashboard. The scores carry real signal; read as "AI availability," the headline is the wrong place to read it.

# 5. Limitations

The convergent claim rests on a single instrument that was pre-registered as a *loose* construct match. The strongest available test — convergence against a category-scoped, construct-matched instrument (share-of-model) — was never run. A single-instrument null on one dimension cannot, on its own, separate a genuine convergence failure from a metric artifact — which is what the exploratory scan suggests is in play, and what a category-scoped instrument would resolve. The tight-instrument test is the one that would separate these, and it is deferred, not answered (§6).

The Grader is brand-absolute and un-scopeable on the free tier. One brand, Stride (D5), carries a name-collision confound; its score may reflect non-target "Stride" entities. Stride is retained in the primary, and the pre-specified `stride_confound` sensitivity excludes it; the convergent estimate is *sensitive* to that exclusion (§3.3) — a real weakness, reported rather than smoothed.

Other bounds: n = 24 is modest, though pre-registered and adequate for the planned correlation; brand recognition is at ceiling on this substrate, so recognition convergence cannot be tested here; the instruments were collected within a bounded window, and brand-level drift over any gap is a residual threat, mitigated but not removed by rank-based correlation; and the six-model panel reflects a particular set of model versions whose behavior will change.

# 6. Future Research

The pre-registered, deferred test stands as the immediate next step: convergence of AIAS recall-SOM against a category-scoped share-of-model instrument (Profound, or a self-serve instrument with equivalent category scoping). That test is decisive in a way this one is not. If recall-SOM converges with a construct-matched instrument, the present null is itself evidence of construct specificity — AIAS Presence converges with category-competitive measures and diverges from brand-absolute ones — and the I1 failure becomes part of the validity story rather than a threat to it. If it fails to converge even with a tight instrument, AIAS Presence has a convergent-validity problem that this study could not, on its own, surface. Either outcome is informative; neither is reachable without the tight instrument.

Beyond that: a confirmatory pre-registration of the recognition and presence-quality convergence surfaced here — those dimensions fixed in advance, on a fresh substrate, to test whether they replicate; completion of the discriminant arm (I3) for a full Campbell-Fiske matrix paired with v0.26; and, gated on construct-validity consolidation, extension from the Presence component to the full multi-component AIAS composite.

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
