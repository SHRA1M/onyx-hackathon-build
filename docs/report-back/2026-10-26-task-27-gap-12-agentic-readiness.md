# Task 27 report-back: gap-12 agent authority, ITU-T Y.3173 in the KB (2026-10-26)

Order: `docs/work-orders/2026-10-26-task-27-gap-12-agentic-readiness.md`. hq rulings: `task-27-stop-ruling-2026-10-26.md`,
`task-27-stop-2-ruling-2026-10-26.md`, `task-27-stop-3-ruling-2026-10-26.md`. Base main at d8284eb, branch `task-27`.
No model call, USD 0.

## What was built

- Part A: ITU-T Y.3173 in the KB. sha256 `63f65c25...94dd` as A1 (HTTP 200, 832,240 bytes, 34 pages). Manifest
  51 rows: 47 VERIFIED, 1 REFERENCED, 3 UNVERIFIED. `kb/chunks/itu-t-y3173.jsonl` holds the 5 cited clauses (3.2.1, 6.1,
  7.2, 8.2, 9), lines copied from `kb/chunks-full`; no other chunk file changed.
- Part B: register row gap-12 "No metric for where an agent's authority ends" (standards, ITU) in `onyx/data/gaps.json`,
  with the Y.3173 clauses in `searched`, SAE J3016 L3 via Table I.1 as the global example, the B4 note. `docs/gaps.md`,
  the README table and `docs/site/gaps.html` regenerated.
- Readiness 2.0 cited as framework, nine entries, not chunked.
- Appendix I.1 cited through chunk 9.
- Part C: report row 12, then hq's cuts to get back to 5 pages.

## The report, step by step (Word, `scripts/report_pages.ps1`, rebuilt and recounted after each)

| Step | Pages | Words |
|---|---|---|
| Row 12 in (stop 2) | 6 | 2,300 |
| F1 row 12 shortened, two "51 documents" | 6 | 2,285 |
| F2 row 2, F3 row 1 (stop 3) | 6 | 2,274 |
| T1 "47 are verified", T2 "Y.3172, Y.3173 and" | 6 | 2,275 |
| G1 gap intro addressee sentence | 6 | 2,265 |
| G2 `replay` clause | 6 | 2,256 |
| G3 coordinator clause | 6 | 2,246 |
| G4 synthetic operator sentence | 6 | 2,239 |
| G5 "written from the binding texts" | 6 | 2,234 |
| G6 Gap 10 sentence joins the recommendations paragraph | **5** | **2,234** |

G7 not needed. The report diff against d8284eb holds F1 to F3, the two "51"s, T1, T2 and G1 to G6 only;
`git diff d8284eb -- docs/report.md | grep -E '^[-+].*\[C[35]'` prints nothing.

## Quote spellings that differ from the order

- Y.3173 3.2.1: "automation capabil ities" (pypdf spacing in the chunk).
- Readiness p. 29: "accountabil- ity" (extractor's hyphen).
- Pages are printed pages; Table I.1 is printed pages 12 to 13 (PDF pages 18 to 19).

## Departures from the order, each already reported at a stop

- `onyx/gaps.py`: a `SHORT` label for the Y.3173 file and an optional `note` printed under "Exposed by" (B4's sentence).
- `onyx/site.py` prints the `note` too (stop 2, question 3, hq yes).
- Tests updated where they pinned old counts or text; four gap-12 tests and one site note test added.
- README outside the table: "Twelve rows", "47 VERIFIED", "(51 rows".
- `kb/local-sources.json` (Y.3173 text and splitter) and `kb/export/InputDocs/Inputs.md` (regenerated);
  `docs/site/index.html` changed with the manifest counts.
- The Adviser's prompt register gains line 12; logs carry only `v5`, replay and eval unchanged.
- "51 documents" twice in the report (stop 2, question 2, hq yes); T1 and T2 from the stop 3 ruling.

## Left out

Nothing in the order. Readiness 2.0 is not chunked and the splitter is not taught appendices, as ruled.

## Time

Four sessions on 2026-10-26, three stops for hq. Not timed more closely.

## Open for hq

- Counts checked against the manifest this session: 51 documents, 47 VERIFIED, 3 UNVERIFIED ("three unpublished").
  The other numbers in the stop 3 trap list (fifteen, nine, 107 of 112, 222, 156) are untouched by this task and
  were not rechecked; eval recomputed with an empty diff.

## Merge and CI

Merged to main without squash (bb48d42), pushed. CI green: run 40320563219 on main, run 40320540518 on `task-27`.
