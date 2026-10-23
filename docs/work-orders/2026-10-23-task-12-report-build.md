# Order: Task 12 part A, the report builder and four small fixes (hq, Fable, 2026-10-23)

Build model: Opus 5.5. No model calls; USD 0. Starts from 9a9577b (CI green). Copy this file into
`docs/work-orders/2026-10-23-task-12-report-build.md` first. Nothing here changes the gate, the keys, the scorer, the
chunks, any committed run or any figure in `eval/results.md`. Sources allowed: this repo, the two files named in item
1, and nothing else; if either is missing, stop. Part B (video script, judge card) comes in a later order.

Why: the report is the first thing the judges read, and two running rivals already have theirs in their repo. Ours
is a draft in hq. The rule since the work order: every number in the report is read from `eval/results.md` by a
script, never typed. The builder is that script.

## Items

1. **Inputs into the repo.** Copy `D:\Projects\hq\uni\ai-for-good-hackathon\report-template.docx` to
   `docs/report-template.docx` unchanged. Copy `D:\Projects\hq\uni\ai-for-good-hackathon\report-draft-2026-10-22.md`
   from its title line (`# AI for Good Sandbox Hackathon – Onyx – Mizan`) to the end into `docs/report.md`; the notes
   above the `---` stay in hq. From this commit on, `docs/report.md` is the report's source; hq sends wording changes
   as order lines, not as a new draft.
2. **`docs/build_report.py`** writes `docs/report.docx` from `docs/report.md` on the template. Add `python-docx` to
   the dev extras; no other new dependency. Rendering rules:
   - The template's first paragraph becomes the draft's title line, keeping the template's run formatting. The four
     header lines (team leader, members, contact, GitHub) follow as four paragraphs, label in bold as the template has
     it.
   - The six section headings keep the template's own heading paragraphs (style `ListParagraph`, numbered), in the
     template's order: Introduction; Description of the use case; Use case requirement; Mapping with ITU-T Y.3172,
     Readiness 2.0 Report, and domain-specific policies; Error scenarios; Policy gaps and standards gaps derived from
     the mapping exercise. The draft's seventh heading, "Limits and next steps", is not a template section: its
     paragraphs go at the end of section 6, the first one opening with the bold words **Limits and next steps.** and no
     heading of its own.
   - Every template example paragraph and every NOTE paragraph is removed. Body text is the template's Normal style
     (12 pt, Letter, 1-inch margins; do not change the page setup). Markdown bold becomes bold runs; nothing else from
     markdown is interpreted except tables, images and headings.
   - Markdown tables become Word tables in the template's table style, header row bold. The mapping table replaces the
     template's existing table in place; the other tables are new.
   - Figure markers: `![Figure 1](docs/fig/fig1-architecture.png)` renders the PNG 12 cm wide, centred;
     `![Figure 2](docs/fig/fig2-results.png)` 16 cm wide, centred. The italic caption line that follows each marker in
     the draft becomes a centred paragraph under the image, 10 pt. If `docs/fig/` is missing a file, fail.
   - The run-set tags in square brackets that open with `C5` or `C3` are stripped from the output. The DP Tech
     reviewer line does not exist yet; add nothing for it.
   - `core.xml` created and modified dates are fixed values, so two builds are byte-identical.
3. **Value check, the point of the script.** Parse `eval/results.md`: the Governed and Ungoverned tables (C3), the
   latency lines under each, the "C3, C4 and C5" table and the per-scenario C3 / C4 / C5 table, and the "Misses"
   line. In every draft paragraph that carries a tag, each figure token must equal a value in the named run set,
   rounded to the token's precision: a two-decimal number between 0.00 and 1.00; "N of M" (107 of 112 is 112 minus the
   Misses line's 5); a number with a unit, where ms in the file may be shown as s in the draft (7837.607 ms is 7.8 s;
   0.458 ms is 0.46 ms). A token that matches nothing fails the build and prints the paragraph and the token. A token
   that matches more than one row is fine. Untagged paragraphs are not checked (their numbers are clause ids). If a
   tagged paragraph holds a token the rule cannot classify, stop and ask; do not widen the rule.
4. **Five-page check.** Word is on this PC at `C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE`. Write
   `scripts/report_pages.ps1`: open `docs/report.docx` through Word's COM object, read `ComputeStatistics(2)` (pages),
   print the number, quit Word. Run it after the build. Five or fewer: record the count in the report-back and go on.
   More than five: stop and report the count, the word count, and the first sentence that falls on page 6; do not
   trim anything, hq trims (scenarios first). CI has no Word: CI builds the docx and runs the tests, not this script.
5. **README run names.** The replay pages for S1, S3, S4 and S5 read C3 runs (`runs/S<n>/run1.jsonl`) while the
   scored run is C5. Regenerate those four pages with `python -m onyx replay-page` from `runs/c5/S<n>/run1.jsonl`
   (the first English C5 run), update the "run read" column and the paragraph above the Scenarios table (which now
   says every page reads a C5 run, S2 the Arabic one for the reason already given), and change the two replay lines in
   "Run it without a key" to `runs/c5/S1/run1.jsonl` and `runs/c5/S2/ar/run1.jsonl`. Keep the "grounded in" column as
   it stands. If a C5 run1 does not cite the grounding clause the column names for that scenario, try run2; if neither
   does, leave that scenario on its C3 run, keep the paragraph honest about it, and say so in the report-back. The
   S2 page and the two screenshots are untouched.
6. **Candidate id.** `onyx/coordinator.py` `_candidate` writes `"id": f"candidate-{release.inject}"`, which gives
   `candidate-S1-6`; the register (`onyx/data/gaps.json`, `docs/gaps.md`) and the key (`onyx/data/keys/S1.json`,
   step 6, `gaps`) say `candidate-4-4-fixed-term-bundle`. Change: if the scenario's key names, at this inject's step,
   exactly one id beginning `candidate-`, write that id as `id` and keep the old form as `local_id`; otherwise write as
   now. Committed runs, committed `candidates.jsonl` files, the scorer and the keys are untouched; `selftest` must
   still print "figures match a fresh eval of runs/". One line in the report-back: does the scorer's gap recall match
   the S1 candidate row by id, and would a new run with this fix change S1's gap recall. Do not re-score anything.
7. **Verified, no change:** `selftest` at 9a9577b prints the C5 governed figures and names C3 only as the ungoverned
   baseline (checked by hq 2026-10-23). The "A judge's added step enters" wording is changed to "will enter" in hq's
   draft before the copy in item 1, so `docs/report.md` already carries it.
8. **Tests fail first then pass:** two builds are byte-identical; a copy of `docs/report.md` with one tagged value
   changed by 0.01 makes the build fail naming the token; the built docx has six `ListParagraph` headings in template
   order, two image parts, no template example sentence (test for "smart pen"), and no square-bracket run-set tag; the
   four regenerated replay pages name their C5 run in their "Generated by" line; the coordinator writes the register
   id for S1 step 6 against the scripted model. CI runs the build. Full suite, CI green, commit, push. Report under 12
   lines to `docs/report-back/2026-10-2X-task-12-report-build.md` with the page count from item 4.

## Stop and ask when

- A value a tagged paragraph needs is not in `eval/results.md`, or a token cannot be classified by item 3's rule.
- The docx is over five pages (item 4).
- python-docx cannot reuse the template's numbered heading paragraphs; say what it can do instead before choosing.
- Anything would change a figure, a run, the scorer, the keys, the gate or the README register.

## Rulings on the build's first stop (hq, 2026-10-23)

1. **Plain decimals (2.3, 2.1 in "What is different"): one new class.** A plain decimal outside 0.00 to 1.00 is
   matched against values of the run set the paragraph's tag names, rounded to the token's decimals (2.33 is 2.3).
   A match from another run set does not count. Nothing else widens.
2. **A single digit alone in brackets, (1) to (9), is a list marker** and is skipped. Two or more digits, or a digit
   with a unit or a decimal point inside the brackets, is still checked.

## Rulings on the build's second stop (Iyas, 2026-10-23)

Commit and push as built; CI must be green.

1. **Docx creator.** Set the docx creator to "Team Onyx" and drop the template author.
2. **Rendering choices.** Captions plain 10 pt, backticks dropped, bold header labels: all accepted.
3. **The Results paragraph.** Keep both tags, but the C3 clause (gate and model latency, 222 decisions, 156 calls)
   must match the C3 latency lines and the C5 figures must match the C5 column. If the check cannot split a
   paragraph by sub-tag, leave it as is and say so in the report-back.
4. **Five pages.** The five-page cut is hq's: a new order will replace `docs/report.md`; do not trim. The
   report-back gives pages 9, words 3,241, the page-6 sentence, and the scorer note on gap recall.
