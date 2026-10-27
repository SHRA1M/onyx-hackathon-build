# Report-back: Task 28, Arabic step text and the Arabic re-record (2026-10-27)

Order: `docs/work-orders/2026-10-27-task-28-arabic-steps.md`. Branch `task-28` from `main` at a3a8d64. Built by Opus 5.5.
**Not merged.** CI on the branch fails until hq updates the C5 Arabic figures in `README.md` and `docs/report.md`, which
the builder may not touch (see "Merge danger").

## Summary

- 26 `text_ar` lines replaced, copied by program from `docs/report-back/2026-10-27-arabic-step-review.md`: the four
  settled rows for S2.1, S2.5, S3.2 and S5.1, plus the two consistency edits on S1.6 and S5.6. S1.2, S1.4, every
  `text_en` line and U1 to U7 are unchanged.
- The 10 C5 Arabic runs moved to `runs/_superseded/c5-ar-2026-10-27/` with `git mv`, then recorded again. Cost
  USD 2.98, under the USD 4 limit. No run failed, none was retried, and no log has a quote or parse failure.
- C5 Arabic action recall rose from 0.94 to 1.00, and key steps hit from 107 to 110 of 112. Several figures moved by
  more than 0.05. I stopped and asked as the order says; Iyas chose to keep the new runs and hand the figures to hq.

## Departures from the order (each asked and ruled by Iyas, 2026-10-27)

1. **Replay fix in `onyx/runs.py` and `onyx/whatif.py` (not in the order's file list).** Once the text changed,
   replay rebuilt each step from the current scenario file, so every Arabic log recorded on the old text (C3, C4,
   ungoverned, bake-offs) replayed to different verdicts: 4 tests failed for a reason other than an old Arabic string.
   The fix: `runs.recorded_scenario` takes each step's text from the log's own `release_event`, and whatif uses it too.
   New test `tests/test_arabic_steps.py` (seen failing first on `runs/c4/S1/ar/run1.jsonl`, then passing).
2. **Spend stop `cost.TOTAL_CAP_USD` raised from 20 to 30 (`onyx/cost.py`, three tests in `tests/test_cost.py` changed).**
   Recorded spend was USD 18.87, so the USD 20 stop would have refused the re-record. Iyas chose USD 30. The order's
   USD 4 limit for this task was kept.
3. **The ungoverned Arabic runs were left as they are.** They do exist: `runs/ungoverned/S1..S5/ar`, 3 runs each, 15 in
   all. They are C3 runs on prompt v3, which no longer exists, so they could not be recorded "on the same prompt", and
   recording them too would have cost about USD 4.38, over the USD 4 limit. Iyas chose to re-record the governed C5
   runs only. These 15 logs, the C3 governed Arabic runs (`runs/S*/ar`) and the C4 Arabic runs still carry the old
   text; with fix 1 they replay as recorded.
4. **`docs/fig/fig2-results.png` and `.svg` were regenerated (not in the list).** Figure 2(a) plots C5 action recall
   per language, and CI fails on a stale figure.

## Record invocation

The C5 runs were recorded one scenario at a time with `--skip-existing`; the archive entry for 2026-10-22 gives the
order but not the command line. This is the reconstructed command, with `ONYX_MODEL=claude-sonnet-5-5` from `.env`
and prompt v5:

`uv run python -m onyx record --source live --root runs/c5 --scenarios <S> --modes governed --runs 2 --skip-existing`

It was run in this order: S1, S2, S3, S4, S5. The English runs already existed and were skipped. The estimate printed
before each scenario counts English too, so it overstates (USD 1.44, 1.19, 1.11, 1.16, 0.90).

| After | Task 28 spend | Recorded total | Quote / parse failures |
|---|---|---|---|
| S1 | USD 0.76 | USD 19.64 | 0 / 0 |
| S2 | USD 1.34 | USD 20.21 | 0 / 0 |
| S3 | USD 1.91 | USD 20.78 | 0 / 0 |
| S4 | USD 2.50 | USD 21.38 | 0 / 0 |
| S5 | USD 2.98 | USD 21.85 | 0 / 0 |

Recorded spend counts the superseded logs too, so the USD 18.87 recorded before Task 28 still includes them.
Time taken: about 3.5 hours, including two waits for Iyas's answers. The 10 live runs took 11 minutes (20:34 to 20:45 UTC).

## C2: figures that moved, old against new (C5, governed, Arabic)

| Figure | Old | New | Move |
|---|---|---|---|
| Action recall, mean S1 to S5 (`results.md` summary) | 0.94 (earlier rule 0.94) | 1.00 (earlier rule 0.96) | +0.06 |
| Obligation proxy, mean | 0.56 | 0.58 | +0.02 |
| S3 ar action recall, run range | 0.67 / 0.90 / 0.80 | 0.67 / 0.90 / 1.00 | +0.20 (C5 cell) |
| S4 ar action recall, run range | 0.47 / 1.00 / 0.90 | 0.47 / 1.00 / 1.00 | +0.10 (C5 cell) |
| S3 ar obligation proxy | 0.36 | 0.46 | +0.10 |
| S4 ar obligation proxy | 0.53 | 0.41 | **-0.12** |
| S5 ar obligation proxy | 0.50 | 0.61 | +0.11 |
| Misses per step, S3-4 care, ar | 2 of 2 | 0 of 2 | |
| Misses per step, S4-4 data office, ar | 1 of 2 | 0 of 2 | |
| Key steps hit ("107 of 112") | 107 of 112 (5 missed) | **110 of 112 (2 missed)** | |
| C5 cost total | USD 5.3350, 104 calls | USD 5.3767, 104 calls | |

The run-range cells list C3 / C4 / C5. The two misses left are both English: S3-4 and S4-4, one run each.

These are unchanged: citation validity (ar 1.00), gate rejection, abstention 1.00, gap recall, hand-over latency, must-cite
given, gap flags without a clause, the "Arabic versus English agreement" line (C5: S1 0.88, S2 0.88, S3 0.57 to 0.86,
S4 0.71 to 0.86, S5 0.88), every C3 and C4 figure, and the gaps page (`docs/gaps.md` and `docs/site/gaps.html` did not
change). The site's verify page still lists 100 logs (C3, C4, C5; superseded logs are not on the site). The hash chain
check by `verify-log` covered 227 committed logs, 0 broken.

### Sentences hq needs to rewrite (builder did not touch them)

- `README.md:49`: "action recall 0.96 English / 0.94 Arabic on C5"
- `README.md:155-156`: "action recall 0.96 / 0.94 ... obligation proxy 0.57 / 0.56; 5 of 112 key steps missed."
- `docs/report.md:100`: "0.96 / 0.94 (107 of 112 key steps; the five misses fall in two steps, S3-4 and S4-4, ...)"
- `docs/report.md:134`: "action recall 0.96 English, 0.94 Arabic (C5)"
- then `docs/report.docx` rebuilt (`docs/build_report.py`; its value check is what fails now).

## Evidence: done means

1. `git diff --stat a3a8d64`: 40 files. These are the order's list, plus `onyx/runs.py`, `onyx/whatif.py`,
   `onyx/cost.py`, `tests/test_cost.py` and `docs/fig/fig2-results.*` (departures 1, 2 and 4). No English run is in
   the diff (`git diff --stat a3a8d64 -- runs/` filtered to English paths prints nothing). The verify-log output file
   named in the order does not exist: verify-log prints and writes nothing.
2. `git diff a3a8d64 -- onyx/gate.py onyx/data/rules.json onyx/data/keys onyx/data/mandates.json onyx/prompts
   onyx/eval.py docs/report.md docs/report.docx README.md | wc -l`: 0 (prompts live in `onyx/agents/`, also unchanged).
   Each scenario file with the `text_ar` lines filtered out is identical to base: S1 to S5.
3. The A3 table is below: 26 rows equal, S1.2 and S1.4 unchanged. "Equal" means the cell after the two A2 edits; S1.6
   and S5.6 differ from their raw cell only by those edits (checked: True, True).
4. `uv run pytest`: 411 before, 413 passing after Part A (2 new tests in `tests/test_arabic_steps.py`). Three cap tests
   changed in `tests/test_cost.py` (20 to 30). No test held old Arabic. Now **398 passed, 5 failed, 10 errors**. All 15
   are the README and report figure checks (`test_readme_three_things_and_the_c5_figures`,
   `test_readme_scored_run_is_c5_with_the_figures_eval_wrote`, and `tests/test_report.py`, whose docx build fails the
   value check on "107 of 112"). They pass once hq's README and report text matches `eval/results.json`.
5. Verify page (Playwright on `docs/site/verify.html`, served from localhost because Playwright blocks file://): 100 logs
   listed. All 10 new Arabic C5 logs show "Chain ok", for example S1 ar run1: "Chain ok: 24 events, every hash
   recomputed and matched." `python -m onyx site` run twice: `git status --short docs/site` empty.
6. Spend: USD 2.98, under USD 4.
7. CI: the branch run fails on the README and report figure tests until hq's change lands. It is **not** green yet;
   nothing is merged.
8. This file.

## Merge danger

Two-way door for the text and the code. The re-record is one-way in spend only: the old runs are kept under
`runs/_superseded/`. Merging before hq's README and report change would turn `main` red.

## A3 table

| step | old text_ar (first 40) | new text_ar (first 40) | equals report-back cell |
|---|---|---|---|
| S1.1 | İÊÍ ãÔÊÑß ãÍÇÏËÉ ÏÇÎá ÊØÈíŞ ÓÍÇÈ. Õäøİ Ş | ŞÇã ÃÍÏ ÇáãÔÊÑßíä ÈİÊÍ ãÍÇÏËÉ ÏÇÎá ÊØÈíŞ | EQUAL (his table) |
| S1.2 | ãÑÍÈÇğ¡ ÓÃÓÇİÑ Åáì áäÏä ÇááíáÉ ÇáÓÇÚÉ 11 | ãÑÍÈÇğ¡ ÓÃÓÇİÑ Åáì áäÏä ÇááíáÉ ÇáÓÇÚÉ 11 | unchanged |
| S1.3 | ÇÚÑÖ Úáì ÇáãÔÊÑß ÈÇŞÉ ÊÌæÇá ÇáããáßÉ ÇáãÊ | ÇÚÑÖ Úáì ÇáãÔÊÑß ÈÇŞÉ ÇáÊÌæÇá İí ÇáããáßÉ | EQUAL (his table) |
| S1.4 | äÚã | äÚã | unchanged |
| S1.5 | ÃÏÎáÊ ÑãÒ ÇáÊÍŞŞ 4471. ÃæÇİŞ Úáì ÇáÔÑæØ  | Êã ÅÏÎÇá ÑãÒ ÇáÊÍŞŞ (OTP) 4471. ÃæÇİŞ Úá | EQUAL (his table) |
| S1.6 | Çáíæã ÇáËÇãä. ÇäÊåÊ ÈÇŞÉ ÇáÃíÇã ÇáÓÈÚÉ æ | Çáíæã ÇáËÇãä. ÇäÊåÊ ÈÇŞÉ ÇáÃíÇã ÇáÓÈÚÉ¡  | EQUAL (his table + A2 edit) |
| S2.1 | İÊÍÊ ãÔÊÑßÉ ãÍÇÏËÉ ÏÇÎá ÊØÈíŞ ÓÍÇÈ. Õäøİ | ŞÇãÊ ÅÍÏì ÇáãÔÊÑßÇÊ ÈİÊÍ ãÍÇÏËÉ ÏÇÎá ÊØÈ | EQUAL (settled table) |
| S2.2 | áãÇĞÇ İÇÊæÑÊí 230 ÏÑåãÇğ åĞÇ ÇáÔåÑ¿ ÚÇÏÉ | áãÇĞÇ ÊÈáÛ İÇÊæÑÊí 230 ÏÑåãÇğ åĞÇ ÇáÔåÑ¿ | EQUAL (his table) |
| S2.3 | áã ÃØáÈ Ãí ãÍÊæì ããíÒ ÃÈÏÇğ. åĞÇ ÎØÃ. ÃÒ | áã ÃØáÈ ãØáŞÇğ Ãí ãÍÊæì ãÏİæÚ. åĞÇ ÛíÑ Õ | EQUAL (his table) |
| S2.4 | ÇáãæÙİ ÇáÈÔÑí H-01: ÌåøÒ áí ãÓæÏÉ ÑÏ áÃÑ | Çáæßíá ÇáÈÔÑí H-01: íÑÌì ÕíÇÛÉ ÑÏ áÃŞæã  | EQUAL (his table) |
| S2.5 | ÈÚÏ ÇáÊĞãÑ İí ÇáÎØæÉ 3¡ ãÇ ÇáÓÑÚÉ ÇáÊí í | ÈÚÏ Ãä ÚÈøÑÊ ÇáãÔÊÑßÉ Úä ÇÓÊíÇÆåÇ İí ÇáÎ | EQUAL (settled table) |
| S2.6 | ÊØáÈ ÇáåíÆÉ ÓÌá ÔßÇæì ÇáãÔÛá áÔåÑ ÃßÊæÈÑ | ÊØáÈ åíÆÉ ÊäÙíã ÇáÇÊÕÇáÇÊ æÇáÍßæãÉ ÇáÑŞã | EQUAL (his table) |
| S3.1 | ÊæŞİæÇ Úä ÇÓÊÎÏÇã ÈíÇäÇÊí ááÊÓæíŞ. áÇ ÃÑ | ÊæŞİæÇ Úä ÇÓÊÎÏÇã ÈíÇäÇÊí áÃÛÑÇÖ ÇáÊÓæíŞ | EQUAL (his table) |
| S3.2 | ÊØáÈ ÔÑßÉ ÏíæäÒ ááÊÌÒÆÉ¡ áÍãáÉ ãÔÊÑßÉ: Ã | ÊØáÈ ÔÑßÉ "ÏíæäÒ ááÊÌÒÆÉ" (Dunes Retail  | EQUAL (settled table) |
| S3.3 | áÕíÇÛÉ ÑÏ Úáì åäÏ¡ íŞÊÑÍ æßíá ÇáÑÚÇíÉ ÅÑ | áÕíÇÛÉ ÑÏòø Úáì "åäÏ"¡ íŞÊÑÍ ãæÙİ ÎÏãÉ Ç | EQUAL (his table) |
| S3.4 | ÕöÛ ÇáÑÏ Úáì åäÏ ÈÇÓÊÎÏÇã ÇáÍÏ ÇáÃÏäì ãä | ÃÚÏø ÇáÑÏ ÇáãæÌå Åáì "åäÏ" ÈÃŞá ŞÏÑ ããßä | EQUAL (his table) |
| S3.5 | ÇáÓÇÚÉ 19:30. íŞÊÑÍ äÙÇã ÇáÍãáÇÊ ÅÌÑÇÁ ã | ÇáÓÇÚÉ ÇáÂä 19:30. íŞÊÑÍ äÙÇã ÇáÍãáÇÊ ÅÌ | EQUAL (his table) |
| S4.1 | İÇÊæÑÉ ÈŞíãÉ 180 ÏÑåãÇğ Úä ÎØ ÇáåÇÊİ Çáã | ÈáÛÊ İÊÑÉ ÊÃÎÑ ÓÏÇÏ İÇÊæÑÉ ÎØ ÇáåÇÊİ Çáã | EQUAL (his table) |
| S4.2 | ÃÑÓá Åáì ÇáãÔÊÑß ÇáÅÔÚÇÑ ÇáİÑÏí æÇáÊÍĞíÑ | ÃÑÓöá Åáì ÇáãÔÊÑß ÇáÅÔÚÇÑ æÇáÊÍĞíÑ ÇáİÑÏ | EQUAL (his table) |
| S4.3 | Çáíæã ÇáËÇãä ÈÚÏ ÇáÊÍĞíÑ. áã ÊõØÇÈŞ Ãí Ï | Çáíæã ÇáËÇãä ÈÚÏ ÇáÅäĞÇÑ. áã íÊã ÇáÚËæÑ  | EQUAL (his table) |
| S4.4 | ÂáÉ ŞØÚÊ ÎØí Ïæä Ãä íäÙÑ ÃÍÏ İí ÍÇáÊí. Ï | ŞÇã äÙÇã Âáí ÈŞØÚ ÎØ ÇáÎÏãÉ ÇáÎÇÕ Èí Ïæä | EQUAL (his table) |
| S4.5 | ãÊì íÌÈ Ãä ÊäÊåí ÇáãÑÇÌÚÉ ÇáÈÔÑíÉ ÇáãØáæ | ÈÍáæá Ãí ãæÚÏ íÌÈ Ãä ÊäÊåí ÇáãÑÇÌÚÉ ÇáÈÔ | EQUAL (his table) |
| S5.1 | ÊÍíá ÇáåíÆÉ äÒÇÚ ÇáãÓÊåáß D-2026-0310 Åá | ÊÍíá åíÆÉ ÊäÙíã ÇáÇÊÕÇáÇÊ æÇáÍßæãÉ ÇáÑŞã | EQUAL (settled table) |
| S5.2 | ÊæÌøå ÇáåíÆÉ ÓÍÇÈ Åáì ÅÚÇÏÉ ÇáÎÏãÉ ÇáÕÇÏ | ÊõæÌöøå åíÆÉ ÊäÙíã ÇáÇÊÕÇáÇÊ æÇáÍßæãÉ Çá | EQUAL (his table) |
| S5.3 | ÓõÑŞ åÇÊİí ŞÈá ÓÇÚÉ. ÇÍÌÈæå ÇáÂä ãä İÖáß | ÓõÑöŞ åÇÊİí ŞÈá ÓÇÚÉ. ÃÑÌæ ÍÙÑå ÇáÂä¡ æÍ | EQUAL (his table) |
| S5.4 | ãÇ ÇáĞí íõÚÏø ÊÍŞŞÇğ ßÇİíÇğ ãä åæíÉ åĞÇ  | ãÇ ÇáĞí íõÚÏø ÊÍŞŞÇğ ßÇİíÇğ ãä åæíÉ ÇáãÊ | EQUAL (his table) |
| S5.5 | ÇáãæÙİ ÇáÈÔÑí H-04: Êã ÇáÊÍŞŞ ãä ÇáåæíÉ  | Çáæßíá ÇáÈÔÑí H-04: Êã ÇáÊÍŞŞ ãä ÇáåæíÉ  | EQUAL (his table) |
| S5.6 | íæã ÇáÚãá ÇáËÇáË ÈÚÏ ÅÍÇáÉ ÇáäÒÇÚ. ÊØáÈ  | ËÇáË íæã Úãá ÈÚÏ ÊŞÏíã ÇáäÒÇÚ. ÊØáÈ åíÆÉ | EQUAL (his table + A2 edit) |

changed 26, equal 26, unchanged 2
S1.6 differs from the raw cell only by A2: True
S5.6 differs from the raw cell only by A2: True
