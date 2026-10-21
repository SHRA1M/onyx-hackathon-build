"""Tokens, cost and the spend guard (Task 8 live-run order, 2026-10-21, Part A).

Every model call's reply is logged verbatim as `model_response`; a chat-completions reply carries `usage`
(prompt_tokens, completion_tokens). Cost is priced from onyx/data/model_prices.json, quoted from Anthropic's pricing
page. A model id with no price row is "price unknown", never zero.

The guard runs before a live run's first call. Its estimate is calls x tokens x price:
- calls and prompt size come from a dry pass that builds the exact prompts the live run will send (the scripted
  model stands in, no call made), converted at the pricing page's own ratio, 10 kB to about 2,500 tokens;
- once a live run of the same model is recorded, its median prompt and completion tokens per call replace that, so
  output is counted from then on (Iyas, 2026-10-21: live-shape prompts, output added once measured).
It refuses a run whose estimate is over --max-usd (default USD 5), or that would take recorded live spend past USD 15.
"""

from __future__ import annotations

import json
import tempfile
from collections.abc import Callable, Iterator
from dataclasses import dataclass, field
from pathlib import Path
from statistics import median
from typing import Any

from onyx import data

PRICES_PATH = data.DATA_DIR / "model_prices.json"
RUNS_DIR = Path(__file__).resolve().parents[1] / "runs"
DEFAULT_MAX_USD = 5
TOTAL_CAP_USD = 15  # the key's cap is USD 20; the order stops at 15
BYTES_PER_TOKEN = 4


class SpendRefused(RuntimeError):
    """A live run that would cost more than allowed, or whose cost cannot be priced. No model call was made."""


def load_prices() -> dict[str, Any]:
    return json.loads(PRICES_PATH.read_text(encoding="utf-8"))


def _usd(value: float) -> str:
    return f"${value:g}" if float(value).is_integer() else f"${value:.2f}"


def check_prices() -> list[str]:
    """Each price must appear in its row's verbatim quote from the pricing page."""
    prices, problems = load_prices(), []
    for model_id, row in prices["models"].items():
        for name in ("usd_per_mtok_in", "usd_per_mtok_out"):
            if f"{_usd(row[name])} / MTok" not in row["quote"]:
                problems.append(f"prices: {model_id} {name} {row[name]} is not in its quote")
    ratio = prices["bytes_per_token"]
    if ratio["value"] != BYTES_PER_TOKEN or "10 kB" not in ratio["quote"] or "2,500 tokens" not in ratio["quote"]:
        problems.append("prices: bytes_per_token does not match its quote (10 kB, about 2,500 tokens)")
    return problems


def cost_usd(model_id: str, prompt_tokens: int, completion_tokens: int) -> float | None:
    row = load_prices()["models"].get(model_id)
    if row is None or prompt_tokens > row.get("max_prompt_tokens", prompt_tokens):
        return None
    return (prompt_tokens * row["usd_per_mtok_in"] + completion_tokens * row["usd_per_mtok_out"]) / 1e6


# --- recorded usage -------------------------------------------------------------------------------------------

def _events(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def call_usage(events: list[dict[str, Any]]) -> list[tuple[int, int] | None]:
    """(prompt_tokens, completion_tokens) per model call, None where the reply carries no usage."""
    out = []
    for e in events:
        if e.get("model_response") is not None:
            usage = e["model_response"].get("usage") or {}
            ok = isinstance(usage.get("prompt_tokens"), int) and isinstance(usage.get("completion_tokens"), int)
            out.append((usage["prompt_tokens"], usage["completion_tokens"]) if ok else None)
    return out


def run_usage(events: list[dict[str, Any]]) -> dict[str, Any]:
    """calls, prompt and completion tokens, cost in USD (None: no usage recorded, or price unknown)."""
    usage, model_id = call_usage(events), events[0]["new_value"].get("model", "")
    known = bool(usage) and all(u is not None for u in usage)
    prompt = sum(u[0] for u in usage) if known else None
    completion = sum(u[1] for u in usage) if known else None
    priced = [cost_usd(model_id, *u) for u in usage] if known else [None]
    return {"calls": len(usage), "prompt_tokens": prompt, "completion_tokens": completion,
            "cost_usd": round(sum(priced), 6) if None not in priced else None}


def live_runs(root: str | Path) -> Iterator[tuple[Path, list[dict[str, Any]]]]:
    for path in sorted(Path(root).rglob("run*.jsonl")) if Path(root).exists() else []:
        events = _events(path)
        if events and events[0]["action"] == "run_start" and events[0]["new_value"].get("source") == "live":
            yield path, events


def spent_usd(root: str | Path) -> float:
    """Recorded live spend under root. A run with no usage or no price adds nothing, so the guard refuses
    unpriced models before they run."""
    return round(sum(run_usage(events)["cost_usd"] or 0 for _, events in live_runs(root)), 6)


# --- the estimate ---------------------------------------------------------------------------------------------

@dataclass
class Plan:
    calls: int
    prompt_bytes: list[int] = field(default_factory=list)

    @property
    def prompt_tokens(self) -> int:
        return round(median(self.prompt_bytes) / BYTES_PER_TOKEN) if self.prompt_bytes else 0


def plan(scenarios: tuple[str, ...], langs: tuple[str, ...], modes: tuple[str, ...], runs: int,
         retriever: Any = None) -> Plan:
    """Dry pass: one run per scenario, language and mode with the scripted model, recording the size of every
    prompt the live run would send (live retrieval unless a retriever is given). No model call."""
    from onyx import coordinator, scripted

    class Capture:
        def __init__(self, inner) -> None:
            self.inner, self.sizes = inner, []

        def complete(self, request_id, messages):
            self.sizes.append(len(json.dumps(messages, ensure_ascii=False).encode("utf-8")))
            return self.inner.complete(request_id, messages)

    retrieve = retriever or coordinator._kb_retriever()
    sizes: list[int] = []
    calls = 0
    for sid in scenarios:
        for mode in modes:
            for lang in langs:
                capture = Capture(scripted.model(sid, lang))
                with tempfile.TemporaryDirectory() as tmp:
                    run = coordinator.Coordinator(data.load_scenario(sid), capture, retrieve,
                                                  log_path=Path(tmp) / "plan.jsonl", gaps_dir=Path(tmp) / "gaps",
                                                  lang=lang, governed=mode == "governed")
                    run.start(source="plan")
                    run.run()
                sizes += capture.sizes
                calls += len(capture.sizes) * runs
    return Plan(calls, sizes)


@dataclass
class Estimate:
    model: str
    calls: int
    prompt_tokens: int
    completion_tokens: int | None  # None until a live run of this model is recorded
    usd: float | None  # None: price unknown
    spent_usd: float
    basis: str

    def line(self, max_usd: float) -> str:
        cost = ("price unknown" if self.usd is None
                else f"USD {self.usd:.2f}" if self.usd >= 0.01 else f"USD {self.usd:.4f}")
        output = (f" + {self.completion_tokens} completion tokens" if self.completion_tokens is not None
                  else "; output not included until a live run of this model is recorded")
        return (f"Estimate before the first call: {self.calls} calls x {self.prompt_tokens} prompt tokens{output} "
                f"({self.basis}), model {self.model}: {cost}. Run cap USD {max_usd:.2f}; recorded live spend "
                f"USD {self.spent_usd:.2f} of {TOTAL_CAP_USD}.")


def estimate(model_id: str, run_plan: Plan, spend_root: str | Path = RUNS_DIR) -> Estimate:
    recorded = [u for _, events in live_runs(spend_root) if events[0]["new_value"].get("model") == model_id
                for u in call_usage(events) if u is not None]
    if recorded:
        prompt, completion = round(median(u[0] for u in recorded)), round(median(u[1] for u in recorded))
        basis = f"medians of {len(recorded)} recorded live calls"
    else:
        prompt, completion = run_plan.prompt_tokens, None
        basis = f"median live-shape prompt, {BYTES_PER_TOKEN} bytes per token"
    per_call = cost_usd(model_id, prompt, completion or 0)
    usd = None if per_call is None else round(run_plan.calls * per_call, 6)
    return Estimate(model_id, run_plan.calls, prompt, completion, usd, spent_usd(spend_root), basis)


def guard(model_id: str, run_plan: Plan, max_usd: float = DEFAULT_MAX_USD, spend_root: str | Path = RUNS_DIR,
          out: Callable[[str], Any] = print) -> Estimate:
    """Print the estimate, then refuse (SpendRefused) or return it. Runs before the first call."""
    est = estimate(model_id, run_plan, spend_root)
    out(est.line(max_usd))
    if est.usd is None:
        raise SpendRefused(f"{model_id}: price unknown (no row in onyx/data/model_prices.json); no call made")
    if est.usd > max_usd:
        raise SpendRefused(f"estimate USD {est.usd:.2f} is over the run cap USD {max_usd:.2f} (--max-usd); "
                           "no call made")
    if est.spent_usd + est.usd > TOTAL_CAP_USD:
        raise SpendRefused(f"recorded spend USD {est.spent_usd:.2f} + estimate USD {est.usd:.2f} would pass "
                           f"USD {TOTAL_CAP_USD}; no call made")
    return est
