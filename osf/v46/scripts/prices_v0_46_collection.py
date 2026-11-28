#!/usr/bin/env python3
"""
prices_v0_46_collection.py -- AIAS v0.46 (#76): price overlay for the collection guard (DEVIATIONS Entry 2).

Section 3.9 (locked): the guard is v0.45's budget_v0_45.Ledger "with the prices in force on each request's date";
"Prices are re-read at collection". v0.45's locked budget_v0_45.py has no rows for the two models Section 3.3 gives
on 2026-11-27/28 (gpt-6.2-astra, gemini-4-carbon), so acquire_v0_46.panel_guard refuses them. This module, imported
by acquire_v0_46.py right after budget_v0_45 and before any Ledger is built, ADDS rows to budget_v0_45's tables in
memory; it changes no existing row and no function, and budget_v0_45.py itself is not edited.

Read on the vendors' own pricing pages on Sat 2026-11-28, 10:05-10:16 UTC (4:05-4:16 am CST), by HTTPS GETs from
the collection computer; the panel check's run of 10:15:51-10:15:55 UTC records the same pages with their SHA-256 and
the price wording in osf/v46/data/v46_panel_verification.json:
  OpenAI  https://developers.openai.com/api/docs/pricing  -- "Flagship models", short context:
          Standard gpt-6.2-astra $8.00 / $40.00 per 1M input / output tokens; Batch $4.00 / $20.00.
          Called synchronously (Section 3.7), so Standard applies. Reasoning tokens are billed as output
          (https://developers.openai.com/api/docs/guides/reasoning, as budget_v0_45 records for gpt-6-astra).
  Google  https://ai.google.dev/gemini-api/docs/pricing (served as https://aistudio.google.com/docs/pricing) --
          "Gemini 4 Carbon", Standard, Paid Tier: input "$2.00 through November 30, 2026. $4.00 starting December 1,
          2026."; "Output price (including thinking tokens)" "$10.00 through November 30, 2026. $20.00 starting
          December 1, 2026."; "Gemini 4 Carbon is not available on the Free tier." Entered as a base row plus a dated
          PRICE_CHANGES row, as budget_v0_45 does for gemini-4-argon.
  Unchanged and re-read the same morning (already in budget_v0_45): claude-fable-5-2 $8 / $40, Batch $4 / $20
  (https://platform.claude.com/docs/en/about-claude/pricing); claude-sonnet-5-5 (judge) $2 / $10, Batch $1 / $5.
Billing of Google thinking: budget_v0_45.part_cost adds thinking_tokens to output for provider "google"; the
worst case reserves output at the 16,384 cap (max_output_tokens), within which Gemini counts thinking (see
DEVIATIONS Entry 2's check).
"""
import budget_v0_45 as BG

READ_UTC = "2026-11-28T10:05:00+00:00/2026-11-28T10:16:00+00:00"
SOURCES = {
    "openai_pricing": "https://developers.openai.com/api/docs/pricing",
    "google_gemini_api_pricing": "https://ai.google.dev/gemini-api/docs/pricing",
    "anthropic_pricing": "https://platform.claude.com/docs/en/about-claude/pricing",
}
PROVIDER_ADD = {"gpt-6.2-astra": "openai", "gemini-4-carbon": "google"}
TOKEN_PRICES_ADD = {
    "gpt-6.2-astra": {"standard": (8.0, 40.0), "batch": (4.0, 20.0)},
    "gemini-4-carbon": {"standard": (2.0, 10.0)},
}
PRICE_CHANGES_ADD = [("gemini-4-carbon", "2026-12-01", {"standard": (4.0, 20.0)})]


def apply(bg=BG):
    """Add the rows (idempotent). Refuses to overwrite a row budget_v0_45 already has with a different value."""
    for m, p in PROVIDER_ADD.items():
        if bg.PROVIDER.get(m, p) != p:
            raise ValueError(f"budget_v0_45 already maps {m} to {bg.PROVIDER[m]}")
        bg.PROVIDER[m] = p
    for m, t in TOKEN_PRICES_ADD.items():
        if m in bg.TOKEN_PRICES and bg.TOKEN_PRICES[m] != t:
            raise ValueError(f"budget_v0_45 already prices {m} as {bg.TOKEN_PRICES[m]}")
        bg.TOKEN_PRICES[m] = dict(t)
    for row in PRICE_CHANGES_ADD:
        if row not in bg.PRICE_CHANGES:
            bg.PRICE_CHANGES.append(row)
    return bg


apply()
