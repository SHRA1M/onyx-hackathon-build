"""hq decision on the C3 stop (order 2026-10-21-task-8-part-c3-citation-rule): citation validity counts only
proposals that cite a clause; a flag_gap that cites nothing is left out of it and counted in "Gap flags without a
clause" (shown only). The bake-off tables keep the definition they were scored on."""

import json

from onyx import data, eval as eval_mod, gate, scripted
from onyx.coordinator import Coordinator
from onyx.model import MockModel

BARE_GAP = {"proposals": [{"verb": "flag_gap", "target": "gap-3", "args": {"gap": "gap-3"}}],
            "notes": ["<INSUFFICIENT_EVIDENCE>"]}


def _metrics(tmp_path, replies, lang="ar"):
    script = {**scripted.model("S5", lang).script, **replies}
    log = tmp_path / "run1.jsonl"
    run = Coordinator(data.load_scenario("S5"), MockModel(script, model="scripted-mock"), scripted.retriever("S5"),
                      log_path=log, gaps_dir=tmp_path / "gaps", lang=lang)
    run.start(source="scripted", model="scripted-mock", run=1, retrieval="scripted")
    run.run()
    return eval_mod.run_metrics(log, data.load_key("S5"), data.load_scenario("S5"), gate.Knowledge.load(),
                                eval_mod._rules_by_chunk())


def test_a_flag_gap_citing_nothing_is_left_out_of_citation_validity_and_counted_apart(tmp_path):
    m = _metrics(tmp_path, {"S5-4-adviser": BARE_GAP})
    assert m["citation_validity"] == 1.0
    assert m["citation_validity_all"] < 1.0
    assert m["gap_flags_without_clause"] == 1


def test_another_verb_citing_nothing_still_counts_as_invalid(tmp_path):
    bare_reply = {"proposals": [{"verb": "draft_reply", "target": "subscriber", "args": {}}], "notes": []}
    m = _metrics(tmp_path, {"S5-3-care": bare_reply})
    assert m["citation_validity"] < 1.0
    assert m["gap_flags_without_clause"] == 0


def test_live_results_show_citation_validity_both_ways_for_s1_to_s3_with_hqs_line(tmp_path):
    results = {"scripted": False, "scenarios": {sid: {mode: {lang: {"citation_validity": {"min": 1.0, "max": 1.0},
                                                                    "citation_validity_all": {"min": 0.8, "max": 0.9}}
                                                             for lang in ("en", "ar")}
                                                      for mode in ("governed", "ungoverned")}
                                                for sid in ("S1", "S2", "S3", "S4", "S5")}}
    lines = eval_mod._both_ways(results)
    text = "\n".join(lines)
    assert "Rule set by hq on 2026-10-21 after S3, before the remaining runs." in text
    assert "| S1 | governed | ar | 1.00 | 0.80 to 0.90 |" in text
    assert "| S4 |" not in text
    assert eval_mod._both_ways({**results, "scripted": True}) == []
