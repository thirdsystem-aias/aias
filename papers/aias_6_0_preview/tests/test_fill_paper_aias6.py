#!/usr/bin/env python3
"""
Tests of the AIAS 6.0 Preview paper pipeline. SYNTHETIC DATA ONLY: the fixtures (tests/fixtures/<scenario>/) are the
locked scorer's own outputs on its own synthetic test repository, or scenarios derived from them with its functions
(make_scenarios_aias6.py). Nothing under osf/ is written; outputs go to temporary directories.

  python3 papers/aias_6_0_preview/tests/test_fill_paper_aias6.py
"""
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAPER = HERE.parent
ROOT = PAPER.parents[1]
FIX = HERE / "fixtures"
sys.path.insert(0, str(PAPER))
sys.path.insert(0, str(HERE))
import fill_paper_aias6 as FP  # noqa: E402
import aias6_values as VV  # noqa: E402
import make_scenarios_aias6 as MS  # noqa: E402

S = FP.scorer()
TPL = (PAPER / "aias_6_0_preview_paper_template.md").read_text(encoding="utf-8")
FILL_SRC = (PAPER / "fill_paper_aias6.py").read_text(encoding="utf-8")
AI_USE = ("During the preparation of this work the author used AI tools (Anthropic's Claude) to assist with study "
          "design, analysis and writing. The author reviewed and edited all content and takes full responsibility "
          "for it.")
STATES_R = {"PASS", "PASS_RETEST_PENDING", "MARGINAL", "FAIL", "UNDETERMINED", "NOT_RUN"}
STATES_S = {"PASS", "PASS_AI_JUDGED", "MARGINAL", "FAIL", "UNDETERMINED", "NOT_RUN"}
STATES_C = {"PASS", "MARGINAL", "FAIL", "UNDETERMINED", "NOT_RUN"}
EXPECTED = {"CASE_PANEL": {"COMPLETE", "REDUCED"}, "CASE_R": STATES_R, "CASE_S": STATES_S, "CASE_COV": STATES_C,
            "CASE_G": STATES_C, "CLASS": {"A", "A_k", "B", "C", "U"},
            "CASE_HS": {"CONFIRMED", "PARTIAL", "FALSIFIED", "UNDETERMINED"}}
FILLED = {}


def setUpModule():
    for s in MS.SCENARIOS:
        FILLED[s] = FP.fill(FIX / s, fig_dir="figs", synthetic=True, class_c_draft=True)


def load(s):
    return VV.load_sources(FIX / s)


def section(text, start, end):
    a = text.index(start)
    return text[a:text.index(end, a)]


def strip_ph(t):
    return re.sub(r"\{\{[^}]*\}\}|\{%[^%]*%\}", " ", t)


class TestTemplate(unittest.TestCase):
    def test_every_switch_value_matches_exactly_one_case(self):
        alts = FP.switch_alternatives(TPL)
        self.assertEqual(set(alts), set(EXPECTED))
        for var, occ in alts.items():
            for cases in occ:
                flat = [a for c in cases for a in c]
                self.assertEqual(len(flat), len(set(flat)), var)
                self.assertEqual(set(flat), EXPECTED[var], var)

    def test_states_are_the_scorers(self):
        self.assertEqual({S.PASS, S.PASS_RETEST, S.PASS_AI, S.MARGINAL, S.FAIL, S.UNDET, S.NOT_RUN},
                         STATES_R | STATES_S)
        self.assertEqual(set(VV.STATE_WORD), STATES_R | STATES_S)

    def test_ai_use_coi_and_citations(self):
        self.assertEqual(TPL.count(AI_USE), 1)
        coi = section(TPL, "## Conflict of interest", "## Funding")
        for s in ("a Samsung subsidiary since March 2017", "Sound United brands, Denon included, on September 23, 2025",
                  "already a Samsung-group brand", "tier-2/3", "Samsung SDI", "Samsung Display", "had no role"):
            self.assertIn(s, coi)
        self.assertNotIn("7685126", TPL)
        refs = section(TPL, "# References", "\\clearpage\n\n# Appendix")
        self.assertIn("https://thirdsystem.ai/studies/v1-9/", refs)
        self.assertIn("https://osf.io/ec6wh/files/osfstorage/6af1fd459966c813ee53ba87", refs)
        for ssrn in ("6659000", "6761698", "6797679", "6799479", "6810758", "6816340", "6878818", "6963359", "6817841"):
            self.assertIn(f"SSRN {ssrn}", refs)
        body = TPL[:TPL.index("# References")]
        for letter in "abcdefghijkl":
            self.assertRegex(body, rf"2026[a-l, 0-9]*{letter}\b", f"2026{letter} not cited")

    def test_fixed_wordings_of_section_6_6(self):
        for s in ("On the newest models, the six provisional parts of AI Availability are six separate readings of a brand.",
                  "provisional parts measured so far are separate readings of a brand",
                  "parts measured are separate readings of a ", " overlaps ", "is only partly separable from",
                  "On the newest models, how the parts relate could not be determined: ",
                  "Presence and Consistency stay separable on the newest models.", "with moderate coupling",
                  "On the newest models Consistency moves with Presence", "AIAS 2.0's separability is shown on the retiring panel only"):
            self.assertTrue(s in FILL_SRC, s)
        self.assertIn("drafting pauses", TPL)


class TestFixtures(unittest.TestCase):
    def test_marked_synthetic_and_consistent_with_the_scorer(self):
        for s in MS.SCENARIOS:
            src = load(s)
            self.assertTrue(VV.is_synthetic(src))
            for k in ("results", "gates", "inputs"):
                self.assertIn("SYNTHETIC", src[k]["synthetic_fixture"])
            self.assertEqual(VV.components_verified(src), [])
            FP.check_consistency(src)

    def test_scenarios_cover_the_plan(self):
        seen = {k: set() for k in ("CLASS", "CASE_HS", "HPC", "R", "S", "Cov", "G")}
        for s in MS.SCENARIOS:
            V = load(s)["results"]
            st = V["structure"]
            seen["CLASS"].add(st["wording_class"])
            seen["CASE_HS"].add(st["H_Structure"]["verdict"])
            seen["HPC"].add(st.get("H_PC_N3"))
            for m in ("R", "S", "Cov", "G"):
                seen[m].add(V["gate_states"][m])
        self.assertEqual(seen["CLASS"], EXPECTED["CLASS"])
        self.assertEqual(seen["CASE_HS"], EXPECTED["CASE_HS"])
        self.assertTrue({"CONFIRMED", "MARGINAL", "FALSIFIED", "UNDETERMINED", None} <= seen["HPC"])
        self.assertTrue({"PASS", "PASS_RETEST_PENDING", "MARGINAL", "FAIL", "NOT_RUN"} <= seen["R"])
        statuses = {v for s in MS.SCENARIOS for v in (load(s)["results"]["structure"].get("status") or {}).values()}
        self.assertEqual(statuses, {"DISTINCT", "PARTLY DISTINCT", "NOT DISTINCT", "UNDETERMINED"})


class TestFill(unittest.TestCase):
    def test_every_scenario_fills(self):
        for s, (text, val, cases, flags) in FILLED.items():
            self.assertNotIn("{{", text, s)
            self.assertNotIn("{%", text, s)
            self.assertIn("SYNTHETIC TEST BUILD", text)

    def test_provenance_re_resolves(self):
        n = 0
        for s, (text, val, cases, flags) in FILLED.items():
            src = load(s)
            for name, p in val.prov.items():
                if p["kind"] == "json":
                    self.assertEqual(VV.FORMATS[p["fmt"]](VV.jget(src[p["source"]], p["path"])), p["formatted"], name)
                    n += 1
                elif p["kind"] == "derived":
                    raws = [VV.jget(src[a], b) for a, b in p["refs"]]
                    self.assertEqual(VV.FORMATS[p["fmt"]](VV.DERIVE[p["fn"]](*raws)), p["formatted"], name)
                    n += 1
                elif p["kind"] == "table":
                    for c in p["cells"]:
                        self.assertEqual(VV.FORMATS[c["fmt"]](VV.jget(src[c["source"]], c["path"])), c["formatted"])
                        n += 1
                elif p["kind"] == "text":
                    for ref in p.get("numbers", []):
                        if ref in val.vals:
                            self.assertIn(val.vals[ref], p["formatted"], f"{s}:{name} lacks {ref}")
        self.assertGreater(n, 800)

    def test_every_number_in_abstract_and_results_is_fixed_or_recorded(self):
        fixed = set(VV.numeric_tokens(strip_ph(TPL)))
        for s, (text, val, cases, flags) in FILLED.items():
            allowed = set(fixed)
            for p in val.prov.values():
                if p["kind"] in ("json", "derived", "table"):
                    allowed |= set(VV.numeric_tokens(p["formatted"]))
                elif p["kind"] == "text":                      # text: only numbers it is declared to contain, and
                    nums = set()                               # identifiers (versions, sections) of fixed wording
                    for ref in p.get("numbers", []):
                        nums |= set(VV.numeric_tokens(val.vals.get(ref, "")))
                    allowed |= nums
            allowed |= set(VV.numeric_tokens(" ".join(str(val.vals[k]) for k in
                                                      ("PREREG_TAG", "PREREG_COMMIT", "PREREG_DATE", "DEV_SENTENCE",
                                                       "VALIDATION_LINE", "FIG_DIR", "DROPPED", "R_GATE_SOURCE_WORD"))))
            allowed |= {"1.14", "1.12", "1.13", "1.11", "0.42", "1.9", "2.0", "6.6", "4.2", "4.3", "6.4", "7", "3",
                        "4", "5", "6", "1", "2", "0.30", "0.50", "95"}
            part = section(text, "# Abstract", "**Keywords") + section(text, "# 3. Results", "# 4. Discussion")
            stray = [t for t in VV.numeric_tokens(part) if t not in allowed]
            self.assertFalse(stray, f"{s}: {stray[:10]}")

    def test_structure_tests_appear_once_with_their_verdicts(self):
        for s, (text, val, cases, flags) in FILLED.items():
            st = load(s)["results"]["structure"]
            res = section(text, "# 3. Results", "# 4. Discussion")
            self.assertEqual(res.count(f"H\\_Structure is {st['H_Structure']['verdict']}"), 1, s)
            if st.get("H_PC_N3"):
                self.assertEqual(res.count(f"H\\_PC\\_N3 is {st['H_PC_N3']}"), 1, s)
            for key, t in (st.get("S_tests") or {}).items():
                a, b = t["pair"]
                rows = [l for l in val.vals["TABLE_S"].splitlines() if l.startswith(f"| {VV.NAME[a]} × {VV.NAME[b]} |")]
                self.assertEqual(len(rows), 1, f"{s}: {key}")
                self.assertIn(f"| {t['verdict']} |", rows[0])
            for x, t in (st.get("I_tests") or {}).items():
                rows = [l for l in val.vals["TABLE_I"].splitlines() if l.startswith(f"| {VV.NAME[x]} |")]
                self.assertEqual(len(rows), 1, f"{s}: I-test {x}")
                self.assertIn(f"| {t['verdict']}", rows[0])

    def test_ranking_marginal_as_the_plan_defines(self):
        """Section 4.2 MARGINAL row and W3: shown below the profile, under review, the marginal leg named, outside K,
        its pairs descriptive only, excluded from the composite check, retest pending while v1.14 has no final gate."""
        for s in ("ranking_marginal", "ranking_marginal_confirmed", "ranking_marginal_partial"):
            text, val, cases, flags = FILLED[s]
            V = load(s)["results"]
            self.assertEqual(V["gate_states"]["R"], "MARGINAL")
            self.assertNotIn("R", V["K"])
            self.assertIn("Ranking (retest pending) is MARGINAL: v1.14's Stage 1 interim verdict was MARGINAL "
                          "(H1\\_Sep\\_Presence, $\\rho_w$ = 0.410, $n$ = 70)", text)
            self.assertIn("shown in a separate band below the profile, labelled under review, and is not in $K$", text)
            self.assertIn("excluded from the composite check", text)
            self.assertIn("## 3.6 Parts under review", text)
            self.assertNotIn("Ranking", val.vals["TABLE_S"])
            self.assertIn("Ranking", val.vals["TABLE_MARGINAL"])
            for w in ("RANK_ABSTRACT", "RANK_DISCUSSION"):
                self.assertIn("retest pending", val.vals[w])
            self.assertNotIn("Ranking", val.vals["K_CAPTION"])

    def test_class_c_refused_without_the_draft_flag(self):
        with self.assertRaises(FP.FillError):
            FP.fill(FIX / "six_falsified", synthetic=True)
        self.assertIn("drafting paused", FILLED["six_falsified"][0])

    def test_every_case_and_flag_renders(self):
        text, val, cases, flags = FILLED["six_partial"]
        vals = dict(val.vals)
        for extra in ("R_LEGS", "COV_LEGS", "G_LEGS", "R_GATE_SOURCE_WORD", "DROPPED", "U_CAUSE"):
            vals.setdefault(extra, "x")
        for var, vs in EXPECTED.items():
            for v in vs:
                FP.render(TPL, vals, {**cases, var: v}, flags)
        for f in flags:
            FP.render(TPL, vals, cases, {**flags, f: not flags[f]})

    def test_samsung_only_in_coi_and_provisional_everywhere(self):
        for s, (text, val, cases, flags) in FILLED.items():
            coi = section(text, "## Conflict of interest", "## Funding")
            self.assertEqual(text.count("Samsung"), coi.count("Samsung"), s)
            self.assertEqual(text.count(AI_USE), 1)
            self.assertIn("(provisional)", text.splitlines()[1])
            self.assertIn(load(s)["results"]["validation_status_line"], text)


class TestRefusals(unittest.TestCase):
    def copy(self, s="ranking_marginal"):
        d = Path(tempfile.mkdtemp(prefix="aias6_ref_"))
        shutil.copytree(FIX / s, d / s)
        self.addCleanup(shutil.rmtree, d, True)
        return d / s

    def edit(self, d, name, fn):
        p = d / VV.NAMES[name]
        doc = json.loads(p.read_text(encoding="utf-8"))
        fn(doc)
        p.write_text(json.dumps(doc), encoding="utf-8")

    def test_real_mode_refuses_synthetic(self):
        with self.assertRaises(FP.FillError):
            FP.fill(FIX / "ranking_marginal")

    def test_synthetic_mode_refuses_real_looking_outputs(self):
        d = self.copy()
        for k in ("results", "gates", "inputs"):
            self.edit(d, k, lambda doc: doc.pop("synthetic_fixture", None))
        self.edit(d, "results", lambda doc: doc["MQ_Lock"].update(ok=True))
        with self.assertRaises(FP.FillError):
            FP.fill(d, synthetic=True)

    def test_state_not_the_scorers_refused(self):
        d = self.copy()
        for k in ("results", "gates"):
            self.edit(d, k, lambda doc: (doc["gate_states"].update(R="PASS_RETEST_PENDING"),
                                         doc.__setitem__("K", ["P", "C", "R", "Cov", "G"])))
        with self.assertRaises(FP.FillError):
            FP.fill(d, synthetic=True)

    def test_verdict_word_not_the_scorers_refused(self):
        d = self.copy()
        self.edit(d, "results", lambda doc: doc["structure"]["H_Structure"].update(verdict="PARTIAL"))
        with self.assertRaises(FP.FillError):
            FP.fill(d, synthetic=True)

    def test_tampered_component_file_refused(self):
        d = self.copy()
        p = d / "components" / "stage1_v1_14.json"
        doc = json.loads(p.read_text(encoding="utf-8"))
        doc["H1_Sep_Presence"]["rho"] = 0.2
        p.write_text(json.dumps(doc), encoding="utf-8")
        with self.assertRaises(FP.FillError):
            FP.fill(d, synthetic=True)

    def test_synthetic_output_inside_repo_refused(self):
        self.assertEqual(FP.main(["--synthetic", "--outputs", str(FIX / "ranking_marginal"),
                                  "--out", str(PAPER / "x_draft.md")]), 2)
        self.assertFalse((PAPER / "x_draft.md").exists())

    def test_charts_and_build_refuse_synthetic_without_watermark(self):
        with tempfile.TemporaryDirectory() as t:
            r = subprocess.run([sys.executable, str(ROOT / "scripts/build_charts_aias6.py"), "--outputs",
                                str(FIX / "ranking_marginal"), "--out", str(Path(t) / "f")], capture_output=True)
            self.assertEqual(r.returncode, 2)
            md = Path(t) / "d.md"
            FP.fill(FIX / "ranking_marginal", out=md, synthetic=True)
            r = subprocess.run([sys.executable, str(ROOT / "scripts/build_paper_aias6.py"), "--source", str(md),
                                "--output", str(Path(t) / "x.pdf")], capture_output=True)
            self.assertNotEqual(r.returncode, 0)
            self.assertFalse((Path(t) / "x.pdf").exists())

    def test_generator_refuses_osf(self):
        with self.assertRaises(SystemExit):
            MS.make(ROOT / "osf/aias_6_0_preview/outputs/synthetic_test", ["not_run"])
        self.assertFalse((ROOT / "osf/aias_6_0_preview/outputs/synthetic_test").exists())


if __name__ == "__main__":
    unittest.main(verbosity=1)
