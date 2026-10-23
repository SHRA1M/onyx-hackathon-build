"""Task 13 Part A (order 2026-10-22-task-13-prompt-v5-c5): prompt v5, two care lines rewritten after the C4 misses
(S2-3, S3-4). The gate, the keys and eval.action_hits are unchanged; these tests pin what they do with the
proposals v5 asks for. Scripted model only, no model call."""

import json
from pathlib import Path

from onyx import data, eval as eval_mod, gate, kb, runs, scripted
from onyx.agents import Care
from onyx.agents.base import PROMPT_VERSION
from onyx.coordinator import Coordinator
from onyx.model import MockModel

V5_LINE_1 = (
    "Verbs: disclose_account is any act that gives account data (balance, plan, usage, invoices, personal details) to "
    "the subscriber or to any other person or body; propose_sale is offering or activating a paid product or bundle, "
    "including an outbound marketing call or message; propose_change is any change to the subscriber's service, "
    "including the warning notice before a suspension (args.change one of: notice, suspend, interrupt, disconnect, "
    "renew, upgrade, migrate, block_device); draft_reply is a message that does none of these. Sending a "
    "de-identified payload (no name, number, ID or invoice) to the model provider under the processor contract on "
    "file, in order to draft a reply, is draft_reply with args.model_provider.payload listing exactly what leaves; it "
    "is not disclose_account."
)
V5_LINE_3 = (
    "Address a draft_reply to the sender of the step's message. On a subscriber's step, target the subscriber, even "
    "inside a Consumer Complaint: cite CPR 26.7.2 and let the gate decide; its block is the hand-over, and it is "
    "recorded. On a human agent's step, target the human agent exactly as the step's facts name them (for example the "
    "value of human_actor), with args.recipient 'human'; the human sends it."
)
HUMAN = "Human agent H-01 (synthetic)"


def _run(sid, entity, proposal, tmp_path):
    """The scripted run of the scenario with one step's care reply replaced; returns that step's gate verdict and
    the run's events."""
    chunk = proposal.pop("chunk")
    document, clause = chunk.split(":", 1)
    reply = {"proposals": [{**proposal, "clause_ids": [chunk],
                            "quote": kb.get_chunk(document, clause)["text_en"][:60], "rationale": "v5 test"}]}
    script = {**scripted.model(sid).script, entity: reply}
    log = tmp_path / "run.jsonl"
    run = Coordinator(data.load_scenario(sid), MockModel(script), scripted.retriever(sid), log_path=log,
                      gaps_dir=tmp_path / "gaps")
    run.start()
    run.run()
    events = [json.loads(line) for line in log.read_text(encoding="utf-8").splitlines()]
    [verdict] = [e for e in events if e["action"] == "gate" and e["entity_id"] == entity
                 and not e["new_value"].get("pending")]
    return verdict, events


def _hit(sid, n, events):
    return eval_mod.action_hits(events, data.load_key(sid), data.load_scenario(sid))[n]


def _gates_named(verdict):
    return {r.get("gate") for r in verdict["new_value"].get("reasons", [])}


# --- S2-3: a subscriber's step inside a complaint --------------------------------------------------------------

def test_s2_3_a_draft_reply_to_the_subscriber_is_blocked_by_the_complaint_gate_and_scores_a_hit(tmp_path):
    verdict, events = _run("S2", "S2-3-care", {"verb": "draft_reply", "target": "subscriber",
                                               "args": {"language": "ar"}, "chunk": "tdra-cpr-v2-en:26.7.2"}, tmp_path)
    assert verdict["verdict"] == gate.BLOCK and "complaint_gate" in _gates_named(verdict)
    assert _hit("S2", 3, events)


def test_s2_3_the_same_draft_reply_to_the_human_scores_a_miss(tmp_path):
    """The order says held; the gate allows it, because S2 has H-01 (synthetic) on shift from the start. C4's holds
    named "Human agent H-01" or "H-xx", no human on shift. The scorer's miss is what this test pins."""
    verdict, events = _run("S2", "S2-3-care", {"verb": "draft_reply", "target": HUMAN,
                                               "args": {"recipient": "human", "language": "ar"},
                                               "chunk": "tdra-cpr-v2-en:26.7.2"}, tmp_path)
    assert verdict["verdict"] == gate.ALLOW
    assert not _hit("S2", 3, events)
    held, _ = _run("S2", "S2-3-care", {"verb": "draft_reply", "target": "Human agent H-01",
                                       "args": {"recipient": "human", "language": "ar"},
                                       "chunk": "tdra-cpr-v2-en:26.7.2"}, tmp_path / "c4-shape")
    assert held["verdict"] == gate.HOLD


# --- S2-4: the human's step ------------------------------------------------------------------------------------

def test_s2_4_a_draft_reply_to_the_named_human_passes_the_complaint_gate_and_scores_a_hit(tmp_path):
    verdict, events = _run("S2", "S2-4-care", {"verb": "draft_reply", "target": HUMAN,
                                               "args": {"recipient": "human", "language": "ar"},
                                               "chunk": "tdra-cpr-v2-en:26.7.2"}, tmp_path)
    assert verdict["verdict"] == gate.ALLOW and "complaint_gate" in _gates_named(verdict)
    assert _hit("S2", 4, events)


# --- S3-4: the de-identified model-provider payload ------------------------------------------------------------

def _s3_4(payload, tmp_path):
    return _run("S3", "S3-4-care", {"verb": "draft_reply", "target": "subscriber",
                                    "args": {"language": "en", "model_provider": {"payload": payload}},
                                    "chunk": "tdra-cpr-v2-en:24.10"}, tmp_path)


def test_s3_4_a_de_identified_payload_passes_the_model_provider_gate_and_scores_a_hit(tmp_path):
    verdict, events = _s3_4(["question_text", "plan_name"], tmp_path)
    assert verdict["verdict"] == gate.ALLOW and "model_provider_gate" in _gates_named(verdict)
    assert _hit("S3", 4, events)


def test_s3_4_the_same_payload_with_a_phone_number_is_blocked(tmp_path):
    verdict, _ = _s3_4(["question_text", "plan_name", "msisdn"], tmp_path)
    assert verdict["verdict"] == gate.BLOCK and "model_provider_gate" in _gates_named(verdict)


# --- the prompt ------------------------------------------------------------------------------------------------

def _care_system():
    seen = {}

    def respond(request_id, messages):
        seen["system"] = messages[0]["content"]
        return {"proposals": []}
    step = {"n": 2, "kind": "subscriber_message", "text_en": "What is my balance?", "facts": {}}
    Care(MockModel(respond), lambda q, d, k: []).run("S1-2-care", step)
    return seen["system"]


def test_care_prompt_carries_the_two_v5_lines_word_for_word_and_no_placeholder():
    system = _care_system()
    assert V5_LINE_1 in system and V5_LINE_3 in system
    assert "H-xx" not in system


def test_prompt_version_is_v5_on_run_start(tmp_path):
    assert PROMPT_VERSION == "v5"
    [path] = runs.record("scripted", tmp_path, scenarios=("S1",), runs=1, langs=("en",), modes=("governed",))
    start = json.loads(path.read_text(encoding="utf-8").splitlines()[0])
    assert start["new_value"]["prompt"] == "v5"


# --- Part C item 10: the C5 column in eval/results.md ---------------------------------------------------------

def test_eval_puts_c5_beside_c3_and_c4_with_misses_per_step(tmp_path):
    root = tmp_path / "runs"
    for sub in ("", "c4", "c5"):
        runs.record("scripted", root / sub, scenarios=("S1",), runs=1, langs=("en", "ar"), modes=("governed",))
    results = eval_mod.evaluate(root, tmp_path / "eval")
    assert results["c5"]["prompts"]["governed"] == ["v5"]
    md = (tmp_path / "eval" / "results.md").read_text(encoding="utf-8")
    assert "| Row | C3 en | C3 ar | C4 en | C4 ar | C5 en | C5 ar |" in md
    assert eval_mod.C5_LINE in md and eval_mod.C5_LINE.startswith("Prompt v5 changes two care lines")
    assert "| Scenario | Lang | Citation validity C3 / C4 / C5 |" in md
    assert "### Misses per step after v5 (C5)" in md and "### C5 runs" in md


# --- Part C item 11: the README's scored-run line is C5, its figures from eval/results.json -------------------

def test_readme_scored_run_is_c5_with_the_figures_eval_wrote():
    root = Path(__file__).resolve().parents[1]
    readme = (root / "README.md").read_text(encoding="utf-8")
    c5 = json.loads((root / "eval" / "results.json").read_text(encoding="utf-8"))["c5"]
    bullet = readme.split("\n- Scored run:", 1)[1].split("\n- ", 1)[0]
    line = " ".join(bullet.split())
    assert "C5" in line and "prompt v5" in line and "two runs per scenario per language" in line and "governed" in line
    fig = lambda m: " / ".join(f"{c5['C5']['all'][lang][m]:.2f}" for lang in ("en", "ar"))
    for label, metric in (("action recall", "action_recall"), ("citation validity", "citation_validity"),
                          ("obligation proxy", "obligation_proxy")):
        assert f"{label} {fig(metric)}" in line
    missed = sum(m[lang][0] for m in c5["misses"].values() for lang in ("en", "ar"))
    assert f"{missed} of {c5['key_steps']} key steps missed" in line
    assert any(x.startswith("- Ungoverned baseline: C3") for x in readme.splitlines())


# --- Part C item 12: the S2 replay page reads the first C5 run that shows the hand-over and the human's allow ---

def test_s2_replay_page_reads_the_first_c5_run_with_the_hand_over_and_step_4_allowed():
    from onyx import replay_page
    assert replay_page.source("S2") == replay_page.RUNS / "c5" / "S2" / "ar" / "run1.jsonl"
    # order 2026-10-23 Task 12 item 5: S3 to S5 read their first English C5 run; S1 stays on C3 (test_report.py)
    for sid in ("S3", "S4", "S5"):
        assert replay_page.source(sid) == replay_page.RUNS / "c5" / sid / "run1.jsonl"
    page = replay_page.render(replay_page.source("S2"))
    assert "`runs/c5/S2/ar/run1.jsonl`" in page and replay_page.C5_S2_LINE in page


# --- hq ruling on the C5 report (2026-10-22): README names each page's run; selftest heads with C5 ------------

def test_readme_names_the_run_each_replay_page_reads():
    from onyx import replay_page
    root = Path(__file__).resolve().parents[1]
    section = (root / "README.md").read_text(encoding="utf-8").split("## Scenarios", 1)[1].split("\n## ", 1)[0]
    assert "runs/S<n>/run1.jsonl" not in section
    for sid in ("S1", "S2", "S3", "S4", "S5"):
        run = replay_page.source(sid).relative_to(root).as_posix()
        assert any(row.startswith(f"| {sid} |") and f"`{run}`" in row for row in section.splitlines()), sid


def test_selftest_headline_is_c5_governed_with_c3_as_the_ungoverned_baseline():
    from onyx import selftest
    root = Path(__file__).resolve().parents[1]
    results = json.loads((root / "eval" / "results.json").read_text(encoding="utf-8"))
    lines = selftest.headline(results)
    c5 = results["c5"]["C5"]
    assert lines[0].startswith("C5 governed") and "runs/c5" in lines[0] and "prompt v5" in lines[0]
    assert f"{c5['all']['en']['runs']} / {c5['all']['ar']['runs']} runs" in lines[0]
    s2_en = next(x for x in lines if x.strip().startswith("S2 en"))
    assert f"{c5['by_scenario']['S2']['en']['action_recall']:.2f}" in s2_en
    baseline = next(x for x in lines if x.startswith("Ungoverned baseline: C3"))
    assert f"{results['scenarios']['S1']['ungoverned']['en']['ungoverned_claims_allowed']['max']}" in baseline
