# Working brief: onyx-hackathon-build

Updated 2026-11-06 (eighty-third wrap, Opus). Handover for the next session.

## Objective

Iyas names the next step when the session opens. Open work: finish Task 53, then the video. Submission 2026-11-09.

## State

- **Task 53: stopped a fourth time, branch `task-53`, pushed, no PR, not merged.** Items 29 to 45 are applied, item 45 as far as step (f). Main text ends page 5, annex on page 6, 16 pages. Docx and PDF rebuilt.
- Tests: 1 failed, 1145 passed. The failure is `tests/test_task_51.py:81`: step (e) took out "over the 20 scored runs".
- Report-back: `docs/report-back/2026-11-06-task-53-stop-4.md`.
- **Fable has ruled: item 46 is at the end of the order, uncommitted in the working tree, not built.** It undoes (e) and tries a language label on the Results line, in the order it gives. It always ends in a fit, so it has no further stop.
- No hidden Word was left when this session ended.

## Open questions

1. Iyas: is Zaid Saaydeh in the Faculty of Artificial Intelligence? His registration is also open (session 5 ruling).
2. Arabic check on Task 52's merged text, still owed (`docs/report-back/2026-11-06-task-52-arabic-check.html`).
3. Earlier, still open: two AI reads of the gap-15 Cabinet sentence; hq's three items in `docs/report-back/2026-11-05-task-51-built.md`; Iyas asks Ra'ed which translations he found wrong.

## Next moves, if Iyas says finish Task 53

1. `git status`; `git switch task-53`; `git pull`. Commit item 46 in the order, by name.
2. Build item 46 only. Measure page 5 on a scratch build after each try: `build_report.py --out <scratch>`, then `report_pages.ps1 -Path <scratch>`. Pin first, then edit; `tests/test_task_53.py` has the demo item 4 and Results pins.
3. Rebuild docx and PDF. Check for hidden Word. Full `pytest`, push, open the PR, watch CI.
4. Write `docs/report-back/2026-11-06-task-53-built.md`, including the diff lines for items 1 to 10 that "done means" asks for; carry over the sweep and count list from stop 4 and recheck the words that changed. Give Iyas the path. He merges.
