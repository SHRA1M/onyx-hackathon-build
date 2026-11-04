# Task 46 done: README diagram keyed to the Y.3172 nodes (2026-11-04)

Order `docs/work-orders/2026-11-04-task-46-readme-diagram.md`, with hq's `task-46-stop-1-ruling-2026-11-04.md`. USD 0, no
model call. PR #15 was merged first; CI "reproduce" passed on main `49bb40a` (run 41876431279) before work began, and
`task-46` was merged up to date with main with no conflict.

Plainly: a reviewer now sees Mizan's own files on the Y.3172 nodes, and a test fails if the figure and the mapping table
ever disagree.

## Done means

| # | Check | Result |
|---|---|---|
| 1 | GitHub renders the diagram in Chrome | Yes, on the branch's README; screenshot below. See "One thing seen in Chrome" |
| 2 | `tests/test_readme_diagram.py` | 17 passed; it first failed 17 of 17 before the README changed |
| 3 | `uv run pytest`; CI "reproduce" on the PR | 749 passed; CI: see the PR section at the end |
| 4 | Reviewer row points at the diagram and table | "[the Y.3172 diagram and mapping table below](#y3172-mapping)": "diagram and" added, no other text in that row changed |
| 5 | Report-back; report unchanged | This file. `docs/report.pdf`, `docs/report.docx`, `docs/report.md` and `docs/annex.md` have no diff against main; body 5 pages, annex from page 6, 12 in all; PDF 12 pages |

Screenshot: `docs/report-back/screenshots/2026-11-04-task-46-diagram.jpg`. The figure is shrunk in the browser only, so
all of it and the caption fit in one image; GitHub's page and the repo are unchanged by that.

## What was built

- One Mermaid flowchart with hq's caption, directly under `## Y.3172 mapping`, above the intro sentence and the table.
  14 boxes in the nine node subgraphs and 21 edges; the coordinator has a box in each of C, D and MLFO.
- The ML sandbox row's two cells take hq's words exactly. The README's other changed line is the reviewer row. Diff against
  main: 64 lines added, 2 removed, and those 2 are these two rows.
- `tests/test_readme_diagram.py`: the order's five checks, each also broken on purpose to prove it fails.

## What differs from the order, and why

1. hq's ruling replaces the order where they conflicted: the ML sandbox row changes, the equality check compares paths under
   `onyx/` only, SRC's box is a folder, and its one edge is a read.
2. Added to the test, beyond the order's list, because the order's rules ask for them: each edge between two files must have a
   real import behind it; solid or dotted must match the ruling; the diagram and table must agree node by node, not only
   as a whole; the caption must match hq's word for word.

## Decisions taken here, for hq to see

1. **Not every import is drawn.** The order allows only edges that exist, and does not ask for all of them. Left out to keep
   the figure readable: `onyx/model.py` to `onyx/audit.py` (used only when replaying a recorded model); coordinator to
   `onyx/model.py` and `onyx/kb.py`; `onyx/runs.py` to `onyx/audit.py` and `onyx/kb.py`; `onyx/eval.py` to `onyx/gate.py`,
   the coordinator and `onyx/runs.py`; the optional modules' imports of `onyx/audit.py`, `onyx/kb.py` and `onyx/runs.py`,
   apart from `localmodel` to `runs`, which hq named.
2. **`onyx/eval.py` to `onyx/audit.py` is solid.** It reads logs after a run, not during one, and `eval` is not one of the
   optional steps the caption names, so dotted would be false too. The local-model run is recorded and not scored, so "every
   recorded run" is looser for this one edge. Not checked: whether any other recorded folder falls outside `eval`.
3. **Which coordinator box each edge meets is my reading of `onyx/coordinator.py`**: the release is MLFO, `agent.run` is C,
   `_gate` and the log are D. The test checks the files on an edge, not this choice.

## One thing seen in Chrome

The first load showed GitHub's "Unable to render rich display". Two further loads rendered with no error, and no change was
pushed between them, so it looks transient. The cause is not established. A local parse of the block never ran: that harness
failed on its own setup ("Element is not defined"), so the evidence is GitHub's rendering, not a parser.

The figure is tall, about 1,936 px at full size in GitHub's frame, so it takes more than one screen; GitHub's frame has pan
and zoom controls. Left as `flowchart TD`.

## Limits line and test output

Touched only the files this order and ruling name, plus the CHANGELOG, this report-back and its screenshot; never `runs/`
or the keys. No prompt, gate, key, run, eval figure, report or annex change; no KB row. No competitor named. None of the
seven layers of `_reference/llm-agents.md` touched. Fails closed: USD 0, nothing recorded, nothing sent outward, stop and ask.
Owner of any failure: Iyas.

`uv run pytest tests/test_readme_diagram.py -q`:

```
.................                                                        [100%]
17 passed in 1.40s
```

`uv run pytest -q`:

```
........................................................................ [  9%]
........................................................................ [ 19%]
........................................................................ [ 28%]
........................................................................ [ 38%]
........................................................................ [ 48%]
........................................................................ [ 57%]
........................................................................ [ 67%]
........................................................................ [ 76%]
........................................................................ [ 86%]
........................................................................ [ 96%]
.............................                                            [100%]
749 passed in 182.67s (0:03:02)
```
