"""Runs and replay (order Task 8).

`record` writes three runs per scenario per mode per language: governed English at runs/S1/run1.jsonl (the order's
path), governed Arabic at runs/S1/ar/run1.jsonl, ungoverned under runs/ungoverned/ in the same shape. A live run
uses the model from .env (onyx.model.from_env) and kb_main retrieval, and stops before any call when the key has no
value; a scripted run uses onyx/scripted.py and goes under runs/scripted/, labelled scripted in its run_start event.
A committed run is never overwritten.

`replay` re-runs a recorded log offline: RecordedModel returns each logged model response, RecordedRetriever returns
each step's logged retrieval, and the gate decides again. The verdicts must equal the recorded ones.
"""

from __future__ import annotations

import json
import tempfile
from pathlib import Path
from typing import Any

from collections.abc import Callable

from onyx import audit, cost, data, kb
from onyx import model as model_mod

SCENARIOS = ("S1", "S2", "S3", "S4", "S5")  # the demo set; the unseen bank is never recorded or scored
LANGS = ("en", "ar")
MODES = ("governed", "ungoverned")
RUNS = 3
DECISIONS = {"gate", "abstain", "override_refused", "override_release"}


def run_path(root: str | Path, sid: str, n: int, lang: str = "en", governed: bool = True) -> Path:
    base = Path(root) if governed else Path(root) / "ungoverned"
    base = base / sid if lang == "en" else base / sid / lang
    return base / f"run{n}.jsonl"


def _events(path: str | Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines()]


def decisions(path: str | Path) -> list[tuple[Any, ...]]:
    """What a replay must reproduce: every gate verdict, abstention and override, with its clause ids."""
    return [(e["entity_id"], e["action"], e["verdict"], tuple(e["clause_ids"])) for e in _events(path)
            if e["action"] in DECISIONS]


def record(source: str, root: str | Path, scenarios: tuple[str, ...] = SCENARIOS, runs: int = RUNS,
           langs: tuple[str, ...] = LANGS, env: str | Path = ".env", modes: tuple[str, ...] = MODES,
           retriever: Any = None, max_usd: float = cost.DEFAULT_MAX_USD, spend_root: str | Path = cost.RUNS_DIR,
           out: Callable[[str], Any] = print, skip_existing: bool = False) -> list[Path]:
    """A live run stops before any call when the key has no value (MissingModelKey) or when the spend guard
    refuses (cost.SpendRefused). `retriever` replaces kb_main in tests only. skip_existing keeps a recorded run and
    records only the missing ones (after a run died; move its partial log out first); without it an existing run
    raises."""
    from onyx import coordinator, scripted

    if source == "live":
        live = model_mod.from_env(env)  # raises MissingModelKey before anything is written
        retriever = retriever or coordinator._kb_retriever()
        cost.guard(live.model, cost.plan(scenarios, langs, modes, runs, retriever), max_usd, spend_root, out)
    elif source != "scripted":
        raise ValueError(f"source {source!r}: live or scripted")
    written = []
    for sid in scenarios:
        scenario = data.load_scenario(sid)
        for governed in (mode == "governed" for mode in modes):
            for lang in langs:
                for n in range(1, runs + 1):
                    path = run_path(root, sid, n, lang, governed)
                    if path.exists() and skip_existing:
                        continue
                    if path.exists():
                        raise FileExistsError(f"{path}: a recorded run is never overwritten")
                    if source == "live":
                        model, retrieve, model_id = live, retriever, live.model
                    else:
                        model, retrieve, model_id = scripted.model(sid, lang), scripted.retriever(sid), "scripted-mock"
                    run = coordinator.Coordinator(scenario, model, retrieve, log_path=path,
                                                  gaps_dir=Path(root) / "gaps", lang=lang, governed=governed)
                    run.start(source=source, model=model_id, run=n,
                              retrieval="kb_main" if source == "live" else "scripted")
                    run.run()
                    written.append(path)
    return written


class RecordedRetriever:
    """Returns, for a step's text, the chunks the recorded run retrieved for it (the propose event's sources_used)."""

    def __init__(self, events: list[dict[str, Any]]) -> None:
        texts = {e["entity_id"] + "-" + e["new_value"]["to"]: e["new_value"]["text"] for e in events
                 if e["action"] == "release_event"}
        self.by_text = {texts[e["entity_id"]]: e["new_value"]["sources_used"] for e in events
                        if e["action"] == "propose" and e["entity_id"] in texts}

    def __call__(self, query: str, documents: list[str], k: int) -> list[dict[str, Any]]:
        return [kb.get_chunk(*chunk.split(":", 1)) for chunk in self.by_text.get(query, [])]


def replay(path: str | Path) -> tuple[list[tuple[Any, ...]], list[tuple[Any, ...]]]:
    """(recorded, replayed) decisions of a run log. A broken chain is never replayed."""
    from onyx import coordinator

    if not audit.verify(path):
        raise ValueError(f"{path}: chain broken; not replayed")
    events = _events(path)
    config = events[0]["new_value"]
    scenario = data.load_scenario(events[0]["entity_id"])
    # a log recorded before prompt v2 gave no mandate clauses; its replay gives none either
    mandate = any(e["new_value"].get("sources_mandate") for e in events if e["action"] == "propose")
    # a log recorded before prompt v3 took no gap from notes; its abstentions carry no gaps_source
    notes_gaps = any("gaps_source" in e["new_value"] for e in events if e["action"] == "abstain")
    with tempfile.TemporaryDirectory() as tmp:
        run = coordinator.Coordinator(scenario, model_mod.RecordedModel(path), RecordedRetriever(events),
                                      log_path=Path(tmp) / "replay.jsonl", gaps_dir=Path(tmp) / "gaps",
                                      lang=config.get("lang", "en"), governed=config.get("mode") != "ungoverned",
                                      mandate_clauses=mandate, notes_gaps=notes_gaps)
        run.start(**{k: v for k, v in config.items() if k not in {"answer_keys", "lang", "mode"}})
        run.run()
        for e in events:
            if e["action"] == "release_event" and e["new_value"]["kind"] == "inject":
                run.inject(e["new_value"]["text"], e["new_value"]["to"])
        return decisions(path), decisions(run.log.path)


# --- command line -----------------------------------------------------------------------------------------------

def _record_cli(args) -> int:
    root = Path(args.root or ("runs" if args.source == "live" else "runs/scripted"))
    try:
        written = record(args.source, root, tuple(args.scenarios or SCENARIOS), args.runs,
                         modes=tuple(args.modes or MODES), max_usd=args.max_usd, skip_existing=args.skip_existing)
    except (model_mod.MissingModelKey, cost.SpendRefused) as e:
        print(f"stopped: {e}")
        return 2
    print(f"{len(written)} runs written under {root} ({args.source}).")
    return 0


def _replay_cli(args) -> int:
    recorded, replayed = replay(args.log)
    for entity, action, verdict, clauses in replayed:
        print(f"  {entity:<18} {action:<16} {verdict or '':<22} {', '.join(clauses[:4])}{', ...' if len(clauses) > 4 else ''}")
    same = recorded == replayed
    print(f"{args.log}: chain ok; replay {'matches' if same else 'DIFFERS FROM'} the recorded verdicts "
          f"({len(recorded)} decisions)")
    return 0 if same else 1


def register(subparsers) -> None:
    parser = subparsers.add_parser("record", help="record three runs per scenario, mode and language (Task 8)")
    parser.add_argument("--source", choices=("scripted", "live"), required=True,
                        help="live: the model in .env (a real call costs money); scripted: no model call")
    parser.add_argument("--root", help="default runs/ (live) or runs/scripted/ (scripted)")
    parser.add_argument("--scenarios", nargs="*", choices=SCENARIOS)
    parser.add_argument("--runs", type=int, default=RUNS)
    parser.add_argument("--modes", nargs="*", choices=MODES, help="default both; the bake-off runs governed only")
    parser.add_argument("--max-usd", type=float, default=cost.DEFAULT_MAX_USD,
                        help=f"refuse a live run whose estimate is over this (default USD {cost.DEFAULT_MAX_USD})")
    parser.add_argument("--skip-existing", action="store_true",
                        help="keep runs already recorded and record only the missing ones (never overwrites)")
    parser.set_defaults(func=_record_cli)
    parser = subparsers.add_parser("replay", help="re-run a recorded log offline and compare the verdicts")
    parser.add_argument("log")
    parser.set_defaults(func=_replay_cli)
