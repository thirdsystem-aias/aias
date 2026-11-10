#!/usr/bin/env python3
"""
fill_paper_v0_42.py -- fills papers/v0_42/v0_42_ssrn_paper_template.md from the scorer's outputs.

The template holds the whole paper. Introduction and Method are fixed text written from PRE_REGISTRATION_v0_42.md
(r2 with clarifications C1-C26). Results and Discussion are written in advance as alternative sentences, one per
pre-registered outcome, inside blocks this script selects from the verdicts:

  {% switch CASE_GEN %} {% case CONFIRMED %} ... {% case MARGINAL|FALSIFIED %} ... {% endswitch %}
  {% if FLAG %} ... {% else %} ... {% endif %}
  {{NAME}}      a value read from a machine output (papers/v0_42/v42_values.py records its JSON path)

Every switch must match exactly one case; an unknown flag or value is an error; the output may contain no
`{{`, `{%` or `%}`. No number is typed here: values are leaves of the verdicts JSON (or of the other machine outputs
listed in v42_values.py), formatted by named functions; the provenance of every value is written beside the paper.

Checks before filling (real mode): verdicts written by the real run (MC_Parity passed, gates P1-P3 true, not the
synthetic flag), prereg_tag == v0.42-prereg-r1, the tag exists in this repository and the OSF anchor record
(osf/v42/anchor/osf_anchor_v0_42.json) names the tag's commit. Synthetic mode (--synthetic) skips the tag and anchor
checks, marks them as unverified in the text, and requires the verdicts to be synthetic.

Usage (real run, after `score_v0_42.py --run`; see papers/v0_42/PIPELINE.md):
  python3 papers/v0_42/fill_paper_v0_42.py
Synthetic test:
  python3 papers/v0_42/fill_paper_v0_42.py --synthetic --verdicts DIR/_score/v42_verdicts.json \
      --table DIR/_score/v42_brand_table.csv --fig-dir /tmp/t4_pipeline_test/figs \
      --out /tmp/t4_pipeline_test/paper/v0_42_ssrn_paper_draft.md
"""
import argparse
import json
import math
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import v42_values as VV  # noqa: E402

ROOT = VV.ROOT
TEMPLATE = HERE / "v0_42_ssrn_paper_template.md"
ANCHOR = ROOT / "osf/v42/anchor/osf_anchor_v0_42.json"
DEVIATIONS = ROOT / "osf/v42/DEVIATIONS.md"


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
def _ok(h, *keys):
    return all(VV.has(h, [k]) for k in keys)


def compute(src, synthetic, fig_dir, prereg_commit, deviations):
    V = src["verdicts"]
    val = VV.Values(src)
    MC = ["manipulation_checks"]
    cases = {"CASE_GEN": VV.case_gen(V), "CASE_PHI": VV.case_phi(V), "CASE_SEARCH": VV.case_search(V),
             "CASE_PARITY": "SYNTHETIC" if synthetic else "PASSED"}
    flags = {}
    val.word("PREREG_TAG", V["prereg_tag"], ["verdicts", "prereg_tag"])
    val.word("PREREG_COMMIT", prereg_commit, ["git", f"refs/tags/{VV.EXPECTED_PREREG_TAG}"])
    val.word("FIG_DIR", str(fig_dir), ["argument --fig-dir"])
    val.word("DEV_SENTENCE", deviations[0], deviations[2])
    val.word("DEV_STATUS", deviations[1], deviations[2])

    # ---------------- background (v0.41, locked at tag v0.41-scoring-locked)
    ps41 = ["verdicts", "H_Presence_LongHorizon", "per_substrate"]
    refs = [("v41", ps41 + [s, "rho"]) for s in VV.SUBS]
    val.derive("V41_PI_MIN", VV.d_min, refs, VV.r2)
    val.derive("V41_PI_MAX", VV.d_max, refs, VV.r2)
    val.put("V41_PHI_RHO", "v41", ["verdicts", "H_Phi_LongHorizon", "rho"], VV.r3)
    val.put("V41_PHI_N", "v41", ["verdicts", "H_Phi_LongHorizon", "n"], VV.i0)

    # ---------------- manipulation checks
    mcc = V["manipulation_checks"]["MC_Complete"]
    val.put("MC_ANSWERED", "verdicts", MC + ["MC_Complete", "answered"], VV.i0)
    val.put("MC_EXPECTED", "verdicts", MC + ["MC_Complete", "expected"], VV.i0)
    val.put("MC_SHARE", "verdicts", MC + ["MC_Complete", "share"], VV.pct1)
    flags["MC_COMPLETE_PASS"] = bool(mcc["pass"])
    excl = V.get("models_excluded_condition") or []
    flags["ANY_EXCLUDED"] = bool(excl)
    parts = []
    for i, k in enumerate(excl):
        m, c = k.split("|")
        a = val.put(f"EXCL_{i}_ANS", "verdicts", MC + ["MC_Complete", "per_model_condition", k, "answered"], VV.i0)
        e = val.put(f"EXCL_{i}_EXP", "verdicts", MC + ["MC_Complete", "per_model_condition", k, "expected"], VV.i0)
        parts.append(f"{VV.MODEL_NAME.get(m, m)} with {VV.COND_NAME[c]} ({a} of {e} answered)")
    val.word("EXCLUDED_SENTENCE", ("Under the drop rule (§2.9) the following were excluded from their condition's panel "
                                   "statistics: " + "; ".join(parts) + ".") if parts else "",
             ["verdicts", "models_excluded_condition"])
    val.word("EXCL_S0_NAMES", VV.names(VV.excluded_models(V, "S0")) or "no model", ["verdicts", "models_excluded_condition"])
    srv = V["manipulation_checks"]["MC_Served"]
    flags["MC_SERVED_PASS"] = bool(srv["pass"])
    val.put("MC_SERVED_N", "verdicts", MC + ["MC_Served", "n_mismatched"], VV.i0)
    if srv.get("ok_calls_without_served_id"):
        n = val.put("MC_NOID", "verdicts", MC + ["MC_Served", "ok_calls_without_served_id"], VV.i0)
        val.word("MC_NOID_SENTENCE", f"{n} answered calls recorded no served model ID; they are listed, not excluded.",
                 ["verdicts", "manipulation_checks", "MC_Served", "ok_calls_without_served_id"])
    else:
        val.word("MC_NOID_SENTENCE", "", ["verdicts", "manipulation_checks", "MC_Served", "ok_calls_without_served_id"])
    flags["MC_OUTSIDE_ANY"] = bool(mcc["outside_design"]["n"])
    val.put("MC_OUTSIDE", "verdicts", MC + ["MC_Complete", "outside_design", "n"], VV.i0)
    mcs = V["manipulation_checks"]["MC_Search"]
    flagged = [m for m in VV.N3 if (mcs.get(m) or {}).get("flag_search_rarely_used")]
    flags["MCS_ANY_FLAG"] = bool(flagged)
    val.word("MCS_FLAGGED", VV.names(flagged), ["verdicts", "manipulation_checks", "MC_Search"])
    mct = V["manipulation_checks"]["MC_Truncation"]
    tparts = []
    for k in sorted(mct):
        if mct[k].get("flag_above_5pct"):
            m, c = k.split("|")
            s = val.put(f"TRUNC_{len(tparts)}", "verdicts", MC + ["MC_Truncation", k, "share"], VV.pct1)
            tparts.append(f"{VV.MODEL_NAME.get(m, m)} with {VV.COND_NAME[c]} ({s})")
    flags["MCT_ANY_FLAG"] = bool(tparts)
    val.word("MCT_FLAGGED", "; ".join(tparts), ["verdicts", "manipulation_checks", "MC_Truncation"])
    win = V["manipulation_checks"]["MC_Window"]
    val.word("WIN_FIRST", str(win.get("first_call_utc")).replace("T", " ").replace("+00:00", ""),
             ["verdicts", "manipulation_checks", "MC_Window", "first_call_utc"])
    val.word("WIN_LAST", str(win.get("last_call_utc")).replace("T", " ").replace("+00:00", ""),
             ["verdicts", "manipulation_checks", "MC_Window", "last_call_utc"])
    if VV.has(win, ["span_hours"]):
        val.put("WIN_SPAN", "verdicts", MC + ["MC_Window", "span_hours"], VV.f1)
    else:
        val.word("WIN_SPAN", "an unknown number of", ["verdicts", "manipulation_checks", "MC_Window", "span_hours"])
    flags["WIN_PASS"] = bool(win.get("pass"))
    val.put("COST_TOTAL", "verdicts", ["descriptives", "6_cost", "total_usd"], VV.usd2)
    val.put("BUDGET_RESERVE", "budget_const", ["judge_reserve_usd"], VV.usd2)
    spend = val.derive("BUDGET_SPEND", VV.d_add, [("verdicts", ["descriptives", "6_cost", "total_usd"]),
                                                  ("budget_const", ["judge_reserve_usd"])], VV.usd2)
    flags["BUDGET_PASS"] = (V["descriptives"]["6_cost"]["total_usd"] + src["budget_const"]["judge_reserve_usd"]
                            <= src["budget_const"]["cap_usd"])
    appr = (src["budget_state"].get("approvals") or {})
    ap = []
    for kind, label in (("past_80", "continuing past the US\\$80 pause"), ("projection", "continuing past the projection pause")):
        if kind in appr:
            s = val.put(f"APPR_{kind.upper()}", "budget_state", ["approvals", kind, "spent_at_approval_usd"], VV.usd2)
            ap.append(f"The pre-registrant approved {label} (recorded at a spend of {s}).")
    val.word("BUDGET_APPROVALS", " ".join(ap) if ap else (
        "No pause approval was recorded by the budget guard." if not synthetic else
        "[Synthetic test run: no budget state file.]"), ["budget_state", "approvals"])
    s1_refs = [("verdicts", MC + ["MC_Complete", "per_model_condition", f"{m}|S1", "answered"]) for m in VV.N3]
    s1_exp = [("verdicts", MC + ["MC_Complete", "per_model_condition", f"{m}|S1", "expected"]) for m in VV.N3]
    s1_ans = sum(val.raw(s, p) for s, p in s1_refs)
    s1_e = sum(val.raw(s, p) for s, p in s1_exp)
    if s1_ans >= s1_e:
        val.word("BUDGET_LIMIT_SENTENCE", "in the event, every search-on call was answered.", ["verdicts", "MC_Complete S1"])
    else:
        a = val.derive("S1_ANSWERED", VV.d_sum, s1_refs, VV.i0)
        e = val.derive("S1_EXPECTED", VV.d_sum, s1_exp, VV.i0)
        val.word("BUDGET_LIMIT_SENTENCE", f"in the event, {a} of the {e} search-on calls were answered (Table 2).",
                 ["verdicts", "MC_Complete S1"])

    # ---------------- Table 2 (manipulation checks)
    cl = Cells(val)
    rows = []
    for m in VV.N3:
        for c in ("S0", "S1"):
            k = f"{m}|{c}"
            pm = MC + ["MC_Complete", "per_model_condition", k]
            rows.append([VV.MODEL_NAME[m], c, f"{cl.f('verdicts', pm + ['answered'], VV.i0)} / "
                         f"{cl.f('verdicts', pm + ['expected'], VV.i0)}",
                         cl.f("verdicts", pm + ["share_of_expected"], VV.pct1),
                         "excluded" if (val.raw("verdicts", pm).get("excluded_below_90pct")) else "retained",
                         cl.f("verdicts", MC + ["MC_Truncation", k, "share"], VV.pct1),
                         cl.f("verdicts", MC + ["MC_Search", m, "share"], VV.pct1) if c == "S1" else "n/a"])
    val.table("TABLE_MC", md_table(["Model", "Cond.", "Answered / expected", "Share", "Drop rule", "At output cap",
                                    "With search"], rows, ["l", "l", "r", "r", "l", "r", "r"]), cl.cells)

    # ---------------- H_Gen_Presence
    H = ["verdicts", "H_Gen_Presence"]
    h = V["verdicts"]["H_Gen_Presence"]
    if cases["CASE_GEN"] in ("CONFIRMED", "MARGINAL", "FALSIFIED"):
        val.put("GEN_RHO", "verdicts", H + ["rho"], VV.r3)
        val.put("GEN_CI_LO", "verdicts", H + ["ci95_rho", 0], VV.r3)
        val.put("GEN_CI_HI", "verdicts", H + ["ci95_rho", 1], VV.r3)
        val.put("GEN_P", "verdicts", H + ["p_perm"], VV.p4)
        val.put("GEN_N", "verdicts", H + ["n"], VV.i0)
        val.put("GEN_NPERM", "verdicts", H + ["n_perm"], VV.i0)
        val.put("GEN_RHO_UNC", "verdicts", H + ["rho_uncentred_v041"], VV.r3)
        val.put("GEN_DELTA", "verdicts", H + ["delta"], VV.sr3)
        val.put("GEN_D_LO", "verdicts", H + ["ci95_delta", 0], VV.sr3)
        val.put("GEN_D_HI", "verdicts", H + ["ci95_delta", 1], VV.sr3)
        lo, hi = h["ci95_delta"]
        cases["GEN_DELTA_DIR"] = "ABOVE" if lo > 0 else ("BELOW" if hi < 0 else "SPANS")
        val.word("FIG1_CAPTION", f"$\\rho_{{\\text{{pw}}}} = {val.vals['GEN_RHO']}$ ($n = {val.vals['GEN_N']}$); "
                                 f"verdict {h['verdict']}.", ["verdicts", "H_Gen_Presence"])
    else:
        cases["GEN_DELTA_DIR"] = "SPANS"
        val.word("FIG1_CAPTION", "Verdict UNDETERMINED (§3.2).", ["verdicts", "H_Gen_Presence", "verdict"])
    ra = h.get("reported_alongside") or {}
    s1v = (ra.get("variants") or {}).get("N3_S1") or {}
    VA = H + ["reported_alongside", "variants", "N3_S1"]
    flags["GEN_S1_PRESENT"] = _ok(s1v, "rho", "p_perm") and bool(s1v.get("ci95_rho"))
    flags["GEN_S1_REDUCED"] = bool(s1v.get("reduced_panel"))
    if flags["GEN_S1_PRESENT"]:
        val.put("GEN_S1_RHO", "verdicts", VA + ["rho"], VV.r3)
        val.put("GEN_S1_CI_LO", "verdicts", VA + ["ci95_rho", 0], VV.r3)
        val.put("GEN_S1_CI_HI", "verdicts", VA + ["ci95_rho", 1], VV.r3)
        val.put("GEN_S1_P", "verdicts", VA + ["p_perm"], VV.p4)
        val.word("GEN_S1_VERDICT", s1v.get("verdict_if_primary", "UNDETERMINED"), VA + ["verdict_if_primary"])
        val.word("GEN_S1_MODELS", VV.names(s1v.get("models") or []), VA + ["models"])
    pparts = []
    for prov in VV.PROVIDERS:
        d = (ra.get("per_provider_generation_pairs") or {}).get(VV.PAIR_KEY[prov]) or {}
        newm = VV.MODEL_NAME[VV.PAIR_NEW[prov]]
        if VV.has(d, ["rho"]):
            r = val.put(f"PAIR_{prov.upper()}", "verdicts",
                        H + ["reported_alongside", "per_provider_generation_pairs", VV.PAIR_KEY[prov], "rho"], VV.r3)
            pparts.append(f"$\\rho_{{\\text{{pw}}}} = {r}$ for {prov} ({VV.PAIR_LEGACY[prov]} against {newm})")
        else:
            pparts.append(f"no value for {prov} ({newm} excluded in S0)")
    val.word("PAIRS_SENTENCE", "; ".join(pparts[:-1]) + "; and " + pparts[-1],
             ["verdicts", "H_Gen_Presence", "reported_alongside", "per_provider_generation_pairs"])
    cl = Cells(val)
    rows = []
    for s in VV.SUBS:
        rows.append([VV.CAT_SHORT[s] + f" ({s})",
                     cl.f("verdicts", H + ["per_substrate", s, "n"], VV.i0),
                     cl.f("verdicts", H + ["per_substrate", s, "rho"], VV.r3),
                     cl.f("verdicts", VA + ["per_substrate", s, "rho"], VV.r3)])
    val.table("TABLE_GEN_SUB", md_table(["Substrate", "Brands", "$\\rho$, search off", "$\\rho$, search on"], rows),
              cl.cells)

    # ---------------- H_Gen_Phi
    P = ["verdicts", "H_Gen_Phi"]
    hp = V["verdicts"]["H_Gen_Phi"]
    cp = cases["CASE_PHI"]
    if cp in ("CONFIRMED", "MARGINAL", "FALSIFIED", "UNDETERMINED_FLOOR"):
        val.put("PHI_N", "verdicts", P + ["n"], VV.i0)
        ps = hp.get("per_substrate") or {}
        if all(VV.has(ps, [s, "n"]) for s in VV.SUBS):
            bits = [f"{val.put('PHI_N_' + s.replace('.', ''), 'verdicts', P + ['per_substrate', s, 'n'], VV.i0)} "
                    f"{VV.CAT_SHORT[s].lower()}" for s in VV.SUBS]
            val.word("PHI_N_BY_SUB", " (" + ", ".join(bits[:-1]) + " and " + bits[-1] + ")", P + ["per_substrate"])
        else:
            val.word("PHI_N_BY_SUB", "", P + ["per_substrate"])
    if cp in ("CONFIRMED", "MARGINAL", "FALSIFIED"):
        val.put("PHI_RHO", "verdicts", P + ["rho"], VV.r3)
        val.put("PHI_CI_LO", "verdicts", P + ["ci95_rho", 0], VV.r3)
        val.put("PHI_CI_HI", "verdicts", P + ["ci95_rho", 1], VV.r3)
        val.put("PHI_P", "verdicts", P + ["p_perm"], VV.p4)
        val.put("PHI_RHO_UNC", "verdicts", P + ["rho_uncentred_v041"], VV.r3)
        val.word("FIG2_CAPTION", f"$\\rho_{{\\text{{pw}}}} = {val.vals['PHI_RHO']}$ ($n = {val.vals['PHI_N']}$); "
                                 f"verdict {hp['verdict']}.", P)
    else:
        val.word("FIG2_CAPTION", "Verdict UNDETERMINED (§3.3).", P + ["verdict"])
    rap = hp.get("reported_alongside") or {}
    pc = rap.get("partition_counts") or {}
    PC = P + ["reported_alongside", "partition_counts"]
    sent = []
    for cond, lead in (("S0", "On the newest models with search off"), ("S1", "with search on")):
        if VV.has(pc, [f"N3_{cond}", "brand_level"]):
            b = PC + [f"N3_{cond}", "brand_level"]
            d, z, sa, u = (val.put(f"PART_{cond}_{k.upper()}", "verdicts", b + [k], VV.i0)
                           for k in ("defined", "zero", "saturated", "undefined"))
            sent.append(f"{lead}, {d} brands had $\\varphi$ defined, {z} were in the zero partition in every run, "
                        f"{sa} in the saturated partition in every run and {u} were undefined (fewer than two defined runs)")
    if VV.has(pc, ["L6_t3", "defined"]):
        d3 = val.put("PART_T3_DEFINED", "verdicts", PC + ["L6_t3", "defined"], VV.i0)
        sent.append(f"at $t_3$, {d3} of the 112 brands had $\\varphi$ defined on the retiring panel")
    val.word("PARTITION_SENTENCE", ("; ".join(sent) + ".") if sent else "", PC)
    mi = (rap.get("mean_independence_S0") or {}).get("N3") or {}
    MI = P + ["reported_alongside", "mean_independence_S0", "N3"]
    flags["MI_PRESENT"] = VV.has(mi, ["abs"])
    flags["MI_FLAG"] = bool(mi.get("flag_ge_0_50"))
    if flags["MI_PRESENT"]:
        val.put("MI_ABS", "verdicts", MI + ["abs"], VV.r3)
        val.put("MI_N", "verdicts", MI + ["n"], VV.i0)
        val.put("MI_UNC", "verdicts", MI + ["rho_pw_phi_pi_uncentred_v041"], VV.r3)
    cl = Cells(val)
    rows = [[VV.CAT_SHORT[s] + f" ({s})", cl.f("verdicts", P + ["per_substrate", s, "n"], VV.i0),
             cl.f("verdicts", P + ["per_substrate", s, "rho"], VV.r3)] for s in VV.SUBS]
    val.table("TABLE_PHI_SUB", md_table(["Substrate", "Brands ($\\varphi$ defined on both)", "$\\rho$"], rows), cl.cells)

    # ---------------- H_Search_Presence
    S = ["verdicts", "H_Search_Presence"]
    hs = V["verdicts"]["H_Search_Presence"]
    cs_ = cases["CASE_SEARCH"]
    flags["S_REDUCED"] = bool(hs.get("reduced_panel"))
    if cs_ in ("ROBUST", "SENSITIVE", "DOMINATED"):
        val.word("S_MODELS", VV.names(hs.get("models") or []), S + ["models"])
        for nm, p_, fm in (("S_RHO", ["rho"], VV.r3), ("S_N", ["n"], VV.i0), ("S_CI_LO", ["ci95_rho", 0], VV.r3),
                           ("S_CI_HI", ["ci95_rho", 1], VV.r3), ("S_RHO_UNC", ["rho_uncentred_v041"], VV.r3),
                           ("S_DELTA", ["delta"], VV.sr3), ("S_D_LO", ["ci95_delta", 0], VV.sr3),
                           ("S_D_HI", ["ci95_delta", 1], VV.sr3)):
            val.put(nm, "verdicts", S + p_, fm)
        val.word("S_WHY", "", S)
        val.word("FIG3_CAPTION", f"$\\rho_S = {val.vals['S_RHO']}$; label {hs['label']}.", S + ["label"])
    else:
        why = (hs.get("reason") or "no model was retained in both conditions") if cs_ == "NOT_COMPUTED" else \
            "the bootstrap interval was not defined on the data"
        val.word("S_WHY", why, S + ["reason"])
        val.word("FIG3_CAPTION", "No label applies (§3.4).", S)
    cl = Cells(val)
    rows = []
    for m in VV.N3:
        pm = S + ["per_model", m]
        if VV.has(hs, ["per_model", m, "n"]):
            rows.append([VV.MODEL_NAME[m], cl.f("verdicts", pm + ["n"], VV.i0), cl.f("verdicts", pm + ["rho"], VV.r3),
                         cl.f("verdicts", pm + ["rho_uncentred_v041"], VV.r3), cl.f("verdicts", pm + ["delta"], VV.sr3)])
        else:
            rows.append([VV.MODEL_NAME[m], "--", "not computed", "--", "--"])
    val.table("TABLE_SEARCH_MODEL", md_table(["Model", "Brands", "$\\rho_{\\text{pw}}$", "Uncentred (v0.41)",
                                              "$\\Delta$ (on minus off)"], rows), cl.cells)

    # ---------------- descriptives
    D = ["descriptives"]
    rel = V["descriptives"]["1_run_reliability"]
    r1 = [("verdicts", D + ["1_run_reliability", k, "rel1"]) for k in sorted(rel) if VV.has(rel, [k, "rel1"])]
    r3 = [("verdicts", D + ["1_run_reliability", k, "rel3"]) for k in sorted(rel) if VV.has(rel, [k, "rel3"])]
    if r1:
        a, b = val.derive("REL1_MIN", VV.d_min, r1, VV.r2), val.derive("REL1_MAX", VV.d_max, r1, VV.r2)
        c, d = val.derive("REL3_MIN", VV.d_min, r3, VV.r2), val.derive("REL3_MAX", VV.d_max, r3, VV.r2)
        val.word("REL_SENTENCE", f"rel1 ranged from {a} to {b} and rel3 from {c} to {d}.", D + ["1_run_reliability"])
    else:
        val.word("REL1_MIN", "--", D); val.word("REL1_MAX", "--", D)
        val.word("REL_SENTENCE", "no run pair had enough brands to compute rel1.", D + ["1_run_reliability"])
    val.word("FIG4_CAPTION", "Descriptive; no verdict.", D + ["1_run_reliability"])
    cl = Cells(val)
    rows = []
    for m in VV.N3:
        for c in ("S0", "S1"):
            pk = D + ["1_run_reliability", f"{m}|{c}"]
            rows.append([VV.MODEL_NAME[m], c, cl.f("verdicts", pk + ["rel1"], VV.r3), cl.f("verdicts", pk + ["rel3"], VV.r3),
                         cl.f("verdicts", pk + ["rel1_uncentred_v041"], VV.r3)])
    val.table("TABLE_REL", md_table(["Model", "Cond.", "rel1", "rel3", "rel1, uncentred (v0.41)"], rows,
                                    ["l", "l", "r", "r", "r"]), cl.cells)
    rec = V["descriptives"]["2_recognition"]
    cl = Cells(val)
    rows = []
    for m in VV.N3:
        pk = D + ["2_recognition", "t4", f"{m}|S0"]
        rows.append([VV.MODEL_NAME[m], "$t_4$, search off", cl.f("verdicts", pk + ["recognized"], VV.i0),
                     cl.f("verdicts", pk + ["coded_answers"], VV.i0), cl.f("verdicts", pk + ["share"], VV.pct1)])
    leg = rec.get("t3_legacy") or {}
    if isinstance(leg, dict) and all(isinstance(leg.get(m), dict) for m in VV.L6):
        for m in VV.L6:
            pk = D + ["2_recognition", "t3_legacy", m]
            rows.append([VV.MODEL_NAME[m], "$t_3$", cl.f("verdicts", pk + ["recognized"], VV.i0),
                         cl.f("verdicts", pk + ["brands"], VV.i0), cl.f("verdicts", pk + ["share"], VV.pct1)])
    val.table("TABLE_RECOG", md_table(["Model", "Wave", "Recognized", "Coded", "Share"], rows,
                                      ["l", "l", "r", "r", "r"]), cl.cells)
    val.word("RECOG_NOTE", "Shares use the answers that could be coded as the denominator; recognition is not "
                           "computed for search on, which r2 does not collect.", D + ["2_recognition"])
    fl = V["descriptives"]["3_floor_persistence"]
    F = D + ["3_floor_persistence"]
    if fl.get("status") == "NOT_COMPUTED":
        val.word("FLOOR_SENTENCE", "Floor persistence was not computed, because a model was excluded in S0.", F)
        val.word("FIG5_CAPTION", "Not computed.", F)
    else:
        b3 = val.put("FL_B3", "verdicts", F + ["below_floor_t3"], VV.i0)
        b4 = val.put("FL_B4", "verdicts", F + ["below_floor_t4"], VV.i0)
        bb = val.put("FL_BOTH", "verdicts", F + ["below_both"], VV.i0)
        s1 = val.put("FL_SHARE", "verdicts", F + ["share_below_t3_still_below_t4"], VV.pct0) \
            if VV.has(fl, ["share_below_t3_still_below_t4"]) else "--"
        s2 = val.put("FL_REV", "verdicts", F + ["reverse_share_below_t4_that_were_below_t3"], VV.pct0) \
            if VV.has(fl, ["reverse_share_below_t4_that_were_below_t3"]) else "--"
        s3 = val.put("FL_UP", "verdicts", F + ["share_above_t3_now_below_t4"], VV.pct0) \
            if VV.has(fl, ["share_above_t3_now_below_t4"]) else "--"
        val.word("FLOOR_SENTENCE",
                 f"Of the {b3} brands below the recall floor at $t_3$, {bb} were still below it on the newest models "
                 f"with search off at $t_4$ ({s1}). Of the {b4} brands below the floor at $t_4$, {bb} had been below "
                 f"it at $t_3$ ({s2}), and {s3} of the brands above the floor at $t_3$ fell below it at $t_4$ "
                 f"(Figure 5; clarification C2).", F)
        val.word("FIG5_CAPTION", f"{bb} of {b3} brands below at $t_3$ were still below at $t_4$.", F)
    form = V["descriptives"]["4_answer_form"]
    cl = Cells(val)
    rows = []
    for m in VV.N3:
        for c in ("S0", "S1"):
            k = f"{m}|{c}"
            pk = D + ["4_answer_form", k]
            if k not in form:
                rows.append([VV.MODEL_NAME[m], c] + ["--"] * 7)
                continue
            fr = ", ".join(f"{name} {cl.f('verdicts', pk + ['finish_reasons', name], VV.i0)}"
                           for name in sorted(form[k].get("finish_reasons") or {}))
            na = pk + ["non_answers"]
            rows.append([VV.MODEL_NAME[m], c, cl.f("verdicts", pk + ["words_per_answer_A_mean"], VV.f1),
                         cl.f("verdicts", pk + ["words_per_answer_B_mean"], VV.f1),
                         cl.f("verdicts", pk + ["registry_brands_named_per_phase_B_answer"], VV.f1),
                         fr.replace("_", "\\_") or "--",
                         cl.f("verdicts", na + ["phase_A_no_yes_or_no_v0_19_to_v0_22"], VV.i0),
                         cl.f("verdicts", na + ["refusals_by_finish_reason"], VV.i0),
                         cl.f("verdicts", na + ["unanswered_calls_error_or_empty"], VV.i0)])
    val.table("TABLE_FORM", md_table(["Model", "Cond.", "Words (A)", "Words (B)", "Brands per B answer",
                                      "Finish reasons", "Non-answers", "Refusals", "Unanswered"], rows,
                                     ["l", "l", "r", "r", "r", "l", "r", "r", "r"]), cl.cells)
    sd = V["descriptives"]["5_search"]
    cl = Cells(val)
    rows, drows = [], []
    for m in VV.N3:
        pk = D + ["5_search", m]
        if m not in sd:
            rows.append([VV.MODEL_NAME[m], "0", "--", "--", "--", "--"])
            drows.append([VV.MODEL_NAME[m], "--"])
            continue
        rows.append([VV.MODEL_NAME[m], cl.f("verdicts", pk + ["s1_answered_calls"], VV.i0),
                     cl.f("verdicts", pk + ["searches_per_call"], VV.f1), cl.f("verdicts", pk + ["sources_per_call"], VV.f1),
                     cl.f("verdicts", pk + ["citations_per_call"], VV.f1),
                     cl.f("verdicts", pk + ["share_with_citation"], VV.pct0)])
        doms = sd[m].get("top20_cited_domains") or []
        drows.append([VV.MODEL_NAME[m], ", ".join(
            f"{dname} ({cl.f('verdicts', pk + ['top20_cited_domains', i, 1], VV.i0)})"
            for i, (dname, _n) in enumerate(doms)) or "--"])
    val.table("TABLE_SEARCHDESC", md_table(["Model", "S1 calls", "Searches per call", "Sources per call",
                                            "Citations per call", "With a citation"], rows), cl.cells)
    cl2 = Cells(val)
    cl2.cells = [c for c in cl.cells if "top20_cited_domains" in c[2]]
    val.table("TABLE_DOMAINS", md_table(["Model", "Domain (citations)"], drows, ["l", "l"]), cl2.cells)
    cost = V["descriptives"]["6_cost"]["per_model_condition"]
    cl = Cells(val)
    rows = []
    for m in VV.N3:
        for c in ("S0", "S1"):
            pk = D + ["6_cost", "per_model_condition", f"{m}|{c}"]
            rows.append([VV.MODEL_NAME[m], c, cl.f("verdicts", pk + ["billed_requests"], VV.i0),
                         cl.f("verdicts", pk + ["input_tokens"], VV.i0),
                         cl.f("verdicts", pk + ["output_tokens_billed"], VV.i0),
                         cl.f("verdicts", pk + ["searches_billed"], VV.i0), cl.f("verdicts", pk + ["usd"], VV.usd2)])
    rows.append(["All", "", "", "", "", "", cl.f("verdicts", D + ["6_cost", "total_usd"], VV.usd2)])
    val.table("TABLE_COST", md_table(["Model", "Cond.", "Billed requests", "Input tokens", "Output tokens",
                                      "Searches", "US\\$"], rows, ["l", "l", "r", "r", "r", "r", "r"]), cl.cells)
    return val, cases, flags


# =========================================================================== checks and main
def deviations_text(synthetic, no_deviations):
    if synthetic:
        t = "[Synthetic test run: the deviations record was not read.]"
        return t, t, ["synthetic"]
    if DEVIATIONS.exists():
        txt = DEVIATIONS.read_text(encoding="utf-8")
        n = len(re.findall(r"(?mi)^#+\s*Entry\b", txt))
        return (f"Deviations are recorded in `osf/v42/DEVIATIONS.md` ({n} entries), each before the step it concerns.",
                f"deviations recorded in `osf/v42/DEVIATIONS.md` ({n} entries).", ["osf/v42/DEVIATIONS.md"])
    if no_deviations:
        return ("No deviation from the pre-registration was recorded.", "no deviation recorded.",
                ["--no-deviations (operator: osf/v42/DEVIATIONS.md absent)"])
    raise FillError("osf/v42/DEVIATIONS.md not found: pass --no-deviations only if no deviation was recorded")


def verify_real(V):
    if VV.is_synthetic(V):
        raise FillError("verdicts come from the scorer's synthetic mode; use --synthetic")
    mp = V["manipulation_checks"]["MC_Parity"]
    det = mp.get("detail") or {}
    if not (mp.get("passed") and all(det.get(g) for g in ("P1", "P2", "P3"))):
        raise FillError(f"parity gates not all passed: {mp}")
    if V.get("prereg_tag") != VV.EXPECTED_PREREG_TAG:
        raise FillError(f"prereg_tag {V.get('prereg_tag')} != {VV.EXPECTED_PREREG_TAG}")
    commit = VV.git_tag_commit()
    if not commit:
        raise FillError(f"tag {VV.EXPECTED_PREREG_TAG} not found in {ROOT}")
    if not ANCHOR.exists() or commit not in ANCHOR.read_text(encoding="utf-8"):
        raise FillError(f"anchor {ANCHOR} missing or does not name {commit}")
    return commit[:10]


def fill(verdicts, table=None, out=None, fig_dir=None, synthetic=False, budget_state=None, no_deviations=False,
         v41=None, template=TEMPLATE):
    src = VV.load_sources(verdicts, table, v41, budget_state)
    V = src["verdicts"]
    if synthetic:
        if not VV.is_synthetic(V):
            raise FillError("--synthetic given but the verdicts are not from the scorer's synthetic mode")
        if V.get("prereg_tag") != VV.EXPECTED_PREREG_TAG:
            raise FillError(f"prereg_tag {V.get('prereg_tag')} != {VV.EXPECTED_PREREG_TAG}")
        commit = "synthetic run: tag not verified"
    else:
        commit = verify_real(V)
    fig_dir = fig_dir or "../../reports/figs/v42"
    val, cases, flags = compute(src, synthetic, fig_dir, commit, deviations_text(synthetic, no_deviations))
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
    ap = argparse.ArgumentParser(description="Fill the v0.42 paper template from the scorer's outputs")
    ap.add_argument("--verdicts", type=Path, default=ROOT / "osf/v42/v42_verdicts.json")
    ap.add_argument("--table", type=Path, default=ROOT / "osf/v42/v42_brand_table.csv")
    ap.add_argument("--budget-state", type=Path, default=ROOT / "osf/v42/data/t4_budget_state.json")
    ap.add_argument("--fig-dir", default=None, help="figure directory as the paper references it "
                                                     "(default ../../reports/figs/v42, relative to papers/v0_42)")
    ap.add_argument("--out", type=Path, default=HERE / "v0_42_ssrn_paper_draft.md")
    ap.add_argument("--synthetic", action="store_true")
    ap.add_argument("--no-deviations", action="store_true",
                    help="assert that no deviation was recorded (only when osf/v42/DEVIATIONS.md does not exist)")
    a = ap.parse_args(argv)
    if a.synthetic and str(a.out.resolve()).startswith(str(ROOT.resolve())):
        sys.exit("[fill v42] REFUSED: synthetic output must be written outside the repository")
    try:
        text, val, cases, flags = fill(a.verdicts, a.table, a.out, a.fig_dir, a.synthetic,
                                       a.budget_state if not a.synthetic else None, a.no_deviations)
    except (FillError, VV.Missing) as e:
        print(f"[fill v42] REFUSED: {e}", file=sys.stderr)
        return 3
    print(f"[fill v42] wrote {a.out} ({len(text.split())} words); cases {cases}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
