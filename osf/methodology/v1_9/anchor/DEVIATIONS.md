# DEVIATIONS

## Entry 1 — lock anchored on OSF before the GitHub push (2026-11-09, before the first t3 call)

**Type:** procedural; ex ante (recorded before any t3 study call).

**Locked sequence:** content lock → commit → tag `v1.9-prereg-r1` → `git push` → OSF deposit → verify both remotes → first t3 call.

**What happened:** the content was locked, committed and tagged, and the pre-registration was deposited on OSF and verified byte for byte (2026-11-09, ~06:40 UTC). The push to GitHub could not be made: no GitHub credentials are available on the acquisition machine, and the session's GitHub access does not include write access to `thirdsystem-aias/aias` (push refused, HTTP 403).

**Handling (Pablo's decision, 2026-11-09 07:31 CT):** proceed with OSF as the external anchor. Before the first t3 call, this file and `git_anchor_*.json` (tag object, commit and tree hashes, and the SHA-256 of every locked file) were deposited on OSF, which timestamps them. The tag is pushed to GitHub as soon as access exists; the pushed tag must resolve to the recorded hashes, which anyone can check.

**Effect on inference:** none. The pre-registration content and its timestamp precede all t3 data; only the order of the two external anchors changes.
