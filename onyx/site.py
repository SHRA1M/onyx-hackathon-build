"""The Mizan site (order 2026-10-25-task-25-site): `python -m onyx site` writes docs/site/, seven static pages that open
from file:// with no server and no network call: index (the figures and counts), runs (the replay viewer), gaps (the
register), kb (the manifest), verify (the hash chain recomputed in the browser), whatif (S2 under gap 1's rule) and
modeldown (S2 with the model call at step 3 made to fail, Task 29 Part A) and localmodel (S2 recorded once on a
local model through Ollama, Task 39 E; shown, never scored).
Every figure, row and quote is read from eval/results.json, eval/results.md, the run logs, kb/manifest.csv and
onyx/data/gaps.json by plain code; none is typed here. Byte-identical on every run.

verify.html carries the text of every C3, C4 and C5 log (C3: runs/S*/ and runs/ungoverned/, governed and ungoverned;
C4: runs/c4/; C5: runs/c5/). Its canonical JSON copies each number as the log wrote it: JSON.parse would turn
Python's 10447.0 into 10447 and break the hash (three events do). tests/test_site.py runs CHAIN_JS through Node on
every log and compares each event's canonical form with audit.canonical_json."""

from __future__ import annotations

import collections
import json
import re
from html import escape
from pathlib import Path
from typing import Any

from onyx import audit, data, eval as eval_mod, gaps, kb, localmodel, modeldown, replay_page, replay_viewer, runs, whatif
from onyx.html_kit import CSS, NOTICE, inline_json, quote, text, verdict

OUT = kb.REPO / "docs" / "site"
RESULTS = kb.REPO / "eval" / "results.json"
RESULTS_MD = kb.REPO / "eval" / "results.md"
REPORT = kb.REPO / "docs" / "report.md"
REPO_URL = "https://github.com/SHRA1M/onyx-hackathon-build"
WHATIF_RUN, WHATIF_RULE = replay_viewer.WHATIF_RUN, "gap-1"
SENTENCE = "A quote that is not word for word in a verified clause is rejected before it reaches the subscriber."
PAGES = (("index.html", "Overview"), ("runs.html", "Runs"), ("gaps.html", "Gap register"),
         ("kb.html", "Knowledge base"), ("verify.html", "Verify a log"), ("whatif.html", "What-if"),
         ("modeldown.html", "Model down"), ("localmodel.html", "Local model"))
C5_HEADLINE = ("citation_validity", "action_recall", "abstention", "gap_recall")
# the labels the report uses, and the name of each metric's definition in eval/results.md
LABELS = {"citation_validity": "Citation validity", "action_recall": "Action recall", "abstention": "Abstention",
          "gap_recall": "Gap recall", "gate_rejection_rate": "Gate rejection", "ungoverned_claims_allowed":
          "Claims allowed, ungoverned"}
DEFINED_AS = {"citation_validity": "citation validity", "action_recall": "action recall", "abstention": "abstention",
              "gap_recall": "gap recall", "gate_rejection_rate": "gate rejection rate",
              "ungoverned_claims_allowed": "ungoverned baseline"}
CONFIGS = (("C3 governed", replay_page.RUNS, True), ("C3 ungoverned", replay_page.RUNS, False),
           ("C4 governed", replay_page.RUNS / "c4", True), ("C5 governed", replay_page.RUNS / "c5", True))


# --- data ------------------------------------------------------------------------------------------------------

def _results() -> dict[str, Any]:
    return json.loads(RESULTS.read_text(encoding="utf-8"))


def definitions() -> dict[str, str]:
    """Each bullet of eval/results.md's Definitions section: the name before the first ': ', and the rest."""
    section = RESULTS_MD.read_text(encoding="utf-8").split("## Definitions", 1)[1]
    items: list[str] = []
    for line in section.splitlines():
        if line.startswith("- "):
            items.append(line[2:])
        elif line.strip() and items and not line.startswith("#"):
            items[-1] += " " + line.strip()
    return {name: rest for name, _, rest in (i.partition(": ") for i in items) if rest}


def verify_logs() -> list[tuple[str, list[Path]]]:
    """Every C3, C4 and C5 log, by configuration, in scenario, language and run order."""
    out = []
    for label, root, governed in CONFIGS:
        paths = [p for sid in runs.SCENARIOS for lang in runs.LANGS for n in range(1, runs.RUNS + 1)
                 if (p := runs.run_path(root, sid, n, lang, governed)).exists()]
        out.append((label, paths))
    return out


def verify_names() -> list[str]:
    return [replay_viewer._rel(p) for _, paths in verify_logs() for p in paths]


def gap_order() -> list[str]:
    """The register's rows in the report's order (its gap table), then the rows the report leaves out, in register
    order."""
    section = REPORT.read_text(encoding="utf-8").split("## Policy gaps", 1)[1]
    numbers = [line.split("|")[1].strip() for line in section.splitlines() if line.startswith("| ")]
    ids = [r["id"] for r in data.load_gaps()["gaps"]]
    in_report = [f"gap-{n}" for n in numbers if f"gap-{n}" in ids]
    return in_report + [i for i in ids if i not in in_report]


def _counts() -> dict[str, int]:
    rows = kb.load_manifest()
    by_status = collections.Counter(r["status"] for r in rows)
    return {"documents": len(rows)} | {s: by_status[s] for s in kb.STATUSES if by_status[s]}


# --- page frame ------------------------------------------------------------------------------------------------

def nav(current: str) -> str:
    links = "".join(f'<a class="site-link{" on" if name == current else ""}" href="{name}">{escape(label)}</a>'
                    for name, label in PAGES)
    return (f'<nav class="site"><span class="brand">Mizan</span>{links}'
            f'<a class="site-link" href="{REPO_URL}">Repository</a></nav>\n')


def _frame(name: str, title: str, body: str, script: str = "") -> str:
    return PAGE.format(title=escape(title), css=CSS + SITE_CSS, nav=nav(name), body=body,
                       script=f"<script>{script}</script>\n" if script else "")


def _fmt(value: Any) -> str:
    if isinstance(value, dict):
        low, high = _fmt(value["min"]), _fmt(value["max"])
        return low if low == high else f"{low} to {high}"
    return eval_mod._fig(value) if isinstance(value, float) or value is None else str(value)


def _fig(value: Any, config: str, metric: str, lang: str, sid: str = "") -> str:
    attrs = f' data-sid="{sid}"' if sid else ""
    return (f'<span class="fig" data-config="{config}" data-metric="{metric}" data-lang="{lang}"{attrs} '
            f'data-value="{escape(json.dumps(value, sort_keys=True))}">{_fmt(value)}</span>')


def _label(metric: str, notes: list[str]) -> str:
    n = notes.index(metric) + 1
    return f'{LABELS[metric]}<sup><a href="#def-{metric}">{n}</a></sup>'


# --- index.html ------------------------------------------------------------------------------------------------

def index() -> str:
    results, defs = _results(), definitions()
    notes = list(C5_HEADLINE) + ["ungoverned_claims_allowed", "gate_rejection_rate"]
    c5, c3 = results["c5"]["C5"]["all"], results["c4"]["C3"]["all"]
    c5_rows = "".join(f'<tr><th>{_label(m, notes)}</th><td class="num">{_fig(c5["en"][m], "C5", m, "en")}</td>'
                      f'<td class="num">{_fig(c5["ar"][m], "C5", m, "ar")}</td></tr>' for m in C5_HEADLINE)
    claims = "ungoverned_claims_allowed"
    c3_rows = (f'<tr><th>{_label(claims, notes)}</th><td class="num">{_fig(c3["en"][claims], "C3", claims, "en")}'
               f'</td><td class="num">{_fig(c3["ar"][claims], "C3", claims, "ar")}</td></tr>')
    rejection = "".join(
        f'<tr><th>{sid}</th>' + "".join(
            f'<td class="num">{_fig(results["scenarios"][sid]["governed"][lang]["gate_rejection_rate"], "C3", "gate_rejection_rate", lang, sid)}</td>'
            for lang in runs.LANGS) + "</tr>" for sid in runs.SCENARIOS)
    runs_c5, runs_c3 = c5["en"]["runs"], c3["en"]["runs"]
    counts = _counts()
    count_cells = "".join(f'<div class="card"><span class="big count" data-status="{s}">{n}</span>'
                          f'<br>{"documents" if s == "documents" else s}</div>' for s, n in counts.items())
    foot = "".join(f'<li id="def-{m}"><b>{escape(DEFINED_AS[m])}</b>: {escape(defs[DEFINED_AS[m]])}</li>'
                   for m in notes)
    body = f"""<h1>Mizan: governed consumer-care agents</h1>
<p class="notice">{escape(NOTICE)}</p>
<p class="lead">{escape(SENTENCE)}</p>
<p>Five agents propose JSON actions; plain-code gates decide from clauses of binding UAE text, in English and Arabic;
every step goes to a hash-chained log you can verify on this site.</p>
<div class="cards">
<a class="card link" href="runs.html"><b>Runs</b><br>Each scenario step by step, governed and without the gates.</a>
<a class="card link" href="gaps.html"><b>Gap register</b><br>What the binding texts leave open, and who could close it.</a>
<a class="card link" href="kb.html"><b>Knowledge base</b><br>Every document, its status and its SHA-256.</a>
<a class="card link" href="verify.html"><b>Verify a log</b><br>Recompute any run's hash chain in this browser.</a>
<a class="card link" href="whatif.html"><b>What-if</b><br>S2 replayed under the rule gap 1 recommends.</a>
<a class="card link" href="modeldown.html"><b>Model down</b><br>S2 with the model call at step 3 made to fail.</a>
<a class="card link" href="localmodel.html"><b>Local model</b><br>S2 recorded once on an open model on a desktop GPU.</a>
</div>
<h2>Governed, C5 ({runs_c5} runs per language)</h2>
<table class="grid figs"><thead><tr><th>Figure</th><th>English</th><th>Arabic</th></tr></thead>
<tbody>{c5_rows}</tbody></table>
<h2>Without the gates, C3 ({runs_c3} runs per language)</h2>
<table class="grid figs"><thead><tr><th>Figure</th><th>English</th><th>Arabic</th></tr></thead>
<tbody>{c3_rows}</tbody></table>
<p>{_label("gate_rejection_rate", notes)}, governed, by scenario (min to max over the runs):</p>
<table class="grid figs"><thead><tr><th>Scenario</th><th>English</th><th>Arabic</th></tr></thead>
<tbody>{rejection}</tbody></table>
<h2>Knowledge base</h2>
<div class="cards counts">{count_cells}</div>
<h2>Definitions</h2>
<p class="meta">From <code>eval/results.md</code>; every figure above is read from <code>eval/results.json</code>.</p>
<ol class="defs">{foot}</ol>
"""
    return _frame("index.html", "Mizan", body)


# --- runs.html -------------------------------------------------------------------------------------------------

def runs_page() -> str:
    html = replay_viewer.Viewer(verify="verify.html", register="gaps.html").render(nav=nav("runs.html"), css=CSS + SITE_CSS)
    # the viewer's what-if page sits beside the old page, docs/replay/
    name = whatif.page_name(WHATIF_RUN, WHATIF_RULE)
    for name in (name, modeldown.page_name(WHATIF_RUN)):
        old = f'<a href="{name}">{name}</a>'
        assert html.count(old) == 1
        html = html.replace(old, f'<a href="../replay/{name}">{name}</a>')
    return html


# --- gaps.html -------------------------------------------------------------------------------------------------

def _lang(text: str) -> str:
    return "ar" if kb._is_arabic(text) else "en"  # an Arabic original's own text (Task 33, 52/2024)


def _searched(s: dict[str, Any]) -> str:
    if s.get("url"):  # a text with no KB row, cited by its URL, as docs/gaps.md (Task 35b)
        page = f'p. {s["page"]}, ' if s.get("page") else ""
        url = escape(s["url"])
        return (f'<li><code>{escape(s["clause"])}</code> ({page}<a href="{url}">{url}</a>): {escape(s["says"])}'
                f'<br>EN: {quote(s["quote"], "en")}</li>')
    if s.get("file"):  # quoted from the stored source, no chunk (Task 32)
        page = f'p. {s["page"]}, ' if s.get("page") else ""  # a web page's text has none (106/2026 English)
        return (f'<li><code>{escape(s["clause"])}</code> ({page}<code>{escape(s["file"])}</code>): '
                f'{escape(s["says"])}<br>{_lang(s["quote"]).upper()}: {quote(s["quote"], _lang(s["quote"]))}</li>')
    document_id, clause = s["clause"].split(":", 1)
    chunk = kb.get_chunk(document_id, clause)
    parts = [f'<code>{escape(s["clause"])}</code> (p. {s.get("page", chunk["page"])}): {escape(s["says"])}']
    en = s.get("quote") or chunk["text_en"]
    if en:
        parts.append(f"EN: {quote(en, 'en')}")
    if chunk["text_ar"]:
        parts.append(f"AR (the whole chunk): {quote(chunk['text_ar'], 'ar')}")
    if s.get("quote_ar"):
        page = f"p. {s['page_ar']}, " if s.get("page_ar") else ""  # the Arabic PDF's page, as docs/gaps.md (Task 41)
        parts.append(f"AR ({page}<code>{escape(s['file_ar'])}</code>): {quote(s['quote_ar'], 'ar')}")
    return "<li>" + "<br>".join(parts) + "</li>"


def _example(ex: dict[str, Any]) -> str:
    page = f"p. {ex['page']}, " if ex.get("page") else ""  # the PDF page, as docs/gaps.md (Task 35)
    lang = "AR: " if kb._is_arabic(ex["quote"]) else ""  # an Arabic original's own text, as docs/gaps.md (Task 35)
    ar = (f"<br>AR (p. {ex['page_ar']}, <code>{escape(ex['file_ar'])}</code>): {quote(ex['quote_ar'], 'ar')}"
          if ex.get("quote_ar") else "")  # the Arabic beside the English (Task 35, Saudi 552/1445)
    return (f"<li>{escape(ex['document'])}, {escape(ex['clause'])} ({escape(ex['status'])}, {page}"
            f"<code>{escape(ex['file'])}</code>): {escape(ex['says']) + ' ' if ex.get('says') else ''}"
            f"{lang}{quote(ex['quote'])}{ar}</li>")  # says: a caveat beside the quote (Task 31)


def _examples(title: str, examples: list[dict[str, Any]]) -> str:
    return f"<h4>{title}</h4><ul>{''.join(_example(ex) for ex in examples)}</ul>"


def _gap(row: dict[str, Any]) -> str:
    searched = "".join(_searched(s) for s in row["searched"])
    searched += "".join(f"<li>{escape(fw['document'])}, {escape(fw['clause'])} (p. {fw['page']}; framework, "
                        f"non-binding): {escape(fw['says'])}<br>EN (<code>{escape(fw['file'])}</code>): "
                        f"{quote(fw['quote'], 'en')}</li>" for fw in row.get("framework", []))
    examples = (_examples("Global example", row["global_examples"]) if row["global_examples"] else
                f"<h4>Global example</h4><p>{escape(row['global_none'])}</p>")
    if row.get("examples_note"):  # the prose line after the examples, as docs/gaps.md (Task 33, gap-8)
        examples += f"<p>{escape(row['examples_note'])}</p>"
    standard = _examples("The standard's own text", row["standard_text"]) if row.get("standard_text") else ""
    note = f'<p>{escape(row["note"])}</p>' if row.get("note") else ""  # as docs/gaps.md (hq ruling 2026-10-26, Task 27)
    return (f'<section class="gap-row" data-id="{row["id"]}" id="{row["id"]}">'
            f'<h2>{escape(row["id"])}: {escape(row["line"])}</h2><p>{escape(row["gap"])}</p>'
            f'<p class="meta">Kind: {escape(row["kind"])}. Category: {escape(row["category"])}. Addressee: '
            f'{escape(", ".join(row["addressee"]))}. Exposed by: {escape(row["exposed_by"])}.</p>{note}'
            f'<h4>Clauses searched</h4><ul class="clauses">{searched}</ul>'
            f'<h4>UAE position</h4><p>{escape(row["uae_position"])}</p>{standard}{examples}'
            f'<h4>Recommendation</h4><p>{escape(row["recommendation"])}</p></section>')


def gaps_page() -> str:
    register = data.load_gaps()
    by_id = {r["id"]: r for r in register["gaps"]}
    order = gap_order()
    toc = "".join(f'<li><a href="#{i}">{escape(i)}</a>: {escape(by_id[i]["line"])}</li>' for i in order)
    def prose(c: dict[str, Any], css: str) -> str:
        return (f'<section class="{css}" data-name="{escape(c["name"])}"><h3>{escape(c["name"])}</h3>'
                f'<p>{escape(c["line"])}</p><ul class="clauses">{"".join(_searched(s) for s in c["searched"])}</ul>'
                '</section>')
    candidates = "".join(prose(c, "candidate") for c in register["candidates"])
    nothing = "".join(prose(c, "nothing-found") for c in register["nothing_found"])  # as docs/gaps.md (Task 41)
    body = (f'<h1>Gap register</h1><p class="notice">{escape(NOTICE)}</p>'
            "<p>A gap is claimed only where no clause in any VERIFIED or REFERENCED document reaches the concern. "
            "Every row lists the clauses searched and what each says, English and, where the chunk holds it, Arabic. "
            "Rows in the report's order; read from <code>onyx/data/gaps.json</code>.</p>"
            f"<p>{escape(gaps.GULF_LINE)}</p><p>{escape(gaps.FREE_ZONE_LINE)}</p>"
            f"<p>{_code(gaps.AUTHORITY_LINE)}</p><p>{escape(gaps.COMPANION_LINE)}</p>"
            f'<ol class="toc">{toc}</ol>' + "".join(_gap(by_id[i]) for i in order) +
            f"<h2>Candidates</h2><p>Flagged as candidates; no global example required.</p>{candidates}"
            f"<h2>Searched, nothing found</h2>{nothing}"
            f'<p class="meta">Sources: {escape(register["source"])}.</p>')
    return _frame("gaps.html", "Mizan: gap register", body)


# --- kb.html ---------------------------------------------------------------------------------------------------

KB_COLUMNS = ("document_id", "title", "issuer", "instrument", "language", "status", "binding_status", "sha256", "url",
              "notes")


def _kb_cell(row: dict[str, str], column: str) -> str:
    value = row[column]
    if column == "title":
        ar = f"<br>{text(row['title_ar'], lang='ar')}" if row["title_ar"] else ""
        return f"{escape(value)}{ar}"
    if column == "sha256":
        return f'<code class="sha">{escape(value)}</code>'
    if column == "url":
        return f'<a class="src" href="{escape(value)}">{escape(value)}</a>' if value.startswith("http") else escape(value)
    if column == "document_id":
        return f"<code>{escape(value)}</code>"
    return escape(value)


def kb_page() -> str:
    rows = kb.load_manifest()
    counts = _counts()
    count_cells = " ".join(f'<span class="count" data-status="{s}">{n}</span> {s}' for s, n in counts.items())
    filters = []
    for column in ("status", "language"):
        values = sorted({r[column] for r in rows})
        buttons = "".join(f'<button data-filter="{column}" data-value="{escape(v)}">{escape(v)}</button>'
                          for v in values)
        filters.append(f'<div class="filters"><span>{column}:</span><button class="on" data-filter="{column}" '
                       f'data-value="">all</button>{buttons}</div>')
    head = "".join(f"<th>{c}</th>" for c in KB_COLUMNS)
    body_rows = "".join(
        f'<tr data-id="{escape(r["document_id"])}" data-status="{escape(r["status"])}" '
        f'data-language="{escape(r["language"])}">' + "".join(f"<td>{_kb_cell(r, c)}</td>" for c in KB_COLUMNS) +
        "</tr>" for r in rows)
    body = (f'<h1>Knowledge base</h1><p class="notice">{escape(NOTICE)}</p>'
            f"<p>{count_cells}. Read from <code>kb/manifest.csv</code>; <code>python -m onyx kb verify</code> checks "
            f"every fetched source against its sha256. What it holds and its limits: "
            f'<a href="../../kb/DATASHEET.md">kb/DATASHEET.md</a>.</p>' + "".join(filters) +
            f'<p class="meta" id="shown"></p><div class="tablewrap"><table class="grid kb"><thead><tr>{head}</tr>'
            f"</thead><tbody>{body_rows}</tbody></table></div>")
    return _frame("kb.html", "Mizan: knowledge base", body, KB_JS)


# --- verify.html -----------------------------------------------------------------------------------------------

def verify_page() -> str:
    groups, logs = [], {}
    for label, paths in verify_logs():
        options = "".join(f'<option value="{replay_viewer._rel(p)}">{replay_viewer._rel(p)}</option>' for p in paths)
        groups.append(f'<optgroup label="{escape(label)} ({len(paths)})">{options}</optgroup>')
        logs |= {replay_viewer._rel(p): p.read_text(encoding="utf-8") for p in paths}
    body = (f'<h1>Verify a log</h1><p class="notice">{escape(NOTICE)}</p>'
            "<p>Every event in a run log carries <code>hash = sha256(prev_hash + canonical_json(event without "
            "\"hash\"))</code>; the first <code>prev_hash</code> is 64 zeros (<code>onyx/audit.py</code>). This page "
            "recomputes the chain in your browser with WebCrypto, from the log text it carries; no network call. "
            "Editing, inserting or deleting any line breaks the chain from that line on.</p>"
            f'<p><label>Run <select id="log">{"".join(groups)}</select></label> '
            '<button id="go">Verify</button></p>'
            '<p>In a terminal: <code id="cmd"></code></p>'
            "<p>Explain one step from the same log, no model call: <code>python -m onyx why &lt;log&gt; --step &lt;n&gt;"
            " [--lang ar]</code> prints the verdict, each clause with its title, page and words, the hand-over and the "
            "event hash.</p>"
            '<p id="summary" class="lead"></p><div class="tablewrap"><table class="grid chain"><thead><tr><th>seq</th>'
            "<th>action</th><th>stored hash</th><th>recomputed</th><th></th></tr></thead><tbody id=\"rows\"></tbody>"
            f'</table></div><script type="application/json" id="logs">{inline_json(logs)}</script>')
    return _frame("verify.html", "Mizan: verify a log", body, CHAIN_JS + VERIFY_JS)


# --- whatif.html -----------------------------------------------------------------------------------------------

def _pill(value: str | None) -> str:
    return verdict(value) if value in replay_viewer.WORDS else escape(str(value))


def whatif_page() -> str:
    rule = whatif.load_rule(WHATIF_RULE)
    recorded, under, changes = whatif.replay_under(WHATIF_RUN, WHATIF_RULE)
    changed = {c[0]: c for c in changes}
    rows = []
    for rec, new in zip(recorded, under, strict=True):
        change = changed.get(rec[0])
        added = "".join(f"<li>{escape(r['kind'])}: {escape(r['text'])}</li>" for r in change[4]) if change else ""
        rows.append(f'<tr class="{"changed" if change else ""}" data-entity="{escape(rec[0])}" '
                    f'data-recorded="{escape(str(rec[2]))}" data-whatif="{escape(str(new[2]))}">'
                    f"<td><code>{escape(rec[0])}</code></td><td>{escape(rec[1])}</td><td>{_pill(rec[2])}</td>"
                    f"<td>{_pill(new[2])}</td><td><ul>{added}</ul></td></tr>")
    findings = "".join(f"<li>{escape(r['text'])}</li>" for c in changes for r in c[4] if r["kind"] == "finding")
    path = replay_viewer._rel(WHATIF_RUN)
    md = whatif.page_name(WHATIF_RUN, WHATIF_RULE)
    body = (f"<h1>What-if: {escape(WHATIF_RUN.parent.name)} under the rule {escape(rule['gap'].replace('-', ' '))} "
            f'recommends</h1><p class="notice">{escape(NOTICE)}</p>'
            f'<p>Run <code>{path}</code>, hash chain {"ok" if audit.verify(WHATIF_RUN) else "BROKEN"} '
            f'<a class="button verify" href="verify.html#{path}">Verify this log</a>. Replayed offline from the '
            "logged model responses; no model call. Left: what the gate decided in the recorded run. Right: the same "
            f'replay with the proposed rule added. Text page: <a href="../replay/{md}">{md}</a>.</p>'
            f'<div class="rule"><h2>Proposed rule, not law</h2><p><code>{escape(rule["id"])}</code>, '
            f"{escape(rule['status'])}, for {escape(rule['addressee'])}.</p>"
            f"<p>{text(rule['text_en'], lang='en')}</p><p>{text(rule['text_ar'], lang='ar')}</p>"
            f"<p>Value: {escape(str(rule['value']))} {escape(rule['unit'])}. Basis: {escape(rule['value_basis'])}.</p>"
            "</div><h2>Decision by decision</h2>"
            '<div class="tablewrap"><table class="grid whatif-table"><thead><tr><th>decision</th><th>action</th>'
            "<th>recorded</th><th>what-if</th><th>added (proposed, not law)</th></tr></thead><tbody>"
            + "".join(rows) + "</tbody></table></div>"
            f"<p>{len(recorded) - len(changes)} of {len(recorded)} decisions identical.</p>"
            f"<h2>Second-order finding</h2><ul>{findings or '<li>none</li>'}</ul>")
    return _frame("whatif.html", "Mizan: what-if", body)


# --- modeldown.html --------------------------------------------------------------------------------------------

def _code(cell: str) -> str:
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", escape(cell))


def modeldown_page() -> str:
    at = replay_viewer.MODELDOWN_AT
    recorded_events, down_events = runs._events(WHATIF_RUN), modeldown.replay_events(WHATIF_RUN, at)
    before, after = modeldown._rows(recorded_events, at), modeldown._rows(down_events, at)
    same, total, notes = modeldown.stays(recorded_events, down_events, at)
    sid = recorded_events[0]["entity_id"]
    rows = "".join(f'<tr data-step="{sid}-{n}"><td><code>{sid}-{n}</code></td>'
                   + "".join("<td><ul>" + "".join(f"<li>{_code(c)}</li>" for c in side.get(n, ["none"])) + "</ul></td>"
                             for side in (before, after)) + "</tr>"
                   for n in sorted(set(before) | set(after)))
    path = replay_viewer._rel(WHATIF_RUN)
    md = modeldown.page_name(WHATIF_RUN)
    body = (f"<h1>Model down: {escape(sid)}, the call at step {at} fails</h1>"
            f'<p class="notice">{escape(NOTICE)}</p>'
            f'<p class="lead">{escape(modeldown.LABEL)}</p>'
            f'<p>Run <code>{path}</code>, hash chain {"ok" if audit.verify(WHATIF_RUN) else "BROKEN"} '
            f'<a class="button verify" href="verify.html#{path}">Verify this log</a>. Replayed offline from the '
            "logged model responses; no model call. Left: what the recorded run decided. Right: the same replay with "
            f"the model call at step {at} raising what the model adapter raises after its last attempt. Text page: "
            f'<a href="../replay/{md}">{md}</a>.</p>'
            f"<h2>Step {at} and after</h2>"
            '<div class="tablewrap"><table class="grid whatif-table"><thead><tr><th>step</th><th>recorded</th>'
            "<th>model-down</th></tr></thead><tbody>" + rows + "</tbody></table></div>"
            f"<h2>What stays</h2><p>{same} of {total} decisions outside step {at} identical.</p>"
            + "".join(f"<p>{_code(n)}</p>" for n in notes)
            + f"<p><b>No model took part in step {at} of the model-down column.</b></p>")
    return _frame("modeldown.html", "Mizan: model down", body)


# --- localmodel.html -------------------------------------------------------------------------------------------

def localmodel_page() -> str:
    m, path = localmodel.machine(), replay_viewer._rel(localmodel.RUN)
    settings = ", ".join(f"<code>{escape(k)}={escape(v)}</code>" for k, v in sorted(m["settings"].items()))
    body_rows = "".join(
        f'<tr data-step="{escape(r["step"])}"><td><code>{escape(r["step"])}</code></td><td>{escape(r["actor"])}</td>'
        f'<td>{escape(r["event"])}</td><td>{verdict(r["verdict"]) if r["verdict"] else ""}</td>'
        f'<td>{"<br>".join(f"<code>{escape(c)}</code>" for c in r["clauses"])}</td><td>{escape(r["note"])}</td></tr>'
        for r in localmodel.rows())
    body = (f"<h1>Local model: S2 on {escape(m['model'])}</h1>"
            f'<p class="notice">{escape(NOTICE)}</p>'
            f'<p class="lead">{escape(localmodel.LABEL)}</p>'
            f"<p>Model <code>{escape(m['model'])}</code> through Ollama {escape(m['ollama'])}, on this machine: GPU "
            f"{escape(m['gpu'])}, RAM {escape(m['ram_gb'])} GB; Ollama settings {settings}. The same adapter, prompt, "
            "gates and answer keys as every other run; only the endpoint and the model name differ, and nothing "
            f"left the PC. Run <code>{path}</code>, hash chain {'ok' if audit.verify(localmodel.RUN) else 'BROKEN'}; "
            f"check it with <code>python -m onyx verify-log {path}</code>.</p>"
            "<h2>Steps, verdicts and clauses, as logged</h2>"
            '<div class="tablewrap"><table class="grid"><thead><tr><th>step</th><th>actor</th><th>event</th>'
            "<th>verdict</th><th>clauses</th><th>proposed, or why not</th></tr></thead><tbody>"
            + body_rows + "</tbody></table></div>")
    return _frame("localmodel.html", "Mizan: local model", body)


# --- write -----------------------------------------------------------------------------------------------------

def render() -> dict[str, str]:
    return {"index.html": index(), "runs.html": runs_page(), "gaps.html": gaps_page(), "kb.html": kb_page(),
            "verify.html": verify_page(), "whatif.html": whatif_page(), "modeldown.html": modeldown_page(),
            "localmodel.html": localmodel_page()}


def write(out: str | Path = OUT) -> list[Path]:
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    written = []
    for name, html in render().items():
        (out / name).write_text(html, encoding="utf-8", newline="\n")
        written.append(out / name)
    return written


def _cli(args) -> int:
    for path in write():
        print(replay_viewer._rel(path))
    return 0


def register(subparsers) -> None:
    parser = subparsers.add_parser("site", help="write docs/site/, the static site, from the committed data")
    parser.set_defaults(func=_cli)


PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>{css}</style>
</head>
<body>
{nav}<main class="site">
{body}
</main>
{script}</body>
</html>
"""

SITE_CSS = """
nav.site { display: flex; flex-wrap: wrap; gap: 4px 16px; align-items: baseline; padding: 10px 0;
  border-bottom: 1px solid var(--line); }
nav.site .brand { font-weight: 700; margin-inline-end: 8px; }
a.site-link { color: var(--ink); text-decoration: none; border-bottom: 2px solid transparent; }
a.site-link.on { border-bottom-color: var(--ink); font-weight: 600; }
a.button { display: inline-block; padding: 0 10px; border: 1px solid var(--line); border-radius: 4px;
  background: var(--panel); color: var(--ink); text-decoration: none; font-size: .9em; }
main.site { max-width: 1200px; }
.lead { font-size: 1.15em; font-weight: 600; }
table.grid { border-collapse: collapse; margin: 8px 0; }
table.grid th, table.grid td { border: 1px solid var(--line); padding: 4px 8px; text-align: start; vertical-align: top; }
td.num { font-variant-numeric: tabular-nums; text-align: end; }
.tablewrap { overflow-x: auto; }
.cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px; margin: 10px 0; }
.card { display: block; border: 1px solid var(--line); border-radius: 6px; padding: 10px 12px; color: var(--ink); }
a.card { text-decoration: none; }
a.card:hover { border-color: var(--ink); }
.big { font-size: 1.8em; font-weight: 700; }
.defs li { font-size: .92em; }
code.sha, td.sha { font-family: Consolas, "Courier New", monospace; font-size: .8em; overflow-wrap: anywhere; }
table.chain { width: 100%; table-layout: fixed; }
table.chain th:nth-child(1) { width: 4em; }
table.chain th:nth-child(2) { width: 10em; }
table.chain th:nth-child(5) { width: 6em; }
table.kb td { font-size: .88em; }
.filters { display: flex; flex-wrap: wrap; gap: 6px; align-items: center; margin: 6px 0; }
.gap-row, .candidate { border-top: 1px solid var(--line); margin-top: 16px; }
.rule { padding: 6px 12px; border: 2px dashed var(--hold); border-radius: 4px; }
tr.changed { background: #fff5d6; }
table.whatif-table td:first-child code { white-space: nowrap; }
.ok { color: var(--allow); font-weight: 600; }
.bad { color: var(--block); font-weight: 600; }
select { font: inherit; max-width: 100%; }
"""

KB_JS = """
(function () {
  var want = {status: "", language: ""};
  function all(sel) { return Array.prototype.slice.call(document.querySelectorAll(sel)); }
  function show() {
    var n = 0;
    all("table.kb tbody tr").forEach(function (tr) {
      var on = (!want.status || tr.dataset.status === want.status) && (!want.language || tr.dataset.language === want.language);
      tr.style.display = on ? "" : "none";
      if (on) { n += 1; }
    });
    all("button[data-filter]").forEach(function (b) { b.classList.toggle("on", want[b.dataset.filter] === b.dataset.value); });
    document.getElementById("shown").textContent = n + " shown";
  }
  all("button[data-filter]").forEach(function (b) {
    b.addEventListener("click", function () { want[b.dataset.filter] = b.dataset.value; show(); });
  });
  show();
})();
"""

# The chain as onyx/audit.py defines it, in JavaScript. parse() keeps each number as its source text, so canonical()
# writes it exactly as Python did; strings and keys go through JSON.stringify; keys sort by code point, as Python's.
CHAIN_JS = """
var GENESIS = "0000000000000000000000000000000000000000000000000000000000000000";
function parse(src) {
  var i = 0, NUM = /-?\\d+(?:\\.\\d+)?(?:[eE][+-]?\\d+)?|true|false|null/y;
  function ws() { while (i < src.length && " \\t\\r\\n".indexOf(src[i]) >= 0) { i += 1; } }
  function str() {
    var start = i;
    i += 1;
    while (src[i] !== '"') { i += src[i] === "\\\\" ? 2 : 1; if (i >= src.length) { throw new Error("unterminated string"); } }
    i += 1;
    return JSON.parse(src.slice(start, i));
  }
  function value() {
    ws();
    var c = src[i];
    if (c === "{") {
      i += 1; var pairs = []; ws();
      if (src[i] === "}") { i += 1; return {t: "o", v: pairs}; }
      for (;;) {
        ws(); var k = str(); ws();
        if (src[i] !== ":") { throw new Error("expected : at " + i); }
        i += 1; pairs.push([k, value()]); ws();
        c = src[i]; i += 1;
        if (c === "}") { return {t: "o", v: pairs}; }
        if (c !== ",") { throw new Error("expected , or } at " + (i - 1)); }
      }
    }
    if (c === "[") {
      i += 1; var items = []; ws();
      if (src[i] === "]") { i += 1; return {t: "a", v: items}; }
      for (;;) {
        items.push(value()); ws();
        c = src[i]; i += 1;
        if (c === "]") { return {t: "a", v: items}; }
        if (c !== ",") { throw new Error("expected , or ] at " + (i - 1)); }
      }
    }
    if (c === '"') { return {t: "s", v: str()}; }
    NUM.lastIndex = i;
    var m = NUM.exec(src);
    if (!m) { throw new Error("unexpected character at " + i); }
    i += m[0].length;
    return {t: "n", v: m[0]};
  }
  var out = value(); ws();
  if (i !== src.length) { throw new Error("trailing text at " + i); }
  return out;
}
function byCodePoint(a, b) {
  var x = Array.from(a[0]), y = Array.from(b[0]);
  for (var j = 0; j < Math.min(x.length, y.length); j += 1) {
    var d = x[j].codePointAt(0) - y[j].codePointAt(0);
    if (d) { return d; }
  }
  return x.length - y.length;
}
function canonical(node) {
  if (node.t === "n") { return node.v; }
  if (node.t === "s") { return JSON.stringify(node.v); }
  if (node.t === "a") { return "[" + node.v.map(canonical).join(",") + "]"; }
  return "{" + node.v.slice().sort(byCodePoint).map(function (p) {
    return JSON.stringify(p[0]) + ":" + canonical(p[1]);
  }).join(",") + "}";
}
function field(node, key) {
  var hit = node.v.filter(function (p) { return p[0] === key; })[0];
  return hit ? (hit[1].t === "s" ? hit[1].v : hit[1].t === "n" ? Number(hit[1].v) : null) : null;
}
// one row per line: the stored and recomputed hash, and ok when seq, prev_hash and hash all chain (audit.first_break)
async function chainRows(text, sha) {
  var rows = [], prev = GENESIS, lines = text.split("\\n").filter(function (l) { return l.length; });
  for (var n = 0; n < lines.length; n += 1) {
    var node = parse(lines[n]);
    var body = {t: "o", v: node.v.filter(function (p) { return p[0] !== "hash"; })};
    var stored = field(node, "hash"), canon = canonical(body);
    var computed = await sha(prev + canon);
    rows.push({seq: field(node, "seq"), action: field(node, "action"), stored: stored, computed: computed,
               canonical: canon, ok: field(node, "seq") === n + 1 && field(node, "prev_hash") === prev && stored === computed});
    prev = stored;
  }
  return rows;
}
"""

VERIFY_JS = """
(function () {
  var logs = JSON.parse(document.getElementById("logs").textContent);
  var select = document.getElementById("log");
  function hex(buf) { return Array.from(new Uint8Array(buf)).map(function (b) { return b.toString(16).padStart(2, "0"); }).join(""); }
  function sha(s) { return crypto.subtle.digest("SHA-256", new TextEncoder().encode(s)).then(hex); }
  function cell(text, cls) { var td = document.createElement("td"); td.textContent = text; if (cls) { td.className = cls; } return td; }
  function command() { document.getElementById("cmd").textContent = "python -m onyx verify-log " + select.value; }
  async function run() {
    var name = select.value, summary = document.getElementById("summary"), body = document.getElementById("rows");
    command();
    body.textContent = "";
    if (!(window.crypto && crypto.subtle)) {
      summary.className = "lead bad";
      summary.textContent = "This browser gives no WebCrypto here; run the command above instead.";
      return;
    }
    summary.className = "lead";
    summary.textContent = "Verifying " + name + "...";
    var rows;
    try { rows = await chainRows(logs[name], sha); }
    catch (err) { summary.className = "lead bad"; summary.textContent = "Could not read the log: " + err.message; return; }
    var first = rows.findIndex(function (r) { return !r.ok; });
    rows.forEach(function (r) {
      var tr = document.createElement("tr");
      tr.appendChild(cell(String(r.seq)));
      tr.appendChild(cell(r.action));
      tr.appendChild(cell(r.stored, "sha"));
      tr.appendChild(cell(r.computed, "sha"));
      tr.appendChild(cell(r.ok ? "match" : "BROKEN", r.ok ? "ok" : "bad"));
      body.appendChild(tr);
    });
    if (first < 0) {
      summary.className = "lead ok";
      summary.textContent = "Chain ok: " + rows.length + " events, every hash recomputed and matched. Final hash " +
        rows[rows.length - 1].computed + ".";
    } else {
      summary.className = "lead bad";
      summary.textContent = "Chain broken: first broken seq " + (first + 1) + " of " + rows.length + ".";
    }
  }
  document.getElementById("go").addEventListener("click", run);
  select.addEventListener("change", command);
  var wanted = decodeURIComponent(location.hash.slice(1));
  if (wanted && logs[wanted]) { select.value = wanted; run(); } else { command(); }
  window.addEventListener("hashchange", function () {
    var name = decodeURIComponent(location.hash.slice(1));
    if (logs[name]) { select.value = name; run(); }
  });
})();
"""
