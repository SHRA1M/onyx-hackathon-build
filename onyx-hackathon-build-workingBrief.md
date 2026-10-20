# Working brief: onyx-hackathon-build

Updated 2026-10-20.

## Objective

Tasks 1 to 3 of `docs/work-orders/2026-10-17-onyx-mizan.md`. Tasks 1, 2 and the Opus half of Task 3 are done; the answer keys and scenario steps (Fable, with Iyas) are next.

## Done

- Task 1: scaffold, CLI, smoke test, MIT (Iyas Shraim), README credits Team Onyx, maps updated, private remote SHRA1M/onyx-hackathon-build.
- Task 2: `kb/manifest.csv` 40 rows (36 VERIFIED, 1 REFERENCED, 3 UNVERIFIED); `jurisdiction` replaces `jurisdiction_level` (Iyas); Cybercrimes 34/2021 added (Iyas). 2,184 clause chunks from 19 documents; CPR chunks carry the Arabic. `kb fetch/verify/chunk/ingest/export`.
- Task 3 (Opus half): `onyx/data/rules.json` 92 rows, `mandates.json` 16 verbs, `python -m onyx check-data`; every quote verbatim.

## Next

1. Fable session with Iyas, target 2026-10-23: scenario steps S1 to S5 and the answer keys; hash into `onyx/data/keys/HASHES.txt`; commit before Task 8's first live run.
2. Then Tasks 4 to 7 (Opus).

## Open questions

- Decision 16/2026 4.17 to 4.19: the Arabic-only PDF has a garbled text layer, so no checkable quote; rules held back (`PENDING` in `tests/test_data.py`).
- Chunks commit nearly every clause of each document, against addendum 15's "quotes the gates need": keep all, or only cited clauses, before the repo goes public.
- Mandate clauses the order leaves open (care verbs, `cite`, `flag_gap`, `order_restore`, `request_report`, coordinator verbs): build-session mapping, marked in `mandates.json`; confirm at the keys session.
- 11 manifest rows have no URL recorded in the sources (56/2024, 57/2024, Child Digital Safety, several Arabic texts).
- Claude API key: walked through before the first real call (Iyas, 2026-10-20).

## Known issues

- Arabic chunks only for the CPR; other Arabic text layers are garbled or OCR. Task 7's Arabic run needs them.
- The UAE legislation portal answers 403 to `kb fetch`; those sources come from the maintainer's copy (`ONYX_SOURCE_DIR` = `D:\Projects\hq\uni\ai-for-good-hackathon`) or, in CI, from the committed chunks.
- Footnotes and annexes attach to the preceding clause's chunk (CPR fn 35 in 24.11, QoS Annex A in 9.5); rules record both `clause` and `chunk`.
