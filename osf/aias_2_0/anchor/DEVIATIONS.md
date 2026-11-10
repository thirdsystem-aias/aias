# DEVIATIONS — AIAS™ 2.0 synthesis outline

## Entry 1 — outline anchored on OSF instead of by a tag push (2026-11-09; deposit waits for Pablo's go)

**Type:** procedural; recorded before any t₃ result exists.

**Locked sequence (outline D10, §10):** commit → tag `aias-2-0-outline-locked` → `git push` → OSF deposit of the outline to `aias_2_0/prereg/` → first t₃ call, so that the synthesis's claims and its outcome-contingent wording (§5) are fixed blind to t₃.

**What happened:** the outline was committed and tagged locally on 2026-11-09 at 13:27:44 UTC (commit `f97db70`, tag object `02d0f9f`). Two things then departed from the sequence:
1. **No push.** GitHub write access to `thirdsystem-aias/aias` is not available (the same cause as v0.41 and v1.9 DEVIATIONS Entry 1).
2. **t₃ started before the outline's external anchor.** The v0.41 git anchor was deposited on OSF at 13:31:49–13:32:08 UTC and t₃ collection started right after it (v0.41 DEVIATIONS Entry 1; STATUS.md). The outline commit predates that deposit by about four minutes, but its own OSF deposit is a gate and waits for Pablo's go.

**Handling:** the same external anchor Pablo chose for v0.41 and v1.9 on Nov 9 (07:31 CT): deposit `prereg/aias_2_0_synthesis_outline.md` (byte-identical to the locked file) and this folder (`anchor/DEVIATIONS.md`, `anchor/git_anchor_aias_2_0_outline.json` with the tag object, commit, tree and SHA-256 of every locked file) on OSF, which timestamps them. Target: before any v0.41 or v1.9 Stage 2 result is computed. The tag is pushed when GitHub access exists; it must resolve to the recorded hashes.

**Effect on inference:** the outline adds no test; its confirmatory content is the v0.41 and v1.9 verdict rules, which are anchored. What the anchor certifies is that the synthesis's wording was fixed before t₃ results. The paper's Declarations report the commit time, the OSF deposit time and whether the deposit preceded the first t₃ verdict file; if it did not, the paper says so and treats §5 as committed-before-t₃ on the git record only.

## Entry 2 — report figures and report timing (2026-11-10)

**Type:** procedural; recorded at the paper and report lock, after all results were known; no test, threshold or verdict is affected.

**Planned (outline §9):** a brand-format report with three figures, built after the paper received its SSRN ID.

**What happened:** the report carries five figures, one per finding (P1–P5), under the program rule adopted on 2026-11-09 that every finding in a brand-format report has its own chart, titled for what it plots. Every value in the five charts is read from the locked records and asserted in `reports/build_charts_aias_2_0_report.py`. The report is published with the paper on OSF and the website before the SSRN submission, because SSRN submissions now wait for the AI-use-statement decision and the program's SSRN pacing (at most three a week), and the website and OSF do not wait for SSRN (program rule, 2026-11-09).

**Also recorded at this lock:** a final full-draft review (Claude Fable, read-only) led to wording corrections in the paper and the report (no number changed; new numbers quoted in the paper are added to `papers/aias_2_0/check_paper_numbers.py`, 54/54 checks). The paper's reference titles for the program's own SSRN papers were checked against the titles SSRN registered with Crossref (DOI 10.2139/ssrn.ID) on 2026-11-10, because the SSRN author dashboard needs the author's sign-in; eight titles were corrected (v0.19–v0.23, v0.33, v1.7 and AIAS 1.0), and five now carry their version label inside the title, as registered or submitted (v0.34, v0.37, v0.41, v1.3 and v1.9). v0.41 (7685100), v1.9 (7685126) and v0.37 (7685199) were not yet registered; their titles are taken from their submission packets.
