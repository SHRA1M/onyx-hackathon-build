# Working brief: onyx-hackathon-build

Updated 2026-11-04 (sixty-seventh wrap, Opus). Handover for the next session.

## Objective

Finish Task 48 before the freeze on 2026-11-06; submission 2026-11-09.

## State

- Branch `task-48`, draft PR #17, head `029d0a1`, not merged. CI passed on `10165d4` (run 41911323863); `029d0a1` adds only the stop file, its CI not looked at.
- Built: the stop 1 ruling, the quote addendum, and items 1 and 3 of addendum 2.
- Held: addendum 2 item 2, the replay line at `onyx/replay_viewer.py` line 286. The line on the branch is the older one, which hq found false for the "Elsewhere" quotes; it must change before the merge.
- Tests 755 here; CI 731 passed, 24 skipped. Report: body 5 pages, annex from page 6, 12 in all.

## Open questions

1. For hq: which replay line goes in? Every step also shows "Without the gates" proposals that no gate checked (65, 60 with a quote). A candidate is in `docs/report-back/2026-11-04-task-48-addendum-2-stop.md`.
2. For Iyas: he has not yet said the texts read right, or given his word on the merge. Addendum 2 changed gap 2's text after he last saw it.

## Next moves

1. `git status`; `git switch task-48`; `git pull`. Read hq's answer. No answer yet: ask Iyas for it, giving the stop file's path.
2. Build the line, its pin at `tests/test_report.py` line 517, then `python -m onyx replay-page --html` and `python -m onyx site`. Only the line should differ in `docs/replay/*.html` and `docs/site/runs.html`.
3. Run addendum 2's done means; write the result in the report-back; paste CI's run id on the new head.
4. Print the new gap-2 `"gap"` and the replay line for Iyas. Merge only on his word.
5. After the merge: CI "reproduce" on main with its run id, and open the README diagram on GitHub. Both not yet run.
