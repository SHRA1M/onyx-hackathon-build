"""Knowledge base: manifest, fetch, verify, clause chunks, ChromaDB ingest, ITU InputDocs export.

Full source texts are fetched to kb/sources/ and never committed (addendum item 15). The committed record is
kb/manifest.csv (one row per document), kb/chunks/*.jsonl (only the clauses rules and mandates cite, Iyas 2026-10-20)
and kb/extracts/ (labelled transcriptions where a text layer cannot be read).
"""

from __future__ import annotations

import csv
import datetime as dt
import hashlib
import json
import math
import os
import re
import shutil
import urllib.error
import urllib.request
from collections import Counter
from pathlib import Path
from typing import Any, Iterable, Iterator

REPO = Path(__file__).resolve().parent.parent
KB_DIR = REPO / "kb"
MANIFEST = KB_DIR / "manifest.csv"
SOURCES_DIR = KB_DIR / "sources"
CHUNKS_DIR = KB_DIR / "chunks"
CHUNKS_FULL_DIR = KB_DIR / "chunks-full"  # every clause, maintainer only, gitignored
EXTRACTS_DIR = KB_DIR / "extracts"
CHROMA_DIR = REPO / "data" / "chromadb"
STATUSES = ("VERIFIED", "REFERENCED", "UNVERIFIED", "HISTORICAL")
COLLECTIONS = ("kb_main", "kb_framework", "kb_decisions")

# Where the maintainer's copies live (the hq notes folder holding standards-text/ and corpus-text/).
SOURCE_DIR_ENV = "ONYX_SOURCE_DIR"
# document_id -> {file, text, splitter, pair_of}: the local file, its text extraction, how to chunk it.
LOCAL: dict[str, dict[str, str]] = json.loads((KB_DIR / "local-sources.json").read_text(encoding="utf-8"))

# A listing or search page in place of the document itself (addendum item 2).
LISTING_PAGE = re.compile(
    r"/(regulations-and-ruling|legal-references|consumer-affairs|licensing|Resources|consumer-tool-hub)/?$"
    r"|^https://u\.ae/?$|^https://tdra\.gov\.ae/?(en|ar)?/?$",
    re.IGNORECASE,
)


# --- manifest ---------------------------------------------------------------------------------------------

def load_manifest() -> list[dict[str, str]]:
    with MANIFEST.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def save_manifest(rows: list[dict[str, str]]) -> None:
    with MANIFEST.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def verified_rows(rows: list[dict[str, str]] | None = None) -> list[dict[str, str]]:
    return [r for r in (rows or load_manifest()) if r["status"] == "VERIFIED"]


def manifest_by_id() -> dict[str, dict[str, str]]:
    return {r["document_id"]: r for r in load_manifest()}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _suffix(document_id: str) -> str:
    return Path(LOCAL.get(document_id, {}).get("file") or "x.pdf").suffix


def source_path(row: dict[str, str]) -> Path | None:
    path = SOURCES_DIR / f"{row['document_id']}{_suffix(row['document_id'])}"
    return path if path.exists() else None


def url_problems(row: dict[str, str]) -> list[str]:
    problems = []
    url = row.get("url", "")
    if url and row.get("source_type") != "web_page" and LISTING_PAGE.search(url):
        problems.append(f"{row['document_id']}: URL is a listing page, not the document: {url}")
    return problems


# --- fetch and verify -------------------------------------------------------------------------------------

def _download(url: str) -> tuple[str, bytes | None]:
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (onyx kb fetch)"})
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return str(response.status), response.read()
    except urllib.error.HTTPError as e:
        return str(e.code), None
    except (urllib.error.URLError, TimeoutError, OSError):
        return "error", None


def fetch(local_dir: str | os.PathLike | None = None, today: str | None = None) -> list[dict[str, str]]:
    """Download every VERIFIED document; where the host blocks or serves other bytes, fall back to the
    maintainer's local copy if its sha256 matches. Records url_accessed and http_status in the manifest."""
    local_dir = Path(local_dir or os.environ.get(SOURCE_DIR_ENV, "")) if (local_dir or os.environ.get(SOURCE_DIR_ENV)) else None
    today = today or dt.date.today().isoformat()
    SOURCES_DIR.mkdir(parents=True, exist_ok=True)
    rows = load_manifest()
    report = []
    for row in rows:
        if row["status"] != "VERIFIED":
            continue
        target = SOURCES_DIR / f"{row['document_id']}{_suffix(row['document_id'])}"
        how = "missing"
        if row["url"]:
            code, body = _download(row["url"])
            row["url_accessed"], row["http_status"] = today, code
            if body is not None and hashlib.sha256(body).hexdigest() == row["sha256"]:
                target.write_bytes(body)
                how = "downloaded"
            elif body is not None:
                how = "downloaded bytes differ"
        if how != "downloaded" and local_dir and LOCAL[row["document_id"]]["file"]:
            copy = local_dir / LOCAL[row["document_id"]]["file"]
            if copy.exists() and sha256_file(copy) == row["sha256"]:
                shutil.copyfile(copy, target)
                how = f"local copy ({how})" if how != "missing" else "local copy"
        if how.startswith(("missing", "downloaded bytes")) and target.exists() and sha256_file(target) == row["sha256"]:
            how = "already on disk"
        report.append({"document_id": row["document_id"], "http_status": row["http_status"], "result": how,
                       "url": row["url"], "target": f"kb/sources/{target.name}"})
    save_manifest(rows)
    return report


def verify(print_counts: bool = False) -> bool:
    """Check every fetched VERIFIED source against its sha256. Prints the four status counts."""
    rows = load_manifest()
    ok = True
    lines = []
    for row in verified_rows(rows):
        path = source_path(row)
        if path is None:
            lines.append(f"  not fetched  {row['document_id']} (runs on the committed cited clauses)")
        elif sha256_file(path) != row["sha256"]:
            ok = False
            lines.append(f"  MISMATCH     {row['document_id']}")
    for row in rows:
        for problem in url_problems(row):
            ok = False
            lines.append(f"  URL          {problem}")
    if print_counts:
        counts = Counter(r["status"] for r in rows)
        print("  ".join(f"{s} {counts.get(s, 0)}" for s in STATUSES))
        print("\n".join(lines) if lines else "  every fetched source matches its sha256")
    return ok


# --- chunking ---------------------------------------------------------------------------------------------

PAGE_MARK = re.compile(r"^\s*=+\s*page[-\s]*(\d+)\s*=*\s*$", re.IGNORECASE)
DECIMAL = re.compile(r"^\s*(\d{1,2}(?:\.\d{1,2}){1,3})\.?(?:\s+(.*))?$")
TOP = re.compile(r"^\s*(\d{1,2})\.?\s+([A-Z][A-Za-z].*)$")
ARTICLE = re.compile(
    r"^\s*Article\s*\(?\s*(\d{1,3})\s*(bis)?\s*\)?\s*(bis)?\s*(?:[-–:.]\s*(.*)|\s+([A-Z(].*)|$)", re.IGNORECASE
)
PARAGRAPH = re.compile(r"^\s*(\d{1,2})\s*[.\-)]\s+(\S.*)$")
ARABIC = re.compile(r"[؀-ۿ]")


def _is_arabic(line: str) -> bool:
    letters = [c for c in line if c.isalpha()]
    return bool(letters) and sum(1 for c in letters if ARABIC.match(c)) / len(letters) > 0.5


def page_lines(text: str) -> list[tuple[int, str]]:
    """Lines with their page numbers, minus page markers, bare page numbers, contents lines and
    running headers or footers (a line repeated on at least 30% of five or more pages)."""
    pages: list[tuple[int, list[str]]] = []
    current = (1, [])
    for line in text.splitlines():
        m = PAGE_MARK.match(line)
        if m:
            if current[1]:
                pages.append(current)
            current = (int(m.group(1)), [])
        else:
            current[1].append(line)
    if current[1]:
        pages.append(current)
    norm = lambda s: re.sub(r"\s+", " ", s).strip()
    seen = Counter()
    for _, lines in pages:
        seen.update({norm(l) for l in lines if norm(l) and len(norm(l)) < 120})
    running = {l for l, n in seen.items() if len(pages) >= 5 and n >= 0.3 * len(pages)}
    out = []
    for number, lines in pages:
        for line in lines:
            n = norm(line)
            if not n or n in running or n.isdigit() or "....." in n or re.fullmatch(r"[.\-–،:;]+", n):
                continue
            out.append((number, line))
    return out


def _next_ok(new: tuple[int, ...], cur: tuple[int, ...] | None, slack: int = 2) -> bool:
    """A clause number is a heading only if it is the next sibling or first child of the current one."""
    if cur is None:
        return new[0] <= slack and all(x == 1 for x in new[1:])
    if new <= cur:
        return False
    i = next((k for k in range(len(new)) if k >= len(cur) or new[k] != cur[k]), len(new))
    if i == len(new):
        return False
    base = cur[i] if i < len(cur) else 0
    return new[i] <= base + slack and all(x == 1 for x in new[i + 1:])


def split_decimal(text: str, keep: str = "en", top: bool = False, strip: str = "") -> list[dict[str, Any]]:
    """Clause headings are decimal numbers at line start (26.7.2). With top=True, a bare number before a
    capitalised title (7 High-level ...) is a heading too; strip removes a running footer glued to a line."""
    chunks: list[dict[str, Any]] = []
    cur: tuple[int, ...] | None = None
    for page, line in page_lines(text):
        if strip:
            line = re.sub(strip, "", line)
        if keep == "en" and _is_arabic(line):
            continue
        t = TOP.match(line) if top else None
        if t and _next_ok((int(t.group(1)),), cur):
            cur = (int(t.group(1)),)
            chunks.append({"clause": t.group(1), "article": t.group(1), "page": page, "lines": [t.group(2)]})
            continue
        m = DECIMAL.match(line)
        if m:
            number = tuple(int(x) for x in m.group(1).split("."))
            if _next_ok(number, cur):
                cur = number
                chunks.append({"clause": m.group(1), "article": str(number[0]), "page": page, "lines": [m.group(2) or ""]})
                continue
            if not m.group(2):
                continue  # a bare repeated number (the other column of a bilingual page)
        if chunks:
            chunks[-1]["lines"].append(line)
    return chunks


def split_articles(text: str, any_gap: bool = False) -> list[dict[str, Any]]:
    articles: list[dict[str, Any]] = []
    prev: tuple[int, int] | None = None
    for page, line in page_lines(text):
        m = ARTICLE.match(line)
        if m:
            n, bis = int(m.group(1)), bool(m.group(2) or m.group(3))
            key = (n, int(bis))
            if prev is None or (key > prev and (any_gap or n - prev[0] <= 3)):
                prev = key
                head = m.group(4) or m.group(5) or ""
                articles.append({"article": f"{n} bis" if bis else str(n), "page": page, "lines": [head], "pages": [page]})
                continue
        if articles:
            articles[-1]["lines"].append(line)
            articles[-1]["pages"].append(page)
    chunks = []
    for art in articles:
        paragraphs: list[dict[str, Any]] = []
        preamble: list[str] = []
        expected = 1
        for line, page in zip(art["lines"], art["pages"]):
            m = PARAGRAPH.match(line)
            if m and int(m.group(1)) == expected:
                paragraphs.append({"clause": f"{art['article']}({expected})", "article": art["article"], "page": page, "lines": [m.group(2)]})
                expected += 1
            elif paragraphs:
                paragraphs[-1]["lines"].append(line)
            else:
                preamble.append(line)
        if not paragraphs or any(l.strip() for l in preamble):
            chunks.append({"clause": art["article"], "article": art["article"], "page": art["page"], "lines": preamble or art["lines"]})
        chunks.extend(paragraphs)
    return chunks


def read_text(path: Path) -> str:
    """Text extractions are UTF-8, except one in Windows-1252 (the IMDA framework)."""
    data = path.read_bytes()
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return data.decode("cp1252")


def source_text(local_dir: Path, spec: dict[str, str]) -> str:
    """A source's text: its extraction file, or, where 'text' names the PDF itself, the PDF read with pypdf. TDRA
    Arabic text layers lose the lam-alef order under PyMuPDF (which made the hq .txt files); pypdf keeps it."""
    if spec["text"].endswith(".pdf"):
        import pypdf
        return "\n".join(page.extract_text() or "" for page in pypdf.PdfReader(local_dir / spec["text"]).pages)
    return read_text(local_dir / spec["text"])


def _join(lines: Iterable[str]) -> str:
    return re.sub(r"\s+", " ", " ".join(lines)).strip()


def read_extract(document_id: str) -> dict[str, Any]:
    """A labelled extract: '# key: value' header lines, then '<clause> <text>' per clause; a line that does not
    open with a clause number (a '-' item, a closing sentence) continues the clause above it."""
    header, clauses, clause = {}, {}, None
    for line in (EXTRACTS_DIR / f"{document_id}.txt").read_text(encoding="utf-8").splitlines():
        if line.startswith("#"):
            key, sep, value = line[1:].strip().partition(": ")
            if sep:
                header[key] = value
        elif re.match(r"\d+(\.\d+)+\s", line):
            clause, text = line.split(maxsplit=1)
            clauses[clause] = text.strip()
        elif line.strip() and clause:
            clauses[clause] = _join([clauses[clause], line])
    return {**header, "clauses": clauses}


def find_extract(document_id: str) -> dict[str, Any] | None:
    """The extract that holds a document's text: its own, or one paired to it ('# pair_of:') for its Arabic."""
    for path in sorted(EXTRACTS_DIR.glob("*.txt")):
        extract = read_extract(path.stem)
        if document_id in (path.stem, extract.get("pair_of")):
            return extract
    return None


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def build_chunks(local_dir: str | os.PathLike | None = None, cited: set[tuple[str, str]] | None = None) -> dict[str, int]:
    """Maintainer step: read each document's text extraction from the local folder (and each kb/extracts/ file)
    and write every clause to kb/chunks-full/, then the cited ones to kb/chunks/. An Arabic sibling (pair_of)
    fills text_ar of the same clause ids. Returns the cited count per document."""
    if cited is None:
        from onyx import data
        cited = data.cited_chunks()
    local_dir = Path(local_dir or os.environ[SOURCE_DIR_ENV])
    manifest = manifest_by_id()
    full: dict[str, list[dict[str, Any]]] = {}
    arabic: dict[str, dict[str, str]] = {}
    for path in sorted(EXTRACTS_DIR.glob("*.txt")):
        extract = read_extract(path.stem)
        if extract.get("pair_of"):  # checked Arabic for clauses of a document chunked from its text layer
            arabic.setdefault(extract["pair_of"], {}).update(extract["clauses"])
            continue
        row = manifest[path.stem]
        text_field = "text_ar" if row["language"] == "ar" else "text_en"
        full[path.stem] = [{
            "document_id": path.stem, "article": clause.split(".")[0], "clause": clause, "page": int(extract["page"]),
            "text_en": "", "text_ar": "", text_field: text,
            "status": row["status"], "retention_class": "", "node": "PP",
        } for clause, text in extract["clauses"].items()]
    for doc_id, spec in LOCAL.items():
        if spec["pair_of"] and spec["text"]:
            text = source_text(local_dir, spec)
            arabic.setdefault(spec["pair_of"], {}).update(
                {c["clause"]: _join(c["lines"]) for c in split_decimal(text, keep="all")})
    for doc_id, spec in LOCAL.items():
        if not spec["text"] or spec["pair_of"]:
            continue
        text = read_text(local_dir / spec["text"])
        row = manifest[doc_id]
        if spec["splitter"] == "decimal":
            raw = split_decimal(text, keep="en", top=spec["top"], strip=spec["strip"])
        else:
            raw = split_articles(text, any_gap=row["source_type"] == "extract")
        ar = arabic.get(doc_id, {})
        out, seen = [], set()
        for c in raw:
            if c["clause"] in seen:
                continue
            seen.add(c["clause"])
            out.append({
                "document_id": doc_id, "article": c["article"], "clause": c["clause"], "page": c["page"],
                "text_en": _join(c["lines"]), "text_ar": ar.get(c["clause"], ""),
                "status": row["status"], "retention_class": "", "node": "PP",
            })
        full[doc_id] = out
    for folder in (CHUNKS_FULL_DIR, CHUNKS_DIR):
        folder.mkdir(parents=True, exist_ok=True)
        for old in folder.glob("*.jsonl"):
            old.unlink()
    counts = {}
    for doc_id, chunks in full.items():
        _write_jsonl(CHUNKS_FULL_DIR / f"{doc_id}.jsonl", chunks)
        kept = [c for c in chunks if (doc_id, c["clause"]) in cited]
        if kept:
            _write_jsonl(CHUNKS_DIR / f"{doc_id}.jsonl", kept)
            counts[doc_id] = len(kept)
    return counts


def iter_chunks(document_id: str | None = None) -> Iterator[dict[str, Any]]:
    files = [CHUNKS_DIR / f"{document_id}.jsonl"] if document_id else sorted(CHUNKS_DIR.glob("*.jsonl"))
    for path in files:
        if path.exists():
            with path.open(encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        yield json.loads(line)


def has_chunks(document_id: str) -> bool:
    return any(True for _ in iter_chunks(document_id))


def get_chunk(document_id: str, clause: str) -> dict[str, Any]:
    for chunk in iter_chunks(document_id):
        if chunk["clause"] == clause:
            return chunk
    raise KeyError(f"{document_id} {clause}")


# --- ChromaDB ---------------------------------------------------------------------------------------------

class HashEmbedding:
    """Deterministic offline embedding for tests and selftest: hashed bag of words, 256 dimensions."""

    def __init__(self, dimensions: int = 256) -> None:
        self.dimensions = dimensions

    def __call__(self, input: list[str]) -> list[list[float]]:
        vectors = []
        for text in input:
            v = [0.0] * self.dimensions
            for word in re.findall(r"\w+", text.lower()):
                v[int(hashlib.md5(word.encode()).hexdigest(), 16) % self.dimensions] += 1.0
            norm = math.sqrt(sum(x * x for x in v)) or 1.0
            vectors.append([x / norm for x in v])
        return vectors

    @staticmethod
    def name() -> str:
        return "onyx-hash"

    def get_config(self) -> dict[str, Any]:
        return {"dimensions": self.dimensions}

    @staticmethod
    def build_from_config(config: dict[str, Any]) -> "HashEmbedding":
        return HashEmbedding(config.get("dimensions", 256))

    def is_legacy(self) -> bool:
        return False

    def embed_query(self, input: list[str]) -> list[list[float]]:
        return self(input)

    def default_space(self) -> str:
        return "cosine"

    def supported_spaces(self) -> list[str]:
        return ["cosine"]


def _framework_documents() -> list[tuple[str, str, dict[str, str]]]:
    path = SOURCES_DIR / "itu-readiness-dimensions.json"
    local = os.environ.get(SOURCE_DIR_ENV)
    if not path.exists() and local:
        path = Path(local) / LOCAL["itu-readiness-dimensions"]["file"]
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    docs = []
    for factor in data.get("factors", []):
        docs.append((f"factor:{factor['id']}", f"{factor['name']}: {factor.get('description', '')}", {"kind": "factor"}))
    for dim in data.get("dimensions", []):
        text = json.dumps(dim, ensure_ascii=False)
        docs.append((f"dimension:{dim.get('id')}", text, {"kind": "dimension", "name": str(dim.get("name", ""))}))
    return docs


def ingest(path: str | os.PathLike | None = None, embedding_function: Any = None):
    """Load the clause chunks into kb_main, the Readiness factors and dimensions into kb_framework, and
    create an empty kb_decisions. Cosine space; one document per clause, so a hit is a citation."""
    import chromadb

    client = chromadb.PersistentClient(path=str(path or CHROMA_DIR))
    manifest = manifest_by_id()
    kwargs = {"metadata": {"hnsw:space": "cosine"}}
    if embedding_function is not None:
        kwargs["embedding_function"] = embedding_function
    for name in COLLECTIONS:
        try:
            client.delete_collection(name)
        except Exception:
            pass
    main, framework, _ = (client.create_collection(name, **kwargs) for name in COLLECTIONS)
    chunks = list(iter_chunks())
    for start in range(0, len(chunks), 200):
        batch = chunks[start:start + 200]
        main.add(
            ids=[f"{c['document_id']}:{c['clause']}" for c in batch],
            documents=[(c["text_en"] + "\n" + c["text_ar"]).strip() for c in batch],
            metadatas=[{
                "document_id": c["document_id"], "article": c["article"], "clause": c["clause"], "page": c["page"],
                "status": c["status"], "node": c["node"], "has_ar": bool(c["text_ar"]),
                "binding_status": manifest[c["document_id"]]["binding_status"],
                "jurisdiction": manifest[c["document_id"]]["jurisdiction"],
            } for c in batch],
        )
    docs = _framework_documents()
    if docs:
        framework.add(ids=[d[0] for d in docs], documents=[d[1] for d in docs], metadatas=[d[2] for d in docs])
    return client


# --- export -----------------------------------------------------------------------------------------------

def _category(row: dict[str, str]) -> str:
    if row["status"] == "UNVERIFIED":
        return "Unverified"
    if row["jurisdiction"] == "UAE":
        return "UAE_Binding" if row["binding_status"] == "binding" else "UAE_Advisory"
    return "Framework" if row["binding_status"] == "method" else "Global_Examples"


def export(out_dir: str | os.PathLike | None = None) -> Path:
    """Write the ITU InputDocs layout: Inputs.md (the reference repo's manifest style plus sha256 and link)
    and, for each fetched source, a copy under its category folder."""
    root = Path(out_dir or KB_DIR / "export") / "InputDocs"
    root.mkdir(parents=True, exist_ok=True)
    rows = load_manifest()
    lines = [
        "# Input Documents Manifest", "",
        "Mizan knowledge base, exported from `kb/manifest.csv` by `python -m onyx kb export`.",
        "Each document sits in the subfolder of its category; full texts are copied only where `kb fetch` holds them.", "",
    ]
    for category in ("UAE_Binding", "UAE_Advisory", "Framework", "Global_Examples", "Unverified"):
        members = [r for r in rows if _category(r) == category]
        lines += ["", f"## {category}/ ({len(members)} files)", "",
                  "| # | Filename | Type | Description | Status | sha256 | Link |", "|---|---|---|---|---|---|---|"]
        for i, r in enumerate(members, 1):
            name = f"{r['document_id']}{_suffix(r['document_id'])}" if r["sha256"] else ""
            src = source_path(r) if r["sha256"] else None
            if src:
                (root / category).mkdir(exist_ok=True)
                shutil.copyfile(src, root / category / name)
            link = f"[link]({r['url']})" if r["url"] else "not recorded"
            sha = f"`{r['sha256'][:12]}…`" if r["sha256"] else ""
            lines.append(f"| {i} | `{name or r['document_id']}` | `{r['source_type']}` | {r['title']} | {r['status']} | {sha} | {link} |")
    lines += ["", "sha256 values in full: `kb/manifest.csv`."]
    out = root / "Inputs.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    return out


# --- CLI --------------------------------------------------------------------------------------------------

def _cli(args) -> int:
    if args.action == "fetch":
        for r in fetch(args.local):
            print(f"{r['http_status'] or '-':>5}  {r['result']:<32} {r['document_id']}")
            if r["result"].startswith(("missing", "downloaded bytes")):
                # Iyas, 2026-10-20: a blocked host gets a hand download; the demo runs on the committed clauses.
                print(f"       download by hand: open {r['url'] or '(no URL recorded)'} and save the file as {r['target']}")
        return 0
    if args.action == "verify":
        return 0 if verify(print_counts=True) else 1
    if args.action == "chunk":
        counts = build_chunks(args.local)
        for doc, n in counts.items():
            print(f"{n:>5}  {doc}")
        print(f"{sum(counts.values()):>5}  cited clauses in {len(counts)} documents (every clause: kb/chunks-full/)")
        return 0
    if args.action == "ingest":
        client = ingest()
        for name in COLLECTIONS:
            print(f"{client.get_collection(name).count():>5}  {name}")
        return 0
    if args.action == "export":
        print(export())
        return 0
    return 2


def register(subparsers) -> None:
    parser = subparsers.add_parser("kb", help="knowledge base: fetch, verify, chunk, ingest, export")
    parser.add_argument("action", choices=["fetch", "verify", "chunk", "ingest", "export"])
    parser.add_argument("--local", help=f"folder holding the maintainer's copies (default: ${SOURCE_DIR_ENV})")
    parser.set_defaults(func=_cli)
