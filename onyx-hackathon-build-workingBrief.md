# Working brief: onyx-hackathon-build

Updated 2026-11-04 (sixty-third wrap, Opus). Handover for the next session.

## Objective

Merge Task 45, then build Tasks 47 and 46 before the freeze on 2026-11-06. Submission 2026-11-09.

## State

- Task 45 done on branch `task-45`, PR #14 open, not merged. CI "reproduce" passed on `0067da5`; check it on the wrap commit.
- Manifest 108 rows (100 / 5 / 3); register 15 gaps, 2 candidates; report 12 pages, main text 5; 722 tests.
- Orders for Tasks 46 and 47 are untracked in `docs/work-orders/`, deliberately not in PR #14.

## Open questions

- Iyas: merge PR #14; send the reviewer email if not yet sent.
- hq: its one "done means" check on Task 45.

## Next moves

1. `git status`; check `gh pr checks 14` on the wrap commit.
2. On Iyas's word: `gh pr merge 14 --merge`, tag `task-45`, push the tag as `refs/tags/task-45`, check CI on main.
3. `git pull` on main, then Task 47's order on branch `task-47` (it ranks above Task 46 if only one fits).
4. Task 46's order on branch `task-46`.
