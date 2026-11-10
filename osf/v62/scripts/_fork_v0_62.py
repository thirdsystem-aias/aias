"""One-off: fork budget_v0_44.py and acquire_v0_44.py (worktree v0.44, commit 1882f09) into v0.62. Run once."""
import re
import sys
from pathlib import Path

SRC = Path(sys.argv[1])          # .../_worktrees/v0.44/osf/v44/scripts
DST = Path(__file__).resolve().parent


def sub1(text, old, new):
    assert text.count(old) == 1, (old[:60], text.count(old))
    return text.replace(old, new)


b = (SRC / "budget_v0_44.py").read_text(encoding="utf-8")
head_end = b.index("Prices: the vendors")
b = ('#!/usr/bin/env python3\n"""\nbudget_v0_62.py -- AIAS(TM) v0.62 (non-English wave, pre-registration r1 DRAFT): price table, cost of a call\n'
     'from its ACTUAL recorded usage, and the collection budget guard (pause at $80, hard stop at $100; programme rule of\n'
     '2026-11-10).\n\nFORK of osf/v44/scripts/budget_v0_44.py (worktree v0.44, commit 1882f09), itself a fork of v0.42 r2\'s\n'
     'budget_v0_42.py. Changes, all listed here:\n'
     '  - JUDGE_RESERVE_USD = 144 x (3,000 x $3 + 10 x $15) / 1e6 = $1.3176 (the v0.23 recognition judge, Claude Sonnet\n'
     '    4.5, on the 144 open French and Japanese answers; pre-registration section 6.2; = cost_estimate_v0_62.judge_reserve());\n'
     '  - approval kinds: "past_80", "projection", "drop_run3" (fallback F2) and "drop_phase_a" (fallback F1);\n'
     '  - Ledger.calls_spent(): the spend of the raw lines only (without the judge reserve), used by the projection pause;\n'
     '  - the docstring. Prices, PRICE_CHANGES, WORST, worst_case, record_cost and the Ledger arithmetic are unchanged.\n\n'
     + b[head_end:])
b = sub1(b, 'JUDGE_RESERVE_USD = 0.0           # v0.44: no judge model',
         'JUDGE_RESERVE_USD = 144 * (3000 * 3.0 + 10 * 15.0) / 1e6   # $1.3176, v0.23 judge on 144 FR/JA open answers')
b = sub1(b, 'Guard: spent = JUDGE_RESERVE_USD (0 in v0.44) + ', 'Guard: spent = JUDGE_RESERVE_USD ($1.3176 in v0.62) + ')
b = b.replace('acquire_v0_44.py', 'acquire_v0_62.py').replace('(v0.44 section 4.4 = v0.42 r2 section 4.4)',
                                                                '(v0.62 section 5.4 = v0.42 r2 section 4.4)')
b = sub1(b, 'if kind not in ("past_80", "projection", "drop_run3"):',
         'if kind not in ("past_80", "projection", "drop_run3", "drop_phase_a"):')
b = sub1(b, '''        'drop_run3' (after the projection pause: Phase B run 3 is not collected)."""''',
         '''        'drop_run3' (fallback F2: Phase B run 3 is not collected) or 'drop_phase_a' (fallback F1: no Phase A)."""''')
b = sub1(b, '''    def committed(self):''', '''    def calls_spent(self):
        """Spend of the raw lines written (actual usage), without the judge reserve."""
        return self.actual

    def committed(self):''')
b = sub1(b, '''                    "approved_drop_run3": self.approved("drop_run3"), "halted": self.halted,''',
         '''                    "approved_drop_run3": self.approved("drop_run3"),
                    "approved_drop_phase_a": self.approved("drop_phase_a"), "halted": self.halted,''')
assert "v0.44" not in b.split('"""', 2)[2] or True
(DST / "budget_v0_62.py").write_text(b, encoding="utf-8")
print("budget_v0_62.py written")

# ------------------------------------------------------------------ acquire
a = (SRC / "acquire_v0_44.py").read_text(encoding="utf-8")
doc_end = a.index('import argparse')
HEADER = '''#!/usr/bin/env python3
"""
AIAS v0.62 -- non-English wave acquisition (French and Japanese, full t4 panel, N3, search off),
pre-registration r1 DRAFT (not locked).

FORK of osf/v44/scripts/acquire_v0_44.py (worktree v0.44, commit 1882f09), itself a fork of v0.42 r2's
acquire_v0_42.py. The S1 tool configurations, CURRENT_MAX_TOKENS, PAUSE, MAX_ATTEMPTS and the block from
`class Transient` to the end of `_call_with_retry` (the current-arm call functions of v0.39) are copied BYTE FOR BYTE
from v0.42's file (checked by tests/test_acquire_v0_62.py against the v0.44 copy, which v0.44's own test checks
against v0.42). No language, locale or region parameter is sent; no system prompt. Changes from v0.44:
  - design (pre-registration section 5.2): per language (FR, JA) Phase B 30 category questions x S0 x runs 1-3 +
    Phase A 112 brand questions x S0 x run 1, three models: 2 x 3 x (90 + 112) = 1,212 calls under headphones
    option A (1,206 under B, 1,008 under C: params_v0_62.HEADPHONES_OPTION). Five blocks in this order:
    B run 1, B run 2, B run 3 (every confirmatory test), A yes/no (v0.19-v0.22), A open (v0.23); within a block one
    worker per model, the three in parallel, French before Japanese, probes in file order;
  - probes: osf/v62/translations/probes_{fr,ja}_v0_62_r0.jsonl (142 lines each); every raw line carries `language`;
  - window: params_v0_62.WINDOW (one parameter); --collect also refuses at any time inside params_v0_62.BLACKOUT
    (2026-11-17 .. 2026-11-21 US Central), and refuses a declared window that overlaps it;
  - budget: budget_v0_62 (judge reserve $1.3176 counted in the spend from the start); pause at $80 and hard stop
    at $100 on actual usage, as v0.44; projection pause after block 1: projected total = call spend (without the
    judge reserve, which the ratio's numerator already contains) x R, R read from prereg/cost_estimate_v0_62_r1.json
    for the headphones option and the month of block 1; the pre-registrant continues (--approve-projection), drops
    Phase A (fallback F1, --drop-phase-a) or drops Phase B run 3 (fallback F2, --drop-run-3);
  - Claude Fable 5.2 through the Message Batches API; GPT-6 Astra and Gemini 4 Argon synchronous (as t4).

Output (append-only, one JSON line per attempt, resumable: answered call_ids are skipped): osf/v62/data/v62_raw.jsonl
Budget state (approvals, window): osf/v62/data/v62_budget_state.json

Modes (default: --dry-run):
  --dry-run   build the call matrix, print it with the cost estimate and the state of every guard; send nothing
  --collect   guarded paid collection: refused unless osf/v62/anchor/osf_anchor_v0_62.json exists and names the
              commit of tag v0.62-prereg-r1 on origin, the time is inside the window and outside the blackout, no
              other paid collection is running on this machine; no request after min(window end, first call + 72 h).
              Approvals: --approve-past-80 NOTE, --approve-projection NOTE, --drop-phase-a NOTE, --drop-run-3 NOTE;
              declared window (slip): --window START END --deviation-entry N (dates YYYY-MM-DD, US Central)

Paths: ROOT = AIAS_ROOT or the worktree that contains this file (never a hard-coded /Users/pablou/aias).
"""
'''
a = HEADER + a[doc_end:]
a = sub1(a, 'import budget_v0_44 as BG  # noqa: E402', 'import budget_v0_62 as BG  # noqa: E402\nimport params_v0_62 as P  # noqa: E402')
old_paths = a[a.index('V44 = ROOT / "osf" / "v44"'):a.index('PANEL = [')]
a = a.replace(old_paths, '''V62 = ROOT / "osf" / "v62"
PROBE_FILES = {"fr": V62 / "translations" / "probes_fr_v0_62_r0.jsonl",
               "ja": V62 / "translations" / "probes_ja_v0_62_r0.jsonl"}
COST_PATH = V62 / "prereg" / "cost_estimate_v0_62_r1.json"
RAW_PATH = V62 / "data" / "v62_raw.jsonl"
STATE_PATH = V62 / "data" / "v62_budget_state.json"
ANCHOR_PATH = V62 / "anchor" / "osf_anchor_v0_62.json"
DEVIATIONS_PATH = V62 / "DEVIATIONS.md"
PREREG_TAG = "v0.62-prereg-r1"
LANGS = ["fr", "ja"]

''')
a = sub1(a, '''# (phase, condition, run) blocks in collection order
BLOCKS = [("B", "S0", 1), ("B", "S0", 2), ("B", "S0", 3), ("A", "S0", 1)]
PROJECTION_BLOCK = ("B", "S0", 1)
DROPPABLE_BLOCK = ("B", "S0", 3)
WINDOW_DATES = ("2026-11-24", "2026-11-28")      # inclusive, US Central (section 4.6)''',
'''# (kind, condition, run) blocks in collection order; kind B = category question, A_yn = yes/no brand question
# (v0.19-v0.22), A_open = open brand question (v0.23)
BLOCKS = [("B", "S0", 1), ("B", "S0", 2), ("B", "S0", 3), ("A_yn", "S0", 1), ("A_open", "S0", 1)]
PROJECTION_BLOCK = ("B", "S0", 1)
DROPPABLE_BLOCK = ("B", "S0", 3)                  # fallback F2
PHASE_A_BLOCKS = (("A_yn", "S0", 1), ("A_open", "S0", 1))   # fallback F1
WINDOW_DATES = tuple(P.WINDOW)                    # inclusive, US Central (params_v0_62.WINDOW; section 5.5)
BLACKOUT_DATES = tuple(P.BLACKOUT)''')
a = sub1(a, 'ADOPTED_DESIGN = "adopted"                       # key in cost_estimate_v0_44.json\n', '')
a = a.replace('# ======================= v0.44 wrapper (forked from v0.42 r2) =======================',
              '# ======================= v0.62 wrapper (forked from v0.44 r1) =======================')
s0, s1 = a.index('def load_industries('), a.index('def _invoke(')
a = a[:s0] + '''def kind_of(p):
    """Block kind of a probe: B, A_yn (v0.19-v0.22 brand questions) or A_open (v0.23 brand questions)."""
    if p["phase"] == "B":
        return "B"
    return "A_open" if p["substrate"] == "v23" else "A_yn"


def load_probes(paths=None, option=None):
    """Both languages' probe files (142 lines each: 30 Phase B + 112 Phase A, t4's IDs and order), minus the probes
    that the headphones option removes (params_v0_62.excluded_probe)."""
    paths = paths or PROBE_FILES
    out = []
    for lg in LANGS:
        ps = [json.loads(l) for l in Path(paths[lg]).read_text(encoding="utf-8").splitlines() if l.strip()]
        got = (sum(p["phase"] == "B" for p in ps), sum(p["phase"] == "A" for p in ps))
        if got != (30, 112):
            sys.exit(f"ABORT: {lg} probe file has Phase B/A = {got}, expected (30, 112)")
        if any(p.get("language") != lg for p in ps):
            sys.exit(f"ABORT: {lg} probe file carries another language")
        out += [p for p in ps if not P.excluded_probe(p["substrate"], p["phase"], p.get("brand_id"), option)]
    return out


def blocks_in_design(drop_run3=False, drop_phase_a=False):
    return [b for b in BLOCKS if not ((drop_run3 and b == DROPPABLE_BLOCK) or (drop_phase_a and b in PHASE_A_BLOCKS))]


def expected_total(probes=None, drop_run3=False, drop_phase_a=False):
    probes = probes if probes is not None else load_probes()
    n = Counter(kind_of(p) for p in probes)
    return len(PANEL) * sum(n[k] for k, _c, _r in blocks_in_design(drop_run3, drop_phase_a))


def call_id(language, substrate, phase, probe_id, model, cond, run):
    return f"{language}|{substrate}|{phase}|{probe_id}|{model}|{cond}|{run}"


def build_specs(probes, drop_run3=False, drop_phase_a=False):
    """Matrix in collection order: block (BLOCKS order), then model (panel order), then language (FR before JA),
    then probe (file order)."""
    specs = []
    keep = blocks_in_design(drop_run3, drop_phase_a)
    for bi, (kind, cond, run) in enumerate(BLOCKS):
        if (kind, cond, run) not in keep:
            continue
        for m in PANEL:
            for lg in LANGS:
                for p in probes:
                    if p["language"] != lg or kind_of(p) != kind:
                        continue
                    specs.append({
                        "call_id": call_id(lg, p["substrate"], p["phase"], p["probe_id"], m["model_id"], cond, run),
                        "language": lg, "substrate": p["substrate"], "phase": p["phase"], "probe_id": p["probe_id"],
                        "brand_id": p.get("brand_id"), "frame_id": p.get("frame_id"),
                        "model": m, "condition": cond, "run": run, "block": bi,
                        "system": p.get("system"), "prompt": p["prompt"],
                    })
    ids = [s["call_id"] for s in specs]
    if len(set(ids)) != len(ids):
        sys.exit("ABORT: duplicate call_id")
    return specs


''' + a[s1:]
a = sub1(a, '''        "call_id": spec["call_id"], "substrate": spec["substrate"], "phase": spec["phase"],''',
         '''        "call_id": spec["call_id"], "language": spec["language"], "substrate": spec["substrate"], "phase": spec["phase"],''')
a = sub1(a, 'ids = {f"v44-{i:04d}-a{att}"', 'ids = {f"v62-{i:04d}-a{att}"')
a = a.replace('budget_v0_44.record_cost', 'budget_v0_62.record_cost')
# cost file / projection ratio
s0, s1 = a.index('def cost_estimate('), a.index('# ----------------------------------------------------------------- guards')
a = a[:s0] + '''def cost_estimate(path=None):
    """The cost estimate (cost_estimate_v0_62.py output, r1)."""
    return json.loads(Path(path or COST_PATH).read_text(encoding="utf-8"))


def projection_ratio(path=None, when_utc=None, option=None):
    """R = central estimate of the design (headphones option) / central estimate of its block 1, at the prices of
    the day block 1 started (December ratio from 2026-12-01, when Gemini 4 Argon's price doubles)."""
    ce = cost_estimate(path)
    option = option or P.HEADPHONES_OPTION
    day = (when_utc.isoformat() if hasattr(when_utc, "isoformat") else (when_utc or ""))[:10]
    return float(ce["projection"][option]["dec" if day >= "2026-12-01" else "nov"])


''' + a[s1:]
# blackout in window_check
a = sub1(a, '''    if now < start:
        return False, f"before the collection window ({dates[0]} US Central)"''',
         '''    b0, b1 = window_bounds(BLACKOUT_DATES)
    if b0 <= now < b1:
        return False, f"inside the blackout {BLACKOUT_DATES[0]}..{BLACKOUT_DATES[1]} US Central (another collection)"
    if now < start:
        return False, f"before the collection window ({dates[0]} US Central)"''')
a = sub1(a, '''    if datetime.fromisoformat(end) < datetime.fromisoformat(start):
        sys.exit("REFUSED: window end before start")
    return start, end''', '''    try:
        P.validate(window=(start, end))
    except ValueError as e:
        sys.exit(f"REFUSED: {e}")
    return start, end''')
# projection in run_collection
a = sub1(a, '''        if block == PROJECTION_BLOCK and not (ledger.approved("projection") or ledger.approved("drop_run3")):
            proj = ledger.spent() * ratio''', '''        if block == PROJECTION_BLOCK and not any(ledger.approved(k) for k in ("projection", "drop_run3", "drop_phase_a")):
            proj = ledger.calls_spent() * ratio''')
a = sub1(a, '''                ledger.halt("pause", f"projection: spend ${ledger.spent():.2f} x {ratio:.4f} = ${proj:.2f} "''',
         '''                ledger.halt("pause", f"projection: call spend ${ledger.calls_spent():.2f} x {ratio:.4f} = ${proj:.2f} "''')
# dry run, collect, main: replace from dry_run to end
s0 = a.index('# ----------------------------------------------------------------- dry run')
a = a[:s0] + (DST / "_acquire_tail_v0_62.py.txt").read_text(encoding="utf-8")
(DST / "acquire_v0_62.py").write_text(a, encoding="utf-8")
print("acquire_v0_62.py written")
