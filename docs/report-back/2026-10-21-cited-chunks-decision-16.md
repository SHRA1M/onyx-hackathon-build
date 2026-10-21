# Report back: cited chunks, history rewrite, Decision 16/2026, 2026-10-21

For `D:\Projects\hq\uni\ai-for-good-hackathon`. Order: `docs/work-orders/2026-10-17-onyx-mizan.md` (addendum item 15, Task 3), with Iyas's answers of 2026-10-20 to the report-back of 2026-10-20.

## Summary

The repo now holds only the clauses rules and mandates cite: 93 of 2,186. History is rewritten so no commit, on either GitHub branch, holds the full chunks. Decision 16/2026 4.17 and 4.18 are rules, checked against a labelled extract. The 11 missing URLs are filled. A judge's clone runs fetch, verify, check-data and the tests without the hq folder; `kb fetch` prints what to download by hand where the portal blocks.

## Evidence

- Clean clone of GitHub main (no `ONYX_SOURCE_DIR`): 13 chunk files, 93 lines; the old commit 18a309a absent; 366 chunk lines across every commit of both branches, 0 uncited.
- In that clone: `kb verify` VERIFIED 36, REFERENCED 1, UNVERIFIED 3, HISTORICAL 0; `check-data` ok (rules 94, mandate verbs 16, manifest rows 40); pytest 18 passed, 1 skipped (keys).
- Rebuild check: `kb chunk` from the hq texts reproduced all 2,184 old clauses byte for byte.
- Rewrite check: each rewritten commit differs from its original only in `kb/chunks/`; the tip tree is identical.
- CI `reproduce` green on 1a39414 (main and backup/main) and 4411a27.

## Differs from the order

- `kb/chunks-full/` (gitignored) is new: `kb chunk` writes every clause there and the cited ones to `kb/chunks/`.
- The extract holds the words quoted in hq, not the full clauses; page 10 comes from the PDF text layer (4.15 to 4.22 sit there). The quotes were not compared with the page image here (no PDF renderer on this machine).
- An Arabic-only document's rule `quote` is Arabic and is checked against `text_ar`.
- `kb/export/InputDocs/Inputs.md` regenerated: the dimensions.json row was stale.

## Decisions taken in the build

- backup/main on GitHub held the full chunks; it was force-pushed to the rewritten main, not deleted.
- `kb fetch` lists every row it could not get (portal 403, page URLs whose bytes never match, two u.ae 404s), with URL and target file.

## Open questions for hq

1. Two u.ae URLs answer 404 today: `mocai-ai-ethics-2022` and `ai-deepfake-guide-2021`. Neither is cited, so nothing breaks; the manifest URLs may need a new address.
2. GitHub can keep the old commits reachable by their hash until its own cleanup. The repo is private until 2026-11-09; a full purge before then is a GitHub Support request. Worth asking?

## Merge danger

One-way door, done: the history rewrite. Blast radius: this repo only; no deploys. Any other clone made before 2026-10-21 still holds the old history and must be re-cloned, not pulled.
