"""Order 2026-11-05 Task 49: eight wording fixes and two searched lines. Kept as the order's checks."""

from __future__ import annotations

import re

import pytest

from onyx import data, kb

OLD = (  # the whole old strings stay out of this file: Done means 2 greps for them
    "six" + " pages",
    "The operator's own code sells through an automated IVR",
    "All 43 QoS chunks searched",
    "no recorded run, C3 or C5",
    "Automated systems may market",
    "(CAD 812",
    "operators' own non-contractual codes",
)
ETHICS_LINE = {
    "clause": "mocai-ai-ethics-2022:3.3.2.2",
    "file": "kb/sources/mocai-ai-ethics-2022.pdf",
    "page": 15,
    "says": "Non-binding: an AI that can pass as a human should say it is an AI first. The only federal text that says it.",
    "quote": "If an AI system can convincingly impersonate a human being, it should do so only after notifying the AI "
             "subject that it is an AI system",
}
CPR_LINE = {
    "clause": "tdra-cpr-v2-en:4.19.3",
    "file": "kb/sources/tdra-cpr-v2-en.pdf",
    "page": 17,
    "says": "SMS or USSD purchase: agreement by a separate step on the same channel; nothing on a channel that "
            "interprets free words.",
    "quote": "the purchase procedure shall necessitate the Consumer to provide agreement to the purchase of the service "
             "by a separate step involving the same means of electronic communications (e.g. SMS or USSD)",
}


def _row(gap_id: str) -> dict:
    [row] = [r for r in data.load_gaps()["gaps"] if r["id"] == gap_id]
    return row


def _says(gap_id: str, clause: str) -> str:
    [line] = [s for s in _row(gap_id)["searched"] if s["clause"] == clause]
    return line["says"]


def _text(path: str) -> str:
    return (kb.REPO / path).read_text(encoding="utf-8")


def test_the_old_wording_is_gone_from_everything_a_reader_opens():
    for path in ("README.md", "docs/annex.md", "docs/gaps.md", "onyx/data/gaps.json"):
        text = _text(path)
        for old in OLD:
            assert old not in text, (path, old)
    site = _text("docs/site/gaps.html").replace("&#x27;", "'").replace("&#39;", "'")
    for old in OLD:
        assert old not in site, old


def test_readme_says_nine_pages_and_limits_the_citation_claim_to_s1():
    readme = _text("README.md")
    assert "Open `docs/site/index.html` from disk: nine pages, no server" in readme
    assert "no recorded S1 run, C3 or C5, cites CPR 17.4 or 17.4.1." in readme


def test_the_register_carries_the_orders_new_wording():
    ivr = ("The operator's own code describes subscription through its IVR as binding with immediate effect; the code "
           "names no OTP, read-back or AI; what the sale must include is set by the CPR, not by the code.")
    assert _says("gap-2", "eand-code-of-practice-en:4") == ivr
    assert _says("gap-11", "eand-code-of-practice-en:4") == ivr
    assert _says("gap-10", "qos-v3-en:9.5").endswith(
        "The QoS Policy v3.0 was searched for language, Arabic, English and لغة: no hit; one chunk (9.5, Annex A) is held.")
    assert _says("gap-6", "cabinet-56-2024-en:5(6)") == (
        "Automated communication systems may market, in accordance with the resolution; no duty to disclose the machine.")
    assert _says("gap-7", "cabinet-56-2024-en:5(6)") == (
        "Automated communication systems may market, in accordance with the resolution. A permission.")
    chatbot = ("The only UAE texts naming an operator chatbot are the operators' own codes of practice; neither sets a "
               "conduct standard (e&'s says it forms no contract).")
    assert _says("gap-7", "du-code-of-practice-en:Annex 1") == chatbot
    assert _says("gap-7", "eand-code-of-practice-en:1") == chatbot


def test_the_air_canada_amount_says_what_was_ordered_in_register_and_annex():
    amount = "(ordered to pay CAD 812.02 in all, CAD 650.88 of it damages)"
    assert amount in _row("gap-7")["note"]
    assert amount in _text("docs/annex.md")


@pytest.mark.parametrize("gap_id,line", [("gap-6", ETHICS_LINE), ("gap-11", CPR_LINE)])
def test_the_two_searched_lines_close_their_gaps_list_and_are_on_their_page(gap_id, line):
    searched = _row(gap_id)["searched"]
    assert searched[-1] == line
    assert [s["clause"] for s in searched].count(line["clause"]) == 1
    assert kb.manifest_by_id()[line["clause"].split(":", 1)[0]]["status"] == "VERIFIED"
    assert f"- `{line['clause']}` (p. {line['page']}, `{line['file']}`): {line['says']}" in _text("docs/gaps.md")
    path = kb.REPO / line["file"]
    if not path.exists():
        pytest.skip("kb/sources/ is local only (gitignored): run kb fetch --local")
    import pypdf
    page = pypdf.PdfReader(path).pages[line["page"] - 1].extract_text() or ""
    squash = lambda text: re.sub(r"\s+", "", text)  # the PDF's text layer breaks lines and spaces
    assert squash(line["quote"]) in squash(page)
