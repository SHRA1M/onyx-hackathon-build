"""Agent base (order Task 5): mandate-scoped retrieval, one model call, typed JSON out, verbs outside the mandate
rejected before the gate.

Output schema (reference code, kept): agent_name, proposals[{verb, target, args, clause_ids[], quote, rationale}],
sources_used[], reasoning_chain[]. Agents exchange these objects, never free text (IMDA 2.3.1). A clause id is the
chunk id `document_id:clause`, the id the agent saw when it retrieved the clause.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from typing import Any, Protocol

from onyx import audit, data, kb
from onyx.model import Model

INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"


@dataclass
class Proposal:
    verb: str
    target: str = ""
    args: dict[str, Any] = field(default_factory=dict)
    clause_ids: list[str] = field(default_factory=list)
    quote: str = ""
    rationale: str = ""


@dataclass
class AgentOutput:
    agent_name: str
    proposals: list[Proposal] = field(default_factory=list)
    sources_used: list[str] = field(default_factory=list)
    reasoning_chain: list[str] = field(default_factory=list)
    rejected: list[Proposal] = field(default_factory=list)  # verbs outside the mandate, never shown to the gate

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def chunk_id(chunk: dict[str, Any]) -> str:
    return f"{chunk['document_id']}:{chunk['clause']}"


def _strip_fence(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[-1].rsplit("```", 1)[0]
    return text


def parse_output(agent_name: str, text: str) -> AgentOutput:
    """The model's reply as an AgentOutput. Anything not in the schema proposes nothing (deny by default)."""
    try:
        reply = json.loads(_strip_fence(text))
        proposals = [Proposal(verb=str(p["verb"]), target=str(p.get("target", "")), args=dict(p.get("args") or {}),
                              clause_ids=[str(c) for c in p.get("clause_ids") or []], quote=str(p.get("quote", "")),
                              rationale=str(p.get("rationale", ""))) for p in reply.get("proposals") or []]
        reasoning = [str(r) for r in reply.get("reasoning_chain") or []]
    except (ValueError, TypeError, KeyError, AttributeError):
        return AgentOutput(agent_name, reasoning_chain=["unparseable model response: no JSON in the agreed schema"])
    return AgentOutput(agent_name, proposals, reasoning_chain=reasoning)


class Retriever(Protocol):
    def __call__(self, query: str, documents: list[str], k: int) -> list[dict[str, Any]]: ...


class ChromaRetriever:
    """kb_main search filtered to the agent's documents; returns the committed chunks, so a hit is a citation."""

    def __init__(self, collection: Any) -> None:
        self.collection = collection

    def __call__(self, query: str, documents: list[str], k: int) -> list[dict[str, Any]]:
        if not documents:
            return []
        where = {"document_id": {"$in": documents}} if len(documents) > 1 else {"document_id": documents[0]}
        result = self.collection.query(query_texts=[query], n_results=k, where=where)
        return [kb.get_chunk(*hit.split(":", 1)) for hit in result["ids"][0]]


class Agent:
    name = ""
    role = ""  # hq hackathon-plan-2026-10-15.docx, Agents table

    def __init__(self, model: Model, retriever: Retriever, log: audit.AuditLog | None = None) -> None:
        self.model, self.retriever, self.log = model, retriever, log

    @classmethod
    def mandate(cls) -> list[dict[str, Any]]:
        return data.load_mandates()[cls.name]["verbs"]

    @classmethod
    def documents_of(cls) -> list[str]:
        """The agent's document set, by role (hq addendum 27): the `documents` list in mandates.json. Every id must
        be a manifest row; an unknown id raises rather than silently narrowing retrieval."""
        documents = data.load_mandates()[cls.name]["documents"]
        unknown = [d for d in documents if d not in kb.manifest_by_id()]
        if unknown:
            raise ValueError(f"{cls.name}: documents not in kb/manifest.csv: {', '.join(unknown)}")
        return list(documents)

    @property
    def verbs(self) -> set[str]:
        return {verb["verb"] for verb in self.mandate()}

    @property
    def documents(self) -> list[str]:
        return self.documents_of()

    def retrieve(self, query: str, k: int = 8) -> list[dict[str, Any]]:
        return self.retriever(query, self.documents, k)

    def messages(self, step: dict[str, Any], text: str, hits: list[dict[str, Any]], lang: str) -> list[dict[str, str]]:
        schema = ('{"proposals": [{"verb": "", "target": "", "args": {}, "clause_ids": [], "quote": "", '
                  '"rationale": ""}], "reasoning_chain": []}')
        system = (
            f"You are the {self.name} agent of Sahab Telecom, a SYNTHETIC UAE operator. Role: {self.role}\n"
            f"You may propose only these verbs: {', '.join(sorted(self.verbs))}.\n"
            f"Reply with one JSON object and nothing else: {schema}\n"
            "Cite only the clauses given below, by their id in square brackets. 'quote' is 20 or more characters "
            "copied exactly from a cited clause. You propose and explain; plain-code gates decide.\n"
            f"If no clause below answers the step, propose nothing and make '{INSUFFICIENT_EVIDENCE}' the first "
            "entry of reasoning_chain."
        )
        clauses = []
        for hit in hits:
            clause = f"[{chunk_id(hit)}] {hit['text_en']}"
            if lang == "ar" and hit["text_ar"]:
                clause += f"\n(Arabic) {hit['text_ar']}"
            clauses.append(clause)
        user = (f"Clauses:\n" + "\n\n".join(clauses) +
                f"\n\nStep {step.get('n')} ({step.get('kind')}), facts: {json.dumps(step.get('facts', {}), ensure_ascii=False)}\n"
                f"Message:\n{text}")
        return [{"role": "system", "content": system}, {"role": "user", "content": user}]

    def run(self, request_id: str, step: dict[str, Any], lang: str = "en") -> AgentOutput:
        text = step[f"text_{lang}"]
        hits = self.retrieve(text)
        response = self.model.complete(request_id, self.messages(step, text, hits, lang))
        out = parse_output(self.name, response.text)
        out.sources_used = [chunk_id(hit) for hit in hits]  # what was retrieved, never what the model claims
        out.rejected = [p for p in out.proposals if p.verb not in self.verbs]
        out.proposals = [p for p in out.proposals if p.verb in self.verbs]
        self._append({"action": "propose", "entity_type": "step", "entity_id": request_id, "new_value": out.to_dict(),
                      "source": response.model, "clause_ids": sorted({c for p in out.proposals for c in p.clause_ids}),
                      "model_request_id": request_id, "model_response": response.raw})
        for p in out.rejected:
            self._append({"action": "reject_proposal", "entity_type": "proposal", "entity_id": request_id,
                          "old_value": asdict(p), "source": "onyx/data/mandates.json",
                          "reason": f"verb {p.verb} is outside the {self.name} mandate; rejected before the gate"})
        return out

    def _append(self, event: dict[str, Any]) -> None:
        if self.log is not None:
            self.log.append({"actor": self.name, **event})
