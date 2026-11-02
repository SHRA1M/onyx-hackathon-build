# Report-back: Task 39 item E, the local-model demo (2026-11-02, Opus, stopped before the run)

Order: `docs/work-orders/2026-11-02-task-39-pre-freeze.md` item E, as amended by hq's
`task-39-stops-ruling-2026-11-02.md` ("E: the model"). Nothing of E is in the repo but this file.

## Done so far

1. `winget install --id Ollama.Ollama -e` -> `Found Ollama [Ollama.Ollama] Version 0.40.13` ... `Successfully
   installed`. No elevation prompt. The server answers: `GET http://localhost:11434/api/version` ->
   `{"version":"0.40.13"}`.
2. Machine as printed: `NVIDIA GeForce RTX 3060, 12288 MiB` (`nvidia-smi`), RAM `15.9` GB (`Win32_ComputerSystem`).
3. `ollama pull qwen2.5:14b-instruct`: started, then stopped by Claude Code because the PC ran low on memory while the session was idle (not an Ollama error). Not restarted; it waits for Iyas's go. The model is not on disk complete, so `/v1/models` was not checked.

## Stop 1: the longest S2 prompt does not fit either context length the ruling allows

The ruling: measure the longest prompt in `runs/c5/S2/run1.jsonl`, then start Ollama with `OLLAMA_CONTEXT_LENGTH` at
"the smallest of 8192 or 16384 that holds it with room for the 16,000 `max_tokens`".

The log has no `prompt` field (a propose event's `new_value` holds `agent_name`, `gaps_in_notes`, `proposals`,
`reasoning_chain`, `rejected`, `sources_mandate`, `sources_used`). The size is in each reply's `usage`, counted by
Claude's tokenizer:

```
S2-2-care     prompt_tokens 29316  completion_tokens 1003
S2-3-care     prompt_tokens 26464  completion_tokens 1608
S2-4-care     prompt_tokens 29013  completion_tokens 1084
S2-5-adviser  prompt_tokens  4577  completion_tokens  895
S2-6-tdra     prompt_tokens 15875  completion_tokens  369
```

Care's prompt is about 29,000 tokens (its mandate lists about 90 clauses since prompt v4). Neither 8,192 nor 16,384
holds it, and with 16,000 for the reply the need is about 45,000. Below 29,000, Ollama truncates the prompt silently,
which the ruling exists to prevent.


Options, for hq:
- (a) `OLLAMA_CONTEXT_LENGTH=32768`, the model's own window. It holds the prompt, with about 3,000 tokens left for
  the reply; the replies in this log are 369 to 1,608 tokens. The 16,000 `max_tokens` would not fit in the window
  (Ollama setting, adapter unchanged). The longer cache may not fit the 12 GB card beside the 9 GB model, so Ollama
  would put some layers on the CPU: slow, which the ruling allows. Two more Ollama settings would shrink the cache
  without touching the adapter: `OLLAMA_FLASH_ATTENTION=1` and `OLLAMA_KV_CACHE_TYPE=q8_0`. Not tried.
- (b) Drop E: "tried on 2026-11-02, not shown".

Question for hq: 1. (a), (a) with the two cache settings, or (b)? Recommendation: (a) with the two cache settings,
since none of them changes the adapter, the prompt or a gate. The deadline stays 2026-11-04 end of day.

## Limits kept

0 USD spent. No run recorded, no file in `runs/demo-local/`, no adapter, prompt, gate or key change. The model and
Ollama are on this PC only; nothing has reached anyone outside the team.

## After ruling 2 (`task-39-stops-ruling-2-2026-11-02.md`, 2026-11-02, fifty-seventh session)

Question 1 answered: (a) with the two cache settings. Not run yet.

- `ollama --version` -> `ollama version is 0.40.13`. `ollama list` -> no models.
- The re-pull was stopped by Claude Code on low memory again (3.7 GB free of 15.9 GB after; no single large
  process). A foreground pull from the session ran at about 500 KB/s (estimate about 4 hours, restarted at 1.1 GB of
  9.0 GB) and was stopped on Iyas's word: he downloads in his own PowerShell window.
- `scripts/demo_local.py` written: it drives the same `Coordinator` that `record` uses, through the unchanged
  `OpenAICompatibleModel`, to `runs/demo-local/S2/<lang>/run1.jsonl`, and prints seconds per call. `record` is not
  used because its spend guard refuses a model with no price row (`cost.guard`), and adding one would be a data
  change. Not run; no file in `runs/demo-local/`.
- The adapter's request timeout is 600 s with four attempts, so a stalled call can take up to 40 minutes before
  it raises. That is above ruling 2's 30-minute step limit; the wall time per call is printed, so a call over 30
  minutes is seen and the 7B fallback taken.

Limits kept: USD 0, no hosted model, no sign-in to ollama.com, no adapter, prompt, gate or key change.

## E recorded (2026-11-02, fifty-eighth session, Opus)

Ruling 2 followed: 14B, the three settings, no fallback needed.

- `ollama list` -> `qwen2.5:14b-instruct  7cdf5a0187d5  9.0 GB` (Iyas's download). Tray server stopped; `ollama serve`
  started with the settings; its log: `OLLAMA_CONTEXT_LENGTH:32768`, `OLLAMA_FLASH_ATTENTION:true`,
  `OLLAMA_KV_CACHE_TYPE:q8_0`. `/v1/models` lists the 14B.
- For this report-back only, never the page: GPU layers `offloaded 42/49 layers to GPU` (CUDA0 7,020 MiB, host
  1,546 MiB). Wall time per call: S2-2-care 189 s, S2-3-care 47 s, S2-4-care 73 s, S2-5-adviser 13 s, S2-6-tdra 45 s.
  No step near 30 minutes.
- Parseable: 4 of 5 model steps. S2-2-care returned JSON outside the agreed schema (logged "unparseable model
  response: no JSON in the agreed schema"), so it proposed nothing. Not more than half: step 5's drop test not met.
- No endpoint error; the adapter's `max_tokens` and JSON mode were accepted as they are.
- `verify-log runs/demo-local/S2/en/run1.jsonl` -> `chain ok`.
- Arabic S2 not run: the order runs it only if the English run completes "with every step decided", and S2-2 reached
  no gate.

Built: `runs/demo-local/S2/en/run1.jsonl`; `runs/demo-local/machine.json` (tag, Ollama version, GPU and RAM as
printed, the three settings; configuration only); `onyx/localmodel.py`; `docs/site/localmodel.html` (eighth page,
nav "Local model", index card; the label, the machine line, every logged step with verdict and clauses; no figure);
the README line under "Model"; the Annex A sentence, filled with `qwen2.5:14b-instruct`;
`tests/test_localmodel.py` (7 tests, including eval over `runs/` writing the committed `eval/results.json` and
`results.md` byte for byte, and a whole-word check that the page carries no score, rate, timing or token word);
`tests/test_site.py` lists eight pages.

Checks: 677 passed (670 before). `check-data ok`. `eval --runs runs --out eval` left `eval/` unchanged. CI's
generators rerun locally: no drift beyond this change. Word: main 5 pages, 2,366 words, annex from page 6, 10 pages,
5,236 words; PDF 10 pages, 359,007 bytes.

Departure from the order: none of substance. The machine values sit in `runs/demo-local/machine.json` so the page
reads them rather than typing them, and the site stays byte-identical on any machine.

Open: after E, the Ollama models move to D (ruling 2, "After E"): a script with a backup, Iyas runs one line. The
`ollama serve` this session started is still running with the three settings; the tray app is closed.
