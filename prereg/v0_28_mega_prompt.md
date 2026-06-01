# v0.28 (CV.04) — AIAS Presence Acquisition Protocol

> **Discriminant construct-validity study.** v0.28 measures AIAS Presence over a
> frozen 24-brand Tech panel and tests whether Presence is *distinct* from human
> brand-norm measures (familiarity, recognition memory) drawn from the BRAND
> database. This is the discriminant cell of a Campbell–Fiske matrix; it pairs
> with v0.25 (CV.01, Google Trends convergent, ρ = 0.74 anchor) and v0.26
> (CV.02, retail best-seller-rank discriminant).

---

## Overview

**Objective:** Acquire AIAS Presence for each of the 24 brands in the frozen Tech
panel, then test discriminant validity against the BRAND familiarity (1–7) and
recognition-sensitivity (d′) norms.

**Protocol lock:** v1.6 (SSRN 6816340). Presence is composed per v1.6.

**Panel:** read verbatim from `prereg/v0_28_panel_brands.txt` (24 brands, FROZEN
pre-acquisition). Do **not** restate the brand list here or anywhere else — the
frozen file is the single source. The matched validator values live in
`prereg/v0_28_brand_validator.csv` (`brand, familiarity_1_7, dprime`).

**Reference panel (fixed from v0.17 onward, six models):**
claude-opus-4-5, claude-sonnet-4-5, gpt-4o, gpt-4o-mini, gemini-2.5-flash,
gemini-2.5-flash-lite.

---

## Blinding (non-negotiable)

Presence is acquired **BLIND to the per-brand validator values**. The BRAND
familiarity and d′ figures are frozen before acquisition and are **not** consulted
during Phase A or Phase B. The validator is the external criterion, never an input
to the measure under test. Do not order, prompt, or weight any probe by a brand's
familiarity or d′.

---

## Phase A — Recognition (24 × 6 = 144 probes)

For each of the 24 frozen panel brands, send the locked recognition probe to each
of the six reference models (24 × 6 = 144 probes total).

Probe (exact wording):

> Is the brand **{BRAND}** commonly recognized as a technology brand? Answer yes or no.

- Per-brand **C_P** = count of "yes" responses across the six-model panel (range 0–6).
- One response per model per brand. No temporal or familiarity cueing.

---

## Phase B — Two-channel recall

Per the v1.6 two-channel recall decomposition, send six recall frames to each of
the six models. All 24 panel brands are scanned for mention in every response
under the canonical brand-mention rules (case-insensitive, accent-stripped,
possessive-aware, first-occurrence-wins).

**R_cat channel (category-canonical retrieval, q1–q3):**

- q1 (best): *What are the best technology brands? List several with descriptions.*
- q2 (expert): *What technology brands do industry experts and analysts recommend? Name several.*
- q3 (quality): *What technology brands are highest quality and most reliable? Name several with descriptions.*

**R_cult channel (cultural-footprint retrieval, q4–q6):**

- q4 (popular): *What technology brands are most talked about right now? List several.*
- q5 (cultural): *What technology brands have the biggest cultural footprint? Name several.*
- q6 (iconic): *Which technology brands have the most iconic or storied identity in popular culture? Name several.*

- Per-brand **R_cat** = mentions across (q1,q2,q3) × 6 models, max 18.
- Per-brand **R_cult** = mentions across (q4,q5,q6) × 6 models, max 18.

---

## Presence composition (Protocol v1.6)

Compose the per-brand Presence score from the Phase A / Phase B signals per the
v1.6 specification. Emit one row per panel brand to:

```
osf/v28/data/v0.28_presence.csv      # columns: brand, presence
```

`brand` must match `prereg/v0_28_panel_brands.txt` verbatim (the scorer joins
exact, then case-insensitive).

---

## Scoring (downstream, automated)

`scripts/score_v28.py` reads the frozen validator + panel and the Presence CSV,
then applies the locked decision rules:

- **H_Disc_Familiarity** (primary, gating): Spearman ρ(Presence, familiarity_1_7);
  band on **|ρ|** — `|ρ|<0.50 CONFIRMED | 0.50–0.74 PARTIAL | ≥0.74 FALSIFIED`.
- **H_Disc_Recognition** (secondary, gating): same logic vs d′.
- **H_Dissociation** (tertiary, descriptive, non-gating): within-panel
  z(Presence) − z(familiarity); amplified > +1.0, suppressed < −1.0.
- Convergent benchmark ρ = 0.74 (v0.25). Spearman primary, Pearson secondary,
  BCa 95% CI (10k, seed 280400, reported non-gating). UNDETERMINED if n < 12 or
  the CI spans all three bands.

Registered prediction: ρ 0.30–0.60 (PARTIAL modal). Tech is the adversarial,
familiarity-variance-rich substrate, so a CONFIRMED result here is a strong test.

---

## Validation checks (post-acquisition)

1. **Completeness:** 24 Presence rows, one per frozen panel brand.
2. **Join integrity:** every `brand` in `v0.28_presence.csv` matches a brand in
   `prereg/v0_28_panel_brands.txt` (exact or case-insensitive); n_joined = 24.
3. **C_P range:** all per-brand C_P in 0–6; R_cat, R_cult in 0–18.
4. **Blinding attestation:** validator values were not consulted during Phase A/B.
5. **Timestamp continuity:** acquisition within the declared window; logged in DEVIATIONS.
