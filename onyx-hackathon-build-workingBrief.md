# Working brief: onyx-hackathon-build

Updated 2026-11-01 (fifty-third wrap, Opus). Handover for the next session.

## Objective

Finish Task 36 (`docs/work-orders/2026-11-01-task-36-template-items.md`) on branch `task-36` (local, four commits,
not pushed). Items 2 (`onyx why`) and 3 (gap-4 rule and page) are built and tested; item 1 (report headings and new
sections) is in `docs/report.md`, but Word says 6 pages. Every change before 2026-11-06; submission 2026-11-09.

## State

- Report on `task-36`: 6 pages, 2,424 words, 12 lines on page 6 after order cuts 1 to 4 and hq's ruling cuts 1 and 2.
- Stop 2 filed: `docs/report-back/2026-11-01-task-36-stop-2.md` (count, every line on page 6, questions for hq).
- Full suite 641 passed. Not pushed, no PR.

## Open questions (with hq)

- Which cut takes the last 12 lines: hq-written gap cells, a shorter Recommendations, narrower figures, other.
- The filed order names the template's example team; the order says that name never appears in the repo.
- Carried: in-force dates (Maine, India TCCRR, Korea Art 31); Saudi Arabic eye-check; GitHub Pages on submission day.

## Next moves

1. `git status`; `git checkout task-36`.
2. Apply hq's stop-2 answer word for word; build the report; `scripts/report_pages.ps1` must say 5.
3. Then the order's item 4: README demo list and `why` line, `verify.html` line (`python -m onyx site`), hq report
   copy, CHANGELOG, selftest figures (C5 0.96 / 1.00, citation 0.99 / 1.00), PR, report-back with outputs pasted.
