#!/bin/bash
# assemble_v18_osf_deposit.sh
#
# Assembles the v0.18 OSF deposit at osf/v18/ by copying files from the
# working repo into the deposit folder structure. Idempotent — running
# again just overwrites with current state.
#
# After running this, the osf/v18/ folder is ready to upload via either:
#   1. osf_upload.py (programmatic, requires OSF_TOKEN env var)
#   2. OSF web UI drag-and-drop (manual fallback)
#
# Run from project root:
#   cd ~/aias
#   bash assemble_v18_osf_deposit.sh

set -e

DEPOSIT=osf/v18
echo "[assemble] Building $DEPOSIT/"

# ---------------------------------------------------------------------------
# Create directory structure
# ---------------------------------------------------------------------------
mkdir -p $DEPOSIT/data/verdicts
mkdir -p $DEPOSIT/figures
mkdir -p $DEPOSIT/scripts/protocol
mkdir -p $DEPOSIT/reports

# ---------------------------------------------------------------------------
# Top-level documents (README, MANIFEST already created by Claude;
# PRE_REGISTRATION and DEVIATIONS already in place)
# ---------------------------------------------------------------------------
# README.md and MANIFEST.md are copied separately from Downloads (below)
# PRE_REGISTRATION_v0_18.md and DEVIATIONS.md are already at osf/v18/
echo "[assemble] Top-level: PRE_REGISTRATION_v0_18.md, DEVIATIONS.md (already in place)"

# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------
cp data/phase_a/v0.18/phase_a_results.json    $DEPOSIT/data/phase_a_results.json
cp data/phase_b/v0.18/phase_b_results.json    $DEPOSIT/data/phase_b_results.json
cp data/verdicts/v0_18_verdict.json           $DEPOSIT/data/verdicts/v0_18_verdict.json
cp data/verdicts/v0_18_verdict.md             $DEPOSIT/data/verdicts/v0_18_verdict.md
echo "[assemble] Data: 4 files copied"

# ---------------------------------------------------------------------------
# Figures
# ---------------------------------------------------------------------------
cp reports/figs/v18/chart_01_mention_rate_distribution.pdf  $DEPOSIT/figures/
cp reports/figs/v18/chart_02_cell_attrition.pdf             $DEPOSIT/figures/
cp reports/figs/v18/chart_03_dissociation_scatter.pdf       $DEPOSIT/figures/
echo "[assemble] Figures: 3 PDFs copied"

# ---------------------------------------------------------------------------
# Scripts (acquisition, scoring, charts)
# ---------------------------------------------------------------------------
cp scripts/_path.py                  $DEPOSIT/scripts/_path.py
cp scripts/acquire_phase_a_v18.py    $DEPOSIT/scripts/acquire_phase_a_v18.py
cp scripts/acquire_phase_b_v18.py    $DEPOSIT/scripts/acquire_phase_b_v18.py
cp scripts/score_v18.py              $DEPOSIT/scripts/score_v18.py
cp scripts/build_charts_v18.py       $DEPOSIT/scripts/build_charts_v18.py
echo "[assemble] Scripts: 5 files copied"

# ---------------------------------------------------------------------------
# Protocol package (canonical v1.4 implementation)
# ---------------------------------------------------------------------------
cp protocol/__init__.py     $DEPOSIT/scripts/protocol/__init__.py
cp protocol/thresholds.py   $DEPOSIT/scripts/protocol/thresholds.py
cp protocol/providers.py    $DEPOSIT/scripts/protocol/providers.py
cp protocol/probe.py        $DEPOSIT/scripts/protocol/probe.py
cp protocol/parse.py        $DEPOSIT/scripts/protocol/parse.py
echo "[assemble] Protocol package: 5 files copied"

# ---------------------------------------------------------------------------
# Reports (brand-format PDF + build pipeline)
# ---------------------------------------------------------------------------
cp osf/v18/reports/v18_indie_fragrance.pdf  $DEPOSIT/reports/v18_indie_fragrance.pdf
cp reports/build_report_v18.py              $DEPOSIT/reports/build_report_v18.py
cp reports/v18_indie_fragrance_content.py   $DEPOSIT/reports/v18_indie_fragrance_content.py
echo "[assemble] Reports: 3 files copied"

# ---------------------------------------------------------------------------
# Verification
# ---------------------------------------------------------------------------
echo ""
echo "[assemble] Deposit assembled. Inventory:"
find $DEPOSIT -type f \( -name "*.md" -o -name "*.json" -o -name "*.py" -o -name "*.pdf" \) \
    | sort

echo ""
echo "[assemble] File counts by directory:"
find $DEPOSIT -type d | while read d; do
    count=$(find "$d" -maxdepth 1 -type f | wc -l | tr -d ' ')
    echo "  $d: $count files"
done

echo ""
echo "[assemble] Done. Next steps:"
echo "  1. Review: open $DEPOSIT/"
echo "  2. Upload via OSF API: python scripts/osf_upload.py --phase v18"
echo "  3. Or upload via web: open https://osf.io/ec6wh/files/"
