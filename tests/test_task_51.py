"""Task 51: the freeze items, and hq's fit-check ruling on the Ra'ed review."""

from __future__ import annotations

import json
import re

import pytest

from onyx import data, kb

REPO = kb.REPO
REPORT = (REPO / "docs" / "report.md").read_text(encoding="utf-8")
ANNEX = (REPO / "docs" / "annex.md").read_text(encoding="utf-8")
README = (REPO / "README.md").read_text(encoding="utf-8")
RUNS_PAGE = (REPO / "docs" / "site" / "runs.html").read_text(encoding="utf-8")
GAPS_MD = (REPO / "docs" / "gaps.md").read_text(encoding="utf-8")
STRIP = ["5 scenarios, 2 languages, 20 recorded runs", "108 documents, 100 verified",
         "action recall 0.96 en / 1.00 ar (110 of 112 key steps)", "citation validity 0.99 / 1.00",
         "expected gaps found 5 of 7 in every run"]
# Each strip cell's figures, as the main text prints them. The cells are shortened, so the words differ.
PRINTED = {STRIP[0]: ["same five scenarios", "both languages", "over 20 runs"],
           STRIP[1]: ["108 documents", "100 are verified"],
           STRIP[2]: ["action recall", "0.96 / 1.00", "110 of 112 key steps"],
           STRIP[3]: ["citation validity 0.99 / 1.00"],
           STRIP[4]: ["5 of 7 found in every run"]}


def _row(gap_id: str) -> dict:
    return next(r for r in data.load_gaps()["gaps"] if r["id"] == gap_id)


# --- 51.A ------------------------------------------------------------------------------------------------------------

def test_the_pages_root_redirects_and_jekyll_is_off():
    assert (REPO / "docs" / ".nojekyll").read_bytes() == b""
    assert 'url=site/' in (REPO / "docs" / "index.html").read_text(encoding="utf-8")


def test_the_runs_page_links_its_own_site_pages_not_the_text_files():
    assert "../replay/" not in RUNS_PAGE
    assert '<a href="whatif.html">whatif.html</a>' in RUNS_PAGE and '<a href="modeldown.html">modeldown.html</a>' in RUNS_PAGE


def test_page_one_has_no_future_tense_and_no_file_still_to_land():
    head = REPORT[:REPORT.index("## Description of the use case")]
    assert "lands" not in head and "will " not in head and "mizan-demo.mp4" not in head


def test_the_knowledge_base_pointers_stay_in_the_readme_reviewer_table():
    row = next(l for l in README.splitlines() if l.startswith("| Knowledge base |"))
    assert "`kb/manifest.csv`" in row and "`kb/DATASHEET.md`" in row


def test_annex_f_is_numbered_in_order():
    assert re.findall(r"^\*\*(F\.\d)", ANNEX, re.M) == ["F.1", "F.2", "F.3", "F.4", "F.5", "F.6"]


def test_gap_13_says_what_was_checked():
    wording = "so no period is in any federal text on the official portal (checked 2026-11-02 and 2026-11-04)"
    assert wording in _row("gap-13")["gap"] and wording in " ".join(ANNEX.split())


@pytest.mark.parametrize("line, number, name", [("| SRC |", 1, "Data/model Marketplace"), ("| MLFO |", 13, "Digital Infrastructure")])
def test_the_documents_only_dimensions_are_named_in_their_rows(line, number, name):
    row = next(l for l in REPORT.splitlines() if l.startswith(line))
    assert f"; and {number} {name}, on documents only" in row


def test_gap_11_says_2fa_per_purchase_with_otp_as_the_default():
    assert "2FA per purchase (4.23.2; OTP by default, 4.11)" in REPORT and "an OTP per purchase" not in REPORT


# --- 51.B ------------------------------------------------------------------------------------------------------------

def test_the_strip_sits_directly_under_the_header_block():
    before = REPORT[:REPORT.index("## Introduction")]
    assert before.rstrip().endswith("| " + " | ".join(STRIP) + " |\n|---|---|---|---|---|")


def test_every_strip_figure_is_printed_elsewhere_in_the_main_text():
    body = " ".join(REPORT[REPORT.index("## Introduction"):].split())
    for cell, figures in PRINTED.items():
        for figure in figures:
            assert figure in body, (cell, figure)


# --- 51.C, 51.D, 51.G, 51.J ------------------------------------------------------------------------------------------

def test_the_controversy_case_is_named_in_annex_c():
    assert ('That is the controversy case: governance looks slower, because the ungoverned run reaches the subscriber\'s '
            '"yes" first and charges on it.') in " ".join(ANNEX.split())


def test_the_readme_first_screen_is_in_the_orders_order():
    top = README[:README.index("## For the reviewer")]
    assert top.index("# Mizan") < top.index("[![reproduce]") < top.index("**Synthetic data.**") < top.index("Mizan is a consumer-care AI")


def test_the_team_table_carries_the_reviewer_with_his_title_and_his_qualification():
    section = README[README.index("## What Mizan is"):README.index("## Why")]
    assert "| Onyx | Iyas Shraim (leader), Mohammed Rawashdeh, Yanal Faouri | Al-Balqa Applied University, Faculty of AI, students |" in section
    assert ("Ra'ed Shraim, Director Business Excellence – DPO, Solidarity First Insurance Company, Amman – Jordan | "
            "practitioner review, not legal advice, no UAE standing |") in section
    assert "Team Onyx (BAU Faculty of AI)" not in README


def test_the_unseen_bank_is_listed_in_the_readme_and_on_the_runs_page():
    line = "No key exists for them and none has been run; their cold runs are a next step."
    assert line in README and line in RUNS_PAGE
    from html import escape
    for path in sorted((data.SCENARIOS_DIR / "unseen").glob("U*.json")):
        scenario = json.loads(path.read_text(encoding="utf-8"))
        assert f"| {scenario['id']} | {scenario['title_en']} | {scenario['title_ar']} |" in README
        assert escape(scenario["title_en"]) in RUNS_PAGE and scenario["title_ar"] in RUNS_PAGE


def test_nothing_offers_a_judge_a_live_step():
    assert not re.search(r"(?i)type a live|type your own|try it live", README + RUNS_PAGE)


# --- 51.H, 51.I, 51.K ------------------------------------------------------------------------------------------------

def test_no_claim_that_the_arabic_prevails_over_the_cpr():
    for text in (README, REPORT, ANNEX):
        for line in text.splitlines():
            if re.search(r"(?i)prevail", line):
                assert not re.search(r"\bCPR\b|gate table", line), line


def test_the_cpr_26_7_2_note_says_stricter_reading_and_keeps_the_quote():
    rule = next(r for r in data.load_rules() if r["id"] == "cpr-26-7-2")
    assert "stricter reading" in rule["language_note"] and "both readings" not in rule["language_note"]
    assert rule["quote_ar"] == "يستثنى أو يستبعد منها استخدام وكلاء غير بشريين"
    assert json.dumps(rule["language_note"], ensure_ascii=False)[1:-1] in ANNEX


def test_licence_3_4_1_note_names_the_half_the_gate_does_not_cite():
    rule = next(r for r in data.load_rules() if r["id"] == "licence-3-4-1")
    assert "prior written approval" in rule["language_note"]
    assert "prior written approval" in kb.get_chunk("licence-2-2026", "3.4.1")["text_en"]


def test_known_limits_are_in_annex_a_as_ruled():
    annex_a = " ".join(ANNEX[:ANNEX.index("## Annex B.")].split())
    assert "**Known limits.**" in annex_a
    for sentence in (
            "of the licence, only a checked fragment of 9.1 is chunked in Arabic",
            "gaps 2, 4, 5, 6 and 7 rest on the English text for the PDPL clauses they cite",
            "retries, then writes a plain-code hand-over to the named human and the gate decides it",
            "no live outage was run and no real human queue or subscriber notice exists",
            "blind review in which 27 of 28 verdicts agreed",
            "is not built",
            "the label is a design rule, not a tested control",
            "the prototype does not write the step 1 objection into the record"):
        assert sentence in annex_a, sentence
    assert "no one is handed the conversation" not in annex_a


def test_interim_lines_are_attributed_and_do_not_imply_a_minor_signal():
    for gap_id, answer in (("gap-5", "answer 2"), ("gap-9", "answer 5")):
        line = _row(gap_id)["interim"]
        assert line.startswith("Interim position (practitioner's view, reviewer):") and answer in line
        assert "not legal advice" in line and line in GAPS_MD
    assert "minor_signal" not in _row("gap-9")["interim"] and "Mizan does not build this." in _row("gap-9")["interim"]
    assert [r["id"] for r in data.load_gaps()["gaps"] if r.get("interim")] == ["gap-5", "gap-9"]


def test_gap_1_marks_the_stop_as_inferred_and_gap_3_maps_levels_to_acts():
    assert "(inferred: the agent stops the conversation; a system acknowledgement carrying the 26.13.2 reference number is not a conversation)" in _row("gap-1")["recommendation"]
    recommendation = _row("gap-3")["recommendation"]
    assert "to acts, not channels" in recommendation and "failed attempts are logged" in recommendation


def test_gap_2_gains_one_sentence_and_is_not_reframed():
    row = _row("gap-2")
    assert ("The CPR classifies by sales medium and the PDPL by processing purpose, and no text requires a conversational "
            "channel to elicit and store the two consents separately.") in row["uae_position"]
    assert row["gap"].startswith("Consent elicited by an AI:")


def test_no_chapeau_rule_row_and_109_rules_stay():
    rules = data.load_rules()
    assert len(rules) == 109 and not any(r.get("chunk") == "26.7" for r in rules)
