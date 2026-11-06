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
         "abstained and logged the gap on the unanswerable step in 20 of 20 runs"]
# Each strip cell's figures, as the main text prints them. The cells are shortened, so the words differ.
PRINTED = {STRIP[0]: ["same five scenarios", "both languages", "over the 20 scored runs"],
           STRIP[1]: ["108 documents", "100 are verified"],
           STRIP[2]: ["action recall", "0.96 / 1.00", "110 of 112 key steps"],
           STRIP[3]: ["citation validity 0.99 / 1.00"],
           STRIP[4]: ["abstention on the one unanswerable step per scenario 1.00"]}


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


@pytest.mark.parametrize("line, number, name", [("| SRC |", 1, "Data/model Marketplace"), ("| MLFO; ML sandbox |", 13, "Digital Infrastructure")])
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


def test_the_sources_sentence_is_cut_and_annex_a_carries_what_it_named():
    """hq's stop 1 ruling, question 1: the cut; the strip's 108 documents stays printed in the main text."""
    body = " ".join(REPORT[REPORT.index("## Introduction"):REPORT.index("## Description of the use case")].split())
    assert body.endswith("Annex A lists the sources (the PDPL is the Personal Data Protection Law 45/2021); 100 are verified: "
                         "the issuing body's file is on disk with its SHA-256, and a test on every push checks each clause "
                         "the gates cite word for word against the text stored from it. No consumer data was used.")
    assert "other UAE texts" not in REPORT and "foreign texts" not in REPORT
    main_text = " ".join(REPORT[REPORT.index("## Introduction"):].split())
    assert "108 documents" in main_text
    annex_a = " ".join(ANNEX[:ANNEX.index("## Annex B.")].split())
    assert "6 ITU texts (Y.3172 and Y.3173 among them, one a work-programme page) and the Readiness report" in annex_a
    for name in ("Telecommunications Law", "CPR", "public licences", "PDPL", "foreign texts"):
        assert name in annex_a, name


def test_figure_2_is_restyled_at_8_pt_with_main_height():
    """51.F, hq's stop 1 ruling: no hatching, 8 pt, the displayed height held at main's 16 by 5 cm so no line moves."""
    script = (REPO / "scripts" / "fig_results.py").read_text(encoding="utf-8")
    assert "FONT = 8 " in script and "hatch" not in script.replace("no hatching", "")
    assert "<pattern" not in (REPO / "docs" / "fig" / "fig2-results.svg").read_text(encoding="utf-8")
    header = (REPO / "docs" / "fig" / "fig2-results.png").read_bytes()[16:24]
    width, height = int.from_bytes(header[:4], "big"), int.from_bytes(header[4:], "big")
    assert round(width / height, 1) == round(16 / 5, 1)


def test_annex_a_prints_the_task_50_figures_and_they_are_the_recorded_ones():
    """hq's stop 1 ruling: the Annex A sentence, stopped on if eval/results.md disagrees."""
    annex = " ".join(ANNEX.split())
    assert ("the best one measured before the freeze, bge-m3, moved pooled recall@8 from 0.24 to 0.34 in English and from "
            "0.09 to 0.32 in Arabic (Retrieval below), short of the 0.40 English target set before measuring; it was not "
            "adopted, because adopting it would have meant re-recording the scored runs.") in annex
    results = (REPO / "eval" / "results.md").read_text(encoding="utf-8")
    shipped = results[results.index("### Shipped embedder"):]
    assert "| Pooled | en | 29 of 123 (0.24) |" in shipped and "| Pooled | ar | 11 of 123 (0.09) |" in shipped
    bge = results[results.index("### bge-m3"):]
    assert "| Pooled | en | 42 of 123 (0.34) |" in bge and "| Pooled | ar | 39 of 123 (0.32) |" in bge


# --- 51.C, 51.D, 51.G, 51.J ------------------------------------------------------------------------------------------

def test_the_controversy_case_is_named_in_annex_c():
    assert ('That is the controversy case: governance looks slower, because the ungoverned run reaches the subscriber\'s '
            '"yes" first and charges on it.') in " ".join(ANNEX.split())


def test_the_readme_first_screen_is_in_the_orders_order():
    top = README[:README.index("## For the reviewer")]
    assert top.index("# Mizan") < top.index("[![reproduce]") < top.index("**Synthetic data.**") < top.index("Mizan is a consumer-care AI")


def test_the_team_table_carries_the_reviewer_with_his_title_and_his_qualification():
    section = README[README.index("## What Mizan is"):README.index("## Why")]
    assert "| Onyx | Iyas Shraim (leader), Mohammed Rawashdeh, Yanal Faouri, Zaid Saaydeh | BAU Faculty of Artificial Intelligence. Mentor: Dr. Wafaa Almaaitah |" in section
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
            # Task 51b: the ruled note's own sentence says the opposite of the claim barred here
            line = line.replace("The CPR does not say which language prevails.", "")
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
