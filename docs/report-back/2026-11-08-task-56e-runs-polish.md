# Report-back: Task 56e, the runs page, judge-first polish (2026-11-08)

Order: `D:\Projects\hq\uni\ai-for-good-hackathon\task-56e-present-15s-order-2026-11-08.md`, with Fable's corrections and its two addenda. Branch `task-56`, PR #26, not merged, not pushed.

Commits:
- Part A (words): `609ab22`
- Part B (behaviour): `c61b599`

The two stops before Part A are in `docs/report-back/2026-11-08-task-56e-runs-polish-interim.md` (committed in `609ab22`).

## In plain words

The runs page now opens on the scenario cards only. Present plays one scenario every 15 seconds and Stop returns to the cards. Each answer label opens to one plain sentence that matches the number of laws the gate listed, then the gate's own reason, then the laws behind a second toggle. The gates-off fold has a clear name and an opening line. The unseen stories moved to a new "More tests" page. The model-down page now reads like a scenario, with its own Present button.

## Checks (done means)

1. After Part A: `uv run pytest -q` 1195 passed; `python -m onyx selftest` exit 0, last line "figures match a fresh eval of runs/".
2. After Part B: `uv run pytest -q` 1198 passed; selftest exit 0, same last line.
3. Pins moved to the new words:
   - Part A: `tests/test_task_56c.py` (SECS 12 to 15); `tests/test_report.py` (the side note names the fold "What happened here with the gates off"); `tests/test_replay_viewer.py` (the "Gate on" line now sits inside the fold as `p.gate-line`, not as the summary).
   - Part B: `tests/test_site.py` (nine pages, More tests after Runs); `tests/test_task_51.py` and `tests/test_task_56c.py` (the unseen boxes are read from `tests.html`).
   - New: `tests/test_task_56e.py`, 7 tests. Written after the code, not test-first.
4. Words lost (`docs/report-back/task-56e-shots/words-lost-part-a.txt`, `words-lost-part-b.txt`):
   - Part A, runs.html and docs/replay/index.html each: "Without the gates" (56 folds plus the side note), the gates-off "allow" pills (72) and "Nothing stopped it." (46), "12", and the old words of the two "sales channel" lines. All replaced labels.
   - Part B: runs.html loses 180 words, all inside the moved section; that section is on `tests.html` byte for byte (script output: "True"; words lost outside it: 0). Every other page: 0.
5. Screenshots, `docs/report-back/task-56e-shots/`, light, 1280 x 720 and 390: `runs-onload-*`, `present-S1-step3-held-*`, `gates-off-S3-step3-*`, `tests-*`, `modeldown-present-step1-*` and `-step3-*`.
6. Browser checks: `docs/report-back/task-56e-shots/checks.txt`, 31 of 31 PASS (Playwright, Chromium).

## Item 5: every link to a scenario or step

No link anywhere (report, annex, README, site pages, the replay page) points at a scenario or a step: none carries a `#` anchor into the runs page. The links into the page, each checked in the browser (checks.txt):

1. The top-bar "Runs" link on each of the eight other site pages: opens runs.html on the cards. 8 PASS.
2. The overview's "Runs" card: opens runs.html on the cards. PASS.
3. `docs/report.md` line 72 names `docs/replay/index.html`: it opens on the cards. PASS.
4. The "Verify this log" buttons on the runs page (out, to verify.html#<log>): open the right log. PASS.
5. With scripts off: runs.html shows 56 of 56 steps, modeldown.html 6 of 6, docs/replay/index.html all. PASS.

## Label count (Fable's second addendum)

The ten runs shown, by label and by N (laws the verdict lists):

| Label | N = 0 | N = 1 | N = 2 or more | With laws |
| --- | --- | --- | --- | --- |
| Allowed | 23 | 6 | 14 | 20 |
| Held for a staff member | 2 | 0 | 17 | 17 |
| Blocked | 3 | 0 | 7 | 7 |
| Not enough evidence | 7 | 0 | 0 | 0 |

These match the interim table (Allowed 20 and 23, Held 17 and 2, Blocked 7 and 3).

"The gate's reason is below" is true on every label that says it: the gate's logged reasons show under the sentence, as logged. 8 allowed labels (N 1 or more) log only obligations, no check. Their sentence ("The law(s) it rests on ...") does not mention a reason, and their obligations show as logged.

## Item 6: sentences the move makes untrue (for hq; not edited)

1. `README.md` line 131: "Open `docs/site/index.html` from disk: eight pages, no server, no network, no key." The site now has nine pages.

Nothing in `README.md`, `docs/report.md`, `docs/annex.md` or the site says the unseen scenarios are shown on the runs page.

## Decisions taken

1. Item 2: the channels come from `CHANNELS` in `onyx/agents/adviser.py` (business_centre, voice, app_chat, web) as "business centre, phone call, app chat or website".
2. Item 5: clicking a card's title opens that scenario at step 1 with Previous and Next, without playing. I read that as the order's "Previous / Next on a card". Present plays. Stop presenting (or Escape) returns to the cards. Key p with no scenario open presents S1.
3. Item 5: in Present, the scenario's title and story box show on step 1 only.
4. Item 7: the model-down story and step lines are on `modeldown.html`. The runs page keeps its Model down and What-if cards as before; they open their text sections, not steps. The page's old table and notes stay under the new part, hidden only during Present. The old heading stays as an h2.
5. Item 7: step 3 in model-down shows the logged `model_unavailable` reason as the care agent's turn, as logged. There is no gates-off fold there: no gates-off run was replayed.
6. Part B fixes a Part A fault: the label's small arrow was written into the CSS as a control character. Part A's commit `609ab22` carries it.

## Every new sentence

Part A:
- S1 step 1: "The coordinator (plain code) tells the adviser a chat has opened and asks where the customer is talking (business centre, phone call, app chat or website)."
- S2 step 1: "The coordinator (plain code) tells the adviser a chat has opened and asks where the customer is talking (business centre, phone call, app chat or website), for sales and for complaints."
- Labels: the sentences of item 3 and both addenda, word for word (`replay_viewer.LEADS`, `TAILS`, `NO_EVIDENCE`). Toggle: "Show the N laws" / "Show the 1 law".
- Fold: "What happened here with the gates off"; "We ran the same conversation again with the gates switched off. This is what went through at this step, with nothing checking it."; per step: "Nothing checked this. It went ahead."
- Side line: "Play the steps by themselves, every 15 seconds: press Present on a scenario card, or key p."

Part B:
- Runs page: "Seven stories not run yet, and the attack test: More tests."
- Top bar and tests.html heading: "More tests".
- modeldown.html title: "The AI fails in the middle of a conversation".
- Story box: "This is scenario 2, replayed from its log with no new AI call. At step 3, where the customer complains about a charge, we made the AI call fail: it failed after 4 tries. The coordinator, which is plain code, wrote a hand-over to a named staff member, and the gate held it for that person. The rest of the conversation then ran as recorded: 7 of 8 later decisions stayed the same. No live outage was run." Sources: the model-down replay log (4 attempts, escalate_to_human held), `modeldown.stays` (7 of 8), `docs/annex.md` line 93. "Complains about a charge" is S2 step 3's own text.
- Step 3 line, added after the S2 line: "Here the AI call fails after 4 tries, and the coordinator (plain code) writes a hand-over to a staff member instead."
- Card: "Model down", "Click Present to start it".

## Not done

- Not pushed. PR #26 gets both commits on the next push, which waits for Iyas's go.
- No CHANGELOG entry: this is not a fix, the same as Task 56c.
- The screenshot folder is not committed, the same as Task 56c's.

## Open for hq

1. README line 131 ("eight pages").
2. The screen clips are re-recorded after this task (the order's note for hq).
