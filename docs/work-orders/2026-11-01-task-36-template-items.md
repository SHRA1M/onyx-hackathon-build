# Work order: Task 36, ITU's template items into the report and the demo (2026-11-01, hq on Fable)

Model: Opus 5.5. Repo: `D:\Projects\engineering\onyx-hackathon-build`. Branch `task-36` from `main` (Task 35b).
Decided by hq from ITU's template `D:\Projects\hq\uni\ai-for-good-hackathon\mentoring\submission-template-2026-10-31.docx`
(example team "Vishnu", read 2026-10-31) and session 5 as Iyas recalled it (gaps, solution and method of analysis
all count). Build this order; do not re-decide it. About 4 hours. Before 2026-11-06.

The rule that governs every line below: the report stays at 5 pages (ITU: "max 5 pages", rules-checklist §5.1). No
recorded run is rerun, no answer key, prompt, gate, rule or mandate changes; C5 and C3 figures stay as printed. The
new demo steps are replays and plain-code pages over the committed logs.

## Task

### 1. Report headings follow the template, content kept

Current order: Introduction; Description of the use case; Use case requirement; Mapping; Error scenarios; Policy gaps;
Limits. New order and headings, exactly these words:

1. Introduction (unchanged text, minus the sentence moved in 2 below).
2. Description of the use case (unchanged).
3. **What is the role played by AI?** New, about 90 words, three sentences in the template's three items: (a) the
   model's part: it reads the subscriber's words in Arabic or English, classifies the step, proposes one verb with
   clause ids and a verbatim quote, and drafts the reply in both languages; (b) the knowledge base's part: 88
   documents chunked by clause, retrieval scoped to the agent's mandate, so the model sees only the policy text its
   role may use; (c) the policy's part: plain code written from the binding texts decides allow, hold, block or
   insufficient evidence; the model never decides. Reuse the intro's sentence "The model proposes and plain code ...
   decides" here and cut it from the Introduction, so the words are spent once.
4. **Requirements**, replacing "Use case requirement". Same node ids, same wording for each, ranked in three
   labelled groups, each group one run-on paragraph starting "It is critical that", "It is expected that", "It is of
   added value that":
   - Critical: P-1, P-2 (gates, four verdicts, one block without override); D-1 (hand-over to a named human); PP-1
     (mandate-scoped retrieval, out-of-mandate id invalid); SRC-2 (verified texts with hash, clause check on push).
   - Expected: SRC-1, C-1, M-1, SINK-1, MLFO-1, SB-1.
   - Added value: the what-if replay (proposed rule tested on a recorded run); the model-down path; Arabic scored
     as a run, not a translation; D-2 routing, marked not built.
   If Iyas wants a different rank for any item he says so before the build; otherwise this is the rank.
5. Mapping with ITU-T Y.3172, Readiness 2.0 Report, and domain-specific policies (heading unchanged). Check, do not
   rewrite: every row's Readiness cell names a dimension outside data and model handling where one applies. Today
   SRC 11, C 7, M 6, P 8, D 6, SINK 10 do; PP 10 is a policies dimension; MLFO and ML sandbox cite factors. Nothing
   to add unless a row is found empty. Report-back states the check row by row.
6. **Demo scenarios** (new heading, before Error scenarios), about 110 words, four numbered steps, each one sentence
   plus the command or page:
   - Step 1, the solution is online: the five recorded scenarios on the replay site, every step with its clause,
     page and words (`docs/replay/index.html`).
   - Step 2, the subscriber asks why: `python -m onyx why <log> --step <n>` (built in 2 below) prints, in plain
     words and in both languages, the verdict, the clause relied on with its quote, and the hash of the event, so
     the explanation is the log, not a second opinion.
   - Step 3, conflicting advice: S3 step 3 as recorded: the care agent proposes sending identifiers to the hosted
     model provider abroad, the gate blocks under PDPL 22 and 23(2), the override request is refused (the log's
     `override_refused` event); the data goes only de-identified under the processor contract. Privacy wins by
     rule, not by the model's mood (`docs/replay/` S3 page, step 3).
   - Step 4, the same framework for another body with a different rule set: `onyx whatif` already replays a
     recorded run under a swapped rule (`docs/replay/whatif-S2-gap-1.md`). Add one more proposed rule for a second
     addressee, the Data Office's gap-4 deadline (item 3 below), and state the cost: a replay costs USD 0 and the gate
     decides in a median of 0.46 ms, against a live run's model spend (eval's per-run USD figure, quote the C5 mean
     per run from `eval`'s cost rows; print the figure the command prints, not a remembered one).
7. Error scenarios (unchanged S1 to S5 and Results).
8. Policy gaps and standards gaps derived from the mapping exercise. Add at the top, replacing the one-sentence
   "Found by absence" opener, a **method paragraph of about 80 words**: every scenario step was put to the gate; a
   step no clause answers returns insufficient evidence and logs a candidate; each candidate was then searched
   across the 32 UAE instruments in both languages, then the GCC regulations, then foreign law for a global
   example; a gap is claimed only when the register lists what was searched and found absent; the recorded runs
   re-find 5 of the 7 expected gaps on every run. Numbers from the register and C5 as printed; no new figure.
9. Limits and next steps (shortened if pages require; see Cuts).

### 2. `onyx why`, a plain-code explanation command

`python -m onyx why runs/c5/S3/run1.jsonl --step 3` (and `--lang ar`): reads the committed log, finds the step's
propose and gate events, prints: the verdict; the clause id, document title, page and the verbatim quote in the
chosen language (from `kb/chunks/`, the same source the gate used); the human it hands to if hold; the event hash.
No model call. Register it in `onyx/__main__.py` beside `whatif`. Tests: S3 step 3 prints `block`, cites PDPL 22 and
23(2), and the `override_refused` line; S2 step 3 prints `hold`/hand-over with CPR 26.7.2 in both languages; a step
with no gate event errors cleanly. One line in the README's commands list and on the site's `verify.html` or
`runs.html` page, whichever lists commands.

### 3. A second proposed rule, `onyx/data/proposed/gap-4.json`

Addressee UAE Data Office; the PDPL 18(4) human review answered within a stated time, the request moment recorded
(the register's gap-4 recommendation; the number is the Office's to set; use "value_basis" to say which existing
clock the placeholder borrows, as gap-1 does with T1(2a)). Arabic text written by the build and labelled "translation
by the team, not eye-checked" in the file. Replay `runs/c5/S4/run1.jsonl --rule gap-4`, page
`docs/replay/whatif-S4-gap-4.md`, same shape as the gap-1 page. Test: the held S4-4 or S4-5 step gains the clock;
nothing else changes verdict. If the S4 log has no step the rule reaches, stop and say so.

### 4. Pages, counts, copies

Word page check (`scripts/report_pages.ps1`) after each heading change; count check over every number the report
states; `docs/report.docx` rebuilt; hq copy `report-draft-2026-10-23.md` replaced with the new text; README demo
section gains the four steps in one short list; CHANGELOG; PR, no merge or tag until Iyas says so; report-back
`docs/report-back/2026-11-01-task-36-template-items.md`.

## Cuts, in this order, only until Word says 5 pages

1. Limits and next steps to two sentences (keys ours and hashed; humans scripted; the four next steps as a list of
   nouns).
2. The Recommendations paragraph under the gaps table: drop the parenthetical gap numbers' repeated text where the
   table already carries it; keep every addressee and every recommendation.
3. Results paragraph: drop the 95% interval sentence (it stays in `eval` output and the README).
4. Mapping table Readiness cells: shorten the quoted factor names to their numbers plus one phrase.
Never cut: a gap row, a scenario, a figure, a clause citation, the method paragraph, the four demo steps.

## Done means (show each output)

- `report_pages.ps1`: 5. Word count printed. Count check passes.
- Headings in `docs/report.md`, in order: Introduction; Description of the use case; What is the role played by
  AI?; Requirements; Mapping with ITU-T Y.3172, Readiness 2.0 Report, and domain-specific policies; Demo scenarios;
  Error scenarios; Policy gaps and standards gaps derived from the mapping exercise; Limits and next steps.
- `python -m onyx why runs/c5/S3/run1.jsonl --step 3` and `--lang ar`: output pasted in the report-back.
- `python -m onyx whatif runs/c5/S4/run1.jsonl --rule gap-4`: page exists, output pasted.
- `selftest` figures unchanged from the Task 35b report-back (C5 recall 0.96 / 1.00, citation 0.99 / 1.00).
- Full suite passes with the new tests; CI green.

## Limits

Seven layers: unchanged from Task 35b; `why` reads logs only (no prompt, no tool, no model), so nothing new ships or
is deferred. No run, no API call, no spend. No change to `gaps.json` rows, keys, prompts, gates, rules.json,
mandates.json. No new KB row. Sources rule: nothing fetched from the web. No wording that implies e& or du breaks a
law or its code. "Vishnu" and the template's example never appear in the repo.

## Stop and ask when

5 pages cannot be held after all four cuts (then show the page count and the two largest remaining sections; do not
cut a gap row or scenario on your own); the S4 log has no step the gap-4 rule reaches; a selftest figure moves; any
test outside the named ones fails; the `why` output for S2 step 3 does not cite CPR 26.7.2 in both languages.
