# Report-back: task-8 live order, Part B, the bake-off (2026-10-21)

For hq, `D:\Projects\hq\uni\ai-for-good-hackathon\`. Order: `docs/work-orders/2026-10-21-task-8-live.md`, item 6 to 8. Part C not started: waits for hq.

## Summary

The bake-off ran: 10 governed runs each for claude-opus-5-5, claude-sonnet-5-5 and claude-haiku-5-5, committed with responses under `runs/bakeoff/<model id>/`. Table: `eval/bakeoff.md`. **hq's rule stops at its last clause: Opus fails the JSON row in Arabic (20 of 26 replies) and the quote row (1 of 5).** No model chosen; hq decides whether Fable 5.1 is tried.

The cause is not Opus's JSON. Every one of its 38 failed replies (18 en, 20 ar) ends with `finish_reason: content_filter`: 23 empty, 15 cut mid-sentence in ordinary consumer-care text (for example S2-3-care stops at "a service the subscriber did not expressly order or opt to p"). Sonnet and Haiku: 0 of 52 each stopped. Same key, endpoint, prompts and retrieval for all three.

## Headline rows (en / ar; full table in eval/bakeoff.md)

| Row | Opus 5.5 | Sonnet 5.5 | Haiku 5.5 |
|---|---|---|---|
| JSON parse failures | 18 of 26 / 20 of 26 | 0 / 0 | 0 / 0 |
| Stopped by endpoint (content_filter) | 18 / 20 | 0 / 0 | 0 / 0 |
| Quote failures | 0 of 12 / 1 of 5 | 0 of 23 / 0 of 13 | 1 of 30 / 1 of 19 |
| Action recall | 0.29 / 0.10 | 0.43 / 0.17 | 0.47 / 0.32 |
| Obligation proxy | 0.10 / 0.04 | 0.17 / 0.23 | 0.17 / 0.16 |
| Arabic vs English agreement | 0.28 | 0.33 | 0.33 |
| Cost USD (10 runs) | 0.91 | 0.63 | 0.04 |

Gap recall is 0.00 for all three: no model named a key's gap id. Worth a look before Part C.

## Evidence

- 30 runs plus 3 partial logs in `runs/bakeoff/_failed/` (kept, counted in spend): `verify-log` 33 ok; `replay` 30 of 30 match.
- `bakeoff` writes the same bytes twice. Full suite 176 passed; check-data ok; `selftest` chain ok, replay matches.
- Spend recorded in the logs: USD 1.63 of the USD 15 stop. Opus never needed more than the USD 5 run cap; the USD 8 allowance was not used.

## Where the build departs from the order

1. Fix: the gate crashed when a proposal's `args.deadline` was free text ("three business days from 2026-10-19", Haiku and Sonnet, S5 step 6). Now blocked with a reason, like a wrong deadline value; no existing verdict changed (scripted eval byte-identical).
2. Fix: a dropped connection (SSL EOF) killed Haiku's first attempt. The adapter now retries a dropped connection or HTTP 429/5xx/529 up to 4 times; `record --skip-existing` resumes without overwriting.
3. Added `python -m onyx selftest` (main order, Task 10 wording), as hq asked; it reads `eval/scripted/results.json` until `eval/results.json` exists.
4. The table compares every row with a direction. Not compared: gate rejection rate (no better direction), tokens, calls.

## Merge danger and blast radius

Two-way door. New modules `bakeoff.py` and `selftest.py`; the gate change only touches a case that used to crash; the adapter retry adds waits, never extra billed calls on success.

## Open for hq

- Opus is stopped by the endpoint's content filter on 73% of calls. Options: Fable 5.1 per the rule, Sonnet (clean on JSON and quotes; behind Opus only on model_ms median, 7.0 s against 5.7 s in English, and Opus's figure is lowered by its short filtered replies), or asking Anthropic about the filter. hq's call.
- Gap recall 0 across models: the prompt never names gap ids, so a model cannot match the key's ids.
