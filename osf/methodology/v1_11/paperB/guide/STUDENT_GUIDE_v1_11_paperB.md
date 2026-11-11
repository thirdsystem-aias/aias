# Student guide, Sentiment Paper B (two pages), as read for the pre-registration

Source: https://claude.ai/artifact/4sCt6DcfA4RD6h4TdvUdZZ (Design canvas "Student guide — Labeling AI answers about brands"), version `1794367225-74d8`, read 2026-11-11 with the Artifact tool's read action (no web fetch). The two artboards are saved byte for byte in `guide/source/`; this file is generated from them by `lock/paperB_lock_v1_11.py --guide-md` (text only: one line per block element, HTML entities decoded, spaces collapsed; layout, colours and bold dropped). The words are the guide's, unchanged.

| Page | File | SHA-256 |
|---|---|---|
| 1 | `guide/source/Main.dc.html` | `fc577e17cc7664dad1e6d85fe6c6b00e5e9762f62c56ae98d3cdd62dee4c1744` |
| 2 | `guide/source/Rules.dc.html` | `806cd6313650b33b99a3fd8e557ddb67c0dd27068852b42ea233e5e4fafa9d23` |

## Page 1

```text
SVA MPS BRANDING · CLASS OF 2027 Third System™ research · page 1 of 2
OPTIONAL · ABOUT 45 MINUTES · NOT GRADED
Labeling AI answers about brands
You'll read about 55 short AI answers and mark the tone toward one brand in each. Your labels show whether an AI judges tone the way people do.
SIGN UP BY
Nov 20
FORM ARRIVES
Nov 23
LABELS DUE
Dec 4
RESULTS TOGETHER
Apr 21
Four questions for each answer
About the named brand only. Examples use a made-up brand, “Halvor”.
1
What's the tone toward the brand?
+2 · Strongly favorable
“The best knife you can buy.”
+1 · Favorable
“Well regarded and good value.”
0 · Neutral or balanced
“Makes knives from $80 to $150.”
−1 · Unfavorable
“A bit overpriced.”
−2 · Strongly unfavorable
“Skip it; the handles crack.”
Not about this brand
“I don't know this brand.”
2
Praise and criticism?
Yes or No
If Yes, your tone is the overall balance: 0 when both sides weigh about the same.
3
Where does the judgment come from?
No judgment · facts only
The AI's own voice · “Halvor is overpriced.”
Quoted sources · “Reviewers rate it highly.”
Both · “Testers love it, and I agree.”
4
How sure?
Sure or Not sure
Use “Not sure” freely; it helps.
Only the text counts, not your opinion of the brand. Work alone and don't look anything up. Rules for hard cases, and the exact instructions the AI judge gets, are on page 2.
How your labels will be used
Your name is replaced by a code before analysis; only I keep the key.
I use AI tools (Claude) to help analyze the coded data.
Coded labels, with no names, go on OSF, a public research archive. Results appear in a paper, on thirdsystem.ai and in Third System talks.
You're named only if you ask to be thanked in the paper.
You can stop at any time, and withdraw your labels until December 18 by emailing pablou@pablou.com.
Signing up means you've read this and agree to take part.Questions: pablou@pablou.com or Emily Weiland
```

## Page 2

```text
LABELING AI ANSWERS ABOUT BRANDS Third System™ research · page 2 of 2
Rules for hard cases
Judge the target brand only. Ignore what the text says about other brands, unless it compares them with the target brand.
Being listed is not tone. Being named, included in a list of picks, or listed first is not an evaluation. Rate the words that describe the brand. Just named, with nothing said about it: tone 0, No judgment.
Facts are not praise. “Has a 10-year warranty” is 0; “stands out for its generous 10-year warranty” is +1.
Reported opinions count. Awards, ratings, complaints and recalls that the text reports are evaluations. “Some owners mention quality issues” is −1, from Quoted sources.
Go by the overall impression. One small caveat inside strong praise is still favorable. Use 0 for mixed texts only when neither side wins.
Work alone. Don't look anything up, don't compare with classmates before April 21, and don't go back to change an answer after you have moved on.
The exact instructions the AI judge receives
You and the AI judge follow the same rules and scale. Here they are word for word. The judge answers in a fixed format, so some lines name its answer fields: your tone answer is its “valence”, “Not about this brand” is “refers_to_brand” false, question 2 is “mixed”, and any answer to question 3 other than “No judgment” is “evaluative”. Question 3's split between the AI's own voice and quoted sources is ours; the judge does not record it.
Rules:
1. Rate only statements about the target brand: its products, quality, performance, value, reputation, people and conduct, and comparisons that involve it. Ignore statements about other brands unless they compare the target brand with them.
2. Being named, listed or recommended by inclusion is not an evaluation in itself. List labels and phrases that only repeat the question (for example "Top picks:" or "Brands for beginners:") are not evaluations of the target brand. Rate the words that describe the target brand itself.
3. Plain facts are neutral: history, founding date, ownership, location, product range, ingredients, price level or market position stated without judgement.
4. Evaluations count: praise or criticism by the assistant, and judgements by others that the text reports (awards, ratings, critical acclaim, complaints, recalls, controversies, lawsuits).
5. "evaluative" is true if the text contains at least one evaluation of the target brand under rule 4, and false if it contains only facts or description.
6. If favourable and unfavourable evaluations are both present, set "mixed" to true and choose the valence that reflects their overall balance (0 if they are of similar weight).
7. If the text does not refer to the target brand (the name is used as an ordinary word or for a different company, or the assistant says it does not know the brand and describes nothing), set "refers_to_brand" to false, "evaluative" to false, "mixed" to false and "valence" to 0.
Valence scale:
2 = strongly favourable: emphatic praise or endorsement of the brand ("outstanding", "the best", "exceptional quality") with no substantive reservation.
1 = favourable: a positive evaluation ("well regarded", "reliable", "good value", "award-winning"), possibly with minor reservations.
0 = neutral: no evaluation of the brand (facts or description only), or favourable and unfavourable evaluations of similar weight.
-1 = unfavourable: a negative evaluation ("overpriced", "inconsistent quality", "mixed reviews", "less refined than"), possibly with some positives.
-2 = strongly unfavourable: emphatic criticism or warning ("avoid", "poor quality", a scandal or recall presented as defining) with no substantive positive.
All examples are invented, about a fictional brand (“Halvor”). None comes from the texts you will label.
```

