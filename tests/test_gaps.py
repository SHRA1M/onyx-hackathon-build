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
# Task 41: gap-13 and gap-14 promoted from the prose candidates, the 79 bis (2) candidate promoted to gap-15
ORDER_IDS = [f"gap-{n}" for n in range(1, 16)] + ["candidate-4-4-fixed-term-bundle"]
GLOBAL_DIR = kb.KB_DIR / "sources" / "global"
REGISTER_ID = re.compile(r"^(gap-\d+|candidate-[\w-]+)$")


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def test_register_holds_the_order_ids_in_order():
    assert [r["id"] for r in ROWS] == ORDER_IDS, "Task 41: 15 gaps and the 4.4 candidate row (16 rows)"


def test_every_row_has_kind_addressee_category():
    for row in ROWS:
        assert row["kind"] in gaps.KINDS, row["id"]
        assert row["category"] in gaps.CATEGORIES, row["id"]
        assert row["addressee"] and all(gaps.addressee_ok(a) for a in row["addressee"]), row["id"]
        assert row["competitor"] in gaps.COMPETITOR, row["id"]
        for field in ("gap", "uae_position", "recommendation", "exposed_by"):
            assert row[field], f"{row['id']}: {field} empty"


def test_every_gap_cites_searched_clauses_in_kb():
    for row in ROWS + data.load_gaps()["candidates"]:
        row.setdefault("id", row.get("name"))
        assert row["searched"], f"{row['id']}: no clause searched"
        for s in row["searched"]:
            assert s["says"], s["clause"]
            if s.get("file") or s.get("url"):  # stored source or URL, no chunk (Task 32, Task 35b): own tests
                continue
            document_id, clause = s["clause"].split(":", 1)
            chunk = kb.get_chunk(document_id, clause)  # KeyError: not a committed chunk
            if s.get("quote"):
                assert _norm(s["quote"]) in _norm(chunk["text_en"]) or _norm(s["quote"]) in _norm(chunk["text_ar"]), \
                    f"{row['id']} {s['clause']}: quote not verbatim in the chunk"


def test_searched_clauses_are_committed_chunks():
    """kb/chunks/ holds the cited clauses, and the register's searched clauses are cited."""
    cited = data.cited_chunks()
    for row in ROWS + data.load_gaps()["candidates"]:
        for s in row["searched"]:
            if not (s.get("file") or s.get("url")):  # a URL-cited text has no chunk (Task 35b)
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
                        "tdra-cpr-v2-en:4.3", "tdra-cpr-v2-en:4.7",
                        "cabres-106-2026-en:2", "cabres-106-2026-en:4(3)"]  # Task 32


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


def test_gap_15_is_the_79bis_2_row():
    row = _row("gap-15")  # the 79 bis (2) candidate, promoted by Task 41
    # gap text: hq's rewrite, order 2026-10-22 Task 16 item 4 (tests/test_pages_grounding_readme.py)
    assert (row["kind"], row["addressee"]) == ("absence", ["Cabinet"])
    assert [(e["clause"], e["file"]) for e in row["global_examples"]] == [
        ("1.11", "kb/sources/global/uk-ofcom-penalty-guidelines-2017.txt"),
        ("1.2", "kb/sources/global/uk-ofcom-penalty-guidelines-2017.txt")] and row["global_none"] == ""
    assert row["exposed_by"] == "mapping (P)"
    # 79 bis (1) and (2) are one chunk, 79 bis
    assert [s["clause"] for s in row["searched"]][:3] == ["telecom-law-3-2003-en:79 bis", "telecom-law-3-2003-en:79 bis",
                                                          "licence-2-2026:16.3.2"]


def test_readme_register_has_fifteen_gaps_and_the_child_left_the_candidates():
    readme = (kb.REPO / "README.md").read_text(encoding="utf-8")
    table = readme.split(gaps.START, 1)[1].split(gaps.END, 1)[0]
    assert table.count("\n| ") == 16 + 2, "Task 41: gap-1 to gap-15 and the 4.4 candidate row, plus header and separator"
    names = [c["name"] for c in data.load_gaps()["candidates"]]
    assert "A child on the line" not in names
    assert names == ["Arabic records"], "Task 41: breach notice and sub-processor promoted, the Executive Order moved"
    assert "### A child on the line" not in (kb.REPO / "docs" / "gaps.md").read_text(encoding="utf-8")


def test_adviser_register_lists_gap_9_and_the_candidate():
    from onyx.agents.adviser import Adviser
    text = "\n".join(Adviser.extra_lines(None))  # the register lines read no instance state
    assert "9. gap-9: " in text and "15. gap-15: " in text  # Task 41: gap-13 to gap-15 at lines 13 to 15
    assert "16. candidate-4-4-fixed-term-bundle: " in text, "Task 41: the 4.4 candidate moves to line 16"


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
    assert "action recall 0.96 English and 1.00 Arabic, citation validity 0.99 and 1.00" in row["uae_position"]
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
                        "tdra-cpr-v2-en:26.2", "tdra-cpr-v2-en:26.6",  # order 2026-10-25 Task 26, A5
                        "du-code-of-practice-en:Annex 1",  # Task 32
                        "saudi-cst-user-protection-552-1445-en:9.2.2", "saudi-cst-user-protection-552-1445-en:16.4",
                        "saudi-cst-user-protection-552-1445-en:26.6"]  # Task 35
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
    canada = [ex for ex in examples if ex["file"] == "kb/sources/global/canada-ola-part-iv.txt"]
    assert {ex["clause"]: ex["quote"] for ex in canada} == CANADA  # Wales joined beside it (Task 30)
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
    earlier = row["searched"][:-len(TASK_35_SEARCHED["gap-12"])]  # Task 35 appends three filed entries
    assert [s["clause"] for s in earlier] == [
        "itu-t-y3173:3.2.1", "itu-t-y3173:6.1", "itu-t-y3173:7.2", "itu-t-y3173:7.2", "itu-t-y3173:8.2",
        "itu-t-y3173:9", "itu-t-y3173:9"]  # Readiness 2.0 is framework, not searched (ruling item 1)
    for s in earlier:
        assert sorted(s) == ["clause", "page", "quote", "says"], s["clause"]
    for s in earlier[-2:]:  # Appendix I.1 through chunk 9 (ruling item 2)
        assert s["says"].startswith("Appendix I.1, Table I.1 (the chunker folds the appendices into clause 9)")
    assert len(row["standard_text"]) == 3 and len(row["global_examples"]) == 5  # SAE L3, L4; roaming x2, AI Act (Task 31)


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


# --- order 2026-10-30-task-30-global-examples -----------------------------------------------------------------

SPAIN = "kb/sources/global/es-ley-10-2025.txt"
WALES = "kb/sources/global/wales-wls-no1-2015-sch1.txt"
TSR = "kb/sources/global/us-tsr-16cfr310.txt"
SPAIN_QUOTES = [
    ("Art 8(2)", "en cualquier momento de la interacción, desde su inicio."),
    ("Art 8(2)", "garantizando que el 95\u202f% de las solicitudes de atención personalizadas sean atendidas, de media, "
                 "en un plazo inferior a tres minutos desde que la clientela efectúe la solicitud."),
    ("Art 8(3)", "que deberá atenderle en el transcurso de esa misma comunicación."),
]
WALES_QUOTES = {
    "Standard 15": "If you have performance indicators for dealing with telephone calls, you must ensure that those "
                   "performance indicators do not treat telephone calls made in Welsh any less favourably than calls "
                   "made in English.",
    "Standard 22": "Any automated telephone systems that you have must provide the complete automated service in Welsh.",
    "Standard 60": "You must ensure that any self service machines that you have function fully in Welsh, and the Welsh "
                   "language must be treated no less favourably than the English language in relation to that machine.",
}
WALES_REG_3_1 = ("The Welsh Ministers authorise the Welsh Language Commissioner to give a compliance notice to the Welsh "
                 "Ministers, to county councils, to county borough councils [F1, to a corporate joint committee] and to "
                 "National Park authorities requiring them to comply with any of the standards specified under "
                 "regulation 2.")  # Task 30b; Task 33 re-held the current text (S.I. 2021/1352 inserted F1)
GAP_5_PORTAL = ("Checked 2026-10-30 on uaelegislation.gov.ae: the related-legislations page of Decree-Law 45/2021 lists "
                "only Decree-Law 30/2024 and Decree-Law 26/2025; no executive regulation and no Cabinet resolution. A "
                "vendor blog's 'Cabinet Decision No. 111/2023' has no instrument on the portal.")


def _examples_in(gap_id: str, file: str) -> list[dict]:
    return [ex for ex in _row(gap_id)["global_examples"] if ex["file"] == file]


def test_gap_1_spain_ley_10_2025_art_8_beside_imda():
    spain = _examples_in("gap-1", SPAIN)
    assert [ex["clause"] for ex in spain] == ["Art 8(2)", "Art 8(2)", "Art 8(3)"]
    for (clause, end), ex in zip(SPAIN_QUOTES, spain):
        assert ex["quote"].endswith(end) and ex["status"] == "VERIFIED", clause
        assert ex["document"].startswith("Spain, Ley 10/2025")
    assert _examples_in("gap-1", "kb/sources/global/imda-agentic-ai-v1.5.txt")  # existing examples stay
    row = _row("gap-1")
    assert row["recommendation"].endswith("the TDRA time can take Spain's shape (a human on request at any moment; "
                                          "95% of requests within three minutes).")
    assert "Art 2(1)(d)" in row["note"] and "Art 2(6)" in row["note"]
    assert "Spain Ley 10/2025 Art 8(2); Spain Ley 10/2025 Art 8(3)" in gaps.table()


def test_gap_10_wales_standards_15_22_60_beside_canada():
    wales = _examples_in("gap-10", WALES)
    assert {ex["clause"]: ex["quote"] for ex in wales} == WALES_QUOTES
    assert all(ex["status"] == "VERIFIED" and ex["document"].startswith("Wales, Welsh Language Standards") for ex in wales)
    assert "reg 3(1)" in _row("gap-10")["note"] and "not operators" in _row("gap-10")["note"]
    assert "Wales WLS Standard 15; Wales WLS Standard 22; Wales WLS Standard 60" in gaps.table()


def test_gap_11_tsr_310_3_a_3_ii_lead_and_items_a_to_h_as_one_quote():
    [tsr] = _examples_in("gap-11", TSR)
    assert tsr["clause"] == "310.3(a)(3)(ii)" and tsr["status"] == "VERIFIED"
    assert tsr["quote"].startswith("Express oral authorization which is audio-recorded")
    assert "receipt of all of the following information: (A) An accurate description" in tsr["quote"]
    assert all(f"({c}) " in tsr["quote"] for c in "ABCDEFGH")
    assert tsr["quote"].endswith("(H) The date of the customer's or donor's oral authorization;")
    assert _examples_in("gap-11", "kb/sources/global/eu-ecommerce-2000-31-art10-11.txt")  # existing stays
    assert "US TSR 16 CFR 310.3(a)(3)(ii)" in gaps.table()


def test_task_30_quotes_are_verbatim_in_their_files():
    if not GLOBAL_DIR.exists():
        pytest.skip("kb/sources/global/ is local only (gitignored, addendum item 15)")
    found = 0
    for gap_id in ("gap-1", "gap-10", "gap-11"):
        for ex in _row(gap_id)["global_examples"]:
            if ex["file"] in (SPAIN, WALES, TSR):
                assert _norm(ex["quote"]) in _norm(kb.read_text(kb.REPO / ex["file"])), (gap_id, ex["clause"])
                found += 1
    assert found == 7
    assert _norm(WALES_REG_3_1) in _norm(kb.read_text(kb.REPO / WALES))  # gap-10 note's reg 3(1), Task 30b


def test_gap_5_records_the_portal_check():
    assert _row("gap-5")["uae_position"].endswith(GAP_5_PORTAL)
    note = kb.manifest_by_id()["pdpl-executive-regulations"]["notes"]
    assert note == ("Not on the official portal as of 2026-10-30 (portal related-legislations checked). Portal checked 2026-11-02, both "
                    "languages: Regulation Table of Decree-Law 45/2021 'No records found'; keyword search 'personal "
                    "data' / 'البيانات الشخصية' (27 / 29 results) lists no executive regulation of this Decree-Law; "
                    "sector list (12 / 14 instruments) has none."), "Task 41 item 1c appends the 2026-11-02 portal check"


# --- order 2026-10-30-task-31-binding-examples ----------------------------------------------------------------

SG = "kb/sources/global/sg-eta-2010-s15.txt"
UTAH = "kb/sources/global/us-utah-13-77-102.txt"
MOFFATT = "kb/sources/global/ca-bccrt-2024-149-moffatt.txt"
ROAMING = "kb/sources/global/eu-roaming-2022-612-art14.txt"
AI_ACT_14 = "kb/sources/global/eu-ai-act-2026-07-27-art14-26.txt"
AI_ACT_CAVEAT = ("High-risk systems only. Chapter III Sections 1 to 3 apply from 2027-12-02 (Annex III) and 2028-08-02 "
                 "(Annex I), Regulation (EU) 2026/1744 Art 1(40)(b).")
TASK_31_QUOTES = {
    (SG, "s. 15"): "A contract formed by the interaction of an automated message system and a natural person, or by the "
                   "interaction of automated message systems, is not to be denied validity or enforceability solely on "
                   "the ground that no natural person reviewed or intervened in each of the individual actions carried "
                   "out by the automated message systems or the resulting contract.",
    (UTAH, "13-77-102"): "It is not a defense to the violation of any statute administered and enforced by the division "
                         "under Section 13-2-102 that generative artificial intelligence: (1) made the violative "
                         "statement; (2) undertook the violative act; or (3) was used in furtherance of the violation.",
    (MOFFATT, "para 27"): "While a chatbot has an interactive component, it is still just a part of Air Canada’s "
                          "website. It should be obvious to Air Canada that it is responsible for all the information on "
                          "its website. It makes no difference whether the information comes from a static page or a "
                          "chatbot.",
    (MOFFATT, "para 28"): "I find Air Canada did not take reasonable care to ensure its chatbot was accurate.",
    (ROAMING, "Art 14(4)"): "If the roaming customer does not respond as prompted in the notification received, the "
                            "roaming provider shall immediately cease to provide and to charge the roaming customer for "
                            "regulated data roaming services, unless and until the roaming customer requests the "
                            "continued or renewed provision of those services.",
    (ROAMING, "Art 14(4), last subparagraph"): "Whenever a roaming customer requests the removal or reinstatement of a "
                                              "financial or volume limit facility, the change shall be made within one "
                                              "working day of receipt of the request",
    (AI_ACT_14, "Art 14(4)(e)"): "to intervene in the operation of the high-risk AI system or interrupt the system "
                                 "through a ‘stop’ button or a similar procedure that allows the system to come "
                                 "to a halt in a safe state.",
}
GAP_2_RECOMMENDATION = ("TDRA to classify an AI agent in each sales medium of Article 4 and say whether 2FA applies; the "
                        "UAE Data Office to say whether a recorded spoken consent meets PDPL 6(1)(b).")
GAP_7_RECOMMENDATION = ("TDRA to set conduct standards for AI agents in consumer care (limits, oversight, logs), as IMDA's "
                        "framework does as a whole; Mizan's gates are one worked form of them.")


def _task_31_examples() -> list[dict]:
    files = {f for f, _ in TASK_31_QUOTES}
    return [ex for gap_id in ("gap-2", "gap-7", "gap-12") for ex in _row(gap_id)["global_examples"] if ex["file"] in files]


def test_task_31_examples_are_the_orders_quotes():
    got = {(ex["file"], ex["clause"]): ex["quote"] for ex in _task_31_examples()}
    assert got == TASK_31_QUOTES
    assert all(ex["status"] == "VERIFIED" for ex in _task_31_examples())


def test_gap_2_adds_singapore_s_15_recommendation_unchanged():
    row = _row("gap-2")
    assert [ex["file"] for ex in row["global_examples"]][-1 - len(TASK_35_EXAMPLES["gap-2"])] == SG  # Task 35 follows
    assert row["note"] == ("Singapore, like UAE Electronic Transactions 46/2021 Art 12(2), validates the automated "
                           "contract; neither names the sales medium. " + DATA_OFFICE)  # Task 33 appends it
    assert row["recommendation"] == GAP_2_RECOMMENDATION
    assert _examples_in("gap-2", "kb/sources/global/eu-crd-2011-83-art8.txt")  # existing examples stay


def test_gap_7_binding_examples_replace_imda_which_stays_in_the_recommendation():
    row = _row("gap-7")
    assert [ex["file"] for ex in row["global_examples"]][:3] == [UTAH, MOFFATT, MOFFATT]  # Task 35b appends
    assert row["recommendation"] == GAP_7_RECOMMENDATION and "IMDA" in row["recommendation"]
    assert row["note"] == ("Utah bars the 'the AI said it' defence; the BC tribunal held Air Canada to its chatbot's "
                           "words (CAD 812.02). The UAE has the general duty (CPR 3.3) and no AI-specific one.")
    assert "Utah Code 13-77-102; Moffatt v. Air Canada 2024 BCCRT 149 para 27" in gaps.table()


def test_gap_12_keeps_sae_and_adds_roaming_and_the_ai_act_with_its_caveat():
    row = _row("gap-12")
    files = [ex["file"] for ex in row["global_examples"]]
    assert files == ["kb/sources/global/itu-t-y3173-2020-02.txt"] * 2 + [ROAMING, ROAMING, AI_ACT_14]
    [ai] = _examples_in("gap-12", AI_ACT_14)
    assert ai["says"] == AI_ACT_CAVEAT
    section = (kb.REPO / "docs" / "gaps.md").read_text(encoding="utf-8").split("## gap-12:", 1)[1]
    assert AI_ACT_CAVEAT in section  # printed beside the quote
    assert "EU Roaming Reg 2022/612 Art 14(4)" in gaps.table() and "EU AI Act Art 14(4)(e)" in gaps.table()


def test_task_31_quotes_are_verbatim_in_their_files():
    if not GLOBAL_DIR.exists():
        pytest.skip("kb/sources/global/ is local only (gitignored, addendum item 15)")
    found = 0
    for ex in _task_31_examples():
        assert _norm(ex["quote"]) in _norm(kb.read_text(kb.REPO / ex["file"])), ex["clause"]
        found += 1
    assert found == 7


# --- Task 31 Part D: the flagged gap explains itself on the replay pages (render only) -------------------------
# Elsewhere: the example marked "elsewhere": true (the report's cell), else the first whose document is binding in
# the manifest, else the first (Iyas, 2026-10-30)

def test_elsewhere_markers_are_the_reports_cells():
    marked = {r["id"]: [(Path(e["file"]).name, e["clause"]) for e in r["global_examples"] if e.get("elsewhere")]
              for r in ROWS}
    assert {k: v for k, v in marked.items() if v} == {
        "gap-1": [("es-ley-10-2025.txt", "Art 8(2)")], "gap-3": [("eidas-910-2014-art8.txt", "Art 8(1)")],
        "gap-10": [("wales-wls-no1-2015-sch1.txt", "Standard 15")]}
    assert gaps.elsewhere("gap-3")["label"] == "eIDAS Art 8(1)"
    assert gaps.elsewhere("gap-10")["label"] == "Wales WLS Standard 15"


def test_elsewhere_is_the_marked_example_else_the_first_binding_else_the_first():
    assert gaps.elsewhere("gap-1")["label"] == "Spain Ley 10/2025 Art 8(2)"  # marked; DSA Art 12(1) is the first binding
    assert gaps.elsewhere("gap-5")["label"] == "GDPR Art 28(3)(a)"
    assert gaps.elsewhere("gap-7")["label"] == "Utah Code 13-77-102"
    assert gaps.elsewhere("gap-12")["label"] == "EU Roaming Reg 2022/612 Art 14(4)"  # SAE via Y.3173 is method
    assert gaps.elsewhere("gap-9")["label"] == "16 CFR 312.5(a)(1)"  # no binding row: the first example
    assert gaps.elsewhere("gap-8")["label"] == "3GPP TS 28.535 §4.2.3"  # Task 33: both method texts, the first
    candidate = _row("candidate-4-4-fixed-term-bundle")
    assert gaps.elsewhere(candidate["id"]) == {"id": candidate["id"], "line": candidate["line"], "label": None,
                                               "quote": None}  # a candidate shows its line only
    assert gaps.elsewhere("gap-99") is None


def test_elsewhere_quotes_are_register_quotes():
    for row in ROWS:
        e = gaps.elsewhere(row["id"])
        if e["quote"]:
            assert e["quote"] in [ex["quote"] for ex in row["global_examples"]]


def test_replay_markdown_explains_each_flagged_gap_under_the_abstention_line():
    s2 = (kb.REPO / "docs" / "replay" / "S2.md").read_text(encoding="utf-8")
    after = s2.split("gap flagged: gap-1, gap-8, gap-12", 1)[1]
    assert f"- gap-1: {_row('gap-1')['line']}" in after
    assert "Elsewhere: Spain Ley 10/2025 Art 8(2)" in after and "../site/gaps.html#gap-1" in after
    assert "Elsewhere: 3GPP TS 28.535 §4.2.3" in after  # gap-8's "none found" until Task 33
    s3 = (kb.REPO / "docs" / "replay" / "S3.md").read_text(encoding="utf-8")
    assert "Elsewhere: GDPR Art 28(3)(a)" in s3.split("gap flagged: gap-5", 1)[1]


def test_replay_viewer_and_site_runs_link_the_flagged_gap_to_the_register():
    viewer = (kb.REPO / "docs" / "replay" / "index.html").read_text(encoding="utf-8")
    runs_page = (kb.REPO / "docs" / "site" / "runs.html").read_text(encoding="utf-8")
    assert "Elsewhere: Spain Ley 10/2025 Art 8(2)" in viewer and "Elsewhere: GDPR Art 28(3)(a)" in viewer
    assert 'href="../site/gaps.html#gap-1"' in viewer and 'href="gaps.html#gap-1"' in runs_page
    assert "Elsewhere: 3GPP TS 28.535 §4.2.3" in viewer  # gap-8's "none found" until Task 33


# --- order 2026-10-30-task-32-operator-codes: searched entries quoted from the stored source, no chunk ----------
# Iyas, 2026-10-30: a searched entry may name its stored file; its quote is checked word for word against that file
# (local only: kb/sources/ is gitignored); gap 9's two 106/2026 entries sit under the English row

DU = "kb/sources/du-code-of-practice-en.pdf"
EAND = "kb/sources/eand-code-of-practice-en.pdf"
R106 = "kb/sources/cabres-106-2026-en.txt"
DU_10 = "CPR 26.13.3 and 26.14.2 restated as 'will try'; no hand-over clause."
CHATBOT = "Chatbot WhatsApp 058-2428268 (058Chatbot)"
GAP_7_SAYS = ("The only UAE texts naming an operator chatbot are the operators' own non-contractual codes; neither sets "
              "a conduct standard.")
IVR_SAYS = ("The operator's own code sells through an automated IVR with immediate binding effect; no OTP, no "
            "read-back, no AI named.")
IVR_QUOTE = ("For customer convenience, subscription to Etisalat plans/services which do not require customers’ ID "
             "verification or supporting documents can be applied through Customer Care Centre, Online (Etisalat’s "
             "web site), and IVR system. In this case the subscription shall be legal and binding to the customer "
             "with immediate effect")
ARABIC_PREVAILS = ("Portal: the Arabic text prevails (cabres-106-2026-ar); Arabic not quote-checked, PDF text "
                   "extraction scrambled.")
TASK_32_SEARCHED = {
    "gap-1": [
        ("du-code-of-practice-en:10", DU, DU_10,
         "We will acknowledge your complaint immediately, in case you submit your complaint by telephone or personal "
         "visit, and within one (1) business days in case you send us your complaint in writing."),
        ("du-code-of-practice-en:10", DU, DU_10,
         "If we cannot resolve your complaint immediately, we will try to resolve it as soon as possible, within 20 "
         "business days of the date of your complaint."),
        ("du-code-of-practice-en:Annex 1", DU,
         "The code names a chatbot as a complaint channel and sets no rule for it.", CHATBOT),
        ("eand-code-of-practice-en:7", EAND, "No deadline, no hand-over, no AI named.",
         "We aim to rectify your problems as soon as possible."),
    ],
    "gap-2": [("eand-code-of-practice-en:4", EAND, IVR_SAYS, IVR_QUOTE)],
    "gap-11": [("eand-code-of-practice-en:4", EAND, IVR_SAYS, IVR_QUOTE)],
    "gap-7": [
        ("du-code-of-practice-en:Annex 1", DU, GAP_7_SAYS, CHATBOT),
        ("eand-code-of-practice-en:1", EAND, GAP_7_SAYS,
         "Nothing in this Code of Practice forms a contract or part of any contract between Etisalat and its customers."),
    ],
    "gap-10": [
        ("du-code-of-practice-en:Annex 1", DU, "Languages for human care; nothing on the chatbot's languages or quality.",
         "contact du Customer Care representatives 24 hours, 7 days a week, to receive general, billing and technical "
         "support in Arabic, English, Hindi, Bengali and Malayalam for du mobile lines and for du home services in "
         "Arabic, English and Hindi."),
    ],
    "gap-9": [
        ("cabres-106-2026-en:2", R106, f"Scope: social media platforms only; a telecom care channel is not one. "
                                       f"{ARABIC_PREVAILS}",
         "This Resolution shall apply to all Social Media Platforms whose services are made available within the "
         "State or directed at users therein."),
        ("cabres-106-2026-en:4(3)", R106, f"Self-declared age is not recognised, on social media platforms (Art 2). "
                                          f"{ARABIC_PREVAILS}",
         "Self-declaration of age, or any other Age Verification mechanism not approved in accordance with the "
         "provisions of this Resolution, shall not be recognized."),
    ],
}


def _filed(gap_id: str) -> list[dict]:
    return [s for s in _row(gap_id)["searched"] if s.get("file") or s.get("url")]  # no chunk (Task 32, 35b)


def _filed_32(gap_id: str) -> list[dict]:
    return _filed(gap_id)[:len(TASK_32_SEARCHED[gap_id])]  # Task 33's entries follow them


def test_task_32_searched_entries_are_the_orders_appended_last():
    for gap_id, expected in TASK_32_SEARCHED.items():
        got = [(s["clause"], s["file"], s["says"], s["quote"]) for s in _filed_32(gap_id)]
        assert got == expected, gap_id
        filed = _filed(gap_id)
        assert _row(gap_id)["searched"][-len(filed):] == filed, gap_id  # appended after the chunked ones
    assert not [r["id"] for r in ROWS + data.load_gaps()["candidates"] if any(s.get("file") for s in r["searched"])
                and r.get("id") not in {**TASK_32_SEARCHED, **TASK_33_SEARCHED, **TASK_35_SEARCHED,
                                        **TASK_35B_SEARCHED, **TASK_41_FILED}]


def test_task_32_files_are_verified_manifest_sources_with_a_page():
    manifest = kb.manifest_by_id()
    for gap_id in TASK_32_SEARCHED:
        for s in (s for s in _filed(gap_id) if s.get("file")):  # a URL-cited text has no row (Task 35b)
            document_id = s["clause"].split(":", 1)[0]
            assert manifest[document_id]["status"] == "VERIFIED"
            assert s["file"] == f"kb/sources/{document_id}{kb._suffix(document_id)}"
            assert int(s["page"]) >= 1 if s["file"].endswith(".pdf") else "page" not in s  # a web page has none


def test_task_32_operator_entries_call_the_code_a_code_never_a_law_or_a_breach():
    for gap_id in TASK_32_SEARCHED:
        for s in _filed(gap_id):
            if "code-of-practice" not in s["clause"]:
                continue
            assert not re.search(r"\b(law|laws|breach\w*|break\w*|violat\w*|non-?complian\w*)\b", s["says"], re.I), s
            assert "rule" not in s["says"].lower() or "sets no rule" in s["says"]  # the code sets none; it is none
    for path in ("docs/gaps.md", "docs/report.md", "README.md"):
        text = (kb.REPO / path).read_text(encoding="utf-8")
        assert not re.search(r"(\be&|\bdu\b|\bEtisalat\b|\bEITC\b)[^.\n]{0,60}\b(breach|break|violat)", text), path


def _stored(path: Path) -> str:
    if path.suffix == ".pdf":
        import pypdf
        return "\n".join(page.extract_text() or "" for page in pypdf.PdfReader(path).pages)
    return kb.read_text(path)


def test_task_32_quotes_are_verbatim_in_the_stored_text():
    files = {kb.REPO / s["file"] for g in TASK_32_SEARCHED for s in _filed_32(g)}
    if not all(f.exists() for f in files):
        pytest.skip("kb/sources/ is local only (gitignored, addendum item 15): run kb fetch --local")
    found = 0
    for gap_id in TASK_32_SEARCHED:
        for s in _filed_32(gap_id):
            text = _stored(kb.REPO / s["file"])
            assert _norm(s["quote"]) in _norm(text), (gap_id, s["clause"])
            found += 1
    assert found == 11


def test_task_32_entries_print_in_the_register_and_on_the_site():
    md = (kb.REPO / "docs" / "gaps.md").read_text(encoding="utf-8")
    html = (kb.REPO / "docs" / "site" / "gaps.html").read_text(encoding="utf-8")
    assert f"- `du-code-of-practice-en:Annex 1` (p. {_filed('gap-1')[2]['page']}, `{DU}`): " in md
    assert "Covers du and Virgin Mobile UAE" not in md  # the manifest note stays in the KB
    assert "<code>eand-code-of-practice-en:4</code>" in html and "<code>kb/sources/eand-code-of-practice-en.pdf</code>" in html


# --- order 2026-10-30-task-33-three-searches Part C ---------------------------------------------------------------

DATA_OFFICE = ("The PDPL names the UAE Data Office (Art 24); its competences move to the Federal Authority for Artificial "
               "Intelligence and Data (announced 2026-06-14, `fed-ai-data-authority-2026-06-14`); the register keeps "
               "the statutory name.")
EO = "kb/sources/executive-order-3-2004.pdf"
R200 = "kb/sources/cabres-200-2025-en.pdf"
R52 = "kb/sources/cabres-52-2024-ar.pdf"
TASK_33_SEARCHED = {  # gap id: [(clause, file, says starts with, quote)], after Task 32's
    "gap-1": [
        ("executive-order-3-2004:32", EO, "The licensee reports complaint numbers and the procedures taken to TDRA on "
         "request; a reporting duty, nothing on the hand-over or its timing.",
         "Upon the Authority's request and within the specified time period indicated therein, the Licensee shall "
         "provide a report in the format set by the Authority showing the number of complaints against them and the "
         "taken procedures in this regard for the period covered in the report."),
        ("cabres-200-2025-en:Schedule row 7", R200, "Where 14/2023 applies, no complaints mechanism is fined (warning, "
         "then AED 2,000 to 20,000 and twenty days' closure); still no stop, hand-over or clock.",
         "Failure to allocate a mechanism for handling complaints."),
    ],
    "gap-2": [
        ("cabres-200-2025-en:Schedule row 1", R200, "Where 14/2023 applies, failing to verify the offer and acceptance "
         "is fined (AED 2,000 up to 100,000 and closure); what verifies a spoken 'yes' through an AI channel is unsaid.",
         "failure to verify the offer and acceptance required for the validity of the contract."),
    ],
    "gap-15": [  # the 79 bis (2) candidate until Task 41
        ("cabres-52-2024-ar:2(2)", R52, "TDRA may double a fine when the same violation is repeated within a year",
         "يجوز للهيئة مضاعفةقيمة الغرامة الإدارية المحددة في الجدول المرفق بهذا القرار في حال تكرار ارتكاب ذات "
         "المخالفة الإدارية قبل مض ي سنة من تاريخ ارتكابها لأول مرة"),
        ("cabres-200-2025-en:3(3)", R200, "The Ministry of Economy may skip the gradation for a serious violation",
         "the Ministry may, in cases of serious violations, impose the more severe administrative penalty without "
         "adhering to the gradation"),
        ("executive-order-3-2004:42", EO, "A fine power for apparatus authorisations, no amount; not the licensee "
         "schedule.",
         "The Authority may perform any of the following in case any of the Authorised or concerned persons in the "
         "Telecommunication Apparatus breaches the terms and restrictions that the Authorisations were granted upon,: "
         "(a) impose a financial fine against the violator ; (b) abolish the issued Authorization."),
    ],
}
GAP_8_NOTE = ("Both are method texts, like Y.3172: 3GPP defines the open control loop, where the system presents and the "
              "human decides; ETSI ZSM defines a flow for a human operator to approve or reject a recommendation. "
              "Neither names a withheld output routed to a named person with its own reference point; the "
              "recommendation stands as the fuller version.")
TASK_33_EXAMPLES = {
    "gap-8": [
        ("kb/sources/global/3gpp-ts-28-535-v19.txt", "§4.2.3",
         "The management system collects, analyses and presents the data to the human operator or other management "
         "entity, but the human operator or other management entity decides which action to take."),
        ("kb/sources/global/etsi-gs-zsm-009-1-v1-1-1.txt", "§7.2.2.4",
         "The customization flow may be used to configure the CL, monitor its continuous operations, approve/reject "
         "recommendations, explain the CL operation and decisions"),
    ],
    "candidate-4-4-fixed-term-bundle": [
        ("kb/sources/global/eu-eecc-2018-1972-art105.txt", "Art 105(3)",
         "Before the contract is automatically prolonged, providers shall inform end-users, in a prominent and timely "
         "manner and on a durable medium, of the end of the contractual commitment and of the means by which to "
         "terminate the contract."),
        ("kb/sources/global/de-tkg-2021-para-56.txt", "§ 56(3)", None),  # a run, "kann der Endnutzer" to "kündigen."
    ],
}


def _filed_33(gap_id: str) -> list[dict]:
    start = len(TASK_32_SEARCHED.get(gap_id, []))
    return _filed(gap_id)[start:start + len(TASK_33_SEARCHED[gap_id])]  # Task 35's entries follow them


def test_task_33_searched_entries_follow_task_32s():
    for gap_id, expected in TASK_33_SEARCHED.items():
        filed = _filed_33(gap_id)
        assert [(s["clause"], s["file"], s["quote"]) for s in filed] == [(c, f, q) for c, f, _, q in expected], gap_id
        for s, (_, _, says, _) in zip(filed, expected):
            assert s["says"].startswith(says), (gap_id, s["clause"])
            assert int(s["page"]) >= 1


def test_task_33_global_examples_replace_the_none_cells():
    for gap_id, expected in TASK_33_EXAMPLES.items():
        row = _row(gap_id)
        assert row["global_none"] == "", gap_id
        assert [(ex["file"], ex["clause"]) for ex in row["global_examples"]] == [(f, c) for f, c, _ in expected]
        for ex, (_, _, quote) in zip(row["global_examples"], expected):
            assert quote is None or ex["quote"] == quote
    tkg = _row("candidate-4-4-fixed-term-bundle")["global_examples"][1]
    assert tkg["quote"].startswith("kann der Endnutzer") and tkg["quote"].endswith("kündigen.")
    assert tkg["says"].startswith("Our English, not an official translation:")  # the gloss is ours
    assert _row("candidate-4-4-fixed-term-bundle")["recommendation"].endswith(
        "falls under 4.4 or needs fresh consent under 4.3, and, if 4.4, require the warning before and the one-month "
        "exit after.")
    assert _row("gap-8")["examples_note"] == GAP_8_NOTE
    assert "3GPP TS 28.535 §4.2.3; ETSI ZSM 009-1 §7.2.2.4" in gaps.table()
    assert "EECC 2018/1972 Art 105(3); TKG 2021 § 56(3)" in gaps.table()


def test_task_33_quotes_are_verbatim_in_the_stored_text():
    entries = [s for g in TASK_33_SEARCHED for s in _filed_33(g)]
    entries += [ex for g in TASK_33_EXAMPLES for ex in _row(g)["global_examples"]]
    if not all((kb.REPO / e["file"]).exists() for e in entries):
        pytest.skip("kb/sources/ is local only (gitignored, addendum item 15): run kb fetch --local")
    for e in entries:
        assert _norm(e["quote"]) in _norm(_stored(kb.REPO / e["file"])), e["file"]
    assert len(entries) == 10


def test_task_33_gap_8_note_prints_after_the_examples_on_the_register_and_the_site():
    section = gaps.render().split("## gap-8:", 1)[1].split("\n## ", 1)[0]
    assert section.index("§7.2.2.4") < section.index(GAP_8_NOTE) < section.index("**Recommendation.**")
    from onyx import site
    html = site._gap(_row("gap-8"))
    assert html.index("7.2.2.4") < html.index(GAP_8_NOTE) < html.index("<h4>Recommendation</h4>")


def test_task_33_arabic_file_quote_is_labelled_ar():
    from onyx import site
    [s] = [s for s in _row("gap-15")["searched"] if s["clause"] == "cabres-52-2024-ar:2(2)"]
    assert gaps._searched(s)[1] == f'  - AR: "{s["quote"]}"'
    assert "<br>AR: " in site._searched(s) and 'dir="rtl"' in site._searched(s)
    [en] = [s for s in _row("gap-1")["searched"] if s["clause"] == "executive-order-3-2004:32"]
    assert gaps._searched(en)[1].startswith("  - EN: ") and "<br>EN: " in site._searched(en)


def test_task_33_executive_order_is_read_not_unpublished():
    [eo] = [c for c in data.load_gaps()["nothing_found"] if c["name"].startswith("The Executive Order")]  # Task 41
    assert eo["name"] == "The Executive Order, read in full"
    assert eo["line"] == ("The Executive Order, read in full (75 articles, English; the Arabic prevails): Art 30 "
                          "directives, Art 32 complaint reporting, Art 42 apparatus fines, Art 47 quality-of-service "
                          "reporting. Nothing on an automated channel, consent, a hand-over or a licensee fine amount.")
    assert [s["clause"] for s in eo["searched"]] == ["licence-2-2026:16.2"]  # the licence cite stays
    for path in ("docs/gaps.md", "kb/DATASHEET.md", "docs/report.md", "README.md"):
        text = (kb.REPO / path).read_text(encoding="utf-8")
        assert not re.search(r"Executive Order[^.\n]{0,80}unpublished|unpublished[^.\n]{0,40}Executive Order", text), path


def test_task_33_data_office_sentence_once_in_the_register():
    assert gaps.render().count(DATA_OFFICE) == 1
    assert _row("gap-2")["addressee"] == ["TDRA", "UAE Data Office"]  # addressee fields unchanged


# --- order 2026-10-30-task-35-gulf-rows, base and Addendum A: Gulf examples and searched entries ------------------
# The English quotes are checked against kb/sources/global/ (local only) and the Arabic from the CST page images
# against hq's read file; nothing here was transcribed by the build (Addendum A, limits).

GULF_LINE = ("The three GCC telecom consumer regulations read (Saudi 2024, Qatar 2024, Kuwait 2022) name no AI channel, "
             "hand-over clock, machine disclosure or Arabic quality measure either; Saudi 552/1445 comes nearest, "
             "requiring a route to an employee and a qualified employee on every complaint.")
QA_PDF, QA_TXT = "kb/sources/qatar-cra-ccpr-2024.pdf", "kb/sources/global/qatar-cra-ccpr-2024.txt"
KW_AR = "kb/sources/kuwait-citra-users-rights-ar.pdf"
SA_EN = "kb/sources/saudi-cst-user-protection-552-1445-en.pdf"
SA_TXT = "kb/sources/global/saudi-cst-user-protection-552-1445-en.txt"
SA_AR = "kb/sources/saudi-cst-user-protection-552-1445-ar.pdf"
Q16, Q16_TXT = "kb/sources/qatar-decree-law-16-2010-ar.md", "kb/sources/global/qatar-decree-law-16-2010-ar.txt"
SAUDI_READ = Path("D:/Projects/hq/uni/ai-for-good-hackathon/perplexity-2026-10-30/saudi-cst-552-read-2026-10-30-fable.md")
TASK_35_EXAMPLES = {  # gap id: [(file, clause, page)], appended after the existing examples
    "gap-1": [(SA_TXT, "§13.1.1", 14), (SA_TXT, "§13.1.2", 14), (SA_TXT, "§26.5.2", 29)],
    "gap-2": [(SA_TXT, "§5.1.2", 8), (SA_TXT, "§5.1.3", 8)],
    "gap-3": [(QA_TXT, "§1.2 (Customer Consent)", 6), (SA_TXT, "§10.7", 13)],
    "gap-11": [(Q16_TXT, "Art 56(1)", None), (Q16_TXT, "Art 19", None)],
}
TASK_35_SEARCHED = {  # gap id: [(clause, file, page)], appended after every earlier entry
    "gap-1": [("kuwait-citra-users-rights-ar:9 (2.9, 4.9, 5.9)", KW_AR, 12),
              ("saudi-cst-user-protection-552-1445-en:26.4", SA_EN, 28),
              ("saudi-cst-user-protection-552-1445-en:13.1.3", SA_EN, 15)],
    "gap-2": [("qatar-cra-ccpr-2024:1.2", QA_PDF, 6), ("kuwait-citra-users-rights-ar:3-1", KW_AR, 6),
              ("saudi-cst-user-protection-552-1445-en:9.5", SA_EN, 12)],
    "gap-3": [("saudi-cst-user-protection-552-1445-en:9.6", SA_EN, 12),
              ("saudi-cst-user-protection-552-1445-en:23.1", SA_EN, 23)],
    "gap-6": [("saudi-cst-user-protection-552-1445-ar:5.1.4", SA_AR, 8), ("qatar-decree-law-16-2010-ar:53(2)", Q16, None),
              ("qatar-decree-law-16-2010-ar:27", Q16, None)],
    "gap-10": [("saudi-cst-user-protection-552-1445-en:9.2.2", SA_EN, 11),
               ("saudi-cst-user-protection-552-1445-en:16.4", SA_EN, 17),
               ("saudi-cst-user-protection-552-1445-en:26.6", SA_EN, 29)],
    "gap-11": [("saudi-cst-user-protection-552-1445-en:10.3", SA_EN, 12),
               ("saudi-cst-user-protection-552-1445-en:10.4", SA_EN, 12),
               ("saudi-cst-user-protection-552-1445-en:23.6", SA_EN, 24)],
    "gap-12": [("saudi-cst-user-protection-552-1445-en:30.2", SA_EN, 32), ("qatar-decree-law-16-2010-ar:1", Q16, None),
               ("qatar-decree-law-16-2010-ar:27", Q16, None)],
}


def _task_35_examples(gap_id: str) -> list[dict]:
    later = len(TASK_35B_APPENDED.get(gap_id, []))  # Task 35b's entries follow Task 35's
    rows = _row(gap_id)["global_examples"]
    return rows[len(rows) - later - len(TASK_35_EXAMPLES[gap_id]):len(rows) - later]


def _task_35_searched(gap_id: str) -> list[dict]:
    later = len(TASK_35B_SEARCHED.get(gap_id, []))  # Task 35b's entries follow Task 35's
    rows = _row(gap_id)["searched"]
    return rows[len(rows) - later - len(TASK_35_SEARCHED[gap_id]):len(rows) - later]


def test_task_35_examples_are_appended_and_the_leads_stay():
    for gap_id, expected in TASK_35_EXAMPLES.items():
        got = _task_35_examples(gap_id)
        assert [(ex["file"], ex["clause"], ex.get("page")) for ex in got] == expected, gap_id
        assert all(ex["status"] == "VERIFIED" and not ex.get("elsewhere") for ex in got), gap_id
        assert got[0]["says"], gap_id  # what the example says, on its first quote
    assert gaps.elsewhere("gap-1")["label"] == "Spain Ley 10/2025 Art 8(2)"  # Spain stays lead
    assert gaps.elsewhere("gap-3")["label"] == "eIDAS Art 8(1)"  # eIDAS stays lead
    qatar = _task_35_examples("gap-3")[0]
    assert qatar["says"] == "Named verification routes for a remote consent, no assurance level."
    assert qatar["quote"].startswith("b. collected through the Number of the Customer")
    assert qatar["quote"].endswith("capturing genuine consent.")
    assert " c. via the Service Provider’s call center" in qatar["quote"] and " d. via digital means" in qatar["quote"]
    for ex in _task_35_examples("gap-1"):  # English as printed, the Arabic beside it from the page image
        assert ex["file_ar"] == SA_AR and ex["page_ar"] in (14, 28) and kb._is_arabic(ex["quote_ar"])
    table = gaps.table()
    for label in ("Saudi CST 552/1445 §13.1.1", "Saudi CST 552/1445 §26.5.2", "Saudi CST 552/1445 §5.1.2",
                  "Qatar CCPR 2024 §1.2 (Customer Consent)", "Saudi CST 552/1445 §10.7", "Qatar 16/2010 Art 56(1)",
                  "Qatar 16/2010 Art 19"):
        assert label in table, label


def test_task_35_searched_entries_are_appended_last():
    for gap_id, expected in TASK_35_SEARCHED.items():
        got = _task_35_searched(gap_id)
        assert [(s["clause"], s["file"], s.get("page")) for s in got] == expected, gap_id
        assert all(s["says"] and s["quote"] for s in got), gap_id
    [kw_9] = [s for s in _task_35_searched("gap-1") if s["clause"].startswith("kuwait")]
    assert kw_9["quote"] == "وان لا يزيد معدل انتظار المشتركين على الخط اكثر من 3 دقيقة"
    assert kw_9["says"] == ("A 3-minute average wait on the complaints line and a dedicated department; no "
                            "bot-to-human hand-over rule.")
    [kw_3] = [s for s in _task_35_searched("gap-2") if s["clause"].startswith("kuwait")]
    assert kw_3["quote"] == "ويجوز ان تكون الموافقة خطية على عقد الاشتراك او شفهية او رسالة الكترونية"
    assert kw_3["says"] == "Spoken consent allowed; the AI channel unnamed."
    assert all(kb._is_arabic(s["quote"]) for s in _task_35_searched("gap-6"))  # Arabic quotes, AR label


def test_task_35_quotes_are_verbatim_in_the_stored_text():
    squash = lambda t: re.sub(r"\s+", "", t)  # pypdf splits words ("succe ssful"); compare without whitespace
    files = {kb.REPO / f for f in (QA_PDF, QA_TXT, KW_AR, SA_TXT, Q16, Q16_TXT)}
    if not all(f.exists() for f in files) or not SAUDI_READ.exists():
        pytest.skip("kb/sources/ is local only (gitignored, addendum item 15): run kb fetch --local")
    stored = {f: squash(_stored(f)) for f in files}
    read = squash(SAUDI_READ.read_text(encoding="utf-8"))
    checked = 0
    for gap_id in TASK_35_SEARCHED:
        for s in _task_35_searched(gap_id):
            if s["file"] == SA_AR:  # the image-only Arabic: the read file's table
                assert squash(s["quote"]) in read, s["clause"]
            else:
                assert squash(s["quote"]) in stored[kb.REPO / (SA_TXT if s["file"] == SA_EN else s["file"])], \
                    (gap_id, s["clause"])
            checked += 1
    for gap_id in TASK_35_EXAMPLES:
        for ex in _task_35_examples(gap_id):
            assert squash(ex["quote"]) in stored[kb.REPO / ex["file"]], (gap_id, ex["clause"])
            if ex.get("quote_ar"):
                assert squash(ex["quote_ar"]) in read, ex["clause"]
            if ex.get("page"):  # the PDF page the quote sits on
                text = re.sub(r"\s+", " ", kb.read_text(kb.REPO / ex["file"]))
                before = text[:text.index(re.sub(r"\s+", " ", ex["quote"]))]
                assert re.findall(r"=== PAGE (\d+) ===", before)[-1] == str(ex["page"]), ex["clause"]
            checked += 1
    assert checked == 20 + 9


def test_task_35_entries_render_on_the_register_and_the_site_arabic_rtl():
    from html import escape

    from onyx import site
    md, html = gaps.render(), site.gaps_page()
    assert md.count(GULF_LINE) == 1 and html.count(GULF_LINE) == 1
    assert (kb.REPO / "README.md").read_text(encoding="utf-8").count(GULF_LINE) == 1
    saudi = _task_35_examples("gap-1")[0]
    assert f"- {saudi['document']}, §13.1.1 (VERIFIED, p. 14, `{SA_TXT}`): {saudi['says']} \"{saudi['quote']}\"" in md
    assert f"  - AR (p. 14, `{SA_AR}`): \"{saudi['quote_ar']}\"" in md
    q56 = _task_35_examples("gap-11")[0]
    assert f"(VERIFIED, `{Q16_TXT}`): {q56['says']} AR: \"{q56['quote']}\"" in md
    assert f"AR (p. 14, <code>{SA_AR}</code>): " in site._gap(_row("gap-1"))
    for row_id in ("gap-1", "gap-2", "gap-6", "gap-11", "gap-12"):
        page = site._gap(_row(row_id))
        entries = _row(row_id)["global_examples"] + _row(row_id)["searched"]
        arabic = [q for e in entries for q in (e.get("quote_ar"), e.get("quote")) if q and kb._is_arabic(q)]
        assert arabic, row_id
        for q in arabic:
            assert f'lang="ar" dir="rtl">{escape(q)}</q>' in page, (row_id, q[:30])
    for gap_id in TASK_35_SEARCHED:
        for s in _task_35_searched(gap_id):
            assert f"- `{s['clause']}` (" in md and f"<code>{escape(s['clause'])}</code>" in html, s["clause"]
    assert (kb.REPO / "docs" / "gaps.md").read_text(encoding="utf-8") == md
    assert (kb.REPO / "docs" / "site" / "gaps.html").read_text(encoding="utf-8") == html


# --- order 2026-10-30-task-35b-bot-disclosure (Addendum B): bot-disclosure statutes on gaps 1, 6 and 7 ----------
# Quotes come from hq's read file's table or, where the stored source has a text layer, verbatim from it; nothing
# retyped (Addendum B). The California extracts carry the read file's quotes only (tests/test_kb.py).

BOT_READ = Path("D:/Projects/hq/uni/ai-for-good-hackathon/perplexity-2026-10-30/"
                "bot-disclosure-statutes-read-2026-10-30-fable.md")
KOREA_HTML = Path("D:/Projects/hq/uni/ai-for-good-hackathon/standards-text/bot-disclosure-2026-10-30/"
                  "korea-ai-basic-act-klri-en.html")
MAINE = "kb/sources/global/maine-1500-dd.txt"
INDIA = "kb/sources/global/india-trai-tccrr-2012.txt"
CA_BPC = "kb/sources/global/california-bpc-17940-17943.txt"
CA_HSC = "kb/sources/global/california-hsc-1339-75.txt"
AI_ACT_50 = "kb/sources/global/eu-ai-act-art50-art113-20260727.txt"
TX = "kb/sources/texas-bcc-552.html"
HSC_SOURCE = "kb/sources/california-hsc-1339-75.txt"
KLRI = "https://elaw.klri.re.kr/eng_service/lawView.do?hseq=73499&lang=ENG"
TRAI_DRAFT = "https://trai.gov.in/sites/default/files/2026-05/Regulation_07052026.pdf"
COMPANION_LINE = "The 2025 to 2026 US statutes on chatbots regulate companions and carve out customer service."
INDIA_3_9 = [(INDIA, "reg 3(9)", 4), (INDIA, "reg 3(9), proviso", 5)]
TASK_35B_LEAD = [(MAINE, "§1500-DD(2)", None), (CA_BPC, "§17941(a)", None), (CA_BPC, "§17941(b)", None)]  # gap-6
TASK_35B_APPENDED = {  # gap id: [(file, clause, page)], after every earlier example
    "gap-1": INDIA_3_9,
    "gap-7": INDIA_3_9 + [(CA_HSC, "§1339.75(a)(1)(C)", None), (CA_HSC, "§1339.75(a)(2)", None)],
}
TASK_35B_SEARCHED = {  # gap id: [(clause, file, url)], after every earlier entry
    "gap-1": [("california-hsc-1339-75:1339.75(a)(2)", HSC_SOURCE, None)],
    "gap-6": [("texas-bcc-552:552.051(b)", TX, None), ("texas-bcc-552:552.051(c)", TX, None),
              ("kr-ai-framework-act-20676:31(1)", None, KLRI)],
    "gap-7": [("trai-tccrr-fourth-amendment-2026-draft:3(11)", None, TRAI_DRAFT)],
}


def _35b_appended(gap_id: str) -> list[dict]:
    return _row(gap_id)["global_examples"][-len(TASK_35B_APPENDED[gap_id]):]


def _35b_searched(gap_id: str) -> list[dict]:
    return _row(gap_id)["searched"][-len(TASK_35B_SEARCHED[gap_id]):]


def test_task_35b_gap_6_maine_leads_california_second_the_ai_act_third():
    files = [(ex["file"], ex["clause"], ex.get("page")) for ex in _row("gap-6")["global_examples"]]
    assert files[:3] == TASK_35B_LEAD
    assert [f for f, _, _ in files[3:]] == [AI_ACT_50] * 3  # Art 50(1), 50(5), 113 unchanged, now third
    maine, bpc_a, _ = _row("gap-6")["global_examples"][:3]
    assert maine["says"].startswith("Plainest binding text: trade and commerce, text or voice, disclose or it is an "
                                    "unfair practice")
    assert "In-force date not on the statute page." in maine["says"]
    assert "a duty only when the bot is used to deceive; disclosure is the defence" in bpc_a["says"]  # intent caveat
    table = gaps.table()
    assert "Maine §1500-DD(2); California BPC §17941(a); California BPC §17941(b); EU AI Act Art 50(1)" in table
    # the report's cell (Addendum B item 3, 5 pages held) and the replay pages' example: Maine, the first binding one
    report = (kb.REPO / "docs" / "report.md").read_text(encoding="utf-8")
    assert "| Cabinet | Maine §1500-DD; EU AI Act Art 50(1) |" in report
    assert gaps.elsewhere("gap-6")["label"] == "Maine §1500-DD(2)" and not any(
        ex.get("elsewhere") for ex in _row("gap-6")["global_examples"])


def test_task_35b_gap_7_and_gap_1_examples_are_appended():
    for gap_id, expected in TASK_35B_APPENDED.items():
        got = _35b_appended(gap_id)
        assert [(ex["file"], ex["clause"], ex.get("page")) for ex in got] == expected, gap_id
        assert all(ex["status"] == "VERIFIED" and not ex.get("elsewhere") for ex in got), gap_id
        assert got[0]["says"], gap_id
    assert _35b_appended("gap-1")[0]["says"] == ("A regulator orders the automated channel to offer a person; "
                                                 "no clock.")
    assert gaps.elsewhere("gap-1")["label"] == "Spain Ley 10/2025 Art 8(2)"  # Spain stays lead
    assert gaps.elsewhere("gap-7")["label"] == "Utah Code 13-77-102"  # Utah stays first
    assert "India TRAI TCCRR 2012 reg 3(9)" in gaps.table() and "California HSC §1339.75(a)(2)" in gaps.table()


def test_task_35b_searched_entries_are_appended_last():
    for gap_id, expected in TASK_35B_SEARCHED.items():
        got = _35b_searched(gap_id)
        assert [(s["clause"], s.get("file"), s.get("url")) for s in got] == expected, gap_id
        assert all(s["says"] and s["quote"] for s in got), gap_id
    [korea] = [s for s in _35b_searched("gap-6") if s.get("url")]
    assert "English is a reference translation; in-force date unverified." in korea["says"]
    [draft] = _35b_searched("gap-7")
    assert draft["says"].startswith("Draft, not law") and "draft" in draft["clause"]
    assert "Brazil" not in json.dumps(data.load_gaps(), ensure_ascii=False)  # dropped by Iyas 2026-10-30


def test_task_35b_quotes_are_verbatim_in_the_stored_text():
    files = [kb.REPO / f for f in (MAINE, INDIA, CA_BPC, CA_HSC, HSC_SOURCE)]
    if not all(f.exists() for f in files) or not BOT_READ.exists() or not KOREA_HTML.exists():
        pytest.skip("kb/sources/ is local only (gitignored, addendum item 15): run kb fetch --local")
    read = _norm(BOT_READ.read_text(encoding="utf-8"))
    korea = _norm(re.sub(r"<[^>]+>", " ", KOREA_HTML.read_text(encoding="utf-8")))
    checked = 0
    for ex in _row("gap-6")["global_examples"][:3] + [e for g in TASK_35B_APPENDED for e in _35b_appended(g)]:
        text = _norm(kb.read_text(kb.REPO / ex["file"]))
        assert _norm(ex["quote"]) in text, ex["clause"]
        if ex.get("page"):  # the PDF page the quote sits on
            before = text[:text.index(_norm(ex["quote"]))]
            assert re.findall(r"=== PAGE (\d+) ===", before)[-1] == str(ex["page"]), ex["clause"]
        checked += 1
    for gap_id in TASK_35B_SEARCHED:
        for s in _35b_searched(gap_id):
            if s.get("file") == TX:  # the stored page is a script shell: the read file's table
                assert _norm(s["quote"]) in read, s["clause"]
            elif s.get("url") == KLRI:  # checked against the stored KLRI page, not the URL bytes (Addendum B)
                assert _norm(s["quote"]) in korea, s["clause"]
            elif s.get("url") == TRAI_DRAFT:  # no row: the build checked it against the fetched draft
                continue
            else:
                assert _norm(s["quote"]) in _norm(kb.read_text(kb.REPO / s["file"])), s["clause"]
            checked += 1
    assert checked == 3 + 2 + 4 + 4


def test_task_35b_entries_render_on_the_register_and_the_site():
    from html import escape

    from onyx import site
    md, html = gaps.render(), site.gaps_page()
    assert md.count(COMPANION_LINE) == 1 and html.count(COMPANION_LINE) == 1
    for gap_id in TASK_35B_SEARCHED:
        for s in _35b_searched(gap_id):
            assert f"- `{s['clause']}` (" in md and f"<code>{escape(s['clause'])}</code>" in html, s["clause"]
            if s.get("url"):
                assert f"{s['url']}): {s['says']}" in md, s["clause"]
                assert f'<a href="{escape(s["url"])}">{escape(s["url"])}</a>' in html, s["clause"]
    for gap_id in ("gap-1", "gap-6", "gap-7"):
        page = site._gap(_row(gap_id))
        for ex in _row(gap_id)["global_examples"]:
            assert escape(ex["quote"]) in page, (gap_id, ex["clause"])
    assert (kb.REPO / "docs" / "gaps.md").read_text(encoding="utf-8") == md
    assert (kb.REPO / "docs" / "site" / "gaps.html").read_text(encoding="utf-8") == html


# --- order 2026-11-02 Task 41, Annex F: gaps 13 to 15 ---------------------------------------------------------------

PDPL_AR = "kb/sources/pdpl-45-2021-ar.pdf"
TASK_41_FILED = {"gap-13": [("pdpl-45-2021-en:28", "kb/sources/pdpl-45-2021-en.pdf", 28),
                            ("pdpl-45-2021-ar:28", PDPL_AR, 20)]}
TASK_41_SEARCHED = {"gap-13": ["pdpl-45-2021-en:9(1)", "pdpl-45-2021-en:9(2)", "pdpl-45-2021-en:28", "pdpl-45-2021-ar:28"],
                    "gap-14": ["pdpl-45-2021-en:7(5)", "pdpl-45-2021-en:8(1)", "pdpl-45-2021-en:8(10)",
                               "pdpl-45-2021-en:8(11)"]}


def _manifest_ids(path: str) -> list[str]:
    """The manifest rows a global example's file extracts: by document id, else by the local-sources file, else by
    instrument (gaps.INSTRUMENT)."""
    manifest, stem, name = kb.manifest_by_id(), Path(path).stem, Path(path).name
    if stem in manifest:
        return [stem]
    local = [d for d, s in kb.LOCAL.items() if any((s.get(k) or "").endswith("/" + name) for k in ("file", "text"))]
    if local:
        return local
    instrument = next((i for prefix, i in gaps.INSTRUMENT.items() if stem.startswith(prefix)), None)
    return [r["document_id"] for r in kb.load_manifest() if r["instrument"] == instrument]


def test_every_global_example_points_at_a_verified_manifest_row():
    manifest = kb.manifest_by_id()
    for row in ROWS:
        for ex in row["global_examples"]:
            ids = _manifest_ids(ex["file"])
            assert any(manifest[i]["status"] == "VERIFIED" and manifest[i]["sha256"] for i in ids), (row["id"], ex["file"])


def test_task_41_rows_are_the_orders():
    g13, g14, g15 = _row("gap-13"), _row("gap-14"), _row("gap-15")
    assert (g13["line"], g13["kind"], g13["category"], g13["exposed_by"]) == (
        "breach notice has no period", "absence", "legislative gap", "mapping (P)")
    assert g13["addressee"] == ["Council of Ministers", "UAE Data Office (proposer, Art 28)"]
    assert g13["note"] == "Promoted from candidate 2026-11-02 (hq read, Perplexity Q1)."
    assert [(e["clause"], e["quote"]) for e in g13["global_examples"]] == [
        ("Art 33(1)", "without undue delay and, where feasible, not later than 72 hours after having become aware of it")]
    assert (g14["line"], g14["exposed_by"]) == ("a processor may bring in another without the controller's say", "S3-4")
    assert g14["addressee"] == ["Council of Ministers (Executive Regulations, 8(11), 28)", "UAE Data Office (proposer)"]
    assert [e["clause"] for e in g14["global_examples"]] == ["Art 28(2)"]
    assert g15["line"] == "the Cabinet schedule of licensee fines under Telecom Law 79 bis (2) is unpublished"
    assert "Cabinet Resolution 206/2025" in g15["gap"] and g15["note"].startswith("A published method, not a tariff.")
    for gap_id, clauses in TASK_41_SEARCHED.items():
        assert [s["clause"] for s in _row(gap_id)["searched"]] == clauses, gap_id
    for row in (g13, g14, g15):  # phrase absence as the portal's, never as a fact about the world (order limits)
        text = " ".join(str(row[k]) for k in ("gap", "uae_position", "recommendation", "note") if row.get(k))
        assert not re.search(r"never issued|never-issued|does not exist", text), row["id"]


def test_no_live_output_says_never_issued():
    """Task 42: absence is the portal's on the day checked, never 'never issued'. The frozen answer keys keep their
    committed bytes (hq, 2026-11-02, answer 1a), so onyx/data/keys/ is left out."""
    root = kb.REPO
    paths = [p for p in (root / "onyx" / "data").rglob("*") if p.is_file() and "keys" not in p.relative_to(root).parts]
    paths += [p for p in (root / "docs" / "site").rglob("*") if p.is_file() and p.suffix in {".html", ".css", ".js", ".json", ".md", ".txt"}]
    paths += [root / f for f in ("docs/gaps.md", "kb/manifest.csv", "kb/DATASHEET.md", "README.md", "docs/report.md",
                                 "docs/annex.md")]
    hits = [str(p.relative_to(root)) for p in paths
            if re.search(r"never issued|never-issued|not issued", p.read_text(encoding="utf-8", errors="ignore"), re.I)]
    assert not hits, hits


def test_task_41_s3_step_4_is_the_processor_contract_step():
    step = next(s for s in data.load_key("S3")["steps"] if s["n"] == 4)
    assert {"pdpl-8-1", "pdpl-7-5"} <= set(step["must_cite"])


def test_task_41_pdpl_quotes_are_verbatim_in_the_held_texts_on_their_pages():
    files = [kb.REPO / PDPL_AR, kb.REPO / "kb/sources/pdpl-45-2021-en.pdf"]
    if not all(f.exists() for f in files):
        pytest.skip("kb/sources/ is local only (gitignored, addendum item 15): run kb fetch --local")
    import pypdf
    squash = lambda t: re.sub(r"\s+", "", t)  # pypdf breaks lines mid-sentence; compare without whitespace
    pages = {f: [squash(p.extract_text() or "") for p in pypdf.PdfReader(f).pages] for f in files}
    checked = 0
    for gap_id in TASK_41_SEARCHED:
        for s in _row(gap_id)["searched"]:
            if s.get("quote_ar"):
                assert s["file_ar"] == PDPL_AR
                assert squash(s["quote_ar"]) in pages[kb.REPO / PDPL_AR][s["page_ar"] - 1], s["clause"]
                checked += 1
            if s.get("file"):
                assert squash(s["quote"]) in pages[kb.REPO / s["file"]][s["page"] - 1], s["clause"]
                checked += 1
    assert checked == 6 + 2


def test_task_41_filed_entries_are_verified_manifest_sources():
    manifest = kb.manifest_by_id()
    for gap_id, filed in TASK_41_FILED.items():
        got = [(s["clause"], s["file"], s["page"]) for s in _filed(gap_id)]
        assert got == filed, gap_id
        for clause, file, _ in filed:
            document_id = clause.split(":", 1)[0]
            assert manifest[document_id]["status"] == "VERIFIED" and file == f"kb/sources/{document_id}{kb._suffix(document_id)}"


def test_task_41_register_and_site_show_the_new_sections():
    md = (kb.REPO / "docs" / "gaps.md").read_text(encoding="utf-8")
    html = (kb.REPO / "docs" / "site" / "gaps.html").read_text(encoding="utf-8")
    for heading in ("## gap-13: breach notice has no period", "## gap-15: the Cabinet schedule",
                    "### Arabic records", "## Searched, nothing found", "### The Executive Order, read in full"):
        assert heading in md, heading
    assert md.index("## Candidates") < md.index("### Arabic records") < md.index("## Searched, nothing found") \
        < md.index("### The Executive Order, read in full")
    assert "### Breach notification without a period" not in md and "### Sub-processor authorisation" not in md
    assert "<h2>Searched, nothing found</h2>" in html and 'id="gap-14"' in html
    assert '  - AR (p. 10, `kb/sources/pdpl-45-2021-ar.pdf`): "' in md  # the Arabic PDF's page, 9(2)
    assert gaps.ids() == ([f"gap-{n}" for n in range(1, 16)],
                          ["candidate-4-4-fixed-term-bundle", "candidate-arabic-records"]), "Task 41: 15 gaps, 2 candidates"
