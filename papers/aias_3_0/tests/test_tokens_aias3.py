#!/usr/bin/env python3
"""
Token-map and placeholder tests for the AIAS 3.0 (Coverage) release drafts: paper template, report content and
website study page. Nothing public; builds go to a temporary folder outside the repository.

Fails when: a {{L:KEY}} or {{P:KEY}} is unmapped; a mapped placeholder is used nowhere or names an unknown input;
a locked key does not resolve at its commit; a final build leaves any token or template syntax; a final build
does not refuse a missing value, an unmapped token or a synthetic values file in real mode; the register rules
break (AI-use verbatim; employer only in the paper's Declarations COI, conformed to v1.12's locked text; held
studies absent; chart titles never repeat or paraphrase finding titles; one chart per finding; no typed number);
a published figure the paper reuses differs from its source commit; the website copy differs.

  PYTHONDONTWRITEBYTECODE=1 python3 papers/aias_3_0/tests/test_tokens_aias3.py
"""
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAPER = HERE.parent
ROOT = PAPER.parents[1]
sys.path.insert(0, str(PAPER))
import sources_aias3 as S  # noqa: E402
import tokens_aias3 as T  # noqa: E402
import build_aias3 as B  # noqa: E402

TPL = (PAPER / "aias_3_0_release_paper_template.md").read_text(encoding="utf-8")
SITE_PATH = PAPER / "site" / "aias-3-0.json"
SITE = json.loads(SITE_PATH.read_text(encoding="utf-8"))
SITE_COPY = Path.home() / "aias/_worktrees/site-aias-3.0-draft/content/pending/aias-3-0.json"
_spec = importlib.util.spec_from_file_location("rc3", ROOT / "reports" / "aias3_release_report_content.py")
RC = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(RC)
REPORT = {k: getattr(RC, k) for k in dir(RC) if k.isupper()}
AI_USE = ("During the preparation of this work the author used AI tools (Anthropic's Claude) to assist with study "
          "design, analysis and writing. The author reviewed and edited all content and takes full responsibility "
          "for it.")
HELD = ("v0.38", "v0.39", "roaster", "aillio", "bellwether")
EMPLOYER = ("Samsung", "Harman", "Cheil")
# published figures the paper reuses, with the commit they were published at (never changed)
REUSED_FIGS = {"reports/figs/v112/chart_02_legs_bands.pdf": S.C["v112_paper"],
               "reports/figs/v119/chart_01_split_reliability.pdf": S.C["v119_paper"]}


def synthetic_values(drop=None, flags=None):
    vals = {k: f"SYNTHETIC-{k}" for k in T.PENDING if k != drop}
    return {"synthetic": True, "values": vals, "flags": dict({f: True for f in T.FLAGS}, **(flags or {}))}


def walk(obj, reqs=()):
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


def body_sections(text):
    """Abstract through Future research (the YAML header, title page, Declarations and References excluded)."""
    a = text.index("# Abstract")
    z = text.index("# Declarations")
    return text[a:z]


class TestMapping(unittest.TestCase):
    def test_every_token_is_mapped(self):
        used = T.keys_in(TPL) | T.keys_in(REPORT) | T.keys_in(SITE)
        self.assertTrue(used)
        unmapped_p = sorted(k for kind, k in used if kind == "P" and k not in T.PENDING)
        unmapped_l = sorted(k for kind, k in used if kind == "L" and k not in S.LOCKED)
        self.assertEqual(unmapped_p, [], "unmapped {{P:KEY}}")
        self.assertEqual(unmapped_l, [], "unmapped {{L:KEY}}")

    def test_every_mapped_placeholder_is_used_and_names_a_known_input(self):
        used = {k for kind, k in T.keys_in(TPL) | T.keys_in(REPORT) | T.keys_in(SITE) if kind == "P"}
        self.assertEqual(sorted(set(T.PENDING) - used), [], "placeholders mapped but used nowhere")
        for k, (inp, where, what) in T.PENDING.items():
            self.assertIn(inp, T.INPUTS, k)
            self.assertTrue(where and what, k)
        for name, i in T.INPUTS.items():
            for f in ("what", "file", "step", "prereg", "pablo", "earliest"):
                self.assertTrue(i.get(f), f"{name}.{f}")

    def test_every_locked_key_resolves_at_its_commit(self):
        for k in S.LOCKED:
            p = S.provenance(k)
            self.assertTrue(p["value"] not in ("", "None"), k)
            self.assertRegex(p["commit"], r"^[0-9a-f]{40}$", k)

    def test_unmapped_tokens_are_refused(self):
        with self.assertRaises(T.TokenError):
            B.fill(TPL + "\n{{P:NOT_A_KEY}}\n", "draft")
        with self.assertRaises(S.SourceError):
            B.fill(TPL + "\n{{L:not.a.key}}\n", "draft")
        with self.assertRaises(T.TokenError):
            T.fill_content({"x": "{{P:NOT_A_KEY}}"}, "final", synthetic_values())

    def test_requires_flags_are_known(self):
        for doc in (REPORT, SITE):
            for _, reqs in walk(doc):
                for r in reqs:
                    self.assertIn(r.lstrip("!"), T.FLAGS)


class TestBuilds(unittest.TestCase):
    def test_draft_fills_every_locked_token_and_shows_every_placeholder(self):
        text, used = B.fill(TPL, "draft")
        self.assertNotIn("{{L:", text)
        self.assertNotIn("{{P:", text)
        for k in used["P"]:
            self.assertIn("P:" + k.replace("_", r"\_"), text.replace("[P:", "P:"))

    def test_final_build_leaves_no_token(self):
        v = synthetic_values()
        text, _ = B.fill(TPL, "final", v)
        self.assertIsNone(T.ANY_TEMPLATE.search(text))
        for doc in (REPORT, SITE):
            out = json.dumps(T.fill_content(doc, "final", v), ensure_ascii=False)
            self.assertNotIn("{{", out)
            self.assertNotIn("{%", out)

    def test_final_build_refuses_each_missing_value(self):
        for k in T.PENDING:
            v = synthetic_values(drop=k)
            with self.assertRaises(T.TokenError, msg=k):
                B.fill(TPL, "final", v)
                for doc in (REPORT, SITE):
                    T.fill_content(doc, "final", v)

    def test_final_build_refuses_template_syntax_left(self):
        with self.assertRaises(T.TokenError):
            B.fill(TPL + "\n{{ stray }}\n", "final", synthetic_values())

    def test_cli_refuses_synthetic_values_in_real_mode_and_builds_outside_the_repo(self):
        with tempfile.TemporaryDirectory() as d:
            vf = Path(d) / "values.json"
            vf.write_text(json.dumps(synthetic_values()), encoding="utf-8")
            with self.assertRaises(SystemExit):
                B.main(["--mode", "final", "--values", str(vf), "--out", str(Path(d) / "o")])
            with self.assertRaises(SystemExit):
                B.main(["--mode", "final", "--values", str(vf), "--synthetic", "--out", str(PAPER / "tmp_out")])
            self.assertEqual(B.main(["--mode", "final", "--values", str(vf), "--synthetic", "--out",
                                     str(Path(d) / "o")]), 0)
            out = (Path(d) / "o" / "aias_3_0_release_paper.md").read_text(encoding="utf-8")
            self.assertNotIn("{{", out)
            with self.assertRaises(SystemExit):
                B.main(["--mode", "draft", "--out", str(PAPER / "tmp_out")])
        self.assertFalse((PAPER / "tmp_out").exists())

    def test_flags_drop_items_in_final_mode(self):
        v = synthetic_values(flags={"PRED_RESULT": False})
        out = T.fill_content(REPORT["FINDINGS"], "final", v)
        self.assertEqual(len(out), len(REPORT["FINDINGS"]) - 1)


class TestRegisterRules(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.paper, _ = B.fill(TPL, "final", synthetic_values())

    def test_ai_use_verbatim(self):
        self.assertIn(AI_USE, self.paper)
        self.assertEqual(REPORT["DISCLOSURES"]["ai_use"], AI_USE)

    def test_employer_only_in_the_papers_declarations_coi(self):
        coi_start = self.paper.index("## Conflict of interest")
        coi_end = self.paper.index("## Funding")
        outside = self.paper[:coi_start] + self.paper[coi_end:]
        for w in EMPLOYER:
            self.assertNotIn(w, outside)
        for doc in (REPORT, SITE):
            text = json.dumps(doc, ensure_ascii=False)
            for w in EMPLOYER:
                self.assertNotIn(w, text)

    def test_coi_is_v112s_locked_text(self):
        src = S.blob(S.C["v112_paper"], S.P112)
        locked = re.search(r"## Conflict of interest \{-\}\n\n(.+?)\n\n## Funding", src, re.S).group(1)
        self.assertIn(locked, self.paper)
        for s in ("Denon", "September 23, 2025", "tier-2/3", "Samsung SDI", "Samsung Display", "Cheil Worldwide",
                  "March 2017" if "March 2017" in locked else "Harman International"):
            self.assertIn(s, self.paper)
        rcoi = REPORT["DISCLOSURES"]["conflicts_of_interest"]
        for s in ("Denon", "September 23, 2025", "November 10, 2026", "Chevrolet", "Eucerin", "Declarations"):
            self.assertIn(s, rcoi)

    def test_held_studies_never_appear(self):
        for text in (self.paper.lower(), json.dumps(REPORT, ensure_ascii=False).lower(),
                     json.dumps(SITE, ensure_ascii=False).lower()):
            for w in HELD:
                self.assertNotIn(w, text)
        self.assertFalse(SITE["held"])

    def test_one_chart_per_finding_and_titles_never_repeat(self):
        charts = REPORT["CHARTS"]
        seen = set()
        for f in REPORT["FINDINGS"]:
            self.assertIn(f["chart"], charts)
            self.assertNotIn(f["chart"], seen)
            seen.add(f["chart"])
        stop = {"of", "the", "and", "a", "on", "by", "for", "each", "with", "per", "at", "in", "to", "every"}
        for f in REPORT["FINDINGS"]:
            ft = f["title"]
            for name, c in charts.items():
                self.assertNotEqual(c["title"], ft)
                cw = set(re.findall(r"[a-z]+", c["title"].lower())) - stop
                fw = set(re.findall(r"[a-z]+", ft.lower())) - stop
                self.assertLess(len(cw & fw) / max(1, len(cw)), 0.6, f"{name} paraphrases '{ft}'")

    def test_no_typed_number_in_report_or_site(self):
        allowed = {"0", "100", "50", "1.0", "2.0", "3.0", "4.0", "5.0", "5.2", "5.5", "6", "4", "2025", "2026",
                   "10", "23", "01", "02", "03", "04", "05", "06", "1.12", "1.19", "0.43"}
        for doc in ({k: v for k, v in REPORT.items() if k not in ("TIER",)}, SITE):
            for s, _ in walk(doc):
                bare = T.TOKEN.sub(" ", s)
                bare = re.sub(r"\b(?:fig_|report_fig_)\d+\w*|v\d+\.\d+|H\d+(?:-H\d+)?|chart_\d+|Stage \d"
                              r"|aias[-_]\d[-_]\d\w*|v1_\d+|osf/\S+|Section \d+"
                              r"|\b(?:Jan|Feb|Mar|Sep|Nov|Dec)\w* \d{1,2}(?:, 20\d\d)?", " ", bare)
                for n in re.findall(r"(?<![\w.])\d+(?:\.\d+)?", bare):
                    self.assertIn(n, allowed, f"typed number {n!r} in: {bare[:100]}")

    def test_no_typed_number_in_the_papers_results_text(self):
        body = T.TOKEN.sub(" ", body_sections(TPL))
        body = re.sub(r"(?m)^#.*$", " ", body)                     # headings (section numbers)
        strip = [r"!\[.*?\]\(.*?\)\{.*?\}",                       # figure lines (paths, widths)
                 r"\bTable \d+\b", r"\bStage \d\b",
                 r"scores 50\b",                                   # Cov*'s scale definition (v1.12 §2.4)
                 r"\b\d{1,2} (?:January|February|March|November|December) 20\d\d\b",   # dated decisions
                 r"\b(?:SSRN|Report No\.|Working Paper) [\d-]+", r"v\d+\.\d+(?:--v\d+\.\d+)?", r"AIAS \d\.\d",
                 r"\b(?:Methodology|Section|Sections|Claim) [\d.]+(?: and \d+)?", r"§\d+(?:\.\d+)?", r"#\d+\w?",
                 r"\$t_\d\$|t_\d|\(t_\d\)|\$P_\{N3\}\$|\$C\^\*_\{N3\}\$|N3|C3|A4", r"\b(?:19|20)\d\d\b",
                 r"\b\d\.\d (?:Release|release)", r"(?:Fable|Opus|Gemini) \d(?:\.\d)?", r"GPT-\d",
                 r"aias-\d\.\d-draft",
                 r"\b(?:4\.0|5\.0|6\.0)\b", r"26-132", r"\bth\b"]
        for p in strip:
            body = re.sub(p, " ", body)
        left = re.findall(r"(?<![\w.])\d+(?:\.\d+)?", body)
        self.assertEqual(left, [], f"typed numbers in the paper's body: {left}")

    def test_reused_published_figures_are_unchanged(self):
        for path, commit in REUSED_FIGS.items():
            here = subprocess.run(["git", "-C", str(ROOT), "hash-object", path], capture_output=True, text=True,
                                  check=True).stdout.strip()
            src = subprocess.run(["git", "-C", str(ROOT), "rev-parse", f"{commit}:{path}"], capture_output=True,
                                 text=True, check=True).stdout.strip()
            self.assertEqual(here, src, path)
            self.assertIn(path, TPL)

    def test_site_copy_in_the_website_branch_is_identical(self):
        if not SITE_COPY.exists():
            self.skipTest("website worktree not present")
        self.assertEqual(SITE_COPY.read_bytes(), SITE_PATH.read_bytes())


if __name__ == "__main__":
    unittest.main(verbosity=1)
