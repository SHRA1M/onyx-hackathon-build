# Working brief: onyx-hackathon-build

Updated 2026-10-21 (eleventh wrap, Opus).

## Objective

Task 8 Part C order (`docs/work-orders/2026-10-21-task-8-part-c.md`): C1 done (a8f4acb), C2 done (0e5f8a6). C3, the scored Sonnet run and the README "Model" section, waits for Iyas's go.

## Next moves, in order

1. On Iyas's go, C3 item 11: Sonnet (already in `.env`), prompt v2, `record --source live` into `runs/` (both modes, both languages, 3 runs each, 60 runs). Cap USD 6; measured about USD 0.086 per run, about USD 5.1. The guard under-estimates v2, so run one scenario at a time with a spend check between (as C2 did). Then `eval --runs runs --out eval`. Stop and report if any row is more than 0.1 below the v2 bake-off.
2. C3 item 12: README "Model" section (live order item 10 wording), bake-off v1 and v2 tables, the Opus finding paragraph (field name, run ids `runs/opus-filter-v2/S2/run1.jsonl` and `.../ar/run1.jsonl`), the UAE-hosted-models sentence, no claim that such a run happened.
3. Report under 25 lines, report-back file, wait.

## Open questions

- hq: Arabic gap recall 0.00 on v2 for both models; the Opus finding caveat (v2 changed more than the field name); the order's "five candidate ids" (only one exists).
- Candidate-id mismatch waits for Task 9 (Iyas).
- Iyas: read the Arabic step text of S1 to S5 on a page.
- `/setup-matt-pocock-skills` not yet run by Iyas.
