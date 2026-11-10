#!/usr/bin/env python3
"""Unit tests for score_v1_10.py on SYNTHETIC data only (no archive file is read).
Run: python3 -m pytest scripts/test_score_v1_10.py   or   python3 scripts/test_score_v1_10.py"""
import sys
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import score_v1_10 as S  # noqa: E402

REG = {"Alpha": ["Alpha Co"], "Beta": [], "Gamma": ["Gamma-X"], "Estée Lauder": ["Estee Lauder"], "La Mer": []}
P = S.compile_registry(REG)


class Extraction(unittest.TestCase):
    def test_normalize_accents_case(self):
        self.assertEqual(S.normalize("Estée LAUDER"), "estee lauder")

    def test_word_boundary_and_accents(self):
        h = S.find_mentions(S.normalize("Summer picks: ESTÉE Lauder's serum."), P)
        self.assertIn("Estée Lauder", h)
        self.assertNotIn("La Mer", h)          # 'summer' must not match 'la mer'/'mer'

    def test_first_mention_and_repeats(self):
        r = S.rank_answer("Beta is good. Alpha too. Beta again, and Gamma.", P, "first_mention")
        self.assertEqual(r["named"], 3)
        self.assertEqual({b: v[0] for b, v in r["ranks"].items()}, {"Beta": 1, "Alpha": 2, "Gamma": 3})

    def test_lead_item_rule_ignores_comparison_mentions(self):
        txt = ("Top picks:\n1. **Alpha** - often compared with Gamma.\n"
               "2. **Beta** - solid.\n3. **Gamma** - premium.\n")
        prim = S.rank_answer(txt, P, "lead_item")
        sens = S.rank_answer(txt, P, "first_mention")
        self.assertTrue(prim["list_structured"])
        self.assertEqual({b: v[0] for b, v in prim["ranks"].items()}, {"Alpha": 1, "Beta": 2, "Gamma": 3})
        self.assertEqual({b: v[0] for b, v in sens["ranks"].items()}, {"Alpha": 1, "Gamma": 2, "Beta": 3})

    def test_nested_sub_bullets_belong_to_parent(self):
        txt = "- Alpha\n    - beats Gamma on price\n- Beta\n- Gamma\n"
        r = S.rank_answer(txt, P, "lead_item")
        self.assertEqual({b: v[0] for b, v in r["ranks"].items()}, {"Alpha": 1, "Beta": 2, "Gamma": 3})

    def test_headings_as_group_labels(self):
        txt = "## Budget\n**Beta** good\n**Alpha** fine\n## Premium\n**Gamma** best\n"
        r = S.rank_answer(txt, P, "lead_item")
        self.assertEqual({b: v[0] for b, v in r["ranks"].items()}, {"Beta": 1, "Alpha": 2, "Gamma": 3})

    def test_non_leading_brand_follows_lead_brands(self):
        txt = "1. Alpha\n2. Beta\n\nAlso consider Gamma for some uses."
        r = S.rank_answer(txt, P, "lead_item")
        self.assertEqual(r["ranks"]["Gamma"][0], 3)

    def test_prose_answer_first_mention(self):
        r = S.rank_answer("I would start with Gamma, then Alpha.", P, "lead_item")
        self.assertFalse(r["list_structured"])
        self.assertEqual(r["ranks"]["Gamma"][0], 1)

    def test_single_brand_not_rankable(self):
        r = S.rank_answer("Only Alpha is worth it.", P)
        self.assertEqual(r["named"], 1)
        self.assertEqual(r["ranks"], {})

    def test_tie_mid_rank_and_min_rank(self):
        reg = S.compile_registry({"Samsung": [], "Samsung SDI": [], "LG": []})
        r = S.rank_answer("Samsung SDI leads; LG follows.", reg, "first_mention")
        self.assertEqual(r["ranks"]["Samsung"], (1.5, 1))
        self.assertEqual(r["ranks"]["Samsung SDI"], (1.5, 1))
        self.assertEqual(r["ranks"]["LG"], (3.0, 3))

    def test_alias_counts_as_brand(self):
        r = S.rank_answer("Gamma-X first, then Alpha Co.", P, "first_mention")
        self.assertEqual(set(r["ranks"]), {"Gamma", "Alpha"})


class Statistics(unittest.TestCase):
    def test_candidates_known_values(self):
        s = S.brand_scores([(1, 1, 3), (3, 3, 3), (2, 2, 5)])
        self.assertAlmostEqual(s["MNP"], 100 * (1 - (0 + 1 + 0.25) / 3))
        self.assertAlmostEqual(s["IRW"], (1 + 1 / 3 + 1 / 2) / 3)
        self.assertAlmostEqual(s["TOP3"], 1.0)
        self.assertAlmostEqual(s["TOP1"], 1 / 3)
        self.assertAlmostEqual(s["MR"], -2.0)
        self.assertEqual(s["MODE"], -1.0)       # all modes tie -> smallest rank

    def test_rating_floor(self):
        rows = [{"panel": "p", "wave": "t1", "category": "c", "brand": "A", "k_mid": 1, "k_min": 1, "n": 2}] * 6
        rows += [{"panel": "p", "wave": "t1", "category": "c", "brand": "B", "k_mid": 2, "k_min": 2, "n": 2}] * 5
        u = S.score_units(rows)
        self.assertTrue(u[("p", "t1", "c", "A")]["rated"])
        self.assertFalse(u[("p", "t1", "c", "B")]["rated"])

    def test_pooled_within_rho_ignores_level_shifts(self):
        x = [1, 2, 3, 101, 102, 103]
        y = [10, 20, 30, 1, 2, 3]
        g = ["a", "a", "a", "b", "b", "b"]
        self.assertAlmostEqual(S.pooled_within_rho(x, y, g), 1.0)

    def test_perm_p_reproducible_and_small_for_strong_signal(self):
        rng = np.random.default_rng(1)
        x = rng.normal(size=60)
        y = x + rng.normal(scale=0.2, size=60)
        g = np.repeat(["a", "b", "c"], 20)
        obs = S.pooled_within_rho(x, y, g)
        p1 = S.perm_p(x, y, g, obs, seed=7, sided="one", n_draws=500)
        p2 = S.perm_p(x, y, g, obs, seed=7, sided="one", n_draws=500)
        self.assertEqual(p1, p2)
        self.assertLess(p1, 0.01)

    def test_shuffle_keeps_named_sets(self):
        rows = [{"panel": "p", "wave": "t1", "category": "c", "answer_id": i, "brand": b,
                 "k_mid": k, "k_min": k, "n": 3} for i in range(4) for k, b in enumerate("ABC", 1)]
        out = S.shuffle_answer_ranks(rows, np.random.default_rng(3))
        for i in range(4):
            ks = sorted(r["k_mid"] for r in out if r["answer_id"] == i)
            self.assertEqual(ks, [1.0, 2.0, 3.0])

    def test_spearman_brown(self):
        self.assertAlmostEqual(S.spearman_brown(0.5), 2 / 3)


class Selection(unittest.TestCase):
    def test_highest_reliability_wins(self):
        self.assertEqual(S.select_statistic({"MNP": 0.60, "IRW": 0.75, "TOP3": 0.50})["selected"], "IRW")

    def test_tie_window_goes_to_order(self):
        self.assertEqual(S.select_statistic({"MNP": 0.74, "IRW": 0.75})["selected"], "MNP")

    def test_floor(self):
        out = S.select_statistic({"MNP": 0.49, "IRW": 0.20})
        self.assertIsNone(out["selected"])


class Verdicts(unittest.TestCase):
    def test_separability_bands(self):
        self.assertEqual(S.verdict_separability({"t1": (0.30, 50), "t2": (-0.10, 50), "t3": (0.2, 50)}), "CONFIRMED")
        self.assertEqual(S.verdict_separability({"t1": (0.31, 50), "t2": (0.10, 50)}), "MARGINAL")
        self.assertEqual(S.verdict_separability({"t1": (-0.50, 50), "t2": (0.10, 50)}), "FALSIFIED")
        self.assertEqual(S.verdict_separability({"t1": (0.10, 50), "t2": (0.10, 29)}), "UNDETERMINED")

    def test_stability_bands(self):
        self.assertEqual(S.verdict_stability(0.55, 0.001, 0.01, 40), "CONFIRMED")
        self.assertEqual(S.verdict_stability(0.45, 0.001, 0.01, 40), "MARGINAL")
        self.assertEqual(S.verdict_stability(0.55, 0.001, 0.20, 40), "FALSIFIED")
        self.assertEqual(S.verdict_stability(0.29, 0.001, 0.01, 40), "FALSIFIED")
        self.assertEqual(S.verdict_stability(0.90, 0.001, 0.01, 20), "UNDETERMINED")

    def test_gate(self):
        self.assertEqual(S.gate_verdict("CONFIRMED", "CONFIRMED", "CONFIRMED"), "PASS")
        self.assertEqual(S.gate_verdict("CONFIRMED", "CONFIRMED", "CONFIRMED", "FALSIFIED"), "MARGINAL")
        self.assertEqual(S.gate_verdict("CONFIRMED", "MARGINAL", "CONFIRMED"), "MARGINAL")
        self.assertEqual(S.gate_verdict("FALSIFIED", "UNDETERMINED", "CONFIRMED"), "FAIL")
        self.assertEqual(S.gate_verdict("CONFIRMED", "UNDETERMINED", "CONFIRMED"), "UNDETERMINED")


class Order(unittest.TestCase):
    def test_pc_refused_before_selection(self):
        if S.SELECTION_FILE.exists():
            self.skipTest("selection file present")
        with self.assertRaises(RuntimeError):
            S.open_presence_consistency(Path("/nonexistent.csv"))


# ===========================================================================
# Added 2026-11-10 (loaders, pipeline, refusal, S7, shuffle nulls). Every test below
# reads synthetic replicas only, built into a temporary directory by
# osf/methodology/v1_10/dryrun/build_dryrun_v1_10.py; no real answer file is opened.
# ===========================================================================
import contextlib  # noqa: E402
import csv  # noqa: E402
import importlib.util  # noqa: E402
import json  # noqa: E402
import os  # noqa: E402
import tempfile  # noqa: E402
from unittest import mock  # noqa: E402

REPO = Path(__file__).resolve().parents[1]


def _load_module(rel, name):
    spec = importlib.util.spec_from_file_location(name, str(REPO / rel))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


B = _load_module("osf/methodology/v1_10/dryrun/build_dryrun_v1_10.py", "build_dryrun_v1_10")
RI = _load_module("osf/methodology/v1_10/registries/build_registry_inputs_v1_10.py", "build_registry_inputs_v1_10")
_TMP = tempfile.TemporaryDirectory(prefix="v110_test_")
_REPLICA = Path(_TMP.name) / "replica"
_MANIFEST = B.build(_REPLICA, Path(_TMP.name) / "manifest.json", seed=4242)


def dry_ctx(outdir=None):
    out = Path(outdir) if outdir else Path(tempfile.mkdtemp(dir=_TMP.name))
    return S.Ctx(dry=True, root=_REPLICA, manifest=_MANIFEST, outdir=out)


def spec_of(name):
    return next(s for s in S.build_sets() if s["set"] == name)


@contextlib.contextmanager
def few_draws():
    keep = (S.N_PERM, S.N_SHUFFLE, S.N_SHUFFLE_MQ7, S.N_BOOT)
    S.N_PERM, S.N_SHUFFLE, S.N_SHUFFLE_MQ7, S.N_BOOT = 199, 199, 40, 40
    try:
        yield
    finally:
        S.N_PERM, S.N_SHUFFLE, S.N_SHUFFLE_MQ7, S.N_BOOT = keep


class Decisions(unittest.TestCase):
    def test_constants(self):
        self.assertEqual((S.N_PERM, S.N_SHUFFLE, S.N_SHUFFLE_MQ7, S.N_BOOT), (10_000, 10_000, 2_000, 2_000))
        self.assertEqual((S.SEEDS["SHUFFLE"], S.SEEDS["MQ7"], S.SEEDS["BOOT"]), (110010, 110030, 110020))
        self.assertEqual((S.RATING_FLOOR, S.N_FLOOR_UNITS, S.MIN_UNITS_PER_CATEGORY), (6, 30, 5))
        self.assertEqual(S.RULES[0], "lead_item")

    def test_held_studies_absent(self):
        paths = json.dumps(S.build_sets())
        self.assertNotIn("v38", paths)
        self.assertNotIn("v39", paths)
        man = json.loads(S.MANIFEST.read_text())
        self.assertFalse([e for e in man["files"] if "/v38/" in e["path"] or "/v39/" in e["path"]])

    def test_manifest_covers_every_input_the_scorer_reads(self):
        pinned = {e["path"] for e in json.loads(S.MANIFEST.read_text())["files"]}
        for s in S.build_sets():
            for k in ("answers", "registry", "coded", "detector", "prompts"):
                if s.get(k):
                    self.assertIn(s[k], pinned, s[k])
        self.assertIn(S.PROFILES_REL, pinned)
        self.assertIn("osf/methodology/v1_10/registries/v0_23_registry_v1_10.json", pinned)
        self.assertIn("scripts/score_v0_23.py", pinned)
        self.assertNotIn(S.COI_REL, pinned)                      # decision 12

    def test_gate_instrument_fail(self):
        self.assertEqual(S.gate_verdict("CONFIRMED", "CONFIRMED", "CONFIRMED", None, instrument_fail=True), "FAIL")

    def test_file_swaps(self):
        self.assertEqual(spec_of("EARLY-2 v0.6 oliveoil")["answers"], "data/oliveoil/results_v2_20260430_091539.csv")
        self.assertEqual(spec_of("EARLY-6 v1.0 household")["answers"],
                         "data/household/results_v2_household_v1.0_final.csv")
        pinned = {e["path"] for e in json.loads(S.MANIFEST.read_text())["files"]}
        self.assertNotIn("data/oliveoil/_pre_revision/results_v2_20260430_085246.csv", pinned)
        self.assertNotIn("data/household/results_v2_household_v1.0_merged.csv", pinned)
        self.assertEqual(spec_of("EARLY-6 v0.16 kitchen_knives")["registry"], "registries/brands_kitchen_knives.json")
        self.assertEqual(spec_of("EARLY-6 v1.0 knives")["registry"], "registries/brands_knives_v1.0.json")


class Centring(unittest.TestCase):
    def test_centred_ranks_sum_to_zero_per_category(self):
        g = np.array(["a"] * 4 + ["b"] * 7)
        r = S.within_ranks(np.arange(11.0), g)
        self.assertAlmostEqual(r[:4].sum(), 0.0)
        self.assertAlmostEqual(r[4:].sum(), 0.0)
        with S.uncentred():
            self.assertEqual(list(S.within_ranks(np.arange(4.0), np.array(["a"] * 4))), [1.0, 2.0, 3.0, 4.0])
        self.assertTrue(S.CENTRE_RANKS)                               # restored after S9

    def test_unequal_category_sizes_no_offset_when_centred(self):
        # two independent variables, categories of 5 and 40 units: centred rho_w averages ~0,
        # the uncentred v0.37-v0.41 convention carries a positive between-category offset
        rng = np.random.default_rng(12)
        g = np.array(["s"] * 5 + ["l"] * 40)
        cen, unc = [], []
        for _ in range(400):
            x, y = rng.normal(size=45), rng.normal(size=45)
            cen.append(S.pooled_within_rho(x, y, g))
            with S.uncentred():
                unc.append(S.pooled_within_rho(x, y, g))
        self.assertLess(abs(np.mean(cen)), 0.03)
        self.assertGreater(np.mean(unc), 0.15)

    def test_fast_path_matches_reference_both_conventions(self):
        rng = np.random.default_rng(13)
        x, y = rng.normal(size=30), rng.normal(size=30)
        g = np.array(["a"] * 6 + ["b"] * 24)
        gidx = S._group_index(g)
        for ctxm in (contextlib.nullcontext(), S.uncentred()):
            with ctxm:
                self.assertAlmostEqual(S.pooled_within_rho(x, y, g),
                                       S._pearson(S._within_ranks_idx(x, gidx), S._within_ranks_idx(y, gidx)))


class Loaders(unittest.TestCase):
    ctx = None

    @classmethod
    def setUpClass(cls):
        cls.ctx = dry_ctx()

    def test_frame_csv_v20(self):
        a = S.load_answers(self.ctx, spec_of("OMNI t2 v0.20"))
        self.assertEqual(len(a), 36)
        self.assertEqual({x["frame"] for x in a}, {"q1", "q2", "q3", "q4", "q5", "q6"})
        self.assertTrue(all(x["text"] and x["run_idx"] is None and x["panel"] == "LEGACY-6" for x in a))

    def test_v19_jsonl(self):
        a = S.load_answers(self.ctx, spec_of("OMNI t1 v0.19"))
        self.assertEqual(len(a), 36)
        self.assertIn("q4_famous", {x["frame"] for x in a})
        self.assertEqual(len({x["model"] for x in a}), 6)

    def test_v23_json_and_unit_keys(self):
        a = S.load_answers(self.ctx, spec_of("OMNI t3 v0.23"))
        self.assertEqual(len(a), 36)
        reg, unit, _ = S.load_registry(self.ctx, spec_of("OMNI t3 v0.23")["registry"], "v23_json")
        self.assertEqual(len(reg), 24)
        self.assertEqual(unit["Hennessy"], "S02")
        self.assertIn("jack daniels", reg["Jack Daniel's"])

    def test_runner_csv_variants_and_missing_cells(self):
        v09 = S.load_answers(self.ctx, spec_of("EARLY-6 v0.9 pm"))
        self.assertEqual(len(v09), 288)
        self.assertEqual({x["run_idx"] for x in v09}, set(range(1, 9)))
        self.assertTrue(any(x["archived_ranked"] for x in v09))
        hh = S.load_answers(self.ctx, spec_of("EARLY-6 v1.0 household"))
        self.assertEqual((len(hh), sum(x["text"] is None for x in hh)), (288, 0))   # the scored _final file
        kk = S.load_answers(self.ctx, spec_of("EARLY-6 v0.16 kitchen_knives"))
        miss = [x for x in kk if x["text"] is None]
        self.assertEqual((len(kk), len(miss)), (515, 181))
        self.assertTrue(all(x["missing_reason"].startswith("status:") for x in miss))
        self.assertEqual(len({x["frame"] for x in kk}), 11)
        v06 = S.load_answers(self.ctx, spec_of("EARLY-2 v0.6 finance"))
        self.assertEqual(len(v06), 96)
        self.assertEqual({x["model"] for x in v06}, set(S.EARLY_SHARED_MODELS))

    def test_v32_and_v28(self):
        a = S.load_answers(self.ctx, spec_of("PAPER-B v0.32 arm B"))
        self.assertEqual(len(a), 36)
        self.assertIn("claude-opus-4-8", {x["model"] for x in a})
        self.assertEqual(len(S.load_answers(self.ctx, spec_of("COI-HOLD v0.28"))), 36)

    def test_v28_parse_only(self):
        self.assertEqual(spec_of("COI-HOLD v0.28")["role"], "coi_hold")
        with mock.patch.object(S, "rank_answer", side_effect=AssertionError("v0.28 must not be ranked")):
            po = S.parse_only_sets(self.ctx)
        self.assertEqual(po["COI-HOLD v0.28"]["with_text"], 36)
        data = S.run_extraction(self.ctx, log=lambda *a: None)
        self.assertNotIn("COI-HOLD v0.28", data)                      # no rank table, no statistic

    def test_registry_formats(self):
        for name, n in (("OMNI t1 v0.19", 16), ("OMNI t1 v0.20", 24), ("OMNI t1 v0.21", 24), ("OMNI t1 v0.22", 24),
                        ("COI-HOLD v0.28", 24), ("PAPER-B v0.32 arm A", 24)):
            sp = spec_of(name)
            reg, unit, _ = S.load_registry(self.ctx, sp["registry"], sp["reg_fmt"])
            self.assertEqual(len(reg), n, name)
            self.assertTrue(all(unit[c] == c for c in reg))
        sp = spec_of("EARLY-6 v0.9 pm")                          # bare-list schema
        reg, _, _ = S.load_registry(self.ctx, sp["registry"], sp["reg_fmt"])
        self.assertGreater(len(reg), 5)
        sp = spec_of("EARLY-6 v0.14 premium_tea")                # wrapper schema, tracked copy
        self.assertEqual(sp["registry"], "osf/v14/registries/brands_premium_tea.json")

    def test_unpinned_path_refused(self):
        with self.assertRaises(S.Halt):
            self.ctx.path("data/pm/results_v2_20260429_181007.csv.not_pinned")

    def test_v23_registry_expansion(self):
        self.assertEqual(RI.expand_pattern(r"\bjack\s+daniel'?s?\b"),
                         ["jack daniel", "jack daniel'", "jack daniel's", "jack daniels"])
        self.assertEqual(RI.expand_pattern(r"\bfernet[\s-]*branca\b"), ["fernet branca", "fernet-branca", "fernetbranca"])
        self.assertEqual(RI.expand_pattern(r"\b(the\s+)?balvenie\b"), ["balvenie", "the balvenie"])


class Refusal(unittest.TestCase):
    def test_refuses_without_tag_and_anchor(self):
        with mock.patch.object(S, "_tag_exists", return_value=False), \
                mock.patch.object(S, "ANCHOR_FILE", Path(_TMP.name) / "no_anchor.json"), \
                mock.patch.object(S, "run_stage_s", side_effect=AssertionError("must not run")), \
                mock.patch.object(S, "run_stage_c", side_effect=AssertionError("must not run")):
            for st in ("S", "C"):
                self.assertEqual(S.main(["--stage", st]), 3)

    def test_refuses_with_tag_but_no_anchor_and_vice_versa(self):
        anchor = Path(_TMP.name) / "anchor_present.json"
        anchor.write_text("{}")
        for tag, anc in ((True, Path(_TMP.name) / "no_anchor.json"), (False, anchor)):
            with mock.patch.object(S, "_tag_exists", return_value=tag), mock.patch.object(S, "ANCHOR_FILE", anc), \
                    mock.patch.object(S, "run_stage_s", side_effect=AssertionError("must not run")):
                self.assertEqual(S.main(["--stage", "S"]), 3)

    def test_runs_when_locked(self):
        anchor = Path(_TMP.name) / "anchor_present.json"
        anchor.write_text("{}")
        with mock.patch.object(S, "_tag_exists", return_value=True), mock.patch.object(S, "ANCHOR_FILE", anchor), \
                mock.patch.object(S, "run_stage_s", return_value={}) as rs:
            self.assertEqual(S.main(["--stage", "S"]), 0)
            self.assertTrue(rs.called)

    def test_dry_run_bypasses_refusal(self):
        with mock.patch.object(S, "_tag_exists", return_value=False), \
                mock.patch.object(S, "ANCHOR_FILE", Path(_TMP.name) / "no_anchor.json"), \
                mock.patch.object(S, "DRY_ROOT", _REPLICA), mock.patch.object(S, "DRY_MANIFEST", _MANIFEST), \
                mock.patch.object(S, "DRY_OUTDIR", Path(_TMP.name) / "dry_out"), \
                mock.patch.object(S, "run_stage_s", return_value={}) as rs:
            self.assertEqual(S.main(["--stage", "S", "--dry-run"]), 0)
            ctx = rs.call_args[0][0]
            self.assertTrue(ctx.dry)
            self.assertEqual(ctx.root, _REPLICA)

    def test_real_run_refused_now(self):
        if S._tag_exists() and S.ANCHOR_FILE.exists():
            self.skipTest("locked")
        with mock.patch.object(S, "run_stage_s", side_effect=AssertionError("must not run")):
            self.assertEqual(S.main(["--stage", "S"]), 3)


class ShuffleNull(unittest.TestCase):
    def _rows(self, n_answers, order_fn, rng, wave="t1"):
        rows = []
        brands = list("ABCDEFG")
        for a in range(n_answers):
            named = list(rng.choice(brands, size=int(rng.integers(2, 7)), replace=False))
            for k, b in enumerate(order_fn(named, rng), 1):
                rows.append({"panel": "p", "wave": wave, "category": "c" + str((a // 2) % 6), "answer_id": f"{wave}-{a}",
                             "brand": b, "k_mid": float(k), "k_min": k, "n": len(named), "run_idx": a % 8 + 1})
        return rows

    def test_rankmatrix_matches_brand_scores(self):
        rng = np.random.default_rng(3)
        rows = self._rows(300, lambda nm, r: sorted(nm), rng)
        rows[0]["k_mid"], rows[1]["k_mid"] = 1.5, 1.5               # a tie
        rows[0]["k_min"] = rows[1]["k_min"] = 1
        RM = S.RankMatrix(rows, unit_of=lambda r: (r["category"], r["brand"]))
        ref = {(k[2], k[3]): v for k, v in S.score_units(rows).items()}
        for stat in S.CANDIDATES:
            v = RM.stat(stat)
            for u, i in RM.uidx.items():
                self.assertAlmostEqual(v[i], ref[u][stat], places=10, msg=(stat, u))

    def test_shuffle_is_a_permutation_within_answer(self):
        rng = np.random.default_rng(4)
        rows = self._rows(50, lambda nm, r: nm, rng)
        RM = S.RankMatrix(rows, unit_of=lambda r: (r["category"], r["brand"]))
        _, k = RM.shuffled(np.random.default_rng(9))
        for a in np.unique(RM.a):
            ks = sorted(k[RM.a == a])
            self.assertEqual(ks, list(range(1, len(ks) + 1)))

    def test_shuffle_p_detects_stable_order_and_not_noise(self):
        rng = np.random.default_rng(5)
        stable = lambda nm, r: sorted(nm)                           # noqa: E731 - same order both waves
        noise = lambda nm, r: list(r.permutation(nm))                # noqa: E731
        a = self._rows(400, stable, rng, "t1")
        b = self._rows(400, stable, rng, "t2")
        Ua, Ub = S.units_cat_brand(a), S.units_cat_brand(b)
        keys = sorted(k for k in Ua if Ua[k]["rated"] and k in Ub and Ub[k]["rated"])
        g = np.array([k[0] for k in keys])
        obs = S.pooled_within_rho([Ua[k]["MNP"] for k in keys], [Ub[k]["MNP"] for k in keys], g)
        self.assertLess(S.shuffle_p(a, b, keys, g, "MNP", obs, seed=1, n_draws=199), 0.05)
        c = self._rows(400, noise, rng, "t1")
        d = self._rows(400, noise, rng, "t2")
        Uc, Ud = S.units_cat_brand(c), S.units_cat_brand(d)
        keys = sorted(k for k in Uc if Uc[k]["rated"] and k in Ud and Ud[k]["rated"])
        g = np.array([k[0] for k in keys])
        obs = S.pooled_within_rho([Uc[k]["MNP"] for k in keys], [Ud[k]["MNP"] for k in keys], g)
        self.assertGreater(S.shuffle_p(c, d, keys, g, "MNP", obs, seed=1, n_draws=199), 0.05)

    def test_mq7_fast_equals_reference_draws(self):
        rng = np.random.default_rng(6)
        rows = self._rows(600, lambda nm, r: sorted(nm), rng)
        res = S.mq7_negative_control(rows, "MNP", n_draws=5, seed=11)
        odd = [r for r in rows if r["run_idx"] % 2 == 1]
        even = [r for r in rows if r["run_idx"] % 2 == 0]
        self.assertAlmostEqual(res["unshuffled_reliability_check"], S.split_half_reliability(odd, even, "MNP")[0])
        r2 = np.random.default_rng(11)
        ref = []
        for _ in range(5):
            sh = S.shuffle_answer_ranks(rows, r2)
            ref.append(S.split_half_reliability([r for r in sh if r["run_idx"] % 2 == 1],
                                                [r for r in sh if r["run_idx"] % 2 == 0], "MNP")[0])
        self.assertAlmostEqual(res["mean_reliability"], float(np.nanmean(ref)), places=10)

    def test_tie_rounding(self):
        self.assertEqual(list(S._rank_avg([0.1 + 0.2, 0.3, 1.0])), [1.5, 1.5, 3.0])


class COIandJoin(unittest.TestCase):
    def test_s7_absent_file(self):
        ctx = dry_ctx()
        ctx.root = Path(_TMP.name) / "empty_root"
        self.assertEqual(S.load_coi(ctx, {})[0], None)

    def test_s7_maps_names_and_excludes_units(self):
        ctx = dry_ctx()
        data = S.run_extraction(ctx, roles=("omni",), log=lambda *a: None)
        flagged, sha, unknown = S.load_coi(ctx, data)
        self.assertEqual(flagged, {("v0.19", "Denon"), ("v0.23", "S02")})
        self.assertEqual(len(sha), 64)
        U = {w: {("v0.19", b): {"rated": True, "MNP": float(i)} for i, b in enumerate("abcdefgh")} for w in S.WAVES}
        for w in S.WAVES:
            U[w][("v0.19", "Denon")] = {"rated": True, "MNP": 99.0}
        P = {w: {k: float(i) for i, k in enumerate(sorted(U[w]))} for w in S.WAVES}
        full = S.separability(U, P, "MNP", 1, boot=False)
        cut = S.separability(U, P, "MNP", 1, excl_units=flagged, boot=False)
        self.assertEqual(full["per_wave"]["t1"]["n"], 9)
        self.assertEqual(cut["per_wave"]["t1"]["n"], 8)

    def test_join_check(self):
        units = {w: {("v0.19", f"B{i}") for i in range(112)} for w in S.WAVES}
        keys = [(w, s, b) for w in S.WAVES for (s, b) in sorted(units[w])]
        self.assertTrue(S.join_check(keys, units)["passes"])
        self.assertFalse(S.join_check(keys + [("t1", "v0.19", "B0")], units)["passes"])
        self.assertFalse(S.join_check(keys[1:], units)["passes"])

    def test_profile_keys_only(self):
        p = Path(_TMP.name) / "prof.csv"
        p.write_text("wave,substrate,brand,P,C_star,rated\nt1,v0.19,X,12.5,40,1\n")
        self.assertEqual(S.profile_keys(p), [("t1", "v0.19", "X")])
        P, C, _ = S.parse_profiles([{"wave": "t1", "substrate": "s", "brand": "a", "P": "1", "C_star": "", "rated": "0"},
                                    {"wave": "t1", "substrate": "s", "brand": "b", "P": "2", "C_star": "3", "rated": "1"}])
        self.assertEqual(set(C["t1"]), {("s", "b")})

    def test_h6_not_run_when_mq8_fails(self):
        self.assertEqual(S.h6_block({}, "MNP", False)["verdict"], "UNDETERMINED")

    def test_s6_real_mc_snapshot_lists_no_mismatch(self):
        # the pinned v0.41 verdict file (not an answer file): no model flagged -> S6 = primary
        models, note = S.s6_flagged_models(S.Ctx())
        self.assertEqual(models, [])
        self.assertIn("MC_Snapshot", note)

    def test_symlink_entries_verified_on_link_text(self):
        d = Path(tempfile.mkdtemp(dir=_TMP.name))
        (d / "target.json").write_text("{}")
        os.symlink("/somewhere/else.json", d / "link.json")
        man = d / "m.json"
        man.write_text(json.dumps({"files": [
            {"path": "link.json", "symlink_to": "/somewhere/else.json", "git_blob": S.git_blob_sha1(d / "link.json"),
             "sha256": "x"},
            {"path": "target.json", "git_blob": S.git_blob_sha1(d / "target.json"), "sha256": S.sha256(d / "target.json")}]}))
        self.assertEqual(S.verify_manifest(man, d), [])
        ctx = S.Ctx(dry=True, root=d, manifest=man, outdir=d / "o")
        with self.assertRaises(S.Halt):
            ctx.path("link.json")


class Pipeline(unittest.TestCase):
    """End to end on a temporary synthetic replica with reduced draws."""

    def test_stage_s_then_c(self):
        out = Path(tempfile.mkdtemp(dir=_TMP.name))
        ctx = dry_ctx(out)
        quiet = lambda *a: None                                     # noqa: E731
        with self.assertRaises(S.Halt):                             # ORDER: no Stage C before Stage S
            S.run_stage_c(ctx, log=quiet)
        calls = []
        real_open, real_keys = S.open_presence_consistency, S.profile_keys

        def spy_open(path, selection_file=None):
            calls.append(("open", Path(selection_file).exists()))
            return real_open(path, selection_file)

        def spy_keys(path):
            calls.append(("keys", None))
            return real_keys(path)
        with few_draws(), mock.patch.object(S, "open_presence_consistency", spy_open), \
                mock.patch.object(S, "profile_keys", spy_keys):
            summ = S.run_stage_s(ctx, log=quiet)
            self.assertEqual(calls, [])                             # Stage S never touches P/C
            self.assertTrue(ctx.selection_file.exists())
            self.assertEqual(summ["selection_sha256"], S.sha256(ctx.selection_file))
            for name, v in summ["rank_tables"].items():
                self.assertEqual(S.sha256(out / v["path"]), v["sha256"], name)
            doc = S.run_stage_c(ctx, log=quiet)
        self.assertEqual(calls, [("open", True)])                   # opened once, after the selection
        self.assertIn(doc["GATE"]["verdict"], ("PASS", "MARGINAL", "FAIL", "UNDETERMINED"))
        for h in ("H1_Sep_Presence", "H2_Sep_Consistency", "H3_Rank_Stability", "H4_Sep_Presence_Early",
                  "H5_Rank_LongHorizon", "H6_Early_Stability"):
            self.assertIn(doc[h]["verdict"], ("CONFIRMED", "MARGINAL", "FALSIFIED", "UNDETERMINED"), h)
        self.assertEqual(len(doc["coi_flags_sha256"]), 64)          # S7 file present in the replica
        self.assertEqual(doc["sensitivities"]["S6_without_flagged_models"]["models_dropped"], ["gpt-4o-mini"])
        self.assertTrue(all(v["passes"] for v in doc["data_quality_from_stage_s"]["MQ2"]["per_set"].values()))
        self.assertEqual({r["stratum"] for r in doc["baseline"]}, {"LEGACY-6", "EARLY-6", "EARLY-2"})
        self.assertFalse([r for r in doc["baseline"] if "v0.32" in r["set"]])   # Paper B arms: not analysed
        self.assertFalse([r for r in doc["baseline"] if "v0.28" in r["set"]])   # v0.28: COI hold
        self.assertEqual({r["set"] for r in doc["baseline"] if r["stratum"] == "LEGACY-6"},
                         {f"OMNI {w} {s}" for w in S.WAVES for s in S.OMNI})   # LEGACY-6 = OMNI only
        self.assertFalse([k for k in doc["rank_tables"] if "v0.28" in k])
        dq = doc["data_quality_from_stage_s"]
        self.assertEqual(set(dq["MQ1_parse_only"]), {"COI-HOLD v0.28"})
        for m in ("MQ1", "MQ3", "MQ4", "MQ5"):
            self.assertFalse([k for k in dq[m] if "v0.28" in k], m)
        s8 = doc["selection"]["S8_without_knife_sets"]                # S8: next to the selection
        self.assertEqual(s8["sets_removed"], S.KNIFE_SETS)
        self.assertEqual(set(s8["reliability"]), set(S.CANDIDATES))
        self.assertIn("would_select", doc["selection"]["S9_uncentred"])
        s9 = doc["sensitivities"]["S9_next_to_primary"]               # S9: next to the primary values
        self.assertEqual(set(s9), {"H1", "H2", "H3", "H4", "H5", "H6", "MQ6", "MQ7", "verdicts_uncentred"})
        self.assertAlmostEqual(s9["H3"]["centred"], doc["H3_Rank_Stability"]["rho"])
        mq5 = doc["data_quality_from_stage_s"]["MQ5"]
        self.assertEqual(set(mq5["EARLY-6 v0.16 kitchen_knives"]["ordinary_word_aliases"]),
                         {"global", "mac", "made in", "dick", "kramer", "new west"})
        self.assertEqual(len(mq5["EARLY-6 v0.16 kitchen_knives"]["canonical_names_ending_non_word"]), 2)
        self.assertTrue(mq5["EARLY-6 v1.0 knives"]["ordinary_word_aliases"])
        json.loads(ctx.verdicts_file.read_text())
        # a tampered rank table index makes Stage C halt
        summ = json.loads(ctx.stage_s_file.read_text())
        first = next(iter(summ["rank_tables"]))
        summ["rank_tables"][first]["sha256"] = "0" * 64
        ctx.stage_s_file.write_text(json.dumps(summ))
        with self.assertRaises(S.Halt):
            S.run_stage_c(ctx, log=quiet)

    def test_parity_mode_on_replica(self):
        out = Path(tempfile.mkdtemp(dir=_TMP.name))
        ctx = dry_ctx(out)
        with mock.patch.object(S, "rank_answer", side_effect=AssertionError("parity must not rank")):
            res = S.run_parity(ctx, log=lambda *a: None)
        self.assertTrue(all(res["summary"].values()))
        self.assertTrue((out / "parity_v1_10.json").exists())

    def test_rank_table_rows(self):
        ctx = dry_ctx()
        data = S.run_extraction(ctx, roles=("paperB",), log=lambda *a: None)
        b = S.rank_table_bytes(data["PAPER-B v0.32 arm A"]).decode()
        rows = list(csv.DictReader(b.splitlines()))
        self.assertEqual(set(rows[0]), set(S.RANK_COLS))
        rk = [r for r in rows if r["k_mid"]]
        self.assertTrue(rk)
        for r in rk:
            self.assertTrue(0.0 <= float(r["q"]) <= 1.0)


if __name__ == "__main__":
    unittest.main(verbosity=1)
