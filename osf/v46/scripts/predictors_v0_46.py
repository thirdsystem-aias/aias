#!/usr/bin/env python3
"""predictors_v0_46.py -- AIAS(TM) v0.46 (#76): Presence P and Ranking R* per unit from the raw predictor answers.

Implements stage1_manuscript_r2.md section 3.4 ("Presence P", "Ranking R*") and section 5.1 ("Predictors").

REFERENCE IMPLEMENTATION (imported, not re-written): v1.14 Stage 1 as run on t4 at commit
3129674a6c2cca64e56cd0f6696e9ab21b385a9a (main repo; "v1.14 Stage 1 (once, on t4 at v0.42-scoring-locked)").
The two files it ran are vendored byte for byte in osf/v46/scripts/ref_v1_14/ from `git show 3129674:scripts/...`
and verified here (SHA-256 and git blob) before import:
    scripts/score_v1_14.py  blob 7aeb18316a23c699a0a6a4358e52ab09f9546ca9 (last changed in a5feb4b)
    scripts/score_v1_10.py  blob 0f8b981b2895a325b50629c85f8e0e6ce8e876f5 (imported by score_v1_14 as R)
Functions used, unchanged:
    P  : score_v1_14.comparators (P = 100 (C_P/3 + 2 pi_hat)/3; C_P/3 = share of the panel's models coding the
         brand recognised in their one S0 Phase A answer; models without a coded answer leave the denominator).
         pi_hat is v0.42's pi_N3_S0, which v1.14 read from v0.42's brand table and asserted (MQ8,
         score_v1_14.comparator_parity) equal to sum(mentions) / (answered Phase B calls) over the panel's models
         x runs 1-3 in the substrate. No brand table exists for v0.46, so pi_hat is computed here with exactly the
         recomputation MQ8 used (`pi_hat` below) and passed to `comparators` in a brand-table row.
    R* : score_v1_14.phase_b_answers -> extract_wave (rules E0-E7, URL-stripped text) -> wave_rows(rule
         "lead_item", condition S0) -> unit_scores (rating floor 6) -> statistic MODE (= modal_position).
The only change is the panel: the three models of section 3.3 in place of t4's N3 (argument `models`).

Registries: the five omnibus registries exactly as v1.10 loads them (score_v1_10.load_registry), each file verified
against the SHA-256 that v1.10's input manifest (osf/methodology/v1_10/registries/INPUTS_MANIFEST_v1_10.json at
3129674) pins. v0.23's file osf/methodology/v1_10/registries/v0_23_registry_v1_10.json was restored from git
(blob 5d6df9c6, first added in 672365b, unchanged at 3129674).

Inputs: raw records in t4's schema (call_id, substrate v20..v23, phase A|B, condition S0, run, model_requested,
served_model, status, text, error, frame_id, probe_id) and v0.42's coded tables (code_t4_v0_42.py output:
{sub}_phase_a.csv, {sub}_phase_b.csv). Coding itself is v0.42's locked coder, run before this module.
NO MODEL IS CALLED. No network.

Usage:
  python3 osf/v46/scripts/predictors_v0_46.py --raw RAW.jsonl --coded-dir DIR --models M1 M2 M3 --out PRED.csv
"""
import argparse
import collections
import csv
import hashlib
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
REF_DIR = HERE / "ref_v1_14"
REF_COMMIT = "3129674a6c2cca64e56cd0f6696e9ab21b385a9a"
REF_FILES = {   # vendored file: (sha256, git blob) of `git show 3129674:scripts/<file>`
    "score_v1_10.py": ("651cb8c240e914e2a82f9b31aa5e46eb5d9d61dbb7a8b4d7072b91d2997975a5",
                       "0f8b981b2895a325b50629c85f8e0e6ce8e876f5"),
    "score_v1_14.py": ("b087fc818105710079e8fea3c8c279373f787efe48c62cbccdcfb0392e1484ce",
                       "7aeb18316a23c699a0a6a4358e52ab09f9546ca9"),
}


class PredictorHalt(RuntimeError):
    """A hash mismatch or an input that cannot be scored."""


def _git_blob(b):
    return hashlib.sha1(b"blob %d\0" % len(b) + b).hexdigest()


def verify_reference(ref_dir=REF_DIR):
    bad = []
    for name, (sha, blob) in REF_FILES.items():
        p = Path(ref_dir) / name
        if not p.exists():
            bad.append(f"missing {p}")
            continue
        b = p.read_bytes()
        if hashlib.sha256(b).hexdigest() != sha or _git_blob(b) != blob:
            bad.append(f"hash mismatch {p}")
    return bad


_bad = verify_reference()
if _bad:
    raise PredictorHalt("v1.14 reference code not as at 3129674: " + "; ".join(_bad))
sys.path.insert(0, str(REF_DIR))
import score_v1_14 as V114  # noqa: E402  (v1.14 Stage 1 code, unchanged)

R = V114.R                   # score_v1_10, unchanged
STAT = V114.STAT             # "MODE"
RATING_FLOOR = V114.RATING_FLOOR   # 6
RULE = "lead_item"
COND = "S0"                  # section 3.7: search off only
RUNS = V114.RUNS             # (1, 2, 3)

# v1.10 input manifest at 3129674: registry path, loader format, SHA-256
REGISTRIES = {
    "v0.19": ("osf/v19/panel_registry_v0_19.csv", "v19_csv",
              "4aba558d5247f1dc250184ce009884e5f49d82697789dbf78beb77557b50dc44"),
    "v0.20": ("prereg/v0_20_registry.json", "cells_json",
              "eb9559eaa6595eaf588dc5ec26c5c742d14c91d4ea93aaedd1e4577e3fa25782"),
    "v0.21": ("prereg/v0_21_registry.json", "cells_json",
              "45efbae5db983c24e00ad30d4b66369e685857295e8fd292a0ee0ca73349b5d3"),
    "v0.22": ("prereg/v0_22_automotive_content.py", "v22_module",
              "431f919c809c6260815b9a7a10fe14cb915ae2ce67660aaa6ef48227783d66b9"),
    "v0.23": ("osf/methodology/v1_10/registries/v0_23_registry_v1_10.json", "v23_json",
              "776d01bc154ce8802432a60aa13394f929e2f4523a07d95bde1711bd94eea33d"),
}
V46_SUBS = ("v0.20", "v0.21", "v0.22", "v0.23")
SUB_CAT = {"v0.20": "skincare", "v0.21": "cosmetics", "v0.22": "cars", "v0.23": "spirits"}
CAT_SUB = {c: s for s, c in SUB_CAT.items()}


class _Ctx:
    """Stands in for score_v1_10.Ctx: resolves only the pinned registry files, after their SHA-256 check."""

    def __init__(self, root=ROOT):
        self.root = Path(root)
        self.pinned = {rel: sha for rel, _f, sha in REGISTRIES.values()}

    def path(self, rel):
        if rel not in self.pinned:
            raise PredictorHalt(f"not a pinned registry file: {rel}")
        p = self.root / rel
        if not p.exists():
            raise PredictorHalt(f"missing registry file: {p}")
        if hashlib.sha256(p.read_bytes()).hexdigest() != self.pinned[rel]:
            raise PredictorHalt(f"registry hash mismatch: {rel}")
        return p


def load_registries(subs=V46_SUBS, root=ROOT):
    """{substrate: (registry {canonical: [aliases]}, unit {canonical: unit key})}, as v1.14 load_registries_v110."""
    ctx = _Ctx(root)
    return {s: R.load_registry(ctx, REGISTRIES[s][0], REGISTRIES[s][1])[:2] for s in subs}


# =========================================================================== analysis set
def analysis_set(raw_records, models, wave="v46"):
    """v1.14 phase_b_answers on the panel `models`: Phase B answers (E0: unanswered = missing cell) and the
    excluded call IDs (outside the design, or answered by another served model ID)."""
    return V114.phase_b_answers(raw_records, wave, models)


def read_coded_dir(coded_dir):
    """v0.42's coded tables, read exactly as v1.14 read them (score_v1_14.read_coded)."""
    return V114.read_coded(V114.Source(base=Path(coded_dir)), ".")


# =========================================================================== Presence
def pi_hat(coded_b, excluded, models, units, cond=COND):
    """Recall Presence per unit: mentions / answered Phase B calls, pooled over `models` x runs 1-3 of the unit's
    substrate (the recomputation of v0.42's pi_N3_S0 that v1.14's MQ8, comparator_parity, asserted exact)."""
    k, ans = collections.defaultdict(int), collections.defaultdict(set)
    for r in coded_b:
        if r["call_id"] in excluded or r["condition"] != cond:
            continue
        ans[(r["model"], r["run"], r["substrate"])].add(r["call_id"])
        k[(r["model"], r["run"], r["substrate"], r["brand"])] += int(r["mentioned"])
    out = {}
    for s, b in units:
        num = sum(k.get((m, r, s, b), 0) for m in models for r in RUNS)
        den = sum(len(ans.get((m, r, s), ())) for m in models for r in RUNS)
        out[(s, b)] = num / den if den else None
    return out


def presence(coded_a, coded_b, excluded, models, units, cond=COND):
    """{"P", "pi_hat", "mentions"} per unit via v1.14's `comparators` (unchanged), pi_hat from `pi_hat`."""
    pi = pi_hat(coded_b, excluded, models, units, cond)
    table = [{"substrate": s, "brand": b, f"pi_N3_{cond}": pi[(s, b)], f"phi_N3_{cond}": "",
              f"phi_partition_N3_{cond}": ""} for s, b in units]
    comp = V114.comparators(table, coded_a, coded_b, excluded, cond, models)
    rec = collections.defaultdict(lambda: [0, 0])
    for r in coded_a:
        if r["condition"] != "S0" or r["model"] not in models or r["call_id"] in excluded or r["recognized"] is None:
            continue
        rec[(r["substrate"], r["brand"])][0] += int(r["recognized"])
        rec[(r["substrate"], r["brand"])][1] += 1
    return {"P": comp["P"], "pi_hat": comp["pi_hat"], "mentions": comp["mentions"],
            "recognized": {u: tuple(rec[u]) if u in rec else (0, 0) for u in units}}


# =========================================================================== Ranking
def ranking(answers, registries, cond=COND, floor=RATING_FLOOR):
    """{unit: {"n_ranked", "MODE", "rated", ...}} via v1.14 extract_wave -> wave_rows(lead_item) -> unit_scores."""
    answers = [a for a in answers if a["category"] in registries]
    infos = V114.extract_wave(answers, registries)
    rows = V114.wave_rows(infos, RULE, cond)
    return V114.unit_scores(rows, floor), infos


def registry_units(registries):
    """[(substrate, unit key)] in registry order (v0.23 unit keys are its S-ids, as in v1.14)."""
    return [(s, u) for s, (_reg, unit) in registries.items() for u in unit.values()]


# =========================================================================== both predictors
def compute(raw_records, coded_a, coded_b, models, subs=V46_SUBS, registries=None, wave="v46"):
    """Every unit of `subs`: P, pi_hat, recognition counts, n_ranked, R* (None when unrated), plus per-model
    pi_hat (descriptive 5). Keys are (substrate, unit key) as in v1.14."""
    models = list(models)
    if len(set(models)) != len(models) or not models:
        raise PredictorHalt(f"bad panel: {models}")
    registries = registries or load_registries(subs)
    answers, meta = analysis_set(raw_records, models, wave)
    excluded = set(meta["excluded_call_ids"])
    units = registry_units(registries)
    pres = presence(coded_a, coded_b, excluded, models, units)
    U, infos = ranking(answers, registries)
    per_model = {m: pi_hat(coded_b, excluded, [m], units) for m in models}
    out = {}
    for u in units:
        s = U.get(u)
        rated = bool(s and s["rated"])
        out[u] = {"P": pres["P"].get(u), "pi_hat": pres["pi_hat"].get(u), "mentions": pres["mentions"].get(u, 0),
                  "recognized": pres["recognized"][u][0], "recognition_coded": pres["recognized"][u][1],
                  "n_ranked": int(s["n_ranked"]) if s else 0, "rated": rated,
                  "R_star": float(s[STAT]) if rated else None,
                  "pi_hat_by_model": {m: per_model[m].get(u) for m in models}}
    meta = dict(meta, models=models, substrates=list(subs), reference_commit=REF_COMMIT,
                answers=len(answers), rankable_rows=sum(v["n_ranked"] for v in U.values()))
    meta["_infos"] = infos      # per-answer extraction (for G2's orientation check); not written to files
    return out, meta


def unit_names(registries):
    """(substrate, unit key) -> (v0.46 category, canonical brand name)."""
    out = {}
    for s, (_reg, unit) in registries.items():
        for canon, key in unit.items():
            out[(s, key)] = (SUB_CAT.get(s, s), canon)
    return out


TABLE_COLS = ["category", "brand", "substrate", "unit_key", "P", "R_star", "pi_hat", "mentions", "recognized",
              "recognition_coded", "n_ranked", "rated"]


def table_rows(pred, registries):
    """Rows for score_v0_46.read_predictors (category, brand, P, R_star, pi_hat) plus provenance columns."""
    names = unit_names(registries)
    rows = []
    for (s, key), v in pred.items():
        cat, brand = names[(s, key)]
        rows.append({"category": cat, "brand": brand, "substrate": s, "unit_key": key,
                     "P": "" if v["P"] is None else repr(float(v["P"])),
                     "R_star": "" if v["R_star"] is None else repr(float(v["R_star"])),
                     "pi_hat": "" if v["pi_hat"] is None else repr(float(v["pi_hat"])),
                     "mentions": v["mentions"], "recognized": v["recognized"],
                     "recognition_coded": v["recognition_coded"], "n_ranked": v["n_ranked"], "rated": int(v["rated"])})
    return rows


def write_table(rows, path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=TABLE_COLS, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--raw", required=True)
    ap.add_argument("--coded-dir", required=True)
    ap.add_argument("--models", nargs="+", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    raw = V114.read_jsonl_text(Path(a.raw).read_text(encoding="utf-8"))
    ca, cb = read_coded_dir(a.coded_dir)
    regs = load_registries()
    pred, meta = compute(raw, ca, cb, a.models, registries=regs)
    write_table(table_rows(pred, regs), a.out)
    print(f"[v46 predictors] {len(pred)} units; rated {sum(v['rated'] for v in pred.values())}; "
          f"P defined {sum(v['P'] is not None for v in pred.values())}; answers {meta['answers']} -> {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
