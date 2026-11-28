"""Tests for panel_check_v0_46.py (Section 3.3 automated panel check). Synthetic pages only; no network, no model.
Run: python3 -m unittest discover -s osf/v46/scripts/tests -p 'test_panel_check_v0_46.py'"""
import json
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import panel_check_v0_46 as PC  # noqa: E402

PAGES = {
    ("anthropic", "overview"): "<h2>Latest models</h2><p>Use Claude Fable 5.2 for demanding reasoning.</p>"
                               "<table><tr><td>Claude API ID</td><td>claude-fable-5-2</td><td>claude-opus-5-5</td></tr></table>",
    ("anthropic", "changelog"): "<p>November 9, 2026 We've launched Claude Fable 5.2 ( claude-fable-5-2 ).</p>",
    ("anthropic", "pricing"): "<p>Claude Fable 5.2 For demanding reasoning $8 / MTok $40 / MTok</p>"
                              "<p>Batch processing 50 percent. Claude Fable 5.2 For demanding reasoning $4 / MTok $20 / MTok</p>",
    ("anthropic", "model"): "<h1>Claude Fable 5.2</h1><code>claude-fable-5-2</code><p>Claude Mythos 5.2 offers the same "
                            "capabilities only to organizations verified through a programme.</p>",
    ("openai", "overview"): "<p>If unsure, use GPT-6.2 Astra , our flagship model for complex reasoning.</p>"
                            "<h2>Flagship models</h2><div>GPT-6.2 Astra Our most capable model. Model ID gpt-6.2-astra</div>",
    ("openai", "changelog"): "<p>Nov 17 Feature gpt-6.2-astra v1/responses Use GPT-6.2 Astra.</p>",
    ("openai", "pricing"): "<p>Flagship models Standard Model Input Output gpt-6.2-astra $8.00 $40.00 gpt-6-astra $10.00 $50.00"
                           " Batch gpt-6.2-astra $4.00 $20.00</p><p>Flex (beta)* only on some models.</p>",
    ("openai", "model"): "<h1>GPT-6.2 Astra</h1><p>gpt-6.2-astra</p><p>Cloud providers Model IDs across cloud providers. "
                         "Provider Model ID Google Cloud Private preview gpt-6.2-astra</p><p>Rate limits apply.</p>",
    ("google", "overview"): '{% card description="Our strongest reasoning model, built for X." title="Gemini 4 Carbon" '
                            'variant="model-card" %} * *Model code* **gemini-4-carbon** {% /card %}'
                            '{% card description="Our efficient model." title="Gemini 4 Argon" %} * *Model code* **gemini-4-argon**',
    ("google", "changelog"): "## November 10, 2026 {% id=\"11-10-2026\" %} * **Gemini 4 Carbon (`gemini-4-carbon`) "
                             "generally available (GA)**: Released Gemini 4 Carbon.",
    ("google", "pricing"): '## Gemini 4 Carbon {% id="gemini-4-carbon" %} Our most capable reasoning model, built for X. '
                           "{% callout %} Gemini 4 Carbon is not available on the Free tier. Every token is billed. {% /callout %}"
                           " * Input price * Not available * $2.00 through November 30, 2026. $4.00 starting December 1, 2026. ---"
                           " * Output price (including thinking tokens) * Not available * $10.00 through November 30, 2026. "
                           "$20.00 starting December 1, 2026. --- * Context",
    ("google", "model"): "{% badge label=Supported (Preview) %} Tool retrieval. Stable: `gemini-4-carbon` gemini-4-carbon",
    ("google", "deprecations"): "* `gemini-4-carbon` * November 10, 2026 * No shutdown date announced * ---",
}


def getter(pages):
    def get(key, url):
        prov = "anthropic" if "claude.com" in url else ("openai" if "openai.com" in url else "google")
        b = pages.get((prov, key), "").encode()
        return {"url": url, "utc": "2026-11-28T10:00:00+00:00", "status": 200 if b else 404, "served_url": url,
                "bytes": len(b), "sha256": "x", "_raw": b}
    return get


class TestPanelCheck(unittest.TestCase):
    def test_all_three_available(self):
        rec = PC.run(get=getter(PAGES), write=False, log=lambda *a: None)
        self.assertEqual(rec["panel"], {"M1_anthropic": "claude-fable-5-2", "M2_openai": "gpt-6.2-astra",
                                        "M3_google": "gemini-4-carbon"})
        self.assertTrue(rec["all_available"], {s: e.get("why_not") for s, e in rec["models"].items()})
        self.assertEqual(rec["manual_steps"], "none")

    def test_google_ga_is_stated_and_dated(self):
        e = PC.run(get=getter(PAGES), write=False, log=lambda *a: None)["models"]["M3_google"]
        self.assertEqual(e["ga_basis"], "stated GA in the provider's changelog")
        self.assertIn("November 10, 2026", e["wording"]["T3_ga"][0])
        self.assertIn("$4.00 starting December 1, 2026", e["wording"]["T4_price"]["standard"])

    def test_restricted_sibling_does_not_disqualify(self):
        e = PC.run(get=getter(PAGES), write=False, log=lambda *a: None)["models"]["M1_anthropic"]
        self.assertTrue(e["tests"]["T5_no_qualifier"])

    def test_third_party_cloud_preview_recorded_not_tested(self):
        e = PC.run(get=getter(PAGES), write=False, log=lambda *a: None)["models"]["M2_openai"]
        self.assertTrue(e["tests"]["T5_no_qualifier"])
        self.assertIn("Private preview", json.dumps(e["wording"]["T5_third_party_listings_not_tested"]))

    def test_preview_on_candidate_fails(self):
        p = dict(PAGES)
        p[("openai", "model")] = "<h1>GPT-6.2 Astra</h1><p>gpt-6.2-astra is in preview for verified customers.</p>"
        e = PC.run(get=getter(p), write=False, log=lambda *a: None)["models"]["M2_openai"]
        self.assertFalse(e["available"])
        self.assertFalse(e["tests"]["T5_no_qualifier"])

    def test_missing_price_fails(self):
        p = dict(PAGES)
        p[("openai", "pricing")] = "<p>Flagship models gpt-6-astra $10.00 $50.00</p>"
        e = PC.run(get=getter(p), write=False, log=lambda *a: None)["models"]["M2_openai"]
        self.assertFalse(e["available"])

    def test_no_flagship_found(self):
        p = dict(PAGES)
        p[("google", "overview")] = "<p>nothing here</p>"
        rec = PC.run(get=getter(p), write=False, log=lambda *a: None)
        self.assertFalse(rec["models"]["M3_google"]["available"])
        self.assertFalse(rec["all_available"])

    def test_page_404_fails(self):
        p = dict(PAGES)
        del p[("anthropic", "changelog")]
        e = PC.run(get=getter(p), write=False, log=lambda *a: None)["models"]["M1_anthropic"]
        self.assertFalse(e["tests"]["all_pages_200"])
        self.assertFalse(e["available"])

    def test_record_shape_read_by_panel_guard(self):
        import acquire_v0_46 as A
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / "rec.json"
            PC.run(get=getter(PAGES), out=out, log=lambda *a: None)
            panel = A.panel_guard(out)
        self.assertEqual([m["model_id"] for m in panel], ["claude-fable-5-2", "gpt-6.2-astra", "gemini-4-carbon"])

    def test_names(self):
        self.assertEqual(PC.name_of("anthropic", "claude-fable-5-2"), "Claude Fable 5.2")
        self.assertEqual(PC.name_of("openai", "gpt-6.2-astra"), "GPT-6.2 Astra")
        self.assertEqual(PC.name_of("google", "gemini-4-carbon"), "Gemini 4 Carbon")


if __name__ == "__main__":
    unittest.main()
