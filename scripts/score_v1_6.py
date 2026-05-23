#!/usr/bin/env python3
"""score_v1_6.py — AIAS v1.6 methodology-version retrospective scorer.

Methodology-version scorer (not a phase scorer). Locked at v1.6-prereg-r1.
Applies the three v1.6 increments to any phase's Phase A + Phase B data:

  Increment 1 — Substrate-level Recognition pre-screen.
    Classification rule: distinct C_P count = 1 in all 3 cells → uniform-saturation.
    Otherwise → differential. Uniform-saturation routes to a single substrate-level
    verdict REGIME-4-UNAVAILABLE-AT-RECOGNITION (distinct from FALSIFIED).

  Increment 2 — H_IdentityLoad_Direct (parallel to H_IdentityLoad_moderator).
    Per cell: δ = mean(R_cult) − mean(R_cat); bootstrap percentile CI,
    n_bootstrap = 10,000, per-cell resampling with replacement.
    Retrospective seed: SEED_V16_RETRO = 1621.
    Verdict matrix (CONFIRMED / PARTIAL / FALSIFIED / INDETERMINATE) per the locked
    IL-gradient prediction with monotonic-gradient check on Cell C.

  Increment 3 — Phantom Brand Persistence Phase B extension.
    R_phantom per off-panel reference-vocabulary brand: count of mentions across
    36 Phase B responses; K = 6 persistence threshold.
    Reference vocabulary: panel + top-50 substrate market-share list +
    cross-validated emergents (Phase-B-only candidates excluded).
    Retrospective scope: v0.21 only (vocabulary files for v0.16–v0.20 out of
    v1.6 scope). Validity check: v0.21 Glossier R_phantom ≥ 6 required.

Reuses v1.4 canonical mention detection and v1.5 Phase A/B loaders from the
score_vNN.py series.

Output: v1_6_retrospective_<phase>.json under
  ~/aias/methodology/v1_6/retrospective/<phase>/

Required pip packages:
    numpy   (for bootstrap)

Usage:
    python score_v1_6.py --phase v0.21
    python score_v1_6.py --phase v0.16 --no-phantom
    python score_v1_6.py --phase v0.21 --registry <path> --phase-a <csv> --phase-b <csv>
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import unicodedata
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

# --- v1.6-prereg-r1 LOCKED CONSTANTS -----------------------------------------

SEED_V16_RETRO = 1621             # Methodology-level seed for retrospective scoring
N_BOOTSTRAP = 10_000              # Locked n_bootstrap
BOOTSTRAP_CI_METHOD = "percentile"  # Locked (not BCa)
K_PHANTOM = 6                     # Locked persistence threshold (mentions across 36 responses)
UNIFORM_SATURATION_RULE = "distinct_eq_1_in_all_3_cells"
PROTOCOL_VERSION = "v1.6"
PREREG_TAG = "v1.6-prereg-r1"

# Paths
AIAS_ROOT = Path.home() / "aias"
OSF_ROOT = AIAS_ROOT / "osf"
METHOD_ROOT = AIAS_ROOT / "methodology" / "v1_6"
VOCAB_DIR = METHOD_ROOT / "reference_vocabs"
RETRO_OUT_ROOT = METHOD_ROOT / "retrospective"

# Phase → OSF directory mapping (handles v0.21 ↔ v21 naming convention)
PHASE_TO_OSF_DIR = {
    "v0.16": "v16",
    "v0.17": "v17",
    "v0.18": "v18",
    "v0.19": "v19",
    "v0.20": "v20",
    "v0.21": "v21",
}

# Phase → registry filename mapping
PHASE_TO_REGISTRY = {
    "v0.16": "prereg/v0_16_registry.json",
    "v0.17": "prereg/v0_17_registry.json",
    "v0.18": "prereg/v0_18_registry.json",
    "v0.19": "prereg/v0_19_registry.json",
    "v0.20": "prereg/v0_20_registry.json",
    "v0.21": "prereg/v0_21_registry.json",
}


# --- v1.4 canonical brand-mention detection (reused from score_v21.py) -------

def _normalize(s: str) -> str:
    """Lowercase and strip diacritics (e.g., 'Estée' → 'estee')."""
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return s.lower()


def detect_mention(response_text: str, brand_name: str) -> bool:
    """v1.4 canonical mention detection: case-insensitive, accent-stripped,
    word-boundary anchored (handles possessives, blocks substring false-positives)."""
    if not response_text or not brand_name:
        return False
    norm_text = _normalize(response_text)
    norm_brand = _normalize(brand_name)
    pattern = r"\b" + re.escape(norm_brand) + r"\b"
    return bool(re.search(pattern, norm_text))


# --- Loaders -----------------------------------------------------------------

def load_registry(path: Path) -> dict:
    with open(path) as f:
        return json.load(f)


def load_csv(path: Path) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _registry_cells(registry: dict):
    """v1.5+ registries use cells as a dict; some older variants used a list.
    Normalize to (cell_id, cell_dict) iterator."""
    cells = registry["cells"]
    if isinstance(cells, dict):
        for cell_id, cell in cells.items():
            yield cell_id, cell
    else:
        for cell in cells:
            yield cell["id"], cell


# --- Phase A: per-brand C_P + per-cell distributional stats ------------------

def compute_cp(phase_a_rows: list[dict], registry: dict) -> dict:
    """Per-brand C_P (Recognition score, max 6) + per-cell distinct/modal stats."""
    result = {"per_brand": {}, "per_cell": {}}
    for cell_id, cell in _registry_cells(registry):
        cell_brand_cps = []
        cell_data = {
            "label": cell.get("label", cell_id),
            "il_tier": cell.get("il_tier"),
            "brands": [],
        }
        for brand in cell["brands"]:
            brand_name = brand["name"] if isinstance(brand, dict) else brand
            cascade_order = brand.get("cascade_order") if isinstance(brand, dict) else None
            brand_rows = [r for r in phase_a_rows if r["brand"] == brand_name]
            cp = sum(1 for r in brand_rows if r["recognized"] == "yes")
            result["per_brand"][brand_name] = {
                "cell": cell_id,
                "cascade_order": cascade_order,
                "cp": cp,
                "panel_responses": len(brand_rows),
            }
            cell_data["brands"].append({"name": brand_name, "cp": cp})
            cell_brand_cps.append(cp)

        counter = Counter(cell_brand_cps)
        if cell_brand_cps:
            modal_cp, modal_freq = counter.most_common(1)[0]
            modal_share = modal_freq / len(cell_brand_cps)
            mean_cp = sum(cell_brand_cps) / len(cell_brand_cps)
        else:
            modal_cp, modal_share, mean_cp = None, 0.0, 0.0
        cell_data.update({
            "distinct_cp_count": len(counter),
            "modal_cp": modal_cp,
            "modal_cp_share": round(modal_share, 4),
            "mean_cp": round(mean_cp, 3),
            "n": len(cell_brand_cps),
        })
        result["per_cell"][cell_id] = cell_data
    return result


# --- Phase B: per-brand R_cat / R_cult --------------------------------------

def compute_recall(phase_b_rows: list[dict], registry: dict) -> dict:
    """Per-brand R_cat (canonical channel) and R_cult (cultural channel) mention counts."""
    result = {"per_brand": {}, "per_cell": {}}
    all_brands = []
    for cell_id, cell in _registry_cells(registry):
        for brand in cell["brands"]:
            brand_name = brand["name"] if isinstance(brand, dict) else brand
            all_brands.append({"name": brand_name, "cell": cell_id})

    for brand in all_brands:
        r_cat = 0
        r_cult = 0
        for row in phase_b_rows:
            if detect_mention(row["response_text"], brand["name"]):
                if row["channel"] == "R_cat":
                    r_cat += 1
                elif row["channel"] == "R_cult":
                    r_cult += 1
        result["per_brand"][brand["name"]] = {
            "cell": brand["cell"],
            "r_cat": r_cat,
            "r_cult": r_cult,
            "delta": r_cult - r_cat,
        }

    for cell_id, cell in _registry_cells(registry):
        cell_brand_names = [b["name"] if isinstance(b, dict) else b for b in cell["brands"]]
        r_cats = [result["per_brand"][n]["r_cat"] for n in cell_brand_names]
        r_cults = [result["per_brand"][n]["r_cult"] for n in cell_brand_names]
        deltas = [result["per_brand"][n]["delta"] for n in cell_brand_names]
        n = len(cell_brand_names)
        result["per_cell"][cell_id] = {
            "label": cell.get("label", cell_id),
            "il_tier": cell.get("il_tier"),
            "n": n,
            "mean_r_cat": round(sum(r_cats) / n, 3) if n else 0.0,
            "mean_r_cult": round(sum(r_cults) / n, 3) if n else 0.0,
            "mean_delta": round(sum(deltas) / n, 3) if n else 0.0,
            "brand_deltas": deltas,
        }
    return result


# --- Increment 1: substrate classification (LOCKED) --------------------------

def classify_substrate(cp_data: dict) -> dict:
    """Locked rule: distinct C_P count = 1 in all 3 cells → uniform-saturation.
    Otherwise → differential."""
    distincts = {cid: cell["distinct_cp_count"] for cid, cell in cp_data["per_cell"].items()}
    all_distinct_eq_1 = all(d == 1 for d in distincts.values())
    classification = "uniform-saturation" if all_distinct_eq_1 else "differential"
    routing = (
        "bypass C2; collapse to REGIME-4-UNAVAILABLE-AT-RECOGNITION; "
        "moderator via H_IdentityLoad_Direct"
        if classification == "uniform-saturation"
        else "standard C1 → C2 → IL-gradient guard → C3 sequence (v1.5)"
    )
    return {
        "rule": UNIFORM_SATURATION_RULE,
        "distinct_cp_per_cell": distincts,
        "classification": classification,
        "routing": routing,
        "regime4_verdict_if_uniform_saturation":
            "REGIME-4-UNAVAILABLE-AT-RECOGNITION" if classification == "uniform-saturation" else None,
    }


# --- Increment 2: H_IdentityLoad_Direct (LOCKED) -----------------------------

def _bootstrap_percentile_ci(values: list[int], n_iter: int, seed: int,
                              alpha: float = 0.05) -> tuple[float, float, float]:
    """Bootstrap percentile CI for the mean of `values`.
    Returns (mean, lo, hi) at (1−alpha) confidence."""
    try:
        import numpy as np
    except ImportError:
        sys.exit("ERROR: numpy not installed. Run: python -m pip install numpy")
    if not values:
        return (0.0, 0.0, 0.0)
    rng = np.random.default_rng(seed)
    arr = np.asarray(values, dtype=float)
    n = len(arr)
    means = np.empty(n_iter, dtype=float)
    for i in range(n_iter):
        sample = rng.choice(arr, size=n, replace=True)
        means[i] = sample.mean()
    lo = float(np.percentile(means, 100 * alpha / 2))
    hi = float(np.percentile(means, 100 * (1 - alpha / 2)))
    return (float(arr.mean()), lo, hi)


def compute_h_il_direct(recall_data: dict, seed: int = SEED_V16_RETRO,
                         n_bootstrap: int = N_BOOTSTRAP) -> dict:
    """Per-cell δ = mean(R_cult) − mean(R_cat) with bootstrap percentile CI.

    Locked verdict matrix (v1.6-prereg-r1):
      CONFIRMED — Cell B δ > 0 CI excludes 0; Cell A δ < 0 CI excludes 0;
                  Cell C δ between Cell A δ and Cell B δ (monotonic-gradient passes).
      PARTIAL  — focal directions match but at least one CI overlaps 0,
                  OR Cell C gradient fails while focal CIs intact.
      FALSIFIED — Cell B δ ≤ 0 with CI excluding 0; OR Cell A δ ≥ 0 with CI excluding 0;
                  OR gradient fails with both focal CIs excluding 0 (irreconcilable).
      INDETERMINATE — brand-level n_post_attrition < 5 in any focal cell (A or B).
    """
    per_cell = {}
    for cell_id, cell in recall_data["per_cell"].items():
        deltas = cell["brand_deltas"]
        # Use a cell-derived seed so all cells share the same methodology seed but
        # produce independent reproducible samples.
        cell_seed = seed + ord(cell_id)
        mean_delta, lo, hi = _bootstrap_percentile_ci(deltas, n_bootstrap, cell_seed)
        per_cell[cell_id] = {
            "n": cell["n"],
            "mean_r_cat": cell["mean_r_cat"],
            "mean_r_cult": cell["mean_r_cult"],
            "delta": round(mean_delta, 3),
            "ci_lo": round(lo, 3),
            "ci_hi": round(hi, 3),
            "ci_excludes_zero": (lo > 0) or (hi < 0),
            "direction": "positive" if mean_delta > 0 else ("negative" if mean_delta < 0 else "zero"),
        }

    # Verdict resolution
    cell_a = per_cell.get("A")
    cell_b = per_cell.get("B")
    cell_c = per_cell.get("C")

    # INDETERMINATE guard
    if cell_a is None or cell_b is None:
        return {
            "per_cell": per_cell,
            "verdict": "INDETERMINATE",
            "reason": "Cell A or Cell B missing from registry",
        }
    if cell_a["n"] < 5 or cell_b["n"] < 5:
        return {
            "per_cell": per_cell,
            "verdict": "INDETERMINATE",
            "reason": (f"n_post_attrition: A={cell_a['n']}, B={cell_b['n']} "
                       f"(< 5 in focal cell)"),
        }

    # Monotonic gradient check (Cell C δ between A δ and B δ)
    if cell_c is not None:
        c_in_gradient = (cell_a["delta"] <= cell_c["delta"] <= cell_b["delta"])
    else:
        c_in_gradient = None  # not evaluable

    b_positive_ci_excl = cell_b["delta"] > 0 and cell_b["ci_excludes_zero"]
    a_negative_ci_excl = cell_a["delta"] < 0 and cell_a["ci_excludes_zero"]
    b_falsified = cell_b["delta"] <= 0 and cell_b["ci_excludes_zero"]
    a_falsified = cell_a["delta"] >= 0 and cell_a["ci_excludes_zero"]
    focal_directions_ok = cell_a["delta"] < 0 and cell_b["delta"] > 0

    # FALSIFIED paths
    if b_falsified or a_falsified:
        verdict = "FALSIFIED"
        reason = ("Focal-cell direction contradicts IL-gradient prediction with CI exclusion: "
                  f"Cell A δ = {cell_a['delta']}, Cell B δ = {cell_b['delta']}")
    elif (c_in_gradient is False) and b_positive_ci_excl and a_negative_ci_excl:
        verdict = "FALSIFIED"
        reason = ("Both focal CIs exclude zero but Cell C breaks monotonic-gradient — "
                  f"A={cell_a['delta']}, C={cell_c['delta']}, B={cell_b['delta']}")
    elif b_positive_ci_excl and a_negative_ci_excl and (c_in_gradient is True):
        verdict = "CONFIRMED"
        reason = ("Focal CIs exclude zero in IL-predicted directions; Cell C monotonic-gradient passes "
                  f"(A={cell_a['delta']}, C={cell_c['delta']}, B={cell_b['delta']})")
    elif b_positive_ci_excl and a_negative_ci_excl and c_in_gradient is None:
        verdict = "CONFIRMED"
        reason = "Focal CIs exclude zero in IL-predicted directions; no Cell C present (gradient n/a)"
    elif focal_directions_ok:
        # Direction matches both focal cells but at least one CI overlaps zero, OR Cell C fails
        verdict = "PARTIAL"
        reason_parts = []
        if not (b_positive_ci_excl and a_negative_ci_excl):
            ci_status = []
            if not b_positive_ci_excl:
                ci_status.append(f"Cell B CI [{cell_b['ci_lo']}, {cell_b['ci_hi']}] overlaps 0")
            if not a_negative_ci_excl:
                ci_status.append(f"Cell A CI [{cell_a['ci_lo']}, {cell_a['ci_hi']}] overlaps 0")
            reason_parts.append("; ".join(ci_status))
        if c_in_gradient is False:
            reason_parts.append(f"Cell C breaks monotonic-gradient (C={cell_c['delta']})")
        reason = "Focal directions match IL prediction; " + " | ".join(reason_parts)
    else:
        verdict = "PARTIAL"
        reason = (f"Mixed signal: Cell A δ={cell_a['delta']}, Cell B δ={cell_b['delta']} "
                  f"(no clear FALSIFIED or CONFIRMED path)")

    return {
        "per_cell": per_cell,
        "monotonic_gradient_check": c_in_gradient,
        "verdict": verdict,
        "reason": reason,
        "bootstrap": {
            "n_iter": n_bootstrap,
            "ci_method": BOOTSTRAP_CI_METHOD,
            "seed_base": seed,
            "per_cell_seed_offset": "ord(cell_id)",
        },
    }


# --- Increment 3: Phantom Brand Persistence (LOCKED) -------------------------

def load_reference_vocab(substrate: str, vocab_dir: Path) -> dict | None:
    """Load locked reference vocabulary for a substrate. Returns None if absent."""
    candidate = vocab_dir / f"{substrate}_v021.json"
    if not candidate.exists():
        # Try generic substrate name
        candidate = vocab_dir / f"{substrate}.json"
    if not candidate.exists():
        return None
    with open(candidate) as f:
        return json.load(f)


def compute_phantom(phase_b_rows: list[dict], vocab: dict, panel_brand_names: list[str]) -> dict:
    """Scan Phase B responses against full reference vocabulary; per-brand R_phantom.
    Off-panel brands counted toward H_PhantomBrandPersistence verdict."""
    all_vocab_brands = list({*vocab.get("panel_brands", []),
                             *vocab.get("market_share_brands", []),
                             *vocab.get("cross_validated_emergents", [])})
    panel_set = set(panel_brand_names)

    per_brand = {}
    for brand_name in all_vocab_brands:
        r_cat_phantom = 0
        r_cult_phantom = 0
        for row in phase_b_rows:
            if detect_mention(row["response_text"], brand_name):
                if row["channel"] == "R_cat":
                    r_cat_phantom += 1
                elif row["channel"] == "R_cult":
                    r_cult_phantom += 1
        r_phantom = r_cat_phantom + r_cult_phantom
        per_brand[brand_name] = {
            "is_panel": brand_name in panel_set,
            "r_cat_phantom": r_cat_phantom,
            "r_cult_phantom": r_cult_phantom,
            "r_phantom": r_phantom,
        }

    off_panel_passing = sorted(
        [(b, d["r_phantom"]) for b, d in per_brand.items()
         if not d["is_panel"] and d["r_phantom"] >= K_PHANTOM],
        key=lambda x: -x[1],
    )

    return {
        "vocab_size": len(all_vocab_brands),
        "vocab_size_off_panel": len([b for b in all_vocab_brands if b not in panel_set]),
        "K_threshold": K_PHANTOM,
        "per_brand": per_brand,
        "off_panel_passing": [{"brand": b, "r_phantom": r} for b, r in off_panel_passing],
        "off_panel_passing_count": len(off_panel_passing),
    }


def resolve_phantom_verdict(phantom: dict, calibration_anchor: dict | None = None) -> dict:
    """H_PhantomBrandPersistence: ≥1 off-panel reference-vocab brand with R_phantom ≥ K → CONFIRMED."""
    count = phantom["off_panel_passing_count"]
    verdict = "CONFIRMED" if count >= 1 else "ABSENT"
    reason = f"{count} off-panel brand(s) with R_phantom ≥ {K_PHANTOM}"
    result = {
        "verdict": verdict,
        "reason": reason,
        "K": K_PHANTOM,
        "off_panel_passing_count": count,
        "off_panel_passing": phantom["off_panel_passing"],
    }
    # Validity check: v0.21 Glossier anchor
    if calibration_anchor:
        anchor_brand = calibration_anchor["brand"]
        anchor_min = calibration_anchor["min_r_phantom"]
        anchor_score = phantom["per_brand"].get(anchor_brand, {}).get("r_phantom", -1)
        anchor_passes = anchor_score >= anchor_min
        result["validity_check"] = {
            "anchor": anchor_brand,
            "anchor_min_required": anchor_min,
            "anchor_observed": anchor_score,
            "passes": anchor_passes,
            "note": ("Per v1.6-prereg-r1: failure triggers pre-reg amendment, "
                     "not silent re-tuning."),
        }
    return result


# --- Main --------------------------------------------------------------------

def resolve_paths(phase: str, args) -> dict:
    """Auto-discover paths from --phase, with explicit overrides taking precedence."""
    osf_dir_name = PHASE_TO_OSF_DIR.get(phase)
    if not osf_dir_name and (args.phase_a is None or args.phase_b is None
                              or args.registry is None):
        sys.exit(f"ERROR: unknown phase {phase}; provide --registry, --phase-a, --phase-b explicitly")
    osf_dir = OSF_ROOT / osf_dir_name if osf_dir_name else None
    registry_path = (Path(args.registry) if args.registry
                      else AIAS_ROOT / PHASE_TO_REGISTRY[phase])
    phase_a_path = (Path(args.phase_a) if args.phase_a
                     else osf_dir / "phase_a_results.csv")
    phase_b_path = (Path(args.phase_b) if args.phase_b
                     else osf_dir / "phase_b_results.csv")
    output_path = (Path(args.output) if args.output
                    else RETRO_OUT_ROOT / phase.replace(".", "_")
                        / f"v1_6_retrospective_{phase.replace('.', '_')}.json")
    return {
        "registry": registry_path,
        "phase_a": phase_a_path,
        "phase_b": phase_b_path,
        "output": output_path,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="AIAS v1.6 retrospective scorer")
    parser.add_argument("--phase", required=True,
                        help="Phase identifier (e.g., v0.21, v0.20, v0.16)")
    parser.add_argument("--registry", help="Override registry JSON path")
    parser.add_argument("--phase-a", help="Override Phase A CSV path")
    parser.add_argument("--phase-b", help="Override Phase B CSV path")
    parser.add_argument("--vocab-dir", default=str(VOCAB_DIR),
                        help=f"Reference vocabulary directory (default: {VOCAB_DIR})")
    parser.add_argument("--no-phantom", action="store_true",
                        help="Skip Increment 3 (Phantom scoring); useful for v0.16–v0.20")
    parser.add_argument("--output", help="Override verdicts JSON output path")
    args = parser.parse_args()

    phase = args.phase
    paths = resolve_paths(phase, args)
    for p, label in [(paths["registry"], "registry"),
                     (paths["phase_a"], "Phase A CSV"),
                     (paths["phase_b"], "Phase B CSV")]:
        if not p.exists():
            print(f"ERROR: {label} not found at {p}", file=sys.stderr)
            return 2

    registry = load_registry(paths["registry"])
    phase_a_rows = load_csv(paths["phase_a"])
    phase_b_rows = load_csv(paths["phase_b"])
    substrate = registry.get("substrate", "unknown")

    print(f"AIAS v1.6 retrospective scorer ({PREREG_TAG})")
    print(f"  Phase:        {phase} ({substrate})")
    print(f"  Registry:     {paths['registry']}")
    print(f"  Phase A CSV:  {paths['phase_a']}  ({len(phase_a_rows)} rows)")
    print(f"  Phase B CSV:  {paths['phase_b']}  ({len(phase_b_rows)} rows)")

    # Phase A + Phase B base computations
    print("\n[1/5] Phase A C_P computation...")
    cp_data = compute_cp(phase_a_rows, registry)
    for cid, c in cp_data["per_cell"].items():
        print(f"      Cell {cid}: mean C_P = {c['mean_cp']:.2f}, "
              f"distinct = {c['distinct_cp_count']}, "
              f"modal_share = {c['modal_cp_share']:.3f}")

    print("\n[2/5] Phase B R_cat/R_cult (v1.4 mention detection)...")
    recall_data = compute_recall(phase_b_rows, registry)
    for cid, c in recall_data["per_cell"].items():
        print(f"      Cell {cid}: mean R_cat = {c['mean_r_cat']:.2f}, "
              f"mean R_cult = {c['mean_r_cult']:.2f}, "
              f"mean δ = {c['mean_delta']:.2f}")

    # Increment 1: substrate classification
    print("\n[3/5] Increment 1: substrate classification (locked rule)...")
    inc1 = classify_substrate(cp_data)
    print(f"      Classification: {inc1['classification']}")
    print(f"      Routing:        {inc1['routing']}")

    # Increment 2: H_IdentityLoad_Direct
    print(f"\n[4/5] Increment 2: H_IdentityLoad_Direct bootstrap (n={N_BOOTSTRAP}, "
          f"seed_base={SEED_V16_RETRO})...")
    inc2 = compute_h_il_direct(recall_data, seed=SEED_V16_RETRO, n_bootstrap=N_BOOTSTRAP)
    for cid, c in inc2["per_cell"].items():
        ci_marker = "excl 0" if c["ci_excludes_zero"] else "incl 0"
        print(f"      Cell {cid}: δ = {c['delta']:+.2f}, "
              f"CI = [{c['ci_lo']:+.2f}, {c['ci_hi']:+.2f}] ({ci_marker})")
    print(f"      → H_IdentityLoad_Direct verdict: {inc2['verdict']}")
    print(f"        ({inc2['reason']})")

    # Increment 3: Phantom (v0.21 only, or any phase with vocabulary file)
    inc3 = None
    if not args.no_phantom:
        vocab_dir = Path(args.vocab_dir)
        vocab = load_reference_vocab(substrate, vocab_dir)
        if vocab is None:
            print(f"\n[5/5] Increment 3: SKIPPED (no reference vocabulary for substrate "
                  f"'{substrate}' in {vocab_dir})")
        else:
            print(f"\n[5/5] Increment 3: Phantom scoring (vocab: {vocab.get('substrate')} "
                  f"v{vocab.get('version', 'TBD')})...")
            panel_names = [b["name"] if isinstance(b, dict) else b
                            for _, cell in _registry_cells(registry)
                            for b in cell["brands"]]
            phantom = compute_phantom(phase_b_rows, vocab, panel_names)
            calibration = (vocab.get("validity_anchor") if phase == "v0.21" else None)
            inc3 = {
                "scoring": phantom,
                "verdict_resolution": resolve_phantom_verdict(phantom, calibration),
                "vocab_source": {k: vocab.get(k) for k in
                                  ("substrate", "version", "market_share_source",
                                   "panel_source", "constructed_at")},
            }
            print(f"      Vocabulary size: {phantom['vocab_size']} "
                  f"(off-panel: {phantom['vocab_size_off_panel']})")
            print(f"      Off-panel brands with R_phantom ≥ {K_PHANTOM}: "
                  f"{phantom['off_panel_passing_count']}")
            for entry in phantom["off_panel_passing"][:10]:
                print(f"        • {entry['brand']:40s} R_phantom = {entry['r_phantom']}")
            v = inc3["verdict_resolution"]
            print(f"      → H_PhantomBrandPersistence verdict: {v['verdict']}")
            if "validity_check" in v:
                vc = v["validity_check"]
                marker = "✓" if vc["passes"] else "✗"
                print(f"      → Validity anchor ({vc['anchor']}): observed "
                      f"R_phantom = {vc['anchor_observed']}, required ≥ {vc['anchor_min_required']} {marker}")
    else:
        print("\n[5/5] Increment 3: SKIPPED (--no-phantom)")

    # --- Compose output ---
    output = {
        "phase": phase,
        "substrate": substrate,
        "protocol_version": PROTOCOL_VERSION,
        "lock_state": PREREG_TAG,
        "scoring_timestamp": datetime.now(timezone.utc).isoformat(),
        "inputs": {k: str(v) for k, v in paths.items()},
        "phase_a": cp_data,
        "phase_b": recall_data,
        "increment_1_substrate_classification": inc1,
        "increment_2_h_il_direct": inc2,
        "increment_3_phantom": inc3,
    }
    paths["output"].parent.mkdir(parents=True, exist_ok=True)
    with open(paths["output"], "w") as f:
        json.dump(output, f, indent=2, default=str)
    print(f"\n✓ Verdicts written: {paths['output']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
