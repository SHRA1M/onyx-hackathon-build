# Task 22: a consequence in every gap row; the what-if words; the Readiness sentence (2026-10-24)

Repo: `D:\Projects\engineering\onyx-hackathon-build`. Builds on 6a0aaf7 (the wrap after Task 21, accepted at 30e02c4). No model calls, USD 0.
Words only: no code, no figure, no tagged value, no run changes.

Why (hq, Fable ruling `fable-first-ruling-2026-10-24.md`): ITU said in session 3 that gap analysis is the most valued
part and that "if you are just listing a table... the quality matters"; the Y.3172 and Readiness mapping is "paper
mapping". Our gap rows say what is missing and not what happens while it is missing. Each row gains that, paid for
by tightening the mapping table's Readiness column.

## Task

All edits are in `docs/report.md`. Old text is quoted exactly; if any old text is not found character for character,
stop and ask before changing anything.

### A. Gap table: replace rows 1 to 10

Row 1, old:
```
| 1 | Complaint hand-over: trigger and human sourced (CPR 2.1.7, 26.7.2, licence 9.1); stop, hand-over and time limit not written | standards | TDRA | IMDA 2.2.2, 2.4.2 |
```
new:
```
| 1 | Complaint hand-over: the bar and the human are sourced (CPR 2.1.7, 26.7.2, licence 9.1); the stop, the hand-over and its clock are not, so the subscriber stays with the machine and no record shows when it stopped | standards | TDRA | IMDA 2.2.2, 2.4.2 |
```

Row 2, old:
```
| 2 | Consent elicited by an AI: the CPR sales-medium classification (4.10, 4.17, 4.22) decides whether an OTP is needed; PDPL 6(1)(b) names written or electronic consent, not spoken | coordination | TDRA, UAE Data Office | EU AI Act Art 50(1); IMDA 2.2.2 |
```
new:
```
| 2 | Consent elicited by an AI: the CPR sales-medium classification (4.10, 4.17, 4.22) decides whether an OTP is needed and names no AI channel; PDPL 6(1)(b) names written or electronic consent, not spoken, so a charge on a spoken "yes" stands or falls on a choice nobody has made | coordination | TDRA, UAE Data Office | EU AI Act Art 50(1); IMDA 2.2.2 |
```

Row 3, old:
```
| 3 | "Adequate verification process" (CPR 24.10) undefined for a remote channel; Electronic Transactions Art 33 trust levels never mapped to it | standards | TDRA | eIDAS Art 8(1), 8(3)(c) |
```
new:
```
| 3 | "Adequate verification process" (CPR 24.10) undefined for a remote channel; Electronic Transactions Art 33 trust levels never mapped to it, so an operator cannot know what check a voice or chat must pass before it blocks a line or changes a record | standards | TDRA | eIDAS Art 8(1), 8(3)(c) |
```

Row 4, old:
```
| 4 | Automated disconnection: the PDPL 18(4) human review has no procedure, deadline or regulator | responsibilities | UAE Data Office | GDPR Art 22(3) |
```
new:
```
| 4 | Automated disconnection: the PDPL 18(4) human review has no procedure, deadline or regulator; a subscriber who contests it has nothing to wait for and nobody to turn to | responsibilities | UAE Data Office | GDPR Art 22(3) |
```

Row 5, old:
```
| 5 | Subscriber data to a hosted model provider: the duties exist (PDPL 7(5), 8(1), 13(2), 23(1)(a), licence 3.4.1), the machinery (Art 22 list, 23(2), 8(11)) was never issued | legislative | UAE Data Office | GDPR Art 28(3)(a), 45(1) |
```
new:
```
| 5 | Subscriber data to a hosted model provider: the duties exist (PDPL 7(5), 8(1), 13(2), 23(1)(a), licence 3.4.1), the machinery (Art 22 list, 23(2), 8(11)) was never issued, so an operator sending subscriber data to a model abroad guesses at a rule that does not yet exist | legislative | UAE Data Office | GDPR Art 28(3)(a), 45(1) |
```

Row 6, old:
```
| 6 | AI disclosure: no general duty to tell a consumer they are talking to an AI; Electronic Transactions 11(2) makes it a validity condition for sales only | legislative | Cabinet | EU AI Act Art 50(1), 50(5) |
```
new:
```
| 6 | AI disclosure: no general duty to tell a consumer they are talking to an AI; Electronic Transactions 11(2) makes it a validity condition for sales only, so outside a sale the machine need never say it is one | legislative | Cabinet | EU AI Act Art 50(1), 50(5) |
```

Row 7, old:
```
| 7 | No binding UAE text sets conduct standards for an AI agent dealing with a consumer | standards | TDRA | IMDA 2.1.2 |
```
new:
```
| 7 | No binding UAE text sets conduct standards for an AI agent dealing with a consumer: beyond the sales rules there is nothing an operator's AI can be measured or sanctioned against | standards | TDRA | IMDA 2.1.2 |
```

Row 8, old:
```
| 8 | Y.3172 has no node outcome for a hand-over to a human: every node outcome is the output moving on to a sink that acts | standards | ITU-T | the recommendation is the example |
```
new:
```
| 8 | Y.3172 has no node outcome for a hand-over to a human: every node outcome is the output moving on to a sink that acts, so a pipeline built to the standard has no place to stop and give a case to a person | standards | ITU-T | the recommendation is the example |
```

Row 9, old:
```
| 9 | A child on the line: the caregiver signs the terms (Child Digital Safety Law 26/2025, 11(1)(b)) and under-13 data needs verified caregiver consent (7(1)); the implementing texts (Arts 6, 11, 16) are unpublished; nothing says how an automated channel learns the person is a child | legislative | TDRA, Cabinet | US COPPA Rule, 16 CFR 312.5(a)(1), (b)(1) |
```
new:
```
| 9 | A child on the line: the caregiver signs the terms (Child Digital Safety Law 26/2025, 11(1)(b)) and under-13 data needs verified caregiver consent (7(1)); the implementing texts (Arts 6, 11, 16) are unpublished; nothing says how an automated channel learns the person is a child, so it serves a child as an adult | legislative | TDRA, Cabinet | US COPPA Rule, 16 CFR 312.5(a)(1), (b)(1) |
```

Row 10, old:
```
| 10 | Arabic on an automated channel: the language is set and its omission fined (CPR 3.2.2, Consumer Law 26, Cabinet 66/2023 Annex 2); no text requires the Arabic answer to be as good as the English one, and the QoS Policy has no indicator per language | standards | TDRA | Canada OLA ss. 22, 26, 27 |
```
new:
```
| 10 | Arabic on an automated channel: the language is set and its omission fined (CPR 3.2.2, Consumer Law 26, Cabinet 66/2023 Annex 2); no text requires the Arabic answer to be as good as the English one, and the QoS Policy has no indicator per language, so the Arabic speaker can get the worse answer and nothing measures it | standards | TDRA | Canada OLA ss. 22, 26, 27 |
```

### B. Mapping table: tighten the third column, nine rows

Only the third column changes. Old third-column text, then new, per row:

SRC: `11 AI for Inclusion, "support for regional languages": every clause given in Arabic where published; Arabic runs scored`
→ `11 AI for Inclusion, "support for regional languages": every clause in Arabic where published; Arabic runs scored`

C: `7 Strategy Alignment, "coordination between service providers": operator, regulator and Data Office are separate agents (S5)`
→ `7 Strategy Alignment, "coordination between service providers": operator, regulator and Data Office as separate agents (S5)`

PP: `10 AI & Policies, "policies for nodes in AI pipelines": the policy text is the retrieval unit`
→ unchanged.

M: `6 Human Interface, "AI models in the local language": drafts in both languages; the gate stands between draft and subscriber`
→ `6 Human Interface, "AI models in the local language": drafts in both; the gate between draft and subscriber`

P: `8 Collaboration with AI, "comparison with baseline", the baseline "only AI with no human-in-the-loop": the governed-against-ungoverned run`
→ `8 Collaboration with AI, baseline "only AI with no human-in-the-loop": the governed-against-ungoverned run`

D: `6 Human Interface: hand-over with both language quotes; no node outcome for it in Y.3172 (gap 8)`
→ `6 Human Interface: hand-over with both quotes; no Y.3172 node outcome for it (gap 8)`

SINK: `10 AI & Policies, "policy inputs from case briefs": the gap register is an output`
→ unchanged.

MLFO: `Standards factor: the pipeline's configuration is recorded and replayable`
→ `Standards factor: configuration recorded and replayable`

ML sandbox: `Sandbox factor: the same scenarios with and without the gates on the same model`
→ `Sandbox factor: same scenarios with and without gates, same model`

### C. The Readiness sentence

After the sentence ending `the other six are not claimed.` (the line under the mapping table), append, same paragraph:
```
 Readiness 2.0 counts agents as an interface metric (dimension 11) and as intent orchestration (7); it has no metric for where an acting agent's authority ends, which is what the P node measures here.
```

### D. The what-if words, two places

Introduction, old: `Every step
goes to a hash-chained log that a judge can replay offline without an API key.`
(one sentence; the line break may differ) → new:
```
Every step goes to a hash-chained log that a judge can replay offline without an API key, and replay again under a proposed rule: a what-if question for the policymaker.
```

S2, old: `Replayed under the rule the register recommends, the held step releases,` → new:
```
Replayed as a what-if question for the policymaker, under the rule the register recommends, the held step releases,
```

### E. Rebuild and count

Rebuild `report.docx` and the PDF the way Task 18 and 21 did. Count pages.

Five pages: finish (section "Done means").

Six pages: take these steps one at a time, recount after each, stop at the first that gives five, and name the
steps taken in the report-back:
1. Remove the section C sentence.
2. Restore row 6 to its old text.
3. Restore row 7 to its old text.
4. Restore row 8 to its old text.
5. Restore row 2 to its old text.
6. Restore row 9 to its old text.

Still six after step 6: stop. Report the count, the word count, and the first sentence on page 6. Change nothing else.
Rows 1, 3, 4, 5, 10 (the gaps the scenarios show) keep their new text in every case.

## Sources

Only `docs/report.md` and this order. No register, README, figure or data file is read for this task.

## Done means (hq checks; show each output in the report-back)

1. `git diff --stat 6a0aaf7` lists only `docs/report.md`, `docs/report.docx`, the PDF, `CHANGELOG.md` and the report-back.
2. `git diff 6a0aaf7 -- docs/report.md` shows: rows 1, 3, 4, 5, 10 with their new text; the mapping column edits of
   section B; section D's two sentences; and, unless cut by the ladder, section C and rows 2, 6, 7, 8, 9.
3. Every tagged paragraph (text inside `[` `]` tags: C3, C5 figures) is byte-identical: `git diff 6a0aaf7 -- docs/report.md | grep -E '^[-+].*\[C[35]'` prints nothing.
4. `git diff c5cea32 -- onyx/gate.py onyx/data/rules.json onyx/data/keys onyx/data/mandates.json onyx/eval.py runs/` prints nothing.
5. Page count is 5 (name the tool that counted it); word count stated.
6. Tests pass, CI green, committed and pushed; report-back at `docs/report-back/2026-10-24-task-22-gap-consequences.md`
   naming which ladder steps, if any, were taken.

## Limits

- Touch no file other than those in check 1. No change to `docs/gaps.md`, the register, README or any figure.
- No other entry's name in any tracked file.
- Stop and ask if any old text quoted above is not found exactly, if the docx build fails, or if the ladder runs out.
