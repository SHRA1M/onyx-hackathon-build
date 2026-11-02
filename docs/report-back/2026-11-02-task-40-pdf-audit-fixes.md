# Report-back: Task 40, two fixes from the Fable audit of report.pdf (2026-11-02, Opus)

Order: `docs/work-orders/2026-11-02-task-40-pdf-audit-fixes.md` (filed copy of hq's
`task-40-pdf-audit-fixes-2026-11-02.md`), with hq's answer to stop 1 (`2026-11-02-task-40-stop-1.md`): option (a).
Built on `task-36` on top of 1a588b7, one push.

## Done means

1. `grep -rn "ITU's request" docs/ README.md` -> nothing (exit 1). `docs/report.md` row 12 ends: "Left open with
   ITU's agreement (2026-10-30)." No site page or README line repeated the old words.
2. Rule: a UAE instrument is a distinct `instrument` of a UAE manifest row whose `source_type` is neither
   `announcement` nor `web_page` (`docs/build_report.py` `NOT_INSTRUMENTS`), as those rows' notes say. 33 UAE ids
   less `fed-ai-data-authority-2026-06-14` and `tdra-dispute-service-page` = 31. The three lines:
   - report.md line 22: "... the Personal Data Protection Law 45/2021 (PDPL) and twenty-seven other UAE texts;"
   - report.md line 131: "Each candidate was then searched across the 31 UAE instruments in both languages, ..."
   - annex.md: "88 documents in `kb/manifest.csv`: 31 UAE instruments (laws, Cabinet resolutions, TDRA regulations,
     the two 2026 public licences, in English and Arabic where both are published) plus a TDRA service page and an
     announcement, which are not instruments; 3 ITU texts and the Readiness report; and 34 foreign texts used only
     as global examples."
   New test `tests/test_annex.py::test_uae_instruments_leave_out_web_pages_and_announcements`: it failed before the
   change (no `NOT_INSTRUMENTS`), then passed. It pins the two rows left out, their notes, 31, and the Annex A
   words. Tightened: the Annex A count pair is now 31 -> 32; report tests check "twenty-seven other UAE texts" and
   "the 31 UAE instruments". The build's count check fails the report on any other number.
3. `report_pages.ps1`: pages: 5, words: 2366, annex starts on page: 6, total pages: 10, total words: 5248.
   `report_pdf.ps1`: word pages: 10, pdf pages: 10, pdf finds 'Annex A': True, pdf finds 'Limits and next steps':
   True, pdf bytes: 359047. The gap 12 line is on PDF page 5 (pypdf), so the cell does not wrap onto page 6.
4. `uv run pytest`: 678 passed. `check-data ok`. CI's generators rerun locally: no drift. Push and CI: in the
   session's closing message.
5. sha256 pairs: in the session's closing message, after the push. hq copies the files itself.

## Departures

The count is 31, not the order's 32 or 33: hq's answer to stop 1, option (a).
