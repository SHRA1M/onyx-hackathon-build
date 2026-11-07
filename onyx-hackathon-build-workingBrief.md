# Working brief: onyx-hackathon-build

Updated 2026-11-06 (eighty-seventh wrap, Opus). Handover for the next session.

## Objective

Finish Task 54 from Fable's ruling on stop 3. Open work after it: the video. Submission 2026-11-09.

## State

- **Task 54: stopped a third time, on branch `task-54`, pushed, no PR, not merged.** Order: `docs/work-orders/2026-11-06-task-54-audit-fixes.md`. Rulings in `D:\Projects\hq\uni\ai-for-good-hackathon\`: `task-54-stop-1-ruling-2026-11-06-fable.md`, `task-54-stop-2-ruling-2026-11-06-fable.md`.
- Stop 3: `docs/report-back/2026-11-06-task-54-stop-3.md`, two questions and six departures to confirm.
- Question 1: `model_provider_gate` and `sharing_gate` (`gate.py` 478, 442) stop only on an exact English match, so an unmatched word is allowed in a constructed test. No recorded run did this. Does the annex disclose it, and does Task 55 move before submission?
- Question 2: with the ruling's three lines and all five cuts, the main text stays 2 lines over page 5. Fable names the cut.
- Built: A.1, A.2, A.4, A.5, A.7, B.1 to B.3, C.3, C.4, C.5, the Annex A sentence. Already in from Task 53: A.3, A.6, C.1, C.2. 1176 tests pass. Report: main text ends page 5, annex page 6, 16 pages; docx and PDF rebuilt.
- Not built: the S3, S4 and S5 lines in `docs/report.md` (S4 and S5 still disagree with the logs). None of the five cuts is applied.
- Not run: the count list, on final text.

## Open questions

1. Fable: the two questions and six departures in stop 3. No ruling has reached this repo.
2. hq: did its one "done means" check on Task 53 run?
3. Iyas: is Zaid Saaydeh in the Faculty of Artificial Intelligence? "Students" stays out until then.
4. Earlier, still open: two AI reads of the gap-15 Cabinet sentence; hq's three items in `docs/report-back/2026-11-05-task-51-built.md`; Iyas asks Ra'ed which translations he found wrong.

## Next moves

1. `git status`; `git switch task-54`; `git pull`.
2. Read Fable's ruling on stop 3. No ruling: ask for it, build nothing.
3. Check any sentence it prescribes against the logs and the code before writing it.
4. Build what it says, then the closing checks in the order's part D: report-back at `docs/report-back/2026-11-07-task-54-built.md`, PR, not merged.
5. Any report change: measure page 5 on a scratch build first (`build_report.py --md <scratch> --out <scratch>`, then `report_pages.ps1 -Path <scratch>`).
