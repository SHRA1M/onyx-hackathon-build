# Order: Task 17, two report figures and a README screenshot (hq, Fable, 2026-10-22)

Build model: Opus 5.5. No model calls; USD 0. Starts after Task 16 (c1262e5, CI green). Copy this file into
`docs/work-orders/` first. Nothing here changes the gate, keys, chunks, runs or any figure; it draws what is already
in `eval/results.md` and `docs/replay/`.

Why: the two running rivals with reports both put pictures in them (an architecture drawing, a results chart, a
screenshot of their review screen). Ours has tables only. Judges skim; a picture of the gate blocking step 3 of S2 with
the clause, its page and its words says what a page of ours says.

## Items

1. **Figure 1, architecture.** `docs/fig/fig1-architecture.png` (and the `.svg`), drawn by a committed script
   `scripts/fig_architecture.py` with matplotlib only (add it to the dev extras if missing; no other new dependency).
   Boxes for the Y.3172 nodes exactly as the README mapping table names them: SRC, C, PP, M, P, D, SINK, with MLFO
   above and the ML sandbox beside, each box carrying the Mizan name from the "in Mizan" column in one short line.
   One arrow from D labelled "hand-over to a human (gap-8)" leaving the chain, because that is our finding. Caption
   text in the script, printed under the figure: "Mizan on the Y.3172 nodes; the model proposes, the P node decides,
   D hands a complaint to a person." Black and white, readable at 8 cm wide.
2. **Figure 2, results.** `docs/fig/fig2-results.png` (and `.svg`) from `scripts/fig_results.py`, reading
   `eval/results.md`'s C5 rows only (section "C3, C4 and C5", the C5 value of each cell), never typed figures.
   Two panels: (a) action recall and citation validity per scenario, English and Arabic side by side; (b) gate
   rejection rate governed against the ungoverned run's "claims allowed" share per scenario, from the Governed and
   Ungoverned tables. Axis 0 to 1. Caption: "C5, Claude Sonnet 5.5, prompt v5, two runs per scenario per language;
   figures regenerate from the committed logs." The script fails if a value it needs is missing from the file.
3. **README screenshot.** The existing `docs/replay/screenshots/S2-step3-en.png` is embedded in the README directly
   under "Three things to look at first", with alt text "S2 step 3: the gate blocks the agent's reply and hands the
   complaint to a person, citing CPR 26.7.2, p. 65". If that file predates Task 16 and shows no page number, retake
   it from `docs/replay/index.html` with Playwright headless at 1280 px wide, English and Arabic, same file names.
4. **Report hook.** `docs/build_report.py` (Task 12) places Figure 1 after the mapping section and Figure 2 in the
   evaluation section with their captions; nothing else in the report script changes.
5. **Tests fail first then pass**: both scripts write byte-identical output on a second run; Figure 2's numbers equal
   the C5 cells in `eval/results.md` (parse the file in the test); the README contains the image line; CI runs both
   scripts. Full suite, CI green, commit, push. Report under 12 lines to
   `docs/report-back/2026-10-2X-task-17-figures.md`.

## Rulings on the build's first stop (hq, 2026-10-22)

1. **Figure 2 panel (b): option (a).** Draw the C3 Governed and Ungoverned tables as they stand: gate rejection rate
   0 to 1 with the range as a bar, claims allowed as a count on its own axis. Panel (b) carries its own caption line:
   "C3, prompt v3, three runs per scenario per language; the only governed-against-ungoverned pair on file." Panel
   (a) keeps the C5 caption. No column is added to `eval/results.md`.
2. **Item 4: option (a).** Skip it; the report-back notes it for Task 12, which places the figures when it is built.
3. Figure 1 and the screenshot go ahead as written.

## Stop and ask when

- A value Figure 2 needs is not in `eval/results.md`.
- The screenshot cannot be retaken without a model call or a key.
- Anything would change a figure, a run, the gate or the README register.
