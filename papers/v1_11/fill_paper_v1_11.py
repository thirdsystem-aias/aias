#!/usr/bin/env python3
"""
fill_paper_v1_11.py -- fills papers/v1_11/v1_11_paper_template.md from the v1.11 scorer's outputs.

The template holds the whole paper. Introduction and Method are fixed text written from PRE_REGISTRATION_v1_11.md
(r1, locked at tag v1.11-prereg-r1). Results and Discussion are written in advance as alternative sentences, one per
pre-registered outcome, inside blocks this script selects from the verdicts (template engine forked unchanged from
papers/v1_12/fill_paper_v1_12.py, itself from papers/v0_42/fill_paper_v0_42.py):

  {% switch CASE_H1 %} {% case CONFIRMED %} ... {% case MARGINAL %} ... {% endswitch %}
  {% if FLAG %} ... {% else %} ... {% endif %}
  {{NAME}}      a value read from a machine output (v111_values.py records its JSON path)

Every switch must match exactly one case; an unknown flag or value is an error; the output may contain no
`{{` or `{%`. No number is typed here: values are leaves of the scorer's outputs (v1_11_verdicts.json from
`score_v1_11.py --stage C`, stage_j_v1_11.json from `--stage J`, judge_outputs_frozen_v1_11.json and plan_v1_11.json
from `judge_v1_11.py`), formatted by named functions; the provenance of every value is written beside the paper.
Verdict words are printed exactly as the scorer wrote them, and the fill refuses a verdict file whose words the
locked scorer's own functions do not reproduce from its statistics (check_consistency).

Checks before filling (real mode): none of the four files is synthetic (dry_run false, no synthetic_fixture);
prereg_tag == v1.11-prereg-r1; the tag exists in this repository and the anchor record
(osf/methodology/v1_11/anchor/git_anchor_v1_11.json) names its commit and a non-empty OSF deposit; the verdicts'
stage_j_sha256 is the Stage J file's; the four files name the same judges. Synthetic mode (--synthetic) requires
synthetic files, says so on the title page and in Results, and refuses to write inside the repository.

Usage (real run, after `score_v1_11.py --stage J` and `--stage C`; see papers/v1_11/PIPELINE.md):
  python3 papers/v1_11/fill_paper_v1_11.py
Synthetic test:
  python3 papers/v1_11/fill_paper_v1_11.py --synthetic --outputs /tmp/v111_pipeline_test/synth/scored \
      --fig-dir /tmp/v111_pipeline_test/scored/figs --out /tmp/v111_pipeline_test/scored/paper/v1_11_paper_draft.md
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
import v111_values as VV  # noqa: E402

ROOT = VV.ROOT
TEMPLATE = HERE / "v1_11_paper_template.md"
ANCHOR = ROOT / "osf/methodology/v1_11/anchor/git_anchor_v1_11.json"
DEVIATIONS = ROOT / "osf/methodology/v1_11/anchor/DEVIATIONS.md"


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
    sys.path.insert(0, str(ROOT / "scripts"))
    import score_v1_11 as S  # noqa: E402  (read-only)
    return S


def _nan(x):
    return float("nan") if x is None else float(x)


def recompute_words(V):
    """The verdict words the locked scorer's functions give for the statistics in V (no new decision)."""
    S = scorer()
    h1 = V["H1_Judge_Agreement"]
    br = h1["brand_rho"]
    raw = {"H1": S.judge_agreement_verdict(_nan(h1["alpha_ordinal"]), _nan(br.get("rho")),
                                           bool(br.get("determinable")) and h1["units_judged_by_both"] >= S.MIN_UNITS_POOLED)}
    for h in VV.SEP_HYPS:
        if h in V:
            pw = V[h]["per_wave"]
            raw[VV.SHORT[h]] = S.separability_verdict([S.wave_abs_rho({**pw[w], "rho": _nan(pw[w].get("rho"))})
                                                       for w in VV.WAVES])
    if "H5_Sep_Ranking" not in V:
        raw["H5"] = V["ranking"]["status"]
    for h in VV.STAB_HYPS:
        r = V[h]
        raw[VV.SHORT[h]] = S.stability_verdict(_nan(r.get("rho")), _nan(r.get("p_perm")), bool(r.get("determinable")))
    r = V["H7_Naming_Frequency"]
    raw["H7"] = S.band_verdict(abs(_nan(r.get("rho")))) if r.get("determinable") else "UNDETERMINED"
    h9 = V["H9_Self_Preference"]
    raw["H9"] = S.self_pref_verdict(_nan(h9.get("delta_points")), h9["n_own_provider"], h9["n_other"])
    final, on = S.apply_noise_guard(raw)
    return raw, final, on


def check_consistency(src):
    V, J, F, P = src["verdicts"], src["stage_j"], src["frozen"], src["plan"]
    raw, final, on = recompute_words(V)
    if raw != V["verdicts_before_noise_guard"] or final != V["VERDICTS"] or on != V["noise_guard_applied"]:
        raise FillError(f"verdict words not reproduced by the scorer's functions: file {V['VERDICTS']}, "
                        f"recomputed {final}")
    for h in VV.HYPS:
        leg = V.get(h)
        if leg is not None and leg.get("verdict") != raw[VV.SHORT[h]]:
            raise FillError(f"{h}: verdict {leg.get('verdict')} != {raw[VV.SHORT[h]]}")
    if J["H1_Judge_Agreement"]["verdict"] != V["H1_Judge_Agreement"]["verdict"]:
        raise FillError("H1 differs between Stage J and Stage C")
    if not (V["roles"] == J["roles"] == F["roles"] == P["roles"]):
        raise FillError("the four files name different judges")
    for k in ("H1", "H2", "H3", "H4", "H5", "H6", "H7", "H8", "H9"):
        if V["VERDICTS"][k] not in VV.VERDICT_WORDS:
            raise FillError(f"{k}: unknown verdict word {V['VERDICTS'][k]!r}")


# =========================================================================== values
SENS_NAME = {"SU_uncentred_ranks": "SU", "SD_without_Denon_v0_19": "SD"}
REDUCTION_TEXT = {"e_cap": "the early window cap lowered from 36 to 24",
                  "j2_e_share": "J2's early sample lowered from 10% to 5%",
                  "e_half": "the early block judged on a seeded half of each set's answers",
                  "e_none": "the early block not judged"}


def put_or(val, name, src, path, fmt, alt="n/a"):
    try:
        return val.put(name, src, path, fmt)
    except VV.Missing:
        return val.word(name, alt, [src] + list(path) + ["(null)"])


def ci_text(val, name, src, path):
    """'lo to hi' from a ci95 pair, each end with its own provenance."""
    lo = put_or(val, f"{name}_LO", src, path + ["ci95", 0], VV.r3)
    hi = put_or(val, f"{name}_HI", src, path + ["ci95", 1], VV.r3)
    return lo, hi


def wave_cells(cl, src, path):
    """One table cell: rho [lo, hi] (n), or n.d. (n) below the floor."""
    leg = VV.jget(cl.val.src[src], path)
    n = cl.f(src, path + ["n"], VV.i0)
    if not leg.get("determinable"):
        return f"n.d. ({n})"
    rho = cl.f(src, path + ["rho"], VV.sr3)
    lo, hi = cl.f(src, path + ["ci95", 0], VV.sr3), cl.f(src, path + ["ci95", 1], VV.sr3)
    return f"{rho} [{lo}, {hi}] ({n})"


def compute(src, synthetic, fig_dir, prereg_commit, prereg_date, deviations):
    V, J, F, P = src["verdicts"], src["stage_j"], src["frozen"], src["plan"]
    W = V["VERDICTS"]
    val = VV.Values(src)
    cases = {"CASE_H1": VV.case_h1(V), "CASE_OVERALL": VV.case_overall(V), "CASE_H7": VV.case_h7(V),
             "CASE_H9": VV.case_h9(V)}
    for h in VV.SEP_HYPS:
        cases[f"CASE_{VV.SHORT[h]}"] = VV.case_sep(V, h)
    for h in VV.STAB_HYPS:
        cases[f"CASE_{VV.SHORT[h]}"] = VV.case_stab(V, h)
    flags = {"SYNTHETIC": synthetic, "H5_ACTIVE": "H5_Sep_Ranking" in V, "GUARD_ON": bool(V["noise_guard_applied"]),
             "H1_FLAG": bool(V["H1_marginal_flag_on_all_verdicts"]), "JOIN_PASS": bool(V["join"]["passes"])}
    val.word("PREREG_TAG", V["prereg_tag"], ["verdicts", "prereg_tag"])
    val.word("PREREG_COMMIT", prereg_commit, ["git", f"refs/tags/{VV.EXPECTED_PREREG_TAG}"])
    val.word("PREREG_DATE", prereg_date, ["git", "taggerdate"])
    val.word("PAPER_DATE", "Synthetic test build" if synthetic else
             datetime.fromisoformat(V["created_utc"]).strftime("%B %Y"), ["verdicts", "created_utc"])
    val.word("FIG_DIR", str(fig_dir), ["argument --fig-dir"])
    val.word("FIG_CAPTION", "SYNTHETIC TEST DATA --- NOT RESULTS." if synthetic else "", ["synthetic flag"])
    val.word("DEV_SENTENCE", deviations[0], deviations[1])

    # ---------------- 3.1 run record
    val.put("RECORDS", "frozen", ["records"], VV.i0)
    val.put("SPEND", "frozen", ["spend_usd"], VV.usd2)
    val.put("SPEND_BATCH", "frozen", ["spend_usd_by_mode", "batch"], VV.usd2)
    val.put("SPEND_SYNC", "frozen", ["spend_usd_by_mode", "sync"], VV.usd2)
    val.put("CAL_J1", "plan", ["calibration", "calls", "J1"], VV.i0)
    val.put("CAL_J2", "plan", ["calibration", "calls", "J2"], VV.i0)
    val.put("OUT_J1", "plan", ["calibration", "output_tokens_per_call", "J1"], VV.i0)
    val.put("OUT_J2", "plan", ["calibration", "output_tokens_per_call", "J2"], VV.i0)
    val.put("PLAN_USD", "plan", ["steps", -1, "usd_with_overhead"], VV.usd2)
    red = P.get("reductions_applied") or []
    val.word("REDUCTION_SENTENCE", "no reduction of the early block applied." if not red else
             "the pre-registered reductions applied in their fixed order: "
             + "; ".join(REDUCTION_TEXT.get(r if isinstance(r, str) else (r.get("param") or r.get("name") or str(r)),
                                            str(r)) for r in red) + ".", ["plan", "reductions_applied"])
    rep = F.get("replacements") or []
    val.word("REPLACEMENT_SENTENCE", "Neither judge was replaced by the alternate." if not rep else
             "The alternate replaced a judge, as recorded in the frozen outputs (`replacements`); the replaced judge's "
             "outputs are kept and not scored.", ["frozen", "replacements"])
    for r in ("J1", "J2"):
        for key, k in (("VALID", "VALID"), ("FAIL", "JUDGE_FAIL"), ("UNJ", "UNJUDGED")):
            put_or(val, f"{r}_{key}", "stage_j", ["outcome_counts", r, k], VV.i0, alt="0")
    fsets = J["judge_fail"]["per_judge_set"]
    val.derive("FAIL_MAX", VV.d_max, [("stage_j", ["judge_fail", "per_judge_set", k, "fail_share"]) for k in fsets],
               VV.pct1)
    served = F.get("served_models") or {}
    other = [k for k in served if k not in V["roles"].values()]
    if other:
        val.derive("SERVED_OTHER", VV.d_sum, [("frozen", ["served_models", k]) for k in other], VV.i0)
        val.word("SERVED_SENTENCE", f"{val.vals['SERVED_OTHER']} responses came without the requested model ID or "
                 "with another one; each counted as invalid output and was retried (§2.3).", ["frozen", "served_models"])
    else:
        val.word("SERVED_SENTENCE", "Every response was served by the requested model.", ["frozen", "served_models"])
    val.derive("WINDOW_MISMATCH", VV.d_len, [("verdicts", ["F_window_count_vs_n_mentions", "mismatches"])], VV.i0)
    val.derive("PC_DIFF", VV.d_len, [("verdicts", ["P_Cstar_v1_9_cross_check", "differences"])], VV.i0)
    val.put("PC_ROWS", "verdicts", ["P_Cstar_v1_9_cross_check", "rows_compared"], VV.i0)
    rk = V["ranking"]
    if rk.get("status") == "ACTIVE":
        tabs = rk.get("rank_tables") or {}
        val.derive("RANK_TABLES", VV.d_len, [("verdicts", ["ranking", "rank_tables"])], VV.i0)
        val.word("RANKING_SENTENCE", f"$R^*$ ({rk.get('statistic')}) was computed with v1.10's locked code; all "
                 f"{val.vals['RANK_TABLES']} regenerated rank tables equalled v1.10's Stage S tables"
                 + ("." if all(t.get("matches_v1_10_stage_s") for t in tabs.values()) else " (see the verdict file)."),
                 ["verdicts", "ranking"])
    else:
        val.word("RANKING_SENTENCE", f"Ranking was not computed (H5 {rk.get('status')}: {rk.get('reason')}).",
                 ["verdicts", "ranking"])

    # ---------------- 3.2 H1 and self-consistency
    H1 = ["H1_Judge_Agreement"]
    val.word("V_H1", W["H1"], ["verdicts", "VERDICTS", "H1"])
    val.put("H1_PAIRS", "verdicts", H1 + ["units_judged_by_both"], VV.i0)
    put_or(val, "H1_ALPHA", "verdicts", H1 + ["alpha_ordinal"], VV.r3)
    put_or(val, "H1_ALPHA_REF", "verdicts", H1 + ["alpha_refers_true_both"], VV.r3)
    for b in ("R", "F", "E"):
        put_or(val, f"H1_ALPHA_{b}", "verdicts", H1 + ["alpha_by_block", b], VV.r3)
    put_or(val, "H1_KAPPA", "verdicts", H1 + ["kappa_evaluative"], VV.r3)
    put_or(val, "H1_BRHO", "verdicts", H1 + ["brand_rho", "rho"], VV.r3)
    val.put("H1_BRHO_N", "verdicts", H1 + ["brand_rho", "n"], VV.i0)
    ci_text(val, "H1_BRHO", "verdicts", H1 + ["brand_rho"])
    SC = ["self_consistency"]
    put_or(val, "SC_J1_ALL", "verdicts", SC + ["J1", "all", "exact_valence_agreement"], VV.r3)
    put_or(val, "SC_J2_ALL", "verdicts", SC + ["J2", "all", "exact_valence_agreement"], VV.r3)
    cl = Cells(val)
    rows, anyflag = [], False
    for r in ("J1", "J2"):
        for b, lab in (("R", "Recognition"), ("F", "Omnibus"), ("E", "Early"), ("all", "All")):
            pk = SC + [r, b]
            if not VV.has(V, pk):
                continue
            anyflag |= bool(VV.jget(V, pk).get("flag_below_0.90"))
            rows.append([f"{r} ({VV.JUDGE_NAME.get(V['roles'][r], V['roles'][r])})" if b == "R" else "", lab,
                         cl.f("verdicts", pk + ["n"], VV.i0), cl.f("verdicts", pk + ["exact_valence_agreement"], VV.r3),
                         cl.f("verdicts", pk + ["alpha_ordinal"], VV.r3), cl.f("verdicts", pk + ["kappa_evaluative"], VV.r3),
                         "yes" if VV.jget(V, pk).get("flag_below_0.90") else "no"])
    flags["SC_ANY_FLAG"] = anyflag
    val.table("TABLE_SELFCON", md_table(["Judge", "Block", "Pairs", "Exact", "$\\alpha$", "$\\kappa$", "Below 0.90"],
                                        rows, ["l", "l", "r", "r", "r", "r", "l"]), cl.cells)

    # ---------------- 3.3 separability table
    cl = Cells(val)
    rows = []
    against = {"H2_Sep_Presence": "Presence $P$", "H3_Sep_Consistency": "Consistency $C^*$",
               "H5_Sep_Ranking": "Ranking $R^*$", "H8_Recognition_Sep": "Presence (recognition $S_{\\text{rec}}$)"}
    for h in VV.SEP_HYPS:
        s = VV.SHORT[h]
        val.word(f"V_{s}", W[s], ["verdicts", "VERDICTS", s])
        if h not in V:
            rows.append([s, against[h], "--", "--", "--", W[s]])
            continue
        rows.append([s, against[h]] + [wave_cells(cl, "verdicts", [h, "per_wave", w]) for w in VV.WAVES] + [W[s]])
    val.table("TABLE_SEP", md_table(["", "Against", "$t_1$", "$t_2$", "$t_3$", "Verdict"], rows,
                                    ["l", "l", "r", "r", "r", "l"]), cl.cells)
    if "H5_secondary_early" in V:
        put_or(val, "H5E_RHO", "verdicts", ["H5_secondary_early", "rho"], VV.r3)
        val.put("H5E_N", "verdicts", ["H5_secondary_early", "n"], VV.i0)
        val.word("H5E_V", V["H5_secondary_early"]["verdict"], ["verdicts", "H5_secondary_early", "verdict"])

    # ---------------- 3.4 stability, 3.5 secondary
    for h in VV.STAB_HYPS:
        s = VV.SHORT[h]
        val.word(f"V_{s}", W[s], ["verdicts", "VERDICTS", s])
        put_or(val, f"{s}_RHO", "verdicts", [h, "rho"], VV.r3)
        val.put(f"{s}_N", "verdicts", [h, "n"], VV.i0)
        ci_text(val, s, "verdicts", [h])
        put_or(val, f"{s}_P", "verdicts", [h, "p_perm"], VV.p4)
    put_or(val, "H7_RHO", "verdicts", ["H7_Naming_Frequency", "rho"], VV.r3)
    val.put("H7_N", "verdicts", ["H7_Naming_Frequency", "n"], VV.i0)
    ci_text(val, "H7", "verdicts", ["H7_Naming_Frequency"])
    H9 = ["H9_Self_Preference"]
    put_or(val, "H9_OWN", "verdicts", H9 + ["mean_diff_own"], VV.sf1)
    put_or(val, "H9_OTHER", "verdicts", H9 + ["mean_diff_other"], VV.sf1)
    put_or(val, "H9_DELTA", "verdicts", H9 + ["delta_points"], VV.sf1)
    val.put("H9_N_OWN", "verdicts", H9 + ["n_own_provider"], VV.i0)
    val.put("H9_N_OTHER", "verdicts", H9 + ["n_other"], VV.i0)

    # ---------------- 3.6 verdict table: every pre-registered test exactly once
    stat = {"H1_Judge_Agreement": "ordinal $\\alpha$; brand $\\rho_w(S_{J1}, S_{J2})$",
            "H2_Sep_Presence": "$\\lvert\\rho_w(S, P)\\rvert$ per wave", "H3_Sep_Consistency":
            "$\\lvert\\rho_w(S, C^*)\\rvert$ per wave", "H4_Stability_Short": "$\\rho_w(S_{t_1}, S_{t_2})$, permutation",
            "H5_Sep_Ranking": "$\\lvert\\rho_w(S, R^*)\\rvert$ per wave", "H6_Stability_Long":
            "$\\rho_w(S_{t_2}, S_{t_3})$, permutation", "H7_Naming_Frequency": "$\\lvert\\rho_w(S, n_{\\text{named}})\\rvert$, early",
            "H8_Recognition_Sep": "$\\lvert\\rho(S_{\\text{rec}}, P)\\rvert$ per wave",
            "H9_Self_Preference": "$\\Delta$ of $u_{J1} - u_{J2}$, own vs other"}
    rows = []
    for h in VV.HYPS:
        s = VV.SHORT[h]
        before = V["verdicts_before_noise_guard"][s]
        rows.append([h.replace("_", "\\_"), VV.TIER[s], stat[h], W[s], before if before != W[s] else "--"])
    val.table("TABLE_VERDICTS", md_table(["Test", "Tier", "Statistic", "Verdict", "Before guard"], rows,
                                         ["l", "l", "l", "l", "l"]), [])

    # ---------------- 3.7 sensitivities
    sens = V["sensitivities"]
    ch = sens.get("verdict_changes") or []
    val.word("SENS_SENTENCE", "No verdict changed under any sensitivity analysis." if not ch else
             "Verdicts changed under a sensitivity analysis (never replacing the primary verdict): " + "; ".join(
                 f"{c['hypothesis']} under {SENS_NAME.get(c['sensitivity'], c['sensitivity'])}, {c['primary']} "
                 f"$\\rightarrow$ {c['under_sensitivity']}" for c in ch) + ".", ["verdicts", "sensitivities",
                                                                                 "verdict_changes"])
    rows = []
    for h in VV.HYPS:
        s = VV.SHORT[h]
        row = [s, V["verdicts_before_noise_guard"][s]]
        for name in ("SU_uncentred_ranks", "SD_without_Denon_v0_19"):
            d = sens[name]
            if h == "H9_Self_Preference":
                row.append((d.get(h) or V[h])["verdict"] if name == "SD_without_Denon_v0_19" else V[h]["verdict"])
            elif h in d:
                row.append(d[h]["verdict"])
            else:
                row.append(W[s] if s == "H5" else "--")
        rows.append(row)
    val.table("TABLE_SENS", md_table(["", "Primary (before guard)", "SU uncentred", "SD without Denon"], rows,
                                     ["l", "l", "l", "l"]), [])
    cl = Cells(val)
    rows = []
    for b in ("R", "F", "E"):
        rows.append([f"$\\alpha$, block {b}", "", cl.f("verdicts", H1 + ["alpha_by_block", b], VV.r3), "", "", ""])
    variants = [("S_NV_in_place_of_S", "NV"), ("S_model_balanced", "Model-balanced"), ("S_J2_scored", "J2-scored"),
                ("S_without_J1_provider_answers", "Without J1-provider answers")]
    for key, lab in variants:
        if key not in sens:
            continue
        for hk in ("H2", "H3"):
            pk = ["sensitivities", key, hk]
            rows.append([f"{lab}, {hk}", VV.jget(V, pk)["verdict"], ""]
                        + [wave_cells(cl, "verdicts", pk + ["per_wave", w]) for w in VV.WAVES])
    val.table("TABLE_SENS_S", md_table(["Variant", "Verdict", "Value", "$t_1$", "$t_2$", "$t_3$"], rows,
                                       ["l", "l", "r", "r", "r", "r"]), cl.cells)

    # ---------------- 3.8 baseline and appendix
    D = ["descriptives"]
    base = V["descriptives"]["baseline"]
    order = sorted(range(len(base)), key=lambda i: ({"R": 0, "F": 1, "E": 2}[base[i]["block"]], base[i]["category"],
                                                    base[i]["wave"]))
    cl = Cells(val)
    rows = []
    for i in order:
        b = base[i]
        pk = D + ["baseline", i]
        lab = (VV.CAT_SHORT.get(b["category"], b["category"]) if b["block"] != "E"
               else VV.EARLY_SHORT.get(b["category"], b["category"]))
        rows.append([{"R": "Recognition", "F": "Omnibus", "E": "Early"}[b["block"]], lab, b["wave"],
                     cl.f("verdicts", pk + ["brands"], VV.i0), cl.f("verdicts", pk + ["brands_rated"], VV.i0),
                     cl.f("verdicts", pk + ["S", "median"], VV.f1),
                     f"{cl.f('verdicts', pk + ['S', 'q25'], VV.f1)}--{cl.f('verdicts', pk + ['S', 'q75'], VV.f1)}",
                     cl.f("verdicts", pk + ["E_mean"], VV.r2), cl.f("verdicts", pk + ["share_non_evaluative"], VV.pct0),
                     cl.f("verdicts", pk + ["share_mixed"], VV.pct0), cl.f("verdicts", pk + ["share_refers_false"], VV.pct1)])
    val.table("TABLE_BASE", md_table(["Block", "Category", "Wave", "Brands", "Rated", "S median", "S IQR", "E",
                                      "Non-eval.", "Mixed", "Not brand"], rows,
                                     ["l", "l", "l", "r", "r", "r", "r", "r", "r", "r", "r"]), cl.cells)
    for blk, nm in (("F", "BASE_F"), ("E", "BASE_E")):
        refs = [("verdicts", D + ["baseline", i, "S", "median"]) for i, b in enumerate(base)
                if b["block"] == blk and VV.has(V, D + ["baseline", i, "S", "median"])]
        if refs:
            val.derive(f"{nm}_MIN", VV.d_min, refs, VV.f1)
            val.derive(f"{nm}_MAX", VV.d_max, refs, VV.f1)
        else:
            val.word(f"{nm}_MIN", "n/a", ["no rated brands"])
            val.word(f"{nm}_MAX", "n/a", ["no rated brands"])
    put_or(val, "PANEL_LEGACY", "verdicts", D + ["mean_u", "by panel", "LEGACY-6", "mean_u"], VV.f1)
    put_or(val, "PANEL_EARLY", "verdicts", D + ["mean_u", "by panel", "EARLY-6", "mean_u"], VV.f1)
    for k, w in enumerate(VV.WAVES, 1):
        put_or(val, f"CONV_T{k}", "verdicts", D + ["convergence_rec_vs_frames", w, "spearman"], VV.r3)
        val.put(f"CONV_N{k}", "verdicts", D + ["convergence_rec_vs_frames", w, "n"], VV.i0)
    cl = Cells(val)
    mu = V["descriptives"]["mean_u"]
    models = sorted({m for g in ("R by model", "F by model", "E by model") for m in (mu.get(g) or {})})
    rows = []
    for m in models:
        rows.append([m] + [cl.f("verdicts", D + ["mean_u", g, m, "mean_u"], VV.f1) + " (" +
                           cl.f("verdicts", D + ["mean_u", g, m, "n"], VV.i0) + ")" if VV.has(V, D + ["mean_u", g, m])
                           else "--" for g in ("R by model", "F by model", "E by model")])
    val.table("TABLE_MODEL", md_table(["Answering model", "Recognition", "Omnibus", "Early"], rows), cl.cells)
    cl = Cells(val)
    conf = H1 + ["confusion_J1_rows_J2_cols"]
    rows = []
    for a in (-2, -1, 0, 1, 2):
        rows.append([f"J1 {a:+d}".replace("+0", "0")] + [cl.f("verdicts", conf + [f"{a}|{b}"], VV.i0, missing="0")
                                                        for b in (-2, -1, 0, 1, 2)])
    val.table("TABLE_CONF", md_table(["", "J2 −2", "J2 −1", "J2 0", "J2 +1", "J2 +2"], rows), cl.cells)
    lg = V["descriptives"].get("legacy_label_agreement") or {}
    if lg.get("n"):
        n = val.put("LEGACY_N", "verdicts", D + ["legacy_label_agreement", "n"], VV.i0)
        a = val.put("LEGACY_AGREE", "verdicts", D + ["legacy_label_agreement", "agreement"], VV.pct1)
        val.word("LEGACY_SENTENCE", f"Exploratory (pre-registration §6.6): on {n} (answer, brand) pairs of the five v0.9 "
                 f"early sets, the sign of J1's valence agreed with the archived per-brand label in {a} of pairs.",
                 ["verdicts"] + D + ["legacy_label_agreement"])
    else:
        val.word("LEGACY_SENTENCE", "Exploratory (pre-registration §6.6): the agreement with the archived per-brand "
                 "labels was not computed.", ["verdicts"] + D + ["legacy_label_agreement"])
    return val, cases, flags


# =========================================================================== checks and main
def deviations_text(synthetic):
    rel = "osf/methodology/v1_11/anchor/DEVIATIONS.md"
    if not DEVIATIONS.exists():
        raise FillError(f"{DEVIATIONS} not found (it is a locked file of v1.11-prereg-r1)")
    txt = DEVIATIONS.read_text(encoding="utf-8")
    after = re.findall(r"(?m)^## Entry ([1-9]\d*)\b", txt)
    n = len(after)
    s = (f"The deviations record (`{rel}`) holds Entry 0, written before the lock (conflict-of-interest screen, the "
         f"Denon correction and the pre-lock record), and {n} entr{'y' if n == 1 else 'ies'} after it, each made "
         f"before the step it concerns.")
    if synthetic:
        s += " [Synthetic test run: the count is read from the record as committed in this worktree.]"
    return s, [rel]


def tag_info():
    commit = VV.git_tag_commit()
    r = subprocess.run(["git", "-C", str(ROOT), "for-each-ref", "--format=%(taggerdate:iso-strict)",
                        f"refs/tags/{VV.EXPECTED_PREREG_TAG}"], capture_output=True, text=True)
    d = r.stdout.strip()
    date = datetime.fromisoformat(d).strftime("%-d %B %Y") if d else None
    return commit, date


def verify_real(src, outputs):
    if VV.is_synthetic(src):
        raise FillError("the outputs come from a dry run or a synthetic scenario (dry_run / synthetic_fixture); "
                        "use --synthetic")
    V = src["verdicts"]
    if V.get("prereg_tag") != VV.EXPECTED_PREREG_TAG or V.get("stage") != "C" or src["stage_j"].get("stage") != "J":
        raise FillError(f"prereg_tag {V.get('prereg_tag')} / stages are not v1.11-prereg-r1 Stage C and Stage J")
    F = src["frozen"]
    if F.get("units_sha256") != V.get("units_sha256") or src["stage_j"].get("units_sha256") != V.get("units_sha256"):
        raise FillError("the frozen judge outputs, Stage J and Stage C were made on different unit tables")
    if F.get("plan_sha256") != VV.sha256(VV.source_path(outputs, "plan")):
        raise FillError("the plan file is not the one the frozen judge outputs record (plan_sha256)")
    commit, date = tag_info()
    if not commit:
        raise FillError(f"tag {VV.EXPECTED_PREREG_TAG} not found in {ROOT}")
    if not ANCHOR.exists():
        raise FillError(f"anchor {ANCHOR} missing")
    an = json.loads(ANCHOR.read_text(encoding="utf-8"))
    if an.get("commit") != commit or not (an.get("osf_deposit") or "").strip():
        raise FillError(f"anchor does not name {commit} with a non-empty osf_deposit")
    return commit, date


def fill(outputs, out=None, fig_dir=None, synthetic=False, template=TEMPLATE):
    src = VV.load_sources(outputs)
    stage_j_sha = VV.sha256(Path(outputs) / VV.NAMES["stage_j"])
    if src["verdicts"].get("stage_j_sha256") != stage_j_sha:
        raise FillError("the verdicts were not computed from this Stage J file (stage_j_sha256 differs)")
    if synthetic:
        if not VV.is_synthetic(src):
            raise FillError("--synthetic given but the outputs are not synthetic")
        if src["verdicts"].get("prereg_tag") != VV.EXPECTED_PREREG_TAG:
            raise FillError(f"prereg_tag {src['verdicts'].get('prereg_tag')} != {VV.EXPECTED_PREREG_TAG}")
        c, d = tag_info()
        commit = c[:10] if c else "synthetic run: tag not found"
        date = d or "synthetic run"
    else:
        c, date = verify_real(src, outputs)
        commit = c[:10]
    check_consistency(src)
    fig_dir = fig_dir or "../../reports/figs/v111"
    val, cases, flags = compute(src, synthetic, fig_dir, commit, date, deviations_text(synthetic))
    tpl = Path(template).read_text(encoding="utf-8")
    text = render(tpl, val.vals, cases, flags)
    if out:
        out = Path(out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
        prov = {"outputs": str(outputs), "synthetic": synthetic, "cases": cases, "flags": flags, "values": val.prov}
        Path(str(out).replace(".md", "_provenance.json")).write_text(
            json.dumps(prov, indent=1, ensure_ascii=False, default=str), encoding="utf-8")
    return text, val, cases, flags


def main(argv=None):
    ap = argparse.ArgumentParser(description="Fill the v1.11 Sentiment Paper A template from the scorer's outputs")
    ap.add_argument("--outputs", type=Path, default=VV.OUTDIR, help="folder with the four scorer/runner outputs")
    ap.add_argument("--fig-dir", default=None, help="figure directory as the paper references it "
                                                     "(default ../../reports/figs/v111, relative to papers/v1_11)")
    ap.add_argument("--out", type=Path, default=HERE / "v1_11_paper_draft.md")
    ap.add_argument("--synthetic", action="store_true")
    a = ap.parse_args(argv)
    if a.synthetic and str(a.out.resolve()).startswith(str(ROOT.resolve())):
        print("[fill v1.11] REFUSED: synthetic output must be written outside the repository", file=sys.stderr)
        return 2
    try:
        text, val, cases, flags = fill(a.outputs, a.out, a.fig_dir, a.synthetic)
    except (FillError, VV.Missing) as e:
        print(f"[fill v1.11] REFUSED: {e}", file=sys.stderr)
        return 3
    print(f"[fill v1.11] wrote {a.out} ({len(text.split())} words); cases {cases}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
