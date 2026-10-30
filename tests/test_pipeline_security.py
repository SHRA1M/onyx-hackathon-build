"""Order 2026-10-30 Task 34, Part B item 6: the README's Y.3172 clause 9 line (security of the pipeline) states only
what these tests show. No provider key in the tracked source tree; a run reads the KB and keys and writes the log
only by appending chained events; the model adapter is the only outward call a run can make."""

import ast
import builtins
import io
import re
import socket
import subprocess
import urllib.request
from pathlib import Path

from onyx import audit, kb, runs

REPO = kb.REPO
# provider key shapes: OpenAI and OpenAI-compatible (sk-, sk-proj-, sk-or-v1-), Anthropic (sk-ant-), AWS, GitHub
KEY_PATTERN = re.compile(r"(?<![A-Za-z0-9_-])sk-(?:ant-|proj-|or-v1-)?[A-Za-z0-9_-]{20,}|AKIA[0-9A-Z]{16}|gh[pousr]_[A-Za-z0-9]{36}")
LOG = REPO / "runs" / "c5" / "S2" / "run1.jsonl"


def _tracked() -> list[Path]:
    out = subprocess.run(["git", "ls-files", "-z"], cwd=REPO, capture_output=True, check=True).stdout
    return [REPO / p for p in out.decode("utf-8").split("\0") if p]


def test_no_provider_key_in_the_source_tree():
    files = _tracked()
    assert len(files) > 100
    assert REPO / ".env" not in files
    hits = []
    for path in files:
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, FileNotFoundError):
            continue
        hits += [f"{path.relative_to(REPO).as_posix()}: {m[0][:12]}..." for m in KEY_PATTERN.finditer(text)]
    assert hits == []


def test_the_key_pattern_catches_a_key():
    assert KEY_PATTERN.search("ONYX_MODEL_API_KEY=sk-or-v1-" + "0123456789abcdef" * 4)
    assert KEY_PATTERN.search("sk-ant-api03-" + "x" * 40)
    assert not KEY_PATTERN.search("risk-free task-34-other-uae-texts-and-more sk-short")


def test_a_run_writes_only_its_log_by_appending_and_makes_no_outward_call(monkeypatch):
    protected = [REPO / "kb", REPO / "onyx" / "data" / "keys", REPO / "runs"]
    opened = []
    real_open = io.open

    def recording_open(file, mode="r", *args, **kwargs):
        if any(c in mode for c in "wax+"):
            opened.append((Path(file).resolve(), mode))
        return real_open(file, mode, *args, **kwargs)

    def no_network(*args, **kwargs):
        raise AssertionError("outward call in a run")

    monkeypatch.setattr(io, "open", recording_open)
    monkeypatch.setattr(builtins, "open", recording_open)
    monkeypatch.setattr(socket, "socket", no_network)
    monkeypatch.setattr(urllib.request, "urlopen", no_network)
    recorded, replayed = runs.replay(LOG)
    assert recorded and replayed == recorded
    assert opened, "the run wrote nothing: the recorder saw no open"
    for path, mode in opened:
        assert not any(path.is_relative_to(p.resolve()) for p in protected), (path, mode)
    logs = [(p, m) for p, m in opened if p.name == "replay.jsonl"]
    assert logs and {m for _, m in logs} == {"a"}


def test_the_log_is_written_only_through_the_chained_append():
    tree = ast.parse((REPO / "onyx" / "audit.py").read_text(encoding="utf-8"))
    modes = [c.args[0].value for c in ast.walk(tree) if isinstance(c, ast.Call)
             and getattr(c.func, "attr", None) == "open" and c.args and isinstance(c.args[0], ast.Constant)]
    assert modes == ["a"]
    assert audit.verify(LOG)


def test_the_model_adapter_is_the_only_outward_call_in_a_run():
    """urlopen, sockets and HTTP clients appear in onyx/model.py and in kb.py's _download (the `kb fetch` command,
    which a run never calls); nowhere else in the package."""
    outward = {"urlopen", "socket", "http.client", "requests", "httpx", "aiohttp", "openai"}
    found = {}
    for path in sorted((REPO / "onyx").rglob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            names = []
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                names = [a.name for a in node.names] + ([node.module] if isinstance(node, ast.ImportFrom) else [])
            elif isinstance(node, ast.Attribute):
                names = [node.attr]
            if any(n in outward for n in names if n):
                found.setdefault(path.relative_to(REPO).as_posix(), set()).update(n for n in names if n in outward)
    assert found == {"onyx/model.py": {"urlopen"}, "onyx/kb.py": {"urlopen"}}
    kb_tree = ast.parse((REPO / "onyx" / "kb.py").read_text(encoding="utf-8"))
    callers = {f.name for f in ast.walk(kb_tree) if isinstance(f, ast.FunctionDef)
               and any(isinstance(n, ast.Attribute) and n.attr == "urlopen" for n in ast.walk(f))}
    assert callers == {"_download"}
    run_modules = {"coordinator", "gate", "audit", "runs"} | {p.stem for p in (REPO / "onyx" / "agents").glob("*.py")}
    for name in run_modules:
        path = REPO / "onyx" / f"{name}.py"
        if not path.exists():
            path = REPO / "onyx" / "agents" / f"{name}.py"
        assert "_download" not in path.read_text(encoding="utf-8"), path
