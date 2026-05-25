"""
v0.22 Automotive — AIAS™ Presence Measurement
==============================================

Pre-Registration r1
-------------------
Tag: v0.22-prereg-r1
Methodology lock: v1.6 (SSRN 6816340)
Carry-forward: v1.5 two-channel Recall (SSRN 6810758),
               v1.2 four-regime taxonomy (SSRN 6761698)

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
D8 — Instrument: GPT-4.1.
D9 — Pre-reg tag: v0.22-prereg-r1.

Hypothesis verdicts (locked falsification)
------------------------------------------
H_Phantom_Defunct (LEAD)
  CONFIRMED  any Cell D brand R_phantom_defunct >= 3
  PARTIAL    >=1 Cell D brand with 1 <= R_phantom_defunct < 3
  FALSIFIED  all Cell D brands R_phantom_defunct = 0

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
Disclosed in §COI of the v0.22 paper per program standard.

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
# LOCKED REGISTRY — DO NOT MODIFY AFTER v0.22-prereg-r1
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
# LOCKED INSTRUMENT
# ============================================================

INSTRUMENT = {
    "model": "gpt-4.1",
    "panel_n": 12,
    "temperature": None,  # Inherit v0.21 default at build time
    "date_window_days": 14,  # Acquisition within 14d of pre-reg
}

# ============================================================
# LOCKED HYPOTHESES
# ============================================================

HYPOTHESES = {
    "H_Phantom_Defunct": {
        "role": "LEAD",
        "operationalization": (
            "R_phantom_defunct(brand) = count of R_cat iterations "
            "in which a Cell D brand appears unprompted across "
            "the n=12 panel."
        ),
        "verdicts": {
            "CONFIRMED": "any Cell D brand R_phantom_defunct >= 3",
            "PARTIAL":   "at least one Cell D brand with 1 <= R_phantom_defunct < 3",
            "FALSIFIED": "all Cell D brands R_phantom_defunct = 0",
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
            "Cell A_Heritage brands."
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
    "AIAS_1.0": "https://ssrn.com/abstract=6817841",
    "foundational": "https://ssrn.com/abstract=6659000",
}

# ============================================================
# Build code, acquisition, scoring, charts — added in
# post-prereg commits via fork of v0.21 build pipeline.
# Registry / probes / instrument / hypotheses above are
# IMMUTABLE from this commit forward.
# ============================================================
