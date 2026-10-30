# Working brief: onyx-hackathon-build

Updated 2026-10-30 (forty-second wrap, Opus).

## Objective

Task 29 (`docs/work-orders/2026-10-29-task-29-field-take.md`): four parts, one PR each, all merged by 2026-11-03 so
the video can start. Parts A and B merged to main (PR #1, PR #2, CI green). Submission 2026-11-09.

## Next moves

1. Part C in a new session (2026-11-01 in the order): C1 binding tag on every cite (replay pages, viewer, site runs
   page), C2 `python -m onyx kb datasheet` writing `kb/DATASHEET.md`, C3 ML Intent only if time. Branch `task-29`
   is level with main; one PR, CI green.
2. Every report-back (Iyas, `_reference/how-we-build.md`, 2026-10-29): paste the full `uv run pytest` output, and
   repeat the Limits line: touches only the named files, never `runs/` or the keys; fails closed (USD 0, nothing
   recorded, nothing pushed outward, stop and ask); owner of any failure is Iyas.
3. Part D on 2026-11-02. Iyas, 2026-10-30: where an interval's upper bound rounds to 1.00 but hits are below n, write
   three decimals: pooled action recall "0.937 to 0.995". B1 short form: "expected gaps: 5 of 7 found in every run,
   2 missed (both in S1), 3 unexpected register ids flagged".

## Open questions

- Part B ran before session 5 and sweep 4b; if either changes prompts or scenarios, hq re-rules and eval regenerates.
- Submission-day order: GitHub Pages source = `docs/site/`; submission email aiforgoodlab@itu.int.
- hq: strips the two entry names from the filed Task 16 and Task 20 orders before 2026-11-09.
- hq: the team members' spellings for the README team line.
- `/setup-matt-pocock-skills` not yet run.
