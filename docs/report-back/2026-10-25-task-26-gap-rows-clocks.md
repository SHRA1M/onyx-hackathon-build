# Report-back: Task 26, rows 1 and 2 pre-empt the CPR clocks and PDPL 4(9) (2026-10-26)

Order: `docs/work-orders/2026-10-25-task-26-gap-rows-clocks.md`. Ruling on the stop:
`D:\Projects\hq\uni\ai-for-good-hackathon\task-26-stop-ruling-2026-10-26.md`. Base: main at 746c2bd. Branch `task-26`.
USD 0, no model call.

## Summary

Register gaps 1 and 2 reworded as A1 and A2; 13 searched entries added (gap-1 +6, gap-2 +1, gap-4 +2, gap-10 +2,
gap-11 +2); report rows 1, 2 and 5 reworded as B1 to B3. Report: **5 pages, 2,222 words** (Word,
`scripts/report_pages.ps1`). Cuts: none.

`kb/chunks` grew from 144 to 151 records, all 7 copied from `chunks-full`; the recorded runs were made before the
addition and are unchanged.

## The stop and the ruling

The build stopped before writing: `tests/test_gaps.py` checks every searched clause against `kb/chunks`, 7 clauses
were only in `chunks-full`, and `11(1)(b)` and `12(4)(c)` were not chunk ids. hq ruled: copy the 7 chunks byte for
byte; cite the parent chunks `pdpl-45-2021-en:11(1)` and `etransactions-46-2021-en:12(4)`, each `says` naming the
sub-paragraph, the quote the sub-paragraph's words. (The ruling says "7 of the 18 new entries"; the order adds 13.)

## Evidence (done means)

1. `git diff --stat 746c2bd` lists the order's files plus the 3 chunk files (ruling item 1) and `tests/test_gaps.py`
   (see Departures).
2. Searched counts before and after: gap-1 8 to 14 (+6), gap-2 8 to 9 (+1), gap-4 9 to 11 (+2), gap-10 9 to 11 (+2),
   gap-11 10 to 12 (+2). Fields changed: gap-1 and gap-2 `gap`, `uae_position`; no other field of any row; candidates
   unchanged. Every added entry has exactly `clause`, `says`, `quote`; every existing entry unchanged and in order.
   `docs/gaps.md` carries no count line: its table holds 11 gap rows and 2 candidate rows, as at base; the count line
   is README line 53, "Eleven rows", unchanged.
3. Each added quote verbatim in `kb/chunks-full/<document_id>.jsonl` (clause, file, chunk):
   - gap-1 `tdra-cpr-v2-en:26.2`, `26.6`, `26.13.2`, `26.13.3`, `26.14.1`, `26.14.2`: `kb/chunks-full/tdra-cpr-v2-en.jsonl`, chunk of the same id
   - gap-2 `pdpl-45-2021-en:4(9)`: `kb/chunks-full/pdpl-45-2021-en.jsonl`, chunk `4(9)`
   - gap-4 `pdpl-45-2021-en:11(1)` (sub-paragraph (b)), `12(2)`: `kb/chunks-full/pdpl-45-2021-en.jsonl`, chunks `11(1)`, `12(2)`
   - gap-10 `tdra-cpr-v2-en:26.2`, `26.6`: `kb/chunks-full/tdra-cpr-v2-en.jsonl`
   - gap-11 `etransactions-46-2021-en:12(4)` (sub-paragraph (c)), `13(5)`: `kb/chunks-full/etransactions-46-2021-en.jsonl`
   All 13 `verbatim=True`.
5. `git diff 746c2bd -- onyx/gate.py onyx/data/rules.json onyx/data/keys onyx/data/scenarios onyx/data/mandates.json
   onyx/eval.py runs/` prints nothing. `git diff --numstat 746c2bd -- kb/`: `2 0` etransactions, `3 0` pdpl,
   `2 0` tdra-cpr; each of the 7 added records compared to its `chunks-full` twin: identical (byte comparison).
   Two existing CPR records, 4.7.3 and 24.7, already differ from the local `chunks-full` by the 2026-10-21 hyphen
   fix (CHANGELOG, "opt-out", "anti-competitive"); they stay as committed.
4. Report diff: the three rows B1, B2, B3 and nothing else; the `[C3`/`[C5` grep prints nothing.
6. `eval` and `eval --runs runs/scripted` recomputed: `git diff -- eval/` prints nothing.
7. Pages 5, words 2,222; cuts none.
9. `pytest`: 406 passed. kb verify 46 VERIFIED; check-data ok; selftest figures match; 217 logs chain ok; replay,
   replay-page, figures, report and site rebuilt; only the listed files changed.

B5: `docs/site/gaps.html` shows "the transfer has none" (gap 1) and "consents to nothing beyond it" (gap 2). The D row
of the mapping table (`docs/report.md` line 62, "CPR 26.13.2, 26.13.3; QoS v3.0 T1(2a)") is unchanged.

## A4: the manifest on gap 5

`kb/manifest.csv` row `pdpl-executive-regulations` ("PDPL Executive Regulations (Art 28 of Federal Decree-Law
45/2021)", UAE Cabinet): status UNVERIFIED, source type unpublished, notes "Not issued as of 2026-10-17. Absence is
evidence." No manifest row records a search for the Article 22 country list (the only Art 22 row, `gdpr-art22`, is
GDPR Art 22). No row added.

## Departures from the order

- `tests/test_gaps.py` changed, not in check 1's list: `test_gap_10_searches_the_orders_clauses` (Task 20) pins
  gap-10's searched list, so A5 failed it; the list gains the two A5 clauses. Two tests added for Task 26 (placement
  and fields of the 13 entries, the A1 and A2 wording).
- Arabic: the order asks for Arabic where the gap's existing entries carry it. No entry holds an Arabic field; the
  Arabic shown in `docs/gaps.md` comes from the chunk's `text_ar`. CPR 26.2 and 26.14.1 carry it; the PDPL and ET
  chunks carry none, like every committed PDPL and ET chunk. Nothing added by hand.

## Open questions for hq

- None from this build.
