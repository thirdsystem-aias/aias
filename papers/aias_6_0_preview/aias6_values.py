#!/usr/bin/env python3
"""
aias6_values.py -- the single place where the AIAS 6.0 Preview paper (and its charts) reads numbers.

Every number printed by fill_paper_aias6.py and scripts/build_charts_aias6.py comes from the locked scorer's outputs
(osf/aias_6_0_preview/scripts/score_aias_6_0_preview.py --run, tag aias-6-0-preview-prereg-r1), never from a typed
literal:

  results   osf/aias_6_0_preview/outputs/results_aias_6_0_preview.json
  gates     osf/aias_6_0_preview/outputs/gates_aias_6_0_preview.json
  inputs    osf/aias_6_0_preview/outputs/inputs_read_aias_6_0_preview.json  (git ref, blob and SHA-256 of every input)
  profile   osf/aias_6_0_preview/outputs/profile_aias_6_0_preview.csv       (D4; per unit)
  components (to name a MARGINAL leg, section 4.2): the component files the scorer read, extracted with `git show`
            from the refs in results.refs into outputs/components/ (stage1_v1_14.json, v112_verdicts.json,
            v1_13_verdicts.json); each must have the SHA-256 that inputs_read records, else the fill refuses.

Values.put() records the source, the JSON path, the raw value and the format of every printed value
(tests/test_fill_paper_aias6.py re-resolves them). Verdict and state words are the scorer's, verbatim.
"""
import csv
import hashlib
import json
import math
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUTDIR = ROOT / "osf/aias_6_0_preview/outputs"
EXPECTED_PREREG_TAG = "aias-6-0-preview-prereg-r1"
ORDER = ["P", "C", "R", "S", "Cov", "G"]
NAME = {"P": "Presence", "C": "Consistency", "R": "Ranking", "S": "Sentiment", "Cov": "Coverage", "G": "Grounding"}
SYM = {"P": "$P$", "C": "$C^*$", "R": "$R^*$", "S": "$S$", "Cov": "Cov\\*", "G": "$G^*$"}
SUBS = ["v0.19", "v0.20", "v0.21", "v0.22", "v0.23"]
CAT = {"v0.19": "Headphones", "v0.20": "Skincare", "v0.21": "Cosmetics", "v0.22": "Automotive", "v0.23": "Spirits"}
NUMWORD = {0: "no", 1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six"}
STATE_WORD = {"PASS": "PASS", "PASS_RETEST_PENDING": "PASS, retest pending", "PASS_AI_JUDGED": "PASS, AI-judged",
              "MARGINAL": "MARGINAL", "FAIL": "FAIL", "UNDETERMINED": "UNDETERMINED", "NOT_RUN": "NOT RUN"}
STATE_PHRASE = {"NOT_RUN": "pending", "MARGINAL": "under review", "FAIL": "not passed",
                "UNDETERMINED": "not determined"}           # A_k wording (section 6.6) and the 4.2 label column
COMPONENT_FILES = {"v1.14": "stage1_v1_14.json", "v1.12": "v112_verdicts.json", "v1.13": "v1_13_verdicts.json"}
COMPONENT_PATHS = {"v1.14": "osf/methodology/v1_14/outputs/stage1/stage1_v1_14.json",
                   "v1.12": "osf/methodology/v1_12/v112_verdicts.json",
                   "v1.13": "osf/methodology/v1_13/v1_13_verdicts.json"}
SYNTHETIC_MARK = "SYNTHETIC TEST — NOT RESULTS"
NAMES = {"results": "results_aias_6_0_preview.json", "gates": "gates_aias_6_0_preview.json",
         "inputs": "inputs_read_aias_6_0_preview.json", "profile": "profile_aias_6_0_preview.csv"}


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


def i0(x):
    return f"{int(round(float(x))):,}"


def f1(x):
    return f"{float(x):.1f}"


def sf1(x):
    s = f"{float(x):+.1f}"
    return "0.0" if s in ("+0.0", "-0.0") else s.replace("-", "−")


FORMATS = {f.__name__: f for f in (r3, r2, sr3, p4, pct0, i0, f1, sf1)}


def d_len(x):
    return float(len(x))


def d_abs(x):
    return abs(float(x))


DERIVE = {f.__name__: f for f in (d_len, d_abs)}


class Values:
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

    def derive(self, name, fn, refs, fmt):
        raws = [jget(self.src[s], p) for s, p in refs]
        raw = fn(*raws)
        s = fmt(raw)
        self.vals[name] = s
        self.prov[name] = {"kind": "derived", "fn": fn.__name__, "consts": [],
                           "refs": [[s_, list(p)] for s_, p in refs], "raw": raw, "fmt": fmt.__name__, "formatted": s}
        return s

    def word(self, name, text, basis, numbers=()):
        """Text chosen from the data; `numbers` lists the put()/derive() names whose values it contains."""
        self.vals[name] = text
        self.prov[name] = {"kind": "text", "basis": basis, "formatted": text, "numbers": list(numbers)}
        return text

    def table(self, name, md, cells):
        self.vals[name] = md
        self.prov[name] = {"kind": "table", "formatted": md,
                           "cells": [{"formatted": f, "source": s, "path": list(p), "fmt": fm} for f, s, p, fm in cells]}
        return md


def sha256(b):
    return hashlib.sha256(b).hexdigest()


def load_sources(outputs_dir):
    d = Path(outputs_dir)
    src = {}
    for k in ("results", "gates", "inputs"):
        p = d / NAMES[k]
        if not p.exists():
            raise Missing(f"{p} not found")
        src[k] = json.loads(p.read_text(encoding="utf-8"))
    p = d / NAMES["profile"]
    src["profile"] = {"rows": list(csv.DictReader(p.read_text(encoding="utf-8").splitlines())) if p.exists() else []}
    comp, comp_sha = {}, {}
    for name, fn in COMPONENT_FILES.items():
        q = d / "components" / fn
        if q.exists():
            b = q.read_bytes()
            comp[name] = json.loads(b.decode("utf-8"))
            comp_sha[name] = sha256(b)
    src["components"] = comp
    src["_component_sha256"] = comp_sha
    return src


def is_synthetic(src):
    return any(isinstance(src.get(k), dict) and "synthetic_fixture" in src[k] for k in ("results", "gates", "inputs")) \
        or (src["results"].get("MQ_Lock") or {}).get("ok") is not True


def components_verified(src):
    """Each extracted component file has the SHA-256 the scorer logged when it read it (inputs_read)."""
    log = src["inputs"].get("inputs_read") or {}
    refs = src["results"].get("refs") or {}
    bad = []
    for name, sh in src["_component_sha256"].items():
        ref = (refs.get(name) or {}).get("ref")
        rec = (log.get(f"{ref}:{COMPONENT_PATHS[name]}") or {}).get("sha256")
        if rec != sh:
            bad.append(f"{name}: {sh} vs logged {rec}")
    return bad


def marginal_legs(src, part):
    """The legs a MARGINAL component's own record names MARGINAL (section 4.2 label: 'the marginal leg named')."""
    out = []
    if part == "R" and "v1.14" in src["components"]:
        s1 = src["components"]["v1.14"]
        for k, v in s1.items():
            if k.startswith("H") and isinstance(v, dict) and v.get("verdict") == "MARGINAL":
                out.append((k, v.get("rho"), v.get("n"), ["components", "v1.14", k]))
    elif part == "Cov" and "v1.12" in src["components"]:
        for k, v in ((src["components"]["v1.12"].get("paper_A_verdict") or {}).get("legs") or {}).items():
            if v == "MARGINAL":
                out.append((k, None, None, ["components", "v1.12", "paper_A_verdict", "legs", k]))
    elif part == "G" and "v1.13" in src["components"]:
        for k, v in (src["components"]["v1.13"].get("verdicts") or {}).items():
            if v == "MARGINAL":
                out.append((k, None, None, ["components", "v1.13", "verdicts", k]))
    return out


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
    return [t.rstrip(".,") for t in _NUM.findall(text)]
