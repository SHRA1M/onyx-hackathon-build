# Working brief: onyx-hackathon-build

Updated 2026-11-05 (seventy-second wrap, Opus). Handover for the next session. This file and the background are current on `task-50`; `task-51` branched from main and holds older copies until Task 50 merges.

## Objective

Finish Task 51 from hq's `D:\Projects\hq\uni\ai-for-good-hackathon\task-50-51-order-2026-11-05.md` and `fit-check-ruling-2026-11-05-fable.md` (filed on `task-51` under `docs/work-orders/`). Freeze 2026-11-06. Submission 2026-11-09.

## State

- **Task 50: done.** Draft PR #19, branch `task-50`. Report-back `docs/report-back/2026-11-05-task-50-built.md`. hq checks and merges. CI push run 42089516363 passed on `162c3bc`. Target not met, so no Task 52.
- **Task 51: built up to stop 1.** Branch `task-51` at `38a6887`. Stop file `docs/report-back/2026-11-05-task-51-stop-1.md`: main text 4 lines over 5 pages (last line page 6, y 120). 786 tests passed before the last commits; `check-data ok`; `selftest` "figures match a fresh eval of runs/". CI on the branch was still running at this wrap: runs 42093260172 and 42093604411; read them.
- Figure 2's restyle is reverted by its fallback. The 8 pt version is saved: `docs/report-back/2026-11-05-task-51-fig2-restyle.patch` on `task-51`. S3's "controversy case" words in report line 90 are out by 51.C's fallback; Annex C has them.

## Not built in Task 51

1. Waiting on Iyas, five blocks: `C:\Users\SUPER\AppData\Local\Temp\claude\b0cdcceaf887c3b6\cd150a46-f312-4682-a59e-35bbc4beae20\scratchpad\eye5\five-arabic-checks.html`. Blocks 34, 65, 66 (the new Cabinet sentence), 89, 90. No answer yet. Those answers release:
   - 51.H.1: the 26.7.2 four-clause note, with the chapeau in both languages, in gap 1, Annex B under the rule sample, and Annex C. No rule row; 109 stays.
   - 51.K.1: gap-1 9.1 entry `quote_ar` and `file_ar` from a new checked file under `docs/sources/`.
   - 51.K.3: the tension row, Arabic first, «دون إبطاء». The recommendation's inferred line is already in.
   - Gap 15: the Arabic Cabinet sentence replaces the Board sentence in `gaps.json`. The sentence is in the stop file.
2. Waiting on hq, six questions in the stop file: which cut (recommended: the sources sentence, which fits at page 5, y 695.25, and needs Y.3173 named in Annex A and pins moved); strip assertion per figure; two "Text page" `.md` links; footer trim needs a chunk edit, so after the shortlist; pins moved; `docs/build_report.py` allowed.
3. After both: `scripts/report_pages.ps1`, `scripts/report_pdf.ps1`, `scripts/check_pdf.py`, the Arabic rendering check on the new PDF (method in the background, Open), re-take screenshots only if a shown page changed, report-back `docs/report-back/2026-11-05-task-51-built.md`, draft PR, CI.

## Open questions

1. Iyas: the five blocks. A wrong quote in a frozen key is a stop.
2. hq: the six in the stop file, and Task 50's check and merge.
3. Iyas asks Ra'ed which translations he found wrong. Still open.

## Next moves

1. `git status`; `git switch task-51`; `git pull`. If PR #19 is merged, rebase `task-51` on main before CI, and bring the folder files across.
2. Read hq's answer and Iyas's five answers. Apply the cut, then the released items.
3. Run the page script after every report change. The body is sensitive: a table row moving costs 72 pt at once, so measure, never estimate.
4. Finish the list under "Not built", item 3.
