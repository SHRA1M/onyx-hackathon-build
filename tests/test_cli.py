"""Order 2026-10-21-task-9-fixes-tasks-10-11, Part B (master order Tasks 10 and 11): the replay shows the hand-over
in both languages, the replay pages are generated and stable, selftest checks its figures against a fresh eval, the
README's two-minute check runs, and its first screen carries the register, the counts and the Y.3172 table."""

import os
import re
import subprocess
import sys
import time
from pathlib import Path

import pytest

from onyx import data, kb, replay_page

ROOT = Path(__file__).resolve().parents[1]
README = (ROOT / "README.md").read_text(encoding="utf-8")


def _onyx(*args):
    env = {k: v for k, v in os.environ.items() if not k.startswith("ONYX_MODEL")} | {"PYTHONIOENCODING": "utf-8"}
    started = time.perf_counter()
    result = subprocess.run([sys.executable, "-m", "onyx", *args], capture_output=True, text=True, encoding="utf-8",
                            cwd=ROOT, env=env)
    return result, time.perf_counter() - started


def _rule(rule_id):
    return next(r for r in data.load_rules() if r["id"] == rule_id)


# --- Task 10: replay shows the hand-over, both languages ----------------------------------------------------

@pytest.mark.parametrize("log", ["runs/S2/run1.jsonl", "runs/S2/ar/run1.jsonl"])
def test_replay_shows_the_handover_in_both_languages(log):
    result, _ = _onyx("replay", log)
    assert result.returncode == 0, result.stdout + result.stderr
    out = result.stdout
    assert "Hand-over" in out
    rule = _rule("cpr-26-7-2")
    assert rule["quote"] in out and rule["quote_ar"] in out


# --- item 7: replay pages ------------------------------------------------------------------------------------

def test_replay_pages_are_committed_and_stable(tmp_path):
    replay_page.write(tmp_path)
    again = tmp_path / "again"
    replay_page.write(again)
    for sid in ("S1", "S2", "S3", "S4", "S5"):
        page = (tmp_path / f"{sid}.md").read_bytes()
        assert page == (again / f"{sid}.md").read_bytes(), sid
        assert page == (replay_page.OUT / f"{sid}.md").read_bytes(), f"{sid}: run `python -m onyx replay-page`"


def test_replay_page_shows_steps_proposals_verdicts_and_quotes():
    page = replay_page.render(replay_page.RUNS / "S2" / "run1.jsonl")
    rule = _rule("cpr-26-7-2")
    for text in ("S2-1", "S2-6", "draft_reply", "block", "CPR 26.7.2", rule["quote"], rule["quote_ar"],
                 "INSUFFICIENT_EVIDENCE"):
        assert text in page, text


def test_replay_page_gives_both_languages_at_every_abstention():
    page = replay_page.render(replay_page.RUNS / "S2" / "run1.jsonl")
    abstention = page.split("INSUFFICIENT_EVIDENCE", 1)[1]
    searched = [r for r in data.load_rules() if r["quote_ar"]]
    assert any(r["quote_ar"] in abstention for r in searched)


# --- addendum item 18 (as the order glosses it): selftest checks its figures -----------------------------------

def test_selftest_checks_figures_against_a_fresh_eval():
    result, elapsed = _onyx("selftest")
    assert result.returncode == 0, result.stdout + result.stderr
    assert "figures match a fresh eval" in result.stdout
    assert elapsed < 60


# --- item 6: the two-minute check ----------------------------------------------------------------------------

def _quickstart():
    block = README.split("## Two-minute check", 1)[1].split("```", 2)[1]
    return [line.strip() for line in block.splitlines() if line.strip()]


def test_quickstart_follows_the_register():
    assert README.index("<!-- gap-register:end -->") < README.index("## Two-minute check") < README.index("## Model")


def test_quickstart_holds_the_order_commands():
    lines = _quickstart()
    assert lines[0].startswith("git clone ") and "uv sync" in lines
    assert "uv run python -m onyx selftest" in lines
    assert any(re.fullmatch(r"uv run python -m onyx replay runs/S2/(ar/)?run\d\.jsonl", l) for l in lines)
    assert "uv run pytest -q" in lines


@pytest.mark.parametrize("line", [l for l in _quickstart() if l.startswith("uv run python -m onyx ")])
def test_every_quickstart_onyx_command_runs_offline_under_60s(line):
    """`git clone`, `uv sync` and `pytest -q` are run by CI (.github/workflows/reproduce.yml)."""
    result, elapsed = _onyx(*line.split()[5:])
    assert result.returncode == 0, result.stdout + result.stderr
    assert elapsed < 60, f"{line}: {elapsed:.1f} s"


# --- addenda items 1/13 and 7: the first screen --------------------------------------------------------------

def test_readme_first_screen_states_the_status_counts():
    rows = kb.load_manifest()
    head = README.split("## Two-minute check", 1)[0]
    for status in ("VERIFIED", "REFERENCED", "UNVERIFIED"):
        count = sum(r["status"] == status for r in rows)
        assert f"{count} {status}" in head, status


# --- master Task 11, addendum item 21: the Y.3172 table -----------------------------------------------------

def test_readme_maps_every_y3172_node_and_leaves_no_cell_blank():
    section = README.split("## Y.3172 mapping", 1)[1].split("\n## ", 1)[0]
    rows = [r for r in section.splitlines() if r.startswith("| ") and not r.startswith("| ---")][1:]
    nodes = [r.split("|")[1].strip() for r in rows]
    for node in ("SRC", "C", "PP", "M", "P", "D", "SINK", "MLFO", "ML sandbox"):
        assert node in nodes, node
    for r in rows:
        assert all(cell.strip() for cell in r.strip().strip("|").split("|")), r


# --- item 8: CI ----------------------------------------------------------------------------------------------

def test_ci_runs_the_order_steps():
    ci = (ROOT / ".github" / "workflows" / "reproduce.yml").read_text(encoding="utf-8")
    for step in ("pytest", "check-data", "kb verify", "verify-log", "onyx replay", "onyx eval", "onyx gaps",
                 "replay-page", "git diff --exit-code"):
        assert step in ci, step
    assert "secrets." not in ci
    assert "actions/workflows/reproduce.yml/badge.svg" in README
