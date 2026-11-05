"""Task 38 (order D:\\Projects\\hq\\uni\\ai-for-good-hackathon\\task-38-annex-order-2026-11-02.md, ruling
task-38-stop-1-ruling-2026-11-02.md): docs/annex.md is hq's annex text v3 with every brace filled from the repo; the
builder appends it to docs/report.docx after a page break and checks its figures; the Limits paragraph points to it."""

import importlib.util
import json
import re
import subprocess
import sys

import pytest

from onyx import kb

DOCS = kb.REPO / "docs"
ANNEX_MD = DOCS / "annex.md"
REPORT_MD = DOCS / "report.md"
POINTER = (" Annex A to F: data and model, clause to code, the governed test, what ITU can reuse, where to look, "
           "further gaps and candidates.")  # Task 41: Annex F added


def _load():
    spec = importlib.util.spec_from_file_location("build_report", DOCS / "build_report.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _annex() -> str:
    return ANNEX_MD.read_text(encoding="utf-8")


def _code_blocks(md: str) -> list[str]:
    return re.findall(r"^```\n(.*?)\n```$", md, re.S | re.M)


def test_annex_headings_are_a_to_f_in_order():
    headings = re.findall(r"^## (Annex [A-Z])\. ", _annex(), re.M)
    assert headings == ["Annex A", "Annex B", "Annex C", "Annex D", "Annex E", "Annex F"], "Task 41 adds Annex F"


def test_no_brace_is_left_in_the_annex():
    assert "{build:" not in _annex()


def _c3_rows(results: str) -> dict[str, list[str]]:
    """Scenario -> [ungoverned claims en, ar, governed gate rejection en, ar], as printed in eval/results.md."""
    rows: dict[str, dict[str, str]] = {}
    for heading, column in (("## Governed", "Gate rejection"), ("## Ungoverned", "Ungoverned claims allowed")):
        section = results[results.index(heading + "\n"):]
        lines = [l for l in section.splitlines() if l.startswith("|")]
        head = [c.strip() for c in lines[0].strip("|").split("|")]
        for line in lines[2:12]:
            cells = dict(zip(head, (c.strip() for c in line.strip("|").split("|"))))
            rows.setdefault(cells["Scenario"], {})[f"{column} {cells['Lang']}"] = cells[column]
    return {s: [r["Ungoverned claims allowed en"], r["Ungoverned claims allowed ar"], r["Gate rejection en"],
                r["Gate rejection ar"]] for s, r in rows.items()}


def test_the_c3_rows_in_the_annex_table_equal_eval_results():
    expected = _c3_rows((kb.REPO / "eval" / "results.md").read_text(encoding="utf-8"))
    table = [l for l in _annex().splitlines() if re.match(r"\| S[1-5] \|", l)]
    got = {c[0]: c[1:] for c in ([x.strip() for x in l.strip("|").split("|")] for l in table)}
    assert list(got) == ["S1", "S2", "S3", "S4", "S5"]
    assert got == expected


def test_the_rule_record_pasted_equals_the_one_in_rules_json():
    rules = json.loads((kb.REPO / "onyx" / "data" / "rules.json").read_text(encoding="utf-8"))["rules"]
    stored = next(r for r in rules if r["id"] == "cpr-26-7-2")
    assert json.loads(_code_blocks(_annex())[0]) == stored


def test_the_gate_sketch_is_complaint_gate_lines_unedited():
    gate = (kb.REPO / "onyx" / "gate.py").read_text(encoding="utf-8").splitlines()
    sketch = _code_blocks(_annex())[1].splitlines()
    assert sketch[0] == "def complaint_gate(p: Any, s: State, kb: Knowledge) -> Verdict | None:"
    assert len(sketch) <= 40
    body = gate[gate.index(sketch[0]):]
    body = body[:next(i for i, l in enumerate(body[1:], 1) if l and not l.startswith(" "))]
    kept = [l for l in sketch if l.strip() != "..."]
    at = 0
    for line in kept:  # each kept line is a line of the function, in the function's order
        at = body.index(line, at) + 1
    assert any("_finding(BLOCK" in l for l in kept) and any("grievance_expressed" in l for l in kept)


def test_the_pointer_sentence_closes_the_limits_paragraph():
    md = REPORT_MD.read_text(encoding="utf-8")
    limits = md[md.index("## Limits and next steps"):]
    para = " ".join(limits.split("\n\n")[1].split())
    assert para.endswith("(practice, not legal advice)." + POINTER)  # Task 51 I(f)


def test_the_example_team_is_absent_from_the_annex():
    name = bytes([86, 105, 115, 104, 110, 117]).decode()  # as in test_report.py
    assert name not in _annex()


def test_the_result_paragraph_carries_a_c3_tag_and_passes_the_value_check():
    build = _load()
    paras = build.annex_paragraphs(_annex())
    result = next(p for p in paras if p.startswith("**Result.**"))
    assert build.tags(result) == ["C3"]
    results = (kb.REPO / "eval" / "results.md").read_text(encoding="utf-8")
    assert build.check_values("", results, paras) == []
    assert build.check_values("", results, [result.replace("2.33", "2.34")]) != []


def test_the_precision_paragraph_figures_are_the_pooled_and_misses_lines():
    results = (kb.REPO / "eval" / "results.md").read_text(encoding="utf-8")
    pooled = re.search(r"^Pooled over both languages \(C5\): action recall (\d+ of \d+) key steps, 95% interval "
                       r"([\d.]+ to [\d.]+); citation validity (\d+ of \d+) citing proposals, 95% interval "
                       r"([\d.]+ to [\d.]+)\.", results, re.M)
    para = " ".join(_annex()[_annex().index("**Precision of the headline figures.**"):].split("\n\n")[0].split())
    assert f"action recall {pooled[1]} key steps, 95% interval {pooled[2]}," in para
    assert f"citation validity {pooled[3]}, 95% interval {pooled[4]}." in para
    misses = re.findall(r"^\| (S\d-\d) \| \w+ \| \w+ \| (\d of \d) \| \d of \d \|$", results, re.M)
    assert misses == [("S3-4", "1 of 2"), ("S4-4", "1 of 2")]
    assert "S3-4" in para and "S4-4" in para and "each missed in 1 of 2 runs" in para


@pytest.mark.parametrize("old, new", [("108 documents in", "107 documents in"), ("100 are VERIFIED", "101 are VERIFIED"),  # Task 45: 108, 100
                                      ("5 REFERENCED", "6 REFERENCED"), ("3 UNVERIFIED", "4 UNVERIFIED"),
                                      ("36 UAE instruments", "37 UAE instruments"),
                                      ("38 foreign texts", "39 foreign texts")])
def test_annex_a_kb_counts_are_read_from_the_manifest(old, new):
    build = _load()
    annex = _annex()
    assert old in annex
    assert build.check_kb_counts(annex, build.ANNEX_KB_COUNTS) == []
    assert build.check_kb_counts(annex.replace(old, new), build.ANNEX_KB_COUNTS) != []


def test_uae_instruments_leave_out_web_pages_and_announcements():
    """Task 40 (hq answer to stop 1, option a): a UAE instrument is a distinct `instrument` of a UAE manifest row that
    is neither a web page nor an announcement, as those rows' own notes say. Annex A names the two rows left out."""
    build = _load()
    rows = [r for r in kb.load_manifest() if r["jurisdiction"] == "UAE"]
    left_out = sorted(r["document_id"] for r in rows if r["source_type"] in build.NOT_INSTRUMENTS)
    assert left_out == ["albayan-arabic-law-2026-04-29", "fed-ai-data-authority-2026-06-14", "tdra-dispute-service-page",
                        "tdra-faqs", "uaepass-docs-account-levels",
                        "wam-2026-06-14-ai-data-authority",
                        "wam-2026-08-21-agentic-ai-guide"]  # Task 44: two web pages and a news report; Task 45: this article
    assert all("not an instrument" in r["notes"] or "not a law" in r["notes"] for r in rows
               if r["source_type"] in build.NOT_INSTRUMENTS)
    count = len({r["instrument"] for r in rows if r["source_type"] not in build.NOT_INSTRUMENTS})
    # Task 45: the WAM article shares its guide's instrument, which stays counted, so it takes nothing off
    assert count == 36 == len({r["instrument"] for r in rows}) - (len(left_out) - 1)
    annex = " ".join(_annex().split())
    assert f"{count} UAE instruments" in annex
    assert ("plus three web pages (a TDRA service page, TDRA's FAQs, the UAE PASS documentation), three announcements and "
            "a news report, which are not instruments") in annex


def test_the_counts_stated_in_the_annex_are_the_repos():
    annex = " ".join(_annex().split())
    rules = json.loads((kb.REPO / "onyx" / "data" / "rules.json").read_text(encoding="utf-8"))["rules"]
    mandates = json.loads((kb.REPO / "onyx" / "data" / "mandates.json").read_text(encoding="utf-8"))["agents"]
    chunks = [json.loads(l) for f in sorted((kb.REPO / "kb" / "chunks").glob("*.jsonl"))
              for l in f.read_text(encoding="utf-8").splitlines() if l.strip()]
    files = list((kb.REPO / "kb" / "chunks").glob("*.jsonl"))
    assert f"{len(chunks)} committed chunks across {len(files)} documents" in annex
    assert f"`rules.json` ({len(rules)} rules)" in annex
    docs = {a: len(m["documents"]) for a, m in mandates.items()}
    assert (f"(care {docs['care']} documents, adviser {docs['adviser']}, TDRA {docs['tdra']}, Data Office "
            f"{docs['data_office']}, coordinator {docs['coordinator']})") in annex
    uae_docs = {r["document_id"] for r in rules if r["jurisdiction"] == "UAE"}
    assert f"({len(rules)} rules over {len(uae_docs)} UAE documents)" in annex
    arabic = sum(1 for c in chunks if c.get("text_ar", "").strip())
    assert f"({arabic} chunks with `text_ar`)" in annex
    assert f"and {len(list((kb.REPO / 'runs' / 'c5').glob('*/ar/*.jsonl')))} recorded Arabic runs" in annex
    collected = subprocess.run([sys.executable, "-m", "pytest", "--collect-only", "-q", "tests/test_gate.py"],
                               capture_output=True, text=True, cwd=kb.REPO).stdout
    assert f"({re.search(r'(\d+) tests? collected', collected)[1]} gate tests" in annex


def test_the_built_report_has_the_annex_after_a_page_break(tmp_path):
    out = tmp_path / "report.docx"
    result = subprocess.run([sys.executable, str(DOCS / "build_report.py"), "--out", str(out)],
                            capture_output=True, text=True, encoding="utf-8", cwd=kb.REPO)
    assert result.returncode == 0, result.stdout + result.stderr
    from docx import Document
    doc = Document(str(out))
    texts = [p.text for p in doc.paragraphs]
    annex = texts.index("Annex")
    assert texts[annex - 1].startswith("Limits and next steps.") and texts[annex - 1].endswith(POINTER.strip())
    assert doc.paragraphs[annex]._p.pPr.find(
        "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}pageBreakBefore") is not None
    leads = [t for t in texts[annex:] if re.match(r"Annex [A-F]\. ", t)]
    assert [t[:8] for t in leads] == ["Annex A.", "Annex B.", "Annex C.", "Annex D.", "Annex E.", "Annex F."]
    assert len(doc.tables) == 5  # the strip (Task 51 B), mapping, gaps, the C3 table, where to look
    code = next(p for p in doc.paragraphs[annex:] if p.text.startswith("def complaint_gate"))
    assert all(r.font.size.pt == 8 and r.font.name == "Courier New" for r in code.runs)


def test_annex_c_handover_sentences_match_the_c5_cells():
    """Task 39 D (ruling task-39-stops-ruling-2026-11-02, D3 and D4): Annex C names S2, S4, S5 at 0 steps in both
    languages and S1, S3 with no hand-over step, as the C5 cells in eval/results.json print them."""
    text = " ".join(ANNEX_MD.read_text(encoding="utf-8").split())
    assert ("In the three scored scenarios that contain a hand-over (S2, S4, S5) the hand-over latency row in "
            "`eval/results.md` is 0 steps in both languages: the run hands over at the key's step, not later; S1 and "
            "S3 have no hand-over step.") in text
    cells = json.loads((kb.REPO / "eval" / "results.json").read_text(encoding="utf-8"))["c5"]["C5"]["by_scenario"]
    for sid, value in {"S1": None, "S2": 0, "S3": None, "S4": 0, "S5": 0}.items():
        assert [cells[sid][lang]["handover_latency_steps"] for lang in ("en", "ar")] == [value, value], sid
    assert "## Key clauses shown and hand-over latency (C5)" in (kb.REPO / "eval" / "results.md").read_text(
        encoding="utf-8")


def test_annex_a_retrieval_sentence_carries_the_printed_key_clause_figures():
    """Ruling 2 (task-39-stops-ruling-2-2026-11-02, B5): the Annex A sentence after "exactly what the model was
    shown." carries the pooled key-clause figures eval/results.json holds and results.md prints."""
    text = " ".join(_annex().split())
    pooled = json.loads((kb.REPO / "eval" / "results.json").read_text(encoding="utf-8"))["c5"]["key_clauses"]["pooled"]
    en, ar = pooled["en"], pooled["ar"]
    assert en["mandate"] == ar["mandate"] and en["total"] == ar["total"]
    shown = (
        f"was shown. Over the scored runs, {en['shown']} of {en['total']} key clauses were in what the model was "
        f"shown in English and {ar['shown']} of {ar['total']} in Arabic; {en['mandate']} of {en['total']} came from "
        "the mandate list alone, which is the English-centred retriever at work, and why the mandate list comes "
        "first.")
    carried = (  # Task 47, hq ruling item 1 puts the "Retrieval alone" sentence between the two
        f" Of the clauses absent at a step that still scored, {en['carried']} in English and {ar['carried']} "
        "in Arabic were carried by the gate's verdict in code; the rest sit on abstention steps, where the key names "
        "the clauses the gap is about and the adviser's act is to flag the gap, not to cite them, except two clauses "
        "at one Arabic step (S3-1) that the English run retrieved and the Arabic run did not.")
    assert shown in text and carried in text and text.index(shown) < text.index(carried)
    md = " ".join((kb.REPO / "eval" / "results.md").read_text(encoding="utf-8").split())
    for lang, cell in pooled.items():
        assert f"of the {cell['absent']} not shown at a step that scored, {cell['carried']} carried by the gate's verdict" in md


def _retrieval_pooled() -> dict[tuple[str, str], str]:
    """(embedder section, lang) -> the printed recall@8 share of the Pooled row in "Retrieval alone"."""
    results = (kb.REPO / "eval" / "results.md").read_text(encoding="utf-8")
    section = results[results.index("## Retrieval alone"):results.index("## Tokens and cost")]
    shipped, bilingual = section.split("### Bilingual embedder")
    return {(name, lang): re.search(rf"^\| Pooled \| {lang} \| \d+ of \d+ \(([\d.]+)\) \|", text, re.M)[1]
            for name, text in (("shipped", shipped), ("bilingual", bilingual)) for lang in ("en", "ar")}


def test_annex_a_retrieval_alone_sentence_equals_the_printed_figures():
    """Task 47, hq ruling task-47-stop-1-ruling-2026-11-04 item 1: hq's sentence, after "why the mandate list comes
    first.", every number a printed value in eval/results.md."""
    p = _retrieval_pooled()
    assert (p["shipped", "en"], p["shipped", "ar"], p["bilingual", "en"], p["bilingual", "ar"]) == (
        "0.24", "0.09", "0.24", "0.15")
    sentence = (
        "and why the mandate list comes first. Measured alone on the same key steps, with no model call and no mandate "
        f"list, the shipped embedder finds {p['shipped', 'en']} of the key clauses in English and {p['shipped', 'ar']} "
        "in Arabic at top 8; a bilingual embedder (multilingual-e5-small, in no scored run) finds "
        f"{p['bilingual', 'en']} and {p['bilingual', 'ar']}, with overlapping Arabic intervals (`eval/results.md`, "
        '"Retrieval alone"). Of the clauses absent')
    assert sentence in " ".join(_annex().split())
    results = (kb.REPO / "eval" / "results.md").read_text(encoding="utf-8")
    bilingual = results[results.index("### Bilingual embedder"):]
    shipped_low, shipped_high = re.search(r"^\| Pooled \| ar \| [^|]+\| ([\d.]+) to ([\d.]+) \|", results[
        results.index("### Shipped embedder"):], re.M).groups()
    bilingual_low, bilingual_high = re.search(r"^\| Pooled \| ar \| [^|]+\| ([\d.]+) to ([\d.]+) \|", bilingual,
                                              re.M).groups()
    assert float(bilingual_low) <= float(shipped_high) and float(shipped_low) <= float(bilingual_high)


def test_annex_a_no_longer_calls_a_bilingual_embedder_the_obvious_upgrade():
    """Task 47, hq ruling item 2: the measurement does not support those words."""
    text = " ".join(_annex().split())
    assert "obvious upgrade" not in text and "its Arabic retrieval is weak" not in text
    assert ("is an English sentence embedder; measured alone it is weak in both languages, and weaker in Arabic "
            "(Retrieval below).") in text
    assert ("A bilingual embedder is listed under next steps; the one measured before the freeze (Retrieval below) is "
            "not a clear gain, so the upgrade is a larger model or a retrieval redesign, and neither was made before "
            "the freeze because it would have meant re-recording the scored runs.") in text


def test_the_results_method_lines_say_what_stays_open_and_the_annex_does_not():
    """Task 47, hq ruling, "Accepted as built": one method line each; the annex carries neither."""
    results = (kb.REPO / "eval" / "results.md").read_text(encoding="utf-8")
    assert "- retrieval alone, not diagnosed: why the figures of both embedders are low.\n" in results
    assert ("- retrieval alone, not measured: `intfloat/multilingual-e5-base` and `BAAI/bge-m3`; the bilingual table is "
            "`intfloat/multilingual-e5-small` only.\n") in results
    assert "not diagnosed" not in _annex().lower() and "bge-m3" not in _annex() and "e5-base" not in _annex()


def test_the_readme_names_the_measurement_and_its_figures():
    """Task 47, hq ruling item 3: the clause in the Knowledge base evidence cell. Task 51 A.6 appends the figures, so
    the "no number" of that ruling gives way to the order's sentence, copied from eval/results.md."""
    readme = (kb.REPO / "README.md").read_text(encoding="utf-8")
    row = next(l for l in readme.splitlines() if l.startswith("| Knowledge base |"))
    evidence = row.split(" | ")[1]
    assert evidence.endswith('; retrieval measured on its own, no model: `eval/results.md`, section "Retrieval alone"; '
                             "the running system shows the model 186 of 234 key clauses in English and 166 in Arabic "
                             "(mandate list first); the embedder alone finds 0.24 / 0.09 at top 8")
    assert "## Retrieval alone" in (kb.REPO / "eval" / "results.md").read_text(encoding="utf-8")
    results = (kb.REPO / "eval" / "results.md").read_text(encoding="utf-8")
    assert "| Pooled | en | 29 of 123 (0.24) |" in results and "| Pooled | ar | 11 of 123 (0.09) |" in results


def test_annex_f_quotes_are_the_registers_and_its_dates_are_iso():
    """Task 41: every quoted phrase in Annex F is in docs/gaps.md (generated from gaps.json, whose quotes the gap tests
    check against the held texts); absence is the portal's, never a fact about the world."""
    annex = _annex()
    f = " ".join(annex[annex.index("## Annex F."):].split())
    register = " ".join((kb.REPO / "docs" / "gaps.md").read_text(encoding="utf-8").split())
    quotes = [q for q in re.findall(r'"([^"]+)"', f) if len(q) > 30]
    assert len(quotes) >= 15
    for q in quotes:
        assert q.rstrip(".") in register, q
    assert not re.search(r"never issued|never-issued|does not exist", f)
    assert "not on the official portal on 2026-11-02" in f
    for lead in ("**F.1 Gap 7:", "**F.2 Gap 13:", "**F.3 Gap 14:", "**F.4 Gap 15:", "**F.5 Candidates",
                 "**F.6 Searched, nothing found.**"):
        assert lead in f, lead
