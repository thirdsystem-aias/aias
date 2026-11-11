"""Tests of gate_p2_v0_62.py (r3): gate P2 with BOTH sides normalised (r1 open item 11), on synthetic English answers,
with the REAL certified matchers of v0.20-v0.22 (scripts/score_v2x.py in this tree, the same git blobs as at tag
v0.42-prereg-r1) and with v0.23's locked patterns. No network, no model; no t4 answer is read."""
import ast
import contextlib
import csv
import io
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import code_v0_62 as C  # noqa: E402
import gate_p2_v0_62 as G  # noqa: E402

ROOT = HERE.parents[3]
TABLE = HERE.parents[1] / "translations" / "brand_aliases_v0_62_r2.csv"
UNITS = {}
for _r in csv.DictReader(open(TABLE, encoding="utf-8")):
    UNITS.setdefault(_r["substrate"], []).append(_r["brand"])
CERTIFIED = ("scripts/score_v20.py", "scripts/score_v21.py", "scripts/score_v22.py", "scripts/score_v0_23.py")

ANSWERS = [
    ("v20", "Top picks: La Mer and Paula’s Choice (see https://www.paulaschoice.com/serum)."),
    ("v20", "Paula's Choice and CeraVe are dermatologist favourites; Estée Lauder too."),
    ("v21", "Try L’Oréal Paris or Maybelline."),
    ("v21", "LʼOréal Paris leads; ＮＡＲＳ is for professionals."),
    ("v22", "Mercedes-Benz, BMW and Rolls-Royce lead; Benz alone is a nickname."),
    ("v22", "Toyota’s Camry and Honda’s Civic; Porsche’s 911."),
]


def certified():
    sys.path.insert(0, str(ROOT / "scripts"))
    import score_v20
    import score_v21
    import score_v22
    return {"v20": score_v20.detect_mention, "v21": score_v21.detect_mention, "v22": score_v22.detect_mention}


def codes(match, sub, text):
    """Phase B coding as v0.42's coder does it for v0.20-v0.22: URLs removed, then detect_mention per registry brand."""
    t = C.strip_urls(text)
    return {b for b in UNITS[sub] if match[sub](t, b)}


def rec(sub, text, phase="B"):
    return {"call_id": f"en|{sub}|{phase}|q1|m|S0|1", "phase": phase, "substrate": sub, "text": text}


class CertifiedMatchers(unittest.TestCase):
    def test_modules_are_the_v042_locked_blobs(self):
        for f in CERTIFIED:
            a = subprocess.run(["git", "-C", str(ROOT), "rev-parse", f"v0.42-prereg-r1:{f}"], capture_output=True, text=True)
            if a.returncode != 0:
                self.skipTest("tag v0.42-prereg-r1 not available")
            b = subprocess.run(["git", "-C", str(ROOT), "hash-object", f], capture_output=True, text=True, check=True)
            self.assertEqual(a.stdout.strip(), b.stdout.strip(), f)

    def test_the_r1_issue_exists_in_the_certified_matchers(self):
        M = certified()
        self.assertFalse(M["v20"]("Try Paula’s Choice.", "Paula's Choice"))      # U+2019: not matched
        self.assertTrue(M["v20"]("Try Paula's Choice.", "Paula's Choice"))
        self.assertFalse(M["v21"]("LʼOréal Paris", "L'Oréal Paris"))             # U+02BC: not matched
        self.assertTrue(M["v21"]("L＇Oréal Paris", "L'Oréal Paris"))             # U+FF07: NFKD maps it already

    def test_v023_patterns_make_the_apostrophe_optional(self):
        tree = ast.parse((ROOT / "scripts/score_v0_23.py").read_text(encoding="utf-8"))
        pats = [ast.literal_eval(n.value) for n in tree.body if isinstance(n, ast.Assign)
                and any(getattr(t, "id", None) == "BRAND_PATTERNS" for t in n.targets)][0]
        for sid, text in (("S03", "jack daniel’s no. 7"), ("S11", "hendrick’s gin")):
            self.assertTrue(any(re.search(p, text) for p in pats[sid]), sid)


class GateP2(unittest.TestCase):
    def test_p2_passes_with_both_sides_normalised(self):
        M = certified()
        for sub, t in ANSWERS:
            pre, ref = G.pre_record(rec(sub, t))["text"], G.ref_record(rec(sub, t))["text"]
            self.assertEqual(codes(M, sub, pre), codes(M, sub, ref), t)

    def test_apostrophe_delta_is_reported_and_only_two_units(self):
        M = certified()
        delta = set()
        for sub, t in ANSWERS:
            ref = codes(M, sub, G.ref_record(rec(sub, t))["text"])
            raw = codes(M, sub, t)                              # what v0.42's locked code saw
            delta |= {(sub, b) for b in ref ^ raw}
        self.assertEqual(delta, {("v20", "Paula's Choice"), ("v21", "L'Oréal Paris")})
        self.assertTrue(delta <= G.APOSTROPHE_UNITS)

    def test_gate_is_sensitive_to_a_perturbed_pre_step(self):
        M = certified()
        real = C.prepare_text

        def broken(text, *a, **k):
            return real(text, *a, **k).replace("La Mer", "")
        sub, t = ANSWERS[0]
        with mock.patch.object(C, "prepare_text", broken):
            pre = G.pre_record(rec(sub, t))["text"]
        self.assertNotEqual(codes(M, sub, pre), codes(M, sub, G.ref_record(rec(sub, t))["text"]))

    def test_prepare_writes_both_sides_and_keeps_the_input(self):
        with tempfile.TemporaryDirectory() as d:
            raw = Path(d) / "raw.jsonl"
            rs = [rec("v20", "Paula’s Choice"), rec("v23", "Hendrick’s is a gin.", phase="A"),
                  rec("v21", "Yes’ L’Oréal Paris", phase="A")]
            raw.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rs), encoding="utf-8")
            before = raw.read_bytes()
            self.assertEqual(G.prepare(raw, Path(d) / "out"), 3)
            self.assertEqual(raw.read_bytes(), before)
            rd = lambda n: [json.loads(x) for x in (Path(d) / "out" / n).read_text(encoding="utf-8").splitlines()]
            pre, ref = rd("p2_pre.jsonl"), rd("p2_ref.jsonl")
            self.assertEqual(pre[0]["text"].strip(), "Paula's Choice")
            self.assertEqual(ref[0]["text"], "Paula's Choice")
            self.assertEqual((pre[1]["text"], ref[1]["text"]), (rs[1]["text"], rs[1]["text"]))   # v0.23 Phase A as written
            self.assertEqual(pre[2]["text"], ref[2]["text"])                                     # v0.21 Phase A: step 1 only
            self.assertEqual([p["text_original"] for p in pre], [r["text"] for r in rs])


class Compare(unittest.TestCase):
    HB = ["call_id", "substrate", "brand", "model", "condition", "run", "probe_id", "frame_id", "mentioned"]
    HA = ["call_id", "substrate", "brand", "brand_id", "model", "condition", "run", "probe_id", "label", "recognized"]

    def _write(self, d, rows_b, rows_a=()):
        d.mkdir(parents=True, exist_ok=True)
        for name, head, rows in (("v20_phase_b.csv", self.HB, rows_b), ("v20_phase_a.csv", self.HA, rows_a)):
            with open(d / name, "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(head)
                w.writerows(rows)

    def test_pass_fail_and_apostrophe_delta(self):
        b = [["en|v20|B|q1|m|S0|1", "v0.20", "Paula's Choice", "m", "S0", "1", "q1", "", "1"],
             ["en|v20|B|q1|m|S0|1", "v0.20", "La Mer", "m", "S0", "1", "q1", "", "0"]]
        a = [["en|v20|A|P1|m|S0|1", "v0.20", "La Mer", "P1", "m", "S0", "1", "P1", "yes", "1"]]
        with tempfile.TemporaryDirectory() as t:
            t = Path(t)
            self._write(t / "pre", b, a)
            self._write(t / "ref", b, a)
            self.assertEqual(G.p2(t / "pre", t / "ref")["result"], "PASS")
            b2 = [list(x) for x in b]
            b2[1][-1] = "1"
            self._write(t / "ref2", b2, a)
            r = G.p2(t / "pre", t / "ref2")
            self.assertEqual(r["result"], "FAIL")
            self.assertEqual(r["pre_vs_ref"]["by_unit"], {"v0.20 | La Mer": 1})
            self._write(t / "ref3", b, [])
            self.assertEqual(G.p2(t / "pre", t / "ref3")["pre_vs_ref"]["only_in_first"], 1)
            lk = [list(x) for x in b]
            lk[0][-1] = "0"                                  # the locked code missed Paula’s Choice
            self._write(t / "locked", lk, a)
            r = G.p2(t / "pre", t / "ref", t / "locked")
            self.assertEqual(r["result"], "PASS")
            d = r["apostrophe_delta_ref_vs_locked"]
            self.assertEqual((d["different"], d["only_apostrophe_units"]), (1, True))
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(G.main(["--compare", str(t / "pre"), str(t / "ref2")]), 2)


if __name__ == "__main__":
    unittest.main()
