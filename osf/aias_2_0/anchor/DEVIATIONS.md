# DEVIATIONS — AIAS™ 2.0 synthesis outline

## Entry 1 — outline anchored on OSF instead of by a tag push (2026-11-09; deposit waits for Pablo's go)

**Type:** procedural; recorded before any t₃ result exists.

**Locked sequence (outline D10, §10):** commit → tag `aias-2-0-outline-locked` → `git push` → OSF deposit of the outline to `aias_2_0/prereg/` → first t₃ call, so that the synthesis's claims and its outcome-contingent wording (§5) are fixed blind to t₃.

**What happened:** the outline was committed and tagged locally on 2026-11-09 at 13:27:44 UTC (commit `f97db70`, tag object `02d0f9f`). Two things then departed from the sequence:
1. **No push.** GitHub write access to `thirdsystem-aias/aias` is not available (the same cause as v0.41 and v1.9 DEVIATIONS Entry 1).
2. **t₃ started before the outline's external anchor.** The v0.41 git anchor was deposited on OSF at 13:31:49–13:32:08 UTC and t₃ collection started right after it (v0.41 DEVIATIONS Entry 1; STATUS.md). The outline commit predates that deposit by about four minutes, but its own OSF deposit is a gate and waits for Pablo's go.

**Handling:** the same external anchor Pablo chose for v0.41 and v1.9 on Nov 9 (07:31 CT): deposit `prereg/aias_2_0_synthesis_outline.md` (byte-identical to the locked file) and this folder (`anchor/DEVIATIONS.md`, `anchor/git_anchor_aias_2_0_outline.json` with the tag object, commit, tree and SHA-256 of every locked file) on OSF, which timestamps them. Target: before any v0.41 or v1.9 Stage 2 result is computed. The tag is pushed when GitHub access exists; it must resolve to the recorded hashes.

**Effect on inference:** the outline adds no test; its confirmatory content is the v0.41 and v1.9 verdict rules, which are anchored. What the anchor certifies is that the synthesis's wording was fixed before t₃ results. The paper's Declarations report the commit time, the OSF deposit time and whether the deposit preceded the first t₃ verdict file; if it did not, the paper says so and treats §5 as committed-before-t₃ on the git record only.
