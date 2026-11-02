# Working brief: onyx-hackathon-build

Updated 2026-11-02 (fifty-fifth wrap, Opus). Handover for the next session.

## Objective

Finish Task 38, the annex (`D:\Projects\hq\uni\ai-for-good-hackathon\task-38-annex-order-2026-11-02.md`, ruling
`task-38-stop-1-ruling-2026-11-02.md`, text v3), on branch `task-36` so PR #13 carries Tasks 36, 37 and 38. Freeze
2026-11-06; submission 2026-11-09.

## State

- Built and committed (`02d4328`, not pushed): `docs/annex.md`, builder annex, `report_pages.ps1` annex line,
  `docs/report.pdf` (`report_pdf.ps1`, `check_pdf.py`), README line, hq copy, `tests/test_annex.py`. 661 tests.
  Word: main 5 pages, 2,366 words; annex from page 6; 10 pages. PDF 10 pages.
- Stopped at stop 2: `docs/report-back/2026-11-02-task-38-annex.md`, section "Stop 2". v3 says "17 verbs"; the code
  has 16.

## Open questions

- hq: "17 verbs" to "16"? (stop 2)
- Iyas: go to push `task-36` (CI on PR #13); his own look at `docs/report.pdf` (Done means 7).
- Carried: Arabic PDPL chunk text for `why --lang ar`; in-force dates (Maine, India TCCRR, Korea Art 31); Saudi
  Arabic eye-check; GitHub Pages on submission day.

## Next moves

1. `git status`, `git pull` on `task-36`.
2. Read hq's answer; edit the one word in `docs/annex.md`; copy it to hq's `report-annex-2026-11-02.md`.
3. `uv run python docs/build_report.py`; `report_pages.ps1`; `report_pdf.ps1`; `uv run pytest`.
4. Update the report-back (stop 2 answered, outputs); commit; with Iyas's go, push and record CI on PR #13.
