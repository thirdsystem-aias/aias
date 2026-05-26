"""
v0.23 Automotive — AIAS™ Presence Measurement
==============================================

Pre-Registration r2  (supersedes r1)
------------------------------------
Tag: v0.23-prereg-r2
Methodology lock: v1.6 (SSRN 6816340)
Carry-forward: v1.5 two-channel Recall (SSRN 6810758),
               v1.2 four-regime taxonomy (SSRN 6761698)

Amendment summary (r1 → r2)
---------------------------
r1 locked INSTRUMENT as single-model GPT-4.1 × n=12 iterations.
This contradicted program convention from v0.17–v0.21, which
uses the 6-model reference panel (one response per model per
probe; max C_P = 6, max R_cat / R_cult = 18). The r1 spec was
a drafting error caught pre-acquisition. r2 corrects INSTRUMENT
to match v0.17–v0.21 convention. The H_Phantom_Defunct
threshold has been moved from N=3 (on the assumed max-12 scale)
to N=4 (on the corrected max-18 scale) to harmonize with the
H_Phantom_Brand_Persistence_heritage PARTIAL floor (4/18). No
acquisition data exists under r1; r2 is the operative lock.
See DEVIATIONS Entry 0 for full audit trail. r1 retained in
git history for reference (tag v0.23-prereg-r1).

Phase position: First prospective phase under v1.6 lock.
Substrate position: 6th anchor family
  (extends knives / kitchenware / indie fragrance /
   audiophile headphones / skincare / cosmetics).

Headline framing
----------------
Stress-test of Phantom Brand Persistence on the most
heritage-saturated substrate yet measured, with a
dedicated Cell D_Defunct panel of discontinued corporate
brands providing the pure-phantom upper-bound test.

Locked decisions (D1–D9)
------------------------
D1 — 4-cell design adopted, including Cell D_Defunct.
D2 — 24-brand registry, 7 / 5 / 7 / 5 distribution.
D3 — Lead: H_Phantom_Defunct.
     Primary supporting: H_Phantom_Brand_Persistence_heritage.
D4 — Standard v1.6 supporting battery.
D5 — R_cult: "What car brands carry deep heritage,
              prestige, or a sense of legacy?"
D6 — Corporate-brand granularity only.
D7 — §COI standard disclosure (Harman / SDI / Display);
     no registry restriction.
D8 — Instrument: 6-model reference panel — claude-opus-4-5,
     claude-sonnet-4-5, gpt-4o, gpt-4o-mini, gemini-2.5-flash,
     gemini-2.5-flash-lite. One response per model per probe.
     [r2 correction; r1 locked single-model GPT-4.1 × n=12 in
      error — see DEVIATIONS Entry 0]
D9 — Pre-reg tag: v0.23-prereg-r2 (supersedes r1).

Hypothesis verdicts (locked falsification)
------------------------------------------
H_Phantom_Defunct (LEAD)
  CONFIRMED  any Cell D brand R_phantom_defunct >= 4
  PARTIAL    >=1 Cell D brand with 1 <= R_phantom_defunct < 4
  FALSIFIED  all Cell D brands R_phantom_defunct = 0
  [r2: threshold N moved 3 -> 4 to harmonize with the max-18
   scale of the 6-model panel; see DEVIATIONS Entry 0]

H_Phantom_Brand_Persistence_heritage (PRIMARY SUPPORTING)
  CONFIRMED  any Cell A brand R_phantom >= 8
  PARTIAL    >=1 Cell A brand with 4 <= R_phantom < 8
  FALSIFIED  all Cell A R_phantom < 4
  Benchmark: v0.21 Glossier R_phantom = 12.

H_Regime4_automotive
  Standard four-regime replication; predicted FALSIFIED
  on uniform Recognition saturation (cf. v0.21 cosmetics).

H_Dissoc_substrate_generalization
  GENERALIZED  >=1 dissociation case in Cells A or B
  PARTIAL      cases exist but in one cell only
  FALSIFIED    no dissociation cases

H_IdentityLoad_direct (v1.6 Inc2)
  CONFIRMED  Cell A mean IL > Cell B mean IL at locked threshold
  FALSIFIED  reversed or null
  Predicted CONFIRMED (high IL: A, D; low IL: B).

H_SubstrateRecognition_PreScreen (v1.6 Inc1)
  Methodological classification probe; non-directional.
  Predicted outcome: UNIFORM SATURATION across all 4 cells.

Conflict of interest
--------------------
Samsung Electronics America (author's employer) has
tier-2/3 supply relationships into automotive via
Harman International (audio: BMW, Mercedes, Volvo),
Samsung SDI (batteries: BMW, Stellantis), and Samsung
Display (infotainment: Mercedes, BMW). These are
non-competitive supply relationships and impose no
operational restriction on registry composition.
Disclosed in §COI of the v0.23 paper per program standard.

Author affiliation block (SSRN standard)
----------------------------------------
Pablo Ulpiano González Castro
SVA, MPS Branding Program, New York, NY
  (primary academic affiliation)
Third System™ (research entity; data archive and
  methodology venue)
Correspondence: pablou@pablou.com · pablou.com
ORCID: 0009-0003-8968-9990
"""

# ============================================================
# LOCKED REGISTRY — DO NOT MODIFY AFTER v0.23-prereg-r2
# ============================================================

REGISTRY = {
    "Cell_A_Heritage": [
        "Mercedes-Benz",
        "Jaguar",
        "Cadillac",
        "Rolls-Royce",
        "Bentley",
        "Porsche",
        "BMW",
    ],
    "Cell_B_Disruptor": [
        "Tesla",
        "Rivian",
        "Lucid",
        "Polestar",
        "Fisker",
    ],
    "Cell_C_Mass_Legacy": [
        "Toyota",
        "Honda",
        "Ford",
        "Chevrolet",
        "Hyundai",
        "Volkswagen",
        "Nissan",
    ],
    "Cell_D_Defunct": [
        "Pontiac",     # closed 2010
        "Oldsmobile",  # closed 2004
        "Plymouth",    # closed 2001
        "Mercury",     # closed 2010
        "Saturn",      # closed 2010
    ],
}

# ============================================================
# LOCKED PROBES
# ============================================================

PROBES = {
    "R_cat":  "What car brands come to mind?",
    "R_cult": (
        "What car brands carry deep heritage, "
        "prestige, or a sense of legacy?"
    ),
}

# ============================================================
# LOCKED INSTRUMENT (r2 — 6-model reference panel)
# ============================================================
#
# Six distinct LLMs, one response per model per probe.
# Panel architecture is unchanged from v0.17 onward.
# Per-brand C_P = yes-count across 6 models, range 0–6.
# Per-brand R_cat / R_cult = mentions across (3 probes × 6 models),
# max 18 per channel per brand.

INSTRUMENT = {
    "panel_models": [
        "claude-opus-4-5",
        "claude-sonnet-4-5",
        "gpt-4o",
        "gpt-4o-mini",
        "gemini-2.5-flash",
        "gemini-2.5-flash-lite",
    ],
    "panel_n": 6,                       # 6 distinct models
    "responses_per_model_per_probe": 1, # one response each
    "max_c_p": 6,                       # Phase A Recognition max
    "max_r_channel": 18,                # 3 probes × 6 models
    "temperature": None,                # Inherit v0.21 default at build time
    "date_window_days": 14,             # Acquisition within 14d of pre-reg
}

# ============================================================
# LOCKED HYPOTHESES
# ============================================================

HYPOTHESES = {
    "H_Phantom_Defunct": {
        "role": "LEAD",
        "operationalization": (
            "R_phantom_defunct(brand) = count of (model × R_cat probe) "
            "responses in which a Cell D brand appears unprompted "
            "across the 6-model panel × 3 R_cat probes (max 18 per "
            "brand). Cell D brands are presented in Phase A Recognition "
            "without temporal cues; R_phantom_defunct measures whether "
            "the panel surfaces these discontinued corporate brands "
            "in unprompted current-tense Recall."
        ),
        "verdicts": {
            "CONFIRMED": "any Cell D brand R_phantom_defunct >= 4",
            "PARTIAL":   "at least one Cell D brand with 1 <= R_phantom_defunct < 4",
            "FALSIFIED": "all Cell D brands R_phantom_defunct = 0",
        },
        "threshold_history": {
            "r1": "CONFIRMED >= 3 on assumed max-12 scale (single-model error)",
            "r2": "CONFIRMED >= 4 on corrected max-18 scale (6-model panel)",
        },
        "exploratory": (
            "R_cult-channel surfacing of Cell D brands as "
            "heritage-coded phantom (non-locked)."
        ),
    },
    "H_Phantom_Brand_Persistence_heritage": {
        "role": "PRIMARY_SUPPORTING",
        "operationalization": (
            "Standard v1.6 Inc3 R_phantom measurement on "
            "Cell A_Heritage brands (max 18 per brand)."
        ),
        "verdicts": {
            "CONFIRMED": "any Cell A brand R_phantom >= 8",
            "PARTIAL":   "at least one Cell A brand with 4 <= R_phantom < 8",
            "FALSIFIED": "all Cell A R_phantom < 4",
        },
        "benchmark": "v0.21 Glossier R_phantom = 12",
    },
    "H_Regime4_automotive": {
        "role": "SUPPORTING",
        "operationalization": (
            "Standard four-regime taxonomy replication test "
            "per v1.2 (SSRN 6761698)."
        ),
        "predicted": "FALSIFIED on uniform Recognition saturation",
    },
    "H_Dissoc_substrate_generalization": {
        "role": "SUPPORTING",
        "operationalization": (
            "Iwachu-anchored Recognition × Recall dissociation "
            "test extended to 6th substrate family."
        ),
        "verdicts": {
            "GENERALIZED": ">=1 dissociation case in Cell A or B",
            "PARTIAL":     "cases exist but in one cell only",
            "FALSIFIED":   "no dissociation cases",
        },
    },
    "H_IdentityLoad_direct": {
        "role": "SUPPORTING",
        "operationalization": (
            "v1.6 Inc2 R4-independent IL Direct bootstrap. "
            "Cell A vs Cell B mean IL comparison at locked threshold."
        ),
        "verdicts": {
            "CONFIRMED": "Cell A mean IL > Cell B mean IL at locked threshold",
            "FALSIFIED": "reversed or null",
        },
        "predicted": "CONFIRMED (high IL: A, D; low IL: B)",
    },
    "H_SubstrateRecognition_PreScreen": {
        "role": "METHODOLOGICAL_CLASSIFICATION",
        "operationalization": (
            "v1.6 Inc1 substrate Recognition pre-screen. "
            "Cell-level C_P saturation pattern (uniform vs differential)."
        ),
        "predicted": "UNIFORM SATURATION across all 4 cells",
        "note": "Non-directional classification probe.",
    },
}

# ============================================================
# DEVIATIONS LOG
# ============================================================

DEVIATIONS = {
    "entry_0_r1_to_r2_instrument_amendment": {
        "date": "2026-05-25",
        "screen_subject": (
            "INSTRUMENT specification and H_Phantom_Defunct "
            "threshold in v0.23-prereg-r1."
        ),
        "issue": (
            "r1 locked INSTRUMENT as single-model GPT-4.1 × n=12 "
            "iterations. This contradicts program convention from "
            "v0.17–v0.21 onward, which uses a 6-model reference "
            "panel (one response per model per probe; max C_P = 6, "
            "max R_cat / R_cult = 3 probes × 6 models = 18). The r1 "
            "spec arose from a Claude-assisted drafting error during "
            "the original lock session, deferred to under user trust "
            "without verification against v0.21 mega-prompt convention."
        ),
        "consequences_if_uncorrected": [
            "Cross-substrate Recognition comparability would break "
            "(C_P range 0–12 vs program-standard 0–6).",
            "Single-model iteration measures model-internal variance, "
            "not the AI mediation layer broadly — a core ecological-"
            "validity feature of the protocol.",
            "Build pipeline (build_charts_v23.py, build_report_v23.py) "
            "is already coded against the 6-model assumption "
            "(C_P max 6, R max 18) and would require methodology-"
            "level rework.",
            "Implicit methodology increment that v0.23 was not "
            "designed to introduce; v0.23 is a substrate phase, not "
            "a methodology phase.",
        ],
        "disposition": (
            "Amendment via v0.23-prereg-r2. Pre-acquisition defect "
            "catch; no data collected under r1. INSTRUMENT corrected "
            "to 6-model reference panel matching v0.17–v0.21 program "
            "convention. H_Phantom_Defunct threshold moved 3 → 4 to "
            "harmonize with the corrected max-18 scale and with the "
            "H_Phantom_Brand_Persistence_heritage PARTIAL floor "
            "(4/18 ≈ 22%). r1 retained in git history (tag "
            "v0.23-prereg-r1) for audit trail."
        ),
        "lock_state": (
            "v0.23-prereg-r2 supersedes v0.23-prereg-r1 as the "
            "operative pre-registration lock for v0.23 acquisition."
        ),
    },
}

# ============================================================
# CROSS-CITATION REGISTRY
# ============================================================

METHODOLOGY_LOCK = {
    "v1.6": "https://ssrn.com/abstract=6816340",
    "v1.5": "https://ssrn.com/abstract=6810758",
    "v1.4": "https://ssrn.com/abstract=6799479",
    "v1.3": "https://ssrn.com/abstract=6797679",
    "v1.2": "https://ssrn.com/abstract=6761698",
}

SYNTHESIS_REFERENCE = {
    "AIAS_1.0":    "https://ssrn.com/abstract=6817841",
    "foundational": "https://ssrn.com/abstract=6659000",
}

# ============================================================
# Build code, acquisition, scoring, charts — added in
# post-prereg commits via fork of v0.21 build pipeline.
# Registry / probes / instrument / hypotheses above are
# IMMUTABLE from this commit forward (v0.23-prereg-r2).
# ============================================================
