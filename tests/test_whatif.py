"""Task 19 (order 2026-10-23-task-19-whatif-replay; hq ruling 2026-10-23, clock on block verdicts only): a recorded
run replayed under a proposed rule that the gate never loads. On S2 exactly two decisions change, in both languages,
and one second-order finding appears."""

import json

import pytest

from onyx import data, gate, kb, replay_viewer, runs, whatif
from onyx.__main__ import main

S2 = kb.REPO / "runs" / "c5" / "S2" / "run1.jsonl"
S2_AR = kb.REPO / "runs" / "c5" / "S2" / "ar" / "run1.jsonl"
PAGE = kb.REPO / "docs" / "replay" / "whatif-S2-gap-1.md"
README = (kb.REPO / "README.md").read_text(encoding="utf-8")


# --- a: the proposed rule is data the gate never loads ----------------------------------------------------------

def test_proposed_rule_loads_and_the_gate_never_sees_it():
    rule = whatif.load_rule("gap-1")
    assert rule["id"] == "proposed-gap-1" and rule["status"] == "proposed, not law"
    assert rule["adds_deadline_to"] == "cpr-26-7-2" and rule["answers"] == {"verb": "route", "mark": "within_time"}
    ids = set(gate.Knowledge.load().rules)
    assert len(ids) == 109 and not any(i.startswith("proposed-") for i in ids)
    assert [r["id"] for r in data.load_rules()] == list(gate.Knowledge.load().rules)


# --- b: no rule equals replay -----------------------------------------------------------------------------------

def test_no_rule_equals_replay():
    recorded, replayed, changes = whatif.replay_under(S2)
    assert (recorded, replayed) == runs.replay(S2)
    assert changes == []


# --- c: exactly two decisions change, in both languages ---------------------------------------------------------

@pytest.mark.parametrize("path", [S2, S2_AR], ids=["en", "ar"])
def test_gap_1_changes_exactly_s2_3_and_s2_5(path):
    recorded, replayed, changes = whatif.replay_under(path, "gap-1")
    assert [c[:4] for c in changes] == [("S2-3-care", "draft_reply", "block", "block"),
                                        ("S2-5-coordinator", "route", "hold", "allow")]
    care, route = changes[0][4], changes[1][4]
    assert [r["kind"] for r in care] == ["obligation"] and care[0]["proposed"] is True
    assert care[0]["deadline"] == {"rule": "proposed-gap-1", "value": "2", "unit": "minutes",
                                   "from": "2026-10-16 10:12 (synthetic)"}
    assert care[0]["text"] == "hand over within 2 minutes of 2026-10-16 10:12 (synthetic) (proposed-gap-1, not law)"
    assert [r["kind"] for r in route] == ["check", "finding"] and all(r["proposed"] is True for r in route)
    assert "second-order: the rule needs the hand-over time recorded" in route[1]["text"]
    # every other decision equal; clause_ids never gain the proposed id
    same = [(a, b) for a, b in zip(recorded, replayed) if a[0] not in {"S2-3-care", "S2-5-coordinator"}]
    assert all(a == b for a, b in same) and len(recorded) == len(replayed)
    assert all("proposed-gap-1" not in d[3] for d in replayed)


def test_s2_4_is_byte_identical_under_the_rule():  # hq ruling 2026-10-23 item 4
    plain, under = whatif.replay_events(S2), whatif.replay_events(S2, whatif.load_rule("gap-1"))
    step4 = [whatif.comparable(e) for e in plain if e["entity_id"].startswith("S2-4")]
    assert step4 and step4 == [whatif.comparable(e) for e in under if e["entity_id"].startswith("S2-4")]


# --- d: only a deny-by-default hold is released -----------------------------------------------------------------

def _route(mark="within_time"):
    from onyx.agents.base import Proposal
    return Proposal(verb="route", target="S2-3 hand-over", args={"handover_step": 3, "mark": mark})


def _state():
    return gate.State(agent="coordinator", inject="S2-5", facts={"grievance_expressed": True, "time": "t0"})


def test_a_hold_with_any_other_check_is_never_released(monkeypatch):
    made_up = gate.Verdict(gate.HOLD, ["cpr-26-7-2"], [
        {"gate": "deny_by_default", "kind": "check", "text": "held"},
        {"gate": "complaint_gate", "kind": "check", "text": "another check", "clause": "cpr-26-7-2"}])
    monkeypatch.setattr(gate, "decide_pending", lambda p, s, kb=None: made_up)
    decide = whatif.decide_pending_under(whatif.load_rule("gap-1"), [])
    assert decide(_route(), _state(), None) is made_up


def test_a_deny_by_default_hold_on_another_question_is_not_released(monkeypatch):
    held = gate.Verdict(gate.HOLD, [], [{"gate": "deny_by_default", "kind": "check", "text": "held"}])
    monkeypatch.setattr(gate, "decide_pending", lambda p, s, kb=None: held)
    decide = whatif.decide_pending_under(whatif.load_rule("gap-1"), [])
    assert decide(_route(mark="other"), _state(), None) is held


def test_the_clock_is_added_on_block_only(monkeypatch):
    duty = {"gate": "complaint_gate", "kind": "obligation", "text": "hand over", "clause": "cpr-26-7-2"}
    rule = whatif.load_rule("gap-1")
    for verdict, added in ((gate.BLOCK, 1), (gate.HOLD, 0), (gate.ALLOW, 0)):
        given = gate.Verdict(verdict, ["cpr-26-7-2"], [duty])
        monkeypatch.setattr(gate, "decide", lambda p, s, kb=None, v=given: v)
        out = whatif.decide_under(rule)(_route(), _state(), None)
        assert len(out.reasons) - 1 == added and out.clause_ids == ["cpr-26-7-2"]


# --- e: page, README, index ---------------------------------------------------------------------------------------

def test_page_is_current_and_says_proposed_not_law():
    assert PAGE.read_text(encoding="utf-8") == whatif.render(S2, "gap-1"), "run `python -m onyx whatif ... --rule gap-1`"
    text = PAGE.read_text(encoding="utf-8")
    rule = whatif.load_rule("gap-1")
    for part in ("## Proposed rule, not law", rule["text_en"], rule["text_ar"], rule["value_basis"], "## What changes",
                 "## What stays", "8 of 10 decisions identical", "## Second-order finding", "proposed, not law",
                 "Generated by `python -m onyx whatif`; the gate, keys and committed runs are unchanged; this page is a "
                 "what-if, not a result."):
        assert part in text, part


def test_readme_carries_the_two_sentences_and_the_reviewer_line():
    flat = " ".join(README.split())
    assert ("Gap 1 is also tested, not only stated: `uv run python -m onyx whatif runs/c5/S2/run1.jsonl --rule gap-1` "
            "replays the recorded S2 run under the rule the register recommends (proposed, not law): the held step "
            "S2-5 is released, the hand-over duty gains a two-minute clock, and one new finding appears: the rule needs "
            "the hand-over time recorded, which this log does not carry. Page: `docs/replay/whatif-S2-gap-1.md`.") in flat
    line2 = next(l for l in README.splitlines() if l.startswith("2. Agent capability in error scenarios"))
    assert line2.endswith("; `docs/replay/whatif-S2-gap-1.md` tests gap 1's recommended rule by replay")


def test_index_links_the_page_and_opens_its_text():
    html = replay_viewer.render()
    assert 'href="whatif-S2-gap-1.md"' in html
    assert '<button data-sid="whatif-S2-gap-1">What-if: S2 under the rule gap 1 recommends</button>' in html
    assert "proposed, not law" in html


# --- the command line ---------------------------------------------------------------------------------------------

def test_cli_without_a_rule_equals_replay(capsys):
    assert main(["whatif", str(S2)]) == 0
    out = capsys.readouterr().out
    assert "no rule: equals replay" in out and "True" in out


def test_cli_with_the_rule_prints_the_changes_and_writes_the_page(tmp_path, capsys):
    assert main(["whatif", str(S2), "--rule", "gap-1", "--out", str(tmp_path)]) == 0
    out = capsys.readouterr().out
    assert "S2-3-care" in out and "S2-5-coordinator" in out and "hold -> allow" in out
    assert (tmp_path / "whatif-S2-gap-1.md").read_bytes() == PAGE.read_bytes()


def test_the_rule_file_is_lf_json():
    raw = (data.DATA_DIR / "proposed" / "gap-1.json").read_bytes()
    assert b"\r\n" not in raw and json.loads(raw)["gap"] == "gap-1"
