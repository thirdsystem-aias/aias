#!/usr/bin/env python3
"""
Tests of the v1.12 Coverage Paper A pipeline (fill, values, charts, packet). SYNTHETIC fixtures only
(tests/fixtures/SYNTHETIC_*: the locked scorer's own output on synthetic inputs, and scenarios derived from it with
the scorer's verdict functions and gate). No real data is read; nothing is written inside the repository.

    cd <worktree> && PYTHONDONTWRITEBYTECODE=1 python3 papers/v1_12/tests/test_fill_paper_v1_12.py
"""
import copy
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAPER = HERE.parent
ROOT = PAPER.parents[1]
sys.path.insert(0, str(PAPER))
sys.path.insert(0, str(HERE))
import fill_paper_v1_12 as F  # noqa: E402
import v112_values as VV  # noqa: E402
import make_scenarios_v1_12 as MS  # noqa: E402

FX = HERE / "fixtures"
SCEN = ["scored", "pass", "fail", "marginal", "downgraded", "undetermined", "instrument", "fallback"]
AI_USE = ("During the preparation of this work the author used AI tools (Anthropic's Claude) to assist with study "
          "design, analysis and writing. The author reviewed and edited all content and takes full responsibility "
          "for it.")
DENON = ("Correction (November 10, 2026): Denon, which replaced AKG in the v0.19 registry, has itself been owned by "
         "Harman International, a wholly owned subsidiary of Samsung Electronics, since September 23, 2025, when "
         "Harman completed its acquisition of Sound United from Masimo; the v0.19 headphones registry therefore "
         "includes one Samsung-group brand. The substitution did not achieve its purpose, and this was not noticed "
         "until November 10, 2026.")
TPL = F.TEMPLATE.read_text(encoding="utf-8")
CASE_VALUES = {"CASE_GATE": ["PASS", "FAIL", "MARGINAL", "MARGINAL_H7", "MARGINAL_TWO_MODEL", "UNDETERMINED",
                             "INSTRUMENT_FAIL"],
               "CASE_MSIT": ["PASSED", "FAILED"], "CASE_H5": ["INACTIVE", "GATING", "REPORTED", "UNAVAILABLE"],
               "CASE_H6": ["INACTIVE", "ACTIVE"], "CASE_PARITY": ["PASSED", "SYNTHETIC"]}
for _k in ("H1", "H2", "H3", "H4", "H7", "H8"):
    CASE_VALUES[f"CASE_{_k}"] = ["CONFIRMED", "MARGINAL", "FALSIFIED", "UNDETERMINED_FLOOR", "UNDETERMINED_REASON",
                                 "UNDETERMINED_DEGENERATE"]


def fx(name):
    return FX / f"SYNTHETIC_{name}_v112_verdicts.json", FX / f"SYNTHETIC_{name}_v112_unit_table.csv"


def fill_doc(doc, table):
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "v.json"
        p.write_text(json.dumps(doc), encoding="utf-8")
        return F.fill(p, table, None, "/tmp/figs", synthetic=True)


def numbers(text):
    return set(VV.numeric_tokens(text))


class TestTemplate(unittest.TestCase):
    def test_every_switch_value_matches_exactly_one_case(self):
        alts = F.switch_alternatives(TPL)
        self.assertEqual(set(alts) - set(CASE_VALUES), set(), "switch on an undeclared variable")
        for var, blocks in alts.items():
            for cases in blocks:
                for v in CASE_VALUES[var]:
                    n = sum(1 for a in cases if v in a)
                    self.assertEqual(n, 1, f"{var}={v} matches {n} cases in a block")

    def test_ai_use_coi_and_samsung_rule_in_template(self):
        self.assertIn(AI_USE, TPL)
        self.assertIn(DENON, TPL)
        head, decl = TPL.split("# Declarations {-}")
        self.assertNotIn("Samsung", head)
        coi = decl.split("## Funding")[0]
        self.assertNotIn("Samsung", decl.replace(coi, ""))


class TestFixtures(unittest.TestCase):
    def test_fixtures_are_marked_synthetic(self):
        files = sorted(FX.iterdir())
        self.assertTrue(files)
        for f in files:
            self.assertTrue(f.name.startswith("SYNTHETIC_"), f.name)
            if f.suffix == ".json":
                V = json.loads(f.read_text(encoding="utf-8"))
                self.assertIn("synthetic_fixture", V)
                self.assertTrue(VV.is_synthetic(V))

    def test_scenarios_cover_every_gate_and_h5_case(self):
        gates, h5 = set(), set()
        for s in SCEN:
            V = json.loads(fx(s)[0].read_text(encoding="utf-8"))
            gates.add(VV.case_gate(V))
            h5.add(VV.case_h5(V))
        self.assertEqual(gates, set(CASE_VALUES["CASE_GATE"]))
        self.assertEqual(h5, set(CASE_VALUES["CASE_H5"]))

    def test_scenario_words_are_the_scorers(self):
        """The derived scenarios' gate equals the scorer's gate() on their own verdicts."""
        S = MS.S
        for s in SCEN:
            V = json.loads(fx(s)[0].read_text(encoding="utf-8"))
            g = V["paper_A_verdict"]
            self.assertIn(g["verdict"], {"PASS", "FAIL", "MARGINAL", "UNDETERMINED", "INSTRUMENT FAIL"})
            for h, v in V["verdicts"].items():
                self.assertIn(v, S.VERDICTS)
            act = {h: (h in g["legs"]) for h in S.CONDITIONAL_LEGS}
            g2 = S.gate(V["MC"]["MC_Situation"]["passed"], V["verdicts"], act, False,
                        two_model=len(V["panels"][V["primary_panel"]]) == 2)
            self.assertEqual(g2["verdict"], g["verdict"], s)


class TestFill(unittest.TestCase):
    def check_render(self, text, val, V, name):
        self.assertNotRegex(text, r"\{\{|\{%", name)
        self.assertIn(AI_USE, text)
        self.assertIn(DENON, text)
        head, decl = text.split("# Declarations {-}")
        self.assertNotIn("Samsung", head, name)
        coi = decl.split("## Funding")[0]
        self.assertNotIn("Samsung", decl.replace(coi, ""), name)
        self.assertIn(f"**{V['paper_A_verdict']['verdict']}**", text, name)
        self.assertIn(V["paper_A_verdict"]["label"], text)
        for h, v in V["verdicts"].items():
            self.assertIn(v, text, f"{name}: {h} word {v} missing")
        # every number in the paper is fixed pre-registration text or a recorded value
        allowed = numbers(TPL)
        for p in val.prov.values():
            allowed |= numbers(p["formatted"])
        stray = numbers(text) - allowed
        self.assertEqual(stray, set(), f"{name}: numbers with no provenance {sorted(stray)[:10]}")

    def test_every_scenario_fills(self):
        for s in SCEN:
            with self.subTest(s=s):
                v, t = fx(s)
                text, val, cases, flags = F.fill(v, t, None, "/tmp/figs", synthetic=True)
                self.check_render(text, val, json.loads(v.read_text(encoding="utf-8")), s)

    def test_provenance_re_resolves(self):
        v, t = fx("pass")
        text, val, cases, flags = F.fill(v, t, None, "/tmp/figs", synthetic=True)
        n = 0
        for name, p in val.prov.items():
            if p["kind"] == "json":
                raw = VV.jget(val.src[p["source"]], p["path"])
                self.assertEqual(VV.FORMATS[p["fmt"]](raw), p["formatted"], name)
                n += 1
            elif p["kind"] == "derived":
                raws = [VV.jget(val.src[s], pp) for s, pp in p["refs"]]
                self.assertEqual(VV.FORMATS[p["fmt"]](VV.DERIVE[p["fn"]](*p["consts"], *raws)), p["formatted"], name)
            elif p["kind"] == "table":
                for c in p["cells"]:
                    self.assertEqual(VV.FORMATS[c["fmt"]](VV.jget(val.src[c["source"]], c["path"])), c["formatted"])
        self.assertGreater(n, 40)

    def test_every_leg_case_renders(self):
        base = json.loads(fx("pass")[0].read_text(encoding="utf-8"))
        t = fx("pass")[1]
        plan = {"CONFIRMED": (0.1, 0.01, False), "MARGINAL": (0.4, 0.01, False), "FALSIFIED": (0.6, 0.0001, False),
                "UNDETERMINED_FLOOR": (0.2, 0.01, True)}
        for h in VV.GATE_LEGS + VV.SEC_LEGS:
            for case, (rho, p, below) in plan.items():
                if h == "H4_Reliability" and case != "UNDETERMINED_FLOOR":
                    rho = {"CONFIRMED": 0.7, "MARGINAL": 0.25, "FALSIFIED": 0.05}[case]
                if h == "H8_Panel_Replication" and case != "UNDETERMINED_FLOOR":
                    rho = {"CONFIRMED": 0.8, "MARGINAL": 0.6, "FALSIFIED": 0.3}[case]
                with self.subTest(h=h, case=case):
                    d = copy.deepcopy(base)
                    MS.set_leg(d["legs"][h], MS.KIND[h], rho, p, below)
                    d["verdicts"][h] = d["legs"][h]["verdict"]
                    act = {"H5_Sep_Ranking": True, "H6_Sep_Sentiment": False}
                    d["paper_A_verdict"] = MS.S.gate(True, d["verdicts"], act)
                    self.assertEqual(VV.case_leg(d, h), case)
                    text, val, cases, flags = fill_doc(d, t)
                    self.check_render(text, val, d, f"{h}/{case}")
        d = copy.deepcopy(base)
        d["legs"]["H8_Panel_Replication"] = {"verdict": "UNDETERMINED", "reason": "['gpt-6-astra'] left the panel"}
        d["verdicts"]["H8_Panel_Replication"] = "UNDETERMINED"
        self.assertEqual(VV.case_leg(d, "H8_Panel_Replication"), "UNDETERMINED_REASON")
        text, val, _, _ = fill_doc(d, t)
        self.assertIn("GPT-6 Astra left the panel", text)

    def test_unknown_verdict_refused(self):
        d = json.loads(fx("pass")[0].read_text(encoding="utf-8"))
        d["paper_A_verdict"]["verdict"] = "PARTIAL"
        with self.assertRaises(ValueError):
            fill_doc(d, fx("pass")[1])


class TestRefusals(unittest.TestCase):
    def test_real_mode_refuses_synthetic(self):
        v, t = fx("pass")
        with self.assertRaises(F.FillError):
            F.fill(v, t, None, None, synthetic=False)

    def test_synthetic_mode_refuses_real_looking_verdicts(self):
        d = json.loads(fx("pass")[0].read_text(encoding="utf-8"))
        d.pop("synthetic_fixture")
        d["parity_gates"]["P1"]["passed"] = True
        with self.assertRaises(F.FillError):
            fill_doc(d, fx("pass")[1])

    def test_real_mode_path_on_a_relabelled_fixture(self):
        """Exercises verify_real and the deviations record in memory only (nothing is written). A synthetic document
        relabelled as real passes the tag/anchor checks only with MC_BrandFree recorded as passed."""
        d = json.loads(fx("pass")[0].read_text(encoding="utf-8"))
        d.pop("synthetic_fixture")
        d["parity_gates"]["P1"]["passed"] = True
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "v.json"
            p.write_text(json.dumps(d), encoding="utf-8")
            with self.assertRaises(F.FillError):                    # no MC_BrandFree record
                F.fill(p, fx("pass")[1], None, "/tmp/figs", synthetic=False)
            d["MC"]["MC_BrandFree"] = {"passed": True, "hits": []}
            p.write_text(json.dumps(d), encoding="utf-8")
            text, val, cases, flags = F.fill(p, fx("pass")[1], None, "/tmp/figs", synthetic=False)
        self.assertEqual(cases["CASE_PARITY"], "PASSED")
        self.assertNotIn("[Synthetic", text)
        self.assertIn(VV.git_tag_commit()[:10], text)
        self.assertIn("anchor/DEVIATIONS.md", text)

    def test_wrong_prereg_tag_refused(self):
        d = json.loads(fx("pass")[0].read_text(encoding="utf-8"))
        d["prereg_tag"] = "v1.12-prereg-r0"
        with self.assertRaises(F.FillError):
            fill_doc(d, fx("pass")[1])

    def test_synthetic_output_inside_repo_refused(self):
        v, t = fx("pass")
        r = subprocess.run([sys.executable, str(PAPER / "fill_paper_v1_12.py"), "--synthetic", "--verdicts", str(v),
                            "--table", str(t), "--out", str(PAPER / "x_draft.md")], capture_output=True, text=True)
        self.assertNotEqual(r.returncode, 0)
        self.assertFalse((PAPER / "x_draft.md").exists())

    def test_charts_refuse_synthetic_without_watermark(self):
        v, t = fx("pass")
        with tempfile.TemporaryDirectory() as d:
            r = subprocess.run([sys.executable, str(ROOT / "scripts/build_charts_v112.py"), "--verdicts", str(v),
                                "--table", str(t), "--out", d], capture_output=True, text=True)
            self.assertNotEqual(r.returncode, 0)
            self.assertIn("REFUSED", r.stdout + r.stderr)
            self.assertEqual(list(Path(d).iterdir()), [])

    def test_make_scenarios_refuses_osf(self):
        with self.assertRaises(SystemExit):
            MS.main([str(ROOT / "osf/methodology/v1_12/_x"), "pass", "--draws", "9"])
        self.assertFalse((ROOT / "osf/methodology/v1_12/_x").exists())


if __name__ == "__main__":
    unittest.main(verbosity=1)
