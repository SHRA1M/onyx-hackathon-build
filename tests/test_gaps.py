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
ORDER_IDS = [f"gap-{n}" for n in range(1, 9)] + ["candidate-4-4-fixed-term-bundle"]
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
    assert headings[:2] == ["Gap register", "Two-minute check"]  # order 2026-10-21-task-9-fixes-tasks-10-11 item 6
    assert table.count("\n| ") == len(ROWS) + 1  # the separator row plus one row per gap


# --- order 2026-10-21-task-9-fixes-tasks-10-11, Part A ------------------------------------------------------------

GAP_7 = ("No binding UAE text sets conduct standards for an AI agent dealing with a consumer. The clauses that name AI "
         "or an automated agent set a charge waiver (CPR 25.14.1), a bar (26.7.2), a definition (Spam Calls v4 "
         "3.3(iii)), a permission (Cabinet 56/2024 5(6)) and a tool (Child Digital Safety 10(1)(g)); PDPL 18 and "
         "Electronic Transactions 11 to 13 govern automated decisions and contracts as outcomes, not the agent's "
         "conduct.")


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
