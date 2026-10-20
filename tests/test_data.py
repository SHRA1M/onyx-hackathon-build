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

# No checkable text on disk yet: the Arabic-only PDF's text layer is garbled (open question to Iyas, 2026-10-20).
PENDING = {"Decision 16/2026 4.17", "Decision 16/2026 4.18", "Decision 16/2026 4.19"}


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


def test_keys_hashed():
    hashes = data.KEYS_DIR / "HASHES.txt"
    if not hashes.exists():
        pytest.skip("answer keys not written yet (Fable session with Iyas, target 2026-10-23)")
    for line in hashes.read_text(encoding="utf-8").splitlines():
        digest, name = line.split(maxsplit=1)
        assert hashlib.sha256((data.KEYS_DIR / name).read_bytes()).hexdigest() == digest, name


def test_check_data_passes(capsys):
    assert data.check_data() == 0, capsys.readouterr().out
