#!/usr/bin/env python3
"""Tests for papers/v1_19/fill_paper_v1_19.py (run: python3 papers/v1_19/tests/test_fill_paper_v1_19.py).

  - the fill refuses a wrong pre-registration tag, a wrong verdicts SHA-256 and a tag/anchor mismatch
  - every number in the filled draft is fixed template text or the text of a recorded value in the provenance, and
    every recorded JSON value re-resolves from its path
  - Samsung appears only in the Conflict of interest paragraph (never in the title page, author block or abstract)
  - the AI-use statement is verbatim CLAUDE.md's and follows Ethics; the Denon/Harman correction is present
  - the pre-registration's agency-work paragraph (Cheil Worldwide / Iris) is ON by default, verbatim from the locked
    PRE_REGISTRATION_v1_19.md section 14; --no-coi-cheil (fill(coi_cheil=False)) removes it; Samsung and Cheil appear only
    inside Declarations, Conflict of interest
Filled drafts are written to a temporary directory, never into the repository.
"""
import copy
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import fill_paper_v1_19 as F  # noqa: E402

CLAUDE_MD = Path("/Users/pablou/aias/Try system book/CLAUDE.md")
AI_USE = ("## Use of AI tools {-}\n\nDuring the preparation of this work the author used AI tools (Anthropic's Claude) "
          "to assist with study design, analysis and writing. The author reviewed and edited all content and takes "
          "full responsibility for it.")
NUM = re.compile(r"(?<![\w.])-?\d+(?:[.,]\d+)*")


def ai_use_from_claude_md():
    if not CLAUDE_MD.exists():
        return AI_USE
    t = CLAUDE_MD.read_text(encoding="utf-8")
    m = re.search(r"```\n(## Use of AI tools \{-\}\n\n.*?)\n```", t, re.DOTALL)
    return m.group(1).strip() if m else AI_USE


def section(text, heading):
    m = re.search(rf"^## {re.escape(heading)} \{{-\}}\n(.*?)(?=^#)", text, re.DOTALL | re.MULTILINE)
    return m.group(1) if m else ""


class Base(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.out = Path(cls.tmp.name) / "draft.md"
        cls.text, cls.prov = F.fill(F.VERDICTS, cls.out)
        cls.V = json.loads(F.VERDICTS.read_text())
        cls.anchor = json.loads(F.ANCHOR.read_text())
        cls.tag_commit = F.git("rev-parse", f"{F.EXPECTED_TAG}^{{commit}}").decode().strip()
        cls.tag_object = F.git("rev-parse", F.EXPECTED_TAG).decode().strip()

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()


class Refusals(Base):
    def test_record_is_sound(self):
        self.assertEqual(F.verify(self.V, F.EXPECTED_SHA, self.anchor, self.tag_commit, self.tag_object), [])

    def test_wrong_tag_refused(self):
        V = copy.deepcopy(self.V)
        V["prereg_tag"] = "v1.19-prereg-r2"
        p = F.verify(V, F.EXPECTED_SHA, self.anchor, self.tag_commit, self.tag_object)
        self.assertTrue(any("prereg_tag" in x for x in p))
        bad = Path(self.tmp.name) / "wrong_tag.json"
        bad.write_text(json.dumps(V))
        with self.assertRaises(F.Refused):
            F.fill(bad, Path(self.tmp.name) / "x.md")
        self.assertFalse((Path(self.tmp.name) / "x.md").exists())

    def test_wrong_hash_refused(self):
        p = F.verify(self.V, "0" * 64, self.anchor, self.tag_commit, self.tag_object)
        self.assertTrue(any("SHA-256" in x for x in p))
        bad = Path(self.tmp.name) / "wrong_hash.json"
        bad.write_bytes(F.VERDICTS.read_bytes() + b"\n")   # same content, one byte more: a different file
        with self.assertRaises(F.Refused):
            F.fill(bad, Path(self.tmp.name) / "y.md")

    def test_tag_or_anchor_mismatch_refused(self):
        self.assertTrue(F.verify(self.V, F.EXPECTED_SHA, self.anchor, "0" * 40, self.tag_object))
        self.assertTrue(F.verify(self.V, F.EXPECTED_SHA, self.anchor, self.tag_commit, "0" * 40))
        a = dict(self.anchor, commit="1" * 40)
        self.assertTrue(F.verify(self.V, F.EXPECTED_SHA, a, self.tag_commit, self.tag_object))


class Numbers(Base):
    def test_no_template_syntax_left(self):
        self.assertNotIn("{{", self.text)
        self.assertNotIn("{%", self.text)

    def test_every_number_is_fixed_text_or_recorded(self):
        tpl = F.TEMPLATE.read_text(encoding="utf-8")
        fixed = re.sub(r"\{\{\w+\}\}", " ", re.sub(r"\{% (?:if \w+|endif) %\}", "", tpl))
        allowed = set(NUM.findall(fixed))
        for v in self.prov["values"].values():
            allowed |= set(NUM.findall(str(v["text"])))
        stray = sorted(set(NUM.findall(self.text)) - allowed)
        self.assertEqual(stray, [], f"numbers in the draft that are neither fixed text nor recorded: {stray}")

    def test_recorded_values_resolve(self):
        n = 0
        for k, v in self.prov["values"].items():
            if v.get("source") == "outputs/v119_verdicts.json" and "*" not in v["path"]:
                self.assertEqual(F.jget(self.V, v["path"]), v["raw"], k)
                n += 1
        self.assertGreater(n, 60)

    def test_all_fixed_sentences_hold(self):
        self.assertTrue(all(a["holds"] for a in self.prov["asserts"]))

    def test_every_verdict_reported(self):
        for h, word in self.V["verdict_summary"].items():
            self.assertIn(word.split(" (")[0], self.text, h)
        for h in ("H32_SetSampling", "H32_CueType", "H34_Floor_Signature", "H34_Floor_BeyondPresence",
                  "H34_Defunct_Occupancy", "H35_IL_Coverage", "H35_IL_Robust", "H35_IL_CueType",
                  "H36_Profile_Replication", "H36_Structure"):
            self.assertIn(h, self.text)


class Declarations(Base):
    def test_samsung_only_in_coi(self):
        coi = section(self.text, "Conflict of interest")
        self.assertIn("Samsung Electronics America", coi)
        rest = self.text.replace(coi, "")
        self.assertNotIn("Samsung", rest)
        self.assertNotIn("Cheil", rest)

    def test_ai_use_verbatim_after_ethics(self):
        stmt = ai_use_from_claude_md()
        self.assertIn(stmt, self.text)
        self.assertLess(self.text.index("## Ethics {-}"), self.text.index(stmt))

    def test_denon_harman_correction(self):
        coi = section(self.text, "Conflict of interest")
        self.assertIn("Correction (November 10, 2026): Denon, which replaced AKG in the v0.19 registry, has itself "
                      "been owned by Harman International", coi)
        self.assertIn("sensitivity S-COI", coi)
        self.assertNotIn("S10", coi)

    def test_cheil_on_by_default_verbatim_and_switch_removes_it(self):
        pre = F.PREREG.read_text(encoding="utf-8")
        para = re.findall(r"Cheil Worldwide, a marketing company.*?\(sensitivity S-COI\)\.", pre, re.DOTALL)
        self.assertEqual(len(para), 1)
        coi = section(self.text, "Conflict of interest")
        self.assertIn(para[0], coi)
        self.assertNotIn("Cheil", self.text.replace(coi, ""))
        self.assertTrue(self.prov["coi_cheil"])
        out = Path(self.tmp.name) / "no_cheil.md"
        text, prov = F.fill(F.VERDICTS, out, coi_cheil=False)
        self.assertNotIn("Cheil", text)
        coi2 = section(text, "Conflict of interest")
        self.assertIn("Every test is also reported without Denon (sensitivity S-COI).", coi2)
        self.assertNotIn("Samsung", text.replace(coi2, ""))
        self.assertFalse(prov["coi_cheil"])

    def test_v19_and_v112_cited_without_ssrn(self):
        refs = self.text[self.text.index("# References {-}"):]
        self.assertNotIn("7685126", self.text)
        line = [l for l in refs.splitlines() if "Methodology v1.12)" in l][0]
        self.assertNotIn("SSRN", line)
        self.assertIn("thirdsystem.ai/studies/v1-9/", refs)
        self.assertIn("<https://thirdsystem.ai/studies/v1-12/>", line)


if __name__ == "__main__":
    unittest.main(verbosity=2)
