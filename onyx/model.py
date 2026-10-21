"""Model adapter (order Task 5): one OpenAI-compatible client, RecordedModel (replay from a run log) and MockModel.

Every model returns the API's JSON verbatim as `raw` (chat-completions shape: model, choices[0].message.content).
The agent writes `raw` to the log as `model_response`, so RecordedModel can replay a run without an API key, and
the model id is in every run. The model proposes and explains; it decides nothing.
"""

from __future__ import annotations

import json
import urllib.request
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

from onyx import audit

Messages = list[dict[str, str]]


@dataclass
class ModelResponse:
    request_id: str
    raw: dict[str, Any]

    @property
    def model(self) -> str:
        return self.raw.get("model", "")

    @property
    def text(self) -> str:
        return self.raw["choices"][0]["message"]["content"]


class Model(Protocol):
    def complete(self, request_id: str, messages: Messages) -> ModelResponse: ...


def _chat_completion(model: str, text: str) -> dict[str, Any]:
    return {"model": model, "choices": [{"index": 0, "message": {"role": "assistant", "content": text}}]}


class OpenAICompatibleModel:
    """Any OpenAI-compatible chat-completions endpoint. A real call costs money: only with Iyas's go."""

    def __init__(self, base_url: str, model: str, api_key: str, timeout: float = 120.0) -> None:
        self.url = base_url.rstrip("/") + "/chat/completions"
        self.model, self.api_key, self.timeout = model, api_key, timeout

    def complete(self, request_id: str, messages: Messages) -> ModelResponse:
        body = json.dumps({"model": self.model, "messages": messages, "temperature": 0}).encode("utf-8")
        request = urllib.request.Request(self.url, data=body, method="POST", headers={
            "Content-Type": "application/json", "Authorization": f"Bearer {self.api_key}"})
        with urllib.request.urlopen(request, timeout=self.timeout) as response:
            return ModelResponse(request_id, json.loads(response.read().decode("utf-8")))


class RecordedModel:
    """Replays the responses of a committed run by model_request_id. A broken chain is never replayed."""

    def __init__(self, log_path: str | Path) -> None:
        self.responses = dict(audit.iter_model_responses(log_path))

    def complete(self, request_id: str, messages: Messages) -> ModelResponse:
        if request_id not in self.responses:
            raise KeyError(f"{request_id}: not in the recorded run")
        return ModelResponse(request_id, self.responses[request_id])


Script = Mapping[str, str | dict[str, Any]] | Callable[[str, Messages], str | dict[str, Any]]


class MockModel:
    """Offline and deterministic, for tests and selftest. `script` maps a request id to the reply (text, or a dict
    sent as JSON), or is a function of (request_id, messages). An unscripted request gets no proposals."""

    def __init__(self, script: Script | None = None, model: str = "mock") -> None:
        self.script, self.model = script or {}, model

    def complete(self, request_id: str, messages: Messages) -> ModelResponse:
        if callable(self.script):
            reply = self.script(request_id, messages)
        else:
            reply = self.script.get(request_id, {"proposals": [], "reasoning_chain": ["mock: nothing scripted"]})
        text = reply if isinstance(reply, str) else json.dumps(reply, ensure_ascii=False)
        return ModelResponse(request_id, _chat_completion(self.model, text))
