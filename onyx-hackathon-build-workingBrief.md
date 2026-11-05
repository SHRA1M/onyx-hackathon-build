# Working brief: onyx-hackathon-build

Updated 2026-11-04 (sixty-ninth wrap, Opus). Handover for the next session.

## Objective

Get Task 49 through hq's check and Iyas's word on the merge, and hold `main` ready for the freeze on 2026-11-06 and submission on 2026-11-09.

## State

- Task 49 is built on `task-49`, draft PR #18, not merged. Order `docs/work-orders/2026-11-05-task-49-register-wording.md`, with hq's rulings on stop 1.
- CI "reproduce" on `a14f960`: run 41929281626 (push), run 41929290011 (PR), success; 736 passed, 26 skipped; 228 logs chain ok.
- Tests 762 on the branch, 756 on main. Report: body 5 pages, annex from page 6, 12 in all.
- This wrap's commit goes on `task-49` after those checks, so it has its own CI run, which is not named here.
- `main` is untouched, at `5bbd68a`.

## Open questions

1. For hq: items 8 and 9 stay in only because `_row_all` in `tests/test_gaps.py` now leaves their two lines out of what older tests read. If hq reads the order's condition more strictly, both lines and the helper change come out.

## Next moves

1. `git status`; `git switch task-49`; `git pull`.
2. Confirm CI passed on this wrap's commit.
3. Wait for hq's check of `docs/report-back/2026-11-05-task-49-built.md` and Iyas's word. Do not merge before both.
4. On his word: mark PR #18 ready, merge, check CI on main. A later order may bring the full audit's findings; invent no work.
