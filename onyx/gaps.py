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
ADDRESSEES = ("TDRA", "UAE Data Office", "the consumer-protection authority", "Cabinet", "ITU",
              "Council of Ministers")  # Task 41: PDPL Art 28's own name for the body that issues its Regulations


def addressee_ok(name: str) -> bool:
    """An addressee is one of ADDRESSEES, optionally with a parenthesised role (Task 41: 'UAE Data Office (proposer)')."""
    return name.split(" (", 1)[0] in ADDRESSEES


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
         "qatar-cra-ccpr-": "Qatar CCPR 2024", "saudi-cst-": "Saudi CST 552/1445",
         "qatar-decree-law-16-": "Qatar 16/2010",  # Task 35
         "maine-": "Maine", "california-bpc-": "California BPC", "california-hsc-": "California HSC",
         "india-trai-": "India TRAI TCCRR 2012",  # Task 35b
         "itu-t-y3173":"SAE J3016 (Y.3173 Table I.1)",  # gap-12 quotes SAE as Y.3173 reproduces it (Task 27)
         "uk-ofcom-": "Ofcom Penalty Guidelines 2017",  # Task 41, gap-15
         # Task 43: a free-zone text is a UAE free-zone example, never a federal rule (order limits)
         "difc-dp-regulations-": "DIFC DP Regulations (UAE free zone, not federal)",
         "difc-dp-law-": "DIFC DP Law 5/2020 (UAE free zone, not federal)",
         "adgm-dpr-": "ADGM DPR 2021 (UAE free zone, not federal)", "itu-t-f748-67": "ITU-T F.748.67"}
# the Gulf telecom consumer regulations read (order 2026-10-30 Task 35, Addendum A): the register's preamble and the README
GULF_LINE = ("The three GCC telecom consumer regulations read (Saudi 2024, Qatar 2024, Kuwait 2022) name no AI channel, "
             "hand-over clock, machine disclosure or Arabic quality measure either; Saudi 552/1445 comes nearest, "
             "requiring a route to an employee and a qualified employee on every complaint.")
# the bot-disclosure statutes read (order 2026-10-30 Task 35b, Addendum B item 2): the register's preamble
COMPANION_LINE = "The 2025 to 2026 US statutes on chatbots regulate companions and carve out customer service."
# the free zones and the AI and Data Authority (order 2026-11-02 Task 43 item 2; hq answers to stop 1, 2 and 3): the
# register's preamble, the site and the README, after the GCC paragraph
FREE_ZONE_LINE = ("Two UAE free zones have their own data protection law: DIFC Law 5/2020 binds Controllers and Processors "
                  "'incorporated in the DIFC, regardless of whether the Processing takes place in the DIFC or not' "
                  "(Art 6(3)(a)), and the ADGM Data Protection Regulations 2021 apply 'in the context of the activities of "
                  "an Establishment of a Controller or a Processor in ADGM' (s. 3(1)). A federal telecom licensee outside "
                  "the zones is not within either. Where a free-zone text fills a federal gap, the row names it as a UAE "
                  "free-zone example, never as a federal rule.")
AUTHORITY_LINE = ("The PDPL names the UAE Data Office (Art 24). On 2026-06-14 the Prime Minister approved an Artificial "
                  "Intelligence and Data Authority, reporting to the Cabinet, that 'will bring together under one mandate "
                  "the functions previously held by three separate entities', the Data Office among them (WAM, 14 June "
                  "2026, `https://www.wam.ae/en/article/c0pz7ku-mohammed-bin-rashid-approves-establishing`; manifest rows "
                  "`wam-2026-06-14-ai-data-authority` and, in Arabic, `fed-ai-data-authority-2026-06-14`). No establishing "
                  "instrument was found on the official portal on 2026-11-02, and dataoffice.gov.ae did not resolve on 2026-11-02. "
                  "The register keeps the PDPL's name.")
# the Gazette (order 2026-11-02 Task 44 method note; addendum 2026-11-03 D2, "unreachable" outcome): preamble, site, README
GAZETTE_LINE = ("The federal Official Gazette (Ministry of Justice, elaws.moj.gov.ae) was unreachable on 2026-11-02, "
                "2026-11-03 and 2026-11-04 (curl and Chrome from hq, GitHub answering as the control), so its issues were "
                "not swept; the legislation portal, which lists each law's Gazette number and its regulations, is the "
                "official check, and it publishes no issue archive; the newest issue the portal names is No. 833 of "
                "14 October 2026 (entry 4660, read 2026-11-04).")


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
    if s.get("url"):  # a text with no KB row, cited by its URL (Task 35b: Korea, the TRAI draft)
        page = f"p. {s['page']}, " if s.get("page") else ""
        return [f"- `{s['clause']}` ({page}{s['url']}): {s['says']}", f"  - EN: \"{s['quote']}\""]
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
        page = f"p. {s['page_ar']}, " if s.get("page_ar") else ""  # the Arabic PDF's page (Task 41, PDPL)
        out.append(f"  - AR ({page}`{s['file_ar']}`): \"{s['quote_ar']}\"")
    return out


def _quotes(title: str, examples: list[dict[str, Any]]) -> list[str]:
    out = [f"**{title}**", ""]
    for ex in examples:
        says = f"{ex['says']} " if ex.get("says") else ""  # a caveat printed beside the quote (Task 31, AI Act)
        page = f"p. {ex['page']}, " if ex.get("page") else ""  # the PDF page, where the source is a PDF (Task 35)
        lang = "AR: " if kb._is_arabic(ex["quote"]) else ""  # an Arabic original's own text (Task 35, Qatar 16/2010)
        out.append(f"- {ex['document']}, {ex['clause']} ({ex['status']}, {page}`{ex['file']}`): {says}{lang}\"{ex['quote']}\"")
        if ex.get("quote_ar"):  # the Arabic beside the English, from the page image (Task 35, Saudi 552/1445)
            out.append(f"  - AR (p. {ex['page_ar']}, `{ex['file_ar']}`): \"{ex['quote_ar']}\"")
    return out + [""]


def render() -> str:
    register = data.load_gaps()
    lines = ["# Gap register", "",
             "Generated by `python -m onyx gaps` from `onyx/data/gaps.json`; do not edit by hand. Operator, subscribers "
             "and scenarios are synthetic; the law texts are real.", "",
             "A gap is claimed only where no clause in any VERIFIED or REFERENCED document reaches the concern; a "
             "clause that exists but gives no method is a method gap (addendum item 19). Every row lists the clauses "
             "searched and what each says, English and, where the chunk holds it, Arabic.", "", GULF_LINE, "",
             FREE_ZONE_LINE, "", AUTHORITY_LINE, "", GAZETTE_LINE, "", COMPANION_LINE, "", table()]
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
    # a text read in full where nothing was found: not a candidate (hq ruling 2026-11-02, Task 41)
    lines += ["## Searched, nothing found", ""]
    for item in register["nothing_found"]:
        lines += [f"### {item['name']}", "", item["line"], ""]
        for s in item["searched"]:
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


def ids() -> tuple[list[str], list[str]]:
    """The register's gap ids and candidate ids: the candidate rows the adviser lists, then the prose candidates."""
    register = data.load_gaps()
    rows = [r["id"] for r in register["gaps"]]
    return ([i for i in rows if i.startswith("gap-")],
            [i for i in rows if i.startswith("candidate-")] + [c["id"] for c in register["candidates"]])


def _cli(args) -> int:
    write()
    gap_ids, candidate_ids = ids()
    print(f"{len(gap_ids)} gaps: {', '.join(gap_ids)}")
    print(f"{len(candidate_ids)} candidates: {', '.join(candidate_ids)}")
    print(f"written: {GAPS_MD.relative_to(kb.REPO).as_posix()} and the README register table")
    return 0


def register(subparsers) -> None:
    parser = subparsers.add_parser("gaps", help="write docs/gaps.md and the README register table from gaps.json")
    parser.set_defaults(func=_cli)
