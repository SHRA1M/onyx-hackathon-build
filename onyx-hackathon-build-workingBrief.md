# Working brief: onyx-hackathon-build

Updated 2026-11-04 (sixty-sixth wrap, Opus). Handover for the next session.

## Objective

Finish Task 48 before the freeze on 2026-11-06; submission 2026-11-09.

## State

- Tasks 46 and 47 merged; main at `43d1e67`, CI passed. Audited against their orders: every check that could run passed (`docs/report-back/2026-11-04-task-48-small-miss.md`).
- Task 48 on `task-48`, draft PR #17, CI passed on `023e27a`. Items 1, 3 to 7 and the rebuild are in; gap 2 is not.
- Tests 749. Report: body 5 pages, annex from page 6, 12 in all.

## Open questions

All three are in `docs/report-back/2026-11-04-task-48-stop-1.md`, for hq:

1. Gap 2's wording: the CPR contradicts "fits none of them", and the ordered cell overflows page 5 even shortened. A candidate that fits is in the file.
2. Page 1's GitHub line still wraps; a shorter label, or accept it?
3. The replay line claims more than CI checks; reword, and does `docs/report.md` line 24 need the same?

Also: three Task 46 decisions are for hq to see; hq's annex copy lacks the three Task 47 edits.

## Next moves

1. `git status`; `git switch task-48`; `git pull`. Read hq's answer to stop 1. No answer yet: ask Iyas for it.
2. Build the answer. Gap 2 also changes the README and `tests/test_gaps.py` line 416.
3. Rerun item 8: `python -m onyx gaps`, `replay-page --html`, `site`, `docs/build_report.py`, `scripts/report_pdf.ps1`. Check 5 main pages, 12 total.
4. Print gap 2's row for Iyas to read. Merge only after that, then paste CI's run id on main (check 6).
