# Task 48: built except gap 2, and the audit of Tasks 46 and 47 (2026-11-04)

Order `docs/work-orders/2026-11-04-task-48-small-miss.md`. USD 0, no model call. Branch `task-48`, draft PR, not merged.

Plainly: six of the seven fixes are in and the report still fits, 5 pages then 12 in all. Gap 2's new sentence is not in,
because the CPR contradicts "fits none of them" and the text overflows page 5. Page 1's GitHub line still wraps. Tasks 46
and 47 hold up against their orders: every check that could run passed, and the diagram rendered on GitHub on both loads.

Questions are in `docs/report-back/2026-11-04-task-48-stop-1.md`.

## Task 48, done means

| # | Check | Result |
|---|---|---|
| 1 | Full suite; pins named | PASS: 749 passed in 219.65s (with item 2 not in). Pins below |
| 2 | `kb verify`, `check-data`, `selftest` | PASS: VERIFIED 100, REFERENCED 5, UNVERIFIED 3 (108); "every fetched source matches its sha256"; "check-data ok"; "figures match a fresh eval of runs/"; 161 chunks |
| 3 | Pages; page 5 end; page 1 line | PARTIAL. PASS: `pages: 5`, `annex starts on page: 6`, `total pages: 12`, PDF 12; page 5 ends in the "Limits and next steps" paragraph. **FAIL: the GitHub line takes two lines; the URL breaks after `onyx-hackathon-` (stop 1, question 2).** Measured without item 2 |
| 4 | Count check | PASS, table below. Annex numbers beyond those listed rest on the build's value check, not on a separate check by me |
| 5 | `git diff --stat` | Listed files plus three departures, below. Nothing under `kb/manifest.csv`, `onyx/data/keys/`, `runs/`, `onyx/prompts/`. `README.md` unchanged, because it carries gap 2's text and item 2 is held |
| 6 | Gap 2 printed; Iyas reads; CI on main after merge | NOT RUN: item 2 held, not merged. The ordered text is in the order; the candidate is in the stop file |
| 7 | hq's copies | None made |
| 8 | `tests/test_task_45.py` line 23 | Read. `GAP_7_POSITION` pinned item 3's sentence; pin updated |

### Items

| Item | State |
|---|---|
| 1 Annex D count | Built |
| 2 Gap 2 | **Held: stop 1, question 1** |
| 3 Gap 7 | Built |
| 4 DHA line | Built, both occurrences |
| 5 One Authority name | Built |
| 6 GitHub line | Built as ordered; still wraps (question 2) |
| 7 Replay line | Built as ordered; the sentence overstates (question 3). `docs/replay/index.html` diff: that one added line |
| 8 Regenerate and rebuild | Done without item 2; must be rerun once item 2 lands |

### Pins changed

- `tests/test_gaps.py`: `DATA_OFFICE`, used by `test_gap_2_adds_singapore_s_15_recommendation_unchanged` and `test_task_33_data_office_sentence_once_in_the_register`; `test_task_43_rows_say_federal_where_they_mean_federal`.
- `tests/test_task_45.py`: `GAP_7_POSITION`, used by `test_the_gap_6_and_gap_7_positions_are_the_rulings_words`.
- `tests/test_report.py`: `LINKS`, used by `test_task_34_team_and_the_four_labelled_links`; `test_eight_list_paragraph_headings_in_template_order`.

### Count check

| Report states | Value found | Proved by |
|---|---|---|
| 108 documents | 108 | `kb/manifest.csv` row count |
| 100 verified; REFERENCED 5; UNVERIFIED 3 ("two unpublished, one unreachable": the 3 counted, the split not recounted) | 100 / 5 / 3 | `kb/manifest.csv` status column, `kb verify` |
| thirty-two other UAE texts; thirty-eight foreign | build passes | `docs/build_report.py` `check_kb_counts` against `kb/manifest.csv` |
| 371,476 complaints | present | `docs/sources/eand-sustainability-report-appendices-2025.txt` |
| 2.3 / 2.1 proposals; 0.99 / 1.00; 0.96 / 1.00 | present | `eval/results.md`, build value check |
| 110 of 112; 5 of 7 found | present | `eval/results.md` |
| gate median 0.46 ms; 222 decisions | 0.458 ms; 222 | `eval/results.md` line 26 |
| model median 7.8 s; 156 calls | 7837.607 ms; 156 | `eval/results.md` line 26 |
| USD 5.3767 over 20 runs; USD 0.27 a run | 5.3767; 5.3767 / 20 = 0.269 | `eval/results.md`; 20 from `runs/c5` (10 en, 10 ar) |
| Annex D: 161 chunks, 77 with `text_ar`, 10 Arabic runs, 23 columns, 21 documents chunked | same | `kb/chunks/*.jsonl`, `runs/c5/S*/ar/`, `kb/manifest.csv` header |

### Departures from check 5's list

`tests/test_report.py` (item 6 cannot pass without it), `tests/test_task_45.py` (check 8 asks for it), `CHANGELOG.md` (standing
rule). Also `docs/site/runs.html` gains the replay line, as the replay text the stop clause allows.

## Audit of Tasks 46 and 47 against commit 43d1e67

Read-only, in a temporary worktree at 43d1e67, removed afterwards (`git worktree list` shows only the repo). Nothing fixed.
The worktree's own install failed on a download timeout ("Failed to download distribution due to network timeout"), so its
first suite run did not start. Tests ran on this repo's `.venv` with `PYTHONPATH` set to the worktree, and printed "onyx from
...wt-43d1e67\onyx\__init__.py". Gitignored `kb/sources`, `data/chromadb` and `kb/index-bilingual` were copied in for run 1.

### Every check and its result

Task 46, order's done means (with ruling `task-46-stop-1-ruling-2026-11-04.md`):

1. Done 1, README renders on GitHub in Chrome: **PASS.** No "Unable to render rich display". Two loads, both rendered in the screenshot: `blob/43d1e67/README.md` and the repo home page, whose latest commit is 43d1e67. Evidence: frame present, 1936 px and 1603 px high. The message would sit inside GitHub's cross-origin frame, so the page's text search cannot rule it out; the screenshots are the evidence. Saved: `C:\Users\SUPER\AppData\Local\Temp\claude-chrome-screenshots-CCPkT5\screenshot-1793820530259-0.jpg`. The Task 46 report-back saw the message once on a first load; two loads here do not prove it never returns.
2. Done 1, screenshot attached: **PASS.** `docs/report-back/screenshots/2026-11-04-task-46-diagram.jpg` opened: whole figure and caption, on branch `task-46`.
3. Done 2, `tests/test_readme_diagram.py`: **PASS.** 17 passed in 1.60s.
4. Done 3, `uv run pytest`: **PASS.** Item 15 below.
5. Done 3, CI "reproduce" on the PR: **PASS.** Run 41878859632, success, `117e084`, pull_request.
6. Done 4, reviewer row: **PASS.** Diff shows "the Y.3172 mapping table below" becoming "the Y.3172 diagram and mapping table below". Removed README lines: only this row and the ML sandbox row, as the ruling allows.
7. Done 5, report-back with test output and screenshot path: **PASS.** Opened; both present.
8. Done 5, report untouched, page counts: **PASS.** `git diff --stat 49bb40a 43d1e67` on report, annex, runs, keys, eval, kb, gate is empty. Word on the 43d1e67 docx: `pages: 5`, `annex starts on page: 6`, `total pages: 12`; PDF 12.
9. Order and ruling text: **PASS.** Mermaid at line 151 under the heading at 149; 14 boxes; nine subgraphs, the nine names; caption matches the ruling word for word (line 211); ML sandbox row's cells match; PR #15 merged first (`49bb40a`). PR #16 merged, `43d1e67`. "No competitor named": word search only, no hit for "competitor" or "rival" in the README, annex or `eval/results.md`; **competitor names NOT RUN**, because the list is outside this check's sources.

Task 47, order's done means (with ruling `task-47-stop-1-ruling-2026-11-04.md`):

10. Done 1, `eval` prints both tables: **PASS.** Exit 0; "Retrieval alone, shipped: all-MiniLM-L6-v2" and "Retrieval alone, bilingual: intfloat/multilingual-e5-small"; tracked diff after eval, 0 lines.
11. Done 2, `uv run pytest`: **PASS.** Item 15 below.
12. Done 2, CI on the PR without the bilingual index: **PASS.** Run 41873930881, success, `2736654`, pull_request. Main at 43d1e67: run 41889674427, success, log "725 passed, 24 skipped", "bilingual index not built", "228 logs: chain ok".
13. Done 3, PDF rebuilt, page counts unchanged: **PASS.** Same counts as item 8; `docs/report.pdf` in the Task 47 diff; "Limits and next steps" on page 5, Annex on page 6.
14. Done 4 and 5: **PASS.** Done 4 is the comparison in item 17. Report-back opened: model, revision `614241f622f53c4eeff9890bdc4f31cfecc418b3`, 775.8 s, both tables, chunk count 161 beside 117. Rulings: "obvious upgrade" and "its Arabic retrieval is weak" 0 hits in the annex; both ruled sentences in; README clause with no number at line 13; two method lines at `eval/results.md` 413 and 414; no file in the Task 47 diff under model, agents, gate, rules, mandates, runs, keys, HASHES or prompts (0 of each); four named unit tests in `tests/test_eval.py`.

Your other checks:

15. Full suite at 43d1e67: **PASS, 749 matches the report-back.** With local sources and indexes: 749 passed in 226.44s. Under CI conditions (those three folders moved away): 727 passed, 22 skipped. CI itself: 725 passed, 24 skipped; the gap of 2 is not diagnosed.
16. Selftest at 43d1e67: **PASS.** "figures match a fresh eval of runs/"; chains ok, key hashes match. `kb verify` 100 / 5 / 3, `check-data` ok.
17. Retrieval figures, `eval/results.md` against Annex A of `docs/report.pdf`: **PASS, all equal.** PDF page 7: "finds 0.24 of the key clauses in English and 0.09 in Arabic at top 8; a bilingual embedder (multilingual-e5-small, in no scored run) finds 0.24 and 0.15". `eval/results.md`: shipped en 29 of 123 (0.24), ar 11 of 123 (0.09), lines 210 and 211; bilingual en 30 of 123 (0.24), ar 18 of 123 (0.15), lines 232 and 233. "Overlapping": 0.05 to 0.15 and 0.09 to 0.22.
18. README on GitHub in a browser: **Renders.** Same evidence as item 1.

Not run or not covered: competitor names (item 9). The Task 46 and 47 orders' `kb/index-bilingual` build was not rerun, the copied index was used. Every edge of the diagram was not hand-checked against the code; the 17 tests are the evidence.

## Limits

No prompt, gate, mandate, retrieval or model change; no KB row; manifest, keys and runs untouched; no eval rerun owed. Fails closed: nothing merged, nothing sent outward.

## CI on the draft PR

PR #17, https://github.com/SHRA1M/onyx-hackathon-build/pull/17, draft, not merged. CI "reproduce" on `023e27a`: success on the pull request (run 41900332291); log "725 passed, 24 skipped". This entry adds only these lines. CI on main after a merge: not run.
