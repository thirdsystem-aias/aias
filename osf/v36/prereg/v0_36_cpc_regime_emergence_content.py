# ---------------------------------------------------------------------------
# AIAS(TM) v0.36 -- CPC Regime Emergence -- PRE-REGISTRATION CONTENT (LOCK CANDIDATE)
# Phase type: re-analysis (no new LLM acquisition; fully retrospective)
# Lock tag: v0.36-prereg-r2   (supersedes r1; r1 remains the deposited record)
#
# r2 amends r1 for a data-lineage defect, a construct-identity correction, and
# a recognition-commensurability finding -- all pre-scoring and outcome-blind
# (see DEVIATIONS Entry 0). Hypotheses, thresholds, and predictions are
# UNCHANGED; r2 assigns each locked criterion to its maximal executable scope.
#
# NOTE TO OPERATOR (Claude Code): before commit, resolve every
# <<CONFORM-VERBATIM: ...>> placeholder by pulling the EXACT locked text from
# the named source record. Do not paraphrase. The guard at the bottom of this
# file raises if any placeholder remains.
# ---------------------------------------------------------------------------

PHASE_ID = "v0.36"
PHASE_TITLE = (
    "CPC Regime Emergence: Does Cross-Model CPC Cluster Structure Recover the "
    "Per-Brand Presence-Regime Classification, Cluster Autonomously, or Collapse "
    "Under Saturation?"
)

# Determinism: single fixed seed for all stochastic steps (gap reference draws,
# permutation nulls, k-means restarts). Recorded in verdicts metadata.
SEED = 36

# ---------------------------------------------------------------------------
# REGIME DISAMBIGUATION (binding -- "regime" is overloaded across the program)
# ---------------------------------------------------------------------------
# The v0.36 OPERATIVE target is row 2 (the v0.23 per-brand Presence-quartile
# regime). Row 1 (the construct r1 mis-cited) is NOT the operative target.
REGIME_DISAMBIGUATION = [
    {
        "construct": "v1.2 Four-Regime Taxonomy (SSRN 6761698)",
        "level": "per-SUBSTRATE",
        "basis": "AI-Presence x Google-Trends construct-validity correlation "
                 "(Regime 1 marginal / 2 age-mediated / 3 scale-mismatch / "
                 "4 covariate-saturated weak)",
        "operative_target": False,
        "note": "External Trends data; not per-brand; not computable from CPC "
                "frozen quantities; NOT assigned for the CPC substrates "
                "(v0.19-v0.23). r1 mis-cited this as the per-brand label source.",
    },
    {
        "construct": "v0.23 per-brand regime (Dominant/Established/Emerging/Absent)",
        "level": "per-BRAND",
        "basis": "within-substrate Presence-composite quartiles "
                 "(score_v0_23.py:332-356)",
        "operative_target": True,
        "note": "The ONLY per-brand four-valued classification existing in frozen "
                "form. Present for v0.23 only. This is the v0.36 regime target.",
    },
    {
        "construct": "H_Regime4_* (v20/v21/v22 verdicts)",
        "level": "hypothesis label",
        "basis": "v1.5 C2 cell-floor distribution test (regime-floor failure)",
        "operative_target": False,
        "note": "A hypothesis verdict, not a per-brand label. Unrelated.",
    },
]

# ---------------------------------------------------------------------------
# DESIGN
# ---------------------------------------------------------------------------
DESIGN = """
Re-analysis, fully retrospective; no new LLM calls. Unsupervised clustering of
the frozen per-model CPC signal, tested for (i) whether per-brand CPC cluster
structure recovers the v0.23 per-brand Presence-regime classification
(inheritance), (ii) whether CPC carries internally-valid structure of its own
(autonomy / typology emergence), (iii) whether such structure survives
residualization on Presence, and (iv) whether it collapses under recognition
saturation (degeneracy).

Per the r2 construct-identity correction (DEVIATIONS Entry 0): the regime target
is the v0.23 per-brand Presence-quartile regime (REGIME_DISAMBIGUATION row 2),
NOT the v1.2 substrate-level Trends taxonomy. Each locked criterion is evaluated
at its maximal executable scope (see HYPOTHESES['...']['scope']).

Output: osf/v36/v36_verdicts.json.
"""

# ---------------------------------------------------------------------------
# DATA & LINEAGE
# ---------------------------------------------------------------------------
DATA_AND_LINEAGE = """
- CPC feature source (all 112 units): osf/v33/data/v33_eta2.csv -- frozen
  per-brand 6-dim per-model recall vectors (recall_per_model) and recognition
  vectors (recog_per_model) for the 5-substrate omnibus (v0.19-v0.23), in
  canonical 6-model PANEL order. Citation route: OSF deposit osf.io/ec6wh/v31/
  (v0.31 SSRN abstract WITHDRAWN -- lineage statement in Sec.2 and DEVIATIONS).
- Regime target (per-brand, four-valued): osf/v23/v23_verdicts.json
  brand_details[].regime (Dominant/Established/Emerging/Absent), read as a
  frozen field -- NO derivation. Present for v0.23 only (24 units).
  Construct identity: this is the v0.23 Presence-quartile regime
  (REGIME_DISAMBIGUATION row 2), explicitly NOT the v1.2 Four-Regime Taxonomy.
- Presence composite (per-brand): osf/v23/v23_verdicts.json
  brand_details[].composite_presence (frozen). Present for v0.23 only.
- Robustness: v0.35 frozen 84-unit analysis set; verdict-concordance check only;
  discordance reported, not adjudicated.
- Fully retrospective; no new LLM calls.

r2 lineage correction (see DEVIATIONS Entry 0): r1 asserted per-brand
Four-Regime labels and Presence composites were locked "in each substrate
phase's verdicts.json" under the v1.2 taxonomy. Verified false: (a) the v1.2
taxonomy is substrate-level and Trends-based, not a per-brand label, and is
unassigned for the CPC substrates; (b) the only per-brand four-valued labels and
the only frozen Presence composite are materialized in v0.23 alone, under a
DIFFERENT construct (Presence quartiles). v0.19-v0.22 measured recognition as
binary (yes/no), so the v0.23 graded-recognition composite is not even
computable for them (commensurability finding, Entry 0).
"""

# ---------------------------------------------------------------------------
# FEATURE SPACE
# ---------------------------------------------------------------------------
FEATURE_SPACE = {
    "primary": (
        "6-dim per-model CPC vector per brand-unit (fixed six-model panel), "
        "z-scored within substrate per model."
    ),
    "sensitivity": "scalar CV-CPC, same standardization.",
    "cpc_definition": "CV-CPC = 1/(1+CV), CV = pop_SD/mean (ddof=0) of the "
                      "per-model recall vector; v1.7 computation (SSRN 6878818).",
    "floor": "mean recall < 1.0 -> CV-CPC UNDEFINED (excluded from analysis set).",
    "residual_presence_primary": (
        "per-brand composite_presence (v0.23 only) -- used for H_ResidualStructure."
    ),
    "residual_recall_sensitivity": (
        "per-brand mean recall (computable for all 112 from v33_eta2.csv) -- "
        "omnibus residualization sensitivity arm, sensitivity-only."
    ),
    "panel": [
        "claude-opus-4-5",
        "claude-sonnet-4-5",
        "gpt-4o",
        "gpt-4o-mini",
        "gemini-2.5-flash",
        "gemini-2.5-flash-lite",
    ],
    "panel_n": 6,
}

# ---------------------------------------------------------------------------
# CLUSTERING (LOCKED)
# ---------------------------------------------------------------------------
CLUSTERING = {
    "primary": "Ward hierarchical, Euclidean, on standardized features.",
    "k_selection": {
        "method": "gap statistic (Tibshirani; uniform reference over the "
                  "feature bounding box)",
        "k_min": 1,            # r2 Entry 1: k=1 selectable (unstructured/degeneracy)
        "k_max": 8,
        "reference_samples_B": 500,
        "rule": "Tibshirani 1-SE rule",
    },
    "sensitivity": "k-means at gap-selected k, 50 restarts.",
    "kmeans_restarts": 50,
    "permutation_null_n": 10000,   # within-substrate label shuffles
    "seed": SEED,
}

# ---------------------------------------------------------------------------
# ANALYSIS-SET SPEC
# (No brand registry this phase -- this section replaces the registry block.
#  No 24-brand validation hooks apply; the analysis sets are enumerated below.)
# ---------------------------------------------------------------------------
# No brand registry this phase.
ANALYSIS_SET_SPEC = {
    "omnibus_set": {
        "source": "osf/v33/data/v33_eta2.csv (frozen; lineage osf.io/ec6wh/v31/)",
        "substrates": {
            "v0.19": "audiophile headphones (16 brands)",
            "v0.20": "skincare (24)",
            "v0.21": "cosmetics (24)",
            "v0.22": "automotive (24)",
            "v0.23": "premium spirits (24)",
        },
        "n_units_raw": 112,
        "analysis_set": "units with computable CV-CPC (mean recall >= 1.0); "
                        "undefined units excluded and counted per substrate.",
    },
    "regime_subsample": {
        "source": "osf/v23/v23_verdicts.json brand_details[] (frozen)",
        "substrate": "v0.23 premium spirits",
        "n_units": 24,
        "fields": ["regime", "composite_presence"],
        "use": "ARI inheritance test + H_ResidualStructure (primary).",
    },
    "robustness_set": {
        "source": "v0.35 frozen 84-unit analysis set",
        "use": "verdict-concordance check only; discordance reported, not adjudicated.",
    },
    # SATURATED-SUBSTRATE LIST -- enumerated by lock (both designations recorded;
    # v0.34 saturation_flagged is OPERATIVE for H_SaturationDegeneracy).
    "saturated_substrate_list": {
        "operative": {
            "criterion": (
                ">=90% per-model recognition among defined brands "
                "(v0.34 saturation_flagged; osf/v34/v34_verdicts.json)"
            ),
            "saturated": {
                "v0.20": "skincare",
                "v0.21": "cosmetics",
                "v0.22": "automotive",
                "v0.23": "premium spirits",
            },
            "unsaturated": {
                "v0.19": "audiophile headphones",
            },
        },
        "secondary_observation": {
            "criterion": (
                "per-substrate covariate (C_P) constant across brands "
                "(v0.35 per_substrate_covariate_constant; osf/v35/v35_verdicts.json)"
            ),
            "constant": {
                "v0.21": "cosmetics",
                "v0.22": "automotive",
                "v0.23": "premium spirits",
            },
            "not_constant": {
                "v0.19": "audiophile headphones",
                "v0.20": "skincare",
            },
        },
        "caveat": (
            "Skincare (v0.20) is recognition-saturated under v0.34 but NOT "
            "covariate-constant under v0.35; recorded as a sensitivity caveat "
            "for H_SaturationDegeneracy (majority tests use the v0.34 operative "
            "list)."
        ),
    },
}

# ---------------------------------------------------------------------------
# HYPOTHESES & CRITERIA
# (thresholds UNCHANGED from r1; r2 adds machine-readable 'criteria' mirrors
#  and per-hypothesis 'scope'. The scorer IMPORTS these -- it does not restate.)
# ---------------------------------------------------------------------------
HYPOTHESES = {
    "H_RegimeInheritance": {
        "statement": (
            "Per-brand CPC cluster structure recovers the v0.23 per-brand "
            "Presence-regime classification."
        ),
        "mutually_exclusive_with": ["H_RegimeAutonomy"],
        "supported_iff": (
            "ARI(CPC clusters, regime labels) >= 0.30 AND ARI > 99th percentile "
            "of permutation null (p < 0.01)."
        ),
        "criteria": {"ari_min": 0.30, "ari_null_pct": 99, "p_max": 0.01},
        "scope": "v0.23 (n=24); ARI against frozen brand_details[].regime; "
                 "within-substrate permutation null.",
    },
    "H_RegimeAutonomy": {
        "statement": (
            "CPC clusters carry internally-valid structure independent of the "
            "regime labels (typology emergence)."
        ),
        "mutually_exclusive_with": ["H_RegimeInheritance"],
        "supported_iff": (
            "gap selects k >= 2 AND mean silhouette >= 0.25 AND silhouette > "
            "95th percentile of null AND ARI < 0.30."
        ),
        "criteria": {"k_min": 2, "silhouette_min": 0.25, "silhouette_null_pct": 95,
                     "ari_max": 0.30},
        "scope": "internal-structure criteria (gap k, silhouette, silhouette "
                 "null) OMNIBUS (112); ARI<0.30 leg on v0.23 (n=24). Composed "
                 "across scopes; each component reported with its scope.",
        "neither_branch": (
            "Neither inheritance nor autonomy -> verdict 'unstructured' "
            "(gap k=1 or silhouette fails null)."
        ),
    },
    "H_ResidualStructure": {
        "statement": (
            "CPC cluster structure survives residualization on Presence."
        ),
        "procedure": (
            "Residualize each model's CPC on the per-brand Presence composite "
            "(OLS, within substrate); cluster the 6-dim residual vector under the "
            "identical procedure; apply the autonomy internal-validity criteria."
        ),
        "supported_iff": "autonomy internal-validity criteria hold on residuals.",
        "criteria": {"k_min": 2, "silhouette_min": 0.25, "silhouette_null_pct": 95},
        "scope": "v0.23 (n=24), residualized on composite_presence (PRIMARY). "
                 "SECONDARY sensitivity (omnibus, 112): residualize 6-dim CPC on "
                 "per-brand mean recall; sensitivity-only, never verdict-determining.",
    },
    "H_SaturationDegeneracy": {
        "statement": "CPC structure collapses under recognition saturation.",
        "supported_iff": (
            "(a) within-substrate CPC variance lower in saturated vs "
            "unsaturated substrates, Brown-Forsythe directional p < 0.05, AND "
            "(b) within-substrate gap statistic resolves k=1 in a majority of "
            "saturated substrates while resolving k >= 2 in a majority of "
            "unsaturated substrates."
        ),
        "criteria": {"bf_alpha": 0.05, "bf_directional": True,
                     "k_degenerate": 1, "k_structured_min": 2},
        "scope": "OMNIBUS (112); saturated list = "
                 "ANALYSIS_SET_SPEC['saturated_substrate_list']['operative'].",
    },
}

# ---------------------------------------------------------------------------
# SENSITIVITY
# ---------------------------------------------------------------------------
SENSITIVITY = """
- Scalar CV-CPC feature arm (vs 6-dim primary), same standardization.
- k-means at gap-selected k, 50 restarts (vs Ward primary); recorded in
  metadata, never verdict-determining.
- Omnibus mean-recall residualization arm for H_ResidualStructure (vs the
  v0.23 composite_presence primary); sensitivity-only, never verdict-determining.
- v0.35 84-unit concordance check; discordance reported, not adjudicated.
"""

# ---------------------------------------------------------------------------
# VERDICT MATRIX (scopes annotated; cell determined by v0.23 inheritance +
# v0.23 residual structure. Omnibus internal-structure reported ALONGSIDE each
# cell, not folded into it.)
# ---------------------------------------------------------------------------
VERDICT_MATRIX = {
    "Cell A": {
        "condition": "inheritance + no residual structure",
        "verdict": "borrowed structure",
        "scope": "v0.23 inheritance SUPPORTED AND v0.23 residual NOT SUPPORTED.",
    },
    "Cell B": {
        "condition": "inheritance + residual structure",
        "verdict": "layered structure",
        "scope": "v0.23 inheritance SUPPORTED AND v0.23 residual SUPPORTED.",
    },
    "Cell C": {
        "condition": "autonomy + residual structure",
        "verdict": "autonomous structure",
        "scope": "autonomy (omnibus internal-structure + v0.23 ARI<0.30) AND "
                 "v0.23 residual SUPPORTED.",
    },
    "Cell D": {
        "condition": "unstructured + no residual structure",
        "verdict": "unstructured",
        "scope": "neither inheritance nor autonomy AND no residual structure.",
    },
    "_reporting_note": (
        "Omnibus internal-structure verdict (gap k, silhouette, null over 112 "
        "units) is reported alongside the cell as the 'own structure / typology "
        "emergence' descriptor."
    ),
}

# ---------------------------------------------------------------------------
# PRE-REGISTERED PREDICTIONS (values UNCHANGED from r1; restated per-scope)
# ---------------------------------------------------------------------------
PREDICTIONS = {
    "H_RegimeInheritance": {"prediction": "SUPPORTED", "scope": "v0.23 (n=24)"},
    "H_ResidualStructure": {"prediction": "NOT SUPPORTED",
                            "scope": "v0.23 primary (omnibus mean-recall arm = sensitivity)"},
    "H_SaturationDegeneracy": {"prediction": "SUPPORTED", "scope": "omnibus (112)"},
    "net": (
        "Cell A (borrowed structure) -- v0.23 inheritance SUPPORTED and v0.23 "
        "residual NOT SUPPORTED. Fifth empirical pillar for the v1.8 "
        "mean-independent instrument requirement. No re-tuning from r1."
    ),
}

# ---------------------------------------------------------------------------
# FUTURE RESEARCH (designations)
# ---------------------------------------------------------------------------
FUTURE_RESEARCH = """
1. v1.8-instrument regime re-test (v0.35 -> v0.38 pattern): once the v1.8
   mean-independent consistency instrument is specified, re-run the
   regime-emergence test on the v1.8 signal under a Presence-decoupled metric.
2. Graded-recognition re-scoring: the binary-vs-graded recognition asymmetry
   across v0.19-v0.22 (binary) vs v0.23 (graded) blocks an omnibus per-brand
   Presence-regime target. A common-protocol re-scoring of all substrates under
   graded recognition would enable the omnibus regime test. Distinct from (1).
3. v1.2 Four-Regime (Trends) taxonomy test: assigning the substrate-level v1.2
   AI-Presence x Google-Trends regimes to the CPC substrates would require new
   Google Trends acquisition; out of scope for this retrospective phase.
"""

# ---------------------------------------------------------------------------
# DEVIATIONS
# ---------------------------------------------------------------------------
DEVIATIONS = """
Entry 0 -- r1 -> r2 amendment (pre-scoring, OUTCOME-BLIND: at amendment time no
clustering, ARI, silhouette, gap, variance, or permutation statistic had been
computed). Hypotheses, thresholds, and predictions are UNCHANGED; r2 only
corrects lineage/construct identity and assigns each criterion to scope.

  (a) Lineage defect. r1 DATA_AND_LINEAGE asserted per-brand Four-Regime labels
      and Presence composites exist in frozen form in each substrate phase's
      verdicts.json. Verified false: materialized only in v0.23 brand_details;
      v0.20-v0.22 carry older-schema cell/cp only; v0.19 has no verdicts.json.

  (b) Construct-identity correction. r1 cited the v1.2 Four-Regime Taxonomy
      (SSRN 6761698) as the per-brand label source. The v1.2 taxonomy is
      SUBSTRATE-level and defined by AI-Presence x Google-Trends correlation
      (Regimes 1-4), is not a per-brand label, and is unassigned for the CPC
      substrates. The operative v0.36 target is the v0.23 per-brand
      Presence-quartile regime (Dominant/Established/Emerging/Absent,
      score_v0_23.py:332-356) -- a DIFFERENT construct, present for v0.23 only.
      The "regime" term is overloaded across three constructs; see the
      REGIME_DISAMBIGUATION table (embedded verbatim below):

        Row 1 | v1.2 Four-Regime Taxonomy (SSRN 6761698) | per-SUBSTRATE |
              AI-Presence x Google-Trends correlation (Regime 1 marginal /
              2 age-mediated / 3 scale-mismatch / 4 covariate-saturated weak) |
              OPERATIVE TARGET: No -- external Trends data, not per-brand, not in
              CPC frozen data, unassigned for v0.19-v0.23; r1 mis-cited this.
        Row 2 | v0.23 per-brand regime (Dominant/Established/Emerging/Absent) |
              per-BRAND | within-substrate Presence-composite quartiles
              (score_v0_23.py:332-356) | OPERATIVE TARGET: Yes -- the only
              per-brand four-valued classification in frozen form; v0.23 only.
        Row 3 | H_Regime4_* (v20/v21/v22 verdicts) | hypothesis label |
              v1.5 C2 cell-floor distribution test | OPERATIVE TARGET: No.

  (c) Recognition-commensurability finding. v0.19-v0.22 measured Phase A
      recognition as BINARY (yes/no); v0.23 measured it as GRADED richness
      (R0-R3, LLM-judged). The v0.23 Presence composite weights graded
      recognition 0.40, so it is not computable for v0.19-v0.22 from any frozen
      artifact -- the binary phases never collected the richness signal. This is
      additional empirical support for the v1.8 graded-recognition-signal
      requirement (cross-ref FUTURE_RESEARCH items 1-2).

  (d) Scope assignment. Each locked criterion is evaluated at maximal executable
      scope (HYPOTHESES['...']['scope']): internal-structure criteria OMNIBUS
      (112); ARI inheritance + H_ResidualStructure primary on v0.23 (n=24);
      H_SaturationDegeneracy OMNIBUS; plus an omnibus mean-recall residual
      sensitivity arm (sensitivity-only).

Entry 1 -- Gap k-range evaluability clarification (execution detail, not a
threshold change): the gap statistic is computed over k in {1..8}. k=1 must be
selectable so the unstructured / saturation-degeneracy verdicts are
expressible; the Tibshirani 1-SE selection rule is unchanged. (r1 CLUSTERING
stated k in {2..8}; r2 sets k_min=1.)

Entry 2 -- COI carry-forward (conformed VERBATIM from locked source records):
v0.36 reuses the v0.19-v0.23 registries and inherits their COI screen.

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

Entry 3 -- v0.31 provenance / SSRN-withdrawn lineage:
The CPC inputs are sourced from the v0.31 OSF deposit (osf.io/ec6wh/v31/) as
archived data only. The v0.31 SSRN abstract is WITHDRAWN and is not cited as
methodological authority. Consumption convention follows the v0.33-v0.35
lineage: frozen per-model inputs remain valid archived data; CV-CPC's
methodological status is fixed by v1.7 (computation defined, instrument not
adopted).

Entry 4 -- Scaffold trim:
No-acquisition re-analysis; any acquisition / two-wave scaffolding carried by
upstream templates is removed. Scaffold artifact, not a methodology amendment.
"""

# ---------------------------------------------------------------------------
# EXTERNAL ANCHOR (binding)
# ---------------------------------------------------------------------------
EXTERNAL_ANCHOR = """
Sequence after content lock (r2):
1. Pathspec-limited commit (prereg + scorer; dirty-tree work excluded).
2. Tag v0.36-prereg-r2 (additive, no force-moves; r1 retained, not deleted).
3. git push origin v0.36 --tags
4. Upload prereg artifacts to osf.io/ec6wh/v36/prereg/ via osf_upload.py
   (alongside the r1 artifacts; r2 supersedes, r1 remains the record).
5. Verify both remotes resolve.
6. Only then: scoring (validation gate step 0), then verdicts.
"""

# ---------------------------------------------------------------------------
# Commit guard -- raises if verbatim-conform placeholders remain unresolved.
# ---------------------------------------------------------------------------
if "<<CONFORM-VERBATIM" in DEVIATIONS:
    raise RuntimeError(
        "v0.36 prereg content module: unresolved CONFORM-VERBATIM placeholder "
        "in DEVIATIONS. Pull exact locked COI text from v0.22/v0.19 records "
        "before commit. COMMIT BLOCKED."
    )
