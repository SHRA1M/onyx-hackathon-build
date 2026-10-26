# Task 27: gap-12, where an agent's authority ends (hq, Fable, 2026-10-26)

Repo: `D:\Projects\engineering\onyx-hackathon-build`. **Base: `main` after the Task 26 merge** (name the commit; if
Task 26 is not merged, stop and say so). Branch `task-27`. No model calls, USD 0. Words and one kb document only.

Ruling: `D:\Projects\hq\uni\ai-for-good-hackathon\agentic-readiness-ruling-2026-10-26.md` (sections 2 to 4 hold
every quote and page). Read it first; copy quotes from the kb chunks, never from the ruling.

## Part A: Y.3173 into the kb

A1. Fetch ITU-T Y.3173 (02/2020) through the existing `kb fetch` path with URL
`https://www.itu.int/rec/dologin_pub.asp?lang=e&id=T-REC-Y.3173-202002-I!!PDF-E&type=items`. Expected sha256
`63f65c25f573779979e6580f16bc72aea86006c1a9d34f222a958d63df1f94dd`, 832,240 bytes, 34 pages. If the bytes differ,
stop and ask with the sha you got. A copy is at
`D:\Projects\hq\uni\ai-for-good-hackathon\standards-text\itu-t-y3173-2020-02.pdf` for the local fallback.
A2. Manifest row `itu-t-y3173`, modelled on `itu-t-y3172`: title "ITU-T Y.3173 (02/2020) Framework for evaluating
intelligence levels of future networks including IMT-2020", issuer ITU-T, status VERIFIED, binding_status as Y.3172's,
language en, source_type standard, country international. Chunk it as the other standards are chunked. Never commit a
manifest whose only change is a fetch date.

## Part B: the register (`onyx/data/gaps.json`; regenerate `docs/gaps.md`, the README table, `docs/site/gaps.html`)

B1. Add `gap-12` after `gap-11`, same keys as `gap-8`. `line`: "No metric for where an agent's authority ends".
`gap`, `kind` (absence), `category` (standards gap), `addressee` (["ITU"]), `uae_position`, `recommendation`,
`exposed_by` ("S1"), `competitor` ("no", basis: the 10-25 sweep found no rival row on ITU's own metrics): text from
ruling section 4, shortened only where the register's other rows are shorter.
B2. `searched`: one entry per clause the ruling cites, each with `clause`, `page`, `says`, `quote`. Readiness 2.0:
p. 12 (Basic Framework "Levels of automation [Y.3173]"), p. 23 (D5), p. 25 (D8), p. 27 (D9 inference-to-action
latency and decisions on AI alerts), p. 29 (D10 accountability remains with humans), p. 31 (D11 agents), p. 35 to 36
(chapter 4 gap list), p. 40 (REQ-027 NOTE), p. 47 (FAQ 11). Y.3173: 3.2.1, 6.1, 7.2 Table 7-1, Table 7-2 NOTE 1,
8.2, I.1 Table I.1 (SAE level 3 and level 4 wording). Every `quote` verbatim from the chunk; if a quote in the ruling
is not found verbatim in the chunk (pypdf spacing differs between extractors; Readiness p. 29 breaks
"accountabil-ity" across a line), use the chunk's spelling and say so in the report-back. If a quoted passage is not in any chunk at all, stop and ask, naming it.
B3. `standard_text`: the Y.3173 Table 7-2 NOTE 1 sentence and the two SAE sentences from Table I.1 (document
"ITU-T Y.3173 (02/2020)", clause and page, file, status VERIFIED). `global_examples`: the SAE level 3 and 4 wording
as reproduced in Y.3173 Table I.1; `global_none` unset.
B4. In `docs/gaps.md`, under gap-12, one sentence: found after the scored runs; S1's expected gaps and the keys are
unchanged, so C5 gap recall does not count it. The count line becomes 12 gaps.
B5. **Keys, scenarios, mandates, rules, runs, eval: untouched.**

## Part C: the report (`docs/report.md`, then `docs/report.docx`)

C1. One row in the gap table, after row 11:
`| 12 | Agent authority: Readiness 2.0 measures the human acting on an AI output (D9 inference-to-action latency) and Y.3173 grades L0 to L5 by who performs each step, a human's order having "the highest authority" (Table 7-2 NOTE 1); neither measures when an acting agent must stop, how often it hands over, or how long the hand-over takes; Y.3173 cites SAE J3016 and drops its fallback column | standards | ITU | SAE J3016 L3 "request to intervene", via Y.3173 Table I.1 |`
C2. Nothing else in the report changes. The report stays at 5 pages (Task 23 ruling). Render the docx and count
pages; if 6, stop and ask with the count and the overflow in lines. Do not cut anything to make room.
C3. Task 26's B1 to B3 text must be present in the base before this diff; `git diff <base> -- docs/report.md` must
show C1 only.

## Done means (hq checks; show each output)

1. `git diff --stat <base>` lists only: `kb/manifest.csv`, the Y.3173 source and chunk files, `onyx/data/gaps.json`,
   `docs/gaps.md`, `README.md` (table only), `docs/site/gaps.html` and `docs/site/kb.html` (and `index.html` if its
   manifest counts changed), `docs/report.md`, `docs/report.docx`, `CHANGELOG.md`, the filed order, the report-back.
2. `git diff <base> -- onyx/gate.py onyx/data/rules.json onyx/data/keys onyx/data/scenarios onyx/data/mandates.json
   onyx/eval.py runs/ eval/` prints nothing.
3. `kb verify`: 51 documents, 47 VERIFIED; the Y.3173 sha equals A1's.
4. Every `quote` in gap-12's `searched` and `standard_text` is found verbatim in its chunk (print the test name
   and count; write the test if the register tests do not already check quotes against chunks).
5. `python -m onyx site` twice; `git status --short docs/site` empty; `uv run pytest` count (404 plus any new).
6. Report page count after render: 5. CI green on the branch and on `main` after the merge; name the run.
7. Report-back at `docs/report-back/2026-10-26-task-27-gap-12-agentic-readiness.md`: what was built, every quote
   whose spelling changed from the ruling, anything left out, the time it took.

## Limits

- No model calls. No change to gates, rules, keys, scenarios, mandates, prompts, scorer, runs, eval, figures.
- No other entry's name in any tracked file.
- Stop and ask: a Y.3173 sha mismatch; a quote absent from every chunk; a sixth report page; Task 26 unmerged.
