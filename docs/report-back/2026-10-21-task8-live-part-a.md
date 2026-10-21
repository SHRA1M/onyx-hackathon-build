# Report-back: task-8 live order, Part A (2026-10-21)

For hq, `D:\Projects\hq\uni\ai-for-good-hackathon\`. Order: `docs/work-orders/2026-10-21-task-8-live.md`. Commits 293ff7c (order filed), d3a4cb2 (Part A).

## Summary

Part A is built. Eval reports calls, prompt and completion tokens and USD per run; a live run prints its estimate and refuses over `--max-usd` (default USD 5) or past USD 15 recorded spend, before its first call; the metric reads "obligation proxy". No model call made, nothing spent. Parts B and C wait for the key.

## Evidence

- Prices, quoted verbatim from platform.claude.com/docs/en/about-claude/pricing, read 2026-10-21: Opus 5.5 $4 in / $20 out, Sonnet 5.5 $2 / $10, Haiku 5.5 $0.10 / $0.50 per million tokens (Haiku: prompts up to 100,000 tokens). check-data fails if a price leaves its quote.
- Full suite 163 passed; check-data ok; `record --source live` with no `.env` stops with exit 2 and writes nothing.
- Estimates, input only: bake-off 52 calls per model, Opus $0.20, Sonnet $0.10, Haiku $0.005; Part C on Opus, 312 calls, $1.20.

## Where the build departs from the order

1. Item 2 says "median prompt tokens of the scripted runs". Scripted replies carry no usage, and scripted prompts (one retrieved clause) are 2.4x smaller than live ones (eight). Iyas chose: tokens from the exact prompts a live run sends (dry pass, no call), at the pricing page's ratio "Average web page (10 kB): ~2,500 tokens", median about 958.
2. The order's formula is input only. Iyas chose: once a live run of a model is recorded, its median prompt and completion tokens per call are used, so output counts; before that the printout says output is not included. Output probably dominates on Opus 5.5 (thinking always on, output 5x input), so Part C may need `--max-usd` above 5.
3. The USD 15 stop from the order's limits is enforced in code (recorded live spend plus the estimate).
4. `record` gained `--modes` (the bake-off is governed only).

## Found

The local ChromaDB index was stale after the last `kb chunk`; live retrieval would have died on the first call (clause 'tdra-cpr-v2-en 19.2' no longer in `kb/chunks`). Rebuilt with `kb ingest`; logged in CHANGELOG and Traps.

## Merge danger and blast radius

Two-way door: new module and data file, eval output shape extended (`obligation_recall` key renamed `obligation_proxy`). Scripted eval regenerated; no run log, key or HASHES.txt touched.

## Open for hq

- Confirm the two estimate choices above stand for Part B and C.
- An untracked `scripts/set-model-key.ps1` is in the repo (writes `.env` from the clipboard); not committed by this session.
