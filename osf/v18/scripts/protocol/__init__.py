"""
protocol/ — canonical AIAS™ Presence Measurement Protocol implementation layer

This package is the SHARED, version-controlled implementation of the protocol.
Every per-phase script (acquire_phase_a_vNN.py, acquire_phase_b_vNN.py,
score_vNN.py) imports from here. New phases never copy-paste protocol logic;
they import it.

Layer separation:
  protocol/        — canonical, cross-phase implementation (this package)
  scripts/         — per-phase orchestration and configuration
  reports/         — per-phase report content and build
  osf/vNN/         — per-phase deposit (pre-reg + data + figures)

The protocol version is bumped when the canonical implementation changes
(see §"Methodology citation chain" — v1.2, v1.3, v1.4, ...).
Phase scripts pin the protocol version they were locked against.
"""

PROTOCOL_VERSION = "v1.4"
PROTOCOL_SSRN_ABSTRACT_ID = "6799479"
PROTOCOL_CITATION_CHAIN = {
    "foundational": "6659000",  # AI Availability — A Third System
    "v1.2": "6761698",           # Methodology Notes and Four-Regime Taxonomy
    "v1.3": "6797679",           # Phase A Pivot-Validation Specification
    "v1.4": "6799479",           # Recognition × Recall Decomposition
}
