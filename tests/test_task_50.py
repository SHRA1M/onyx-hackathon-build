"""Task 50: the plain-code BM25, the hybrid retriever, the extra tables in "Retrieval alone". No model, no index."""

from __future__ import annotations

import json
import math

import pytest

from onyx import data, eval as onyx_eval, kb, retrieval
from onyx.agents import AGENTS
from onyx.agents.base import ChromaRetriever, HybridRetriever, chunk_id

TARGET_LINE = "Target set 2026-11-05 before measurement: pooled recall@8 at least 0.40 en and 0.30 ar; "


# --- normalize_ar and tokenize ---------------------------------------------------------------------------------------

@pytest.mark.parametrize("written, normal", [
    ("أحمد", "احمد"),  # alef with hamza above
    ("إذن", "اذن"),  # alef with hamza below
    ("آخر", "اخر"),  # alef with madda
    ("ٱلله", "الله"),  # alef wasla
    ("فاتورة", "فاتوره"),  # taa marbuta to haa
    ("مستوى", "مستوي"),  # alef maqsura to yaa
    ("مُشْتَرِكٌ", "مشترك"),  # diacritics
    ("خـــدمة", "خدمه"),  # tatweel
])
def test_normalize_ar(written, normal):
    assert retrieval.normalize_ar(written) == normal


def test_normalize_ar_leaves_latin_text_alone():
    assert retrieval.normalize_ar("Clause 4.22, opt-in") == "Clause 4.22, opt-in"


def test_tokenize_lowercases_splits_on_non_letters_and_normalizes():
    assert retrieval.tokenize("OTP: opt-in (4.22) الفاتورةُ") == ["otp", "opt", "in", "الفاتوره"]


def test_a_diacritic_does_not_split_an_arabic_word():
    assert retrieval.tokenize("مُشْتَرِك") == ["مشترك"]


# --- BM25 ------------------------------------------------------------------------------------------------------------

CORPUS = [
    {"document_id": "a", "clause": "1", "text_en": "the licensee shall refund the subscriber", "text_ar": ""},
    {"document_id": "a", "clause": "2", "text_en": "roaming charges and roaming notices", "text_ar": "رسوم التجوال"},
    {"document_id": "b", "clause": "1", "text_en": "personal data of the subscriber", "text_ar": ""},
    {"document_id": "b", "clause": "2", "text_en": "", "text_ar": "الفاتورة الشهرية"},
]


def test_bm25_okapi_arithmetic_on_a_fixed_corpus():
    """k1 1.5, b 0.75, idf ln(1 + (N - n + 0.5) / (n + 0.5)), length over both fields of the chunk."""
    bm25 = retrieval.BM25Retriever(CORPUS)
    lengths = [6, 7, 5, 2]
    average = sum(lengths) / 4
    idf = math.log(1 + (4 - 1 + 0.5) / (1 + 0.5))  # "roaming" is in one chunk
    expected = idf * 2 * 2.5 / (2 + 1.5 * (1 - 0.75 + 0.75 * lengths[1] / average))
    assert bm25.score("roaming", CORPUS[1]) == pytest.approx(expected)
    assert bm25.score("roaming", CORPUS[0]) == 0


def test_bm25_reads_both_fields_and_stays_in_scope():
    bm25 = retrieval.BM25Retriever(CORPUS)
    assert [chunk_id(c) for c in bm25("فاتورةُ", ["a", "b"], 8)] == []  # another word form: no stemming
    assert [chunk_id(c) for c in bm25("الفاتورةُ", ["a", "b"], 8)] == ["b:2"]  # Arabic field, normalised both sides
    assert [chunk_id(c) for c in bm25("roaming", ["b"], 8)] == []  # the only match is outside the scope
    assert [chunk_id(c) for c in bm25("subscriber", ["b"], 8)] == ["b:1"]
    assert bm25("subscriber", [], 8) == []


def test_bm25_ties_break_by_chunk_id_so_the_lists_are_stable():
    twins = [{"document_id": d, "clause": "1", "text_en": "same words here", "text_ar": ""} for d in ("z", "y", "x")]
    assert [chunk_id(c) for c in retrieval.BM25Retriever(twins)("words", ["x", "y", "z"], 2)] == ["x:1", "y:1"]


def test_bm25_on_the_committed_chunks_returns_the_shipped_shape():
    documents = AGENTS["care"].documents_of()
    hits = retrieval.BM25Retriever()("Can I cancel the roaming bundle and get a refund?", documents, 8)
    assert 0 < len(hits) <= 8
    for hit in hits:
        assert hit == kb.get_chunk(hit["document_id"], hit["clause"])
        assert hit["document_id"] in documents


# --- the hybrid ------------------------------------------------------------------------------------------------------

def _chunk(cid: str) -> dict:
    document, clause = cid.split(":")
    return {"document_id": document, "clause": clause, "text_en": cid, "text_ar": ""}


class Fixed:
    """A retriever with a fixed ranking that records what it was asked and filters by scope as the real ones do."""

    def __init__(self, ranked: list[str]) -> None:
        self.ranked, self.calls = ranked, []

    def __call__(self, query, documents, k):
        self.calls.append((query, list(documents), k))
        return [_chunk(c) for c in self.ranked if c.split(":")[0] in documents][:k]


def test_hybrid_is_reciprocal_rank_fusion_with_k_60_of_two_top_30s():
    sparse, dense = Fixed(["a:1", "a:2", "a:3"]), Fixed(["a:3", "a:4", "a:1"])
    hits = HybridRetriever(sparse, dense)("q", ["a"], 8)
    scores = {"a:1": 1 / 61 + 1 / 63, "a:3": 1 / 63 + 1 / 61, "a:2": 1 / 62, "a:4": 1 / 62}
    assert [chunk_id(h) for h in hits] == sorted(scores, key=lambda c: (-round(scores[c], 12), c))
    assert sparse.calls == dense.calls == [("q", ["a"], 30)]


def test_hybrid_returns_the_top_8_in_the_shipped_shape_within_scope():
    inside = [f"a:{n}" for n in range(1, 31)]
    outside = [f"z:{n}" for n in range(1, 31)]
    hits = HybridRetriever(Fixed(outside + inside), Fixed(outside + list(reversed(inside))))("q", ["a"], 8)
    assert len(hits) == 8
    assert {h["document_id"] for h in hits} == {"a"}
    assert all(set(h) == {"document_id", "clause", "text_en", "text_ar"} for h in hits)


def test_hybrid_with_no_documents_asks_nobody():
    sparse, dense = Fixed(["a:1"]), Fixed(["a:1"])
    assert HybridRetriever(sparse, dense)("q", [], 8) == []
    assert sparse.calls == dense.calls == []


def test_hybrid_keeps_each_agents_document_scope_as_chroma_retriever_does():
    """The same Retriever signature: both inner retrievers get exactly the agent's documents, the way Agent.retrieve
    hands them to ChromaRetriever."""
    sparse, dense = Fixed([]), Fixed([])
    agent = AGENTS["tdra"](model=None, retriever=HybridRetriever(sparse, dense))
    agent.retrieve("a question")
    assert sparse.calls == dense.calls == [("a question", data.load_mandates()["tdra"]["documents"], 30)]
    assert ChromaRetriever.__call__.__annotations__ == HybridRetriever.__call__.__annotations__


# --- the record and the tables ---------------------------------------------------------------------------------------

def _record_with(*names: str, perfect: tuple[str, ...] = ()) -> dict:
    targets = retrieval.targets()
    def lists(hit: bool) -> dict:
        return {step: {lang: (list(dict.fromkeys(chunks))[:8] if hit else []) for lang in ("en", "ar")}
                for step, chunks in targets.items()}
    record = {"inputs_sha256": retrieval.inputs_hash(), "k": 8,
              "shipped": {"embedder": retrieval.SHIPPED, "lists": lists(False)}}
    for name in names:
        record[name] = {"embedder": "fake/encoder", "revision": "abc", "build_seconds": 1.0, "command": "built",
                        "lists": lists(name in perfect)}
    return record


def test_every_recorded_name_prints_as_its_own_section_with_the_target_line():
    names = ("bm25", "e5-base", "bge-m3", "hybrid-e5-base", "hybrid-bge-m3")
    section = "\n".join(onyx_eval.retrieval_section(_record_with(*names)))
    for name in names:
        assert section.count(f"### {name}, not used in any scored run") == 1
        assert f"{TARGET_LINE}{name}: not met." in section
    assert section.index("### Shipped embedder") < section.index("### bm25")


def test_the_target_line_says_met_only_when_both_languages_reach_it():
    record = _record_with("hybrid-e5-base", perfect=("hybrid-e5-base",))
    assert f"{TARGET_LINE}hybrid-e5-base: met." in "\n".join(onyx_eval.retrieval_section(record))
    targets = retrieval.targets()
    record["hybrid-e5-base"]["lists"] = {step: {"en": list(dict.fromkeys(chunks))[:8], "ar": []}
                                         for step, chunks in targets.items()}
    assert f"{TARGET_LINE}hybrid-e5-base: not met." in "\n".join(onyx_eval.retrieval_section(record))


def test_the_extra_tables_do_not_move_the_shipped_section():
    without = "\n".join(onyx_eval.retrieval_section(_record_with()))
    with_all = "\n".join(onyx_eval.retrieval_section(_record_with("bm25", "hybrid-e5-base")))
    assert with_all.startswith(without.rstrip("\n"))


def test_the_committed_record_prints_every_name_the_order_lists():
    record = json.loads(retrieval.RECORD.read_text(encoding="utf-8"))
    results = (kb.REPO / "eval" / "results.md").read_text(encoding="utf-8")
    assert record["inputs_sha256"] == retrieval.inputs_hash()
    for name in ("bm25", "e5-base", "bge-m3", "hybrid-e5-base", "hybrid-bge-m3"):
        assert name in record
        assert results.count(f"### {name}, not used in any scored run") == 1
        assert f"{TARGET_LINE}{name}: not met." in results  # measured 2026-11-05; the target stands as it was set


def test_refresh_measures_a_dense_index_and_its_hybrid_in_their_own_names(tmp_path):
    embed = kb.HashEmbedding()
    index = tmp_path / "index-bilingual"
    retrieval.write_index(index / "e5-base", name="fake/encoder", revision="abc", seconds=1.5,
                          encode_passages=embed, encode_queries=embed, command="built")
    record = tmp_path / "retrieval.json"
    retrieval.refresh(record, chroma_dir=tmp_path / "no-chroma", bilingual_dir=index)
    written = json.loads(record.read_text(encoding="utf-8"))
    assert {"bm25", "e5-base", "hybrid-e5-base"} <= set(written)
    assert "bge-m3" not in written and "bilingual" not in written
    assert written["e5-base"]["embedder"] == written["hybrid-e5-base"]["embedder"] == "fake/encoder"
    queries = {(q["step"], q["lang"]): q["documents"] for q in retrieval.queries()}
    for name in ("bm25", "e5-base", "hybrid-e5-base"):
        for step, by_lang in written[name]["lists"].items():
            for lang, ranked in by_lang.items():
                assert len(ranked) <= 8
                assert all(c.split(":")[0] in queries[step, lang] for c in ranked), (name, step, lang)


def test_each_new_index_has_its_own_folder_so_the_e5_small_section_cannot_move():
    assert retrieval.index_dir("intfloat/multilingual-e5-small") == retrieval.BILINGUAL_DIR
    assert retrieval.index_dir("intfloat/multilingual-e5-base") == retrieval.BILINGUAL_DIR / "e5-base"
    assert retrieval.index_dir("BAAI/bge-m3") == retrieval.BILINGUAL_DIR / "bge-m3"
