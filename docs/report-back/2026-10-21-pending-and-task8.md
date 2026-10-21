# Report back: pending proposals and Task 8, 2026-10-21 (Opus)

Order: hq `task-8-order-2026-10-21.md`. Part A complete (d4ec049). Part B built and committed with scripted runs (d85871d); the live runs stopped as the order says: no `.env`, no model key, no call made.

## What was built

- Addendum 29: `pending_proposal` on the five abstention steps, submitted after the abstention, verdict logged under the proposing agent (`S3-3-care`). Gate verdicts equal every key's `gate_outcome`. S3: H-02's override refused and logged with the name. No key changed.
- Task 8: `record` (live or scripted), `replay`, `eval`; `gate_ms` and `model_ms` on every event (addendum 18); 60 scripted runs in `runs/scripted/`, results in `eval/scripted/` labelled SCRIPTED.
- Model (order Task 5 decision): base URL `https://api.anthropic.com/v1/`, model `claude-opus-5-5`, from platform.claude.com/docs/en/cli-sdks-libraries/libraries/openai-sdk via context7. `.env.example` committed.

## Differs from the order, and why

1. `gate.decide_pending` added to the gate (the order named the coordinator only). A pending proposal cites no clause, so `decide` returns insufficient_evidence and never the hold item 29 expects.
2. `OpenAICompatibleModel` no longer sends temperature 0 (the order said "as built"): the doc page says any value below 1 is a 400 on Claude 4.7 and later. It now sends max_tokens 16000. CHANGELOG entry.

## Decisions taken, for hq to confirm

1. Addressee in action recall: the keys have no addressee field. Where the key answers a step sent by a human with draft_reply, the reply must be addressed to the human; every other step a non-human addressee (S2 steps 3 and 4 told apart).
2. Obligation recall: obligations are free text, so it is step-level: the step reached the key's verdict and every must_cite clause is on its record.
3. Hand-over latency: first step from handover_step that is a hold, an allowed proposal to or asking for a human, or a complaint_gate hand-over duty.

## Open

- Live runs and `eval/results.md` wait for the key (about 312 calls, estimate $20 to $40).
