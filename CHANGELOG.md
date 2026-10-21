# Changelog

One entry per fix: date, what broke, what changed.

## 2026-10-21

- Broke: 38 of 52 committed Arabic chunks (all CPR) had the lam-alef ligature reversed ('عالقات' for 'علاقات', 'اإلنجليزية' for 'الإنجليزية', a lone 'ال' for 'لا'): the hq .txt files were made with PyMuPDF, which reverses it on TDRA text layers. Changed: `check-data` fails on those shapes in any chunk (`ligature_problems`); the CPR Arabic is re-read from the PDF with pypdf (0 hits, against 1,417 for PyMuPDF; pdftotext also 0), 46 chunks re-chunked; the `quote_ar` of cpr-17-2 and cpr-26-7-2 now hold the correct words.
- Broke: licence-9-1's Arabic was PENDING, with no checked text. Changed: hq `licence-2-2026-ar-9.1-checked.txt` (Iyas against the PDF, page 22) is copied to `kb/extracts/licence-2-2026-ar.txt`, a paired extract (`# pair_of:`) that fills `text_ar` of licence 9.1; the rule's `quote_ar` is that fragment and its `checked_file` names it. `check-data` finds a document's paired extract (`kb.find_extract`).
- Broke: Decision 16/2026 4.18 lost its last sentence (the other licensee's two-hour limit) and ran its two dash items into one line; its quotes were checked against an extract made from the same hq note. Changed: `kb/extracts/decision-16-2026-ar.txt` is the hq checked file (`decision-16-2026-ar-4.17-4.18-checked.txt`, Iyas by eye, 2026-10-21); the 4.18 rule covers both two-hour limits; `read_extract` joins continuation lines.
- Broke: nothing marked a quote read from page images or scanned text. Changed: such rules carry `transcription` (from, field, checked_file); `check-data` lists them, marks one without an hq checked file PENDING (licence-9-1's Arabic), and fails one whose KB text is not from its checked file.
- Broke: the repo committed all 2,184 clause chunks, more than addendum item 15 allows. Changed: `kb/chunks/` holds only the 93 clauses rules and mandates cite; `kb chunk` writes every clause to `kb/chunks-full/` (gitignored); history rewritten so no commit holds the full chunks (Iyas).
- Broke: `kb fetch` gave no way forward where the portal blocks. Changed: it prints the row's URL and the `kb/sources/` file name to save by hand.
- Broke: 11 manifest rows had no URL. Changed: filled from hq `kb-missing-urls-2026-10-20.md`, `url_accessed` 2026-10-20.
- Broke: Decision 16/2026 4.17 and 4.18 had no checkable text. Changed: `kb/extracts/decision-16-2026-ar.txt` holds the hq transcription (from page images, 2026-10-17); two rules and chunks follow it; `check-data` matches Arabic-only quotes against `text_ar`.
- Broke: `kb/export/InputDocs/Inputs.md` was stale on the dimensions.json row. Changed: regenerated.
