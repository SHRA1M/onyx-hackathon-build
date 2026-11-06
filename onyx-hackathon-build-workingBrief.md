# Working brief: onyx-hackathon-build

Updated 2026-11-06 (eighty-fifth wrap, Opus). Handover for the next session.

## Objective

Finish Task 54 from Fable's ruling on its stop. Open work after it: the video. Submission 2026-11-09.

## State

- **Task 54: stopped at C.3, on branch `task-54`, pushed, no PR, not merged.** Order: `docs/work-orders/2026-11-06-task-54-audit-fixes.md`.
- Built: A.1, A.2, A.4, A.5, A.7, B.1 to B.3, C.4. Already in from Task 53: A.3, A.6, C.1, C.2. 1167 tests pass; main text ends page 5, annex page 6, 16 pages.
- Not built: the Annex C paragraph (C.3), the README bullet (C.5), "(Annex C)" on the S3 and S5 lines.
- Not run: the count list, the item 25 grep. Report PDF not rebuilt; the docx is.
- `task-54` carries the eighty-fourth wrap's three files, which never reached main.

## Open questions

1. Fable: the seven questions in `docs/report-back/2026-11-06-task-54-stop-1.md`. No ruling has reached this repo.
2. hq: did its one "done means" check on Task 53 run?
3. Iyas: is Zaid Saaydeh in the Faculty of Artificial Intelligence? "Students" stays out until then.
4. Arabic check on Task 52's merged text, still owed (`docs/report-back/2026-11-06-task-52-arabic-check.html`).
5. Earlier, still open: two AI reads of the gap-15 Cabinet sentence; hq's three items in `docs/report-back/2026-11-05-task-51-built.md`; Iyas asks Ra'ed which translations he found wrong.

## Next moves

1. `git status`; `git switch task-54`; `git pull`.
2. Read Fable's ruling. No ruling: ask for it, build nothing.
3. Build what it says, then the closing checks in the order's part D: report-back at `docs/report-back/2026-11-07-task-54-built.md`, PR, not merged.
4. Any report change: measure page 5 on a scratch build first (`build_report.py --out <scratch>`, then `report_pages.ps1 -Path <scratch>`).
