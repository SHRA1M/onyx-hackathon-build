"""Task 8 Part C4 (order 2026-10-21-task-8-part-c4): the corrected addressee rule, prompt v4 (three care lines) and
care's mandate widened to the clauses its gates test. Logs recorded before v4 replay as recorded."""

import ast
import json
from pathlib import Path

from onyx import data, eval as eval_mod, gate, kb, runs, scripted
from onyx.agents import Care
from onyx.coordinator import Coordinator
from onyx.model import MockModel

V4_LINES = (
    "Verbs: disclose_account is any act that gives account data (balance, plan, usage, invoices, personal details) "
    "to anyone, the subscriber included; propose_sale is offering or activating a paid product or bundle, including "
    "an outbound marketing call or message; propose_change is any change to the subscriber's service, including the "
    "warning notice before a suspension (args.change one of: notice, suspend, interrupt, disconnect, renew, upgrade, "
    "migrate, block_device); draft_reply is a message that does none of these.",
    "When the message asks Sahab to act, propose that act, cite the clauses that permit, condition or bar it, and say "
    "in the rationale which. Do not refuse in place of the gates: your refusal is not recorded; a gate's block is.",
    "Inside a Consumer Complaint (a grievance is expressed), a draft_reply is addressed to the named human agent: "
    "target 'Human agent H-xx', args.recipient 'human'. The human sends it.",
)
CARE_VERBS = ("propose_sale", "propose_change", "disclose_account", "draft_reply")


def _gate_event(entity, verb, target, **args):
    return {"action": "gate", "entity_id": entity, "new_value": {}, "old_value": {"verb": verb, "target": target,
                                                                                   "args": args}}


def _hits(sid, events, corrected=True):
    return eval_mod.action_hits(events, data.load_key(sid), data.load_scenario(sid), corrected=corrected)


# --- item 1: the addressee rule ------------------------------------------------------------------------------

def test_a_human_review_request_to_a_named_human_is_a_hit():
    events = [_gate_event("S4-4-data_office", "request_human_review", "Human agent H-03")]
    assert _hits("S4", events)[4]
    assert not _hits("S4", events, corrected=False)[4]  # the earlier rule, kept for the bake-off and C3 column


def test_a_draft_reply_to_a_human_on_a_subscribers_step_is_still_a_miss():
    events = [_gate_event("S2-3-care", "draft_reply", "Human agent H-01", recipient="human")]
    assert not _hits("S2", events)[3]


def test_a_draft_reply_to_the_human_on_a_humans_step_is_still_a_hit():
    events = [_gate_event("S2-4-care", "draft_reply", "Human agent H-01", recipient="human")]
    assert _hits("S2", events)[4]


# --- item 2: prompt v4 ---------------------------------------------------------------------------------------

def _system(agent_cls):
    seen = {}

    def respond(request_id, messages):
        seen["system"] = messages[0]["content"]
        return {"proposals": []}
    step = {"n": 2, "kind": "subscriber_message", "text_en": "What is my balance?", "facts": {}}
    agent_cls(MockModel(respond), lambda q, d, k: []).run("S1-2-x", step)
    return seen["system"]


def test_care_prompt_keeps_v4_line_2_word_for_word():
    """v5 (order 2026-10-22) rewrote lines 1 and 3 (tests/test_prompt_v5.py); line 2 stays."""
    system = _system(Care)
    assert V4_LINES[1] in system
    assert V4_LINES[0] not in system and V4_LINES[2] not in system


def test_other_agents_prompts_are_unchanged():
    from onyx.agents import Adviser, DataOffice, Tdra
    for cls in (Adviser, DataOffice, Tdra):
        assert not any(line in _system(cls) for line in V4_LINES)


def test_a_care_draft_reply_for_the_human_on_a_complaint_step_passes_the_complaint_gate(tmp_path):
    scenario = data.load_scenario("S2")
    human = scenario["steps"][3]["facts"]["human_actor"]
    quote = kb.get_chunk("tdra-cpr-v2-en", "26.7.2")["text_en"][:60]
    reply = {"proposals": [{"verb": "draft_reply", "target": human, "args": {"recipient": "human", "language": "ar"},
                            "clause_ids": ["tdra-cpr-v2-en:26.7.2"], "quote": quote, "rationale": "for H-01"}]}
    script = {**scripted.model("S2").script, "S2-4-care": reply}
    run = Coordinator(scenario, MockModel(script), scripted.retriever("S2"), log_path=tmp_path / "run.jsonl",
                      gaps_dir=tmp_path / "gaps")
    run.start()
    results = run.run()
    [(_, verdict)] = results[3].verdicts
    assert verdict.verdict == gate.ALLOW
    assert not any(r.get("gate") == "complaint_gate" and r.get("kind") == "check" and "precluded" in r["text"]
                   for r in verdict.reasons)


# --- item 3: care's mandate is its gates' clauses ------------------------------------------------------------

def _gate_rule_ids(verb):
    """Every rules.json id written in gate.py inside the verb's gate functions and the module names they use."""
    rules = {r["id"] for r in data.load_rules()}
    tree = ast.parse(Path(gate.__file__).read_text(encoding="utf-8"))
    top = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            top[node.name] = node
        elif isinstance(node, (ast.Assign, ast.AnnAssign)):
            for t in node.targets if isinstance(node, ast.Assign) else [node.target]:
                if isinstance(t, ast.Name) and t.id != "GATES":
                    top[t.id] = node

    def ids(name, seen):
        if name in seen or name not in top:
            return set()
        seen.add(name)
        found = set()
        for n in ast.walk(top[name]):
            if isinstance(n, ast.Constant) and n.value in rules:
                found.add(n.value)
            elif isinstance(n, ast.Name):
                found |= ids(n.id, seen)
        return found
    seen: set[str] = set()
    return set().union(*(ids(fn.__name__, seen) for fn in gate.GATES[verb]))


def test_care_mandate_clauses_are_the_clauses_its_gates_test():
    rules = {r["id"]: r for r in data.load_rules()}
    verbs = {v["verb"]: v for v in data.load_mandates()["care"]["verbs"]}
    for verb in CARE_VERBS:
        expected = {(rules[i]["document_id"], rules[i]["chunk"]) for i in _gate_rule_ids(verb)}
        got = {(c["document_id"], c["chunk"]) for c in verbs[verb]["clause_ids"]}
        assert expected <= got, f"{verb}: missing {sorted(expected - got)}"
        assert "Widened 2026-10-21 (hq C4) to the clauses the verb's gates test, read from gate.py." in verbs[verb]["note"]


def test_care_mandate_stays_inside_its_document_set():
    care = data.load_mandates()["care"]
    assert {c["document_id"] for v in care["verbs"] for c in v["clause_ids"]} <= set(care["documents"])


# --- replay of logs recorded before v4 -------------------------------------------------------------------------

class NoHits:
    def __call__(self, query, documents, k):
        return []


def test_replay_gives_each_agent_the_mandate_clauses_its_log_recorded(tmp_path):
    """A log recorded on the narrower mandate: a citation of a clause it was not given stays insufficient on
    replay, though today's wider mandate would give it."""
    quote = kb.get_chunk("tdra-cpr-v2-en", "3.3")["text_en"][:60]
    script = {**scripted.model("S1").script,
              "S1-2-care": {"proposals": [{"verb": "disclose_account", "target": "subscriber",
                                           "args": {"data": ["roaming_status"]},
                                           "clause_ids": ["tdra-cpr-v2-en:3.3"], "quote": quote}]}}
    log = tmp_path / "v3.jsonl"
    run = Coordinator(data.load_scenario("S1"), MockModel(script), NoHits(), log_path=log, gaps_dir=tmp_path / "gaps",
                      recorded_mandates={"care": ["tdra-cpr-v2-en:24.10"]})
    run.start()
    run.run()
    recorded, replayed = runs.replay(log)
    assert ("S1-2-care", "gate", gate.INSUFFICIENT) in {e[:3] for e in recorded}
    assert replayed == recorded
