"""Tests of score_ai_sens_v0_62.py (S-Trans, S-AliasAI; DEVIATIONS Entry 2 (b)-(d)) on synthetic coded tables."""
import hashlib
import json
import sys
import unittest
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import score_v0_62 as S  # noqa: E402
import score_ai_sens_v0_62 as X  # noqa: E402

SIZES = {"v0.19": 16, "v0.20": 24, "v0.21": 24, "v0.22": 24, "v0.23": 24}
QS = {"v0.19": [f"phase_b__q{i}_x" for i in range(1, 7)]}
QS.update({s: [f"q{i}" for i in range(1, 7)] for s in ("v0.20", "v0.21", "v0.22", "v0.23")})
NP = NB = 99


def units():
    u = [("v0.19", "Denon")] + [("v0.19", f"h{i}") for i in range(15)]
    for s, n in list(SIZES.items())[1:]:
        u += [(s, f"{s}-b{i}") for i in range(n)]
    return u


def rows(U, pi, seed, lang="es", drop_model=None, pi_q=None):
    """Coded Phase B rows with v0.62 call ids 'lang|sub|B|probe_id|model|S0|run'; pi_q(unit, q) overrides pi."""
    rng = np.random.default_rng(seed)
    out = []
    for m in S.MODELS:
        for r in S.RUNS:
            for s in SIZES:
                for qi, q in enumerate(QS[s]):
                    if drop_model == m and qi > 0:
                        continue
                    cid = f"{lang}|{X.sub_key(s)}|B|{q}|{m}|S0|{r}"
                    for u in U:
                        if u[0] == s:
                            p = pi_q(u, qi) if pi_q else pi[u]
                            out.append({"call_id": cid, "substrate": s, "brand": u[1], "model": m,
                                        "condition": "S0", "run": r, "mentioned": int(rng.random() < p)})
    return out


def english(U, seed=1):
    rng = np.random.default_rng(seed)
    pi = {u: float(rng.uniform(0.05, 0.95)) for u in U}
    B = rows(U, pi, seed + 100, lang="en")
    V = S.unit_values(U, B)
    return pi, B, {u: {"pi": V[u]["pi"], "phi": V[u]["phi"]} for u in U}


def dump(v):
    return json.dumps(S._clean(v), indent=1, ensure_ascii=False, sort_keys=False)


class LockedScorer(unittest.TestCase):
    def test_score_v0_62_is_the_locked_file(self):
        man = (HERE.parents[1] / "prereg" / "LOCK_MANIFEST_v0_62.sha256").read_text(encoding="utf-8")
        locked = {ln.split()[1]: ln.split()[0] for ln in man.splitlines() if ln.strip()}
        sha = hashlib.sha256((HERE.parent / "score_v0_62.py").read_bytes()).hexdigest()
        self.assertEqual(locked["osf/v62/scripts/score_v0_62.py"], sha)


class Kernels(unittest.TestCase):
    def test_phi_m_f_equals_locked_at_6(self):
        rng = np.random.default_rng(3)
        for _ in range(300):
            k = rng.integers(0, 7, size=3)
            self.assertEqual(X.phi_m_f(k, 6), S.phi_m(k))

    def test_unit_values_f_equals_locked_at_6(self):
        U = units()
        pi, _B, _en = english(U)
        for B in (rows(U, pi, 7), rows(U, pi, 8, drop_model="gpt-6-astra")):
            self.assertEqual(X.unit_values_f(U, B, X.f_by_sub(set())), S.unit_values(U, B))

    def test_question_of(self):
        self.assertEqual(X.question_of({"call_id": "ko|v20|B|q3|gpt-6-astra|S0|2"}), ("v20", "q3"))
        self.assertEqual(X.question_of({"probe_id": "q1", "substrate": "v0.21"}), ("v21", "q1"))
        with self.assertRaises(ValueError):
            X.question_of({"call_id": "x|y"})
        self.assertEqual(X.removed_set(["v20|q1", ("v0.21", "q2")]), {("v20", "q1"), ("v21", "q2")})

    def test_reduced_question_set(self):
        U = units()
        pi, _B, _en = english(U)
        B = rows(U, pi, 7)
        rem = X.removed_set(["v20|q1", "v20|q2"])
        R = X.drop_questions(B, rem)
        V = X.unit_values_f(U, R, X.f_by_sub(rem))
        u = ("v0.20", "v0.20-b0")
        k = [[sum(r["mentioned"] for r in R if r["model"] == m and int(r["run"]) == run and r["brand"] == u[1])
              for m in S.MODELS] for run in S.RUNS]
        phis = [X.phi_m_f(kk, 4)[0] for kk in k]
        vals = [p for p in phis if p is not None]
        if len(vals) >= 2:
            self.assertAlmostEqual(V[u]["phi"], float(np.mean(vals)))
        self.assertAlmostEqual(V[u]["pi"], sum(sum(kk) for kk in k) / (3 * 3 * 4))
        self.assertEqual(S.unit_values(U, R)[u]["partition"], "undefined")   # the locked F = 6 would see missing runs
        self.assertEqual(S.dropped_models(R, 28), [])


class ByteIdentical(unittest.TestCase):
    """Entry 2 (d): no confirmatory statistic, threshold or unit set changes; default behaviour byte-identical."""

    @classmethod
    def setUpClass(cls):
        U = units()
        pi, en_B, en = english(U)
        rev = {u: 1.0 - pi[u] for u in U}
        cls.U, cls.pi, cls.en_B, cls.en = U, pi, en_B, en
        cls.B = {"es": rows(U, pi, 7), "ko": rows(U, rev, 8, "ko"), "zh": rows(U, pi, 9, "zh")}

    def test_default_is_byte_identical(self):
        for opt in ("A", "B", "C"):
            a = dump(S.score(self.U, self.en, self.B, n_perm=NP, n_boot=NB, option=opt))
            b = dump(X.score(self.U, self.en, self.B, n_perm=NP, n_boot=NB, option=opt))
            self.assertEqual(a.encode("utf-8"), b.encode("utf-8"), opt)

    def test_with_sensitivities_primary_unchanged(self):
        a = S.score(self.U, self.en, self.B, n_perm=NP, n_boot=NB, option="A")
        flags = {lg: {"flagged": ["v20|q1"], "strictly_flagged": []} for lg in S.LANGS}
        b = X.score(self.U, self.en, self.B, n_perm=NP, n_boot=NB, option="A", s_trans=flags, en_B=self.en_B,
                    s_alias_ai={"ko": self.B["es"]})
        self.assertEqual(set(b) - set(a), {"sensitivities_ai_check"})
        for k in a:
            self.assertEqual(dump(a[k]), dump(b[k]), k)

    def test_score_language_mirrors_locked_score(self):
        a = S.score(self.U, self.en, self.B, n_perm=NP, n_boot=NB, option="A")
        for lg in S.LANGS:
            t, s = X.score_language(lg, self.U, self.en, S.unit_values(self.U, self.B[lg]), self.B[lg], 30,
                                    option="A", n_perm=NP, n_boot=NB)
            self.assertEqual(dump(t), dump({k: v for k, v in a["tests"].items() if k.endswith("_" + lg)}))
            self.assertEqual(dump(s), dump({k: v for k, v in a["sensitivities"].items() if k.endswith("_" + lg)}))


class STrans(unittest.TestCase):
    def setUp(self):
        self.U = units()
        self.pi, self.en_B, self.en = english(self.U)
        self.B = {lg: rows(self.U, self.pi, 7 + i, lg) for i, lg in enumerate(S.LANGS)}

    def test_no_flags_equals_primary_on_recomputed_english(self):
        flags = {lg: {"flagged": [], "strictly_flagged": []} for lg in S.LANGS}
        v = X.score(self.U, self.en, self.B, n_perm=NP, n_boot=NB, option="A", s_trans=flags, en_B=self.en_B)
        ref = S.score(self.U, self.en, self.B, n_perm=NP, n_boot=NB, option="A")    # en was built from en_B
        st = v["sensitivities_ai_check"]["S-Trans"]["flagged"]
        for k in ("H_Lang_Presence_es", "H_Lang_Phi_ko", "H_Lang_Presence_zh"):
            self.assertEqual(dump(st["tests"][k]), dump(ref["tests"][k]), k)
        self.assertEqual(st["joint_reading"], ref["joint_reading"])
        self.assertEqual(st["presence_differs"], {"es": False, "ko": False, "zh": False})
        self.assertEqual(st["tests"]["H_Lang_Rank_es"]["verdict"], "NOT TESTED")

    def test_removed_category_and_counts(self):
        allv19 = [f"v19|{q}" for q in QS["v0.19"]]
        flags = {"es": {"flagged": allv19 + ["v20|q1"], "strictly_flagged": ["v20|q1"]},
                 "ko": {"flagged": [], "strictly_flagged": []}, "zh": {"flagged": [], "strictly_flagged": []}}
        v = X.score(self.U, self.en, self.B, n_perm=NP, n_boot=NB, option="A", s_trans=flags, en_B=self.en_B)
        f = v["sensitivities_ai_check"]["S-Trans"]["flagged"]
        self.assertEqual(f["tests"]["H_Lang_Presence_es"]["n"], 96)                # v0.19 has no question left
        self.assertNotEqual(f["tests"]["H_Lang_Presence_es"]["verdict"], "UNDETERMINED")   # n_b adjusted (23)
        self.assertEqual(f["removed"]["es"], sorted(allv19 + ["v20|q1"]))
        self.assertEqual(f["tests"]["H_Lang_Presence_ko"]["n"], 112)
        s = v["sensitivities_ai_check"]["S-Trans"]["strictly_flagged"]
        self.assertEqual(s["tests"]["H_Lang_Presence_es"]["n"], 112)
        self.assertEqual(v["tests"]["H_Lang_Presence_es"]["n"], 112)               # primary untouched

    def test_presence_differs(self):
        # KO: questions q1-q3 carry the English order, q4-q6 the reverse; flagging q4-q6 everywhere restores it
        rev = {u: 1.0 - self.pi[u] for u in self.U}
        ko = rows(self.U, self.pi, 11, "ko", pi_q=lambda u, qi: self.pi[u] if qi < 3 else rev[u])
        B = dict(self.B, ko=ko)
        fl = [f"{X.sub_key(s)}|{q}" for s in SIZES for q in QS[s][3:]]
        flags = {"es": {"flagged": [], "strictly_flagged": []}, "ko": {"flagged": fl, "strictly_flagged": fl},
                 "zh": {"flagged": [], "strictly_flagged": []}}
        v = X.score(self.U, self.en, B, n_perm=NP, n_boot=NB, option="A", s_trans=flags, en_B=self.en_B)
        st = v["sensitivities_ai_check"]["S-Trans"]["flagged"]
        self.assertNotEqual(v["tests"]["H_Lang_Presence_ko"]["verdict"], "CONFIRMED")
        self.assertEqual(st["tests"]["H_Lang_Presence_ko"]["verdict"], "CONFIRMED")
        self.assertTrue(st["presence_differs"]["ko"])

    def test_needs_english_rows(self):
        with self.assertRaises(ValueError):
            X.score(self.U, self.en, self.B, n_perm=NP, n_boot=NB, s_trans={"es": {}})


class SAliasAI(unittest.TestCase):
    def test_alias_ai_presence(self):
        U = units()
        pi, _B, en = english(U)
        B = {lg: rows(U, pi, 7 + i, lg) for i, lg in enumerate(S.LANGS)}
        rev = {u: 1.0 - pi[u] for u in U}
        v = X.score(U, en, B, n_perm=NP, n_boot=NB, option="A", s_alias_ai={"ko": rows(U, rev, 20, "ko"),
                                                                             "zh": B["zh"]})
        a = v["sensitivities_ai_check"]["S-AliasAI"]
        self.assertEqual(v["tests"]["H_Lang_Presence_ko"]["verdict"], "CONFIRMED")
        self.assertEqual(a["S-AliasAI_ko"]["verdict"], "FALSIFIED")
        self.assertTrue(a["S-AliasAI_ko"]["presence_differs"])
        self.assertFalse(a["S-AliasAI_zh"]["presence_differs"])
        self.assertEqual(dump({k: a["S-AliasAI_zh"][k] for k in ("rho_c", "p_perm", "n")}),
                         dump({k: v["tests"]["H_Lang_Presence_zh"][k] for k in ("rho_c", "p_perm", "n")}))
        with self.assertRaises(ValueError):
            X.score(U, en, B, n_perm=NP, n_boot=NB, s_alias_ai={"es": B["es"]})

    def test_alias_ai_aliaser(self):
        import code_v0_62 as C
        al, n = X.alias_ai_aliaser([["v22", "Toyota", "도요타"]])
        self.assertEqual(n, 1)
        self.assertNotIn("Toyota", al.canonicalise("도요타 자동차", "v22"))
        self.assertIn("Toyota", al.canonicalise("토요타 자동차", "v22"))
        self.assertIn("Toyota", C.Aliaser().canonicalise("도요타 자동차", "v22"))     # the primary coder keeps it
        with self.assertRaises(ValueError):
            X.alias_ai_aliaser([["v22", "Toyota", "없는별칭"]])


if __name__ == "__main__":
    unittest.main()
