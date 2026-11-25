R=~/aias/_worktrees/_runner_tmp/r1125
H=~/aias/_worktrees/_runner_tmp/heavy_lock.sh
W=~/aias/_worktrees/v0.62-nohand
V42=~/aias/_worktrees/v0.42
PY=~/aias/venv/bin/python
export PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
cd $W
ts() { echo "[$(date "+%Y-%m-%d %H:%M:%S %Z")] $*"; }
zsh $H acquire "r1125 v0.62 scoring" || { ts "heavy lock not acquired; not starting"; exit 8; }
G=osf/v62/data/gates
mkdir -p $G
ts "gate P2: prepare on t4 English answers"
$PY osf/v62/scripts/gate_p2_v0_62.py --prepare $V42/osf/v42/data/t4_raw.jsonl $R/p2_work || { ts "P2 prepare failed"; zsh $H release "r1125 v0.62 scoring"; exit 2; }
$PY $V42/osf/v42/scripts/code_t4_v0_42.py --raw $R/p2_work/p2_pre.jsonl --out $R/p2_work/pre || { ts "P2 code pre failed"; zsh $H release "r1125 v0.62 scoring"; exit 2; }
$PY $V42/osf/v42/scripts/code_t4_v0_42.py --raw $R/p2_work/p2_ref.jsonl --out $R/p2_work/ref || { ts "P2 code ref failed"; zsh $H release "r1125 v0.62 scoring"; exit 2; }
$PY osf/v62/scripts/gate_p2_v0_62.py --compare $R/p2_work/pre $R/p2_work/ref --locked $V42/osf/v42/data/coded --json $G/gate_P2_v0_62.json
p2=$?
ts "gate P2 exit $p2"
if [ $p2 -ne 0 ]; then ts "P2 did not pass: STOP before coding/scoring"; zsh $H release "r1125 v0.62 scoring"; exit 4; fi
ts "coding: pre-step"
$PY osf/v62/scripts/code_v0_62.py --prepare osf/v62/data/v62_raw.jsonl --out osf/v62/data/coded || { ts "pre-step failed/refused"; zsh $H release "r1125 v0.62 scoring"; exit 5; }
for lg in es ko zh; do
  ts "coding: v0.42 coder on $lg"
  $PY $V42/osf/v42/scripts/code_t4_v0_42.py --raw osf/v62/data/coded/v62_prepared_$lg.jsonl --out osf/v62/data/coded/$lg || { ts "coder failed on $lg"; zsh $H release "r1125 v0.62 scoring"; exit 5; }
done
ts "scoring (once)"
$PY osf/v62/scripts/score_v0_62.py --run --english $V42/osf/v42/v42_brand_table.csv --rank-status "MARGINAL (v1.14 Stage 1, commit 3129674; not PASS)"
sc=$?
ts "scorer exit $sc"
zsh $H release "r1125 v0.62 scoring"
ts "ALL DONE"
