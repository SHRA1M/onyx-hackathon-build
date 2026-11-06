# Working brief: onyx-hackathon-build

Updated 2026-11-06 (seventy-seventh wrap, Opus). Handover for the next session.

## Objective

Get hq's answers on Task 52, then build the next order: Task 53 (wording), then the video. Submission 2026-11-09.

## State

- **Task 52: merged.** Iyas merged PR #22 on 2026-11-06 at 04:26 Amman, `f6442d3`, inside the time box. Work continues from `main`. Report-back `docs/report-back/2026-11-06-task-52-built.md`. 914 tests. USD 7.13 spent, USD 28.98 of 45 in all.
- **Result:** governed 8 of 48 steps passed a barred act, ungoverned 48 of 48. All eight are one gate fault: `disclose_account` naming the partner in `target` or `recipient_type` with `args.recipient` empty. Not fixed, as ruled. The fault is now on the record in Annex C and the README on `main`.
- Report: main text 5 pages, annex from page 6, 14 pages in all.
- This repo does not know whether hq has read the report-back.

## Open questions

1. hq: the seven questions in the report-back. The first three matter most: Annex A's ruled sentence names change words, not the fault the runs found; the after-shortlist fix does not close that fault; C5 S3-2 has the same shape, held only because no trust level is set.
2. Arabic check, still owed on merged text: Claude Cowork read not run; Iyas's eye-check of steps 3, 4, 6 not done. Page: `docs/report-back/2026-11-06-task-52-arabic-check.html`.
3. Task 53 item 18's report clause must carry 8 of 48, not 0.
4. Earlier, still open: the note's "cites the chapeau"; two AI reads of the gap-15 Cabinet sentence; hq's three items in `docs/report-back/2026-11-05-task-51-built.md`; Iyas asks Ra'ed which translations he found wrong.

## Next moves

1. `git status`; `git switch main`; `git pull`.
2. If hq sends changes to Task 52: a new dated order, one task, on a new branch. The U8 key and `runs/u8/` are not edited.
3. Otherwise the next order from hq, in a fresh session.
