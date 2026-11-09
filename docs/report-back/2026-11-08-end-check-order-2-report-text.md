# Report-back: end-check order 2, report main text

Order: `D:\Projects\hq\uni\ai-for-good-hackathon\end-check-order-2-report-text-2026-11-08.md`, with hq's answer to the interim stop (Fable, 2026-11-08: option a). Branch `end-check-2-report-text` from `main`. Commit `12cb625`. PR: https://github.com/SHRA1M/onyx-hackathon-build/pull/27 (not merged).

## The stop, and hq's answer

The U8 sentences at the end of the C3-tagged paragraph failed `docs/build_report.py`'s value check (their counts are not in `eval/results.md`). hq: option a, their own untagged paragraph right after "What is different.", same words; one test pins the counts to the annex; try 4b, drop it if rejected; `build_report.py` unchanged.

## The edits

1. U8 sentences: made, as their own paragraph after "What is different." (line 33), words as in end check part 5.
2. Cut 1, Introduction "The case is an ordinary customer...": made.
3. Cut 2, Demo item 4 "A re-run costs USD 0...": made.
4. Demo item 3, "the scenario has the care agent propose": made.
4b. "(29 of the 67 are test proposals we wrote in; Annex C)": NOT made. The value check rejected it ("29: cannot classify", "67: cannot classify"). The annex carries it.
5. "Next steps: Annex A.": made, end of the Limits paragraph.
Reserve cut (part 5, cut 3; part 9 ruling 9): made. With edits 1 to 4 the main text ran to page 6. Removed from Results: "The gate decides in a median of 0.46 ms; the model's proposal takes a median of 7.8 s `[C3, governed, 222 decisions, 156 calls]`." Both medians remain in `eval/results.md` line 26 (0.458 ms, 7837.607 ms).

## Numbers in the edited paragraphs and their source

- "What is different." (`docs/report.md` line 31): 2.3 and 2.1, `eval/results.md` (C3), passed the builder's value check.
- U8 paragraph (line 33): 8 of 48, 0 of 48, six runs, 48 of 48: `docs/annex.md` line 255 ("the gate allowed 8 of 48 governed steps"; "0 of 48 governed steps, in 0 of 6 governed runs"; "Without the gate, 48 of 48 steps passed"). Match; pinned by the new test.
- Introduction (line 14): no number left in it.
- Demo item 3: S3, step 3, PDPL 22 and 23(2): unchanged.
- Demo item 4: gap 1, gap 4, S2, S4: unchanged.
- Results: 0.99 / 1.00, 0.96 / 1.00, 110 of 112, 1.00, 5 of 7, gaps 2 and 6, 3 unexpected: unchanged, passed the value check.
- Limits: no number.

## Tests moved (no visible word changed by any of them)

- `tests/test_task_53.py`: the S3 item and Demo item 4 pins follow the new wording; the cut Introduction sentence no longer required in the report (still required in the README).
- `tests/test_annex.py`: `LIMITS_END` now ends "Next steps: Annex A."
- `tests/test_task_51.py`: the strip's "20 recorded runs" was matched to "over the 20 scored runs", which cut 2 removed. Now matched to "two runs per scenario per language" (5 scenarios x 2 languages x 2 runs). **For hq:** the main text no longer prints "20" runs outside the strip; say if that matters.
- `tests/test_report.py`: new `test_u8_counts_in_the_main_text_match_the_annex`.

## Checks

`scripts/report_pages.ps1` (after `uv run python docs/build_report.py`):

```
pages: 5
words: 2570
annex starts on page: 6
total pages: 16
total words: 9765
```

Report tests (`tests/test_report.py test_annex.py test_task_45.py test_task_51.py test_task_51b.py test_task_53.py test_task_54.py test_site.py test_gaps.py`): `410 passed in 40.86s`.

Not run: the full suite (the order asks for the report tests); `docs/report.pdf` not rebuilt (not in the order).

## Open questions for hq

1. The "20 runs" pin above.
2. `docs/report.pdf` is now older than `docs/report.docx`; rebuild in a later order.
