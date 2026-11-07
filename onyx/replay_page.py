"""Replay pages (order 2026-10-21-task-9-fixes-tasks-10-11 item 7): `python -m onyx replay-page` writes
docs/replay/S1.md to S5.md, one recorded governed run each (runs/S<n>/run1.jsonl, English): the steps in order, each
proposal, the gate's verdict, the clause ids with their quotes, and both language quotes at every hand-over and
abstention. Text only, read from the committed log and rules.json; byte-identical on every run.

S2 reads the first C5 run (runs/c5/S2: English run1, run2, then Arabic) whose step 3 carries the hand-over with both
quotes and whose step 4, the human's, is allowed, when there is one (order 2026-10-22 item 12); the page says so.
S1, S3, S4 and S5 read the first English C5 run (run1, then run2) that cites every clause the scenario is grounded in,
in a proposal or a gate verdict; with none, the C3 run above (order 2026-10-23 Task 12 item 5)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from onyx import audit, data, kb, runs
from onyx.html_kit import tag

RUNS = kb.REPO / "runs"
OUT = kb.REPO / "docs" / "replay"
SCENARIOS = ("S1", "S2", "S3", "S4", "S5")
HANDOVER_QUOTES = {"CPR 26.7.2", "Licence 9.1"}
ARABIC_ONLY = "Arabic-only text; no official English on file"
C5_S2_LINE = ("This page reads a C5 run (prompt v5), not runs/S2/run1.jsonl: the first C5 S2 run whose step 3 carries "
              "the hand-over with both quotes and whose step 4, the human's, is allowed (order 2026-10-22 item 12).")


def _shows_handover(path: Path) -> bool:
    gates = [e for e in runs._events(path) if e["action"] == "gate"]
    step3 = any(HANDOVER_QUOTES <= {r.get("label") for r in e["new_value"].get("reasons", []) if r.get("kind") == "quote"}
                for e in gates if e["entity_id"] == "S2-3-care")
    step4 = any(e["verdict"] == "allow" for e in gates if e["entity_id"] == "S2-4-care")
    return step3 and step4


def cites_grounding(path: Path, sid: str) -> bool:
    """Every grounded_in clause of the scenario is cited in the run: a proposal's clause id, or the clause of a rule
    a gate verdict names."""
    rules = _rules()
    cited: set[str] = set()
    for e in runs._events(path):
        if e["action"] == "propose":
            cited |= {c for p in e["new_value"]["proposals"] for c in p.get("clause_ids", [])}
        elif e["action"] == "gate":
            cited |= {f"{rules[r]['document_id']}:{rules[r]['chunk']}" if r in rules else r
                      for r in e.get("clause_ids") or []}
    return all(c["clause_id"] in cited for c in data.load_scenario(sid)["grounded_in"]["clauses"])


def source(sid: str) -> Path:
    """The run a scenario's page reads (module docstring): a C5 run where one qualifies, else runs/S<n>/run1.jsonl."""
    if sid == "S2":
        for lang in runs.LANGS:
            for n in (1, 2):
                path = runs.run_path(RUNS / "c5", sid, n, lang)
                if path.exists() and _shows_handover(path):
                    return path
    else:
        for n in (1, 2):
            path = runs.run_path(RUNS / "c5", sid, n, "en")
            if path.exists() and cites_grounding(path, sid):
                return path
    return RUNS / sid / "run1.jsonl"


def _rules() -> dict[str, dict[str, Any]]:
    return {r["id"]: r for r in data.load_rules()}


def _page(clause_id: str) -> int | None:
    """The page of a cited `document:clause` id, from the committed chunks (kb.page_of)."""
    document_id, _, clause = clause_id.partition(":")
    return kb.page_of(document_id, clause) if clause else None


def cite(clause_id: str) -> str:
    """`document:clause` (p. N) [binding, UAE]: the page, then the binding tag (order 2026-10-29-task-29 Part C1)."""
    page = _page(clause_id)
    document_id, _, clause = clause_id.partition(":")
    return f"`{clause_id}`" + (f" (p. {page})" if page else "") + f" {tag(document_id, clause)}"


def _rule_tag(rule_id: str, rules: dict[str, dict[str, Any]]) -> str:
    return tag(rules[rule_id]["document_id"], rules[rule_id]["chunk"])


def rule_texts(rule: dict[str, Any]) -> tuple[str, str]:
    """A rule's English and Arabic (order Task 54 B.1, B.2). Arabic: the chunk's text_ar, then the rule's quote_ar.
    English: the rule's quote, then the chunk's text_en; "" where the chunk holds Arabic and no English."""
    try:
        chunk = kb.get_chunk(rule["document_id"], rule["chunk"])
    except KeyError:
        chunk = {}
    en, ar = " ".join(chunk.get("text_en", "").split()), " ".join(chunk.get("text_ar", "").split())
    if chunk and not en and ar:
        return "", ar
    return rule["quote"] or en, ar or rule.get("quote_ar", "")


def check_lines(reasons: list[dict[str, Any]]) -> list[str]:
    """The check a verdict with no clause rests on, as the log holds it (order Task 54 B.3)."""
    return [f"{'base' if r.get('gate') == 'base' else r.get('gate')} check: {r['text']}"
            for r in reasons if r.get("kind") == "check"]


def _clauses(ids: list[str], rules: dict[str, dict[str, Any]]) -> list[str]:
    out = []
    for rule_id in ids:
        rule = rules.get(rule_id)
        if not rule:
            out.append(f"  - `{rule_id}`")
            continue
        page = kb.page_of(rule["document_id"], rule["chunk"])
        en, _ = rule_texts(rule)
        out.append(f"  - `{rule_id}` {rule['label']}{f', p. {page}' if page else ''} {_rule_tag(rule_id, rules)}: "
                   f"{'' if en else 'AR: '}\"{rule['quote']}\"")
        if not en:
            out.append(f"    - EN: {ARABIC_ONLY}")
    return out


def grounded(scenario: dict[str, Any]) -> str:
    """The scenario's grounding line (order 2026-10-22 Task 16 item 2): its clauses with their pages, then the line."""
    g = scenario["grounded_in"]
    return f"Grounded in: {', '.join(cite(c['clause_id']) for c in g['clauses'])}. {g['line']}"


def _flagged(gap_ids: list[str], register: str = "../site/gaps.html") -> list[str]:
    """Each flagged gap's line, an example from elsewhere and its register link (order Task 31 Part D)."""
    from onyx import gaps  # render only: read from onyx/data/gaps.json at render time

    out = []
    for e in filter(None, map(gaps.elsewhere, gap_ids)):
        out.append(f"  - {e['id']}: {e['line']}")
        if e["label"] is None:  # a candidate: its line only
            continue
        out.append(f"    - Elsewhere: {e['label']}: \"{e['quote']}\"" if e["label"] else f"    - {gaps.NONE_FOUND}")
        out.append(f"    - Register: [{e['id']}]({register}#{e['id']})")
    return out


def _both(label: str, en: str, ar: str) -> list[str]:
    return [f"  - {label} EN: \"{en}\"", f"  - {label} AR: \"{ar or 'no Arabic text on file'}\""]


def _searched(searched: dict[str, Any], rules: dict[str, dict[str, Any]]) -> list[str]:
    """One clause an abstention searched: the English the log holds, the Arabic its chunk holds (Task 54 B.1, B.2)."""
    label = f"{searched['label']} {_rule_tag(searched['rule'], rules)}"
    en, ar = rule_texts(rules[searched["rule"]])
    if not en:
        return [f"  - {label} EN: {ARABIC_ONLY}", f"  - {label} AR: \"{ar}\""]
    return _both(label, searched["says"] or en, ar)


def _proposal(p: dict[str, Any]) -> list[str]:
    out = [f"- Proposal `{p['verb']}` to {p.get('target') or 'no target'}; cites "
           f"{', '.join(cite(c) for c in p.get('clause_ids', [])) or 'no clause'}"]
    if p.get("quote"):
        out.append(f"  - quoted: \"{p['quote']}\"")
    return out


def render(path: str | Path) -> str:
    path = Path(path)
    events = runs._events(path)
    config = events[0]["new_value"]
    sid = events[0]["entity_id"]
    scenario = data.load_scenario(sid)
    rules = _rules()
    lines = [f"# Replay: {sid}, {scenario['title_en']}", "", grounded(scenario), "",
             f"Generated by `python -m onyx replay-page` from `{path.relative_to(kb.REPO).as_posix()}`; do not edit by "
             "hand. The operator, subscriber and numbers are synthetic; the clauses are real.", "",
             f"Model `{config.get('model')}`, prompt {config.get('prompt', 'not logged (labels began with v4)')}, "
             f"{config.get('mode')}, "
             f"{config.get('lang')}. Hash chain: {'ok' if audit.verify(path) else 'BROKEN'}."]
    if sid == "S2" and "c5" in path.resolve().relative_to(RUNS).parts:
        lines += ["", C5_S2_LINE]
    for e in events[1:]:
        nv = e["new_value"] or {}
        if e["action"] == "release_event":
            lines += ["", f"## Step {nv['n']} ({e['entity_id']}), to {nv['to']}", "", f"> {nv['text']}", ""]
        elif e["action"] == "classify_channel":
            lines.append(f"- Channel (plain code): `{nv['channel']}`; {e['reason']}")
        elif e["action"] == "propose":
            for p in nv["proposals"]:
                lines += _proposal(p)
            for p in nv.get("rejected", []):
                lines.append(f"- Rejected before the gate (outside {e['actor']}'s mandate): `{p['verb']}`")
            if not nv["proposals"] and not nv.get("rejected"):
                lines.append(f"- {e['actor']} proposed nothing")
        elif e["action"] == "gate":
            what = f"`{e['old_value']['verb']}`" if (e.get("old_value") or {}).get("verb") else e["entity_id"]
            lines.append(f"- Gate on {what}: **{e['verdict']}**")
            lines += _clauses(e["clause_ids"], rules)
            if not e["clause_ids"]:
                lines += [f"  - {line}" for line in check_lines(nv.get("reasons", []))]
            quotes = [r for r in nv.get("reasons", []) if r.get("kind") == "quote"]
            if quotes:
                lines.append("- Hand-over, both languages:")
                for q in quotes:
                    lines += _both(f"{q['label']} {_rule_tag(q['clause'], rules)}", q["en"], q["ar"])
        elif e["action"] == "abstain":
            lines.append(f"- Abstention: **{nv['answer']}**; gap flagged: {', '.join(nv['gaps']) or 'none'}")
            lines += _flagged(nv["gaps"])
            lines.append("- Clauses searched, both languages:")
            for s in nv["searched"]:
                lines += _searched(s, rules)
        elif e["action"] == "override_refused":
            lines.append(f"- Override refused: {e['reason']}")
        else:
            lines.append(f"- {e['action']}: {e['entity_id']}")
    return "\n".join(lines) + "\n"


def write(out: str | Path = OUT) -> list[Path]:
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    written = []
    for sid in SCENARIOS:
        page = out / f"{sid}.md"
        page.write_text(render(source(sid)), encoding="utf-8", newline="\n")
        written.append(page)
    return written


def register(subparsers) -> None:
    parser = subparsers.add_parser("replay-page", help="write docs/replay/S1.md to S5.md from one recorded run each")
    parser.add_argument("--html", action="store_true", help="write docs/replay/index.html, the replay viewer, instead")
    parser.set_defaults(func=_cli)


def _cli(args) -> int:
    if args.html:
        from onyx import replay_viewer  # it imports this module
        print(replay_viewer.write().relative_to(kb.REPO).as_posix())
        return 0
    print("\n".join(p.relative_to(kb.REPO).as_posix() for p in write()))
    return 0
