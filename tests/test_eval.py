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


# --- Task 39 B (order 2026-11-02-task-39-pre-freeze; ruling task-39-stops-ruling-2026-11-02) ----------------------

def test_key_clauses_shown_counts_mandate_and_retrieval_apart():
    """A must_cite entry is shown when its chunk is in a propose event of the step (any agent): by mandate when in
    sources_mandate, only by retrieval when in sources_used and not sources_mandate. Steps with no propose event
    are outside the total; each entry counts once, so two rules on one chunk count twice."""
    rules = {r["id"]: f"{r['document_id']}:{r['chunk']}" for r in data.load_rules()}
    key = {"scenario": "SX", "steps": [{"n": 1, "agent": "care", "must_cite": ["cpr-26-7-2"]},
                                       {"n": 2, "agent": "care", "must_cite": ["cpr-26-7-2", "licence-9-1", "cpr-4-6"]},
                                       {"n": 3, "agent": "adviser", "must_cite": ["pdpl-13-2-d", "pdpl-13-2-g"]}]}
    assert rules["pdpl-13-2-d"] == rules["pdpl-13-2-g"]

    def propose(entity, mandate, used):
        return {"action": "propose", "entity_id": entity,
                "new_value": {"sources_mandate": mandate, "sources_used": used}}
    events = [propose("SX-2-care", [rules["cpr-26-7-2"]], [rules["cpr-26-7-2"], rules["licence-9-1"]]),
              propose("SX-3-adviser", [], []), propose("SX-3-tdra", [], [rules["pdpl-13-2-d"]])]
    assert onyx_eval.key_clauses_shown(events, key) == {"shown": 4, "total": 5, "mandate": 1, "retrieval": 3}


def test_key_clauses_shown_c5_totals_are_pinned():
    """234 must-cite entries per language over the C5 runs (S1-1 and S2-1 send no prompt and are outside); a key
    change shows up here. The figures equal the probe of 2026-11-02 (report-back, stop 1)."""
    c5 = json.loads(C5_RESULTS.read_text(encoding="utf-8"))["c5"]["key_clauses"]
    assert c5["pooled"] == {"en": {"shown": 186, "total": 234, "mandate": 160, "retrieval": 26, "absent": 43,
                                   "carried": 23},
                            "ar": {"shown": 166, "total": 234, "mandate": 160, "retrieval": 6, "absent": 68,
                                   "carried": 36}}
    for lang in ("en", "ar"):
        cells = [c5["by_scenario"][sid][lang] for sid in onyx_eval.SCENARIOS]
        assert {k: sum(c[k] for c in cells) for k in onyx_eval.KEY_CLAUSES} == c5["pooled"][lang]
        assert all(c["shown"] == c["mandate"] + c["retrieval"] for c in cells)


def test_key_clauses_row_is_recomputed_from_the_committed_logs():
    """Deterministic over the committed C5 logs: recomputed per run, summed per cell, equal to results.json, and the
    printed row and pooled line in results.md carry those numbers."""
    committed = json.loads(C5_RESULTS.read_text(encoding="utf-8"))["c5"]["key_clauses"]
    md = (ROOT / "eval" / "results.md").read_text(encoding="utf-8")
    for sid in onyx_eval.SCENARIOS:
        key = data.load_key(sid)
        for lang in ("en", "ar"):
            paths = [p for n in range(1, runs.RUNS + 1)
                     if (p := runs.run_path(ROOT / "runs" / "c5", sid, n, lang)).exists()]
            per_run = [onyx_eval.key_clauses_cell(_events(p), key, data.load_scenario(sid)) for p in paths]
            cell = {k: sum(r[k] for r in per_run) for k in onyx_eval.KEY_CLAUSES}
            assert cell == committed["by_scenario"][sid][lang]
            assert onyx_eval.key_clauses_cells(cell) in md
    for lang in ("en", "ar"):
        assert onyx_eval.key_clauses_pooled(lang, committed["pooled"][lang]) in md
    assert "- key clauses shown (C5, shown only, never compared):" in md


def test_c5_handover_latency_cells_equal_the_json_values():
    """Ruling D4: results.md prints the C5 hand-over latency per scenario and language from the values in
    results.json (n/a where the key has no hand-over step), never the C3 Governed column."""
    c5 = json.loads(C5_RESULTS.read_text(encoding="utf-8"))["c5"]["C5"]["by_scenario"]
    md = (ROOT / "eval" / "results.md").read_text(encoding="utf-8")
    section = md.split("## Key clauses shown and hand-over latency (C5)", 1)[1].split("\n## ", 1)[0]
    rows = {tuple(c.strip() for c in line.strip("|").split("|")[:2]): line.strip("|").split("|")[-1].strip()
            for line in section.splitlines() if line.startswith("| S")}
    expected = {"S1": "n/a", "S2": "0", "S3": "n/a", "S4": "0", "S5": "0"}
    for sid in onyx_eval.SCENARIOS:
        for lang in ("en", "ar"):
            value = c5[sid][lang]["handover_latency_steps"]
            assert rows[(sid, lang)] == onyx_eval._steps(value) == expected[sid]


def test_key_clauses_absent_and_carried_by_the_gate():
    """Ruling 2 (task-39-stops-ruling-2-2026-11-02, B5): a must_cite entry not shown at a step whose action hit is
    absent; it is carried when the step's gate record holds it: a rule id in a gate event's reasons (clause), or its
    chunk among the clause_ids of the proposal the gate judged (old_value)."""
    rules = {r["id"]: f"{r['document_id']}:{r['chunk']}" for r in data.load_rules()}
    key = {"scenario": "SX", "steps": [{"n": 2, "agent": "care", "must_cite": ["cpr-26-7-2", "licence-9-1", "cpr-4-6"]},
                                       {"n": 3, "agent": "care", "must_cite": ["cpr-22-2"]}]}
    events = [{"action": "propose", "entity_id": "SX-2-care", "new_value": {"sources_mandate": [], "sources_used": []}},
              {"action": "propose", "entity_id": "SX-3-care", "new_value": {"sources_mandate": [], "sources_used": []}},
              {"action": "gate", "entity_id": "SX-2-care", "old_value": {"clause_ids": [rules["licence-9-1"]]},
               "new_value": {"reasons": [{"clause": "cpr-26-7-2"}, {"source": "imda", "clause": "2.2.2"}]}}]
    absent = onyx_eval.key_clauses_absent(events, key, {2: True, 3: False})
    assert absent == [(2, "cpr-26-7-2", True), (2, "licence-9-1", True), (2, "cpr-4-6", False)]


def test_uncarried_key_clauses_sit_on_abstention_steps_but_two_at_s3_1_arabic():
    """Ruling 2, B5: over the committed C5 logs every absent entry the gate does not carry is on a step with an
    abstain event, except cpr-28-26 and consumer-law-4-5 at S3-1 in Arabic, which the English runs retrieved
    (sources_used, not the mandate list). The Annex A sentence says this."""
    exceptions, english = set(), {}
    for sid in onyx_eval.SCENARIOS:
        key, scenario = data.load_key(sid), data.load_scenario(sid)
        for lang in ("en", "ar"):
            for n in range(1, runs.RUNS + 1):
                path = runs.run_path(ROOT / "runs" / "c5", sid, n, lang)
                if not path.exists():
                    continue
                events = _events(path)
                abstained = {int(e["entity_id"].split("-")[1]) for e in events if e["action"] == "abstain"}
                hits = onyx_eval.action_hits(events, key, scenario)
                exceptions |= {(sid, step, rule, lang) for step, rule, carried in
                               onyx_eval.key_clauses_absent(events, key, hits)
                               if not carried and step not in abstained}
                if (sid, lang) == ("S3", "en"):
                    english[n] = [e["new_value"] for e in events
                                  if e["action"] == "propose" and e["entity_id"].startswith("S3-1-")]
    assert exceptions == {("S3", 1, "cpr-28-26", "ar"), ("S3", 1, "consumer-law-4-5", "ar")}
    rules = {r["id"]: f"{r['document_id']}:{r['chunk']}" for r in data.load_rules()}
    assert english
    for proposes in english.values():
        for rule in ("cpr-28-26", "consumer-law-4-5"):
            assert any(rules[rule] in p["sources_used"] for p in proposes)
            assert not any(rules[rule] in p.get("sources_mandate", []) for p in proposes)
