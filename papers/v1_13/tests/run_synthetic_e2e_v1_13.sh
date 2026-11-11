#!/bin/zsh
# Synthetic end-to-end test of the v1.13 Grounding Paper A pipeline. SYNTHETIC DATA ONLY.
# Writes only under OUT (default /tmp/v113_pipeline_test/e2e); refuses a path inside the repository. Never touches
# osf/methodology/v1_13 (locked files, data or outputs), never opens osf/v42 (t4), and changes no tracked file; every
# PDF page and every chart is stamped "SYNTHETIC TEST — NOT RESULTS".
#
#   zsh papers/v1_13/tests/run_synthetic_e2e_v1_13.sh [OUT] [scenario ...]
#   scenarios: scored pass_reported downgraded downgraded_h6 c1_h4 fail marginal h3_undetermined dropped mq5 floor
#              interim (default: all)
#
# Steps: synthetic scorer outputs (make_scenarios_v1_13.py: the locked scorers' functions on synthetic inputs, 10,000
# permutations and 2,000 bootstrap draws) -> per scenario: charts -> paper fill -> pandoc build (watermarked) -> page
# PNGs; then the fill tests.
set -euo pipefail
WT=$(cd "$(dirname "$0")/../../.." && pwd)
OUT=${1:-/tmp/v113_pipeline_test/e2e}
shift || true
if (( $# )); then SCENS=("$@"); else
  SCENS=(scored pass_reported downgraded downgraded_h6 c1_h4 fail marginal h3_undetermined dropped mq5 floor interim); fi
W="SYNTHETIC TEST — NOT RESULTS"
mkdir -p "$(dirname "$OUT")"
case "$(cd "$(dirname "$OUT")" && pwd)/$(basename "$OUT")" in
  "$WT"*) echo "REFUSED: $OUT is inside the repository"; exit 2;;
esac
rm -rf "$OUT"; mkdir -p "$OUT"
cd "$WT"
export PYTHONDONTWRITEBYTECODE=1
echo "== 1 synthetic scorer outputs"
python3 papers/v1_13/tests/make_scenarios_v1_13.py "$OUT/synth" $SCENS
for S in $SCENS; do
  V="$OUT/synth/SYNTHETIC_${S}_v1_13_verdicts.json"; SD="$OUT/synth/SYNTHETIC_${S}_v1_13_sdri.csv"
  SDA=(); [[ -f "$SD" ]] && SDA=(--sdri "$SD")
  D="$OUT/$S"
  echo "== $S: charts, fill, build"
  python3 scripts/build_charts_v113.py --verdicts "$V" $SDA --out "$D/figs" --watermark "$W" | tail -1
  python3 papers/v1_13/fill_paper_v1_13.py --synthetic --verdicts "$V" $SDA --fig-dir "$D/figs" \
      --out "$D/paper/v1_13_paper_draft.md" | cut -c1-160
  python3 scripts/build_paper_v1_13.py --source "$D/paper/v1_13_paper_draft.md" \
      --output "$D/paper/v1_13_paper.pdf" --watermark "$W" | tail -2
  mkdir -p "$D/png"; pdftoppm -r 80 -png "$D/paper/v1_13_paper.pdf" "$D/png/paper"
  echo "   pages: $(pdfinfo "$D/paper/v1_13_paper.pdf" | awk '/^Pages/ {print $2}')"
done
echo "== fill tests"
python3 papers/v1_13/tests/test_fill_paper_v1_13.py 2>&1 | tail -3
echo "tracked files changed by this run: $(git status --porcelain --untracked-files=no | wc -l | tr -d ' ')"
echo "PNG pages for the visual pre-flight: $OUT/<scenario>/png/"
