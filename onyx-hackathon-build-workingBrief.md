# Working brief: onyx-hackathon-build

Updated 2026-11-09 (wrap after merging PR #26, Opus). Handover for the next session.

## Objective

Submission day, 2026-11-09. Built work is on `main`. What is left is hq's and Iyas's: PR #28, Pages, film line, the email.

## State

- `main` holds PR #26 (merge `1a6b9f7`); 1199 tests pass, selftest 0.
- PR #28 (`end-check-3-annex`) open, not merged; it carries the annex sentence the README note points to.
- README links to `https://shra1m.github.io/onyx-hackathon-build/site/runs.html`; 404 until Pages is on (docs folder, main).
- Shots folders under `docs/report-back/` are not committed, by design.

## Open questions

1. hq: merge PR #28.
2. Earlier, still open: Task 53 check; Zaid Saaydeh's faculty; gap-15 AI reads; Task 51 items; Task 52 Arabic check.

## Next moves

1. `git status` on `main`.
2. Take only a new order from hq; do not invent work.

## Earlier brief (2026-11-08, from end-check-3-annex)

Updated 2026-11-08 (ninety-first wrap, Opus). Handover for the next session.


hq's end-check orders 4 and 5 (`D:\Projects\hq\uni\ai-for-good-hackathon\end-check-order-*`), one order per session. Then the video. Submission 2026-11-09.


- Three PRs open, none merged: #26 `task-56` (site look, Tasks 56, 56b, 56d), #27 `end-check-2-report-text` (report main text), #28 `end-check-3-annex` (annex).
- #27 and #28 both rebuild `docs/report.docx` from `main`: after the second merge, rebuild it (`uv run python docs/build_report.py`) and run `scripts/report_pages.ps1`. `docs/report.pdf` is behind both.
- This wrap is committed on `end-check-3-annex`.
- Numbers in a `[C3]`/`[C5]` tagged paragraph must be in `eval/results.md`; other counts go in their own untagged paragraph (hq, 2026-11-08).


1. hq: order 2's strip pin now matches "two runs per scenario per language", since cut 2 removed "over the 20 scored runs". Fine?
2. hq: PDF rebuild order after the merges.
3. Earlier, still open: Task 53's one check; Zaid Saaydeh's faculty; gap-15 AI reads; Ra'ed's translations; Task 52 Arabic check.


1. `git status`; switch to `main` (or the branch the next order names).
2. Build end-check order 4 from its file, then report-back and stop.
3. Iyas merges #26, #27, #28; then rebuild the docx and PDF.
