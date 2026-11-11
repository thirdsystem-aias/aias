#!/usr/bin/env python3
"""
Tests of the v1.13 Grounding Paper A pipeline (values, fill, charts, build). SYNTHETIC fixtures only
(tests/fixtures/SYNTHETIC_*: the locked scorers' own functions on synthetic inputs, see make_scenarios_v1_13.py).
No real data is read (osf/v42 is never opened); nothing is written inside the repository.

    cd <worktree> && PYTHONDONTWRITEBYTECODE=1 python3 papers/v1_13/tests/test_fill_paper_v1_13.py
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
import fill_paper_v1_13 as F  # noqa: E402
import v113_values as VV  # noqa: E402

S = VV.S
FX = HERE / "fixtures"
SCEN = ["scored", "pass_reported", "downgraded", "downgraded_h6", "c1_h4", "fail", "marginal", "h3_undetermined",
        "dropped", "mq5", "floor", "interim"]
AI_USE = ("During the preparation of this work the author used AI tools (Anthropic's Claude) to assist with study "
          "design, analysis and writing. The author reviewed and edited all content and takes full responsibility "
          "for it.")
DENON = ("Correction (November 10, 2026): Denon, which replaced AKG in the v0.19 registry, has itself been owned by "
         "Harman International, a wholly owned subsidiary of Samsung Electronics, since September 23, 2025, when "
         "Harman completed its acquisition of Sound United from Masimo; the v0.19 headphones registry therefore "
         "includes one Samsung-group brand. The substitution did not achieve its purpose, and this was not noticed "
         "until November 10, 2026.")
TPL = F.TEMPLATE.read_text(encoding="utf-8")
CASE_VALUES = {
    "CASE_GATE": ["PASS", "FAIL", "MARGINAL", "MARGINAL_DOWNGRADED", "UNDETERMINED_MQ5", "UNDETERMINED"],
    "CASE_H1": ["CONFIRMED", "MARGINAL", "FALSIFIED", "UNDETERMINED_FLOOR", "UNDETERMINED_MQ5"],
    "CASE_H2": ["CONFIRMED", "MARGINAL", "FALSIFIED", "UNDETERMINED_FLOOR", "UNDETERMINED_MQ5"],
    "CASE_H3": ["CONFIRMED", "MARGINAL", "FALSIFIED", "UNDETERMINED_PAIRS"],
    "CASE_H4": ["INACTIVE", "PENDING", "UNAVAILABLE", "GATING", "REPORTED"],
    "CASE_H5": ["INACTIVE", "ACTIVE"],
    "CASE_H6": ["INACTIVE", "PENDING", "UNAVAILABLE", "COMPUTED"],
    "CASE_H7": ["CONFIRMED", "MARGINAL", "FALSIFIED", "UNDETERMINED_FLOOR", "NOT_COLLECTED", "PENDING"],
    "CASE_PART2": ["COLLECTED", "LOCKED_NOT_COLLECTED", "NOT_LOCKED", "PENDING"]}
# CLAUDE.md: declined by SSRN, or not yet posted -- never cited by number
DECLINED = ["6720959", "6722319", "6745040", "6748341", "6750498", "6842138", "6854758", "6865478", "6875319",
            "6880959", "6921758", "6927958", "7685126", "7685100", "7685199"]


def fx(name):
    v, s = FX / f"SYNTHETIC_{name}_v1_13_verdicts.json", FX / f"SYNTHETIC_{name}_v1_13_sdri.csv"
    return v, (s if s.exists() else None)


def load(name):
    return json.loads(fx(name)[0].read_text(encoding="utf-8"))


def fill_doc(doc, sdri=None, **kw):
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "v.json"
        p.write_text(json.dumps(doc), encoding="utf-8")
        return F.fill(p, sdri, None, "/tmp/figs", synthetic=kw.pop("synthetic", True), **kw)


def numbers(text):
    return set(VV.numeric_tokens(text))


def recompute_c1(d):
    """As make_scenarios_v1_13.recompute_c1: verdict words and gate from the scorer's functions."""
    mq5 = bool(d["MQ"]["MQ5"]["failed"])
    v = d["verdicts"]
    v["H1_Sep_Presence"] = S.sep_verdict(d["legs"]["H1_Sep_Presence"], mq5)
    v["H2_Sep_Consistency"] = S.sep_verdict(d["legs"]["H2_Sep_Consistency"], mq5)
    v["H3_Run_Reliability"] = S.reliability_verdict(d["H3"])
    gating = {"H4_Sep_Ranking": bool((d.get("H4_ranking_source") or {}).get("h4_gates"))}
    d["gate"] = json.loads(json.dumps(S.gate(v, d["gate"]["active"], gating), default=str))
    d["verdict_changes"] = {nm: {h: [sv["verdicts"][h], v[h]] for h in sv.get("verdicts", {}) if sv["verdicts"][h] != v[h]}
                            for nm, sv in (d.get("sensitivities") or {}).items() if "verdicts" in sv}


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
        for word in ("Samsung", "Harman", "Cheil"):
            self.assertNotIn(word, head, word)
            coi = decl.split("## Funding")[0]
            self.assertNotIn(word, decl.replace(coi, ""), word)

    def test_citations_only_from_references_bib_or_the_prereg(self):
        """Background cites only papers/references.bib entries (by their bib titles and numbers) or records the locked
        pre-registration names; no SSRN number of a declined or unposted paper; no ssrn.com link."""
        bib = (ROOT / "papers/references.bib").read_text(encoding="utf-8")
        for num in re.findall(r"\b(6\d{6}|7\d{6})\b", TPL):
            self.assertIn(num, bib, f"SSRN {num} is not in references.bib")
        for num in DECLINED:
            self.assertNotIn(num, TPL)
        self.assertNotIn("ssrn.com", TPL.lower())
        refs = TPL.split("# References {-}")[1].split("\\clearpage")[0]
        entries = [p.strip() for p in refs.strip().split("\n\n") if p.strip()]
        allowed = ("González Castro, P. U. (2026a)", "González Castro, P. U. (2026b)", "González Castro, P. U. (2026c)",
                   "Sharp, B. (2010)", "Sharp, B., & Romaniuk, J. (2021)", "Programme records cited by version")
        for e in entries:
            self.assertTrue(e.startswith(allowed), e[:60])
        prereg = (VV.DESIGN / "prereg/PRE_REGISTRATION_v1_13.md").read_text(encoding="utf-8")
        self.assertIn("HARMAN-Completes-Sound-United-Acquisition-to-Expand-Premium-Audio-Leadership", prereg)
        for t in ("AI Availability: A Theoretical Framework for Brand Surfacing in the Age of",
                  "Tri-System Brand Growth: Mental, Physical, and", "How Brands Grow: What Marketers Don't Know",
                  "How Brands Grow Part 2: Including Emerging Markets"):
            self.assertIn(t, refs)
            self.assertIn(t.replace("AI Availability", "{AI} Availability").replace("and AI", "and {AI}")
                          .replace("LLM", "{LLM}"), bib.replace("\n", " "))

    def test_thresholds_in_the_text_are_the_scorers(self):
        self.assertEqual((S.SEP_CONFIRM, S.SEP_FALSIFY), (0.30, 0.50))
        self.assertEqual((S.REL3_CONFIRM, S.REL3_FALSIFY, S.ALPHA), (0.50, 0.30, 0.05))
        self.assertEqual((S.H7_CONFIRM, S.H7_FALSIFY), (0.30, 0.10))
        self.assertEqual((S.FLOOR_G, S.FLOOR_G_RUN, S.FLOOR_UNITS, S.MIN_UNITS_PER_SUB), (6, 3, 30, 5))
        self.assertEqual((S.N_PERM, S.N_BOOT, S.CI_LEVEL), (10_000, 2_000, 90.0))
        self.assertEqual((S.MQ2_FLAG, S.MQ2_DROP, S.MQ3_FLAG, S.MQ3_LOW, S.MQ4_DROP), (0.25, 0.10, 0.40, 0.60, 0.20))
        self.assertEqual((S.MQ5_ZERO_SHARE, S.MQ5_FLAT_SUBSTRATES, S.MQ6_FLAG), (0.80, 3, 0.50))
        for t in ("rel3 $\\geq 0.50$, $p < 0.05$", "rel3 $< 0.30$", "$\\rho \\geq 0.30$, $p < 0.05$",
                  "$\\rho \\leq 0.10$", "g_b \\geq 6", "10,000 draws", "2,000 bootstrap", "113001--113010"):
            self.assertIn(t, TPL)

    def test_no_shipping_language(self):
        for w in ("ship", "launch", "adopt"):
            self.assertIsNone(re.search(rf"\b{w}", TPL, re.I), w)


class TestFixtures(unittest.TestCase):
    def test_fixtures_are_marked_synthetic(self):
        files = sorted(FX.iterdir())
        self.assertTrue(files)
        for f in files:
            self.assertTrue(f.name.startswith("SYNTHETIC_"), f.name)
            if f.suffix == ".json":
                self.assertIn("synthetic_fixture", json.loads(f.read_text(encoding="utf-8")))

    def test_every_fixture_is_consistent_with_the_scorer(self):
        for s in SCEN:
            with self.subTest(s=s):
                v, sd = fx(s)
                VV.check_consistency(VV.load_sources(v, sd))
                self.assertEqual(sd is not None, load(s)["synthetic_fixture"]["part2"] == "collected")

    def test_scenarios_cover_every_outcome(self):
        seen = {k: set() for k in ("gate", "h1", "h3", "h4", "h4word", "h6", "h6word", "h7", "part2")}
        for s in SCEN:
            V = load(s)
            seen["gate"].add(VV.case_gate(V))
            seen["h1"].add(VV.case_sep(V, "H1_Sep_Presence"))
            seen["h3"].add(VV.case_h3(V))
            for h, k in (("H4_Sep_Ranking", "h4"), ("H6_Sep_Coverage", "h6")):
                st = VV.cond_state(V, h)
                c = st["case"] if st["case"] != "COMPUTED" or h != "H4_Sep_Ranking" else \
                    ("GATING" if st["gating"] else "REPORTED")
                seen[k].add(c)
                if st["case"] == "COMPUTED":
                    seen[k + "word"].add(st["word"])
            seen["h7"].add(VV.h7_state(V)["case"])
            seen["part2"].add(V["synthetic_fixture"]["part2"])
        self.assertEqual(seen["gate"], set(CASE_VALUES["CASE_GATE"]))
        self.assertEqual(seen["h1"], {"CONFIRMED", "FALSIFIED", "UNDETERMINED_FLOOR", "UNDETERMINED_MQ5"})
        self.assertEqual(seen["h3"], {"CONFIRMED", "FALSIFIED", "UNDETERMINED_PAIRS"})
        self.assertEqual(seen["h4"], {"PENDING", "UNAVAILABLE", "GATING", "REPORTED"})
        self.assertEqual(seen["h4word"], {"CONFIRMED", "FALSIFIED", "UNDETERMINED"})
        self.assertEqual(seen["h6"], {"PENDING", "UNAVAILABLE", "COMPUTED"})
        self.assertEqual(seen["h6word"], {"CONFIRMED", "FALSIFIED"})
        self.assertEqual(seen["h7"], set(CASE_VALUES["CASE_H7"]))
        self.assertEqual(seen["part2"], {"collected", "not_run", "held"})


class TestFill(unittest.TestCase):
    def check_render(self, text, val, V, name):
        self.assertNotRegex(text, r"\{\{|\{%", name)
        self.assertIn(AI_USE, text)
        self.assertIn(DENON, text)
        head, decl = text.split("# Declarations {-}")
        for word in ("Samsung", "Harman", "Cheil"):
            self.assertNotIn(word, head, f"{name}: {word}")
            coi = decl.split("## Funding")[0]
            self.assertNotIn(word, decl.replace(coi, ""), f"{name}: {word}")
        fg = VV.final_gate(V)
        self.assertIn(f"**{fg['final']}**", text, name)
        for h in VV.GATE_LEGS:
            self.assertIn(V["verdicts"][h], text, f"{name}: {h}")
        self.assertNotIn("Pablo's", text, name)                    # the scorer's gate notes are never printed
        self.assertNotIn("not SEPARABLE (N19)", text, name)
        allowed = numbers(TPL)
        for p in val.prov.values():
            allowed |= numbers(p["formatted"])
        stray = numbers(text) - allowed
        self.assertEqual(stray, set(), f"{name}: numbers with no provenance {sorted(stray)[:10]}")

    def test_every_scenario_fills(self):
        for s in SCEN:
            with self.subTest(s=s):
                v, sd = fx(s)
                text, val, cases, flags = F.fill(v, sd, None, "/tmp/figs", synthetic=True)
                V = load(s)
                self.check_render(text, val, V, s)
                self.assertEqual(cases["CASE_GATE"], VV.case_gate(V))

    def test_provenance_re_resolves(self):
        for s in ("scored", "dropped"):
            v, sd = fx(s)
            text, val, cases, flags = F.fill(v, sd, None, "/tmp/figs", synthetic=True)
            n = 0
            for name, p in val.prov.items():
                if p["kind"] == "json":
                    raw = VV.jget(val.src[p["source"]], p["path"])
                    self.assertEqual(VV.FORMATS[p["fmt"]](raw), p["formatted"], name)
                    n += 1
                elif p["kind"] == "derived":
                    raws = [VV.jget(val.src[s_], pp) for s_, pp in p["refs"]]
                    self.assertEqual(VV.FORMATS[p["fmt"]](VV.DERIVE[p["fn"]](*p["consts"], *raws)), p["formatted"], name)
                elif p["kind"] == "table":
                    for c in p["cells"]:
                        self.assertEqual(VV.FORMATS[c["fmt"]](VV.jget(val.src[c["source"]], c["path"])), c["formatted"])
            self.assertGreater(n, 30)

    def test_every_gate_leg_case_renders(self):
        """H1/H2 legs and H3 under each verdict, words recomputed by the scorer (interim fixture: Stage C1 only)."""
        base = load("interim")
        plan = {"CONFIRMED": (0.1, False), "MARGINAL": (0.4, False), "FALSIFIED": (0.6, False),
                "UNDETERMINED_FLOOR": (0.2, True)}
        for h in ("H1_Sep_Presence", "H2_Sep_Consistency"):
            for case, (rho, below) in plan.items():
                with self.subTest(h=h, case=case):
                    d = copy.deepcopy(base)
                    leg = d["legs"][h][1]
                    leg["rho_w"] = rho
                    if below:
                        leg["n"], leg["below_n_floor"] = 24, True
                    recompute_c1(d)
                    self.assertEqual(VV.case_sep(d, h), case)
                    text, val, cases, flags = fill_doc(d)
                    self.check_render(text, val, d, f"{h}/{case}")
        for case, rel3 in (("CONFIRMED", 0.9), ("MARGINAL", 0.4), ("FALSIFIED", 0.2)):
            d = copy.deepcopy(base)
            d["H3"]["rel3"] = rel3
            recompute_c1(d)
            self.assertEqual(VV.case_h3(d), case)
            text, val, cases, flags = fill_doc(d)
            self.check_render(text, val, d, f"H3/{case}")

    def test_conditional_leg_words_render(self):
        """H4 and H6 computed at Stage C2 under MARGINAL (no re-issue change): the scorer's sep_verdict gives the word."""
        for h, key in (("H4_Sep_Ranking", "ranking"), ("H6_Sep_Coverage", "coverage")):
            d = load("scored")
            sd = fx("scored")[1]
            r = d["stage_C2"][key]
            r["leg"]["rho_w"] = 0.41
            r[h] = S.sep_verdict([r["leg"]])
            self.assertEqual(r[h], "MARGINAL")
            text, val, cases, flags = fill_doc(d, sd)
            self.assertIn(f"**MARGINAL**", text)
            self.check_render(text, val, d, h)

    def test_part2_and_dependency_wording(self):
        t_fail = F.fill(*fx("fail"), None, "/tmp/figs", synthetic=True)[0]
        self.assertIn("tag `v1.13-audit-r1` does not exist", t_fail)
        self.assertIn("handed to the second paper", t_fail)
        self.assertIn("score not available", t_fail)
        self.assertIn("goes back to design", t_fail)
        t_m = F.fill(*fx("marginal"), None, "/tmp/figs", synthetic=True)[0]
        self.assertIn("Part II was locked, but its audit had not been collected", t_m)
        self.assertIn("pre-registrant's recorded decision", t_m)
        t_i = F.fill(*fx("interim"), None, "/tmp/figs", synthetic=True)[0]
        self.assertIn("Stage C2 has not run", t_i)
        self.assertIn("H4 is pending", t_i)
        t_d = F.fill(*fx("downgraded"), None, "/tmp/figs", synthetic=True)[0]
        self.assertIn("downgraded", t_d)
        self.assertIn("H4 turned PASS into MARGINAL", t_d)
        t_c = F.fill(*fx("c1_h4"), None, "/tmp/figs", synthetic=True)[0]
        self.assertIn("At Stage C1, H4 (computed from its score at C1) downgraded the PASS to MARGINAL.", t_c)
        t_p = F.fill(*fx("pass_reported"), None, "/tmp/figs", synthetic=True)[0]
        self.assertIn("neither gates nor downgrades", t_p)
        self.assertIn("**PASS**", t_p)

    def test_cheil_switch_off_by_default(self):
        v, sd = fx("scored")
        text = F.fill(v, sd, None, "/tmp/figs", synthetic=True)[0]
        self.assertNotIn("Cheil", text)
        text, val, cases, flags = F.fill(v, sd, None, "/tmp/figs", synthetic=True, coi_cheil=True)
        coi = text.split("## Conflict of interest {-}")[1].split("## Funding")[0]
        self.assertIn("Cheil Worldwide", coi)
        self.check_render(text, val, load("scored"), "cheil")
        self.assertEqual({k for k in VV.CHEIL_UNITS} <= set(S.load_brand_domains()), True)
        names = {k: S.load_brand_domains()[k]["brand"] for k in VV.CHEIL_UNITS}
        self.assertEqual(set(names.values()), {"Chevrolet", "BMW", "Bentley", "Jack Daniel's", "Eucerin"})


class TestRefusals(unittest.TestCase):
    def test_inconsistent_word_refused(self):
        d = load("scored")
        d["verdicts"]["H1_Sep_Presence"] = "MARGINAL"
        with self.assertRaisesRegex(F.FillError, "H1_Sep_Presence"):
            fill_doc(d, fx("scored")[1])

    def test_wrong_reissue_refused(self):
        d = load("downgraded")
        d["stage_C2"]["ranking"]["gate_reissued"]["after"] = "PASS"
        with self.assertRaisesRegex(F.FillError, "re-issue"):
            fill_doc(d, fx("downgraded")[1])

    def test_sdri_and_part2_must_agree(self):
        with self.assertRaisesRegex(F.FillError, "no SDRI table"):
            fill_doc(load("scored"), None)
        with self.assertRaisesRegex(F.FillError, "not collected"):
            fill_doc(load("fail"), fx("scored")[1])
        with self.assertRaisesRegex(F.FillError, "H7 n"):
            fill_doc(load("scored"), fx("h3_undetermined")[1])     # half the home pages blocked: another n

    def test_real_mode_refuses_synthetic_and_relabelled(self):
        v, sd = fx("scored")
        with self.assertRaisesRegex(F.FillError, "synthetic"):
            F.fill(v, sd, None, None, synthetic=False)
        d = load("interim")
        d.pop("synthetic_fixture")
        with self.assertRaisesRegex(F.FillError, "Stage C2 has not run"):
            fill_doc(d, None, synthetic=False)
        with self.assertRaisesRegex(F.FillError, "112"):
            fill_doc(d, None, synthetic=False, interim=True)   # tag and anchor pass; 40 synthetic units do not

    def test_synthetic_mode_refuses_real_looking_file(self):
        d = load("scored")
        d.pop("synthetic_fixture")
        with self.assertRaisesRegex(F.FillError, "not synthetic"):
            fill_doc(d, fx("scored")[1])

    def test_synthetic_output_inside_repo_refused(self):
        v, sd = fx("scored")
        r = subprocess.run([sys.executable, str(PAPER / "fill_paper_v1_13.py"), "--synthetic", "--verdicts", str(v),
                            "--sdri", str(sd), "--out", str(PAPER / "x_draft.md")], capture_output=True, text=True)
        self.assertNotEqual(r.returncode, 0)
        self.assertFalse((PAPER / "x_draft.md").exists())

    def test_charts_refuse_synthetic_without_watermark(self):
        v, sd = fx("scored")
        with tempfile.TemporaryDirectory() as d:
            r = subprocess.run([sys.executable, str(ROOT / "scripts/build_charts_v113.py"), "--verdicts", str(v),
                                "--sdri", str(sd), "--out", d], capture_output=True, text=True)
            self.assertNotEqual(r.returncode, 0)
            self.assertIn("REFUSED", r.stdout + r.stderr)
            self.assertEqual(list(Path(d).iterdir()), [])

    def test_build_refuses_synthetic_without_watermark(self):
        v, sd = fx("scored")
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / "draft.md"
            F.fill(v, sd, out, "/tmp/figs", synthetic=True)
            r = subprocess.run([sys.executable, str(ROOT / "scripts/build_paper_v1_13.py"), "--source", str(out),
                                "--output", str(Path(d) / "x.pdf")], capture_output=True, text=True)
            self.assertNotEqual(r.returncode, 0)
            self.assertIn("watermark", r.stdout + r.stderr)
            self.assertFalse((Path(d) / "x.pdf").exists())

    def test_make_scenarios_refuses_osf(self):
        import make_scenarios_v1_13 as MS
        with self.assertRaises(SystemExit):
            MS.main([str(ROOT / "osf/methodology/v1_13/_x"), "interim", "--perm", "9", "--boot", "0"])
        self.assertFalse((ROOT / "osf/methodology/v1_13/_x").exists())


if __name__ == "__main__":
    unittest.main(verbosity=1)
