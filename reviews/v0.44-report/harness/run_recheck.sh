#!/bin/zsh
# Re-check round for the v0.44 report gate: one fresh read-only Claude Opus judge session verifies that the r1
# judge's edits were applied to the rebuilt PDF, and screens the changed text for new problems.
C="/Users/pablou/Library/Application Support/Claude/claude-code/2.1.330/4262a1273231/claude.app/Contents/MacOS/claude"
W=/Users/pablou/aias/_worktrees/v0.44-report
R=/tmp/v44review
RND=${1:-r2}
PREV=${2:-r1}
cd $R
cat > $R/rprompt_recheck_$RND.txt <<EOF
You are the review judge for a re-check round ($RND) of the AIAS v0.44 REPORT review gate (TS-FL-v0.44-r1, DRAFT, 2026-11-24). Rubric: $R/review-rubric-v1.md; judge brief: "Review judge brief" in $R/briefs.md.
The previous round's judge report is $R/${PREV}_judge.md (briefs: $R/${PREV}_report_b1.md, b2, b3, b5). The author has rebuilt the report. Deliverable now: $W/reports/output/TS-FL-v0.44-r1_known-but-not-named.pdf, text $R/report.txt, renders $R/rpng/p-01.png ... p-14.png; content module $W/reports/v44_report_content.py; chart builder $W/scripts/build_charts_v44_report.py; values files $W/papers/v0_44/v44_values.json and $W/reports/v44_report_values.json (script $W/reports/v44_report_values.py); sources $W/osf/v44/DEVIATIONS.md, $W/osf/v44/v44_verdicts.json, $W/papers/v0_44/v0_44_paper_draft.md (Declarations, Limitations).
Rules: managerial register, no H_ labels, 'named' not 'recommended' or 'suggested', chart title/insight/caption never repeat or paraphrase the finding headline, employer not named in the report and the small-print COI faithful to the paper's Declarations and DEVIATIONS Entry 0, AI-use statement verbatim, no v0.38/v0.39, every number from a values file by key.
Task: for each concrete edit (1-10) and each needs-Pablo item of the previous judge report, say applied / partly / not applied, with evidence from the new text or renders. Then screen all changed passages and every page render for new defects (numbers vs key displays, overflow, clipping, overlaps). End with counts and a verdict (passed / passed with notes / blocked (needs Pablo)). Use only Read, Grep and Glob; change nothing. At most about 900 words.
EOF
"$C" -p --model opus --allowedTools "Read Grep Glob" --disallowedTools "Bash Edit Write NotebookEdit WebFetch WebSearch" --add-dir $W < $R/rprompt_recheck_$RND.txt > $R/${RND}_recheck.md 2> $R/${RND}_err_recheck.txt
echo done > $R/${RND}_recheck_done
