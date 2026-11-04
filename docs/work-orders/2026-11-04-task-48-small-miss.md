# Task 48: small-miss fixes before the freeze (order, Fable, 2026-11-04)

Build session: `D:\Projects\engineering\onyx-hackathon-build`, Opus. Start with `git switch main`, `git pull`
(main = 43d1e67, CI run 41889674427 "reproduce" passed). Branch `task-48`, one PR.

Sources allowed: the repo as it stands (the CPR chunks in `kb/chunks/tdra-cpr-v2-en.jsonl` and the CPR text in
`kb/sources/` included), and this order. No web reads, no new knowledge-base row, no manifest change, no change under `onyx/data/keys/` or `runs/`. Stop if a
string below is not found once, exactly.

## What Fable checked tonight, and found

CI green on 43d1e67. `task-46` holds nothing past main. Replay viewer shows both languages (English and Arabic
run blocks, language toggle). Saudi 552/1445 Arabic quotes 13.1.1 and 13.1.2 match page 14 of the Arabic PDF by
eye. DIFC Art 6(3)(a) quote matches the stored text. The two Authority rows (WAM English, TDRA Arabic) are not
duplicates: different publishers, each note names the other. COPPA row title stays (the extract line dates the
text; no amendment date is on file). Cabinet 21/2013 needs no line (information security in federal entities; not
a licensee: inferred from its title, the text was not opened). `docs/report.pdf` is the Task 47 build, newer than
the last change to `report.md`; 12 pages, 5 main; every page read as a low-resolution image. The misses are items 1
to 7 below; item 8 rebuilds.

Not covered tonight: `docs/gaps.md` lines 304 to 393 and 440 to 897; the README past line 80; CPR 4.18 to 4.21 (only
the earlier full-read summary), and 4.17.2 and 4.23.1 (not in the chunks); the full twelfth-wrap submission list.
`tests/test_task_45.py` line 23 matched the sweep's search and was not read.

## Tasks

1. **Annex D, stale count.** `docs/annex.md` line 222: `the 89 records` becomes `the 108 records`. (Checked
   tonight: 161 chunks, 77 with `text_ar`, 10 C5 Arabic runs: Annex D's other numbers hold.)

2. **Gap 2, the claim a telecom lawyer attacks first** (prep ruling 2026-11-03, section 4). The CPR already sorts
   sales by channel; the row must say what the channel rules do not cover. First read CPR 4.15 to 4.23 whole in the
   English text in `kb/sources/`; if any clause contradicts "a conversational agent fits none of them", stop and ask.
   Three places, each the whole string:

   a. `onyx/data/gaps.json`, gap-2 `"gap"`, replace the whole value with:
   `Consent elicited by an AI: the CPR accepts spoken consent if it can be stored (4.7.2) and sets the consent safeguard by sales medium: a recording of the Subscriber giving verbal consent on a call to the call centre (4.17.3), a 'no' default on yes/no screens in the Licensee App (4.22.3), 2FA for each online purchase (4.23.2). A conversational agent fits none of them: a spoken or typed 'yes' has no screen to default to 'no', and a recording proves what was said, not which medium's rule the agent was under; so the same agent meets a different standard depending on where the operator embeds it, and whether a recorded spoken 'yes' is consent 'in writing or electronically' under the PDPL (6(1)(b)) for processing beyond the contract (4(9)) is unsaid.`

   b. `docs/report.md` line 138, the row-2 gap cell (between `| 2 | ` and ` | coordination |`), replace with:
   `Consent elicited by an AI: the CPR sets the consent safeguard by sales medium (recorded verbal consent on a call, 4.17.3; a "no" default on app screens, 4.22.3; 2FA online, 4.23.2); a conversational agent fits none, so the same agent meets a different standard depending on where it is embedded, and whether a recorded spoken "yes" is consent "in writing or electronically" under the PDPL (6(1)(b)) for processing beyond the contract is unsaid`

   c. Any test that pins the old gap-2 wording (search `nobody has said`): pin the new text instead.
   The clauses searched, UAE position and recommendation of gap 2 stay as they are. If page 5 of the rebuilt PDF
   overflows, shorten cell (b) by dropping `2FA online, 4.23.2; ` first, never the 6(1)(b) clause.

3. **Gap 7, "three UAE texts".** ADGM's held extract (sections 3, 26, 32, 33) has no automated-decision line, so
   the sentence is a claim about texts read. In `onyx/data/gaps.json` gap-7 `"uae_position"` and
   `tests/test_gaps.py` line 1393: `Below the federal level, three UAE texts set such standards` becomes
   `Below the federal level, three of the UAE texts read set such standards`.

4. **DHA "says" line, narrower than scope 2.1.** DHA policy 2.1 reaches facilities, professionals, pharmaceutical
   manufacturers, insurers, public health entities and researchers in DHA's jurisdiction. In `onyx/data/gaps.json`,
   both occurrences (lines 227 and 272) of
   `Sector line: DHA policy 4.3.2 binds DHA-licensed healthcare entities in Dubai (scope 2.1);` become
   `Sector line: DHA policy 4.3.2 applies to AI solutions in healthcare services used by facilities, professionals, pharmaceutical manufacturers, insurers, public health entities and researchers within DHA's jurisdiction (scope 2.1);`

5. **One name for the Authority.** `docs/gaps.md` calls it "Artificial Intelligence and Data Authority" (line 11)
   and "Federal Authority for Artificial Intelligence and Data" (line 141, from gap-2's `"note"`). In
   `onyx/data/gaps.json` gap-2 `"note"` (the backslashes below only mark literal backticks; they are not in the
   string):
   `its competences move to the Federal Authority for Artificial Intelligence and Data (announced 2026-06-14, \`fed-ai-data-authority-2026-06-14\`); the register keeps the statutory name.` becomes
   `on 2026-06-14 the Prime Minister approved an Artificial Intelligence and Data Authority to take over its functions (rows \`wam-2026-06-14-ai-data-authority\`, \`fed-ai-data-authority-2026-06-14\`); the register keeps the statutory name.`
   Update the pin `DATA_OFFICE` in `tests/test_gaps.py` (line 827) to match. `tests/test_report.py` line 454 checks
   `docs/report.md` only; it must still pass unchanged.

6. **Page 1, the date that breaks across lines.** `docs/report.md` line 6:
   `**GitHub link (code):** https://github.com/SHRA1M/onyx-hackathon-build (public from 2026-11-09)` becomes
   `**GitHub link (code, public from 2026-11-09):** https://github.com/SHRA1M/onyx-hackathon-build`

7. **The verify page, one door from the replay page.** The replay index links no verification page.
   In the generator (`replay_viewer.py` or wherever `docs/replay/index.html` is built; never the HTML by hand), add
   one line under the page header: `Every quote on this page is checked word for word against the issuer's file on
   every push; to check one yourself: <a href="../site/verify.html">verify</a>.` Regenerate the replay pages; the
   only diff is that line.

8. **Regenerate and rebuild.** `python -m onyx gaps` (diff of `docs/gaps.md` is items 2 to 5 only), the site pages
   that carry gap text, then the report (`docs/build_report.py` as Task 47 ran it) to `report.docx` and
   `report.pdf`.

## Done means (show each output in the report-back)

1. Full test suite passes; print the count (749 by the last report-back) and the names of every test whose pinned
   string changed.
2. `python -m onyx kb verify`, `check-data`, `selftest`: unchanged counts (108 / 100 / 5 / 3; 161 chunks).
3. Page count of the rebuilt PDF: 5 main, 12 total, printed by the page script. Page 5 still ends with "Limits and
   next steps"; page 1 shows the GitHub line on one line.
4. The count check, every number the report states (not only 108): list them with the file that proves each.
5. `git diff --stat` on the PR: `onyx/data/gaps.json`, `docs/gaps.md`, `docs/report.md`, `docs/annex.md`,
   `docs/report.docx`, `docs/report.pdf`, the replay generator and `docs/replay/*.html`, the site gap pages,
   `tests/test_gaps.py`; nothing under `kb/manifest.csv`, `onyx/data/keys/`, `runs/`, `onyx/prompts/`.
6. Print gap 2's new row text in the report-back and do not merge until Iyas has read it: the wording is a new legal
   claim. Then CI "reproduce" green on main after the merge; paste the run id.
7. hq's copies: none; the report and annex are read from the repo (brief, open question 3).
8. Read `tests/test_task_45.py` line 23: if it pins a string this order changes, update the pin and name it under
   check 1.

## Limits (the seven layers)

No prompt, gate, mandate, retrieval or model change: versioned prompt, grounding, gated tools, identity, injection
defence, cost cap and trace all as shipped at Task 47, untouched; no eval rerun is owed because no prompt or rule
changed (standing rule 3 applies to prompt changes). Masking, cache/router and identity stay deferred (Fable
2026-10-29 and 10-30; nothing due before 11-09). No new knowledge-base row (Fable, 11-04). COPPA and WAM rows
unchanged. Frozen keys never edited.

## Stop and ask when

A string above is found zero or more than once; a test pins a report figure this order does not name and the
figure changes; page 5 still overflows after the item-2 shortening; the replay page tests fail on the new line;
anything in `docs/site/` would change beyond the gap and replay text.

## Not built, and why (Fable, 2026-11-04)

The per-quote verify button (rival read, section 10 item 5; Iyas's condition met tonight): no. Criterion 3 already
holds the proof (CI verbatim check, `kb verify`, `docs/site/verify.html`, clause, page and words per step on the
replay page); the 11-06 video will show the replay page (inferred; the video plan was not read), and a viewer
feature on 11-05 can put a defect into the video. Item 7 gives the judge the door for far less: one line, low risk
but not none, because it also regenerates the replay pages, so its diff check must pass before the video. After the
shortlist, with voice input.
