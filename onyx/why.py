"""Why a step was decided (order 2026-11-01-task-36-template-items item 2).

`python -m onyx why <log> --step <n> [--lang ar]` reads a committed run log and prints, for every decision the log
records at that step: the verdict, each clause relied on with its document title, page and verbatim words from
kb/chunks/ (the source the gate read), the human it hands to, and the event's hash. The explanation is the log, not
a second opinion: no model, no prompt, no tool, no gate call. A broken hash chain is never explained.

The Arabic labels are the team's translation, not eye-checked. A clause whose committed chunk holds no Arabic text
prints its English words after the line `NO_AR`."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from onyx import audit, data, kb, runs
from onyx.html_kit import tag

NO_AR = "لا يحمل المقطع المعتمد نصاً عربياً لهذا البند؛ النص الإنجليزي:"  # the chunk has no Arabic; the English text:

LABELS = {
    "en": {"step": "step", "verdict": "verdict", "clause": "clause", "handover": "hand-over", "humans": "on shift",
           "hash": "event hash", "override": "override_refused", "by": "by", "stands": "the verdict stands",
           "note": "From the committed log only; no model call. Operator, subscribers and numbers are synthetic.",
           "allow": "allow", "hold": "hold", "block": "block", "insufficient_evidence": "insufficient evidence"},
    "ar": {"step": "الخطوة", "verdict": "القرار", "clause": "البند", "handover": "تسليم إلى إنسان",
           "humans": "المناوبون", "hash": "بصمة الحدث", "override": "override_refused", "by": "من",
           "stands": "القرار قائم", "note": "من السجل المعتمد فقط؛ دون استدعاء نموذج. المشغّل والمشتركون والأرقام "
                                            "اصطناعية. (العناوين ترجمة الفريق، لم تُراجع بالعين)",
           "allow": "سماح", "hold": "تعليق", "block": "منع", "insufficient_evidence": "أدلة غير كافية"},
}


def _verdict(verdict: str, lang: str) -> str:
    words = LABELS[lang].get(verdict, verdict)
    return verdict if lang == "en" or words == verdict else f"{verdict} / {words}"


def _quote(rule: dict[str, Any], lang: str) -> list[str]:
    """The clause's words in `lang`, from its committed chunk; the rule's quote when the chunk carries it."""
    try:
        chunk = kb.get_chunk(rule["document_id"], rule["chunk"])
    except KeyError:
        chunk = {"text_en": rule["quote"], "text_ar": rule.get("quote_ar", "")}
    if lang == "ar":
        text, quote = chunk.get("text_ar", ""), rule.get("quote_ar", "")
        if not text:
            return [f"    {NO_AR}", f'    "{_from(chunk["text_en"], rule["quote"])}"']
        return [f'    "{_from(text, quote)}"']
    return [f'    "{_from(chunk["text_en"], rule["quote"])}"']


def _from(text: str, quote: str) -> str:
    return quote if quote and quote.rstrip(".") in text else text


def _clause(rule_id: str, rules: dict[str, dict[str, Any]], titles: dict[str, dict[str, str]], lang: str) -> list[str]:
    rule = rules.get(rule_id)
    if rule is None:
        return [f"  {LABELS[lang]['clause']} {rule_id}"]
    row = titles.get(rule["document_id"], {})
    title = (row.get("title_ar") if lang == "ar" else "") or row.get("title", rule["document_id"])
    page = kb.page_of(rule["document_id"], rule["chunk"])
    head = (f"  {LABELS[lang]['clause']} {rule['label']} ({rule_id}), {title}"
            f"{f', p. {page}' if page else ''} {tag(rule['document_id'], rule['chunk'])}")
    return [head, *_quote(rule, lang)]


def _humans(events: list[dict[str, Any]], seq: int) -> list[str]:
    """The named humans on shift in the last released facts before `seq`."""
    on = []
    for e in events:
        if e["seq"] > seq:
            break
        if e["action"] == "release_event":
            on = e["new_value"].get("facts", {}).get("human_agents_on_shift", on)
    return list(on)


def explain(path: str | Path, step: int, lang: str = "en") -> list[str]:
    if not audit.verify(path):
        raise ValueError(f"{path}: chain broken; not explained")
    events = runs._events(path)
    sid = events[0]["entity_id"]
    step_id = f"{sid}-{step}"
    mine = [e for e in events if e["action"] in runs.DECISIONS
            and (e["entity_id"] == step_id or e["entity_id"].startswith(f"{step_id}-"))]
    if not any(e["action"] == "gate" for e in mine):
        raise ValueError(f"{path}: no gate event at step {step_id}")
    rules = {r["id"]: r for r in data.load_rules()}
    titles = kb.manifest_by_id()
    words = LABELS[lang]
    lines = [f"{sid} {words['step']} {step} ({step_id}), {Path(path).as_posix()}", words["note"]]
    for e in mine:
        if e["action"] == "override_refused":
            lines += [f"{e['entity_id']}  {words['override']} {words['by']} {e['actor']}: "
                      f"{_verdict(e['verdict'], lang)}, {words['stands']}",
                      f"  {words['hash']} {e['hash']}"]
            continue
        verb = (e.get("old_value") or {}).get("verb") or e["action"]
        lines += ["", f"{e['entity_id']}  {verb}  {words['verdict']}: {_verdict(e['verdict'], lang)}",
                  f"  {words['hash']} {e['hash']}"]
        if e["action"] == "abstain":
            lines.append("  " + ", ".join(rules[c]["label"] if c in rules else c for c in e["clause_ids"]))
            continue
        for rule_id in e["clause_ids"]:
            lines += _clause(rule_id, rules, titles, lang)
        reasons = (e.get("new_value") or {}).get("reasons", [])
        handover = [r["text"] for r in reasons if r["kind"] == "obligation" and "human" in r["text"].lower()]
        for text in handover:
            lines.append(f"  {words['handover']}: {text}")
        if handover and (on := _humans(events, e["seq"])):
            lines.append(f"  {words['humans']}: {', '.join(on)}")
    return lines


# --- command line -----------------------------------------------------------------------------------------------

def _cli(args) -> int:
    try:
        lines = explain(args.log, args.step, args.lang)
    except (ValueError, FileNotFoundError) as error:
        print(f"why: {error}", file=sys.stderr)
        return 2
    print("\n".join(lines))
    return 0


def register(subparsers) -> None:
    parser = subparsers.add_parser("why", help="explain a recorded step from its log: verdict, clause, quote, hash")
    parser.add_argument("log")
    parser.add_argument("--step", type=int, required=True, help="the scenario step, e.g. 3")
    parser.add_argument("--lang", choices=("en", "ar"), default="en")
    parser.set_defaults(func=_cli)
