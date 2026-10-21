"""Audit log (order Task 4): every step appended to a hash-chained JSONL file, and the replay store.

hash = sha256(prev_hash + canonical_json(event without 'hash')); the first prev_hash is 64 zeros. Editing,
inserting or deleting any line breaks the chain from that line on, and `verify-log` names the first broken seq.
"""

import hashlib
import json
from collections.abc import Callable, Iterator
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from onyx import data

GENESIS = "0" * 64
FIELDS = ("seq", "ts", "prev_hash", "hash", "actor", "action", "entity_type", "entity_id", "old_value",
          "new_value", "source", "reason", "clause_ids", "quote", "verdict", "model_request_id", "model_response",
          "gate_ms", "model_ms")  # addendum 18: decision time and model time, in milliseconds


def canonical_json(event: dict[str, Any]) -> str:
    return json.dumps(event, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def event_hash(prev_hash: str, event: dict[str, Any]) -> str:
    body = {k: v for k, v in event.items() if k != "hash"}
    return hashlib.sha256((prev_hash + canonical_json(body)).encode("utf-8")).hexdigest()


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


def key_hashes() -> dict[str, str]:
    """sha256 of every answer key as it is on disk, not as HASHES.txt says: eval compares the two."""
    return {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(data.KEYS_DIR.glob("S*.json"))}


class AuditLog:
    def __init__(self, path: str | Path, clock: Callable[[], str] = _now) -> None:
        self.path = Path(path)
        self.clock = clock
        self.seq, self.last_hash = 0, GENESIS
        if self.path.exists():
            for line in self.path.read_text(encoding="utf-8").splitlines():
                event = json.loads(line)
                self.seq, self.last_hash = event["seq"], event["hash"]

    def start(self, scenario_id: str, actor: str = "coordinator", config: dict[str, Any] | None = None) -> str:
        """The run_start event: the sha256 of every answer key, so a run proves which keys it was scored against,
        and the run's configuration (language, mode, model) when given."""
        return self.append({"actor": actor, "action": "run_start", "entity_type": "scenario", "entity_id": scenario_id,
                            "new_value": {"answer_keys": key_hashes(), **(config or {})}, "source": "onyx/data/keys"})

    def append(self, event: dict[str, Any]) -> str:
        record: dict[str, Any] = {field: None for field in FIELDS}
        record["clause_ids"] = []
        record.update(event)
        record.update(seq=self.seq + 1, ts=event.get("ts") or self.clock(), prev_hash=self.last_hash)
        record["hash"] = event_hash(self.last_hash, record)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8", newline="\n") as f:
            f.write(canonical_json(record) + "\n")
        self.seq, self.last_hash = record["seq"], record["hash"]
        return record["hash"]


def first_break(path: str | Path) -> int | None:
    """The line number (= the seq it should hold) of the first line that does not chain, or None."""
    prev = GENESIS
    for n, line in enumerate(Path(path).read_bytes().decode("utf-8", errors="replace").splitlines(), start=1):
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            return n
        if event.get("seq") != n or event.get("prev_hash") != prev or event.get("hash") != event_hash(prev, event):
            return n
        prev = event["hash"]
    return None


def verify(path: str | Path) -> bool:
    return first_break(path) is None


def iter_model_responses(path: str | Path) -> Iterator[tuple[str, Any]]:
    """(model_request_id, model_response) in log order, for RecordedModel. A broken chain is never replayed."""
    broken = first_break(path)
    if broken is not None:
        raise ValueError(f"{path}: chain broken at seq {broken}; not replayed")
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        event = json.loads(line)
        if event.get("model_response") is not None:
            yield event["model_request_id"], event["model_response"]


def _cli(args) -> int:
    broken = first_break(args.file)
    if broken is None:
        print("chain ok")
        return 0
    print(f"chain broken: first broken seq {broken} ({args.file}, line {broken})")
    return 1


def register(subparsers) -> None:
    parser = subparsers.add_parser("verify-log", help="check a run log's hash chain")
    parser.add_argument("file")
    parser.set_defaults(func=_cli)
