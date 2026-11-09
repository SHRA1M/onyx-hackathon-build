# Report-back: competitor names removed from tracked files (2026-11-09)

Opus. Branch `remove-competitor-names`, PR #29. Repo still private, Pages off.

This file names no team. The 11 names are the entries, repos, handles and people listed in hq's competitor reads
(`D:\Projects\hq\uni\ai-for-good-hackathon\competitor-*.md`), plus the two Saudi winners the first order names.

## How the search was done

All tracked files (`git grep -i`, text files) were searched for every name in hq's competitor reads.
`docs/report.docx` and `docs/report.pdf` were also checked by text extraction and had no hits. No file name holds a
name. Every hit was in `docs/work-orders/`.

Note: those orders are frozen under this repo's rules. This order named them, so they were edited.

## Every hit, by file and line (each replaced with "another team"; no other word changed)

1. `docs/work-orders/2026-10-17-onyx-mizan.md`: lines 34, 36 (two, inside file names), 60, 273, 344 (two), 353, 369,
   374, 379, 385, 389 (two), 391, 397, 427. 16 replacements, three names (one repo name, two Saudi winners).
2. `docs/work-orders/2026-10-22-task-16-pages-grounding-readme.md`: lines 8 (two), 10. Three replacements, two names.
3. `docs/work-orders/2026-10-24-task-20-gap-10-arabic-parity.md`: line 73 (two). Two names.
4. `docs/work-orders/2026-10-29-task-29-field-take.md`: line 41 (four). Four names.
5. `docs/work-orders/2026-10-30-task-30-global-examples.md`: line 72 (two). Two names.
6. `docs/work-orders/2026-11-08-task-56-site-restyle.md`: line 11 (four, three inside a URL and a file name). One
   name and one GitHub handle.

Total: 34 replacements in 6 files. A case-insensitive search afterwards finds none.

Inside file paths and the URL, the replacement leaves odd text such as `https://github.com/another team/another team`.
That is the literal replacement the order asked for.

## Checks

- `uv run pytest -q`: 1200 passed (run before this file was written; this file's first version named the teams and
  failed `test_no_other_entry_is_named_in_a_tracked_file` on `main`; rewritten 2026-11-09).
- `uv run python -m onyx selftest`: "figures match a fresh eval of runs/", exit 0.

## Git history: yes, the names are still there

Each of the 11 names sits in 1 to 4 old commits (`git log --all -i -G`); one name is in history only, in no tracked
file today. If the repo goes public, anyone can read them. Handled by hq's history-clean order of 2026-11-09.

## Open for hq

1. `tests/test_pages_grounding_readme.py` still skips `docs/work-orders/`. With the orders now clean, it could cover
   them too. Not done; outside this order.
