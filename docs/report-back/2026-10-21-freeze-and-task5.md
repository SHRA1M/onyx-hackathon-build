# Report back: keys freeze and Task 5, 2026-10-21 (Opus)

For `D:\Projects\hq\uni\ai-for-good-hackathon`. Orders: `freeze-order-2026-10-21.md`, `freeze-order-2026-10-21-part2.md`, then order Task 5 (`docs/work-orders/2026-10-17-onyx-mizan.md`).

## Summary

The freeze is applied and pushed (e8b17cb); the keys carry the hq answers to both 2026-10-21 report-backs. Task 5 is built (07416f4): model adapter with replay and mock, five agents, mandate-scoped retrieval, verbs outside the mandate rejected before the gate, channel classification in plain code. One question blocks Task 6: what each agent may retrieve.

## Evidence

- Freeze: `grep -c "34(3)\|34-3" onyx/data/keys/S4.json` = 0; check-data ok; pytest 41 passed; HASHES.txt re-hashed in the same commit.
- PNG checks of CPR 24.7 (page 60) and the 3.9 table (PDF page 12) sent to hq; both 3.9 quotes match, not changed.
- Task 5: tests written first (failed on import), then code. Suite 52 passed; check-data ok. MockModel run of S1 steps 1 and 2: `classify_channel` logged with 4.22, 4.10, 4.11; care's `order_restore` logged as `reject_proposal`; `verify-log` true. No real model call.

## Where the build departs from or fills the orders

1. Freeze step 2: the 22(1) chunk came from `kb chunk` reading the hq extractions (the repo's documented route). The rebuild re-broke licence 3.4.1 and 9.1, so that file kept its committed text plus the two 'the' in 9.3.
2. pdpl-22-1's unspecified fields copied its neighbours: verb `condition` (as pdpl-22), language_note as pdpl-17.
3. CHANGELOG says three quote fixes (the commit holds three; the instruction said five).
4. Task 5, channel classification is plain code, from the plan's "The checks (plain code, not AI judgement)". App chat carries 4.11 as well as the order's 4.22 and 4.10 (key S1 step 1, strict reading); business centre maps to 4.15 (the clause's own words, in the mandate).
5. Task 5, an agent's "mandate's document set" is read as every document its mandate verbs cite in `mandates.json`. No hq source defines it.
6. Clause ids in proposals are chunk ids (`tdra-cpr-v2-en:4.22`), the id the agent saw; keys cite rules.json ids, so eval maps chunk to rule.

## Open questions for the plan

1. **Each agent's document set (blocks Task 6).** Under reading 5, care retrieves only the CPR, the 2026 licence and Cabinet 66/2023, so it cannot cite Electronic Transactions 11(2), which key S1 step 3 requires; the gate would then hold for want of a retrieved clause. hq: a list per agent, or a rule (for example: the mandate's documents plus every document a rule names for that agent's verbs).
2. S2 steps 3 and 4 share verb draft_reply (from the blind review; not in the freeze).
3. The order's Task 6 `disconnection_gate` line names 66/2023 34(3); the keys now use 34(1). Build the gate on 34(1)?

## Merge danger

Two-way door: Task 5 is new code behind small interfaces; the document-set rule is one function (`Agent.documents_of`). The freeze is one-way by design (hashed keys).
