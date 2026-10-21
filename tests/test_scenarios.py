"""Order Task 7: scenarios and the coordinator (staged release, live inject, Arabic runs). Runs use the scripted
MockModel and retriever (onyx/scripted.py): no model call, no network."""

import json

import pytest

from onyx import coordinator, data, scripted

SCENARIOS = ["S1", "S2", "S3", "S4", "S5"]
SUBSCRIBER_FIELDS = ("subscriber", "account", "catalogue")


def _run(tmp_path, sid, lang="en", governed=True, until=None):
    run = coordinator.Coordinator(
        data.load_scenario(sid), scripted.model(sid, lang), scripted.retriever(sid),
        log_path=tmp_path / f"{sid}-{lang}.jsonl", gaps_dir=tmp_path / "gaps", lang=lang, governed=governed)
    run.start()
    results = run.run(until=until)
    return run, results


def _events(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def _subscriber_values(scenario):
    values = []
    for name in SUBSCRIBER_FIELDS:
        block = scenario.get(name, {})
        values += [str(v) for v in (block.values() if isinstance(block, dict) else []) if isinstance(v, str)]
    return values


def test_staged_release(tmp_path):
    scenario = data.load_scenario("S1")
    run, _ = _run(tmp_path, "S1", until=2)
    seen = json.dumps([r.to_dict() for r in run.inboxes["tdra"]], ensure_ascii=False)
    assert run.inboxes["tdra"] == []
    for value in _subscriber_values(scenario) + [scenario["steps"][0]["text_en"]]:
        assert value not in seen
    care = json.dumps([r.to_dict() for r in run.inboxes["care"]], ensure_ascii=False)
    assert scenario["subscriber"]["msisdn"] in care  # the care agent serves the subscriber
    assert "S1-1" not in {r.inject for r in run.inboxes["care"]}  # step 1 went to the adviser only
    released = [e for e in _events(run.log.path) if e["action"] == "release_event"]
    assert [(e["entity_id"], e["new_value"]["to"]) for e in released] == [("S1-1", "adviser"), ("S1-2", "care")]


@pytest.mark.parametrize("sid", SCENARIOS)
def test_tdra_never_receives_subscriber_data(tmp_path, sid):
    scenario = data.load_scenario(sid)
    run, _ = _run(tmp_path, sid)
    seen = json.dumps([r.to_dict() for r in run.inboxes["tdra"]], ensure_ascii=False)
    for name in SUBSCRIBER_FIELDS:
        assert f'"{name}"' not in seen
    for step in scenario["steps"]:
        if step["to"] != "tdra":
            assert step["text_en"] not in seen


def test_live_inject_with_no_rule_flags_gap(tmp_path):
    run, _ = _run(tmp_path, "S2")
    text = "May the chatbot use the subscriber's voice to clone a greeting for her voicemail?"
    result = run.inject(text)
    assert result.inject == "S2-7" and result.agent == "adviser"
    assert result.answer == "INSUFFICIENT_EVIDENCE"
    [row] = [json.loads(line) for line in (tmp_path / "gaps" / "candidates.jsonl").read_text(encoding="utf-8").splitlines()]
    assert row["scenario"] == "S2" and row["inject"] == "S2-7" and row["text"] == text
    assert row["status"] == "candidate" and row["clauses_searched"]
    events = _events(run.log.path)
    [abstain] = [e for e in events if e["action"] == "abstain"
                 and e["entity_id"] == "S2-7"]
    assert abstain["verdict"] == "insufficient_evidence" and abstain["actor"] == "adviser"
    assert row["log_hash"] == abstain["hash"]
    assert [e for e in events if e["action"] == "release_event"][-1]["new_value"]["kind"] == "inject"


@pytest.mark.parametrize("sid", SCENARIOS)
def test_arabic_run_cites_same_clause_ids_as_english(tmp_path, sid):
    def cited(lang):
        run, _ = _run(tmp_path, sid, lang=lang)
        return [(e["entity_id"], e["action"], e["verdict"], e["clause_ids"]) for e in _events(run.log.path)
                if e["action"] in {"gate", "abstain"}]
    english, arabic = cited("en"), cited("ar")
    assert english and arabic == english
    # The Arabic run reads Arabic: every Arabic step text is what the agent received.
    run, _ = _run(tmp_path, sid, lang="ar")
    for agent, inbox in run.inboxes.items():
        for release in inbox:
            if release.kind != "classification":
                assert release.text == data.load_scenario(sid)["steps"][release.n - 1]["text_ar"]


def test_arabic_quotes_come_from_arabic_text(tmp_path):
    run, _ = _run(tmp_path, "S2", lang="ar")
    [gate_event] = [e for e in _events(run.log.path) if e["action"] == "gate" and e["entity_id"] == "S2-3-care"]
    assert any("؀" <= ch <= "ۿ" for ch in gate_event["quote"])


def test_adviser_lists_clauses_searched_on_s4_step_5(tmp_path):
    run, results = _run(tmp_path, "S4")
    step5 = results[-1]
    assert step5.answer == "INSUFFICIENT_EVIDENCE"
    must = set(data.load_key("S4")["steps"][4]["must_cite"])
    assert must <= set(step5.searched_ids)
    [abstain] = [e for e in _events(run.log.path) if e["action"] == "abstain"]
    rules = {r["id"]: r for r in data.load_rules()}
    for row in abstain["new_value"]["searched"]:
        assert row["says"] == rules[row["rule"]]["quote"]
    assert abstain["new_value"]["gaps"] == ["gap-4"]


@pytest.mark.parametrize("sid", SCENARIOS)
def test_scripted_governed_run_reaches_each_key_verdict(tmp_path, sid):
    """Each step's gate verdict on the scripted proposal equals the frozen key; the abstention step answers
    INSUFFICIENT_EVIDENCE. Scripts stand in for the model: this tests the coordinator, not a model."""
    _, results = _run(tmp_path, sid)
    key = data.load_key(sid)
    for result, step in zip(results, key["steps"]):
        if step.get("abstain"):
            assert result.answer == "INSUFFICIENT_EVIDENCE", (sid, step["n"])
            continue
        verdicts = [v.verdict for _, v in result.verdicts]
        assert verdicts == [step["verdict"]], (sid, step["n"], verdicts)


@pytest.mark.parametrize("sid", SCENARIOS)
def test_ungoverned_run_allows_everything(tmp_path, sid):
    _, results = _run(tmp_path, sid, governed=False)
    assert all(v.verdict == "allow" and v.clause_ids == [] for r in results for _, v in r.verdicts)


def test_run_log_chains_and_carries_key_hashes(tmp_path):
    from onyx import audit
    run, _ = _run(tmp_path, "S3")
    assert audit.verify(run.log.path)
    first = _events(run.log.path)[0]
    assert first["action"] == "run_start" and first["new_value"]["answer_keys"]


def test_unseen_bank_is_out_of_the_demo_set():
    assert not set(scripted.SCRIPTS) & {p.stem for p in (data.SCENARIOS_DIR / "unseen").glob("*.json")}
    for path in (data.SCENARIOS_DIR / "unseen").glob("*.json"):
        scenario = json.loads(path.read_text(encoding="utf-8"))
        assert scenario["synthetic"] is True and scenario["steps"]
        assert not (data.KEYS_DIR / path.name).exists()
        for step in scenario["steps"]:
            assert step["text_en"] and step["text_ar"]


def test_cli_run_with_inject(tmp_path, capsys):
    from onyx.__main__ import main
    out = tmp_path / "S2.jsonl"
    code = main(["run", "S2", "--inject", "Can the chatbot bill a late-night data top-up?", "--out", str(out),
                 "--gaps", str(tmp_path / "gaps")])
    printed = capsys.readouterr().out
    assert code == 0 and "SYNTHETIC" in printed and "S2-7" in printed and "chain ok" in printed
    assert (tmp_path / "gaps" / "candidates.jsonl").exists()
