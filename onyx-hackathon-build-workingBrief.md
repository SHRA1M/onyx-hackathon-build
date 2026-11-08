# Working brief: onyx-hackathon-build

Updated 2026-11-08 (eighty-ninth wrap, Opus). Handover for the next session.

## Objective

Task 56 (site restyle) is built, PR #26 open, not merged. Next: the README task, from its own order. Submission 2026-11-09.

## State

- Branch `task-56` pushed, PR #26 (https://github.com/SHRA1M/onyx-hackathon-build/pull/26). It carries Task 56 and the eighty-eighth wrap (bd3cc6e), which was on local `main` only.
- Local `main` is one commit ahead of origin (bd3cc6e) until PR #26 merges.
- 1178 tests pass; selftest exit 0. Report unchanged: main text page 5, annex page 6, 16 pages.
- Report-back: `docs/report-back/2026-11-08-task-56-site-restyle.md`.

## After the shortlist

- Survey every exact-match read in `gate.py` outside `read_items`; Task 55 item 3 covers what it finds (stop-3 ruling C).
- Task 55 item 3, the two match-only checks: Fable writes the Perplexity question first; no order before that read (stop-3 ruling B.2).
- Task 55 items 1 and 2: `marketing_gate` on outbound words; a text deadline held, not blocked. Order text in `docs/work-orders/2026-11-06-task-54-audit-fixes.md`.

## Open questions

1. hq: does Task 56 want a CHANGELOG line? The order's file list left it out.
2. hq: did its one "done means" check on Task 53 run? (`docs/report-back/2026-11-06-task-53-built.md`)
3. Iyas: is Zaid Saaydeh in the Faculty of Artificial Intelligence? "Students" stays out until then.
4. Earlier, still open: two AI reads of the gap-15 Cabinet sentence; hq's three items in `docs/report-back/2026-11-05-task-51-built.md`; Iyas asks Ra'ed which translations he found wrong; Task 52's Arabic check.

## Next moves

1. `git status`. If PR #26 is merged: `git switch main`, `git pull`. If not: ask Iyas before starting the next order on top of it.
2. Build the README order from `D:\Projects\hq\uni\ai-for-good-hackathon\` (one task). Build nothing without an order.
3. Any report change: measure page 5 on a scratch build first (`build_report.py --out <scratch>`, then `report_pages.ps1 -Path <scratch>`).
