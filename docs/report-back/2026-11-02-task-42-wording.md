# Report-back: Task 42, "never issued" wording and one stale count (2026-11-02, Opus)

Order: `D:\Projects\hq\uni\ai-for-good-hackathon\task-42-wording-order-2026-11-02.md`. Branch `task-36`, PR #13.

## What was built

- Gap-4 and gap-5 `uae_position`, the PDPL 23(2) rule `value`, the `pdpl-executive-regulations` manifest note:
  replaced word for word as the order wrote them.
- README line 30: "22 rows link a landing page".
- Regenerated: `docs/gaps.md`, README register, `kb/DATASHEET.md`, export, `docs/site/`.
- New test `test_no_live_output_says_never_issued`; `test_gap_5_records_the_portal_check` updated.

## Where it differs from the order, and why

1. Item 4 not done: `onyx/data/keys/S4.json` keeps its committed bytes (stop 1, hq answer 1a). Its hash is in 228
   recorded runs; editing it makes `eval` exit 1. The grader reads the key's gap id (`"gaps": ["gap-4"]`) and counts
   obligations by number (`onyx/eval.py:376`), never the `gap_row` text, so no score depends on it. The new test and
   check 1 skip `onyx/data/keys/`.
2. One phrase added (stop 2, hq answer 1): manifest row `pdpl-45-2021-en` ended "Executive Regulations (Art 28) not
   issued." and now ends "Executive Regulations (Art 28) not on the official portal (checked 2026-11-02)."
3. Check 1 allows `kb/chunks/` (verbatim law text, Decree-Law 46/2021 Art 12(4), stop 1 answer 2). Its other
   unlisted hits are in `tests/`: the search patterns themselves.
4. Item 8: a new test, not an extension of the two existing patterns, which cover only Annex F and gaps 13 to 15.
5. Items 7 and 9: `docs/report.md` and `docs/annex.md` held none of the old words, so the report, PDF and hq copies
   were not changed.

## Checks

pytest 686 passed. Gaps 15, candidates 2. `eval` (live and scripted) results.json byte-identical before and after
and equal to the committed `eval/results.json`; key hashes match: yes. PDF 12 pages, Annex A from page 6. CI: see
`gh pr checks 13` after the push.

## Open for hq

- The S4 key still says "were never issued" in a frozen file. If the report or annex ever quotes the key text,
  it would need a note; today neither does.
