"""Task 56c (order 2026-11-08-task-56c-site-words): the site's plain words, pinned to their sources."""

import json
import re

from onyx import data, eval as eval_mod, gate, kb, replay_page, replay_viewer, runs, site

SITE = kb.REPO / "docs" / "site"


def _page(name):
    return (SITE / name).read_text(encoding="utf-8")


def _flat(html):
    return " ".join(re.sub(r"<script.*?</script>|<style.*?</style>", "", html, flags=re.S).split())


def test_committed_pages_are_current():
    for name, html in site.render().items():
        assert _page(name) == html, name


def test_overview_carries_agents_trick_and_plan_in_order():
    html = _page("index.html")
    hero, agents, trick = html.index('class="hero"'), html.index(site.AGENTS_TEXT), html.index("We tried to trick it")
    nxt = html.index("Where Mizan goes next")
    assert hero < agents < trick < nxt and nxt > html.index('id="definitions"')
    assert "Plan, not built" in html
    for word in ("safe", "cannot be tricked"):
        assert word not in site.TRICK.lower()


def test_trick_figures_are_the_annex_figures():
    annex = " ".join((kb.REPO / "docs" / "annex.md").read_text(encoding="utf-8").split())
    assert all(fact in annex for fact in site.ANNEX_FACTS)
    assert "8 of 48" in site.TRICK and "0 of 48" in site.TRICK and "48 of 48" in site.TRICK


def test_english_only_chunks_count():
    assert site.english_only() == 84
    assert "Arabic text for the 84 clauses" in _page("index.html")


def test_written_proposal_note_on_each_pending_step():
    html = _page("runs.html")
    for sid in replay_page.SCENARIOS:
        pending = [s["n"] for s in data.load_scenario(sid)["steps"] if s.get("pending_proposal")]
        assert len(pending) == 1
        for lang in runs.LANGS:
            run = html.split(f'data-sid="{sid}" data-lang="{lang}" data-run=', 1)[1].split('<div class="run"', 1)[0]
            steps = re.findall(r'<article class="step" data-n="(\d+)".*?</article>', run, flags=re.S)
            noted = [int(m.group(1)) for m in re.finditer(r'<article class="step" data-n="(\d+)"[^>]*>\n'
                                                           r'<p class="plain-step">[^<]*</p>\n<p class="written">', run)]
            assert noted == pending, (sid, lang, steps)
    assert {(1, "S1", 6), (1, "S2", 5), (1, "S3", 3), (1, "S4", 5), (1, "S5", 4)} == {
        (1, sid, n) for sid in replay_page.SCENARIOS for n in
        [s["n"] for s in data.load_scenario(sid)["steps"] if s.get("pending_proposal")]}


def test_every_step_has_a_plain_line_and_story_quotes_first_message():
    html = _page("runs.html")
    for sid in replay_page.SCENARIOS:
        scenario = data.load_scenario(sid)
        assert {n for (s, n) in replay_viewer.STEP_LINES if s == sid} == {s["n"] for s in scenario["steps"]}
        first = next(s["text_en"] for s in scenario["steps"] if s["from"] == "subscriber")
        from html import escape
        assert f"The customer says: '{escape(first)}'" in html
        assert f"Click Present to start {sid}" in html


def test_plain_figure_lines_equal_the_eval():
    viewer = replay_viewer.Viewer()
    knowledge, by_chunk = gate.Knowledge.load(), eval_mod._rules_by_chunk()
    html = _page("runs.html")
    for sid in replay_page.SCENARIOS:
        for lang in runs.LANGS:
            path = replay_viewer.source(sid, lang)
            m = eval_mod.run_metrics(path, data.load_key(sid), data.load_scenario(sid), knowledge, by_chunk)
            line = viewer.plain_figures(path, m)
            assert line in html.replace("&#x27;", "'")
            hits = eval_mod.action_hits(runs._events(path), data.load_key(sid), data.load_scenario(sid))
            assert round(sum(hits.values()) / len(hits), 4) == m["action_recall"]
            free = runs.run_path(replay_page.RUNS, sid, 1, lang, governed=False)
            n = eval_mod.run_metrics(free, data.load_key(sid), data.load_scenario(sid), knowledge,
                                     by_chunk)["ungoverned_claims_allowed"]
            assert f"Same conversation with the gates off: {n} action" in html


def test_unseen_boxes_and_old_heading_gone():
    html = _page("tests.html")  # Task 56e item 6: the boxes moved to the More tests page
    assert "The unseen bank" not in html and "The unseen bank" not in _page("runs.html")
    assert "Next tests: seven new stories, not run yet" in html
    assert "The attack test: a customer tries to trick Mizan" in html


def test_no_present_seconds_box_and_fifteen_seconds():
    for html in (_page("runs.html"), (kb.REPO / "docs" / "replay" / "index.html").read_text(encoding="utf-8")):
        assert 'id="secs"' not in html and "seconds per step" not in html
        assert "SECS = 15" in html  # Task 56e item 1


def test_no_em_dash_and_no_arabic_added():
    old_ar = set()
    for sid in replay_page.SCENARIOS:
        old_ar.add(data.load_scenario(sid)["title_ar"])
    for words in (site.AGENTS_TEXT, site.TRICK, site.NEXT_LEAD, *site.NEXT_STEPS, site.VERIFY_PLAIN,
                  site.LOCAL_PLAIN, site.UNSEEN_TEXT, site.U8_TEXT, replay_viewer.WRITTEN, replay_viewer.SAHAB,
                  replay_viewer.START, replay_viewer.TOP, replay_viewer.PLAY, *replay_viewer.PLAIN_TITLES.values(),
                  *replay_viewer.STORY_TEST.values(), *replay_viewer.STEP_LINES.values()):
        assert "—" not in words and not kb._is_arabic(words), words


def test_whatif_story_and_columns():
    html = _page("whatif.html")
    assert html.index('class="lead"') < html.index('class="beforeafter"') < html.index("Decision by decision")
    assert "within 2 minutes" in html and "8 of 10 decisions stay the same" in html


def test_localmodel_label_and_gap_5():
    html = _page("localmodel.html")
    assert "Demo, not scored" in html and "gap 5" in html and "it does not close it" in html
    assert json.dumps(True)
