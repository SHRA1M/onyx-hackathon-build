"""Task 56e part A (order task-56e-present-15s-order-2026-11-08.md and its two addenda): the runs page's words."""

import re
from html import unescape

from onyx import gate, kb, replay_page, replay_viewer, runs
from onyx.agents.adviser import CHANNELS

PAGES = ("docs/site/runs.html", "docs/replay/index.html")


def _html(name: str) -> str:
    return (kb.REPO / name).read_text(encoding="utf-8")


def test_fifteen_seconds_and_no_twelve():
    for name in PAGES:
        html = _html(name)
        assert "SECS = 15" in html and "every 15 seconds" in html and "every 12" not in html


def test_where_the_customer_is_talking_names_only_the_classifier_channels():
    plain = {"business_centre": "business centre", "voice": "phone call", "app_chat": "app chat", "web": "website"}
    assert set(plain) == set(CHANNELS)
    assert replay_viewer.WHERE == f"where the customer is talking ({', '.join(plain.values()).replace(', website', ' or website')})"
    for name in PAGES:
        html = unescape(_html(name))
        plain = re.findall(r'<p class="plain-step">([^<]*)</p>', html)
        assert plain and not any("channel" in line for line in plain)  # logged messages keep their own words
        assert html.count(replay_viewer.WHERE) == 2 * 2  # S1 and S2, two languages


def test_each_label_sentence_follows_the_count_of_laws():
    viewer = replay_viewer.Viewer()
    seen = set()
    for sid in replay_page.SCENARIOS:
        for lang in runs.LANGS:
            for e in runs._events(replay_viewer.source(sid, lang)):
                if e["action"] != "gate":
                    continue
                n = len(e["clause_ids"])
                html = unescape(viewer.answer(e))
                line = re.search(r'<p class="answer-line">([^<]*)</p>', html).group(1)
                assert line == replay_viewer.answer_line(e["verdict"], n)
                assert ("law" in line.split(".")[-2]) == (n > 0 and e["verdict"] != gate.INSUFFICIENT) or \
                    e["verdict"] == gate.INSUFFICIENT
                assert (f"Show the {n} law" in html) == (n > 0)
                if "reason" in line:  # "the gate's reason is below" is true: a logged reason is on the page
                    assert '<ul class=reasons><li>' in html
                seen.add((e["verdict"], min(n, 2)))
    assert (gate.ALLOW, 0) in seen and (gate.ALLOW, 1) in seen and (gate.HOLD, 0) in seen


def test_gates_off_fold_words_and_team_note():
    html = unescape(_html("docs/site/runs.html"))
    folds = re.findall(r'<details class="ungoverned"><summary>(.*?)</summary>(.*?)</details>', html, re.S)
    assert folds and all(s == replay_viewer.GATES_OFF and b.startswith(f"<p>{replay_viewer.GATES_OFF_LEAD}</p>")
                         for s, b in folds)
    assert "Without the gates</summary>" not in html and "Nothing stopped it." not in html
    assert all("passed" not in b and "follows the law" not in b for _, b in folds)
    written = [b for _, b in folds if replay_viewer.WRITTEN in b]
    assert len(written) == 5 * 2  # S1 6, S2 5, S3 3, S4 5, S5 4, in two languages


# --- part B -------------------------------------------------------------------------------------------------------

from onyx import modeldown, site  # noqa: E402


def test_runs_page_keeps_one_line_to_more_tests_and_the_boxes_moved_whole():
    runs_html, tests_html = _html("docs/site/runs.html"), _html("docs/site/tests.html")
    assert '<section class="unseen">' not in runs_html
    assert f'{site.MORE_LINE}<a href="tests.html">More tests</a>.' in runs_html
    assert site.unseen_bank() in tests_html


def test_cards_first_and_scripts_off_shows_every_step():
    for name in PAGES + ("docs/site/modeldown.html",):
        html = _html(name)
        assert 'document.documentElement.classList.add("js")' in html and "var sid = null" in html
        assert "html:not(.js) .scenario, html:not(.js) .whatif, html:not(.js) .run, html:not(.js) .step" in html


def test_modeldown_page_is_a_scenario_from_its_own_log():
    html = unescape(_html("docs/site/modeldown.html"))
    events = modeldown.replay_events(replay_viewer.WHATIF_RUN, replay_viewer.MODELDOWN_AT)
    down = next(e for e in events if e["action"] == "model_unavailable")
    assert f"<h1>{replay_viewer.MODELDOWN_TITLE}</h1>" in html
    assert f"it failed after {down['new_value']['attempts']} tries" in html and "No live outage was run." in html
    assert "no live outage was run" in " ".join(_html("docs/annex.md").split())
    same, total, _ = modeldown.stays(runs._events(replay_viewer.WHATIF_RUN), events, replay_viewer.MODELDOWN_AT)
    assert f"{same} of {total} later decisions stayed the same" in html
    assert html.count('<p class="plain-step">') == 6 and html.count('<p class="answer-line">') > 0
    assert 'class="present" data-sid="model-down-S2"' in html and down["reason"] in html
    assert "What happened here with the gates off" not in html  # no ungoverned run was replayed
