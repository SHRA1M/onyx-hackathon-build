# Task 46: README architecture diagram keyed to Y.3172 nodes (order written on Fable, 2026-11-04)

Decided in `D:\Projects\hq\uni\ai-for-good-hackathon\rival-strengths-read-2026-11-04-fable.md`, section 8. Build on
Opus, after Task 45 is merged, before 2026-11-06. Start with `git pull` on main. Branch `task-46`.

## Task

Add one Mermaid flowchart to `README.md`, directly under the `## Y.3172 mapping` heading and above the existing
table. It shows Mizan's own modules as boxes, grouped into subgraphs named by the Y.3172 node each serves (SRC, C, PP,
M, P, D, SINK, MLFO, ML sandbox), with the edges that exist in the code. Convention stated in a Mermaid comment and a
one-line caption under the figure: solid edge, used on every recorded run; dotted edge, used only by an optional
command (`whatif`, `model-down`, `localmodel`, `kb fetch`).

Boxes name the file: for example `Gate<br/>onyx/gate.py`. Only files that exist under `onyx/` may appear. Only calls
or imports that exist may appear as edges. The grouping follows the existing Y.3172 mapping table in the README; the
diagram and the table must agree node by node.

## Done means

1. `README.md` renders the diagram on GitHub (open the branch's README in Chrome, screenshot the figure, attach the
   path in the report-back).
2. `tests/test_readme_diagram.py`: parses the Mermaid block out of `README.md`; every `onyx/...py` path named in a
   box is a file in the repo; every edge's two ends are boxes defined in the block; every subgraph title is one of the
   nine Y.3172 names used in the mapping table; the set of files named in the diagram equals the set of files named
   in the mapping table (so the two cannot drift apart). Fails on any miss.
3. `uv run pytest` green; CI "reproduce" green on the PR.
4. The README's "For the reviewer" row for Y.3172 points at the diagram and the table (one phrase added, no other
   README text changed).
5. Report-back in `docs/report-back/` with the test output and the screenshot path; the page counts of
   `docs/report.pdf` unchanged (the report is not touched).

## Limits

- Text only. No prompt, gate, key, run, eval figure, report or annex change. No new row in the KB.
- No competitor is named anywhere.
- The seven layers of `_reference/llm-agents.md`: none touched; nothing shipped or deferred changes.
- Stop and ask if: a module in the mapping table has no file under `onyx/` (the table is then wrong, and that is a
  separate fix); the diagram needs more than about 25 boxes to be true (then group by package, not file, and say so);
  GitHub does not render the block.
