# Report back: agent document sets and Task 6, 2026-10-21 (Opus)

For `D:\Projects\hq\uni\ai-for-good-hackathon`. Order: `task-6-order-2026-10-21.md` (Part A, addendum 27; Part B, Task 6 with addenda 16 and 17).

## Summary

Part A done (13c02c6): each agent's `documents` list in `mandates.json`, exactly the order's ids (adviser written out, 40); `documents_of` reads it and fails loudly on an id outside the manifest. Part B done (4adbebb): `onyx/gate.py`, every order gate, ungoverned mode, the named override. No key, rules.json or HASHES.txt change was needed. Task 7 not started.

## Evidence

- Part A: both new tests failed first (17 citations outside the old sets; the coordinator's IMDA exception missing), then passed. Unknown id: `raised: care: documents not in kb/manifest.csv: no-such-doc`.
- Part B: tests first (failed on import). Full suite `102 passed`; `check-data ok: every quote verbatim, every rule cites a clause`; `git diff` on keys, rules.json and HASHES.txt empty.
- On the 19 key steps the gate tests use, every governed verdict equals the frozen key (gate_outcome where the agent abstains); allow_all allows each. S2 step 3: block on cpr-2-1-7, 26.7.2, licence 9.1, 26.13.2, 26.13.3 written, 26.7.1, with 26.7.2 quoted in English and Arabic and the hand-over, reference and IVR-moment obligations.
- must_cite coverage: full on 18 of 19; S4 step 5 has 2 of 6 (the rest is the adviser's list of clauses searched, Task 7).
- Override: a hold released by Human agent H-03 logs `override_release` with that actor and reason; an attempt by H-02 on the S3 model-provider block logs `override_refused` and the block stands.

## Where the build departs from or fills the order

1. Telecom Law 72(2), named in `model_provider_gate`, has no rules.json row and no chunk; this order forbids editing rules.json, so the gate does not cite it.
2. `disconnection_gate` cites Cabinet 66/2023 34(1), not the order's 34(3): the frozen keys cite 34(1), and the text of 34(3) is about conformity, not termination.
3. price_change, cancellation and child gates have no scenario step (all subscribers are adults); their tests use synthetic states on S1's subscriber.
4. Verdict mapping the order left open: no gate for the verb, or no reachable human: hold. Verb outside the mandate, inject not released, deadline not equal to rules.json: block. Bad quote, unretrieved or non-VERIFIED chunk: insufficient_evidence. Only a hold can be overridden.
5. Gates read the scenario files' own fact names; proposals state what they want in `args` (change, recipient, payload, outbound, price_aed). S2 steps 3 and 4 (both draft_reply) are told apart by `recipient`.
6. Two gate checks added from the keys' own obligations: the model-provider block also states that 23(1)(a), 8(1) and 13(2)(d),(g) do not make an approved case (S3 step 3); a human review states that 18(4) is unconditional and contract term 14.2 is no escape (18(1), 18(2), 34(1); S4 step 4).
7. Global design-basis quotes are verbatim from the hq standards-text files (IMDA 2.2.2 'Denying action by default when approval infrastructures fail'; EU AI Act 50(1); GDPR 22(3)).

## Open questions for the plan

1. Telecom Law 72(2): add a row and chunk, or drop it from the gate line?
2. Is the verdict mapping in item 4 what hq wants judges to see?

## Merge danger

Two-way door: the gate is new code behind one function; the document sets are data. Blast radius: Task 7 must produce the gate's State and args vocabulary.
