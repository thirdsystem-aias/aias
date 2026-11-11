# DEVIATIONS — v0.43

Post-lock record for v0.43, locked as `v0.43-prereg-r1` (tag object 9955529f7c26407df2b24f8eb8523ba5b91d8380, commit 8c96d9cf8ead60105589269db69df398a2b8c329, 2026-11-11 00:31 CT). Each entry is recorded before the data it could affect.

## Entry 1 — clarification C11: the topic ID arrives in `q`, not in a field named `mid` (recorded 2026-11-11, before any search-interest request)

**Type:** logged clarification, not a deviation; ex ante: recorded after the day-1 autocomplete look-ups (`terms`) and before the sizing pull (`size`) or any other search-interest request.

**Locked text:** C7 (§3.2, §4): "The topic ID is the suggestion's `mid`."

**What was observed:** in the 111 day-1 look-ups (2026-11-11, after the lock; `registries/terms_v0_43.json`, 256,079 bytes, SHA-256 2e83420f2c693f394aa4cea5003c6b3a29545a7a732fcf6c12e482e27952bb56), SerpAPI's Google Trends autocomplete returned 666 suggestions, each with exactly the keys `link`, `q`, `serpapi_link`, `title` and `type`; none has a key named `mid`. All 555 suggestions whose `type` is not "Search term" carry the topic's Knowledge Graph ID in `q` (each begins with `/m/` or `/g/`); all 111 of type "Search term" carry plain text in `q`.

**Handling:** no change to code, data or rules. The locked parser (`scripts/trends_common_v0_43.py`, `choose_term`) takes the topic ID from `mid` when that key exists and otherwise from `q` when `q` begins with "/", so it read the ID of every topic suggestion. The `mid` of C7 is this ID (the name Google uses for it; SerpAPI returns it as `q`). The day-1 look-ups stand as run: 112 units from 111 distinct names, 62 resolved to a topic and 50 to a plain search term (`summary.share_topic` = 0.5536).

**Effect on inference:** none. The entry only names the response field that carries the topic ID.
