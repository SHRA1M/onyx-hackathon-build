"""Order 2026-10-17, Task 10: `python -m onyx selftest` runs S1 with MockModel, no key, under 60 seconds, and prints
the headline figures from eval/results.json (eval/scripted/results.json, labelled scripted, until live results
exist)."""

import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_selftest_offline_under_60s(tmp_path):
    env = {k: v for k, v in os.environ.items() if not k.startswith("ONYX_MODEL")}
    started = time.perf_counter()
    result = subprocess.run([sys.executable, "-m", "onyx", "selftest"],
                            capture_output=True, text=True, encoding="utf-8", cwd=ROOT, env=env)
    elapsed = time.perf_counter() - started
    assert result.returncode == 0, result.stdout + result.stderr
    assert elapsed < 60, f"selftest took {elapsed:.1f} s"
    out = result.stdout
    assert "S1" in out and "no model call" in out
    assert "chain ok" in out and "replay matches" in out
    assert "Headline figures" in out and "results.json" in out
    assert "Action recall" in out and "Obligation proxy" in out


def _files():
    return {p for d in ("runs/scripted", "runs/local", "eval", "gaps") for p in (ROOT / d).rglob("*") if p.is_file()}


def test_selftest_writes_nothing_in_the_repo():
    before = _files()
    subprocess.run([sys.executable, "-m", "onyx", "selftest"], capture_output=True, text=True, encoding="utf-8",
                   cwd=ROOT, check=True)
    assert _files() == before
