"""Task 9 (order 2026-10-21-task-9-gaps): the gap register. onyx/data/gaps.json is the single source; docs/gaps.md
and the README's register table are generated from it. Every searched clause resolves to a committed KB chunk and
its quote is verbatim there; every global example quotes a file under kb/sources/global/ that carries its source
line."""

import glob
import json
import re
from pathlib import Path

import pytest

from onyx import data, gaps, kb

ROWS = data.load_gaps()["gaps"]
ORDER_IDS = [f"gap-{n}" for n in range(1, 13)] + ["candidate-4-4-fixed-term-bundle", "candidate-79bis-2-fine-schedule"]
GLOBAL_DIR = kb.KB_DIR / "sources" / "global"
REGISTER_ID = re.compile(r"^(gap-\d+|candidate-[\w-]+)$")


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def test_register_holds_the_order_ids_in_order():
    assert [r["id"] for r in ROWS] == ORDER_IDS


def test_every_row_has_kind_addressee_category():
    for row in ROWS:
        assert row["kind"] in gaps.KINDS, row["id"]
        assert row["category"] in gaps.CATEGORIES, row["id"]
        assert row["addressee"] and all(a in gaps.ADDRESSEES for a in row["addressee"]), row["id"]
        assert row["competitor"] in gaps.COMPETITOR, row["id"]
        for field in ("gap", "uae_position", "recommendation", "exposed_by"):
            assert row[field], f"{row['id']}: {field} empty"


def test_every_gap_cites_searched_clauses_in_kb():
    for row in ROWS + data.load_gaps()["candidates"]:
        row.setdefault("id", row.get("name"))
        assert row["searched"], f"{row['id']}: no clause searched"
        for s in row["searched"]:
            document_id, clause = s["clause"].split(":", 1)
            chunk = kb.get_chunk(document_id, clause)  # KeyError: not a committed chunk
            assert s["says"], s["clause"]
            if s.get("quote"):
                assert _norm(s["quote"]) in _norm(chunk["text_en"]) or _norm(s["quote"]) in _norm(chunk["text_ar"]), \
                    f"{row['id']} {s['clause']}: quote not verbatim in the chunk"


def test_searched_clauses_are_committed_chunks():
    """kb/chunks/ holds the cited clauses, and the register's searched clauses are cited."""
    cited = data.cited_chunks()
    for row in ROWS + data.load_gaps()["candidates"]:
        for s in row["searched"]:
            assert tuple(s["clause"].split(":", 1)) in cited, s["clause"]


def test_every_global_example_is_verified_status():
    for row in ROWS:
        for ex in row["global_examples"] + row.get("standard_text", []):
            assert ex["file"].startswith("kb/sources/global/"), ex["file"]
            assert ex["status"] == "VERIFIED", ex
            assert ex["quote"] and ex["clause"] and ex["document"], ex
        if not row["global_examples"]:
            assert row["global_none"], f"{row['id']}: no example and no reason"


def test_every_global_quote_is_verbatim_in_its_file():
    if not GLOBAL_DIR.exists():
        pytest.skip("kb/sources/global/ is local only (gitignored, addendum item 15)")
    for row in ROWS:
        for ex in row["global_examples"] + row.get("standard_text", []):
            text = kb.read_text(kb.REPO / ex["file"])
            assert text.startswith("Source: http"), f"{ex['file']}: no source line"
            assert _norm(ex["quote"]) in _norm(text), f"{row['id']} {ex['document']} {ex['clause']}: not verbatim"


def test_register_holds_every_id_the_runs_and_keys_flag():
    ids = {r["id"] for r in ROWS}
    expected = {g for sid in ("S1", "S2", "S3", "S4", "S5") for g in data.load_key(sid)["gaps_expected"]}
    assert expected <= ids
    flagged = set()
    for path in glob.glob(str(kb.REPO / "runs" / "**" / "*.jsonl"), recursive=True):
        for line in Path(path).read_text(encoding="utf-8").splitlines():
            e = json.loads(line)
            old, new = e.get("old_value"), e.get("new_value")
            if isinstance(old, dict) and old.get("verb") == "flag_gap":
                flagged.add(str((old.get("args") or {}).get("gap") or old.get("target")))
            if e.get("action") == "abstain" and isinstance(new, dict):
                flagged |= {str(g) for g in new.get("gaps") or []}
    assert {g for g in flagged if REGISTER_ID.match(g)} <= ids


def test_gaps_md_is_generated_and_stable(tmp_path):
    out = tmp_path / "gaps.md"
    gaps.write(out, readme=None)
    first = out.read_bytes()
    gaps.write(out, readme=None)
    assert out.read_bytes() == first
    assert first == (kb.REPO / "docs" / "gaps.md").read_bytes(), "docs/gaps.md is stale: run python -m onyx gaps"


def test_readme_leads_with_the_register():
    readme = (kb.REPO / "README.md").read_text(encoding="utf-8")
    table = gaps.table()
    assert table in readme, "README register table is stale: run python -m onyx gaps"
    headings = re.findall(r"^## (.+)$", readme, re.MULTILINE)
    # order Task 16 item 3: Why and Three things lead, then the register (was order 2026-10-21-task-9 item 6)
    assert headings[:5] == ["For the reviewer", "Why", "Three things to look at first", "Gap register",
                            "Run it without a key"]  # Task 18 item 5: the reviewer block leads
    assert table.count("\n| ") == len(ROWS) + 1  # the separator row plus one row per gap


# --- order 2026-10-21-task-9-fixes-tasks-10-11, Part A ------------------------------------------------------------

# reworded by order 2026-10-24 Task 23, B2
GAP_7 = ("No binding UAE text sets conduct standards specific to an AI agent dealing with a consumer: CPR 3.3's duty of "
         "fairness and accurate information is general; Trade Law 14/2023 names AI in its definition (Art 1) and bars "
         "misleading dealing (Art 5(7)); nothing names disclosure, limits, escalation or a hand-over for an automated "
         "agent.")


def test_gap_7_is_hqs_text_and_a_standards_gap():
    [row] = [r for r in ROWS if r["id"] == "gap-7"]
    assert row["line"] == "five mentions no standard"
    assert row["gap"] == GAP_7
    assert row["category"] == "standards gap"
    searched = {s["clause"] for s in row["searched"]}
    # etransactions 13 is left out: its chunk is the heading "Acknowledgment of Receipt" (report-back)
    assert {"pdpl-45-2021-en:18(4)", "etransactions-46-2021-en:11(2)", "etransactions-46-2021-en:12(2)",
            "cabinet-57-2024-en:7"} <= searched


def test_public_outputs_carry_no_competitor_column(tmp_path):
    readme = tmp_path / "README.md"
    readme.write_text(gaps.README.read_text(encoding="utf-8"), encoding="utf-8")
    gaps.write(tmp_path / "gaps.md", readme)
    for path in (tmp_path / "gaps.md", readme):
        assert "competitor" not in path.read_text(encoding="utf-8").lower(), path.name
    assert all("competitor" in row for row in ROWS)  # hq's internal note stays in gaps.json


# --- order 2026-10-22-task-15-gap-9-child -------------------------------------------------------------------------

# reworded by order 2026-10-24 Task 23, B2
GAP_9 = ("A child on the line: the caregiver signs the terms (Child Digital Safety Law 26/2025, 11(1)(b)) and under-13 "
         "data needs verified caregiver consent (7(1)); the Art 11 instructions to providers and the Art 16 penalties are "
         "unpublished, and Cabinet Resolution 106/2026's age checks reach social media platforms only (Art 2); nothing "
         "says how a telecom channel learns the person is a child.")
COPPA = {"312.5(a)(1)": "obtain verifiable parental consent before any collection, use, or disclosure of personal "
                        "information from children",
         "312.5(b)(1)": "reasonably calculated, in light of available technology, to ensure that the person providing "
                        "consent is the child's parent"}
CDS = "child-digital-safety-26-2025-en"


def _row(rid):
    [row] = [r for r in ROWS if r["id"] == rid]
    return row


def test_gap_9_is_the_orders_text():
    row = _row("gap-9")
    assert row["gap"] == GAP_9
    assert (row["kind"], row["category"], row["addressee"]) == ("method", "legislative gap", ["TDRA", "Cabinet"])
    assert row["exposed_by"] == "mapping (SRC, P); U2 (drill bank, not run)"
    assert row["uae_position"].startswith("The duty is the law's own words; the operator's licence 3.2 makes it")
    assert "'Self-declaration of age ... shall not be recognized' (Art 4(3))" in row["uae_position"]
    assert row["uae_position"].endswith("it is not on the TDRA Regulations and Ruling register.")
    assert row["recommendation"].startswith("TDRA to issue the Art 11 instructions with the caregiver check")
    assert row["recommendation"].endswith("can name a list of the same shape for telecom channels.")


def test_gap_9_searches_the_orders_clauses():
    searched = [s["clause"] for s in _row("gap-9")["searched"]]
    # 10(1)(g) sits in chunk 10(1) and 11(2) in chunk 11(1): the chunker keeps them together, as gap-7 cites 10(1)
    assert searched == [f"{CDS}:7(1)", f"{CDS}:9(2)", f"{CDS}:10(1)", f"{CDS}:11(1)", f"{CDS}:11(1)",
                        "tdra-cpr-v2-en:4.3", "tdra-cpr-v2-en:4.7"]


def test_gap_9_arabic_is_verbatim_in_the_source_file():
    [ar] = [s for s in _row("gap-9")["searched"] if s.get("quote_ar")]
    assert ar["clause"] == f"{CDS}:11(1)" and ar["file_ar"] == "docs/sources/child-digital-safety-law-26-2025-ar.txt"
    assert _norm(ar["quote_ar"]) in _norm((kb.REPO / ar["file_ar"]).read_text(encoding="utf-8"))


def test_gap_9_global_example_is_coppa_312_5():
    examples = _row("gap-9")["global_examples"]
    assert {ex["clause"]: ex["quote"] for ex in examples} == COPPA
    assert {ex["file"] for ex in examples} == {"kb/sources/global/coppa-16cfr312-5.txt"}
    assert "16 CFR 312.5(a)(1); 16 CFR 312.5(b)(1)" in gaps.table()


def test_coppa_quotes_are_verbatim_in_the_fetched_file():
    path = GLOBAL_DIR / "coppa-16cfr312-5.txt"
    if not path.exists():
        pytest.skip("kb/sources/global/ is local only (gitignored, addendum item 15)")
    text = path.read_text(encoding="utf-8")
    assert text.startswith("Source: https://www.ecfr.gov/")
    for quote in COPPA.values():
        assert _norm(quote) in _norm(text)


def test_candidate_79bis_2_row():
    row = _row("candidate-79bis-2-fine-schedule")
    # gap text: hq's rewrite, order 2026-10-22 Task 16 item 4 (tests/test_pages_grounding_readme.py)
    assert (row["kind"], row["addressee"], row["global_examples"]) == ("absence", ["Cabinet"], [])
    assert row["exposed_by"] == "mapping (P)"
    # 79 bis (1) and (2) are one chunk, 79 bis
    assert [s["clause"] for s in row["searched"]][:3] == ["telecom-law-3-2003-en:79 bis", "telecom-law-3-2003-en:79 bis",
                                                          "licence-2-2026:16.3.2"]


def test_readme_register_has_twelve_rows_and_the_child_left_the_candidates():
    readme = (kb.REPO / "README.md").read_text(encoding="utf-8")
    table = readme.split(gaps.START, 1)[1].split(gaps.END, 1)[0]
    assert table.count("\n| ") == 14 + 2  # gap-1 to gap-12 (Task 27) and two candidate rows, plus header and separator
    names = [c["name"] for c in data.load_gaps()["candidates"]]
    assert "A child on the line" not in names and len(names) == 4  # Task 23 B3: sub-processor authorisation added
    assert "### A child on the line" not in (kb.REPO / "docs" / "gaps.md").read_text(encoding="utf-8")


def test_adviser_register_lists_gap_9_and_the_candidate():
    from onyx.agents.adviser import Adviser
    text = "\n".join(Adviser.extra_lines(None))  # the register lines read no instance state
    assert "9. gap-9: " in text and "14. candidate-79bis-2-fine-schedule: " in text  # gap-10, 11, 12 at lines 10 to 12 (Tasks 20, 23, 27)


# --- order 2026-10-24-task-20-gap-10-arabic-parity ----------------------------------------------------------------

GAP_10 = ("Arabic on an automated channel: the texts set the language (CPR 3.2.2: written information in Arabic or "
          "English as the Consumer prefers, both if unknown; Consumer Law 26: data, advertisements and contracts in "
          "Arabic; 8(4): the invoice in Arabic; Cabinet 66/2023 Annex 2: AED 100,000 for each) and none sets the "
          "quality: no binding text requires an automated channel to answer as well in Arabic as in English, and the "
          "QoS Policy v3.0 has no indicator per language.")
CANADA = {"s. 22": "Every federal institution has the duty to ensure that any member of the public can communicate with "
                   "and obtain available services from its head or central office in either official language",
          "s. 26": "Every federal institution that regulates persons or organizations with respect to any of their "
                   "activities that relate to the health, safety or security of members of the public has the duty to "
                   "ensure, through its regulation of those persons or organizations, wherever it is reasonable to do "
                   "so in the circumstances, that members of the public can communicate with and obtain available "
                   "services from those persons or organizations in relation to those activities in both official "
                   "languages.",
          "s. 27": "the duty applies in respect of oral and written communications and in respect of any documents or "
                   "activities that relate to those communications or services."}
NEW_CHUNKS = [("tdra-cpr-v2-en", "4.25.3"), ("tdra-cpr-v2-en", "17.3"), ("consumer-law-15-2020-en", "25(1)"),
              ("consumer-law-15-2020-en", "26"), ("licence-2-2026", "16.7")]


def test_gap_10_is_the_orders_text():
    row = _row("gap-10")
    assert row["line"] == "Arabic at equal quality" and row["gap"] == GAP_10
    assert (row["kind"], row["category"], row["addressee"]) == ("method", "standards gap", ["TDRA"])
    assert row["exposed_by"] == "C5 per-language scoring (M, D nodes); mapping (SRC)"
    assert row["uae_position"].startswith("The language duty is binding and fined; Mizan meets it by answering")
    assert "action recall 0.96 English and 0.94 Arabic, citation validity 0.99 and 1.00" in row["uae_position"]
    assert row["uae_position"].endswith("Searched 2026-10-24 in both languages.")
    assert row["recommendation"].startswith("TDRA to add to the QoS Policy, for every automated consumer channel")
    assert row["recommendation"].endswith("and s. 27 extends it to oral channels.")
    # the order's basis names two entries; no other entry is named in a tracked file (Task 16 ruling), so it is held unnamed
    assert row["competitor"] == "no" and row["competitor_basis"].endswith("which is why the candidate was searched.")


def test_gap_10_searches_the_orders_clauses():
    searched = [s["clause"] for s in _row("gap-10")["searched"]]
    assert searched == ["tdra-cpr-v2-en:3.2.2", "tdra-cpr-v2-en:4.25.3", "tdra-cpr-v2-en:17.3",
                        "consumer-law-15-2020-en:26", "consumer-law-15-2020-en:25(1)", "consumer-law-15-2020-en:8(4)",
                        "cabinet-66-2023-en:43(5)", "licence-2-2026:16.7", "qos-v3-en:9.5",
                        "tdra-cpr-v2-en:26.2", "tdra-cpr-v2-en:26.6"]  # order 2026-10-25 Task 26, A5
    assert "inferred" in _row("gap-10")["searched"][0]["says"]  # 3.2.1 (electronic form) reaches an app chat


def test_gap_10_new_chunks_are_committed_once_each():
    for document_id, clause in NEW_CHUNKS:
        lines = (kb.KB_DIR / "chunks" / f"{document_id}.jsonl").read_text(encoding="utf-8").splitlines()
        assert sum(json.loads(line)["clause"] == clause for line in lines) == 1, (document_id, clause)


def test_gap_10_framework_line_is_readiness_dimension_6_non_binding():
    [fw] = _row("gap-10")["framework"]
    assert fw["status"] == "NON-BINDING" and fw["page"] == 23
    assert fw["quote"] == "Availability of AI models in the local language used in the human interface"
    assert "(p. 23; framework, non-binding)" in gaps.render()
    path = kb.REPO / fw["file"]
    if not path.exists():
        pytest.skip("kb/sources/ is local only")
    assert fw["quote"] in path.read_text(encoding="utf-8")


def test_gap_10_global_example_is_canada_ola_part_iv():
    examples = _row("gap-10")["global_examples"]
    assert {ex["clause"]: ex["quote"] for ex in examples} == CANADA
    assert {ex["file"] for ex in examples} == {"kb/sources/global/canada-ola-part-iv.txt"}
    assert "Canada OLA s. 22; Canada OLA s. 26; Canada OLA s. 27" in gaps.table()


def test_canada_quotes_are_verbatim_in_the_fetched_file():
    path = GLOBAL_DIR / "canada-ola-part-iv.txt"
    if not path.exists():
        pytest.skip("kb/sources/global/ is local only (gitignored, addendum item 15)")
    text = path.read_text(encoding="utf-8")
    assert text.startswith("Source: https://laws-lois.justice.gc.ca/eng/acts/O-3.01/")
    for quote in CANADA.values():
        assert _norm(quote) in _norm(text)


def test_arabic_records_candidate_is_unchanged():
    [cand] = [c for c in data.load_gaps()["candidates"] if c["name"] == "Arabic records"]
    assert [s["clause"] for s in cand["searched"]] == ["consumer-law-15-2020-en:8(4)", "cabinet-66-2023-en:43(5)",
                                                       "consumer-law-15-2020-en:4(5)"]


def test_adviser_register_lists_gap_10():
    from onyx.agents.adviser import Adviser
    assert "10. gap-10: Arabic at equal quality" in "\n".join(Adviser.extra_lines(None))


# --- order 2026-10-25 Task 26: rows 1 and 2 pre-empt the CPR clocks and PDPL 4(9); searched lists extended ----------

TASK_26_ADDED = {
    "gap-1": ["tdra-cpr-v2-en:26.2", "tdra-cpr-v2-en:26.6", "tdra-cpr-v2-en:26.13.2", "tdra-cpr-v2-en:26.13.3",
              "tdra-cpr-v2-en:26.14.1", "tdra-cpr-v2-en:26.14.2"],
    "gap-2": ["pdpl-45-2021-en:4(9)"],
    "gap-4": ["pdpl-45-2021-en:11(1)", "pdpl-45-2021-en:12(2)"],  # 11(1)(b) cites its parent chunk (hq ruling 2026-10-26)
    "gap-10": ["tdra-cpr-v2-en:26.2", "tdra-cpr-v2-en:26.6"],
    "gap-11": ["etransactions-46-2021-en:12(4)", "etransactions-46-2021-en:13(5)"],  # 12(4)(c) likewise
}


def test_task_26_searched_entries_are_placed_as_ordered():
    clauses = {rid: [s["clause"] for s in _row(rid)["searched"]] for rid in TASK_26_ADDED}
    after = {"gap-1": "tdra-cpr-v2-en:26.13.1", "gap-4": "pdpl-45-2021-en:18(4)",
             "gap-10": "qos-v3-en:9.5", "gap-11": "etransactions-46-2021-en:12(7)"}
    for rid, prev in after.items():
        i = clauses[rid].index(prev) + 1
        assert clauses[rid][i:i + len(TASK_26_ADDED[rid])] == TASK_26_ADDED[rid], rid
    i = clauses["gap-2"].index("pdpl-45-2021-en:6(1)")
    assert clauses["gap-2"][i - 1] == "pdpl-45-2021-en:4(9)"
    for rid in TASK_26_ADDED:
        for s in _row(rid)["searched"]:
            if s["clause"] in TASK_26_ADDED[rid]:
                assert sorted(s) == ["clause", "quote", "says"], (rid, s["clause"])
    assert _row("gap-4")["searched"][clauses["gap-4"].index("pdpl-45-2021-en:11(1)")]["says"].startswith("11(1)(b)")
    assert _row("gap-11")["searched"][clauses["gap-11"].index("etransactions-46-2021-en:12(4)")]["says"].startswith(
        "12(4)(c)")


def test_task_26_rows_1_and_2_name_the_clocks_and_4_9():
    assert "the complaint has clocks (acknowledge at once by telephone, 26.13.3; conclude in twenty business days, " \
           "26.14.2); the transfer has none" in _row("gap-1")["gap"]
    assert _row("gap-1")["uae_position"].endswith("and a reference number is not a conversation.")
    assert "the PDPL permits the processing the contract needs without consent (4(9))" in _row("gap-2")["gap"]
    assert "one spoken 'yes' buys the service and consents to nothing beyond it" in _row("gap-2")["gap"]
    assert "The processing the contract needs is lawful without consent (4(9))" in _row("gap-2")["uae_position"]


# --- order 2026-10-26 Task 27: gap-12, where an agent's authority ends (hq ruling task-27-stop-ruling-2026-10-26) ----

READINESS_TEXT = GLOBAL_DIR / "itu-ai-readiness-report-2-0-2026-01.txt"


def test_gap_12_row_is_the_orders():
    row = _row("gap-12")
    assert row["line"] == "No metric for where an agent's authority ends"
    assert (row["kind"], row["category"], row["addressee"], row["exposed_by"]) == (
        "absence", "standards gap", ["ITU"], "S1")
    assert row["competitor"] == "no" and row["global_none"] == ""
    assert [s["clause"] for s in row["searched"]] == [
        "itu-t-y3173:3.2.1", "itu-t-y3173:6.1", "itu-t-y3173:7.2", "itu-t-y3173:7.2", "itu-t-y3173:8.2",
        "itu-t-y3173:9", "itu-t-y3173:9"]  # Readiness 2.0 is framework, not searched (ruling item 1)
    for s in row["searched"]:
        assert sorted(s) == ["clause", "page", "quote", "says"], s["clause"]
    for s in row["searched"][-2:]:  # Appendix I.1 through chunk 9 (ruling item 2)
        assert s["says"].startswith("Appendix I.1, Table I.1 (the chunker folds the appendices into clause 9)")
    assert len(row["standard_text"]) == 3 and len(row["global_examples"]) == 2


def test_gap_12_readiness_is_nine_non_binding_framework_lines():
    framework = _row("gap-12")["framework"]
    assert [fw["page"] for fw in framework] == [12, 23, 25, 27, 29, 31, "35 to 36", 40, 47]
    assert [fw["clause"] for fw in framework] == ["Basic Framework", "D5", "D8", "D9", "D10", "D11",
                                                  "ch. 4 gap list", "REQ-027 NOTE", "FAQ 11"]
    for fw in framework:
        assert fw["status"] == "NON-BINDING" and fw["file"] == "kb/sources/global/itu-ai-readiness-report-2-0-2026-01.txt"
        assert fw["document"].startswith("ITU AI Readiness 2.0 (2026-01)") and fw["says"] and fw["quote"]


def test_gap_12_framework_quotes_are_verbatim_in_the_readiness_text():
    if not READINESS_TEXT.exists():
        pytest.skip("kb/sources/global/ is local only (gitignored, addendum item 15)")
    text = READINESS_TEXT.read_text(encoding="utf-8")
    assert text.startswith("Source: https://www.itu.int/dms_pub/itu-t/opb/ai4g/T-AI4G-AI4GOOD-2025-6-PDF-E.pdf")
    for fw in _row("gap-12")["framework"]:
        assert _norm(fw["quote"]) in _norm(text), fw["clause"]


def test_gap_12_note_is_under_its_heading_and_the_keys_do_not_flag_it():
    md = gaps.render()
    section = md.split("## gap-12:", 1)[1].split("\n## ", 1)[0]
    assert "Found after the scored runs; S1's expected gaps and the keys are unchanged, so C5 gap recall does not " \
           "count it." in section
    assert all("gap-12" not in data.load_key(sid)["gaps_expected"] for sid in ("S1", "S2", "S3", "S4", "S5"))
    assert "SAE J3016 (Y.3173 Table I.1) level 3" in gaps.table()
