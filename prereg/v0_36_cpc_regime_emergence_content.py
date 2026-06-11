# ---------------------------------------------------------------------------
# AIAS(TM) v0.36 -- CPC Regime Emergence -- PRE-REGISTRATION CONTENT (LOCK CANDIDATE)
# Phase type: re-analysis (no new LLM acquisition; fully retrospective)
# Lock tag: v0.36-prereg-r1
#
# NOTE TO OPERATOR (Claude Code): before commit, resolve every
# <<CONFORM-VERBATIM: ...>> placeholder by pulling the EXACT locked text from
# the named source record. Do not paraphrase. The guard at the bottom of this
# file raises if any placeholder remains.
# ---------------------------------------------------------------------------

PHASE_ID = "v0.36"
PHASE_TITLE = (
    "CPC Regime Emergence: Do Cross-Model CPC Clusters Inherit, Diverge From, "
    "or Collapse Under the Locked Four-Regime Brand Taxonomy?"
)

# ---------------------------------------------------------------------------
# DESIGN
# ---------------------------------------------------------------------------
DESIGN = """
Re-analysis, fully retrospective; no new LLM calls. Unsupervised clustering of
the frozen per-model CPC signal, tested against the locked per-brand Four-Regime
assignments. The phase asks whether CPC cluster structure INHERITS the regime
taxonomy (borrowed structure), clusters AUTONOMOUSLY (regime-independent
structure), survives residualization on Presence (layered structure), or
collapses under recognition saturation (degeneracy).

Output: osf/v36/v36_verdicts.json.
"""

# ---------------------------------------------------------------------------
# DATA & LINEAGE  (spec prose embedded verbatim; structured set in ANALYSIS_SET_SPEC)
# ---------------------------------------------------------------------------
DATA_AND_LINEAGE = """
- Primary: v0.31 retroactive CV-CPC cross-category baseline, 8 substrates x 24
  brands minus v0.31 locked exclusions. Citation route: OSF deposit
  osf.io/ec6wh/v31/ (SSRN abstract withdrawn -- lineage statement in Sec.2 and
  DEVIATIONS).
- Robustness: v0.35 frozen 84-unit analysis set; verdict-concordance check only;
  discordance reported, not adjudicated.
- Regime labels: locked per-brand Four-Regime assignments from each substrate
  phase's verdicts.json (taxonomy per Protocol v1.2, SSRN 6761698).
- Fully retrospective; no new LLM calls.

Provenance note: v0.31 is the data source by OSF deposit only; the v0.31 SSRN
abstract is WITHDRAWN and is not cited as methodological authority (consumed as
archived inputs). The 8-substrate-x-24-brand frame resolves, under v0.31's
locked exclusions and supplementary-set rules, to the 5-substrate panel-uniform
omnibus enumerated in ANALYSIS_SET_SPEC.
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
        "method": "gap statistic",
        "k_range": "k in {2..8}",
        "reference_samples_B": 500,
        "rule": "Tibshirani 1-SE rule",
    },
    "sensitivity": "k-means at gap-selected k, 50 restarts.",
    "permutation_null": "10,000 label shuffles within substrate.",
}

# ---------------------------------------------------------------------------
# ANALYSIS-SET SPEC
# (No brand registry this phase -- this section replaces the registry block.
#  No 24-brand validation hooks apply; the analysis sets are enumerated below.)
# ---------------------------------------------------------------------------
# No brand registry this phase.
ANALYSIS_SET_SPEC = {
    "primary_set": {
        "source": "v0.31 retroactive CV-CPC cross-category baseline (OSF osf.io/ec6wh/v31/)",
        "frame": "8 substrates x 24 brands minus v0.31 locked exclusions",
        "resolved_omnibus": "5-substrate panel-uniform omnibus (v0.19-v0.23); ~112 brand units",
        "substrates": {
            "v0.19": "audiophile headphones (16 brands)",
            "v0.20": "skincare (24)",
            "v0.21": "cosmetics (24)",
            "v0.22": "automotive (24)",
            "v0.23": "premium spirits (24)",
        },
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
# ---------------------------------------------------------------------------
HYPOTHESES = {
    "H_RegimeInheritance": {
        "statement": (
            "CPC cluster structure inherits the locked Four-Regime brand "
            "taxonomy."
        ),
        "mutually_exclusive_with": ["H_RegimeAutonomy"],
        "supported_iff": (
            "ARI(CPC clusters, Four-Regime labels) >= 0.30 AND ARI > 99th "
            "percentile of permutation null (p < 0.01)."
        ),
    },
    "H_RegimeAutonomy": {
        "statement": (
            "CPC clusters carry internally-valid structure that is independent "
            "of the Four-Regime labels."
        ),
        "mutually_exclusive_with": ["H_RegimeInheritance"],
        "supported_iff": (
            "gap selects k >= 2 AND mean silhouette >= 0.25 AND silhouette > "
            "95th percentile of null AND ARI < 0.30."
        ),
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
            "Residualize each model's CPC on the canonical per-brand Presence "
            "composite from phase verdicts (OLS, within substrate); cluster the "
            "6-dim residual vector under the identical procedure."
        ),
        "supported_iff": (
            "autonomy internal-validity criteria hold on residuals."
        ),
    },
    "H_SaturationDegeneracy": {
        "statement": (
            "CPC structure collapses under recognition saturation."
        ),
        "supported_iff": (
            "(a) within-substrate CPC variance lower in saturated vs "
            "unsaturated substrates, Brown-Forsythe directional p < 0.05, AND "
            "(b) within-substrate gap statistic resolves k=1 in a majority of "
            "saturated substrates while resolving k >= 2 in a majority of "
            "unsaturated substrates."
        ),
        "saturated_list_ref": "ANALYSIS_SET_SPEC['saturated_substrate_list']['operative']",
    },
}

# ---------------------------------------------------------------------------
# VERDICT MATRIX
# ---------------------------------------------------------------------------
VERDICT_MATRIX = {
    "Cell A": {
        "condition": "inheritance + no residual structure",
        "verdict": "borrowed structure",
    },
    "Cell B": {
        "condition": "inheritance + residual structure",
        "verdict": "layered structure",
    },
    "Cell C": {
        "condition": "autonomy + residual structure",
        "verdict": "autonomous structure",
    },
    "Cell D": {
        "condition": "unstructured + no residual structure",
        "verdict": "unstructured",
    },
}

# ---------------------------------------------------------------------------
# PRE-REGISTERED PREDICTIONS
# ---------------------------------------------------------------------------
PREDICTIONS = {
    "H_RegimeInheritance": "SUPPORTED",
    "H_ResidualStructure": "NOT SUPPORTED",
    "H_SaturationDegeneracy": "SUPPORTED",
    "net": (
        "Cell A (borrowed structure) -- fifth empirical pillar for the v1.8 "
        "mean-independent instrument requirement."
    ),
}

# ---------------------------------------------------------------------------
# FUTURE RESEARCH (designations)
# ---------------------------------------------------------------------------
FUTURE_RESEARCH = """
v1.8-instrument regime re-test designated in Future Research
(v0.35 -> v0.38 pattern): once the v1.8 mean-independent consistency instrument
is specified, re-run the regime-emergence test on the v1.8 signal to determine
whether borrowed structure persists under a Presence-decoupled metric.
"""

# ---------------------------------------------------------------------------
# DEVIATIONS
# ---------------------------------------------------------------------------
DEVIATIONS = """
Entry 0 -- COI carry-forward (conformed VERBATIM from locked source records):
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

Entry 1 -- v0.31 provenance / SSRN-withdrawn lineage:
The primary analysis set is sourced from the v0.31 OSF deposit
(osf.io/ec6wh/v31/) as archived data only. The v0.31 SSRN abstract is WITHDRAWN
and is not cited as methodological authority. Consumption convention follows the
v0.33-v0.35 lineage: frozen per-model inputs remain valid archived data; CV-CPC's
methodological status is fixed by v1.7 (computation defined, instrument not
adopted).

Entry 2 -- Scaffold trim:
No-acquisition re-analysis; any acquisition / two-wave scaffolding carried by
upstream templates is removed. Scaffold artifact, not a methodology amendment.
"""

# ---------------------------------------------------------------------------
# EXTERNAL ANCHOR (binding)
# ---------------------------------------------------------------------------
EXTERNAL_ANCHOR = """
Sequence after content lock:
1. Pathspec-limited commit (enumerated paths only; dirty-tree work excluded).
2. Tag v0.36-prereg-r1 (additive, no force-moves).
3. git push origin v0.36 --tags
4. Upload prereg artifacts to osf.io/ec6wh/v36/prereg/ via osf_upload.py.
5. Verify both remotes resolve.
6. Only then: clustering + scoring.
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
