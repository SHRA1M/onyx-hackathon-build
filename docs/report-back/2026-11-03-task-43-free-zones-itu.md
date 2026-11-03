# Task 43 done: free zones, ITU F-series, the Authority, three "never" phrases (2026-11-03, Opus build session)

Order: `D:\Projects\hq\uni\ai-for-good-hackathon\task-43-free-zones-itu-order-2026-11-02.md`, with the answers to
stops 1, 2 and 3. Branch `task-36`, PR #13.

## What was built

- KB: five texts (DIFC Law 5/2020, DIFC Regulations v2, ADGM DPR 2021, ITU-T F.746.16, ITU-T F.748.67) and the WAM
  page, VERIFIED on the build's own extracts in `kb/sources/global/`. New jurisdiction value `UAE-free-zone`.
- Register: preamble's two paragraphs; every ordered row change, with the stop 1 and stop 2 rewordings.
- Report: table rows 3, 5, 6, 13. Row 5 now ends "the machinery (Art 22 list, 23(2), 8(11)): not on the portal"
  (stop 3, answer b). Annex A and F follow the register.
- Tests: Task 42 pattern gains "has not been issued" (it hits nothing in the test's paths; the one repo hit is
  verbatim UAE law text in `kb/chunks/etransactions-46-2021-en.jsonl`, outside them) plus the three Task 43 phrases;
  free-zone label test; F.746.16 quote test. The old gap-7 note test was updated to stop 2 answer 5's wording.
- hq copies: `report-draft-2026-10-23.md` and `report-annex-2026-11-02.md` replaced, `.bak-2026-11-02-task-43`
  backups beside them. sha256: report 474ecbea...0283 (both copies), annex 85b0f32f...1036 (both copies).

## Done checks

1. `kb verify`: VERIFIED 90, REFERENCED 2, UNVERIFIED 3 (95 rows with WAM), "every fetched source matches its sha256".
2. `pytest`: 697 passed.
3. `gaps`: 15 gaps, 2 candidates. `docs/gaps.md` diff touches only the preamble and gaps 3, 5, 6, 7, 8, 12, 13, 14,
   all named in the order.
4. `git grep -i -E "never mapped|any published UAE text|No binding UAE text"`: hits only `docs/work-orders/`,
   `docs/report-back/`, the archive, and the test's own pattern line in `tests/test_gaps.py:1271`.
5. 12 of 12 free-zone and ITU example quotes found verbatim in their extract; the two preamble quotes, the WAM quote,
   "manual intervention rate" and "average queue duration" found too.
6. `eval` live and scripted: `eval/` byte-identical to committed; "Every run_start carries the current key hashes: yes".
7. Word: main 5 pages, annex starts on page 6, 12 pages. `check_pdf`: 12 pages, "Annex A", "Limits and next steps",
   "Annex F" found.
8. CI on PR #13: see the result below.

## Differs from the order

- Report cell row 3 changed beyond "cells 6 and 13" (stop 2, answer 1). Row 5 changed (stop 2 answer 6, stop 3 b).
- Free-zone rows carry country `UAE`, not `AE`; "compliance voluntary" in place of "both voluntary" (stop 2,
  decisions confirmed).
- LLM layers: no change (the adviser lists id and short line only; no short line changed).

## For hq: gap 12's full wording, as stop 2 answer 3 asked

"...Mapped there, neither text measures when an acting agent must stop or how long the hand-over takes; ITU-T F.746.16
11.2 measures how often (a manual intervention rate, graded so that less intervention scores a higher level, no
threshold), the opposite direction to a regulator's floor such as CPR 26.7.2. Y.3173 Table 7-2 NOTE 1 (p. 7) gives a
human's order the highest authority (...); it never requires the system to ask. Y.3173 cites SAE J3016 and drops its
fallback column, the request to intervene (Appendix I.1, Table I.1, p. 12 to 13)."

Recommendation ends: "...plus the existence of defined stop points, and a floor-direction measure beside F.746.16's
rate: the hand-over required by rule, whether it happened, and its latency."

## Open

- Nothing from the build. hq to judge gap 12's wording above.
