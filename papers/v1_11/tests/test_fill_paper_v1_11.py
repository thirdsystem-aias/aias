#!/usr/bin/env python3
"""
Tests of the v1.11 Sentiment Paper A pipeline (SYNTHETIC DATA ONLY; nothing under osf/ is read except the locked
DEVIATIONS record and anchor, nothing is written inside the repository).

  python3 papers/v1_11/tests/test_fill_paper_v1_11.py

Scenarios are generated into a temporary folder by make_scenarios_v1_11.py from the committed base fixtures (the
scorer's own dry-run Stage J / Stage C outputs).
"""
import copy
import hashlib
import json
import math
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
sys.path.insert(0, str(PAPER))
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "scripts"))
import fill_paper_v1_11 as FP  # noqa: E402
import make_scenarios_v1_11 as MS  # noqa: E402
import v111_values as VV  # noqa: E402
import score_v1_11 as S  # noqa: E402

TPL = (PAPER / "v1_11_paper_template.md").read_text(encoding="utf-8")
AI_USE = ("During the preparation of this work the author used AI tools (Anthropic's Claude) to assist with study "
          "design, analysis and writing. The author reviewed and edited all content and takes full responsibility "
          "for it.")
EXPECTED_CASES = {
    "CASE_H1": {"CONFIRMED", "MARGINAL", "FALSIFIED", "UNDETERMINED"},
    "CASE_H2": {"CONFIRMED", "MARGINAL", "FALSIFIED", "UNDETERMINED_GUARD", "UNDETERMINED_WAVES"},
    "CASE_H3": {"CONFIRMED", "MARGINAL", "FALSIFIED", "UNDETERMINED_GUARD", "UNDETERMINED_WAVES"},
    "CASE_H5": {"CONFIRMED", "MARGINAL", "FALSIFIED", "UNDETERMINED_GUARD", "UNDETERMINED_WAVES", "PENDING",
                "INACTIVE"},
    "CASE_H8": {"CONFIRMED", "MARGINAL", "FALSIFIED", "UNDETERMINED_GUARD", "UNDETERMINED_WAVES"},
    "CASE_H4": {"CONFIRMED", "MARGINAL", "FALSIFIED_RHO", "FALSIFIED_P", "UNDETERMINED"},
    "CASE_H6": {"CONFIRMED", "MARGINAL", "FALSIFIED_RHO", "FALSIFIED_P", "UNDETERMINED"},
    "CASE_H7": {"CONFIRMED", "MARGINAL", "FALSIFIED", "UNDETERMINED_GUARD", "UNDETERMINED_FLOOR"},
    "CASE_H9": {"CONFIRMED", "MARGINAL", "FALSIFIED", "UNDETERMINED"},
    "CASE_OVERALL": {"SEPARABLE", "SEPARABLE_FLAGGED", "NOT_SEPARABLE", "MIXED", "INSTRUMENT_FAILED", "UNSTABLE",
                     "INSTRUMENT_UNDETERMINED"},
}
TMP = None
FILLED = {}


def setUpModule():
    global TMP
    TMP = Path(tempfile.mkdtemp(prefix="v111_tests_"))
    MS.make(TMP / "synth")
    for s in MS.SCENARIOS:
        FILLED[s] = FP.fill(TMP / "synth" / s, out=TMP / s / "v1_11_paper_draft.md", fig_dir="figs", synthetic=True)


def tearDownModule():
    shutil.rmtree(TMP, ignore_errors=True)


def scen(s):
    return TMP / "synth" / s


def load(s):
    return VV.load_sources(scen(s))


def section(text, start, end):
    a = text.index(start)
    b = text.index(end, a)
    return text[a:b]


def keyset(o, depth=2, pre=""):
    out = set()
    if isinstance(o, dict) and depth:
        for k, v in o.items():
            out.add(pre + str(k))
            out |= keyset(v, depth - 1, pre + str(k) + "/")
    return out


class TestTemplate(unittest.TestCase):
    def test_every_switch_value_matches_exactly_one_case(self):
        alts = FP.switch_alternatives(TPL)
        self.assertEqual(set(alts), set(EXPECTED_CASES))
        for var, occurrences in alts.items():
            for cases in occurrences:
                flat = [a for c in cases for a in c]
                self.assertEqual(len(flat), len(set(flat)), f"{var}: a value appears in two cases")
                self.assertEqual(set(flat), EXPECTED_CASES[var], f"{var}: cases differ from the expected outcomes")

    def test_ai_use_and_coi_in_template(self):
        self.assertEqual(TPL.count(AI_USE), 1)
        coi = section(TPL, "## Conflict of interest", "## Funding")
        for s in ("a Samsung subsidiary since March 2017", "Sound United", "Denon included, on September 23, 2025",
                  "already a Samsung-group brand", "tier-2/3", "Samsung SDI", "Samsung Display",
                  "had no role in the design"):
            self.assertIn(s, coi)

    def test_citations_canonical(self):
        refs = section(TPL, "# References", "\\clearpage\n\n# Appendix")
        self.assertNotIn("7685126", TPL)
        self.assertIn("https://thirdsystem.ai/studies/v1-9/", refs)
        self.assertIn("https://osf.io/ec6wh/files/osfstorage/6af1fd459966c813ee53ba87", refs)
        for ssrn in ("6659000", "6761698", "6797679", "6799479", "6810758", "6816340", "6878818", "6963359",
                     "6817841"):
            self.assertIn(f"SSRN {ssrn}", refs)
        self.assertIn("Report No. 26-132", refs)
        body = TPL[:TPL.index("# References")]
        for letter in "abcdefghijkl":
            self.assertRegex(body, rf"2026[a-l, 0-9]*{letter}\b", f"reference 2026{letter} not cited")
        for cite in ("Sharp, 2010", "Sharp & Romaniuk, 2021", "Krippendorff, 2004"):
            self.assertIn(cite, body)

    def test_thresholds_in_the_text_are_the_scorers(self):
        for x in (S.ALPHA_CONFIRMED_MIN, S.ALPHA_FALSIFIED_BELOW, S.BRAND_AGREE_CONFIRMED_MIN,
                  S.BRAND_AGREE_FALSIFIED_BELOW, S.BAND_CONFIRMED_MAX, S.BAND_FALSIFIED_MIN, S.SELFCON_MIN_EXACT):
            self.assertIn(f"{x:.2f}".rstrip("0") if x != 0.667 else "0.667", TPL)
        self.assertEqual((S.N_FLOOR, S.MIN_UNITS_POOLED, S.MIN_GROUPS, S.MIN_UNITS_PER_GROUP), (6, 20, 3, 4))
        self.assertEqual((S.SELF_PREF_OK_MAX, S.SELF_PREF_MATERIAL_MIN, S.N_BOOT, S.N_PERM), (5.0, 10.0, 10_000, 10_000))
        self.assertEqual(S.NOISE_GUARDED, VV.NOISE_GUARDED)


class TestFixtures(unittest.TestCase):
    def test_base_is_the_scorers_dry_run(self):
        for k in MS.NAMES:
            p = MS.base_path(k)
            self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(), MS.BASE_SHA256[k])
            if k != "plan":                                  # the plan file carries no dry_run field
                self.assertTrue(json.loads(p.read_text(encoding="utf-8"))["dry_run"])

    def test_every_scenario_is_marked_and_consistent_with_the_scorer(self):
        for s in MS.SCENARIOS:
            src = load(s)
            self.assertTrue(VV.is_synthetic(src))
            for k, d in src.items():
                self.assertIn("SYNTHETIC", d["synthetic_fixture"], f"{s}/{k}")
            FP.check_consistency(src)

    def test_scenarios_keep_the_scorers_schema(self):
        base = {k: json.loads(MS.base_path(k).read_text(encoding="utf-8")) for k in MS.NAMES}
        for s in MS.SCENARIOS:
            src = load(s)
            for k in MS.NAMES:
                extra = keyset(src[k]) - keyset(base[k]) - {"synthetic_fixture", "ranking/reason",
                                                            "sensitivities/S_without_J1_provider_answers"}
                extra = {e for e in extra if not e.startswith("sensitivities/S_without_J1_provider_answers")}
                self.assertFalse(extra, f"{s}/{k}: keys the scorer does not write: {sorted(extra)[:5]}")
                missing = keyset(base[k]) - keyset(src[k])
                missing = {m for m in missing if "H5_" not in m and not m.startswith("ranking/")}
                self.assertFalse(missing, f"{s}/{k}: keys missing: {sorted(missing)[:5]}")

    def test_scenarios_cover_every_verdict(self):
        seen = {h: set() for h in ("H1", "H2", "H3", "H4", "H5", "H6", "H7", "H8", "H9")}
        for s in MS.SCENARIOS:
            for h, w in load(s)["verdicts"]["VERDICTS"].items():
                seen[h].add(w)
        for h, ws in seen.items():
            self.assertTrue({"CONFIRMED", "MARGINAL", "FALSIFIED", "UNDETERMINED"} <= ws, f"{h}: {ws}")
        self.assertTrue({"PENDING", "INACTIVE"} <= seen["H5"])
        overall = {FILLED[s][2]["CASE_OVERALL"] for s in MS.SCENARIOS}
        self.assertEqual(overall, EXPECTED_CASES["CASE_OVERALL"])


class TestFill(unittest.TestCase):
    def test_every_scenario_fills_without_template_residue(self):
        for s, (text, val, cases, flags) in FILLED.items():
            self.assertNotIn("{{", text, s)
            self.assertNotIn("{%", text, s)
            self.assertIn("SYNTHETIC TEST BUILD", text, s)

    def test_provenance_re_resolves(self):
        n = 0
        for s, (text, val, cases, flags) in FILLED.items():
            src = load(s)
            for name, p in val.prov.items():
                if p["kind"] == "json":
                    raw = VV.jget(src[p["source"]], p["path"])
                    self.assertEqual(VV.FORMATS[p["fmt"]](raw), p["formatted"], f"{s}:{name}")
                    n += 1
                elif p["kind"] == "derived":
                    raws = [VV.jget(src[a], b) for a, b in p["refs"]]
                    raw = VV.DERIVE[p["fn"]](*p["consts"], *raws)
                    self.assertEqual(VV.FORMATS[p["fmt"]](raw), p["formatted"], f"{s}:{name}")
                    n += 1
                elif p["kind"] == "table":
                    for c in p["cells"]:
                        self.assertEqual(VV.FORMATS[c["fmt"]](VV.jget(src[c["source"]], c["path"])), c["formatted"])
                        n += 1
        self.assertGreater(n, 1000)

    def test_every_number_in_results_is_fixed_text_or_a_recorded_value(self):
        fixed = set(VV.numeric_tokens(_PH_STRIP(TPL)))
        for s, (text, val, cases, flags) in FILLED.items():
            allowed = set(fixed)
            for p in val.prov.values():
                allowed |= set(VV.numeric_tokens(p.get("formatted") or ""))
                for c in p.get("cells", []):
                    allowed |= set(VV.numeric_tokens(c["formatted"]))
            res = section(text, "# 3. Results", "# 4. Discussion") + section(text, "# Abstract", "**Keywords")
            stray = [t for t in VV.numeric_tokens(res) if t not in allowed]
            self.assertFalse(stray, f"{s}: numbers neither fixed nor recorded: {stray[:10]}")
            for p in val.prov.values():                      # every recorded json number is the file's value
                if p["kind"] == "json" and isinstance(p["raw"], (int, float)):
                    self.assertEqual(VV.FORMATS[p["fmt"]](p["raw"]), p["formatted"])

    def test_every_test_appears_exactly_once_with_its_verdict(self):
        for s, (text, val, cases, flags) in FILLED.items():
            W = load(s)["verdicts"]["VERDICTS"]
            for h in VV.HYPS:
                tag = h.replace("_", "\\_")
                self.assertEqual(text.count(tag), 1, f"{s}: {h} appears {text.count(tag)} times")
                self.assertEqual(text.count(h), 0, f"{s}: {h} unescaped outside the verdict table")
                row = next(line for line in text.splitlines() if tag in line)
                self.assertIn(f"| {W[VV.SHORT[h]]} |", row, f"{s}: {h} row lacks its verdict")

    def test_verdict_words_in_text_match_the_file(self):
        for s, (text, val, cases, flags) in FILLED.items():
            text = section(text, "# 3. Results", "# 4. Discussion")
            W = load(s)["verdicts"]["VERDICTS"]
            for h in ("H1", "H2", "H3", "H4", "H6", "H7", "H8", "H9"):
                if W[h] in ("CONFIRMED", "MARGINAL", "FALSIFIED"):
                    self.assertRegex(text, rf"{h} is {W[h]}", f"{s}: {h}")
            for h in ("H1", "H2", "H3", "H4", "H5", "H6", "H7", "H8", "H9"):
                for w in ("CONFIRMED", "MARGINAL", "FALSIFIED"):
                    if w != W[h]:
                        self.assertNotRegex(text, rf"\b{h} is {w}\b", f"{s}: {h} said {w}, file {W[h]}")

    def test_every_case_and_flag_renders(self):
        text, val, cases, flags = FILLED["scored"]
        for var, vals in EXPECTED_CASES.items():
            for v in vals:
                FP.render(TPL, val.vals, {**cases, var: v}, flags)
        for f in flags:
            FP.render(TPL, val.vals, cases, {**flags, f: not flags[f]})

    def test_samsung_only_in_the_coi_paragraph(self):
        for s, (text, val, cases, flags) in FILLED.items():
            coi = section(text, "## Conflict of interest", "## Funding")
            self.assertEqual(text.count("Samsung"), coi.count("Samsung"), s)
            self.assertEqual(text.count(AI_USE), 1, s)


def _PH_STRIP(t):
    return re.sub(r"\{\{[^}]*\}\}|\{%[^%]*%\}", " ", t)


class TestRefusals(unittest.TestCase):
    def copy_scen(self, s="scored"):
        d = Path(tempfile.mkdtemp(prefix="v111_ref_", dir=TMP))
        for f in scen(s).iterdir():
            shutil.copy(f, d / f.name)
        return d

    def edit(self, d, key, fn, rehash=False):
        p = d / VV.NAMES[key]
        doc = json.loads(p.read_text(encoding="utf-8"))
        fn(doc)
        p.write_text(json.dumps(doc), encoding="utf-8")
        if rehash:
            v = d / VV.NAMES["verdicts"]
            vd = json.loads(v.read_text(encoding="utf-8"))
            vd["stage_j_sha256"] = hashlib.sha256((d / VV.NAMES["stage_j"]).read_bytes()).hexdigest()
            v.write_text(json.dumps(vd), encoding="utf-8")

    def test_real_mode_refuses_synthetic(self):
        with self.assertRaises(FP.FillError):
            FP.fill(scen("scored"), synthetic=False)

    def test_synthetic_mode_refuses_real_looking_files(self):
        d = self.copy_scen()

        def strip(doc):
            doc["dry_run"] = False
            doc.pop("synthetic_fixture", None)
        for k in ("frozen", "plan", "verdicts"):
            self.edit(d, k, strip)
        self.edit(d, "stage_j", strip, rehash=True)
        with self.assertRaises(FP.FillError):
            FP.fill(d, synthetic=True)

    def relabel(self):
        """A scenario relabelled as real (marks removed, hashes re-linked): only the real-mode checks differ."""
        d = self.copy_scen()

        def strip(doc):
            if "dry_run" in doc:
                doc["dry_run"] = False
            doc.pop("synthetic_fixture", None)
        self.edit(d, "plan", strip)
        plan_sha = hashlib.sha256((d / VV.NAMES["plan"]).read_bytes()).hexdigest()
        self.edit(d, "frozen", lambda doc: (strip(doc), doc.__setitem__("plan_sha256", plan_sha)))
        self.edit(d, "verdicts", strip)
        self.edit(d, "stage_j", strip, rehash=True)
        return d

    def test_real_mode_checks_pass_on_a_relabelled_fixture(self):
        d = self.relabel()
        text, val, cases, flags = FP.fill(d, synthetic=False)
        self.assertNotIn("SYNTHETIC", text)
        self.assertIn(VV.git_tag_commit()[:10], text)

    def test_real_mode_refuses_a_foreign_plan(self):
        d = self.relabel()
        self.edit(d, "plan", lambda doc: doc.__setitem__("fits", False))
        with self.assertRaises(FP.FillError):
            FP.fill(d, synthetic=False)

    def test_inconsistent_verdict_word_refused(self):
        d = self.copy_scen()
        self.edit(d, "verdicts", lambda doc: doc["VERDICTS"].__setitem__("H2", "FALSIFIED"))
        with self.assertRaises(FP.FillError):
            FP.fill(d, synthetic=True)

    def test_changed_statistic_refused(self):
        d = self.copy_scen()
        self.edit(d, "verdicts", lambda doc: doc["H4_Stability_Short"].__setitem__("rho", 0.1))
        with self.assertRaises(FP.FillError):
            FP.fill(d, synthetic=True)

    def test_stage_j_hash_mismatch_refused(self):
        d = self.copy_scen()
        self.edit(d, "stage_j", lambda doc: doc.__setitem__("created_utc", "x"))
        with self.assertRaises(FP.FillError):
            FP.fill(d, synthetic=True)

    def test_synthetic_output_inside_repo_refused(self):
        rc = FP.main(["--synthetic", "--outputs", str(scen("scored")), "--out", str(PAPER / "x_draft.md")])
        self.assertEqual(rc, 2)
        self.assertFalse((PAPER / "x_draft.md").exists())

    def test_charts_refuse_synthetic_without_watermark(self):
        r = subprocess.run([sys.executable, str(ROOT / "scripts/build_charts_v111.py"), "--outputs", str(scen("scored")),
                            "--out", str(TMP / "nofigs")], capture_output=True, text=True)
        self.assertEqual(r.returncode, 2)
        self.assertFalse((TMP / "nofigs").exists())

    def test_build_refuses_synthetic_without_watermark(self):
        r = subprocess.run([sys.executable, str(ROOT / "scripts/build_paper_v1_11.py"), "--source",
                            str(TMP / "scored" / "v1_11_paper_draft.md"), "--output", str(TMP / "x.pdf")],
                           capture_output=True, text=True)
        self.assertNotEqual(r.returncode, 0)
        self.assertFalse((TMP / "x.pdf").exists())

    def test_make_scenarios_refuses_osf(self):
        with self.assertRaises(SystemExit):
            MS.make(ROOT / "osf/methodology/v1_11/outputs/synthetic_test", ["scored"])
        self.assertFalse((ROOT / "osf/methodology/v1_11/outputs/synthetic_test").exists())


if __name__ == "__main__":
    unittest.main(verbosity=1)
