"""
AIAS 1.0 Synthesis Paper — Cross-Phase Source-of-Truth Builder.

Builds osf/aias_1_0/aias_1_0_synthesis_data.json — the single artifact
that backs the synthesis paper's §4 prose and all §5 charts.

Pulls from:
  - osf/v20/v20_verdicts.json, osf/v21/v21_verdicts.json
    (dissociation counts, v1.4/v1.5 hypothesis verdicts)
  - methodology/v1_6/retrospective/v0_2{0,1}/v1_6_retrospective_v0_2{0,1}.json
    (v1.6 Increment 1 / 2 / 3 results)
  - PUBLISHED_REFERENCE (this file) for v0.16–v0.19, where v1.6 increments
    are out of retrospective scope per the v1.6-prereg-r1 boundary.

Boundary (locked at v1.6 §7):
  - Inc 1 (substrate pre-screen): narrative for v0.16–v0.19, scored for v0.20–v0.21.
  - Inc 2 (H_IdentityLoad_Direct): scored for v0.20–v0.21 only.
                                   v0.16–v0.19 lack R_cult.
  - Inc 3 (Phantom): scored for v0.21 only.

Lock: aias-1-0-outline-locked (2026-05-22).
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUTPUT_DIR = REPO / "osf" / "aias_1_0"
OUTPUT_PATH = OUTPUT_DIR / "aias_1_0_synthesis_data.json"

PHASE_ORDER = ["v0.16", "v0.17", "v0.18", "v0.19", "v0.20", "v0.21"]

# Per-phase static metadata. SSRN IDs from CLAUDE.md registry.
PHASE_META: dict[str, dict] = {
    "v0.16": {"substrate": "Kitchen knives",         "ssrn_id": "6791999", "panel_design": "3-cell IL-gradient"},
    "v0.17": {"substrate": "Premium kitchenware",    "ssrn_id": "6802261", "panel_design": "3-cell IL-gradient"},
    "v0.18": {"substrate": "Indie fragrance",        "ssrn_id": "6806558", "panel_design": "3-cell IL-gradient"},
    "v0.19": {"substrate": "Audiophile headphones",  "ssrn_id": "6809182", "panel_design": "2-cell uniform-IL"},
    "v0.20": {"substrate": "Skincare",               "ssrn_id": "6811441", "panel_design": "3-cell IL-gradient"},
    "v0.21": {"substrate": "Cosmetics",              "ssrn_id": "6815378", "panel_design": "3-cell IL-gradient"},
}

# Reference data for v0.16–v0.19. v1.6 increments do not apply (Inc 1
# narrative classification only; Inc 2 needs R_cult which was first
# acquired at v0.20; Inc 3 prospective-only from v0.22). Source: each
# phase's SSRN paper + the v1.6 §5 table_data file.
PUBLISHED_REFERENCE: dict[str, dict] = {
    "v0.16": {
        "v1_4_v1_5_verdicts": {
            "H_Regime4": {"verdict": "BOUNDARY", "note": "Original Regime 4 boundary phase; discourse-language carryforward documented."},
            "H_IdentityLoad_moderator_leg": "PARTIAL",
        },
        "dissociation_counts": {"iwachu": None, "type_1": None, "type_2": None, "note": "Pre-v1.4 framework; dissociation quadrants not formalized at acquisition."},
        "inc1_narrative_classification": "differential",
        "inc1_basis": "Published Phase A C_P distributions show within-cell variance across cells.",
        "inc2_status": "N/A — R_cult not collected (v1.5 prospective increment first acquired in v0.20).",
        "inc3_status": "N/A — Phantom out of v1.6 retrospective scope.",
        "source": "SSRN 6791999; v1.6 §5 table_data narrative.",
    },
    "v0.17": {
        "v1_4_v1_5_verdicts": {
            "H_Regime4": {"verdict": "FALSIFIED-on-panel-inadequacy", "note": "Panel inadequacy at the Recognition layer drove the verdict."},
            "H_IdentityLoad_moderator_leg": "FALSIFIED-on-panel-inadequacy",
            "H_Iwachu": {"note": "First Iwachu dissociation case named (Japanese knives recognized at high C_P but sparse canonical Recall)."},
        },
        "dissociation_counts": {"iwachu": "present (single-channel framework)", "type_1": None, "type_2": None,
                                  "note": "Iwachu pattern documented per-brand under v1.4 single-channel scoring; cross-quadrant counts not enumerated."},
        "inc1_narrative_classification": "differential",
        "inc1_basis": "Within-cell variance plus panel inadequacy; not uniform-saturation.",
        "inc2_status": "N/A — R_cult not collected.",
        "inc3_status": "N/A — Phantom out of v1.6 retrospective scope.",
        "source": "SSRN 6802261; v1.6 §5 table_data narrative.",
    },
    "v0.18": {
        "v1_4_v1_5_verdicts": {
            "H_Regime4": {"verdict": "PARTIAL", "note": "C_P modal share 0.69 worst cell; differential pattern."},
            "H_IdentityLoad_moderator_joint": "PARTIAL joint (3-leg with v0.16, v0.17)",
            "H_Iwachu_multi_cell": {"note": "First multi-cell Iwachu generalization in English-language substrate."},
        },
        "dissociation_counts": {"iwachu": "multi-cell (single-channel framework)", "type_1": None, "type_2": None,
                                  "note": "Iwachu pattern surfaces in ≥2 cells under v1.4 single-channel scoring."},
        "inc1_narrative_classification": "differential",
        "inc1_basis": "C_P modal share 0.69 worst cell; not uniform.",
        "inc2_status": "N/A — R_cult not collected.",
        "inc3_status": "N/A — Phantom out of v1.6 retrospective scope.",
        "source": "SSRN 6806558; v1.6 §5 table_data narrative.",
    },
    "v0.19": {
        "v1_4_v1_5_verdicts": {
            "H_Regime4": {"verdict": "UNDETERMINED", "note": "v1.4.x protocol; 2-cell Heritage/Boutique design; C2 FAILED → UNDETERMINED."},
            "H_IdentityLoad_moderator_leg": "Excluded from joint (uniform-IL design; no contribution).",
        },
        "dissociation_counts": {"iwachu": None, "type_1": None, "type_2": None,
                                  "note": "2-cell uniform-IL design; cross-quadrant dissociation framework not the focus."},
        "inc1_narrative_classification": "mixed",
        "inc1_basis": "Cell B modal_share 0.875 high but distinct ≠ 1 in either cell; not uniform-saturation.",
        "inc2_status": "N/A — single-channel q1–q6 design; no R_cult / R_cat decomposition at acquisition.",
        "inc3_status": "N/A — Phantom out of v1.6 retrospective scope.",
        "source": "SSRN 6809182; v1.6 §5 table_data narrative.",
    },
}


def load_json(path: Path) -> dict:
    with path.open() as f:
        return json.load(f)


def build_scored_phase(phase: str) -> dict:
    """v0.20 and v0.21: pull from verdict JSON + v1.6 retrospective JSON."""
    short = phase.replace("v0.", "v")              # v0.20 -> v20  (osf/ dirs)
    long  = phase.replace(".", "_")                # v0.20 -> v0_20 (methodology/ dirs)
    verdicts = load_json(REPO / "osf" / short / f"{short}_verdicts.json")
    retro_dir = REPO / "methodology" / "v1_6" / "retrospective" / long
    retro = load_json(retro_dir / f"v1_6_retrospective_{long}.json")

    dissoc = verdicts["dissociation"]
    inc1 = retro["increment_1_substrate_classification"] or {}
    inc2 = retro["increment_2_h_il_direct"] or {}
    inc3 = retro["increment_3_phantom"] or {}

    h_type2 = verdicts["hypotheses"]["H_Type2_emergence"]
    record: dict = {
        "phase": phase,
        "source_type": "scored",
        "v1_4_v1_5_verdicts": {
            "H_Type2_emergence": {
                "verdict":              h_type2["verdict"],
                "reason":               h_type2.get("reason"),
                "cell_b_n":             h_type2.get("cell_b_n"),
                "cell_b_type2_count":   h_type2.get("cell_b_type2_count"),
                "note":                 "verdict-driving Cell B count, per each phase's own prereg-r1 matrix; not the all-cell dissociation framework count below",
            },
            "H_Regime4":                               next(v["verdict"] for k, v in verdicts["hypotheses"].items() if k.startswith("H_Regime4")),
            "H_Dissociation_substrate_generalization": verdicts["hypotheses"]["H_Dissociation_substrate_generalization"]["verdict"],
            "H_IdentityLoad_moderator":                verdicts["hypotheses"]["H_IdentityLoad_moderator"]["verdict"],
        },
        "dissociation_counts": {
            "iwachu":  dissoc["iwachu_count"],
            "type_1":  dissoc["type_1_count"],
            "type_2":  dissoc["type_2_count"],
            "iwachu_cells": dissoc["iwachu_cells"],
            "type_1_cells": dissoc["type_1_cells"],
            "type_2_cells": dissoc["type_2_cells"],
            "_note": "All-cell algorithmic counts from each phase's own scoring. Distinct from cell_b_type2_count under v1_4_v1_5_verdicts.H_Type2_emergence, which drives the published PARTIAL/EMERGED/etc. verdict.",
        },
        "dissociation_brands": {
            "iwachu":  [{"brand": b["brand"], "cell": b["cell"], "r_cat": b["r_cat"], "r_cult": b["r_cult"]} for b in dissoc["iwachu"]],
            "type_1":  [{"brand": b["brand"], "cell": b["cell"], "r_cat": b["r_cat"], "r_cult": b["r_cult"]} for b in dissoc["type_1"]],
            "type_2":  [{"brand": b["brand"], "cell": b["cell"], "r_cat": b["r_cat"], "r_cult": b["r_cult"]} for b in dissoc["type_2"]],
        },
        "type_2_out_of_cell_cases": [
            {"brand": b["brand"], "cell": b["cell"], "r_cat": b["r_cat"], "r_cult": b["r_cult"]}
            for b in dissoc["type_2"] if b["cell"] != "B"
        ],
        "phase_b_per_cell": {
            cell: {
                "label":       data["label"],
                "il_tier":     data["il_tier"],
                "n":           data["n"],
                "mean_r_cat":  data["mean_r_cat"],
                "mean_r_cult": data["mean_r_cult"],
            }
            for cell, data in verdicts["phase_b"]["per_cell"].items()
        },
        "v1_6_retrospective": {
            "inc1": {
                "classification":           inc1["classification"],
                "distinct_cp_per_cell":     inc1["distinct_cp_per_cell"],
                "regime4_verdict_if_uniform_saturation": inc1.get("regime4_verdict_if_uniform_saturation"),
            },
            "inc2": {
                "verdict":  inc2.get("verdict"),
                "per_cell": inc2.get("per_cell", {}),
                "monotonic_gradient_check": inc2.get("monotonic_gradient_check"),
            },
            "inc3": (
                {
                    "verdict":                 inc3["verdict_resolution"]["verdict"],
                    "K":                       inc3["verdict_resolution"]["K"],
                    "off_panel_passing_count": inc3["verdict_resolution"]["off_panel_passing_count"],
                    "off_panel_passing":       inc3["verdict_resolution"]["off_panel_passing"],
                    "validity_check":          inc3["verdict_resolution"]["validity_check"],
                    "vocab_size":              inc3["scoring"]["vocab_size"],
                    "vocab_size_off_panel":    inc3["scoring"]["vocab_size_off_panel"],
                }
                if inc3 and inc3.get("verdict_resolution") else
                {"verdict": None, "status": "out of v1.6 retrospective scope"}
            ),
        },
        "source_paths": {
            "verdicts":      str((REPO / "osf" / short / f"{short}_verdicts.json").relative_to(REPO)),
            "retrospective": str((retro_dir / f"v1_6_retrospective_{phase.replace('.', '_')}.json").relative_to(REPO)),
        },
    }
    return record


def build_reference_phase(phase: str) -> dict:
    """v0.16–v0.19: encode published-paper reference data; no machine re-scoring."""
    ref = PUBLISHED_REFERENCE[phase]
    return {
        "phase": phase,
        "source_type": "published_reference",
        "v1_4_v1_5_verdicts":  ref["v1_4_v1_5_verdicts"],
        "dissociation_counts": ref["dissociation_counts"],
        "v1_6_retrospective": {
            "inc1": {
                "classification": ref["inc1_narrative_classification"],
                "basis":          ref["inc1_basis"],
            },
            "inc2": {"verdict": None, "status": ref["inc2_status"]},
            "inc3": {"verdict": None, "status": ref["inc3_status"]},
        },
        "source": ref["source"],
    }


def build_phase_records() -> list[dict]:
    records: list[dict] = []
    for phase in PHASE_ORDER:
        base = {"phase": phase, **PHASE_META[phase]}
        if phase in {"v0.20", "v0.21"}:
            base.update(build_scored_phase(phase))
        else:
            base.update(build_reference_phase(phase))
        records.append(base)
    return records


def build_cross_phase_summary(records: list[dict]) -> dict:
    """Aggregations consumed directly by §5 charts."""
    by_phase = {r["phase"]: r for r in records}

    def get(phase: str, *path):
        node = by_phase[phase]
        for key in path:
            node = node.get(key) if isinstance(node, dict) else None
            if node is None:
                return None
        return node

    def get_type2_verdict(phase: str):
        node = by_phase[phase].get("v1_4_v1_5_verdicts", {}).get("H_Type2_emergence")
        if isinstance(node, dict):
            return node.get("verdict")
        return node  # for v0.16–v0.19 published-reference shape (string or None)

    def get_type2_cell_b(phase: str):
        node = by_phase[phase].get("v1_4_v1_5_verdicts", {}).get("H_Type2_emergence")
        return node.get("cell_b_type2_count") if isinstance(node, dict) else None

    return {
        "_labeling_note": (
            "type_*_dissociation_count_by_phase reports the all-cell algorithmic count "
            "from each phase's own scoring (R_cat ≤ 2 ∧ R_cult ≥ 5 for Type 2, etc.). "
            "type_2_verdict_by_phase and type_2_cell_b_count_by_phase report the "
            "verdict-driving Cell B count per each phase's own prereg-r1 matrix — "
            "the number that maps to the published PARTIAL/EMERGED/FALSIFIED label. "
            "These can differ when out-of-cell cases exist (e.g., v0.20 La Mer in Cell A, "
            "v0.21 e.l.f. Cosmetics in Cell C). The published verdict is the authority."
        ),
        "iwachu_dissociation_count_by_phase": {
            p: get(p, "dissociation_counts", "iwachu") for p in PHASE_ORDER
        },
        "type_1_dissociation_count_by_phase": {
            p: get(p, "dissociation_counts", "type_1") for p in PHASE_ORDER
        },
        "type_2_dissociation_count_by_phase": {
            p: get(p, "dissociation_counts", "type_2") for p in PHASE_ORDER
        },
        "type_2_verdict_by_phase": {
            p: get_type2_verdict(p) for p in PHASE_ORDER
        },
        "type_2_cell_b_count_by_phase": {
            p: get_type2_cell_b(p) for p in PHASE_ORDER
        },
        "inc1_classification_by_phase": {
            p: get(p, "v1_6_retrospective", "inc1", "classification") for p in PHASE_ORDER
        },
        "il_direct_by_phase": {
            p: get(p, "v1_6_retrospective", "inc2", "verdict") for p in PHASE_ORDER
        },
        "phantom_by_phase": {
            p: get(p, "v1_6_retrospective", "inc3", "verdict") for p in PHASE_ORDER
        },
        "il_direct_deltas_by_phase_cell": {
            p: {
                cell: {"delta": data.get("delta"),
                       "ci_lo": data.get("ci_lo"),
                       "ci_hi": data.get("ci_hi"),
                       "ci_excludes_zero": data.get("ci_excludes_zero")}
                for cell, data in (get(p, "v1_6_retrospective", "inc2", "per_cell") or {}).items()
            }
            for p in PHASE_ORDER
            if get(p, "v1_6_retrospective", "inc2", "per_cell")
        },
        "phantom_brands_v021": (
            get("v0.21", "v1_6_retrospective", "inc3", "off_panel_passing") or []
        ),
        "type_2_out_of_cell_cases_by_phase": {
            p: (by_phase[p].get("type_2_out_of_cell_cases") or [])
            for p in PHASE_ORDER
        },
        "phantom_channel_signatures_v021": [
            {"brand": b["brand"],
             "r_cat_phantom":  per_brand[b["brand"]]["r_cat_phantom"],
             "r_cult_phantom": per_brand[b["brand"]]["r_cult_phantom"],
             "r_phantom":      b["r_phantom"]}
            for b in (get("v0.21", "v1_6_retrospective", "inc3", "off_panel_passing") or [])
            for per_brand in [
                load_json(REPO / "methodology" / "v1_6" / "retrospective" / "v0_21" /
                          "v1_6_retrospective_v0_21.json")["increment_3_phantom"]["scoring"]["per_brand"]
            ]
        ],
    }


def build_claim_layer_support(records: list[dict]) -> dict:
    """L1–L7 claim-layer support map for §5 narrative."""
    by_phase = {r["phase"]: r for r in records}

    def has_iwachu(phase: str) -> bool:
        v = by_phase[phase].get("dissociation_counts", {}).get("iwachu")
        return isinstance(v, int) and v > 0 or (isinstance(v, str) and "present" in v.lower() or isinstance(v, str) and "multi" in v.lower())

    return {
        "L1_third_layer":                       PHASE_ORDER,
        "L2_multi_component_recognition_recall": PHASE_ORDER,
        "L3_two_channel":                       ["v0.20", "v0.21"],
        "L4_three_quadrants": {
            "iwachu_support":            [p for p in PHASE_ORDER if has_iwachu(p)],
            "type_1_support":            [p for p in ["v0.20", "v0.21"]
                                          if (by_phase[p].get("dissociation_counts", {}).get("type_1") or 0) > 0],
            "type_2_cell_b_support":     [p for p in ["v0.20", "v0.21"]
                                          if (by_phase[p].get("v1_4_v1_5_verdicts", {}).get("H_Type2_emergence", {}).get("cell_b_type2_count") or 0) > 0],
            "type_2_emerged_published":  [p for p in ["v0.20", "v0.21"]
                                          if by_phase[p].get("v1_4_v1_5_verdicts", {}).get("H_Type2_emergence", {}).get("verdict") == "EMERGED"],
        },
        "L5_il_moderator":                      ["v0.18", "v0.20", "v0.21"],
        "L5_il_direct_confirmed":               [p for p in ["v0.20", "v0.21"]
                                                 if by_phase[p].get("v1_6_retrospective", {}).get("inc2", {}).get("verdict") == "CONFIRMED"],
        "L6_phantom_persistence":               ["v0.21"],
        "L7_presence_only_with_roadmap":        "meta — applies to the whole construct, not anchored to specific phases.",
    }


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    records = build_phase_records()
    output = {
        "metadata": {
            "paper": "AIAS 1.0 Synthesis",
            "lock_state": "aias-1-0-outline-locked",
            "lock_date":  "2026-05-22",
            "generated":  datetime.now(timezone.utc).isoformat(),
            "v1_6_boundary": {
                "inc1": "narrative for v0.16–v0.19, scored for v0.20–v0.21",
                "inc2": "scored for v0.20–v0.21 only; v0.16–v0.19 lack R_cult",
                "inc3": "scored for v0.21 only",
            },
            "verdict_discipline": (
                "Each phase's published verdict (PARTIAL/EMERGED/CONFIRMED/FALSIFIED/etc.) "
                "stands as the authority. The builder does NOT re-apply later-version "
                "thresholds retrospectively (D4 boundary). Where multiple counts could be "
                "reported (e.g., Type 2 all-cell dissociation count vs. verdict-driving "
                "Cell B count), both are surfaced with explicit labeling; the verdict "
                "label remains the authority for §4 prose."
            ),
            "cross_phase_synthesis_contributions": [
                {
                    "topic": "Out-of-cell Type 2 as a cross-phase recurrent feature of the dissociation framework",
                    "contribution": (
                        "The synthesis's cross-phase all-cell dissociation count "
                        "surfaces out-of-cell Type 2 cases that per-phase "
                        "Cell-B-anchored verdict matrices correctly did not "
                        "surface within their own scope. v0.20 La Mer "
                        "(Cell A — Prestige; C_P=6, R_cat=2, R_cult=7) and v0.21 "
                        "e.l.f. Cosmetics (Cell C — Drugstore/mass; C_P=6, R_cat=1, "
                        "R_cult=9) jointly establish out-of-cell Type 2 as a "
                        "recurrent feature of the dissociation framework across "
                        "substrate families. The per-phase Cell B verdicts (PARTIAL "
                        "for v0.20, EMERGED for v0.21) stand as the authoritative "
                        "within-phase results; the synthesis adds the cross-phase "
                        "algorithmic perspective alongside them."
                    ),
                    "framing": (
                        "Synthesis-layer contribution, not a correction to prior "
                        "work. The pattern is visible only at the cross-phase view; "
                        "no per-phase paper could have surfaced it within its own "
                        "scope because each phase's verdict matrix is correctly "
                        "Cell-B-anchored by construction."
                    ),
                    "synthesis_handling": (
                        "§4.4 (v0.20 anchor) and §4.5 (v0.21 anchor) surface both "
                        "cases under the all-cell dissociation framework while "
                        "preserving each phase's published verdict as the authority "
                        "for its own H_Type2_emergence label. No erratum on either "
                        "phase's SSRN deposit."
                    ),
                    "captured_at": "aias-1-0-data-build (step 2, post-La-Mer-verification)",
                },
            ],
            "source_files": [
                "osf/v20/v20_verdicts.json",
                "osf/v21/v21_verdicts.json",
                "methodology/v1_6/retrospective/v0_20/v1_6_retrospective_v0_20.json",
                "methodology/v1_6/retrospective/v0_21/v1_6_retrospective_v0_21.json",
                "PUBLISHED_REFERENCE (embedded in scripts/aias_1_0_synthesis_data.py for v0.16–v0.19)",
            ],
        },
        "phases":                records,
        "cross_phase_summary":   build_cross_phase_summary(records),
        "claim_layer_support":   build_claim_layer_support(records),
    }
    with OUTPUT_PATH.open("w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
        f.write("\n")

    # Verification report to stdout.
    print(f"Wrote {OUTPUT_PATH.relative_to(REPO)}")
    print(f"  phases: {len(records)}")
    print()
    print("Cross-phase summary:")
    cps = output["cross_phase_summary"]
    print(f"  Iwachu (dissociation count) by phase:      {cps['iwachu_dissociation_count_by_phase']}")
    print(f"  Type 1 (dissociation count) by phase:      {cps['type_1_dissociation_count_by_phase']}")
    print(f"  Type 2 (dissociation count, all cells):    {cps['type_2_dissociation_count_by_phase']}")
    print(f"  Type 2 Cell B count (verdict-driving):     {cps['type_2_cell_b_count_by_phase']}")
    print(f"  Type 2 published verdict by phase:         {cps['type_2_verdict_by_phase']}")
    print(f"  Inc 1 classification by phase:             {cps['inc1_classification_by_phase']}")
    print(f"  H_IL_Direct verdict by phase:              {cps['il_direct_by_phase']}")
    print(f"  Phantom verdict by phase:                  {cps['phantom_by_phase']}")
    print()
    print("Claim-layer support:")
    cl = output["claim_layer_support"]
    print(f"  L3 two-channel:                            {cl['L3_two_channel']}")
    print(f"  L4 Iwachu support:                         {cl['L4_three_quadrants']['iwachu_support']}")
    print(f"  L4 Type 1 support:                         {cl['L4_three_quadrants']['type_1_support']}")
    print(f"  L4 Type 2 Cell B support (any cases):      {cl['L4_three_quadrants']['type_2_cell_b_support']}")
    print(f"  L4 Type 2 EMERGED (published verdict):     {cl['L4_three_quadrants']['type_2_emerged_published']}")
    print(f"  L5 IL Direct CONFIRMED:                    {cl['L5_il_direct_confirmed']}")
    print(f"  L6 Phantom:                                {cl['L6_phantom_persistence']}")
    print()
    print("Type 2 out-of-cell cases by phase (algorithmic; not in verdict's Cell B count):")
    for p, cases in cps["type_2_out_of_cell_cases_by_phase"].items():
        if cases:
            for c in cases:
                print(f"  {p}: {c['brand']:<22} cell={c['cell']}  R_cat={c['r_cat']}  R_cult={c['r_cult']}")
    print()
    print("v0.21 Phantom off-panel passing brands:")
    for b in cps["phantom_brands_v021"]:
        print(f"  {b['brand']:<22} R_phantom = {b['r_phantom']}")
    print()
    print("Cross-phase synthesis contributions flagged:")
    for c in output["metadata"]["cross_phase_synthesis_contributions"]:
        print(f"  - {c['topic']}")
        print(f"    Framing: {c['framing']}")


if __name__ == "__main__":
    main()
