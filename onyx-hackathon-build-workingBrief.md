# Working brief: onyx-hackathon-build

Updated 2026-11-02 (sixtieth wrap, Opus). Handover for the next session.

## Objective

Finish Task 43 (`D:\Projects\hq\uni\ai-for-good-hackathon\task-43-free-zones-itu-order-2026-11-02.md`) on
`task-36`. It is built and UNCOMMITTED in the working tree, held at stop 3. Deadline: pushed with CI green by
2026-11-05; freeze 2026-11-06; submission 2026-11-09.

## State

- Task 42 committed and pushed (`a7b923b`), CI green.
- Task 43: answers to stops 1 and 2 applied (hq files `task-43-stop-1-answers-2026-11-02.md`,
  `task-43-stop-2-answers-2026-11-02.md`). Stop 3: row 5's new words make the main text 6 pages
  (`docs/report-back/2026-11-02-task-43-stop-3.md`). The report and PDF on disk are that 6-page build.

## Open questions

- hq: Task 43 stop 3, row 5 (recommended a: keep "has not been issued"; drop it from the test pattern in
  `tests/test_gaps.py` `test_no_live_output_says_never_issued`).
- Iyas: send the reviewer email (target 2026-11-03).

## Next moves

1. `git status` (expect Task 43's files modified), `git pull` on `task-36`.
2. Apply the stop 3 answer, `uv run python docs/build_report.py`, `scripts/report_pages.ps1` (main 5, annex page 6),
   `scripts/report_pdf.ps1`, `scripts/check_pdf.py docs/report.pdf`.
3. Run the 8 done checks with output; hq copies with backups; CHANGELOG; commit by name; push; `gh pr checks 13`;
   done report `docs/report-back/2026-11-0X-task-43-free-zones-itu.md`.
