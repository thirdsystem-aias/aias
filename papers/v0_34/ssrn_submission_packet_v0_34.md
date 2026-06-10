# SSRN Submission Packet — AIAS™ v0.34

**Paper:** Two-Wave Temporal Stability of an AI Brand-Recall Consistency Quantity
**File to upload:** `papers/v0_34/v0_34_ssrn_paper.pdf`
**Submission target:** SSRN — papers.ssrn.com → Submit a paper
**Date prepared:** June 2026

---

## Step 1 — Paper type

- **Working Paper**

## Step 2 — Document Settings

- **Document type:** Article
- **License:** All rights reserved
- **Display abstract:** Yes
- **Allow citations:** Yes
- **Allow downloads:** Yes

---

## Step 3 — Paper details

### Title (paste verbatim — SSRN has one Title field; subtitle folded in)

```
Two-Wave Temporal Stability of an AI Brand-Recall Consistency Quantity: A Pre-Registered Longitudinal Re-Acquisition Across Five Product Categories (AIAS™ v0.34)
```

### Subtitle (titlepage only — SSRN has no separate subtitle field; folded into Title above)

```
A Pre-Registered Longitudinal Re-Acquisition Across Five Product Categories (AIAS™ v0.34)
```

### Abstract (paste verbatim — matches paper page 2)

```
Whether quantities derived from large language model (LLM) outputs are stable enough over time to function as brand-measurement instruments is an open empirical question. This study reports a pre-registered, two-wave longitudinal re-acquisition of the AIAS™ measurement protocol across five product-category panels (audiophile headphones, skincare, cosmetics, automotive, premium spirits; 112 brand units), re-running each panel's original acquisition pipeline verbatim 15–21 days after first measurement against a fixed six-model panel spanning three providers. Four hypotheses were pre-registered and externally anchored before re-acquisition. H_CPC_Temporal_Stability was CONFIRMED: per-brand rank order of the CV-based consistency quantity (CV-CPC) was stable in four of five categories (Spearman ρ = 0.76–0.96; the exception, the smallest panel, ρ = 0.42, n.s.). H_CPC_Drift_Beyond_Presence was MARGINAL by structural collapse: recognition saturation in four of five categories rendered Presence-residualization a no-op, leaving one informative category — in which residualized stability (ρ = 0.61) exceeded raw stability (ρ = 0.42). H_Presence_Temporal_Stability was MARGINAL by ceiling: rank stability was high wherever rank variance existed (ρ = 0.81–1.00), but two categories were recognition-constant in both waves. Phantom status (below-recall-floor) persisted in 56 of 57 brands. The findings characterize CV-CPC's temporal behavior without validating it as a Consistency instrument, document pervasive recognition-ceiling effects in consumer categories, and motivate the mean-independent instrument requirement of the forthcoming v1.8 methodology revision.
```

### Keywords (paste verbatim, semicolon-separated)

```
AI availability; brand availability; AIAS; large language models; temporal stability; test–retest reliability; consistency; CV-CPC; recognition saturation; pre-registration; Ehrenberg-Bass; brand recall
```

### JEL codes (paste verbatim)

```
M31; L86; L15; D83; M37
```

**JEL rationale (for your reference):** M31; L86, L15, D83, M37

---

## Step 4 — Subject classifications (select up to 7)

Select these networks/eJournals on the SSRN classification picker:

1. **Marketing eJournal**
2. **Marketing Strategy eJournal**
3. **Consumer Behavior eJournal**
4. **Advertising & Marketing Communication eJournal**
5. **Information Systems eJournal**
6. **Artificial Intelligence eJournal**
7. **Decision-Making Under Risk & Uncertainty eJournal**

(Same classification set as v0.16–v0.21 papers for consistency.)

---

## Step 5 — Authors, affiliations, contact

```
Pablo Ulpiano González Castro

School of Visual Arts (SVA), MPS Branding Program
New York, NY, United States

Third System™ (research entity; data archive and methodology venue)
thirdsystem.ai

Email: pablou@pablou.com
Website: pablou.com
ORCID: 0009-0003-8968-9990
```

---

## Step 6 — Declarations (Conflict of Interest, Funding, Ethics)

### Declaration of Interest (paste verbatim)

```
The author is Director, Corporate Brand Creative and Governance at Samsung Electronics America. This study re-acquires measurements against brand registries fixed in earlier phases (v0.19--v0.23); it performs no new brand selection, and each registry carries its source-phase conflict-of-interest handling forward unchanged. Two items of record apply. In the automotive registry, Samsung subsidiaries hold tier-2/3 component supply relationships with several registry brands --- Harman International (audio systems), Samsung SDI (battery cells), and Samsung Display (infotainment) --- characterized in the source phase as non-competitive, with no brand-level overlap, and imposing no operational restriction on registry composition (v0.22 Declarations; screened in v0.22 DEVIATIONS Entry 0, Part B). In the audiophile-headphones registry, AKG was substituted with Denon before the v0.19 pre-registration lock because AKG's parent, Harman International, is a Samsung subsidiary. Acquisition, coding, and scoring are fully automated against the locked registries; the pre-registration was tagged and externally deposited before any second-wave call; and the author's affiliation played no role in registry construction, acquisition, scoring, or the resulting verdicts. Samsung Electronics had no role in the design, conduct, analysis, or reporting of this work.
```

### Funder (paste verbatim)

```
Self-funded.
```

### Ethics statement (paste verbatim)

```
Not applicable; no human subjects; public APIs and LLM prompts only.
```

### Data and code availability (paste verbatim)

```
All materials are deposited at OSF, `ec6wh/v34`: the locked pre-registration (`v0.34-prereg-r1`, externally deposited before acquisition), both waves' acquisition outputs and the provenance sidecar, the acquisition manifest with per-substrate probe-set SHA-256 checksums, the scorer (`score_v34.py`), the verdicts (`v34_verdicts.json`), and the figure sources.
```

---

## Step 7 — Final review & upload

- **File:** `papers/v0_34/v0_34_ssrn_paper.pdf`
- **Cover letter:** Not required for SSRN Working Paper submissions.
- **Suggested citation (post-submission, fill in SSRN abstract ID):**

```
González Castro, P. U. (2026). Two-Wave Temporal Stability of an AI Brand-Recall Consistency Quantity: A Pre-Registered Longitudinal Re-Acquisition Across Five Product Categories (AIAS™ v0.34). SSRN Working Paper [ABSTRACT_ID].
```

---

## Post-submission checklist

1. **Capture SSRN abstract ID** when SSRN returns it (URL format: `https://ssrn.com/abstract={ID}`).
2. **Update memory:** add the v0.34 SSRN abstract ID entry to the recent_updates section of userMemories.
3. **Run final OSF deposit:** `python3 ~/aias/scripts/osf_upload.py ~/aias/osf/v34 v34`
4. **Cross-citation** in next phase: this v0.34 SSRN ID gets added to next phase's paper bibliography upstream-phases line.

---

**End of submission packet — v0.34 ready to upload.**
