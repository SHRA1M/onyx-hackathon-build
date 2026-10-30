"""Task 25 (order 2026-10-25-task-25-site): `python -m onyx site` writes docs/site/, six static pages rendered from
the committed data. Stable bytes; every figure on index.html equals eval/results.json; kb.html has one row per
manifest row; gaps.html has the 11 register gaps and the candidates; verify.html carries every C3, C4 and C5 log
and recomputes the hash chain in the browser with a canonical JSON that equals Python's byte for byte."""

import collections
import contextlib
import io
import json
import shutil
import subprocess
from html.parser import HTMLParser

import pytest

from onyx import audit, data, kb, site, whatif
from onyx.__main__ import build_parser

PAGES = ("index.html", "runs.html", "gaps.html", "kb.html", "verify.html", "whatif.html", "modeldown.html")


class Page(HTMLParser):
    """Every start tag with its attributes and its text."""

    def __init__(self):
        super().__init__()
        self.stack, self.elements = [], []

    def handle_starttag(self, tag, attrs):
        if tag in {"meta", "input", "br", "link"}:
            return
        el = {"tag": tag, "attrs": dict(attrs), "text": ""}
        self.elements.append(el)
        self.stack.append(el)

    def handle_endtag(self, tag):
        while self.stack:
            if self.stack.pop()["tag"] == tag:
                break

    def handle_data(self, text):
        for el in self.stack:
            el["text"] += text


@pytest.fixture(scope="module")
def pages():
    return site.render()


def _parse(html):
    parser = Page()
    parser.feed(html)
    return parser.elements


def _with(elements, cls):
    return [e for e in elements if cls in e["attrs"].get("class", "").split()]


def _results():
    return json.loads((kb.REPO / "eval" / "results.json").read_text(encoding="utf-8"))


def test_seven_pages_linked_from_one_bar(pages):
    assert tuple(pages) == PAGES
    for name, html in pages.items():
        links = [e["attrs"]["href"] for e in _parse(html) if e["tag"] == "a" and "site-link" in
                 e["attrs"].get("class", "")]
        assert links == list(PAGES) + [site.REPO_URL], name


def test_bytes_stable_and_committed(tmp_path, pages):
    site.write(tmp_path / "a")
    site.write(tmp_path / "b")
    for name in PAGES:
        first = (tmp_path / "a" / name).read_bytes()
        assert first == (tmp_path / "b" / name).read_bytes(), name
        assert first == pages[name].encode("utf-8"), name
        assert (site.OUT / name).read_bytes() == first, f"{name}: run `python -m onyx site`"


def test_cli_has_site_command():
    assert build_parser().parse_args(["site"]).func is site._cli


def test_no_network_at_view_time(pages):
    for name, html in pages.items():
        for el in _parse(html):
            assert el["tag"] not in {"img", "iframe"} or not el["attrs"].get("src", "").startswith("http"), name
            assert not (el["tag"] == "script" and el["attrs"].get("src")), name
            assert not (el["tag"] == "link" and el["attrs"].get("href", "").startswith("http")), name


# --- index.html ----------------------------------------------------------------------------------------------------

def test_index_notice_and_sentence(pages):
    text = pages["index.html"]
    assert site.NOTICE in text and site.SENTENCE in text


def test_index_figures_equal_results_json(pages):
    results = _results()
    figs = _with(_parse(pages["index.html"]), "fig")
    seen = collections.Counter()
    for f in figs:
        a = f["attrs"]
        config, metric, lang = a["data-config"], a["data-metric"], a["data-lang"]
        value = json.loads(a["data-value"])
        if metric == "gate_rejection_rate":
            expected = results["scenarios"][a["data-sid"]]["governed"][lang]["gate_rejection_rate"]
            assert value == expected, (a["data-sid"], lang)
        elif config == "C5":
            assert value == results["c5"]["C5"]["all"][lang][metric], (metric, lang)
        else:
            assert (config, metric) == ("C3", "ungoverned_claims_allowed")
            assert value == results["c4"]["C3"]["all"][lang][metric], lang
        seen[(config, metric)] += 1
    assert seen == {("C5", m): 2 for m in site.C5_HEADLINE} | {("C3", "ungoverned_claims_allowed"): 2,
                                                                 ("C3", "gate_rejection_rate"): 10}


def test_index_definitions_from_results_md(pages):
    definitions = site.definitions()
    html = pages["index.html"]
    for metric, name in site.DEFINED_AS.items():
        assert definitions[name] and site.escape(definitions[name]) in html, metric


def test_index_counts_equal_kb_verify(pages):
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        kb.verify(print_counts=True)
    printed = out.getvalue()
    counts = {e["attrs"]["data-status"]: int(e["text"]) for e in _with(_parse(pages["index.html"]), "count")}
    for status in ("VERIFIED", "REFERENCED", "UNVERIFIED"):
        assert f"{status} {counts[status]}" in printed, status
    assert counts["documents"] == len(kb.load_manifest())


# --- kb.html -------------------------------------------------------------------------------------------------------

def test_kb_one_row_per_manifest_row(pages):
    elements = _parse(pages["kb.html"])
    rows = [e for e in elements if e["tag"] == "tr" and "data-status" in e["attrs"]]
    manifest = kb.load_manifest()
    assert [r["attrs"]["data-id"] for r in rows] == [m["document_id"] for m in manifest]
    for row, m in zip(rows, manifest):
        assert row["attrs"]["data-status"] == m["status"] and row["attrs"]["data-language"] == m["language"]
        assert m["sha256"] in row["text"]
    counts = {e["attrs"]["data-status"]: int(e["text"]) for e in _with(elements, "count")}
    assert counts == {"documents": len(manifest)} | collections.Counter(m["status"] for m in manifest)
    buttons = {(e["attrs"].get("data-filter"), e["attrs"].get("data-value")) for e in elements if e["tag"] == "button"}
    assert {("status", m["status"]) for m in manifest} | {("language", m["language"]) for m in manifest} <= buttons


# --- gaps.html -----------------------------------------------------------------------------------------------------

def test_gaps_rows_and_texts(pages):
    register = data.load_gaps()
    elements = _parse(pages["gaps.html"])
    rows = [e for e in elements if e["tag"] == "section" and "gap-row" in e["attrs"].get("class", "")]
    ids = [r["attrs"]["data-id"] for r in rows]
    assert sorted(ids) == sorted(r["id"] for r in register["gaps"])
    assert len([i for i in ids if i.startswith("gap-")]) == 12  # gap-12, order 2026-10-26 Task 27
    assert ids == site.gap_order()
    by_id = {r["id"]: r for r in register["gaps"]}
    for row in rows:
        g = by_id[row["attrs"]["data-id"]]
        for field in ("gap", "uae_position", "recommendation"):
            assert g[field] in row["text"], (g["id"], field)
        for s in g["searched"]:
            assert s["clause"] in row["text"] and s["says"] in row["text"], (g["id"], s["clause"])
        for ex in g["global_examples"]:
            assert ex["quote"] in row["text"] and ex["file"] in row["text"], (g["id"], ex["file"])
    candidates = [e for e in elements if e["tag"] == "section" and "candidate" in e["attrs"].get("class", "")]
    assert [c["attrs"]["data-name"] for c in candidates] == [c["name"] for c in register["candidates"]]


def test_gap_order_follows_the_report():
    report = (kb.REPO / "docs" / "report.md").read_text(encoding="utf-8").split("## Policy gaps", 1)[1]
    order = site.gap_order()
    in_report = [g for g in order if f"| {g.removeprefix('gap-')} |" in report]
    assert order[:len(in_report)] == in_report
    assert [report.index(f"| {g.removeprefix('gap-')} |") for g in in_report] == sorted(
        report.index(f"| {g.removeprefix('gap-')} |") for g in in_report)


# --- runs.html -----------------------------------------------------------------------------------------------------

def test_runs_page_is_the_viewer_with_verify_links(pages):
    elements = _parse(pages["runs.html"])
    shown = {e["attrs"]["data-run"] for e in elements if e["tag"] == "div" and "run" in e["attrs"].get("class", "")}
    links = {e["attrs"]["href"] for e in _with(elements, "verify")}
    assert shown and {f"verify.html#{r}" for r in shown} <= links
    logs = {audit_path for audit_path in site.verify_names()}
    assert {h.removeprefix("verify.html#") for h in links} <= logs


# --- verify.html ---------------------------------------------------------------------------------------------------

def test_verify_lists_every_c3_c4_c5_log(pages):
    names = site.verify_names()
    assert len(names) == 100
    assert sum(n.startswith("runs/c4/") for n in names) == 20 and sum(n.startswith("runs/c5/") for n in names) == 20
    elements = _parse(pages["verify.html"])
    options = [e["attrs"]["value"] for e in elements if e["tag"] == "option"]
    assert options == names
    blob = next(e for e in elements if e["attrs"].get("id") == "logs")["text"]
    logs = json.loads(blob)
    assert list(logs) == sorted(names)
    for name in names:
        assert logs[name] == (kb.REPO / name).read_text(encoding="utf-8"), name


def test_every_log_chains_in_python():
    for name in site.verify_names():
        prev = audit.GENESIS
        for line in (kb.REPO / name).read_text(encoding="utf-8").splitlines():
            event = json.loads(line)
            assert event["prev_hash"] == prev and audit.event_hash(prev, event) == event["hash"], (name, event["seq"])
            prev = event["hash"]


def _walk(value):
    if isinstance(value, dict):
        for k, v in value.items():
            yield k
            yield from _walk(v)
    elif isinstance(value, list):
        for v in value:
            yield from _walk(v)
    else:
        yield value


def test_no_value_the_page_could_write_differently():
    """The page copies every number as the log wrote it; strings and keys go through JSON.stringify, which equals
    Python's ensure_ascii=False form for every character but a lone surrogate, and keys sort by code point."""
    for name in site.verify_names():
        for line in (kb.REPO / name).read_text(encoding="utf-8").splitlines():
            for v in _walk(json.loads(line)):
                if isinstance(v, str):
                    assert not any(0xD800 <= ord(c) <= 0xDFFF for c in v), name


NODE_DRIVER = """
const fs = require("fs"), crypto = require("crypto");
%s
const sha = (s) => Promise.resolve(crypto.createHash("sha256").update(s, "utf8").digest("hex"));
(async () => {
  const out = [];
  for (const path of JSON.parse(fs.readFileSync(0, "utf8"))) {
    const rows = await chainRows(fs.readFileSync(path, "utf8"), sha);
    out.push({path, rows});
  }
  process.stdout.write(JSON.stringify(out));
})();
"""


@pytest.mark.skipif(shutil.which("node") is None, reason="Node is not on this machine")
def test_javascript_canonical_json_equals_python(tmp_path):
    script = tmp_path / "driver.js"
    script.write_text(NODE_DRIVER % site.CHAIN_JS, encoding="utf-8")
    paths = [str(kb.REPO / n) for n in site.verify_names()]
    done = subprocess.run(["node", str(script)], input=json.dumps(paths), capture_output=True, text=True,
                          encoding="utf-8", check=True)
    results = json.loads(done.stdout)
    events = 0
    for path, result in zip(paths, results, strict=True):
        lines = open(path, encoding="utf-8").read().splitlines()
        assert len(result["rows"]) == len(lines), path
        prev = audit.GENESIS
        for line, row in zip(lines, result["rows"]):
            event = json.loads(line)
            body = {k: v for k, v in event.items() if k != "hash"}
            assert row["canonical"] == audit.canonical_json(body), (path, event["seq"])
            assert row["computed"] == audit.event_hash(prev, event) == row["stored"] and row["ok"], (path, event["seq"])
            prev = event["hash"]
            events += 1
    assert events > 2000


# --- whatif.html ---------------------------------------------------------------------------------------------------

def test_whatif_side_by_side(pages):
    recorded, under, changes = whatif.replay_under(site.WHATIF_RUN, "gap-1")
    elements = _parse(pages["whatif.html"])
    rows = [e for e in elements if e["tag"] == "tr" and "data-entity" in e["attrs"]]
    assert [r["attrs"]["data-entity"] for r in rows] == [d[0] for d in recorded]
    changed = {c[0]: c for c in changes}
    for row, rec, new in zip(rows, recorded, under):
        assert row["attrs"]["data-recorded"] == rec[2] and row["attrs"]["data-whatif"] == new[2]
        assert ("changed" in row["attrs"].get("class", "")) == (rec[0] in changed)
    findings = [r["text"] for c in changes for r in c[4] if r["kind"] == "finding"]
    assert findings and all(f in pages["whatif.html"] for f in findings)
    rule = whatif.load_rule("gap-1")
    assert site.escape(rule["text_en"]) in pages["whatif.html"] and site.escape(rule["text_ar"]) in pages["whatif.html"]


TAMPER_DRIVER = """
const fs = require("fs"), crypto = require("crypto");
%s
const sha = (s) => Promise.resolve(crypto.createHash("sha256").update(s, "utf8").digest("hex"));
chainRows(fs.readFileSync(0, "utf8"), sha).then((rows) => process.stdout.write(JSON.stringify(rows.map((r) => r.ok))));
"""


@pytest.mark.skipif(shutil.which("node") is None, reason="Node is not on this machine")
def test_javascript_names_the_first_broken_event(tmp_path):
    """One character changed in event 5 breaks the chain there, as audit.first_break says."""
    lines = (kb.REPO / site.verify_names()[0]).read_text(encoding="utf-8").splitlines()
    lines[4] = lines[4].replace('"actor":"', '"actor":"x', 1)
    tampered = tmp_path / "run.jsonl"
    tampered.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    script = tmp_path / "driver.js"
    script.write_text(TAMPER_DRIVER % site.CHAIN_JS, encoding="utf-8")
    done = subprocess.run(["node", str(script)], input=tampered.read_text(encoding="utf-8"), capture_output=True,
                          text=True, encoding="utf-8", check=True)
    ok = json.loads(done.stdout)
    assert audit.first_break(tampered) == 5 and ok.index(False) + 1 == 5 and all(ok[:4])


def test_a_rows_note_shows_on_the_site_as_on_the_register_page(pages):
    """hq ruling 2026-10-26 on the Task 27 second stop, question 3: the site and docs/gaps.md never disagree."""
    elements = _parse(pages["gaps.html"])
    rows = {r["attrs"]["data-id"]: r for r in elements if r["tag"] == "section" and "gap-row" in r["attrs"].get("class", "")}
    gaps_md = (kb.REPO / "docs" / "gaps.md").read_text(encoding="utf-8")
    noted = [g for g in data.load_gaps()["gaps"] if g.get("note")]
    assert [g["id"] for g in noted] == ["gap-12"]
    for g in noted:
        assert g["note"] in rows[g["id"]]["text"] and g["note"] in gaps_md


def test_runs_page_cites_carry_binding_tags(pages):  # order 2026-10-29-task-29 Part C1
    import re
    html = pages["runs.html"]
    codes = re.findall(r"<code>[a-z0-9-]+:[^<]+</code>", html)
    tagged = re.findall(r'<code>[a-z0-9-]+:[^<]+</code>(?: \((?:<a [^>]*>)?p\. \d+(?:</a>)?\))? <span class="tag" '
                        r'data-binding="(?:binding|advisory|method)"', html)
    assert codes and len(tagged) == len(codes)


def test_kb_page_links_the_datasheet(pages):  # order 2026-10-29-task-29 Part C2
    assert '<a href="../../kb/DATASHEET.md">kb/DATASHEET.md</a>' in pages["kb.html"]
    assert (kb.REPO / "docs" / "site" / "../../kb/DATASHEET.md").resolve().exists()


def test_readme_first_screen_links_the_datasheet():
    readme = (kb.REPO / "README.md").read_text(encoding="utf-8")
    line = next(l for l in readme.splitlines() if l.startswith("1. Knowledge base:"))
    assert "`kb/export/InputDocs/Inputs.md`" in line and "`kb/DATASHEET.md`" in line
