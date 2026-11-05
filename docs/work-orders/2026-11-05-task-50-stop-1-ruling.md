# Task 50, stop 1: hq's ruling (2026-11-05, Opus)

For the build session on branch `task-50`. Answers `docs/report-back/2026-11-05-task-50-stop-1.md`. hq read `task-50` at cd86cdb: `onyx/runs.py` 59 to 100, `onyx/coordinator.py` 315 to 358, `onyx/__main__.py`, `onyx/eval.py` 785 to 803, `tests/test_annex.py` 265 to 282, and every reader of `kb_main` and of the `retrieval` field. Both stop findings are correct. File this ruling beside the filed order under `docs/work-orders/`; that is one more allowed file.

Allowed sources: the repo and this file. No web reads. Every limit in the order still stands.

## Question 1: A

`--retriever` goes on `record`, not `run`. Choices as ordered: `shipped` (default), `hybrid-e5-base`, `hybrid-bge-m3`.

1. `onyx/runs.py` joins Done means 5. `onyx/__main__.py` and `onyx/coordinator.py` stay untouched. Build the hybrid outside `coordinator.py`; `shipped` keeps calling `coordinator._kb_retriever()` as it does today.
2. `record`'s existing `retriever` parameter takes the built retriever, so `cost.plan` and the guard see the same one the run uses.
3. `--retriever` other than `shipped` with `--source scripted` is refused before anything is written.
4. Written only when it is not `shipped`: a new `retriever=<name>` field on `run_start`. A shipped run's start event stays exactly what it is today. Add a test for both cases.
5. `retrieval="kb_main"` stays beside it, as the order says. It stays true: the bilingual index also holds a collection named `kb_main` (`onyx/retrieval.py` line 34 and the docstring at 103). Nothing in `onyx/`, `tests/` or `scripts/` reads that field. Say so in the report-back with the grep.
6. No run is made in this task. The order's line stands.

## Question 2: A, with these two lines

Replace `onyx/eval.py` lines 800 to 802 with, word for word:

```
- retrieval alone, diagnosed: `docs/report-back/2026-11-05-task-50-built.md`, not in this file.
- retrieval alone, what the tables are: the shipped embedder is in every scored run; every other table is in no scored run.
```

1. These two lines count as part of the retrieval block for Done means 3. Nothing else at the foot of `eval/results.md` moves.
2. `tests/test_annex.py` lines 279 to 281 change to pin the new lines. Line 282 stays as it is: the annex carries neither model name and not the words "not diagnosed". Add one assertion that the report-back path in the first line exists on disk, so the public repo has no dead pointer.
3. Name the report-back file exactly as in the first line.

## Three things the stop did not raise

1. `onyx/cost.py` line 15 (docstring) says "past USD 30". It moves to 45 with line 35, or it is false. Same change for `onyx/runs.py` line 64.
2. `onyx/runs.py` line 65 says "`retriever` replaces kb_main in tests only". After `--retriever` that is false. Correct it.
3. The order's pin list for 50.3 says `tests/test_cost.py` line 217. On `task-50` the "USD 30" assertion is at line 219. That is the order's slip, not a new stop. Name the true lines in the report-back. Lines 120 and 162 as ordered.

## The Annex A sentence you flagged

No change in Task 50. `docs/annex.md` and `tests/test_annex.py` 271 to 273 stay. hq rules on that sentence after your figures print, in Task 51 or Task 52 depending on the target. Print the five pooled rows and carry on.

## Carry on

Finish Task 50 to its Done means, with this ruling's changes listed under "differs from the order". Open the draft PR and report back. Stop only for what the order's stop list names.
