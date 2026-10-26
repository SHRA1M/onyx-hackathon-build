# onyx-hackathon-build: archive

## 2026-10-20: Repo set up, Tasks 1 and 2, Task 3 rules and mandates

Copied the hq order over the local one (sha256 b88fa014...818da, identical) and filed it. git init, private remote SHRA1M/onyx-hackathon-build. Task 1 scaffold test-first. Task 2: manifest of 40 rows built from the hq notes; live fetch matched 12 documents byte for byte (TDRA, IMDA, ITU Readiness); the legislation portal 403s, so those fall back to hq copies. Chunker: decimal clauses (CPR, licence, policies) and Articles with numbered paragraphs (laws); 2,184 clauses from 19 documents, every clause the rule list needs present. Tried and fixed: Y.3172 headings without dots and a footer glued to clause numbers; a cover line read as clause 1.0; the dimensions.json URL (short sha and wrong path gave 404). Task 3: 92 rules and 16 mandate verbs, all quotes verbatim on first run; a mutation test confirmed check-data fails on an altered quote. CI green on a clean runner. Iyas then decided to cut the chunks back to cited ones with a history rewrite, and to use the hq transcription for Decision 16/2026 4.17 and 4.18; session wrapped at 311k context before doing either.

## 2026-10-21: Chunks cut to cited clauses, history rewritten, Decision 16/2026 extract

Done items 1 and 2 of the brief. `kb chunk` now writes every clause to `kb/chunks-full/` (gitignored) and only the clauses rules and mandates cite to `kb/chunks/`: 93 of 2,186 (91 cited before, plus Decision 16/2026 4.17 and 4.18). The rebuild reproduced all 2,184 old clauses byte for byte. History rewritten with `git filter-branch` on 627efec..main (each kb/chunks file cut to the same 93 clauses; nothing else changed in any commit; tip tree identical); `refs/original` dropped, reflog expired, gc; force-pushed main and backup/main (backup had held the full chunks). A safety bundle of the old history was kept only in the session scratchpad. Tried: the first filter run failed on Git Bash path conversion (C: paths); the first gc left the old objects because the remote-tracking refs still pointed at them; second gc after the push removed them. Decision 16/2026: the two quotes copied byte for byte from hq `tdra-and-licences.md` line 194 into `kb/extracts/decision-16-2026-ar.txt`, page 10 (from the PDF text layer, where 4.15 to 4.22 sit); could not check them against the page image (no PDF renderer on this machine). `check-data` matches an Arabic-only document's quote against `text_ar`. 11 manifest URLs filled from hq `kb-missing-urls-2026-10-20.md`. `kb fetch` prints the URL and target file for every row it cannot get. Clean clone without the hq folder: fetch, verify, check-data ok, pytest 18 passed 1 skipped. CI green on 1a39414 and 4411a27.

## 2026-10-21: Checked Arabic texts, transcription rule, lam-alef fix

Decision 16/2026: the extract now copies hq `decision-16-2026-ar-4.17-4.18-checked.txt` (Iyas by eye against the PDF); the 2026-10-17 note had dropped the last sentence of 4.18 and run its dash items together. `read_extract` joins continuation lines. The 4.18 rule quotes the whole clause and covers both two-hour limits. New rule from Iyas: a quote from page images or scanned text needs an hq `-checked.txt`, and the KB text must come from it; `transcription` field on rules, `check-data` lists them. licence-9-1's Arabic was listed (text layer with lam-alef restored by hand), PENDING at first, then checked by Iyas (`licence-2-2026-ar-9.1-checked.txt`, page 22, "توفير ما يلزم من موظفين مدربين"); a paired extract fills `text_ar` of 9.1. Lam-alef: Iyas counted 25 of 52 Arabic chunks broken (the اإل/األ shape only); with اا, a lone ال and known words, 38. New test failed on 38, then the extractors compared on every Arabic PDF (broken count, whole document):

| Source | hq .txt | pypdf | PyMuPDF | pdfminer | pdfium | pdftotext |
|---|---|---|---|---|---|---|
| CPR v2 Arabic | 1417 | 0 | 1417 | 486 | 1401 | 0 |
| Licence 2/2026 | 519 | 1 | 519 | 179 | 511 | 0 |
| PDPL | - | 2 | 215 | 82 | 206 | 0 |
| Telecom Law | - | 136 | 824 | 531 | 820 | 130 |
| Cabinet 56/2024 | - | 3 | 97 | 45 | 85 | 1 |
| Cabinet 57/2024 | - | 95 | 132 | 117 | 156 | 94 |
| Spam Calls v4 | - | 1 | 521 | 243 | 549 | 232 |
| Child Digital Safety | - | 1 | 291 | 64 | 277 | 5 |
| Cybercrimes | - | 1 | 507 | 100 | 503 | 0 |
| Instructions 1/2014 | - | 0 | 83 | 49 | 81 | 0 |

E-Transactions, Consumer Law, Cabinet 66, Spam SMS and Decision 16 Arabic have no readable text layer (0 words). hq .txt equals PyMuPDF output exactly. CPR Arabic re-chunked from pypdf: same clause ids, English unchanged, 46 chunks changed; cpr-17-2 and cpr-26-7-2 `quote_ar` updated from the new chunks. Tried: `طالما` in the word list (a real word, removed); a sed edit that mangled the regex range (redone in Python). uv.lock committed. Commits 79e74fc, fb71bd7, 6ae7419, 5c020e8; CI green on each push. Tests 27 passed, 1 skipped (keys).

## 2026-10-21: Keys session (Fable): scenarios S1 to S5, answer keys, mandate clauses

Brought forward from 2026-10-23 (IEEE poster dropped). Sources rule from Iyas mid-session: project material only (kb/, onyx/data/, the order, hq notes), no web, no law from memory, stop on a missing fact. Done: five scenario files (EN and AR steps, facts only), five keys (verdict, must_cite rule ids, obligations, gaps, note per step; one abstention step each; hand-over step; ungoverned claims), `keys/HASHES.txt`, `scenarios/README.md`, three tests, `data.load_scenario/load_key`. 13 rules added so every key citation resolves to a committed chunk (cited clauses 93 to 104). Mandates: `order_restore` moved to CPR 26.11; three verbs widened; all notes now say confirmed. Tried: a `kb chunk` rebuild to pick up the new clauses; it dropped the licence document (splitter stops at 1.1.7 on the hq text), restored from git, logged as open. Not done: Iyas has not read the Arabic step text on a page. Checks run: check-data ok; pytest 31 passed, 0 skipped; sha256sum -c on HASHES.txt all OK; reversed lam-alef scan of scenario Arabic clean; 0 CRLF files.

## 2026-10-21: Keys after hq review, licence splitter, Task 4, quote audit (Opus)

Keys: four edits from the hq review (Fable) applied as written, re-hashed (S1, S2, S5 changed; S3, S4 unchanged), commit 7cb7900 pushed with the keys-session commit 457e006. Noted to Iyas once: the repo rule said keys are not edited after HASHES.txt is committed; done on his instruction, and the keys' 'frozen' line is now untrue (hq to reword).

Splitter: hq re-extracted the licence .txt with pypdf. Two causes found: a heading line now carries its Arabic title ('3.1 General 3.1 <Arabic>'), and the English pass dropped it as Arabic when the Arabic outweighed the English, so no clause after 2.2 was accepted; and pypdf writes no page markers, so every clause was page 1. Fixed test first (two tests, red then green): `_english_heading` keeps the English title, `page_lines(bare_page_numbers=True)` for the licence only (itu-t-y3172, IMDA, EU AI Act and GDPR also have no markers and stay as they were). First version left the Arabic title on English-heavy headings (9.1, 9.3); a third test assertion caught it. Rebuild: same 5 clauses and pages, Arabic unchanged, every other document byte-identical in chunks and chunks-full; 3 text differences remained (pur suant, billin g, 9.3 'the parties ... the Telecommunications Law'). PDF page 24 rendered with PyMuPDF: the PDF has both 'the'. Committed chunks kept; licence-9-3 quote flagged to hq. Commit 2a3af77.

Task 4: `onyx/audit.py`, 8 tests (chain verifies, one-byte edit caught at line 2, deleted line caught, run_start key hashes, order fields present, replay verbatim, replay refuses a broken chain, `verify-log` CLI). One test had a wrong line index, fixed in the test. Commit ec000e3. Both commits pushed by Iyas.

Quote audit (report only, nothing changed): 110 quotes (107 quote, 3 quote_ar) against pdftotext of the 13 source PDFs in kb/sources, whitespace collapsed only; the three transcribed quotes against the hq checked files. 97 found, 13 not: 8 layout only (licence Arabic column interleaved 3.4.1, 9.1, 9.2.4, 9.4.3; PDPL page footer 6(1)(b), 13(2)(g), 23(1)(a); CPR 17.2 Arabic bidi marks), 5 for hq (licence-9-3; cpr-4-7-3 and cpr-24-7 hyphen plus space, PDF pages 15 and 60 break the word at a line end; cpr-3-9-recordings and cpr-3-9-notices table cells interleaved). pdftotext is xpdf 4.00 here; its QoS output carried split surrogates, decoded with surrogatepass and replace. Key hq references: every file, section, gap and item resolves except 'hq plan, S2' (the words are in domain-problem-scores-2026-10-14.md section 3.1, Scenarios, S2, a file outside the order's sources table). Audit scripts and full table stayed in the session scratchpad. check-data ok; pytest 41 passed.

## 2026-10-21: Blind review of the answer keys (Fable, wrapped on Opus)

hq asked for a blind review, report only. All 28 steps decided from kb/ and onyx/data rules and mandates before the keys were opened; verdicts written to the session scratchpad first. Then compared. 27 of 28 match. Differ: S1 step 6 (review hold, key insufficient_evidence: all three 4.4 terms fail on the facts). Wrong citation: Cabinet 66/2023 34(3) in S4 steps 1, 4, 5 (conformity, not unilateral termination; 34(1) fits) and the 18(2)(a) reasoning in S4 step 4. Shape: S3 step 3 says no adequacy test in any VERIFIED text, but chunks-full holds PDPL 22(1) and 22(2); gate_outcome null on S1 step 6 and S2 step 5; receive_objection mandate lacks PDPL 17; S2 steps 3 and 4 share verb draft_reply. Nothing edited, nothing re-hashed, Task 5 not started. Report-back `docs/report-back/2026-10-21-blind-keys-review.md`.

## 2026-10-21: Keys freeze from hq, Task 5 built (Opus)

First freeze order arrived scrambled as a paste; asked for a file, then built hq `freeze-order-2026-10-21.md` (11 steps) and `-part2.md` (5 steps). The 22(1) chunk came from `kb chunk` with `ONYX_SOURCE_DIR` (hq extractions); the rebuild also brought 'pur suant' and 'billin g' back into licence 3.4.1 and 9.1, so the licence file was restored and only 9.3's two 'the' added by hand. CPR pages rendered with PyMuPDF in a throwaway uv env (page 60 for 24.7, PDF page 12 for the 3.9 table; both 3.9 quotes match). Keys re-hashed; freeze commit e8b17cb pushed. CHANGELOG entry 4cfce07 (three quote fixes; Iyas said five, the commit holds three). Task 5: tests first (failed on import), then `onyx/model.py` and `onyx/agents/`; 11 new tests, suite 52 passed, check-data ok; a MockModel run of S1 steps 1 and 2 logged the classification and a rejected order_restore, chain verifies. Commit 07416f4, pushed by Iyas. Superseded open items, now answered by the freeze:
- For hq (report-back 2026-10-21-keys-review-splitter-task4): the licence-9-3 quote; four more quotes not verbatim in the PDF text (cpr-4-7-3, cpr-24-7, cpr-3-9-recordings, cpr-3-9-notices); the keys' 'Never edited after HASHES.txt is committed' line, now untrue; the keys' 'hq plan, S2' reference, which no plan file holds.
- For hq (report-back 2026-10-21-blind-keys-review): S1 step 6 decidable from 4.4 (hold, not insufficient_evidence); Cabinet 66/2023 34(3) cited in S4 where 34(1) fits; S3 step 3 wording ignores PDPL 22(1) and 22(2) in chunks-full; gate_outcome null on S1 step 6 and S2 step 5; receive_objection lacks PDPL 17; S2 steps 3 and 4 share verb draft_reply. Keys unchanged until hq answers.

## 2026-10-21: Agent document sets (addendum 27) and Task 6, the gate (Opus)

From hq `task-6-order-2026-10-21.md`. Part A: `documents` lists per agent in mandates.json, written by a script from the order's lists and the manifest (every id checked in the manifest); `documents_of` reads them and raises on an unknown id (tried by monkeypatch, raised). Two tests failed first (17 citations outside the old verb-derived sets; IMDA exception missing), then passed. Suite 54, check-data ok, commit 13c02c6 pushed. Part B: tests first (import error), then `onyx/gate.py`. One test was wrong (it expected the account's '(synthetic)' report time; the step 3 fact overrides it), fixed in the test. A coverage run over the 19 key steps the tests use: every verdict equals the key; must_cite fully met except S3 step 3 and S4 step 4 (gate checks added from the keys' own obligations: 23(1)(a), 8(1), 13(2)(d),(g) on the block; 18(1), 18(2), 34(1) on the human review) and S4 step 5 (the adviser's searched list, left for Task 7). Telecom Law 72(2) not citable (no row, no chunk). Suite 102 passed, check-data ok, keys, rules and HASHES untouched, commit 4adbebb pushed. Superseded: the open question on agent document sets (answered by addendum 27) and the 34(3) question (built on 34(1)).

## 2026-10-21: Pending proposals (addendum 29) and Task 8 runs, replay, eval (Opus)

From hq `task-8-order-2026-10-21.md`. Part A: `pending_proposal` inserted into S1 step 6, S2 step 5, S3 step 3, S4 step 5, S5 step 4 by a script that edits only those lines (a json re-dump would have reflowed the files). Tests first (7 failed: no `pending`), then the coordinator path. The pending proposal cites no clause, so `decide` would answer insufficient_evidence; `gate.decide_pending` added (mandate, then the verb's gates, else deny-by-default hold). Reasons checked per step: S1 4.4 conditions, S2 deny by default, S3 identifiers abroad, S4 open 18(4) review, S5 unverified reporter. First ungoverned version logged a refused override on an allow; fixed so an override runs only on hold or block. The addendum-17 test in test_gate.py now runs the S3 coordinator. 137 passed, check-data ok, commit d4ec049 pushed.

Part B: endpoint facts from context7 (the claude-api skill has no page for the OpenAI-compatible endpoint): base URL, model id, and that temperature below 1 is a 400 on Claude 4.7+, which the adapter's temperature 0 would have hit on every call. Tests first (collection error), then `onyx/runs.py`, `onyx/eval.py`, timing fields. First addressee rule (any step sent by a human expects a human addressee) failed S5 step 5, where the human verifies and the block is for the subscriber; narrowed to draft_reply. Idempotence test caught an absolute runs path in results.json; made repo-relative. No `.env` on disk: `record --source live` stopped with exit 2, nothing written, no model call. 60 scripted runs and `eval/scripted/` committed. 148 passed, check-data ok, commit d85871d pushed.

## 2026-10-21: Task-8 live order, Part A (ninth session, Opus)

Filed hq's `task-8-live-order-2026-10-21.md` as `docs/work-orders/2026-10-21-task-8-live.md` (293ff7c). Built Part A (d3a4cb2): `onyx/cost.py`, `onyx/data/model_prices.json` (pricing page fetched through the claude-api skill's live-sources Pricing row, read 2026-10-21), per-run tokens and cost in eval, the spend guard in `record --source live`, `--modes` and `--max-usd`, "obligation proxy" label; 15 new tests, written first and seen failing; eval/scripted regenerated. Found while measuring prompts: the local ChromaDB index was stale after the last `kb chunk` (KeyError 'tdra-cpr-v2-en 19.2' on live retrieval); rebuilt with `kb ingest`. The order's estimate basis (median prompt tokens of the scripted runs) had no data: scripted replies carry no usage and their prompts are 2.4x smaller than live ones. Iyas chose live-shape prompts, and output tokens added once a live run is measured. A test first reached example.invalid because it did not stub the call (estimate under one cent, so the $15 check did not trip); fixed. No model call made; no money spent.

## 2026-10-21: Task-8 live order, Part B, the bake-off (tenth session, Opus)

hq's go with Iyas's key in `.env`. Committed hq's `scripts/set-model-key.ps1` (66e3c37). Added `python -m onyx selftest` (test first, then `onyx/selftest.py`). Ran the bake-off with `ONYX_MODEL` set per process, the three models in parallel. Haiku's first attempt died on run 2 on an SSL EOF; added adapter retries and `record --skip-existing` (tests first). Haiku and then Sonnet died on S5 step 6: the gate crashed on a free-text `args.deadline` ("three business days from 2026-10-19"); now blocked as a deadline not from rules.json (test case first). Three partial logs moved to `runs/bakeoff/_failed/`, kept for spend. Built `onyx/bakeoff.py` and `eval/bakeoff.md` (tests first). The first table showed Opus with 38 of 52 parse failures; reading the replies showed every one is `finish_reason: content_filter` (23 empty, 15 cut mid-sentence), so a "stopped by the endpoint" row was added. hq's rule stops: Opus fails JSON (20 of 26) and quotes (1 of 5) in Arabic. Checks: verify-log 33 ok, replay 30 of 30, bakeoff byte-identical twice, 176 passed, check-data ok, selftest ok. Spend USD 1.63. Commit 6ac1a21 pushed; report-back `2026-10-21-task8-bakeoff.md`. Superseded: "Part B waits for the key" and the untracked-script note.

## 2026-10-21: Task 8 Part C1 and C2 (prompt v2, Opus finding test, v2 bake-off)

- Filed hq's Part C order as `docs/work-orders/2026-10-21-task-8-part-c.md`.
- C1 (a8f4acb): prompt v2 in `onyx/agents/base.py` with the order's lines; mandate clauses first in every prompt, logged as `sources_mandate`; the gate counts mandate and retrieved clauses as given; adviser gets `onyx/data/gaps.json`; wire field `notes`. Eval "Must-cite given" column; eval/scripted identical except that column (checked by script). Replay of pre-v2 logs runs without mandate clauses, so all 30 bake-off logs still replay. 15 tests red then green; 193 passed.
- Departures reported: the order's "five candidate-* ids" (only `candidate-4-4-fixed-term-bundle` exists in the keys and hq); the bracketed `<INSUFFICIENT_EVIDENCE>` is accepted by parse_output; the replay switch.
- C2 (0e5f8a6): Opus S2 en and ar on v2, 0 of 10 content_filter stops (v1 8 of 10), USD 0.39 (over the item's 0.30 estimate: the guard uses v1 prompt sizes). Haiku v2 bake-off USD 0.05, then Sonnet one scenario at a time with a projected-cost check before each, USD 0.86. C2 USD 1.30 of 1.50. `eval/bakeoff.md` now holds v1 (d85871d) and v2 (a8f4acb) tables; `bakeoff --runs` dropped. 195 passed; 22 new logs verify and replay.
- Superseded: "No model chosen; hq decides" (Part B) is now hq's decision Sonnet; the Part A Part C cost estimate on Opus (about USD 5.5 for 60 runs) is replaced by Sonnet v2's USD 0.086 per run.
- `.env` model switched by a scratchpad script (one line, key never printed): Opus, Haiku, then Sonnet, left on Sonnet.

## 2026-10-21: Task 8 Part C2b, hq's citation rule, C3 scored run (twelfth wrap, Opus)

- C2b (bbc5497): checked that 10 of 10 Arabic v2 bake-off logs name the key's gap id in the adviser's notes. Prompt v3 gap line; `parse_output` collects exact register ids from an abstaining reply's notes; abstain events carry `gaps_source`; eval column "Gaps from notes"; pre-v3 logs replay without notes gaps; the ordered line under the v2 table. 9 tests failed first, then passed.
- C3 first pass: governed S1 to S3 (18 runs, USD 1.61) recorded scenario by scenario with a running comparison against the v2 bake-off. Stopped by the 0.1 rule after S3: Arabic citation validity 0.87 against 1.00. Cause: 7 of 9 failing proposals were Arabic flag_gap proposals citing nothing, which v3 asked for (bfbc171, report-back c2b-c3-stop).
- hq's rule (f8a7504): citation validity leaves out a flag_gap citing nothing; new shown-only column; live results show both ways for S1 to S3; bake-off tables keep the old definition (byte-identical).
- C3 resumed: a batch loop piped the stop check through `tail` and lost its exit code; stopped it by hand, partial S4 log moved to `runs/_failed/S4/`, restarted with the exit code captured. A self-set USD 1.50 headroom check paused before S5 ungoverned; recorded after, inside the cap. 60 runs, USD 5.27 of 6; README "Model" section; report-back c3 (7b13260).
- Superseded: the C2 line "the finding paragraph names `reasoning_chain` as the trigger" (hq corrected it: cause not isolated).

## 2026-10-21: Task 8 Part C4, items 1 to 4 and the stopped run (thirteenth wrap, Opus)

- Filed hq's C4 order and the C3 miss analysis in `docs/work-orders/`. Tests first (`tests/test_prompt_v4.py`, 7 failed); the complaint-gate test passed before any change (the gate already allowed a care draft for a named human). Built the corrected addressee rule, care's three v4 lines, care mandate widened from gate.py (chunks added: propose_sale 56, propose_change 55, disclose_account 29, draft_reply 25; all inside care's document set), `prompt: v4` on run_start (the order said "as now"; it was not logged before), replay from recorded `sources_mandate`. `test_prompt_v2` fixture moved from CPR 3.3 to 26.6 (3.3 is now a mandate clause). 217 passed, check-data ok, selftest ok, bake-off byte-identical, eval twice same bytes, 112 live logs replay. Commit 359a498.
- Estimate before any call: governed batch USD 7.68 (en 3.34, ar 4.34) against the USD 6 cap; stopped and asked. Iyas chose governed only, 2 runs per cell.
- C4 S1 recorded (4 runs, USD 1.31; total USD 9.50). 0.1 rule tripped: S1 en citation validity 0.87 vs 1.00, a mangled document id on S1 step 3 in both runs. Action recall S1 en 1.00, ar 1.00 (C3 0.61, 0.67). Stopped; commit 17a1f14. Nothing pushed.

## 2026-10-21: Task 8 Part C4 addendum and C4 batch (fourteenth wrap, Opus)

hq's addendum after the C4 S1 stop (filed `docs/work-orders/2026-10-21-task-8-part-c4-addendum.md`). Built `gate.resolve_ids`, used by `decide` and by the eval's citation validity; gate events record `{cited, resolved}`; run_start logs `clause_resolution: true` and older logs replay without it (176 checked). Tests first: 8 of 9 red, then green; 226 pass; check-data, selftest, eval twice same bytes, bake-off byte-identical (e8fef52). hq's line said "4 of 341 citations"; the logs show 6 ids (C4 S1 also cites 5(7) bare) in 4 of 389 proposals citing a clause; Iyas chose the logs' figures. S1 en under the new scoring 1.00 = C3, so the run resumed with Iyas's go: S2 to S5 governed, 2 runs per cell, one at a time with a spend and 0.1 check after each (S2 1.08, S3 1.01, S4 1.05, S5 0.82; S5 estimated 1.13 to 1.32 from C3 cost ratios before running). No scenario skipped, no stop rule hit. The gate resolved `spam-calls-v4:10.2` and `:15.4` live on S3-5 in all 4 runs. Iyas's C4 wording added to results.md; report-back written and trimmed to 29 lines; pushed 48d191d.

Moved from the background (least current decisions):
- 2026-10-20: MIT licence holder Iyas Shraim; README credits Team Onyx only (member spellings unconfirmed).
- 2026-10-20: one column `jurisdiction` in {UAE, foreign, international}; `jurisdiction_level` dropped (addendum 13).
- 2026-10-20: Cybercrimes 34/2021 is a VERIFIED, binding, UAE row.
- 2026-10-21: only cited clauses are committed; history rewritten and force-pushed, no commit holds the full chunks (Iyas). Demo, eval and CI run on the cited clauses alone; a judge's search covers those only.
- 2026-10-21: `kb fetch` downloads what it can; for a blocked row it prints the URL and the `kb/sources/` file name to save by hand (Iyas).
- 2026-10-21: a quote from page images or scanned text is valid only if hq holds a `-checked.txt` for it, and the KB text must be copied from that file, never from the note the quote came from. Rules carry `transcription` {from, field, checked_file}; `check-data` lists them and marks one without a checked file PENDING (Iyas). Now: d16-4-17, d16-4-18, licence-9-1, none pending.
- 2026-10-21: Decision 16/2026 4.17 and 4.18 from hq `decision-16-2026-ar-4.17-4.18-checked.txt`; the 4.18 rule covers both two-hour limits (ours, and the other licensee's from receipt of our notice). 4.19 stays in `PENDING` (tests) and is never cited.
- 2026-10-21: `check-data` fails on a reversed lam-alef in any committed chunk (`ligature_problems`): only shapes correct Arabic never has (اا, اإل/األ, a lone ال) plus a list of broken words seen. No swap rule: a real لا is common (Iyas).
- 2026-10-21: an Arabic-only document's rule `quote` is Arabic and is matched against `text_ar`.
- 2026-10-21: the 11 URLs from hq `kb-missing-urls-2026-10-20.md` are portal landing pages, `url_accessed` 2026-10-20; the two UNVERIFIED rows stay empty.
- 2026-10-20: rules carry `clause` (the citation) and `chunk` (where the quote sits); CPR fn 35 is in chunk 24.11, QoS Annex A (T1(2a)) in 9.5.
- 2026-10-20: dimensions.json canonical bytes are upstream's (commit 6c6771c6, path simulation/data/framework/).

## 2026-10-21: Task 9, gap register and global examples

Built order `docs/work-orders/2026-10-21-task-9-gaps.md` (bafd4a3): `onyx/data/gaps.json` rewritten to 9 rows (gap-1 to gap-8, candidate-4-4) plus 4 candidates, `onyx/gaps.py` and `python -m onyx gaps` writing `docs/gaps.md` and the README register table (README reordered: Gap register, Model, Setup, Licence), `tests/test_gaps.py` (9 tests, failed first). Two eur-lex fetches by scrapling (a plain request got HTTP 202 and an empty body; the browser fetch returned the article): eIDAS 910/2014 Art 8 as adopted, GDPR Art 28(3) and 45. IMDA and Y.3172 copies got a `Source:` header from the manifest URL. `kb chunk` rebuilt with ONYX_SOURCE_DIR, then merged so HEAD lines stayed and 10 new cited clauses were added; `kb ingest` (kb_main 116). 235 tests, check-data ok, selftest ok, eval twice identical and unchanged. Departures in `docs/report-back/2026-10-21-task9.md`.

Decision lines moved here from the background (superseded by later orders, still true):

- 2026-10-21 (live order Part B, commit 6ac1a21): bake-off run, 30 live runs, USD 1.63 recorded spend. hq's rule stops: Opus 5.5 fails JSON in Arabic (20 of 26) and quotes (1 of 5); every Opus failure is a `finish_reason: content_filter` stop by the endpoint (38 of 52 calls: 23 empty, 15 cut mid-sentence), Sonnet and Haiku 0 of 52. Sonnet beats or equals Opus on every compared row except model_ms median. hq then chose Sonnet (Part C order, decision 1). Report-back `2026-10-21-task8-bakeoff.md`.
- 2026-10-21 (Part C2, commit 0e5f8a6): Opus on prompt v2, S2 en and ar: 0 of 10 replies stopped (v1: 8 of 10). hq corrected the finding (C2b order): v2 changed more than the field name, the cause is not isolated, Opus stays out, no further Opus spend; README carries hq's paragraph word for word. Sonnet v2 action recall en 0.70 / ar 0.48 (v1 0.43 / 0.17), gap recall en 0.47 / ar 0.00. C2 spent USD 1.30 of 1.50; recorded spend USD 2.92 of 15.
- 2026-10-21 (hq C2b order, commit bbc5497): in every Arabic v2 bake-off run the adviser named the key's gap id in `notes`, not a flag_gap (10 of 10). Prompt v3 asks for flag_gap in every language; v2 runs not rescored; one line under the v2 table in eval/bakeoff.md.
- 2026-10-21 (live order Part A, commit d3a4cb2; Iyas's answers the same day): the guard's prompt tokens come from the prompts a live run would send (live retrieval, median 3,831 bytes, about 958 tokens), not the scripted runs (1,624 bytes, which record no usage). Output tokens enter the estimate once a live run of that model is recorded (its median prompt and completion tokens per call); before that, input only, and the printout says so.

## 2026-10-21: hq accepts Task 9

hq checked Task 9 at bafd4a3 and accepted it (relayed by Iyas). Report-back items 1 (gap-4 competitor yes), 2 (Consumer Law 4(5) not about Arabic), 3 ('prohibited term', not 'void') and 6 (source-line headers on the IMDA and Y.3172 texts) stand as built. Items 4 (gap-7 wording), 5 (builder's category and recommendation per row) and the prompt v4 label (adviser gained gap-8) wait for an hq ruling; nothing changed. Only the background file was updated (decision line, Open item, next action). No code, no fix, no CHANGELOG entry.

## 2026-10-21: order task-9-fixes-tasks-10-11 (Parts A and B)

Part A (d52e39d): gap-7 rewritten to hq text, category standards gap, searched rows PDPL 18(4), ET 11(2), 12(2), Cabinet 57/2024 Art 7 row 16 (promoted to kb/chunks, kb_main 117); ET 13 left out (chunk is the heading). Competitor column out of docs/gaps.md and README. PROMPT_VERSION v4.1. README line on where global quotes are checked. Part B: two-minute check, replay hand-over quotes EN and AR, replay-page (docs/replay), selftest recomputes figures, CI reproduce.yml (first run failed: kb_framework count needs the fetched dimensions file; test now skips with its reason; green at 2996808). Item 9: curl fetch of the 16 document links to the scratchpad returned Cloudflare 403 (uaelegislation.gov.ae) and an ITU "Request Rejected" page; hq ruling (a) applied: rows keep landing URL with the mark in notes, KB export Inputs.md committed and linked. I told Iyas 15 rows; there were 16 (15 portal plus Y.3172), corrected in the report-back.

Decision lines moved here from the background (older, still true):

- 2026-10-21 (hq check of Task 9 at bafd4a3): accepted. Report-back items 1 (gap-4 competitor yes), 2 (Consumer Law 4(5) not about Arabic), 3 ('prohibited term', not 'void') and 6 (source-line headers on the IMDA and Y.3172 texts) stand as built. Items 4 (gap-7 wording), 5 (category and recommendation) and the prompt v4 label (adviser gained gap-8) wait for an hq ruling: change nothing until it comes.
- 2026-10-21: sources rule for keys and audits (Iyas): only kb/, onyx/data/, the order and the hq notes (an audit may also use the PDFs, pdftotext and the hq checked files); no web, no law from memory; a missing fact stops the step.
- 2026-10-21: every flagged mandate clause checked. Changed: `tdra.order_restore` to CPR 26.11 (licence 9.3 kept second). Widened: `propose_change` +4.9, `raise_dispute` +licence 9.3, `request_report` +CPR 3.9. The rest confirmed; `cite`, `flag_gap`, `release_event`, `route` stay method basis only.
- 2026-10-21: 13 rules added for the keys (CPR 2.1.7, 26.4.5, 26.11, 4.9, 13.4, 13.8, 5.3, 4.22.4, 4.17.1, 4.23.2, 3.9 notices; PDPL 23(2); licence 9.3), quotes from kb/chunks-full/.
- 2026-10-21: licence splitter reads the pypdf .txt: an English clause heading keeps its number and English title and drops the Arabic title on the same line; `bare_page_numbers` starts a page at a line holding only the next page number. Committed licence chunks kept as they are (see Traps).
- 2026-10-21 (freeze, hq orders freeze-order-2026-10-21.md and part 2, commit e8b17cb): quotes licence-9-3 ('between the parties ... with the Telecommunications Law'), cpr-4-7-3 ('opt-out'), cpr-24-7 ('anti-competitive') fixed in rules and committed chunks; 3.9 quotes checked against CPR PDF page 12 and kept; rule pdpl-22-1 added; `receive_objection` cites PDPL 18(1) and 17 (quote stays 18(1)); S1 step 6 and S2 step 5 gate_outcome hold; S3 step 3 cites pdpl-22-1; S4 cites 66/2023 34(1) only, no 34(3) anywhere; frozen line: any later key change re-hashes HASHES.txt in the same commit.

## 2026-10-22: Task 13, prompt v5 and the C5 scored run

Order `docs/work-orders/2026-10-22-task-13-prompt-v5-c5.md` (hq, Fable, with Iyas). Built by Opus 5.5.
- Part A (1fe11bb): care lines 1 and 3 word for word, PROMPT_VERSION v5; v4 tests narrowed to line 2. The order's S2-3
  test said a draft to "Human agent H-01 (synthetic)" is held; the gate allows it (H-01 on shift from the start), so the
  test pins allow plus the scorer's miss, and the C4 spelling "Human agent H-01" pins hold. Spend guard: Sonnet estimate
  from C4 actual cost per run plus 10 percent (USD 5.80 for the batch); TOTAL_CAP_USD 15 to 20; `record` stops between
  runs on the total or the batch cap.
- Part B: C5 S2 en run2 crashed in gate.py `records` (a dict in `args.data`). Asked; hq ruled option 1 with canonical
  JSON text, nothing skipped. `gate.read_items` (f31fb4b); 193 logs replayed, 0 verdicts changed; partial log to
  `runs/_failed/c5/S2/`. Resumed with --skip-existing; order S2, S3, S1, S4, S5, each checked against C4 (citation
  validity within 0.1 everywhere; S2 en 0.94 from one malformed id `tdra-cpr-v2-4.3`). Runs 72439fa.
- C5 result: 5 of 112 key steps missed (C4: 7). S2-3 hit 4 of 4. S3-4 care set recipient human on the coordinator's
  step (en 1 of 2, ar 2 of 2); S4-4 data office addressed "H-03" and "Sahab Telecom account of Khalid". USD 5.41
  (S2 1.17 with the partial run, S3 1.02, S1 1.32, S4 1.06, S5 0.83); recorded total USD 18.88 of 20.00.
- Part C (7bb8cb6): eval `_rerun` for any re-run folder, C5 beside C3 and C4 with a six-metric per-scenario table and
  misses per step; README scored-run line is C5 (tested against results.json); S2 replay page reads
  `runs/c5/S2/ar/run1.jsonl` (no C5 English run had step 4 allowed: run1 hold, run2 insufficient evidence).
- hq ruling on the report (19584b1): README Scenarios table names each page's run; selftest heads with C5 governed and
  names the run set, C3 ungoverned as the baseline line; hand-over latency added to eval's per-scenario summary. No v6.
- CI: the Part C run showed in progress 17 min though every step passed; it ended green. 19584b1 green (10m46s).
- Decisions moved here from the background (superseded detail, still true):
  - 2026-10-21 (Task 4): `hash = sha256(prev_hash + canonical_json(event without 'hash'))`, canonical = sorted keys, compact separators, UTF-8 unescaped; first `prev_hash` 64 zeros; `seq` from 1 and must equal the line number; `run_start` holds the sha256 of each key file as on disk (`new_value.answer_keys`); a broken chain is never replayed. Addendum 17's two override tests need the gate and are left for Task 6.
  - 2026-10-21 (Task 5, Opus, commit 07416f4): channel classification is plain code (hq plan: 'The checks (plain code, not AI judgement)'): business_centre 4.15, voice 4.17, app_chat 4.22 + 4.10 + 4.11 (strict reading, key S1 step 1), web 4.23; unknown channel raises. An unparseable reply proposes nothing. No new dependency; no real model call made.
  - 2026-10-21 (hq task-7 order, commits b048945, 93a7d40): Telecom Law 72(2) has a rules.json row and chunk; model_provider_gate cites it. Task 7 coordinator built (staged release, live inject, Arabic runs cite the same clause ids as English).
  - 2026-10-21 (Task 5 model decision, hq task-8 order): the live model is Claude through Anthropic's OpenAI-compatible endpoint, base URL `https://api.anthropic.com/v1/`, model `claude-opus-5-5` (platform.claude.com/docs/en/cli-sdks-libraries/libraries/openai-sdk, read through context7). Temperature below 1 is a 400 on Claude 4.7+, so it is omitted.
  - 2026-10-21 (live order Part B): a proposal whose `args.deadline` is not a {rule, value, unit} object is blocked by the base checks (it crashed the gate on Haiku's and Sonnet's S5 step 6). No existing verdict changed.
  - 2026-10-21 (Task 8, commit d85871d): every event has `gate_ms` and `model_ms` (null where not measured). Action recall addressee: where the key answers a step sent by a human with draft_reply, the reply must be addressed to the human; every other step a non-human addressee. Obligation recall is step-level (key verdict reached and every must_cite on the step's record). Hand-over latency: first step from handover_step that is a hold, an allowed proposal to or asking for a human, or a complaint_gate hand-over duty. All three sent to hq to confirm.

## 2026-10-22: Task 14, the replay viewer

Order `docs/work-orders/2026-10-22-task-14-replay-viewer.md` (hq, Fable). Built by Opus 5.5, no model call, USD 0.
- The hq ruling on the C5 report (items 2 and 3) was already in 19584b1; nothing further to do. Order filed dd69538.
- Built ebc29a2: `onyx/replay_viewer.py`, `replay-page --html`, `docs/replay/index.html` (1,110,983 bytes), CI step,
  README line, 10 tests (282 in all). Steps rendered in Python (parseable, testable); events inline as JSON as ordered.
- S2 English run: no C5 English run allows step 4; C3 `runs/S2/run1.jsonl` blocks with both quotes at steps 3 and 4,
  breaking the order's "panel at step 3 only" test, so `runs/c5/S2/run1.jsonl` (step 4 hold). C5 Arabic step 4 also
  carries both quotes on an allow: the panel needs a block.
- First test run found 4 quotes "missing": the Decision 16 rules hold Arabic in `quote`; the page had tagged them
  English. Language now detected from the text; all quotes verbatim in kb/chunks.
- Screenshots via a localhost server (Playwright blocks file://). CI green on ebc29a2 (1m7s).
- Moved from the background (superseded by C5 as the headline, still true): 2026-10-21 (C4 result, 1deb675): governed (en / ar) citation validity 1.00 / 1.00, action recall 0.93 / 0.95 (earlier rule 0.89 / 0.91), obligation proxy 0.47 / 0.50, gap recall 0.87 / 0.87, abstention 1 / 1. Misses 7 of 112 key steps: S2-3 and S3-4 care, both from v4 lines. 12 ids resolved (S1-3 4 by the eval only, S3-5 8 by the gate live). C4 USD 5.28 of 6.00.

## 2026-10-22: Task 15, gap-9 and the 79 bis (2) candidate

Order `docs/work-orders/2026-10-22-task-15-gap-9-child.md` (hq, Fable, final). Built by Opus 5.5, no model call, USD 0.
- Copied the order and three hq source texts (Resolution 106 EN, Telecom for Minors EN, child law AR) to `docs/`; Iyas said "two" files, the order lists three. `.gitignore` gained `!docs/sources/*.txt`.
- COPPA 16 CFR 312.5: ecfr.gov page gave a CAPTCHA to scrapling; fetched from the eCFR versioner API (2026-10-19 text). Both quotes verbatim; all nine item-2 quotes verbatim in the copies.
- gap-9 and candidate-79bis-2-fine-schedule added by a scratch script in the file's layout; "A child on the line" left Candidates. Renderer: `16 CFR` short name, Arabic line from `quote_ar`/`file_ar`.
- kb/chunks: a filter of local chunks-full would have reverted four hand fixes (pur suant, billin g, opt- out, anti- competitive); restored, then only 9(2), CPR 4.7, 79 bis, licence 16.3.2 added. `kb ingest` rebuilt (121 kb_main).
- Tests: 8 new; `test_prompt_v3` example id gap-9 became gap-10. 290 passed; every CI step run locally with no diff; CI green on 7313ead (1m9s).
- Moved from the background (C3 and C4 detail, superseded by C5 as the headline, still true):
  - 2026-10-21 (hq, after C3 stopped at S3 on the 0.1 rule, commit f8a7504): citation validity counts only proposals that cite a clause; a flag_gap citing nothing is counted apart ("Gap flags without a clause"). Narrower reading taken: any other verb citing nothing still fails (only flag_gap cites nothing in every committed run). Bake-off tables keep the old definition.
  - 2026-10-21 (C3, commit 7b13260): Sonnet on v3, governed all five (en / ar): citation validity 0.97 / 0.98 (hq rule; 0.95 / 0.87 every proposal), action recall 0.71 / 0.71, obligation proxy 0.32 / 0.35, gap recall 0.87 / 0.87, abstention 1 / 1; gaps from notes 0. C3 spent USD 5.27 of 6; recorded spend USD 8.19 of 15.
  - 2026-10-21 (Iyas, after the governed estimate of USD 7.68 broke the USD 6 C4 cap): C4 is governed only, 2 runs per scenario and language; no ungoverned C4; results.md must say the ungoverned rows are C3 on prompt v3 and that C4 has 2 runs per cell; every stop rule of the order still applies.
  - 2026-10-21 (hq C4 addendum, Fable): clause-id resolution, one function for gate and eval; older logs replay as recorded; no prompt change, v4 stands. Iyas chose the logs' count for the results line and README ("6 ids in 4 of 389 proposals citing a clause across C3 and C4 S1") over hq's "4 of 341".

## 2026-10-22: Task 16, pages, grounding, README, 79 bis row

- Built order `2026-10-22-task-16-pages-grounding-readme.md` (d7ff66b). First stop: CPR 17.4 and 4.20.1 not in kb/chunks, and the S1 line said more than 17.4 holds; hq ruled (add four chunk lines, S1 reworded to 17.4 and 17.4.1, PDF test without whitespace) and updated the order file before the build went on.
- PDF page test: the three clauses sit on their pages; a plain substring missed on 26.7.2 and 79 bis only because the text layer splits words ('non -human', 'o f this').
- Taken without asking, reported: `page_of` placeholder rule (all page 1), S1 lists two clauses, `grounded_in` shape, README bullets capitalised, team and KB lines kept above `## Why`, competitor read left uncommitted.
- CI failed on d7ff66b: the filed order names two entries. c8c08e2 skipped `docs/work-orders/` but was pushed with the test file itself naming them (`;` chain); c1262e5 checks word hashes instead, CI green. Viewer checked in Playwright over a localhost server.
- Moved from the background (still true, least current):
  - 2026-10-21 (hq Part C order, decision 1): the main model is `claude-sonnet-5-5`, set in `.env`. Opus is out; its 10 runs stay committed and the content_filter stops are a finding (fail closed on an opaque upstream component), not a bug. Fable not tried.
  - 2026-10-21 (C4 order, hq Fable): keys frozen, no refusal counted as a hit; scorer addressee rule corrected and shown both ways; prompt v4 care only; care mandate = its gates' clauses. Built 359a498: C3 governed action recall 0.75 en / 0.73 ar (earlier rule 0.71 / 0.71).
  - 2026-10-21 (Task 9, bafd4a3): 9 rows plus 4 candidates; a row's quotes are verbatim in a committed chunk or a `kb/sources/global/` file. Departures sent to hq in the report-back: gap-4 competitor yes (hq reading notes), Consumer Law 4(5) not about Arabic, 66/2023 34 says 'prohibited' not 'void', gap-7 wording, builder-chosen category and recommendation. 10 chunks added; adviser prompt gained gap-8 under the v4 label.
  - Adding cited clauses: `kb chunk` rewrites kb/chunks; keep HEAD's lines and add only the new clause lines (Task 9 did this with a merge script), then `kb ingest`.
  - `runs/bakeoff/<model id>/` (prompt v1, 10 governed live runs each, committed with responses) and `runs/bakeoff/_failed/` (3 partial logs of crashed runs, kept so their spend counts). `runs/bakeoff-v2/claude-sonnet-5-5/` and `claude-haiku-5-5/` (prompt v2, 10 each). `runs/opus-filter-v2/S2/` (Opus on v2, en and ar: the finding test).
  - 2026-10-21 (keys session, Fable): scenarios S1 to S5 and the answer keys written and hashed. Keys cite rules.json ids; gap ids follow the Task 9 register order (the order's S2 line says 'gap 2' in the research numbering; it is `gap-1`).
  - 2026-10-21: S3 step 4 (de-identified payload to the model provider) is the order's design rule, not a KB-confirmed PDPL 22 exemption; the key says so.
  - 2026-10-21 (Iyas): the candidate-id mismatch (coordinator writes `candidate-S1-6`, S1's key expects `candidate-4-4-fixed-term-bundle`): the Task 9 order did not address it; still open for hq.
  - GitHub may keep the old commits reachable by their hash until its own cleanup; private repo. A full purge is a GitHub Support request.

## 2026-10-22: Task 17, figures and README screenshot (twenty-second wrap)

Built order 2026-10-22-task-17-figures. First stop: panel (b)'s values are not C5 (Governed and Ungoverned tables are C3; claims allowed is a count) and `docs/build_report.py` does not exist; hq ruled (a) for both. Built the two figure scripts (matplotlib added to dev extras), PNG and SVG in `docs/fig/`, retook both S2 step 3 screenshots at 1280 px (they predated Task 16's page numbers), embedded the English one in the README, added both scripts to CI; `tests/test_figures.py` 10 tests failed first, then passed; suite 329 passed locally. Commits 9f95e33 (order), 045f28b, 20cc23e (SVG CRLF from matplotlib on Windows), report-back update. CI run 39842151859 failed: PNG bytes from Linux differ from Windows; SVGs match. Stopped for hq (report-back item 8). A `taskkill` by image name used to stop the screenshot server closed every Python process on the PC (Iyas: no harm).

Moved from background (superseded by the date-order pointer): Orders: `docs/work-orders/2026-10-17-onyx-mizan.md`, then `2026-10-21-task-8-live.md` (Parts A and B done), then `2026-10-21-task-8-part-c.md`, `2026-10-21-task-8-part-c2b.md` and `2026-10-21-task-8-part-c3-citation-rule.md` (all done; C3 commit 7b13260), then `2026-10-21-task-8-part-c4.md` (with `2026-10-21-c3-miss-analysis.md`; items 1 to 4 done 359a498, run stopped after S1, 17a1f14) and its addendum `2026-10-21-task-8-part-c4-addendum.md` (clause-id resolution e8fef52; S2 to S5 1deb675; report-back `docs/report-back/2026-10-21-task8-part-c4.md`). C4 is done. Then `2026-10-21-task-9-gaps.md` (Task 9, bafd4a3; report-back `docs/report-back/2026-10-21-task9.md`), then `2026-10-21-task-9-fixes-tasks-10-11.md` (Part A d52e39d, report-back `2026-10-21-task9-fixes.md`; Part B, report-back `2026-10-21-tasks-10-11.md`). Then `2026-10-22-task-13-prompt-v5-c5.md` (Part A 1fe11bb, gate fix f31fb4b, C5 runs 72439fa, Part C 7bb8cb6, hq ruling fixes 19584b1; report-back `docs/report-back/2026-10-22-prompt-v5-c5.md`). Then `2026-10-22-task-14-replay-viewer.md` (ebc29a2; report-back `docs/report-back/2026-10-22-task-14-replay-viewer.md`). Then `2026-10-22-task-15-gap-9-child.md` (7313ead; report-back `docs/report-back/2026-10-22-task-15-gap-9.md`). Then `2026-10-22-task-16-pages-grounding-readme.md` (with hq's rulings on its first stop; d7ff66b, test fixes c8c08e2 and c1262e5; report-back `docs/report-back/2026-10-22-task-16-pages-grounding-readme.md`). Next: hq's rulings on the Task 14 and Task 16 report-backs, or the next order.

Moved from background traps (live runs are over, USD 1.12 left): The spend guard estimates from the medians of recorded calls, mostly prompt v1; v2 prompts are about twice as long (Haiku 1.96x prompt tokens, Sonnet cost 1.36x). The guard under-estimates v2 runs: project from `runs/bakeoff-v2` costs and run in slices with a spend check between them.

## 2026-10-22: Task 17 ruling 4, report-back rulings on Tasks 14 and 16 filed (twenty-third session)

- Ruling 4 applied (151402f): `tests/test_figures.py` holds only the SVGs to the committed files, PNGs to a second
  draw in the same run; CI's closing `git diff --exit-code` excludes `docs/fig/*.png`. Tamper check: a changed PNG
  passes the diff, a changed SVG fails it. 329 passed; CI run 39845579560 green. Task 17 accepted.
- hq's report-back rulings on Tasks 14 and 16 copied to the end of their filed orders: all accepted as built,
  nothing to build. Superseded: the "awaiting hq" lines for both tasks and the red-CI trap.

## 2026-10-23: Task 12 part A, the report builder (twenty-fourth session)

Built order 2026-10-23-task-12-report-build (filed with hq's rulings on the first stop). Items 1 to 3: template and
draft copied; `docs/build_report.py` with the value check; both tagged paragraphs pass. First stop: 2.3 / 2.1 and the
(1) to (4) markers had no class; hq ruled (plain decimals from the named run set only; single-digit list markers
skipped). Item 5: S3 to S5 pages on C5 run1; S1 stays C3 (no run, C3 or C5, cites CPR 17.4 or 17.4.1). A Task 14 test
then failed (viewer must match the pages); Iyas ruled the viewer follows. Item 6: register candidate id in the
coordinator. Item 4: Word counts 9 pages, 3,241 words; stopped, nothing trimmed. Rendering checked on a PDF export:
correct; the length is the text. 354 tests pass; selftest "figures match a fresh eval of runs/". CI not yet run on it.

Moved from background (superseded or old):
- 2026-10-22 (Task 15, 7313ead): register 11 rows (gap-9 method / legislative gap, TDRA and Cabinet, global example COPPA 16 CFR 312.5; candidate-79bis-2-fine-schedule absence, Cabinet); child-law 10(1)(g), 11(2) and Telecom Law 79 bis (1)/(2) cited by their merged chunks (10(1), 11(1), 79 bis). hq kept the category, `line` labels and competitor 'not read'; Task 16 rewrote the candidate's gap and UAE position.
- 2026-10-22 (hq, Task 14 report-back rulings, filed in the order): accepted as built. S2 English shows `runs/c5/S2/run1.jsonl` (C5 is the run the report cites); figures are per run shown, run named; holds name no approver (human steps are scripted; a real approver comes after the shortlist).
- 2026-10-22 (Iyas, hq order Task 13): the two C4 causes fixed before the report; stop raised to USD 20.00, the prepaid balance. Prompt v5 care lines 1 and 3 word for word; scorer, keys, rules.json, mandates.json unchanged.
- ecfr.gov answers a browser-style scripted request with a CAPTCHA; its versioner API works with curl `--compressed` (it refuses uncompressed replies). The local `kb/chunks-full/` is older than the committed chunks: copy only new clause lines from it.
- Git Bash turns `C:/...` arguments into broken paths inside `git filter-branch`; use `/c/...`.
- The IMDA text is Windows-1252; `kb.read_text` falls back.
- Y.3172 needs `top` headings and a footer strip that splits glued page numbers (`138.1` is page 13 + clause 8.1).
- pdftotext on this machine is xpdf 4.00 (`/mingw64/bin`), not poppler: CRLF line ends, and it writes math-alphabet letters as split surrogates (QoS); decode with `surrogatepass`.
- `طالما` and `ثالث` are real words: do not add them to the broken-word list.

## 2026-10-23: Task 12 finished on Iyas's rulings; Task 18 built (twenty-fifth wrap, Opus)

- Iyas's rulings on Task 12's second stop, filed at the end of its order: docx creator and last editor "Team Onyx" (the template's "Meng, Jiaying" gone from every part); captions, backticks and bold labels accepted as built; the Results paragraph checked sentence by sentence against its own tag (a C3-only 0.86 in the C5 part fails; a C5-only 0.96 in the C3 part fails). Five tests failed first, then passed. 8cd6727, CI green run 39984374759. Report-back rewritten: 9 pages, 3,241 words, page-6 sentence, scorer note on gap recall.
- Task 18 (order filed 4ed618d, built 1acf952, CI green run 39992063346): hq's 2026-10-23 text over `docs/report.md` (value check passed unchanged); builder table cells 10 pt with zero spacing, both figures 16 cm, keep-with-next on pictures and the six headings; Figure 1 redrawn as a 16 by 4.5 cm landscape strip, Figure 2 side by side at 16 by 5 cm (panel (b) legend in one column over its own axes, y ticks fixed at 0.2 steps), both captions removed from the images. Word: 5 pages, 2,175 words, no ladder step used. README "For the reviewer" block added; every path tracked, `kb verify` and the C5 replay run. Three older README layout tests updated to the new first heading; the 0.01 value test follows the new line wrap. 363 tests pass.
- Item 6 held: manifest row telecom-law-3-2003-ar says the Arabic Articles 13, 14, 72 to 79 bis were read from page images, against the order's "with their text layers (no OCR)". Both rows quoted in the report-back for hq.
- Tried: Python heredocs for the figure and test edits; twice the written \n became a real newline and the edit aborted or broke the file. Fixed with the Edit tool.
- Moved here from the background (still true, least current):
- 2026-10-21 (hq review on Fable, applied on Opus, commit 7cb7900): four key edits, then re-hashed (S1, S2, S5 changed; S3, S4 not). S2 step 3 acknowledgement is reference number and time-frame within one business day of the written complaint (26.13.3); issuing it at the same step is a design note that eval reports as hand-over latency. S5 step 3 ungoverned claim is only the block on the caller's word; 'refuses to act' is a note. S5 steps 3 and 4 do not cite cpr-4-17-1 (notes only). S1 step 6 candidate row: kind 'scope', addressee TDRA, never numbered among gaps 1 to 7. Any further key change comes from hq the same way.
- 2026-10-21 (hq addendum 27, commit 13c02c6): an agent's document set follows its role, listed in `mandates.json` (care 27, adviser all 40, tdra 18, data_office 22, coordinator 8). Tests: every key `must_cite` document lies in the step agent's set; global examples reach only the adviser, except IMDA for the coordinator (deny-by-default source). A future key that breaks this goes to hq; the set is not widened.
- 2026-10-21 (Task 6, commit 4adbebb): base checks first. A verb with no gate, or no reachable human, is a hold (IMDA 2.2.2 as design basis). A verb outside the mandate, an inject not released, or a deadline not equal to rules.json is a block. A bad quote, or an unretrieved or non-VERIFIED chunk, is insufficient_evidence. Then every gate for the verb; the strictest wins (block, hold, allow). Only a hold can be overridden, by a named human; a block override is refused and logged. disconnection_gate cites 66/2023 34(1) (as the frozen keys), not the order's 34(3). Global examples (IMDA 2.2.2, EU AI Act 50(1) and 50(5), GDPR 22(3)) quoted from the hq standards-text files, in reasons only.
- 2026-10-21 (hq task-8 order Part A, addendum 29, commit d4ec049): the five abstention steps carry `pending_proposal`; after the adviser abstains the coordinator submits it through `gate.decide_pending` (mandate check, then the verb's gates; block or hold stands, else a deny-by-default hold). Verdicts equal every key's gate_outcome; S3's H-02 override is refused and logged with the name. Ungoverned: allow_all, no override event.
- 2026-10-21 (hq, order task-9-fixes-tasks-10-11): gap-7 is hq's text, category standards gap; ET 13 left out (heading only). Competitor fields stay in gaps.json, out of the public outputs. Prompt label v4.1 (unscored). Item 9 ruling (a): no second fetch; 16 landing rows marked (order said 15). Departures accepted: no kb fetch in CI, no eval-generated README results block, counts VERIFIED / REFERENCED / UNVERIFIED.

## 2026-10-23: Twenty-sixth wrap, Task 18 item 6 and Task 19 what-if replay

- Task 18 item 6 (hq ruling `task-18-item-6-ruling-2026-10-23.md`): manifest rows unchanged since 1acf952; hq's reworded Telecom Law 3/2003 sentence (page images for Arabic Arts 13, 14, 72 to 79 bis) closes the README "Knowledge base" paragraph, test first. 6259011, CI run 39993970699 green; line 9 added to the Task 18 report-back (62b7833).
- Task 19 filed (bb08c33). First pass stopped before code: under the order's literal rule S2-4-care `draft_reply` (hold en, allow ar) also carries an obligation on `cpr-26-7-2`, so three decisions would change. hq ruled block only (`task-19-ruling-block-only-2026-10-23.md`).
- Built (7615029, CI run 39995571844 green): `onyx/whatif.py`, `onyx/data/proposed/gap-1.json` (order text verbatim), CLI `whatif`, page `docs/replay/whatif-S2-gap-1.md`, viewer picker entry and link, README two sentences and reviewer line 2, report S2 sentence. Word went to 6 pages; Task 18 ladder step 1 (drop "A judge's added step") gave 5 pages, 2,178 words. Tests 378. Item 7f diff empty. Wrappers install on governed runs only (an addition the order did not name). Sweep of 212 committed runs: nothing outside S2 changes; older S2 runs with S2-4 blocked gain the clock there. Report-back `docs/report-back/2026-10-23-task-19-whatif-replay.md` (0174976).
- Superseded from the background's decisions (still true, moved for size):
  - 2026-10-22 (hq, Task 16 report-back rulings, filed in the order): accepted as built. `page_of` returns None only when every committed chunk of a document says page 1; S1 `grounded_in` lists 17.4 and 17.4.1. The two entry names inside the filed order stay until hq strips them with the clean-history public repo before 2026-11-09; the name test skips `docs/work-orders/` until then.
  - 2026-10-22 (hq, Task 17 ruling 4, 151402f): figure SVGs are byte-checked against the committed files across machines; PNGs only against a same-machine redraw (test draws twice; CI's `git diff` excludes `docs/fig/*.png`). Committed PNGs are the Windows ones.
  - 2026-10-22 (hq rulings on Task 17's first stop): panel (b) draws the C3 Governed and Ungoverned tables with its own caption line, no column added to results.md; item 4 (report hook) waits for Task 12, which places both figures.

## 2026-10-23: Twenty-seventh wrap, Task 19b gap 1 Arabic text

- Order filed (fc2c02e). `text_ar` in `onyx/data/proposed/gap-1.json` set from the filed order's line programmatically. A first raw text replace broke the JSON on the string's two straight quotes; redone through `json.dumps` (stored as `\"`), decoded value asserted equal to the order's string.
- Regenerated `docs/replay/whatif-S2-gap-1.md` (`whatif runs/c5/S2/run1.jsonl --rule gap-1`) and `docs/replay/index.html` (`replay-page --html`), one line each. What-if output on the en and ar C5 S2 runs captured before and after: identical (S2-3 block to block + obligation, S2-5 hold to allow + check, finding; 8 of 10 identical).
- Checks: old text only in the Task 19 and 19b filed orders; new text once in JSON, page, viewer; item 7f diff against 1acf952 empty; 378 tests pass; check-data ok; report files untouched (5 pages stand, Word not re-run). Built at c5cea32, CI run 40031528270 green.
- A stale empty `.git/index.lock` (no git process running) blocked the first commit; removed.

## 2026-10-24: Twenty-eighth wrap, Task 20 gap-10 (Arabic at equal quality)

- Order filed (358d600), built at 5dbb250 (CI run 40036518055 green), report-back 026d8c2.
- Fetch: scrapling `make_request` with a `#wb-cont` selector returned only the title; curl of `page-2.html` and `page-3.html` (laws-lois.justice.gc.ca) into the scratchpad, HTML stripped by a script, Part IV ss. 21 to 33 saved as `kb/sources/global/canada-ola-part-iv.txt`. Act current to 2026-09-30. ss. 22, 26, 27 verbatim.
- Every chunk claim in the order matched; the 43 QoS chunks carry no language word in either language. Five chunk lines inserted in document order (no existing line changed), `kb ingest` 130.
- Row gap-10 with nine searched clauses (QoS by 9.5, the only committed QoS chunk) and a new `framework` field for the Readiness 2.0 d6_m02 line (non-binding); `gaps.py` gained the Canada label and the framework render. Tests in `tests/test_gaps.py`; `tests/test_prompt_v3.py` non-id changed to gap-11; candidates now at adviser lines 11 and 12.
- The order's competitor basis named two entries; `test_no_other_entry_is_named_in_a_tracked_file` failed on it. Iyas chose the unnamed wording.
- Report: one sentence after the gap 8 paragraph; README "Ten rows"; docx 5 pages, 2,204 words. 386 tests, check-data ok; protected diff from c5cea32 empty (`onyx/scorer.py` named by the order does not exist; `onyx/eval.py` unchanged).
- Tried: a Python heredoc to edit tests failed its own assert (the Git Bash quoting trap); redone with the Edit tool.
- Moved here from the background (still true, least current):
  - 2026-10-23 (hq rulings on Task 12's first stop, filed in the order): a plain decimal outside 0.00 to 1.00 matches only the named run set, rounded (2.33 is 2.3); a single digit alone in brackets is a list marker. Ids (S1, S3-4, C5, v3) are skipped as names.
  - 2026-10-23 (Iyas, rulings on Task 12's second stop, filed in the order): docx creator "Team Onyx"; captions plain 10 pt, backticks dropped, bold header labels accepted; a paragraph with two tags is checked sentence by sentence, each against its own tag (the Results paragraph: C5 sentences against the C5 column, the latency sentence against the C3 latency lines). The five-page cut is hq's, by a new order replacing `docs/report.md`.

## 2026-10-24: Twenty-ninth wrap, Task 21 gap 10 in the report's table and recommendations

- Order filed (96d6388), built at 30e02c4 (CI run 40039491351 green), report-back in the same commit, CI run named in a follow-up commit.
- The order's three edits took the report to 6 pages (2,274 words). Order allowed one ladder step: step 2 (test bench sentence) still 6 (2,255); stopped and asked.
- hq ruling in chat: keep step 2, skip step 3 (Figure 2 panel (a) carries 0.96 and 0.94), take step 4 (gaps 1 and 2 use-case sentence): still 6 (2,199). Stopped.
- hq ruling file `task-21-ruling-page-six-2026-10-24.md`: cut A (shorter row 10, gap 10 sentence, item (10)) still 6 (2,189); cut B (dropped "Mizan carries this at D ... reference point.") gave 5 pages, 2,169 words. Page 6 began "What ITU can reuse" at every 6-page build.
- Fewer words than the 5-page Task 20 build (2,204) yet 6 pages: the table row is what costs the space.
- Checks: 10 table rows, old sentence gone, list ends (10), protected diff from c5cea32 empty, 386 tests pass.

## 2026-10-24: Thirtieth wrap, Task 22 consequences in the gap rows

- Order filed in its own commit (e367548), built at 34dc036 (CI run 40134100696 green), CI run named in the report-back in a follow-up commit.
- Iyas's answers before the build: the section C anchor wrapped across two lines counts as found; no PDF (none ever built), docx only; file the order and note the extra file in check 1.
- Edits A to D gave 6 pages, 2,371 words. Ladder steps 1 to 6 (Readiness sentence out; rows 6, 7, 8, 2, 9 back to old text) stayed 6, ending at 2,261 words, 57 words (4 lines) on page 6. Stopped.
- hq ruling `task-22-ruling-page-six-2026-10-24.md`: cut C (five sentences shortened: Introduction, use-case problem, Our solution, S3, Limits) gave 5 pages, 2,224 words; C6 not needed.
- Checks: tagged-paragraph grep empty, protected diff from c5cea32 empty, 386 tests pass.
- Superseded in the background: report at 2,169 words (Task 21); the Task 21 open question on the gaps 1 and 2 sentence; the Task 18 and 19 order lines in "What this is" (Task 19 at 7615029, CI 39995571844, block-only ruling `task-19-ruling-block-only-2026-10-23.md`; Task 18 at 1acf952, item 6 at 6259011).

## 2026-10-24: Thirty-first wrap, Task 23 gap hunt paused at 6 pages

- Order filed at 7c9b32b; all work on branch `task-23-wip` (Iyas: not main). Local main reset to origin/main after branching, so the order commit lives on the branch only.
- Stops before the build, Iyas's answers: the three UAE texts blocked (portal 403; hq's `law-14-2023-en.pdf` and `cabres-28-2023-en.pdf` were the 5,495-byte challenge page; no Arabic file): build without, Task 24 adds them. gap-11 kind: "method" (order said "standards", not a kind). Every count updated, not only C8. Extra files allowed (chunks, local-sources, export, two `onyx/gaps.py` labels, pinned tests).
- Built: TDRA registration policy (tdra.gov.ae 200, matches hq copy) and six global extracts (EUR-Lex by scrapling with wait_selector; eCFR versioner API, needs `--compressed`; Justice Laws pages 2 and 3, s. 27 on page 3). Manifest 47 rows, 43 VERIFIED, nine foreign (old text said four, the rule gave three). gap-11, gaps 2, 4, 6, 7, 9 reworded, breach candidate extended (not duplicated), sub-processor candidate added. 138 cited chunks. Adviser register line 11 (Task 15 and 20 precedent, label v5).
- Report: C1 to C8 gave 6 pages, 2,334 words; ladder 1 to 4 left 6 pages, 2,286 words, page 6 starting "What ITU can reuse". Stopped; hq cuts on 2026-10-25.
- Checks: 386 tests pass, check-data ok, kb verify clean, protected diff from c5cea32 empty, eval unchanged, manifest added rows only.

## 2026-10-25: Thirty-second wrap, Task 23 finished and merged, Task 24 built

- hq ruling `task-23-ruling-five-pages-2026-10-25.md`: cut D (six shortenings) left 6 pages, 2,250 words; E1 (Gap 8 sentence) 6 pages, 2,224 words, 17 words on 2 lines of page 6. Stopped. Addendum `task-23-ruling-addendum-2026-10-25.md`: cut F (Error scenarios one-line paragraph dropped; ITU reuse sentence to one line) gave 5 pages, 2,181 words. Why D moved little: each cut shortened a last line without emptying one.
- Register (Part 2, 3): gap-2 EU AI Act 50(1) replaced by CRD 8(2); gap-4 gains GDPR 12(3) and DSA 20(6); gap-1 DSA 12(1); gap-3 47 CFR 64.2010(b). `onyx/gaps.py` gained DSA and 47 CFR short labels. Committed f53eff1, merged cc7b73b (no squash), CI 40211462109 green.
- Task 24: Trade Law 14/2023 EN and AR, Cabinet 28/2023 EN from hq's browser-saved PDFs (hashes match the order); text by pypdf (no PyMuPDF here), running headers removed; extracts kept in `kb/sources/` (not hq's `standards-text/`: the repo writes nothing outside itself). Seven `searched` entries in gaps 1, 2, 3, 6, 7, 11; Art 5(5) left out. Counts 50 / 46 / 9; "eleven" became "fifteen" (binding VERIFIED UAE instruments besides the four named; 13 on the Task 23 manifest). Branch `task-24`, 8596e95, CI 40212609968 green, not merged.
- One slip caught: the gap-2 `searched` entry first landed in `global_examples` (list closes at another indent); moved before the chunk build.
- Checks both tasks: 386 tests pass, check-data ok, kb verify clean, eval unchanged, frozen diff from c5cea32 / cc7b73b empty, tagged-paragraph grep empty.
- Moved from the background (superseded or settled long ago):
  - 2026-10-23 (Iyas, Task 19b): `text_ar` of `onyx/data/proposed/gap-1.json` is Iyas's wording; its two straight quotes are stored as `\"`, so the decoded value is the order's string. What-if decisions unchanged.
  - 2026-10-23 (Iyas): the replay viewer follows the markdown pages (Task 14's rule kept), so English S3 to S5 show C5 run1.
  - 2026-10-23 (Task 12 item 6): a candidate row carries the register id when the key names exactly one `candidate-` id at that step (`local_id` keeps `candidate-S1-6`). Gap recall reads the log's flag_gap and abstention gaps, not candidates.jsonl, so the fix changes no score.
  - For hq (report-back 2026-10-21-pending-and-task8): confirm the addressee rule, the obligation-proxy definition and the hand-over latency definition.

## 2026-10-25: Thirty-third wrap, Task 24 closed and merged

- hq's `task-24-merge-order-2026-10-25.md` accepted all three report-back points: Art 5(5) stays out of gap-11; "fifteen" stands (hq recounted 19 binding VERIFIED non-foreign, minus the four named); the two text extracts moved to hq's `standards-text/` (byte-identical to `kb/sources/`, checked with `cmp`).
- `kb/local-sources.json`: the two `text` values changed from `../../../engineering/onyx-hackathon-build/kb/sources/...` to `standards-text/...`; nothing else. Commit 6477407.
- Branch was at 75281a3, two wrap-doc commits past the order's 8596e95; merged as is.
- Checks: kb verify VERIFIED 46, check-data ok, 386 tests pass. Merged `task-24` into main without squash (420c14d), pushed; CI run 40213102487 green on 420c14d.

## 2026-10-25: Thirty-fourth wrap, Task 25 (the site) built and merged

- Order `2026-10-25-task-25-site.md` (filed 54c69bf). Plan approved by Iyas before code: 100 logs (the order's "60" was hq's miscount: C3 alone is 60, C4 and C5 add 20 each), a raw-number JSON reader in the page, verify.html about 5 MB.
- Found before planning: a naive Node canonicaliser broke 3 of 2,104 hashes (`model_ms` 10447.0, 6555.0, 4509.0 in runs/c5/S2/ar/run1, runs/S1/run3, runs/ungoverned/S5/run3). Fixed by parsing each number as source text.
- Built: `onyx/html_kit.py` (moved from the viewer, old page byte-identical), `onyx/site.py`, `site` command, `tests/test_site.py` (18, red first), CI step after the figure scripts (an earlier placement broke `test_ci_runs_both_figure_scripts_before_the_diff`, which reads the first `git diff`), README "Open the site", two screenshots. Commit 6a12296, report-back c788b78, merge e1e81cc; CI 40219984220 and 40220128812 (branch), 40220134358 (main), all green.
- Browser: Playwright refused file://; headless Chrome loaded all six pages from file:// and verified two logs green; clicks via Playwright on a local server (filters 3 UNVERIFIED and 15 Arabic, runs link to verify green, tampered line broken at seq 5).
- Checks: 404 tests pass, protected diff empty, site twice with no change, 20 index figures equal results.json, kb verify 46, check-data ok.
- Moved from the background (old or settled):
  - `gh run` status lags on GitHub (2026-10-22: a 42 s job showed in progress for 17 min after every step passed); read the job's steps with `gh run view <id> --json jobs`.
  - 2026-10-22 (hq Task 16 and its rulings): README leads with hq's first paragraph, `## Why` (e& 371,476 and TDRA 23,464, three linked sources), `## Three things to look at first`, then the register; headings "Run it without a key" and "What we do not claim". No other entry is named in the repo; the competitor read lives in hq only (the repo copy was removed outside this session). CPR 17.4, 17.4.1, 4.20.1 and licence 16.3.3 added to kb/chunks (ruling 1). PDF page test compares with whitespace removed (ruling 3).

## 2026-10-26: Task 26 merged; Task 27 built and paused three times on the report's length

- Task 26 (gap rows 1 and 2, 13 searched entries): stopped once (7 clauses only in `kb/chunks-full`, two clause ids not chunks), resumed on hq's ruling, merged to main 241c936, CI green runs 40246430008 (main) and 40246430014 (task-26).
- Task 27 (gap-12 "No metric for where an agent's authority ends", ITU-T Y.3173 into the KB, report row 12): stop 1 (Readiness 2.0 not chunked, Appendix I.1 has no chunk); stop 2 (row 12 made the report 6 pages); stop 3 (hq's cuts F1 row 12, F2 row 2, F3 row 1 left 6 pages, 2,285 / 2,279 / 2,274 words). Also done: "51 documents" twice in the report, the site prints a row's `note`.
- Tried: `kb chunk` over the whole kb reverted the hand-fixed CPR and licence chunk files; restored from git, Y.3173 lines copied from chunks-full. `powershell -ExecutionPolicy Bypass` through Bash denied by the classifier; the PowerShell tool runs the script.
- Checks at the pause: 411 tests, kb verify 51 (47 VERIFIED), check-data ok, protected diff 0 bytes, site twice identical, `git diff d8284eb --stat -- kb/chunks/` only itu-t-y3173.jsonl.
- Moved from the background:
  - 2026-10-23 (hq ruling on Task 19's stop): the proposed gap-1 clock goes only on a `block` verdict; S2-4 (already with H-01) never gains it. On the C5 S2 runs, en and ar, S2-3 gains the clock and S2-5 goes hold to allow with the hand-over-time finding; 8 of 10 decisions identical. Older S2 runs where S2-4 was a block gain it at S2-4 too (reported, no page reads them).
  - `check-data` compares quotes with our chunks, not with the PDFs. The 2026-10-21 pdftotext audit found 13 of 110 quotes not verbatim in pdftotext output (8 layout only); see the report-back.
  - Chaining commit and push after a test with `;` pushes a red commit (c8c08e2, 2026-10-22): chain with `&&`. A test run before a new file is tracked passes locally and fails in CI (the name test met the filed order only in CI).
  - Windows globbing is case-insensitive: `runs/S*` also matches `runs/scripted`. Filter on `Path(p).parts[1]` in S1..S5 or ungoverned.
  - A batch loop that pipes a check through `tail` loses its exit code: use `set -o pipefail` or capture `$?` before piping, or a stop rule silently passes.
  - 2026-10-23 (Task 18 item 5): README opens with `## For the reviewer` (the four criteria, one place each) under the synthetic-data notice; the README layout tests expect it as the first heading.
