# Task 56c: the site's words (Opus, engineering)

Written by Opus in hq, 2026-11-08 (Iyas's override: Opus writes it; Fable checks all report-backs together at the end). Branch `task-56`, add to PR #26, do not merge.

**Start only when** `git status` in the repo is clean and no other session is working there (order 2, the report text, runs in the same repo). If it is not clean, stop.

## Task

In `D:\Projects\engineering\onyx-hackathon-build`, make the site (`docs/site/`, built by `onyx/site.py` and `onyx/replay_viewer.py`) readable by a judge who is not an engineer. Plain words, short sentences, no em dashes. Every number on the site stays as it is; every new number comes from the source named beside it.

1. **Verify page:** one plain sentence on top: what the page checks (that no line of a run's log was changed after it was written) and how (the hash chain).
2. **What-if page:** a plain story on top, three or four sentences: what was changed, what happened before, what happened after. Then a simple before/after view of the same step (two columns). The existing detail stays below.
3. **Runs page:**
   - Run header: one plain line above the existing meta line, saying which scenario, which language, gates on, and that the log's chain checks out. The meta line stays, smaller.
   - The "Without the gates" line: one plain sentence saying what it counts (actions that went through with the gates off that the law does not allow).
   - The written proposals: one plain note on each scenario's step that carries a `pending_proposal` (S1 step 6, S2 step 5, S3 step 3, S4 step 5, S5 step 4): "This move was written into the test by the team, to check the gate. It was not the AI's idea." Source: `D:\Projects\hq\uni\ai-for-good-hackathon\end-check-2026-11-08-fable.md`, part 9, ruling 6.
   - "The unseen bank" heading becomes "Stories not tested yet", with one sentence: seven scenarios written before the first scored run and never sent to the model.
4. **Local model page:** one plain paragraph on top: the operator chooses the model. The same adapter, prompt, gates and keys run on it; only the endpoint and model name change. Tie it to gap 5 in one sentence: this shows a way around gap 5 (data leaving the country), it does not close it. Label the page's run "demo, not scored".
5. **New section "We tried to trick it"** (on the overview page, after the hero): a customer who pushes Mizan to break the law, eight messages, three runs in English and three in Arabic, 48 tries. Before the fix, 8 of 48 went through, all from one fault (sharing data with an outside company). After the fix, 0 of 48. With the gates off, 48 of 48. Source: `docs/annex.md`, the "Steered subscriber, U8" paragraph. Never the words "safe" or "cannot be tricked".
6. **New section "Where Mizan goes next"** (overview page, last), headed with a visible label "Plan, not built": a customer chat in the operator's app and a staff screen, in Arabic and English, text then voice; then the seven steps in `end-check-2026-11-08-fable.md`, part 6, in plain words.
7. **The agents, on the overview page under the hero:** "Mizan has two parts: five agents, and the gates. The care agent talks to the customer, the adviser checks the law, and two agents play the regulators, TDRA and the Data Office. These four are AI. The fifth, the coordinator, is plain code that routes each step. The gates are code too. They check every action against the law: allow, hold for a staff member, or block. All logged." (Iyas's film wording, 2026-11-08.)

## Done means

- `uv run pytest -q` passes; `python -m onyx selftest` exits 0; both outputs shown.
- A list of every new or changed English sentence, page by page, old against new.
- Every number in a new sentence listed with the file and line it comes from.
- Words lost: list them (a script, scripts and styles stripped). Only the replaced lines named above may lose words.
- Screenshots of every changed page at 1280 and 390, light, in `docs/report-back/task-56c-shots/`.
- Report-back `docs/report-back/2026-11-08-task-56c-site-words.md`, with the commit hash.

## Limits

- **English only.** No Arabic word added, changed or translated, and the Arabic view's English labels stay English: Arabic needs the Arabic check (two reads and Iyas), which this order does not carry. In the Arabic view the new English sentences show as they are.
- Only `onyx/site.py`, `onyx/replay_viewer.py`, the pages they build, and tests pinned to their words.
- No figure changes. No model call. No README, report or annex edit.
- Sources: the repo and the end-check file only. Nothing from memory.

## Stop and ask when

- A number you need is in neither source.
- A change would remove a figure, a clause, a quote or a link.
- The repo is not clean at the start.
When the report-back is written, stop.

## Addendum (Iyas, 2026-11-08)

- Runs page, top, one line: "Sahab Telecom is a made-up operator we built for these tests. Its customers, numbers and prices are made up; the laws are real." Source: `onyx/data/scenarios/README.md` line 5.
- **Unseen bank (replaces item 3's last bullet):** two boxes. (a) U1 to U7, heading "Next tests: seven new stories, not run yet", text: "We wrote these seven stories before our first scored run and locked them, so we could not tune Mizan to them. After the shortlist we run them for the first time, in English and Arabic." (b) U8, heading "The attack test: a customer tries to trick Mizan", text: "We ran this one. Before our fix, 8 of 48 tries got through; after it, 0 of 48." (annex line 255).
- **Each of the five scenarios reads as a story (Iyas, 2026-11-08), the pattern below, written from that scenario's own JSON file and the report's Demo scenarios item; nothing invented:**
  1. English title in plain words (S1: "A customer flying abroad wants their phone to work there"). The Arabic title stays as it is.
  2. A story box on top: "A customer of Sahab Telecom (a made-up UAE operator) opens the chat in the Sahab app and talks to Mizan, the operator's AI assistant. The customer says: '<the customer's first message, verbatim>'." Then one sentence on what the test asks and what the law expects.
  3. One plain line above each step, saying who speaks to whom and what happens, naming the coordinator as plain code. S1 example: "1. The coordinator (plain code) tells the adviser a chat has opened and asks: which sales channel is this? 2. The customer writes to Mizan, asking about using their line in London. 3. The coordinator tells the care agent to offer the UK roaming bundle. 4. The customer says yes. 5. The customer confirms with a code and accepts the terms. 6. A week later the bundle ends while the customer is still abroad. The test asks: can it be renewed without asking the customer again?"
  4. The step's existing detail stays, below the plain line.
- **Verify lines and technical lines** (the long grey paragraph, the run header, the "Without the gates" file line, "Verify this log" buttons): move to a small side column (below the story at 390 px), each with one plain sentence. Top paragraph becomes: "Every law quote here is checked word for word against the official text. To check a run yourself, use Verify." Run header plain line: "Scenario 1, run 1, in English, with the gates on. The log is untouched." "Without the gates" plain line: "Same conversation with the gates off: 3 actions went through that the law does not allow." The technical lines stay, in small print.
- Report-back: every story box and every plain step line, all five scenarios, listed in full for Iyas to read.
- **Arabic view, right to left (Iyas, 2026-11-08):** in the Arabic view, every block that holds Arabic text (story boxes, titles, plain step lines' Arabic parts, chat bubbles, headings) sits right to left, aligned right. English lines inside stay left to right. Layout only; no Arabic word changes.
- **Previous / Next beside the step (Iyas, 2026-11-08):** move the Previous and Next buttons (and the step counter) out of the top bar to sit right under the current step, so the reader does not scroll up to move on. At 390 px they stay on screen (sticky at the bottom).
- **"Present (key p), seconds per step":** a slideshow mode that moves to the next step by itself every N seconds. Keep it, move it into the side column, and give it a plain label: "Play the steps by themselves, every N seconds".
- **Replaces the "seconds per step" bullet above (Iyas, 2026-11-08). The runs page is for a judge who opens it cold:**
  1. Top of the page, before anything else, one plain box: "Here are the five scenarios we ran. Pick English or Arabic, then pick a scenario. Press Present to watch it step by step, or use Previous and Next."
  2. Each scenario card carries a visible **Present** button and a line above it: "Click Present to start S1" (S2, S3 ... on each card). Present starts that scenario from step 1.
  3. Present moves every **12 seconds**, fixed, no number box. A Pause / Play button and Previous / Next sit beside it. Key p keeps working.
  4. In Present, the whole current step (customer line, agent proposal, the gate's answer, any hand-over box) fits on one screen at 1280 x 720 and above, with no scrolling; long quotes and clause lists fold closed and show a "show the law" toggle.
  5. The "Figures for runs/... (eval.run_metrics): citation validity 1.00, action recall 0.67, abstention 1, gap recall 0.33" line becomes one plain sentence with the same figures, for example: "In this run: every law quote was correct; Mizan took the expected action at 2 of 3 key steps; it said 'no rule covers this' where it should; it flagged 1 of 3 gaps." Write each from the metric's definition in `eval/results.md`; if a plain wording cannot be traced to that definition, keep the technical term and say so in the report-back. The technical line moves to the side column in small print, with the Verify button.
  6. Use the full screen width up to 1440 px for the runs page; no empty side bands at 1920 beyond that cap.
  - Done means adds: screenshots at 1280 x 720 of Present on S1 step 3 (English and Arabic) showing the full step with no scroll bar.
