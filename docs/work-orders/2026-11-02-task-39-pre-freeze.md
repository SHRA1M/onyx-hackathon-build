# Work order: Task 39, the pre-freeze changes from the 11-02 rival sweep (2026-11-02, hq on Fable)

Model for the build: Opus 5.5. Repo `D:\Projects\engineering\onyx-hackathon-build`, branch `task-36` (PR #13 carries
36, 37, 38; Task 38 is committed locally, not pushed). Build this order; do not re-decide it. About 6 hours. Done
before 2026-11-06; item E has its own deadline, 2026-11-04 end of day.

Source: `D:\Projects\hq\uni\ai-for-good-hackathon\rival-sweep-2026-11-02.md` sections 6 and 8. Iyas confirms the item
list before the build starts; an item he strikes is skipped and listed as "not built, Iyas's call" in the report-back.

## Why, in one line each

A. Task 38 stop 2 is answered: the annex states a number the repo does not print. B. Two rivals print a retrieval
figure and we print none, although every log already holds what is needed. C. The judge's first screen should say how
to check each criterion, not only where to look. D. The one question every judge asks of a gate, "does it slow the
subscriber", is answered by a row we already compute. E. The annex says the model is swappable and would run
in-country; a recorded local run is the proof, and the direct answer to the ITU reviewer's model question.

## Task

**A. Task 38 stop 2.** In `docs/annex.md` Annex B item 2, "the 17 verbs the agents may propose" becomes "the 16 verbs
the agents may propose". Same change in the hq copy `D:\Projects\hq\uni\ai-for-good-hackathon\report-annex-2026-11-02.md`
(write it if Task 38 did not) and in `task-38-annex-text-2026-11-02.md` v3, marked "(16: repo count, Task 39)".
Rebuild `docs/report.docx` and `docs/report.pdf`; the page counts must not change. Push `task-36`; CI on PR #13 must be
green before B starts.

**B. Retrieval coverage of the key clauses, from the recorded logs.** No model call. In `eval` add one row per
scenario and language, "Key clauses shown", computed over the C5 runs: for each step, each clause id in the key's
`must_cite` for that step; it counts as shown if it is in that step's `sources_mandate` or `sources_used` (the agent
of the step; if several agents act in one step, any of their events). Print three numbers per cell: shown of total,
the share shown by mandate only, the share shown only by retrieval (in `sources_used` and not in `sources_mandate`).
Also one pooled line per language. Append the definition to the `eval` definitions list in `eval/results.md` in the
same style as "hand-over latency". Then one sentence in Annex A, paragraph "Retrieval", after "so a reviewer can see
exactly what the model was shown.": "Over the scored runs, {build: N of M} key clauses were in what the model was
shown in English and {build: N of M} in Arabic; {build: share} came from the mandate list alone." Replace the braces
from the printed row; if the Arabic retrieval-only share is below the English one, add the clause "which is the
English-centred retriever at work, and why the mandate list comes first." Tests: the row is deterministic over the
committed logs; the sentence's numbers equal the printed row.

**C. README "For the reviewer" as a check table.** Replace the four numbered lines with a table of four rows:
criterion (the event page's wording, as the README already uses it), evidence (the file or page), how to check it
(one command or one link). Every command named must exist in `python -m onyx --help`; every path must exist. The
annex pointer line stays under the table. No new figure; counts already on the first screen may be repeated there.

**D. Annex C, "Reading it".** After "and it does so in both languages.", add two sentences: "The cost of the gate is
the hand-over: the governed run stops at the step the key marks and passes the conversation to a named human, and
the hand-over latency row in `eval/results.md` is {build: value} steps in every scored run. The subscriber is served
by a person at that step instead of charged by a machine." Fill the brace from the C5 hand-over latency cells; if
they are not all equal, write the range and drop "in every scored run". Re-run `scripts/report_pages.ps1`: the main
text stays 5 pages, the annex may not pass page 10.

**E. The local-model demo, bounded.** One scenario, S2, English, on a small open model on this PC through the
existing adapter, shown and never scored.
1. Install Ollama with `winget install Ollama.Ollama` (if winget asks for an elevation prompt, stop and hand Iyas the
   one step); pull `qwen3:8b` (if it does not fit the 12 GB GPU, the next smaller Qwen3 tag; record which). Confirm
   `curl http://localhost:11434/v1/models` lists it.
2. Run S2 English once with `ONYX_MODEL_BASE_URL=http://localhost:11434/v1`, `ONYX_MODEL=<tag>`,
   `ONYX_MODEL_API_KEY=ollama`, output under `runs/demo-local/S2/en/`, prompt v5 unchanged, no gate change, no key
   change. The adapter's `max_tokens` and JSON mode are left as they are; if the endpoint rejects a parameter, stop
   and report the exact error, do not edit the adapter.
3. `verify-log` on the run. `eval` must ignore `runs/demo-local/` (a test proves the C5 figures are unchanged).
4. One page `docs/site/localmodel.html` beside `modeldown.html`: the model tag, the machine (GPU and RAM as printed
   by the build), the run's steps with verdicts and clauses from the log, and the label "A demo of the adapter, not
   of quality: this run is not scored and is not compared with the report's figures." No figure of any kind on the
   page, in the README line or in the annex sentence: no score, count, rate, timing or comparison with the scored
   model (Iyas, 2026-11-02). Groq or any other hosted provider is not a substitute: the demo must run on this PC
   (Iyas asked, Opus answered 2026-11-02: a hosted provider abroad does not show local running). One README line under
   "Model". One sentence in Annex A after "nothing else in Mizan changes, because the gates, not the model, hold the
   law.": "A recorded run of S2 on {build: tag} through Ollama on a desktop GPU is in `runs/demo-local/`, shown in
   `docs/site/localmodel.html` and not scored." Arabic S2 only if the English run completes with every step decided.
5. Stop and drop if Ollama cannot load the model, or more than half of the steps return no parseable proposal; then
   the report-back records "tried on 2026-11-0N, not shown", the page and sentences are not written, and nothing
   remains in the repo but the report-back.

## Done means (show each output)

1. A: `grep -c "17 verbs" docs/annex.md` prints 0; `report_pages.ps1` prints `pages: 5`, `annex starts on page: 6`,
   `total pages: 10`; PR #13 CI green.
2. B: the `eval` row printed for S1 to S5, en and ar, and the pooled line; the Annex A sentence with its numbers
   beside the row; `uv run pytest` green with the new tests.
3. C: the table rendered in the README; every command in it run once with its first output line shown.
4. D: the two sentences and the C5 cells they come from; `report_pages.ps1` output.
5. E: `curl .../v1/models` output; the run's `verify-log` output; `eval` figures before and after identical (diff of
   `eval/results.md` empty); the page opened in Chrome (screenshot path); or the "tried, not shown" record.
6. Full suite green; CI green on PR #13; `docs/report.pdf` rebuilt, page count printed, "Annex A" found.

## Limits

No change to any scored figure, gap, rule, key, prompt, gate, mandate or scenario. No paid API call; E spends 0 USD.
No wording that implies e& or du breaks a law or code. No merge, no tag. Seven layers: versioned prompt unchanged
(v5); grounding unchanged; gated tools unchanged; identity deferred (post-shortlist, 10-29 ruling); injection
defence and masking deferred (post-shortlist; synthetic data only); cost cap unchanged (`TOTAL_CAP_USD` 30; E runs
outside it, local); trace and evals: every E event goes through the same hash-chained log and `verify-log`, and B
adds an eval row with a test. Nothing in E reaches anyone outside the team.

## Stop and ask when

The main text goes past 5 pages or the annex past 10 (show the lines; cut nothing); a C5 hand-over latency cell is
not a number; the key-clause row shows a step whose must-cite clause was never shown to the model in a run that
still scored a hit (name it: that is a finding, not a bug to hide); winget needs elevation; the local model's run
would need any change to the adapter, the prompt or a gate; any test outside the named ones fails; the clock
reaches 2026-11-04 end of day with E not green.
