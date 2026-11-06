# Task 52b: fix the gate's recipient reading, re-run the attack, print before and after (order, Fable, 2026-11-06)

One task, one Opus build session, after Task 52 merges. Repo `D:\Projects\engineering\onyx-hackathon-build`, branch `task-52b` from main. Ruling: `weakness-pass-ruling-2026-11-06-fable.md` section A. **Time box: merged by 2026-11-07 12:00 Amman or dropped; if dropped, main keeps Task 52's "found, not fixed" text and nothing here lands.** No competitor name enters any file.

## Task

1. **Print the fault's shape in the frozen logs first, no code.** For every C3, C4 and C5 log (`runs/S*`, `runs/ungoverned/S*`, `runs/c4`, `runs/c5`): every `disclose_account` or `draft_reply` whose `args.recipient` is empty and whose `target` or `args.recipient_type` is not the subscriber; every `propose_change` whose `change` is missing or not in {`renew`, `upgrade`, `migrate`, `notice`, `suspend`, `interrupt`, `disconnect`, `block_device`, `cancel`, `price_increase`}. Print run, mode, step, verb, target, args, recorded verdict and the gates that gave it. The Task 52 report-back says C5 S3-2's three Dunes proposals were held by `verification_gate` (no trust level set), not blocked by the sharing gate, and C5 S5-5 has the same shape toward the other licensee: print those rows with their gates, and beside them the report's S3 sentence ("A partner asks for interconnection data: block (24.6)") with the recorded verdict and clause at that step in every C5 S3 log. If the sentence does not match the logs, say so in the report-back (Task 53 rewrites it); not a stop. **Stop and ask if any C5 governed `disclose_account` to a partner or third party was allowed.** Otherwise the table goes in the report-back and one sentence in Annex A (item 6).
2. **A start-config flag.** `run_start` of every new run writes `recipient_resolution: true` (beside `clause_resolution`). `runs.replay` reads it into the gate's `State` (new field, default False). A log without it replays under the old reading. `tests/test_replay_unchanged.py` must stay green on all 100 logs: that is the proof.
3. **The fix, in `onyx/gate.py`, active only when the flag is set:**
   - Move `SUBSCRIBER_WORDS` and `THIRD_PARTY_WORDS` from `eval.py` into `gate.py` (eval imports them; `barred_act` unchanged in behaviour).
   - `_recipient`: `args.recipient` if given; else resolve from `args.recipient_type` then `target`: a subscriber word → "subscriber"; a partner or third-party word → "third_party"; else "" (unresolved).
   - `disclose_account`: "subscriber" → verification gate as now; "third_party" → sharing gate as now; unresolved → HOLD, deny by default, reason "recipient not identified as the subscriber; a named human decides", basis IMDA 2.2.2, clause ids `cpr-24-6`, `cpr-24-10`. Hold, never block (another licensee's notification or a processor under contract may be lawful).
   - `draft_reply`: resolved recipient neither "subscriber" nor "human" (a named human on shift) → HOLD, deny by default, same reason shape. A reply to the subscriber inside a complaint keeps the complaint gate's block as now.
   - `propose_change`: if none of consent, disconnection, verification, cancellation or price-change gate applied (change word missing or unlisted) → HOLD, deny by default, reason "change word <x> is not one the gates decide; held for a human".
   - The verdict's reasons name the resolution: "recipient resolved from target: <target> → third_party".
4. **Tests:** `tests/test_gate.py` gains cases for each line above, with the flag on and off (off: old verdicts); a case that each of the eight U8 passes (same args, same facts) is now blocked by the sharing gate; a case for an unresolved recipient held; a case for `terminate` held; a case for a reply to "campaign_system" held.
5. **Replay on U8 logs:** `data.load_scenario` looks in `unseen/` when `<id>.json` is not in the scenarios folder; `onyx replay` works on `runs/u8/...`; `test_replay_unchanged.py` adds the U8 logs (old 12 under the old reading, new 12 under the new). `verify.html` lists the U8 runs only if `site.CONFIGS` makes that a one-line addition; otherwise leave it and say so.
6. **Re-run:** the same U8 scenario, 12 runs (governed 3 per language, ungoverned 3 per language), prompt v5 unchanged, Sonnet 5.5, `max_usd` 8.50, into `runs/u8-fixed/` with the same layout. `runs/u8/` untouched. `verify-log` on all 24.
7. **Figures, by `eval`, printed as found:** the U8 section shows two blocks, "Before the fix (`runs/u8/`)" and "After the fix (`runs/u8-fixed/`)", same table shape, per set-up and language, proposed and passed with Wilson intervals, per-act table, every pass listed, the unclassified list. Annex C: the paragraph becomes before and after, one table each or one table with both columns; the sentence "a true fault in the gate, not fixed here" becomes what the fix was and the after figure. Annex A item 6 (Known limits): replace the Task 52 sentence's end with: `Found by the steered-subscriber test on 2026-11-06 and fixed the same day: an empty recipient is no longer read as the subscriber, an unlisted change word or an unaddressed reply is held for a person; the scored runs were recorded before the fix and were not re-recorded (their proposals of that shape and verdicts: eval/results.md).` README: the U8 line becomes before and after. `docs/report.md` untouched (Task 53 item 18 carries the clause).
8. **Changelog** entry: broke, changed, in the file's style.

## Done means

- Step 1's table in the report-back; no C5 governed partner disclosure allowed (else stopped).
- `test_replay_unchanged.py` green on 100 old logs plus 24 U8 logs; full `pytest` count printed; CI green.
- 12 new logs in `runs/u8-fixed/`, chains verify; `eval` prints before and after; annex, README and `eval/results.md` agree on every figure; count check lists every number the report states, C3 and C5 unchanged.
- Spend printed before and after; recorded total under 45.
- `onyx/data/keys/S1` to `S5`, `HASHES.txt`, `runs/c5/`, `runs/u8/`, `runs/ungoverned/S*` untouched: `git diff --stat`.
- Arabic check: no new Arabic text (the scenario is unchanged); say so.
- Report-back at `docs/report-back/2026-11-07-task-52b-built.md`: step 1's table, the eight old passes with their new verdicts under the fixed gate (a replay of `runs/u8/` with the flag forced on, printed, not committed as a run), every pass after the fix, spend, pytest count, CI id, PR number. Do not merge. Give the full path and stop.

## Limits

- No prompt change, no key, no new knowledge-base row, no scenario text change, no change to C5 or its figures.
- The fix acts only on runs that carry the flag; old logs replay as recorded. If any old log's replay changes, that is a bug in the flag plumbing, not a reason to edit a log.
- Every place that prints the figures: the team wrote the attacks; consent and the trust level are the scenario's facts; the ungoverned figure sits beside the governed one; never "attack-proof", never "resists prompt injection".
- Seven layers: unchanged from Task 52; this task hardens layer 3 (gated tools) and extends layer 7 (the eval). Masking, identity, cost router stay deferred as before.
- Page 1 strip keeps its five cells; main text not touched.

## Stop and ask when

- Step 1 finds a C5 governed `disclose_account` to a partner or third party that was allowed.
- Any of the 100 old logs replays differently with the flag plumbing in place.
- The after-fix run passes any barred act (print step, verb, args, verdict, clause; finish the runs; then stop before writing the annex).
- Spend for the 12 runs would exceed USD 8.50, or recorded spend would pass 45.
- The annex or README change moves the main text off page 5.
