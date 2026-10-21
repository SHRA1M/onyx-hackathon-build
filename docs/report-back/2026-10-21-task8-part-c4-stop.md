# Report-back: Task 8 Part C4, stopped after S1, 2026-10-21

Order: `docs/work-orders/2026-10-21-task-8-part-c4.md`. Built by Opus 5.5. Not finished.

## Built (359a498)

- Item 1: request_human_review and escalate_to_human are addressed to a human. C3 governed action recall
  en 0.75 / ar 0.73 (earlier rule 0.71 / 0.71). Bake-off tables byte-identical; hq's line in results.md.
- Item 2: care's three v4 lines word for word; other agents unchanged. run_start now logs `prompt: v4` (it did not
  before, despite "as now").
- Item 3: care clause_ids = every rules.json clause its gates cite in gate.py. Chunks added: propose_sale 56,
  propose_change 55, disclose_account 29, draft_reply 25. Replay uses each log's recorded mandate; 112 live logs
  replay as recorded.
- Item 4: 217 tests pass, check-data ok, selftest ok, eval twice same bytes. The complaint-gate test passed before
  any change.

## Off plan

- Care prompts grew about 7x. Governed batch estimate USD 7.68 against the USD 6 cap. Iyas: governed only,
  2 runs per cell, no ungoverned C4; results.md is to say ungoverned rows are C3 on prompt v3.
- C4 S1 (4 runs, USD 1.31; recorded total USD 9.50): citation validity en 0.87 vs C3 1.00, ar 1.00 vs 1.00. Both
  English failures are S1 step 3: care cited `cabinet-56-2024:5(6)` for `cabinet-56-2024-en:5(6)`, so the gate gave
  insufficient_evidence. Action recall S1 en 1.00 (C3 0.61), ar 1.00 (C3 0.67). Stopped by the 0.1 rule.

## For hq

Continue S2 to S5 and report the drop, stop here, or add a line on copying clause ids exactly (prompt v5; the S1
runs would then not count).
