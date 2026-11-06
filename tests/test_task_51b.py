"""Task 51b (order D:\\Projects\\hq\\uni\\ai-for-good-hackathon\\task-51b-order-2026-11-05.md): the four items held for
Iyas's five Arabic blocks. Every Arabic string here was eye-checked by him on its page, 2026-11-05."""
import json
import re
from html import escape

import pytest
from docx import Document
from docx.oxml.ns import qn
from pypdf import PdfReader

from onyx import data, kb

NOTE = ("The English 26.7.2 is an active prohibition ('preclude'). The Arabic is a passive exclusion, 'excepted or "
        "excluded from them', whose antecedent is the chapeau, 'the provisions of sub-article 26.6', a duty to keep "
        "trained personnel for complaints. TDRA's own English rendering reads the exclusion as a bar, and licence 9.1 "
        "(Arabic binding, licence 16.7) independently requires trained personnel to receive and respond to complaints. "
        "The CPR does not say which language prevails. Mizan enforces the stricter reading, citing 26.7.2 and "
        "licence 9.1; the chapeau is quoted here and holds no rule.")
CLAUSES = [
    ("26.6", 50, "Licensees shall maintain an adequate number of properly trained personal to receive, process, and "
                 "respond to Consumer Complaints in a timely and prompt manner.",
     "يجب على المرخص لهم الحفاظ على عدد كافٍ من الموظفين المدربين تدريباً مناسباً لاستقبال ومعالجة والرد على الشكاوى "
     "المقدمة من المستهلكين في الوقت المناسب وبالسرعة اللازمة."),
    ("26.7", 51, "The provisions of sub-article 26.6:", "أحكام المادة الفرعية26.6:"),
    ("26.7.1", 51, "apply in all cases regardless of which Mandatory Channel is used; and",
     "تسري في كل الحالات بغض النظر عن القناة الإلزامية المستخدمة؛ و"),
    ("26.7.2", 51, "preclude the use of non-human agents by Licensees in conversations with Consumers regarding "
                   "Consumer Complaints.",
     "يستثنى أو يستبعد منها استخدام وكلاء غير بشريين من قبل المرخص لهم في المحادثات مع المستهلكين بشأن الشكاوى المقدمة "
     "من قبلهم."),
]
LICENCE_9_1_AR = ("على المرخص له توفير ما يلزم من موظفين مدربين لتلقي والإجابة دون إبطاء على الشكاوى والمنازعات الخاصة "
                  "بالمشتركين، كما يتعين عليه إتخاذ جميع الإجراءات المعقولة للمعالجة الآنية ولتجنب تكرارأسباب الشكاوى "
                  "ونزاعاتهم ذات العلاقة بجودة الخدمة وتوفرها وتسليمها وفوترتها.بالإضافة إلى ذلك، يتعين على المرخص له "
                  "إتخاذ جميع التدابير الضرورية لضمان أداء المبالغ المستحقة للمشتركين وبشكل كامل.")
LICENCE_FILE = "docs/sources/licence-2-2026-ar-9.1-full-checked.txt"
CABINET_AR = ("ويصدر مجلس الوزراء قراراً بجدول المخالفات والغرامات التي توقع على المرخص لهم وبما لا يزيد على (10.000.000) "
              "عشرة ملايين درهم عن كل مخالفة.")
TENSION = ("Two duties meet at that moment: licence 9.1 has complaints answered «دون إبطاء» (without delay; the English "
           "text reads \"promptly\"; the Arabic binds, licence 16.7), and Trade Law 14/2023 Art 6(7) has complaint means "
           "\"always available without interruption with qualified staff\"; neither sets a hand-over or a time.")


def _row(gap_id):
    return next(r for r in data.load_gaps()["gaps"] if r["id"] == gap_id)


def _squeezed(path, page):
    if not (kb.REPO / path).exists():
        pytest.skip(f"{path} is local only")
    return re.sub(r"\s+", "", PdfReader(kb.REPO / path).pages[page - 1].extract_text())


def _annex_section(letter):
    annex = (kb.REPO / "docs" / "annex.md").read_text(encoding="utf-8")
    return re.split(r"^## Annex [A-F]\.", annex, flags=re.M)["ABCDEF".index(letter) + 1]


def test_the_four_clause_note_is_in_gap_1_with_both_languages():
    note = _row("gap-1")["clause_note"]
    assert note["note"] == NOTE
    assert [(c["clause"], c["page_ar"], c["en"], c["ar"]) for c in note["clauses"]] == CLAUSES
    assert {c["page"] for c in note["clauses"]} == {65}


@pytest.mark.parametrize("clause,page,en,ar", CLAUSES)
def test_the_note_quotes_are_on_their_pages(clause, page, en, ar):
    assert re.sub(r"\s+", "", ar) in _squeezed("kb/sources/tdra-cpr-v2-ar.pdf", page)
    assert re.sub(r"\s+", "", en) in _squeezed("kb/sources/tdra-cpr-v2-en.pdf", 65)


@pytest.mark.parametrize("clause,page,en,ar", [c for c in CLAUSES if c[0] != "26.7"])
def test_the_note_quotes_are_verbatim_in_the_committed_chunks(clause, page, en, ar):
    chunk = kb.get_chunk("tdra-cpr-v2-en", clause)
    assert en in chunk["text_en"] and ar in chunk["text_ar"]


def test_the_chapeau_gets_no_rule_and_no_chunk():
    assert len(data.load_rules()) == 109 and not any(r.get("chunk") == "26.7" for r in data.load_rules())
    lines = (kb.KB_DIR / "chunks" / "tdra-cpr-v2-en.jsonl").read_text(encoding="utf-8").splitlines()
    assert "26.7" not in [json.loads(line)["clause"] for line in lines]


def test_the_note_prints_in_the_register_and_the_site():
    md = (kb.REPO / "docs" / "gaps.md").read_text(encoding="utf-8")
    register = md[md.index("gap-1: "):md.index("gap-2: ")]
    html = (kb.REPO / "docs" / "site" / "gaps.html").read_text(encoding="utf-8")
    page = html[html.index('id="gap-1"'):html.index('id="gap-2"')]
    for text in [q for c in CLAUSES for q in c[2:]]:
        assert text in register and escape(text) in page, text
    assert NOTE in register and escape(NOTE) in page


@pytest.mark.parametrize("letter", ["B", "C"])
def test_the_note_is_in_annex_b_and_c(letter):
    section = _annex_section(letter)
    flat = " ".join(section.split())
    assert NOTE in flat
    for _, _, en, ar in CLAUSES:
        assert en in flat and ar in flat


def test_annex_b_prints_it_under_the_rule_sample():
    section = _annex_section("B")
    assert section.index('"jurisdiction": "UAE"') < section.index(NOTE[:40]) < section.index("What the gate does with it")


def test_each_arabic_quote_is_a_right_to_left_paragraph_in_the_word_file():
    # A quote inside an English paragraph came out with its clause number and quote marks scrambled (PDF page image).
    word = Document(kb.REPO / "docs" / "report.docx")
    for _, _, _, ar in CLAUSES:
        found = [p for p in word.paragraphs if p.text == ar]
        assert len(found) == 2, ar
        for p in found:
            assert p._p.pPr.find(qn("w:bidi")) is not None
            assert all(r._r.rPr.find(qn("w:rtl")) is not None for r in p.runs)


def test_the_note_stays_out_of_the_report_body():
    body = (kb.REPO / "docs" / "report.md").read_text(encoding="utf-8")
    assert "antecedent" not in body and "أحكام المادة الفرعية" not in body


def test_the_9_1_entry_quotes_the_full_arabic_from_the_new_file():
    [entry] = [s for s in _row("gap-1")["searched"] if s["clause"] == "licence-2-2026:9.1"]
    assert (entry["quote_ar"], entry["file_ar"], entry["page_ar"]) == (LICENCE_9_1_AR, LICENCE_FILE, 22)
    held = (kb.REPO / LICENCE_FILE).read_text(encoding="utf-8")
    assert held.splitlines()[-1] == LICENCE_9_1_AR
    assert re.sub(r"\s+", "", LICENCE_9_1_AR) in _squeezed("kb/sources/licence-2-2026.pdf", 22)


def test_the_licence_rule_and_chunk_stay():
    rule = next(r for r in data.load_rules() if r["id"] == "licence-9-1")
    assert rule["quote_ar"] == "توفير ما يلزم من موظفين مدربين"
    assert kb.get_chunk("licence-2-2026", "9.1")["text_ar"] == "توفير ما يلزم من موظفين مدربين"


def test_gap_15_quotes_the_cabinet_sentence_not_the_board_sentence():
    row = _row("gap-15")["searched"][1]
    assert row["quote"].startswith("The Cabinet shall issue a resolution")
    assert (row["quote_ar"], row["file_ar"], row["page_ar"]) == (CABINET_AR, "kb/sources/telecom-law-3-2003-ar.pdf", 24)
    for path in ("docs/gaps.md", "docs/site/gaps.html", "onyx/data/gaps.json"):
        text = (kb.REPO / path).read_text(encoding="utf-8")
        assert "لمجلس الإدارة توقيع غرامات إدارية" not in text and CABINET_AR in text, path


def test_gap_1_prints_the_tension_arabic_first():
    position = _row("gap-1")["uae_position"]
    assert TENSION in position
    assert position.index("دون إبطاء") < position.index('"promptly"')
    assert position.endswith("and a reference number is not a conversation.")
