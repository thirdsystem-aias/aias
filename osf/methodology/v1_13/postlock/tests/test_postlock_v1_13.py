#!/usr/bin/env python3
"""Tests of the v1.13 post-lock modules (postlock/). SYNTHETIC inputs only: the locked scorer's own synthetic t4
generator (scripts/tests/test_score_v1_13.synthetic_t4) and hand-made audit records under .test; no t4 data, no
network. Run:
    PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s osf/methodology/v1_13/postlock/tests -v
"""
import csv
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
POST = HERE.parent
PHASE = POST.parent
sys.path.insert(0, str(PHASE / "scripts"))
sys.path.insert(0, str(PHASE / "scripts" / "tests"))
sys.path.insert(0, str(POST))
sys.dont_write_bytecode = True
import score_v1_13 as S  # noqa: E402
import audit_checks_v1_13 as AC  # noqa: E402
import c2_extras_v1_13 as CX  # noqa: E402
import run_stage_v1_13 as RS  # noqa: E402
import write_part2_addendum_v1_13 as WA  # noqa: E402
from test_score_v1_13 import synthetic_t4  # noqa: E402


def page(outcome="ok", status=200, types=(), same_as=(), blocks=1, errors=0):
    return {"outcome": outcome, "status": status, "types": list(types), "same_as": list(same_as),
            "ld_blocks": blocks, "ld_errors": errors}


def rec(bid, p1, p2=None, phantom=False, domain="x.test"):
    pages = {"P1": p1}
    if p2:
        pages["P2"] = p2
    return {"substrate": "v19", "brand_id": bid, "brand": bid, "phantom": phantom, "domain": domain, "pages": pages}


class TestAuditChecks(unittest.TestCase):
    def test_aq2_status_200_vs_ok(self):
        r = [rec("A", page()), rec("B", page(status=203)), rec("C", page("blocked", 403)),
             rec("D", {}, phantom=True, domain=None)]
        q = AC.aq2(r)
        self.assertEqual((q["units_with_domain"], q["p1_status_200"], q["p1_outcome_ok"]), (3, 1, 2))
        self.assertAlmostEqual(q["share_status_200"], 1 / 3)
        self.assertTrue(q["flag_below_0_80"])

    def test_aq3_counts_parse_errors_on_fetched_pages(self):
        r = [rec("A", page(blocks=3, errors=1), page(blocks=2, errors=2)), rec("B", page("blocked", 403, errors=9))]
        self.assertEqual(AC.aq3(r), {"pages_parsed": 2, "ld_blocks": 5, "ld_parse_errors": 3})

    def test_aq4_p1_only_both_passes(self):
        a1 = rec("A", page(types=["Organization"]), page(types=["Product"]))       # P3-like type ignored
        b1 = rec("B", page(types=["Organization"], same_as=["https://www.wikidata.org/wiki/Q1"]))
        c1 = rec("C", page("blocked", 403))
        a2 = rec("A", page(types=["Organization"]))
        b2 = rec("B", page(types=["Organization"]))                                    # sameAs gone: (4),(5) change
        c2 = rec("C", page())
        q = AC.aq4([a1, b1, c1], [a2, b2, c2])
        self.assertEqual((q["units_ok_in_both"], q["changed"], q["units_changed"]), (2, 1, ["v19|B"]))

    def test_skg_sensitivity_uses_the_scorer(self):
        inp = synthetic_t4()
        doc = json.loads(json.dumps(S.stage_c1(inp, n_perm=0, n_boot=0, sensitivities=False), default=str))
        gs = {tuple(k.split("|")): u["G_star"] for k, u in doc["units"].items() if u["rated"]}
        rows = [{"substrate": k[0], "brand_id": k[1], "phantom": "0", "SDRI_kg": str(round(g / 100 * 3) * 100 / 3)}
                for k, g in gs.items()]
        out = AC.skg_sensitivity(rows, doc, n_perm=99, n_boot=0)
        self.assertEqual(out["leg"]["n"], len(gs))
        self.assertEqual(out["leg"]["sided"], "one")
        self.assertEqual(out["seed"], 113009)
        self.assertGreater(out["leg"]["rho_w"], 0.5)
        self.assertFalse(out["gating"])
        self.assertIn(out["band_reading_H7"], S.VERDICTS)

    def test_cli_refuses_locked_dirs_and_overwrite(self):
        for d in ("prereg", "anchor", "scripts", "lock", "registries", "data"):
            with self.assertRaises(SystemExit):
                AC.main(["--out", str(PHASE / d / "x.json")])
        with tempfile.TemporaryDirectory() as t:
            p = Path(t) / "out.json"
            p.write_text("{}")
            with self.assertRaises(SystemExit):
                AC.main(["--out", str(p)])

    def test_cli_writes_once_with_hashes(self):
        with tempfile.TemporaryDirectory() as t:
            t = Path(t)
            recs = t / "r.jsonl"
            recs.write_text("\n".join(json.dumps(r) for r in [rec("A", page()), rec("B", page(status=301))]))
            sd = t / "s.csv"
            sd.write_text("substrate,brand_id,phantom,SDRI_kg\nv19,A,0,33.3\n")
            dom = t / "d.csv"
            with open(dom, "w", newline="") as f:
                w = csv.writer(f)
                w.writerow(["substrate", "brand_id", "brand", "coder_key", "status", "domain", "aliases", "source",
                            "ambiguity", "runner_decision"])
                w.writerow(["v19", "A", "A", "A", "RESOLVED", "x.test", "", "s", "", ""])
            out = t / "o.json"
            AC.main(["--records", str(recs), "--sdri", str(sd), "--domains", str(dom), "--out", str(out)])
            d = json.loads(out.read_text())
            self.assertEqual(d["inputs"]["records"][1], hashlib.sha256(recs.read_bytes()).hexdigest())
            self.assertTrue(d["inputs"]["test_only"])
            self.assertEqual(d["AQ4"]["status"], "NOT_COMPUTED")
            self.assertEqual(d["S_KG"]["status"], "NOT_COMPUTED")


FAKE_SCORER = '''import sys, json
a = sys.argv[1:]
out = a[a.index("--out") + 1]
if "--fail" in a:
    sys.exit(3)
open(out, "w").write(json.dumps({"stage": a[a.index("--stage") + 1]}))
print("fake scorer ran")
'''


class TestRunStage(unittest.TestCase):
    def setUp(self):
        self.t = tempfile.TemporaryDirectory()
        self.d = Path(self.t.name)
        self.scorer = self.d / "fake_scorer.py"
        self.scorer.write_text(FAKE_SCORER)
        (self.d / "coded").mkdir()
        (self.d / "coded" / "v19_phase_b.csv").write_text("x\n")
        (self.d / "t4.jsonl").write_text('{"a": 1}\n')
        (self.d / "bt.csv").write_text("b\n")
        self.out = self.d / "v.json"

    def tearDown(self):
        self.t.cleanup()

    def args(self, stage, *extra):
        return ["--", "--stage", stage, "--t4", str(self.d / "t4.jsonl"), "--coded", str(self.d / "coded"),
                "--brand-table", str(self.d / "bt.csv"), "--out", str(self.out), *extra]

    def test_c1_records_hashes_before_and_output_after(self):
        self.assertEqual(RS.main(self.args("C1"), scorer=self.scorer), 0)
        r = json.loads((self.d / "v1_13_inputs_C1.json").read_text())
        self.assertEqual(r["inputs"]["t4_raw"]["sha256"], hashlib.sha256(b'{"a": 1}\n').hexdigest())
        self.assertTrue(r["inputs"]["coded"]["v19_phase_b.csv"]["exists"])
        self.assertFalse(r["inputs"]["coded"]["v19_phase_a.csv"]["exists"])
        self.assertFalse(r["verdict_file_before"]["exists"])
        self.assertEqual(r["verdict_file_after"]["sha256"], hashlib.sha256(self.out.read_bytes()).hexdigest())
        self.assertEqual(r["scorer_exit"], 0)
        self.assertNotIn("sdri", r["inputs"])
        with self.assertRaises(SystemExit):                                       # one record per stage
            RS.main(self.args("C1"), scorer=self.scorer)

    def test_c2_records_sdri_presence_and_hash(self):
        sd = self.d / "sdri.csv"
        RS.main(self.args("C2", "--sdri", str(sd)), scorer=self.scorer)
        r = json.loads((self.d / "v1_13_inputs_C2.json").read_text())
        self.assertFalse(r["inputs"]["sdri"]["part2_collected_at_c2_start"])
        (self.d / "v1_13_inputs_C2.json").unlink()
        sd.write_text("substrate\n")
        RS.main(self.args("C2", "--sdri", str(sd)), scorer=self.scorer)
        r = json.loads((self.d / "v1_13_inputs_C2.json").read_text())
        self.assertTrue(r["inputs"]["sdri"]["part2_collected_at_c2_start"])
        self.assertEqual(r["inputs"]["sdri"]["sha256"], hashlib.sha256(b"substrate\n").hexdigest())

    def test_refused_run_does_not_block_the_record(self):
        self.assertEqual(RS.main(self.args("C1", "--fail", "x"), scorer=self.scorer), 3)
        self.assertFalse((self.d / "v1_13_inputs_C1.json").exists())
        self.assertEqual(len(list(self.d.glob("v1_13_inputs_C1_exit3_*.json"))), 1)

    def test_needs_a_stage(self):
        with self.assertRaises(SystemExit):
            RS.main(["--", "--t4", "x"], scorer=self.scorer)


class TestC2Extras(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inp = synthetic_t4()
        cls.doc = json.loads(json.dumps(S.stage_c1(cls.inp, n_perm=0, n_boot=0, sensitivities=False), default=str))

    def test_s6_without_aliases_reproduces_the_primary_verdicts(self):
        out = CX.extras(self.inp, self.doc, aliases={}, n_perm=0)
        self.assertEqual(out["S6_verified_D_b"]["verdict_changes"], {})
        self.assertEqual(out["S6_verified_D_b"]["n_rated"], self.doc["MQ"]["MQ5"]["n_rated"])
        self.assertEqual(out["S7_legacy_t3"]["status"], "NOT_COMPUTED")
        self.assertEqual(out["MQ2_kept"]["status"], "NOT_APPLICABLE")

    def test_s6_alias_counts_as_own_domain(self):
        k = ("v19", "B1")
        base = CX.extras(self.inp, self.doc, aliases={}, n_perm=0)
        out = CX.extras(self.inp, self.doc, aliases={k: {"rtings.com"}}, n_perm=0)   # every answer retrieves it
        self.assertEqual(out["S6_verified_D_b"]["aliases"], {"v19|B1": ["rtings.com"]})
        self.assertNotEqual(out["S6_verified_D_b"]["rho"], base["S6_verified_D_b"]["rho"])

    def test_aliases_from_audit_records(self):
        units = self.inp["units"]
        recs = [{"substrate": "v19", "brand_id": "B1", "verified_alias": "b1-us.test",
                 "kg": {"status": "chosen", "qid": "Q1", "p856": ["https://www.b1-global.test/"]}},
                {"substrate": "v19", "brand_id": "B2", "kg": {"status": "tie", "qid": None,
                                                              "tied_p856": {"Q7": ["https://b2-x.test/en"]}}},
                {"substrate": "v19", "brand_id": "B3", "verified_alias": "v19-b3.test", "kg": {"status": "none"}}]
        sdri = [{"substrate": "v19", "brand_id": "B1", "qid": "Q1"}, {"substrate": "v19", "brand_id": "B2", "qid": "Q7"},
                {"substrate": "v19", "brand_id": "B3", "qid": ""}]
        al = CX.aliases_from_audit(recs, sdri, units, S.load_classes()["multi_suffix"])
        self.assertEqual(al, {("v19", "B1"): {"b1-us.test", "b1-global.test"}, ("v19", "B2"): {"b2-x.test"}})

    def test_s7_cited_primary_baseline_and_mq2_both_ways(self):
        profiles = [{"wave": "t3", "substrate": S.CODER_SUB[k[0]], "brand": u["coder_key"], "P": str(i),
                     "C_star": str(100 - i), "rated": "1"} for i, (k, u) in enumerate(sorted(self.inp["units"].items()))]
        doc = json.loads(json.dumps(self.doc))
        doc["dropped_models"] = [S.GPT6]
        doc["panel_models"] = [m for m in S.PANELS["N3"] if m != S.GPT6]
        doc["MQ"]["MQ2"][S.GPT6]["dropped_from_g_star"] = True
        out = CX.extras(self.inp, doc, aliases=None, profiles=profiles, n_perm=0)
        self.assertEqual(set(out["S7_legacy_t3"]["verdicts"]), set(S.GATE_LEGS))
        self.assertEqual(out["S6_verified_D_b"]["status"], "NOT_COMPUTED")
        self.assertEqual(out["MQ2_kept"]["models_kept"], [S.GPT6])
        self.assertIn("v19|claude-fable-5-2", out["baseline_cited_set_all_N3"]["per_substrate_model"])
        self.assertNotIn(f"v19|{S.GPT6}", out["baseline_primary_panel"]["per_substrate_model"])
        self.assertIn(f"v19|{S.GPT6}", out["baseline_cited_set_all_N3"]["per_substrate_model"])

    def test_primary_baseline_equals_locked_baseline_without_drops(self):
        out = CX.extras(self.inp, self.doc, aliases=None, n_perm=0)
        self.assertEqual(out["baseline_primary_panel"], self.doc["baseline"])


class TestAddendum(unittest.TestCase):
    def test_frozen_text_unchanged_at_head(self):
        fc = WA.frozen_check("HEAD")
        self.assertEqual(fc["differ_from_lock_commit"], [])
        self.assertEqual(fc["files"], 22)

    def test_dry_run_and_refusals(self):
        r = subprocess.run([sys.executable, str(POST / "write_part2_addendum_v1_13.py"), "--ref", "HEAD", "--dry-run"],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("TEST_ONLY", r.stdout)
        r = subprocess.run([sys.executable, str(POST / "write_part2_addendum_v1_13.py"), "--ref", "062b94a",
                            "--dry-run"], capture_output=True, text=True)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("REFUSED", r.stderr + r.stdout)


if __name__ == "__main__":
    unittest.main()
