# Report-back: Task 12 part A, built and pushed (2026-10-23)

1. Item 4: Word counts 9 pages, 3,241 words; first sentence on page 6: "S1, roaming before a flight." Nothing trimmed: the five-page cut is hq's, by a new order replacing `docs/report.md` (Iyas's ruling 4).
2. Items 1 to 3 built: `docs/report.md`, `docs/report-template.docx`, `docs/build_report.py`, `docs/report.docx`; both tagged paragraphs pass the value check; two builds byte-identical on Windows and Linux; CI builds it.
3. First stop ruled by hq (filed in the order): plain decimals from the named run set; single-digit list markers skipped. Ids (S1, S3-4, C5, v3) skipped as names.
4. Results paragraph (ruling 3): split, not left as is. A paragraph with two tags is checked sentence by sentence: the C5 sentences against the C5 column and Misses line, the last sentence (0.46 ms, 7.8 s, 222 decisions, 156 calls) against the C3 latency lines. Tested both ways (a C3-only 0.86 in the C5 part fails; a C5-only 0.96 in the C3 part fails).
5. Item 5: S3, S4, S5 pages read `runs/c5/S<n>/run1.jsonl`. S1 stays on C3: no run, C3 or C5, cites CPR 17.4 or 17.4.1; the README paragraph says so.
6. Item 6, scorer note: the coordinator writes `candidate-4-4-fixed-term-bundle` (`local_id` `candidate-S1-6`). The scorer's gap recall reads the log's flag_gap and abstention gaps, not the candidate row, so it does not match the S1 candidate row by id, and a new run with this fix would not change S1's gap recall.
7. Rulings 1 and 2: docx creator and last editor "Team Onyx", the template author gone from every part; captions plain 10 pt, backticks dropped, bold header labels kept.
8. Tests: 359 pass; selftest prints "figures match a fresh eval of runs/".
9. Open for hq: the order that replaces `docs/report.md` to reach five pages.
