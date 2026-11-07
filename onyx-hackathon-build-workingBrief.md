# Working brief: onyx-hackathon-build

Updated 2026-11-06 (eighty-sixth wrap, Opus). Handover for the next session.

## Objective

Finish Task 54 from Fable's ruling on stop 2. Open work after it: the video. Submission 2026-11-09.

## State

- **Task 54: stopped a second time, on branch `task-54`, pushed, no PR, not merged.** Order: `docs/work-orders/2026-11-06-task-54-audit-fixes.md`. Ruling on stop 1: `D:\Projects\hq\uni\ai-for-good-hackathon\task-54-stop-1-ruling-2026-11-06-fable.md`.
- Stop 2: `docs/report-back/2026-11-06-task-54-stop-2.md`, eight questions. Its draft annex table is ready once the rows are ruled.
- Why it stopped: the main text stays 2 lines over page 5 after every cut the ruling allows, and the ruling's S4 text does not match the logs.
- Built: A.1, A.2, A.4, A.5, A.7, B.1 to B.3, C.4. Already in from Task 53: A.3, A.6, C.1, C.2. 1167 tests pass. Committed report: main text ends page 5, annex page 6.
- Arabic checks from the ruling are done: 0 empty boxes, 0 ligature hits, S5 page 3 looked at.
- Not built: Annex C table (C.3), README bullet (C.5), the S4 and S5 lines, "(Annex C)" on S3, their kept tests, the `CHANGELOG.md` entry, rebuilt docx and PDF.
- Not run: the count list, the item 25 grep.
- `f5d9c88` was not cherry-picked: its content is already here through the eighty-fifth wrap.

## Open questions

1. Fable: the eight questions in stop 2. No ruling has reached this repo.
2. hq: did its one "done means" check on Task 53 run?
3. Iyas: is Zaid Saaydeh in the Faculty of Artificial Intelligence? "Students" stays out until then.
4. Earlier, still open: two AI reads of the gap-15 Cabinet sentence; hq's three items in `docs/report-back/2026-11-05-task-51-built.md`; Iyas asks Ra'ed which translations he found wrong.

## Next moves

1. `git status`; `git switch task-54`; `git pull`.
2. Read Fable's ruling on stop 2. No ruling: ask for it, build nothing.
3. Check any sentence it prescribes against the logs before writing it.
4. Build what it says, then the closing checks in the order's part D: report-back at `docs/report-back/2026-11-07-task-54-built.md`, PR, not merged.
5. Any report change: measure page 5 on a scratch build first (`build_report.py --md <scratch> --out <scratch>`, then `report_pages.ps1 -Path <scratch>`).
