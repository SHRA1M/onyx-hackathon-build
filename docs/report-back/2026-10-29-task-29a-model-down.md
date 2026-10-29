# Report-back: Task 29 Part A, model down (2026-10-29)

Order: `docs/work-orders/2026-10-29-task-29-field-take.md`, Part A. Branch `task-29`, commit 44cf73b. Opus 5.5. USD 0.

## Summary

A dead model no longer kills a run. When the model call raises what `OpenAICompatibleModel` raises after its last
attempt, the step's agent logs `model_unavailable`, the coordinator authors an `escalate_to_human` proposal in plain
code, and the gate decides it as a pending proposal (addendum 29). On the recorded S2 run with step 3 failing, the
gate holds and hands the conversation to Human agent H-01 (synthetic), the same human the recorded run reaches at S2-4.

## Evidence

- `uv run pytest`: 522 passed (421 before Part A's new replay test).
- `tests/test_modeldown.py`: 8 passed (the three order tests, the page, the command, viewer, site, README).
- `tests/test_replay_unchanged.py`: 101 passed (20 C5 logs, 80 C3 and C4 logs, one count check).
- `git diff --stat df7c29c -- runs onyx/data/keys`: empty.
- Browser (Playwright, local server): `docs/site/modeldown.html` shows the table and the "No model took part" line;
  the viewer's "Model down: S2, the call at step 3 fails" button opens the page's text beside the what-if button.
- CI: **not run**. The push of `task-29` was blocked in this session; it waits for Iyas's go. No PR yet.

## What differs from the order, and why

1. `test_c5_logs_replay_unchanged` did not exist; the order named it as existing. Written in
   `tests/test_replay_unchanged.py`, over C3 (`runs/S*/`, `runs/ungoverned/`), C4 and C5. Logs under `_failed/` do
   not replay (crashed runs, kept as history) and are outside the test.
2. "Every other decision identical": every verdict outside step 3 is identical. One clause list is not: the S2-5
   abstention lists every clause the gate cited earlier in the case, so the five ids cited only by the recorded
   S2-3 `propose_change` (cpr-22-1-2, cpr-22-3, cpr-22-4, pdpl-21-2-a, cpr-22-2) drop out (19 ids, not 24). The page
   says so; the test pins exactly that difference. Not hidden, not changed.
3. Site: a sibling page `docs/site/modeldown.html` (seventh page, nav "Model down", a card on the index). The
   what-if page is unchanged.
4. CI gains one step: `python -m onyx model-down runs/c5/S2/run1.jsonl --at 3`, so the page is regenerated and diffed.

## Decisions taken

- Attempts in the event: 4 for a connection error or a retried status, 1 for an HTTP status never retried
  (`model.attempts_made`); the retry loop is unchanged.
- The hand-over proposal on a complaint step cites `tdra-cpr-v2-en:26.7.2` and `licence-2-2026:9.1`, quote 26.7.2's
  rules.json words; `args: {"reason": "model unavailable"}`.

## Open question for hq

- The hold's deny-by-default reason, written by `gate.decide_pending`, reads "the adviser answered
  INSUFFICIENT_EVIDENCE on S2-3: no VERIFIED clause permits escalate_to_human". On this path the adviser did not
  answer; the model was down. `gate.py` is outside Part A's files, so it is unchanged. The page and viewer do not
  print reasons, but the replayed log carries it. Change the wording in a later order, or leave it?

## Merge danger

Two-way door. The except path runs only on an exception; every C3, C4 and C5 log replays as recorded.

## The page (`docs/replay/model-down-S2.md`)

    # Model down: S2, the call at step 3 fails
    
    Run `runs/c5/S2/run1.jsonl`; chain ok. Replayed offline from the logged model responses; no model call. The operator, subscriber and numbers are synthetic.
    
    Fault injection: the model call is made to fail at this step; nothing else changes.
    
    ## Step 3 and after
    
    | step | recorded | model-down |
    | --- | --- | --- |
    | S2-3 | care `propose_change`: block (cpr-22-1-1, cpr-22-1-2, cpr-22-3, cpr-22-4, pdpl-21-2-a, cpr-22-2)<br>care `draft_reply`: block (cpr-2-1-7, cpr-26-7-2, licence-9-1, cpr-26-13-2, cpr-26-13-3-written, cpr-26-7-1, licence-9-2-4) | care: `model_unavailable` (URLError, 4 attempts)<br>coordinator `escalate_to_human` to Human agent H-01 (synthetic): hold (licence-9-1, cpr-26-7-2, cpr-2-1-7, cpr-26-13-2, cpr-26-13-3-written, cpr-26-7-1, licence-9-2-4) |
    | S2-4 | care `draft_reply`: hold (cpr-26-7-2, licence-9-1, cpr-4-6, cpr-3-2-2, licence-9-2-4) | care `draft_reply`: hold (cpr-26-7-2, licence-9-1, cpr-4-6, cpr-3-2-2, licence-9-2-4) |
    | S2-5 | adviser `flag_gap`: allow (no clause)<br>adviser `flag_gap`: allow (no clause)<br>adviser `abstain`: insufficient_evidence<br>coordinator `route`: hold (no clause) | adviser `flag_gap`: allow (no clause)<br>adviser `flag_gap`: allow (no clause)<br>adviser `abstain`: insufficient_evidence<br>coordinator `route`: hold (no clause) |
    | S2-6 | tdra `request_report`: allow (licence-9-2-4, cpr-3-9-complaints, cpr-26-14-2) | tdra `request_report`: allow (licence-9-2-4, cpr-3-9-complaints, cpr-26-14-2) |
    
    ## What stays
    
    7 of 8 decisions outside step 3 identical.
    
    S2-5 `abstain` keeps its verdict (insufficient_evidence); its clause list has 19 ids, not 24: cpr-22-1-2, cpr-22-3, cpr-22-4, pdpl-21-2-a, cpr-22-2 dropped out (cited only by step 3's recorded proposals, which no model made here).
    
    No model took part in step 3 of the model-down column.
    
    Generated by `python -m onyx model-down`; the gate, keys and committed runs are unchanged; this page is a fault injection, not a result.
