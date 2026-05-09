# AIAS v0.10 — Pre-Registration

**Title.** Naive-Phantom Rate Longitudinal Stability — Mint Designed-for-Test Subset, t₁→t₂

**Version.** v0.10 pre-registration · draft for git lock
**Methodology Protocol.** AIAS Presence Measurement Protocol v1.1 (SSRN 6722319)
**Registry.** brands_pmtools_v0.6 (frozen)
**Date drafted.** 2026-05-09
**Lock target.** git commit prior to any application of the v0.7 caveat-classifier to v0.9 raw responses
**Author.** Pablo Ulpiano Gonzalez Castro
**Research entity.** Third System™

**Cross-cites.** AI Availability foundational paper (SSRN 6659000) · AIAS Presence Measurement Protocol v1.1 (SSRN 6722319) · v0.6 Cross-Category Findings (SSRN 6720959) · v0.7 Phantom-Brand BBB (SSRN 6721779) · v0.8 Discourse-Language Knives (SSRN 6728000) · v0.9 Longitudinal Re-Baseline (SSRN 6736878).

---

## 1. Background

v0.7 (Phantom-Brand BBB) introduced a designed-for-test reframe distinguishing two phantom-brand presence types for **Mint**, the personal-finance application decommissioned by Intuit in March 2024:

- **Naive-phantom presence.** The brand is recommended or described as if currently available — no caveat about decommissioning, sunset, or discontinuation appears anywhere in the response.
- **Caveated-phantom presence.** The brand is mentioned but accompanied by explicit acknowledgment of decommissioning or successor-product migration.

At v0.7 BBB the naive-phantom rate for Mint was **1.7%**, against a gross Presence rate of **38.2%**. The two are mechanistically distinct: gross Presence indexes whether the retrieval system surfaces the brand at all; naive-phantom rate indexes the subset of those surfacings delivered as live recommendations.

v0.9 (Longitudinal Re-Baseline) confirmed gross Presence stability for Mint within the pre-registered ±5pp band (44.8% → 41.7%, |Δ|=3.1pp) under H4. What v0.9 H4 did not test is whether the naive-phantom *subset* exhibits comparable stability — that is, whether AI systems' tendency to recommend Mint as if fully live persists at the same rate over the longitudinal interval, separately from the gross-mention rate.

v0.10 tests precisely this: **does the naive-phantom rate exhibit longitudinal stability comparable to gross Presence?**

The substantive question matters for the program's theoretical contribution. v0.7 framed the phantom mechanism in terms of two distinguishable failure modes — bare retrieval and recommendation-as-live. v0.9 demonstrated that gross retrieval is durable. v0.10 asks whether the more consequential subset — recommendation slots delivered without caveat — is also durable, or whether classifier-detectable correction is propagating through the model substrate over the longitudinal window.

**No new measurement is required.** v0.9 deposited raw responses for both waves at OSF project ec6wh, /v09/data/responses/. v0.10 applies the v0.7 caveat-classifier to the Mint subset of those responses.

---

## 2. Hypotheses

### H1 (primary, confirmatory) — Naive-Phantom Rate Stability

The naive-phantom rate for Mint is stable t₁→t₂ within a **±2pp** band.

- **Operationalization.** r_naive,wave = N_naive / N_matched-subset, computed independently for t₁ and t₂, restricted to the matched-classifier subset (§4).
- **Confirmed if** |r_naive,t₂ − r_naive,t₁| ≤ 2.0 pp.
- **Falsified if** |r_naive,t₂ − r_naive,t₁| > 2.0 pp, in either direction.

### H2 (secondary, confirmatory) — Naive-Phantom Persistence

The naive-phantom rate is non-zero at both waves.

- **Confirmed if** r_naive,t₁ > 0 AND r_naive,t₂ > 0.
- **Falsified if** r_naive = 0 at either wave.

H2 protects against the interpretation that v0.7 BBB's naive rate was an artifact of the v0.7 measurement window. Stability under H1 is informative only if there is a non-zero rate to be stable.

### H3 (exploratory) — Naive-vs-Gross Co-Movement

The directional change in naive-phantom rate is consistent with the directional change in gross Presence rate as reported in v0.9.

- **Diagnostic only**, no falsification status.
- Reported as: directional concordance (both rise / both fall / decoupled) and magnitude ratio |Δr_naive| / |Δr_gross|.
- Substantive interpretation reserved for the discussion section, contingent on H1 outcome.

---

## 3. Threshold Justification

The ±2pp band for H1 is **tighter** than the ±5pp band used in v0.9 H4 (gross Presence). Three considerations support the choice.

1. **Proportional sensitivity to base rate.** The v0.7 BBB baseline naive-phantom rate is 1.7%. A ±5pp band on this base rate would permit the observed rate to triple or fall to zero while remaining classified as "stable" — semantically inadequate for a stability test.
2. **Symmetry preservation.** A ±2pp band on a 1.7%-class baseline permits the rate to range across approximately [0.0%, 3.7%] under stability. Bounded but allows the natural asymmetry of small base rates without forcing artificially tight detection.
3. **Sampling-variance acknowledgment.** Single-response flips translate to large pp shifts at small matched-subset n. **Effective n at the matched subset will be reported alongside the result**, allowing readers to calibrate the test's effective resolution. The pre-registered band is fixed at ±2pp regardless of effective n; we do not adjust the threshold post hoc to absorb sampling noise.

The choice of ±2pp over ±3pp reflects a deliberate preference for a tighter test where the substantive theory (recommendation-slot persistence) implies that meaningful drift should be detectable rather than absorbed into the band. The cost is higher Type I risk under sampling noise, which we accept and disclose transparently. Note that the v0.7 baseline of 1.7% is **background context only**; t₁ may resolve to a different value, and the test evaluates t₁ vs t₂ regardless of how either compares to the v0.7 BBB datapoint.

### 3.4 Effective-n Floor

H1 is evaluated only if the matched-subset effective n (responses containing a Mint mention) is **≥ 100 at both waves**. The floor is specified such that a single-response classification change moves r_naive by ≤ 1.0 pp — half the ±2pp stability band — preserving the test's resolution against single-flip sampling noise.

If effective n < 100 at either wave, H1 is declared **underpowered** and reported as indeterminate. The naive-phantom rates are still computed and reported as descriptive, with an explicit underpowered flag in the canonical scoring document. v0.10 terminates at descriptive disclosure under that condition; no confirmatory claim about stability is made.

The floor is fixed at lock and is not adjusted post hoc.

---

## 4. Data and Matched Subset

### Source

v0.9 raw responses, deposited at OSF project ec6wh, path /v09/data/responses/, under git tag `v0.9-published`. **No new prompting, no new model calls, no new wave windows.**

### Restriction

- **Brand.** Mint only. v0.10 is a single-brand designed-for-test extension of the v0.7 BBB protocol, not a category-wide claim.
- **Models — matched subset.** Sonnet 4.6 + gpt-5.4-mini, identical to the v0.9 H4 matched subset. Other models present in the v0.9 deposit are excluded for v0.10.
- **Waves.** t₁ and t₂ as defined in v0.9 pre-registration. Wave windows, prompts, and registry are inherited unchanged from v0.9; brands_pmtools_v0.6 remains frozen.

### Unit of Analysis

A single response (one model × one prompt × one wave). Each response containing a Mint reference is independently classified into one of three mutually exclusive categories: (a) naive-phantom, (b) caveated-phantom, (c) no Mint presence.

---

## 5. Classifier Operationalization

The v0.7 caveat-classifier (specified in v0.7 §[classifier-method-section, to be cited at v0.7 §reference at lock]) applies the following rule set to each response containing a Mint mention:

- **Caveated** if the response contains explicit acknowledgment of any of: decommissioning, shutdown, sunset, discontinuation, end-of-life, migration to successor product (Credit Karma), historical-reference framing ("Mint was…"), or temporal qualifier indicating non-current availability.
- **Naive** if the response describes Mint, recommends Mint, or provides feature/usage details with no such acknowledgment present anywhere in the response.

The classifier inherits the v0.7 keyword/phrase rule list and judge-LLM verification protocol unchanged. The full v0.7 rule list is reproduced verbatim in `/v10/registries/v07_caveat_classifier.json` prior to commit lock.

### Pre-Specified Decision Rules — Edge Cases

**E1 — Zero Mint mentions in a wave.** If a wave contains no responses with Mint presence (denominator restricted to *responses containing Mint*: zero), r_naive for that wave is **undefined**, not zero. H1 cannot be evaluated under that condition; H2 is automatically falsified for that wave. The condition is reported transparently and v0.10 terminates at descriptive disclosure rather than confirmatory claim. (Note: this condition is not anticipated given v0.9's reported gross Presence rates of 44.8% / 41.7%, but the rule is pre-specified for completeness.)

**E2 — Zero naive-phantom presence in one wave only.** If r_naive resolves to 0.0% in one wave and a non-zero value in the other, H1 evaluates the absolute difference against the ±2pp band as specified. H2 is falsified. The directional asymmetry is reported and presented in discussion as evidence of one-sided correction in the model substrate.

**E3 — Light-hedging ambiguity.** Responses containing weak hedging language (e.g., "you might want to verify availability"; "as of the model's knowledge cutoff…") **without explicit decommissioning acknowledgment** are classified as **naive-phantom in the primary analysis**. A sensitivity analysis re-classifying these as caveated is reported as a robustness check, with both rates disclosed in the canonical scoring document. The primary-analysis convention preserves alignment with v0.7's classifier as written; the sensitivity analysis transparently exposes the boundary's effect on H1 outcome.

**E4 — Classifier-judge disagreement.** Where the rule-based classifier and the judge-LLM verification disagree, the response is hand-adjudicated by the author against the v0.7 rule set as written. Adjudication decisions are logged in `/v10/data/adjudication_log.csv` with timestamp, response ID, rule applied, and decision rationale. The full log is committed to OSF as part of the v0.10 deposit. Adjudication rate (% of responses requiring author intervention) is reported alongside H1 outcome as a classifier-confidence diagnostic.

**E5 — Successor-product framing.** Mentions framed primarily as Credit Karma migration, with Mint introduced only as antecedent context, are classified as **caveated** if the migration framing appears in the same paragraph as the Mint mention; **naive** otherwise. This rule is documented here because Mint→Credit Karma migration is foreseeably the dominant decommissioning frame and warrants explicit pre-specification.

---

## 6. Analysis Plan

1. Pull v0.9 raw responses from OSF /v09/data/responses/, filter to Mint subset within matched-subset models, separate by wave.
2. Apply v0.7 caveat-classifier to each response in the filtered subset.
3. Apply judge-LLM verification.
4. Resolve disagreements per E4; log all adjudications.
5. Compute r_naive,t₁; r_naive,t₂; |Δr_naive|; r_caveated,t₁; r_caveated,t₂; effective n per wave. Verify n ≥ 100 floor at both waves before proceeding to H1 evaluation per §3.4; if floor is breached, route to descriptive disclosure path.
6. Evaluate H1, H2 against pre-registered thresholds.
7. Compute H3 diagnostic against v0.9-reported gross Presence values.
8. Produce sensitivity analysis per E3.
9. Generate canonical scoring document (CSV + JSON).
10. Build report (build_report_v10.py forks build_report_v09.py; build_charts_v10.py with naive-phantom-specific charts).
11. Draft SSRN paper.
12. Deposit at OSF project ec6wh, /v10/.

**No additional analyses beyond the above will be reported as confirmatory.** Any further exploration is labeled exploratory and confined to the discussion section.

---

## 7. Falsification Summary

| Hypothesis | Confirmed | Falsified | Indeterminate |
|---|---|---|---|
| **H1** — Stability | \|Δr_naive\| ≤ 2.0 pp | \|Δr_naive\| > 2.0 pp | E1 holds at either wave OR effective n < 100 at either wave (per §3.4) |
| **H2** — Persistence | r_naive > 0 at both waves | r_naive = 0 at either wave | E1 holds at either wave |
| **H3** — Co-movement | n/a (diagnostic) | n/a | n/a |

---

## 8. Deviations and Amendments

Any deviation from this pre-registration after git lock is logged in `/v10/DEVIATIONS.md` with timestamp, change rationale, and the original-vs-amended specification. The v0.10 paper carries an explicit deviations section in its declarations block. Substantive amendments after data are touched are flagged as exploratory in the published paper, regardless of label.

---

## 9. Methodology Version and Cross-References

- **AIAS Presence Measurement Protocol.** v1.1 (unchanged from v0.9) — SSRN 6722319.
- **Brand registry.** brands_pmtools_v0.6 (frozen, identical to v0.7 / v0.8 / v0.9) — distributed under `/v10/registries/`.
- **v0.9 raw response source.** OSF project ec6wh, /v09/data/responses/, git tag `v0.9-published`.
- **v0.7 caveat-classifier specification.** SSRN 6721779 + rule list reproduced verbatim in `/v10/registries/v07_caveat_classifier.json`.

---

## 10. Authorship and Declarations

**Author.** Pablo Ulpiano Gonzalez Castro.
**Research entity.** Third System™ (thirdsystem.ai).
**Affiliation (academic).** Faculty, MPS Branding, School of Visual Arts.
**COI declaration.** The author is also Director of Corporate Brand Creative and Governance at Samsung Electronics America. The v0.10 study, like all AIAS program publications, is independent research developed outside the scope of that employment. Mint and Credit Karma are not Samsung properties.
**Funding.** None.
**Data and code availability.** All raw responses, classifier configs, adjudication logs, scoring outputs, registry files, and build scripts are deposited at OSF project ec6wh, /v10/, prior to SSRN submission.

---

## 11. Lock

This document is locked at git commit `8767f44` on `2026-05-09`, **prior to any application of the v0.7 caveat-classifier to the v0.9 Mint response subset**. No analysis output exists at the moment of lock.
