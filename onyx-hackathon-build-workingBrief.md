# Working brief: onyx-hackathon-build

Updated 2026-11-07 (eighty-eighth wrap, Opus). Handover for the next session.

## Objective

Task 54 is merged (PR #25). Open work: the video. Submission 2026-11-09.

## State

- `main` at 940df10 plus this wrap. Report: main text ends page 5, annex page 6, 16 pages; docx and PDF current. 1178 tests pass; CI green.
- No order is open in this repo.

## After the shortlist

- Survey every exact-match read in `gate.py` outside `read_items`; Task 55 item 3 covers what it finds (stop-3 ruling C).
- Task 55 item 3, the two match-only checks: Fable writes the Perplexity question first; no order before that read (stop-3 ruling B.2).
- Task 55 items 1 and 2: `marketing_gate` on outbound words; a text deadline held, not blocked. Order text in `docs/work-orders/2026-11-06-task-54-audit-fixes.md`.

## Open questions

1. hq: did its one "done means" check on Task 53 run?
2. Iyas: is Zaid Saaydeh in the Faculty of Artificial Intelligence? "Students" stays out until then.
3. Earlier, still open: two AI reads of the gap-15 Cabinet sentence; hq's three items in `docs/report-back/2026-11-05-task-51-built.md`; Iyas asks Ra'ed which translations he found wrong; Task 52's Arabic check.

## Next moves

1. `git status`; `git pull` on `main`.
2. Wait for the next order from `D:\Projects\hq\uni\ai-for-good-hackathon\` (the video, or the submission-day order). Build nothing without one.
3. Any report change: measure page 5 on a scratch build first (`build_report.py --out <scratch>`, then `report_pages.ps1 -Path <scratch>`).
