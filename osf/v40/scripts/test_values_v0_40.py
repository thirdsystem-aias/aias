#!/usr/bin/env python3
"""Tests for values_v0_40.py (the v0.40 values file). Run: python3 osf/v40/scripts/test_values_v0_40.py
Reads the repo's real scoring outputs (read only); refusal tests run in a temporary directory."""
import json
import math
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import values_v0_40 as VV  # noqa: E402

ROOT = VV.ROOT
DOC = VV.build(ROOT)
VALS = DOC["values"]


def load(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


class SourceMatch(unittest.TestCase):
    def test_every_file_value_equals_its_source_path(self):
        cache = {}
        n = 0
        for key, e in VALS.items():
            s = e["source"]
            if "file" not in s:
                continue
            src = cache.setdefault(s["file"], load(s["file"]))
            got = VV.resolve(src, s["path"])
            self.assertEqual(type(got), type(e["value"]), key)
            self.assertEqual(got, e["value"], key)
            n += 1
        self.assertGreater(n, 2000)

    def test_every_scalar_in_the_sources_is_present(self):
        have = {(e["source"]["file"], tuple(e["source"]["path"])) for e in VALS.values() if "file" in e["source"]}
        for name in ("verdicts", "audit", "manifest"):
            rel = VV.REL[name]
            for path, val in VV.walk(load(rel)):
                if isinstance(val, list) or (path and path[-1] in VV.SKIP_LEAVES):
                    continue
                self.assertIn((rel, tuple(path)), have, f"{rel} {path}")

    def test_display_is_the_rule_applied_to_the_value(self):
        for key, e in VALS.items():
            self.assertIn(e["rule"], VV.RULES, key)
            self.assertEqual(e["rule_text"], VV.RULES[e["rule"]], key)
            self.assertEqual(VV.display(e["rule"], e["value"]), e["display"], key)

    def test_every_hypothesis_verdict_and_manipulation_check(self):
        v = load(VV.REL["verdicts"])
        for h in VV.HYPOTHESES:
            self.assertEqual(VALS[f"{h}.verdict"]["value"], v[h]["verdict"])
        for mc, rec in v["manipulation_checks"].items():
            self.assertEqual(VALS[f"manipulation_checks.{mc}.pass"]["value"], rec["pass"], mc)
        fails = [mc for mc, rec in v["manipulation_checks"].items() if not rec["pass"]]
        for mc in fails:                                   # failures are carried, not dropped
            self.assertEqual(VALS[f"manipulation_checks.{mc}.pass"]["display"], "no")


class Computed(unittest.TestCase):
    def test_counts_from_the_raw_file_and_manifest(self):
        recs = [json.loads(l) for l in (ROOT / VV.REL["raw"]).read_text(encoding="utf-8").splitlines() if l.strip()]
        self.assertEqual(VALS["acquisition.records_total"]["value"], len(recs))
        man = load(VV.REL["manifest"])
        self.assertEqual(VALS["coding.answers"]["value"], man["answers_coded"])
        self.assertEqual(VALS["coding.mentions"]["value"], VV.csv_rows(ROOT / VV.REL["mentions"]))
        self.assertEqual(VALS["coding.answers"]["value"], VV.csv_rows(ROOT / VV.REL["coded"]))
        by = sum(e["value"] for k, e in VALS.items() if k.startswith("acquisition.records.") and k.count(".") == 3)
        self.assertEqual(by, len(recs))

    def test_costs(self):
        recs = [json.loads(l) for l in (ROOT / VV.REL["raw"]).read_text(encoding="utf-8").splitlines() if l.strip()]
        # independent of the guard code: the cost_usd field written on each raw line at collection time
        self.assertTrue(math.isclose(VALS["cost.collection_usd"]["value"], sum(r["cost_usd"] for r in recs),
                                     abs_tol=1e-9))
        parts = VALS["cost.prelock_check_usd"]["value"] + VALS["cost.technical_check_usd"]["value"]
        self.assertTrue(math.isclose(parts, VALS["cost.prelock_total_usd"]["value"], abs_tol=1e-12))
        acq = VALS["cost.judge_reserve_usd"]["value"] + parts + VALS["cost.collection_usd"]["value"]
        self.assertTrue(math.isclose(acq, VALS["cost.acquisition_recorded_usd"]["value"], abs_tol=1e-9))
        self.assertEqual(VALS["cost.audit_usd"]["value"], load(VV.REL["audit"])["spent_usd"])
        self.assertTrue(math.isclose(VALS["cost.paper_total_usd"]["value"],
                                     acq + VALS["cost.audit_usd"]["value"], abs_tol=1e-9))

    def test_acquisition_cost_matches_the_deviations_record(self):
        # DEVIATIONS.md (audit entry, written before this script) states the recorded spend in prose
        dev = (ROOT / "osf/v40/DEVIATIONS.md").read_text(encoding="utf-8")
        self.assertIn(VALS["cost.acquisition_recorded_usd"]["display"] + " was recorded at the end of the collection",
                      dev)

    def test_audit_kappas(self):
        a = load(VV.REL["audit"])
        self.assertEqual(VALS["audit.threshold.kappa"]["value"],
                         a["agreement"]["consensus_vs_rule"]["gone_flag"]["all"]["kappa"])
        self.assertEqual(VALS["audit.threshold.met"]["value"], a["threshold"]["kappa"] >= a["threshold"]["kappa_min"])


class Rounding(unittest.TestCase):
    def test_half_up_not_bankers_or_binary(self):
        self.assertEqual(VV.fmt_usd(0.125), "$0.13")      # round() gives 0.12
        self.assertEqual(VV.fmt_usd(2.675), "$2.68")      # round() gives 2.67 (binary)
        self.assertEqual(VV.fmt_dec(0.0005, 3), "0.001")
        self.assertEqual(VV.fmt_dec(-0.2865, 3), "-0.287")
        self.assertEqual(VV.fmt_pct(0.0625), "6.3%")
        self.assertEqual(VV.fmt_pct(0.125), "12.5%")
        self.assertEqual(VV.fmt_pct(96.03004291845494, already_percent=True), "96.0%")

    def test_p_values(self):
        self.assertEqual(VV.fmt_p(1.4e-115), "< 0.001")
        self.assertEqual(VV.fmt_p(0.001), "0.001")
        self.assertEqual(VV.fmt_p(0.0334966503349665), "0.033")
        self.assertEqual(VV.fmt_p(0.9995), "> 0.999")
        self.assertEqual(VV.fmt_p(0.999), "0.999")

    def test_ints_bools_null_text_thresholds(self):
        self.assertEqual(VV.display("INT", 27647), "27,647")
        self.assertEqual(VV.display("BOOL", False), "no")
        self.assertEqual(VV.display("NULL", None), "n/a")
        self.assertEqual(VV.display("TEXT", "PARTIAL"), "PARTIAL")
        self.assertEqual(VV.display("THRESH", 0.8), "0.8")

    def test_rule_choice(self):
        self.assertEqual(VV.rule_for(["H_Flag", "ghost_rate"], 0.5), "PCT")
        self.assertEqual(VV.rule_for(["H_Flag", "p_fisher"], 0.5), "P")
        self.assertEqual(VV.rule_for(["H_Decay", "rho"], -0.5), "DEC3")
        self.assertEqual(VV.rule_for(["thresholds", "flag_rate"], 0.8), "THRESH")
        self.assertEqual(VV.rule_for(["x", "share", "B6"], 0.5), "PCT")
        self.assertEqual(VV.rule_for(["spent_usd"], 6.1), "USD")
        self.assertEqual(VV.rule_for(["seed"], 4040), "THRESH")


class Refusal(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="v040_values_test_"))

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _copy_inputs(self, skip=()):
        for name, rel in VV.REL.items():
            if name in skip:
                continue
            (self.tmp / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / rel, self.tmp / rel)

    def _outputs_absent(self):
        return not (self.tmp / VV.OUT_JSON).exists() and not (self.tmp / VV.OUT_MD).exists()

    def test_refuses_without_verdicts(self):
        self._copy_inputs(skip=("verdicts",))
        with self.assertRaises(VV.Refused):
            VV.build(self.tmp)
        self.assertEqual(VV.main([], root=self.tmp, out_root=self.tmp), 2)
        self.assertTrue(self._outputs_absent())

    def test_refuses_on_empty_tree(self):
        self.assertEqual(VV.main([], root=self.tmp, out_root=self.tmp), 2)
        self.assertTrue(self._outputs_absent())

    def test_refuses_without_a_hypothesis_or_its_verdict(self):
        self._copy_inputs()
        p = self.tmp / VV.REL["verdicts"]
        v = json.loads(p.read_text(encoding="utf-8"))
        del v["H_Search"]
        p.write_text(json.dumps(v), encoding="utf-8")
        self.assertEqual(VV.main([], root=self.tmp, out_root=self.tmp), 2)
        v = load(VV.REL["verdicts"])
        v["H_Flag"]["verdict"] = None
        p.write_text(json.dumps(v), encoding="utf-8")
        self.assertEqual(VV.main([], root=self.tmp, out_root=self.tmp), 2)
        p.write_text("{not json", encoding="utf-8")
        self.assertEqual(VV.main([], root=self.tmp, out_root=self.tmp), 2)
        self.assertTrue(self._outputs_absent())

    def test_refuses_when_coded_file_differs_from_manifest(self):
        self._copy_inputs()
        with open(self.tmp / VV.REL["mentions"], "a", encoding="utf-8") as f:
            f.write("extra,row\n")
        self.assertEqual(VV.main([], root=self.tmp, out_root=self.tmp), 2)
        self.assertTrue(self._outputs_absent())

    def test_builds_in_a_copy_identically(self):
        self._copy_inputs()
        doc = VV.build(self.tmp)
        self.assertEqual(doc["values"], DOC["values"])


class Output(unittest.TestCase):
    def test_deterministic(self):
        self.assertEqual(VV.to_json(VV.build(ROOT)), VV.to_json(DOC))
        self.assertEqual(VV.to_md(VV.build(ROOT)), VV.to_md(DOC))

    def test_committed_files_are_current(self):
        self.assertEqual((ROOT / VV.OUT_JSON).read_text(encoding="utf-8"), VV.to_json(DOC))
        self.assertEqual((ROOT / VV.OUT_MD).read_text(encoding="utf-8"), VV.to_md(DOC))

    def test_inputs_unchanged_by_the_build(self):
        out = subprocess.run(["git", "-C", str(ROOT), "status", "--porcelain", "--", *VV.REL.values()],
                             capture_output=True, text=True)
        self.assertEqual(out.stdout.strip(), "")

    def test_fill(self):
        t = VV.fill("ghost rate {{v:H_Flag.ghost_rate}}, kappa {{v: audit.threshold.kappa }}", DOC)
        self.assertEqual(t, f"ghost rate {VALS['H_Flag.ghost_rate']['display']}, kappa "
                            f"{VALS['audit.threshold.kappa']['display']}")
        with self.assertRaises(KeyError):
            VV.fill("{{v:H_Nope.x}}", DOC)


if __name__ == "__main__":
    unittest.main(verbosity=1)
