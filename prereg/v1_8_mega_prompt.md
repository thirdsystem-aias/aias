# AIAS™ v1.8 — CPC Instrument Redesign

**Pre-registration specification.** Methodology lock · frozen-set validation · no acquisition.

> This document locks the v1.8 instrument definitions, validation plan, hypotheses, verdict
> matrix, and falsification criteria *before* any scoring run against the frozen sets. It is
> the pre-registration anchor: the external git tag (`v1.8-prereg-r1`, amended pre-scoring at
> `v1.8-prereg-r2` — frames-per-channel correction, Entry 1 — and `v1.8-prereg-r3` — channel-agnostic
> primary instrument, Entry 2) and OSF deposit precede any φ / J / R_grad computation, per the v0.33+
> anchoring discipline (here the one-way boundary is the first scoring call, since there is no API
> acquisition).

---

## 0. Design class & scope

**Is:** a methodology lock that redesigns the Consistency (CPC) instrument, replacing the
CV-CPC measure falsified in v1.7. Specifies and validates a mean-independent consistency
instrument and a graded recognition signal against frozen analysis sets. The typology /
regime-detection methodology is **deferred** to a later lock, to be run as a fresh emergence
phase on the redesigned instrument.

**Is not:** a new-substrate acquisition phase (no Phase A / Phase B probes, no 24-brand
registry); not the two-component composite calibration (that is v1.9 — no φ/J composition is
performed here); not a typology finding (v0.36 already returned Cell D under the broken
instrument).

**Locked decisions carried in:** φ (quasi-binomial dispersion) as primary CPC + Jaccard
set-stability as positional diagnostic; tiered-depth graded recognition; no composition in
v1.8; frozen validation baselines v0.34 / v0.35 / v0.36.

---

## 1. Motivation — the CV-CPC failure cascade

CV-CPC (CPC_raw = SD/mean; CPC_corr = SD/√(μ(1−μ))) was not adopted. The cascade:

- **v1.7 (6878818):** CV-CPC fails the dissociation criterion — pooled |ρ| = 0.77 against the
  Presence mean vs. the 0.50 ceiling; Poisson CV ≈ 1/√mean coupling at low recall counts.
  CV-CPC not adopted.
- **v0.32 (6898581):** version-snapshot fragility (rank stability borderline / provider-dependent;
  score-magnitude stability falsified).
- **v0.33 (6909019):** provider saturation-collapse.
- **v0.34 (6915458):** CV-CPC rank order is temporally stable (the machinery reproduces), **but**
  recognition-ceiling effects in 4/5 consumer categories structurally collapse both the
  Beyond-Presence gate and the Presence rank-test → demonstrated necessity of a mean-independent
  consistency instrument *and* a graded recognition signal.
- **v0.35 (6921758):** control-flip — the binary C_P control is inert under recognition
  saturation; the recall-mean control annihilates the contrast. Converts both requirements into
  empirically-backed specifications. The phantom-signature question is designated as a
  v1.8-instrument re-test, with the frozen 84-unit set as baseline.
- **v0.36 (6927958):** regime falsification (Cell D); four instrument pathologies — CV
  computability floor erases low-recall coverage (15/24 in the label substrate); saturation
  direction reversal (dispersion HIGHER under saturation, Levene p = .003); structure visible only
  under mean removal; floor-dependent headline verdict. Adds the third requirement: defined
  coverage over the low-recall segment.

**Three locked requirements for the replacement instrument:**

1. **Mean-independence** — escape the CV ≈ 1/√mean trap (|ρ| against the recall mean ≤ 0.50).
2. **Graded recognition signal** — finer than binary C_P (inert under saturation), and *not* the
   recall mean (which annihilated the contrast).
3. **Defined low-recall coverage** — remain computable across the segment where CV is undefined.

---

## 2. Instrument specifications (locked)

Notation: brand *b*; six-model panel *m* ∈ {1..M}, M = 6; **F = 6 probe-frames per model**
(3 R_cat + 3 R_cult), **pooled channel-agnostically** for the primary instrument — the φ
normalization constant. Binary surfacing per (model, frame). Per-model count k(b,m) ∈ {0..F};
pooled rate π̂_b = Σ_m k(b,m) / (M·F), with **M·F = 36**.

**The primary instruments are channel-agnostic.** The certified omnibus extraction
(`score_v0_31` → a 0..6 per-model count) and all three validation framings are channel-agnostic
by construction, and v0.23's two channels (cultural-cult / editorial-authority) are not
commensurable with R_cat / R_cult. Because φ is mean-independent by construction (it divides out
the binomial variance F·π̂(1−π̂)), the channel-mixing *level* confound that would otherwise
motivate splitting channels is already removed; the residual channel signal is *positional* —
J's domain. **A per-channel variant of φ / J (R_cat, R_cult separately, F = 3, M·F = 18) is
retained as a SECONDARY, non-gating diagnostic on the canonical two-channel substrates v0.20–v0.22
only**; **v0.19** (single-channel — no R_cat/R_cult split) and **v0.23** (non-canonical channels;
the R_cat/R_cult equivalence was deferred to v0.31, unvalidated) are both excluded from it.

### 2.1 φ — primary CPC (quasi-binomial between-model dispersion), inconsistency-oriented

    φ_b = [1/(M−1)] · Σ_m  (k(b,m) − F·π̂_b)²  /  [ F·π̂_b·(1−π̂_b) ]

Pearson dispersion (χ²/df, df = M−1) of per-model surfacing against the homogeneity null
(every model shares π̂_b). Null E[φ] = 1. φ > 1 → models disagree (inconsistent);
φ < 1 → models agree beyond chance (consistent). **Mean-independent by construction** — the
denominator divides out the binomial-expected variance F·π̂(1−π̂), removing the level coupling.
**Defined** for all *b* with π̂_b ∈ (0,1) (≥1 surfacing, not full saturation); undefined only at
the true-zero floor — which is correct behavior, not a CV-style blowup. A brand surfacing once
total (π̂ = 1/36, i.e. one surfacing across the 6 models × 6 frames, channel-agnostic) still
yields a finite φ. *(The secondary per-channel diagnostic uses F = 3, M·F = 18, π̂ floor = 1/18,
on v0.20–v0.22.)*

### 2.2 J — positional diagnostic (mean pairwise Jaccard), consistency-oriented

    S(b,m) = { frames where b surfaced under model m }
    J_b    = mean over model pairs (m,m′) of  |S(b,m) ∩ S(b,m′)| / |S(b,m) ∪ S(b,m′)|

J ∈ [0,1]; J = 1 every model surfaces *b* in identical frames (positionally consistent);
J → 0 disjoint frames. Defined for ≥1 surfacing across ≥2 models. Captures *where* a brand
surfaces, not *how much* — the facet φ cannot see. Computed channel-agnostically (over all six
frames) for the primary; the per-channel J is part of the secondary diagnostic (v0.20–v0.22).

*Pre-specified R1 contingency (locked, not post-hoc):* if |ρ(J, μ)| > 0.50 from small-set bias,
fall back to chance-corrected Jaccard J_adj = (J − E[J|sizes]) / (1 − E[J|sizes]).

### 2.3 R_grad — graded recognition (tiered depth), **schema-conditional**

Per (brand, model): D(b,m) ∈ {0 = not recognized, 1 = name, 2 = name + correct category,
3 = name + category + ≥1 correct attribute}. R_grad_b = mean_m D(b,m) ∈ [0,3]. Retains
discriminating variance under binary-C_P saturation (premium / heritage brands reach tier 3
while mass brands sit at tier 1, even when C_P = M for all). Sourced from the *recognition* probe,
not recall — sidestepping v0.35's recall-mean over-control.

**Conditional:** deriving tiers 2–3 retroactively requires the frozen recognition channel to
retain re-scorable response text. If re-scorable → R_grad validates here (H_GradedRecognition is
PRIMARY). If the frozen channel holds binary verdicts only → R_grad locks as a **forward spec**
(defined here, validated in a designated later phase); v1.8's empirical results reduce to φ + J,
a clean and honest outcome.

---

## 3. Validation-set manifest & inclusion partition

| Set | Role |
|---|---|
| **v0.34** (6915458) two-wave t₁→t₂ | φ / J temporal reproducibility across waves |
| **v0.35** (6921758) frozen 84-unit set | phantom-signature baseline (H_PhantomSignature) |
| **v0.36** (6927958) label substrate | low-recall stress case (the 15/24 CV-undefined cohort) |

All three sets are framings of one frozen omnibus (the v0.19–v0.23 five-substrate, six-model
panel); the primary φ / J are channel-agnostic, so all five substrates — including v0.23 —
participate. The per-channel secondary diagnostic runs on v0.20–v0.22 only.

**Inclusion partition (pre-locked, pre-analysis):** φ / J computed for every brand with ≥1
surfacing. True-zero brands are partitioned out *before* analysis and reported
separately. The defined / undefined split is a **pre-specified partition, not a finding** — this
avoids the v1.7 trap where the defined-rate emerged as a result.

---

## 4. Hypotheses

| ID | Tier | Statement | CONFIRMED threshold | Directional lean |
|---|---|---|---|---|
| **H_CV_Reproduces** | baseline / manipulation check | CV-CPC's mean-coupling reproduces on the frozen sets | \|ρ(CV-CPC, μ)\| ≥ 0.50, in the v1.7 neighborhood | CONFIRMED |
| **H_MeanIndependent** | PRIMARY | φ is mean-independent | \|ρ(φ, μ)\| ≤ 0.50, pooled across sets | CONFIRMED (risk: floor effects reintroduce coupling) |
| **H_LowRecallDefined** | PRIMARY | φ extends defined coverage into the low-recall segment | φ defined for 100% of ≥1-surfacing brands AND φ-defined set strictly contains the CV-CPC-defined set, gain concentrated in the low-recall stratum | CONFIRMED |
| **H_GradedRecognition** | PRIMARY* | tiered R_grad discriminates under C_P saturation and is not recall-mean in disguise | among C_P = M brands: Var(R_grad) > 0 spanning ≥2 tiers AND \|ρ(R_grad, μ)\| ≤ 0.50 | CONFIRMED if re-scorable; else FORWARD-SPEC |
| **H_PositionalDissociation** | SECONDARY | φ and J capture distinct facets | \|ρ(φ, J)\| ≤ 0.70 AND ≥1 identified discordant brand | CONFIRMED (positional vs magnitude facet; per-channel asymmetry = secondary-diagnostic view) |
| **H_PhantomSignature** | TERTIARY (exploratory) | near-phantom (≥1-surfacing) brands carry a distinct φ / J signature vs the v0.35 84-unit baseline | no directional commitment | exploratory |

\* PRIMARY if frozen recognition is re-scorable; FORWARD-SPEC otherwise.

---

## 5. Verdict matrix (exhaustiveness-checked — v0.36 institutional rule)

Every reachable outcome mapped; no unmapped residual.

- **H_CV_Reproduces:** { CONFIRMED ≥0.50 · NULL <0.50 (data artifact — invalidates the comparison) }
- **H_MeanIndependent:** { CONFIRMED ≤0.50 · FALSIFIED >0.50 }
- **H_LowRecallDefined:** { CONFIRMED full recovery, zero residual undefined among ≥1-surfacing · PARTIAL recovery with residual undefined (implementation flag) · FALSIFIED no gain }
- **H_GradedRecognition:** { CONFIRMED variance + distinct · FALSIFIED-circular variance but \|ρ(R_grad,μ)\| > 0.50 · FALSIFIED-degenerate no variance under saturation · FORWARD-SPEC frozen data not re-scorable }
- **H_PositionalDissociation:** { CONFIRMED non-redundant + discordants exist · PARTIAL \|ρ\| ≤ 0.70 but no discordant brand · FALSIFIED \|ρ\| > 0.70 (redundant) }
- **H_PhantomSignature:** { SIGNATURE-PRESENT · NULL · UNDETERMINED (insufficient non-zero phantoms) }

---

## 6. Scoring & falsification

- **ρ = Spearman** (program convention), computed **per set** then pooled with set as a blocking
  factor; per-set ρ reported alongside the pooled value to catch set-dependence (the v0.32
  provider-dependence lesson).
- **Make-or-break line:** H_MeanIndependent. If |ρ(φ, μ)| > 0.50 pooled, φ fails its central
  requirement and **v1.8 cannot lock φ** — escalation path is the beta-binomial ICC /
  overdispersion ρ alternative, re-entered *before* any instrument is locked. All downstream work
  (v0.37+, v1.9 composite) depends on this gate passing.
- No verdict is assigned before the scoring run produces `osf/.../v1_8/v1_8_verdicts.json`. No
  figures or report copy precede the verdicts JSON.

---

## 7. Pre-registration discipline

- Scope lock → scaffold → **this spec locked at commit + tag `v1.8-prereg-r1`**, amended
  pre-scoring at **`v1.8-prereg-r2`** (frames-per-channel correction) and **`v1.8-prereg-r3`**
  (channel-agnostic primary instrument) → external anchor (tag push + OSF deposit) → scoring →
  figures → paper → brand report → OSF deposit → SSRN. ORDER LOCKED.
- The external anchor precedes the **first scoring call** (v1.8's one-way boundary, in place of an
  API acquisition call).
- Tags additive-only, never force-moved. Pre-scoring amendments (methodology or design defects
  caught before the one-way boundary) are documented as additive DEVIATIONS entries (F-correction =
  Entry 1; channel-agnostic primary = Entry 2).

---

## 8. Declarations (stub — finalized in paper §COI)

- **COI:** Samsung tier-2/3 disclosure is *inherited from the substrates present in the frozen
  validation sets* (v0.34 / v0.35 / v0.36). Named subsidiaries to be verified against each frozen
  set's locked registry before paper submission — do not assume the automotive trio applies unless
  an automotive substrate is in scope.
- **Funding:** Self-funded.
- **Ethics:** Not applicable; no human subjects; frozen public-API + LLM-prompt data, re-analyzed.
- **Data & code:** frozen inputs and scoring code deposited at osf.io/ec6wh under the v1.8 tree.

---

## DEVIATIONS

*(contemporaneous; additive log, mirrored in the locked content module — no values computed)*

- **Entry 0 (r1 lock) — R_grad FORWARD-SPEC resolution.** A pre-scoring feasibility check on the
  frozen recognition channel resolves H_GradedRecognition along its pre-committed FORWARD-SPEC
  branch: the frozen v0.34 / v0.35 / v0.36 lock retains binary recognition only (hash-sealed at
  v0.35), no re-scorable response text, so tiers 2–3 of R_grad cannot be derived retroactively.
  R_grad is therefore DEFINED here and validated in a designated later fresh-collection phase
  (v0.32 / v0.28 are the retained re-scorable-text corpora). The audit
  `osf/v33/exploratory/v33_recognition_source_audit.json` confirms the recognition saturation is
  REAL (v0.23 r_level uniformly R3), not a binarization artifact. v1.8's empirical results reduce
  to φ + J. Not result-driven.
- **Entry 1 (r1 → r2) — frames-per-channel correction.** Pre-scoring methodology correction,
  caught before the one-way boundary (no φ / J computed). r1 specified F = 6 frames per model and a
  φ low-recall floor π̂ = 1/36, but the frozen v0.34 Phase B acquisition has **F = 3 frames per
  channel** (q1–q3 → R_cat, q4–q6 → R_cult; 6 per model total). Because all instruments are
  computed per channel (channel pooling prohibited), the per-channel φ denominator uses F = 3,
  **M·F = 18**, and the minimum non-zero per-channel **π̂ = 1/18**. The r1 figures assumed 6 frames
  within a channel; corrected here. Same defect class as v1.7's r3 frames-per-channel amendment.
  No hypotheses or thresholds change (all F-independent); only the φ normalization constant and the
  ILLUSTRATION / low-recall-note figures. *(Superseded in substance by Entry 2: r3 makes the primary
  instrument channel-agnostic, which restores F = 6 for a different, correct reason; the per-channel
  F = 3 figures here now describe the secondary diagnostic only.)*
- **Entry 2 (r2 → r3) — channel-agnostic primary instrument.** Pre-scoring design correction, caught
  before the one-way boundary (no φ / J computed). r1 and r2 both specified **per-channel** φ / J
  (R_cat, R_cult separately; channel pooling prohibited). Inspecting the frozen omnibus channel
  structure exposed an internal contradiction: the validation sets span v0.19–v0.23, but **v0.23's
  channels are cultural-cult / editorial-authority, not R_cat / R_cult**, and **v0.19 is
  single-channel** (no R_cat/R_cult split at all) — so two of the five substrates break the
  per-channel framing and a per-channel R_cat/R_cult instrument cannot span the stated omnibus. Mapping v0.23's channels onto R_cat/R_cult is the
  channel-construct equivalence v1.7 explicitly **deferred to v0.31 as unvalidated** — rejected. r3
  resolves it by making φ / J **channel-agnostic** as the PRIMARY instrument: the six frames per model
  pool to a 0..6 count (F = 6, **M·F = 36**, φ floor **π̂ = 1/36**), matching the certified
  channel-agnostic omnibus extraction (`score_v0_31` → 0..6 per model) on which all three framings and
  v1.7's own CV-CPC were already built. The per-channel variant is **retained as a SECONDARY,
  non-gating diagnostic on v0.20–v0.22 only**. Not a loss: φ is mean-independent by construction, so
  the channel-mixing *level* confound that motivated pooling-prohibition is already divided out; the
  residual channel signal is positional (J's domain). Honest record of the arc: r1's F = 6 was the
  right number for the wrong reason (assumed 6 frames/channel); r2's F = 3 was correct *for* a
  per-channel instrument, but per-channel was itself the error — specified from the out-of-sample v0.24
  channel structure, not verified against the v0.19–v0.23 omnibus the framings are built on; r3
  restores F = 6 for the correct reason (channel-agnostic pooling). Root cause: locked (r1) and amended
  (r2) before inspecting the omnibus channel structure. All five substrates retained channel-agnostically.
