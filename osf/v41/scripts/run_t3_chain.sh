#!/bin/zsh
# run_t3_chain.sh — v0.41 t3 acquisition chain (logging wrapper; no runner change).
# MC_ProbeParity: the 8 probe artifacts are checked against the locked SHA-256
# immediately before each substrate's runner; any mismatch or runner failure halts.
# Usage (Mac, login shell for keys):
#   zsh -ic 'cd ~/aias/_worktrees/v0.41 && caffeinate -dimsu zsh osf/v41/scripts/run_t3_chain.sh'
set -u
cd "${0:A:h}/../../.."
ROOT="$PWD"; export AIAS_ROOT="$ROOT"
PY="$HOME/aias/.venv-v41/bin/python"
LOG="$ROOT/osf/v41/data/_acq_chain.log"; mkdir -p "$ROOT/osf/v41/data"
ts() { date -u +%Y-%m-%dT%H:%M:%SZ; }
check() {
  local bad=0
  while read -r h f; do
    [[ -z "$h" ]] && continue
    got=$(shasum -a 256 "$ROOT/$f" | cut -d' ' -f1)
    [[ "$got" == "$h" ]] || { echo "$(ts) PARITY FAIL $f" | tee -a "$LOG"; bad=1; }
  done <<'SUMS'
276f8f5c16a9b28e813842601b5ecc416b78e6948bfefdf2df7d617b658c687e osf/v19/phase_a_queries.jsonl
75e4838dee08d6862118b6d4ef19d3f38b2d061e8059afc402eab88f874c4188 osf/v19/phase_b_queries.jsonl
542fd89b9406d18bb8635baa64d99fa1ce0999cd183f16aa56d3fb023cf6aa61 osf/v19/thresholds_v0_19.json
eb9559eaa6595eaf588dc5ec26c5c742d14c91d4ea93aaedd1e4577e3fa25782 prereg/v0_20_registry.json
45efbae5db983c24e00ad30d4b66369e685857295e8fd292a0ee0ca73349b5d3 prereg/v0_21_registry.json
431f919c809c6260815b9a7a10fe14cb915ae2ce67660aaa6ef48227783d66b9 prereg/v0_22_automotive_content.py
59f711b82efb0846f8305e7d84423667571e819aa80ad071edb01c9b1c883cfe scripts/run_acquisition_v22.py
7056f4fa88a9c2e353421f9a967470375db77f5f4a17603115810681b87152da scripts/acquire_v0_23.py
SUMS
  return $bad
}
echo "$(ts) START t3 chain (root $ROOT)" | tee -a "$LOG"
for sub in ${@:-v20 v21 v22 v23 v19}; do
  check || { echo "$(ts) HALT before $sub: probe parity" | tee -a "$LOG"; exit 2; }
  echo "$(ts) parity 8/8 ok; START $sub" | tee -a "$LOG"
  "$PY" -u osf/v41/scripts/run_acquisition_v41.py --substrate "$sub" >> "$ROOT/osf/v41/data/_acq_$sub.log" 2>&1
  rc=$?
  echo "$(ts) END $sub exit=$rc" | tee -a "$LOG"
  [[ $rc -eq 0 ]] || { echo "$(ts) HALT after $sub" | tee -a "$LOG"; exit 3; }
done
echo "$(ts) DONE t3 chain" | tee -a "$LOG"
