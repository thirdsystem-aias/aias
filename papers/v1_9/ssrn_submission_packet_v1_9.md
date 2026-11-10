# SSRN Submission Packet — AIAS™ v1.9

**Paper:** One Score or Two? Calibrating a Presence and Consistency Composite for AI Brand Availability
**File to upload:** `papers/v1_9/v1_9_ssrn_paper.pdf`
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
One Score or Two? Calibrating a Presence and Consistency Composite for AI Brand Availability: A Pre-Registered Calibration with Blind Five-Month Confirmation (AIAS™ Methodology v1.9)
```

### Subtitle (titlepage only — SSRN has no separate subtitle field; folded into Title above)

```
A Pre-Registered Calibration with Blind Five-Month Confirmation (AIAS™ Methodology v1.9)
```

### Abstract (paste verbatim — matches paper page 2)

```
The AIAS™ measurement program now has two validated components of AI brand availability: Presence, how often a fixed panel of large language models names a brand (v1.6), and Consistency, whether the panel's models agree about it, measured by the mean-independent dispersion statistic φ (v1.8). This paper asks whether the two should be combined into one score. Stage 1, declared as calibration on two frozen waves (112 brand units, five product categories, six models), evaluated a pre-specified grid of eight composite specifications (two Consistency scores, two rules for brands with few mentions, two composition forms) against three constraints: the Consistency score must stay separable from Presence (|ρ| ≤ 0.50), the composite must carry information Presence does not (|ρ(A, P)| ≤ 0.95), and one or two mentions must not buy more credit than Presence already gives. No specification passed all three at both waves. Every composite that withheld Consistency from brands with few mentions ranked brands almost exactly as Presence did (ρ(A, P) = 0.971–0.997), and shrinking low-count scores toward the scale midpoint tied Consistency to Presence (ρ = 0.715–0.773). Under the pre-registered rule, v1.9 locks no single composite: the program's next synthesis reports Presence and Consistency as two scores. The Consistency score is locked as C_φ = 100(1 - φ/7.2), rated only for brands with at least six mentions. Stage 2 confirmed the locked specification blind, on a third wave collected after the lock, 152 days after the second: Presence retest ρ = 0.954 (n = 112); Consistency separable from Presence (ρ = 0.189, n = 54); Consistency retest ρ = 0.647 (n = 52), beyond a frame-structure null (p_frame = 0.008); and the best composite still tracked Presence (ρ = 0.969).
```

### Keywords (paste verbatim, semicolon-separated)

```
AI availability; brand availability; AIAS; pre-registration; Ehrenberg-Bass; large language models; composite measurement; consistency; test–retest reliability; scale construction
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
The author is Director, Corporate Brand Creative and Governance at Samsung Electronics America. This study re-analyses measurements taken against brand registries fixed in earlier phases (v0.19–v0.23); it performs no new brand selection, and each registry carries its source-phase conflict-of-interest handling forward unchanged. Two items of record apply. In the automotive registry, Samsung subsidiaries hold tier-2/3 component supply relationships with several registry brands — Harman International (audio systems), Samsung SDI (battery cells), and Samsung Display (infotainment) — characterized in the source phase as non-competitive, with no brand-level overlap, and imposing no operational restriction on registry composition (v0.22 Declarations; screened in v0.22 DEVIATIONS Entry 0, Part B). In the audiophile-headphones registry, AKG was substituted with Denon before the v0.19 pre-registration lock because AKG's parent, Harman International, is a Samsung subsidiary. Scoring is fully automated against the locked registries and the locked specification; the pre-registration was locked and deposited before any confirmation-wave data existed; and the author's affiliation played no role in registry construction, calibration, scoring, or the resulting verdicts. Samsung Electronics had no role in the design, conduct, analysis, or reporting of this work.
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
Materials are deposited at OSF, `ec6wh/methodology/v1_9`: the locked pre-registration with the Stage 1 calibration table, the anchor record (tag, commit and file hashes) and the deviations record. At publication the deposit adds the scorer (`score_v1_9.py`), the Stage 1 calibration output (`v1_9_calibration.json`), the Stage 2 verdicts (`v1_9_verdicts.json`) and the scoping script. The underlying waves are deposited with their source studies (OSF `ec6wh/v19`–`v23`, `v34`, `v41`).
```

---

## Step 7 — Final review & upload

- **File:** `papers/v1_9/v1_9_ssrn_paper.pdf`
- **Cover letter:** Not required for SSRN Working Paper submissions.
- **Suggested citation (post-submission, fill in SSRN abstract ID):**

```
González Castro, P. U. (2026). One Score or Two? Calibrating a Presence and Consistency Composite for AI Brand Availability: A Pre-Registered Calibration with Blind Five-Month Confirmation (AIAS™ Methodology v1.9). SSRN Working Paper [ABSTRACT_ID].
```

---

## Post-submission checklist

1. **Capture SSRN abstract ID** when SSRN returns it (URL format: `https://ssrn.com/abstract={ID}`).
2. **Update memory:** add the v1.9 SSRN abstract ID entry to the recent_updates section of userMemories.
3. **Run final OSF deposit:** `python3 ~/aias/scripts/osf_upload.py ~/aias/osf/methodology/v1_9 methodology/v1_9`
4. **Cross-citation** in next phase: this v1.9 SSRN ID gets added to next phase's paper bibliography upstream-phases line.

---

**End of submission packet — v1.9 ready to upload.**
