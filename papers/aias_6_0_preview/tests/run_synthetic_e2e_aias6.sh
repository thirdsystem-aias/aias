#!/bin/zsh
# Synthetic end-to-end test of the AIAS 6.0 Preview paper pipeline. SYNTHETIC DATA ONLY.
# Writes only under OUT (default /tmp/aias6_pipeline_test/e2e); refuses a path inside the repository. Every PDF page and
# every chart is stamped "SYNTHETIC TEST — NOT RESULTS".
#
#   zsh papers/aias_6_0_preview/tests/run_synthetic_e2e_aias6.sh [OUT] [--regenerate] [scenario ...]
#
# Default: the committed fixtures (tests/fixtures/<scenario>/, the locked scorer's outputs on its own synthetic test
# repository). --regenerate first rebuilds them into OUT/synth with make_scenarios_aias6.py (about 75 s).
# Per scenario: charts -> paper fill (class C with --class-c-draft) -> pandoc build (watermarked) -> page PNGs
# (pdftoppm -r 100); then the tests.
set -euo pipefail
WT=$(cd "$(dirname "$0")/../../.." && pwd)
OUT=${1:-/tmp/aias6_pipeline_test/e2e}
shift || true
SRC="$WT/papers/aias_6_0_preview/tests/fixtures"
if [[ "${1:-}" == "--regenerate" ]]; then REGEN=1; shift; else REGEN=0; fi
W="SYNTHETIC TEST — NOT RESULTS"
case "$(cd "$(dirname "$OUT")" 2>/dev/null && pwd)/$(basename "$OUT")" in
  "$WT"*) echo "REFUSED: $OUT is inside the repository"; exit 2;;
esac
rm -rf "$OUT"; mkdir -p "$OUT"
cd "$WT"
export PYTHONDONTWRITEBYTECODE=1
if (( REGEN )); then
  echo "-- synthetic scorer outputs (regenerated)"
  python3 papers/aias_6_0_preview/tests/make_scenarios_aias6.py "$OUT/synth" "$@"
  SRC="$OUT/synth"
fi
if (( $# )); then SCENS=("$@"); else SCENS=($(ls "$SRC")); fi
for S in $SCENS; do
  D="$OUT/$S"
  echo "-- $S"
  python3 scripts/build_charts_aias6.py --outputs "$SRC/$S" --out "$D/figs" --watermark "$W" | tail -1
  python3 papers/aias_6_0_preview/fill_paper_aias6.py --synthetic --class-c-draft --outputs "$SRC/$S" \
      --fig-dir "$D/figs" --out "$D/paper/aias_6_0_preview_paper_draft.md" | cut -c1-140
  python3 scripts/build_paper_aias6.py --source "$D/paper/aias_6_0_preview_paper_draft.md" \
      --output "$D/paper/aias_6_0_preview_paper.pdf" --watermark "$W" | grep -E "Built|WARNING|ERROR|Error" || true
  mkdir -p "$D/png"; pdftoppm -r 100 -png "$D/paper/aias_6_0_preview_paper.pdf" "$D/png/p"
  echo "   pages: $(pdfinfo "$D/paper/aias_6_0_preview_paper.pdf" | awk '/^Pages/ {print $2}')"
done
echo "-- tests"
python3 papers/aias_6_0_preview/tests/test_fill_paper_aias6.py 2>&1 | tail -3
echo "tracked files changed by this run: $(git status --porcelain --untracked-files=no | wc -l | tr -d ' ')"
