"""Tests of ai_check_v0_62.py (DEVIATIONS Entry 2) on fakes: no network, no model, no SDK."""
import hashlib
import inspect
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest import mock
from zoneinfo import ZoneInfo

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import ai_check_v0_62 as A  # noqa: E402

CT = ZoneInfo("America/Chicago")


def payload(prompt):
    m = re.search(r"(?:Items|Aliases) \(JSON\):\n(.*)\Z", prompt, re.S)
    return json.loads(m.group(1))


def check_of(prompt):
    if prompt.startswith("Translate literally"):
        return "C1"
    if prompt.startswith("You are reviewing"):
        return "C2"
    if prompt.startswith("Each item below gives an English source"):
        return "C3"
    return "C4"


def is_korean(prompt):
    return re.search("[가-힣]", prompt) is not None


def reply_for(prompt, code=None):
    """A valid reply. code(check, id, korean) -> code string (C2 equivalence / C3 code / C4 usage) or None for the
    default; korean: the prompt carries Hangul (a KO call)."""
    c = check_of(prompt)
    rows = payload(prompt)
    out = []
    for r in rows:
        k = code(c, r["id"], is_korean(prompt)) if code else None
        if c == "C1":
            out.append({"id": r["id"], "english": "back " + r["text"]})
        elif c == "C2":
            out.append({"id": r["id"], "equivalence": k or "equivalent", "naturalness": "natural",
                        "category_scope": False, "speech_act_format": False, "added_or_removed": False,
                        "reason": "fine."})
        elif c == "C3":
            out.append({"id": r["id"], "code": k or "equivalent", "reason": "fine."})
        else:
            out.append({"id": r["id"], "usage": k or "standard", "common_word": False, "reason": "fine."})
    key = "aliases" if c == "C4" else "items"
    return "Here is the JSON:\n```json\n" + json.dumps({key: out}, ensure_ascii=False) + "\n```"


class FakeSender:
    def __init__(self, code=None, fail=None, garble=None, tokens_out=3000):
        self.calls, self.code, self.fail, self.garble, self.tokens_out = [], code, fail or {}, garble or {}, tokens_out

    def __call__(self, model, prompt):
        c = check_of(prompt)
        self.calls.append((c, model, prompt))
        n = sum(1 for x in self.calls if x[0] == c and x[2] == prompt)
        if self.fail.get(c, 0) >= n:
            raise RuntimeError("fake transient")
        text = "I cannot comply." if self.garble.get(c, 0) >= n else reply_for(prompt, self.code)
        if self.tokens_out == "cap":       # every reply at its worst case: input = prompt bytes, output at the cap
            tin, tout = len(prompt.encode("utf-8")), A.OUTPUT_CAP
            th = A.OUTPUT_CAP if model.startswith("gemini") else None
        else:
            tin, tout, th = 4000, self.tokens_out, (0 if model.startswith("gemini") else None)
        return {"text": text, "served_model": model, "finish_reason": "completed", "tokens_in": tin,
                "tokens_out": tout, "tokens_thought": th, "paused_continued": False, "search": None}


class Frozen(unittest.TestCase):
    def test_frozen_files_match(self):
        self.assertEqual(A.frozen_problems(), [])
        self.assertEqual(set(A.FROZEN), {f"c{i}_instruction.txt" for i in range(1, 5)} |
                         {f"c{i}_schema.json" for i in range(1, 5)} | {"check_params.json"})

    def test_frozen_detects_change(self):
        with tempfile.TemporaryDirectory() as d:
            for n in A.FROZEN:
                Path(d, n).write_bytes((A.FROZEN_DIR / n).read_bytes())
            self.assertEqual(A.frozen_problems(d), [])
            Path(d, "c1_instruction.txt").write_text("changed", encoding="utf-8")
            self.assertEqual(len(A.frozen_problems(d)), 1)

    def test_entry2_constants(self):
        p = A.params()
        self.assertEqual(p["seed"], 20261121)
        self.assertEqual(p["cap_usd"], 8.0)
        self.assertEqual(p["models"], {"C1": "gpt-6-astra", "C2": "gpt-6-astra", "C3": "gemini-4-argon",
                                       "C4": "gpt-6-astra"})
        self.assertEqual(p["languages"]["C4"], ["ko", "zh"])
        self.assertTrue(A.frozen_text("c1_instruction.txt").startswith("Translate literally into English."))
        self.assertEqual(A.schema_enum("C2", "equivalence"), A.EQ_CODES)
        self.assertEqual(A.schema_enum("C3", "code"), A.EQ_CODES)
        self.assertEqual(A.schema_enum("C2", "naturalness"), ("natural", "acceptable", "unnatural"))
        self.assertEqual(A.schema_enum("C4", "usage"), ("standard", "acceptable variant", "not used for this brand",
                                                        "unknown"))
        import acquire_v0_62 as Q
        self.assertEqual(A.OUTPUT_CAP, Q.CURRENT_MAX_TOKENS)
        self.assertEqual(A.LAST_DAY_END, datetime(2026, 11, 29, tzinfo=CT))

    def test_provider_defaults_in_helpers(self):
        import acquire_v0_62 as Q
        for fn in (Q.call_openai_current, Q.call_google_current):
            src = inspect.getsource(fn)
            for w in ("temperature", "top_p", "top_k", "reasoning_effort", "\"reasoning\"", "thinking_config"):
                self.assertNotIn(w, src, (fn.__name__, w))
        seen = []
        with mock.patch.object(Q, "call_openai_current", lambda *a, **k: seen.append(("o", a, k)) or {}), \
                mock.patch.object(Q, "call_google_current", lambda *a, **k: seen.append(("g", a, k)) or {}):
            A.helper_sender("gpt-6-astra", "p")
            A.helper_sender("gemini-4-argon", "q")
        self.assertEqual(seen, [("o", ("gpt-6-astra", "p", False), {}), ("g", ("gemini-4-argon", "q", False), {})])


class Items(unittest.TestCase):
    def test_counts_and_consistency(self):
        self.assertEqual(A.consistency_problems(), [])
        for lg in A.LANGS:
            its = A.items(lg)
            self.assertEqual(len(its), 50)
            self.assertEqual([x["kind"] for x in its].count("phase_b"), 30)
            self.assertEqual([x["kind"] for x in its].count("template"), 5)
            self.assertEqual([x["kind"] for x in its].count("label"), 15)
            self.assertEqual(len({x["key"] for x in its}), 50)
            self.assertEqual(sum(1 for x in its if x["claude"]), 35)

    def test_alias_rows(self):
        ko, zh = A.alias_rows("ko"), A.alias_rows("zh")
        self.assertEqual(len({(r["substrate"], r["brand"]) for r in ko}), 88)
        self.assertEqual(len({(r["substrate"], r["brand"]) for r in zh}), 44)
        self.assertEqual((len(ko), len(zh)), (94, 48))
        self.assertEqual(ko[0]["id"], "a001")
        rows_ko = {(r["substrate"], r["brand"], r["status"]) for r in ko}
        self.assertEqual(sum(1 for r in rows_ko if r[2] == "UNCONFIRMED"), 84)
        self.assertEqual(sum(1 for r in rows_ko if r[2] == "PARTLY"), 4)

    def test_plan(self):
        self.assertEqual(A.plan(), [("C1", "es"), ("C3", "es"), ("C2", "es"), ("C1", "ko"), ("C3", "ko"),
                                    ("C2", "ko"), ("C1", "zh"), ("C3", "zh"), ("C2", "zh"), ("C4", "ko"),
                                    ("C4", "zh")])


class Blindness(unittest.TestCase):
    def test_ids_seeded_permutation(self):
        b1, b2 = A.blind_ids(), A.blind_ids()
        self.assertEqual(b1, b2)
        for lg in A.LANGS:
            self.assertEqual(sorted(b1[lg].values()), [f"i{n:02d}" for n in range(1, 51)])
            order = [b1[lg][x["key"]] for x in A.items(lg)]
            self.assertNotEqual(order, sorted(order))              # renumbered, not file order
        self.assertNotEqual(A.blind_ids(seed=1), b1)

    def test_c1_sees_target_only(self):
        tr = A.load_translations()
        for lg in A.LANGS:
            p = A.c1_prompt(lg)
            rows = payload(p)
            self.assertEqual(set(rows[0]), {"id", "text"})
            self.assertEqual([r["id"] for r in rows], sorted(r["id"] for r in rows))
            for x in A.items(lg):
                self.assertIn(json.dumps(x["target"], ensure_ascii=False)[1:-1], p)
                if x["kind"] != "label" and x["en"] != x["target"]:
                    self.assertNotIn(x["en"], p)
            for x in tr["phase_b"]:
                self.assertNotIn(x["probe_id"], p)
                self.assertNotIn(x[lg + "_back"], p)
                if x.get("notes"):
                    self.assertNotIn(str(x["notes"])[:40], p)
            for w in ("v19", "v20", "v21", "v22", "v23", "drift", "equivalent", "phase_b", "template__", "label__"):
                self.assertNotIn(w, p)

    def test_c2_sees_source_and_target_not_claude(self):
        tr = A.load_translations()
        for lg in A.LANGS:
            p = A.c2_prompt(lg)
            self.assertIn(A.params()["variety"][lg], p)
            for x in A.items(lg):
                self.assertIn(json.dumps(x["en"], ensure_ascii=False)[1:-1], p)
                self.assertIn(json.dumps(x["target"], ensure_ascii=False)[1:-1], p)
            for x in tr["phase_b"]:
                if x[lg + "_back"] != x["en"]:
                    self.assertNotIn(json.dumps(x[lg + "_back"], ensure_ascii=False)[1:-1], p)
                self.assertNotIn(x["probe_id"], p)
            self.assertEqual(set(payload(p)[0]), {"id", "english", "translation"})

    def test_c3_sees_source_and_back_only(self):
        for lg in A.LANGS:
            ids = A.blind_ids()[lg]
            back = {i: f"BACK-{i}" for i in ids.values()}
            p = A.c3_prompt(lg, back)
            self.assertEqual(set(payload(p)[0]), {"id", "source", "back_translation"})
            for x in A.items(lg):
                self.assertIn(f"BACK-{ids[x['key']]}", p)
                if x["kind"] == "phase_b":
                    self.assertNotIn(json.dumps(x["target"], ensure_ascii=False)[1:-1], p)

    def test_c4_hides_status_and_source(self):
        for lg in ("ko", "zh"):
            p = A.c4_prompt(lg)
            for w in ("UNCONFIRMED", "PARTLY", "CONFIRMED", "http", "accessed", "2026-11-11"):
                self.assertNotIn(w, p)
            rows = payload(p)
            self.assertEqual(set(rows[0]), {"id", "brand", "category", "alias"})
            self.assertEqual(len(rows), len(A.alias_rows(lg)))


class Extraction(unittest.TestCase):
    def setUp(self):
        self.p = A.c1_prompt("es")
        self.ids = A.expected_ids("C1", "es")

    def test_surrounding_text_and_fence(self):
        obj, why = A.extract("C1", reply_for(self.p), self.ids)
        self.assertIsNone(why)
        self.assertEqual(len(obj["items"]), 50)

    def test_missing_extra_duplicate(self):
        good = json.loads(reply_for(self.p).split("```json\n")[1].split("\n```")[0])
        bad = {"items": good["items"][:-1]}
        self.assertIsNone(A.extract("C1", json.dumps(bad), self.ids)[0])
        bad = {"items": good["items"] + [{"id": "i99", "english": "x"}]}
        self.assertIsNone(A.extract("C1", json.dumps(bad), self.ids)[0])
        bad = {"items": good["items"][:-1] + [good["items"][0]]}
        self.assertIsNone(A.extract("C1", json.dumps(bad), self.ids)[0])
        self.assertIsNone(A.extract("C1", "no json here", self.ids)[0])
        self.assertIsNone(A.extract("C1", json.dumps(good)[:-3], self.ids)[0])      # truncated

    def test_codes_and_booleans(self):
        p2 = A.c2_prompt("ko")
        ids = A.expected_ids("C2", "ko")
        good = json.loads(reply_for(p2).split("```json\n")[1].split("\n```")[0])
        good["items"][0]["equivalence"] = "  Meaning Change "
        obj, why = A.extract("C2", json.dumps(good), ids)
        self.assertIsNone(why)
        self.assertEqual(A.entries("C2", obj)[good["items"][0]["id"]]["equivalence"], "meaning change")
        good["items"][0]["equivalence"] = "different"
        self.assertIsNone(A.extract("C2", json.dumps(good), ids)[0])
        good["items"][0]["equivalence"] = "equivalent"
        good["items"][1]["category_scope"] = "false"
        self.assertIsNone(A.extract("C2", json.dumps(good), ids)[0])

    def test_first_valid_object_wins(self):
        txt = '{"note": 1} then ' + reply_for(self.p)
        self.assertIsNotNone(A.extract("C1", txt, self.ids)[0])


class Guards(unittest.TestCase):
    def test_date(self):
        self.assertTrue(A.date_check(datetime(2026, 11, 28, 23, 59, tzinfo=CT))[0])
        self.assertFalse(A.date_check(datetime(2026, 11, 29, 0, 0, tzinfo=CT))[0])
        self.assertFalse(A.date_check(datetime(2026, 11, 29, 6, 0, tzinfo=timezone.utc))[0])   # = 00:00 CT
        self.assertTrue(A.date_check(datetime(2026, 11, 29, 5, 59, tzinfo=timezone.utc))[0])

    def test_answer_files(self):
        with tempfile.TemporaryDirectory() as d:
            paths = [Path(d, "data", "v62_raw.jsonl"), Path(d, "data", "coded")]
            self.assertEqual(A.answer_files(paths), [])
            paths[0].parent.mkdir()
            paths[0].write_text("")
            self.assertEqual(A.answer_files(paths), [str(paths[0])])
        self.assertEqual(A.STUDY_ANSWER_PATHS[0], A.V62 / "data" / "v62_raw.jsonl")

    def test_addendum(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d, "D.md")
            sha = A.sha256_file(A.HERE)
            p.write_text("## Entry 1 — x\n" + sha + "\n## Entry 2 — y\nno hash\n", encoding="utf-8")
            self.assertFalse(A.addendum_names_script(p))                # in Entry 1 only
            p.write_text("## Entry 1 — x\n\n## Entry 2 — y\n**Addendum** " + sha + "\n", encoding="utf-8")
            self.assertTrue(A.addendum_names_script(p))

    def test_other_paid_runs(self):
        ps = ("100 1 /bin/zsh\n101 100 python3 ai_check_v0_62.py --run\n"
              "200 1 python3 osf/v62/scripts/acquire_v0_62.py --collect\n"
              "201 1 python3 acquire_v0_62.py --dry-run\n"
              "202 1 python3 sentiment_judge_v1.py --run\n"
              "203 1 python3 other_ai_check_v0_62.py --run\n"
              "204 1 vim notes.txt\n")
        hits = {p for p, _ in A.other_paid_runs(ps, me=101)}
        self.assertEqual(hits, {200, 202, 203})

    def test_model_check_today(self):
        now = datetime(2026, 11, 22, 15, 0, tzinfo=timezone.utc)
        with tempfile.TemporaryDirectory() as d:
            self.assertIsNone(A.model_check_today(now, d))
            rec = {"central_date": "2026-11-22", "models": {"gpt-6-astra": {"found": True},
                                                             "gemini-4-argon": {"found": True}}}
            Path(d, "model_check_x.json").write_text(json.dumps(rec))
            self.assertIsNotNone(A.model_check_today(now, d))
            self.assertIsNone(A.model_check_today(datetime(2026, 11, 23, 15, 0, tzinfo=timezone.utc), d))
            rec["models"]["gemini-4-argon"]["found"] = False
            Path(d, "model_check_x.json").write_text(json.dumps(rec))
            self.assertIsNone(A.model_check_today(now, d))

    def test_run_refused_without_addendum_sends_nothing(self):
        with mock.patch.object(A, "run_checks", side_effect=AssertionError("must not run")), \
                mock.patch.object(A, "addendum_names_script", return_value=False), \
                mock.patch.object(A, "_ps", return_value=""):
            self.assertEqual(A.main(["--run"]), 3)

    def test_run_refused_after_window_start(self):
        with mock.patch.object(A, "addendum_names_script", return_value=True), \
                mock.patch.object(A, "model_check_today", return_value="x"), \
                mock.patch.object(A, "_ps", return_value=""):
            self.assertEqual(A.run_guards(datetime(2026, 11, 28, 12, tzinfo=CT)), [])
            bad = A.run_guards(datetime(2026, 11, 29, 0, 1, tzinfo=CT))
            self.assertEqual(len(bad), 1)
            self.assertIn("on or after", bad[0])


class DryRun(unittest.TestCase):
    def test_no_sdk_no_network(self):
        code = (
            "import socket, sys\n"
            "def boom(*a, **k): raise AssertionError('network used')\n"
            "socket.socket.connect = boom; socket.create_connection = boom\n"
            f"sys.path.insert(0, {str(HERE.parent)!r})\n"
            "import ai_check_v0_62 as A\n"
            "A._ps = lambda: ''\n"
            "rc = A.main(['--dry-run'])\n"
            "bad = [m for m in sys.modules if m.split('.')[0] in ('openai', 'anthropic', 'httpx')\n"
            "       or m.startswith('google.genai')]\n"
            "print('SDK', bad); sys.exit(rc)\n")
        r = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, timeout=120)
        self.assertEqual(r.returncode, 0, r.stderr + r.stdout)
        self.assertIn("SDK []", r.stdout)
        self.assertIn("central $3.43, high $6.75", r.stdout)
        self.assertIn("items = locked stimuli: OK", r.stdout)

    def test_entry2_estimate(self):
        cen, high = A.entry2_estimate()
        self.assertAlmostEqual(cen, 3.431, places=3)
        self.assertAlmostEqual(high, 6.751, places=3)

    def test_worst_case(self):
        p = "x" * 1000
        self.assertAlmostEqual(A.worst_case("gpt-6-astra", p), ((1000 + 512) * 10 + 16384 * 50) / 1e6)
        self.assertAlmostEqual(A.worst_case("gemini-4-argon", p), ((1000 + 512) * 4 + 2 * 16384 * 20) / 1e6)


class Run(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.TemporaryDirectory()
        self.raw = Path(self.d.name, "raw.jsonl")

    def tearDown(self):
        self.d.cleanup()

    def test_happy_path(self):
        s = FakeSender()
        self.assertEqual(A.run_checks(self.raw, s, log=lambda *_: None), "done")
        lines = A.read_raw(self.raw)
        self.assertEqual([x["call_key"] for x in lines], [f"{c}|{l}" for c, l in A.plan()])
        self.assertTrue(all(x["parse_ok"] and x["attempt"] == 1 and x["cost_basis"] == "usage" for x in lines))
        c3 = [p for c, _m, p in s.calls if c == "C3"][0]
        self.assertIn("back ", c3)                                     # C1's reply reaches C3
        self.assertEqual({m for c, m, _ in s.calls if c == "C3"}, {"gemini-4-argon"})
        self.assertAlmostEqual(lines[0]["cost_usd"], (4000 * 10 + 3000 * 50) / 1e6)
        self.assertEqual(A.run_checks(self.raw, FakeSender(), log=lambda *_: None), "done")   # resumable: no re-send
        self.assertEqual(len(A.read_raw(self.raw)), 11)

    def test_one_resend_on_failure(self):
        s = FakeSender(fail={"C1": 1}, garble={"C2": 1})
        self.assertEqual(A.run_checks(self.raw, s, log=lambda *_: None), "done")
        lines = A.read_raw(self.raw)
        es = [x for x in lines if x["call_key"] == "C1|es"]
        self.assertEqual([x["attempt"] for x in es], [1, 2])
        self.assertEqual(es[0]["cost_basis"], "worst_case (no usage)")
        self.assertAlmostEqual(es[0]["cost_usd"], es[0]["worst_case_reserved_usd"])
        c2 = [x for x in lines if x["call_key"] == "C2|es"]
        self.assertEqual([x["parse_ok"] for x in c2], [False, True])

    def test_at_most_two_attempts_across_invocations(self):
        s = FakeSender(fail={"C1": 99})
        self.assertEqual(A.run_checks(self.raw, s, log=lambda *_: None), "incomplete")
        lines = A.read_raw(self.raw)
        self.assertEqual(sum(1 for x in lines if x["check"] == "C1"), 6)       # 3 languages x 2
        self.assertFalse(any(x["check"] == "C3" for x in lines))             # C3 needs C1
        n = len(lines)
        self.assertEqual(A.run_checks(self.raw, FakeSender(), log=lambda *_: None), "incomplete")
        self.assertEqual(sum(1 for x in A.read_raw(self.raw) if x["check"] == "C1"), 6)
        self.assertEqual(len(A.read_raw(self.raw)), n)

    def test_cap_stops_before_a_call_whose_worst_case_would_pass(self):
        msgs = []
        s = FakeSender(tokens_out="cap")
        st = A.run_checks(self.raw, s, log=msgs.append)
        lines = A.read_raw(self.raw)
        self.assertEqual(st, "stop")
        tot = A.spent(lines)
        self.assertLessEqual(tot, 8.0)
        for x in lines:
            self.assertLessEqual(x["cost_usd"], x["worst_case_reserved_usd"] + 1e-12)
        nxt = [(c, l) for c, l in A.plan() if not any(y["call_key"] == f"{c}|{l}" for y in lines)][0]
        prompt = A.build_prompt(nxt[0], nxt[1], lines)
        self.assertGreater(tot + A.worst_case(A.model_of(nxt[0]), prompt), 8.0)
        self.assertTrue(any(m.startswith("STOP before") for m in msgs))

    def test_cap_counts_recorded_spend_from_file(self):
        rec = {"call_key": "X|es", "check": "X", "language": "es", "cost_usd": 7.5, "parse_ok": False}
        self.raw.write_text(json.dumps(rec) + "\n")
        s = FakeSender()
        self.assertEqual(A.run_checks(self.raw, s, log=lambda *_: None), "stop")
        self.assertEqual(s.calls, [])


class Analyze(unittest.TestCase):
    def test_kappa_known(self):
        E, M, C = A.EQ_CODES
        a, b = [E, E, E, M, M], [E, E, M, M, M]
        self.assertAlmostEqual(A.kappa(a, b), (0.8 - 0.48) / 0.52)
        self.assertIsNone(A.kappa([E, E], [E, E]))                      # chance agreement 1: undefined
        self.assertEqual(A.kappa([E, M], [E, M]), 1.0)
        # linear weighted kappa against the disagreement form 1 - sum(v O) / sum(v E), v = |i - j|
        a, b = [E, M, C, E, C, M, E], [E, C, C, M, M, M, E]
        ix = {E: 0, M: 1, C: 2}
        n = len(a)
        O = [[0.0] * 3 for _ in range(3)]
        for x, y in zip(a, b):
            O[ix[x]][ix[y]] += 1 / n
        ra = [sum(r) for r in O]
        cb = [sum(O[i][j] for i in range(3)) for j in range(3)]
        num = sum(abs(i - j) * O[i][j] for i in range(3) for j in range(3))
        den = sum(abs(i - j) * ra[i] * cb[j] for i in range(3) for j in range(3))
        self.assertAlmostEqual(A.kappa(a, b, weighted=True), 1 - num / den)
        ag = A.agreement(a, b)
        self.assertAlmostEqual(ag["agreement_pct"], 100 * 4 / 7)

    def _run(self, code):
        with tempfile.TemporaryDirectory() as d:
            raw = Path(d, "raw.jsonl")
            A.run_checks(raw, FakeSender(code=code), log=lambda *_: None)
            return A.analyze(A.read_raw(raw))

    def test_flags_rule_e_and_counts(self):
        ids = A.blind_ids()["ko"]
        pb = [x["key"] for x in A.items("ko") if x["kind"] == "phase_b"]
        strict = {ids[k] for k in pb[:7]}                    # 7 > 6 strictly flagged in KO
        one = {ids[pb[7]]}                                    # C2 only
        tmpl = {ids["template__v21"]}
        off_ids = {"a001", "a002"}
        ko_c2 = A.c2_prompt("ko")

        def code(c, i, korean):
            if c == "C4" and i in off_ids:
                return "not used for this brand"
            if not korean:
                return None
            if c == "C2" and (i in strict or i in one or i in tmpl):
                return "meaning change"
            if c == "C3" and i in strict:
                return "meaning change"
            return None
        res, s_trans, s_alias = self._run(code)
        ko = res["languages"]["ko"]
        self.assertEqual(len(ko["phase_b_strictly_flagged"]), 7)
        self.assertEqual(len(ko["phase_b_flagged"]), 8)
        self.assertTrue(ko["rule_e_decision"])
        self.assertEqual(ko["templates_flagged"], ["template__v21"])
        self.assertIn("template_note", ko)
        self.assertEqual(sorted(s_trans["ko"]["strictly_flagged"]), sorted(pb[:7]))
        self.assertTrue(all("|" in k for k in s_trans["ko"]["flagged"]))
        self.assertFalse(res["languages"]["es"]["rule_e_decision"])
        self.assertEqual(res["languages"]["es"]["flagged"], [])
        # C2 equivalence differs from C3 on 8 + 1 template KO items; Claude has no code on the 15 labels
        pr = ko["pairs"]
        self.assertEqual(pr["c2_vs_c3"]["n"], 50)
        self.assertEqual(pr["claude_vs_c2"]["n"], 35)
        self.assertAlmostEqual(pr["c2_vs_c3"]["agreement_pct"], 100 * (50 - 2) / 50)
        self.assertEqual(ko["c2_naturalness"], {"natural": 50})
        self.assertEqual(ko["c2_checklist_counts"], {"category_scope": 0, "speech_act_format": 0, "added_or_removed": 0})
        a = res["aliases"]["ko"]
        self.assertEqual(a["usage_counts"], {"standard": 92, "not used for this brand": 2})
        self.assertAlmostEqual(a["share_not_used"], 2 / 94)
        self.assertEqual(len(s_alias["ko"]["off"]), 2)
        self.assertTrue(s_alias["zh"]["complete"])
        self.assertEqual(len(s_alias["zh"]["off"]), 2)                 # a001/a002 exist in ZH too
        self.assertGreater(len(ko_c2), 0)

    def test_missing_reply_reported(self):
        with tempfile.TemporaryDirectory() as d:
            raw = Path(d, "raw.jsonl")
            A.run_checks(raw, FakeSender(fail={"C3": 99}), log=lambda *_: None)
            res, s_trans, _ = A.analyze(A.read_raw(raw))
        self.assertFalse(res["languages"]["es"]["c3_available"])
        self.assertEqual(res["languages"]["es"]["pairs"]["c2_vs_c3"]["n"], 0)
        self.assertFalse(s_trans["es"]["complete"])


if __name__ == "__main__":
    unittest.main()
