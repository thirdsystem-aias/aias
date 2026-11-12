"""
Tests of the exploratory v1.18 section (§3.8) of Grounding Paper A. v1.13's parts: SYNTHETIC fixtures only; v1.18's
parts: the recorded copies in papers/v1_13/inputs/v1_18/ (real v1.18 outputs, SHA-256 checked). Nothing is written
inside the repository.

    cd <worktree> && PYTHONDONTWRITEBYTECODE=1 python3 papers/v1_13/tests/test_v118_section.py
"""
import hashlib
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAPER = HERE.parent
ROOT = PAPER.parents[1]
sys.path.insert(0, str(PAPER))
sys.path.insert(0, str(ROOT / "scripts"))
import fill_paper_v1_13 as F  # noqa: E402
import v113_values as VV  # noqa: E402
import v118_section as V118  # noqa: E402

FX = HERE / "fixtures"
SCORED = (FX / "SYNTHETIC_scored_v1_13_verdicts.json", FX / "SYNTHETIC_scored_v1_13_sdri.csv")
TPL = (PAPER / "v1_13_paper_template.md").read_text(encoding="utf-8")


def section(text):
    a = text.index("## 3.8 Exploratory")
    return text[a:text.index("# 4. Discussion", a)]


def tmp_inputs(d, edit=None):
    """Copy the recorded inputs to d; edit(results) changes the results and the record is rewritten to match."""
    for p in V118.INPUT_DIR.iterdir():
        shutil.copy(p, d / p.name)
    if edit:
        R = json.loads((d / "v1_18_results.json").read_text(encoding="utf-8"))
        edit(R)
        data = json.dumps(R).encode()
        (d / "v1_18_results.json").write_bytes(data)
        rec = json.loads((d / V118.RECORD).read_text(encoding="utf-8"))
        rec["files"]["v1_18_results.json"]["sha256"] = hashlib.sha256(data).hexdigest()
        (d / V118.RECORD).write_text(json.dumps(rec), encoding="utf-8")
        D = json.loads((d / "descriptive_v1_18.json").read_text(encoding="utf-8"))
        D["inputs"]["v1_18_results"] = rec["files"]["v1_18_results.json"]["sha256"]
        data = json.dumps(D).encode()
        (d / "descriptive_v1_18.json").write_bytes(data)
        rec["files"]["descriptive_v1_18.json"]["sha256"] = hashlib.sha256(data).hexdigest()
        (d / V118.RECORD).write_text(json.dumps(rec), encoding="utf-8")
    return d


class TestV118Section(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text, cls.val, cls.cases, cls.flags = F.fill(SCORED[0], SCORED[1], None, "/tmp/figs", synthetic=True)

    def test_recorded_copies_match_their_sha256(self):
        rec = json.loads((V118.INPUT_DIR / V118.RECORD).read_text(encoding="utf-8"))
        for name in V118.FILES.values():
            self.assertEqual(V118.sha256(V118.INPUT_DIR / name), rec["files"][name]["sha256"])
        self.assertEqual(rec["branch"], "v1.18")

    def test_changed_copy_refused(self):
        with tempfile.TemporaryDirectory() as d:
            d = tmp_inputs(Path(d))
            with open(d / "v1_18_results.json", "a", encoding="utf-8") as f:
                f.write(" ")
            with self.assertRaises(V118.InputError):
                V118.load(d)

    def test_descriptive_from_another_results_file_refused(self):
        with tempfile.TemporaryDirectory() as d:
            d = tmp_inputs(Path(d))
            D = json.loads((d / "descriptive_v1_18.json").read_text(encoding="utf-8"))
            D["inputs"]["v1_18_results"] = "0" * 64
            data = json.dumps(D).encode()
            (d / "descriptive_v1_18.json").write_bytes(data)
            rec = json.loads((d / V118.RECORD).read_text(encoding="utf-8"))
            rec["files"]["descriptive_v1_18.json"]["sha256"] = hashlib.sha256(data).hexdigest()
            (d / V118.RECORD).write_text(json.dumps(rec), encoding="utf-8")
            with self.assertRaises(V118.InputError):
                V118.load(d)

    def test_every_number_of_the_section_comes_from_the_two_files(self):
        sec = section(self.text)
        allowed = set(VV.numeric_tokens(section(TPL)))
        n = 0
        for name, p in self.val.prov.items():
            if not name.startswith(("V118_", "TABLE_V118_")):
                continue
            allowed |= set(VV.numeric_tokens(p["formatted"]))
            srcs = {p.get("source")} if p["kind"] == "json" else (
                {s for s, _ in p.get("refs", [])} if p["kind"] == "derived" else
                {c["source"] for c in p.get("cells", [])} if p["kind"] == "table" else set())
            self.assertTrue(srcs <= {"v118", "v118d"}, name)
            if p["kind"] == "json":
                self.assertEqual(VV.FORMATS[p["fmt"]](VV.jget(self.val.src[p["source"]], p["path"])), p["formatted"])
                n += 1
            elif p["kind"] == "table":
                for c in p["cells"]:
                    self.assertEqual(VV.FORMATS[c["fmt"]](VV.jget(self.val.src[c["source"]], c["path"])),
                                     c["formatted"])
                    n += 1
        self.assertEqual(set(VV.numeric_tokens(sec)) - allowed, set())
        self.assertGreater(n, 60)
        self.assertNotIn("{{", sec)

    def test_headline_values_and_flag(self):
        R, D = self.val.src["v118"], self.val.src["v118d"]
        for d, s, _ in V118.DEFS:
            self.assertEqual(self.val.vals[f"V118_{s}"], VV.r2(R["primary"]["program"]["pair_weighted"][d]))
        self.assertEqual(self.val.vals["V118_UNRES_CIT"],
                         VV.f1(R["sensitivities"]["S1_unresolved_out"]["program"]["mix_pair_weighted"]["UNRESOLVED"]))
        for b in D["bootstrap_draws"]["flagged"]:
            nm = self.val.src["registry"][b.replace(":", "|", 1)]["brand"]
            self.assertIn(nm, self.val.vals["V118_FLAG_SENTENCE"])
        sec = section(self.text)
        for word in ("exploratory", "gates nothing", "two AI coders", "S7"):
            self.assertIn(word, sec)
        self.assertNotRegex(sec, r"Samsung|Harman|Cheil")

    def test_v118_changes_nothing_of_v113(self):
        def edit(R):
            for d in R["primary"]["program"]["pair_weighted"]:
                R["primary"]["program"]["pair_weighted"][d] = 50.0
        with tempfile.TemporaryDirectory() as d:
            d = tmp_inputs(Path(d), edit)
            old = V118.INPUT_DIR
            V118.INPUT_DIR = d
            try:
                text, val, cases, flags = F.fill(SCORED[0], SCORED[1], None, "/tmp/figs", synthetic=True)
            finally:
                V118.INPUT_DIR = old
        self.assertEqual((cases, flags), (self.cases, self.flags))
        for k, v in self.val.vals.items():
            if not k.startswith(("V118_", "TABLE_V118_")):
                self.assertEqual(val.vals[k], v, k)
        self.assertEqual(self.text.replace(section(self.text), ""), text.replace(section(text), ""))
        self.assertEqual(val.vals["V118_K"], "50.00")

    def test_distinct_sentence_follows_interval_overlap(self):
        R = {"primary_ci": {"program_pair_weighted": {"K_own_domain": [0, 1], "P_any_company": [5, 10],
                                                       "Y_own_plus_listings": [8, 12], "M_not_owned": [98, 99]}}}
        s = V118.distinct_sentence(R)
        self.assertIn("differs between K and P, K and Y, K and M, P and M and Y and M", s)
        self.assertIn("P and Y are not distinguishable", s)

    def test_chart_09_point_and_whisker(self):
        import build_charts_v113 as BC
        R = V118.load()["v118"]
        self.assertNotIn("Exploratory", BC.TITLES[9])
        self.assertIn("90% intervals", BC.TITLES[9])
        with tempfile.TemporaryDirectory() as d:
            BC.chart_09(R, Path(d))
            self.assertTrue((Path(d) / "chart_09_v118_definitions.pdf").stat().st_size > 1000)
        self.assertIn("ax.errorbar", Path(BC.__file__).read_text(encoding="utf-8").split("def chart_09")[1]
                      .split("def main")[0])
        self.assertNotIn("ax.bar", Path(BC.__file__).read_text(encoding="utf-8").split("def chart_09")[1]
                         .split("def main")[0])


if __name__ == "__main__":
    unittest.main()
