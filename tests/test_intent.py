"""Order 2026-10-29-task-29 Part C3: `python -m onyx intent` writes docs/intent.json, the ML Intent: manifest ids by
Y.3172 node, the agents with their verbs and document sets, the model and prompt C5 recorded, the gate's version,
the key hashes, the four verdicts and the scenario ids. Nothing reads it at run time; byte-identical on every run."""

import json

from onyx import data, gate, intent, kb


def test_intent_idempotent(tmp_path):
    committed = (kb.REPO / "docs" / "intent.json").read_bytes()
    assert intent.write(tmp_path / "intent.json").read_bytes() == committed
    assert intent.write(tmp_path / "intent.json").read_bytes() == committed


def test_intent_first_key_says_nothing_reads_it():
    doc = intent.build()
    assert next(iter(doc)) == "note" and "run time" in doc["note"]


def test_intent_reads_the_committed_sources():
    doc = intent.build()
    assert sorted(i for ids in doc["manifest_by_node"].values() for i in ids) == sorted(kb.manifest_by_id())
    mandates = json.loads((kb.REPO / "onyx" / "data" / "mandates.json").read_text(encoding="utf-8"))["agents"]
    assert doc["agents"] == {a: {"verbs": m["verbs"], "documents": m["documents"]} for a, m in mandates.items()}
    assert doc["c5"] == {"model": "claude-sonnet-5-5", "prompt": "v5"}
    assert doc["verdicts"] == [gate.ALLOW, gate.HOLD, gate.BLOCK, gate.INSUFFICIENT]
    hashes = (kb.REPO / "onyx" / "data" / "keys" / "HASHES.txt").read_text(encoding="utf-8").split()
    assert doc["key_hashes"] == dict(zip(hashes[1::2], hashes[0::2]))
    assert doc["scenarios"] == ["S1", "S2", "S3", "S4", "S5"]
    assert doc["gate"]["sha256"] == kb.sha256_file(kb.REPO / "onyx" / "gate.py")


def test_readme_mlfo_row_names_the_intent():
    readme = (kb.REPO / "README.md").read_text(encoding="utf-8")
    row = next(l for l in readme.splitlines() if l.startswith("| MLFO |"))
    assert "ML Intent: `docs/intent.json`" in row
