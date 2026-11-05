"""Task 50.1: why the shipped embedder misses. Read-only, no model, nothing written.

For every (query, must-cite entry) pair the shipped lists in eval/retrieval.json miss, re-query the local shipped
Chroma collection for the full ranking within the same document scope as the measurement, and print markdown tables for
the report-back. Run: uv run python -X utf8 scripts/retrieval_diagnose.py (`kb ingest` first if the index is not built).
"""

from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from onyx import kb, retrieval  # noqa: E402
from onyx.agents.base import chunk_id  # noqa: E402
from onyx.eval import retrieval_scores  # noqa: E402

LANGS = ("en", "ar")
LIMITS = (100, 256, 1000)  # words; all-MiniLM-L6-v2 reads the first 256 word pieces of a chunk
CPR = "tdra-cpr-v2-en"
# A short list, for "shares no token" only; BM25 itself uses none.
STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "can", "do", "does", "for", "from", "has", "have", "i", "if", "in",
    "is", "it", "its", "me", "my", "no", "not", "of", "on", "or", "our", "shall", "so", "that", "the", "their", "this",
    "to", "was", "we", "what", "when", "which", "will", "with", "you", "your",
    "في", "من", "الي", "علي", "عن", "ان", "هذا", "هذه", "ذلك", "التي", "الذي", "او", "و", "لا", "ما", "هل", "لي", "مع",
}


def content_tokens(text: str) -> set[str]:
    return set(retrieval.tokenize(text)) - {retrieval.normalize_ar(w) for w in STOPWORDS}


def full_ranking(collection, query: str, documents: list[str]) -> list[str]:
    """Every chunk of the scope, best first: the same call as ChromaRetriever with n_results the size of the scope."""
    size = len(collection.get(where={"document_id": {"$in": documents}}, include=[])["ids"])
    return collection.query(query_texts=[query], n_results=size, where={"document_id": {"$in": documents}})["ids"][0]


def table(header: list[str], rows: list[list[object]]) -> None:
    print("| " + " | ".join(header) + " |")
    print("|" + "---|" * len(header))
    for row in rows:
        print("| " + " | ".join(str(cell) for cell in row) + " |")
    print()


def main() -> int:
    collection = retrieval._collection(kb.CHROMA_DIR)
    if collection is None:
        print(f"{retrieval.SHIPPED_NOT_BUILT}: run `uv run python -m onyx kb ingest` first", file=sys.stderr)
        return 1
    retrieval._require_current(collection, retrieval.SHIPPED, "uv run python -m onyx kb ingest")
    record = retrieval.load_record()
    if record["inputs_sha256"] != retrieval.inputs_hash():
        raise retrieval.StaleMeasurement("eval/retrieval.json is of other chunks, queries or scope")
    targets, lists = retrieval.targets(), record["shipped"]["lists"]
    chunks = {chunk_id(c): c for c in kb.iter_chunks()}
    queries = {(q["step"], q["lang"]): q for q in retrieval.queries()}

    def words(cid: str) -> int:
        return len((chunks[cid]["text_en"] + " " + chunks[cid]["text_ar"]).split())

    pairs = []
    for step, entries in targets.items():
        for lang in LANGS:
            q = queries[step, lang]
            ranking = full_ranking(collection, q["text"], q["documents"])
            # the re-query must reproduce what was measured, or the ranks below describe another index
            if ranking[:8] != lists[step][lang]:
                print(f"re-query differs from the record at {step} {lang}", file=sys.stderr)
                return 1
            shared_query = content_tokens(q["text"])
            for cid in entries:
                chunk = chunks[cid]
                top8_same = sum(chunks[c]["document_id"] == chunk["document_id"] for c in ranking[:8])
                pairs.append({
                    "step": step, "lang": lang, "clause": cid, "document": chunk["document_id"],
                    "has_ar": bool(chunk["text_ar"]), "words": words(cid), "in_scope": chunk["document_id"] in q["documents"],
                    "rank": ranking.index(cid) + 1 if cid in ranking else None, "scope": len(ranking),
                    "shares": bool(shared_query & content_tokens(chunk["text_en"] + " " + chunk["text_ar"])),
                    "top8_same": top8_same})
    missed = [p for p in pairs if p["rank"] is None or p["rank"] > 8]

    print("## Corpus\n")
    both = sum(bool(c["text_en"]) and bool(c["text_ar"]) for c in chunks.values())
    en_only = sum(bool(c["text_en"]) and not c["text_ar"] for c in chunks.values())
    ar_only = sum(not c["text_en"] and bool(c["text_ar"]) for c in chunks.values())
    sizes = sorted(words(c) for c in chunks)
    table(["Chunks", "Both languages", "English only", "Arabic only", "CPR chunks", "Fewest words", "Median words", "Most words"],
          [[len(chunks), both, en_only, ar_only, sum(c["document_id"] == CPR for c in chunks.values()), sizes[0],
            sizes[len(sizes) // 2], sizes[-1]]])

    print(f"## Every miss ({len(missed)} of {len(pairs)} entries)\n")
    table(["Query", "Lang", "Clause", "Document", "Arabic text", "Words", "Rank in scope", "Scope size"],
          [[p["step"], p["lang"], p["clause"], p["document"], "yes" if p["has_ar"] else "no", p["words"],
            p["rank"] if p["rank"] else "not in scope", p["scope"]] for p in missed])

    print("## Grouped counts\n")
    rows = []
    for lang in LANGS:
        mine = [p for p in missed if p["lang"] == lang]
        band = [p for p in mine if p["rank"] and 9 <= p["rank"] <= 30]
        rows.append([lang, len(mine), sum(not p["has_ar"] for p in mine), sum(not p["shares"] for p in mine), len(band),
                     sum(p["top8_same"] > 0 for p in band), sum(p["rank"] is None for p in mine),
                     sum(bool(p["rank"]) and p["rank"] > 30 for p in mine)])
    table(["Lang", "Misses", "Chunk has no Arabic text", "Query and chunk share no token", "Rank 9 to 30",
           "Of those, the top 8 holds a chunk of the same document", "Clause not in scope", "Rank past 30"], rows)

    print("## Recall@8 by what the target chunk is\n")
    def share(selected: list[dict]) -> str:
        hits = sum(p["rank"] is not None and p["rank"] <= 8 for p in selected)
        return f"{hits} of {len(selected)} ({hits / len(selected):.2f})" if selected else "none"
    buckets = [(f"up to {LIMITS[0]} words", lambda p: p["words"] <= LIMITS[0]),
               (f"{LIMITS[0] + 1} to {LIMITS[1]} words", lambda p: LIMITS[0] < p["words"] <= LIMITS[1]),
               (f"{LIMITS[1] + 1} to {LIMITS[2]} words", lambda p: LIMITS[1] < p["words"] <= LIMITS[2]),
               (f"over {LIMITS[2]} words", lambda p: p["words"] > LIMITS[2]),
               ("chunk has Arabic text", lambda p: p["has_ar"]), ("chunk has no Arabic text", lambda p: not p["has_ar"]),
               ("CPR chunk", lambda p: p["document"] == CPR), ("any other document", lambda p: p["document"] != CPR),
               ("query and chunk share a token", lambda p: p["shares"]),
               ("query and chunk share no token", lambda p: not p["shares"])]
    table(["Target", "en", "ar"], [[label, *(share([p for p in pairs if p["lang"] == lang and test(p)]) for lang in LANGS)]
                                   for label, test in buckets])

    print("## Misses by document\n")
    counts = Counter((p["document"], p["lang"]) for p in missed)
    table(["Document", "en", "ar"], [[d, counts[d, "en"], counts[d, "ar"]] for d in sorted({p["document"] for p in missed})])

    lists_bm25 = retrieval.measure(retrieval.BM25Retriever())
    pooled = retrieval_scores(lists_bm25, targets)["recall_at_8"]
    print("BM25 recall@8, same queries and targets, normalisation of 50.2: "
          f"en {pooled['en']['hits']} of {pooled['en']['n']} ({pooled['en']['hits'] / pooled['en']['n']:.2f}); "
          f"ar {pooled['ar']['hits']} of {pooled['ar']['n']} ({pooled['ar']['hits'] / pooled['ar']['n']:.2f})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
