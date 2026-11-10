#!/bin/zsh
# Synthetic end-to-end test of the v0.42 (t4) paper and report pipeline. SYNTHETIC DATA ONLY.
# Writes only under OUT (default /tmp/t4_pipeline_test/e2e); refuses a path inside the repository. Never touches
# osf/v42/data, the locked files or any tracked file; every PDF page is stamped "SYNTHETIC TEST — NOT RESULTS".
#
#   zsh papers/v0_42/tests/run_synthetic_e2e_v0_42.sh [OUT] [scenario: noisy|copy]
#
# Steps: synthetic t4 raw + coded tables (make_scenarios_v0_42.py, real formats) -> the real scorer in its synthetic
# mode (score_v0_42.py --synthetic, full 10,000 draws) -> charts -> paper fill -> pandoc build -> SSRN packet hook ->
# report build -> page PNGs for the visual pre-flight -> fill tests.
set -euo pipefail
WT=$(cd "$(dirname "$0")/../../.." && pwd)
OUT=${1:-/tmp/t4_pipeline_test/e2e}
SCEN=${2:-noisy}
W="SYNTHETIC TEST — NOT RESULTS"
case "$(cd "$(dirname "$OUT")" 2>/dev/null && pwd)/$(basename "$OUT")" in
  "$WT"*) echo "REFUSED: $OUT is inside the repository"; exit 2;;
esac
rm -rf "$OUT"; mkdir -p "$OUT"
cd "$WT"
export PYTHONDONTWRITEBYTECODE=1
S="$OUT/synth/$SCEN/_score"
echo "== 1/8 synthetic data ($SCEN)";   python3 papers/v0_42/tests/make_scenarios_v0_42.py "$OUT/synth" "$SCEN"
echo "== 2/8 scorer (synthetic mode)";  python3 osf/v42/scripts/score_v0_42.py --synthetic "$OUT/synth/$SCEN"
echo "== 3/8 charts";                   python3 scripts/build_charts_v42.py --verdicts "$S/v42_verdicts.json" \
                                          --table "$S/v42_brand_table.csv" --out "$OUT/figs" \
                                          --report-out "$OUT/figs/report" --watermark "$W" | tail -1
echo "== 4/8 paper fill";               python3 papers/v0_42/fill_paper_v0_42.py --synthetic \
                                          --verdicts "$S/v42_verdicts.json" --table "$S/v42_brand_table.csv" \
                                          --fig-dir "$OUT/figs" --out "$OUT/paper/v0_42_ssrn_paper_draft.md"
echo "== 5/8 paper build";              python3 scripts/build_paper_v0_42.py --source "$OUT/paper/v0_42_ssrn_paper_draft.md" \
                                          --output "$OUT/paper/v0_42_ssrn_paper.pdf" --watermark "$W"
echo "== 6/8 SSRN packet hook";         python3 papers/v0_42/ssrn_packet_hook_v0_42.py \
                                          --paper "$OUT/paper/v0_42_ssrn_paper_draft.md" \
                                          --output "$OUT/paper/ssrn_submission_packet_v0_42.md"
echo "== 7/8 report build";             python3 reports/build_report_v42.py --verdicts "$S/v42_verdicts.json" \
                                          --chart-dir "$OUT/figs/report" \
                                          --output "$OUT/report/v42_t4_generation_report.pdf" --watermark "$W" \
                                          | grep -E "page count|watermark|MISSING" || true
echo "== 8/8 page images + fill tests"
mkdir -p "$OUT/png"
pdftoppm -r 80 -png "$OUT/paper/v0_42_ssrn_paper.pdf" "$OUT/png/paper"
pdftoppm -r 80 -png "$OUT/report/v42_t4_generation_report.pdf" "$OUT/png/report"
python3 papers/v0_42/tests/test_fill_paper_v0_42.py 2>&1 | tail -3
echo "paper pages:  $(pdfinfo "$OUT/paper/v0_42_ssrn_paper.pdf" | awk '/^Pages/ {print $2}')"
echo "report pages: $(pdfinfo "$OUT/report/v42_t4_generation_report.pdf" | awk '/^Pages/ {print $2}')"
echo "tracked files changed by this run: $(git status --porcelain --untracked-files=no | wc -l | tr -d ' ')"
echo "PNG pages for the visual pre-flight: $OUT/png/"
