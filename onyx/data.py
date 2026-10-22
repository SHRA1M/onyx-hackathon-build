"""Mandates, rule table and answer keys, and `check-data`: every quote the gates rely on is verbatim in the KB."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from onyx import kb

DATA_DIR = Path(__file__).resolve().parent / "data"
KEYS_DIR = DATA_DIR / "keys"
MIN_QUOTE = 20  # Task 6: a quote of 20+ characters


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def load_rules() -> list[dict[str, Any]]:
    return json.loads((DATA_DIR / "rules.json").read_text(encoding="utf-8"))["rules"]


def load_mandates() -> dict[str, Any]:
    return json.loads((DATA_DIR / "mandates.json").read_text(encoding="utf-8"))["agents"]


def load_gaps() -> dict[str, Any]:
    """The gap register ids and one-liners the adviser names in args.gap (gaps.json, from the keys' gap_ids)."""
    return json.loads((DATA_DIR / "gaps.json").read_text(encoding="utf-8"))


def cited_chunks() -> set[tuple[str, str]]:
    """(document_id, chunk) for every chunk a rule, a mandate verb or a gap row (searched clauses, Task 9) cites:
    what kb/chunks/ holds."""
    cited = {(rule["document_id"], rule["chunk"]) for rule in load_rules()}
    for spec in load_mandates().values():
        for verb in spec["verbs"]:
            cited |= {(ref["document_id"], ref["chunk"]) for ref in verb["clause_ids"]}
    register = load_gaps()
    for row in register["gaps"] + register.get("candidates", []):
        cited |= {tuple(s["clause"].split(":", 1)) for s in row.get("searched", [])}
    return cited


def _chunk(document_id: str, clause: str) -> dict[str, Any] | None:
    try:
        return kb.get_chunk(document_id, clause)
    except KeyError:
        return None


def check_rules() -> list[str]:
    manifest = kb.manifest_by_id()
    problems, seen = [], set()
    for rule in load_rules():
        rid = rule["id"]
        if rid in seen:
            problems.append(f"{rid}: duplicate id")
        seen.add(rid)
        if not rule.get("clause"):
            problems.append(f"{rid}: no clause id")
        row = manifest.get(rule["document_id"])
        if row is None:
            problems.append(f"{rid}: document {rule['document_id']} not in the manifest")
            continue
        if (rule["binding_status"], rule["jurisdiction"]) != (row["binding_status"], row["jurisdiction"]):
            problems.append(f"{rid}: binding_status or jurisdiction differs from the manifest")
        chunk = _chunk(rule["document_id"], rule["chunk"])
        if chunk is None:
            problems.append(f"{rid}: no chunk {rule['document_id']} {rule['chunk']}")
            continue
        if chunk["status"] != "VERIFIED":
            problems.append(f"{rid}: chunk status {chunk['status']}")
        if len(rule["quote"]) < MIN_QUOTE:
            problems.append(f"{rid}: quote shorter than {MIN_QUOTE} characters")
        text = chunk["text_ar"] if row["language"] == "ar" else chunk["text_en"]  # an Arabic-only document
        if normalize(rule["quote"]) not in normalize(text):
            problems.append(f"{rid}: quote not verbatim in {rule['document_id']} {rule['chunk']}")
        if rule.get("quote_ar") and normalize(rule["quote_ar"]) not in normalize(chunk["text_ar"]):
            problems.append(f"{rid}: Arabic quote not verbatim in {rule['document_id']} {rule['chunk']}")
        problems += _check_transcription(rule)
    return problems


def _check_transcription(rule: dict[str, Any]) -> list[str]:
    """Iyas, 2026-10-21: a quote from page images or scanned text is valid only if hq holds a '-checked.txt' for it,
    and the KB text it is matched against must be that file, not one made from the same note as the quote."""
    checked = rule.get("transcription", {}).get("checked_file")
    if not checked:
        return []
    if not checked.endswith("-checked.txt"):
        return [f"{rule['id']}: checked file {checked} is not an hq '-checked.txt'"]
    extract = kb.find_extract(rule["document_id"])
    if extract is None or not extract.get("checked", "").startswith(checked):
        return [f"{rule['id']}: the KB text for {rule['document_id']} is not from its checked file {checked}"]
    return []


# Iyas, 2026-10-21: TDRA text layers write the lam-alef ligature reversed (alef before lam). A detector, not a fix:
# a real 'لا' is common, so only shapes correct Arabic never has (a lone 'ال' is 'لا'), plus broken words seen in
# the CPR.
REVERSED_LAM_ALEF = re.compile(r"اا|ا[أإآ]ل|(?<![؀-ۿ])ال(?![؀-ۿ])")
REVERSED_LAM_ALEF_WORDS = {"خالل", "عالقات", "وكالء", "الالزمة", "استالم", "سجالت", "مالئم", "إصالح", "اطالع",
                           "إطالقاً", "فضالً"}


def ligature_problems() -> list[str]:
    """Every committed chunk whose Arabic shows a reversed lam-alef."""
    problems = []
    for chunk in kb.iter_chunks():
        words = set(re.findall(r"[؀-ۿ]+", chunk["text_ar"]))
        bad = sorted(set(REVERSED_LAM_ALEF.findall(chunk["text_ar"])) | (words & REVERSED_LAM_ALEF_WORDS))
        if bad:
            problems.append(f"{chunk['document_id']} {chunk['clause']}: reversed lam-alef in Arabic ({', '.join(bad)})")
    return problems


def transcribed_rules() -> list[dict[str, Any]]:
    """Rules whose quote (or the Arabic in a field) was read from page images or scanned text."""
    return [rule for rule in load_rules() if rule.get("transcription")]


def pending_rules() -> list[dict[str, Any]]:
    """Transcribed rules with no hq checked file yet: their transcribed text is not verified."""
    return [rule for rule in transcribed_rules() if not rule["transcription"]["checked_file"]]


def check_mandates() -> list[str]:
    problems = []
    for agent, spec in load_mandates().items():
        for verb in spec["verbs"]:
            name = f"{agent}.{verb['verb']}"
            if not verb["clause_ids"]:
                problems.append(f"{name}: no clause")
                continue
            texts = []
            for ref in verb["clause_ids"]:
                chunk = _chunk(ref["document_id"], ref["chunk"])
                if chunk is None:
                    problems.append(f"{name}: no chunk {ref['document_id']} {ref['chunk']}")
                else:
                    texts.append(normalize(chunk["text_en"]))
            if len(verb["quote"]) < MIN_QUOTE or not any(normalize(verb["quote"]) in t for t in texts):
                problems.append(f"{name}: quote not verbatim in its clauses")
    return problems


def check_data() -> int:
    """Addendum item 2: fail on a listing-page URL, on a quote that is not the document's text, on a rule
    without a clause id. Rows with no recorded URL are listed, not failed."""
    from onyx import cost

    rows = kb.load_manifest()
    failures = [p for r in rows for p in kb.url_problems(r)] + check_rules() + check_mandates() + ligature_problems()
    failures += cost.check_prices()
    no_url = [r["document_id"] for r in rows if not r["url"] and r["status"] != "UNVERIFIED"]
    rules, mandates = load_rules(), load_mandates()
    print(f"rules {len(rules)}  mandate verbs {sum(len(s['verbs']) for s in mandates.values())}  "
          f"manifest rows {len(rows)}  model prices {len(cost.load_prices()['models'])}")
    if no_url:
        print(f"no URL recorded ({len(no_url)}): {', '.join(no_url)}")
    print("transcribed from page images or scanned text:")
    for rule in transcribed_rules():
        t = rule["transcription"]
        print(f"  {rule['id']} ({t['field']}, {t['from']}): {t['checked_file'] or 'PENDING, no hq checked file'}")
    print("\n".join(failures) if failures else "check-data ok: every quote verbatim, every rule cites a clause")
    return 1 if failures else 0


def register(subparsers) -> None:
    parser = subparsers.add_parser("check-data", help="prove every rule and mandate quote is verbatim in the KB")
    parser.set_defaults(func=lambda args: check_data())


SCENARIOS_DIR = DATA_DIR / "scenarios"


def load_scenario(scenario_id: str) -> dict[str, Any]:
    return json.loads((SCENARIOS_DIR / f"{scenario_id}.json").read_text(encoding="utf-8"))


def load_key(scenario_id: str) -> dict[str, Any]:
    """A frozen answer key (order Task 3): never edited once HASHES.txt is committed."""
    return json.loads((KEYS_DIR / f"{scenario_id}.json").read_text(encoding="utf-8"))
