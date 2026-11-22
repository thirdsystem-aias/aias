#!/usr/bin/env python3
"""
v120_values.py -- the single place where Sentiment Paper A (v1.11 study, scored under its pre-registered successor
rule v1.20; case B) reads numbers, for the paper and the charts. Forked from papers/v1_11/v111_values.py (pre-data
pipeline, branch v1.11-paper); the formats, Values class and verdict cases are unchanged.

Every number printed by fill_paper_v1_20.py and scripts/build_charts_v120.py comes from one of these machine
outputs, never from a hand-typed literal:

  verdicts    osf/methodology/v1_20/outputs/v1_20_verdicts.json            score_v1_20.py --stage C
  stage_j     osf/methodology/v1_20/outputs/stage_j_v1_20.json             score_v1_20.py --stage J
  comparison  osf/methodology/v1_20/outputs/comparison_v1_11_v1_20.json    score_v1_20.py --stage J and C
  frozen      osf/methodology/v1_11/outputs/judge_outputs_frozen_v1_11.json   judge_v1_11.py --freeze
  plan        osf/methodology/v1_11/data/plan_v1_11.json                   judge_v1_11.py (binding projection)
  run         papers/v1_20/run_values_v1_20.json                           make_run_values_v1_20.py (call-record
              metadata: status, finish reason, tokens, run window; SHA-256 of the raw file checked against frozen)
  v111_log    osf/methodology/v1_11/outputs/stage_j_run_v1_11.log           v1.11's own Stage J console record (halt)

Values.put() records, for every formatted value, the source, the JSON path, the raw value and the formatting
function, so the tests can re-resolve each printed number (tests/test_fill_paper_v1_11.py).

Verdict words are the scorer's, verbatim: CONFIRMED, MARGINAL, FALSIFIED, UNDETERMINED for H1-H9, and PENDING or
INACTIVE for H5 (score_v1_11.h5_status). The case_* functions only split those words by cause (which template
sentence explains them); they never re-decide.
"""
import json
import math
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DESIGN = ROOT / "osf/methodology/v1_20"
OUTDIR = DESIGN / "outputs"
V111 = ROOT / "osf/methodology/v1_11"

EXPECTED_PREREG_TAG = "v1.20-prereg-r1"
V111_TAG = "v1.11-prereg-r1"
WAVES = ["t1", "t2", "t3"]
SUBS = ["v0.19", "v0.20", "v0.21", "v0.22", "v0.23"]
CAT = {"v0.19": "audiophile headphones", "v0.20": "skincare", "v0.21": "cosmetics",
       "v0.22": "automotive", "v0.23": "premium spirits"}
CAT_SHORT = {"v0.19": "Headphones", "v0.20": "Skincare", "v0.21": "Cosmetics", "v0.22": "Automotive",
             "v0.23": "Spirits"}
EARLY = ["pm", "finance", "oliveoil", "running", "skincare", "household", "knives", "premium_tea"]
EARLY_SHORT = {"pm": "PM software", "finance": "Finance apps", "oliveoil": "Olive oil", "running": "Running shoes",
               "skincare": "Facial skincare", "household": "Household retail", "knives": "Kitchen knives",
               "premium_tea": "Premium tea"}
J1_NAME, J2_NAME = "Claude Opus 5.5", "GPT-6.1 Sol"
JUDGE_NAME = {"claude-opus-5-5": J1_NAME, "gpt-6.1-sol": J2_NAME, "gemini-4-argon": "Gemini 4 Argon"}
HYPS = ["H1_Judge_Agreement", "H2_Sep_Presence", "H3_Sep_Consistency", "H4_Stability_Short", "H5_Sep_Ranking",
        "H6_Stability_Long", "H7_Naming_Frequency", "H8_Recognition_Sep", "H9_Self_Preference"]
SHORT = {h: h.split("_")[0] for h in HYPS}
TIER = {"H1": "Primary (gate)", "H2": "Primary", "H3": "Primary", "H4": "Primary", "H5": "Primary",
        "H6": "Secondary", "H7": "Secondary", "H8": "Secondary", "H9": "Secondary"}
SEP_HYPS = ["H2_Sep_Presence", "H3_Sep_Consistency", "H5_Sep_Ranking", "H8_Recognition_Sep"]
STAB_HYPS = ["H4_Stability_Short", "H6_Stability_Long"]
NOISE_GUARDED = ("H2", "H3", "H5", "H7", "H8")
SYNTHETIC_MARK = "SYNTHETIC TEST — NOT RESULTS"
VERDICT_WORDS = ("CONFIRMED", "MARGINAL", "FALSIFIED", "UNDETERMINED", "PENDING", "INACTIVE")


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
    return "0.000" if s in ("+0.000", "-0.000") else s.replace("-", "−")


def p4(x):
    return f"{float(x):.4f}"


def pct0(x):
    return f"{100 * float(x):.0f}%"


def pct2(x):
    return f"{100 * float(x):.2f}%"


def pct1(x):
    return f"{100 * float(x):.1f}%"


def i0(x):
    return f"{int(round(float(x))):,}"


def usd2(x):
    return f"US\\${float(x):,.2f}"


def sci1(x):
    """e.g. 4.8e-05 -> $4.8 \\times 10^{-5}$"""
    m, e = f"{float(x):.1e}".split("e")
    return f"${m} \\times 10^{{{int(e)}}}$"


def f1(x):
    return f"{float(x):.1f}"


def sf1(x):
    s = f"{float(x):+.1f}"
    return "0.0" if s in ("+0.0", "-0.0") else s.replace("-", "−")


def sf2(x):
    s = f"{float(x):+.2f}"
    return "0.00" if s in ("+0.00", "-0.00") else s.replace("-", "−")


def sr4(x):
    s = f"{float(x):+.4f}"
    return "0.0000" if s in ("+0.0000", "-0.0000") else s.replace("-", "−")


FORMATS = {f.__name__: f for f in (r3, r2, sr3, p4, pct0, pct1, pct2, i0, usd2, f1, sf1, sf2, sr4)}


# --------------------------------------------------------------------------- derived values (named; tests recompute)
def d_sum(*xs):
    return float(sum(float(x) for x in xs))


def d_min(*xs):
    return float(min(float(x) for x in xs))


def d_max(*xs):
    return float(max(float(x) for x in xs))


def d_abs(x):
    return abs(float(x))


def d_len(x):
    return float(len(x))


def d_add(a, b):
    return float(a) + float(b)


def d_ratio(a, b):
    return float(a) / float(b) if float(b) else float("nan")


def d_sub(a, b):
    return float(a) - float(b)


def d_count(*xs):
    return float(len(xs))


def d_signed(signs, *xs):
    """sum of sign * value; the signs are recorded as constants in the provenance."""
    return float(sum(s * float(x) for s, x in zip(signs, xs)))


DERIVE = {f.__name__: f for f in (d_sum, d_min, d_max, d_abs, d_len, d_add, d_ratio, d_sub, d_count, d_signed)}


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
NAMES = {"verdicts": "v1_20_verdicts.json", "stage_j": "stage_j_v1_20.json",
         "comparison": "comparison_v1_11_v1_20.json", "frozen": "judge_outputs_frozen_v1_11.json",
         "plan": "plan_v1_11.json", "run": "run_values_v1_20.json", "cutlist": "cut_units_v1_20.json",
         "xcheck": "v1_9_cross_check_v1_20.json"}
V111_LOG = V111 / "outputs/stage_j_run_v1_11.log"


def source_path(outputs_dir, k):
    """v1.20's three outputs sit in outputs_dir; v1.11's frozen record in osf/methodology/v1_11/outputs/, its plan in
    osf/methodology/v1_11/data/; the run values beside this module."""
    d = Path(outputs_dir)
    p = d / NAMES[k]
    if p.exists():
        return p
    return {"frozen": V111 / "outputs", "plan": V111 / "data", "run": HERE, "xcheck": HERE,
            "cutlist": DESIGN / "scoping"}.get(k, d) / NAMES[k]


def load_sources(outputs_dir):
    src = {}
    for k in NAMES:
        p = source_path(outputs_dir, k)
        if not p.exists():
            raise Missing(f"{p} not found")
        src[k] = json.loads(p.read_text(encoding="utf-8"))
    return src


def v111_halt_log():
    """v1.11's own Stage J console record: the halt line and the exit code, as written."""
    txt = V111_LOG.read_text(encoding="utf-8")
    halt = [ln for ln in txt.splitlines() if "HALT" in ln]
    exitc = [ln.split("=", 1)[1] for ln in txt.splitlines() if ln.startswith("EXIT=")]
    started = [ln.split(":", 1)[1].strip() for ln in txt.splitlines() if ln.startswith("started_utc")]
    return {"halt_line": halt[0] if halt else None, "exit": exitc[0] if exitc else None,
            "started_utc": started[0] if started else None}


def sha256(path):
    import hashlib
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def is_synthetic(src):
    """The scorer marks its dry runs (dry_run: true); the scenario generator adds synthetic_fixture."""
    return any(bool(src[k].get("dry_run")) or "synthetic_fixture" in src[k] for k in src if isinstance(src[k], dict))


# --------------------------------------------------------------------------- verdict cases (cause of each word)
def guard_on(V):
    return bool(V.get("noise_guard_applied"))


def case_h1(V):
    v = V["VERDICTS"]["H1"]
    if v not in ("CONFIRMED", "MARGINAL", "FALSIFIED", "UNDETERMINED"):
        raise ValueError(f"H1: unknown verdict {v!r}")
    return v


def case_sep(V, h):
    """H2, H3, H5, H8: three-wave rule; UNDETERMINED by the noise guard or by fewer than two determined waves."""
    s = SHORT[h]
    v = V["VERDICTS"][s]
    if v in ("PENDING", "INACTIVE"):
        if s != "H5":
            raise ValueError(f"{h}: {v} is only possible for H5")
        return v
    if v in ("CONFIRMED", "MARGINAL", "FALSIFIED"):
        return v
    if v != "UNDETERMINED":
        raise ValueError(f"{h}: unknown verdict {v!r}")
    if guard_on(V) and s in NOISE_GUARDED and V["verdicts_before_noise_guard"][s] != "UNDETERMINED":
        return "UNDETERMINED_GUARD"
    return "UNDETERMINED_WAVES"


def case_stab(V, h):
    s = SHORT[h]
    v = V["VERDICTS"][s]
    if v in ("CONFIRMED", "MARGINAL", "UNDETERMINED"):
        return v
    if v != "FALSIFIED":
        raise ValueError(f"{h}: unknown verdict {v!r}")
    leg = V[h]
    return "FALSIFIED_RHO" if leg["rho"] < 0.30 else "FALSIFIED_P"


def case_h7(V):
    v = V["VERDICTS"]["H7"]
    if v in ("CONFIRMED", "MARGINAL", "FALSIFIED"):
        return v
    if v != "UNDETERMINED":
        raise ValueError(f"H7: unknown verdict {v!r}")
    if guard_on(V) and V["verdicts_before_noise_guard"]["H7"] != "UNDETERMINED":
        return "UNDETERMINED_GUARD"
    return "UNDETERMINED_FLOOR"


def case_h9(V):
    v = V["VERDICTS"]["H9"]
    if v not in ("CONFIRMED", "MARGINAL", "FALSIFIED", "UNDETERMINED"):
        raise ValueError(f"H9: unknown verdict {v!r}")
    return v


def case_overall(V):
    """Which Discussion opening applies (a reading of the scorer's words, never a new verdict)."""
    W = V["VERDICTS"]
    if W["H1"] == "FALSIFIED":
        return "INSTRUMENT_FAILED"
    if W["H4"] == "FALSIFIED":
        return "UNSTABLE"
    if W["H1"] == "UNDETERMINED":
        return "INSTRUMENT_UNDETERMINED"
    gate = [W["H2"], W["H3"]] + ([W["H5"]] if W["H5"] not in ("PENDING", "INACTIVE") else [])
    if any(w == "FALSIFIED" for w in gate):
        return "NOT_SEPARABLE"
    if all(w == "CONFIRMED" for w in gate) and W["H4"] == "CONFIRMED":
        return "SEPARABLE_FLAGGED" if W["H1"] == "MARGINAL" else "SEPARABLE"
    return "MIXED"


def joinand(xs):
    xs = list(xs)
    if len(xs) <= 1:
        return "".join(xs)
    return ", ".join(xs[:-1]) + " and " + xs[-1]


def git_tag_commit(tag=EXPECTED_PREREG_TAG, root=ROOT):
    r = subprocess.run(["git", "-C", str(root), "rev-parse", "-q", "--verify", f"refs/tags/{tag}^{{commit}}"],
                       capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else None


_NUM = re.compile(r"\d+(?:[.,]\d+)*")


def numeric_tokens(text):
    """Digit groups (decimals and thousands separators kept together), trailing separators dropped."""
    return [t.rstrip(".,") for t in _NUM.findall(text)]
