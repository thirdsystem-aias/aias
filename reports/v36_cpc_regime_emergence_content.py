"""
v0.36 CPC Regime Emergence — Third System brand-format report content module.

Managerial register (P-framing; no H_* labels outside the scoring table's plain
names). Every statistic is pulled from osf/v36/v36_verdicts.json at import time
(see V below) so the report cannot drift from the locked scorer output.

Eleven attributes, consumed by reports/build_report_v36.py:
  COVER, STANDFIRST, LEAD_DECK, EXEC_SUMMARY, WHAT_WE_MEASURED, PATTERNS,
  LIMITATIONS, WHATS_NEXT, HYPOTHESIS_SCORING, HYPOTHESIS_DETAILS, CLOSING
"""

import json
from pathlib import Path

# --- SSOT: locked scorer output (tag v0.36-prereg-r2) ----------------------
_V = json.load(open(Path(__file__).resolve().parent.parent / "osf" / "v36" / "v36_verdicts.json"))
_H = _V["hypotheses"]
_INH = _H["H_RegimeInheritance"]
_AUT = _H["H_RegimeAutonomy"]
_RES = _H["H_ResidualStructure"]
_SAT = _H["H_SaturationDegeneracy"]
_K = _V["selected_k"]
_OMNI = _V["omnibus_internal_structure_descriptor"]
_NDEF = _V["metadata"]["n_defined_per_substrate"]
_SAT_K = _SAT["per_substrate_gap_k"]
_KSTR = "/".join(str(_SAT_K[s]) for s in ["v0.19", "v0.20", "v0.21", "v0.22", "v0.23"])
_NDEF_TOT = sum(_NDEF.values())

# ---------------------------------------------------------------------------
COVER = {
    "eyebrow": "AIAS™ Measurement Program · Phase v0.36",
    "title": "The Structure That Wasn’t There",
    "subtitle": "Cross-model consistency does not inherit the brand-presence "
                "hierarchy — and the way it fails tells us exactly what to build next.",
}

# ---------------------------------------------------------------------------
STANDFIRST = (
    "Before any data ran, this phase pre-registered a specific bet: that “AI "
    "consistency” clusters would turn out to be brand presence wearing a "
    "different name. The bet lost — and not because consistency revealed a "
    "hidden order of its own. The measuring instrument broke first, in three "
    "instructive ways. This report scores the loss as registered, then reads the "
    "wreckage."
)

# ---------------------------------------------------------------------------
# LEAD_DECK — the five propositions as a deck (rendered as one block, <br/> lines)
LEAD_DECK = (
    "<b>P1</b> AI consistency, as currently measurable, is not a hidden brand "
    "ranking: consistency clusters do not recover the presence hierarchy.<br/>"
    "<b>P2</b> The instrument fails where brands are weakest: a computability "
    "floor silently erased 15 of 24 premium-spirits brands before the test could run.<br/>"
    "<b>P3</b> Saturated categories are noisier, not quieter: recognition "
    "ceilings appear to amplify cross-model dispersion rather than collapse it — "
    "the pre-registered prediction reversed.<br/>"
    "<b>P4</b> A faint cross-category signature exists in how models disagree: "
    "three clusters, one hair under the evidentiary bar. Suggestive, not decision-grade.<br/>"
    "<b>P5</b> Every failure points one direction: consistency needs a "
    "mean-independent instrument before it can carry managerial weight."
)

# ---------------------------------------------------------------------------
# EXEC_SUMMARY — paragraphs split on blank lines. ¶1 final sentence and ¶2
# carry the finalized replacements (deposit-timeline precision; loss not overstated).
EXEC_SUMMARY = (
    "This phase asked whether cross-platform consistency (CPC) — how uniformly "
    "six frontier models recall a brand — has regime structure of its own, or "
    "merely inherits the brand-presence hierarchy already measured by the AIAS™ "
    "Presence component. The design was fully retrospective: 112 brand-units across "
    "five categories, frozen data, zero new model calls. Decision rules, thresholds, "
    "and predictions were locked and deposited before any data was analyzed; the "
    "build-time corrections that followed were authored and timestamped outcome-blind, "
    "before a single statistic existed.\n\n"

    "The pre-registered prediction was “borrowed structure”: consistency "
    "clusters would recover presence regimes, and would dissolve once presence was "
    "statistically removed. The result landed in the opposite cell of the locked "
    "verdict matrix — unstructured. The headline prediction was wrong, and is "
    "reported as wrong; the one call that held was the narrower one, that consistency "
    "carries no presence-independent structure.\n\n"

    "But the three individual failures share an anatomy. The inheritance test "
    "couldn’t run at power because the consistency metric is mathematically "
    "undefined for low-recall brands — a coverage hole, not a verdict. The "
    "saturation test reversed direction because the metric’s dispersion is "
    "driven by the recall mean it divides by. And the strongest structural signal in "
    "the data appeared only in a sensitivity arm that removed the mean entirely. "
    "Three failures, one diagnosis: the current consistency metric is welded to "
    "presence by construction.\n\n"

    "That diagnosis was already suspected — four prior phases flagged it. This "
    "phase adds the regime evidence and converts the case for a mean-independent "
    "consistency instrument (methodology phase v1.8) from motivated to overdetermined."
)

# ---------------------------------------------------------------------------
# WHAT_WE_MEASURED — paragraphs; final paragraph is the finalized transparency note.
WHAT_WE_MEASURED = (
    "v0.36 is a re-analysis: no new AI queries, no new brands. The inputs are the "
    "program’s frozen omnibus panels measured across the same six-model panel "
    "used since v0.17 — audiophile headphones, skincare, cosmetics, automotive, "
    "and premium spirits: 112 brand-units in all. CPC is how uniformly the six models "
    "recall a brand. Every clustering parameter — the algorithm, the "
    "cluster-count selection rule, the thresholds, the permutation tests, the random "
    "seed — was locked at pre-registration and deposited to OSF; the seed-bearing "
    "scoring code was committed under tag v0.36-prereg-r2, and the deposited "
    "amendment record attests that no statistic had been computed when it was "
    "written.\n\n"

    "The regime target — the per-brand presence classification (Dominant / "
    "Established / Emerging / Absent) — is frozen in the premium-spirits phase, "
    "the only category where such labels exist. The pre-registration documents that "
    "constraint rather than papering over it.\n\n"

    "Two principal corrections were made during the build and timestamped before any "
    "result existed: a data-lineage error (the per-brand regime labels are "
    "materialized in one category, not all five) and a construct-naming collision "
    "(the regime target is the premium-spirits presence-quartile classification, not "
    "the program’s substrate-level Trends taxonomy that happens to share the word "
    "“regime”). Scope and analysis-range clarifications were logged "
    "alongside. All are public in the deposit record."
)

# ---------------------------------------------------------------------------
# PATTERNS — five findings, authored directly, each anchored to a chart.
#   P1 -> chart_02 (inheritance floor) [references the matrix, chart_05, in exec]
#   P2 -> text-only (references the floor chart in P1)
#   P3 -> chart_03 (saturation reversal)
#   P4 -> chart_01 (omnibus structure)
#   P5 -> chart_04 (residual divergence)
PATTERNS = [
    {
        "number": 1,
        "title": "AI consistency is not a hidden brand ranking",
        "chart_slot": "inheritance",
        "paragraphs": [
            "The bet was that consistency clusters would recover the brand-presence "
            "hierarchy — that a brand’s consistency rank would track its "
            "presence rank. It does not. Where the test could be run, cluster "
            "structure and the presence-regime labels share no measurable agreement "
            f"(Adjusted Rand Index {_INH['ari']:.2f}). On the locked verdict matrix "
            "the phase landed in the opposite corner from the prediction: not "
            "“borrowed structure” but “unstructured.”",
            "That is the headline, and it is reported exactly as it scored. What the "
            "test could actually see, though, is the real story — and it is "
            "smaller than it should have been (see P2).",
        ],
    },
    {
        "number": 2,
        "title": "The instrument fails where brands are weakest",
        "chart_slot": None,
        "paragraphs": [
            "Consistency is a ratio that divides by how often a brand is recalled. "
            "Below a floor of recall, the metric does not exist — you cannot "
            "measure the consistency of something that is never named. In premium "
            f"spirits that floor erased 15 of 24 brands, leaving {_NDEF['v0.23']} "
            "measurable. These are exactly the weak-recall brands a consistency "
            "diagnostic should care about most.",
            "A metric blind to the bottom of the market cannot classify the market. "
            "The inheritance test above ran on those nine survivors — too few, "
            "too top-heavy, for a verdict to mean much. We record it as scored and "
            "name the limitation plainly.",
        ],
    },
    {
        "number": 3,
        "title": "Saturated categories are noisier, not quieter",
        "chart_slot": "saturation_rev",
        "paragraphs": [
            "The prediction was that categories where every brand is well recognized "
            "would show flatter, more uniform consistency — a ceiling effect "
            "collapsing the variation. The opposite happened. Saturated categories "
            f"carry more cross-model dispersion, not less ({_SAT['dev_mean_saturated']:.3f} "
            f"versus {_SAT['dev_mean_unsaturated']:.3f}), and the difference is "
            f"significant in the wrong direction (Levene p={_SAT['bf_levene_p_two_sided']:.3f}).",
            "Read post-hoc, this is mechanically consistent with a ratio metric whose "
            "denominator shrinks across long, low-recall tails — the same "
            "presence-coupling that undoes the other tests. Offered as interpretation, "
            "not as a pre-registered finding.",
        ],
    },
    {
        "number": 4,
        "title": "A faint signature exists in how models disagree",
        "chart_slot": "omnibus",
        "paragraphs": [
            "Pool all 112 brand-units and a structure does flicker into view: three "
            f"clusters emerge above chance. But it sits at silhouette "
            f"{_OMNI['silhouette']:.4f}, a hair under the locked evidentiary bar of "
            "0.25 — above the noise floor, below the line we set in advance. We "
            "score it not supported and relax no threshold to rescue it.",
            "It is described here because it is real enough that the next instrument "
            "must explain it: there is something in how the models disagree about "
            "lesser-known brands, even if today’s metric cannot resolve it cleanly.",
        ],
    },
    {
        "number": 5,
        "title": "Every failure points the same direction",
        "chart_slot": "residual",
        "paragraphs": [
            "One arm of the analysis removed recall volume from the signal entirely "
            "— and only there did structure appear (two clean clusters, criteria "
            "met). It was pre-specified as a sensitivity check, never able to set the "
            "verdict, and it is treated that way. But the tell is unmistakable: the "
            "one place structure survives is the one place the mean is gone.",
            "Inheritance unevaluable, saturation reversed, structure only without the "
            "mean — three different failures, one diagnosis. The consistency "
            "metric is welded to presence by construction. That is the specification "
            "for what comes next.",
        ],
    },
]

# ---------------------------------------------------------------------------
LIMITATIONS = (
    "The inheritance and residual tests ran on a single category at nine defined "
    "units — unevaluable at meaningful power, recorded as-scored rather than "
    "adjudicated. The regime target exists for one substrate only; the omnibus "
    "version is blocked by a binary-versus-graded recognition asymmetry across the "
    "earlier phases, which measured recognition as a yes/no rather than a graded "
    "signal. The mean-recall sensitivity arm was pre-specified as never "
    "verdict-determining and is treated accordingly. And the consistency quantity "
    "here holds characterization status only — it was never adopted as a "
    "canonical instrument, which is, in the end, part of what this phase is the case for."
)

# ---------------------------------------------------------------------------
# WHATS_NEXT — item 1 carries the finalized five-convergent-lines enumeration.
WHATS_NEXT = (
    "Three threads follow. First, the v1.8 mean-independent consistency instrument, "
    "now carrying five convergent lines of motivation — the v1.7 "
    "presence-coupling result and the saturation-collapse findings of v0.33, v0.34, "
    "and v0.35, joined now by this phase’s regime evidence — with the "
    "regime question designated for re-test once the instrument exists. Second, a "
    "common-protocol graded-recognition re-scoring of all substrates, which would "
    "unlock the omnibus regime target this phase could not assemble. Third, the "
    "substrate-level Trends-based taxonomy test, which requires new external data and "
    "is explicitly out of retrospective scope."
)

# ---------------------------------------------------------------------------
# HYPOTHESIS_SCORING — the four hypotheses + Net, scored. Verdicts from SSOT.
HYPOTHESIS_SCORING = {
    "heading": "The hypotheses, scored",
    "intro": "Each row is a locked pre-registered test, scored against its frozen "
             "threshold. Plain names stand in for the formal hypothesis labels; the "
             "net cell is the verdict-matrix landing.",
    "columns": ["Hypothesis", "Scope", "Predicted", "Verdict"],
    "rows": [
        ("Inheritance", "spirits, n=9 defined", "Supported",
         f"{_INH['verdict'].title()} — unevaluable at power", "miss"),
        ("Autonomy", "omnibus 112 + spirits ARI", "—",
         f"{_AUT['verdict'].title()} — silhouette {_OMNI['silhouette']:.4f} < 0.25", "miss"),
        ("Residual structure", "spirits primary", "Not supported",
         f"{_RES['verdict'].title()} — sensitivity arm diverges", "match"),
        ("Saturation degeneracy", "omnibus 112", "Supported",
         f"{_SAT['verdict'].title()} — direction reversed", "miss"),
    ],
    "net": ("Net", "verdict matrix", "Cell A (borrowed structure)",
            f"{_V['verdict_matrix_cell']} — {_V['verdict_matrix_cell_verdict']}", "net"),
}

# ---------------------------------------------------------------------------
# HYPOTHESIS_DETAILS — per-hypothesis stat paragraphs (exact numbers from SSOT).
HYPOTHESIS_DETAILS = {
    "heading": "The numbers behind the verdicts",
    "intro": "For readers checking the work against the deposited record "
             "(osf.io/ec6wh/v36). All statistics are reproducible from the locked "
             f"scorer at seed {_V['metadata']['seed']}.",
    "items": [
        ("inheritance",
         "<b>Inheritance.</b> Gap selection chose k=" f"{_K['v23_raw']}"
         " on the nine defined premium-spirits units — a single cluster — "
         f"so the Adjusted Rand Index against the presence-quartile regime is "
         f"{_INH['ari']:.2f} (null percentile {_INH['ari_null_pct']:.0f}, "
         f"p={_INH['ari_p']:.2f}). With one forced cluster, zero agreement is "
         "mechanical, not evidential."),
        ("autonomy",
         "<b>Autonomy.</b> Across all 112 units gap selected k=" f"{_K['omnibus_raw']}"
         f"; mean silhouette {_OMNI['silhouette']:.4f} clears the permutation null "
         f"(null percentile {_OMNI['null_pct']:.0f}) but falls under the locked 0.25 "
         "bar. Above chance, below the line — not supported, no threshold relaxed."),
        ("residual",
         "<b>Residual structure.</b> Residualized on the presence composite, premium "
         f"spirits resolved to k={_K['v23_residual']} (no structure). The omnibus "
         f"mean-recall sensitivity arm resolved to k={_K['omnibus_mean_recall_residual']} "
         "and met the internal-validity criteria — but it is sensitivity-only and "
         "never verdict-determining."),
        ("saturation",
         "<b>Saturation degeneracy.</b> Within-substrate dispersion ran higher in "
         f"saturated categories ({_SAT['dev_mean_saturated']:.3f}) than unsaturated "
         f"({_SAT['dev_mean_unsaturated']:.3f}); Levene p={_SAT['bf_levene_p_two_sided']:.3f} "
         f"with the directional test at p={_SAT['bf_directional_p']:.4f} (wrong sign). "
         f"Per-substrate cluster resolution {_KSTR} also fails criterion (b). Both "
         "legs miss; the prediction reversed."),
    ],
}

# ---------------------------------------------------------------------------
CLOSING = (
    "A measurement program proves itself on the misses. The prediction was locked, "
    "timestamped, deposited, and wrong — and the falsification did more work than "
    "a confirmation would have: it located the failure inside the instrument rather "
    "than the brands, and specified the repair. Consistency remains a component worth "
    "building. v1.8 is where it gets an instrument that can carry it."
)
