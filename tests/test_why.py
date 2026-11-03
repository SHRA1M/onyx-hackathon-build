"""Task 36 item 2 (order 2026-11-01-task-36-template-items): `python -m onyx why <log> --step <n>` explains a recorded
step from the log alone: verdict, clause, document, page, verbatim quote from kb/chunks/, the human handed to, the
event hash. No model call."""

import pytest

from onyx import kb, runs, why
from onyx.__main__ import main

S2 = kb.REPO / "runs" / "c5" / "S2" / "run1.jsonl"
S3 = kb.REPO / "runs" / "c5" / "S3" / "run1.jsonl"
CPR_26_7_2_EN = "preclude the use of non-human agents by Licensees in conversations with Consumers regarding Consumer Complaints"
CPR_26_7_2_AR = "يستثنى أو يستبعد منها استخدام وكلاء غير بشريين"


def _hashes(path, entity):
    return [e["hash"] for e in runs._events(path) if e["entity_id"] == entity and e["action"] in runs.DECISIONS]


def test_s3_step_3_prints_block_pdpl_22_and_23_2_and_the_refused_override(capsys):
    assert main(["why", str(S3), "--step", "3"]) == 0
    out = capsys.readouterr().out
    assert "S3-3-care" in out and "block" in out
    assert "PDPL 22" in out and "PDPL 23(2)" in out
    assert "Personal Data may be transferred to outside of the State in the following cases approved by the Bureau" in out
    assert "override_refused" in out and "Human agent H-02 (synthetic)" in out
    assert "p. 25" in out and "Federal Decree-Law No. 45 of 2021" in out
    for h in _hashes(S3, "S3-3-care"):
        assert h in out


def test_s3_step_3_in_arabic_says_when_the_chunk_has_no_arabic(capsys):
    assert main(["why", str(S3), "--step", "3", "--lang", "ar"]) == 0
    out = capsys.readouterr().out
    assert "منع" in out and "PDPL 22" in out and "override_refused" in out
    assert why.NO_AR in out  # the PDPL chunks carry English only; the English quote follows, marked


@pytest.mark.parametrize("lang,quote", [("en", CPR_26_7_2_EN), ("ar", CPR_26_7_2_AR)])
def test_s2_step_3_hands_over_with_cpr_26_7_2_in_both_languages(capsys, lang, quote):
    assert main(["why", str(S2), "--step", "3", "--lang", lang]) == 0
    out = capsys.readouterr().out
    assert "CPR 26.7.2" in out and quote in out and "p. 65" in out
    assert "hand the conversation to a named human (26.7.2; licence 9.1)" in out
    assert ("hand-over" if lang == "en" else "تسليم") in out


def test_a_step_with_no_gate_event_errors_cleanly(capsys):
    assert main(["why", str(S3), "--step", "9"]) == 2
    captured = capsys.readouterr()
    assert "S3-9" in captured.err and "no gate event" in captured.err and "Traceback" not in captured.err


def test_why_never_calls_a_model(monkeypatch):
    from onyx import model
    for name in ("OpenAICompatibleModel", "RecordedModel", "MockModel"):
        if hasattr(model, name):
            monkeypatch.setattr(model, name, None)
    lines = why.explain(S3, 3)
    assert any("block" in line for line in lines)


def test_a_broken_chain_is_not_explained(tmp_path):
    raw = S3.read_text(encoding="utf-8").replace("H-02", "H-99", 1)
    bad = tmp_path / "run1.jsonl"
    bad.write_text(raw, encoding="utf-8", newline="\n")
    with pytest.raises(ValueError, match="chain broken"):
        why.explain(bad, 3)
