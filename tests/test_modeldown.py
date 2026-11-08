"""Task 29 Part A (order 2026-10-29-task-29-field-take): the model is down, the gate still decides. A fault injection
on a recorded run: the model call at one step raises what OpenAICompatibleModel raises after its last attempt; the
coordinator logs `model_unavailable`, authors a plain-code `escalate_to_human` proposal and the gate decides it."""

import urllib.error

import pytest

from onyx import audit, data, gate, kb, modeldown, runs, scripted
from onyx.coordinator import Coordinator
from onyx.model import ATTEMPTS, FailingModel, MockModel

S2 = kb.REPO / "runs" / "c5" / "S2" / "run1.jsonl"
PAGE = kb.REPO / "docs" / "replay" / "model-down-S2.md"
H01 = "Human agent H-01 (synthetic)"


def test_failing_model_raises_at_step():
    inner = MockModel({"S1-1-adviser": {"proposals": [], "reasoning_chain": ["one"]},
                       "S1-3-care": {"proposals": [], "reasoning_chain": ["three"]}})
    model = FailingModel(inner, at=2)
    with pytest.raises(urllib.error.URLError) as raised:
        model.complete("S1-2-care", [])
    assert raised.value.attempts == ATTEMPTS
    assert model.complete("S1-1-adviser", []).raw == inner.complete("S1-1-adviser", []).raw
    assert model.complete("S1-3-care", []).raw == inner.complete("S1-3-care", []).raw
    assert model.complete("S1-12-care", []).raw == inner.complete("S1-12-care", []).raw  # step 12, not 2


def test_coordinator_survives_model_failure(tmp_path):
    log = tmp_path / "S1.jsonl"
    run = Coordinator(data.load_scenario("S1"), FailingModel(scripted.model("S1", "en"), at=2),
                      scripted.retriever("S1"), log_path=log, gaps_dir=tmp_path / "gaps")
    run.start()
    results = run.run()
    assert len(results) == len(data.load_scenario("S1")["steps"])  # the run completes
    events = runs._events(log)
    down = next(i for i, e in enumerate(events) if e["action"] == "model_unavailable")
    assert events[down]["actor"] == "care" and events[down]["entity_id"] == "S1-2-care"
    assert {"error", "attempts", "elapsed_ms", "step"} <= set(events[down]["new_value"])
    assert events[down]["new_value"]["error"] == "URLError" and events[down]["new_value"]["step"] == "S1-2"
    after = events[down + 1]
    assert after["action"] == "gate" and after["verdict"] == gate.HOLD
    assert after["old_value"]["verb"] == "escalate_to_human" and after["new_value"]["pending"] is True
    assert after["old_value"]["target"] == "a named trained human (licence 9.1)"  # S1 names no human
    assert after["old_value"]["args"] == {"reason": "model unavailable"}
    assert not any(e["action"] == "propose" and e["entity_id"] == "S1-2-care" for e in events)
    assert any(e["action"] == "propose" and e["entity_id"] == "S1-3-care" for e in events)  # later steps call it
    assert audit.verify(log)


def test_model_down_s2_hands_over(tmp_path):
    recorded, down = modeldown.compare(S2, at=3)
    assert [d[:3] for d in recorded if d[0].startswith("S2-3-")] == [
        ("S2-3-care", "gate", "block"), ("S2-3-care", "gate", "block")]
    step3 = [e for e in modeldown.replay_events(S2, at=3) if e["entity_id"].startswith("S2-3")]
    assert [e["action"] for e in step3] == ["release_event", "model_unavailable", "gate"]
    hand_over = step3[2]
    assert hand_over["verdict"] in {gate.HOLD, gate.BLOCK}
    assert hand_over["old_value"]["verb"] == "escalate_to_human" and hand_over["entity_id"] == "S2-3-coordinator"
    # the same named human the recorded run hands the conversation to (S2-4, the human's own request)
    recorded_human = next(e["old_value"]["target"] for e in runs._events(S2)
                          if e["action"] == "gate" and e["entity_id"] == "S2-4-care")
    assert hand_over["old_value"]["target"] == recorded_human == H01
    assert {"cpr-26-7-2", "licence-9-1"} <= set(hand_over["clause_ids"])
    assert hand_over["old_value"]["clause_ids"] == ["tdra-cpr-v2-en:26.7.2", "licence-2-2026:9.1"]
    # every other decision identical in verdict; in clauses too, except the S2-5 abstention's clauses-searched list,
    # which lists every clause the gate cited earlier in the case: the five cited only by the recorded S2-3
    # propose_change (no model proposed it here) drop out
    rec = [d for d in recorded if not d[0].startswith("S2-3-")]
    new = [d for d in down if not d[0].startswith("S2-3-")]
    assert [d[:3] for d in rec] == [d[:3] for d in new]
    differ = [(a, b) for a, b in zip(rec, new) if a != b]
    assert [a[:2] for a, _ in differ] == [("S2-5", "abstain")]
    a, b = differ[0]
    only_s2_3 = {"cpr-22-1-2", "cpr-22-3", "cpr-22-4", "pdpl-21-2-a", "cpr-22-2"}
    assert set(b[3]) < set(a[3]) and set(a[3]) - set(b[3]) == only_s2_3
    same, total, notes = modeldown.stays(runs._events(S2), modeldown.replay_events(S2, at=3), 3)
    assert (same, total, len(notes)) == (7, 8, 1)
    # the page is byte-identical on rerun, and equal to the committed page
    first = modeldown.write(S2, 3, tmp_path / "a").read_bytes()
    assert first == modeldown.write(S2, 3, tmp_path / "b").read_bytes() == PAGE.read_bytes()


def test_model_down_page_says_what_it_is():
    page = PAGE.read_text(encoding="utf-8")
    assert modeldown.LABEL in page and "chain ok" in page
    assert "No model took part in step 3 of the model-down column." in page
    assert "| S2-3 |" in page and "escalate_to_human" in page and "model_unavailable" in page


def test_cli_writes_the_page(tmp_path, capsys):
    from onyx.__main__ import main
    assert main(["model-down", str(S2), "--at", "3", "--out", str(tmp_path)]) == 0
    assert (tmp_path / "model-down-S2.md").read_bytes() == PAGE.read_bytes()
    assert "model-down-S2.md" in capsys.readouterr().out


# --- viewer, site, README -----------------------------------------------------------------------------------------

def test_viewer_opens_the_page_beside_the_whatif():
    from onyx import replay_viewer
    html = replay_viewer.render()
    whatif_button = '<button class="pick" data-sid="whatif-S2-gap-1">What-if: S2 under the rule gap 1 recommends</button>'
    down_button = '<button class="pick" data-sid="model-down-S2">Model down: S2, the call at step 3 fails</button>'
    assert html.index(whatif_button) < html.index(down_button)
    assert 'href="model-down-S2.md"' in html
    assert site_escape(modeldown.render(S2, 3)) in html


def site_escape(text):
    from html import escape
    return escape(text)


def test_site_reaches_it_in_one_click():
    from onyx import site
    pages = site.render()
    page = pages["modeldown.html"]
    for name in ("index.html", "runs.html"):
        assert 'href="modeldown.html"' in pages[name], name
    assert '<a href="modeldown.html">modeldown.html</a>' in pages["runs.html"]  # Task 51 A.1
    assert site_escape(modeldown.LABEL) in page
    assert "No model took part in step 3 of the model-down column." in page
    assert page.count('<tr data-step="S2-') == 4  # steps 3 to 6
    assert "<code>escalate_to_human</code> to Human agent H-01 (synthetic): hold" in page


def test_readme_paragraph_follows_the_whatif():
    readme = (kb.REPO / "README.md").read_text(encoding="utf-8")
    paragraphs = readme.split("\n\n")
    at = next(i for i, p in enumerate(paragraphs) if "Gap 1 is also tested, not only stated" in p)
    nxt = " ".join(paragraphs[at + 1].split())
    assert "uv run python -m onyx model-down runs/c5/S2/run1.jsonl --at 3" in nxt
    assert "the model call is made to fail at this step; nothing else changes" in nxt
    assert "`docs/replay/model-down-S2.md`" in nxt


def _deny(event):
    return [r["text"] for r in event["new_value"]["reasons"] if r.get("gate") == "deny_by_default"
            and r.get("kind") == "check"]


def test_model_down_hold_says_the_model_was_unavailable():
    """Task 29 Part B, hq ruling 2026-10-29: on the model-down path the deny-by-default reason says the model was
    unavailable, not that the adviser answered; it is in the log on the gate event, the step's last event, so
    nothing acts before it is written (layer 7). The adviser's own pending hold at S2-5 keeps its recorded words."""
    events = modeldown.replay_events(S2, at=3)
    step3 = [e for e in events if e["entity_id"].startswith("S2-3")]
    assert [e["action"] for e in step3] == ["release_event", "model_unavailable", "gate"]
    assert _deny(step3[-1]) == ["the model was unavailable on S2-3: no model proposed and no VERIFIED clause "
                                "permits escalate_to_human; held for a human"]
    assert not any("adviser answered" in r.get("text", "") for r in step3[-1]["new_value"]["reasons"])
    recorded = runs._events(S2)
    pending = [(e["entity_id"], _deny(e)) for e in recorded if e["action"] == "gate" and e["new_value"].get("pending")]
    assert pending and all("the adviser answered INSUFFICIENT_EVIDENCE" in t for _, texts in pending for t in texts)
    assert pending == [(e["entity_id"], _deny(e)) for e in events if e["action"] == "gate"
                       and e["new_value"].get("pending") and not e["entity_id"].startswith("S2-3")]
