"""Task 54, audit fixes before the film (docs/work-orders/2026-11-06-task-54-audit-fixes.md)."""

from __future__ import annotations

import ast
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


# --- C.3, C.5: recorded verdicts against the keys (rulings of 2026-11-06, stop 1 and stop 2) ----------------------

DIAGNOSED = {"S3-5", "S4-2", "S4-3", "S5-5", "S5-6"}


def _flat(text: str) -> str:
    return " ".join(text.split())


def _verdicts_paragraph() -> str:
    start = ANNEX.index("**Recorded verdicts against the keys.**")
    return ANNEX[start:ANNEX.index("**What the test does not show.**")]


def test_c3_no_step_the_key_stops_was_allowed():
    """The annex prints this count, so it is computed from the logs and keys, over all 112."""
    counts = {"block": [0, 0], "hold": [0, 0], "allow": [0, 0], "insufficient_evidence": [0, 0]}
    for sid in eval_mod.SCENARIOS:
        key = data.load_key(sid)
        for lang in eval_mod.LANGS:
            for n in range(1, 3):
                events = eval_mod._events(eval_mod.run_path(REPO / "runs" / "c5", sid, n, lang, True))
                for step in key["steps"]:
                    judged = eval_mod.judged_verdicts(events, key, step)
                    cell = counts[step.get("gate_outcome", step["verdict"])]
                    cell[0] += 1
                    cell[1] += any(e["verdict"] == "allow" for e in judged)
    assert (counts["block"], counts["hold"]) == ([20, 0], [28, 0])
    assert sum(cell[0] for cell in counts.values()) == 112
    assert "over all 112 run-steps: key block 20, key hold 28, allowed 0" in _flat(_verdicts_paragraph())


def test_c3_the_annex_paragraph_opens_with_the_count(agreement):
    assert ANNEX.count("**Recorded verdicts against the keys.**") == 1
    assert "**Recorded verdicts against the keys.**" in _annex("## Annex C.", "## Annex D.")
    steps = {r["step"] for r in agreement["differences"]}
    total = sum(len(data.load_key(sid)["steps"]) for sid in eval_mod.SCENARIOS)
    assert (len(steps), total, len(agreement["differences"])) == (9, 28, 26)
    assert ("differs from the key's at 9 of the 28 steps in the keys, 26 of the 112 run-steps (verdict agreement 0.77, en "
            "and ar; `eval/results.md`). In none of the 26 did the gate allow an act the key stops") in _flat(_verdicts_paragraph())


def test_c3_every_differing_step_has_one_row_and_only_five_are_listed_for_the_fix(agreement):
    rows = [line for line in _verdicts_paragraph().splitlines() if line.startswith("| S") and not line.startswith("| Step")]
    assert {row.split("|")[1].strip() for row in rows} == {r["step"] for r in agreement["differences"]}
    assert len(rows) == 9
    listed = {row.split("|")[1].strip() for row in rows if "listed for the fix after the shortlist" in row}
    assert listed == DIAGNOSED


def test_c3_the_s4_3_row_says_the_proposal_kept_the_services():
    """The first ruling's reading ('cut incoming calls') was false against the logs."""
    for run in ("run1", "run2"):
        events = eval_mod._events(REPO / "runs" / "c5" / "S4" / "ar" / f"{run}.jsonl")
        args = next(e["old_value"]["args"] for e in events
                    if e.get("action") == "gate" and e["entity_id"] == "S4-3-care")
        assert "المكالمات الواردة" in args["kept"] and "أرقام الطوارئ" in args["kept"]
    row = next(line for line in _verdicts_paragraph().splitlines() if line.startswith("| S4-3 "))
    assert "kept incoming calls and emergency numbers in Arabic words" in row


def test_c3_the_survey_counts_the_fixed_term_reads():
    """Ruling C: every read_items call with a fixed English term set. The one at services takes its term from a fact."""
    tree = ast.parse((REPO / "onyx" / "gate.py").read_text(encoding="utf-8"))
    calls = [n for n in ast.walk(tree) if isinstance(n, ast.Call) and getattr(n.func, "id", "") == "read_items"]
    fixed = [c for c in calls if not isinstance(c.args[1], ast.IfExp)]
    assert (len(calls), len(fixed)) == (7, 6)
    assert "(6 checks in `onyx/gate.py`)" in _flat(_verdicts_paragraph())


@pytest.mark.parametrize("payload", [["الاسم", "رقم الهاتف"], ["full name", "phone number"]])
def test_c3_an_unmatched_word_is_not_a_held_word(payload):
    """Why the annex does not print 'never allowed': this check stops on a match, so a miss lets the payload through.
    Pinned as found, not as wanted. No recorded run did this. The fix is listed after the shortlist."""
    assert not gate.read_items(payload, gate.DIRECT_IDENTIFIERS) & gate.DIRECT_IDENTIFIERS
    assert "never allowed" not in _verdicts_paragraph()


def test_c5_the_readme_bullet_is_the_rulings():
    assert ("- Nine of the 28 key steps (26 of 112 run-steps) record a gate verdict that differs from the key's: five are "
            "field-shape faults, the gate read a field in a shape the model did not write, in English or in Arabic (S3-5, "
            "S4-2, S4-3, S5-5, S5-6), listed for the fix after the shortlist; at the other four the gate held or blocked "
            "where the key allows, holds or blocks, or the cited clause was not retrieved. In none of the 26 was an act the "
            "key stops allowed. The list: `eval/results.md`, Annex C.") in README


def test_b8_the_annex_says_which_chunks_keep_page_furniture():
    chunks = {c: kb.get_chunk("tdra-cpr-v2-en", c)["text_ar"] for c in ("3.9", "4.7.3", "4.23.2", "24.6", "26.6")}
    assert all("نسخة رقم" in text for text in chunks.values())
    assert "Page 60" in kb.get_chunk("tdra-cpr-v2-en", "24.5")["text_en"]
    flat = _flat(ANNEX)
    assert "five Arabic chunks (CPR 3.9, 4.7.3, 4.23.2, 24.6, 26.6) still carry the page footer" in flat
    assert "Running headers are removed. " not in flat


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
