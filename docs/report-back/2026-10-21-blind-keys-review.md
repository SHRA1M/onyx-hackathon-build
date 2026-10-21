# Report back: blind review of the answer keys, 2026-10-21 (Fable, wrapped on Opus)

For `D:\Projects\hq\uni\ai-for-good-hackathon`. Task from hq (agreed in its session 2026-10-21 that it needs Fable): decide all 28 steps of S1 to S5 from `kb/` and `onyx/data/rules.json` and `mandates.json` only, before opening `onyx/data/keys`, then list every disagreement with the clause id and text. Report only: no file in `onyx/data` or `kb/` changed, no key re-hashed, Task 5 not started.

## Summary

27 of 28 verdicts match the keys. One verdict differs (S1 step 6), one citation is wrong (Cabinet 66/2023 34(3) in S4), and four points of key shape are for hq. No step was "cannot decide": every step's clauses are in `kb/`. Already known items (licence-9-3 'the', cpr-4-7-3 and cpr-24-7 hyphens, cpr-3-9 table quotes, 'hq plan, S2') are not repeated.

## Blind verdicts (written before the keys were opened)

| Scenario | Steps 1 to 6 |
|---|---|
| S1 | allow, allow, hold, hold, allow, hold |
| S2 | allow, allow, block, allow, insufficient_evidence, allow |
| S3 | allow, block, insufficient_evidence (gate: block), allow, block |
| S4 | block, allow, allow, allow, insufficient_evidence |
| S5 | allow, allow, hold, insufficient_evidence, allow, allow |

## Disagreements

1. **S1 step 6: key insufficient_evidence, review hold.** The text decides it without answering whether a lapsed bundle is "extended or renewed", because all three 4.4 terms fail on the facts ("fixed-term, non-recurring per the catalogue"; "new_consent: none"):
   - cpr-4-4-1: "consistent with the terms of the contract for that existing Service" (the contract term is a non-recurring 7 days).
   - cpr-4-4-2: "unquestionably without prejudice to the Subscriber" (a second AED 95 charge without consent is at least open to question).
   - cpr-4-4-3: "unquestionably to the advantage of the Subscriber" (same).
   - cpr-4-4 language_note: "The gate tests the three conditions, not the word 'renewal'."

   Gate outcome is hold either way. hq decides whether S1 keeps this as its abstention step.

2. **S4 steps 1, 4, 5: cabinet-66-2023-34-3 does not fit.** Its text: "Authorising the provider to determine by himself and without referring to the consumer whether the goods or service subject of the contract is in conformity with what is stipulated in the contract". That is about conformity, not a suspend-at-discretion term. Term 14.2 is caught by cabinet-66-2023-34-1: "unilaterally terminate it without referring to the consumer or giving him the right to claim compensation". Step 4's obligation "18(2)(a) is undercut by 66/2023 34(3)" also does not hold: pdpl-18-2 needs automated processing "agreed upon under the contract made between the Data Subject and the Controller", and term 14.2 says nothing about automated processing, so 18(2)(a) is not engaged at all. The order's Task 6 `disconnection_gate` line names 34(3) too. Verdicts unchanged.

## Key-shape points for hq

3. **S3 step 3: "no list in any VERIFIED text" is inaccurate.** `kb/chunks` holds only the PDPL 22 lead-in, but `kb/chunks-full` holds 22(1) as VERIFIED: "The State or Province to which the Personal Data is transferred shall have legislations addressing Personal Data Protection ... The State or the Province shall also have a judicial o regulatory authority imposing appropriate measures against the Controller or the Processor." and 22(2) (a bilateral or multilateral agreement). The abstention stands, because the scenario does not name the country and no Bureau approval is on file; the obligation's wording should say that.
4. **gate_outcome is null on S1 step 6 and S2 step 5.** S3, S4 and S5 abstention steps carry block or hold; the README says the field records what the gate does. S1's obligation says "extension_held", so hold.
5. **mandates.json `data_office.receive_objection` hangs on PDPL 18(1) only** (automated decisions). S3 step 1 is a PDPL 17 objection, and the key rightly cites pdpl-17, cpr-28-26, consumer-law-4-5. Add PDPL 17 to the verb?
6. **S2 steps 3 and 4 both have verb draft_reply** (3 blocked, 4 allowed). Eval's action recall counts the verb; Task 8 must tell the two apart by addressee (subscriber or human), or step 3's verb should be the care reply it blocks.

## Evidence

Blind verdicts written to the session scratchpad before `onyx/data/keys` was read (file `blind-verdicts-2026-10-21.md`, not committed; its content is the table above plus per-step clauses). `git status` clean before the wrap.
