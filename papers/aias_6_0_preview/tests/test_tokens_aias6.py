#!/usr/bin/env python3
"""
Placeholder-mapping tests for the AIAS 6.0 Preview drafts (paper, report, website study page). SYNTHETIC DATA ONLY
(the paper pipeline's fixtures); nothing is written.

Fails when: a {{NAME}} in the paper template is not computed by fill_paper_aias6.py; a {{v:KEY}} in the report
content or the site page is not in tokens_aias6.TOKEN_MAP; a {{build:KEY}} is not in BUILD_KEYS; a mapped key does
not resolve on a scenario where its flag holds; a conditional key is used outside an item that requires its flag;
any scenario leaves a token unfilled. Also checks the register rules the drafts must keep.

  PYTHONDONTWRITEBYTECODE=1 python3 papers/aias_6_0_preview/tests/test_tokens_aias6.py
"""
import importlib.util
import json
import re
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAPER = HERE.parent
ROOT = PAPER.parents[1]
FIX = HERE / "fixtures"
sys.path.insert(0, str(PAPER))
sys.path.insert(0, str(HERE))
import tokens_aias6 as T  # noqa: E402
import make_scenarios_aias6 as MS  # noqa: E402

TPL = (PAPER / "aias_6_0_preview_paper_template.md").read_text(encoding="utf-8")
FILL_SRC = (PAPER / "fill_paper_aias6.py").read_text(encoding="utf-8")
SITE_PATH = PAPER / "site" / "aias-6-0-preview.json"
SITE = json.loads(SITE_PATH.read_text(encoding="utf-8"))
SITE_COPY = Path.home() / "aias/_worktrees/site-preview-6.0-draft/content/pending/aias-6-0-preview.json"
_spec = importlib.util.spec_from_file_location("rc", ROOT / "reports" / "aias6_preview_report_content.py")
RC = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(RC)
REPORT = {k: getattr(RC, k) for k in dir(RC) if k.isupper()}
AI_USE = ("During the preparation of this work the author used AI tools (Anthropic's Claude) to assist with study "
          "design, analysis and writing. The author reviewed and edited all content and takes full responsibility "
          "for it.")
BUILD = re.compile(r"\{\{build:([^}]+)\}\}")
# build facts known only once the PDFs exist (never results): each is filled at the website hand-off
BUILD_KEYS = {"month", "paper_title", "report_file", "report_pages", "report_code", "paper_pages", "plain_found",
              "plain_short", "abstract_verbatim"}
CTX = {}


def setUpModule():
    for s in MS.SCENARIOS:
        CTX[s] = T.context(FIX / s, synthetic=True)


def walk(obj, reqs=()):
    """Yield (string, requirements in force) for every string in obj."""
    if isinstance(obj, str):
        yield obj, set(reqs)
    elif isinstance(obj, dict):
        r = tuple(reqs) + tuple(obj.get("requires", ()))
        for k, v in obj.items():
            if k != "requires" and not str(k).startswith("_"):
                yield from walk(v, r)
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            yield from walk(v, reqs)


class TestMapping(unittest.TestCase):
    def test_paper_placeholders_are_computed_by_the_fill(self):
        names = set(re.findall(r"\{\{\s*([A-Z0-9_]+)\s*\}\}", TPL))
        self.assertTrue(names)
        def computed(n):   # a literal name, or an f-string name such as f"HS_{k.upper()}"
            return f'"{n}"' in FILL_SRC or any(f'f"{n[:i]}{{' in FILL_SRC for i in range(1, len(n)))
        unmapped = sorted(n for n in names if not computed(n))
        self.assertEqual(unmapped, [], f"paper placeholders with no value in fill_paper_aias6.py: {unmapped}")

    def test_report_and_site_tokens_are_mapped(self):
        used = T.keys_in(REPORT) | T.keys_in(SITE)
        self.assertTrue(used)
        self.assertEqual(sorted(used - set(T.TOKEN_MAP)), [], "unmapped {{v:KEY}} tokens")
        built = {m for s, _ in walk(SITE) for m in BUILD.findall(s)} | {m for s, _ in walk(REPORT)
                                                                       for m in BUILD.findall(s)}
        self.assertEqual(sorted(built - BUILD_KEYS), [], "unknown {{build:KEY}} tokens")

    def test_unmapped_token_is_refused(self):
        with self.assertRaises(T.TokenError):
            T.resolve("pv.not_a_key", CTX["ranking_marginal"])
        with self.assertRaises(T.TokenError):
            T.fill_content("x {{v:pv.not_a_key}}", CTX["ranking_marginal"])

    def test_map_entries_are_well_formed(self):
        for k, spec in T.TOKEN_MAP.items():
            self.assertIn(spec[0], ("results", "gates", "inputs", "paper", "scorer"), k)
            self.assertIn(spec[2], T.FMT, k)
            if len(spec) > 3:
                self.assertIn(spec[3], T.FLAGS, k)

    def test_conditional_keys_are_used_only_under_their_flag(self):
        for doc in (REPORT, SITE):
            for s, reqs in walk(doc):
                for k in T.TOKEN.findall(s):
                    when = T.TOKEN_MAP[k][3] if len(T.TOKEN_MAP[k]) > 3 else None
                    if when:
                        self.assertIn(when, reqs, f"{k} needs requires [{when!r}] around: {s[:70]}")

    def test_every_key_resolves_where_its_flag_holds(self):
        for s, ctx in CTX.items():
            for k, spec in T.TOKEN_MAP.items():
                when = spec[3] if len(spec) > 3 else None
                if when is None or ctx["flags"][when]:
                    try:
                        T.resolve(k, ctx)
                    except Exception as e:  # noqa: BLE001
                        self.fail(f"{s}: {k} does not resolve: {e}")

    def test_report_and_site_fill_in_every_scenario(self):
        for s, ctx in CTX.items():
            for doc in (REPORT, SITE):
                out = json.dumps(T.fill_content(doc, ctx), ensure_ascii=False)
                self.assertNotIn("{{v:", out, s)
                self.assertNotIn("{%", out, s)


class TestRegisterRules(unittest.TestCase):
    def test_ai_use_verbatim_and_employer_not_named_outside_the_paper(self):
        self.assertEqual(REPORT["DISCLOSURES"]["ai_use"], AI_USE)
        for doc in (REPORT, SITE):
            text = json.dumps(doc, ensure_ascii=False)
            for word in ("Samsung", "Harman", "Cheil"):
                self.assertNotIn(word, text)
        coi = REPORT["DISCLOSURES"]["conflicts_of_interest"]
        for s in ("Denon", "September 23, 2025", "November 10, 2026", "Chevrolet", "Eucerin", "Declarations"):
            self.assertIn(s, coi)

    def test_held_studies_never_appear(self):
        for doc in (REPORT, SITE):
            text = json.dumps(doc, ensure_ascii=False).lower()
            for word in ("v0.38", "v0.39", "roaster", "aillio", "bellwether"):
                self.assertNotIn(word, text)
        self.assertFalse(SITE["held"])

    def test_chart_titles_never_repeat_finding_titles(self):
        titles = set()
        for f in REPORT["FINDINGS"]:
            titles |= {f["title"]} if "title" in f else {t["text"] for t in f["title_by_class"]}
        charts = REPORT["CHARTS"]
        for f in REPORT["FINDINGS"]:
            self.assertIn(f["chart"], charts)
        for name, c in charts.items():
            self.assertNotIn(c["title"], titles, name)
            self.assertNotIn("{{v:pv.headline", c["title"] + c["subtitle"], name)
            words = set(re.findall(r"[a-z]+", c["title"].lower())) - {"of", "the", "and", "a", "on", "by", "for",
                                                                        "each", "with", "per", "at"}
            for t in titles:
                tw = set(re.findall(r"[a-z]+", t.lower()))
                self.assertLess(len(words & tw) / max(1, len(words)), 0.6, f"{name} paraphrases '{t}'")

    def test_provisional_everywhere(self):
        for name, c in REPORT["CHARTS"].items():
            self.assertIn("provisional", c["subtitle"], name)
        for f in REPORT["FINDINGS"]:
            self.assertIn("Provisional", f["caption"])
        self.assertIn("pv.title", REPORT["DECK"])
        self.assertIn("pv.validation_line", " ".join(s for s, _ in walk(REPORT["INTRO"])))

    def test_no_typed_number_in_report_text(self):
        allowed = {"0", "100", "90", "2025", "2026", "23", "10", "2.0", "3.0", "5.0", "5.2", "6", "4", "1", "6.0"}
        for s, _ in walk({k: v for k, v in REPORT.items() if k not in ("REPORT_CODE", "TIER", "COVER")}):
            bare = T.TOKEN.sub(" ", s)
            for n in re.findall(r"(?<![\w.])\d+(?:\.\d+)?", bare):
                if re.fullmatch(r"0\d", n):      # row numbers of the scored table
                    continue
                self.assertIn(n, allowed, f"typed number {n!r} in: {bare[:90]}")

    def test_site_copy_in_the_website_branch_is_identical(self):
        if not SITE_COPY.exists():
            self.skipTest("website worktree not present")
        self.assertEqual(SITE_COPY.read_bytes(), SITE_PATH.read_bytes())


if __name__ == "__main__":
    unittest.main(verbosity=1)
