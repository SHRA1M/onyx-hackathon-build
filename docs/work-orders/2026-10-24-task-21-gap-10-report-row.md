# Task 21: gap 10 in the report's gap table and recommendations (2026-10-24)

Repo: `D:\Projects\engineering\onyx-hackathon-build`. Builds on 026d8c2. No model calls, USD 0.

## Task

The report (`docs/report.md`, section "Policy gaps and standards gaps derived from the mapping exercise") lists gaps 1 to 9 in its table and recommendations paragraph. Task 20 added gap 10 to the register and one sentence to the report. Bring gap 10 into the table and the recommendations, replacing the loose sentence.

Three edits, exact text:

1. Append this row to the gap table, after row 9:

```
| 10 | Arabic on an automated channel: the language is set (CPR 3.2.2, Consumer Law 26, 8(4)) and its omission fined (Cabinet 66/2023 Annex 2); nothing requires the Arabic answer to be as good as the English one, and the QoS Policy v3.0 has no indicator per language | standards | TDRA | Canada OLA ss. 22, 26, 27 |
```

2. In the paragraph after the table, replace the two-line sentence that starts `Gap 10: the texts fix the language of service` and ends `is measurable.` with:

```
Gap 10 is measurable: Mizan's own per-language figures (action recall 0.96 English, 0.94 Arabic, C5) are the indicator the QoS Policy lacks.
```

3. In the recommendations paragraph, TDRA list, after `the Art 11 instructions with a caregiver check (9)` and before the full stop, insert:

```
; QoS indicators per language for every automated consumer channel, Arabic and English reported separately with a parity band (10)
```

Then rebuild `report.docx`. If it reaches 6 pages, take one step down the ladder the earlier orders used; report which step.

## Sources

Only `onyx/data/gaps.json` (gap-10 row) and `docs/report.md`. The figures 0.96 and 0.94 are the gap-10 row's `uae_position`. If either figure is not there, stop and ask.

## Done means

- The table has 10 rows; row 10 is the text above, character for character.
- The old "Gap 10: the texts fix" sentence is gone; the new sentence is in its place.
- The TDRA recommendation list ends with item (10).
- No other line in `docs/report.md` changes (`git diff --stat` shows `docs/report.md`, `docs/report.docx`, `CHANGELOG.md` only).
- Report at 5 pages, or the ladder step named.
- `git diff c5cea32 -- onyx/gate.py onyx/data/rules.json onyx/data/keys onyx/data/mandates.json onyx/eval.py runs/` prints nothing.
- Tests pass, CI green, committed and pushed, report-back at `docs/report-back/2026-10-24-task-21-gap-10-report-row.md`.

## Limits

- Touch no file other than the three named. No change to the register, README or `docs/gaps.md`.
- No other entry's name in any tracked file.
- Stop and ask if the table format or the recommendations paragraph differs from what this order quotes.
