# Working brief: onyx-hackathon-build

Updated 2026-10-21 (seventh wrap, Opus).

## Objective

Task 7: scenarios and the coordinator (staged release, live inject), feeding `gate.decide` a State per step.

## Next moves, in order

1. hq: read report-back `2026-10-21-doc-sets-and-gate` (72(2) not citable; 34(1) used; three gates tested on synthetic states).
2. Opus: Task 7 per the order. The coordinator builds `gate.State` from each step (see `tests/test_gate.py` `_facts`, `_state`) and the args vocabulary in `onyx/gate.py`.
3. Iyas: read the Arabic step text of S1 to S5 on a page (scenarios are not hashed; wording fixes allowed).
4. Then Task 8 (runs, replay, eval; gate_ms and model_ms).

## Open questions

- Telecom Law 72(2): add a rules.json row and chunk, or drop it from model_provider_gate (hq).
- Decision 16/2026 4.19: no checked text; never cited.
- Claude API key: walked through before the first real call; a cost estimate first.
- `/setup-matt-pocock-skills` not yet run by Iyas.
