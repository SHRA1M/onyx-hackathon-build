# Report-back: competitor names removed from tracked files (2026-11-09)

Opus. Branch `remove-competitor-names`, PR open, not merged. Repo still private, Pages off.

## How the search was done

All tracked files (`git grep -i`, text files) were searched for every entry, repo, handle and person named in hq's
competitor reads (`D:\Projects\hq\uni\ai-for-good-hackathon\competitor-*.md`). Those include the Saudi winners another team
and another team, which the orders name. `docs/report.docx` and `docs/report.pdf` were also checked by text extraction and
had no hits. No file name holds a name. Every hit was in `docs/work-orders/`.

Note: those orders are frozen under this repo's rules. This order named them, so they were edited.

## Every hit, by file and line (each replaced with "another team"; no other word changed)

1. `docs/work-orders/2026-10-17-onyx-mizan.md`
   - 34: another team (in `competitor-another team-README.md`)
   - 36: another team (in `another team_README.md`), another team (in `another team_JUDGE-QA.md`)
   - 60, 273, 344, 369, 385, 389 (two), 391, 397, 427: another team
   - 344, 353, 374, 379: another team
2. `docs/work-orders/2026-10-22-task-16-pages-grounding-readme.md`
   - 8: another team, another team
   - 10: another team
3. `docs/work-orders/2026-10-24-task-20-gap-10-arabic-parity.md`
   - 73: another team, another team
4. `docs/work-orders/2026-10-29-task-29-field-take.md`
   - 41: another team, another team, another team, another team
5. `docs/work-orders/2026-10-30-task-30-global-examples.md`
   - 72: another team, another team
6. `docs/work-orders/2026-11-08-task-56-site-restyle.md`
   - 11: another team (twice, one in the URL), another team (in the URL), another team (in `another team-demo.mp4`)

Total: 34 replacements in 6 files. A case-insensitive search afterwards finds none.

Inside file paths and the URL, the replacement leaves odd text such as `https://github.com/another team/another team`.
That is the literal replacement the order asked for.

## Checks

- `uv run pytest -q`: 1200 passed.
- `uv run python -m onyx selftest`: "figures match a fresh eval of runs/", exit 0.

## Git history: yes, the names are still there

Commits touching each name (`git log --all -i -G`): another team 3, another team 2, another team 3, another team 1, another team 4,
another team 1, another team 2, another team 1, another team 1, another team 1, another team 2 (another team is in history only, in
no tracked file today). SYNORA and ITUAIIP: 0.

If the repo goes public, anyone can read these names in old commits. Removing them means rewriting history (for
example `git filter-repo`) and force-pushing `main`. That is a decision for hq and Iyas; this branch does not do it.

## Open for hq

1. Rewrite history before going public, or accept the names in old commits?
2. `tests/test_pages_grounding_readme.py` still skips `docs/work-orders/`. With the orders now clean, it could cover them too. Not done; outside this order.
