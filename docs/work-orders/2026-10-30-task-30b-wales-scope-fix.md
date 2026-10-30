# Task 30b: fix the Wales scope citation (written 2026-10-30, hq uni, Opus)

Repo: `D:\Projects\engineering\onyx-hackathon-build`, branch `task-30` (PR #5, still open). Build on Opus.
Same branch, same PR. Iyas merges and tags after this.

## Why

Gap 10's note says Wales's Standards "bind public bodies under a compliance notice (reg 2(1)(b)), not operators".
hq read regulation 2 at the primary today: reg 2(1)(b) only says Schedule 1 Part 2 links some standards to
others. The rule that limits who can be given a compliance notice is **regulation 3(1)**:

> "The Welsh Ministers authorise the Welsh Language Commissioner to give a compliance notice to the Welsh
> Ministers, to county councils, to county borough councils and to National Park authorities requiring them to
> comply with any of the standards specified under regulation 2."

Source: https://www.legislation.gov.uk/wsi/2015/996/regulation/3/made (data.xml at the same path + `/data.xml`).

## Task

1. Fetch regulation 3 as made from legislation.gov.uk (the data.xml route if the page blocks curl). Add its text to
   the stored Welsh Standards document (append reg 3 above Schedule 1, marked as such), recompute its hash, update
   the manifest. Same document, so the KB stays 54 documents, 50 verified, 12 foreign.
2. In `onyx/data/gaps.json` gap-10 `note` and `docs/gaps.md` line 397: change `reg 2(1)(b)` to `reg 3(1)`. Keep
   the rest of the sentence. If the note quotes, quote reg 3(1) word for word as above.
3. Update `tests/test_gaps.py:454` to expect `reg 3(1)`, and add the reg 3(1) sentence to the quote-found-in-stored-
   text check.
4. Gap 10's recommendation keeps naming Canada (hq decision 2026-10-30: both examples are held, no change before
   the freeze).
5. Append a short "Task 30b" section to `docs/report-back/2026-10-30-task-30-global-examples.md`.

## Done means

- `kb verify`: VERIFIED 50, REFERENCED 1, UNVERIFIED 3, all hashes match.
- The reg 3(1) sentence is found word for word in the stored text (show the check output).
- `grep -rn "2(1)(b)"` over `onyx/`, `docs/gaps.md`, `tests/` returns nothing.
- Full test suite passes; CI green on PR #5; report still 5 pages.
- Committed and pushed on `task-30`.

## Limits

No change to gates, keys, runs, prompts or eval. No other gap rows. No report text change unless the report quotes
reg 2(1)(b) (hq found none). USD 0 model spend.

## Stop and ask when

- legislation.gov.uk text differs from the quote above.
- The KB counts would change.
- The report page count moves off 5.
