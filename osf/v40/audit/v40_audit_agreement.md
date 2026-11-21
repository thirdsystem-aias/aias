# v0.40 audit: agreement of the AI-only analyst with the rule-based coder

No human check: two AI coders from two providers, blind to the rule-based codes and to each other, with a third model from a third provider breaking ties (DEVIATIONS 2026-11-21).

Coders: A claude-fable-5-2, B gpt-6.2-astra, tie-breaker T gemini-4-carbon. Spend $6.12 of the $25.00 cap; complete: True.

Threshold (section 5.5): kappa >= 0.80 on the gone-flag. Consensus vs rule kappa = 0.883: **met**.

| comparison | field | n | % agreement | kappa |
|---|---|---|---|---|
| consensus_vs_rule | subject | 6600 | 100.0 | 0.999 |
| consensus_vs_rule | ambiguous | 932 | 100.0 | 1.000 |
| consensus_vs_rule | gone_flag | 932 | 96.0 | 0.883 |
| consensus_vs_rule | successor_near | 168 | 97.0 | 0.933 |
| consensus_vs_rule | status_flag | 100 | 99.0 | 0.965 |
| A_vs_rule | subject | 6600 | 99.9 | 0.998 |
| A_vs_rule | ambiguous | 932 | 100.0 | 1.000 |
| A_vs_rule | gone_flag | 932 | 96.1 | 0.886 |
| A_vs_rule | successor_near | 168 | 97.6 | 0.947 |
| A_vs_rule | status_flag | 100 | 99.0 | 0.965 |
| B_vs_rule | subject | 6600 | 100.0 | 1.000 |
| B_vs_rule | ambiguous | 933 | 100.0 | 1.000 |
| B_vs_rule | gone_flag | 933 | 95.8 | 0.878 |
| B_vs_rule | successor_near | 168 | 98.8 | 0.973 |
| B_vs_rule | status_flag | 100 | 99.0 | 0.965 |
| A_vs_B | subject | 6600 | 99.9 | 0.998 |
| A_vs_B | ambiguous | 932 | 100.0 | 1.000 |
| A_vs_B | gone_flag | 932 | 99.5 | 0.985 |
| A_vs_B | successor_near | 168 | 97.6 | 0.946 |
| A_vs_B | status_flag | 100 | 100.0 | 1.000 |

Sample rates (rule-coded vs AI-coded, same answers): {"rule": {"status_ghost_answers": 77, "status_ghost_flag_rate": 0.987012987012987, "status_control_answers": 23, "status_control_flag_rate": 0.2608695652173913, "rec_ghost_mentions": 30, "rec_ghost_mentions_not_gone_flagged_rate": 0.8333333333333334}, "ai": {"status_ghost_answers": 77, "status_ghost_flag_rate": 0.987012987012987, "status_control_answers": 23, "status_control_flag_rate": 0.30434782608695654, "rec_ghost_mentions": 30, "rec_ghost_mentions_not_gone_flagged_rate": 0.6333333333333333}}
