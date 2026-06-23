# ---------------------------------------------------------------------------
# AIAS(TM) v0.37 -- Identity-Load (IL-Direct) x CPC -- PRE-REGISTRATION CONTENT
# Phase type: re-analysis (no new LLM acquisition; v0.33 pattern)
# Lock tag: v0.37-prereg-r1
# Amended at v0.37-prereg-r2 (additive; r1 frozen at 2f381f7).
#   r2 = verdict-matrix exhaustiveness completion of the FALSIFIED row; see DEVIATIONS Entry 2.
#
# NOTE TO OPERATOR (Claude Code): before commit, resolve every
# <<CONFORM-VERBATIM: ...>> placeholder by pulling the EXACT locked text from
# the named source record. Do not paraphrase. The guard at the bottom of this
# file raises if any placeholder remains.
#
# SCORER-WIRING NOTE (downstream, not this authoring pass): the seated
# score_v0_37.py is the v1.8 phi/J kernel and expects STRUCTURED constants from
# its content module (METADATA, COMPUTATION, M, THRESHOLDS, HYPOTHESES-as-dict,
# VERDICT_KEYS). This module is the PROSE lock record. Bridging the two -- adding
# the structured config OR adapting the scorer's reads -- is part of the flagged
# phi/J scorer rework and happens after this lock, before --run. Not done here.
# PINNED CONSTRAINT (F): the structured constants (thresholds, sign convention,
# verdict keys) MUST be a faithful transcription of this locked prose. On ANY
# discrepancy, THIS PROSE IS AUTHORITATIVE -- the scorer rework may not silently
# re-number a threshold or flip a sign.
# ---------------------------------------------------------------------------

PHASE_ID = "v0.37"
PHASE_TITLE = ("Identity-Load x CPC: Does Cultural-Channel Recall Asymmetry "
               "Condition Cross-Model Presence Consistency?")

# ---------------------------------------------------------------------------
# DESIGN
# ---------------------------------------------------------------------------
DESIGN = """
Frozen re-analysis, no new LLM acquisition (v0.33 pattern).

Scope = the canonical two-channel trio v0.20 / v0.21 / v0.22, n = 72 (24x3) --
the intersection of phi-availability (defined across all five omnibus
substrates) and continuous IL-Direct availability (the two-channel
decomposition exists only for the trio). v0.19 is EXCLUDED (single-channel by
acquisition; the two-channel R_cult decomposition was first acquired at v0.20,
so IL-Direct is out of construct, not recomputable without re-acquisition).
v0.23 is an OPTIONAL runtime-verify extension, walled (not in the canonical
two-channel trio; frame granularity runtime-uncertain).

Per-brand inputs:
  DV         = phi (v1.8 mean-independent consistency instrument; from the
               seated score_v0_37.py phi/J kernel). CPC reported per the v1.8
               scorer's locked convention.
  moderator  = IL-Direct delta = mean(R_cult) - mean(R_cat), used at brand
               granularity (R_cult_total - R_cat_total) from
               osf/methodology/v1_7/data/v1_7_cpc.csv.
  controls   = C_P (v1.6) + recall-mean, for SECONDARY presence-robustness only.

Output: osf/v37/v37_verdicts.json.
"""

# ---------------------------------------------------------------------------
# METRIC DEFINITION (pinned) -- the DV. Rewritten from CV-CPC to phi/J.
# ---------------------------------------------------------------------------
METRIC_DEFINITION = """
DV = phi, the v1.8 cross-model consistency instrument (locked formula):

    phi_b = [1/(M-1)] * sum_m (k - F*pi_hat)^2 / [F*pi_hat*(1-pi_hat)]

channel-agnostic; k in 0..F is the per-model surfacing count, pi_hat =
sum_k/(M*F). Fork-A partition (pre-specified exclusions): pi_hat == 0
(true-zero floor) and pi_hat == 1 (saturation ceiling) are partitioned out,
counts reported separately.

ORIENTATION (PINNED; verified against score_v0_37.py:275 and :651, not memory):
phi is INCONSISTENCY-oriented -- higher phi = greater cross-model dispersion =
LOWER consistency. The kernel's consistency-oriented transform is
cons_phi = 1 - pctrank(phi). v0.37 computes the PRIMARY statistic on RAW phi;
the "IL up -> consistency down" prediction therefore maps to a PREDICTED
rho(IL-Direct, phi) > 0. This sign convention is binding for the verdict matrix.

MEAN-INDEPENDENCE (the reason the manipulation-check scaffolding is retired):
|rho(phi, mu)| = 0.091 at v1.8 results-lock, vs CV-CPC's 0.682. phi is not
mechanically coupled to recall level, so the raw IL->phi arm is an inferential
claim, not a pipeline manipulation check.

CV-CPC (v1.7, instrument NOT adopted) is retained as a COMPARATOR only, reported
alongside per the v1.8 scorer's convention -- never as a v0.37 DV. J (the
frame-resolved consistency-oriented instrument; consistency = pctrank(J)) is
reported per scorer convention where frame-resolved.
"""

# ---------------------------------------------------------------------------
# MODERATOR DEFINITION (locked) -- replaces v0.35's phantom classification.
# ---------------------------------------------------------------------------
MODERATOR_DEFINITION = """
Moderator = IL-Direct, the per-brand two-channel recall asymmetry:

    IL-Direct(b) = R_cult(b) - R_cat(b)

a CONTINUOUS per-brand covariate, consumed as R_cult_total - R_cat_total from
osf/methodology/v1_7/data/v1_7_cpc.csv. Higher IL-Direct = more
cultural-channel-led surfacing = higher Identity Load.

Construct anchor: v1.6 (SSRN 6816340) Increment 2, H_IdentityLoad_Direct,
delta = mean(R_cult) - mean(R_cat). v1.6 evaluated it at CELL granularity; v0.37
uses the same functional at BRAND granularity as the continuous moderator.

Availability is the scope boundary (this is the design clarifying itself, not a
limitation): the two-channel decomposition is frozen per-brand ONLY for the
canonical trio v0.20 / v0.21 / v0.22 (confirmed at score_v0_37.py:112,
SEC_SUBS; and v1_7_cpc.csv columns). v0.19 is single-channel (out of construct);
v0.23 is the walled runtime-verify extension. This is precisely the scope where
IL-Direct is construct-valid, so the n=72 restriction is honest, not arbitrary.
"""

# ---------------------------------------------------------------------------
# PROVENANCE FORWARD-NOTE (resolves the v0.31<->v0.32 framing thread)
# ---------------------------------------------------------------------------
PROVENANCE_FORWARD_NOTE = """
The paper's provenance section states the consumption convention explicitly:
the v0.31 frozen per-model inputs remain valid archived data; the v0.31 paper
is withdrawn; CV-CPC's methodological status is fixed by v1.7 (computation
defined; instrument not adopted), and all downstream phases (v0.32-v0.37)
consume the quantity under that status.

v0.37-specific: the ADOPTED DV is the v1.8 phi instrument (mean-independent);
CV-CPC appears here only as a retained comparator, consumed under the v1.7
not-adopted status above.
"""

# ---------------------------------------------------------------------------
# INPUT RECONCILIATION GUARDRAIL (binding) -- INHERITED, no edit (pins trio).
# ---------------------------------------------------------------------------
RECONCILIATION_GUARDRAIL = """
Gate, run after lock and before any contrast is computed:

1. Consumed CV-CPC and C_P vectors must reproduce the v0.33-deposited values
   bit-for-bit (hash check).
2. v0.20 / v0.21 / v0.22 vectors must reconcile to the v1.7 r_per_model column
   per the v0.33 anchor-scope convention (scope limited to those three phases).
3. The IL-Direct moderator source -- R_cult_total and R_cat_total in
   osf/methodology/v1_7/data/v1_7_cpc.csv -- must reproduce the v1.7-deposited
   values bit-for-bit (hash check). IL-Direct is a NEW input axis this phase and
   is anchored on the same footing as the DV-side inputs (clause added at r1 per
   author direction; the v0.35-inherited guardrail covered only DV-side inputs).

Reconciliation failure halts the phase.
"""

# ---------------------------------------------------------------------------
# ELIGIBILITY + ATTRITION (computed before any contrast) -- re-pointed to trio.
# ---------------------------------------------------------------------------
ELIGIBILITY_ATTRITION = """
Scoring step 1 enumerates the trio analysis set and writes it to
osf/v37/data/v37_il_phi_analysis_set.csv before any contrast is computed.

A brand unit is eligible iff BOTH:
  - phi is defined (scorer phi_defined flag; excludes the Fork-A pi_hat=0
    true-zero floor and pi_hat=1 saturation ceiling), AND
  - IL-Direct is defined (guaranteed across the trio from v1_7_cpc.csv).
Analysis set = phi-defined AND IL-defined units across v0.20 / v0.21 / v0.22.
Attrition (trio brands vs analyzable) is reported per substrate.

Primary inference is POOLED at brand level (n up to 72, within-substrate ranks).
The per-substrate test is reported DESCRIPTIVELY only (N=3 substrates; see
H_IL_Cross_Substrate). No per-substrate eligibility floor gates the pooled
primary.

Fork-A saturation diagnostic (pre-registered; recognition saturation was heavy
in this trio -- v0.21 uniform C_P = 6/6, v0.22 uniform saturation -- so the phi
pi_hat=1 ceiling exclusion is expected to bite). Before any contrast, and
reported regardless of outcome:
  - realized analyzable n PER SUBSTRATE after Fork-A (the true count, not the
    nominal 24/cell);
  - the IL-Direct distribution of EXCLUDED vs INCLUDED units, so the truncation
    is CHARACTERIZED empirically, not assumed;
  - an n-floor of 45 (LOCKED at r1): if realized pooled analyzable n < 45, the
    PRIMARY is reported INDETERMINATE-UNDERPOWERED rather than forced (the v0.17
    panel-inadequacy disposition). Rationale (band-coherence, not plucked): the
    CONFIRMED band requires |rho| >= 0.30 AND p < .05, but the critical
    two-sided Spearman rho at p=.05 RISES as n falls -- it crosses 0.30 at
    n ~= 44. Below ~44 the band's two conditions are mutually inconsistent (one
    cannot reach p < .05 at |rho| = 0.30), so the verdict structure is
    incoherent; 45 pins the floor with a hair of margin.
  - per-substrate fragility flag: any substrate contributing < 10 analyzable
    units has unstable within-substrate ranks -- reported as a fragility note on
    the pooled primary, NOT a gate.

Truncation-bias direction is CHARACTERIZED EMPIRICALLY, not asserted UNSIGNED:
if saturated brands skew low-IL (canonical category staples saturate), the
ceiling exclusion truncates the LOW-IL end of the IL-Direct range -- a SIGNED
truncation on the IL->phi slope. The excluded-vs-included IL-Direct distribution
above is what settles the sign; it is reported, not presumed.
"""

# ---------------------------------------------------------------------------
# HYPOTHESES (phi DV; single inferential primary)
# ---------------------------------------------------------------------------
HYPOTHESES = """
H_IL_Consistency -- PRIMARY (gating; the phase's single inferential test).
Continuous IL-Direct conditions cross-model phi-consistency. Statistic: ranks
computed WITHIN substrate, pooled to a single Spearman rho(IL-Direct, phi)
across the trio; permutation inference with IL-Direct labels permuted WITHIN
substrate only, >= 10,000 Monte Carlo draws, TWO-SIDED.
  CONFIRMED:           |rho| >= 0.30, p < 0.05.
                       Sign split (phi inconsistency-oriented; see
                       METRIC_DEFINITION):
                         rho > 0 (predicted: IL up -> consistency down) = CONFIRMED
                         rho < 0 (opposite)                             = CONFIRMED_REVERSED
  FALSIFIED:           |rho| < 0.15.
  MARGINAL:            0.15 <= |rho| < 0.30, OR |rho| >= 0.30 with p >= 0.05.
Directional pre-commitment: IL up -> consistency down (cultural-channel-led
presence surfaces more idiosyncratically across model corpora than
category-canonical presence), i.e. predicted rho(IL-Direct, phi) > 0.
Inferential weight (pinned): because phi is mean-independent (|rho(phi,mu)| =
0.091), this raw arm IS the inferential claim -- not a manipulation check. The
v0.35-era recall-coupling manipulation-check scaffolding does not apply.

H_IL_Presence_Robustness -- SECONDARY (robustness; NOT a gate).
Partial Spearman rho(IL-Direct, phi | C_P, recall-mean). Substantial
attenuation (|rho_partial| < 0.15 when the raw primary rho >= 0.30) indicates a
presence-MEDIATED association and is reported as a scope QUALIFICATION, not a
falsification. This is explicitly NOT a control-flip -> UNDETERMINED gate: that
machinery was a CV-CPC recall-coupling artifact, and phi's mean-independence
retires it.

[r2 amendment -- see DEVIATIONS Entry 2] Partial-arm computation and bands, pinned:
  Method (SINGLE authoritative computation): partial Spearman via inversion of the
  4-variable Spearman rank-correlation matrix over {IL-Direct, phi, C_P, recall-mean};
  the IL-Direct x phi partial = -P[IL,phi] / sqrt(P[IL,IL] * P[phi,phi]) from the
  precision matrix P. The 4x4 precision-matrix inversion partials out C_P and
  recall-mean SIMULTANEOUSLY and is ORDER-INDEPENDENT; it IS the locked computation.
  The pairwise-recursive two-control formula is population-equivalent but is NOT the
  locked computation -- it can differ in finite samples by computation order, and the
  verdict can hinge on which side of 0.30 the partial lands. One method, no ambiguity.
  Inference: the SAME within-substrate stratified permutation as the primary --
  IL-Direct labels permuted WITHIN substrate, phi / C_P / recall-mean held fixed,
  >= 10,000 MC draws, TWO-SIDED; p_perm is the partial's two-sided permutation p.
  Bands (symmetric to the primary; govern the raw-FALSIFIED verdict-matrix row):
    partial CONFIRMED : |rho_partial| >= 0.30 AND p_perm < .05
    partial NULL      : |rho_partial| < 0.15
    partial MIDDLE    : 0.15 <= |rho_partial| < 0.30, OR |rho_partial| >= 0.30
                        with p_perm >= .05
  The CONFIRMED-branch attenuation cut above (|rho_partial| < 0.15 when the raw
  primary rho >= 0.30) is UNCHANGED; these bands add the raw-FALSIFIED row mapping only.

H_IL_Cross_Substrate -- SECONDARY, descriptive-only.
Per-substrate rho sign consistency across the trio. N = 3 -> NO inferential
claim (below the v0.33 underpowered-ordinal precedent). The per-substrate rho
table is reported regardless of pattern.

H_IL_t2_Stability -- TERTIARY, exploratory, walled.
ONLY where the v0.34 t2 wave intersects the trio (runtime-verify): a descriptive
test-retest of the IL-Direct -> phi association. No confirmatory threshold;
quarantined from PRIMARY verdict logic; dropped silently if no intersecting t2
wave exists.
"""

# ---------------------------------------------------------------------------
# DECISION RULES (thresholds, inference, robustness)
# ---------------------------------------------------------------------------
DECISION_RULES = """
Primary statistic: pooled within-substrate-ranked Spearman rho(IL-Direct, phi).
Bands (pinned): |rho| >= 0.30 & p < .05 -> CONFIRMED (sign-split per
HYPOTHESES); |rho| < 0.15 -> FALSIFIED; 0.15 <= |rho| < 0.30, or |rho| >= 0.30
with p >= .05 -> MARGINAL. Inference: within-substrate stratified permutation,
two-sided, >= 10,000 MC.

Robustness (reported, not gating the verdict):
  - LOSO: drop each substrate in turn, recompute rho on the remaining 48 units.
    Coarse at 3 substrates. NON-SURVIVAL (a leave-one-out sign flip, or |rho|
    crossing a band boundary) DOWNGRADES the verdict ONE band: CONFIRMED ->
    MARGINAL. A MARGINAL that fails LOSO is reported as fragile-MARGINAL (not
    further downgraded -- absence on a 2-substrate subset is uninformative).
    This is a DELIBERATE departure from the v0.32 precedent (LOSO non-survival
    -> hard UNDETERMINED), softened because a hard gate is too brittle at N=3
    substrates; the departure is documented here, not silent.
  - Brand-level jackknife / influence diagnostics given n <= 72.
  - Threshold sensitivity: rerun the primary at rho cutoffs +/- 0.05.

MARGINAL is acknowledged as a plausible MODAL outcome on fixed data and is a
publishable, honestly-indeterminate result routed forward.

Partial-arm (H_IL_Presence_Robustness) [r2]: partial Spearman via 4-variable
rank-correlation-matrix inversion over {IL-Direct, phi, C_P, recall-mean};
inference by the SAME within-substrate stratified permutation as the primary
(>= 10,000 MC, two-sided). Verdict-matrix bands for the partial are pinned in
H_IL_Presence_Robustness (r2). Permutation determinism: the MC seed is pinned in
the SCORER (not this lock -- pinning an arbitrary integer would over-constrain the
lock); every permutation p is reported with its Monte Carlo standard error, and
any |rho| within ~2 MC-SE of the .05 boundary is flagged seed-sensitive
(rationale: DEVIATIONS Entry 2).
"""

# ---------------------------------------------------------------------------
# VERDICT MATRIX (exhaustive over primary x presence-robustness)
# ---------------------------------------------------------------------------
VERDICT_MATRIX = """
Cells = PRIMARY rho verdict (H_IL_Consistency) x presence-robustness
concordance (H_IL_Presence_Robustness). Every reachable cell is assigned; no
positive claim arises from a suppression-only or threshold-edge pattern.

  CONFIRMED (predicted sign, rho > 0)
    x partial CONCORDANT (|rho_partial| >= 0.15):
        -> HEADLINE POSITIVE. IL-Direct conditions cross-model consistency
           mean- AND presence-independently.
    x partial ATTENUATES (|rho_partial| < 0.15):
        -> PRESENCE-SCOPED POSITIVE, qualified (presence-mediated). Reported,
           NOT falsified.

  CONFIRMED_REVERSED (rho < 0)
    -> Real OPPOSITE finding (cultural-load brands MORE consistent), reported in
       its own cell; same partial-concordance qualifier applies.

  MARGINAL
    -> Weak-but-present (modal-plausible). Reported; routed forward.

  FALSIFIED  (raw |rho| < 0.15; partial bands per H_IL_Presence_Robustness r2)
    x partial NULL  (|rho_partial| < 0.15):
        -> CLEAN NULL. IL-Direct orthogonal to phi-consistency. Negative result
           reported. This is the ONLY FALSIFIED-row cell that reads as a clean negative.
    x partial CONFIRMED  (|rho_partial| >= 0.30 & p_perm < .05)
      OR partial MIDDLE  (0.15 <= |rho_partial| < 0.30, or |rho_partial| >= 0.30
                          with p_perm >= .05):
        -> *** SUPPRESSION CELL -> UNDETERMINED-pending-suppression-diagnosis. ***
           ANY non-null presence-controlled partial under a null raw arm is the
           suppression signature: the presence control revealed structure the raw
           masked. Do NOT claim a clean IL -> consistency effect, and do NOT wave it
           through as CLEAN NULL. Mapped conservatively toward UNDETERMINED -- the
           v0.36 lesson: reachable cell, explicitly assigned, never a positive, and a
           weak-but-present partial is NOT a clean negative.
           [r2 -- DEVIATIONS Entry 2: completes the FALSIFIED row that r1 split only on
           the raw-CONFIRMED-branch attenuation cut.]
"""

# ---------------------------------------------------------------------------
# SUPPLEMENTARY CONTRAST (pre-registered; illustrative, NON-GATING)
# ---------------------------------------------------------------------------
SUPPLEMENTARY_CONTRAST = """
Alongside the primary IL-Direct -> phi test, run the SAME pooled
within-substrate-ranked Spearman on IL-Direct -> CV-CPC (the v1.7 retired
instrument) as an INSTRUMENT-SENSITIVITY illustration: it shows whether the
retired instrument would have yielded a different read. EXPLICITLY NON-GATING --
it touches no verdict, no threshold, no routing. Pre-registered as
supplementary-illustrative so the post-hoc objection ("you only report the
instrument that worked") cannot land.
"""

# ---------------------------------------------------------------------------
# CONSTRUCT LIMITATION (carried into the paper, not engineered away)
# ---------------------------------------------------------------------------
CONSTRUCT_LIMITATION = """
IL-Direct (delta = R_cult - R_cat) and phi are different functionals of the SAME
probe matrix. A confirmed IL -> inconsistency link may therefore reflect a
common diffuse-identity cause rather than IL CAUSING inconsistency. State this
in the paper; do not attempt to engineer it away.
"""

# ---------------------------------------------------------------------------
# DEVIATIONS
# ---------------------------------------------------------------------------
DEVIATIONS = """
Entry 0 -- COI carry-forward (no new acquisition; conformed from the locked
Declarations of EACH trio substrate -- v0.20, v0.21, v0.22 -- not from memory).
v0.37 re-uses the v0.20 / v0.21 / v0.22 registries and inherits their locked
screens unchanged; no new exposure arises from a frozen re-analysis.

  v0.20 skincare (conformed from papers/v0_20/v0_20_ssrn_paper_draft.md
  Declarations + DEVIATIONS Entry 0, v0.20-prereg-r1):
  None of the 24 brands in the v0.20 registry is affiliated with Samsung
  Electronics America. Samsung's historical beauty exposure was via Cheil
  Industries (spun off pre-2026 in corporate restructuring); no current overlap
  with the v0.20 registry. Disposition: no deviation warranted. (Disclosed
  historical exposure -- NOT a bare "no affiliation" claim.)

  v0.21 cosmetics (conformed from papers/v0_21/v0_21_ssrn_paper_draft.md
  Declarations + DEVIATIONS Entry 0, v0.21-prereg-r1):
  None of the 24 brands in the v0.21 registry is affiliated with Samsung
  Electronics America. Clean screen; documented as DEVIATIONS Entry 0 per
  program convention.

  v0.22 automotive (conformed from papers/v0_22/v0_22_ssrn_paper_draft.md
  Declarations "Conflict of interest" + DEVIATIONS Entry 0 Part B, v0.22-prereg):
  Samsung subsidiaries hold tier-2/3 component supply relationships with several
  brands in the v0.22 registry: Harman International (audio systems) supplies
  Mercedes-Benz, BMW, and other premium automotive OEMs; Samsung SDI (battery
  cells) supplies BMW (i-series), Volkswagen Group brands including Bentley and
  Porsche (Stellantis-adjacent platforms), and others; Samsung Display
  (infotainment) supplies Mercedes-Benz and BMW. Tesla and Polestar also have tangential Samsung-component exposure at the
  parts level. These are non-competitive supply relationships; Samsung
  Electronics America does not produce or market passenger car brands and has no
  brand-level competitive overlap with any v0.22 registry entry. No operational
  restriction on registry composition was imposed.

  v0.19 AKG -> Denon substitution (RETAINED as program-lineage provenance only;
  v0.19 is NOT in the v0.37 trio analysis set -- conformed from osf/v19/
  PRE_REGISTRATION_v0_19.md Sec. 2.3 + v0.19 DEVIATIONS Entry 1):
  AKG was substituted with Denon before the v0.19 pre-reg lock (AKG owned by
  Harman International, a Samsung subsidiary, since 2016) to avoid any appearance
  of conflict; it was AKG only (not JBL).

Entry 1 -- Scaffold reframe (not a methodology amendment):
The cloned v0.35 phantom-signature hypothesis stubs (H_Phantom_*) were the
scaffolder's carry-forward, not v0.37's design; they are overwritten by the
IL-Direct x phi moderation design authored here. v0.34 two-wave acquisition
scaffolding removed (v0.37 is a no-acquisition re-analysis). The v1.8 phi/J
instrument is v0.37's adopted DV BY ORIGINAL DESIGN -- not a deviation from a
prior adopted instrument.

Entry 2 -- r2 amendment: verdict-matrix exhaustiveness completion (PRE-ACQUISITION; no --run).
Caught by pre-acquisition inspection of the seated scorer against the locked matrix --
BEFORE any scoring call. The blinding boundary is intact: no --run has occurred and no
verdict has been computed, so amending the lock now is fully legitimate. This is an
r1 -> r2 amendment working as intended: a methodology under-specification caught
pre-acquisition and fixed in the LOCK, not in code.

WHAT WAS UNDER-SPECIFIED (GAP-A): the VERDICT_MATRIX FALSIFIED row split on "partial
CONFIRMED vs partial null," but H_IL_Presence_Robustness (r1) defined the partial cut
(|rho_partial| < 0.15) ONLY conditioned on the raw-CONFIRMED branch (the attenuation
case). In the raw-FALSIFIED row the partial-CONFIRMED / partial-null boundary was never
pinned and the 0.15-0.30 partial-middle was unmapped -- a REACHABLE cell (this trio is
heavily saturated, so the raw arm can land FALSIFIED while a presence-controlled partial
survives) deciding UNDETERMINED-pending-suppression vs CLEAN NULL, a headline-level
difference. Exactly the unmappable-cell trap this module already invokes by name (v0.36).

WHAT r2 PINS (a completion to design intent already on record -- NOT a verdict change):
  - "partial CONFIRMED" = |rho_partial| >= 0.30 AND p_perm < .05, SYMMETRIC to the
    primary band (CONFIRMED means the same thing on both axes; no second, looser
    threshold introduced).
  - FALSIFIED-row mapping: partial NULL (|rho_partial| < 0.15) -> CLEAN NULL;
    EVERYTHING else (partial CONFIRMED or partial MIDDLE) ->
    UNDETERMINED-pending-suppression-diagnosis.
  - Conservative-direction rationale: under a null raw arm, a partial that is NOT
    ESTABLISHED AS NULL routes to diagnosis (UNDETERMINED), never to a clean negative.
    Only partial-also-null (|rho_partial| < 0.15) is CLEAN NULL. On the partial MIDDLE
    specifically -- including the large-but-not-significant case (|rho_partial| >= 0.30
    with p_perm >= .05) -- the routing is UNDETERMINED rather than CLEAN NULL because
    under a null raw arm we have NO positive evidence the partial is genuinely zero, and
    suppression is precisely the regime where the marginal (raw) test is underpowered
    while the conditional structure is real. Insufficient evidence to establish null
    routes to diagnosis, not to clean-negative. The cell asserts we CANNOT RULE OUT a
    conditional signal -- not that one is established.

GAP-B (folded in): the partial Spearman's inference is pinned to the SAME within-substrate
stratified permutation as the primary (IL-Direct labels permuted within substrate,
>= 10,000 draws, two-sided); the partial METHOD is named (4-variable Spearman
rank-correlation-matrix inversion). Transcription, not a design choice.

GAP-C (recorded, NOT locked): the permutation MC seed is an implementation-determinism
choice pinned IN THE SCORER with a comment, not in this lock. The scorer reports every
permutation p with its Monte Carlo standard error so boundary fragility (any |rho| within
~2 MC-SE of .05) is auditable rather than hidden behind a single draw. This entry records
WHY a bare p is insufficient at the boundary.

SCOPE: this amendment touches H_IL_Presence_Robustness, the VERDICT_MATRIX FALSIFIED row,
and DECISION_RULES only. The PRIMARY H_IL_Consistency bands, the n-floor (45), the sign
convention, LOSO, the supplementary contrast, and Entry 0 COI carry-forward are UNCHANGED.
r1 stays frozen at 2f381f7 as the original lock; r2 is additive.
"""

# ---------------------------------------------------------------------------
# EXTERNAL ANCHOR (D6, binding)
# ---------------------------------------------------------------------------
EXTERNAL_ANCHOR = """
Sequence after content lock:
1. Pathspec-limited commit (enumerated paths only; dirty-tree work excluded).
2. Tag v0.37-prereg-r1 (additive, no force-moves).
3. git push origin v0.37 --tags
4. Upload prereg artifacts to osf.io/ec6wh/v37/prereg/ via osf_upload.py.
5. Verify both remotes resolve.
6. Only then: reconciliation gate, then scoring.
"""

# ---------------------------------------------------------------------------
# Commit guard -- raises if verbatim-conform placeholders remain unresolved.
# ---------------------------------------------------------------------------
if "<<CONFORM-VERBATIM" in DEVIATIONS:
    raise RuntimeError(
        "v0.37 prereg content module: unresolved CONFORM-VERBATIM placeholder "
        "in DEVIATIONS. Pull exact locked COI text from v0.22/v0.19 records "
        "before commit. COMMIT BLOCKED."
    )
