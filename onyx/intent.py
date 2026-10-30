"""ML Intent (order 2026-10-29-task-29 Part C3): `python -m onyx intent` writes docs/intent.json, the Y.3172 MLFO's
intent for Mizan, read from the committed data: manifest ids by node, the agents with their verbs and document sets,
the model and prompt the C5 runs recorded, the gate's version (sha256 of onyx/gate.py, which has no version number),
the key hashes, the four verdicts and the scenario ids. Nothing reads it at run time. Byte-identical on every run."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from onyx import data, gate, kb, runs

OUT = kb.REPO / "docs" / "intent.json"
GATE = kb.REPO / "onyx" / "gate.py"
KEYS = data.DATA_DIR / "keys" / "HASHES.txt"
NOTE = ("ML Intent, written by `python -m onyx intent` from the committed data. Nothing reads this file at run time: "
        "the coordinator, agents and gate read their own files; this is the record of what they read.")


def _c5() -> dict[str, str]:
    """The model and prompt every C5 run's run_start records; ValueError if the runs disagree."""
    seen = {(e["new_value"]["model"], e["new_value"]["prompt"])
            for p in sorted((kb.REPO / "runs" / "c5").rglob("*.jsonl")) for e in runs._events(p)[:1]}
    if len(seen) != 1:
        raise ValueError(f"C5 runs record {len(seen)} model and prompt pairs")
    model, prompt = seen.pop()
    return {"model": model, "prompt": prompt}


def build() -> dict[str, Any]:
    by_node: dict[str, list[str]] = {}
    for row in kb.load_manifest():
        by_node.setdefault(row["node"] or "none", []).append(row["document_id"])
    mandates = json.loads((data.DATA_DIR / "mandates.json").read_text(encoding="utf-8"))["agents"]
    hashes = [line.split() for line in KEYS.read_text(encoding="utf-8").splitlines() if line.strip()]
    return {
        "note": NOTE,
        "manifest_by_node": dict(sorted(by_node.items())),
        "agents": {a: {"verbs": m["verbs"], "documents": m["documents"]} for a, m in mandates.items()},
        "c5": _c5(),
        "gate": {"file": "onyx/gate.py", "sha256": kb.sha256_file(GATE)},
        "key_hashes": {name: sha for sha, name in hashes},
        "verdicts": [gate.ALLOW, gate.HOLD, gate.BLOCK, gate.INSUFFICIENT],
        "scenarios": sorted(p.stem for p in data.SCENARIOS_DIR.glob("S*.json")),
    }


def write(out: str | Path = OUT) -> Path:
    out = Path(out)
    out.write_text(json.dumps(build(), ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    return out


def register(subparsers) -> None:
    parser = subparsers.add_parser("intent", help="write docs/intent.json, the ML Intent, from the committed data")
    parser.set_defaults(func=_cli)


def _cli(args) -> int:
    print(write().relative_to(kb.REPO).as_posix())
    return 0
