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
