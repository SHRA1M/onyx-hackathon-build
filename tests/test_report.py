"""Task 12 part A (order 2026-10-23-task-12-report-build): docs/build_report.py writes docs/report.docx from
docs/report.md on the template, byte-identical on a second build, and fails when a figure in a tagged paragraph
matches no value of its run set in eval/results.md (hq rulings 1 and 2 on the build's first stop); the replay pages
read C5 runs where a C5 run cites the grounding clause; the coordinator writes the register's candidate id."""

import importlib.util
import json
import re
import subprocess
import sys
import zipfile

import pytest

from onyx import data, kb, replay_page, scripted
from onyx.coordinator import Coordinator
from onyx.model import MockModel

DOCS = kb.REPO / "docs"
REPORT_MD = DOCS / "report.md"
HEADINGS = ["Introduction", "Description of the use case", "Use case requirement",
            "Mapping with ITU-T Y.3172, Readiness 2.0 Report, and domain-specific policies", "Error scenarios",
            "Policy gaps and standards gaps derived from the mapping exercise"]


def _load():
    spec = importlib.util.spec_from_file_location("build_report", DOCS / "build_report.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _build(md, out):
    return subprocess.run([sys.executable, str(DOCS / "build_report.py"), "--md", str(md), "--out", str(out)],
                          capture_output=True, text=True, encoding="utf-8", cwd=kb.REPO)


@pytest.fixture(scope="module")
def built(tmp_path_factory):
    out = tmp_path_factory.mktemp("report") / "report.docx"
    result = _build(REPORT_MD, out)
    assert result.returncode == 0, result.stdout + result.stderr
    return out


def _xml(docx_path, name="word/document.xml") -> str:
    with zipfile.ZipFile(docx_path) as z:
        return z.read(name).decode("utf-8")


# --- item 2: the build ---------------------------------------------------------------------------------------

def test_two_builds_are_byte_identical_and_match_the_committed_docx(built, tmp_path):
    again = tmp_path / "again.docx"
    assert _build(REPORT_MD, again).returncode == 0
    assert built.read_bytes() == again.read_bytes()
    assert built.read_bytes() == (DOCS / "report.docx").read_bytes(), "run `python docs/build_report.py`"


def test_six_list_paragraph_headings_in_template_order(built):
    from docx import Document
    doc = Document(str(built))
    headings = [p.text for p in doc.paragraphs if p.style.name == "List Paragraph"]
    assert headings == HEADINGS
    assert doc.paragraphs[0].text == "AI for Good Sandbox Hackathon – Onyx – Mizan"
    assert [p.text.split(":")[0] for p in doc.paragraphs[1:5]] == ["Team leader", "Team members", "Contact details",
                                                                  "GitHub link"]


def test_two_image_parts_no_template_example_and_no_run_set_tag(built):
    with zipfile.ZipFile(built) as z:
        media = [n for n in z.namelist() if n.startswith("word/media/")]
    assert len(media) == 2
    text = re.sub(r"<[^>]+>", "", _xml(built))
    for gone in ("smart pen", "NOTE", "Step-1", "Team Name"):
        assert gone not in text, gone
    assert not re.search(r"\[C[35]", text)
    assert "`" not in text and "**" not in text


def test_limits_and_next_steps_close_section_6_without_a_heading(built):
    from docx import Document
    doc = Document(str(built))
    para = next(p for p in doc.paragraphs if p.text.startswith("Limits and next steps."))
    assert para.runs[0].bold and para.runs[0].text.strip() == "Limits and next steps."
    assert para.style.name != "List Paragraph"


def test_the_mapping_table_replaces_the_template_table_and_tables_keep_its_style(built):
    from docx import Document
    doc = Document(str(built))
    assert len(doc.tables) == 2
    mapping, gaps = doc.tables
    assert mapping.rows[0].cells[0].text == "Node" and mapping.rows[1].cells[0].text == "SRC"
    assert gaps.rows[0].cells[0].text == "#" and gaps.rows[9].cells[0].text == "9"
    for table in doc.tables:
        assert table.style.style_id == "TableGridLight"
        assert all(r.bold for c in table.rows[0].cells for p in c.paragraphs for r in p.runs)


def test_core_dates_are_fixed(built):
    core = _xml(built, "docProps/core.xml")
    assert "2026-10-23T00:00:00Z" in core


def test_a_missing_figure_fails_the_build(tmp_path):
    md = tmp_path / "report.md"
    md.write_text(REPORT_MD.read_text(encoding="utf-8").replace("fig2-results.png", "fig9-missing.png"),
                  encoding="utf-8", newline="\n")
    result = _build(md, tmp_path / "out.docx")
    assert result.returncode != 0 and "fig9-missing.png" in result.stdout + result.stderr


# --- item 3: the value check ---------------------------------------------------------------------------------

def test_a_tagged_value_changed_by_001_fails_naming_the_token(tmp_path):
    text = REPORT_MD.read_text(encoding="utf-8")
    assert "action recall against the frozen keys\n0.96 / 0.94" in text
    md = tmp_path / "report.md"
    md.write_text(text.replace("keys\n0.96 / 0.94", "keys\n0.97 / 0.94"), encoding="utf-8", newline="\n")
    result = _build(md, tmp_path / "out.docx")
    output = result.stdout + result.stderr
    assert result.returncode != 0
    assert "0.97" in output and "Results" in output


def test_every_tagged_paragraph_of_the_report_passes():
    build = _load()
    sets = build.run_sets((kb.REPO / "eval" / "results.md").read_text(encoding="utf-8"))
    tagged = [p for p in build.paragraphs(REPORT_MD.read_text(encoding="utf-8")) if build.tags(p)]
    assert len(tagged) == 2
    for para in tagged:
        assert build.check_paragraph(para, sets) == []


def test_the_run_sets_hold_the_values_the_order_names():
    build = _load()
    sets = build.run_sets((kb.REPO / "eval" / "results.md").read_text(encoding="utf-8"))
    assert (107, 112) in sets["C5"].pairs
    assert any(u == "ms" and str(v) == "0.458" for v, u in sets["C3"].units)
    assert any(u == "ms" and str(v) == "7837.607" for v, u in sets["C3"].units)
    assert any(str(v) == "2.33" for v in sets["C3"].values)
    assert not any(str(v) == "2.33" for v in sets["C5"].values)


@pytest.mark.parametrize("para, bad", [
    ("Passed 2.3 `[C5, governed]`.", "2.3"),              # ruling 1: a match from another run set does not count
    ("It took 0.47 ms `[C3, governed]`.", "0.47 ms"),
    ("It took 7.9 s `[C3, governed]`.", "7.9 s"),
    ("Recall 108 of 112 `[C5, governed]`.", "108 of 112"),
    ("Seen 223 decisions `[C3, governed]`.", "223 decisions"),
])
def test_a_figure_that_matches_nothing_in_its_run_set_fails(para, bad):
    build = _load()
    sets = build.run_sets((kb.REPO / "eval" / "results.md").read_text(encoding="utf-8"))
    problems = build.check_paragraph(para, sets)
    assert len(problems) == 1 and problems[0].startswith(f"{bad}:")


@pytest.mark.parametrize("para", ["(1) Passed 2.3 and 2.1 `[C3, prompt v3]`.", "Recall 0.96 in S3-4 `[C5, x]`."])
def test_list_markers_and_ids_are_skipped(para):
    build = _load()
    sets = build.run_sets((kb.REPO / "eval" / "results.md").read_text(encoding="utf-8"))
    assert build.check_paragraph(para, sets) == []


@pytest.mark.parametrize("para, bad", [("Counted 222 `[C3, governed]`.", "222"), ("(12) items `[C3, x]`.", "12"),
                                       ("Version 2FA `[C3, x]`.", "2FA")])
def test_a_token_the_rule_cannot_classify_fails(para, bad):
    build = _load()
    sets = build.run_sets((kb.REPO / "eval" / "results.md").read_text(encoding="utf-8"))
    problems = build.check_paragraph(para, sets)
    assert len(problems) == 1 and problems[0].startswith(f"{bad}:") and "cannot classify" in problems[0]


# --- item 5: replay pages read C5 runs ----------------------------------------------------------------------

@pytest.mark.parametrize("sid", ["S3", "S4", "S5"])
def test_regenerated_replay_pages_name_their_c5_run(sid):
    page = (DOCS / "replay" / f"{sid}.md").read_text(encoding="utf-8")
    assert f"replay-page` from `runs/c5/{sid}/run1.jsonl`" in page
    assert replay_page.C5_S2_LINE not in page


def test_s1_stays_on_c3_because_no_run_cites_its_grounding_clause():
    assert replay_page.source("S1") == replay_page.RUNS / "S1" / "run1.jsonl"
    for n in (1, 2):
        assert not replay_page.cites_grounding(replay_page.RUNS / "c5" / "S1" / f"run{n}.jsonl", "S1")


# --- item 6: the register's candidate id --------------------------------------------------------------------

def test_the_coordinator_writes_the_register_id_for_s1_step_6(tmp_path):
    # a candidate row is written when the abstention names no gap (as in the bake-off runs that wrote candidate-S1-6)
    script = scripted.model("S1", "en").script
    silent = {"proposals": [], "reasoning_chain": ["INSUFFICIENT_EVIDENCE", "scripted abstention naming no gap"]}
    run = Coordinator(data.load_scenario("S1"), MockModel({**script, "S1-6-adviser": silent}, model="scripted-mock"),
                      scripted.retriever("S1"), log_path=tmp_path / "run1.jsonl", gaps_dir=tmp_path / "gaps")
    run.start(source="scripted", model="scripted-mock", run=1, retrieval="scripted")
    run.run()
    rows = [json.loads(line) for line in (tmp_path / "gaps" / "candidates.jsonl").read_text("utf-8").splitlines()]
    row = next(r for r in rows if r["inject"] == "S1-6")
    assert row["id"] == "candidate-4-4-fixed-term-bundle" and row["local_id"] == "candidate-S1-6"
    assert row["id"] in {g["id"] for g in data.load_gaps()["gaps"]}
