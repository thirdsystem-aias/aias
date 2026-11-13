# AIAS™ 2.0 Synthesis Paper — Working Outline (r1)

**Status:** r1, drafted Nov 9, 2026 by the autopilot (decisions D1–D10 below are Claude's; Pablo can overrule any of them). Committed on branch `aias-2.0` (from `v1.9-prereg-r1`, commit `70e19ac`) and tagged locally `aias-2-0-outline-locked`. **The outline is written before any t₃ answer exists.** Its anchor (tag pushed + this file deposited at `osf.io/ec6wh/aias_2_0/prereg/`) is a gate, queued for Pablo's go together with the `v0.41-prereg-r1` / `v1.9-prereg-r1` push, so that the synthesis's claim structure and its outcome-contingent wording (§5) are fixed blind to t₃.
**Predecessors:** AIAS™ 1.0 synthesis (SSRN 6817841, Presence) · v0.29 Presence construct-validity baseline (SSRN 6870778) · the Consistency arc v0.30–v0.37 · methodology v1.7 (SSRN 6878818), v1.8 (SSRN 6963359), v1.9 (locked r1, Nov 9, 2026; OSF `methodology/v1_9/prereg/`).
**Joint corpus:** the five panel-uniform omnibus substrates v0.19–v0.23 (112 brand units) on the six-model legacy panel, at t₁ (May 2026), t₂ (Jun 10, 2026, v0.34) and t₃ (v0.41; locked date Nov 9, 2026).
**Locks consumed (not re-opened):** Presence v1.6 (P = the v0.25 `presence_composite`); Consistency v1.8 (φ); scoring rule v1.9 (C* = C_phi rated at ≥ 6 total mentions; no composite).
**Waits on:** v0.41 t₃ acquisition and scoring (`osf/v41/v41_verdicts.json`) and v1.9 Stage 2 (`osf/methodology/v1_9/v1_9_verdicts.json`). Nothing in this outline reads t₃.
**Resume context for later sessions:** this file + `~/aias/Try system book/` (kickoff prompt, roadmap, CLAUDE.md, STATUS.md). Source paths below are on branch `aias-2.0` unless stated.

---

## 1. Positioning

### What it IS

- The program's **second whole-version synthesis**: AI Availability measured on **two components**, Presence and Consistency, reported **side by side as a two-score profile** (v1.9 Stage 1 outcome, confirmed by Pablo on Nov 9, 2026).
- A **consolidation of locked records**. Every statistic it reports is already in a locked verdict file (v0.29, v0.30–v0.37, v1.7, v1.8, v1.9, v0.41). The synthesis adds framing, cross-phase tables and figures, not new tests.
- The place where the Consistency arc is told as one argument: an instrument that failed (CV-CPC, v1.7), the instrument that replaced it (φ, v1.8), the scoring rule that makes it usable (v1.9), the evidence that it is a separate component (v1.8, v1.9, v0.37), and its stability over a short and a long horizon (v0.34, v1.8, v1.9, v0.41).
- A **two-deliverable event** (D6): SSRN paper (academic register) + Third System™ brand-format report (managerial register).

### What it is NOT

- **Not a new acquisition.** t₃ belongs to v0.41 and its lock; the synthesis only consumes v0.41's and v1.9's locked outputs.
- **Not a composite index.** v1.9 Stage 1 found no candidate composite that carries information Presence does not (K2) without tying Consistency to Presence (K1/K3). AIAS 2.0 does not publish a single 0–100 score. A composite is reconsidered only at v1.11 (two → three components, after Ranking), under a new calibration lock.
- **Not a re-scoring of the CV-CPC era.** v0.30–v0.36 measured Consistency with CV-CPC, which v1.7 falsified as an independent component (coupled to Presence). Those results are reported as **instrument lineage**, not as AIAS 2.0 evidence, except where a later locked record re-scored them under φ (v1.8's three framings).
- **Not a validity claim against behaviour.** Neither component is tested against purchase, consideration or search outcomes here (Phase S). Presence's construct-validity baseline (v0.29) is cited, not extended to Consistency.
- **Not panel-general.** Every AIAS 2.0 number binds to the retiring six-model legacy panel (D9). The current arm used since v0.38 is out of scope.
- **Not a model-comparison paper.** Per-model or per-provider rankings are not claims of the synthesis.

### Venue (D1)

SSRN preprint + Third System report first (program convention). Journal routing (roadmap JOUR.02: JAR / Marketing Letters / IJRM) is decided at the paper lock, once the Stage 2 verdicts are known.

---

## 2. Working title (D2)

> *Presence and Consistency: A Two-Component Measurement of AI Availability (AIAS™ 2.0)*

Names the two components and the version, and stays neutral on every t₃ outcome (it holds under classes A, B, C and U of §5).

**Alternatives considered:**
- *Beyond Presence: Cross-Model Consistency as a Second, Separable Component of AI Availability* — claims separability in the title; separability is re-tested at t₃ (H_Dissociation_t3), so the title would pre-judge a confirmatory test.
- *Two Stable Components of AI Availability* — pre-judges H_Consistency_Reliability and H_Presence_Score_Reliability. Rejected for the same reason.
- Reuse of *AI Availability as a Third Measurable Layer…* (AIAS 1.0) — that title is the 1.0 claim; 2.0 adds a component, it does not restate the layer claim.

---

## 3. Evidence base

### 3.1 Presence, carried forward by citation (not re-scored)

- **AIAS 1.0** (SSRN 6817841): Presence measurable under locked v1.6 across the five-substrate-family anchor base; claim layers L1–L7.
- **v0.29** (SSRN 6870778): H_CV_Baseline CONFIRMED — convergent ρ = 0.7411 (Presence × Google Trends, p = 3.4e-05), discriminant ρ = −0.0002 (Presence × Amazon BSR, p = 0.998), Campbell–Fiske gap 0.7409. Source: `osf/v29/data/v29_verdicts.json`.
- **The score AIAS 2.0 reports:** P = 100 · (C_P/6 + R_cat/18 + R_cult/18)/3, the v0.25 `presence_composite`, equal to 100 · (C_P/6 + 2π̂)/3 for all five omnibus substrates (v1.9 pre-registration, PRESENCE).

### 3.2 Consistency: instrument lineage (CV-CPC era, reported as lineage)

| Phase | SSRN | Locked result | Role in AIAS 2.0 |
|---|---|---|---|
| v0.30 CPC.01 pilot | 6875319 (declined; cite OSF/site copy) | F1 Computable CONFIRM; F2 LevelConfound and F3 LevelCorrected UNDETERMINED; F4 SubstrateVariation CONFIRM | first operationalization; the level-confound question that v1.7 later answered |
| v0.31 cross-category | 6880959 (withdrawn; cite OSF copy) | Computable CONFIRM; CrossCategory CONFIRM (Kruskal–Wallis H = 21.51, p = 0.00025) | lineage only |
| v0.32 version-snapshot | 6898581 | PRIMARY CONFIRMED (ρ = 0.708); SECONDARY and TERTIARY FALSIFIED; leave-one-provider-out ρ 0.512 / 0.822 / 0.482 (drop Anthropic / OpenAI / Google) | lineage; provider dependence noted |
| v0.33 provider asymmetry | 6909019 | H_Provider_Asymmetry CONFIRMED (mean η² = 0.360, MC p = 0.0007); H_Provider_Beyond_Presence criterion met (δη² = 0.505, MC p = 0.0001) but saturation-collapsed per the paper; H_Provider_Ordinal UNINFORMATIVE | lineage; why "beyond Presence" needs a mean-independent instrument |
| v0.34 t₁→t₂ | 6915458 | H_CPC_Temporal_Stability CONFIRMED (ρ 0.78 / 0.89 / 0.96 / 0.76 for v0.20–v0.23; v0.19 0.42); H_CPC_Drift_Beyond_Presence MARGINAL (recognition saturated in 4/5); H_Presence_Temporal_Stability MARGINAL | short-horizon lineage; the mandate for v1.8 |
| v0.35 phantom × CPC | 6921758 (declined) | H_Phantom_CPC_Signature CONFIRMED; H_Phantom_Beyond_Presence UNDETERMINED (control flip); H_Phantom_Cross_Substrate UNINFORMATIVE | lineage |
| v0.36 regime emergence | 6927958 (declined) | Cell D (unstructured); all four structure hypotheses NOT SUPPORTED | Consistency has no typology (Claim 7) |
| v1.7 CV-CPC lock | 6878818 | H_CPC_Dissociates FALSIFIED (pooled composite ρ = 0.766, n = 38); H_CPC_Defined FALSIFIED (defined rate 0.567) | **the turning point:** CV-CPC is not independent of Presence; not adopted |

Sources: `osf/v30/v30_cpc_verdicts.json`, `osf/v31/v31_cpc_verdicts.json`, `osf/v32/v32_verdicts.json`, `osf/v33/v33_provider_asymmetry_verdicts.json`, `osf/v34/v34_verdicts.json`, `osf/v35/v35_verdicts.json`, `osf/v36/v36_verdicts.json` (branch v0.36), `osf/methodology/v1_7/v1_7_cpc_verdicts.json`. Declined and withdrawn papers are cited by title with the thirdsystem.ai or OSF copy, not an ssrn.com link (kickoff registry, Nov 8–9, 2026).

### 3.3 Consistency: the locked instrument and scoring rule (AIAS 2.0 evidence)

- **v1.8 φ** (SSRN 6963359): between-model dispersion of per-model recall counts on a quasi-binomial basis. H_CV_Reproduces CONFIRMED (CV-CPC's coupling reproduced: |ρ(CV-CPC, μ)| = 0.682, n = 55); **H_MeanIndependent CONFIRMED** (pooled |ρ(φ, μ)| = 0.091, n = 197); H_LowRecallDefined CONFIRMED (φ defined for 84/84 surfacing brands, against 55 for CV-CPC); H_PositionalDissociation CONFIRMED (ρ(φ, J) = −0.403, n = 74); H_GradedRecognition FORWARD-SPEC; H_PhantomSignature NULL (exploratory). Two-wave reproducibility ρ(φ_t₁, φ_t₂) = 0.645 (n = 83). Source: `osf/v41/registries/v1_8_verdicts.json` (frozen copy of the v1.8 record).
- **v0.37** (SSRN pending): H_IL_Consistency FALSIFIED → clean null, ρ = −0.008, p_perm = 0.955, n = 53; Presence's Identity-Load moderator does not carry over to Consistency. Source: `osf/v37/v37_verdicts.json`.
- **v1.9 Stage 1** (calibration on frozen t₁/t₂, declared, not a test; full table in `osf/methodology/v1_9/v1_9_calibration.json`):
  - Scale: C_phi = 100 · (1 − φ/φ_max), φ_max = 7.2 for M = F = 6. Never-named brands are not rated.
  - **Selected Consistency score C\* = C_phi, rated only at ≥ 6 total mentions.** Separable from Presence: ρ(C\*, P) = 0.073 (t₁, n = 55) and 0.082 (t₂, n = 54). Retest t₁→t₂ 0.736 (n = 53), against 0.533 for unfloored C_phi (within-substrate ranks, v1.9 pre-look).
  - Share of the 112 units **not rated**: 0.509 (t₁) and 0.518 (t₂).
  - **No composite:** FLOOR composites rank brands as Presence does (ρ(A, P) 0.971–0.997, K2 fails); SHRINK ties Consistency to Presence (C_phi + SHRINK: ρ(C\*, P) 0.715 / 0.773, K1 fails; ΔA 10.3–14.2 at t₁ and 10.2–15.0 at t₂ against ΔP + 5 = 7.3 / 7.7, K3 fails). C_phiJ + FLOOR retests higher (0.868) but sits on the K1 line (0.456 / 0.530).
  - Presence retest t₁→t₂: 0.970 (n = 112).
  - Why a floor (pre-look): a naive (P + C_phi)/2 would score brands named once 58.0 on average (n = 9) against 30.4 for brands never named (n = 28).
  - Frame structure: within-frame model shuffles leave ρ(φ_t₂, φ_shuffled) at mean 0.39 (95th percentile 0.55) (v0.41 SCORER_NOTES S2; `osf/v41/prereg/frame_structure_floor_v0_41.json`).

### 3.4 The long horizon (pending; locked tests, governing verdicts for §5)

| Record | Hypothesis | Rule (as locked) |
|---|---|---|
| v1.9 Stage 2 | H_Presence_Score_Reliability (PRIMARY) | ρ(P_t₂, P_t₃) ≥ 0.80 and p_perm < .05 → CONFIRMED; ρ < 0.60 or p ≥ .05 → FALSIFIED |
| v1.9 Stage 2 | H_Dissociation_t3 (PRIMARY) | \|ρ(C\*_t₃, P_t₃)\| ≤ 0.30 → CONFIRMED; ≥ 0.50 → FALSIFIED |
| v1.9 Stage 2 | H_Consistency_Reliability (PRIMARY) | ρ(C\*_t₂, C\*_t₃) ≥ 0.50 and p_frame < .05 → CONFIRMED; ρ < 0.30 or p_frame ≥ .05 → FALSIFIED |
| v1.9 Stage 2 | H_NoComposite_t3 (descriptive) | ρ(A, P) at t₃ for C_phi + FLOOR + ADD, against the K2 line 0.95 |
| v0.41 | H_Phi_LongHorizon (PRIMARY) | ρ ≥ 0.50 and p_perm < .05 and p_frame < .05 → CONFIRMED; ρ < 0.30 or p_perm ≥ .05 → FALSIFIED |
| v0.41 | H_Presence_LongHorizon (PRIMARY) | ρ(π̂_t₂, π̂_t₃) ≥ 0.70 in ≥ 4/5 substrates → CONFIRMED; < 0.50 in ≥ 3/5 → FALSIFIED |
| v0.41 | H_Horizon_Decay (SECONDARY) | bootstrap CI of ρ(t₁,t₂) − ρ(t₁,t₃) above 0 → CONFIRMED |
| v0.41 | H_Drift_Dissociation (SECONDARY) | \|ρ(Δφ, Δπ)\| ≤ 0.30 → CONFIRMED; ≥ 0.50 with p < .05 → FALSIFIED |
| v0.41 | H_Phantom_LongPersistence (descriptive), MC_ProbeParity, MC_Snapshot, MC_Completeness, MC_Truncation | as locked |

Rules copied from `osf/methodology/v1_9/prereg/v1_9_two_component_composite_content.py` and `osf/v41/prereg/v0_41_longitudinal_t3_omnibus_content.py`; those files govern if this table and they ever disagree.

---

## 4. The construct claim (paper §5 spine)

Each claim names its governing verdict. "Governing" means the paper's wording for that claim follows that verdict under §5; supporting records are cited alongside.

### Claim 1 — AI Availability is measured on two components, reported as a profile
- **Statement:** AIAS 2.0 reports two scores per brand: Presence P (0–100, every brand) and Consistency C\* (0–100, brands with ≥ 6 total mentions). They are not combined.
- **Governing:** v1.9 Stage 1 (locked outcome: no composite).
- **Boundary:** L1 of AIAS 1.0 (AI Availability as a measurable third layer) is carried by citation, not re-argued.

### Claim 2 — Consistency is the agreement among AI models on whether a brand is named
- **Statement:** Consistency is how evenly the panel's models retrieve a brand across the same frames, measured by φ and scaled as C_phi; 100 = identical counts across models, 0 = maximal polarization (v1.9 scale).
- **Governing:** v1.8 instrument definition; v1.9 scale.
- **Boundary:** a property of the panel's answers about a brand, measured per wave. Whether it is a stable brand trait is Claim 5.

### Claim 3 — Consistency is separable from Presence
- **Statement:** a brand's Consistency carries information its Presence does not.
- **Governing:** H_Dissociation_t3 (v1.9 Stage 2).
- **Supporting:** v1.8 H_MeanIndependent (0.091); v1.9 K1 at t₁/t₂ (0.073 / 0.082; calibration, not confirmatory); v1.7 as the contrast case (CV-CPC 0.766); v0.41 H_Drift_Dissociation (change-level).
- **Boundary:** separability is established on a mean-independent instrument only; CV-CPC-era claims of "beyond Presence" are not used.

### Claim 4 — Consistency is rated only where there is evidence to rate
- **Statement:** C\* is not rated for brands with fewer than 6 total mentions, and never for brands no model names ("consistency of absence is not consistency of availability"). About half the 112 omnibus units were not rated at t₁ and t₂ (0.509 / 0.518).
- **Governing:** v1.9 Stage 1 selection (FLOOR) and pre-look (the 58.0 vs 30.4 windfall a naive average would create).
- **Boundary:** AIAS 2.0's Consistency claims are about recalled brands. The share not rated at t₃ is reported, not interpreted as a finding about the brands.

### Claim 5 — Reliability over time
- **Statement (wording set by §5):** the order of brands on each component holds over a short horizon (≈ 3 weeks: P 0.970; C\* 0.736; φ 0.645 pooled) and, per the Stage 2 verdicts, over a long horizon (≈ 5 months).
- **Governing:** H_Consistency_Reliability and H_Presence_Score_Reliability (v1.9 Stage 2) for the scores AIAS 2.0 reports.
- **Supporting:** H_Phi_LongHorizon, H_Presence_LongHorizon, H_Horizon_Decay (v0.41); v0.34 and v1.8 (short horizon).
- **Boundary:** reliability is reported against the frame-structure null (mean 0.39, 95th percentile 0.55), because part of φ's stability comes from the frames, not the models.

### Claim 6 — No single composite
- **Statement:** on this panel and these substrates, no 0–100 combination of P and C\* both adds information to P and keeps Consistency separate; the profile is the measurement.
- **Governing:** v1.9 Stage 1 (8-row table). **Supporting:** H_NoComposite_t3 (descriptive).
- **Boundary:** a descriptive t₃ value below 0.95 does not revive a composite (§5, rule R6).

### Claim 7 — What Consistency is not (component boundaries)
- **Statement:** Consistency does not inherit Presence's structure: no Identity-Load moderation (v0.37 clean null, ρ = −0.008, n = 53); no phantom signature under φ (v1.8 NULL, exploratory); no regime typology (v0.36 Cell D, CV-CPC era, reported as such). Provider asymmetry was measured only under CV-CPC (v0.33) and is not claimed for φ.
- **Governing:** v0.37 (confirmatory null); the others are lineage or exploratory and labeled so.
- **Boundary:** "no moderator found" is a statement about Identity Load as operationalized by cell design (AIAS 1.0, L5 boundary), not about consumer identity.

### Claim 8 — The synthesis position
- **Statement:** AIAS 2.0 = Presence + Consistency as a two-score profile, measured on one retiring panel. Ranking (RS → AIAS 3.0), Sentiment, Coverage and Grounding remain on the roadmap; the next composite question is v1.11 (two → three components).
- **Boundary:** the 0–100 scales are measurement conventions, not probabilities; the φ scale's maximum depends on the panel size M, so C\* must be recalibrated on the new reference panel before any post-legacy comparison (D9).

---

## 5. Outcome-contingent wording (locked before t₃)

The headline class is set by the governing verdicts. Supporting verdicts are always reported in full, including where they disagree with the governing one.

| Class | Condition (v1.9 Stage 2) | Headline wording | What changes in the paper |
|---|---|---|---|
| **A** | H_Dissociation_t3 CONFIRMED or MARGINAL, and H_Consistency_Reliability CONFIRMED | "AI Availability measured on two separable components, each holding its brand order over five months on one panel." | full claim set; MARGINAL separability is reported as "separable, with moderate coupling at t₃" and the coupling value is printed |
| **B** | Dissociation CONFIRMED or MARGINAL, and Reliability MARGINAL | "…two separable components; Consistency carries brand-level signal over five months, less reliably than Presence." | C\* is published with its retest coefficient; the report advises reading C\* per wave, not as a trend |
| **C** | Dissociation CONFIRMED or MARGINAL, and Reliability FALSIFIED | "…two separable components; Consistency is a property of each wave's answers, not yet a stable brand trait." | Claim 5 is rewritten as a negative result; C\* stays in the profile labeled "per-wave"; Pablo is told before drafting continues |
| **D** | Dissociation FALSIFIED | none — **drafting pauses** | the two-component claim is not supported at t₃; Claude writes a one-page options memo (e.g. hold AIAS 2.0 for the new panel, or publish a qualified synthesis); a change of direction, so Pablo decides |
| **U** | v0.41 halts, or Stage 2 UNDETERMINED (n floors) | "…two components, separable and reliable over three weeks; the five-month test is undetermined." | long-horizon claims reported as UNDETERMINED (data gap); the new panel's first two-wave study becomes the long-horizon test |

**Rules that apply in every class**

- **R1** H_Presence_Score_Reliability below CONFIRMED qualifies only the Presence stability sentence; AIAS 1.0's measurability claim and v0.29's validity baseline are cited unchanged.
- **R2** If H_Phi_LongHorizon (raw φ) and H_Consistency_Reliability (C\*) disagree, both are reported; the headline follows C\*, the score AIAS 2.0 publishes.
- **R3** H_Drift_Dissociation FALSIFIED while H_Dissociation_t3 holds → the paper states both: levels separate, changes move together.
- **R4** H_Horizon_Decay is reported as measured; it never changes the class.
- **R5** MC_Snapshot failure for a model → v0.41's locked sensitivity (without that model) is printed beside the primary; the class is set by the primary.
- **R6** H_NoComposite_t3 is descriptive. A t₃ value below 0.95 is reported and does not revive a composite (the selection rule is locked at Stage 1; any composite needs a new calibration lock, v1.11).
- **R7** No t₃-based statistic beyond those locked in v0.41 and v1.9 enters a confirmatory sentence. Anything else is labeled exploratory and listed in the data lock before it is computed.

---

## 6. Paper structure (SSRN version, ~7K words; D7)

**Abstract** (≤ 250 words): two components, how each is measured, the separability and reliability verdicts (wording per §5), no composite, the rating floor, panel binding; disclaims behavioural validity.

**§1 Introduction.** Why a second component: an AI intermediary can name a brand often but unevenly across models; Presence alone cannot see that. Roadmap of the paper.

**§2 Theoretical positioning (~700 words).** Ehrenberg-Bass Mental and Physical Availability; the Tri-System framework (cite MSI Working Paper 26-132 wherever invoked; Shaw & Nave, SSRN 6097646, if "System 3" or "cognitive surrender" appears); measurement-theory anchors for Consistency: agreement among raters (models as raters) and overdispersion (quasi-binomial dispersion). Candidate references, bibliographic details to verify at drafting: Sharp (2010); Romaniuk & Sharp (edition/year open, program-wide item); Fleiss (1971); McCullagh & Nelder (1989); Shrout & Fleiss (1979); Campbell & Fiske (1959); Nosek et al. (2018).

**§3 Methodology (consolidated).** Panel (six-model legacy panel, temperature 0, 2,048-token cap); the five omnibus substrates and three waves; P; φ, C_phi, the floor; the locked verdict rules imported from v1.9 and v0.41 (§3.4 table); pre-registration chain and anchors (tags and OSF deposits, with dates).

**§4 Evidence.** 4.1 From CV-CPC to φ (lineage table, v1.7 turning point) · 4.2 Separability (Claim 3) · 4.3 The rating floor (Claim 4) · 4.4 Reliability, short and long horizon (Claim 5) · 4.5 Why no composite (Claim 6) · 4.6 What Consistency is not (Claim 7).

**§5 The AIAS™ 2.0 construct.** Claims 1–8; the spine is Claim 1 with Claim 8.

**§6 Discussion.** For marketing science: a second, separable component of AI Availability. For practice: being named often and being named consistently are different problems. Limitations: one retiring panel; five substrates and 112 units (16–24 brands per substrate); about half the brands not rated for Consistency; English-language prompts; recognition binary by probe design (v1.8 H_GradedRecognition is forward-spec); no behavioural criterion.

**§7 Future research.** Recalibrate C\* on the new reference panel; Ranking (v0.42 onward); a φ-based Consistency typology test; predictive validity of the profile (Phase S).

**References.** Methodology chain v1.2–v1.8 (+ v1.9 record); AIAS 1.0; v0.29; v0.30–v0.37 and v0.41 (declined or withdrawn ones by title with OSF or site copy); foundational SSRN 6659000; MSI WP 26-132. Titles verified verbatim against the SSRN author dashboard at drafting, never copied from CLAUDE.md.

**Declarations.** Samsung COI in §COI only (carry-forward: v0.22 tier-2/3 Harman / Samsung SDI / Samsung Display; v0.19 AKG → Denon, as in v0.41 DEVIATIONS Entry 0). Funder: self-funded. Ethics: not applicable. Data and code: OSF `ec6wh/aias_2_0/`. Outline lock `aias-2-0-outline-locked`. Trademark notice.

---

## 7. Decisions (D1–D10, decided by Claude on Nov 9, 2026; overrule anytime)

- **D1 Venue:** SSRN + report now; journal routing at the paper lock. *Reason:* the tier a two-component claim can carry depends on the long-horizon verdicts, which do not exist yet.
- **D2 Title:** neutral (§2). *Reason:* a title must hold under every §5 class.
- **D3 Scope:** joint analyses on the five omnibus substrates × t₁/t₂/t₃ only; Presence carried by citation. *Reason:* the only corpus where both components are measured on the same units, panel and waves.
- **D4 Boundary:** consume locked records exactly; CV-CPC era as lineage; no new confirmatory statistic (R7). *Reason:* same discipline as AIAS 1.0 D4; a post-hoc re-scoring would need its own lock.
- **D5 Positioning:** two-score profile, no composite. *Reason:* v1.9 Stage 1 outcome, confirmed by Pablo (Nov 9, 12:15 am CT).
- **D6 Report:** yes, managerial register (P1–P5), after the SSRN ID, as in AIAS 1.0. *Reason:* the first time AIAS reports a profile rather than one number is a managerial event in its own right.
- **D7 Length:** ~7K words (SSRN version). *Reason:* one new component; the lineage table carries the history.
- **D8 Outcome-contingent wording:** §5, locked now. *Reason:* fixes the framing before t₃ exists, the synthesis-level equivalent of a pre-registered verdict rule.
- **D9 Panel binding:** legacy panel only; the current arm (v0.38–v0.40) is out of scope. *Reason:* φ_max depends on M and C\* was calibrated on this panel; mixing panels needs a new calibration.
- **D10 Lock and anchor:** commit + local tag now; push + OSF deposit queued with the v0.41/v1.9 anchor, before the first t₃ call. *Reason:* the outline's integrity value is that it predates t₃ on an external record.

**Recommendation to the v1.9 owner (not decided here):** give v1.9 its own short methodology paper after Stage 2 (every v1.N lock so far has one), so AIAS 2.0 cites a locked methodology record rather than reporting the calibration itself.

---

## 8. Infrastructure

### Code
- **`scripts/aias_2_0_synthesis_data.py`** → **`osf/aias_2_0/aias_2_0_synthesis_data.json`**: the single source for §4 prose and every figure. Reads only locked files: the eight lineage verdict files (§3.2), `osf/v41/registries/v1_8_verdicts.json`, `osf/v37/v37_verdicts.json`, `osf/v29/data/v29_verdicts.json`, `osf/methodology/v1_9/v1_9_calibration.json`, and, once they exist, `osf/v41/v41_verdicts.json` and `osf/methodology/v1_9/v1_9_verdicts.json` plus the per-brand P and C\* tables those scorers write. Refuses the Stage-2 sections unless both verdict files exist and both prereg tags are on origin (checked with `git ls-remote`, not the local tag). Records the SHA-256 of every input.
- **Declared descriptive summaries (R7):** per-substrate share of units rated for C\* per wave; P × C\* joint distribution per wave; the class (§5) computed mechanically from the governing verdicts.
- **`scripts/build_charts_aias_2_0.py`** → `reports/figs/aias_2_0/` (fork `scripts/build_charts_aias_1_0.py`; Akkurat Pro; brand tokens).
- **`papers/aias_2_0/build_paper_aias_2_0.py`** (copy of `papers/aias_1_0/build_paper_aias_1_0.py`, version strings only) + `papers/aias_2_0/aias_2_0_synthesis_paper_draft.md`.
- **Report:** `reports/build_report_aias_2_0.py` + `reports/aias_2_0_content.py` (fork the AIAS 1.0 pair).

### Locks and OSF
- Tags: `aias-2-0-outline-locked` (this file) → `aias-2-0-data-locked` → `aias-2-0-charts-locked` → `aias-2-0-paper-locked` → `aias-2-0-report-locked`. Tags are additive; a revised outline is `-r2`, never a moved tag.
- OSF: `osf.io/ec6wh/aias_2_0/` with `prereg/` (this outline), `scoring/` (synthesis data JSON + input hashes), `figures/`, `paper/`, `report/`.

---

## 9. Figures

**SSRN paper (six):**
1. **Two measured components in the six-component roadmap** (conceptual; Presence 1.0, Consistency 2.0, four to come).
2. **Coupling with Presence, by instrument:** CV-CPC (v1.7 0.766; v1.8 0.682) vs φ (0.091) vs C\* (0.073 / 0.082) vs C_phiJ + FLOOR (0.456 / 0.530), against the 0.50 line.
3. **P × C\* by substrate** at t₂ and t₃; unrated brands drawn on the P axis.
4. **Reliability ladder:** retest of P, C\* and φ at ≈ 3 weeks and ≈ 5 months, with the frame-structure null band (0.39 mean, 0.55 95th percentile).
5. **Why no composite:** ρ(A, P) for the eight Stage 1 candidates at t₁ and t₂ against the K2 line 0.95, with the t₃ descriptive point.
6. **The rating floor:** share rated by substrate and wave; the 58.0 vs 30.4 windfall a naive average would create.

**Report (managerial):** R1 the profile (P and C\* side by side) as the new AIAS read-out; R2 "named often vs named consistently" quadrant built from Figure 3; R3 the reliability ladder in managerial styling.

---

## 10. Sequence

1. **Now (Nov 9):** this outline committed and tagged locally.
2. **Gate (Pablo):** push `v0.41-prereg-r1`, `v1.9-prereg-r1`, `aias-2-0-outline-locked` and their branches; deposit this file to `aias_2_0/prereg/`. Then t₃ (v0.41's first paid run, also a gate).
3. **v0.41 scoring + v1.9 Stage 2** (owned by the v0.41/v1.9 line).
4. **Data lock** within 3 days of both verdict files (class computed mechanically).
5. **Charts → paper → report**, each with render → rasterize → view pre-flight. Targets: paper draft by Fri Dec 4, report draft by Fri Dec 18, 2026 (v0.40's Dec 8 / Dec 14 dates take precedence).
6. **Gates:** OSF deposit and the SSRN submission (delegated to Claude, packet regenerated and checked first); site hand-off after Pablo's go.

Planning estimate: 12–18 autopilot sessions from data lock to submission-ready.

---

## 11. Open questions

- **OQ1** v0.37 SSRN abstract ID (submission scheduled Nov 9) → reference list.
- **OQ2** Romaniuk & Sharp edition/year (program-wide open item).
- **OQ3** Should the current arm (v0.38–v0.40) ever contribute a cross-panel Consistency check? Not in AIAS 2.0 (D9); revisit when the new reference panel is chosen.
- **OQ4** v0.38 / v0.39 (held studies) are out of scope; their fate is Pablo's call (roadmap).
- **OQ5** Whether the v1.9 module's planning text "collected Nov 17–21" needs a DEVIATIONS note now that the v0.41 lock dates t₃ Nov 9 (for the v1.9 owner; no effect on the outline).

---

*Outline r1, Nov 9, 2026. Working notes; not for distribution.*
