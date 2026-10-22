# Order: Task 14, the replay viewer (hq, Fable, 2026-10-22)

Build model: Opus 5.5. No model calls; USD 0. Starts after the C5 order (Task 13) is committed and pushed. Copy this
file into `docs/work-orders/` first.

Decision (hq, Fable, 2026-10-22, Iyas agreed): the video and the judges need to see a scenario play, and a terminal
does not read on screen. Not a dashboard and not a live console: a static HTML page generated from the committed
run logs, the same way `replay-page` writes `docs/replay/S<n>.md`. Live step entry comes with the routing step after
2026-11-18 and is not in this order.

## Sources allowed, and nothing else

The committed run logs (`runs/`), `kb/chunks/`, the eval module's figures, the existing `replay-page` code, this
order. No new text, no outside library, no CDN, no font download: everything inline in the file.

## What it is

1. **Command**: `python -m onyx replay-page --html` writes `docs/replay/index.html`, one file, self-contained: inline
   CSS, inline JavaScript, and the events of the chosen runs inline as JSON. It opens from `file://` with no server
   and no network (so no `fetch`, no external URL of any kind in the file; a test greps for `http` outside the
   clause source links and fails on any). Byte-identical on a second run; a test checks it.
2. **Runs shown**: the same run per scenario that the markdown replay pages use, so the two agree; after Task 13
   item 12, that may be a C5 run for S2. The page names the run file and its prompt version at the top of each
   scenario. For the "without the gates" panel (item 6), the C3 ungoverned run 1 of the same scenario and language.
3. **Languages**: English and Arabic runs, a switch at the top. Arabic text renders right to left (`dir="rtl"`,
   `lang="ar"` on those blocks) in a system Arabic font stack; no font file.
4. **Screen**: a scenario picker (S1 to S5, title in both languages), then one step at a time, with Previous and
   Next, the arrow keys, and the step number out of the total. Per step, in this order:
   - the message as released by the coordinator, from whom to which agent, in the run's language;
   - each proposal: verb, target, the clause ids cited, the quote;
   - the gate's verdict on each proposal in colour: allow green, hold amber, block red, insufficient evidence grey,
     with the word written out beside the colour (never colour alone);
   - the clauses the verdict relied on, with the English quote and the Arabic quote where the chunk has one;
   - on a hand-over step: a panel "Handed to a human" with both language quotes of CPR 26.7.2 and licence 9.1;
   - on a hold: the named human who approved, and the override attempt where the log has one; on the model-provider
     block: "no override" stated;
   - on an abstention: "Insufficient evidence: logged as a candidate gap" and the gap id the run flagged.
5. **Top of every scenario**: the synthetic-data notice ("The operator, subscribers and numbers are synthetic; the
   law texts are real, linked and hashed") and the hash chain result for that run ("hash chain: ok" from a real
   check at generation time, never a constant).
6. **Without the gates**: a panel per step, collapsed by default, showing what the ungoverned run proposed at the same
   step and that nothing stopped it; the count of ungoverned claims allowed for the run, read from the eval, not
   typed. Where the ungoverned run has no event for that step, the panel says so.
7. **Headline line** on the index, under the title: citation validity, action recall, abstention, gap recall, read
   from the eval module for the runs shown (the same figures `selftest` prints), with the run set named. If the eval
   has no function that returns them, leave the line out and say so in the report-back; do not type figures.
8. **Present mode**: a toggle (key `p`) that enlarges the type to about 1.4 times, hides the picker, and auto-advances
   every N seconds (N from a box, default 8). This is for the screen recording. Nothing else changes.
9. **README**: one line under "Two-minute check": "Replay viewer: open `docs/replay/index.html` in a browser
   (no server, no key)." The markdown pages stay.
10. **CI**: `reproduce.yml` runs `replay-page --html` and `git diff --exit-code` already covers the file.

## Tests, fail first then pass

- Byte-identical output on two runs; no external URL in the file; the file parses (an HTML parser finds the five
  scenario sections and the notice in each).
- Every quote in the HTML exists verbatim in `kb/chunks/` (English) or in the chunk's `text_ar` (Arabic).
- Every verdict word in the HTML is one of the four, and each carries its colour class.
- The hand-over panel appears exactly at S2 step 3 and nowhere else in S2.
- The headline figures in the HTML equal the eval's figures for the same runs.

## Report-back

Under 20 lines to `docs/report-back/2026-10-2X-task-14-replay-viewer.md`: file size, which run per scenario, what
the eval exposed for item 7, screenshots of S2 step 3 in both languages saved under `docs/replay/screenshots/`
(for the video folder, not for the README), anything that departs from this order.

## Stop and ask when

- The file would exceed 5 MB, or needs anything fetched at open time.
- The eval needs a change to expose the figures.
- A quote in a log is not found verbatim in `kb/chunks/` (that is a finding, not something to patch in the page).
- Any item needs a model call or a change to logs, keys, `rules.json` or `kb/`.

## Rulings on the report-back (hq, 2026-10-22, after Task 17)

All accepted as built; nothing to build. File these rulings into `docs/work-orders/` beside this order and clear them
from the build's background and brief.
1. S2 English shows `runs/c5/S2/run1.jsonl`, not C3 run1 (report-back item 3). Accepted: C5 is the run the report cites.
2. Headline figures are per run shown, with the run named (item 5). Accepted.
3. Holds name no approver; the page says the log records no approval (item 6). Accepted: it matches hq's decision of
   2026-10-22 that the human steps are scripted and a real approver comes after the shortlist.
