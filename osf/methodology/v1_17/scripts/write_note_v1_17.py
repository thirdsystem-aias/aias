"""
write_note_v1_17.py -- fills the fixed-form results note of v1.17 (PRE_REGISTRATION_v1_17.md sections 5 and 6) from
a results JSON. Wording around the numbers may be edited by hand afterwards; the numbers come only from the JSON.

usage: python3 write_note_v1_17.py RESULTS_JSON OUT_MD [--v040-runs R] [--v040-brands N] [--v040-questions Q]
                                   [--synthetic]
"""
import argparse
import json
import math
from pathlib import Path

ASSUME = "assuming independent runs with the same variance as t4's three"


def f3(x):
    return f"{x:.3f}"


def rstar(row, tau):
    r = row[f"R_needed_se_below_{tau:.2f}"]
    lo, hi = r["ci95_cluster_bootstrap"]
    flag = " (interval flagged: fewer than 10 clusters)" if row.get("few_clusters_flag") else ""
    unit = "run" if r["point"] == 1 else "runs"
    return f"{r['point']} {unit} (95% interval {lo}–{hi}){flag}"


def block(name, row, what="units"):
    return (f"- {name} (n = {row['n_units']:,} {what}, {row['n_clusters']} answer cells): one run's standard error "
            f"{f3(row['sd_one_run'])}; three runs {f3(row['se_at_R']['3'])}. Below 0.10: {rstar(row, 0.10)}; below "
            f"0.05: {rstar(row, 0.05)}, {ASSUME}.")


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("out")
    ap.add_argument("--v040-runs", type=int)
    ap.add_argument("--v040-brands", type=int)
    ap.add_argument("--v040-questions", type=int)
    ap.add_argument("--synthetic", action="store_true")
    a = ap.parse_args(argv)
    d = json.loads(Path(a.src).read_text(encoding="utf-8"))
    t4, om = d["t4"], d["omnibus"]
    P, A = t4["primary"], t4["alongside"]
    L = []
    if a.synthetic:
        L.append("> SYNTHETIC DATA (dry run). These numbers describe made-up data with a known answer.\n")
    L.append("# v1.17 results note: how many runs are enough (exploratory)\n")
    L.append("## Runs needed, by category size\n")
    for k, lab in (("all", "All brands"), ("size_24", "24-brand categories"), ("size_16", "16-brand category (v0.19)")):
        L.append(block(lab, P[k]))
    L.append("")
    L.append("Without Denon and the five brands with agency ties (S-COI):")
    for k, lab in (("S_COI_all", "All"), ("S_COI_size_24", "24-brand"), ("S_COI_size_16", "16-brand")):
        L.append(block(lab, A[k]))
    L.append("\n## By how often a brand is named\n")
    for b in ("zero", "low", "middle", "high", "full"):
        row = A[f"band_{b}"]
        if row["n_units"]:
            L.append(f"- {b}: n = {row['n_units']} units; one run's standard error {f3(row['sd_one_run'])}.")
        else:
            L.append(f"- {b}: no units.")
    L.append("\n## Other scales\n")
    L.append(block("Per question (frame level)", t4["alongside_frame_level"]["all"], "unit-question pairs"))
    L.append(block("Three-model panel (published N3 Presence)", t4["alongside_panel_N3"]["all"], "brand-condition pairs"))
    pu = t4["per_unit_se"]
    L.append(f"- Per unit, from its own three runs (2 degrees of freedom each): {pu['se3_below_0.10']} of "
             f"{pu['n_units']} units have a three-run standard error below 0.10 and {pu['se3_below_0.05']} below 0.05; "
             f"{pu['units_zero_variance']} did not move at all.")
    o = t4["once_vs_three"]
    L.append("\n## Measured once instead of three times\n")
    u, p = o["unit_level_vs_three_run_mean"], o["panel_N3_vs_three_run_mean"]
    L.append(f"- Per model: {u['brands_changing_place']:,} of {u['brand_runs']:,} brand-runs change place against at "
             f"least one brand ({u['share_brands_changing_place']:.1%}); {u['discordant_pairs']:,} of {u['pairs']:,} pairs "
             f"reverse ({u['share_pairs_reversed']:.1%}).")
    L.append(f"- Three-model panel: {p['brands_changing_place']:,} of {p['brand_runs']:,} brand-runs ({p['share_brands_changing_place']:.1%}); "
             f"{p['discordant_pairs']:,} of {p['pairs']:,} pairs reverse ({p['share_pairs_reversed']:.1%}).")
    for c, lab in (("S0", "search off"), ("S1", "search on")):
        fl = o["published_floor_N3"][c]
        per = ", ".join(f"{x['brands_crossing']} (run {x['run']})" for x in fl["per_run"])
        L.append(f"- Recall floor, {lab}: {fl['below_floor_three_runs']} of {fl['n_brands']} brands below it with three "
                 f"runs; one run alone would change the status of {per} (mean {fl['mean_brands_crossing']:.1f}).")
    nm = o["unit_named_three_runs_not_in_one"]
    L.append(f"- Of {nm['units_named_in_three_runs']} units named at least once in three runs, a single run would show "
             f"{', '.join(str(x) for x in nm['per_run_missed'])} (runs 1, 2, 3) as never named.")
    L.append("\n## Omnibus waves (time drift plus run noise; legacy models; never pooled with t4)\n")
    for k, lab in (("all", "All"), ("size_24", "24-brand"), ("size_16", "16-brand")):
        row = om["strata"][k]
        lo, hi = (math.sqrt(v) for v in row["var_ci95_cluster_bootstrap"])
        L.append(f"- {lab} (n = {row['n_units']} units): wave-to-wave standard deviation {f3(row['sd_one_run'])} "
                 f"(95% interval {f3(lo)}–{f3(hi)}).")
    g = om["half_mean_squared_change"]
    L.append(f"- Half mean squared change: t1→t2 {f3(g['t1_t2']['all'])}, t2→t3 {f3(g['t2_t3']['all'])}, "
             f"t1→t3 {f3(g['t1_t3']['all'])} (all units).")
    L.append("\n## What v0.40 should check (recommendation only; v0.40's own pre-registration decides)\n")
    allr = P["all"]
    if a.v040_runs:
        R = a.v040_runs
        lo, hi = (math.sqrt(v / R) for v in allr["var_ci95_cluster_bootstrap"])
        L.append(f"- At {R} runs per cell, v1.17 suggests a per-model standard error of about "
                 f"{f3(allr['sd_one_run'] / math.sqrt(R))} (95% interval {f3(lo)}–{f3(hi)}), {ASSUME}; "
                 f"{'enough' if R >= allr['R_needed_se_below_0.10']['point'] else 'not enough'} for 0.10 and "
                 f"{'enough' if R >= allr['R_needed_se_below_0.05']['point'] else 'not enough'} for 0.05.")
    else:
        L.append("- v0.40's runs per cell: not given to this script.")
    if a.v040_brands:
        if 16 <= a.v040_brands <= 24:
            near = "size_16" if abs(a.v040_brands - 16) < abs(a.v040_brands - 24) else "size_24"
            L.append(block(f"Nearest t4 size ({near})", P[near]))
        else:
            L.append(f"- v0.40 has {a.v040_brands} brands per category: no t4 size stratum matches.")
    if a.v040_questions:
        v = t4["alongside_frame_level"]["all"]["pooled_var"] / a.v040_questions
        L.append(f"- With {a.v040_questions} questions per category, one run's standard error would be about "
                 f"{f3(math.sqrt(v))}, assuming the questions of one run vary independently.")
    L.append("- Legacy arm (one call per probe and model): t4 has no legacy runs; the omnibus figures above mix drift "
             "and noise and are not a run-to-run estimate for it.")
    Path(a.out).write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"wrote {a.out}")


if __name__ == "__main__":
    main()
