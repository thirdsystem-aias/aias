#!/usr/bin/env python3
"""
Tests of the v0.43 Stage 1 paper pipeline (values, fill, charts, build). SYNTHETIC fixtures only
(tests/fixtures/SYNTHETIC_*: the locked scorer's own output on invented units and synthetic Trends responses, made by
make_scenarios_v0_43.py). No real data is read; nothing is written inside the repository.

    cd <worktree> && PYTHONDONTWRITEBYTECODE=1 python3 papers/v0_43/tests/test_fill_paper_v0_43.py
"""
import copy
import json
import math
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
PAPER = HERE.parent
ROOT = PAPER.parents[1]
sys.path.insert(0, str(PAPER))
sys.path.insert(0, str(HERE))
import fill_paper_v0_43 as F  # noqa: E402
import v043_values as VV  # noqa: E402
import make_scenarios_v0_43 as MS  # noqa: E402

SC = VV.SC
FX = HERE / "fixtures"
SCEN = ["lead", "lag", "null", "marginal", "sparse"]
PREREG = (ROOT / "osf/v43/prereg/PRE_REGISTRATION_v0_43.md").read_text(encoding="utf-8")
TPL = F.TEMPLATE.read_text(encoding="utf-8")
AI_USE = ("During the preparation of this work the author used AI tools (Anthropic's Claude) to assist with study "
          "design, analysis and writing. The author reviewed and edited all content and takes full responsibility "
          "for it.")
DENON = ("Correction (November 10, 2026): Denon, which replaced AKG in the v0.19 registry, has itself been owned by "
         "Harman International, a wholly owned subsidiary of Samsung Electronics, since September 23, 2025, when "
         "Harman completed its acquisition of Sound United from Masimo; the v0.19 headphones registry therefore "
         "includes one Samsung-group brand. The substitution did not achieve its purpose, and this was not noticed "
         "until November 10, 2026.")
CASES = ["CONFIRMED", "MARGINAL", "FALSIFIED", "UNDETERMINED", "UNDETERMINED_N", "UNDETERMINED_RHO"]
CASE_VALUES = {f"CASE_{k}": CASES for k in VV.SHORT.values()}
CHEIL_BRANDS = ("Chevrolet", "BMW", "Bentley", "Jack Daniel's", "Eucerin")


def fx(name):
    return FX / f"SYNTHETIC_{name}_v43_stage1_verdicts.json", FX / f"SYNTHETIC_{name}_v43_pulls.json"


def load(name):
    v, p = fx(name)
    return json.loads(v.read_text(encoding="utf-8")), json.loads(p.read_text(encoding="utf-8"))


def fill_doc(doc, pulls, check=False, synthetic=True, **kw):
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "v.json"
        p.write_text(json.dumps(doc), encoding="utf-8")
        return F.fill(p, pulls, None, "/tmp/figs", synthetic=synthetic, check=check, **kw)


def numbers(text):
    return set(VV.numeric_tokens(text))


def coi(text):
    return text.split("## Conflict of interest {-}")[1].split("## Funding")[0]


def set_test(doc, name, rho, p1, p2, ci90, n, has_ci=True):
    """Give a test new statistics; verdict, labels and reason are the LOCKED scorer's verdict() on them."""
    T = doc["tests"][name]
    for k in ("rho", "p_one", "p_two", "ci90", "ci95", "boot_valid", "reason"):
        T.pop(k, None)
    T["n"] = n
    if rho is not None:
        T["rho"] = rho
    if p1 is not None:
        T["p_one"], T["p_two"] = p1, p2
    if has_ci and ci90 is not None:
        T["ci90"] = list(ci90)
        T["ci95"] = [ci90[0] - 0.05, ci90[1] + 0.05]
        T["boot_valid"] = doc["B_boot"]
    v = SC.verdict(rho if rho is not None else None, p1, p2, ci90[1] if (has_ci and ci90) else None, n, T["min_n"])
    T.update(verdict=v["verdict"], labels=v["labels"], reason=v["reason"])
    return T


def swap_two_outcomes(d, pulls):
    """Swap the change Y of two headphone brands in the unit table: their ranks change, so the recomputed rho must."""
    rows = [r for r in d["unit_table"] if r["sub"] == "v0.19" and VV.finite(r.get("Y"))]
    a, b = sorted(rows, key=lambda r: r["Y"])[0], sorted(rows, key=lambda r: r["Y"])[-1]
    a["Y"], b["Y"] = b["Y"], a["Y"]


PLAN = {  # case -> list of (rho, p1, p2, ci90, n_offset, has_ci, reversed)
    "CONFIRMED": [(0.30, 0.001, 0.002, (0.15, 0.45), 40, True, False)],
    "MARGINAL": [(0.12, 0.08, 0.16, (-0.03, 0.27), 40, True, False)],
    "FALSIFIED": [(0.02, 0.40, 0.80, (-0.12, 0.09), 40, True, False),
                  (-0.30, 0.999, 0.003, (-0.45, -0.15), 40, True, True)],
    "UNDETERMINED": [(0.05, 0.30, 0.60, (-0.10, 0.20), 40, True, False),
                     (-0.20, 0.98, 0.04, (-0.38, 0.11), 40, True, True)],
    "UNDETERMINED_N": [(0.30, 0.01, 0.02, (0.10, 0.50), -1, True, False),
                       (None, None, None, None, None, False, False)],
    "UNDETERMINED_RHO": [(float("nan"), 1.0, 1.0, None, 40, False, False)],
}


class TestTemplate(unittest.TestCase):
    def test_every_switch_value_matches_exactly_one_case(self):
        alts = F.switch_alternatives(TPL)
        self.assertEqual(set(alts) - set(CASE_VALUES), set(), "switch on an undeclared variable")
        self.assertEqual(set(alts), set(CASE_VALUES))
        for var, blocks in alts.items():
            for cases in blocks:
                for v in CASE_VALUES[var]:
                    n = sum(1 for a in cases if v in a)
                    self.assertEqual(n, 1, f"{var}={v} matches {n} cases in a block")

    def test_declarations_follow_the_locked_text(self):
        """AI-use statement verbatim; the COI paragraph is the pre-registration's section 7 text, word for word, plus
        only the optional Cheil sentence; Samsung appears only in the COI paragraph."""
        self.assertIn(AI_USE, TPL)
        self.assertIn(DENON, TPL)
        pre_coi = PREREG.split("**Conflict of interest.** ")[1].split("\n")[0].strip()
        tpl_coi = coi(TPL).strip()
        no_cheil = re.sub(r"\{% if COI_CHEIL %\}.*?\{% endif %\}", "", tpl_coi, flags=re.S)
        # one change of tense, the only edit to the locked text: "this pre-registration is locked" (written before the
        # lock) -> "the pre-registration was locked" (the paper, written after it)
        norm = lambda s: (s.replace("---", "—").replace("--", "–")  # noqa: E731
                          .replace("the pre-registration was locked", "this pre-registration is locked"))
        self.assertEqual(norm(no_cheil), pre_coi)
        head, decl = TPL.split("# Declarations {-}")
        self.assertNotIn("Samsung", head)
        self.assertNotIn("Samsung", decl.replace(coi(TPL), ""))
        self.assertNotIn("Harman", head)

    def test_hypotheses_and_thresholds_quoted_from_the_prereg(self):
        quotes = re.findall("\u201c([^\u201d]{30,})\u201d", TPL.split("# 2. Method")[1].split("# 3. Results")[0])
        self.assertGreaterEqual(len(quotes), 4)
        flat = lambda s: re.sub(r"\$\\rho\$", "ρ", s).replace("$", "")  # noqa: E731
        for q in quotes:
            self.assertIn(flat(q), PREREG, q[:60])
        for s in ("(§2.2", "(§2.3)", "(§2.1)", "(§2.7)", "(§2.8)", "(§4.3)", "(§4.4)", "(§4.6)", "(§3.2)", "(§5.5)"):
            self.assertIn(s, TPL)
        for thr in ("\\geq 0.15$ and $p < 0.05$", "below 0.10", "$p < 0.10$", "fewer than 60", "30 for the Consistency"):
            self.assertIn(thr, TPL)

    def test_citations(self):
        """No SSRN number or ssrn.com link for a paper SSRN declined or has not posted (v1.9, v0.25, v0.28, v0.11,
        v0.41, v0.37 ...); v1.9 by title with its thirdsystem.ai and OSF copies; the foundational paper as references.bib
        has it; no SSRN packet step."""
        declined = ["6720959", "6722319", "6745040", "6748341", "6750498", "6842138", "6854758", "6865478", "6875319",
                    "6880959", "6921758", "6927958", "7685126"]
        for i in declined + ["7685100", "7685199"]:
            self.assertNotIn(i, TPL)
        self.assertNotIn("ssrn.com", TPL.lower())
        refs = TPL.split("# References {-}")[1]
        v19 = [ln for ln in refs.splitlines() if "Methodology v1.9" in ln]
        self.assertEqual(len(v19), 1)
        for u in ("<https://thirdsystem.ai/studies/v1-9/>", "<https://osf.io/ec6wh/files/osfstorage/6af1fd459966c813ee53ba87>"):
            self.assertIn(u, v19[0])
        # canonical forms of CLAUDE.md ("Methodology citation chain (canonical)", "Phase SSRN ID registry")
        for t, i in (("AI Availability: Extending Mental and Physical Availability into Algorithmic Retrieval", "6659000"),
                     ("Consistency without Independence", "6878818"), ("A Mean-Independent Consistency Instrument", "6963359"),
                     ("What AI Presence Does Not Predict", "6847678"), ("The Presence Component Is Construct-Valid", "6870778")):
            self.assertRegex(refs, rf"\*{re.escape(t)}[^\n]*SSRN {i}\.")
        for i in ("6761698", "6797679", "6799479", "6810758", "6816340", "6817841", "6809182", "6811441", "6815378", "6829118", "6834298"):
            self.assertIn(f"SSRN {i}", refs)
        for u in ("<https://thirdsystem.ai/studies/v0-25/>", "<https://thirdsystem.ai/studies/v0-41/>"):
            self.assertIn(u, refs)
        # every lettered reference is cited in the text and every in-text letter has a reference
        body = TPL.split("# References {-}")[0]
        have = set(re.findall(r"(?m)^González Castro, P\. U\. \(2026([a-z])\)", refs))
        cited = set(re.findall(r"2026([a-z])(?![a-z])", body))
        self.assertEqual(have - cited, set())
        self.assertEqual(cited - have, set())
        self.assertNotIn("SSRN packet", TPL)
        self.assertNotIn("ssrn_submission", TPL)


class TestFixtures(unittest.TestCase):
    def test_fixtures_are_marked_synthetic(self):
        files = sorted(FX.iterdir())
        self.assertEqual(len(files), 2 * len(SCEN))
        for f in files:
            self.assertTrue(f.name.startswith("SYNTHETIC_"), f.name)
        for s in SCEN:
            V, P = load(s)
            self.assertTrue(VV.is_synthetic(V))
            self.assertTrue(all(r["unit"].startswith("SYN-") for r in V["unit_table"]))
            self.assertTrue(P["raw_dir"].startswith("SYNTHETIC"))
            self.assertEqual((V["B_perm"], V["B_boot"]), (10000, 10000))

    def test_fixtures_are_the_locked_scorers_output(self):
        """Every verdict, label, flag and check in each fixture re-derives with the scorer's own functions, and each
        test's rho recomputes from the unit table."""
        for s in SCEN:
            V, P = load(s)
            with self.subTest(s=s):
                self.assertTrue(VV.check_consistency(V, real=True))
                F.check_pulls(V, P, real=True)

    def test_fixtures_cover_the_outcomes(self):
        prim, rev, flags, conc, rel, terms, missing, broken = set(), False, set(), set(), set(), set(), 0, 0
        for s in SCEN:
            V, _ = load(s)
            prim.add(VV.case_test(V["tests"]["H_Pred_Presence"]))
            rev |= any(VV.reversed_label(T) for T in V["tests"].values())
            flags |= set(V["flags"])
            mc = V["manipulation_checks"]
            conc.add(mc["MC_Concurrent"]["pass_"])
            rel.add(mc["MC_PullReliability"]["pass_"])
            terms.add(mc["MC_Terms"]["pass_"])
            missing += mc["MC_Weekly"]["missing"]
            broken += sum(v["links"] - v["links_held"] for st in mc["MC_Chain"].values() for v in st.values())
        self.assertEqual(prim, {"CONFIRMED", "MARGINAL", "FALSIFIED", "UNDETERMINED", "UNDETERMINED_N"})
        self.assertTrue(rev)
        self.assertEqual(flags, set(VV.FLAG_WORDS))
        self.assertEqual(conc, {True, False})
        self.assertEqual(rel, {True, False})
        self.assertEqual(terms, {True, False})
        self.assertGreater(missing, 0)
        self.assertGreater(broken, 0)


class TestFill(unittest.TestCase):
    def check_render(self, text, val, V, name, synthetic=True):
        self.assertNotRegex(text, r"\{\{|\{%", name)
        self.assertIn(AI_USE, text)
        self.assertIn(DENON, text)
        head, decl = text.split("# Declarations {-}")
        self.assertNotIn("Samsung", head, name)
        self.assertNotIn("Samsung", decl.replace(coi(text), ""), name)
        for n_, T in V["tests"].items():
            self.assertIn(f"**{T['verdict']}**", text, f"{name}: {n_}")
            if VV.reversed_label(T):
                self.assertIn("REVERSED", text)
        for f in V["flags"]:
            self.assertIn(f, text)
        if synthetic:
            self.assertIn("SYNTHETIC TEST RUN", text)
        else:
            self.assertNotIn("SYNTHETIC", text)
        allowed = numbers(TPL)
        for p in val.prov.values():
            allowed |= numbers(p["formatted"])
        stray = numbers(text) - allowed
        self.assertEqual(stray, set(), f"{name}: numbers with no provenance {sorted(stray)[:10]}")

    def test_every_fixture_fills(self):
        for s in SCEN:
            with self.subTest(s=s):
                v, p = fx(s)
                text, val, cases, flags = F.fill(v, p, None, "/tmp/figs", synthetic=True)
                self.check_render(text, val, json.loads(v.read_text(encoding="utf-8")), s)
                self.assertNotIn("Cheil", text)

    def test_provenance_re_resolves(self):
        v, p = fx("sparse")
        text, val, cases, flags = F.fill(v, p, None, "/tmp/figs", synthetic=True)
        n = 0
        for name, pv in val.prov.items():
            if pv["kind"] == "json":
                raw = VV.jget(val.src[pv["source"]], pv["path"])
                self.assertEqual(VV.FORMATS[pv["fmt"]](raw), pv["formatted"], name)
                n += 1
            elif pv["kind"] == "derived":
                raws = [VV.jget(val.src[s], pp) for s, pp in pv["refs"]]
                self.assertEqual(VV.FORMATS[pv["fmt"]](VV.DERIVE[pv["fn"]](*pv["consts"], *raws)), pv["formatted"])
            elif pv["kind"] == "table":
                for c in pv["cells"]:
                    self.assertEqual(VV.FORMATS[c["fmt"]](VV.jget(val.src[c["source"]], c["path"])), c["formatted"])
        self.assertGreater(n, 40)

    def test_every_outcome_renders_for_every_test(self):
        """Each test under every outcome the pre-registration allows (CONFIRMED, MARGINAL, FALSIFIED with and without
        REVERSED, UNDETERMINED with and without REVERSED, UNDETERMINED below the minimum n with and without a
        statistic, UNDETERMINED with rho undefined); words from the locked scorer's verdict()."""
        base, pulls = load("lead")
        for name in VV.TESTS:
            for case, plans in PLAN.items():
                for rho, p1, p2, ci90, noff, has_ci, rev in plans:
                    with self.subTest(test=name, case=case, rev=rev):
                        d = copy.deepcopy(base)
                        minn = d["tests"][name]["min_n"]
                        n = 2 if noff is None else minn + noff
                        T = set_test(d, name, rho, p1, p2, ci90, n, has_ci)
                        self.assertEqual(VV.case_test(T), case)
                        self.assertEqual(VV.reversed_label(T), rev)
                        text, val, cases, flags = fill_doc(d, pulls)
                        self.assertEqual(cases[f"CASE_{VV.SHORT[name]}"], case)
                        self.check_render(text, val, d, f"{name}/{case}")
                        if rev:
                            self.assertIn("**REVERSED**", text)

    def test_every_flag_combination_renders(self):
        base, pulls = load("lead")
        for mask in range(8):
            fl = [w for i, w in enumerate(VV.FLAG_WORDS) if mask >> i & 1]
            with self.subTest(flags=fl):
                d = copy.deepcopy(base)
                d["flags"] = fl
                for T in d["tests"].values():
                    T["flags"] = fl
                mc = d["manipulation_checks"]
                mc["MC_Concurrent"]["pass_"] = "criterion doubtful" not in fl
                mc["MC_PullReliability"]["pass_"] = "outcome unreliable" not in fl
                mc["MC_Terms"]["pass_"] = "mostly plain search terms" not in fl
                text, val, cases, flags = fill_doc(d, pulls)
                self.check_render(text, val, d, str(fl))
                if fl:
                    self.assertIn(f"carries the flag{'s' if len(fl) > 1 else ''} ", text)
                else:
                    self.assertIn("No check raised a flag", text)

    def test_coi_cheil_switch_is_off_by_default(self):
        v, p = fx("lead")
        off, *_ = F.fill(v, p, None, "/tmp/figs", synthetic=True)
        on, val, _, flags = F.fill(v, p, None, "/tmp/figs", synthetic=True, coi_cheil=True)
        self.assertNotIn("Cheil", off)
        self.assertNotIn("v0.62", off)
        self.assertTrue(flags["COI_CHEIL"])
        c = coi(on)
        self.assertIn("Cheil Worldwide, a Samsung affiliate, or its Iris unit", c)
        for b in CHEIL_BRANDS:
            self.assertIn(b, c)
        self.assertEqual(on.count("Cheil"), 1)
        self.check_render(on, val, json.loads(v.read_text(encoding="utf-8")), "cheil on")

    def test_unknown_verdict_or_label_refused(self):
        d, pulls = load("lead")
        d["tests"]["H_Pred_Presence"]["verdict"] = "PARTIAL"
        with self.assertRaises(VV.Inconsistent):
            fill_doc(d, pulls)
        d, pulls = load("lead")
        d["tests"]["H_Pred_Presence"]["labels"] = ["LAGGING"]
        with self.assertRaises(VV.Inconsistent):
            fill_doc(d, pulls)


class TestRefusals(unittest.TestCase):
    def tampered(self, fn):
        """Strictest path: the lead fixture relabelled as real (in memory only), then tampered."""
        d, pulls = load("lead")
        d.pop("synthetic_fixture")
        fill_doc(d, pulls, check=True, synthetic=False)          # untampered: accepted
        fn(d, pulls)
        with self.assertRaises(F.FillError):
            fill_doc(d, pulls, check=True, synthetic=False)

    def test_inconsistent_verdicts_refused(self):
        T = "H_Pred_Presence"
        cases = {
            "rho": lambda d, p: d["tests"][T].__setitem__("rho", d["tests"][T]["rho"] + 0.01),
            "word": lambda d, p: d["tests"][T].__setitem__("verdict", "MARGINAL"),
            "label": lambda d, p: d["tests"][T].__setitem__("labels", ["REVERSED"]),
            "flags": lambda d, p: d.__setitem__("flags", ["outcome unreliable"]),
            "test flags": lambda d, p: d["tests"][T].__setitem__("flags", ["criterion doubtful"]),
            "seed": lambda d, p: d["tests"][T].__setitem__("seed", 430042),
            "min_n": lambda d, p: d["tests"][T].__setitem__("min_n", 30),
            "spec": lambda d, p: d["tests"][T]["spec"].__setitem__("controls", []),
            "n": lambda d, p: d["tests"][T]["n_per_substrate"].__setitem__("v0.19", 3),
            "unit table": swap_two_outcomes,
            "intervals": lambda d, p: d["tests"][T].__setitem__("ci95", [0.3, 0.31]),
            "MC pass": lambda d, p: d["manipulation_checks"]["MC_Concurrent"].__setitem__("pass_", False),
            "weekly vs records": lambda d, p: p["steps"]["main2"].__setitem__("ok", 27),
            "draws": lambda d, p: d.__setitem__("B_perm", 999),
            "pulls used": lambda d, p: d.__setitem__("pulls_used", ["main1", "main2"]),
            "stage": lambda d, p: d.__setitem__("stage", 2),
            "missing test": lambda d, p: d["tests"].pop("H_Pred_Consistency"),
            "missing ci": lambda d, p: d["tests"][T].pop("ci90"),
            "defined counts": lambda d, p: d["outcome_defined_per_substrate"]["v0.20"].__setitem__("Y_defined", 3),
        }
        for k, fn in cases.items():
            with self.subTest(k):
                self.tampered(fn)

    def test_real_mode_refuses_synthetic_and_synthetic_mode_refuses_real(self):
        v, p = fx("lead")
        with self.assertRaises(F.FillError):
            F.fill(v, p, None, None, synthetic=False)
        d, pulls = load("lead")
        d.pop("synthetic_fixture")
        with self.assertRaises(F.FillError):
            fill_doc(d, pulls, check=True, synthetic=True)

    def test_real_mode_path_on_a_relabelled_fixture(self):
        """In memory only: a synthetic document relabelled as real passes every real-mode check (lock, consistency,
        112 units, 84 requests, 3 pulls 24 h apart) and renders without any synthetic mark."""
        d, pulls = load("lead")
        d.pop("synthetic_fixture")
        text, val, cases, flags = fill_doc(d, pulls, check=True, synthetic=False)
        self.assertNotIn("SYNTHETIC", text)
        self.assertIn(VV.EXPECTED_COMMIT[:10], text)
        self.assertIn("osf/v43/anchor/DEVIATIONS.md", text)
        p2 = copy.deepcopy(pulls)
        p2["steps"]["main2"]["first_utc"] = "2026-11-12T20:00:00+00:00"
        with self.assertRaisesRegex(F.FillError, "24 hours"):
            fill_doc(d, p2, check=True, synthetic=False)
        p3 = copy.deepcopy(pulls)
        p3["steps"].pop("main3")
        with self.assertRaisesRegex(F.FillError, "main3"):
            fill_doc(d, p3, check=True, synthetic=False)

    def test_real_main_refuses_without_scorer_output(self):
        if (ROOT / "osf/v43/v43_stage1_verdicts.json").exists():
            self.skipTest("Stage 1 has been scored in this worktree")
        r = subprocess.run([sys.executable, str(PAPER / "fill_paper_v0_43.py"), "--out", "/tmp/_v043_never.md"],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 3)
        self.assertIn("REFUSED", r.stderr)
        r = subprocess.run([sys.executable, str(PAPER / "fill_paper_v0_43.py"), "--pulls", str(fx("lead")[1])],
                           capture_output=True, text=True)
        self.assertNotEqual(r.returncode, 0)

    def test_lock_records(self):
        self.assertEqual(F.verify_lock(), VV.EXPECTED_COMMIT)
        self.assertEqual(VV.manifest_mismatches(), [])
        orig = F.DEVIATIONS
        with tempfile.TemporaryDirectory() as tmp:
            fake = Path(tmp) / "DEVIATIONS.md"
            fake.write_text(orig.read_text(encoding="utf-8").replace("00:31 CT", "01:31 CT"), encoding="utf-8")
            F.DEVIATIONS = fake
            try:
                with self.assertRaisesRegex(F.FillError, "lock time"):
                    F.deviations_text()
            finally:
                F.DEVIATIONS = orig
        s, status, _ = F.deviations_text()
        self.assertIn("Entry 1, clarification C11", s)

    def test_synthetic_outputs_inside_repo_refused(self):
        v, p = fx("lead")
        r = subprocess.run([sys.executable, str(PAPER / "fill_paper_v0_43.py"), "--synthetic", "--verdicts", str(v),
                            "--pulls", str(p), "--out", str(PAPER / "x_draft.md")], capture_output=True, text=True)
        self.assertNotEqual(r.returncode, 0)
        self.assertFalse((PAPER / "x_draft.md").exists())
        with self.assertRaises(SystemExit):
            MS.main([str(PAPER / "_x"), "lead", "--draws", "9"])
        self.assertFalse((PAPER / "_x").exists())

    def test_charts_watermark_rules_and_build(self):
        v, _ = fx("sparse")
        with tempfile.TemporaryDirectory() as d:
            r = subprocess.run([sys.executable, str(ROOT / "scripts/build_charts_v043.py"), "--verdicts", str(v),
                                "--out", d], capture_output=True, text=True)
            self.assertNotEqual(r.returncode, 0)
            self.assertIn("REFUSED", r.stdout + r.stderr)
            self.assertEqual(list(Path(d).iterdir()), [])
            r = subprocess.run([sys.executable, str(ROOT / "scripts/build_charts_v043.py"), "--verdicts", str(v),
                                "--out", d, "--watermark", VV.SYNTHETIC_MARK], capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr[-800:])
            self.assertEqual(len(list(Path(d).glob("chart_0*.pdf"))), 8)
        r = subprocess.run([sys.executable, str(ROOT / "scripts/build_charts_v043.py"), "--verdicts", str(v),
                            "--out", str(ROOT / "reports/figs/_v043_test"), "--watermark", VV.SYNTHETIC_MARK],
                           capture_output=True, text=True)
        self.assertNotEqual(r.returncode, 0)
        self.assertFalse((ROOT / "reports/figs/_v043_test").exists())

    def test_build_refuses_synthetic_without_watermark(self):
        v, p = fx("lead")
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / "draft.md"
            F.fill(v, p, out, "/tmp/figs", synthetic=True)
            r = subprocess.run([sys.executable, str(ROOT / "scripts/build_paper_v0_43.py"), "--source", str(out),
                                "--output", str(Path(d) / "x.pdf")], capture_output=True, text=True)
            self.assertNotEqual(r.returncode, 0)
            self.assertIn("watermark", r.stdout + r.stderr)
            self.assertFalse((Path(d) / "x.pdf").exists())

    def test_locked_files_untouched(self):
        r = subprocess.run(["git", "-C", str(ROOT), "status", "--porcelain", "--", "osf/v43"], capture_output=True,
                           text=True)
        self.assertEqual(r.stdout.strip(), "")
        self.assertFalse((ROOT / "osf/v43/v43_stage1_verdicts.json").exists() and
                         VV.is_synthetic(json.loads((ROOT / "osf/v43/v43_stage1_verdicts.json").read_text())))


if __name__ == "__main__":
    unittest.main(verbosity=1)
