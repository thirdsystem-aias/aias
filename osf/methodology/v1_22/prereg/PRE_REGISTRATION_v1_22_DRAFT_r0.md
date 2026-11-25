# AIAS v1.22 — Grounding, Paper B: the unmet gate conditions re-tested on t₅, retest stability, structured data, phantom brands, identity load and typology

AIAS™ Measurement Program — Third System™. Pre-registration **DRAFT r0** (2026-11-25, about 0:10–1:30 am CT), written by a lane of the AIAS research runner on Pablo's "Ok" of Tue 2026-11-24, 11:15 pm CT (prepare Grounding Paper B so that, if he chooses it, it can lock before t₅ collects). **Not locked. Not sent to OSF. Not pushed.** No t₅ answer exists (t₅'s first call is not before Thu 2026-12-03 06:00 UTC, v0.45 §4.6). No model was called, nothing was spent, and no statistic of this study was computed on real data while drafting (§12 lists everything read).

**Study number.** `v1.22` is a working number, proposed (Call C2). On 2026-11-25 ~0:20 am CT the repository had tags up to `v1.21-prereg-r1` and no local or remote branch or tag matching `v1.22*` (`git branch -a`, `git tag -l "v1.*"`, `git for-each-ref`); `Try system book/CLAUDE.md`, `STATUS.md`, `aias_roadmap_ssot.md` and the Claude project docs (search "v1.22") do not mention v1.22. Not checked: OSF `methodology/v1_22` (this lane made no OSF call), and whether another lane has reserved the number since (check at r1).

---

## For Pablo: what this is, in plain words

Grounding Paper A (v1.13, published Sun 11/22) built the Grounding score G\* — the share of a brand's search-on AI answers whose retrieved sources include the brand's own website — and ran the separability gate. The gate came out **MARGINAL**, not PASS: G\* was clearly separate from Consistency (H2 CONFIRMED), but its link with Presence sat between the bands (H1 MARGINAL: ρ_w 0.307 and 0.395, the bar is ≤ 0.30 on both), and run-to-run reliability could not be computed because too few brands had enough grounded answers in each single run (H3 UNDETERMINED: 0 of 3 run pairs reached 30 brands). Under v1.13 §3 a MARGINAL gate means **Paper B proceeds only on your recorded decision**, and Paper A's discussion (§4) says the condition that was not met must be Paper B's first confirmatory test.

This draft does exactly that, with **no paid model call of its own**: t₅ (v0.45, locked, collects Dec 3–6) repeats t₄'s search-on questions on the same three models, three runs. So Paper B can

1. **re-test the two unmet gate conditions on fresh answers** — Presence separability on t₅ (HB1) and reliability, both as a t₄ → t₅ retest of G\* (HB2, the same test v0.45 §2.6 owns unless a Grounding Paper B pre-registers it before t₅'s answers exist) and as Paper A's H3 on t₅'s runs (HB3) — plus Consistency on t₅ (HB4), and decide, by a rule fixed now (§3.5), whether Grounding's gate is completed (PASS), stays MARGINAL, or fails;
2. run the four structure studies the Full study list assigns to Grounding Paper B (#44 rich vs sparse structured data, #46 phantom brands, #47 identity load, #48 typology) on t₄ + t₅ pooled, and #45 (stability of cited sources t₄ → t₅ → t₆) with the t₆ part pre-registered now and run when t₆ exists.

**Why lock before Dec 3.** v0.45 §2.6 says the Grounding retest is v0.45's own component leg "if the leg is active; if Grounding Paper B pre-registers the same retest before t₅'s answers exist, its verdict is carried instead". Locking before t₅'s first call keeps the retest and the t₅ re-tests of H1/H3 genuinely confirmatory.

**If you say no** (B does not run on MARGINAL): nothing here runs; G\* stays a candidate measure reported beside Presence and Consistency (v1.13 §4), as Ranking was after its MARGINAL, and v0.45 computes its own Grounding leg as written.

### Calls for Pablo (each with a recommended answer; §15 has the reasons)

| # | Call | Recommended |
|---|---|---|
| C1 | Does Grounding Paper B proceed after Paper A's MARGINAL gate? (v1.13 §3: your dated, written decision) | **Yes**, recorded in `anchor/pablo_decision_paper_B.json` and DEVIATIONS; every verdict labelled "conditional on a MARGINAL Paper A gate (H1 MARGINAL, H3 UNDETERMINED)" |
| C2 | Study number | **v1.22** (next free); alternative `v1.13-paperB` (the v1.11-paperB precedent) |
| C3 | May Paper B complete the gate (PASS → Grounding eligible for a release), by the rule in §3.5? | **Yes**, as drafted; otherwise Paper B only reports, and Grounding stays MARGINAL whatever t₅ shows |
| C4 | Make HB2 the identical test to v0.45 §2.6's Grounding leg (statistic, bands, floor, seed 450046), so v0.45 carries this verdict ("one test, one owner") | **Yes** |
| C5 | If v0.45's guard stops t₅'s search-on runs 2–3 (projection pause; v0.45 §4.5 puts that at the high cost estimate), fund them under this study's own $100 cap? | **Yes, contingent**: same probes, models, call policy, inside t₅'s window, separate ledger, pause $80, hard stop $100 (v0.45's own estimate for the two runs: $36.77 central, about $80.19 high) |
| C6 | v0.40's search-on arm (US airlines and retail banks; one run; a registry with no own-domain list) | **Descriptive appendix only**, after v0.40 is public (launch Dec 14); no verdict, no G\* |
| C7 | Structure studies (#44, #46, #47) on G\* pooled over t₄ + t₅ (six runs) rather than one wave | **Yes** (Paper A rated 42 of 112 units on three runs; the structure tests have floors of 30–45 units) |
| C8 | Phantom set for #46 | **F, the frozen recall-floor flags** (57 of 112; v1.19's roster, SHA-256 `9b67e892…`), as Coverage Paper B; the five defunct car brands descriptive only (no own domain) |
| C9 | Bands for #47 (mean within-brand difference ≥ 5 points CONFIRMED, < 2 points FALSIFIED) and #48 (v1.19's 0.20 / 0.10) | **Accept as proposed**, subject to the r1 synthetic dry run showing each test returns a built effect (§11) |
| C10 | Lock timing | **24 h after you receive r1, and in any case before Thu 12/3 06:00 UTC (Wed 12/2 midnight CT)**; target Mon 11/30 or Tue 12/1, after your C1 decision (~11/29) |
| C11 | A t₅ re-audit of the brands' sites (Part II protocol, home page plus up to two pages; Dec 7–10, after t₅'s collection, no paid calls) | **Yes**, sensitivity and stability only |
| C12 | Pre-register the t₆ legs of #45 now (Stage 2, run when t₆ exists, ~Feb 2027) | **Yes** |

---

## 0. Status, scope and lineage

| Field | Value |
|---|---|
| PHASE_ID | **v1.22** (working number; C2) |
| PHASE_TYPE | methodology study: re-analysis of archived t₄ (v0.42) and of t₅ (v0.45) once collected and scored; new public web data (a t₅ re-audit, C11); **no paid model call of its own** (C5 is the only contingent spend) |
| Branch | `v1.22`, from `v1.13-paper` @ `32b85a5` (the last commit of Grounding Paper A, which holds v1.13's locked scorer, frozen lists, postlock scripts and paper; the way v1.19 was based on v1.12's last commit) |
| Worktree | `~/aias/_worktrees/v1.22` |
| Status | DRAFT r0, local commit only; not pushed, not on OSF, not sent |
| Studies (Full study list, tab "📋 Full study list", read 2026-11-25) | **#44** Rich vs sparse structured data: does it show? · **#45** Stability of cited sources over time (t4 → t5 → t6) · **#46** Phantom brands: grounding signature · **#47** Identity-load moderator · **#48** Grounding typology / regimes — each "Grounding Paper B", est. Mar. (#41–#43 are Paper A, done Sun 11/22; #43's row reads "gate MARGINAL".) Plus the gate re-tests that v1.13 §4 requires as the first confirmatory test (HB1–HB4). |
| Not in scope | Model-version and prompt-phrasing robustness (named generically for Paper B's in `CLAUDE.md`, "Plan for speed"): the Full study list assigns no such Grounding study; they would need new collections and their own pre-registration. Sentiment separability (v1.13 H5 was INACTIVE, so it is not inherited; v1.13 §8 inherits only pending active legs). Ranking (closed into Presence, roadmap Nov 12): R\* appears only as a descriptive column. |
| Locks on | C1 decision recorded → r1 (dry run, tests, Calls settled) → Pablo receives r1 → 24 h (or his waiver) → `prereg/LOCK_MANIFEST_v1_22.sha256` → commit → tag `v1.22-prereg-r1` → push → OSF `methodology/v1_22/` (`prereg/`, `anchor/`, `scripts/`, `dryrun/`; SHA-256 verified with `osf_deposit.py`) → `anchor/osf_anchor_v1_22.json`. **All before t₅'s first call, Thu 2026-12-03 06:00 UTC** (§10). |

**Lineage.** v1.13 §8 ("What Paper B inherits", locked): "Pre-registered separately, only after PASS (or MARGINAL with Pablo's recorded decision): the locked parser, `source_classes_v1_13.md`, D_b, `score_v1_13.py` and tests; per-answer source tables (SHA-256 pinned); **source-coverage stability over waves** (t4 → v0.40 S1 arm, Nov 17–21, US airlines and retail banks → t5 → t6, each re-classified with the frozen lists); **phantom-brand grounding** (what answers retrieve when they name a registry phantom brand; registry phantom flags); **identity load** (OMNI cultural vs category frames); **typology** (G\* × P × C\* × R\* profiles); H7 if Part II was not collected in time; any active H4–H6 whose score did not exist by Stage C2; re-audits of structured data at t5/t6; v0.40's brands added to the audit if v0.40's pre-registration declares its search record." Paper A §6 repeats it and §4 adds: "a second paper proceeds only on the pre-registrant's recorded decision, with the condition that was not met as its first confirmatory test." H7 was collected in time but UNDETERMINED (26 brands, floor 30); H6 was computed at Stage C2 (MARGINAL); no H4–H6 leg is pending. v0.45 §1 and §2.6 name this study as the owner of the Grounding retest if it locks before t₅'s answers exist.

## 1. Conditionality on Paper A's gate (binding)

Paper A's verdict is `gate.verdict` of `osf/methodology/v1_13/v1_13_verdicts.json` as deposited (MARGINAL; legs H1 MARGINAL, H2 CONFIRMED, H3 UNDETERMINED; Stage C2 re-issued it unchanged on 2026-11-22 18:09 UTC, paper §3.5). The scorer reads it and nothing else decides:

| Paper A verdict | v1.22 |
|---|---|
| MARGINAL | **Runs only on Pablo's recorded decision** (v1.13 §3): dated written text, logged in `anchor/DEVIATIONS.md` and recorded for the scorer in `anchor/pablo_decision_paper_B.json` (`{"go": true, "date": …, "text": …}`; undated or unworded does not count). Every verdict carries "conditional on a MARGINAL Paper A gate (H1 MARGINAL, H3 UNDETERMINED)". Without the record: NOT RUN (pending); `outputs/v122_not_run.json` holds the verdict read and its SHA-256, no statistic. With `{"go": false}`: NOT RUN (declined), same record. |
| anything else, or no verdict file | Refused (no output). (PASS cannot occur: the verdict is final.) |

## 2. Data and shared definitions

All definitions are v1.13's, imported from its locked scorer `osf/methodology/v1_13/scripts/score_v1_13.py` (SHA-256 `fee2e553…a8641`, equal to `LOCK_MANIFEST_v1_13.sha256` and to the file at `32b85a5`), never copied or edited: source parsing and classes (`source_classes_v1_13.md`, `dbc8b9ef…`), own domains D_b (`brand_domains_v1_13.csv`, `38198fdf…`), answers, comparators, G\*, floors, ρ_w, permutation and bootstrap, separability and reliability verdicts, MQ checks.

- **Waves.** t₄ = v0.42's raw record at tag `v0.42-acquisition-locked`, coded tables at v0.42's scored commit (as v1.13 Stage C1 read them). t₅ = v0.45's raw record at tag `v0.45-acquisition-locked` and its coded tables and brand table at v0.45's scored commit (v0.45 §4.6 steps 4–6; coded by v0.42's certified coder, v0.45 §5.1). t₆ = the third wave on the newest-models panel (v0.45 §1: about three months after t₄; target 2027-02-12 per v0.42), under its own pre-registration; used only in Stage 2 (§3.6 #45).
- **Answers.** Per wave, v1.13 §2.1 unchanged: answered search-on (S1) Phase B category answers of panel N3 (Claude Fable 5.2, GPT-6 Astra, Gemini 4 Argon), 30 questions × 3 runs per model; evidence field `sources`. A model dropped from a wave's S1 under v0.42 §5.4 (fewer than 90% of its 90 S1 calls answered) or by v1.13's MQ2/MQ4 rules leaves that wave's G\*; tests then run on the remaining models and are labelled "reduced panel"; fewer than two models in S1 at a wave → every test that needs that wave is NOT MEASURED.
- **G\*_w** (per wave w ∈ {t₄, t₅, t₆}): v1.13 §2.4 on wave w's three runs (rated iff g_b ≥ 6 and b has a D_b). G\*_t₄ is Paper A's G\* (parity gate B-P1, §9).
- **G\*_pool**: the same formula over the six runs of t₄ and t₅ together (o_b and g_b summed over both waves), rated iff g_b ≥ 6 and D_b (C7). A new estimand, labelled as such; used only by #44, #46, #47 and #48b.
- **P and C\* at t₅**: P_S0,t₅, P_S1,t₅ and C\*_S0,t₅, C\*_S1,t₅ by v1.13 §2.2's formulas on t₅'s brand table (π̂ and φ from v0.45's scored output; C_P/3 from t₅'s single S0 recognition run, v0.23 units coded by v0.45's successor judge after its J1 parity, v0.45 §5.1). If v0.45 leaves the 24 v0.23 units out of P (J1 failed), they leave HB1 and the label says so.
- **ρ_w, floors, draws.** v1.13 §2.6: within-category average ranks centred on the category mean, Pearson pooled; categories with ≥ 5 units; n floor 30; 10,000 permutations (within category); 2,000-draw 90% bootstrap intervals (report only). HB2 alone uses v0.45 §2.1's conventions (10,000 bootstrap resamples, 95% interval; one-sided permutation), so that it is v0.45's test (C4).
- **Phantom set F** (#46): the recall-floor flags frozen in v1.19's `prereg/phantom_roster_v1_19.csv` (at tag `v1.19-prereg-r1`, commit `4bc4ce4`; SHA-256 `9b67e89231f4…873cb`; 112 rows; column `recall_floor_flag_F`): mean recall below 1.0 across the six legacy models at t₁ (v0.31 archive; v0.35's FLOOR). Imported by hash, not rebuilt. Set D (`defunct_D`: Pontiac, Oldsmobile, Plymouth, Mercury, Saturn) has no own domain (v1.13 §2.3), so it is never rated; descriptive only.
- **Channels** (#47): each Phase B question's `channel` field in `osf/v42/prereg/probes_v0_42.jsonl` (t₅'s probe file is byte-identical, v0.45 MC_Probe_Parity): category-anchored (`category_anchored`, `R_cat`) versus cultural (`cultural_footprint`, `R_cult`); three of each per category. The exact label strings per substrate are mapped in the scorer and unit-tested against the probe file (r1).
- **Identity load IL_b** (#47b): v1.19 D6's definition, t₄ N3 S0: IL_b = k_{b,cult}/n_{cult} − k_{b,cat}/n_{cat}; eligible iff 0 < π̂_b < 1; construct-valid on the two-channel trio v0.20, v0.21, v0.22 only (v0.37; v1.19 §6.1).
- **Source-class profile** (#48): for brand b at wave w, over its grounded answers, the mean share of the answer's distinct resolved domains in each of six classes — brand-owned, reference, forum/UGC, news, review/editorial, retailer (v1.13 `source_mix`; "other" and "unresolved" are left out of the profile and their share is reported) — each centred on its category mean: x_{b,w} ∈ ℝ⁶.
- **Seeds.** 122001 (HB1), 450046 (HB2; C4 — v0.45's component-leg seed), 122003 (HB3), 122004 (HB4), 122441 (HB44), 122442 (HB44b), 122451 (HB45_t5t6), 122452 (HB45_t4t6), 122461 (HB46), 122462 (HB46b), 122471 (HB47), 122472 (HB47b), 122481 (HB48), 122482 / 122483 (HB48b full / residual arms), 122490–122494 (dry-run worlds). Bootstrap streams: seed + 500000.
- **α** = 0.05 per test; no multiplicity correction (programme convention); every verdict is reported whatever it is.

## 3. Hypotheses, exact tests and decision rules

### 3.1 HB1_Sep_Presence_t5 — PRIMARY (the first unmet condition, H1)

- **Statement.** On fresh answers, G\* is separable from Presence in both conditions.
- **Statistic.** ρ_w(G\*_t₅, P_S1,t₅) and ρ_w(G\*_t₅, P_S0,t₅) over t₅-rated units; two-sided permutation p (G\* permuted within category), seed 122001; 90% bootstrap intervals.
- **Verdict (v1.13 §3's H1 rule, imported `sep_verdict`, in this order).** MQ5 failed on t₅ → UNDETERMINED; a leg with ≥ 30 units and |ρ_w| ≥ 0.50 → FALSIFIED; a leg below 30 units → UNDETERMINED; both |ρ_w| ≤ 0.30 → CONFIRMED; otherwise MARGINAL.
- **Prediction (stated before t₅ exists).** MARGINAL is the most likely single outcome: Paper A's legs were 0.307 and 0.395 on 42 units, and Paper A's sensitivities (its §3.7) ranged 0.196–0.489 on S1 and 0.315–0.516 on S0. §8 gives the precision.

### 3.2 HB2_Retest_t4t5 — PRIMARY (the second unmet condition, reliability; study #45, first part)

- **Statement.** G\* orders brands at t₅ as it did at t₄ (the same three models, the same questions, three weeks apart).
- **Statistic.** ρ_pw(G\*_t₄, G\*_t₅) over units rated at both waves (v0.45 §2.1's ρ_pw = this study's ρ_w); one-sided permutation p (t₅ values shuffled within category), 10,000 draws, seed 450046; bootstrap 95% interval, 10,000 resamples.
- **Verdict (v0.45 §2.6, word for word in its bands).** UNDETERMINED if n < 30 · CONFIRMED if ρ ≥ 0.50 and p < 0.05 · FALSIFIED if ρ < 0.30 · MARGINAL otherwise (v0.45's "PARTIAL"; the same band). Not measured if G\* does not exist at both waves.
- **One test, one owner.** Under C4 this is v0.45's Grounding component leg, carried into v0.45's paper with this study's verdict (v0.45 §2.6); the scorer writes it to `outputs/v122_hb2_for_v045.json` with its inputs' SHA-256.

### 3.3 HB3_Run_Reliability_t5 — PRIMARY (Paper A's H3, unchanged, on t₅)

- **Statistic and verdict.** v1.13 §3's H3, imported (`per_run_maps`, `reliability_test`, `reliability_verdict`): per-run G\*_r on t₅ with floor g_{b,r} ≥ 3; ρ_w for each run pair with ≥ 30 units rated in both; rel1 = mean; rel3 = 3·rel1/(1 + 2·rel1); one-sided permutation, seed 122003. CONFIRMED rel3 ≥ 0.50 and p < 0.05; FALSIFIED rel3 < 0.30; MARGINAL otherwise; UNDETERMINED with fewer than 30 units in two or more of the three run pairs.
- **Prediction.** UNDETERMINED is likely again (Paper A: 23, 27 and 24 units per pair). This is why HB2 is the reliability test with the better chance to decide; HB3 is kept because it is the exact unmet leg.
- **Reported beside (no verdict).** The 15 run pairs of the six runs t₄ + t₅ (within- and cross-wave ρ_w and their units), as v0.45 `H_Stab_Drift` reports for S0.

### 3.4 HB4_Sep_Consistency_t5 — SECONDARY (H2 replicated; enters the completion rule only as "not FALSIFIED")

ρ_w(G\*_t₅, C\*_S1,t₅) and ρ_w(G\*_t₅, C\*_S0,t₅) over units rated on both; seed 122004; v1.13's H2 rule (as HB1).

### 3.5 Gate completion rule (GB) — fixed now (C3)

Reliability condition **R**: MET if HB2 or HB3 is CONFIRMED and neither is FALSIFIED; FAILED if HB2 or HB3 is FALSIFIED and neither is CONFIRMED; MIXED if one is CONFIRMED and the other FALSIFIED; OPEN otherwise.

| Outcome | Rule (evaluated top to bottom) | Consequence |
|---|---|---|
| **FAIL** | HB1 FALSIFIED, or R FAILED, or HB4 FALSIFIED | Grounding failed its gate on replication: reported and redesigned, not shipped (CLAUDE.md, "Plan for speed") |
| **PASS (completed)** | HB1 CONFIRMED and R MET (and HB4 not FALSIFIED, by the row above) | Grounding's gate is completed; Grounding becomes eligible for the next release calibration in the roadmap's order (AIAS 3.0 / 4.0 / 5.0 = the next parts that pass) under that release's own pre-registration |
| **UNDETERMINED** | HB1 UNDETERMINED, or R OPEN with both HB2 and HB3 UNDETERMINED | Not decided; t₆ (Stage 2) can decide R only through a dated amendment before t₆'s answers exist |
| **MARGINAL** | otherwise (including R MIXED) | Stays MARGINAL; G\* remains a candidate measure reported beside Presence and Consistency (v1.13 §4); Pablo decides on the record whether anything further runs |

H6 (Coverage, MARGINAL at Stage C2) is not re-tested: t₅ has no Coverage re-ask (v0.45 §2.6, NOT MEASURED). The completion rule does not use it; the paper states that Coverage separability stays at Paper A's MARGINAL. The structure studies below never change GB.

### 3.6 Structure studies (Full study list #44–#48)

**#44 — HB44_SDRI (PRIMARY for #44).** ρ_w(SDRI, G\*_pool), one-sided (prediction positive), seed 122441, over units with both, in categories with ≥ 5 such units. SDRI = Paper A's Part II pass-1 SDRI (`audit/v1_13_sdri.csv`, as deposited; median 37.5, 77 brands rated). Bands = v1.13 H7: CONFIRMED ρ ≥ 0.30 and p < 0.05; FALSIFIED ρ ≤ 0.10; MARGINAL otherwise; UNDETERMINED below 30 units. **Seen before this lock (declared):** Paper A's H7 on the t₄ half (ρ_w 0.081, n 26, UNDETERMINED) and its SDRI_kg sensitivity (ρ_w −0.035, n 42); the confirmatory increment is t₅'s half of G\*_pool. **HB44b (SECONDARY):** the same with G\*_t₅ alone (no seen part), seed 122442. **Sensitivities:** S-SDRI-t5 (SDRI from the t₅ re-audit, C11); S-SDRI-kg (indicators 6–8 alone, all brands with a D_b, as Paper A's protocol §5 sensitivity); site-only SDRI (1–5). **Descriptive D44:** rich (top within-category tercile of SDRI) versus sparse (bottom tercile) brands: G\*_pool medians and source-class profiles.

**#45 — stability over waves.** First part = HB2 (§3.2). **Stage 2 (secondary, run once t₆ is collected and scored under its own pre-registration): HB45_t5t6** ρ_pw(G\*_t₅, G\*_t₆), seed 122451, and **HB45_t4t6** ρ_pw(G\*_t₄, G\*_t₆), seed 122452; HB2's bands and floor. **Descriptive D45 (each wave pair):** per model, Jaccard overlap of the 20 most-retrieved domains and of each class's top-10 domains; per category, the class mix with its change; the share of brand units whose own domain was retrieved at one wave and not the other. **v0.40's S1 arm (C6):** class mix only, under the frozen classes, after v0.40 is public; no G\* (v0.40's registry has no frozen D_b list) and no verdict.

**#46 — HB46_Phantom_Signature (PRIMARY for #46).** Pooled within-category Cliff's δ of G\*_pool between F and non-F units (v0.35 D1 as v1.19 H34: within-category cross pairs, pair-count weighted), units rated in categories with ≥ 5 rated units; two-sided permutation p (F labels shuffled within category, counts fixed), 10,000 draws, seed 122461. **Prediction: δ > 0** — when search surfaces a brand the legacy models seldom recalled, fewer third-party pages discuss it, so its grounded answers lean more on its own site. **Verdict (v1.19 H34 bands):** |δ| ≥ 0.30 and p < 0.05: CONFIRMED if δ > 0, CONFIRMED_REVERSED if δ < 0; |δ| < 0.15: FALSIFIED; otherwise MARGINAL; UNDETERMINED with fewer than 10 rated F units, fewer than 10 rated non-F units, or fewer than 3 categories holding both. **HB46b (SECONDARY):** the same contrast on within-category rank residuals of G\*_pool on P (P_S1 pooled over t₄ and t₅ as the mean of the two waves' P_S1), seed 122462; if HB46 and HB46b fall in different bands both are reported and HB46 is labelled "Presence-sensitive". **Descriptive D46:** the class mix of answers naming F versus non-F brands; per wave, F units named in S1 but never in S0 ("search-surfaced"); for D (defunct, no D_b): S1 answers naming each, their class mix, and naive versus caveated mentions by v1.19's 150-character keyword rule. v0.40's H_Search owns "does search correct ghosts"; D46 makes no such claim.

**#47 — HB47_IL_Channel (PRIMARY for #47).** On trio units (v0.20, v0.21, v0.22) with a D_b and at least 3 grounded answers in each channel (pooled t₄ + t₅ S1, N3): d_b = 100·(o_{b,cat}/g_{b,cat} − o_{b,cult}/g_{b,cult}), in percentage points. Statistic: mean d̄; one-sided sign-flip permutation (each d_b's sign flipped at random), 10,000 draws, seed 122471. **Prediction: d̄ > 0** (category-anchored questions ask for brands "with descriptions" and retrieve product pages; cultural questions retrieve reference and news pages). **Verdict (C9):** CONFIRMED d̄ ≥ 5 and p < 0.05; FALSIFIED d̄ < 2 (including any negative value); MARGINAL otherwise; UNDETERMINED with fewer than 20 eligible units or a trio category with fewer than 3. **HB47b (SECONDARY, the moderator):** ρ_w(IL_b, G\*_pool) on trio units eligible and rated; two-sided, seed 122472; v0.37 / v1.19 H35 bands (|ρ_w| ≥ 0.30 and p < 0.05: CONFIRMED if ρ_w < 0 (prediction: culture-led brands lean less on their own site), CONFIRMED_REVERSED if > 0; |ρ_w| < 0.15 FALSIFIED; otherwise MARGINAL; UNDETERMINED below 45 units or a trio category under 5). Prediction: UNDETERMINED is likely (v1.19 had 26 eligible units against the same floor). **Sensitivities:** S-AllChannels (all five categories' channel labels; v0.19 and v0.23 outside the construct's validated scope, labelled); S-IL-t1 (v0.37's t₁ IL-Direct, as v1.19).

**#48 — HB48_Profile_Replication (PRIMARY for #48).** Units rated at both t₄ and t₅. R = mean over the six classes c of ρ_w(x_{b,t₄,c}, x_{b,t₅,c}); one-sided p by permuting the t₅ profiles across units within category (one permutation for all six classes), 10,000 draws, seed 122481. **Verdict (v1.19 D9 bands, C9):** CONFIRMED R ≥ 0.20 and p < 0.05; FALSIFIED R < 0.10 or p ≥ 0.05; MARGINAL otherwise; UNDETERMINED below 30 units. Per-class values reported beside R. **HB48b (SECONDARY, typology; only if HB48 is CONFIRMED or MARGINAL, else "NO TYPOLOGY"):** on G\*_pool-rated units, features = the pooled six-class profile plus centred within-category ranks of G\*_pool, P_S1 (mean of waves) and C\*_S0 (mean of waves); Ward linkage, Euclidean; k by the gap statistic over 1…8 (500 references, 1-SE rule); silhouette null 10,000 within-category coordinate permutations (seed 122482; residual arm 122483); Presence tiers by v0.23's quartile rule within category; v1.19 §7.3's exhaustive matrix (LAYERED, BORROWED, AUTONOMOUS, PRESENCE-DEPENDENT, RESIDUAL-ONLY, UNSTRUCTURED; MARGINAL replication adds "provisional"). **Descriptive D48:** within-category median split G\*_pool × P_S1 (own-site-led and named / own-site-led and seldom named / third-party-led and named / third-party-led and seldom named); R\*_S1 at t₄ (v1.14 Stage 1) as a column, no test.

### 3.7 Quality checks (no verdict unless stated)

v1.13 §4's MQ1–MQ8 on t₅ and on the pool, imported unchanged; MQ5 on t₅ can make HB1/HB4 UNDETERMINED as in Paper A. MQ3 is expected to flag again (Paper A: 71.8% of distinct (answer, domain) pairs other or unresolved, above 0.60, "low coverage"); every class-based result (#45 D45, #46 D46, #48) carries that label when it fires. Added: **MQ9** per model, the S1 served model ID at t₅ versus t₄ (v0.45 MC_Served flag carried); **MQ10** the t₅ S1 calls answered per model (v0.42 drop rule) and whether C5's arm was used.

## 4. Models

This study calls no model. Its answers come from t₄ and t₅, whose panel is fixed by their own locked pre-registrations: N3 = Claude Fable 5.2 (`claude-fable-5-2`), GPT-6 Astra (`gpt-6-astra`), Gemini 4 Argon (`gemini-4-argon`), search on as v0.39 / v0.42 §4.4; t₅ keeps the same IDs unless v0.45 §4.3's replacement rule fires (then the replacement's answers are labelled and every t₄ → t₅ comparison involving that provider is reported "model changed"; HB2 runs on the common panel, ≥ 2 models).

**The programme rule "newest GA flagship per provider, verified from vendor docs at pre-registration" applies only to C5's contingent arm, and there parity wins:** the arm must use t₅'s own model IDs (otherwise it would not complete t₅). **To verify at lock (r1):** (a) the three IDs are still listed as available (Anthropic models / deprecations page, OpenAI models page, Google Vertex AI model page), quoted with date and time; (b) whether any provider has since released a newer GA flagship — if so it is recorded as a limitation (t₅ is no longer "the newest models") and is not substituted; (c) prices for C5 (programme rule: verify at each pre-registration). Nothing in this list was checked by this lane (no vendor page was read for r0); the last reading in the record is v0.45 r1's (2026-11-11, 08:36–08:38 am CT: "nothing changed for the panel, and no panel model has an announced retirement or shutdown before the window ends") and the coordinator's lock-lane reading of ~02:50 UTC on 2026-11-11 (STATUS.md: "Claude Fable 5.2 and Opus 5.5 Active; GPT-6 Astra no deprecation notice; Gemini 4 Argon Stable").

## 5. Budget, cap and stop rules

- **Own paid model calls: none. $0.** The t₅ answers are paid under v0.45's own $100 cap (r1 estimate $70.40 central / $149.55 high for 876 calls, $72.90 central with the judge reserve; v0.45 §4.5). This study adds nothing to it.
- **Web audit (C11):** public pages and Wikidata, no paid API; Mac-light; scheduled after t₅'s collection ends (never beside a paid collection, the Mac rule).
- **C5 contingent arm (only if Pablo answers C5 "yes" and v0.45's guard stops S1 runs 2–3).** Same 90 S1 questions × runs 2 and 3 on the models still in t₅'s S1 panel (at most 180 calls), inside t₅'s window (v0.45 §4.6), only after v0.45's collection has stopped (one paid collection at a time), with v0.45's acquisition code and call policy unchanged and its own ledger `osf/methodology/v1_22/data/c5_budget_state.json`. **Estimate:** v0.45's own figures for blocks 6–7, $18.05 + $18.72 = **$36.77 central**, about **$80.19 at v0.45's high estimate** (v0.45 §4.5); to be re-estimated at r1 from t₄'s recorded usage at the prices verified at lock. **Cap $100 hard stop and pause at $80, computed from actual recorded usage** (programme rule), worst case reserved before each request as v0.45's `budget_v0_45.Ledger`. If the arm cannot fit, HB3 and the six-run pool use what exists and say so. These answers enter only this study (and v0.45's leg only through HB2's carried verdict), labelled "C5 arm".
- **No other spend.** Anything else needs a dated amendment before it happens.

## 6. Stages and order

| Stage | When | Needs | Computes |
|---|---|---|---|
| Lock | before 2026-12-03 06:00 UTC | §10 | nothing |
| C5 arm (contingent) | inside t₅'s window, after v0.45 stops | C5 "yes" + v0.45 projection pause | collection only |
| Re-audit (C11) | Dec 7–10, after t₅'s last call | lock | Part II pass 3 (protocol unchanged; robots.txt; ≥ 10 s per host) |
| **Stage 1** (once) | after `v0.45-acquisition-locked` and v0.45's scored commit exist, and `anchor/pablo_decision_paper_B.json` | B-P0–B-P3 (§9) | HB1–HB4, GB, HB44(b), HB46(b), HB47(b), HB48(b), D44–D48, MQ, sensitivities |
| **Stage 2** (once) | after t₆ is collected and scored under its own pre-registration | t₆ tags | HB45_t5t6, HB45_t4t6, D45 for t₆ pairs |

Each stage refuses to run twice (its output folder must be empty). Stage 1 never waits for Stage 2; the paper may ship after Stage 1 with Stage 2 "pending" (Full study list estimate: Mar).

## 7. Sensitivities (reported beside each verdict; never change one; every differing verdict is listed)

S-COI (without Denon and the five Cheil / Iris brands: Chevrolet, BMW, Bentley, Jack Daniel's, Eucerin) · S-Floor3 and S-Floor10 (v1.13 S4) · S-Cited (the `citations` field; v1.13 S2) · S-NoGemini (Gemini 4 Argon out; MQ2 flagged it "search rarely used" at t₄, 17.8%) · S-m (denominator m_b; v1.13 S1) · S-Uncentred (v1.13 S10) · S-LOCO (leave one category out) · S-Pool / S-Wave (each structure test on G\*_pool versus G\*_t₅ alone) · S-SDRI-t5, S-SDRI-kg (#44) · S-AllChannels, S-IL-t1 (#47) · S-F-noD (#46 without the five defunct brands; they are unrated anyway, so a check) · S-C5 (without C5's arm, if used) · S-House (without the three house / portal-domain units: Dior Beauty, Chanel Beauty, Lagavulin).

## 8. Power and precision (approximate; not verdict inputs)

Simulated with bivariate normal data and Pearson's r, one leg, 8,000 draws per cell (lane computation, 2026-11-25; a rank statistic on real ranks will differ somewhat):

| Units n | True ρ | P(\|r\| ≤ 0.30) (separability "CONFIRMED" side, one leg) | P(\|r\| ≥ 0.50) |
|---|---|---|---|
| 30 | 0.00 / 0.15 / 0.30 / 0.40 | 0.89 / 0.78 / 0.49 / 0.27 | 0.01 / 0.02 / 0.11 / 0.25 |
| 42 | 0.00 / 0.15 / 0.30 / 0.40 | 0.95 / 0.83 / 0.50 / 0.23 | 0.00 / 0.01 / 0.08 / 0.22 |
| 60 | 0.00 / 0.15 / 0.30 / 0.40 | 0.98 / 0.89 / 0.50 / 0.19 | 0.00 / 0.00 / 0.04 / 0.18 |

HB1 needs both legs ≤ 0.30; if the true association is near Paper A's point estimates (0.31–0.40), HB1 is more likely MARGINAL than CONFIRMED at n ≈ 42 — the test is fair but not generous, and a CONFIRMED there would be informative.

| Units n | True retest ρ | P(r ≥ 0.50) (HB2 CONFIRMED side, ignoring p) | P(r < 0.30) (FALSIFIED) |
|---|---|---|---|
| 30 | 0.4 / 0.5 / 0.6 / 0.7 | 0.27 / 0.53 / 0.79 / 0.95 | 0.26 / 0.10 / 0.02 / 0.00 |
| 42 | 0.4 / 0.5 / 0.6 / 0.7 | 0.22 / 0.52 / 0.83 / 0.98 | 0.22 / 0.06 / 0.01 / 0.00 |
| 60 | 0.4 / 0.5 / 0.6 / 0.7 | 0.17 / 0.51 / 0.87 / 0.99 | 0.19 / 0.03 / 0.00 / 0.00 |

**The binding risk is n, not power:** HB2 needs ≥ 30 units rated at both waves. Paper A rated 42 at t₄; if t₅ rates a similar number, the overlap may fall near 30 (not estimated from data here: that would mean reading t₄ per-brand rating flags against a t₅ that does not exist). The pooled score (C7) is how the structure tests reach their floors (30 for #44/#48, 45 for #47b, 10 + 10 for #46). Fisher-z 95% half-width at ρ = 0.50: about ±0.30 at n = 30 and ±0.24 at n = 42.

## 9. Gates before any statistic, and no peeking

`score_v1_22.py --stage 1` refuses unless: tag `v1.22-prereg-r1` is on origin and `anchor/osf_anchor_v1_22.json` names its commit; `anchor/pablo_decision_paper_B.json` is valid (§1); tags `v0.45-acquisition-locked` and v0.45's scored commit exist; `outputs/stage1/` is empty. Then, in order, each failure stopping the run (fix logged in DEVIATIONS first):

- **B-P0** the imported v1.13 scorer, `source_classes_v1_13.md` and `brand_domains_v1_13.csv` hash to v1.13's lock manifest; v1.19's phantom roster hashes to `9b67e892…`.
- **B-P1** G\*_t₄ recomputed with the imported functions from t₄'s files equals Paper A's per-unit G\* (o_b, g_b, rated flag) for all 112 units, and Paper A's H1/H2 statistics reproduce to 1e-12.
- **B-P2** t₅'s probe file equals t₄'s byte for byte (v0.45 MC_Probe_Parity) and t₅'s S1 records parse (MQ1).
- **B-P3** P and C\* at t₅ recomputed from v0.45's brand table equal v0.45's reported P_S0 (v0.45 §2.2 "reported alongside") for every unit where both exist.

**Ex ante state.** At lock no t₅ answer exists. What this study has already seen of t₄ is Paper A in full (every published G\*, H1–H7 statistic, sensitivity, MQ value and per-brand appendix), so every test is confirmatory only on its t₅ part; tests on G\*_pool are labelled "partly seen (t₄ half published in Paper A)". If the lock slips past t₅'s first call, HB1–HB4 and HB2's carry into v0.45 stay valid only if this study locks before any t₅ S1 record is read for any purpose (coding included); the lock record says which came first, and v0.45 §2.6 then decides whether its own leg or this study's verdict is carried (v0.45's text: "before t₅'s answers exist" — a lock after the first call means v0.45 keeps its own leg; flagged in Call C10).

## 10. Lock: earliest date and what it needs

- **Earliest possible lock:** 24 hours after Pablo receives r1 (programme rule; he may waive it, as for v1.13 Part I). If r1 reaches him Wed 11/25, the earliest lock is Thu 11/26 (Thanksgiving). **Recommended:** Mon 11/30 or Tue 12/1, after his C1 decision (expected with the Grounding paper call, ~11/29). **Latest:** tag pushed and OSF deposit verified before **Thu 2026-12-03 06:00 UTC (Wed 12/2, midnight CT)**; to leave room, start the lock steps by Wed 12/2 6 pm CT.
- **Needs:** (1) Pablo's answers to C1–C12 (C1 can be recorded at or after the lock, but before Stage 1; recommended at lock); (2) r1: the scorer `score_v1_22.py` written against v1.13's imported functions, its unit tests and the synthetic dry run (§11), all green; the channel-label map checked against the probe file; the C5 re-estimate and vendor check (§4) if C5 is "yes"; (3) the number re-checked (git, OSF); (4) `LOCK_MANIFEST_v1_22.sha256`; (5) one OSF upload at a time (`osf_deposit.py`, dry run first); not beside v0.62's paid collection if it is still running (Mac rule).

## 11. Keyless dry-run plan (synthetic only; no network, no key, no real answer)

1. **Synthetic worlds** (seeds 122490–122494), each with t₄'s real design (112 units in 16/24/24/24/24; 30 questions with their real channel labels from the probe file; N3 × 3 runs × 2 waves; per-answer source lists drawn over the eight classes with Paper A's published class shares and search-use rates per model as parameters, and own-domain hits from a brand-level propensity): **null** (G\* independent of P and C\*; no retest signal; no F, channel or SDRI effect); **effects** (retest ρ ≈ 0.7; F brands +0.4 SD own share; category-channel own share +8 points; SDRI → G\* ρ ≈ 0.4; three source-profile types); **Paper-A-like** (G\*–P ρ ≈ 0.35; per-run floors binding as in Paper A); **thin S1** (Gemini search use 18%, one model dropped at t₅); **C5 world** (t₅ with one S1 run plus a C5 arm).
2. **Run** `python3 osf/methodology/v1_22/scripts/score_v1_22.py --dry-run osf/methodology/v1_22/dryrun --draws 10000` on the Mac when no paid collection runs (or in the cloud container with the repo's v1.13 scorer staged); record runtime, every verdict and statistic, and the scorer's SHA-256.
3. **Pass conditions before lock:** effects world returns each built effect (else the band or test is changed *before* lock and listed in the change log, as v1.19 D9); null world returns no CONFIRMED on HB44/HB46/HB47/HB48 beyond chance and GB = MARGINAL or FAIL; the Paper-A-like world reproduces HB3 UNDETERMINED; the not-run paths (no decision; `go: false`) write the not-run record with no statistic; B-P1 passes on a synthetic Paper-A output written by v1.13's own `score` functions.
4. **Unit tests:** GB and R tables exhaustive over all verdict combinations; HB2 equals v0.45's component-leg function on the same inputs (import v0.45's `score_v0_45.py` at its locked blob if it exposes the leg; else a hand-built fixture); Cliff's δ against brute force; sign-flip p against enumeration for n ≤ 12; profile vectors; G\*_pool arithmetic; refusal guards.
5. **Stub status at r0:** `scripts/score_v1_22.py` holds the constants, the decision tables (R, GB, the #44–#48 bands) and the refusal guards; `scripts/tests/test_decision_rules_v1_22.py` tests the tables. Data paths are r1 work.

## 12. What was read while drafting (ex ante record)

Read on 2026-11-25 between ~0:10 and ~1:30 am CT: the Full study list tab (Grounding rows #41–#48 and the rows mentioning MARGINAL / Paper B; read only, not edited); `Try system book/CLAUDE.md` (lines matching Paper B / registry / MARGINAL / grounding; "Plan for speed"; the $100 rule); `STATUS.md` and `aias_roadmap_ssot.md` lines matching grounding / v1.13 / Paper B; v1.13's deposited `v1_13_verdicts.json` (gate, legs, H3 pairs, MQ — Stage C1 file), its paper draft §Abstract–§6 (all published), its pre-registration headings and §8, its lock-manifest lines for the scorer and frozen lists, its scorer's function list; v0.45's pre-registration §0–§2.8 and §4.5–§4.6; v0.42's probe file (keys, phase counts, the first seven Phase B rows); v0.40's pre-registration lines on search; v1.19's pre-registration (whole) and DEVIATIONS Entry 0 (first part); v1.19's phantom roster (header, two rows, line count, SHA-256). **One incidental read of t₄ answer text:** a `grep -o` for the word "phantom" on `osf/v42/data/t4_raw.jsonl` printed three ~200-character fragments of t₄ answer text (automotive answers mentioning the Rolls-Royce Phantom model); no source record, rating or statistic was read or computed. No t₅ data exist. No vendor page was read.

## 13. Limitations

1. MARGINAL start: every verdict is conditional on Pablo's decision (C1), and Paper A's t₄ results are fully known; only the t₅ parts are unseen.
2. t₅ is three weeks after t₄ on the same models: HB2 measures short-term stability of "model plus web on the day", not durability; t₆ (Stage 2) extends it.
3. Units rated at both waves may fall below 30 (§8); several structure tests are likely UNDETERMINED (predicted in §3).
4. MQ3 low coverage (most retrieved domains classed "other" at t₄): class profiles (#48) and mixes rest on the classified minority.
5. Gemini 4 Argon used search in 17.8% of t₄ category answers; its contribution to G\* is small (S-NoGemini).
6. G\*_pool mixes two waves; it is a new estimand, not Paper A's G\*.
7. The phantom flags come from the legacy six-model panel at t₁; IL is construct-valid on three categories only; US English; five categories.
8. Own-domain retrieval depends on sites being indexed and open to crawlers (Paper A §5); the audit's AQ2 fetched 72% of home pages.
9. No multiplicity correction; 16 verdict-bearing tests across two stages, each reported.

## 14. Declarations

**Conflict of interest.** Carried forward from v1.13's locked record and v1.19 §14, quoted from their source records there (v0.19 AKG → Denon substitution and the Nov 10, 2026 correction that Denon is owned by Harman International, a Samsung Electronics subsidiary, since Sep 23, 2025; v0.22's tier-2/3 supply relationships via Harman, Samsung SDI and Samsung Display, non-competitive, no restriction on registry composition; Cheil Worldwide / Iris agency work for Chevrolet, BMW, Bentley, Jack Daniel's and Eucerin, v0.62 DEVIATIONS Entry 0 Part F). At r1 the exact wording is conformed to v1.13's locked Declarations, not to memory (CLAUDE.md). All six brands stay in every analysis; S-COI reports each test without them. Samsung appears only in Declarations; Samsung Electronics had no role in the design, conduct, analysis or reporting.

**Funding.** Self-funded; no paid model call (C5 contingent). **Ethics.** No human subjects; the audit reads public pages under robots.txt.

**Use of AI tools.** During the preparation of this work the author used AI tools (Anthropic's Claude) to assist with study design, analysis and writing. The author reviewed and edited all content and takes full responsibility for it.

## 15. Calls for Pablo: reasons for the recommended answers

- **C1 (go on MARGINAL): yes.** No leg failed; H3 was undetermined by a floor (per-run counts), not by evidence of unreliability; t₅ supplies a fresh, already-funded test of exactly the two unmet conditions at no extra cost. Saying no leaves Grounding where Ranking is (reported inside Presence's story) without having tested what t₅ can test.
- **C2 (number): v1.22.** Next free methodology number; the v1.19 precedent (Coverage Paper B took the next number). `v1.13-paperB` is the alternative naming.
- **C3 (completion rule): yes.** Without it, a clean t₅ replication could never move Grounding out of MARGINAL. The rule demands HB1 CONFIRMED (both legs ≤ 0.30 on fresh answers) and reliability MET, and fails Grounding on any falsification, so it is no easier than Paper A's gate.
- **C4 (HB2 = v0.45's leg, seed 450046): yes.** v0.45 §2.6 already pre-commits to carrying a Paper B verdict; identical statistic, bands and seed mean the two documents cannot disagree.
- **C5 (contingent S1 completion): yes, capped.** HB3 needs three t₅ runs; without runs 2–3, HB3 is UNDETERMINED for certain and the pool has four runs instead of six. v0.45 itself says the two runs would not fit its cap at the high estimate. Cost only if it happens.
- **C6 (v0.40): descriptive only.** One S1 run, a different registry, no frozen own-domain list, and v0.40 is unpublished until Dec 14.
- **C7 (pooled G\*): yes.** Paper A rated 42 units on three runs and its H7 fell short at 26; six runs should rate more units. It is declared partly seen.
- **C8 (phantom = F): yes.** Same set as Coverage Paper B (comparable across components); the defunct brands have no own domain, so they cannot be rated.
- **C9 (bands): accept, subject to the dry run.** #47's bands are new (no programme precedent for a within-brand difference of shares); #48 borrows v1.19's bands, which were set for Coverage profiles on synthetic data. The r1 dry run must show each test detects its built effect, as v1.19 did.
- **C10 (timing): lock before Dec 3 06:00 UTC.** After t₅'s first call, v0.45's own leg owns the retest and HB1–HB3 lose their ex-ante status.
- **C11 (re-audit): yes.** Free; gives a second SDRI reading for the sensitivity and a stability check (Paper A's pass 2 found 0% change among 77 home pages, so little change is expected).
- **C12 (t₆ legs now): yes.** Pre-registering before t₆ exists keeps #45's second half confirmatory at no cost.

## 16. Deviations procedure

`anchor/DEVIATIONS.md` (Entry 0 written with this draft) and, after the lock, `postlock/DEVIATIONS_continued_v1_22.md`. Entries are appended, never edited, each dated (CT and UTC) and marked ex ante (before any v1.22 statistic on real data) or ex post. Before the lock, a change that alters no hypothesis, statistic, band, floor, seed, exclusion or decision rule is a clarification logged in §18; any other change restarts the 24 hours. After the lock nothing in §1–§3 changes; a needed change is a dated deviation with its reason, the result is reported both ways where both can be computed, and the paper lists every deviation. A failed gate (B-P0–B-P3) stops the run; the fix is logged before re-running. The OSF deposit of each entry follows the lock-and-deposit steps (`osf_deposit.py`).

## 17. Files (r0)

`prereg/PRE_REGISTRATION_v1_22_DRAFT_r0.md` (this file); `anchor/DEVIATIONS.md` (Entry 0, draft); `scripts/score_v1_22.py` (stub: constants, decision tables, guards); `scripts/tests/test_decision_rules_v1_22.py`. At r1: the scorer's data paths, the synthetic worlds, the dry-run records, `LOCK_MANIFEST_v1_22_DRAFT.sha256`.

## 18. Change log

- 2026-11-25, ~0:10–1:30 am CT: r0 drafted by a lane of the AIAS runner (local commit on branch `v1.22`; not pushed, not deposited, not sent).
