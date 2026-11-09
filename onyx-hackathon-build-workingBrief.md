# Working brief: onyx-hackathon-build

Updated 2026-11-08 (ninety-first wrap, Opus). Handover for the next session.

## Objective

hq's end-check orders 4 and 5 (`D:\Projects\hq\uni\ai-for-good-hackathon\end-check-order-*`), one order per session. Then the video. Submission 2026-11-09.

## State

- Three PRs open, none merged: #26 `task-56` (site look, Tasks 56, 56b, 56d), #27 `end-check-2-report-text` (report main text), #28 `end-check-3-annex` (annex).
- #27 and #28 both rebuild `docs/report.docx` from `main`: after the second merge, rebuild it (`uv run python docs/build_report.py`) and run `scripts/report_pages.ps1`. `docs/report.pdf` is behind both.
- This wrap is committed on `end-check-3-annex`.
- Numbers in a `[C3]`/`[C5]` tagged paragraph must be in `eval/results.md`; other counts go in their own untagged paragraph (hq, 2026-11-08).

## Open questions

1. hq: order 2's strip pin now matches "two runs per scenario per language", since cut 2 removed "over the 20 scored runs". Fine?
2. hq: PDF rebuild order after the merges.
3. Earlier, still open: Task 53's one check; Zaid Saaydeh's faculty; gap-15 AI reads; Ra'ed's translations; Task 52 Arabic check.

## Next moves

1. `git status`; switch to `main` (or the branch the next order names).
2. Build end-check order 4 from its file, then report-back and stop.
3. Iyas merges #26, #27, #28; then rebuild the docx and PDF.
