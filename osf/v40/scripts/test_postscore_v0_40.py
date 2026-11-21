#!/usr/bin/env python3
"""Tests for postscore_v0_40.py (DEVIATIONS Entry 2). Run: python3 osf/v40/scripts/test_postscore_v0_40.py
Reads the repo's frozen study files (read only); refusal tests run in a temporary directory."""
import csv
import json
import math
import shutil
import sys
import tempfile
import unittest
from collections import defaultdict
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import postscore_v0_40 as P  # noqa: E402
import score_v0_40 as S  # noqa: E402
import values_v0_40 as VV  # noqa: E402

ROOT = P.ROOT
DOC, MD = P.build(ROOT)
VER = json.loads((ROOT / P.REL["verdicts"]).read_text(encoding="utf-8"))
PRE = DOC["prereg"]
PT = PRE["per_test"]


def frame():
    with open(ROOT / P.REL["coded"], newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def mentions():
    with open(ROOT / P.REL["mentions"], newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


class Inputs(unittest.TestCase):
    def test_locked_scorer_is_the_locked_bytes(self):
        for name in ("score_v0_40.py", "stoprule_v0_40.py"):
            self.assertEqual(P.sha256(HERE / name), P.locked_sha("scripts/" + name))
        self.assertEqual(P.locked_sha("scripts/score_v0_40.py"),
                         "9fd69115ea5260ee960894c578ce7c2fac293e0e8100955a3ca279b8583365e3")

    def test_mentions_file_is_the_frozen_file(self):
        self.assertEqual(P.sha256(ROOT / P.REL["mentions"]), P.MENTIONS_SHA256)
        self.assertTrue(P.MENTIONS_SHA256.startswith("0a83b397"))

    def test_code_answer_is_restored(self):
        P.frozen_scorer(ROOT, perms=0)
        self.assertEqual(S.code_answer.__module__, "score_v0_40")
        self.assertEqual(S.code_answer.__name__, "code_answer")

    def test_closure_checks_passed(self):
        cc = DOC["_meta"]["closure_checks"]
        self.assertTrue(cc["mentions_file_byte_identical"])
        self.assertTrue(cc["primary_tests_and_S_D4_equal_verdict_file"])
        self.assertEqual(DOC["_meta"]["permutations"], S.PERMS)


class Refusal(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="v040_postscore_test_"))
        for rel in P.REL.values():
            (self.tmp / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / rel, self.tmp / rel)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_copy_builds_identically(self):
        doc, md = P.build(self.tmp, perms=0)
        self.assertEqual(doc["ceiling"], DOC["ceiling"])
        self.assertEqual(doc["prereg"], PRE)
        self.assertEqual(md, MD)

    def test_refuses_a_changed_mentions_file(self):
        p = self.tmp / P.REL["mentions"]
        p.write_bytes(p.read_bytes() + b"x")
        with self.assertRaises(P.Refused):
            P.build(self.tmp, perms=0)
        self.assertEqual(P.main([], root=self.tmp), 2)
        self.assertFalse((self.tmp / P.OUT_JSON).exists())

    def test_refuses_a_changed_raw_file(self):
        p = self.tmp / P.REL["raw"]
        p.write_bytes(p.read_bytes() + b"\n")
        with self.assertRaises(P.Refused):
            P.build(self.tmp, perms=0)

    def test_refuses_a_verdict_file_the_frozen_coding_does_not_reproduce(self):
        p = self.tmp / P.REL["verdicts"]
        v = json.loads(p.read_text(encoding="utf-8"))
        v["H_Amplify"]["airline"]["k"] += 1
        p.write_text(json.dumps(v), encoding="utf-8")
        with self.assertRaises(P.Refused):
            P.build(self.tmp)

    def test_writes_only_at_the_locked_permutation_count(self):
        self.assertEqual(P.main(["--perms", "10"], root=self.tmp), 2)
        self.assertFalse((self.tmp / P.OUT_JSON).exists())


class Ceiling(unittest.TestCase):
    def test_registered_values_equal_the_verdict_file(self):
        for cat in P.CATS:
            c, a = DOC["ceiling"][cat], VER["H_Amplify"][cat]
            for k in ("k", "n", "p0", "ratio", "leader"):
                self.assertEqual(c[k], a[k], (cat, k))

    def test_arithmetic(self):
        for cat in P.CATS:
            c = DOC["ceiling"][cat]
            self.assertTrue(math.isclose(c["ceiling_ratio"], (c["answers"] / c["n"]) / c["p0"], rel_tol=1e-12))
            self.assertTrue(math.isclose(c["ceiling_ratio"], 1 / (c["units_per_answer"] * c["p0"]), rel_tol=1e-12))
            self.assertTrue(math.isclose(c["ratio"], c["leader_answer_share"] * c["ceiling_ratio"], rel_tol=1e-12))
            self.assertLess(c["ceiling_ratio"], S.T["amplify_ratio"])
            self.assertFalse(c["ceiling_reaches_threshold"])
        self.assertLess(DOC["ceiling"]["bank"]["ceiling_ratio"], 1.0)
        self.assertFalse(DOC["ceiling"]["bank"]["ceiling_reaches_parity"])

    def test_answer_count_from_the_frame(self):
        fr = frame()
        for cat in P.CATS:
            n = sum(1 for r in fr if r["kind"] == "recommendation" and r["condition"] == "S0"
                    and r["category"] == cat and r["slot"] in S.TESTED_SLOTS)
            self.assertEqual(DOC["ceiling"][cat]["answers"], n)
            self.assertEqual(n, 16 * 9 * 3)

    def test_specs_equal_the_scored_sensitivities(self):
        sp, sens = DOC["ceiling"]["specs"], VER["sensitivity"]
        pairs = [("all_nine", c, VER["H_Amplify"][c]) for c in P.CATS]
        pairs += [("legacy", c, sens["S-Arm"]["legacy"]["H_Amplify"][c]) for c in P.CATS]
        pairs += [("current", c, sens["S-Arm"]["current"]["H_Amplify"][c]) for c in P.CATS]
        pairs += [("S-Ambig", c, sens["S-Ambig"]["H_Amplify"][c]) for c in P.CATS]
        pairs += [("S-Operating", "airline", sens["S-Operating"]["H_Amplify_airline"]),
                  ("S-SunCountry", "airline", sens["S-SunCountry"]["H_Amplify_airline"])]
        for name, cat, want in pairs:
            for k in ("k", "n", "p0", "ratio", "leader"):
                self.assertEqual(sp[name][cat][k], want[k], (name, cat, k))

    def test_per_model_ceilings_sit_in_the_ceiling_block_only(self):
        # the ceiling is the post-scoring check of DEVIATIONS Entry 2, never part of the pre-registered tables
        self.assertNotIn("ceiling_ratio", json.dumps(PRE))
        for sl in S.TESTED_SLOTS:
            for cat in P.CATS:
                c, a = DOC["ceiling"]["by_model"][sl][cat], PT["H_Amplify"]["by_model"][sl][cat]
                self.assertEqual((c["k"], c["n"], c["answers"]), (a["k"], a["n"], a["answers"]))
                self.assertTrue(math.isclose(c["ceiling_ratio"], (c["answers"] / c["n"]) / c["p0"], rel_tol=1e-12))

    def test_a_leader_in_every_answer_reaches_exactly_the_ceiling(self):
        # synthetic: 10 answers, each naming the leader and two others (n = 30), p0 = 0.25 -> (10/30)/0.25
        k, n, a, p0 = 10, 30, 10, 0.25
        self.assertTrue(math.isclose((k / n) / p0, (a / n) / p0))
        self.assertTrue(math.isclose((a / n) / p0, 1 / ((n / a) * p0)))


class PerTest(unittest.TestCase):
    def test_flag_tables_add_up_to_the_test(self):
        g, c = PT["H_Flag"]["by_ghost"].values(), PT["H_Flag"]["by_control"].values()
        self.assertEqual(sum(x["flagged"] for x in g), VER["H_Flag"]["ghost_flagged"])
        self.assertEqual(sum(x["answers"] for x in g), VER["H_Flag"]["ghost_answers"])
        self.assertEqual(sum(x["flagged"] for x in c), VER["H_Flag"]["control_flagged"])
        self.assertEqual(sum(x["answers"] for x in c), VER["H_Flag"]["control_answers"])
        m = PT["H_Flag"]["by_model"].values()
        self.assertEqual(sum(x["ghost_flagged"] for x in m), VER["H_Flag"]["ghost_flagged"])
        self.assertEqual(sum(x["control_answers"] for x in m), VER["H_Flag"]["control_answers"])

    def test_discover_without_it_equals_S_Discover(self):
        d = PT["H_Flag"]["by_control"]["DISCOVER"]
        sd = VER["sensitivity"]["S-Discover"]
        self.assertEqual(VER["H_Flag"]["control_flagged"] - d["flagged"], sd["control_flagged"])
        self.assertEqual(VER["H_Flag"]["control_answers"] - d["answers"], sd["control_answers"])
        self.assertEqual(PRE["discover_status"]["tested_S0"]["flagged"], d["flagged"])
        self.assertEqual(PRE["discover_status"]["tested_S0"]["answers"], d["answers"])

    def test_afterlife_and_decay_tables_add_up(self):
        for cat in P.CATS:
            bm = [PT["H_Afterlife"]["by_model"][sl][cat] for sl in S.TESTED_SLOTS]
            self.assertEqual(sum(x["pairs"] for x in bm), VER["H_Afterlife"][cat]["pairs"])
            self.assertEqual(sum(x["afterlife_pairs"] for x in bm), VER["H_Afterlife"][cat]["afterlife_pairs"])
            bg = [PT["H_Afterlife"]["by_ghost"][gid] for gid, g in PRE["d2_ghosts"].items() if g["category"] == cat]
            self.assertEqual(sum(x["pairs"] for x in bg), VER["H_Afterlife"][cat]["pairs"])
            self.assertEqual(sum(x["afterlife_pairs"] for x in bg), VER["H_Afterlife"][cat]["afterlife_pairs"])
        dm = PT["H_Decay"]["by_model"].values()
        self.assertEqual(sum(x["pairs"] for x in dm), VER["H_Decay"]["pairs"])
        self.assertEqual(sum(x["pairs_present"] for x in dm), VER["H_Decay"]["pairs_present"])
        dg = PT["H_Decay"]["by_ghost"].values()
        self.assertEqual(sum(x["pairs_present"] for x in dg), VER["H_Decay"]["pairs_present"])

    def test_search_tables_add_up(self):
        for axis in ("by_model", "by_ghost"):
            t = PT["H_Search"][axis].values()
            self.assertEqual(sum(x["paired_cells"] for x in t), VER["H_Search"]["paired_cells"])
            self.assertEqual(sum(x["s1_only_flagged"] for x in t), VER["H_Search"]["s1_only_flagged"])
            self.assertEqual(sum(x["s0_only_flagged"] for x in t), VER["H_Search"]["s0_only_flagged"])
            self.assertEqual(sum(x["post_cutoff_cells"] for x in t), VER["H_Search"]["post_cutoff_cells"])
            self.assertEqual(sum(x["post_cutoff_s1_flagged"] for x in t), VER["H_Search"]["post_cutoff_s1_flagged"])

    def test_per_model_arm_split_matches_S_Arm(self):
        for arm, slots in (("legacy", S.LEGACY_SLOTS), ("current", S.CURRENT_SLOTS)):
            want = VER["sensitivity"]["S-Arm"][arm]["H_Flag"]
            self.assertEqual(sum(PT["H_Flag"]["by_model"][sl]["ghost_flagged"] for sl in slots), want["ghost_flagged"])
            self.assertEqual(sum(PT["H_Flag"]["by_model"][sl]["control_flagged"] for sl in slots),
                             want["control_flagged"])


class Descriptives(unittest.TestCase):
    def test_slopes_with_D4_equal_the_verdict_file(self):
        for cat in P.CATS:
            self.assertEqual(PRE["d1_ai_share"][cat]["loglog_slope"]["all_nine_S0"], VER["H_Amplify"][cat]["loglog_slope"])
        self.assertIn("all_nine_S0_without_D4", PRE["d1_ai_share"]["bank"]["loglog_slope"])
        self.assertEqual(sorted(PRE["d1_ai_share"]["bank"]["D4_excluded"]),
                         sorted(VER["sensitivity"]["S-D4"]["excluded"]))

    def test_slope_without_D4_by_hand(self):
        # independent of the Scorer: shares from the mentions file and frame, D4 holders removed before normalising
        fr = {r["call_id"]: r for r in frame() if r["kind"] == "recommendation" and r["condition"] == "S0"
              and r["category"] == "bank" and r["slot"] in S.TESTED_SLOTS}
        units = {u["id"]: u for u in S.load_registry()[0] if u["category"] == "bank"}
        ex = set(VER["sensitivity"]["S-D4"]["excluded"])
        seen = defaultdict(set)
        for m in mentions():
            if m["call_id"] in fr and m["ambiguous"] == "False":
                # as the locked Scorer counts: only current-unit entities; a control counts toward a unit only when
                # their aliases overlap, which Discover and Capital One do not (to_unit["DISCOVER"] is None)
                eid = m["entity"]
                if eid in units and eid not in ex:
                    seen[m["call_id"]].add(eid)
        per_slot = defaultdict(lambda: defaultdict(int))
        for cid, us in seen.items():
            for u in us:
                per_slot[fr[cid]["slot"]][u] += 1
        keys = [u for u in units if u not in ex]
        shares = {u: sum(per_slot[sl][u] / sum(per_slot[sl].values()) for sl in S.TESTED_SLOTS) / 9 for u in keys}
        xs = [(math.log(units[u]["share"]), math.log(shares[u])) for u in keys if shares[u] > 0]
        mx, my = sum(a for a, _ in xs) / len(xs), sum(b for _, b in xs) / len(xs)
        slope = sum((a - mx) * (b - my) for a, b in xs) / sum((a - mx) ** 2 for a, _ in xs)
        self.assertTrue(math.isclose(slope, PRE["d1_ai_share"]["bank"]["loglog_slope"]["all_nine_S0_without_D4"],
                                     rel_tol=1e-9))

    def test_locked_mapping_of_controls_to_units(self):
        # DEVIATIONS Entry 2, "observed": the locked Scorer maps a control to a unit only through shared aliases;
        # Hawaiian goes to Alaska, Sun Country to itself, Discover to no unit (D12 is not applied by the scorer)
        sc = P.frozen_scorer(ROOT, perms=0)
        self.assertEqual(sc.to_unit.get("HA"), "AS")
        self.assertEqual(sc.to_unit.get("SY"), "SY")
        self.assertIsNone(sc.to_unit.get("DISCOVER"))

    def test_per_model_shares_sum_to_one(self):
        for cat in P.CATS:
            for cell, row in PRE["d1_ai_share"][cat]["by_model"].items():
                tot = sum(x["ai_share"] for u, x in row.items() if u != "answers")
                self.assertTrue(math.isclose(tot, 1.0, rel_tol=1e-9), (cat, cell))

    def test_ghost_presence_by_hand(self):
        fr = frame()
        named = defaultdict(set)
        for m in mentions():
            if m["kind"] == "ghost" and m["ambiguous"] == "False":
                named[m["entity"]].add(m["call_id"])
        for gid, g in PRE["d2_ghosts"].items():
            for cell, x in g["by_model"].items():
                sl, cond = cell.split("|")
                ids = [r["call_id"] for r in fr if r["kind"] == "recommendation" and r["condition"] == cond
                       and r["slot"] == sl and r["category"] == g["category"]]
                self.assertEqual(x["answers"], len(ids), (gid, cell))
                self.assertEqual(x["named_answers"], len(named[gid] & set(ids)), (gid, cell))

    def test_post_cutoff_pairs_shown_apart(self):
        post = {g: x["post_cutoff_pairs"] for g, x in PRE["d2_ghosts"].items() if x["post_cutoff_pairs"]}
        self.assertEqual(set(post), {"NK", "SVB", "FIRSTREPUBLIC"})
        self.assertEqual(sum(post.values()), 216 - 197)

    def test_discover_file_lists_every_discover_status_answer(self):
        n = sum(1 for r in frame() if r["tier"] == "S" and r["brand_id"] == "DISCOVER")
        self.assertEqual(MD.count("\n## "), n)
        s = PRE["discover_status"]
        self.assertEqual(s["tested_S0"]["answers"] + s["current_S1"]["answers"] + s["M5X_S0"]["answers"], n)


class Output(unittest.TestCase):
    def test_deterministic_and_committed(self):
        self.assertEqual(P.to_json(DOC), P.to_json(P.build(ROOT)[0]))
        self.assertEqual((ROOT / P.OUT_JSON).read_text(encoding="utf-8"), P.to_json(DOC))
        self.assertEqual((ROOT / P.OUT_DISCOVER).read_text(encoding="utf-8"), MD + "\n")

    def test_values_file_carries_every_value_with_its_label(self):
        vals = json.loads((ROOT / VV.OUT_JSON).read_text(encoding="utf-8"))["values"]
        n_pre = n_ceil = 0
        for k, e in vals.items():
            if k.startswith("prereg_post."):
                self.assertEqual(e["source"]["label"], P.LABEL_PREREG, k)
                n_pre += 1
            elif k.startswith("ceiling."):
                self.assertEqual(e["source"]["label"], P.LABEL_CEILING, k)
                n_ceil += 1
        have = {tuple(e["source"]["path"]) for e in vals.values() if e["source"].get("file") == P.OUT_JSON}
        for path, val in VV.walk({"ceiling": DOC["ceiling"], "prereg": PRE}):
            self.assertIn(tuple(path), have, path)
        self.assertGreater(n_pre, 1000)
        self.assertGreater(n_ceil, 50)
        self.assertEqual(LABEL_TEXT, P.LABEL_PREREG)


LABEL_TEXT = "pre-registered, computed after scoring because the locked scorer did not output them"

if __name__ == "__main__":
    unittest.main(verbosity=1)
