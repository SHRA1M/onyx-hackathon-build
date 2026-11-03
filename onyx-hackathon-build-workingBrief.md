# Working brief: onyx-hackathon-build

Updated 2026-11-03 (sixty-first wrap, Opus). Handover for the next session.

## Objective

Finish Task 44 (`D:\Projects\hq\uni\ai-for-good-hackathon\task-44-sweep-fixes-order-2026-11-02.md` with
`task-44-addendum-2026-11-03.md`) on `task-36`. It is built and UNCOMMITTED in the working tree, held at stop 1.
Deadline: pushed with CI green by 2026-11-05; freeze 2026-11-06; submission 2026-11-09.

## State

- Task 43 committed and pushed (`0ac34f7`, `a4fc1db`), CI green on PR #13.
- Task 44: everything but the TRAI items is in (`docs/report-back/2026-11-03-task-44-stop-1.md` lists it).
  Manifest 103 rows; register 15 gaps, 2 candidates. Count tests fail until the TRAI row lands.

## Open questions

- hq: answers file `task-44-stop-1-answers-2026-11-03.md` (TRAI eye-check, C1 Charter, D2, B2, gap 7 draft).
- Iyas: send the reviewer email.

## Next moves

1. `git status` (expect Task 44's files modified plus the stop file), `git pull` on `task-36`.
2. Apply the answers: TRAI row and register lines, SHORT key, counts (104 / 97 / 4 / 3, 38 foreign, 33 UAE
   instruments), Annex F TRAI sentence, E1 sentence.
3. Regenerate, rebuild the report (5 pages, annex page 6), run the 8 done checks and the addendum's lines with output;
   hq copies with backups; CHANGELOG; done report; commit by name; push; `gh pr checks 13`.
