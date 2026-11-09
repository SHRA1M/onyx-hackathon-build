# Report-back: Task 56f, model-down story sentence (2026-11-08)

Order: `D:\Projects\hq\uni\ai-for-good-hackathon\task-56f-modeldown-sentence-order-2026-11-08.md`. Branch `task-56`, commit `4cb6fa2`, not pushed, not merged.

## What changed

Old: "The rest of the conversation then ran as recorded: 7 of 8 later decisions stayed the same."

New: "The rest of the conversation ran as recorded: all 8 decisions outside step 3 kept their verdict. One of them, at step 5, lists 19 laws instead of 24, because the other five were cited only by the AI's step 3 proposals, which were never made here."

## Departure from the order (approved by Iyas in session)

The sentence is built in `onyx/replay_viewer.py` (`MODELDOWN_STORY`), not `onyx/site.py`. Iyas approved editing that file instead. It appears in one place only. In the template, "8" comes from `{total}` and "step 3" from `{at}`. 19, 24 and "five" are fixed text.

## Checks

- Numbers confirmed in `docs/replay/model-down-S2.md` ("What stays"): 8 decisions, S2-5, 19 ids instead of 24, five ids dropped. They match.
- Pin moved in `tests/test_task_56e.py::test_modeldown_page_is_a_scenario_from_its_own_log`. The test now asserts the new sentence and asserts that the old wording is gone. It failed before the edit and passed after.
- `uv run pytest -q`: 1198 passed.
- `python -m onyx selftest`: exit 0.
- `python -m onyx site` diff stat: only `docs/site/modeldown.html`, 1 line. "7 of 8 decisions outside step 3 identical." is still on the page as generated.

## Open questions for hq

None.
