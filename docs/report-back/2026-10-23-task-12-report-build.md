# Report-back: Task 12 part A, stopped at item 4 (2026-10-23)

1. Stop (item 4): Word counts 9 pages, 3,241 words; first sentence on page 6: "S1, roaming before a flight." Nothing trimmed. Rendering checked on a PDF export: the length is the text (about 6.5 pages before the two tables and two figures).
2. Items 1 to 3 built: `docs/report.md`, `docs/report-template.docx`, `docs/build_report.py`, `docs/report.docx`; both tagged paragraphs pass the value check; two builds byte-identical; CI builds it before the figure redraw.
3. First stop ruled by hq (filed in the order): plain decimals from the named run set; single-digit list markers skipped. Ids (S1, S3-4, C5, v3) skipped as names. The Results paragraph's two tags are checked as one set (looser there).
4. Item 5: S3, S4, S5 pages read `runs/c5/S<n>/run1.jsonl`. S1 stays on C3: no run, C3 or C5, cites CPR 17.4 or 17.4.1; the README paragraph says so. Iyas ruled the viewer follows the pages (English S3 to S5 now C5).
5. Item 6: the coordinator writes `candidate-4-4-fixed-term-bundle` (`local_id` `candidate-S1-6`). The scorer's gap recall reads the log's flag_gap and abstention gaps, not the candidate row, so a new run with this fix would not change S1's gap recall.
6. Rendering choices: backticks dropped; captions plain 10 pt; header labels bold from the draft (the template's are not); docx creator still the template author.
7. Tests: 354 pass, selftest prints "figures match a fresh eval of runs/".
8. Open for hq: the trim; the creator field.
