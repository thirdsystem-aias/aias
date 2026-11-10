#!/usr/bin/env python3
"""Tests for score_v1_11.py on synthetic data only (no archive answer is read, no model call).
Run from the repo root:  python3 -m unittest scripts/test_score_v1_11.py scripts/test_judge_v1_11.py"""
import json
import math
import os
import random
import re
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import score_v1_11 as S  # noqa: E402

V = S.V
PROMPT_MD = os.path.join(HERE, "..", "osf", "methodology", "v1_11", "prereg", "judge_prompt_v1_11.md")


def ok(v=0, ev=False, mixed=False, ref=True, evidence=""):
    return json.dumps({"refers_to_brand": ref, "evaluative": ev, "mixed": mixed, "valence": v, "evidence": evidence})


def draft_segments(text):
    """The draft r0 segmenter, verbatim, to show that the span-based version keeps its segments."""
    out = []
    for line in S._LINE_SPLIT.split(text.replace("\r\n", "\n")):
        for item in S._INLINE_MARK.split(line.strip()):
            out.extend(p.strip() for p in S._SENT_SPLIT.split(item.strip()) if p.strip())
    return out


class TestWindow(unittest.TestCase):
    ANSWER = ("For small teams, these are the top picks:\n\n### Best overall: **ClickUp**\n"
              "- Very flexible\n- Can feel overwhelming at first\n\n### Simplest: **Trello**\n"
              "- Easy to learn\n- Limited for complex projects\n\nOverall, Trello and ClickUp both work.")

    def test_brand_block_takes_sub_bullets_and_stops_at_next_brand(self):
        w = S.build_window(self.ANSWER, ["ClickUp"], ["Trello"])
        self.assertIn("Very flexible", w)
        self.assertIn("overwhelming", w)
        self.assertNotIn("Easy to learn", w)
        self.assertIn("Overall, Trello and ClickUp both work.", w)
        self.assertIn("[...]", w)

    def test_flattened_newlines(self):
        flat = self.ANSWER.replace("\n", "  ")
        self.assertEqual(S.build_window(flat, ["ClickUp"], ["Trello"]), S.build_window(self.ANSWER, ["ClickUp"], ["Trello"]))

    def test_miss_returns_none_and_word_boundary(self):
        self.assertIsNone(S.build_window("Asana is fine.", ["Notion"]))
        self.assertIsNone(S.build_window("Notional limits apply.", ["Notion"]))

    def test_accent_folding_and_case(self):
        self.assertIsNotNone(S.build_window("I like WUSTHOF knives.", ["Wüsthof"]))

    def test_alias_cut_by_the_sentence_splitter_is_located(self):
        for text, alias in (("Try e.l.f. Cosmetics. It is cheap and good.", "e.l.f. Cosmetics"),
                            ("St. George Spirits makes a fine gin. Others exist.", "St. George Spirits"),
                            ("1. Zwilling J.A. Henckels - durable blades.", "Zwilling J.A. Henckels")):
            w = S.build_window(text, [alias])
            self.assertIsNotNone(w, alias)
            self.assertIn(alias.split()[-1], w)

    def test_segments_identical_to_draft_and_spans_exact(self):
        rng = random.Random(5)
        texts = [self.ANSWER, self.ANSWER.replace("\n", "  "), "A. B.  C\r\n- d 1. e  ## f: g? H! i",
                 "Plain sentence. Another one! Third? 4) item - bullet * star"]
        for _ in range(30):
            texts.append("".join(rng.choice(["Ab", " ", "  ", "\n", ". ", "- ", "1. ", "## ", "X", ": "]) for _ in range(60)))
        for t in texts:
            sp = S.segment_spans(t)
            self.assertEqual([s for s, _, _ in sp], draft_segments(t))
            tn = t.replace("\r\n", "\n")
            for s, a, b in sp:
                self.assertEqual(tn[a:b], s)

    def test_cap(self):
        long = "Brandx is good. " + " ".join(["Brandx again has a long sentence here."] * 100)
        w = S.build_window(long, ["Brandx"], cap=200)
        self.assertLessEqual(len(w), 200 + len(" [...]") + len("[...] "))
        self.assertTrue(w.endswith("[...]"))

    def test_recognition_cap(self):
        t, cut = S.recognition_text("a" * 20, cap=10)
        self.assertTrue(cut)
        self.assertEqual(S.recognition_text("short")[1], False)

    def test_bare(self):
        pat = S.alias_pattern(["Acme"])
        self.assertTrue(S.is_bare("[...] - Acme [...]", pat))
        self.assertFalse(S.is_bare("Acme makes very durable and well priced tools.", pat))


class TestCapAndSamples(unittest.TestCase):
    def units(self, n=120, models=6, s="E1", block="E"):
        return [{"unit_id": f"u{i:04d}", "set": s, "wave": "single", "brand": f"B{i % 3}", "model": f"m{i % models}",
                 "block": block, "category": "c", "frame": f"p{i % 6}", "answer_id": f"a{i // 2}"} for i in range(n)]

    def test_cap_is_seeded_and_model_balanced(self):
        units = [{**u, "brand": "B"} for u in self.units()]
        a, b = S.cap_windows(units, k=36), S.cap_windows(units, k=36)
        self.assertEqual([u["unit_id"] for u in a], [u["unit_id"] for u in b])
        self.assertEqual(len(a), 36)
        per_model = {m: sum(u["model"] == m for u in a) for m in {u["model"] for u in a}}
        self.assertEqual(set(per_model.values()), {6})

    def test_cap_noop_below_k(self):
        units = [{**u, "brand": "B"} for u in self.units(10)]
        self.assertEqual(len(S.cap_windows(units, k=36)), 10)

    def test_stratified_samples(self):
        units = self.units(400)
        j2 = S.j2_sample(units)
        self.assertEqual(j2, S.j2_sample(units))
        per = {m: sum(1 for u in units if u["unit_id"] in set(j2) and u["model"] == m) for m in {u["model"] for u in units}}
        for m, k in per.items():
            n = sum(u["model"] == m for u in units)
            self.assertEqual(k, S._k_of(0.10, n))
        other = [{**u, "unit_id": "f" + u["unit_id"]} for u in self.units(100, block="F", s="F1")]
        sc = S.selfcon_sample(units + other)
        self.assertEqual(len(sc), S._k_of(0.05, 400) + S._k_of(0.05, 100))
        self.assertEqual(sc, S.selfcon_sample(units + other))

    def test_human_sample_constraints(self):
        rng = random.Random(1)
        units = []
        models = [f"m{i}" for i in range(6)]
        for cat, blk, waves in (("v0.20", "F", ["t1", "t2", "t3"]), ("pm", "E", ["v0.9"])):
            for i in range(600):
                units.append({"unit_id": f"{cat}-{i:04d}", "block": blk, "category": cat, "wave": rng.choice(waves),
                              "model": rng.choice(models), "frame": f"f{rng.randint(1, 6)}", "brand": f"b{rng.randint(1, 24)}"})
        for b in range(24):
            for w in ("t1", "t2", "t3"):
                for m in models:
                    units.append({"unit_id": f"R-{b}-{w}-{m}", "block": "R", "category": "v0.23", "wave": w, "model": m,
                                  "frame": "A", "brand": f"S{b:02d}"})
        hs, rep = S.human_sample(units)
        self.assertEqual(rep["total"], 40 + 40 + 48)
        for cat in ("v0.20", "pm"):
            got = [u for u in hs if u["category"] == cat]
            self.assertEqual(len(got), 40)
            self.assertLessEqual(max(sum(1 for u in got if u["brand"] == b) for b in {u["brand"] for u in got}), 3)
            self.assertEqual(sorted(sum(1 for u in got if u["model"] == m) for m in models), [6, 6, 7, 7, 7, 7])
        f = [u for u in hs if u["category"] == "v0.20"]
        self.assertEqual([sum(1 for u in f if u["wave"] == w) for w in ("t1", "t2", "t3")], [14, 13, 13])
        r = [u for u in hs if u["block"] == "R"]
        for b in {u["brand"] for u in r}:
            two = [u for u in r if u["brand"] == b]
            self.assertEqual(len(two), 2)
            self.assertNotEqual(two[0]["model"], two[1]["model"])
            self.assertNotEqual(two[0]["wave"], two[1]["wave"])
        self.assertEqual([u["unit_id"] for u in S.human_sample(units)[0]], [u["unit_id"] for u in hs])

    def test_effective_units(self):
        units = []
        for i in range(300):
            units.append({"unit_id": f"e{i:03d}", "block": "E", "set": "EARLY-6 v0.9 pm", "wave": "v0.9", "category": "pm",
                          "brand": f"b{i % 2}", "model": f"m{i % 6}", "answer_id": f"a{i}", "judged": True, "j2": False,
                          "selfcon": i % 20 == 0, "human": i < 5})
        units += [{"unit_id": f"f{i}", "block": "F", "set": "OMNI t1 v0.20", "wave": "t1", "category": "v0.20", "brand": "x",
                   "model": "m0", "answer_id": f"fa{i}", "judged": True, "j2": True, "selfcon": False, "human": False}
                  for i in range(10)]
        same = S.effective_units(units, S.DEFAULT_PLAN)
        self.assertEqual([(u["judged"], u["j2"]) for u in same], [(u["judged"], u["j2"]) for u in units])
        none = S.effective_units(units, {"e_none": True})
        self.assertEqual({u["unit_id"] for u in none if u["block"] == "E" and u["judged"]}, {f"e{i:03d}" for i in range(5)})
        self.assertTrue(all(u["judged"] and u["j2"] for u in none if u["block"] == "F"))
        cap = S.effective_units(units, {"e_cap": 24})
        self.assertEqual(sum(u["judged"] for u in cap if u["block"] == "E" and not u["human"]) <= 48, True)


class TestJudgeOutput(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(S.parse_judge_output(ok(1, True, evidence="well regarded"))["valence"], 1)
        self.assertEqual(S.parse_judge_output("```json\n" + ok() + "\n```")["valence"], 0)

    def test_invalid(self):
        bad = ["not json", ok(3, True), ok(1, False), ok(0, False, True), ok(1, True, ref=False),
               json.dumps({"valence": 0}), ok(0).replace("false", "0", 1), "", None]
        for b in bad:
            with self.assertRaises(S.JudgeOutputError, msg=str(b)):
                S.parse_judge_output(b)

    def test_request_is_blind_and_sends_no_sampling_parameter(self):
        unit = {"unit_id": "x", "brand_display": "Acme", "category_label": "widgets", "question": "Best widgets?",
                "unit_type": "mention", "text": "Acme is fine.", "model": "secret-model", "wave": "t2", "set": "secret-set"}
        r = S.build_request(unit)
        self.assertNotIn("secret-model", r["user"] + r["system"])
        self.assertNotIn("secret-set", r["user"])
        self.assertNotIn("t2", r["user"])
        flat = json.dumps(r["policy"])
        for w in ("temperature", "top_p", "top_k"):
            self.assertNotIn(f'"{w}"', flat)
        self.assertEqual(r["policy"]["max_output_tokens"], 4096)
        self.assertIsNone(r["policy"]["response_schema"])

    def test_prompt_md_matches_script(self):
        with open(PROMPT_MD, encoding="utf-8") as f:
            md = f.read()
        for name, value in (("SYSTEM_PROMPT", S.SYSTEM_PROMPT), ("USER_TEMPLATE", S.USER_TEMPLATE)):
            block = re.search(rf"<!-- BEGIN {name} -->\n```text\n(.*?)\n```\n<!-- END {name} -->", md, re.S)
            self.assertIsNotNone(block, name)
            self.assertEqual(block.group(1), value, name)
        schema = re.search(r"<!-- BEGIN OUTPUT_SCHEMA -->\n```json\n(.*?)\n```", md, re.S).group(1)
        self.assertEqual(json.loads(schema), S.OUTPUT_SCHEMA)
        tt = re.search(r"<!-- BEGIN TEXT_TYPES -->\n```json\n(.*?)\n```", md, re.S).group(1)
        self.assertEqual(json.loads(tt), S.TEXT_TYPES)
        cl = re.search(r"<!-- BEGIN CATEGORY_LABELS -->\n```json\n(.*?)\n```", md, re.S).group(1)
        self.assertEqual(json.loads(cl), S.CATEGORY_LABELS)

    def test_judges_endpoints_and_vendor_prices(self):
        """Section 7 (budget redesign): judges, endpoints and the vendor pages' prices of 2026-11-10."""
        self.assertEqual({k: v["model_id"] for k, v in S.JUDGES.items()},
                         {"J1": "claude-opus-5-5", "J2": "gpt-6.1-sol", "ALT": "gemini-4-argon"})
        self.assertEqual({k: v["mode"] for k, v in S.JUDGES.items()}, {"J1": "batch", "J2": "batch", "ALT": "sync"})
        self.assertEqual(S.PRICES["claude-opus-5-5"], (4.0, 20.0))
        self.assertEqual(S.PRICES_BATCH["claude-opus-5-5"], (2.0, 10.0))
        self.assertEqual(S.PRICES["gpt-6.1-sol"], (2.0, 10.0))
        self.assertEqual(S.PRICES_BATCH["gpt-6.1-sol"], (1.0, 5.0))
        self.assertEqual(S.PRICES["gpt-6-astra"], (10.0, 50.0))
        self.assertEqual(S.PRICES_BATCH["gpt-6-astra"], (5.0, 25.0))
        self.assertEqual(S.PRICES["claude-fable-5-2"], (8.0, 40.0))
        for m, (pi, po) in S.PRICES_BATCH.items():           # batch = 50% of list on every page
            self.assertEqual((pi, po), (S.PRICES[m][0] / 2, S.PRICES[m][1] / 2), m)
        dec = datetime(2026, 12, 2, tzinfo=timezone.utc)
        self.assertEqual(S.price("gemini-4-argon", dec), (4.0, 20.0))
        self.assertEqual(S.price("gemini-4-argon", dec, batch=True), (2.0, 10.0))
        self.assertEqual((S.HARD_CAP_USD, S.PAUSE_USD, S.PLAN_TARGET_USD), (100.0, 80.0, 80.0))
        self.assertEqual(S.MAX_OUTPUT_TOKENS, 4096)
        self.assertAlmostEqual(S.plan_tokens_per_char("anthropic"), 1.30 / 4.547)
        for j in S.JUDGES.values():
            flat = json.dumps(j["reasoning_param"])
            self.assertIn('"low"', flat)
            for w in ("temperature", "top_p", "top_k"):
                self.assertNotIn(w, flat)
        for prov in ("anthropic", "openai", "google"):
            self.assertIn("accessed 2026-11-10", S.PRICE_SOURCES[prov])

    def test_token_counts_match_the_planning_constant(self):
        tc = json.loads((S.PREREG_DIR / "token_counts_v1_11.json").read_text(encoding="utf-8"))
        u0 = json.loads((S.PREREG_DIR / S.U0_NAME).read_text(encoding="utf-8"))
        self.assertEqual(tc["units_sha256"], u0["units_file"]["sha256"])
        self.assertAlmostEqual(tc["chars_per_token_all"], S.O200K_CHARS_PER_TOKEN, places=3)
        self.assertLessEqual(tc["reply_tokens"]["maximal_valid"], S.PLAN_OUT_VISIBLE)


class TestScore(unittest.TestCase):
    def test_unit_score(self):
        self.assertEqual([S.unit_score(v) for v in S.VALENCES], [0, 25, 50, 75, 100])

    def test_floor_and_neutral_kept(self):
        j = [S.parse_judge_output(ok(0)) for _ in range(4)] + [S.parse_judge_output(ok(2, True, evidence="the best"))] * 2
        bs = S.brand_score(j)
        self.assertEqual(bs.n, 6)
        self.assertAlmostEqual(bs.S, (4 * 50 + 2 * 100) / 6)
        self.assertAlmostEqual(bs.E, 2 / 6)
        self.assertIsNone(bs.NV)
        self.assertIsNone(S.brand_score(j[:5]).S)

    def test_excluded_units(self):
        j = [S.parse_judge_output(ok(ref=False))] + [None] + [S.parse_judge_output(ok(1, True))] * 6
        bs = S.brand_score(j)
        self.assertEqual((bs.n, bs.n_excluded), (6, 2))
        self.assertAlmostEqual(bs.S, 75.0)


def rec(role, uid, attempt, text, status="ok", served=True, model=None, pas="main"):
    return {"role": role, "judge_model": model or S.JUDGES[role]["model_id"], "unit_id": uid, "pass": pas,
            "attempt": attempt, "status": status, "text": text, "served_ok": served, "started_utc": f"t{attempt}"}


class TestOutcomes(unittest.TestCase):
    ROLES = {"J1": "claude-opus-5-5", "J2": "gpt-6.1-sol"}

    def test_valid_fail_unjudged(self):
        recs = [rec("J1", "u1", 1, "bad"), rec("J1", "u1", 2, ok(1, True)),
                rec("J1", "u2", 1, "bad"), rec("J1", "u2", 2, ok(1, True), served=False), rec("J1", "u2", 3, "bad"),
                rec("J1", "u3", 1, "bad"), rec("J1", "u3", 2, "", status="error"),
                rec("J2", "u1", 1, ok(), model="gemini-4-argon")]
        oc = S.outcomes(recs, self.ROLES)
        self.assertEqual(oc[("J1", "u1", "main")]["status"], S.VALID)
        self.assertEqual(oc[("J1", "u1", "main")]["out"]["valence"], 1)
        self.assertEqual(oc[("J1", "u2", "main")]["status"], S.FAIL)
        self.assertEqual(oc[("J1", "u3", "main")]["status"], S.UNJUDGED)
        self.assertNotIn(("J2", "u1", "main"), oc)            # a replaced judge's records are not used


class TestStats(unittest.TestCase):
    def test_spearman_ties(self):
        self.assertAlmostEqual(S.spearman([1, 2, 3, 4], [10, 20, 30, 40]), 1.0)
        self.assertAlmostEqual(S.spearman([1, 2, 3, 4], [4, 3, 2, 1]), -1.0)
        self.assertEqual(S.average_ranks([5, 5, 1]), [2.5, 2.5, 1.0])

    def test_rho_w_is_v1_10_centred_and_removes_level_differences(self):
        g = ["a"] * 5 + ["b"] * 5
        x = [1, 2, 3, 4, 5, 101, 102, 103, 104, 105]
        y = [5, 4, 3, 2, 1, 15, 14, 13, 12, 11]
        self.assertGreater(S.spearman(x, y), 0.5)
        self.assertAlmostEqual(S.rho_w(g, x, y), -1.0)
        r = V.within_ranks(np.array(x, float), np.array(g))
        self.assertAlmostEqual(float(r[:5].mean()), 0.0)
        self.assertAlmostEqual(float(r[5:].mean()), 0.0)

    def test_uncentred_convention_differs_with_unequal_groups(self):
        g = ["a"] * 3 + ["b"] * 9
        x = [1, 2, 3] + list(range(1, 10))
        y = [2, 3, 1] + [9, 1, 8, 2, 7, 3, 6, 4, 5]
        c = S.rho_w(g, x, y)
        with V.uncentred():
            u = S.rho_w(g, x, y)
        self.assertNotAlmostEqual(c, u)
        self.assertTrue(V.CENTRE_RANKS)

    def test_bands_and_three_wave_rule(self):
        self.assertEqual(S.band_verdict(0.30), "CONFIRMED")
        self.assertEqual(S.band_verdict(0.31), "MARGINAL")
        self.assertEqual(S.band_verdict(0.50), "FALSIFIED")
        nan = float("nan")
        # decision 22: v1.10's locked rule (verdict_separability at tag v1.10-prereg-r2)
        self.assertEqual(S.separability_verdict([0.1, 0.2, 0.3]), "CONFIRMED")
        self.assertEqual(S.separability_verdict([0.1, 0.55, 0.6]), "FALSIFIED")
        self.assertEqual(S.separability_verdict([0.1, 0.55, 0.2]), "FALSIFIED")     # any determined wave
        self.assertEqual(S.separability_verdict([0.1, 0.40, 0.2]), "MARGINAL")
        self.assertEqual(S.separability_verdict([0.1, nan, 0.2]), "CONFIRMED")      # 2 determined waves suffice
        self.assertEqual(S.separability_verdict([0.6, nan, nan]), "UNDETERMINED")   # fewer than 2 determined
        self.assertEqual(S.separability_verdict([0.6, 0.6, nan]), "FALSIFIED")
        for case in ([0.1, 0.2, 0.3], [0.1, 0.55, 0.2], [0.1, 0.40, 0.2], [0.1, nan, 0.2], [0.6, nan, nan],
                     [0.6, 0.6, nan], [nan, nan, nan], [0.31, 0.29, 0.5]):
            by_wave = {w: (r, 0 if math.isnan(r) else V.N_FLOOR_UNITS) for w, r in zip(S.WAVES, case)}
            self.assertEqual(S.separability_verdict(case), V.verdict_separability(by_wave), case)

    def test_pooled_test_min_n_and_groups(self):
        rng = random.Random(3)
        g = [s for s in "abc" for _ in range(7)] + ["d"] * 3
        x = [rng.random() for _ in g]
        r = S.pooled_test(x, x, g)
        self.assertEqual(r["n"], 21)                 # group d (3 units < 4) does not enter
        self.assertTrue(r["determinable"])
        r2 = S.pooled_test(x[:14] + x[21:], x[:14] + x[21:], g[:14] + g[21:])
        self.assertFalse(r2["determinable"])         # 14 units from 2 groups
        r3 = S.pooled_test(x[:21], x[:21], ["one"] * 21, single_group=True)
        self.assertTrue(r3["determinable"])

    def test_permutation_seeded_and_detects_signal(self):
        rng = random.Random(7)
        g = [s for s in "abcde" for _ in range(12)]
        x = [rng.random() for _ in g]
        y = [v + rng.gauss(0, 0.1) for v in x]
        old = S.N_PERM
        try:
            S.N_PERM = 500
            r1 = S.pooled_test(x, y, g, perm_seed=1)
            r2 = S.pooled_test(x, y, g, perm_seed=1)
        finally:
            S.N_PERM = old
        self.assertEqual((r1["rho"], r1["p_perm"]), (r2["rho"], r2["p_perm"]))
        self.assertGreater(r1["rho"], 0.8)
        self.assertLess(r1["p_perm"], 0.01)
        self.assertEqual(S.stability_verdict(r1["rho"], r1["p_perm"]), "CONFIRMED")
        self.assertEqual(S.stability_verdict(0.6, 0.2), "FALSIFIED")
        self.assertEqual(S.stability_verdict(0.4, 0.01), "MARGINAL")
        self.assertEqual(S.stability_verdict(0.9, 0.01, determinable=False), "UNDETERMINED")

    def test_alpha(self):
        perfect = [(v, v) for v in S.VALENCES for _ in range(5)]
        self.assertAlmostEqual(S.krippendorff_alpha_ordinal(perfect), 1.0)
        rng = random.Random(3)
        noise = [(rng.choice(S.VALENCES), rng.choice(S.VALENCES)) for _ in range(2000)]
        self.assertLess(abs(S.krippendorff_alpha_ordinal(noise)), 0.1)
        # hand-computed: n_-1 = 2, n_0 = 3, n_1 = 3; delta(0,1) = 9; alpha = 1 - 7*18/600 = 0.79
        self.assertAlmostEqual(S.krippendorff_alpha_ordinal([(-1, -1), (0, 0), (1, 1), (1, 0)]), 0.79)
        self.assertEqual(S.judge_agreement_verdict(0.70, 0.85), "CONFIRMED")
        self.assertEqual(S.judge_agreement_verdict(0.70, 0.55), "FALSIFIED")
        self.assertEqual(S.judge_agreement_verdict(0.60, 0.85), "MARGINAL")
        self.assertEqual(S.judge_agreement_verdict(0.49, 0.95), "FALSIFIED")
        self.assertAlmostEqual(S.cohen_kappa([1, 0, 1, 0], [1, 0, 1, 0]), 1.0)

    def test_self_preference_and_noise_guard(self):
        self.assertEqual(S.self_pref_verdict(4.9, 30, 30), "CONFIRMED")
        self.assertEqual(S.self_pref_verdict(-10.0, 30, 30), "FALSIFIED")
        self.assertEqual(S.self_pref_verdict(7.0, 30, 30), "MARGINAL")
        self.assertEqual(S.self_pref_verdict(1.0, 19, 30), "UNDETERMINED")
        v = {"H1": "FALSIFIED", "H2": "CONFIRMED", "H3": "CONFIRMED", "H4": "CONFIRMED", "H5": "PENDING",
             "H6": "CONFIRMED", "H7": "CONFIRMED", "H8": "CONFIRMED", "H9": "CONFIRMED"}
        out, on = S.apply_noise_guard(v)
        self.assertTrue(on)
        self.assertEqual([out[h] for h in ("H2", "H3", "H5", "H7", "H8")], ["UNDETERMINED"] * 2 + ["PENDING"] + ["UNDETERMINED"] * 2)
        self.assertEqual(out["H6"], "CONFIRMED")
        self.assertFalse(S.apply_noise_guard({**v, "H1": "MARGINAL"})[1])
        self.assertTrue(S.apply_noise_guard({**v, "H1": "CONFIRMED", "H4": "FALSIFIED"})[1])


class TestCost(unittest.TestCase):
    def test_prices_and_gemini_change(self):
        from datetime import datetime, timezone
        before = datetime(2026, 11, 30, 23, 0, tzinfo=timezone.utc)
        after = datetime(2026, 12, 1, 0, 0, tzinfo=timezone.utc)
        self.assertEqual(S.price("gemini-4-argon", before), (2.0, 10.0))
        self.assertEqual(S.price("gemini-4-argon", after), (4.0, 20.0))
        self.assertEqual(S.price("claude-opus-5-5", after), (4.0, 20.0))
        self.assertAlmostEqual(S.call_usd("gpt-6-astra", 1_000_000, 1_000_000, before), 60.0)

    def test_guard_pause_cap_and_call_cap(self):
        g = S.CostGuard(cap_usd=10.0)                # pause at 80% (US$80 of US$100 in the real run)
        g.reserve(1.0)
        g.settle(1.0, 7.9)
        self.assertIsNone(g.check(0.1))
        g.reserve(0.2)
        g.settle(0.2, 0.2)                          # spend 8.1 >= 8.0
        self.assertIn("PAUSED", g.check(0.1))
        self.assertEqual(g.fit([0.1, 0.1]), (0, g.check(0.1)))
        g.approved_past_pause = "Pablo, test"
        self.assertIsNone(g.check(1.8))
        self.assertIn("CAP", g.check(2.0))
        with self.assertRaises(RuntimeError):
            g.reserve(2.0)
        self.assertEqual(g.fit([0.5, 0.5, 0.5, 0.5]), (3, None))   # 8.1 + 1.5 <= 10 < 8.1 + 2.0
        g.reserve_many([0.5, 0.5, 0.5])
        self.assertAlmostEqual(g.reserved_usd, 1.5)
        self.assertIn("CAP", g.fit([0.5])[1])
        g2 = S.CostGuard(cap_calls=1)
        g2.reserve(0.0)
        self.assertIn("CALL CAP", g2.check(0.0))
        self.assertEqual(S.CostGuard().pause_usd, 80.0)

    def test_batch_prices_in_projection(self):
        p = S.project_plan([("claude-opus-5-5", 4547)] * 10, out_per_call=370,
                           in_per_char=S.plan_tokens_per_char("anthropic"))
        ti = math.ceil(4547 * S.plan_tokens_per_char("anthropic"))              # 1.30 tokens per o200k token
        self.assertIn(ti, (1300, 1301))
        self.assertAlmostEqual(p["usd"], 10 * (ti * 2 + 370 * 10) / 1e6)        # batch price (J1 is a batch judge)

    def test_project_plan(self):
        p = S.project_plan([("claude-opus-5-5", 4000)] * 10, out_per_call=370)
        self.assertAlmostEqual(p["usd"], 10 * (1000 * 2 + 370 * 10) / 1e6)
        self.assertAlmostEqual(p["usd_with_overhead"], p["usd"] * 1.15)
        q = S.project_plan([("gpt-6-astra", 4000)] * 10, out_per_call=370)   # not a judge: synchronous price
        self.assertAlmostEqual(q["usd"], 10 * (1000 * 10 + 370 * 50) / 1e6)

    def test_judge_call_is_not_implemented_here(self):
        with self.assertRaises(NotImplementedError):
            S.judge_call({}, "any")


class TestSetsAndLock(unittest.TestCase):
    EXPECTED_ANSWERS = sorted(
        [S.R_FILES[w] for w in S.WAVES]
        + [f"osf/v19/phase_b_responses.jsonl", "osf/v34/data/v19/phase_b_responses.jsonl",
           "osf/v41/data/v19/phase_b_responses.jsonl"]
        + [f"{b}/v2{k}/phase_b_results.csv" for b in ("osf", "osf/v34/data", "osf/v41/data") for k in "012"]
        + ["osf/v23/data/v23_phase_b_raw.json", "osf/v34/data/v23/v23_phase_b_raw.json",
           "osf/v41/data/v23/v23_phase_b_raw.json"]
        + ["data/pm/results_enriched_v09_20260507_181205.csv", "data/finance/results_enriched_v09_20260507_190816.csv",
           "data/oliveoil/results_enriched_v09_20260507_184159.csv", "data/running/results_enriched_v09_20260507_183238.csv",
           "data/skincare/results_enriched_v09_20260507_185427.csv", "data/household/results_v2_household_v1.0_final.csv",
           "data/knives/results_v2_knives_v1.0_final.csv",
           "data/premium_tea/results_v2_premium_tea_20260512_161817_filled.csv"])

    def test_sets(self):
        sets = S.build_sets()
        self.assertEqual([sum(s["block"] == b for s in sets) for b in "RFE"], [3, 15, 8])
        self.assertEqual(sorted(s["answers"] for s in sets), self.EXPECTED_ANSWERS)   # nothing else is loaded
        hh = next(s for s in sets if s["category"] == "household")
        self.assertTrue(hh["answers"].endswith("results_v2_household_v1.0_final.csv"))
        tea = next(s for s in sets if s["category"] == "premium_tea")
        self.assertEqual(tea["registry"], "osf/v14/registries/brands_premium_tea.json")
        self.assertEqual({s["category"] for s in sets if s["block"] == "E"}, set(S.E_PROMPTS))
        for s in sets:
            self.assertIn(s["category"], S.CATEGORY_LABELS)

    def test_v1_10_copy_is_the_locked_file(self):
        p = Path(HERE) / "score_v1_10.py"
        self.assertEqual(V.git_blob_sha1(p), S.V110_SCORER_BLOB)
        r = subprocess.run(["git", "-C", HERE, "rev-parse", f"{S.V110_TAG}:scripts/score_v1_10.py"],
                           capture_output=True, text=True)
        if r.returncode == 0:
            self.assertEqual(r.stdout.strip(), S.V110_SCORER_BLOB)

    def test_v1_10_copies_are_committed_blobs_of_the_tag(self):
        """Decision 23: both v1.10 files are committed byte-identical, their blobs recorded."""
        for rel, blob in S.V110_COPIES.items():
            self.assertEqual(V.git_blob_sha1(S.ROOT / rel), blob, rel)
            r = subprocess.run(["git", "-C", str(S.ROOT), "rev-parse", f"{S.V110_TAG}:{rel}"],
                               capture_output=True, text=True)
            if r.returncode == 0:
                self.assertEqual(r.stdout.strip(), blob, rel)
        self.assertEqual(S.V23_REGISTRY, "osf/methodology/v1_10/registries/v0_23_registry_v1_10.json")

    def test_lock_files_exist_and_manifest_format(self):
        for p in S.LOCK_FILES:
            self.assertTrue((S.ROOT / p).exists(), p)
        txt = S.lock_manifest_text()
        self.assertEqual(len(txt.splitlines()), len(S.LOCK_FILES))
        self.assertTrue(all(re.fullmatch(r"[0-9a-f]{64}  \S+", ln) for ln in txt.splitlines()))
        for v110 in S.V110_COPIES:
            self.assertIn(v110, S.LOCK_FILES)

    def test_anchor_template_and_check_agree(self):
        """Decision 24: the record --write-anchor fills has every field the --run guard checks."""
        t = S.anchor_template()
        self.assertEqual(tuple(t), S.ANCHOR_FIELDS)
        self.assertIn("osf_deposit", t)
        full = {**t, "tag": S.PREREG_TAG, "tag_object": "a" * 40, "commit": "b" * 40, "tree": "c" * 40,
                "branch": "v1.11", "tagger_date": "2026-11-10T12:00:00-06:00", "remote_tag_ref": "x",
                "recorded_utc": "2026-11-10T18:00:00Z", "repository": "r",
                "locked_files": {p: {"sha256": "0" * 64, "git_blob": "0" * 40} for p in S.LOCK_FILES}}
        self.assertIn("the anchor file records no OSF deposit (osf_deposit is empty)", S.anchor_problems(full, "b" * 40))
        ok_anchor = {**full, "osf_deposit": "https://osf.io/ec6wh/ (osfstorage: methodology/v1_11/...)"}
        self.assertEqual(S.anchor_problems(ok_anchor, "b" * 40), [])
        self.assertTrue(any("does not name the commit" in w for w in S.anchor_problems(ok_anchor, "d" * 40)))
        self.assertTrue(S.anchor_problems({"osf_deposit": "x"}))
        import judge_v1_11 as J
        import inspect
        self.assertIn("anchor_problems", inspect.getsource(J.prereg_guard))
        self.assertEqual(S.main(["--write-anchor"]), 3)                    # no --osf-deposit: refused

    def test_coi_and_ai_use_text_verbatim(self):
        """Step 4: the canonical Denon sentence and the AI-use statement, verbatim; Samsung only in
        the Declarations' COI paragraph of the pre-registration."""
        denon = ("Correction (November 10, 2026): Denon, which replaced AKG in the v0.19 registry, has itself been "
                 "owned by Harman International, a wholly owned subsidiary of Samsung Electronics, since September 23, "
                 "2025, when Harman completed its acquisition of Sound United from Masimo; the v0.19 headphones registry "
                 "therefore includes one Samsung-group brand. The substitution did not achieve its purpose, and this "
                 "was not noticed until November 10, 2026.")
        ai = ("During the preparation of this work the author used AI tools (Anthropic's Claude) to assist with study "
              "design, analysis and writing. The author reviewed and edited all content and takes full responsibility "
              "for it.")
        pre = (S.PREREG_DIR / "PRE_REGISTRATION_v1_11.md").read_text(encoding="utf-8")
        dev = (S.ROOT / S.V111 / "anchor/DEVIATIONS.md").read_text(encoding="utf-8")
        self.assertEqual(pre.count(denon), 1)
        self.assertEqual(pre.count(ai), 1)
        self.assertIn(denon, dev)
        coi = pre.split("**Conflict of interest.**")[1].split("**Funding.**")[0]
        self.assertEqual(pre.count("Samsung"), coi.count("Samsung"))

    def test_refuses_stages_before_the_lock(self):
        if V._tag_exists(S.PREREG_TAG, S.ROOT) and S.ANCHOR_FILE.exists():
            self.skipTest("locked tree")
        self.assertEqual(S.main(["--stage", "J"]), 3)
        self.assertEqual(S.main(["--stage", "C"]), 3)

    def test_stage_c_refuses_before_stage_j(self):
        with tempfile.TemporaryDirectory() as d:
            ctx = S.make_ctx(True, root=d, manifest=os.path.join(d, "m.json"), outdir=d)
            with self.assertRaises(V.Halt):
                S.run_stage_c(ctx, log=lambda *a: None)
            with self.assertRaises(V.Halt):
                S.load_frozen_outputs(ctx)


if __name__ == "__main__":
    unittest.main()
