"""Task 8 Part C1 (order 2026-10-21-task-8-part-c, items 5 and 6): prompt v2. The model proposes what the step calls
for and the gate decides; facts are the operator's records; mandate clauses travel in every prompt; the adviser
gets the gap register; the schema field reasoning_chain goes on the wire as notes."""

import json

import pytest

from onyx import audit, data, kb
from onyx.agents import Adviser, Care, base
from onyx.model import MockModel, RecordedModel
from onyx.coordinator import Coordinator
from onyx import scripted

STEP = {"n": 2, "to": "care", "kind": "subscriber_message",
        "text_en": "Hi, I fly to London tonight. Does my line work there? What will it cost me?",
        "text_ar": "مرحباً، سأسافر إلى لندن الليلة. هل يعمل خطي هناك؟", "facts": {}}


class NoHits:
    def __call__(self, query, documents, k):
        return []


class OneHit:
    """Retrieves one chunk that is also a care mandate clause, and one that is not."""

    def __call__(self, query, documents, k):
        return [kb.get_chunk("tdra-cpr-v2-en", "4.3"), kb.get_chunk("tdra-cpr-v2-en", "3.3")]


def _prompt(agent_cls, lang="en", retriever=None):
    seen = {}

    def respond(request_id, messages):
        seen["messages"] = messages
        return {"proposals": []}
    agent_cls(MockModel(respond), retriever or NoHits()).run("S1-2-" + agent_cls.name, STEP, lang=lang)
    return seen["messages"][0]["content"], seen["messages"][1]["content"]


def _mandate_ids(agent_cls):
    ids = []
    for verb in agent_cls.mandate():
        ids += [f"{c['document_id']}:{c['chunk']}" for c in verb["clause_ids"]
                if f"{c['document_id']}:{c['chunk']}" not in ids]
    return ids


def test_prompt_asks_for_the_action_and_leaves_the_decision_to_the_gates():
    system, _ = _prompt(Care)
    assert "If no clause below answers the step" not in system
    assert ("Propose the action this step calls for, citing the clauses that govern it; the gates decide whether "
            "it is allowed.") in system
    assert ("Propose nothing, and make '<INSUFFICIENT_EVIDENCE>' the first entry of the last field, only when the "
            "step asks for a rule, figure or deadline that no clause below states.") in system


def test_prompt_treats_facts_as_the_operators_records():
    system, _ = _prompt(Care)
    assert ("Facts are Sahab's own records (account, catalogue, consent log). Use them as true. Clauses are for "
            "citations only.") in system


@pytest.mark.parametrize("lang, line", [("en", "Reply in the language of this run: English."),
                                        ("ar", "Reply in the language of this run: Arabic.")])
def test_prompt_names_the_language_of_the_run(lang, line):
    system, _ = _prompt(Care, lang)
    assert line in system


def test_mandate_clauses_reach_the_prompt_first_and_once():
    _, user = _prompt(Care, retriever=OneHit())
    mandate = _mandate_ids(Care)
    positions = [user.index(f"[{cid}]") for cid in mandate]
    assert positions == sorted(positions)
    assert user.count("[tdra-cpr-v2-en:4.3]") == 1  # retrieved and mandate: given once
    assert user.index("[tdra-cpr-v2-en:3.3]") > positions[-1]  # retrieved only: after the mandate clauses


def test_sources_used_and_sources_mandate_are_logged_apart(tmp_path):
    log = audit.AuditLog(tmp_path / "run.jsonl", clock=lambda: "2026-10-21T12:00:00.000+00:00")
    log.start("S1")
    out = Care(MockModel(), OneHit(), log).run("S1-2-care", STEP)
    assert out.sources_used == ["tdra-cpr-v2-en:4.3", "tdra-cpr-v2-en:3.3"]
    assert out.sources_mandate == _mandate_ids(Care)
    [propose] = [json.loads(l) for l in log.path.read_text(encoding="utf-8").splitlines() if '"propose"' in l]
    assert propose["new_value"]["sources_used"] == out.sources_used
    assert propose["new_value"]["sources_mandate"] == out.sources_mandate


def test_gate_accepts_a_cited_mandate_clause_that_was_not_retrieved(tmp_path):
    """Citation validity checks against what was given: a mandate clause is given even when retrieval missed it."""
    quote = kb.get_chunk("tdra-cpr-v2-en", "24.10")["text_en"][:60]
    model = MockModel({"S1-2-care": {"proposals": [{"verb": "disclose_account", "target": "subscriber",
                                                    "args": {"data": ["roaming_status"]},
                                                    "clause_ids": ["tdra-cpr-v2-en:24.10"], "quote": quote}]}})
    run = Coordinator(data.load_scenario("S1"), model, NoHits(), log_path=tmp_path / "run.jsonl",
                      gaps_dir=tmp_path / "gaps")
    run.start()
    run.step(data.load_scenario("S1")["steps"][0])
    result = run.step(data.load_scenario("S1")["steps"][1])
    [(_, verdict)] = result.verdicts
    assert not any("was not retrieved" in r.get("text", "") for r in verdict.reasons)


def test_adviser_prompt_lists_the_gap_register():
    system, _ = _prompt(Adviser)
    gaps = data.load_gaps()
    assert [g["id"] for g in gaps["gaps"]][:7] == [f"gap-{n}" for n in range(1, 8)]
    for n, gap in enumerate(gaps["gaps"], 1):
        assert f"{n}. {gap['id']}: {gap['line']}" in system
    assert "propose a `flag_gap` action with the register id in `args.gap`, in every language" in system


def test_gap_register_holds_every_id_the_keys_expect():
    expected = {g for sid in ("S1", "S2", "S3", "S4", "S5") for g in data.load_key(sid)["gaps_expected"]}
    assert expected <= {g["id"] for g in data.load_gaps()["gaps"]}


def test_care_prompt_has_no_gap_register():
    system, _ = _prompt(Care)
    assert "gap-1" not in system


def test_schema_on_the_wire_names_notes():
    system, _ = _prompt(Care)
    assert '"notes": []' in system and "reasoning_chain" not in system


@pytest.mark.parametrize("field", ["notes", "reasoning_chain"])
def test_parse_output_accepts_notes_and_reasoning_chain(field):
    out = base.parse_output("care", json.dumps({"proposals": [], field: [base.INSUFFICIENT_EVIDENCE, "why"]}))
    assert out.reasoning_chain == [base.INSUFFICIENT_EVIDENCE, "why"]


def test_angle_bracketed_insufficient_evidence_counts_as_abstention():
    """The prompt spells it '<INSUFFICIENT_EVIDENCE>'; a model that copies the brackets still abstains."""
    out = base.parse_output("adviser", json.dumps({"proposals": [], "notes": ["<INSUFFICIENT_EVIDENCE>"]}))
    assert out.reasoning_chain[:1] == [base.INSUFFICIENT_EVIDENCE]


def test_replay_of_a_log_without_mandate_clauses_gives_the_gate_what_the_run_gave(tmp_path):
    """A log recorded before prompt v2 carries no mandate clauses; replayed today, a citation of a mandate clause
    retrieval missed must stay insufficient, as it was recorded."""
    from onyx import gate, runs
    quote = kb.get_chunk("tdra-cpr-v2-en", "24.10")["text_en"][:60]
    script = {**scripted.model("S1").script,
              "S1-2-care": {"proposals": [{"verb": "disclose_account", "target": "subscriber",
                                           "args": {"data": ["roaming_status"]},
                                           "clause_ids": ["tdra-cpr-v2-en:24.10"], "quote": quote}]}}
    log = tmp_path / "v1.jsonl"
    run = Coordinator(data.load_scenario("S1"), MockModel(script), NoHits(), log_path=log,
                      gaps_dir=tmp_path / "gaps", mandate_clauses=False)
    run.start()
    run.run()
    recorded, replayed = runs.replay(log)
    assert ("S1-2-care", "gate", gate.INSUFFICIENT) in {e[:3] for e in recorded}
    assert replayed == recorded
