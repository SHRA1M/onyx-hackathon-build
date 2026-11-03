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
    "cabres-106-2026-ar", "cabres-106-2026-en",  # Task 32: the order's portal page URLs; hq saved the texts
    "cabres-200-2025-en", "cabres-200-2025-ar", "cabres-52-2024-ar", "cabres-52-2024-en"}  # Task 33, the same way


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
    assert schema["properties"]["binding_status"]["enum"] == ["binding", "advisory", "method", "decision", "guideline"], \
        "Task 41: guideline added for a statutory guideline the regulator must have regard to (Ofcom, s. 392(6))"
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
    # the counts moved to Task 33's test below (74, 69, 3, 2, 21, 31)


# --- order 2026-10-30-task-33-three-searches Part A ---------------------------------------------------------------

STD = "standards-text/"
TASK_33 = {  # document_id: (status, binding, jurisdiction, language, source_type, sha256 or "", hq local source)
    "3gpp-ts-28-535-v19": ("VERIFIED", "method", "foreign", "en", "standard",
                           "f43be1bda69e707be8e02d197e90218864d36f241152a6cb48c23a492e8321fc", None),
    "etsi-gs-zsm-009-1-v1-1-1": ("VERIFIED", "method", "foreign", "en", "standard",
                                 "492bac2214010d4846b847d45dfd8af629f978c92f97704b9ff29a3c926e4c0b", None),
    "eu-eecc-2018-1972-art105": ("VERIFIED", "binding", "foreign", "en", "extract", None, None),
    "de-tkg-2021-para-56": ("VERIFIED", "binding", "foreign", "de", "extract", None, None),
    "executive-order-3-2004": ("VERIFIED", "binding", "UAE", "en", "executive order",
                               "23f3e4022033142fac09fb7e37281225c2c216fac8cd8c54f02b0e2d6945f2e5", None),
    "executive-order-3-2004-ar": ("VERIFIED", "binding", "UAE", "ar", "executive order",
                                  "99cb1e43df2633fb7c3fbc56e2fb643f709036b44d16963f641fc122fee1ab8f", None),
    "cabres-200-2025-en": ("VERIFIED", "binding", "UAE", "en", None,
                           "cdff987ad304ef162852be32e693634dfae79dddbf0144e63b24b1561a26972d",
                           STD + "modern-tech-trade-penalties-cabinet-200-2025-en.pdf"),
    "cabres-200-2025-ar": ("VERIFIED", "binding", "UAE", "ar", None,
                           "ad851801ec71e97c5ba855da5b3c35e1ff72c3d313428b03e7346f0a769ace5f",
                           STD + "modern-tech-trade-penalties-cabinet-200-2025-ar.pdf"),
    "cabres-52-2024-ar": ("VERIFIED", "binding", "UAE", "ar", None,
                          "32c667ed631031cb33a25d3ed746904b62ba2d0e4bd2097c3990202404e46693",
                          STD + "etransactions-penalties-cabinet-52-2024-ar.pdf"),
    "cabres-52-2024-en": ("VERIFIED", "binding", "UAE", "en", None, None, None),
    "fed-ai-data-authority-2026-06-14": ("VERIFIED", "advisory", "UAE", "ar", "announcement", None, None),  # Task 44 B1
}


def test_task_33_rows_are_the_orders():
    rows = kb.manifest_by_id()
    for document_id, (status, binding, jurisdiction, language, source_type, sha, local) in TASK_33.items():
        r = rows[document_id]
        assert (r["status"], r["binding_status"], r["jurisdiction"], r["language"]) ==             (status, binding, jurisdiction, language), document_id
        if source_type:
            assert r["source_type"] == source_type, document_id
        if sha is not None:
            assert r["sha256"] == sha, document_id
        if local:
            assert kb.LOCAL[document_id]["file"] == local
            if HQ_DIR.exists():  # hq's copy, byte for byte
                assert kb.sha256_file(HQ_DIR / local) == sha, document_id
    eo = rows["executive-order-3-2004"]
    assert (eo["page_count"], eo["is_official_translation"]) == ("28", "yes (cover: Arabic prevails)")
    assert eo["notes"].startswith("Official Gazette 421, October 2004; amended by Supreme Committee Resolutions 4/2005 "
                                  "and 2/2006 (two footnotes). The 10-17 fetch saw only a cover page; the full order "
                                  "was served 2026-10-30.")
    assert "unpublished" not in eo["notes"].lower()
    assert rows["executive-order-3-2004-ar"]["page_count"] == "33"
    assert "German original; no official translation; the row's English gloss is ours." in         rows["de-tkg-2021-para-56"]["notes"]
    assert "Clause 4.2.3 read the same in V18.2.0." in rows["3gpp-ts-28-535-v19"]["notes"]
    assert "EUR-Lex" in rows["eu-eecc-2018-1972-art105"]["notes"] and "refused" in rows["eu-eecc-2018-1972-art105"]["notes"]
    assert "Articles 1 to 8 only; the annex is a separate portal page, not held; see the Arabic row." in         rows["cabres-52-2024-en"]["notes"]
    assert rows["fed-ai-data-authority-2026-06-14"]["notes"].startswith(
        "Announcement, not a law: the Data Office's competences move to the new authority; no decree number or "
        "transfer date published. The PDPL still names the Data Office.")
    for document_id in ("cabres-200-2025-en", "cabres-200-2025-ar", "cabres-52-2024-ar", "cabres-52-2024-en"):
        assert "through a browser 2026-10-30" in rows[document_id]["notes"], document_id


def test_task_33_rows_have_no_chunks_and_the_counts_are_the_orders():
    cited = {d for d, _ in data.cited_chunks()}
    for document_id in TASK_33:
        if document_id != "executive-order-3-2004":  # an older row; it had no chunks either
            assert document_id not in cited, document_id
        assert not kb.has_chunks(document_id), document_id
    manifest = kb.load_manifest()
    status = lambda s: sum(r["status"] == s for r in manifest)
    # Task 34 Part C adds eIDAS, COPPA and Licence 3/2026 (Iyas, 2026-10-30: the pin follows the counts);
    # Task 35 adds six Gulf rows, all foreign (test_task_35_counts); Task 35b five more (test_task_35b_counts)
    assert (len(manifest), status("VERIFIED"), status("UNVERIFIED"), status("REFERENCED")) == (105, 98, 3, 4), \
        "Task 44: ten rows (TRAI 2026 and the UAE AI Charter last) make 105 rows, 98 VERIFIED"
    assert sum(r["jurisdiction"] == "foreign" for r in manifest) == 38, "Task 44: Maine PL c. 294, Korea and TRAI 2026 make 38 foreign texts"
    # the announcement is not an instrument (order Part A)
    assert len({r["instrument"] for r in manifest if r["jurisdiction"] == "UAE"
                and r["source_type"] != "announcement"}) == 38  # Task 44


# --- order 2026-10-30-task-33-three-searches Part B ---------------------------------------------------------------

SPAIN_DATES = "In force 2025-12-28; companies have until 2026-12-28 to adapt (disposición transitoria única)."
AI_ACT_1744 = ("Regulation (EU) 2026/1744 (OJ 2026-07-24) is inside this consolidation; it does not touch Art 50(1) or "
               "50(5).")


def test_task_33_wales_is_held_from_the_current_text():
    r = kb.manifest_by_id()["wales-wls-no1-2015-sch1"]
    assert r["url"] == "https://www.legislation.gov.uk/wsi/2015/996/schedule/1/data.xht?view=snippet&wrap=true"
    assert "as made" not in r["title"] + r["notes"] and "/made" not in r["url"]
    assert "S.I. 2021/1352 (2021-12-03, reg 3(1))" in r["notes"] and "S.I. 2025/339 (2025-03-28, reg 3(3))" in r["notes"]
    path = kb.REPO / "kb" / "sources" / "global" / "wales-wls-no1-2015-sch1.txt"
    if not path.exists():
        pytest.skip("kb/sources/ is local only (gitignored)")
    text = path.read_text(encoding="utf-8")
    assert "/regulation/3/data.xht?view=snippet&wrap=true" in text and "/made/" not in text
    assert "to a corporate joint committee" in text and "Welsh Revenue Authority" in text
    assert (kb.REPO / "kb" / "sources" / "wales-wls-no1-2015-sch1.txt").read_bytes() == path.read_bytes()


def test_task_33_spain_and_ai_act_notes():
    rows = kb.manifest_by_id()
    assert SPAIN_DATES in rows["es-ley-10-2025"]["notes"]
    assert SPAIN_DATES in [g for g in data.load_gaps()["gaps"] if g["id"] == "gap-1"][0]["note"]
    for document_id in ("eu-ai-act-2026-07-27", "eu-ai-act-2026-07-27-art14-26"):
        assert AI_ACT_1744 in rows[document_id]["notes"], document_id


# --- order 2026-10-30 Task 34 Part C: texts the report cites but the manifest lacked --------------------------------

TASK_34 = {  # document_id: (jurisdiction, binding, source_type, sha256, url, local file)
    "eidas-910-2014-art8": ("foreign", "binding", "extract",
                            "fa53cfcbef9b82c81029833f10dee1e866c003bfbeaae26d8f6f98da091b6c04",
                            "https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32014R0910",
                            "../../../engineering/onyx-hackathon-build/kb/sources/global/eidas-910-2014-art8.txt"),
    "coppa-16cfr312-5": ("foreign", "binding", "extract",
                         "f62f7bff5bb3659e176c669b7aabab412cfca352dc2d996fcafc3bd41b04b6b5",
                         "https://www.ecfr.gov/current/title-16/chapter-I/subchapter-C/part-312/section-312.5",
                         "../../../engineering/onyx-hackathon-build/kb/sources/global/coppa-16cfr312-5.txt"),
    "licence-3-2026": ("UAE", "binding", "licence",
                       "ccafd4ed2d5a960bc1fb2ff27c6161a95a948ee2547ac13b87589a79ddcf7924",
                       "https://tdra.gov.ae/-/media/About/LICENSING/EN/Licence-32026-EITC-Public.ashx",
                       STD + "licence-3-2026-eitc-du-public-telecom-en-ar.pdf"),
}


def test_task_34_rows_are_verified_from_the_publishers_files_with_no_chunks():
    rows = kb.manifest_by_id()
    cited = {d for d, _ in data.cited_chunks()}
    for document_id, (jurisdiction, binding, source_type, sha, url, local) in TASK_34.items():
        r = rows[document_id]
        assert (r["status"], r["binding_status"], r["jurisdiction"], r["source_type"], r["sha256"], r["url"]) ==             ("VERIFIED", binding, jurisdiction, source_type, sha, url), document_id
        assert r["http_status"] == "200" and int(r["bytes"]) > 0 and not kb.url_problems(r), document_id
        assert kb.LOCAL[document_id]["file"] == local
        held = (kb.REPO / "kb" / "sources" / "global" / f"{document_id}.txt") if jurisdiction == "foreign"             else (HQ_DIR / local)
        if held.exists():
            assert kb.sha256_file(held) == sha, document_id
        assert document_id not in cited and not kb.has_chunks(document_id), document_id
    for document_id in ("eidas-910-2014-art8", "coppa-16cfr312-5"):
        assert "never a deciding clause" in rows[document_id]["notes"]
    assert rows["licence-3-2026"]["page_count"] == "47"


# --- order 2026-10-30-task-35-gulf-rows, base and Addendum A: six Gulf rows, binding in their state ----------------

GULF = STD + "gulf-2026-10-30/"
TASK_35 = {  # document_id: (sha256, local file, language, source_type, page_count)
    "qatar-cra-ccpr-2024": ("c8a04d663cad91b8b39800e509201cdc703d78b4f5efaffae6a5143594ece53d",
                            GULF + "qatar-cra-ccpr-2024.pdf", "en,ar", "regulation", "69"),
    "kuwait-citra-res-69-2022-en": ("4c9f2e4d746969e39866e94e3c256ec30406af316bbe90c5fdec6d2df8685bfa",
                                    GULF + "kuwait-citra-res-69-2022-en.pdf", "en", "decision", "2"),
    "kuwait-citra-users-rights-ar": ("5107d9d0eafc55a9c680edd568b9e0e186c2a1810d75725e87ca14e4def7d5bb",
                                     GULF + "kuwait-citra-users-rights-ar.pdf", "ar", "regulation", "18"),
    "saudi-cst-user-protection-552-1445-en": ("113cc118ff4eb0f6b36415eafd3557f50bd01712ca5cc68670484a592857969d",
                                              STD + "saudi-cst-user-protection-552-1445-en.pdf", "en", "regulation", "34"),
    "saudi-cst-user-protection-552-1445-ar": ("eaa4035d46b5cf0b203f70746f3d4768f3a9b6e831f329143798c30aac8a4f10",
                                              STD + "saudi-cst-user-protection-552-1445-ar.pdf", "ar", "regulation", "32"),
    "qatar-decree-law-16-2010-ar": ("505cb4cdae5f07e22537d4c58523efcf9f8ce20ab84c354083335801d289881a",
                                    GULF + "qatar-decree-law-16-2010-ar-extract.md", "ar", "extract", ""),
}


def test_task_35_six_rows_are_verified_foreign_binding_with_no_chunks():
    rows = kb.manifest_by_id()
    cited = {d for d, _ in data.cited_chunks()}
    for document_id, (sha, local, language, source_type, pages) in TASK_35.items():
        r = rows[document_id]
        assert (r["status"], r["binding_status"], r["jurisdiction"], r["language"], r["source_type"], r["sha256"],
                r["page_count"], r["http_status"]) == \
            ("VERIFIED", "binding", "foreign", language, source_type, sha, pages, "200"), document_id
        assert r["url"].startswith("https://") and not kb.url_problems(r), document_id
        assert "never a deciding clause" in r["notes"], document_id  # binding in its own state, never a gate basis
        assert kb.LOCAL[document_id]["file"] == local
        if (HQ_DIR / local).exists():
            assert kb.sha256_file(HQ_DIR / local) == sha and int(r["bytes"]) == (HQ_DIR / local).stat().st_size
        assert document_id not in cited and not kb.has_chunks(document_id), document_id


def test_task_35_row_notes_carry_the_orders_caveats():
    rows = kb.manifest_by_id()
    assert "in-force date not read" in rows["qatar-cra-ccpr-2024"]["notes"].lower()
    assert "Which language prevails: not stated" in rows["qatar-cra-ccpr-2024"]["notes"]
    assert "Art 4 in force on publication in the Official Gazette (date not found)" in \
        rows["kuwait-citra-res-69-2022-en"]["notes"]
    assert "whether every clause stood on 2022-04-21 is not known" in rows["kuwait-citra-users-rights-ar"]["notes"]
    for document_id in ("saudi-cst-user-protection-552-1445-en", "saudi-cst-user-protection-552-1445-ar"):
        notes = rows[document_id]["notes"]
        assert "552/1445 of 08/02/2024, replaces 423/1441" in notes and \
            "2024-05-08 (computed from the 90 days; not printed)" in notes, document_id
    assert rows["saudi-cst-user-protection-552-1445-ar"]["notes"].startswith(
        "Text layer unreadable; quotes transcribed from page images, two independent readings agree; not eye-checked by "
        "a person.")
    assert "URL returns 200" in rows["qatar-decree-law-16-2010-ar"]["notes"]
    # Kuwait's decision (en) and regulation (ar) are two texts, not one text in two languages
    assert rows["kuwait-citra-res-69-2022-en"]["instrument"] != rows["kuwait-citra-users-rights-ar"]["instrument"]
    assert rows["saudi-cst-user-protection-552-1445-en"]["instrument"] == \
        rows["saudi-cst-user-protection-552-1445-ar"]["instrument"]


def test_task_35_counts():
    manifest = kb.load_manifest()
    status = lambda s: sum(r["status"] == s for r in manifest)
    # Task 35b adds five foreign rows (test_task_35b_counts)
    assert (len(manifest), status("VERIFIED"), status("REFERENCED"), status("UNVERIFIED")) == (105, 98, 4, 3), \
        "Task 44: ten rows (TRAI 2026 and the UAE AI Charter last) make 105 rows, 98 VERIFIED"
    assert sum(r["jurisdiction"] == "foreign" for r in manifest) == 38, "Task 44: Maine PL c. 294, Korea and TRAI 2026 make 38 foreign texts"
    assert len({r["instrument"] for r in manifest if r["jurisdiction"] == "UAE"
                and r["source_type"] != "announcement"}) == 38  # Task 44: web pages and the news report counted here


# --- order 2026-10-30-task-35b-bot-disclosure (Addendum B): five bot-disclosure rows, binding in their state ---------

BOT = STD + "bot-disclosure-2026-10-30/"
CA_GLOBAL = "../../../engineering/onyx-hackathon-build/kb/sources/global/"
TASK_35B = {  # document_id: (sha256, local file, source_type, http_status, page_count)
    "maine-1500-dd": ("85e41c95d5905780ac6cc4289fbbcb8cccba60bac75c4ea03a25084b568efe2e", BOT + "maine-1500-DD.html",
                      "law", "200", ""),
    "india-trai-tccrr-2012": ("5d0b0da12fc58d88ea9cb3924a7bcb3ac0aaf7e2ae11675fd9ce2c1957eb0ef3",
                              BOT + "india-trai-tccrr-2012.pdf", "regulation", "200", "13"),
    "texas-bcc-552": ("dbfba8a96dc3cd584157ca66aaafdf67e0ed15dd5a0c8a58f3d4bd0f109fc646", BOT + "texas-bcc-552.html",
                      "law", "200", ""),
    # leginfo answers curl with 403: an extract of the read file's quotes, hashed as filed (Addendum B item 1)
    "california-bpc-17940-17943": ("cfa4c3ccba6c6fd4018618ba541ea4a641d765af5b44ee2634b9a0821feff125",
                                   CA_GLOBAL + "california-bpc-17940-17943.txt", "extract", "403", ""),
    "california-hsc-1339-75": ("86d9eda28fb05b61685d04a063874d7d2f98e763e264375f9425e2b7ac69aa2c",
                               CA_GLOBAL + "california-hsc-1339-75.txt", "extract", "403", ""),
}


def test_task_35b_five_rows_are_verified_foreign_binding_with_no_chunks():
    rows = kb.manifest_by_id()
    cited = {d for d, _ in data.cited_chunks()}
    for document_id, (sha, local, source_type, http, pages) in TASK_35B.items():
        r = rows[document_id]
        assert (r["status"], r["binding_status"], r["jurisdiction"], r["language"], r["source_type"], r["sha256"],
                r["page_count"], r["http_status"]) == \
            ("VERIFIED", "binding", "foreign", "en", source_type, sha, pages, http), document_id
        assert r["url"].startswith("https://") and not kb.url_problems(r), document_id
        assert r["notes"].endswith("Global example; never a deciding clause."), document_id  # never a gate basis
        assert kb.LOCAL[document_id]["file"] == local
        if (HQ_DIR / local).exists():
            assert kb.sha256_file(HQ_DIR / local) == sha and int(r["bytes"]) == (HQ_DIR / local).stat().st_size
        assert document_id not in cited and not kb.has_chunks(document_id), document_id


def test_task_35b_row_notes_print_only_what_the_page_prints():
    rows = kb.manifest_by_id()
    assert "In-force date: not on the statute page." in rows["maine-1500-dd"]["notes"]
    assert '"Effective January 1, 2019. Operative July 1, 2019, pursuant to Section 17943."' in \
        rows["california-bpc-17940-17943"]["notes"]
    assert '"Effective January 1, 2025" (AB 3030, Stats. 2024, Ch. 848)' in rows["california-hsc-1339-75"]["notes"]
    assert '"eff. January 1, 2026"' in rows["texas-bcc-552"]["notes"]
    assert "the chapter text loads by script and is not in them" in rows["texas-bcc-552"]["notes"]
    assert "date not verified" in rows["india-trai-tccrr-2012"]["notes"]
    for document_id in ("california-bpc-17940-17943", "california-hsc-1339-75"):
        assert "the sha256 is the extract file's" in rows[document_id]["notes"], document_id


def test_task_35b_california_extracts_carry_exactly_the_read_files_quotes():
    read = HQ_DIR / "perplexity-2026-10-30" / "bot-disclosure-statutes-read-2026-10-30-fable.md"
    files = [kb.REPO / "kb" / "sources" / "global" / f"{d}.txt" for d in ("california-bpc-17940-17943",
                                                                       "california-hsc-1339-75")]
    if not read.exists() or not all(f.exists() for f in files):
        pytest.skip("kb/sources/ is local only (gitignored, addendum item 15)")
    table = read.read_text(encoding="utf-8")
    for f in files:
        source, _, _, *clauses = f.read_text(encoding="utf-8").rstrip("\n").split("\n")
        assert source == "Source: " + kb.manifest_by_id()[f.stem]["url"]
        assert clauses, f.name
        for line in clauses:
            assert line.split(": ", 1)[1] in table, line[:40]


def test_task_35b_counts():
    manifest = kb.load_manifest()
    status = lambda s: sum(r["status"] == s for r in manifest)
    assert (len(manifest), status("VERIFIED"), status("REFERENCED"), status("UNVERIFIED")) == (105, 98, 4, 3), \
        "Task 44: ten rows (TRAI 2026 and the UAE AI Charter last) make 105 rows, 98 VERIFIED"
    assert sum(r["jurisdiction"] == "foreign" for r in manifest) == 38, "Task 44: Maine PL c. 294, Korea and TRAI 2026 make 38 foreign texts"
    assert len({r["instrument"] for r in manifest if r["jurisdiction"] == "UAE"
                and r["source_type"] != "announcement"}) == 38  # Task 44: web pages and the news report counted here


# --- order 2026-11-02 Task 43: five texts (DIFC, ADGM, ITU F-series) and the WAM page --------------------------------

TASK_43 = {  # document_id: (jurisdiction, binding, source_type, country, sha256 of the extract, page_count)
    "difc-dp-law-5-2020": ("UAE-free-zone", "binding", "law", "UAE",
                           "0f1345a99a100ac5bfddbedd599b87620d43015094f754d0c54e2d0e74eb64b2", "54"),
    "difc-dp-regulations-v2-2023": ("UAE-free-zone", "binding", "regulation", "UAE",
                                    "59dadfe2f05de8db1fbfd08a5468016be9aedcd3d10c5385353236d9eabcd025", "20"),
    "adgm-dpr-2021": ("UAE-free-zone", "binding", "extract", "UAE",
                      "13b6c0cec2acdc390682ac05bceff6c65fe522913b378714928bc1f29078909d", ""),
    "itu-t-f746-16": ("international", "method", "standard", "international",
                      "efd3821ce46046b5b0000eda5ebd74cdc2298e4e232cff354ad131c849537b37", "24"),
    "itu-t-f748-67": ("international", "method", "standard", "international",
                      "c05e362fd940ecfce82ef159d21a71b36d09e89088881d37e91651ce541234a8", "30"),
    "wam-2026-06-14-ai-data-authority": ("UAE", "advisory", "announcement", "UAE",
                                         "c10f13619aa0cfb40f2b6c0de577cae6ead870c0eb4c188c3d41dec0f4751430", ""),
}


def test_task_43_rows_are_the_orders():
    rows = kb.manifest_by_id()
    for document_id, (jurisdiction, binding, source_type, country, sha, pages) in TASK_43.items():
        r = rows[document_id]
        assert (r["status"], r["jurisdiction"], r["binding_status"], r["source_type"], r["country"], r["sha256"],
                r["page_count"], r["language"], r["fetched_at"]) == \
            ("VERIFIED", jurisdiction, binding, source_type, country, sha, pages, "en", "2026-11-02"), document_id
        assert not kb.has_chunks(document_id), document_id  # no chunks (order item 1)
        assert kb.LOCAL[document_id]["file"].endswith(f"kb/sources/global/{document_id}.txt"), document_id
    assert rows["itu-t-y3172"]["jurisdiction"] == "international"  # the ITU rows follow Y.3172's row (hq answer 4)
    assert "Compliance voluntary (p. 4)" in rows["itu-t-f746-16"]["notes"] + rows["itu-t-f748-67"]["notes"]
    assert "452,759 bytes, 24 pages" in rows["itu-t-f746-16"]["notes"]
    assert "1,851,338 bytes, 30 pages" in rows["itu-t-f748-67"]["notes"]
    assert "Prime Minister approved" in rows["wam-2026-06-14-ai-data-authority"]["notes"]


def test_task_43_free_zone_jurisdiction_is_one_schema_value():
    schema = json.loads((kb.KB_DIR / "manifest.schema.json").read_text(encoding="utf-8"))
    assert schema["properties"]["jurisdiction"]["enum"] == ["UAE", "UAE-free-zone", "foreign", "international"]
    manifest = kb.load_manifest()
    assert sorted(r["document_id"] for r in manifest if r["jurisdiction"] == "UAE-free-zone") == \
        ["adgm-dpr-2021", "difc-dp-law-5-2020", "difc-dp-regulations-v2-2023"]
    # the free-zone rows are not UAE instruments, and the WAM page is an announcement, so the report's 31 holds
    assert len({r["instrument"] for r in manifest if r["jurisdiction"] == "UAE"
                and r["source_type"] not in ("announcement", "web_page", "news")}) == 34  # Task 44: VD 1/2009, DHA, the AI Charter
    assert sum(r["jurisdiction"] == "foreign" for r in manifest) == 38


def test_task_43_extracts_match_their_hashes():
    for document_id, (*_, sha, _) in TASK_43.items():
        held = kb.REPO / "kb" / "sources" / "global" / f"{document_id}.txt"
        if not held.exists():
            pytest.skip("kb/sources/ is local only (gitignored)")
        assert kb.sha256_file(held) == sha, document_id
        assert (kb.REPO / "kb" / "sources" / f"{document_id}.txt").read_bytes() == held.read_bytes(), document_id
        assert kb.read_text(held).startswith("Source: https://"), document_id
