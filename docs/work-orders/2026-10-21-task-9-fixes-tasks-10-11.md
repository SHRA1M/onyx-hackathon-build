# Order: Task 9 fixes, then Tasks 10 and 11 (hq, Fable, 2026-10-21, after the Task 9 check)

Build model: Opus 5.5. No model calls; USD 0. Copy this file into `docs/work-orders/` first.
hq checked Task 9 at bafd4a3 (tests, check-data, regeneration, the 10 promoted chunks, all 16 global quotes against
the originals and a fresh eur-lex fetch) and accepted it. Report-back items 1, 2, 3 and 6 stand as built. This order
rules on items 4 and 5 and the prompt label, then moves to Tasks 10 and 11 of the master order
(`docs/work-orders/2026-10-17-onyx-mizan.md`) with its addenda.

## Sources allowed, and nothing else

- UAE clauses: `kb/chunks/` and `kb/chunks-full/` only, by chunk id. A clause not in the KB is not cited.
- Global texts: `kb/sources/global/` as they are. Nothing is fetched in this order.
- The master order and its addenda; the Task 9 order; `docs/sources/` (hq notes).

## Part A: Task 9 fixes (same day)

1. **gap-7 rewrite.** `line` stays (it is a key string). `gap` becomes, word for word:
   "No binding UAE text sets conduct standards for an AI agent dealing with a consumer. The clauses that name AI or an
   automated agent set a charge waiver (CPR 25.14.1), a bar (26.7.2), a definition (Spam Calls v4 3.3(iii)), a
   permission (Cabinet 56/2024 5(6)) and a tool (Child Digital Safety 10(1)(g)); PDPL 18 and Electronic Transactions
   11 to 13 govern automated decisions and contracts as outcomes, not the agent's conduct."
   `category` becomes `standards gap` (a reader of "technology gap" thinks the technology is missing; it is not).
   Add searched rows for `pdpl-45-2021-en:18(4)`, `etransactions-46-2021-en:12(2)`, `etransactions-46-2021-en:13` and
   `cabinet-57-2024-en:7` (all exist in `kb/chunks-full/`; `11(2)` is already searched under gap-6, cite it here too),
   each with a one-line "what it says" written from the chunk text. If a chunk does not say what the report-back
   claimed, leave that row out and say so in the report-back. Rewrite the UAE position line to match the new `gap`
   text; the recommendation stands.
2. **Competitor column out of the public outputs.** `docs/gaps.md` (table and the per-row line) and the README table
   drop "competitor has it". The fields stay in `gaps.json` (hq's internal note). A test asserts that the word
   "competitor" appears in neither generated file. Reason: the register is public at submission and leads the README;
   a rival-tracking column is not for the judge's first screen.
3. **Prompt label.** `PROMPT_VERSION = "v4.1"` in `onyx/agents/base.py`, with one docstring line: "v4.1 (Task 9,
   unscored): the adviser's register lists gap-8 and the candidate at line 9; kb_main grew from 106 chunks with the
   Task 9 searched clauses (and again with item 1 above). Recorded runs are v4 and replay as recorded." `eval` output
   for the recorded runs must still read v4. If a test pins "v4" for new runs, the test changes, not the label.
4. **README limits line.** State that the verbatim check of global quotes runs offline against the fetched texts
   (`kb/sources/global/`, not committed, addendum item 15), while CI checks every UAE quote against the committed
   chunks and the register's structure. One sentence, no apology.
5. Full suite, check-data, `python -m onyx gaps` byte-identical on a second run, eval twice byte-identical and
   unchanged. Commit, push.

## Part B: Tasks 10 and 11 (by 2026-10-26)

Follow the master order's Task 10 and Task 11 checklists and these addendum items: 1 (VERIFIED / REFERENCED / METHOD
counts on the README's first screen), 2 (tests: no portal URLs, no summaries, every rule has a clause id), 7 (gaps and
the counts on the first screen), 16 and 17 (Y.3172 table with all seven nodes; an unmapped cell is written as a
finding, never left blank), 18 (selftest checks that figures match). Specifics:

6. **Judge quickstart.** A "two-minute check" block at the top of the README, after the register: clone, `uv sync`,
   `python -m onyx selftest` (no key), `python -m onyx replay runs/S2/<run>.jsonl` (the hand-over step, both
   languages), `pytest -q`. Every command in the block is run by a test (or by CI) so it cannot rot.
7. **Replay page, text.** `python -m onyx replay-page` writes `docs/replay/S1.md` to `S5.md` from one recorded
   governed run each: the steps in order, each proposal, the gate's verdict, the clause ids with their quotes, and at
   every hand-over or abstention both language quotes. Byte-identical on a second run; a test checks it. No HTML.
8. **CI.** `.github/workflows/reproduce.yml` runs, on push: `pytest`, `check-data`, `kb verify`, `verify-log` on every
   committed run log, `replay` of one run per scenario, `eval`, `gaps`, `replay-page`, then `git diff --exit-code`.
   Badge in the README. No secret is needed; if one turns out to be, stop and ask.
9. **KB export.** `python -m onyx kb export` output committed under `kb/export/`, ITU InputDocs layout, with a direct
   document link (the manifest URL) per record. README links it as "the knowledge base, downloadable".
10. **README team line.** "Team Onyx (BAU Faculty of AI): Iyas Shraim, leader, and three members" until hq confirms
    the other spellings. No contact details in the README (public repo); they go in the report's title line.
11. Full suite, CI green on the private repo, eval twice byte-identical. Commit, push. Report under 30 lines to
    `docs/report-back/2026-10-2X-tasks-10-11.md`: what runs in CI, the quickstart commands with their timings, what
    the sources did not support, anything that departs from this order.

## Stop and ask when

- Any change to keys, `rules.json`, `mandates.json` or the eval would be needed.
- A manifest URL is a portal page rather than a document, or a record's text is a summary.
- CI needs a secret, or a step needs a model call.
- A quickstart command takes longer than 60 seconds offline.
