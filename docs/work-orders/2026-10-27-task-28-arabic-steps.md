# Task 28: Arabic step text, S1 to S5, and the Arabic re-record (hq, Fable, 2026-10-27)

Repo: `D:\Projects\engineering\onyx-hackathon-build`. **Base: `main` at a3a8d64** (if `main` has moved, name the
commit and go on; if a task branch is open, stop and say so). Branch `task-28`. Model calls: yes, Arabic runs only.
**Spend limit USD 4**, stop and ask when passed. The API organisation holds USD 100 promotional credit granted
2026-10-27 (expires 2026-11-25) on top of USD 1.11; keys in `.env` have values (checked 2026-10-27).

Ruling: `D:\Projects\hq\uni\ai-for-good-hackathon\arabic-steps-ruling-2026-10-27.md`. Source of the text:
`docs/report-back/2026-10-27-arabic-step-review.md` (commit 8ffbd4b). Iyas chose 2026-10-27 to run this before the
10-31 sweep, knowing the 10-31 order may re-record again if prompts or scenarios change. Timing objection stated, his call.

## Part A: the text (`onyx/data/scenarios/S1.json` to `S5.json`, key `text_ar` only)

A1. Replace `text_ar` on every step listed in the report-back's "His wording, verbatim" table with that table's Arabic,
except: S2.1, S2.5, S3.2, S5.1 take the "Settled with Iyas" table instead. S1.2 and S1.4 unchanged. `text_en`
unchanged everywhere. U1 to U7 unchanged.
A2. Two consistency edits on top (ruling section 2), applied to the copied text, nothing else in the line changes:
- S1.6: `يقترح ممثل خدمة العملاء` becomes `يقترح موظف خدمة العملاء`.
- S5.6: `تطلب هيئة تنظيم الاتصالات (TDRA)` becomes `تطلب هيئة تنظيم الاتصالات والحكومة الرقمية (TDRA)`.
A3. Copy the Arabic from the report-back file by program or by exact paste, never retyped. After the edit, print a
table: step, old `text_ar` first 40 characters, new `text_ar` first 40 characters, and for every changed step a check
that the new value equals the report-back table cell (normalise only trailing whitespace). 26 changed, 2 unchanged.
A4. `check-data`, `uv run pytest`, scripted replay. `tests/test_scenarios.py:91` (scripted release equals file text) must
pass; if any test hard-codes old Arabic, change the test's expected string to the new text and list it in the report-back.

## Part B: the re-record (Arabic only)

B1. Move `runs/c5/S1/ar` to `runs/c5/S5/ar` into `runs/_superseded/c5-ar-2026-10-27/S1/ar` and so on, by `git mv`.
Do the same for any Arabic ungoverned cells under `runs/ungoverned/` (list what exists first; if none, say so).
English runs untouched. Every English run file's hash before equals its hash after (print `git diff --stat <base> -- runs/`
filtered to `/en/`: must be empty).
B2. Record the Arabic cells again with the exact `record` invocation used for C5 (find it in `CHANGELOG.md` or the C5
report-back; name it in the report-back). Same run count per cell as the superseded cells (2 governed per scenario, checked
2026-10-27). Same model, same prompt version, same keys. If the ungoverned Arabic cells existed, record them too.
B3. Print spend after every scenario (the gateway's usage fields or the Console). Stop and ask if a run fails on a quote or
parse error more than once in one cell, or if spend passes USD 4.

## Part C: everything downstream

C1. Re-run eval, selftest, verify-log, replay-page, `python -m onyx site` (twice; `git status --short docs/site` empty).
C2. Report-back table of every figure that moved, old against new: each Arabic row of `eval/results.md` (gate rejection,
citation validity, action recall, obligation proxy, gap recall, abstention, hand-over latency, must-cite given, gap flags
without a clause), the "Arabic versus English agreement" line, the 107 of 112 line and any count on the gaps page, the
hash chain length (100 logs before; state the new count). hq rewrites `docs/report.md` sentences that carry a moved
figure; **the builder does not touch `docs/report.md` or `docs/report.docx`.**
C3. `CHANGELOG.md`: one entry naming the superseded folder and the 26 steps changed.

## Done means (hq checks; show each output)

1. `git diff --stat <base>` lists only: the five scenario files, `runs/_superseded/c5-ar-2026-10-27/**` (moves),
   new `runs/c5/*/ar/*.jsonl` (and ungoverned ar if any), `eval/**`, `docs/replay/**`, `docs/site/**`, the verify-log
   output file, `CHANGELOG.md`, any test whose expected Arabic changed, the filed order, the report-back.
2. `git diff <base> -- onyx/gate.py onyx/data/rules.json onyx/data/keys onyx/data/mandates.json onyx/prompts
   onyx/eval.py docs/report.md docs/report.docx README.md` prints nothing; `text_en` unchanged (diff the five files
   with `text_ar` lines filtered out: empty).
3. A3's equality table: 26 rows equal, S1.2 and S1.4 unchanged.
4. `uv run pytest` count (411 before; name the new count and any test string changed).
5. Verify page recomputes the chain in the browser on the rebuilt site: open `docs/site/verify.html`, print the count it
   shows and that it says valid.
6. Spend: the figure, under USD 4.
7. CI green on the branch and on `main` after the merge; name the run.
8. Report-back at `docs/report-back/2026-10-27-task-28-arabic-steps.md`: C2's table, the `record` invocation, runs
   that failed and were retried, time taken, anything left out.

## Limits

- Arabic `text_ar` on S1 to S5 only. No gate, rule, key, mandate, prompt, scorer, English run, report or README change.
- No other entry's name in any tracked file. Never commit a manifest changed only by a fetch date.
- Stop and ask: a task branch already open; a test that fails for a reason other than an old Arabic string; a figure
  that moves by more than 0.05 (report it, do not "fix" it); spend past USD 4; the chain fails to verify.
