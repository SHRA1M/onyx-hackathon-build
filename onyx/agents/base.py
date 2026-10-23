"""Agent base (order Task 5): mandate-scoped retrieval, one model call, typed JSON out, verbs outside the mandate
rejected before the gate.

Output schema (reference code, kept): agent_name, proposals[{verb, target, args, clause_ids[], quote, rationale}],
sources_used[], reasoning_chain[]. Agents exchange these objects, never free text (IMDA 2.3.1). A clause id is the
chunk id `document_id:clause`, the id the agent saw when it was given the clause.

Prompt v2 (order 2026-10-21-task-8-part-c, items 5 and 6): the model proposes what the step calls for and the gates
decide; it abstains only when the step asks for a rule, figure or deadline no clause states. It is given the
mandate clauses of its verbs (mandates.json) first, then the retrieved chunks, deduplicated; both sets are logged
apart (sources_mandate, sources_used) and both are what the gate counts as given. On the wire reasoning_chain is
named `notes` (parse_output accepts both); the internal and logged name stays reasoning_chain.

Prompt v3 (order 2026-10-21-task-8-part-c2b): when a reply abstains, parse_output also collects the gap register
ids (onyx/data/gaps.json) its notes name, exact id strings only, in gaps_in_notes. The coordinator records them on
the abstention when no flag_gap proposal names a gap.

Prompt v4 (order 2026-10-21-task-8-part-c4): three care lines (Care.extra_lines) and care's mandate widened to the
clauses its gates test. A replay gives each agent the mandate clauses its log recorded (recorded_mandate), so a log
recorded on a narrower mandate is decided again on what its run was given.

v4.1 (Task 9, unscored): the adviser's register lists gap-8 and the candidate at line 9; kb_main grew from 106 chunks with the Task 9 searched clauses (and again with item 1 above). Recorded runs are v4 and replay as recorded.

v5 (order 2026-10-22): line 1 carves the de-identified model-provider payload out of disclose_account; line 3 addresses the sender of the step and names the human from the facts. Scored as C5. Recorded C3 and C4 runs replay as recorded.

v5, register grown (Task 15, unscored): the adviser's register adds gap-9 and candidate-79bis-2-fine-schedule at lines 9 and 11; label stays v5; recorded runs replay as recorded.

v5, register grown again (Task 20, unscored): the adviser's register adds gap-10 at line 10, so the candidates move to lines 11 and 12; label stays v5; recorded runs replay as recorded.
"""

from __future__ import annotations

import json
import re
import time
from dataclasses import asdict, dataclass, field
from typing import Any, Protocol

from onyx import audit, data, kb
from onyx.model import Model

INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"
PROMPT_VERSION = "v5"  # logged on run_start
LANGUAGE = {"en": "English", "ar": "Arabic"}


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
    sources_used: list[str] = field(default_factory=list)  # retrieved for this step
    sources_mandate: list[str] = field(default_factory=list)  # the mandate clauses of the agent's verbs
    reasoning_chain: list[str] = field(default_factory=list)
    gaps_in_notes: list[str] = field(default_factory=list)  # register ids named in an abstaining reply's notes
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


def _gaps_in(notes: list[str]) -> list[str]:
    """Register ids named in the notes, in register order: the exact id, not inside a longer word or id."""
    text = "\n".join(notes)
    return [g["id"] for g in data.load_gaps()["gaps"]
            if re.search(rf"(?<![\w-]){re.escape(g['id'])}(?![\w-])", text)]


def parse_output(agent_name: str, text: str) -> AgentOutput:
    """The model's reply as an AgentOutput. Anything not in the schema proposes nothing (deny by default)."""
    try:
        reply = json.loads(_strip_fence(text))
        proposals = [Proposal(verb=str(p["verb"]), target=str(p.get("target", "")), args=dict(p.get("args") or {}),
                              clause_ids=[str(c) for c in p.get("clause_ids") or []], quote=str(p.get("quote", "")),
                              rationale=str(p.get("rationale", ""))) for p in reply.get("proposals") or []]
        reasoning = [str(r) for r in reply.get("notes", reply.get("reasoning_chain")) or []]
        if reasoning and reasoning[0] == f"<{INSUFFICIENT_EVIDENCE}>":
            reasoning[0] = INSUFFICIENT_EVIDENCE
    except (ValueError, TypeError, KeyError, AttributeError):
        return AgentOutput(agent_name, reasoning_chain=["unparseable model response: no JSON in the agreed schema"])
    abstains = not proposals or reasoning[:1] == [INSUFFICIENT_EVIDENCE]
    return AgentOutput(agent_name, proposals, reasoning_chain=reasoning,
                       gaps_in_notes=_gaps_in(reasoning) if abstains else [])


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

    def __init__(self, model: Model, retriever: Retriever, log: audit.AuditLog | None = None,
                 mandate_clauses: bool = True, recorded_mandate: list[str] | None = None) -> None:
        self.model, self.retriever, self.log = model, retriever, log
        self.mandate_clauses = mandate_clauses  # False only to replay a log recorded before prompt v2
        self.recorded_mandate = recorded_mandate  # replay only: the sources_mandate its log recorded

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

    def mandate_chunks(self) -> list[dict[str, Any]]:
        """The clauses mandates.json maps the agent's verbs to, in order, once each."""
        if not self.mandate_clauses:
            return []
        if self.recorded_mandate is not None:
            return [kb.get_chunk(*c.split(":", 1)) for c in self.recorded_mandate]
        seen, chunks = set(), []
        for verb in self.mandate():
            for c in verb["clause_ids"]:
                if (c["document_id"], c["chunk"]) not in seen:
                    seen.add((c["document_id"], c["chunk"]))
                    chunks.append(kb.get_chunk(c["document_id"], c["chunk"]))
        return chunks

    def extra_lines(self) -> list[str]:
        return []

    def messages(self, step: dict[str, Any], text: str, hits: list[dict[str, Any]], lang: str) -> list[dict[str, str]]:
        """`hits` are the clauses given, mandate clauses first (see run)."""
        schema = ('{"proposals": [{"verb": "", "target": "", "args": {}, "clause_ids": [], "quote": "", '
                  '"rationale": ""}], "notes": []}')
        system = "\n".join([
            f"You are the {self.name} agent of Sahab Telecom, a SYNTHETIC UAE operator. Role: {self.role}",
            f"You may propose only these verbs: {', '.join(sorted(self.verbs))}.",
            f"Reply with one JSON object and nothing else: {schema}",
            "Cite only the clauses given below, by their id in square brackets. 'quote' is 20 or more characters "
            "copied exactly from a cited clause. You propose and explain; plain-code gates decide.",
            "Propose the action this step calls for, citing the clauses that govern it; the gates decide whether it "
            f"is allowed. Propose nothing, and make '<{INSUFFICIENT_EVIDENCE}>' the first entry of the last field, "
            "only when the step asks for a rule, figure or deadline that no clause below states.",
            "Facts are Sahab's own records (account, catalogue, consent log). Use them as true. Clauses are for "
            "citations only.",
            f"Reply in the language of this run: {LANGUAGE[lang]}.",
            *self.extra_lines(),
        ])
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
        hits, mandate = self.retrieve(text), self.mandate_chunks()
        given = mandate + [hit for hit in hits if chunk_id(hit) not in {chunk_id(m) for m in mandate}]
        started = time.perf_counter()
        response = self.model.complete(request_id, self.messages(step, text, given, lang))
        model_ms = round((time.perf_counter() - started) * 1000, 3)
        out = parse_output(self.name, response.text)
        out.sources_used = [chunk_id(hit) for hit in hits]  # what was retrieved, never what the model claims
        out.sources_mandate = [chunk_id(m) for m in mandate]
        out.rejected = [p for p in out.proposals if p.verb not in self.verbs]
        out.proposals = [p for p in out.proposals if p.verb in self.verbs]
        self._append({"action": "propose", "entity_type": "step", "entity_id": request_id, "new_value": out.to_dict(),
                      "source": response.model, "clause_ids": sorted({c for p in out.proposals for c in p.clause_ids}),
                      "model_request_id": request_id, "model_response": response.raw, "model_ms": model_ms})
        for p in out.rejected:
            self._append({"action": "reject_proposal", "entity_type": "proposal", "entity_id": request_id,
                          "old_value": asdict(p), "source": "onyx/data/mandates.json",
                          "reason": f"verb {p.verb} is outside the {self.name} mandate; rejected before the gate"})
        return out

    def _append(self, event: dict[str, Any]) -> None:
        if self.log is not None:
            self.log.append({"actor": self.name, **event})
