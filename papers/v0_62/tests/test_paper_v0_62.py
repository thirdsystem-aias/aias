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
        mod.build()
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
        allowed = {"30", "88", "95", "100", "0", "7", "8", "6", "4", "5.2"}   # questions, yes/no items, CI %, cap, Entries 0--8 and 7, Claude Fable 5.2 / GPT-6 / Gemini 4
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
    def test_r2_without_draft_banner_or_notes(self):
        self.assertIn("November 2026 (r2)", section(DRAFT, "\\begin{titlepage}", "\\end{titlepage}"))
        self.assertIn("**Paper status:** r2", DRAFT)
        self.assertNotIn("fancyhead[C]", DRAFT)
        for w in ("DRAFT", "this draft", "in r1", "not for circulation", "Open for this draft",
                  "four questions", "not yet reviewed"):
            self.assertNotIn(w, DRAFT, w)

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

    def test_deviations_section_cites_entries_0_to_8(self):
        dev = section(DRAFT, "# 4. Deviations", "# 5. Discussion")
        self.assertEqual(VALUES["dev.n_entries"]["value"], 9)
        for e in range(9):
            self.assertRegex(dev, rf"\n\| {e} \|")
        self.assertIn("DEVIATIONS Entries 0--8", dev)
        self.assertIn("holds 9 entries", dev)
        self.assertNotIn("not covered by an entry", dev)

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


MODELS = ["claude-fable-5-2", "gpt-6-astra", "gemini-4-argon"]
E7_SUMMARY = ROOT / "osf/v62/data/v62_planned_items_summary_v0_62.json"


class TestEntries7And8(unittest.TestCase):
    """r2: the DEVIATIONS Entry 7 items and the Entry 8 cost record, read from the files and printed in the paper."""

    @classmethod
    def setUpClass(cls):
        cls.S = json.loads(E7_SUMMARY.read_text(encoding="utf-8"))
        cls.meta = json.loads((P / "v62_values.json").read_text(encoding="utf-8"))["_meta"]

    def test_new_sources_in_provenance(self):
        ins = self.meta["inputs_sha256"]
        for f in ("v62_planned_items_summary_v0_62.json", "v62_planned_items_v0_62.json",
                  "v62_planned_category_labels_v0_62.csv", "v62_planned_top10_shift_v0_62.csv",
                  "v62_planned_checks_v0_62.csv"):
            self.assertIn(f"osf/v62/data/{f}", ins)
        self.assertIn("osf/v62/DEVIATIONS.md", ins)
        self.assertEqual(ins["osf/v62/data/v62_planned_items_summary_v0_62.json"],
                         "0b5429c025ea85c4a4508180850ea320d308590f926d4028d7ba87e08ec4a1dd")   # Entry 7
        self.assertEqual(ins["osf/v62/data/v62_planned_items_v0_62.json"],
                         "034f46c8ec6d9f17828b38684a417dcc60a2fc60f42342b85f34ecd08e5393c7")   # Entry 7

    def test_per_model_values_match_summary_both_readings(self):
        for L in LANGS:
            for m in MODELS:
                r = self.S["per_model_rho_c"][f"{L}|{m}"]
                self.assertEqual(VALUES[f"E7.pm.{L}.{m}.i"]["value"], r["i_same_model_english"])
                self.assertEqual(VALUES[f"E7.pm.{L}.{m}.ii"]["value"], r["ii_n3_english"])
                self.assertIn(VALUES[f"E7.pm.{L}.{m}.i"]["display"], DRAFT)
        # appendix claims: every cell >= 0.70; Claude Fable 5.2 highest in each language under both readings
        self.assertEqual(VALUES["E7.pm.n_below70"]["value"], 0)
        for L in LANGS:
            for rd in ("i", "ii"):
                vals = {m: VALUES[f"E7.pm.{L}.{m}.{rd}"]["value"] for m in MODELS}
                self.assertEqual(max(vals, key=vals.get), "claude-fable-5-2", (L, rd))
        app = section(DRAFT, "# Appendix A.", "## A.2")
        self.assertIn("Reading (i)", app)
        self.assertIn("Reading (ii)", app)

    def test_phi_pi_flag_not_raised(self):
        for L in LANGS:
            for k in ("phi_L_defined", "h_lang_phi_units"):
                self.assertFalse(self.S["phi_pi_flag"][L][k]["flag"])
        self.assertLess(VALUES["E7.phipi.max_abs"]["value"], 0.50)
        self.assertIn("The flag is not raised in any language", DRAFT)

    def test_category_labels_table(self):
        for k, d in self.S["category_labels"].items():
            L, c = k.split("|")
            self.assertEqual(VALUES[f"E7.cat.{L}.{c}.label"]["value"], d["label"])
            self.assertEqual(VALUES[f"E7.cat.{L}.{c}.rho"]["value"], d["rho_c"])
        self.assertEqual(VALUES["E7.cat.n.language-sensitive"]["value"], 0)
        self.assertEqual(VALUES["E7.cat.zh.v0.20.label"]["value"], "intermediate")   # named in the text
        self.assertEqual(VALUES["E7.cat.n.intermediate"]["value"], 1)
        tab = section(DRAFT, "## A.2", "## A.3")
        self.assertEqual(tab.count("language-stable |") + tab.count("level-shifted |") + tab.count("intermediate |"), 15)

    def test_language_pairs(self):
        for p, d in self.S["language_pairs"].items():
            self.assertEqual(VALUES[f"E7.pair.{p}.rho"]["value"], d["rho_c"])
            self.assertIn(VALUES[f"E7.pair.{p}.rho"]["display"], section(DRAFT, "## A.2", "## A.3"))

    def test_top10_and_erratum_units(self):
        self.assertEqual({VALUES["E7.top.es.1.name"]["value"], VALUES["E7.top.es.2.name"]["value"]},
                         {"L'Oréal Paris", "Paula's Choice"})
        self.assertEqual(VALUES["E7.top.ko.9.name"]["value"], "Paula's Choice")
        for i in (2, 5):   # "skincare brands that the English answers did not name at all"
            row = [r for r in self.S["top10_shift"]["zh"] if r[1] == VALUES[f"E7.top.zh.{i}.name"]["value"]][0]
            self.assertEqual(row[0], "v0.20")
            self.assertEqual(row[2], 0.0)
        a = section(DRAFT, "## A.2", "## A.3")
        self.assertIn("two units of t₄'s apostrophe erratum", a)
        self.assertIn("measured here against the locked English comparator", a)
        for L in LANGS:
            for i in range(1, 11):
                self.assertIn(VALUES[f"E7.top.{L}.{i}.name"]["display"], a)

    def test_manipulation_checks(self):
        mc = self.S["checks"]
        self.assertEqual(VALUES["E7.mc.served.mismatched"]["value"], mc["MC_Served"]["n_mismatched"])
        self.assertEqual(sorted(mc["MC_Language"]["flagged_all_answers"]),
                         [f"es|{m}|all" for m in sorted(MODELS)])
        self.assertEqual(mc["MC_Language"]["flagged_phase_B"], [])
        self.assertEqual(VALUES["E7.mc.lang.zh.claude-fable-5-2.B"]["display"], "0.9667")
        self.assertEqual(VALUES["E7.mc.lang.zh.claude-fable-5-2.B.flag"]["value"], False)
        for m in MODELS:
            self.assertTrue(VALUES[f"E7.mc.lang.es.{m}.all.flag"]["value"])
            for L in LANGS:
                self.assertGreaterEqual(VALUES[f"E7.mc.lang.{L}.{m}.B"]["value"], 0.95)
        self.assertEqual(VALUES["E7.mc.alias.matches"]["value"], VALUES["alias.matches"]["value"])
        self.assertEqual(VALUES["E7.mc.script.n"]["value"], 0)
        self.assertEqual(VALUES["E7.mc.trunc.n"]["value"], 0)
        a = section(DRAFT, "## A.3", "## A.4")
        self.assertIn('"Sí."', a)
        self.assertIn("flags every Spanish model", a)
        # the three off-language Chinese category answers: one question, runs 1-3 (text says so)
        I = json.loads((ROOT / "osf/v62/data/v62_planned_items_v0_62.json").read_text(encoding="utf-8"))
        off = I["7.5_sensitivities"]["S-Language_zh"]["excluded_calls"]
        self.assertEqual(sorted(int(x.split("|")[-1]) for x in off), [1, 2, 3])
        self.assertEqual({x.split("|")[4] for x in off}, {"claude-fable-5-2"})
        self.assertEqual({x.split("|")[1] for x in off}, {"v23"})

    def test_entry7_sensitivities_confirmed_and_in_table4(self):
        for k, d in self.S["sensitivities"].items():
            name, L = k.rsplit("_", 1)
            self.assertEqual(VALUES[f"E7.{name}.{L}.verdict"]["value"], "CONFIRMED")
            self.assertEqual(VALUES[f"E7.{name}.{L}.rho"]["value"], d["rho_c"])
            self.assertLess(VALUES[f"E7.{name}.{L}.p"]["value"], 0.001)
        t4 = section(DRAFT, "| Specification | n |", "![Rank agreement of recall Presence with English under each")
        for s in ("S-Language, Entry 7", "S-Script, Entry 7", "S-Alias, Entry 7"):
            self.assertIn(s, t4)
        src = (ROOT / "scripts/build_charts_v62_paper.py").read_text(encoding="utf-8")
        for s in ("E7.S-Language.{L}", "E7.S-Script.{L}", "E7.S-Alias.{L}"):
            self.assertIn(s, src)

    def test_descriptives(self):
        for L in LANGS:
            for m in MODELS:
                self.assertEqual(VALUES[f"E7.rec.{L}.{m}"]["value"], self.S["recognition"][L][m]["recognized"])
                self.assertEqual(VALUES[f"E7.rel.{L}.{m}.rel1"]["value"], self.S["rel1_rel3"][f"{L}|{m}"]["rel1"])
                self.assertEqual(VALUES[f"E7.cost.{L}.{m}"]["value"], self.S["cost"][f"{L}|{m}"]["usd"])
        self.assertTrue(VALUES["E7.lf.pooled_below_plan"]["value"])
        above = sorted((L, m, ph) for L in LANGS for m in MODELS for ph in ("A", "B")
                       if VALUES[f"E7.lf.{L}.{m}.{ph}"]["value"] > VALUES[f"E7.lf.{L}.plan"]["value"])
        self.assertEqual(above, [("es", "gemini-4-argon", "A"), ("es", "gpt-6-astra", "B")])   # named in A.4
        self.assertEqual([VALUES[f"E7.lf.{L}.plan"]["value"] for L in LANGS], [1.25, 1.75, 1.5])
        self.assertEqual(VALUES["E7.home.status"]["value"], "not computed")
        self.assertEqual(VALUES["E7.time.status"]["value"], "not available")
        self.assertIn("Home-language descriptive (pre-registration §2.9 item 5): not computed", DRAFT)
        self.assertIn("Benchmark for time (pre-registration §2.7): not available", DRAFT)
        self.assertAlmostEqual(VALUES["E7.cost.total"]["value"], VALUES["raw.cost_sum"]["value"], places=6)

    def test_entry7_labelled_as_post_scoring(self):
        app = section(DRAFT, "# Appendix A.", "## A.1")
        self.assertIn("after the one scoring run", app)
        self.assertIn("No item here changes a verdict", app)
        s310 = section(DRAFT, "## 3.10", "# 4. Deviations")
        self.assertIn("DEVIATIONS Entry 7", s310)
        self.assertIn("none bears on a verdict", s310)

    def test_entry8_cost_note(self):
        self.assertEqual(VALUES["err.cost"]["display"], "$0")
        self.assertEqual(VALUES["cost.worst_case"]["display"], "$0.16784")
        self.assertEqual(VALUES["cost.strict_total"]["display"], "$28.297192")
        self.assertEqual(VALUES["raw.cost_sum6"]["display"], "$28.129352")
        self.assertEqual(VALUES["log.rerun_start_s"]["value"], "08:38:44")
        self.assertEqual(VALUES["log.rerun_end_s"]["value"], "08:39:04")
        self.assertEqual(VALUES["budget.rerun_note_given"]["value"], "7:15 am")
        self.assertEqual(VALUES["cost.astra_wc"]["display"], "$0.8392")
        note = section(DRAFT, "**Cost note (DEVIATIONS Entry 8).**", "## 3.2")
        for s in ("$0.16784", "$28.297192", "$28.129352", "would not have paused without the approval",
                  "projection approval", "7:15 am"):
            self.assertIn(s, note)
        self.assertIn("08:38:44 to 08:39:04 US Central", DRAFT)

    def test_jack_reference(self):
        refs = section(DRAFT, "# References {-}", "# Appendix A.")
        self.assertIn("Jack, W., Lehman, N., Maloney, K., & Xu, S. (2026). *Persona Conditioning of Brand "
                      "Recommendations in Retrieval-Augmented Commercial Chat: A Prominence-Stratified Cross-Provider "
                      "Audit*. arXiv 2605.30207 (v1, 28 May 2026; cs.AI).", refs)
        self.assertIn("(Jack et al., 2026)", section(DRAFT, "# 6. Limitations", "# 7."))

    def test_data_availability_cites_entry_7_8_commit(self):
        da = section(DRAFT, "## Data and code availability {-}", "# References {-}")
        self.assertIn("`69e1aa9`", da)
        self.assertIn("branch `v0.62-nohand`", da)
        for f in ("v62_planned_items_v0_62.json", "v62_planned_items_summary_v0_62.json",
                  "v62_planned_category_labels_v0_62.csv", "v62_planned_top10_shift_v0_62.csv",
                  "v62_planned_checks_v0_62.csv"):
            self.assertIn(f, da)


class TestReviewFixes(unittest.TestCase):
    """Fixes from the review record reviews/v0.62-paper/2026-11-25.md (F1-F9, N1-N5)."""

    def test_f1_zh_phase_a_flag_in_main_text(self):
        self.assertEqual(VALUES["E7.mc.lang.zh.claude-fable-5-2.A"]["display"], "0.9432")
        self.assertTrue(VALUES["E7.mc.lang.zh.claude-fable-5-2.A.flag"]["value"])
        self.assertIn("flagged (Spanish, all answers; Chinese Claude Fable 5.2, yes/no answers 0.9432); no code changed",
                      DRAFT)
        self.assertIn("also flags Chinese Claude Fable 5.2 (0.9432)", section(DRAFT, "## 3.10", "# 4. Deviations"))

    def test_f2_figure4_subtitle(self):
        src = (ROOT / "scripts/build_charts_v62_paper.py").read_text(encoding="utf-8")
        self.assertIn("Every specification gives \"\n           \"the primary verdict in every language", src)
        self.assertNotIn("is \"\n           \"CONFIRMED in every language", src)
        self.assertNotIn("every specification is", src)

    def test_f3_f4_f9_wording(self):
        self.assertIn("Every result in this paper is read from", DRAFT)
        self.assertIn("design constants (budget, alias counts, seeds, manifest size) are quoted from the locked "
                      "pre-registration", DRAFT)
        self.assertIn("the forms that could be listed before the lock", DRAFT)
        self.assertNotIn("runner could list", DRAFT)
        self.assertIn("(the forward translator is of the same provider; limitation 2)", DRAFT)
        lim2 = section(DRAFT, "\n2. The forward translator", "\n3. ")
        self.assertIn("same provider as one of the measured models", lim2)

    def test_f5_phi_wording_and_intervals(self):
        s35 = section(DRAFT, "## 3.5 H_Lang_Phi", "| | Spanish |")
        self.assertNotIn("(MARGINAL)", s35)
        self.assertIn("both intervals reach below 0.30 and above 0.50", s35)
        for L in ("ko", "zh"):
            lo, hi = VALUES[f"Phi.{L}.ci"]["value"]
            self.assertLess(lo, 0.30)
            self.assertGreater(hi, 0.50)
            self.assertLess(VALUES[f"Phi.{L}.p"]["value"], 0.05)
            self.assertTrue(0.30 < VALUES[f"Phi.{L}.rho"]["value"] < 0.50)

    def test_f6_prereg_section_references_prefixed(self):
        for s in ("re-run pass of pre-registration §5.3", "(primary, pre-registration §2.2)",
                  "(secondary, pre-registration §2.3)", "(secondary, conditional, pre-registration §2.4)",
                  "Joint reading (pre-registration §2.6)", "Sensitivities (pre-registration §7.5;",
                  "four gates had to pass (pre-registration §7.3)", "Under pre-registration §2.8"):
            self.assertIn(s, DRAFT)
        for bad in ("pass of §5.3", "(primary, §2.2)", "Joint reading (§2.6)", "of §7.5", "Under §2.8"):
            self.assertNotIn(bad, DRAFT)

    def test_f7_f8_references_and_keyword(self):
        refs = section(DRAFT, "# References {-}", "# Appendix A.")
        self.assertIn("Rienecker, J., Mpofu, K., Goel, N., Datta, S., Zhao, J., Danielsson, O., & Thorsen, F. (2026).",
                      refs)
        self.assertIn("arXiv 2603.18300 (v1, 18 March 2026; cs.HC)", refs)
        self.assertIn("Qi, J., Fernández, R., & Bisazza, A. (2023).", refs)
        self.assertIn("Steenkamp, J.-B. E. M., & Baumgartner, H. (1998).", refs)
        self.assertIn("Brislin, R. W. (1970).", refs)
        body = DRAFT.split("# References {-}")[0]
        for c in ("(Qi, Fernández & Bisazza, 2023)", "(Steenkamp & Baumgartner, 1998)", "(Brislin, 1970)"):
            self.assertIn(c, body)
        self.assertIn("cross-language rank agreement", DRAFT)
        self.assertNotIn("measurement invariance\n", DRAFT)
        self.assertNotIn("; measurement invariance", DRAFT)

    def test_n1_n2_n3_n5(self):
        self.assertIn("p was 0.0001 in each (1/10,001, the smallest value 10,000 draws allow)", DRAFT)
        self.assertIn("88 Korean and 44 Chinese rows", DRAFT)
        refs = section(DRAFT, "# References {-}", "# Appendix A.")
        letters = re.findall(r"González Castro, P\. U\. \(2026([a-z])\)", refs)
        self.assertEqual(letters, [chr(ord("a") + i) for i in range(len(letters))])
        body = DRAFT.split("# References {-}")[0].split("\n---\n", 1)[1]
        self.assertNotIn(" --- ", body)
        self.assertNotIn("—", body)


if __name__ == "__main__":
    unittest.main()
