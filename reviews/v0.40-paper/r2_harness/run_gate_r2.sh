#!/bin/zsh
# Row 32 review gate, re-run (r2) for branch v0.40-paper-r2: same harness as /tmp/v40review (run_briefs.sh, run_judge.sh,
# run_report_gate.sh): fresh read-only Claude Opus sessions (-p --model opus, Read/Grep/Glob only).
# Paper: briefs 1-4 + judge. Report: briefs 1, 2, 3, 5 + judge.
C="/Users/pablou/Library/Application Support/Claude/claude-code/2.1.328/c141a31688d6/claude.app/Contents/MacOS/claude"
W=/Users/pablou/aias/_worktrees/v0.40-paper-r2
R=/tmp/v40review_r2
cd $R
CTX="Context for this re-run (r2): the pre-registrant's decisions of Sat 21 November 2026, 1:56 pm CT, are binding and are not to be re-opened: (1) H_Amplify stays FALSIFIED as registered; a dated post-scoring DEVIATIONS entry (Entry 2) records the ceiling of the registered ratio, computed in code (values file keys ceiling.*); the paper and report must say that the test could not have confirmed and must make no claim that AI flattens or exaggerates the leader. (2) Gemini 4 Carbon timing: accepted as disclosed, recorded in Entry 2, limitation kept. (3) The pre-registered reporting the locked scorer did not output is computed after scoring by $W/osf/v40/scripts/postscore_v0_40.py from the frozen coded mentions and labelled (values keys prereg_post.*; $W/osf/v40/v40_postscore.json; $W/osf/v40/v40_discover_status_answers.md); the gap is recorded in Entry 2. Judge whether the deliverable applies these decisions correctly and completely; flag anything that fails to. The previous gate's records are in $W/reviews/v0.40-paper/ and $W/reviews/v0.40-report/ (dated 2026-11-21)."
PSRC="Sources (read-only): $W/osf/v40/v40_values.md and .json; $W/osf/v40/v40_verdicts.json; locked pre-registration $W/osf/v40/prereg/PRE_REGISTRATION_v0_40.md; $W/osf/v40/DEVIATIONS.md; $W/osf/v40/audit/v40_audit_agreement.md; post-scoring file $W/osf/v40/v40_postscore.json and its script $W/osf/v40/scripts/postscore_v0_40.py; $W/osf/v40/v40_discover_status_answers.md; frozen registry $W/osf/v40/registries/out/; scorer $W/osf/v40/scripts/score_v0_40.py."
for b in 1 2 3 4; do
  cat > $R/prompt_b$b.txt <<EOF
You are a reviewer for the AIAS v0.40 paper review gate (item: v0.40 SSRN-format paper, revision r2, date 2026-11-21). Run ONLY Brief $b of $R/briefs.md, under its Common header, using the rubric $R/review-rubric-v1.md.
$CTX
Deliverable: the paper PDF $W/papers/v0_40/v0_40_ssrn_paper.pdf; its extracted text is $R/paper.txt (read the text; the six figures are described by their titles, axis labels and captions in the text, and their PNG renders are $R/fig_01.png ... $R/fig_06.png).
$PSRC
The paper's Markdown template with value keys: $W/papers/v0_40/v0_40_ssrn_paper_template.md
Use only Read, Grep and Glob. Change nothing. Reply with your report only (findings table and one-line verdict), at most about 1,200 words.
EOF
  "$C" -p --model opus --allowedTools "Read Grep Glob" --disallowedTools "Bash Edit Write NotebookEdit WebFetch WebSearch" --add-dir $W < $R/prompt_b$b.txt > $R/report_b$b.md 2> $R/err_b$b.txt &
done
RSRC="$PSRC The study's academic paper text $R/paper.txt (reviewed separately); report content module with value keys $W/reports/v40_report_content.py."
for b in 1 2 3 5; do
  EXTRA=""
  [ $b = 5 ] && EXTRA="Brief 5: First-time reader. Goal: read as a brand leader seeing it cold, and list everything that blocks understanding: every number whose origin is not stated nearby; instructions that cannot be followed; labels, captions or chart lines that repeat each other or the finding headline; jargon not explained at first use; anything you did not understand; anything cut off, overlapping or unreadable. Tick each rubric principle met / not met / not applicable, quoting the passage for every not met. Severity: a number with no stated origin is a fix; a claim that misleads a cold reader is a blocker; style points are notes. Brief 5 note: the deliverable is a PDF report, not a web page; there are no phone screenshots. Read the page renders in order and judge legibility at print size; mark P1 (phone) not applicable. The rubric is approved (Nov 21)."
  cat > $R/rprompt_b$b.txt <<EOF
You are a reviewer for the AIAS v0.40 REPORT review gate (item: v0.40 Third System flagship report TS-FL-v0.40-r1, managerial register, re-run r2, date 2026-11-21). Run ONLY Brief $b of $R/briefs.md (for Brief 5, use the "Brief 5: First-time reader" text below), under its Common header, using the rubric $R/review-rubric-v1.md.
$EXTRA
$CTX
Deliverable: the report PDF $W/reports/output/TS-FL-v0.40-r1_leaders-challengers-and-ghosts.pdf; extracted text $R/report.txt; page renders $R/rpng/p-01.png ... p-15.png (read them).
$RSRC
Report-register rules: no hypothesis labels; "named", not "recommended", for what the measure counts; one chart per finding, the chart title says what is plotted and neither the title nor the insight line nor the caption repeats or paraphrases the finding headline; the employer is not named in the report (only in the paper's Declarations); every number comes from the values file.
Use only Read, Grep and Glob. Change nothing. Reply with your report only (findings table and one-line verdict), at most about 900 words.
EOF
  "$C" -p --model opus --allowedTools "Read Grep Glob" --disallowedTools "Bash Edit Write NotebookEdit WebFetch WebSearch" --add-dir $W < $R/rprompt_b$b.txt > $R/rreport_b$b.md 2> $R/rerr_b$b.txt &
done
wait
echo done > $R/briefs_done
cat > $R/prompt_judge.txt <<EOF
You are the review judge for the AIAS v0.40 paper review gate (item: v0.40 SSRN-format paper, revision r2, date 2026-11-21). Follow the "Review judge brief" in $R/briefs.md under its Common header, with the rubric $R/review-rubric-v1.md.
$CTX
Deliverable: the paper PDF $W/papers/v0_40/v0_40_ssrn_paper.pdf; its extracted text $R/paper.txt; figure renders $R/fig_01.png ... $R/fig_06.png; Markdown template with value keys $W/papers/v0_40/v0_40_ssrn_paper_template.md.
$PSRC
Programme record supplied for the Declarations (the project's standing conventions file, quoted): "Denon / Harman (found Nov 10, 2026): Harman International (a Samsung subsidiary since March 2017; deal agreed Nov 2016) completed its acquisition of Masimo's Sound United brands, Denon included, on Sep 23, 2025. Denon, chosen for v0.19 in place of AKG, was therefore already a Samsung-group brand. Every COI declaration carrying the v0.19 disclosure must state this." and "COI notes (found Nov 11, 2026 by the v0.62 r3 screen ...): Samsung's agency Cheil Worldwide, or its Iris unit, has worked for five omnibus-registry brands ... sources in v0.62 DEVIATIONS Entry 0, Part F." and the SSRN registry: v0.37 is SSRN 7685199 (submitted Nov 9, 2026).
Brief reports to judge: $R/report_b1.md (numbers and citations), $R/report_b2.md (verdict and framing), $R/report_b3.md (consistency), $R/report_b4.md (editor screen).
For each finding: holds / doesn't hold / needs Pablo, with your own evidence and a severity (blocker, fix, note); merge duplicates; then list gaps no brief examined and check the most important ones yourself. In particular verify by your own arithmetic the ceiling values the paper prints (ceiling = (answers / n) / p0 for each category) and that no passage claims AI flattens or exaggerates the leader. End with counts and a verdict (passed / passed with notes / blocked (needs Pablo)), and a numbered list of the concrete edits the author must make. Use only Read, Grep and Glob; change nothing. At most about 1,800 words.
EOF
"$C" -p --model opus --allowedTools "Read Grep Glob" --disallowedTools "Bash Edit Write NotebookEdit WebFetch WebSearch" --add-dir $W < $R/prompt_judge.txt > $R/judge.md 2> $R/err_judge.txt &
cat > $R/rprompt_judge.txt <<EOF
You are the review judge for the AIAS v0.40 REPORT review gate (item: v0.40 flagship report TS-FL-v0.40-r1, re-run r2, 2026-11-21). Follow the "Review judge brief" in $R/briefs.md with the rubric $R/review-rubric-v1.md.
$CTX
Deliverable: $W/reports/output/TS-FL-v0.40-r1_leaders-challengers-and-ghosts.pdf, text $R/report.txt, renders $R/rpng/p-01.png ... p-15.png. $RSRC
Brief reports: $R/rreport_b1.md, $R/rreport_b2.md, $R/rreport_b3.md, $R/rreport_b5.md. For each finding: holds / doesn't hold / needs Pablo with your evidence and severity; merge duplicates; list gaps and check the most important; counts and verdict (passed / passed with notes / blocked (needs Pablo)); then a numbered list of concrete edits. Use only Read, Grep and Glob; change nothing. At most about 1,200 words.
EOF
"$C" -p --model opus --allowedTools "Read Grep Glob" --disallowedTools "Bash Edit Write NotebookEdit WebFetch WebSearch" --add-dir $W < $R/rprompt_judge.txt > $R/rjudge.md 2> $R/rerr_judge.txt &
wait
echo done > $R/gate_done
