"""Scripted stand-ins for the model and the retriever, for offline runs (tests, selftest, `run` without a key).

Each scenario step has one canonical proposal, in the gate's args vocabulary (onyx/gate.py; the same proposals
tests/test_gate.py builds), citing one clause; the retriever returns that clause for the step's text in either
language, so the proposal passes the base checks. On a question the adviser cannot answer, the script abstains:
INSUFFICIENT_EVIDENCE first in reasoning_chain, and flag_gap naming the gap. The scripts never read the answer
keys; a scripted run tests the coordinator and the gate, never a model.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from onyx import data, kb
from onyx.agents.base import INSUFFICIENT_EVIDENCE
from onyx.model import MockModel

CPR = "tdra-cpr-v2-en"
PDPL = "pdpl-45-2021-en"
ROAMING = {"sku": "ROAM-UK-7D", "price_aed": 95}
SERVICES = ["mobile line"]
KEPT = ["incoming calls", "emergency numbers", "home broadband"]


def _deadline(rule_id: str) -> dict[str, str]:
    rule = next(r for r in data.load_rules() if r["id"] == rule_id)
    return {"rule": rule_id, "value": rule["value"], "unit": rule["unit"]}


# SCRIPTS[scenario][step n]: the canonical proposal (verb, chunk, target, args) or an abstention (gap, chunk).
# Classification steps have none: the adviser classifies in plain code (onyx/agents/adviser.py).
SCRIPTS: dict[str, dict[int, dict[str, Any]]] = {
    "S1": {
        2: {"verb": "disclose_account", "chunk": f"{CPR}:24.10", "args": {"data": ["roaming_status"]}},
        3: {"verb": "propose_sale", "chunk": f"{CPR}:4.3", "args": ROAMING},
        4: {"verb": "propose_sale", "chunk": f"{CPR}:4.3", "args": ROAMING},
        5: {"verb": "propose_sale", "chunk": f"{CPR}:4.3", "args": ROAMING},
        6: {"abstain": True, "chunk": f"{CPR}:4.4", "gap": "candidate-4-4-fixed-term-bundle"},
    },
    "S2": {
        2: {"verb": "disclose_account", "chunk": f"{CPR}:24.10", "args": {"data": ["invoice"]}},
        3: {"verb": "draft_reply", "chunk": f"{CPR}:26.7.2", "args": {"language": "ar"}},
        4: {"verb": "draft_reply", "chunk": f"{CPR}:26.7.2", "target": "Human agent H-01 (synthetic)",
            "args": {"recipient": "human", "language": "ar"}},
        5: {"abstain": True, "chunk": f"{CPR}:26.7.1", "gap": "gap-1"},
        6: {"verb": "request_report", "chunk": f"{CPR}:26.14.2", "target": "TDRA", "args": {}},
    },
    "S3": {
        1: {"verb": "receive_objection", "chunk": f"{PDPL}:17", "args": {}},
        2: {"verb": "disclose_account", "chunk": f"{CPR}:24.10", "target": "Dunes Retail LLC (synthetic)",
            "args": {"recipient": "third_party", "data": ["name", "msisdn", "top_up_history", "interconnection"]}},
        3: {"abstain": True, "chunk": f"{PDPL}:22", "gap": "gap-5"},
        4: {"verb": "draft_reply", "chunk": f"{CPR}:24.10",
            "args": {"language": "en", "model_provider": {"payload": ["question_text", "plan_name"]}}},
        5: {"verb": "propose_sale", "chunk": f"{CPR}:4.3", "args": {"outbound": True}},
    },
    "S4": {
        1: {"verb": "propose_change", "chunk": f"{CPR}:4.9",
            "args": {"change": "suspend", "services": ["mobile line", "home broadband"], "kept": [],
                     "basis": "contract term 14.2"}},
        2: {"verb": "propose_change", "chunk": f"{CPR}:4.9",
            "args": {"change": "notice", "languages": ["ar", "en"],
                     "content": ["actions_required", "due_dates", "consequences", "interruption_date"]}},
        3: {"verb": "propose_change", "chunk": f"{CPR}:4.9",
            "args": {"change": "interrupt", "services": SERVICES, "kept": KEPT}},
        4: {"verb": "request_human_review", "chunk": f"{PDPL}:18(4)", "args": {}},
        5: {"abstain": True, "chunk": f"{PDPL}:18(4)", "gap": "gap-4"},
    },
    "S5": {
        1: {"verb": "raise_dispute", "chunk": f"{CPR}:26.16.1", "target": "Sahab Telecom (synthetic)",
            "args": {"deadline": _deadline("cpr-26-16-1")}},
        2: {"verb": "order_restore", "chunk": f"{CPR}:26.11", "target": "Sahab Telecom (synthetic)", "args": {}},
        3: {"verb": "propose_change", "chunk": f"{CPR}:24.10", "args": {"change": "block_device"}},
        4: {"abstain": True, "chunk": f"{CPR}:24.10", "gap": "gap-3"},
        5: {"verb": "propose_change", "chunk": f"{CPR}:24.10", "args": {"change": "block_device"}},
        6: {"verb": "request_report", "chunk": f"{CPR}:26.16.1", "target": "TDRA", "args": {}},
    },
}


def _quote(chunk_id: str, lang: str) -> str:
    chunk = kb.get_chunk(*chunk_id.split(":", 1))
    text = chunk["text_ar"] if lang == "ar" and chunk["text_ar"] else chunk["text_en"]
    return text[:60]


def reply(sid: str, n: int, lang: str) -> dict[str, Any]:
    entry = SCRIPTS[sid][n]
    quote = _quote(entry["chunk"], lang)
    if entry.get("abstain"):
        return {"proposals": [{"verb": "flag_gap", "target": entry["gap"], "args": {"gap": entry["gap"]},
                               "clause_ids": [entry["chunk"]], "quote": quote,
                               "rationale": "no clause retrieved answers the question"}],
                "reasoning_chain": [INSUFFICIENT_EVIDENCE, f"scripted abstention; gap {entry['gap']}"]}
    return {"proposals": [{"verb": entry["verb"], "target": entry.get("target", "subscriber"),
                           "args": dict(entry["args"]), "clause_ids": [entry["chunk"]], "quote": quote,
                           "rationale": "scripted canonical proposal"}],
            "reasoning_chain": ["scripted"]}


def model(sid: str, lang: str = "en") -> MockModel:
    """MockModel keyed by request id `<scenario>-<n>-<agent>`; an unscripted request (a live inject) gets no
    proposals, which the coordinator records as an abstention."""
    steps = {s["n"]: s for s in data.load_scenario(sid)["steps"]}
    script = {f"{sid}-{n}-{steps[n]['to']}": reply(sid, n, lang) for n in SCRIPTS.get(sid, {})}
    return MockModel(script, model="scripted-mock")


class ScriptedRetriever:
    """Returns the scripted clause for a step's text (English or Arabic), within the agent's documents. Any other
    query goes to `fallback` (the real kb_main search) or finds nothing."""

    def __init__(self, sid: str, fallback: Callable[..., list[dict[str, Any]]] | None = None) -> None:
        self.by_text: dict[str, str] = {}
        for step in data.load_scenario(sid)["steps"]:
            entry = SCRIPTS.get(sid, {}).get(step["n"])
            if entry:
                self.by_text[step["text_en"]] = self.by_text[step["text_ar"]] = entry["chunk"]
        self.fallback = fallback

    def __call__(self, query: str, documents: list[str], k: int) -> list[dict[str, Any]]:
        chunk_id = self.by_text.get(query)
        if chunk_id is None:
            return self.fallback(query, documents, k) if self.fallback else []
        document_id, clause = chunk_id.split(":", 1)
        return [kb.get_chunk(document_id, clause)] if document_id in documents else []


def retriever(sid: str, fallback: Callable[..., list[dict[str, Any]]] | None = None) -> ScriptedRetriever:
    return ScriptedRetriever(sid, fallback)
