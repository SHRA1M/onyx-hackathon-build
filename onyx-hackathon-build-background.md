# onyx-hackathon-build: background

Updated 2026-10-21.

## What this is

Mizan, team Onyx's entry to the ITU AI for Good Lab Hackathon UAE 2026 (telecom T1). Agents propose JSON actions; plain-code gates decide from clauses of binding UAE text; every step goes to a hash-chained log. Order: `docs/work-orders/2026-10-17-onyx-mizan.md`. Thinking and business facts: `D:\Projects\hq\uni\ai-for-good-hackathon\`. Submission 2026-11-09.

## Stack and how it runs

Python 3.12 (uv), ChromaDB 1.5.9 (default embedding all-MiniLM-L6-v2, 79 MB, downloaded once), pytest, jsonschema, pypdf. CLI: `python -m onyx kb fetch|verify|chunk|ingest|export`, `python -m onyx check-data`. `ONYX_SOURCE_DIR=D:\Projects\hq\uni\ai-for-good-hackathon` lets `kb fetch` fall back to the hq copies and `kb chunk` read the hq text extractions (maintainer only). Remote: github.com/SHRA1M/onyx-hackathon-build, private, branches main and backup/main, CI `reproduce.yml` (kb fetch, kb verify, check-data, pytest). Not hosted; no push deploys.

## Where things live

- `kb/manifest.csv` (40 rows), `kb/manifest.schema.json`, `kb/local-sources.json` (hq file, text file, splitter per document), `kb/export/InputDocs/Inputs.md`.
- `kb/chunks/*.jsonl`: only the 93 cited clauses, 13 documents (committed). `kb/chunks-full/`: every clause, 2,186 (gitignored, written by `kb chunk`).
- `kb/extracts/<document_id>.txt`: labelled transcriptions (`# key: value` header, then `<clause> <text>` lines); `kb chunk` reads them without hq. One so far: Decision 16/2026.
- `onyx/kb.py`, `onyx/data.py` (`cited_chunks()`), `onyx/data/rules.json` (94 rules), `onyx/data/mandates.json` (16 verbs).

## Decisions settled

- 2026-10-20: MIT licence holder Iyas Shraim; README credits Team Onyx only (member spellings unconfirmed).
- 2026-10-20: one column `jurisdiction` in {UAE, foreign, international}; `jurisdiction_level` dropped (addendum 13).
- 2026-10-20: Cybercrimes 34/2021 is a VERIFIED, binding, UAE row.
- 2026-10-20: answer keys are hashed and committed before Task 8's first live run; Fable session target 2026-10-23.
- 2026-10-21: only cited clauses are committed; history rewritten and force-pushed, no commit holds the full chunks (Iyas). Demo, eval and CI run on the cited clauses alone; a judge's search covers those only.
- 2026-10-21: `kb fetch` downloads what it can; for a blocked row it prints the URL and the `kb/sources/` file name to save by hand (Iyas).
- 2026-10-21: Decision 16/2026 4.17 and 4.18 from the hq transcription (tdra-and-licences.md line 194), page 10, labelled "transcribed from page images, hq 2026-10-17"; 4.19 stays in `PENDING`.
- 2026-10-21: an Arabic-only document's rule `quote` is Arabic and is matched against `text_ar`.
- 2026-10-21: the 11 URLs from hq `kb-missing-urls-2026-10-20.md` are portal landing pages, `url_accessed` 2026-10-20; the two UNVERIFIED rows stay empty.
- 2026-10-20: rules carry `clause` (the citation) and `chunk` (where the quote sits); CPR fn 35 is in chunk 24.11, QoS Annex A (T1(2a)) in 9.5.
- 2026-10-20: dimensions.json canonical bytes are upstream's (commit 6c6771c6, path simulation/data/framework/).
- Unanchored agent-verb clause choices stay flagged; checked in the 2026-10-23 Fable session (Iyas).

## Traps

- A new rule citing an uncited clause: run `kb chunk` with `ONYX_SOURCE_DIR` set, read the clause in `kb/chunks-full/`, add the rule, run `kb chunk` again so `kb/chunks/` picks it up.
- `kb fetch` rewrites `url_accessed` and `http_status` in the manifest to the run's date: do not commit a manifest changed only by a fetch.
- The UAE legislation portal answers 403 to scripts; Y.3172 and EUR-Lex URLs are pages, so their bytes never match.
- Arabic text layers are garbled except the CPR's (lam-alef printed as alef-lam, e.g. وكالء); chunks keep the extraction verbatim.
- The IMDA text is Windows-1252; `kb.read_text` falls back.
- Y.3172 needs `top` headings and a footer strip that splits glued page numbers (`138.1` is page 13 + clause 8.1).
- `.gitattributes` forces LF so hashes match on every machine.
- Git Bash turns `C:/...` arguments into broken paths inside `git filter-branch`; use `/c/...`.

## Open

- Decision 16/2026 quotes not compared with the page image in this repo (no PDF renderer here); they rest on the hq read.
- GitHub may keep the old commits reachable by their hash until its own cleanup; private repo. A full purge is a GitHub Support request.
- Mandate clauses the order leaves open are build mappings (marked in mandates.json).

## Next action

Fable session with Iyas, target 2026-10-23: scenario steps S1 to S5, answer keys hashed into `onyx/data/keys/HASHES.txt`, and the flagged verb clauses.
