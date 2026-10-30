# Report-back: Task 33, the three 10-30 searches enter the KB and register (2026-10-30)

Order: `docs/work-orders/2026-10-30-task-33-three-searches.md` (hq, Fable, 2026-10-30). Read files:
`perplexity-2026-10-30/none-rows-read-2026-10-30-fable.md`, `foreign-currency-read-2026-10-30-fable.md`,
`uae-unread-read-2026-10-30-fable.md`. Base: `main` after Task 32 (tag `task-32`). Branch `task-33`. Opus 5.5, two
sessions (the forty-eighth wrap held Part A and Part C data). USD 0.

**Limits:** KB rows, gap data, the register and site render code, the report count check, report and README text. No
model call, nothing recorded, nothing sent outward, nothing under `runs/`, `onyx/data/keys/` or `kb/chunks/`, no gate,
rule, mandate, eval, model, prompt or agent file changed (check 10). Seven layers (`engineering/_reference/llm-agents.md`):
unchanged from Task 32; nothing shipped or deferred by this task. Owner of any failure: Iyas.

## Summary

The Executive Order 3/2004 is no longer "unpublished" anywhere: the row holds the full English order (28 pages) and an
Arabic row is added (33 pages). Eleven rows in all; the KB is 74 documents, 69 VERIFIED, 2 REFERENCED, 3 UNVERIFIED,
21 foreign, 31 UAE instruments. Gap 8 and candidate 4.4 have examples now; gaps 1, 2 and candidate 79 bis (2) gain six
searched clauses from the Order and the two Cabinet fine schedules. All 17 foreign rows re-checked at source: no text
has changed. The report holds 5 pages after one ruling from Iyas (row 8 drops "TS").

## Decisions and choices

1. **Executive Order id (restated plainly).** The English row keeps its id `executive-order-3-2004`; it is not renamed
   `-en`, because `onyx/data/mandates.json` cites that id and the Limits forbid agent data changes. The Arabic row is
   `executive-order-3-2004-ar`. The register's clause ids are `executive-order-3-2004:32` and `executive-order-3-2004:42`.
2. **Data Office sentence.** In the register: appended to gap-2's note (gap 2 is addressed to TDRA and the Data
   Office). In the report: not placed, because 5 pages do not hold it; it is in the README once, under the
   register table, as the order allows.
3. **Row 1 cell** ("no fine for a missing hand-over"): not added; 5 pages do not hold it.
4. **Row 8 cell (Iyas, 2026-10-30).** The ordered cell "3GPP TS 28.535 §4.2.3; ETSI ZSM 009-1 §7.2.2.4" wraps in the
   narrow column and made the report 6 pages (two lines over; with the old cell it was 5). Tested in Word: dropping
   "TS" holds 5 pages, dropping the clause numbers also holds 5, a "ZSM" without "ETSI" does not. Iyas chose
   **"3GPP 28.535 §4.2.3; ETSI ZSM 009-1 §7.2.2.4"**. The register, README table and site keep "3GPP TS 28.535".
5. **"fifteen" recounted.** 31 UAE instruments (the announcement is not one) minus the four the sentence names
   (Telecommunications Law 3/2003, CPR v2.0, Licence 2/2026, PDPL) = **27**: "twenty-seven other UAE laws, resolutions
   and TDRA instruments". The count check now tests it. **For hq:** the 27 include two operator codes, two federal AI
   guidelines, the CSC policy, a TDRA service page and two unpublished texts, so "laws, resolutions and TDRA
   instruments" is loose; "twenty-seven other UAE texts" is shorter and exact if hq wants it (the check would need
   its pattern widened).
6. **`cabres-52-2024-ar:2(2)`** quotes the PDF text layer as stored, with its two spacing faults ("مضاعفةقيمة",
   "مض ي"); the `says` names both. **For Iyas:** eye-check against the PDF, page 2 (hq: the choice stands).
7. **Arabic quote label.** A `searched` entry quoted from a file printed "EN" whatever the language; it now prints "AR"
   (and `dir="rtl"` on the site) when the quote is Arabic. Only `cabres-52-2024-ar:2(2)` is affected.
8. **gap-8 prose line** is a new field `examples_note`, printed after the examples on the register and the site. It
   says both texts are method texts like Y.3172 and never that they outrank it.
9. **TKG § 56(3)** quote is the continuous run "kann der Endnutzer ... kündigen."; the English gloss is in `says`,
   starting "Our English, not an official translation:".
10. **`cabres-52-2024-en`** is the portal page's English article text read through Iyas's Chrome (not taken from the
    read file).
11. **EECC Art 105** is held from legislation.gov.uk; EUR-Lex refused non-browser fetches (HTTP 202). In Chrome today
    EUR-Lex's own adopted text (CELEX 32018L1972, `#art_105`) contains the Art 105(3) quote word for word. The row was
    not switched.
12. **Wales** is one row whose file holds reg 3 and Schedule 1. Re-held from the current text (`/data.xht` without
    `/made`) into `kb/sources/global/` and `kb/sources/` alike, with legislation.gov.uk's annotations (E+W, F1, I1) kept
    as printed. The extractor was first proved on the `/made` pages: it rebuilds the held file exactly (642 of 642
    Schedule lines, reg 3 identical). The manifest title never said "as made"; the notes did and now name S.I.
    2021/1352 (2021-12-03, reg 3(1)) and S.I. 2025/339 (2025-03-28, reg 3(3)). The Task 30b test that pinned reg 3(1)
    as made now pins the current wording. Standards 15, 22 and 60 quotes unchanged and found.

## Part A: hashes

Every SHA-256 the order names equals the file held, and hq's copy (`test_task_33_rows_are_the_orders`, check 1b):
3GPP `f43be1bd...`, ETSI ZSM `492bac22...`, Executive Order EN `23f3e402...`, AR `99cb1e43...`, 200/2025 EN
`cdff987a...`, AR `ad851801...`, 52/2024 AR `32c667ed...`. EECC `afa1a1d4...` and TKG `ed78ba96...` are this build's
extracts (no hq hash named). 200/2025 Gazette date from the portal record: Official Gazette 813 of 2025-12-12, in force
2025-12-13.

## Part B: the 17 foreign rows (fetched 2026-10-30)

Nine rows re-fetched by a helper and rebuilt byte-equal to the manifest (detail:
`docs/report-back/2026-10-30-task-33-partb-refetch-notes.md`). The eight EUR-Lex rows refuse non-browser clients
(AWS WAF challenge, HTTP 202), so per hq they were read in Iyas's Chrome, reading only: each article element's text,
whitespace collapsed, hashed and compared with the same article of the held file. The scrapling extraction cannot be
re-run byte for byte, so these are "text equal, hash not compared", not a hash pass.

| row | result |
|---|---|
| imda-mgf-agentic-v1-5 | hash equal (raw PDF) |
| us-47cfr-64-2010 | hash equal (rebuilt) |
| ca-ola-s22-27 | hash equal (rebuilt) |
| es-ley-10-2025 | hash equal (rebuilt) |
| wales-wls-no1-2015-sch1 | hash equal for `/made` (rebuilt); then re-held from the current text (decision 12), new hash `8ae75b07...` |
| us-tsr-16cfr310 | hash equal (rebuilt) |
| sg-eta-2010-s15 | hash equal (rebuilt) |
| us-utah-13-77-102 | hash equal (rebuilt) |
| ca-bccrt-2024-149-moffatt | hash equal (rebuilt) |
| eu-crd-2011-83-art8 | text equal, hash not compared (Art 8: 772 words) |
| gdpr-art22 | text equal, hash not compared (Art 22: 222) |
| gdpr-art12-28-33 | text equal, hash not compared (Arts 12, 28, 33: 586, 878, 288) |
| eu-dsa-2022-2065-art12-20 | text equal, hash not compared (Arts 12, 20: 116, 426) |
| eu-ecommerce-2000-31-art10-11 | text equal, hash not compared (Arts 10, 11: 204, 159) |
| eu-roaming-2022-612-art14 | text equal, hash not compared (Arts 14, 24: 1354, 86) |
| eu-ai-act-2026-07-27-art14-26 | text equal, hash not compared (Arts 14, 26: 512, 1159) |
| eu-ai-act-2026-07-27 | text equal, hash not compared (abridged extract: 12 of 12 held text lines found word for word; the bracketed omissions are the file's own) |

Latest consolidations, from each CELEX record page in Chrome: AI Act 32024R1689 **2026-07-27**; GDPR 32016R0679
**2016-05-04**; CRD 32011L0083 **2026-09-27**; e-Commerce 32000L0031 **2024-02-17**. Each is the one held, so no
newer consolidation exists to compare. No stop.

Spain's note and gap 1's note gain "In force 2025-12-28; companies have until 2026-12-28 to adapt (disposición
transitoria única)."; both AI Act rows gain "Regulation (EU) 2026/1744 (OJ 2026-07-24) is inside this consolidation; it
does not touch Art 50(1) or 50(5)."

## Count check (every number, `docs/build_report.py` `check_kb_counts`)

```
'holds 74 documents': report 74, manifest 74 (documents)
'**SRC-2** 74 documents': report 74, manifest 74 (documents)
'69 are verified': report 69, manifest 69 (verified)
'twenty-one foreign texts': report 21, manifest 21 (foreign)
'twenty-seven other UAE laws': report 27, manifest 27 (uae_other)
UAE instruments 31 minus 4 named = 27
problems: []
value check: 0 failures
```

The check read "twenty-one" as "one" before; it now reads hyphenated numbers, and the "other UAE laws" count is new.
Line 26 now reads "two unpublished texts and one unreachable one back no claim" (UNVERIFIED: the Cabinet agentic
framework, the PDPL executive regulations, the CSC policy; tested).

## Checks

| # | Check | Output |
|---|---|---|
| 1 | `kb verify` | `VERIFIED 69  REFERENCED 2  UNVERIFIED 3  HISTORICAL 0` / `every fetched source matches its sha256`; 74 rows, 21 foreign, 31 UAE instruments (`test_task_33_rows_have_no_chunks_and_the_counts_are_the_orders`) |
| 1b | Order and hq SHA-256 | all seven named hashes equal the held file and hq's copy (above) |
| 2 | Part B | 17 rows: 9 hash equal, 8 text equal (hash not compared); 4 consolidations are the held ones |
| 3 | Quote-in-stored-text, new entries | `test_task_33_quotes_are_verbatim_in_the_stored_text`: 10 of 10 (6 searched, 4 global examples; local, CI skips) |
| 4 | `check-data` | `check-data ok: every quote verbatim, every rule cites a clause` |
| 5 | Register, replay pages, viewer, site, intent, datasheet, export rebuilt twice | 19 files identical on the second run; viewer identical on rebuild. Changed by this task: gap 8's replay line now names 3GPP TS 28.535 §4.2.3 |
| 6 | Replay | S1 to S5, runs 1 to 3: "chain ok; replay matches the recorded verdicts" (15 of 15) |
| 7 | `verify-log` | 227 of 227 chained logs pass (the 6 `gaps/candidates.jsonl` are not chained logs, as in Task 32) |
| 8 | Report | `scripts/report_pages.ps1`: `pages: 5`, `words: 2243`; two builds byte-identical (`b0d84f98...`) |
| 9 | hq copy | `docs/report.md` copied to `D:\Projects\hq\uni\ai-for-good-hackathon\report-draft-2026-10-23.md` (old kept as `.bak-2026-10-30-task-33`); both sha256 `e1d6c4b2...` |
| 10 | Limits | `git diff main -- onyx/gate.py onyx/data/rules.json onyx/data/keys onyx/data/mandates.json onyx/eval.py runs/ onyx/model.py onyx/prompts onyx/agents kb/chunks eval/`: 0 lines |
| 11 | Full suite | `607 passed` |
| 12 | CI on PR #9 | push run 41114092776 and PR run 41114124399 on b0a930d: `pass` (1m55s, 1m54s); "227 logs: chain ok"; S1 to S5 replay match |

## Open questions for hq

- Decision 5: keep "twenty-seven other UAE laws, resolutions and TDRA instruments", or "twenty-seven other UAE texts".
- The Data Office sentence and the row 1 cell are out of the report for space; say if either should displace something.
- Carried from Task 31: eIDAS and COPPA have stored texts but no manifest rows.

## Merge danger

Two-way door: data, render code and report text. The new `examples_note` field and the AR label change nothing for
rows without them. The replay viewer and S2 replay page change only on gap 8's "Elsewhere" line.
