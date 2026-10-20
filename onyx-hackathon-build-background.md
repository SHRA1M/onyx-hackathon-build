# onyx-hackathon-build: background

Updated 2026-10-20.

## What this is

Mizan, team Onyx's entry to the ITU AI for Good Lab Hackathon UAE 2026 (telecom T1). Agents propose JSON actions; plain-code gates decide from clauses of binding UAE text; every step goes to a hash-chained log. Order: `docs/work-orders/2026-10-17-onyx-mizan.md`. Thinking and business facts: `D:\Projects\hq\uni\ai-for-good-hackathon\`. Submission 2026-11-09.

## Stack and how it runs

Python 3.12 (uv), ChromaDB 1.5.9 (default embedding all-MiniLM-L6-v2, 79 MB, downloaded once), pytest, jsonschema, pypdf. CLI: `python -m onyx kb fetch|verify|chunk|ingest|export`, `python -m onyx check-data`. `ONYX_SOURCE_DIR=D:\Projects\hq\uni\ai-for-good-hackathon` lets `kb fetch` fall back to the hq copies and `kb chunk` read the hq text extractions. Remote: github.com/SHRA1M/onyx-hackathon-build, private, CI `reproduce.yml` (kb fetch, kb verify, check-data, pytest). Not hosted; no push deploys.

## Where things live

- `kb/manifest.csv` (40 rows), `kb/manifest.schema.json`, `kb/local-sources.json` (hq file, text file, splitter per document), `kb/chunks/*.jsonl`, `kb/export/InputDocs/Inputs.md`.
- `onyx/kb.py`, `onyx/data.py`, `onyx/data/rules.json` (92 rules), `onyx/data/mandates.json` (16 verbs).

## Decisions settled

- 2026-10-20: MIT licence holder Iyas Shraim; README credits Team Onyx only (member spellings unconfirmed).
- 2026-10-20: one column `jurisdiction` in {UAE, foreign, international}; `jurisdiction_level` dropped (addendum 13).
- 2026-10-20: Cybercrimes 34/2021 is a VERIFIED, binding, UAE row.
- 2026-10-20: answer keys move; they are hashed and committed before Task 8's first live run; Fable session target 2026-10-23.
- 2026-10-20: commit only the chunks that rules and gates cite; rewrite history to remove the full chunks while private (Iyas). NOT DONE YET.
- 2026-10-20: Decision 16/2026 4.17 and 4.18 use the hq transcription (tdra-and-licences.md line 194), notes "transcribed from page images, hq 2026-10-17"; 4.19 stays out. NOT DONE YET.
- 2026-10-20: rules carry `clause` (the citation) and `chunk` (where the quote sits); CPR fn 35 is in chunk 24.11, QoS Annex A (T1(2a)) in 9.5.
- 2026-10-20: dimensions.json canonical bytes are upstream's (commit 6c6771c6, path simulation/data/framework/); the hq copy differs only in line endings.

## Traps

- The UAE legislation portal answers 403 to scripts; Y.3172 and EUR-Lex URLs are pages, so their bytes never match.
- Arabic text layers are garbled except the CPR's (lam-alef printed as alef-lam, e.g. وكالء); chunks keep the extraction verbatim.
- The IMDA text is Windows-1252; `kb.read_text` falls back.
- Y.3172 needs `top` headings and a footer strip that splits glued page numbers (`138.1` is page 13 + clause 8.1).
- `.gitattributes` forces LF so hashes match on every machine.

## Open

- Cutting chunks back means a fresh clone cannot rebuild the full chunks (chunking reads hq text extractions, not fetched PDFs); live inject on a judge's machine would search cited clauses only.
- Decision 16/2026 transcription: CI cannot read an hq file; put the two quotes in `kb/extracts/decision-16-2026-ar.txt` with the source note and check against it.
- Mandate clauses the order leaves open are build-session mappings (marked in mandates.json); confirm at the keys session.
- 11 manifest rows have no URL in the sources.

## Next action

Opus session: do the two NOT DONE decisions above (history rewrite and force-push included), show a clean clone and green CI. Then the Fable keys session.
