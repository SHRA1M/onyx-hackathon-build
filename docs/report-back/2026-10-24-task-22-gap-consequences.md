# Report-back: Task 22, a consequence in gap rows; the what-if words

Order `docs/work-orders/2026-10-24-task-22-gap-consequences.md` (filed e367548), with Iyas's three answers of 2026-10-24 (in chat) and hq's ruling `task-22-ruling-page-six-2026-10-24.md` (cut C). No model calls, USD 0.

## Built

- Gap table rows 1, 3, 4, 5 and 10: the order's new text, each saying what happens while the gap is open.
- Mapping table, Readiness column: the seven section B edits (PP and SINK unchanged, as ordered).
- Section D: the Introduction and S2 sentences name the replay under a proposed rule as a what-if question for the policymaker.
- Cut C, C1 to C5, in the ruling's words: Limits and next steps, the use-case problem paragraph, Our solution, S3, the Introduction's "It is scored in both languages".
- `docs/report.docx` rebuilt: Word counts 5 pages, 2,224 words.

## Page count, step by step

Counted by Word through `scripts/report_pages.ps1`.

| Build | Pages | Words | Page 6 starts |
|---|---|---|---|
| Order's edits A to D | 6 | 2,371 | "The Cabinet: AI disclosure at first contact (6)." |
| + ladder step 1 (section C sentence removed) | 6 | 2,337 | same |
| + step 2 (row 6 old text) | 6 | 2,325 | same |
| + step 3 (row 7 old text) | 6 | 2,309 | "Limits and next steps." |
| + step 4 (row 8 old text) | 6 | 2,290 | same |
| + step 5 (row 2 old text) | 6 | 2,269 | "Before the final on 2026-12-08: ..." |
| + step 6 (row 9 old text) | 6 | 2,261 | same (57 words, 4 lines on page 6) |
| + cut C (C1 to C5) | 5 | 2,224 | none |

Cut C6 not taken: five pages after C.

## Checks

1. `git diff --stat 6a0aaf7`: see below (the committed result).
2. `git diff 6a0aaf7 -- docs/report.md`: rows 1, 3, 4, 5, 10 new; section B's seven cells; section D's two sentences; cut C's five edits. Section C and rows 2, 6, 7, 8, 9 cut by the ladder (old text).
3. `git diff 6a0aaf7 -- docs/report.md | grep -E '^[-+].*\[C[35]'`: printed nothing.
4. `git diff c5cea32 -- onyx/gate.py onyx/data/rules.json onyx/data/keys onyx/data/mandates.json onyx/eval.py runs/`: printed nothing.
5. Word (`scripts/report_pages.ps1`): 5 pages, 2,224 words.
6. `uv run pytest`: 386 passed. CI: see below.

## Differs from the order

- Section C's anchor was wrapped across two lines in `docs/report.md` ("the other" / "six are not claimed."); treated as found (Iyas, answer 1). The sentence was later removed by ladder step 1.
- No PDF: Tasks 18 and 21 built only the docx and none is tracked (Iyas, answer 2).
- Check 1 lists one more file: the filed order, `docs/work-orders/2026-10-24-task-22-gap-consequences.md`, in its own commit e367548 before the build (Iyas, answer 3).
- Five sentences outside the order's edits were shortened by cut C, as ruled.

## Open questions for hq

- The Readiness 2.0 sentence (section C) and the row 2, 6, 7, 8, 9 consequences are out. Bringing any back needs another cut.
- The use-case problem paragraph now opens "The four acts above": it points back to the Introduction's list. hq may want to check that it still reads right on its own.
- `report-draft-2026-10-23.md` in hq should take the same edits so it stays aligned with `docs/report.md`.
