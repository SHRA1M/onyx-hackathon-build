"""Task 53: the report's wording after Iyas's review and the gap ruling (order 2026-11-05, with its 2026-11-06 changes).

Text only: each test pins a sentence the order quotes, read with whitespace folded, because the source files wrap.
"""
import importlib.util
import json
import re
import sys

import pytest

from onyx import data, kb, site

REPO = kb.REPO


def _fold(text: str) -> str:
    return re.sub(r"\s+", " ", text)


REPORT = _fold((REPO / "docs" / "report.md").read_text(encoding="utf-8"))
ANNEX = _fold((REPO / "docs" / "annex.md").read_text(encoding="utf-8"))
README = _fold((REPO / "README.md").read_text(encoding="utf-8"))
GAPS_MD = _fold((REPO / "docs" / "gaps.md").read_text(encoding="utf-8"))
INDEX = _fold((REPO / "docs" / "site" / "index.html").read_text(encoding="utf-8"))
GAPS_HTML = _fold((REPO / "docs" / "site" / "gaps.html").read_text(encoding="utf-8"))

CASE = "The case is an ordinary customer talking to their phone company in a chat or on a call, not a practice exercise."
TEAM = "Mohammed Rawashdeh, Yanal Faouri, Zaid Saaydeh"
FACULTY = "BAU Faculty of Artificial Intelligence"
MENTOR = "Mentor: Dr. Wafaa Almaaitah"
STRIP_CELL = "abstained and logged the gap on the unanswerable step in 20 of 20 runs"
NEW_NOTE = ("Mizan enforces the stricter reading, citing 26.7.2 and licence 9.1; the chapeau is quoted here and holds no "
            "rule.")
OLD_NOTE = "Mizan enforces the stricter reading and cites the chapeau, the clause and licence 9.1 together."
CABINET = ("The Cabinet shall issue a resolution on the schedule of violations and fines imposed on licensees provided "
           "they do not exceed (10,000,000) ten million dirhams for each violation.")
TILE = ("(average of the five scenarios; S1 reads 0.33, see Annex C; the report counts all gaps together, 5 of 7)")
DEF_END = "S1 reads 0.33 because its key places two gaps at steps the adviser does not reach; see Annex C."

REPORT_HAS = [
    "**Team leader:** Iyas Shraim (BAU Faculty of Artificial Intelligence)",
    f"**Team members:** {TEAM}",
    CASE,
    "UAE telecom rules already in force set four limits on an AI in that seat. It cannot charge a customer for a service "
    "they did not expressly order, so nobody pays for what they did not ask for (TDRA Consumer Protection Regulations "
    "v2.0, CPR 4.3). It cannot share their data with affiliates or outside parties without prior consent, so the customer "
    "decides who sees it (24.6). It cannot cut their line for non-payment without a warning first, so they have time to "
    "act (22.1). And it cannot handle their complaint, because that conversation is reserved for a person: 26.7.2 "
    "requires licensees to \"preclude the use of non-human agents by Licensees in conversations with Consumers regarding "
    "Consumer Complaints\".",
    "**Demo video:** see the repository README.",
    STRIP_CELL,
    "expected gaps: 5 of 7 found in every run; the 2 not found (gaps 2 and 6) are keyed to S1 steps where the adviser, "
    "the only agent that holds the register, does not speak (Annex C); 3 unexpected ids flagged",
    "The recorded runs re-find, on every run, all 5 expected gaps keyed to a step where the adviser speaks; gaps 2 and 6 "
    "are keyed to S1 steps it does not reach (Annex C).",
    "We ran the same five scenarios twice on the same model, once with the gates on and once with them off. With the "
    "gates off, on average about two acts per run went through that should have been stopped or handed to a person: 2.3 "
    "in English and 2.1 in Arabic `[C3, prompt v3, three runs per scenario per language]`.",
    "The test results in this report can be checked: a command called `eval` recalculates them from the run logs, and "
    "anyone can run it.",
    "where its authority ends",
    "Five agents (care, the policy and legal adviser, the Data Office, TDRA and a coordinator), each with a fixed list of "
    "what it may do and read.",
    "each agent searches only the documents its role allows, so the model sees only the policy text that role may use",
    "each agent searches only the documents its role allows, a cited id",
    "retrieval limited by role",
    "Of the 13 Readiness 2.0 dimensions, we claim five (6, 7, 8, 10, 11) with evidence from the running system and two "
    "(1, 13) from documents only, with no running system behind them; the other six we do not claim.",
    "We test Mizan on five made-up customer conversations, called S1 to S5: S1, roaming before a flight; S2, a billing "
    "question that becomes a complaint; S3, a partner wants the data and the AI provider is abroad; S4, non-payment and "
    "an automated disconnection; S5, a TDRA dispute and a loss report. Each is shown in detail under Error scenarios.",
    "1. See it online, nothing to install. The replay site shows each recorded conversation step by step, with the "
    "clause, page and words behind every decision (`docs/replay/index.html`).",
    "2. A customer asks why. One command prints the decision, the clause with its quote and the log entry's fingerprint, "
    "in English or Arabic: `python -m onyx why <log> --step <n>`, where `<log>` is the file of the recorded conversation "
    "and `<n>` is the step number. The answer is read from the log, so no AI is asked to explain itself afterwards.",
    "3. Two instructions conflict (the controversy case). In S3, step 3, the care agent proposes sending customer "
    "identifiers to the AI provider abroad. The gate blocks it under PDPL 22 and 23(2), and refuses even a staff member's "
    "override (logged as `override_refused`). Privacy wins by rule, not by what the model happens to do.",
    "4. Another regulator, another rule. `onyx whatif` re-runs a recorded conversation under a proposed new rule: TDRA's "
    "missing hand-over rule (gap 1) on S2, and the Data Office's missing rule on reviewing an automated decision (gap 4) "
    "on S4. A re-run costs USD 0; a new live run on the model costs USD 0.27 (USD 5.3767 over the 20 scored runs).",
    "A partner asks for subscriber data: held, no verification level set (24.10); the override to send identifiers "
    "abroad: block, no override (PDPL 22, 23(2); gap 5).",
    "Ra'ed Shraim, a data-protection officer outside the team, reviewed the gates' reading of the texts (practice, not "
    "legal advice, no UAE standing); what he found and what changed are in Annex A. Next:",
    "team approval of holds. Annex A to F",
]
REPORT_GONE = [
    "BAU Faculty of AI", "not an institution in a drill", "bar any AI in that seat",
    "expected gaps found 5 of 7 in every run", "2 missed (both S1)", "re-find 5 of the 7 expected gaps",
    "`eval` recomputes every figure", "where its mandate ends", "bounded mandates", "mandate-scoped retrieval",
    "scoped to the agent's mandate", "Claimed on running evidence", "not by the model's mood",
    "interconnection data", "a data-protection practitioner's review", "supervised by",
]
ANNEX_HAS = [
    "An agent's mandate is its fixed list of what it may do and read.",
    "Reviewed on 2026-11-05 by Ra'ed Shraim, Director Business Excellence – DPO, Solidarity First Insurance Company, "
    "Amman – Jordan (practitioner review, not legal advice, no UAE standing): his points on CPR 26.7.2's Arabic, licence "
    "3.4.1 and licence 9.1 are in gap 1 and the rule notes; his code-level points are listed for after the shortlist.",
    "Gap recall counts flags, and only the adviser may flag: flag_gap is in its mandate alone. The S1 key places gap 2 at "
    "the channel classification, which is plain code, and gap 6 at the care agent's offer; neither step calls the "
    "adviser. Its one model turn in S1, step 6, shows it only the renewal question, and no run flagged gaps 2 or 6 there, "
    "so S1 reads 0.33. The keys were not edited; after the shortlist the adviser reads the whole conversation or the care "
    "agent gets the register, and the runs are repeated.",
    "Three runs per cell is enough to show the effect, not to estimate it finely. After the shortlist the same test runs "
    "on more runs, with attacks written by people who have not read the gate's code.",
]


@pytest.mark.parametrize("words", REPORT_HAS)
def test_report_says(words):
    assert words in REPORT


@pytest.mark.parametrize("words", REPORT_GONE)
def test_report_no_longer_says(words):
    assert words not in REPORT


def test_mentor_in_the_header_as_mentor():
    header = REPORT.split("## Introduction")[0]
    assert "**Mentor:** Dr. Wafaa Almaaitah" in header
    assert MENTOR in README


def test_strip_keeps_five_cells():
    row = next(line for line in (REPO / "docs" / "report.md").read_text(encoding="utf-8").splitlines()
               if line.startswith("| 5 scenarios"))
    assert len(row.strip("|").split("|")) == 5 and STRIP_CELL in row


def test_clause_18_prints_the_pair_from_eval():
    assert ("On eight steps we wrote where the subscriber's words try to force a barred act, the gate passed 8 of 48 "
            "before a fix made the same day and 0 of 48 after (Annex C).") in _build().strip_tags(REPORT)


@pytest.mark.parametrize("para, problem", [
    ("It passed 8 of 48 and 0 of 48 `[U8, x]`.", None),
    ("It passed 9 of 48 `[U8, x]`.", "9 of 48"),
    ("It passed 48 of 48 `[U8, x]`.", "48 of 48"),       # the proposed count and the ungoverned count, not the governed pass
    ("It passed 8 of 48 `[C3, x]`.", "8 of 48"),         # the pair belongs to U8 alone
    ("Gaps: the 2 not found (gaps 2 and 6) `[C5, x]`.", None),
    ("Gaps: the 3 not found `[C5, x]`.", "3 not found"),
    ("Gaps: the 2 not found (gaps 2 and 7) `[C5, x]`.", "gaps 2 and 7"),
])
def test_the_value_check_reads_the_new_wording_and_still_fails_a_wrong_figure(para, problem):
    build = _build()
    sets = build.run_sets((REPO / "eval" / "results.md").read_text(encoding="utf-8"))
    problems = build.check_paragraph(para, sets)
    assert problems == [] if problem is None else any(p.startswith(problem + ":") for p in problems)


@pytest.mark.parametrize("words", ANNEX_HAS)
def test_annex_says(words):
    assert words in ANNEX


def test_new_annex_sentences_sit_where_the_order_puts_them():
    assert ANNEX.index("Reviewed on 2026-11-05") < ANNEX.index("## Annex B")
    assert ANNEX.index("The gate decides from the proposal's verb") < ANNEX.index("Reviewed on 2026-11-05")
    limits = ANNEX.split("**What the test does not show.**")[1].split("## Annex D")[0]
    assert limits.rstrip().endswith("and the runs are repeated.")


def test_note_on_the_chapeau_everywhere_it_prints():
    gap = next(g for g in data.load_gaps()["gaps"] if g["id"] == "gap-1")
    assert gap["clause_note"]["note"].endswith(NEW_NOTE)
    for text in (ANNEX, GAPS_MD, GAPS_HTML):
        assert OLD_NOTE not in text
    assert ANNEX.count(NEW_NOTE) == 2 and NEW_NOTE in GAPS_MD and NEW_NOTE in GAPS_HTML


def test_gap_15_quote_is_the_whole_sentence_and_its_arabic_is_unchanged():
    raw = (REPO / "onyx" / "data" / "gaps.json").read_text(encoding="utf-8")
    assert json.dumps(CABINET) in raw
    assert CABINET in GAPS_MD and CABINET in GAPS_HTML


def test_readme_team_case_model_and_after_shortlist():
    assert f"| Onyx | Iyas Shraim (leader), {TEAM} | {FACULTY}, students. {MENTOR} |" in README
    assert "Faculty of AI" not in README and "supervised by" not in README
    assert "- " + CASE in README and "not an institution in a drill" not in README
    assert ("obligation proxy 0.57 / 0.58 (share of key obligations on steps that reached the key's verdict with every "
            "must_cite clause on the step's record); 2 of 112 key steps missed") in README
    bullet = next(line for line in (REPO / "README.md").read_text(encoding="utf-8").splitlines()
                  if line.startswith("- Not changed before submission, listed for after the shortlist"))
    assert bullet.endswith("attacks written by people who have not read the gate's code, on more runs.")


def test_site_definition_and_tile_explain_the_figure():
    assert INDEX.count(TILE) == 1 and INDEX.count(DEF_END) == 1
    assert site.LABELS["gap_recall"] == "Gap recall"
    row = INDEX[INDEX.index('href="#def-gap_recall"') - 200:INDEX.index('href="#def-gap_recall"') + 300]
    assert TILE in row
    assert INDEX.index(DEF_END) > INDEX.index('id="def-gap_recall"')


def test_tile_average_is_what_the_code_computes():
    """Item 22: 0.87 is the mean of the five scenarios' gap recall, S1 being one found of three."""
    results = json.loads((REPO / "eval" / "results.json").read_text(encoding="utf-8"))
    by_scenario = results["c5"]["C5"]["by_scenario"]
    for lang in ("en", "ar"):
        values = [by_scenario[s][lang]["gap_recall"] for s in ("S1", "S2", "S3", "S4", "S5")]
        assert round(values[0], 2) == 0.33 and values[1:] == [1.0, 1.0, 1.0, 1.0]
        assert sum(values) / 5 == pytest.approx(results["c5"]["C5"]["all"][lang]["gap_recall"], abs=0.001)
        assert round(sum(values) / 5, 2) == 0.87


def test_every_annex_table_keeps_its_header_with_its_rows(tmp_path):
    """Item 27: a table header never sits alone at the foot of a page. The main text's tables do not move."""
    from docx import Document

    out = tmp_path / "report.docx"
    assert _build().main(["--out", str(out)]) == 0
    tables = Document(str(out)).tables

    def keeps(table):
        return {p.paragraph_format.keep_with_next for c in table.rows[0].cells for p in c.paragraphs}

    assert [t.rows[0].cells[0].text[:3] for t in tables[:3]] == ["5 s", "Nod", "#"]  # the strip, Y.3172, the gaps
    assert all(keeps(t) == {None} for t in tables[:3])
    assert "Question" in [t.rows[0].cells[0].text for t in tables[3:]]
    assert all(keeps(t) == {True} for t in tables[3:])


def _build():
    spec = importlib.util.spec_from_file_location("build_report", REPO / "docs" / "build_report.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules["build_report"] = module
    spec.loader.exec_module(module)
    return module


COMPARATIVE = ("the only entry", "the only team", "the only system", "first in the", "unlike other", "no other team",
               "no other entry", "none of the other", "the first to", "the only one")


@pytest.mark.parametrize("path", ["docs/report.md", "docs/annex.md", "README.md", "docs/site/index.html"])
def test_no_comparison_with_other_entries(path):
    """Item 25, Iyas's standing rule: Mizan does not say it is the only one of anything."""
    text = _fold((REPO / path).read_text(encoding="utf-8")).lower()
    assert [w for w in COMPARATIVE if w in text] == []
