# v0.12 — Three-Category Construct-Validity Expansion (Kickoff Prompt)

---

## Context

I'm Pablo Ulpiano González Castro — Director, Corporate Brand Creative and Governance at Samsung Electronics America; faculty in Creative Strategy at the SVA MPS Branding Program; founder of Third System™ (thirdsystem.ai), an independent research entity where I run the AIAS Presence Measurement Programme.

The AIAS programme has shipped through v0.11. The build pipeline lives at `/Users/pablou/aias/`:
- `scripts/` — Python acquisition, rescaling, scoring, chart-building
- `reports/` — ReportLab brand-format report builder (three-file set per version)
- `osf/vNN/` — per-version OSF deposit folder (uploaded via `scripts/osf_upload.py`)
- `brand/third_system_brand.json` — visual identity tokens (Indigo #37237B primary, Akkurat Pro)

Each new phase forks build files with a new prefix, locks a pre-registration at a git commit prior to data collection, and ships three deliverables: a brand-format PDF report (Akkurat Pro, ReportLab+pypdf two-pass), an SSRN academic paper (Carlito, pandoc+xelatex), and an OSF deposit at `osf.io/ec6wh/files/osfstorage/vNN/`.

Standard cross-cite list (use these for all bibliography work):

| Version | SSRN abstract |
|---|---|
| AI Availability foundational paper | 6659000 |
| AIAS Presence Measurement Protocol v1.1 | 6722319 |
| v0.6 Cross-Category Findings | 6720959 |
| v0.7 Phantom-Brand BBB | 6721779 |
| v0.8 Discourse-Language Knives | 6728000 |
| v0.9 Longitudinal Re-Baseline | 6736878 |
| v0.10 Naive-Phantom Rate Stability | 6741163 |
| **v0.11 PM × Trends Construct Validity** | **6745040** |

URL pattern: `https://ssrn.com/abstract={id}`

---

## What v0.11 found (input to v0.12)

v0.11 was the **first construct-validity test** in the programme: a single-category pre-registered pilot of per-brand AI Presence rates against per-brand Google Trends search interest, for 18 project management software brands at two longitudinal waves seven days apart.

**Results:**
- **H1 (cross-sectional construct validity):** Spearman ρ = 0.496 at t₁, 0.476 at t₂; one-tailed *p* < 0.05 at both waves. Significance bar cleared; **moderate-to-strong magnitude threshold (ρ > 0.5) missed by 0.004 at t₁. Falsified.**
- **H2 (stability):** |Δρ| = 0.020 against a 0.15 tolerance. **Confirmed with almost an order of magnitude of margin.**
- **H3 (leaderboard top-3 ⊆ top-5):** 1 of 3 at both waves. **Falsified decisively.**
- **H4 (covariate-controlled, age + tier):** partial ρ = 0.407 / 0.428 across waves; magnitude bar missed. **Falsified.**

**Substantive interpretation (the v0.12 hypothesis):**

AI applies a **tighter and partly-different category boundary** than consumer search does. Two diagnostic cases anchor the finding:

- **Linear paradox:** AI's #1 PM-software recommendation at both waves (86.5%, 89.6% AI Presence) with negligible consumer search interest (Trends ≈ 1.88 with Asana indexed to 100). Inside AI's category, barely inside consumers'.
- **Todoist inverse:** 1% AI Presence with Trends value comparable to GitHub Projects (which receives 40× more AI Presence at the same search interest). Outside AI's category (AI frames it as a personal task manager), well inside consumers'.

The construct of AI Availability is **correlated but not equivalent** to Mental Availability. v0.12's job is to test whether this category-boundary mechanism generalises beyond PM software.

---

## v0.12 — what we're building

**Project:** Three-category construct-validity expansion of v0.11.

**Categories** (per memory and v0.11 §7):
1. **PM software** — direct replication of v0.11 with a fresh acquisition window
2. **Premium olive oil** — leadership zone is stable across both AI and consumer search (Brightland, Graza, Castillo de Canena lead in both per v0.6 and v0.9); cleanest replication candidate; predicted ρ > 0.5
3. **Premium running shoes** — high brand density (12+ active brands); tests the pattern under competitive saturation; prediction less clear

**Sharpened hypothesis space** (to be locked at pre-reg):
- H1 per category: cross-sectional construct validity, two waves
- H2 per category: cross-wave stability
- H3 per category: leaderboard top-3 ⊆ top-5
- H4 per category: covariate-controlled (age + tier)
- **H5 — generalisation (new in v0.12):** Does the H1 just-miss / H3 leaderboard divergence pattern reproduce in 2 of 3 categories?
- **H6 — category-boundary mechanism (new in v0.12):** Does each category produce its own Linear-paradox-style and Todoist-inverse-style brand pair? (Operationalisation TBD at pre-reg.)

**AI Presence input:** Use the v0.9 deposited matched-subset measurements (Sonnet 4.6 + GPT-5.4-mini) for all three categories. Same registry freeze from v0.6. No new LLM measurement at v0.12; the construct-validity test is between the existing AI Presence rates and freshly-acquired Trends data.

**Google Trends acquisition:** Fresh session at v0.12 lock + 1 day. Same pivot-rescaling protocol as v0.11. Per-category pivot selection is a pre-reg decision (likely: PM software = Asana; olive oil = California Olive Ranch or Cobram Estate; running shoes = Asics or Nike).

---

## Key pre-registration design decisions to lock first

These are the open questions for the pre-reg draft. Each needs an explicit decision before lock:

1. **Wave windows:** v0.11 used a Sun-Sat window centred on v0.6 and v0.9 collection. For v0.12, do we replicate the same exact window dates, or pick fresh windows? (Locking fresh windows means acquisition has to happen during them; locking historical windows means lock can happen at any time.)

2. **Per-category pivot brand:** Asana worked for PM software because of stable high-volume Trends signal. Olive oil and running shoes need pivot selection. Brightland or California Olive Ranch as olive oil pivot? Asics or Nike for running shoes? Need to check Trends volume to pick a robust pivot.

3. **Pooling vs per-category analysis:** Are H1/H2/H3/H4 evaluated per category (six hypothesis × three categories = 18 outcomes), pooled across categories (single ρ on stacked data), or both? My preference is per-category as primary, pooled as sensitivity.

4. **n-floor per category:** PM software cleared 17-of-19. Olive oil registry has ~11 brands per v0.6; running shoes has ~12. Need explicit n-floors that match category sizes.

5. **H5/H6 operationalisation:** "Generalisation" and "category-boundary mechanism" need precise numerical thresholds. The Linear/Todoist diagnostic in v0.12 needs a falsifiable definition — what counts as a "Linear" in olive oil or running shoes?

6. **Brand age sourcing:** v0.11 used product-launch years for PM software. Need analogous sources for the other two categories (founding year for olive oil brands; running-shoe-line launch year for footwear).

---

## Workflow (same as v0.11, well-tested)

1. **Pre-registration draft** → lock at `v0.12-prereg` git tag, commit hash recorded
2. **Acquisition** — SerpAPI Google Trends, 5 pivot bundles × 3 categories × 2 regions = 30 API calls
3. **Pivot-rescaling** — same protocol as v0.11; per-brand within-window means
4. **Scoring** — per-category hypothesis evaluation; cross-category aggregation for H5/H6
5. **Charts** — fork `scripts/build_charts_v11_pmtrends.py`; ~4 figures per category + 1 cross-category summary
6. **Brand-format report** — fork `reports/build_report_v11.py` + content module; ~14-18 pages target
7. **SSRN paper** — fork `papers/v11_ssrn_paper_v2.md` structure; ~7,000 words; pandoc + xelatex + Carlito
8. **OSF deposit** — `python ~/aias/scripts/osf_upload.py ~/aias/osf/v12 v12`
9. **SSRN submission** — yields new abstract ID for cross-cite list

---

## First action

Draft the v0.12 pre-registration document. Walk me through the six design decisions listed above one at a time. For each:
- Recommend a position with reasoning
- Flag the alternatives I'd want to consider
- Ask for my decision before moving to the next

Once all six are locked, generate the full pre-registration document for me to review before git commit.

The v0.11 pre-reg lives at `/Users/pablou/aias/osf/v11/PRE_REGISTRATION.md` and is the template to fork from. The v0.11 paper at `/Users/pablou/aias/osf/v11/papers/v11_ssrn_paper_v2.md` documents the methodology in depth.

Ready when you are.
