"""Replay viewer (order 2026-10-22-task-14-replay-viewer): `python -m onyx replay-page --html` writes
docs/replay/index.html, one self-contained page (inline CSS, inline JavaScript, the events of the runs shown inline as
JSON) that opens from file:// with no server and no network. The steps are rendered here, in plain code, from the
committed logs, rules.json and the manifest; the script only shows one step at a time. Byte-identical on every run.

Runs shown, per scenario and language: the markdown page's rule (replay_page.source). S2 reads the first C5 run in
that language whose step 3 carries the hand-over with both quotes and whose step 4 is allowed; with none (English),
the first C5 run whose step 3 carries the hand-over. In English, S1, S3, S4 and S5 show the markdown page's run (a
C5 run where one cites the grounding clauses, order 2026-10-23 Task 12 item 5, Iyas's ruling); in Arabic, C3 run 1.
Beside each, the C3 ungoverned run 1 of the same scenario and language. Figures are eval.run_metrics on those runs, never typed."""

from __future__ import annotations

import json
from html import escape
from pathlib import Path
from typing import Any

from onyx import audit, data, eval as eval_mod, gaps, gate, kb, modeldown, replay_page, runs, whatif
from onyx.html_kit import CSS, NOTICE, WORDS, inline_json
from onyx.html_kit import cite as _cite, page as _page, quote as _quote, rel as _rel, text as _text
from onyx.html_kit import tag_html as _tag, verdict as _verdict

OUT = kb.REPO / "docs" / "replay" / "index.html"
HEADLINE = ("citation_validity", "action_recall", "abstention", "gap_recall")
NAMES = {"citation_validity": "citation validity", "action_recall": "action recall", "abstention": "abstention",
         "gap_recall": "gap recall", "ungoverned_claims_allowed": "ungoverned claims allowed"}
WHATIF_RUN = replay_page.RUNS / "c5" / "S2" / "run1.jsonl"
WHATIF_LABEL = "What-if: S2 under the rule gap 1 recommends"
MODELDOWN_AT = 3
MODELDOWN_LABEL = "Model down: S2, the call at step 3 fails"


def _step3_handover(path: Path) -> bool:
    return any(_is_handover(e) for e in runs._events(path) if e["action"] == "gate" and e["entity_id"] == "S2-3-care")


def source(sid: str, lang: str) -> Path:
    """The governed run shown for a scenario in a language (module docstring)."""
    if sid == "S2":
        c5 = [p for n in (1, 2) if (p := runs.run_path(replay_page.RUNS / "c5", sid, n, lang)).exists()]
        for path in [p for p in c5 if replay_page._shows_handover(p)] + [p for p in c5 if _step3_handover(p)]:
            return path
    if lang == "en":
        return replay_page.source(sid)
    return runs.run_path(replay_page.RUNS, sid, 1, lang)


def _is_handover(e: dict[str, Any]) -> bool:
    """A block whose reasons carry both hand-over quotes: the gate stops the agent and hands the conversation over."""
    labels = {r.get("label") for r in (e["new_value"] or {}).get("reasons", []) if r.get("kind") == "quote"}
    return e["verdict"] == gate.BLOCK and replay_page.HANDOVER_QUOTES <= labels


def _fig(path: Path, metric: str, value: Any) -> str:
    shown = eval_mod._fig(value) if isinstance(value, float) else ("n/a" if value is None else str(value))
    return (f'{NAMES[metric]} <span class="fig" data-run="{_rel(path)}" data-metric="{metric}" '
            f'data-value="{escape(json.dumps(value))}">{shown}</span>')


def _steps(events: list[dict[str, Any]]) -> dict[int, list[dict[str, Any]]]:
    """The events of each step, from its release to the next."""
    out: dict[int, list[dict[str, Any]]] = {}
    n = 0
    for e in events[1:]:
        if e["action"] == "release_event":
            n = e["new_value"]["n"]
        out.setdefault(n, []).append(e)
    return out


class Viewer:
    def __init__(self, verify: str | None = None, register: str = "../site/gaps.html") -> None:
        """verify: the site's verify page (order Task 25); each run's header then links to it. None: no link.
        register: the gap register page a flagged gap links to (order Task 31 Part D)."""
        self.verify, self.register = verify, register
        self.rules = {r["id"]: r for r in data.load_rules()}
        self.urls = {d: row["url"] for d, row in kb.manifest_by_id().items()}
        self.knowledge, self.by_chunk = gate.Knowledge.load(), eval_mod._rules_by_chunk()
        self.events: dict[str, list[dict[str, Any]]] = {}

    def metrics(self, path: Path) -> dict[str, Any]:
        sid = runs._events(path)[0]["entity_id"]
        return eval_mod.run_metrics(path, data.load_key(sid), data.load_scenario(sid), self.knowledge, self.by_chunk)

    def clause(self, rule_id: str) -> str:
        rule = self.rules.get(rule_id)
        if not rule:
            return f'<li><code>{escape(rule_id)}</code></li>'
        url = self.urls.get(rule["document_id"], "")
        link = f' <a class="src" href="{escape(url)}">source</a>' if url.startswith("http") else ""
        ar = f"<br>{_quote(rule['quote_ar'], 'ar')}" if rule.get("quote_ar") else ""
        page = _page(rule["document_id"], rule["chunk"])
        page = f", {page}" if page else ""
        tag = _tag(rule["document_id"], rule["chunk"])
        return (f"<li><code>{escape(rule_id)}</code> {escape(rule['label'])}{page} {tag}{link}<br>{_quote(rule['quote'])}"
                f"{ar}</li>")

    def rule_tag(self, rule_id: str) -> str:
        rule = self.rules[rule_id]
        return _tag(rule["document_id"], rule["chunk"])

    def flagged(self, gap_ids: list[str]) -> str:
        """Each flagged gap's line, an example from elsewhere with its quote, and the register link (Task 31 D)."""
        items = []
        for e in filter(None, map(gaps.elsewhere, gap_ids)):
            item = f"<code>{escape(e['id'])}</code>: {escape(e['line'])}"
            if e["label"] is not None:  # a candidate shows its line only
                # a register quote, verbatim in kb/sources/global/ (test_gaps), not a chunk quote: its own class
                item += ("<br>Elsewhere: " + escape(e["label"]) + f': <q class="elsewhere" lang="en">{escape(e["quote"])}</q>'
                         if e["label"]
                         else "<br>" + escape(gaps.NONE_FOUND))
                item += f'<br><a href="{escape(self.register)}#{escape(e["id"])}">register: {escape(e["id"])}</a>'
            items.append(f"<li>{item}</li>")
        return f"<ul>{''.join(items)}</ul>" if items else ""

    def proposal(self, p: dict[str, Any]) -> str:
        cites = ", ".join(_cite(c) for c in p.get("clause_ids") or []) or "no clause"
        quote = f'<div class="pq">quoted: {_quote(p["quote"])}</div>' if p.get("quote") else ""
        return (f'<li class="proposal"><b>{escape(p["verb"])}</b> to {escape(str(p.get("target") or "no target"))}; '
                f"cites {cites}{quote}</li>")

    def step(self, n: int, total: int, step_events: list[dict[str, Any]], scenario: dict[str, Any],
             ungoverned: list[dict[str, Any]] | None) -> str:
        release = step_events[0]["new_value"]
        sender = next((s["from"] for s in scenario["steps"] if s["n"] == n), "coordinator")
        proposals, verdicts, notes, handover, abstain = [], [], [], "", ""
        for e in step_events[1:]:
            nv = e["new_value"] or {}
            if e["action"] == "classify_channel":
                proposals.append(f'<li class="proposal"><b>classify_channel</b>: <code>{escape(nv["channel"])}</code>'
                                 f" (plain code)</li>")
            elif e["action"] == "propose":
                proposals += [self.proposal(p) for p in nv["proposals"]]
                proposals += [f'<li class="proposal">Rejected before the gate (outside {escape(e["actor"])}\'s '
                              f'mandate): <b>{escape(p["verb"])}</b></li>' for p in nv.get("rejected", [])]
                if not nv["proposals"] and not nv.get("rejected"):
                    proposals.append(f'<li class="proposal">{escape(e["actor"])} proposed nothing</li>')
            elif e["action"] == "gate":
                verb = (e.get("old_value") or {}).get("verb") or e["entity_id"]
                clauses = "".join(self.clause(c) for c in e["clause_ids"])
                relied = f'<ul class="clauses">{clauses}</ul>' if clauses else ""
                verdicts.append(f'<li>Gate on <b>{escape(verb)}</b>: {_verdict(e["verdict"])}{relied}</li>')
                if e["verdict"] == gate.HOLD:
                    notes.append(f"<li>Hold on <b>{escape(verb)}</b>: waits for a named human; this run's log "
                                 "records no approval.</li>")
                if _is_handover(e) and not handover:
                    quotes = [r for r in nv["reasons"] if r.get("kind") == "quote"]
                    handover = ('<div class="handover"><h4>Handed to a human</h4><ul>' + "".join(
                        f"<li>{escape(r['label'])} {self.rule_tag(r['clause'])}<br>{_quote(r['en'], 'en')}<br>{_quote(r['ar'], 'ar')}</li>"
                        for r in quotes) + "</ul></div>")
            elif e["action"] == "abstain":
                gaps = ", ".join(f"<code>{escape(g)}</code>" for g in nv["gaps"]) or "none"
                abstain = (f'<div class="abstain">Insufficient evidence: logged as a candidate gap. '
                           f"Gap flagged: {gaps}{self.flagged(nv['gaps'])}</div>")
            elif e["action"] == "override_refused":
                notes.append(f"<li>Override attempt: {escape(e['reason'])}. No override.</li>")
        attempted = release["facts"].get("override_attempted_by")
        if attempted and not any(e["action"] == "override_refused" for e in step_events):
            notes.append(f"<li>Override attempt named in the step: {escape(attempted)}</li>")
        parts = [f'<article class="step" data-n="{n}" data-total="{total}">',
                 f'<h3>Step {n} of {total}: from {escape(sender)} to {escape(release["to"])}</h3>',
                 _text(release["text"], "message", "div"),
                 f'<h4>Proposals</h4><ul>{"".join(proposals) or "<li>none</li>"}</ul>',
                 f'<h4>Gate</h4><ul class="verdicts">{"".join(verdicts) or "<li>no gate event</li>"}</ul>',
                 handover, f'<ul class="notes">{"".join(notes)}</ul>' if notes else "", abstain,
                 self.without_gates(ungoverned), "</article>"]
        return "\n".join(p for p in parts if p)

    def without_gates(self, ungoverned: list[dict[str, Any]] | None) -> str:
        body = []
        if not ungoverned:
            body.append("<p>The ungoverned run has no event for this step.</p>")
        else:
            gates = [e for e in ungoverned if e["action"] == "gate"]
            for e in ungoverned:
                if e["action"] == "propose":
                    body += [f"<ul>{self.proposal(p)}</ul>" for p in e["new_value"]["proposals"]]
            body += [f"<p>{escape((e.get('old_value') or {}).get('verb') or e['entity_id'])}: {_verdict(e['verdict'])}"
                     "</p>" for e in gates]
            if gates and all(e["verdict"] == gate.ALLOW for e in gates):
                body.append("<p>Nothing stopped it.</p>")
        return '<details class="ungoverned"><summary>Without the gates</summary>' + "".join(body) + "</details>"

    def verify_link(self, path: Path) -> str:
        if not self.verify:
            return ""
        return f' <a class="button verify" href="{self.verify}#{_rel(path)}">Verify this log</a>'

    def run(self, sid: str, lang: str) -> tuple[str, str]:
        """The run's block and its headline line."""
        path = source(sid, lang)
        events = runs._events(path)
        self.events[_rel(path)] = events
        config = events[0]["new_value"]
        scenario = data.load_scenario(sid)
        free = runs.run_path(replay_page.RUNS, sid, 1, lang, governed=False)
        free_events = runs._events(free)
        self.events[_rel(free)] = free_events
        free_steps = _steps(free_events)
        metrics, free_metrics = self.metrics(path), self.metrics(free)
        steps = _steps(events)
        total = len(scenario["steps"])
        head = [f'<div class="run" data-sid="{sid}" data-lang="{lang}" data-run="{_rel(path)}">',
                f'<p class="notice">{escape(NOTICE)}</p>',
                f"<p class=\"meta\">Run <code>{_rel(path)}</code>, prompt "
                f"{escape(config.get('prompt', 'not logged (labels began with v4)'))}, model "
                f"<code>{escape(config.get('model', ''))}</code>, {escape(config.get('mode', ''))}, {lang}; "
                f"hash chain: {'ok' if audit.verify(path) else 'BROKEN'}.{self.verify_link(path)}</p>",
                f'<p class="meta">Without the gates: <code>{_rel(free)}</code>, '
                f'{_fig(free, "ungoverned_claims_allowed", free_metrics["ungoverned_claims_allowed"])} (eval).'
                f'{self.verify_link(free)}</p>']
        body = [self.step(n, total, steps[n], scenario, free_steps.get(n)) for n in sorted(steps) if n]
        headline = (f'<p class="headline" data-sid="{sid}" data-lang="{lang}">Figures for <code>{_rel(path)}</code> '
                    f"(eval.run_metrics): " + ", ".join(_fig(path, m, metrics[m]) for m in HEADLINE) + ".</p>")
        return "\n".join(head + body + ["</div>"]), headline

    def render(self, nav: str = "", css: str = CSS) -> str:
        """nav: a bar above the header (the site's, order Task 25); css: the page's styles."""
        sections, headlines, picker = [], [], []
        for sid in replay_page.SCENARIOS:
            scenario = data.load_scenario(sid)
            picker.append(f'<button data-sid="{sid}">{sid} {escape(scenario["title_en"])} '
                          f'{_text(scenario["title_ar"], lang="ar")}</button>')
            runs_html = []
            for lang in runs.LANGS:
                html, headline = self.run(sid, lang)
                runs_html.append(html)
                headlines.append(headline)
            sections.append(f'<section class="scenario" data-sid="{sid}"><h2>{sid}: {escape(scenario["title_en"])} '
                            f'{_text(scenario["title_ar"], lang="ar")}</h2>\n' + "\n".join(runs_html) + "</section>")
        # Task 19 item 2: the what-if page's text, opened from the picker, under a link to the page
        name = whatif.page_name(WHATIF_RUN, "gap-1")
        sid = name.removesuffix(".md")
        picker.append(f'<button data-sid="{sid}">{escape(WHATIF_LABEL)}</button>')
        sections.append(f'<section class="whatif" data-sid="{sid}"><h2>{escape(WHATIF_LABEL)}</h2>\n'
                        f'<p class="meta"><a href="{name}">{name}</a></p>\n'
                        f'<pre class="text" dir="auto">{escape(whatif.render(WHATIF_RUN, "gap-1"))}</pre></section>')
        # Task 29 Part A: the model-down page's text, beside the what-if
        name = modeldown.page_name(WHATIF_RUN)
        sid = name.removesuffix(".md")
        picker.append(f'<button data-sid="{sid}">{escape(MODELDOWN_LABEL)}</button>')
        sections.append(f'<section class="whatif" data-sid="{sid}"><h2>{escape(MODELDOWN_LABEL)}</h2>\n'
                        f'<p class="meta"><a href="{name}">{name}</a></p>\n'
                        f'<pre class="text" dir="auto">{escape(modeldown.render(WHATIF_RUN, MODELDOWN_AT))}</pre>'
                        "</section>")
        return TEMPLATE.format(css=css, js=JS, nav=nav, headlines="\n".join(headlines), picker="\n".join(picker),
                               sections="\n".join(sections), events=inline_json(self.events))


def render() -> str:
    return Viewer().render()


def write(out: str | Path = OUT.parent) -> Path:
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    page = out / OUT.name
    page.write_text(render(), encoding="utf-8", newline="\n")
    return page


TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Mizan replay</title>
<style>{css}</style>
</head>
<body>
{nav}<header>
<h1>Mizan replay</h1>
<div class="headlines">
{headlines}
</div>
<nav class="bar">
<span class="langs"><button data-lang="en">English</button> <button data-lang="ar">Arabic</button></span>
<span class="pos"><button id="prev">Previous</button> <span id="count"></span> <button id="next">Next</button></span>
<label class="secs">Present (key p), seconds per step <input id="secs" type="number" min="1" value="8"></label>
</nav>
<nav class="picker">
{picker}
</nav>
</header>
<main>
{sections}
</main>
<script type="application/json" id="events">{events}</script>
<script>{js}</script>
</body>
</html>
"""

JS = """
(function () {
  var sid = "S1", lang = "en", index = 0, timer = null;
  function all(sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); }
  function steps() {
    var run = document.querySelector('.run[data-sid="' + sid + '"][data-lang="' + lang + '"]');
    return run ? all(".step", run) : [];
  }
  function show() {
    all(".scenario, .whatif").forEach(function (el) { el.classList.toggle("on", el.dataset.sid === sid); });
    all(".run").forEach(function (el) { el.classList.toggle("on", el.dataset.sid === sid && el.dataset.lang === lang); });
    all(".headline").forEach(function (el) {
      el.classList.toggle("on", el.dataset.sid === sid && el.dataset.lang === lang);
    });
    all(".picker button").forEach(function (el) { el.classList.toggle("on", el.dataset.sid === sid); });
    all(".langs button").forEach(function (el) { el.classList.toggle("on", el.dataset.lang === lang); });
    var list = steps();
    index = Math.max(0, Math.min(index, list.length - 1));
    list.forEach(function (el, i) { el.classList.toggle("on", i === index); });
    document.getElementById("count").textContent = list.length ? "Step " + (index + 1) + " of " + list.length : "";
  }
  function move(delta) {
    var list = steps();
    if (delta > 0 && index >= list.length - 1) { stop(); return; }
    index += delta;
    show();
  }
  function stop() { if (timer) { clearInterval(timer); timer = null; } }
  function present() {
    var on = document.body.classList.toggle("present");
    stop();
    if (on) {
      var secs = Math.max(1, Number(document.getElementById("secs").value) || 8);
      timer = setInterval(function () { move(1); }, secs * 1000);
    }
  }
  all(".picker button").forEach(function (el) {
    el.addEventListener("click", function () { sid = el.dataset.sid; index = 0; show(); });
  });
  all(".langs button").forEach(function (el) {
    el.addEventListener("click", function () { lang = el.dataset.lang; show(); });
  });
  document.getElementById("prev").addEventListener("click", function () { move(-1); });
  document.getElementById("next").addEventListener("click", function () { move(1); });
  document.addEventListener("keydown", function (ev) {
    if (ev.target && ev.target.tagName === "INPUT") { return; }
    if (ev.key === "ArrowRight") { move(1); }
    else if (ev.key === "ArrowLeft") { move(-1); }
    else if (ev.key === "p" || ev.key === "P") { present(); }
  });
  show();
})();
"""
