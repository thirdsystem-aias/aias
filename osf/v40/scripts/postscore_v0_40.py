#!/usr/bin/env python3
"""
postscore_v0_40.py -- AIAS(TM) v0.40: pre-registered reporting the locked scorer did not output, and the H_Amplify
ceiling check (DEVIATIONS Entry 2, Pablo's decision of Sat 21 November 2026, 1:56 pm CT).

What it computes (no test, no verdict, no scored number is changed or re-computed for the record):
  prereg  -- "pre-registered, computed after scoring because the locked scorer did not output them":
             descriptive 1 (AI share against market share per unit and model, both arms, search off and on; the
             log-log slope with and without the brokerage and wealth holders, D4), descriptive 2 (ghost Presence and
             the afterlife flag per ghost, model and arm; post-cutoff exits apart), the per-ghost and per-model
             results beside each test (pre-registration section 8 item 6), and the Discover status answers in full
             (section 3.2, version (a)).
  ceiling -- a post-scoring check of the locked H_Amplify measure, not a pre-registered test: the largest ratio
             (k/n)/p0 the measure could reach at the observed breadth of answers (a leader named in every answer,
             k = answers, n as observed), for the registered rule and for each specification of Figure 2.
  post_sensitivity -- "sensitivity, not pre-registered as run; computed after scoring" (DEVIATIONS Entry 4, Pablo's
             decision of Sat 21 November 2026, ~3 pm CT): the six tests recomputed by the locked methods, locked
             permutation count and seed, with non-ambiguous Discover mentions counted toward the Capital One holder as
             section 2.1 / D12 say (the locked scorer links a control to a unit only through shared aliases, so it
             never does). Only the scorer's control-to-unit map changes, on a copy; nothing is re-scored for the record.

How. It reads only frozen, checksummed files: the coded mentions osf/v40/data/v40_mentions.csv (SHA-256 must be
0a83b397..., as in the coding manifest, the DEVIATIONS record and step 9), the coded-answer frame
data/v40_coded_answers.csv and the acquisition record data/v40_raw.jsonl (SHA-256 as in the coding manifest), the
frozen registry and probe set. It imports the locked score_v0_40.py UNCHANGED (its SHA-256 and that of
stoprule_v0_40.py are checked against the lock manifest first) and builds the locked Scorer with its own __init__;
the only substitution is that the registry coding of each answer is looked up in the frozen mentions file instead of
being re-run (score_v0_40.code_answer is replaced for the duration of the constructor; the near-floor "other" coding
is left as it is). Two closure checks must pass before anything is written: (1) the Scorer's mention rows, written
with the scorer's own writer, are byte-identical to the frozen mentions file; (2) the six primary tests and S-D4,
recomputed by the locked methods with the locked permutation count and seed, equal v40_verdicts.json exactly.
Answer text is read from the acquisition record only where the locked rules read it (the status-answer flag rule of
section 2.1 reads the first 300 characters when the subject is not matched) and for the Discover answers in full.

Outputs: osf/v40/v40_postscore.json (read by values_v0_40.py into v40_values.json) and
         osf/v40/v40_discover_status_answers.md (the Discover status answers in full, section 3.2).
Usage:   python3 osf/v40/scripts/postscore_v0_40.py [--check] [--perms N]
         --check: exit 1 if the committed outputs differ from a fresh build (nothing written).
Deterministic: no network, no model call, no clock.
"""
import argparse
import copy
import csv
import hashlib
import io
import json
import math
import sys
from collections import defaultdict
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import score_v0_40 as S  # noqa: E402  (the locked scorer; imported, never modified)

V40 = S.V40
ROOT = V40.parent.parent
LOCK_MANIFEST = V40 / "prereg" / "LOCK_MANIFEST_v0_40.sha256"
MENTIONS_SHA256 = "0a83b397fa00401cef70570a35e3c443e318e52213752a261f79ac5de14dfffe"
REL = {"mentions": "osf/v40/data/v40_mentions.csv", "coded": "osf/v40/data/v40_coded_answers.csv",
       "raw": "osf/v40/data/v40_raw.jsonl", "manifest": "osf/v40/data/v40_coding_manifest.json",
       "verdicts": "osf/v40/v40_verdicts.json"}
OUT_JSON = "osf/v40/v40_postscore.json"
OUT_DISCOVER = "osf/v40/v40_discover_status_answers.md"
LABEL_PREREG = "pre-registered, computed after scoring because the locked scorer did not output them"
LABEL_CEILING = ("post-scoring check of the locked H_Amplify measure (DEVIATIONS Entry 2); not a pre-registered test; "
                 "no verdict changes")
LABEL_SENS = ("sensitivity, not pre-registered as run; computed after scoring (DEVIATIONS Entry 4); "
              "no verdict changes")
SLOT_NAME = {"M1": "Claude Opus 4.5", "M2": "Claude Sonnet 4.5", "M3": "GPT-4o", "M4": "GPT-4o mini",
             "M5": "Gemini 2.5 Flash", "M6": "Gemini 2.5 Flash-Lite", "C1": "Claude Fable 5.2", "C2": "GPT-6 Astra",
             "C3": "Gemini 4 Argon"}
CATS = ("airline", "bank")


class Refused(Exception):
    pass


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def locked_sha(name, manifest=LOCK_MANIFEST):
    for line in Path(manifest).read_text(encoding="utf-8").splitlines():
        parts = line.split()
        if len(parts) >= 2 and parts[-1].lstrip("*").endswith(name):
            return parts[0]
    return None


def check_inputs(root=ROOT):
    """Refuse unless the locked scorer is the locked bytes and every frozen input has its recorded SHA-256."""
    root = Path(root)
    for name in ("scripts/score_v0_40.py", "scripts/stoprule_v0_40.py"):
        want, have = locked_sha(name), sha256(HERE / Path(name).name)
        if want is None or want != have:
            raise Refused(f"{name}: SHA-256 {have} does not match the lock manifest ({want})")
    man = json.loads((root / REL["manifest"]).read_text(encoding="utf-8"))
    got = sha256(root / REL["mentions"])
    if got != MENTIONS_SHA256 or got != man["outputs"]["v40_mentions.csv"]["sha256"]:
        raise Refused(f"v40_mentions.csv SHA-256 {got} is not the frozen {MENTIONS_SHA256}")
    if sha256(root / REL["coded"]) != man["outputs"]["v40_coded_answers.csv"]["sha256"]:
        raise Refused("v40_coded_answers.csv SHA-256 differs from the coding manifest")
    if sha256(root / REL["raw"]) != man["inputs"]["raw"]["sha256"]:
        raise Refused("v40_raw.jsonl SHA-256 differs from the coding manifest")
    if man.get("cut_before_first_brand_missing") != 0:
        raise Refused("the coding manifest records answers cut before the first brand; not handled here")
    return man


def read_mentions(path):
    """Frozen mentions, grouped by call ID in file order, as the coder's mention dicts."""
    by = defaultdict(list)
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            by[r["call_id"]].append({"entity": r["entity"], "kind": r["kind"], "alias": r["alias"],
                                     "start": int(r["start"]), "ambiguous": r["ambiguous"] == "True",
                                     "gone_flag": r["gone_flag"] == "True",
                                     "successor_near": r["successor_near"] == "True"})
    return by


def frozen_scorer(root=ROOT, perms=S.PERMS):
    """The locked Scorer built by its own __init__, with each answer's registry coding taken from the frozen file."""
    root = Path(root)
    records = S.load_raw(root / REL["raw"])
    ments = read_mentions(root / REL["mentions"])
    frame = {r["call_id"]: r for r in csv.DictReader(open(root / REL["coded"], newline="", encoding="utf-8"))}
    ok_ids = [r["call_id"] for r in records if r.get("status") == "ok" and (r.get("text") or "").strip()]
    if set(ok_ids) != set(frame) or len(ok_ids) != len(frame):
        raise Refused("the coded-answer frame does not list exactly the answers the scorer keeps")
    if set(ments) - set(frame):
        raise Refused("the mentions file names a call ID that is not in the coded-answer frame")
    by_text = {}
    for r in records:
        if r["call_id"] not in frame:
            continue
        f = frame[r["call_id"]]
        for k in ("arm", "slot", "condition", "kind", "tier", "category", "probe_id"):
            if str(r.get(k)) != f[k]:
                raise Refused(f"{r['call_id']}: field {k} differs between the raw record and the coded frame")
        m = ments.get(r["call_id"], [])
        if len(m) != int(f["n_mentions"]):
            raise Refused(f"{r['call_id']}: {len(m)} mentions in the file, {f['n_mentions']} in the frame")
        prev = by_text.setdefault(r["text"], m)
        if prev != m:
            raise Refused(f"{r['call_id']}: two answers with the same text carry different frozen mentions")
    original = S.code_answer

    def lookup(text, matchers, succ):
        if succ:                                    # the registry coding (Scorer passes self.succ); frozen
            return [dict(x) for x in by_text[text]]
        return original(text, matchers, succ)       # the near-floor "other" coding, as locked (not used here)

    units, subjects, gaps = S.load_registry()
    subjects = subjects + S.switch_controls(subjects)
    S.code_answer = lookup
    try:
        sc = S.Scorer(records, units, subjects, gaps, perms)
    finally:
        S.code_answer = original
    return sc


def mention_bytes(sc):
    """The mentions file exactly as score_v0_40.main() writes it."""
    rows = list(sc.mention_rows())
    buf = io.StringIO(newline="")
    w = csv.DictWriter(buf, fieldnames=list(rows[0]) if rows else ["call_id"])
    w.writeheader()
    w.writerows(rows)
    return buf.getvalue().encode("utf-8")


def _same(a, b):
    return json.loads(json.dumps(a, default=str)) == json.loads(json.dumps(b, default=str))


def closure_checks(sc, root=ROOT, perms=S.PERMS):
    root = Path(root)
    if mention_bytes(sc) != (root / REL["mentions"]).read_bytes():
        raise Refused("closure check 1 failed: the Scorer's mention rows differ from the frozen mentions file")
    ver = json.loads((root / REL["verdicts"]).read_text(encoding="utf-8"))
    out = {"mentions_file_byte_identical": True}
    if perms == S.PERMS:
        got = sc.tests()
        got["S-D4"] = sc.d4()
        want = {h: ver[h] for h in got if h != "S-D4"}
        want["S-D4"] = ver["sensitivity"]["S-D4"]
        bad = [h for h in got if not _same(got[h], want[h])]
        if bad:
            raise Refused(f"closure check 2 failed: {bad} differ from v40_verdicts.json")
        out["primary_tests_and_S_D4_equal_verdict_file"] = True
    else:
        out["primary_tests_and_S_D4_equal_verdict_file"] = None     # not checked at a reduced permutation count
    return out


# ----------------------------------------------------------------------------- helpers
def clean(x):
    """NaN (an undefined correlation) is stored as null."""
    if isinstance(x, float) and math.isnan(x):
        return None
    return x


def loglog_slope(shares, ms):
    """The descriptive slope exactly as score_v0_40.Scorer.h_amplify computes it (units with AI share > 0)."""
    xs = [(math.log(ms[u]), math.log(v)) for u, v in shares.items() if v > 0 and ms[u] > 0]
    if len(xs) < 3:
        return None
    mx, my = sum(a for a, _ in xs) / len(xs), sum(b for _, b in xs) / len(xs)
    sxx = sum((a - mx) ** 2 for a, _ in xs)
    return sum((a - mx) * (b - my) for a, b in xs) / sxx if sxx else None


def market(sc, cat, exclude=()):
    return {u["id"]: u["share"] for u in sc.units if u["category"] == cat and u["id"] not in exclude}


def answers(sc, cat, slots=None, cond="S0"):
    return len(sc.recs("recommendation", cond=cond, slots=slots, category=cat))


def spec_variants(sc):
    """The specifications of Figure 2, built exactly as Scorer.sensitivities() builds them."""
    op_units = [dict(u, share=u["share_alt"]) if u["category"] == "airline" and u.get("share_alt") is not None else u
                for u in sc.units]
    return {"all_nine": (sc, CATS), "legacy": (sc.variant(slots=S.LEGACY_SLOTS), CATS),
            "current": (sc.variant(slots=S.CURRENT_SLOTS), CATS), "S-Ambig": (sc.variant(amb=True), CATS),
            "S-Operating": (sc.variant(units=op_units, leader={"airline": "DL"}), ("airline",)),
            "S-SunCountry": (sc.variant(units=S.sun_country_inside_allegiant(sc.units)), ("airline",))}


def ceiling_of(v, cat):
    """Largest (k/n)/p0 at the observed breadth: every answer names the leader (k = answers), n as observed."""
    a = v.h_amplify()[cat]
    na = answers(v, cat)
    return {"leader": a["leader"], "answers": na, "k": a["k"], "n": a["n"], "p0": a["p0"], "ratio": a["ratio"],
            "units_per_answer": a["n"] / na, "leader_answer_share": a["k"] / na,
            "ceiling_ratio": (na / a["n"]) / a["p0"],
            "ceiling_reaches_threshold": (na / a["n"]) / a["p0"] >= S.T["amplify_ratio"],
            "ceiling_reaches_parity": (na / a["n"]) / a["p0"] >= 1.0}


# ----------------------------------------------------------------------------- the ceiling check
def ceiling(sc):
    out = {"label": LABEL_CEILING,
           "definition": "ceiling_ratio = (answers / n) / p0: the registered ratio (k/n)/p0 with the leader named in "
                         "every search-off recommendation answer (k = answers) and n, the unit-namings, as observed; "
                         "units_per_answer = n / answers"}
    for cat in CATS:
        out[cat] = ceiling_of(sc, cat)
    out["specs"] = {name: {cat: ceiling_of(v, cat) for cat in cats} for name, (v, cats) in spec_variants(sc).items()}
    out["by_model"] = {sl: {cat: ceiling_of(sc.variant(slots=[sl]), cat) for cat in CATS} for sl in S.TESTED_SLOTS}
    return out


# ----------------------------------------------------------------------------- Discover toward Capital One (Entry 4)
def discover_target(sc):
    """The current unit Discover's mentions count toward under section 2.1 / D12, read from the frozen registry: the
    unit whose aliases include a name in Discover's successor column (successor_names, as the locked coder parses it)."""
    s = sc.subj.get("DISCOVER")
    if s is None or s["role"] != "control":
        raise Refused("DISCOVER is not a control of the frozen registry")
    names = set(S.successor_names(s["successor"]))
    hits = [u["id"] for u in sc.units if u["category"] == s["category"] and names & set(u["aliases"])]
    if len(hits) != 1:
        raise Refused(f"Discover's successor {s['successor']!r} matches {len(hits)} bank units, not exactly one")
    return hits[0]


def _cleaned(obj):
    return json.loads(json.dumps(obj, default=str), parse_constant=lambda c: None) if obj is not None else None


def discover_to_capital_one(sc, ver):
    """Sensitivity, not pre-registered as run (DEVIATIONS Entry 4): the six tests recomputed by the locked methods
    with non-ambiguous Discover mentions counted toward the Capital One holder (section 2.1, D12), which the locked
    scorer does not do (it links a control to a unit only through shared aliases). Only Scorer.to_unit changes."""
    uid = discover_target(sc)
    if sc.to_unit.get("DISCOVER") is not None:
        raise Refused("the locked scorer already maps DISCOVER to a unit; nothing to check")
    v = sc.variant()
    v.to_unit = dict(sc.to_unit)
    v.to_unit["DISCOVER"] = uid
    got = v.tests()
    rs = sc.recs("recommendation", cond="S0", category="bank")
    disc = [r for r in rs if sc.names(r, "DISCOVER")]
    base_c, new_c = sc.unit_counts(rs, "bank"), v.unit_counts(rs, "bank")
    locked = sc.perms == S.PERMS
    verdicts = {h: got[h]["verdict"] for h in got}
    reg = {h: ver[h]["verdict"] for h in got}
    rb, ab = got["H_Reinforce"]["bank"], got["H_Amplify"]["bank"]
    return {"label": LABEL_SENS,
            "rule": "non-ambiguous mentions of the control DISCOVER count toward the bank unit named in its "
                    "successor column (section 2.1, D12); every other rule, input and setting as locked",
            "target_unit": uid, "target_brand": sc.unit_of[uid]["brand"],
            "permutations": sc.perms,
            "search_off_recommendation_answers_naming_discover": len(disc),
            "of_which_already_naming_target": sum(1 for r in disc if any(
                sc.to_unit.get(m["entity"]) == uid for m in r["_m"] if not m["ambiguous"])),
            "target_unit_namings": {"registered": base_c[uid], "with_discover": new_c[uid]},
            "bank_unit_namings": {"registered": sum(base_c.values()), "with_discover": sum(new_c.values())},
            "H_Reinforce_bank": {"registered_rho": ver["H_Reinforce"]["bank"]["rho"], "rho": rb["rho"],
                                 "registered_p_perm": ver["H_Reinforce"]["bank"]["p_perm"], "p_perm": rb["p_perm"],
                                 "units_present": rb["units_present"], "pass": rb["pass"]},
            "H_Amplify_bank": {"registered_ratio": ver["H_Amplify"]["bank"]["ratio"], "ratio": ab["ratio"],
                               "k": ab["k"], "n": ab["n"], "p0": ab["p0"], "p_greater": ab["p_greater"],
                               "p_less": ab["p_less"], "loglog_slope": ab["loglog_slope"],
                               "amplified": ab["amplified"], "flattened": ab["flattened"]},
            "ceiling_bank": ceiling_of(v, "bank"),
            "tests": _cleaned(got),
            "verdicts": verdicts, "registered_verdicts": reg,
            "verdicts_unchanged": (verdicts == reg) if locked else None}


# ----------------------------------------------------------------------------- descriptive 1
def d1_ai_share(sc, d4_excluded):
    out = {}
    cells = [(sl, "S0") for sl in S.TESTED_SLOTS] + [(sl, "S1") for sl in S.CURRENT_SLOTS]
    pools = {"all_nine_S0": (S.TESTED_SLOTS, "S0"), "legacy_S0": (S.LEGACY_SLOTS, "S0"),
             "current_S0": (S.CURRENT_SLOTS, "S0"), "current_S1": (S.CURRENT_SLOTS, "S1")}
    for cat in CATS:
        ms = market(sc, cat)
        tot = sum(ms.values())
        c = {"units": {u: {"brand": next(x["brand"] for x in sc.units if x["id"] == u), "market_share": ms[u] / tot}
                       for u in ms},
             "by_model": {}, "pooled": {}, "loglog_slope": {}}
        for sl, cond in cells:
            v = sc.variant(slots=[sl])
            sh = v.ai_share(cat, cond=cond)
            cnt = v.unit_counts(v.recs("recommendation", cond=cond, category=cat), cat)
            c["by_model"][f"{sl}|{cond}"] = {u: {"ai_share": sh[u], "named_answers": cnt[u]} for u in ms}
            c["by_model"][f"{sl}|{cond}"]["answers"] = answers(v, cat, cond=cond)
        for name, (slots, cond) in pools.items():
            v = sc.variant(slots=slots)
            sh = v.ai_share(cat, cond=cond)
            c["pooled"][name] = {u: {"ai_share": sh[u]} for u in ms}
            c["loglog_slope"][name] = loglog_slope(sh, ms)
            if cat == "bank":     # S-D4's own path: Scorer.ai_share(..., exclude=the three D4 holders)
                c["loglog_slope"][name + "_without_D4"] = loglog_slope(
                    v.ai_share(cat, cond=cond, exclude=d4_excluded), market(sc, cat, d4_excluded))
        if cat == "bank":
            c["D4_excluded"] = {u: next(x["brand"] for x in sc.units if x["id"] == u) for u in d4_excluded}
        out[cat] = c
    return out


# ----------------------------------------------------------------------------- descriptive 2 and per-ghost tables
def d2_ghosts(sc):
    out = {}
    cells = [(sl, "S0") for sl in S.TESTED_SLOTS] + [(sl, "S1") for sl in S.CURRENT_SLOTS]
    for g in sc.ghosts():
        gid = g["id"]
        row = {"brand": g["brand"], "category": g["category"], "by_model": {}}
        for sl, cond in cells:
            rs = sc.recs("recommendation", cond=cond, slots=[sl], category=g["category"])
            ns = [sc.names(r, gid) for r in rs]
            gp = sc.gap(gid, sl)
            row["by_model"][f"{sl}|{cond}"] = {
                "gap_months": int(gp) if gp is not None and gp == int(gp) else gp, "pre_cutoff": gp is not None and gp > 0, "answers": len(rs),
                "named_answers": sum(bool(x) for x in ns),
                "presence": (sum(bool(x) for x in ns) / len(rs)) if rs else None,
                "afterlife": any(not m["gone_flag"] for x in ns for m in x)}
        s0 = [row["by_model"][f"{sl}|S0"] for sl in S.TESTED_SLOTS]
        pre = [x for x in s0 if x["pre_cutoff"]]
        row["pre_cutoff_pairs"] = len(pre)
        row["post_cutoff_pairs"] = sum(1 for x in s0 if x["gap_months"] is not None and x["gap_months"] <= 0)
        row["afterlife_pairs"] = sum(x["afterlife"] for x in pre)
        row["pairs_named"] = sum(x["named_answers"] > 0 for x in pre)
        row["mean_presence_pre_cutoff"] = (sum(x["presence"] for x in pre) / len(pre)) if pre else None
        out[gid] = row
    return out


def search_cells(sc):
    """Per (ghost, current model) status cell, exactly as Scorer.h_search reads them."""
    s0, s1 = defaultdict(list), {}
    for r in sc.recs(tier="S", slots=S.CURRENT_SLOTS):
        sid = r["brand_id"]
        if sid not in sc.subj or sc.subj[sid]["role"] != "ghost":
            continue
        if r["condition"] == "S0":
            s0[(sid, r["slot"])].append(sc.flagged(r, sid))
        else:
            s1[(sid, r["slot"])] = sc.flagged(r, sid)
    cells = {}
    for key, f1 in s1.items():
        gp = sc.gap(*key)
        c = {"s1_flagged": bool(f1), "post_cutoff": gp is not None and gp < 0, "paired": key in s0}
        if key in s0:
            f0 = sum(s0[key]) * 2 > len(s0[key])
            c.update(s0_flagged=bool(f0), s1_only=bool(f1 and not f0), s0_only=bool(f0 and not f1))
        cells[key] = c
    return cells


# ----------------------------------------------------------------------------- per-ghost and per-model results
def per_test(sc, ghosts):
    out = {"H_Reinforce": {"by_model": {}}, "H_Amplify": {"by_model": {}},
           "H_Afterlife": {"by_model": {}, "by_ghost": {}}, "H_Decay": {"by_model": {}, "by_ghost": {}},
           "H_Flag": {"by_model": {}, "by_ghost": {}, "by_control": {}}, "H_Search": {"by_model": {}, "by_ghost": {}}}
    for sl in S.TESTED_SLOTS:
        v = sc.variant(slots=[sl])
        v.perms = 0                       # correlations only; per-model p-values are not part of the report
        for cat in CATS:
            ms = market(v, cat)
            sh = v.ai_share(cat)
            ks = list(ms)
            out["H_Reinforce"]["by_model"].setdefault(sl, {})[cat] = {
                "rho": clean(S.spearman([ms[k] for k in ks], [sh[k] for k in ks])),
                "units_present": sum(sh[k] > 0 for k in ks), "n_units": len(ks)}
            a = v.h_amplify()[cat]
            out["H_Amplify"]["by_model"].setdefault(sl, {})[cat] = {
                "k": a["k"], "n": a["n"], "ratio": clean(a["ratio"]), "answers": answers(v, cat)}
        aft = v.h_afterlife()
        out["H_Afterlife"]["by_model"][sl] = {cat: {"pairs": aft[cat]["pairs"], "afterlife_pairs": aft[cat]["afterlife_pairs"],
                                                    "rate": clean(aft[cat]["rate"])} for cat in CATS}
        dec = v.h_decay()
        out["H_Decay"]["by_model"][sl] = {"pairs": dec["pairs"], "pairs_present": dec["pairs_present"],
                                          "rho": clean(dec["rho"])}
        fl = v.h_flag()
        out["H_Flag"]["by_model"][sl] = {k: clean(fl[k]) for k in ("ghost_answers", "ghost_flagged", "ghost_rate",
                                                                    "control_answers", "control_flagged", "control_rate")}
    for gid, g in ghosts.items():
        pre = [x for x in (g["by_model"][f"{sl}|S0"] for sl in S.TESTED_SLOTS) if x["pre_cutoff"]]
        out["H_Afterlife"]["by_ghost"][gid] = {"pairs": len(pre), "afterlife_pairs": sum(x["afterlife"] for x in pre),
                                               "rate": (sum(x["afterlife"] for x in pre) / len(pre)) if pre else None}
        out["H_Decay"]["by_ghost"][gid] = {"pairs": len(pre), "pairs_present": sum(x["presence"] > 0 for x in pre),
                                           "mean_presence": (sum(x["presence"] for x in pre) / len(pre)) if pre else None}
    # H_Flag by subject (as Scorer.h_flag reads the status answers: search off, tested models, pre-cutoff ghosts)
    tally = defaultdict(lambda: [0, 0])
    for r in sc.recs(tier="S", cond="S0"):
        sid = r["brand_id"]
        s = sc.subj.get(sid)
        role = s["role"] if s else ("incumbent" if sid in sc.inc else None)
        if role == "ghost":
            gp = sc.gap(sid, r["slot"])
            if gp is None or gp <= 0:
                continue
        elif role not in ("control", "incumbent"):
            continue
        t = tally[(role, sid)]
        t[0] += 1
        t[1] += sc.flagged(r, sid)
    for (role, sid), (n, k) in sorted(tally.items()):
        dest = out["H_Flag"]["by_ghost" if role == "ghost" else "by_control"]
        dest[sid] = {"role": role, "answers": n, "flagged": k, "rate": k / n if n else None}
    # H_Search by ghost and by model (cells exactly as Scorer.h_search)
    cells = search_cells(sc)
    for axis, pick in (("by_ghost", 0), ("by_model", 1)):
        agg = defaultdict(lambda: {"cells": 0, "paired_cells": 0, "s1_flagged": 0, "s0_flagged": 0, "s1_only_flagged": 0,
                                   "s0_only_flagged": 0, "post_cutoff_cells": 0, "post_cutoff_s1_flagged": 0})
        for key, c in cells.items():
            a = agg[key[pick]]
            a["cells"] += 1
            a["s1_flagged"] += c["s1_flagged"]
            if c["paired"]:
                a["paired_cells"] += 1
                a["s0_flagged"] += c["s0_flagged"]
                a["s1_only_flagged"] += c["s1_only"]
                a["s0_only_flagged"] += c["s0_only"]
            if c["post_cutoff"]:
                a["post_cutoff_cells"] += 1
                a["post_cutoff_s1_flagged"] += c["s1_flagged"]
        out["H_Search"][axis] = {k: agg[k] for k in sorted(agg)}
    return out


# ----------------------------------------------------------------------------- Discover status answers (section 3.2)
def discover_answers(sc):
    rows = []
    for r in sorted(sc.ok, key=lambda r: (r["condition"], r["slot"], r["run"])):
        if r["tier"] != "S" or r.get("brand_id") != "DISCOVER":
            continue
        rows.append({"call_id": r["call_id"], "slot": r["slot"], "model": SLOT_NAME.get(r["slot"], r["slot"]),
                     "condition": r["condition"], "run": r["run"], "flagged": bool(sc.flagged(r, "DISCOVER")),
                     "names_capital_one": "Capital One" in r["text"], "text": r["text"]})
    groups = {"tested_S0": [x for x in rows if x["condition"] == "S0" and x["slot"] in S.TESTED_SLOTS],
              "current_S1": [x for x in rows if x["condition"] == "S1"],
              "M5X_S0": [x for x in rows if x["slot"] == "M5X"]}
    summary = {g: {"answers": len(xs), "flagged": sum(x["flagged"] for x in xs),
                   "flag_rate": (sum(x["flagged"] for x in xs) / len(xs)) if xs else None,
                   "naming_capital_one": sum(x["names_capital_one"] for x in xs),
                   "flagged_and_naming_capital_one": sum(x["flagged"] and x["names_capital_one"] for x in xs)}
               for g, xs in groups.items()}
    summary["file"] = OUT_DISCOVER
    return summary, rows


def discover_md(rows, summary):
    out = ["# v0.40 status answers about Discover, in full", "",
           f"Machine-written by `osf/v40/scripts/postscore_v0_40.py` ({LABEL_PREREG}; pre-registration section 3.2, "
           "version (a): \"the status answers about Discover are shown in full in the descriptives, because an answer "
           "that says its deposits now sit with Capital One may be correct\"). Text as recorded in "
           "`osf/v40/data/v40_raw.jsonl`; \"flagged\" is the locked status-answer rule of section 2.1 "
           "(`score_v0_40.Scorer.flagged`); \"names Capital One\" is a plain substring check.", "",
           "| Group | Answers | Flagged | Name Capital One | Flagged and name Capital One |", "|---|---|---|---|---|"]
    for g in ("tested_S0", "current_S1", "M5X_S0"):
        s = summary[g]
        out.append(f"| {g} | {s['answers']} | {s['flagged']} | {s['naming_capital_one']} | "
                   f"{s['flagged_and_naming_capital_one']} |")
    out.append("")
    for x in rows:
        out += [f"## {x['model']} ({x['slot']}), search {'on' if x['condition'] == 'S1' else 'off'}, run {x['run']}", "",
                f"Call `{x['call_id']}`. Flagged: {'yes' if x['flagged'] else 'no'}. Names Capital One: "
                f"{'yes' if x['names_capital_one'] else 'no'}.", ""]
        out += ["> " + line if line.strip() else ">" for line in x["text"].splitlines()]
        out.append("")
    return "\n".join(out)


# ----------------------------------------------------------------------------- build and output
def build(root=ROOT, perms=S.PERMS):
    root = Path(root)
    man = check_inputs(root)
    sc = frozen_scorer(root, perms)
    closure = closure_checks(sc, root, perms)
    ver = json.loads((root / REL["verdicts"]).read_text(encoding="utf-8"))
    d4_ex = list(ver["sensitivity"]["S-D4"]["excluded"])
    ghosts = d2_ghosts(sc)
    disc_summary, disc_rows = discover_answers(sc)
    doc = {"_meta": {"phase": "v0.40", "script": "osf/v40/scripts/postscore_v0_40.py",
                     "deviation": "osf/v40/DEVIATIONS.md, Entries 2 and 4 (Sat 21 November 2026)",
                     "inputs": {n: {"file": REL[n], "sha256": sha256(root / REL[n])} for n in REL},
                     "locked_scorer_sha256": {"score_v0_40.py": sha256(HERE / "score_v0_40.py"),
                                              "stoprule_v0_40.py": sha256(HERE / "stoprule_v0_40.py")},
                     "coding_manifest_mentions_sha256": man["outputs"]["v40_mentions.csv"]["sha256"],
                     "permutations": perms, "closure_checks": closure,
                     "labels": {"prereg": LABEL_PREREG, "ceiling": LABEL_CEILING, "post_sensitivity": LABEL_SENS}},
           "ceiling": ceiling(sc),
           "post_sensitivity": {"label": LABEL_SENS, "discover_to_capital_one": discover_to_capital_one(sc, ver)},
           "prereg": {"label": LABEL_PREREG,
                      "d1_ai_share": d1_ai_share(sc, d4_ex),
                      "d2_ghosts": ghosts,
                      "per_test": per_test(sc, ghosts),
                      "discover_status": disc_summary}}
    return doc, discover_md(disc_rows, disc_summary)


def to_json(doc):
    return json.dumps(doc, indent=1, ensure_ascii=False, allow_nan=False) + "\n"


def main(argv=None, root=ROOT):
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--perms", type=int, default=S.PERMS)
    a = ap.parse_args(argv)
    root = Path(root)
    try:
        doc, md = build(root, a.perms)
    except Refused as e:
        print(f"REFUSED: {e} (nothing written)", file=sys.stderr)
        return 2
    js = to_json(doc)
    pj, pm = root / OUT_JSON, root / OUT_DISCOVER
    if a.check:
        same = pj.exists() and pm.exists() and pj.read_text(encoding="utf-8") == js and \
            pm.read_text(encoding="utf-8") == md + "\n"
        print("postscore outputs up to date" if same else "postscore outputs DIFFER from a fresh build")
        return 0 if same else 1
    if a.perms != S.PERMS:
        print(f"REFUSED: outputs are written only at the locked permutation count ({S.PERMS})", file=sys.stderr)
        return 2
    pj.write_text(js, encoding="utf-8")
    pm.write_text(md + "\n", encoding="utf-8")
    c = doc["ceiling"]
    print(f"wrote {OUT_JSON} and {OUT_DISCOVER}; closure checks passed")
    print(f"ceiling: airline {c['airline']['ceiling_ratio']:.6f}, bank {c['bank']['ceiling_ratio']:.6f}")
    d = doc["post_sensitivity"]["discover_to_capital_one"]
    print(f"Discover toward Capital One: bank rho {d['H_Reinforce_bank']['rho']:.6f}, bank ratio "
          f"{d['H_Amplify_bank']['ratio']:.6f}, verdicts unchanged: {d['verdicts_unchanged']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
