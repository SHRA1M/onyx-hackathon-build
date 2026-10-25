"""HTML pieces shared by the replay viewer (order Task 14) and the site (order 2026-10-25 Task 25): the notice, the
verdict words and colours, the text, quote and clause helpers and the base CSS. Moved out of replay_viewer.py
unchanged, so docs/replay/index.html keeps its bytes."""

from __future__ import annotations

import json
from html import escape
from pathlib import Path

from onyx import gate, kb

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


def cite(clause_id: str) -> str:
    document_id, _, clause = clause_id.partition(":")
    shown = page(document_id, clause) if clause else ""
    return f"<code>{escape(clause_id)}</code>" + (f" ({shown})" if shown else "")


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
.scenario, .whatif, .run, .step, .headline { display: none; }
.scenario.on, .whatif.on, .run.on, .step.on, .headline.on { display: block; }
pre.text { white-space: pre-wrap; font: inherit; font-size: .92em; }
body.present { font-size: 22.4px; }
body.present .picker { display: none; }
"""
