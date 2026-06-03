# SSRN Submission Packet — AIAS™ v0.30

**Paper:** Recognition Saturates, Consistency Doesn't
**File to upload:** `papers/v0_30/v0_30_ssrn_paper.pdf`
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

### Title (paste verbatim)

```
Recognition Saturates, Consistency Doesn't
```

### Subtitle (paste verbatim)

```
An Instrument-Specification Pilot of the AIAS™ Consistency Component (CPC) across Skincare, Cosmetics, and Automotive
```

### Abstract (paste verbatim — matches paper page 2)

```
The AIAS (AI Availability Score) program measures a brand's availability inside large language models. Its first component, Presence, captures whether a brand surfaces; its second, Consistency (CPC), captures how stably it surfaces across the model panel. This instrument-specification pilot defines Consistency as the cross-model dispersion of a brand's recall signal and tests it on three anchored substrates — skincare, cosmetics, and automotive — each measured against an identical six-model panel, reusing deposited data under a pre-registered analysis plan. Recall-based Consistency is defined for a majority of brands precisely where recognition has saturated and can no longer discriminate (confirmed), and corrected Consistency differs significantly across categories with the apparatus held fixed (confirmed). The raw measure is mechanically confounded with brand prominence, and a maximum-normalized (Bhatia–Davis) correction removes that confound — but this was testable in only one substrate, because the apparatus-homogeneous categories that sharpen the cross-category comparison are the mature categories in which recognition, the prominence variable, saturates. The confound hypotheses are therefore undetermined rather than confirmed. That tension — between the apparatus homogeneity a clean category comparison demands and the prominence variance a confound test requires — is the pilot's principal contribution, and it specifies the design the construct's validation must adopt.
```

### Keywords (paste verbatim, semicolon-separated)

```
AI Availability; AI Availability Score; large language models; brand consistency; construct validity; coefficient of variation; brand measurement; generative AI search
```

### JEL codes (paste verbatim)

```
M31; M37; L15; L86; D83
```

**JEL rationale (for your reference):** M31 (primary); M37, L15, L86, D83

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
The author is employed by Samsung Electronics America; the research entity Third System is independent. The three substrates analysed (skincare, cosmetics, automotive) contain no Samsung-owned brands, and the employer had no role in the design, analysis, or reporting.
```

### Funder (paste verbatim)

```
Self-funded.
```

### Ethics statement (paste verbatim)

```
Not applicable. The research uses public LLM APIs and standard prompt batteries; no human subjects, no personal data, no protected populations.
```

### Data and code availability (paste verbatim)

```
Pre-registration, reused measurement data, scoring code, and verdicts are deposited at OSF (osf.io/ec6wh, v30), under tags v0.30-prereg-r1 / r2 and v0.30-results-r2.
```

---

## Step 7 — Final review & upload

- **File:** `papers/v0_30/v0_30_ssrn_paper.pdf`
- **Cover letter:** Not required for SSRN Working Paper submissions.
- **Suggested citation (post-submission, fill in SSRN abstract ID):**

```
González Castro, P. U. (2026). Recognition Saturates, Consistency Doesn't. SSRN Working Paper [ABSTRACT_ID].
```

---

## Post-submission checklist

1. **Capture SSRN abstract ID** when SSRN returns it (URL format: `https://ssrn.com/abstract={ID}`).
2. **Update memory:** add the v0.30 SSRN abstract ID entry to the recent_updates section of userMemories.
3. **Run final OSF deposit:** `python3 ~/aias/scripts/osf_upload.py ~/aias/osf/v30 v30`
4. **Cross-citation** in next phase: this v0.30 SSRN ID gets added to next phase's paper bibliography upstream-phases line.

---

**End of submission packet — v0.30 ready to upload.**
