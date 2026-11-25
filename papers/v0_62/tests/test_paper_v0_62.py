#!/usr/bin/env python3
"""Tests for the v0.62 paper (draft r1): numbers trace to files, conventions hold, claims in captions are true.

Run from the worktree root:  python3 papers/v0_62/tests/test_paper_v0_62.py -v
"""
import importlib.util
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
P = ROOT / "papers/v0_62"
TEMPLATE = (P / "v0_62_paper_template.md").read_text(encoding="utf-8")
DRAFT = (P / "v0_62_paper_draft.md").read_text(encoding="utf-8")
VALUES = json.loads((P / "v62_values.json").read_text(encoding="utf-8"))["values"]
LANGS = ["es", "ko", "zh"]
AI_USE = ("During the preparation of this work the author used AI tools (Anthropic's Claude) to assist with study "
          "design, analysis and writing. The author reviewed and edited all content and takes full responsibility for it.")


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def section(text, start, end):
    a = text.index(start)
    b = text.index(end, a + len(start))
    return text[a:b]


class TestValuesAndFill(unittest.TestCase):
    def test_values_file_is_current(self):
        """values_v0_62.py, re-run in memory, gives the same values as the committed file."""
        mod = load_module(P / "values_v0_62.py", "values_v0_62_test")
        mod.VALS.clear()
        V = mod.verdicts()
        mod.coi106(V)
        mod.ai_sens(V)
        mod.en_corrected(V)
        ai = mod.ai_check()
        tot = mod.collection()
        mod.logs(tot, ai)
        mod.gates()
        fresh = json.loads(json.dumps(mod.VALS, ensure_ascii=False))
        self.assertEqual(fresh, VALUES)

    def test_draft_is_the_filled_template(self):
        key = re.compile(r"\{\{v:([^}]+)\}\}")
        filled = key.sub(lambda m: VALUES[m.group(1).strip()]["display"], TEMPLATE)
        self.assertEqual(filled, DRAFT)
        self.assertNotIn("{{", DRAFT)

    def test_every_value_has_a_source(self):
        for k, v in VALUES.items():
            self.assertTrue(v["source"], k)

    def test_abstract_numbers_come_from_values(self):
        """Outside the {{v:...}} keys, the abstract may print only the design constants listed here."""
        ab = section(TEMPLATE, "# Abstract {-}", "**Keywords:**")
        bare = re.sub(r"\{\{v:[^}]+\}\}", " ", ab)
        nums = set(re.findall(r"\d+(?:\.\d+)?", bare))
        allowed = {"30", "88", "95", "100", "0", "6", "4", "5.2"}   # questions, yes/no items, CI %, cap, Entries 0--6, Claude Fable 5.2 / GPT-6 / Gemini 4
        self.assertTrue(nums <= allowed, nums - allowed)

    def test_locked_headline_figures(self):
        """The figures of the task brief, read from the files."""
        self.assertEqual(VALUES["P.es.rho"]["display"], "0.931")
        self.assertEqual(VALUES["P.es.ci"]["display"], "0.864–0.959")
        self.assertEqual(VALUES["P.ko.rho"]["display"], "0.867")
        self.assertEqual(VALUES["P.ko.ci"]["display"], "0.764–0.924")
        self.assertEqual(VALUES["P.zh.rho"]["display"], "0.812")
        self.assertEqual(VALUES["P.zh.ci"]["display"], "0.685–0.885")
        self.assertEqual(VALUES["joint"]["value"], "Language-robust")
        self.assertEqual([VALUES[f"Phi.{L}.rho"]["display"] for L in LANGS], ["0.623", "0.343", "0.330"])
        self.assertEqual([VALUES[f"Phi.{L}.verdict"]["value"] for L in LANGS], ["CONFIRMED", "MARGINAL", "MARGINAL"])
        self.assertEqual({VALUES[f"Rank.{L}.verdict"]["value"] for L in LANGS}, {"NOT TESTED"})
        self.assertEqual(VALUES["raw.ok"]["value"], 1602)
        self.assertEqual(VALUES["raw.per_lang"]["value"], 534)
        self.assertEqual(VALUES["raw.per_model"]["value"], 534)
        self.assertEqual(VALUES["cost.spend"]["display"], "$28.1294")
        self.assertEqual(VALUES["cost.worst_case"]["display"], "$0.16784")
        self.assertEqual(VALUES["cost.strict_total"]["display"], "$28.297192")
        self.assertEqual(VALUES["ENC.Phi.zh.rho4"]["display"], "0.3048")
        self.assertEqual(VALUES["ENC.Phi.zh.verdict"]["value"], "MARGINAL")
        self.assertEqual(VALUES["COI.n_as_run"]["value"], 107)
        self.assertEqual(VALUES["COI.n_106"]["value"], 106)
        self.assertEqual(VALUES["err.kind"]["value"], "ConnectTimeout")
        self.assertEqual(VALUES["err.call_id"]["value"], "ko|v19|B|phase_b__q6_iconic|gemini-4-argon|S0|1")


class TestCaptionClaims(unittest.TestCase):
    def test_every_presence_specification_confirmed_at_min_p(self):
        prefixes = [f"{s}.{L}" for L in LANGS for s in ("P", "S-Denon", "S-Headphones", "S-COI", "S-COI106", "ENC.P",
                                                         "ENC.S-COI106", "STrans.flagged.P", "STrans.strictly_flagged.P")]
        prefixes += ["SAliasAI.ko", "SAliasAI.zh"]
        for p in prefixes:
            self.assertEqual(VALUES[f"{p}.verdict"]["value"], "CONFIRMED", p)
            self.assertLess(VALUES[f"{p}.p"]["value"], 0.001, p)

    def test_s_trans_equals_locked_and_corrected_verdicts_same(self):
        for line in ("flagged", "strictly_flagged"):
            for L in LANGS:
                self.assertTrue(VALUES[f"STrans.{line}.{L}.equal_locked"]["value"])
                self.assertEqual(VALUES[f"STrans.{line}.{L}.removed"]["value"], 0)
        self.assertTrue(VALUES["ENC.all_verdicts_same"]["value"])
        self.assertEqual(VALUES["ENC.joint"]["value"], "Language-robust")

    def test_no_unnatural_items_and_no_strict_flags(self):
        for L in LANGS:
            self.assertEqual(VALUES[f"AIC.{L}.nat.unnatural"]["value"], 0)
            self.assertEqual(VALUES[f"AIC.{L}.strictly_flagged"]["value"], 0)
            self.assertEqual(VALUES[f"AIC.{L}.phase_b_flagged"]["value"], 0)

    def test_delta_intervals_exclude_zero(self):
        for L in LANGS:
            lo, hi = VALUES[f"P.{L}.dL_ci"]["value"]
            self.assertTrue(lo > 0 or hi < 0, L)

    def test_chinese_presence_interval_is_the_only_one_below_070(self):
        self.assertGreaterEqual(VALUES["P.es.ci"]["value"][0], 0.70)
        self.assertGreaterEqual(VALUES["P.ko.ci"]["value"][0], 0.70)
        self.assertLess(VALUES["P.zh.ci"]["value"][0], 0.70)
        self.assertGreater(VALUES["P.zh.ci"]["value"][0], 0.50)


class TestConventions(unittest.TestCase):
    def test_draft_banner(self):
        self.assertIn("DRAFT r1", section(DRAFT, "\\begin{titlepage}", "\\end{titlepage}"))
        self.assertIn("\\fancyhead[C]{\\footnotesize\\textbf{DRAFT r1}", DRAFT)

    def test_samsung_only_in_declarations_coi(self):
        coi = section(DRAFT, "## Conflict of interest {-}", "## Funding {-}")
        rest = DRAFT.replace(coi, "")
        for word in ("Samsung", "Cheil", "Iris", "Harman"):
            self.assertIn(word, coi)
            self.assertNotIn(word, rest, word)

    def test_denon_correction_and_v022_wording(self):
        coi = section(DRAFT, "## Conflict of interest {-}", "## Funding {-}")
        self.assertIn("has itself been owned by Harman International, a wholly owned subsidiary of Samsung Electronics, "
                      "since September 23, 2025", coi)
        self.assertIn("tier-2/3 component supply relationships", coi)
        self.assertIn("Samsung SDI (battery cells), and Samsung Display (infotainment)", coi)

    def test_ai_use_statement_verbatim(self):
        block = section(DRAFT, "## Use of AI tools {-}", "## Data and code availability {-}")
        self.assertEqual(block.split("\n\n")[1].strip(), AI_USE)

    def test_jel_label(self):
        self.assertIn("**JEL codes:** M31; L86, L15, D83, M37", DRAFT)

    def test_every_test_and_verdict_reported(self):
        table = section(DRAFT, "## 3.9 Summary of verdicts", "## 3.10")
        for h in ("H_Lang_Presence", "H_Lang_Phi", "H_Lang_Rank"):
            self.assertIn(h, table)
        for w in ("CONFIRMED", "MARGINAL", "NOT TESTED", "Language-robust"):
            self.assertIn(w, table)

    def test_deviations_section_cites_entries_0_to_6(self):
        dev = section(DRAFT, "# 4. Deviations", "# 5. Discussion")
        for e in range(7):
            self.assertRegex(dev, rf"\n\| {e} \|")

    def test_chart_titles_do_not_repeat_finding_headings(self):
        src = (ROOT / "scripts/build_charts_v62_paper.py").read_text(encoding="utf-8")
        titles = re.findall(r'header\(fig, "([^"]+)"', src)
        self.assertEqual(len(titles), 4)
        heads = [re.sub(r"\s*\(.*$", "", h.split(":", 1)[1]).strip().lower()
                 for h in re.findall(r"^## 3\.[3-7] (.+)$", TEMPLATE, re.M) if ":" in h]
        self.assertEqual(len(heads), 5)
        for t in titles:
            for h in heads:
                self.assertNotIn(h, t.lower())
                self.assertNotIn(t.lower(), h)

    def test_one_figure_per_finding_and_files_exist(self):
        figs = re.findall(r"\]\(\.\./\.\./(reports/figs/v62/paper/[^)]+\.pdf)\)", DRAFT)
        self.assertEqual(len(figs), 4)
        self.assertEqual(len(set(figs)), 4)
        for f in figs:
            self.assertTrue((ROOT / f).exists(), f)


if __name__ == "__main__":
    unittest.main()
