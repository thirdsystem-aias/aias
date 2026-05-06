#!/bin/bash
# ====================================================================
# AIAS folder cleanup — pre-v0.8 reorganization
# Author: Pablo Ulpiano González Castro (with Claude)
# Date: 2026-05-05
# Purpose: organize /aias before v0.8 knives measurement; eliminate
#          the brands.json/prompts.json overwrite trap; archive supersedes.
#
# Rollback: tar snapshot is created in Phase 0. To revert:
#   cd ~ && rm -rf aias && tar -xzf aias_pre_cleanup_<timestamp>.tar.gz
#
# Runs from ~/aias. set -e exits on first error.
# Review each phase before running, or run section-by-section by
# commenting out the function calls at the bottom.
# ====================================================================

set -e
cd "$HOME/aias"

# --------------------------------------------------------------------
# Phase 0 — Snapshot insurance
# --------------------------------------------------------------------
phase_0_snapshot() {
  echo "[Phase 0] Creating safety snapshot..."
  cd "$HOME"
  local stamp
  stamp=$(date +%Y%m%d_%H%M%S)
  tar -czf "aias_pre_cleanup_${stamp}.tar.gz" \
    --exclude='aias/venv' \
    --exclude='aias/__pycache__' \
    --exclude='aias/.git' \
    aias/
  echo "  Snapshot: ~/aias_pre_cleanup_${stamp}.tar.gz"
  cd "$HOME/aias"
}

# --------------------------------------------------------------------
# Phase 1 — Build folder skeleton (additive, zero risk)
# --------------------------------------------------------------------
phase_1_skeleton() {
  echo "[Phase 1] Creating new folder structure..."
  mkdir -p registries prompts
  mkdir -p data/{pm,running,oliveoil,skincare,finance,household,knives}
  mkdir -p data/oliveoil/_pre_revision
  mkdir -p data/skincare/_pre_revision
  mkdir -p data/household/logs
  mkdir -p pre_registration protocol
  mkdir -p archive/{old_reports,old_scripts,old_protocols,old_data,misc}
  echo "  Done."
}

# --------------------------------------------------------------------
# Phase 2 — Promote canonical docs
# --------------------------------------------------------------------
phase_2_promote() {
  echo "[Phase 2] Promoting canonical docs..."
  cp "research log after v0.7/MEASUREMENT_PROTOCOL_v1_1.md" protocol/

  # Diff RESEARCH_LOG before overwriting — manual decision
  if [[ -f "research log after v0.7/RESEARCH_LOG.md" ]]; then
    if ! diff -q RESEARCH_LOG.md "research log after v0.7/RESEARCH_LOG.md" > /dev/null 2>&1; then
      echo "  ⚠ RESEARCH_LOG.md at root DIFFERS from version inside 'research log after v0.7/'"
      echo "  ⚠ Manually merge or pick one before deleting either."
      echo "  ⚠ For now, keeping both — root version untouched."
    else
      echo "  RESEARCH_LOG.md identical in both locations."
    fi
  fi

  cp PRE_REGISTRATION_household_v1.0.md pre_registration/
  echo "  Done."
}

# --------------------------------------------------------------------
# Phase 3 — Per-category brands/prompts (the overwrite fix)
# --------------------------------------------------------------------
phase_3_registries() {
  echo "[Phase 3] Splitting brands/prompts by category..."

  # Root brands.json/prompts.json = household_goods_retail (verified)
  cp brands.json   registries/brands_household.json
  cp prompts.json  prompts/prompts_household.json

  # PM software (v0.6 inaugural) preserved in backup/
  cp backup/brands.json   registries/brands_pm.json
  cp backup/prompts.json  prompts/prompts_pm.json

  echo "  ✓ household + pm restored from working/backup."
  echo ""
  echo "  ⚠ MANUAL STEP REQUIRED:"
  echo "  ⚠ Restore from iCloud snapshots:"
  echo "  ⚠   registries/brands_running.json    (29 April 21:03)"
  echo "  ⚠   registries/brands_oliveoil.json   (30 April 09:01, 20-brand post-revision)"
  echo "  ⚠   registries/brands_skincare.json   (30 April evening, never preserved — reconstruct from §B.4)"
  echo "  ⚠   registries/brands_finance.json    (30 April evening, live file at root pre-cleanup if any)"
  echo "  ⚠   prompts/prompts_running.json      (29 April 20:38)"
  echo "  ⚠   prompts/prompts_oliveoil.json     (30 April 08:33)"
  echo "  ⚠   prompts/prompts_skincare.json     (reconstruct from §A.4)"
  echo "  ⚠   prompts/prompts_finance.json      (30 April evening)"
}

# --------------------------------------------------------------------
# Phase 4 — Sort CSVs into per-category data folders (cp, not mv)
# --------------------------------------------------------------------
phase_4_sort_csvs() {
  echo "[Phase 4] Sorting CSVs into data/<category>/ ..."

  # PM software (29 April evening, post-revision)
  cp results_v2_20260429_181007.csv         data/pm/
  cp results_enriched_20260429_181355.csv    data/pm/
  cp presence_index_v0.3_20260429_181355.csv data/pm/

  # Running shoes (29 April evening, no revision)
  cp results_v2_20260429_205023.csv         data/running/
  cp results_enriched_20260429_205407.csv    data/running/
  cp presence_index_v0.3_20260429_205407.csv data/running/

  # Olive oil — first run (16-brand registry, pre-revision)
  cp results_v2_20260430_085246.csv         data/oliveoil/_pre_revision/
  cp results_enriched_20260430_085800.csv    data/oliveoil/_pre_revision/
  cp presence_index_v0.3_20260430_085800.csv data/oliveoil/_pre_revision/

  # Olive oil — post-revision (20-brand registry, CANONICAL)
  cp results_v2_20260430_091539.csv         data/oliveoil/
  cp results_enriched_20260430_092033.csv    data/oliveoil/
  cp presence_index_v0.3_20260430_092033.csv data/oliveoil/

  # Skincare — TWO RUNS, canonical TBD by Pablo
  # 17:35 timestamp run
  cp results_v2_20260430_173125.csv         data/skincare/_pre_revision/
  cp results_enriched_20260430_173546.csv    data/skincare/_pre_revision/
  cp presence_index_v0.3_20260430_173546.csv data/skincare/_pre_revision/
  # 17:55 timestamp run (assumed canonical post-revision)
  cp results_v2_20260430_175139.csv         data/skincare/
  cp results_enriched_20260430_175546.csv    data/skincare/
  cp presence_index_v0.3_20260430_175546.csv data/skincare/

  # Personal finance (30 April evening)
  cp results_v2_20260430_181613.csv         data/finance/
  cp results_enriched_20260430_182025.csv    data/finance/
  cp presence_index_v0.3_20260430_182025.csv data/finance/

  # Household BBB v0.7 (4 May)
  cp results_v2_20260504_132404.csv                       data/household/
  cp results_v2_20260504_132404_rerun_google.csv          data/household/
  cp results_v2_20260504_132404_rerun_no_google.csv       data/household/
  cp results_v2_household_v1.0_final.csv                  data/household/
  cp results_v2_household_v1.0_merged.csv                 data/household/
  cp results_enriched_household_v1.0_20260504_162106.csv  data/household/
  cp presence_index_v0.3_household_v1.0_20260504_162106.csv data/household/
  cp manual_review_bbb_20260504_170819.csv                data/household/
  cp manual_review_bbb_checkpoint.csv                     data/household/
  cp spot_check_audit_20260504_171624.csv                 data/household/
  cp cross_tab_valence_20260504_171229.csv                data/household/
  cp spot_check_summary_household_v1.0.txt                data/household/

  # Household logs
  cp analyze_household_v1.0.log     data/household/logs/
  cp extraction_household_v1.0.log  data/household/logs/
  cp manual_review_bbb.log          data/household/logs/
  cp run_household_v1.0.log         data/household/logs/
  cp rerun_household_v1.0.log       data/household/logs/
  cp rerun_google.log               data/household/logs/
  cp rerun_no_google.log            data/household/logs/
  cp spot_check_audit.log           data/household/logs/
  cp cross_tab_valence.log          data/household/logs/

  # v0.1 / v0.2 era PM software runs (pre-published-data, methodologically interesting)
  mv leaderboard_20260429_105403.csv          archive/old_data/
  mv results_20260429_105403.csv              archive/old_data/
  mv leaderboard_v2_20260429_172238.csv       archive/old_data/
  mv results_enriched_20260429_172238.csv     archive/old_data/

  echo "  ✓ CSVs copied to data/<category>/ (root copies kept until you verify)"
}

# --------------------------------------------------------------------
# Phase 5 — Archive superseded files
# --------------------------------------------------------------------
phase_5_archive() {
  echo "[Phase 5] Archiving superseded files..."

  # Old protocols
  mv MEASUREMENT_PROTOCOL_v1_0_FINAL.md  archive/old_protocols/ 2>/dev/null || true
  mv MEASUREMENT_PROTOCOL_v1.0_FINAL.md  archive/old_protocols/ 2>/dev/null || true
  mv methodology.md                       archive/old_protocols/ 2>/dev/null || true

  # Old reports + root-level chart PDFs
  mv report_v0.3.md            archive/old_reports/ 2>/dev/null || true
  mv report_v0.3.pdf           archive/old_reports/ 2>/dev/null || true
  mv report_v0.3_cross.md      archive/old_reports/ 2>/dev/null || true
  mv report_v0.3_cross.pdf     archive/old_reports/ 2>/dev/null || true
  mv report_v0.4_cross.md      archive/old_reports/ 2>/dev/null || true
  mv report_v0.4_cross.pdf     archive/old_reports/ 2>/dev/null || true
  mv report_v0.6_cross.md      archive/old_reports/ 2>/dev/null || true
  mv report_v0.6_cross.pdf     archive/old_reports/ 2>/dev/null || true
  mv chart_aggregate_matrix.pdf       archive/old_reports/ 2>/dev/null || true
  mv chart_cep_comparison.pdf         archive/old_reports/ 2>/dev/null || true
  mv chart_cep_heatmap.pdf            archive/old_reports/ 2>/dev/null || true
  mv chart_leaderboards_side_by_side.pdf archive/old_reports/ 2>/dev/null || true
  mv chart_leaderboards.pdf           archive/old_reports/ 2>/dev/null || true
  mv chart_p1_coherence_variance.pdf  archive/old_reports/ 2>/dev/null || true
  mv chart_p2_comparison_discovery.pdf archive/old_reports/ 2>/dev/null || true
  mv chart_p3_awareness_divergence.pdf archive/old_reports/ 2>/dev/null || true
  mv chart_p4_country_origin.pdf      archive/old_reports/ 2>/dev/null || true
  mv chart_p6_phantom_mint.pdf        archive/old_reports/ 2>/dev/null || true
  mv chart_per_model_variance.pdf     archive/old_reports/ 2>/dev/null || true
  mv v06_source_text.md               archive/old_reports/ 2>/dev/null || true

  # Old scripts (canonical: run_aias_v2.py + analyze_v3.py + extractor.py)
  mv analyze.py     archive/old_scripts/ 2>/dev/null || true
  mv analyze_v2.py  archive/old_scripts/ 2>/dev/null || true
  mv run_aias.py    archive/old_scripts/ 2>/dev/null || true

  # Misc
  mv "AIAS Phase 2 — Pre-registration- Household Goods Retail (Pattern 6 : Phantom-Brand Persistence).rtf" archive/misc/ 2>/dev/null || true
  mv build_report.sh archive/misc/ 2>/dev/null || true   # stale launcher; reports/build_report*.py is canonical

  # The orphan latex file — kept in misc until you decide
  mv thirdsystem.tex archive/misc/ 2>/dev/null || true

  # Stray root-level third_system_brand.json (canonical lives in brand/)
  if [[ -f third_system_brand.json && -f brand/third_system_brand.json ]]; then
    if diff -q third_system_brand.json brand/third_system_brand.json > /dev/null 2>&1; then
      rm third_system_brand.json
      echo "  ✓ Removed duplicate third_system_brand.json (identical to brand/ copy)"
    else
      mv third_system_brand.json archive/misc/third_system_brand_root_copy.json
      echo "  ⚠ Root third_system_brand.json DIFFERS from brand/ — moved to archive/misc/ for review"
    fi
  fi

  echo "  ✓ Archived."
}

# --------------------------------------------------------------------
# Phase 6 — Junk removal
# --------------------------------------------------------------------
phase_6_junk() {
  echo "[Phase 6] Removing junk..."
  rm -f _test_write.txt
  rm -f hello_world.py
  rm -f test_extractor.py
  rm -f files.zip
  rm -f "research log after v0.7.zip"
  # The unzipped folder contents already promoted in Phase 2
  rm -rf "research log after v0.7"
  # macOS detritus (skip venv/.git)
  find . -name '.DS_Store' \
    -not -path './venv/*' \
    -not -path './.git/*' \
    -delete 2>/dev/null || true
  echo "  ✓ Junk removed."
}

# --------------------------------------------------------------------
# Phase 7 — Verification
# --------------------------------------------------------------------
phase_7_verify() {
  echo "[Phase 7] Verification..."
  echo ""
  echo "Top-level structure:"
  find . -maxdepth 2 -type d \
    -not -path './venv*' \
    -not -path './.git*' \
    -not -path './__pycache__*' \
    -not -path './reports/__pycache__*' \
    -not -path './reports/charts/__pycache__*' \
    | sort
  echo ""
  echo "Files per category in data/:"
  for cat in pm running oliveoil skincare finance household knives; do
    count=$(find "data/$cat" -type f 2>/dev/null | wc -l | tr -d ' ')
    echo "  data/$cat: $count files"
  done
  echo ""
  echo "registries/ contents:"
  ls -1 registries/ 2>/dev/null
  echo ""
  echo "prompts/ contents:"
  ls -1 prompts/ 2>/dev/null
  echo ""
  echo "Root-level CSVs still present (DELETE MANUALLY after verifying data/):"
  ls -1 *.csv 2>/dev/null | head -30
  echo ""
  echo "Root-level loose files remaining:"
  find . -maxdepth 1 -type f \
    -not -name '.*' \
    -not -name '*.csv' \
    | sort
  echo ""
  echo "===================================================================="
  echo "Done. Manual follow-ups:"
  echo "  1. Restore registries/brands_{running,oliveoil,skincare,finance}.json from iCloud"
  echo "  2. Restore prompts/prompts_{running,oliveoil,skincare,finance}.json from iCloud"
  echo "  3. Confirm skincare canonical run (17:35 vs 17:55) and rename _pre_revision/ accordingly"
  echo "  4. After spot-checking data/, delete root-level CSVs:"
  echo "       rm results_v2_*.csv results_enriched_*.csv presence_index_*.csv"
  echo "       rm manual_review_bbb_*.csv spot_check_audit_*.csv cross_tab_valence_*.csv"
  echo "       rm spot_check_summary_household_v1.0.txt"
  echo "       rm *.log"
  echo "  5. Decide whether to delete brands.json + prompts.json at root, or"
  echo "     symlink them to registries/brands_household.json + prompts/prompts_household.json"
  echo "     (keeping the runner working until the --category refactor lands)"
  echo "  6. Refactor run_aias_v2.py to take --category arg (Phase 2 to-do per protocol §C)"
  echo "===================================================================="
}

# ====================================================================
# Run all phases
# Comment out lines below to run incrementally.
# ====================================================================
phase_0_snapshot
phase_1_skeleton
phase_2_promote
phase_3_registries
phase_4_sort_csvs
phase_5_archive
phase_6_junk
phase_7_verify
