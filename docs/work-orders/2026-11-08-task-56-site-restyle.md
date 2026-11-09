# Work order: Task 56, site restyle, look only (Opus, 2026-11-08)

Written on Opus at Iyas's override (no Fable order, Fable plan check skipped this once, his word 2026-11-08). Repo: `D:\Projects\engineering\onyx-hackathon-build`. Copy this file to `docs/work-orders/2026-11-08-task-56-site-restyle.md` first.

**One task.** Fresh branch `task-56` from local `main` (main is one commit ahead of origin, bd3cc6e; do not push main). No model call. Frozen logs, keys, `HASHES.txt`, `runs/`, `eval/` and `kb/` are never edited. The README is NOT part of this task (it is the next task, in its own session).

## Goal

Someone who has never seen Mizan opens `docs/site/index.html` and can say within 30 seconds what Mizan does. Today the overview opens on jargon ("governed consumer-care agents", "JSON actions", "hash-chained") and a wall of tables. Make all eight pages simpler, cleaner, lined up and easier to read. Same facts.

Reference for the feel (ideas only, copy no code or text): another team's demo, `https://github.com/another team/another team` (README and `another team-demo.mp4`): one clear title, a short plain explanation, roomy cards, calm colours.

The best web designer would refuse to add decoration that hides the numbers, or to change a figure to make a page look tidier.

## What to change

1. **New top block on `index.html` (the only new words allowed).** Above everything else, a plain hero with exactly this text:
   - Title: "Mizan"
   - Line: "A customer-care AI for a UAE telecom operator that stays inside the law."
   - Three short steps, side by side as cards (stacked on a phone):
     1. "The AI proposes." / "An AI agent drafts each step: a reply, a refund, a warning."
     2. "The code decides." / "Plain code checks the step against UAE law and answers allow, hold for a staff member, or block."
     3. "A person has the final word." / "A named staff member takes every complaint and approves what is held."
   - One small line under it: "Tested on a fictional operator with real UAE laws, in English and Arabic. Every step is written to a log you can check on this site."
   This block replaces the paragraph "Five agents propose JSON actions; plain-code gates decide ... verify on this site." (that line is also inexact: the fifth component, the coordinator, is plain code and proposes nothing, `onyx/coordinator.py` line 1). The H1 "Mizan: governed consumer-care agents" becomes the hero title. `NOTICE` and `SENTENCE` stay, word for word, below the hero.
2. **Overview order:** hero, then the page cards ("Runs", "Gap register", ...) as a tidy grid with the same labels and one-line descriptions, then the figure tables, then knowledge-base counts, then definitions. Definitions folded in a `<details>` titled "Definitions" (closed by default), same text.
3. **Look, all eight pages:** one consistent style: a clear top nav (current page marked), wider line spacing, a readable max width (about 960 px, tables may go wider and scroll inside their box), aligned table columns (numbers right-aligned, same widths across the three overview tables), cards with equal heights in a row, one accent colour plus the existing verdict colours (allow green, hold amber, block red, keep their meaning), light and dark both readable (`prefers-color-scheme`). Phone width works: 16 px side gutter, no sideways page scroll.
4. **Where:** `SITE_CSS` and the markup in `onyx/site.py` only. Do not edit `onyx/html_kit.py` `CSS` or `onyx/replay_viewer.py` (they also make `docs/replay/`, which must not change). Override in `SITE_CSS` instead.
5. Regenerate with `python -m onyx site`. Retake `docs/site/screenshots/index.png` and `verify.png` at the same size as now.

## Limits

- No word, figure, label, link or footnote changes anywhere, except item 1. Every `data-*` attribute on figures and counts stays (tests read them).
- No external fonts, scripts or network calls: the site must still open from disk with no server.
- Seven layers: unchanged (no prompt, gate, model or agent code touched; nothing sends text to a model).
- Fable's "no GUI before the shortlist" (2026-11-05) is about a live app. This is a static restyle of existing pages, not a live GUI (hq's reading, inferred).

## Done means (show each output in the report-back)

1. `uv run pytest -q` green, including `tests/test_site.py` (the pinned-bytes test passes after regeneration).
2. `python -m onyx selftest` green.
3. `git status` and `git diff --stat`: only `onyx/site.py`, `docs/site/*.html`, `docs/site/screenshots/*.png`, the order copy and the report-back. `docs/replay/` unchanged (show `git diff --stat docs/replay` empty).
4. A text check: strip tags from every old and new `docs/site/*.html` and diff the visible words; the only difference is the hero block (item 1), the removed "Five agents propose..." paragraph and the old H1. Print that diff.
5. Screenshots, desktop (1280 wide) and phone (390 wide), of `index.html`, `runs.html`, `gaps.html`, `verify.html`, saved under `docs/report-back/task-56-shots/`, list their paths.
6. Report-back at `docs/report-back/2026-11-08-task-56-site-restyle.md`, PR opened, not merged. Give its full path and stop.

## Stop and ask when

A test cannot pass without changing a word or a figure; the runs page cannot be restyled without editing `replay_viewer.py` or `html_kit.py`; any page's visible words differ beyond item 1.
