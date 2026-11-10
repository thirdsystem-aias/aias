#!/usr/bin/env python3
"""
v42_values.py -- the single place where the v0.42 (t4) paper, report and charts read numbers.

Every number printed by fill_paper_v0_42.py, reports/v42_t4_generation_content.py and scripts/build_charts_v42.py
comes from one of these machine outputs, never from a hand-typed literal:

  verdicts      osf/v42/v42_verdicts.json            (score_v0_42.py --run; synthetic: DIR/_score/v42_verdicts.json)
  table         osf/v42/v42_brand_table.csv          (same run; per-brand t3 and t4 values)
  v41           osf/v41/v41_verdicts.json            (locked at tag v0.41-scoring-locked; background numbers only)
  budget_state  osf/v42/data/t4_budget_state.json    (acquisition guard; approvals past the $80 / projection pauses;
                                                      absent when no approval was needed)
  budget_const  osf/v42/scripts/budget_v0_42.py      (locked constants: cap, pause, judge reserve)

Values.put() records, for every formatted value, the source, the JSON path (or table column), the raw value and the
formatting function, so tests can re-resolve each printed number (papers/v0_42/tests/test_fill_paper_v0_42.py).

Verdict cases (case_*) follow the pre-registration r2 (section 2): H_Gen_Presence and H_Gen_Phi resolve to CONFIRMED,
MARGINAL, FALSIFIED or UNDETERMINED (split here by cause: a model excluded under section 5.4, n below the floor of
H_Gen_Phi, or a degenerate statistic, scorer note N14); H_Search_Presence carries labels, not verdicts
(search-robust, search-sensitive, search-dominated; UNDETERMINED / NOT_COMPUTED when no interval exists).
"""
import csv
import json
import math
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]

EXPECTED_PREREG_TAG = "v0.42-prereg-r1"           # prereg header and section 9, C21 (tag name kept from r1)
SUBS = ["v0.19", "v0.20", "v0.21", "v0.22", "v0.23"]
CAT = {"v0.19": "audiophile headphones", "v0.20": "skincare", "v0.21": "cosmetics",
       "v0.22": "automotive", "v0.23": "premium spirits"}
CAT_SHORT = {"v0.19": "Headphones", "v0.20": "Skincare", "v0.21": "Cosmetics", "v0.22": "Automotive",
             "v0.23": "Spirits"}
N3 = ["claude-fable-5-2", "gpt-6-astra", "gemini-4-argon"]
L6 = ["claude-opus-4-5", "claude-sonnet-4-5", "gpt-4o", "gpt-4o-mini", "gemini-2.5-flash", "gemini-2.5-flash-lite"]
MODEL_NAME = {"claude-fable-5-2": "Claude Fable 5.2", "gpt-6-astra": "GPT-6 Astra", "gemini-4-argon": "Gemini 4 Argon",
              "claude-opus-4-5": "Claude Opus 4.5", "claude-sonnet-4-5": "Claude Sonnet 4.5", "gpt-4o": "GPT-4o",
              "gpt-4o-mini": "GPT-4o mini", "gemini-2.5-flash": "Gemini 2.5 Flash",
              "gemini-2.5-flash-lite": "Gemini 2.5 Flash-Lite"}
PROVIDERS = ["Anthropic", "OpenAI", "Google"]
PAIR_KEY = {"Anthropic": "Anthropic: legacy pair -> claude-fable-5-2", "OpenAI": "OpenAI: legacy pair -> gpt-6-astra",
            "Google": "Google: legacy pair -> gemini-4-argon"}
PAIR_LEGACY = {"Anthropic": "Claude Opus 4.5 + Claude Sonnet 4.5", "OpenAI": "GPT-4o + GPT-4o mini",
               "Google": "Gemini 2.5 Flash + Flash-Lite"}
PAIR_NEW = {"Anthropic": "claude-fable-5-2", "OpenAI": "gpt-6-astra", "Google": "gemini-4-argon"}
COND_NAME = {"S0": "search off", "S1": "search on"}
SYNTHETIC_MARK = "SYNTHETIC TEST — NOT RESULTS"

# Status words by register. Paper: the pre-registered verdicts and labels as the scorer writes them.
# Report (managerial, P1-P5): plain-language status, no hypothesis labels (CLAUDE.md, Two-register discipline).
PAPER_STATUS = {"CONFIRMED": "CONFIRMED", "MARGINAL": "MARGINAL", "FALSIFIED": "FALSIFIED",
                "UNDETERMINED_EXCLUDED": "UNDETERMINED", "UNDETERMINED_DEGENERATE": "UNDETERMINED",
                "UNDETERMINED_FLOOR": "UNDETERMINED", "ROBUST": "search-robust", "SENSITIVE": "search-sensitive",
                "DOMINATED": "search-dominated", "UNDETERMINED": "UNDETERMINED", "NOT_COMPUTED": "NOT COMPUTED",
                "DESCRIPTIVE": "descriptive"}
REPORT_STATUS = {"CONFIRMED": "SUPPORTED", "MARGINAL": "PARTLY SUPPORTED", "FALSIFIED": "NOT SUPPORTED",
                 "UNDETERMINED_EXCLUDED": "NOT DECIDED", "UNDETERMINED_DEGENERATE": "NOT DECIDED",
                 "UNDETERMINED_FLOOR": "NOT DECIDED", "ROBUST": "HELD WITH SEARCH ON",
                 "SENSITIVE": "PARTLY CHANGED BY SEARCH", "DOMINATED": "RESHAPED BY SEARCH",
                 "UNDETERMINED": "NOT DECIDED", "NOT_COMPUTED": "NOT DECIDED", "DESCRIPTIVE": "OBSERVED"}
REPORT_STATUS_CLASS = {"SUPPORTED": "positive", "HELD WITH SEARCH ON": "positive", "PARTLY SUPPORTED": "neutral",
                       "PARTLY CHANGED BY SEARCH": "neutral", "NOT DECIDED": "neutral", "OBSERVED": "neutral",
                       "NOT SUPPORTED": "negative", "RESHAPED BY SEARCH": "negative"}


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


FORMATS = {f.__name__: f for f in (r3, r2, sr3, p4, pct0, pct1, i0, usd2, usd2_plain, f1)}


# --------------------------------------------------------------------------- derived values (named; tests recompute)
def d_sum(*xs):
    return float(sum(float(x) for x in xs))


def d_min(*xs):
    return float(min(float(x) for x in xs))


def d_max(*xs):
    return float(max(float(x) for x in xs))


def d_add(a, b):
    return float(a) + float(b)


def d_ratio(a, b):
    return float(a) / float(b) if float(b) else float("nan")


def d_diff(a, b):
    return float(a) - float(b)


def d_count_ge(thr, *xs):
    return float(sum(1 for x in xs if x is not None and float(x) >= float(thr)))


DERIVE = {f.__name__: f for f in (d_sum, d_min, d_max, d_add, d_ratio, d_diff, d_count_ge)}


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
def budget_constants():
    """Locked guard constants, read from osf/v42/scripts/budget_v0_42.py (not re-typed)."""
    sys.path.insert(0, str(ROOT / "osf/v42/scripts"))
    import budget_v0_42 as BG  # noqa: E402
    return {"cap_usd": float(BG.BUDGET_CAP_USD), "pause_usd": float(BG.PAUSE_AT_USD),
            "judge_reserve_usd": float(BG.JUDGE_RESERVE_USD)}


def load_sources(verdicts_path, table_path=None, v41_path=None, budget_state_path=None):
    src = {"verdicts": json.load(open(verdicts_path, encoding="utf-8"))}
    if table_path:
        src["table"] = {"rows": list(csv.DictReader(open(table_path, newline="", encoding="utf-8")))}
    v41_path = Path(v41_path) if v41_path else ROOT / "osf/v41/v41_verdicts.json"
    src["v41"] = json.load(open(v41_path, encoding="utf-8"))
    bs = Path(budget_state_path) if budget_state_path else None
    src["budget_state"] = json.load(open(bs, encoding="utf-8")) if bs and bs.exists() else {"approvals": {}}
    src["budget_state_present"] = bool(bs and bs.exists())
    src["budget_const"] = budget_constants()
    return src


def is_synthetic(V):
    return (V.get("manipulation_checks", {}).get("MC_Parity", {}) or {}).get("detail") == "SKIPPED_SYNTHETIC"


# --------------------------------------------------------------------------- verdict cases
def case_gen(V):
    h = V["verdicts"]["H_Gen_Presence"]
    v = h.get("verdict")
    if v in ("CONFIRMED", "MARGINAL", "FALSIFIED"):
        return v
    return "UNDETERMINED_EXCLUDED" if h.get("reason") else "UNDETERMINED_DEGENERATE"


def case_phi(V):
    h = V["verdicts"]["H_Gen_Phi"]
    v = h.get("verdict")
    if v in ("CONFIRMED", "MARGINAL", "FALSIFIED"):
        return v
    if h.get("reason"):
        return "UNDETERMINED_EXCLUDED"
    if h.get("n") is not None and h["n"] < 40:          # section 2.4: UNDETERMINED if n < 40
        return "UNDETERMINED_FLOOR"
    return "UNDETERMINED_DEGENERATE"


def case_search(V):
    h = V["verdicts"]["H_Search_Presence"]
    if h.get("status") == "NOT_COMPUTED":
        return "NOT_COMPUTED"
    return {"search-robust": "ROBUST", "search-sensitive": "SENSITIVE",
            "search-dominated": "DOMINATED"}.get(h.get("label"), "UNDETERMINED")


def verdict_word(case):
    return case.split("_")[0]


def excluded_models(V, cond):
    out = []
    for k in V.get("models_excluded_condition") or []:
        m, c = k.split("|")
        if c == cond:
            out.append(m)
    return out


def names(models):
    ns = [MODEL_NAME.get(m, m) for m in models]
    if len(ns) <= 1:
        return "".join(ns)
    return ", ".join(ns[:-1]) + " and " + ns[-1]


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
