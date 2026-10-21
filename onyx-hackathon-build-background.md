# onyx-hackathon-build: background

Updated 2026-10-21 (seventh wrap, Opus: agent document sets, Task 6 gate built).

## What this is

Mizan, team Onyx's entry to the ITU AI for Good Lab Hackathon UAE 2026 (telecom T1). Agents propose JSON actions; plain-code gates decide from clauses of binding UAE text; every step goes to a hash-chained log. Order: `docs/work-orders/2026-10-17-onyx-mizan.md`. Thinking and business facts: `D:\Projects\hq\uni\ai-for-good-hackathon\`. Submission 2026-11-09.

## Stack and how it runs

Python 3.12 (uv), ChromaDB 1.5.9 (default embedding all-MiniLM-L6-v2, 79 MB, downloaded once), pytest, jsonschema, pypdf. CLI: `python -m onyx kb fetch|verify|chunk|ingest|export`, `python -m onyx check-data`, `python -m onyx verify-log <file>`. `ONYX_SOURCE_DIR=D:\Projects\hq\uni\ai-for-good-hackathon` lets `kb fetch` fall back to the hq copies and `kb chunk` read the hq text extractions (maintainer only); the CPR Arabic it reads from the PDF with pypdf, because the hq .txt files (made with PyMuPDF) reverse the lam-alef. Remote: github.com/SHRA1M/onyx-hackathon-build, private, branches main and backup/main, CI `reproduce.yml` (kb fetch, kb verify, check-data, pytest). Not hosted; no push deploys.

## Where things live

- `kb/manifest.csv` (40 rows), `kb/manifest.schema.json`, `kb/local-sources.json` (hq file, text file or the PDF itself to read with pypdf, splitter per document; `bare_page_numbers: true` on licence-2-2026 only), `kb/export/InputDocs/Inputs.md`.
- `kb/chunks/*.jsonl`: only the 105 cited clauses, 13 documents (committed). `kb/chunks-full/`: every clause (gitignored, written by `kb chunk`).
- `kb/extracts/*.txt`: copies of hq `-checked.txt` files (`# key: value` header with `checked:`, then `<clause> <text>`; a line without a clause number continues the clause). `decision-16-2026-ar.txt` (4.17, 4.18 in full); `licence-2-2026-ar.txt` (`pair_of: licence-2-2026`, fills `text_ar` of 9.1 with the checked fragment). `kb chunk` reads them without hq.
- `onyx/kb.py`, `onyx/data.py` (`cited_chunks()`), `onyx/data/rules.json` (108 rules), `onyx/data/mandates.json` (16 verbs; a `documents` list per agent), `onyx/data/scenarios/S1..S5.json` (steps, EN and AR, facts only), `onyx/data/keys/S1..S5.json` (`HASHES.txt`), `onyx/data/scenarios/README.md` (shapes, gap ids, verdict map). `data.load_scenario()`, `data.load_key()`.
- `onyx/audit.py` (Task 4): `AuditLog(path, clock)` with `start(scenario_id)` and `append(event) -> hash`; `verify(path)`, `first_break(path)`, `iter_model_responses(path)`, `key_hashes()`, `FIELDS`. Tests `tests/test_audit.py`.
- `onyx/model.py` (Task 5): `ModelResponse(request_id, raw)` (`raw` is chat-completions JSON, logged verbatim as `model_response`), `OpenAICompatibleModel(base_url, model, api_key)` (stdlib urllib, temperature 0), `RecordedModel(log_path)` (replay by `model_request_id`), `MockModel(script)` (dict or function, offline).
- `onyx/agents/` (Task 5): `base.Agent` (`run(request_id, step, lang)`: retrieve within `documents_of()`, one model call, `parse_output`, verbs outside the mandate moved to `rejected` and logged as `reject_proposal`; `sources_used` is what was retrieved, set by code), `ChromaRetriever(kb_main collection)`, `AGENTS` (care, adviser, tdra, data_office, coordinator; roles from the hq plan's Agents table). `Adviser.classify_channel` is plain code (`CHANNELS`). Clause ids in proposals are chunk ids `document_id:clause`. `documents_of()` reads the agent's `documents` list and raises on an id not in the manifest. Tests `tests/test_agents.py`.
- `onyx/gate.py` (Task 6): `decide(proposal, State, Knowledge) -> Verdict{verdict, clause_ids, reasons}`, `allow_all` (ungoverned), `DECIDERS`, `override(verdict, approver, reason, log, entity_id)`, `GATES` (verb to gate functions). `State`: agent, inject, released, retrieved, channel, facts (scenario field names), humans. `Knowledge.load()` (rules, mandates, chunks; injectable). clause_ids are rules.json ids; reasons carry `gate` and `kind` (check, obligation, quote, design_basis, override). Tests `tests/test_gate.py` (48), whose `_facts` and `_state` show how a step becomes a State.

## Decisions settled

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
- 2026-10-21 (keys session, Fable): scenarios S1 to S5 and the answer keys written and hashed. Keys cite rules.json ids; gap ids follow the Task 9 register order (the order's S2 line says 'gap 2' in the research numbering; it is `gap-1`).
- 2026-10-21 (hq review on Fable, applied on Opus, commit 7cb7900): four key edits, then re-hashed (S1, S2, S5 changed; S3, S4 not). S2 step 3 acknowledgement is reference number and time-frame within one business day of the written complaint (26.13.3); issuing it at the same step is a design note that eval reports as hand-over latency. S5 step 3 ungoverned claim is only the block on the caller's word; 'refuses to act' is a note. S5 steps 3 and 4 do not cite cpr-4-17-1 (notes only). S1 step 6 candidate row: kind 'scope', addressee TDRA, never numbered among gaps 1 to 7. Any further key change comes from hq the same way.
- 2026-10-21: sources rule for keys and audits (Iyas): only kb/, onyx/data/, the order and the hq notes (an audit may also use the PDFs, pdftotext and the hq checked files); no web, no law from memory; a missing fact stops the step.
- 2026-10-21: every flagged mandate clause checked. Changed: `tdra.order_restore` to CPR 26.11 (licence 9.3 kept second). Widened: `propose_change` +4.9, `raise_dispute` +licence 9.3, `request_report` +CPR 3.9. The rest confirmed; `cite`, `flag_gap`, `release_event`, `route` stay method basis only.
- 2026-10-21: 13 rules added for the keys (CPR 2.1.7, 26.4.5, 26.11, 4.9, 13.4, 13.8, 5.3, 4.22.4, 4.17.1, 4.23.2, 3.9 notices; PDPL 23(2); licence 9.3), quotes from kb/chunks-full/.
- 2026-10-21: S3 step 4 (de-identified payload to the model provider) is the order's design rule, not a KB-confirmed PDPL 22 exemption; the key says so.
- 2026-10-21: licence splitter reads the pypdf .txt: an English clause heading keeps its number and English title and drops the Arabic title on the same line; `bare_page_numbers` starts a page at a line holding only the next page number. Committed licence chunks kept as they are (see Traps).
- 2026-10-21 (Task 4): `hash = sha256(prev_hash + canonical_json(event without 'hash'))`, canonical = sorted keys, compact separators, UTF-8 unescaped; first `prev_hash` 64 zeros; `seq` from 1 and must equal the line number; `run_start` holds the sha256 of each key file as on disk (`new_value.answer_keys`); a broken chain is never replayed. Addendum 17's two override tests need the gate and are left for Task 6.
- 2026-10-21 (freeze, hq orders freeze-order-2026-10-21.md and part 2, commit e8b17cb): quotes licence-9-3 ('between the parties ... with the Telecommunications Law'), cpr-4-7-3 ('opt-out'), cpr-24-7 ('anti-competitive') fixed in rules and committed chunks; 3.9 quotes checked against CPR PDF page 12 and kept; rule pdpl-22-1 added; `receive_objection` cites PDPL 18(1) and 17 (quote stays 18(1)); S1 step 6 and S2 step 5 gate_outcome hold; S3 step 3 cites pdpl-22-1; S4 cites 66/2023 34(1) only, no 34(3) anywhere; frozen line: any later key change re-hashes HASHES.txt in the same commit.
- 2026-10-21 (Task 5, Opus, commit 07416f4): channel classification is plain code (hq plan: 'The checks (plain code, not AI judgement)'): business_centre 4.15, voice 4.17, app_chat 4.22 + 4.10 + 4.11 (strict reading, key S1 step 1), web 4.23; unknown channel raises. An unparseable reply proposes nothing. No new dependency; no real model call made.

- 2026-10-21 (hq addendum 27, commit 13c02c6): an agent's document set follows its role, listed in `mandates.json` (care 27, adviser all 40, tdra 18, data_office 22, coordinator 8). Tests: every key `must_cite` document lies in the step agent's set; global examples reach only the adviser, except IMDA for the coordinator (deny-by-default source). A future key that breaks this goes to hq; the set is not widened.
- 2026-10-21 (Task 6, commit 4adbebb): base checks first. A verb with no gate, or no reachable human, is a hold (IMDA 2.2.2 as design basis). A verb outside the mandate, an inject not released, or a deadline not equal to rules.json is a block. A bad quote, or an unretrieved or non-VERIFIED chunk, is insufficient_evidence. Then every gate for the verb; the strictest wins (block, hold, allow). Only a hold can be overridden, by a named human; a block override is refused and logged. disconnection_gate cites 66/2023 34(1) (as the frozen keys), not the order's 34(3). Global examples (IMDA 2.2.2, EU AI Act 50(1) and 50(5), GDPR 22(3)) quoted from the hq standards-text files, in reasons only.

## Traps

- A new rule citing an uncited clause: run `kb chunk` with `ONYX_SOURCE_DIR` set, read the clause in `kb/chunks-full/`, add the rule, run `kb chunk` again so `kb/chunks/` picks it up. Then `git checkout -- kb/chunks/licence-2-2026.jsonl` and `kb/chunks/tdra-cpr-v2-en.jsonl`, and re-apply the hand fixes (next item).
- A `kb chunk` rebuild undoes hand fixes in committed chunks: licence 3.4.1 'pur suant' and 9.1 'billin g' (pypdf errors; the committed file has them right), and the CPR 4.7.3 'opt-out' and 24.7 'anti-competitive' (the extraction keeps 'opt- out', 'anti- competitive'). Licence 9.3 now matches the rebuild. Never commit a rebuilt licence or CPR file unchanged.
- `check-data` compares quotes with our chunks, not with the PDFs. The 2026-10-21 pdftotext audit found 13 of 110 quotes not verbatim in pdftotext output (8 layout only); see the report-back.
- `kb fetch` rewrites `url_accessed` and `http_status` in the manifest to the run's date: do not commit a manifest changed only by a fetch.
- The UAE legislation portal answers 403 to scripts; Y.3172 and EUR-Lex URLs are pages, so their bytes never match.
- PyMuPDF and pdfium reverse the lam-alef on TDRA and portal Arabic text layers; pypdf and pdftotext keep it. The hq .txt files are PyMuPDF output (except the licence, re-extracted with pypdf 2026-10-21): re-extract with pypdf before chunking any other Arabic source. pdftotext adds bidi control marks.
- pdftotext on this machine is xpdf 4.00 (`/mingw64/bin`), not poppler: CRLF line ends, and it writes math-alphabet letters as split surrogates (QoS); decode with `surrogatepass`.
- `طالما` and `ثالث` are real words: do not add them to the broken-word list.
- The IMDA text is Windows-1252; `kb.read_text` falls back.
- Y.3172 needs `top` headings and a footer strip that splits glued page numbers (`138.1` is page 13 + clause 8.1).
- `.gitattributes` forces LF so hashes match on every machine.
- Git Bash turns `C:/...` arguments into broken paths inside `git filter-branch`; use `/c/...`.

## Open

- For hq (report-back 2026-10-21-doc-sets-and-gate): Telecom Law 72(2), named in the order's model_provider_gate, has no rules.json row or chunk, so it is not cited; 34(1) used in place of the order's 34(3); price_change, cancellation and child gates have no scenario step (synthetic tests). Still open from the blind review: S2 steps 3 and 4 share verb draft_reply (the gate tells them apart by `recipient`).
- The gate's fact and args vocabulary (change, recipient, payload, outbound, human_review_open) is the gate's own; Task 7's coordinator and mock scripts must produce it. S4 step 5's `must_cite` is the adviser's searched list, met in Task 7, not by the gate.
- Telecom Law and Cabinet 57/2024 Arabic still show about 95 to 136 hits under every extractor; not read, not chunked.
- The hq research notes quote Arabic from the broken .txt files; an hq session should re-check them.
- GitHub may keep the old commits reachable by their hash until its own cleanup; private repo. A full purge is a GitHub Support request.
- Arabic in the scenario steps (`text_ar`) is the assistant's synthetic subscriber speech, not yet read by Iyas on a page; scenarios are not hashed, so a wording fix is allowed.

## Next action

Task 7 (scenarios and the coordinator: staged release, live inject) on Opus; it builds a State from each step and feeds the gate.
