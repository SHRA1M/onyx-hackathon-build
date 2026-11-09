# Report-back: Task 56d, display fix on the runs page

Order: `D:\Projects\hq\uni\ai-for-good-hackathon\task-56d-display-fixes-order-2026-11-08.md`. Branch `task-56`, PR #26, not merged. Commit `2bb02bd`.

## What changed

- `onyx/replay_viewer.py`, `Viewer.answer`: the fold summary "Gate on <verb>: <verdict>" now prints the verdict as plain text (same word), no coloured pill. The coloured answer label ("Blocked" etc.) is the one coloured mark per gate line.
- `docs/site/runs.html` and `docs/replay/index.html` rebuilt (`python -m onyx site`, `python -m onyx replay-page --html`).
- `tests/test_replay_viewer.py`: `test_every_verdict_word_is_one_of_four_with_its_colour` pinned the old pill (it required all four pills on the page). Moved to the answer labels: each label is one of the four words with its colour, all four appear. New test `test_gate_summary_verdict_has_no_colour_of_its_own`. No visible word changed, so no stop.
- Arabic text and quote markup untouched. No model call, no figure change.

## Checks

- `uv run pytest -q`: `1179 passed in 392.82s`.
- `uv run python -m onyx selftest`: exit 0, last line "figures match a fresh eval of runs/".
- Visible words (scripts and styles stripped), HEAD vs new:
  - `docs/site/runs.html`: before 26512, after 26512, lost 0, added 0
  - `docs/replay/index.html`: before 26277, after 26277, lost 0, added 0
- Pills left in gate summaries: 0 in both pages (was 79 in the replay page).
- Screenshots, S2 step 3, light: `docs/report-back/task-56d-shots/runs-S2-step3-{en,ar}-{1920,390}-light.png`.

## Open questions for hq

None.
