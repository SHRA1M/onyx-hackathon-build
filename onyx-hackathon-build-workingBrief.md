# Working brief: onyx-hackathon-build

Updated 2026-11-05 (seventy-first wrap, Opus). Handover for the next session.

## Objective

Finish Task 50, then build Task 51, from `D:\Projects\hq\uni\ai-for-good-hackathon\task-50-51-order-2026-11-05.md`. Each has its own branch, draft PR and report-back; hq checks and merges. Freeze for Task 51: 2026-11-06. Submission 2026-11-09.

## State

- `task-50` holds Task 50's measurements at `78b307f`, plus wrap commits and the fit-check file. No PR yet.
- Measured, in `eval/retrieval.json` and `eval/results.md`. Pooled recall@8 en / ar: shipped 0.24 / 0.09, e5-small 0.24 / 0.15, bm25 0.20 / 0.15, e5-base 0.27 / 0.19, bge-m3 0.34 / 0.32, hybrid-e5-base 0.27 / 0.18, hybrid-bge-m3 0.27 / 0.23. Target 0.40 / 0.30 not met by any, so no Task 52. Nothing tuned after the target.
- At `78b307f`: 787 tests passed, `check-data` ok, `selftest` "figures match a fresh eval of runs/", repeat `eval` byte-identical, `inputs_sha256` unchanged. Spend USD 21.85, cap 45 on the branch. Not re-run at this wrap; no code changed since.
- Index builds, with `uv run --with sentence-transformers==6.2.0`, CPU: e5-base 23.7 s, bge-m3 395.1 s. Downloaded first, separately (70 s, 137 s), so the recorded `build_seconds` leave the download out: say so in the report-back.
- Ra'ed's review: section 5 of `D:\Projects\hq\uni\ai-for-good-hackathon\raed-review-ruling-2026-11-05-fable.md` done up to its stop. Eye-check page built and rendering check run; Task 51 items appended to hq's order, six marked HELD; hq's brief updated. No repo code changed.

## Not built yet in Task 50

hq's ruling is on file and not applied: `D:\Projects\hq\uni\ai-for-good-hackathon\task-50-stop-1-ruling-2026-11-05.md`. File it under `docs/work-orders/`.

1. `--retriever` on `record`, and the `run_start` field. It also needs a retriever that encodes unseen queries: stored vectors hold only the key steps' texts, and a live run sends others.
2. The two method lines at the foot of `results.md`, word for word from the ruling, and their pin in `tests/test_annex.py` 279 to 281.
3. The USD 30 mentions: `onyx/cost.py` line 15, `onyx/runs.py` 64 and 65.
4. Report-back `docs/report-back/2026-11-05-task-50-built.md`, draft PR, CI run id.

## Draft verdicts for the report-back (from `scripts/retrieval_diagnose.py`; re-run it for the tables, about 1 minute)

Misses: en 94, ar 112, of 123 entries each. None out of scope.

1. Lay sentence against statute clause: supported. Query and chunk share no token in 59 en and 77 ar misses; en recall 0.41 with a shared token, 0.08 without. "Often procedural": not testable, the repo holds no such label.
2. No Arabic text, English-only embedder: supported. 72 / 84 / 5 confirmed. Arabic recall on chunks with no Arabic text 0 of 46; on chunks with it 11 of 77 (0.14).
3. CPR paragraphs close in wording: not supported as a main cause. 71 of 161 confirmed, but CPR targets do no worse (en 0.21 against 0.26, ar 0.10 against 0.08), and only 28 en and 14 ar misses sit at ranks 9 to 30 behind the same document; 63 en and 98 ar are past rank 30.
4. Chunk sizes: supported but small. 10 to 5,946 words confirmed. Targets over 256 words hit 0 of 6, per language, so they account for at most 6 misses each.

## Open questions

1. hq, on Fable: six questions in `docs/report-back/2026-11-05-raed-ruling-fit-check.md`. Iyas was given the paste; not known if it has run. HELD items wait on the answers: outage sentence, Arabic coverage paragraph, Limits length, chapeau rule row, licence 9.1 full Arabic. Question 6 (gap 15 mismatched pair, page footers in stored Arabic) holds no appended item.
2. Iyas: the eye-check list (`D:\Projects\hq\uni\ai-for-good-hackathon\arabic-eye-check-2026-11-05.html`, 90 blocks; ticks stay in his browser). A wrong quote in a frozen key is a stop.
3. Iyas asks Ra'ed which pages carried the symbols and which translations he found wrong. Page 13 of the pack is confirmed by the rendering check.

## Next moves

1. `git status`; `git switch task-50`; `git pull`. Confirm CI.
2. Apply the stop 1 ruling and finish Task 50. If the freeze is close, branch `task-51` from main, as the order allows, and rebase before CI.
3. Build Task 51 from hq's copy of the order; the filed copy lacks the Ra'ed section, which is filed as its own dated file. Build no HELD item without hq's answer on file.
4. Re-run the Arabic rendering check on the rebuilt `docs/report.pdf` and paste the output in the report-back.
5. The context was past 200k at this wrap, so start a fresh session on Opus.
