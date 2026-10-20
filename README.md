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

## Licence

Code: MIT (see `LICENSE`). Knowledge-base documents remain their publishers'.
