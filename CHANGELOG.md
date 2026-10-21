# Changelog

One entry per fix: date, what broke, what changed.

## 2026-10-20

- Broke: the repo committed all 2,184 clause chunks, more than addendum item 15 allows. Changed: `kb/chunks/` holds only the 93 clauses rules and mandates cite; `kb chunk` writes every clause to `kb/chunks-full/` (gitignored); history rewritten so no commit holds the full chunks (Iyas).
- Broke: `kb fetch` gave no way forward where the portal blocks. Changed: it prints the row's URL and the `kb/sources/` file name to save by hand.
- Broke: 11 manifest rows had no URL. Changed: filled from hq `kb-missing-urls-2026-10-20.md`, `url_accessed` 2026-10-20.
- Broke: Decision 16/2026 4.17 and 4.18 had no checkable text. Changed: `kb/extracts/decision-16-2026-ar.txt` holds the hq transcription (from page images, 2026-10-17); two rules and chunks follow it; `check-data` matches Arabic-only quotes against `text_ar`.
- Broke: `kb/export/InputDocs/Inputs.md` was stale on the dimensions.json row. Changed: regenerated.
