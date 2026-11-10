"""One-off: PRE_REGISTRATION_v0_62_DRAFT_r1.md = r0 + the r1-draft changes (listed in its 'Changes from r0'); fix 88 -> 96."""
from pathlib import Path

V = Path(__file__).resolve().parents[1]
s = (V / "prereg/PRE_REGISTRATION_v0_62_DRAFT_r0.md").read_text(encoding="utf-8")


def sub1(old, new):
    global s
    assert s.count(old) == 1, (old[:70], s.count(old))
    s = s.replace(old, new)


sub1("Pre-Registration v0.62 (revision r0, DRAFT for the pre-registrant's first look)",
     "Pre-Registration v0.62 (revision r1, WORKING DRAFT — not locked, not final)")
sub1("**Status:** r0 draft, written 2026-11-10 by the programme runner (lane 6) for the pre-registrant's first look.",
     "**Status:** r1 working draft (2026-11-10, programme runner lane 9), built on r0 (lane 6, same day); every change is listed in §11 \"Changes from r0\". Scripts and tests now exist (§5, §7); the pre-registrant's three choices are still open and are each one parameter in `osf/v62/scripts/params_v0_62.py` (§9). r0 status text follows:")
sub1("All figures: `python3 osf/v62/scripts/cost_estimate_v0_62.py`.",
     "All figures: `python3 osf/v62/scripts/cost_estimate_v0_62.py` (r1 output `osf/v62/prereg/cost_estimate_v0_62_r1.txt`).")
sub1("(Cells rounded; totals from unrounded values; `cost_estimate_v0_62_r0.txt`.)",
     "(Cells rounded; totals from unrounded values; `cost_estimate_v0_62_r1.txt`. The by-phase lines of that file now list the judge reserve as a line of its own: Phase B + Phase A yes/no + Phase A open = $33.92 + $15.78 + $9.04 = $58.74 at December prices, plus the $1.32 reserve = $60.06; high $79.55 + $43.84 + $21.21 = $144.60 + $1.32 = $145.92. r0's printout omitted the reserve line, which made the phase lines look $1.32 short.)")
sub1("Under it the guard ends the collection inside Phase A, after blocks 1–3 are complete ($71.29 November; $79.55 December, just under the pause): no confirmatory test is lost, only recognition descriptives.",
     "Under it the guard ends the collection inside Phase A, after blocks 1–3 are complete: no confirmatory test is lost, only recognition descriptives. **Correction (r1):** the guard counts the $1.32 judge reserve in the spend from the first call (§6.5), so at the end of blocks 1–3 the guard's spend is $72.61 at November prices but **$80.87 at December prices** (high scenario): at December prices the $80 pause is reached inside block 3, and the last Phase B calls wait for the pre-registrant's `--approve-past-80`. They are paused, not lost; the hard stop ($100) is not near. At the expected cost the figure is $31.88 / $35.24.")
sub1("3. **Projection pause:** after block 1, projected total = actual spend × 5.3413",
     "3. **Projection pause:** after block 1, projected total = actual call spend (r1: without the judge reserve, which the ratio's numerator already contains) × 5.3413")
sub1("- **S-Headphones.** Every test without the v0.19 category: 88 units (DEVIATIONS Entry 0).",
     "- **S-Headphones.** Every test without the v0.19 category: 96 units (r1 correction: r0 said 88; 112 − 16 = 96) (DEVIATIONS Entry 0).")
sub1("Every alias is a **draft from the runner's knowledge**, to be checked against each brand's Japanese or French site or packaging and at native review before r1; the check record (alias, source, date) is part of the lock.",
     "Every alias was a draft from the runner's knowledge in r0. **r1:** `brand_aliases_v0_62_r1.csv` carries, per unit, the check status, the source opened (the brand's Japanese site and/or the Japanese Wikipedia article linked from the English one) and the access date (`check_aliases_v0_62.py` → `alias_check_v0_62_r1.csv`, 2026-11-10): 51 units confirmed, 4 partly confirmed, 55 unconfirmed (no reachable source showed the form), 1 without alias, 1 changed from a source (Lucid: ルシード added). Unconfirmed aliases stay in force (they are spelling transcriptions) and are flagged for the native review. Four more rows changed for **parity with the certified English matchers**, which count only the full registry string (v0.20–v0.22 `detect_mention`; e.g. \"Mercedes-Benz\", \"Milani Cosmetics\"): an alias may not be looser than the English rule, so bare ベンツ and bare クレ・ド・ポー are dropped, ミラニ becomes ミラニ・コスメティックス, and the company forms ニッカウヰスキー / ニッカウイスキー are added for Nikka (v0.23's English rule counts \"Nikka Whisky\"). The same parity reason settles r0's open note on bare ディオール / シャネル / ロレアル: not aliases, because the English rule does not count bare \"Dior\", \"Chanel\" or \"L'Oréal\". The French unaccented forms are redundant with the certified matchers (which strip accents) and harmless.")
sub1("1. Unicode NFC; typographic apostrophes → '; no-break and narrow no-break spaces → space; URLs removed (`strip_urls`, byte copy of v0.42's).",
     "1. Unicode NFC; full-width Latin letters, digits and signs and half-width katakana → their ordinary forms (NFKC, r1: ＢＭＷ → BMW, ﾄﾖﾀ → トヨタ); ideographic space → space; typographic apostrophes → '; no-break and narrow no-break spaces → space; URLs removed (`strip_urls`, byte copy of v0.42's).")
sub1("so that ソニー matches in ソニーの but コス does not match inside コスメ or コスプレ. Kanji aliases match as written.",
     "so that ソニー matches in ソニーの but コス does not match inside コスメ or コスプレ. Kanji aliases match as written. r1: the two loan words of registry names match in both common spellings, ビューティ / ビューティー and コスメティクス / コスメティックス, and the middle dot · is a separator.")
sub1("Coder `osf/v62/scripts/code_v0_62.py` (r1), which imports v0.42's functions unchanged and adds only the pre-step and the answer-word mapping.",
     "Coder `osf/v62/scripts/code_v0_62.py` (r1), which adds only the pre-step and the answer-word mapping and writes prepared copies of the raw answers per language; v0.42's coder (`code_t4_v0_42.py`) then runs unchanged on each prepared copy (r1: as a separate process, because the v0.62 branch does not contain osf/v41–v42 and v0.42's coder re-executes itself with its own ROOT shim).")
sub1("It imports the π̂ and φ kernels from `score_v0_42.py` (which takes them from `score_v41.py`), the centred ρ and permutation from v0.44's scorer, and, for §2.4, `score_v1_14.modal_position`.",
     "r1 draft: it carries transcriptions of the π̂ and φ kernels (`score_v41.phi_m`, `score_v0_42.pi_hat` / `phi_panel`) and of v0.44's centred ρ and permutation, because the v0.62 branch does not contain osf/v41–v42; gate P1 must show that the transcriptions reproduce v0.42's English t₄ values exactly before the lock, or the v0.42 scripts are merged and imported instead. R\\* values (§2.4) are an input from v1.14's own scorer.")
sub1("Settled in r0 by the runner (can be overruled):",
     "**Each of questions 1–3 is one parameter (r1):** `HEADPHONES_OPTION = \"A\"` and `WINDOW = (\"2026-11-29\", \"2026-12-02\")` in `osf/v62/scripts/params_v0_62.py` (read by the acquisition, cost, coding and scoring scripts; a window touching 2026-11-17..21 is refused), and the native review changes only the translation files. The pre-registrant's answer becomes a one-line edit plus a change-log line.\nSettled in r0 by the runner (can be overruled):")
s = s.replace("**Change log**\n\n- 2026-11-10, r0 written (no earlier revision).",
"""**Change log**

- 2026-11-10, r0 written (no earlier revision).
- 2026-11-10, r1 working draft (lane 9): see "Changes from r0".

### Changes from r0 (r1 working draft, 2026-11-10)

1. Scripts written, with unittest tests on local fakes (no network, no model): `acquire_v0_62.py` (dry run by default; fork of v0.44's, call functions byte-copied from v0.42), `budget_v0_62.py`, `params_v0_62.py`, `code_v0_62.py`, `score_v0_62.py`, `check_aliases_v0_62.py`, `make_alias_table_r1_v0_62.py`; tests `osf/v62/scripts/tests/` (48 tests).
2. The three open choices are parameters: headphones option and window in `params_v0_62.py`; option B removes the Denon Phase A probe (1,206 calls), option C the v0.19 category (1,008 calls); costs per option in `cost_estimate_v0_62_r1.txt`.
3. Collection blocks: Phase A is split into block 4 (yes/no) and block 5 (open), as r0's table already listed; fallback F1 is `--drop-phase-a`, F2 `--drop-run-3`.
4. Cost script reconciled (§6.3): the by-phase lines omitted the $1.32 judge reserve; it is now printed as its own line with a sum check. No total changes.
5. Correction (§6.3): with the judge reserve counted from the first call, the December high scenario reaches the $80 pause inside block 3 ($80.87 at the end of blocks 1–3); r0 said blocks 1–3 stay under $80 at December prices. November: $72.61.
6. Projection pause (§6.5): computed on the call spend without the judge reserve (the ratio's numerator already contains it); thresholds unchanged ($14.98 / $15.06).
7. Correction (§7.5, DEVIATIONS Entry 0): without the headphones category 96 units remain, not 88.
8. Alias table r1 (§4.2): check record with sources and dates; Lucid gains ルシード; parity changes for Mercedes-Benz, Clé de Peau Beauté, Milani Cosmetics; Nikka gains ニッカウヰスキー / ニッカウイスキー.
9. Pre-step (§4.3): full-width and half-width normalisation; ビューティ(ー) and コスメティ(ッ)クス spelling variants; · as a separator.
10. Coding and scoring architecture (§7.1, §7.2): v0.42's coder runs as a separate process on prepared copies; the scorer carries transcribed kernels pending gate P1 (or a merge of the v0.42 scripts).
11. Open issue for the lock (not changed): the pre-step maps typographic apostrophes to ', which the certified English matchers do not; gate P2 (pre-step inert on English) will fail on any English t₄ answer that writes a registry name with ’ (e.g. Paula’s Choice, L’Oréal Paris). Either P2 is read on the mention cells after the same mapping is applied to English, or the mapping is dropped (French answers, which commonly write L’Oréal, would then under-match).
""")
(V / "prereg/PRE_REGISTRATION_v0_62_DRAFT_r1.md").write_text(s, encoding="utf-8")

d = (V / "DEVIATIONS.md").read_text(encoding="utf-8")
assert d.count("**S-Headphones** (88 units") == 1 and d.count("runs on 88 units") == 1
d = d.replace("**S-Headphones** (88 units", "**S-Headphones** (96 units; r1 correction of r0's 88")
d = d.replace("runs on 88 units", "runs on 96 units (r1 correction of r0's 88)")
(V / "DEVIATIONS.md").write_text(d, encoding="utf-8")
p = (V / "scripts/params_v0_62.py").read_text(encoding="utf-8").replace("tests on 88 units", "tests on 96 units")
(V / "scripts/params_v0_62.py").write_text(p, encoding="utf-8")
print("r1 text written; DEVIATIONS and params corrected")
