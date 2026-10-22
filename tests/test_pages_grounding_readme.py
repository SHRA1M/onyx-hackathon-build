"""Task 16 (order 2026-10-22-task-16-pages-grounding-readme): the page of every citation (kb.page_of, from the
committed chunks), one grounding line per scenario, the README in our own words, and the candidate-79bis-2 row in
hq's wording. The README figures and quoted phrases are checked against the source copies in docs/sources/."""

import json
import re

import pytest

from onyx import data, gaps, kb, replay_page, replay_viewer

README = (kb.REPO / "README.md").read_text(encoding="utf-8")
SOURCES = kb.REPO / "docs" / "sources"
OPENING_READ = SOURCES / "opening-figure-read-2026-10-20.md"
LAW_FILE = "docs/sources/telecom-law-and-licences-2026-10-17.md"


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _squeeze(text: str) -> str:
    """No whitespace at all: the PDF text layer splits words ("non -human", "o f this"); ruling 3, 2026-10-22."""
    return re.sub(r"\s+", "", text).replace("’", "'")


# --- item 1: pages ---------------------------------------------------------------------------------------------

def test_page_of_reads_the_committed_chunks():
    assert kb.page_of("tdra-cpr-v2-en", "26.7.2") == 65
    assert kb.page_of("licence-2-2026", "9.1") == 22
    assert kb.page_of("tdra-cpr-v2-en", "no-such-clause") is None


def test_page_of_is_none_for_every_y3172_id():
    ids = [c["clause"] for c in kb.iter_chunks("itu-t-y3172")]
    assert ids and all(kb.page_of("itu-t-y3172", c) is None for c in ids)


def test_page_of_keeps_a_real_page_on_a_one_page_document():
    # decision-16 has one committed page (10); only an all-page-1 document is a placeholder
    assert kb.page_of("decision-16-2026-ar", "4.18") == 10


PAGE_TEST = [("tdra-cpr-v2-en", "26.7.2", 65), ("licence-2-2026", "16.3.2", 45), ("telecom-law-3-2003-en", "79 bis", 29)]


@pytest.mark.parametrize("document_id,clause,page", PAGE_TEST)
def test_the_quote_is_on_its_pdf_page(document_id, clause, page):
    pdf = kb.KB_DIR / "sources" / f"{document_id}.pdf"
    if not pdf.exists():
        pytest.skip("kb/sources/ is local only (fetched, gitignored)")
    from pypdf import PdfReader
    rules = [r for r in data.load_rules() if r["document_id"] == document_id and r["chunk"] == clause]
    quote = rules[0]["quote"] if rules else kb.get_chunk(document_id, clause)["text_en"]
    assert kb.page_of(document_id, clause) == page
    text = PdfReader(pdf).pages[page - 1].extract_text()
    assert _squeeze(quote[:40]) in _squeeze(text)


def test_replay_page_prints_pages_on_cites_and_rule_lines():
    page = replay_page.render(replay_page.RUNS / "S2" / "run1.jsonl")
    assert "`tdra-cpr-v2-en:26.7.2` (p. 65)" in page
    rule = next(r for r in data.load_rules() if r["id"] == "cpr-26-7-2")
    assert f"CPR 26.7.2, p. 65: \"{rule['quote']}\"" in page
    assert "(page " not in page


def test_replay_page_prints_no_page_for_a_placeholder_document():
    rules = {r["id"]: r for r in data.load_rules()}
    y3172 = [rid for rid, r in rules.items() if r["document_id"] == "itu-t-y3172"]
    for line in replay_page._clauses(y3172, rules):
        assert ", p. " not in line


def test_viewer_links_the_page_of_a_pdf_and_not_of_a_landing_page():
    viewer = replay_viewer.Viewer()
    cpr = viewer.clause("cpr-26-7-2")
    url = kb.manifest_by_id()["tdra-cpr-v2-en"]["url"]
    assert f'href="{url}#page=65"' in cpr and "p. 65" in cpr
    law = next(r["id"] for r in data.load_rules() if r["document_id"] == "telecom-law-3-2003-en")
    shown = viewer.clause(law)
    assert "#page=" not in shown and "p. " in shown
    proposal = viewer.proposal({"verb": "draft_reply", "clause_ids": ["tdra-cpr-v2-en:26.7.2"]})
    assert f'href="{url}#page=65"' in proposal


def test_kb_export_has_a_pages_column(tmp_path):
    out = kb.export(tmp_path).read_text(encoding="utf-8")
    assert "| # | Filename | Type | Description | Status | sha256 | Pages | Link |" in out
    cpr = next(l for l in out.splitlines() if "`tdra-cpr-v2-en.pdf`" in l)
    assert "| 74 |" in cpr


# --- item 2: one grounding line per scenario --------------------------------------------------------------------

GROUNDED = {
    "S1": (["tdra-cpr-v2-en:17.4", "tdra-cpr-v2-en:17.4.1"], [51, 51],
           "CPR 17.4 and 17.4.1 require the operator, where possible and practicable, to provide a facility that tells "
           "a roaming subscriber the applicable retail roaming prices for calls and SMS; the price question in step 2 "
           "is the one that facility answers."),
    "S2": (["tdra-cpr-v2-en:4.20.1"], [17],
           "CPR 4.20.1 requires a PIN or TDRA-approved 2FA for each and every content purchase, premium channels "
           "included; the AED 45 charge with no consent record is the charge that rule exists to stop."),
    "S3": (["pdpl-45-2021-en:23(1)"], [25],
           "PDPL 23(1) lets personal data leave the State only in listed cases, one being a contract binding the "
           "foreign recipient to this law's controls; the model provider abroad is such a recipient."),
    "S4": (["tdra-cpr-v2-en:22.1.1"], [58],
           "CPR 22.1.1 requires, wherever possible, an individual notice and warning before a disconnection for "
           "non-payment; step 1 fires with `warning_sent: false`."),
    "S5": (["decision-16-2026-ar:4.18", "tdra-cpr-v2-en:26.11"], [10, 66],
           "Decision 16/2026 4.17 and 4.18 make the operator verify the reporter's identity at once and block a lost "
           "device within two hours; CPR 26.11 lets TDRA order a service restored while a dispute is open."),
}


@pytest.mark.parametrize("sid", sorted(GROUNDED))
def test_grounded_in_is_the_orders_line_on_committed_chunks(sid):
    ids, pages, line = GROUNDED[sid]
    grounded = data.load_scenario(sid)["grounded_in"]
    assert [c["clause_id"] for c in grounded["clauses"]] == ids
    assert [c["page"] for c in grounded["clauses"]] == pages
    assert grounded["line"] == line
    for clause_id, page in zip(ids, pages):
        document_id, clause = clause_id.split(":", 1)
        assert kb.get_chunk(document_id, clause)["page"] == page == kb.page_of(document_id, clause)
        assert (document_id, clause) in data.cited_chunks()


def test_replay_page_prints_the_grounding_under_the_title():
    for sid in replay_page.SCENARIOS:
        lines = replay_page.render(replay_page.source(sid)).splitlines()
        assert lines[0].startswith(f"# Replay: {sid},")
        assert lines[2].startswith("Grounded in: ") and GROUNDED[sid][2] in lines[2]


def test_readme_scenarios_table_has_the_grounded_in_column():
    section = README.split("## Scenarios", 1)[1].split("\n## ", 1)[0]
    assert "| id | scenario | steps | replay page | run read | grounded in |" in section
    for sid, (ids, pages, _) in GROUNDED.items():
        row = next(r for r in section.splitlines() if r.startswith(f"| {sid} |"))
        cell = row.strip().strip("|").split("|")[-1].strip()
        assert cell == ", ".join(f"`{i}` (p. {p})" for i, p in zip(ids, pages))


# --- item 3: the README ----------------------------------------------------------------------------------------

FIRST = ("Mizan puts a consumer on the line. It is a consumer-care AI for a synthetic UAE operator, Team Onyx's entry to "
         "the ITU AI for Good Lab Hackathon UAE 2026 (telecom track): agents propose each step of a chat or call, "
         "plain-code gates written from binding UAE clauses allow or block it, and the same gates run in Arabic and "
         "English from the same clauses. Every step is written to a hash-chained log that replays offline, with the "
         "clause, its page and its words.")
WHY_URLS = {
    "e&, Sustainability Report Appendices 2025":
        "https://www.eand.com/content/dam/eand/assets/docs/sustainability/2025/eand-sustainability-report-appendices.pdf",
    "TDRA, Sustainability Report 2023":
        "https://tdra.gov.ae/-/media/Media/Press-Kit/Sustainability-Report/EN/Sustainability-report-2023-English.ashx",
    "Etisalat's Virtual Assistant": "https://www.eand.ae/en/c/etisalat-virtual-assistant.html",
}
ETISALAT = "Etisalat's Virtual Assistant"
WHY = ("e& reported 371,476 customer complaints in its UAE operations for 2025 ([e&, Sustainability Report Appendices "
       f"2025]({WHY_URLS['e&, Sustainability Report Appendices 2025']}), Appendix 1, PDF page 7). TDRA dealt with "
       "23,464 complaints about licensees in 2023, the latest count it has published ([TDRA, Sustainability Report "
       f"2023]({WHY_URLS['TDRA, Sustainability Report 2023']}), p. 34). At the operator the first contact is already "
       f"an AI: [Etisalat's Virtual Assistant]({WHY_URLS[ETISALAT]}), "
       "\"AI (Artificial Intelligence) powered\", 24/7, English or Arabic, whose listed jobs include \"adding or "
       "deleting services, changing of packages\" and \"Billing related clarifications\". No source on file says what "
       "stops such an AI when a chat becomes a complaint or a disconnection. The binding texts do, and Mizan's gates "
       "are written from them.")
THREE = [
    "- A consumer on the line: five scenarios of a subscriber in a chat or call, not an institution in a drill.",
    "- Gates from binding UAE clauses: every allow and block names the clause, its page and its words, in "
    "`docs/replay/`.",
    "- Arabic parity: the same gates and keys in both languages, action recall 0.96 English / 0.94 Arabic on C5 "
    "(`eval/results.md`).",
]
LAST_LIMIT = ("- No source on file shows how a UAE operator's assistant is governed; the Etisalat Virtual Assistant page "
              "lists what it does, not what stops it.")


def _section(heading: str) -> str:
    return README.split(f"\n## {heading}\n", 1)[1].split("\n## ", 1)[0]


def test_readme_first_paragraph_is_the_orders():
    head = README.split("\n## ", 1)[0]
    assert FIRST in [_norm(p) for p in head.split("\n\n")]
    assert "Team Onyx's entry to the ITU AI for Good Lab Hackathon UAE 2026 (telecom track). A consumer-care" not in README


def test_readme_why_is_the_orders_with_three_links():
    assert _norm(_section("Why")) == WHY


def test_readme_why_urls_come_from_the_opening_figure_read():
    read = OPENING_READ.read_text(encoding="utf-8")
    for url in WHY_URLS.values():
        assert url in read, url


def test_readme_figures_and_phrases_are_verbatim_in_the_sources():
    read = _norm(OPENING_READ.read_text(encoding="utf-8"))
    eand = _norm((SOURCES / "eand-sustainability-report-appendices-2025.txt").read_text(encoding="utf-8",
                                                                                         errors="replace"))
    tdra = _norm((SOURCES / "tdra-sustainability-report-2023-en.txt").read_text(encoding="utf-8", errors="replace"))
    assert "371,476" in eand and "371,476" in read
    assert "In 2023, the Authority dealt with 23,464 complaints submitted by business and home subscribers regarding " \
           "licensees" in tdra
    for phrase in ("AI (Artificial Intelligence) powered", "adding or deleting services, changing of packages",
                   "Billing related clarifications"):
        assert phrase in read, phrase
        assert f'"{phrase}"' in _norm(_section("Why"))


def test_readme_three_things_and_the_c5_figures():
    section = _section("Three things to look at first")
    assert [l for l in section.splitlines() if l.startswith("- ")] == THREE
    results = json.loads((kb.REPO / "eval" / "results.json").read_text(encoding="utf-8"))["c5"]["C5"]["all"]
    assert (f"{results['en']['action_recall']:.2f}", f"{results['ar']['action_recall']:.2f}") == ("0.96", "0.94")


def test_readme_headings_in_the_orders_order():
    headings = re.findall(r"^## (.+)$", README, re.MULTILINE)
    assert headings[:4] == ["Why", "Three things to look at first", "Gap register", "Run it without a key"]
    assert "Two-minute check" not in headings and "Limits" not in headings
    assert [l for l in _section("What we do not claim").splitlines() if l.startswith("- ")][-1] == LAST_LIMIT


def test_no_other_entry_is_named_in_a_tracked_file():
    import subprocess
    tracked = subprocess.run(["git", "ls-files"], cwd=kb.REPO, capture_output=True, text=True).stdout.split()
    names = re.compile(r"\b(another team|another team|another team|another team)\b")
    for name in tracked:
        if name.startswith("docs/work-orders/"):  # hq's frozen orders; Task 16's own order names two entries
            continue
        path = kb.REPO / name
        if path.suffix in {".md", ".py", ".json", ".html", ".txt", ".csv"} and path.exists():
            assert not names.search(path.read_text(encoding="utf-8", errors="replace")), name


# --- item 4: the candidate-79bis-2 row --------------------------------------------------------------------------

GAP_79 = ("The Cabinet schedule of licensee violations and fines that Telecom Law 79 bis (2) promises (fines up to AED "
          "10,000,000 a violation) is not published; the only published telecom fine schedule, Cabinet 57/2024, covers "
          "the Telemarketing Regulations. Until it exists, a CPR breach by an automated channel sits in the 79 bis (1) "
          "and licence 16.3.2 band, AED 50,000 to 200,000, doubled under licence 16.3.3 for repetition, a missed date "
          "or a material failure.")
UAE_79 = ("Searched 2026-10-16 on the legislation portal and the web, both languages: not found. Whether the Board may "
          "fine a licensee under 79 bis (2) before the schedule exists is not stated in the text (inferred gap, hq "
          "2026-10-22).")


def _row():
    return next(r for r in data.load_gaps()["gaps"] if r["id"] == "candidate-79bis-2-fine-schedule")


def test_candidate_79bis_2_is_hqs_wording():
    row = _row()
    assert row["gap"] == GAP_79 and row["uae_position"] == UAE_79
    assert row["recommendation"] == ("Cabinet to issue the schedule of licensee violations and fines that Telecom Law "
                                     "79 bis (2) promises.")
    assert (row["category"], row["competitor"]) == ("legislative gap", "not read")
    assert [s["clause"] for s in row["searched"]] == ["telecom-law-3-2003-en:79 bis", "telecom-law-3-2003-en:79 bis",
                                                      "licence-2-2026:16.3.2", "licence-2-2026:16.3.3"]
    assert kb.page_of("licence-2-2026", "16.3.3") == 45


def test_candidate_79bis_arabic_is_verbatim_in_the_law_file():
    law = (kb.REPO / LAW_FILE).read_text(encoding="utf-8")
    rows = _row()["searched"][:2]
    for s in rows:
        assert s["file_ar"] == LAW_FILE and s["quote_ar"] in law
    assert "(50.000)" in rows[0]["quote_ar"] and "لمجلس الإدارة توقيع غرامات إدارية" in rows[1]["quote_ar"]


def test_readme_register_row_is_hqs_wording():
    row = next(l for l in README.splitlines() if l.startswith("| candidate-79bis-2-fine-schedule |"))
    assert row.split(" | ")[1] == GAP_79


def test_gaps_md_labels_pages_p():
    text = (kb.REPO / "docs" / "gaps.md").read_text(encoding="utf-8")
    assert "` (page " not in text and "`licence-2-2026:16.3.3` (p. 45)" in text  # the label, not a row's own words


# --- byte-identical on a second run ----------------------------------------------------------------------------

def test_gaps_and_replay_pages_are_byte_identical_on_a_second_run(tmp_path):
    gaps.write(tmp_path / "a.md", readme=None)
    gaps.write(tmp_path / "b.md", readme=None)
    assert (tmp_path / "a.md").read_bytes() == (tmp_path / "b.md").read_bytes()
    first = [p.read_bytes() for p in replay_page.write(tmp_path / "one")]
    second = [p.read_bytes() for p in replay_page.write(tmp_path / "two")]
    assert first == second
    assert first == [(replay_page.OUT / f"{s}.md").read_bytes() for s in replay_page.SCENARIOS]
