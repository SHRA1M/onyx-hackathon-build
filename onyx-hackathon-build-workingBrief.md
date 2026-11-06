# Working brief: onyx-hackathon-build

Updated 2026-11-06 (eighty-first wrap, Opus). Handover for the next session.

## Objective

Finish Task 53 once Fable rules on stop 2, then the video. Submission 2026-11-09.

## State

- **Task 53: stopped again, branch `task-53`, pushed, no PR, not merged.** Items 29 to 36 and all four cuts of item 32 are applied. Main text ends page 6, about 18 printed lines over; it must end on page 5.
- Tests: 1118 passed, 3 failed. One is the docx not rebuilt. Two pin the old ending of the third Introduction paragraph (`tests/test_report.py:517`, `tests/test_task_51.py:91`).
- Report-back: `docs/report-back/2026-11-06-task-53-stop-2.md`.
- No hidden Word process at the last check, so the rebuild is not blocked.

## Open questions

1. hq, the six in the report-back: what pays the 18 lines; item 32(d)'s sentence overstates CI; figures at 7.7 cm print at about 3 to 4 pt; item 30's field names; item 29's "documents" and its place; item 31's "no telecom field".
2. Iyas: is Zaid Saaydeh in the Faculty of Artificial Intelligence? His registration is also open (session 5 ruling).
3. Arabic check on Task 52's merged text, still owed (`docs/report-back/2026-11-06-task-52-arabic-check.html`).
4. Earlier, still open: two AI reads of the gap-15 Cabinet sentence; hq's three items in `docs/report-back/2026-11-05-task-51-built.md`; Iyas asks Ra'ed which translations he found wrong.

## Next moves

1. `git status`; `git switch task-53`; `git pull`.
2. Iyas takes the report-back to hq; apply only what the ruling names.
3. Measure page 5 on a scratch build. Over: stop again.
4. Rebuild docx and PDF, rerun item 25 and list every hit, full `pytest`, push, open the PR, watch CI.
5. Write `docs/report-back/2026-11-06-task-53-built.md`, give Iyas the path. He merges.
