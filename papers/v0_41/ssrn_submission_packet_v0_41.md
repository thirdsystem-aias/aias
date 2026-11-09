# SSRN Submission Packet — AIAS™ v0.41

**Paper:** Five-Month Stability of AI Brand Consistency and Presence
**File to upload:** `papers/v0_41/v0_41_ssrn_paper.pdf`
**Submission target:** SSRN — papers.ssrn.com → Submit a paper
**Date prepared:** November 2026

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
Five-Month Stability of AI Brand Consistency and Presence: A Pre-Registered Third Wave on a Retiring Six-Model Panel (AIAS™ v0.41)
```

### Subtitle (titlepage only — SSRN has no separate subtitle field; folded into Title above)

```
A Pre-Registered Third Wave on a Retiring Six-Model Panel (AIAS™ v0.41)
```

### Abstract (paste verbatim — matches paper page 2)

```
Brand measures derived from large language model (LLM) outputs are only useful if they hold still when nothing about the brand has changed. This study reports a pre-registered third wave of the AIAS™ measurement protocol: a verbatim re-acquisition, in November 2026, of five product-category panels (audiophile headphones, skincare, cosmetics, automotive, premium spirits; 112 brand units) first measured in May 2026 (t₁) and re-measured in June 2026 (t₂), on a fixed six-model panel whose dated versions were confirmed identical to t₂ and which begins retiring on 24 November 2026. The t₂→t₃ interval is 152 days. All 852 study calls returned, and four computational-reproducibility gates passed before any t₃ statistic was computed. The per-brand rank order of the v1.8 Consistency instrument φ held over the long horizon (H_Phi_LongHorizon CONFIRMED: pooled ρ = 0.681, n = 80), exceeding both a brand-label permutation null and a pre-registered frame-structure null that scrambles model identity within each question (p_frame = 0.0001; null 95th percentile 0.51). Recall Presence held its order in all five categories (H_Presence_LongHorizon CONFIRMED: ρ = 0.927–0.976). No decay from the three-week to the five-month horizon was detectable for either instrument (H_Horizon_Decay MARGINAL for both; D = +0.019 and +0.002, intervals spanning zero). Changes in Consistency were unrelated to changes in Presence (H_Drift_Dissociation CONFIRMED: ρ = 0.032). Of 58 brands below the recall floor at t₂, 56 remained below it. The results give the two-component AIAS 2.0 construct a long-horizon reliability base and are the last data this model panel can provide.
```

### Keywords (paste verbatim, semicolon-separated)

```
AI availability; brand availability; AIAS; pre-registration; Ehrenberg-Bass; large language models; test–retest reliability; longitudinal measurement; consistency; brand recall
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
The author is Director, Corporate Brand Creative and Governance at Samsung Electronics America. This study re-acquires measurements against brand registries fixed in earlier phases (v0.19–v0.23); it performs no new brand selection, and each registry carries its source-phase conflict-of-interest handling forward unchanged. Two items of record apply. In the automotive registry, Samsung subsidiaries hold tier-2/3 component supply relationships with several registry brands — Harman International (audio systems), Samsung SDI (battery cells), and Samsung Display (infotainment) — characterized in the source phase as non-competitive, with no brand-level overlap, and imposing no operational restriction on registry composition (v0.22 Declarations; screened in v0.22 DEVIATIONS Entry 0, Part B). In the audiophile-headphones registry, AKG was substituted with Denon before the v0.19 pre-registration lock because AKG's parent, Harman International, is a Samsung subsidiary. Acquisition, coding, and scoring are fully automated against the locked registries; the pre-registration was locked and deposited before any third-wave call; and the author's affiliation played no role in registry construction, acquisition, scoring, or the resulting verdicts. Samsung Electronics had no role in the design, conduct, analysis, or reporting of this work.
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
Materials are deposited at OSF, `ec6wh/v41`: the locked pre-registration and its anchor record (tag, commit and file hashes), the acquisition manifest with probe-set checksums, the pre-lock feasibility check, parity record and frame-structure calibration, and the deviations record. At publication the deposit adds the t₃ acquisition outputs and provenance sidecar, the scorer (`score_v41.py`) and its test suite, the verdicts (`v41_verdicts.json`), the three-wave table and the figure sources.
```

---

## Step 7 — Final review & upload

- **File:** `papers/v0_41/v0_41_ssrn_paper.pdf`
- **Cover letter:** Not required for SSRN Working Paper submissions.
- **Suggested citation (post-submission, fill in SSRN abstract ID):**

```
González Castro, P. U. (2026). Five-Month Stability of AI Brand Consistency and Presence: A Pre-Registered Third Wave on a Retiring Six-Model Panel (AIAS™ v0.41). SSRN Working Paper [ABSTRACT_ID].
```

---

## Post-submission checklist

1. **Capture SSRN abstract ID** when SSRN returns it (URL format: `https://ssrn.com/abstract={ID}`).
2. **Update memory:** add the v0.41 SSRN abstract ID entry to the recent_updates section of userMemories.
3. **Run final OSF deposit:** `python3 ~/aias/scripts/osf_upload.py ~/aias/osf/v41 v41`
4. **Cross-citation** in next phase: this v0.41 SSRN ID gets added to next phase's paper bibliography upstream-phases line.

---

**End of submission packet — v0.41 ready to upload.**
