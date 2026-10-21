import hashlib

import pytest

from onyx import data, kb

# Order Task 3: the agents and verbs of mandates.json.
ORDER_MANDATES = {
    "care": {"propose_sale", "propose_change", "disclose_account", "draft_reply"},
    "adviser": {"classify_channel", "cite", "flag_gap"},
    "tdra": {"raise_dispute", "order_restore", "request_report"},
    "data_office": {"receive_objection", "receive_dpia", "request_human_review"},
    "coordinator": {"release_event", "route", "escalate_to_human"},
}

# Order Task 3: the rules.json clause list, as citation labels.
ORDER_RULES = (
    "CPR 4.3|CPR 4.4|CPR 4.6|CPR 4.7.1|CPR 4.7.2|CPR 4.7.3|CPR 4.10|CPR 4.11|CPR 4.17.3|CPR 4.22.1|CPR 4.22.2|CPR 4.22.3|"
    "CPR 4.23.3|CPR 5.4.1|CPR 9.4.2|CPR 13.6|CPR 16.9.2|CPR 17.2|CPR 22.1.1|CPR 22.1.2|CPR 22.2|CPR 22.3|CPR 22.4|CPR 22.5|"
    "CPR 24.5|CPR 24.6|CPR 24.6 fn 35|CPR 24.7|CPR 24.9|CPR 24.10|CPR 26.6|CPR 26.7.1|CPR 26.7.2|CPR 26.13.2|CPR 26.13.3|"
    "CPR 26.14.2|CPR 26.16.1|CPR 3.2.2|CPR 3.3|CPR 3.9|CPR 28.11|CPR 28.25|CPR 28.26|"
    "Licence 9.1|Licence 9.2.4|Licence 9.4.3|Licence 3.4.1|"
    "PDPL 6(1)(b)|PDPL 7(5)|PDPL 8(1)|PDPL 13(2)(d)|PDPL 13(2)(g)|PDPL 17|PDPL 18(1)|PDPL 18(2)|PDPL 18(4)|PDPL 21(2)(a)|"
    "PDPL 22|PDPL 23(1)(a)|"
    "ET 10|ET 11(2)|ET 12(2)(b)|ET 28(1)|ET 33|"
    "Consumer Law 4(5)|Consumer Law 8(4)|Consumer Law 29|"
    "Cabinet 66/2023 34(1)|Cabinet 66/2023 34(3)|Cabinet 66/2023 34(5)|"
    "Cabinet 56/2024 4|Cabinet 56/2024 5(6)|Cabinet 56/2024 5(7)|"
    "Spam Calls v4 3.3(iii)|Spam Calls v4 9.5|Spam Calls v4 10.2|Spam Calls v4 14.3|Spam Calls v4 15.4|"
    "Child Digital Safety 7(1)|Child Digital Safety 11(1)(b)|"
    "Decision 16/2026 4.17|Decision 16/2026 4.18|Decision 16/2026 4.19|"
    "QoS v3.0 T1(2a)|Cybercrimes 48"
).split("|")

# 4.17 and 4.18 come from the hq checked file (kb/extracts/); 4.19 has no checked text yet (Iyas, 2026-10-20).
PENDING = {"Decision 16/2026 4.19"}


def test_every_rule_quote_is_verbatim():
    problems = data.check_rules()
    assert not problems, "\n".join(problems)


def test_every_rule_has_a_clause_id_and_a_binding_flag():
    for rule in data.load_rules():
        assert rule["clause"] and rule["chunk"], rule["id"]
        assert rule["binding_status"] in {"binding", "advisory", "method"}, rule["id"]
        assert rule["jurisdiction"] in {"UAE", "foreign", "international"}, rule["id"]


def test_rules_cover_the_order_list():
    labels = {rule["label"] for rule in data.load_rules()}
    missing = [label for label in ORDER_RULES if label not in labels and label not in PENDING]
    assert not missing, missing


def test_every_mandate_verb_cites_a_clause():
    problems = data.check_mandates()
    assert not problems, "\n".join(problems)


def test_mandates_hold_the_order_verbs():
    mandates = data.load_mandates()
    assert {agent: {v["verb"] for v in spec["verbs"]} for agent, spec in mandates.items()} == ORDER_MANDATES


# Iyas, 2026-10-21: a quote read from page images or scanned text is valid only if hq holds a "-checked.txt"
# for it. Every such rule, and the ones still pending.
TRANSCRIBED = {"d16-4-17", "d16-4-18", "licence-9-1"}
PENDING_CHECK: set[str] = set()  # licence-9-1 checked by Iyas, 2026-10-21


def test_transcribed_rules_are_listed_and_pending_marked():
    rules = {r["id"]: r for r in data.load_rules()}
    assert {rid for rid, r in rules.items() if r.get("transcription")} == TRANSCRIBED
    assert {r["id"] for r in data.pending_rules()} == PENDING_CHECK
    for rid in TRANSCRIBED:
        t = rules[rid]["transcription"]
        assert t["from"] and t["field"] in rules[rid], rid
        assert t["checked_file"].endswith("-checked.txt") or rid in PENDING_CHECK, rid


def test_a_checked_file_must_be_what_the_kb_holds(monkeypatch):
    # A quote checked against a file made from the same note does not count: the KB text must come from the
    # checked file itself, so the extract header names it.
    rule = next(r for r in data.load_rules() if r["id"] == "d16-4-17")
    other = {**rule, "transcription": {**rule["transcription"], "checked_file": "other-checked.txt"}}
    monkeypatch.setattr(data, "load_rules", lambda: [other])
    assert any("checked file" in p for p in data.check_rules())
    unchecked = {**rule, "transcription": {**rule["transcription"], "checked_file": ""}}
    monkeypatch.setattr(data, "load_rules", lambda: [unchecked])
    assert not data.check_rules()
    assert [r["id"] for r in data.pending_rules()] == ["d16-4-17"]


def test_d16_4_18_covers_both_two_hour_limits():
    rule = next(r for r in data.load_rules() if r["id"] == "d16-4-18")
    assert "خلال فترة لا تتجاوز ساعتين من وقت استلام البلاغ" in rule["quote"]
    assert "ويتعين على المرخص له الآخر تنفيذ الحجب خلال ساعتين من وقت استلام الإخطار" in rule["quote"]
    assert "other licensee" in rule["unit"]


def test_licence_9_1_arabic_is_the_checked_fragment():
    rule = next(r for r in data.load_rules() if r["id"] == "licence-9-1")
    assert rule["quote_ar"] == "توفير ما يلزم من موظفين مدربين"
    assert rule["transcription"]["field"] == "quote_ar"
    assert rule["transcription"]["checked_file"] == "licence-2-2026-ar-9.1-checked.txt"


def test_no_arabic_chunk_has_a_reversed_lam_alef():
    # TDRA text layers write 'علاقات' as 'عالقات' and 'الإنجليزية' as 'اإلنجليزية' (Iyas, 2026-10-21).
    problems = data.ligature_problems()
    assert not problems, f"{len(problems)} chunks:\n" + "\n".join(problems)


def test_keys_hashed():
    hashes = data.KEYS_DIR / "HASHES.txt"
    if not hashes.exists():
        pytest.skip("answer keys not written yet (Fable session with Iyas, target 2026-10-23)")
    for line in hashes.read_text(encoding="utf-8").splitlines():
        digest, name = line.split(maxsplit=1)
        assert hashlib.sha256((data.KEYS_DIR / name).read_bytes()).hexdigest() == digest, name


def test_check_data_passes(capsys):
    assert data.check_data() == 0, capsys.readouterr().out


# Order Task 3 (keys session, Fable, 2026-10-21): scenarios S1 to S5 and their frozen answer keys.
SCENARIOS = ["S1", "S2", "S3", "S4", "S5"]
VERDICTS = {"allow", "hold", "block", "insufficient_evidence"}


def test_every_scenario_has_steps_in_both_languages():
    mandates = data.load_mandates()
    for sid in SCENARIOS:
        scenario = data.load_scenario(sid)
        assert scenario["id"] == sid and scenario["synthetic"] is True, sid
        assert scenario["steps"], sid
        for i, step in enumerate(scenario["steps"], start=1):
            assert step["n"] == i, f"{sid} step {i}"
            assert step["to"] in mandates, f"{sid} step {i}: agent {step['to']}"
            assert step["text_en"].strip() and step["text_ar"].strip(), f"{sid} step {i}: both languages"


def test_every_key_matches_its_scenario_and_cites_rules():
    rules = {r["id"] for r in data.load_rules()}
    mandates = data.load_mandates()
    for sid in SCENARIOS:
        scenario, key = data.load_scenario(sid), data.load_key(sid)
        assert key["scenario"] == sid
        assert [s["n"] for s in key["steps"]] == [s["n"] for s in scenario["steps"]], sid
        abstain = [s["n"] for s in key["steps"] if s.get("abstain")]
        assert len(abstain) == 1, f"{sid}: exactly one INSUFFICIENT_EVIDENCE step, got {abstain}"
        assert key["abstain_step"] == abstain[0], sid
        for step, sstep in zip(key["steps"], scenario["steps"]):
            label = f"{sid} step {step['n']}"
            assert step["verdict"] in VERDICTS, label
            assert step["must_cite"], f"{label}: a key step names the clauses it rests on"
            missing = [c for c in step["must_cite"] if c not in rules]
            assert not missing, f"{label}: must_cite not in rules.json: {missing}"
            if step.get("abstain"):
                assert step["verdict"] in {"insufficient_evidence", "hold"}, label
            if step.get("verb"):
                assert step["verb"] in {v["verb"] for v in mandates[sstep["to"]]["verbs"]}, f"{label}: {step['verb']}"
        assert key["handover_step"] is None or key["handover_step"] in [s["n"] for s in key["steps"]], sid
        assert key["ungoverned_claims"], f"{sid}: the ungoverned baseline names what the gate rejects"


def test_keys_file_set_is_frozen():
    hashes = data.KEYS_DIR / "HASHES.txt"
    assert hashes.exists(), "answer keys must be hashed before the first live run (order Task 3)"
    names = {line.split(maxsplit=1)[1] for line in hashes.read_text(encoding="utf-8").splitlines()}
    assert names == {f"{sid}.json" for sid in SCENARIOS}, names
