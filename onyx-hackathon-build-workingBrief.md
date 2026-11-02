# Working brief: onyx-hackathon-build

Updated 2026-11-02 (fifty-sixth wrap, Opus). Handover for the next session.

## Objective

Finish Task 39 (`docs/work-orders/2026-11-02-task-39-pre-freeze.md`, ruling
`D:\Projects\hq\uni\ai-for-good-hackathon\task-39-stops-ruling-2026-11-02.md`) on branch `task-36`, so PR #13
carries Tasks 36 to 39. Freeze 2026-11-06; E due 2026-11-04 end of day; submission 2026-11-09.

## State

- Built, pushed, CI green at `100ecd3` (head `31b0c42`): A, C, D, and B's eval row and C5 hand-over cells. 667
  tests. Word main 5 pages, annex from page 6, 10 pages; PDF 10 pages.
- Waiting on hq: question 5 in `docs/report-back/2026-11-02-task-39-pre-freeze.md` (the Annex A retrieval sentence,
  stop 3: the gate carries 63% en / 65% ar of the not-shown clauses, under 90%); question 1 in
  `docs/report-back/2026-11-02-task-39-e-local-model.md` (context 32,768 with flash attention and q8_0 cache, or
  drop E).
- Ollama 0.40.13 installed; `qwen2.5:14b-instruct` pull stopped half done (low memory); restart only on Iyas's go.

## Open questions

- hq: Task 39 question 5; E question 1. Also whether D's three sentences should sit after "puts the decision in
  code." (the old "That is the number..." now follows them).
- Iyas: open `docs/report.pdf` (10 pages, page 5 ends with Limits, page 6 starts "Annex"), then send the reviewer
  email (target 2026-11-03); go to re-pull the model.

## Next moves

1. `git status`, `git pull` on `task-36`.
2. Read hq's answers. Add the Annex A sentence with a test that its numbers equal the printed row; copy the annex to
   hq's `report-annex-2026-11-02.md` with the Edit tool; `build_report.py`, `report_pages.ps1`, `report_pdf.ps1`;
   full `uv run pytest`; push; CI.
3. E as ruled: pull, `curl http://localhost:11434/v1/models`, S2 English to `runs/demo-local/S2/en/`, `verify-log`,
   the eval-ignores test, `docs/site/localmodel.html`, README and annex lines; or record "tried, not shown".
