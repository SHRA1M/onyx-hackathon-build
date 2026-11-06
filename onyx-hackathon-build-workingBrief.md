# Working brief: onyx-hackathon-build

Updated 2026-11-06 (eighty-second wrap, Opus). Handover for the next session.

## Objective

Finish Task 53 once Fable rules on stop 3, then the video. Submission 2026-11-09.

## State

- **Task 53: stopped a third time, branch `task-53`, pushed, no PR, not merged.** Items 29 to 44 are applied. Main text ends page 6, 9 lines over; it must end on page 5.
- Tests: 1137 passed, 1 failed, the docx not rebuilt.
- Report-back: `docs/report-back/2026-11-06-task-53-stop-3.md`. Its scratch measurements: only Figure 1 out with the demo items run together reached 5 pages. Figure 1 out alone leaves 3 lines.
- Four hidden Word processes may still run (PIDs 2828, 17308, 7820, 23228, `/Automation -Embedding`, no window), unless Windows was restarted. They were left by this build; closing them was refused. Item 37 wants them gone before the rebuild.

## Open questions

1. hq: the six questions in the stop 3 report-back. Until the ruling is in the order, do not cut.
2. Iyas: is Zaid Saaydeh in the Faculty of Artificial Intelligence? His registration is also open (session 5 ruling).
3. Arabic check on Task 52's merged text, still owed (`docs/report-back/2026-11-06-task-52-arabic-check.html`).
4. Earlier, still open: two AI reads of the gap-15 Cabinet sentence; hq's three items in `docs/report-back/2026-11-05-task-51-built.md`; Iyas asks Ra'ed which translations he found wrong.

## Next moves

1. `git status`; `git switch task-53`; `git pull`. Commit the order's new items, by name.
2. Apply those items and only those. Measure page 5 on a scratch build after each. Still over: stop.
3. Check for hidden Word. Rebuild docx and PDF, rerun item 25 and list every hit, full `pytest`, push, open the PR, watch CI.
4. Write `docs/report-back/2026-11-06-task-53-built.md`, give Iyas the path. He merges.
