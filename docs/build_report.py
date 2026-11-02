"""The report builder (order 2026-10-23-task-12-report-build items 2 and 3): writes docs/report.docx from
docs/report.md on docs/report-template.docx. Every figure in a paragraph tagged `[C5, ...]` or `[C3, ...]` is checked
against eval/results.md first; one that matches no value of the run set the paragraph's tags name fails the build.

Rendering: the template's title paragraph and its six numbered ListParagraph headings are kept, their text replaced,
and two copies of one carry the sections the template lists unnumbered (Task 36);
the header lines become five paragraphs with the labels in bold; every template example and NOTE paragraph goes. Body
paragraphs are Normal with the template's body run (Times New Roman, justified); markdown bold becomes bold runs,
backticks are dropped, nothing else is interpreted but tables, images and headings. The mapping table reuses the
template's table in place; the gap table is new, with the same table properties. "Limits and next steps" closes
section 6 under a bold lead, with no heading. Run-set tags are stripped. Task 18 item 2: table cells 10 pt with no
space before or after, both figures 11 cm wide (Task 36 stop 2 ruling), picture paragraphs and the six headings keep with next. The paragraph after each table is a 4 pt spacer (run 4 pt,
line exactly 4 pt, no space before or after; Task 36 stop 2 ruling). Fixed core dates and zip times make two
builds byte-identical.

Value check (item 3, hq rulings 1 and 2 of 2026-10-23): in each tagged paragraph every token holding a digit is
  - a list marker, a single digit alone in brackets: skipped;
  - an id, letters then a digit (S1, S3-4, C5, v3): skipped;
  - "N of M": a pair in the run set (C5: the Misses line's M minus N, and N of M itself; the Pooled line's counts;
    the gaps-against-keys line's N of M);
  - "N missed" and "N unexpected": the gaps-against-keys line's counts (C5, Task 29 Part D);
  - "95% interval L to H": the Wilson interval of a Pooled line count (C5), rounded to each bound's decimals; a bound
    that rounds to 1.00 while misses exist fails: write it with three decimals (Iyas, 2026-10-30);
  - a number with a unit (ms, s, decisions, calls): a value with that unit, ms shown as s allowed, rounded to the
    token's decimals;
  - a two-decimal number from 0.00 to 1.00, or a plain decimal outside it: a unitless value, rounded likewise;
  - anything else: "cannot classify", and the build fails.
Values come from the Governed and Ungoverned tables and their latency lines (C3), the "C3, C4 and C5" table and the
per-scenario C3 / C4 / C5 table (C3 and C5 columns), and the Misses, Pooled and gaps-against-keys lines (C5). A paragraph with both tags is checked sentence by sentence, each against its own tag.

Annex (order 2026-11-02 Task 38 item 3): docs/annex.md follows the report after a page break, under "Annex" in the
template's heading (its numbering removed); the five sections "Annex A." to "Annex E." are bold leads (the template
has no second-level heading); body and list text 10 pt, code blocks Courier New 8 pt, tables as above. The annex
passes the same value check and the knowledge-base counts of Annex A (ANNEX_KB_COUNTS).

    uv run python docs/build_report.py [--md docs/report.md] [--annex docs/annex.md] [--out docs/report.docx]
"""

import argparse
import copy
import datetime as dt
import io
import re
import sys
import zipfile
from dataclasses import dataclass, field
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt
from docx.table import Table
from docx.text.paragraph import Paragraph

from onyx import kb
from onyx.eval import wilson

REPO = Path(__file__).resolve().parent.parent
TEMPLATE = REPO / "docs" / "report-template.docx"
REPORT_MD = REPO / "docs" / "report.md"
REPORT_DOCX = REPO / "docs" / "report.docx"
ANNEX_MD = REPO / "docs" / "annex.md"
ANNEX = "Annex"
ANNEX_SECTIONS = ["Annex A.", "Annex B.", "Annex C.", "Annex D.", "Annex E."]
ANNEX_SIZE = Pt(10)
CODE_SIZE = Pt(8)
MONO = "Courier New"
RESULTS = REPO / "eval" / "results.md"
MAPPING = "Mapping with ITU-T Y.3172, Readiness 2.0 Report, and domain-specific policies"
SECTIONS = ["Introduction", "Description of the use case", "What is the role played by AI?", "Requirements", MAPPING,
            "Demo scenarios", "Error scenarios", "Policy gaps and standards gaps derived from the mapping exercise"]
# order 2026-11-01-task-36 item 1: the template's six numbered headings carry six sections; the two the template
# lists as plain lines ("What is the role played by AI?", "Demo scenarios") get a copy of a numbered heading
ADDED = {"What is the role played by AI?", "Demo scenarios"}
TAIL = "Limits and next steps"
FIGURE_WIDTH = {"docs/fig/fig1-architecture.png": Cm(11), "docs/fig/fig2-results.png": Cm(11)}  # Task 36 stop 2 ruling (was 12 cm, Task 36; 16 cm, Task 18 item 2b)
SPACER = Pt(4)  # Task 36 stop 2 ruling: the paragraph after each table, was a full 12 pt body line
FIXED_DATE = dt.datetime(2026, 10, 23, tzinfo=dt.timezone.utc)
ZIP_TIME = (2026, 10, 23, 0, 0, 0)
TABLE_WIDTH = 9359  # the template table's width, dxa
FONT = "Times New Roman"
CELL_SIZE = Pt(10)  # Task 18 item 2a: every table run 10 pt, every cell paragraph 0 pt before and after
CREATOR = "Team Onyx"

TAG = re.compile(r"\s*`\[(C[35])\b[^\]]*\]`")
TOKEN = re.compile(r"(?P<marker>\(\d\)(?![\d.]))"
                   r"|(?P<ident>(?<![\w.])[A-Za-z]+\d[\w-]*)"
                   r"|(?P<interval>(?<![\w.])95% interval (?P<lo>\d\.\d+) to (?P<hi>\d\.\d+))"
                   r"|(?P<count>(?<![\w.])(?P<cv>\d+) (?P<cu>missed|unexpected)\b)"
                   r"|(?P<of>(?<![\w.])(?P<n>\d+) of (?P<m>\d+)(?![\w.]))"
                   r"|(?P<unit>(?<![\w.])(?P<uv>\d+(?:\.\d+)?) (?P<u>ms|s|decisions|calls)\b)"
                   r"|(?P<num>(?<![\w.])\d+(?:\.\d+)?(?![\w]|\.\d))"
                   r"|(?P<other>[^\s()\[\],;:]*\d[^\s()\[\],;:]*)")


# --- the markdown -----------------------------------------------------------------------------------------------

def paragraphs(md: str) -> list[str]:
    """Blank-line separated blocks, soft line breaks joined with a space (table blocks keep their lines)."""
    blocks = [b.strip("\n") for b in re.split(r"\n\s*\n", md) if b.strip()]
    return [b if b.startswith("|") else " ".join(line.strip() for line in b.splitlines()) for b in blocks]


def tags(para: str) -> list[str]:
    return TAG.findall(para)


def strip_tags(text: str) -> str:
    return TAG.sub("", text)


@dataclass
class Report:
    title: str
    header: list[tuple[str, str]]
    sections: dict[str, list[str]] = field(default_factory=dict)


def parse(md: str) -> Report:
    blocks = paragraphs(md)
    if not blocks[0].startswith("# "):
        raise SystemExit("docs/report.md: the first line is not the title")
    header = []
    for line in md.split("\n\n", 2)[1].splitlines():
        m = re.fullmatch(r"\*\*(.+?)\*\* (.+)", line.strip())
        if not m:
            raise SystemExit(f"docs/report.md: header line not '**Label:** value': {line!r}")
        header.append((m.group(1), m.group(2)))
    if len(header) != 5:  # Task 34: the links take two lines (Iyas)
        raise SystemExit("docs/report.md: five header lines expected under the title")
    report, current = Report(blocks[0][2:], header), None
    for block in blocks[2:]:
        if block.startswith("## "):
            current = block[3:]
            if current not in SECTIONS + [TAIL]:
                raise SystemExit(f"docs/report.md: heading {current!r} is not a template section")
            report.sections[current] = []
        elif current is None:
            raise SystemExit(f"docs/report.md: text before the first heading: {block[:60]!r}")
        else:
            report.sections[current].append(block)
    if [s for s in report.sections if s != TAIL] != SECTIONS:
        raise SystemExit(f"docs/report.md: headings {list(report.sections)} not in template order")
    return report


def annex_blocks(md: str) -> list[tuple[str, object]]:
    """docs/annex.md as (kind, content): "section" (an "## Annex X." line, the "## " dropped), "code" (a fenced
    block, verbatim), "table", "list" (numbered items, each joined to one line) or "para"."""
    out, lines, i = [], md.replace("\r\n", "\n").split("\n"), 0
    while i < len(lines):
        if lines[i].startswith("```"):
            end = lines.index("```", i + 1)
            out.append(("code", "\n".join(lines[i + 1:end])))
            i = end + 1
            continue
        block = []
        while i < len(lines) and lines[i].strip() and not lines[i].startswith("```"):
            block.append(lines[i])
            i += 1
        if not block:
            i += 1
            continue
        text = "\n".join(block)
        if text.startswith("## "):
            out.append(("section", text[3:].strip()))
        elif text.startswith("|"):
            out.append(("table", text))
        elif re.match(r"\d+\. ", text):
            items = re.split(r"\n(?=\d+\. )", text)
            out.append(("list", [" ".join(line.strip() for line in item.splitlines()) for item in items]))
        else:
            out.append(("para", " ".join(line.strip() for line in block)))
    sections = [c for k, c in out if k == "section"]
    if [" ".join(c.split(" ", 2)[:2]) for c in sections] != ANNEX_SECTIONS:
        raise SystemExit(f"docs/annex.md: sections {sections} are not Annex A. to Annex E. in order")
    if not out or out[0][0] != "section":
        raise SystemExit("docs/annex.md: text before the first section")
    return out


def annex_paragraphs(md: str) -> list[str]:
    """The annex's prose paragraphs and list items, for the value check."""
    blocks = annex_blocks(md)
    return [c for k, c in blocks if k == "para"] + [i for k, c in blocks if k == "list" for i in c]


# --- the value check --------------------------------------------------------------------------------------------

@dataclass
class RunSet:
    values: list[Decimal] = field(default_factory=list)
    units: list[tuple[Decimal, str]] = field(default_factory=list)
    pairs: set[tuple[int, int]] = field(default_factory=set)
    counts: set[tuple[int, str]] = field(default_factory=set)
    pooled: set[tuple[int, int]] = field(default_factory=set)


def _section(text: str, heading: str) -> str:
    if heading not in text:
        raise SystemExit(f"eval/results.md: section {heading!r} missing")
    start = text.index(heading)
    end = text.find("\n## ", start + len(heading))
    return text[start:] if end == -1 else text[start:end]


def _numbers(cell: str) -> list[Decimal]:
    return [Decimal(n) for n in re.findall(r"(?<![\w.])\d+(?:\.\d+)?(?![\w.])", cell)]


def _tables(section: str) -> list[list[list[str]]]:
    """Every markdown table in the section: rows of cells, the header row first, the --- row dropped."""
    tables, rows = [], []
    for line in section.splitlines() + [""]:
        if line.startswith("|"):
            if not set(line) <= set("|- "):
                rows.append([c.strip() for c in line.strip().strip("|").split("|")])
        elif rows:
            tables.append(rows)
            rows = []
    return tables


def run_sets(results: str) -> dict[str, RunSet]:
    c3, c5 = RunSet(), RunSet()
    for heading in ("## Governed", "## Ungoverned"):
        section = _section(results, heading)
        table = next(t for t in _tables(section) if "Gate rejection" in t[0])
        for row in table[1:]:
            for cell in row[2:]:
                c3.values += _numbers(cell)
        latency = re.search(r"^Latency: .*$", section, re.M)
        if not latency:
            raise SystemExit(f"eval/results.md: no latency line under {heading!r}")
        c3.units += [(Decimal(v), u) for v, u in re.findall(r"(\d+(?:\.\d+)?) (ms|decisions|calls)\b", latency[0])]
    section = _section(results, "## C3, C4 and C5")
    tables = _tables(section)
    summary = next(t for t in tables if t[0][:2] == ["Row", "C3 en"])
    for row in summary[1:]:
        cells = dict(zip(summary[0], row))
        for name, run_set in (("C3", c3), ("C5", c5)):
            for lang in ("en", "ar"):
                run_set.values += _numbers(cells[f"{name} {lang}"])
    by_scenario = next(t for t in tables if "Citation validity C3 / C4 / C5" in t[0])
    for row in by_scenario[1:]:
        for cell in row[2:]:
            parts = cell.split(" / ")
            if len(parts) != 3:
                raise SystemExit(f"eval/results.md: per-scenario cell not 'C3 / C4 / C5': {cell!r}")
            c3.values += _numbers(parts[0])
            c5.values += _numbers(parts[2])
    misses = re.search(r"^Misses: (\d+) of (\d+) key steps", section, re.M)
    if not misses:
        raise SystemExit("eval/results.md: no 'Misses:' line")
    missed, total = int(misses[1]), int(misses[2])
    c5.pairs |= {(total - missed, total), (missed, total)}
    pooled = re.search(r"^Pooled over both languages \(C5\): .*$", section, re.M)
    if not pooled:
        raise SystemExit("eval/results.md: no 'Pooled over both languages' line")
    c5.pooled |= {(int(n), int(m)) for n, m in re.findall(r"(\d+) of (\d+) [^,;]*, 95% interval", pooled[0])}
    c5.pairs |= c5.pooled
    found = re.search(r"^(\d+) of (\d+) expected gaps found in every run; (\d+) missed .*?; (\d+) unexpected "
                      r"register ids flagged\.$", _section(results, "## Gaps against the keys"), re.M)
    if not found:
        raise SystemExit("eval/results.md: no 'N of M expected gaps found in every run' line")
    c5.pairs.add((int(found[1]), int(found[2])))
    c5.counts |= {(int(found[3]), "missed"), (int(found[4]), "unexpected")}
    return {"C3": c3, "C5": c5}


def _rounded(value: Decimal, token: str) -> Decimal:
    places = len(token.partition(".")[2])
    return value.quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP)


def _parts(para: str) -> list[tuple[str, list[str]]]:
    """A paragraph with one run set whole; one with two split into sentences, each under the tag it carries, else
    the last tag before it, else the first after it (hq ruling, 2026-10-23: the Results paragraph's C5 and C3
    parts are checked apart)."""
    names = list(dict.fromkeys(tags(para)))
    if len(names) < 2:
        return [(para, names)]
    sentences = re.split(r"(?<=\.)\s+(?=[A-Z*(])", para)
    named = [list(dict.fromkeys(tags(s))) for s in sentences]
    for order in (range(1, len(named)), range(len(named) - 2, -1, -1)):
        for i in order:
            j = i - 1 if order.step == 1 else i + 1
            named[i] = named[i] or named[j]
    return list(zip(sentences, named))


def check_paragraph(para: str, sets: dict[str, RunSet]) -> list[str]:
    """Each figure token of a tagged paragraph that matches no value of the named run sets, with why."""
    return [problem for part, names in _parts(para) for problem in _check(part, [sets[n] for n in names])]


def _check(para: str, named: list[RunSet]) -> list[str]:
    values = [v for s in named for v in s.values]
    units = [u for s in named for u in s.units]
    pairs = set().union(*(s.pairs for s in named))
    counts = set().union(*(s.counts for s in named))
    pooled = set().union(*(s.pooled for s in named))
    problems = []
    for m in TOKEN.finditer(para):
        token = m.group(0)
        if m["marker"] or m["ident"]:
            continue
        if m["interval"]:
            bounds = (Decimal(m["lo"]), Decimal(m["hi"]))
            fits = [(n, total) for n, total in pooled
                    if bounds == tuple(_rounded(Decimal(str(b)), t) for b, t in zip(wilson(n, total), (m["lo"], m["hi"])))]
            if not fits:
                problems.append(f"{token}: no pooled count in the run set has that interval")
            elif bounds[1] == 1 and all(n < total for n, total in fits):
                problems.append(f"{token}: misses exist, so the upper bound is below 1; write three decimals")
        elif m["count"]:
            if (int(m["cv"]), m["cu"]) not in counts:
                problems.append(f"{token}: no such count in the run set")
        elif m["of"]:
            if (int(m["n"]), int(m["m"])) not in pairs:
                problems.append(f"{token}: no 'N of M' in the run set")
        elif m["unit"]:
            value, unit = Decimal(m["uv"]), m["u"]
            wanted = [v / 1000 if unit == "s" else v for v, u in units if u == unit or (unit == "s" and u == "ms")]
            if value not in {_rounded(v, m["uv"]) for v in wanted}:
                problems.append(f"{token}: no value with that unit in the run set")
        elif m["num"] and "." in token:
            if Decimal(token) not in {_rounded(v, token) for v in values}:
                problems.append(f"{token}: no value in the run set")
        else:
            problems.append(f"{token}: cannot classify (item 3); stop and ask hq")
    return problems


NUMBER_WORDS = ("zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen "
                "seventeen eighteen nineteen twenty").split()
TENS = {"twenty": 20, "thirty": 30}  # "twenty-one" (Task 33)


def _number(word: str) -> int | None:
    if word.isdigit():
        return int(word)
    if word in NUMBER_WORDS:
        return NUMBER_WORDS.index(word)
    tens, _, unit = word.partition("-")
    return TENS[tens] + NUMBER_WORDS.index(unit) if tens in TENS and unit in NUMBER_WORDS[1:10] else None


# the knowledge-base counts the report states, each read against kb/manifest.csv (order Task 30, Part C)
KB_COUNTS = {"documents": re.compile(r"(?:holds|\*\*SRC-2\*\*)\s+(\d+)\s+documents"),
             "verified": re.compile(r"(\d+)\s+are\s+verified"),
             "foreign": re.compile(r"\b([a-z]+(?:-[a-z]+)?)\s+foreign\s+texts"),
             "uae_other": re.compile(r"\b([a-z]+(?:-[a-z]+)?)\s+other\s+UAE\s+(?:laws|texts)"),
             "uae": re.compile(r"\b(\d+)\s+UAE\s+instruments")}  # Task 36 item 1: the method paragraph
# "the Telecommunications Law 3/2003, the CPR v2.0, Licence 2/2026, the PDPL and N other UAE laws": the UAE
# instruments less the four the sentence names (order Task 33, Part D)
NAMED_UAE = 4
# Task 40 (hq answer to stop 1, option a): a web page and an announcement are not instruments, as their manifest
# notes say ("Service page, not an instrument"; "Announcement, not a law"); Annex A names the two rows
NOT_INSTRUMENTS = ("announcement", "web_page")


# Annex A's counts (order Task 38 item 3): "88 documents in `kb/manifest.csv`: 31 UAE instruments ... 34 foreign
# texts ... 83 are VERIFIED ..., 2 REFERENCED ... and 3 UNVERIFIED"
ANNEX_KB_COUNTS = {"documents": re.compile(r"(\d+)\s+documents\s+in\s+`kb/manifest\.csv`"),
                   "uae": KB_COUNTS["uae"],
                   "foreign": re.compile(r"\b(\d+)\s+foreign\s+texts"),
                   "verified": re.compile(r"\b(\d+)\s+are\s+VERIFIED"),
                   "referenced": re.compile(r"\b(\d+)\s+REFERENCED"),
                   "unverified": re.compile(r"\b(\d+)\s+UNVERIFIED")}


def check_kb_counts(md: str, patterns: dict[str, re.Pattern] = KB_COUNTS) -> list[str]:
    rows = kb.load_manifest()
    uae = {r["instrument"] for r in rows if r["jurisdiction"] == "UAE" and r["source_type"] not in NOT_INSTRUMENTS}
    actual = {"documents": len(rows), "verified": len(kb.verified_rows(rows)),
              "foreign": sum(r["jurisdiction"] == "foreign" for r in rows), "uae_other": len(uae) - NAMED_UAE,
              "uae": len(uae), "referenced": sum(r["status"] == "REFERENCED" for r in rows),
              "unverified": sum(r["status"] == "UNVERIFIED" for r in rows)}
    problems = []
    for name, pattern in patterns.items():
        for m in pattern.finditer(md):
            value = _number(m[1])
            if value != actual[name]:
                problems.append(f"{' '.join(m[0].split())}: kb/manifest.csv has {actual[name]} ({name})")
    return problems


def check_values(md: str, results: str, blocks: list[str] | None = None) -> list[str]:
    sets = run_sets(results)
    failures = []
    for para in paragraphs(md) if blocks is None else blocks:
        if tags(para):
            failures += [f"{problem}\n  in: {para}" for problem in check_paragraph(para, sets)]
    return failures


# --- the docx ---------------------------------------------------------------------------------------------------

def _plain(text: str) -> str:
    return strip_tags(text).replace("`", "")


def _runs(paragraph: Paragraph, text: str, size: Pt | None = None) -> None:
    """Markdown bold as bold runs, in the template's body run (Times New Roman, theme text colour)."""
    for i, piece in enumerate(re.split(r"\*\*", _plain(text))):
        if piece:
            _run(paragraph, piece, bold=i % 2 == 1, size=size)


def _run(paragraph: Paragraph, text: str, bold: bool = False, size: Pt | None = None):
    run = paragraph.add_run(text)
    fonts = OxmlElement("w:rFonts")
    for attr in ("w:ascii", "w:eastAsia", "w:hAnsi", "w:cs"):
        fonts.set(qn(attr), FONT)
    run._r.get_or_add_rPr().insert(0, fonts)
    color = OxmlElement("w:color")
    color.set(qn("w:val"), "000000")
    color.set(qn("w:themeColor"), "text1")
    run._r.get_or_add_rPr().append(color)
    if bold:
        run.bold = True
    if size:
        run.font.size = size
    return run


def _strip_ids(element) -> None:
    for el in element.iter():
        for attr in [a for a in el.attrib if a.startswith("{http://schemas.microsoft.com/office/word/2010/wordml}")]:
            del el.attrib[attr]


class Builder:
    def __init__(self, template: Path):
        self.doc = Document(str(template))
        self.body = self.doc.element.body
        self.tbl_pr = copy.deepcopy(self.doc.tables[0]._tbl.tblPr)

    def paragraph(self, after, text: str = "", align=WD_ALIGN_PARAGRAPH.JUSTIFY) -> Paragraph:
        p = OxmlElement("w:p")
        after.addnext(p)
        paragraph = Paragraph(p, self.doc._body)
        paragraph.alignment = align
        if text:
            _runs(paragraph, text)
        return paragraph

    def spacer(self, after) -> Paragraph:
        """An empty 4 pt paragraph: one empty run and the paragraph mark at 4 pt, line exactly 4 pt, 0 before and after."""
        paragraph = self.paragraph(after)
        fmt = paragraph.paragraph_format
        fmt.space_before = fmt.space_after = Pt(0)
        fmt.line_spacing_rule = WD_LINE_SPACING.EXACTLY
        fmt.line_spacing = SPACER
        paragraph.add_run("").font.size = SPACER
        mark = OxmlElement("w:rPr")
        for tag in ("w:sz", "w:szCs"):
            el = OxmlElement(tag)
            el.set(qn("w:val"), str(int(SPACER.pt * 2)))
            mark.append(el)
        paragraph._p.get_or_add_pPr().append(mark)
        return paragraph

    def image(self, after, marker: str) -> Paragraph:
        m = re.fullmatch(r"!\[[^\]]*\]\(([^)]+)\)", marker)
        path = m.group(1) if m else ""
        if path not in FIGURE_WIDTH:
            raise SystemExit(f"docs/report.md: figure marker not in the order: {marker!r}")
        if not (REPO / path).exists():
            raise SystemExit(f"{path}: figure missing; run the figure scripts")
        paragraph = self.paragraph(after, align=WD_ALIGN_PARAGRAPH.CENTER)
        paragraph.paragraph_format.keep_with_next = True
        paragraph.add_run().add_picture(str(REPO / path), width=FIGURE_WIDTH[path])
        return paragraph

    def table(self, after, block: str, reuse=None):
        rows = [[_plain(c.strip()) for c in _cells(line)]
                for line in block.splitlines() if not set(line.strip()) <= set("|- ")]
        tbl = reuse if reuse is not None else OxmlElement("w:tbl")
        if reuse is None:
            tbl.append(copy.deepcopy(self.tbl_pr))
        for child in [c for c in tbl if c.tag != qn("w:tblPr")]:
            tbl.remove(child)
        widths = _widths(rows)
        grid = OxmlElement("w:tblGrid")
        for w in widths:
            col = OxmlElement("w:gridCol")
            col.set(qn("w:w"), str(w))
            grid.append(col)
        tbl.append(grid)
        table = Table(tbl, self.doc._body)
        for r, cells in enumerate(rows):
            tr = OxmlElement("w:tr")
            tbl.append(tr)
            for c, text in enumerate(cells):
                tc = OxmlElement("w:tc")
                tc_pr = OxmlElement("w:tcPr")
                tc_w = OxmlElement("w:tcW")
                tc_w.set(qn("w:w"), str(widths[c]))
                tc_w.set(qn("w:type"), "dxa")
                tc_pr.append(tc_w)
                tc.append(tc_pr)
                tc.append(OxmlElement("w:p"))
                tr.append(tc)
                paragraph = Paragraph(tc[-1], table)
                paragraph.paragraph_format.space_before = Pt(0)
                paragraph.paragraph_format.space_after = Pt(0)
                if r == 0:
                    _run(paragraph, text.replace("**", ""), bold=True, size=CELL_SIZE)
                else:
                    _runs(paragraph, text, size=CELL_SIZE)
        after.addnext(tbl)
        return tbl

    def heading(self, element, text: str) -> None:
        """Keep the template heading paragraph and its first run's formatting; replace the text."""
        runs = element.findall(qn("w:r"))
        for extra in runs[1:]:
            element.remove(extra)
        for el in [e for e in element if e.tag in (qn("w:proofErr"), qn("w:bookmarkStart"), qn("w:bookmarkEnd"))]:
            element.remove(el)
        texts = runs[0].findall(qn("w:t"))
        for t in texts[1:]:
            runs[0].remove(t)
        texts[0].text = text
        texts[0].set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
        Paragraph(element, self.doc._body).paragraph_format.keep_with_next = True  # Task 18 item 2d


def _cells(line: str) -> list[str]:
    """A table row's cells, split at the pipes outside backticks (Annex E: `--rule gap-1|gap-4`)."""
    return re.findall(r"(?:`[^`]*`|[^|`])+|(?<=\|)(?=\|)", line.strip().strip("|"))


def _mono(paragraph: Paragraph, text: str) -> None:
    """A code block in one paragraph: each line a Courier New 8 pt run, lines joined by breaks, nothing edited."""
    for n, line in enumerate(text.split("\n")):
        run = _run(paragraph, line, size=CODE_SIZE)
        fonts = run._r.rPr.find(qn("w:rFonts"))
        for attr in ("w:ascii", "w:eastAsia", "w:hAnsi"):
            fonts.set(qn(attr), MONO)
        if n:
            run._r.insert(1, OxmlElement("w:br"))


def render_annex(b: "Builder", heading_proto, md: str) -> None:
    """Order Task 38 item 3: a page break, "Annex" in the template's heading, then the sections."""
    last = [e for e in b.body if e.tag != qn("w:sectPr")][-1]
    heading = copy.deepcopy(heading_proto)
    _strip_ids(heading)
    p_pr = heading.find(qn("w:pPr"))
    p_pr.remove(p_pr.find(qn("w:numPr")))
    p_pr.insert(1, OxmlElement("w:pageBreakBefore"))
    last.addnext(heading)
    b.heading(heading, ANNEX)
    after = heading
    for kind, content in annex_blocks(md):
        if kind == "table":
            after = b.spacer(b.table(after, content))._p
            continue
        if kind == "list":
            for item in content:
                p = b.paragraph(after)
                p.paragraph_format.left_indent, p.paragraph_format.first_line_indent = Cm(0.6), Cm(-0.6)
                _runs(p, item, size=ANNEX_SIZE)
                after = p._p
            continue
        p = b.paragraph(after, align=WD_ALIGN_PARAGRAPH.LEFT if kind == "code" else WD_ALIGN_PARAGRAPH.JUSTIFY)
        if kind == "section":
            _run(p, content, bold=True, size=Pt(11))
            p.paragraph_format.keep_with_next = True
            p.paragraph_format.space_before = Pt(6)
        elif kind == "code":
            _mono(p, content)
        else:
            _runs(p, content, size=ANNEX_SIZE)
        after = p._p


def _widths(rows: list[list[str]]) -> list[int]:
    """Column widths in dxa over the template table's width, by each column's mean text length, at least 600."""
    cols = len(rows[0])
    weight = [max(sum(len(r[c]) for r in rows) / len(rows), 4) ** 0.75 for c in range(cols)]
    raw = [max(600, int(TABLE_WIDTH * w / sum(weight))) for w in weight]
    raw[-1] += TABLE_WIDTH - sum(raw)
    return raw


def render(report: Report, annex: str | None = None) -> Builder:
    b = Builder(TEMPLATE)
    elements = list(b.body)
    paras = [e for e in elements if e.tag == qn("w:p")]
    headings = [p for p in paras if p.find(qn("w:pPr")) is not None
                and p.find(qn("w:pPr") + "/" + qn("w:pStyle")) is not None
                and p.find(qn("w:pPr") + "/" + qn("w:pStyle")).get(qn("w:val")) == "ListParagraph"
                and p.find(qn("w:pPr") + "/" + qn("w:numPr") + "/" + qn("w:numId")) is not None
                and p.find(qn("w:pPr") + "/" + qn("w:numPr") + "/" + qn("w:numId")).get(qn("w:val")) == "4"]
    if len(headings) != 6:
        raise SystemExit(f"report-template.docx: {len(headings)} numbered ListParagraph headings, 6 expected")
    title, header_proto, spacer = paras[0], paras[1], paras[4]
    mapping_tbl = b.doc.tables[0]._tbl
    keep = {title, spacer, *headings, mapping_tbl, b.body.find(qn("w:sectPr"))}
    header_proto = copy.deepcopy(header_proto)
    for el in elements:
        if el not in keep:
            b.body.remove(el)

    b.heading(title, report.title)
    after = title
    for label, value in report.header:
        p = copy.deepcopy(header_proto)
        _strip_ids(p)
        for r in p.findall(qn("w:r")):
            p.remove(r)
        after.addnext(p)
        paragraph = Paragraph(p, b.doc._body)
        _run(paragraph, label, bold=True)
        _runs(paragraph, " " + value)
        after = p

    mapping_tbl.getparent().remove(mapping_tbl)
    template_headings, placed = iter(headings), []
    for name in SECTIONS:
        if name in ADDED:
            added = copy.deepcopy(headings[0])
            _strip_ids(added)
            placed[-1].addnext(added)
            placed.append(added)
        else:
            placed.append(next(template_headings))
    for name, heading in zip(SECTIONS, placed):
        b.heading(heading, name)
        blocks = list(report.sections[name])
        if name == SECTIONS[-1] and TAIL in report.sections:
            tail = report.sections[TAIL]
            blocks += [f"**{TAIL}.** {tail[0]}"] + tail[1:]
        after = heading
        tables_seen = 0
        for i, block in enumerate(blocks):
            if block.startswith("|"):
                reuse = mapping_tbl if name == MAPPING and tables_seen == 0 else None
                after = b.table(after, block, reuse)
                tables_seen += 1
            elif block.startswith("!["):
                after = b.image(after, block)._p
            elif i and blocks[i - 1].startswith("![") and block.startswith("*") and block.endswith("*"):
                caption = b.paragraph(after, align=WD_ALIGN_PARAGRAPH.CENTER)
                _runs(caption, block.strip("*"), size=Pt(10))
                after = caption._p
            else:
                after = b.paragraph(after, block)._p
            if after.tag == qn("w:tbl"):
                # a paragraph after each table keeps two tables from merging and spaces it from the text
                after = b.spacer(after)._p
    if mapping_tbl.getparent() is None:
        raise SystemExit("docs/report.md: section 4 has no table to replace the template's mapping table")
    if annex is not None:
        render_annex(b, placed[0], annex)
    core = b.doc.core_properties
    core.created = FIXED_DATE
    core.modified = FIXED_DATE
    core.author = core.last_modified_by = CREATOR  # hq ruling, 2026-10-23: not the template's author
    return b


def write(builder: Builder, out: Path) -> None:
    """Save, then rewrite the zip with fixed entry times and no compression, so two builds are byte-identical on
    every machine."""
    buffer = io.BytesIO()
    builder.doc.save(buffer)
    out.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(buffer) as src, zipfile.ZipFile(out, "w", zipfile.ZIP_STORED) as dst:
        for info in src.infolist():
            entry = zipfile.ZipInfo(info.filename, date_time=ZIP_TIME)
            entry.create_system = 0  # zipfile writes 3 on Linux, 0 on Windows
            entry.external_attr = 0o600 << 16
            dst.writestr(entry, src.read(info.filename))


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--md", default=str(REPORT_MD))
    parser.add_argument("--annex", default=str(ANNEX_MD), help="an empty value leaves the annex out")
    parser.add_argument("--out", default=str(REPORT_DOCX))
    args = parser.parse_args(argv)
    md = Path(args.md).read_text(encoding="utf-8")
    annex = Path(args.annex).read_text(encoding="utf-8") if args.annex else None
    results = RESULTS.read_text(encoding="utf-8")
    failures = check_values(md, results)
    if annex is not None:
        failures += check_values("", results, annex_paragraphs(annex))
    if failures:
        print("value check failed (eval/results.md):", *failures, sep="\n", file=sys.stderr)
        return 1
    failures = check_kb_counts(md) + (check_kb_counts(annex, ANNEX_KB_COUNTS) if annex is not None else [])
    if failures:
        print("knowledge-base count check failed (kb/manifest.csv):", *failures, sep="\n", file=sys.stderr)
        return 1
    write(render(parse(md), annex), Path(args.out))
    print(Path(args.out).resolve().relative_to(REPO).as_posix() if Path(args.out).resolve().is_relative_to(REPO)
          else args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
