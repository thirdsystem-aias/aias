#!/bin/zsh
# Row 32 review gate for the v0.44 flagship report TS-FL-v0.44-r1 (2026-11-24). Same harness as the v0.40 report gate
# (reviews/v0.40-report on branch v0.40-paper-r2): fresh read-only Claude Opus sessions (-p --model opus,
# Read/Grep/Glob only). Report: briefs 1, 2, 3, 5 + judge. Briefs and rubric: copies of the project docs
# claude/review-briefs-v1-draft.md and claude/review-rubric-v1.md (as used for v0.40), in $R.
# Usage: run_gate.sh <round>   (round tag, e.g. r1)
C="/Users/pablou/Library/Application Support/Claude/claude-code/2.1.330/4262a1273231/claude.app/Contents/MacOS/claude"
W=/Users/pablou/aias/_worktrees/v0.44-report
R=/tmp/v44review
RND=${1:-r1}
cd $R
PDF=$W/reports/output/TS-FL-v0.44-r1_known-but-not-named.pdf
SRC="Sources (read-only): the paper's values file $W/papers/v0_44/v44_values.json (written by $W/papers/v0_44/values_v0_44.py); the report's added values file $W/reports/v44_report_values.json (written by $W/reports/v44_report_values.py from the verdict file, unit table and the locked scorer's constants); $W/osf/v44/v44_verdicts.json; $W/osf/v44/v44_unit_table.csv; $W/osf/v44/DEVIATIONS.md; locked pre-registration $W/osf/v44/prereg/PRE_REGISTRATION_v0_44.md; scorer $W/osf/v44/scripts/score_v0_44.py; the study's academic paper (published, 22 pp) text $R/paper.txt and its Markdown $W/papers/v0_44/v0_44_paper_draft.md; report content module with value keys $W/reports/v44_report_content.py; report chart builder $W/scripts/build_charts_v44_report.py; report builder $W/reports/build_report_v44_r1.py."
RULES="Report-register rules: managerial register, P1-P5 propositions, no hypothesis labels (H_...); 'named', not 'recommended', for what the measure counts; one chart per finding, the chart title says what is plotted and neither the chart title nor its insight line nor the caption repeats or paraphrases the finding headline; colour never the only cue in a chart; the author's employer is not named in the report (only in the paper's Declarations; the brand file's commercial-outputs rule), and the report's small-print COI must be faithful to the paper's Declarations COI and DEVIATIONS Entry 0; the AI-use statement verbatim: 'During the preparation of this work the author used AI tools (Anthropic's Claude) to assist with study design, analysis and writing. The author reviewed and edited all content and takes full responsibility for it.'; studies v0.38 and v0.39 are never mentioned; every number comes from one of the two values files by key (no typed numbers); the two refused starts (DEVIATIONS Entry 3) and the limitations are stated honestly, as in the paper. Findings 04 and 05 are pre-registered descriptives (no verdict)."
for b in 1 2 3 5; do
  EXTRA=""
  [ $b = 5 ] && EXTRA="Brief 5: First-time reader. Goal: read as a brand leader seeing it cold, and list everything that blocks understanding: every number whose origin is not stated nearby; instructions that cannot be followed; labels, captions or chart lines that repeat each other or the finding headline; jargon not explained at first use; anything you did not understand; anything cut off, overlapping or unreadable. Tick each rubric principle met / not met / not applicable, quoting the passage for every not met. Severity: a number with no stated origin is a fix; a claim that misleads a cold reader is a blocker; style points are notes. Brief 5 note: the deliverable is a PDF report, not a web page; there are no phone screenshots. Read the page renders in order and judge legibility at print size; mark P1 (phone) not applicable. The rubric is approved (Nov 21)."
  cat > $R/rprompt_b$b.txt <<EOF
You are a reviewer for the AIAS v0.44 REPORT review gate (item: v0.44 Third System flagship report TS-FL-v0.44-r1, managerial register, DRAFT, round $RND, date 2026-11-24). Run ONLY Brief $b of $R/briefs.md (for Brief 5, use the "Brief 5: First-time reader" text below), under its Common header, using the rubric $R/review-rubric-v1.md.
$EXTRA
Deliverable: the report PDF $PDF; extracted text $R/report.txt; page renders $R/rpng/p-01.png ... p-14.png (read them).
$SRC
$RULES
Use only Read, Grep and Glob. Change nothing. Reply with your report only (findings table and one-line verdict), at most about 900 words.
EOF
  "$C" -p --model opus --allowedTools "Read Grep Glob" --disallowedTools "Bash Edit Write NotebookEdit WebFetch WebSearch" --add-dir $W < $R/rprompt_b$b.txt > $R/${RND}_report_b$b.md 2> $R/${RND}_err_b$b.txt &
done
wait
cat > $R/rprompt_judge.txt <<EOF
You are the review judge for the AIAS v0.44 REPORT review gate (item: v0.44 flagship report TS-FL-v0.44-r1, DRAFT, round $RND, 2026-11-24). Follow the "Review judge brief" in $R/briefs.md with the rubric $R/review-rubric-v1.md.
Deliverable: $PDF, text $R/report.txt, renders $R/rpng/p-01.png ... p-14.png. $SRC
$RULES
Brief reports: $R/${RND}_report_b1.md, $R/${RND}_report_b2.md, $R/${RND}_report_b3.md, $R/${RND}_report_b5.md. For each finding: holds / doesn't hold / needs Pablo with your evidence and severity; merge duplicates; list gaps and check the most important yourself (in particular: that every printed number matches its key's display string, and that the COI small print matches the paper's Declarations). Counts and verdict (passed / passed with notes / blocked (needs Pablo)); then a numbered list of concrete edits. Use only Read, Grep and Glob; change nothing. At most about 1,200 words.
EOF
"$C" -p --model opus --allowedTools "Read Grep Glob" --disallowedTools "Bash Edit Write NotebookEdit WebFetch WebSearch" --add-dir $W < $R/rprompt_judge.txt > $R/${RND}_judge.md 2> $R/${RND}_err_judge.txt
echo done > $R/${RND}_gate_done
