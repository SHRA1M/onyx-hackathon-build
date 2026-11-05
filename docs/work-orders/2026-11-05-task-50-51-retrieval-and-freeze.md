# Tasks 50 and 51: retrieval measured, then the freeze items (hq, Fable, 2026-11-05)

For a build session, Opus, in `D:\Projects\engineering\onyx-hackathon-build`. Two tasks, in this order, each on its own branch with its own draft PR and report-back. Rulings behind every item: `D:\Projects\hq\uni\ai-for-good-hackathon\presentation-ruling-2026-11-05-fable.md` and `full-audit-2026-11-05-fable.md`; hq checked each fact below against main at 7de5b3f on 2026-11-05 and corrected two (items 51.E and 51.G). Decisions by Iyas, 2026-11-05: retrieval is fixed, starting now; the spend cap rises to USD 45; nothing else is cut.

**Start:** `git switch main`, `git pull` (the checkout was left on `task-49`; main is 7de5b3f, PR #18 merged, CI run 41933666672 green). Then correct `onyx-hackathon-build-background.md` and `onyx-hackathon-build-workingBrief.md`: Task 49 is merged at 7de5b3f, not waiting on a draft PR. Commit that on `task-50` as its first commit.

Allowed sources: the repo and this file. No web reads. No new knowledge-base row, no manifest change, nothing under `runs/`, `onyx/data/keys/`, `kb/chunks/`, `kb/manifest.csv`; no change to any gate, to the prompt text (`PROMPT_VERSION` stays `v5`, `tests/test_prompt_v5.py` untouched) or to any scenario or key. Never imply e& or du breaks a law or code. No em dashes in anything written.

Each task ends with a report-back under `docs/report-back/` in the Task 49 shape: differs from the order, done-means table with outputs, every changed line printed, `git diff --stat`, CI run id. The filed copy of this order under `docs/work-orders/` is the one extra file. hq checks the report-back against this file and merges on its own check; Iyas has handed that call to hq (2026-11-05).

---

## Task 50: why retrieval is low, and a hybrid retriever measured, not shipped

Branch `task-50` from main. Shown only; no scored run is touched. USD 0: no model call.

**Target, set before any measurement (Fable, 2026-11-05):** pooled recall@8 at least **0.40 English and 0.30 Arabic** for the hybrid retriever on the queries and targets already in `eval/retrieval.json` (the shipped embedder prints 0.24 en / 0.09 ar, intervals to 0.32 / 0.15). Met: hq writes Task 52, a re-record of C5 as C6 on the hybrid. Not met: the hybrid ships nowhere, its figures print as measured, and the submission goes with the current runs. Either way this task is complete when its figures are printed.

### 50.1 Diagnosis script (about 1 hour)

New `scripts/retrieval_diagnose.py`, read-only, no model. For every (query, must-cite clause) pair the shipped embedder missed in `eval/retrieval.json` (`shipped` lists against `retrieval.targets()`), print: query id and language; the clause; its `document_id`; whether the chunk holds Arabic text (`text_ar` non-empty); the chunk's word count; the rank the chunk did reach in the shipped index (re-query the local shipped Chroma collection for the full ranking within the same scope as the measurement; if the local index is not built, build it with `kb ingest` first, and say so). Then three grouped counts, English and Arabic apart: misses whose chunk has no Arabic text; misses whose query and chunk share no token after normalisation and a short stopword list; misses that sit at ranks 9 to 30 behind chunks of the same document. Last line: BM25 recall@8 en and ar on the same queries and targets, with the normalisation of 50.2. All of it goes in the report-back as tables; the script is committed; nothing under `eval/` changes in this step.

The diagnosis Fable wrote without measuring, for the build to confirm or refute: (1) the query is the subscriber's lay sentence and the target is a statute clause, often procedural; (2) 84 of the 161 chunks have no Arabic text (hq counted: 72 both, 84 English only, 5 Arabic only) and `all-MiniLM-L6-v2` is English-only, so Arabic is near the floor; (3) 71 of 161 chunks are CPR paragraphs close in wording; (4) chunk sizes run 10 to 5,946 words. State for each: supported, not supported, or not testable, with the number.

### 50.2 Hybrid retriever and the measurement (about 4 to 5 hours)

In `onyx/retrieval.py`: `normalize_ar()` (alef variants to bare alef, taa marbuta to haa, alef maqsura to yaa, strip diacritics and tatweel), `tokenize()` (lowercase, split on non-letters, apply `normalize_ar`), a plain-code BM25 (Okapi, k1 1.5, b 0.75) over `text_en` and `text_ar` as two fields of one document, no new dependency. In `onyx/agents/base.py`, beside `ChromaRetriever`: `HybridRetriever`, the same `Retriever` protocol, the same signature, **the same mandate scope filter per agent as `ChromaRetriever`** (scope is part of `inputs_hash()`; a scope change is a stop), reciprocal rank fusion (k 60) of BM25 top 30 and dense top 30 from a bilingual index, returning the top 8 in the shipped shape. Dense indexes: `build_bilingual` for `intfloat/multilingual-e5-base` and `BAAI/bge-m3`, both already in `MODELS`, under the existing 30-minute build limit each; if one cannot build on this PC inside the limit, measure with the other and say so.

Measure with `measure()` and record in `eval/retrieval.json`, each under its own name, each marked "not used in any scored run": `bm25`, `e5-base`, `bge-m3`, `hybrid-e5-base`, `hybrid-bge-m3`. `onyx/eval.py` `retrieval_results` and `_retrieval_lines` print every recorded name as its own `###` under "Retrieval alone", same table, same interval, and one line under the heading: "Target set 2026-11-05 before measurement: pooled recall@8 at least 0.40 en and 0.30 ar; <name>: met / not met." `inputs_sha256` must not change (chunks, queries and scope are the same).

A `--retriever` option on `run` (`shipped` default, `hybrid-e5-base`, `hybrid-bge-m3`), and the retriever's name in the `run_start` event beside `retrieval="kb_main"` as a new optional field; every existing log must still verify (CI's 228 logs: chain ok). No run is made in this task.

### 50.3 The cap

`onyx/cost.py` line 35: `TOTAL_CAP_USD = 45  # Iyas raised it 2026-11-05 for the C6 re-record (Task 50); was 30 from 2026-10-27`. Pins: `tests/test_cost.py` lines 120, 161 to 162, 217 (the 30 figures). Print the recorded spend with `cost.spent_usd` on the `runs/` folder (the root `onyx/runs.py` line 98 uses) in the report-back, to two decimals.

### Done means, Task 50

1. The diagnosis tables and the four verdicts (50.1) in the report-back.
2. `eval/results.md` "Retrieval alone": the shipped section byte-identical to main's; the e5-small section unchanged; the new sections present, each with the target line. Paste the five pooled rows en / ar / both.
3. Nothing else in `eval/results.md` or `eval/results.json` moves: `git diff` of both shows only the retrieval block. `selftest`: "figures match a fresh eval of runs/". `check-data ok`.
4. Full suite passes; name every test whose pin changed and every test added (at least: hybrid returns the top 8 in the shipped shape within scope; `normalize_ar` on the six cases above; the target line prints).
5. `git diff --stat`: only `onyx/retrieval.py`, `onyx/agents/base.py`, `onyx/eval.py`, `onyx/__main__.py`, `onyx/cost.py`, `scripts/retrieval_diagnose.py`, `eval/retrieval.json`, `eval/results.md`, `eval/results.json`, tests, `CHANGELOG.md`, the two folder files from Start, the report-back, the filed order. Site pages only if `site` renders retrieval figures (say which).
6. Recorded spend printed. The cap line printed.
7. CI "reproduce" green on the head commit; run id.

### Stop and ask, Task 50

`inputs_sha256` changes. The shipped section's figures change. A protected path changes. A test outside the named ones pins something this task moves. The hybrid cannot keep the per-agent scope filter in the same place as `ChromaRetriever`. The build thinks a dependency is needed. Any model call would be made.

---

## Task 51: the freeze items (presentation, audit, screenshots, Figure 2, unseen bank)

Branch `task-51` from main after Task 50 merges; if Task 50 is still open when Task 51 starts, branch from main and rebase before CI. Text, pictures and the site generator only. Freeze for everything in this task: 2026-11-06.

`docs/gaps.md`, the README gap table and `docs/site/*` are generated: edit `onyx/data/gaps.json`, `onyx/gaps.py`, `onyx/site.py`, then regenerate (`gaps`, `site`, the report build `docs/build_report.py`, `scripts/report_pdf.ps1`). Every report change ends with `scripts/report_pages.ps1`: the main text stays **5 pages**, page 5 ends with the last sentence of "Limits and next steps" ("...further gaps and candidates." on main), annex from page 6; print total pages and whether 12 moved.

### 51.A Audit items (Fable, 2026-11-05; hq confirmed each string on main)

1. `docs/.nojekyll`, empty; `docs/index.html`, a plain redirect to `site/`. `onyx/site.py`: the two links in `docs/site/runs.html` to `../replay/whatif-S2-gap-1.md` (line 601 on main) and `../replay/model-down-S2.md` (line 634) point at `whatif.html` and `modeldown.html` (line 88 already does). Confirm no other `../replay/*.md` link remains under `docs/site/` (`git grep`).
2. Report header, `docs/report.md` line 7. On main: `**Knowledge base:** ... **Demo video:** \`docs/video/mizan-demo.mp4\` there (file lands 2026-11-08). **Replay site, no install:** <url>`. Becomes: `**Replay site, no install:** <the same url>. **Demo video:** see the repository README.` The knowledge-base pointers stay in the README reviewer table (row 1 names `kb/manifest.csv` and `kb/DATASHEET.md`; confirm, else keep them in the header). No future tense anywhere on page 1. Pins: `tests/test_report.py` lines 66 to 68 (header labels and the video paragraph) and 460. The URL itself goes in on 2026-11-08 by the submission-day order, with the tag and the "public from" parenthetical.
3. `onyx/gaps.py` line 54 `COMPANION_LINE`: `The 2025 to 2026 US statutes on chatbots regulate companions and carve out customer service.` becomes `The 2025 to 2026 US companion-chatbot statutes regulate companions and carve out customer service.` Pin: `tests/test_gaps.py` line 1153.
4. Gap 13: `onyx/data/gaps.json` line 510 `so no period exists in any published federal text` and `docs/annex.md` line 290 `so no published federal text sets a period` both become `so no period is in any federal text on the official portal (checked 2026-11-02 and 2026-11-04)`.
5. `docs/annex.md`: headings `**F.2 Gap 13`, `**F.2 Gap 14`, `**F.2 Gap 15`, `**F.3 Candidates`, `**F.4 Searched` renumber to F.2, F.3, F.4, F.5, F.6. Pin: `tests/test_annex.py` lines 308 to 309. Any cross-reference to F.3 or F.4 in the report, annex or README follows (`git grep -E 'F\.[2-4]'`).
6. README reviewer table, row "Knowledge base", Evidence cell: append `; the running system shows the model 186 of 234 key clauses in English and 166 in Arabic (mandate list first); the embedder alone finds 0.24 / 0.09 at top 8` (figures: `eval/results.md` lines 189 to 190 and the shipped Retrieval alone pooled rows; copy the printed fractions).
7. Report line 78 `Claimed on running evidence: 6, 7, 8, 10, 11; on documents only: 1, 13; not claimed: six.`: no table row names 1 or 13. Add to the SRC row's third cell `; and 1 <name>, on documents only` and to the MLFO row `; and 13 <name>, on documents only`, names copied from the Readiness 2.0 report text held in the knowledge base (its chunk file or source on disk). If the dimension list is not in the repo, add the numbers without names and change the sentence to `on documents only: 1 and 13 (SRC and MLFO rows)`.
8. Report line 146, gap 11: `an OTP per purchase (4.23.2)` becomes `2FA per purchase (4.23.2; OTP by default, 4.11)` (hq read both chunks: 4.23.2 says "a 2FA procedure", 4.11 makes OTP the default 2FA method).
9. README lines 44 to 45: `No source on file says what stops such an AI when a chat becomes a complaint or a disconnection. The binding texts do, and Mizan's gates are written from them.` becomes `The public page does not say what the assistant does when a chat becomes a complaint; the binding texts do, and Mizan's gates are written from them.` Pin: `tests/test_pages_grounding_readme.py` lines 168 to 169. Report line 15: `The binding texts bar such an AI from charging` becomes `The binding texts bar any AI in that seat from charging` (hq's ruling on the intro sentence: the facts stay, the pairing with e& goes).

### 51.B Report page 1: five figures above the fold (about 1.5 hours)

Directly under the header block, before "## Introduction", a one-row, five-cell table, no heading. Cells, each a figure already printed in the main text (the build confirms each by `grep` and adds one assertion to `tests/test_report.py` that every strip string occurs elsewhere in `docs/report.md` before "Annex"):
`5 scenarios, 2 languages, 20 recorded runs` | `108 documents, 100 verified` | `action recall 0.96 en / 1.00 ar (110 of 112 key steps)` | `citation validity 0.99 / 1.00` | `expected gaps found 5 of 7 in every run`.
Pay for the lines: the header line 7 shortening (51.A.2) and the third Introduction paragraph (lines 21 to 25 on main, the sources list that Annex A carries): cut to its first sentence plus `100 are verified: the issuing body's file is on disk with its SHA-256, and a test on every push checks each clause the gates cite word for word against the text stored from it. No consumer data was used.` Every text named in the cut sentence must still be named in Annex A (confirm by grep). Body stays 5 pages or stop.

### 51.C Controversy, ITU's word (about 0.5 hours)

The template asks scenarios to discuss "the situations where the solution might face controversy"; the word is in no file of ours (`git grep -i controvers` on README, report, annex: 0). Annex C, the "Reading it" paragraph (line 185): after `...passes the conversation to a named human.` insert `That is the controversy case: governance looks slower, because the ungoverned run reaches the subscriber's "yes" first and charges on it.` The next sentence (hand-over latency 0 steps in S2, S4, S5) already answers it; leave it. Report line 90, S3's line: `3. Conflicting advice:` becomes `3. Conflicting advice, the controversy case:` if page 5 holds; if not, leave the report and say so.

### 51.D README first screen (about 1 hour)

New order of the top: title; badge; synthetic notice; one line, new: `Mizan is a consumer-care AI for a synthetic UAE operator: agents propose each step of a chat or call, plain-code gates written from binding UAE clauses allow or block it, in Arabic and English, and every step is replayable from a hash-chained log.`; `## For the reviewer` (table unchanged except 51.A.6); `## Three things to look at first` moved up whole (its screenshot stays its first line, `tests/test_figures.py` 153 to 154 then needs no change); new `## What Mizan is` holding, in this order, the long paragraph (line 21 on main), a team table, the annex line (line 19) and the knowledge-base paragraph (lines 28 to 34) with its sentence of nested parentheses split into two sentences and the `Knowledge base: ` lead kept (pins read it: `tests/test_pages_grounding_readme.py` 303, `tests/test_report.py` 417); then `## Why` and the rest unchanged. Team table replaces line 26:

| Team | Members | Affiliation |
|---|---|---|
| Onyx | Iyas Shraim (leader), Mohammed Rawashdeh, Yanal Faouri | Al-Balqa Applied University, Faculty of AI, students |

No mentor line, no reviewer line (added only when a written yes exists). Heading-order pins to update: `tests/test_gaps.py` 116 and `tests/test_pages_grounding_readme.py` 225 (`headings[:5]` becomes `["For the reviewer", "Three things to look at first", "What Mizan is", "Why", "Gap register"]`); `_section("Three things to look at first")` at 217 must still find its three items. No video placeholder: "Demo video: <URL>" is added on 2026-11-08.

### 51.E Screenshots are stale (hq found, 2026-11-05)

`docs/site/screenshots/index.png` (README line 128, "the C5 and C3 figures, read from eval/results.json") shows 50 documents / 46 VERIFIED, action recall 0.94 Arabic, "10 runs per language"; the site and report on main say 108 / 100, 1.00, two runs per scenario per language. A judge who reads the README sees two sets of numbers. Re-take every committed screenshot from the current pages the way Task 25 did (headless Chrome from `file://`, same viewport, no new dependency): `docs/site/screenshots/index.png`, `verify.png`, `replay-S2-step5-elsewhere.png`, `replay-S3-step3-elsewhere.png`, `docs/replay/screenshots/S2-step3-en.png`, `S2-step3-ar.png`. Open each new PNG and state in the report-back what it shows (index: 108 / 100 / 5 / 3 and the C5 table with 1.00 ar). The site tiles themselves are right on main (`onyx/site.py` counts the manifest); no label change.

### 51.F Figure 2 restyle (about 1 hour; keep, Iyas 2026-11-05)

`scripts/fig_results.py`: `FONT` 9, no hatching (solid fill for the first series, outlined white fill for the second), legends below their panels (`loc="upper center"`, `bbox_to_anchor` under the axes, two columns), titles above with no overlap. Same data, same numbers, same width; height may grow. Re-render `docs/fig/fig2-results.svg` and `.png`, rebuild the report, page check. If the body leaves 5 pages, reduce `FONT` to 8 before cutting anything; if still over, revert this item and say so.

### 51.G The unseen bank, listed (about 0.5 hours)

README "Scenarios" section, after the line on the seven unseen scenarios (line 147), a table: id, `title_en`, `title_ar` from `onyx/data/scenarios/unseen/U*.json`, and one line under it: `No key exists for them and none has been run; their cold runs are a next step.` The same table on `docs/site/runs.html` through `onyx/site.py`. Nothing anywhere says a judge can type a live step: hq checked that no file on main offers one, and this order adds none.

### Done means, Task 51

1. Each "first" or "confirm" check above, with output: the `.md` link grep, the knowledge-base pointer grep, the strip-string greps, the Annex A names grep, the F-number grep, the Readiness names source.
2. `git grep` for each old string: hits only in `docs/report-back/`, `docs/work-orders/`, `docs/sources/` and archive files.
3. Page script: 5 main pages, the page-5 ending, annex from page 6, total pages; `scripts/report_pdf.ps1`: Word and PDF page counts equal; `scripts/check_pdf.py` passes. The PDF's page 1 holds the strip and no future-tense line (print page 1's text).
4. Full suite passes; every pin changed named with its line; tests added named.
5. `kb verify`, `check-data`, `selftest`: 108 / 100 / 5 / 3; 161 chunks; "figures match a fresh eval of runs/".
6. CI "reproduce" green (the site regenerates byte for byte in CI; the screenshots are not generated, so they pass as files); run id.
7. `git diff --stat`: only `README.md`, `docs/report.md`, `docs/annex.md`, `docs/.nojekyll`, `docs/index.html`, `onyx/gaps.py`, `onyx/data/gaps.json`, `onyx/site.py`, `scripts/fig_results.py`, `docs/fig/*`, the six screenshots, what regenerates (`docs/gaps.md`, `docs/site/*`, `docs/report.docx`, `docs/report.pdf`), tests, `CHANGELOG.md`, the report-back, the filed order. Nothing under `runs/`, `kb/`, `onyx/data/keys/`, no gate, no prompt.
8. Every changed line printed as it stands, screenshots described.

### Stop and ask, Task 51

The main text leaves 5 pages after 51.B, 51.C or 51.F and the fallbacks above do not bring it back. Page 5 no longer ends with the Limits sentence. A strip figure is not already printed in the main text. A test pins a figure or a clause this order does not name. A string above is found a different number of times than stated. Any screenshot cannot be re-taken without a new dependency. Anything would touch a run, key, chunk, gate or prompt.

---

## Limits, the seven layers (both tasks)

Versioned prompt: shipped, v5, untouched. Grounding: shipped; Task 50 adds a second retriever behind the same protocol and scope, default off, in no scored run. Gated tools: shipped, untouched. Asker's identity: deferred (Fable, 2026-10-29; no one outside the team reaches the model before the shortlist). Injection defence and masking: defence shipped and untouched; masking deferred (same ruling). Cost cap and router: cap shipped and raised to 45 here; router deferred. Trace and evals: shipped; Task 50's `run_start` field is additive and every existing log must still verify. No eval rerun owed by either task: no prompt, gate, key or scored run changes.

## After these two tasks (hq writes, not the build)

Task 52, only if Task 50's hybrid met the target: re-record C5 as C6 under `runs/c6/` on the hybrid, same prompt v5, keys, gates, model, two runs per scenario per language, about USD 6 to 8; C5 kept; C6 replaces C5 as the scored run only if action recall, citation validity and expected gaps hold or rise (C5: 0.96 / 1.00, 0.99 / 1.00, 5 of 7) and key clauses shown rises; then the report, annex, README, site, replay pages and tests move with one disclosure sentence in Annex A. Retrieval-only freeze 2026-11-08 12:00 Amman. Submission-day order by 2026-11-08: header URL and tag, "public from" parenthetical out, README video line, cold runs of U1 to U7 if time, the brief's list.
