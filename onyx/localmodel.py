"""Task 39 E (order 2026-11-02-task-39-pre-freeze item E, hq rulings task-39-stops-ruling and -ruling-2): S2 recorded
once on a local model through Ollama (scripts/demo_local.py), read here for docs/site/localmodel.html.

Shown, never scored: eval reads only runs/S*, runs/ungoverned, runs/c4 and runs/c5, so runs/demo-local/ is outside
every figure (tests/test_localmodel.py proves the C5 files unchanged). The page carries configuration and the
log's own steps, verdicts and clauses; no score, count, rate, timing or comparison (Iyas, 2026-11-02)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from onyx import kb, runs

ROOT = kb.REPO / "runs" / "demo-local"
RUN = ROOT / "S2" / "en" / "run1.jsonl"
MACHINE = ROOT / "machine.json"
LABEL = "A demo of the adapter, not of quality: this run is not scored and is not compared with the report's figures."
SKIP = {"run_start", "release_event"}


def machine() -> dict[str, Any]:
    return json.loads(MACHINE.read_text(encoding="utf-8"))


def events(path: Path = RUN) -> list[dict[str, Any]]:
    return runs._events(path)


def rows(path: Path = RUN) -> list[dict[str, Any]]:
    """One row per logged event after the releases: the step, who acted, what, the verdict and the clause ids."""
    out = []
    for e in events(path):
        if e["action"] in SKIP:
            continue
        nv = e["new_value"] if isinstance(e["new_value"], dict) else {}
        row = {"step": e["entity_id"], "actor": e["actor"], "event": e["action"], "verdict": e["verdict"] or "",
               "clauses": list(e["clause_ids"] or []), "note": ""}
        if e["action"] == "propose":
            proposals = nv.get("proposals") or []
            row["proposals"] = len(proposals)
            row["note"] = (", ".join(p["verb"] for p in proposals) if proposals
                           else "; ".join(nv.get("reasoning_chain") or []))
        elif e["action"] == "gate":
            old = e["old_value"] if isinstance(e["old_value"], dict) else {}
            row["note"] = old.get("verb", "")
        else:
            row["note"] = e["reason"] or ""
        out.append(row)
    return out
