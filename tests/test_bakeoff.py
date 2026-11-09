"""Task 8 live order, Part B: the bake-off table (eval/bakeoff.md) and hq's decision rule. Fixtures are copies of
the committed scripted runs, so no model call is made."""

import shutil
from pathlib import Path

from onyx import bakeoff, runs

ROOT = Path(__file__).resolve().parents[1]
SCRIPTED = ROOT / "runs" / "scripted"
OPUS, SONNET, HAIKU = bakeoff.MODELS


def _copy_runs(dest: Path) -> None:
    for sid in runs.SCENARIOS:
        for lang in runs.LANGS:
            src = runs.run_path(SCRIPTED, sid, 1, lang)
            out = runs.run_path(dest, sid, 1, lang)
            out.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(src, out)


def test_parse_failures_count_unreadable_replies():
    events = [{"action": "propose", "new_value": {"reasoning_chain": [
                  "unparseable model response: no JSON in the agreed schema"], "proposals": []}},
              {"action": "propose", "new_value": {"reasoning_chain": ["INSUFFICIENT_EVIDENCE"], "proposals": []}}]
    assert bakeoff.parse_failures(events) == 1


def test_quote_failures_count_quotes_not_verbatim_in_a_cited_clause():
    kb = bakeoff.gate.Knowledge.load()
    chunk_id = "tdra-cpr-v2-en:4.3"
    text = kb.chunk(chunk_id)["text_en"]

    def gate_event(quote):
        return {"action": "gate", "new_value": {"pending": False},
                "old_value": {"verb": "propose_sale", "clause_ids": [chunk_id], "quote": quote}}
    events = [gate_event(text[:40]), gate_event("words that are not in clause 4.3 at all"), gate_event(text[:10])]
    assert bakeoff.quote_failures(events, kb) == 2


def test_table_reads_each_model_folder(tmp_path):
    for model in (OPUS, SONNET):
        _copy_runs(tmp_path / model)
    table = bakeoff.build(tmp_path)
    assert [m["model"] for m in table["models"]] == [OPUS, SONNET]
    opus = table["models"][0]
    assert opus["en"]["runs"] == 5 and opus["ar"]["runs"] == 5
    assert opus["en"]["action_recall"] == 1.0 and opus["ar"]["parse_failures"] == 0
    assert opus["ar_en_agreement"] is not None
    assert opus["cost_usd"] is None  # scripted replies carry no usage: price unknown, never zero


def test_markdown_has_one_row_per_metric_and_the_decision(tmp_path):
    for model in (OPUS, SONNET, HAIKU):
        _copy_runs(tmp_path / model)
    bakeoff.write(bakeoff.build_all((("v1", tmp_path, "d7bb264"),)), tmp_path / "out")
    md = (tmp_path / "out" / "bakeoff.md").read_text(encoding="utf-8")
    for label in ("Obligation proxy", "JSON parse failures", "Quote failures", "Arabic versus English agreement",
                  "model_ms median", "Cost (USD)", "Decision"):
        assert label in md, label
    assert (tmp_path / "out" / "bakeoff.json").exists()


def _row(**overrides):
    base = {"runs": 5, "gate_rejection_rate": 0.3, "action_recall": 0.8, "citation_validity": 0.9,
            "obligation_proxy": 0.7, "gap_recall": 0.6, "abstention": 0.8, "handover_latency_steps": 0.0,
            "parse_failures": 0, "quote_failures": 0, "model_ms_median": 9000.0, "model_ms_max": 20000.0,
            "prompt_tokens": 50000, "completion_tokens": 40000, "calls": 26}
    return {**base, **overrides}


def _model(name, en=None, ar=None, agreement=0.8, cost=2.0):
    return {"model": name, "en": en or _row(), "ar": ar or _row(), "ar_en_agreement": agreement, "cost_usd": cost}


def test_decision_opus_unless_sonnet_equals_or_beats_every_row():
    opus = _model(OPUS, cost=3.0)
    assert bakeoff.decide([opus, _model(SONNET, cost=1.0)])["model"] == SONNET
    worse = _model(SONNET, ar=_row(action_recall=0.7), cost=1.0)
    decision = bakeoff.decide([opus, worse])
    assert decision["model"] == OPUS and "action_recall" in " ".join(decision["sonnet_behind"])


def test_decision_stops_when_opus_fails_json_or_quotes_in_arabic():
    decision = bakeoff.decide([_model(OPUS, ar=_row(parse_failures=2)), _model(SONNET)])
    assert decision["model"] is None and decision["stop"]
    decision = bakeoff.decide([_model(OPUS, ar=_row(quote_failures=1)), _model(SONNET)])
    assert decision["model"] is None and decision["stop"]
    decision = bakeoff.decide([_model(OPUS, en=_row(quote_failures=1)), _model(SONNET)])
    assert not decision["stop"]  # the stop rule is about Arabic


def test_filter_stops_count_replies_the_endpoint_stopped():
    """Opus 5.5 in the bake-off: empty or cut replies with finish_reason content_filter, counted apart from JSON."""
    def propose(reason):
        return {"action": "propose", "model_response": {"choices": [{"finish_reason": reason, "message": {
            "content": ""}}]}}
    assert bakeoff.filter_stops([propose("content_filter"), propose("stop"), {"action": "gate"}]) == 1


def test_v2_table_sits_beside_v1_with_the_prompt_commit_on_each(tmp_path):
    """Order 2026-10-21-task-8-part-c item 10: eval/bakeoff.md carries the v1 and v2 tables, each with the commit of
    the prompt it ran on; the v1 decision stays; v2 is shown under hq's decision, not re-decided."""
    for model in (OPUS, SONNET, HAIKU):
        _copy_runs(tmp_path / "v1" / model)
    for model in (SONNET, HAIKU):
        _copy_runs(tmp_path / "v2" / model)
    versions = (("v1", tmp_path / "v1", "d7bb264"), ("v2", tmp_path / "v2", "a85a448"))
    tables = bakeoff.build_all(versions)
    assert [t["prompt"] for t in tables] == ["v1", "v2"]
    assert [t["prompt_commit"] for t in tables] == ["d7bb264", "a85a448"]
    assert [m["model"] for m in tables[1]["models"]] == [SONNET, HAIKU]
    bakeoff.write(tables, tmp_path / "out")
    md = (tmp_path / "out" / "bakeoff.md").read_text(encoding="utf-8")
    assert "## Prompt v1, commit d7bb264" in md and "## Prompt v2, commit a85a448" in md
    assert md.index("## Prompt v1") < md.index("## Prompt v2")
    assert md.count("| Row |") == 2
    assert "claude-sonnet-5-5 is the main model (hq, order 2026-10-21-task-8-part-c, decision 1)" in md


def test_bakeoff_versions_name_the_committed_prompts():
    assert [(label, commit) for label, _, commit in bakeoff.VERSIONS] == [("v1", "d7bb264"), ("v2", "a85a448")]


def test_v2_table_carries_the_c2b_line_on_arabic_gap_ids_in_notes():
    """Order 2026-10-21-task-8-part-c2b item 3: the v2 runs are not rescored; one line under the v2 table says why
    their Arabic gap recall reads 0."""
    md = (bakeoff.ROOT / "eval" / "bakeoff.md").read_text(encoding="utf-8")
    line = "Arabic gap ids present in notes in 10 of 10 runs; scored 0 under v2 parsing; see C2b."
    assert md.count(line) == 1
    assert md.index("## Prompt v2") < md.index(line) < md.index("### Decision (v2)")
