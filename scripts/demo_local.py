"""Task 39 E (ruling task-39-stops-ruling-2-2026-11-02): record S2 once on a local model through Ollama.

Shown, never scored. The existing adapter (onyx.model.OpenAICompatibleModel), prompt, gates and keys, unchanged;
the run goes through the same Coordinator `record` uses. `record` is not used because its spend guard refuses a
model with no price row, and a price row would be a data change. Ollama must already be serving with
OLLAMA_CONTEXT_LENGTH=32768, OLLAMA_FLASH_ATTENTION=1 and OLLAMA_KV_CACHE_TYPE=q8_0 (Ollama settings, not code).

    uv run python scripts/demo_local.py qwen2.5:14b-instruct [--lang en]

Writes runs/demo-local/S2/<lang>/run1.jsonl; never overwrites. Prints the wall time per model call (for the
report-back only, never the page).
"""

from __future__ import annotations

import argparse
import time
from pathlib import Path

from onyx import coordinator, data
from onyx.agents.base import PROMPT_VERSION
from onyx.model import OpenAICompatibleModel

BASE_URL = "http://localhost:11434/v1"  # Ollama on this PC; nothing leaves the machine
ROOT = Path("runs/demo-local")


class Timed:
    def __init__(self, inner: OpenAICompatibleModel) -> None:
        self.inner, self.model = inner, inner.model

    def complete(self, request_id, messages):
        start = time.monotonic()
        try:
            return self.inner.complete(request_id, messages)
        finally:
            print(f"{request_id}: {time.monotonic() - start:.0f} s", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("tag")
    parser.add_argument("--lang", choices=("en", "ar"), default="en")
    args = parser.parse_args()
    path = ROOT / "S2" / args.lang / "run1.jsonl"
    if path.exists():
        raise SystemExit(f"{path}: a recorded run is never overwritten")
    model = Timed(OpenAICompatibleModel(BASE_URL, args.tag, "ollama"))
    run = coordinator.Coordinator(data.load_scenario("S2"), model, coordinator._kb_retriever(), log_path=path,
                                  gaps_dir=ROOT / "gaps", lang=args.lang, governed=True)
    run.start(source="live", model=args.tag, run=1, retrieval="kb_main", prompt=PROMPT_VERSION)
    for step in run.run():
        print(step, flush=True)
    print(f"written {path}")


if __name__ == "__main__":
    main()
