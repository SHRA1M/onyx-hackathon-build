"""Model down (order 2026-10-29 Task 29 Part A): the model is down, the gate still decides.

`replay_events(path, at)` replays a recorded run as `whatif.replay_events` does (the same RecordedModel and
RecordedRetriever, a broken chain is never replayed; the setup is copied, runs.py is not edited), with the model
wrapped in `FailingModel`: the call at step `at` raises what OpenAICompatibleModel raises after its last attempt. The
coordinator's except path logs `model_unavailable`, authors a plain-code `escalate_to_human` proposal and submits it
to the gate as a pending proposal; every later step replays from the log as recorded.

`python -m onyx model-down <log> --at <step>` prints the step and writes docs/replay/model-down-<sid>.md,
byte-identical on every run. Fault injection, not a result: the committed logs are unchanged."""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Any

from onyx import audit, kb, runs, whatif
from onyx import model as model_mod

OUT = kb.REPO / "docs" / "replay"
LABEL = "Fault injection: the model call is made to fail at this step; nothing else changes."


def replay_events(path: str | Path, at: int) -> list[dict[str, Any]]:
    """The events of a replay of `path` with the model call at step `at` made to fail."""
    from onyx import coordinator

    if not audit.verify(path):
        raise ValueError(f"{path}: chain broken; not replayed")
    events = runs._events(path)
    config = events[0]["new_value"]
    scenario = runs.recorded_scenario(events)
    # the same reading of the log as runs.replay and whatif.replay_events (copied, runs.py is not edited)
    mandate = any(e["new_value"].get("sources_mandate") for e in events if e["action"] == "propose")
    recorded_mandates = {e["actor"]: e["new_value"]["sources_mandate"] for e in reversed(events)
                         if e["action"] == "propose" and "sources_mandate" in e["new_value"]}
    notes_gaps = any("gaps_source" in e["new_value"] for e in events if e["action"] == "abstain")
    resolve = bool(config.get("clause_resolution"))
    model = model_mod.FailingModel(model_mod.RecordedModel(path), at)
    with tempfile.TemporaryDirectory() as tmp:
        run = coordinator.Coordinator(scenario, model, runs.RecordedRetriever(events),
                                      log_path=Path(tmp) / "replay.jsonl", gaps_dir=Path(tmp) / "gaps",
                                      lang=config.get("lang", "en"), governed=config.get("mode") != "ungoverned",
                                      mandate_clauses=mandate, notes_gaps=notes_gaps,
                                      recorded_mandates=recorded_mandates, resolve_ids=resolve,
                                      recipient_resolution=bool(config.get("recipient_resolution")))
        run.start(**{k: v for k, v in config.items() if k not in runs.REPLAY_SET_KEYS})
        run.run()
        for e in events:
            if e["action"] == "release_event" and e["new_value"]["kind"] == "inject":
                run.inject(e["new_value"]["text"], e["new_value"]["to"])
        return runs._events(run.log.path)


def compare(path: str | Path, at: int) -> tuple[list[tuple[Any, ...]], list[tuple[Any, ...]]]:
    """(recorded, model-down): each decision as (entity_id, action, verdict, clause_ids), in log order."""
    recorded = whatif._decisions(runs._events(path))
    down = whatif._decisions(replay_events(path, at))
    return [whatif._as_tuple(e) for e in recorded], [whatif._as_tuple(e) for e in down]


def _step(entity_id: str) -> int:
    return int(entity_id.split("-")[1])


def _cell(e: dict[str, Any]) -> str:
    agent = e["entity_id"].split("-", 2)[2] if e["entity_id"].count("-") >= 2 else e["actor"]
    if e["action"] == "model_unavailable":
        v = e["new_value"]
        return f"{agent}: `model_unavailable` ({v['error']}, {v['attempts']} attempts)"
    if e["action"] == "gate":
        p = e["old_value"]
        to = f" to {p['target']}" if p["verb"] == "escalate_to_human" else ""
        return f"{agent} `{p['verb']}`{to}: {e['verdict']} ({', '.join(e['clause_ids']) or 'no clause'})"
    return f"{e['actor']} `{e['action']}`: {e['verdict']}"


def _rows(events: list[dict[str, Any]], at: int) -> dict[int, list[str]]:
    rows: dict[int, list[str]] = {}
    for e in events:
        if e["action"] in {*runs.DECISIONS, "model_unavailable"} and _step(e["entity_id"]) >= at:
            rows.setdefault(_step(e["entity_id"]), []).append(_cell(e))
    return rows


def stays(recorded_events: list[dict[str, Any]], down_events: list[dict[str, Any]],
          at: int) -> tuple[int, int, list[str]]:
    """(identical, total, notes) over the decisions outside step `at`. A decision with the same verdict whose clause
    list differs gets a note: an abstention lists every clause the gate cited earlier in the case, so the clauses
    cited only by step `at`'s recorded proposals drop out of it when no model proposed them."""
    recorded = [whatif._as_tuple(e) for e in whatif._decisions(recorded_events) if _step(e["entity_id"]) != at]
    down = [whatif._as_tuple(e) for e in whatif._decisions(down_events) if _step(e["entity_id"]) != at]
    if [r[:3] for r in recorded] != [d[:3] for d in down]:
        raise ValueError("a decision outside the failed step changed verdict; the page would hide it")
    notes = []
    for r, d in zip(recorded, down):
        if r != d:
            gone = [c for c in r[3] if c not in d[3]]
            added = [c for c in d[3] if c not in r[3]]
            notes.append(f"{r[0]} `{r[1]}` keeps its verdict ({r[2]}); its clause list has {len(d[3])} ids, not "
                         f"{len(r[3])}: {', '.join(gone) or 'none'} dropped out"
                         + (f", {', '.join(added)} added" if added else "")
                         + f" (cited only by step {at}'s recorded proposals, which no model made here).")
    return sum(r == d for r, d in zip(recorded, down)), len(recorded), notes


def page_name(path: str | Path) -> str:
    return f"model-down-{runs._events(path)[0]['entity_id']}.md"


def render(path: str | Path, at: int) -> str:
    recorded_events, down_events = runs._events(path), replay_events(path, at)
    sid = recorded_events[0]["entity_id"]
    before, after = _rows(recorded_events, at), _rows(down_events, at)
    same, total, notes = stays(recorded_events, down_events, at)
    lines = [f"# Model down: {sid}, the call at step {at} fails", "",
             f"Run `{whatif._rel(path)}`; {'chain ok' if audit.verify(path) else 'chain BROKEN'}. Replayed "
             "offline from the logged model responses; no model call. The operator, subscriber and numbers are "
             "synthetic.", "",
             LABEL, "",
             f"## Step {at} and after", "",
             "| step | recorded | model-down |", "| --- | --- | --- |"]
    for n in sorted(set(before) | set(after)):
        cells = ["<br>".join(rows.get(n, ["none"])).replace("|", "\\|") for rows in (before, after)]
        lines.append(f"| {sid}-{n} | {cells[0]} | {cells[1]} |")
    lines += ["", "## What stays", "", f"{same} of {total} decisions outside step {at} identical.", "", *(line for note in notes for line in (note, "")),
              f"No model took part in step {at} of the model-down column.", "",
              "Generated by `python -m onyx model-down`; the gate, keys and committed runs are unchanged; this page is "
              "a fault injection, not a result."]
    return "\n".join(lines) + "\n"


def write(path: str | Path, at: int, out: str | Path = OUT) -> Path:
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    page = out / page_name(path)
    page.write_text(render(path, at), encoding="utf-8", newline="\n")
    return page


# --- command line -----------------------------------------------------------------------------------------------

def _cli(args) -> int:
    for cell in _rows(replay_events(args.log, args.at), args.at).get(args.at, []):
        print(f"  {cell}")
    print(whatif._rel(write(args.log, args.at, args.out)))
    return 0


def register(subparsers) -> None:
    parser = subparsers.add_parser("model-down", help="replay a recorded run with one model call made to fail (Task 29)")
    parser.add_argument("log")
    parser.add_argument("--at", type=int, required=True, help="the step whose model call fails")
    parser.add_argument("--out", default=str(OUT), help="where the page goes (default docs/replay)")
    parser.set_defaults(func=_cli)
