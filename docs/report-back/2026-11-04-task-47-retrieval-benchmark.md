# Task 47 done: retrieval measured on its own (2026-11-04)

Order `docs/work-orders/2026-11-04-task-47-retrieval-benchmark.md`, finished from hq's
`task-47-stop-1-ruling-2026-11-04.md`. USD 0, no model call. No scored figure, prompt, gate, key, mandate, rule or run
changed. C5 stays Sonnet's: action recall 0.96 en / 1.00 ar, citation validity 0.99 / 1.00.

Plainly: a judge asking "how well does your retrieval work?" now gets a measured answer, and it is low. Annex A says so
with its frame, and no longer calls a bilingual embedder the obvious upgrade. The README points to the figures without
carrying them.

## Done means

| # | Check | Result |
|---|---|---|
| 1 | `uv run python -m onyx eval` prints both tables | printed locally, tables below |
| 2 | `uv run pytest`; CI "reproduce" on the PR | 732 passed; CI: see the PR section at the end |
| 3 | `docs/report.pdf` rebuilt, page counts unchanged | before and after: body 5 pages, annex from page 6, 12 in all. PDF 12 pages, "Annex A", "Annex F", "Limits and next steps" found. The annex sentence did not need cutting |
| 4 | Every annex number equals a printed value | the pairs below; `test_annex_a_retrieval_alone_sentence_equals_the_printed_figures` keeps it |
| 5 | This report-back | model, revision, build time and tables below |

## The two tables, as `eval/results.md` prints them

Shipped embedder, `all-MiniLM-L6-v2`, the one in every scored run:

| Scenario | Lang | Key clauses in the top 8 | 95% interval |
|---|---|---|---|
| S1 | en | 4 of 27 (0.15) | 0.06 to 0.32 |
| S1 | ar | 1 of 27 (0.04) | 0.01 to 0.18 |
| S2 | en | 4 of 26 (0.15) | 0.06 to 0.34 |
| S2 | ar | 4 of 26 (0.15) | 0.06 to 0.34 |
| S3 | en | 8 of 27 (0.30) | 0.16 to 0.48 |
| S3 | ar | 0 of 27 (0.00) | 0.00 to 0.12 |
| S4 | en | 6 of 27 (0.22) | 0.11 to 0.41 |
| S4 | ar | 1 of 27 (0.04) | 0.01 to 0.18 |
| S5 | en | 7 of 16 (0.44) | 0.23 to 0.67 |
| S5 | ar | 5 of 16 (0.31) | 0.14 to 0.56 |
| Pooled | en | 29 of 123 (0.24) | 0.17 to 0.32 |
| Pooled | ar | 11 of 123 (0.09) | 0.05 to 0.15 |
| Pooled | both | 40 of 246 (0.16) | 0.12 to 0.21 |

Recall@1 pooled: en 11 of 123 (0.09); ar 3 of 123 (0.02); both 14 of 246 (0.06), 95% interval 0.03 to 0.09.

Bilingual embedder, not used in any scored run, `intfloat/multilingual-e5-small`, never compared with C5:

| Scenario | Lang | Key clauses in the top 8 | 95% interval |
|---|---|---|---|
| S1 | en | 3 of 27 (0.11) | 0.04 to 0.28 |
| S1 | ar | 2 of 27 (0.07) | 0.02 to 0.23 |
| S2 | en | 3 of 26 (0.12) | 0.04 to 0.29 |
| S2 | ar | 4 of 26 (0.15) | 0.06 to 0.34 |
| S3 | en | 9 of 27 (0.33) | 0.19 to 0.52 |
| S3 | ar | 1 of 27 (0.04) | 0.01 to 0.18 |
| S4 | en | 7 of 27 (0.26) | 0.13 to 0.45 |
| S4 | ar | 2 of 27 (0.07) | 0.02 to 0.23 |
| S5 | en | 8 of 16 (0.50) | 0.28 to 0.72 |
| S5 | ar | 9 of 16 (0.56) | 0.33 to 0.77 |
| Pooled | en | 30 of 123 (0.24) | 0.18 to 0.33 |
| Pooled | ar | 18 of 123 (0.15) | 0.09 to 0.22 |
| Pooled | both | 48 of 246 (0.20) | 0.15 to 0.25 |

Recall@1 pooled: en 10 of 123 (0.08); ar 6 of 123 (0.05); both 16 of 246 (0.07), 95% interval 0.04 to 0.10.

One chunk fills rank 1, so at most 30 of 123 (0.24) per language can reach it.

Model and revision: `intfloat/multilingual-e5-small`, `614241f622f53c4eeff9890bdc4f31cfecc418b3`, sentence-transformers
6.2.0. Index build: 775.8 s including the 12 min 45 s download. `query: ` and `passage: ` prefixes used.

Index the benchmark ran on: 161 chunks, both embedders. The scored C5 runs were recorded when `kb/chunks` held 117
(last chunk commit before them, d52e39d), a smaller index; `kb_main` held 138 just before this task rebuilt it. Nothing
in a recorded run reads the rebuilt index.

## Each annex number against its printed value

| Annex sentence | `eval/results.md`, "Retrieval alone" |
|---|---|
| shipped, English 0.24 | Shipped table, Pooled en: 29 of 123 (0.24) |
| shipped, Arabic 0.09 | Shipped table, Pooled ar: 11 of 123 (0.09) |
| bilingual, English 0.24 | Bilingual table, Pooled en: 30 of 123 (0.24) |
| bilingual, Arabic 0.15 | Bilingual table, Pooled ar: 18 of 123 (0.15) |
| "overlapping Arabic intervals" | shipped 0.05 to 0.15, bilingual 0.09 to 0.22 |

## What differs from the order, and why

1. `eval/retrieval.json` is committed and CI recomputes both tables from it; the order had `eval` skip the bilingual
   table in CI, but `results.md` carries it and CI fails on any differing byte. Accepted by hq. The CI log keeps the line
   "bilingual index not built".
2. The e5-small attempt ran past the order's 15-minute limit and out of its sequence, on hq's decision. e5-base and
   bge-m3 were not measured. The first build ran 47 minutes and was stopped, and it never showed why e5-base and
   e5-small failed; the stop file has the detail. Accepted by hq.
3. Annex: three edits by hq's ruling in place of the order's two sentences. Added to the order's README clause: it names
   the measurement, with no number (hq, item 3).
4. `data/chromadb` was rebuilt (138 to 161 chunks). Read by no recorded run. Accepted by hq.
5. One older test changed: `test_annex_a_retrieval_sentence_carries_the_printed_key_clause_figures` pinned one unbroken
   passage, and hq's sentence now sits inside it. It asserts the same two passages, in order.

## Decisions taken here

- Wording of the two method lines hq asked for: "retrieval alone, not diagnosed: why the figures of both embedders are
  low." and "retrieval alone, not measured: `intfloat/multilingual-e5-base` and `BAAI/bge-m3`; the bilingual table is
  `intfloat/multilingual-e5-small` only."

## Open for hq

1. Why both figures are low: not diagnosed, and stays open until after the shortlist, as ruled.
2. hq's own copy of the annex text does not have these three edits; this session writes only inside the repo.

## PR and CI

PR #15, https://github.com/SHRA1M/onyx-hackathon-build/pull/15. CI "reproduce" on `2736654`: success on the pull request
(run 41873930881) and on the push (run 41873916567). The pull request run's log: "708 passed, 24 skipped" and "bilingual
index not built", so CI recomputed both tables from `eval/retrieval.json` and no byte differed. This entry adds only
these lines to this file.

## Limits line and full test output

Touched only the files this order and ruling name, plus the tests and report-back they require; never `runs/` or the keys. Fails closed: USD 0, nothing recorded, nothing sent outward, stop and ask. Owner of any failure: Iyas.

`uv run pytest -q`, added at the wrap, on the commit holding the CI entry above:

```
........................................................................ [  9%]
........................................................................ [ 19%]
........................................................................ [ 29%]
........................................................................ [ 39%]
........................................................................ [ 49%]
........................................................................ [ 59%]
........................................................................ [ 68%]
........................................................................ [ 78%]
........................................................................ [ 88%]
........................................................................ [ 98%]
............                                                             [100%]
732 passed in 181.85s (0:03:01)
```
