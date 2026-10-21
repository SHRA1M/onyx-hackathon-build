# Working brief: onyx-hackathon-build

Updated 2026-10-21 (thirteenth wrap, Opus).

## Objective

Finish Task 8 Part C4 (`docs/work-orders/2026-10-21-task-8-part-c4.md`). Items 1 to 4 done (359a498). The run is governed only, 2 runs per scenario and language (Iyas). It stopped after S1 on the 0.1 rule (17a1f14).

## Next moves, in order

1. Get hq's decision on `docs/report-back/2026-10-21-task8-part-c4-stop.md`: continue S2 to S5, stop, or a v5 prompt line.
2. If continuing: `ONYX_MODEL=claude-sonnet-5-5 uv run python -u -m onyx record --source live --root runs/c4 --scenarios S2 --runs 2 --modes governed --max-usd 6.00`, one scenario at a time; after each, check spend (C4 under USD 6.00, total under 14.50) and citation validity per scenario and language against C3.
3. Add Iyas's wording to the C4 section of `eval/results.md` (2 runs per cell; ungoverned rows are C3 on prompt v3), regenerate eval, write report-back `2026-10-21-task8-part-c4.md`, push with Iyas's go.

## Open questions

- hq: the C4 S1 stop (above); S4 Arabic and S3 English citation misses (report-back c3).
- Iyas: read the Arabic step text of S1 to S5 on a page. `/setup-matt-pocock-skills` not yet run.
