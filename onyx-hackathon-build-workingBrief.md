# Working brief: onyx-hackathon-build

Updated 2026-11-06 (eighty-first wrap, Opus). Handover for the next session.

## Objective

Finish Task 53 from Fable's stop 2 ruling (order items 38 to 44), then the video. Submission 2026-11-09.

## State

- **Task 53: stopped again, branch `task-53`, pushed, no PR, not merged.** Items 29 to 36 and all four cuts of item 32 are applied. Main text ends page 6, about 18 printed lines over; it must end on page 5.
- Tests: 1118 passed, 3 failed. One is the docx not rebuilt. Two pin the old ending of the third Introduction paragraph (`tests/test_report.py:517`, `tests/test_task_51.py:91`).
- Report-back: `docs/report-back/2026-11-06-task-53-stop-2.md`.
- No hidden Word process at the last check, so the rebuild is not blocked.

## Open questions

1. hq's ruling on stop 2 arrived during the wrap and was not read in full or applied here. It sits in the order, uncommitted, with `task-53-stop-2-ruling-2026-11-06-fable.md` in hq. If layer 7 is still over: stop.
2. Iyas: is Zaid Saaydeh in the Faculty of Artificial Intelligence? His registration is also open (session 5 ruling).
3. Arabic check on Task 52's merged text, still owed (`docs/report-back/2026-11-06-task-52-arabic-check.html`).
4. Earlier, still open: two AI reads of the gap-15 Cabinet sentence; hq's three items in `docs/report-back/2026-11-05-task-51-built.md`; Iyas asks Ra'ed which translations he found wrong.

## Next moves

1. `git status`; `git switch task-53`; `git pull`. Commit the order's items 38 to 44, by name.
2. Apply items 38 to 44 and only those.
3. Measure page 5 on a scratch build after each layer. Over after layer 7: stop.
4. Rebuild docx and PDF, rerun item 25 and list every hit, full `pytest`, push, open the PR, watch CI.
5. Write `docs/report-back/2026-11-06-task-53-built.md`, give Iyas the path. He merges.
