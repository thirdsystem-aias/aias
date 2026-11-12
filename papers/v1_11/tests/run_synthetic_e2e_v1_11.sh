#!/bin/zsh
# Synthetic end-to-end test of the v1.11 Sentiment Paper A pipeline. SYNTHETIC DATA ONLY.
# Writes only under OUT (default /tmp/v111_pipeline_test/e2e); refuses a path inside the repository. Never touches
# osf/methodology/v1_11 (data, outputs or locked files) or any tracked file; every PDF page and every chart is
# stamped "SYNTHETIC TEST — NOT RESULTS".
#
#   zsh papers/v1_11/tests/run_synthetic_e2e_v1_11.sh [OUT] [scenario ...]
#   scenarios: scored confirmed h1_falsified unstable marginal mixed presence undetermined inactive (default: all)
#
# Steps: synthetic scorer outputs (make_scenarios_v1_11.py: the scorer's own dry-run Stage J/C outputs, plus scenarios
# whose verdict words are recomputed with the locked scorer's functions) -> per scenario: charts -> paper fill ->
# pandoc build (watermarked) -> page PNGs (pdftoppm -r 100); then the fill tests.
set -euo pipefail
WT=$(cd "$(dirname "$0")/../../.." && pwd)
OUT=${1:-/tmp/v111_pipeline_test/e2e}
shift || true
if (( $# )); then SCENS=("$@"); else SCENS=(scored confirmed h1_falsified unstable marginal mixed presence undetermined inactive); fi
W="SYNTHETIC TEST — NOT RESULTS"
case "$(cd "$(dirname "$OUT")" 2>/dev/null && pwd)/$(basename "$OUT")" in
  "$WT"*) echo "REFUSED: $OUT is inside the repository"; exit 2;;
esac
rm -rf "$OUT"; mkdir -p "$OUT"
cd "$WT"
export PYTHONDONTWRITEBYTECODE=1
echo "-- 1 synthetic scorer outputs"
python3 papers/v1_11/tests/make_scenarios_v1_11.py "$OUT/synth" $SCENS
for S in $SCENS; do
  D="$OUT/$S"
  echo "-- $S: charts, fill, build"
  python3 scripts/build_charts_v111.py --outputs "$OUT/synth/$S" --out "$D/figs" --watermark "$W" | tail -1
  python3 papers/v1_11/fill_paper_v1_11.py --synthetic --outputs "$OUT/synth/$S" --fig-dir "$D/figs" \
      --out "$D/paper/v1_11_paper_draft.md" | cut -c1-160
  python3 scripts/build_paper_v1_11.py --source "$D/paper/v1_11_paper_draft.md" \
      --output "$D/paper/v1_11_paper.pdf" --watermark "$W" | tail -2
  mkdir -p "$D/png"; pdftoppm -r 100 -png "$D/paper/v1_11_paper.pdf" "$D/png/paper"
  echo "   pages: $(pdfinfo "$D/paper/v1_11_paper.pdf" | awk '/^Pages/ {print $2}')"
done
echo "-- fill tests"
python3 papers/v1_11/tests/test_fill_paper_v1_11.py 2>&1 | tail -3
echo "tracked files changed by this run: $(git status --porcelain --untracked-files=no | wc -l | tr -d ' ')"
echo "PNG pages for the visual pre-flight: $OUT/<scenario>/png/"
