"""Task 47: retrieval measured on its own, with no model and no mandate list.

Each key step's text (scenario file, English and Arabic) goes to the retriever within the documents of the step's
agent, as Agent.retrieve sends it; the top 8 chunk ids are the measurement. eval.py scores them against the keys.

Two embedders: the shipped all-MiniLM-L6-v2 (kb_main in data/chromadb, from `kb ingest`) and a multilingual one in
kb/index-bilingual/ (`retrieval-index`, git-ignored, never read by an agent, a run or the gate). The top-8 lists are
committed in eval/retrieval.json: CI holds neither index, so it recomputes the figures from the lists, the way a replay
reads a recorded log, and inputs_hash fails closed if the chunks, the queries or the document scope moved. `eval`
re-measures whichever index is on disk. The bilingual index stores its query vectors, so `eval` needs no
sentence-transformers.

Task 50 adds, each under its own name in the record and in no scored run: `bm25` (plain code, no index), `e5-base` and
`bge-m3` (each its own index in a sub-folder of kb/index-bilingual/), and `hybrid-e5-base`, `hybrid-bge-m3` (reciprocal
rank fusion of bm25 and that index). Rebuilding e5-small replaces kb/index-bilingual/, sub-folders included.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
import shutil
import sys
import time
from collections import Counter
from importlib import metadata
from pathlib import Path
from typing import Any, Callable

from onyx import data, kb
from onyx.agents import AGENTS
from onyx.agents.base import ChromaRetriever, HybridRetriever, Retriever, chunk_id
from onyx.runs import LANGS, SCENARIOS

K = 8
RECORD = kb.REPO / "eval" / "retrieval.json"
BILINGUAL_DIR = kb.KB_DIR / "index-bilingual"
META = "meta.json"
COLLECTION = "kb_main"
SHIPPED = "all-MiniLM-L6-v2"
# Order Task 47, in the order to try. The e5 cards ask for these prefixes; bge-m3 takes none.
MODELS = {"intfloat/multilingual-e5-base": ("query: ", "passage: "),
          "intfloat/multilingual-e5-small": ("query: ", "passage: "),
          "BAAI/bge-m3": ("", "")}
BUILD_LIMIT_SECONDS = 30 * 60
NOT_BUILT = "bilingual index not built"
SHIPPED_NOT_BUILT = "shipped index not built"
Encoder = Callable[[list[str]], list[list[float]]]
# Task 50: the record's name of each further dense index, which is also its sub-folder of BILINGUAL_DIR.
DENSE = {"e5-base": "intfloat/multilingual-e5-base", "bge-m3": "BAAI/bge-m3"}
BM25 = "bm25"
# In the order results.md prints them, after the shipped and bilingual sections.
ADDED = (BM25, *DENSE, *(f"hybrid-{name}" for name in DENSE))
TARGET = {"en": 0.40, "ar": 0.30}  # Fable, 2026-11-05, set before any measurement
BM25_K1, BM25_B = 1.5, 0.75
_ALEF_TAA_YAA_TATWEEL = str.maketrans({"أ": "ا", "إ": "ا", "آ": "ا", "ٱ": "ا", "ة": "ه", "ى": "ي", "ـ": None})
_DIACRITICS = re.compile("[ً-ٰٟ]")
_LETTERS = re.compile(r"[^\W\d_]+")


class StaleMeasurement(RuntimeError):
    """The recorded lists, or an index on disk, are of other chunks, queries or document scope."""


def normalize_ar(text: str) -> str:
    """Alef variants to bare alef, taa marbuta to haa, alef maqsura to yaa; diacritics and tatweel gone."""
    return _DIACRITICS.sub("", text.translate(_ALEF_TAA_YAA_TATWEEL))


def tokenize(text: str) -> list[str]:
    """Lowercase, normalised, letters only. Normalised before the split: a diacritic is not a letter and would cut a
    word in two."""
    return _LETTERS.findall(normalize_ar(text.lower()))


class BM25Retriever:
    """Okapi BM25 over text_en and text_ar as two fields of one document: their tokens are counted together and the
    length is both. Term statistics are of the whole corpus; a query searches within the agent's documents, and a chunk
    sharing no term with it is not returned, so a list can be shorter than k. Same signature as ChromaRetriever."""

    def __init__(self, chunks: list[dict[str, Any]] | None = None) -> None:
        self.chunks = list(kb.iter_chunks()) if chunks is None else list(chunks)
        self.counts = {chunk_id(c): Counter(tokenize(c["text_en"]) + tokenize(c["text_ar"])) for c in self.chunks}
        self.lengths = {cid: sum(counts.values()) for cid, counts in self.counts.items()}
        self.average = sum(self.lengths.values()) / len(self.chunks)
        self.seen_in = Counter(term for counts in self.counts.values() for term in counts)

    def score(self, query: str, chunk: dict[str, Any]) -> float:
        cid, total = chunk_id(chunk), 0.0
        for term in sorted(set(tokenize(query))):
            tf, n = self.counts[cid][term], self.seen_in[term]
            if tf:
                idf = math.log(1 + (len(self.chunks) - n + 0.5) / (n + 0.5))
                norm = 1 - BM25_B + BM25_B * self.lengths[cid] / self.average
                total += idf * tf * (BM25_K1 + 1) / (tf + BM25_K1 * norm)
        return total

    def __call__(self, query: str, documents: list[str], k: int) -> list[dict[str, Any]]:
        scored = [(self.score(query, c), c) for c in self.chunks if c["document_id"] in documents]
        ranked = sorted((pair for pair in scored if pair[0] > 0), key=lambda pair: (-pair[0], chunk_id(pair[1])))
        return [chunk for _, chunk in ranked[:k]]


def targets() -> dict[str, list[str]]:
    """Per key step, each must_cite entry mapped to its chunk, as "Key clauses shown" maps it: two rules on one chunk
    count twice."""
    chunks = {r["id"]: f"{r['document_id']}:{r['chunk']}" for r in data.load_rules()}
    return {f"{sid}-{step['n']}": [chunks[rule] for rule in step["must_cite"]]
            for sid in SCENARIOS for step in data.load_key(sid)["steps"] if step["must_cite"]}


def queries() -> list[dict[str, Any]]:
    """One query per key step and language: the text the step's agent receives, within its documents."""
    found = []
    for sid in SCENARIOS:
        steps = {s["n"]: s for s in data.load_scenario(sid)["steps"]}
        for step in data.load_key(sid)["steps"]:
            if step["must_cite"]:
                found += [{"step": f"{sid}-{step['n']}", "lang": lang, "text": steps[step["n"]][f"text_{lang}"],
                           "documents": AGENTS[step["agent"]].documents_of()} for lang in LANGS]
    return found


def _corpus() -> dict[str, dict[str, Any]]:
    """Chunk id to its id, its text as `kb ingest` embeds it, and its document."""
    return {chunk_id(c): {"text": (c["text_en"] + "\n" + c["text_ar"]).strip(), "document_id": c["document_id"]}
            for c in kb.iter_chunks()}


def inputs_hash() -> str:
    payload = {"queries": queries(), "corpus": {cid: c["text"] for cid, c in _corpus().items()}}
    return hashlib.sha256(json.dumps(payload, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()


def measure(retriever: Retriever) -> dict[str, dict[str, list[str]]]:
    lists: dict[str, dict[str, list[str]]] = {}
    for q in queries():
        hits = retriever(q["text"], q["documents"], K)
        lists.setdefault(q["step"], {})[q["lang"]] = [chunk_id(hit) for hit in hits]
    return lists


class StoredQueryRetriever(ChromaRetriever):
    """The bilingual index: the query's vector comes from the index's meta file, written when it was built."""

    def __init__(self, collection: Any, vectors: dict[str, list[float]]) -> None:
        super().__init__(collection)
        self.vectors = vectors

    def __call__(self, query: str, documents: list[str], k: int) -> list[dict[str, Any]]:
        where = {"document_id": {"$in": documents}} if len(documents) > 1 else {"document_id": documents[0]}
        result = self.collection.query(query_embeddings=[self.vectors[query]], n_results=k, where=where)
        return [kb.get_chunk(*hit.split(":", 1)) for hit in result["ids"][0]]


def _collection(path: Path) -> Any | None:
    """kb_main in an index folder, or None; a missing folder stays missing."""
    if not path.exists():
        return None
    import chromadb
    from chromadb.errors import NotFoundError

    try:
        return chromadb.PersistentClient(path=str(path)).get_collection(COLLECTION)
    except NotFoundError:
        return None


def _require_current(collection: Any, name: str, fix: str) -> None:
    """An index of other chunks would print a figure about the wrong corpus."""
    held = collection.get(include=["documents"])
    if dict(zip(held["ids"], held["documents"])) != {cid: c["text"] for cid, c in _corpus().items()}:
        raise StaleMeasurement(f"{name}: the index does not hold the chunks in kb/chunks; run `{fix}`")


def write_index(path: str | Path, name: str, revision: str, seconds: float, encode_passages: Encoder,
                encode_queries: Encoder, command: str = "") -> None:
    """Embed every chunk and every query into a separate index. Nothing here touches data/chromadb."""
    import chromadb

    path, corpus = Path(path), _corpus()
    texts = sorted({q["text"] for q in queries()})
    passages, vectors = encode_passages([c["text"] for c in corpus.values()]), encode_queries(texts)
    if path.exists():
        shutil.rmtree(path)
    client = chromadb.PersistentClient(path=str(path))
    collection = client.create_collection(COLLECTION, metadata={"hnsw:space": "cosine"}, embedding_function=None)
    collection.add(ids=list(corpus), embeddings=passages, documents=[c["text"] for c in corpus.values()],
                   metadatas=[{"document_id": c["document_id"]} for c in corpus.values()])
    meta = {"embedder": name, "revision": revision, "build_seconds": seconds, "command": command,
            "query_vectors": dict(zip(texts, vectors))}
    (path / META).write_text(json.dumps(meta, sort_keys=True, ensure_ascii=False), encoding="utf-8", newline="\n")


def load_record(path: str | Path = RECORD) -> dict[str, Any] | None:
    path = Path(path)
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


def refresh(record_path: str | Path = RECORD, chroma_dir: str | Path = kb.CHROMA_DIR,
            bilingual_dir: str | Path = BILINGUAL_DIR) -> list[str]:
    """Re-measure each index on disk and write the record; an index that is not there leaves its lists as they are.
    Returns what happened, one line each."""
    record_path, lines = Path(record_path), []
    record = load_record(record_path) or {}
    shipped, bilingual = _collection(Path(chroma_dir)), _collection(Path(bilingual_dir))
    dense = {name: _collection(Path(bilingual_dir) / name) for name in DENSE}
    if shipped is None:
        lines.append(SHIPPED_NOT_BUILT)
    else:
        _require_current(shipped, SHIPPED, "uv run python -m onyx kb ingest")
        record["shipped"] = {"embedder": SHIPPED, "lists": measure(ChromaRetriever(shipped))}
    if bilingual is None:
        lines.append(NOT_BUILT)
    else:
        _require_current(bilingual, "bilingual", "retrieval-index")
        meta = json.loads((Path(bilingual_dir) / META).read_text(encoding="utf-8"))
        record["bilingual"] = {**{k: meta[k] for k in ("embedder", "revision", "build_seconds", "command")},
                               "lists": measure(StoredQueryRetriever(bilingual, meta["query_vectors"]))}
    if shipped is not None or bilingual is not None or any(c is not None for c in dense.values()):
        bm25 = BM25Retriever()
        record[BM25] = {"lists": measure(bm25)}
        for name, collection in dense.items():
            if collection is not None:
                _require_current(collection, name, f"retrieval-index --model {DENSE[name]}")
                meta = json.loads((Path(bilingual_dir) / name / META).read_text(encoding="utf-8"))
                stored = StoredQueryRetriever(collection, meta["query_vectors"])
                built = {k: meta[k] for k in ("embedder", "revision", "build_seconds", "command")}
                record[name] = {**built, "lists": measure(stored)}
                record[f"hybrid-{name}"] = {**built, "lists": measure(HybridRetriever(bm25, stored))}
        record.update(inputs_sha256=inputs_hash(), k=K)
        record_path.write_text(json.dumps(record, indent=1, sort_keys=True, ensure_ascii=False) + "\n",
                               encoding="utf-8", newline="\n")
    return lines


def _download(name: str) -> tuple[Path, str]:
    """Only what sentence-transformers loads, at one exact commit (these repos also hold other weight formats and
    hundreds of benchmark result files). The folder is named by the commit, so the revision printed is the one
    embedded with."""
    from huggingface_hub import list_repo_files, snapshot_download

    weights = "model.safetensors" if "model.safetensors" in list_repo_files(name) else "pytorch_model.bin"
    path = Path(snapshot_download(name, allow_patterns=[weights, "*.json", "*.model", "*.txt"]))
    return path, path.name


def index_dir(name: str) -> Path:
    """e5-small keeps kb/index-bilingual/; each further model has its own sub-folder, so building one cannot move the
    e5-small section."""
    return next((BILINGUAL_DIR / short for short, full in DENSE.items() if full == name), BILINGUAL_DIR)


def build_bilingual(out: str | Path | None = None, models: list[str] | None = None) -> int:
    """The first model of the order's list that loads and embeds the whole corpus inside the limit is the one."""
    from sentence_transformers import SentenceTransformer

    corpus = [c["text"] for c in _corpus().values()]
    texts = sorted({q["text"] for q in queries()})
    for name in models or list(MODELS):
        command = f"uv run --with sentence-transformers=={metadata.version('sentence-transformers')} " \
                  f"python -m onyx retrieval-index --model {name}"
        query_prefix, passage_prefix = MODELS[name]
        started = time.perf_counter()
        try:
            path, revision = _download(name)
            print(f"{name}: revision {revision}, loading", flush=True)
            encoder = SentenceTransformer(str(path))

            def encode(prefix: str, items: list[str]) -> list[list[float]]:
                return encoder.encode([prefix + t for t in items], batch_size=8, normalize_embeddings=True,
                                      show_progress_bar=False).tolist()
            passages = encode(passage_prefix, corpus)
            vectors = encode(query_prefix, texts)
        except Exception as error:  # the order: try the next name
            print(f"{name}: failed after {time.perf_counter() - started:.0f} s: {error}", flush=True)
            continue
        seconds = round(time.perf_counter() - started, 1)
        if seconds >= BUILD_LIMIT_SECONDS:
            print(f"{name}: {seconds} s, over the limit of {BUILD_LIMIT_SECONDS} s", flush=True)
            continue
        path = Path(out) if out else index_dir(name)
        write_index(path, name, revision, seconds, lambda _, v=passages: v, lambda _, v=vectors: v, command)
        print(f"{name}: {len(corpus)} chunks and {len(texts)} queries embedded in {seconds} s; index in {path}", flush=True)
        return 0
    print("no bilingual model loaded", file=sys.stderr)
    return 1


def _cli(args) -> int:
    return build_bilingual(models=[args.model] if args.model else None)


def register(subparsers) -> None:
    parser = subparsers.add_parser("retrieval-index", help="build the bilingual index the retrieval benchmark reads "
                                   "(kb/index-bilingual, git-ignored; needs `uv run --with sentence-transformers`)")
    parser.add_argument("--model", choices=list(MODELS), help="one model instead of the order's list")
    parser.set_defaults(func=_cli)
