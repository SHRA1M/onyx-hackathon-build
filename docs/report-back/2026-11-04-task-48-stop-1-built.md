# Task 48, stop 1 ruling and quote addendum: built, waiting for Iyas's read (2026-11-04)

Ruling `task-48-stop-1-ruling-2026-11-04.md`, addendum `task-48-addendum-quote-9-2026-11-04.md`. Branch `task-48`, draft PR #17, not merged. USD 0, no model call.

Plainly: gap 2 now says the safeguard follows the channel, and that nothing says whether a "yes" the agent itself heard counts as consent. The GitHub line fits on one line. The three claims now state what actually runs. The Arabic quote reads as printed. The report still fits: 5 main pages, 12 in all. Two checks wait for the merge.

## Done means, ruling

| # | Check | Result |
|---|---|---|
| 1 | Full suite; pins | PASS: 753 passed in 206.58s, before one test-only tidy; `tests/test_gaps.py` then rerun alone, 99 passed. CI on the final code: 729 passed, 24 skipped. Pins below |
| 2 | `kb verify`, `check-data`, `selftest` | PASS: VERIFIED 100, REFERENCED 5, UNVERIFIED 3 (108); "every fetched source matches its sha256"; "check-data ok"; "figures match a fresh eval of runs/"; 161 chunks. `selftest` was run before the addendum, and again in CI after it. **Departure below: `check-data` does not read the four quotes** |
| 3 | Pages | PASS: `pages: 5`, `annex starts on page: 6`, `total pages: 12`, PDF 12. Page 5 read as an image: ends in the "Limits and next steps" paragraph. Page 1 read as an image: the GitHub line is on one line; the first shortening was enough |
| 4 | Count check | PASS, table below |
| 5 | `git diff --stat` | In the PR. `kb/manifest.csv`, `onyx/data/keys/`, `runs/`, `onyx/prompts/`: empty |
| 6 | Text printed; Iyas reads; CI on main | Text below. **Iyas's read: waiting. CI on main: NOT RUN, not merged** |
| 7 | `pytest -rs` under CI conditions | PASS, below |
| 8 | README diagram on GitHub after the merge | **NOT RUN, not merged** |

CI on the PR, commit `b519176`: run 41907213578 (pull_request) success, run 41907202209 (push) success; "729 passed, 24 skipped", "228 logs: chain ok".

## Departure: `check-data` and the four quotes

The ruling asks that `check-data` finds the four 1d quotes. It cannot: `check_data()` in `onyx/data.py` compares rule and mandate quotes. It reads gap `searched` lines only to know which chunks are cited. So its "ok" says nothing about these quotes. No quote failed, so the stop clause was not met.

What does compare them: `test_every_gap_cites_searched_clauses_in_kb` (every gap quote against its chunk, on every push) and the new `test_task_48_four_searched_lines_follow_4_22_in_order_with_quotes_from_the_chunks`. Both pass. The quotes were cut by script from `kb/chunks/tdra-cpr-v2-en.jsonl`. `check-data` was not widened; that is not in the ruling. For hq: its message says "every quote verbatim", which is wider than what it reads.

## Pins changed

- `tests/test_report.py`: `LINKS`, used by `test_task_34_team_and_the_four_labelled_links`; `test_eight_list_paragraph_headings_in_template_order`.
- `tests/test_gaps.py`: `TASK_33_SEARCHED["gap-15"]` (addendum), used by `test_task_33_searched_entries_follow_task_32s`; `test_task_33_quotes_are_verbatim_in_the_stored_text` takes the one named exception, `PRINTED_NOT_TEXT_LAYER`.
- Lines 416 to 418 of `tests/test_gaps.py`: unchanged, as the ruling says. No other test pinned old gap 2 text.
- New, 4: `test_task_48_gap_2_says_the_safeguard_follows_the_channel`, `test_task_48_four_searched_lines_follow_4_22_in_order_with_quotes_from_the_chunks`, `test_task_48_gap_2_cell_is_the_rulings_and_the_claim_matches_what_ci_checks`, `test_task_48_addendum_52_2024_quote_is_as_printed_with_one_exception`. 749 + 4 = 753.

## Count check

| Report states | Value found | Proved by |
|---|---|---|
| 108 documents; 100 / 5 / 3 ("two unpublished, one unreachable": the 3 counted, the split not recounted) | 108; 100 / 5 / 3 | `kb/manifest.csv`, `kb verify` |
| thirty-two other UAE texts; thirty-eight foreign | build passes | `docs/build_report.py` `check_kb_counts` |
| 371,476 complaints | found once | `docs/sources/eand-sustainability-report-appendices-2025.txt` |
| 2.3 / 2.1 proposals; 0.99 / 1.00; 0.96 / 1.00 | present in the report | build value check, `selftest` |
| 110 of 112; 5 of 7 | present | `eval/results.md` |
| gate median 0.46 ms; 222 decisions | 0.458 ms; 222 | `eval/results.md` |
| model median 7.8 s; 156 calls | 7837 ms; 156 | `eval/results.md` |
| USD 5.3767 over 20 runs; USD 0.27 a run | 5.3767; 20 runs | `eval/results.md`, `runs/c5` |
| Annex D: 161 chunks, 77 with `text_ar`, 10 Arabic runs, 23 columns, 21 documents, 108 records | same | `kb/chunks/*.jsonl`, `runs/c5/S*/ar/`, `kb/manifest.csv` |

Annex numbers beyond these rest on the build's value check, not on a separate check by me.

## Skipped tests under CI conditions

A clean worktree of `00f978c`, without `kb/sources`, `data/chromadb` or `kb/index-bilingual`: 730 passed, 22 skipped. All 22 skip because `kb/sources/` is not there: `tests/test_gaps.py` lines 77, 247, 346, 360, 454, 537, 638, 807, 922, 1056, 1194, 1312, 1473, 1484, 1583; `tests/test_kb.py` lines 134, 422, 592, 662; `tests/test_pages_grounding_readme.py` line 53 (3 tests). Line numbers are as of `00f978c`.

The gap in one line: CI skips 2 more because `test_extract_body_is_the_hq_checked_file` has two cases and needs `D:/Projects/hq`, which exists only on this machine. This is read from the skip conditions and fits the count (22 + 2 = 24); CI's log prints no skip names, because it runs `pytest -q`. No fix made.

## The text for Iyas to read

**1a, gap 2 in `onyx/data/gaps.json`:**

Consent elicited by an AI: the CPR accepts spoken consent if it can be stored (4.7.2) and sets the consent safeguard by sales medium: a recording of the Subscriber giving verbal consent on a call to the call centre (4.17.3), a 'no' default on yes/no screens in the Licensee App (4.22.3), 2FA for each online purchase (4.23.2), and 2FA in all digital applications unless expressly specified otherwise (4.10); none names an AI channel, so the safeguard an agent must meet follows the channel the operator embeds it in (a voice agent on the call-centre line reads as 4.17, a chat agent in the app as 4.22 or 4.10, a web chat as 4.23), not what the agent does; the PDPL permits the processing the contract needs without consent (4(9)) and wants any further processing consented 'in writing or electronically' (6(1)(b)); one spoken 'yes' buys the service and consents to nothing beyond it, and whether a 'yes' the agent itself heard and interpreted is the Subscriber's positive affirmative action taken freely (4.7.1), or consent in writing or electronically under 6(1)(b), is unsaid.

**1b, row 2 in `docs/report.md`:**

| 2 | Consent elicited by an AI: the CPR sets the consent safeguard by sales medium (4.17.3, 4.22.3, 4.23.2) and names no AI channel, so an agent's safeguard follows where it is embedded; whether a "yes" the agent itself heard and interpreted is a positive affirmative action (4.7.1), or consent "in writing or electronically" under the PDPL (6(1)(b)), is unsaid | coordination | TDRA, UAE Data Office | CRD 2011/83 Art 8(2); IMDA 2.2.2; Singapore ETA s. 15 |

**1c, first sentence of `uae_position`:**

No CPR sales medium names a conversational agent; Mizan reads the agent as inheriting the medium it is embedded in, so whether an AI-elicited purchase needs an OTP depends on where the operator puts it.

**3a, `onyx/replay_viewer.py` line 286:**

`<p class="meta">Every quote on this page is checked word for word against its stored clause on every push; <code>kb verify</code> checks each stored source against the issuer's file by SHA-256 where the file is on disk; to check a run's log chain yourself: <a href="../site/verify.html">verify</a>.</p>`

**3b, `docs/report.md` line 25:**

clause the gates cite word for word against the text stored from it; two unpublished texts and one unreachable one back no claim. No consumer data was used.

**3c, `docs/annex.md` line 148:**

the rule, the rule names the clause, the clause's quote is checked against the stored clause text on every push, and the stored text against the issuer's file by hash where it is on disk. The

Not traced: that every quote shown on the replay page is a rule or mandate quote, which 3a's first clause assumes.

## Addendum, done means

1. `git grep -F` of the old string on the branch: `docs/report-back/2026-10-30-task-33-three-searches.md` and `tests/test_gaps.py` line 920, the named exception. PASS.
2. PASS: as checks 1 and 2 above. Tests changed: named above. `docs/report.docx` did not change on rebuild, so the page count holds. Only `test_task_33_quotes_are_verbatim_in_the_stored_text` needed the exception; the other tests that read this quote compare without whitespace. Other quotes are compared as before.
3. The new quote, as it stands in `onyx/data/gaps.json`:

يجوز للهيئة مضاعفة قيمة الغرامة الإدارية المحددة في الجدول المرفق بهذا القرار في حال تكرار ارتكاب ذات المخالفة الإدارية قبل مضي سنة من تاريخ ارتكابها لأول مرة

Its `says`: TDRA may double a fine when the same violation is repeated within a year; an itemised schedule TDRA administers under the neighbouring trust-services law, binding trust service providers, not telecom licensees. Portal English: 'The Authority may double the value of the administrative fine specified in the Table attached to this resolution in the event of the repetition of the same Administrative Violation before one year has passed from the date of its first time.' Arabic as printed on page 2 (eye-checked 2026-11-04); the PDF text layer has two spacing faults there.

I did not compare this against the printed page myself; Iyas's eye-check of 2026-11-04 is the evidence. The test compares it with the text layer through the exception.

## Limits

No prompt, gate, mandate, retrieval or model change; no knowledge-base row; manifest, keys and runs untouched; no eval rerun owed. Nothing merged.
