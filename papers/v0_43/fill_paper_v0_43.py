#!/usr/bin/env python3
"""
fill_paper_v0_43.py -- fills papers/v0_43/v0_43_paper_template.md from the Stage 1 scorer's output.

The template holds the whole paper. Introduction and Method are fixed text written from PRE_REGISTRATION_v0_43.md
(r1 + C1-C10, locked at tag v0.43-prereg-r1; hypotheses and thresholds quoted with their section numbers). Results and
Discussion are written in advance as alternative sentences, one per outcome the pre-registration allows, inside blocks
this script selects from the verdicts (template engine forked unchanged from papers/v1_12/fill_paper_v1_12.py, branch
v1.12-paper):

  {% switch CASE_PRES %} {% case CONFIRMED %} ... {% case UNDETERMINED_N|UNDETERMINED_RHO %} ... {% endswitch %}
  {% if FLAG %} ... {% else %} ... {% endif %}
  {{NAME}}      a value read from a machine output (papers/v0_43/v043_values.py records its JSON path)

Every switch must match exactly one case; an unknown flag or value is an error; the output may contain no `{{`, `{%`.
No number is typed here: values are leaves of the verdicts JSON or of the pull summary, formatted by named functions;
the provenance of every value is written beside the paper. Verdict words and labels are printed exactly as the scorer
wrote them.

Checks before filling, in every mode:
  - the lock: tag v0.43-prereg-r1 exists and resolves to commit 8c96d9cf, its tagger date is 2026-11-11 06:31 UTC,
    osf/v43/anchor/osf_anchor_v0_43.json names that commit, anchor/DEVIATIONS.md records the lock time, and every file
    in prereg/LOCK_MANIFEST_v0_43.sha256 still has its locked SHA-256 (so the scorer that ran is the locked one);
  - consistency (v043_values.check_consistency): every verdict, label, reason and flag re-derived with the locked
    scorer's own verdict() and specs; each test's rho recomputed from the scorer's unit table with its rho_pw;
    n = sum of n per category; intervals ordered; MC pass_ values follow their rules;
  - the pull summary agrees with MC_Weekly (requests, ok, missing, re-sends).
Real mode additionally: the verdicts carry no synthetic_fixture key, used the three pulls main1-3 and 10,000 draws,
cover all 112 units, and the stored raw records hold 28 requests per pull, each pull starting at least 24 hours after
the previous one was stored. Synthetic mode (--synthetic) requires synthetic verdicts, says so in the text and refuses
to write inside the repository.

Pending decision (not made here): Samsung's agency Cheil Worldwide / its Iris unit has worked for five registry brands
of this study (Chevrolet, BMW, Bentley, Jack Daniel's, Eucerin). --coi-cheil adds one COI sentence about it; it is OFF
by default and is switched on only on the pre-registrant's decision.

Usage (real run, after `score_v0_43.py --stage 1`; see papers/v0_43/PIPELINE.md):
  python3 papers/v0_43/fill_paper_v0_43.py
Synthetic test:
  python3 papers/v0_43/fill_paper_v0_43.py --synthetic \
      --verdicts papers/v0_43/tests/fixtures/SYNTHETIC_lead_v43_stage1_verdicts.json \
      --pulls papers/v0_43/tests/fixtures/SYNTHETIC_lead_v43_pulls.json \
      --fig-dir /tmp/v043_pipeline_test/figs --out /tmp/v043_pipeline_test/paper/v0_43_paper_draft.md
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import v043_values as VV  # noqa: E402

ROOT = VV.ROOT
TEMPLATE = HERE / "v0_43_paper_template.md"
ANCHOR = ROOT / "osf/v43/anchor/osf_anchor_v0_43.json"
DEVIATIONS = ROOT / "osf/v43/anchor/DEVIATIONS.md"
RAW_DIR = ROOT / "osf/v43/data/trends_raw"
VERDICTS = ROOT / "osf/v43/v43_stage1_verdicts.json"


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
    vis = lambda t: len(re.sub(r"\$[^$]*\$|\\[a-z]+|[{}`]", "x", t))      # noqa: E731  visible width, roughly
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
        if not VV.finite(raw):
            return missing
        s = fmt(raw)
        self.cells.append((s, src, path, fmt.__name__))
        return s


# =========================================================================== values
SPEC_TEXT = {"H_Pred_Presence": ("$P$", "$L$"), "H_Pred_Presence_SA": ("$P$", "$L$"),
             "H_Pred_Presence_Momentum": ("$P$", "$L$, $M$"), "H_Pred_Consistency": ("$C^*$", "$L$, $P$")}
OUTCOME_TEXT = {"H_Pred_Presence": "$Y$", "H_Pred_Presence_SA": "$Y^{SA}$", "H_Pred_Presence_Momentum": "$Y$",
                "H_Pred_Consistency": "$Y$"}
FLAG_MEANING = {"criterion doubtful": "in these categories Presence did not show the same-time link with search "
                                      "level that v0.25 found, so the criterion itself is in doubt.",
                "outcome unreliable": "the three pulls did not agree well enough on each brand's change, so the "
                                      "outcome is noisy.",
                "mostly plain search terms": "fewer than half the brands were searched by topic, so plain search terms "
                                             "that also catch other meanings dominate the outcome."}


def _word(T):
    return T["verdict"] + (" (REVERSED)" if VV.reversed_label(T) else "")


def compute(src, synthetic, fig_dir, commit, deviations, coi_cheil=False):
    V = src["verdicts"]
    val = VV.Values(src)
    cases, flags = {}, {"COI_CHEIL": bool(coi_cheil)}
    val.word("PREREG_TAG", VV.EXPECTED_PREREG_TAG, ["verdicts", "prereg"])
    val.word("PREREG_COMMIT", commit[:10], ["git", f"refs/tags/{VV.EXPECTED_PREREG_TAG}^{{commit}}"])
    val.word("FIG_DIR", str(fig_dir), ["argument --fig-dir"])
    val.word("FIG_CAPTION", "SYNTHETIC TEST DATA --- NOT RESULTS." if synthetic else "", ["synthetic flag"])
    val.word("SYN_NOTE", ("**[SYNTHETIC TEST RUN. Every number in this document comes from invented brands and "
                          "synthetic search-interest responses scored by the locked scorer; nothing here is a result.]**")
             if synthetic else "", ["synthetic flag"])
    val.word("DEV_SENTENCE", deviations[0], deviations[2])
    val.word("DEV_STATUS", deviations[1], deviations[2])

    # ---------------- review additions (14 Nov 2026): who left which test (names from unit_table), sign of the
    # primary rho, and a real-data-only sentence on one sampling swing (verified in data/trends_raw, see template)
    flags["V043_REAL"] = not synthetic
    _r = V["tests"]["H_Pred_Presence"].get("rho")
    flags["PRES_NEG"] = _r is not None and _r < 0
    _ut = V["unit_table"]

    def _left(pred):
        parts = []
        for sub, cat in VV.CAT_SHORT.items():
            ns = [u["unit"] for u in _ut if u["sub"] == sub and pred(u)]
            if ns:
                parts.append(f"{VV.joinand(ns)} ({cat.lower()})")
        return "; ".join(parts)
    for key, pred, col in (("NOY", lambda u: u["Y"] is None, "Y"),
                           ("NOSA", lambda u: u["Y"] is not None and u["Y_SA"] is None, "Y_SA"),
                           ("NOM", lambda u: u["Y"] is not None and u["M"] is None, "M")):
        txt = _left(pred)
        flags[f"ANY_{key}"] = bool(txt)
        val.word(f"{key}_LIST", txt, ["verdicts", "unit_table", col])

    # ---------------- flags (the scorer's words)
    fl = list(V["flags"])
    flags["ANY_FLAG"] = bool(fl)
    val.word("FLAG_LIST", VV.joinand(f"“{f}”" for f in fl), ["verdicts", "flags"])
    val.word("FLAG_PLURAL", "s" if len(fl) > 1 else "", ["verdicts", "flags"])
    val.word("FLAG_MEANING", " ".join(FLAG_MEANING[f][0].upper() + FLAG_MEANING[f][1:] if i else FLAG_MEANING[f]
                                      for i, f in enumerate(fl)), ["verdicts", "flags"])

    # ---------------- pulls and checks
    P_ = src["pulls"]["steps"]
    parts = []
    for k, step in enumerate(VV.STEPS):
        a = val.put(f"PULL{k + 1}_FIRST", "pulls", ["steps", step, "first_utc"], VV.utc_min)
        b = val.put(f"PULL{k + 1}_LAST", "pulls", ["steps", step, "last_utc"], VV.utc_min)
        parts.append((a, b))
    g1 = val.derive("GAP12", VV.d_hours, [("pulls", ["steps", "main1", "last_utc"]),
                                          ("pulls", ["steps", "main2", "first_utc"])], VV.f1)
    g2 = val.derive("GAP23", VV.d_hours, [("pulls", ["steps", "main2", "last_utc"]),
                                          ("pulls", ["steps", "main3", "first_utc"])], VV.f1)
    val.word("PULLS_SENTENCE",
             f"The three main pulls ran from {parts[0][0]} to {parts[0][1]}, from {parts[1][0]} to {parts[1][1]} and "
             f"from {parts[2][0]} to {parts[2][1]} (UTC); the second and third started {g1} and {g2} hours after "
             f"the last request of the pull before.", ["pulls", "steps"])
    MC = ["manipulation_checks"]
    per = val.put("MCW_REQ_PER_PULL", "pulls", ["steps", "main1", "records"], VV.i0)
    val.put("MCW_REQ", "verdicts", MC + ["MC_Weekly", "requests"], VV.i0)
    val.put("MCW_OK", "verdicts", MC + ["MC_Weekly", "ok"], VV.i0)
    nm = V["manipulation_checks"]["MC_Weekly"]["missing"]
    val.put("MCW_MISSING", "verdicts", MC + ["MC_Weekly", "missing"], VV.i0)
    rs = val.put("MCW_RESENT", "verdicts", MC + ["MC_Weekly", "resent"], VV.i0)
    nr = V["manipulation_checks"]["MC_Weekly"]["resent"]
    miss = (f"{val.vals['MCW_MISSING']} {'was' if nm == 1 else 'were'} recorded as missing after their re-sends"
            if nm else "none was missing")
    resent = (f"{rs} re-send{'' if nr == 1 else 's'} {'was' if nr == 1 else 'were'} made in all" if nr
              else "no re-send was needed")
    val.word("MCW_MISSING_SENTENCE", f"{miss}, and {resent}", ["verdicts"] + MC + ["MC_Weekly"])
    ch = V["manipulation_checks"]["MC_Chain"]
    refs_h = [("verdicts", MC + ["MC_Chain", st, s, "links_held"]) for st in VV.STEPS if st in ch for s in VV.SUBS
              if s in ch[st]]
    refs_t = [("verdicts", MC + ["MC_Chain", st, s, "links"]) for st in VV.STEPS if st in ch for s in VV.SUBS
              if s in ch[st]]
    val.derive("CHAIN_HELD", VV.d_sum, refs_h, VV.i0)
    val.derive("CHAIN_TOTAL", VV.d_sum, refs_t, VV.i0)
    cl = Cells(val)
    rows = []
    for st in VV.STEPS:
        cells = [f"Pull {st[-1]}"]
        for s in VV.SUBS:
            h = cl.f("verdicts", MC + ["MC_Chain", st, s, "links_held"], VV.i0)
            t = cl.f("verdicts", MC + ["MC_Chain", st, s, "links"], VV.i0)
            cells.append(f"{h} of {t}")
        rows.append(cells)
    val.table("TABLE_CHAIN", md_table(["Pull"] + [VV.CAT_SHORT[s] for s in VV.SUBS], rows), cl.cells)
    cl = Cells(val)
    rows = []
    for st in VV.STEPS:
        pk = ["steps", st]
        rows.append([f"Pull {st[-1]}", cl.f("pulls", pk + ["first_utc"], VV.utc_min),
                     cl.f("pulls", pk + ["last_utc"], VV.utc_min), cl.f("pulls", pk + ["records"], VV.i0),
                     cl.f("pulls", pk + ["ok"], VV.i0), cl.f("pulls", pk + ["missing"], VV.i0),
                     cl.f("pulls", pk + ["resent"], VV.i0)])
    val.table("TABLE_PULLS", md_table(["Pull", "First request", "Last request", "Requests", "Valid", "Missing",
                                       "Re-sends"], rows), cl.cells)
    # terms
    share = val.put("TERMS_SHARE", "verdicts", MC + ["MC_Terms", "share_topic"], VV.pct1)
    n_topic = sum(1 for r in V["unit_table"] if r.get("kind") == "topic")
    n_units = len(V["unit_table"])
    if V["manipulation_checks"]["MC_Terms"]["pass_"]:
        val.word("TERMS_RESULT", f"{n_topic} of {n_units} brands ({share}) were searched by topic and the rest by "
                                 f"plain search term, so `MC_Terms` raised no flag.",
                 ["verdicts", "unit_table", "kind == topic (count)", "MC_Terms"])
    else:
        val.word("TERMS_RESULT", f"Only {n_topic} of {n_units} brands ({share}) were searched by topic, below half, "
                                 f"so `MC_Terms` raised the flag “mostly plain search terms”.",
                 ["verdicts", "unit_table", "kind == topic (count)", "MC_Terms"])
    # concurrent and reliability
    c = V["manipulation_checks"]["MC_Concurrent"]
    flags["CONC_PASS"] = bool(c["pass_"])
    val.put("CONC_RHO", "verdicts", MC + ["MC_Concurrent", "rho"], VV.r3)
    val.put("CONC_P", "verdicts", MC + ["MC_Concurrent", "p_one"], VV.p4)
    val.put("CONC_N", "verdicts", MC + ["MC_Concurrent", "n"], VV.i0)
    rel = V["manipulation_checks"]["MC_PullReliability"]
    flags["REL_PASS"] = bool(rel["pass_"])
    pairs = [val.put(f"REL_PAIR{i + 1}", "verdicts", MC + ["MC_PullReliability", "pairs", i], VV.r3)
             for i in range(len(rel.get("pairs") or []))]
    val.word("REL_PAIRS", VV.joinand(pairs) if pairs else "not computable",
             ["verdicts"] + MC + ["MC_PullReliability", "pairs"])
    if VV.finite(rel.get("mean_pairwise_pooled_spearman")):
        val.put("REL_MEAN", "verdicts", MC + ["MC_PullReliability", "mean_pairwise_pooled_spearman"], VV.r3)
    else:
        val.word("REL_MEAN", "not computable (counted as failed, clarification C6)",
                 ["verdicts"] + MC + ["MC_PullReliability"])

    # ---------------- outcome definedness
    D = V["outcome_defined_per_substrate"]
    val.derive("UNITS_TOTAL", VV.d_sum, [("verdicts", ["outcome_defined_per_substrate", s, "units"]) for s in VV.SUBS],
               VV.i0)
    val.derive("Y_DEF_TOTAL", VV.d_sum, [("verdicts", ["outcome_defined_per_substrate", s, "Y_defined"])
                                         for s in VV.SUBS], VV.i0)
    cl = Cells(val)
    rows = []
    for s in VV.SUBS:
        r = [VV.CAT_SHORT[s], cl.f("verdicts", ["outcome_defined_per_substrate", s, "units"], VV.i0),
             cl.f("verdicts", ["outcome_defined_per_substrate", s, "Y_defined"], VV.i0)]
        for name in VV.TESTS:
            r.append(cl.f("verdicts", ["tests", name, "n_per_substrate", s], VV.i0))
        rows.append(r)
    tot = ["All", val.vals["UNITS_TOTAL"], val.vals["Y_DEF_TOTAL"]] + [cl.f("verdicts", ["tests", n, "n"], VV.i0)
                                                                      for n in VV.TESTS]
    rows.append(tot)
    val.table("TABLE_DEFINED", md_table(["Category", "Units", "$Y$ defined", "Primary", "SA", "Momentum",
                                         "Consistency"], rows), cl.cells)

    # ---------------- tests
    for name in VV.TESTS:
        k = VV.SHORT[name]
        T = V["tests"][name]
        tp = ["tests", name]
        cases[f"CASE_{k}"] = VV.case_test(T)
        flags[f"{k}_REVERSED"] = VV.reversed_label(T)
        flags[f"{k}_HAS_CI"] = VV.has(T, ["ci90", 1]) and VV.finite(T.get("rho"))
        val.word(f"{k}_WORD", _word(T), ["verdicts"] + tp + ["verdict", "labels"])
        val.put(f"{k}_N", "verdicts", tp + ["n"], VV.i0)
        val.put(f"{k}_MINN", "verdicts", tp + ["min_n"], VV.i0)
        for nm_, key, fmt in (("RHO", ["rho"], VV.r3), ("P1", ["p_one"], VV.p4), ("P2", ["p_two"], VV.p4),
                              ("CI90_LO", ["ci90", 0], VV.r3), ("CI90_HI", ["ci90", 1], VV.r3),
                              ("CI95_LO", ["ci95", 0], VV.r3), ("CI95_HI", ["ci95", 1], VV.r3)):
            if VV.has(T, key):
                val.put(f"{k}_{nm_}", "verdicts", tp + key, fmt)
            else:
                val.word(f"{k}_{nm_}", "--", ["verdicts"] + tp + key + ["(not computed)"])
        need = {"CONFIRMED": ["rho", "p_one", "ci90", "ci95"], "MARGINAL": ["rho", "p_one", "ci90", "ci95"],
                "FALSIFIED": ["rho", "p_one", "ci90", "ci95"], "UNDETERMINED": ["rho", "p_one", "ci90", "ci95"]}
        for key in need.get(cases[f"CASE_{k}"], []):
            if not VV.has(T, [key]):
                raise FillError(f"{name}: {cases[f'CASE_{k}']} but {key} is missing")
        if flags[f"{k}_REVERSED"] and not VV.has(T, ["p_two"]):
            raise FillError(f"{name}: REVERSED but p_two is missing")
    cl = Cells(val)
    rows = []
    for name in VV.TESTS:
        T, tp = V["tests"][name], ["tests", name]
        ci = lambda a: (f"[{cl.f('verdicts', tp + [a, 0], VV.r3)}, {cl.f('verdicts', tp + [a, 1], VV.r3)}]"  # noqa
                        if VV.has(T, [a, 1]) else "--")
        rows.append([name, SPEC_TEXT[name][0], OUTCOME_TEXT[name], SPEC_TEXT[name][1], cl.f("verdicts", tp + ["n"], VV.i0),
                     cl.f("verdicts", tp + ["rho"], VV.r3), ci("ci90"), ci("ci95"),
                     cl.f("verdicts", tp + ["p_one"], VV.p4), cl.f("verdicts", tp + ["p_two"], VV.p4),
                     f"**{T['verdict']}**" + (" REVERSED" if VV.reversed_label(T) else "")])
    val.table("TABLE_TESTS", md_table(["Test", "$X$", "Outcome", "$Z$", "$n$", "$\\rho_{\\text{pw}\\mid Z}$",
                                       "90% interval", "95% interval", "$p$ (one-sided)", "$p$ (two-sided)",
                                       "Verdict"], rows,
                                      ["l", "l", "l", "l", "r", "r", "r", "r", "r", "r", "l"]), cl.cells)
    # bootstrap resamples dropped (C6)
    drops = []
    for name in VV.TESTS:
        T = V["tests"][name]
        if VV.has(T, ["boot_valid"]) and int(T["boot_valid"]) < int(V["B_boot"]):
            d = val.derive(f"BOOT_DROP_{VV.SHORT[name]}", VV.d_diff, [("verdicts", ["B_boot"]),
                                                                      ("verdicts", ["tests", name, "boot_valid"])],
                           VV.i0)
            drops.append(f"{d} for {name}")
    val.put("B_BOOT", "verdicts", ["B_boot"], VV.i0)
    val.put("B_PERM", "verdicts", ["B_perm"], VV.i0)
    if drops:
        val.word("BOOT_SENTENCE", f"Of the {val.vals['B_BOOT']} bootstrap resamples, some had an undefined $\\rho$ and "
                                  f"were dropped and counted (clarification C6): {VV.joinand(drops)}.",
                 ["verdicts", "tests", "boot_valid"])
    else:
        val.word("BOOT_SENTENCE", f"Every test used {val.vals['B_PERM']} permutations and {val.vals['B_BOOT']} "
                                  f"bootstrap resamples, none of them dropped.", ["verdicts", "B_perm", "B_boot"])

    # ---------------- descriptives
    DS = ["descriptives"]
    cl = Cells(val)
    rows = []
    for name in VV.TESTS:
        cells = [name]
        for s in VV.SUBS:
            pk = DS + ["per_substrate", name, s]
            r_ = cl.f("verdicts", pk + ["rho"], VV.r3)
            if r_ == "--":
                cells.append(f"-- ({cl.f('verdicts', pk + ['n'], VV.i0)})")
            else:
                cells.append(f"{r_} ({cl.f('verdicts', pk + ['n'], VV.i0)}) [{cl.f('verdicts', pk + ['p_one'], VV.p4)}]")
        rows.append(cells)
    val.table("TABLE_PERSUB", md_table(["Test"] + [VV.CAT_SHORT[s] for s in VV.SUBS], rows), cl.cells)
    cl = Cells(val)
    rows = []
    for label, path, item in VV.DESC_ROWS:
        pk = DS + path
        ci = (f"[{cl.f('verdicts', pk + ['ci90', 0], VV.r3)}, {cl.f('verdicts', pk + ['ci90', 1], VV.r3)}]"
              if VV.has(V, pk + ["ci90", 1]) else "--")
        rows.append([f"{item}. {label}", cl.f("verdicts", pk + ["n"], VV.i0), cl.f("verdicts", pk + ["rho"], VV.r3),
                     ci, cl.f("verdicts", pk + ["p_one"], VV.p4)])
    val.table("TABLE_DESC", md_table(["Descriptive (§2.8)", "$n$", "$\\rho_{\\text{pw}\\mid Z}$", "90% interval",
                                      "$p$ (one-sided)"], rows), cl.cells)
    xl = V["descriptives"].get("cross_lagged")
    flags["XL_HAS"] = bool(xl) and all(VV.finite(xl.get(k)) for k in ("rho_AI_to_search", "rho_search_to_AI"))
    if flags["XL_HAS"]:
        xp = DS + ["cross_lagged"]
        val.put("XL_N", "verdicts", xp + ["n"], VV.i0)
        val.put("XL_A", "verdicts", xp + ["rho_AI_to_search"], VV.r3)
        val.put("XL_B", "verdicts", xp + ["rho_search_to_AI"], VV.r3)
        val.put("XL_DIFF", "verdicts", xp + ["difference"], VV.r3)
        for nm_, key in (("CI90_LO", ["difference_ci90", 0]), ("CI90_HI", ["difference_ci90", 1]),
                         ("CI95_LO", ["difference_ci95", 0]), ("CI95_HI", ["difference_ci95", 1])):
            val.put(f"XL_{nm_}", "verdicts", xp + key, VV.r3)
    return val, cases, flags


# =========================================================================== checks and main
def deviations_text():
    if not DEVIATIONS.exists():
        raise FillError(f"{DEVIATIONS} not found (written at the lock's anchor step)")
    nums, txt = VV.deviation_entries(DEVIATIONS)
    if VV.LOCK_RECORD_PHRASE not in txt:
        raise FillError(f"{DEVIATIONS} does not record the lock time {VV.LOCK_RECORD_PHRASE}")
    titles = re.findall(r"(?m)^## Entry (\d+) — (.+)$", txt)
    rel = "osf/v43/anchor/DEVIATIONS.md"
    if not titles:
        return (f"No deviation was recorded after the lock (`{rel}`).", "no deviations recorded after the lock.", [rel])
    items = "; ".join(f"Entry {n}, {t.strip().rstrip('.')}" for n, t in titles)
    ent = f"{len(titles)} entr{'y' if len(titles) == 1 else 'ies'}"
    return (f"After the lock, `{rel}` recorded {ent}, each before the data it could affect: {items}. The record "
            f"states for each whether it changes code, data, rules or inference.",
            f"{ent} in the post-lock deviations record.", [rel])


def verify_lock():
    """The lock records in this repository (both modes). Returns the tag's commit."""
    commit = VV.git_tag_commit()
    if not commit:
        raise FillError(f"tag {VV.EXPECTED_PREREG_TAG} not found in {ROOT}")
    if commit != VV.EXPECTED_COMMIT:
        raise FillError(f"tag {VV.EXPECTED_PREREG_TAG} resolves to {commit}, not {VV.EXPECTED_COMMIT}")
    when = VV.git_tag_date_utc()
    if when != VV.LOCK_UTC:
        raise FillError(f"tag {VV.EXPECTED_PREREG_TAG} is dated {when} UTC, not {VV.LOCK_UTC} (Method 2.8 states it)")
    if not ANCHOR.exists() or commit not in ANCHOR.read_text(encoding="utf-8"):
        raise FillError(f"anchor {ANCHOR} missing or does not name {commit}")
    bad = VV.manifest_mismatches()
    if bad:
        raise FillError(f"locked files differ from LOCK_MANIFEST_v0_43.sha256: {bad}")
    return commit


def check_pulls(V, pulls, real):
    st = pulls.get("steps") or {}
    miss = [s for s in VV.STEPS if s not in st]
    if miss:
        raise FillError(f"no stored records for pull(s) {miss} in {pulls.get('raw_dir')}")
    w = V["manipulation_checks"]["MC_Weekly"]
    tot = {k: sum(int(st[s][k]) for s in VV.STEPS) for k in ("records", "ok", "missing", "resent")}
    if (tot["records"], tot["ok"], tot["missing"], tot["resent"]) != (w["requests"], w["ok"], w["missing"], w["resent"]):
        raise FillError(f"stored records {tot} disagree with MC_Weekly {w}")
    if real:
        for s in VV.STEPS:
            if st[s]["records"] != VV.REQUESTS_PER_PULL:
                raise FillError(f"pull {s} has {st[s]['records']} stored requests, not {VV.REQUESTS_PER_PULL}")
        for a, b in zip(VV.STEPS, VV.STEPS[1:]):
            if VV.d_hours(st[a]["last_utc"], st[b]["first_utc"]) < 24:
                raise FillError(f"pull {b} started less than 24 hours after pull {a} was stored")


def fill(verdicts, pulls, out=None, fig_dir=None, synthetic=False, coi_cheil=False, template=TEMPLATE, check=True):
    """pulls: a pull-summary dict, a path to a pull-summary JSON, or a raw directory (read with pull_summary)."""
    if isinstance(pulls, (str, Path)) and Path(pulls).is_dir():
        pulls = VV.pull_summary(pulls)
    src = VV.load_sources(verdicts, pulls)
    V = src["verdicts"]
    if synthetic and not VV.is_synthetic(V):
        raise FillError("--synthetic given but the verdicts are not from a synthetic run")
    if not synthetic and VV.is_synthetic(V):
        raise FillError("the verdicts carry synthetic_fixture: use --synthetic (and never publish the result)")
    commit = verify_lock()
    if check:
        try:
            VV.check_consistency(V, real=not synthetic)
        except VV.Inconsistent as e:
            raise FillError(f"inconsistent verdicts: {e}")
        check_pulls(V, src["pulls"], real=not synthetic)
    fig_dir = fig_dir or "../../reports/figs/v043"
    val, cases, flags = compute(src, synthetic, fig_dir, commit, deviations_text(), coi_cheil)
    tpl = Path(template).read_text(encoding="utf-8")
    text = render(tpl, val.vals, cases, flags)
    if out:
        out = Path(out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
        prov = {"verdicts": str(verdicts), "pulls": src["pulls"].get("raw_dir"), "synthetic": synthetic,
                "coi_cheil": bool(coi_cheil), "cases": cases, "flags": flags, "values": val.prov}
        Path(str(out).replace(".md", "_provenance.json")).write_text(
            json.dumps(prov, indent=1, ensure_ascii=False, default=str), encoding="utf-8")
    return text, val, cases, flags


def main(argv=None):
    ap = argparse.ArgumentParser(description="Fill the v0.43 Stage 1 paper template from the scorer's output")
    ap.add_argument("--verdicts", type=Path, default=VERDICTS)
    ap.add_argument("--pulls", type=Path, default=None, help="pull-summary JSON (synthetic fixtures)")
    ap.add_argument("--raw-dir", type=Path, default=None, help="stored request records (default osf/v43/data/trends_raw)")
    ap.add_argument("--fig-dir", default=None, help="figure directory as the paper references it "
                                                     "(default ../../reports/figs/v043, relative to papers/v0_43)")
    ap.add_argument("--out", type=Path, default=HERE / "v0_43_paper_draft.md")
    ap.add_argument("--synthetic", action="store_true")
    ap.add_argument("--coi-cheil", action="store_true",
                    help="add the optional COI sentence on Cheil Worldwide / Iris (OFF by default; pending decision)")
    a = ap.parse_args(argv)
    if a.synthetic and str(a.out.resolve()).startswith(str(ROOT.resolve()) + "/"):
        sys.exit("[fill v0.43] REFUSED: synthetic output must be written outside the repository")
    if not a.synthetic and (a.pulls or a.raw_dir):
        sys.exit("[fill v0.43] REFUSED: the real fill reads the stored records in osf/v43/data/trends_raw only")
    pulls = a.pulls or a.raw_dir or RAW_DIR
    try:
        text, val, cases, flags = fill(a.verdicts, pulls, a.out, a.fig_dir, a.synthetic, a.coi_cheil)
    except (FillError, VV.Missing, VV.Inconsistent, FileNotFoundError) as e:
        print(f"[fill v0.43] REFUSED: {e}", file=sys.stderr)
        return 3
    print(f"[fill v0.43] wrote {a.out} ({len(text.split())} words); cases {cases}; "
          f"flags {[k for k, v in flags.items() if v]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
