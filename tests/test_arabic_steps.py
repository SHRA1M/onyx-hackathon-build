"""Order 2026-10-27-task-28-arabic-steps: Iyas's Arabic step text on S1 to S5, and replay of the runs recorded on
the old text (Iyas, 2026-10-27: replay uses the step text the log recorded)."""

import json
from pathlib import Path

from onyx import data, runs

ROOT = Path(__file__).resolve().parents[1]
OLD_ARABIC_LOG = ROOT / "runs" / "c4" / "S1" / "ar" / "run1.jsonl"  # C4, recorded on the text before Task 28


def _sent(log: Path) -> dict[int, str]:
    events = [json.loads(line) for line in log.read_text(encoding="utf-8").splitlines()]
    return {e["new_value"]["n"]: e["new_value"]["text"] for e in events
            if e["action"] == "release_event" and e["new_value"]["kind"] != "inject"}


def test_a_log_recorded_on_old_step_text_replays_as_recorded():
    file_text = {s["n"]: s["text_ar"] for s in data.load_scenario("S1")["steps"]}
    assert any(file_text[n] != text for n, text in _sent(OLD_ARABIC_LOG).items())  # the text did change
    recorded, replayed = runs.replay(OLD_ARABIC_LOG)
    assert recorded and replayed == recorded


def test_s1_6_and_s5_6_carry_the_two_consistency_rulings():
    s1, s5 = data.load_scenario("S1")["steps"], data.load_scenario("S5")["steps"]
    assert "يقترح موظف خدمة العملاء" in s1[5]["text_ar"] and "ممثل" not in s1[5]["text_ar"]
    assert "تطلب هيئة تنظيم الاتصالات والحكومة الرقمية (TDRA)" in s5[5]["text_ar"]
