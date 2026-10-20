# onyx-hackathon-build

Mizan, team Onyx's entry to the ITU AI for Good Lab Hackathon UAE 2026 (telecom track T1). A synthetic UAE operator's consumer-care AI: five agents propose JSON actions, `gate.py` (the Y.3172 P node) decides in plain code from clauses of binding UAE text, every step lands in a hash-chained log. Readers: the hackathon judges, then ITU. Built by Iyas alone. Submission 2026-11-09.

## Session start

1. `git status`; name anything uncommitted or unpushed.
2. Read `onyx-hackathon-build-workingBrief.md`, then the latest order in `docs/work-orders/`. The order is the contract: build it task by task, nothing more.
3. Thinking and every business fact live in `D:\Projects\hq\uni\ai-for-good-hackathon\`. A rule, figure, name or date missing from the order's sources table: name `D:\Projects\hq\uni` and stop.

## Stack

Python 3.12 (uv-managed), `uv`, ChromaDB, `pytest`, Rich. One OpenAI-compatible model adapter with `RecordedModel` (replay) and `MockModel` (tests). CLI only.

## Commands

- Install: `uv venv --python 3.12` then `uv pip install -e ".[dev]"`
- Test: `uv run pytest`
- Run: `uv run python -m onyx <command>` (`--help` lists the commands)

## Where things live

- `docs/work-orders/`: dated orders, frozen once committed.
- `onyx/`: the package. `onyx/data/`: mandates, rules, scenarios, answer keys.
- `kb/`: manifest and clause chunks (committed); `kb/sources/` full texts (fetched, gitignored).
- `runs/`: recorded run logs, committed with their model responses.
- `CHANGELOG.md`: one entry per fix.

## Conventions

- Decisions are plain code. The model proposes and explains; the gate decides.
- Every rule, figure and name traces to the order's sources table, quoted verbatim. `check-data` proves it.
- Tests run on `MockModel`. A real model call waits for Iyas's go and a cost estimate.
- Test first (`/tdd`): see it fail, then pass.
- Operator, subscribers and numbers are synthetic and labelled so.
- Files are LF (`.gitattributes`), so hashes match on every machine.

## Do not touch

- `docs/work-orders/*`: a change of direction is a new dated order.
- `onyx/data/keys/*` once `HASHES.txt` is committed, and committed files in `runs/`: the hashes and chain prove they were never edited.
- `.env`: keys only, never committed, never printed.
- Remote and visibility: private until 2026-11-09; create or push only with Iyas's go.
