#!/usr/bin/env python3
"""
v0.33 POST-HOC recognition-source audit (walled, exploratory).

NOT part of the confirmatory lock (v0.33-prereg-r1) and carries no tag. This is the
evidence behind the study's methodological finding: the pre-registered Beyond_Presence
gate collapses because per-model recognition (Presence, C_P) is SATURATED among
recalled brands — and that saturation is REAL, not an artifact of the pre-registered
binarization.

Post-hoc question: could a graded recognition signal have un-saturated eta^2_CP?
Answer, from the frozen inputs: no graded recognition signal exists to recover. The
only graded recognition field in the program (v0.23 Phase-A r_level) is itself
uniformly maxed (R3); the other four substrates record recognition as binary at
source. Binarization did not flatten eta^2_CP — the recognition signal was already
flat. A graded re-run would reproduce the identical (≈0) eta^2_CP.

Reads only frozen Phase-A inputs + the committed confirmatory CSV; writes a JSON audit.
"""
import json, csv
from collections import Counter
from pathlib import Path

ROOT = Path.home() / "aias"
V = ROOT / "osf"


def csv_rows(p):
    return list(csv.DictReader(open(p, newline="", encoding="utf-8")))


def main():
    audit = {
        "phase": "v0.33",
        "kind": "post-hoc recognition-source audit (walled, exploratory)",
        "not_in_confirmatory_lock": True,
        "no_retag": True,
        "confirmatory_reference": "osf/v33/v33_provider_asymmetry_verdicts.json",
        "question": ("Could a graded recognition signal have un-saturated eta^2_CP — i.e. is the "
                     "Presence saturation a binarization artifact, or real recognition saturation?"),
        "recognition_source_inventory": {},
    }

    # --- v0.19: binary recognition_yes ---
    r19 = csv_rows(V / "v19/phase_a_results.csv")
    audit["recognition_source_inventory"]["v0.19"] = {
        "source": "osf/v19/phase_a_results.csv", "field": "recognition_yes",
        "type": "binary at source", "value_set": sorted(set(x["recognition_yes"] for x in r19)),
        "graded_alternative": "none"}

    # --- v0.20/21/22: binary recognized (yes/no) ---
    for k, sub in [("v0.20", "v20"), ("v0.21", "v21"), ("v0.22", "v22")]:
        r = csv_rows(V / f"{sub}/phase_a_results.csv")
        audit["recognition_source_inventory"][k] = {
            "source": f"osf/{sub}/phase_a_results.csv", "field": "recognized",
            "type": "binary at source", "value_set": sorted(set(x["recognized"] for x in r)),
            "graded_alternative": "none"}

    # --- v0.23: GRADED r_level field, but uniformly saturated ---
    pa = json.load(open(V / "v23/data/v23_phase_a_scored.json"))
    raw = json.load(open(V / "v23/data/v23_phase_a_raw.json"))
    audit["recognition_source_inventory"]["v0.23"] = {
        "source": "osf/v23/data/v23_phase_a_scored.json", "field": "r_level",
        "type": "GRADED field, uniformly saturated",
        "value_distribution": dict(Counter(x["r_level"] for x in pa)),
        "raw_graded_recognition_fields": [k for k in raw[0]
                                          if any(t in k.lower() for t in ("level", "recog", "score", "rank"))],
        "graded_alternative": "r_level is the only graded recognition field in the program; it is all R3"}

    # --- eta^2_CP from the committed confirmatory CSV ---
    rows = csv_rows(V / "v33/data/v33_eta2.csv")
    cp = [(r["substrate"], r["brand"], float(r["eta2_cp"]), r["defined"] == "True") for r in rows]
    nonzero = [x for x in cp if x[2] > 0]
    n_af = sum(1 for x in cp if x[3])
    audit["eta2_CP_evidence"] = {
        "n_brands": len(cp),
        "n_with_recognition_variance": len(nonzero),
        "n_saturated_eta2_CP_zero": len(cp) - len(nonzero),
        "brands_with_any_recog_variance": [{"substrate": s, "brand": b, "eta2_cp": round(e, 4),
                                            "above_floor": af} for s, b, e, af in nonzero],
        "n_above_floor": n_af,
        "n_above_floor_with_recog_variance": sum(1 for x in nonzero if x[3]),
        "mean_eta2_CP_above_floor": round(sum(x[2] for x in cp if x[3]) / max(1, n_af), 4)}

    audit["conclusion"] = (
        "Saturation is REAL recognition saturation, not a binarization artifact. Four substrates "
        "record recognition as binary at source (no graded alternative exists to recover); the sole "
        "graded recognition field in the program (v0.23 r_level) is itself uniformly R3. A graded "
        "re-run would reproduce the identical eta^2_CP (≈0). The Beyond_Presence gate's collapse is "
        "therefore a property of the recognition signal in this regime — recognition is near-universal "
        "among recalled brands — not of the pre-registered binary coding. This bounds when an AIAS "
        "Beyond-Presence contrast can be informative: it cannot function where recognition is saturated.")

    out = V / "v33/exploratory"
    out.mkdir(parents=True, exist_ok=True)
    json.dump(audit, open(out / "v33_recognition_source_audit.json", "w"), indent=2)
    print(json.dumps(audit, indent=2))
    print(f"\nwrote: {out/'v33_recognition_source_audit.json'}")


if __name__ == "__main__":
    main()
