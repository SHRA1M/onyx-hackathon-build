import hashlib
import json

import pytest

from onyx import audit, data
from onyx.__main__ import main


def _log(tmp_path):
    log = audit.AuditLog(tmp_path / "run.jsonl", clock=lambda: "2026-10-21T12:00:00.000+00:00")
    log.start("S2")
    log.append({"actor": "care", "action": "propose", "entity_type": "step", "entity_id": "S2-3",
                "model_request_id": "req-1", "model_response": {"verb": "draft_reply", "text": "نعتذر"}})
    log.append({"actor": "gate", "action": "decide", "verdict": "block", "clause_ids": ["cpr-26-7-2"],
                "reason": "Consumer Complaint: no non-human agents (26.7.2)"})
    return log


def test_chain_verifies(tmp_path):
    log = _log(tmp_path)
    assert audit.verify(log.path)
    assert audit.first_break(log.path) is None


def test_chain_breaks_on_edit(tmp_path):
    log = _log(tmp_path)
    lines = log.path.read_bytes().split(b"\n")
    lines[1] = lines[1].replace(b"draft_reply", b"draft_replz")  # one byte, line 2 (seq 2)
    log.path.write_bytes(b"\n".join(lines))
    assert audit.verify(log.path) is False
    assert audit.first_break(log.path) == 2


def test_chain_breaks_on_a_deleted_line(tmp_path):
    log = _log(tmp_path)
    lines = log.path.read_bytes().split(b"\n")
    del lines[1]
    log.path.write_bytes(b"\n".join(lines))
    assert audit.first_break(log.path) == 2


def test_first_event_carries_key_hashes(tmp_path):
    log = _log(tmp_path)
    first = json.loads(log.path.read_text(encoding="utf-8").splitlines()[0])
    assert first["seq"] == 1 and first["action"] == "run_start" and first["entity_id"] == "S2"
    expected = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(data.KEYS_DIR.glob("S*.json"))}
    assert set(expected) == {f"S{i}.json" for i in range(1, 6)}
    assert first["new_value"]["answer_keys"] == expected


def test_every_event_has_the_order_fields(tmp_path):
    log = _log(tmp_path)
    for line in log.path.read_text(encoding="utf-8").splitlines():
        assert set(audit.FIELDS) <= set(json.loads(line))


def test_iter_model_responses_replays_verbatim(tmp_path):
    log = _log(tmp_path)
    assert list(audit.iter_model_responses(log.path)) == [("req-1", {"verb": "draft_reply", "text": "نعتذر"})]


def test_replay_refuses_a_broken_chain(tmp_path):
    log = _log(tmp_path)
    log.path.write_bytes(log.path.read_bytes().replace(b"care", b"carE", 1))
    with pytest.raises(ValueError, match="seq 2"):
        list(audit.iter_model_responses(log.path))


def test_verify_log_cli(tmp_path, capsys):
    log = _log(tmp_path)
    assert main(["verify-log", str(log.path)]) == 0
    assert capsys.readouterr().out.strip() == "chain ok"
    log.path.write_bytes(log.path.read_bytes().replace(b"block", b"allow"))
    assert main(["verify-log", str(log.path)]) == 1
    assert "first broken seq 3" in capsys.readouterr().out
