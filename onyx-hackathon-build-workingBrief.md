# Working brief: onyx-hackathon-build

Updated 2026-11-05 (seventy-third wrap, Opus). Handover for the next session. Iyas said he will name the next session's work: wait for that word, and do not start the list below on your own.

## Objective

Task 51 checked by hq and merged, then its four held items built once Iyas answers. Freeze 2026-11-06. Submission 2026-11-09.

## State

- **Task 50: merged**, PR #19. Target not met, so no Task 52.
- **Task 51: built up to the five blocks.** Draft PR #20, branch `task-51`. Report-back `docs/report-back/2026-11-05-task-51-built.md`, handed to Iyas for hq. CI passed on build commit `d97c4ab`, run 42096308359; later commits (the report-back, this wrap) run their own, not read.
- Main text 5 pages, page 5 ends with the Limits sentence, annex from page 6, 13 pages in all (main has 12). 827 tests passed.

## Not built in Task 51

Waiting on Iyas, blocks 34, 65, 66, 89, 90: `C:\Users\SUPER\AppData\Local\Temp\claude\b0cdcceaf887c3b6\cd150a46-f312-4682-a59e-35bbc4beae20\scratchpad\eye5\five-arabic-checks.html`. A temp folder: if it is gone, rebuild the page from `D:\Projects\hq\uni\ai-for-good-hackathon\arabic-eye-check-2026-11-05.html` and the fit-check ruling.

1. 51.H.1: the 26.7.2 four-clause note, with the chapeau in both languages, in gap 1, Annex B under the rule sample, and Annex C. No rule row; 109 stays.
2. 51.K.1: gap-1 9.1 entry `quote_ar` and `file_ar` from a new checked file under `docs/sources/`.
3. 51.K.3: the tension row, Arabic first, «دون إبطاء». The recommendation's inferred line is already in.
4. Gap 15: the Arabic Cabinet sentence replaces the Board sentence in `gaps.json`. The sentence is in `docs/report-back/2026-11-05-task-51-stop-1.md`.

These grow the annex, not the main text. After them: `gaps`, `site`, `docs/build_report.py`, `scripts/report_pages.ps1`, `scripts/report_pdf.ps1`, `scripts/check_pdf.py`, the Arabic rendering check. Re-take a screenshot only if a page it shows changed.

## Open questions

1. Iyas: the five blocks. A wrong quote in a frozen key is a stop.
2. hq: the three items under "Three things for hq to read" in the report-back (instrument numbers in Annex A; "10 runs per language"; gap recall 0.87 beside 5 of 7).
3. Iyas asks Ra'ed which translations he found wrong. Still open.

## Next moves

1. `git status`; `git switch task-51`; `git pull`.
2. Take Iyas's word for the session's one task.
3. Run the page script after every report change: measure, never estimate. In Git Bash, write scripts holding `\n` with the Write tool, not a heredoc.
