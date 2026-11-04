"""Order 2026-11-04 Task 45: the 11-04 sweep fixes. Kept as the order's checks."""

from __future__ import annotations

import re

from onyx import data, gaps, kb

WAM = "wam-2026-08-21-agentic-ai-guide"
GUIDE = "agentic-ai-gov-guide-2026-08-21"
DOH = "doh-responsible-ai-standard-v1-2025"
WAM_FILE = f"kb/sources/{WAM}.txt"
DOH_FILE = f"kb/sources/{DOH}.pdf"
HANDOVER = ("ضمان الانتقال السلس إلى موظف مختص عند الحاجة، مع نقل كامل تفاصيل الطلب والخطوات المنجزة، حتى لا يضطر "
            "المتعامل لإعادة شرح طلبه من جديد")
CONSENT = "والحصول على موافقته قبل اتخاذ أي إجراء"
OBJECTION = "وتمكينه من السؤال أو التصحيح أو الاعتراض"
TAB = "and 2026-11-04 (Arabic regulations tab, Chrome from hq: «لم يتم العثور على أية بيانات»)"


CSC_NOTE = "Host unreachable from Amman 2026-10-17, 2026-10-30, 2026-11-03 (Chrome) and 2026-11-04 (TLS handshake failed, GitHub as control); no Internet Archive copy. Described at u.ae (page updated 2026-07-02): six chapters, Governance, Infrastructure and Application Security, Algorithm Security, Operational Safety, Adversarial AI Attacks, AI Monitoring and Response. Not read. Recorded as advisory; binding status unknown."
GAP_6_POSITION = "Before a purchase through the agent, disclosure is a validity condition of the sale (11(2)); for service, data and complaint conversations no binding federal text requires it. The non-binding AI Ethics guideline 3.3.2.2 is the only federal text that says it; DIFC Regulation 10.2.2(a) does, for DIFC establishments only (UAE free zone, not federal); the DHA policy 4.3.2 (Dubai, 2021) requires disclosure of AI-enabled functions and the DoH standard 3.1.6.1.1 (Abu Dhabi, 2025) requires telling patients when AI contributes to a decision, each within its own health regulator's scope only. None reaches a telecom licensee."
GAP_7_POSITION = "The binding federal texts read name AI or an automated agent to set a charge waiver, a bar, a definition, a permission and a tool; none sets how an AI agent must behave with a consumer. PDPL 18(4), Electronic Transactions 11(2) and 12(2) and Cabinet 57/2024 Table No. (1) row 16 govern automated decisions, contracts, documents and calls as outcomes, not the agent's conduct. Below the federal level, three of the UAE texts read set such standards, each within its own scope only: the DIFC Data Protection Regulations (Regulation 10, UAE free zone (DIFC), not federal) name notice, limits and intervention for an automated system; the DHA policy 4.3.2 (Dubai, 2021) requires disclosure of AI-enabled functions; the DoH standard 3.1.1.2.2 (Abu Dhabi, 2025) requires human oversight and escalation, with agents in scope. None reaches a telecom licensee, and TDRA has no counterpart."
GAP_7_DOH_SAYS = "Sector line, with the DHA row: the Abu Dhabi Department of Health binds its licensed entities to human oversight and escalation for AI systems, 'agents' named in scope (DoH 1.2); the DHA row sets disclosure, not oversight; TDRA sets no such rule for its licensees."
GAP_7_WAM_SAYS = "Searched, non-binding, government services only: the one UAE text read that is written for agentic AI dealing with the public (approval before any action, hand-over with the full request, a route to ask, correct or object) is guidance for federal government services; it binds no licensee."


def _text(path: str) -> str:
    return (kb.REPO / path).read_text(encoding="utf-8")


def _row(gap_id: str) -> dict:
    return next(r for r in data.load_gaps()["gaps"] if r["id"] == gap_id)


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def test_the_gazette_line_is_dated_and_names_issue_833_in_both_hand_written_sources():
    line = ("The federal Official Gazette (Ministry of Justice, elaws.moj.gov.ae) was unreachable on 2026-11-02, 2026-11-03 "
            "and 2026-11-04 (curl and Chrome from hq, GitHub answering as the control), so its issues were not swept; the "
            "legislation portal, which lists each law's Gazette number and its regulations, is the official check, and it "
            "publishes no issue archive; the newest issue the portal names is No. 833 of 14 October 2026 (entry 4660, read "
            "2026-11-04).")
    assert gaps.GAZETTE_LINE == line
    assert _text("README.md").count(line) == 1
    assert _text("docs/gaps.md").count(line) == 1


def test_the_csc_note_carries_the_11_04_date():
    note = kb.manifest_by_id()["csc-ai-security-policy-v1-1"]["notes"]
    assert note == CSC_NOTE  # hq ruling on Task 45 stop 1: the whole note
    assert note in _text("kb/DATASHEET.md")
    assert "Host unreachable from Amman 2026-10-17 and 2026-10-30" not in _text("kb/DATASHEET.md")


def test_the_readme_lists_the_five_published_criteria():
    readme = _text("README.md")
    assert "The five published criteria" in readme and "four published" not in readme
    block = readme.split("## For the reviewer\n", 1)[1].split("Mizan puts a consumer on the line", 1)[0]
    rows = [line for line in block.splitlines() if line.startswith("| ") and not line.startswith("| Criterion")]
    assert [row.split(" | ")[0] for row in rows] == [
        "| Knowledge base", "| Agent capability in error scenarios", "| Policy, strategy and standards gaps",
        "| Auditability", "| ITU-T Y.3172 and the Readiness Framework"]
    assert "`docs/replay/index.html`" in rows[1] and "python -m onyx why" in rows[1]
    assert "`docs/gaps.md`" in rows[2] and "`docs/replay/whatif-S2-gap-1.md`" in rows[2]


def test_the_pdpl_regulations_tab_recheck_is_dated():
    assert TAB in _row("gap-5")["uae_position"]
    assert TAB in _row("gap-13")["uae_position"]
    assert TAB in _row("gap-14")["uae_position"]
    assert TAB in kb.manifest_by_id()["pdpl-executive-regulations"]["notes"]
    assert _row("gap-3")["gap"].endswith("(portal and TDRA site checked 2026-11-02 and 2026-11-04).")


def test_the_three_rows_are_the_orders():
    rows = kb.manifest_by_id()
    wam, guide, doh = rows[WAM], rows[GUIDE], rows[DOH]
    assert (wam["status"], wam["binding_status"], wam["jurisdiction"], wam["language"], wam["source_type"], wam["node"]) == \
        ("VERIFIED", "advisory", "UAE", "ar", "announcement", "SRC")
    assert wam["url"] == "https://www.wam.ae/ar/article/c1uggxh" and len(wam["sha256"]) == 64
    assert (guide["status"], guide["binding_status"], guide["jurisdiction"], guide["language"], guide["source_type"]) == \
        ("REFERENCED", "advisory", "UAE", "ar", "guidance")
    assert guide["url"] == "https://uaemodel.egsep.ae/agentic_ai_guide_website.html" and not guide["sha256"]
    assert guide["notes"].endswith("Guidance for federal government entities; binds no licensee.")
    assert (doh["status"], doh["binding_status"], doh["jurisdiction"], doh["language"], doh["source_type"]) == \
        ("VERIFIED", "binding", "UAE", "en", "policy")
    assert (doh["sha256"], doh["bytes"], doh["page_count"]) == \
        ("5e03adb731620ed5013e7fbefa0502603338c762e9995da547e69e7f5243d97d", "490537", "15")
    assert doh["notes"].endswith("never a rule for a telecom licensee.")
    assert not kb.has_chunks(GUIDE)


def test_the_five_new_chunks_hold_the_quotes_word_for_word():
    for clause, quote in (("consent", CONSENT), ("handover", HANDOVER), ("objection", OBJECTION)):
        assert _norm(quote) in _norm(kb.get_chunk(WAM, clause)["text_ar"]), clause
    assert kb.get_chunk(DOH, "3.1.1.2.2")["page"] == 5
    assert kb.get_chunk(DOH, "3.1.6.1.1")["page"] == 8
    assert sum(1 for _ in kb.iter_chunks(WAM)) == 3 and sum(1 for _ in kb.iter_chunks(DOH)) == 2


def test_the_searched_lines_quote_their_chunks_and_their_files():
    expected = {"gap-1": [(f"{WAM}:handover", WAM_FILE, None, HANDOVER)],
                "gap-2": [(f"{WAM}:consent", WAM_FILE, None, CONSENT)],
                "gap-11": [(f"{WAM}:objection", WAM_FILE, None, OBJECTION)],
                "gap-6": [(f"{DOH}:3.1.6.1.1", DOH_FILE, 8, None)],
                "gap-7": [(f"{WAM}:handover", WAM_FILE, None, HANDOVER), (f"{DOH}:3.1.1.2.2", DOH_FILE, 5, None)]}
    cited = data.cited_chunks()
    for gap_id, lines in expected.items():
        searched = {s["clause"]: s for s in _row(gap_id)["searched"]}
        for clause, file, page, quote in lines:
            s = searched[clause]
            assert s["file"] == file and s.get("page") == page, clause
            assert quote is None or s["quote"] == quote, clause
            assert tuple(clause.split(":", 1)) in cited, clause
            chunk = kb.get_chunk(*clause.split(":", 1))
            assert _norm(s["quote"]) in _norm(chunk["text_ar"] or chunk["text_en"]), clause


def test_every_count_follows_the_manifest():
    rows = kb.load_manifest()
    status = lambda s: sum(r["status"] == s for r in rows)
    assert (len(rows), status("VERIFIED"), status("REFERENCED"), status("UNVERIFIED")) == (108, 100, 5, 3)
    assert sum(r["jurisdiction"] == "foreign" for r in rows) == 38
    assert len({r["instrument"] for r in rows}) == 86
    assert "108 manifest rows, one per document, 86 instruments." in _text("kb/DATASHEET.md")
    annex = " ".join(_text("docs/annex.md").split())
    assert "108 documents in `kb/manifest.csv`: 36 UAE instruments" in annex
    assert "the DHA AI policy, the DoH standard and the UAE AI Charter" in annex
    assert "three announcements and a news report" in annex
    assert "161 committed chunks across 21 documents" in annex
    report = " ".join(_text("docs/report.md").split())
    assert "holds 108 documents" in report and "100 are verified" in report and "thirty-two other UAE texts" in report
    assert "**SRC-2** 108 documents" in report and "the 36 UAE instruments" in report
    assert "thirty-eight foreign texts" in report
    readme = _text("README.md")
    assert "(108 rows, status, sha256" in readme and "100 VERIFIED" in readme and "5 REFERENCED" in readme


def test_the_gap_6_and_gap_7_positions_are_the_rulings_words():
    assert _row("gap-6")["uae_position"] == GAP_6_POSITION
    assert _row("gap-7")["uae_position"] == GAP_7_POSITION
    md = _text("docs/gaps.md")
    assert GAP_6_POSITION in md and GAP_7_POSITION in md
    assert "the only UAE text of any level" not in md
    searched = {s["clause"]: s for s in _row("gap-7")["searched"]}
    assert searched[f"{DOH}:3.1.1.2.2"]["says"] == GAP_7_DOH_SAYS  # hq ruling: the DHA row sets disclosure, not oversight
    assert searched[f"{WAM}:handover"]["says"] == GAP_7_WAM_SAYS
    assert {s["clause"]: s for s in _row("gap-1")["searched"]}[f"{WAM}:handover"]["says"].startswith(
        "Searched, non-binding, government services only: the National Committee")  # gap-1's line is unchanged
    for gap_id, clauses in (("gap-6", ("dha-ai-policy-2021:4.3.2", f"{DOH}:3.1.6.1.1")),
                            ("gap-7", ("dha-ai-policy-2021:4.3.2", f"{DOH}:3.1.1.2.2"))):
        searched = {s["clause"] for s in _row(gap_id)["searched"]}
        assert set(clauses) <= searched, gap_id  # every clause the position names is on its own row
