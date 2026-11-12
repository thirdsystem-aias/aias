#!/usr/bin/env python3
"""
score_v0_40.py -- AIAS(TM) v0.40 (US airlines and retail banks): rule-based coding and the six pre-registered tests.
Pre-registration: osf/v40/prereg/PRE_REGISTRATION_v0_40.md, sections 2 (hypotheses) and 5 (coding and analysis).
No LLM is used as coder or judge (section 5.1).

Inputs:  osf/v40/data/v40_raw.jsonl (acquire_v0_40.py), osf/v40/registries/out/*.csv (frozen 2026-11-12),
         osf/v40/registries/aliases_current.csv, osf/v40/prereg/probes_v0_40.json
Outputs: osf/v40/data/v40_mentions.csv (one row per coded mention), osf/v40/v40_verdicts.json
Usage:   python3 score_v0_40.py [--raw PATH] [--out-dir DIR] [--perms 10000]
"""
import argparse
import csv
import json
import math
import random
import re
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
V40 = HERE.parent
REG = V40 / "registries"
SEED = 4040
PERMS = 10_000
WINDOW = 150                      # characters either side of a mention (gone-flag, successor name)
ALPHA = 0.05

# Locked thresholds (pre-registration section 2)
T = {"reinforce_rho": 0.50, "amplify_ratio": 1.25, "afterlife_rate": 0.20, "afterlife_null": 0.05,
     "decay_rho": -0.30, "decay_min_present": 10, "flag_rate": 0.80, "flag_floor": 0.50,
     "search_post_rate": 0.80, "search_min_discordant": 10, "min_units_present": 5}

# Gone-flag lexicon (case-insensitive; locked). A mention is gone-flagged when any pattern occurs within WINDOW
# characters before the mention's start or after its end.
GONE = [r"no longer", r"defunct", r"ceased", r"cease(?:d)? operations", r"went out of business", r"out of business",
        r"merged (?:into|with)", r"was acquired", r"acquired by", r"absorbed", r"folded into", r"now part of",
        r"is now", r"now (?:known|operat\w+|called) as", r"rebrand\w*", r"renamed", r"became", r"formerly",
        r"former", r"used to be", r"was (?:a|an) ", r"shut down", r"closed", r"collapse\w*", r"failed", r"failure",
        r"seized", r"bankrupt\w*", r"discontinued", r"retired", r"defunct", r"does(?: not|n't) exist", r"taken over",
        r"wound down", r"wind-down", r"liquidat\w+", r"transitioned to", r"converted to"]
GONE_RE = re.compile("|".join(GONE), re.I)
# D11 collisions: these bare aliases are coded "ambiguous" (reported with and without; primary excludes them)
AMBIGUOUS = {"American", "United", "Delta", "Frontier", "Spirit", "Continental", "Northwest", "Breeze", "Southwest",
             "Alaska", "Commerce Bank", "Union Bank", "Signature Bank", "Discover", "Sovereign", "Compass Bank", "ATA",
             "Harris Bank", "National City"}
GAP_MODEL = {"M1": "Claude Opus 4.5", "M2": "Claude Sonnet 4.5", "M3": "GPT-4o", "M4": "GPT-4o mini",
             "M5": "Gemini 2.5 Flash", "M6": "Gemini 2.5 Flash-Lite", "M5X": "Gemini 2.5 Flash",
             # Claude Fable 5.2: training-data cutoff Jun 2026, the same month as Claude Opus 5.5 (Anthropic models
             # overview, opened 2026-11-12), so the frozen Opus 5.5 gap rows apply unchanged (section 4.3).
             "C1": "Claude Opus 5.5", "C2": "GPT-6 Astra", "C3": "Gemini 4 Argon"}
TESTED_SLOTS = ["M1", "M2", "M3", "M4", "M5", "M6", "C1", "C2", "C3"]      # M5X is reported, never tested
LEADER = {"airline": "AA", "bank": "1039502"}


# ----------------------------------------------------------------------------- registry
def read_csv(p):
    with open(p, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_registry(reg=REG):
    units = []   # current share units
    for r in read_csv(reg / "out" / "airlines_current.csv"):
        if r["in_registry"] == "True":
            units.append({"id": r["code"], "category": "airline", "role": "current", "brand": r["name"],
                          "aliases": r["aliases"].split("|"), "share": float(r["brand_share_pct"]),
                          "share_alt": float(r["operating_share_pct"])})
    for r in read_csv(reg / "out" / "banks_current.csv"):
        if r["in_registry"] == "True":
            units.append({"id": r["HOLDER"], "category": "bank", "role": "current", "brand": r["brand"],
                          "aliases": r["aliases"].split("|"), "share": float(r["share_pct"]), "share_alt": None})
    subjects = []
    for r in read_csv(reg / "out" / "exits_and_controls.csv"):
        if r["role"] == "ghost" and r["in_registry"] != "True":
            continue
        subjects.append({"id": r["id"], "category": r["category"], "role": r["role"], "brand": r["brand"],
                         "aliases": r["aliases"].split("|"), "successor": r["successor"]})
    gaps = {}
    for r in read_csv(reg / "out" / "exit_cutoff_gaps.csv"):
        gaps[(r["ghost"], r["model"])] = float(r["gap_brand_m"])
    return units, subjects, gaps


# ----------------------------------------------------------------------------- coding
def _pattern(alias):
    return re.compile(r"(?<![\w&])" + re.escape(alias) + r"(?![\w&])")


def build_matchers(units, subjects):
    """(entity id, kind, alias, compiled) sorted longest alias first; ghosts and controls before current units."""
    out = []
    for s in subjects:
        for a in s["aliases"]:
            out.append((s["id"], s["role"], a, _pattern(a)))
    for u in units:
        for a in u["aliases"]:
            out.append((u["id"], "current", a, _pattern(a)))
    return sorted(out, key=lambda t: -len(t[2]))


def successor_names(succ):
    if not succ or succ.lower().startswith("none"):
        return []
    parts = re.split(r"\s*(?:/|,| then |\(|\))\s*", succ)
    names = [p.strip() for p in parts if p.strip() and not re.match(r"^(brand kept|brand kept for now|\d{4})$", p.strip())]
    return [n for n in names if n not in ("brand kept", "brand kept for now")]


def code_answer(text, matchers, succ_by_id):
    """Mentions in one answer: longest alias wins; overlapping shorter matches are dropped."""
    taken = []
    out = []
    for eid, kind, alias, pat in matchers:
        for m in pat.finditer(text or ""):
            a, b = m.span()
            if any(a < y and b > x for x, y in taken):
                continue
            taken.append((a, b))
            ctx = text[max(0, a - WINDOW):a] + " " + text[b:b + WINDOW]
            near_new = any(n in ctx for n in succ_by_id.get(eid, []))
            out.append({"entity": eid, "kind": kind, "alias": alias, "start": a, "end": b,
                        "ambiguous": alias in AMBIGUOUS, "gone_flag": bool(GONE_RE.search(ctx)),
                        "successor_near": near_new})
    return sorted(out, key=lambda d: d["start"])


# ----------------------------------------------------------------------------- statistics (exact / permutation)
def rank(xs):
    idx = sorted(range(len(xs)), key=lambda i: xs[i])
    r = [0.0] * len(xs)
    i = 0
    while i < len(xs):
        j = i
        while j + 1 < len(xs) and xs[idx[j + 1]] == xs[idx[i]]:
            j += 1
        for k in range(i, j + 1):
            r[idx[k]] = (i + j) / 2 + 1
        i = j + 1
    return r


def spearman(x, y):
    if len(x) < 3:
        return float("nan")
    rx, ry = rank(x), rank(y)
    mx, my = sum(rx) / len(rx), sum(ry) / len(ry)
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = math.sqrt(sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry))
    return num / den if den else float("nan")


def perm_spearman(x, y, perms, tail, strata=None, seed=SEED):
    """One-sided permutation p for Spearman rho (tail 'greater' or 'less'); permutes y within strata."""
    obs = spearman(x, y)
    if math.isnan(obs):
        return obs, float("nan")
    rng = random.Random(seed)
    groups = defaultdict(list)
    for i, s in enumerate(strata or [0] * len(y)):
        groups[s].append(i)
    hits = 0
    for _ in range(perms):
        yp = list(y)
        for idx in groups.values():
            vals = [y[i] for i in idx]
            rng.shuffle(vals)
            for i, v in zip(idx, vals):
                yp[i] = v
        r = spearman(x, yp)
        if (tail == "greater" and r >= obs - 1e-12) or (tail == "less" and r <= obs + 1e-12):
            hits += 1
    return obs, (hits + 1) / (perms + 1)


def binom_pmf(i, n, p):
    if p <= 0:
        return 1.0 if i == 0 else 0.0
    if p >= 1:
        return 1.0 if i == n else 0.0
    return math.exp(math.lgamma(n + 1) - math.lgamma(i + 1) - math.lgamma(n - i + 1) + i * math.log(p) + (n - i) * math.log1p(-p))


def binom_sf(k, n, p):
    """P(X >= k), X ~ Binomial(n, p), exact (log-space terms)."""
    if k <= 0:
        return 1.0
    return min(1.0, sum(binom_pmf(i, n, p) for i in range(k, n + 1)))


def binom_cdf(k, n, p):
    return min(1.0, sum(binom_pmf(i, n, p) for i in range(0, k + 1)))


def fisher_greater(a, b, c, d):
    """One-sided Fisher exact p that row 1's rate a/(a+b) exceeds row 2's c/(c+d)."""
    n1, n2, k = a + b, c + d, a + c
    tot = math.comb(n1 + n2, k)
    return sum(math.comb(n1, i) * math.comb(n2, k - i) for i in range(a, min(n1, k) + 1)) / tot if tot else float("nan")


# ----------------------------------------------------------------------------- scoring
def verdict(conf, part, fals):
    return "CONFIRMED" if conf else ("PARTIAL" if part else ("FALSIFIED" if fals else "UNDETERMINED"))


class Scorer:
    def __init__(self, records, units, subjects, gaps, perms=PERMS):
        self.units, self.subjects, self.gaps, self.perms = units, subjects, gaps, perms
        self.all = records
        self.ok = [r for r in records if r.get("status") == "ok" and (r.get("text") or "").strip()]
        self.matchers = build_matchers(units, subjects)
        succ = {s["id"]: successor_names(s["successor"]) for s in subjects}
        self.unit_of = {u["id"]: u for u in units}
        self.subj = {s["id"]: s for s in subjects}
        # a retained brand's mentions count toward its share unit (D2, D12)
        self.to_unit = {u["id"]: u["id"] for u in units}
        for s in subjects:
            if s["role"] == "control":
                for u in units:
                    if u["category"] == s["category"] and set(u["aliases"]) & set(s["aliases"]):
                        self.to_unit[s["id"]] = u["id"]
        self.inc = {"AA": "AA", "DL": "DL", "JPMC": "1039502", "BAC": "1073757"}
        for r in self.ok:
            r["_m"] = code_answer(r["text"], self.matchers, succ)

    # helpers
    def recs(self, kind=None, tier=None, cond=None, slots=TESTED_SLOTS, category=None):
        return [r for r in self.ok if (kind is None or r["kind"] == kind) and (tier is None or r["tier"] == tier)
                and (cond is None or r["condition"] == cond) and r["slot"] in slots
                and (category is None or r["category"] == category)]

    def names(self, r, ent, ambiguous_ok=False):
        return [m for m in r["_m"] if m["entity"] == ent and (ambiguous_ok or not m["ambiguous"])]

    def unit_counts(self, rs, category):
        c = {u["id"]: 0 for u in self.units if u["category"] == category}
        for r in rs:
            seen = {self.to_unit.get(m["entity"]) for m in r["_m"] if not m["ambiguous"]}
            for u in seen:
                if u in c:
                    c[u] += 1
        return c

    def ai_share(self, category, cond="S0", exclude=()):
        per_slot = []
        for sl in TESTED_SLOTS:
            c = self.unit_counts(self.recs("recommendation", cond=cond, slots=[sl], category=category), category)
            c = {k: v for k, v in c.items() if k not in exclude}
            tot = sum(c.values())
            if tot:
                per_slot.append({k: v / tot for k, v in c.items()})
        keys = [u["id"] for u in self.units if u["category"] == category and u["id"] not in exclude]
        return {k: (sum(s[k] for s in per_slot) / len(per_slot) if per_slot else 0.0) for k in keys}

    # H_Reinforce
    def h_reinforce(self):
        out = {}
        for cat in ("airline", "bank"):
            sh = self.ai_share(cat)
            ms = {u["id"]: u["share"] for u in self.units if u["category"] == cat}
            ks = list(ms)
            present = sum(sh[k] > 0 for k in ks)
            rho, p = perm_spearman([ms[k] for k in ks], [sh[k] for k in ks], self.perms, "greater")
            out[cat] = {"n_units": len(ks), "units_present": present, "rho": rho, "p_perm": p,
                        "pass": present >= T["min_units_present"] and rho >= T["reinforce_rho"] and p < ALPHA,
                        "evaluable": present >= T["min_units_present"]}
        ev = all(v["evaluable"] for v in out.values())
        npass = sum(v["pass"] for v in out.values())
        out["verdict"] = verdict(npass == 2, npass == 1, ev and npass == 0 and all(v["p_perm"] >= ALPHA for v in out.values()))
        return out

    # H_Amplify
    def h_amplify(self):
        out = {}
        for cat in ("airline", "bank"):
            rs = self.recs("recommendation", cond="S0", category=cat)
            c = self.unit_counts(rs, cat)
            ms = {u["id"]: u["share"] for u in self.units if u["category"] == cat}
            n, k = sum(c.values()), c[LEADER[cat]]
            p0 = ms[LEADER[cat]] / sum(ms.values())
            ratio = (k / n) / p0 if n else float("nan")
            pg, pl = binom_sf(k, n, p0), binom_cdf(k, n, p0)
            xs = [(math.log(ms[u]), math.log(v)) for u, v in self.ai_share(cat).items() if v > 0 and ms[u] > 0]
            slope = None
            if len(xs) >= 3:
                mx, my = sum(a for a, _ in xs) / len(xs), sum(b for _, b in xs) / len(xs)
                sxx = sum((a - mx) ** 2 for a, _ in xs)
                slope = sum((a - mx) * (b - my) for a, b in xs) / sxx if sxx else None
            out[cat] = {"leader": LEADER[cat], "k": k, "n": n, "p0": p0, "ratio": ratio, "p_greater": pg, "p_less": pl,
                        "loglog_slope": slope, "amplified": n > 0 and ratio >= T["amplify_ratio"] and pg < ALPHA,
                        "flattened": n > 0 and ratio < 1 and pl < ALPHA}
        na = sum(out[c]["amplified"] for c in ("airline", "bank"))
        nf = sum(out[c]["flattened"] for c in ("airline", "bank"))
        out["verdict"] = verdict(na == 2, na == 1, nf == 2)
        return out

    # ghosts
    def ghosts(self, category=None):
        return [s for s in self.subjects if s["role"] == "ghost" and (category is None or s["category"] == category)]

    def gap(self, gid, slot):
        return self.gaps.get((gid, GAP_MODEL[slot]))

    def h_afterlife(self):
        out = {}
        for cat in ("airline", "bank"):
            k = n = 0
            for g in self.ghosts(cat):
                for sl in TESTED_SLOTS:
                    gp = self.gap(g["id"], sl)
                    if gp is None or gp <= 0:
                        continue
                    n += 1
                    rs = self.recs("recommendation", cond="S0", slots=[sl], category=cat)
                    k += any(not m["gone_flag"] for r in rs for m in self.names(r, g["id"]))
            rate = k / n if n else float("nan")
            p = binom_sf(k, n, T["afterlife_null"]) if n else float("nan")
            out[cat] = {"pairs": n, "afterlife_pairs": k, "rate": rate, "p_exact": p,
                        "pass": n > 0 and rate >= T["afterlife_rate"] and p < ALPHA, "low": n > 0 and rate < T["afterlife_null"]}
        npass = sum(out[c]["pass"] for c in ("airline", "bank"))
        out["verdict"] = verdict(npass == 2, npass == 1, all(out[c]["low"] for c in ("airline", "bank")))
        return out

    def h_decay(self):
        xs, ys, st = [], [], []
        for g in self.ghosts():
            for sl in TESTED_SLOTS:
                gp = self.gap(g["id"], sl)
                if gp is None or gp <= 0:
                    continue
                rs = self.recs("recommendation", cond="S0", slots=[sl], category=g["category"])
                if not rs:
                    continue
                xs.append(gp)
                ys.append(sum(bool(self.names(r, g["id"])) for r in rs) / len(rs))
                st.append(sl)
        present = sum(y > 0 for y in ys)
        rho, p = perm_spearman(xs, ys, self.perms, "less", strata=st)
        ev = present >= T["decay_min_present"]
        out = {"pairs": len(xs), "pairs_present": present, "rho": rho, "p_perm": p, "evaluable": ev}
        out["verdict"] = "UNDETERMINED" if not ev else verdict(rho <= T["decay_rho"] and p < ALPHA,
                                                               rho < 0 and p < ALPHA, rho >= 0)
        return out

    def flagged(self, r, sid):
        ent = self.inc.get(sid, sid)
        ms = [m for m in r["_m"] if m["entity"] == ent]
        if ms:
            return any(m["gone_flag"] for m in ms)
        return bool(GONE_RE.search(r["text"][:2 * WINDOW]))

    def h_flag(self, drop_controls=()):
        gk = gn = ck = cn = 0
        for r in self.recs(tier="S", cond="S0"):
            sid = r["brand_id"]
            s = self.subj.get(sid)
            role = s["role"] if s else ("incumbent" if sid in self.inc else None)
            if role == "ghost":
                gp = self.gap(sid, r["slot"])
                if gp is None or gp <= 0:
                    continue
                gn += 1
                gk += self.flagged(r, sid)
            elif role in ("control", "incumbent") and sid not in drop_controls:
                cn += 1
                ck += self.flagged(r, sid)
        rg = gk / gn if gn else float("nan")
        rc = ck / cn if cn else float("nan")
        pf = fisher_greater(gk, gn - gk, ck, cn - ck) if gn and cn else float("nan")
        a, b = gn > 0 and rg >= T["flag_rate"], gn > 0 and pf < ALPHA
        out = {"ghost_answers": gn, "ghost_flagged": gk, "ghost_rate": rg, "control_answers": cn, "control_flagged": ck,
               "control_rate": rc, "p_fisher": pf}
        out["verdict"] = verdict(a and b, a or b, gn > 0 and rg < T["flag_floor"] and not b)
        return out

    def h_search(self):
        cur = ["C1", "C2", "C3"]
        s0 = defaultdict(list)
        s1 = {}
        for r in self.recs(tier="S", slots=cur):
            sid = r["brand_id"]
            if sid not in self.subj or self.subj[sid]["role"] != "ghost":
                continue
            key = (sid, r["slot"])
            if r["condition"] == "S0":
                s0[key].append(self.flagged(r, sid))
            else:
                s1[key] = self.flagged(r, sid)
        b = c = 0
        post_k = post_n = 0
        for key, f1 in s1.items():
            if key in s0:
                f0 = sum(s0[key]) * 2 > len(s0[key])
                b += f1 and not f0
                c += f0 and not f1
            gp = self.gap(*key)
            if gp is not None and gp < 0:
                post_n += 1
                post_k += f1
        p = binom_sf(b, b + c, 0.5) if b + c else float("nan")
        post = post_k / post_n if post_n else float("nan")
        mc_ok = b + c >= T["search_min_discordant"] and p < ALPHA
        post_ok = post_n > 0 and post >= T["search_post_rate"]
        out = {"paired_cells": sum(1 for k in s1 if k in s0), "s1_only_flagged": b, "s0_only_flagged": c,
               "p_mcnemar_exact": p, "discordant_evaluable": b + c >= T["search_min_discordant"],
               "post_cutoff_cells": post_n, "post_cutoff_s1_flagged": post_k, "post_cutoff_s1_rate": post}
        out["verdict"] = verdict(mc_ok and post_ok, mc_ok or post_ok, b <= c and post_n > 0 and post < T["flag_floor"])
        return out

    # manipulation checks (section 2.7) and descriptives (section 2.8)
    def manipulation(self, expected=None):
        out = {}
        for arm in ("L", "C"):
            rs = [r for r in self.all if r.get("arm") == arm]
            ids = {r["call_id"] for r in self.ok if r.get("arm") == arm}
            exp = (expected or {}).get(arm) or len({r["call_id"] for r in rs}) or 1
            out[f"MC1_complete_{arm}"] = {"ok_calls": len(ids), "expected": exp, "pass": len(ids) / exp >= 0.95}
        for sl in ("C1", "C2", "C3"):
            rs = self.recs(cond="S1", slots=[sl])
            used = sum(((r.get("search") or {}).get("n_searches") or 0) > 0 for r in rs)
            out[f"MC2_search_used_{sl}"] = {"n": len(rs), "searched": used, "pass": bool(rs) and used / len(rs) >= 0.80}
        rs = [r for r in self.recs(tier="K") if r["brand_id"] in self.inc]
        named = sum(bool(self.names(r, self.inc[r["brand_id"]], True)) for r in rs)
        out["MC3_incumbents_recognised"] = {"n": len(rs), "named": named, "pass": bool(rs) and named / len(rs) >= 0.95}
        trunc = re.compile(r"max_tokens|length|MAX_TOKENS|max_output_tokens", re.I)
        for arm, lim in (("L", 0.05), ("C", 0.02)):
            rs = [r for r in self.ok if r.get("arm") == arm]
            t = sum(bool(trunc.search(str(r.get("finish_reason") or ""))) for r in rs)
            out[f"MC4_truncation_{arm}"] = {"n": len(rs), "truncated": t, "limit": lim, "pass": bool(rs) and t / len(rs) <= lim}
        return out

    def descriptives(self):
        d = {}
        gm = [m for r in self.recs() for m in r["_m"] if m["kind"] == "ghost"]
        d["ghost_mentions"] = len(gm)
        d["ghost_mentions_with_successor_near"] = sum(m["successor_near"] for m in gm)
        d["ghost_mentions_gone_flagged"] = sum(m["gone_flag"] for m in gm)
        d["ambiguous_mentions"] = sum(m["ambiguous"] for r in self.recs() for m in r["_m"])
        x = [r for r in self.ok if r["slot"] == "M5X"]
        d["M5X_v039_setting_answers"] = len(x)
        # run-to-run standard error of per-model Presence at S0 (check on v1.17's 0.040)
        ses = []
        for sl in TESTED_SLOTS:
            for cat in ("airline", "bank"):
                runs = defaultdict(list)
                for r in self.recs("recommendation", cond="S0", slots=[sl], category=cat):
                    runs[r["run"]].append(r)
                if len(runs) < 2:
                    continue
                for u in [u["id"] for u in self.units if u["category"] == cat]:
                    pr = [sum(any(self.to_unit.get(m["entity"]) == u and not m["ambiguous"] for m in r["_m"]) for r in rs) / len(rs)
                          for rs in runs.values() if rs]
                    mu = sum(pr) / len(pr)
                    sd = math.sqrt(sum((p - mu) ** 2 for p in pr) / (len(pr) - 1)) if len(pr) > 1 else 0.0
                    ses.append(sd / math.sqrt(len(pr)))
        d["presence_se_mean_S0"] = sum(ses) / len(ses) if ses else None
        d["presence_se_units"] = len(ses)
        return d

    def run(self, expected=None):
        res = {"phase": "v0.40", "seed": SEED, "permutations": self.perms, "thresholds": T, "window_chars": WINDOW,
               "H_Reinforce": self.h_reinforce(), "H_Amplify": self.h_amplify(), "H_Afterlife": self.h_afterlife(),
               "H_Decay": self.h_decay(), "H_Flag": self.h_flag(), "H_Search": self.h_search(),
               "sensitivity": {
                   "H_Flag_without_DISCOVER": self.h_flag(drop_controls=("DISCOVER",)),
                   "H_Reinforce_banks_without_brokerage_D4": self.d4()},
               "manipulation_checks": self.manipulation(expected), "descriptives": self.descriptives()}
        return res

    def d4(self):
        ex = [u["id"] for u in self.units if u["category"] == "bank"
              and re.search(r"Morgan Stanley|Schwab|UBS", u["brand"] + " " + " ".join(u["aliases"]))]
        sh = self.ai_share("bank", exclude=ex)
        ms = {u["id"]: u["share"] for u in self.units if u["category"] == "bank" and u["id"] not in ex}
        ks = list(ms)
        rho, p = perm_spearman([ms[k] for k in ks], [sh[k] for k in ks], self.perms, "greater")
        return {"excluded": ex, "rho": rho, "p_perm": p}

    def mention_rows(self):
        for r in self.ok:
            for m in r["_m"]:
                yield {"call_id": r["call_id"], "slot": r["slot"], "condition": r["condition"], "run": r["run"],
                       "probe_id": r["probe_id"], "entity": m["entity"], "kind": m["kind"], "alias": m["alias"],
                       "start": m["start"], "ambiguous": m["ambiguous"], "gone_flag": m["gone_flag"],
                       "successor_near": m["successor_near"]}


def switch_controls(subjects, probes_path=V40 / "prereg" / "probes_v0_40.json"):
    """Discover switch (b): a replacement control named in the final probe set but not in the registry's
    exits_and_controls.csv is added as a control, matched by its probe name (pre-registration section 3.2)."""
    known = {s["id"] for s in subjects} | {"AA", "DL", "JPMC", "BAC"}
    spec = json.loads(Path(probes_path).read_text(encoding="utf-8"))
    return [{"id": s["subject_id"], "category": s["category"], "role": "control", "brand": s["registry_brand"],
             "aliases": [s["name_in_probe"]], "successor": ""}
            for s in spec.get("subjects", []) if s["subject_id"] not in known and s["role"] == "control"]


def load_raw(path):
    return [json.loads(l) for l in Path(path).read_text(encoding="utf-8").splitlines() if l.strip()]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", default=str(V40 / "data" / "v40_raw.jsonl"))
    ap.add_argument("--out-dir", default=str(V40))
    ap.add_argument("--perms", type=int, default=PERMS)
    a = ap.parse_args()
    units, subjects, gaps = load_registry()
    subjects = subjects + switch_controls(subjects)
    sc = Scorer(load_raw(a.raw), units, subjects, gaps, a.perms)
    res = sc.run(expected={"L": 1786, "C": 1035})
    out = Path(a.out_dir)
    (out / "data").mkdir(parents=True, exist_ok=True)
    rows = list(sc.mention_rows())
    with open(out / "data" / "v40_mentions.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]) if rows else ["call_id"])
        w.writeheader()
        w.writerows(rows)
    (out / "v40_verdicts.json").write_text(json.dumps(res, indent=2, default=str), encoding="utf-8")
    for h in ("H_Reinforce", "H_Amplify", "H_Afterlife", "H_Decay", "H_Flag", "H_Search"):
        print(f"{h:12s} {res[h]['verdict']}")


if __name__ == "__main__":
    main()
