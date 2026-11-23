#!/usr/bin/env python3
"""Builds the synthetic fixtures of the v1.21 scorer tests (no real data, no model call).

Run from the repository root (rewrites osf/methodology/v1_21/tests/fixtures/<world>/; deterministic):
  PYTHONDONTWRITEBYTECODE=1 python3 osf/methodology/v1_21/tests/fixtures/build_fixtures_v1_21.py

Each world mimics the t4 / t5 design (5 omnibus categories, 3 answering models x 6 questions x 3 runs = 54 S0
answers per category and wave) with 10 registry brands per category. A brand is named in an answer with its
own naming probability pi_b; P_S0 = 100 pi_b. J1's valence of a window = clip(round(0.9 tau_b + register of the
answer + model shift + noise)); J2 = J1 with occasional one-step disagreements. tau_b is the brand's latent tone:
  confirmed      tau independent of pi (permuted so that its within-category rank correlation with pi is ~0)
  falsified      tau = z(pi): tone tracks Presence
  marginal       tau = 0.45 z(pi) + independent part
  retest_fail    as confirmed at t4, an independent tau at t5 (H4 FALSIFIED, noise guard on)
  judge_noise    as confirmed, J2 unrelated to J1 (H1_t5 FALSIFIED, noise guard on)
  two_cats       as confirmed, only 2 categories (every pooled row UNDETERMINED)
Expected verdicts are not written into the fixtures; the tests state what each world must produce.
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "scripts"))
import score_v1_21 as T  # noqa: E402

CATS = ["v0.19", "v0.20", "v0.21", "v0.22", "v0.23"]
SPECIAL = {"v0.19": ["Denon"], "v0.20": ["Eucerin"], "v0.22": ["BMW", "Bentley", "Chevrolet"], "v0.23": ["S03"]}
MODELS = [("claude-fable-5-2", "anthropic", 0.3), ("gpt-6-astra", "openai", 0.0), ("gemini-4-argon", "google", -0.3)]
NB = 10
PERM_NULL = np.array([4, 9, 1, 6, 0, 8, 3, 5, 2, 7])   # tone ranks unrelated to Presence ranks
PERM_T5 = np.array([7, 2, 5, 3, 8, 0, 6, 1, 9, 4])     # retest_fail: a different tone order at t5
ROLES = {"J1": "claude-opus-5-5", "J2": "gpt-6.1-sol"}
WORLDS = {"confirmed": 121501, "falsified": 121502, "marginal": 121503, "retest_fail": 121504,
          "judge_noise": 121505, "two_cats": 121506}


def brands(cat):
    sp = SPECIAL.get(cat, [])
    return sp + [f"B{i:02d}" for i in range(1, NB - len(sp) + 1)]


def z(x):
    x = np.asarray(x, float)
    return (x - x.mean()) / x.std()


def latent(world, rng, pi):
    rk = np.argsort(np.argsort(pi))                           # rank of each brand's pi (0..9)
    base = z(rk)
    indep = z(PERM_NULL[rk])                                  # rank correlation with pi: -0.018 (checked in main)
    if world == "falsified":
        return base.copy(), base.copy()
    if world == "marginal":
        t = 0.45 * base + np.sqrt(1 - 0.45 ** 2) * indep
        return t, t
    if world == "retest_fail":
        return indep, z(PERM_T5[rk])
    return indep, indep


def build(world: str, seed: int, out: Path) -> None:
    rng = np.random.default_rng(seed)
    cats = CATS[:2] if world == "two_cats" else CATS
    rows = {"t4": [], "t5": []}
    pres = []
    for cat in cats:
        bs = brands(cat)
        pi = np.linspace(0.12, 0.80, NB)[rng.permutation(NB)]
        tau4, tau5 = latent(world, rng, pi)
        cstar = rng.uniform(40, 100, NB)
        for wv, tau in (("t4", tau4), ("t5", tau5)):
            for i, b in enumerate(bs):
                pres.append({"wave": wv, "category": cat, "brand": b, "P_S0": round(100 * pi[i] + rng.normal(0, 2), 4),
                             "C_star_S0": round(float(cstar[i] + rng.normal(0, 3)), 4)})
            for model, prov, shift in MODELS:
                for q in range(1, 7):
                    for run in range(1, 4):
                        aid = f"{wv} {cat}::{model}|q{q}|S0|{run}"
                        reg = rng.normal(0, 0.8)
                        named = [i for i in range(NB) if rng.random() < pi[i]]
                        for i in named:
                            v1 = int(np.clip(np.rint(0.9 * tau[i] + reg + shift + rng.normal(0, 0.6)), -2, 2))
                            if world == "judge_noise":
                                v2 = int(rng.integers(-2, 3))
                            else:
                                v2 = int(np.clip(v1 + (rng.choice([-1, 1]) if rng.random() < 0.15 else 0), -2, 2))
                            refers = rng.random() > 0.03
                            st1 = "JUDGE_FAIL" if rng.random() < 0.004 else "VALID"
                            if not refers:
                                v1 = v2 = 0
                            ev1 = refers and (v1 != 0 or rng.random() < 0.3)
                            ev2 = refers and (v2 != 0 or rng.random() < 0.3)
                            r = {"unit_id": f"{aid}#{bs[i]}", "wave": wv, "category": cat, "brand": bs[i],
                                 "answer_id": aid, "model": model, "provider": prov,
                                 "J1": (st1, v1, ev1, refers), "J2": ("VALID", v2, ev2, refers)}
                            if rng.random() < 0.05 and st1 == "VALID":
                                rep = int(np.clip(v1 + (rng.choice([-1, 1]) if rng.random() < 0.1 else 0), -2, 2))
                                r["J1rep"] = ("VALID", rep)
                                r["J2rep"] = ("VALID", v2)
                            if rng.random() < 0.02 and st1 == "VALID":
                                va = int(np.clip(v1 + rng.choice([-1, 1]), -2, 2)) if refers else 0
                                r["J1att"] = ("VALID", va, refers and (va != 0 or ev1), refers)
                            rows[wv].append(r)
    out.mkdir(parents=True, exist_ok=True)
    for wv, rs in rows.items():
        with open(out / f"unit_outcomes_{wv}.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f, lineterminator="\n")
            w.writerow(T.UNIT_COLS)
            for r in rs:
                line = [r[k] for k in ("unit_id", "wave", "category", "brand", "answer_id", "model", "provider")]

                def judge(t):
                    st, v, ev, rf = t
                    return [st, v, int(ev), int(rf)] if st == "VALID" else [st, "", "", ""]
                line += judge(r["J1"]) + judge(r["J2"])
                for k in ("J1rep", "J2rep"):
                    line += list(r[k]) if k in r else ["", ""]
                line += judge(r.get("J1att", r["J1"])) + judge(r["J2"])
                w.writerow(line)
    with open(out / "presence.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, ["wave", "category", "brand", "P_S0", "C_star_S0"], lineterminator="\n")
        w.writeheader()
        w.writerows(pres)
    (out / "fixture.json").write_text(json.dumps({"name": world, "seed": seed, "roles": ROLES,
                                                  "synthetic": True}, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    assert abs(np.corrcoef(np.arange(10), PERM_NULL)[0, 1]) < 0.02
    for world, seed in WORLDS.items():
        build(world, seed, HERE / world)
        print(f"built {world}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
