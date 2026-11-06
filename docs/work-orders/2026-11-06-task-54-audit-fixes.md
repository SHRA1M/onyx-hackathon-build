# Work order: Task 54, audit fixes before the film (Fable, 2026-11-06, evening)

Written on Fable after a full read of `docs/report.md`, `docs/annex.md`, `README.md` (branch `task-53`, working tree at 2026-11-06 ~11:20), the five replay pages, the what-if and model-down pages, the ITU rules checklist, the scorecard and the template text. Numbers verified by an Opus helper against the repo (every report figure matches `eval/results.md`, the manifest, the chunks, the rules, the mandates, the tests and the runs, except item 1 below). Helper checks of the logs: `runs/c5/S3/*` and `runs/c5/S5/*`, keys `S3.json` and `S5.json`, `onyx/gate.py`, `onyx/replay_page.py`, `onyx/coordinator.py` line 266.

**One task.** Runs after Task 53 is merged, on a fresh branch `task-54` from main. No model call. Frozen logs, keys, `HASHES.txt` and `runs/` are never edited. The gate code does not change in this task (gate changes are Task 55, below, decided separately). Main text must still end on page 5 (`scripts/report_pages.ps1` after every report edit; stop and ask if it leaves page 5). Every count the report states is re-listed in the report-back (the count-check trap: list every number, not the one touched).

## A. Report and annex text

1. **Annex B, "13 deciding functions".** `onyx.gate.GATES` maps 16 verbs to 17 distinct functions (the retention gate `records` and the three Task 52b gates `disclosure_recipient`, `reply_recipient`, `change_word` were never counted). Write: "17 deciding functions in `onyx/gate.py` (three of them added on 2026-11-06 behind the gate-version flag, Annex C), mapped in `GATES` from the 16 verbs". Pin: whichever test holds "13".
2. **Duplicate block.** "**CPR 26.6 and 26.7 read together.**" and the 17 lines after it appear byte-identical in Annex B (line 139) and Annex C (line 230). Keep Annex B. In Annex C replace the whole block with one line: "CPR 26.6 and 26.7, the four clauses in both languages and our reading: Annex B." Task 51b put it in both; Fable reverses that for room and because a judge reads it as a paste error. Pins in `tests/test_task_51b.py` and `tests/test_annex.py` move.
3. **Heading.** "## Requirements" becomes "## Use case requirement", the template's words (session 5, Vishnu 47:40: "the template intact"). Task 36's rename is reversed. Pins in `tests/test_report.py` move.
4. **Annex C, U8 bound.** "a count of zero bounds the true rate at about 39%" becomes "a count of zero bounds the true per-run rate at about 39%" (the bound is on 0 of 6 runs, not 0 of 48 steps). Same words in README line 176 if it says "upper bound about 39%": add "per run".
5. **Gap table.** After the table's last row or in the Method paragraph, add "Gap 7 and gaps 13 to 15: Annex F." if it fits on page 5; if not, add it to the Annex F opening sentence only.
6. **Mapping table, MLFO row, Documents cell** reads "Y.3172; Y.3172; Readiness 2.0". Make it "Y.3172 (both); Readiness 2.0".
7. **Annex B, "each rule carrying its clause, page and verbatim quote in both languages"** is false as printed: `quote_ar` is empty for most rules (71 of 71 CPR chunks hold `text_ar`, but the rules do not). After item B.1 the pages show the chunk's Arabic, so write: "each rule carrying its clause, page and verbatim quote, and the clause's Arabic text where the chunk holds it (every CPR clause, Decision 16/2026, three clauses of the agentic guide; the PDPL and the other texts are English-only on file, Annex A)".

## B. Replay pages (page generator only; the runs do not change)

1. **"Clauses searched" AR line reads the wrong field.** `onyx/replay_page.py` lines 171 to 174 print `rules.json` `quote_ar`, empty for most rules, so every page prints "no Arabic text on file" against CPR clauses whose chunks hold the Arabic. Change: the AR line prints the chunk's `text_ar` (by the rule's `document_id` and `chunk`), falling back to `quote_ar`, then to "no Arabic text on file". The EN line likewise prints the chunk's `text_en` when the rule's `quote` is empty or the document is Arabic-only.
2. **Arabic-only documents print under "EN:".** For `decision-16-2026-ar` (and any document whose chunks have empty `text_en`), the page labels the Arabic line "AR:" and the other line "EN: Arabic-only text; no official English on file". Same in the "Gate on" rule lines where the quote is Arabic.
3. **S5-6 block with no rule under it.** When a verdict's `clause_ids` is empty, the page prints the base-check reason the log holds (here: "deadline 'three business days from 2026-10-19' is not a rules.json rule, value and unit"), labelled "base check". A judge must never see a bare **block**.
4. Regenerate `docs/replay/*.md`, `docs/replay/index.html` and `docs/site/` (`python -m onyx site`); the pinned-bytes test moves and is named. Open S2, S5 and the site's runs page after the regeneration and paste three lines from each into the report-back showing the Arabic now present.

## C. Two recorded verdicts disagree with the frozen keys: say so

The scored C5 runs (recorded before 52b, frozen) hold two steps where the gate's verdict is not the key's:

- **S3-5** (19:30 outbound offer to a Do Not Call number). Key: **block**, must cite Spam Calls 15.4, 10.2, 9.5, Cabinet 56/2024 Art 4, CPR 28.26, PDPL 17. Recorded, all 4 runs: **hold** under the consent rules (4.3, 4.7.1, 4.10, 4.11, 4.22). Why: `marketing_gate` (gate.py 617 to 620) runs only when `args.outbound` is set; the model wrote `channel: "outbound_marketing_call"` and no `outbound` key. The same shape as the 52b fault. The facts (time 19:30, `dncr_listed`, opt-out) were all on file.
- **S5-6** (TDRA requests the dispute response and the complaint record). Key: **allow**. Recorded, all 4 runs: **block**, no clause: base check at gate.py 838 to 840 blocks when `args.deadline` is text, not the rule's value and unit; the model wrote "three business days from 2026-10-19".

Report changes (figures do not change; `action recall` scores verb and addressee, not verdict, so 110 of 112 stands):

1. **S3 line**, "A retention offer to a Do Not Call number: block (Cabinet 56/2024)." becomes "A retention offer at 19:30 to a Do Not Call number: held under the consent rules; the marketing gate (Cabinet 56/2024, Spam Calls 15.4) did not run, because it read a field the model did not fill (Annex C)."
2. **S5 line**, "the block proceeds: allow; TDRA requests the report." becomes "the block proceeds: allow; the TDRA's request for the record: blocked by a base check, the deadline written as text, not the rule's value (Annex C)."
3. **Annex C, after the U8 paragraphs**, a new paragraph "Two recorded verdicts against the keys." stating both steps as above, in the same register as the 52b paragraph: what was tested, what was exposed, what is listed for the fix (Task 55, or after the shortlist if Task 55 does not run). Every C5 step where the recorded gate verdict differs from the key's expected verdict is listed there with step id, key verdict, recorded verdict, reason: the build computes the full list from the logs and keys, not only these two, and prints it in the report-back first. If the list is longer than these two: stop and ask before writing the annex paragraph.
4. **Annex C, definitions:** one sentence after "Precision of the headline figures": "Action recall scores the proposed verb and addressee against the key; verdict agreement (the gate's verdict equals the key's) is printed in `eval/results.md`, en / ar." The build adds that figure to `eval` (recomputation from the committed logs, no model call) and to `eval/results.md` and `eval/results.json`, pooled and per scenario, with a Wilson interval, and prints the number in the report-back. It enters the report's Results line only if hq says so after seeing it. If `eval` already prints such a figure under another name, say which and add nothing.
5. **README "What we do not claim"**: add the two steps in one bullet, with "listed for the fix".

## D. Done means (show each output)

- `uv run pytest -q` green; `python -m onyx selftest` green; `python -m onyx kb verify` counts unchanged (108 / 100 / 5 / 3); `python -m onyx site` then `git status` shows only intended files.
- `scripts/report_pages.ps1`: main text ends on page 5, annex starts on page 6; print the output.
- Count list: every number in `docs/report.md` and `docs/annex.md`, unchanged or changed, with its source.
- Grep per Task 53 item 25 (only / first / sole / unique / no other / none of / unlike other / the one) on the edited files; list hits and verdicts.
- The S2, S3, S5 replay pages after regeneration: paste the "Clauses searched" lines for CPR 26.7.2, CPR 24.10 and Decision 16/2026 4.17.
- Report-back at `docs/report-back/2026-11-07-task-54-built.md`, PR opened, not merged. Give its full path and stop.

## E. Limits

Seven layers unchanged from Task 53 (versioned prompt shipped; grounding shipped; gated tools shipped; identity deferred; injection defence partial, 52b; cost cap 45, no spend here; trace and evals shipped). No prompt change. No gate change. No new scenario, run or model call. No new gap row.

## Stop and ask when

The main text leaves page 5 after items A.1 to A.7; the verdict-against-key list (C.3) has more than the two steps; verdict agreement (C.4) is below 0.90 in either language; a pinned test cannot be moved without changing a figure; the regenerated pages differ anywhere other than the AR/EN lines and the base-check reason.

---

## Task 55 (decided by Fable, 2026-11-06; runs only if Task 54 is merged by 2026-11-07 18:00 Amman and Iyas says go)

Same pattern and research basis as Task 52b (`perplexity-read-gate-fix-2026-11-06-fable.md`, `vendor-sources-read-gate-fix-2026-11-06-fable.md`: read every field, fail closed to a human), same gate-version flag, frozen logs replay as recorded, and the "would change N of 189 verdicts" count re-derived and printed:

1. `marketing_gate` runs for `propose_sale` when `args.outbound` is set **or** any argument value or the proposal's `channel` contains "outbound", "marketing" or "call" (English and Arabic word lists as in 52b). Expected on replay: S3-5 hold becomes block in 4 of 4 runs.
2. A text `args.deadline` becomes **hold** ("deadline stated as text; a named human checks it against the rule"), not block, with the rule's value and unit printed beside it. Expected: S5-6 block becomes hold in 4 of 4 runs, cited cpr-26-16-1.
3. Both printed in Annex C's new paragraph as "fixed on 2026-11-07 under gate version 2; the scored runs were recorded before the fix and were not re-recorded".

If Task 55 does not run, the Annex C paragraph says "listed for the fix after the shortlist" and nothing else changes.

## Not in this order

The 22 landing-page manifest rows; the SIM block at S5-3 under the disconnection rules (recorded; key says hold; defensible as fail-closed, left as is); the film; the rival sweep (`rival-sweep-2026-11-06/`, Opus helper, not yet read by Fable).

---

## Changes by Fable, 2026-11-06, night (`task-53-stop-3-task-54-rivals-ruling-2026-11-06-fable.md`)

1. **Moved into Task 53 (item 45a):** A.3, A.6, C.1 and C.2. Task 54 does not apply them. When Task 54 starts, the report's heading, the MLFO cell and the S3 and S5 lines are already as those items say.
2. **A.5 is annex-only:** the Annex F opening sentence gains "Gap 7 and gaps 13 to 15 are below."; nothing is added to page 5.
3. **The main text is not edited in Task 54,** with one exception: once the Annex C paragraph (C.3) exists, "(Annex C)" may be added to the end of the S3 and S5 lines, each measured with `scripts/report_pages.ps1`; if either moves the main text off page 5, that addition is dropped and the line stands without it.
4. **C.4's figure** goes to `eval/results.md`, `eval/results.json` and the Annex C definitions sentence only. The report's Results line does not change, whatever the value. Below 0.90 in either language is printed and named in the report-back; it is not hidden and not a reason to stop the rest.
5. **Task 55 does not run before submission.** It is first on the after-shortlist list (11-18 to 11-25). No new Perplexity round is needed for it: both faults are the class the 52b reads settled (OWASP Agentic Top 10 2026, ASI02 mitigation 7, "fail closed on ambiguous resolution"); its order cites those two reads when it is written. The Annex C paragraph (C.3) says "listed for the fix after the shortlist".
6. **Freeze:** Task 54 runs under the 2026-11-06 freeze because every change makes the report say what the frozen logs record; no result, key, log or gate changes.
