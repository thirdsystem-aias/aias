#!/usr/bin/env python3
"""Unit tests for the v1.20 parsing rule (synthetic replies only; no model call, no real data).

Run from the repository root:
  PYTHONDONTWRITEBYTECODE=1 python3 -m unittest scripts/test_score_v1_20.py
"""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import score_v1_11 as S  # noqa: E402
import score_v1_20 as R  # noqa: E402

GOOD = {"refers_to_brand": True, "evaluative": True, "mixed": False, "valence": 1,
        "evidence": "well regarded for build quality"}
NEUTRAL = {"refers_to_brand": True, "evaluative": False, "mixed": False, "valence": 0, "evidence": ""}


def js(d=None, **kw):
    x = dict(GOOD if d is None else d)
    x.update(kw)
    return json.dumps(x)


def rule(raw):
    """True if the v1.20 rule accepts the reply text."""
    try:
        R.parse_reply(raw)
        return True
    except S.JudgeOutputError:
        return False


def old(raw):
    """True if v1.11's locked parser accepts the reply text."""
    try:
        S.parse_judge_output(raw)
        return True
    except S.JudgeOutputError:
        return False


class TestRule(unittest.TestCase):
    def test_bare_object(self):
        self.assertTrue(old(js()) and rule(js()))
        self.assertEqual(R.parse_reply(js())["valence"], 1)

    def test_sentence_before_json(self):
        raw = "Here is my rating of the text.\n\n" + js()
        self.assertFalse(old(raw))
        self.assertTrue(rule(raw))
        self.assertEqual(R.parse_reply(raw)["evidence"], GOOD["evidence"])

    def test_json_then_trailing_text(self):
        raw = js() + "\n\nThe text praises the brand's build quality."
        self.assertFalse(old(raw))
        self.assertTrue(rule(raw))

    def test_text_on_both_sides(self):
        self.assertTrue(rule("Rating:\n" + js(NEUTRAL) + "\nDone."))

    def test_two_objects_invalid(self):
        self.assertFalse(rule(js() + "\n" + js()))                      # identical copies
        self.assertFalse(rule(js() + " " + js(valence=2)))              # different
        self.assertFalse(rule('Format: {"valence": 0}\n' + js()))      # an example object in the preamble
        self.assertFalse(rule("[" + js() + ", " + js(NEUTRAL) + "]"))   # two objects in an array

    def test_missing_key_invalid(self):
        d = dict(GOOD)
        del d["mixed"]
        self.assertFalse(rule(json.dumps(d)))
        self.assertFalse(rule("Sure. " + json.dumps(d)))

    def test_extra_key_invalid(self):
        self.assertFalse(rule(js(confidence=0.9)))

    def test_truncated_object_invalid(self):
        full = "I rate it as follows. " + js()
        for cut in (len(full) - 1, len(full) - 12, len(full) // 2, 30):
            self.assertFalse(rule(full[:cut]), cut)

    def test_code_fenced(self):
        self.assertTrue(old("```json\n" + js() + "\n```") and rule("```json\n" + js() + "\n```"))
        self.assertTrue(rule("```\n" + js() + "\n```"))
        raw = "My answer:\n```json\n" + js() + "\n```"
        self.assertFalse(old(raw))
        self.assertTrue(rule(raw))
        self.assertTrue(rule("```json\n" + js()))                       # unclosed fence: surrounding text

    def test_braces_inside_strings(self):
        raw = js(evidence="the {best} value } in its class {")
        self.assertTrue(old(raw) and rule(raw))
        self.assertEqual(len(R.top_level_objects(raw)), 1)

    def test_non_json_brace_in_text_ignored(self):
        self.assertTrue(rule("I will rate {brand} now. " + js()))
        self.assertTrue(rule("Note: { not json } " + js()))

    def test_nested_wrapper_invalid(self):
        self.assertFalse(rule(json.dumps({"rating": GOOD})))           # one top-level object, wrong keys

    def test_broken_wrapper_around_valid_object(self):
        # The wrapper does not decode, so it is surrounding text; the complete inner object counts.
        self.assertTrue(rule('{"rating": ' + js()))

    def test_single_object_in_array_counts(self):
        self.assertTrue(rule("[" + js() + "]"))

    def test_v111_checks_unchanged(self):
        self.assertFalse(rule("Ok. " + js(evaluative=False)))             # non-evaluative needs valence 0
        self.assertFalse(rule("Ok. " + js(refers_to_brand=False)))        # refers false needs 0/false/false
        self.assertFalse(rule("Ok. " + js(valence="1")))
        self.assertFalse(rule("Ok. " + js(valence=True)))
        self.assertFalse(rule("Ok. " + js(valence=3)))
        self.assertFalse(rule("Ok. " + js(valence=1.0)))
        self.assertFalse(rule("Ok. " + js(mixed="false")))
        self.assertFalse(rule("Ok. " + js(evidence=None)))
        long_q = " ".join(["word"] * 25)
        self.assertTrue(R.parse_reply("Ok. " + js(evidence=long_q))["evidence_over_limit"])  # flag only

    def test_single_quotes_and_python_literals_invalid(self):
        self.assertFalse(rule(str(GOOD)))                                 # Python repr, not JSON
        self.assertFalse(rule(js().replace("true", "True")))

    def test_empty_invalid(self):
        for raw in ("", "   \n", None):
            self.assertFalse(rule(raw))

    def test_superset_of_v111(self):
        cases = [js(), " " + js(NEUTRAL) + "\n", "```json\n" + js() + "\n```", js(evidence="a {b} c"),
                 json.dumps(GOOD, indent=2), js(valence=-2, evidence="avoid")]
        for raw in cases:
            self.assertTrue(old(raw), raw)
            self.assertTrue(rule(raw), raw)
            self.assertEqual(R.parse_reply(raw), S.parse_judge_output(raw))

    def test_reply_invalid_is_judge_output_error(self):
        self.assertTrue(issubclass(R.ReplyInvalid, S.JudgeOutputError))


class TestCap(unittest.TestCase):
    def test_cap_reasons(self):
        for fr in ("max_tokens", "incomplete:max_output_tokens", "MAX_TOKENS", "FinishReason.MAX_TOKENS", "length"):
            self.assertTrue(R.cut_by_cap(fr), fr)
        for fr in (None, "end_turn", "completed", "STOP", "FinishReason.STOP", "incomplete:content_filter", "stop_sequence"):
            self.assertFalse(R.cut_by_cap(fr), fr)

    def test_record_cut_by_cap_invalid_even_with_complete_object(self):
        rec = {"status": "ok", "served_ok": True, "finish_reason": "max_tokens", "text": js() + " and then"}
        self.assertIsNone(R.record_judgement(rec))
        rec["finish_reason"] = "end_turn"
        self.assertIsNotNone(R.record_judgement(rec))

    def test_served_model_mismatch_invalid(self):
        rec = {"status": "ok", "served_ok": False, "finish_reason": "end_turn", "text": js()}
        self.assertIsNone(R.record_judgement(rec))

    def test_empty_status_invalid(self):
        self.assertIsNone(R.record_judgement({"status": "empty", "served_ok": True, "text": ""}))


def rec(role, uid, attempt, text, status="ok", pas="main", model=None, fr="end_turn", served_ok=True):
    model = model or {"J1": "claude-opus-5-5", "J2": "gpt-6.1-sol"}[role]
    return {"role": role, "judge_model": model, "unit_id": uid, "pass": pas, "attempt": attempt,
            "status": status, "served_ok": served_ok, "finish_reason": fr, "text": text,
            "started_utc": f"2026-11-22T06:00:0{attempt}+00:00", "served_model": model}


ROLES = {"J1": "claude-opus-5-5", "J2": "gpt-6.1-sol"}
PROSE = "Here is the rating.\n"


class TestOutcomes(unittest.TestCase):
    def test_first_counting_attempt_is_used(self):
        recs = [rec("J1", "u1", 0, PROSE + js(valence=2, evidence="outstanding")), rec("J1", "u1", 1, js())]
        new, oldo = R.outcomes(recs, ROLES), S.outcomes(recs, ROLES)
        self.assertEqual(new[("J1", "u1", "main")]["status"], S.VALID)
        self.assertEqual(new[("J1", "u1", "main")]["attempt_used"], 0)
        self.assertEqual(new[("J1", "u1", "main")]["out"]["valence"], 2)
        self.assertEqual(oldo[("J1", "u1", "main")]["out"]["valence"], 1)   # v1.11 scores the retry

    def test_three_prose_replies_fail_v111_pass_v120(self):
        recs = [rec("J1", "u2", a, PROSE + js()) for a in range(3)]
        self.assertEqual(S.outcomes(recs, ROLES)[("J1", "u2", "main")]["status"], S.FAIL)
        self.assertEqual(R.outcomes(recs, ROLES)[("J1", "u2", "main")]["status"], S.VALID)

    def test_three_invalid_replies_fail_both(self):
        recs = [rec("J1", "u3", a, "I cannot rate this text.") for a in range(3)]
        self.assertEqual(R.outcomes(recs, ROLES)[("J1", "u3", "main")]["status"], S.FAIL)

    def test_api_errors_skipped_and_unjudged(self):
        recs = [rec("J1", "u4", 0, "", status="error"), rec("J1", "u4", 1, "no json here")]
        self.assertEqual(R.outcomes(recs, ROLES)[("J1", "u4", "main")]["status"], S.UNJUDGED)

    def test_other_model_records_ignored(self):
        recs = [rec("J1", "u5", 0, PROSE + js(), model="gemini-4-argon")]
        self.assertEqual(R.outcomes(recs, ROLES), {})

    def test_cap_cut_attempt_then_valid_retry(self):
        recs = [rec("J1", "u6", 0, PROSE + js(valence=2), fr="max_tokens"), rec("J1", "u6", 1, js(NEUTRAL))]
        o = R.outcomes(recs, ROLES)[("J1", "u6", "main")]
        self.assertEqual((o["status"], o["attempt_used"], o["out"]["valence"]), (S.VALID, 1, 0))

    def test_passes_kept_apart(self):
        recs = [rec("J2", "u7", 0, js()), rec("J2", "u7", 0, PROSE + js(NEUTRAL), pas="repeat")]
        o = R.outcomes(recs, ROLES)
        self.assertEqual(o[("J2", "u7", "repeat")]["out"]["valence"], 0)
        self.assertEqual(o[("J2", "u7", "main")]["out"]["valence"], 1)

    def test_two_percent_rule_reevaluated_with_v111_fail_check(self):
        units = [{"unit_id": f"u{i:03d}", "set": "F t1 v0.21", "judged": True, "j2": False} for i in range(100)]
        recs = []
        for i, u in enumerate(units):
            if i < 3:   # 3 of 100 units: prose before the JSON on all three tries
                recs += [rec("J1", u["unit_id"], a, PROSE + js()) for a in range(3)]
            else:
                recs.append(rec("J1", u["unit_id"], 0, js()))
        old_fc = S.fail_check(units, S.outcomes(recs, ROLES), ("J1",))
        new_fc = S.fail_check(units, R.outcomes(recs, ROLES), ("J1",))
        self.assertEqual(old_fc["halt"], ["J1 F t1 v0.21"])                  # 3% > 2%
        self.assertEqual(new_fc["halt"], [])
        self.assertEqual(new_fc["per_judge_set"]["J1 F t1 v0.21"]["judge_fail"], 0)


class TestClassify(unittest.TestCase):
    def test_shapes(self):
        cases = {js(): ("bare", False), "```json\n" + js() + "\n```": ("bare", True),
                 PROSE + js(): ("text_before", False), PROSE + "```json\n" + js() + "\n```": ("text_before", True),
                 js() + "\nThanks": ("text_after", False), "A\n" + js() + "\nB": ("text_before_and_after", False),
                 "": ("empty", False), "no json": ("no_object", False), js() + js(): ("several_objects", False),
                 "x " + js()[:-5]: ("no_object", False), "```json\n" + js(): ("text_before", False)}
        for raw, (shape, fenced) in cases.items():
            c = R.classify(raw)
            self.assertEqual((c["shape"], c["fenced"]), (shape, fenced), raw)

    def test_flags(self):
        c = R.classify(PROSE + js())
        self.assertEqual((c["v111_valid"], c["v120_valid"], c["object_checks"]), (False, True, "pass"))
        c = R.classify(PROSE + js(confidence=1))
        self.assertEqual((c["v120_valid"], c["object_checks"]), (False, "fail: keys differ from schema"))
        self.assertNotIn("valence", c)


def sw(**kw):
    d = dict(R.DECIDED)
    d.update(kw)
    return d


class TestSwitches(unittest.TestCase):
    def test_config_holds_pablos_answers(self):
        # Pablo, 2026-11-14, 9:04 am CT (section 15): questions 1-6 are the switches; 7-9 are recorded decisions
        answers = {"Q1_study_id": "v1.20", "Q2_scored_attempt": "first_counting", "Q3_cap_cut_reply_invalid": True,
                   "Q4_reject_identical_objects": True, "Q5_cut_answers": "keep_r4", "Q6_case_b_result": True}
        self.assertEqual(R.load_switches(), answers)
        self.assertEqual(R.DECIDED, answers)
        self.assertEqual((R.PHASE_ID, R.PREREG_TAG), ("v1.20", "v1.20-prereg-r1"))
        doc = json.loads(R.CONFIG_FILE.read_text(encoding="utf-8"))
        self.assertEqual(sorted(k for k in doc["decisions"] if k.startswith("Q")),
                         ["Q7_rule_d_E_estimate", "Q8_s_cut_identical_text", "Q9_file_renames"])

    def test_config_refuses_values_outside_options(self):
        import tempfile
        doc = json.loads(R.CONFIG_FILE.read_text(encoding="utf-8"))
        for key, bad in (("Q3_cap_cut_reply_invalid", 1), ("Q5_cut_answers", "keep_r5"), ("Q1_study_id", "v1.21")):
            d = json.loads(json.dumps(doc))
            d["switches"][key]["value"] = bad
            with tempfile.TemporaryDirectory() as t:
                p = Path(t) / "c.json"
                p.write_text(json.dumps(d), encoding="utf-8")
                with self.assertRaises(ValueError):
                    R.load_switches(p)

    def test_q4_identical_copies(self):
        raw = js() + "\n" + js()
        self.assertFalse(rule(raw))                                              # decided (Q4 true): invalid
        self.assertEqual(R.parse_reply(raw, sw(Q4_reject_identical_objects=False))["valence"], 1)
        other = js() + "\n" + js(valence=2, evidence="best in class")
        with self.assertRaises(S.JudgeOutputError):
            R.parse_reply(other, sw(Q4_reject_identical_objects=False))           # different objects stay invalid
        typed = json.dumps(NEUTRAL) + json.dumps({**NEUTRAL, "valence": False})  # 0 and false differ as JSON
        with self.assertRaises(S.JudgeOutputError):
            R.parse_reply(typed, sw(Q4_reject_identical_objects=False))

    def test_q3_cap_cut_reply(self):
        rec_ = {"status": "ok", "served_ok": True, "finish_reason": "max_tokens", "text": js()}
        self.assertIsNone(R.record_judgement(rec_))
        self.assertEqual(R.record_judgement(rec_, sw(Q3_cap_cut_reply_invalid=False))["valence"], 1)
        rec_["text"] = PROSE + js()[:20]                                          # cut object: never counts
        self.assertIsNone(R.record_judgement(rec_, sw(Q3_cap_cut_reply_invalid=False)))

    def test_q2_pick_and_q5_floors(self):
        a, b = {"a": 1}, {"b": 2}
        self.assertEqual(R.pick(a, b)[2], "S_ATT_v1_11_first")
        self.assertIs(R.pick(a, b, sw(Q2_scored_attempt="v1_11_first"))[0], b)
        self.assertEqual([(R.r_floor(sw(Q5_cut_answers=v)), R.primary_drops_cut(sw(Q5_cut_answers=v)))
                          for v in ("keep_r4", "keep_r6", "drop_r4", "drop_r6")],
                         [(4, False), (6, False), (4, True), (6, True)])


class TestStageLogic(unittest.TestCase):
    def test_s_att_takes_v111_judgement_where_valid(self):
        recs = [rec("J1", "u1", 1, PROSE + js(valence=2, evidence="outstanding")), rec("J1", "u1", 2, js()),
                rec("J1", "u2", 1, PROSE + js()), rec("J1", "u2", 2, PROSE + js()), rec("J1", "u2", 3, PROSE + js())]
        o111, o120 = S.outcomes(recs, ROLES), R.outcomes(recs, ROLES)
        att = R.outcomes_v111_first(o111, o120)
        self.assertEqual(att[("J1", "u1", "main")]["out"]["valence"], 1)        # v1.11's retry
        self.assertEqual(o120[("J1", "u1", "main")]["out"]["valence"], 2)       # v1.20: first counting
        self.assertEqual(att[("J1", "u2", "main")]["status"], S.VALID)          # v1.11 JUDGE_FAIL -> v1.20's
        self.assertEqual(R.v111_attempts_used(recs, ROLES), {("J1", "u1", "main"): 2})

    def test_comparison_counts(self):
        recs = [rec("J1", "u1", 1, PROSE + js()), rec("J1", "u1", 2, js()),
                rec("J1", "u2", 1, PROSE + js()), rec("J1", "u2", 2, PROSE + js()), rec("J1", "u2", 3, PROSE + js()),
                rec("J1", "u3", 1, js(), fr="max_tokens")]
        o111, o120 = S.outcomes(recs, ROLES), R.outcomes(recs, ROLES)
        units = [{"unit_id": u, "set": "F t1 v0.20", "judged": True, "j2": False} for u in ("u1", "u2", "u3")]
        fcs = {"v1.11": S.fail_check(units, o111, ("J1",)), "v1.20": S.fail_check(units, o120, ("J1",))}
        c = R.comparison(recs, ROLES, o111, o120, fcs)
        self.assertEqual(c["status_transitions_v1_11_to_v1_20"],
                         {"J1 main: JUDGE_FAIL -> VALID": 1, "J1 main: VALID -> UNJUDGED": 1, "J1 main: VALID -> VALID": 1})
        self.assertEqual(c["valid_under_both_from_a_different_attempt"]["J1 main"], {"n": 1, "unit_ids": ["u1"]})
        self.assertEqual(c["judge_fail_by_judge_set"]["J1 F t1 v0.20"]["v1.11"]["judge_fail"], 1)

    def test_v111_stage_j_state(self):
        import tempfile
        from types import SimpleNamespace
        units = [{"unit_id": f"u{i}", "set": "F t1 v0.20", "judged": True, "j2": False} for i in range(10)]
        fail = [rec("J1", "u0", a, PROSE + js()) for a in (1, 2, 3)] + [rec("J1", f"u{i}", 1, js()) for i in range(1, 10)]
        ok = [rec("J1", f"u{i}", 1, js()) for i in range(10)]
        with tempfile.TemporaryDirectory() as t:
            run = SimpleNamespace(ctx=SimpleNamespace(dry=True, outdir=t))
            st = R.v111_stage_j_state(run, units, fail, ROLES)
            self.assertEqual((st["state"], st["case"], st["halt"]), ("halted", "B", ["J1 F t1 v0.20"]))
            with self.assertRaises(S.Halt):                                      # v1.11 Stage J not run yet
                R.v111_stage_j_state(run, units, ok, ROLES)
            (Path(t) / S.STAGE_J_NAME).write_text("{}", encoding="utf-8")
            self.assertEqual(R.v111_stage_j_state(run, units, ok, ROLES)["case"], "A")

    def test_scores_r_floor(self):
        units, recs = [], []
        for blk, n in (("R", 4), ("F", 4)):
            for i in range(n):
                uid = f"{blk}{i}"
                units.append({"unit_id": uid, "block": blk, "wave": "t3", "category": "v0.23", "brand": "B1",
                              "judged": True, "j2": False, "answer_id": uid})
                recs.append(rec("J1", uid, 1, js()))
        oc = R.outcomes(recs, ROLES)
        s6, s4 = R.scores(units, oc, "J1"), R.scores(units, oc, "J1", rfloor=4)
        self.assertFalse(s6[("R", "t3", "v0.23", "B1")]["rated"])
        self.assertTrue(s4[("R", "t3", "v0.23", "B1")]["rated"])
        self.assertFalse(s4[("F", "t3", "v0.23", "B1")]["rated"])               # F keeps the floor of 6
        keep = R.both(lambda u: u["unit_id"] != "R0", None)
        self.assertEqual(R.scores(units, oc, "J1", keep, rfloor=4)[("R", "t3", "v0.23", "B1")]["n"], 3)
        self.assertIsNone(R.both(None, None))

    def test_load_cut(self):
        import tempfile
        with tempfile.TemporaryDirectory() as t:
            c, j = Path(t) / "c.csv", Path(t) / "c.json"
            c.write_text("block,answer_id\nR,R t3 v0.23::gemini-2.5-flash|S01\n", encoding="utf-8")
            j.write_text(json.dumps({"s_cut_m_cells": [["R", "v0.23", "gemini-2.5-flash"]]}), encoding="utf-8")
            ids, cells, meta = R.load_cut(c, j)
            self.assertEqual((ids, cells, meta["answers_flagged"]),
                             ({"R t3 v0.23::gemini-2.5-flash|S01"}, {("R", "v0.23", "gemini-2.5-flash")}, 1))


class TestCutList(unittest.TestCase):
    def test_list_and_summary_agree(self):
        import csv
        with open(R.CUT_CSV, encoding="utf-8", newline="") as f:
            rows = list(csv.DictReader(f))
        js = json.loads(R.CUT_JSON.read_text(encoding="utf-8"))
        self.assertEqual(len(rows), js["rows"])
        self.assertEqual(len({r["answer_id"] for r in rows}), len(rows))
        cells = sorted(k.split("|") for k, (cut, n) in js["t3_answers_and_cut_by_cell"].items() if cut and 2 * cut >= n)
        self.assertEqual(cells, sorted(js["s_cut_m_cells"]))
        for r in rows:
            self.assertEqual(r["unit_status"], "kept" if int(r["v1_11_units"]) else "none")
            self.assertIn(r["evidence_class"], ("finish_reason", "tokens_at_cap", "identical_to_t3 (inferred)"))

    def test_answers_7_and_8(self):
        # question 7: rule (d) dropped, no E row and no estimate row; question 8: S-CUT takes the 8 rows
        # flagged by identical text (rule (c): R 4, F 4) with every other row of the list
        import csv
        from collections import Counter
        with open(R.CUT_CSV, encoding="utf-8", newline="") as f:
            rows = list(csv.DictReader(f))
        self.assertEqual([r for r in rows if r["block"] not in ("R", "F")], [])
        self.assertEqual([r for r in rows if "estimate" in r["evidence_class"]], [])
        ident = [r for r in rows if r["evidence_class"] == "identical_to_t3 (inferred)"]
        self.assertEqual(sorted(Counter(r["block"] for r in ident).items()), [("F", 4), ("R", 4)])
        ids, _, meta = R.load_cut(R.CUT_CSV, R.CUT_JSON)
        self.assertTrue({r["answer_id"] for r in ident} <= ids)
        self.assertEqual((len(ids), meta["answers_flagged"]), (66, 66))


class TestLock(unittest.TestCase):
    def test_imported_scorers_equal_v111_lock_manifest(self):
        self.assertEqual(R.v111_integrity(), [])

    def test_lock_files(self):
        self.assertEqual(len(R.LOCK_FILES), len(set(R.LOCK_FILES)))
        for p in (R.V111_LOCK_MANIFEST, "scripts/score_v1_11.py", "scripts/score_v1_10.py", "scripts/score_v1_20.py",
                  "osf/methodology/v1_20/prereg/config_v1_20.json", "osf/methodology/v1_20/scoping/cut_units_v1_20.csv"):
            self.assertIn(p, R.LOCK_FILES)
        self.assertNotIn("osf/methodology/v1_20/prereg/LOCK_MANIFEST_v1_20.sha256", R.LOCK_FILES)

    def test_anchor_problems(self):
        why = R.anchor_problems(R.anchor_template())
        self.assertTrue(any("osf_deposit" in w for w in why) and any("tag" in w for w in why))
        a = {k: "x" for k in R.ANCHOR_FIELDS} | {"tag": "v1.11-prereg-r1", "locked_files": {p: {} for p in R.LOCK_FILES}}
        self.assertEqual(R.anchor_problems(a), ["anchor tag v1.11-prereg-r1 is not v1.20-prereg-r1"])
        a["tag"] = R.PREREG_TAG
        self.assertEqual(R.anchor_problems(a), [])
        self.assertEqual(len(R.anchor_problems(a, commit="abc")), 1)


if __name__ == "__main__":
    unittest.main()
