#!/usr/bin/env python3
"""
score_v0_63.py - AIAS(TM) v0.63: panel-construction sensitivity of the Recognition x Recall verdicts.

Pre-registered RE-ANALYSIS of the archived omnibus (v0.19-v0.23 at t1, t2, t3). No collection, no model
call, no network. Transcribes osf/v63/prereg/PRE_REGISTRATION_v0_63.md; the prose is authoritative and every
constant cites its section. A disagreement is a bug to fix toward the prose.

Modes (exactly one):
  --rules            write registries/panel_rules_v0_63.json from the locked registries ONLY (no answer is
                     read): the deterministic structural rules and the structural comparison count (sec 4, 8).
  --parity           pre-lock parity (sec 7): the loaders reproduce published per-brand Recognition / Recall
                     values and the published t1 verdicts. Writes prereg/parity_v0_63.json. Computes no
                     hypothesis statistic and no verdict that is not already published.
  --power            synthetic power / sensitivity check (sec 9). No archive file is opened.
  --lock-manifest    write prereg/LOCK_MANIFEST_v0_63.sha256
  --verify-lock      check every locked file against the manifest
  --write-anchor     after the tag is pushed and the OSF deposit is done: anchor/git_anchor_v0_63.json
  --run              the real scoring, ONCE. Refuses unless tag v0.63-prereg-r1 exists, the anchor file
                     exists, the lock manifest verifies and the parity file records a pass.
  --dry-run FILE     full scoring on a synthetic archive (JSON written by the tests); outputs next to FILE.

Root: this file lives at <root>/osf/v63/scripts/. The certified wave loader (osf/v41/scripts/score_v41.py
load_wave, which imports scripts/score_v0_31.py and scripts/score_v33.py) reads ~/aias; when ~/aias is not
<root> the archive modes re-execute this script with HOME pointing at a temporary folder whose 'aias' entry
links to <root> (the v0.41 shim, unchanged), so every module reads the same tree.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import subprocess
import sys
import tempfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
V63 = "osf/v63"

# ===========================================================================
# TRANSCRIBED CONSTANTS (section cited inline)
# ===========================================================================
PHASE_ID = "v0.63"
PREREG_TAG = "v0.63-prereg-r1"                         # sec 0
ANCHOR_FILE = ROOT / V63 / "anchor/git_anchor_v0_63.json"
LOCK_MANIFEST = ROOT / V63 / "prereg/LOCK_MANIFEST_v0_63.sha256"
RULES_FILE = ROOT / V63 / "registries/panel_rules_v0_63.json"
PARITY_FILE = ROOT / V63 / "prereg/parity_v0_63.json"
POWER_FILE = ROOT / V63 / "prereg/power_v0_63.json"
OUT_DIR = ROOT / V63 / "outputs"

OMNI = ["v0.19", "v0.20", "v0.21", "v0.22", "v0.23"]   # sec 3
WAVES = ["t1", "t2", "t3"]                             # sec 3
EXPECTED_BRANDS = {"v0.19": 16, "v0.20": 24, "v0.21": 24, "v0.22": 24, "v0.23": 24}   # sec 3 (112 per wave)
CELLED = ["v0.19", "v0.20", "v0.21", "v0.22"]          # sec 5.1: F1 and F3 defined
IL_GRADIENT = ["v0.20", "v0.21", "v0.22"]              # sec 5.1: IL guard and F2 defined
CAT_PREFIX = ("q1", "q2", "q3", "EA")                  # sec 5: category channel (R_cat)
CULT_PREFIX = ("q4", "q5", "q6", "CC")                 # sec 5: cultural channel (R_cult)
N_MODELS, N_FRAMES = 6, 6

# sec 5.1 - thresholds of prereg/v0_21_registry.json "thresholds" (v1.5) + v1.6 Increment 1
N_FLOOR_WORLD = 12
N_FLOOR_C3 = 5
DISTINCT_MIN = 3
MODAL_MAX = 0.625
IL_SEP_MIN = 0.10
RHO_C3 = 0.50
C3_CELLS_MIN = 2
IWACHU_CP_MIN, IWACHU_RCAT_MAX = 5, 2
T1_RCAT_MIN, T1_RCULT_MAX = 5, 2
T2_RCAT_MAX, T2_RCULT_MIN = 2, 5
T2_EMERGED_MIN = 3
CELL_B_N_MIN = 5
# sec 5.2 - v1.4 composite (recall-leaning, the primary Presence score) and v0.23 quartile regime rule
W_R, W_C = 0.3, 0.7
RECOG_PASS = 5                                         # C_P >= 5 of 6 -> R(b) = 1 (v1.4 sec 5.2)
REGIMES = ("Dominant", "Established", "Emerging", "Absent")

# sec 6 - hypotheses
H1_CONF, H1_FALS, H1_NULL_PI = 0.80, 0.60, 0.60
H2_CONF, H2_FALS = 0.80, 0.60
H4_F4_CONF, H4_F4_FALS = 0.90, 0.75
N_MIN_COMPARISONS = 15
ALPHA_PRIMARY = 0.025                                  # sec 6.5: Bonferroni over H1, H2
ALPHA_SECONDARY = 0.05                                 # sec 6.5: H3 (the only secondary with a p-value)
N_DRAWS_RANDOM = 500                                   # sec 4 R9
RANDOM_SHARE = 0.75                                    # sec 4 R9
N_PERM_H2 = 1_000                                      # sec 6.2
N_MC_H3 = 2_000                                        # sec 6.3
SEEDS = {"R9": 630009, "H2": 630002, "H3": 630003, "POWER": 630090}

DENON = ("v0.19", "Denon")                             # Declarations, COI

# where the parity references live (sec 7)
REF_THREE_WAVE = "osf/v41/v41_three_wave_table.csv"
REF_T1_VERDICTS = {"v0.20": "osf/v20/v20_verdicts.json", "v0.21": "osf/v21/v21_verdicts.json",
                   "v0.22": "osf/v22/v22_verdicts.json"}
REF_V23 = "osf/v23/v23_verdicts.json"
REF_V19_OUTPUT = "osf/v19/scoring_output_v0_19.txt"
REGISTRY_FILES = {"v0.19": "osf/v19/panel_registry_v0_19.csv", "v0.20": "prereg/v0_20_registry.json",
                  "v0.21": "prereg/v0_21_registry.json", "v0.22": "prereg/v0_22_automotive_content.py",
                  "v0.23": "osf/methodology/v1_10/registries/v0_23_registry_v1_10.json"}


class Halt(RuntimeError):
    pass


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def git_blob_bytes(b: bytes) -> str:
    return hashlib.sha1(b"blob %d\0" % len(b) + b).hexdigest()


def _clean(o):
    if isinstance(o, dict):
        return {str(k): _clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple, set)):
        return [_clean(v) for v in (sorted(o) if isinstance(o, set) else o)]
    if isinstance(o, float):
        return None if (math.isnan(o) or math.isinf(o)) else round(o, 10)
    if hasattr(o, "item"):
        return _clean(o.item())
    return o


def _write_json(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(_clean(obj), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


# ===========================================================================
# SEC 5 - THE RECOGNITION x RECALL VERDICT FUNCTIONS (pure; a panel is {brand: unit})
#   unit = {"cell": str, "cp": int 0..6, "r_cat": int 0..18, "r_cult": int 0..18, "cascade": int|None}
# ===========================================================================
def spearman(x, y):
    """Spearman rho with average ranks; None when undefined (n < 2 or a constant vector) - sec 6.4."""
    n = len(x)
    if n < 2 or len(set(x)) < 2 or len(set(y)) < 2:
        return None

    def ranks(v):
        order = sorted(range(n), key=lambda i: v[i])
        r = [0.0] * n
        i = 0
        while i < n:
            j = i
            while j + 1 < n and v[order[j + 1]] == v[order[i]]:
                j += 1
            avg = (i + j) / 2 + 1
            for k in range(i, j + 1):
                r[order[k]] = avg
            i = j + 1
        return r
    rx, ry = ranks(x), ranks(y)
    mx, my = sum(rx) / n, sum(ry) / n
    sxy = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    sxx = sum((a - mx) ** 2 for a in rx)
    syy = sum((b - my) ** 2 for b in ry)
    return sxy / math.sqrt(sxx * syy)


def cells_of(panel: dict) -> dict:
    out = {}
    for b, u in panel.items():
        out.setdefault(u["cell"], []).append(b)
    return {c: sorted(v) for c, v in sorted(out.items())}


def cell_c2(panel: dict, brands) -> dict:
    cps = [panel[b]["cp"] for b in brands]
    cnt = Counter(cps)
    distinct = len(cnt)
    modal_share = (cnt.most_common(1)[0][1] / len(cps)) if cps else 0.0
    return {"n": len(cps), "distinct": distinct, "modal_share": round(modal_share, 4),
            "passes": distinct >= DISTINCT_MIN and modal_share <= MODAL_MAX}


def top2_share(panel, brands) -> float:
    r = sorted((panel[b]["r_cat"] for b in brands), reverse=True)
    tot = sum(r)
    return (sum(r[:2]) / tot) if tot > 0 else 0.0


def f1_regime4(panel: dict, il_gradient: bool, prescreen: bool = True) -> dict:
    """F1 = H_Regime4 routing (sec 5.1): v1.6 Increment 1 pre-screen, then v1.5 C1 -> C2 -> IL guard -> C3.
    UNDEFINED (None) when the panel has fewer than 2 non-empty cells; INADEQUATE (C1 fails) is not a
    verdict for comparison (sec 6.4)."""
    cells = cells_of(panel)
    if len(cells) < 2:
        return {"verdict": None, "why": "fewer than 2 cells"}
    c2 = {c: cell_c2(panel, bs) for c, bs in cells.items()}
    if prescreen and all(v["distinct"] == 1 for v in c2.values()):
        return {"verdict": "REGIME-4-UNAVAILABLE-AT-RECOGNITION", "resolved_at": "pre-screen", "c2": c2}
    n = len(panel)
    if n < N_FLOOR_WORLD:
        return {"verdict": "INADEQUATE", "resolved_at": "C1", "n": n, "c2": c2}
    failing = [c for c, v in c2.items() if not v["passes"]]
    if len(failing) >= 2:
        return {"verdict": "FALSIFIED", "resolved_at": "C2", "failing": failing, "c2": c2}
    if len(failing) == 1:
        return {"verdict": "PARTIAL", "resolved_at": "C2", "failing": failing, "c2": c2}
    if il_gradient and "B" in cells and "C" in cells:
        sep = top2_share(panel, cells["B"]) - top2_share(panel, cells["C"])
        if sep < IL_SEP_MIN:
            return {"verdict": "PARTIAL", "resolved_at": "IL guard", "separation": sep, "c2": c2}
    rho = {}
    clearing = []
    for c, bs in cells.items():
        r = spearman([panel[b]["cp"] for b in bs], [panel[b]["r_cat"] for b in bs])
        rho[c] = r
        if len(bs) >= N_FLOOR_C3 and r is not None and r >= RHO_C3:
            clearing.append(c)
    v = "CONFIRMED" if len(clearing) >= C3_CELLS_MIN else "PARTIAL"
    return {"verdict": v, "resolved_at": "C3", "rho": rho, "clearing": clearing, "c2": c2}


def is_iwachu(u):
    return u["cp"] >= IWACHU_CP_MIN and u["r_cat"] <= IWACHU_RCAT_MAX


def is_type1(u):
    return u["r_cat"] >= T1_RCAT_MIN and u["r_cult"] <= T1_RCULT_MAX


def is_type2(u):
    return u["r_cat"] <= T2_RCAT_MAX and u["r_cult"] >= T2_RCULT_MIN


def f2_type2(panel: dict) -> dict:
    """F2 = H_Type2_emergence (sec 5.1): Type 2 count in Cell B. Cell B absent or n_B < 5 -> UNDETERMINED,
    which is not a verdict for comparison (sec 6.4)."""
    bs = [b for b, u in panel.items() if u["cell"] == "B"]
    if len(bs) < CELL_B_N_MIN:
        return {"verdict": "UNDETERMINED", "n_B": len(bs)}
    k = sum(1 for b in bs if is_type2(panel[b]))
    v = "EMERGED" if k >= T2_EMERGED_MIN else ("PARTIAL" if k >= 1 else "FALSIFIED")
    return {"verdict": v, "n_B": len(bs), "type2_in_B": k}


def f3_dissociation(panel: dict) -> dict:
    """F3 = H_Dissociation_substrate_generalization (sec 5.1): number of cells holding an Iwachu case."""
    cells = cells_of(panel)
    if len(cells) < 2:
        return {"verdict": None, "why": "fewer than 2 cells"}
    with_iw = sorted({panel[b]["cell"] for b in panel if is_iwachu(panel[b])})
    v = "GENERALIZED" if len(with_iw) >= 2 else ("PARTIAL" if len(with_iw) == 1 else "NARROWED")
    return {"verdict": v, "iwachu_cells": with_iw}


def composite(u):
    """v1.4 recall-leaning composite A = 0.3 R + 0.7 C; R = 1[C_P >= 5]; C = (R_cat + R_cult) / 36.
    None (descoped) when R = 0 (v1.4 sec 7: C_P FAIL brands are descoped)."""
    if u["cp"] < RECOG_PASS:
        return None
    return W_R * 1.0 + W_C * (u["r_cat"] + u["r_cult"]) / (N_MODELS * N_FRAMES)


def percentile(sorted_vals, q):
    """numpy.percentile, linear interpolation (the rule of scripts/score_v0_23.py)."""
    n = len(sorted_vals)
    pos = (n - 1) * q / 100.0
    lo = math.floor(pos)
    hi = min(lo + 1, n - 1)
    return sorted_vals[lo] + (sorted_vals[hi] - sorted_vals[lo]) * (pos - lo)


def f4_regimes(panel: dict) -> dict:
    """F4 = per-brand quartile regime within the panel (sec 5.2; scripts/score_v0_23.py lines 332-356):
    quartiles of the composite over the non-descoped brands; descoped -> Absent; fewer than 4 scored brands
    -> every regime UNDEFINED (None)."""
    comp = {b: composite(u) for b, u in panel.items()}
    active = sorted(v for v in comp.values() if v is not None)
    if len(active) < 4:
        return {b: None for b in panel}
    q25, q50, q75 = (percentile(active, q) for q in (25, 50, 75))
    out = {}
    for b, c in comp.items():
        if c is None:
            out[b] = "Absent"
        elif c >= q75:
            out[b] = "Dominant"
        elif c >= q50:
            out[b] = "Established"
        elif c >= q25:
            out[b] = "Emerging"
        else:
            out[b] = "Absent"
    return out


def brand_level(panel: dict) -> dict:
    """Panel-independent brand-level quantities (MC1): C_P, R_cat, R_cult and class memberships."""
    return {b: (u["cp"], u["r_cat"], u["r_cult"], is_iwachu(u), is_type1(u), is_type2(u))
            for b, u in panel.items()}


def substrate_verdicts(sub: str, panel: dict) -> dict:
    """Every substrate-level family defined for this substrate (sec 5.1)."""
    out = {}
    if sub in CELLED:
        out["F1"] = f1_regime4(panel, il_gradient=sub in IL_GRADIENT)["verdict"]
        out["F3"] = f3_dissociation(panel)["verdict"]
    if sub in IL_GRADIENT:
        out["F2"] = f2_type2(panel)["verdict"]
    return out


UNCOMPARABLE = {None, "INADEQUATE", "UNDETERMINED"}    # sec 6.4


# ===========================================================================
# SEC 4 - PANEL-BUILD RULES
# ===========================================================================
def _cell_letter(label: str) -> str:
    """'A_Heritage' / 'Cell_B_Disruptor' / 'C' -> 'A' / 'B' / 'C'."""
    s = label[5:] if label.startswith("Cell_") else label
    return s[:1]


def load_registry_meta(root: Path = ROOT) -> dict:
    """{substrate: {brand_key: {"cell", "cascade", "flags"}}} from the locked registries ONLY (no answer).
    Brand keys are the keys of the certified loader (S-ids for v0.23)."""
    import ast
    import csv
    meta = {}
    m = {}
    with open(root / REGISTRY_FILES["v0.19"], encoding="utf-8") as fh:
        rows19 = list(csv.DictReader(fh))
    for r in rows19:
        fl = set()
        if r["cross_cultural_flag"].strip() == "True":
            fl.add("cross_cultural")
        if r["borderline_flag"].strip() == "True":
            fl.add("borderline")
        if ("v0.19", r["brand"]) == DENON:
            fl.add("coi_flagged")
        m[r["brand"]] = {"cell": _cell_letter(r["cell"]), "cascade": int(r["cascade_order"]), "flags": fl}
    meta["v0.19"] = m
    for sub in ("v0.20", "v0.21"):
        d = json.loads((root / REGISTRY_FILES[sub]).read_text(encoding="utf-8"))
        m = {}
        for cid, cell in d["cells"].items():
            for b in cell["brands"]:
                fl = {"borderline"} if b.get("borderline_classification") else set()
                m[b["name"]] = {"cell": _cell_letter(cid), "cascade": int(b["cascade_order"]), "flags": fl}
        meta[sub] = m
    src = (root / REGISTRY_FILES["v0.22"]).read_text(encoding="utf-8")
    tree = ast.parse(src)
    reg = None
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(getattr(t, "id", None) == "REGISTRY" for t in node.targets):
            reg = ast.literal_eval(node.value)
    if reg is None:
        raise Halt("v0.22 REGISTRY not found")
    m = {}
    for cid, names in reg.items():
        for i, n in enumerate(names, 1):
            fl = {"defunct"} if cid == "Cell_D_Defunct" else set()
            m[n] = {"cell": _cell_letter(cid), "cascade": i, "flags": fl}
    meta["v0.22"] = m
    d = json.loads((root / REGISTRY_FILES["v0.23"]).read_text(encoding="utf-8"))
    meta["v0.23"] = {b["id"]: {"cell": "-", "cascade": None,
                               "flags": {"conglomerate"} if int(b["conglomerate"]) == 1 else set(),
                               "name": b["brand"]} for b in d["brands"]}
    return meta


STRUCTURAL_RULES = ["R1_DROP_DEFUNCT", "R2_DROP_COI_FLAGGED", "R3_DROP_CROSS_CULTURAL",
                    "R4_DROP_BORDERLINE", "R5_CASCADE_TOP5", "R6_LEAVE_ONE_CELL_OUT"]
DATA_RULES = ["R7_RECOGNITION_ANCHORED", "R8_RECALL_SOURCED_XWAVE"]
DETERMINISTIC_RULES = STRUCTURAL_RULES + DATA_RULES
DISCLOSED_RULES = ["R1_DROP_DEFUNCT", "R2_DROP_COI_FLAGGED", "R3_DROP_CROSS_CULTURAL"]   # H4
F4_ONLY_RULES = ["R11_INDEPENDENT_ONLY"]                # descriptive (sec 4)
XWAVE_SOURCE = {"t1": "t2", "t2": "t1", "t3": "t2"}     # sec 4 R8


def structural_variants(sub: str, meta_sub: dict) -> list:
    """[(rule, variant_id, kept brand list)] for the structural rules; only variants that change the panel."""
    full = sorted(meta_sub)
    out = []

    def add(rule, vid, kept):
        kept = sorted(kept)
        if kept != full and kept and all(kept != o[2] for o in out):   # a panel identical to an earlier
            out.append((rule, vid, kept))                                # rule's is not a new comparison

    def drop_flag(rule, flag):
        add(rule, rule, [b for b in full if flag not in meta_sub[b]["flags"]])

    drop_flag("R1_DROP_DEFUNCT", "defunct")
    drop_flag("R2_DROP_COI_FLAGGED", "coi_flagged")
    drop_flag("R3_DROP_CROSS_CULTURAL", "cross_cultural")
    drop_flag("R4_DROP_BORDERLINE", "borderline")
    if sub in CELLED:
        add("R5_CASCADE_TOP5", "R5_CASCADE_TOP5", [b for b in full if meta_sub[b]["cascade"] <= 5])
        for c in sorted({meta_sub[b]["cell"] for b in full}):
            add("R6_LEAVE_ONE_CELL_OUT", f"R6_LEAVE_OUT_{c}", [b for b in full if meta_sub[b]["cell"] != c])
    if sub == "v0.23":
        add("R11_INDEPENDENT_ONLY", "R11_INDEPENDENT_ONLY",
            [b for b in full if "conglomerate" not in meta_sub[b]["flags"]])
    return out


def data_variants(sub: str, panel: dict, source_panel: dict | None) -> list:
    """R7 and R8 (sec 4): defined from the archive, applied at scoring time."""
    full = sorted(panel)
    out = []
    kept = [b for b in full if panel[b]["cp"] >= RECOG_PASS]
    if kept != full and kept:
        out.append(("R7_RECOGNITION_ANCHORED", "R7_RECOGNITION_ANCHORED", kept))
    if source_panel is not None:
        kept = [b for b in full if (source_panel[b]["r_cat"] + source_panel[b]["r_cult"]) >= 1]
        if kept != full and kept:
            out.append(("R8_RECALL_SOURCED_XWAVE", "R8_RECALL_SOURCED_XWAVE", kept))
    return out


def subpanel(panel: dict, kept) -> dict:
    return {b: panel[b] for b in kept}


def build_rules_doc(root: Path = ROOT) -> dict:
    """registries/panel_rules_v0_63.json: structural rule applications and the structural comparison count
    (an upper bound for H1 before data-dependent rules and uncomparable verdicts). Reads registries only."""
    meta = load_registry_meta(root)
    subs = {}
    n_struct = 0
    for sub in OMNI:
        fams = [f for f, ok in (("F1", sub in CELLED), ("F2", sub in IL_GRADIENT), ("F3", sub in CELLED)) if ok]
        vs = []
        for rule, vid, kept in structural_variants(sub, meta[sub]):
            dropped = sorted(set(meta[sub]) - set(kept))
            cells_left = sorted({meta[sub][b]["cell"] for b in kept})
            fam_here = [] if rule in F4_ONLY_RULES else [
                f for f in fams if not ((f in ("F1", "F3") and len(cells_left) < 2) or (f == "F2" and "B" not in cells_left))]
            n_struct += len(fam_here) * len(WAVES)
            vs.append({"rule": rule, "variant": vid, "n_kept": len(kept), "dropped": dropped,
                       "cells_left": cells_left, "families_comparable_structurally": fam_here})
        subs[sub] = {"registry": REGISTRY_FILES[sub], "n_brands": len(meta[sub]),
                     "cells": dict(Counter(v["cell"] for v in meta[sub].values())),
                     "flags": {b: sorted(v["flags"]) for b, v in sorted(meta[sub].items()) if v["flags"]},
                     "families": fams, "variants": vs}
    return {"phase": PHASE_ID, "created_utc": _now(), "reads": "registries only (no answer file)",
            "registry_sha256": {s: sha256_bytes((root / p).read_bytes()) for s, p in REGISTRY_FILES.items()},
            "rules": {"structural": STRUCTURAL_RULES, "data_dependent": DATA_RULES,
                      "random": ["R9_RANDOM_75_STRATIFIED", "R10_RANDOM_SIZE_MATCHED (H3 null)"],
                      "f4_descriptive_only": F4_ONLY_RULES, "disclosed_handling_H4": DISCLOSED_RULES},
            "structural_comparisons_upper_bound_H1": n_struct, "substrates": subs}


# ===========================================================================
# SEC 6 - STATISTICS
# ===========================================================================
def binom_sf(k: int, n: int, p_num: int = 3, p_den: int = 5) -> float:
    """Exact P(X >= k), X ~ Binomial(n, p_num/p_den) (default 0.60), with integer arithmetic."""
    if n == 0:
        return 1.0
    q_num = p_den - p_num
    tot = sum(math.comb(n, i) * p_num ** i * q_num ** (n - i) for i in range(max(k, 0), n + 1))
    return tot / p_den ** n


def compare(canon: dict, alt: dict) -> list:
    """Per family: {"family", "canon", "alt", "status": match|flip|uncomparable}."""
    rows = []
    for f, cv in canon.items():
        av = alt.get(f)
        if cv in UNCOMPARABLE or av in UNCOMPARABLE:
            st = "uncomparable"
        else:
            st = "match" if cv == av else "flip"
        rows.append({"family": f, "canon": cv, "alt": av, "status": st})
    return rows


def f4_agreement(canon_reg: dict, alt_reg: dict) -> tuple[int, int]:
    """(agreeing, defined) over retained brands with both regimes defined."""
    a = d = 0
    for b, r in alt_reg.items():
        c = canon_reg.get(b)
        if r is None or c is None:
            continue
        d += 1
        a += int(r == c)
    return a, d


def verdict_h1(matched: int, defined: int) -> dict:
    if defined < N_MIN_COMPARISONS:
        return {"verdict": "UNDETERMINED", "A": (matched / defined) if defined else None, "n": defined,
                "p_binom": None}
    A = matched / defined
    p = binom_sf(matched, defined)
    if A < H1_FALS:
        v = "FALSIFIED"
    elif A >= H1_CONF and p < ALPHA_PRIMARY:
        v = "CONFIRMED"
    else:
        v = "MARGINAL"
    return {"verdict": v, "A": A, "n": defined, "matched": matched, "p_binom": p}


def verdict_h2(S, n_units: int, p_perm) -> dict:
    if S is None or n_units < 10:
        return {"verdict": "UNDETERMINED", "S": S, "n_substrate_waves": n_units, "p_perm": p_perm}
    if S < H2_FALS:
        v = "FALSIFIED"
    elif S >= H2_CONF and p_perm is not None and p_perm < ALPHA_PRIMARY:
        v = "CONFIRMED"
    else:
        v = "MARGINAL"
    return {"verdict": v, "S": S, "n_substrate_waves": n_units, "p_perm": p_perm}


def verdict_h3(f_obs, f_null_mean, p, n: int) -> dict:
    if n < N_MIN_COMPARISONS or f_obs is None or f_null_mean is None:
        return {"verdict": "UNDETERMINED", "f_obs": f_obs, "f_null_mean": f_null_mean, "p_mc": p, "n": n}
    if f_obs <= f_null_mean:
        v = "FALSIFIED"
    elif p < ALPHA_SECONDARY:
        v = "CONFIRMED"
    else:
        v = "MARGINAL"
    return {"verdict": v, "f_obs": f_obs, "f_null_mean": f_null_mean, "p_mc": p, "n": n}


def verdict_h4(flips: int, defined: int, f4_agree: int, f4_def: int) -> dict:
    if defined == 0 and f4_def == 0:
        return {"verdict": "UNDETERMINED", "flips": flips, "defined": defined, "f4": None}
    f4 = (f4_agree / f4_def) if f4_def else None
    if flips >= 2 or (f4 is not None and f4 < H4_F4_FALS):
        v = "FALSIFIED"
    elif flips == 0 and (f4 is None or f4 >= H4_F4_CONF):
        v = "CONFIRMED"
    else:
        v = "MARGINAL"
    return {"verdict": v, "flips": flips, "defined": defined, "f4_agreement": f4, "f4_defined": f4_def}


def stratified_draw(rng, panel: dict, share: float = RANDOM_SHARE) -> list:
    """R9: per cell, ceil(share * n_cell) brands without replacement (one stratum when no cells)."""
    kept = []
    for c, bs in cells_of(panel).items():
        k = math.ceil(share * len(bs))
        idx = rng.choice(len(bs), size=k, replace=False)
        kept += [bs[i] for i in sorted(idx)]
    return sorted(kept)


# ===========================================================================
# SEC 6 - SCORING (pure: archive = {wave: {substrate: panel}}, meta from the registries)
# ===========================================================================
def check_archive(archive: dict, meta: dict, expected=None) -> list:
    """MC4: every substrate-wave holds exactly the registry's brands (and the expected count)."""
    bad = []
    for w in WAVES:
        for s in OMNI:
            got = set(archive.get(w, {}).get(s, {}))
            if got != set(meta[s]):
                bad.append(f"{w} {s}: brand set differs from the registry "
                           f"(missing {sorted(set(meta[s]) - got)[:5]}, extra {sorted(got - set(meta[s]))[:5]})")
            if expected and len(got) != expected[s]:
                bad.append(f"{w} {s}: {len(got)} brands, expected {expected[s]}")
            for b in got & set(meta[s]):
                if archive[w][s][b]["cell"] != meta[s][b]["cell"]:
                    bad.append(f"{w} {s} {b}: cell {archive[w][s][b]['cell']} != registry {meta[s][b]['cell']}")
    return bad


def drop_brands(archive: dict, meta: dict, sub: str, brands) -> tuple[dict, dict]:
    """Sensitivity S1 (COI): the same scoring with brands removed from every wave of one substrate."""
    a2 = {w: {s: ({b: u for b, u in p.items() if not (s == sub and b in brands)}) for s, p in sw.items()}
          for w, sw in archive.items()}
    m2 = {s: ({b: v for b, v in ms.items() if not (s == sub and b in brands)}) for s, ms in meta.items()}
    return a2, m2


def score_core(archive: dict, meta: dict, n_draws: int = N_DRAWS_RANDOM, n_perm: int = N_PERM_H2,
               n_mc: int = N_MC_H3, do_h2: bool = True, do_h3: bool = True, log=print) -> dict:
    import numpy as np
    bad = check_archive(archive, meta)
    if bad:
        raise Halt("MC4 failed: " + "; ".join(bad[:5]))
    canon, canon_reg = {}, {}
    for w in WAVES:
        for s in OMNI:
            canon[w, s] = substrate_verdicts(s, archive[w][s])
            canon_reg[w, s] = f4_regimes(archive[w][s])

    comparisons, f4_rows, groups, mc1_fail = [], [], [], []
    for w in WAVES:
        for s in OMNI:
            panel = archive[w][s]
            full_bl = brand_level(panel)
            variants = list(structural_variants(s, meta[s]))
            for v in data_variants(s, panel, archive[XWAVE_SOURCE[w]][s]):
                if all(v[2] != o[2] for o in variants):             # sec 4: duplicates count once
                    variants.append(v)
            for rule, vid, kept in variants:
                alt = subpanel(panel, kept)
                if brand_level(alt) != {b: full_bl[b] for b in kept}:          # MC1
                    mc1_fail.append(f"{w} {s} {vid}")
                a, d = f4_agreement(canon_reg[w, s], f4_regimes(alt))
                f4_rows.append({"wave": w, "substrate": s, "rule": rule, "variant": vid, "n_kept": len(kept),
                                "f4_agree": a, "f4_defined": d})
                if rule in F4_ONLY_RULES:
                    continue
                rows = compare(canon[w, s], substrate_verdicts(s, alt))
                for r in rows:
                    comparisons.append({"wave": w, "substrate": s, "rule": rule, "variant": vid,
                                        "n_kept": len(kept), **r})
                comp_fams = [r["family"] for r in rows if r["status"] != "uncomparable"]
                if comp_fams:
                    groups.append((w, s, len(kept), comp_fams))
    if mc1_fail:
        raise Halt("MC1 (brand-level invariance) failed: " + "; ".join(mc1_fail[:5]))

    # H1 - deterministic rules, families F1-F3
    det = [c for c in comparisons if c["rule"] in DETERMINISTIC_RULES]
    defined = [c for c in det if c["status"] != "uncomparable"]
    matched = sum(c["status"] == "match" for c in defined)
    h1 = verdict_h1(matched, len(defined))
    h1["uncomparable"] = len(det) - len(defined)

    def table(key):
        t = {}
        for c in det:
            k = c[key]
            e = t.setdefault(k, {"match": 0, "flip": 0, "uncomparable": 0})
            e[c["status"]] += 1
        for e in t.values():
            n = e["match"] + e["flip"]
            e["A"] = (e["match"] / n) if n else None
        return t

    loso = {}
    for s in OMNI:
        rest = [c for c in defined if c["substrate"] != s]
        loso[s] = (sum(c["status"] == "match" for c in rest) / len(rest)) if rest else None

    # H4 - disclosed-handling rules
    h4 = {}
    for rule in DISCLOSED_RULES:
        cs = [c for c in comparisons if c["rule"] == rule]
        dfd = [c for c in cs if c["status"] != "uncomparable"]
        fr = [r for r in f4_rows if r["rule"] == rule]
        h4[rule] = verdict_h4(sum(c["status"] == "flip" for c in dfd), len(dfd),
                              sum(r["f4_agree"] for r in fr), sum(r["f4_defined"] for r in fr))
    cs = [c for c in comparisons if c["rule"] in DISCLOSED_RULES]
    dfd = [c for c in cs if c["status"] != "uncomparable"]
    fr = [r for r in f4_rows if r["rule"] in DISCLOSED_RULES]
    h4_all = verdict_h4(sum(c["status"] == "flip" for c in dfd), len(dfd),
                        sum(r["f4_agree"] for r in fr), sum(r["f4_defined"] for r in fr))

    out = {"H1_SubstrateVerdictStability": h1, "H4_DisclosedHandlingNeutral": {**h4_all, "per_rule": h4},
           "descriptives": {"H1_by_rule": table("rule"), "H1_by_family": table("family"),
                            "H1_by_substrate": table("substrate"), "H1_by_wave": table("wave"),
                            "H1_leave_one_substrate_out_A": loso,
                            "F4_deterministic": f4_rows,
                            "canonical_verdicts": {f"{w} {s}": v for (w, s), v in canon.items()}},
           "comparisons": comparisons, "manipulation_checks": {"MC1_brand_level_invariance": "pass",
                                                               "MC4_brand_sets": "pass"}}

    # H2 - per-brand regime stability under R9 (stratified random 75%)
    if do_h2:
        rng = np.random.default_rng(SEEDS["R9"])
        rngp = np.random.default_rng(SEEDS["H2"])
        code = {r: i for i, r in enumerate(REGIMES)}
        s_obs, s_null, per_sw = [], [], {}
        for w in WAVES:
            for s in OMNI:
                panel = archive[w][s]
                cr = canon_reg[w, s]
                if all(v is None for v in cr.values()):
                    per_sw[f"{w} {s}"] = None
                    for _ in range(n_draws):                    # keep the stream aligned across substrates
                        stratified_draw(rng, panel)
                    continue
                agrees, null_acc, used = [], np.zeros(n_perm), 0
                for _ in range(n_draws):
                    kept = stratified_draw(rng, panel)
                    ar = f4_regimes(subpanel(panel, kept))
                    pairs = [(code[cr[b]], code[ar[b]]) for b in kept if cr.get(b) is not None and ar[b] is not None]
                    if not pairs:
                        continue
                    c = np.array([p[0] for p in pairs])
                    a = np.array([p[1] for p in pairs])
                    agrees.append(float((c == a).mean()))
                    idx = rngp.permuted(np.tile(np.arange(len(a)), (n_perm, 1)), axis=1)
                    null_acc += (a[idx] == c).mean(axis=1)
                    used += 1
                if used == 0:
                    per_sw[f"{w} {s}"] = None
                    continue
                per_sw[f"{w} {s}"] = float(np.mean(agrees))
                s_obs.append(float(np.mean(agrees)))
                s_null.append(null_acc / used)
        S = float(np.mean(s_obs)) if s_obs else None
        p = None
        if s_obs:
            null_S = np.mean(np.vstack(s_null), axis=0)
            p = float((1 + np.sum(null_S >= S - 1e-12)) / (1 + n_perm))
            out["descriptives"]["H2_null_mean"] = float(null_S.mean())
        out["H2_RegimeAssignmentStability"] = verdict_h2(S, len(s_obs), p)
        out["descriptives"]["H2_per_substrate_wave"] = per_sw

    # H3 - purposive rules vs total-size-matched random subsets
    if do_h3:
        f_obs = (1 - h1["A"]) if h1.get("A") is not None else None
        rng = np.random.default_rng(SEEDS["H3"])
        reps = []
        for _ in range(n_mc):
            fl = cp = 0
            for (w, s, k, fams) in groups:
                panel = archive[w][s]
                full = sorted(panel)
                kept = sorted(full[i] for i in rng.choice(len(full), size=k, replace=False))
                av = substrate_verdicts(s, subpanel(panel, kept))
                for f in fams:
                    if av.get(f) in UNCOMPARABLE:
                        continue
                    cp += 1
                    fl += int(av[f] != canon[w, s][f])
            reps.append(fl / cp if cp else float("nan"))
        reps = np.array(reps)
        ok = reps[~np.isnan(reps)]
        f_null = float(ok.mean()) if ok.size else None
        p = float((1 + np.sum(ok >= f_obs - 1e-12)) / (1 + ok.size)) if (ok.size and f_obs is not None) else None
        out["H3_PurposiveVsRandom"] = verdict_h3(f_obs, f_null, p, len(defined))
    return out


def score_all(archive: dict, meta: dict, log=print, **kw) -> dict:
    """Primary scoring + sensitivity S1 (COI: v0.19 without Denon in every panel; H1, H2, H4 only)."""
    res = score_core(archive, meta, log=log, **kw)
    a2, m2 = drop_brands(archive, meta, DENON[0], {DENON[1]})
    kw2 = dict(kw, do_h3=False)
    s1 = score_core(a2, m2, log=log, **kw2)
    res["sensitivity_S1_without_Denon"] = {k: s1[k] for k in ("H1_SubstrateVerdictStability",
                                                               "H2_RegimeAssignmentStability",
                                                               "H4_DisclosedHandlingNeutral") if k in s1}
    v = {k: res[k]["verdict"] for k in ("H1_SubstrateVerdictStability", "H2_RegimeAssignmentStability",
                                         "H3_PurposiveVsRandom", "H4_DisclosedHandlingNeutral") if k in res}
    res["verdicts"] = v
    return res


# ===========================================================================
# SEC 3 - ARCHIVE LOADER (certified lineage: osf/v41/scripts/score_v41.py load_wave)
# ===========================================================================
def _ensure_home_shim():
    """The v0.41 shim: make ~/aias resolve to ROOT for the certified modules, or re-execute."""
    try:
        same = (Path.home() / "aias").resolve() == ROOT
    except OSError:
        same = False
    os.environ["AIAS_ROOT"] = str(ROOT)
    if same:
        return
    if os.environ.get("_V63_HOME_SHIM"):
        sys.exit(f"[v0.63] ROOT shim failed: ~/aias -> {(Path.home() / 'aias').resolve()} != {ROOT}")
    import site
    shim = Path(tempfile.mkdtemp(prefix="v63_home_"))
    (shim / "aias").symlink_to(ROOT)
    env = dict(os.environ, HOME=str(shim), _V63_HOME_SHIM="1", AIAS_ROOT=str(ROOT))
    env.setdefault("PYTHONUSERBASE", site.getuserbase())
    os.execve(sys.executable, [sys.executable, os.path.abspath(sys.argv[0])] + sys.argv[1:], env)


def _s41():
    p = str(ROOT / "osf/v41/scripts")
    if p not in sys.path:
        sys.path.insert(0, p)
    import score_v41 as S41
    if Path(S41.ROOT).resolve() != ROOT:
        raise Halt(f"certified loader reads {S41.ROOT}, not {ROOT}")
    return S41


ARCHIVE_DATA_FILES = [f"osf/{d}/{f}" for d in ("v20", "v21", "v22") for f in ("phase_a_results.csv", "phase_b_results.csv")] \
    + ["osf/v19/phase_a_results.csv", "osf/v19/phase_b_results.csv",
       "osf/v23/data/v23_phase_a_scored.json", "osf/v23/data/v23_phase_b_scored.json"] \
    + [f"osf/{base}/{d}/{f}" for base in ("v34/data", "v41/data") for d in ("v19", "v20", "v21", "v22")
       for f in ("phase_a_results.csv", "phase_b_results.csv")] \
    + [f"osf/{base}/v23/{f}" for base in ("v34/data", "v41/data") for f in ("v23_phase_a_scored.json",
                                                                            "v23_phase_b_scored.json")]
LOADER_CODE_FILES = ["osf/v41/scripts/score_v41.py", "scripts/score_v0_31.py", "scripts/score_v33.py",
                     "scripts/score_v20.py", "scripts/score_v21.py", "scripts/score_v22.py",
                     "prereg/v0_31_cpc_baseline_content.py", "prereg/v0_33_provider_asymmetry_content.py"]


def channel_counts(frames_by_model: dict) -> tuple[int, int]:
    r_cat = sum(1 for fs in frames_by_model.values() for f in fs if str(f).startswith(CAT_PREFIX))
    r_cult = sum(1 for fs in frames_by_model.values() for f in fs if str(f).startswith(CULT_PREFIX))
    return r_cat, r_cult


def load_archive(meta: dict) -> dict:
    """{wave: {substrate: {brand: unit}}} with unit = cell, cp, r_cat, r_cult, cascade, k (per-model recall)."""
    S41 = _s41()
    lays = {"t1": S41.LAYOUT["t1"], "t2": S41.LAYOUT["t2"], "t3": S41._layout(S41.DATA3, S41.DATA3 / "v23")}
    arch = {}
    for w in WAVES:
        wave = S41.load_wave(lays[w])
        arch[w] = {}
        for s in OMNI:
            x = wave[s]
            panel = {}
            for b, vec in x["counts"].items():
                k = [int(v) for v in vec]
                r_cat, r_cult = channel_counts(x["frames"].get(b, {}))
                if r_cat + r_cult != sum(k):
                    raise Halt(f"{w} {s} {b}: channel split {r_cat}+{r_cult} != recall {sum(k)}")
                if b not in meta[s]:
                    raise Halt(f"{w} {s}: brand {b!r} is not in the registry")
                cl = x["cells"].get(b) or ""
                if cl and _cell_letter(cl) != meta[s][b]["cell"]:
                    raise Halt(f"{w} {s} {b}: loader cell {cl} != registry cell {meta[s][b]['cell']}")
                rg = x["recog"].get(b, [0] * N_MODELS)
                panel[b] = {"cell": meta[s][b]["cell"], "cp": int(sum(int(v) for v in rg)), "r_cat": r_cat,
                            "r_cult": r_cult, "cascade": meta[s][b]["cascade"], "k": k}
            arch[w][s] = panel
    bad = check_archive(arch, meta, EXPECTED_BRANDS)
    if bad:
        raise Halt("MC4 failed: " + "; ".join(bad[:5]))
    return arch


# ===========================================================================
# SEC 7 - PRE-LOCK PARITY (published values only)
# ===========================================================================
V16_TABLE = {   # papers/v1_6/v1_6_ssrn_paper_draft.md, Increment 1 table (rows v0.20, v0.21)
    "v0.20": {"distinct": [2, 3, 1], "modal": [0.750, 0.625, 1.000], "class": "differential",
              "F1": "FALSIFIED"},
    "v0.21": {"distinct": [1, 1, 1], "modal": [1.000, 1.000, 1.000], "class": "uniform-saturation",
              "F1": "REGIME-4-UNAVAILABLE-AT-RECOGNITION"},
}


def _parse_v19_output(text: str) -> dict:
    import re
    iw = {m.group(1): (int(m.group(3)), int(m.group(4))) for m in
          re.finditer(r"^\s+(.+?) \((A_Heritage|B_Boutique)\): C_P=(\d)/6, mentions=(\d+)/18", text, re.M)}
    t1 = {m.group(1): (int(m.group(3)), int(m.group(4))) for m in
          re.finditer(r"^\s+(.+?) \((A_Heritage|B_Boutique)\): category=(\d+)/18, cultural=(\d+)/18", text, re.M)}
    modal = {}
    cur = None
    for line in text.splitlines():
        m = re.match(r"^\s{2}(A_Heritage|B_Boutique):\s*$", line)
        if m:
            cur = _cell_letter(m.group(1))
        m = re.match(r"^\s+C_P modal share = ([0-9.]+)", line)
        if m and cur:
            modal[cur] = float(m.group(1))
    return {"iwachu": iw, "type1": t1, "cp_modal_share": modal}


def run_parity(arch: dict, root: Path = ROOT) -> dict:
    import csv
    checks = {}
    # P1 - v0.41 three-wave table: C_P and per-model recall vector, 336 rows, all three waves
    rows = list(csv.DictReader(open(root / REF_THREE_WAVE, encoding="utf-8")))
    mism = []
    for r in rows:
        u = arch[r["wave"]][r["substrate"]].get(r["brand"])
        if u is None or int(r["C_P"]) != u["cp"] or json.loads(r["k_per_model"]) != u["k"]:
            mism.append(f"{r['wave']} {r['substrate']} {r['brand']}")
    checks["P1_three_wave_table"] = {"reference": REF_THREE_WAVE, "rows": len(rows), "values_checked": 2 * len(rows),
                                     "mismatches": mism, "passed": not mism and len(rows) == 336}
    # P2 - t1 per-brand C_P, R_cat, R_cult of the certified v0.20-v0.22 scorers
    mism, n = [], 0
    for s, rel in REF_T1_VERDICTS.items():
        d = json.loads((root / rel).read_text(encoding="utf-8"))
        for b, a in d["phase_a"]["per_brand"].items():
            pb = d["phase_b"]["per_brand"][b]
            u = arch["t1"][s][b]
            for key, ref in (("cp", a["cp"]), ("r_cat", pb["r_cat"]), ("r_cult", pb["r_cult"])):
                n += 1
                if u[key] != ref:
                    mism.append(f"{s} {b} {key}: {u[key]} != {ref}")
    checks["P2_t1_per_brand_v20_v22"] = {"reference": list(REF_T1_VERDICTS.values()),
                                         "keys": "phase_a.per_brand.<b>.cp, phase_b.per_brand.<b>.r_cat / r_cult",
                                         "values_checked": n, "mismatches": mism, "passed": not mism and n == 216}
    # P3 - t1 v0.23 recall_total / recall_ea / recall_cc
    d = json.loads((root / REF_V23).read_text(encoding="utf-8"))
    mism, n = [], 0
    for e in d["brand_details"]:
        u = arch["t1"]["v0.23"][e["brand_id"]]
        for key, mine in (("recall_total", u["r_cat"] + u["r_cult"]), ("recall_ea", u["r_cat"]),
                          ("recall_cc", u["r_cult"])):
            n += 1
            if int(e[key]) != mine:
                mism.append(f"{e['brand_id']} {key}: {mine} != {e[key]}")
    checks["P3_t1_v23_recall"] = {"reference": REF_V23, "keys": "brand_details[].recall_total / recall_ea / recall_cc",
                                  "values_checked": n, "mismatches": mism, "passed": not mism and n == 72}
    # P4 - t1 v0.19 published case lists and C_P modal shares
    pub = _parse_v19_output((root / REF_V19_OUTPUT).read_text(encoding="utf-8"))
    p19 = arch["t1"]["v0.19"]
    my_iw = {b: (u["cp"], u["r_cat"]) for b, u in p19.items() if is_iwachu(u)}
    my_t1 = {b: (u["r_cat"], u["r_cult"]) for b, u in p19.items() if is_type1(u)}
    my_modal = {c: cell_c2(p19, bs)["modal_share"] for c, bs in cells_of(p19).items()}
    ok4 = my_iw == pub["iwachu"] and my_t1 == pub["type1"] and \
        all(abs(my_modal[c] - v) < 5e-4 for c, v in pub["cp_modal_share"].items()) and len(pub["cp_modal_share"]) == 2
    checks["P4_t1_v19_case_lists"] = {"reference": REF_V19_OUTPUT, "published": pub,
                                      "reproduced": {"iwachu": my_iw, "type1": my_t1, "cp_modal_share": my_modal},
                                      "passed": ok4}
    # P5 - t1 published verdicts (v1.5 routing, no pre-screen) and C2 / IL-guard values, v0.20-v0.22
    mism = []
    names = {"v0.20": "H_Regime4_skincare", "v0.21": "H_Regime4_cosmetics", "v0.22": "H_Regime4_automotive"}
    dis = {"v0.20": "H_Dissociation_substrate_generalization", "v0.21": "H_Dissociation_substrate_generalization",
           "v0.22": "H_Dissoc_substrate_generalization"}
    rep = {}
    for s, rel in REF_T1_VERDICTS.items():
        d = json.loads((root / rel).read_text(encoding="utf-8"))
        p = arch["t1"][s]
        r4 = f1_regime4(p, il_gradient=True, prescreen=False)
        got = {"F1_v1_5": r4["verdict"], "F3": f3_dissociation(p)["verdict"]}
        exp = {"F1_v1_5": d["hypotheses"][names[s]]["verdict"], "F3": d["hypotheses"][dis[s]]["verdict"]}
        if "H_Type2_emergence" in d["hypotheses"]:
            got["F2"] = f2_type2(p)["verdict"]
            exp["F2"] = d["hypotheses"]["H_Type2_emergence"]["verdict"]
        for c, v in d["v1_5_c2_per_cell"].items():
            mine = cell_c2(p, cells_of(p)[c])
            got[f"C2_{c}"] = [mine["distinct"], mine["modal_share"]]
            exp[f"C2_{c}"] = [v["distinct_cp_count"], round(v["modal_cp_share"], 4)]
        cs = cells_of(p)
        got["IL_separation"] = round(top2_share(p, cs["B"]) - top2_share(p, cs["C"]), 4)
        exp["IL_separation"] = d["il_gradient_guard"]["separation"]
        for k in exp:
            if got[k] != exp[k]:
                mism.append(f"{s} {k}: {got[k]} != {exp[k]}")
        rep[s] = {"reproduced": got, "published": exp}
    checks["P5_t1_published_verdicts"] = {"reference": list(REF_T1_VERDICTS.values()), "detail": rep,
                                          "mismatches": mism, "passed": not mism}
    # P6 - v1.6 Increment 1 table (v0.20, v0.21) and the v1.6 Regime 4 reclassification
    mism, rep = [], {}
    for s, e in V16_TABLE.items():
        p = arch["t1"][s]
        c2 = [cell_c2(p, cells_of(p)[c]) for c in ("A", "B", "C")]
        got = {"distinct": [x["distinct"] for x in c2], "modal": [round(x["modal_share"], 3) for x in c2],
               "class": "uniform-saturation" if all(x["distinct"] == 1 for x in c2) else "differential",
               "F1": f1_regime4(p, il_gradient=True)["verdict"]}
        for k in e:
            if got[k] != e[k]:
                mism.append(f"{s} {k}: {got[k]} != {e[k]}")
        rep[s] = got
    checks["P6_v1_6_increment1_table"] = {"reference": "papers/v1_6/v1_6_ssrn_paper_draft.md (Increment 1 table; "
                                                       "retrospective verdict table)", "expected": V16_TABLE,
                                          "reproduced": rep, "mismatches": mism, "passed": not mism}
    # P7 - v0.22's own pre-screen rule (every cell's modal C_P >= 5 -> UNIFORM SATURATION), published value
    d = json.loads((root / REF_T1_VERDICTS["v0.22"]).read_text(encoding="utf-8"))
    p = arch["t1"]["v0.22"]
    modal = {c: Counter(p[b]["cp"] for b in bs).most_common(1)[0][0] for c, bs in cells_of(p).items()}
    got = "UNIFORM SATURATION" if all(v >= 5 for v in modal.values()) else "DIFFERENTIAL"
    exp = d["hypotheses"]["H_SubstrateRecognition_PreScreen"]["verdict"]
    checks["P7_v22_own_prescreen"] = {"reference": REF_T1_VERDICTS["v0.22"], "published": exp, "reproduced": got,
                                      "modal_cp_per_cell": modal, "passed": got == exp}
    passed = all(c["passed"] for c in checks.values())
    return {"phase": PHASE_ID, "created_utc": _now(), "passed": passed,
            "note": "Reproduces published per-brand values (t1-t3) and published t1 verdicts only. No hypothesis "
                    "statistic and no alternative-panel verdict is computed before the lock.",
            "reference_sha256": {rel: sha256_bytes((root / rel).read_bytes()) for rel in
                                 [REF_THREE_WAVE, REF_V23, REF_V19_OUTPUT, *REF_T1_VERDICTS.values()]},
            "checks": checks}


# ===========================================================================
# SEC 9 - POWER / SENSITIVITY ON SYNTHETIC DATA (no archive file is opened)
# ===========================================================================
def _h2_S_synthetic(panels: list, rng, n_draws: int) -> float:
    vals = []
    for panel in panels:
        cr = f4_regimes(panel)
        ag = []
        for _ in range(n_draws):
            kept = stratified_draw(rng, panel)
            ar = f4_regimes(subpanel(panel, kept))
            pr = [(cr[b], ar[b]) for b in kept if cr[b] is not None and ar[b] is not None]
            if pr:
                ag.append(sum(a == b for a, b in pr) / len(pr))
        if ag:
            vals.append(sum(ag) / len(ag))
    return sum(vals) / len(vals) if vals else float("nan")


def synthetic_panel(rng, scenario: str, n_per_cell: int = 8, cells=("A", "B", "C")) -> dict:
    p = {}
    for c in cells:
        for i in range(n_per_cell):
            if scenario == "spread":
                cp, rt = 6, int(rng.integers(0, 37))
            elif scenario == "ties":
                cp, rt = 6, (0 if rng.random() < 0.6 else int(rng.integers(1, 37)))
            else:   # "floor": recognition varies, recall near zero
                cp, rt = int(rng.choice([4, 5, 6])), int(rng.choice([0, 0, 0, 1, 2, 3]))
            rc = int(rng.integers(0, min(rt, 18) + 1)) if rt else 0
            rc = max(rc, rt - 18)
            p[f"{c}{i}"] = {"cell": c, "cp": cp, "r_cat": rc, "r_cult": rt - rc, "cascade": i + 1}
    return p


def power_check(reps: int = 1000, h2_draws: int = 200) -> dict:
    import numpy as np
    rng = np.random.default_rng(SEEDS["POWER"])
    ns = (45, 90, 135, 180)
    pis = (0.50, 0.60, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95)
    ptab = {n: [binom_sf(k, n) for k in range(n + 1)] for n in ns}
    h1 = []
    for n in ns:
        for icc in (0.0, 0.2):
            for pi in pis:
                tally = Counter()
                sizes = [n // 5 + (1 if i < n % 5 else 0) for i in range(5)]
                for _ in range(reps):
                    if icc > 0:
                        ab = (1 - icc) / icc
                        pis_s = rng.beta(pi * ab, (1 - pi) * ab, size=5)
                    else:
                        pis_s = [pi] * 5
                    k = int(sum(rng.binomial(m, q) for m, q in zip(sizes, pis_s)))
                    A = k / n
                    p = ptab[n][k]
                    v = "FALSIFIED" if A < H1_FALS else ("CONFIRMED" if (A >= H1_CONF and p < ALPHA_PRIMARY)
                                                         else "MARGINAL")
                    tally[v] += 1
                h1.append({"n": n, "icc": icc, "true_agreement": pi,
                           **{f"P_{v}": tally[v] / reps for v in ("CONFIRMED", "MARGINAL", "FALSIFIED")}})
    h3 = []
    for n in ns[:3]:
        for pr in (0.05, 0.10, 0.20, 0.30):
            crit = next(c for c in range(n + 2) if binom_sf(c, n, int(pr * 100), 100) <= ALPHA_SECONDARY)
            for d in (0.05, 0.10, 0.15, 0.20):
                pd = min(pr + d, 1.0)
                h3.append({"n": n, "flip_rate_random": pr, "difference": d,
                           "power_approx": binom_sf(crit, n, int(round(pd * 100)), 100)})
    h2 = {}
    for sc in ("spread", "ties", "floor"):
        panels = [synthetic_panel(rng, sc) for _ in range(5)]
        h2[sc] = _h2_S_synthetic(panels, rng, h2_draws)
    return {"phase": PHASE_ID, "created_utc": _now(), "seed": SEEDS["POWER"], "reps": reps,
            "H1_operating_characteristics": h1,
            "H3_power_fixed_null_binomial_approximation": h3,
            "H2_S_on_synthetic_panels_75pct_subsets": h2,
            "note": "Synthetic only. H1: 5 equal clusters (substrates), beta-binomial between-cluster spread with "
                    "intra-cluster correlation icc. H3: exact binomial power against a fixed random-subset flip "
                    "rate (ignores Monte Carlo variance of the null). H2: S for three synthetic score shapes."}


# ===========================================================================
# SEC 10 - LOCK, ANCHOR, ORDER OF OPERATIONS
# ===========================================================================
REF_FILES = [REF_THREE_WAVE, REF_V23, REF_V19_OUTPUT, *REF_T1_VERDICTS.values()]
LOCKED_FILES = [
    V63 + "/prereg/PRE_REGISTRATION_v0_63.md",
    V63 + "/LOCK_STEPS.md",
    V63 + "/README.md",
    V63 + "/anchor/DEVIATIONS.md",
    V63 + "/registries/panel_rules_v0_63.json",
    V63 + "/prereg/parity_v0_63.json",
    V63 + "/prereg/power_v0_63.json",
    V63 + "/scripts/score_v0_63.py",
    V63 + "/scripts/test_score_v0_63.py",
    *REGISTRY_FILES.values(),
    *LOADER_CODE_FILES,
    *REF_FILES,
    *ARCHIVE_DATA_FILES,
]


def _git(*args) -> str:
    r = subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True)
    if r.returncode != 0:
        raise Halt(f"git {' '.join(args)} failed: {r.stderr.strip()[:200]}")
    return r.stdout.strip()


def tag_exists(tag: str = PREREG_TAG) -> bool:
    r = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "-q", "--verify", f"refs/tags/{tag}"],
                       capture_output=True, text=True)
    return r.returncode == 0 and bool(r.stdout.strip())


def lock_manifest_text(files=LOCKED_FILES, root: Path = ROOT) -> str:
    return "".join(f"{sha256_bytes((root / f).read_bytes())}  {f}\n" for f in files)


def verify_lock_manifest(path: Path = LOCK_MANIFEST, root: Path = ROOT) -> list:
    if not path.exists():
        return [f"lock manifest missing: {path}"]
    bad = []
    listed = set()
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        h, f = line.split("  ", 1)
        listed.add(f)
        p = root / f
        if not p.exists() or sha256_bytes(p.read_bytes()) != h:
            bad.append(f"changed since the lock: {f}")
    for f in LOCKED_FILES:
        if f not in listed:
            bad.append(f"not in the manifest: {f}")
    return bad


def lock_status(anchor: Path = ANCHOR_FILE, parity: Path = PARITY_FILE) -> tuple[bool, list]:
    """--run needs: tag v0.63-prereg-r1, the anchor file (written after push + OSF deposit), every locked file
    unchanged, and the pre-lock parity file recording a pass."""
    why = []
    if not tag_exists():
        why.append(f"git tag {PREREG_TAG} does not exist")
    if not Path(anchor).exists():
        why.append(f"anchor file {anchor} does not exist")
    if not why:
        why += verify_lock_manifest()
    if Path(parity).exists():
        if not json.loads(Path(parity).read_text()).get("passed"):
            why.append("parity file does not record a pass")
    else:
        why.append("parity file missing")
    return (not why), why


def write_anchor(osf_note: str = "", anchor: Path = ANCHOR_FILE) -> dict:
    """Written right after the tag is pushed and the OSF deposit is verified, before --run."""
    if anchor.exists():
        raise Halt(f"anchor already written: {anchor}")
    bad = verify_lock_manifest()
    if bad:
        raise Halt("lock manifest does not verify: " + "; ".join(bad[:5]))
    remote = _git("ls-remote", "--tags", "origin", PREREG_TAG)
    if f"refs/tags/{PREREG_TAG}" not in remote:
        raise Halt(f"tag {PREREG_TAG} is not on origin")
    commit = _git("rev-parse", f"{PREREG_TAG}^{{commit}}")
    if _git("rev-parse", "HEAD") != commit:
        raise Halt("HEAD is not the tagged commit")
    files = {}
    for line in LOCK_MANIFEST.read_text().splitlines():
        h, f = line.split("  ", 1)
        files[f] = {"sha256": h, "git_blob": git_blob_bytes((ROOT / f).read_bytes())}
    doc = {"tag": PREREG_TAG, "tag_object": _git("rev-parse", PREREG_TAG), "commit": commit,
           "tree": _git("rev-parse", f"{commit}^{{tree}}"), "branch": "v0.63",
           "tagger_date": _git("for-each-ref", f"refs/tags/{PREREG_TAG}", "--format=%(taggerdate:iso-strict)"),
           "remote_tag_ref": remote.splitlines()[0], "recorded_utc": _now(), "osf_deposit": osf_note,
           "lock_manifest_sha256": sha256_bytes(LOCK_MANIFEST.read_bytes()), "locked_files": files}
    _write_json(anchor, doc)
    return doc


def write_outputs(res: dict, outdir: Path, provenance: dict) -> Path:
    import csv
    out_json = outdir / "v0_63_verdicts.json"
    if out_json.exists():
        raise Halt(f"scored once: {out_json} already exists")
    outdir.mkdir(parents=True, exist_ok=True)
    comps = res.pop("comparisons")
    cols = ["wave", "substrate", "rule", "variant", "n_kept", "family", "canon", "alt", "status"]
    with open(outdir / "v0_63_comparisons.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for c in comps:
            w.writerow({k: c.get(k) for k in cols})
    _write_json(out_json, {"phase": PHASE_ID, "created_utc": _now(), "prereg_tag": PREREG_TAG, "seeds": SEEDS,
                           **provenance, **res})
    return out_json


def run_real(log=print) -> dict:
    ok, why = lock_status()
    if not ok:
        raise Halt("refusing to score before the lock: " + "; ".join(why))
    meta = load_registry_meta()
    frozen = json.loads(RULES_FILE.read_text(encoding="utf-8"))
    for s in OMNI:                                           # MC3: rule applications as frozen
        now = [[v[0], v[1], v[2]] for v in structural_variants(s, meta[s])]
        was = [[v["rule"], v["variant"], sorted(set(meta[s]) - set(v["dropped"]))]
               for v in frozen["substrates"][s]["variants"]]
        if now != was:
            raise Halt(f"MC3: structural rule application for {s} differs from {RULES_FILE.name}")
    arch = load_archive(meta)
    res = score_all(arch, meta, log=log)
    prov = {"dry_run": False, "anchor_sha256": sha256_bytes(ANCHOR_FILE.read_bytes()),
            "lock_manifest_sha256": sha256_bytes(LOCK_MANIFEST.read_bytes())}
    p = write_outputs(res, OUT_DIR, prov)
    log(f"[v0.63] verdicts: {res['verdicts']}  -> {p}")
    return res


def run_dry(path: Path, log=print, **kw) -> dict:
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    meta = {s: {b: {**v, "flags": set(v.get("flags", []))} for b, v in ms.items()} for s, ms in d["meta"].items()}
    res = score_all(d["archive"], meta, log=log, **kw)
    write_outputs(dict(res), Path(path).parent / "_score", {"dry_run": True, "input": str(path)})
    return res


def main(argv=None):
    ap = argparse.ArgumentParser(description="AIAS v0.63 panel-construction sensitivity scorer")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--rules", action="store_true")
    g.add_argument("--parity", action="store_true")
    g.add_argument("--power", action="store_true")
    g.add_argument("--lock-manifest", action="store_true")
    g.add_argument("--verify-lock", action="store_true")
    g.add_argument("--write-anchor", action="store_true")
    g.add_argument("--run", action="store_true")
    g.add_argument("--dry-run", metavar="FILE")
    ap.add_argument("--osf-note", default="")
    a = ap.parse_args(argv)
    try:
        if a.rules:
            _write_json(RULES_FILE, build_rules_doc())
            print(f"[v0.63] {RULES_FILE}")
            return 0
        if a.power:
            _write_json(POWER_FILE, power_check())
            print(f"[v0.63] {POWER_FILE}")
            return 0
        if a.lock_manifest:
            LOCK_MANIFEST.write_text(lock_manifest_text())
            print(f"[v0.63] {LOCK_MANIFEST} ({len(LOCKED_FILES)} files)")
            return 0
        if a.verify_lock:
            bad = verify_lock_manifest()
            print("lock manifest OK" if not bad else "\n".join(bad))
            return 0 if not bad else 1
        if a.write_anchor:
            d = write_anchor(a.osf_note)
            print(json.dumps({k: d[k] for k in ("tag", "tag_object", "commit", "tree")}, indent=1))
            return 0
        if a.dry_run:
            r = run_dry(Path(a.dry_run))
            print(json.dumps(r["verdicts"]))
            return 0
        if a.parity or a.run:
            if a.run:
                ok, why = lock_status()
                if not ok:
                    raise Halt("refusing to score before the lock: " + "; ".join(why))
            _ensure_home_shim()
            if a.parity:
                meta = load_registry_meta()
                doc = run_parity(load_archive(meta))
                _write_json(PARITY_FILE, doc)
                print(f"[v0.63] parity passed={doc['passed']}: " +
                      ", ".join(f"{k}={v['passed']}" for k, v in doc["checks"].items()))
                return 0 if doc["passed"] else 2
            run_real()
            return 0
    except Halt as e:
        print(f"[v0.63] HALT: {e}", file=sys.stderr)
        return 3
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
