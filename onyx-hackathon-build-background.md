# onyx-hackathon-build: background

Updated 2026-10-21 (fourth wrap, Opus: keys after hq review, licence splitter, Task 4, quote audit).

## What this is

Mizan, team Onyx's entry to the ITU AI for Good Lab Hackathon UAE 2026 (telecom T1). Agents propose JSON actions; plain-code gates decide from clauses of binding UAE text; every step goes to a hash-chained log. Order: `docs/work-orders/2026-10-17-onyx-mizan.md`. Thinking and business facts: `D:\Projects\hq\uni\ai-for-good-hackathon\`. Submission 2026-11-09.

## Stack and how it runs

Python 3.12 (uv), ChromaDB 1.5.9 (default embedding all-MiniLM-L6-v2, 79 MB, downloaded once), pytest, jsonschema, pypdf. CLI: `python -m onyx kb fetch|verify|chunk|ingest|export`, `python -m onyx check-data`, `python -m onyx verify-log <file>`. `ONYX_SOURCE_DIR=D:\Projects\hq\uni\ai-for-good-hackathon` lets `kb fetch` fall back to the hq copies and `kb chunk` read the hq text extractions (maintainer only); the CPR Arabic it reads from the PDF with pypdf, because the hq .txt files (made with PyMuPDF) reverse the lam-alef. Remote: github.com/SHRA1M/onyx-hackathon-build, private, branches main and backup/main, CI `reproduce.yml` (kb fetch, kb verify, check-data, pytest). Not hosted; no push deploys.

## Where things live

- `kb/manifest.csv` (40 rows), `kb/manifest.schema.json`, `kb/local-sources.json` (hq file, text file or the PDF itself to read with pypdf, splitter per document; `bare_page_numbers: true` on licence-2-2026 only), `kb/export/InputDocs/Inputs.md`.
- `kb/chunks/*.jsonl`: only the 104 cited clauses, 13 documents (committed). `kb/chunks-full/`: every clause (gitignored, written by `kb chunk`).
- `kb/extracts/*.txt`: copies of hq `-checked.txt` files (`# key: value` header with `checked:`, then `<clause> <text>`; a line without a clause number continues the clause). `decision-16-2026-ar.txt` (4.17, 4.18 in full); `licence-2-2026-ar.txt` (`pair_of: licence-2-2026`, fills `text_ar` of 9.1 with the checked fragment). `kb chunk` reads them without hq.
- `onyx/kb.py`, `onyx/data.py` (`cited_chunks()`), `onyx/data/rules.json` (107 rules), `onyx/data/mandates.json` (16 verbs), `onyx/data/scenarios/S1..S5.json` (steps, EN and AR, facts only), `onyx/data/keys/S1..S5.json` (`HASHES.txt`), `onyx/data/scenarios/README.md` (shapes, gap ids, verdict map). `data.load_scenario()`, `data.load_key()`.
- `onyx/audit.py` (Task 4): `AuditLog(path, clock)` with `start(scenario_id)` and `append(event) -> hash`; `verify(path)`, `first_break(path)`, `iter_model_responses(path)`, `key_hashes()`, `FIELDS`. Tests `tests/test_audit.py`.

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

## Traps

- A new rule citing an uncited clause: run `kb chunk` with `ONYX_SOURCE_DIR` set, read the clause in `kb/chunks-full/`, add the rule, run `kb chunk` again so `kb/chunks/` picks it up. Then `git checkout -- kb/chunks/licence-2-2026.jsonl` unless hq has settled the licence text (next item).
- A `kb chunk` rebuild changes `kb/chunks/licence-2-2026.jsonl` in three places: 'pur suant' (3.4.1) and 'billin g' (9.1) are pypdf errors; 9.3 'between the parties ... with the Telecommunications Law' is right (PDF page 24). The rebuilt 9.3 fails `check-data` on licence-9-3 until hq corrects that quote. Do not commit a rebuilt licence file.
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

- For hq (report-back 2026-10-21-keys-review-splitter-task4): the licence-9-3 quote; four more quotes not verbatim in the PDF text (cpr-4-7-3, cpr-24-7, cpr-3-9-recordings, cpr-3-9-notices); the keys' 'Never edited after HASHES.txt is committed' line, now untrue; the keys' 'hq plan, S2' reference, which no plan file holds.
- Telecom Law and Cabinet 57/2024 Arabic still show about 95 to 136 hits under every extractor; not read, not chunked.
- The hq research notes quote Arabic from the broken .txt files; an hq session should re-check them.
- GitHub may keep the old commits reachable by their hash until its own cleanup; private repo. A full purge is a GitHub Support request.
- Arabic in the scenario steps (`text_ar`) is the assistant's synthetic subscriber speech, not yet read by Iyas on a page; scenarios are not hashed, so a wording fix is allowed.

## Next action

Task 5 (model adapter and agents) on Opus.
