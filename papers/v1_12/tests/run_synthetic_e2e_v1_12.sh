#!/bin/zsh
# Synthetic end-to-end test of the v1.12 Coverage Paper A pipeline. SYNTHETIC DATA ONLY.
# Writes only under OUT (default /tmp/v112_pipeline_test/e2e); refuses a path inside the repository. Never touches
# osf/methodology/v1_12 (data, outputs or locked files) or any tracked file; every PDF page and every chart is
# stamped "SYNTHETIC TEST — NOT RESULTS".
#
#   zsh papers/v1_12/tests/run_synthetic_e2e_v1_12.sh [OUT] [scenario ...]
#   scenarios: scored pass fail marginal downgraded undetermined instrument fallback (default: all)
#
# Steps: synthetic scorer outputs (make_scenarios_v1_12.py: the locked scorer's score_coverage on synthetic inputs,
# full 10,000 draws, plus scenarios derived with the scorer's own verdict functions and gate) -> per scenario: charts
# -> paper fill -> pandoc build (watermarked) -> SSRN packet hook -> page PNGs; then the fill tests.
set -euo pipefail
WT=$(cd "$(dirname "$0")/../../.." && pwd)
OUT=${1:-/tmp/v112_pipeline_test/e2e}
shift || true
if (( $# )); then SCENS=("$@"); else SCENS=(scored pass fail marginal downgraded undetermined instrument fallback); fi
W="SYNTHETIC TEST — NOT RESULTS"
case "$(cd "$(dirname "$OUT")" 2>/dev/null && pwd)/$(basename "$OUT")" in
  "$WT"*) echo "REFUSED: $OUT is inside the repository"; exit 2;;
esac
rm -rf "$OUT"; mkdir -p "$OUT"
cd "$WT"
export PYTHONDONTWRITEBYTECODE=1
echo "== 1 synthetic scorer outputs"
python3 papers/v1_12/tests/make_scenarios_v1_12.py "$OUT/synth" --draws 10000 $SCENS
for S in $SCENS; do
  V="$OUT/synth/SYNTHETIC_${S}_v112_verdicts.json"; T="$OUT/synth/SYNTHETIC_${S}_v112_unit_table.csv"
  D="$OUT/$S"
  echo "== $S: charts, fill, build, packet"
  python3 scripts/build_charts_v112.py --verdicts "$V" --table "$T" --out "$D/figs" --watermark "$W" | tail -1
  python3 papers/v1_12/fill_paper_v1_12.py --synthetic --verdicts "$V" --table "$T" --fig-dir "$D/figs" \
      --out "$D/paper/v1_12_ssrn_paper_draft.md" | cut -c1-160
  python3 scripts/build_paper_v1_12.py --source "$D/paper/v1_12_ssrn_paper_draft.md" \
      --output "$D/paper/v1_12_ssrn_paper.pdf" --watermark "$W" | tail -2
  python3 papers/v1_12/ssrn_packet_hook_v1_12.py --paper "$D/paper/v1_12_ssrn_paper_draft.md" \
      --output "$D/paper/ssrn_submission_packet_v1_12.md" | tail -1
  mkdir -p "$D/png"; pdftoppm -r 80 -png "$D/paper/v1_12_ssrn_paper.pdf" "$D/png/paper"
  echo "   pages: $(pdfinfo "$D/paper/v1_12_ssrn_paper.pdf" | awk '/^Pages/ {print $2}')"
done
echo "== fill tests"
python3 papers/v1_12/tests/test_fill_paper_v1_12.py 2>&1 | tail -3
echo "tracked files changed by this run: $(git status --porcelain --untracked-files=no | wc -l | tr -d ' ')"
echo "PNG pages for the visual pre-flight: $OUT/<scenario>/png/"
