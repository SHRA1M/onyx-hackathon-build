"""Task 46 (order 2026-11-04-task-46-readme-diagram, hq ruling task-46-stop-1-ruling-2026-11-04): the Mermaid figure
under "## Y.3172 mapping" and the mapping table cannot drift apart. `problems` returns every miss, so the same checks
run on the README as committed and, broken on purpose, on the cases below."""

import ast
import re

import pytest

from onyx import kb

README = (kb.REPO / "README.md").read_text(encoding="utf-8")
NINE = {"SRC", "C", "PP", "M", "P", "D", "SINK", "MLFO", "ML sandbox"}
FOLDER = "onyx/data/scenarios/"  # ruling item 3: the one path that is not a .py file
OPTIONAL = {"onyx/whatif.py", "onyx/modeldown.py", "onyx/localmodel.py"}
CAPTION = ("Solid edge: used on every recorded run. Dotted edge: used only by an optional step: `whatif`, `model-down`, "
           "`kb fetch`, and `localmodel` (a page, recorded by `scripts/demo_local.py`).")
SANDBOX_WHERE = ("`onyx/runs.py`, `onyx/eval.py`, `onyx/whatif.py`, `onyx/modeldown.py`, `onyx/localmodel.py`; "
                 "`runs/ungoverned/`, `eval/results.md`")
SANDBOX_IN_MIZAN = ("the governed-versus-ungoverned run on the same scenarios; optional replays under a proposed rule "
                    "or a failed model call, and a local-model run, none scored")

BOX = re.compile(r'^(\w+)\["([^"]*)"\]$')
SUBGRAPH = re.compile(r'^subgraph \w+\["([^"]+)"\]$')
EDGE = re.compile(r'^(\w+) (-->|-\.->|-\. "[^"]+" \.->) (\w+)$')


def _section(readme: str) -> str:
    return readme.split("## Y.3172 mapping\n", 1)[1].split("\n## ", 1)[0]


def _block(readme: str) -> str | None:
    found = re.search(r"\A\n```mermaid\n(.*?)\n```\n", _section(readme), re.S)
    return found[1] if found else None


def _parse(block: str) -> tuple[dict[str, tuple[str, str]], list[tuple[str, str, str]], list[str], list[str]]:
    """Boxes {id: (subgraph title, path)}, edges (from, kind, to), comments, lines it could not read."""
    boxes, edges, comments, unread, title = {}, [], [], [], None
    for line in (l.strip() for l in block.splitlines()):
        if line.startswith("%%"):
            comments.append(line)
        elif not line or line.startswith("flowchart "):
            continue
        elif line == "end":
            title = None
        elif found := SUBGRAPH.match(line):
            title = found[1]
        elif found := BOX.match(line):
            path = found[2].rsplit("<br/>", 1)[-1]
            boxes[found[1]] = (title, path)
        elif found := EDGE.match(line):
            edges.append((found[1], "solid" if found[2] == "-->" else "dotted", found[3]))
        else:
            unread.append(line)
    return boxes, edges, comments, unread


def _table(readme: str) -> dict[str, list[str]]:
    """Mapping table: node -> the cells after it."""
    rows = [l for l in _section(readme).splitlines() if l.startswith("| ") and not l.startswith("| ---")][1:]
    return {r.strip("|").split("|")[0].strip(): [c.strip() for c in r.strip().strip("|").split("|")[1:]] for r in rows}


def _under_onyx(cell: str) -> set[str]:
    return {p for p in re.findall(r"`([^`]+)`", cell) if p.startswith("onyx/")}


def _imports(path: str) -> set[str]:
    found = set()
    for node in ast.walk(ast.parse((kb.REPO / path).read_text(encoding="utf-8"))):
        if isinstance(node, ast.ImportFrom) and node.module and node.module.startswith("onyx"):
            found.add(node.module)
            found |= {f"{node.module}.{a.name}" for a in node.names}
    return found


def _module(path: str) -> str:
    return path.removesuffix(".py").replace("/", ".")


def problems(readme: str) -> list[str]:
    block = _block(readme)
    if block is None:
        return ["no Mermaid block directly under the heading"]
    boxes, edges, comments, unread = _parse(block)
    missed = [f"line not read: {l}" for l in unread]
    table = _table(readme)
    paths = {path for _, path in boxes.values()}

    for box, (title, path) in boxes.items():
        if title not in NINE:
            missed.append(f"box {box} is in subgraph {title}")
        if not (kb.REPO / path).exists():
            missed.append(f"{path} is not in the repo")
        if not (path == FOLDER or re.fullmatch(r"onyx/[\w/]+\.py", path)):
            missed.append(f"{path} may not appear")
    titles = set(re.findall(r'subgraph \w+\["([^"]+)"\]', block))
    if titles != NINE:
        missed.append(f"subgraph titles {sorted(titles)}")
    if not NINE <= set(table):
        missed.append("a node is missing from the table")
    if len(boxes) > 25:
        missed.append(f"{len(boxes)} boxes")

    named = {p for cells in table.values() for p in _under_onyx(cells[-1])}
    if paths != named:
        missed.append(f"diagram and table differ: {sorted(paths ^ named)}")
    for node in NINE & set(table):
        here = {p for t, p in boxes.values() if t == node}
        if here != _under_onyx(table[node][-1]):
            missed.append(f"{node}: diagram {sorted(here)}, table {table[node][-1]}")

    for start, kind, end in edges:
        if start not in boxes or end not in boxes:
            missed.append(f"edge {start} {end}: an end is not a box")
            continue
        source, target = boxes[start][1], boxes[end][1]
        optional = {source, target} & OPTIONAL or (source == target == "onyx/kb.py")
        if kind != ("dotted" if optional else "solid"):
            missed.append(f"edge {start} {end} is {kind}")
        if source == FOLDER:
            if target != "onyx/coordinator.py":
                missed.append(f"the folder edge goes to {target}")
        elif source != target and source.endswith(".py") and (kb.REPO / source).exists() and (
                _module(target) not in _imports(source)):  # a bad path is reported above
            missed.append(f"{source} does not import {target}")
    if sum(boxes.get(s, ("", ""))[1] == FOLDER for s, _, _ in edges) != 1:
        missed.append("the scenarios folder needs exactly one edge")
    if not any("onyx/data.py" in c for c in comments):
        missed.append("no comment says the folder edge is a read through onyx/data.py")
    if not any("solid" in c and "dotted" in c for c in comments):
        missed.append("no comment states the edge convention")
    wanted = {("onyx/kb.py", "dotted", "onyx/kb.py"), ("onyx/localmodel.py", "dotted", "onyx/runs.py")}
    held = {(boxes[s][1], k, boxes[e][1]) for s, k, e in edges if s in boxes and e in boxes}
    if not wanted <= held:
        missed.append(f"missing edges: {sorted(wanted - held)}")

    after = _section(readme).split("\n```\n", 1)[1].lstrip("\n").split("\n", 1)[0]
    if after != CAPTION:
        missed.append(f"caption is {after!r}")
    return missed


def test_the_readme_diagram_has_no_miss():
    assert problems(README) == []


def test_the_diagram_sits_above_the_table():
    section = _section(README)
    assert section.index("```mermaid") < section.index("| node | in Y.3172 | in Mizan | where |")


def test_the_ml_sandbox_row_is_hqs():
    row = _table(README)["ML sandbox"]
    assert row == ["ML sandbox", SANDBOX_IN_MIZAN, SANDBOX_WHERE]


def test_the_reviewer_row_points_at_the_diagram_and_the_table():
    row = next(l for l in README.splitlines() if l.startswith("| ITU-T Y.3172 and the Readiness Framework |"))
    assert row.endswith("| [the Y.3172 diagram and mapping table below](#y3172-mapping) |")


@pytest.mark.parametrize("old, new, why", [
    ('onyx/gate.py"]', 'onyx/nothing.py"]', "is not in the repo"),
    ('onyx/gate.py"]', 'docs/gaps.md"]', "may not appear"),
    (' --> gate\n', ' --> nobox\n', "an end is not a box"),
    ('subgraph n_p["P"]', 'subgraph n_p["Policy"]', "subgraph"),
    ('onyx/localmodel.py"]', 'onyx/why.py"]', "diagram and table differ"),
    ('| `onyx/gate.py` |', '| `onyx/gate.py`, `onyx/why.py` |', "diagram and table differ"),
    ('| `onyx/model.py` |', '| `onyx/gate.py` |', "M: diagram"),
    (' --> gate\n', ' -.-> gate\n', "is dotted"),
    ('localmodel -.-> runs', 'localmodel --> runs', "is solid"),
    ('localmodel -.-> runs', 'localmodel -.-> gate', "does not import"),
    ('kb -. "kb fetch" .-> kb', '%% gone', "missing edges"),
    ('Dotted edge: used only', 'Dotted edge: only', "caption is"),
    ('```mermaid', '```text', "no Mermaid block"),
])
def test_each_kind_of_miss_fails(old, new, why):
    assert old in README, old
    assert any(why in p for p in problems(README.replace(old, new))), why
