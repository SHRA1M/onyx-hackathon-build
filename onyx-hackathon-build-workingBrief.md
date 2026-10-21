# Working brief: onyx-hackathon-build

Updated 2026-10-21 (eighth wrap, Opus).

## Objective

Task 8 live runs: three runs per scenario per mode per language with Claude (claude-opus-5-5 through Anthropic's OpenAI-compatible endpoint), then `eval/results.md` from them.

## Next moves, in order

1. Iyas: copy `.env.example` to `.env` and fill the three values (key never in chat).
2. Opus: `python -m onyx record --source live`, then `python -m onyx eval --runs runs --out eval`; check chains and replays; commit `eval: results from runs/` with the responses; report.
3. hq: read report-back `2026-10-21-pending-and-task8` (addressee rule, obligation recall, hand-over latency, `decide_pending`).
4. Then Task 9 on a new hq order only.

## Open questions

- Cost: about 312 calls, estimate $20 to $40; Iyas's go is in the task-8 order once the key is in.
- Iyas: read the Arabic step text of S1 to S5 on a page.
- `/setup-matt-pocock-skills` not yet run by Iyas.
