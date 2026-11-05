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
HEADINGS = ["Introduction", "Description of the use case", "What is the role played by AI?", "Requirements",
            "Mapping with ITU-T Y.3172, Readiness 2.0 Report, and domain-specific policies", "Demo scenarios",
            "Error scenarios", "Policy gaps and standards gaps derived from the mapping exercise"]  # Task 36 item 1


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


def test_eight_list_paragraph_headings_in_template_order(built):
    from docx import Document
    doc = Document(str(built))
    headings = [p.text for p in doc.paragraphs if p.style.name == "List Paragraph"]
    assert headings == HEADINGS + ["Annex"]  # Task 38: the annex heading, unnumbered, after the eight
    assert doc.paragraphs[0].text == "AI for Good Sandbox Hackathon – Onyx – Mizan"
    assert [p.text.split(":")[0] for p in doc.paragraphs[1:6]] == ["Team leader", "Team members", "Contact details",
                                                                  "GitHub (public from 2026-11-09)", "Replay site, no install"]  # Task 51 A.2
    assert "Demo video: see the repository README." in doc.paragraphs[5].text


def test_two_image_parts_no_template_example_and_no_run_set_tag(built):
    with zipfile.ZipFile(built) as z:
        media = [n for n in z.namelist() if n.startswith("word/media/")]
    assert len(media) == 2
    text = re.sub(r"<[^>]+>", "", _xml(built))
    # the template's notes read "NOTE:" and "NOTE-"; row 12 quotes Y.3173's "Table 7-2 NOTE 1" (order Task 27, C1)
    for gone in ("smart pen", "NOTE:", "NOTE-", "Step-1", "Team Name"):
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
    assert len(doc.tables) == 5  # Task 38: the annex adds the C3 table and "where to look"; Task 51 B: the strip
    assert doc.tables[0].rows[0].cells[0].text == "5 scenarios, 2 languages, 20 recorded runs"
    mapping, gaps = doc.tables[1:3]
    assert mapping.rows[0].cells[0].text == "Node" and mapping.rows[1].cells[0].text == "SRC"
    assert gaps.rows[0].cells[0].text == "#" and gaps.rows[10].cells[0].text == "11"  # Task 37, rows in number order
    assert gaps.rows[11].cells[0].text == "12"  # Task 37, rows in number order
    for table in doc.tables:
        assert table.style.style_id == "TableGridLight"
        assert all(r.bold for c in table.rows[0].cells for p in c.paragraphs for r in p.runs)


def test_core_dates_are_fixed(built):
    core = _xml(built, "docProps/core.xml")
    assert "2026-10-23T00:00:00Z" in core


def test_the_creator_is_team_onyx_and_the_template_author_is_gone(built):
    core = _xml(built, "docProps/core.xml")
    assert "<dc:creator>Team Onyx</dc:creator>" in core
    with zipfile.ZipFile(built) as z:
        for name in z.namelist():
            assert b"Meng" not in z.read(name), name


def test_a_missing_figure_fails_the_build(tmp_path):
    md = tmp_path / "report.md"
    md.write_text(REPORT_MD.read_text(encoding="utf-8").replace("fig2-results.png", "fig9-missing.png"),
                  encoding="utf-8", newline="\n")
    result = _build(md, tmp_path / "out.docx")
    assert result.returncode != 0 and "fig9-missing.png" in result.stdout + result.stderr


# --- item 3: the value check ---------------------------------------------------------------------------------

def test_a_tagged_value_changed_by_001_fails_naming_the_token(tmp_path):
    text = REPORT_MD.read_text(encoding="utf-8")
    assert "against the frozen keys 0.96 / 1.00" in text
    md = tmp_path / "report.md"
    md.write_text(text.replace("keys 0.96 / 1.00", "keys 0.97 / 1.00"), encoding="utf-8", newline="\n")
    result = _build(md, tmp_path / "out.docx")
    output = result.stdout + result.stderr
    assert result.returncode != 0
    assert "0.97" in output and "Results" in output


def test_a_c3_only_value_in_the_c5_part_of_the_results_paragraph_fails(tmp_path):
    text = REPORT_MD.read_text(encoding="utf-8")
    assert "citation validity 0.99 / 1.00" in text  # Task 29 Part D: "gap recall 0.87" became the B1 line
    md = tmp_path / "report.md"
    md.write_text(text.replace("citation validity 0.99 / 1.00", "citation validity 0.86 / 1.00"), encoding="utf-8",
                  newline="\n")
    result = _build(md, tmp_path / "out.docx")
    assert result.returncode != 0 and "0.86: no value in the run set" in result.stdout + result.stderr


@pytest.mark.parametrize("para, bad", [
    ("Recall 0.96 `[C5, x]`. The gate took 0.46 ms and 0.96 `[C3, y]`.", "0.96"),   # 0.96 is C5 only
    ("Recall 0.86 `[C5, x]`. The gate took 0.46 ms `[C3, y]`.", "0.86"),            # 0.86 is C3 only
    ("Recall 0.87 and 0.46 ms `[C5, x]`. Then 7.8 s `[C3, y]`.", "0.46 ms"),        # C5 has no latency line
])
def test_a_paragraph_with_two_tags_checks_each_sentence_against_its_own_tag(para, bad):
    build = _load()
    sets = build.run_sets((kb.REPO / "eval" / "results.md").read_text(encoding="utf-8"))
    problems = build.check_paragraph(para, sets)
    assert len(problems) == 1 and problems[0].startswith(f"{bad}:")


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
    assert (110, 112) in sets["C5"].pairs
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


# --- Task 18 (order 2026-10-23-task-18-report-five-pages) ----------------------------------------------------

def test_every_table_cell_is_10_pt_with_no_space_before_or_after(built):
    from docx import Document
    from docx.shared import Pt
    doc = Document(str(built))
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    assert p.paragraph_format.space_before == 0 and p.paragraph_format.space_after == 0
                    assert p.runs and all(r.font.size == Pt(10) for r in p.runs), cell.text


def test_both_pictures_are_12_cm_wide_and_keep_with_next(built):
    from docx import Document
    from docx.shared import Cm
    doc = Document(str(built))
    pictures = [p for p in doc.paragraphs if p._p.xpath(".//pic:pic")]
    assert len(pictures) == 2
    for p in pictures:
        assert p.paragraph_format.keep_with_next is True
        assert int(p._p.xpath(".//wp:extent/@cx")[0]) == Cm(11)  # Task 36 stop 2 ruling


def test_the_eight_headings_keep_with_next(built):
    from docx import Document
    doc = Document(str(built))
    headings = [p for p in doc.paragraphs if p.style.name == "List Paragraph"]
    assert len(headings) == 9 and all(p.paragraph_format.keep_with_next for p in headings)  # Task 38: + "Annex"


def test_the_readme_has_the_reviewer_block_under_the_synthetic_data_notice():
    readme = (kb.REPO / "README.md").read_text(encoding="utf-8")
    notice = readme.index("> **Synthetic data.**")
    block = readme.index("## For the reviewer\n\nThe five published criteria, each with its evidence and one way to "
                         "check it:")
    assert notice < block < readme.index("Mizan puts a consumer on the line")
    lines = readme[block:readme.index("Mizan puts a consumer on the line")].strip().splitlines()
    rows = [line for line in lines if line.startswith("| ") and not line.startswith("| Criterion")]  # Task 39 C
    assert len(rows) == 5  # Task 45: the gaps row split from the agent row
    assert rows[0].startswith(f"| Knowledge base | `kb/manifest.csv` ({len(kb.load_manifest())} rows")  # read, Task 30
    assert rows[4].startswith("| ITU-T Y.3172 and the Readiness Framework |")


def test_the_reviewer_table_names_only_commands_and_paths_that_exist():
    """Task 39 C: every `python -m onyx <command>` in the table is in `python -m onyx --help`, every backticked path
    (and every path a command names) exists, and every link is a heading of the README."""
    readme = (kb.REPO / "README.md").read_text(encoding="utf-8")
    block = readme.split("## For the reviewer\n", 1)[1].split("Mizan puts a consumer on the line", 1)[0]
    rows = [line for line in block.splitlines() if line.startswith("| ") and not line.startswith("| Criterion")]
    assert len(rows) == 5 and all(len(row.strip("|").split(" | ")) == 3 for row in rows)
    helptext = subprocess.run([sys.executable, "-m", "onyx", "--help"], capture_output=True, text=True,
                              cwd=kb.REPO, check=True).stdout
    listed = set(re.findall(r"^    (\S+)\s", helptext, re.M))
    ticked = [t for row in rows for t in re.findall(r"`([^`]+)`", row)]
    commands = [t for t in ticked if "python -m onyx" in t]
    assert len(commands) == 3
    for command in commands:
        words = command.split("python -m onyx ", 1)[1].split()
        assert words[0] in listed, command
        assert all((kb.REPO / w).exists() for w in words if "/" in w), command
    paths = [t.split(" ")[0] for t in ticked if t not in commands]
    assert paths and all((kb.REPO / p).exists() for p in paths), paths
    anchors = re.findall(r"\]\(#([^)]+)\)", "\n".join(rows))
    headings = {re.sub(r"[^a-z0-9 -]", "", h.lower()).replace(" ", "-") for h in re.findall(r"^## (.+)$", readme, re.M)}
    assert anchors and set(anchors) <= headings, anchors


# --- Task 29 Part D (order 2026-10-29-task-29-field-take, Part D; release order 2026-10-30) --------------------

def _gap_cell(md: str, n: str) -> str:
    row = next(line for line in md.splitlines() if line.startswith(f"| {n} |"))
    return row.split("|")[2]


def test_report_gap12_maps_before_claiming():
    cell = _gap_cell(REPORT_MD.read_text(encoding="utf-8"), "12")
    assert cell.index("Y.3173") < cell.index("neither") and cell.index("D9") < cell.index("neither")
    assert cell.strip().endswith("Left open with ITU's agreement (2026-10-30).")
    gap = data.load_gaps()["gaps"]
    row = next(g for g in gap if g["id"] == "gap-12")["gap"]
    assert row.index("Y.3173") < row.index("neither") and row.index("D9") < row.index("neither")


def test_report_figures_match_eval():
    build = _load()
    sets = build.run_sets((kb.REPO / "eval" / "results.md").read_text(encoding="utf-8"))
    text = REPORT_MD.read_text(encoding="utf-8")
    b1 = "expected gaps: 5 of 7 found in every run, 2 missed (both S1), 3 unexpected ids flagged"  # Task 36 stop 2 ruling, change 6
    assert b1 in text
    # Task 36 cut 3: the interval left the report's Results; it stays in eval's output and the README
    assert "95% interval" not in text.split("**Results**")[1].split("## ")[0]
    for where in ("eval/results.md", "README.md"):
        assert "110 of 112 key steps, 95% interval 0.94 to 1.00" in (kb.REPO / where).read_text(encoding="utf-8")
    assert build.check_paragraph(f"Results {b1} `[C5, x]`.", sets) == []
    assert build.check_paragraph("Recall 110 of 112, 95% interval 0.937 to 0.995 pooled `[C5, x]`.", sets) == []


@pytest.mark.parametrize("para, bad", [
    ("Expected gaps: 4 of 7 found in every run `[C5, x]`.", "4 of 7"),
    ("Expected gaps: 1 missed `[C5, x]`.", "1 missed"),
    ("Then 4 unexpected register ids flagged `[C5, x]`.", "4 unexpected"),
    ("Recall 95% interval 0.938 to 0.995 pooled `[C5, x]`.", "95% interval 0.938 to 0.995"),
    # a bound that rounds to 1.00 while misses exist is written with three decimals (Iyas, 2026-10-30)
    ("Recall 95% interval 0.94 to 1.00 pooled `[C5, x]`.", "95% interval 0.94 to 1.00"),
    ("Recall 95% interval 0.937 to 0.995 pooled `[C3, x]`.", "95% interval 0.937 to 0.995"),
])
def test_a_b1_count_or_interval_that_matches_nothing_fails(para, bad):
    build = _load()
    sets = build.run_sets((kb.REPO / "eval" / "results.md").read_text(encoding="utf-8"))
    problems = build.check_paragraph(para, sets)
    assert len(problems) == 1 and problems[0].startswith(f"{bad}:"), problems


def test_the_pooled_citation_interval_reads_too():
    build = _load()
    sets = build.run_sets((kb.REPO / "eval" / "results.md").read_text(encoding="utf-8"))
    assert build.check_paragraph("Validity 95% interval 0.958 to 0.999 `[C5, x]`.", sets) == []  # 130 of 131


def test_the_s2_paragraph_names_the_model_down_page():
    text = REPORT_MD.read_text(encoding="utf-8")
    whatif = text.index("(`docs/replay/whatif-S2-gap-1.md`).")
    down = text.index("With the model call made to fail at step 3, the coordinator's deny-by-default hold hands the "
                      "conversation to the same human, with no model in that step (`docs/replay/model-down-S2.md`).")
    assert whatif < down < text.index("**S3,")
    assert (kb.REPO / "docs" / "replay" / "model-down-S2.md").exists()


# --- order 2026-10-30-task-30-global-examples, Part C ----------------------------------------------------------

@pytest.mark.parametrize("n, label", [("1", "Spain Ley 10/2025 Art 8(2), 8(3)"),
                                      ("10", "Wales WLS Regs 2015 Sch 1 Std 15, 22"),
                                      ("11", "US TSR 16 CFR 310.3(a)(3)(ii)"),
                                      ("8", "3GPP 28.535 §4.2.3; ETSI ZSM 009-1 §7.2.2.4"),  # Task 33; "TS" dropped to hold 5 pages (Iyas, 2026-10-30)
                                      ("12", "EU Roaming Reg 2022/612 Art 14(4); EU AI Act Art 14(4)(e) (high-risk, from "
                                             "2027)")])
def test_report_global_example_cells_are_the_closer_examples(n, label):
    row = next(line for line in REPORT_MD.read_text(encoding="utf-8").splitlines() if line.startswith(f"| {n} |"))
    assert row.split("|")[-2].strip() == label


def test_report_kb_counts_are_read_from_the_manifest():
    build = _load()
    text = REPORT_MD.read_text(encoding="utf-8")
    assert build.check_kb_counts(text) == []
    assert "holds 108 documents" in text and "100 are verified" in text  # Task 45
    assert "the 36 UAE instruments" in text  # Task 51 stop 1 ruling: the foreign and other-UAE counts moved to Annex A


@pytest.mark.parametrize("wrong", ["holds 51 documents", "47 are verified", "**SRC-2** 51 documents"])
def test_a_typed_kb_count_that_differs_from_the_manifest_fails(wrong):
    build = _load()
    text = REPORT_MD.read_text(encoding="utf-8")
    right = {"holds 51 documents": "holds 108 documents", "47 are verified": "100 are verified",
             "**SRC-2** 51 documents": "**SRC-2** 108 documents"}[wrong]
    assert right in text
    problems = build.check_kb_counts(text.replace(right, wrong))
    assert len(problems) == 1 and problems[0].startswith(wrong), problems


@pytest.mark.parametrize("typed, ok", [("nine foreign texts", False), ("thirty-eight foreign texts", True),
                                       ("fifteen other UAE texts", False), ("thirty-two other UAE texts", True)])
def test_the_count_check_still_reads_those_words_if_they_come_back(typed, ok):
    """Task 51: the report no longer prints these two counts; the build must still refuse a wrong one."""
    build = _load()
    text = REPORT_MD.read_text(encoding="utf-8") + f"\n\nThere are {typed}.\n"
    assert (build.check_kb_counts(text) == []) is ok


def test_report_build_refuses_a_wrong_kb_count(tmp_path):
    md = tmp_path / "report.md"
    md.write_text(REPORT_MD.read_text(encoding="utf-8").replace("100 are verified", "47 are verified"), encoding="utf-8")
    assert _load().main(["--md", str(md), "--out", str(tmp_path / "r.docx")]) == 1
    assert not (tmp_path / "r.docx").exists()


def test_readme_kb_counts_are_the_manifests():
    readme = (kb.REPO / "README.md").read_text(encoding="utf-8")
    rows = kb.load_manifest()
    count = lambda s: sum(r["status"] == s for r in rows)
    assert (f"\nKnowledge base: {count('VERIFIED')} VERIFIED (text on disk, sha256 matches), {count('REFERENCED')} "
            f"REFERENCED (opened, text not held), {count('UNVERIFIED')} UNVERIFIED") in readme


def test_report_has_no_row_7_gap_7_stays_in_the_register():
    # Task 31 C: gap 7 is out of the report's table (since Task 25); Iyas 2026-10-30: leave it out, the register
    # and the site carry Utah and Moffatt
    assert not any(line.startswith("| 7 |") for line in REPORT_MD.read_text(encoding="utf-8").splitlines())


# --- order 2026-10-30-task-32-operator-codes, Part C ----------------------------------------------------------

def test_report_row_1_names_dus_chatbot_channel_and_no_operator_is_said_to_break_anything():
    text = REPORT_MD.read_text(encoding="utf-8")
    row = next(line for line in text.splitlines() if line.startswith("| 1 |"))
    # Task 34 A4 cut (b), Iyas: the du clause left the report row for space; the register keeps du's chatbot channel
    assert "chatbot" not in row.split("|")[2]
    assert "The code names a chatbot as a complaint channel and sets no rule for it." in         (DOCS / "gaps.md").read_text(encoding="utf-8")
    assert not re.search(r"(\be&|\bdu\b|\bEtisalat\b|\bEITC\b)[^.\n]{0,80}\b(breach|break|violat|fail)", text)


def test_task_33_line_26_names_two_unpublished_texts_and_one_unreachable_one():
    text = REPORT_MD.read_text(encoding="utf-8")
    # Task 51 B: the clause leaves the Introduction; Annex A and the README keep it
    assert "3 UNVERIFIED (unpublished or unreachable; they back no quoted clause" in " ".join(
        (DOCS / "annex.md").read_text(encoding="utf-8").split())
    assert "three unpublished texts" not in text
    rows = kb.load_manifest()
    assert sorted(r["document_id"] for r in rows if r["status"] == "UNVERIFIED") == [
        "cabinet-agentic-ai-framework-2026-05-18", "csc-ai-security-policy-v1-1", "pdpl-executive-regulations"]


def test_task_33_data_office_sentence_is_in_the_readme_once_not_the_report():
    # order Task 33 Part D: in the report only if 5 pages hold; they do not, so README only
    # Task 43 (hq answer 2a): the register's Authority paragraph replaces the README line; still not in the report
    from onyx import gaps
    readme = (kb.REPO / "README.md").read_text(encoding="utf-8")
    assert readme.count(gaps.AUTHORITY_LINE) == 1 and readme.index(gaps.AUTHORITY_LINE) < readme.index("<!-- gap-register:start -->")
    report = REPORT_MD.read_text(encoding="utf-8")
    assert "Federal Authority for Artificial Intelligence" not in report and "Intelligence and Data Authority" not in report


# --- order 2026-10-30 Task 34 Part A: team and links -------------------------------------------------------------

LINKS = ["**GitHub (public from 2026-11-09):** https://github.com/SHRA1M/onyx-hackathon-build",
         "**Replay site, no install:** https://shra1m.github.io/onyx-hackathon-build/site/. **Demo video:** see the "
         "repository README."]  # Iyas's A4 answer (1): five header lines; Task 51 A.2


def test_task_34_team_and_the_four_labelled_links():
    lines = REPORT_MD.read_text(encoding="utf-8").splitlines()
    assert lines[3] == "**Team members:** Mohammed Rawashdeh, Yanal Faouri"
    assert lines[5:7] == LINKS
    assert not any(line.startswith("**GitHub link:**") for line in lines)
    for path in (REPORT_MD, kb.REPO / "README.md"):
        assert "Saaydeh" not in path.read_text(encoding="utf-8"), path


def test_the_template_example_team_never_appears_in_report_readme_or_site():
    # hq, 2026-11-01: the filed Task 36 order may quote the template's example team; nothing a reader sees may
    name = bytes([86, 105, 115, 104, 110, 117]).decode()  # spelled by code so this file does not carry it
    paths = [DOCS / "report.md", kb.REPO / "README.md", *sorted((DOCS / "site").glob("*.html"))]
    assert all(name not in p.read_text(encoding="utf-8") for p in paths)
    with zipfile.ZipFile(DOCS / "report.docx") as z:
        assert name not in z.read("word/document.xml").decode("utf-8")


# --- Task 37 item 1 (order 2026-11-02-task-37-audit-fixes) -----------------------------------------------------

def test_no_numbered_section_pointer_into_the_report():
    """README, the site and the datasheet name a report section by its heading, never by a number (Task 36 renumbered
    them). Only pointers into the report count: a law's or a source note's own sections are left alone."""
    repo = kb.REPO
    files = [repo / "README.md", repo / "kb" / "DATASHEET.md", *sorted((repo / "docs" / "site").glob("*.html"))]
    pointer = re.compile(r"report(\.docx|\.md)?[^.;\n<]{0,40}?\bsections?\s+\d", re.IGNORECASE)
    hits = [f"{f.name}: {m.group(0)}" for f in files for m in pointer.finditer(f.read_text(encoding="utf-8"))]
    assert hits == []


# Task 44: the knowledge base reached thirty other UAE texts; a round tens word must read as its number
@pytest.mark.parametrize("word,value", [("thirty", 30), ("twenty", 20), ("thirty-eight", 38), ("nine", 9)])
def test_a_round_tens_word_reads_as_its_number(word, value):
    assert _load()._number(word) == value


# --- order 2026-11-04 Task 48, ruling task-48-stop-1: the report states the check that runs ---------------------------


def test_task_48_gap_2_cell_is_the_rulings_and_the_claim_matches_what_ci_checks():
    report = REPORT_MD.read_text(encoding="utf-8")
    assert ('| 2 | Consent elicited by an AI: the CPR sets the consent safeguard by sales medium (4.17.3, 4.22.3, 4.23.2) '
            'and names no AI channel, so an agent\'s safeguard follows where it is embedded; whether a "yes" the agent '
            'itself heard and interpreted is a positive affirmative action (4.7.1), or consent "in writing or '
            'electronically" under the PDPL (6(1)(b)), is unsaid | coordination |') in report
    flat = " ".join(report.split())
    assert "clause the gates cite word for word against the text stored from it" in flat
    annex = " ".join((kb.REPO / "docs" / "annex.md").read_text(encoding="utf-8").split())
    assert ("the clause's quote is checked against the stored clause text on every push, and the stored text against "
            "the issuer's file by hash where it is on disk") in annex
    for html in ("docs/replay/index.html", "docs/site/runs.html"):
        page = (kb.REPO / html).read_text(encoding="utf-8")
        assert ('<p class="meta">Rule quotes on this page are checked word for word against their stored clauses on '
                "every push; in a governed run the gate must find the agent's quote verbatim in a cited clause before it "
                'can allow a proposal, and "Without the gates" shows proposals no gate checked; an "Elsewhere" quote is '
                "checked against its source file where that file is on disk; <code>kb verify</code> checks each stored "
                "source against the issuer's file by SHA-256 where the file is on disk; to check a run's log chain "
                'yourself: <a href="../site/verify.html">verify</a>.</p>') in page, html  # hq, addendum 2, item 2
        assert "Every quote on this page" not in page, html
        assert "against the issuer's file on every push" not in page, html


# --- hq, task-48-addendum-2-claims-2026-11-04, items 1 and 3 -------------------------------------------------------


def test_task_48_addendum_2_clause_4_10_keeps_both_exceptions():
    row = next(r for r in data.load_gaps()["gaps"] if r["id"] == "gap-2")
    assert "and 2FA in all digital applications unless objectively justified or expressly specified otherwise (4.10)" in row["gap"]
    [line] = [s for s in row["searched"] if s["clause"] == "tdra-cpr-v2-en:4.10"]
    assert line["says"] == "Digital applications: multi-step, 2FA unless objectively justified or expressly specified otherwise."


def test_task_48_addendum_2_check_data_says_what_it_reads(capsys):
    assert data.check_data() == 0
    assert "check-data ok: every rule and mandate quote verbatim, every rule cites a clause" in capsys.readouterr().out

