# SSRN Submission Packet — AIAS™ v0.32

**Paper:** Version-Snapshot Stability of an AI-Presence Consistency Score
**File to upload:** `papers/v0_32/v0_32_ssrn_paper.pdf`
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
Version-Snapshot Stability of an AI-Presence Consistency Score: A Pre-Registered Two-Arm Cross-Generation Test of the v1.7 CPC Operationalization
```

### Subtitle (titlepage only — SSRN has no separate subtitle field; folded into Title above)

```
A Pre-Registered Two-Arm Cross-Generation Test of the v1.7 CPC Operationalization
```

### Abstract (paste verbatim — matches paper page 2)

```
The AIAS™ (AI Availability Score) program operationalizes AI Availability as a measurable brand-growth layer alongside Mental and Physical Availability. Its Consistency component is presently scored by CPC = 1/(1+CV), the coefficient-of-variation transform locked in methodology version v1.7. v1.7 established that this score is not a mean-independent consistency construct — it is mechanically coupled to recall level (|ρ| with Presence = 0.77) — and did not adopt it; a mean-independent redefinition was escalated to v1.8. The present study sets construct validity aside to ask a logically prior question: is the v1.7 score even version-stable? A measure that moves with the model vintage on which it is taken cannot track a brand across time, whatever its construct status. A pre-registered two-arm design measured CPC on a fixed 24-brand automotive registry under two model-version snapshots — an older vintage and the current frontier — across a six-model panel, holding probe wording, registry, and frame battery identical and varying only the dated model identifier; the contrast was made deliberately maximal across model generations. Brand-mention extraction reused the prior coder verbatim (pre-registered); a pre-scoring spot-check confirmed symmetric extraction across arms. Rank-order stability cleared the registered threshold marginally (Spearman ρ = 0.708) but proved fragile under a pre-registered leave-one-provider-out analysis (ρ ranging 0.48–0.82), with instability concentrated in the gpt-4o→gpt-5.x jump. Magnitude stability was falsified (mean |ΔCPC| = 0.077, exceeding the 0.5·SD tolerance of 0.069), though with no net directional drift — version change reshuffles which brands read as consistent without shifting the overall level. The emerging-brand instability prediction was falsified: no brand crossed the recall floor between arms. The v1.7 CPC score is therefore at best partially and provider-dependently version-stable; version-fragility compounds the recall-coupling already identified in v1.7 as grounds for the v1.8 redefinition. The contribution is a characterization of the interim instrument, not a validation of it.
```

### Keywords (paste verbatim, semicolon-separated)

```
AI availability; brand availability; AIAS; pre-registration; Ehrenberg-Bass; large language models; brand presence; measurement stability; model versioning; coefficient of variation
```

### JEL codes (paste verbatim)

```
M31; L86; M37; D83
```

**JEL rationale (for your reference):** M31 (primary); L86; M37; D83

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
The author is employed by Samsung Electronics America in a corporate brand-creative and governance role. Samsung participates in the automotive sector as a component supplier rather than as a vehicle marque — through Harman International (in-vehicle audio and infotainment), Samsung SDI (battery cells), and Samsung Display (automotive displays) — but does not compete as an automotive brand, and no brand in the v0.22 registry scored here is Samsung-owned or -affiliated; a pre-acquisition conflict-of-interest screen confirmed this. The brand-level supply relationships underlying this disclosure are itemized in the conflict-of-interest statement of v0.22 (SSRN 6829118), cited above as the registry source. The research is conducted independently through Third System and is self-funded; Samsung Electronics America had no role in the study's design, data, analysis, or reporting. A single pre-registered instrument was applied uniformly across all brands in both arms, and no brand was singled out for differential treatment.
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
Pre-registration, locked registry, two-arm acquisition data (Phase A and Phase B, both arms, provider-returned version metadata preserved), scoring code, and figures are deposited at the Open Science Framework (osf.io/ec6wh, v32 component). Methodology was locked at git tags v0.32-prereg-r1 (design) and v0.32-prereg-r2 (acquisition prompt) before any data were collected.
```

---

## Step 7 — Final review & upload

- **File:** `papers/v0_32/v0_32_ssrn_paper.pdf`
- **Cover letter:** Not required for SSRN Working Paper submissions.
- **Suggested citation (post-submission, fill in SSRN abstract ID):**

```
González Castro, P. U. (2026). Version-Snapshot Stability of an AI-Presence Consistency Score: A Pre-Registered Two-Arm Cross-Generation Test of the v1.7 CPC Operationalization. SSRN Working Paper 6898581.
```

---

## Post-submission checklist

1. **Capture SSRN abstract ID** when SSRN returns it (URL format: `https://ssrn.com/abstract={ID}`).
2. **Update memory:** add the v0.32 SSRN abstract ID entry to the recent_updates section of userMemories.
3. **Run final OSF deposit:** `python3 ~/aias/scripts/osf_upload.py ~/aias/osf/v32 v32`
4. **Cross-citation** in next phase: this v0.32 SSRN ID gets added to next phase's paper bibliography upstream-phases line.

---

**End of submission packet — v0.32 ready to upload.**
