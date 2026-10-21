import json
import re
import warnings
from pathlib import Path

import jsonschema
import pytest

from onyx import data, kb

HQ_DIR = Path("D:/Projects/hq/uni/ai-for-good-hackathon")


def test_manifest_validates():
    schema = json.loads((kb.KB_DIR / "manifest.schema.json").read_text(encoding="utf-8"))
    rows = kb.load_manifest()
    assert rows, "manifest is empty"
    ids = [r["document_id"] for r in rows]
    assert len(ids) == len(set(ids)), "duplicate document_id"
    for row in rows:
        jsonschema.validate(row, schema)
    for row in kb.verified_rows(rows):
        path = kb.source_path(row)
        if path is None:
            # Addendum item 15: a blocked host leaves only the committed cited clauses; say so.
            warnings.warn(f"{row['document_id']}: source not fetched; runs on the committed cited clauses")
            continue
        assert kb.sha256_file(path) == row["sha256"], f"{row['document_id']}: sha256 differs from the file on disk"


def test_chunk_cpr_26_7_2_both_languages():
    chunk = kb.get_chunk("tdra-cpr-v2-en", "26.7.2")
    assert "preclude the use of non-human agents" in chunk["text_en"]
    assert "يستثنى أو يستبعد منها" in chunk["text_ar"]
    assert chunk["status"] == "VERIFIED"
    assert chunk["article"] == "26"


def test_committed_chunks_are_the_cited_clauses_only():
    # Addendum item 15 (Iyas, 2026-10-20): the repo holds the clauses rules and mandates cite, nothing more.
    committed = {(c["document_id"], c["clause"]) for c in kb.iter_chunks()}
    assert committed == data.cited_chunks()


def test_extract_chunks_match_the_extract():
    # Decision 16/2026 is Arabic only with a garbled text layer: its clauses come from the labelled extract,
    # which is the hq file Iyas checked by eye against the PDF page, not the 2026-10-17 note.
    extract = kb.read_extract("decision-16-2026-ar")
    assert extract["checked"].startswith("decision-16-2026-ar-4.17-4.18-checked.txt")
    assert {"4.17", "4.18"} <= extract["clauses"].keys()
    assert extract["clauses"]["4.18"].endswith("ويتعين على المرخص له الآخر تنفيذ الحجب خلال ساعتين من وقت استلام الإخطار.")
    for chunk in kb.iter_chunks("decision-16-2026-ar"):
        assert chunk["text_ar"] == extract["clauses"][chunk["clause"]]
        assert chunk["text_en"] == "" and chunk["page"] == 10


@pytest.mark.parametrize("extract, checked", [
    ("decision-16-2026-ar.txt", "decision-16-2026-ar-4.17-4.18-checked.txt"),
    ("licence-2-2026-ar.txt", "licence-2-2026-ar-9.1-checked.txt"),
])
def test_extract_body_is_the_hq_checked_file(extract, checked):
    if not (HQ_DIR / checked).exists():
        pytest.skip("hq folder not on this machine")
    # hq writes the bare words where the clause is known from the file name; compare without clause numbers.
    body = lambda path: [re.sub(r"^\d+(\.\d+)+\s", "", l) for l in path.read_text(encoding="utf-8").splitlines()
                         if l.strip() and not l.startswith("#")]
    assert body(kb.EXTRACTS_DIR / extract) == body(HQ_DIR / checked)


def test_a_paired_extract_fills_the_arabic_of_its_document():
    # The licence is chunked from its text layer; the checked Arabic of 9.1 comes from kb/extracts/.
    extract = kb.find_extract("licence-2-2026")
    assert extract["pair_of"] == "licence-2-2026"
    assert extract["checked"].startswith("licence-2-2026-ar-9.1-checked.txt")
    assert kb.get_chunk("licence-2-2026", "9.1")["text_ar"] == extract["clauses"]["9.1"]


def test_extract_continuation_lines_join_the_clause(tmp_path, monkeypatch):
    (tmp_path / "doc.txt").write_text("# page: 1\n4.1 first line:\n- item one,\n- item two.\n4.2 next\n", encoding="utf-8")
    monkeypatch.setattr(kb, "EXTRACTS_DIR", tmp_path)
    assert kb.read_extract("doc")["clauses"] == {"4.1": "first line: - item one, - item two.", "4.2": "next"}


def test_fetch_prints_the_url_of_a_blocked_row(tmp_path, monkeypatch, capsys):
    # Iyas, 2026-10-20: where the portal blocks, print the row's URL so a judge can download it by hand.
    manifest = tmp_path / "manifest.csv"
    manifest.write_bytes(kb.MANIFEST.read_bytes())
    monkeypatch.setattr(kb, "MANIFEST", manifest)
    monkeypatch.setattr(kb, "SOURCES_DIR", tmp_path / "sources")
    monkeypatch.setattr(kb, "_download", lambda url: ("403", None))
    monkeypatch.delenv(kb.SOURCE_DIR_ENV, raising=False)
    kb._cli(type("Args", (), {"action": "fetch", "local": None})())
    out = capsys.readouterr().out
    row = kb.manifest_by_id()["cabinet-56-2024-en"]
    assert row["url"] in out
    assert "kb/sources/cabinet-56-2024-en.pdf" in out


def test_every_chunk_has_the_order_fields():
    fields = {"document_id", "article", "clause", "page", "text_en", "text_ar", "status", "retention_class", "node"}
    for chunk in kb.iter_chunks():
        assert fields <= chunk.keys(), chunk.get("clause")
        assert chunk["text_en"] or chunk["text_ar"]


def test_clause_ids_are_unique_per_document():
    seen = set()
    for chunk in kb.iter_chunks():
        key = (chunk["document_id"], chunk["clause"])
        assert key not in seen, key
        seen.add(key)


def test_verify_prints_four_status_counts(capsys):
    kb.verify(print_counts=True)
    out = capsys.readouterr().out
    for status in ("VERIFIED", "REFERENCED", "UNVERIFIED", "HISTORICAL"):
        assert status in out


def test_check_data_rejects_a_listing_page_url():
    row = {"document_id": "x", "status": "VERIFIED", "source_type": "law",
           "url": "https://tdra.gov.ae/en/About/regulations-and-ruling"}
    assert kb.url_problems(row)


def test_ingest_builds_three_collections(tmp_path):
    client = kb.ingest(path=tmp_path / "chroma", embedding_function=kb.HashEmbedding())
    names = {c.name for c in client.list_collections()}
    assert names == {"kb_main", "kb_framework", "kb_decisions"}
    assert client.get_collection("kb_main").count() == sum(1 for _ in kb.iter_chunks())
    assert client.get_collection("kb_framework").count() > 0


def test_export_writes_inputs_md(tmp_path):
    out = kb.export(tmp_path)
    text = out.read_text(encoding="utf-8")
    assert "tdra-cpr-v2-en" in text and "sha256" in text


def test_a_bilingual_heading_with_a_long_arabic_title_is_still_a_clause():
    # pypdf puts the Arabic title on the English heading line (licence-2-2026, 2026-10-21 re-extraction).
    text = "2.1 Roll-Out and Coverage 2.1  تغطية\nshall roll out.\n3.1 General 3.1  الشروط العامة للترخيص\nshall comply.\nيلتزم المرخص له\n3.2 Law\n"
    chunks = kb.split_decimal(text, keep="en")
    assert [c["clause"] for c in chunks] == ["2.1", "3.1", "3.2"]
    assert kb._join(chunks[0]["lines"]) == "Roll-Out and Coverage shall roll out."  # Arabic the lesser part
    assert kb._join(chunks[1]["lines"]) == "General shall comply."


def test_bare_page_numbers_mark_pages_when_asked():
    text = " 1 \nHeader\n1.1 One\n 2 \nHeader\n1.2 Two\n7\n 3 \nHeader\n1.3 Three\n"
    assert [p for p, _ in kb.page_lines(text)] == [1] * 6  # no markers, no option: one page
    assert [(p, l) for p, l in kb.page_lines(text, bare_page_numbers=True)] == [
        (1, "Header"), (1, "1.1 One"), (2, "Header"), (2, "1.2 Two"), (3, "Header"), (3, "1.3 Three")]
