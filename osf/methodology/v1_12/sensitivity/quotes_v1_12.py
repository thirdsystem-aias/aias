#!/usr/bin/env python3
"""
quotes_v1_12.py - AIAS(TM) 3.0 pre-registration section 10.2 (D4): the coding sensitivity S-Q for Coverage Papers A
(v1.12) and B (v1.19), "typographic quotes normalised". NOT part of any locked pipeline: v1.12's locked coding and
scorers stay primary for v1.12, v1.19 and every statistic of AIAS 3.0. This wrapper imports the locked modules
unchanged and changes no locked file. Written 2026-11-28 after the AIAS 3.0 lock (tag aias-3-0-prereg-r1), tested on
synthetic data only; not run on program data. No model call, no network beyond `git ls-remote` in the guards.

Definition (section 10.2, exactly):
  1. Text map. In the answer text (the raw record's "text" field) of every call in v112_raw.jsonl (949be61; all four
     models), U+2019 and U+2018 are replaced by U+0027. No other character changes. The wrapper first counts every
     other apostrophe-like character (U+02BC, U+2032, U+FF07, U+201B) in the file and reports the count; it maps none.
  2. Both sides together. The comparators come from t4's S-Q tables (47f1748: v42_brand_table_SQ.csv, SHA-256
     de8559cb..., and t4_SQ/coded/), read, not re-made; recognition codes unchanged. H7's legacy comparator (AIAS 2.0's
     t3 Presence) is kept as published (no S-Q table of t3 is locked).
  3. Coding. v0.42's coder (v1.12's vendored copy, blob 2d36735d, re-checked at tag v0.42-prereg-r1) codes the mapped
     text exactly as v1.12's primary run did (score_v1_12.code_coverage).
  4. Scoring. score_v1_12.score_coverage, unchanged, with its seeds and settings (10,000 / 10,000 draws; P1 record,
     MC_BrandFree record, H5 from v1.14's Stage 1 output as published), on the S-Q tables; then score_v1_19.run_real,
     unchanged (blob-checked against v1.19's lock manifest), on the S-Q tables of v1.12. AIAS 3.0's own statistics on the
     S-Q inputs are computed by osf/aias_3_0/scripts/score_aias_3_0.py in the same run as the primary (its N10).
  5. Reproduction first. Before writing anything, the wrapper re-codes v1.12 with the locked coder and re-scores v1.12
     and v1.19 with the locked scorers; it writes nothing unless 0 coded cells, 0 leaves of v112_verdicts.json and
     v119_verdicts.json and 0 cells of v112_unit_table.csv differ from the published files.
  6. When. Once, after the AIAS 3.0 lock and after the S-Q DEVIATIONS entries are committed on v1.12 and v1.19; the
     wrapper refuses to overwrite its outputs.
  7. Reporting. Beside each v1.12 and v1.19 statistic: the S-Q value, its label and whether the label is the same
     (comparison in sq_record_v1_12.json); a changed label is "coding-sensitive".

Outputs (this folder, osf/methodology/v1_12/sensitivity/): coded_SQ/ (v112_mentions.csv, registry_v1_12.json,
coding_record_v1_12.json), v112_verdicts_SQ.json, v112_unit_table_SQ.csv, v119_verdicts_SQ.json, flips_v1_12_SQ.json
(cell by cell: substrate, brand, model, panels, CEP, run; and the answers holding U+2019 / U+2018), sq_record_v1_12.json
(definition, reproduction, counts, the v1.14 read-only check, comparison, inputs read).

WRAPPER_NOTES (where the text is silent; "A<n>" = listed in the hand-off as an ambiguity)
 Q1 (A11) "0 leaves differ" ignores the leaves that hold local file paths of the original run (inputs.raw,
    inputs.coded, inputs.t4.*, H5_ranking_source.file): they name where the files were, not a result. Every hash leaf
    (raw_sha256, scorer_sha256, coder, rank-table SHA-256) is compared.
 Q2 (A12) v1.19 on S-Q reads the mapped raw text (its caveat counts read answer text), the S-Q coded tables, verdict
    file and unit table of v1.12, and t4's S-Q coded tables for its identity load (both sides together, step 2).
 Q3 (A13) The DEVIATIONS guard: refs origin/v1.12 and origin/v1.19 (overridable) must hold an anchor/DEVIATIONS.md whose
    locked bytes (at the lock tag) are an unchanged prefix and whose added text has an entry naming "S-Q" and "U+2019".
 Q4 (A14) The v1.14 check (the [OPEN] item of 10.2 step 4) is read-only: t4 S0 Phase B answers of N3 whose text
    names Paula's Choice or L'Oreal Paris only with U+2019/U+2018, and whether v1.14's Stage 1 rank table (3129674) lists
    that brand for that answer. Reported; it changes nothing.
"""
from __future__ import annotations

import argparse
import collections
import csv
import hashlib
import importlib.util
import json
import math
import re
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]                       # <repo>/osf/methodology/v1_12/sensitivity -> <repo>
for _p in (ROOT / "osf/methodology/v1_12/scripts", ROOT / "osf/aias_3_0/scripts"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))
import score_v1_12 as A        # noqa: E402  (locked; imported unchanged)
import score_aias_3_0 as R3    # noqa: E402  (git readers, MQ_Lock, pins)

QUOTE_MAP = {"’": "'", "‘": "'"}
_TABLE = str.maketrans(QUOTE_MAP)
OTHER_APOSTROPHE_LIKE = {"U+02BC": "ʼ", "U+2032": "′", "U+FF07": "＇", "U+201B": "‛"}
OUT_DIR = HERE
OUTPUTS = {"coded": "coded_SQ", "v112_verdicts": "v112_verdicts_SQ.json", "v112_unit_table": "v112_unit_table_SQ.csv",
           "v119_verdicts": "v119_verdicts_SQ.json", "flips": "flips_v1_12_SQ.json", "record": "sq_record_v1_12.json"}
IGNORED_PATH_LEAVES = (r"^\.inputs\.raw$", r"^\.inputs\.coded$", r"^\.inputs\.t4\.", r"^\.H5_ranking_source\.file$")

P = R3.PINS
SQ_PINS = {
    "v1.12_anchor": {"ref": P["v1.12"]["ref"], "p1": "osf/methodology/v1_12/anchor/parity_P1_v1_12.json",
                     "brandfree": "osf/methodology/v1_12/anchor/mc_brandfree_v1_12.json",
                     "profiles": "osf/aias_2_0/aias_2_0_profiles.csv"},
    "v1.14": {"ref": "3129674a6c2cca64e56cd0f6696e9ab21b385a9a",
              "stage1": "osf/methodology/v1_14/outputs/stage1/stage1_v1_14.json",
              "rank_table": "osf/methodology/v1_14/outputs/stage1/rank_table_t4_v1_14.csv"},
    "v1.19": {"ref": "6e8f1570de0967749a7ab2e8e0a4e968c9a18c06", "lock_tag": "v1.19-prereg-r1",
              "manifest": "osf/methodology/v1_19/prereg/LOCK_MANIFEST_v1_19.sha256",
              "scorer": "osf/methodology/v1_19/scripts/score_v1_19.py",
              "scorer_sha256": "7bbf6b1cc22aa26ed2892c07cab930c4497515c06b54261c5b3365c19b2c4242",
              "roster": "osf/methodology/v1_19/prereg/phantom_roster_v1_19.csv",
              "verdicts": "osf/methodology/v1_19/outputs/v119_verdicts.json",
              "il_t1": "osf/methodology/v1_7/data/v1_7_cpc.csv"},
    "v0.42_probes": {"ref": P["v0.42"]["ref"], "path": "osf/v42/prereg/probes_v0_42.jsonl"},
    "deviations": {"v1.12": {"ref": "origin/v1.12", "path": "osf/methodology/v1_12/anchor/DEVIATIONS.md",
                             "lock_tag": "v1.12-prereg-r1"},
                   "v1.19": {"ref": "origin/v1.19", "path": "osf/methodology/v1_19/anchor/DEVIATIONS.md",
                             "lock_tag": "v1.19-prereg-r1"}},
}


class Refused(RuntimeError):
    pass


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def sha256_file(p) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


# --------------------------------------------------------------------------- step 1: the text map and the counts
def normalise(text):
    return text.translate(_TABLE) if isinstance(text, str) else text


def normalise_records(records: list[dict]) -> list[dict]:
    """Copies of the raw records with the answer text mapped; the inputs are not modified."""
    return [dict(r, text=normalise(r["text"])) if isinstance(r.get("text"), str) else dict(r) for r in records]


def apostrophe_counts(records: list[dict]) -> dict:
    """Answers (raw lines with text) holding U+2019 / U+2018, by substrate and model; and every other apostrophe-like
    character of section 10.2 step 1, counted (characters and lines) and NOT mapped."""
    curly = collections.Counter()
    other = {k: {"characters": 0, "lines": 0} for k in OTHER_APOSTROPHE_LIKE}
    for r in records:
        t = r.get("text")
        if not isinstance(t, str):
            continue
        if any(ch in t for ch in QUOTE_MAP):
            curly[f"{r.get('substrate')}|{r.get('model_requested')}"] += 1
        for k, ch in OTHER_APOSTROPHE_LIKE.items():
            n = t.count(ch)
            if n:
                other[k]["characters"] += n
                other[k]["lines"] += 1
    return {"lines_with_U2019_or_U2018": dict(sorted(curly.items())), "total_lines_with_U2019_or_U2018": sum(curly.values()),
            "other_apostrophe_like_not_mapped": other}


def answered_counts(records: list[dict]) -> dict:
    """The count of answers (deduplicated, answered calls) holding U+2019 or U+2018, by substrate and model."""
    c = collections.Counter()
    for r in A.dedupe_calls(records):
        if A.is_answered(r) and any(ch in r["text"] for ch in QUOTE_MAP):
            c[f"{r['substrate']}|{r['model_requested']}"] += 1
    return {"by_substrate_model": dict(sorted(c.items())), "total": sum(c.values())}


# --------------------------------------------------------------------------- comparisons
def mention_diffs(primary_rows: list[dict], sq_rows: list[dict]) -> dict:
    """Cells (call x brand) whose code differs; each with substrate, brand, model, the panels holding the model, CEP
    (probe) and run."""
    key = lambda r: (r["call_id"], r["brand"])                          # noqa: E731
    p, q = {key(r): r for r in primary_rows}, {key(r): r for r in sq_rows}
    cells = []
    for k in sorted(set(p) | set(q)):
        a, b = p.get(k), q.get(k)
        va = int(a["mentioned"]) if a else None
        vb = int(b["mentioned"]) if b else None
        if va != vb:
            r = a or b
            cells.append({"call_id": r["call_id"], "substrate": r["substrate"], "brand": r["brand"], "model": r["model"],
                          "panels": [n for n, ms in A.PANELS.items() if r["model"] in ms], "cep": r["probe_id"],
                          "run": int(r["run"]), "primary": va, "SQ": vb})
    by = collections.Counter(f"{c['substrate']}|{c['brand']}|{c['model']}" for c in cells)
    return {"n_cells_differ": len(cells),
            "by_direction": dict(collections.Counter(f"{c['primary']}->{c['SQ']}" for c in cells)),
            "by_substrate_brand_model": dict(sorted(by.items(), key=lambda kv: (-kv[1], kv[0]))), "cells": cells}


def _leaves(o, p=""):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from _leaves(v, f"{p}.{k}")
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from _leaves(v, f"{p}[{i}]")
    else:
        yield p, o


def json_leaf_diff(a, b, ignore=IGNORED_PATH_LEAVES, tol=1e-12) -> list:
    """Leaves that differ (v0.45's json_diff, with the local-path leaves of Q1 ignored)."""
    la, lb = dict(_leaves(a)), dict(_leaves(b))
    pats = [re.compile(x) for x in ignore]
    out = []
    for k in sorted(set(la) | set(lb)):
        if any(pt.search(k) for pt in pats):
            continue
        x, y = la.get(k, "<absent>"), lb.get(k, "<absent>")
        if isinstance(x, float) and isinstance(y, float) and (abs(x - y) <= tol or (x != x and y != y)):
            continue
        if x != y:
            out.append([k, x, y])
    return out


def csv_cell_diff(pa, pb, keys=("substrate", "brand")) -> list:
    Ra = {tuple(r[k] for k in keys): r for r in A.read_csv_rows(pa)}
    Rb = {tuple(r[k] for k in keys): r for r in A.read_csv_rows(pb)}
    out = []
    for k in sorted(set(Ra) | set(Rb)):
        if k not in Ra or k not in Rb:
            out.append([list(k), "<row>", k in Ra, k in Rb])
            continue
        for c in set(Ra[k]) | set(Rb[k]):
            if Ra[k].get(c) != Rb[k].get(c):
                out.append([list(k), c, Ra[k].get(c), Rb[k].get(c)])
    return out


def compare_v112(pub: dict, sq: dict) -> list:
    rows = [{"test": "paper_A_verdict (GATE; never re-opened by S-Q)", "primary": pub["paper_A_verdict"]["verdict"],
             "SQ": sq["paper_A_verdict"]["verdict"]}]
    for h, v in pub["verdicts"].items():
        lp, lq = pub["legs"].get(h, {}), sq["legs"].get(h, {})
        rows.append({"test": h, "primary": v, "SQ": sq["verdicts"].get(h), "rho_w_primary": lp.get("rho_w"),
                     "rho_w_SQ": lq.get("rho_w"), "n_primary": lp.get("n"), "n_SQ": lq.get("n")})
    rows.append({"test": "MC_Situation", "primary": pub["MC"]["MC_Situation"].get("passed"),
                 "SQ": sq["MC"]["MC_Situation"].get("passed")})
    for r in rows:
        r["same_label"] = r["primary"] == r["SQ"]
        r["flag"] = "" if r["same_label"] else "coding-sensitive"
    return rows


def compare_v119(pub: dict, sq: dict) -> list:
    a, b = pub.get("verdict_summary") or {}, sq.get("verdict_summary") or {}
    rows = [{"test": k, "primary": a.get(k), "SQ": b.get(k)} for k in sorted(set(a) | set(b))]
    if not a or not b:
        rows.append({"test": "status", "primary": pub.get("status"), "SQ": sq.get("status")})
    for r in rows:
        r["same_label"] = r["primary"] == r["SQ"]
        r["flag"] = "" if r["same_label"] else "coding-sensitive"
    return rows


# --------------------------------------------------------------------------- steps 3-4: coding and scoring, unchanged
def v112_inputs(src: dict, raw_path, coded_dir, t4_side: str) -> tuple[dict, dict]:
    """The inputs score_v1_12.run_score assembles for its --run (H5 from v1.14's Stage 1 output; P1 and MC_BrandFree
    from v1.12's anchor), with t4's primary or S-Q tables."""
    mentions, registry = A.read_coded(coded_dir)
    t = src["t4"][t4_side]
    t4, window, missing = A.load_t4(src["t4_raw"], t["coded"], t["brand_table"], t["verdicts"])
    if missing:
        raise Refused(f"t4 files missing: {missing}")
    bf = json.loads(Path(src["brandfree"]).read_text(encoding="utf-8")) if src.get("brandfree") else None
    if bf:
        bf.pop("registry", None)
    inp = {"raw": A.read_jsonl(raw_path), "mentions": mentions, "registry": registry,
           "probes": A.load_probes(src["v112_probes"]), "t4": t4, "t4_window": window, "t4_missing": [],
           "profiles": A.read_csv_rows(src["profiles"]) if src.get("profiles") else None,
           "active": {}, "extra": {}, "h6_cross_panel": False, "brandfree": bf}
    if src.get("h5_stage1"):
        s = A.load_ranking_source(src["h5_stage1"], A.H5_CONDITION, allow_dry=bool(src.get("allow_dry_h5")))
        inp["active"]["H5_Sep_Ranking"] = True
        inp["extra"]["H5_Sep_Ranking"] = s["values"]
        inp["h5_source"], inp["h5_unavailable"] = s, None
    gates = {"enforce": True, "require_p1": bool(src.get("require_p1"))}
    if src.get("p1"):
        gates["P1"] = json.loads(Path(src["p1"]).read_text(encoding="utf-8")).get("v1_12")
    paths = {"raw": str(raw_path), "coded": str(coded_dir),
             "t4": {"raw": str(src["t4_raw"]), "coded": str(t["coded"]), "brand_table": str(t["brand_table"]),
                    "verdicts": str(t["verdicts"])}}
    return inp, {"gates": gates, "paths": paths}


def score_v112(src: dict, raw_path, coded_dir, t4_side: str, verdicts_path, table_path, cfg=None) -> dict:
    """score_v1_12.score_coverage unchanged, with the inputs block run_score adds, written by v1.12's writer."""
    inp, meta = v112_inputs(src, raw_path, coded_dir, t4_side)
    doc, rows = A.score_coverage(inp, cfg or A.Cfg(), meta["gates"])
    doc["inputs"] = {"raw": meta["paths"]["raw"], "raw_sha256": A.sha256_file(raw_path), "coded": meta["paths"]["coded"],
                     "t4": meta["paths"]["t4"], "t4_missing": [], "scorer_sha256": A.sha256_file(A.__file__),
                     "coder": A.verify_coder()}
    A.write_outputs(doc, rows, verdicts_path, table_path)
    return json.loads(Path(verdicts_path).read_text(encoding="utf-8"))


def load_v119(scorer_path):
    """score_v1_19.py from its scored commit, imported unchanged (its SHA-256 is checked by the caller)."""
    spec = importlib.util.spec_from_file_location("score_v1_19", str(scorer_path))
    mod = importlib.util.module_from_spec(spec)
    sys.modules["score_v1_19"] = mod
    spec.loader.exec_module(mod)
    return mod


def run_v119(S19, src: dict, a_raw, a_coded, a_verdicts, a_unit_table, t4_coded, out_dir, n_perm=None, gap_b=None):
    """score_v1_19.run_real unchanged (guards off: the wrapper's own guards ran), output in out_dir. Returns the
    written document (v119_verdicts.json, or v119_not_run.json when Paper A's verdict does not let Paper B run)."""
    v = src["v119"]
    paths = {"a_raw": a_raw, "a_coded": a_coded, "a_verdicts": a_verdicts, "a_unit_table": a_unit_table,
             "a_probes": src["v112_probes"], "roster": v["roster"], "t4_raw": src["t4_raw"], "t4_coded": t4_coded,
             "t4_probes": v["t4_probes"], "decision": Path(out_dir) / "_no_decision_file.json", "out": out_dir,
             "il_t1": v.get("il_t1") or "", "only_sens": None}
    S19.run_real(paths, n_perm or S19.N_PERM, gap_b or S19.GAP_B, guards=False)
    for name in ("v119_verdicts.json", "v119_not_run.json"):
        f = Path(out_dir) / name
        if f.exists():
            return json.loads(f.read_text(encoding="utf-8")), f
    raise Refused(f"score_v1_19 wrote no output in {out_dir}")


# --------------------------------------------------------------------------- Q4: v1.14's extractor (read-only check)
APOS_BRANDS = {"v20": "paula's choice", "v21": "l'oréal paris"}


def v114_check(t4_raw: list[dict], rank_table_path) -> dict:
    """Read-only (section 10.2 step 4, [OPEN]): t4 N3 S0 Phase B answers naming Paula's Choice / L'Oreal Paris only with
    a typographic apostrophe, and whether v1.14's Stage 1 rank table lists that brand for that answer."""
    if not rank_table_path or not Path(rank_table_path).exists():
        return {"status": "NOT CHECKED: v1.14 rank table not supplied"}
    listed = collections.defaultdict(set)
    ids = set()
    for r in A.read_csv_rows(rank_table_path):
        ids.add(r.get("answer_id"))
        listed[r.get("answer_id")].add(normalise(r.get("brand") or "").lower())
    hits = []
    for r in A.dedupe_calls(t4_raw):
        sub = r.get("substrate")
        if (sub not in APOS_BRANDS or r.get("phase") != "B" or r.get("condition") != "S0"
                or r.get("model_requested") not in A.T4_N3 or not A.is_answered(r)):
            continue
        t = r["text"].lower()
        name = APOS_BRANDS[sub]
        typo = [name.replace("'", ch) for ch in QUOTE_MAP]
        if any(x in t for x in typo) and name not in t:
            hits.append({"call_id": r["call_id"], "substrate": sub, "model": r["model_requested"],
                         "in_rank_table": r["call_id"] in ids, "brand_listed": name in listed.get(r["call_id"], set())})
    return {"status": "CHECKED (read-only; changes nothing)", "rank_table_sha256": sha256_file(rank_table_path),
            "answers_typographic_only": len(hits), "answers_in_rank_table": sum(h["in_rank_table"] for h in hits),
            "brand_listed_for_answer": sum(h["brand_listed"] for h in hits),
            "reading": "if answers_in_rank_table > brand_listed_for_answer, v1.14's extractor shares the miss",
            "answers": hits}


# --------------------------------------------------------------------------- step 6: guards
def deviations_guard(root: Path = ROOT, spec: dict | None = None) -> dict:
    """Q3: the S-Q entries are committed on v1.12 and v1.19 (their locked DEVIATIONS bytes an unchanged prefix)."""
    spec = spec or SQ_PINS["deviations"]
    out, ok = {}, True
    for name, s in spec.items():
        cur, locked = R3._git_show(root, s["ref"], s["path"]), R3._git_show(root, s["lock_tag"], s["path"])
        added = cur[len(locked):].decode("utf-8", "replace") if (cur is not None and locked is not None
                                                                 and cur.startswith(locked)) else ""
        has = bool(re.search(r"^##+ .*Entry", added, re.M)) and "S-Q" in added and "U+2019" in added
        out[name] = {"ref": s["ref"], "locked_prefix_unchanged": bool(cur is not None and locked is not None
                                                                      and cur.startswith(locked)),
                     "s_q_entry_found": has}
        ok = ok and out[name]["locked_prefix_unchanged"] and has
    return {"ok": ok, "entries": out}


def outputs_absent(out_dir: Path) -> list:
    return [n for n in OUTPUTS.values() if (Path(out_dir) / n).exists()]


def real_guards(root: Path = ROOT, out_dir: Path = OUT_DIR) -> dict:
    """Section 10.2 step 6 / 11.1: after the AIAS 3.0 lock, after the DEVIATIONS entries, once."""
    lock = R3.mq_lock(root)
    if not lock["ok"]:
        raise Refused("MQ_Lock (AIAS 3.0): " + "; ".join(lock["why"]))
    dev = deviations_guard(root)
    if not dev["ok"]:
        raise Refused(f"the S-Q DEVIATIONS entries are not committed on v1.12 and v1.19 first (section 10.2): {dev}")
    tag = A.coder_blob_at_tag()
    if not tag["match"] or not A.verify_coder()["match"]:
        raise Refused(f"v0.42 coder pin: {tag}, {A.verify_coder()}")
    sc = R3.check_scorer(root)
    if not sc["passed"]:
        raise Refused(f"the imported v1.12 scorer is not the locked file: {sc}")
    there = outputs_absent(out_dir)
    if there:
        raise Refused(f"S-Q outputs exist ({there}): S-Q is computed once and never overwritten")
    return {"MQ_Lock": lock, "deviations": dev, "coder_at_v042_tag": tag, "v112_scorer": sc}


def materialise_real(rd, pins: dict = P, sq: dict = SQ_PINS) -> dict:
    """Every input of the real run read with `git show` at its pinned commit into a scratch directory (logged)."""
    v112, v042, q45 = pins["v1.12"], pins["v0.42"], pins["v0.45_SQ"]
    an, v114, v119 = sq["v1.12_anchor"], sq["v1.14"], sq["v1.19"]
    src = {"v112_raw": rd.materialise(v112["ref"], v112["raw"], "v112"),
           "v112_probes": rd.materialise(v112["ref"], v112["probes"], "v112"),
           "v112_coded": rd.materialise_dir(v112["ref"], v112["coded_dir"], R3.V112_CODED_FILES, "v112_coded"),
           "v112_verdicts": rd.materialise(v112["ref"], v112["verdicts"], "v112"),
           "v112_unit_table": rd.materialise(v112["ref"], v112["unit_table"], "v112"),
           "p1": rd.materialise(an["ref"], an["p1"], "v112_anchor"),
           "brandfree": rd.materialise(an["ref"], an["brandfree"], "v112_anchor"),
           "profiles": rd.materialise(an["ref"], an["profiles"], "v112_profiles"),
           "h5_stage1": rd.materialise(v114["ref"], v114["stage1"], "v114"),
           "rank_table": rd.materialise(v114["ref"], v114["rank_table"], "v114"),
           "t4_raw": rd.materialise(v042["ref"], v042["raw"], "v042"),
           "t4": {"primary": {"coded": rd.materialise_dir(v042["ref"], v042["coded_dir"], R3.T4_CODED_FILES, "v042_coded"),
                              "brand_table": rd.materialise(v042["ref"], v042["brand_table"], "v042"),
                              "verdicts": rd.materialise(v042["ref"], v042["verdicts"], "v042")},
                  "SQ": {"coded": rd.materialise_dir(q45["ref"], q45["coded_dir"], R3.T4_CODED_FILES, "v045_coded"),
                         "brand_table": rd.materialise(q45["ref"], q45["brand_table"], "v045"),
                         "verdicts": rd.materialise(q45["ref"], q45["verdicts"], "v045")}},
           "require_p1": True}
    if sha256_file(src["t4"]["SQ"]["brand_table"]) != q45["brand_table_sha256"]:
        raise Refused("t4 S-Q brand table SHA-256 differs from the pin (section 10.2 step 2)")
    tree = rd.scratch / "v119_tree"
    s19 = tree / v119["scorer"]
    s19.parent.mkdir(parents=True, exist_ok=True)
    s19.write_bytes(rd.read(v119["ref"], v119["scorer"]))
    man = tree / pins["v1.12"]["manifest"]
    man.parent.mkdir(parents=True, exist_ok=True)
    man.write_bytes(rd.read(pins["v1.12"]["lock_tag"], pins["v1.12"]["manifest"]))
    listed = [ln.split()[0] for ln in rd.read(v119["lock_tag"], v119["manifest"]).decode("utf-8").splitlines()
              if ln.strip().endswith(v119["scorer"])]
    if not (sha256_file(s19) == v119["scorer_sha256"] and listed == [v119["scorer_sha256"]]):
        raise Refused("score_v1_19.py at the scored commit is not the file of v1.19's lock manifest")
    src["v119"] = {"scorer": s19, "roster": rd.materialise(v119["ref"], v119["roster"], "v119"),
                   "verdicts": rd.materialise(v119["ref"], v119["verdicts"], "v119"),
                   "t4_probes": rd.materialise(sq["v0.42_probes"]["ref"], sq["v0.42_probes"]["path"], "v042_probes"),
                   "il_t1": rd.materialise(v119["ref"], v119["il_t1"], "v119")}
    return src


# --------------------------------------------------------------------------- the pipeline (steps 1-7)
def write_jsonl(records: list[dict], path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in records), encoding="utf-8")
    return path


def sq_pipeline(src: dict, out_dir: Path, cfg=None, v119_draws: tuple | None = None, scratch: Path | None = None,
                guards: dict | None = None, log=print) -> dict:
    """Steps 1-7 on local copies of the inputs (src). Reproduction first: nothing is written to out_dir unless the
    locked coder and scorers reproduce the published v1.12 coding, verdicts and unit table and v1.19's verdicts."""
    out_dir = Path(out_dir)
    there = outputs_absent(out_dir)
    if there:
        raise Refused(f"S-Q outputs exist ({there}): S-Q is computed once and never overwritten")
    scratch = Path(scratch or tempfile.mkdtemp(prefix="v112_sq_"))
    cfg = cfg or A.Cfg()
    n19, gap19 = v119_draws or (None, None)
    raw = A.read_jsonl(src["v112_raw"])
    counts = {"raw_lines": apostrophe_counts(raw), "answers": answered_counts(raw)}
    C = A.load_coder()
    # step 5: reproduction
    rows_re, _calls = A.code_coverage(raw, C)
    pub_rows, pub_reg = A.read_coded(src["v112_coded"])
    d_code = mention_diffs(pub_rows, rows_re)
    reg = A.registry_from_coder(C)
    rep_dir = scratch / "reproduction"
    doc_re = score_v112(src, src["v112_raw"], src["v112_coded"], "primary", rep_dir / "v112_verdicts.json",
                        rep_dir / "v112_unit_table.csv", cfg)
    pub_doc = json.loads(Path(src["v112_verdicts"]).read_text(encoding="utf-8"))
    d_v112 = json_leaf_diff(pub_doc, doc_re)
    d_tab = csv_cell_diff(src["v112_unit_table"], rep_dir / "v112_unit_table.csv")
    rep = {"coded_cells_differ": d_code["n_cells_differ"], "registry_same": reg == pub_reg,
           "v112_verdict_leaves_differ": len(d_v112), "v112_unit_table_cells_differ": len(d_tab),
           "ignored_path_leaves": list(IGNORED_PATH_LEAVES), "examples": {"v112": d_v112[:10], "table": d_tab[:10],
                                                                          "coded": d_code["cells"][:10]}}
    S19 = None
    if src.get("v119"):
        S19 = load_v119(src["v119"]["scorer"])
        doc19_re, _f19 = run_v119(S19, src, src["v112_raw"], src["v112_coded"], src["v112_verdicts"],
                                  src["v112_unit_table"], src["t4"]["primary"]["coded"], rep_dir / "v119", n19, gap19)
        pub19 = json.loads(Path(src["v119"]["verdicts"]).read_text(encoding="utf-8"))
        d19 = json_leaf_diff(pub19, doc19_re)
        rep["v119_verdict_leaves_differ"] = len(d19)
        rep["examples"]["v119"] = d19[:10]
    else:
        rep["v119_verdict_leaves_differ"] = None
        rep["v119_status"] = "not run (no v1.19 inputs supplied: synthetic test)"
    bad = [k for k in ("coded_cells_differ", "v112_verdict_leaves_differ", "v112_unit_table_cells_differ",
                       "v119_verdict_leaves_differ") if rep.get(k)] + ([] if rep["registry_same"] else ["registry"])
    if bad:
        raise Refused(f"reproduction failed ({bad}): nothing written (section 10.2 step 5). "
                      f"{json.dumps(R3._jsonable(rep['examples']), ensure_ascii=False)[:2000]}")
    log(f"[S-Q] reproduction: 0 coded cells, 0 v1.12 leaves, 0 table cells"
        f"{', 0 v1.19 leaves' if S19 else ''} differ")
    # steps 1, 3: the text map and the coding
    mapped = normalise_records(raw)
    raw_sq = write_jsonl(mapped, scratch / "sq" / "v112_raw_SQ.jsonl")
    rows_sq, calls_sq = A.code_coverage(mapped, C)
    flips = mention_diffs(pub_rows, rows_sq)
    flips["answers_with_U2019_or_U2018"] = counts["answers"]
    flips["definition"] = "S-Q: U+2019/U+2018 -> U+0027 in the answer text, then v0.42's coder unchanged (10.2)"
    out_dir.mkdir(parents=True, exist_ok=True)
    coded_sq = out_dir / OUTPUTS["coded"]
    A.write_coded(rows_sq, reg, {"phase": "v1.12 S-Q (AIAS 3.0 pre-registration section 10.2)",
                                 "coder": A.verify_coder(), "coder_at_v042_tag": A.coder_blob_at_tag(),
                                 "raw_sha256": A.sha256_file(src["v112_raw"]), "raw_SQ_sha256": A.sha256_file(raw_sq),
                                 "calls_deduplicated": len(calls_sq), "mention_rows": len(rows_sq),
                                 "url_removal": True, "coded_utc": _now()}, coded_sq)
    # step 4: scoring on the S-Q tables (t4's S-Q comparators: both sides together)
    doc_sq = score_v112(src, raw_sq, coded_sq, "SQ", out_dir / OUTPUTS["v112_verdicts"],
                        out_dir / OUTPUTS["v112_unit_table"], cfg)
    comparison = {"v1_12": compare_v112(pub_doc, doc_sq)}
    if S19 is not None:
        doc19_sq, f19 = run_v119(S19, src, raw_sq, coded_sq, out_dir / OUTPUTS["v112_verdicts"],
                                 out_dir / OUTPUTS["v112_unit_table"], src["t4"]["SQ"]["coded"], scratch / "v119_sq",
                                 n19, gap19)
        shutil.copyfile(f19, out_dir / OUTPUTS["v119_verdicts"])
        comparison["v1_19"] = compare_v119(pub19, doc19_sq)
    comparison["all_labels_same"] = all(r["same_label"] for rows in comparison.values() if isinstance(rows, list)
                                        for r in rows)
    t4_raw = A.read_jsonl(src["t4_raw"])
    R3.write_json(out_dir / OUTPUTS["flips"], flips)
    rec = {"phase": "v1.12 / v1.19 sensitivity S-Q (AIAS 3.0 pre-registration section 10.2, D4)",
           "created_utc": _now(), "definition": {"map": {"U+2019": "U+0027", "U+2018": "U+0027"},
                                                "other_characters_mapped": "none"},
           "guards": guards, "reproduction": rep, "counts": counts,
           "flips_summary": {k: flips[k] for k in ("n_cells_differ", "by_direction", "by_substrate_brand_model")},
           "v114_extractor_check": v114_check(t4_raw, src.get("rank_table")),
           "comparison": comparison, "H7_note": "H7's legacy comparator is kept as published (no locked S-Q table of t3)",
           "outputs": {n: (A.sha256_file(out_dir / n) if (out_dir / n).is_file() else "directory")
                       for n in OUTPUTS.values() if (out_dir / n).exists()}}
    R3.write_json(out_dir / OUTPUTS["record"], rec)
    log(f"[S-Q] {flips['n_cells_differ']} cells differ {flips['by_direction']}; all labels same: "
        f"{comparison['all_labels_same']} -> {out_dir}")
    return rec


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="S-Q for v1.12 and v1.19 (AIAS 3.0 pre-registration section 10.2)")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--run", action="store_true", help="the real run (once; after the lock and the DEVIATIONS entries)")
    g.add_argument("--synthetic", metavar="SRC_JSON", help="a JSON map of local input paths (tests only)")
    ap.add_argument("--out", help="output directory (synthetic only; the real run writes beside this file)")
    ap.add_argument("--draws", type=int, help="permutation/bootstrap draws (synthetic only)")
    a = ap.parse_args(argv)
    try:
        A.load_coder()                      # first: the coder's HOME shim may re-execute this script (v1.12 N13)
        if a.run:
            if a.out or a.draws:
                raise Refused("--out and --draws are for synthetic runs only")
            g_rec = real_guards(ROOT, OUT_DIR)
            rd = R3.Reader(ROOT)
            src = materialise_real(rd)
            rec = sq_pipeline(src, OUT_DIR, guards=g_rec)
            rec["inputs_read"] = rd.log
            R3.write_json(OUT_DIR / OUTPUTS["record"], rec)
            return 0
        src = json.loads(Path(a.synthetic).read_text(encoding="utf-8"))
        if not a.out:
            raise Refused("--synthetic needs --out")
        if Path(a.out).resolve() == OUT_DIR.resolve():
            raise Refused("a synthetic run never writes into the real output folder")
        cfg = A.Cfg(a.draws, a.draws) if a.draws else A.Cfg()
        d19 = (a.draws, 3) if a.draws else None
        sq_pipeline(src, Path(a.out), cfg, d19, guards={"synthetic": True})
        return 0
    except Refused as e:
        print(f"[S-Q] REFUSED: {e}", file=sys.stderr)
        return 3
    except A.Halt as e:
        print(f"[S-Q] HALT: {e}", file=sys.stderr)
        return 4


if __name__ == "__main__":
    sys.exit(main())
