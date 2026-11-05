# Working brief: onyx-hackathon-build

Updated 2026-11-05 (seventieth wrap, Opus). Handover for the next session.

## Objective

Finish Task 50, then build Task 51, from `docs/work-orders/2026-11-05-task-50-51-retrieval-and-freeze.md`. Each has its own branch, draft PR and report-back; hq checks and merges. Freeze for Task 51: 2026-11-06. Submission 2026-11-09.

## State

- `task-50` is pushed at `78b307f` plus this wrap's commit. No PR yet. CI run 41942547287 passed on `78b307f`; this wrap's commit has its own run, not named here.
- Measured, in `eval/retrieval.json` and `eval/results.md`. Pooled recall@8 en / ar: shipped 0.24 / 0.09, e5-small 0.24 / 0.15, bm25 0.20 / 0.15, e5-base 0.27 / 0.19, bge-m3 0.34 / 0.32, hybrid-e5-base 0.27 / 0.18, hybrid-bge-m3 0.27 / 0.23. Target 0.40 / 0.30 not met by any, so no Task 52. Nothing tuned after the target.
- Locally 787 tests passed, `check-data` ok, `selftest` "figures match a fresh eval of runs/", repeat `eval` byte-identical. `git diff` of results shows only the retrieval block; `inputs_sha256` unchanged. Spend USD 21.85, cap 45 on the branch.
- Index builds, with `uv run --with sentence-transformers==6.2.0`, CPU: e5-base 23.7 s, bge-m3 395.1 s. Downloaded first, separately (70 s, 137 s), so the recorded `build_seconds` leave the download out: say so in the report-back.

## Not built yet in Task 50

1. `--retriever` and the `run_start` field (question 1). It also needs a retriever that encodes unseen queries: stored vectors hold only the key steps' texts, and a live run sends others.
2. The two method lines at the foot of `results.md` and their pin in `tests/test_annex.py` 279 to 281 (question 2).
3. Report-back `docs/report-back/2026-11-05-task-50-built.md`, draft PR, CI run id.

## Draft verdicts for the report-back (from `scripts/retrieval_diagnose.py`; re-run it for the tables, about 1 minute)

Misses: en 94, ar 112, of 123 entries each. None out of scope.

1. Lay sentence against statute clause: supported. Query and chunk share no token in 59 en and 77 ar misses; en recall 0.41 with a shared token, 0.08 without. "Often procedural": not testable, the repo holds no such label.
2. No Arabic text, English-only embedder: supported. 72 / 84 / 5 confirmed. Arabic recall on chunks with no Arabic text 0 of 46; on chunks with it 11 of 77 (0.14).
3. CPR paragraphs close in wording: not supported as a main cause. 71 of 161 confirmed, but CPR targets do no worse (en 0.21 against 0.26, ar 0.10 against 0.08), and only 28 en and 14 ar misses sit at ranks 9 to 30 behind the same document; 63 en and 98 ar are past rank 30.
4. Chunk sizes: supported but small. 10 to 5,946 words confirmed. Targets over 256 words hit 0 of 6, per language, so they account for at most 6 misses each.

## Open questions

1. hq, Task 50 stop 1, `docs/report-back/2026-11-05-task-50-stop-1.md`: where `--retriever` goes (recommended `record`, allowing `onyx/runs.py`, whose docstring line 64 still says USD 30), and the two method lines.

## Next moves

1. `git status`; `git switch task-50`; `git pull`. Confirm CI.
2. With hq's answers, finish the three items above. No answers and the freeze is close: branch `task-51` from main, as the order allows, and rebase before CI.
3. Build Task 51. The context was past 200k at this wrap, so start a fresh session on Opus.
