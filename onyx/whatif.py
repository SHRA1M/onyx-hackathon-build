"""What-if replay (order 2026-10-23 Task 19; hq ruling 2026-10-23, clock on block verdicts only).

`replay_under(path, rule_id)` re-decides a recorded run exactly as `runs.replay` does (same RecordedModel and
RecordedRetriever, a broken chain is never replayed), with two wrappers around the frozen gate. The proposed rule is
data in onyx/data/proposed/, never loaded by the gate: its id appears in reasons only, marked `proposed: true`, and
never in clause_ids.

- `decide_under`: on a `block` whose reasons hold an obligation on the rule's clause while the trigger fact is yes, one
  obligation reason is added with the rule's deadline. The verdict and clause_ids are unchanged.
- `decide_pending_under`: a deny-by-default hold on the question the rule answers is released to allow, with a check
  reason and, when the log records no time at the hand-over step, a second-order finding. Any other hold, and every
  block, is returned as the gate gave it.

`python -m onyx whatif <log> [--rule gap-1]` prints the changes and writes docs/replay/whatif-<sid>-<rule>.md,
byte-identical on every run."""

from __future__ import annotations

import dataclasses
import json
import tempfile
from collections.abc import Callable
from pathlib import Path
from typing import Any

from onyx import audit, data, gate, kb, runs
from onyx import model as model_mod

PROPOSED_DIR = data.DATA_DIR / "proposed"
OUT = kb.REPO / "docs" / "replay"
VOLATILE = {"ts", "prev_hash", "hash", "gate_ms", "model_ms"}  # differ on every replay; the decision does not
Decide = Callable[..., gate.Verdict]


def load_rule(rule_id: str) -> dict[str, Any]:
    return json.loads((PROPOSED_DIR / f"{rule_id}.json").read_text(encoding="utf-8"))


def _added(rule: dict[str, Any], kind: str, text: str, **extra: Any) -> dict[str, Any]:
    return {"gate": rule["id"], "kind": kind, "proposed": True, "text": text, **extra}


def decide_under(rule: dict[str, Any]) -> Decide:
    def decide(proposal: Any, state: gate.State, kb_: gate.Knowledge | None = None) -> gate.Verdict:
        verdict = gate.decide(proposal, state, kb_)
        duty = any(r["kind"] == "obligation" and r.get("clause") == rule["adds_deadline_to"] for r in verdict.reasons)
        if verdict.verdict != gate.BLOCK or not duty or not gate._yes(state.facts.get(rule["trigger_fact"])):
            return verdict
        start = state.facts.get("time")
        clock = _added(rule, "obligation", f"hand over within {rule['value']} {rule['unit']} of {start} "
                                           f"({rule['id']}, not law)",
                       deadline={"rule": rule["id"], "value": rule["value"], "unit": rule["unit"], "from": start})
        return dataclasses.replace(verdict, reasons=[*verdict.reasons, clock])
    return decide


def _has_time(events: list[dict[str, Any]], step: str) -> bool:
    return any("time" in e["new_value"].get("facts", {}) for e in events
               if e["action"] == "release_event" and e["entity_id"] == step)


def decide_pending_under(rule: dict[str, Any], events: list[dict[str, Any]]) -> Decide:
    """`events` is the recorded log, read for the time fact at the hand-over step."""
    def decide_pending(proposal: Any, state: gate.State, kb_: gate.Knowledge | None = None) -> gate.Verdict:
        verdict = gate.decide_pending(proposal, state, kb_)
        checks = [r for r in verdict.reasons if r["kind"] == "check"]
        if (verdict.verdict != gate.HOLD or any(r["gate"] != "deny_by_default" for r in checks)
                or proposal.verb != rule["answers"]["verb"] or proposal.args.get("mark") != rule["answers"]["mark"]):
            return verdict
        reasons = [*verdict.reasons, _added(rule, "check", f"the proposed rule answers the step's question: "
                                                           f"{rule['text_en']}")]
        step = f"{state.inject.rsplit('-', 1)[0]}-{int(proposal.args['handover_step']) + 1}"
        if not _has_time(events, step):
            reasons.append(_added(rule, "finding", "second-order: the rule needs the hand-over time recorded; this run "
                                                   f"records the trigger at {state.facts.get('time')} and no hand-over "
                                                   "time, so the two-minute condition cannot be checked"))
        return dataclasses.replace(verdict, verdict=gate.ALLOW, reasons=reasons)
    return decide_pending


def replay_events(path: str | Path, rule: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    """The events of a replay of `path`, set up as runs.replay sets it up; with a rule, under the two wrappers."""
    from onyx import coordinator

    if not audit.verify(path):
        raise ValueError(f"{path}: chain broken; not replayed")
    events = runs._events(path)
    config = events[0]["new_value"]
    scenario = data.load_scenario(events[0]["entity_id"])
    # the same reading of the log as runs.replay (copied, runs.py is not edited)
    mandate = any(e["new_value"].get("sources_mandate") for e in events if e["action"] == "propose")
    recorded_mandates = {e["actor"]: e["new_value"]["sources_mandate"] for e in reversed(events)
                         if e["action"] == "propose" and "sources_mandate" in e["new_value"]}
    notes_gaps = any("gaps_source" in e["new_value"] for e in events if e["action"] == "abstain")
    resolve = bool(config.get("clause_resolution"))
    with tempfile.TemporaryDirectory() as tmp:
        run = coordinator.Coordinator(scenario, model_mod.RecordedModel(path), runs.RecordedRetriever(events),
                                      log_path=Path(tmp) / "replay.jsonl", gaps_dir=Path(tmp) / "gaps",
                                      lang=config.get("lang", "en"), governed=config.get("mode") != "ungoverned",
                                      mandate_clauses=mandate, notes_gaps=notes_gaps,
                                      recorded_mandates=recorded_mandates, resolve_ids=resolve)
        if rule is not None and run.governed:  # an ungoverned run has no gate to wrap
            run.decide, run.decide_pending = decide_under(rule), decide_pending_under(rule, events)
        run.start(**{k: v for k, v in config.items() if k not in {"answer_keys", "lang", "mode", "clause_resolution"}})
        run.run()
        for e in events:
            if e["action"] == "release_event" and e["new_value"]["kind"] == "inject":
                run.inject(e["new_value"]["text"], e["new_value"]["to"])
        return runs._events(run.log.path)


def comparable(event: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in event.items() if k not in VOLATILE}


def _decisions(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [e for e in events if e["action"] in runs.DECISIONS]


def _as_tuple(e: dict[str, Any]) -> tuple[Any, ...]:
    return e["entity_id"], e["action"], e["verdict"], tuple(e["clause_ids"])


def replay_under(path: str | Path, rule_id: str | None = None) -> tuple[list[tuple[Any, ...]], list[tuple[Any, ...]],
                                                                        list[tuple[Any, ...]]]:
    """(recorded, what-if, changes). A change row: (entity_id, verb, recorded verdict, what-if verdict, added
    reasons), one per decision whose verdict or reasons differ from the plain replay. No rule: the plain replay."""
    recorded = _decisions(runs._events(path))
    plain = _decisions(replay_events(path))
    if rule_id is None:
        return [_as_tuple(e) for e in recorded], [_as_tuple(e) for e in plain], []
    under = _decisions(replay_events(path, load_rule(rule_id)))
    changes = []
    for rec, before, after in zip(recorded, plain, under, strict=True):
        if comparable(before) == comparable(after):
            continue
        reasons = (before.get("new_value") or {}).get("reasons", [])
        added = [r for r in (after.get("new_value") or {}).get("reasons", []) if r not in reasons]
        verb = (after.get("old_value") or {}).get("verb") or after["action"]
        changes.append((after["entity_id"], verb, rec["verdict"], after["verdict"], added))
    return [_as_tuple(e) for e in recorded], [_as_tuple(e) for e in under], changes


def _rel(path: str | Path) -> str:
    path = Path(path).resolve()
    return path.relative_to(kb.REPO).as_posix() if path.is_relative_to(kb.REPO) else path.as_posix()


def page_name(path: str | Path, rule_id: str) -> str:
    return f"whatif-{runs._events(path)[0]['entity_id']}-{rule_id}.md"


def render(path: str | Path, rule_id: str) -> str:
    rule = load_rule(rule_id)
    sid = runs._events(path)[0]["entity_id"]
    recorded, under, changes = replay_under(path, rule_id)
    findings = [r["text"] for row in changes for r in row[4] if r["kind"] == "finding"]
    lines = [f"# What-if: {sid} under the rule {rule['gap'].replace('-', ' ')} recommends", "",
             f"Run `{_rel(path)}`; hash chain: {'ok' if audit.verify(path) else 'BROKEN'}. Replayed offline from the "
             "logged model responses; no model call. The operator, subscriber and numbers are synthetic.", "",
             "## Proposed rule, not law", "",
             f"`{rule['id']}`, {rule['status']}, for {rule['addressee']}.", "",
             f"EN: {rule['text_en']}", "",
             f"AR: {rule['text_ar']}", "",
             f"Value: {rule['value']} {rule['unit']}. Basis: {rule['value_basis']}.", "",
             "## What changes", "",
             "| decision | verb | recorded | what-if | added (proposed, not law) |",
             "| --- | --- | --- | --- | --- |"]
    for entity, verb, before, after, added in changes:
        text = "; ".join(f"{r['kind']}: {r['text']}" for r in added).replace("|", "\\|")
        lines.append(f"| {entity} | `{verb}` | {before} | {after} | {text} |")
    lines += ["", "## What stays", "", f"{len(recorded) - len(changes)} of {len(recorded)} decisions identical.", "",
              "## Second-order finding", "", *(findings or ["none"]), "",
              "Generated by `python -m onyx whatif`; the gate, keys and committed runs are unchanged; this page is a "
              "what-if, not a result."]
    return "\n".join(lines) + "\n"


def write(path: str | Path, rule_id: str, out: str | Path = OUT) -> Path:
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    page = out / page_name(path, rule_id)
    page.write_text(render(path, rule_id), encoding="utf-8", newline="\n")
    return page


# --- command line -----------------------------------------------------------------------------------------------

def _cli(args) -> int:
    if not args.rule:
        recorded, replayed, _ = replay_under(args.log)
        same = recorded == replayed
        print(f"no rule: equals replay: {same} ({len(recorded)} decisions)")
        return 0 if same else 1
    recorded, _, changes = replay_under(args.log, args.rule)
    for entity, verb, before, after, added in changes:
        print(f"  {entity:<18} {verb:<12} {before} -> {after}  + {', '.join(r['kind'] for r in added)} (proposed)")
    print(f"{len(recorded) - len(changes)} of {len(recorded)} decisions identical")
    print(_rel(write(args.log, args.rule, args.out)))
    return 0


def register(subparsers) -> None:
    parser = subparsers.add_parser("whatif", help="replay a recorded run under a proposed rule (not law; Task 19)")
    parser.add_argument("log")
    parser.add_argument("--rule", help="a proposed rule in onyx/data/proposed/, e.g. gap-1")
    parser.add_argument("--out", default=str(OUT), help="where the page goes (default docs/replay)")
    parser.set_defaults(func=_cli)
