# SSRN Submission Packet — AIAS™ v0.33

**Paper:** Provider-Asymmetric Consistency in AI Brand Availability
**File to upload:** `papers/v0_33/v0_33_ssrn_paper.pdf`
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

### Title (paste verbatim — SSRN has one Title field; subtitle folded in)

```
Provider-Asymmetric Consistency in AI Brand Availability: A pre-registered re-analysis: modest between-provider structure in CV-CPC recall, and the limits of a Beyond-Presence gate under recognition saturation
```

### Subtitle (titlepage only — SSRN has no separate subtitle field; folded into Title above)

```
A pre-registered re-analysis: modest between-provider structure in CV-CPC recall, and the limits of a Beyond-Presence gate under recognition saturation
```

### Abstract (paste verbatim — matches paper page 2)

```
AI Availability --- the discoverability and representation of a brand in the outputs of large language models --- has been proposed as a third layer of brand availability, complementing the Mental and Physical Availability of the Ehrenberg-Bass tradition. Within the AIAS™ (AI Availability Score) program, the Consistency component is operationalized as CV-CPC, a coefficient-of-variation statistic over per-model recall; a prior methodology lock found CV-CPC strongly presence-coupled ($|\rho| = 0.77$) and did not adopt it as a validated Consistency instrument. This pre-registered re-analysis tests, across five panel-uniform substrates (112 brands; a fixed six-model panel spanning three providers --- Anthropic, OpenAI, and Google), whether the per-model recall structure underlying CV-CPC is systematically organized by provider, and whether any such organization exceeds the provider structure present in Presence (recognition). Between-provider organization of per-model recall is statistically robust but modest: the between-provider variance share exceeds its permutation null ($p < 0.001$) and survives all five leave-one-substrate-out refits, though its excess over a high small-group chance floor is small. The pre-registered Beyond-Presence gate met its criterion yet does not establish dissociation: binary recognition is saturated among recalled brands --- carrying negligible between-provider variance --- so the gate collapses onto the recall-asymmetry test rather than contrasting with Presence. This inverts the pre-registered directional prediction and reframes the gate's behavior as the study's principal methodological result: a Beyond-Presence contrast is uninformative wherever recognition is saturated. Provider rank-stability was uninformative as pre-registered, underpowered at five substrates. The study positions provider as a modest organizing factor in CV-CPC recall and bounds the conditions under which the AIAS Beyond-Presence gate can fire.
```

### Keywords (paste verbatim, semicolon-separated)

```
AI Availability; AI Availability Score (AIAS); Consistency; CV-CPC; large language models; provider asymmetry; variance decomposition; recognition saturation; pre-registered re-analysis; brand availability; Ehrenberg-Bass; pre-registration
```

### JEL codes (paste verbatim)

```
M31; L86; L15; D83; M37
```

**JEL rationale (for your reference):** M31; L86; L15; D83; M37

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
The author is Director, Corporate Brand Creative and Governance at Samsung Electronics America. This study is a secondary re-analysis of data assembled in earlier phases (v0.19--v0.23); it introduces no new brand selection or data collection. Two of the five re-analyzed substrates intersect businesses owned by Samsung Electronics: audiophile headphones, a category that includes brands of Harman International (a Samsung subsidiary), and automotive, where Samsung interests include Harman automotive systems and Samsung SDI. The brand registries were fixed under the locked protocol of the original phases, scoring is fully automated against those registries, and the analysis reported here was pre-registered (tag `v0.33-prereg-r1`) before any scoring; the author's affiliation played no role in registry construction, scoring, or the resulting verdicts. Samsung Electronics had no role in the design, conduct, analysis, or reporting of this work.
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
Pre-registration, scoring code, per-brand outputs, and verdicts are deposited at OSF (`osf.io/ec6wh`, component `v33`): the locked pre-registration (`v0.33-prereg-r1`), the scorer (`score_v33.py`), the per-brand recall/recognition vectors and $\eta^2$ values (`v33_eta2.csv`), the verdicts (`v33_provider_asymmetry_verdicts.json`) including reconciliation and computation notes, and the post-hoc recognition-source audit.
```

---

## Step 7 — Final review & upload

- **File:** `papers/v0_33/v0_33_ssrn_paper.pdf`
- **Cover letter:** Not required for SSRN Working Paper submissions.
- **Suggested citation (post-submission, fill in SSRN abstract ID):**

```
González Castro, P. U. (2026). Provider-Asymmetric Consistency in AI Brand Availability: A pre-registered re-analysis: modest between-provider structure in CV-CPC recall, and the limits of a Beyond-Presence gate under recognition saturation. SSRN Working Paper [ABSTRACT_ID].
```

---

## Post-submission checklist

1. **Capture SSRN abstract ID** when SSRN returns it (URL format: `https://ssrn.com/abstract={ID}`).
2. **Update memory:** add the v0.33 SSRN abstract ID entry to the recent_updates section of userMemories.
3. **Run final OSF deposit:** `python3 ~/aias/scripts/osf_upload.py ~/aias/osf/v33 v33`
4. **Cross-citation** in next phase: this v0.33 SSRN ID gets added to next phase's paper bibliography upstream-phases line.

---

**End of submission packet — v0.33 ready to upload.**
