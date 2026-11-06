"""Every committed C3, C4 and C5 run log replays as recorded (order 2026-10-29 Task 29, global constraint "logs
untouched": each part must leave every recorded decision as the log wrote it). Offline: RecordedModel, no call."""

import pytest

from onyx import audit, kb, runs

RUNS = kb.REPO / "runs"
# C3: runs/S*/ and runs/ungoverned/; C4: runs/c4/; C5: runs/c5/ (as site.py's verify page reads them)
LOGS = sorted(p for p in RUNS.rglob("*.jsonl") if "gaps" not in p.parts
              and (p.relative_to(RUNS).parts[0] in {"c4", "c5", "ungoverned"} or p.relative_to(RUNS).parts[0] in
                   {"S1", "S2", "S3", "S4", "S5"}))
C5 = [p for p in LOGS if p.relative_to(RUNS).parts[0] == "c5"]
EARLIER = [p for p in LOGS if p.relative_to(RUNS).parts[0] != "c5"]
# Task 52b: the U8 logs, under the old reading (runs/u8) and the new (runs/u8-fixed), each by its own start config
U8 = sorted(p for name in ("u8", "u8-fixed") for p in (RUNS / name).rglob("*.jsonl"))


def _id(path):
    return path.relative_to(RUNS).as_posix()


def test_logs_found():
    assert (len(C5), len(EARLIER)) == (20, 80)
    assert len(U8) == 24


@pytest.mark.parametrize("log", C5, ids=_id)
def test_c5_logs_replay_unchanged(log):
    assert audit.verify(log)
    recorded, replayed = runs.replay(log)
    assert recorded and replayed == recorded


@pytest.mark.parametrize("log", EARLIER, ids=_id)
def test_c3_c4_logs_replay_unchanged(log):
    assert audit.verify(log)
    recorded, replayed = runs.replay(log)
    assert recorded and replayed == recorded


@pytest.mark.parametrize("log", U8, ids=_id)
def test_u8_logs_replay_unchanged(log):
    assert audit.verify(log)
    recorded, replayed = runs.replay(log)
    assert recorded and replayed == recorded
