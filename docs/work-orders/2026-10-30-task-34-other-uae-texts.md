# Work order: Task 34, "other UAE texts" (2026-10-30)

Model: Opus 5.5. Repo: `D:\Projects\engineering\onyx-hackathon-build`. Branch `task-34` from `main` (c4102b7).
Decided by hq (uni). Build this order; do not re-decide it.

## Task

1. `docs/report.md` lines 23-24: replace "twenty-seven other UAE laws, resolutions and TDRA instruments" with
   "twenty-seven other UAE texts". The phrase spans a line break; touch nothing else in the sentence.
2. `docs/build_report.py` line 298: widen the `uae_other` pattern so it matches "other UAE texts" (and still
   matches "other UAE laws"), e.g. `other\s+UAE\s+(?:laws|texts)`.
3. `tests/test_report.py` line 357: assert "twenty-seven other UAE texts" instead of "twenty-seven other UAE laws".
4. Regenerate the report pages the way Task 33 did. CHANGELOG line for Task 34.
5. Copy `docs/report.md` byte for byte to `D:\Projects\hq\uni\ai-for-good-hackathon\report-draft-2026-10-23.md`,
   after backing the old one up as `report-draft-2026-10-23.md.bak-2026-10-30-task-34`.

## Done means (show each output in the report-back)

- `grep -rn "other UAE laws" docs/report.md` returns nothing; `grep -n "other UAE texts" docs/report.md` returns one line.
- Count check passes: report 27, manifest 27 (uae_other).
- 5-page check: report is 5 pages (it was 5 before; the change only shortens).
- Full suite passes (607 or more), CI green on the PR.
- `cmp` (or SHA-256) of repo `docs/report.md` and the hq draft: equal.
- Report-back at `docs/report-back/2026-10-30-task-34-other-uae-texts.md`.

## Limits

- No other wording changes, no KB rows, no new sources. Sources rule: nothing is fetched or cited for this task.
- Do not merge the PR or tag until Iyas says so.

## Stop and ask when

- The report goes over 5 pages, or any count other than uae_other changes.
- Any test other than the one in step 3 fails.
- The hq draft differs from repo `docs/report.md` before your copy in anything other than this phrase.
