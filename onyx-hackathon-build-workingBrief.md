# Working brief: onyx-hackathon-build

Updated 2026-11-02 (fifty-fourth wrap, Opus). Handover for the next session.

## Objective

Task 38, the annex ITU's reviewer asked for (`D:\Projects\hq\uni\ai-for-good-hackathon\task-38-annex-order-2026-11-02.md`),
on branch `task-36` so PR #13 carries Tasks 36, 37 and 38. Freeze 2026-11-06; submission 2026-11-09.

## State

- Tasks 36 and 37 done: report 5 pages, 2,346 words; 644 tests; CI green on PR #13 (not merged, no tag).
- Task 38 stopped before any build: `docs/report-back/2026-11-02-task-38-stop-1.md`. Twelve brace values are in its
  table; braces A (pooled C3 gate rejection en/ar) and B (definition line) are not in the repo; sentences C ("zero"
  in governed runs) and D (eye-check of page images) are unbacked.
- hq's annex text `task-38-annex-text-2026-11-02.md` changed on disk after the stop: read it again first.

## Open questions (with hq)

- Stop 1 questions 1 to 6 (A to D, gate-function count 14 or 13, go ahead with the text-independent parts).
- Carried: Arabic PDPL chunk text for `why --lang ar`; in-force dates (Maine, India TCCRR, Korea Art 31); Saudi
  Arabic eye-check; GitHub Pages on submission day.

## Next moves

1. `git status`, `git pull` on `task-36`.
2. Read hq's answer to stop 1 and the current annex text; diff the text against the stop file's assumptions.
3. Build items 1 to 7 of the order; `report_pages.ps1` must say 5 for the main text, annex on page 6; PDF export.
4. Report-back `docs/report-back/2026-11-02-task-38-annex.md` with the brace table and outputs.
