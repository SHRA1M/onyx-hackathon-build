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
