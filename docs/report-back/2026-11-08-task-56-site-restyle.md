# Report-back: Task 56, site restyle, look only (2026-11-08, Opus)

Order: `docs/work-orders/2026-11-08-task-56-site-restyle.md` (copy of `D:\Projects\hq\uni\ai-for-good-hackathon\task-56-site-restyle-order-2026-11-08.md`). Branch `task-56` from local `main` (bd3cc6e). No model call.

## In plain words

The overview now opens on a plain block: "Mizan", one line on what it is, and three cards (the AI proposes, the code decides, a person has the final word). All eight pages share one calm style: a pill nav with the current page marked, a 960 px column, roomier lines, right-aligned numbers, light and dark. No figure, label, link or footnote moved, except the hero words the order gave.

## What was built

1. `onyx/site.py` only (plus the generated `docs/site/*.html` and two screenshots).
   - Hero on `index.html`, words exactly as order item 1, held in `HERO_LINE`, `HERO_STEPS`, `HERO_FOOT`. The step numbers 1 to 3 come from a CSS counter, so they add no words to the page.
   - Old H1 "Mizan: governed consumer-care agents" and the "Five agents propose JSON actions..." paragraph removed. `NOTICE` and `SENTENCE` unchanged, below the hero.
   - Overview order: hero, page cards (same labels and lines), the three figure tables, knowledge-base counts, then Definitions folded in a closed `<details>` with the same text.
   - A small inline script opens the Definitions box when a footnote link (`#def-...`) is followed, so the superscript links still land on their definition.
   - Nav: current page gets `aria-current="page"` and an accent pill.
   - `SITE_CSS` rewritten: one accent colour (`#0b5cad` light, `#6cb0f5` dark); verdict colours unchanged in meaning; `prefers-color-scheme: dark` palette; body max width 992 px (960 px content plus the 16 px gutters already in `html_kit.CSS`); line height 1.65; overview figure tables `table-layout: fixed`, the English and Arabic columns 9em wide on all three; numbers and their headings right-aligned; equal-height cards (CSS grid); wide tables scroll inside `.tablewrap`; on the verify page the hash table keeps a 640 px minimum and scrolls in its box on a phone, and the summary line wraps its 64-character hash.
2. `onyx/html_kit.py` and `onyx/replay_viewer.py` not touched. Everything is overridden in `SITE_CSS`, so `docs/replay/` is unchanged.

## Differs from the order, and why

- A pre-existing bug fixed in passing: `td.num { text-align: end }` was outranked by `table.grid td { text-align: start }`, so the overview numbers sat left before. The selector is now `table.grid td.num`. This is the order's "numbers right-aligned", not a new item.
- No `CHANGELOG.md` entry: the order's file list (done means 3) names only `onyx/site.py`, the site, the screenshots, the order copy and this file. hq to say if it wants one added.
- The PR also carries commit bd3cc6e (the eighty-eighth wrap), because `task-56` branches from local `main`, which was one commit ahead of origin. `main` itself was not pushed.

## Checks (done means)

### 1. `uv run pytest -q`

```
1178 passed in 425.80s (0:07:05)
```

`tests/test_site.py` included (the pinned-bytes test passes after `python -m onyx site`).

### 2. `python -m onyx selftest`

```
Ungoverned baseline: C3, runs/ungoverned (30 runs), ungoverned claims allowed per run: S1 en 3, S1 ar 3, S2 en 2, S2 ar 2, S3 en 2 to 3, S3 ar 2 to 3, S4 en 2, S4 ar 1 to 2, S5 en 2, S5 ar 2
figures match a fresh eval of runs/
selftest exit 0
```

### 3. `git status` and `git diff --stat` (before this file and the commit)

```
 M docs/site/gaps.html
 M docs/site/index.html
 M docs/site/kb.html
 M docs/site/localmodel.html
 M docs/site/modeldown.html
 M docs/site/runs.html
 M docs/site/screenshots/index.png
 M docs/site/screenshots/verify.png
 M docs/site/verify.html
 M docs/site/whatif.html
 M onyx/site.py
?? docs/report-back/task-56-shots/
?? docs/work-orders/2026-11-08-task-56-site-restyle.md

 docs/site/gaps.html              |  99 ++++++++++++++++++++-------
 docs/site/index.html             | 124 ++++++++++++++++++++++++++--------
 docs/site/kb.html                |  99 ++++++++++++++++++++-------
 docs/site/localmodel.html        |  99 ++++++++++++++++++++-------
 docs/site/modeldown.html         |  99 ++++++++++++++++++++-------
 docs/site/runs.html              |  99 ++++++++++++++++++++-------
 docs/site/screenshots/index.png  | Bin 100751 -> 116449 bytes
 docs/site/screenshots/verify.png | Bin 101280 -> 110348 bytes
 docs/site/verify.html            |  99 ++++++++++++++++++++-------
 docs/site/whatif.html            |  99 ++++++++++++++++++++-------
 onyx/site.py                     | 142 ++++++++++++++++++++++++++++++---------
 11 files changed, 731 insertions(+), 228 deletions(-)
```

`git diff --stat docs/replay`: empty (printed nothing). The screenshots are 1280x1400 and 1280x900, as before.

### 4. Visible words, old against new (tags, scripts and styles stripped)

```
gaps.html: visible words identical
index.html: differs
  replace
    - Mizan: governed consumer-care agents
    + Mizan A customer-care AI for a UAE telecom operator that stays inside the law. The AI proposes.An AI agent drafts each step: a reply, a refund, a warning.The code decides.Plain code checks the step against UAE law and answers allow, hold for a staff member, or block.A person has the final word.A named staff member takes every complaint and approves what is held. Tested on a fictional operator with real UAE laws, in English and Arabic. Every step is written to a log you can check on this site.
  delete
    - Five agents propose JSON actions; plain-code gates decide from clauses of binding UAE text, in English and Arabic; every step goes to a hash-chained log you can verify on this site.
    +
kb.html: visible words identical
localmodel.html: visible words identical
modeldown.html: visible words identical
runs.html: visible words identical
verify.html: visible words identical
whatif.html: visible words identical
```

("proposes.An" is the stripper joining two block elements; on the page they are separate lines.) The "Definitions" heading became the `<summary>` of the closed box: same word, so it does not show in the diff.

### 5. Screenshots (light, Playwright, true 1280 and 390 px viewports)

- `docs/report-back/task-56-shots/index-desktop.png`, `index-phone.png`
- `docs/report-back/task-56-shots/runs-desktop.png`, `runs-phone.png`
- `docs/report-back/task-56-shots/gaps-desktop.png`, `gaps-phone.png`
- `docs/report-back/task-56-shots/verify-desktop.png`, `verify-phone.png`
- Extra, dark mode: `index-desktop-dark.png`, `index-phone-dark.png`

No sideways page scroll: page width measured on all eight pages, light and dark, at 1280 and 390. Every page fits (at 390 the page is 375 px wide inside a 390 viewport; one first pass found the verify page at 630 px, fixed as above).

### 6. PR

Opened from `task-56`, not merged: https://github.com/SHRA1M/onyx-hackathon-build/pull/26

## Open questions for hq

1. Does hq want a `CHANGELOG.md` line for this restyle (left out to match the order's file list)?
2. The README's "Open the site" screenshots are now the new look; the README text itself is the next task, as the order says.
