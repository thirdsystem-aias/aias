#!/usr/bin/env python3
"""
sens_coi106_en_corrected_v0_62.py -- AIAS v0.62, post-scoring sensitivities of DEVIATIONS Entries 4 and 6
(written Wed 2026-11-25, after the one scoring run of commit 262464d; approved by the pre-registrant, "Pablo, Wed
2026-11-25 9:40 am CT, control chat: Ok to all"). No model is called. score_v0_62.py and params_v0_62.py (locked,
73-file manifest) are imported UNCHANGED; this script only calls their functions. The locked verdicts stand as scored.

Step 0 (reproduction): score_v0_62.score() is re-run on the locked inputs (v0.42 v42_brand_table.csv, the coded
  tables of commit 262464d, the same --rank-status) and its JSON is compared with osf/v62/v62_verdicts.json; the
  script stops if they differ.
Entry 4, S-COI (106 units): params_v0_62.COI_FLAGGED names v0.23's unit as ("v0.23", "Jack Daniel's"), but the t4
  and v0.62 tables key v0.23 units by registry id (S01-S24), so the locked S-COI removed 5 of the 6 units (107 units).
  Here the flagged names are mapped to the table keys with v0.23's registry (osf/v23/scripts/score_v0_23.py:
  S03 = Jack Daniel's) and S-COI is recomputed on 106 units: H_Lang_Presence's rank_test with the primary seed,
  verdict_presence and the 90% drop rule, exactly as score_v0_62.score() computes S-COI. Reported beside the as-run
  107-unit S-COI.
Entry 6, corrected English comparator: score_v0_62.score() run in full with the English comparator
  v42_brand_table_corrected_2026-11-25.csv (v0.42 erratum of 2026-11-25; SHA-256 de8559cb...; 14 cells of Paula's
  Choice and L'Oreal Paris differ) instead of the locked v42_brand_table.csv (792e14ad...), plus the 106-unit S-COI
  on that comparator. Reported beside the locked comparison.

Usage: python3 sens_coi106_en_corrected_v0_62.py --v42 <v0.42 worktree>/osf/v42 [--out-dir osf/v62/data]
Writes (refuses to overwrite): v62_sens_coi106_v0_62.json, v62_sens_en_corrected_v0_62.json.
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import params_v0_62 as P  # noqa: E402  (locked; unchanged)
import score_v0_62 as S  # noqa: E402  (locked; unchanged)

RANK_STATUS = "MARGINAL (v1.14 Stage 1, commit 3129674; not PASS)"   # as in data/gates/run_v62_score.sh
LOCKED_EN_SHA = "792e14addb7ad1ef03a147ee16cee56e82cfecd58030d2e8e3cf3e3ea255af7f"
CORR_EN_SHA = "de8559cbe21db91e8922337c7ab5bdfaa7d1d2325f6bbe0870e6abcd812a5c4d"
V23_REGISTRY = S.ROOT / "osf/v23/scripts/score_v0_23.py"


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def v23_ids(path=V23_REGISTRY):
    """v0.23 registry: brand name -> registry id (S01-S24), read from score_v0_23.py's BRANDS list."""
    text = Path(path).read_text(encoding="utf-8")
    m = dict((b, i) for i, b in re.findall(r'\{"id": "(S\d\d)", "brand": "([^"]+)"', text))
    if len(m) != 24:
        raise SystemExit(f"v0.23 registry: expected 24 ids, found {len(m)}")
    return m


def coi_keys_mapped(ids):
    """params_v0_62.COI_FLAGGED with v0.23 brand names mapped to their table keys."""
    return {(s, ids[b]) if s == "v0.23" else (s, b) for s, b in P.COI_FLAGGED}


def s_coi_106(units, en, lang_B, flagged, option=None):
    """S-COI as score_v0_62.score() computes it, on the 112 units minus the six flagged units (mapped keys)."""
    option = option or P.HEADPHONES_OPTION
    keys107 = S.unit_set(units, option, "S-COI")
    keys = [u for u in S.unit_set(units, option) if u not in flagged]
    out = {}
    for lg in S.LANGS:
        V = S.unit_values(units, lang_B[lg])
        drop = S.dropped_models(lang_B[lg], 30)
        xpi, ypi = {u: en[u]["pi"] for u in en}, {u: V[u]["pi"] for u in V}
        t = S.rank_test(xpi, ypi, keys, S.SEEDS[("H_Lang_Presence", lg)], S.N_PERM, S.N_BOOT)
        t["verdict"] = "UNDETERMINED" if drop else S.verdict_presence(t["rho_c"], t["p_perm"])
        if drop:
            t["reason"] = f"models below 90% of Phase B calls in {lg}: {drop}"
        out[f"S-COI-106_{lg}"] = t
    return out, keys, keys107


def summary(v, extra):
    """Compact per-language table: Presence, Phi, S-COI (as-run 107) and S-COI-106."""
    rows = {}
    for lg in S.LANGS:
        p, f = v["tests"][f"H_Lang_Presence_{lg}"], v["tests"][f"H_Lang_Phi_{lg}"]
        c7, c6 = v["sensitivities"][f"S-COI_{lg}"], extra[f"S-COI-106_{lg}"]
        rows[lg] = {
            "H_Lang_Presence": {k: p[k] for k in ("n", "rho_c", "ci95_rho_c", "p_perm", "delta_L", "delta_L_ci95", "verdict")},
            "H_Lang_Phi": {k: f[k] for k in ("n", "rho_c", "ci95_rho_c", "p_perm", "verdict")},
            "S-Denon": {k: v["sensitivities"][f"S-Denon_{lg}"][k] for k in ("n", "rho_c", "ci95_rho_c", "p_perm", "verdict")},
            "S-Headphones": {k: v["sensitivities"][f"S-Headphones_{lg}"][k] for k in ("n", "rho_c", "ci95_rho_c", "p_perm", "verdict")},
            "S-COI_as_run_107": {k: c7[k] for k in ("n", "rho_c", "ci95_rho_c", "p_perm", "verdict")},
            "S-COI_106": {k: c6[k] for k in ("n", "rho_c", "ci95_rho_c", "p_perm", "verdict")},
        }
    return rows


def write_new(path, obj):
    path = Path(path)
    if path.exists():
        raise SystemExit(f"REFUSED: {path} exists (new files only)")
    path.write_text(json.dumps(S._clean(obj), indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"wrote {path} sha256 {sha256(path)}")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--v42", required=True, help="v0.42's osf/v42 folder (holds both English brand tables)")
    ap.add_argument("--coded", default=str(S.V62 / "data/coded"))
    ap.add_argument("--out-dir", default=str(S.V62 / "data"))
    a = ap.parse_args(argv)
    out_coi = Path(a.out_dir) / "v62_sens_coi106_v0_62.json"
    out_cor = Path(a.out_dir) / "v62_sens_en_corrected_v0_62.json"
    for p in (out_coi, out_cor):
        if p.exists():
            raise SystemExit(f"REFUSED: {p} exists (new files only)")
    en_locked_p = Path(a.v42) / "v42_brand_table.csv"
    en_corr_p = Path(a.v42) / "v42_brand_table_corrected_2026-11-25.csv"
    if sha256(en_locked_p) != LOCKED_EN_SHA or sha256(en_corr_p) != CORR_EN_SHA:
        raise SystemExit("English tables do not have the expected SHA-256")
    ids = v23_ids()
    flagged = coi_keys_mapped(ids)
    en_l, en_c = S.read_english(en_locked_p), S.read_english(en_corr_p)
    if sorted(en_l) != sorted(en_c):
        raise SystemExit("the two English tables do not have the same units")
    units = sorted(en_l)
    lang_B = {lg: S.read_coded_b(Path(a.coded) / lg) for lg in S.LANGS}

    # Step 0: reproduce the locked verdicts file byte for byte.
    v_l = S.score(units, en_l, lang_B, rank_status=RANK_STATUS)
    locked_text = S.VERDICTS.read_text(encoding="utf-8")
    repro = json.dumps(S._clean(v_l), indent=1, ensure_ascii=False) == locked_text
    print("reproduces v62_verdicts.json byte for byte:", repro)
    if not repro:
        raise SystemExit("STOP: the locked scoring does not reproduce; nothing written")

    inputs = {"v62_verdicts.json": sha256(S.VERDICTS), "v42_brand_table.csv": sha256(en_locked_p),
              "v42_brand_table_corrected_2026-11-25.csv": sha256(en_corr_p),
              "score_v0_62.py": sha256(Path(S.__file__)), "params_v0_62.py": sha256(Path(P.__file__)),
              "osf/v23/scripts/score_v0_23.py": sha256(V23_REGISTRY)}
    common = {"no_model_called": True, "locked_verdicts_stand": True, "rank_status": RANK_STATUS,
              "reproduced_locked_verdicts_byte_for_byte": repro, "inputs_sha256": inputs,
              "coi_flagged_params": [list(u) for u in P.COI_FLAGGED],
              "coi_flagged_table_keys": sorted(list(u) for u in flagged)}

    # Entry 4: S-COI on 106 units, locked comparator.
    c_l, keys106, keys107 = s_coi_106(units, en_l, lang_B, flagged)
    if len(keys106) != 106 or len(keys107) != 107 or set(keys107) - set(keys106) != {("v0.23", ids["Jack Daniel's"])}:
        raise SystemExit(f"unit sets unexpected: {len(keys106)} / {len(keys107)}")
    write_new(out_coi, dict(common, deviation_entry=4, comparator="v42_brand_table.csv (locked, section 7.3)",
                            n_units_as_run=len(keys107), n_units_106=len(keys106),
                            unit_left_in_by_locked_code=["v0.23", ids["Jack Daniel's"], "Jack Daniel's"],
                            sensitivities=c_l, summary=summary(v_l, c_l)))

    # Entry 6: corrected English comparator (all tests), with the 106-unit S-COI on it.
    v_c = S.score(units, en_c, lang_B, rank_status=RANK_STATUS)
    c_c, _k, _k7 = s_coi_106(units, en_c, lang_B, flagged)
    diff = {lg: {t: {"locked": summary(v_l, c_l)[lg][t]["verdict"], "corrected": summary(v_c, c_c)[lg][t]["verdict"]}
                 for t in summary(v_l, c_l)[lg]} for lg in S.LANGS}
    write_new(out_cor, dict(common, deviation_entry=6,
                            comparator="v42_brand_table_corrected_2026-11-25.csv (v0.42 erratum of 2026-11-25)",
                            result_corrected=v_c, s_coi_106_corrected=c_c,
                            summary_locked=summary(v_l, c_l), summary_corrected=summary(v_c, c_c),
                            verdicts_side_by_side=diff,
                            joint_reading={"locked": v_l["joint_reading"], "corrected": v_c["joint_reading"]}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
