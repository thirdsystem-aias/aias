#!/usr/bin/env python3
"""
v113_values.py -- the single place where the v1.13 Grounding Paper A (paper and charts) reads numbers.

Every number printed by fill_paper_v1_13.py and scripts/build_charts_v113.py comes from one of these machine outputs,
never from a hand-typed literal:

  verdicts  osf/methodology/v1_13/v1_13_verdicts.json   score_v1_13.py --stage C1, then --stage C2 (appends
            "stage_C2"); synthetic: tests/fixtures/SYNTHETIC_<scenario>_v1_13_verdicts.json
  sdri      osf/methodology/v1_13/audit/v1_13_sdri.csv   audit_v1_13.py --sdri (Part II; present only if collected)
  registry  osf/methodology/v1_13/registries/brand_domains_v1_13.csv  (locked; brand names and D_b status only)

Values.put() records, for every formatted value, the source, the path, the raw value and the formatting function, so
the tests can re-resolve each printed number (tests/test_fill_paper_v1_13.py). Values.derive() records a named
function of several leaves (counts and shares over the SDRI table, minima and maxima across substrates).

Verdict words are the scorer's, verbatim: CONFIRMED, MARGINAL, FALSIFIED, UNDETERMINED, INACTIVE for the legs
(score_v1_13.VERDICTS) and PASS, FAIL, MARGINAL, UNDETERMINED for the gate (score_v1_13.gate). The case_* functions
only split those words by cause (which template sentence explains them); check_consistency() recomputes every word
with the locked scorer's own verdict functions and refuses the file if one differs.
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
DESIGN = ROOT / "osf/methodology/v1_13"
sys.path.insert(0, str(DESIGN / "scripts"))
import score_v1_13 as S  # noqa: E402  (read-only: verdict functions and constants; no stage is run)

PREREG_TAG, AUDIT_TAG = "v1.13-prereg-r1", "v1.13-audit-r1"
VERDICTS_JSON = DESIGN / "v1_13_verdicts.json"
SDRI_CSV = DESIGN / "audit" / "v1_13_sdri.csv"
REGISTRY_CSV = DESIGN / "registries" / "brand_domains_v1_13.csv"
GIT_ANCHOR = DESIGN / "anchor" / "git_anchor_v1_13.json"
AUDIT_ANCHOR = DESIGN / "anchor" / "audit_anchor_v1_13.json"
AUDIT_RECEIPT = DESIGN / "anchor" / "audit_receipt_v1_13.json"
DEVIATIONS = DESIGN / "anchor" / "DEVIATIONS.md"

SUBS = list(S.SUBSTRATES)
CAT = {"v19": "audiophile headphones", "v20": "skincare", "v21": "cosmetics", "v22": "automotive",
       "v23": "premium spirits"}
CAT_SHORT = {"v19": "Headphones", "v20": "Skincare", "v21": "Cosmetics", "v22": "Automotive", "v23": "Spirits"}
MODELS = list(S.PANELS["N3"])
MODEL_NAME = {S.FABLE: "Claude Fable 5.2", S.GPT6: "GPT-6 Astra", S.GEM4: "Gemini 4 Argon"}
PROVIDER_NAME = {"anthropic": "Anthropic", "openai": "OpenAI", "google": "Google"}
CLASSES = list(S.CLASS_ORDER)
CLASS_NAME = {"brand_owned": "brand-owned", "reference": "Wikipedia/reference", "forum_ugc": "forum/UGC",
              "news": "news", "review_editorial": "review/editorial", "retailer": "retailer", "other": "other",
              "unresolved": "unresolved"}
GATE_LEGS = list(S.GATE_LEGS)
COND_LEGS = list(S.CONDITIONAL_LEGS)
SHORT = {"H1_Sep_Presence": "H1", "H2_Sep_Consistency": "H2", "H3_Run_Reliability": "H3", "H4_Sep_Ranking": "H4",
         "H5_Sep_Sentiment": "H5", "H6_Sep_Coverage": "H6", "H7_Struct_Gap": "H7"}
PLAIN = {"H1_Sep_Presence": "Presence", "H2_Sep_Consistency": "Consistency", "H3_Run_Reliability": "run reliability",
         "H4_Sep_Ranking": "Ranking", "H5_Sep_Sentiment": "Sentiment", "H6_Sep_Coverage": "Coverage",
         "H7_Struct_Gap": "structured-data richness"}
SENS = [("S1_denominator_m", "S1 denominator $m_b$"), ("S2_citations", "S2 cited set"),
        ("S4_floor_3", "S4 floor 3"), ("S4_floor_10", "S4 floor 10"), ("S5_gemini_dropped", "S5 Gemini dropped"),
        ("S5_gemini_kept", "S5 Gemini kept"), ("S7_legacy_t3", "S7 AIAS 2.0 $t_3$ comparators"),
        ("S9_text_urls", "S9 URLs in the text"), ("S10_uncentred", "S10 uncentred ranks"),
        ("S11_without_Denon", "S11 without Denon")]
SYNTHETIC_MARK = "SYNTHETIC TEST — NOT RESULTS"
# Pending decision (coordinator, Nov 11, 2026): Samsung's agency Cheil Worldwide / its Iris unit has worked for five
# registry brands. Text from CLAUDE.md's COI notes of Nov 11, 2026 (v0.62 r3 screen); off unless --coi-cheil is given.
CHEIL_UNITS = [("v22", "C.4"), ("v22", "A.7"), ("v22", "A.5"), ("v23", "S03"), ("v20", "C.7")]


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


def has(obj, path):
    try:
        v = jget(obj, path)
    except Missing:
        return False
    return v is not None and not (isinstance(v, float) and not math.isfinite(v))


def finite(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)


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


def f1(x):
    s = f"{float(x):.1f}"
    return "0.0" if s == "-0.0" else s


FORMATS = {f.__name__: f for f in (r3, r2, p4, pct0, pct1, i0, f1)}


# --------------------------------------------------------------------------- derived values (named; tests recompute)
def d_min(*xs):
    return float(min(float(x) for x in xs))


def d_max(*xs):
    return float(max(float(x) for x in xs))


def d_count(*xs):
    """Number of non-missing values."""
    return float(sum(1 for x in xs if x not in (None, "")))


def d_count_eq(val, *xs):
    return float(sum(1 for x in xs if str(x) == str(val)))


def d_share_eq(val, *xs):
    xs = [x for x in xs if x not in (None, "")]
    return float(sum(1 for x in xs if str(x) == str(val))) / len(xs) if xs else float("nan")


def d_median(*xs):
    v = sorted(float(x) for x in xs if x not in (None, ""))
    if not v:
        return float("nan")
    n = len(v)
    return v[n // 2] if n % 2 else (v[n // 2 - 1] + v[n // 2]) / 2


def d_sum(*xs):
    return float(sum(float(x) for x in xs if x not in (None, "")))


DERIVE = {f.__name__: f for f in (d_min, d_max, d_count, d_count_eq, d_share_eq, d_median, d_sum)}


class Values:
    """Formatted values with provenance: put() for one leaf, derive() for a named function of leaves, word() for text
    chosen from the data, table() for a markdown table whose every number is listed."""

    def __init__(self, sources):
        self.src = sources
        self.vals = {}
        self.prov = {}

    def raw(self, src, path):
        return jget(self.src[src], path)

    def put(self, name, src, path, fmt):
        raw = jget(self.src[src], path)
        if raw is None or raw == "" or (isinstance(raw, float) and not math.isfinite(raw)):
            raise Missing(f"{src}:{'/'.join(map(str, path))} is null")
        s = fmt(raw)
        self.vals[name] = s
        self.prov[name] = {"kind": "json", "source": src, "path": list(path), "raw": raw, "fmt": fmt.__name__,
                           "formatted": s}
        return s

    def derive(self, name, fn, refs, fmt, consts=()):
        raws = [jget(self.src[s], p) for s, p in refs]
        raw = fn(*consts, *raws)
        if isinstance(raw, float) and not math.isfinite(raw):
            raise Missing(f"{name}: derived value undefined")
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
def read_rows(path):
    return list(csv.DictReader(Path(path).read_text(encoding="utf-8").splitlines()))


def load_sources(verdicts_path, sdri_path=None, registry_path=REGISTRY_CSV):
    V = json.loads(Path(verdicts_path).read_text(encoding="utf-8"))
    sdri = {"rows": read_rows(sdri_path)} if sdri_path and Path(sdri_path).exists() else {"rows": []}
    reg = {f"{r['substrate']}|{r['brand_id']}": r for r in read_rows(registry_path)}
    return {"verdicts": V, "sdri": sdri, "registry": reg}


def is_synthetic(V):
    return "synthetic_fixture" in V


def brand_name(src, key):
    r = src["registry"].get(key)
    return r["brand"] if r and not is_synthetic(src["verdicts"]) else key.split("|", 1)[1]


def unit_key(k):
    s, b = k.split("|", 1)
    return s, b


# --------------------------------------------------------------------------- where each leg's final record lives
def cond_state(V, h):
    """H4/H6 (and H5): {case, word, leg_path, src_path, stage, gating, reason}. case: INACTIVE, PENDING (Stage C1 only),
    UNAVAILABLE (not by Stage C2: handed to Paper B), COMPUTED."""
    active = bool((V["gate"].get("active") or {}).get(h))
    if not active:
        return {"case": "INACTIVE", "word": V["verdicts"].get(h, "INACTIVE")}
    srckey = {"H4_Sep_Ranking": "H4_ranking_source", "H6_Sep_Coverage": "H6_coverage_source"}.get(h)
    c2key = {"H4_Sep_Ranking": "ranking", "H6_Sep_Coverage": "coverage"}.get(h)
    if srckey is None:                                          # H5: no reader in the locked scorer (N20)
        return {"case": "COMPUTED" if (V["legs"].get(h)) else "UNAVAILABLE", "word": V["verdicts"][h],
                "leg_path": ["legs", h, 0], "stage": "C1", "gating": True, "reason": (V.get("reasons") or {}).get(h)}
    src = V.get(srckey) or {}
    if src.get("sha256"):
        return {"case": "COMPUTED", "word": V["verdicts"][h], "leg_path": ["legs", h, 0], "src_path": [srckey],
                "stage": "C1", "gating": bool((V["gate"].get("gating") or {}).get(h)) and
                (h != "H4_Sep_Ranking" or bool(src.get("h4_gates")))}
    c2 = V.get("stage_C2")
    if c2 is None:
        return {"case": "PENDING", "word": V["verdicts"][h], "reason": (V.get("reasons") or {}).get(h)}
    r = c2.get(c2key) or {}
    if "leg" in r:
        src2 = r.get(srckey) or {}
        gating = bool(r.get("h4_gates")) if h == "H4_Sep_Ranking" else True
        return {"case": "COMPUTED", "word": r[h], "leg_path": ["stage_C2", c2key, "leg"],
                "src_path": ["stage_C2", c2key, srckey], "stage": "C2", "gating": gating, "src": src2}
    return {"case": "UNAVAILABLE", "word": r.get(h, "UNDETERMINED"), "reason": r.get("reason") or ""}


def h7_state(V):
    c2 = V.get("stage_C2")
    if c2 is None:
        return {"case": "PENDING", "word": None}
    w = c2["H7_Struct_Gap"]
    if "leg" not in c2:
        return {"case": "NOT_COLLECTED", "word": w, "reason": c2.get("reason") or ""}
    leg = c2["leg"]
    if w == "UNDETERMINED":
        return {"case": "UNDETERMINED_FLOOR", "word": w, "leg_path": ["stage_C2", "leg"]}
    return {"case": w, "word": w, "leg_path": ["stage_C2", "leg"], "leg": leg}


def final_gate(V):
    """{c1, final, reissues: [(leg, before, after)], downgraded_by: [legs]} from the C1 gate and Stage C2's re-issues."""
    c1 = V["gate"]["verdict"]
    out = {"c1": c1, "final": c1, "reissues": [], "downgraded_by": []}
    for n in V["gate"].get("notes") or []:
        m = re.match(r"PASS downgraded to MARGINAL: (.*) FALSIFIED", n)
        if m:
            out["downgraded_by"] += [x.strip() for x in m.group(1).split(",")]
    c2 = V.get("stage_C2") or {}
    for h, key in (("H4_Sep_Ranking", "ranking"), ("H6_Sep_Coverage", "coverage")):
        ri = (c2.get(key) or {}).get("gate_reissued")
        if ri:
            out["reissues"].append((h, ri["before"], ri["after"]))
            if ri["before"] == "PASS" and ri["after"] == "MARGINAL":
                out["downgraded_by"].append(h)
            out["final"] = ri["after"]
    return out


# --------------------------------------------------------------------------- verdict cases (cause of each word)
def case_sep(V, h):
    """H1/H2: CONFIRMED, MARGINAL, FALSIFIED, UNDETERMINED_MQ5, UNDETERMINED_FLOOR."""
    w = V["verdicts"][h]
    if w in ("CONFIRMED", "MARGINAL", "FALSIFIED"):
        return w
    if w != "UNDETERMINED":
        raise ValueError(f"{h}: unknown verdict {w!r}")
    if V["MQ"]["MQ5"]["failed"]:
        return "UNDETERMINED_MQ5"
    return "UNDETERMINED_FLOOR"


def case_h3(V):
    w = V["verdicts"]["H3_Run_Reliability"]
    if w in ("CONFIRMED", "MARGINAL", "FALSIFIED"):
        return w
    if w != "UNDETERMINED":
        raise ValueError(f"H3: unknown verdict {w!r}")
    return "UNDETERMINED_PAIRS"


def case_leg_word(word, leg):
    """A computed one-leg verdict (H4, H6) split by cause."""
    if word in ("CONFIRMED", "MARGINAL", "FALSIFIED"):
        return word
    if word != "UNDETERMINED":
        raise ValueError(f"unknown verdict {word!r}")
    return "UNDETERMINED_FLOOR"


def case_gate(V):
    g = final_gate(V)
    f = g["final"]
    if f == "MARGINAL" and g["downgraded_by"]:
        return "MARGINAL_DOWNGRADED"
    if f == "UNDETERMINED":
        return "UNDETERMINED_MQ5" if V["MQ"]["MQ5"]["failed"] else "UNDETERMINED"
    if f in ("PASS", "FAIL", "MARGINAL"):
        return f
    raise ValueError(f"unknown gate verdict {f!r}")


# --------------------------------------------------------------------------- consistency (the scorer's own functions)
def check_consistency(src):
    """Recompute every verdict word from its statistics with the locked scorer's functions; refuse any difference.
    Also: the C2 re-issue chain, H7 against the SDRI table, MQ5's rated count against the units, the sensitivity
    verdict changes against the sensitivities. Raises Inconsistent."""
    V = src["verdicts"]
    errs = []
    for k in ("phase", "stage", "primary_field"):
        want = {"phase": S.PHASE_ID, "stage": "C1", "primary_field": S.PRIMARY_FIELD}[k]
        if V.get(k) != want:
            errs.append(f"{k} = {V.get(k)!r}, expected {want!r}")
    for h, w in V["verdicts"].items():
        if w not in S.VERDICTS:
            errs.append(f"{h}: verdict {w!r} is not a scorer word")
    mq5 = bool(V["MQ"]["MQ5"]["failed"])
    for h in ("H1_Sep_Presence", "H2_Sep_Consistency"):
        if S.sep_verdict(V["legs"][h], mq5) != V["verdicts"][h]:
            errs.append(f"{h}: {V['verdicts'][h]} but its legs give {S.sep_verdict(V['legs'][h], mq5)}")
    if S.reliability_verdict(V["H3"]) != V["verdicts"]["H3_Run_Reliability"]:
        errs.append("H3_Run_Reliability: verdict differs from reliability_verdict(H3)")
    rs = V.get("H4_ranking_source") or {}
    gating = {"H4_Sep_Ranking": S.h4_gates(rs if rs.get("sha256") else None)}
    try:
        g = S.gate(V["verdicts"], V["gate"]["active"], gating)
        if g["verdict"] != V["gate"]["verdict"]:
            errs.append(f"gate {V['gate']['verdict']} but gate() gives {g['verdict']}")
    except ValueError as e:
        errs.append(f"gate(): {e}")
    for h in ("H4_Sep_Ranking", "H6_Sep_Coverage"):
        st = cond_state(V, h)
        if st["case"] == "COMPUTED":
            leg = jget(V, st["leg_path"])
            if S.sep_verdict([leg]) != st["word"]:
                errs.append(f"{h}: {st['word']} but its leg gives {S.sep_verdict([leg])}")
    c2 = V.get("stage_C2")
    if c2 is not None:
        before = V["gate"]["verdict"]
        r = c2.get("ranking") or {}
        if r.get("gate_reissued"):
            ri = r["gate_reissued"]
            want = "MARGINAL" if (r.get("h4_gates") and before == "PASS" and r["H4_Sep_Ranking"] == "FALSIFIED") \
                else before
            if ri["before"] != before or ri["after"] != want:
                errs.append(f"H4 re-issue {ri['before']}->{ri['after']}, expected {before}->{want}")
            before = ri["after"]
        cv = c2.get("coverage") or {}
        if cv.get("gate_reissued"):
            ri = cv["gate_reissued"]
            want = "MARGINAL" if (before == "PASS" and cv["H6_Sep_Coverage"] == "FALSIFIED") else before
            if ri["before"] != before or ri["after"] != want:
                errs.append(f"H6 re-issue {ri['before']}->{ri['after']}, expected {before}->{want}")
        collected = "leg" in c2
        if S.struct_gap_verdict(c2.get("leg"), collected) != c2["H7_Struct_Gap"]:
            errs.append("H7_Struct_Gap differs from struct_gap_verdict(leg)")
        rows = src["sdri"]["rows"]
        if collected and not rows:
            errs.append("H7 was computed (Part II collected) but no SDRI table was given")
        if not collected and rows:
            errs.append("an SDRI table was given but Stage C2 recorded Part II as not collected")
        if collected and rows:
            n = h7_expected_n(V, rows)
            if n != c2["leg"]["n"]:
                errs.append(f"H7 n = {c2['leg']['n']} but the SDRI table and the rated G* give {n}")
    n_rated = sum(1 for u in V["units"].values() if u["rated"])
    if V["MQ"]["MQ5"]["n_rated"] != n_rated:
        errs.append(f"MQ5 n_rated {V['MQ']['MQ5']['n_rated']} != rated units {n_rated}")
    sens = V.get("sensitivities") or {}
    vc = V.get("verdict_changes") or {}
    for name, sv in sens.items():
        if "verdicts" not in sv:
            continue
        want = {h: [sv["verdicts"][h], V["verdicts"][h]] for h in sv["verdicts"] if sv["verdicts"][h] != V["verdicts"][h]}
        got = {h: list(v) for h, v in (vc.get(name) or {}).items()}
        if want != got:
            errs.append(f"verdict_changes[{name}] does not match the sensitivity's verdicts")
    if errs:
        raise Inconsistent("; ".join(errs))


def h7_expected_n(V, rows):
    """Units with a finite SDRI (phantom rows excluded, as read_sdri) and a rated G*, in substrates with >= 5."""
    gs = {k: u["G_star"] for k, u in V["units"].items() if u["rated"]}
    keys = []
    for r in rows:
        k = f"{r['substrate']}|{r['brand_id']}"
        if str(r.get("phantom", "0")) == "1" or r.get("SDRI") in ("", None) or k not in gs:
            continue
        keys.append(k)
    per = {}
    for k in keys:
        per[k.split("|")[0]] = per.get(k.split("|")[0], 0) + 1
    return sum(1 for k in keys if per[k.split("|")[0]] >= S.MIN_UNITS_PER_SUB)


# --------------------------------------------------------------------------- git (real mode)
def git(args, root=ROOT):
    r = subprocess.run(["git", "-C", str(root)] + args, capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else None


def tag_commit(tag):
    return git(["rev-parse", "-q", "--verify", f"refs/tags/{tag}^{{commit}}"])


def tag_date_utc(tag):
    from datetime import datetime, timezone
    s = git(["for-each-ref", "--format=%(taggerdate:iso-strict)", f"refs/tags/{tag}"])
    if not s:
        return None
    return datetime.fromisoformat(s).astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M")


def joinand(xs):
    xs = list(xs)
    if len(xs) <= 1:
        return "".join(xs)
    return ", ".join(xs[:-1]) + " and " + xs[-1]


def names(models):
    return joinand(MODEL_NAME.get(m, m) for m in models)


_NUM = re.compile(r"\d+(?:[.,]\d+)*")


def numeric_tokens(text):
    return [t.rstrip(".,") for t in _NUM.findall(text)]
