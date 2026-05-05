# Third System Reports — System Notes

Operating knowledge for the report-generation pipeline. Brand-spec-derived
constants live in `brand/third_system_brand.json`. **This file captures
the lessons not in the JSON** — empirical defaults, gotchas, debug
recipes, and design decisions discovered during chart development.

When in doubt: brand JSON wins on values, this file wins on patterns.

---

## Typography

### Font verification (one-line diagnostic)
When typography looks "off" or generic, run:

```python
from matplotlib.font_manager import findfont, FontProperties
print(findfont(FontProperties(family="Akkurat Pro")))
```

If the resolved path contains `Akkurat` → the font IS installed. But this
test only confirms the font can be found by **explicit family request**.
It does NOT confirm the font is being used as the rcParams default.

### CRITICAL: Akkurat Pro requires the sans-serif registration pattern
Setting `mpl.rcParams['font.family'] = 'Akkurat Pro'` looks like it should
work but **does not**. matplotlib treats `font.family` as a *generic
family* lookup (sans-serif, serif, monospace, etc.); a face name set
directly is silently ignored and falls back.

The working pattern (now in chart_style.py):
```python
mpl.rcParams['font.family'] = 'sans-serif'
mpl.rcParams['font.sans-serif'] = ['Akkurat Pro', 'Inter', 'DejaVu Sans']
```

To verify the rcParams default is actually using Akkurat:
```python
from matplotlib.font_manager import findfont, FontProperties
print(findfont(FontProperties()))  # NO family arg — uses rcParams default
```
If the path contains `Akkurat` → the default is correctly using it.
If the path is DejaVu/Liberation → the rcParams pattern is wrong and
charts are silently rendering in the fallback font.

### Font installation (Pablo's machine, May 2026)
Akkurat Pro is installed at `/Users/pablou/Library/Fonts/AkkuratPro-Regular.otf`.
`Akkurat Light Pro` is also installed (used for the AIPT lockup
endorsement line). matplotlib registers both correctly.

### Akkurat looks similar to default sans at small sizes
Akkurat Pro is a quiet humanist sans. At small chart sizes (8–12pt),
its differences from default DejaVu Sans are subtle — wider apertures,
slightly more geometric forms, more open counters. Don't mistake the
"quiet" character for fallback rendering. If `findfont()` confirms
Akkurat, trust it.

---

## Subtitles

### Length limits per column span
Hard practical limits based on chart width and brand-spec font sizes:

- **3-col inline (3.68")** at 9pt subtitle → **~50 characters per line**
- **6-col hero (7.5")** at 11pt subtitle → **~95 characters per line**
- **Two-panel spread (7.5", 4.5" tall)** at 11pt → ~95 per line

Beyond these, lines either wrap awkwardly or extend past the chart area.

### Multi-line subtitles are first-class
For 3-col charts especially, write subtitles as:
- **Line 1**: the fact (the "what")
- **Line 2**: the implication (the "so what")

Pattern:
```python
cs.editorial_title(
    ax,
    title="Phantom brand presence",
    subtitle=(
        "Mint shut down March 2024.\n"                     # fact
        "25 months later, AI still mentions it 44% of the time."  # implication
    ),
    column_span="3col_inline",
)
```

`editorial_title()` reserves vertical space proportional to the number
of `\n`-separated lines automatically. No manual padding needed.

### Don't combine subtitle + inline callout
If the subtitle says "Mint shut down March 2024" and the chart highlights
Mint in Indigo against grayscale, an inline callout pointing at the bar
("Defunct since March 2024") is redundant. Color does the editorial
work; the subtitle explains. Adding both clutters the chart and tends
to collide with legends.

---

## Source line + version stamp interaction

### At 3-col inline width
Source line and version stamp **collide** if both are added — the chart
isn't wide enough to fit "Source: ... · n=96 per category" on the left
AND "v0.6 · 30 Apr 2026" on the right.

**Default**: include version in the source line itself, omit the version
stamp. Example: `"Source: Third System AI Presence Index v0.6 · n=96 per category"`

### At 6-col hero width
Plenty of room for both. Use them.

### Source line conventions
Format: `Source: Third System {Product} v{version} · {n}={qualifier} · {date if relevant}`

Examples:
- `Source: Third System AI Presence Index v0.6 · n=96 per category`
- `Source: Third System AI Presence Index v0.6 · 30 Apr 2026`
- `Source: Third System AI Brand Visibility Diagnostic v0.7 · {Client} · 30 Apr 2026`

---

## Color discipline

### Grid behavior depends on chart orientation
The brand spec's default grid is y-axis-only horizontal lines. This
works for **vertical bar charts** (helps readers compare bar heights)
but creates a visual artifact for **horizontal bar charts** — the
gridlines run *through* each bar's centerline, making bars look
striped.

`style_axis_minimal()` accepts an `orientation` argument:
- `'vertical_bar'` (default) — y-axis horizontal gridlines
- `'horizontal_bar'` — no gridlines (the only safe choice for horizontal bars)
- `'scatter'` / `'plot'` — light gridlines on both axes
- `'none'` — no gridlines

For any chart using `ax.barh()`, pass `orientation='horizontal_bar'`:
```python
cs.style_axis_minimal(ax, orientation="horizontal_bar")
```

### The default chart pattern (brand spec)
**Indigo as highlight + Black 20 for everything else.** This is the
qualitative_recommended scheme. Apply it for any chart where one item
needs to stand out from a category of similar items.

```python
colors = cu.highlight_colors(brands, highlight="Mint")
# Returns: [BLACK_20, BLACK_20, ..., ACCENT_INDIGO (for Mint), BLACK_20, ...]
```

### When the highlight needs to fork (per-model breakdown)
For charts that show two values per item (e.g., Anthropic vs OpenAI
presence), the highlighted brand uses **Indigo + Petro** (the family's
accent + lighter shade), and non-highlighted brands use **Black 60 +
Black 20** (matching depth contrast).

This preserves the "single accent + grayscale" rule while distinguishing
the two values per item.

### Tier colors are AIPT-specific
`COLOR_INCUMBENT` (Indigo), `COLOR_MIDTIER` (Petro), `COLOR_CHALLENGER`
(Copper Plate) are reserved for charts that explicitly encode brand
competitive tier — leaderboards, dumbbell variance plots, anywhere the
incumbent/midtier/challenger distinction is the chart's primary axis.

For most charts, use the default (Indigo + grayscale) instead. Don't
default to tier colors just because the data has tiers.

### Per-category coloring violates the spec
Earlier sessions used per-category accent colors (PM = teal, Finance =
copper, etc.) in the matrix and Pattern 2 small multiples. This violates
the spec's "limit to ≤3 colors, ideally one accent + grayscale" rule.

When regenerating these charts, use Indigo+grayscale at the cell level
or single-color sequential ramps within each panel. Do not assign a
unique color per category.

---

## Filename + output discipline

### Canonical filenames (locked)
Output filenames are not improvised. Use `cu.save_chart(fig, pattern_id, column_span)`.
This writes to `reports/output/` with the canonical pattern from the
brand spec:

- `chart_p1_3col.pdf`, `chart_p2_6col.pdf`, etc. (single-span charts)
- `chart_p4_spread.pdf` (two-panel spread)
- `chart_<pattern>_<col_span>col_<medium>.<ext>` (when overriding default print medium)

The typesetting pipeline (Phase C) will look for these exact names.

### Don't use `bbox_inches='tight'` without `pad_inches`
The brand spec mandates `pad_inches=0.15` (with `bbox_inches='tight'`).
Without explicit padding, tight bbox produces inconsistent whitespace
across charts, breaking the page-grid embedding. `cu.save_chart()`
applies these correctly — use it.

---

## Layout patterns

### Scale charts based on content density (top principle)
Chart figsize is a function of data density and visual complexity, NOT
a default. The brand spec defines five figsize options for a reason:

| figsize | When to use |
|---------|-------------|
| 3-col inline (3.68 × 2.85) | ≤8 data points, single message, body-flow chart |
| 4-col (4.95 × 3.71) | 10-20 points per group, multiple groups, callouts |
| 6-col hero (7.5 × 5.0) | 20-50 points, clear visual story, ≤10 labels |
| 6-col hero TALL (7.5 × 6.5) | 50+ points, dense scatter, many labels, aspect=equal |
| 6-col hero SHORT (7.5 × 3.5) | Few categories, banner/landscape feel |

Pattern 2 is the empirical proof: at standard hero (5.0" tall), 80
brands + 25 labels + diagonal aspect=equal crowded the data into ~4×4"
of plotting area. Going to TALL (6.5") gives ~5.5×5.5" — labels
breathe, adjustText resolves cleanly, story reads at a glance.

**Rule of thumb: if `set_aspect("equal")` is set AND the chart has
20+ labeled points, default to TALL (6.5") not standard hero (5.0").**

### Reserve margins BEFORE drawing
The order matters. Always:

```python
fig, ax = plt.subplots(figsize=cs.FIGSIZE_3COL_INLINE)
cs.reserve_margins(fig, layout="single_panel")  # FIRST
# ... draw bars, labels, etc. ...
cs.editorial_title(ax, ...)                      # AFTER drawing
cs.add_source(ax, ...)
```

If you call `editorial_title()` before drawing, the title position
won't match the final axes position (matplotlib re-adjusts).

### `layout` argument matches the chart shape
- `"single_panel"` — one Axes (most charts)
- `"two_panel_landscape"` — Pattern 4 country origin spread, two side-by-side
- `"tall_with_legend_below"` — Pattern 2 small multiples (when implemented)

### Multi-panel charts (3+ panels, e.g., leaderboards)
The `reserve_margins()` helper assumes single-panel — use manual
`fig.subplots_adjust()` for multi-panel layouts. Pattern that works
for vertically-stacked panels:

```python
fig.subplots_adjust(
    top=0.90,      # room for figure-level title + subtitle
    bottom=0.07,   # room for x-axis label AND source line
    left=0.18,     # room for brand-name labels
    right=0.95,
    hspace=0.55,   # vertical space between panels for category labels
)
```

**Critical:** when using manual `subplots_adjust`, **do NOT save with
`bbox_inches='tight'`** — tight cropping eats your reserved margins.
Save with explicit `pad_inches=0.15` only:

```python
fig.savefig(output_path, dpi=cs.DPI_PRINT, pad_inches=cs.PAD_INCHES)
# Note: NOT bbox_inches='tight' for multi-panel charts.
```

`cu.save_chart()` defaults to `bbox_inches='tight'` (correct for
single-panel). For multi-panel, save manually as above.

---

## Data flow assumptions

### Where charts live and what they assume
Charts in `reports/charts/*.py` assume:
1. CWD is the `aias/` root (where the CSVs live)
2. `chart_style`, `chart_utils`, `chart_data` are importable from `reports/`
3. Brand JSON is at `aias/brand/third_system_brand.json`

The `pattern_6_phantom.py` template handles CWD switching internally
(switches to aias root, reads CSVs, switches back). Future charts
follow this pattern.

### Leaderboard CSV columns
Format established in `presence_index_v0.3_*.csv`:
```
rank, brand, tier, presence, consistency, rank_som,
primary_pct, presence_anthropic, presence_openai
```

`load_all_categories()` returns `(data_dict, paths_dict)` where
data_dict keys are: PM, Running, Olive Oil, Skincare, Finance.

### Enriched CSV columns (CEP-level data)
Established in `results_enriched_*.csv`:
```
timestamp, methodology_version, prompt_set_version, brand_registry_version,
prompt_id, cep, model, model_version, temperature, run_idx, call_status,
attempts, elapsed_sec, raw_response, brands_canonical, brands_unknown,
brands_ranked, primary_recommendation, sentiment_summary, extraction_method
```

### CEP label conventions (v0.6)
The `cep` column uses ALL-CAPS labels:
- `COMPARISON` — forced choice across category
- `DISCOVERY` — emerging/noteworthy brands frame
- `FUNCTIONAL_WHY` — functional purpose frame
- `CONTEXTUAL_WHEN` — situational/temporal frame
- `CONSTRAINT_WITH` — constraint/limitation frame
- `IDENTITY_HOW_FEELING` — identity/emotion frame

6 CEPs × 16 runs (8 per model × 2 models) = 96 measurements per category.

When a chart filters by CEP, accommodate the all-caps form first.
Test data and older runs may use Title case (e.g., "Comparison") so
include both as accepted variants.

---

## Versioning the system itself

### When chart_style.py changes
Update the docstring header. The brand spec version it sources from
is logged at module load (`BRAND_SCHEMA_VERSION`).

### When charts change after publication
A published chart filename should not change without the report
version changing. If `chart_p6_3col.pdf` v0.6 ships and we then
revise it for v0.7, the new file replaces the old at the same name —
the report version captures the difference, not the filename.

For pre-publication iteration (like today), overwrite freely.

---

## Empirical defaults (developed from chart sessions, not in brand JSON)

| Pattern | Value | Source |
|---------|-------|--------|
| Bar height (grouped barh) | 0.38 | Pattern 6 — leaves visible gap between brand pairs |
| Diagonal reference linewidth | 0.5pt | Subtle background grid weight |
| adjustText force_text | (0.5, 0.8) | Tuned for 6-col scatter with ≤20 labels |
| adjustText force_points | (0.4, 0.6) | Allows labels to push slightly off points |
| Subtitle leading | font_size + 2pt | Standard typographic leading |
| Source-line offset below axes | 0.50 inches | Clears x-axis tick labels + axis label |

These get used as defaults but are not locked. If a future chart needs
a different value, document why in the chart file's docstring.

---

## Phase B chart inventory (status)

| # | File | Status | Notes |
|---|------|--------|-------|
| 1 | `pattern_6_phantom.py` | ✅ Working | First chart proved system end-to-end, two-line subtitle |
| 2 | `leaderboards_panel.py` | ✅ Working | Five-category panel, multi-panel margin pattern |
| 3 | `pattern_1_variance.py` | ✅ Working | Per-model dumbbell, right-side spread labels, horizontal_dot orientation |
| 4 | `pattern_3_awareness.py` | ✅ Working | Awareness divergence dot plot, beeswarm + adjustText, 4-col span |
| 5a | `pattern_2_asymmetry.py` | ✅ Working | **Hero scatter with margin annotations** (reconstruction of original parallel-chat form). Two annotation stacks (Discovery-favoring above, Comparison-favoring below) sorted by dot _plot_y to prevent leader-line crossings. |
| 5b | `pattern_2_smallmultiples.py` | ✅ Working | **Alternative form** — 2×3 small multiples (5 category panels + legend cell). Saves to `chart_p2_6col_smallmultiples.pdf`. Both forms kept for layout flexibility. |
| 6 | `pattern_4_country.py` | ✅ Working | Two-panel spread (FIGSIZE_SPREAD 7.5×4.5), strip plot per panel, brands grouped by country on y-axis, color encodes heritage vs newer producer. Hard-coded brand→country map covers ~30 brands per category. Uses anisotropic `axis="y"` jitter (threshold=5.0, spread=0.32) to fan close brands vertically within each row without moving x. |
| 7 | `cep_heatmap.py` | ✅ Working | 3-col inline heatmap, top 8 brands × 6 CEPs (PM Software featured), Indigo intensity scale 0-100%. Cells annotated when ≥10%. Bold y-tick labels mark Default Reinforcement signature (mean ≥40, spread <35). Mode-aware hatching infrastructure wired via MODE_BY_CELL hook (unused in v0.6 — activates when v0.7 enriched data adds mode column). |
| 8 | `matrix_aggregate.py` | ✅ Working | 6-col TALL **categorical evidence matrix**, 6 patterns + 1 Modes row × 5 categories. Each cell holds a concrete data tag ("42pt", "9 brands", "Spanish < 25%", "Mint 44%") not a derived score. 5-step intensity scale (Not present → Very strong) drives cell opacity. Each column uses **its own category accent color** at varying opacity rather than one shared Indigo gradient — preserves category visual identity while keeping shading semantics within each column. Cell content stored in `MATRIX_CONTENT` dict at top of file; edit dict to update for new versions. |

---

## Lessons from charts 3-5 (May 2 session continuation)

### Chart construction checklist (auto-applied, every chart)
**Before declaring any chart "done", verify these proactively. The user
should not have to ask.**

1. **Coincident dot check.** If the chart has scatter dots and ANY two
   data points share an (x, y) within ~2 percentage points, apply
   `cu.jitter_overlapping_points()` BEFORE plotting. This applies to:
   - Cross-category scatters (Pattern 2)
   - Strip plots per row/group (Pattern 4)
   - Any beeswarm or 1D distribution (Pattern 3)
   - Anywhere multiple brands share an axis value
   The reflex must be: "scatter chart? → jitter check first."

2. **Diagonal-after-limits.** If the chart has `add_diagonal_reference()`,
   call it AFTER `set_xlim`/`set_ylim` AND pass explicit `lo=`, `hi=`.

3. **Grid orientation.** Charts with horizontal-data-axis (dot plots,
   bars) use `orientation="horizontal_dot"` or `"horizontal_bar"`,
   never the default. This suppresses irrelevant gridlines.

4. **Label collision.** Any chart with >5 labels needs adjustText OR
   margin annotations. Inline labels with no collision-resolution
   only work for ≤5 brand callouts.

5. **Empty space audit.** Before saving, mentally check: is there
   empty space inside the figure that's not data-meaningful? If yes,
   either fill it (margin annotations, legend, callouts) or shrink
   the figsize.

6. **Title verb → color encoding.** Color encodes whatever the title's
   verb operates on. Don't default to tier colors — choose deliberately.

7. **Subtitle line width.** Each subtitle line ≤80 characters at 6-col,
   ≤55 at 4-col, ≤45 at 3-col. Break long subtitles into 2 lines.

8. **Source line + version.** At hero scale, drop the version stamp
   (include date in source line). At 3-col, source line only.

If any of these are missing when you preview a chart, fix them BEFORE
asking the user "does this look good?"

### Normalize CEP keys (and similar enum-like data fields)
Real v0.6 data uses ALL_CAPS_WITH_UNDERSCORES for CEPs ("FUNCTIONAL_WHY",
"COMPARISON"). Older test data and the brand JSON use Title Case
("Functional", "Comparison"). When you write a chart that depends on
specific CEP keys, never hardcode one casing. Use a normalization helper:

```python
def _cep_canonical_key(observed_cep: str) -> str | None:
    if not observed_cep:
        return None
    head = observed_cep.upper().split("_")[0]
    head = head.split()[0]
    for canonical in CEP_ORDER:
        if canonical.split("_")[0] == head:
            return canonical
    return None
```

Apply the same pattern for any enum-like field (mode, tier, category)
that might come in different casing across data versions. Always
match by leading word, case-insensitive.

### `aspect="equal"` traps the matrix into wasted space
Heatmap matrices intuitively want square cells, but `set_aspect("equal")`
forces the matrix to shrink to whichever dimension is most constrained.
With 6 columns × 8 rows in a 3-col-wide chart, square cells make the
matrix tiny relative to the available canvas. Drop `set_aspect` for
heatmaps and let cells be rectangular — they fill the space, the
content stays readable, and the chart doesn't look anemic.

The same applies to stacked bars, mosaic plots, and any rectangular-grid
chart where cells don't carry geometric meaning beyond "this row × this
column." Reserve `aspect="equal"` for scatters with a y=x diagonal
(Pattern 2) where the geometry of the diagonal must be 45°.

### Forward-looking infrastructure hooks
Pattern 5 wires up `MODE_BY_CELL` and `mode_style()` even though v0.6
data has no mode classification. The chart renders fine in pure brand
mode today, and the moment v0.7 enrichment adds a mode column, hatching
activates without code changes — populate the `MODE_BY_CELL` dict and
the chart picks it up.

Pattern: when adding infrastructure for a feature that's coming but
isn't here yet, build the hook as an empty dict/lookup and document
where to populate it. Don't gate the chart on the feature; let it
render gracefully without and upgrade silently when data lands.

### Content-driven matrix vs computed-score heatmap (Pattern 8)
For summary charts that aggregate findings across many patterns, prefer
**concrete data labels per cell** over a single 0-100 derived score.
Pattern 8's first version used `PATTERN_SCORERS` formulas to compute
each cell's strength as a number — clean code, but the chart became
abstract: every cell looked the same shape and the reader had to trust
the math.

The second version stored each cell's actual finding ("9 brands",
"Spanish < 25%", "6/6 CEPs", "Mint 44%") with an explicit 0-4 intensity
rating, in a hardcoded `MATRIX_CONTENT` dict at the top of the file.
This is *more* work to update (edit a dict for each report version) but
*much* more readable — the cell IS the finding, not a number standing
in for one.

**Decision rule:**
- Use computed-score heatmap when cells share a meaningful unit (e.g.,
  Pattern 5: every cell is "% mention rate at this CEP").
- Use content-driven matrix when cells across rows have heterogeneous
  units that would require unit-stripping (e.g., "42 points" for
  variance, "9 brands" for asymmetry, "Spanish < 25%" for language
  bias). Don't force them onto a unified 0-100 scale; show the original
  units and add a separate intensity rating.

When the cell IS the finding, the matrix becomes a self-contained report
summary readable independently of the body copy.

### Per-column accent colors with intensity-based opacity
For category-distinguishing matrices like Pattern 8, instead of one
shared Indigo gradient across all columns, use **each category's own
accent color** at varying opacity per cell. This preserves the
category's visual identity while keeping intensity-shading semantics
inside the column.

```python
CATEGORY_COLORS = {
    "PM":        cs.ACCENT_INDIGO,
    "Running":   cs.COLOR_MIDTIER,
    "Olive Oil": cs.ACCENT_HONEY,
    "Skincare":  cs.ACCENT_COPPER_PLATE,
    "Finance":   cs.ACCENT_OCEAN,
}

face = _hex_to_rgba(CATEGORY_COLORS[cat], alpha=intensity_opacity)
```

This works because the reader compares cells *within* a column (across
rows) more than *between* columns (across categories). The within-column
opacity gradient is what carries the strength claim; the between-column
color difference reinforces "these are different categories." Win-win.

The legend below uses one neutral color for the 5 intensity swatches —
otherwise the 5×5 = 25 swatches needed to show every category's gradient
would overwhelm the reader.

### Multi-line column headers must fit within column width
Long category labels like "Premium Facial Skincare" or "Personal
Finance Apps" can collide with adjacent columns when set as `\n`-broken
two-liners — the second line of one header overlaps the first line of
the next. Matplotlib doesn't auto-wrap text to column width.

**The fix:** shorten each label so each line fits its column. "Premium
Facial Skincare" → "Premium\nSkincare". "Personal Finance Apps" →
"Personal\nFinance Apps". The full names live in body copy, not chart
headers. Chart headers are scan targets — they need to be short
enough to not collide, not exhaustive.

Sanity check before saving: at the chart's intended print size, does
each header line fit within ~85% of its column width? If not, drop
words.

### Per-pattern strength formulas as tunable config (Pattern 8)
When a chart needs to score multiple heterogeneous patterns onto a
single scale (Pattern 8 maps 6 patterns × 5 categories to 0-100), the
scoring functions belong at the top of the file as a `PATTERN_SCORERS`
dict — each function takes `(category, leaderboards, cep_counts, ...)`
and returns a 0-100 float. Pattern:

```python
def score_p1_variance(category, leaderboards, **_) -> float:
    rows = leaderboards.get(category, [])
    spreads = [...]  # compute from data
    return min(100.0, mean(spreads))

PATTERN_SCORERS = {
    "p1": score_p1_variance,
    "p2": score_p2_asymmetry,
    ...
}
```

Why this pattern works:
- **Scoring logic is one expression per pattern**, easy to read and
  tune independently
- **Falsifiable per pattern** — bad score? Look at one function.
- **Forward-compatible** — when a new pattern ships, add a new scorer
- **Sensible defaults** — patterns without applicable data return 0,
  not error (Heritage geography returns 0 for PM/Running/Finance)

Document the formula's domain assumption in the docstring (e.g., "50pp
spread = 100 score"). Future-you will tune these constants and want
to know what the original mapping was.

### Manual matrix axis positioning instead of subplots
Pattern 5 and Pattern 8 both use `fig.add_axes([left, bottom, w, h])`
with explicit figure-relative coordinates instead of `plt.subplots()`.
This is the right call when:
- Multiple matrix-like axes need precise vertical stacking (Pattern 8:
  6×5 main matrix + 1×5 modes row strip below)
- You need a manual colorbar position outside of subplots layout
- Margin reservation must be exact for title/subtitle/source bands

The trick: lay out the y-coordinates as a vertical budget, top-down:
```
top=0.96  (figure top edge)
↓ title
0.93
↓ subtitle line 1
0.90
↓ subtitle line 2 (if needed)
0.87
↓ ↓ small gap
matrix_top_y = 0.78  (top of matrix axis, leaves room for column headers)
↓ matrix
matrix_bot_y = 0.22
↓ modes row (separated by 0.02 gap)
modes row 0.14-0.20
↓ source line
0.018 (bottom)
```

Allocate by reading top-to-bottom; each band gets specific height.

### Verify jitter against real data, not synthetic previews
Synthetic test data routinely underrepresents the pathologies of real
data. Pattern 4 took two stacking complaints to fix because synthetic
preview showed only 2-3 brands per country — real data had 5-8 brands
per country with multiple clusters of close-but-not-identical values.

**Protocol when a chart has scatter dots that might overlap:**

1. Before rendering, ask the user to run a one-line diagnostic that
   lists every per-group cluster in the real data:

```python
from collections import defaultdict
import numpy as np
data = get_<chart>_data()
for group_key, rows in data.items():
    print(f"=== {group_key} ===")
    by_subgroup = defaultdict(list)  # e.g., country, category
    for r in rows:
        by_subgroup[r["subgroup"]].append(r)
    for sg, brands in by_subgroup.items():
        if len(brands) < 2:
            continue
        brands.sort(key=lambda b: b["value"])
        print(f"  {sg} (n={len(brands)}):")
        for b in brands:
            print(f"    {b['name']:30s} value={b['value']:6.2f}")
```

2. Look at the output. Identify the closest pairs/triples of values
   within each subgroup. Tune `threshold` to be slightly larger than
   the largest in-cluster gap you want to spread.
3. THEN render. Don't tune jitter parameters in the dark.

**Coincidence threshold rule of thumb (percentage-presence data):**
- threshold=2 catches only near-identical values (gap < 2pp)
- threshold=5 catches loose clusters (gap up to 5pp) — usually right
- threshold=10 catches broader clusters but starts pulling unrelated points
- Spread ≈ 0.3 in y-units works for strip plots where row height = 1

**Mapping completeness check.** When a chart relies on a hard-coded
brand→attribute mapping (Pattern 4's country dict), the diagnostic
output will surface unmapped brands as `[warn] no mapping for: X, Y, Z`.
Look at that warn list before considering the chart done. Pattern 4
silently dropped 17 of 31 skincare brands the first time.

### Always ask for prior versions before rebuilding (process lesson)
**Pattern 2 was built once before in a parallel chat at the wrong
dimensions (9.5×8.0).** A separate brand-spec chat sent a directive
to "re-render at 7.5×5.0 or 7.5×6.5." Today's session interpreted
that directive as "build from scratch at the new dimensions" — and
ran through 6 painful iterations rediscovering density, jitter, and
form decisions the parallel chat had likely already solved.

The fix: **at the start of any chart session, ask "is there a prior
version of this chart in another chat? If so, please share the code
or PDF."** Even at wrong dimensions, the prior version contains:
- Chart-form decisions (scatter vs bars vs slope) already made
- Color/tier encoding already chosen
- Label strategy already considered
- Anti-collision tactics already attempted

Re-scaling an existing chart is ~30 minutes. Rebuilding from zero is
half a day. The same applies for chart #6 (Pattern 4) — it was also
built in the parallel chat at 13×6.5; ask for the code BEFORE writing
new code.

### When iterating fails, change form (top meta-lesson)
**Two-round budget rule.** If a chart receives the same complaint
(crowded / overlapping / hard to read) on two consecutive iterations,
STOP iterating on parameters. The form is wrong. Examples of "same
complaint" — these are the same problem in different words:
- "too dense" / "too crowded" / "hard to read"
- "overlapping" (any kind: dots, labels, lines)
- "still cluttered after [your fix]"
- "I can't tell where things are"

What I did wrong on Pattern 2 (DON'T REPEAT):
1. Round 1: built single 6-col hero scatter, 80 dots, dense
2. Round 2: added adjustText threshold + label filter (still dense)
3. Round 3: switched to TALL figsize + better legend (still dense)
4. Round 4: added 2D jitter helper for coincident dots (still dense)
5. Round 5: rebuilt as small multiples 2×3 grid (still dense)
6. Round 6: tuned jitter parameters more aggressively per-panel (acceptable)

That's six rounds. It should have been two. After round 2's complaint
matched round 1's, I should have asked: **"is a scatter the right form
for this data?"** rather than added another anti-collision tool.

What to do at the two-round mark:
1. **Inventory the real data.** Send a one-line diagnostic to count
   coincident points, ranges, distribution. Synthetic preview data
   often lies about pathologies.
2. **Question the form, not the parameters.** Ask explicitly: "Could
   ranked bars / slope chart / categorical dot plot / table tell this
   story more directly than a scatter?"
3. **Match form to claim.** "Asymmetry repeats across categories"
   could be: 5 small scatters (used), OR 5 ranked-bar panels (cannot
   overlap), OR a slope chart per brand connecting two ranks. Pick the
   form whose shape IS the claim.
4. **Propose 2-3 alternative forms with explicit trade-offs** before
   patching again. Let the user choose. Don't just iterate.

The reflex "add another anti-collision mechanism" is the trap.
Chart-level questions trump tool-level fixes. **Ask "what shape tells
this story?" before "what parameter fixes this complaint?"**

### When to choose small multiples over a single hero
Pattern 2 was first attempted as a single 6-col hero scatter with all
~80 brands across 5 categories on one set of axes. Even with jitter +
adjustText + tier color encoding, the chart stayed too dense to read.

Reason: when the editorial claim is **"this pattern repeats across
groups"** (as Pattern 2 says — "the asymmetry repeats across all five
categories"), the right form is small multiples. A single hero hides
the cross-group claim inside within-group clutter. Small multiples
expose it through repetition: 5 panels each showing the same
upper-left/lower-right asymmetry IS the cross-category claim.

Decision criteria for small multiples:
- The claim is "X repeats across groups" or "X varies systematically"
- Each group has ≥10 data points (enough to show pattern)
- ≤6 groups (more than 6 makes the grid too cramped per panel)
- Within-group reading matters as much as cross-group comparison

For Pattern 2: 5 groups × ~15 brands each in a 2×3 grid (6th cell =
legend with descriptions) at 6-col TALL figsize. Each panel ~2.4×3"
plotting area. Top 3 most asymmetric brands per panel labeled. Reader
can scan panels to see the pattern (cross-category claim) AND zoom
into any panel for within-category detail.

If you find yourself adding more and more anti-collision machinery
(jitter, adjustText, distance thresholds, top-N-per-tier filtering)
to a single hero chart, that's a signal to step back and consider
small multiples instead.

### When to graduate a chart from 3-col to 4-col
Brand spec defines `4_column` figsize (4.95" × 3.71") for "wider-than-body
charts that need more horizontal space without going full-width." Use it
when ALL of these apply:
- ≥3 categorical groups (rows or panels)
- ≥10 data points per group
- Inline label callouts beyond 3-4 highlighted brands

Pattern 3 was the canonical case: 5 category rows × ~12 brands × 7+
highlighted brands with adjustText. 3-col was too cramped; 6-col would
have been overkill. 4-col fits the "more room without becoming a hero"
brief perfectly.

### Right-side annotations for under-utilized whitespace
When a chart's data range doesn't fill its column width (e.g., dot plot
with x ranging 0-100 but most data clustering 0-80), use the right-side
empty space for value annotations. Pattern 1 establishes this pattern:

```python
SPREAD_LABEL_X = 108  # Just outside xlim=(-5, 105) — extends past edge
ax.set_xlim(-5, 145)  # Extend xlim to make room for labels
ax.set_xticks([0, 20, 40, 60, 80, 100])  # Restrict tick labels to data range
for yi, val, brand in zip(y, vals, brands):
    ax.text(SPREAD_LABEL_X, yi, f"{val} pt",
            ha="left", va="center", fontsize=sizes["data_label"],
            color=cs.COLOR_MUTED)
```

The visual rule: extend xlim past the data range, restrict x-ticks to
the data range, place labels in the extension. Reads as "annotation,
not data."

### Right-edge label flipping (for labels at high x values)
When a labeled brand sits at the right edge of the chart (x ≥ ~85% of
xlim), flip the label to the LEFT of the dot to avoid clipping. Pattern 3
established this:

```python
if presence_vals[i] >= 85:
    label_x = presence_vals[i] - 1.5
    ha = "right"
else:
    label_x = presence_vals[i] + 1.5
    ha = "left"
```

YNAB at 100% in Personal Finance was the case that surfaced this. Apply
the same rule to any right-edge labeled brand.

### Distance-threshold labeling for cross-category scatters
Pattern 2's hero scatter has ~80 brands across 5 categories. Labeling
all of them is visual noise; labeling none defeats the chart. The rule:
**label only brands whose asymmetry exceeds a threshold.**

```python
LABEL_DISTANCE_THRESHOLD = 30  # in presence-percentage points
def is_labeled(r):
    return abs(r["discovery_pct"] - r["comparison_pct"]) >= LABEL_DISTANCE_THRESHOLD
```

This labels the brands where the chart's story is sharpest. Adjust
threshold per chart based on data spread — 30 worked for Pattern 2,
might need to be 25 or 40 for other 6-col scatter charts.

### Hero (6-col) charts: source line should include date
At 6-col width, the legend tile + source line + version stamp at the
bottom can collide horizontally. Solution: drop the version stamp,
include the date in the source line itself:

```python
SOURCE_TEXT = "Source: ... v0.6 · n=96 per category · 30 Apr 2026"
cs.add_source(ax, SOURCE_TEXT)
# Note: NO add_version_stamp at hero scale.
```

The source line carries all the provenance information without needing
a second annotation.

### Tier color encoding is the right call for cross-category scatters
Pattern 2 uses Indigo (incumbent) + Petro (mid-tier) + Copper Plate
(challenger) as primary visual encoding. This is the AIPT canonical
scheme and works because:
- The story IS the tier-frame interaction (challengers in upper-left,
  incumbents in lower-right of the diagonal)
- Tiers are stable across categories (incumbent in PM ≠ incumbent in
  Skincare, but both are "incumbent" tier)
- Three colors stay within the brand spec's "≤3 colors" rule

Don't use tier colors for charts where tier ISN'T the primary signal.
Pattern 1 (per-model variance dumbbell) doesn't tier-encode — variance
itself is the message; tier is incidental.

### Set aspect="equal" for diagonal-reference scatters
`ax.set_aspect("equal", adjustable="box")` makes a 45° diagonal
genuinely 45° on the page. Without it, the diagonal looks 45° in data
space but might render at 30° or 60° depending on figure proportions.
Pattern 2 needs aspect=equal because the y=x reference is the chart's
primary semantic structure.

### CRITICAL: call `add_diagonal_reference()` AFTER `set_xlim/set_ylim`
Bug pattern hit on Pattern 2: diagonal vanishes silently if drawn
BEFORE axis limits are set. matplotlib's `get_xlim()` returns the
default `(0.0, 1.0)` until `set_xlim()` is called, so the diagonal
gets drawn from (0,0) to (1,1) — invisible inside a (0,100) chart.

Two fixes (use both, defensively):
1. **Always set xlim/ylim BEFORE calling diagonal helper.**
2. **Pass explicit `lo=0, hi=100`** to `add_diagonal_reference()` so
   the line draws from data-meaningful coordinates regardless of
   axis state at call time.

```python
# CORRECT order:
ax.set_xlim(-3, 105)
ax.set_ylim(-3, 105)
cu.add_diagonal_reference(ax, lo=0, hi=100, ...)  # explicit + safe
```

The helper now also emits a warning if the resolved range looks like
the matplotlib default `(0,1)`, so the bug isn't silent next time.

### Top-N-per-tier label policy for cross-category scatters
For dense scatters (50+ brands across multiple tiers), pure threshold-
based labeling is fragile — real data may produce 40 labels above any
reasonable threshold, overwhelming adjustText.

Better pattern: filter by minimum threshold, THEN keep top-N most
extreme per tier. Caps total labels regardless of data density:

```python
LABEL_DISTANCE_THRESHOLD = 35  # min asymmetry to be a candidate
LABELS_PER_TIER = 5            # top-N per tier — total ≤15 labels

candidates = [r for r in rows if asymmetry(r) >= THRESHOLD]
# group by tier, sort desc by asymmetry, keep top N per tier
```

For Pattern 2 with ~80 brands: 5 per tier × 3 tiers = up to 15 labels,
which adjustText can resolve cleanly at 6-col TALL figsize.

### Two-panel spread (FIGSIZE_SPREAD = 7.5 × 4.5) margins
For two-panel side-by-side charts like Pattern 4 (country origin):

```python
fig, axes = plt.subplots(1, 2, figsize=cs.FIGSIZE_SPREAD)
fig.subplots_adjust(
    top=0.78,       # title + 2-line subtitle band
    bottom=0.22,    # x-axis labels + legend + source line
    left=0.13,      # y-axis country labels need ~13% (longest: "USA (n=8)")
    right=0.97,
    wspace=0.42,    # generous between panels — long y-labels need room
)
```

`wspace=0.42` is wider than the brand-spec default of 0.18 because long
y-axis labels would collide if panels were closer. Tune by label length:
short labels → 0.18, long labels (with parenthetical n=) → 0.42.

### Color encoding follows the title's verb
For Pattern 4, color is NOT tier — it's heritage-vs-newer producer
country. **Indigo = heritage, Copper Plate = newer.**

Decision rule: **encode whatever the title's verb operates on.**
- "Heritage geography reinforces bias" → encode by heritage status (Pattern 4)
- "Discourse position outranks commercial scale" → encode by divergence direction (Pattern 3)
- "AI's answer depends on the question" → encode by tier (Pattern 2 — tier is the actor whose behavior changes between frames)

Don't default to tier color encoding for every chart. Tier is the right
encoding when tier IS the primary signal (Pattern 2), wrong when the
signal is something else (heritage status, divergence direction).

### Hard-coded brand attribute mappings
When a chart needs a brand attribute not in the leaderboard CSVs (country,
founding year, parent company, etc.), keep the mapping as a module-level
dict at the top of the chart file. Pattern 4 uses `OLIVE_OIL_COUNTRY`
and `SKINCARE_COUNTRY` dicts plus a `HERITAGE_COUNTRIES` set per category.
Brands not in the mapping are DROPPED with a `[warn]` so absences are
visible at render time.

Don't try to infer brand attributes from brand names at runtime — that's
brittle and silent-failing. Explicit mapping + loud unknowns is safer.

### Mean-marker tick for categorical strip plots
For strip plots with multiple dots per row (Pattern 4), add a vertical
tick at each row's mean as visual summary:

```python
for i, country in enumerate(sorted_countries):
    mean_x = country_means[country]
    ax.plot([mean_x, mean_x], [i - 0.25, i + 0.25],
            color=cs.BLACK_60, linewidth=1.2, zorder=2)
```

The eye reads "where is the country mean?" before noticing individual
dot positions. Without it, readers have to mentally average each row.

### Coincident dots need 2D jitter, not just label adjustment
For dense scatters (Pattern 2 cross-category, future similar charts):
multiple brands often sit at exactly the same (x, y) — e.g., 4 incumbents
all surfacing in 100% of Comparison runs. Without jitter, only ONE dot
is visible; the others stack invisibly underneath.

`adjustText` only spreads LABELS; the underlying dots remain stacked.

Use `cu.jitter_overlapping_points()` to spread coincident dots in a
small ring around their shared center BEFORE plotting:

```python
all_x = np.array([r["x_val"] for r in rows])
all_y = np.array([r["y_val"] for r in rows])
jit_x, jit_y = cu.jitter_overlapping_points(
    all_x, all_y,
    threshold=2.0,   # within 2 units = "same point"
    spread=2.5,      # ring radius for clustered dots
)
# Store jittered positions on the row dicts so labels point to the visible dot
for r, jx, jy in zip(rows, jit_x, jit_y):
    r["_plot_x"] = float(jx)
    r["_plot_y"] = float(jy)
```

Then use `r["_plot_x"]` and `r["_plot_y"]` for both `ax.scatter()` AND
`ax.text()` placement, so labels follow the dot to its jittered position.

Tune `threshold` and `spread` based on data range:
- Percentage data (0-100): threshold ~1-2, spread ~2-3
- Per-row scaled data (0-5): threshold ~0.05, spread ~0.1

### Empty quadrants in scatter plots are often structurally meaningful
A Comparison-vs-Discovery scatter has natural empty regions:
- **Upper-right** (high in both frames) is rare — few brands score
  high in both Comparison AND Discovery contexts
- **Lower-left** (low in both) is the "doesn't surface anywhere" tail

Don't fight these empty regions by compressing axes. They communicate
structural facts about how brands distribute across prompt frames.
**Use them productively for the legend** — Pattern 2 puts the legend
in the upper-right at `bbox_to_anchor=(0.98, 0.98)`, which is the
quadrant guaranteed to be sparse.

### font_sizes_for() now handles all column spans
Previously fell through to 3-col defaults for 4-col, 2-col, and 1-col.
Now reads the brand spec's `by_column_span` table and returns
appropriate sizes for any span. **When using a chart at non-3-col
width, always pass the explicit column span to all helpers:**

```python
sizes = cs.font_sizes_for("4col")  # ← top of render() function
ax.set_xlabel("...", fontsize=sizes["axis_label"])
cs.editorial_title(ax, ..., column_span="4col")
```

Don't reuse `cs.FONT_SIZES_3COL` literals when the chart is 4-col.

### Grid orientation: explicitly disable, then enable
The fix in `style_axis_minimal()` is to call `ax.grid(False)` first,
THEN `ax.grid(True, axis="x|y|both")` for the wanted axis. Without the
explicit disable, the global rcParams default (y-axis grid for vertical
bars) leaks through into orientations that should suppress it.

For dumbbells/dot plots: use `orientation="horizontal_dot"` — vertical
gridlines only, no horizontal stripes through rows.

For horizontal bars: use `orientation="horizontal_bar"` — no gridlines
at all (horizontal grid + horizontal bars = stripe artifact).

For scatter plots: use `orientation="scatter"` — gridlines on both
axes.

### Multi-panel margins pattern (5 panels stacked)
For leaderboards-style multi-panel charts:

```python
fig.subplots_adjust(
    top=0.88,      # room for figure-level title + subtitle (2 lines)
    bottom=0.07,   # room for x-axis label + source/version line
    left=0.18,     # room for brand-name labels
    right=0.95,
    hspace=0.55,   # vertical space between panels for category labels
)
```

**Critical: do NOT use `bbox_inches='tight'` for multi-panel charts.**
Tight cropping eats your reserved margins. Save manually with explicit
`pad_inches=0.15`:

```python
fig.savefig(output_path, dpi=cs.DPI_PRINT, pad_inches=cs.PAD_INCHES)
# NOT bbox_inches='tight'
```

`cu.save_chart()` defaults to tight bbox — correct for single-panel,
wrong for multi-panel. For multi-panel, save manually as above.

---

Last updated: 2 May 2026 (v0.6 redesign session, charts 3-5 added)
