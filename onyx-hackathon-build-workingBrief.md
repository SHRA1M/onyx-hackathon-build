# Working brief: onyx-hackathon-build

Updated 2026-10-29 (forty-second session, Opus).

## Objective

Task 29 (`docs/work-orders/2026-10-29-task-29-field-take.md`): four parts, one PR each, all merged by 2026-11-03 so
the video can start. Part A (model down) merged to main through PR #1 on 2026-10-29. Submission 2026-11-09.

## Next moves

1. Part B on 2026-10-31 (eval: gaps against keys, Wilson intervals, citation failures by kind), after session 5 and
   sweep 4b. If either changes anything, hq re-rules before Part C.
2. Part B also fixes the hold reason (hq ruling, 2026-10-29). On the model-down path only, `gate.decide_pending` says
   the model was unavailable, not that the adviser answered INSUFFICIENT_EVIDENCE. Add `onyx/gate.py` to Part B's
   files for this one change. Every C3, C4, C5 log must still replay unchanged (`tests/test_replay_unchanged.py`).
3. Every report-back from Part B on (Iyas, `_reference/how-we-build.md`, 2026-10-29): paste the full `uv run pytest`
   output, and repeat the Limits line: touches only the named files, never `runs/` or the keys; fails closed (USD 0,
   nothing recorded, nothing pushed outward, stop and ask); owner of any failure is Iyas.
4. Part C (binding tags, KB datasheet, optional ML Intent) on 2026-11-01; Part D (gap-12 words, report rebuild,
   5 pages) on 2026-11-02.

## Open questions

- Submission-day order: GitHub Pages source = `docs/site/`; submission email aiforgoodlab@itu.int.
- hq: strips the two entry names from the filed Task 16 and Task 20 orders before 2026-11-09.
- hq: the team members' spellings for the README team line.
- `/setup-matt-pocock-skills` not yet run.
