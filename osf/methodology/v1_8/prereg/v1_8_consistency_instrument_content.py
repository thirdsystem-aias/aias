"""
v1.8 — CPC Instrument Redesign · Pre-registration content (r1)

AIAS™ Measurement Program. This module encodes the LOCKED v1.8 instrument
redesign. It replaces the CV-CPC Consistency measure falsified in v1.7 with a
mean-independent instrument family (phi / J / R_grad) and pre-registers the
validation plan, hypotheses, thresholds, verdict matrix, and falsification
criteria BEFORE any scoring run against the frozen analysis sets.

Instrument family (locked):
  - phi    : primary CPC — quasi-binomial between-model dispersion
             (inconsistency-oriented). Mean-independent by construction; defined
             into the low-recall segment where CV is undefined.
  - J      : positional diagnostic — mean pairwise Jaccard set-stability
             (consistency-oriented). Captures WHERE a brand surfaces.
  - R_grad : graded recognition (tiered depth), schema-conditional. FORWARD-SPEC
             in r1 (frozen recognition channel retains binary verdicts only —
             see DEVIATIONS Entry 0).

Supersedes the v1.7 CV-CPC instrument (SSRN 6878818): pooled |rho(CV-CPC, mu)| =
0.77 > the 0.50 dissociation ceiling; Poisson CV ~ 1/sqrt(mean) coupling at low
recall counts. Not adopted; redefinition escalated here onto a mean-independent
basis.

No acquisition. Frozen-set validation against v0.34 / v0.35 / v0.36; the first
scoring call is the one-way boundary, in place of an API acquisition call. The
external anchor (git tag v1.8-prereg-r1 + OSF deposit) precedes that first
scoring call, per the v0.33+ anchoring discipline.

Revision r2. r1 (v1.8-prereg-r1) was the first lock; r2 (v1.8-prereg-r2) is a
pre-scoring methodology-defect correction — the per-channel frame count F was
mis-specified as 6 and is corrected to 3 against the frozen v0.34 Phase B
structure (3 frames/channel; 6/model total), so per-channel M*F = 18 and the
phi low-recall floor is pi_hat = 1/18 (DEVIATIONS Entry 1; no values computed).
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
    "revision": "r2",                            # r1 first lock; r2 = pre-scoring F-correction (Entry 1)
    "prereg_tag": "v1.8-prereg-r2",              # additive; r1 = v1.8-prereg-r1 (first lock)
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
        "six-model reference panel, measured separately per channel."
    ),
    "primary": "phi",                   # quasi-binomial between-model dispersion (inconsistency-oriented)
    "positional_diagnostic": "J",       # mean pairwise Jaccard set-stability (consistency-oriented)
    "graded_recognition": "R_grad",     # tiered depth; schema-conditional (FORWARD-SPEC in r1)
    "per_channel": ["R_cat", "R_cult"], # computed separately; channel reported as a factor
    "channel_pooling": "prohibited",    # pooling blends challenger/incumbent asymmetry -> confound
    "rationale": (
        "Challengers populate the cultural channel and incumbents the category channel; "
        "pooling channels would reintroduce that asymmetry as a confound. phi divides out the "
        "binomial-expected variance F*pi(1-pi), so consistency no longer reparametrizes recall "
        "level (the v1.7 CV failure). J reads the positional facet phi cannot see; R_grad reads "
        "a graded recognition signal finer than the saturated binary C_P."
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
#   brand b; six-model panel m in {1..M}, M=6; 6 probe-frames per model total =
#   3 R_cat + 3 R_cult, so F = frames_per_channel = 3 (the phi normalization
#   constant, since instruments are computed per channel); binary surfacing per
#   (model, frame); per-model count k(b,m) in {0..F}; pooled rate
#   pi_hat_b = sum_m k(b,m) / (M*F), M*F = 6*3 = 18 PER CHANNEL.
# ---------------------------------------------------------------------------
COMPUTATION = {
    "panel_n": 6,                        # M, fixed six-model panel
    "frames_per_model": 6,               # TOTAL frames per model = 3 R_cat + 3 R_cult
    "frames_per_channel": 3,             # F — the phi normalization constant (instruments per channel); M*F = 18
    "surfacing": "binary_per_model_frame",
    "per_model_count": "k(b,m) in 0..F  (F = frames_per_channel = 3)",
    "pooled_rate": "pi_hat_b = sum_m k(b,m) / (M*F); F = frames_per_channel = 3, so M*F = 18 PER CHANNEL",
    "per_channel": ["R_cat", "R_cult"],  # computed separately; channel as a factor
    "rho": "spearman",                   # program convention
    "pooling": "per-set, then pooled with set as a blocking factor; per-set rho reported alongside pooled",

    # --- phi: primary CPC — quasi-binomial between-model dispersion (Pearson chi2/df) ---
    "phi": {
        "formula": "phi_b = [1/(M-1)] * sum_m (k(b,m) - F*pi_hat_b)^2 / [F*pi_hat_b*(1-pi_hat_b)]  (F = frames_per_channel = 3)",
        "df": "M-1",
        "null_expectation": 1.0,         # E[phi]=1 under homogeneity (all models share pi_hat)
        "interpretation": "phi>1 -> models disagree (inconsistent); phi<1 -> agree beyond chance (consistent)",
        "mean_independent": True,        # denominator divides out binomial variance F*pi(1-pi)
        "defined_domain": "pi_hat in (0,1)  (>=1 surfacing, not full saturation)",
        "undefined_only_at": "true-zero floor (correct behavior; not a CV-style blowup)",
        "low_recall_note": "a brand surfacing once in-channel (pi_hat = 1/18: one surfacing across 6 models x 3 frames within a channel) still yields a finite phi",
    },

    # --- J: positional diagnostic — mean pairwise Jaccard ---
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
        "directional_lean": "CONFIRMED (channel-asymmetry evidence)",
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
        "CONFIRMED (full recovery; zero residual undefined among >=1-surfacing)",
        "PARTIAL (recovery with residual undefined — implementation flag)",
        "FALSIFIED (no gain over the CV-CPC-defined set)",
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
    "inputs": "frozen per-(brand, model, frame, channel) surfacing from v0.34 / v0.35 / v0.36",
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
            "setup": "low-recall brand surfacing once within a channel, pi_hat = 1/18",
            "cv_cpc": "undefined / explosive (1/sqrt(mean) blowup)",
            "phi": "finite and defined",
            "demonstrates": "coverage gain — phi covers the low-recall segment CV cannot (H_LowRecallDefined)",
        },
        {
            "id": "channel_asymmetry_dissociation",
            "label": "illustrative / synthetic",
            "setup": "channel-asymmetry brand: strong in R_cult, ~zero in R_cat",
            "phi": "magnitude facet (between-model dispersion)",
            "J": "positional facet (where surfacing lands across frames)",
            "demonstrates": "phi (magnitude) and J (positional) dissociate — facets non-redundant (H_PositionalDissociation)",
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
# DEVIATIONS — contemporaneous log (additive; Entry 0 at r1 lock, Entry 1 r1->r2)
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
]
