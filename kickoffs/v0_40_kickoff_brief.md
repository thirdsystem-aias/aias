AIAS v0.40 — flagship study kickoff

You are working with Pablo Ulpiano González Castro on the AIAS™ research program (Third System). This chat designs, drafts and decides; Claude Code on Pablo's Mac (~/aias) executes; Pablo relays. Read the project docs first.

The job. Design and run AIAS v0.40, the flagship study for the new thirdsystem.ai launch (target Dec 14, 2026). It must be:

	•	surprising and useful to marketers in any category;
	•	fully independent: no focal brand, no lessons addressed to a brand, no brand contacted;
	•	anchored to public, official data;
	•	clear of conflict of interest: Pablo works at Samsung Electronics America, so no category where Samsung competes.

Working title: Leaders, challengers and ghosts. Two US categories reshaped by mergers and failures.

	•	RQ1 (MSI paper, proposition P1): does AI's share of recommendations track real market share, amplify the leader (Double Jeopardy) or flatten it?
	•	RQ2: do brands that disappeared through a merger, failure or rename still appear in AI answers? Does that presence decay with the time between the exit and each model's training cutoff? Do answers say the brand is gone?
	•	Prior evidence: Mint was named in 44.8% of answers 25 months after closing (v0.10), while five car brands closed in 2001–2010 were named in 0 of 18 answers (v0.22). Find the curve.

Categories (confirm at scope lock).

	1.	US airlines: share from BTS domestic market share (revenue passenger miles). Ghost candidates: Virgin America, US Airways, Continental, AirTran, Northwest. Status checks: Hawaiian, Spirit.
	2.	US retail banks: share from FDIC Summary of Deposits. Ghost candidates: SunTrust and BB&T (now Truist), Wachovia, Washington Mutual, First Republic, Silicon Valley Bank, Signature, MUFG Union Bank, TCF, People's United, BBVA USA. Status check: Discover.

Every candidate, date and status is a lead: verify each against a primary source and cite it.

Design to draft (Pablo decides at lock).

	•	Registry: built mechanically: current brands covering at least 90% of official share, plus every exit in a dated window (propose 2008–2025) with its official date and successor. Old and new names are aliases. Frozen before the lock.
	•	Probes per category: generic recommendations, need-specific ones, and one recognition probe and one status probe per ghost.
	•	Legacy arm: the six-model panel used from v0.17 to v0.39, at temperature 0 with a 2,048-token cap. It must finish before 2026-11-24, the earliest possible retirement of Claude Opus 4.5. Decide the Gemini 2.5 Flash cap problem before the lock.
	•	Current arm: Claude Opus 5.5, GPT-6 Astra and Gemini 4 Argon, each with search off and on. Propose repeats (for example 3 runs per cell).
	•	Measures:
	•	Presence and first-mention share;
	•	AI share against market share (ratio and log-log slope);
	•	ghost Presence against the time from exit to each model's cutoff;
	•	whether an answer flags the brand as gone (within ±150 characters);
	•	use of the old name vs the new one.
	•	Coding: automated with aliases, then an analyst audit of a declared sample.

Hypotheses. H_Reinforce, H_Amplify, H_Afterlife, H_Decay, H_Flag and H_Search, each with a verdict rule (CONFIRMED / PARTIAL / UNDETERMINED / FALSIFIED), thresholds and an exact or permutation test written before acquisition. Add manipulation checks, descriptives and limitations.

Conventions.

	•	Fork with python3 scripts/aias_new_phase.py --from v0.39 --to v0.40 --substrate "<label>" --dry-run, then remove every bit of cloned v0.39 content.
	•	Lock at tag v0.40-prereg-r1 and deposit to OSF (ec6wh → v40/prereg/) before any study probe.
	•	Log deviations; report every test, including failures. Never invent a number, source or date.
	•	Deliverables: the Third System report, the SSRN-format paper, and data on OSF.
	•	Citations: the MSI paper (26-132, to confirm), and Shaw & Nave wherever "System 3" appears.
	•	Disclosure: independent research; the author's employer, and why these categories avoid it.

Site hand-off. A study folder (metadata, files, page counts, featured: true), three headline numbers with sources, explorer CSVs, and one claims-register row per number.

First reply.

	1.	Restate the design in one screen and list Pablo's decisions, with your recommendation for each: one category or both, the ghost window, repeats, the Gemini cap, probe counts, and dates working back from Nov 23.
	2.	On his "go", give the scaffold command, then draft the registry with sources.