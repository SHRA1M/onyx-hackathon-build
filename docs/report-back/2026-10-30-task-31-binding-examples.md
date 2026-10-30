# Report-back: Task 31, binding global examples for gaps 2, 7 and 12; the flagged gap explains itself (2026-10-30)

Order: `docs/work-orders/2026-10-30-task-31-binding-examples.md` (hq, Fable, 2026-10-30; Part D added the same day).
Read file: `perplexity-2026-10-30/global-examples-narrow-read-2026-10-30-fable.md` sections 2 and 4. Base: `main` at
74e63e3 (PR #6 merge, tag `task-30`). Branch `task-31`. Opus 5.5. USD 0.

**Limits:** words, data and render code only. No model call, nothing recorded, nothing sent outward, nothing under
`runs/` or `onyx/data/keys/`, no gate, rule, mandate, eval, model or prompt file changed (check 9). Owner of any
failure: Iyas.

## Summary

Five texts fetched from the issuing bodies' own sites by the routes in the read file, every quoted sentence word for
word as the read file has it. KB 59 documents, 55 VERIFIED, 17 foreign. Gap 2 adds Singapore s. 15; gap 7's IMDA
examples are replaced by Utah 13-77-102 and Moffatt paras 27 and 28; gap 12 adds roaming Art 14(4) and AI Act
Art 14(4)(e) with its caveat. Report: row 12 and row 2 cells, the three counts; still 5 pages. Replay pages and viewer:
each flagged gap shows its line, one example from elsewhere and a register link.

## Corrections to the order (Iyas, 2026-10-30)

1. **Report row 7.** The report's gap table has no row 7 (out since Task 25 at least). Left without one; gap 7 is in
   the register and on the site with Utah and Moffatt. The row 7 cell test became
   `test_report_has_no_row_7_gap_7_stays_in_the_register`.
2. **"Elsewhere" rule.** The order said the first global example; gap 1's first is IMDA 2.2.2 and its first binding
   one is DSA Art 12(1), while the order expects Spain. Rule now: the example marked `"elsewhere": true` in
   `gaps.json`, else the first whose document is binding in the manifest, else the first. Markers match the report's
   cells: gap 1 Spain Art 8(2), gap 3 eIDAS Art 8(1) (its stored text exists and its quote passes the word-for-word
   check), gap 10 Wales Standard 15. `gaps.json` not reordered.
3. **S2 step number.** The order says S2 step 3; gap 1 is flagged at S2 step 5 (S2-5) in the viewer and in
   `docs/replay/S2.md`. Step 3 holds no abstention. Screenshot taken at step 5.

## Outside the order

1. **`says` printed.** `docs/gaps.md` and `docs/site/gaps.html` now print an example's `says` before its quote; only
   the AI Act entry has one. Without it the caveat would sit in the data unseen (accepted by Iyas).
2. **Short labels.** `onyx/gaps.py` gained four table labels (Singapore ETA, Utah Code, Moffatt v. Air Canada 2024
   BCCRT 149, EU Roaming Reg 2022/612), as Task 30 did.
3. **Viewer quote markup.** The "Elsewhere" quote uses `<q class="elsewhere">`, not the chunk-quote class: the viewer
   test requires every chunk quote to be in `kb/chunks/`, and register quotes live in `kb/sources/global/`.
4. **Spanish quote.** The order says the quote in English; gap 1's Spain quote is Spanish, the stored text, with no
   official English version.
5. **Apostrophes.** Moffatt's site prints curly apostrophes, the read file straight ones; the stored text and quotes
   keep the site's (accepted by Iyas).
6. **Schema.** `binding_status` gains `decision` for Moffatt, as the order allows.

## Sources

| document_id | route | HTTP | bytes | sha256 |
|---|---|---|---|---|
| sg-eta-2010-s15 | sso.agc.gov.sg, scrapling, network idle, 10 s; "Current version as at 30 Oct 2026" | 200 | 695 | 6b4f70b8... |
| us-utah-13-77-102 | le.utah.gov PDF, curl, pdftotext -layout | 200 | 638 | 55bb3659... |
| ca-bccrt-2024-149-moffatt | decisions.civilresolutionbc.ca iframe view, scrapling | 200 | 6,768 | 83f7b6e9... |
| eu-roaming-2022-612-art14 | EUR-Lex CELEX 32022R0612, scrapling, 8 s | 200 | 9,375 | 65797bd9... |
| eu-ai-act-2026-07-27-art14-26 | EUR-Lex CELEX 02024R1689-20260727, scrapling, 8 s | 200 | 11,035 | b1c7492a... |

The AI Act caveat checked at EUR-Lex OJ:L_202601744: Regulation (EU) 2026/1744 of 8 July 2026, published 24.7.2026,
Art 1(40)(b): Chapter III Sections 1, 2 and 3 apply from 2 December 2027 (Annex III) and 2 August 2028 (Annex I);
Art 4: in force on the third day after publication.

## Checks

| # | Check | Output |
|---|---|---|
| 1 | `kb verify` | `VERIFIED 55  REFERENCED 1  UNVERIFIED 3  HISTORICAL 0` / `every fetched source matches its sha256`; rows 59, foreign 17 |
| 2 | Quote-in-stored-text, new quotes | `test_task_31_quotes_are_verbatim_in_their_files`: 7 of 7 found; generic verbatim test passes |
| 3 | `check-data` | `check-data ok: every quote verbatim, every rule cites a clause` |
| 4 | Register, replay pages, viewer, site, export, datasheet, intent rebuilt twice | hash `7fffefc5056d5291` both runs |
| 5 | Elsewhere labels | S2-5: gap-1 Spain Ley 10/2025 Art 8(2), gap-8 none found; S3-3: gap-5 GDPR Art 28(3)(a); S5: gap-3 eIDAS Art 8(1); S1: candidate line only |
| 6 | Screenshots, Chrome | `docs/site/screenshots/replay-S2-step5-elsewhere.png`, `replay-S3-step3-elsewhere.png` |
| 7 | Report | count check ok; `scripts/report_pages.ps1`: `pages: 5`, `words: 2226` (row 2 addition kept) |
| 8 | hq copy | `docs/report.md` sha256 6c075adc... equals `report-draft-2026-10-23.md`; previous kept as `.bak-2026-10-30-task-31` |
| 9 | Limits | `git diff refs/tags/task-30 -- onyx/gate.py onyx/data/rules.json onyx/data/keys onyx/data/mandates.json onyx/eval.py runs/ onyx/model.py onyx/prompts`: empty |
| 10 | Full suite | `581 passed` |
| 11 | CI on `task-31` | run 41071603129 on d24801c `success`: "568 passed, 13 skipped" (the 13 read the gitignored `kb/sources/`) |

Not checked: the subscriber-facing replies are unchanged by construction (render code reads no log field it did not
before); the replay tests confirm every log replays as recorded.

## Open questions for hq

1. Gap 3's report cell leads with eIDAS, which has a stored text but no manifest row (nor does COPPA, gap 9). Add
   manifest rows for both, or leave them as register-only texts?
2. Gap 1's register lists four IMDA examples and the DSA before Spain; the report leads with Spain. Reorder at the
   next register edit?
