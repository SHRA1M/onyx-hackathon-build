"""Task 14 (order 2026-10-22-task-14-replay-viewer): `python -m onyx replay-page --html` writes docs/replay/index.html,
one self-contained page from the committed run logs. Stable bytes, no external URL but the clause source links, five
scenario sections each with the notice, quotes verbatim from kb/chunks, the four verdict words in colour, the
hand-over panel at S2 step 3 only, and the figures equal to the eval's for the same runs."""

import json
import re
from html.parser import HTMLParser
from pathlib import Path

import pytest

from onyx import audit, data, eval as eval_mod, gate, kb, replay_page, replay_viewer, runs

NOTICE = "The operator, subscribers and numbers are synthetic; the law texts are real, linked and hashed"
VERDICTS = {"allow": "v-allow", "hold": "v-hold", "block": "v-block", "insufficient evidence": "v-insufficient"}


class Page(HTMLParser):
    """The elements the tests read: every start tag with its attributes and its text, nested by depth."""

    def __init__(self):
        super().__init__()
        self.stack, self.elements = [], []

    def handle_starttag(self, tag, attrs):
        if tag in {"meta", "input", "br", "link"}:
            return
        el = {"tag": tag, "attrs": dict(attrs), "text": "", "parents": list(self.stack)}
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
def html():
    return replay_viewer.render()


@pytest.fixture(scope="module")
def page(html):
    parser = Page()
    parser.feed(html)
    return parser.elements


def _has(el, cls):
    return cls in el["attrs"].get("class", "").split()


def _within(el, cls):
    return [p for p in el["parents"] if _has(p, cls)]


def _norm(text):
    return re.sub(r"\s+", " ", text).strip()


def test_byte_identical_on_two_runs(tmp_path):
    first, second = tmp_path / "a", tmp_path / "b"
    replay_viewer.write(first)
    replay_viewer.write(second)
    assert (first / "index.html").read_bytes() == (second / "index.html").read_bytes()


def test_committed_page_is_current(html):
    assert replay_viewer.OUT.read_text(encoding="utf-8") == html, "run `python -m onyx replay-page --html`"


def test_no_external_url_but_the_clause_source_links(html):
    rest = re.sub(r'<a class="src" href="https?://[^"]*"', "", html)
    assert "http" not in rest
    assert "fetch(" not in html and "<link" not in html and " src=" not in html
    assert len(html.encode("utf-8")) < 5_000_000


def test_five_scenario_sections_each_with_the_notice(page):
    sections = [el for el in page if _has(el, "scenario")]
    assert [s["attrs"]["data-sid"] for s in sections] == list(replay_page.SCENARIOS)
    for s in sections:
        for lang in runs.LANGS:
            run = next(el for el in page if _has(el, "run") and s in el["parents"] and el["attrs"]["data-lang"] == lang)
            assert NOTICE in _norm(run["text"])
            path = kb.REPO / run["attrs"]["data-run"]
            # Task 56c: the technical line sits in the side column; the run carries the plain line
            tech = next(el for el in page if _has(el, "run-tech") and el["attrs"]["data-sid"] == s["attrs"]["data-sid"]
                        and el["attrs"]["data-lang"] == lang)
            assert f"hash chain: {'ok' if audit.verify(path) else 'BROKEN'}" in tech["text"]
            assert ("The log is untouched." if audit.verify(path) else "The log chain is BROKEN.") in run["text"]


def test_runs_shown_agree_with_the_markdown_pages():
    for sid in replay_page.SCENARIOS:
        md = replay_page.source(sid)
        lang = "ar" if "ar" in md.relative_to(kb.REPO).parts else "en"
        assert replay_viewer.source(sid, lang) == md
    assert replay_viewer.source("S2", "en").relative_to(kb.REPO).as_posix().startswith("runs/c5/S2/")


def test_every_quote_is_verbatim_in_the_chunks(page):
    texts = {"en": [], "ar": []}
    for path in sorted((kb.REPO / "kb" / "chunks").glob("*.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            chunk = json.loads(line)
            texts["en"].append(_norm(chunk.get("text_en") or ""))
            texts["ar"].append(_norm(chunk.get("text_ar") or ""))
    quotes = [el for el in page if _has(el, "quote")]
    assert quotes
    missing = [(el["attrs"]["data-lang"], el["text"]) for el in quotes
               if not any(_norm(el["text"]) in t for t in texts[el["attrs"]["data-lang"]] if t)]
    assert missing == []


ANSWER_COLOURS = {"Allowed": "v-allow", "Held for a staff member": "v-hold", "Blocked": "v-block",
                  "Not enough evidence": "v-insufficient"}


def test_every_verdict_word_is_one_of_four_with_its_colour(page):
    """Task 56d: the gate line's one coloured mark is its answer label; the fold summary's verdict is plain text."""
    for el in (el for el in page if _has(el, "verdict")):
        assert el["text"] in VERDICTS, el["text"]
        assert _has(el, VERDICTS[el["text"]])
    answers = [el for el in page if _has(el, "answer")]
    assert answers
    for el in answers:
        assert el["text"] in ANSWER_COLOURS, el["text"]
        assert _has(el, ANSWER_COLOURS[el["text"]])
    assert {el["text"] for el in answers} == set(ANSWER_COLOURS)


def test_gate_summary_verdict_has_no_colour_of_its_own():
    html = (kb.REPO / "docs" / "replay" / "index.html").read_text(encoding="utf-8")
    # Task 56e item 3: the "Gate on" line moved inside the fold, under the label's plain sentence
    lines = re.findall(r'<p class="gate-line">Gate on <b>[^<]*</b>: ([^<]*)</p>', html)
    assert lines and set(lines) <= set(VERDICTS)
    assert not re.search(r'<p class="gate-line">Gate on <b>[^<]*</b>: <span', html)


def test_arabic_blocks_render_right_to_left(page):
    for el in page:
        if el["attrs"].get("lang") == "ar":
            assert el["attrs"].get("dir") == "rtl"
    assert any(el["attrs"].get("lang") == "ar" for el in page if _has(el, "message"))


def test_handover_panel_at_s2_step_3_only(page):
    for lang in runs.LANGS:
        steps = [el for el in page if _has(el, "step") and _within(el, "run")
                 and _within(el, "run")[0]["attrs"]["data-sid"] == "S2"
                 and _within(el, "run")[0]["attrs"]["data-lang"] == lang]
        with_panel = [s["attrs"]["data-n"] for s in steps
                      if any(_has(el, "handover") and s in el["parents"] for el in page)]
        assert with_panel == ["3"], lang


def test_headline_figures_equal_the_eval(page):
    knowledge, by_chunk = gate.Knowledge.load(), eval_mod._rules_by_chunk()
    figs = [el for el in page if _has(el, "fig")]
    shown = {(el["attrs"]["data-run"], el["attrs"]["data-metric"]) for el in figs}
    for sid in replay_page.SCENARIOS:
        for lang in runs.LANGS:
            for path, metrics in ((replay_viewer.source(sid, lang), replay_viewer.HEADLINE),
                                  (runs.run_path(replay_page.RUNS, sid, 1, lang, governed=False),
                                   ("ungoverned_claims_allowed",))):
                for metric in metrics:
                    assert (path.relative_to(kb.REPO).as_posix(), metric) in shown
    for el in figs:
        path = kb.REPO / el["attrs"]["data-run"]
        sid = runs._events(path)[0]["entity_id"]
        expected = eval_mod.run_metrics(path, data.load_key(sid), data.load_scenario(sid), knowledge,
                                        by_chunk)[el["attrs"]["data-metric"]]
        assert json.loads(el["attrs"]["data-value"]) == expected
