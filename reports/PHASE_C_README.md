# Phase C — v0.6 Cross-Category Findings Pipeline

## TL;DR — this runs on your Mac in terminal

```bash
cd /Users/pablou/aias/reports
python3 build_report.py
open output/v06_cross_category.pdf
```

That's the deliverable. The script reads your fonts, your Phase B charts, and your brand JSON, then writes the report.

The sample PDF I include in this delivery is **not** your report. It's a test render I produced in a Linux container that has no Akkurat Pro and no Phase B charts. The fonts in my sample are Inter (the documented fallback), and the charts in my sample are `[STUB]`-labeled placeholders. Both will be replaced when you run the script on your Mac. **You will only ever see Akkurat and your charts after running the script locally.**

## Files in this delivery

| File | Where it goes on your Mac | Role |
|---|---|---|
| `build_report.py`   | `/Users/pablou/aias/reports/build_report.py`   | Two-pass typesetting pipeline. |
| `v06_content.py`    | `/Users/pablou/aias/reports/v06_content.py`    | v0.6 cross-category body copy. |
| `tsboilerplate.py`  | `/Users/pablou/aias/reports/tsboilerplate.py`  | Reusable framework boilerplate (Short / Medium / Long). |
| `v06_cross_category.pdf` | sample only — do not use as final | 20-page test render with Inter + stub charts. |

## What the terminal output tells you

When you run `python3 build_report.py`, the first thing it prints is a font diagnostic:

```
[fonts] scanned NN font files across 10 dirs:
  [ok] /Users/pablou/Library/Fonts          ← if [ok], your user font dir was scanned
  [ok] /Library/Fonts
  [ok] /System/Library/Fonts
  ...
[fonts] N Akkurat file(s) found:
  - /Users/pablou/Library/Fonts/AkkuratPro-Bold.otf
  - /Users/pablou/Library/Fonts/AkkuratPro-Regular.otf
  ...
  [register] Akkurat-Light            <- AkkuratPro-Light.otf
  [register] Akkurat-Regular          <- AkkuratPro-Regular.otf
  [register] Akkurat-Bold             <- AkkuratPro-Bold.otf
  ...
[fonts] using Akkurat Pro (brand-compliant)
```

If you see `[fonts] using Akkurat Pro (brand-compliant)` — your report is in Akkurat. If you see `[fonts] using Inter (documented fallback)` — Akkurat couldn't be loaded; look at the file list above to see what filenames the scan found. The scan is recursive and case-insensitive; any file with "akkurat" in its name in any standard macOS font directory will be picked up.

Next is the chart pre-flight:

```
[build_report] chart pre-flight (looking in /Users/pablou/aias/reports/output)
  [FOUND  ] inline_p1_variance                 -> chart_p1_3col.pdf
  [FOUND  ] hero_p2_scatter                    -> chart_p2_6col.pdf
  [FOUND  ] inline_p3_awareness_gap            -> chart_p3_3col.pdf
  [FOUND  ] hero_p4_country                    -> chart_p4_spread.pdf
  [FOUND  ] inline_p5_default_reinforcement    -> chart_p5_3col.pdf
  [FOUND  ] inline_p6_phantom                  -> chart_p6_3col.pdf
  [MISSING] hero_leaderboards                  -> chart_leaderboards_6col.pdf
  [MISSING] hero_aggregate                     -> chart_aggregate_6col.pdf
```

`[FOUND]` means the chart will be embedded. `[MISSING]` means the script skips that page entirely (no blank stub).

## The eight chart slots

The report expects these chart filenames in `/Users/pablou/aias/reports/output/`:

| Slot | Filename | Size |
|---|---|---|
| Pattern 1 inline      | `chart_p1_3col.pdf`           | 3.68" × 2.85" |
| Pattern 2 hero        | `chart_p2_6col.pdf`           | 7.5" × 5.0" |
| Pattern 3 inline      | `chart_p3_3col.pdf`           | 3.68" × 2.85" |
| Pattern 4 hero spread | `chart_p4_spread.pdf`         | 7.5" × 4.5" |
| Pattern 5 inline      | `chart_p5_3col.pdf`           | 3.68" × 2.85" |
| Pattern 6 inline      | `chart_p6_3col.pdf`           | 3.68" × 2.85" |
| Leaderboards hero     | `chart_leaderboards_6col.pdf` | 7.5" × 5.0" |
| Aggregate matrix      | `chart_aggregate_6col.pdf`    | 7.5" × 6.5" |

The bottom two are slots I added per your "best guess" Q3 default. If you don't have them rendered yet, the pipeline drops those pages from the report. Page count goes from 20 → ~17–18.

## Optional flags

```bash
python3 build_report.py --debug-layout
python3 build_report.py --chart-dir /path/to/alternate/charts
python3 build_report.py --output /tmp/report.pdf
```

`--debug-layout` outlines every chart slot in dashed indigo so you can verify geometry.

## Decisions taken on "best guess"

1. **Pattern 2** — Hero only, small multiples dropped.
2. **Pattern 3** — 3-col inline (matches original spec; Q2 default to graduate to 4-col was wrong because a 4-col chart at column 1 overlaps the right body column in a 3+3 layout).
3. **Cross-category leaderboards** — 6-col hero, placed right after the executive summary as the data-anchor before "What we measured."
4. **Aggregate matrix** — 6-col tall hero, placed just before the closing page.
5. **Cover** — All template `is_image_placeholder` rectangles left as whitespace. No indigo rule under the lockup.
6. **Body header** — Wordmark left, page meta right, no rule.
7. **Closing page** — Lead block is the System Overview Medium (from `tsboilerplate.py`), then byline → methodology disclaimer → citation → datasets → contact.

## Brand color flag

Handoff doc says primary is `#25408F` Third System Blue. Brand JSON v1.4 says primary is `#37237B` Indigo and its own `version_history` shows the swap at v1.1. I followed the JSON as the locked source of truth. Wordmark, headlines, accent rules, cover subtitle, standfirst, and pattern titles are all `#37237B`. To swap back, change the primary in the brand JSON and the pipeline picks it up.

## Locked rules followed

- ✅ No `is_image_placeholder` rectangles get filled — all whitespace.
- ✅ Template `Color/C=0 M=100 Y=90 K=0` red overridden to brand primary.
- ✅ Naming hierarchy locked: "Third System" (two words), "AI Presence Index", "AI Availability Score (AIAS)".
- ✅ Samsung omitted from byline.
- ✅ Public-report footer printed verbatim on every body page.
- ✅ Methodology disclaimer printed verbatim on closing page.
- ✅ Citation rendered in locked format.
- ✅ Charts embedded at native figsize, no rescaling.
- ✅ Source content from `v06_source_text.md`, with PDF-extraction artifacts cleaned.

## tsboilerplate.py — reusable framework copy

Drop-in copy bank for any Third System report. Each topic has Short / Medium / Long versions. Imports as:

```python
import tsboilerplate as bp
bp.SYSTEM_OVERVIEW["medium"]    # one paragraph, fits a closing page
bp.PRESENCE_INDEX["short"]      # a sentence
bp.COMPONENTS["presence"]["long"]   # one component description
```

Topics: `SYSTEM_OVERVIEW`, `AIAS_CORE`, `PRESENCE_INDEX`, `SHARE_OF_MODEL`, `COMPONENTS` (with `intro`, `presence`, `som`, `ranking`, `consistency`, `coverage`, `grounding`), `RESPONSE_MODES`, `REPORT_TYPES`, `VERSIONING`, `CORE_STATEMENT`. The closing page in this report uses `SYSTEM_OVERVIEW["medium"]` as its lead block.

Edit `tsboilerplate.py` to update boilerplate everywhere it's used. If you ever want a different version of the closing block on this specific report, change the one line in `build_closing_story()`.

## Typography & fallback

Search runs over: `~/Library/Fonts/`, `/Library/Fonts/`, `/System/Library/Fonts/`, `/System/Library/Fonts/Supplemental/`, `~/.fonts/`, `~/.local/share/fonts/`, `/usr/share/fonts/`, `/usr/local/share/fonts/`. All directories scanned recursively. Filename match is case-insensitive substring.

Akkurat slots resolved by these patterns:

| Slot | Matches filename containing |
|---|---|
| Akkurat-Light      | `akkurat` + `light` |
| Akkurat-Regular    | `akkurat` + `regular` (or `akkuratpro.` / `akkurat pro.`) |
| Akkurat-Bold       | `akkurat` + `bold` (and not `italic`) |
| Akkurat-Italic     | `akkurat` + `italic` (and not `bold`) |
| Akkurat-BoldItalic | `akkurat` + `bolditalic` |

Same patterns for `inter` if Akkurat isn't found. Helvetica is the last-resort fallback with a hard warning.

`pdfmetrics.registerFontFamily()` is called for both base weights (Regular and Light) so inline `<b>` and `<i>` tags in the source text correctly switch fonts.

## Page-flow notes (current 20-page render)

- Page 1: cover.
- Pages 2–3: standfirst + executive summary (six findings).
- Page 4: cross-category leaderboards hero spread.
- Page 5: What we measured + Three modes of AI response (both fit; section transition mid-page).
- Pages 6–17: six pattern sections, with hero spreads on pages 9 (Pattern 2 scatter) and 13 (Pattern 4 country two-panel).
- Pages 18–19: Limitations + What's next.
- Page 19: aggregate matrix hero.
- Page 20: closing (About the Third System + byline + methodology + citation + datasets).

## What's likely to need your eye on first run

- **Akkurat metrics vs Inter metrics**: my sample render uses Inter widths. Akkurat Pro is slightly tighter, so on your Mac the page count may drop from 20 to 18–19, and a few line breaks will land differently.
- **Real chart aspect ratios**: pipeline embeds charts at the locked figsize. If your Phase B render of any chart deviates by more than 2% from its locked figsize, you'll get a warning; otherwise no warning means exact match.
- **Chart visual integration**: pipeline preserves vector quality but does not touch chart styling. If a chart's internal palette or font drifts from brand spec, that's a Phase B concern, not Phase C.
