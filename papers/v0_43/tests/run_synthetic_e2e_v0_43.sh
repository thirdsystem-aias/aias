#!/bin/zsh
# Synthetic end-to-end test of the v0.43 Stage 1 paper pipeline. SYNTHETIC DATA ONLY.
# Writes only under OUT (default /tmp/v043_pipeline_test/e2e); refuses a path inside the repository. Never touches
# osf/v43 (data, outputs or locked files) or any tracked file; every PDF page and every chart is stamped
# "SYNTHETIC TEST — NOT RESULTS".
#
#   zsh papers/v0_43/tests/run_synthetic_e2e_v0_43.sh [OUT] [scenario ...]
#   scenarios: lead lag null marginal sparse (default: all)
#
# Steps: synthetic scorer outputs (make_scenarios_v0_43.py: invented units and synthetic Trends responses in a scratch
# root under OUT, scored by the locked score_v0_43.score() with 10,000 draws) -> per scenario: charts -> paper fill ->
# pandoc build (watermarked) -> page PNGs; then the fill tests.
set -euo pipefail
WT=$(cd "$(dirname "$0")/../../.." && pwd)
OUT=${1:-/tmp/v043_pipeline_test/e2e}
shift || true
if (( $# )); then SCENS=("$@"); else SCENS=(lead lag null marginal sparse); fi
W="SYNTHETIC TEST — NOT RESULTS"
mkdir -p "$(dirname "$OUT")"
case "$(cd "$(dirname "$OUT")" && pwd -P)/$(basename "$OUT")" in
  "$(cd "$WT" && pwd -P)"*) echo "REFUSED: $OUT is inside the repository"; exit 2;;
esac
rm -rf "$OUT"; mkdir -p "$OUT"
cd "$WT"
export PYTHONDONTWRITEBYTECODE=1
echo "== 1 synthetic scorer outputs (locked scorer, 10,000 draws)"
python3 papers/v0_43/tests/make_scenarios_v0_43.py "$OUT/synth" --draws 10000 $SCENS
for S in $SCENS; do
  V="$OUT/synth/SYNTHETIC_${S}_v43_stage1_verdicts.json"; P="$OUT/synth/SYNTHETIC_${S}_v43_pulls.json"
  D="$OUT/$S"
  echo "== $S: charts, fill, build"
  python3 scripts/build_charts_v043.py --verdicts "$V" --out "$D/figs" --watermark "$W" | tail -1
  python3 papers/v0_43/fill_paper_v0_43.py --synthetic --verdicts "$V" --pulls "$P" --fig-dir "$D/figs" \
      --out "$D/paper/v0_43_paper_draft.md" | cut -c1-220
  python3 scripts/build_paper_v0_43.py --source "$D/paper/v0_43_paper_draft.md" \
      --output "$D/paper/v0_43_paper.pdf" --watermark "$W" | tail -2
  mkdir -p "$D/png"; pdftoppm -r 80 -png "$D/paper/v0_43_paper.pdf" "$D/png/paper"
  echo "   pages: $(pdfinfo "$D/paper/v0_43_paper.pdf" | awk '/^Pages/ {print $2}')"
done
echo "== fill tests"
python3 papers/v0_43/tests/test_fill_paper_v0_43.py 2>&1 | tail -3
echo "tracked files changed by this run: $(git status --porcelain --untracked-files=no | wc -l | tr -d ' ')"
echo "PNG pages for the visual pre-flight: $OUT/<scenario>/png/"
