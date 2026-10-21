# Working brief: onyx-hackathon-build

Updated 2026-10-21 (tenth wrap, Opus).

## Objective

Task-8 live order (`docs/work-orders/2026-10-21-task-8-live.md`): Parts A and B done (d3a4cb2, 6ac1a21). Part B stopped by hq's rule: Opus 5.5 fails JSON and quotes in Arabic, all from the endpoint's content filter. Part C waits for hq's model decision.

## Next moves, in order

1. hq: read report-back `2026-10-21-task8-bakeoff` (and the earlier `pending-and-task8`, `task8-live-part-a`); decide the model: Fable 5.1, Sonnet 5.5, or ask Anthropic about the filter. A Fable try is a new bake-off folder `runs/bakeoff/claude-fable-5-1/` and needs a price row first.
2. Opus: Part C on the chosen model, `eval/results.md`, README "Model" section. Set `--max-usd` from the bake-off's measured cost per run.
3. hq: gap recall is 0 for every model (prompt never names gap ids): decide whether that changes before Part C.

## Open questions

- Part C cost: Opus measured about USD 0.09 per run (understated by cut replies), Sonnet 0.06; 60 runs. Total stays under USD 15; USD 1.63 spent.
- Iyas: read the Arabic step text of S1 to S5 on a page.
- `/setup-matt-pocock-skills` not yet run by Iyas.
