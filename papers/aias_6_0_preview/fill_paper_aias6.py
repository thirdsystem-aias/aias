#!/usr/bin/env python3
"""
fill_paper_aias6.py -- fills papers/aias_6_0_preview/aias_6_0_preview_paper_template.md from the AIAS 6.0 Preview
scorer's outputs (osf/aias_6_0_preview/scripts/score_aias_6_0_preview.py --run, tag aias-6-0-preview-prereg-r1).

Introduction and Method are fixed text written from the locked pre-registration. Results and Discussion are written
in advance as alternative sentences, one per pre-registered outcome, inside blocks this script selects from the
scorer's outputs (template engine forked unchanged from papers/v1_11/fill_paper_v1_11.py on branch v1.11-paper, itself
from v1.12 and v0.42). The headline sentence follows the wording fixed in pre-registration section 6.6 (classes A,
A_k, B, C, U) and rules W1-W3; for class C (H_Structure FALSIFIED) drafting pauses: the fill refuses unless
--class-c-draft is given, which builds an internal draft marked as such.

No number is typed here: values are leaves of the scorer's outputs, formatted by named functions, with the provenance
of every value written beside the paper. The fill refuses outputs whose state or verdict words the locked scorer's
own functions do not reproduce (check_consistency), component files whose SHA-256 differs from the scorer's input
log, and (real mode) synthetic outputs, a missing tag or an anchor that does not name the tag's commit.

Usage (real run; see papers/aias_6_0_preview/PIPELINE.md):
  python3 papers/aias_6_0_preview/fill_paper_aias6.py
Synthetic test:
  python3 papers/aias_6_0_preview/fill_paper_aias6.py --synthetic --outputs /tmp/aias6_pipeline_test/synth/ranking_marginal \
      --fig-dir /tmp/aias6_pipeline_test/e2e/ranking_marginal/figs --out /tmp/aias6_pipeline_test/e2e/ranking_marginal/paper/aias_6_0_preview_paper_draft.md
"""
import argparse
import json
import math
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import aias6_values as VV  # noqa: E402

ROOT = VV.ROOT
TEMPLATE = HERE / "aias_6_0_preview_paper_template.md"
ANCHOR = ROOT / "osf/aias_6_0_preview/anchor/git_anchor_aias_6_0_preview.json"
DEVIATIONS = ROOT / "osf/aias_6_0_preview/anchor/DEVIATIONS.md"


class FillError(RuntimeError):
    pass


# =========================================================================== template engine (forked unchanged)
_TAG = re.compile(r"\{%\s*(switch|case|endswitch|if|else|endif)\b\s*([^%]*?)\s*%\}")
_PH = re.compile(r"\{\{\s*([A-Z0-9_]+)\s*\}\}")


def _tokens(tpl):
    tpl = re.sub(r"(?m)^[ \t]*(\{%[^%]*%\})[ \t]*\n", r"\1", tpl)      # a tag alone on its line: drop the line
    out, pos = [], 0
    for m in _TAG.finditer(tpl):
        out.append(("text", tpl[pos:m.start()]))
        out.append((m.group(1), m.group(2).strip()))
        pos = m.end()
    out.append(("text", tpl[pos:]))
    return out


def _parse(toks, i, stop):
    nodes = []
    while i < len(toks):
        kind, arg = toks[i]
        if kind in stop:
            return nodes, i
        if kind == "text":
            nodes.append(("text", arg))
            i += 1
        elif kind == "if":
            then, i = _parse(toks, i + 1, {"else", "endif"})
            other = []
            if toks[i][0] == "else":
                other, i = _parse(toks, i + 1, {"endif"})
            if i >= len(toks) or toks[i][0] != "endif":
                raise FillError(f"unclosed if {arg}")
            nodes.append(("if", arg, then, other))
            i += 1
        elif kind == "switch":
            i += 1
            cases = []
            while i < len(toks) and toks[i][0] == "text":
                if toks[i][1].strip():
                    raise FillError(f"text between switch {arg} and its first case")
                i += 1
            while i < len(toks) and toks[i][0] == "case":
                alts = [a.strip() for a in toks[i][1].split("|")]
                body, i = _parse(toks, i + 1, {"case", "endswitch"})
                cases.append((alts, body))
            if i >= len(toks) or toks[i][0] != "endswitch":
                raise FillError(f"unclosed switch {arg}")
            nodes.append(("switch", arg, cases))
            i += 1
        else:
            raise FillError(f"unexpected {kind} {arg}")
    if stop:
        raise FillError(f"missing {stop}")
    return nodes, i


def _eval(nodes, cases, flags, used):
    out = []
    for n in nodes:
        if n[0] == "text":
            out.append(n[1])
        elif n[0] == "if":
            if n[1] not in flags:
                raise FillError(f"unknown flag {n[1]}")
            used.add(("flag", n[1]))
            out.append(_eval(n[2] if flags[n[1]] else n[3], cases, flags, used))
        else:
            var, alts = n[1], n[2]
            if var not in cases:
                raise FillError(f"unknown switch variable {var}")
            hit = [body for a, body in alts if cases[var] in a]
            if len(hit) != 1:
                raise FillError(f"switch {var}={cases[var]} matched {len(hit)} cases (need exactly 1)")
            used.add(("case", var, cases[var]))
            out.append(_eval(hit[0], cases, flags, used))
    return "".join(out)


def switch_alternatives(tpl):
    """{var: [list of alternative sets]} -- used by the tests to enumerate every outcome."""
    nodes, _ = _parse(_tokens(tpl), 0, set())
    acc = {}

    def walk(ns):
        for n in ns:
            if n[0] == "switch":
                acc.setdefault(n[1], []).append([a for a, _ in n[2]])
                for _, b in n[2]:
                    walk(b)
            elif n[0] == "if":
                walk(n[2]); walk(n[3])
    walk(nodes)
    return acc


def render(tpl, values, cases, flags):
    nodes, _ = _parse(_tokens(tpl), 0, set())
    used = set()
    body = _eval(nodes, cases, flags, used)
    missing = sorted({m.group(1) for m in _PH.finditer(body) if m.group(1) not in values})
    if missing:
        raise FillError(f"no value for placeholders: {missing}")
    body = _PH.sub(lambda m: values[m.group(1)], body)
    for bad in ("{{", "{%"):
        if bad in body:
            raise FillError(f"unfilled template syntax {bad!r} in output")
    return body


# =========================================================================== tables
def md_table(header, rows, align=None):
    align = align or ["l"] + ["r"] * (len(header) - 1)
    vis = lambda t: len(re.sub(r"\$[^$]*\$|\\[a-z]+|[{}`]", "x", t))      # visible width, roughly
    widths = [max(4, min(60, max([vis(header[j])] + [vis(r[j]) for r in rows]))) for j in range(len(header))]
    widths[0] += 4
    sep = ["|:" + "-" * w if a == "l" else "|" + "-" * w + ":" for a, w in zip(align, widths)]
    lines = ["| " + " | ".join(header) + " |", "".join(sep) + "|"]
    lines += ["| " + " | ".join(r) + " |" for r in rows]
    return "\n".join(lines)


class Cells:
    """Collects (formatted, source, path, fmt) for every number put in a table."""

    def __init__(self, val):
        self.val, self.cells = val, []

    def f(self, src, path, fmt, missing="--"):
        try:
            raw = self.val.raw(src, path)
        except VV.Missing:
            return missing
        if raw is None or (isinstance(raw, float) and not math.isfinite(raw)):
            return missing
        s = fmt(raw)
        self.cells.append((s, src, path, fmt.__name__))
        return s


# =========================================================================== consistency with the locked scorer
def scorer():
    sys.path.insert(0, str(ROOT / "osf/aias_6_0_preview/scripts"))
    import score_aias_6_0_preview as S  # noqa: E402  (read-only)
    return S


def _f(x):
    return float("nan") if x is None else float(x)


def check_consistency(src):
    """Every state and verdict word in the outputs is what the locked scorer's functions give (no new decision)."""
    S = scorer()
    V, G = src["results"], src["gates"]
    states = V["gate_states"]
    K = S.included_set(states)
    if K != V["K"] or G["K"] != K or G["gate_states"] != states:
        raise FillError(f"K / gate states are not the scorer's: {V['K']} vs {K}")
    v114 = G.get("v1.14") or {}
    if v114.get("STAGE1_VERDICT") or v114.get("GATE"):
        if S.gate_ranking(v114.get("GATE"), v114.get("STAGE1_VERDICT")) != states["R"]:
            raise FillError("Ranking state is not the scorer's reading of v1.14")
    for m, key in (("Cov", "v1.12_GATE"), ("G", "v1.13_GATE")):
        if G.get(key) and S.gate_component(G[key]) != states[m]:
            raise FillError(f"{m} state is not the scorer's reading of {key}")
    if G.get("v1.11_H1_H5") is not None and S.gate_sentiment(G["v1.11_H1_H5"], bool(G.get("S_t4"))) != states["S"] \
            and states["S"] != "PASS":
        raise FillError("Sentiment state is not the scorer's reading of v1.11")
    for m in ("P", "C"):
        if V["labels"][m]["bridge"] not in S.BRIDGE.values():
            raise FillError(f"bridge label of {m} is not one of the scorer's")
    st = V["structure"]
    panel_ok = bool(V["MQ_Panel"]["ok"])
    if not panel_ok or "S_tests" not in st:
        if st["H_Structure"]["verdict"] != "UNDETERMINED" or st["wording_class"] != "U":
            raise FillError("no structure test, but H_Structure is not UNDETERMINED / class U")
        return
    s_res = {}
    for t in st["S_tests"].values():
        if t.get("source", "Preview") == "Preview":
            ok = (t.get("n") or 0) >= S.N_FLOOR_UNITS and (t.get("categories") or 0) >= S.MIN_CATEGORIES
            if S.band(_f(t["rho"]), ok) != t["verdict"]:
                raise FillError(f"S-test {t['pair']}: verdict {t['verdict']} is not the band of its rho")
        s_res[tuple(t["pair"])] = t
    for x, t in st["I_tests"].items():
        r = _f(t.get("R_adj"))
        if (S.band(r, True) if math.isfinite(r) else "UNDETERMINED") != t["verdict"]:
            raise FillError(f"I-test {x}: verdict {t['verdict']} is not the band of its R_adj")
    status = {m: S.component_status(m, K, s_res, st["I_tests"]) for m in K}
    hs = S.h_structure(K, status, panel_ok)
    if status != st["status"] or hs["verdict"] != st["H_Structure"]["verdict"] or \
            S.wording_class(hs["verdict"], hs["k"]) != st["wording_class"] or s_res[("P", "C")]["verdict"] != st["H_PC_N3"]:
        raise FillError(f"structure words not reproduced: file {st['H_Structure']['verdict']}/{st['wording_class']}, "
                        f"scorer {hs['verdict']}")


# =========================================================================== values
def esc(s):
    return str(s).replace("_", "\\_")


BAND_WORD = {"CONFIRMED": "at most 0.30", "MARGINAL": "between 0.30 and 0.50", "FALSIFIED": "at least 0.50",
             "UNDETERMINED": "below the floor"}


def put_or(val, name, src, path, fmt, alt="n/a"):
    try:
        return val.put(name, src, path, fmt)
    except VV.Missing:
        return val.word(name, alt, [src] + list(path) + ["(null)"])


def names(parts):
    return VV.joinand(VV.NAME[m] for m in parts)


def compute(src, synthetic, fig_dir, prereg_commit, prereg_date, deviations, class_c_draft):
    V, G = src["results"], src["gates"]
    st = V["structure"]
    states = V["gate_states"]
    K = V["K"]
    panel_ok = bool(V["MQ_Panel"]["ok"])
    struct = panel_ok and "S_tests" in st
    val = VV.Values(src)
    cls = st["wording_class"]
    cases = {"CASE_PANEL": "COMPLETE" if panel_ok else "REDUCED", "CASE_R": states["R"], "CASE_S": states["S"],
             "CASE_COV": states["Cov"], "CASE_G": states["G"], "CLASS": cls,
             "CASE_HS": st["H_Structure"]["verdict"]}
    r_pending = not (G.get("v1.14") or {}).get("GATE")
    flags = {"SYNTHETIC": synthetic, "CLASS_C_DRAFT": cls == "C", "STRUCT": struct, "W2": states["S"] == "NOT_RUN",
             "RANK_SHOWN": states["R"] != "NOT_RUN", "R_PENDING": r_pending,
             "ANY_EXPLORATORY": any("label" in t for t in list((st.get("S_tests") or {}).values())
                                    + list((st.get("I_tests") or {}).values())),
             "ANY_MARGINAL_PART": bool(st.get("descriptive_marginal_pairs")),
             "COV_REDUCED": bool(V["labels"]["Cov"].get("reduced_panel")),
             "G_REDUCED": bool(V["labels"]["G"].get("reduced_panel"))}
    val.word("PREREG_TAG", V["prereg_tag"], ["results", "prereg_tag"])
    val.word("PREREG_COMMIT", prereg_commit, ["git", f"refs/tags/{VV.EXPECTED_PREREG_TAG}"])
    val.word("PREREG_DATE", prereg_date, ["git", "taggerdate"])
    val.word("PAPER_DATE", "Synthetic test build" if synthetic else
             datetime.fromisoformat(V["created_utc"]).strftime("%B %Y"), ["results", "created_utc"])
    val.word("FIG_DIR", str(fig_dir), ["argument --fig-dir"])
    val.word("FIG_CAPTION", "SYNTHETIC TEST DATA --- NOT RESULTS." if synthetic else "", ["synthetic flag"])
    val.word("DEV_SENTENCE", deviations[0], deviations[1])
    val.word("VALIDATION_LINE", V["validation_status_line"], ["results", "validation_status_line"])

    # ---------------- K, states and the words of section 6.6
    out_parts = [m for m in VV.ORDER if m not in K]
    kword = VV.NUMWORD[len(K)]
    byphrase = {}
    for m in out_parts:
        byphrase.setdefault(VV.STATE_PHRASE.get(states[m], states[m].lower()), []).append(m)
    outside = "; ".join(f"{names(ms)} {'are' if len(ms) > 1 else 'is'} {ph}" for ph, ms in byphrase.items())
    val.word("K_SENTENCE", f"The included set has {kword} parts ({names(K)}).",
             ["results", "K", "gate_states"])
    val.word("K_CAPTION", "Included set $K$: " + names(K) + ".", ["results", "K"])
    pc = (st.get("S_tests") or {}).get("PxC")
    if pc is not None:
        put_or(val, "HPC_RHO", "results", ["structure", "S_tests", "PxC", "rho"], VV.r3)
        val.put("HPC_N", "results", ["structure", "S_tests", "PxC", "n"], VV.i0)
        put_or(val, "HPC_LO", "results", ["structure", "S_tests", "PxC", "ci90", 0], VV.r3)
        put_or(val, "HPC_HI", "results", ["structure", "S_tests", "PxC", "ci90", 1], VV.r3)
        val.word("HPC_V", st["H_PC_N3"], ["results", "structure", "H_PC_N3"])
    hpc = st.get("H_PC_N3")
    w1 = {"CONFIRMED": "Presence and Consistency stay separable on the newest models.",
          "MARGINAL": f"Presence and Consistency stay separable on the newest models, with moderate coupling "
                      f"(ρ = {val.vals.get('HPC_RHO')}).",
          "FALSIFIED": f"On the newest models Consistency moves with Presence (ρ = {val.vals.get('HPC_RHO')}); "
                       f"AIAS 2.0's separability is shown on the retiring panel only.",
          "UNDETERMINED": "Whether Presence and Consistency stay separable on the newest models could not be determined "
                          "(H\\_PC\\_N3 below its floor).",
          None: "Presence and Consistency were not tested on the newest models (no structure test, §4.3)."}[hpc]
    val.word("W1_SENTENCE", w1, ["results", "structure", "H_PC_N3"],
             ["HPC_RHO"] if hpc in ("MARGINAL", "FALSIFIED") else [])
    val.word("W2_SENTENCE", "Sentiment is not on the Preview's panel: it is reported beside the profile as a separate "
             "reading on the legacy panel.", ["results", "gate_states", "S"])
    hs = st["H_Structure"]
    for k in ("k", "d", "u"):
        val.put(f"HS_{k.upper()}", "results", ["structure", "H_Structure", k], VV.i0)
    k = hs["k"]
    if not panel_ok:
        cause = "an N3 model failed v0.42's drop rule in the search-off condition (§4.3)"
    elif k < 3:
        cause = f"fewer than three parts were in the included set (only {names(K)})"
    else:
        cause = "fewer than three included parts had a determined status"
    val.word("U_CAUSE", cause, ["results", "structure", "H_Structure"])
    val.word("CLASS", {"A_k": "A$_k$"}.get(cls, cls), ["results", "structure", "wording_class"])
    if cls == "A":
        head = "On the newest models, the six provisional parts of AI Availability are six separate readings of a brand."
    elif cls == "A_k":
        head = (f"On the newest models, the {kword} provisional parts measured so far are separate readings of a brand"
                + (f"; {outside}." if outside else "."))
    elif cls == "B":
        bits = []
        for key, t in st["S_tests"].items():
            if t["verdict"] == "FALSIFIED":
                a, b = t["pair"]
                r = val.put(f"OVL_{key}", "results", ["structure", "S_tests", key, "rho"], VV.r3)
                bits.append(f"{VV.NAME[b]} overlaps {VV.NAME[a]} (ρ = {r})")
        for m in K[1:]:
            if st["status"][m] == "PARTLY DISTINCT":
                earlier = [e for e in K if VV.ORDER.index(e) < VV.ORDER.index(m)
                           and st["S_tests"][f"{e}x{m}"]["verdict"] == "MARGINAL"]
                with_ = [VV.NAME[e] for e in earlier]
                if st["I_tests"].get(m, {}).get("verdict") == "MARGINAL":
                    with_.append("the earlier parts taken together")
                bits.append(f"{VV.NAME[m]} is only partly separable from {VV.joinand(with_)}")
            elif st["status"][m] == "UNDETERMINED":
                bits.append(f"the status of {VV.NAME[m]} could not be determined")
        head = (f"On the newest models, {VV.NUMWORD[hs['d']]} of the {kword} parts measured are separate readings of a "
                f"brand; " + "; ".join(bits) + ".")
    elif cls == "C":
        head = "No headline: under the pre-registration (§6.6, class C) drafting pauses and the author decides the direction."
    else:
        head = f"On the newest models, how the parts relate could not be determined: {cause}."
    val.word("HEADLINE", head, ["results", "structure", "wording_class"], [n for n in val.vals if n.startswith("OVL_")])

    # ---------------- Ranking (W3: "retest pending" until v1.14's final gate exists) and the marginal legs
    val.word("R_GATE_SOURCE", "Stage 1 interim verdict" if r_pending else "final gate after its retest",
             ["gates", "v1.14"])
    legs_txt = {}
    for m in ("R", "Cov", "G"):
        parts = []
        for name, rho, n, path in VV.marginal_legs(src, m):
            t = esc(name)
            if rho is not None:
                r = val.put(f"LEG_{m}_{name}_RHO", "components", path[1:] + ["rho"], VV.r3)
                nn = val.put(f"LEG_{m}_{name}_N", "components", path[1:] + ["n"], VV.i0)
                t += f", $\\rho_w$ = {r}, $n$ = {nn}"
            parts.append(t)
        legs_txt[m] = "; ".join(parts) if parts else "the marginal leg is not named in the component files read"
        val.word({"R": "R_LEGS", "Cov": "COV_LEGS", "G": "G_LEGS"}[m], legs_txt[m],
                 ["components", m], [n for n in val.vals if n.startswith(f"LEG_{m}_")])
    rp = " (retest pending)" if r_pending else ""
    rank_abs = {"PASS": "Ranking is included as provisional after its final gate.",
                "PASS_RETEST_PENDING": "Ranking is included as provisional, retest pending.",
                "MARGINAL": f"Ranking{rp} is under review: its {val.vals['R_GATE_SOURCE']} was MARGINAL, so it is shown "
                            f"below the profile and counts in no verdict.",
                "FAIL": f"Ranking{rp} did not pass its {val.vals['R_GATE_SOURCE']} and is not in the profile.",
                "UNDETERMINED": f"Ranking's {val.vals['R_GATE_SOURCE']} was UNDETERMINED{rp}; it is not in the profile.",
                "NOT_RUN": ""}[states["R"]]
    val.word("RANK_ABSTRACT", rank_abs, ["results", "gate_states", "R"])
    rank_disc = {"PASS": "Ranking enters with its final gate; its place in the structure is as tested above.",
                 "PASS_RETEST_PENDING": "Every Ranking result above is provisional, retest pending: v1.14's final gate "
                                        "needs the $t_5$ retest, and a different final gate is entered by dated addendum.",
                 "MARGINAL": f"Ranking's place is open{rp}: its {val.vals['R_GATE_SOURCE']} was MARGINAL ({legs_txt['R']}), "
                             f"so it stands outside every structure verdict here, and its correlations with the included "
                             f"parts are descriptive only."
                             + (" Whether it joins the profile is decided by v1.14's final gate after its retest, entered "
                                "by dated addendum." if r_pending else ""),
                 "FAIL": f"Ranking{rp} did not pass its {val.vals['R_GATE_SOURCE']}; it is reported as a negative result "
                         f"in its own paper and is outside the profile.",
                 "UNDETERMINED": f"Ranking's {val.vals['R_GATE_SOURCE']} was UNDETERMINED{rp}; the structure question "
                                 f"for Ranking stays open.",
                 "NOT_RUN": ""}[states["R"]]
    val.word("RANK_DISCUSSION", rank_disc, ["results", "gate_states", "R"], [n for n in val.vals if n.startswith("LEG_R_")])
    val.word("R_RETEST", rp, ["gates", "v1.14", "GATE"])
    gw = G.get("v1.14") or {}
    val.word("R_GATE_SOURCE_WORD", f"{val.vals['R_GATE_SOURCE']} {gw.get('GATE') or gw.get('STAGE1_VERDICT')}{rp}",
             ["gates", "v1.14"])
    for m, nm in (("P", "BRIDGE_P"), ("C", "BRIDGE_C")):
        val.word(nm, f"is labelled “{V['labels'][m]['bridge']}”", ["results", "labels", m, "bridge"])

    # ---------------- 3.1 checks
    mj = V["MQ_Join"]
    n112 = val.put("JOIN_N", "results", ["MQ_Join", "expected_units"], VV.i0)
    par = V["MQ_Parity_comparators"]
    if par.get("passes"):
        pn = val.put("PARITY_N", "results", ["MQ_Parity_comparators", "units_compared"], VV.i0)
        ptxt = (f"Presence and Consistency recomputed from v0.42's files with v1.14's locked function equalled v1.14's "
                f"values on all {pn} units it lists (MQ\\_Parity)")
    else:
        ptxt = "MQ\\_Parity on Presence and Consistency was not applicable (no v1.14 Stage 1 output)"
    lock = V["MQ_Lock"]
    ltxt = ("the lock record (tag, anchor and every locked file) was verified (MQ\\_Lock)" if lock.get("ok") is True
            else "MQ\\_Lock was not checked (synthetic test run)")
    val.word("MQ_SENTENCE", f"Every unit table carried the same {n112} unit keys one to one (MQ\\_Join); {ptxt}; every "
             f"hash record that chains the components' files agreed; {ltxt}.", ["results", "MQ_Join"],
             ["JOIN_N", "PARITY_N"])
    mb = V["MQ_Blind"]
    if mb.get("ok") is True:
        bt = "Every $t_4$-based input was committed after the pre-registration tag (MQ\\_Blind)."
    elif mb.get("ok") is False:
        bt = (f"Some $t_4$-based inputs were committed before the pre-registration tag ({esc(VV.joinand(mb.get('late_inputs') or []))}); "
              f"the Preview's own tests on them are labelled exploratory (MQ\\_Blind).")
    else:
        bt = "MQ\\_Blind was not checked (the tag is not in the repository read)."
    val.word("BLIND_SENTENCE", bt, ["results", "MQ_Blind"])
    val.word("DROPPED", esc(", ".join(V["MQ_Panel"].get("dropped_S0") or [])), ["results", "MQ_Panel"])

    # ---------------- gate table
    v111 = G.get("v1.11_H1_H5") or {}
    src_word = {"R": (f"v1.14 {gw.get('GATE') and 'final gate ' + gw['GATE'] or 'Stage 1 ' + str(gw.get('STAGE1_VERDICT'))}"
                      if (gw.get("GATE") or gw.get("STAGE1_VERDICT")) else "no output"),
                "S": ("v1.11 H1–H5: " + ", ".join(str(v111.get(h, "--")) for h in
                                                    ("H1_Judge_Agreement", "H2_Sep_Presence", "H3_Sep_Consistency",
                                                     "H4_Stability_Short", "H5_Sep_Ranking"))
                      + ("; $S_{t_4}$ scored" if G.get("S_t4") else "; no $S_{t_4}$")) if v111 else "no output",
                "Cov": f"v1.12 gate {G.get('v1.12_GATE')}" if G.get("v1.12_GATE") else "no output",
                "G": f"v1.13 gate {G.get('v1.13_GATE')}" if G.get("v1.13_GATE") else "no output"}
    rows = [["Presence", "AIAS 1.0 (published)", "always included", V["labels"]["P"]["label"], "yes"],
            ["Consistency", "AIAS 2.0", "always included", V["labels"]["C"]["label"], "yes"]]
    for m in ("R", "S", "Cov", "G"):
        lab = V["labels"][m]
        shown = "yes" if lab.get("shown_in_profile") else ("below the profile" if lab.get("band") else "no")
        rows.append([VV.NAME[m], src_word[m], VV.STATE_WORD[states[m]], lab.get("label") or "none", shown])
    val.table("TABLE_GATES", md_table(["Part", "Its own gate", "State read", "Label", "In profile"], rows,
                                      ["l", "l", "l", "l", "l"]), [])

    # ---------------- structure tables
    if struct:
        cl = Cells(val)
        rows = []
        for key, t in st["S_tests"].items():
            a, b = t["pair"]
            pk = ["structure", "S_tests", key]
            srcw = esc(t.get("source", "Preview")) + (" (exploratory)" if t.get("label") else "")
            rows.append([f"{VV.NAME[a]} × {VV.NAME[b]}", cl.f("results", pk + ["rho"], VV.sr3),
                         f"{cl.f('results', pk + ['ci90', 0], VV.sr3)}, {cl.f('results', pk + ['ci90', 1], VV.sr3)}",
                         cl.f("results", pk + ["n"], VV.i0), cl.f("results", pk + ["categories"], VV.i0),
                         cl.f("results", pk + ["p_perm"], VV.p4), t["verdict"], srcw])
        val.table("TABLE_S", md_table(["Pair", "$\\rho_w$", "90% interval", "$n$", "Cat.", "$p$", "Verdict", "Source"],
                                      rows, ["l", "r", "r", "r", "r", "r", "l", "l"]), cl.cells)
        cl = Cells(val)
        rows = []
        for x, t in st["I_tests"].items():
            pk = ["structure", "I_tests", x]
            rows.append([VV.NAME[x], names(t.get("predecessors") or []), cl.f("results", pk + ["n"], VV.i0),
                         cl.f("results", pk + ["R2"], VV.r3), cl.f("results", pk + ["R_adj"], VV.r3),
                         cl.f("results", pk + ["p_perm"], VV.p4), t["verdict"] + (" (exploratory)" if t.get("label") else "")])
        val.table("TABLE_I", md_table(["Part", "Earlier members", "$n$", "$R^2$", "$R_{\\text{adj}}$", "$p$", "Verdict"],
                                      rows, ["l", "l", "r", "r", "r", "r", "l"]), cl.cells)
        val.table("TABLE_STATUS", md_table(["Member", "Status"], [[VV.NAME[m], st["status"][m] + (" (anchor)" if m == "P" else "")]
                                                                 for m in K], ["l", "l"]), [])
        val.word("STATUS_SENTENCE", "Status of the members of $K$ (§6.4): " + "; ".join(
            f"{VV.NAME[m]} {st['status'][m]}" for m in K) + ".", ["results", "structure", "status"])
        cl = Cells(val)
        rows = []
        for key, t in (st.get("descriptive_marginal_pairs") or {}).items():
            a, b = t["pair"]
            pk = ["structure", "descriptive_marginal_pairs", key]
            rows.append([f"{VV.NAME[a]} × {VV.NAME[b]}", cl.f("results", pk + ["rho"], VV.sr3),
                         cl.f("results", pk + ["n"], VV.i0), cl.f("results", pk + ["categories"], VV.i0),
                         BAND_WORD[t["verdict"]]])
        val.table("TABLE_MARGINAL", md_table(["Pair", "$\\rho_w$", "$n$", "Cat.", "$\\lvert\\rho_w\\rvert$ (no verdict)"], rows,
                                             ["l", "r", "r", "r", "l"]), cl.cells)
        cc = st.get("composite_check") or {}
        if cc:
            P = ["structure", "composite_check"]
            r = put_or(val, "CC_RHO", "results", P + ["rho_A_P"], VV.r3)
            da = put_or(val, "CC_DA", "results", P + ["K3_dA"], VV.f1)
            dp = put_or(val, "CC_DP5", "results", P + ["K3_dP_plus_5"], VV.f1)
            fn = val.put("CC_FLOOR_N", "results", P + ["floor_set", "n"], VV.i0)
            fr = put_or(val, "CC_FLOOR_RHO", "results", P + ["floor_set", "rho_A_P"], VV.r3)
            yes = lambda b: "passes" if b else "does not pass"  # noqa: E731
            allp = cc.get("K1_passes") and cc.get("K2_passes") and cc.get("K3_passes")
            val.word("COMPOSITE_SENTENCE",
                     f"Descriptively, the equal-weight mean $A_K$ of each brand's rated parts in $K$ would "
                     f"{'pass' if allp else 'not pass'} v1.9's constraints: K1 (separation) {yes(cc.get('K1_passes'))}; "
                     f"K2 (adds information) {yes(cc.get('K2_passes'))}, with $\\rho_w(A_K, P)$ = {r}; K3 (no windfall) "
                     f"{yes(cc.get('K3_passes'))}, with a difference of {da} points for barely named brands against "
                     f"{dp} allowed. On the {fn} units of the complete-profile set, $\\rho_w(A_K, P)$ = {fr}. Nothing is "
                     f"adopted (§7).", ["results"] + P, ["CC_RHO", "CC_DA", "CC_DP5", "CC_FLOOR_N", "CC_FLOOR_RHO"])
        else:
            val.word("COMPOSITE_SENTENCE", "The composite check was not computed.", ["results", "structure"])
        d3 = V["descriptives"]["D3_dimensions"]
        if "participation_ratio" in d3:
            pr = val.put("D3_PR", "results", ["descriptives", "D3_dimensions", "participation_ratio"], VV.r2)
            na = val.put("D3_NA", "results", ["descriptives", "D3_dimensions", "parallel_analysis", "n_above_null_p95"], VV.i0)
            nu = val.put("D3_N", "results", ["descriptives", "D3_dimensions", "n_U_K"], VV.i0)
            val.word("D3_SENTENCE", f"On the {nu} units of the complete-profile set, the effective number of dimensions "
                     f"of the included parts' rank correlations was {pr} of {kword}, and the number of eigenvalues above "
                     f"the 95th percentile of the within-category permutation null was {na} (D3).", ["results", "descriptives", "D3_dimensions"],
                     ["D3_PR", "D3_NA", "D3_N"])
        else:
            val.word("D3_SENTENCE", "The dimension analysis (D3) was below its floor.", ["results", "descriptives", "D3_dimensions"])
        D9 = ["descriptives", "D9_coverage", "U_K_against_all", "P"]
        un = val.put("UK_N", "results", ["structure", "U_K", "n"], VV.i0)
        um = put_or(val, "UK_P_MED", "results", D9 + ["U_K", "median"], VV.f1)
        am = put_or(val, "ALL_P_MED", "results", D9 + ["all", "median"], VV.f1)
        val.word("UK_SENTENCE", f"{un} units carry every part of $K$ (the complete-profile set); their median Presence "
                 f"was {um}, against {am} over all {n112} units, the lean to well-named brands that sensitivity SD "
                 f"examines (D9).", ["results"] + D9, ["UK_N", "UK_P_MED", "ALL_P_MED", "JOIN_N"])
        sens = V["sensitivities"]
        ch = sens.get("verdict_changes") or []
        hs_ch = [c for c in ch if c["test"] in ("H_Structure", "H_PC_N3")]
        val.word("SENS_SENTENCE", ("No sensitivity analysis changed H\\_Structure or H\\_PC\\_N3." if not hs_ch else
                                   "Under the sensitivity analyses (which never change a verdict) H\\_Structure or "
                                   "H\\_PC\\_N3 differed in: " + "; ".join(
                                       f"{esc(c['sensitivity'])}, {esc(c['test'])} {c['primary']} $\\rightarrow$ "
                                       f"{c['under_sensitivity']}" for c in hs_ch) + ".")
                 + (" Every other listed difference concerns a single pair or status and is in the scorer's output "
                    "(`sensitivities.verdict_changes`)." if len(ch) > len(hs_ch) else ""),
                 ["results", "sensitivities", "verdict_changes"])
        rows = []
        lab = {"SA_without_coi_unit": "SA without the COI-flagged unit", "SB_uncentred": "SB uncentred ranks",
               "SE_without_Sentiment": "SE without Sentiment", "SF_Ranking_by_MNP": "SF Ranking by MNP",
               "SG_Sentiment_legacy_panel": "SG Sentiment, legacy panel", "SH_search_on_variants": "SH search-on variants"}
        for key, nm in lab.items():
            s = sens.get(key) or {}
            if "H_Structure" in s:
                rows.append([nm, s["H_Structure"], str(s.get("H_PC_N3"))])
            else:
                rows.append([nm, "--", esc(s.get("status", "--"))])
        loo = sens.get("SC_leave_one_category_out") or {}
        rows.append(["SC leave one category out", ", ".join(f"{VV.CAT.get(c, c)}: {v['H_Structure']}" for c, v in loo.items()),
                     ", ".join(sorted({str(v.get('H_PC_N3')) for v in loo.values()}))])
        val.table("TABLE_SENS", md_table(["Sensitivity", "H\\_Structure", "H\\_PC\\_N3 (or why not run)"], rows,
                                         ["l", "l", "l"]), [])
    # ---------------- bridge (descriptive; also without structure)
    B = ["descriptives", "D5_bridge"]
    br = put_or(val, "BR_P_RHO", "results", B + ["rho_P", "rho"], VV.r3)
    bn = val.put("BR_P_N", "results", B + ["rho_P", "n"], VV.i0)
    sh = put_or(val, "BR_SHIFT", "results", B + ["P_level_shift", "mean_t4_minus_t3"], VV.sf1)
    lo = put_or(val, "BR_SHIFT_LO", "results", B + ["P_level_shift", "ci90", 0], VV.sf1)
    hi = put_or(val, "BR_SHIFT_HI", "results", B + ["P_level_shift", "ci90", 1], VV.sf1)
    bc = put_or(val, "BR_C_RHO", "results", B + ["rho_C_star", "rho"], VV.r3)
    bcn = val.put("BR_C_N", "results", B + ["rho_C_star", "n"], VV.i0)
    fl = "; below the floor, descriptive" if V["descriptives"]["D5_bridge"]["rho_C_star"].get("below_n_floor") else ""
    val.word("BRIDGE_SENTENCE", f"Against the AIAS 2.0 legacy profile ($t_3$, six-model panel; printed beside, never "
             f"pooled), the within-category rank correlation of Presence was {br} ({bn} units), with a mean level shift "
             f"of {sh} points (90% interval {lo} to {hi}); for $C^*$ it was {bc} ({bcn} units{fl}), without a level "
             f"comparison (D5).", ["results"] + B, ["BR_P_RHO", "BR_P_N", "BR_SHIFT", "BR_SHIFT_LO", "BR_SHIFT_HI",
                                                     "BR_C_RHO", "BR_C_N"])
    # ---------------- appendix
    cl = Cells(val)
    rows = []
    for m in VV.ORDER:
        pk = ["descriptives", "D1_distributions", m, "all"]
        d = VV.jget(V, pk)
        if not d.get("n_rated"):
            rows.append([VV.NAME[m], "0", "--", "--", "--"])
            continue
        rows.append([VV.NAME[m], cl.f("results", pk + ["n_rated"], VV.i0), cl.f("results", pk + ["median"], VV.f1),
                     f"{cl.f('results', pk + ['q25'], VV.f1)} to {cl.f('results', pk + ['q75'], VV.f1)}",
                     f"{cl.f('results', pk + ['min'], VV.f1)} to {cl.f('results', pk + ['max'], VV.f1)}"])
    val.table("TABLE_D1", md_table(["Part", "Rated", "Median", "IQR", "Range"], rows), cl.cells)
    rpu = V["descriptives"]["D9_coverage"]["rated_parts_per_unit"]["K"]
    cl = Cells(val)
    rows = []
    for c in VV.SUBS:
        if c not in rpu:
            continue
        rows.append([VV.CAT[c]] + [cl.f("results", ["descriptives", "D9_coverage", "rated_parts_per_unit", "K", c, str(j)],
                                        VV.i0, missing="0") for j in range(len(K) + 1)])
    val.table("TABLE_D9", md_table(["Category"] + [str(j) for j in range(len(K) + 1)], rows), cl.cells)
    return val, cases, flags


# =========================================================================== checks and main
def deviations_text():
    rel = "osf/aias_6_0_preview/anchor/DEVIATIONS.md"
    if not DEVIATIONS.exists():
        raise FillError(f"{DEVIATIONS} not found (a locked file of {VV.EXPECTED_PREREG_TAG})")
    txt = DEVIATIONS.read_text(encoding="utf-8")
    cl = sorted({int(x) for x in re.findall(r"(?m)^\*\*C(\d+) —", txt)})
    after = re.findall(r"(?m)^## Entry ([1-9]\d*)\b", txt)
    n = len(after)
    crange = f"C{cl[0]}–C{cl[-1]}" if cl else "none"
    return (f"The deviations record (`{rel}`) holds Entry 0 and the clarifications {crange}, all written before the "
            f"lock, and {n} entr{'y' if n == 1 else 'ies'} after it.", [rel])


def tag_info():
    commit = VV.git_tag_commit()
    r = subprocess.run(["git", "-C", str(ROOT), "for-each-ref", "--format=%(taggerdate:iso-strict)",
                        f"refs/tags/{VV.EXPECTED_PREREG_TAG}"], capture_output=True, text=True)
    d = r.stdout.strip()
    return commit, (datetime.fromisoformat(d).strftime("%-d %B %Y") if d else None)


def verify_real(src):
    if VV.is_synthetic(src):
        raise FillError("the outputs are synthetic (synthetic_fixture, or MQ_Lock not verified): use --synthetic")
    V = src["results"]
    if V.get("prereg_tag") != VV.EXPECTED_PREREG_TAG:
        raise FillError(f"prereg_tag {V.get('prereg_tag')} != {VV.EXPECTED_PREREG_TAG}")
    commit, date = tag_info()
    if not commit:
        raise FillError(f"tag {VV.EXPECTED_PREREG_TAG} not found in {ROOT}")
    an = json.loads(ANCHOR.read_text(encoding="utf-8")) if ANCHOR.exists() else {}
    if an.get("commit") != commit:
        raise FillError(f"anchor {ANCHOR} missing or does not name {commit}")
    return commit, date


def fill(outputs, out=None, fig_dir=None, synthetic=False, class_c_draft=False, template=TEMPLATE):
    src = VV.load_sources(outputs)
    bad = VV.components_verified(src)
    if bad:
        raise FillError("component files are not the ones the scorer read: " + "; ".join(bad))
    if synthetic:
        if not VV.is_synthetic(src):
            raise FillError("--synthetic given but the outputs are not synthetic")
        c, d = tag_info()
        commit, date = (c[:10] if c else "synthetic run"), (d or "synthetic run")
    else:
        c, date = verify_real(src)
        commit = c[:10]
    check_consistency(src)
    if src["results"]["structure"]["wording_class"] == "C" and not class_c_draft:
        raise FillError("H_Structure FALSIFIED (class C): drafting pauses under the pre-registration (§6.6); write the "
                        "options memo for the author. --class-c-draft builds an internal draft for that memo only")
    fig_dir = fig_dir or "../../reports/figs/aias6"
    val, cases, flags = compute(src, synthetic, fig_dir, commit, date, deviations_text(), class_c_draft)
    text = render(Path(template).read_text(encoding="utf-8"), val.vals, cases, flags)
    if out:
        out = Path(out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
        prov = {"outputs": str(outputs), "synthetic": synthetic, "cases": cases, "flags": flags, "values": val.prov}
        Path(str(out).replace(".md", "_provenance.json")).write_text(
            json.dumps(prov, indent=1, ensure_ascii=False, default=str), encoding="utf-8")
    return text, val, cases, flags


def main(argv=None):
    ap = argparse.ArgumentParser(description="Fill the AIAS 6.0 Preview paper template from the scorer's outputs")
    ap.add_argument("--outputs", type=Path, default=VV.OUTDIR)
    ap.add_argument("--fig-dir", default=None)
    ap.add_argument("--out", type=Path, default=HERE / "aias_6_0_preview_paper_draft.md")
    ap.add_argument("--synthetic", action="store_true")
    ap.add_argument("--class-c-draft", action="store_true", help="class C only: an internal draft for the options memo")
    a = ap.parse_args(argv)
    if a.synthetic and str(a.out.resolve()).startswith(str(ROOT.resolve())):
        print("[fill aias6] REFUSED: synthetic output must be written outside the repository", file=sys.stderr)
        return 2
    try:
        text, val, cases, flags = fill(a.outputs, a.out, a.fig_dir, a.synthetic, a.class_c_draft)
    except (FillError, VV.Missing) as e:
        print(f"[fill aias6] REFUSED: {e}", file=sys.stderr)
        return 3
    print(f"[fill aias6] wrote {a.out} ({len(text.split())} words); cases {cases}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
