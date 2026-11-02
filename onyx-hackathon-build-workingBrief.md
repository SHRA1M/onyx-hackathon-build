# Working brief: onyx-hackathon-build

Updated 2026-11-02 (fifty-seventh wrap, Opus). Handover for the next session.

## Objective

Finish Task 39 item E (`docs/work-orders/2026-11-02-task-39-pre-freeze.md` item E, as amended by hq's
`task-39-stops-ruling-2026-11-02.md` and `task-39-stops-ruling-2-2026-11-02.md`) on branch `task-36`, so PR #13
carries Tasks 36 to 39. E due 2026-11-04 end of day or dropped; freeze 2026-11-06; submission 2026-11-09.

## State

- A to D built, B's Annex A sentence included. Pushed; CI green at `61460dd`; head `42fcc67` plus this wrap. 670
  tests. Word main 5 pages, annex from page 6, 10 pages; PDF 10 pages.
- E: ruled (32k context, flash attention, q8_0 cache; 14B, then 7B). `scripts/demo_local.py` written, never run.
  Iyas is downloading `qwen2.5:14b-instruct` in his own PowerShell window (about 4 hours at 500 KB/s).

## Open questions

- hq: confirm the strict "carried" reading (23 en / 36 ar, not stop 3's 27 / 44), question 1 in the B5 section of
  `docs/report-back/2026-11-02-task-39-pre-freeze.md`.
- Iyas: open `docs/report.pdf`, then send the reviewer email (clear now; target 2026-11-03).

## Next moves

1. `git status`, `git pull` on `task-36`. Wait for Iyas's go; check `ollama list` shows the 14B.
2. Stop the tray app's Ollama server; start `ollama serve` as a background task with `OLLAMA_CONTEXT_LENGTH=32768`,
   `OLLAMA_FLASH_ATTENTION=1`, `OLLAMA_KV_CACHE_TYPE=q8_0`, its output to a log file (for GPU layers).
   `curl http://localhost:11434/v1/models`.
3. `uv run python scripts/demo_local.py qwen2.5:14b-instruct` (prints seconds per call). 7B fallback on a load
   failure, a step over 30 minutes, or over half unparseable.
4. `verify-log`; a test that `eval` ignores `runs/demo-local/`; `docs/site/localmodel.html` (no figure); README line
   under "Model"; Annex A sentence; rebuild report and PDF; full tests; push; CI; E report-back.
