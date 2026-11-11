#!/usr/bin/env python3
"""Tests for paperB_lock_v1_11.py, the Paper B packet script and the forms mock. No network, no model call.
Run: PYTHONDONTWRITEBYTECODE=1 python3 -m unittest osf/methodology/v1_11/paperB/lock/test_paperB_lock_v1_11.py"""
import json, os, re, shutil, subprocess, sys, tempfile, unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paperB_lock_v1_11 as L

OUT = None


def setUpModule():
    global OUT
    OUT = L.rebuild_packets()


def tearDownModule():
    shutil.rmtree(OUT, ignore_errors=True)


class Guide(unittest.TestCase):
    def test_saved_pages_have_recorded_hashes(self):
        self.assertEqual(L.sha256(L.P["page1"]), "fc577e17cc7664dad1e6d85fe6c6b00e5e9762f62c56ae98d3cdd62dee4c1744")
        self.assertEqual(L.sha256(L.P["page2"]), "806cd6313650b33b99a3fd8e557ddb67c0dd27068852b42ea233e5e4fafa9d23")

    def test_guide_markdown_is_generated_from_pages(self):
        self.assertEqual(L.read(L.P["guide_md"]), L.guide_markdown() + "\n")

    def test_page2_equals_judge_rules_and_scale(self):
        d = L.diff_guide()
        self.assertTrue(d["identical"], d["differences"])
        self.assertEqual((d["judge_lines"], d["rules"], d["scale_lines"]), (14, 7, 5))

    def test_recorded_diff_file_is_current(self):
        self.assertEqual(json.load(open(L.P["diff"], encoding="utf-8")), L.diff_guide())

    def test_diff_detects_a_changed_word_a_missing_line_and_a_quote_style(self):
        g = L.guide_block()
        j = L.judge_block()
        g1 = list(g); g1[3] = g1[3].replace("Plain facts", "Simple facts")
        self.assertEqual([x["line"] for x in L.diff_guide(g1, j)["differences"]], [4])
        self.assertFalse(L.diff_guide(g[:-1], j)["identical"])
        g3 = list(g); g3[2] = g3[2].replace('"Top picks:"', "“Top picks:”")
        self.assertFalse(L.diff_guide(g3, j)["identical"])

    def test_judge_block_comes_from_the_locked_prompt(self):
        j = L.judge_block()
        self.assertEqual(j[0], "Rules:")
        self.assertTrue(j[-1].startswith("-2 = strongly unfavourable"))
        self.assertEqual(L.sha256(L.P["judge"]), "bcc079d38c677bd3eb616e6532e15b799c36d976431e3f4d09fc605979c1c284")


class Forms(unittest.TestCase):
    def test_questions_and_options_match_page1(self):
        f = L.check_forms()
        self.assertTrue(all(v["same"] for v in f.values()), f)
        self.assertEqual(len(f["titles"]["guide"]), 4)
        self.assertEqual(len(f["tone"]["guide"]), 6)

    def test_forms_check_detects_a_changed_option(self):
        code = L.read(L.P["code"]).replace("'Quoted sources'", "'Quoted sources (reviews)'")
        self.assertFalse(L.check_forms(code)["source"]["same"])

    def test_code_statement_equals_statement_file(self):
        self.assertEqual(L.code_statement(), L.statement_paragraphs())
        self.assertEqual(len(L.statement_paragraphs()), 7)

    def test_js_literal_round_trip(self):
        import ast
        for s in ["plain", "it's", 'say "hi"', "it's \"both\""]:
            self.assertEqual(ast.literal_eval(L.js_literal(s)), s)

    def test_sync_is_idempotent(self):
        before = {k: L.read(L.P[k]) for k in ("code", "prereg")}
        L.sync()
        after = {k: L.read(L.P[k]) for k in ("code", "prereg")}
        self.assertEqual(before, after)

    def test_mock_run_builds_forms_and_parses_labels(self):
        r = subprocess.run(["zsh", os.path.join(L.PB, "forms", "mock_run.sh"), OUT], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        o = r.stdout
        self.assertIn("LOG: All 19 forms built.", o)
        self.assertIn("map rows 5180", o)
        self.assertIn("DESC_HAS_STATEMENT true", o)
        self.assertIn('"equals_statement":true', o)
        q = json.loads(re.search(r"^QCHECK (.*)$", o, re.M).group(1))
        g = L.guide_page1()
        self.assertEqual([x["title"] for x in q], g["titles"])
        self.assertEqual([x["choices"] for x in q], [g["tone"], g["both"], g["source"], g["sure"]])
        tone = json.loads(re.search(r"^TONECHECK (.*)$", o, re.M).group(1))
        self.assertEqual([t[1] for t in tone], [2, 1, 0, -1, -2, ""])
        self.assertEqual([t[2] for t in tone], [True] * 5 + [False])
        n = int(re.search(r"label rows (\d+) expected (\d+)", o).group(1))
        self.assertEqual(n, int(re.search(r"label rows (\d+) expected (\d+)", o).group(2)))


class Statement(unittest.TestCase):
    def test_consistency_check_flags_disagreement(self):
        page1 = ["about 55 short AI answers", "ABOUT 45 MINUTES", "LABELS DUE", "Dec 4",
                 "withdraw your labels until December 18 by emailing x"]
        ok = ("**What you do.** You read about 55 short AI answers. It takes about 45 minutes, on your own time, "
              "by December 4.\n\n**Your choice.** You can withdraw your labels until December 18 by emailing me.")
        r = L.statement_vs_guide(ok, page1)
        self.assertTrue(all(v["same"] for v in r.values()), r)
        bad = ok.replace("December 18", "February 1")
        self.assertFalse(L.statement_vs_guide(bad, page1)["withdraw_until"]["same"])

    def test_prereg_statement_block_matches_file(self):
        pr = L.read(L.P["prereg"])
        self.assertIn("<!-- BEGIN STATEMENT -->\n" + L.prereg_statement_body() + "\n<!-- END STATEMENT -->", pr)
        self.assertIn("<!-- BEGIN GUIDE -->\n" + L.prereg_guide_body() + "\n<!-- END GUIDE -->", pr)


class Packets(unittest.TestCase):
    def test_variant_b_counts_and_coi(self):
        pk = L.check_packets(OUT)
        self.assertTrue(pk["byte_identical_to_recorded"])
        self.assertEqual((pk["units"], pk["labels"], pk["seed"], pk["variant"]), (518, 1036, 111023, "b"))
        self.assertEqual(pk["loads"], {"55": 10, "54": 9, "other": 0})
        self.assertTrue(pk["every_unit_two_distinct_students"])
        self.assertTrue(pk["no_student_sees_a_unit_twice"])
        self.assertEqual(pk["recognition_units"], 0)
        self.assertEqual(pk["coi_target_brand_hits"], [])
        self.assertEqual(pk["sample_sha256"], "94d120f4a752d72f4fe96f90523fb3be663b3feba92fc3ff0dcdd2a11da0295e")

    def test_rebuild_is_deterministic(self):
        d2 = L.rebuild_packets()
        try:
            a = json.load(open(os.path.join(OUT, "packet_design.json")))["outputs_sha256"]
            b = json.load(open(os.path.join(d2, "packet_design.json")))["outputs_sha256"]
            self.assertEqual(a, b)
        finally:
            shutil.rmtree(d2, ignore_errors=True)

    def test_packets_never_show_hidden_fields(self):
        import csv
        head = next(csv.reader(open(os.path.join(OUT, "packets", "packets_all.csv"), encoding="utf-8")))
        self.assertEqual(head, ["student_id", "position", "n_items", "item_id", "target_brand", "category",
                                "question", "text_type", "text"])


class Prereg(unittest.TestCase):
    def test_samsung_only_in_coi_and_ai_use_after_ethics(self):
        res = {r["check"]: r["ok"] for r in L.checks(packets=False)}
        self.assertTrue(res["Samsung named only in the COI section"])
        self.assertTrue(res["AI-use statement verbatim, after Ethics"])
        self.assertTrue(res["no open placeholder in the pre-registration"])

    def test_coi_wording_copied_from_v063(self):
        pr = L.read(L.P["prereg"])
        src = subprocess.run(["git", "-C", L.REPO, "show", "v0.63-prereg-r1:osf/v63/prereg/PRE_REGISTRATION_v0_63.md"],
                             capture_output=True, text=True, check=True).stdout.splitlines()
        v019 = src[183].split(" In this study Denon remains")[0]       # line 184: the v0.19 item, verbatim part
        v022 = src[185].split(" These are supply relationships")[0]  # line 186: the v0.22 item, verbatim part
        self.assertIn(v019, pr)
        self.assertIn(v022, pr)
        self.assertIn(src[189].split(". ")[-1], pr)                   # closing sentence (line 190)


class Manifest(unittest.TestCase):
    def test_manifest_round_trip_and_tamper(self):
        d = tempfile.mkdtemp()
        try:
            f = os.path.join(d, "a.txt")
            open(f, "w").write("x")
            m = os.path.join(d, "m.sha256")
            open(m, "w").write(f"{L.sha256(f)}  a.txt\n")
            self.assertEqual(L.verify_manifest(m, d), [])
            open(f, "w").write("y")
            self.assertEqual(L.verify_manifest(m, d), ["a.txt"])
        finally:
            shutil.rmtree(d)

    def test_locked_files_exist_and_tag_is_the_proposed_one(self):
        missing = [L.REL(p) for p in L.LOCKED if not os.path.exists(p)]
        self.assertEqual(missing, [])
        self.assertEqual(L.TAG, "v1.11-paperB-prereg-r1")

    def test_write_anchor_refuses_without_osf_note(self):
        with self.assertRaises(SystemExit):
            L.write_anchor("  ")


if __name__ == "__main__":
    unittest.main()
