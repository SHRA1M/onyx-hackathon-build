"""Task 39 E (order 2026-11-02-task-39-pre-freeze item E, hq rulings task-39-stops-ruling and -ruling-2): S2 recorded
once on a local model through Ollama, shown on docs/site/localmodel.html and never scored."""

import json
from html import escape
import re

from onyx import audit, eval as onyx_eval, kb, localmodel, site

REPO = kb.REPO


def test_the_run_is_live_on_the_machine_tag_and_its_chain_holds():
    assert audit.verify(localmodel.RUN)
    start = localmodel.events()[0]
    assert start["action"] == "run_start" and start["new_value"]["source"] == "live"
    assert start["new_value"]["model"] == localmodel.machine()["model"] == "qwen2.5:14b-instruct"


def test_eval_ignores_demo_local(tmp_path):
    """The C5 figures are unchanged with runs/demo-local/ present: eval over runs/ writes the committed files."""
    assert localmodel.RUN.exists()
    onyx_eval.evaluate(REPO / "runs", tmp_path)
    for name in ("results.json", "results.md"):
        assert (tmp_path / name).read_bytes() == (REPO / "eval" / name).read_bytes(), name
    assert "demo-local" not in (tmp_path / "results.json").read_text(encoding="utf-8")


def test_rows_come_from_the_log():
    rows = localmodel.rows()
    assert [r["step"] for r in rows if r["event"] == "propose"] == ["S2-2-care", "S2-3-care", "S2-4-care",
                                                                     "S2-5-adviser", "S2-6-tdra"]
    unparsed = [r for r in rows if r["event"] == "propose" and r["proposals"] == 0]
    assert [r["step"] for r in unparsed] == ["S2-2-care"]
    gates = {r["step"]: r["verdict"] for r in rows if r["event"] == "gate"}
    assert gates["S2-3-care"] == "hold" and gates["S2-6-tdra"] == "insufficient_evidence"


def test_page_shows_label_machine_and_steps_and_no_figure():
    page = site.render()["localmodel.html"]
    assert escape(localmodel.LABEL) in page
    m = localmodel.machine()
    for value in (m["model"], m["ollama"], m["gpu"], m["ram_gb"], *m["settings"], *m["settings"].values()):
        assert escape(value) in page, value
    for row in localmodel.rows():
        assert row["step"] in page
    text = re.sub(r"<[^>]+>", " ", page.split('<main class="site">', 1)[1])
    for word in ("seconds?", "tokens?", "scores?", "recall", "validity", "rate", "faster", "slower", "usd"):
        assert not re.search(rf"\b{word}\b", text.lower()), word
    assert "%" not in text
    assert "model_ms" not in page and "gate_ms" not in page


def test_page_is_in_the_bar_and_on_the_index():
    pages = site.render()
    assert 'href="localmodel.html"' in pages["index.html"]
    assert ("localmodel.html", "Local model") in site.PAGES


def test_readme_and_annex_carry_one_line_each():
    readme = (REPO / "README.md").read_text(encoding="utf-8")
    model = readme.split("## Model", 1)[1].split("\n## ", 1)[0]
    assert "docs/site/localmodel.html" in model and "runs/demo-local/" in model
    annex = (REPO / "docs" / "annex.md").read_text(encoding="utf-8")
    sentence = ("A recorded run of S2 on qwen2.5:14b-instruct through Ollama on a desktop GPU is in "
                "`runs/demo-local/`, shown in `docs/site/localmodel.html` and not scored.")
    assert "the gates, not the model, hold the law. " + sentence in " ".join(annex.split())


def test_machine_file_holds_configuration_only():
    m = json.loads((REPO / "runs" / "demo-local" / "machine.json").read_text(encoding="utf-8"))
    assert set(m) == {"model", "ollama", "gpu", "ram_gb", "settings", "recorded"}
