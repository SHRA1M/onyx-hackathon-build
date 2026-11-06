# Working brief: onyx-hackathon-build

Updated 2026-11-06 (seventy-sixth wrap, Opus). Handover for the next session.

## Objective

Get Task 52 read by hq and merged by 2026-11-06 16:00 Amman, else it is dropped. Task 53 (wording) and the video follow. Submission 2026-11-09.

## State

- **Task 52: built, not merged.** Branch `task-52`, PR #22, report-back `docs/report-back/2026-11-06-task-52-built.md`. CI passed on `28e41a7`; the later commits add only the report-back and this wrap. 914 tests. USD 7.13 spent, USD 28.98 of 45 in all.
- **Result:** governed 8 of 48 steps passed a barred act, ungoverned 48 of 48. All eight are one gate fault: `disclose_account` naming the partner in `target` or `recipient_type` with `args.recipient` empty. Not fixed, as ruled.
- Report: main text 5 pages, annex from page 6, 14 pages in all on this branch.

## Open questions

1. hq: the seven questions in the report-back. The first three matter most: Annex A's ruled sentence names change words, not the fault the runs found; the after-shortlist fix does not close that fault; C5 S3-2 has the same shape, held only because no trust level is set.
2. Arabic check: Claude Cowork read not run; Iyas's eye-check of steps 3, 4, 6 not done. Page: `docs/report-back/2026-11-06-task-52-arabic-check.html`.
3. Task 53 item 18's report clause must carry 8 of 48, not 0.
4. Earlier, still open: the note's "cites the chapeau"; two AI reads of the gap-15 Cabinet sentence; hq's three items in `docs/report-back/2026-11-05-task-51-built.md`; Iyas asks Ra'ed which translations he found wrong.

## Next moves

1. `git status`; `git switch task-52`; `git pull`.
2. If hq sends changes to Task 52: a new dated order, one task. The U8 key and `runs/u8/` are not edited.
3. If hq clears it: Iyas gives the word, then `gh pr merge 22 --merge`. Merge only on his word.
4. Then the next order from hq, in a fresh session.
