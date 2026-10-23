# Report-back: Task 19b, gap 1 rule, Arabic text replaced (2026-10-23)

1. `text_ar` in `onyx/data/proposed/gap-1.json` is now the order's string, taken programmatically from the filed order's line, so the bytes match. The string carries two straight double quotes around "شكوى مستهلك"; JSON stores them as `\"`. `json.load` returns exactly the order's string (asserted when written). No other field changed.
2. `docs/replay/whatif-S2-gap-1.md` regenerated with `python -m onyx whatif runs/c5/S2/run1.jsonl --rule gap-1`, `docs/replay/index.html` with `python -m onyx replay-page --html`. One line changed in each. The viewer shows the quotes as `&quot;` in its HTML source (they display as quotes).
3. What-if output on `runs/c5/S2/run1.jsonl` (en) and `runs/c5/S2/ar/run1.jsonl` (ar), compared line by line with the output captured before the edit: identical. `S2-3-care` `draft_reply` block to block + obligation; `S2-5-coordinator` `route` hold to allow + check, finding; 8 of 10 decisions identical.
4. `git grep -n "يتوقف الوكيل غير البشري ويتولى"` prints two filed orders: Task 19's (line 26) and this order itself (line 18, where the Done-means line quotes the old text as the grep pattern). No other file.
5. `git grep -c "ومُحدَّد الهوية"`: gap-1.json 1, whatif-S2-gap-1.md 1, index.html 1 (plus this order, 2).
6. Item 7f diff against 1acf952 on the protected files: empty. Tests: 378 passed. check-data ok. CI: see the commit's run.
7. Report: `docs/report.md` and `docs/report.docx` untouched (the report holds no Arabic rule text), so the 5 pages stand; Word was not re-run.
8. Housekeeping: a stale empty `.git/index.lock` (no git process running) blocked the first commit; removed.
