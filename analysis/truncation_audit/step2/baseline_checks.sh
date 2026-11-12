#!/bin/zsh
# Step 2: re-run every baseline comparison and the variant cross-checks; output -> results/baseline_checks.txt
# Usage: zsh analysis/truncation_audit/step2/baseline_checks.sh   (from the truncation-audit worktree root)
setopt nonomatch
S=/Users/pablou/aias/_worktrees/_runner_tmp/truncation_s2
A=/Users/pablou/aias/_worktrees/aias-2.0
T=/Users/pablou/aias/_worktrees/truncation-audit
PY=/Users/pablou/aias/venv/bin/python3
C=$T/analysis/truncation_audit/step2/compare_outputs.py
export PYTHONDONTWRITEBYTECODE=1
cd $T
{
echo "== v0.41 stock --synthetic on byte copy of osf/v41/data vs published (whole file; table)"
$PY $C json osf/v41/v41_verdicts.json $S/out/v41_full/v41_verdicts.json
$PY $C csv osf/v41/v41_three_wave_table.csv $S/out/v41_full/v41_three_wave_table.csv
echo "== v0.41 per-substrate wrapper, mode baseline, vs published (verdicts; table)"
$PY $C json osf/v41/v41_verdicts.json $S/out/v41ps_baseline/v41_verdicts.json --key verdicts
$PY $C csv osf/v41/v41_three_wave_table.csv $S/out/v41ps_baseline/v41_three_wave_table.csv
echo "== v0.41 wrapper mode b vs stock --synthetic on the Flash-free copy (verdicts; table)"
$PY $C json $S/out/v41_noflash/v41_verdicts.json $S/out/v41ps_b/v41_verdicts.json --key verdicts
$PY $C csv $S/out/v41_noflash/v41_three_wave_table.csv $S/out/v41ps_b/v41_three_wave_table.csv
echo "== v1.9 Stage 2 stock --stage2-synthetic on byte copy vs published (whole file)"
$PY $C json $A/osf/methodology/v1_9/v1_9_verdicts.json $S/t3/full/_score_v1_9/v1_9_verdicts.json
echo "== v1.9 wrapper mode baseline vs published (verdicts; constraints_t3)"
$PY $C json $A/osf/methodology/v1_9/v1_9_verdicts.json $S/out/v19ps_baseline/v1_9_verdicts.json --key verdicts
$PY $C json $A/osf/methodology/v1_9/v1_9_verdicts.json $S/out/v19ps_baseline/v1_9_verdicts.json --key constraints_t3
echo "== v1.9 wrapper mode b vs stock on the Flash-free copy (verdicts; constraints_t3)"
$PY $C json $S/t3/noflash/_score_v1_9/v1_9_verdicts.json $S/out/v19ps_b/v1_9_verdicts.json --key verdicts
$PY $C json $S/t3/noflash/_score_v1_9/v1_9_verdicts.json $S/out/v19ps_b/v1_9_verdicts.json --key constraints_t3
echo "== AIAS 2.0 builder (test flags, published v0.41 + v1.9 files) vs published: profiles; synthesis json"
$PY $C csv $A/osf/aias_2_0/aias_2_0_profiles.csv $S/out/a20_baseline/aias_2_0_profiles.csv
$PY $C json $A/osf/aias_2_0/aias_2_0_synthesis_data.json $S/out/a20_baseline/aias_2_0_synthesis_data.json
for k in stage2 parity_builder_vs_stage1 parity_gates_v0_41 lineage spec status; do
  $PY $C json $A/osf/aias_2_0/aias_2_0_synthesis_data.json $S/out/a20_baseline/aias_2_0_synthesis_data.json --key $k | head -1
done
echo "== AIAS 2.0 builder baseline under PYTHONHASHSEED 0/1/2 (summaries identical to each other?)"
$PY $C json $S/out/a20_baseline_hash0/aias_2_0_synthesis_data.json $S/out/a20_baseline_hash1/aias_2_0_synthesis_data.json --key summaries | head -1
$PY $C json $S/out/a20_baseline_hash0/aias_2_0_synthesis_data.json $S/out/a20_baseline_hash2/aias_2_0_synthesis_data.json --key summaries | head -1
echo "== v0.34 stock score_v34.py under HOME=scratch mirror vs published (whole file)"
$PY $C json osf/v34/v34_verdicts.json $S/home34/aias/osf/v34/v34_verdicts.json
echo "== v0.34 wrapper mode baseline vs published (each published key)"
for k in phase title lock seed mc_draws panel n_brand_units verdicts per_substrate delta_t; do
  $PY $C json osf/v34/v34_verdicts.json $S/out/v34ps_baseline.json --key $k | head -1
done
echo "== v1.8 kernel mode baseline vs frozen v1.8 record (exact; then hash seeds 1/2/3)"
$PY $C json osf/v41/registries/v1_8_verdicts.json $S/out/v18k_baseline.json --key verdicts
$PY $C json osf/v41/registries/v1_8_verdicts.json $S/out/v18k_baseline.json --key two_wave_reproducibility
for h in 1 2 3; do
  echo "PYTHONHASHSEED=$h:"; $PY $C json osf/v41/registries/v1_8_verdicts.json $S/out/v18k_baseline_hash$h.json --key verdicts
done
$PY -c "import json; d=json.load(open('$S/out/v18k_baseline.json')); print('instrument table vs frozen:', d['baseline_check']['instrument_table_vs_frozen'])"
} 2>&1
