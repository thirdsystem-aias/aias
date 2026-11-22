"""Tests for sva_sample_replace_v1_11.py (v1.11 DEVIATIONS Entry 1). Run: python3 -m pytest
scripts/test_sva_sample_replace_v1_11.py (or python3 -m unittest). Reads the locked files read-only."""
import hashlib, sys, tempfile, unittest
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sva_sample_replace_v1_11 as R  # noqa: E402
import score_v1_11 as S  # noqa: E402

EXPECTED_SHA256 = "94d120f4a752d72f4fe96f90523fb3be663b3feba92fc3ff0dcdd2a11da0295e"


def _u(uid, brand, frame="q1", wave="t2", model="m1", judged=True, text="x", block="F", cat="c"):
    return {"unit_id": uid, "block": block, "category": cat, "wave": wave, "model": model, "frame": frame,
            "brand": brand.lower(), "brand_display": brand, "judged": judged, "text": text, "question": "q"}


class Locked(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.units, cls.ids = R.load_locked()
        cls.by_id = {u["unit_id"]: u for u in cls.units}
        cls.res = R.replace(cls.units, cls.ids)

    def test_locked_sample_reproduced_from_unit_table(self):
        orig = sorted((self.by_id[i] for i in self.ids), key=lambda u: u["unit_id"])
        self.assertEqual(S.human_csv_bytes(orig), R.SAMPLE.read_bytes())
        self.assertEqual(len(orig), 566)

    def test_screen(self):
        scr = self.res["screen"]
        self.assertEqual([self.by_id[i]["brand_display"] for i in scr["subject"]], ["Denon", "Denon"])
        self.assertEqual(sorted(t for v in scr["mention_only"].values() for t in v), ["AKG", "AKG", "JBL"])

    def test_new_sample_size_strata_and_no_sg_brand(self):
        new = self.res["sample"]
        self.assertEqual(len(new), 566)
        orig = [self.by_id[i] for i in self.ids]
        self.assertEqual(Counter(map(R.stratum, orig)), Counter(map(R.stratum, new)))
        self.assertFalse([u for u in new if R.is_sg_brand(u["brand_display"])])

    def test_replacements_eligible(self):
        for d in self.res["draws"]:
            x, y = self.by_id[d["out"]], self.by_id[d["in"]]
            self.assertEqual(R.stratum(x), R.stratum(y))
            self.assertTrue(y["judged"])
            self.assertNotIn(y["unit_id"], self.ids)
            self.assertFalse(R.names_sg(y))
            self.assertFalse(R.is_sg_brand(y["brand_display"]))

    def test_deterministic_and_expected_hash(self):
        again = R.replace(self.units, self.ids)
        a, b = S.human_csv_bytes(self.res["sample"]), S.human_csv_bytes(again["sample"])
        self.assertEqual(a, b)
        self.assertEqual(hashlib.sha256(a).hexdigest(), EXPECTED_SHA256)

    def test_locked_files_unchanged(self):
        self.assertEqual(R.sha256_file(R.SAMPLE), R.SAMPLE_SHA256)
        self.assertEqual(R.sha256_file(R.UNITS), R.UNITS_SHA256)


class Synthetic(unittest.TestCase):
    def test_prefers_brand_under_cap_then_frame(self):
        units = [_u("a1", "Denon", "q2"), _u("b1", "Alpha", "q1"), _u("b2", "Alpha", "q1"),
                 _u("b3", "Alpha", "q1"), _u("c1", "Beta", "q2"), _u("c2", "Gamma", "q1"),
                 _u("c3", "Delta", "q2", text="pairs with JBL"), _u("c4", "Eps", "q2", judged=False),
                 _u("c5", "Zeta", "q2", model="m2")]
        res = R.replace(units, {"a1", "b1", "b2", "b3"})
        self.assertEqual(res["draws"][0]["in"], "c1")         # under cap, same frame, eligible, same stratum
        self.assertFalse(res["draws"][0]["cap_relaxed"])

    def test_cap_relaxed_minimally(self):
        units = [_u("a1", "Denon")] + [_u(f"b{i}", "Alpha") for i in range(5)] + \
                [_u(f"c{i}", "Beta") for i in range(5)]
        res = R.replace(units, {"a1", "b0", "b1", "b2", "c0", "c1", "c2", "c3"})
        self.assertTrue(res["draws"][0]["cap_relaxed"])
        self.assertTrue(res["draws"][0]["in"].startswith("b"))   # Alpha has 3, Beta 4: fewest wins

    def test_no_candidate_leaves_unit_out(self):
        res = R.replace([_u("a1", "Denon"), _u("b1", "Marantz")], {"a1"})
        self.assertIsNone(res["draws"][0]["in"])
        self.assertEqual(res["sample"], [])

    def test_common_words_not_flagged(self):
        self.assertEqual(R.sg_terms_in("a definitive statement; to revel in infinity; Denona"), [])
        self.assertEqual(R.sg_terms_in("Polk Audio and B&W, Bowers and Wilkins, Harman Kardon"),
                         ["Bowers & Wilkins", "Harman", "Harman Kardon", "Polk Audio"])


if __name__ == "__main__":
    unittest.main()
