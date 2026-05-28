# SSRN Submission Packet — AIAS™ v0.26

**Paper:** Predictive Validity of AI Presence Index Against Google Trends Search Interest on the B2B SaaS Substrate
**File to upload:** `papers/v0_26/v0_26_amazon_bsr_predictive_validity.pdf`
**Submission target:** SSRN — papers.ssrn.com → Submit a paper
**Date prepared:** May 2026

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
Predictive Validity of AI Presence Index Against Google Trends Search Interest on the B2B SaaS Substrate
```

### Subtitle (paste verbatim)

```
Construct Validity Pilot Under Protocol v1.6
```

### Abstract (paste verbatim — matches paper page 2)

```
This study tests the predictive validity of AI Presence Index scores against Google Trends search interest on a 24-brand B2B SaaS substrate. AI Presence data are inherited from v0.24 (SSRN 6838802), collected under Protocol v1.6 with a six-model reference panel. Google Trends data were acquired via SerpAPI over a contemporaneous seven-day window (United States geography) using cross-bundle normalization with Salesforce as the pivot brand. Six pre-registered hypotheses test convergent validity (composite, Recognition-only, and Recall-only correlations with Trends), discriminant anchoring (Phantom brands at floor), cell-level monotonicity, and discriminant validity of Identity Load. The primary result is a Spearman rank correlation of 0.74 (p < 0.001) between the AIAS Presence composite and Google Trends search interest, confirming convergent validity. Recognition (C_P) was constant at 6/6 across all 24 brands (ceiling effect), rendering the Recognition-only hypothesis untestable. Category Recall alone correlated at 0.67 (p < 0.001). Phantom brands anchored the floor on both measures. Identity Load was confirmed as uncorrelated with search interest, supporting its status as a discriminant construct. These results establish that AIAS Presence scores, as operationalized under Protocol v1.6, correspond to real-world brand salience as proxied by consumer search behavior.
```

### Keywords (paste verbatim, semicolon-separated)

```
AI Availability; brand measurement; construct validity; Google Trends; large language models; AIAS; brand salience; B2B SaaS
```

### JEL codes (paste verbatim)

```
M31; L86; L15; D83; M37
```

**JEL rationale (for your reference):** M31 (primary); L86, L15, D83, M37 (secondary).

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

(Same classification set as v0.16–v0.24 papers for consistency.)

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
The author is Director of Corporate Brand Creative and Governance at Samsung Electronics America. The v0.26 study, like all AIAS programme publications, is independent research developed outside the scope of that employment. None of the brands in the v0.26 registry are Samsung properties.
```

### Funder (paste verbatim)

```
Self-funded.
```

### Ethics statement (paste verbatim)

```
Not applicable. All data derived from public APIs (Google Trends via SerpAPI) and large language model prompts; no human subjects, no personal data.
```

### Data and code availability (paste verbatim)

```
All inputs (v0.24 AI Presence scores), Google Trends raw responses, topic-ID suggestion logs, pre-acquisition validation outputs, resolved topic-ID registry, scoring outputs, build scripts, chart source code, and this paper's source are deposited at OSF project ec6wh, /v26/. Pre-registration is locked at git tag v0.26-prereg-r1 (commit 6ff9403). The methodology version that governs scoring is Protocol v1.6 (González Castro 2026a).
```

---

## Step 7 — Final review & upload

- **File:** `papers/v0_26/v0_26_amazon_bsr_predictive_validity.pdf`
- **Cover letter:** Not required for SSRN Working Paper submissions.
- **Suggested citation (post-submission, fill in SSRN abstract ID):**

```
González Castro, P. U. (2026). Predictive Validity of AI Presence Index Against Google Trends Search Interest on the B2B SaaS Substrate. SSRN Working Paper [ABSTRACT_ID].
```

---

## Post-submission checklist

1. **Capture SSRN abstract ID** when SSRN returns it (URL format: `https://ssrn.com/abstract={ID}`).
2. **Update CLAUDE.md:** add the v0.26 SSRN abstract ID to the Phase SSRN ID registry.
3. **Run final OSF deposit:** `python3 ~/aias/scripts/osf_upload.py ~/aias/osf/v26 v26`
4. **Cross-citation** in next phase: this v0.26 SSRN ID gets added to next phase's paper bibliography.

---

**End of submission packet — v0.26 ready to upload.**
