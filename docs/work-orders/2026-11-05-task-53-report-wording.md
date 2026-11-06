# Task 53: report wording after Iyas's review and the gap ruling (order, Fable, 2026-11-05)

One task, one build session, after Task 52 (the attack test) merges. Report, README and site text only. No run, no key, no prompt,
no code path that acts. Starts from main after 51b. Renumbered from 52 to 53 on 2026-11-06 (Iyas: the attack test goes first). Starts from main after the attack task
(Task 52) merges. Annex and README line numbers below may have moved: find each sentence by its words, and stop only if the words are missing.

Source rulings: `gap-recall-ruling-2026-11-05-fable.md` section 1; `review-fixes-2026-11-05.md` items 1 to 5
(Iyas's PDF review). If Iyas sends more page notes before the session starts, hq appends them here as items 11 on;
nothing else is added.

## Task

Edit the texts below, word for word where a replacement is quoted, rebuild `docs/report.pdf`, regenerate the site.

1. Report header and README team table: "BAU Faculty of Artificial Intelligence", in full, never "AI".
2. Report header and README: add Zaid Saaydeh as the fourth member (spelling as Iyas gave it: Zaid Saaydeh).
3. Report Introduction and README line 25: replace the "not an institution in a drill" sentence with: "The case is an
   ordinary customer talking to their phone company in a chat or on a call, not a practice exercise."
4. Report Introduction, the "binding texts" sentence, replace with (Iyas asked for it clearer, 2026-11-05): "UAE
   telecom rules already in force set four limits on an AI in that seat. It cannot charge a customer for a service they
   did not expressly order, so nobody pays for what they did not ask for (TDRA Consumer Protection Regulations v2.0,
   CPR 4.3). It cannot share their data with affiliates or outside parties without prior consent, so the customer
   decides who sees it (24.6). It cannot cut their line for non-payment without a warning first, so they have time to
   act (22.1). And it cannot handle their complaint, because that conversation is reserved for a person: 26.7.2
   requires licensees to "preclude the use of non-human agents by Licensees in conversations with Consumers regarding
   Consumer Complaints"." Wording pins (`bar any AI in that seat`) move with it. This is longer than the sentence it
   replaces: pay from the two allowed places, and if the main text still leaves page 5, stop and ask (below).
5. Header "Demo video" line: unchanged now ("see the repository README"); the URL lands in the submission-day order.
6. Strip, cell 5 (`docs/report.md` line 9): `expected gaps found 5 of 7 in every run` becomes
   `abstained and logged the gap on the unanswerable step in 20 of 20 runs`.
7. Results paragraph (line 121): `expected gaps: 5 of 7 found in every run, 2 missed (both S1), 3 unexpected ids
   flagged` becomes `expected gaps: 5 of 7 found in every run; the 2 not found (gaps 2 and 6) are keyed to S1 steps
   where the adviser, the only agent that holds the register, does not speak (Annex C); 3 unexpected ids flagged`.
8. Gaps section (line 133): `The recorded runs re-find 5 of the 7 expected gaps on every run.` becomes `The recorded
   runs re-find, on every run, all 5 expected gaps keyed to a step where the adviser speaks; gaps 2 and 6 are keyed
   to S1 steps it does not reach (Annex C).`
9. Annex C, end of "What the test does not show": add `Gap recall counts flags, and only the adviser may flag:
   flag_gap is in its mandate alone. The S1 key places gap 2 at the channel classification, which is plain code, and
   gap 6 at the care agent's offer; neither step calls the adviser. Its one model turn in S1, step 6, shows it only
   the renewal question, and no run flagged gaps 2 or 6 there, so S1 reads 0.33. The keys were not edited; after the
   shortlist the adviser reads the whole conversation or the care agent gets the register, and the runs are repeated.`
10. Site, the gap recall definition (`def-gap_recall`, source in `onyx/site.py`): append `S1 reads 0.33 because its
    key places two gaps at steps the adviser does not reach; see Annex C.` Regenerate `docs/site/`.
11. (Added by Fable at the 51b check, `task-51b-check-and-perplexity-read-2026-11-05-fable.md`.) The four-clause
    note's last sentence overstates the gate: `complaint_gate`'s clause list (`onyx/gate.py` 545) has no chapeau, and
    Annex B prints that list right under the note. In `onyx/data/gaps.json` (gap 1 `clause_note.note`), and so in
    `docs/gaps.md`, `docs/annex.md` (Annex B and C) and `docs/site/gaps.html`, replace `Mizan enforces the stricter
    reading and cites the chapeau, the clause and licence 9.1 together.` with `Mizan enforces the stricter reading,
    citing 26.7.2 and licence 9.1; the chapeau is quoted here and holds no rule.` The pin is `NOTE` in
    `tests/test_task_51b.py`; `rules.json`'s `language_note` for `cpr-26-7-2` is already right and does not change.
12. (Added at the Arabic check, Claude Cowork flagged the pair, 2026-11-05.) Gap 15's English quote stops before the
    cap that its Arabic carries. In `onyx/data/gaps.json` line 572, `quote` becomes the whole sentence of the official
    English, as in the chunk: `The Cabinet shall issue a resolution on the schedule of violations and fines imposed on
    licensees provided they do not exceed (10,000,000) ten million dirhams for each violation.` `quote_ar` does not
    change. It flows to `docs/gaps.md` and `docs/site/gaps.html` on regeneration.
13. (Iyas, 2026-11-05: a reader must understand it.) `docs/report.md` lines 37 and 38, the "What is different"
    paragraph, replace the text after the bold lead with: `We ran the same five scenarios twice on the same model, once
    with the gates on and once with them off. With the gates off, on average about two acts per run went through that
    should have been stopped or handed to a person: 2.3 in English and 2.1 in Arabic `[C3, prompt v3, three runs per
    scenario per language]`.` The two figures stay as they are, unchanged from `eval`.
14. (Iyas, 2026-11-05: a reader must understand it.) `docs/report.md` line 35, replace `` `eval` recomputes every
    figure in this report from the logs. `` with `The test results in this report can be checked: a command called
    `eval` recalculates them from the run logs, and anyone can run it.`
15. (Iyas, 2026-11-05: "mandate" is not a word a reader knows.) In `docs/report.md`, word for word:
    - Line 29: `where its mandate ends` becomes `where its authority ends`.
    - Line 32: `Five agents with bounded mandates (care, the policy and legal adviser, the Data Office, TDRA and a
      coordinator).` becomes `Five agents (care, the policy and legal adviser, the Data Office, TDRA and a coordinator),
      each with a fixed list of what it may do and read.`
    - Line 44: `retrieval is scoped to the agent's mandate, so the model sees only the policy text its role may use`
      becomes `each agent searches only the documents its role allows, so the model sees only the policy text that role
      may use`.
    - Lines 51 and 52: `retrieval is scoped to the agent's mandate, a cited id` becomes `each agent searches only the
      documents its role allows, a cited id`.
    - Line 70: `mandate-scoped retrieval` becomes `retrieval limited by role`.
    In `docs/annex.md` line 21, before `every agent's mandate names the clauses`, add: `An agent's mandate is its fixed
    list of what it may do and read.` The annex keeps the word from there on because it names `mandates.json` and
    `sources_mandate`. Code, data, logs, tests of code names and the README's technical tables keep the word.
16. (Iyas, 2026-11-05: a reader must understand it.) `docs/report.md` line 78, replace the sentence with: `Of the 13
    Readiness 2.0 dimensions, we claim five (6, 7, 8, 10, 11) with evidence from the running system and two (1, 13)
    from documents only, with no running system behind them; the other six we do not claim.`
17. (Iyas, 2026-11-05: "there is nothing understood here".) `docs/report.md` lines 86 to 93, the body of "Demo
    scenarios", replace with the text below, word for word. Every figure stays as it was.

    We test Mizan on five made-up customer conversations, called S1 to S5: S1, roaming before a flight; S2, a billing
    question that becomes a complaint; S3, a partner wants the data and the AI provider is abroad; S4, non-payment and
    an automated disconnection; S5, a TDRA dispute and a loss report. Each is shown in detail under Error scenarios.

    1. See it online, nothing to install. The replay site shows each recorded conversation step by step, with the
    clause, page and words behind every decision (`docs/replay/index.html`).
    2. A customer asks why. One command prints the decision, the clause with its quote and the log entry's fingerprint,
    in English or Arabic: `python -m onyx why <log> --step <n>`, where `<log>` is the file of the recorded conversation
    and `<n>` is the step number. The answer is read from the log, so no AI is asked to explain itself afterwards.
    3. Two instructions conflict. In S3, step 3, the care agent proposes sending customer identifiers to the AI provider
    abroad. The gate blocks it under PDPL 22 and 23(2), and refuses even a staff member's override (logged as
    `override_refused`). Privacy wins by rule, not by what the model happens to do.
    4. Another regulator, another rule. `onyx whatif` re-runs a recorded conversation under a proposed new rule: TDRA's
    missing hand-over rule (gap 1) on S2, and the Data Office's missing rule on reviewing an automated decision (gap 4)
    on S4. A re-run costs USD 0; a new live run on the
    model costs USD 0.27 (USD 5.3767 over the 20 scored runs).

18. (Replaced 2026-11-06.) The annex and README lines on the steered subscriber are in Task 52. Here, one clause in the
    "What is different" paragraph, after item 13's text, only if the main text still ends on page 5:
    `On eight steps we wrote where the subscriber's words try to force a barred act, the gate passed N of M (Annex C).`
    N and M come from `eval/results.md`. If it does not fit, leave it out; that is not a stop. If Task 52 was dropped,
    skip this clause and add to Annex A "Known limits": `No scenario carries subscriber text that tries to steer the
    agent; none was run.`

19. (Added by Fable, 2026-11-05, Iyas asked where the DPO review shows.) The review happened on 2026-11-05 and the
    README names the reviewer, but `docs/report.md` line 159 still lists it under "Next:" as future work. Fix, word
    for word: in line 159 remove `; a data-protection practitioner's review
    (practice, not legal advice)` from the "Next:" list, so it ends `team approval of holds.`; then, in line 158,
    after `Annex A, "Known limits".` and before `Next:`, insert `Ra'ed Shraim, a data-protection officer outside the
    team, reviewed the gates' reading of the texts (practice, not legal advice, no UAE standing); what he found and what
    changed are in Annex A.` In `docs/annex.md`, Annex A, add one sentence after the Known limits: `Reviewed on 2026-11-05
    by Ra'ed Shraim, Director Business Excellence – DPO, Solidarity First Insurance Company, Amman – Jordan (practitioner
    review, not legal advice, no UAE standing): his points on CPR 26.7.2's Arabic, licence 3.4.1 and licence 9.1 are in
    gap 1 and the rule notes; his code-level points are listed for after the shortlist.`
    **Name in, relationship not stated (Iyas, 2026-11-06). The title is exactly as his review document gives it. He is
    the leader's father, so no text calls him "independent" or "unrelated".** README line 39, the Reviewer row, stays as
    it is on main. No company ranking enters until Iyas gives its source. Word count on page 5 is about even (one clause
    out, one in); the page check still rules.

    For items 13 to 19 only: a test pinning the old wording of a replaced sentence moves with it and is named with its
    line in the report-back; this is not a stop. The main text must still end on page 5.

## Done means

- Each of items 1 to 10 shows as a diff line in the report-back, with the file and line.
- The main text still ends on page 5 and the annex starts on page 6; the PDF page count is printed. If the main text
  runs to page 6, stop (below). Items 3, 4, 7 and 8 add words; the header "Knowledge base:" line and the third
  introduction paragraph are the places to pay from, as the presentation ruling allowed.
- Every number the report states is listed and unchanged (count check lists all, not only the touched ones).
- Test pins moved and green: `tests/test_task_51.py` lines 20 and 26, `tests/test_report.py` line 330, any pin on the
  replaced sentences. `tests/test_eval.py` line 183 pins the generated `eval/results.md` and does not change.
- Full `pytest` run, count printed; CI green on the PR.
- `onyx/data/keys/`, `HASHES.txt`, `runs/`, `eval/results.md`, `eval/results.json` untouched: `git diff --stat` shows
  none of them.
- Report-back at `docs/report-back/2026-11-06-task-53-built.md`; hq checks it; Iyas runs the merge line.

## Limits

- Text only. No new knowledge-base row, no scenario, no prompt line, no change to `eval.py` or any gate.
- Seven layers: none touched; all stay as Task 51 left them (prompt v5, gates, log chain, masking and router
  deferred by the 10-29 and 10-30 rulings).
- No competitor name enters the report.
- The strip keeps five cells; nothing else on page 1 moves.

## Stop and ask when

- The main text leaves page 5 after paying from the two allowed places. Print how many lines it runs over and stop:
  Fable decides what to cut and simplify (Iyas, 2026-11-05). The build does not cut anything on its own.
- A replaced sentence is not found word for word at the line given (lines read on branch task-51b at 46ca90c, not main).
- A pin outside the four named fails after the change.
- A README table or site page prints "5 of 7" anywhere the order does not name.

## Changes by Fable, 2026-11-06 (`weakness-pass-ruling-2026-11-06-fable.md`, section C)

Task 53 now starts from main after Task 52b merges, or after 52b is dropped (2026-11-07 12:00 Amman). Items 1 to 19 stand. Item 18 and three new items:

18. (Replaced 2026-11-06, second time.) The clause after item 13's text, only if the main text still ends on page 5: if 52b merged, `On eight steps we wrote where the subscriber's words try to force a barred act, the gate passed 8 of 48 before a fix made the same day and N of 48 after (Annex C).`; if 52b was dropped, `On eight steps we wrote where the subscriber's words try to force a barred act, the gate passed 8 of 48, one fault, printed and listed for the fix (Annex C).` N from `eval/results.md`. If it does not fit, leave it out; not a stop.
20. Item 17's third line opens `3. Two instructions conflict (the controversy case).` The rest of the line as written. The template asks scenarios to discuss controversy; the word must be in the report once.
21. README "Model" section, the scored-run line: after `obligation proxy 0.57 / 0.58`, add in brackets the definition from `eval/results.md`'s Definitions section, quoted word for word and shortened to one clause if it runs long; it is not an accuracy figure and the README must not let a reader take it for one.
22. Site overview, the gap recall tile: label it so the 0.87 beside the report's 5 of 7 is explained in the tile's own words: append to its label `(average of the five scenarios; S1 reads 0.33, see Annex C; the report counts all gaps together, 5 of 7). First confirm from the code that 0.87 is that average; if not, stop and ask`, consistent with item 10's definition text. Regenerate `docs/site/`; `test_site.py` pins move with it and are named in the report-back.

Done means and limits unchanged; item 21 is README text, item 22 is site text; neither touches a figure.
23. (Fable, 2026-11-06, from the Task 52 report-back.) Only if 52b was dropped: Annex A's steered-subscriber sentence gains, after "passes them", `, and an empty recipient field is read as the subscriber, which is how the eight steered passes went through (Annex C)`. If 52b merged, its own sentence stands and this item is skipped.
24. (Fable, 2026-11-06.) The report's S3 line "A partner asks for interconnection data: block (24.6)" is checked against the C5 S3 logs' recorded verdict and clauses at that step (52b's report-back prints them; else read `runs/c5/S3/*.jsonl`). If the recorded verdict is a hold by the verification gate rather than a block under 24.6, the line becomes `A partner asks for subscriber data: held, no verification level set (24.10); the override to send identifiers abroad: block, no override (PDPL 22, 23(2); gap 5)`, with the clause ids as the log gives them. Figures do not change. Page 5 rule still holds.

25. (Iyas, 2026-11-06, standing rule: "we don't know so many private repos, so Mizan should not say it's the only of anything".) After every other item is applied, grep `docs/report.md`, `docs/annex.md`, `README.md` and `docs/site/` for `only`, `first`, `sole`, `unique`, `no other`, `none of`, `unlike other`, `the one`. Every hit that compares Mizan with other entries, teams or systems is reworded to state only what Mizan does, with no comparison. Hits that describe Mizan's own internals (the first run, the only citation form the gate accepts, the only route a law gives) stay. On 2026-11-06 Fable found no comparative hit on `task-52`; the build session re-checks after its own edits, and the report-back lists every hit and its verdict (kept or reworded).

## Change by Iyas, 2026-11-06

26. Report header and README team table: add "Mentor: Dr. Wafaa Almaaitah". Iyas says she approved (his word, 2026-11-06). Use "mentor", never "supervised by". Same stop as the rest of this order if the main text leaves page 5.
27. (Fable, 2026-11-07, `task-52b-merge-ruling-2026-11-07-fable.md`) Annex E's table header sits alone at the foot of PDF page 12 since the second U8 table landed; keep the header with its rows (a page break before the heading, or the table's rows kept together). Same page-5 stop.
28. (Fable, 2026-11-07, on Iyas's ask) The after-shortlist attack test goes in Annex C only, not the main text: page 5 is full, item 18 is the main text's one clause on this test, and the main text carries results, not plans. In Annex C, the "What the test does not show" paragraph, after "Three runs per cell is enough to show the effect, not to estimate it finely.", add: `After the shortlist the same test runs on more runs, with attacks written by people who have not read the gate's code.` README: the after-shortlist bullet (now line 262) gains, as its last item, "attacks written by people who have not read the gate's code, on more runs". No number, no date, no "huge"; never "will prove" or "resistance". Not a stop if Annex C's page count moves; the main-text page-5 check stands.

## Changes by Fable, 2026-11-06 night, after session 5 (`session-5-ruling-2026-11-06-fable.md`)

29. Y.3172 table, `docs/report.md`: SRC row's second cell gains "108 instruments (100 verified), 161 clause chunks, English and Arabic; subscriber and account data synthetic, no real person"; PP row's second cell gains "chunk = document, clause, page, text in both languages, status". Counts from the register as built, not from this line. Page-5 stop: if they do not fit, one sentence under the table in Annex B instead, table unchanged.
30. P row's second cell becomes "plain-code gates reading JSON clause rows (`rules.json`: id, document, clause, page, text en and ar); four verdicts (P-1, P-2)". Annex A known limits, one sentence: "The gate's rules are code; the clauses it cites are JSON rows. We found no standard machine-readable form for regulatory rules in the texts we hold and claim none; a standards gap on that form is a candidate for after the shortlist, not a finding." No new gap row. Field names checked against `rules.json` before writing.
31. Annex D, after the SNAI item (corrected by Fable 2026-11-06 against the code on main; replaces the sentence built at stop 1): "The chunk format carries no telecom field (document, clause, page, text in both languages, status): another sector's texts chunked the same way serve the same retrieval, hash-chained log and replay. A swap is not free of code: the gates name CPR clauses by design; the adviser's sales-channel table (`onyx/agents/adviser.py`), the care agent's hand-over line and the coordinator's TDRA role name the same regulation; the replay page highlights two telecom hand-over quotes. Each would be rewritten for that sector. We state the cost of a swap rather than claim a generic framework." Never "domain-independent"; never "serve the same agents". Why: on main the agents are not sector-free (`agents/adviser.py` 6 and 36 to 40, `agents/care.py` 24, `coordinator.py` 6 and 23, `replay_page.py` 22), and Vishnu said of a hard swap "just document it, that is valuable information for us" (session 5, 19:15 to 20:39).

## Changes by Fable, 2026-11-06, after stop 1 (`task-53-stop-1-ruling-2026-11-06-fable.md`)

Answers `docs/report-back/2026-11-06-task-53-stop-1.md`. A fresh session continues Task 53 on branch `task-53` from the working tree as stop 1 left it: commit that state first ("Task 53: stop 1 state"), since `git log main..task-53` is empty. Items 29 to 31 were not applied at stop 1 and are part of this task. The same done-means and limits hold.

32. The cuts, in layers. Measure after each layer with `scripts/report_pages.ps1`; stop cutting at the first layer where the main text ends on page 5 and the annex starts on page 6. Print the measurement after every layer in the report-back.
    - Layer 1, no words lost: Figures 1 and 2 printed at 70 percent of their current width in `docs/build_report.py` (if the builder has no width setting, say so and skip this part); item 29 goes straight to its Annex B fallback, one sentence under the table, the table unchanged; item 30's P-cell change applies; item 31 as corrected applies.
    - Layer 2, duplicated words: (a) the "Demo scenarios" opening paragraph ("We test Mizan on five made-up customer conversations ... under Error scenarios.") is cut, the Error scenarios headings name the five; (b) demo item 2 loses ", where `<log>` is the file of the recorded conversation and `<n>` is the step number"; (c) demo item 4's last sentence becomes "A re-run costs USD 0; a live run on the model USD 0.27 (USD 5.3767 over the 20 scored runs)."; (d) the third Introduction paragraph becomes "Annex A lists the sources (the PDPL is the Personal Data Protection Law 45/2021); 100 are verified: the issuing body's file is on disk with its SHA-256, and a test on every push checks each clause the gates cite word for word against it. No consumer data was used." (`tests/test_task_51.py` keeps "100 are verified").
    - Layer 3: item 18's U8 clause leaves the main text; Annex C and the README carry the test.
    - Layer 4: in item 4's paragraph the three "so" clauses go: ", so nobody pays for what they did not ask for", ", so the customer decides who sees it", ", so they have time to act". The four limits and the 26.7.2 quote stay.
    - Still over after layer 4: stop, print the lines over, ask. The build cuts nothing else.
33. Item 24, the S3 line, word for word: "A partner asks for subscriber data: held, no verification level set (24.10; one Arabic run: block, 24.6); the override to send identifiers abroad: block, no override (PDPL 22, 23(2); gap 5)." Clause ids as `runs/c5/S3/ar/run2.jsonl` gives them.
34. Items 7, 8, 9, 10: "does not speak" (item 7) stays. Item 9, Annex C: "neither step calls the adviser" becomes "neither step gives the adviser a model turn". Item 8: "keyed to S1 steps it does not reach" becomes "keyed to S1 steps where it has no model turn". Item 10, site: "steps the adviser does not reach" becomes "steps where the adviser has no model turn". Why: the log records the adviser's plain-code `classify_channel` at S1-1.
35. Items 1, 2, 26, README: the team cell does not say "students" (Zaid's faculty is not confirmed); it names the faculty only. "Al-Balqa Applied University (BAU)" is spelled out once in the README, in the team row or the line above it. The report header stays as built.
36. Item 27: the guard built stays; no further action.
37. After the cuts: item 25 again; rebuild `docs/report.docx` and `docs/report.pdf` (Word's lock must be gone: PID 6680 or any `WINWORD.EXE /Automation -Embedding` with no window); full `pytest`; PR; final report-back at `docs/report-back/2026-11-06-task-53-built.md`. No merge.

## Changes by Fable, 2026-11-06, after stop 2 (`task-53-stop-2-ruling-2026-11-06-fable.md`)

Answers `docs/report-back/2026-11-06-task-53-stop-2.md`. A fresh session continues Task 53 on branch `task-53` from its last commit. Items 32 to 37 stand except where changed here.

38. The last lines, in layers. Measure after each layer with `scripts/report_pages.ps1`; stop cutting at the first layer where the main text ends on page 5 and the annex starts on page 6. Print every measurement in the report-back.
    - Layer 5, all of these, then measure: (a) Figure 2 and its caption move out of the main text to Annex C, printed at 16 cm, at the end of the C5 results there; the Results paragraph's figure line is replaced by nothing, and the paragraph's first sentence ends ", en / ar]` (Figure 2, Annex C):". Figure 1 prints at 11 cm (`FIGURE_WIDTH` or a per-figure width; if the builder has one width for both, add a per-figure width). (b) The four "Demo scenarios" items print as a numbered list, one item per paragraph, as Markdown lists render; if the builder cannot, a blank line between items in `docs/report.md`. (c) S2's last sentence, "With the model call made to fail at step 3 ... (`docs/replay/model-down-S2.md`).", leaves the main text; the Requirements line "the model-down path hands over with no model in the step" and the annex keep it. (d) "What is the role played by AI?", the last sentence becomes "Plain code written from the binding UAE texts decides; every verdict names the clause it relied on, its page and its words, in English and Arabic; the model never decides." (e) "Limits and next steps", the whole paragraph becomes: "One team wrote the keys, gates and scenarios; the humans are scripted; Arabic coverage is uneven; an outage is shown only by fault injection; erasure from the log and de-identification are unsolved (Annex A, "Known limits"). Ra'ed Shraim, a data-protection officer outside the team, reviewed the gates' reading of the texts (practice, not legal advice, no UAE standing); what he found and what changed are in Annex A. Next: cold runs of the seven unseen scenarios; routing (D-2); team approval of holds. Annex A to F follow."
    - Layer 6: the MLFO and ML sandbox rows of the Y.3172 table become one row, first cell "MLFO; ML sandbox", the other cells joined with "; " and nothing dropped.
    - Layer 7: gap row 12's Gap cell becomes "Agent authority: Mizan's stop at S2-3 sits at Y.3173 'Human and System' on the decision step (Table 7-1), and its hand-over is Readiness D9's inference-to-action latency in the other direction; neither text measures when an acting agent must stop, how often it hands over or how long that takes. Left open with ITU's agreement (2026-10-30)." (every claim kept; if `gaps.json` or a test pins the old cell, the pin moves and is named). Figure 1 at 9 cm.
    - Still over after layer 7: stop, print the lines over, ask. The build cuts nothing else.
39. Item 32(d): the third Introduction paragraph's ending is "against the text stored from it" (the build's suggestion; CI does not hold the issuers' files). `tests/test_task_53.py` moves; `tests/test_report.py:517` and `tests/test_task_51.py:91` stay.
40. Item 30: the field names as built stand: "(`rules.json`: id, document_id, clause, chunk, quote, quote_ar)".
41. Item 29: "108 documents" and the Annex B place stand; the chunk count becomes "161 clause chunks (77 with the Arabic text), English and Arabic".
42. Item 31: the first sentence becomes "The chunk format carries no telecom-specific field (document, article, clause, page, text in both languages, status, retention class, Y.3172 node): another sector's texts chunked the same way serve the same retrieval, hash-chained log and replay." The rest unchanged.
43. Figure 1's label "mandate-scoped retrieval": if `docs/fig/fig1-architecture.png` is generated by a script in the repo, regenerate it with "retrieval limited by role" and say which script; if it is a hand-made image, leave it and list it in the README's after-shortlist bullet.
44. Item 35 stands: no "students" until Iyas answers.

## Changes by Fable, 2026-11-06, night (stop 3 ruling: `task-53-stop-3-task-54-rivals-ruling-2026-11-06-fable.md`)

45. Stop 3: the last 9 lines. First end the four hidden Word processes (item 37). Then the steps below, in order. Measure with `scripts/report_pages.ps1` after each step from (b) on; stop cutting at the first step where the main text ends on page 5 and the annex starts on page 6. Print every measurement in the report-back. Then finish the order (rebuild, item 25 sweep, count list, pytest, PR).
    - (a) Four wording changes, applied before the first measurement, no decision in them. (1) The heading "## Requirements" becomes "## Use case requirement" (the template's words; Task 36's rename reversed; pins in `tests/test_report.py` move). (2) The MLFO row's Documents cell becomes "Y.3172 (both); Readiness 2.0". (3) S3's last sentence becomes "A retention offer at 19:30 to a Do Not Call number: held under the consent rules; the marketing gate (Cabinet 56/2024, Spam Calls 15.4) did not run, because it read a field the model did not fill." (4) S5's last clause, from "The human verifies", becomes "The human verifies, the block proceeds: allow; the TDRA's request for the record: blocked by a base check, the deadline written as text, not the rule's value." Before writing (3) and (4), read the four S3 and four S5 C5 logs (`runs/c5/S3/*`, `runs/c5/S5/*`) and confirm: S3-5 recorded hold under the consent rules in 4 of 4 runs with `args.outbound` absent; S5-6 recorded block with empty `clause_ids` in 4 of 4 runs with a text `args.deadline`. If any run differs, stop and print it. These two lines are true-ness fixes from Task 54 (C.1, C.2), moved here so page 5 is settled once; they carry no "(Annex C)" pointer yet.
    - (b) Figure 1 and its caption leave the main text and print in Annex A, after its first paragraph, at 16 cm, through the annex image path built at stop 3; caption unchanged. The mapping section's last sentence ("Of the 13 Readiness 2.0 dimensions ... we do not claim.") gains " Figure 1 (Annex A) draws the nodes." as its last clause, no new paragraph. The missing-figure test (`tests/test_report.py:118`) and the width test move to the annex. Measure.
    - (c) The Results paragraph's opening becomes "**Results** `[C5, governed, two runs per scenario per language, mean over S1 to S5, en / ar]` (Figure 2, Annex C):" (the prose repeated the bracket; no fact lost). Measure.
    - (d) The Method paragraph's last sentence ("The recorded runs re-find, on every run, ... (Annex C).") leaves; the Results paragraph carries the same statement. If a test from items 6 to 10 pins it, the pin moves and is named. Measure.
    - (e) Demo item 4: "(USD 5.3767 over the 20 scored runs)" leaves only if Annex C or `eval/results.md` prints that figure; if nowhere else, keep it and skip this step. Measure.
    - (f) The four demo items run together in one paragraph, numbers inline (layer 5(b) undone). The build measured (b) with (f) to fit. Measure.
    - (g) Demo item 2's last sentence ("The answer is read from the log, so no AI is asked to explain itself afterwards.") leaves. Measure.
    - (h) Still over after (g): stop, print the lines over, ask. The build cuts nothing else.
    - After the fit: if the gap table's header row still sits alone at the foot of a page, keep it with its first row (the item 27 mechanism) and measure once; if that moves the main text off page 5, undo it and name the orphan in the report-back. The typed demo numbers with blank lines stand (no builder list code). The README PP row change stands. No "students" (item 44).
