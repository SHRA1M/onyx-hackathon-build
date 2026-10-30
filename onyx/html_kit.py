"""HTML pieces shared by the replay viewer (order Task 14) and the site (order 2026-10-25 Task 25): the notice, the
verdict words and colours, the text, quote and clause helpers and the base CSS. Moved out of replay_viewer.py
unchanged, so docs/replay/index.html keeps its bytes."""

from __future__ import annotations

import json
from functools import lru_cache
from html import escape
from pathlib import Path

from onyx import data, gate, kb

NOTICE = "The operator, subscribers and numbers are synthetic; the law texts are real, linked and hashed."
WORDS = {gate.ALLOW: ("allow", "v-allow"), gate.HOLD: ("hold", "v-hold"), gate.BLOCK: ("block", "v-block"),
         gate.INSUFFICIENT: ("insufficient evidence", "v-insufficient")}


def rel(path: Path) -> str:
    return path.relative_to(kb.REPO).as_posix()


def text(text: str, cls: str = "", tag: str = "span", lang: str | None = None) -> str:
    """A text block; Arabic text (or lang='ar') renders right to left."""
    lang = lang or ("ar" if kb._is_arabic(text) else "en")
    attrs = f' class="{cls}"' if cls else ""
    attrs += ' lang="ar" dir="rtl"' if lang == "ar" else ""
    return f"<{tag}{attrs}>{escape(text)}</{tag}>"


def quote(text: str, lang: str | None = None) -> str:
    lang = lang or ("ar" if kb._is_arabic(text) else "en")
    rtl = ' lang="ar" dir="rtl"' if lang == "ar" else ""
    return f'<q class="quote" data-lang="{lang}"{rtl}>{escape(text)}</q>'


def page(document_id: str, clause: str) -> str:
    """ "p. N" for a committed chunk's page (kb.page_of), a link to the PDF at that page where the manifest's url is
    the document itself; "" where there is no page (order 2026-10-22 Task 16 item 1)."""
    page = kb.page_of(document_id, clause)
    if not page:
        return ""
    url = kb.page_link(document_id, page)
    return f'<a class="src" href="{escape(url)}">p. {page}</a>' if url else f"p. {page}"


@lru_cache(maxsize=None)
def _rows() -> tuple[dict[tuple[str, str], dict[str, str]], dict[str, dict[str, str]]]:
    rules = {}
    for r in data.load_rules():
        rules.setdefault((r["document_id"], r["chunk"]), r)
    return rules, kb.manifest_by_id()


BARE = "id lacks its language ending"


def bare(document_id: str) -> bool:
    """A cited document id with no -en / -ar ending: no manifest row, but the instrument of one (Iyas, 2026-10-29:
    tag it by the law and say so after the cite)."""
    manifest = _rows()[1]
    return document_id not in manifest and any(r["instrument"] == document_id for r in manifest.values())


def _instrument(document_id: str) -> dict[str, str]:
    """The manifest rows of an instrument, when all agree on binding_status and jurisdiction; KeyError otherwise."""
    rows = [r for r in _rows()[1].values() if r["instrument"] == document_id]
    if not rows or len({(r["binding_status"], r["jurisdiction"]) for r in rows}) != 1:
        raise KeyError(document_id)
    return rows[0]


def binding(document_id: str, clause: str = "", design_basis: bool = False) -> tuple[str, str]:
    """binding / advisory / method and UAE / foreign / international for a cited clause (order 2026-10-29-task-29
    Part C1): its rules.json row, else the manifest row of its document, else the rows of the instrument a bare id
    names (bare); KeyError with none. A design-basis
    reason (gate.py: IMDA, EU AI Act, GDPR) shows method, never binding: it never decides (addendum 16)."""
    rules, manifest = _rows()
    row = rules.get((document_id, clause)) or manifest.get(document_id) or _instrument(document_id)
    return ("method" if design_basis else row["binding_status"]), row["jurisdiction"]


def tag(document_id: str, clause: str = "", design_basis: bool = False) -> str:
    """The cite's binding tag as text, "[binding, UAE]", for the markdown pages; a bare id's note after it."""
    return "[{}, {}]".format(*binding(document_id, clause, design_basis)) + (f" ({BARE})" if bare(document_id) else "")


def tag_html(document_id: str, clause: str = "", design_basis: bool = False) -> str:
    status, jurisdiction = binding(document_id, clause, design_basis)
    note = f" ({BARE})" if bare(document_id) else ""
    return (f'<span class="tag" data-binding="{status}" data-jurisdiction="{jurisdiction}">{status}, '
            f"{jurisdiction}</span>{note}")


def cite(clause_id: str) -> str:
    document_id, _, clause = clause_id.partition(":")
    shown = page(document_id, clause) if clause else ""
    return f"<code>{escape(clause_id)}</code>" + (f" ({shown})" if shown else "") + f" {tag_html(document_id, clause)}"


def verdict(verdict: str) -> str:
    word, cls = WORDS[verdict]
    return f'<span class="verdict {cls}">{word}</span>'


def inline_json(value: object) -> str:
    """JSON for a <script type="application/json"> block: no '</' or '<!--' can close or comment it out."""
    out = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return out.replace("</", "<\\/").replace("<!--", "<\\!--")


CSS = """
:root { --ink: #1c1f24; --muted: #5b6270; --line: #d8dbe0; --bg: #ffffff; --panel: #f5f6f8;
  --allow: #1a7f37; --hold: #9a6700; --block: #c62828; --insufficient: #5f6773; }
* { box-sizing: border-box; }
body { margin: 0; padding: 0 16px 48px; background: var(--bg); color: var(--ink);
  font: 16px/1.5 "Segoe UI", system-ui, -apple-system, Helvetica, Arial, sans-serif; }
[lang="ar"] { font-family: "Segoe UI", "Geeza Pro", "Noto Naskh Arabic", "Arabic Typesetting", Tahoma, Arial,
  sans-serif; }
header { position: sticky; top: 0; background: var(--bg); border-bottom: 1px solid var(--line); padding: 8px 0; z-index: 1; }
h1 { margin: 4px 0; font-size: 1.4em; }
h2 { font-size: 1.2em; margin: 16px 0 4px; }
h3 { font-size: 1.05em; margin: 12px 0 6px; }
h4 { font-size: .95em; margin: 12px 0 4px; color: var(--muted); }
button { font: inherit; padding: 4px 10px; border: 1px solid var(--line); background: var(--panel); border-radius: 4px;
  cursor: pointer; }
button.on { background: var(--ink); color: var(--bg); }
.bar { display: flex; flex-wrap: wrap; gap: 12px; align-items: center; margin: 6px 0; }
.picker { display: flex; flex-wrap: wrap; gap: 6px; }
.picker button { text-align: start; }
.headline, .meta { margin: 2px 0; color: var(--muted); font-size: .9em; }
.notice { margin: 8px 0; padding: 6px 10px; background: var(--panel); border-left: 4px solid var(--hold); }
.message { padding: 10px 12px; background: var(--panel); border-radius: 4px; font-size: 1.05em; }
ul { padding-inline-start: 20px; margin: 4px 0; }
li { margin: 4px 0; }
.clauses { font-size: .92em; }
q.quote { display: inline-block; margin: 2px 0; }
.verdict { display: inline-block; padding: 0 8px; border-radius: 10px; color: #fff; font-weight: 600; }
.v-allow { background: var(--allow); }
.v-hold { background: var(--hold); }
.v-block { background: var(--block); }
.v-insufficient { background: var(--insufficient); }
.handover { margin: 10px 0; padding: 8px 12px; border: 2px solid var(--block); border-radius: 4px; }
.handover h4 { margin-top: 0; color: var(--block); }
.abstain { margin: 10px 0; padding: 8px 12px; border: 2px solid var(--insufficient); border-radius: 4px; }
.ungoverned { margin-top: 12px; padding: 6px 10px; border: 1px dashed var(--line); }
.ungoverned summary { cursor: pointer; color: var(--muted); }
code { font-size: .9em; overflow-wrap: anywhere; }
.tag { display: inline-block; padding: 0 6px; border: 1px solid var(--line); border-radius: 8px; color: var(--muted);
  font-size: .8em; white-space: nowrap; }
.scenario, .whatif, .run, .step, .headline { display: none; }
.scenario.on, .whatif.on, .run.on, .step.on, .headline.on { display: block; }
pre.text { white-space: pre-wrap; font: inherit; font-size: .92em; }
body.present { font-size: 22.4px; }
body.present .picker { display: none; }
"""
