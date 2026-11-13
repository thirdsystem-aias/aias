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


if __name__ == "__main__":
    unittest.main()
