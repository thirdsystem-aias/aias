"""Fork build_report_v10.py -> build_report_v11.py with surgical edits.

Run from the repo root after sourcing the venv:
    cp ~/aias/reports/build_report_v10.py ~/aias/reports/build_report_v11.py
    python scripts/fork_v10_to_v11.py

Each patch is asserted-on-load: if a target isn't found exactly once (or N
times where N is documented), the script halts before writing. Idempotent on
a clean copy of v0.10.
"""
from pathlib import Path
import sys

SRC = Path.home() / "aias" / "reports" / "build_report_v11.py"

PATCHES = [
    # --- 1. Module docstring header
    (
        '"""\nv0.10 Naive-Phantom Rate Longitudinal Stability — typesetting pipeline.\n\nForked from build_report_v09.py with surgical changes:',
        '"""\nv0.11 PM Software × Google Trends Construct Validity — typesetting pipeline.\n\nForked from build_report_v10.py with surgical changes:',
    ),

    # --- 2. Import line
    (
        "import v10_naivephantom_content as content  # noqa: E402",
        "import v11_pmtrends_content as content  # noqa: E402",
    ),

    # --- 3. Add v0.11 figsize keys to CHART_FIGSIZE_IN dict
    (
        '    "6_col_v10_h3":         (7.50, 4.40),  # F3 H3 decoupling line plot\n}',
        '    "6_col_v10_h3":         (7.50, 4.40),  # F3 H3 decoupling line plot\n'
        '    # v0.11 additions: three figsize variants matching the matplotlib\n'
        '    # figsize used in build_charts_v11_pmtrends.py.\n'
        '    "6_col_v11_scatter":    (7.50, 5.00),  # F1 / F2 scatter plots\n'
        '    "6_col_v11_rankshift":  (7.50, 6.50),  # F3 rank-shift slope chart (tall)\n'
        '    "6_col_v11_partial":    (7.50, 5.00),  # F4 partial-residual scatter\n'
        '}',
    ),

    # --- 4. Header right text on body chrome
    (
        '"Naive-Phantom Rate Stability \\u00b7 v0.10 \\u00b7 9 May 2026"',
        '"PM Software \\u00d7 Trends Construct Validity \\u00b7 v0.11 \\u00b7 10 May 2026"',
    ),

    # --- 5. Hero check tuple — add v0.11 slot names
    (
        '        # v0.10 slot names — all three findings render full-width hero\n'
        '        # (the charts are wide-format and benefit from the spread frame).\n'
        '        "hero_f1_valence", "hero_f2_h2_split", "hero_f3_decoupling",\n'
        '    )',
        '        # v0.10 slot names — all three findings render full-width hero\n'
        '        # (the charts are wide-format and benefit from the spread frame).\n'
        '        "hero_f1_valence", "hero_f2_h2_split", "hero_f3_decoupling",\n'
        '        # v0.11 slot names — all four findings render full-width hero.\n'
        '        "f1_scatter_t1", "f2_scatter_t2", "f3_rank_shift_t1", "f4_partial_residual_t1",\n'
        '    )',
    ),

    # --- 6. Append v0.11 captions to HERO_FIGURE_CAPTIONS
    (
        '    "hero_f3_decoupling": (\n'
        '        "Figure 3 \\u00b7 Directional decoupling of gross Presence and "\n'
        '        "naive-phantom rate across t<sub size=\'6\'>1</sub> \\u2192 t<sub size=\'6\'>2</sub>. "\n'
        '        "Gross Presence falls from 44.79% to 41.67% (\\u0394 = \\u22123.12pp) "\n'
        '        "while the naive rate rises from 0.00% to 2.50% (\\u0394 = +2.50pp). "\n'
        '        "The directions are opposite; the magnitudes are comparable in "\n'
        '        "absolute terms. At the matched-subset n observed (43 and 40), the "\n'
        '        "pattern is noise-dominated and reported as diagnostic only per "\n'
        '        "pre-reg \\u00a72 H3."\n'
        '    ),\n'
        '}',
        '    "hero_f3_decoupling": (\n'
        '        "Figure 3 \\u00b7 Directional decoupling of gross Presence and "\n'
        '        "naive-phantom rate across t<sub size=\'6\'>1</sub> \\u2192 t<sub size=\'6\'>2</sub>. "\n'
        '        "Gross Presence falls from 44.79% to 41.67% (\\u0394 = \\u22123.12pp) "\n'
        '        "while the naive rate rises from 0.00% to 2.50% (\\u0394 = +2.50pp). "\n'
        '        "The directions are opposite; the magnitudes are comparable in "\n'
        '        "absolute terms. At the matched-subset n observed (43 and 40), the "\n'
        '        "pattern is noise-dominated and reported as diagnostic only per "\n'
        '        "pre-reg \\u00a72 H3."\n'
        '    ),\n'
        '    # v0.11 figure captions\n'
        '    "f1_scatter_t1": (\n'
        '        "Figure 1 \\u00b7 Per-brand AI Presence (matched subset, Sonnet 4.6 + "\n'
        '        "GPT-5.4-mini, PM software) against Google Trends rescaled mean at "\n'
        '        "t<sub size=\'6\'>1</sub>. Worldwide region. Log-y axis. Pivot brand Asana indexed "\n'
        '        "to 100 by construction. Spearman <font name=\'Helvetica\'>\\u03c1</font> = 0.496 "\n'
        '        "(p<sub size=\'6\'>1t</sub> = 0.021); Pearson r = 0.544. n = 17."\n'
        '    ),\n'
        '    "f2_scatter_t2": (\n'
        '        "Figure 2 \\u00b7 Same shape at t<sub size=\'6\'>2</sub>. The cross-wave visual "\n'
        '        "stability is the H2 finding: Spearman <font name=\'Helvetica\'>\\u03c1</font> = 0.476; "\n'
        '        "|\\u0394<font name=\'Helvetica\'>\\u03c1</font>| from t<sub size=\'6\'>1</sub> = 0.020. "\n'
        '        "Whatever the construct is, it reproduces."\n'
        '    ),\n'
        '    "f3_rank_shift_t1": (\n'
        '        "Figure 3 \\u00b7 Slope chart: each brand\'s rank by AI Presence (left) "\n'
        '        "connected to its rank by Trends (right) at t<sub size=\'6\'>1</sub>. Steep slopes "\n'
        '        "indicate construct divergence. Extreme cases (|\\u0394rank| \\u2265 8) "\n'
        '        "highlighted in copper. Linear (top-left) and Todoist (mid-right) anchor "\n'
        '        "the divergence diagnostic discussed in Finding 3."\n'
        '    ),\n'
        '    "f4_partial_residual_t1": (\n'
        '        "Figure 4 \\u00b7 H4 partial correlation visualisation. Rank residuals on "\n'
        '        "both axes after OLS on rank-transformed brand age and tier ordinal. "\n'
        '        "Partial Spearman <font name=\'Helvetica\'>\\u03c1</font> = 0.407 (p<sub size=\'6\'>1t</sub> = 0.066), "\n'
        '        "missing both the moderate-to-strong threshold and (at t<sub size=\'6\'>1</sub>) "\n'
        '        "the significance bar."\n'
        '    ),\n'
        '}',
    ),

    # --- 7. _slot_lookup table: append v0.11 entries
    (
        '        "hero_f1_valence":            ("chart_v10_valence_distribution.pdf",         "6_col_v10_valence"),\n'
        '        "hero_f2_h2_split":           ("chart_v10_h2_naive_caveated.pdf",            "6_col_v10_h2"),\n'
        '        "hero_f3_decoupling":         ("chart_v10_h3_decoupling.pdf",                "6_col_v10_h3"),\n'
        '    }',
        '        "hero_f1_valence":            ("chart_v10_valence_distribution.pdf",         "6_col_v10_valence"),\n'
        '        "hero_f2_h2_split":           ("chart_v10_h2_naive_caveated.pdf",            "6_col_v10_h2"),\n'
        '        "hero_f3_decoupling":         ("chart_v10_h3_decoupling.pdf",                "6_col_v10_h3"),\n'
        '        # v0.11 PM Software x Google Trends Construct Validity findings\n'
        '        "f1_scatter_t1":              ("chart_v11_h1_scatter_t1_6col.pdf",           "6_col_v11_scatter"),\n'
        '        "f2_scatter_t2":              ("chart_v11_h1_scatter_t2_6col.pdf",           "6_col_v11_scatter"),\n'
        '        "f3_rank_shift_t1":           ("chart_v11_h3_rank_shift_t1_6col.pdf",        "6_col_v11_rankshift"),\n'
        '        "f4_partial_residual_t1":     ("chart_v11_h4_partial_residual_t1_6col.pdf",  "6_col_v11_partial"),\n'
        '    }',
    ),

    # --- 8. Citation block in build_closing_story
    (
        '    citation_text = (\n'
        '        "Gonzalez Castro, P. U. (2026). "\n'
        '        "<i>Naive-Phantom Rate Longitudinal Stability: AI Presence Index v0.10 "\n'
        '        "\\u2014 Mint, designed-for-test extension</i>. "\n'
        '        "Third System. thirdsystem.ai/v10-naivephantom-stability"\n'
        '    )',
        '    citation_text = (\n'
        '        "Gonzalez Castro, P. U. (2026). "\n'
        '        "<i>PM Software \\u00d7 Google Trends Construct Validity: AI Presence Index "\n'
        '        "v0.11 \\u2014 Phase 3 pilot</i>. "\n'
        '        "Third System. thirdsystem.ai/v11-pm-trends-construct-validity"\n'
        '    )',
    ),

    # --- 9. build() docstring
    (
        '    Build the v0.10 Naive-Phantom Rate Stability report.',
        '    Build the v0.11 PM Software x Google Trends Construct Validity report.',
    ),

    # --- 10. print labels [build_report_v10] -> [build_report_v11]  (multiple occurrences — special-cased below)
    (
        '[build_report_v10]',
        '[build_report_v11]',
    ),

    # --- 11. Preconditions block: full replacement (was patches 11+12, merged)
    (
        '    # Preconditions\n'
        '    chart_dir = chart_dir or OUTPUT_DIR\n'
        '    output_path = output_path or (OUTPUT_DIR / "v10_naivephantom_stability.pdf")\n'
        '    base_pdf = OUTPUT_DIR / "_v10_base.pdf"\n'
        '    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)',
        '    # Preconditions — v0.11 deposits live under /v11/, not in reports/output.\n'
        '    # Default chart and report paths point at the deposit so the report sits\n'
        '    # with the data.\n'
        '    V11_DEPOSIT_ROOT = AIAS_ROOT / "osf" / "v11"\n'
        '    chart_dir = chart_dir or (V11_DEPOSIT_ROOT / "figures")\n'
        '    output_path = output_path or (V11_DEPOSIT_ROOT / "reports" / "v11_pmtrends_construct_validity.pdf")\n'
        '    base_pdf = output_path.parent / "_v11_base.pdf"\n'
        '    output_path.parent.mkdir(parents=True, exist_ok=True)',
    ),

    # --- 12. expected_slots list — v0.10 set → v0.11 set
    (
        '    expected_slots = [\n'
        '        "hero_f1_valence", "hero_f2_h2_split", "hero_f3_decoupling",\n'
        '    ]',
        '    expected_slots = [\n'
        '        "f1_scatter_t1", "f2_scatter_t2",\n'
        '        "f3_rank_shift_t1", "f4_partial_residual_t1",\n'
        '    ]',
    ),

    # --- 13. unused-charts pre-flight check — chart_v10 → chart_v11
    (
        'and p.name.startswith("chart_v10")',
        'and p.name.startswith("chart_v11")',
    ),
    (
        'print(f"[build_report_v11] chart files in dir not matched by any v10 slot:")',
        'print(f"[build_report_v11] chart files in dir not matched by any v11 slot:")',
    ),

    # --- 14. DocTemplate title
    (
        'title="Naive-Phantom Rate Stability \\u2014 AI Presence Index v0.10"',
        'title="PM Software \\u00d7 Google Trends Construct Validity \\u2014 AI Presence Index v0.11"',
    ),

    # --- 15. Page count target band note
    (
        '    # Page count check — v0.10 is narrower scope (3 findings) so target band\n'
        "    # is shorter than v0.9's 12-22.\n"
        '    final_pages = len(PdfReader(str(output_path)).pages)\n'
        '    print(f"[build_report_v11] page count: {final_pages}")\n'
        '    if final_pages < 8 or final_pages > 18:',
        '    # Page count check — v0.11 is single-category with 4 findings, similar\n'
        "    # to v0.10's scope plus one extra finding.\n"
        '    final_pages = len(PdfReader(str(output_path)).pages)\n'
        '    print(f"[build_report_v11] page count: {final_pages}")\n'
        '    if final_pages < 9 or final_pages > 20:',
    ),

    # --- 16. argparse --output default reference
    (
        'help="Output PDF path. Defaults to ./output/v10_naivephantom_stability.pdf")',
        'help="Output PDF path. Defaults to ~/aias/osf/v11/reports/v11_pmtrends_construct_validity.pdf")',
    ),
]

# Index of patch that intentionally has multiple occurrences (1-indexed).
MULTI_OCCURRENCE_OK = {10}

# ----------------------------------------------------------------------------
# Run patches
# ----------------------------------------------------------------------------

if not SRC.exists():
    sys.exit(f"ERROR: {SRC} does not exist. Did you cp build_report_v10.py to "
             f"build_report_v11.py first?")

text = SRC.read_text()

for i, (find, replace) in enumerate(PATCHES, 1):
    count = text.count(find)
    if count == 0:
        sys.exit(f"PATCH {i} FAILED: target string not found:\n{find[:200]}...")
    if count > 1 and i not in MULTI_OCCURRENCE_OK:
        sys.exit(f"PATCH {i} AMBIGUOUS: target string found {count} times; "
                 f"expected exactly 1. First 200 chars:\n{find[:200]}...")
    text = text.replace(find, replace)
    print(f"  patch {i:2d} applied  ({count} occurrence{'s' if count != 1 else ''})")

SRC.write_text(text)
print()
print(f"Wrote: {SRC}")
print(f"Run with: python ~/aias/reports/build_report_v11.py")
