# Working brief: onyx-hackathon-build

Updated 2026-11-05 (seventy-fourth wrap, Opus). Handover for the next session. Iyas names the next session's work: wait for that word, and do not start the list below on your own.

## Objective

Task 51b checked by hq and merged. Freeze 2026-11-06. Submission 2026-11-09.

## State

- **Task 51: merged**, PR #20.
- **Task 51b: built.** Draft PR #21, branch `task-51b`. Report-back `docs/report-back/2026-11-05-task-51b-built.md`, path handed to Iyas for hq. CI passed on build commit `46ca90c`, run 42104679280; later commits (the report-back, this wrap) run their own, not read.
- Main text 5 pages, page 5 ends with the Limits sentence, annex from page 6, 13 pages in all. 846 tests passed.

## Open questions

1. hq: the note's "cites the chapeau". The gate's clause list has no chapeau and the order bars a rule row. Built word for word, flagged.
2. hq: `docs/build_report.py` changed for right-to-left paragraphs, not named in the order; gap 15's `file_ar` now cites the Arabic law PDF.
3. Owed before shipping: two AI reads (Fable, Claude Cowork) of the gap-15 Cabinet sentence against its English.
4. Not fixed, outside the order: `scripts/report_pdf.ps1` can pass on an old PDF after a failed export.
5. Earlier, still open: hq's three items in `docs/report-back/2026-11-05-task-51-built.md`; Iyas asks Ra'ed which translations he found wrong.

## Next moves

1. `git status`; `git switch task-51b`; `git pull`.
2. Take Iyas's word for the session's one task.
3. Run the page script after every report change, and look at a page image of any new Arabic. Close `docs/report.pdf` in Foxit first.
