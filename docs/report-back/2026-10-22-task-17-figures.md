# Report-back: Task 17, figures and README screenshot (2026-10-22, Opus)

1. Built: `scripts/fig_architecture.py` and `scripts/fig_results.py` (matplotlib only, added to dev extras); `docs/fig/fig1-architecture` and `fig2-results` (.png, .svg); README image line under "Three things to look at first"; CI runs both scripts before `git diff --exit-code`.
2. Figure 1: each node's line is a phrase taken word for word from the README "in Mizan" cell (tested), shortened to fit 8 cm (for example D: "the human hand-over").
3. Figure 2: (a) C5 cells, caption as ordered; (b) C3 per ruling 1, rejection as a bar to its minimum with the range hatched above, claims allowed as circles joined over their range on a 0 to 4 right axis.
4. Screenshots: both predated Task 16, so both were retaken at 1280 px from a localhost copy of `docs/replay/index.html` (the browser tool blocks file://). Both now show p. 65. The tool did not say whether its browser ran headless.
5. Item 4 skipped per ruling 2: Task 12 places Figure 1 after the mapping section and Figure 2 in the evaluation section, with the captions from the scripts.
6. Tests: `tests/test_figures.py` (10, failed first): bytes on rerun and against the committed files, panel values against a separate parse of `eval/results.md`, a missing row exits with its scenario and language, captions, README line, CI order. Full suite 329 passed.
7. Merge danger: two-way door. Blast radius: new files plus one README line and two CI steps. No change to gate, keys, runs or figures in `eval/`.
8. Open for hq: if CI on Linux renders PNG bytes that differ from Windows, the CI diff fails. I would then compare only the SVG in CI, which is a ruling for hq.
