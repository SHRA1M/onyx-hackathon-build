# Task 24: the three UAE texts Task 23 left out, into the KB and the register (2026-10-24)

Written by hq (Opus 5.5, mechanical follow-up to a Fable decision). Build on Opus.

## Why

Task 23 was built without Decree-Law 14/2023 (EN, AR) and Cabinet Resolution 28/2023 (EN) because the portal refused a
script. hq has now saved the official PDFs from a browser. This order adds exactly what Task 23 would have added for them.

## Base

Start only after Task 23 is committed and its report-back is filed. Base = the last Task 23 commit. If Task 23 is not
committed, stop and ask.

## Inputs (on disk, checked by hq: `%PDF-` header, text layer present)

Folder: `D:\Projects\hq\uni\ai-for-good-hackathon\perplexity-2026-10-24\fetched-2026-10-24\`

| File | Bytes | Pages | sha256 starts | Portal URL |
|---|---|---|---|---|
| law-14-2023-en.pdf | 140244 | 17 | a52f4dcc23156819 | https://uaelegislation.gov.ae/en/legislations/2150/download |
| law-14-2023-ar.pdf | 187890 | 11 | 4769f8f1af60d537 | https://uaelegislation.gov.ae/ar/legislations/2150/download |
| cabres-28-2023-en.pdf | 199612 | 30 | 89ab2b52d9d53400 | https://uaelegislation.gov.ae/en/legislations/2199/download |

Copy them in. Do not re-download. Record the portal URL as the source and 2026-10-24 as accessed.

## Task

1. **KB rows.** Add the three rows exactly as Task 23 Part A specified them (order file
   `task-23-gap-hunt-order-2026-10-24.md`, Part A table, rows law-14-2023-en, law-14-2023-ar, cabres-28-2023-en), status
   VERIFIED with the full sha256, text extracts in `standards-text/` the same way the other UAE texts are stored, chunks for
   the clauses cited below, and `kb/local-sources.json` and `kb/export/InputDocs/Inputs.md` updated as in Task 23.
2. **Register.** Add every Trade Law 14/2023 and Cabinet Resolution 28/2023 `searched` entry Task 23 Part B named and Task 23
   left out: gap-11 (Art 5(5), 6(7)), gap-2 (Art 13(2)), gap-6 (Art 1), gap-7 (Art 1, 5(7)), gap-1 (Art 6(7)), gap-3
   (Cabinet 28/2023 Art 15(9), 24(3)). Each with its verbatim quote from the PDF text. Regenerate `docs/gaps.md` and the
   README table.
3. **Counts.** Update the KB totals everywhere Task 23 updated them (report Introduction, report lines that state counts,
   README, the tests pinned to them), from the manifest. One set of numbers everywhere.
4. **Nothing else in the report.** No row, recommendation or prose changes beyond the counts. The report does not cite
   these texts.

## Report-back must paste, verbatim from the PDFs

Decree-Law 14/2023 English: Art 1 (definitions "Modern Technology-Based Trade" and "Modern Technology"), Art 2(2)(b),
Art 5(5), Art 5(7), Art 6(7), Art 13(2). Cabinet Resolution 28/2023: Art 15(9), Art 24(3).
hq has not yet read Art 5(5). If its text does not support "a safe default against a mistaken order", leave Art 5(5) out
of gap-11 and say so.

## Done means (show each output)

1. `git diff <base> -- onyx/gate.py onyx/data/rules.json onyx/data/keys onyx/data/mandates.json onyx/eval.py runs/` is empty.
2. Tagged-paragraph grep for changed `[C3` / `[C5` paragraphs is empty.
3. `eval` recompute byte-identical to `eval/results.md` and `eval/results.json`.
4. `kb/manifest.csv`: the three rows present, VERIFIED, sha256 matching `sha256sum` of the committed PDFs.
5. `docs/gaps.md` shows the new `searched` entries for gaps 1, 2, 3, 6, 7, 11.
6. Report still 5 pages (`scripts/report_pages.ps1`), word count printed.
7. Full test suite passes; CI green on the pushed commit.
8. No manifest row changed only by a refreshed `url_accessed`.

## Limits

Words and data only. No code beyond regenerating what the existing scripts generate. No scored runs, no API spend.
No other competitor's name in any tracked file. Stop and ask if a quote cannot be found in the PDF text, if pages go to
six, or if any frozen-set check is not empty.
