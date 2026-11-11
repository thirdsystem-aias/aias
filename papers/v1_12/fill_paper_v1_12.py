#!/usr/bin/env python3
"""
fill_paper_v1_12.py -- fills papers/v1_12/v1_12_ssrn_paper_template.md from the scorer's outputs.

The template holds the whole paper. Introduction and Method are fixed text written from PRE_REGISTRATION_v1_12.md
(r1, locked at tag v1.12-prereg-r1). Results and Discussion are written in advance as alternative sentences, one per
pre-registered outcome, inside blocks this script selects from the verdicts (template engine forked unchanged from
papers/v0_42/fill_paper_v0_42.py on branch t4-paper):

  {% switch CASE_GATE %} {% case PASS %} ... {% case MARGINAL|MARGINAL_H7 %} ... {% endswitch %}
  {% if FLAG %} ... {% else %} ... {% endif %}
  {{NAME}}      a value read from a machine output (papers/v1_12/v112_values.py records its JSON path)

Every switch must match exactly one case; an unknown flag or value is an error; the output may contain no
`{{`, `{%` or `%}`. No number is typed here: values are leaves of the verdicts JSON, the unit table or the locked N1
record, formatted by named functions; the provenance of every value is written beside the paper. Verdict words are
printed exactly as the scorer wrote them.

Checks before filling (real mode): the verdicts are not synthetic (parity gate P1 passed, no synthetic_fixture key),
P2 and P3 passed, prereg_tag == v1.12-prereg-r1, the tag exists in this repository, and the OSF anchor record
(osf/methodology/v1_12/anchor/osf_anchor_v1_12.json) names the tag's commit. Synthetic mode (--synthetic) skips the
tag and anchor checks, says so in the text, requires synthetic verdicts and refuses to write inside the repository.

Usage (real run, after `score_v1_12.py --run`; see papers/v1_12/PIPELINE.md):
  python3 papers/v1_12/fill_paper_v1_12.py
Synthetic test:
  python3 papers/v1_12/fill_paper_v1_12.py --synthetic \
      --verdicts papers/v1_12/tests/fixtures/SYNTHETIC_pass_v112_verdicts.json \
      --table papers/v1_12/tests/fixtures/SYNTHETIC_pass_v112_unit_table.csv \
      --fig-dir /tmp/v112_pipeline_test/figs --out /tmp/v112_pipeline_test/paper/v1_12_ssrn_paper_draft.md
"""
import argparse
import json
import math
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import v112_values as VV  # noqa: E402

ROOT = VV.ROOT
TEMPLATE = HERE / "v1_12_ssrn_paper_template.md"
ANCHOR = ROOT / "osf/methodology/v1_12/anchor/osf_anchor_v1_12.json"
DEVIATIONS = ROOT / "osf/methodology/v1_12/anchor/DEVIATIONS.md"


class FillError(RuntimeError):
    pass


# =========================================================================== template engine
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
    for bad in ("{{", "{%"):      # "}}" (LaTeX, \rho_{\text{pw}}) and "%}" (pandoc, {width=100%}) are legitimate
        if bad in body:
            raise FillError(f"unfilled template syntax {bad!r} in output")
    return body


# =========================================================================== tables
def md_table(header, rows, align=None):
    align = align or ["l"] + ["r"] * (len(header) - 1)
    vis = lambda t: len(re.sub(r"\$[^$]*\$|\\[a-z]+|[{}`]", "x", t))      # visible width, roughly
    widths = [max(4, min(60, max([vis(header[j])] + [vis(r[j]) for r in rows]))) for j in range(len(header))]
    widths[0] += 4                                   # first column (model / substrate names) never wraps
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


# =========================================================================== values
FAIL_WORDS = ("FALSIFIED",)


def _legs_with(V, legs, word):
    return [h for h in legs if V["verdicts"].get(h) == word]


def _plain(h):
    return {"H1_Sep_Presence": "Presence", "H2_Sep_Consistency": "Consistency",
            "H3_Sep_NamingRate": "the brand's own naming rate", "H4_Reliability": "split-half reliability",
            "H5_Sep_Ranking": "Ranking", "H6_Sep_Sentiment": "Sentiment"}[h]


def _short(hs):
    return VV.joinand(VV.LEG_SHORT[h] for h in hs)


def _verb(hs):
    return "were" if len(hs) > 1 else "was"


def _why(V, h):
    """Readable cause of an UNDETERMINED leg, from the scorer's own fields (never a new decision)."""
    leg = V["legs"][h]
    r = leg.get("reason") or ""
    if "left the panel" in r:
        gone = [m for m in VV.MODELS4 if m in r]
        return f"{VV.names(gone)} left the panel statistics under the drop rule"
    if "no locked score" in r:
        return "the leg was active but its locked score was not supplied"
    if leg.get("below_n_floor"):
        return (f"{leg.get('n')} units in {leg.get('n_categories')} categories with at least five entered, below the "
                f"floor of 30 units in three categories")
    return "its statistic was undefined on the data"


def compute(src, synthetic, fig_dir, prereg_commit, deviations):
    V = src["verdicts"]
    val = VV.Values(src)
    MC = ["MC"]
    gate_legs = list(V["paper_A_verdict"]["legs"])                      # the legs the scorer's gate used
    cases = {"CASE_GATE": VV.case_gate(V), "CASE_MSIT": "PASSED" if V["MC"]["MC_Situation"]["passed"] else "FAILED",
             "CASE_H5": VV.case_h5(V), "CASE_H6": VV.case_h6(V),
             "CASE_PARITY": "SYNTHETIC" if synthetic else "PASSED"}
    for h in VV.GATE_LEGS + VV.SEC_LEGS:
        cases[f"CASE_{VV.LEG_SHORT[h]}"] = VV.case_leg(V, h)
    flags = {}
    val.word("PREREG_TAG", V["prereg_tag"], ["verdicts", "prereg_tag"])
    val.word("PREREG_COMMIT", prereg_commit, ["git", f"refs/tags/{VV.EXPECTED_PREREG_TAG}"])
    val.word("FIG_DIR", str(fig_dir), ["argument --fig-dir"])
    val.word("FIG_CAPTION", "SYNTHETIC TEST DATA --- NOT RESULTS." if synthetic else "",
             ["synthetic flag"])
    val.word("DEV_SENTENCE", deviations[0], deviations[2])
    val.word("DEV_STATUS", deviations[1], deviations[2])
    val.word("PRIMARY", V["primary_panel"], ["verdicts", "primary_panel"])

    # ---------------- calibration N1 (locked record)
    st = ["statistic_r1"]
    val.put("N1_UNITS", "n1", st + ["n_units"], VV.i0)
    val.put("N1_CATS", "n1", st + ["n_categories"], VV.i0)
    val.put("N1_RHO", "n1", st + ["pooled_centred_rho_w"], VV.r4s)
    val.put("N1_DEC", "n1", st + ["max_abs_decile_deviation_from_50"], VV.r2)
    val.word("N1_RESULT", src["n1"]["statistic_r1"]["result"], ["n1", "statistic_r1", "result"])

    # ---------------- parity and checks
    pg = V["parity_gates"]
    val.word("P2_STATUS", "passed" if pg["P2"].get("passed") else str(pg["P2"].get("status") or "did not pass"),
             ["verdicts", "parity_gates", "P2"])
    val.word("P3_STATUS", "passed" if pg["P3"].get("passed") else "did not pass", ["verdicts", "parity_gates", "P3"])
    mcc = V["MC"]["MC_Complete"]
    val.put("MC_ANSWERED", "verdicts", MC + ["MC_Complete", "answered"], VV.i0)
    val.put("MC_EXPECTED", "verdicts", MC + ["MC_Complete", "expected"], VV.i0)
    val.put("MC_SHARE", "verdicts", MC + ["MC_Complete", "share"], VV.pct1)
    flags["MC_COMPLETE_PASS"] = bool(mcc["pass"])
    dropped = V.get("models_dropped_section_7_3") or []
    flags["ANY_DROPPED"] = bool(dropped)
    parts = []
    for m in dropped:
        a = val.put(f"DROP_{m}", "verdicts", MC + ["MC_Complete", "per_model", m, "answered"], VV.i0)
        parts.append(f"{VV.MODEL_NAME.get(m, m)} ({a} of 225 answered)")
    val.word("DROPPED_SENTENCE", ("Under the drop rule (§2.7) the following left the panel statistics: "
                                  + "; ".join(parts) + ".") if parts else "", ["verdicts", "models_dropped_section_7_3"])
    val.word("DROPPED_NAMES", VV.names(dropped) or "no model", ["verdicts", "models_dropped_section_7_3"])
    srv = V["MC"]["MC_Served"]
    flags["MC_SERVED_PASS"] = bool(srv["pass"])
    val.put("MC_SERVED_N", "verdicts", MC + ["MC_Served", "n_mismatched"], VV.i0)
    mset = V["MC"]["MC_Settings"]
    flags["MC_SETTINGS_PASS"] = bool(mset.get("pass"))
    val.put("MC_SETTINGS_MISSING", "verdicts", MC + ["MC_Settings", "records_without_recorded_settings"], VV.i0)
    mct = V["MC"]["MC_Truncation"]
    tparts = []
    for m in VV.MODELS4:
        if (mct.get(m) or {}).get("flag_above_5pct"):
            s = val.put(f"TRUNC_{m}", "verdicts", MC + ["MC_Truncation", m, "share"], VV.pct1)
            tparts.append(f"{VV.MODEL_NAME[m]} ({s} of calls at the cap)")
    flags["MCT_ANY_FLAG"] = bool(tparts)
    val.word("MCT_FLAGGED", "; ".join(tparts), ["verdicts", "MC", "MC_Truncation"])
    win = V["MC"]["MC_Window"]
    for k, key in (("WIN_FIRST", "first_call_utc"), ("WIN_LAST", "last_call_utc")):
        val.word(k, str(win.get(key))[:16].replace("T", " "), ["verdicts", "MC", "MC_Window", key])
    val.put("WIN_SPAN", "verdicts", MC + ["MC_Window", "span_hours"], VV.f1)
    flags["WIN_PASS"] = bool(win.get("pass"))
    val.put("SPEND_TOTAL", "verdicts", ["descriptives", "tokens_and_spend", "total_usd"], VV.usd2)
    rs = V["MC"]["MC_RegistryShare"]
    rflag = [VV.CAT[s] for s in VV.SUBS if (rs.get(s) or {}).get("flag_below_0_50")]
    flags["REGSHARE_ANY_FLAG"] = bool(rflag)
    val.word("REGSHARE_FLAGGED", VV.joinand(rflag), ["verdicts", "MC", "MC_RegistryShare"])
    val.derive("REGSHARE_MIN", VV.d_min, [("verdicts", MC + ["MC_RegistryShare", s, "share_naming_registry_brand"])
                                          for s in VV.SUBS if s in rs], VV.pct0)
    dft = V["MC"]["MC_Defunct"]
    flags["DEFUNCT_FLAG"] = bool(dft.get("flagged"))
    val.put("DEFUNCT_SHARE", "verdicts", MC + ["MC_Defunct", "share_naming_any"], VV.pct1)
    pos = V["MC"]["MC_Positive"]
    flags["POSITIVE_FLAG"] = bool(pos.get("flagged"))
    val.put("POSITIVE_RHO", "verdicts", MC + ["MC_Positive", "rho_w_raw_cov_pi_cov"], VV.r3)
    dz = V["delta_fits"]["set_to_zero"]
    if dz:
        n = val.put("DELTA_ZERO", "verdicts", ["delta_fits", "set_to_zero"], VV.i0)
        val.word("DELTA_SENTENCE", f"{n} brand × model fits of the situation effects did not converge or had no "
                                   f"informative brand and used $\\delta = 0$ (§2.4).", ["verdicts", "delta_fits"])
    else:
        val.word("DELTA_SENTENCE", "Every leave-one-out fit of the situation effects converged (§2.4).",
                 ["verdicts", "delta_fits"])
    cl = Cells(val)
    rows = []
    st_ = V["MC"]["MC_Settings"].get("reasoning_tokens_per_model") or {}
    for m in VV.MODELS4:
        pk = MC + ["MC_Complete", "per_model", m]
        rows.append([VV.MODEL_NAME[m], cl.f("verdicts", pk + ["answered"], VV.i0),
                     cl.f("verdicts", pk + ["share"], VV.pct1),
                     cl.f("verdicts", MC + ["MC_Settings", "reasoning_tokens_per_model", m, "reasoning_tokens_mean"],
                          VV.i0) if m in st_ else "--",
                     cl.f("verdicts", MC + ["MC_Truncation", m, "share"], VV.pct1),
                     "dropped" if m in dropped else "kept"])
    val.table("TABLE_MC", md_table(["Model", "Answered", "Share", "Reasoning tokens (mean)", "At output cap",
                                    "Drop rule"], rows), cl.cells)

    # ---------------- MC_Situation
    ms = MC + ["MC_Situation"]
    val.put("MSIT_CELLS", "verdicts", ms + ["cells_used"], VV.i0)
    val.put("MSIT_JW", "verdicts", ms + ["pooled_mean_J_within"], VV.r3)
    val.put("MSIT_JB", "verdicts", ms + ["pooled_mean_J_between"], VV.r3)
    val.put("MSIT_DIFF", "verdicts", ms + ["pooled_mean_J_within_minus_J_between"], VV.r3)
    val.put("MSIT_C0", "verdicts", ms + ["mean_J_with_C0"], VV.r3)

    # ---------------- legs
    rated = sum(1 for r in src["table"]["rows"] if str(r.get("rated")) == "1")
    val.word("RATED_N", str(rated), ["table", "rows", "rated == 1 (count)"])
    for h in VV.ALL_LEGS:
        k = VV.LEG_SHORT[h]
        leg = V["legs"][h]
        lp = ["legs", h]
        val.word(f"{k}_WORD", leg["verdict"], ["verdicts"] + lp + ["verdict"])
        val.word(f"{k}_WHY", _why(V, h) if leg["verdict"] == "UNDETERMINED" else "", ["verdicts"] + lp)
        if VV.has(leg, ["rho_w"]):
            val.put(f"{k}_RHO", "verdicts", lp + ["rho_w"], VV.r3)
            val.put(f"{k}_N", "verdicts", lp + ["n"], VV.i0)
            val.put(f"{k}_NCAT", "verdicts", lp + ["n_categories"], VV.i0)
        else:
            for s in ("RHO", "N", "NCAT"):
                val.word(f"{k}_{s}", "--", ["verdicts"] + lp + ["(not computed)"])
        if VV.has(leg, ["n"]) and not VV.has(leg, ["rho_w"]):
            val.put(f"{k}_N", "verdicts", lp + ["n"], VV.i0)
            val.put(f"{k}_NCAT", "verdicts", lp + ["n_categories"], VV.i0)
        val.word(f"{k}_P", VV.p4(leg["p_perm"]) if VV.has(leg, ["p_perm"]) else "--", ["verdicts"] + lp + ["p_perm"])
        if VV.has(leg, ["p_perm"]):
            val.put(f"{k}_P", "verdicts", lp + ["p_perm"], VV.p4)
        if VV.has(leg, ["ci95_rho_w"]):
            val.put(f"{k}_CI_LO", "verdicts", lp + ["ci95_rho_w", 0], VV.r3)
            val.put(f"{k}_CI_HI", "verdicts", lp + ["ci95_rho_w", 1], VV.r3)
        else:
            val.word(f"{k}_CI_LO", "--", ["verdicts"] + lp)
            val.word(f"{k}_CI_HI", "--", ["verdicts"] + lp)
    h4 = V["legs"]["H4_Reliability"]
    if VV.has(h4, ["transformed"]):
        val.put("H4_REL", "verdicts", ["legs", "H4_Reliability", "transformed"], VV.r3)
    else:
        val.word("H4_REL", "not computed", ["verdicts", "legs", "H4_Reliability"])
    if VV.has(h4, ["ci95_transformed"]):
        val.put("H4_REL_LO", "verdicts", ["legs", "H4_Reliability", "ci95_transformed", 0], VV.r3)
        val.put("H4_REL_HI", "verdicts", ["legs", "H4_Reliability", "ci95_transformed", 1], VV.r3)
    else:
        val.word("H4_REL_LO", "--", ["verdicts", "legs", "H4_Reliability"])
        val.word("H4_REL_HI", "--", ["verdicts", "legs", "H4_Reliability"])
    flags["H7_DOWNGRADES"] = V["verdicts"].get("H7_Sep_Presence_Legacy") == "FALSIFIED"
    h5src = V.get("H5_ranking_source") or {}
    val.word("H5_STAGE1", str(h5src.get("stage1_verdict") or "not available"), ["verdicts", "H5_ranking_source"])
    if cases["CASE_H5"] == "UNAVAILABLE":
        val.word("H5_WHY", str(h5src.get("reason") or "no Stage 1 output"), ["verdicts", "H5_ranking_source", "reason"])
    comp = V.get("comparators") or {}
    flags["CROSS_PANEL"] = bool(comp.get("cross_panel"))
    val.word("CROSS_REASON", str(comp.get("reason") or ""), ["verdicts", "comparators", "reason"])

    cl = Cells(val)
    rows = []
    for h in VV.ALL_LEGS:
        leg, lp = V["legs"][h], ["legs", h]
        ci = (f"[{cl.f('verdicts', lp + ['ci95_rho_w', 0], VV.r3)}, {cl.f('verdicts', lp + ['ci95_rho_w', 1], VV.r3)}]"
              if VV.has(leg, ["ci95_rho_w"]) else "--")
        tier = "gate" if h in gate_legs else ("conditional" if h in VV.COND_LEGS else "secondary")
        if h in VV.COND_LEGS and h not in gate_legs and leg["verdict"] != "INACTIVE":
            tier = "reported, not gating"
        rows.append([f"{VV.LEG_SHORT[h]}", VV.LEG_AGAINST[h], tier, cl.f("verdicts", lp + ["n"], VV.i0),
                     cl.f("verdicts", lp + ["rho_w"], VV.r3), ci, cl.f("verdicts", lp + ["p_perm"], VV.p4),
                     f"**{leg['verdict']}**"])
    val.table("TABLE_LEGS", md_table(["Leg", "Cov* against", "Role", "$n$", "$\\rho_w$", "95% interval",
                                      "$p_{\\text{perm}}$", "Verdict"], rows,
                                     ["l", "l", "l", "r", "r", "r", "r", "l"]), cl.cells)

    # ---------------- gate
    g = V["paper_A_verdict"]
    val.word("GATE_LABEL", g["label"], ["verdicts", "paper_A_verdict", "label"])
    val.word("GATE_LEG_LIST", _short(gate_legs), ["verdicts", "paper_A_verdict", "legs"])
    for w, key in (("FALSIFIED", "FAIL"), ("MARGINAL", "MARGINAL"), ("UNDETERMINED", "UNDET")):
        hs = [h for h in gate_legs if g["legs"].get(h) == w]
        val.word(f"{key}_LEGS", _short(hs), ["verdicts", "paper_A_verdict", "legs"])
        val.word(f"{key}_VERB", _verb(hs), ["verdicts", "paper_A_verdict", "legs"])
        plain = VV.joinand(f"{_plain(h)} ({VV.LEG_SHORT[h]})" for h in hs)
        val.word(f"{key}_LEGS_PLAIN", plain, ["verdicts", "paper_A_verdict", "legs"])
    rep = V.get("gate_repeated_on") or {}
    for name in ("C3", "A4"):
        val.word(f"GATE_{name}", (rep.get(name) or {}).get("gate", {}).get("label", "not computed (primary panel)"),
                 ["verdicts", "gate_repeated_on", name, "gate", "label"])

    # ---------------- sensitivities
    S = V.get("sensitivities") or {}
    cl = Cells(val)
    rows = []
    for key, label in VV.SENS:
        if key not in S:
            continue
        cells = [label]
        for h in VV.GATE_LEGS:
            p = ["sensitivities", key, "rho_w", h]
            if not VV.has(V, p):
                cells.append("--")
                continue
            s = cl.f("verdicts", p, VV.r3)
            vc = (S[key].get("verdict_changes") or {}).get(h)
            cells.append(s + (f" ({vc[1]})" if vc else ""))
        rows.append(cells)
    val.table("TABLE_SENS", md_table(["Sensitivity"] + [VV.LEG_SHORT[h] for h in VV.GATE_LEGS], rows), cl.cells)
    ch = V.get("verdict_changes_under_sensitivities") or {}
    if ch:
        val.word("SENS_CHANGES_SENTENCE",
                 "A verdict would differ under " + VV.joinand(sorted({k.split("_")[0] for k in ch}, key=lambda x: int(x[1:]))) +
                 " (marked in the table; for S5 and S6 the changes are listed in the verdict file); the primary "
                 "verdicts stand.", ["verdicts", "verdict_changes_under_sensitivities"])
    else:
        val.word("SENS_CHANGES_SENTENCE", "No sensitivity analysis would change a verdict.",
                 ["verdicts", "verdict_changes_under_sensitivities"])
    rng = ["sensitivities", "S5_leave_one_category_out", "rho_w_range"]
    for h, k in (("H1_Sep_Presence", "H1"), ("H3_Sep_NamingRate", "H3")):
        if VV.has(V, rng + [h]):
            val.put(f"S5_{k}_LO", "verdicts", rng + [h, 0], VV.r3)
            val.put(f"S5_{k}_HI", "verdicts", rng + [h, 1], VV.r3)
        else:
            val.word(f"S5_{k}_LO", "--", ["verdicts"] + rng)
            val.word(f"S5_{k}_HI", "--", ["verdicts"] + rng)
    s6 = (S.get("S6_leave_one_W_out") or {}).get("verdict_changes") or {}
    val.word("S6_SENTENCE", ("Leaving out one cue type (S6) would change a verdict when " + VV.joinand(
        f"*{w}*" for w in s6) + " is left out.") if s6 else "Leaving out any one cue type (S6) changes no verdict.",
        ["verdicts", "sensitivities", "S6_leave_one_W_out", "verdict_changes"])
    s7 = S.get("S7_presence_alternatives") or {}
    p7 = ["sensitivities", "S7_presence_alternatives"]
    if VV.has(V, p7 + ["pi_hat_N3", "rho_w", "H1_Sep_Presence"]):
        a = val.put("S7_PI", "verdicts", p7 + ["pi_hat_N3", "rho_w", "H1_Sep_Presence"], VV.r3)
        b = val.put("S7_MEN", "verdicts", p7 + ["t4_mentions_N3_S0", "rho_w", "H1_Sep_Presence"], VV.r3)
        val.word("S7_SENTENCE", f"With recall $\\hat\\pi_{{N3}}$ or total $t_4$ mentions in place of $P_{{N3}}$ (S7), "
                                f"H1's $\\rho_w$ was {a} and {b}.", ["verdicts"] + p7)
    else:
        val.word("S7_SENTENCE", "S7 was not computed: " + str((s7.get("pi_hat_N3") or {}).get("reason") or
                                                               "comparators not available") + ".", ["verdicts"] + p7)

    # ---------------- baseline
    D = ["descriptives"]
    pr = V["primary_panel"]
    cl = Cells(val)
    rows = []
    for s in VV.SUBS:
        pk = D + ["per_category_panel", f"{s}|{pr}"]
        rows.append([VV.CAT_SHORT[s], cl.f("verdicts", pk + ["units"], VV.i0), cl.f("verdicts", pk + ["rated"], VV.i0),
                     cl.f("verdicts", pk + ["cov_star", "median"], VV.f1),
                     f"{cl.f('verdicts', pk + ['cov_star', 'q1'], VV.f1)}--{cl.f('verdicts', pk + ['cov_star', 'q3'], VV.f1)}",
                     cl.f("verdicts", pk + ["raw_cov_k2", "median"], VV.f1),
                     cl.f("verdicts", pk + ["share_of_ceps_no_registry_brand_in_any_panel_answer"], VV.pct0)])
    val.table("TABLE_BASE", md_table(["Category", "Brands", "Rated", "Cov* median", "Cov* IQR", "Raw Cov median",
                                      "CEPs, no brand"], rows), cl.cells)
    refs = [("verdicts", D + ["per_category_panel", f"{s}|{pr}", "cov_star", "median"]) for s in VV.SUBS]
    lo = val.derive("BASE_MED_MIN", VV.d_min, refs, VV.f1)
    hi = val.derive("BASE_MED_MAX", VV.d_max, refs, VV.f1)
    val.word("BASE_SENTENCE", f"Median Cov* ranged from {lo} to {hi} across categories.",
             ["verdicts"] + D + ["per_category_panel"])
    rr = [("verdicts", D + ["run_to_run_reliability", m, "rel1"]) for m in VV.MODELS4
          if VV.has(V, D + ["run_to_run_reliability", m, "rel1"])]
    val.derive("REL1_MIN", VV.d_min, rr, VV.r3)
    val.derive("REL1_MAX", VV.d_max, rr, VV.r3)
    bp = [("verdicts", D + ["per_category_model", f"{s}|{m}", "registry_brands_named_per_cep_answer_mean"])
          for s in VV.SUBS for m in VV.MODELS4
          if VV.has(V, D + ["per_category_model", f"{s}|{m}", "registry_brands_named_per_cep_answer_mean"])]
    val.derive("BRANDS_MIN", VV.d_min, bp, VV.f1)
    val.derive("BRANDS_MAX", VV.d_max, bp, VV.f1)

    # ---------------- appendix: section 5 descriptives
    cl = Cells(val)
    rows = []
    for s in VV.SUBS:
        for m in VV.MODELS4:
            pk = D + ["per_category_model", f"{s}|{m}"]
            if not VV.has(V, pk):
                continue
            rows.append([VV.CAT_SHORT[s] if m == VV.MODELS4[0] else "", VV.MODEL_NAME[m],
                         cl.f("verdicts", pk + ["cep_answers"], VV.i0), cl.f("verdicts", pk + ["missing_cells"], VV.i0),
                         cl.f("verdicts", pk + ["words_per_answer_mean"], VV.i0),
                         cl.f("verdicts", pk + ["registry_brands_named_per_cep_answer_mean"], VV.f1),
                         cl.f("verdicts", pk + ["share_of_ceps_with_no_registry_brand"], VV.pct0),
                         cl.f("verdicts", pk + ["mean_jaccard_cep_answer_vs_C0"], VV.r2),
                         cl.f("verdicts", pk + ["beta_distribution", "median"], VV.r2)])
    val.table("TABLE_DESC", md_table(["Category", "Model", "CEP answers", "Missing", "Words", "Brands per answer",
                                      "CEPs, no brand", "Jaccard with C0", "Median $\\beta$"], rows,
                                     ["l", "l", "r", "r", "r", "r", "r", "r", "r"]), cl.cells)
    pw = V["descriptives"].get("per_W_coverage_primary_panel") or {}
    rows = []
    for s in VV.SUBS:
        units = [u for u in pw if u.split("|")[0] == s]
        cells = [VV.CAT_SHORT[s]]
        for w in VV.W_TYPES:
            refs = [("verdicts", D + ["per_W_coverage_primary_panel", u, w]) for u in units]
            cells.append(val.derive(f"PERW_{s}_{w}", VV.d_mean, refs, VV.r2) if refs else "--")
        rows.append(cells)
    val.table("TABLE_PERW", md_table(["Category"] + [w for w in VV.W_TYPES], rows), [])
    cl = Cells(val)
    rows = []
    for m in VV.MODELS4:
        rk = D + ["run_to_run_reliability", m]
        sk = D + ["tokens_and_spend", "per_model", m]
        rows.append([VV.MODEL_NAME[m], cl.f("verdicts", rk + ["rel1"], VV.r3), cl.f("verdicts", rk + ["rel3"], VV.r3),
                     cl.f("verdicts", sk + ["records"], VV.i0), cl.f("verdicts", sk + ["input_tokens"], VV.i0),
                     cl.f("verdicts", sk + ["output_tokens"], VV.i0), cl.f("verdicts", sk + ["thinking_tokens"], VV.i0),
                     cl.f("verdicts", sk + ["usd_billed"], VV.usd2)])
    rows.append(["All", "", "", "", "", "", "", cl.f("verdicts", D + ["tokens_and_spend", "total_usd"], VV.usd2)])
    val.table("TABLE_RELCOST", md_table(["Model", "rel1", "rel3", "Records", "Input tokens", "Output tokens",
                                         "Reasoning tokens", "US\\$"], rows), cl.cells)
    return val, cases, flags


# =========================================================================== checks and main
def deviations_text(synthetic):
    if synthetic:
        t = "[Synthetic test run: the deviations record was not read.]"
        return t, t, ["synthetic"]
    if not DEVIATIONS.exists():
        raise FillError(f"{DEVIATIONS} not found (it is a locked file of v1.12-prereg-r1)")
    txt = DEVIATIONS.read_text(encoding="utf-8")
    n = len(re.findall(r"(?m)^- \*\*\d{4}-\d{2}-\d{2}", txt))
    rel = "osf/methodology/v1_12/anchor/DEVIATIONS.md"
    return (f"Deviations are recorded in `{rel}` ({n} dated entries), each before the step it concerns.",
            f"deviations recorded in `{rel}` ({n} dated entries).", [rel])


def verify_real(V):
    if VV.is_synthetic(V):
        raise FillError("verdicts come from a synthetic run (parity gate P1 not passed or synthetic_fixture present); "
                        "use --synthetic")
    pg = V.get("parity_gates") or {}
    if not all((pg.get(g) or {}).get("passed") is True for g in ("P1", "P3")):
        raise FillError(f"parity gates P1/P3 not passed: {json.dumps(pg)[:400]}")
    if not (pg.get("P2") or {}).get("passed") and not (V.get("comparators") or {}).get("cross_panel"):
        raise FillError("parity gate P2 not passed and the comparators are not the declared fallback")
    if V.get("prereg_tag") != VV.EXPECTED_PREREG_TAG:
        raise FillError(f"prereg_tag {V.get('prereg_tag')} != {VV.EXPECTED_PREREG_TAG}")
    bf = (V.get("MC") or {}).get("MC_BrandFree") or {}
    if bf.get("passed") is not True or bf.get("hits"):
        raise FillError(f"MC_BrandFree record not passed in the verdicts (Method §2.1 states 0 hits): {bf}")
    commit = VV.git_tag_commit()
    if not commit:
        raise FillError(f"tag {VV.EXPECTED_PREREG_TAG} not found in {ROOT}")
    if not ANCHOR.exists() or commit not in ANCHOR.read_text(encoding="utf-8"):
        raise FillError(f"anchor {ANCHOR} missing or does not name {commit}")
    return commit[:10]


def fill(verdicts, table, out=None, fig_dir=None, synthetic=False, n1=None, template=TEMPLATE):
    src = VV.load_sources(verdicts, table, n1)
    V = src["verdicts"]
    if synthetic:
        if not VV.is_synthetic(V):
            raise FillError("--synthetic given but the verdicts are not from a synthetic run")
        if V.get("prereg_tag") != VV.EXPECTED_PREREG_TAG:
            raise FillError(f"prereg_tag {V.get('prereg_tag')} != {VV.EXPECTED_PREREG_TAG}")
        commit = "synthetic run: tag not verified"
    else:
        commit = verify_real(V)
    fig_dir = fig_dir or "../../reports/figs/v112"
    val, cases, flags = compute(src, synthetic, fig_dir, commit, deviations_text(synthetic))
    tpl = Path(template).read_text(encoding="utf-8")
    text = render(tpl, val.vals, cases, flags)
    if out:
        out = Path(out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
        prov = {"verdicts": str(verdicts), "table": str(table), "synthetic": synthetic, "cases": cases, "flags": flags,
                "values": val.prov}
        Path(str(out).replace(".md", "_provenance.json")).write_text(
            json.dumps(prov, indent=1, ensure_ascii=False, default=str), encoding="utf-8")
    return text, val, cases, flags


def main(argv=None):
    ap = argparse.ArgumentParser(description="Fill the v1.12 Coverage Paper A template from the scorer's outputs")
    ap.add_argument("--verdicts", type=Path, default=ROOT / "osf/methodology/v1_12/v112_verdicts.json")
    ap.add_argument("--table", type=Path, default=ROOT / "osf/methodology/v1_12/v112_unit_table.csv")
    ap.add_argument("--fig-dir", default=None, help="figure directory as the paper references it "
                                                     "(default ../../reports/figs/v112, relative to papers/v1_12)")
    ap.add_argument("--out", type=Path, default=HERE / "v1_12_ssrn_paper_draft.md")
    ap.add_argument("--synthetic", action="store_true")
    a = ap.parse_args(argv)
    if a.synthetic and str(a.out.resolve()).startswith(str(ROOT.resolve())):
        sys.exit("[fill v1.12] REFUSED: synthetic output must be written outside the repository")
    try:
        text, val, cases, flags = fill(a.verdicts, a.table, a.out, a.fig_dir, a.synthetic)
    except (FillError, VV.Missing) as e:
        print(f"[fill v1.12] REFUSED: {e}", file=sys.stderr)
        return 3
    print(f"[fill v1.12] wrote {a.out} ({len(text.split())} words); cases {cases}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
