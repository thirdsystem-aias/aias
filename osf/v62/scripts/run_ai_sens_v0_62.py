#!/usr/bin/env python3
"""
run_ai_sens_v0_62.py -- AIAS v0.62: thin run wrapper for the Entry 2 sensitivities S-Trans and S-AliasAI
(DEVIATIONS Entry 5; written Wed 2026-11-25 after the one scoring run of commit 262464d; approved by the
pre-registrant, "Pablo, Wed 2026-11-25 9:40 am CT, control chat: Ok to all").

score_ai_sens_v0_62.py (commit d75ff81, SHA-256 b328995c..., named in Entry 2's addendum) has no run entry point. This
wrapper only reads files and calls functions of the existing modules, unchanged:
  --prepare-alias-ai WORK OUT  score_ai_sens_v0_62.alias_ai_aliaser(off) on the C4 result
                               (ai_check/results/s_alias_ai_off_v0_62.json, Korean and Chinese lists together), then
                               code_v0_62.prepare_raw(osf/v62/data/v62_raw.jsonl, WORK, aliaser=...) and v0.42's coder
                               (code_t4_v0_42.py --raw WORK/v62_prepared_{ko,zh}.jsonl --out OUT/{ko,zh}; judge OFF)
                               exactly as the primary coding (data/gates/run_v62_score.sh), Korean and Chinese only.
  --score OUT                  score_ai_sens_v0_62.score(units, en, lang_B, rank_status=..., s_trans=flags,
                               en_B=t4's coded English Phase B rows, s_alias_ai={'ko': OUT/ko, 'zh': OUT/zh}) with
                               the locked English comparator (v0.42 v42_brand_table.csv) and the primary coded tables;
                               writes the result (refuses to overwrite) and checks that its 'tests', 'sensitivities'
                               and 'joint_reading' equal osf/v62/v62_verdicts.json.
No model is called (the v0.42 coder runs without --judge; the C4 and C1-C3 results are the archived ones).
"""
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import code_v0_62 as C  # noqa: E402  (locked; unchanged)
import score_ai_sens_v0_62 as SA  # noqa: E402  (Entry 2 (d); unchanged)
import score_v0_62 as S  # noqa: E402  (locked; unchanged)

RANK_STATUS = "MARGINAL (v1.14 Stage 1, commit 3129674; not PASS)"   # as in data/gates/run_v62_score.sh
RES = S.V62 / "ai_check/results"
FLAGS = RES / "s_trans_flags_v0_62.json"
ALIAS_OFF = RES / "s_alias_ai_off_v0_62.json"


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def prepare_alias_ai(work, out, v42):
    off_json = json.loads(ALIAS_OFF.read_text(encoding="utf-8"))
    if not all(off_json[lg].get("complete") for lg in ("ko", "zh")):
        raise SystemExit("C4 result not complete")
    off = [tuple(x) for lg in ("ko", "zh") for x in off_json[lg]["off"]]
    aliaser, n_removed = SA.alias_ai_aliaser(off)
    print(f"S-AliasAI: {len(off)} alias(es) switched off: {off}; {n_removed} alias row(s) removed from the coder input")
    n, h = C.prepare_raw(C.REAL_RAW, work, aliaser=aliaser)
    print(f"prepared {n} lines; {h} collision-prone alias matches")
    for lg in ("ko", "zh"):
        r = subprocess.run([sys.executable, str(Path(v42) / "scripts/code_t4_v0_42.py"), "--raw",
                            str(Path(work) / f"v62_prepared_{lg}.jsonl"), "--out", str(Path(out) / lg)])
        if r.returncode != 0:
            raise SystemExit(f"coder failed on {lg}")
    return 0


def score(out, v42, result_path):
    result_path = Path(result_path)
    if result_path.exists():
        raise SystemExit(f"REFUSED: {result_path} exists (new files only)")
    en_p = Path(v42) / "v42_brand_table.csv"
    en = S.read_english(en_p)
    units = sorted(en)
    lang_B = {lg: S.read_coded_b(S.V62 / "data/coded" / lg) for lg in S.LANGS}
    en_B = S.read_coded_b(Path(v42) / "data/coded")
    flags = json.loads(FLAGS.read_text(encoding="utf-8"))
    if not all(flags[lg].get("complete") for lg in S.LANGS):
        raise SystemExit("S-Trans flags not complete")
    s_trans = {lg: {k: flags[lg][k] for k in SA.LINES} for lg in S.LANGS}
    s_alias = {lg: S.read_coded_b(Path(out) / lg) for lg in ("ko", "zh")}
    v = SA.score(units, en, lang_B, rank_status=RANK_STATUS, s_trans=s_trans, en_B=en_B, s_alias_ai=s_alias)
    locked = json.loads(S.VERDICTS.read_text(encoding="utf-8"))
    mine = json.loads(json.dumps(S._clean(v), ensure_ascii=False))
    same = all(mine[k] == locked[k] for k in ("tests", "sensitivities", "joint_reading"))
    print("primary keys equal v62_verdicts.json:", same)
    v["wrapper"] = {"deviation_entry": 5, "no_model_called": True, "rank_status": RANK_STATUS,
                    "primary_keys_equal_locked_verdicts": same,
                    "comparator": "v42_brand_table.csv (locked, section 7.3)",
                    "inputs_sha256": {"v42_brand_table.csv": sha256(en_p), "s_trans_flags_v0_62.json": sha256(FLAGS),
                                      "s_alias_ai_off_v0_62.json": sha256(ALIAS_OFF),
                                      "score_ai_sens_v0_62.py": sha256(SA.__file__),
                                      "score_v0_62.py": sha256(S.__file__),
                                      "v62_verdicts.json": sha256(S.VERDICTS)},
                    "en_B": str(Path(v42) / "data/coded") + " (t4 coded English Phase B rows, locked)",
                    "s_alias_ai_coded": str(out)}
    result_path.write_text(json.dumps(S._clean(v), indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"wrote {result_path} sha256 {sha256(result_path)}")
    return 0 if same else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description="v0.62 Entry 2 sensitivities: thin run wrapper (DEVIATIONS Entry 5)")
    ap.add_argument("--v42", required=True, help="v0.42's osf/v42 folder")
    ap.add_argument("--prepare-alias-ai", nargs=2, metavar=("WORK", "OUT"))
    ap.add_argument("--score", metavar="OUT", help="folder with the S-AliasAI coded ko/ and zh/ tables")
    ap.add_argument("--result", default=str(S.V62 / "data/v62_sens_ai_check_v0_62.json"))
    a = ap.parse_args(argv)
    if a.prepare_alias_ai:
        work, out = a.prepare_alias_ai
        for lg in ("ko", "zh"):
            if (Path(out) / lg).exists():
                raise SystemExit(f"REFUSED: {Path(out) / lg} exists (new files only)")
        return prepare_alias_ai(work, out, a.v42)
    if a.score:
        return score(a.score, a.v42, a.result)
    ap.error("--prepare-alias-ai WORK OUT or --score OUT")


if __name__ == "__main__":
    sys.exit(main())
