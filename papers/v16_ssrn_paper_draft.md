---
# V16_PAPER_V15_TEMPLATE_RESTRUCTURE
title: "Regime 4 Boundary and Discourse-Language Carryforward on the Kitchen-Knives Substrate (AIAS v0.16)"
author: "Pablo Ulpiano González Castro"
date: "18 May 2026"
mainfont: "Carlito"
fontsize: 11pt
geometry: margin=1in
papersize: letter
linestretch: 1.36
header-includes:
  - \usepackage{float}
  - \floatplacement{figure}{H}
  - \usepackage[labelfont={bf,it},textfont=it,labelsep=period,justification=raggedright,singlelinecheck=false]{caption}
---
<!-- PAPER_V16_FIGURES_EMBEDDED -->

\begin{center}
\vspace{8pt}

{\fontsize{16}{21.76}\selectfont \textbf{Regime 4 Boundary and Discourse-Language Carryforward}}

\vspace{2pt}

{\fontsize{16}{21.76}\selectfont \textbf{on the Kitchen-Knives Substrate (AIAS v0.16)}}

\vspace{20pt}

{\fontsize{11}{16}\selectfont
Pablo Ulpiano González Castro \\[2pt]
School of Visual Arts, MPS Branding Program, New York, NY \\
\emph{(primary academic affiliation)} \\[6pt]
Third System\textsuperscript{TM} \\
\emph{Independent research entity; data archive and methodology venue} \\[10pt]
Correspondence: pablou@pablou.com $\cdot$ pablou.com \\
ORCID: \href{https://orcid.org/0009-0003-8968-9990}{0009-0003-8968-9990} \\[12pt]
18 May 2026
}

\vspace{20pt}
\end{center}

\newpage

# Abstract

v0.16 of the AIAS™ Presence Measurement Programme brings the v1.2-formalized construct-validity panel to the kitchen-knives substrate, completing a programme arc that began in v0.8 Discourse-Language Knives (SSRN 6728000). Two hypotheses pre-registered at git tag `v0.16-prereg` (commit `511e339`, 16 May 2026) tested at a single measurement wave (t~1~: April 27 – May 3, 2026; t~2~: May 4 – May 10, 2026). **H_Regime4_replication_knives** evaluates whether kitchen knives exhibits the canonical Regime 4 (Covariate-saturated weak) signature established on premium facial skincare (v0.11), personal finance apps (v0.13), and premium tea (v0.14, v0.15); verdict **PARTIAL** on the worldwide primary panel (n = 13). Bivariate Spearman ρ(AI Presence, Google Trends) = +0.022 at t~1~ and +0.003 at t~2~ (both within C2 threshold |ρ| < 0.35); partial ρ after brand_age + tradition_cell control = +0.101 and +0.080 (both fail C3 partial ρ < 0). The pre-registered PARTIAL tier names a non-saturated weak signature: bivariate decoupling holds, conservative covariate-saturated test fails. **H_Discourse_Language_carryforward** tests whether the v0.8 Discourse-Language Bias finding on knives survives v1.2 protocol with corrected eligibility filtering; verdict **CARRY-FORWARD CONFIRMED** on the Japanese tradition cell (n = 6; ρ(English-prompt AI Presence, Japanese-prompt AI Presence) = +0.197 at t~1~ and −0.149 at t~2~, both far below the 0.85 CONFIRMED threshold). The pre-registered US-region cell (n = 10, below the n = 12 inferential floor) reads as descriptive sensitivity with strongly-negative correlations: three brands (Güde, Sunlong, Au Nain) drop from US-region eligibility because their US-region Trends signal sits at the 14-day-zero floor. The US/worldwide divergence is the same underlying brand-asymmetry surfacing via registry coverage rather than via prompt language. The v0.16 reading positions kitchen knives as a productive boundary case for Regime 4 — not a falsification, not a fourth-substrate canonical confirmation — while closing the v0.8 discourse-language lineage under canonical pre-registered protocol.

**Keywords:** AI Availability; brand mediation; Spearman correlation; construct validity; pre-registration; large language models; Google Trends; kitchen knives; discourse-language bias
**JEL Classification:** M31; L86; L15; D83; M37

# 1. Introduction

The AIAS™ Presence Measurement Programme is a multi-substrate empirical research stream operationalizing AI Availability — the brand-level property defined by Gonzalez Castro [-@gonzalezcastro2026foundational] as the probability that a brand is retrieved, recommended, or selected by an AI intermediary in a category-relevant decision context. The programme's first component, **AI Presence**, measures the rate at which each brand appears across matched LLM responses to category-recommendation prompts. Construct validity for the Presence component has been built up across studies v0.11–v0.15, anchored by the four-regime taxonomy formalized in v0.13 [@gonzalezcastro2026fourregimes] and the AIAS Presence Measurement Protocol v1.2 [@gonzalezcastro2026protocolv12].

v0.16 brings this canonical protocol to the kitchen-knives substrate. The selection is not arbitrary: kitchen knives appeared in the programme's earlier work at v0.8 [@gonzalezcastro2026discoursetext] under a *pre-construct-validity* protocol — that study surfaced a Discourse-Language Bias on Japanese-tradition kitchen-knife brands that systematically underperformed in English-language prompt conditions relative to discourse-language-matched conditions. v0.16 returns to the same substrate with two purposes. First, to test whether kitchen knives exhibits the canonical Regime 4 (Covariate-saturated weak) signature established in three other substrates. Second, to verify whether the v0.8 discourse-language finding survives under v1.2 protocol with corrected eligibility filtering.

The verdicts are documented at the **PARTIAL** verdict tier and the **CARRY-FORWARD CONFIRMED** verdict tier respectively. The first verdict introduces a refinement to the regime taxonomy: PARTIAL is a productive boundary finding distinct from FALSIFIED, registered at v0.16 pre-registration as a sub-classification of v0.15's canonical FALSIFIED tier. The second verdict closes the v0.8 lineage under canonical pre-registered protocol — the original finding is no longer a one-paper observation but a documented carryforward under construct-validity eligibility, full pre-registration discipline, and OSF data transparency.

A subsidiary substantive finding is surfaced by the pre-registered US-region descriptive sensitivity: three eligible-at-worldwide brands (Güde, Sunlong, Au Nain) drop from US-region eligibility because their US-region Google Trends signal sits at the 14-day-zero floor. The US-region cell reads strongly negative on both waves (bivariate ρ = −0.881 / −0.812). This US/worldwide divergence is itself the same brand-asymmetry that the H_Discourse_Language_carryforward hypothesis surfaces via prompt language — appearing here via registry coverage. The paper develops the dual-aperture reading in §6.3.

Section 2 sets the programme context. Section 3 specifies the two pre-registered hypotheses and their decision rules. Section 4 details the methods. Section 5 reports results. Section 6 discusses the PARTIAL boundary finding, the discourse-language carryforward, the dual-aperture asymmetry, and v0.16's contribution to the AIAS programme. Sections 7 and 8 cover limitations and next steps.

# 2. Background: Regime 4 and the v0.8 Discourse-Language Lineage

The four-regime taxonomy [@gonzalezcastro2026fourregimes] classifies brand–category substrates by the structural relationship between AI Presence and Google Trends search interest. Regime 1 (Trends-tracking strong) shows high positive bivariate ρ that remains positive after covariate control. Regime 2 (Trends-tracking moderate) shows moderate positive bivariate ρ with moderate covariate decrement. Regime 3 (Scale-mismatch low-n) describes substrates where small-cell eligibility prevents inferential evaluation. **Regime 4 (Covariate-saturated weak)** is the diagnostic locus of this paper: |bivariate ρ(AI, Trends)| < 0.35 AND partial ρ(AI, Trends | brand_age, tradition_cell) < 0. Bivariate decoupling combined with negative residual association is the signature of a substrate in which AI Presence is structurally weak in tracking consumer-search interest and where the controllable confounds (age, tradition) do not rescue the relationship.

The Regime 4 cluster currently includes three confirmed substrates: premium facial skincare (v0.11; SSRN 6745040), personal finance apps (v0.13; SSRN 6750498), and premium tea (v0.14/v0.15; SSRN 6755621 and 6768059). Each substrate landed in Regime 4 under canonical pre-registered conditions at both waves. v0.16 tests whether kitchen knives extends this cluster to a fourth substrate, or — alternatively — lands at one of the regime boundaries.

The v0.8 Discourse-Language Knives paper [@gonzalezcastro2026discoursetext] was conducted *before* the construct-validity eligibility panel and the four-regime taxonomy were formalized. v0.8 documented an asymmetric finding: Japanese-tradition knife brands (Shun, Global, Mac, Miyabi) generated substantially different AI Presence rankings under English-language category-recommendation prompts vs equivalent Japanese-language prompts. The finding was publishable on its own terms but did not employ the v1.2 protocol's full construct-validity panel — Phase A pivot validation, Phase B topic-ID resolution, E1a/E1b/E5 eligibility tiers, or the n = 12 inferential floor. v0.16 returns to the v0.8 substrate with the full canonical protocol, providing an empirical test of whether the original v0.8 finding was an artifact of pre-v1.2 measurement or a substantive observation about AI-mediated brand surfacing.

The "identity-load" parameter of the Tri-System Brand Growth framework [@gonzalezcastro2026trisystem] places kitchen knives at medium identity-load — a clearer connoisseurship signal than tea, finance, or skincare, but well below fragrance or luxury watches. This positioning is methodologically productive: a confirmed Regime 4 classification would extend the regime's empirical floor across identity-load conditions, not only at the low-identity-load floor where the regime was established. A falsified classification would directly support the hypothesis that Regime 4 is bounded by identity-load below a threshold yet to be specified.

# 3. Pre-registration and Hypotheses

All thresholds, decision rules, and analysis-plan specifications were locked at git tag `v0.16-prereg` (commit `511e339`) on 16 May 2026 UTC, prior to any LLM acquisition call against the wave windows. The pre-registration document is deposited in the OSF project at `/v16/PRE_REGISTRATION_v0_16.md` and is mirror-deposited at `~/aias/registries/PRE_REGISTRATION_v0_16.md` in the canonical repository.

## 3.1 Primary hypothesis: H_Regime4_replication_knives

**Statement.** Brand AI Presence on the kitchen-knives substrate exhibits the canonical Regime 4 (Covariate-saturated weak) signature established on premium facial skincare (v0.11), personal finance apps (v0.13), and premium tea (v0.14, v0.15).

**Operationalization.** Per AIAS Presence Measurement Protocol v1.2 §3.4 [@gonzalezcastro2026protocolv12]. All correlations are Spearman ρ on per-brand rank data. Conditions must hold at both waves t~1~ and t~2~.

**Decision rules.**

| Verdict | Conditions |
|---|---|
| **CONFIRMED** | (1) n_eligible ≥ 12 ∧ (2) \|ρ(AI, Trends)\| < 0.35 ∧ (3) partial ρ(AI, Trends \| age, tradition) < 0 |
| **PARTIAL** | (1) and (2) hold but (3) fails — non-saturated weak signature; productive boundary finding |
| **FALSIFIED** | (1) fails OR (2) fails — productive falsification |

Controls in Condition 3's partial correlation: brand_age (continuous, rank-transformed) + tradition_cell (categorical dummies, k_adj = 5 for the five-cell panel under tradition-cell with one reference cell omitted).

PARTIAL is a v0.16 refinement of v0.15's binary CONFIRMED/FALSIFIED structure. It names a specific substantive pattern that v0.15-canonical would have collapsed to FALSIFIED: bivariate decoupling holds (the central Regime 4 diagnostic), but the residual association after covariate control does not deepen into the negative-partial signature. The PARTIAL tier is not a contradiction of v0.15 canonical — it is a strict sub-classification.

## 3.2 Exploratory hypothesis: H_Discourse_Language_carryforward

**Statement.** The v0.8 Discourse-Language Bias finding on knives — that non-English-discourse-anchored brands (the Japanese tradition cell in particular) underperform in English-language prompt conditions relative to discourse-language-matched conditions — holds under v1.2 protocol with corrected eligibility filtering.

**Operationalization.** Computed on the Japanese tradition cell as anchor cell for the v0.8 finding. For each Japanese-cell brand, compute its AI Presence under (a) the English-language category-recommendation prompt and (b) the equivalent Japanese-language prompt. Rank-correlate the two vectors across brands.

**Decision rules.**

| Verdict | Condition |
|---|---|
| **CARRY-FORWARD CONFIRMED** | n_japanese ≥ 5 ∧ ρ(English, native-language) < 0.85, both waves |
| **CARRY-FORWARD WEAKENED** | n_japanese ≥ 5 ∧ ρ ∈ [0.85, 0.95), both waves |
| **CARRY-FORWARD FALSIFIED-favorable** | n_japanese ≥ 5 ∧ ρ ≥ 0.95, both waves — v0.8 finding was pre-v1.2 protocol artifact corrected by v1.2 |
| **INCONCLUSIVE** | n_japanese < 5 |

## 3.3 Pre-registered deviations from v0.15 paper structure

v0.15 (and earlier v0.13/v0.14) pre-registrations included a battery of construct-validity hypotheses H1–H4 (per-category bivariate, cross-wave stability, leadership-zone subset, partial Spearman) and a regime-classification hypothesis H7. v0.16 pre-registration does *not* include these as separate hypotheses; their information content is subsumed in the two pre-registered hypotheses above plus the descriptive observations developed in §5.3 and §6.3. The v0.16 paper accordingly does not report H1–H4 or H7 results.

# 4. Methods

## 4.1 Panel construction

The v0.16 brand panel comprises 22 non-pivot primary brands stratified across five tradition cells, with Victorinox as pre-registered Phase A pivot (replaced by Wüsthof at Phase A; see §4.3). The cells are:

- **Japanese** (n = 6): Shun, Global, Miyabi, Mac, Tojiro, Yoshihiro
- **German** (n = 5 primary − 1 pivot reassigned): Wüsthof (pivot, exits cell), Zwilling J.A. Henckels, Messermeister, Güde, Friedr. Dick
- **French** (n = 4 after alternate activation): Sabatier, Opinel, Laguiole, Au Nain (activated; Nogent EXCLUDED_E1a)
- **American specialty** (n = 5): Cutco, Dalstrong, Misen, New West KnifeWorks, Made In
- **Chinese** (n = 3 after alternate-pool exhaustion): Sunlong, ZHEN, Hengtai (activated; primary brands CCK Chan Chi Kee, Shibazi failed Phase B topic-ID; alternates Hu Si Chao and Dengjia also EXCLUDED_E1a)

The Japanese tradition cell is the anchor cell for H_Discourse_Language_carryforward; the six-brand cell exceeds the n = 5 inferential floor.

## 4.2 Measurement waves

Two waves separated by 14 days: t~1~ April 27 – May 3, 2026; t~2~ May 4 – May 10, 2026. Wave windows are pre-registered and locked at git tag `v0.16-prereg`.

## 4.3 Phase A and Phase B

**Phase A pivot validation.** Pre-registered pivot Victorinox failed canonical-query Trends eligibility (EXCLUDED_E1a — kitchen-knife brand presence below Trends-eligibility floor on the bare canonical query). Per pre-reg §6 contingency, Wüsthof was activated as pivot; the German cell reduces by one brand and Wüsthof exits within-cell scoring. DEVIATIONS Entry 3 (deposited in OSF `/v16/DEVIATIONS.md`) documents the operational handling.

**Phase B topic-ID resolution.** Per v1.2 §4 five-stage protocol. Two pre-registered primary brands required alternate activation: Hu Si Chao and Dengjia (Chinese cell primaries) both EXCLUDED_E1a; Hengtai activated from alternates and passed. Au Nain (French cell alternate) activated after Nogent EXCLUDED_E1a. DEVIATIONS Entry 4 documents the alternate-activation sequence. The Chinese cell stops at n = 3 after alternate-pool exhaustion — pre-reg §6 cell-collapse contingency retains the cell for descriptive reporting with explicit underpower flag.

## 4.4 LLM acquisition and AI Presence

AI Presence is computed across six LLM slots: Anthropic Sonnet 4.6, Anthropic Opus 4.7, OpenAI gpt-5.4-mini, OpenAI gpt-5.5, Google gemini-2.5-flash, xAI grok-4-1-fast-reasoning. All responses at provider status = ok. The full acquisition produced 960 cells (20 prompts × 6 model slots × 8 runs); function-calling extraction enriched all 960 with zero errors. Per-model breakdowns and the matched-model subset specification are documented in the canonical scoring script (`score_v16.py`) at git commit `511e339` (same as pre-reg tag).

## 4.5 Scoring

Per pre-reg §5. All Spearman correlations computed on per-brand rank data. Partial correlations control for brand_age (continuous, rank-transformed) and tradition_cell (categorical dummies). df adjustment per v0.15-canonical implementation. Worldwide-region cell is inferential primary; US-region cell is descriptive sensitivity when n < 12. Tea Box-excluded sensitivity (carried forward from v0.14) does not apply at v0.16 because Tea Box is a tea-substrate brand not in the v0.16 kitchen-knives registry. All scoring outputs (canonical_scoring.csv/json, per_brand_paired.csv, h_regime4_replication_knives.csv, h_discourse_language_carryforward.csv) are deposited in the OSF project at `/v16/analysis/`.

# 5. Results

## 5.1 H_Regime4_replication_knives PARTIAL

The worldwide primary panel satisfies two of three pre-registered conditions and fails the third.

- **C1 (n ≥ 12).** Satisfied at both waves: n = 13.
- **C2 (|bivariate ρ(AI, Trends)| < 0.35).** Satisfied with substantial margin: ρ = +0.022 at t~1~ and +0.003 at t~2~.
- **C3 (partial ρ(AI, Trends | age, tradition) < 0).** Fails at both waves: partial ρ = +0.101 at t~1~ and +0.080 at t~2~ (positive rather than negative).

Per pre-reg §2 decision rules: **PARTIAL**. The bivariate decoupling diagnostic holds with margin (correlation magnitudes near zero, well within the C2 threshold); the conservative covariate-saturated test fails because the residual association after age and tradition control is slightly positive rather than negative.

The 13 worldwide-eligible brands: Tojiro, Yoshihiro, Zwilling J.A. Henckels, Messermeister, Güde, Sabatier, Opinel, Laguiole, Cutco, Dalstrong, Sunlong, ZHEN, Au Nain. Five-cell representation: 2 Japanese, 3 German, 4 French, 2 American, 2 Chinese.

The pre-registered Tea Box-excluded sensitivity is not applicable at v0.16 (Tea Box is not in the kitchen-knives registry; the sensitivity was carried forward from v0.14 tea-substrate work). No other within-panel sensitivities were pre-registered.

![Regime 4 canonical classification: each AIAS-programme category at (bivariate Spearman ρ × partial Spearman ρ), worldwide, with t~1~→t~2~ connectors. Kitchen knives v0.16 sits at bivariate decoupling (|ρ| < 0.35 satisfied with substantial margin) but with slightly positive partial ρ after age + tradition control — the PARTIAL verdict tier, a productive boundary case for Regime 4 rather than a fourth-substrate canonical confirmation.](../figures/chart_v16_regime4_canonical.pdf){width=6.5in}



## 5.2 H_Discourse_Language_carryforward CARRY-FORWARD CONFIRMED

The Japanese tradition cell anchor analysis exceeds both pre-registered thresholds.

- **n_japanese ≥ 5.** Satisfied: n = 6 (Shun, Global, Miyabi, Mac, Tojiro, Yoshihiro).
- **ρ(English-prompt AI Presence, Japanese-prompt AI Presence) < 0.85, both waves.** Satisfied with substantial margin: ρ~t~~1~ = +0.197; ρ~t~~2~ = −0.149.

Per pre-reg §2 decision rules: **CARRY-FORWARD CONFIRMED**. Both correlations sit far below the 0.85 threshold, with t~2~ actually slightly negative. The brands the LLM panel surfaces when prompted in English are not the same brands (in the same relative ranking) it surfaces when prompted in Japanese, even within the same six-brand Japanese tradition cell. The v0.8 finding survives v1.2 protocol with corrected eligibility filtering.

![H_Discourse_Language_carryforward, Japanese tradition cell (Shun, Global, Miyabi, Mac, Tojiro, Yoshihiro; n = 6). Per-brand AI Presence under the English-language category-recommendation prompt (x-axis) vs the equivalent Japanese-language prompt (y-axis), at t~1~ (left) and t~2~ (right). ρ at t~1~ = +0.197; ρ at t~2~ = −0.149 — both far below the 0.85 CARRY-FORWARD CONFIRMED threshold. The v0.8 finding survives v1.2 protocol with corrected eligibility filtering.](../figures/chart_v16_discourse_language_pair.pdf){width=6.5in}



## 5.3 US/worldwide divergence (descriptive sensitivity)

Per pre-reg §2, the US-region panel is descriptive sensitivity when n < 12. v0.16's US panel sits at n = 10 at both waves; three brands fall out of US-region eligibility:

- **Güde** (German tradition): worldwide Trends signal supports eligibility; US-region signal at 14-day-zero floor
- **Sunlong** (Chinese tradition): same pattern
- **Au Nain** (French tradition): same pattern

Descriptive correlations on the US panel read strongly negative on both waves:

- Bivariate ρ = −0.881 at t~1~ and −0.812 at t~2~
- Partial ρ = −0.940 at t~1~ and −0.708 at t~2~

The worldwide panel reads near-zero bivariate correlation; the US panel reads strongly negative. The pattern is not symmetric across regions. The three dropped brands are all *foreign-tradition* (German, Chinese, French) — their worldwide AI Presence is generated by LLMs trained on multilingual corpora and serves multilingual queries; their US-region Google Trends signal is constrained by the English-language consumer-search environment in the US Trends aperture. The US/worldwide divergence is itself a substantive observation about the asymmetry between AI-mediated brand surfacing and English-language US consumer search — addressed in §6.3 alongside the discourse-language finding.

![v0.16 panel per-tradition small-multiples. Five tradition cells with per-cell axes (magnitudes vary substantially across cells). The Japanese cell (n = 6) anchors H_Discourse_Language_carryforward. The Chinese cell at n = 3 — after primary-brand topic-ID failures and alternate-pool exhaustion — is the smallest cell in the panel and retained for descriptive reporting per pre-reg §6 cell-collapse contingency. Markers: t~1~ (filled) and t~2~ (open).](../figures/chart_v16_kitchen_knives_per_tradition.pdf){width=6.5in}



# 6. Discussion

![Per-category construct validity across the AIAS programme. Kitchen knives v0.16 reads bivariate ρ near zero (within C2 threshold |ρ| < 0.35) but partial ρ slightly positive (failing C3 partial ρ < 0) — the PARTIAL boundary verdict. The Regime 4 cluster's three canonical confirmations (skincare v0.11, finance v0.13, premium tea v0.14/v0.15) show deeper inverse partial ρ; kitchen knives v0.16 documents the regime's identity-load boundary rather than extending the canonical cluster.](../figures/chart_v16_per_category_rho_comparison.pdf){width=6.5in}



## 6.1 The PARTIAL verdict: identity-load boundary

H_Regime4_replication_knives PARTIAL is the headline finding of v0.16, and the verdict tier most worth interpreting carefully. PARTIAL is *not* falsification: condition C2, the central Regime 4 diagnostic of bivariate decoupling between AI Presence and Trends, holds with substantial margin (ρ near zero at both waves). PARTIAL is *not* confirmation: condition C3, the conservative covariate-saturated test of negative residual association after age and tradition control, fails by a small positive margin (+0.101 / +0.080) at both waves.

The substantive interpretation is that kitchen knives exhibits the weak-coupling diagnostic of Regime 4 but does not exhibit the negative-residual covariate-saturated signature. In the three previously-confirmed Regime 4 substrates (skincare, finance, tea), the residual association after controls was negative at both waves — a structural pattern in which brand age and tradition-cell membership do not rescue the AI–Trends relationship and the residual co-movement is *inversely* signed. v0.16 kitchen knives does not produce this inverted residual pattern.

A direct candidate explanation is identity-load. Kitchen knives carry medium identity-load — a clearer connoisseurship signal than tea, finance, or skincare. The Tri-System framework [@gonzalezcastro2026trisystem] hypothesizes that AI Availability dynamics differ by identity-load: low-identity-load substrates support the canonical Regime 4 inversion because consumers under low identity-load defer to AI recommendation broadly, generating brand-surface patterns where AI-visibility and search-interest are weakly coupled and even inversely associated after covariate control. At higher identity-load, consumers integrate AI recommendation with their own connoisseurship signals — and the resulting brand-surface pattern is more idiosyncratic. The PARTIAL verdict at v0.16 is consistent with kitchen knives sitting at the identity-load boundary where the canonical Regime 4 signature attenuates rather than reverses.

This interpretation is hypothesis-generating rather than confirmatory. v0.16's pre-registration did not specify identity-load as a moderating variable; the PARTIAL verdict supports developing identity-load as a pre-registered moderator in future programme phases.

## 6.2 Discourse-language carryforward under canonical protocol

H_Discourse_Language_carryforward CARRY-FORWARD CONFIRMED closes the v0.8 lineage under canonical pre-registered protocol. The original v0.8 Discourse-Language Knives finding [@gonzalezcastro2026discoursetext] was conducted before the v1.2 construct-validity eligibility panel existed; it was publishable on its own terms but did not employ the canonical Phase A / Phase B resolution, the eligibility tiers, or the four-regime taxonomy. v0.16 demonstrates that the v0.8 finding survives v1.2 protocol: on the six-brand Japanese tradition cell, English-prompt and Japanese-prompt AI Presence rankings differ substantially (ρ = +0.197 at t~1~, −0.149 at t~2~ — far below the 0.85 CONFIRMED threshold).

The finding is now a documented carryforward — no longer a one-paper observation but an empirical regularity available for downstream programme work. Specifically, it supplies an empirical anchor for the Tri-System framework's argument that AI Availability has language and region dependencies absent from classical search-interest measures.

## 6.3 US/Worldwide divergence as second measurement aperture

Pattern 1's US/worldwide divergence and Pattern 2's discourse-language CONFIRMED are two views of the same structural property. The US-region panel measures a region-induced registry-coverage effect: US sparsity drops three foreign-tradition brands from the eligible panel because their US-region Trends signal is at floor. The discourse-language test measures a prompt-language-induced ranking effect: English-prompt vs Japanese-prompt rankings on the same six Japanese-cell brands diverge sharply. Both surface a structural property of AI Availability that classical brand-equity measures (Google Trends search interest) do not symmetrically capture: AI mediation for foreign-tradition brands has language and region dependencies absent from English-language US search-interest measures.

The dual-aperture reading strengthens both findings. The discourse-language carryforward is no longer a single-aperture observation tied to a specific prompt-language operationalization — it is one of two methodologically distinct measurement apertures producing the same structural inference. The US/worldwide divergence is no longer an artifact of which brands made it into a specific eligibility cell — it is the same underlying asymmetry as the prompt-language test, surfacing via a different measurement choice.

The dual-aperture framing also clarifies what v0.16 does *not* claim. The US-region bivariate ρ of −0.881 is descriptive sensitivity per pre-reg §2 — the n = 10 panel sits below the inferential floor. The claim is not "Regime 4 confirmed in US-region kitchen knives." The claim is: when the measurement aperture narrows from worldwide to US-region, the panel composition shifts (three foreign-tradition brands drop out), and the descriptive correlations on the smaller panel are strongly negative. This is structurally informative — it documents the asymmetry between AI-mediated worldwide brand surfacing and US-region search-interest measurement. It is not a parallel inferential verdict.

## 6.4 v0.8 lineage closure

The combined v0.16 reading methodologically closes the v0.8 lineage. v0.8 surfaced the discourse-language finding before v1.2 protocol existed; v0.16 reproduces the finding under v1.2's canonical construct-validity panel with full pre-registration discipline (tag `v0.16-prereg` at commit `511e339`) and full data transparency via the OSF deposit. The Discourse-Language Carryforward is documented under canonical protocol, available for future AIAS programme work that implicates AI Availability's language and region dependencies.

The Regime 4 reading does not close — it opens the regime's identity-load boundary as a productive line of inquiry. Future programme phases may revisit kitchen knives or related medium-identity-load substrates (premium kitchenware, single-origin chocolate, specialty coffee) with identity-load as a pre-registered moderator.

# 7. Limitations

**Single substrate at v0.16.** v0.16 tests kitchen knives as the fourth-substrate Regime 4 test. The PARTIAL verdict documents a regime-boundary observation on a single substrate; the cross-substrate triangulation that the Regime 4 cluster's three confirmed substrates supply (skincare, finance, tea) is not extended at v0.16.

**Two-wave short window.** Both waves are within 14 days. Cross-wave stability of the Regime 4 signature at month-to-month or quarter-to-quarter horizons is not tested at v0.16. v0.16's wave windows align with the protocol's standard two-week locked acquisition window per v1.2 §3.4.

**Six-LLM panel at status = ok.** AI Presence is computed across six LLM slots from four providers. The six-slot panel factors variation across providers but does not decompose it. Per-model AI Presence breakdowns are available in the OSF deposit's `/v16/analysis/per_brand_paired.csv` augmented by per-model intermediate outputs.

**Single external validator.** Construct validity is tested against Google Trends as sole external consumer-search reference. A multi-validator design (search interest plus social-media mentions, retail sales data, consumer-survey aided recall) is the medium-term goal of the AIAS programme (Phase 3).

**US-region panel below inferential floor.** The pre-registered US-region cell sits at n = 10 — below the n = 12 inferential floor. The strongly-negative US correlations are reported as descriptive sensitivity per pre-reg §2, not as a parallel verdict. The US/worldwide divergence is itself a substantive observation (§5.3, §6.3), but cannot be inferentially generalized at v0.16 without panel expansion adding US-eligible foreign-tradition brands.

**Chinese cell at n = 3 after alternate-pool exhaustion.** The Chinese cell is retained for descriptive reporting per pre-reg §6 cell-collapse contingency but is the smallest cell in the panel. The cell's structural smallness reflects under-representation of Chinese-tradition kitchen-knife brands in English-language Google Trends signal at v0.16's acquisition timestamp — a substrate-specific Trends-coverage observation worth flagging for downstream interpretation.

**Phase A pivot fallback.** v0.16 Phase A pivot validation surfaced a contingency that Protocol v1.2 does not centrally specify: Victorinox (pre-registered pivot) EXCLUDED_E1a, requiring Wüsthof activation per pre-reg §6. The forward action is a methodology-paper v1.3 increment specifying pivot-validation criteria centrally.

# 8. Conclusion and Next Steps

v0.16 lands two pre-registered verdicts on the kitchen-knives substrate. H_Regime4_replication_knives **PARTIAL** — a productive boundary finding rather than a falsification or a fourth-substrate canonical confirmation; bivariate decoupling holds, conservative covariate-saturated test fails. H_Discourse_Language_carryforward **CARRY-FORWARD CONFIRMED** — the v0.8 finding survives v1.2 protocol on the Japanese tradition cell. A subsidiary descriptive observation surfaces the same brand-asymmetry via a second measurement aperture: foreign-tradition brands fall out of US-region eligibility because their US-region Trends signal is at floor; the US-region panel reads strongly negative as descriptive sensitivity.

**Next steps in the AIAS programme.** (1) The methodology-paper v1.3 increment specifying Phase A pivot-validation criteria centrally. (2) Identity-load as a pre-registered moderator in future Regime 4 tests, motivated by v0.16's PARTIAL verdict. (3) Phase 4 — measurement work on the five remaining AIAS components (Ranking, Consistency, Coverage, Grounding, Sentiment) — anchored against the four-substrate construct-validity baseline that now includes the kitchen-knives PARTIAL. (4) The Tri-System Brand Growth framework (MSI Working Paper) bibliography updated to incorporate v0.16 alongside v0.13, v0.14, v0.15, and AIAS Protocol v1.2 (SSRN 6761698).

# Acknowledgments

The author acknowledges the AIAS Presence Measurement Programme's iterative development across v0.6–v0.15 and the methodological foundations supplied by the Ehrenberg-Bass tradition [@sharp2010; @sharp2021; @romaniuk2018]. The author thanks the open-data and open-science infrastructure provided by the Open Science Framework and SSRN, which together enable the programme's pre-registration discipline and full data-transparency commitments.

# Declarations

**Funding.** Self-funded. No external research funding or sponsorship.

**Conflict of Interest.** The author is Director, Corporate Brand Creative & Governance, at Samsung Electronics America. The AIAS programme is conducted independently of this employment relationship; Samsung has no role in the research design, data acquisition, analysis, manuscript preparation, or submission of this work. The author's academic affiliation (School of Visual Arts, MPS Branding Program, New York, NY) is the primary academic affiliation; Third System™ is the independent research entity through which the AIAS programme is conducted.

**Ethics approval.** Not applicable. No human subjects; data sources are public APIs (LLM provider APIs) and Google Trends.

**Pre-registration.** All hypotheses, thresholds, decision rules, panel composition, alternate-activation rule, and contingency handling were locked at git tag `v0.16-prereg` (commit `511e339`) on 16 May 2026 UTC prior to LLM acquisition. The pre-registration is deposited at OSF `/v16/PRE_REGISTRATION_v0_16.md`.

# Data Availability

All data, pre-registration, analysis code, charts, the brand-format report, and this paper are deposited at the OSF project `ec6wh`, `/v16/` (https://osf.io/ec6wh/). The deposit includes:

- `PRE_REGISTRATION_v0_16.md` — canonical pre-registration locked at git tag `v0.16-prereg` (commit `511e339`)
- `analysis/canonical_scoring.json` and `canonical_scoring.csv` — per-region per-wave correlation matrices
- `analysis/per_brand_paired.csv` — per-brand AI Presence × Trends data
- `analysis/h_regime4_replication_knives.csv` — primary hypothesis verdict + conditions
- `analysis/h_discourse_language_carryforward.csv` — exploratory hypothesis verdict + numerics
- `figures/` — five chart PDFs (canonical regime classification; per-category ρ comparison; discourse-language pair; per-brand AI × Trends scatter; per-tradition small-multiples)
- `reports/v16_kitchen_knives.pdf` — brand-format report (Third System™ template)
- `DEVIATIONS.md` — pre-registered deviations log (Entry 3: Phase A pivot fallback; Entry 4: alternate activation)
- `MANIFEST.md` — file-level provenance

The canonical scoring script (`score_v16.py`) and chart-build scripts are version-locked to the same git commit (`511e339`) as the pre-registration tag.

# References

<!-- PAPER_V16_CITEPROC_BIB — references generated by pandoc citeproc from references.bib -->

::: {#refs}
:::
