"""Task 54, audit fixes before the film (docs/work-orders/2026-11-06-task-54-audit-fixes.md)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from onyx import data, eval as eval_mod, gate, kb, replay_page, replay_viewer

REPO = Path(__file__).resolve().parents[1]
ANNEX = (REPO / "docs" / "annex.md").read_text(encoding="utf-8")
README = (REPO / "README.md").read_text(encoding="utf-8")
RULES = {r["id"]: r for r in data.load_rules()}
ARABIC_ONLY = "Arabic-only text; no official English on file"


def _annex(start: str, end: str) -> str:
    return ANNEX[ANNEX.index(start):ANNEX.index(end)]


# --- A: annex text ---------------------------------------------------------------------------------------------

def test_a1_the_annex_counts_the_deciding_functions_gates_maps():
    functions = {f for v in gate.GATES.values() for f in (v if isinstance(v, (list, tuple)) else [v])}
    assert (len(gate.GATES), len(functions)) == (16, 17)
    assert ("17 deciding functions in `onyx/gate.py` (three of them added on 2026-11-06 behind the gate-version flag, "
            "Annex C), mapped in `GATES` from the 16 verbs") in " ".join(ANNEX.split())


def test_a2_the_four_clause_block_stands_once_in_annex_b():
    assert ANNEX.count("**CPR 26.6 and 26.7 read together.**") == 1
    assert "**CPR 26.6 and 26.7 read together.**" in _annex("## Annex B.", "## Annex C.")
    assert ("CPR 26.6 and 26.7, the four clauses in both languages and our reading: Annex B."
            in _annex("## Annex C.", "## Annex D."))


def test_a4_the_u8_bound_is_per_run():
    assert "a count of zero bounds the true per-run rate at about 39%" in ANNEX
    assert "upper bound about 39% per run" in README


def test_a5_annex_f_names_the_gaps_it_holds():
    assert "Gap 7 and gaps 13 to 15 are below." in _annex("## Annex F.", "**F.1 Gap 7")


def test_a7_the_annex_says_which_rules_carry_arabic():
    counts = {}
    for path in (REPO / "kb" / "chunks").glob("*.jsonl"):
        for line in path.read_text(encoding="utf-8").splitlines():
            chunk = json.loads(line)
            if chunk["text_ar"]:
                counts[chunk["document_id"]] = counts.get(chunk["document_id"], 0) + 1
    assert counts == {"tdra-cpr-v2-en": 71, "decision-16-2026-ar": 2, "licence-2-2026": 1,
                      "wam-2026-08-21-agentic-ai-guide": 3}
    assert kb.get_chunk("licence-2-2026", "9.1")["text_ar"]
    assert ("each rule carrying its clause, page and verbatim quote, and the clause's Arabic text where the chunk holds "
            "it (every CPR clause, Decision 16/2026, licence 9.1, three clauses of the agentic guide; the PDPL and the "
            "other texts are English-only on file, Annex A)") in " ".join(ANNEX.split())


# --- B: replay pages -------------------------------------------------------------------------------------------

def test_b1_rule_texts_read_the_chunk():
    en, ar = replay_page.rule_texts(RULES["cpr-24-10"])
    assert en == RULES["cpr-24-10"]["quote"]
    assert RULES["cpr-24-10"]["quote_ar"] == "" and ar == " ".join(kb.get_chunk("tdra-cpr-v2-en", "24.10")["text_ar"].split())


def test_b1_rule_texts_fall_back_to_the_quote_ar_then_to_nothing():
    rule = {"document_id": "pdpl-45-2021-en", "chunk": "no such clause", "quote": "words", "quote_ar": "نص"}
    assert replay_page.rule_texts(rule) == ("words", "نص")
    assert replay_page.rule_texts({**rule, "quote_ar": ""}) == ("words", "")


def test_b1_rule_texts_fill_an_empty_quote_from_the_chunk():
    en = kb.get_chunk("tdra-cpr-v2-en", "24.10")["text_en"]
    assert replay_page.rule_texts({**RULES["cpr-24-10"], "quote": ""})[0] == " ".join(en.split())


def test_b1_clauses_searched_print_the_chunks_arabic():
    page = replay_page.render(replay_page.source("S5"))
    searched = page[page.index("Clauses searched"):]
    arabic = [r for r in RULES.values() if r["document_id"] == "tdra-cpr-v2-en"]
    assert any(f'{r["label"]} ' in searched and " ".join(kb.get_chunk(r["document_id"], r["chunk"])["text_ar"].split())
               in searched for r in arabic)
    # a clause whose chunk truly has no Arabic still says so
    assert 'Spam Calls v4 14.3 [binding, UAE] AR: "no Arabic text on file"' in searched


def test_b2_an_arabic_only_document_is_labelled():
    rule = RULES["d16-4-17"]
    assert replay_page.rule_texts(rule)[0] == ""
    lines = replay_page._clauses(["d16-4-17"], RULES)
    assert lines[0].endswith(f': AR: "{rule["quote"]}"')
    assert lines[1] == f"    - EN: {ARABIC_ONLY}"
    searched = replay_page._searched({"label": rule["label"], "rule": "d16-4-17", "says": rule["quote"]}, RULES)
    assert searched[0].endswith(f"EN: {ARABIC_ONLY}") and ' AR: "' in searched[1] and rule["quote"] in searched[1]


@pytest.mark.parametrize("sid", replay_page.SCENARIOS)
def test_b2_no_arabic_text_is_printed_under_en(sid):
    for line in replay_page.render(replay_page.source(sid)).splitlines():
        if " EN: \"" in line:
            quoted = line.split(' EN: "', 1)[1]
            assert not kb._is_arabic(quoted), line


def test_b3_a_verdict_with_no_clause_prints_the_logs_base_check():
    page = replay_page.render(replay_page.RUNS / "c5" / "S5" / "run1.jsonl")
    assert ("- Gate on `request_report`: **block**\n  - base check: deadline 'three business days from 2026-10-19' is "
            "not a rules.json rule, value and unit") in page


def test_b3_no_verdict_stands_bare_on_a_shown_page():
    for sid in replay_page.SCENARIOS:
        lines = replay_page.render(replay_page.source(sid)).splitlines()
        for i, line in enumerate(lines):
            if line.startswith("- Gate on "):
                assert lines[i + 1].startswith("  - "), (sid, line)


def test_b1_b2_b3_the_viewer_reads_the_same_fields():
    viewer = replay_viewer.Viewer()
    cpr = viewer.clause("cpr-24-10")
    assert kb.get_chunk("tdra-cpr-v2-en", "24.10")["text_ar"].split()[0] in cpr and 'data-lang="ar"' in cpr
    d16 = viewer.clause("d16-4-17")
    assert f"EN: {ARABIC_ONLY}" in d16 and "AR: " in d16
    html = (REPO / "docs" / "replay" / "index.html").read_text(encoding="utf-8")
    assert "base check: deadline &#x27;three business days from 2026-10-19&#x27;" in html


# --- C.4: verdict agreement ------------------------------------------------------------------------------------

@pytest.fixture(scope="module")
def agreement():
    return eval_mod.verdict_agreement(REPO / "runs" / "c5")


def test_c4_verdict_agreement_counts(agreement):
    assert (agreement["en"]["hits"], agreement["en"]["n"]) == (43, 56)
    assert (agreement["ar"]["hits"], agreement["ar"]["n"]) == (43, 56)
    assert (agreement["pooled"]["hits"], agreement["pooled"]["n"]) == (86, 112)
    low, high = agreement["pooled"]["ci95"]
    assert low < 86 / 112 < high
    assert sum(agreement["by_scenario"][sid]["pooled"]["n"] for sid in agreement["by_scenario"]) == 112
    assert sum(agreement["by_scenario"][sid]["pooled"]["hits"] for sid in agreement["by_scenario"]) == 86


def test_c4_every_difference_is_listed_with_the_keys_verdict(agreement):
    rows = agreement["differences"]
    assert len(rows) == 112 - 86
    assert {r["step"] for r in rows} == {"S2-4", "S3-2", "S3-5", "S4-1", "S4-2", "S4-3", "S5-3", "S5-5", "S5-6"}
    s35 = [r for r in rows if r["step"] == "S3-5"]
    assert len(s35) == 4 and all((r["key"], r["recorded"]) == ("block", ["hold"]) for r in s35)
    s56 = [r for r in rows if r["step"] == "S5-6"]
    assert len(s56) == 4 and all(r["key"] == "allow" and r["recorded"] == ["block"] and not r["clauses"] for r in s56)
    assert "deadline" in s56[0]["reason"]


def test_c4_results_print_the_figure_and_leave_the_report_alone(agreement):
    results = json.loads((REPO / "eval" / "results.json").read_text(encoding="utf-8"))
    assert results["c5"]["verdict_agreement"] == json.loads(json.dumps(agreement))
    md = (REPO / "eval" / "results.md").read_text(encoding="utf-8")
    assert "## Verdict agreement against the keys (C5)" in md
    assert "en 43 of 56" in md and "ar 43 of 56" in md and "pooled 86 of 112" in md
    report = (REPO / "docs" / "report.md").read_text(encoding="utf-8")
    assert "erdict agreement" not in report, "Fable's change 4: the Results line does not change"


def test_c4_the_annex_definition_carries_the_figure(agreement):
    pooled = agreement["pooled"]
    interval = f"{pooled['ci95'][0]:.2f} to {pooled['ci95'][1]:.2f}"
    assert ("Action recall scores the proposed verb and addressee against the key; verdict agreement (the gate's verdict "
            f"equals the key's) is 0.77 / 0.77, 86 of 112 key steps, 95% interval {interval}, printed in "
            "`eval/results.md`, en / ar.") in " ".join(ANNEX.split())
