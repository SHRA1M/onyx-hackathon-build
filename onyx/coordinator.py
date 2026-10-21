"""The coordinator (order Task 7; Y.3172 D node): releases a scenario's steps in stages, one agent per step, runs
the agent, passes every proposal to the gate, and appends each act to the run's hash-chained log.

Staged release: each agent has an inbox and sees only the steps released to it, in the run's language. The
subscriber's record (subscriber, account, catalogue) goes only to the agents that serve the subscriber (care, and
the data office, which receives the subscriber's objections and review requests); the adviser and the TDRA get the
step alone. The gate, the P node, reads the whole case: State.facts is the record plus every step's facts so far.

Abstention: when the adviser's model puts INSUFFICIENT_EVIDENCE first, proposes nothing, or every proposal fails
the gate on evidence, the adviser answers INSUFFICIENT_EVIDENCE and lists the clauses searched, each with what it
says (its rules.json quote): the clauses it retrieved for the question and every clause the gate has cited in
this case so far. A live inject (`run S2 --inject "<text>"`) that ends in abstention writes a row to
gaps/candidates.jsonl (order review focus 4).
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from onyx import audit, data, gate
from onyx.agents import AGENTS, Adviser
from onyx.agents.base import INSUFFICIENT_EVIDENCE, AgentOutput, Proposal, Retriever
from onyx.model import Model

RECORD_FIELDS = ("subscriber", "account", "catalogue")
SERVES_SUBSCRIBER = {"care", "data_office"}
QUESTION_KINDS = {"question", "inject"}
GAPS_DIR = Path("gaps")
DEFAULT_CHANNEL = "app_chat"


@dataclass
class Release:
    """One entry in an agent's inbox: what the coordinator released to it for one step."""
    inject: str
    n: int
    to: str
    kind: str
    text: str
    facts: dict[str, Any] = field(default_factory=dict)
    record: dict[str, Any] = field(default_factory=dict)  # only for agents that serve the subscriber

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class StepResult:
    inject: str
    agent: str
    output: AgentOutput | None
    verdicts: list[tuple[Proposal, gate.Verdict]] = field(default_factory=list)
    answer: str = ""  # INSUFFICIENT_EVIDENCE on an abstention
    searched: list[dict[str, str]] = field(default_factory=list)
    gaps: list[str] = field(default_factory=list)

    @property
    def searched_ids(self) -> list[str]:
        return [row["rule"] for row in self.searched]


def _rules_by_chunk() -> dict[str, list[str]]:
    index: dict[str, list[str]] = {}
    for rule in data.load_rules():
        index.setdefault(f"{rule['document_id']}:{rule['chunk']}", []).append(rule["id"])
    return index


class Coordinator:
    def __init__(self, scenario: dict[str, Any], model: Model, retriever: Retriever, log_path: str | Path,
                 gaps_dir: str | Path = GAPS_DIR, lang: str = "en", governed: bool = True,
                 knowledge: gate.Knowledge | None = None) -> None:
        if lang not in {"en", "ar"}:
            raise ValueError(f"language {lang!r}: en or ar")
        self.scenario, self.lang, self.governed = scenario, lang, governed
        self.sid = scenario["id"]
        self.log = audit.AuditLog(log_path)
        self.gaps_dir = Path(gaps_dir)
        self.kb = knowledge or gate.Knowledge.load()
        self.decide = gate.decide if governed else gate.allow_all
        self.agents = {name: cls(model, retriever, self.log) for name, cls in AGENTS.items()}
        self.inboxes: dict[str, list[Release]] = {name: [] for name in AGENTS}
        self.record = {name: scenario[name] for name in RECORD_FIELDS if name in scenario}
        self.facts: dict[str, Any] = {**scenario.get("subscriber", {}), **scenario.get("account", {}),
                                      "catalogue": scenario.get("catalogue", {}).get("items", [])}
        self.channel = scenario.get("channel", "")
        self.cited: list[str] = []  # rules.json ids the gate has cited in this case, in order
        self.steps_run = 0
        self.rules = {r["id"]: r for r in data.load_rules()}
        self.by_chunk = _rules_by_chunk()

    # --- the run --------------------------------------------------------------------------------------------

    def start(self) -> str:
        return self.log.start(self.sid)

    def run(self, until: int | None = None) -> list[StepResult]:
        steps = [s for s in self.scenario["steps"] if until is None or s["n"] <= until]
        return [self.step(s) for s in steps]

    def inject(self, text: str, to: str = "adviser") -> StepResult:
        """A step added at run time (order Task 7, live step). It goes to the adviser as a question."""
        n = len(self.scenario["steps"]) + 1 + sum(1 for r in self._all_releases() if r.kind == "inject")
        return self.step({"n": n, "from": "judge", "to": to, "kind": "inject", f"text_{self.lang}": text, "facts": {}})

    def step(self, step: dict[str, Any]) -> StepResult:
        self.steps_run += 1
        self.facts.update(step.get("facts", {}))
        if step.get("facts", {}).get("channel"):
            self.channel = step["facts"]["channel"]
        release = self._release(step)
        agent = self.agents[release.to]
        request_id = f"{self.sid}-{step['n']}-{release.to}"
        if release.kind == "classification":
            return self._classify(release, request_id)
        output = agent.run(request_id, {"n": release.n, "kind": release.kind, f"text_{self.lang}": release.text,
                                        "facts": {**release.record, **release.facts}}, self.lang)
        result = StepResult(release.inject, release.to, output)
        for proposal in output.proposals:
            result.verdicts.append((proposal, self._gate(proposal, release, request_id, output.sources_used)))
        if release.to == "adviser" and release.kind in QUESTION_KINDS and self._abstains(result):
            self._abstain(result, release)
        return result

    # --- staged release ---------------------------------------------------------------------------------------

    def _release(self, step: dict[str, Any]) -> Release:
        to = step["to"]
        first = not self.inboxes[to]
        release = Release(inject=f"{self.sid}-{step['n']}", n=step["n"], to=to, kind=step["kind"],
                          text=step.get(f"text_{self.lang}", ""), facts=dict(step.get("facts", {})),
                          record=self.record if to in SERVES_SUBSCRIBER and first else {})
        self.inboxes[to].append(release)
        self.log.append({"actor": "coordinator", "action": "release_event", "entity_type": "step",
                         "entity_id": release.inject, "new_value": release.to_dict(),
                         "source": f"onyx/data/scenarios/{self.sid}.json",
                         "reason": f"released to {to} only (staged release)"})
        return release

    def _all_releases(self) -> list[Release]:
        return [r for inbox in self.inboxes.values() for r in inbox]

    # --- the gate ---------------------------------------------------------------------------------------------

    def _state(self, agent: str, inject: str, retrieved: list[str]) -> gate.State:
        humans = tuple(self.facts.get("human_agents_on_shift", [])) + tuple(
            self.facts[k] for k in ("human_actor", "verified_by") if self.facts.get(k))
        return gate.State(agent=agent, inject=inject, released={r.inject for r in self.inboxes[agent]},
                          retrieved=set(retrieved), channel=self.channel or DEFAULT_CHANNEL, facts=dict(self.facts),
                          humans=humans)

    def _gate(self, proposal: Proposal, release: Release, request_id: str, retrieved: list[str]) -> gate.Verdict:
        verdict = self.decide(proposal, self._state(release.to, release.inject, retrieved), self.kb)
        self.cited += [c for c in verdict.clause_ids if c not in self.cited]
        if verdict.verdict == gate.ALLOW and proposal.verb == "request_human_review":
            self.facts["human_review_open"] = True  # every further automated step waits for it (PDPL 18(4))
        self.log.append({"actor": "gate", "action": "gate", "entity_type": "proposal", "entity_id": request_id,
                         "old_value": asdict(proposal), "new_value": {"reasons": verdict.reasons},
                         "verdict": verdict.verdict, "clause_ids": verdict.clause_ids, "quote": proposal.quote,
                         "source": "onyx/gate.py decide" if self.governed else "onyx/gate.py allow_all (ungoverned)"})
        return verdict

    def _classify(self, release: Release, request_id: str) -> StepResult:
        adviser: Adviser = self.agents["adviser"]  # type: ignore[assignment]
        channel = release.facts.get("channel") or self.channel
        output = adviser.classify_channel(request_id, channel)
        self.channel = channel
        result = StepResult(release.inject, release.to, output)
        for proposal in output.proposals:
            result.verdicts.append((proposal, self._gate(proposal, release, request_id, proposal.clause_ids)))
        return result

    # --- abstention -------------------------------------------------------------------------------------------

    @staticmethod
    def _abstains(result: StepResult) -> bool:
        out = result.output
        if out is None or not out.proposals or (out.reasoning_chain[:1] == [INSUFFICIENT_EVIDENCE]):
            return True
        return all(v.verdict == gate.INSUFFICIENT for _, v in result.verdicts)

    def _searched(self, retrieved: list[str]) -> list[dict[str, str]]:
        ids: list[str] = []
        for chunk in retrieved:
            ids += [r for r in self.by_chunk.get(chunk, []) if r not in ids]
        ids += [r for r in self.cited if r not in ids]
        return [{"rule": r, "label": self.rules[r]["label"], "says": self.rules[r]["quote"]} for r in ids]

    def _abstain(self, result: StepResult, release: Release) -> None:
        out = result.output
        result.answer = INSUFFICIENT_EVIDENCE
        result.searched = self._searched(out.sources_used if out else [])
        result.gaps = [str(p.args.get("gap") or p.target) for p in (out.proposals if out else [])
                       if p.verb == "flag_gap"]
        event_hash = self.log.append({
            "actor": "adviser", "action": "abstain", "entity_type": "step", "entity_id": release.inject,
            "new_value": {"answer": INSUFFICIENT_EVIDENCE, "searched": result.searched, "gaps": result.gaps},
            "verdict": gate.INSUFFICIENT, "clause_ids": result.searched_ids, "source": "onyx/coordinator.py",
            "reason": "no VERIFIED clause retrieved answers the step; clauses searched listed with what each says"})
        if release.kind == "inject" or not result.gaps:
            self._candidate(release, result, event_hash)

    def _candidate(self, release: Release, result: StepResult, event_hash: str) -> None:
        self.gaps_dir.mkdir(parents=True, exist_ok=True)
        row = {"id": f"candidate-{release.inject}", "scenario": self.sid, "inject": release.inject,
               "lang": self.lang, "text": release.text, "status": "candidate",
               "clauses_searched": result.searched, "gaps_named": result.gaps, "log": str(self.log.path),
               "log_hash": event_hash}
        with (self.gaps_dir / "candidates.jsonl").open("a", encoding="utf-8", newline="\n") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


# --- command line -----------------------------------------------------------------------------------------------

def _kb_retriever() -> Retriever:
    import chromadb

    from onyx import kb
    from onyx.agents.base import ChromaRetriever
    return ChromaRetriever(chromadb.PersistentClient(path=str(kb.CHROMA_DIR)).get_collection("kb_main"))


def _cli(args) -> int:
    from onyx import scripted

    scenario = data.load_scenario(args.scenario)
    mode = "governed" if not args.ungoverned else "ungoverned"
    out = Path(args.out or f"runs/local/{args.scenario}-{args.lang}-{mode}.jsonl")
    if out.exists():
        out.unlink()
    fallback = _kb_retriever() if args.search_kb else None
    run = Coordinator(scenario, scripted.model(args.scenario, args.lang), scripted.retriever(args.scenario, fallback),
                      log_path=out, gaps_dir=args.gaps, lang=args.lang, governed=not args.ungoverned)
    print(f"{scenario['id']} {scenario['title_' + args.lang]} ({args.lang}, {mode}). SYNTHETIC operator and subscriber.")
    print("Model: scripted-mock (no model call). Retrieval: scripted" + (", kb_main for injects." if fallback else "."))
    run.start()
    results = run.run()
    for text in args.inject or []:
        results.append(run.inject(text))
    for r in results:
        verdicts = ", ".join(f"{p.verb}: {v.verdict} [{', '.join(v.clause_ids[:4])}"
                             f"{', ...' if len(v.clause_ids) > 4 else ''}]" for p, v in r.verdicts) or "no proposal"
        print(f"  {r.inject:<6} {r.agent:<12} {verdicts}")
        if r.answer:
            print(f"         {r.answer}; searched {len(r.searched)} clauses; gaps {', '.join(r.gaps) or 'none named'}")
    print(f"log: {out} ({'chain ok' if audit.verify(out) else 'chain broken'})")
    return 0


def register(subparsers) -> None:
    parser = subparsers.add_parser("run", help="run a scenario through the agents and the gate (offline, scripted)")
    parser.add_argument("scenario", help="S1 to S5")
    parser.add_argument("--lang", choices=("en", "ar"), default="en")
    parser.add_argument("--ungoverned", action="store_true", help="replace the gate with allow_all")
    parser.add_argument("--inject", action="append", metavar="TEXT", help="append a step at run time (to the adviser)")
    parser.add_argument("--out", help="run log path (default runs/local/<scenario>-<lang>-<mode>.jsonl)")
    parser.add_argument("--gaps", default=str(GAPS_DIR), help="where candidates.jsonl is written")
    parser.add_argument("--search-kb", action="store_true",
                        help="search kb_main (data/chromadb, from `kb ingest`) for an injected step")
    parser.set_defaults(func=_cli)
