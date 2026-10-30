"""Order Task 8: runs, replay, eval. Committed runs are read, never written; eval output goes to tmp_path and is
compared with the committed files."""

import json
from pathlib import Path

import pytest

from onyx import audit, data, eval as onyx_eval, gate, model, runs

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


def test_must_cite_given_is_the_share_of_must_cite_chunks_in_the_prompt():
    """Order 2026-10-21 Part C1 item 7: diagnostic only. S2 step 3 (care, draft_reply): the scripted run gave the
    care agent CPR 26.7.2 alone, so of the step's must_cite rules only those on 26.7.2 were given."""
    events = _events(SCRIPTED / "S2" / "run1.jsonl")
    key = data.load_key("S2")
    given = onyx_eval.must_cite_given(events, key)
    step = next(s for s in key["steps"] if s["n"] == 3)
    rules = {r["id"]: f"{r['document_id']}:{r['chunk']}" for r in data.load_rules()}
    assert given[3] == round(sum(rules[r] == "tdra-cpr-v2-en:26.7.2" for r in step["must_cite"])
                             / len(step["must_cite"]), 4)
    assert given[1] is None  # step 1 is classified in plain code: no prompt
    with_mandate = [{**e, "new_value": {**e["new_value"], "sources_mandate": [rules[r] for r in step["must_cite"]]}}
                    if e["action"] == "propose" and e["entity_id"] == "S2-3-care" else e for e in events]
    assert onyx_eval.must_cite_given(with_mandate, key)[3] == 1.0


def test_must_cite_given_is_shown_not_compared(tmp_path):
    results = onyx_eval.evaluate(SCRIPTED, tmp_path)
    assert "must_cite_given" not in onyx_eval.METRICS
    row = results["scenarios"]["S2"]["governed"]["en"]
    assert set(row["must_cite_given"]) == {"min", "max"}
    assert "Must-cite given" in (tmp_path / "results.md").read_text(encoding="utf-8")


# --- Task 29 Part B (order 2026-10-29-task-29-field-take): gaps against the keys, intervals, citation failures ---

C5_RESULTS = ROOT / "eval" / "results.json"


def test_wilson_known_values():
    """95% Wilson score interval, worked by hand from the formula (z = 1.96): 110 of 112 and 54 of 56."""
    assert [round(v, 3) for v in onyx_eval.wilson(110, 112)] == [0.937, 0.995]
    assert [round(v, 3) for v in onyx_eval.wilson(54, 56)] == [0.879, 0.990]
    assert onyx_eval.wilson(56, 56)[1] == 1.0 and onyx_eval.wilson(0, 10)[0] == 0.0
    assert onyx_eval.wilson(0, 0) is None


def test_gaps_vs_keys_s1_misses_two():
    """S1 C5: the key expects three gaps; the candidate is found in every run, gap-2 and gap-6 in none."""
    table = onyx_eval.gaps_against_keys(ROOT / "runs" / "c5")
    s1 = {r["lang"]: r for r in table["rows"] if r["scenario"] == "S1"}
    for lang in ("en", "ar"):
        assert s1[lang]["runs"] == 2
        assert s1[lang]["expected"] == ["gap-2", "gap-6", "candidate-4-4-fixed-term-bundle"]
        assert s1[lang]["found_every_run"] == ["candidate-4-4-fixed-term-bundle"]
        assert s1[lang]["found_some_runs"] == {} and s1[lang]["missed"] == ["gap-2", "gap-6"]
    s2 = {r["lang"]: r for r in table["rows"] if r["scenario"] == "S2"}
    assert s2["en"]["unexpected"] == {"gap-8": 2} and s2["ar"]["unexpected"] == {"gap-8": 2, "gap-12": 2}
    assert all(r["flags_without_register_id"] == 0 for r in table["rows"])
    summary = table["summary"]
    assert (summary["expected"], summary["found_every_run"], summary["missed"], summary["unexpected"]) == (
        7, 5, ["S1 gap-2", "S1 gap-6"], 3)
    assert table["line"] == ("5 of 7 expected gaps found in every run; 2 missed (S1 gap-2, S1 gap-6); "
                               "3 unexpected register ids flagged")


def test_citation_failures_by_kind_in_c5():
    """B3, shown only: C5's one invalid citation names a chunk id that does not exist (its language ending lost)."""
    table = onyx_eval.citation_failures(ROOT / "runs" / "c5")
    assert table["failures"] == [{"run": "S2/run2.jsonl", "step": "S2-4-care", "cited": ["tdra-cpr-v2-4.3"],
                                  "kind": "id unknown"}]
    assert table["by_kind"] == {"id unknown": 1, "id in another document": 0, "quote not verbatim": 0,
                                "chunk not VERIFIED": 0}
    assert table["by_lang"] == {"en": [71, 72], "ar": [59, 59]}  # valid, citing proposals


def test_citation_failure_kinds():
    kb = gate.Knowledge.load()
    quote = "The Licensee shall maintain adequate trained personnel to receive and respond promptly to complaints"
    given = ["licence-2-2026:9.1", "tdra-cpr-v2-en:4.6"]
    elsewhere = {"clause_ids": ["tdra-cpr-v2-en:4.6"], "quote": quote}
    assert onyx_eval.citation_failure(elsewhere, kb, given) == ("id in another document", ["tdra-cpr-v2-en:4.6"])
    invented = {"clause_ids": ["licence-2-2026:9.1"], "quote": "The Licensee may answer complaints whenever it likes"}
    assert onyx_eval.citation_failure(invented, kb, given) == ("quote not verbatim", ["licence-2-2026:9.1"])
    assert onyx_eval.citation_failure({"clause_ids": ["licence-2-2026:9.1"], "quote": quote}, kb, given) is None


def test_c5_results_carry_the_three_sections():
    """The committed eval output: B1's summary line under c5.gaps_vs_keys, B2's intervals with n, B3's table; the
    README results block shows the pooled action-recall interval only, read from results.json."""
    c5 = json.loads(C5_RESULTS.read_text(encoding="utf-8"))["c5"]
    assert c5["gaps_vs_keys"]["line"] == onyx_eval.gaps_against_keys(ROOT / "runs" / "c5")["line"]
    recall = c5["intervals"]["action_recall"]
    assert (recall["pooled"]["hits"], recall["pooled"]["n"], recall["en"]["n"], recall["ar"]["n"]) == (110, 112, 56, 56)
    assert [round(v, 3) for v in recall["pooled"]["ci95"]] == [0.937, 0.995]
    validity = c5["intervals"]["citation_validity"]
    assert (validity["en"]["hits"], validity["en"]["n"], validity["ar"]["n"]) == (71, 72, 59)
    assert c5["citation_failures"]["by_kind"]["id unknown"] == 1
    md = (ROOT / "eval" / "results.md").read_text(encoding="utf-8")
    for heading in ("## Gaps against the keys (C5)", "## Citation failures by kind (C5)"):
        assert heading in md
    assert c5["gaps_vs_keys"]["line"] in md
    assert ("the interval treats key steps as independent trials; they are not (steps of one run share a "
            "conversation), so read it as a rough width, not a guarantee") in md
    lo, hi = recall["pooled"]["ci95"]
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert f"110 of 112 key steps, 95% interval {lo:.2f} to {hi:.2f}" in " ".join(readme.split())
