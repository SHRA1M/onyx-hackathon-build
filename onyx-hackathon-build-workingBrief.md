# Working brief: onyx-hackathon-build

Updated 2026-11-06 (eightieth wrap, Opus). Handover for the next session.

## Objective

Finish Task 53 once Fable rules on the page-5 cut, then the video. Submission 2026-11-09.

## State

- **Task 53: stopped, branch `task-53`, pushed, no PR, not merged.** Main text ends page 6, line 37; it must end on page 5.
- Tests: 1108 passed, 1 failed (committed docx not rebuilt, expected).
- Report-back: `docs/report-back/2026-11-06-task-53-stop-1.md`, with `-evidence.md` and `-item-25-hits.md` beside it.
- Task 52b merged, PR #23.

## Open questions

1. hq: the six questions in the report-back (the cut, item 18, S3 mixed logs, item 9's "calls the adviser", Zaid Saaydeh, item 27 not reproduced).
2. A hidden Word process (PID 6680) locks `docs/report.docx`. It must be gone before the rebuild; a restart clears it. If `report.docx` still fails to write, Iyas ends WINWORD.EXE in Task Manager.
3. Arabic check on Task 52's merged text, still owed (`docs/report-back/2026-11-06-task-52-arabic-check.html`).
4. Earlier, still open: two AI reads of the gap-15 Cabinet sentence; hq's three items in `docs/report-back/2026-11-05-task-51-built.md`; Iyas asks Ra'ed which translations he found wrong.

## Next moves

1. `git status`; `git switch task-53`; `git pull`.
2. Iyas takes the report-back to hq; apply only what the ruling names.
3. Measure page 5 on a scratch build. Over: stop again.
4. Rebuild docx and PDF, rerun item 25, full `pytest`, push, open the PR, watch CI.
5. Write `docs/report-back/2026-11-06-task-53-built.md`, give Iyas the path. He merges.
