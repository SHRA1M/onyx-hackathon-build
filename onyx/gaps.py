"""The gap register (order Task 9 and 2026-10-21-task-9-gaps). onyx/data/gaps.json is the single source;
`python -m onyx gaps` writes docs/gaps.md and the register table at the top of the README from it, byte-identical
on every run. The clause texts come from the committed chunks (kb/chunks/), English and, where the chunk has it,
Arabic; the global quotes are checked against kb/sources/global/ by tests/test_gaps.py."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from onyx import data, kb

GAPS_MD = kb.REPO / "docs" / "gaps.md"
README = kb.REPO / "README.md"
START, END = "<!-- gap-register:start -->", "<!-- gap-register:end -->"

KINDS = ("method", "scope", "absence", "currency")  # addendum item 19 (Sabeeh)
CATEGORIES = ("unclear responsibilities", "standards gap", "technology gap", "legislative gap",
              "coordination problem", "conflict between objectives")  # addendum item 10, the UAE page's list
ADDRESSEES = ("TDRA", "UAE Data Office", "the consumer-protection authority", "Cabinet", "ITU")
COMPETITOR = ("yes", "no", "not read")
# short names for the table, by the file a global example quotes
SHORT = {"imda-": "IMDA", "eu-ai-act-": "EU AI Act", "gdpr-": "GDPR", "eidas-": "eIDAS", "itu-t-y3172": "Y.3172",
         "coppa-": "16 CFR", "canada-ola-": "Canada OLA", "eu-ecommerce-": "E-Commerce Dir. 2000/31",
         "eu-crd-": "CRD 2011/83", "eu-dsa-": "DSA 2022/2065", "us-47cfr-": "47 CFR",
         "es-ley-10-2025": "Spain Ley 10/2025", "wales-wls-": "Wales WLS", "us-tsr-": "US TSR 16 CFR",  # Task 30
         "sg-eta-": "Singapore ETA", "us-utah-": "Utah Code", "ca-bccrt-": "Moffatt v. Air Canada 2024 BCCRT 149",
         "eu-roaming-": "EU Roaming Reg 2022/612",  # Task 31
         "3gpp-ts-28-535": "3GPP TS 28.535", "etsi-gs-zsm-009-1": "ETSI ZSM 009-1",
         "eu-eecc-": "EECC 2018/1972", "de-tkg-": "TKG 2021",  # Task 33
         "itu-t-y3173": "SAE J3016 (Y.3173 Table I.1)"}  # gap-12 quotes SAE as Y.3173 reproduces it (Task 27)


def _short(path: str) -> str:
    name = Path(path).name
    return next(label for prefix, label in SHORT.items() if name.startswith(prefix))


# a global example file whose name is not a manifest id: the manifest instrument it extracts (Task 31 Part D)
INSTRUMENT = {"gdpr-": "gdpr", "canada-ola-": "ca-ola", "imda-": "imda-mgf-agentic", "itu-t-y3173": "itu-t-y3173"}


def _binding(path: str) -> bool:
    """True when the example's document is binding in the manifest: by document id, else by instrument."""
    rows = kb.load_manifest()
    stem = Path(path).stem
    row = next((r for r in rows if r["document_id"] == stem), None)
    if row:
        return row["binding_status"] == "binding"
    instrument = next((i for prefix, i in INSTRUMENT.items() if stem.startswith(prefix)), None)
    return any(r["instrument"] == instrument and r["binding_status"] == "binding" for r in rows)


def elsewhere(gap_id: str) -> dict[str, Any]:
    """A flagged gap for the replay pages (order Task 31 Part D): its line and one example from elsewhere: the one
    marked `"elsewhere": true` (the report's cell), else the first whose document is binding in the manifest, else
    the first (Iyas, 2026-10-30). label "" with no example (gap-8);
    label None for a candidate, which shows its line only. None for an id the register does not hold."""
    row = next((r for r in data.load_gaps()["gaps"] if r["id"] == gap_id), None)
    if row is None:
        return None
    if gap_id.startswith("candidate-"):
        return {"id": gap_id, "line": row["line"], "label": None, "quote": None}
    examples = row["global_examples"]
    if not examples:
        return {"id": gap_id, "line": row["line"], "label": "", "quote": ""}
    ex = next((e for e in examples if e.get("elsewhere")), None) or next(
        (e for e in examples if _binding(e["file"])), examples[0])
    return {"id": gap_id, "line": row["line"], "label": f"{_short(ex['file'])} {ex['clause']}", "quote": ex["quote"]}


NONE_FOUND = "Elsewhere: none found; this recommendation is the example."


def _cell(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ")


def _examples(row: dict[str, Any]) -> str:
    if not row["global_examples"]:
        return row["global_none"]
    seen: list[str] = []
    for ex in row["global_examples"]:
        label = f"{_short(ex['file'])} {ex['clause']}"
        if label not in seen:
            seen.append(label)
    return "; ".join(seen)


def table() -> str:
    """The register as one Markdown table: the README's first section and the top of docs/gaps.md."""
    # the competitor fields stay in gaps.json as hq's internal note, out of the public register (order
    # 2026-10-21-task-9-fixes-tasks-10-11 item 2)
    lines = ["| id | gap | kind | category | addressee | global example | exposed by |",
             "| --- | --- | --- | --- | --- | --- | --- |"]
    for row in data.load_gaps()["gaps"]:
        lines.append("| " + " | ".join(_cell(c) for c in (
            row["id"], row["gap"], row["kind"], row["category"], ", ".join(row["addressee"]), _examples(row),
            row["exposed_by"])) + " |")
    return "\n".join(lines) + "\n"


def _searched(s: dict[str, Any]) -> list[str]:
    if s.get("file"):  # quoted from the stored source, no chunk (Task 32: operator codes, 106/2026)
        page = f"p. {s['page']}, " if s.get("page") else ""  # a web page's text has none (106/2026 English)
        lang = "AR" if kb._is_arabic(s["quote"]) else "EN"  # an Arabic original's own text (Task 33, 52/2024)
        return [f"- `{s['clause']}` ({page}`{s['file']}`): {s['says']}", f"  - {lang}: \"{s['quote']}\""]
    document_id, clause = s["clause"].split(":", 1)
    chunk = kb.get_chunk(document_id, clause)
    # "p.": the PDF page index (order Task 16 item 1); a row's own page, read from the text on disk, where the chunk's is wrong (every Y.3172 chunk says page 1)
    out = [f"- `{s['clause']}` (p. {s.get('page', chunk['page'])}): {s['says']}"]
    if s.get("quote"):
        out.append(f"  - EN: \"{s['quote']}\"")
    elif chunk["text_en"]:
        out.append(f"  - EN: \"{chunk['text_en']}\"")
    if chunk["text_ar"]:
        out.append(f"  - AR (the whole chunk): \"{chunk['text_ar']}\"")
    # the chunk has no Arabic: the phrase from the Arabic source text (order 2026-10-22 Task 15, gap-9 11(1))
    if s.get("quote_ar"):
        out.append(f"  - AR (`{s['file_ar']}`): \"{s['quote_ar']}\"")
    return out


def _quotes(title: str, examples: list[dict[str, Any]]) -> list[str]:
    out = [f"**{title}**", ""]
    for ex in examples:
        says = f"{ex['says']} " if ex.get("says") else ""  # a caveat printed beside the quote (Task 31, AI Act)
        out.append(f"- {ex['document']}, {ex['clause']} ({ex['status']}, `{ex['file']}`): {says}\"{ex['quote']}\"")
    return out + [""]


def render() -> str:
    register = data.load_gaps()
    lines = ["# Gap register", "",
             "Generated by `python -m onyx gaps` from `onyx/data/gaps.json`; do not edit by hand. Operator, subscribers "
             "and scenarios are synthetic; the law texts are real.", "",
             "A gap is claimed only where no clause in any VERIFIED or REFERENCED document reaches the concern; a "
             "clause that exists but gives no method is a method gap (addendum item 19). Every row lists the clauses "
             "searched and what each says, English and, where the chunk holds it, Arabic.", "",
             table()]
    for row in register["gaps"]:
        lines += [f"## {row['id']}: {row['line']}", "",
                  f"{row['gap']}", "",
                  f"Kind: {row['kind']}. Category: {row['category']}. Addressee: {', '.join(row['addressee'])}. "
                  f"Exposed by: {row['exposed_by']}.", ""]
        if row.get("note"):  # a row's own sentence under its heading (order 2026-10-26 Task 27, B4)
            lines += [row["note"], ""]
        lines += ["**Clauses searched**", ""]
        for s in row["searched"]:
            lines += _searched(s)
        # a framework row is no clause of law: listed with the searched clauses, marked non-binding (order Task 20)
        for fw in row.get("framework", []):
            lines += [f"- {fw['document']}, {fw['clause']} (p. {fw['page']}; framework, non-binding): {fw['says']}",
                      f"  - EN (`{fw['file']}`): \"{fw['quote']}\""]
        lines += ["", f"**UAE position.** {row['uae_position']}", ""]
        if row.get("standard_text"):
            lines += _quotes("The standard's own text", row["standard_text"])
        if row["global_examples"]:
            lines += _quotes("Global example", row["global_examples"])
            if row.get("examples_note"):  # the prose line after the examples (Task 33, gap-8)
                lines += [row["examples_note"], ""]
        else:
            lines += [f"**Global example.** {row['global_none']}", ""]
        lines += [f"**Recommendation.** {row['recommendation']}", ""]
    lines += ["## Candidates", "", "Flagged as candidates; no global example required.", ""]
    for cand in register["candidates"]:
        lines += [f"### {cand['name']}", "", cand["line"], ""]
        for s in cand["searched"]:
            lines += _searched(s)
        lines.append("")
    lines += ["## Sources", "", f"{register['source']}.", ""]
    return "\n".join(lines)


def write(out: str | Path = GAPS_MD, readme: str | Path | None = README) -> None:
    Path(out).write_text(render(), encoding="utf-8", newline="\n")
    if readme is None:
        return
    text = Path(readme).read_text(encoding="utf-8")
    head, rest = text.split(START, 1)
    _, tail = rest.split(END, 1)
    Path(readme).write_text(f"{head}{START}\n{table()}{END}{tail}", encoding="utf-8", newline="\n")


def _cli(args) -> int:
    write()
    register = data.load_gaps()
    print(f"{len(register['gaps'])} rows and {len(register['candidates'])} candidates: {GAPS_MD.relative_to(kb.REPO)} "
          f"and the README register table")
    return 0


def register(subparsers) -> None:
    parser = subparsers.add_parser("gaps", help="write docs/gaps.md and the README register table from gaps.json")
    parser.set_defaults(func=_cli)
