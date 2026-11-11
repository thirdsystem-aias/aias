#!/usr/bin/env python3
"""
v043_values.py -- the single place where the v0.43 Stage 1 paper (fill and charts) reads numbers.

Every number printed by fill_paper_v0_43.py and scripts/build_charts_v043.py comes from one of these machine
outputs, never from a hand-typed literal:

  verdicts  osf/v43/v43_stage1_verdicts.json      written by `score_v0_43.py --stage 1` (the only file Stage 1 writes)
  pulls     a summary of osf/v43/data/trends_raw/main{1,2,3}/*.json (fetched_utc, status, n_attempts of each stored
            request; read-only), made by pull_summary() below
  repo      the lock records: tag v0.43-prereg-r1, osf/v43/anchor/osf_anchor_v0_43.json, anchor/DEVIATIONS.md,
            prereg/LOCK_MANIFEST_v0_43.sha256

Values.put() records, for every formatted value, the source, the JSON path, the raw value and the formatting function,
so the tests can re-resolve each printed number (papers/v0_43/tests/test_fill_paper_v0_43.py).

Verdict words and labels are the scorer's, verbatim (score_v0_43.verdict: CONFIRMED, MARGINAL, FALSIFIED, UNDETERMINED;
label REVERSED; flags "criterion doubtful", "outcome unreliable", "mostly plain search terms"). case_test() only splits
UNDETERMINED by its cause (which template sentence explains it); it never re-decides. check_consistency() re-derives
every verdict, label and flag with the locked scorer's own functions (imported read-only) and recomputes each test's
rho from the scorer's unit table; the fill refuses on any difference.
"""
import datetime as dt
import glob
import hashlib
import json
import math
import os
import re
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True          # never leave __pycache__ beside the locked scripts
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
V43 = ROOT / "osf/v43"
SCRIPTS = V43 / "scripts"
sys.path.insert(0, str(SCRIPTS))
import numpy as np  # noqa: E402
import score_v0_43 as SC  # noqa: E402  (locked scorer, read-only: its verdict rule, specs and rho_pw)

EXPECTED_PREREG_TAG = "v0.43-prereg-r1"
EXPECTED_PREREG_FIELD = "PRE_REGISTRATION_v0_43.md (tag v0.43-prereg-r1)"
EXPECTED_COMMIT = "8c96d9cf8ead60105589269db69df398a2b8c329"
LOCK_UTC = "2026-11-11T06:31"            # tagger date 2026-11-11T00:31:14-06:00
LOCK_RECORD_PHRASE = "2026-11-11 00:31 CT"
STEPS = ["main1", "main2", "main3"]
REQUESTS_PER_PULL = 28
N_UNITS = 112
B_REAL = 10000
SUBS = list(SC.SUBSTRATES)
CAT = {"v0.19": "audiophile headphones", "v0.20": "skincare", "v0.21": "cosmetics",
       "v0.22": "automotive", "v0.23": "premium spirits"}
CAT_SHORT = {"v0.19": "Headphones", "v0.20": "Skincare", "v0.21": "Cosmetics", "v0.22": "Automotive",
             "v0.23": "Spirits"}
TESTS = ["H_Pred_Presence", "H_Pred_Presence_SA", "H_Pred_Presence_Momentum", "H_Pred_Consistency"]
SHORT = {"H_Pred_Presence": "PRES", "H_Pred_Presence_SA": "SA", "H_Pred_Presence_Momentum": "MOM",
         "H_Pred_Consistency": "CONS"}
PRESENCE_TESTS = TESTS[:3]
FLAG_WORDS = ["criterion doubtful", "outcome unreliable", "mostly plain search terms"]
SYNTHETIC_MARK = "SYNTHETIC TEST — NOT RESULTS"
DESC_ROWS = [  # (label, path under descriptives, prereg item)
    ("No defunct automotive brands: H_Pred_Presence", ["presence_without_defunct_automotive", "H_Pred_Presence"], 2),
    ("No defunct automotive brands: H_Pred_Presence_SA", ["presence_without_defunct_automotive", "H_Pred_Presence_SA"], 2),
    ("No defunct automotive brands: H_Pred_Presence_Momentum", ["presence_without_defunct_automotive", "H_Pred_Presence_Momentum"], 2),
    ("Recall alone ($\\hat\\pi$ in place of $P$)", ["recall_alone"], 3),
    ("Units searched by topic only", ["topic_only_primary"], 4),
    ("Longer lead ($P$ at $t_1$, May 2026)", ["longer_lead_P_t1"], 5),
]


class Missing(KeyError):
    pass


class Inconsistent(ValueError):
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


def finite(v):
    return v is not None and not (isinstance(v, float) and not math.isfinite(v))


def has(obj, path):
    try:
        v = jget(obj, path)
    except Missing:
        return False
    return finite(v)


# --------------------------------------------------------------------------- formats (named; tests re-apply them)
def r3(x):
    s = f"{float(x):.3f}"
    return "0.000" if s == "-0.000" else s


def r2(x):
    s = f"{float(x):.2f}"
    return "0.00" if s == "-0.00" else s


def p4(x):
    return f"{float(x):.4f}"


def pct0(x):
    return f"{100 * float(x):.0f}%"


def pct1(x):
    return f"{100 * float(x):.1f}%"


def i0(x):
    return f"{int(round(float(x))):,}"


def utc_min(x):
    """ISO time -> 'YYYY-MM-DD HH:MM' (UTC)."""
    t = dt.datetime.fromisoformat(str(x).replace("Z", "+00:00"))
    if t.tzinfo is not None:
        t = t.astimezone(dt.timezone.utc)
    return t.strftime("%Y-%m-%d %H:%M")


def f1(x):
    return f"{float(x):.1f}"


FORMATS = {f.__name__: f for f in (r3, r2, p4, pct0, pct1, i0, utc_min, f1)}


# --------------------------------------------------------------------------- derived values (named; tests recompute)
def d_sum(*xs):
    return float(sum(float(x) for x in xs))


def d_min(*xs):
    return float(min(float(x) for x in xs))


def d_max(*xs):
    return float(max(float(x) for x in xs))


def d_diff(a, b):
    return float(a) - float(b)


def d_hours(a, b):
    """Hours from ISO time a to ISO time b."""
    ta = dt.datetime.fromisoformat(str(a).replace("Z", "+00:00"))
    tb = dt.datetime.fromisoformat(str(b).replace("Z", "+00:00"))
    return (tb - ta).total_seconds() / 3600.0


DERIVE = {f.__name__: f for f in (d_sum, d_min, d_max, d_diff, d_hours)}


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
        if not finite(raw):
            raise Missing(f"{src}:{'/'.join(map(str, path))} is null")
        s = fmt(raw)
        self.vals[name] = s
        self.prov[name] = {"kind": "json", "source": src, "path": list(path), "raw": raw, "fmt": fmt.__name__,
                           "formatted": s}
        return s

    def derive(self, name, fn, refs, fmt, consts=()):
        raws = [jget(self.src[s], p) for s, p in refs]
        if not all(finite(r) for r in raws):
            raise Missing(f"{name}: a referenced value is null")
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
def load_sources(verdicts_path, pulls):
    """pulls: a dict (pull_summary output) or a path to a JSON file holding one."""
    src = {"verdicts": json.loads(Path(verdicts_path).read_text(encoding="utf-8"))}
    if isinstance(pulls, (str, Path)):
        pulls = json.loads(Path(pulls).read_text(encoding="utf-8"))
    src["pulls"] = pulls
    return src


def is_synthetic(V):
    return "synthetic_fixture" in V


def pull_summary(raw_dir):
    """Read-only summary of the stored Stage 1 requests (acquire_trends_v0_43.py records): per pull, the number of
    stored request records, how many are ok or missing, re-sends, and the first and last fetched_utc."""
    out = {"raw_dir": str(raw_dir), "steps": {}}
    for step in STEPS:
        files = sorted(glob.glob(os.path.join(str(raw_dir), step, "*_b*.json")))
        if not files:
            continue
        times, ok, missing, resent = [], 0, 0, 0
        for fn in files:
            with open(fn, encoding="utf-8") as fh:
                rec = json.load(fh)
            times.append(rec["fetched_utc"])
            ok += rec["status"] == "ok"
            missing += rec["status"] != "ok"
            resent += int(rec["n_attempts"]) - 1
        ts = sorted(times, key=lambda s: dt.datetime.fromisoformat(s.replace("Z", "+00:00")))
        out["steps"][step] = {"records": len(files), "ok": ok, "missing": missing, "resent": resent,
                              "first_utc": ts[0], "last_utc": ts[-1]}
    return out


# --------------------------------------------------------------------------- verdict cases (cause of each word)
def case_test(T):
    """CONFIRMED / MARGINAL / FALSIFIED / UNDETERMINED (thresholds not met) / UNDETERMINED_N (below the minimum n) /
    UNDETERMINED_RHO (statistic undefined). Splits only the scorer's own UNDETERMINED by its recorded reason."""
    v = T["verdict"]
    if v in ("CONFIRMED", "MARGINAL", "FALSIFIED"):
        return v
    if v != "UNDETERMINED":
        raise Inconsistent(f"unknown verdict {v!r}")
    r = T.get("reason") or ""
    if r.startswith("n="):
        return "UNDETERMINED_N"
    if r:
        return "UNDETERMINED_RHO"
    return "UNDETERMINED"


def reversed_label(T):
    labels = T.get("labels") or []
    bad = [x for x in labels if x != "REVERSED"]
    if bad:
        raise Inconsistent(f"unknown label(s) {bad}")
    return "REVERSED" in labels


def joinand(xs):
    xs = list(xs)
    if len(xs) <= 1:
        return "".join(xs)
    return ", ".join(xs[:-1]) + " and " + xs[-1]


# --------------------------------------------------------------------------- consistency with the locked scorer
def _rows_from_unit_table(V):
    return [dict(r) for r in V["unit_table"]]


def recompute_rho(V, spec, rows=None):
    """rho_pw|Z from the scorer's unit table with the scorer's own rho_pw (strata with >= 2 complete rows, as run_stat).
    Returns (rho, n, residuals): residuals = list of (substrate, ry, rx) arrays for the charts."""
    rows = rows if rows is not None else _rows_from_unit_table(V)
    need = [spec[0], spec[1]] + list(spec[2])
    rows = [r for r in rows if all(finite(r.get(k)) for k in need)]
    strata, subs = [], []
    for s in SUBS:
        rs = [r for r in rows if r["sub"] == s]
        if len(rs) >= 2:
            strata.append({k: np.array([r[k] for r in rs], float) for k in need})
            subs.append(s)
    if len(rows) < 3 or not strata:
        return None, len(rows), []
    rho, ry, rx = SC.rho_pw(strata, spec)
    return rho, len(rows), list(zip(subs, ry, rx))


def _close(a, b, tol=1e-9):
    if not finite(a) and not finite(b):
        return True
    return finite(a) and finite(b) and abs(float(a) - float(b)) <= tol


def check_consistency(V, real):
    """Raise Inconsistent if the verdicts disagree with the locked scorer's rules or with themselves."""
    probs = []
    specs = {name: (spec, seed, min_n) for name, spec, seed, min_n, _ in SC.test_specs(1)}
    if V.get("stage") != 1:
        probs.append(f"stage {V.get('stage')!r} is not 1")
    if V.get("prereg") != EXPECTED_PREREG_FIELD:
        probs.append(f"prereg field {V.get('prereg')!r}")
    if set((V.get("tests") or {})) != set(TESTS):
        probs.append(f"tests {sorted((V.get('tests') or {}))} are not the four Stage 1 tests")
        raise Inconsistent("; ".join(probs))
    ut = V.get("unit_table") or []
    if real and len(ut) != N_UNITS:
        probs.append(f"unit table has {len(ut)} rows, not {N_UNITS}")
    mc = V["manipulation_checks"]
    # --- manipulation checks and flags (score_v0_43.score)
    c = mc["MC_Concurrent"]
    conc_ok = bool(c.get("rho") is not None and finite(c.get("rho")) and c["rho"] >= 0.30 and c.get("p_one", 1) < 0.05)
    if bool(c.get("pass_")) != conc_ok:
        probs.append("MC_Concurrent pass_ does not follow its rule")
    if finite(c.get("rho")):
        r_c, _, _ = recompute_rho(V, ("P", "Lc", []), [dict(r, Lc=r["L"]) for r in ut])
        if not _close(r_c, c["rho"]):
            probs.append(f"MC_Concurrent rho {c['rho']} != {r_c} recomputed from the unit table")
    rel = mc["MC_PullReliability"]
    m = rel.get("mean_pairwise_pooled_spearman")
    rel_ok = bool(m is not None and m >= 0.70)
    if bool(rel.get("pass_")) != rel_ok:
        probs.append("MC_PullReliability pass_ does not follow its rule")
    if rel.get("pairs") and not _close(m, float(np.mean(rel["pairs"]))):
        probs.append("MC_PullReliability mean is not the mean of its pairs")
    share = mc["MC_Terms"].get("share_topic")
    if bool(mc["MC_Terms"].get("pass_")) != bool(share is not None and share >= 0.5):
        probs.append("MC_Terms pass_ does not follow its rule")
    flags = []
    if not conc_ok:
        flags.append("criterion doubtful")
    if not rel_ok:
        flags.append("outcome unreliable")
    if share is not None and share < 0.5:
        flags.append("mostly plain search terms")
    if V.get("flags") != flags:
        probs.append(f"flags {V.get('flags')} != {flags} derived from the checks")
    w = mc["MC_Weekly"]
    if w["requests"] != w["ok"] + w["missing"]:
        probs.append("MC_Weekly requests != ok + missing")
    if real and w["requests"] != REQUESTS_PER_PULL * 3:
        probs.append(f"MC_Weekly counts {w['requests']} requests, not {REQUESTS_PER_PULL * 3}")
    if real and (V.get("pulls_used") != STEPS or V.get("B_perm") != B_REAL or V.get("B_boot") != B_REAL):
        probs.append(f"pulls {V.get('pulls_used')} / draws {V.get('B_perm')}, {V.get('B_boot')} are not the "
                     f"pre-registered three pulls and 10,000 draws")
    # --- outcome definedness
    for s in SUBS:
        d = V["outcome_defined_per_substrate"].get(s) or {}
        nu = sum(1 for r in ut if r["sub"] == s)
        ny = sum(1 for r in ut if r["sub"] == s and finite(r.get("Y")))
        if d.get("units") != nu or d.get("Y_defined") != ny:
            probs.append(f"outcome_defined_per_substrate[{s}] {d} != unit table ({nu}, {ny})")
    # --- tests
    for name in TESTS:
        T = V["tests"][name]
        spec, seed, min_n = specs[name]
        if T.get("seed") != seed or T.get("min_n") != min_n:
            probs.append(f"{name}: seed/min_n {T.get('seed')}/{T.get('min_n')} != locked {seed}/{min_n}")
        if T.get("spec") != {"x": spec[0], "y": spec[1], "controls": list(spec[2])}:
            probs.append(f"{name}: spec {T.get('spec')} != locked {spec}")
        if T.get("flags") != V.get("flags"):
            probs.append(f"{name}: flags differ from the run's flags")
        if T.get("n") != sum((T.get("n_per_substrate") or {}).values()):
            probs.append(f"{name}: n != sum of n_per_substrate")
        ci90 = T.get("ci90") or [None, None]
        want = SC.verdict(T.get("rho"), T.get("p_one"), T.get("p_two"), ci90[1], T.get("n"), min_n)
        if T.get("verdict") != want["verdict"] or (T.get("labels") or []) != want["labels"]:
            probs.append(f"{name}: verdict {T.get('verdict')} {T.get('labels')} != scorer rule {want['verdict']} "
                         f"{want['labels']}")
        if (T.get("reason") or None) != (want.get("reason") or None):
            probs.append(f"{name}: reason {T.get('reason')!r} != {want.get('reason')!r}")
        if finite(T.get("rho")):
            r2_, n2, _ = recompute_rho(V, spec)
            if n2 != T["n"] or not _close(r2_, T["rho"]):
                probs.append(f"{name}: rho {T['rho']} (n {T['n']}) != {r2_} (n {n2}) recomputed from the unit table")
            if T.get("ci90") and T.get("ci95"):
                lo95, hi95, lo90, hi90 = T["ci95"][0], T["ci95"][1], T["ci90"][0], T["ci90"][1]
                if not (lo95 <= lo90 + 1e-12 and lo90 <= hi90 + 1e-12 and hi90 <= hi95 + 1e-12):
                    probs.append(f"{name}: intervals out of order {T['ci90']} {T['ci95']}")
            for k in ("p_one", "p_two"):
                if finite(T.get(k)) and not (0 < T[k] <= 1):
                    probs.append(f"{name}: {k} = {T[k]} outside (0, 1]")
    if probs:
        raise Inconsistent("; ".join(probs))
    return True


# --------------------------------------------------------------------------- repository lock records (real mode)
def git(*args, root=ROOT):
    r = subprocess.run(["git", "-C", str(root)] + list(args), capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else None


def git_tag_commit(tag=EXPECTED_PREREG_TAG, root=ROOT):
    return git("rev-parse", "-q", "--verify", f"refs/tags/{tag}^{{commit}}", root=root)


def git_tag_date_utc(tag=EXPECTED_PREREG_TAG, root=ROOT):
    s = git("for-each-ref", "--format=%(taggerdate:iso-strict)", f"refs/tags/{tag}", root=root)
    if not s:
        return None
    return dt.datetime.fromisoformat(s).astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M")


def manifest_mismatches(root=ROOT):
    """Locked files whose SHA-256 differs from prereg/LOCK_MANIFEST_v0_43.sha256 (empty list = all match)."""
    man = Path(root) / "osf/v43/prereg/LOCK_MANIFEST_v0_43.sha256"
    bad = []
    for line in man.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        sha, rel = line.split(None, 1)
        p = Path(root) / rel.strip()
        got = hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None
        if got != sha:
            bad.append(rel.strip())
    return bad


def deviation_entries(path):
    txt = Path(path).read_text(encoding="utf-8")
    return re.findall(r"(?m)^## Entry (\d+)", txt), txt


_NUM = re.compile(r"\d+(?:[.,]\d+)*")


def numeric_tokens(text):
    """Digit groups (decimals and thousands separators kept together), trailing separators dropped."""
    return [t.rstrip(".,") for t in _NUM.findall(text)]
