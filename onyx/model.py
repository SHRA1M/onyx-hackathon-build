"""Model adapter (order Task 5): one OpenAI-compatible client, RecordedModel (replay from a run log) and MockModel.

Every model returns the API's JSON verbatim as `raw` (chat-completions shape: model, choices[0].message.content).
The agent writes `raw` to the log as `model_response`, so RecordedModel can replay a run without an API key, and
the model id is in every run. The model proposes and explains; it decides nothing.
"""

from __future__ import annotations

import json
import os
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
    """Any OpenAI-compatible chat-completions endpoint. A real call costs money: only with Iyas's go.

    temperature is sent only when given: Anthropic's OpenAI-compatible endpoint returns a 400 for any value below 1
    on Claude 4.7 and later models (platform.claude.com/docs/en/cli-sdks-libraries/libraries/openai-sdk)."""

    def __init__(self, base_url: str, model: str, api_key: str, timeout: float = 600.0,
                 temperature: float | None = None, max_tokens: int = 16000) -> None:
        self.url = base_url.rstrip("/") + "/chat/completions"
        self.model, self.api_key, self.timeout = model, api_key, timeout
        self.temperature, self.max_tokens = temperature, max_tokens

    def complete(self, request_id: str, messages: Messages) -> ModelResponse:
        request: dict[str, Any] = {"model": self.model, "messages": messages, "max_tokens": self.max_tokens}
        if self.temperature is not None:
            request["temperature"] = self.temperature
        body = json.dumps(request).encode("utf-8")
        request = urllib.request.Request(self.url, data=body, method="POST", headers={
            "Content-Type": "application/json", "Authorization": f"Bearer {self.api_key}"})
        with urllib.request.urlopen(request, timeout=self.timeout) as response:
            return ModelResponse(request_id, json.loads(response.read().decode("utf-8")))


ENV_NAMES = ("ONYX_MODEL_BASE_URL", "ONYX_MODEL", "ONYX_MODEL_API_KEY")


class MissingModelKey(RuntimeError):
    """A live run needs ONYX_MODEL_API_KEY with a value; the scripted model never stands in for it."""


def read_env(path: str | Path = ".env") -> dict[str, str]:
    """KEY=VALUE lines of the repo's .env (gitignored), then the process environment. Values are never printed."""
    values: dict[str, str] = {}
    env = Path(path)
    if env.exists():
        for line in env.read_text(encoding="utf-8").splitlines():
            name, sep, value = line.strip().partition("=")
            if sep and not name.startswith("#"):
                values[name.strip()] = value.strip().strip('"').strip("'")
    for name in ENV_NAMES:
        if os.environ.get(name):
            values[name] = os.environ[name]
    return values


def from_env(path: str | Path = ".env") -> OpenAICompatibleModel:
    """The live model (order Task 5, decided 2026-10-21: Claude through Anthropic's OpenAI-compatible endpoint)."""
    values = read_env(path)
    missing = [name for name in ENV_NAMES if not values.get(name)]
    if missing:
        raise MissingModelKey(f"no value in .env for {', '.join(missing)}; live runs stopped (no model call made)")
    return OpenAICompatibleModel(values["ONYX_MODEL_BASE_URL"], values["ONYX_MODEL"], values["ONYX_MODEL_API_KEY"])


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
