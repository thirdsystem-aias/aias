# SSRN Submission Packet — v0.11

**Working title:** v0.11 PM Software × Google Trends Construct Validity
**Submission target:** SSRN (papers.ssrn.com)
**Author:** Pablo Ulpiano González Castro
**Submission date:** 10 May 2026

---

## 1. Final paper PDF

Render command (from `~/aias/osf/v11/papers/`):

```
pandoc v11_ssrn_paper_v2.md --pdf-engine=xelatex \
  --include-in-header=preamble.tex \
  -o v11_ssrn_paper_v2.pdf
```

Upload `v11_ssrn_paper_v2.pdf` as the paper.

---

## 2. Title (SSRN form field: "Title")

**Primary title:**

> A Construct-Validity Pilot for AI Presence Against External Behavioural Data

(73 characters — well under SSRN's 250-char limit.)

**If SSRN requires a single long title combining the descriptive tagline:**

> A Construct-Validity Pilot for AI Presence Against External Behavioural Data: Pre-Registered Evidence from 18 Project Management Software Brands at Two Longitudinal Waves Against Google Trends

(193 characters.)

---

## 3. Subtitle / Descriptive line (SSRN form field: "Subtitle", if present)

> Pre-Registered Evidence from 18 Project Management Software Brands at Two Longitudinal Waves Against Google Trends; the Linear Paradox and the Todoist Inverse Anchor a Tighter Category Boundary in AI Mediation than in Consumer Search

(238 characters.)

---

## 4. Abstract (SSRN form field: "Abstract")

SSRN's abstract field accepts long-form text (no hard cap in practice; v0.8 and v0.9 abstracts ran ~500 words each). Use the **full version below**.

**Full abstract** (466 words, 3,191 characters):

> This paper reports the first construct-validity test in the AIAS measurement programme: a single-category pre-registered pilot comparing per-brand AI Presence rates against per-brand Google Trends search interest for eighteen project management software brands, measured at two longitudinal waves seven days apart. The study opens Phase 3 of the AIAS programme by establishing whether the LLM-side measurement instrument developed across versions v0.6 through v0.10 corresponds to observable consumer behaviour at the brand level. Four hypotheses with explicit numerical thresholds were committed to a pre-registration document locked at git commit f20ade8 (tag v0.11-prereg) prior to any Google Trends acquisition call against the wave windows.
>
> The result is informative in a way that a clean confirmation or a hard rejection would not be. AI Presence and Google Trends search interest are positively correlated (Spearman rho = 0.496 at t1, 0.476 at t2; one-tailed p < 0.05 at both waves) and stably so across the seven-day longitudinal interval (|delta-rho| = 0.020 — H2 confirmed with almost an order of magnitude of margin against the pre-registered 0.15 tolerance). But the correlation narrowly misses the pre-registered moderate-to-strong threshold (rho > 0.5) at t1 by 0.004 and weakens further under covariate control (partial rho ≈ 0.41 after brand age and competitive density adjustment — H4 falsified). The leaderboard test (H3) localises where the construct fails: at both waves, only one of three AI-top-three brands appears in the Trends top-five. The construct's divergence is concentrated at the top of the AI Presence distribution.
>
> Two diagnostic cases anchor the substantive interpretation. Linear has the highest AI Presence in the registry (86.5 percent) and a Google Trends rescaled mean of 1.88 with Asana indexed to 100 — AI's number-one PM-software recommendation despite negligible consumer search interest. Todoist has the inverse profile: 1.04 percent AI Presence with a Trends value of 28, comparable to GitHub Projects, which receives forty times more AI Presence. Both cases support the same finding: AI applies a tighter and partly-different category boundary than consumer search does. Linear is inside AI's PM-software category but barely inside consumers' search-revealed one; Todoist is outside AI's PM-software category but well inside consumers'. The construct of AI Availability is correlated but not equivalent to Mental Availability — consistent with the theoretical position articulated in the Tri-System Brand Growth framework.
>
> The combined result set is interpreted as a partial validity argument for AI Presence as a distinct construct. AI Presence behaves like a real, structured property at the brand level — it covaries with consumer search interest at moderate strength, reproduces across waves at near-identity, and diverges from consumer search in identifiable, theoretically-predictable places. It is not, however, interchangeable with Mental Availability at the level of practical inference, and the practical question of whether AI Presence predicts purchase behaviour remains the object of the Phase 3 expansion programme.

**Short version** (in case SSRN form imposes a stricter limit; 1,236 chars):

> This paper reports the first construct-validity test in the AIAS measurement programme: a single-category pre-registered pilot comparing per-brand AI Presence rates against per-brand Google Trends search interest for 18 project management software brands at two longitudinal waves. Spearman rho = 0.496 at t1, 0.476 at t2; one-tailed p < 0.05 at both waves; |delta-rho| = 0.020 across waves. H1 falsified at the locked moderate-to-strong threshold (rho > 0.5) by 0.004; H2 confirmed; H3 falsified (1 of 3 AI-top-three brands in Trends top-five at both waves); H4 falsified after covariate control. Two diagnostic cases anchor the interpretation: Linear (AI's #1 PM-software recommendation at 86.5% AI Presence with negligible consumer search interest) and Todoist (1% AI Presence with search interest comparable to GitHub Projects, which receives 40 times more AI Presence). Both support a single finding: AI applies a tighter and partly-different category boundary than consumer search does. AI Availability is correlated but not equivalent to Mental Availability — consistent with the Tri-System Brand Growth framework. Pre-registered at git commit f20ade8 prior to acquisition; data, code, and registry deposited at osf.io/ec6wh.

---

## 5. Keywords (SSRN form field: "Keywords")

Semicolon-separated, paste verbatim:

```
AI Availability; AI Presence; Mental Availability; brand mediation; construct validity; AIAS; Google Trends; pre-registered measurement; longitudinal replication; project management software; LLM brand recommendations
```

---

## 6. JEL Classification (SSRN form field: "JEL Codes")

Primary: **M31** (Marketing)

Secondary:
- **L86** (Information and Internet Services; Computer Software)
- **L15** (Information and Product Quality)
- **D83** (Search; Learning; Information and Knowledge; Communication; Belief; Unawareness)
- **M37** (Advertising)

Paste format (most SSRN forms accept codes separated by commas or semicolons):

```
M31; L86; L15; D83; M37
```

---

## 7. Suggested SSRN Networks / Subject Area Classifications

Subscribe the paper to the same networks used for v0.6 through v0.10. Likely candidates based on prior submissions:

- Marketing eJournal
- Behavioral Marketing eJournal
- Information Systems & Economics eJournal
- AI - Artificial Intelligence eJournal
- Information & Knowledge Management eJournal
- Marketing Science Institute Research Network
- Decision Sciences eJournal

(SSRN typically pre-populates suggested networks from your prior submissions — check the auto-suggested list and keep what aligns.)

---

## 8. Related Works (SSRN form: "References" or in-paper citation IDs)

The paper cross-cites the following prior SSRN abstracts. After submission, when you receive the v0.11 abstract ID, return to each of these and add v0.11 as a related work in the reverse direction.

| Reference | SSRN ID | URL |
|---|---|---|
| AI Availability foundational paper | 6659000 | https://ssrn.com/abstract=6659000 |
| AIAS Presence Measurement Protocol v1.1 | 6722319 | https://ssrn.com/abstract=6722319 |
| v0.6 Cross-Category Findings | 6720959 | https://ssrn.com/abstract=6720959 |
| v0.7 Phantom-Brand Persistence (BBB) | 6721779 | https://ssrn.com/abstract=6721779 |
| v0.8 Discourse-Language Knives | 6728000 | https://ssrn.com/abstract=6728000 |
| v0.9 Longitudinal Re-Baseline | 6736878 | https://ssrn.com/abstract=6736878 |
| v0.10 Naive-Phantom Rate Stability | 6741163 | https://ssrn.com/abstract=6741163 |

---

## 9. Author Information (SSRN profile entry)

If SSRN asks for a co-author or affiliation update for this submission, confirm the existing profile already shows:

- **Name:** Pablo Ulpiano González Castro
- **Primary affiliation:** School of Visual Arts (SVA), MPS Branding Program, New York, NY
- **Secondary affiliation:** Third System™ (research entity)
- **Email:** pablou@pablou.com
- **Website:** pablou.com
- **ORCID:** 0009-0003-8968-9990

---

## 10. Date of Posting

**Suggested posting date:** 10 May 2026 (today, matching the date on the paper's title page and the data acquisition timestamp)

If you prefer to space submissions out from v0.10 (posted 9 May), 11 May or 12 May also works and doesn't conflict with anything in the deposit. The pre-registration lock timestamp (f20ade8, 10 May 2026 UTC) is what matters for the credibility argument; SSRN posting date is independent.

---

## 11. OSF Deposit (link from the paper's Data Availability statement)

Confirm the OSF deposit at osf.io/ec6wh/files/osfstorage/v11/ is uploaded **before** SSRN posting. The paper's Data Availability section points there. Upload order:

1. Final paper PDF (`v11_ssrn_paper_v2.pdf`)
2. Brand-format report (`v11_pmtrends_construct_validity.pdf`)
3. PRE_REGISTRATION.md (locked at f20ade8)
4. analysis/ folder (canonical_scoring.json, per_brand_paired.csv)
5. data/ folder (trends_raw, trends_processed, registries, validation logs)
6. figures/ folder (4 chart PDFs)
7. scripts/ folder (acquisition, rescaling, scoring, chart-building scripts)
8. MANIFEST.md describing the deposit lineage

Per memory: drag-and-drop via the OSF web UI at osf.io/ec6wh/files/osfstorage/v11/. Do not use osfclient.

---

## 12. Pre-submission Checklist

Run through before clicking Submit on SSRN:

- [ ] Paper PDF renders cleanly via `pandoc ... --include-in-header=preamble.tex`
- [ ] Title page shows: SSRN WORKING PAPER header / main title / italic tagline / version line / author block / date / disclaimer
- [ ] Abstract appears on page 2 with Keywords / JEL / Paper status below
- [ ] All four figures (F1 t1 scatter, F2 t2 scatter, F3 rank-shift, F4 partial residual) render inline at their expected sizes
- [ ] Table 1 (Pre-Registration Outcomes) renders with booktabs styling and 5 columns
- [ ] References list resolves all SSRN URLs as clickable links
- [ ] Declarations include Conflict of Interest, Funding, Data Availability
- [ ] Author Information block sits below Declarations
- [ ] Page count is 18–24 (similar to v0.9's 27 pages or v0.8's 25 pages)
- [ ] OSF deposit at /v11/ is complete and publicly viewable (run a fresh-browser test)
- [ ] PRE_REGISTRATION.md in the OSF deposit shows lock at commit f20ade8 prior to acquisition
- [ ] DEVIATIONS.md in /v11/ either lists deviations or states "None as of this draft"

---

## 13. After SSRN issues the v0.11 abstract ID

Memory update for the AIAS cross-cite list:

```
Add to userMemories:
v0.11 PM Software × Google Trends Construct Validity: SSRN abstract ID [NEW_ID]
```

Then update the in-progress Tri-System Brand Growth manuscript bibliography to cite the v0.11 SSRN ID alongside v0.6–v0.10.

---

## 14. Cover note (optional, if SSRN asks for "Notes to Editor")

Working-paper submission. Pre-registered. Phase 3 pilot in the AIAS Presence Measurement Programme; follows the cross-category baseline at SSRN 6720959 and the longitudinal re-baseline at SSRN 6736878. Construct-validity test against an external behavioural validator (Google Trends search interest). Single-category pilot in project management software; v0.12 and v0.13 expansion to three- and five-category replications planned. Pre-registration locked at git commit f20ade8 on 10 May 2026 UTC prior to acquisition; deposit at osf.io/ec6wh/.
