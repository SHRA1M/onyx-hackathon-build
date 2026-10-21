import json
import socket

import pytest

from onyx import audit, kb
from onyx.agents import AGENTS, Adviser, Care, base
from onyx.model import MockModel, RecordedModel


@pytest.fixture(scope="module")
def retriever(tmp_path_factory):
    client = kb.ingest(path=tmp_path_factory.mktemp("chroma"), embedding_function=kb.HashEmbedding())
    return base.ChromaRetriever(client.get_collection("kb_main", embedding_function=kb.HashEmbedding()))


@pytest.fixture
def log(tmp_path):
    log = audit.AuditLog(tmp_path / "run.jsonl", clock=lambda: "2026-10-21T12:00:00.000+00:00")
    log.start("S1")
    return log


def _events(log):
    return [json.loads(line) for line in log.path.read_text(encoding="utf-8").splitlines()]


def _proposal(verb, **extra):
    return {"verb": verb, "target": "account", "args": {}, "clause_ids": [], "quote": "", "rationale": "", **extra}


STEP = {"n": 2, "to": "care", "kind": "subscriber_message",
        "text_en": "Hi, I fly to London tonight. Does my line work there? What will it cost me?",
        "text_ar": "مرحباً، سأسافر إلى لندن الليلة. هل يعمل خطي هناك؟", "facts": {}}


def test_care_agent_cannot_call_order_restore(retriever, log):
    model = MockModel({"S1-2-care": {"proposals": [_proposal("order_restore"), _proposal("propose_sale")]}})
    out = Care(model, retriever, log).run("S1-2-care", STEP)
    assert [p.verb for p in out.proposals] == ["propose_sale"]
    assert [p.verb for p in out.rejected] == ["order_restore"]
    rejected = [e for e in _events(log) if e["action"] == "reject_proposal"]
    assert len(rejected) == 1 and rejected[0]["actor"] == "care"
    assert "order_restore" in rejected[0]["reason"] and "mandate" in rejected[0]["reason"]


@pytest.mark.parametrize("channel, clauses", [
    ("voice", ["4.17"]),
    ("app_chat", ["4.22", "4.10"]),
    ("web", ["4.23"]),
])
def test_adviser_classifies_channel(retriever, log, channel, clauses):
    out = Adviser(MockModel(), retriever, log).classify_channel("S1-1-adviser", channel)
    [proposal] = out.proposals
    assert proposal.verb == "classify_channel"
    for clause in clauses:
        assert f"tdra-cpr-v2-en:{clause}" in proposal.clause_ids
    cited = kb.get_chunk("tdra-cpr-v2-en", clauses[0])
    assert len(proposal.quote) >= 20 and proposal.quote in cited["text_en"]
    [event] = [e for e in _events(log) if e["action"] == "classify_channel"]
    assert event["actor"] == "adviser" and event["new_value"]["channel"] == channel
    assert event["clause_ids"] == proposal.clause_ids
    assert event["model_response"] is None  # plain code, no model call


def test_adviser_refuses_an_unknown_channel(retriever, log):
    with pytest.raises(ValueError):
        Adviser(MockModel(), retriever, log).classify_channel("S1-1-adviser", "carrier_pigeon")


def test_mock_model_runs_offline(retriever, log, monkeypatch):
    def no_network(*args, **kwargs):
        raise AssertionError("network used")
    monkeypatch.setattr(socket, "socket", no_network)
    model = MockModel({"S1-2-care": {"proposals": [_proposal("propose_sale")], "reasoning_chain": ["offer"]}})
    out = Care(model, retriever, log).run("S1-2-care", STEP)
    assert [p.verb for p in out.proposals] == ["propose_sale"]
    assert out.reasoning_chain == ["offer"]
    [event] = [e for e in _events(log) if e["action"] == "propose"]
    assert event["model_request_id"] == "S1-2-care" and event["model_response"]["model"] == "mock"
    assert audit.verify(log.path)


def test_retrieval_stays_in_mandate_documents(retriever):
    for name, cls in AGENTS.items():
        agent = cls(MockModel(), retriever)
        hits = agent.retrieve("consent personal data complaint human review dispute", k=20)
        assert hits, name
        assert {h["document_id"] for h in hits} <= set(agent.documents), name


def test_sources_used_are_what_the_agent_retrieved(retriever, log):
    model = MockModel({"S1-2-care": {"proposals": [], "sources_used": ["gdpr-art22:22"]}})
    out = Care(model, retriever, log).run("S1-2-care", STEP)
    assert out.sources_used and "gdpr-art22:22" not in out.sources_used
    assert all(s.split(":")[0] in Care.documents_of() for s in out.sources_used)


def test_unparseable_response_proposes_nothing(retriever, log):
    out = Care(MockModel({"S1-2-care": "Sure! I will activate it now."}), retriever, log).run("S1-2-care", STEP)
    assert out.proposals == [] and "unparseable" in out.reasoning_chain[0]


def test_recorded_model_replays_a_run(retriever, log):
    script = {"S1-2-care": {"proposals": [_proposal("propose_sale", quote="x")], "reasoning_chain": ["r"]}}
    first = Care(MockModel(script), retriever, log).run("S1-2-care", STEP)
    replayed = Care(RecordedModel(log.path), retriever).run("S1-2-care", STEP)
    assert replayed.to_dict() == first.to_dict()
    with pytest.raises(KeyError):
        RecordedModel(log.path).complete("S9-9-care", [])


def test_arabic_step_text_reaches_the_model(retriever):
    seen = {}

    def respond(request_id, messages):
        seen["text"] = messages[-1]["content"]
        return {"proposals": []}
    Care(MockModel(respond), retriever).run("S1-2-care", STEP, lang="ar")
    assert STEP["text_ar"] in seen["text"]
