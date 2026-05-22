# v0.12 Deviations and Methodology Notes

This file documents post-lock methodology observations during the v0.12
acquisition session. None of the entries below modify the pre-registered
hypotheses, thresholds, or analytic design; they document operational
choices that future versions of the AIAS programme will benefit from.

---

## Entry 1 — Olive oil Bundle 2 padding choice produces quantization noise

**Locked acquisition timestamp:** 2026-05-11T10:33:22Z
**Affected bundle:** `oliveoil_bundle_2_*` (Worldwide and US regions)
**Composition:** California Olive Ranch (pivot) + Brightland + Graza + Kosterina + "extra virgin olive oil" (padding)

**Observation.** The padding query "extra virgin olive oil" — chosen at pre-reg
lock to fill the fifth bundle slot — is a generic category term with absolute
search volume orders of magnitude higher than any premium brand in the bundle.
This caused the bundle's 0–100 relative-scaling reference to be set by the
padding term, compressing the brand and pivot raw values to small integers:

- Worldwide: pivot (California Olive Ranch) raw values 2–3 across 14 days;
  Brightland 1–2; Graza 8–10; Kosterina constant at 1; padding 73–100.
- US: pivot 3–5; Brightland 2–3; Graza 13–18; Kosterina 1–2;
  padding 67–100.

**Quantitative impact.** Integer quantization in raw values 1–3 produces
substantial pivot-rescaling noise: single-integer changes in numerator or
denominator swing rescaled values by 30–50%. Per-day rescaled values for
Bundle 2 brands carry an effective precision of ±20–30%.

**Qualitative impact.** None on rankings. Brand ordering is robust across
both regions: Graza >> Brightland > Kosterina, with Kosterina effectively at
the Trends absolute-volume floor (raw value = 1 every day Worldwide).

**Disposition.** Acquisition is retained as-is. Reasons:
1. Olive oil is routed to descriptive-only per pre-reg §3.4a; no confirmatory
   inference depends on precision-of-rescaled-means for this category.
2. The Category-Scale Mismatch Finding (pre-reg §10) reports per-brand AI
   Presence alongside Trends acquisition outcome qualitatively. The noise
   floor does not undermine the finding.
3. Re-acquiring would split the locked acquisition across two timestamps —
   a methodological cost without proportional benefit for a descriptive arm.

**Reporting in v0.12 paper.** The v0.12 paper's Category-Scale Mismatch
section will note (a) the bundle composition, (b) the quantization
characteristic for Bundle 2 olive oil brands, (c) that absolute
pivot-rescaled values carry ±20–30% noise, and (d) that rankings remain
robust.

**Methodology lesson for v0.13+.** Bundle padding must be brand-volume-
comparable. Generic category terms (e.g., "extra virgin olive oil",
"running shoes", "project management software") have absolute search
volumes orders of magnitude higher than individual brands and will swamp
the bundle's 0–100 scale. v0.11's PM software Bundle 5 used kanban / agile
/ scrum padding — these are concept terms in the same volume order as
brand searches and produced no quantization issue. Future-version padding
selections should follow that template: brand-comparable concept terms
specific to the category, not generic product-category terms.

**Pre-reg compatibility.** This is a methodology note, not a deviation
from pre-registered design. The pre-reg §5.1 specifies the pivot-rescaling
formula (which proceeds normally); §10 specifies the Category-Scale
Mismatch Finding as descriptive (which is not noise-sensitive at this
level). No hypothesis, threshold, n-floor, or analytic rule is modified.
