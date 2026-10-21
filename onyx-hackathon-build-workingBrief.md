# Working brief: onyx-hackathon-build

Updated 2026-10-21 (ninth wrap, Opus).

## Objective

Task-8 live order (`docs/work-orders/2026-10-21-task-8-live.md`): Part A done (d3a4cb2). Next, Part B: the three-model bake-off, then Part C: the scored live runs.

## Next moves, in order

1. Iyas: fill `.env` (`scripts/set-model-key.ps1` from the clipboard, or by hand), key never in chat. Then say go.
2. Opus: bake-off, 10 governed runs per model under `runs/bakeoff/<model id>/` (`record --source live --root ... --modes governed --runs 1`), committed with responses; build `eval/bakeoff.md` with JSON parse failures and quote failures added; apply hq's decision rule; report.
3. Opus: Part C on the chosen model, `eval/results.md`, README "Model" section.
4. hq: read report-backs `2026-10-21-pending-and-task8` and `2026-10-21-task8-live-part-a`.

## Open questions

- Part C cost: once Opus output is measured the run may exceed the $5 default cap; Iyas sets `--max-usd`. Total stays under $15.
- Iyas: read the Arabic step text of S1 to S5 on a page.
- `/setup-matt-pocock-skills` not yet run by Iyas.
