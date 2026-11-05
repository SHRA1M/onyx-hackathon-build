# Working brief: onyx-hackathon-build

Updated 2026-11-06 (seventy-fifth wrap, Opus). Handover for the next session.

## Objective

Task 52: an adversarial subscriber, measured. Order `docs/work-orders/2026-11-05-task-52-adversarial-subscriber.md`. Time box 2026-11-06 16:00 Amman, else dropped. Task 53 and the video follow. Submission 2026-11-09.

## State

- **Task 52: stopped, nothing built.** Branch `task-52`, one commit on main 45c7316 (the filed order and the stop report). `docs/report-back/2026-11-06-task-52-stop-1.md`, path given to Iyas for hq. USD 0 spent, no model call.
- Tasks 51 and 51b merged, PR #20 and #21. 846 tests at the last full run (Task 51b); not rerun this session.

## Open questions

1. hq: may Task 52 spend up to USD 8.50? Estimate USD 7.42 against the order's USD 5.
2. hq: what counts as a barred act? Recommended: by effect, from a fixed list committed with the key.
3. hq: does the annex sentence add "args and quote"? Otherwise it goes in word for word.
4. Earlier, still open: the note's "cites the chapeau"; two AI reads of the gap-15 Cabinet sentence; hq's three items in `docs/report-back/2026-11-05-task-51-built.md`; Iyas asks Ra'ed which translations he found wrong.

## Next moves

1. `git status`; `git switch task-52`; `git pull`.
2. Read hq's ruling. No ruling: stop and ask for it.
3. Write U8 and `onyx/data/keys/U8.json`, with the barred-act classifier and its tests, test first; commit before the first run.
4. Run through `runs.record` with scenario `unseen/U8-steered-subscriber`, root `runs/u8`, `max_usd` as ruled. The guard's USD 1.71 is wrong: do not rely on it. Then eval, annex, README, Arabic check, report-back `docs/report-back/2026-11-06-task-52-built.md`.
5. Complaint steps are 7 and 8: `grievance_expressed` stays on once set. U8 also needs a row in the README's unseen list and on the runs page.
