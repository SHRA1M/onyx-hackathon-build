# Work order: Task 34, the report's last text changes before the freeze (2026-10-30, hq on Fable)

Model: Opus 5.5. Repo: `D:\Projects\engineering\onyx-hackathon-build`. Branch `task-34` from `main` (c4102b7).
Decided by hq. Build this order; do not re-decide it. Why now and not on 2026-11-08: the report has no slack (row 8
lost "TS" to hold 5 pages), so every text change that needs a page fit happens before the freeze, not on the last day.

## Task

**A. Report text (`docs/report.md`), then regenerate the pages the Task 33 way.**
1. Lines 23-24: "twenty-seven other UAE laws, resolutions and TDRA instruments" → "twenty-seven other UAE texts"
   (the phrase spans a line break; touch nothing else in the sentence). If Part C adds UAE rows, the number moves
   with the count check.
2. Line 4: "**Team members:** Mohammed Rawashdeh, Yanal Faouri" (Zaid Saaydeh out; team settled 2026-10-28).
3. Line 6 becomes a labelled link list, one line each, this order and wording:
   - **Code:** https://github.com/SHRA1M/onyx-hackathon-build (public from 2026-11-09)
   - **Knowledge base:** https://github.com/SHRA1M/onyx-hackathon-build/blob/main/kb/manifest.csv (what it holds: `kb/DATASHEET.md`)
   - **Demo video:** https://github.com/SHRA1M/onyx-hackathon-build/blob/main/docs/video/mizan-demo.mp4 (the file lands 2026-11-08)
   - **Replay site, no install:** https://shra1m.github.io/onyx-hackathon-build/site/
   The site URL assumes GitHub Pages served from the `main` branch, folder `/docs` (Pages offers root or `/docs`,
   not `docs/site/`; with `/docs` the replay index is also served at `/replay/`). Enabling Pages waits for the repo
   to go public on 2026-11-09; the submission-day order checks the URL GitHub shows before the email goes.
4. Page fit. If Word says 6 pages after 1-3, cut in this order, one at a time, recount after each, stop at 5:
   (a) gap 12 row: delete " (Table 7-2 NOTE 1 gives a human's order the highest authority; it never requires the
   system to ask)"; (b) gap 1 row: delete "; du's code names a chatbot channel and sets no hand-over rule";
   (c) Introduction: delete "It is scored in both languages, because the texts are published in both. ".
   Register, README and site keep the full text. Still 6 after (c): stop and ask with page and word count.

**B. README.**
5. "Iyas Shraim, leader, and three members" → "Iyas Shraim, leader, Mohammed Rawashdeh and Yanal Faouri".
6. One new line under the Y.3172 mapping table answering Y.3172 clause 9 (security of the pipeline), stating only
   what a test shows: no key in the source tree (a test greps for the provider key pattern and fails on a hit);
   the KB, keys and logs are files the gate reads and never writes except by appending a chained event; the model
   adapter is the only outward call. If any of the three is not already tested, add the test or drop that clause.

**C. KB rows for texts the report cites but the manifest lacks.**
7. eIDAS (Reg. 910/2014, Art 8) and the US COPPA Rule (16 CFR 312.5) are report gap-3 and gap-9 examples with
   stored texts and no manifest rows. Add the rows (VERIFIED, hash of the stored official file, document link not a
   homepage, binding_status as the Task 31 rows set it for foreign texts). Licence 3/2026 (du): add a row only if the
   stored file is TDRA's own and hashes; otherwise leave it and say so. Counts, datasheet, report sentence and the
   count check follow (74 → 76 or 77; "twenty-one foreign" → "twenty-three"). No chunks, no agent data.

**D. Close.** CHANGELOG line; `tests/test_report.py` pins updated to the new phrases and counts; full suite; PR
(do not merge or tag until Iyas says so); copy `docs/report.md` byte for byte to
`D:\Projects\hq\uni\ai-for-good-hackathon\report-draft-2026-10-23.md` after backing the old one up as
`report-draft-2026-10-23.md.bak-2026-10-30-task-34`; report-back `docs/report-back/2026-10-30-task-34-last-text.md`.

## Done means (show each output in the report-back)

- `grep -c "other UAE laws" docs/report.md` = 0; `grep -c "Saaydeh" docs/report.md README.md` = 0.
- The four labelled links present in `docs/report.md`; `scripts/report_pages.ps1` says 5 pages; word count stated.
- Count check passes on every number the report states (not only the ones this task touched).
- `python -m onyx kb verify` counts match the report sentence and the datasheet; the eIDAS and COPPA rows hash.
- Full suite passes (607 or more); CI green on the PR.
- SHA-256 of repo `docs/report.md` equals the hq draft's.
- Which cuts in A4 were taken, if any, and the page count after each.

## Limits

- No other wording changes, no new sources fetched (the three texts are already stored), no chunks, no runs, no
  gate, rule, mandate, prompt, eval or agent file. Seven layers (`engineering/_reference/llm-agents.md`): unchanged
  from Task 33; nothing shipped or deferred by this task.
- Do not merge the PR or tag until Iyas says so.

## Stop and ask when

- 6 pages after cut (c); any count other than the ones named above changes; any test outside `test_report.py`
  and the new key-pattern test fails.
- A stored eIDAS or COPPA file is not the publisher's own document (then no row: say what the file is).
- The hq draft differs from repo `docs/report.md` before your copy in anything other than this task's phrases.
