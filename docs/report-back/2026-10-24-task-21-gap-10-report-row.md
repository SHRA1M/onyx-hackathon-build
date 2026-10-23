# Report-back: Task 21, gap 10 in the report's table and recommendations

Order `docs/work-orders/2026-10-24-task-21-gap-10-report-row.md` (filed 96d6388), with hq's two rulings of 2026-10-24 (in chat: keep step 2, skip step 3, take step 4; then `task-21-ruling-page-six-2026-10-24.md` in hq: cut A, cut B). No model calls, USD 0.

## Built

- Gap table row 10, the gap 10 sentence after the table and TDRA recommendation (10), in the ruling's cut A wording (character for character).
- The old "Gap 10: the texts fix" sentence is gone.
- `docs/report.docx` rebuilt: Word counts 5 pages, 2,169 words.

## Page count, step by step

| Build | Pages | Words | Page 6 starts |
|---|---|---|---|
| Order's three edits | 6 | 2,274 | "What ITU can reuse: ..." |
| + ladder step 2 (dropped "The gates, scenarios and keys are offered to TDRA as a test bench ...") | 6 | 2,255 | same |
| + ladder step 4 (dropped "The existing protections stop short of the channel ... (gap 1).") | 6 | 2,199 | same |
| + cut A (row 10, gap 10 sentence, item (10) shortened) | 6 | 2,189 | same |
| + cut B (dropped "Mizan carries this at D as a hand-over with no sink; the standard needs that outcome and its reference point.") | 5 | 2,169 | none |

Ladder step 3 skipped (hq: Figure 2 panel (a) carries the 0.96 and 0.94 figures the gap 10 sentence cites).

## Checks

1. Table rows: 10; row 10 matches the ruling's text.
2. `grep -c "Gap 10: the texts fix" docs/report.md`: 0; new sentence in its place.
3. TDRA list ends "... with a parity band (10)."
4. `git diff --stat`: `docs/report.md`, `docs/report.docx`, `CHANGELOG.md`, plus this report-back.
5. Word: 5 pages, 2,169 words.
6. `git diff c5cea32 -- onyx/gate.py onyx/data/rules.json onyx/data/keys onyx/data/mandates.json onyx/eval.py runs/`: printed nothing.
7. `uv run pytest`: 386 passed. CI: see the commit's run.

## Differs from the order

- Row 10, the gap 10 sentence and item (10) use the ruling's shortened text, not the order's.
- Three report sentences outside the three edits were dropped (steps 2 and 4, cut B), as ruled.

## Open questions for hq

- The use-case section no longer names gaps 1 and 2 (step 4); they now appear first in the gap table. hq may want to check that the problem paragraph still reads as complete.
- `report-draft-2026-10-23.md` in hq should take the same cuts so it stays aligned with `docs/report.md`.
