"""Order Task 8: runs, replay, eval. Committed runs are read, never written; eval output goes to tmp_path and is
compared with the committed files."""

import json
from pathlib import Path

import pytest

from onyx import audit, data, eval as onyx_eval, model, runs

ROOT = Path(__file__).resolve().parents[1]
SCRIPTED = ROOT / "runs" / "scripted"
SCRIPTED_EVAL = ROOT / "eval" / "scripted"


def test_replay_matches_recorded_verdicts():
    log = SCRIPTED / "S2" / "run1.jsonl"
    assert audit.verify(log)
    recorded, replayed = runs.replay(log)
    assert recorded and replayed == recorded
    assert ("S2-3-care", "gate", "block") in {(e[0], e[1], e[2]) for e in recorded}


def test_replay_of_an_arabic_ungoverned_run():
    recorded, replayed = runs.replay(SCRIPTED / "ungoverned" / "S3" / "ar" / "run1.jsonl")
    assert recorded and replayed == recorded


def test_eval_is_idempotent(tmp_path):
    first, second = tmp_path / "a", tmp_path / "b"
    onyx_eval.evaluate(SCRIPTED, first)
    onyx_eval.evaluate(SCRIPTED, second)
    for name in ("results.json", "results.md"):
        assert (first / name).read_bytes() == (second / name).read_bytes()
        assert (first / name).read_bytes() == (SCRIPTED_EVAL / name).read_bytes(), f"{name} differs from committed"


def test_three_runs_per_scenario_per_mode_per_language():
    for sid in onyx_eval.SCENARIOS:
        for governed in (True, False):
            for lang in ("en", "ar"):
                paths = [runs.run_path(SCRIPTED, sid, n, lang, governed) for n in (1, 2, 3)]
                assert all(p.exists() for p in paths), paths


def test_unseen_bank_is_never_scored():
    unseen = {p.stem for p in (data.SCENARIOS_DIR / "unseen").glob("*.json")}
    assert not unseen & set(onyx_eval.SCENARIOS)
    results = json.loads((SCRIPTED_EVAL / "results.json").read_text(encoding="utf-8"))
    assert set(results["scenarios"]) == {"S1", "S2", "S3", "S4", "S5"}


def _events(path):
    return [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines()]


def test_action_recall_tells_s2_steps_3_and_4_apart_by_addressee():
    """Blind keys review: S2 steps 3 and 4 both carry draft_reply; step 4's reply is for the human."""
    events = _events(SCRIPTED / "S2" / "run1.jsonl")
    hits = onyx_eval.action_hits(events, data.load_key("S2"), data.load_scenario("S2"))
    assert hits[3] and hits[4]
    swapped = []
    for e in events:  # the step-3 reply re-addressed to the human: the verb alone would still match
        if e["action"] == "gate" and e["entity_id"] == "S2-3-care":
            e = {**e, "old_value": {**e["old_value"], "target": "Human agent H-01 (synthetic)",
                                    "args": {"recipient": "human"}}}
        swapped.append(e)
    assert not onyx_eval.action_hits(swapped, data.load_key("S2"), data.load_scenario("S2"))[3]


def test_pending_proposal_verb_is_not_counted():
    events = _events(SCRIPTED / "S3" / "run1.jsonl")
    pending = [e for e in events if e["action"] == "gate" and e["new_value"].get("pending")]
    assert [e["entity_id"] for e in pending] == ["S3-3-care"]
    without = [e for e in events if e not in pending]
    key, scenario = data.load_key("S3"), data.load_scenario("S3")
    assert onyx_eval.action_hits(without, key, scenario) == onyx_eval.action_hits(events, key, scenario)


def test_every_event_records_gate_ms_and_model_ms():
    events = _events(SCRIPTED / "S1" / "run1.jsonl")
    assert all("gate_ms" in e and "model_ms" in e for e in events)
    assert all(e["gate_ms"] is not None for e in events if e["action"] == "gate")
    assert all(e["model_ms"] is not None for e in events if e["action"] == "propose")


def test_scripted_runs_are_labelled_scripted():
    for path in SCRIPTED.rglob("run*.jsonl"):
        start = _events(path)[0]["new_value"]
        assert start["source"] == "scripted" and start["model"] == "scripted-mock", path
    assert "scripted" in (SCRIPTED_EVAL / "results.md").read_text(encoding="utf-8").splitlines()[0].lower()


def test_live_record_stops_without_a_key(tmp_path, monkeypatch):
    for name in model.ENV_NAMES:
        monkeypatch.delenv(name, raising=False)
    (tmp_path / ".env").write_text("ONYX_MODEL_BASE_URL=https://example.invalid/v1/\nONYX_MODEL=m\n"
                                   "ONYX_MODEL_API_KEY=\n", encoding="utf-8")
    with pytest.raises(model.MissingModelKey):
        runs.record("live", tmp_path / "runs", env=tmp_path / ".env")
    assert not (tmp_path / "runs").exists()


def test_openai_compatible_model_omits_temperature_by_default():
    sent = {}

    class Reply:
        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

        def read(self):
            return json.dumps({"model": "m", "choices": [{"message": {"content": "{}"}}]}).encode()

    def fake_urlopen(request, timeout):
        sent.update(json.loads(request.data))
        return Reply()

    import urllib.request
    m = model.OpenAICompatibleModel("https://example.invalid/v1/", "m", "k")
    original, urllib.request.urlopen = urllib.request.urlopen, fake_urlopen
    try:
        m.complete("r", [{"role": "user", "content": "x"}])
    finally:
        urllib.request.urlopen = original
    assert "temperature" not in sent and sent["model"] == "m" and sent["max_tokens"] > 0
