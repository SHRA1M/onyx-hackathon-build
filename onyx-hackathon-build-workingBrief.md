# Working brief: onyx-hackathon-build

Updated 2026-10-20 (wrap).

## Objective

Finish Task 2 and 3 corrections from Iyas (2026-10-20), then the answer keys.

## Next moves, in order

1. Opus: commit only the chunks cited by `rules.json` and `mandates.json` (order item 15). Gitignore the rest; `kb chunk` rebuilds them locally. Rewrite history so the full chunks are gone from every commit (`git filter-repo` or a rebuilt history), force-push with Iyas's go already given (2026-10-20), then show a clean clone holds only cited chunks and CI is green. Tests that count all chunks (`test_ingest_builds_three_collections`) must follow the new rule.
2. Opus: Decision 16/2026 4.17 and 4.18 rules from the hq transcription at `D:\Projects\hq\uni\ai-for-good-hackathon\research-notes\uae-rules-2026-10-17\tdra-and-licences.md` line 194; notes "transcribed from page images, hq 2026-10-17". Put the quotes in `kb/extracts/decision-16-2026-ar.txt` with that label so check-data and CI can match them (an hq path is invisible to CI). 4.19 stays in `PENDING`.
3. Fable, with Iyas, target 2026-10-23: scenario steps S1 to S5 and the answer keys, hashed into `onyx/data/keys/HASHES.txt`, committed before Task 8's first live run.

## Open questions

- Mandate clauses the order leaves open: confirm at the keys session.
- 11 manifest rows without a URL in the sources (hq `uni`).
- Claude API key: walked through before the first real call.
- `/setup-matt-pocock-skills` not yet run by Iyas.
