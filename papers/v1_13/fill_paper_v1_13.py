#!/usr/bin/env python3
"""
fill_paper_v1_13.py -- fills papers/v1_13/v1_13_paper_template.md from the v1.13 scorers' outputs.

The template holds the whole paper. Introduction and Method are fixed text written from the locked pre-registration
(PRE_REGISTRATION_v1_13.md, tag v1.13-prereg-r1) and the Part II protocol (website_audit_protocol_v1_13.md), with
section numbers. Results and Discussion are written in advance as alternative sentences, one per pre-registered
outcome, inside blocks this script selects from the verdicts (template engine forked unchanged from
papers/v1_12/fill_paper_v1_12.py, itself from papers/v0_42/):

  {% switch CASE_GATE %} {% case PASS %} ... {% case MARGINAL|MARGINAL_DOWNGRADED %} ... {% endswitch %}
  {% if FLAG %} ... {% else %} ... {% endif %}
  {{NAME}}      a value read from a machine output (papers/v1_13/v113_values.py records its path)

Every switch must match exactly one case; an unknown flag or value is an error; the output may contain no `{{` or
`{%`. No number is typed here: values are leaves of the verdict file (score_v1_13.py --stage C1 and --stage C2) or of
the SDRI table (audit_v1_13.py --sdri), or named functions of such leaves; the provenance of every value is written
beside the paper. Verdict words are printed exactly as the scorer wrote them.

Refusals (both modes): a verdict word, the gate, a Stage C2 re-issue or H7 that the locked scorer's own functions do
not reproduce from the file's statistics (v113_values.check_consistency); an SDRI table without a Part II verdict, or
the reverse; a missing value the template needs.
Real mode also refuses: a synthetic file; no Stage C2 unless --interim; tag v1.13-prereg-r1 missing or the anchor not
naming its commit; conditional legs other than the anchor's activation record; a v1.14 Stage 1 source that is a dry run
or a v1.12 source not from the anchored commit; a computed H7 without tag v1.13-audit-r1 and its audit anchor; the
deviations record no longer stating the waiver of the 24-hour review; any of the three house/portal units missing.

Usage (real run, after score_v1_13.py --stage C1 and --stage C2; see papers/v1_13/PIPELINE.md):
  python3 papers/v1_13/fill_paper_v1_13.py [--coi-cheil]
Synthetic test (outputs outside the repository only):
  python3 papers/v1_13/fill_paper_v1_13.py --synthetic \
      --verdicts papers/v1_13/tests/fixtures/SYNTHETIC_scored_v1_13_verdicts.json \
      --sdri papers/v1_13/tests/fixtures/SYNTHETIC_scored_v1_13_sdri.csv \
      --fig-dir /tmp/v113_pipeline_test/figs --out /tmp/v113_pipeline_test/paper/v1_13_paper_draft.md
"""
import argparse
import json
import math
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import v113_values as VV  # noqa: E402

ROOT = VV.ROOT
S = VV.S
TEMPLATE = HERE / "v1_13_paper_template.md"


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

# =========================================================================== values
DASH = "--"


def _verb(hs):
    return "were" if len(hs) > 1 else "was"


def _short(hs):
    return VV.joinand(VV.SHORT[h] for h in hs)


def _plain(hs):
    return VV.joinand(f"{VV.PLAIN[h]} ({VV.SHORT[h]})" for h in hs)


def _changes(ch):
    """{leg: [word under the sensitivity, primary word]} -> 'H1, H2 UNDETERMINED; H3 MARGINAL' (grouped by word)."""
    by = {}
    for h, w in ch.items():
        by.setdefault(w[0], []).append(VV.SHORT[h])
    return "; ".join(f"{', '.join(hs)} {w}" for w, hs in by.items()) or "none"


def _opt(val, name, src, path, fmt):
    """put() if the leaf exists and is finite, else the dash (recorded as text)."""
    if VV.has(val.src[src], path):
        return val.put(name, src, path, fmt)
    return val.word(name, DASH, [src] + list(path) + ["(not computed)"])


def _leg(val, prefix, path):
    """N, RHO, P, LO, HI of one leg (dash where the scorer wrote no value)."""
    _opt(val, f"{prefix}_N", "verdicts", path + ["n"], VV.i0)
    _opt(val, f"{prefix}_RHO", "verdicts", path + ["rho_w"], VV.r3)
    _opt(val, f"{prefix}_P", "verdicts", path + ["p"], VV.p4)
    _opt(val, f"{prefix}_LO", "verdicts", path + ["ci90", "lo"], VV.r3)
    _opt(val, f"{prefix}_HI", "verdicts", path + ["ci90", "hi"], VV.r3)


class Cells:
    """Collects (formatted, source, path, fmt) for every number put in a table."""

    def __init__(self, val):
        self.val, self.cells = val, []

    def f(self, src, path, fmt, missing=DASH):
        try:
            raw = self.val.raw(src, path)
        except VV.Missing:
            return missing
        if raw is None or raw == "" or (isinstance(raw, float) and not math.isfinite(raw)):
            return missing
        s = fmt(raw)
        self.cells.append((s, src, path, fmt.__name__))
        return s


def md_table(header, rows, align=None):
    align = align or ["l"] + ["r"] * (len(header) - 1)
    vis = lambda t: len(re.sub(r"\$[^$]*\$|\\[a-z]+|[{}`]", "x", t))      # noqa: E731  visible width, roughly
    widths = [max(4, min(60, max([vis(header[j])] + [vis(r[j]) for r in rows]))) for j in range(len(header))]
    widths[0] += 4
    sep = ["|:" + "-" * w if a == "l" else "|" + "-" * w + ":" for a, w in zip(align, widths)]
    lines = ["| " + " | ".join(header) + " |", "".join(sep) + "|"]
    lines += ["| " + " | ".join(r) + " |" for r in rows]
    return "\n".join(lines)


def compute(src, synthetic, fig_dir, ctx):
    """ctx: prereg_commit, prereg_tag_utc, part2_locked, part2_commit, receipt_utc, deviations (sentence, status,
    basis), coi_cheil."""
    V = src["verdicts"]
    val = VV.Values(src)
    cases, flags = {}, {}
    fg = VV.final_gate(V)
    c2 = V.get("stage_C2")
    flags["STAGE_C1_ONLY"] = c2 is None
    cases["CASE_GATE"] = VV.case_gate(V)
    for h in ("H1_Sep_Presence", "H2_Sep_Consistency"):
        cases[f"CASE_{VV.SHORT[h]}"] = VV.case_sep(V, h)
    cases["CASE_H3"] = VV.case_h3(V)
    val.word("PREREG_COMMIT", ctx["prereg_commit"], ["git", "refs/tags/v1.13-prereg-r1"])
    val.word("PREREG_TAG_UTC", ctx["prereg_tag_utc"], ["git", "tagger date of v1.13-prereg-r1"])
    val.word("FIG_DIR", str(fig_dir), ["argument --fig-dir"])
    val.word("FIG_CAPTION", "SYNTHETIC TEST DATA --- NOT RESULTS." if synthetic else "", ["synthetic flag"])
    val.word("DEV_SENTENCE", ctx["deviations"][0], ctx["deviations"][2])
    val.word("DEV_STATUS", ctx["deviations"][1], ctx["deviations"][2])
    val.word("GATE_FINAL", fg["final"], ["verdicts", "gate / stage_C2 re-issues"])

    # ---------------- data, units, quality checks
    MQ = ["MQ"]
    val.put("MQ1_N", "verdicts", MQ + ["MQ1_parsed_s1_records"], VV.i0)
    panel = V["panel_models"]
    val.derive("N_CAT_ANSWERS", VV.d_sum, [("verdicts", MQ + ["MQ2", m, "answers"]) for m in panel], VV.i0)
    units = V["units"]
    val.word("UNITS_N", str(len(units)), ["verdicts", "units (count)"])
    val.put("RATED_N", "verdicts", MQ + ["MQ5", "n_rated"], VV.i0)
    val.word("NOTRATED_FLOOR_N", str(sum(1 for u in units.values() if u["reason"] == "g_b below floor")),
             ["verdicts", "units", "reason == 'g_b below floor' (count)"])
    val.word("NOTRATED_NODB_N", str(sum(1 for u in units.values() if u["reason"].startswith("no D_b"))),
             ["verdicts", "units", "reason startswith 'no D_b' (count)"])
    dropped = V.get("dropped_models") or []
    flags["ANY_DROPPED"] = bool(dropped)
    val.word("DROPPED_NAMES", VV.names(dropped), ["verdicts", "dropped_models"])
    parts = []
    for m in dropped:
        if V["MQ"]["MQ2"].get(m, {}).get("dropped_from_g_star"):
            s = val.put(f"MQ2_DROP_{m}", "verdicts", MQ + ["MQ2", m, "share"], VV.pct1)
            parts.append(f"MQ2 dropped {VV.MODEL_NAME[m]} from the primary G\\* (search returned sources in {s} of its "
                         f"category answers, below 0.10)")
        elif m == S.GEM4 and V["MQ"]["MQ4"].get("drop_gemini"):
            s = val.put("MQ4_DROP", "verdicts", MQ + ["MQ4", "unresolved_share"], VV.pct1)
            parts.append(f"MQ4 dropped Gemini 4 Argon from the primary G\\* ({s} of its sources unresolved, above 0.20)")
    val.word("DROPPED_SENTENCE", ("; ".join(parts) + f". The gate is computed on {VV.names(panel)} and labelled "
                                  "accordingly; sensitivity S5 reverses the Gemini decision.") if parts else "",
             ["verdicts", "dropped_models", "MQ"])
    _opt(val, "MQ4_UNRES", "verdicts", MQ + ["MQ4", "unresolved_share"], VV.pct1)
    fl = [m for m in VV.MODELS if (V["MQ"]["MQ2"].get(m) or {}).get("flag_search_rarely_used")]
    flags["MQ2_ANY_FLAG"] = bool(fl)
    val.word("MQ2_FLAGGED", VV.names(fl), ["verdicts", "MQ", "MQ2", "flag_search_rarely_used"])
    _opt(val, "MQ3_SHARE", "verdicts", MQ + ["MQ3", "share"], VV.pct1)
    flags["MQ3_FLAG"] = bool(V["MQ"]["MQ3"].get("flag"))
    flags["MQ3_LOW"] = bool(V["MQ"]["MQ3"].get("low_coverage"))
    flags["MQ6_FLAG"] = bool(V["MQ"]["MQ6"].get("flag"))
    _opt(val, "MQ6_GSTAR_G", "verdicts", MQ + ["MQ6", "rho_gstar_g"], VV.r3)
    _opt(val, "MQ6_G_PI", "verdicts", MQ + ["MQ6", "rho_g_pi_s1"], VV.r3)
    flags["MQ5_FAILED"] = bool(V["MQ"]["MQ5"]["failed"])
    _opt(val, "MQ5_ZERO_SHARE", "verdicts", MQ + ["MQ5", "zero_share"], VV.pct0)
    flat = V["MQ"]["MQ5"].get("flat_substrates") or []
    val.word("MQ5_FLAT_CLAUSE", (f", and G\\* had a single value within {VV.joinand(VV.CAT[s] for s in flat)}"
                                 if flat else ", and no category had a single G\\* value"),
             ["verdicts", "MQ", "MQ5", "flat_substrates"])
    cl = Cells(val)
    rows = []
    for m in VV.MODELS:
        pk = MQ + ["MQ2", m]
        q = V["MQ"]["MQ2"].get(m) or {}
        status = "dropped (MQ2)" if q.get("dropped_from_g_star") else (
            "dropped (MQ4)" if m in dropped else ("search rarely used" if q.get("flag_search_rarely_used") else "kept"))
        rows.append([VV.MODEL_NAME[m], cl.f("verdicts", pk + ["answers"], VV.i0),
                     cl.f("verdicts", pk + ["with_source"], VV.i0), cl.f("verdicts", pk + ["share"], VV.pct1),
                     cl.f("verdicts", MQ + ["MQ4", "via_title_share"], VV.pct1) if m == S.GEM4 else DASH,
                     cl.f("verdicts", MQ + ["MQ4", "unresolved_share"], VV.pct1) if m == S.GEM4 else DASH, status])
    val.table("TABLE_MQ", md_table(["Model", "Category answers", "With a source", "Share (MQ2)",
                                    "Domain from title (MQ4)", "Unresolved (MQ4)", "Primary G\\*"], rows,
                                   ["l", "r", "r", "r", "r", "r", "l"]), cl.cells)
    cl = Cells(val)
    rows = []
    for prov in ("anthropic", "openai", "google"):
        pk = MQ + ["MQ8", prov]
        if not VV.has(V, pk):
            continue
        rows.append([VV.PROVIDER_NAME[prov], cl.f("verdicts", pk + ["answers"], VV.i0),
                     cl.f("verdicts", pk + ["with_citations"], VV.i0),
                     cl.f("verdicts", pk + ["share_with_citations"], VV.pct1), cl.f("verdicts", pk + ["cited"], VV.i0),
                     cl.f("verdicts", pk + ["share_cited_in_sources"], VV.pct1)])
    val.table("TABLE_MQ8", md_table(["Provider", "Answers", "With citations", "Share", "Cited URLs",
                                     "Also in sources"], rows), cl.cells)

    # ---------------- baseline (section 6)
    B = ["baseline"]
    psm = V["baseline"]["per_substrate_model"]
    keys = [k for k in psm]
    for nm, field, fmt in (("SRC", "share_with_source", VV.pct0), ("DOM", "domains_per_answer", VV.f1),
                           ("OWN", "share_any_brand_owned", VV.pct0)):
        refs = [("verdicts", B + ["per_substrate_model", k, field]) for k in keys]
        val.derive(f"BASE_{nm}_MIN", VV.d_min, refs, fmt)
        val.derive(f"BASE_{nm}_MAX", VV.d_max, refs, fmt)
    v = val.vals
    val.word("BASE_SENTENCE",
             f"Across categories and models (all three N3 models, as the baseline of §6 is defined), the share of "
             f"category answers whose search returned at least one source ranged from {v['BASE_SRC_MIN']} to "
             f"{v['BASE_SRC_MAX']}, grounded answers held a mean of {v['BASE_DOM_MIN']} to {v['BASE_DOM_MAX']} distinct "
             f"resolved domains, and the share of answers retrieving any registry brand's own domain ranged from "
             f"{v['BASE_OWN_MIN']} to {v['BASE_OWN_MAX']}.", ["verdicts", "baseline", "per_substrate_model"])
    cl = Cells(val)
    rows = []
    for s in VV.SUBS:
        pk = B + ["g_star_by_substrate", s]
        rows.append([VV.CAT_SHORT[s], cl.f("verdicts", pk + ["units"], VV.i0), cl.f("verdicts", pk + ["rated"], VV.i0),
                     cl.f("verdicts", pk + ["median"], VV.f1),
                     f"{cl.f('verdicts', pk + ['q1'], VV.f1)}--{cl.f('verdicts', pk + ['q3'], VV.f1)}",
                     cl.f("verdicts", pk + ["share_zero"], VV.pct0)])
    val.table("TABLE_GSTAR", md_table(["Category", "Units", "Rated", "G\\* median", "G\\* IQR", "Share at 0"], rows),
              cl.cells)
    cl = Cells(val)
    td = []
    for i, d in enumerate(V["baseline"]["top_domains"]):
        td.append(f"{d[0]} ({cl.f('verdicts', B + ['top_domains', i, 1], VV.i0)})")
    val.table("TOP_DOMAINS", "; ".join(td).replace("_", "\\_"), cl.cells)
    house = [k for k, u in units.items() if u.get("house_portal_domain")]
    if house:
        cl = Cells(val)
        hp = []
        for k in sorted(house):
            g = cl.f("verdicts", ["units", k, "G_star"], VV.f1) if units[k]["rated"] else None
            hp.append(f"{VV.brand_name(src, k)} ({'G* = ' + g if g else 'not rated'})")
        val.table("HOUSE_SENTENCE", "The three units with a house or portal domain (§2.3) are reported with that flag: "
                  + "; ".join(hp).replace("G*", "G\\*") + ".", cl.cells)
    else:
        val.word("HOUSE_SENTENCE", "[Synthetic test run: the three house or portal units are not among its units.]",
                 ["verdicts", "units", "house_portal_domain"])

    # ---------------- H1, H2, H3
    for h in ("H1_Sep_Presence", "H2_Sep_Consistency"):
        k = VV.SHORT[h]
        for i, c in enumerate(("S1", "S0")):
            _leg(val, f"{k}_{c}", ["legs", h, i])
    h3 = V["H3"]
    val.put("H3_NQ", "verdicts", ["H3", "n_qualifying_pairs"], VV.i0)
    for nm, key, fmt in (("H3_REL1", "rel1", VV.r3), ("H3_REL3", "rel3", VV.r3), ("H3_P", "p", VV.p4)):
        _opt(val, nm, "verdicts", ["H3", key], fmt)
    cl = Cells(val)
    rows = []
    for i, pr in enumerate(h3["pairs"]):
        rows.append([f"Runs {pr['pair'][0]} and {pr['pair'][1]}", cl.f("verdicts", ["H3", "pairs", i, "n"], VV.i0),
                     cl.f("verdicts", ["H3", "pairs", i, "rho_w"], VV.r3), "yes" if pr["qualifies"] else "no"])
    val.table("TABLE_H3", md_table(["Run pair", "Units rated in both", "$\\rho_w$", "Qualifies"], rows), cl.cells)

    # ---------------- conditional legs H4-H6
    st4, st6 = VV.cond_state(V, "H4_Sep_Ranking"), VV.cond_state(V, "H6_Sep_Coverage")
    st5 = VV.cond_state(V, "H5_Sep_Sentiment")
    cases["CASE_H4"] = st4["case"] if st4["case"] != "COMPUTED" else ("GATING" if st4["gating"] else "REPORTED")
    cases["CASE_H6"] = st6["case"]
    cases["CASE_H5"] = "INACTIVE" if st5["case"] == "INACTIVE" else "ACTIVE"
    val.word("H5_WORD", st5["word"], ["verdicts", "verdicts", "H5_Sep_Sentiment"])
    for k, st in (("H4", st4), ("H6", st6)):
        val.word(f"{k}_WORD", st["word"], ["verdicts", "(final leg record)", k])
        val.word(f"{k}_WHY", str(st.get("reason") or ""), ["verdicts", "reason", k])
        val.word(f"{k}_STAGE", st.get("stage") or DASH, ["verdicts", "stage of computation", k])
        if st["case"] == "COMPUTED":
            _leg(val, k, st["leg_path"])
            flags[f"{k}_BELOW_FLOOR"] = bool(VV.jget(V, st["leg_path"]).get("below_n_floor"))
        else:
            for s_ in ("N", "RHO", "P", "LO", "HI"):
                val.word(f"{k}_{s_}", DASH, ["verdicts", k, "(not computed)"])
            flags[f"{k}_BELOW_FLOOR"] = False
    s1v = (VV.jget(V, st4["src_path"]) if st4["case"] == "COMPUTED" else {}).get("stage1_verdict")
    val.word("H4_STAGE1", str(s1v or DASH), ["verdicts", "H4_ranking_source", "stage1_verdict"])

    # ---------------- gate
    gl = V["gate"]["legs"]
    fals = [h for h in VV.GATE_LEGS if gl.get(h) == "FALSIFIED"]
    val.word("FAIL_LEGS", _short(fals), ["verdicts", "gate", "legs"])
    val.word("FAIL_LEGS_PLAIN", _plain(fals), ["verdicts", "gate", "legs"])
    val.word("FAIL_VERB", _verb(fals), ["verdicts", "gate", "legs"])
    notc = [h for h in VV.GATE_LEGS if gl.get(h) != "CONFIRMED"]
    val.word("NOTCONF_LEGS_PLAIN", VV.joinand(f"{VV.PLAIN[h]} ({VV.SHORT[h]}) {gl[h]}" for h in notc),
             ["verdicts", "gate", "legs"])
    val.word("NOTCONF_LEGS_WORDS", VV.joinand(f"{VV.SHORT[h]} was {gl[h]}" for h in notc), ["verdicts", "gate", "legs"])
    und = [h for h in ("H1_Sep_Presence", "H2_Sep_Consistency") if gl.get(h) == "UNDETERMINED"]
    val.word("UNDET_LEGS", _short(und), ["verdicts", "gate", "legs"])
    val.word("UNDET_VERB", _verb(und), ["verdicts", "gate", "legs"])
    val.word("UNDET_LEGS_PLAIN", _plain(und), ["verdicts", "gate", "legs"])
    down = list(dict.fromkeys(fg["downgraded_by"]))
    val.word("DOWN_LEGS", _short(down), ["verdicts", "gate notes / stage_C2 re-issues"])
    val.word("DOWN_LEGS_PLAIN", _plain(down), ["verdicts", "gate notes / stage_C2 re-issues"])
    val.word("DOWN_VERB", _verb(down), ["verdicts", "gate notes / stage_C2 re-issues"])
    hist = []
    c1_down = [h for h in down if h not in [r[0] for r in fg["reissues"]]]
    if c1_down:
        hist.append(f"At Stage C1, {_short(c1_down)} (computed from its score at C1) downgraded the PASS to MARGINAL.")
    if c2 is None:
        hist.append(f"This is the Stage C1 verdict ({fg['c1']}); Stage C2 has not run, so H4 and H6 are pending and "
                    "the verdict may still be re-issued, downgrade only.")
    else:
        when = str(c2.get("appended_utc") or "")[:16].replace("T", " ")
        moved = [(h, b, a) for h, b, a in fg["reissues"] if b != a]
        if moved:
            hist.append(f"At Stage C1 the gate was {fg['c1']}; Stage C2 (appended {when} UTC) re-issued it: " +
                        "; ".join(f"{VV.SHORT[h]} turned {b} into {a}" for h, b, a in moved) + " (downgrade only).")
        elif fg["reissues"]:
            hist.append(f"Stage C2 (appended {when} UTC) re-issued the gate after "
                        f"{_short([r[0] for r in fg['reissues']])} without changing it ({fg['final']}).")
        else:
            hist.append(f"Stage C2 (appended {when} UTC) computed no leg that re-issues the gate.")
    val.word("GATE_HISTORY", " ".join(hist), ["verdicts", "gate", "stage_C2", "gate_reissued"])

    # ---------------- H7 and Part II
    s7 = VV.h7_state(V)
    cases["CASE_H7"] = s7["case"]
    flags["H7_IS_CONFIRMED"] = s7["case"] == "CONFIRMED"
    flags["H7_IS_FALSIFIED"] = s7["case"] == "FALSIFIED"
    val.word("H7_WORD", str(s7.get("word") or DASH), ["verdicts", "stage_C2", "H7_Struct_Gap"])
    if "leg_path" in s7:
        _leg(val, "H7", s7["leg_path"])
    else:
        for s_ in ("N", "RHO", "P", "LO", "HI"):
            val.word(f"H7_{s_}", DASH, ["verdicts", "H7", "(not computed)"])
    _opt(val, "H7_RHO_P", "verdicts", ["stage_C2", "rho_sdri_p_s0"], VV.r3)
    _opt(val, "H7_PARTIAL", "verdicts", ["stage_C2", "partial_rho_sdri_gstar_given_p_s0"], VV.r3)
    collected = s7["case"] not in ("NOT_COLLECTED", "PENDING")
    flags["PART2_COLLECTED"] = collected
    if c2 is None:
        cases["CASE_PART2"] = "PENDING"
    elif collected:
        cases["CASE_PART2"] = "COLLECTED"
    else:
        cases["CASE_PART2"] = "LOCKED_NOT_COLLECTED" if ctx["part2_locked"] else "NOT_LOCKED"
    if ctx["part2_locked"]:
        val.word("PART2_TITLE_LINE", f"\\texttt{{v1.13-audit-r1}} (commit \\texttt{{ {ctx['part2_commit']} }})",
                 ["git", "refs/tags/v1.13-audit-r1"])
        val.word("PART2_LOCK_SENTENCE",
                 f"Part II was locked separately at tag `v1.13-audit-r1` (commit `{ctx['part2_commit']}`) with its own "
                 f"anchor record; its audit could start only 24 hours after the pre-registrant received the locked "
                 f"text ({ctx['receipt_utc']}) and never between 17 and 22 November 2026 (protocol §4, §8).",
                 ["git", "anchor/audit_anchor_v1_13.json", "anchor/audit_receipt_v1_13.json"])
    else:
        val.word("PART2_TITLE_LINE", "not locked before Stage C2" if c2 is not None else "not locked at Stage C1",
                 ["git", "refs/tags/v1.13-audit-r1 (absent)"])
        val.word("PART2_LOCK_SENTENCE", "Part II was not locked before Stage C2, so no website was fetched."
                 if c2 is not None else "Part II had not been locked when Stage C1 ran.",
                 ["git", "refs/tags/v1.13-audit-r1 (absent)"])
    rows_s = src["sdri"]["rows"]
    if collected:
        aud = [r for r in rows_s if str(r.get("phantom")) != "1"]
        idx = {id(r): i for i, r in enumerate(rows_s)}
        P = lambda r, c: ("sdri", ["rows", idx[id(r)], c])                                       # noqa: E731
        n_aud = val.word("SDRI_N_AUDITED", str(len(aud)), ["sdri", "rows", "phantom != 1 (count)"])
        n_ok = val.derive("SDRI_P1_OK", VV.d_count_eq, [P(r, "p1_outcome") for r in aud], VV.i0, consts=("ok",))
        sh_ok = val.derive("SDRI_P1_SHARE", VV.d_share_eq, [P(r, "p1_outcome") for r in aud], VV.pct0, consts=("ok",))
        n_sd = val.derive("SDRI_RATED", VV.d_count, [P(r, "SDRI") for r in aud], VV.i0)
        med = val.derive("SDRI_MEDIAN", VV.d_median, [P(r, "SDRI") for r in aud], VV.f1)
        flag = float(sum(1 for r in aud if r.get("p1_outcome") == "ok")) / len(aud) < 0.80 if aud else False
        val.word("SDRI_SENTENCE",
                 f"Part II's first pass recorded {n_aud} brands with an own domain; the home page was fetched for {n_ok} "
                 f"({sh_ok}{', below the 80% at which AQ2 flags the audit' if flag else '; AQ2 flags a share below 80%'}), "
                 f"SDRI was rated for {n_sd}, and the median SDRI was {med}. The table gives the indicators per "
                 f"category.",
                 ["sdri", "rows"])
        cl = Cells(val)
        rows = []
        for s in VV.SUBS:
            rs = [r for r in aud if r["substrate"] == s]
            if not rs:
                continue
            cells = [VV.CAT_SHORT[s],
                     val.derive(f"SDRI_{s}_N", VV.d_count, [P(r, "substrate") for r in rs], VV.i0),
                     val.derive(f"SDRI_{s}_OK", VV.d_count_eq, [P(r, "p1_outcome") for r in rs], VV.i0, ("ok",)),
                     val.derive(f"SDRI_{s}_MED", VV.d_median, [P(r, "SDRI") for r in rs], VV.f1)
                     if any(r.get("SDRI") not in ("", None) for r in rs) else DASH]
            for j in range(1, 9):
                refs = [P(r, f"i{j}") for r in rs]
                cells.append(val.derive(f"SDRI_{s}_I{j}", VV.d_share_eq, refs, VV.pct0, ("1",))
                             if any(r.get(f"i{j}") not in ("", None) for r in rs) else DASH)
            rows.append(cells)
        val.table("TABLE_SDRI", md_table(["Category", "Audited", "Home page", "Median SDRI"] +
                                         [f"({j})" for j in range(1, 9)], rows), cl.cells)
    else:
        val.word("SDRI_SENTENCE", "", ["sdri (not collected)"])
        val.word("TABLE_SDRI", "", ["sdri (not collected)"])

    # ---------------- legs table
    cl = Cells(val)
    rows = []

    def legrow(label, against, role, path, word, stat=None):
        stat = stat or path + ["rho_w"]
        ci = (f"[{cl.f('verdicts', path + ['ci90', 'lo'], VV.r3)}, {cl.f('verdicts', path + ['ci90', 'hi'], VV.r3)}]"
              if VV.has(V, path + ["ci90", "lo"]) else DASH)
        rows.append([label, against, role, cl.f("verdicts", path + ["n"], VV.i0) if path else DASH,
                     cl.f("verdicts", stat, VV.r3) if stat else DASH, ci,
                     cl.f("verdicts", path + ["p"], VV.p4) if path else DASH, f"**{word}**"])
    for h, against in (("H1_Sep_Presence", "Presence $P$"), ("H2_Sep_Consistency", "Consistency $C^*$")):
        for i, c in enumerate(("S1", "S0")):
            legrow(f"{VV.SHORT[h]} ({c})", f"{against}, {c}", "gate", ["legs", h, i], V["verdicts"][h])
    rows.append(["H3", "run against run", "gate", cl.f("verdicts", ["H3", "n_qualifying_pairs"], VV.i0) + " pairs",
                 cl.f("verdicts", ["H3", "rel3"], VV.r3) + " (rel3)", DASH, cl.f("verdicts", ["H3", "p"], VV.p4),
                 f"**{V['verdicts']['H3_Run_Reliability']}**"])
    for h, st, against in (("H4_Sep_Ranking", st4, "Ranking $R^*_{S1}$"), ("H5_Sep_Sentiment", st5, "Sentiment $S$"),
                           ("H6_Sep_Coverage", st6, "Coverage Cov\\*")):
        if st["case"] == "INACTIVE":
            rows.append([VV.SHORT[h], against, "conditional", DASH, DASH, DASH, DASH, f"**{st['word']}**"])
        elif st["case"] in ("PENDING", "UNAVAILABLE") or "leg_path" not in st:
            rows.append([VV.SHORT[h], against, "conditional", DASH, DASH, DASH, DASH,
                         f"**{st['word']}** ({'pending' if st['case'] == 'PENDING' else 'score not available'})"])
        else:
            role = "conditional, gating" if st["gating"] else "conditional, reported"
            legrow(VV.SHORT[h], against, role, st["leg_path"], st["word"])
    if "leg_path" in s7:
        legrow("H7", "SDRI (one-sided)", "secondary", s7["leg_path"], s7["word"])
    else:
        rows.append(["H7", "SDRI (one-sided)", "secondary", DASH, DASH, DASH, DASH,
                     f"**{s7['word']}** (Part II not collected)" if s7["word"] else "pending (Stage C2)"])
    val.table("TABLE_LEGS", md_table(["Leg", "G\\* against", "Role", "$n$", "$\\rho_w$", "90% interval", "$p$",
                                      "Verdict"], rows, ["l", "l", "l", "r", "r", "r", "r", "l"]), cl.cells)

    # ---------------- sensitivities
    SN = V.get("sensitivities") or {}
    VC = V.get("verdict_changes") or {}
    cl = Cells(val)
    rows = []
    for key, label in VV.SENS:
        if key not in SN:
            continue
        sp = ["sensitivities", key]
        ch = VC.get(key) or {}
        rows.append([label] + [cl.f("verdicts", sp + ["rho", h, i], VV.r3) for h in ("H1_Sep_Presence",
                                                                                  "H2_Sep_Consistency")
                               for i in (0, 1)] +
                    [cl.f("verdicts", sp + ["rel3"], VV.r3), SN[key].get("gate", DASH), _changes(ch)])
    val.table("TABLE_SENS", md_table(["Sensitivity", "H1 S1", "H1 S0", "H2 S1", "H2 S0", "rel3", "Gate",
                                      "Verdicts that differ"], rows, ["l", "r", "r", "r", "r", "r", "l", "l"]), cl.cells)
    changed = sorted({k.split("_")[0] for k, v in VC.items() if v}, key=lambda x: int(x[1:]))
    val.word("SENS_CHANGES_SENTENCE",
             (f"A verdict would differ under {VV.joinand(changed)} (listed in the table); the primary verdicts stand."
              if changed else "No sensitivity analysis would change a verdict."),
             ["verdicts", "verdict_changes"])
    s11 = VC.get("S11_without_Denon") or {}
    val.word("S11_SENTENCE", ("Without the Denon unit (S11), " + VV.joinand(f"{VV.SHORT[h]} would be {w[0]}"
                                                                           for h, w in s11.items()) + "."
                              if s11 else "Without the Denon unit (S11) no verdict changes."),
             ["verdicts", "verdict_changes", "S11_without_Denon"])
    val.word("S7_SENTENCE", "" if "S7_legacy_t3" in SN else
             "Sensitivity S7 (AIAS 2.0 $t_3$ comparators) was not computed: the scorer was given no $t_3$ profile "
             "input.", ["verdicts", "sensitivities", "S7_legacy_t3"])
    lo = SN.get("S8_leave_one_substrate_out") or {}
    cl = Cells(val)
    rows = []
    for s in VV.SUBS:
        if s not in lo:
            continue
        sp = ["sensitivities", "S8_leave_one_substrate_out", s]
        rows.append([VV.CAT_SHORT[s]] + [cl.f("verdicts", sp + ["rho", h, i], VV.r3) for h in ("H1_Sep_Presence",
                                                                                           "H2_Sep_Consistency")
                                         for i in (0, 1)] +
                    [cl.f("verdicts", sp + ["rel3"], VV.r3),
                     ", ".join(f"{VV.SHORT[h]} {w}" for h, w in lo[s]["verdicts"].items())])
    val.table("TABLE_S8", md_table(["Left out", "H1 S1", "H1 S0", "H2 S1", "H2 S0", "rel3", "Verdicts"], rows,
                                   ["l", "r", "r", "r", "r", "r", "l"]), cl.cells)
    r8 = [("verdicts", ["sensitivities", "S8_leave_one_substrate_out", s, "rho", "H1_Sep_Presence", 0]) for s in lo
          if VV.has(V, ["sensitivities", "S8_leave_one_substrate_out", s, "rho", "H1_Sep_Presence", 0])]
    q8 = [("verdicts", ["sensitivities", "S8_leave_one_substrate_out", s, "rel3"]) for s in lo
          if VV.has(V, ["sensitivities", "S8_leave_one_substrate_out", s, "rel3"])]
    for nm, refs, fn in (("S8_H1_LO", r8, VV.d_min), ("S8_H1_HI", r8, VV.d_max), ("S8_REL_LO", q8, VV.d_min),
                         ("S8_REL_HI", q8, VV.d_max)):
        if refs:
            val.derive(nm, fn, refs, VV.r3)
        else:
            val.word(nm, DASH, ["verdicts", "sensitivities", "S8 (not computed)"])

    # ---------------- appendix: per-brand table
    cl = Cells(val)
    rows = []
    rated = sorted((k for k, u in units.items() if u["rated"]), key=lambda k: (k.split("|")[0], -units[k]["G_star"], k))
    for k in rated:
        up, dp = ["units", k], ["descriptives", k]
        mix = [cl.f("verdicts", dp + ["mix", c], VV.pct0) for c in ("brand_owned", "reference", "review_editorial",
                                                                  "retailer", "news", "forum_ugc", "other")]
        nm = VV.brand_name(src, k).replace("&", "\\&") + (" $\\dagger$" if units[k].get("house_portal_domain") else "")
        rows.append([VV.CAT_SHORT[k.split("|")[0]], nm, cl.f("verdicts", up + ["m"], VV.i0),
                     cl.f("verdicts", up + ["g"], VV.i0), cl.f("verdicts", up + ["o"], VV.i0),
                     cl.f("verdicts", up + ["G_star"], VV.f1), cl.f("verdicts", dp + ["d"], VV.f1)] + mix)
    val.table("TABLE_BRANDS", md_table(["Category", "Brand", "$m$", "$g$", "$o$", "G\\*", "$d$", "own", "ref", "rev",
                                        "ret", "news", "UGC", "other"], rows,
                                       ["l", "l"] + ["r"] * 12), cl.cells)
    cl = Cells(val)
    nodb = [k for k, u in sorted(units.items()) if u["reason"].startswith("no D_b")]
    low = [k for k, u in sorted(units.items()) if u["reason"] == "g_b below floor"]
    parts = []
    if nodb:
        parts.append("Without an own domain (not rated; reported apart): " + "; ".join(
            f"{VV.brand_name(src, k)} ($m$ = {cl.f('verdicts', ['units', k, 'm'], VV.i0)}, "
            f"$g$ = {cl.f('verdicts', ['units', k, 'g'], VV.i0)})" for k in nodb) + ".")
    if low:
        parts.append("Below the floor of six grounded answers: " + "; ".join(
            f"{VV.brand_name(src, k)} ($g$ = {cl.f('verdicts', ['units', k, 'g'], VV.i0)})" for k in low) + ".")
    val.table("NOTRATED_SENTENCE", " ".join(parts) or "Every unit was rated.", cl.cells)

    # ---------------- declarations
    flags["COI_CHEIL"] = bool(ctx["coi_cheil"])
    present = [k for k in VV.CHEIL_UNITS if f"{k[0]}|{k[1]}" in units]
    val.word("CHEIL_SENTENCE",
             "Cheil Worldwide, a Samsung affiliate, or its Iris unit has worked for five brands of these registries: "
             "Chevrolet (GM Korea ad, 2017), BMW (BMW Group UK consumer PR, 2018), Bentley (Americas experiential, "
             "2021), Jack Daniel's (UK digital, 2022) and Eucerin (Beiersdorf search marketing, 2024), as recorded in "
             "v0.62 DEVIATIONS Entry 0, Part F. This study performs no brand selection, so they stay in the registry; "
             "no sensitivity analysis without them was pre-registered." if ctx["coi_cheil"] else "",
             ["CLAUDE.md COI notes, Nov 11, 2026", f"units present: {len(present)}"])
    return val, cases, flags


# =========================================================================== checks and main
WAIVER_PHRASE = "waived the 24-hour review on 2026-11-10 at 20:26 CT"


def deviations_text(synthetic):
    if synthetic:
        t = "[Synthetic test run: the deviations record was not read.]"
        return t, t, ["synthetic"]
    if not VV.DEVIATIONS.exists():
        raise FillError(f"{VV.DEVIATIONS} not found (a locked file of v1.13-prereg-r1)")
    txt = VV.DEVIATIONS.read_text(encoding="utf-8")
    if WAIVER_PHRASE not in txt:
        raise FillError(f"{VV.DEVIATIONS} no longer records '{WAIVER_PHRASE}' (Method §2.9 states it)")
    n = len([m for m in re.findall(r"(?m)^## Entry (\d+)\b", txt) if int(m) >= 1])
    rel = "osf/methodology/v1_13/anchor/DEVIATIONS.md"
    if n:
        ent = f"{n} entr{'y' if n == 1 else 'ies'} after the lock"
        return (f"Deviations are recorded in `{rel}` ({ent}), each before the step it concerns.",
                f"deviations recorded in `{rel}` ({ent}).", [rel])
    return (f"No deviation after the lock is recorded in `{rel}` (its Entries 0 and 0a were written before the lock).",
            f"no deviation after the lock (`{rel}`).", [rel])


def real_context(V, interim):
    if VV.is_synthetic(V):
        raise FillError("the verdict file is synthetic (synthetic_fixture present): use --synthetic")
    if V.get("stage_C2") is None and not interim:
        raise FillError("Stage C2 has not run (no stage_C2 in the verdict file); pass --interim for a Stage C1 draft")
    commit = VV.tag_commit(VV.PREREG_TAG)
    if not commit:
        raise FillError(f"tag {VV.PREREG_TAG} not found in {ROOT}")
    anchor = json.loads(VV.GIT_ANCHOR.read_text(encoding="utf-8")) if VV.GIT_ANCHOR.exists() else {}
    if anchor.get("commit") != commit:
        raise FillError(f"{VV.GIT_ANCHOR.name} does not name the tag's commit {commit}")
    act = S.activation(anchor)
    if dict(V["gate"]["active"]) != act:
        raise FillError(f"conditional legs {V['gate']['active']} differ from the anchor's activation record {act}")
    rs = V.get("H4_ranking_source") or ((V.get("stage_C2") or {}).get("ranking") or {}).get("H4_ranking_source") or {}
    if rs.get("dry_run"):
        raise FillError("H4 was computed from a v1.14 dry-run Stage 1 file")
    cs = V.get("H6_coverage_source") or ((V.get("stage_C2") or {}).get("coverage") or {}).get("H6_coverage_source") or {}
    want6 = ((anchor.get("conditional_legs") or {}).get("H6_Sep_Coverage") or {}).get("commit")
    if cs.get("sha256") and cs.get("v1_12_commit") != want6:
        raise FillError(f"H6's Cov* source names v1.12 commit {cs.get('v1_12_commit')}, not the anchored {want6}")
    missing = [k for k in S.HOUSE_PORTAL_UNITS if f"{k[0]}|{k[1]}" not in V["units"]]
    if missing or len(V["units"]) != 112:
        raise FillError(f"the verdict file has {len(V['units'])} units (expected 112; house/portal missing: {missing})")
    p2 = VV.tag_commit(VV.AUDIT_TAG)
    receipt = "receipt not recorded"
    if p2:
        aa = json.loads(VV.AUDIT_ANCHOR.read_text(encoding="utf-8")) if VV.AUDIT_ANCHOR.exists() else {}
        if aa.get("commit") != p2:
            raise FillError(f"tag {VV.AUDIT_TAG} exists but {VV.AUDIT_ANCHOR.name} does not name its commit")
        if VV.AUDIT_RECEIPT.exists():
            receipt = "received " + str(json.loads(VV.AUDIT_RECEIPT.read_text(encoding="utf-8")).get(
                "received_utc", "?"))[:16].replace("T", " ") + " UTC"
    if "leg" in (V.get("stage_C2") or {}) and not p2:
        raise FillError("H7 was computed but tag v1.13-audit-r1 does not exist (Part II cannot have been collected)")
    return {"prereg_commit": commit[:10], "prereg_tag_utc": VV.tag_date_utc(VV.PREREG_TAG),
            "part2_locked": bool(p2), "part2_commit": (p2 or "")[:10], "receipt_utc": receipt}


def synthetic_context(V):
    if not VV.is_synthetic(V):
        raise FillError("--synthetic given but the verdict file is not synthetic (no synthetic_fixture)")
    part2 = V["synthetic_fixture"].get("part2")
    if part2 not in ("collected", "not_run", "held"):
        raise FillError(f"synthetic_fixture.part2 = {part2!r}")
    return {"prereg_commit": "synthetic run: tag not verified", "prereg_tag_utc": "[synthetic run: not read]",
            "part2_locked": part2 != "held", "part2_commit": "synthetic: not verified",
            "receipt_utc": "synthetic run: receipt not read"}


def fill(verdicts, sdri=None, out=None, fig_dir=None, synthetic=False, interim=False, coi_cheil=False,
         template=TEMPLATE):
    src = VV.load_sources(verdicts, sdri)
    V = src["verdicts"]
    ctx = synthetic_context(V) if synthetic else real_context(V, interim)
    try:
        VV.check_consistency(src)
    except VV.Inconsistent as e:
        raise FillError(f"inconsistent verdict file: {e}")
    ctx["deviations"] = deviations_text(synthetic)
    ctx["coi_cheil"] = coi_cheil
    fig_dir = fig_dir or "../../reports/figs/v113"
    val, cases, flags = compute(src, synthetic, fig_dir, ctx)
    tpl = Path(template).read_text(encoding="utf-8")
    text = render(tpl, val.vals, cases, flags)
    if out:
        out = Path(out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
        prov = {"verdicts": str(verdicts), "sdri": str(sdri), "synthetic": synthetic, "interim": interim,
                "coi_cheil": coi_cheil, "cases": cases, "flags": flags, "values": val.prov}
        Path(str(out).replace(".md", "_provenance.json")).write_text(
            json.dumps(prov, indent=1, ensure_ascii=False, default=str), encoding="utf-8")
    return text, val, cases, flags


def main(argv=None):
    ap = argparse.ArgumentParser(description="Fill the v1.13 Grounding Paper A template from the scorers' outputs")
    ap.add_argument("--verdicts", type=Path, default=VV.VERDICTS_JSON)
    ap.add_argument("--sdri", type=Path, default=None, help=f"Part II SDRI table (default {VV.SDRI_CSV} if it exists)")
    ap.add_argument("--fig-dir", default=None, help="figure directory as the paper references it "
                                                     "(default ../../reports/figs/v113, relative to papers/v1_13)")
    ap.add_argument("--out", type=Path, default=HERE / "v1_13_paper_draft.md")
    ap.add_argument("--synthetic", action="store_true")
    ap.add_argument("--interim", action="store_true", help="real mode: allow a Stage C1-only draft (labelled interim)")
    ap.add_argument("--coi-cheil", action="store_true",
                    help="add the optional Cheil Worldwide / Iris COI sentence (pending decision; off by default)")
    a = ap.parse_args(argv)
    if a.synthetic and str(a.out.resolve()).startswith(str(ROOT.resolve())):
        sys.exit("[fill v1.13] REFUSED: synthetic output must be written outside the repository")
    sdri = a.sdri if a.sdri else (VV.SDRI_CSV if (not a.synthetic and VV.SDRI_CSV.exists()) else None)
    try:
        text, val, cases, flags = fill(a.verdicts, sdri, a.out, a.fig_dir, a.synthetic, a.interim, a.coi_cheil)
    except (FillError, VV.Missing) as e:
        print(f"[fill v1.13] REFUSED: {e}", file=sys.stderr)
        return 3
    print(f"[fill v1.13] wrote {a.out} ({len(text.split())} words); cases {cases}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
