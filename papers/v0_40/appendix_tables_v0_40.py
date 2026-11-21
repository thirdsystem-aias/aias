#!/usr/bin/env python3
"""Write Appendix A of the v0.40 paper template: the pre-registered tables the locked scorer did not output,
computed after scoring by osf/v40/scripts/postscore_v0_40.py (DEVIATIONS Entry 2).

The block between the APPENDIX markers of papers/v0_40/v0_40_ssrn_paper_template.md is (re)written with
{{v:KEY}} placeholders only: no number is typed. Which keys exist (for example, a ghost with no pre-cutoff status
answer has no H_Flag row) is read from osf/v40/v40_values.json. fill_paper_v0_40.py then fills the template as usual.

Run from the repo or worktree root:  python3 papers/v0_40/appendix_tables_v0_40.py [--check]
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = ROOT / "papers/v0_40/v0_40_ssrn_paper_template.md"
VALUES = json.loads((ROOT / "osf/v40/v40_values.json").read_text(encoding="utf-8"))["values"]
START, END = "<!-- APPENDIX A START (appendix_tables_v0_40.py) -->", "<!-- APPENDIX A END -->"
SLOTS = ["M1", "M2", "M3", "M4", "M5", "M6", "C1", "C2", "C3"]
NAMES = {"M1": "Claude Opus 4.5", "M2": "Claude Sonnet 4.5", "M3": "GPT-4o", "M4": "GPT-4o mini",
         "M5": "Gemini 2.5 Flash", "M6": "Gemini 2.5 Flash-Lite", "C1": "Claude Fable 5.2", "C2": "GPT-6 Astra",
         "C3": "Gemini 4 Argon"}
PT = "prereg_post.per_test"
D1 = "prereg_post.d1_ai_share"
D2 = "prereg_post.d2_ghosts"


def k(key):
    if key not in VALUES:
        raise KeyError(key)
    return "{{v:" + key + "}}"


def has(key):
    return key in VALUES


def of(a, b):
    return f"{k(a)} of {k(b)}"


def table(caption, head, align, rows):
    out = [f"Table: {caption}", "", "| " + " | ".join(head) + " |", "|" + "|".join(align) + "|"]
    out += ["| " + " | ".join(r) + " |" for r in rows]
    return "\n".join(out) + "\n"


def a1():
    rows = []
    for sl in SLOTS:
        rows.append([f"{NAMES[sl]} ({sl})",
                     k(f"{PT}.H_Reinforce.by_model.{sl}.airline.rho"), k(f"{PT}.H_Reinforce.by_model.{sl}.bank.rho"),
                     k(f"{PT}.H_Amplify.by_model.{sl}.airline.ratio"), k(f"{PT}.H_Amplify.by_model.{sl}.airline.ceiling_ratio"),
                     k(f"{PT}.H_Amplify.by_model.{sl}.bank.ratio"), k(f"{PT}.H_Amplify.by_model.{sl}.bank.ceiling_ratio")])
    return table("Per-model results beside H_Reinforce and H_Amplify (search off; computed after scoring, DEVIATIONS "
                 "Entry 2). ρ: Spearman correlation of market share with the model's AI share; ratio: the leader's "
                 "(k/n)/p₀ for the model; ceiling: the largest ratio the measure could reach at the model's breadth "
                 "of answers. Per-model statistics carry no test.",
                 ["Model", "ρ airlines", "ρ banks", "Ratio airlines", "Ceiling airlines", "Ratio banks", "Ceiling banks"],
                 [":---", "---:", "---:", "---:", "---:", "---:", "---:"], rows)


def a2():
    rows = []
    for sl in SLOTS:
        srch = (f"{k(f'{PT}.H_Search.by_model.{sl}.s1_only_flagged')} / {k(f'{PT}.H_Search.by_model.{sl}.s0_only_flagged')}"
                if has(f"{PT}.H_Search.by_model.{sl}.s1_only_flagged") else "--")
        rows.append([f"{NAMES[sl]} ({sl})",
                     of(f"{PT}.H_Afterlife.by_model.{sl}.airline.afterlife_pairs", f"{PT}.H_Afterlife.by_model.{sl}.airline.pairs"),
                     of(f"{PT}.H_Afterlife.by_model.{sl}.bank.afterlife_pairs", f"{PT}.H_Afterlife.by_model.{sl}.bank.pairs"),
                     of(f"{PT}.H_Decay.by_model.{sl}.pairs_present", f"{PT}.H_Decay.by_model.{sl}.pairs"),
                     k(f"{PT}.H_Decay.by_model.{sl}.rho"),
                     of(f"{PT}.H_Flag.by_model.{sl}.ghost_flagged", f"{PT}.H_Flag.by_model.{sl}.ghost_answers"),
                     of(f"{PT}.H_Flag.by_model.{sl}.control_flagged", f"{PT}.H_Flag.by_model.{sl}.control_answers"),
                     srch])
    return table("Per-model results beside H_Afterlife, H_Decay, H_Flag and H_Search (computed after scoring, DEVIATIONS "
                 "Entry 2). Afterlife: pre-cutoff ghost pairs named without a gone-flag; Decay: pairs with ghost "
                 "Presence above zero, and the within-model Spearman ρ of gap against ghost Presence (n/a: no pair "
                 "named); Flag: flagged status answers about pre-cutoff ghosts and about living brands; Search: paired "
                 "ghost status cells flagged with search on only / with search off only (current models).",
                 ["Model", "Afterlife airlines", "Afterlife banks", "Decay pairs named", "Decay ρ", "Flag ghosts",
                  "Flag living brands", "Search on / off only"],
                 [":---", "---:", "---:", "---:", "---:", "---:", "---:", "---:"], rows)


def ghost_ids():
    ids = []
    for key in VALUES:
        if key.startswith(D2 + ".") and key.endswith(".brand"):
            ids.append(key[len(D2) + 1:-len(".brand")])
    return ids


def a3():
    rows = []
    for g in ghost_ids():
        b = f"{D2}.{g}"
        flag = (of(f"{PT}.H_Flag.by_ghost.{g}.flagged", f"{PT}.H_Flag.by_ghost.{g}.answers")
                if has(f"{PT}.H_Flag.by_ghost.{g}.flagged") else "--")
        rows.append([k(f"{b}.brand"), k(f"{b}.pre_cutoff_pairs"), k(f"{b}.post_cutoff_pairs"), k(f"{b}.afterlife_pairs"),
                     k(f"{b}.pairs_named"), k(f"{b}.mean_presence_pre_cutoff"), flag,
                     f"{k(f'{PT}.H_Search.by_ghost.{g}.s1_only_flagged')} / {k(f'{PT}.H_Search.by_ghost.{g}.s0_only_flagged')}",
                     of(f"{PT}.H_Search.by_ghost.{g}.post_cutoff_s1_flagged", f"{PT}.H_Search.by_ghost.{g}.post_cutoff_cells")])
    return table("Per-ghost results (descriptive 2 and the per-ghost results beside each test; computed after scoring, "
                 "DEVIATIONS Entry 2). Pairs: ghost × tested model, search off; pre- and post-cutoff exits shown "
                 "apart. Afterlife: pre-cutoff pairs named without a gone-flag; named: pre-cutoff pairs with ghost "
                 "Presence above zero; Presence: mean over pre-cutoff pairs; Flag: flagged search-off status answers "
                 "(pre-cutoff pairs; -- where there are none); Search: cells flagged with search on only / off only; "
                 "post-cutoff: of the post-cutoff current-model cells, those flagged with search on.",
                 ["Ghost", "Pre-cutoff pairs", "Post-cutoff pairs", "Afterlife", "Named", "Presence", "Flag",
                  "Search on / off only", "Post-cutoff flagged"],
                 [":---", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:"], rows)


def unit_ids(cat):
    pre = f"{D1}.{cat}.units."
    return [key[len(pre):-len(".brand")] for key in VALUES if key.startswith(pre) and key.endswith(".brand")]


def a45(cat, label):
    rows = []
    for u in unit_ids(cat):
        rows.append([k(f"{D1}.{cat}.units.{u}.brand"), k(f"{D1}.{cat}.units.{u}.market_share"),
                     k(f"{D1}.{cat}.pooled.all_nine_S0.{u}.ai_share"), k(f"{D1}.{cat}.pooled.legacy_S0.{u}.ai_share"),
                     k(f"{D1}.{cat}.pooled.current_S0.{u}.ai_share"), k(f"{D1}.{cat}.pooled.current_S1.{u}.ai_share")])
    s = f"{D1}.{cat}.loglog_slope"
    slopes = (f"Log-log slope of AI share on market share: all nine {k(s + '.all_nine_S0')}, legacy "
              f"{k(s + '.legacy_S0')}, current {k(s + '.current_S0')}, current with search {k(s + '.current_S1')}")
    if cat == "bank":
        slopes += (f"; without the brokerage and wealth holders (D4): {k(s + '.all_nine_S0_without_D4')}, "
                   f"{k(s + '.legacy_S0_without_D4')}, {k(s + '.current_S0_without_D4')} and "
                   f"{k(s + '.current_S1_without_D4')}")
    return table(f"AI share and market share of each current {label} unit (descriptive 1; computed after scoring, "
                 f"DEVIATIONS Entry 2). Market share: share of the category's current units; AI share: mean over the "
                 f"models of each model's share of unit-namings (search off unless stated). {slopes}. Each model's "
                 f"own shares are in the values file.",
                 ["Unit", "Market share", "AI share, nine", "Legacy", "Current", "Current, search on"],
                 [":---", "---:", "---:", "---:", "---:", "---:"], rows)


def a6():
    rows = []
    for g in ghost_ids():
        cells = []
        for sl in SLOTS:
            b = f"{D2}.{g}.by_model.{sl}|S0"
            mark = "" if VALUES[b + ".pre_cutoff"]["value"] else "†"
            cells.append(k(b + ".named_answers") + mark)
        rows.append([k(f"{D2}.{g}.brand")] + cells)
    ans = k(f"{D2}.{ghost_ids()[0]}.by_model.M1|S0.answers")
    return table("Ghost Presence by model: search-off recommendation answers naming the ghost, of the "
                 f"{ans} answers per model and category (descriptive 2; computed after scoring, DEVIATIONS Entry 2). "
                 "†: post-cutoff exit for that model (not a tested pair). Models: M1 Claude Opus 4.5, M2 Claude "
                 "Sonnet 4.5, M3 GPT-4o, M4 GPT-4o mini, M5 Gemini 2.5 Flash, M6 Gemini 2.5 Flash-Lite, C1 Claude "
                 "Fable 5.2, C2 GPT-6 Astra, C3 Gemini 4 Argon. The search-on answers and the gaps are in the values "
                 "file.",
                 ["Ghost"] + SLOTS, [":---"] + ["---:"] * len(SLOTS), rows)


def block():
    intro = ("These tables are pre-registered, computed after scoring because the locked scorer did not output them "
             "(§3.10; DEVIATIONS Entry 2). They were computed from the frozen coded mentions by "
             "`osf/v40/scripts/postscore_v0_40.py`, which imports the locked scorer unchanged and first reproduces "
             "the scored tests exactly; they carry no verdict and change none. Every value is read from "
             "`osf/v40/v40_values.json` (keys `prereg_post.*`).")
    parts = [START, "", "# Appendix A. Pre-registered tables computed after scoring {-}", "", intro, "",
             a1(), a2(), a3(), a45("airline", "airline"), a45("bank", "bank"), a6(), END]
    return "\n".join(parts)


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    tpl = TEMPLATE.read_text(encoding="utf-8")
    new_block = block()
    if START in tpl:
        a, rest = tpl.split(START, 1)
        _, b = rest.split(END, 1)
        out = a + new_block + b
    else:
        out = tpl.rstrip("\n") + "\n\n" + new_block + "\n"
    if "--check" in argv:
        same = out == tpl
        print("appendix up to date" if same else "appendix DIFFERS")
        return 0 if same else 1
    TEMPLATE.write_text(out, encoding="utf-8")
    print(f"wrote Appendix A into {TEMPLATE.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
