# Report-back: README top part (2026-11-09)

Order: `D:\Projects\hq\uni\ai-for-good-hackathon\readme-top-order-2026-11-08.md`, with its addendum. Branch `task-56`, commit `1a52558`, pushed to `task-56` (PR #26). Not merged.

## The new block (README.md, replacing old line 7, copied word for word)

1. "Mizan is a consumer-care AI for a phone company, tested on written scenarios with a fictional UAE operator, not on live customers. The AI proposes each step of a conversation; code written from binding UAE law (the gates) allows it, holds it for a staff member or blocks it, in Arabic and English, and every step goes into a log that anyone can replay."
2. "Five agents: the care agent talks to the customer, the adviser checks the law, and two agents play the regulators, TDRA and the Data Office. These four are AI. The fifth, the coordinator, is plain code that routes each step."
3. Picture `docs/site/screenshots/runs-S1-step3-held.png`, copied from 56e's `present-S1-step3-held-1280.png`. It is 1280 x 720, light, and shows S1 step 3 with "Held for a staff member" open. Alt text as in the order.
4. `<!-- film-link -->` (a comment only). "See the runs: https://shra1m.github.io/onyx-hackathon-build/site/runs.html". "Read the report: docs/report.pdf".
5. "In each of the five scored scenarios, one move was written into the test by the team, not proposed by the AI, to check the gate: S1 step 6, S2 step 5, S3 step 3, S4 step 5, S5 step 4. The runs page marks each one; the report's annex lists them."

Addendum: "## Open the site" now says "nine pages" instead of "eight pages".

## The Pages address

hq set the address in session on 2026-11-09. It was not read from a Pages setup, because the repo has none: the only workflow is `reproduce.yml`, and `gh api .../pages` returns 404. Per hq, Pages will be switched on on sending day to serve `docs/` from `main`. No workflow was added and no setting was changed.

## Checks before writing

- Steps from `pending_proposal` (field `n`): S1 6, S2 5, S3 3, S4 5, S5 4. They match the note.
- `WRITTEN` is in `onyx/replay_viewer.py:118` and is rendered on the runs page (lines 325 and 359).
- The annex sentence "Each scored scenario also carries one proposal written by the team" is on `end-check-3-annex` (PR #28), not yet on `task-56`. The order allows either branch.
- Nine pages: `docs/site/` holds 9 html files, and `tests/test_site.py` `PAGES` has 9 entries.

## Done means

- Tests: `uv run pytest -q` gives 1199 passed. The pin "eight pages" in `tests/test_task_49.py` became "nine pages", and the test was renamed to `test_readme_says_nine_pages_and_limits_the_citation_claim_to_s1`. The new `tests/test_readme_top.py` pins the block in order above "## For the reviewer". Both failed before the README edit and passed after. No test pinned old line 7.
- `python -m onyx selftest`: exit 0, ending "figures match a fresh eval of runs/".
- GitHub render on `task-56`: screenshot at `C:\Users\SUPER\AppData\Local\Temp\claude-chrome-screenshots-xYMmHY\screenshot-1794224461753-0.jpg`. The block does NOT fit in one screen. The picture fills most of the first screen. In a 911 px high viewport, the note ends at about 1348 px and "## For the reviewer" at about 1410 px, so a judge scrolls about half a screen to reach the links and the note. Viewport width was 1920 CSS px on this display, not 1280; the README column is fixed width, so the height is about the same. One option for hq: a smaller picture, or the links above it. That would change the order's sequence, so I did not do it.
- Links:
  - The report link opens `blob/task-56/docs/report.pdf` on GitHub. `docs/report.pdf` is 499,712 bytes.
  - The Pages link returns 404, as expected before sending day. The file it points to exists: `docs/site/runs.html`, 1,502,083 bytes.
  - The picture loads in the render.

## Open questions for hq

1. Is the half-screen scroll to the links and the note acceptable, or should a new order change the picture or the sequence?
2. Once PR #28 merges, the annex sentence will be on the same branch as the note.
