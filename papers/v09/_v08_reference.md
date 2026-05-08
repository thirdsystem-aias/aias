---
documentclass: article
geometry: margin=1in
fontsize: 11pt
mainfont: Carlito
header-includes:
  - \usepackage{setspace}
  - \setstretch{1.36}
  - \setlength{\parskip}{8pt}
  - \setlength{\parindent}{0pt}
  - \usepackage{float}
  - \floatplacement{figure}{H}
  - \usepackage{caption}
  - \captionsetup[figure]{font=small,labelfont={bf,it},textfont=it,justification=raggedright,singlelinecheck=false}
  - \usepackage{titlesec}
  - \titleformat{\section}{\Large\bfseries}{\thesection.}{0.5em}{}
  - \titleformat{\subsection}{\large\bfseries}{\thesubsection}{0.5em}{}
---

\begin{center}
\setlength{\parskip}{10.36pt}

\vspace{2em}

SSRN WORKING PAPER

\vspace{1em}

{\fontsize{16}{21.76}\selectfont\bfseries A Designed-for-Test Measurement of Discourse-Language Bias in Large Language Model Brand Recommendations}

\textit{Pre-Registered Evidence from Premium Kitchen Knives, with Marketing-Language Coverage as the Candidate Mechanism}

Working Paper · Version 0.8 · Designed-for-Test (Premium Kitchen Knives)

\vspace{2em}

Pablo Ulpiano González Castro

School of Visual Arts, MPS Branding Program, New York, NY \\
(primary academic affiliation)

Third System\textsuperscript{™} (research entity; data archive and methodology venue)

Correspondence: pablou@pablou.com · pablou.com

ORCID: https://orcid.org/0009-0003-8968-9990

\vspace{1em}

6 May 2026

\textit{Working paper. Not under peer review. Pre-registered.}

\end{center}

\newpage

# Abstract {-}

This paper reports a designed-for-test measurement of discourse-language bias in large language model (LLM) brand recommendations for premium kitchen knives — a category dominated in production and chef reputation by Japan but mediated in English-language coverage through US/UK food media. Thirty-three brands across four lineages (Japanese, German, American, shared) plus one hybrid (Miyabi) were measured against six pre-registered prompts anchored to Category Entry Points, six frontier models from four labs (Anthropic Claude Sonnet 4.6 and Opus 4.7, OpenAI gpt-5.4-mini and gpt-5.5, Google Gemini 2.5 Flash, xAI Grok 4.1 Fast), and eight runs each (n = 288 successful measurements). Eight hypotheses with explicit numerical thresholds were committed to a pre-registration document locked at git commit d3e0989 prior to any data collection.

The headline lineage-aggregate hypothesis (H1) was disconfirmed at both registry versions. At the locked v1.0 registry (21 brands), Japanese aggregate Presence was 36.2 percent versus German 27.3 percent — an 8.9-point gap in the wrong direction. At the published v1.2 registry (33 brands, 19 Japanese standard plus 1 hybrid, after the registry-revision protocol added boundary-condition makers from the unknown-mentions list), Japanese aggregate fell to 25.7 percent and German held at 27.2 percent — a 1.5-point gap in the predicted direction but below the 5-point partial-confirmation threshold. The lineage-aggregate hypothesis therefore fails consistently across registry construction.

The within-lineage results carry a different signal entirely. Within Japanese, mass-market English-marketed brands (Shun, Global, Mac) surface at 55.2 percent versus 6.8 percent for the fourteen boundary-condition Japanese makers in the canonical scoring — a 48.4-percentage-point gap and approximately 8x ratio. Within German, the boundary case (Güde) appears in zero of 288 measurements while English-marketed German makers (Wüsthof, Henckels) average 62.0 percent. Within the boundary-condition Japanese cohort itself, seven brands clear the 5-percent floor and two stand markedly apart at the upper end: Masamoto at 18.1 percent and Takamura at 16.7 percent — both characterized by substantial US-targeted English-language distribution and chef-endorsed English-media coverage. Of 262 named authority mentions across all 288 measurements, 100 percent are English-language; no Japanese, German, French, or other-language sources surface in any response.

A secondary finding replicates across providers: newer-generation models within both Anthropic (Opus 4.7 versus Sonnet 4.6) and OpenAI (gpt-5.5 versus gpt-5.4-mini) surface boundary-condition Japanese brands at higher rates than their older counterparts — the second cross-category replication of a "newer models surface boundary cases more, not less" pattern in the AIAS measurement program.

The lineage-aggregate failure (H1) and the within-lineage convergence (H3, H5, H8) together motivate a candidate alternative framing: *marketing-language coverage as a brand-level mediator* of AI brand presence in cross-lingual categories. Brands with substantial English-language marketing infrastructure surface at materially higher rates than equivalently positioned brands without such infrastructure, *within* every lineage of origin tested. The framing is offered as a candidate hypothesis adjacent to but structurally distinct from existing AI-Surfacing hypotheses (Default Reinforcement; recommendation-slot persistence; freshness-lag). It predicts that brand-level English-marketing investment, not lineage of origin, is the binding variable for AI Presence in cross-lingual categories. Construct validity remains open and is the proposed object of a Phase 3 designed-for-confirmation study.

# Keywords {-}

AI brand visibility; marketing-language coverage; discourse-language bias; cross-lingual recommendation; pre-registered measurement; designed-for-test methodology; brand-visibility measurement; large language models; AIAS

# JEL Classification {-}

M31 (Marketing) — primary; L86 (Information and Internet Services; Computer Software); L15 (Information and Product Quality); D83 (Search; Learning; Information and Knowledge; Communication; Belief; Unawareness)

# Paper status {-}

Working paper. Not under peer review. Designed-for-test follow-up study in the AIAS measurement program. Builds on Pattern 4 (discourse-language bias) observations from González Castro (2026), "AI Presence Measurement Across Consumer Categories" (SSRN ID 6720959). Companion empirical artifact to González Castro (2026), "AI Availability: Extending Mental and Physical Availability into Algorithmic Retrieval" (SSRN ID 6659000). Methodological reference: González Castro (2026), "AIAS Presence Measurement Protocol v1.1" (SSRN ID 6722319). Adjacent designed-for-test study: González Castro (2026), "A Designed-for-Test Measurement of Phantom-Brand Presence in Large Language Model Outputs" (SSRN ID 6721779). Pre-registration document (PRE_REGISTRATION_knives_v1.0.md, locked at git commit d3e0989) and underlying datasets released alongside this paper at osf.io/ec6wh/.

\newpage

# 1. Introduction

In the cross-category baseline reported as v0.6 of the AIAS measurement program (González Castro 2026, "AI Presence Measurement Across Consumer Categories"), a structural property of LLM-mediated brand visibility was observed across two cross-lingual categories that no other pattern in the dataset captured. In premium olive oil and premium facial skincare, brand-presence rates appeared to track English-language marketing infrastructure rather than category positioning, brand origin, or production heritage. The observation was termed *discourse-language bias* and registered as Pattern 4 of the v0.6 cross-category framework. Two-category support is substantively suggestive but not designed-for-test. The question of whether discourse-language bias is a structural property of LLM-mediated brand visibility — versus an artefact of two adjacent categories' discourse profiles — required a measurement designed explicitly to test the mechanism rather than to map it.

Premium kitchen knives were selected as the designed-for-test target. The category satisfies four structural criteria that no other category in the AIAS candidate set satisfies as cleanly. First, Japan dominates premium production and chef reputation, providing the boundary lineage where the mechanism predicts the largest gap between English-marketed and non-English-marketed brands. Second, English-language category coverage is concentrated in identifiable US/UK food media — Sur La Table, Serious Eats, Williams-Sonoma, Wirecutter, Amazon, America's Test Kitchen — making the discourse-language-mediation hypothesis directly observable in authority citations. Third, Germany and the United States provide structurally analogous lineages on the same product, allowing within-product comparison rather than cross-product confound. Fourth, within the Japanese cohort, two brands have substantially developed US-targeted English-language infrastructure (Masamoto operates masamoto.us; Takamura is endorsed by named chefs in English-language food media) while the remainder do not — allowing a within-Japanese variance test that holds lineage and quality constant while varying discourse-language coverage.

Eight hypotheses with explicit numerical thresholds were committed to a pre-registration document (PRE_REGISTRATION_knives_v1.0.md) locked at git commit d3e0989 prior to any data collection (Nosek et al. 2018). The hypotheses isolated specific candidate mechanisms: lineage-aggregate comparison (H1); American-comparator behavior (H2); within-Japanese mass-market versus traditional gap (H3); per-prompt variance (H4); within-German boundary case (H5); cross-lab newer-versus-older model variance (H6); authority-citation language composition (H7); and boundary-condition cohort floor effect (H8). Pre-registered predictions and outcomes are reported as Table 1 in §4.

The locked v1.0 registry comprised twenty-one brands across three lineages plus one hybrid; per the pre-registered registry-revision protocol (AIAS Presence Measurement Protocol v1.1 §2.4), twelve additional Japanese brands surfaced in the unknown-mentions list during data extraction at non-trivial rates and were added to the registry, producing the published v1.2 registry of thirty-three brands (19 Japanese standard, 1 Japanese hybrid, 5 German, 5 American, 3 shared). The canonical scoring was performed against the v1.2 registry. The H1 hypothesis is reported against both v1.0 and v1.2 for transparency about how lineage-aggregate values move with registry construction.

The headline lineage-aggregate result was disconfirmed at both registry versions. At v1.0 (locked, 21 brands), Japanese aggregate AI Presence was 36.2 percent and German aggregate was 27.3 percent — an 8.9-point gap in the *opposite* direction of the H1 prediction. At v1.2 (published, 33 brands), Japanese aggregate fell to 25.7 percent and German aggregate held at 27.2 percent — a 1.5-point gap *in* the predicted direction but below the 5-point partial-confirmation threshold. The lineage-aggregate hypothesis fails consistently regardless of how the registry is constructed. The 10.5-percentage-point shift in Japanese aggregate between the two versions is itself informative — adding boundary-condition Japanese brands moves the aggregate, but never enough to confirm a lineage-level prediction at the pre-registered threshold.

The within-lineage findings tell a different and more tightly supported story. Within Japanese: mass-market English-marketed brands (Shun, Global, Mac) surface at 55.2 percent versus 6.8 percent for the fourteen boundary-condition Japanese makers in the canonical scoring — a 48.4-percentage-point gap and approximately 8x ratio (H3 confirmed at strongest level). Within German: the boundary case (Güde, a 240-year-old Solingen maker with negligible US-targeted English-language presence) appears in zero of 288 measurements while English-marketed German makers (Wüsthof at 68.4 percent, Henckels at 55.6 percent) average 62.0 percent (H5 confirmed at strongest possible form). Within the boundary-condition Japanese cohort itself: seven of the fourteen brands clear the 5-percent floor, with two standing markedly apart at the upper end — Masamoto at 18.1 percent and Takamura at 16.7 percent. Both are characterized by substantial US-targeted English-language distribution and chef-endorsed English-media coverage. Sakai Takayuki (10.8 percent), Konosuke (9.7 percent), Korin (8.3 percent), Nigara Hamono (5.9 percent), and Yu Kurosaki (5.2 percent) cluster in a middle band. Six brands surface below 5 percent (H8 partially confirmed at 6.8 percent aggregate, in the 5–15 percent partial band).

The authority-citation composition further tightens the brand-level framing. Of 262 named authority mentions across all 288 measurements (publications, retailers, online communities), 100 percent are English-language. No Japanese, German, French, or other-language sources surface in any response. The discourse infrastructure that LLMs draw on for premium kitchen knife recommendations is exclusively English. H7 was reframed per AIAS Protocol §6.4 (the locked threshold required ≥ 90 percent of authority-mode responses to be English; the locked operationalization had insufficient denominator at two of 288 strict-mode rows; the reframe scored authority naming across all responses against the same threshold) and confirmed at the strongest possible level.

A secondary finding replicates across providers. Within Anthropic, Opus 4.7 surfaces Japanese aggregate at 21.1 percent versus Sonnet 4.6 at 18.8 percent — 2.3 points toward the boundary lineage. Within OpenAI, gpt-5.5 surfaces Japanese aggregate at 25.2 percent versus gpt-5.4-mini at 15.0 percent — 10.2 points in the same direction. The pattern is the second cross-category replication of "newer models surface boundary cases more, not less" in the AIAS measurement program (the first being v0.7's within-lab handling-improvement pattern for phantom-brand mentions; González Castro 2026, "Phantom-Brand Presence"). H6 was reported descriptively rather than as a confirmation because the pre-registered direction of effect was not specified.

The remainder of the paper is organized as follows. Section 2 describes the pre-registered method, including registry construction with the v1.0 to v1.2 expansion protocol, prompt structure, model lineup, mode classification with cross-lab AI audit, the auxiliary unknowns-classification step that produced the H7 reframe denominator, and pre-registration. Section 3 reports the five findings in narrative form. Section 4 reports pre-registered hypothesis outcomes in tabular form. Section 5 develops the candidate hypothesis: marketing-language coverage as a brand-level mediator of AI Presence in cross-lingual categories. Section 6 addresses limitations, including the H1 lineage-aggregate failure, the American-comparator collapse that prevented H2 evaluation, and the construct-validity gap between the LLM-tier measurement and downstream consumer behavior. Section 7 outlines Phase 3 work: cross-lingual replication in adjacent categories, construct-validity correlation against external consumer-tracking data, and additional Identity Load tests for hybrid brand cases like Miyabi (a Japanese-branded, German-corporate-parent maker that surfaced at 31.6 percent — closer to German aggregate than Japanese mass-market).

# 2. Method

The measurement followed the AIAS Presence Measurement Protocol v1.1 (González Castro 2026), with the registry-revision protocol (Protocol §2.4) and the hypothesis-reframe convention (Protocol §6.4) exercised end-to-end during the v0.8 measurement.

## 2.1 Designed-for-Test Selection and Brand Registry

The category was selected explicitly as a designed-for-test target for Pattern 4 (discourse-language bias) from v0.6. Premium kitchen knives at the v0.6 single-category baseline could not be measured because no kitchen-knives data was collected in the v0.6 sweep; v0.8 represents the first AIAS measurement of the category. The category satisfies the four structural criteria stated in §1 — Japanese-dominated premium production, English-mediated authority structure, lineage-analogous German and American comparators, and within-Japanese variation in marketing-language infrastructure — that make it the cleanest available test of whether discourse-language bias is a brand-level or a lineage-level phenomenon.

The brand registry was constructed in two canonical versions, with both preserved in the deposit and the H1 hypothesis scored against both for transparency. *Version 1.0 (locked).* Twenty-one brands across three lineages (Japanese, German, American) plus one hybrid (Miyabi, exploratory), constructed prior to data collection on the basis of category-knowledge research and US-targeted retail availability. The registry was committed to a public git repository at commit d3e0989 prior to any data collection. *Version 1.2 (published).* During data extraction, twelve additional Japanese brands surfaced in the unknown-mentions list at non-trivial rates and were added to the registry through the pre-registered registry-revision protocol (AIAS Protocol §2.4). The published registry totals thirty-three brands: nineteen Japanese (standard lineage), one Japanese hybrid (Miyabi, Zwilling-Henckels-owned Japanese line), five German, five American, and three shared (multi-lineage brand families). The canonical scoring of all eight hypotheses was performed against v1.2.

The H1 hypothesis is reported against both v1.0 and v1.2 to expose how lineage-aggregate values move with registry construction. Other hypotheses (H3, H5, H7) are not registry-construction-dependent at the brand level and are reported against v1.2. H8 is reported against both v1.0 (the three-brand boundary cohort locked at pre-registration: Masamoto, Sakai Takayuki, Yoshihiro) and v1.2 (the fourteen-brand boundary cohort after registry revision).

The category boundary excludes folding/tactical knife brands (which leaked into the DISCOVERY prompt; documented in §6) and pure cookware retailers without knife specialization. Güde was added at v1.0 as the German-side boundary-condition case; the American-side cohort (five brands including Cutco, Buck, KA-BAR, Bark River, Lamson) was preserved as a third-lineage comparator.

## 2.2 Prompt Set

Six prompts were anchored to Category Entry Points (CEPs) per AIAS Protocol §3.1: FUNCTIONAL_WHY ("best chef knife for an enthusiast home cook"); CONTEXTUAL_WHEN ("knives to gift a serious cook on a meaningful occasion"); CONSTRAINT_WITH ("Japanese chef knife — what should I know before buying"); IDENTITY_HOW_FEELING ("knives that real chefs use day to day"); DISCOVERY ("emerging or innovative knife brands"); and COMPARISON ("compare leading premium kitchen knife brands"). The CONSTRAINT prompt was anchored to a Japanese-bias frame intentionally as the in-target test of whether the constraint frame elicits Japanese-lineage saturation; the IDENTITY prompt was anchored to a chef-endorsement frame intentionally as the in-target test of whether the identity frame activates the cross-lingual marketing infrastructure most directly. No prompt named any specific brand.

## 2.3 Model Lineup

Six frontier models from four labs spanned the production lineup as of May 2026. Anthropic Claude Sonnet 4.6 and Anthropic Claude Opus 4.7 (within-Anthropic generational comparison). OpenAI gpt-5.4-mini and OpenAI gpt-5.5 (within-OpenAI mini-versus-flagship comparison). Google Gemini 2.5 Flash. xAI Grok 4.1 Fast. The model lineup matches the v0.7 measurement (González Castro 2026, "Phantom-Brand Presence") to enable cross-version comparison of model-pipeline phantom signatures.

## 2.4 Measurement Volume and Failed-Call Recovery

Each prompt by model combination ran eight times at temperature 0.7 where supported, producing a target of 288 measurements. An initial sweep produced 287 of 288 successful measurements; the single failed cell was recovered through the pre-registered failed-call recovery cycle (AIAS Protocol §4.3), yielding 288 successful measurements with full lineup coverage.

## 2.5 Brand Mention Extraction

Brand mentions were extracted using gpt-5.4-mini at temperature 0 with structured-output classification, producing canonical brand mentions per response with rank, sentiment, and primary-recommendation flags. Mentions of brands not in the v1.0 registry were retained on a continuing unknown-mentions list and triaged through the pre-registered registry-revision protocol (Protocol §2.4) into either: (a) registry-eligible brands meeting category and quality criteria, added to the published v1.2 registry; or (b) authority-class entities (publications, retailers, online communities) and out-of-category brands (folding/tactical, pure cookware), retained in the unknowns list for downstream analysis.

## 2.6 Mode Classification and Cross-Lab Audit

Each successful measurement was classified along a five-mode taxonomy: *brand* (response surfaces specific named brand recommendations); *mixed* (response surfaces brand recommendations alongside generic component or retailer guidance); *component* (response is dominated by component-level guidance — steel grades, blade geometry, handle materials — without brand-specific recommendations); *authority* (response cites publications, retailers, or chef endorsements as the source of guidance, with or without specific brand names); *refusal* (response declines to make brand recommendations). The mode classifier was run by gpt-5.4-mini at temperature 0 with structured output. The classification has no operational consequence for H1 through H8 in their pre-registered form (which score against brand-surfacing rate); it provides a diagnostic for H7 (authority-language composition) and a measurement of category-discourse mode distribution.

A cross-lab AI audit was conducted on a stratified twenty-five-row sample drawn across the five modes. The audit was performed blind by a second instance of Claude Opus 4.7 (a different lab from the gpt-5.4-mini classifier). Strict mode agreement (all five categories) was 68 percent; strict brand-surfacing macro agreement (collapsing brand and mixed into "surfaces brand-level recommendations" versus the rest) was 96 percent. All eight strict-mode disagreements clustered on the brand-versus-mixed boundary, paralleling the v0.7 caveated/correction/historical adjacency clustering (González Castro 2026, "Phantom-Brand Presence", §2.6). The disagreement budget does not affect H1 through H8 (which score against the brand-surfacing macro unit at which agreement is 96 percent). The five-mode-versus-macro gap is itself a methodological observation about taxonomy granularity in LLM-output classification.

## 2.7 Authority-Class Classifier

The H7 hypothesis as locked required ≥ 90 percent of authority-mode responses to cite English-language sources. The locked operationalization had a denominator-coverage problem: only two of 288 responses scored as pure authority-mode (per §2.6), insufficient for a 90-percent-of-N test. The hypothesis was reframed per AIAS Protocol §6.4 (hypothesis reframe convention) to score authority-class entity citations across all responses, against the same 90 percent threshold. An auxiliary unknowns classifier was run on every brands_unknown surface mention from the brand-extraction step, classifying each into one of seven types: knife_brand (out-of-registry maker); publication (e.g., Serious Eats, Wirecutter, Cook's Illustrated); retailer (e.g., Sur La Table, Williams-Sonoma, Knifewear); community (e.g., Reddit, BladeHQ); smith (named knifemaker, not a brand); product_term (steel grade, blade type); other. Each entity was tagged with an English-language flag based on the entity's primary discourse language and target audience. The denominator for the H7 reframe is the 262 authority-class mentions (publications + retailers + communities) thus identified.

## 2.8 Pre-Registration

Eight hypotheses with explicit numerical thresholds were locked in PRE_REGISTRATION_knives_v1.0.md at git commit d3e0989, prior to any data collection. The pre-registration document, the registry version that obtained at lock time (v1.0), the locked prompt set, the locked model lineup, and the failed-call recovery procedure were committed to a public git repository before data collection began. Each hypothesis isolated a specific candidate mechanism. Hypotheses, predicted thresholds, and outcomes are reported in Table 1 (§4).

# 3. Results

![Figure A. Brands ordered by AI Presence across the v1.2 registry. Wüsthof leads at 68.4 percent; Güde at 0.0 percent anchors the German-side boundary case. Within the Japanese cohort, the mass-market trio (Shun, Global, Mac) sits in the upper third, while the boundary-condition makers spread across the lower two-thirds — with Masamoto and Takamura clearly detached above the cohort floor.](/Users/pablou/aias_v08_osf_deposit/figures/chart_v08_leaderboard_6col.pdf){ width=100% }

## 3.1 Finding 1 — Lineage isn't the variable. Marketing-language coverage is.

The H1 lineage-aggregate hypothesis was disconfirmed at both registry versions. At v1.0 (locked, 21 brands), Japanese aggregate AI Presence was 36.2 percent and German aggregate was 27.3 percent — an 8.9-point gap in the *opposite* direction of the prediction. At v1.2 (published, 33 brands), after the registry-revision protocol added twelve boundary-condition Japanese brands surfaced from the unknown-mentions list, Japanese aggregate fell to 25.7 percent and German aggregate held at 27.2 percent — a 1.5-point gap *in* the predicted direction but below the 5-point partial-confirmation threshold. By the pre-registered scoring rubric (≥ 15pp = CONFIRMED, 5–15pp = PARTIAL, < 5pp or wrong direction = DISCONFIRMED), both registry versions DISCONFIRM.

![Figure 1. Lineage-aggregate AI Presence at v1.0 (locked) and v1.2 (published) registries. Both registry versions disconfirm H1: at v1.0 Japanese exceeds German in the wrong direction; at v1.2 the gap closes to 1.5 percentage points in the predicted direction but below the partial-confirmation threshold. The 10.5-point shift in Japanese aggregate is driven by adding twelve boundary-condition makers from the unknown-mentions list.](/Users/pablou/aias_v08_osf_deposit/figures/chart_v08_f1_lineage_aggregates_6col.pdf){ width=100% }

The 10.5-percentage-point shift in Japanese aggregate between v1.0 and v1.2 is informative. The shift is entirely accounted for by adding boundary-condition Japanese makers from the unknown-mentions list — most of whom surface at 2 to 10 percent of measurements individually but, in aggregate, pull the lineage mean down by ten points. A symmetric expansion did not apply on the German side because German premium-knife production is itself concentrated in a smaller set of named makers (Wüsthof, Henckels, Güde, Messermeister), all of which were already in the v1.0 registry. The German aggregate is therefore stable across registry versions.

The H1 outcome is consistent with the alternative framing developed in §5: marketing-language coverage is brand-level, not lineage-level. The lineage-aggregate hypothesis fails because aggregating brands of varying marketing-language coverage within a lineage averages out the within-lineage signal that the brand-level mechanism predicts. The brand-level findings in §3.3 are robust to this aggregation problem because they hold the lineage constant and vary on the marketing-language coverage axis directly.

## 3.2 Finding 2 — The discourse infrastructure is exclusively English.

Of 262 named authority mentions across all 288 measurements, 100 percent are English-language. The top fifteen authority sources, in order of mention count, are: Sur La Table (27 mentions); Serious Eats (22); Williams-Sonoma (22); Wirecutter (21); Amazon (21); America's Test Kitchen (13); Japanese Knife Imports (13, a US-based English-language retailer despite the Japanese-language brand name); Knifewear (8); Reddit (7); BladeHQ (7); Cook's Illustrated (6); Burrfection (6, a US-based YouTube channel); KnifeCenter (6); ChefKnivestoGo (5); Blade HQ (5). No Japanese-language authority — neither the named Japanese culinary press, nor any Japanese-language retailer, nor any Japanese-language community — surfaces in any of the 288 responses. No German-language authority surfaces. No French-language authority surfaces. The discourse infrastructure that LLMs draw on for premium kitchen knife recommendations is exclusively English-language.

![Figure 2. Authority-class mention composition across the 288 measurements. 262 of 262 named authorities are English-language — the strongest possible form of the H7 reframe. The right-hand bar chart shows the top fifteen authority sources by mention count.](/Users/pablou/aias_v08_osf_deposit/figures/chart_v08_f2_authorities_6col.pdf){ width=100% }

The H7 hypothesis as locked required ≥ 90 percent of authority-mode responses to be English-language; the locked operationalization had insufficient denominator (two of 288 strict-mode rows). The hypothesis was reframed per Protocol §6.4 to score authority-class entity citations across all responses against the same threshold. The reframe scored at 100 percent — the strongest possible value of the metric. In the AIAS measurement program, this is the strongest replication of the v0.6 Pattern 4 signal in any measurement to date.

The result is consistent with a structural observation about how the LLMs' training corpora were constituted. The premium kitchen knife category is internationally produced but English-mediated: chefs cited in English-language food media (Redzepi, Adrià, Ramsay, Chang, Brock, Stewart, Bourdain), retail aggregators that index English-language reviews (Sur La Table, Williams-Sonoma, Amazon), and English-language YouTube channels and forums (Burrfection, Reddit r/chefknives, BladeHQ) collectively dominate the indexable discourse. Japanese-language category coverage exists in volume in Japanese culinary press, retailer catalogs, and community forums, but does not appear to enter the LLMs' English-language brand-recommendation surface at any detectable rate.

## 3.3 Finding 3 — Within every lineage, English-marketed brands surface; non-English-marketed brands don't.

Three within-lineage tests on the same dataset converge on the same brand-level mechanism. The convergence is stronger evidence for the marketing-language-coverage framing than any single test in isolation, because the three tests vary on lineage (Japanese, German, boundary-Japanese subset) while holding the brand-level mechanism constant.

![Figure 3. Within-lineage convergence on the marketing-language-coverage mechanism. Top: within-Japanese mass-market versus boundary cohort at v1.2 — 55.2 percent versus 6.8 percent, an approximately 8x ratio. Masamoto and Takamura stand markedly apart at the upper end of the boundary cohort; both have substantially developed US-targeted English-language infrastructure. Bottom: within-German English-marketed (Wüsthof 68.4 percent, Henckels 55.6 percent) versus boundary (Güde 0.0 percent across all 288 measurements).](/Users/pablou/aias_v08_osf_deposit/figures/chart_v08_f3_within_lineage_6col.pdf){ width=100% }

*Within Japanese: approximately 8x ratio.* Mass-market English-marketed Japanese brands (Shun, Global, Mac, all with substantial US distribution and English-language coverage in food media) surface at 55.2 percent mean. The fourteen boundary-condition Japanese makers in the canonical v1.2 cohort (Kikuichi, Konosuke, Korin, Masamoto, Mazaki, Nenox, Nigara Hamono, Sakai Takayuki, Takamura, Takeda, Togiharu, Yoshihiro, Yoshikane, Yu Kurosaki) surface at 6.8 percent aggregate — a 48.4-percentage-point gap. The locked-registry version (with three boundary brands: Masamoto, Sakai Takayuki, Yoshihiro) showed a 44.3-percentage-point gap and approximately 5x ratio; the expanded cohort sharpens the ratio to approximately 8x because the additional boundary brands surface predominantly in the 2–10 percent range, lowering the cohort mean. H3 confirms at the strongest level.

*Within German: zero versus 62 percent.* English-marketed German makers (Wüsthof at 68.4 percent, Henckels at 55.6 percent) surface at 62.0 percent mean. Güde — a 240-year-old Solingen maker with substantial European reputation but negligible US-targeted English-language presence — surfaces in zero of 288 measurements: across every model, every prompt, and every run. H5 confirms at the strongest possible form (the same form as v0.7's Pier 1 result for the phantom hypothesis: zero across n = 288).

*Within boundary-condition Japanese: the marketing-language-coverage signal is monotonic.* Of the fourteen boundary-condition Japanese brands, seven clear the 5-percent floor and seven do not. The seven that clear the floor — Masamoto (18.1 percent), Takamura (16.7 percent), Sakai Takayuki (10.8), Konosuke (9.7), Korin (8.3), Nigara Hamono (5.9), Yu Kurosaki (5.2) — share the property of having substantively developed US-targeted English-language presence: US-distributed retail, chef endorsements in English-language food media, English-language community forum activity, or named-by-American-knife-retailer indexing. The seven that do not clear the floor — Yoshihiro (3.8), Takeda (3.5), Yoshikane (3.5), Mazaki (2.8), Kikuichi (2.4), Nenox (2.4), Togiharu (2.1) — are characterized by predominantly Japanese-language marketing or by US-distribution without chef-endorsed media coverage. The two clearly-detached outliers above 15 percent (Masamoto, Takamura) are the boundary-condition Japanese brands with the most substantially developed US-targeted infrastructure: Masamoto operates masamoto.us as a direct US-consumer channel, Takamura has been endorsed by Redzepi, Adrià, Ramsay, Chang, Brock, and Stewart in English-language food media. H8 confirms partially: the cohort aggregate of 6.8 percent sits in the 5–15 percent partial-confirmation band; the per-brand distribution monotonically follows English-language marketing-coverage gradients.

The three tests converge on a common mechanism: within any single lineage, brands' AI Presence ranks with their English-language marketing-coverage gradient. The convergence holds across Japanese mass-market versus traditional, across German English-marketed versus boundary, and across the within-boundary-Japanese ordering. The mechanism operates at brand level. Lineage-level claims about AI bias do not capture it.

## 3.4 Finding 4 — The variance is in German. Japanese is the steady lineage.

Per-CEP analysis for H4 reveals that the variance in lineage-aggregate AI Presence by prompt frame lives in the German lineage, not the Japanese. Japanese aggregate is steady across the six prompts at 21.3 percent in the constraint frame (anchored to a Japanese-bias frame, where the prediction was Japanese saturation) versus 22.8 percent baseline mean across the other five prompts — a ratio of 0.93. The H4 hypothesis as pre-registered predicted that the constraint frame would elicit Japanese saturation; the result instead shows Japanese as the *steady* lineage.

![Figure 4. Per-CEP brand-surfacing rate by lineage. Japanese aggregate is steady across all six prompt frames; German aggregate collapses to 2.1 percent in the CONSTRAINT frame (Japanese-bias anchor) and peaks at 45.8 percent in the IDENTITY frame (chef-endorsement anchor). The variance is in German, not Japanese.](/Users/pablou/aias_v08_osf_deposit/figures/chart_v08_f4_per_cep_6col.pdf){ width=100% }

The variance is German. German aggregate collapses to 2.1 percent in the constraint frame (the frame anchored to "Japanese chef knife — what should I know") and peaks at 45.8 percent in the identity frame ("knives that real chefs use day to day"). The asymmetric variance in German is structurally interpretable: when the prompt activates the Japanese-bias frame, the model stops recommending German knives (presumably because the model recognizes the constraint as out-of-frame for German production); when the prompt activates the chef-endorsement identity frame, the model surfaces German knives because the chef-endorsement infrastructure for German makers (Wüsthof's Bourdain endorsement; Henckels' chef-line) is concentrated in the same English-language food media that dominates the authority structure (§3.2).

The structural finding parallels v0.7's per-CEP cognitive-geometry observation (González Castro 2026, "Phantom-Brand Presence", §3.4): prompt frame activates different temporal and lineage cognitive slots within the same model. The same brand can simultaneously occupy a recommended-as-current slot in one prompt frame and a recommended-as-historical slot in another. In v0.8, the same lineage can simultaneously occupy a saturated slot in one prompt frame and a near-zero slot in another, even when the lineage's mean aggregate is mid-range.

## 3.5 Finding 5 — Newer models surface boundary lineages more, not less.

Within-lab generational comparisons replicate v0.7's "newer models phantom-mention with different valence handling, not at lower frequencies" observation, on the discourse-language axis rather than the phantom axis. Within Anthropic, Claude Opus 4.7 surfaces Japanese aggregate at 21.1 percent versus Claude Sonnet 4.6 at 18.8 percent — 2.3 points toward the boundary lineage. Within OpenAI, gpt-5.5 surfaces Japanese aggregate at 25.2 percent versus gpt-5.4-mini at 15.0 percent — 10.2 points in the same direction.

![Figure 5. Within-lab generational comparison. Newer-generation models within both Anthropic and OpenAI surface Japanese aggregate at higher rates than their older counterparts. The cross-category replication of v0.7's within-lab handling-improvement pattern strengthens the claim that newer models surface boundary cases more, not less.](/Users/pablou/aias_v08_osf_deposit/figures/chart_v08_f5_freshness_4col.pdf){ width=70% }

The pattern is the second cross-category replication of "newer models surface boundary cases more, not less" in the AIAS measurement program. In v0.7, the pattern appeared as within-lab handling improvement: newer models phantom-mention with more responsible per-mention valence distribution rather than at lower frequencies. In v0.8, the pattern appears as boundary-lineage surfacing: newer models surface non-English-marketed and boundary-condition brands at higher rates, even as the mean aggregate Presence varies across models for unrelated reasons. The cross-category nature of the replication strengthens the claim that the pattern is a structural property of model generation rather than an artefact of either category.

The candidate mechanism — newer models have larger and more diverse training corpora that include longer-tail boundary-condition discourse — is consistent with both the v0.7 handling-improvement observation and the v0.8 boundary-surfacing observation. H6 was reported descriptively (the pre-registration did not specify a direction of effect) but the cross-category replication promotes the descriptive observation toward a candidate hypothesis worth committing to in a future pre-registration.

# 4. Pre-Registration Outcomes

Eight hypotheses with explicit numerical thresholds were locked in PRE_REGISTRATION_knives_v1.0.md at git commit d3e0989, prior to any data collection. Two were confirmed at the strongest level. Two were partially confirmed. Two were disconfirmed at the headline level but reframed productively (one via Protocol §6.4 reframe convention to a confirmed mechanism statement; one via reframe of the variance structure). One could not be evaluated due to comparator collapse. One was reported descriptively. Predictions and outcomes are reported in Table 1.

**Table 1.** Pre-registered hypotheses, predictions, and outcomes.

| H | Pre-registered prediction | Result | Status |
|---|---|---|---|
| H1 | JP aggregate < DE aggregate by ≥ 10pp | v1.0: jp 36.2% > de 27.3% (gap −8.9pp); v1.2: jp 25.7% < de 27.2% (gap +1.5pp, below 5pp partial threshold) | Disconfirmed at both registry versions |
| H2 | American aggregate < German aggregate by ≥ 15pp | American aggregate 0.6% (comparator effectively collapsed); cross-lineage comparison non-evaluable | Cannot evaluate |
| H3 | Within-Japanese mass-market > traditional by ≥ 30pp | mass-market 55.2% vs traditional 6.8% (v1.2: 48.4pp gap, approximately 8x ratio); v1.0 boundary set: 44.3pp gap | Confirmed strongly |
| H4 | Constraint prompt elicits Japanese-aggregate saturation ≥ 40% | Japanese constraint 21.3% vs baseline 22.8% (ratio 0.93); variance is in German (constraint 2.1%, identity 45.8%) | Disconfirmed at headline; reframe finding (German variance, Japanese steady) |
| H5 | Within-German English-marketed > boundary by ≥ 30pp; Güde < 1/3 of (Wüsthof+Henckels mean) | English-marketed German 62.0% vs Güde 0.0% across 288 measurements; ratio = 0.0 | Confirmed at strongest possible form |
| H6 | Within-lab newer-versus-older variance | Within Anthropic: Opus 4.7 21.1% > Sonnet 4.6 18.8% (+2.3pp); within OpenAI: gpt-5.5 25.2% > gpt-5.4-mini 15.0% (+10.2pp); both toward boundary | Descriptive (direction of effect not pre-registered); cross-category replication of v0.7 |
| H7 | ≥ 90% of authority-mode responses are English-language | Reframed per Protocol §6.4: 262 of 262 authority mentions across all responses are English-language (100%) | Confirmed reframed at strongest possible form |
| H8 | Boundary-condition Japanese cohort aggregates < 5% | v1.0 (3 brands): 10.9% (5–15% partial band); v1.2 (14 brands): 6.8% (5–15% partial band) | Partially confirmed (both registry versions) |

Each hypothesis isolated a specific candidate mechanism. H1 tested the lineage-aggregate prediction directly. H2 was intended as a structural-comparator test (American makers as the lineage with negligible chef-reputation infrastructure but full English-language coverage); the comparator collapsed at 0.6 percent aggregate, indicating that AI does not recognize "American kitchen knives" as a meaningful category, regardless of brand. H3 tested the within-Japanese mass-market-versus-traditional gap. H4 tested per-prompt variance with the constraint frame as the predicted Japanese-saturation prompt. H5 tested the within-German boundary case. H6 tested cross-lab generational variance. H7 tested authority-language composition (locked threshold; reframed denominator per Protocol §6.4). H8 tested the boundary-condition cohort floor effect.

# 5. Discussion: Marketing-Language Coverage as a Brand-Level Mediator

The v0.6 Pattern 4 observation was framed as a lineage-level phenomenon: AI Presence in cross-lingual categories appeared to track the discourse-language profile of the lineage. The framing predicted that the variable available for analysis is lineage-level discourse aggregate — that lineages whose category discourse exists primarily in non-English languages would surface at lower rates than lineages whose category discourse is English-mediated.

The v0.8 result is inconsistent with that framing at the mechanism level. The H1 lineage-aggregate test was disconfirmed at both registry versions: at v1.0 with the locked 21-brand registry, at v1.2 with the expanded 33-brand registry. The Japanese aggregate moved by 10.5 percentage points between versions (36.2 percent to 25.7 percent) but never crossed below the German aggregate by more than 1.5 percentage points, well short of the 5-point partial-confirmation threshold. The lineage-aggregate hypothesis fails consistently regardless of registry construction.

The brand-level findings, in contrast, are robust and consistent. Within Japanese, the approximately 8x ratio between mass-market and the boundary-condition cohort holds at v1.2 (and at the v1.0 boundary set, at 5x). Within German, the Güde-versus-mass-market 62-point gap is independent of any registry choice. Within the boundary-condition Japanese cohort, the per-brand surface-rate distribution monotonically tracks the brands' US-targeted English-language marketing infrastructure. None of these brand-level findings depend on registry construction.

A candidate alternative framing — *marketing-language coverage as a brand-level mediator* — is proposed. On this account, the binding variable for AI Presence in cross-lingual categories is brand-level English-marketing coverage, not lineage-level discourse aggregate. Brands with substantial English-language marketing infrastructure surface in LLM recommendations at materially higher rates than equivalently positioned brands without such infrastructure, *within* every lineage of origin. The framing is consistent with three observations from this measurement that the lineage-aggregate framing does not predict.

(a) *Within-lineage convergence on the same mechanism (§3.3).* Three independent tests on the same dataset — within-Japanese mass-market versus traditional, within-German English-marketed versus boundary, within-boundary-Japanese marketing-coverage gradient — all show the same brand-level pattern. The lineage-aggregate framing has no mechanism for this convergence; the brand-level mediator framing predicts it directly.

(b) *Authority infrastructure exclusively English (§3.2).* The 262-authority composition is 100-percent English-language. The lineage-aggregate framing has no mechanism for why authority composition would be uniform across all six pre-registered prompts; the brand-level mediator framing predicts that the discourse infrastructure that LLMs draw on for cross-lingual categories is the discourse infrastructure that names and ranks brands in the LLMs' training language, regardless of brand origin.

(c) *Newer-models cross-category replication (§3.5).* The within-lab generational pattern toward boundary-condition surfacing replicates the v0.7 within-lab handling-improvement pattern on a different axis. The lineage-aggregate framing has no clear mechanism for this replication; the brand-level mediator framing — combined with a candidate hypothesis that newer models have more diverse training corpora that include more longer-tail boundary-condition discourse — predicts both observations.

The framing is offered as a candidate hypothesis adjacent to but structurally distinct from existing AI-Surfacing hypotheses. It is distinct from *Default Reinforcement* (which addresses why the strongest-presence brand in a category becomes the modal recommendation) in that it addresses why some brands acquire the discourse mass to enter the recommendation surface in the first place. It is distinct from *recommendation-slot persistence* (the v0.7 candidate hypothesis; González Castro 2026, "Phantom-Brand Presence") in that it addresses cross-lingual entry rather than within-language persistence beyond entity changes. It is distinct from *freshness-lag* in that it predicts a structural rather than temporal asymmetry: the gap between English-marketed and non-English-marketed brands in cross-lingual categories will persist across model generations, even as both categories' mean aggregates shift with training-data evolution.

The framing predicts three falsifiable consequences. *Prediction 1.* In any cross-lingual product category, within-lineage variance on AI Presence will be driven primarily by brand-level English-marketing coverage rather than by brand-level production quality, age, or category prestige. *Prediction 2.* Boundary-condition brands that develop US-targeted English-language infrastructure (chef endorsements in English-language food media, English-language retailer indexing, English-language community presence) will see AI Presence rise within a measurable lag period, even without changes in production. *Prediction 3.* Lineage-level aggregate tests in cross-lingual categories will systematically fail or produce unstable results, while within-lineage brand-level mechanism tests will produce consistent results across registry constructions.

Construct validity remains open. The marketing-language-coverage framing is a property of LLM mediation, not directly of consumer behavior. Whether consumers in cross-lingual categories actually act on AI recommendations of English-marketed brands at higher rates than non-English-marketed brands — and at what rates such recommendations affect consideration, purchase intent, or category share in the consumer-facing market — is the separate question the AIAS Phase 3 construct-validity program will address. Both possible outcomes are publishable: a strong correlation establishes AI Presence as a leading indicator of consumer behavior in cross-lingual categories; a weak correlation establishes the index as a measurement of LLM behavior with implications limited to channel optimization for AI-mediated visibility. Neither is established here.

# 6. Limitations

Six caveats apply to the findings reported here.

*Single designed-for-test category.* Phase 2 v0.8 measures one designed-for-test cross-lingual category (premium kitchen knives). Together with the v0.6 single-category observations in olive oil and skincare, the program now has one-category-confirmed-plus-two-preliminary for Pattern 4. The mechanism is not yet generalizable to all cross-lingual categories. Phase 3 will test additional cross-lingual categories (premium tea and traditional spirits identified as candidates) before the marketing-language-coverage framing can be claimed as a general property of cross-lingual category visibility in LLMs.

*H1 lineage-aggregate failure interpretation.* The H1 hypothesis was disconfirmed at both registry versions. Two readings are available. *Reading A:* the lineage-aggregate hypothesis as written is wrong; the underlying mechanism is brand-level (the §5 reframe). *Reading B:* the registry construction did not include enough boundary-condition brands at v1.2 to fully expose a lineage-aggregate signal that exists at the population level. Reading A is supported by the within-lineage convergence in §3.3, which constitutes positive evidence for the brand-level mechanism rather than merely the absence of evidence for the lineage-aggregate mechanism. Reading B cannot be ruled out without measurement against a registry constructed with full population coverage of all four lineages, which is not feasible in this designed-for-test framework. The paper takes Reading A as the more parsimonious interpretation but flags Reading B as a residual uncertainty.

*American comparator collapsed.* The H2 hypothesis required a meaningful American-aggregate signal as a structural comparator for the lineage-aggregate test. The American aggregate was 0.6 percent across all 288 measurements: AI does not recognize "American kitchen knives" as a meaningful category, regardless of brand. The H2 robustness check that the pre-registration framework anticipated was therefore unavailable. The comparator collapse is itself a finding — about category-discourse history shaping AI Presence — but it forecloses one specific test the pre-registration design was meant to enable.

*Mode-classification disagreement budget.* The cross-lab AI audit produced 96 percent strict agreement on the brand-surfacing macro unit (which H1 through H8 score against) and 68 percent strict agreement on the underlying five-mode taxonomy. The mode-versus-macro gap is methodologically interesting and parallels v0.7's caveated/correction/historical adjacency clustering. The disagreement budget does not affect the headline H1–H8 outcomes (which score against the macro unit) but introduces a small uncertainty on the H7 reframe denominator at the strict-mode level. The reframe is reported using the cross-all-responses denominator (262 authority mentions) rather than the strict-mode denominator, mitigating but not eliminating the dependence.

*Out-of-category leakage in DISCOVERY prompt.* The DISCOVERY prompt ("emerging or innovative knife brands") drifted into folding/tactical knife brands (Tactile Knife, Vosteed, Civivi, etc.) rather than premium kitchen-knife brands. The leakage indicates an out-of-category cognitive slot in AI's "emerging knife brands" frame: the model interprets "emerging" + "knife brand" as the folding-knife / tactical category rather than as the premium-kitchen category. The leakage is documented and the DISCOVERY-prompt rows are flagged in the deposited dataset; the H1 through H8 analyses use the brand-extraction step's registry-membership filter to exclude out-of-category mentions from per-brand aggregates.

*Construct validity unproven.* AI Presence measures a real and stable property of the LLM tier, but whether that property correlates with consumer consideration, purchase intent, or sales in cross-lingual categories is unknown. The marketing-language-coverage framing is a property of LLM mediation, not of consumer behavior; whether consumers in cross-lingual categories actually act on AI recommendations of English-marketed brands is the separate question the AIAS Phase 3 construct-validity program will address.

# 7. Future Research

The Phase 3 program will address four priorities surfaced by the v0.8 findings.

*Cross-lingual replication.* Premium tea and traditional spirits are identified as candidate categories for the next designed-for-test measurement. Both satisfy the four cross-lingual structural criteria stated in §1: dominant non-English-language production heritage, English-mediated authority structure, lineage-analogous comparators, and within-non-English-lineage variation in marketing-language infrastructure. Either category, measured against the same eight-hypothesis framework with category-appropriate prompt anchoring, would extend the program from one designed-for-test confirmation to two — the threshold the program has set for promoting a candidate hypothesis from "exploratory" to "supported."

*Construct-validity correlation.* For premium kitchen knives specifically, candidate validators include Google Trends (English-language search-volume comparison between mass-market and traditional Japanese makers), Wirecutter and Serious Eats reader-survey data, and DTC brand-tracking instruments where available. The marketing-language-coverage framing predicts that consumer awareness of Masamoto and Takamura within US/UK consumers will be detectably higher than for Sakai Takayuki and Yoshihiro, even after controlling for production volume — and that the gap will be similar in magnitude to the AI Presence gap. If the prediction holds, AI Presence is a leading indicator of consumer-side cross-lingual brand visibility. If it does not, AI Presence is a property of LLM mediation with limited consumer-behavior implication.

*Identity Load tests for hybrid brand cases.* The Miyabi observation in v0.8 (Japanese-branded, German-corporate-parent maker; surfaces at 31.6 percent — closer to German aggregate than Japanese mass-market) suggests that German-parent English-marketing infrastructure can elevate a Japanese-origin brand to German-aggregate-equivalent visibility, but not to mass-market-Japanese leadership. The observation cross-cites to the Identity Load moderator developed in González Castro (2026), "AI Availability" (Section 4.1a), which predicts that brand-Identity-Load attenuates AI Presence even with strong corporate-parent marketing infrastructure. A measurement designed to isolate Identity Load — with a registry of hybrid brands of varying Identity Load — would test whether Miyabi's intermediate position generalizes.

*Within-lab handling at the recommendation-slot level.* The v0.7 within-lab handling-improvement pattern and the v0.8 within-lab boundary-surfacing pattern suggest that LLM handling of cross-lingual and disrupted brands varies by model generation in structurally similar ways. A measurement isolating model-size-versus-training-cutoff (running the same brand registry against same-cutoff models of different sizes within a single lab) would clarify whether the cross-version pattern is driven by training-data diversity, by reasoning-mode capability, or by instruction-tuning evolution.

# References {-}

Bender, E. M., Gebru, T., McMillan-Major, A., & Shmitchell, S. (2021). On the dangers of stochastic parrots: Can language models be too big? *Proceedings of the 2021 ACM Conference on Fairness, Accountability, and Transparency*, 610–623.

Brown, T. B., Mann, B., Ryder, N., et al. (2020). Language models are few-shot learners. *Advances in Neural Information Processing Systems*, 33.

González Castro, P. U. (2026). AI Availability: Extending Mental and Physical Availability into Algorithmic Retrieval. *SSRN Working Paper*. https://ssrn.com/abstract=6659000

González Castro, P. U. (2026). AI Presence Measurement Across Consumer Categories: A Cross-Category Baseline of Brand Visibility in Large Language Model Outputs. *SSRN Working Paper*. https://ssrn.com/abstract=6720959

González Castro, P. U. (2026). A Designed-for-Test Measurement of Phantom-Brand Presence in Large Language Model Outputs: Pre-Registered Evidence from Bed Bath & Beyond, with Pier 1 as Structural Comparator. *SSRN Working Paper*. https://ssrn.com/abstract=6721779

González Castro, P. U. (2026). AIAS Presence Measurement Protocol v1.1. *SSRN Working Paper*. https://ssrn.com/abstract=6722319

Keller, K. L. (2013). *Strategic Brand Management: Building, Measuring, and Managing Brand Equity* (4th ed.). Pearson.

Nosek, B. A., Ebersole, C. R., DeHaven, A. C., & Mellor, D. T. (2018). The preregistration revolution. *Proceedings of the National Academy of Sciences*, 115(11), 2600–2606.

Romaniuk, J. (2023). *Better Brand Health: Measures and Metrics for a How Brands Grow World*. Oxford University Press.

Romaniuk, J., & Sharp, B. (2016). *How Brands Grow: Part 2 — Including Emerging Markets, Services, Durables, New and Luxury Brands*. Oxford University Press.

Sharp, B. (2010). *How Brands Grow: What Marketers Don't Know*. Oxford University Press.

# Declarations {-}

## Conflict of Interest {-}

The author serves as Director, Corporate Brand Creative and Governance at Samsung Electronics America. The research presented here is independent of Samsung Electronics America and does not constitute Samsung research. No Samsung Electronics America data, personnel, or commercial interests influenced the design, conduct, analysis, or reporting of this study. Samsung Electronics America did not review the manuscript prior to posting. The brand population evaluated in this study (premium kitchen knives) does not include Samsung product lines.

## Funding {-}

Self-funded. No external funding sources contributed to this research.

## Data Availability {-}

Underlying datasets, the locked pre-registration document (PRE_REGISTRATION_knives_v1.0.md, locked at git commit d3e0989, lock date 6 May 2026 prior to data collection), both registry versions (v1.0 locked, v1.2 published), the canonical scoring tables, the auxiliary unknowns classification, the cross-lab AI audit sample, and the build-pipeline source code are deposited in an Open Science Framework project at https://osf.io/ec6wh/. The deposit contains row-level CSV outputs throughout — the v0.8 measurement was conducted within a git-tracked repository from pre-registration through publication, and no provenance gaps obtain. The OSF MANIFEST.md documents the file inventory, the lineage between raw measurements and derived analyses, and the cryptographic git-commit anchors for the locked pre-registration and the locked registry versions.

# Author Information {-}

Pablo Ulpiano González Castro is faculty in the MPS Branding Program at the School of Visual Arts, New York, where he teaches Brand Transformation through Human-Centered Methodologies. He maintains Third System™ (research entity; data archive and methodology venue) as the publication venue for the AIAS measurement program. Correspondence: pablou@pablou.com · pablou.com.
