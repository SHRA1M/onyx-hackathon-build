# Task 37 report-back: two fixes from hq's audit of Task 36 (2026-11-02, Opus)

Order: `D:\Projects\hq\uni\ai-for-good-hackathon\task-37-audit-fixes-2026-11-02.md`, built on `task-36` so PR #13
carries both tasks.

## What was built

1. `README.md:14` now says "`docs/report.docx`, the Requirements and Mapping sections,". The grep of `README.md`,
   `docs/site/*.html` and `kb/DATASHEET.md` found no other numbered pointer into the report. The other "section N" hits
   are a law's own sections (kb.html, gaps.html: CFR, AI Act, Utah, California) or a source note's sections
   (gaps.html: `docs/sources/...md sections 5 and 6`, `... section 3`), not the report, and were left alone. New test
   `tests/test_report.py::test_no_numbered_section_pointer_into_the_report`: it failed on the old README
   (`['README.md: ..., sections 3']`) and passes now.
2. Report gap rows reordered to 1 to 6, 8 to 12. Only the row order changed: same lines, same text. `test_report.py:97`
   now checks rows 10 and 11 hold "11" and "12", comment "Task 37, rows in number order".
3. `docs/report.docx` rebuilt, `docs/site/gaps.html` regenerated, hq copy replaced, CHANGELOG line.

## Differs from the order

- `onyx/data/gaps.json` was already in id order (gap-1 to gap-12, then the two candidates), and so were the README
  register and `docs/gaps.md`: `python -m onyx gaps` regenerated them with no diff. Only the report's table was out of
  order. `docs/site/gaps.html` takes its order from the report's table (`site.gap_order`), so it followed the report.
  That function puts rows the report leaves out at the end, so the site reads 1 to 6, 8 to 12, then gap 7. The report
  has no row 7 (it was deleted in Task 23).
- Nothing reads `gaps.json` by position: a grep for index reads on the gaps list found none.

## Checks

1. `scripts/report_pages.ps1`:

```
pages: 5
words: 2346
```

2. `grep -n "^| [0-9]* |" docs/report.md`:

```
137:| 1 |
138:| 2 |
139:| 3 |
140:| 4 |
141:| 5 |
142:| 6 |
143:| 8 |
144:| 9 |
145:| 10 
146:| 11 
147:| 12
```

3. `grep -n "sections 3 and 4" README.md`: no output (exit 1).
4. `docs/build_report.py` passes its count and value checks. Selftest ends "figures match a fresh eval of runs/", same
   rows as at Task 36 (C5 recall 0.96 / 1.00, citation 0.99 / 1.00 in `eval/results.md`, unchanged).
5. Full suite: `644 passed in 144.87s (0:02:24)` (643 plus the new test). CI: `reproduce` green on the push (run 41418780306) and on PR #13 (run 41418788802).
6. Files changed against the Task 36 head (`15df647`): see the commit; README.md, CHANGELOG.md, docs/report.md,
   docs/report.docx, docs/site/gaps.html, tests/test_report.py and this file.
7. sha256: `docs/report.md` and hq's `report-draft-2026-10-23.md` are both
   `46db4387f9a730eb22f549430c1297d728950b98bb2ab44b31dc402cbcdf0908`.

## Open for hq

Nothing new. Carried from Task 36: Arabic PDPL chunk text for `why --lang ar`; in-force dates; Saudi Arabic eye-check.
