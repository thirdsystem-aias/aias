#!/usr/bin/env python3
"""
quotes_v0_45.py -- AIAS(TM) v0.45, DEVIATIONS Entry 2 (ex ante, 2026-11-25, written before any t5 call):
pre-specified sensitivity S-Q, "typographic quotes normalised". NOT part of the locked pipeline: the locked
coding (code_t5_v0_45.py -> v0.42's coder) and the locked scorer (score_v0_45.py) stay primary and decide every
verdict. This file adds a second, separately reported run. It imports the locked modules unchanged and changes no
locked file.

Why. v0.42's certified coder matches registry names that contain a straight apostrophe (U+0027: "Paula's Choice",
"L'Oréal Paris") literally, so an answer that writes the same name with a right single quotation mark (U+2019,
"Paula’s Choice") is coded "not named". At t4 this missed 46 Phase B brand-answer cells (all 0 -> 1 under S-Q).

Definition of S-Q (exactly):
  1. Text map. In the answer text (the raw record's "text" field) of every call of both waves (t4 and t5), U+2019
     RIGHT SINGLE QUOTATION MARK and U+2018 LEFT SINGLE QUOTATION MARK are replaced by U+0027 APOSTROPHE. No other
     character is changed (QUOTE_MAP).
  2. Coding. v0.42's coder (osf/v42/scripts/code_t4_v0_42.py, imported unchanged; its git blob is checked against
     the pin 2d36735d... by code_t5_v0_45.coder_blob_ok) codes the mapped text exactly as the primary run does:
     C.code_calls(calls, probes, strip=True): URL removal before Phase B matching, Phase B mentions for all five
     substrates, Phase A yes/no parsing for v0.19-v0.22. v0.23 Phase A recognition labels come from an LLM judge
     and are NOT re-requested: S-Q copies the primary run's v0.23 Phase A rows unchanged (and score_v0_45 applies
     the J1 t4 codes exactly as in the primary run). S-Q makes no model call.
  3. Scoring. score_v0_45.score(), unchanged, on the S-Q tables of both waves with the primary run's settings
     (seeds, draws, panels, drop rule, J1 record, carried Ranking verdict, component files). Gate G3 compares the
     S-Q t4 values with the S-Q t4 brand table (v0.42's scorer on the S-Q t4 tables, written by --t4-correction),
     because v0.42's published table holds the primary coding.
  4. Reporting. Beside every primary statistic and verdict: the S-Q value and verdict and whether the label is the
     same (comparison_SQ.json). Verdict rules unchanged; S-Q never replaces a primary verdict; a test whose label
     differs is reported as "coding-sensitive". Also reported: the cells that differ (wave, substrate, brand,
     model, condition) and the number of answers holding U+2019/U+2018.

Modes (no model API is called in any mode):
  --t4-correction T4DIR OUTDIR [--v42-verdicts F --v42-brand-table F]
        T4DIR holds t4_raw.jsonl and coded/ (v0.42's locked tables; published scorer files default to T4DIR/..).
        First reproduces the locked Phase B table and v0.42's published verdicts and brand table from the primary
        tables (refuses on any difference), then writes OUTDIR/coded (S-Q tables), flips_t4_SQ.json,
        v42_verdicts_SQ.json, v42_brand_table_SQ.csv, t4_correction_diff_SQ.json. OUTDIR must not exist.
  --t5 --t4-dir D --t4-sq-dir Q --j1 F [--ranking-stage2 R] [--component NAME=T4CSV,T5CSV,GATE ...]
        Only after score_v0_45.py --run has written osf/v45/v45_verdicts.json (the primary run) and with the same
        inputs: S-Q of both waves -> osf/v45/sensitivity/out/ (refuses before the primary run or if out/ exists).
"""
import argparse
import collections
import csv
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
V45_SCRIPTS = HERE.parent / "scripts"
sys.path.insert(0, str(V45_SCRIPTS))
import code_t5_v0_45 as K     # noqa: E402  (imports v0.42's coder unchanged and bootstraps ROOT)

C = K.C
ROOT = K.ROOT
QUOTE_MAP = {"’": "'", "‘": "'"}
_TABLE = str.maketrans(QUOTE_MAP)
PRIMARY_VERDICTS = ROOT / "osf/v45/v45_verdicts.json"
SQ_OUT = ROOT / "osf/v45/sensitivity/out"
T4_PROBES = ROOT / "osf/v42/prereg/probes_v0_42.jsonl"
STAT_KEYS = ("panel", "n", "rho", "p_perm", "p_exact", "SR", "D", "delta", "verdict")
V42_GATES = {"passed": True, "enforce": False, "detail": {"P1": True, "P2": True, "P3": True}}


class Refused(RuntimeError):
    pass


# --------------------------------------------------------------------------- S-Q coding
def normalise(text):
    return text.translate(_TABLE) if isinstance(text, str) else text


def normalise_calls(calls):
    """Copies of the call records with the answer text mapped; the inputs are not modified."""
    return [dict(r, text=normalise(r["text"])) if isinstance(r.get("text"), str) else dict(r) for r in calls]


def curly_counts(calls):
    """Answered calls whose text holds U+2019 or U+2018, by substrate and phase."""
    c = collections.Counter()
    for r in calls:
        if C.is_answered(r) and any(ch in r["text"] for ch in QUOTE_MAP):
            c[f"{C.SUB_MAP[r['substrate']]}|phase_{r['phase']}"] += 1
    return dict(sorted(c.items()))


def check_coder():
    ok, blob = K.coder_blob_ok()
    if not ok:
        raise Refused(f"v0.42 coder blob {blob} != pin {K.CODER_BLOB_PIN}")


def code_sq(calls, probes, primary_A):
    """S-Q tables (A, B) for deduped calls: the locked coder on mapped text (judge OFF) + the primary v0.23 Phase A
    rows, copied."""
    check_coder()
    A, B = C.code_calls(normalise_calls(calls), probes, strip=True, judge_client=None)
    A = [r for r in A if r["substrate"] != "v0.23"] + [dict(r) for r in primary_A if r["substrate"] == "v0.23"]
    return A, B


def roundtrip(A, B, d):
    """Write the tables in v0.42's format and read them back (the scorer always reads written tables)."""
    C.write_tables(A, B, d)
    return C.read_tables(d)


def cell_diffs(Ap, Bp, As, Bs):
    """Cells whose code differs between the primary (p) and S-Q (s) tables."""
    out = []
    for ph, P, Q, key, val in (("B", Bp, Bs, lambda r: (r["call_id"], r["brand"]), "mentioned"),
                               ("A", Ap, As, lambda r: (r["call_id"],), "label")):
        p, q = {key(r): r for r in P}, {key(r): r for r in Q}
        for k in sorted(set(p) | set(q)):
            x, y = p.get(k), q.get(k)
            vx, vy = (x or {}).get(val), (y or {}).get(val)
            if str(vx) != str(vy):
                r = x or y
                out.append({"phase": ph, "call_id": r["call_id"], "substrate": r["substrate"], "brand": r["brand"],
                            "model": r["model"], "condition": r["condition"], "run": r["run"],
                            "frame_id": r.get("frame_id"), "primary": vx, "SQ": vy})
    cnt = collections.Counter(f"{d['phase']}|{d['substrate']}|{d['brand']}|{d['model']}|{d['condition']}" for d in out)
    return {"n_cells_differ": len(out),
            "by_direction": dict(collections.Counter(f"{d['primary']}->{d['SQ']}" for d in out)),
            "by_cell": dict(sorted(cnt.items(), key=lambda kv: (-kv[1], kv[0]))), "cells": out}


# --------------------------------------------------------------------------- comparisons
def _leaves(o, p=""):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from _leaves(v, f"{p}.{k}")
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from _leaves(v, f"{p}[{i}]")
    else:
        yield p, o


def json_diff(a, b, tol=1e-12):
    la, lb = dict(_leaves(a)), dict(_leaves(b))
    out = []
    for k in sorted(set(la) | set(lb)):
        x, y = la.get(k, "<absent>"), lb.get(k, "<absent>")
        if isinstance(x, float) and isinstance(y, float) and (abs(x - y) <= tol or (x != x and y != y)):
            continue
        if x != y:
            out.append([k, x, y])
    return out


def csv_diff(pa, pb, keys=("substrate", "brand")):
    A = {tuple(r[k] for k in keys): r for r in csv.DictReader(open(pa, newline="", encoding="utf-8"))}
    B = {tuple(r[k] for k in keys): r for r in csv.DictReader(open(pb, newline="", encoding="utf-8"))}
    out = []
    for k in sorted(set(A) | set(B)):
        if k not in A or k not in B:
            out.append([list(k), "<row>", k in A, k in B])
            continue
        for c in A[k]:
            if A[k][c] != B[k].get(c):
                out.append([list(k), c, A[k][c], B[k].get(c)])
    return out


def compare(primary, sq):
    """Primary vs S-Q, test by test (statistics, verdict, same label?) and part by part."""
    rows = []
    for name, p in primary.get("verdicts", {}).items():
        q = sq.get("verdicts", {}).get(name, {})
        same = p.get("verdict") == q.get("verdict")
        rows.append({"test": name, "primary": {k: p[k] for k in STAT_KEYS if k in p},
                     "SQ": {k: q[k] for k in STAT_KEYS if k in q}, "same_verdict": same,
                     "flag": "" if same else "coding-sensitive"})
    parts = {n: {"primary": v.get("verdict", v.get("verdict_from")),
                 "SQ": sq.get("parts", {}).get(n, {}).get("verdict", sq.get("parts", {}).get(n, {}).get("verdict_from"))}
             for n, v in primary.get("parts", {}).items()}
    pa = primary.get("verdicts", {}).get("H_Stab_Presence", {}).get("P_alongside", {})
    qa = sq.get("verdicts", {}).get("H_Stab_Presence", {}).get("P_alongside", {})
    return {"sensitivity": "S-Q (U+2019/U+2018 -> U+0027 before coding; DEVIATIONS Entry 2)", "tests": rows,
            "parts": parts, "P_alongside_rho": {"primary": pa.get("rho"), "SQ": qa.get("rho")},
            "all_verdicts_same": all(r["same_verdict"] for r in rows)}


# --------------------------------------------------------------------------- modes
def t4_correction(t4_dir, out_dir, v42_verdicts=None, v42_brand_table=None, cfg=None):
    import score_v0_42 as S
    t4_dir, out_dir = Path(t4_dir), Path(out_dir)
    if out_dir.exists():
        raise Refused(f"{out_dir} exists; S-Q outputs are written once, never overwritten")
    v42_verdicts = Path(v42_verdicts or t4_dir.parent / "v42_verdicts.json")
    v42_brand_table = Path(v42_brand_table or t4_dir.parent / "v42_brand_table.csv")
    cfg = cfg or S.Cfg()
    raw = C.read_raw(t4_dir / "t4_raw.jsonl")
    calls = C.dedupe_calls(raw)
    probes = C.load_probe_map(T4_PROBES)
    A0, B0 = C.read_tables(t4_dir / "coded")
    check_coder()
    Ar, Br = C.code_calls(calls, probes, strip=True)          # the locked coder, unmapped, judge OFF
    rep = cell_diffs([r for r in A0 if r["substrate"] != "v0.23"], B0, Ar, Br)
    if rep["n_cells_differ"]:
        raise Refused(f"the locked coder does not reproduce the locked t4 tables ({rep['n_cells_differ']} cells)")
    As, Bs = roundtrip(*code_sq(calls, probes, A0), out_dir / "coded")
    flips = cell_diffs(A0, B0, As, Bs)
    flips["answers_with_U2019_or_U2018"] = curly_counts(calls)
    flips["definition"] = "S-Q: U+2019/U+2018 -> U+0027 in the answer text, then v0.42's coder unchanged"
    (out_dir / "flips_t4_SQ.json").write_text(json.dumps(flips, indent=1, ensure_ascii=False), encoding="utf-8")
    t3 = S.load_t3_table()
    tmp = out_dir / "_primary_rerun"
    out_p, rows_p = S.score_t4(raw, A0, B0, t3, cfg, V42_GATES)
    S.write_outputs(out_p, rows_p, tmp / "v42_verdicts.json", tmp / "v42_brand_table.csv")
    dv = json_diff(json.load(open(v42_verdicts, encoding="utf-8")), json.load(open(tmp / "v42_verdicts.json", encoding="utf-8")))
    dt = csv_diff(v42_brand_table, tmp / "v42_brand_table.csv")
    if dv or dt:
        raise Refused(f"published v0.42 outputs not reproduced from the primary tables: {len(dv)} verdict leaves, "
                      f"{len(dt)} table cells differ ({tmp})")
    out_s, rows_s = S.score_t4(raw, As, Bs, t3, cfg, V42_GATES)
    S.write_outputs(out_s, rows_s, out_dir / "v42_verdicts_SQ.json", out_dir / "v42_brand_table_SQ.csv")
    pub = json.load(open(v42_verdicts, encoding="utf-8"))
    sq = json.load(open(out_dir / "v42_verdicts_SQ.json", encoding="utf-8"))
    summary = {"reproduced_published": {"verdict_leaves_differ": 0, "brand_table_cells_differ": 0},
               "verdicts": {k: {"primary": pub["verdicts"][k].get("verdict", pub["verdicts"][k].get("label")),
                                "SQ": sq["verdicts"][k].get("verdict", sq["verdicts"][k].get("label")),
                                "rho_primary": pub["verdicts"][k].get("rho"), "rho_SQ": sq["verdicts"][k].get("rho")}
                            for k in pub["verdicts"]},
               "verdict_leaves_differ": json_diff(pub, sq),
               "brand_table_cells_differ": csv_diff(v42_brand_table, out_dir / "v42_brand_table_SQ.csv")}
    (out_dir / "t4_correction_diff_SQ.json").write_text(json.dumps(summary, indent=1, ensure_ascii=False), encoding="utf-8")
    for f in tmp.iterdir():
        f.unlink()
    tmp.rmdir()
    return flips, summary


def run_sq(t4, t4_sq, t5_raw, t5_A, t5_B, probes5, cfg, extras, coded_dir):
    """S-Q scoring of both waves. t4 = (raw, A, B) primary; t4_sq = (A, B) S-Q; t5_raw = the raw lines as read
    (the scorer gets them as in the primary run; coding uses the deduped calls). Returns (out, rows, t5 diffs)."""
    import score_v0_45 as SC
    t5_calls = C.dedupe_calls(t5_raw)
    A5s, B5s = roundtrip(*code_sq(t5_calls, probes5, t5_A), coded_dir)
    out, rows = SC.score((t4[0], *t4_sq), (t5_raw, A5s, B5s), cfg, extras)
    d5 = cell_diffs(t5_A, t5_B, A5s, B5s)
    d5["answers_with_U2019_or_U2018"] = curly_counts(t5_calls)
    return out, rows, d5


def t5_main(a):
    import score_v0_45 as SC
    S = SC.S
    if not PRIMARY_VERDICTS.exists():
        raise Refused(f"primary run first: {PRIMARY_VERDICTS} does not exist")
    if SQ_OUT.exists():
        raise Refused(f"{SQ_OUT} exists; S-Q is run once")
    t4_dir, q = Path(a.t4_dir), Path(a.t4_sq_dir)
    raw4 = C.read_raw(t4_dir / "t4_raw.jsonl")
    A4, B4 = C.read_tables(t4_dir / "coded")
    A4s, B4s = C.read_tables(q / "coded")
    chk = cell_diffs(A4s, B4s, *code_sq(C.dedupe_calls(raw4), C.load_probe_map(T4_PROBES), A4))
    if chk["n_cells_differ"]:
        raise Refused(f"{q}/coded is not the S-Q coding of {t4_dir} ({chk['n_cells_differ']} cells)")
    j1 = json.load(open(a.j1, encoding="utf-8"))
    comps = {}
    for spec in a.component:
        name, rest = spec.split("=", 1)
        comps[name] = tuple(rest.split(","))
    extras = {"t4_brand_table": q / "v42_brand_table_SQ.csv", "j1": j1, "ranking_stage2": a.ranking_stage2,
              "components": comps, "v23_t4_successor": j1.get("t4_codes") if j1.get("verdict", {}).get("pass") else None}
    raw5 = C.read_raw(K.REAL_RAW)
    A5, B5 = C.read_tables(K.DEFAULT_OUT)
    SQ_OUT.mkdir(parents=True)
    out, rows, d5 = run_sq((raw4, A4, B4), (A4s, B4s), raw5, A5, B5, C.load_probe_map(K.PROBES_PATH),
                           S.Cfg(), extras, SQ_OUT / "coded_t5")
    S.write_outputs(out, rows, SQ_OUT / "v45_verdicts_SQ.json", SQ_OUT / "v45_unit_table_SQ.csv")
    (SQ_OUT / "flips_t5_SQ.json").write_text(json.dumps(d5, indent=1, ensure_ascii=False), encoding="utf-8")
    cmp_ = compare(json.load(open(PRIMARY_VERDICTS, encoding="utf-8")),
                   json.load(open(SQ_OUT / "v45_verdicts_SQ.json", encoding="utf-8")))
    (SQ_OUT / "comparison_SQ.json").write_text(json.dumps(cmp_, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"S-Q -> {SQ_OUT}: t5 cells differ {d5['n_cells_differ']}; all verdicts same: {cmp_['all_verdicts_same']}")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="AIAS v0.45 sensitivity S-Q (quotes normalised; DEVIATIONS Entry 2)")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--t4-correction", nargs=2, metavar=("T4DIR", "OUTDIR"))
    g.add_argument("--t5", action="store_true")
    ap.add_argument("--v42-verdicts")
    ap.add_argument("--v42-brand-table")
    ap.add_argument("--t4-dir")
    ap.add_argument("--t4-sq-dir")
    ap.add_argument("--j1")
    ap.add_argument("--ranking-stage2")
    ap.add_argument("--component", action="append", default=[])
    a = ap.parse_args(argv)
    try:
        if a.t4_correction:
            flips, summ = t4_correction(*a.t4_correction, a.v42_verdicts, a.v42_brand_table)
            print(f"t4 S-Q: {flips['n_cells_differ']} cells differ {flips['by_direction']}; verdicts {summ['verdicts']}")
            return 0
        if not (a.t4_dir and a.t4_sq_dir and a.j1):
            ap.error("--t5 needs --t4-dir, --t4-sq-dir and --j1")
        return t5_main(a)
    except Refused as e:
        print(f"[v45 S-Q] REFUSED: {e}", file=sys.stderr)
        return 3


if __name__ == "__main__":
    sys.exit(main())
