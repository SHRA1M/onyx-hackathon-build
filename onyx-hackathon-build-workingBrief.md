# Working brief: onyx-hackathon-build

Updated 2026-11-04 (sixty-fourth wrap, Opus). Handover for the next session.

## Objective

Finish Task 47 once hq has answered, then Task 46, before the freeze on 2026-11-06. Submission 2026-11-09.

## State

- Task 45 merged (PR #14, `8b5a569`, CI passed). Its tag was not checked this session.
- Task 47 on branch `task-47`, committed and pushed, no PR. Benchmark, `eval` section and tests are in; both tables are in `eval/results.md`.
- Recall@8, shipped en 0.24, ar 0.09; bilingual `multilingual-e5-small` en 0.24, ar 0.15. Both low, printed as found.
- Task 46's order is untracked, deliberately.

## Open questions

The four in `docs/report-back/2026-11-04-task-47-stop-1.md`: annex figures as found; the words "the obvious upgrade"; README clause or none; and the finish. Iyas chose a fresh session for the finish.

## Next moves

1. `git status`; `git switch task-47`; `git pull`; check CI "reproduce" on the wrap commit.
2. With hq's answers: Annex A sentences (at most two) and a kept test that each number equals `eval/results.md`.
3. README clause only if hq says so. Rebuild `docs/report.pdf`; state body and annex page counts, unchanged.
4. CHANGELOG entry; report-back with the tables, model, revision, build time and the Limits line; full `uv run pytest`.
5. Open the PR, Task 46's order left out; confirm CI on the PR. Then Task 46 on branch `task-46`.
