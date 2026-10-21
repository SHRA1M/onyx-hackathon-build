# Report back: keys session, 2026-10-21 (Fable)

For `D:\Projects\hq\uni\ai-for-good-hackathon`. Order: `docs/work-orders/2026-10-17-onyx-mizan.md`, Task 3 (scenarios, answer keys) and the flagged mandate clauses. Brought forward from 2026-10-23.

## Summary

Task 3 complete. Five scenarios (`onyx/data/scenarios/S1..S5.json`, English and Arabic steps, facts only) and five frozen keys (`onyx/data/keys/S1..S5.json`, `HASHES.txt`). Every clause a key cites is a rules.json row whose quote is verbatim in a committed chunk. Every flagged mandate clause checked: one changed, three widened, the rest confirmed.

## Evidence

check-data ok (107 rules, 16 verbs, 40 manifest rows); pytest 31 passed, 0 skipped (the keys test now runs); `sha256sum -c HASHES.txt`: five OK; reversed lam-alef scan of the scenario Arabic: clean.

## Differs from the order

- Gap numbering: keys use the Task 9 register order (gap-1 complaint hand-over, gap-2 consent and channel, gap-3 verification, gap-4 disconnection review, gap-5 model provider, gap-6 AI disclosure, gap-7 five mentions). The order's Task 7 line for S2 says "gap 2" in the research numbering.
- 13 rules added beyond the Task 3 list so the keys can cite them (CPR 2.1.7, 26.4.5, 26.11, 4.9, 13.4, 13.8, 5.3, 4.22.4, 4.17.1, 4.23.2, 3.9 notices; PDPL 23(2); licence 9.3). Task 6 names most of them as gate clauses.
- S3 step 4 (minimum de-identified payload to the model provider) is scored as the order's design rule, not as a PDPL 22 exemption; the key states that.
- Decision 16/2026 4.19 ("free") is never cited: no checked text.

## Decisions taken

- `tdra.order_restore` cites CPR 26.11 (direct restoration) with licence 9.3 second.
- One abstention step per scenario: S1 step 6 (is an expired fixed-term bundle a 4.4 renewal), S2 step 5 (how fast must an app chatbot hand over), S3 step 3 (PDPL 22 adequacy; the hard block with no override), S4 step 5 (deadline for the 18(4) review), S5 step 4 (what adequate verification is).
- The model-provider export is the demo's hard block; the human override attempt at S3 step 3 is refused and logged by name (addendum 17).

## Open questions for hq

1. S1 step 6 produces a new candidate gap row (CPR 4.4 and an expired fixed-term bundle). Does it enter the register, and under which `kind`?
2. S2 step 3: the design acknowledges the complaint immediately although 26.13.3 allows one business day for a written complaint. Keep as design, or score only the one-business-day rule?
3. `kb chunk` drops the licence document on a rebuild (splitter stops at 1.1.7 on the hq .txt). Was the hq licence text re-extracted after the 2026-10-21 chunk commit?

## Merge danger

Two-way door except the keys: once `HASHES.txt` is committed the keys are frozen and the commit hash goes in the report. Blast radius: this repo only; no deploys.
