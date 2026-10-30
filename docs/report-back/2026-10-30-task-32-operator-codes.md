# Report-back: Task 32, the operators' codes, 106/2026 and the CSC policy enter the KB (2026-10-30)

Order: `docs/work-orders/2026-10-30-task-32-operator-codes.md` (hq, Fable, 2026-10-30). Read file:
`perplexity-2026-10-30/uae-recheck-read-2026-10-30-fable.md`. Base: `main` at df903ae (PR #7 merge, tag `task-31`).
Branch `task-32`. Opus 5.5. USD 0.

**Limits:** KB rows, gap `searched` entries, count sentences, report row 1, and the render code for entries that name
their file. No model call, nothing recorded, nothing sent outward, nothing under `runs/`, `onyx/data/keys/` or
`kb/chunks/`, no gate, rule, mandate, eval, model, prompt or agent file changed (check 9). Seven layers
(`engineering/_reference/llm-agents.md`): unchanged from Task 31; nothing shipped or deferred by this task. Owner of
any failure: Iyas.

## Summary

Both operator PDFs fetched from e& and du today; their SHA-256 equal hq's copies. KB 64 documents: 59 VERIFIED, 4
UNVERIFIED, 1 REFERENCED, 17 foreign, 29 UAE instruments. Eleven `searched` entries on gaps 1, 2, 7, 9, 10 and 11, each
quote found word for word in the stored text. Report row 1 names du's chatbot channel; still 5 pages. No chunks, so
`kb_main`, retrieval and every recorded run are untouched.

## Decisions taken with Iyas (2026-10-30)

1. **Searched entries without chunks.** The register test required every `searched` clause to be a committed chunk;
   the order forbids chunks. Iyas: an entry may name its stored file (`file`, and `page` for a PDF); its quote is
   checked word for word against that file. CI skips the check (`kb/sources/` is gitignored), as for global
   examples; it ran locally, 11 of 11 (check 2).
2. **Gap 9.** Its 106/2026 cites were sentences in the prose, not entries, and the Arabic PDF's text layer gives
   presentation forms, so no Arabic quote can be checked. Iyas: two entries under `cabres-106-2026-en`, Art 2 and Art
   4(3), each quote checked against the English text, each `says` ending "Portal: the Arabic text prevails
   (cabres-106-2026-ar); Arabic not quote-checked, PDF text extraction scrambled." Gap 9's sentences unchanged. Both
   quotes passed, so no fallback.

## Outside the order, and why

1. **Schema.** `source_type` has no enum in `kb/manifest.schema.json` (a free string), so `operator code` needed no
   schema change.
2. **Landing mark.** The order's 106/2026 URLs are portal pages; `kb verify` rejects those without
   `landing page: document link not verified`, so both rows carry it. Landing rows 16 to 18 (README, datasheet).
3. **README UNVERIFIED gloss.** "3 UNVERIFIED (asserted, not published; they back no claim)" became "4 UNVERIFIED
   (asserted, not published or not reached; ...)": the CSC policy is published but unreachable. The datasheet's
   generated definition line still says "not published"; left, as generator text.
4. **du §10.** The order gives one `says` for two sentences that are not adjacent; two entries, same `says`.
5. **"Code, never rule or law."** Three of the order's `says` texts do not name the document ("CPR 26.13.3 ...",
   "No deadline ...", "Languages for human care ..."); used as written. Gap 1's Annex 1 text says the code "sets no
   rule"; kept, it does not call the code a rule. The test bars "law", "breach", "break", "violate" in those fields
   and any sentence pairing e&, du, Etisalat or EITC with breach, break, violate or fail in the register, report and
   README.
6. **Capitals.** The order's `says` texts start lower case; first letter capitalised to match the register.
7. **Chatbot quote.** Quoted as the Annex 1 lines "Chatbot WhatsApp 058-2428268 (058Chatbot)" (whitespace
   normalised), not the bare word.
8. **e& §4 apostrophes.** The PDF prints curly apostrophes (customers’, Etisalat’s); the quote keeps them.
9. **hq copy.** `report-draft-2026-10-23.md` replaced from `docs/report.md`; the previous kept as
   `report-draft-2026-10-23.md.bak-2026-10-30-task-32` (Task 31's pattern). The one write outside this repo.

## Sources

| Row | From | SHA-256 | Pages |
|---|---|---|---|
| `eand-code-of-practice-en` | eand.com, HTTP 200, 2026-10-30 | `4b6383a7...` = hq | 13 |
| `du-code-of-practice-en` | du.ae/files/1430740188355, HTTP 200, 2026-10-30 | `8f8014d9...` = hq | 5 |
| `cabres-106-2026-ar` | hq `standards-text/cabinet-resolution-106-2026-children-social-media-ar.pdf` | `18a7068c...` | 7 |
| `cabres-106-2026-en` | hq `standards-text/cabinet-resolution-106-2026-children-social-media-en.txt` | `c589e279...` | |
| `csc-ai-security-policy-v1-1` | not fetched (host unreachable) | | |

`kb fetch --local` accepts the four hq files: each exists at its `kb/local-sources.json` path and matches the
manifest SHA-256 (the condition `fetch` uses). No `csc-ai-security-policy-v1-1.pdf` in hq at start.

## Checks

| # | Check | Output |
|---|---|---|
| 1 | `kb verify` | `VERIFIED 59  REFERENCED 1  UNVERIFIED 4  HISTORICAL 0` / `every fetched source matches its sha256`; 64 rows, 17 foreign, 29 UAE instruments (`test_task_32_rows_have_no_chunks_and_the_counts_are_the_orders`) |
| 1b | Operator SHA-256 vs hq | eand `4b6383a7523a...1d05ddd`, du `8f8014d981c1...8e34d`: download = hq copy = order |
| 2 | Quote-in-stored-text, new entries | `test_task_32_quotes_are_verbatim_in_the_stored_text`: 11 of 11 found (local; CI skips) |
| 3 | `check-data` | `check-data ok: every quote verbatim, every rule cites a clause` (manifest rows 64) |
| 4 | Register, replay pages, site, export, datasheet, intent rebuilt twice | hash `798a78ca6ad3d5d8` both runs; replay pages unchanged |
| 5 | Replay | S1 to S5 `run1.jsonl`: "replay matches the recorded verdicts" (8, 10, 7, 8, 10 decisions); eval and figures: "figures match a fresh eval of runs/" |
| 6 | `verify-log` | 227 of 227 run logs pass (CI's set: `runs/*.jsonl` without `/gaps/`; the 6 `gaps/candidates.jsonl` are not chained logs) |
| 7 | Report | count check ok; `scripts/report_pages.ps1`: `pages: 5`, `words: 2237` (row 1 addition kept) |
| 8 | hq copy | `docs/report.md` sha256 `73d925ba...` equals `report-draft-2026-10-23.md` |
| 9 | Limits | `git diff main -- onyx/gate.py onyx/data/rules.json onyx/data/keys onyx/data/mandates.json onyx/eval.py runs/ onyx/model.py onyx/prompts onyx/agents kb/chunks eval/`: 0 lines |
| 10 | Full suite | `591 passed in 115.62s` |
| 11 | Site, Playwright | `docs/site/gaps.html`: 11 entries render with clause, page, file, says and quote; only console error a favicon 404 from the local test server |
| 12 | CI on the PR | not run: branch not pushed (waits for Iyas's go) |

## Open questions for hq

- The report's "three unpublished texts back no claim" is still true but there are now four UNVERIFIED rows; the
  fourth is unreachable, not unpublished. Left, per "no other report wording changes".
- The datasheet's generated UNVERIFIED definition ("asserted, not published") does not fit the CSC row.
- "fifteen other UAE laws" in the report: left for the submission-day count check, as ordered.

## Merge danger

Two-way door: data and render code only; the new `file` path in the register and site leaves every existing entry's
rendering unchanged (the rebuilt register differs only by the eleven new entries).
