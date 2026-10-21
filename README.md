# Mizan

> **Synthetic data.** The operator, subscribers and numbers in this repo are synthetic. The law texts are real, public, linked and hashed. No consumer data.

Team Onyx's entry to the ITU AI for Good Lab Hackathon UAE 2026 (telecom track). A consumer-care AI for a synthetic UAE operator: agents propose actions, plain-code gates written from binding UAE text decide, and every step is written to a hash-chained log.

Built by Team Onyx.

## Setup from a fresh clone

Needs [uv](https://docs.astral.sh/uv/).

```
uv venv --python 3.12
uv pip install -e ".[dev]"
uv run pytest
uv run python -m onyx --help
```

## Model

- Model: `claude-sonnet-5-5`, through Anthropic's OpenAI-compatible endpoint `https://api.anthropic.com/v1/`
  (`onyx/model.py`, one adapter for every model).
- Prices: https://platform.claude.com/docs/en/about-claude/pricing, read 2026-10-21 (`onyx/data/model_prices.json`).
- Bake-off: [`eval/bakeoff.md`](eval/bakeoff.md), one governed run per scenario (S1 to S5) per language per model.
- Scored run: [`eval/results.md`](eval/results.md), Sonnet on prompt v3, three runs per scenario per mode per language.

The adapter takes any OpenAI-compatible endpoint; a UAE-hosted Jais 3 or Falcon-H1 Arabic served through vLLM
exposes the same API, so the provider is three values in `.env`.

Bake-off rows (English / Arabic), copied from `eval/bakeoff.md`:

| Row | Opus 5.5 v1 | Sonnet 5.5 v1 | Haiku 5.5 v1 | Sonnet 5.5 v2 | Haiku 5.5 v2 |
|---|---|---|---|---|---|
| Citation validity | 1.00 / 0.88 | 1.00 / 1.00 | 0.97 / 0.97 | 0.97 / 1.00 | 0.92 / 0.95 |
| Action recall | 0.29 / 0.10 | 0.43 / 0.17 | 0.47 / 0.32 | 0.70 / 0.48 | 0.45 / 0.39 |
| Obligation proxy | 0.10 / 0.04 | 0.17 / 0.23 | 0.17 / 0.16 | 0.23 / 0.35 | 0.23 / 0.29 |
| Gap recall | 0.00 / 0.00 | 0.00 / 0.00 | 0.00 / 0.00 | 0.47 / 0.00 | 0.20 / 0.00 |
| JSON parse failures | 18 of 26 / 20 of 26 | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 |
| Replies stopped by the endpoint | 18 of 26 / 20 of 26 | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 |
| Cost, 10 runs (USD) | 0.91 | 0.63 | 0.04 | 0.86 | 0.05 |

Prompt v1 is commit d85871d, v2 is a8f4acb. In v2 the Arabic gap ids were present in the replies' notes in 10 of
10 runs but scored 0; prompt v3 asks for them as `flag_gap` proposals.

With prompt v1, the endpoint stopped 38 of 52 Opus replies (content_filter). With prompt v2, which renamed the
`reasoning_chain` field and added instructions and clause text, 0 of 10 were stopped
(`runs/opus-filter-v2/S2/run1.jsonl`, `runs/opus-filter-v2/S2/ar/run1.jsonl`). The cause is not isolated. Where a
reply was stopped, the adapter recorded the reason, the reply proposed nothing, the gate saw no malformed action,
and the run went on.

## Licence

Code: MIT (see `LICENSE`). Knowledge-base documents remain their publishers'.
