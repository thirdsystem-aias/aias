"""
v1.8 — CPC Instrument Redesign · Pre-registration content (r1)

AIAS™ Measurement Program. This module encodes the LOCKED v1.8 instrument
redesign. It replaces the CV-CPC Consistency measure falsified in v1.7 with a
mean-independent instrument family (phi / J / R_grad) and pre-registers the
validation plan, hypotheses, thresholds, verdict matrix, and falsification
criteria BEFORE any scoring run against the frozen analysis sets.

Instrument family (locked):
  - phi    : primary CPC — quasi-binomial between-model dispersion
             (inconsistency-oriented), computed CHANNEL-AGNOSTICALLY (the six
             probe frames per model pooled to a 0..6 count). Mean-independent by
             construction; defined into the low-recall segment where CV is
             undefined. A per-channel variant is retained as a SECONDARY
             diagnostic on the canonical-channel substrates (v0.20-v0.22).
  - J      : positional diagnostic — mean pairwise Jaccard set-stability
             (consistency-oriented). Captures WHERE a brand surfaces.
  - R_grad : graded recognition (tiered depth), schema-conditional. FORWARD-SPEC
             (frozen recognition channel retains binary verdicts only — see
             DEVIATIONS Entry 0).

Supersedes the v1.7 CV-CPC instrument (SSRN 6878818): pooled |rho(CV-CPC, mu)| =
0.77 > the 0.50 dissociation ceiling; Poisson CV ~ 1/sqrt(mean) coupling at low
recall counts. Not adopted; redefinition escalated here onto a mean-independent
basis.

No acquisition. Frozen-set validation against v0.34 / v0.35 / v0.36; the first
scoring call is the one-way boundary, in place of an API acquisition call. The
external anchor (git tag v1.8-prereg-r1 + OSF deposit) precedes that first
scoring call, per the v0.33+ anchoring discipline.

Revision r4. Lock arc (all pre-scoring; no phi / J values computed): r1
(v1.8-prereg-r1, first lock) specified PER-CHANNEL phi with F=6; r2
(v1.8-prereg-r2) corrected the per-channel frame count to F=3 (Entry 1); r3
(v1.8-prereg-r3) makes phi / J CHANNEL-AGNOSTIC as the primary instrument
(frames pooled 0..6; F = frames_per_model = 6, M*F = 36, phi floor pi_hat =
1/36) and demotes the per-channel variant to a secondary diagnostic on the
canonical-channel substrates v0.20-v0.22 (Entry 2); r4 (v1.8-prereg-r4) adds a
fourth H_LowRecallDefined verdict cell (PARTIAL-STRUCTURAL) for the reachable
gain-holds / saturation-ceiling-breaks-containment outcome the r1-r3 three-cell
matrix left unmapped, and makes the original "implementation flag" PARTIAL an
explicit fail-loud guard (Entry 3). This matches the certified channel-agnostic
omnibus extraction and accommodates v0.23's non-canonical channels
(cultural-cult / editorial-authority).
Upstream lineage: extends
v1.7 (SSRN 6878818); failure cascade v0.32 (6898581), v0.33 (6909019),
v0.34 (6915458), v0.35 (6921758), v0.36 (6927958). Feeds forward to v0.37+
(emergence / typology on the redesigned instrument) and v1.9 (two-component
phi/J composite calibration).
"""

# ---------------------------------------------------------------------------
# Metadata
# ---------------------------------------------------------------------------
METADATA = {
    "version": "v1.8",
    "title": "CPC Instrument Redesign",
    "type": "methodology_lock",
    "component": "CPC",                          # Consistency — instrument redesign
    "extends": "v1.7",                           # SSRN 6878818 (CV-CPC negative result)
    "supersedes_instrument": "CV-CPC",           # falsified v1.7; not adopted
    "revision": "r4",                            # r3 channel-agnostic primary (Entry 2); r4 H_LowRecallDefined 4th cell (Entry 3)
    "prereg_tag": "v1.8-prereg-r4",              # additive; r1/r2/r3 preserved at their tags
    "acquisition": False,                        # frozen-set re-analysis; no probes
    "validation_sets": ["v0.34", "v0.35", "v0.36"],  # frozen; no acquisition
    "one_way_boundary": "first_scoring_call",    # external anchor precedes it
    "register": "academic",                      # paper + figures; report deferred to AIAS 2.0
    "feeds_forward": ["v0.37+", "v1.9"],         # v1.9 = phi/J composite calibration
    # Upstream citations (SSRN-id forward refs; v1.7 extended, v0.32-v0.36 cascade)
    "upstream_citations": {
        "v1.7": "6878818",                       # extends — CV-CPC falsification
        "v0.32": "6898581",
        "v0.33": "6909019",
        "v0.34": "6915458",
        "v0.35": "6921758",
        "v0.36": "6927958",
    },
    # Identity (canonical author block lives in the paper; employer COI disclosed ONLY in paper §COI)
    "author": "Pablo Ulpiano González Castro",
    "affiliation_primary": "School of Visual Arts, MPS Branding Program, New York, NY",
    "affiliation_research": "Third System™ (research entity; data archive and methodology venue)",
    "orcid": "0009-0003-8968-9990",
}

# ---------------------------------------------------------------------------
# Construct
# ---------------------------------------------------------------------------
CONSTRUCT = {
    "name": "Cross-model Presence Consistency (CPC) — redesigned",
    "definition": (
        "Mean-independent stability of a brand's per-model AI surfacing across the fixed "
        "six-model reference panel, pooled across probe frames (channel-agnostic primary); a "
        "per-channel variant is retained as a secondary diagnostic on the canonical-channel "
        "substrates."
    ),
    "primary": "phi",                   # channel-agnostic between-model dispersion (inconsistency-oriented)
    "positional_diagnostic": "J",       # channel-agnostic mean pairwise Jaccard (consistency-oriented)
    "graded_recognition": "R_grad",     # tiered depth; schema-conditional (FORWARD-SPEC)
    "channel_mode": "channel-agnostic (primary): the six probe frames per model pooled to a 0..6 count",
    "secondary_diagnostic": {           # per-channel variant — diagnostic, non-gating
        "what": "per-channel phi / J (R_cat, R_cult separately)",
        "scope": "canonical two-channel substrates only: v0.20, v0.21, v0.22",
        "excludes": (
            "v0.23 (non-canonical channels cultural-cult / editorial-authority; channel-construct "
            "equivalence with R_cat/R_cult was DEFERRED to v0.31 and is unvalidated) AND v0.19 "
            "(single-channel — no R_cat/R_cult split exists)"
        ),
        "status": "reported alongside the channel-agnostic primary; does not gate any verdict",
    },
    "rationale": (
        "The primary instruments are channel-agnostic: the certified omnibus extraction "
        "(score_v0_31 -> 0..6 per model) and all three validation framings are channel-agnostic by "
        "construction, and v0.23's channels (cultural-cult / editorial-authority) are not "
        "commensurable with R_cat / R_cult. phi is mean-independent by construction (it divides out "
        "the binomial-expected variance F*pi(1-pi)), so the channel-mixing LEVEL confound that "
        "originally motivated prohibiting channel pooling is already removed; the residual channel "
        "signal is POSITIONAL, which is J's domain. The per-channel variant is therefore retained "
        "only as a secondary diagnostic where channels are genuinely canonical (v0.20-v0.22). "
        "R_grad reads a graded recognition signal finer than the saturated binary C_P."
    ),
    "supersedes": {
        "instrument": "CV-CPC (CPC_raw = SD/mean; CPC_corr = SD/sqrt(mu*(1-mu)))",
        "reason": (
            "Falsified in v1.7 (SSRN 6878818): pooled |rho(CV-CPC, mu)| = 0.77 > 0.50 ceiling; "
            "Poisson CV ~ 1/sqrt(mean) coupling at low recall counts. Undefined at the low-recall "
            "floor. Not adopted; redefinition escalated to this mean-independent family."
        ),
    },
    "requirements": {
        "mean_independence": "escape the CV ~ 1/sqrt(mean) trap; |rho(phi, mu)| <= 0.50",
        "graded_recognition": (
            "finer than binary C_P (inert under saturation) and NOT the recall mean "
            "(which annihilated the contrast in v0.35)"
        ),
        "low_recall_coverage": "remain computable across the segment where CV is undefined",
    },
}

# ---------------------------------------------------------------------------
# Computation
#   brand b; six-model panel m in {1..M}, M=6; F = 6 probe-frames per model
#   (3 R_cat + 3 R_cult), POOLED channel-agnostically for the primary instrument;
#   binary surfacing per (model, frame); per-model count k(b,m) in {0..F};
#   pooled rate pi_hat_b = sum_m k(b,m) / (M*F), M*F = 36. The per-channel
#   SECONDARY diagnostic uses F = frames_per_channel = 3 (M*F = 18) on v0.20-v0.22.
# ---------------------------------------------------------------------------
COMPUTATION = {
    "panel_n": 6,                        # M, fixed six-model panel
    "frames_per_model": 6,               # F (PRIMARY) — channel-agnostic frames per model; M*F = 36
    "frames_per_channel": 3,             # F (SECONDARY per-channel diagnostic); M*F = 18, on v0.20-v0.22 only
    "channel_mode": "channel-agnostic (primary): 6 frames pooled to 0..6 per model",
    "surfacing": "binary_per_model_frame",
    "per_model_count": "k(b,m) in 0..F  (F = frames_per_model = 6; channel-agnostic primary)",
    "pooled_rate": "pi_hat_b = sum_m k(b,m) / (M*F); F = frames_per_model = 6, so M*F = 36 (channel-agnostic primary)",
    "rho": "spearman",                   # program convention
    "pooling": "per-set, then pooled with set as a blocking factor; per-set rho reported alongside pooled",

    # --- phi: primary CPC — quasi-binomial between-model dispersion (Pearson chi2/df) ---
    "phi": {
        "formula": "phi_b = [1/(M-1)] * sum_m (k(b,m) - F*pi_hat_b)^2 / [F*pi_hat_b*(1-pi_hat_b)]  (F = frames_per_model = 6, channel-agnostic primary)",
        "df": "M-1",
        "null_expectation": 1.0,         # E[phi]=1 under homogeneity (all models share pi_hat)
        "interpretation": "phi>1 -> models disagree (inconsistent); phi<1 -> agree beyond chance (consistent)",
        "mean_independent": True,        # denominator divides out binomial variance F*pi(1-pi)
        "defined_domain": "pi_hat in (0,1)  (>=1 surfacing, not full saturation)",
        "undefined_only_at": "true-zero floor (correct behavior; not a CV-style blowup)",
        "low_recall_note": "a brand surfacing once total (pi_hat = 1/36: one surfacing across 6 models x 6 frames, channel-agnostic) still yields a finite phi",
    },

    # --- per-channel SECONDARY diagnostic (non-gating; canonical-channel substrates only) ---
    "per_channel_secondary": {
        "channels": ["R_cat", "R_cult"],    # computed separately
        "F": 3,                             # frames_per_channel; M*F = 18 per channel
        "scope": "v0.20, v0.21, v0.22 (canonical R_cat/R_cult)",
        "excludes": "v0.23 (non-canonical channels) and v0.19 (single-channel; no R_cat/R_cult split)",
        "status": "diagnostic only; not gating; reported alongside the channel-agnostic primary",
    },

    # --- J: positional diagnostic — mean pairwise Jaccard (channel-agnostic primary) ---
    "J": {
        "set": "S(b,m) = { frames where b surfaced under model m }",
        "formula": "J_b = mean over model pairs (m,m') of |S(b,m) intersect S(b,m')| / |S(b,m) union S(b,m')|",
        "range": "[0,1]",
        "interpretation": "J=1 -> every model surfaces b in identical frames (positionally consistent); J->0 disjoint",
        "defined_domain": ">=1 surfacing across >=2 models",
        "small_set_contingency": {       # pre-specified, LOCKED — not post-hoc
            "trigger": "|rho(J, mu)| > 0.50 from small-set bias",
            "fallback": "chance-corrected J_adj = (J - E[J|sizes]) / (1 - E[J|sizes])",
        },
    },

    # --- R_grad: graded recognition — tiered depth (schema-conditional) ---
    "R_grad": {
        "tiers": {
            0: "not recognized",
            1: "name",
            2: "name + correct category",
            3: "name + category + >=1 correct attribute",
        },
        "formula": "R_grad_b = mean_m D(b,m) in [0,3]",
        "source": "recognition probe (NOT recall — sidesteps the v0.35 recall-mean over-control)",
        "schema_conditional": "tiers 2-3 require the frozen recognition channel to retain re-scorable response text",
        "status_r1": "FORWARD-SPEC",     # frozen v0.34-v0.36 channel is binary-only (DEVIATIONS Entry 0)
    },

    "rejected_instrument": {
        "CV-CPC": "mean-coupled (|rho|=0.77, v1.7); undefined at low recall; falsified, not adopted",
    },
}

# ---------------------------------------------------------------------------
# Thresholds (decision constants; read by the v1.8 scorer)
# ---------------------------------------------------------------------------
THRESHOLDS = {
    "mean_independence_ceiling": 0.50,        # H_MeanIndependent: |rho(phi, mu)| <= 0.50  (MAKE-OR-BREAK)
    "cv_reproduces_floor": 0.50,              # H_CV_Reproduces:   |rho(CV-CPC, mu)| >= 0.50 (manipulation check)
    "positional_dissociation_ceiling": 0.70,  # H_PositionalDissociation: |rho(phi, J)| <= 0.70
    "graded_recognition_ceiling": 0.50,       # H_GradedRecognition: |rho(R_grad, mu)| <= 0.50
    "J_small_set_trigger": 0.50,              # |rho(J, mu)| > this -> switch to chance-corrected J_adj
    "low_recall_defined_target": 1.00,        # H_LowRecallDefined: phi defined for 100% of >=1-surfacing brands
    "make_or_break": "H_MeanIndependent",     # if |rho(phi,mu)| > 0.50 pooled, phi cannot lock
    "escalation_path": "beta-binomial ICC / overdispersion rho, re-entered before any instrument lock",
}

# ---------------------------------------------------------------------------
# Hypotheses (six; tiered)
# ---------------------------------------------------------------------------
HYPOTHESES = [
    {
        "id": "H_CV_Reproduces",
        "tier": "baseline / manipulation check",
        "statement": "CV-CPC's mean-coupling reproduces on the frozen sets.",
        "confirmed_threshold": "|rho(CV-CPC, mu)| >= 0.50, in the v1.7 neighborhood",
        "directional_lean": "CONFIRMED",
        "figure": "fig_01_mean_independence",
    },
    {
        "id": "H_MeanIndependent",
        "tier": "PRIMARY",
        "make_or_break": True,
        "statement": "phi is mean-independent.",
        "confirmed_threshold": "|rho(phi, mu)| <= 0.50, pooled across sets",
        "directional_lean": "CONFIRMED (risk: floor effects reintroduce coupling)",
        "figure": "fig_01_mean_independence",
    },
    {
        "id": "H_LowRecallDefined",
        "tier": "PRIMARY",
        "statement": "phi extends defined coverage into the low-recall segment.",
        "confirmed_threshold": (
            "phi defined for 100% of >=1-surfacing brands AND the phi-defined set strictly "
            "contains the CV-CPC-defined set, with the gain concentrated in the low-recall stratum"
        ),
        "directional_lean": "CONFIRMED",
        "figure": "fig_02_defined_coverage",
    },
    {
        "id": "H_GradedRecognition",
        "tier": "PRIMARY*",   # PRIMARY if frozen recognition is re-scorable; else FORWARD-SPEC
        "status_r1": "FORWARD-SPEC",   # see DEVIATIONS Entry 0
        "statement": "tiered R_grad discriminates under C_P saturation and is not the recall mean in disguise.",
        "confirmed_threshold": (
            "among C_P = M brands: Var(R_grad) > 0 spanning >=2 tiers AND |rho(R_grad, mu)| <= 0.50"
        ),
        "directional_lean": "CONFIRMED if re-scorable; else FORWARD-SPEC",
        "figure": None,   # no empirical figure in r1 (forward-spec)
    },
    {
        "id": "H_PositionalDissociation",
        "tier": "SECONDARY",
        "statement": "phi and J capture distinct facets.",
        "confirmed_threshold": "|rho(phi, J)| <= 0.70 AND >=1 identified discordant brand",
        "directional_lean": "CONFIRMED (positional vs magnitude facet; per-channel asymmetry is the secondary-diagnostic view)",
        "figure": "fig_03_phi_j_dissociation",
    },
    {
        "id": "H_PhantomSignature",
        "tier": "TERTIARY (exploratory)",
        "statement": (
            "near-phantom (>=1-surfacing) brands carry a distinct phi / J signature vs the "
            "v0.35 84-unit baseline."
        ),
        "confirmed_threshold": "no directional commitment",
        "directional_lean": "exploratory",
        "figure": "fig_04_per_set_rho",
    },
]

# ---------------------------------------------------------------------------
# Verdict matrix — exhaustive reachable outcome space per hypothesis
# (v0.36 institutional rule: every reachable outcome mapped; no unmapped residual)
# ---------------------------------------------------------------------------
VERDICT_KEYS = {
    "H_CV_Reproduces": [
        "CONFIRMED (|rho| >= 0.50)",
        "NULL (|rho| < 0.50 — data artifact; invalidates the comparison)",
    ],
    "H_MeanIndependent": [
        "CONFIRMED (|rho| <= 0.50)",
        "FALSIFIED (|rho| > 0.50)",
    ],
    "H_LowRecallDefined": [
        "CONFIRMED (full recovery; 100% phi-defined among >=1-surfacing AND phi-defined strictly contains CV-CPC_raw-defined AND non-empty low-recall gain)",
        "PARTIAL-IMPLEMENTATION (a residual >=1-surfacing brand is undefined for a reason OTHER than the saturation ceiling — an implementation defect; structurally unreachable given phi totality on (0,1); retained as a fail-loud guard)",
        "FALSIFIED (no gain over the CV-CPC_raw-defined set — vacuous extension)",
        "PARTIAL-STRUCTURAL (low-recall gain confirmed, but strict containment is broken SOLELY by the by-design pi_hat=1 ceiling exclusion: phi undefined at the ceiling where CV-CPC_raw is defined, so the two defined sets are non-nested; a structural property of the instrument pair, not a defect)",
    ],
    "H_GradedRecognition": [
        "CONFIRMED (variance under saturation + distinct from mu)",
        "FALSIFIED-circular (variance but |rho(R_grad, mu)| > 0.50)",
        "FALSIFIED-degenerate (no variance under saturation)",
        "FORWARD-SPEC (frozen data not re-scorable)",
    ],
    "H_PositionalDissociation": [
        "CONFIRMED (non-redundant + discordants exist)",
        "PARTIAL (|rho| <= 0.70 but no discordant brand)",
        "FALSIFIED (|rho| > 0.70 — redundant)",
    ],
    "H_PhantomSignature": [
        "SIGNATURE-PRESENT",
        "NULL",
        "UNDETERMINED (insufficient non-zero phantoms)",
    ],
}

# ---------------------------------------------------------------------------
# Pipeline integration
# ---------------------------------------------------------------------------
INTEGRATION = {
    "computed_in": "scoring_step",       # score_v1_8.py (to be authored) reads COMPUTATION + THRESHOLDS
    "inputs": "frozen Phase B response_text over the v0.19-v0.23 omnibus (the shared basis of v0.34 / v0.35 / v0.36); binary surfacing is DERIVED, not pre-deposited",
    "surfacing_extraction": (
        "channel-agnostic per-model 0..6 counts via the certified omnibus lineage "
        "(score_v0_31.counts_v19/v23 + score_v20/21/22 detect_mention, orchestrated as in score_v33, "
        "with its reconciliation gate); the per-channel secondary diagnostic re-runs the certified "
        "matcher per channel on v0.20-v0.22 only"
    ),
    "reacquisition_required": False,
    "one_way_boundary": "first scoring call (in place of an API acquisition call); external anchor precedes it",
    "replaces": "v1.7 CV-CPC instrument",
    "composition_in_v1_8": False,        # no phi/J composition performed here (that is v1.9)
    "feeds_forward": [
        "v0.37+ (emergence / typology on the redesigned instrument)",
        "v1.9 (two-component phi/J composite calibration)",
    ],
    "typology_deferred_to": "a later emergence lock, run on the redesigned instrument",
    "graded_recognition_validation_deferred_to": (
        "a fresh-collection phase (v0.32 / v0.28 are the program's retained re-scorable-text corpora)"
    ),
    "make_or_break_escalation": "beta-binomial ICC / overdispersion rho",
    "no_verdict_before": "osf/methodology/v1_8/v1_8_verdicts.json (no figures or copy precede the verdicts JSON)",
}

# ---------------------------------------------------------------------------
# Illustration boundary — synthetic worked cases (for exposition only)
# ---------------------------------------------------------------------------
ILLUSTRATION = {
    "scope": "instrument_exposition_only",
    "note": (
        "Illustrative / synthetic worked cases for exposition — NOT drawn from the frozen sets and "
        "NOT data. They show the two failure modes the phi / J family fixes, and assign no verdicts."
    ),
    "cases": [
        {
            "id": "low_recall_finite_phi",
            "label": "illustrative / synthetic",
            "setup": "low-recall brand surfacing once total, pi_hat = 1/36 (channel-agnostic: one across 6 models x 6 frames)",
            "cv_cpc": "undefined / explosive (1/sqrt(mean) blowup)",
            "phi": "finite and defined",
            "demonstrates": "coverage gain — phi covers the low-recall segment CV cannot (H_LowRecallDefined)",
        },
        {
            "id": "positional_dissociation",
            "label": "illustrative / synthetic",
            "setup": "brand with equal between-model surfacing magnitude but divergent frame positions across models",
            "phi": "magnitude facet (between-model dispersion) — agreement, so phi is low",
            "J": "positional facet (which frames) — disagreement, so J is low",
            "demonstrates": (
                "phi (magnitude) and J (positional) dissociate channel-agnostically — facets non-redundant "
                "(H_PositionalDissociation); per-channel R_cat/R_cult asymmetry is the secondary-diagnostic "
                "view of the same effect"
            ),
        },
    ],
}

# ---------------------------------------------------------------------------
# Figures — PLANNED specs only (built post-scoring; placeholders now)
#   path stem: reports/figs/v1_8/chart_NN_<topic>.pdf
# ---------------------------------------------------------------------------
FIGURES = [
    {
        "path": "reports/figs/v1_8/chart_01_mean_independence.pdf",
        "caption": (
            "phi-vs-mu mean-independence (|rho(phi, mu)| <= 0.50) contrasted against CV-CPC-vs-mu at "
            "the v1.7 rho = 0.77. HEADLINE."
        ),
        "label": "fig_01_mean_independence",
    },
    {
        "path": "reports/figs/v1_8/chart_02_defined_coverage.pdf",
        "caption": (
            "Defined coverage of phi vs CV-CPC across the recall range; gain concentrated in the "
            "low-recall stratum."
        ),
        "label": "fig_02_defined_coverage",
    },
    {
        "path": "reports/figs/v1_8/chart_03_phi_j_dissociation.pdf",
        "caption": "phi-vs-J scatter; |rho| annotated; discordant brands flagged.",
        "label": "fig_03_phi_j_dissociation",
    },
    {
        "path": "reports/figs/v1_8/chart_04_per_set_rho.pdf",
        "caption": "Per-set rho panel across v0.34 / v0.35 / v0.36 (catches set-dependence; the v0.32 lesson).",
        "label": "fig_04_per_set_rho",
    },
]

# ---------------------------------------------------------------------------
# DEVIATIONS — contemporaneous log (additive; Entry 0 at r1 lock, Entry 1 r1->r2, Entry 2 r2->r3)
# ---------------------------------------------------------------------------
DEVIATIONS = [
    {
        "entry": 0,
        "type": "pre-scoring feasibility resolution (no phi / J / R_grad values computed)",
        "summary": (
            "A pre-scoring feasibility check on the frozen recognition channel resolves "
            "H_GradedRecognition along its pre-committed FORWARD-SPEC branch for r1. Tiers 2-3 of "
            "R_grad require re-scorable recognition response text; the frozen v0.34 / v0.35 / v0.36 "
            "lock retains binary recognition only (hash-sealed at v0.35) — no re-scorable text is "
            "retained. Per spec section 2.3, R_grad is therefore DEFINED here and validated in a "
            "designated later fresh-collection phase (v0.32 and v0.28 are the program's retained "
            "re-scorable-text corpora). The exploratory audit "
            "osf/v33/exploratory/v33_recognition_source_audit.json confirms the recognition "
            "saturation is REAL (v0.23 r_level uniformly R3), not a binarization artifact, so the "
            "deferral reflects data availability rather than an instrument defect. v1.8's empirical "
            "results reduce to phi + J — a clean, honest outcome. Resolved before any computation; "
            "not a methodology change and not result-driven."
        ),
    },
    {
        "entry": 1,
        "amendment": "r1 -> r2",
        "type": "pre-scoring methodology correction (no phi / J / R_grad values computed)",
        "summary": (
            "Pre-scoring methodology correction, caught before the one-way boundary (no phi/J "
            "computed). r1 specified frames_per_model = 6 and a phi low-recall floor pi_hat = "
            "1/36, but the frozen v0.34 Phase B acquisition has F = 3 frames per channel "
            "(q1-q3 -> R_cat, q4-q6 -> R_cult; 6 per model total). Because all instruments are "
            "computed per channel (channel_pooling prohibited), the per-channel phi denominator "
            "uses F = 3, M*F = 18, and the minimum non-zero per-channel pi_hat = 1/18. The r1 "
            "figures assumed 6 frames within a channel; corrected here. Same defect class as "
            "v1.7's r3 frames-per-channel amendment. No hypotheses or thresholds change (all "
            "F-independent); only the phi normalization constant and the ILLUSTRATION / "
            "low-recall-note figures. The per-channel mandate is the binding design; the r1 "
            "F=6 / pi_hat=1/36 figures were the arithmetic outlier, now reconciled."
        ),
    },
    {
        "entry": 2,
        "amendment": "r2 -> r3",
        "type": "pre-scoring design correction (no phi / J / R_grad values computed)",
        "summary": (
            "Pre-scoring design correction, caught before the one-way boundary (no phi/J computed). "
            "r1 and r2 both specified PER-CHANNEL phi/J (R_cat, R_cult separately; channel pooling "
            "prohibited). Inspecting the frozen omnibus channel structure exposed an internal "
            "contradiction: the validation sets span v0.19-v0.23, but v0.23's two channels are "
            "cultural-cult / editorial-authority, NOT R_cat / R_cult, so a per-channel R_cat/R_cult "
            "instrument cannot span the stated omnibus; and v0.19 is single-channel (no R_cat/R_cult "
            "split at all), so TWO of the five substrates break the per-channel framing. Mapping "
            "v0.23's channels onto R_cat/R_cult is "
            "the channel-construct equivalence v1.7 explicitly DEFERRED to v0.31 as unvalidated, and "
            "was rejected. r3 resolves the contradiction by making phi / J CHANNEL-AGNOSTIC as the "
            "PRIMARY instrument: the six frames per model are pooled to a 0..6 count (F = "
            "frames_per_model = 6, M*F = 36, phi floor pi_hat = 1/36), matching the certified "
            "channel-agnostic omnibus extraction (score_v0_31 -> 0..6 per model) on which all three "
            "framings (v0.34 / v0.35 / v0.36) and v1.7's own CV-CPC were already built. The "
            "per-channel variant is retained as a SECONDARY, non-gating diagnostic on the "
            "canonical-channel substrates v0.20-v0.22 only. Justification that this is not a loss: "
            "phi is mean-independent by construction, so the channel-mixing LEVEL confound that "
            "originally motivated prohibiting pooling is already divided out; the residual channel "
            "signal is positional, which is J's domain. Honest record of the arc: r1's F=6 was the "
            "right number for the wrong reason (it assumed 6 frames per channel); r2 corrected F to 3, "
            "which was correct FOR a per-channel instrument but the per-channel framing was itself the "
            "error — it was specified from the out-of-sample v0.24 channel structure, not verified "
            "against the v0.19-v0.23 omnibus the framings are built on. r3 restores F=6 for the "
            "correct reason (channel-agnostic pooling, 6 frames per model). Root cause: locked (r1) "
            "and amended (r2) before inspecting the omnibus channel structure. No thresholds change "
            "(all F-independent); the primary instrument's channel mode, F, M*F, and the phi floor / "
            "ILLUSTRATION figures change. All five substrates are retained channel-agnostically; the "
            "'even v0.19 raw recognition is binary' note (corroborating Entry 0) goes to the paper's "
            "methods, not a further lock bump."
        ),
    },
    {
        "entry": 3,
        "amendment": "r3 -> r4",
        "type": "pre-scoring verdict-matrix exhaustiveness correction (no phi / J / R_grad values computed)",
        "summary": (
            "Pre-scoring, pre-boundary verdict-matrix correction, reasoned from the instrument's "
            "mathematical structure with the one-way boundary intact (no phi/J computed; surfaced "
            "during scorer construction). The r1-r3 H_LowRecallDefined matrix had three cells "
            "{CONFIRMED, PARTIAL (residual undefined - implementation flag), FALSIFIED}. Working the "
            "instrument domains exposed a reachable outcome with no truthful cell: phi is TOTAL on "
            "pi_hat in (0,1), so the ONLY >=1-surfacing brand that can lack a phi is one at the "
            "pi_hat=1 ceiling (a by-design Fork-A exclusion); meanwhile CV-CPC_raw carries v1.7's "
            "MU_FLOOR and stays defined at the ceiling. So when the low-recall gain holds AND a "
            "ceiling brand exists, the phi-defined and CV-CPC_raw-defined sets are non-nested -> "
            "strict containment breaks. That outcome cannot be CONFIRMED (forbids residual), is not "
            "FALSIFIED (gain exists), and the only PARTIAL cell named it an 'implementation flag' - "
            "but the sole reachable trigger is the structural ceiling, which that wording misnames. "
            "r4 adds a fourth cell, PARTIAL-STRUCTURAL, for exactly this non-nested-by-design "
            "outcome, and re-scopes the original PARTIAL to PARTIAL-IMPLEMENTATION: a residual "
            "undefined for a NON-ceiling reason, which is structurally impossible given phi's "
            "totality and is therefore retained only as a fail-loud guard (it firing would mean an "
            "extraction/phi bug, not a legitimate partial). The CONFIRMED condition and the "
            "make-or-break bar (H_MeanIndependent) are UNCHANGED; r4 refines only the partial region. "
            "Root cause: the r1-r3 matrix was specified before the phi-totality / saturation-ceiling "
            "/ MU_FLOOR interaction was fully worked through. This is pre-registration refinement "
            "reasoned from logically reachable outcomes of the instrument math, not result-tuning - "
            "no data was peeked at; the boundary holds."
        ),
    },
]
