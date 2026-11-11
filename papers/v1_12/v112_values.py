#!/usr/bin/env python3
"""
v112_values.py -- the single place where the v1.12 Coverage Paper A (paper and charts) reads numbers.

Every number printed by fill_paper_v1_12.py and scripts/build_charts_v112.py comes from one of these machine outputs,
never from a hand-typed literal:

  verdicts   osf/methodology/v1_12/v112_verdicts.json   (score_v1_12.py --run; synthetic: tests/fixtures/SYNTHETIC_*)
  table      osf/methodology/v1_12/v112_unit_table.csv  (same run; one row per brand unit)
  n1         osf/methodology/v1_12/prereg/calibration_N1_v1_12.json   (calibration N1, locked at v1.12-prereg-r1)

Values.put() records, for every formatted value, the source, the JSON path, the raw value and the formatting
function, so the tests can re-resolve each printed number (papers/v1_12/tests/test_fill_paper_v1_12.py).

Verdict words are the scorer's, verbatim: CONFIRMED, MARGINAL, FALSIFIED, UNDETERMINED, INACTIVE for the legs
(score_v1_12.VERDICTS) and PASS, FAIL, MARGINAL, UNDETERMINED, INSTRUMENT FAIL for Paper A (score_v1_12.gate).
The case_* functions only split those words by cause (which template sentence explains them); they never re-decide.
"""
import csv
import json
import math
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DESIGN = ROOT / "osf/methodology/v1_12"

EXPECTED_PREREG_TAG = "v1.12-prereg-r1"
SUBS = ["v0.19", "v0.20", "v0.21", "v0.22", "v0.23"]
CAT = {"v0.19": "audiophile headphones", "v0.20": "skincare", "v0.21": "cosmetics",
       "v0.22": "automotive", "v0.23": "premium spirits"}
CAT_SHORT = {"v0.19": "Headphones", "v0.20": "Skincare", "v0.21": "Cosmetics", "v0.22": "Automotive",
             "v0.23": "Spirits"}
FABLE, OPUS, GPT6, GEM4 = "claude-fable-5-2", "claude-opus-5-5", "gpt-6-astra", "gemini-4-argon"
MODELS4 = [FABLE, OPUS, GPT6, GEM4]
MODEL_NAME = {FABLE: "Claude Fable 5.2", OPUS: "Claude Opus 5.5", GPT6: "GPT-6 Astra", GEM4: "Gemini 4 Argon"}
W_TYPES = ["why", "when", "where", "while", "with whom", "with what", "how feeling"]
GATE_LEGS = ["H1_Sep_Presence", "H2_Sep_Consistency", "H3_Sep_NamingRate", "H4_Reliability"]
COND_LEGS = ["H5_Sep_Ranking", "H6_Sep_Sentiment"]
SEC_LEGS = ["H7_Sep_Presence_Legacy", "H8_Panel_Replication"]
ALL_LEGS = GATE_LEGS + COND_LEGS + SEC_LEGS
LEG_SHORT = {h: h.split("_")[0] for h in ALL_LEGS}
LEG_AGAINST = {"H1_Sep_Presence": "Presence $P_{N3}$", "H2_Sep_Consistency": "Consistency $C^*_{N3}$",
               "H3_Sep_NamingRate": "naming rate $\\pi_{\\text{cov}}$", "H4_Reliability": "the other CEP half",
               "H5_Sep_Ranking": "Ranking $R^*_{S0}$", "H6_Sep_Sentiment": "Sentiment $S$",
               "H7_Sep_Presence_Legacy": "published Presence, $t_3$",
               "H8_Panel_Replication": "Cov* on panel C3"}
SYNTHETIC_MARK = "SYNTHETIC TEST — NOT RESULTS"
SENS = [("S1_raw_Cov_k2", "S1 raw Cov ($k = 2$)"), ("S2_floor_6", "S2 floor 6"), ("S2_floor_28", "S2 floor 28"),
        ("S3_equal_weight_null", "S3 equal-weight null"), ("S4_room_to_vary", "S4 room to vary"),
        ("S8_mid_p", "S8 mid-$p$ $\\beta$"), ("S9_uncentred_rho_w", "S9 uncentred $\\rho_w$"),
        ("S10_without_Denon", "S10 without Denon")]


class Missing(KeyError):
    pass


def jget(obj, path):
    cur = obj
    for part in path:
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        elif isinstance(cur, list) and isinstance(part, int) and -len(cur) <= part < len(cur):
            cur = cur[part]
        else:
            raise Missing("/".join(map(str, path)))
    return cur


def has(obj, path):
    try:
        v = jget(obj, path)
    except Missing:
        return False
    return v is not None and not (isinstance(v, float) and not math.isfinite(v))


# --------------------------------------------------------------------------- formats (named; tests re-apply them)
def r3(x):
    s = f"{float(x):.3f}"
    return "0.000" if s == "-0.000" else s


def r2(x):
    s = f"{float(x):.2f}"
    return "0.00" if s == "-0.00" else s


def sr3(x):
    s = f"{float(x):+.3f}"
    return "0.000" if s in ("+0.000", "-0.000") else s


def r4s(x):
    s = f"{float(x):.4f}"
    return "0.0000" if s == "-0.0000" else s


def p4(x):
    return f"{float(x):.4f}"


def pct0(x):
    return f"{100 * float(x):.0f}%"


def pct1(x):
    return f"{100 * float(x):.1f}%"


def i0(x):
    return f"{int(round(float(x))):,}"


def usd2(x):
    return f"\\${float(x):,.2f}"


def usd2_plain(x):
    return f"${float(x):,.2f}"


def f1(x):
    return f"{float(x):.1f}"


FORMATS = {f.__name__: f for f in (r4s, r3, r2, sr3, p4, pct0, pct1, i0, usd2, usd2_plain, f1)}


# --------------------------------------------------------------------------- derived values (named; tests recompute)
def d_sum(*xs):
    return float(sum(float(x) for x in xs))


def d_min(*xs):
    return float(min(float(x) for x in xs))


def d_max(*xs):
    return float(max(float(x) for x in xs))


def d_mean(*xs):
    return float(sum(float(x) for x in xs)) / len(xs)


def d_add(a, b):
    return float(a) + float(b)


def d_ratio(a, b):
    return float(a) / float(b) if float(b) else float("nan")


def d_diff(a, b):
    return float(a) - float(b)


def d_count_ge(thr, *xs):
    return float(sum(1 for x in xs if x is not None and float(x) >= float(thr)))


DERIVE = {f.__name__: f for f in (d_mean, d_sum, d_min, d_max, d_add, d_ratio, d_diff, d_count_ge)}


class Values:
    """Formatted values with provenance: put() for one JSON leaf, derive() for a named function of leaves,
    word() for text chosen from the data, table() for a markdown table whose every number is listed."""

    def __init__(self, sources):
        self.src = sources
        self.vals = {}
        self.prov = {}

    def raw(self, src, path):
        return jget(self.src[src], path)

    def put(self, name, src, path, fmt):
        raw = jget(self.src[src], path)
        if raw is None or (isinstance(raw, float) and not math.isfinite(raw)):
            raise Missing(f"{src}:{'/'.join(map(str, path))} is null")
        s = fmt(raw)
        self.vals[name] = s
        self.prov[name] = {"kind": "json", "source": src, "path": list(path), "raw": raw, "fmt": fmt.__name__,
                           "formatted": s}
        return s

    def derive(self, name, fn, refs, fmt, consts=()):
        raws = [jget(self.src[s], p) for s, p in refs]
        raw = fn(*consts, *raws)
        s = fmt(raw)
        self.vals[name] = s
        self.prov[name] = {"kind": "derived", "fn": fn.__name__, "consts": list(consts),
                           "refs": [[s_, list(p)] for s_, p in refs], "raw": raw, "fmt": fmt.__name__, "formatted": s}
        return s

    def word(self, name, text, basis):
        self.vals[name] = text
        self.prov[name] = {"kind": "text", "basis": basis, "formatted": text}
        return text

    def table(self, name, md, cells):
        self.vals[name] = md
        self.prov[name] = {"kind": "table", "formatted": md,
                           "cells": [{"formatted": f, "source": s, "path": list(p), "fmt": fm}
                                     for f, s, p, fm in cells]}
        return md


# --------------------------------------------------------------------------- loading
def load_sources(verdicts_path, table_path=None, n1_path=None):
    src = {"verdicts": json.loads(Path(verdicts_path).read_text(encoding="utf-8"))}
    rows = list(csv.DictReader(Path(table_path).read_text(encoding="utf-8").splitlines())) if table_path else []
    src["table"] = {"rows": rows}
    n1_path = Path(n1_path) if n1_path else DESIGN / "prereg/calibration_N1_v1_12.json"
    src["n1"] = json.loads(Path(n1_path).read_text(encoding="utf-8"))
    return src


def is_synthetic(V):
    """The real run (score_v1_12.py --run) requires parity gate P1 to have passed; the synthetic mode skips it."""
    p1 = ((V.get("parity_gates") or {}).get("P1") or {})
    return p1.get("passed") is not True or "synthetic_fixture" in V


# --------------------------------------------------------------------------- verdict cases (cause of each word)
def case_gate(V):
    g = V["paper_A_verdict"]
    v = g["verdict"]
    notes = " ".join(g.get("notes") or [])
    if v == "INSTRUMENT FAIL":
        return "INSTRUMENT_FAIL"
    if v == "MARGINAL" and "downgraded to MARGINAL" in notes:
        return "MARGINAL_H7"
    if v == "MARGINAL" and "two-model panel" in notes and all(
            g["legs"].get(h) == "CONFIRMED" for h in g["legs"]):
        return "MARGINAL_TWO_MODEL"
    if v in ("PASS", "FAIL", "MARGINAL", "UNDETERMINED"):
        return v
    raise ValueError(f"unknown Paper A verdict {v!r}")


def case_leg(V, h):
    leg = V["legs"][h]
    v = leg["verdict"]
    if v in ("CONFIRMED", "MARGINAL", "FALSIFIED", "INACTIVE"):
        return v
    if v != "UNDETERMINED":
        raise ValueError(f"{h}: unknown verdict {v!r}")
    if leg.get("reason"):
        return "UNDETERMINED_REASON"
    if leg.get("below_n_floor"):
        return "UNDETERMINED_FLOOR"
    return "UNDETERMINED_DEGENERATE"


def case_h5(V):
    leg = V["legs"]["H5_Sep_Ranking"]
    if leg["verdict"] == "INACTIVE":
        return "INACTIVE"
    src = V.get("H5_ranking_source") or {}
    if leg.get("reason") or src.get("status") == "NOT_AVAILABLE":
        return "UNAVAILABLE"
    return "GATING" if src.get("h5_gates") else "REPORTED"


def case_h6(V):
    return "INACTIVE" if V["legs"]["H6_Sep_Sentiment"]["verdict"] == "INACTIVE" else "ACTIVE"


def verdict_word(case):
    return {"INSTRUMENT_FAIL": "INSTRUMENT FAIL", "MARGINAL_H7": "MARGINAL", "MARGINAL_TWO_MODEL": "MARGINAL"}.get(
        case, case.split("_")[0])


def names(models):
    ns = [MODEL_NAME.get(m, m) for m in models]
    if len(ns) <= 1:
        return "".join(ns)
    return ", ".join(ns[:-1]) + " and " + ns[-1]


def joinand(xs):
    xs = list(xs)
    if len(xs) <= 1:
        return "".join(xs)
    return ", ".join(xs[:-1]) + " and " + xs[-1]


def git_tag_commit(tag=EXPECTED_PREREG_TAG, root=ROOT):
    r = subprocess.run(["git", "-C", str(root), "rev-parse", "-q", "--verify", f"refs/tags/{tag}^{{commit}}"],
                       capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else None


def fnum(s):
    return None if s in ("", None) else float(s)


_NUM = re.compile(r"\d+(?:[.,]\d+)*")


def numeric_tokens(text):
    """Digit groups (decimals and thousands separators kept together), trailing separators dropped."""
    return [t.rstrip(".,") for t in _NUM.findall(text)]
