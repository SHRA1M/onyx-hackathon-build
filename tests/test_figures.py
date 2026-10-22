"""Task 17 (order 2026-10-22-task-17-figures): Figure 1 (architecture) and Figure 2 (results), drawn by committed
scripts with matplotlib only, byte-identical on a second run; Figure 2's numbers are the cells of eval/results.md,
parsed here on their own; the README embeds the S2 step 3 screenshot; CI runs both scripts."""

import importlib.util
import re
import subprocess
import sys

import pytest

from onyx import kb

SCRIPTS = kb.REPO / "scripts"
FIG = kb.REPO / "docs" / "fig"
RESULTS = kb.REPO / "eval" / "results.md"
README = (kb.REPO / "README.md").read_text(encoding="utf-8")
SCENARIOS = ["S1", "S2", "S3", "S4", "S5"]
LANGS = ["en", "ar"]


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _run(name: str, out):
    result = subprocess.run([sys.executable, str(SCRIPTS / f"{name}.py"), "--out", str(out)], capture_output=True,
                            text=True, encoding="utf-8", cwd=kb.REPO)
    assert result.returncode == 0, result.stderr


def _section(text: str, heading: str) -> str:
    start = text.index(heading)
    end = text.find("\n## ", start + len(heading))
    return text[start:] if end == -1 else text[start:end]


def _rows(section: str) -> list[list[str]]:
    return [[c.strip() for c in line.strip().strip("|").split("|")] for line in section.splitlines()
            if re.match(r"\| S\d \|", line)]


def _span(cell: str) -> tuple[float, float]:
    parts = [float(p) for p in cell.split(" to ")]
    return parts[0], parts[-1]


# --- byte-identical output ---------------------------------------------------------------------------------------

@pytest.mark.parametrize("name,stem", [("fig_architecture", "fig1-architecture"), ("fig_results", "fig2-results")])
def test_a_second_run_writes_the_same_bytes(tmp_path, name, stem):
    first, second = tmp_path / "a", tmp_path / "b"
    _run(name, first)
    _run(name, second)
    for ext in ("png", "svg"):
        assert (first / f"{stem}.{ext}").read_bytes() == (second / f"{stem}.{ext}").read_bytes()
    # ruling 4 (hq, 2026-10-22): matplotlib's PNG bytes differ across machines, so only the SVG is held to the
    # committed file; the PNG is held to a same-machine redraw above
    assert (FIG / f"{stem}.svg").read_bytes() == (first / f"{stem}.svg").read_bytes(), f"{stem}.svg stale"


# --- Figure 1 ----------------------------------------------------------------------------------------------------

def test_figure_1_labels_come_from_the_readme_mapping_table():
    fig1 = _load("fig_architecture")
    table = {}
    for line in README.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == 4 and cells[0] in fig1.NODES:
            table[cells[0]] = cells[2]
    assert set(table) == set(fig1.NODES) == {"SRC", "C", "PP", "M", "P", "D", "SINK", "MLFO", "ML sandbox"}
    for node, label in fig1.NODES.items():
        assert label in table[node], node


def test_figure_1_carries_the_hand_over_arrow_and_caption():
    fig1 = _load("fig_architecture")
    assert fig1.HANDOVER == "hand-over to a human (gap-8)"
    assert fig1.CAPTION == ("Mizan on the Y.3172 nodes; the model proposes, the P node decides, D hands a complaint "
                            "to a person.")
    svg = (FIG / "fig1-architecture.svg").read_text(encoding="utf-8")
    assert "gap-8" in svg and "hands a complaint" in svg


# --- Figure 2 ----------------------------------------------------------------------------------------------------

def _c5_from_file() -> dict:
    text = RESULTS.read_text(encoding="utf-8")
    section = _section(text, "## C3, C4 and C5")
    out = {}
    for cells in _rows(section):
        if len(cells) != 7:
            continue
        scenario, lang, citation, recall = cells[0], cells[1], cells[2], cells[3]
        out[(scenario, lang)] = {
            "citation": float(citation.split(" / ")[2]),
            "recall": float(re.sub(r"\s*\(.*\)", "", recall.split(" / ")[2])),
        }
    return out


def _c3_from_file() -> dict:
    text = RESULTS.read_text(encoding="utf-8")
    governed, ungoverned = _rows(_section(text, "## Governed")), _rows(_section(text, "## Ungoverned"))
    out = {}
    for g, u in zip(governed, ungoverned):
        assert g[:2] == u[:2]
        out[(g[0], g[1])] = {"rejection": _span(g[3]), "claims": _span(u[11])}
    return out


def test_figure_2_panel_a_is_the_c5_cells_of_results_md():
    fig2 = _load("fig_results")
    expected = _c5_from_file()
    assert set(expected) == {(s, lang) for s in SCENARIOS for lang in LANGS}
    assert fig2.read_values(RESULTS)["a"] == expected


def test_figure_2_panel_b_is_the_c3_governed_and_ungoverned_tables():
    fig2 = _load("fig_results")
    expected = _c3_from_file()
    assert set(expected) == {(s, lang) for s in SCENARIOS for lang in LANGS}
    assert expected[("S1", "ar")]["rejection"] == (0.38, 0.50) and expected[("S1", "en")]["claims"] == (3.0, 3.0)
    assert fig2.read_values(RESULTS)["b"] == expected


def test_figure_2_fails_when_a_value_is_missing(tmp_path):
    fig2 = _load("fig_results")
    text = RESULTS.read_text(encoding="utf-8")
    broken = tmp_path / "results.md"
    broken.write_text(re.sub(r"\n\| S3 \| ar \| 1\.00 / 1\.00 / 1\.00 \|[^\n]*", "", text, count=1), encoding="utf-8")
    with pytest.raises(SystemExit, match="S3 ar"):
        fig2.read_values(broken)


def test_figure_2_captions():
    fig2 = _load("fig_results")
    assert fig2.CAPTION_A == ("C5, Claude Sonnet 5.5, prompt v5, two runs per scenario per language; figures "
                              "regenerate from the committed logs.")
    assert fig2.CAPTION_B == ("C3, prompt v3, three runs per scenario per language; the only "
                              "governed-against-ungoverned pair on file.")


# --- README and CI -----------------------------------------------------------------------------------------------

def test_readme_embeds_the_screenshot_under_three_things():
    line = ("![S2 step 3: the gate blocks the agent's reply and hands the complaint to a person, citing CPR 26.7.2, "
            "p. 65](docs/replay/screenshots/S2-step3-en.png)")
    assert "## Three things to look at first\n\n" + line + "\n" in README


def test_ci_runs_both_figure_scripts_before_the_diff():
    ci = (kb.REPO / ".github" / "workflows" / "reproduce.yml").read_text(encoding="utf-8")
    diff = ci.index("git diff --exit-code")
    for name in ("fig_architecture", "fig_results"):
        assert -1 < ci.find(f"scripts/{name}.py") < diff
