# ---------------------------------------------------------------------------
# AIAS(TM) v0.35 -- Naive-Phantom x CPC -- PRE-REGISTRATION CONTENT (LOCK CANDIDATE)
# Phase type: re-analysis (no new LLM acquisition; v0.33 pattern)
# Lock tag: v0.35-prereg-r1
#
# NOTE TO OPERATOR (Claude Code): before commit, resolve every
# <<CONFORM-VERBATIM: ...>> placeholder by pulling the EXACT locked text from
# the named source record. Do not paraphrase. The guard at the bottom of this
# file raises if any placeholder remains.
# ---------------------------------------------------------------------------

PHASE_ID = "v0.35"
PHASE_TITLE = "Naive-Phantom x CPC: Do Phantom-Flagged Brands Carry a Distinct Consistency Signature?"

# ---------------------------------------------------------------------------
# DESIGN
# ---------------------------------------------------------------------------
DESIGN = """
Re-analysis, no new LLM acquisition (v0.33 pattern). Inputs are the frozen
per-brand t1 quantities: per-brand CV-CPC, per-brand C_P (v1.6), per-brand
recall-mean, and the frozen phantom-flag classification, across the five
omnibus substrates -- v0.19 audiophile headphones (16 brands), v0.20 skincare
(24), v0.21 cosmetics (24), v0.22 automotive (24), v0.23 premium spirits (24);
112 brand units; canonical 6-model t1 panel.

Output: osf/v35/v35_verdicts.json.
"""

# ---------------------------------------------------------------------------
# METRIC DEFINITION (pinned)
# ---------------------------------------------------------------------------
METRIC_DEFINITION = """
CV-CPC = 1/(1+CV) of the per-model recall vector, exactly per the v1.7
computation (SSRN 6878818). Higher CV-CPC = greater cross-model consistency.

CV-CPC is used strictly as a characterization quantity, not an adopted
Consistency instrument, per the v1.7 negative result.

Mechanical note (pinned at lock): CV scales approximately as 1/sqrt(mean) at
low recall, so low-recall units mechanically depress CV-CPC. This is the
contamination the gating hypothesis exists to handle.
"""

# ---------------------------------------------------------------------------
# PHANTOM CLASSIFICATION (locked, no re-derivation)
# ---------------------------------------------------------------------------
PHANTOM_CLASSIFICATION = """
Method anchor: Phantom Brand Persistence as locked at v1.6 (SSRN 6816340) and
instantiated in the substrate phases (v0.19-v0.23).

Operational input: the frozen recall-floor flags as archived in the v0.31 OSF
deposit -- consumed as data provenance only; v0.31 (WITHDRAWN) is not cited as
methodological authority. These are the identical flags consumed by v0.33's
H_Provider_Phantom and v0.34's t1 phantom set. Zero judgment calls at analysis
time.

Lineage note: the Naive-Phantom construct traces to the v1.0 stability study;
operational anchoring here is strictly the frozen flags.
"""

# ---------------------------------------------------------------------------
# PROVENANCE FORWARD-NOTE (resolves the v0.31<->v0.32 framing thread)
# ---------------------------------------------------------------------------
PROVENANCE_FORWARD_NOTE = """
The paper's provenance section states the consumption convention explicitly:
the v0.31 frozen per-model inputs remain valid archived data; the v0.31 paper
is withdrawn; CV-CPC's methodological status is fixed by v1.7 (computation
defined; instrument not adopted), and all downstream phases (v0.32-v0.35)
consume the quantity under that status.
"""

# ---------------------------------------------------------------------------
# INPUT RECONCILIATION GUARDRAIL (binding)
# ---------------------------------------------------------------------------
RECONCILIATION_GUARDRAIL = """
Gate, run after lock and before any contrast is computed:

1. Consumed CV-CPC and C_P vectors must reproduce the v0.33-deposited values
   bit-for-bit (hash check).
2. v0.20 / v0.21 / v0.22 vectors must reconcile to the v1.7 r_per_model column
   per the v0.33 anchor-scope convention (scope limited to those three phases).

Reconciliation failure halts the phase.
"""

# ---------------------------------------------------------------------------
# PHANTOM ENUMERATION + ATTRITION (computed before any contrast)
# ---------------------------------------------------------------------------
ENUMERATION_ATTRITION = """
Scoring step 1 enumerates phantom-flagged units per substrate from the frozen
flags and writes the roster to osf/v35/data/v35_phantom_roster.csv before any
contrast is computed.

Units with all-zero recall vectors have undefined CV under v1.7 and are
excluded; the analysis set is phantom-flagged units with computable CV-CPC.
Attrition (flagged vs. analyzable) is reported per substrate.

Pre-registered bias direction: the exclusion drops the most mechanically-
extreme phantoms, pulling the analyzable phantom set toward non-phantoms in
recall -- conservative (attenuating) for the raw arm; UNSIGNED for the
residualized gate, where it is reported as a stated limitation.

Eligibility floor: >= 4 analyzable phantom units for the per-substrate test;
below-floor substrates enter pooled analysis only.
"""

# ---------------------------------------------------------------------------
# HYPOTHESES
# ---------------------------------------------------------------------------
HYPOTHESES = """
H_Phantom_CPC_Signature -- PRIMARY (raw arm; manipulation check).
Phantom vs. non-phantom contrast on CV-CPC. Statistic: pooled Cliff's delta,
permutation strata within substrate (labels shuffled within substrate only),
>= 10,000 Monte Carlo draws, TWO-SIDED.
  CONFIRMED:  |delta| >= 0.30, p < 0.05.
  FALSIFIED:  |delta| < 0.15, or sign opposite the mechanistic annotation at
              p < 0.05.
  Otherwise MARGINAL.
Mechanistic annotation (descriptive only, not a confirmatory direction):
mechanism predicts phantoms LOWER CV-CPC.
Inferential weight statement (pinned): both sides of this contrast are
recall-coupled by construction (flag from recall-floor; metric from
recall-mean), so a raw CONFIRMED is treated as a manipulation check confirming
the pipeline reproduces the known mechanical coupling -- not as evidence of a
Consistency-flavored phantom signature. The phase's inferential claim rests
entirely on the gate.

H_Phantom_Beyond_Presence -- PRIMARY, gating.
Residualize CV-CPC on C_P within substrate (rank-based); identical pooled
Cliff's delta + stratified permutation on residuals, two-sided.
  CONFIRMED:  |delta_resid| >= 0.30, p < 0.05.
  FALSIFIED:  |delta_resid| < 0.15.
  Otherwise MARGINAL.
Co-primary control sensitivity (BINDING): the identical procedure
residualized on recall-mean directly. The gate verdict is reported as stable
only if both controls agree; if the verdict flips between the C_P control and
the recall-mean control, the gate is reported UNDETERMINED and the flip itself
is reported as the finding, routed to v1.8.
Directional pre-commitment: lean FALSIFIED-or-marginal (rho = 0.77
Presence-coupling, v1.7; v0.34 residual findings). Either outcome feeds
v1.8's mean-independence requirement.

H_Phantom_Cross_Substrate -- SECONDARY.
Sign consistency of per-substrate delta across eligible substrates (>= 4
analyzable-phantom floor). Exact binomial sign test. Pre-registered as
underpowered at the substrate level (v0.33 ordinal convention); the
per-substrate delta table is reported regardless of verdict.

H_Phantom_t2_Stability -- TERTIARY, exploratory, walled.
Same pooled contrasts computed on the v0.34 t2 wave as a TEST-RETEST STABILITY
CHECK (t2 is a near-replica panel: 0.98 phantom persistence per v0.34; no
independence claimed). Descriptive only; no confirmatory threshold;
quarantined from PRIMARY verdict logic. v0.33/v0.34 tertiary phantom
observations are motivation only, never confirmatory evidence.
"""

# ---------------------------------------------------------------------------
# SENSITIVITY
# ---------------------------------------------------------------------------
SENSITIVITY = """
PRIMARY robustness: leave-one-substrate-out (LOSO) on both PRIMARY verdicts;
a verdict that does not survive LOSO is reported fragile / UNDETERMINED
(v0.32 precedent).

Threshold sensitivity: rerun PRIMARY at delta thresholds 0.20 and 0.40,
reported descriptively.

Pre-acknowledged: on fixed data the 0.15-0.30 MARGINAL band is wide and
MARGINAL is a plausible modal outcome; honestly-indeterminate is a publishable
result routed to v1.8.
"""

# ---------------------------------------------------------------------------
# DEVIATIONS
# ---------------------------------------------------------------------------
DEVIATIONS = """
Entry 0 -- COI carry-forward (conformed VERBATIM from locked source records):
v0.35 reuses the v0.19-v0.23 registries and inherits their COI screen.

  v0.22 SS-COI tier-2/3 disclosure (conformed from v0.22 locked Declarations
  Sec. COI, papers/v0_22/v0_22_ssrn_paper_draft.md; screened in v0.22 DEVIATIONS
  Entry 0 Part B):
  Samsung subsidiaries hold tier-2/3 component supply relationships with several
  brands in the registry: Harman International (audio systems), Samsung SDI
  (battery cells), and Samsung Display (infotainment). These are non-competitive
  supply relationships; Samsung Electronics America does not produce or market
  passenger car brands and has no brand-level competitive overlap with any
  registry entry. No operational restriction on registry composition was imposed.

  v0.19 AKG -> Denon substitution record (conformed from osf/v19/
  PRE_REGISTRATION_v0_19.md Sec. 2.3 + Declaration; recorded in v0.19 DEVIATIONS
  Entry 1 and Sec. 5 of the v0.19 SSRN paper):
  AKG was substituted with Denon before the v0.19 pre-reg lock (AKG owned by
  Harman International, a Samsung subsidiary, since 2016) to avoid any appearance
  of conflict. The substitution preserved Cell A_Heritage's eight-brand
  composition and occurred prior to lock; it was AKG only (not JBL).

Entry 1 -- Scaffold trim:
v0.34 two-wave acquisition scaffolding removed; v0.35 is a no-acquisition
re-analysis. Scaffold artifact, not a methodology amendment.
"""

# ---------------------------------------------------------------------------
# EXTERNAL ANCHOR (D6, binding)
# ---------------------------------------------------------------------------
EXTERNAL_ANCHOR = """
Sequence after content lock:
1. Pathspec-limited commit (enumerated paths only; dirty-tree work excluded).
2. Tag v0.35-prereg-r1 (additive, no force-moves).
3. git push origin v0.35 --tags
4. Upload prereg artifacts to osf.io/ec6wh/v35/prereg/ via osf_upload.py.
5. Verify both remotes resolve.
6. Only then: reconciliation gate, then scoring.
"""

# ---------------------------------------------------------------------------
# Commit guard -- raises if verbatim-conform placeholders remain unresolved.
# ---------------------------------------------------------------------------
if "<<CONFORM-VERBATIM" in DEVIATIONS:
    raise RuntimeError(
        "v0.35 prereg content module: unresolved CONFORM-VERBATIM placeholder "
        "in DEVIATIONS. Pull exact locked COI text from v0.22/v0.19 records "
        "before commit. COMMIT BLOCKED."
    )
