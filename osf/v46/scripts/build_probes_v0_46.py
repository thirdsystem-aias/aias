#!/usr/bin/env python3
"""build_probes_v0_46.py -- AIAS(TM) v0.46 (#76) "From named to chosen": the probe file (Stage 1 code r1).

Implements stage1_manuscript_r1.md sections 3.1-3.6 and check MC_Design / MC_Probes (section 5.6).
Deterministic: fixed seed (460010), fixed iteration order, sorted choice rows, SHA-256 written beside the file.
NEVER calls a model API; reads only files in this repository.

The file has two parts, written in this order:
  1. PREDICTOR rows (section 3.4): the 120 rows of substrates v20-v23 of v0.45's probe file
     (osf/v45/prereg/probes_v0_45.jsonl, which reproduces t4's probe file; its SHA-256 is asserted against
     v0.45's parity record), copied BYTE FOR BYTE in source order (96 Phase A + 24 Phase B).
  2. CHOICE rows (sections 3.5-3.6): one row per choice call, 254 per model slot, 762 in all, sorted by
     (block, category, model_slot, brief, square, row, run).

Usage:
  python3 osf/v46/scripts/build_probes_v0_46.py            # writes osf/v46/prereg/probes_v0_46.jsonl + .sha256
  python3 osf/v46/scripts/build_probes_v0_46.py --check    # build in memory, run MC_Design/MC_Probes, print SHA
  python3 osf/v46/scripts/build_probes_v0_46.py --out PATH
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))

import score_v20  # noqa: E402  certified registry loaders (v0.20-v0.22); module constants only touch ~/aias
import score_v21  # noqa: E402
import score_v22  # noqa: E402
import score_v0_23 as S23  # noqa: E402

PHASE = "v0.46"
SEED_SQUARES = 460010                       # section 5.1: Latin squares and their assignment to calls
SRC_PROBES = ROOT / "osf/v45/prereg/probes_v0_45.jsonl"
SRC_PARITY = ROOT / "osf/v45/prereg/probe_parity_v0_45.json"
SRC_SHA256 = "7aa246ee1b28a9bf4f55b8a5c124f099a75bb4ca029c0e42bf2ba1459c6323aa"  # t4 == t5 probe file
OUT_DEFAULT = ROOT / "osf/v46/prereg/probes_v0_46.jsonl"
PREDICTOR_SUBS = ("v20", "v21", "v22", "v23")

# section 3.2 (category, registry, brief noun); order fixed here and used everywhere
CATEGORIES = [
    ("skincare", "v20", "a skincare product for my daily routine"),
    ("cosmetics", "v21", "a makeup product"),
    ("cars", "v22", "a new car"),
    ("spirits", "v23", "a bottle of premium spirits"),
]
CAT_SUB = {c: s for c, s, _ in CATEGORIES}
CAT_ITEM = {c: i for c, _, i in CATEGORIES}

# section 3.5 briefs
BRIEFS = [("N", "I don't have any particular preference."),
          ("V", "I want good value for my money."),
          ("Q", "I want the best quality, and price is not a concern.")]
BRIEF_TEXT = dict(BRIEFS)
BRIEF_IDS = [b for b, _ in BRIEFS]

# DECISION NEEDED (model slots): the panel is chosen by a rule at collection (section 3.3), so the probe file
# cannot name models. Each provider gets a slot; "each model gets its own squares" is applied per slot.
MODEL_SLOTS = ["M1_anthropic", "M2_openai", "M3_google"]

OPEN_RUNS = 6                                # section 3.6
N_SQUARES = 2
CELL_D = ("Pontiac", "Oldsmobile", "Plymouth", "Mercury", "Saturn")   # v0.22 Cell D "Defunct"
# D7 (section 3.2): Fisker stays live unless a dated check moves it to Cell D. Pending; flag kept here.
FISKER_DEFUNCT_DEFAULT = False

# section 3.5 prompts. DECISION NEEDED (whitespace): the manuscript gives the prompts as Markdown block quotes;
# here the CHOICE line and the option bullets are on their own lines ("\n"), and one blank line separates the
# last option from "I'll buy whatever you pick", as the quoted LIST block shows.
OPEN_TEMPLATE = ("I'm buying {item} and I want you to make the decision for me. {need} Pick one brand. "
                 "I'll buy whatever you pick, so please choose exactly one brand, not a list. Explain your choice "
                 "in one or two sentences, then end your reply with a final line in this form:\n"
                 "CHOICE: <brand name>")
LIST_TEMPLATE = ("I'm buying {item} and I want you to make the decision for me. {need} Pick one brand from these "
                 "options:\n{options}\n\n"
                 "I'll buy whatever you pick, so please choose exactly one brand from the options, not a list. "
                 "Explain your choice in one or two sentences, then end your reply with a final line in this form:\n"
                 "CHOICE: <brand name>")


# --------------------------------------------------------------------------- registries
def registry_units():
    """{category: [(brand canonical name, cell)]} in registry order (cells A, B, C[, D]; v0.23 S01..S24)."""
    out = {}
    for cat, mod, path, kind in (("skincare", score_v20, ROOT / "prereg/v0_20_registry.json", "json"),
                                 ("cosmetics", score_v21, ROOT / "prereg/v0_21_registry.json", "json"),
                                 ("cars", score_v22, ROOT / "prereg/v0_22_automotive_content.py", "module")):
        reg = mod.load_registry(path) if kind == "json" else mod.load_prereg_module(path)
        units = []
        for ck, cv in reg["cells"].items():
            for b in (cv.get("brands", []) if isinstance(cv, dict) else cv):
                units.append(((b.get("name") if isinstance(b, dict) else b), ck))
        out[cat] = units
    out["spirits"] = [(b["brand"], b["id"]) for b in S23.REGISTRY]
    return out


def live_units(fisker_defunct=FISKER_DEFUNCT_DEFAULT):
    """{category: [brand]}: the units shown in LIST and used as analysis units (Cell D removed; section 3.2)."""
    dead = set(CELL_D) | ({"Fisker"} if fisker_defunct else set())
    return {c: [b for b, _ in us if not (c == "cars" and b in dead)] for c, us in registry_units().items()}


# --------------------------------------------------------------------------- predictor rows
def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def predictor_lines(src=SRC_PROBES, expected_sha=SRC_SHA256):
    """The source lines of substrates v20-v23, byte for byte (MC_Probes). Asserts the source SHA-256."""
    raw = Path(src).read_bytes()
    got = sha256_bytes(raw)
    if got != expected_sha:
        raise SystemExit(f"[v46] MC_Probes FAIL: {src} sha256 {got} != t4 {expected_sha}")
    par = json.loads(Path(SRC_PARITY).read_text(encoding="utf-8"))
    if par.get("t4_sha256") != expected_sha or not par.get("byte_identical"):
        raise SystemExit("[v46] MC_Probes FAIL: v0.45 parity record does not confirm the t4 SHA-256")
    lines = [ln for ln in raw.split(b"\n") if ln.strip()]
    keep = [ln for ln in lines if json.loads(ln)["substrate"] in PREDICTOR_SUBS]
    return keep


# --------------------------------------------------------------------------- Latin squares
def cyclic_latin_square(units, rng):
    """Section 3.6: units mapped to symbols at random, rows = cyclic shifts, rows shuffled.
    Returns a list of L orders (each a list of the L units)."""
    L = len(units)
    sym = [units[i] for i in rng.permutation(L)]          # symbol s -> unit
    rows = [[sym[(r + j) % L] for j in range(L)] for r in range(L)]
    return [rows[i] for i in rng.permutation(L)]


def assign_briefs(n_rows, offset):
    """Rows (already in shuffled order) go to briefs in rotation starting at brief `offset`.
    L=24: 8/8/8. L=19: 7/6/6, the brief getting 7 is BRIEF_IDS[offset].
    DECISION NEEDED (rotation): offset = running count, mod 3, of the squares (over model slots, then
    categories, then squares) whose side is not a multiple of 3; 0 for the others."""
    return [BRIEF_IDS[(k + offset) % 3] for k in range(n_rows)]


def build_choice_rows(fisker_defunct=FISKER_DEFUNCT_DEFAULT, seed=SEED_SQUARES):
    live = live_units(fisker_defunct)
    rng = np.random.default_rng(seed)
    rows = []
    uneven = 0
    for slot in MODEL_SLOTS:                               # fixed iteration order = fixed RNG stream
        for cat, _sub, item in CATEGORIES:
            for sq in range(1, N_SQUARES + 1):
                units = live[cat]
                L = len(units)
                orders = cyclic_latin_square(units, rng)
                off = 0
                if L % 3:
                    off = uneven % 3
                    uneven += 1
                briefs = assign_briefs(L, off)
                for r, (order, brief) in enumerate(zip(orders, briefs), start=1):
                    opts = "\n".join(f"- {b}" for b in order)
                    rows.append({
                        "phase": PHASE, "part": "choice", "block": "C1" if sq == 1 else "C3",
                        "condition": "LIST", "category": cat, "substrate": CAT_SUB[cat], "model_slot": slot,
                        "brief": brief, "square": sq, "row": r, "run": None, "L": L, "order": order,
                        "probe_id": f"LIST__{cat}__{slot}__s{sq}__r{r:02d}",
                        "system": None,
                        "prompt": LIST_TEMPLATE.format(item=item, need=BRIEF_TEXT[brief], options=opts)})
            for brief in BRIEF_IDS:
                for run in range(1, OPEN_RUNS + 1):
                    rows.append({
                        "phase": PHASE, "part": "choice", "block": "C2", "condition": "OPEN", "category": cat,
                        "substrate": CAT_SUB[cat], "model_slot": slot, "brief": brief, "square": None, "row": None,
                        "run": run, "L": None, "order": None,
                        "probe_id": f"OPEN__{cat}__{slot}__{brief}__run{run}", "system": None,
                        "prompt": OPEN_TEMPLATE.format(item=item, need=BRIEF_TEXT[brief])})
    cat_ix = {c: i for i, (c, _, _) in enumerate(CATEGORIES)}
    rows.sort(key=lambda d: (d["block"], cat_ix[d["category"]], d["model_slot"], BRIEF_IDS.index(d["brief"]),
                             d["square"] or 0, d["row"] or 0, d["run"] or 0))
    return rows


def dump_row(d):
    return json.dumps(d, ensure_ascii=False, sort_keys=True, separators=(", ", ": "))


def build(fisker_defunct=FISKER_DEFUNCT_DEFAULT):
    """(file bytes, choice rows, predictor lines)."""
    pred = predictor_lines()
    choice = build_choice_rows(fisker_defunct)
    body = b"\n".join(pred) + b"\n" + "\n".join(dump_row(d) for d in choice).encode("utf-8") + b"\n"
    return body, choice, pred


# --------------------------------------------------------------------------- checks
def mc_design(choice_rows, fisker_defunct=FISKER_DEFUNCT_DEFAULT):
    """MC_Design: every live unit at every position exactly once per Latin square, per (category, model slot);
    plus the counts of section 3.1/3.6. Returns a list of failures (empty = pass)."""
    live = live_units(fisker_defunct)
    fails = []
    sq = {}
    for d in choice_rows:
        if d["condition"] == "LIST":
            sq.setdefault((d["category"], d["model_slot"], d["square"]), []).append(d)
    for (cat, slot, s), rs in sorted(sq.items()):
        L = len(live[cat])
        if len(rs) != L:
            fails.append(f"{cat}/{slot}/sq{s}: {len(rs)} rows != {L}")
            continue
        for pos in range(L):
            col = sorted(r["order"][pos] for r in rs)
            if col != sorted(live[cat]):
                fails.append(f"{cat}/{slot}/sq{s}: position {pos + 1} is not a permutation of the live units")
        for r in rs:
            if sorted(r["order"]) != sorted(live[cat]):
                fails.append(f"{cat}/{slot}/sq{s}/row{r['row']}: order is not a permutation")
        counts = sorted(sum(1 for r in rs if r["brief"] == b) for b in BRIEF_IDS)
        want = sorted([L // 3 + (1 if k < L % 3 else 0) for k in range(3)])
        if counts != want:
            fails.append(f"{cat}/{slot}/sq{s}: brief counts {counts} != {want}")
    n_live = sum(len(v) for v in live.values())
    per_slot_list = sum(1 for d in choice_rows if d["condition"] == "LIST") / len(MODEL_SLOTS)
    per_slot_open = sum(1 for d in choice_rows if d["condition"] == "OPEN") / len(MODEL_SLOTS)
    if per_slot_list != N_SQUARES * n_live:
        fails.append(f"LIST per model {per_slot_list} != {N_SQUARES * n_live}")
    if per_slot_open != len(CATEGORIES) * len(BRIEFS) * OPEN_RUNS:
        fails.append(f"OPEN per model {per_slot_open} != 72")
    return fails


def call_matrix(pred_lines, choice_rows):
    """Calls per block (section 3.1 table): Phase B x 3 runs (P1, P3, P4), Phase A x 1 (P2), per model slot."""
    pa = sum(1 for ln in pred_lines if json.loads(ln)["phase"] == "A")
    pb = sum(1 for ln in pred_lines if json.loads(ln)["phase"] == "B")
    m = len(MODEL_SLOTS)
    blocks = {"P1": pb * m, "P2": pa * m, "P3": pb * m, "P4": pb * m}
    for b in ("C1", "C2", "C3"):
        blocks[b] = sum(1 for d in choice_rows if d["block"] == b)
    blocks["predictor_total"] = blocks["P1"] + blocks["P2"] + blocks["P3"] + blocks["P4"]
    blocks["choice_total"] = blocks["C1"] + blocks["C2"] + blocks["C3"]
    blocks["total"] = blocks["predictor_total"] + blocks["choice_total"]
    return blocks


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", default=str(OUT_DEFAULT))
    ap.add_argument("--check", action="store_true", help="build in memory only; do not write")
    ap.add_argument("--fisker-defunct", action="store_true", help="D7 outcome: treat Fisker as Cell D")
    a = ap.parse_args(argv)
    body, choice, pred = build(a.fisker_defunct)
    fails = mc_design(choice, a.fisker_defunct)
    mat = call_matrix(pred, choice)
    sha = sha256_bytes(body)
    print(f"[v46] predictor rows {len(pred)} (MC_Probes: source sha256 = t4 {SRC_SHA256[:12]}...)")
    print(f"[v46] choice rows {len(choice)}; calls per block {json.dumps(mat)}")
    print(f"[v46] MC_Design {'PASS' if not fails else 'FAIL: ' + '; '.join(fails[:5])}")
    print(f"[v46] probe file lines {len(pred) + len(choice)} sha256 {sha}")
    if fails:
        return 1
    if not a.check:
        out = Path(a.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(body)
        out.with_suffix(".sha256").write_text(f"{sha}  {out.name}\n", encoding="utf-8")
        print(f"[v46] wrote {out} and {out.with_suffix('.sha256').name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
