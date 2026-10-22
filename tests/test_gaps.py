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
    assert headings[:2] == ["Gap register", "Model"]
    assert table.count("\n| ") == len(ROWS) + 1  # the separator row plus one row per gap
