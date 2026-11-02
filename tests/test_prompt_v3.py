"""Task 8 Part C2b (order 2026-10-21-task-8-part-c2b): prompt v3. In Arabic the adviser named the right gap id in
`notes` instead of a flag_gap proposal; v3 asks for flag_gap in every language, and parse_output records a register
id found in an abstaining reply's notes, with gaps_source "notes". Logs recorded before v3 replay as recorded."""

import json

from onyx import data, eval as eval_mod, gate, runs, scripted
from onyx.agents import Adviser, base
from onyx.coordinator import Coordinator
from onyx.model import MockModel

V3_LINE = ("When a rule is missing, propose a `flag_gap` action with the register id in `args.gap`, in every "
           "language, also when you abstain. A gap id written only in `notes` is not recorded.")
NOTES_REPLY = {"proposals": [], "notes": ["<INSUFFICIENT_EVIDENCE>", "gap-3: التحقق الكافي غير معرّف في النص"]}


def _adviser_prompt():
    seen = {}

    def respond(request_id, messages):
        seen["system"] = messages[0]["content"]
        return {"proposals": []}
    step = {"n": 4, "kind": "agent_question", "text_en": "What counts as adequate verification?", "facts": {}}
    Adviser(MockModel(respond), lambda q, d, k: []).run("S5-4-adviser", step)
    return seen["system"]


def _s5(tmp_path, reply, lang="ar", **kwargs):
    """S5 on the scripted model with the abstention step's reply replaced; returns the adviser's abstain event."""
    script = {**scripted.model("S5", lang).script, "S5-4-adviser": reply}
    log = tmp_path / "run1.jsonl"
    run = Coordinator(data.load_scenario("S5"), MockModel(script, model="scripted-mock"), scripted.retriever("S5"),
                      log_path=log, gaps_dir=tmp_path / "gaps", lang=lang, **kwargs)
    run.start(source="scripted", model="scripted-mock", run=1, retrieval="scripted")
    run.run()
    events = [json.loads(line) for line in log.read_text(encoding="utf-8").splitlines()]
    [abstain] = [e for e in events if e["action"] == "abstain" and e["actor"] == "adviser"]
    return log, abstain


def test_adviser_prompt_asks_for_flag_gap_in_every_language():
    system = _adviser_prompt()
    assert V3_LINE in system
    assert "When you flag a gap or abstain because a rule is missing, name the register id" not in system


def test_parse_output_finds_a_register_id_in_an_abstaining_replys_notes():
    out = base.parse_output("adviser", json.dumps(NOTES_REPLY, ensure_ascii=False))
    assert out.gaps_in_notes == ["gap-3"]


def test_an_id_not_in_the_register_is_ignored():
    reply = {"proposals": [], "notes": ["<INSUFFICIENT_EVIDENCE>", "gap-99 and gap-16 and gap-3x and Gap-3 are not ids"]}  # gap-13 to gap-15 joined the register (Task 41)
    assert base.parse_output("adviser", json.dumps(reply)).gaps_in_notes == []


def test_a_reply_that_does_not_abstain_takes_no_gap_from_notes():
    reply = {"proposals": [{"verb": "draft_reply", "target": "subscriber"}], "notes": ["see gap-3"]}
    assert base.parse_output("adviser", json.dumps(reply)).gaps_in_notes == []


def test_arabic_abstention_with_the_gap_in_notes_records_it_with_source_notes(tmp_path):
    _, abstain = _s5(tmp_path, NOTES_REPLY)
    assert abstain["new_value"]["gaps"] == ["gap-3"]
    assert abstain["new_value"]["gaps_source"] == "notes"


def test_english_flag_gap_proposal_path_is_unchanged(tmp_path):
    _, abstain = _s5(tmp_path, scripted.reply("S5", 4, "en"), lang="en")
    assert abstain["new_value"]["gaps"] == ["gap-3"]
    assert abstain["new_value"]["gaps_source"] == "proposal"


def test_eval_counts_notes_gaps_in_gap_recall_and_shows_how_many(tmp_path):
    log, _ = _s5(tmp_path, NOTES_REPLY)
    metrics = eval_mod.run_metrics(log, data.load_key("S5"), data.load_scenario("S5"), gate.Knowledge.load(),
                                   eval_mod._rules_by_chunk())
    assert metrics["gap_recall"] == 1.0
    assert metrics["gaps_from_notes"] == 1


def test_a_log_recorded_before_v3_replays_as_recorded(tmp_path, monkeypatch):
    """Before v3 a gap in notes was not recorded; the replay of such a log must not record it either."""
    log, abstain = _s5(tmp_path, NOTES_REPLY, notes_gaps=False)
    assert abstain["new_value"]["gaps"] == [] and "gaps_source" not in abstain["new_value"]
    seen = {}

    class Spy(Coordinator):
        def __init__(self, *args, **kwargs):
            seen["notes_gaps"] = kwargs.get("notes_gaps", True)
            super().__init__(*args, **kwargs)
    monkeypatch.setattr("onyx.coordinator.Coordinator", Spy)
    recorded, replayed = runs.replay(log)
    assert seen["notes_gaps"] is False
    assert replayed == recorded
