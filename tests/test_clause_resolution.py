"""hq addendum to C4 (order 2026-10-21-task-8-part-c4-addendum): a cited id that is not among the clauses given to
the agent for the step resolves to the one given clause whose id is equal once the language ending (-en, -ar) is
removed from the document part of both. Never against the whole KB, never when two match. One function, used by the
gate and by the eval; logs recorded before it replay as recorded."""

from onyx import data, eval as eval_mod, gate, runs, scripted
from onyx.agents.base import Proposal
from onyx.coordinator import Coordinator
from onyx.model import MockModel

GIVEN_EN = "cabinet-56-2024-en:5(6)"
CITED = "cabinet-56-2024:5(6)"


def _quote():
    return gate.Knowledge.load().chunk(GIVEN_EN)["text_en"][:60]


def test_an_id_missing_its_language_ending_resolves_to_the_one_given_clause():
    assert gate.resolve_ids([CITED], [GIVEN_EN, "licence-2-2026:9.1"]) == (
        [GIVEN_EN], [{"cited": CITED, "resolved": GIVEN_EN}])


def test_the_same_id_with_the_clause_not_given_stays_as_cited():
    assert gate.resolve_ids([CITED], ["cabinet-56-2024-en:5(7)"]) == ([CITED], [])


def test_an_id_matching_two_given_clauses_stays_as_cited():
    assert gate.resolve_ids([CITED], [GIVEN_EN, "cabinet-56-2024-ar:5(6)"]) == ([CITED], [])


def test_an_exact_id_is_untouched_and_a_repeated_given_id_is_one_clause():
    assert gate.resolve_ids([GIVEN_EN], [GIVEN_EN, GIVEN_EN]) == ([GIVEN_EN], [])
    assert gate.resolve_ids([CITED], [GIVEN_EN, GIVEN_EN]) == ([GIVEN_EN], [{"cited": CITED, "resolved": GIVEN_EN}])


def test_eval_citation_valid_with_the_clause_given_and_invalid_without():
    kb = gate.Knowledge.load()
    proposal = {"verb": "draft_reply", "clause_ids": [CITED], "quote": _quote()}
    assert eval_mod._citation_valid(proposal, kb, [GIVEN_EN])
    assert not eval_mod._citation_valid(proposal, kb, ["cabinet-56-2024-en:5(7)"])
    assert not eval_mod._citation_valid(proposal, kb, [GIVEN_EN, "cabinet-56-2024-ar:5(6)"])
    assert not eval_mod._citation_valid(proposal, kb)  # the earlier rule: no resolution


def _state(resolve=True):
    return gate.State(agent="care", inject="S1-3", released={"S1-3"}, retrieved={GIVEN_EN}, channel="app_chat",
                      resolve=resolve)


def test_the_gate_resolves_and_records_cited_and_resolved():
    proposal = Proposal(verb="draft_reply", target="subscriber", clause_ids=[CITED], quote=_quote())
    verdict = gate.decide(proposal, _state())
    assert not any("not retrieved" in r["text"] for r in verdict.reasons)
    assert verdict.resolved == [{"cited": CITED, "resolved": GIVEN_EN}]
    assert proposal.clause_ids == [CITED]  # the proposal as cited is kept for the log


def test_the_gate_without_resolution_decides_as_before():
    proposal = Proposal(verb="draft_reply", target="subscriber", clause_ids=[CITED], quote=_quote())
    verdict = gate.decide(proposal, _state(resolve=False))
    assert verdict.verdict == gate.INSUFFICIENT and verdict.resolved == []


def test_a_new_run_logs_the_correction_on_the_gate_event_and_replays_the_same(tmp_path):
    script = scripted.model("S1", "en").script
    reply = {**script["S1-3-care"]}
    reply["proposals"] = [{**reply["proposals"][0], "clause_ids": ["tdra-cpr-v2:4.3"]}]
    log = tmp_path / "run1.jsonl"
    run = Coordinator(data.load_scenario("S1"), MockModel({**script, "S1-3-care": reply}, model="scripted-mock"),
                      scripted.retriever("S1"), log_path=log, gaps_dir=tmp_path / "gaps")
    run.start(source="scripted", model="scripted-mock", run=1, retrieval="scripted")
    run.run()
    events = eval_mod._events(log)
    assert events[0]["new_value"]["clause_resolution"] is True
    gate_event = next(e for e in events if e["action"] == "gate" and e["entity_id"] == "S1-3-care")
    assert gate_event["old_value"]["clause_ids"] == ["tdra-cpr-v2:4.3"]
    assert gate_event["new_value"]["resolved"] == [{"cited": "tdra-cpr-v2:4.3", "resolved": "tdra-cpr-v2-en:4.3"}]
    assert gate_event["verdict"] != gate.INSUFFICIENT
    recorded, replayed = runs.replay(log)
    assert recorded == replayed


def test_a_log_recorded_before_the_rule_replays_as_recorded():
    log = "runs/c4/S1/run1.jsonl"
    recorded, replayed = runs.replay(log)
    assert recorded == replayed
    assert ("S1-3-care", "gate", gate.INSUFFICIENT, ()) in recorded
