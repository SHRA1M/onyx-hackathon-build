# Working brief: onyx-hackathon-build

Updated 2026-10-30 (forty-eighth wrap, Opus). Handover for the next session (Opus).

## Objective

Finish Task 33 on branch `task-33` (order `docs/work-orders/2026-10-30-task-33-three-searches.md`, filed in the
wrap commit). Every change before 2026-11-06; submission 2026-11-09.

## Done on `task-33` (committed in the wrap, not pushed)

- Part A: 11 rows in `kb/manifest.csv` and `kb/local-sources.json`; schema language allows `de`. `kb verify`:
  `VERIFIED 69  REFERENCED 2  UNVERIFIED 3`, every fetched source matches. My downloads of the two ETSI PDFs, EECC Art
  105 XML, TKG § 56 HTML and both Executive Order PDFs equal hq's SHA-256 and the order's. EUR-Lex refused Art 105
  (HTTP 202, twice): held from legislation.gov.uk, note says so. Portal rows (200/2025, 52/2024) from hq's copies;
  52/2024 English page text and the 200/2025 Gazette date (813 of 2025-12-12, in force 2025-12-13) read in Chrome.
  New gitignored files: `kb/sources/global/{3gpp-ts-28-535-v19,etsi-gs-zsm-009-1-v1-1-1,eu-eecc-2018-1972-art105,
  de-tkg-2021-para-56,cabres-52-2024-en}.txt` and their copies under `kb/sources/`; rebuild with `kb fetch --local` is
  not needed on this PC.
- Part C data: `onyx/data/gaps.json` has every entry of the order. New field `examples_note` on gap-8 (the prose line
  after the examples): **not rendered yet**. Data Office sentence: appended to gap-2's `note`.
- `onyx/gaps.py` SHORT gains the four new file prefixes. Nothing regenerated; tests not run since.

## Choices to restate in the report-back

1. Plainly (it reached hq garbled): the Executive Order row keeps its id `executive-order-3-2004`; it was not renamed
   to `-en`, because `onyx/data/mandates.json` cites that id and the Limits line forbids agent data changes. The
   Arabic row is `executive-order-3-2004-ar`. Clause ids are `executive-order-3-2004:32` and `:42`.
2. Data Office sentence: in gap-2's note.
3. `cabres-52-2024-ar:2(2)` quotes the PDF text layer as stored ("مضاعفةقيمة", "مض ي"). hq: choice stands; the
   report-back flags it for Iyas to eye-check against the page (PDF p. 2).

## hq's answers (2026-10-30)

- Part B EUR-Lex: open the 8 EUR-Lex rows and the 4 CELEX record pages (`/legal-content/EN/ALL/?uri=CELEX:3...`) in
  Iyas's Chrome, reading only. Per row: download the exact file the manifest names and hash it with the original
  extraction; where that can't be done, compare every quoted article word for word and mark "text equal, hash not
  compared" (not a pass). Record the 4 consolidation dates. A differing hash, or a newer consolidation that changes a
  quoted article, is still a stop.
- The other 9 foreign rows: re-fetched 2026-10-30 by a helper, rebuilt file byte-equal to the manifest SHA-256 for
  all 9 (IMDA, 47 CFR, Canada OLA, Spain, Wales, US TSR, Singapore, Utah, Moffatt). Results:
  `C:\Users\SUPER\AppData\Local\Temp\claude\D--Projects-engineering-onyx-hackathon-build\2cb68851-a7c5-4f1b-8cc6-41cb61f443dc\scratchpad\partb\results.md`
  (scratchpad; copy the table into the report-back early, it may be cleared).

## Next moves, in order

1. `git status -sb` on `task-33`. Render `examples_note` in `onyx/gaps.py` (after the Global example quotes) and
   `onyx/site.py`; label an Arabic quote in a `file` entry "AR" (gaps.py `_searched` file branch prints "EN" today;
   site passes `"en"` to `quote`).
2. Tests first (`/tdd`), Task 32 style: `test_kb.py` Task 33 rows and counts (74/69/3/2/21; 31 UAE instruments =
   distinct UAE instruments minus source_type `announcement`; move the count from the Task 32 test); `test_gaps.py`
   Task 33 searched and examples, quote check (local), and adjust Task 32's `_filed` test and gap-2 note test for
   the new entries; add the 10 new landing/portal rows to `LANDING_ROWS` as needed.
3. Part B rest: EUR-Lex in Chrome (above). Wales re-hold from the current text (both `/data.xht` URLs without
   `/made`; title drops "as made"; notes name S.I. 2021/1352 and 2025/339; change `kb/sources/` and
   `kb/sources/global/` alike); Spain note and gap-1 Spain example note; AI Act notes (2026/1744 sentence).
4. Part D: report counts (74, 69, twenty-one, SRC-2 74), "fifteen" recounted (31 minus 4 = 27, show arithmetic),
   line 26 "two unpublished texts and one unreachable one back no claim", row 8 cell "3GPP TS 28.535 §4.2.3; ETSI ZSM
   009-1 §7.2.2.4", optional row 1 cell and Data Office sentence only if 5 pages hold; README UNVERIFIED line;
   `NUMBER_WORDS` stops at twenty: extend for twenty-one.
5. Regenerate twice (gaps, site, intent, kb datasheet, kb export), check-data, replay S1 to S5, verify-log on all
   logs, full pytest, `build_report.py`, `report_pages.ps1`, copy `docs/report.md` to hq's
   `report-draft-2026-10-23.md` (keep a `.bak-2026-10-30-task-33`).
6. CHANGELOG entry (Executive Order "unpublished" corrected), report-back
   `docs/report-back/2026-10-30-task-33-three-searches.md` with the checks table, push `task-33`, PR, CI green.

## Open questions

- hq (Task 31): eIDAS and COPPA have stored texts but no manifest rows; gap 1's register lists IMDA and the DSA before Spain.
- hq: the report's 371,476 and design counts have no line in `eval/results.md` or `kb/DATASHEET.md` (Task 29 D).
- Submission-day order: GitHub Pages source = `docs/site/`; submission email aiforgoodlab@itu.int.
- hq: strips the two entry names from the filed Task 16 and Task 20 orders before 2026-11-09.
- hq: the team members' spellings for the README team line.
