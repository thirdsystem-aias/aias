#!/usr/bin/env python3
"""
Tests for the v0.42 paper fill (papers/v0_42/fill_paper_v0_42.py), the report content module and the chart/report
builders' refusal rules. SYNTHETIC fixtures only (papers/v0_42/tests/fixtures/SYNTHETIC_*: the scorer's own output on
the synthetic "noisy" scenario of make_scenarios_v0_42.py; MC_Parity = SKIPPED_SYNTHETIC). No model is called and
nothing is written inside the repository (temporary files go to a TemporaryDirectory).

What is tested
  1. Every switch in the template covers every pre-registered outcome exactly once (CASE_GEN, CASE_PHI, CASE_SEARCH,
     GEN_DELTA_DIR, CASE_PARITY).
  2. For every outcome (verdict variants built from the fixture by changing the scorer's fields), the fill succeeds,
     leaves no template syntax ({{, {%), and every number in the paper is traced: it is either a static number of the
     template (each listed below with its source in the pre-registration or the programme's records) or a value
     whose provenance (JSON path or table cell, formatting function) re-resolves to exactly the printed string.
  3. Every static number of the template has a declared source (no hand-typed result can enter the template).
  4. Refusals: real mode on synthetic verdicts, synthetic mode on real-looking verdicts, a wrong pre-registration
     tag, a real fill without the tag in the repository, an unknown placeholder, a switch with no matching case.
  5. The report content module builds every variant without placeholders, None or nan, with P1-P5.
Run: python3 papers/v0_42/tests/test_fill_paper_v0_42.py   (or the unittest runner)
"""
import copy
import importlib
import json
import math
import os
import re
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAPER = HERE.parent
ROOT = PAPER.parents[1]
sys.path.insert(0, str(PAPER))
sys.path.insert(0, str(ROOT / "reports"))
import v42_values as VV  # noqa: E402
import fill_paper_v0_42 as FP  # noqa: E402

FIX_V = HERE / "fixtures" / "SYNTHETIC_noisy_v42_verdicts.json"
FIX_T = HERE / "fixtures" / "SYNTHETIC_noisy_v42_brand_table.csv"
TEMPLATE = PAPER / "v0_42_ssrn_paper_template.md"

# ---------------------------------------------------------------------------------------------- static numbers
# Every number that the template states as fixed text, with its source. Results are never in this list.
_SRC = {
    "structure (section, table, figure numbering; enumerations such as '2 of 3', 'runs 1 to 3')":
        "1 2 3 4 5 6 7 8 9 10 11 2.1 2.2 2.3 2.4 2.5 2.6 2.7 2.8 2.9 2.10 3.1 3.2 3.3 3.4 3.5 01 02 03 04",
    "LaTeX layout (template preamble, title page, needspace; v0.41 preamble plus float placement)":
        "0.07 0.8 0.9 1.0 1.36 10000 12 14 18 20 28",
    "pre-registration header and §4.2 (design: 112 brands, 30 + 112 probes, 3 runs, 876 calls, 202/90 per model)":
        "112 30 876 202 90 142",
    "pre-registration §2.1 (seeds; 10,000 draws; p = (1 + #)/10,001; 95% intervals; alpha .05)":
        "420041 420042 420043 420044 420045 10,000 001 95 05",
    "pre-registration §2.2 (bar 0.70, falsification 0.50, legacy 0.93-0.98 over five months)": "0.70 0.50 0.93 0.98",
    "pre-registration §2.4 (bars 0.50 / 0.30, n floor 40)": "0.30 40",
    "pre-registration §2.5 (labels at 0.80 / 0.50)": "0.80",
    "pre-registration §2.6 (98% complete, 25% search flag, 5% truncation flag, 72-hour window)": "98 25 72",
    "pre-registration §4.1 (720 of 720 t3 records; 8 of 8 checksums; 132 query IDs)": "720 132",
    "pre-registration §4.4 (16,384-token cap; legacy caps 64 to 2,048; temperature 0.0; web_search_20250305; "
    "at most 5 uses; up to 3 attempts)": "16,384 2,048 0.0 64 20250305",
    "pre-registration §4.5 (US$100 cap, US$80 pause, estimate US$64 central / US$136 high)": "100 80 136",
    "pre-registration §1 and v0.41 (152 days from t2 to t3)": "152",
    "pre-registration C25 (null mean +0.0464; substrates of 16 and 24 brands); C1-C26 numbering": "0.0464 16 24 26",
    "pre-registration §5.1 (coder git blob 2d36735d...)": "36735",
    "dates (pre-registration header, §1, §4.3, §6, C26; v0.41 t3 date; references)":
        "2010 2022 2024 2025 2026 2027 13 23 59",
    "ORCID (CLAUDE.md standard author block)": "0009 0003 8968 9990",
    "LOCK_STEPS clarification of 2026-11-11 (tag set at 02:53 UTC); C27-C28 numbering; Harman a Samsung "
    "subsidiary since March 2017 (coordinator's COI wording, Nov 11, 2026)": "02 53 27 2017",
    "SSRN IDs (CLAUDE.md methodology chain and phase registry)":
        "6659000 6761698 6797679 6799479 6809182 6810758 6811441 6815378 6816340 6817841 6829118 6834298 "
        "6878818 6915458 6963359 7685100",
    "programme versions (phases v0.17-v0.42, methodology v1.2-v1.8, AIAS 1.0)":
        "0.17 0.19 0.20 0.21 0.22 0.23 0.34 0.38 0.39 0.40 0.41 0.42 1.2 1.3 1.4 1.5 1.6 1.7 1.8 41 42",
    "model names (pre-registration §2.1, §4.3: Claude Opus 4.5, Claude Fable 5.2, Claude Opus 5.5, GPT-6.1 Terra, "
    "Gemini 2.5 Flash)": "4.5 5.2 5.5 6.1",
    "JEL codes (CLAUDE.md SSRN packet: M31; L86, L15, D83, M37)": "31 86 15 83 37",
    "code identifiers and pre-registration section references (acquire_v0_19, score_v0_23, code_t4_v0_42; "
    "partition pi = 0; pre-registration §4.3)": "0 19 4.3",
}
STATIC_SOURCES = {tok: src for src, toks in _SRC.items() for tok in toks.split()}


def template_static_tokens(tpl):
    t = re.sub(r"\{\{[^}]*\}\}", " ", tpl)
    t = re.sub(r"\{%[^%]*%\}", " ", t)
    return set(VV.numeric_tokens(t))


# ---------------------------------------------------------------------------------------------- variants
def base():
    return json.load(open(FIX_V, encoding="utf-8"))


def v_gen(V, case):
    h = V["verdicts"]["H_Gen_Presence"]
    if case == "MARGINAL":
        h.update(verdict="MARGINAL", rho=0.6123456)
    elif case == "FALSIFIED":
        h.update(verdict="FALSIFIED", rho=0.4123456)
    elif case == "UNDETERMINED_DEGENERATE":
        for k in ("rho", "p_perm", "ci95_rho", "delta", "ci95_delta"):
            h[k] = None
        h["verdict"] = "UNDETERMINED"
    elif case == "UNDETERMINED_EXCLUDED":
        excl_s0(V)
    return V


def excl_s0(V):
    """Gemini 4 Argon below 90% in S0: both generation tests UNDETERMINED (section 5.4); search on a reduced panel."""
    k = "gemini-4-argon|S0"
    pm = V["manipulation_checks"]["MC_Complete"]["per_model_condition"][k]
    pm.update(answered=150, share_of_expected=150 / 202, excluded_below_90pct=True)
    V["manipulation_checks"]["MC_Complete"]["below_90pct"] = [k]
    V["manipulation_checks"]["MC_Complete"]["answered"] = 824
    V["manipulation_checks"]["MC_Complete"]["share"] = 824 / 876
    V["manipulation_checks"]["MC_Complete"]["pass"] = False
    V["models_excluded_condition"] = [k]
    reason = "gemini-4-argon excluded (answered < 90%): hypothesis UNDETERMINED (r2: no fallback panel)"
    for hk in ("H_Gen_Presence", "H_Gen_Phi"):
        h = V["verdicts"][hk]
        V["verdicts"][hk] = {"tier": h["tier"], "seed": h["seed"], "verdict": "UNDETERMINED", "reason": reason,
                             "reported_alongside": h.get("reported_alongside", {})}
    pp = V["verdicts"]["H_Gen_Presence"]["reported_alongside"].get("per_provider_generation_pairs", {})
    pp["Google: legacy pair -> gemini-4-argon"] = {"status": "NOT_COMPUTED", "reason": "model excluded"}
    V["verdicts"]["H_Gen_Phi"]["reported_alongside"].get("mean_independence_S0", {}).pop("N3", None)
    s = V["verdicts"]["H_Search_Presence"]
    s["models"] = ["claude-fable-5-2", "gpt-6-astra"]
    s["reduced_panel"] = True
    s["per_model"].pop("gemini-4-argon", None)
    V["descriptives"]["3_floor_persistence"] = {"status": "NOT_COMPUTED"}


def v_phi(V, case):
    h = V["verdicts"]["H_Gen_Phi"]
    if case == "CONFIRMED":
        h.update(verdict="CONFIRMED", rho=0.7123456)
    elif case == "FALSIFIED":
        h.update(verdict="FALSIFIED", rho=0.2123456)
    elif case == "UNDETERMINED_FLOOR":
        h.update(verdict="UNDETERMINED", n=35)
    elif case == "UNDETERMINED_DEGENERATE":
        h.update(verdict="UNDETERMINED", rho=None, p_perm=None, ci95_rho=None)
    return V


def v_search(V, case):
    h = V["verdicts"]["H_Search_Presence"]
    if case == "ROBUST":
        h.update(label="search-robust", ci95_rho=[0.8123456, 0.9523456], rho=0.9012345)
    elif case == "DOMINATED":
        h.update(label="search-dominated", ci95_rho=[0.1123456, 0.4423456], rho=0.3012345)
    elif case == "UNDETERMINED":
        h.update(label="UNDETERMINED", ci95_rho=None)
    elif case == "NOT_COMPUTED":
        V["verdicts"]["H_Search_Presence"] = {"tier": "SECONDARY", "seed": 420044, "status": "NOT_COMPUTED",
                                              "reason": "no model retained in both conditions",
                                              "reported_alongside": {"per_substrate_rho": None}}
    return V


def v_flags(V):
    """Every optional sentence on: search rarely used, truncation, served-ID failure, outside-design lines,
    calls without served ID, failed window, delta above zero, S1 variant on a reduced panel."""
    V["manipulation_checks"]["MC_Search"]["gpt-6-astra"].update(flag_search_rarely_used=True, share=0.2111)
    V["manipulation_checks"]["MC_Truncation"]["claude-fable-5-2|S1"].update(flag_above_5pct=True, share=0.0667, at_cap=6)
    V["manipulation_checks"]["MC_Served"].update(n_mismatched=3, pass_=False, ok_calls_without_served_id=2)
    V["manipulation_checks"]["MC_Served"]["pass"] = False
    V["manipulation_checks"]["MC_Complete"]["outside_design"]["n"] = 4
    V["manipulation_checks"]["MC_Window"].update(span_hours=80.25, **{"pass": False})
    V["verdicts"]["H_Gen_Presence"]["ci95_delta"] = [0.0123, 0.0456]
    V["verdicts"]["H_Gen_Presence"]["reported_alongside"]["variants"]["N3_S1"].update(
        reduced_panel=True, models=["claude-fable-5-2", "gpt-6-astra"])
    return V


def variants():
    out = [("base", base())]
    for c in ("MARGINAL", "FALSIFIED", "UNDETERMINED_DEGENERATE", "UNDETERMINED_EXCLUDED"):
        out.append((f"gen_{c}", v_gen(base(), c)))
    for c in ("CONFIRMED", "FALSIFIED", "UNDETERMINED_FLOOR", "UNDETERMINED_DEGENERATE"):
        out.append((f"phi_{c}", v_phi(base(), c)))
    for c in ("ROBUST", "DOMINATED", "UNDETERMINED", "NOT_COMPUTED"):
        out.append((f"search_{c}", v_search(base(), c)))
    v = base()
    v["verdicts"]["H_Gen_Presence"]["ci95_delta"] = [-0.0456, -0.0123]
    out.append(("delta_below", v))
    out.append(("flags", v_flags(base())))
    return out


# ---------------------------------------------------------------------------------------------- helpers
def resolve(src, path):
    return VV.jget(src, path)


def check_provenance(test, src, prov, fig_dir):
    """Every value re-resolves to its printed string; returns the numeric tokens the values account for."""
    toks = set(VV.numeric_tokens(str(fig_dir)))
    for name, p in prov.items():
        if p["kind"] == "json":
            raw = resolve(src[p["source"]], p["path"])
            test.assertEqual(VV.FORMATS[p["fmt"]](raw), p["formatted"], name)
            toks |= set(VV.numeric_tokens(p["formatted"]))
        elif p["kind"] == "derived":
            raws = [resolve(src[s], pp) for s, pp in p["refs"]]
            test.assertEqual(VV.FORMATS[p["fmt"]](VV.DERIVE[p["fn"]](*p["consts"], *raws)), p["formatted"], name)
            toks |= set(VV.numeric_tokens(p["formatted"]))
        elif p["kind"] == "table":
            for c in p["cells"]:
                raw = resolve(src[c["source"]], c["path"])
                test.assertEqual(VV.FORMATS[c["fmt"]](raw), c["formatted"], f"{name} {c['path']}")
                toks |= set(VV.numeric_tokens(c["formatted"]))
        else:
            test.assertTrue(p["basis"], f"{name}: text value without a basis")
            b = p["basis"]
            for cand in (b[1:], b):
                try:
                    v = resolve(src["verdicts"], cand)
                except (VV.Missing, TypeError):
                    continue
                if isinstance(v, str):
                    toks |= set(VV.numeric_tokens(v))
                break
    return toks


def run_fill(test, V, tmp, name, synthetic=True, budget_state=None):
    vp = Path(tmp) / f"{name}_verdicts.json"
    vp.write_text(json.dumps(V), encoding="utf-8")
    out = Path(tmp) / f"{name}_paper.md"
    text, val, cases, flags = FP.fill(vp, FIX_T, out, "/tmp/t4_figs", synthetic, budget_state)
    src = VV.load_sources(vp, FIX_T, None, budget_state)
    return text, val, cases, flags, src


# ---------------------------------------------------------------------------------------------- tests
class TestTemplate(unittest.TestCase):
    OUTCOMES = {"CASE_GEN": {"CONFIRMED", "MARGINAL", "FALSIFIED", "UNDETERMINED_EXCLUDED", "UNDETERMINED_DEGENERATE"},
                "CASE_PHI": {"CONFIRMED", "MARGINAL", "FALSIFIED", "UNDETERMINED_FLOOR", "UNDETERMINED_EXCLUDED",
                             "UNDETERMINED_DEGENERATE"},
                "CASE_SEARCH": {"ROBUST", "SENSITIVE", "DOMINATED", "UNDETERMINED", "NOT_COMPUTED"},
                "GEN_DELTA_DIR": {"ABOVE", "BELOW", "SPANS"}, "CASE_PARITY": {"PASSED", "SYNTHETIC"}}

    def test_every_switch_covers_every_outcome_once(self):
        sw = FP.switch_alternatives(TEMPLATE.read_text(encoding="utf-8"))
        self.assertEqual(set(sw), set(self.OUTCOMES))
        for var, switches in sw.items():
            for alts in switches:
                flat = [a for case in alts for a in case]
                self.assertEqual(sorted(flat), sorted(self.OUTCOMES[var]), f"{var}: {alts}")

    def test_static_numbers_have_sources(self):
        toks = template_static_tokens(TEMPLATE.read_text(encoding="utf-8"))
        missing = sorted(toks - set(STATIC_SOURCES))
        self.assertEqual(missing, [], f"template numbers without a declared source: {missing}")

    def test_prereg_tag_token_present(self):
        tpl = TEMPLATE.read_text(encoding="utf-8")
        self.assertIn("{{PREREG_TAG}}", tpl.replace(" ", ""))
        self.assertNotIn(VV.EXPECTED_PREREG_TAG, tpl, "the tag is filled from the verdicts and checked, not typed")


class TestFillVariants(unittest.TestCase):
    def test_all_variants_fill_and_every_number_is_traced(self):
        static = template_static_tokens(TEMPLATE.read_text(encoding="utf-8"))
        seen = {k: set() for k in ("CASE_GEN", "CASE_PHI", "CASE_SEARCH", "GEN_DELTA_DIR")}
        with tempfile.TemporaryDirectory() as tmp:
            for name, V in variants():
                with self.subTest(variant=name):
                    text, val, cases, flags, src = run_fill(self, V, tmp, name)
                    for k in seen:
                        seen[k].add(cases[k])
                    for bad in (r"\{\{", r"\{%", r"\bNone\b", r"\bnan\b", r"\bNaN\b"):
                        m = re.search(bad, text)
                        self.assertIsNone(m, f"{name}: {bad!r} in output near {text[max(0, m.start() - 60):m.end() + 20]!r}"
                                          if m else "")
                    traced = check_provenance(self, src, val.prov, "/tmp/t4_figs")
                    untraced = sorted(set(VV.numeric_tokens(text)) - static - traced)
                    self.assertEqual(untraced, [], f"{name}: numbers with no source: {untraced}")
                    self.assertIn("**JEL codes:** M31; L86, L15, D83, M37", text)
                    self.assertEqual(text.count("Samsung"), text.split("# Declarations")[1].count("Samsung"),
                                     "Samsung appears outside the Declarations")
        self.assertEqual(seen["CASE_GEN"], TestTemplate.OUTCOMES["CASE_GEN"])
        self.assertEqual(seen["CASE_PHI"], TestTemplate.OUTCOMES["CASE_PHI"])
        self.assertEqual(seen["CASE_SEARCH"], TestTemplate.OUTCOMES["CASE_SEARCH"])
        self.assertEqual(seen["GEN_DELTA_DIR"], TestTemplate.OUTCOMES["GEN_DELTA_DIR"])

    def test_budget_approval_sentence_reads_state_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            bs = Path(tmp) / "t4_budget_state.json"
            bs.write_text(json.dumps({"approvals": {"past_80": {"note": "x", "utc": "2026-11-13T10:00:00+00:00",
                                                                 "spent_at_approval_usd": 80.1234}}}))
            text, val, *_ = run_fill(self, base(), tmp, "budget", budget_state=bs)
            self.assertIn("approved continuing past the US\\$80 pause (recorded at a spend of \\$80.12)", text)
            self.assertEqual(val.prov["APPR_PAST_80"]["path"], ["approvals", "past_80", "spent_at_approval_usd"])


class TestRefusals(unittest.TestCase):
    def test_real_mode_refuses_synthetic_verdicts(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(FP.FillError):
                run_fill(self, base(), tmp, "r1", synthetic=False)

    def test_synthetic_mode_refuses_real_verdicts(self):
        V = base()
        V["manipulation_checks"]["MC_Parity"] = {"passed": True, "detail": {"P1": True, "P2": True, "P3": True}}
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(FP.FillError):
                run_fill(self, V, tmp, "r2", synthetic=True)

    def test_real_mode_checks_tag_in_repository(self):
        V = base()
        V["manipulation_checks"]["MC_Parity"] = {"passed": True, "detail": {"P1": True, "P2": True, "P3": True}}
        if VV.git_tag_commit():
            self.skipTest("tag exists in this repository (after the lock): covered by the real run")
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(FP.FillError, "not found"):
                run_fill(self, V, tmp, "r3", synthetic=False)

    def test_real_mode_refuses_failed_parity(self):
        V = base()
        V["manipulation_checks"]["MC_Parity"] = {"passed": False, "detail": {"P1": True, "P2": False, "P3": True}}
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(FP.FillError, "parity"):
                run_fill(self, V, tmp, "r4", synthetic=False)

    def test_wrong_prereg_tag_refused(self):
        V = base()
        V["prereg_tag"] = "v0.42-prereg-r2"
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(FP.FillError, "prereg_tag"):
                run_fill(self, V, tmp, "r5")

    def test_unknown_placeholder_and_unmatched_switch(self):
        with self.assertRaisesRegex(FP.FillError, "NOPE"):
            FP.render("a {{NOPE}} b", {}, {}, {})
        with self.assertRaisesRegex(FP.FillError, "matched 0"):
            FP.render("{% switch X %}{% case A %}a{% endswitch %}", {}, {"X": "B"}, {})
        with self.assertRaisesRegex(FP.FillError, "unknown flag"):
            FP.render("{% if F %}a{% endif %}", {}, {}, {})


class TestReportContent(unittest.TestCase):
    def test_content_module_builds_every_variant(self):
        with tempfile.TemporaryDirectory() as tmp:
            for name, V in variants():
                with self.subTest(variant=name):
                    vp = Path(tmp) / f"{name}.json"
                    vp.write_text(json.dumps(V), encoding="utf-8")
                    os.environ["AIAS_V42_VERDICTS"] = str(vp)
                    import v42_t4_generation_content as CM
                    CM = importlib.reload(CM)
                    blob = json.dumps({k: getattr(CM, k) for k in ("COVER", "STANDFIRST", "LEAD_DECK", "EXEC_SUMMARY",
                                                                  "WHAT_WE_MEASURED", "LIMITATIONS", "WHATS_NEXT",
                                                                  "HYPOTHESIS_SCORING", "HYPOTHESIS_DETAILS",
                                                                  "FIGURE_CAPTIONS", "CLOSING")})
                    for bad in (r"\bNone\b", r"\bnan\b", r"\{\{", "H_Gen", "H_Search", "Samsung"):
                        self.assertIsNone(re.search(bad, blob), f"{name}: {bad!r}")
                    self.assertEqual([h["id"] for h in CM.HYPOTHESIS_SCORING], ["P1", "P2", "P3", "P4", "P5"])
                    self.assertEqual(set(CM.HYPOTHESIS_DETAILS), {"P1", "P2", "P3", "P4", "P5"})
        os.environ.pop("AIAS_V42_VERDICTS", None)


if __name__ == "__main__":
    r = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__]))
    sys.exit(0 if r.wasSuccessful() else 1)
