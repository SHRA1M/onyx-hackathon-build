# Order: Task 18, the report at five pages, two README blocks (hq, Fable, 2026-10-23)

Build model: Opus 5.5. No model calls; USD 0. Starts from 8cd6727 (CI green, run 39984374759). Copy this file into
`docs/work-orders/2026-10-23-task-18-report-five-pages.md` first. Nothing here changes the gate, the keys, the
scorer, the chunks, the register, any committed run or any figure in `eval/results.md`. Sources allowed: this repo
and the one hq file named in item 1; if it is missing, stop.

Why: Task 12 built the report at 9 pages, 3,241 words; the limit is five pages (checklist section 5, event page).
hq rewrote the text and dry-built it on this repo's `docs/build_report.py` with the rendering below simulated
(tables at 10 pt, figures at the sizes in item 3): Word counted **5 pages, 2,175 words**. The same text with
Figure 2 at 6 cm tall counted 6 pages, so the sizes in item 3 are not optional. Expected result: 5 pages with the
ladder in item 4 unused.

## Items

1. **Replace the report text.** Copy `D:\Projects\hq\uni\ai-for-good-hackathon\report-draft-2026-10-23.md` from its
   title line (`# AI for Good Sandbox Hackathon – Onyx – Mizan`) to the end over `docs/report.md`; the notes above
   the `---` stay in hq. Changes a reader will notice, all wording: requirement ids per node (SRC-1 to SB-1) in
   "Use case requirement", cited in the mapping table and the scenarios; MLFO and ML sandbox rows in the mapping
   table; "Limits and next steps" now ends with the reuse paragraph naming ITU's three vehicles; both figure
   markers now sit after the text that precedes them in reading order (Figure 1 after the mapping table's closing
   paragraph, Figure 2 after the Results paragraph), so a figure never strands a page. Every tagged value is as in
   Task 12; the value check must pass unchanged. "Limits and next steps" is still a seventh heading in the markdown
   and still folds into section 6 as Task 12 item 2 says.
2. **Builder rendering (`docs/build_report.py`).** (a) Table cells: every run 10 pt, every cell paragraph 0 pt
   space before and after; header row bold as now; widths by `_widths` as now. (b) `FIGURE_WIDTH`: both figures
   16 cm. (c) The paragraph holding a picture gets keep-with-next, so the caption stays under its image. (d) The
   six heading paragraphs get keep-with-next if the template's style does not already set it. Nothing else in the
   builder changes; two builds stay byte-identical.
3. **Figures (`scripts/fig_architecture.py`, `scripts/fig_results.py`).** Both scripts drop the caption drawn inside
   the image (`CAPTION`, `CAPTION_A`, `CAPTION_B`); the Word caption under each figure carries that text. Labels
   stay exactly as `tests/test_figures.py` checks them against the README mapping table; fonts no smaller than
   6.5 pt.
   - Figure 1: landscape, 16 cm wide by at most 4.5 cm tall. The chain SRC, C, PP, M, P, D, SINK runs left to right;
     MLFO is a wide box above the chain with its dashed arrows down; ML sandbox is a dashed box below the chain;
     the hand-over arrow leaves D downward or to the right with its label "hand-over to a human (gap-8)"; P keeps
     its heavier border. Each box keeps its node name and its one short line.
   - Figure 2: panels (a) and (b) side by side, 16 cm wide by at most 5 cm tall, each with its title, legend above
     the axes, and the same bars, ranges and markers as now. If the x labels or legends cannot fit at 6.5 pt without
     overlap, draw panel (b) alone at 16 by 5 cm and say so in the report-back; (a)'s figures are in the Results
     paragraph.
   - Record the rendered height of each PNG in the report-back. Tests: `test_figure_1_carries_the_hand_over_arrow_and_caption`
     and `test_figure_2_captions` change to assert the caption text is absent from the SVG; every other figure test
     stays.
4. **Five-page check.** Build, then run `scripts/report_pages.ps1`. Five or fewer: record pages and words in the
   report-back and go on. Six: apply the ladder below one step at a time, rebuilding and recounting after each, and
   record which steps were used. Four or fewer: stop and report, something rendered wrong.
   1. Drop the paragraph beginning **A judge's added step**.
   2. In "Limits and next steps", drop the last sentence, "The gates, scenarios and keys are offered to TDRA as a
      test bench for any licensee's consumer-facing AI agent."
   3. Figure 2 becomes panel (b) alone, 16 by 4.5 cm; the caption keeps only its (b) clause.
   4. In "Description of the use case", drop the last sentence of the first paragraph, from "The existing
      protections stop short" to "(gap 1)."
   5. Still six: stop and report the count and the first sentence on page 6; hq cuts.
5. **README, "For the reviewer" block.** Directly under the synthetic-data notice, before the paragraph "Mizan puts a
   consumer on the line", add:

   ```
   ## For the reviewer

   The four published criteria, each with the one place that shows it:

   1. Knowledge base: `kb/manifest.csv` (40 rows, status, sha256, both languages); `python -m onyx kb verify` prints the counts; the downloadable copy is `kb/export/InputDocs/Inputs.md`.
   2. Agent capability in error scenarios, and the gaps: `docs/replay/index.html` (five recorded runs, every step with its clause, page and words; no install, no key); the gap register below and `docs/gaps.md`.
   3. Auditability: `uv run python -m onyx selftest` recomputes every figure in `docs/report.docx` from the committed hash-chained logs in `runs/`; `uv run python -m onyx replay runs/c5/S2/ar/run1.jsonl` re-decides one run offline.
   4. ITU-T Y.3172 and the Readiness Framework: `docs/report.docx`, sections 3 and 4, and the Y.3172 mapping table below.
   ```

   If any path or command in the block does not exist or does not run from a fresh clone, stop and say which.
6. **README, one provenance sentence** at the end of the "Knowledge base" paragraph (the one that starts
   "Knowledge base: 36 VERIFIED"): "The Telecommunications Law 3/2003 is read from the federal legislation
   portal's consolidated texts, English and Arabic, with their text layers (no OCR); Arabic prevails, and Art 14(3)
   is quoted from the Arabic because the portal's English mistranslates it (manifest notes)." Check the two
   manifest rows (`telecom-law-3-2003-en`, `-ar`) say what the sentence says before adding it; if they do not, stop
   and quote the rows.
7. **Tests fail first then pass:** the builder sets 10 pt and zero spacing in every table cell; both pictures are
   16 cm wide and their paragraphs keep with next; the two figure SVGs carry no caption text; the README has the
   "For the reviewer" heading with four numbered lines and the provenance sentence. CI builds the docx and runs the
   figure scripts as now. Full suite, CI green, commit, push. Report under 12 lines to
   `docs/report-back/2026-10-23-task-18-report-five-pages.md`: pages, words, each figure's rendered size, ladder
   steps used (none expected), whether Figure 2 kept both panels, test count.

## Stop and ask when

- The value check fails on any paragraph of the new `docs/report.md` (quote the paragraph and the token).
- The ladder reaches step 5.
- Figure 2's labels cannot fit at 6.5 pt even with panel (b) alone.
- A README path or command in item 5 does not exist, or the manifest rows contradict item 6.
- Anything would change a figure in `eval/results.md`, a run, the scorer, the keys, the gate or the register.
