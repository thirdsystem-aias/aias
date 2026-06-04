# SSRN Submission Packet — AIAS™ v1.7

**Paper:** Consistency without Independence
**File to upload:** `papers/v1_7/v1_7_ssrn_paper.pdf`
**Submission target:** SSRN — papers.ssrn.com → Submit a paper
**Date prepared:** [DATE NOT FOUND IN YAML]

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
Consistency without Independence
```

### Subtitle (paste verbatim)

```
A Pre-Registered Test of Coefficient-of-Variation as the Consistency Component of AIAS™
```

### Abstract (paste verbatim — matches paper page 2)

```
AI Availability extends brand-science accounts of mental and physical availability into AI-mediated discovery, and its measurement programme builds the construct one component at a time. Presence shipped as the first component; Consistency, the stability of a brand's presence across a model panel, is the candidate second. This paper pre-registers and tests the natural operationalization: the coefficient of variation of cross-model recall, mapped to a bounded consistency score. Under a locked protocol applied to three anchored substrates, the instrument fails its pre-registered independence criterion. Consistency correlates with Presence at pooled $|\rho| = 0.77$, above the 0.50 ceiling and positive in every substrate. The failure traces to a mechanical identity: at the recall counts language models return, dispersion follows the Poisson relation in which the standard deviation scales with the square root of the mean, so the coefficient of variation approximates the reciprocal of the square root of the mean and reparametrizes presence level rather than isolating a distinct construct. A secondary result documents a recognition–recall gap that leaves consistency undefined for recognized-but-unrecalled brands, concentrated among prestige labels. Per the pre-registered rule, the instrument is not adopted, and the paper specifies the mean-independence requirement any replacement must satisfy.
```

### Keywords (paste verbatim, semicolon-separated)

```
AI Availability; AIAS; brand measurement; large language models; coefficient of variation; consistency; recall; pre-registration; negative result; mental availability
```

### JEL codes (paste verbatim)

```
M31; L86; L15; D83; M37
```

**JEL rationale (for your reference):** M31 (primary); L86; L15; D83; M37

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
The author is employed by Samsung Electronics America. Samsung markets no consumer brands in the skincare or cosmetics categories examined. In automotive, Samsung does not market vehicle marques of the kind measured here, though affiliated units participate in the automotive supply chain (Harman International in connected-vehicle and audio systems; Samsung SDI in vehicle batteries); this is disclosed for completeness. The employer had no role in the study's design, execution, analysis, or decision to publish, and the research is conducted independently through Third System™.
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
Pre-registration artifacts, scoring code, the scored dataset, and figures are deposited at OSF (`osf.io/ec6wh/methodology/v1_7`). Consistency values reconcile with the pilot's recorded output to a maximum absolute difference of $2\times10^{-16}$.
```

---

## Step 7 — Final review & upload

- **File:** `papers/v1_7/v1_7_ssrn_paper.pdf`
- **Cover letter:** Not required for SSRN Working Paper submissions.
- **Suggested citation (post-submission, fill in SSRN abstract ID):**

```
González Castro, P. U. (2026). Consistency without Independence. SSRN Working Paper [ABSTRACT_ID].
```

---

## Post-submission checklist

1. **Capture SSRN abstract ID** when SSRN returns it (URL format: `https://ssrn.com/abstract={ID}`).
2. **Update memory:** add the v1.7 SSRN abstract ID entry to the recent_updates section of userMemories.
3. **Run final OSF deposit:** `python3 ~/aias/scripts/osf_upload.py ~/aias/osf/methodology/v1_7 methodology/v1_7`
4. **Cross-citation** in next phase: this v1.7 SSRN ID gets added to next phase's paper bibliography upstream-phases line.

---

**End of submission packet — v1.7 ready to upload.**
