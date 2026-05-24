# AIAS™ 1.0 Housekeeping — Claude Code Kickoff Prompt

**Save location:** `~/aias/aias_1_0_housekeeping_kickoff_prompt.md`

**Usage:** Copy the fenced markdown block below and paste into a fresh Claude Code session opened in `~/aias/`. The session reads `CLAUDE.md` first, then this prompt drives the work. Bounded scope: one session, documentation-only changes, no new substantive content.

---

```markdown
We're closing the loose ends on the AIAS™ 1.0 cycle. This is a documentation-only 
session — no new substantive content, no new measurement, no new builders. The 
synthesis paper (SSRN 6817841) and brand-format report (r2 locked at 
aias-1-0-report-locked-r2) are both shipped. This session updates the program's 
documentation trail to reflect that ship state.

═══════════════════════════════════════════════════════════════════════════════
BEFORE ANY EDITS — READ THESE
═══════════════════════════════════════════════════════════════════════════════

1. CLAUDE.md (current state of the project context document)
2. The Tri-System Brand Growth MSI Working Paper bibliography section — find 
   the current bibliography file in the Tri-System paper's directory (likely 
   ~/aias/papers/tri_system/ or wherever the MSI WP lives)

═══════════════════════════════════════════════════════════════════════════════
SCOPE — Three deliverables, bounded
═══════════════════════════════════════════════════════════════════════════════

1. CLAUDE.md backfill — update the project context document to reflect AIAS™ 
   1.0 final ship state (synthesis paper SSRN 6817841, brand-format report 
   at r2 lock tag, full milestone status)

2. Tri-System MSI WP bibliography backfill — add three SSRN cross-citations:
   - v0.21 Cosmetics (SSRN 6815378)
   - v1.6 Methodology (SSRN 6816340)
   - AIAS™ 1.0 Synthesis (SSRN 6817841)

3. Surface anything else from cycle close — git tag inventory, OSF deposit 
   completeness, any straggler files that should be committed or cleaned up. 
   Documentation-only fixes; no substantive changes.

═══════════════════════════════════════════════════════════════════════════════
DELIVERABLE 1 — CLAUDE.md backfill
═══════════════════════════════════════════════════════════════════════════════

Read CLAUDE.md first, then apply these updates in the existing structure:

a. PHASE SSRN ID REGISTRY — verify these entries exist; add any missing:
   - v0.16 — 6791999 (kitchen knives)
   - v0.17 — 6802261 (premium kitchenware)
   - v0.18 — 6806558 (indie fragrance)
   - v0.19 — 6809182 (audiophile headphones)
   - v0.20 — 6811441 (skincare)
   - v0.21 — 6815378 (cosmetics)

b. METHODOLOGY SSRN ID REGISTRY — verify these entries exist; add any missing:
   - v1.2 — 6761698 (Construct Validity / Four-Regime Taxonomy)
   - v1.3 — 6797679 (Phase A Pivot-Validation)
   - v1.4 — 6799479 (Recognition × Recall Decomposition)
   - v1.5 — 6810758 (Multi-Statistic C2 + Two-Channel Recall)
   - v1.6 — 6816340 (Substrate Pre-Screen + IL Direct + Phantom)

c. SYNTHESIS REGISTRY — add new section if not present:
   - AIAS™ 1.0 — 6817841 (Five-Substrate Foundational Construct Claim, May 2026)
   - Tri-System Brand Growth — 6659000 (foundational architectural paper)

d. CURRENT STATE — update to reflect:
   - AIAS™ 1.0 synthesis paper SHIPPED (SSRN 6817841, May 2026)
   - AIAS™ 1.0 brand-format Third System™ report SHIPPED (locked at 
     aias-1-0-report-locked-r2)
   - Active next deliverable: JAR submission of AIAS™ 1.0 synthesis paper 
     (2–3 sessions, async); then v0.22 prospective phase under v1.6

e. AIAS™ 1.0 SHIP STATE MILESTONES section — add if not present:
   - Five-substrate empirical anchor base complete (kitchenware / fragrance 
     / audio / skincare / cosmetics)
   - Six phase papers shipped (v0.16 → v0.21)
   - Five methodology papers shipped (v1.2 → v1.6)
   - Foundational construct claim staked under pre-registration discipline
   - Construct validity + behavioral correlate explicitly held as Phase 3 
     future work
   - Version-numbering discipline: AIAS™ 1.0 → 6.0 binds to measurement 
     surface, not architectural ambition

f. GIT TAG INVENTORY — verify all AIAS™ 1.0 lock tags are documented:
   - aias-1-0-outline-locked (36918dc)
   - aias-1-0-data-locked (7298411)
   - aias-1-0-charts-locked (5f6bf70)
   - aias-1-0-paper-locked
   - aias-1-0-report-locked (a199b93, original r1 — broken layout, preserved 
     for pre-reg integrity)
   - aias-1-0-report-locked-r2 (fix commit, r2 — shipping version)

g. PRE-FLIGHT PROTOCOL — confirm aias-preflight-visual-inspection rule is 
   documented as permanent requirement for brand-format report renders.

After CLAUDE.md updates: commit as documentation-only change.

   git add CLAUDE.md
   git commit -m "CLAUDE.md: backfill AIAS 1.0 cycle final ship state"

═══════════════════════════════════════════════════════════════════════════════
DELIVERABLE 2 — Tri-System MSI WP bibliography backfill
═══════════════════════════════════════════════════════════════════════════════

Locate the Tri-System Brand Growth MSI Working Paper bibliography file. Likely 
at ~/aias/papers/tri_system/ or similar. Surface the file location before 
editing.

Add three SSRN cross-citations to the existing bibliography in alphabetical-
by-year order:

   González Castro, P. U. (2026). The AIAS Presence Measurement Protocol: 
   Substrate Pre-Screening, Independent Moderator Pathway, and Phantom Brand 
   Persistence Phase B Extension (v1.6). SSRN Working Paper. 
   https://ssrn.com/abstract=6816340

   González Castro, P. U. (2026). Type 2 Confirmation, Recognition Ceiling, 
   and Phantom Brand Persistence on a Cosmetics IL-Gradient Substrate (v0.21). 
   SSRN Working Paper. https://ssrn.com/abstract=6815378

   González Castro, P. U. (2026). AI Availability as a Third Measurable Layer 
   of Brand Availability: Five-Substrate Empirical Anchoring of the AIAS™ 
   Presence Measurement Protocol (AIAS 1.0). SSRN Working Paper. 
   https://ssrn.com/abstract=6817841

If the Tri-System WP also has inline citations to the AIAS phase chain, add 
in-line cross-references where the v0.21 / v1.6 / AIAS™ 1.0 findings could 
strengthen the WP's empirical anchor — but only where natural, no forced 
insertions. Surface candidate locations before editing if uncertain.

After bibliography updates: commit as documentation-only change.

   git add papers/tri_system/  # adjust path to actual file
   git commit -m "Tri-System MSI WP: backfill v0.21, v1.6, AIAS 1.0 SSRN citations"

═══════════════════════════════════════════════════════════════════════════════
DELIVERABLE 3 — Cycle-close inspection
═══════════════════════════════════════════════════════════════════════════════

Surface any straggler items from the AIAS™ 1.0 cycle:

a. Git status check — any uncommitted files in the working tree? Any 
   .DS_Store or __pycache__ that should be cleaned? Any test outputs sitting 
   around?

b. OSF deposit completeness — check osf.io/ec6wh/aias_1_0/ tree for missing 
   subtrees. Expected:
   - paper/ (synthesis paper PDF + draft .md + build script)
   - figures/ (chart_01 through chart_06)
   - scoring/ (synthesis_data.json + synthesis_data.py + chart builder)
   - prereg/ (outline + SSRN submission packet + kickoff prompt)
   - reports/ (brand-format report PDF — r2 version) 
   
   Verify reports/ deposit reflects r2 (not r1). If r1 is still on OSF and 
   r2 wasn't successfully overwritten, surface this — overwrite via patched 
   osf_upload.py.

c. Git tag verification — run git tag -l "aias-1-0*" and confirm all six 
   tags exist locally and on origin. If aias-1-0-report-locked-r2 didn't 
   push successfully, surface this.

d. Any kickoff prompts that should be archived — kickoff_prompt.md for the 
   synthesis paper and reports/aias_1_0_report_kickoff_prompt.md for the 
   brand-format report. Both should live in their canonical locations for 
   future session restart context.

For each straggler surfaced: documentation-only fix, single commit per 
category.

═══════════════════════════════════════════════════════════════════════════════
WHAT NOT TO DO IN THIS SESSION
═══════════════════════════════════════════════════════════════════════════════

- Don't re-render any PDFs
- Don't touch any chart builders or content modules
- Don't address the deferred items (P1 chart-caption gap, font glyph fallback, 
  P5 vertical rhythm, P2/P4 orphan headings) — these are tracked for a future 
  cycle that addresses chart-builder issues cross-cutting both papers
- Don't start JAR submission packaging (that's its own 2–3 session 
  deliverable)
- Don't start v0.22 substrate selection or pre-reg work
- Don't refactor anything

Documentation-only. One session. Bounded scope.

═══════════════════════════════════════════════════════════════════════════════
START HERE
═══════════════════════════════════════════════════════════════════════════════

Read CLAUDE.md first. Then run git status + git tag -l "aias-1-0*" to 
surface the current state. Walk through Deliverable 1 → 2 → 3 in order. 
Surface findings at each deliverable before applying edits; commit per 
deliverable.

Holding for explicit go-ahead on each commit (same friction protocol as 
the synthesis paper + brand-format report sessions).
```

---

## Notes for Pablo (not part of the prompt)

**Estimated effort:** 1 session, 30–60 minutes elapsed Claude Code time. Three deliverables, none substantive, all documentation hygiene.

**Why this matters even though it's "just housekeeping":** the program's credibility lives in its documentation trail. CLAUDE.md is the restart context for every future session (you've watched it carry seven program updates this run). The Tri-System MSI WP bibliography update is what lets future citers find the AIAS™ 1.0 chain when they read Tri-System — it's how the program's papers become discoverable as a connected body of work.

**On the deferred items:** the kickoff prompt explicitly tells Claude Code NOT to address P1 chart-caption gaps, font glyph fallback, P5 vertical rhythm, or P2/P4 orphan headings in this session. These items are tracked for a future cycle that addresses chart-builder issues cross-cutting the SSRN paper + brand-format report in one coherent pass. Mixing them into housekeeping would dilute the cycle's documentation focus and risk new edits that need their own pre-flight.

**After this session closes:** AIAS™ 1.0 is genuinely done. JAR submission (Track 2) becomes the next async work item; v0.22 (Track 3) becomes the next major build. Both kickoff prompts can be drafted in their own sessions.
