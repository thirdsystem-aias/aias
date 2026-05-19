---
title: "The AIAS™ Presence Measurement Protocol: Phase A Pivot-Validation Specification (v1.3)"
author: |
  Pablo Ulpiano González Castro \\
  \small SVA, MPS Branding Program, New York, NY \\
  \small (primary academic affiliation) \\
  \small Third System™ (research entity; data archive and methodology venue) \\
  \vspace{0.3cm}
  \small Correspondence: pablou@pablou.com · pablou.com \\
  \small ORCID: 0009-0003-8968-9990
date: \today
mainfont: Carlito
fontsize: 11pt
geometry: margin=1in
colorlinks: true
linkcolor: blue
urlcolor: blue
header-includes:
  - \usepackage{setspace}
  - \setstretch{1.36}
  - \setlength{\parskip}{8pt}
  - \setlength{\parindent}{0pt}
  - \setcounter{secnumdepth}{-1}
  - \usepackage{float}
  - \floatplacement{figure}{H}
  - \usepackage{caption}
  - \captionsetup{labelfont={bf,it}, textfont=it, justification=raggedright, singlelinecheck=false}
  - \usepackage{titlesec}
  - \titleformat{\section}{\bfseries\large}{}{0pt}{}
  - \titleformat{\subsection}{\bfseries\normalsize}{}{0pt}{}
  - \titleformat{\subsubsection}{\bfseries\small}{}{0pt}{}
  - \usepackage{amsmath}
  - \usepackage{amssymb}
  - \makeatletter
  - \renewcommand{\maketitle}{\begin{titlepage}\centering\vspace*{2cm}{\fontsize{16}{21.76}\selectfont\bfseries\setlength{\parskip}{10.36pt}\@title\par}\vspace{1.5cm}\@author\par\vfill\@date\end{titlepage}}
  - \makeatother
---

**Keywords:** methodology; Phase A; pivot validation; Google Trends; Knowledge Graph entity suggestions; bounded override; pre-registration; AIAS Presence Measurement Protocol

**JEL codes:** M31 (primary); L86, L15, D83, M37

\newpage

## Abstract

The AIAS Presence Measurement Protocol (v1.2; SSRN 6761698) specified Phase A pivot validation as the step that establishes a brand's substrate-category fit before Phase B topic-ID resolution proceeds, but documented the validation at the level of intent only — the specific stages, thresholds, and contingency-handling rules used in operational practice were not centrally specified. v0.16 (kitchen knives; SSRN 6791999) surfaced the gap operationally: the pre-registered pivot Victorinox failed Phase A on canonical-query Trends eligibility, and the activated alternate Wüsthof failed all three numeric stages of the same protocol, yet was activated as the operational pivot under pre-reg §6 contingency through manual operator intervention. This methodological note specifies the Phase A pivot-validation procedure centrally. §6.4 formalizes the five-stage protocol used in practice: Stage 1 (Knowledge Graph entity-suggestion audit for the pivot brand), Stage 2 (baseline Trends stability check), Stage 3 (bundle position check against in-category reference brands), Stage 4 (adjacency check against the pre-registered substrate-vs-adjacent keyword pair), Stage 5 (verdict aggregation under stage-conjunction thresholds on Stages 2–4). The fallback activation rule ($R_F$) implements bounded override: when both the primary pivot and the activated alternate fail Stage 5, the operator may invoke a one-time bounded override per cell per phase with mandatory DEVIATIONS log entry. The v0.16 Victorinox/Wüsthof case is retrospectively scored against the v1.3 specification in §6.4.8. v1.3 is a v1.2 successor increment; §6.4 is added, all other Protocol v1.2 sections remain byte-identical.

\newpage

## §1 Motivation

### §1.1 The AIAS Presence Measurement Protocol and the Phase A pivot-validation step

The AIAS Presence Measurement Protocol (Protocol v1.2; SSRN 6761698) specifies a four-phase pipeline for measuring the AI Availability Score's Presence component across single-substrate brand panels: Phase A (pivot validation), Phase B (topic-ID resolution), Phase C (LLM acquisition), and Phase D (enrichment and scoring). The pipeline's cross-phase integrity rests on each phase's output being well-formed for the next phase's input. Phase A's output is a validated pivot brand for each tradition cell in the panel — a brand whose substrate-category fit has been verified before Phase B topic-ID resolution proceeds. Phase B reads the validated pivots and resolves them to Google Trends topic-IDs; Phase C uses the resolved topic-IDs to construct LLM query prompts against the reference model set; Phase D computes the Presence Index against the LLM responses, with Trends data entering as the bivariate correlate.

Phase A pivot validation matters because brand names are not category-typed in natural language and are not category-typed in the Trends search distribution either. Victorinox refers to Swiss Army knives, multi-tool products, kitchenware, watches, and luggage in both natural language and Trends co-occurrence patterns. Le Creuset refers to cookware, kettles, bakeware, and small accessories. Tom Ford refers to fragrance, beauty, and apparel. A pivot anchor that fails to fix the substrate category produces a Phase B topic-ID resolution that may resolve to the wrong category's Trends entity, and a Phase C LLM acquisition that measures the wrong category's AI Presence — a structural validity failure invisible to the downstream pipeline because all numeric values resolve cleanly.

### §1.2 The gap surfaced at v0.16

Protocol v1.2 §6.1 specified the goal of Phase A pivot validation: the canonical pivot should establish the brand's substrate-category fit before Phase B proceeds. It did not specify the operational procedure by which fit is established, the thresholds against which fit is judged, or the contingency rules when a candidate pivot fails. In practice, the AIAS programme had implemented Phase A as a five-stage procedure from v0.11 onward — Knowledge Graph entity-suggestion audit, Trends baseline stability, bundled position against reference brands, adjacency-keyword discrimination, and verdict aggregation — but the procedure was documented only in the operational `phase_a/` scripts and in per-phase pre-registration §6 contingency text. Through v0.15, this absence did not bind: the substrates measured under v1.2 (premium tea, skincare, finance, project-management software) were single-category-saturated at brand level, and the operational pivots passed Phase A unanimously without operator intervention. The methodology paper did not need to document Phase A's operational structure because the structure was never exercised in a problematic way.

v0.16 (kitchen knives; SSRN 6791999) exercised it. The pre-registered pivot Victorinox failed Phase A on canonical-query Trends eligibility — Victorinox's bare canonical query returned kitchen-knife brand presence below the Trends-eligibility floor (per the v0.16 paper §4.3). Per pre-reg §6, Wüsthof was activated as fallback pivot and underwent its own Phase A run. Wüsthof's Phase A returned numerical failure on all three quantitative stages: Stage 2 baseline stability CV at 42.19% against the 30.0% threshold; Stage 3 bundle position ratio at 0.0 against the [0.5, 5.0] band; Stage 4 adjacency `chef_proportion` at 0.004 against the 0.2 substrate minimum, with `swiss_army_proportion` at 0.996 against the 0.7 adjacent maximum. Wüsthof's Stage 5 verdict was FAIL.

The operator activated Wüsthof as the operational pivot anyway, under pre-reg §6 contingency, with manual intervention noted in the verdict's `next_steps` field and the operational handling documented in DEVIATIONS Entry 3. The German tradition cell scored at n = 4 (Wüsthof exited within-cell scoring as pivot brands always do, regardless of the alternate-also-fails state).

The substantive call was correct — the panel had to proceed, and the alternate-pool for the german cell had been exhausted at the first alternate. The operational record was logged as a deviation because Protocol v1.2 did not specify three things that v1.3 now specifies centrally: the canonical operational structure of Phase A (the five stages and their data contracts); the thresholds against which each stage passes or fails; the contingency rule when an activated alternate also numerically fails the same stages. A future operator facing a similar case under v1.2 has the protocol's intent but not its operational specification.

### §1.3 Contribution of v1.3

This methodological note specifies Phase A pivot validation centrally. §6.4 introduces six components added to Protocol v1.2 §6:

- **§6.4.2** specifies Stage 1 (Knowledge Graph entity-suggestion audit) — the diagnostic pytrends/SerpAPI query that documents the pivot brand's Knowledge Graph entity context at validation time.
- **§6.4.3** specifies Stage 2 (baseline Trends stability) — the SerpAPI-based check that the pivot brand returns a stable Trends signal over the acquisition window.
- **§6.4.4** specifies Stage 3 (bundle position) — the bundled-Trends check that the pivot brand sits in the right competitive tier within its tradition cell.
- **§6.4.5** specifies Stage 4 (adjacency) — the discriminative check that the pivot brand's Trends signal anchors on the pre-registered substrate keyword, not on the pre-registered adjacent-category keyword.
- **§6.4.6** specifies Stage 5 (verdict aggregation) — the stage-conjunction rule that converts the per-stage pass/fail results on Stages 2–4 into a Phase A pass/fail verdict, with canonical threshold values locked at v1.3.
- **§6.4.7** specifies the fallback activation rule ($R_F$) — the ordinal-sequence activation of registry alternates when Stage 5 returns FAIL, the bounded-override rule when an activated alternate also fails Stage 5, the cell-collapse handling when alternates exhaust without override, and the audit-log requirements for each fallback event.

§6.4.8 retrospectively scores the v0.16 Victorinox/Wüsthof case against §6.4.2 through §6.4.7 to demonstrate consistency between the v1.2 operator action and the v1.3 specification.

The contribution is dual: descriptive of existing practice for §6.4.2–§6.4.6 (the five stages and their thresholds have been version-locked in operational scripts since v0.11 but were not formalized in the methodology paper), and prescriptive for §6.4.7 (the bounded-override rule resolves an operational gap that v0.16 surfaced and v1.2 did not address). The Phase A $\rightarrow$ Phase B $\rightarrow$ Phase C $\rightarrow$ Phase D pipeline is unchanged; the four-regime taxonomy of Protocol v1.2 §6 is unchanged; the scoring rules of Protocol v1.2 §7 are unchanged. v1.3 specifies an operational layer that v1.2 documented at the level of intent.

## §2 Positioning as v1.2 successor

### §2.1 Versioning convention

The AIAS Presence Measurement Protocol uses minor-version increments for additions that specify operational procedure within stages already named at the level of intent in the prior major version, without changing the protocol's phase structure or measurement composition. Major-version increments (v1.x $\rightarrow$ v2.0) are reserved for changes that alter what is being measured or how the phases compose; minor-version increments (v1.2 $\rightarrow$ v1.3) lock operational specifications at stages previously specified only at the level of intent. v1.3 is a minor-version increment under this convention.

The full Protocol document — Protocol v1.3 — is the v1.2 document with §6.4 added and the version stamp updated. Sections §1 through §6.3 are byte-identical to v1.2. §7 (scoring), §8 (figures and reporting), and §9 (limitations and falsifiability) are byte-identical to v1.2. No section other than §6.4 is added, modified, or deleted.

### §2.2 Relationship to SSRN 6761698

SSRN 6761698 (*The AIAS Presence Measurement Protocol: Methodological Notes on Construct Validity and the Four-Regime Taxonomy*) is the canonical v1.2 specification. This note (v1.3) is its successor in the methodological-paper sequence. The canonical citation for AIAS Presence Measurement Protocol methodology after v1.3 publication is the pair (SSRN 6761698, v1.3 SSRN ID) — readers of subsequent phase findings citing protocol methodology should be directed to both, with v1.3 as the controlling document on Phase A pivot validation.

OSF deposit is not required for v1.3: no new data is introduced, and the §6.4.8 worked example reads against the existing v0.16 OSF deposit at osf.io/ec6wh/v16/ (specifically `/data/phaseA/stage5_verdict.json` and the file's referenced `stage_results` field).

### §2.3 Forward integration

The v0.17 pre-registration (premium kitchenware) is the first phase to pre-register against v1.3 §6.4 directly. v0.17 Phase A applies the §6.4.2–§6.4.6 stage protocol and the §6.4.7 fallback rule with bounded override against the kitchenware brand panel before Phase B topic-ID resolution proceeds. Each fallback event — primary alternate activation, bounded override, or cell collapse — produces a §6.4.7.4-compliant DEVIATIONS entry at the time of the event. Subsequent phases inherit the same standard.

## §3 Cross-references to v1.2 sections preserved

v1.3 specifies an operational layer atop Protocol v1.2; it does not modify, supersede, or invalidate any v1.2 section. The full Protocol v1.3 document is the v1.2 document with §6.4 added and the version stamp updated; all other sections are byte-identical. This section enumerates the preservation explicitly to support auditability.

**§3.1 Framing and definitions (§1–§3 of v1.2).** The protocol's framing — the AI Availability construct, the Presence component as the protocol's measurement target, the relationship to the broader AIAS composite, and the four-regime taxonomy as canonical category-classification — is preserved unchanged. v1.3 introduces no construct-level modifications.

**§3.2 Pipeline architecture (§4–§5 of v1.2).** The four-phase pipeline (Phase A $\rightarrow$ Phase B $\rightarrow$ Phase C $\rightarrow$ Phase D), the inter-phase data contracts, and the reference model set specification are preserved unchanged. v1.3 adds an operational specification within Phase A but does not modify Phase A's interface with Phase B or Phase B's downstream consumption.

**§3.3 Stage protocols (§6.1–§6.3 of v1.2).** Phase A intent (§6.1), Phase B topic-ID resolution against Google Trends (§6.2), and Phase C LLM acquisition against the reference model set (§6.3) are preserved unchanged. v1.2 §6.1 stands as the statement of Phase A's purpose; v1.3 §6.4 specifies the five-stage operational procedure that realizes that purpose. The two are complementary: §6.1 explains *why* Phase A exists; §6.4 specifies *how* Phase A is conducted.

**§3.4 Scoring, reporting, and falsifiability (§7–§9 of v1.2).** The scoring rules for the Presence Index, the canonical figure set for phase publications, the limitations and falsifiability framing, and the relationship between the Protocol and the broader Tri-System theoretical programme are preserved unchanged.

The byte-identical claim is verifiable: the v1.3 Protocol document is structurally a diff against v1.2 with one positive entry (§6.4 added) and zero deletions or modifications elsewhere.

## §6.4 Phase A Pivot-Validation Specification

### §6.4.1 Motivation

Protocol v1.2 §6.1 specified the goal of Phase A pivot validation — the canonical pivot should establish the brand's substrate-category fit before Phase B topic-ID resolution proceeds — but did not centrally specify the operational structure of the validation. In practice, the AIAS programme implemented Phase A as a five-stage procedure: Knowledge Graph entity-suggestion audit, Trends baseline stability, bundled position against reference brands, adjacency-keyword discrimination, and verdict aggregation. The procedure was version-locked at the level of operational scripts from v0.11 onward but documented only by those scripts and by per-phase pre-registration §6 contingency text, not by the methodology paper.

v0.16 (kitchen knives) surfaced the gap operationally. The pre-registered pivot Victorinox failed Phase A on canonical-query Trends eligibility — the kitchen-knife brand presence sits below the 14-day Trends-eligibility floor on the bare canonical query. Per pre-reg §6, Wüsthof was activated as fallback pivot. Wüsthof's own Phase A run returned numeric failure on all three quantitative stages — Stage 2 CV at 42.19% against the 30.0% stability threshold, Stage 3 pivot-to-reference ratio at 0.0 against the [0.5, 5.0] band, Stage 4 `chef_proportion` at 0.004 against the 0.2 minimum with `swiss_army_proportion` at 0.996 against the 0.7 maximum. Wüsthof was nonetheless activated as the operational pivot per pre-reg §6 contingency, with manual intervention noted in the verdict's `next_steps` field and documented in DEVIATIONS Entry 3.

The substantive call was correct. The operational record was logged as a deviation because Protocol v1.2 did not specify (a) the canonical operational structure of Phase A, (b) the thresholds against which each stage passes or fails, or (c) the contingency rule when an activated alternate also numerically fails the same stages. The pre-registration discipline that the AIAS programme maintains requires that operations of this class be pre-registered ahead of acquisition, not retrospectively reconstructed.

v1.3 specifies these three components centrally as §6.4. The specification is descriptive of existing practice for the stages and their thresholds (§6.4.2 through §6.4.6) and prescriptive for the alternate-also-fails contingency (§6.4.7), which the v0.16 case exposed as a missing rule. The v0.16 case is retrospectively scored against the v1.3 specification in §6.4.8.

### §6.4.2 Stage 1 — Knowledge Graph entity-suggestion audit

Stage 1 documents the Google Knowledge Graph entity context for the pivot brand at validation time. The output is a set of N entity suggestions returned by the Trends suggestions API for the bare canonical brand name, with their Knowledge Graph identifiers, entity titles, and entity types.

**Input:** the pivot brand's canonical name; the bare-canonical query convention inherited per DEVIATIONS Entry 1 of the phase's prior-version lineage (v0.14 / v0.15 inheritance chain).

**Procedure:** the Trends suggestions endpoint (pytrends.suggestions() or equivalent SerpAPI implementation) is queried with the bare canonical brand name. The top N entity suggestions are captured, each with `mid` (Knowledge Graph identifier), `title` (entity name), and `type` (entity category from Knowledge Graph).

**Output:** `stage1_suggestions.json` with fields `pivot_canonical`, `session_timestamp`, `query_source`, `n_suggestions`, `suggestions`, `audit_note`. The `suggestions` field is a list of entity records; the `query_source` field records the query construction convention (the v0.16 production value is `bare_canonical_per_DEVIATIONS_Entry_1`).

**Threshold and verdict:** Stage 1 has no pass/fail criterion at the stage level. The Stage 5 verdict aggregator records `stage1_audit_n_suggestions` as a count audit (v1.3 commits N = 5 as canonical, matching v0.16's `stage1_audit_n_suggestions: 5`) but does not gate the Phase A pass/fail decision on Stage 1's output.

**Role of Stage 1 in the protocol.** Stage 1 is diagnostic, not parametric. Stage 4's adjacency keywords (substrate keyword and adjacent keyword) are pre-registered per substrate phase in the pre-registration's Phase A section — they are not derived from Stage 1's output. Stage 1's suggestions serve three secondary purposes: (a) operator pre-acquisition diagnostic — surfacing the pivot's Knowledge Graph entity diversity and any cross-category drift visible at the KG layer before the Trends-based stages run; (b) audit trail — recording the KG context at the time of validation for retrospective analysis; (c) forward compatibility — future protocol versions may use Stage 1 outputs to seed substrate-adaptive keyword construction, but v1.3 does not.

### §6.4.3 Stage 2 — Baseline Trends stability

Stage 2 verifies the pivot brand's bare canonical name returns a stable Google Trends signal over the pre-registered acquisition window.

**Input:** pivot brand canonical name; acquisition window (locked at pre-reg, defaulting to 14 days terminating on Stage 2 run timestamp); geographic scope (worldwide for primary; US for descriptive sensitivity per substrate phase pre-reg).

**Procedure:** SerpAPI Google Trends query against the bare canonical name; daily-mean series collected over the window; coefficient of variation computed as standard deviation divided by mean, expressed as percentage.

**Output:** `stage2_baseline.json` with fields `pivot_canonical`, `session_timestamp`, `window`, `geo`, `http_status`, `serpapi_error`, `n_days`, `mean`, `sd`, `min`, plus derived `cv_pct`.

**Threshold:** Stage 2 passes when `cv_pct` $\leq$ 30.0 (the v0.16 `stage2_cv_threshold_pct`). The threshold formalizes the criterion that the brand's Trends signal must be stable enough over the acquisition window to support meaningful comparison against reference brands in subsequent stages.

**Verdict:** `stage2_stability_pass` is a boolean; pass at `cv_pct` $\leq$ 30.0, fail otherwise.

### §6.4.4 Stage 3 — Bundle position

Stage 3 validates the pivot brand's position within the substrate's competitive reference set via a bundled Trends query.

**Input:** pivot brand canonical name; the pre-registered set of in-category reference brands for the substrate (typically the panel's primary brands from the pivot's tradition cell plus 2–3 cross-tradition references); the Stage 2 acquisition window.

**Procedure:** SerpAPI bundled Trends query of the pivot brand against the reference set; per-brand means and maxima computed over the window; `pivot_to_ref_ratio = pivot_mean / max(ref_means)`.

**Output:** `stage3_bundle_position.json` with fields `pivot_canonical`, `session_timestamp`, `window`, `query`, `http_status`, `serpapi_error`, `pivot_mean`, `pivot_max`, `ref_means`, `ref_median`, plus derived `pivot_to_ref_ratio`.

**Threshold:** Stage 3 passes when `pivot_to_ref_ratio` $\in$ [0.5, 5.0] (the v0.16 `stage3_pivot_to_ref_band`). The lower bound (0.5) ensures the pivot is not dominated by reference-set brands by more than 2x — i.e., the pivot is not a minor player in its claimed competitive set. The upper bound (5.0) ensures the pivot is not so dominant that the reference set fails to represent its competitive context — i.e., the pivot is in the right competitive tier, not above it.

**Verdict:** `stage3_position_pass` is a boolean; pass when the ratio is within the band, fail otherwise.

### §6.4.5 Stage 4 — Adjacency

Stage 4 verifies that the pivot brand's Trends signal anchors on the pre-registered substrate keyword, not on the pre-registered adjacent-category keyword.

**Input:** pivot brand canonical name; substrate keyword (the canonical category term pre-registered for the substrate phase, e.g., "chef" for kitchen knives); adjacent-category keyword (pre-registered for the substrate phase, e.g., "swiss army" for kitchen knives); the Stage 2 acquisition window. Both keywords are specified at pre-registration in the phase's Phase A section, not derived from Stage 1's output.

**Procedure:** bundled SerpAPI Trends query co-locating the pivot brand with substrate-keyword and adjacent-keyword anchors over the window. Per-anchor means computed. Proportions normalized to sum to unity: `substrate_proportion = substrate_mean / (substrate_mean + adjacent_mean)`; `adjacent_proportion = 1 $-$ substrate_proportion`.

**Output:** `stage4_adjacency.json` with fields `pivot_canonical`, `session_timestamp`, `window`, `query`, `http_status`, `serpapi_error`, `pivot_mean`, `substrate_mean`, `adjacent_mean`, plus derived `substrate_proportion`, `adjacent_proportion`. For backward compatibility with v0.16's deposit, the kitchen-knife substrate retains `chef_mean`, `swiss_army_mean`, `chef_proportion`, `swiss_army_proportion` as substrate-specific aliases.

**Threshold:** Stage 4 passes when `substrate_proportion` $\geq$ 0.2 AND `adjacent_proportion` $\leq$ 0.7 (the v0.16 `stage4_chef_prop_min` and `stage4_swiss_army_prop_max`). The two conditions operate in conjunction: the pivot must achieve a meaningful substrate signal AND not be dominated by the adjacent category. The 0.1 gap between 0.2 and (1 $-$ 0.7) is intentional: the protocol does not require pivot brands to be primarily category-anchored, only to be sufficiently category-anchored that downstream LLM acquisition does not measure the wrong category's AI Presence.

**Verdict:** `stage4_adjacency_pass` is a boolean; pass when both threshold conditions hold, fail otherwise.

### §6.4.6 Stage 5 — Verdict aggregation

Stage 5 aggregates Stages 1–4 into a per-pivot Phase A verdict.

#### §6.4.6.1 Stage-conjunction rule

Phase A returns PASS when Stages 2, 3, and 4 all return pass. Stage 1 is informational (Knowledge Graph entity-suggestion audit) and does not contribute to the pass/fail decision. If any of Stages 2, 3, or 4 fails, Phase A returns FAIL for the pivot under consideration.

#### §6.4.6.2 Output

`stage5_verdict.json` with fields `session_timestamp`, `pivot_canonical`, `stage_results` (dict containing each stage's audit metric and pass/fail flag for Stages 2–4; audit count for Stage 1), `verdict` (PASS or FAIL), `action` (next-step instruction conditional on verdict and on §6.4.7 fallback state), `panel_cell_impact` (description of the verdict's effect on the panel cell), `thresholds_applied` (dict of the canonical threshold values used), `next_steps`.

#### §6.4.6.3 Canonical thresholds (locked at v1.3)

```
stage2_cv_threshold_pct:        30.0
stage3_pivot_to_ref_band:       [0.5, 5.0]
stage4_substrate_prop_min:      0.2
stage4_adjacent_prop_max:       0.7
```

For backward compatibility with v0.16's deposit, kitchen-knife-substrate phases may name `stage4_chef_prop_min` and `stage4_swiss_army_prop_max` for `stage4_substrate_prop_min` and `stage4_adjacent_prop_max`. Threshold values are constant across substrates at v1.3.

#### §6.4.6.4 Threshold heritage and provider stability

The threshold values were established empirically during v0.6–v0.15 development and locked at v0.16 as production values. v1.3 does not modify them. Future phases report stage-level metric values alongside the binary pass/fail verdict to build the data corpus for a future threshold-sensitivity analysis. Phase A has no LLM dependencies; reference-model-set changes (per Protocol v1.2 §5.2) affect Phase C and downstream cross-phase comparability but do not directly affect Phase A's stage-level metrics or thresholds. Trends-provider changes (e.g., SerpAPI deprecation, switch to a successor pytrends-equivalent service) do affect Phase A directly and trigger a minor-version protocol increment with re-calibrated thresholds against the successor provider's measurement characteristics.

### §6.4.7 Fallback activation rule ($R_F$) with bounded override

When Stage 5 returns FAIL, the pivot is excluded from operational use and a fallback procedure activates. v1.3 specifies bounded override as the canonical fallback structure.

#### §6.4.7.1 Primary alternate activation

Per Protocol v1.2 §6 and the pre-registration's §6 alternate sequence, the next pre-registered alternate brand in the failed pivot's tradition cell is activated as candidate pivot. The activated alternate undergoes Phase A in full (Stages 1–5).

#### §6.4.7.2 Bounded override

If the activated alternate also returns Stage 5 FAIL, the operator may invoke a one-time bounded override per cell per phase. Bounded override permits the failing alternate to serve as operational pivot for downstream Phase B and Phase C work, with the activated pivot exiting within-cell scoring as it would under a passing verdict.

**Conditions for bounded override:**

- The override is logged in DEVIATIONS at the time of override (not retrospectively at publication) with: (a) the failing alternate's stage-level metric values, (b) the operator's substantive justification for accepting the failure, (c) the next-pre-registered-alternate ordinal position in the cell's alternate sequence, (d) explicit statement that no further alternates will be tried under this phase's pre-reg.
- Bounded override is one-time per tradition cell per phase. If a second alternate-also-fails event occurs in the same cell, the cell collapses (§6.4.7.3).
- Bounded override does not modify the activated alternate's Stage 5 FAIL verdict. The published findings continue to report the verdict as FAIL with the bounded override invoked.

#### §6.4.7.3 Cell collapse

If all pre-registered alternates in a cell fail Stage 5 and bounded override is unavailable (already used in the cell within this phase, or operator declines), the cell is marked `CELL_COLLAPSE`. Brands from a collapsed cell do not contribute to the worldwide $\rho$ computation. Cell collapse is reported in §Limitations of the published findings and is grounds for a registry-revision DEVIATIONS entry in the subsequent phase.

#### §6.4.7.4 Audit log requirement

Every fallback event — successful alternate activations (passing Phase A on a second attempt), bounded overrides (FAIL accepted under override), and cell collapses — produces a DEVIATIONS entry at the time of the event. The entry includes: failed primary pivot identification, Phase A stage-level results for the primary; activated alternate identification, Phase A stage-level results for the alternate; the fallback outcome (cascade-success, bounded-override, or cell-collapse); panel-cell-impact statement.

### §6.4.8 Worked example — v0.16 retrospective application

v0.16 Phase A pivot validation, scored against v1.3 §6.4.2 through §6.4.7.

**Victorinox (pre-registered pivot).** Failed Phase A. Per the v0.16 paper §4.3, the failure mode was canonical-query Trends eligibility — Victorinox's bare canonical query returned kitchen-knife brand presence below the Trends-eligibility floor. The stage-level decomposition is not preserved in the v0.16 deposit (the Phase A stage files were overwritten when Wüsthof was activated as alternate and re-run). The paper-narrative description is consistent with a Stage 2 or Stage 4 failure under v1.3 decomposition. Per §6.4.7.1, the next pre-registered alternate (Wüsthof) was activated.

**Wüsthof (first alternate).** Failed Phase A on all three quantitative stages, preserved in the v0.16 OSF deposit at `osf.io/ec6wh/v16/data/phaseA/stage5_verdict.json`:

- Stage 1 (entity-suggestion audit): `n_suggestions = 5` — informational, no pass/fail.
- Stage 2 (baseline stability): `cv_pct = 42.19%` against the 30.0% threshold. `stage2_stability_pass: false`.
- Stage 3 (bundle position): `pivot_to_ref_ratio = 0.0` against the [0.5, 5.0] band. `stage3_position_pass: false`.
- Stage 4 (adjacency): `chef_proportion = 0.004` against the 0.2 substrate minimum, with `swiss_army_proportion = 0.996` against the 0.7 adjacent maximum. `stage4_adjacency_pass: false`.

Stage 5 returned `verdict: FAIL` per §6.4.6.1 (Stages 2, 3, and 4 all failed; Stage 1 informational). Under Protocol v1.2, no rule governed the alternate-also-fails case; the operator invoked manual intervention and proceeded with Wüsthof as operational pivot per pre-reg §6 contingency. The action was logged in DEVIATIONS Entry 3.

**v1.3 retrospective classification.** The v0.16 operator action falls within the scope of §6.4.7.2 bounded override: alternate-also-fails accepted with operator activation. Under v1.3, the same action would be pre-registered as a bounded-override invocation, with DEVIATIONS Entry 3 documenting per §6.4.7.4: the failed primary pivot's narrative-recorded failure mode (stage-level results not preserved); Wüsthof's three-stage numeric failure; the bounded-override invocation at the first alternate (no cascade attempts beyond); and the panel-cell-impact statement matching v0.16's published "Wüsthof exits within-cell scoring, German cell scored at n = 4" consequence.

The v0.16 case is consistent with the v1.3 §6.4.7 bounded override structure. Pre-registration of the same case under v1.3 would have committed the bounded override rule ahead of acquisition rather than recording the operational handling as a post-hoc deviation.

## §7 Limitations of v1.3

Limitations are organized by scope — what §6.4 addresses, what dependencies it introduces, what design choices remain operator-judgment, and what the worked example does and does not establish.

### §7.1 Scope: what §6.4 addresses and what it does not

§6.4 specifies Phase A pivot validation only. Pipeline failure modes outside Phase A's scope remain under their respective v1.2 specifications and are not modified by v1.3:

- **Phase B topic-ID resolution failures** — EXCLUDED_E1a / E1b at the per-brand level during Phase B's own five-stage topic-ID resolution protocol (per v1.2 §4) — remain under v1.2 §4. The exclusion codes E1a and E1b apply at both Phase A (pivot-level) and Phase B (per-brand-level); v1.3 specifies only the Phase A application. Phase B's five-stage protocol — distinct from Phase A's five-stage protocol despite both having five stages — is not modified.
- **Registry-coverage exclusions** — brands omitted at registry construction for insufficient market presence, missing tradition-cell assignment, or other registry-stage criteria — remain at the registry-construction layer and precede Phase A entirely.
- **Phase D scoring-stage eligibility** — brands that pass Phases A through C but fail the n-floor or other scoring-stage filters in Phase D — remains under v1.2 §7.

§6.4 also does not address cross-substrate brand allocation for brands with genuine multi-substrate presence — that question is taken up in §7.5.

### §7.2 SerpAPI dependency

§6.4 introduces one external-service dependency that did not exist at v1.2 §6.1's level of intent specification. Stages 1, 2, 3, and 4 all use SerpAPI as the Google Trends provider — Stage 1 for the entity-suggestions endpoint, Stages 2 through 4 for the Trends timeseries and bundled-query endpoints. SerpAPI rate limits, API contract changes, and deprecation are operational risks that the v1.3 specification inherits from the operational implementation. v1.3 does not specify a fallback Trends provider or a degraded-mode acquisition rule for SerpAPI outages: Phase A runs against an unavailable SerpAPI are paused with a session-timestamp gap and resume when service is restored. Sustained SerpAPI deprecation would require a minor-version protocol increment to specify a successor Trends provider and re-calibrated thresholds against the successor's measurement characteristics.

Phase A has no LLM dependencies. The LLM reference model set specified in Protocol v1.2 §5.2 governs Phase C acquisition only; Phase A operates independently of the LLM reference set.

### §7.3 Threshold heritage and forward sensitivity analysis

The four canonical threshold values locked at §6.4.6.3 — `stage2_cv_threshold_pct: 30.0`, `stage3_pivot_to_ref_band: [0.5, 5.0]`, `stage4_substrate_prop_min: 0.2`, `stage4_adjacent_prop_max: 0.7` — were established empirically during v0.6 through v0.15 development against the substrates measured in those phases (premium tea, skincare, finance, project-management software, plus retired exploratory substrates). No formal sensitivity analysis of these thresholds was conducted or published prior to v1.3. v1.3 locks them as production values to preserve cross-phase comparability of Phase A verdicts; v1.3 does not validate them as optimal.

Three transparency commitments follow from the heritage:

- **Stage-level metric reporting in published findings.** Phase findings papers report the per-pivot stage-level metric values alongside the binary pass/fail verdict. The v0.16 paper §4.3 narrates pivot-level outcomes; subsequent phases under v1.3 should additionally publish a stage-level metric table for the panel's Phase A runs.
- **OSF deposit of Phase A data.** Per-phase OSF deposits include the full `phaseA/` directory (stage1 through stage5 JSON outputs) so external readers can re-derive stage-level metrics and apply alternate thresholds for sensitivity analysis.
- **Future sensitivity analysis.** A dedicated methodological note covering threshold sensitivity is committed to the AIAS programme's medium-term roadmap, once five to seven phases of post-v1.3 stage-level data have accumulated to support the analysis.

### §7.4 Operator judgment in bounded override

§6.4.7.2 permits a one-time bounded override per tradition cell per phase when an activated alternate also fails Stage 5. The override permits operational continuation of a failing pivot — explicitly accepting the Stage 5 FAIL verdict rather than cascading through additional alternates or collapsing the cell. The override's substantive justification, recorded in the DEVIATIONS audit log, is operator judgment. v1.3 does not constrain the justification's content beyond requiring the four log fields specified at §6.4.7.4.

This is a named degree of freedom. The bounded structure (one-time per cell per phase; mandatory DEVIATIONS log; explicit statement that no further alternates will be tried) limits the scope of the freedom. But the substantive choice to invoke override rather than cascade — and the choice to invoke at the first alternate-fail rather than after a deeper cascade — sits with the operator. v1.3 names this as the intended structure rather than as a limitation to engineer around: not every methodological judgment can be reduced to an automatic decision rule, and the auditability of operator judgments via DEVIATIONS is the protocol's accountability mechanism for the freedom it preserves.

### §7.5 Multi-anchor brands

Stage 4's adjacency check tests the pivot brand's Trends signal against one pre-registered adjacent-category keyword. For brands with genuine multi-substrate presence — Le Creuset across cookware, bakeware, and kettles; Tom Ford across fragrance, beauty, and apparel — a single adjacency check may understate the pivot brand's category-anchoring problem if the substantive cross-category drift is distributed across two or more adjacent categories.

The protocol presupposes a single substrate per measurement phase. Brands that span multiple substrate categories are handled by Stage 4 either passing (if `substrate_proportion` meets the threshold against the pre-registered adjacent keyword) or failing (if not). The protocol does not specify a multi-substrate brand-handling rule that allocates a brand's measurement across substrates.

The v0.18 indie fragrance phase, with brands that span fragrance, candles, and personal-care substrates, may surface this limitation; v1.x increments may address it through cross-substrate brand allocation or through a multi-adjacency Stage 4 variant. v1.3 does not.

### §7.6 Status of the v0.16 retrospective application

The §6.4.8 worked example is post-hoc, applied retrospectively to v0.16 data. It demonstrates that the operator action taken under v1.2 (Wüsthof activated despite Stage 5 FAIL) maps cleanly onto the §6.4.7.2 bounded-override structure specified in v1.3 — but consistency between an existing action and a newly-specified rule is not validation of the rule. The first pre-registered application of v1.3 §6.4 is the v0.17 kitchenware phase. Subsequent phases inherit the standard. Genuine validation of v1.3 §6.4 against operational use accumulates over the first three to five phases pre-registered under it.

## §8 Declarations and references

**Declaration of competing interest.** The author is employed full-time at Samsung Electronics America (Director, Corporate Brand Creative and Governance). The AIAS Presence Measurement Protocol and the broader Third System programme are independent research conducted under the SVA MPS Branding Program affiliation and the Third System research entity. Samsung Electronics America did not commission, fund, or review this research. No Samsung products are measured in any AIAS programme phase to date; Samsung is not represented in any published or in-pipeline brand panel. The author declares no other competing interests.

**Funder.** Self-funded.

**Ethics.** Not applicable; no human subjects. Data collection uses public Google Trends API (via SerpAPI) and public LLM API endpoints under standard developer terms of service.

**Data availability.** v1.3 introduces no new measurement. The §6.4.8 worked example reads against the v0.16 OSF deposit at osf.io/ec6wh/v16/, specifically `/data/phaseA/stage5_verdict.json` and its `stage_results` field. The full v0.16 Phase A audit trail — `stage1_suggestions.json` through `stage5_verdict.json` — is deposited in the same `/data/phaseA/` directory.

**References**

González Castro, P. U. (2026a). AI Availability: A Theoretical Framework for Brand Surfacing in the Age of LLM-Mediated Discovery. *SSRN Working Paper Series*. https://ssrn.com/abstract=6659000

González Castro, P. U. (2026b). The AIAS Presence Measurement Protocol: Methodological Notes on Construct Validity and the Four-Regime Taxonomy (v1.2). *SSRN Working Paper Series*. https://ssrn.com/abstract=6761698

González Castro, P. U. (2026c). Regime 4 Boundary and Discourse-Language Carryforward on the Kitchen-Knives Substrate (v0.16). *SSRN Working Paper Series*. https://ssrn.com/abstract=6791999
