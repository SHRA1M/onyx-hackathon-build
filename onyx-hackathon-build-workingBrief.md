# Working brief: onyx-hackathon-build

Updated 2026-10-24 (thirty-first wrap, Opus).

## Objective

Finish Task 23 (gap hunt). Built on branch `task-23-wip` (pushed, not merged); draft report-back
`docs/report-back/2026-10-24-task-23-gap-hunt.md`. The report is 6 pages, 2,286 words, ladder exhausted: hq decides
the five-page cut (expected 2026-10-25). Task 24 (`D:\Projects\hq\uni\ai-for-good-hackathon\task-24-uae-texts-order-2026-10-24.md`,
Trade Law 14/2023 EN and AR, Cabinet 28/2023) waits until Task 23 is merged.

## Next moves

1. `git switch task-23-wip`; apply hq's cut; rebuild (`uv run python docs/build_report.py`), recount
   (`powershell -ExecutionPolicy Bypass -File scripts/report_pages.ps1`).
2. Finish the report-back (cut, page count, CI run), commit, push the branch, CI green; merge to main with Iyas's go.
3. Then Task 24.

## Open questions

- hq: the draft report-back's five points and gap-11 kind "method" (Iyas's choice; the order said "standards").
- hq: align `report-draft-2026-10-23.md` to `docs/report.md` (Tasks 19, 21, 22, 23 changes).
- hq: strips the two entry names from the filed Task 16 and Task 20 orders before 2026-11-09.
- USD 1.12 left of the USD 20 balance: any live run needs a top-up.
- hq: the team members' spellings for the README team line.
- Iyas: read the Arabic step text of S1 to S5 on a page. `/setup-matt-pocock-skills` not yet run.
