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
    if not kb._framework_documents():
        # CI runs no `kb fetch` (it rewrites the manifest's access dates); the dimensions file is fetched, not committed
        pytest.skip("kb/sources/itu-readiness-dimensions.json not on disk: run `python -m onyx kb fetch`")
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


# --- order 2026-10-21-task-9-fixes-tasks-10-11 item 9, hq ruling (a) -----------------------------------------------

LANDING_ROWS = {
    "telecom-law-3-2003-en", "telecom-law-3-2003-ar", "etransactions-46-2021-ar", "consumer-law-15-2020-en",
    "consumer-law-15-2020-ar", "cabinet-66-2023-en", "cabinet-66-2023-ar", "cabinet-56-2024-en", "cabinet-56-2024-ar",
    "cabinet-57-2024-en", "cabinet-57-2024-ar", "child-digital-safety-26-2025-en", "child-digital-safety-26-2025-ar",
    "cybercrimes-34-2021-en", "cybercrimes-34-2021-ar", "itu-t-y3172",
    "cabres-106-2026-ar", "cabres-106-2026-en"}  # Task 32: the order's portal page URLs; hq saved the texts


def test_no_portal_url_except_the_marked_landing_rows():
    rows = kb.load_manifest()
    assert {r["document_id"] for r in rows if kb.LANDING_MARK in r["notes"]} == LANDING_ROWS
    assert not [p for r in rows for p in kb.url_problems(r)]


def test_a_landing_url_without_the_mark_is_rejected():
    row = {"document_id": "x", "status": "VERIFIED", "source_type": "law", "notes": "",
           "url": "https://uaelegislation.gov.ae/en/legislations/1132"}
    assert kb.url_problems(row)
    assert kb.url_problems({**row, "url": "https://www.itu.int/rec/T-REC-Y.3172/en"})
    assert not kb.url_problems({**row, "url": row["url"] + "/download"})


def test_kb_export_is_committed_with_a_link_per_record(tmp_path):
    out = kb.export(tmp_path)
    assert out.read_bytes() == (kb.KB_DIR / "export" / "InputDocs" / "Inputs.md").read_bytes()
    text = out.read_text(encoding="utf-8")
    for r in kb.load_manifest():
        if r["url"]:
            assert f"]({r['url']})" in text, r["document_id"]
    assert text.count("document link not verified") == len(LANDING_ROWS)


# --- order 2026-10-29-task-29 Part C2: the KB datasheet --------------------------------------------------------

def test_datasheet_counts_match_kb_verify(capsys):
    kb.verify(print_counts=True)
    counts = capsys.readouterr().out.splitlines()[0]  # "VERIFIED 47  REFERENCED 1  UNVERIFIED 3  HISTORICAL 0"
    sheet = (kb.KB_DIR / "DATASHEET.md").read_text(encoding="utf-8")
    for status, n in re.findall(r"([A-Z]+) (\d+)", counts):
        assert f"| {status} | {n} |" in sheet, (status, n)
    chunks = list(kb.iter_chunks())
    assert f"{len(chunks)} cited clauses in {len({c['document_id'] for c in chunks})} documents" in sheet
    assert f"{sum(kb.LANDING_MARK in r['notes'] for r in kb.load_manifest())} rows link a landing page" in sheet


def test_datasheet_idempotent(tmp_path):
    committed = (kb.KB_DIR / "DATASHEET.md").read_bytes()
    out = kb.write_datasheet(tmp_path / "DATASHEET.md")
    assert out.read_bytes() == committed
    assert kb.write_datasheet(tmp_path / "DATASHEET.md").read_bytes() == committed


def test_datasheet_reads_the_manifest_only():
    sheet = kb.datasheet()
    rows = kb.load_manifest()
    for r in rows:
        if r["status"] == "UNVERIFIED":
            assert r["document_id"] in sheet
    assert "lam-alef" in sheet and "14(3)" in sheet and "page images" in sheet
    assert "Generated by `python -m onyx kb datasheet`" in sheet


# --- order 2026-10-30-task-30-global-examples -----------------------------------------------------------------

def test_task_30_three_global_sources_are_verified_binding_foreign():
    rows = kb.manifest_by_id()
    expected = {"es-ley-10-2025": "es", "wales-wls-no1-2015-sch1": "en", "us-tsr-16cfr310": "en"}
    for document_id, language in expected.items():
        r = rows[document_id]
        assert (r["status"], r["binding_status"], r["jurisdiction"], r["language"]) ==             ("VERIFIED", "binding", "foreign", language), document_id
        assert len(r["sha256"]) == 64 and r["url"].startswith("https://") and "never a deciding clause" in r["notes"]
        assert kb.LOCAL[document_id]["file"].endswith(f"kb/sources/global/{document_id}.txt")
    assert rows["us-tsr-16cfr310"]["url"].startswith("https://www.ecfr.gov/")  # official, not a mirror
    # the counts moved to Task 31's test below (59, 55, 17)


# --- order 2026-10-30-task-31-binding-examples ----------------------------------------------------------------

TASK_31_HOSTS = {"sg-eta-2010-s15": "https://sso.agc.gov.sg/", "us-utah-13-77-102": "https://le.utah.gov/",
                 "ca-bccrt-2024-149-moffatt": "https://decisions.civilresolutionbc.ca/",
                 "eu-roaming-2022-612-art14": "https://eur-lex.europa.eu/",
                 "eu-ai-act-2026-07-27-art14-26": "https://eur-lex.europa.eu/"}


def test_task_31_five_extracts_are_verified_foreign_from_the_official_sites():
    rows = kb.manifest_by_id()
    for document_id, host in TASK_31_HOSTS.items():
        r = rows[document_id]
        binding = "decision" if document_id == "ca-bccrt-2024-149-moffatt" else "binding"
        assert (r["status"], r["binding_status"], r["jurisdiction"], r["language"], r["source_type"]) == \
            ("VERIFIED", binding, "foreign", "en", "extract"), document_id
        assert r["url"].startswith(host) and r["fetched_at"] == "2026-10-30" and r["http_status"] == "200"
        assert len(r["sha256"]) == 64 and int(r["bytes"]) > 0 and "never a deciding clause" in r["notes"]
        assert kb.LOCAL[document_id]["file"].endswith(f"kb/sources/global/{document_id}.txt")
    ai = rows["eu-ai-act-2026-07-27-art14-26"]
    assert ai["url"] == rows["eu-ai-act-2026-07-27"]["url"]  # same consolidated URL, a new row
    assert ai["notes"].startswith("High-risk systems only. Chapter III Sections 1 to 3 apply from 2027-12-02 (Annex "
                                  "III) and 2028-08-02 (Annex I), Regulation (EU) 2026/1744 Art 1(40)(b).")
    schema = json.loads((kb.KB_DIR / "manifest.schema.json").read_text(encoding="utf-8"))
    assert schema["properties"]["binding_status"]["enum"] == ["binding", "advisory", "method", "decision"]
    # the counts moved to Task 32's test below (64, 59, 17)


# --- order 2026-10-30-task-32-operator-codes ------------------------------------------------------------------

OPERATOR_CODES = {
    "eand-code-of-practice-en": (
        "e& (Etisalat)", "https://eand.com/en/system/com/assets/docs/general/code-of-practice-for-customer-affairs.pdf",
        "4b6383a7523a3e2b6122dc923199583be7a1f15cbf26c6e6172f39fa31d05ddd", "13",
        "§1: not a contract or part of one. No version or date printed.",
        "standards-text/eand-code-of-practice-customer-affairs-en.pdf"),
    "du-code-of-practice-en": (
        "EITC (du)", "https://www.du.ae/files/1430740188355",
        "8f8014d981c1a407715a03ddb6fbd28192b81d52f414150a3f64b68d42e8e34d", "5",
        "§1: approved by the TDRA; not a contract or part of one. No date printed. Covers du and Virgin Mobile UAE.",
        "standards-text/du-code-of-practice-en.pdf"),
}
TASK_32_IDS = [*OPERATOR_CODES, "cabres-106-2026-ar", "cabres-106-2026-en", "csc-ai-security-policy-v1-1"]
CSC_NOTES = ("Host unreachable from Amman 2026-10-17 and 2026-10-30; no Internet Archive copy. Described at u.ae (page "
             "updated 2026-07-02): six chapters, Governance, Infrastructure and Application Security, Algorithm "
             "Security, Operational Safety, Adversarial AI Attacks, AI Monitoring and Response. Not read.")


def test_task_32_operator_codes_are_verified_advisory_operator_codes():
    rows = kb.manifest_by_id()
    for document_id, (issuer, url, sha, pages, notes, local) in OPERATOR_CODES.items():
        r = rows[document_id]
        assert (r["status"], r["binding_status"], r["jurisdiction"], r["language"], r["source_type"]) == \
            ("VERIFIED", "advisory", "UAE", "en", "operator code"), document_id
        assert (r["issuer"], r["url"], r["sha256"], r["page_count"], r["fetched_at"]) == (issuer, url, sha, pages,
                                                                                           "2026-10-30")
        assert r["notes"] == notes and r["http_status"] == "200"
        assert kb.LOCAL[document_id]["file"] == local
        if HQ_DIR.exists():  # the operator's file today is hq's copy, byte for byte
            assert kb.sha256_file(HQ_DIR / local) == sha


def test_task_32_resolution_106_2026_rows_arabic_prevails():
    rows = kb.manifest_by_id()
    ar, en = rows["cabres-106-2026-ar"], rows["cabres-106-2026-en"]
    for r, lang in ((ar, "ar"), (en, "en")):
        assert (r["status"], r["binding_status"], r["jurisdiction"], r["language"], r["instrument"]) == \
            ("VERIFIED", "binding", "UAE", lang, "cabres-106-2026")
        assert r["url"] == f"https://uaelegislation.gov.ae/{lang}/legislations/4506"
        assert "Regulation of Children's Access to Social Media Platforms" in r["title"]
        assert "Issued 2026-06-17, effective 2026-06-30, Official Gazette 826 of 2026-06-29" in r["notes"]
    assert ar["page_count"] == "7" and ar["is_official_translation"] == "original"
    assert "Portal: the Arabic text prevails." in en["notes"]
    assert kb.LOCAL["cabres-106-2026-ar"]["file"] == "standards-text/cabinet-resolution-106-2026-children-social-media-ar.pdf"
    assert kb.LOCAL["cabres-106-2026-en"]["file"] == "standards-text/cabinet-resolution-106-2026-children-social-media-en.txt"


def test_task_32_csc_policy_is_unverified_and_says_why():
    r = kb.manifest_by_id()["csc-ai-security-policy-v1-1"]
    assert (r["status"], r["binding_status"], r["jurisdiction"], r["language"], r["sha256"]) == \
        ("UNVERIFIED", "advisory", "UAE", "en", "")
    assert r["url"].startswith("https://csc.gov.ae/documents/38662/1042755/National+Cyber+Security+Policy+for+")
    assert r["title"].startswith("The National Cyber Security Policy for Artificial Intelligence, v1.1")
    assert r["issuer"] == "UAE Cyber Security Council"
    assert CSC_NOTES in r["notes"] and "binding status unknown" in r["notes"]


def test_task_32_rows_have_no_chunks_and_the_counts_are_the_orders():
    cited = {d for d, _ in data.cited_chunks()}
    for document_id in TASK_32_IDS:
        assert not kb.has_chunks(document_id) and document_id not in cited, document_id
    manifest = kb.load_manifest()
    status = lambda s: sum(r["status"] == s for r in manifest)
    assert (len(manifest), status("VERIFIED"), status("UNVERIFIED"), status("REFERENCED")) == (64, 59, 4, 1)
    assert sum(r["jurisdiction"] == "foreign" for r in manifest) == 17
    assert len({r["instrument"] for r in manifest if r["jurisdiction"] == "UAE"}) == 29
