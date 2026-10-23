# Working brief: onyx-hackathon-build

Updated 2026-10-23 (twenty-fourth wrap, Opus).

## Objective

Finish Task 12 part A (`docs/work-orders/2026-10-23-task-12-report-build.md`). Built and committed; stopped at item 4
because `docs/report.docx` is 9 pages against a limit of 5. hq trims `docs/report.md` (scenarios first).

## Next moves

1. Apply hq's trim lines to `docs/report.md`; rebuild with `uv run python docs/build_report.py`.
2. Count pages: `powershell -ExecutionPolicy Bypass -File scripts/report_pages.ps1`. Five or fewer: put the count in
   `docs/report-back/2026-10-23-task-12-report-build.md`, commit, push, check CI.
3. Then Part B (video script, judge card) when hq orders it.

## Open questions

- hq: the trim; whether the docx creator should stop reading the template author.
- hq: strips the two entry names from the filed Task 16 order before 2026-11-09.
- USD 1.12 left of the USD 20 balance: any live run needs a top-up.
- hq: the team members' spellings for the README team line.
- Iyas: read the Arabic step text of S1 to S5 on a page. `/setup-matt-pocock-skills` not yet run.
