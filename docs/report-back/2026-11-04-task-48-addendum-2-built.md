# Task 48, addendum 2: items 2 and 4 built (2026-11-04)

Addendum `task-48-addendum-2-claims-2026-11-04.md`, for hq (`D:\Projects\hq\uni\ai-for-good-hackathon\`) and for Iyas's read. Branch `task-48`, draft PR #17, not merged. USD 0, no model call. Items 1 and 3 were already in (`10165d4`) and were not redone.

Plainly: the replay page's line now says what each check covers, and gap 2 no longer says a flat "buys the service". No item on the stop list was met. Nothing differs from the addendum except one added test, named below.

## Stop list, checked before any edit

| Stop | Result |
|---|---|
| A string in item 2 or 4 found zero or more than once | Not met. Item 4 `"gap"` string: 1 in the file, 1 in the field. Item 4 `"uae_position"` string: 1, 1. Item 2's sentence in `onyx/replay_viewer.py`: 1 |
| A governed run has an allowed proposal whose quote is not verbatim in a cited clause | Not met. 10 governed runs, 79 gate events: 43 allow, 19 hold, 10 block, 7 insufficient evidence. All 43 allowed quotes are verbatim in a cited clause, read from each gate event's own `old_value` with ids resolved as the verdict records (1 such id). This count includes the 4 `classify_channel` events. `override_release` events: 0. Read-only script; the repo does not run this check |
| The page count changes | Not met. 5 main pages, annex from page 6, 12 in all |
| A test pins a figure this file does not name | Not met. Only the two named pins failed |

## Done means

| # | Check | Result |
|---|---|---|
| 1 | Full suite; pins | PASS: 756 passed in 186.00s. Pins changed: `test_task_26_rows_1_and_2_name_the_clocks_and_4_9` (`tests/test_gaps.py` line 416), `test_task_48_gap_2_cell_is_the_rulings_and_the_claim_matches_what_ci_checks` (`tests/test_report.py` line 517). New, 1: `test_task_48_addendum_2_spoken_consent_is_to_the_purchase_not_a_flat_cover` (`tests/test_gaps.py`), which pins the new `uae_position`; the addendum names no pin for it. All three seen failing first |
| 2 | `kb verify`, `check-data`, `selftest` | PASS: `VERIFIED 100  REFERENCED 5  UNVERIFIED 3  HISTORICAL 0`, 108 manifest rows; "every fetched source matches its sha256"; `check-data ok: every rule and mandate quote verbatim, every rule cites a clause`; "figures match a fresh eval of runs/"; 161 chunks |
| 3 | Page script | PASS: `pages: 5`, `words: 2379`, `annex starts on page: 6`, `total pages: 12`, `total words: 6943`. `docs/report.docx` did not change on rebuild. `docs/report.pdf` as committed: 12 pages; page 5 holds "Limits and next steps" and ends with its paragraph ("...further gaps and candidates."); page 6 opens "Annex" |
| 4 | `git diff --stat` | Below. Nothing under `kb/`, `onyx/data/keys/`, `runs/` or `onyx/prompts/`; `onyx/gate.py` and the mandates untouched |
| 5 | The three texts as they stand | Below |
| 6 | CI "reproduce" on the new head | PASS on `ca4957a`: run 41915274765 (push) and run 41915290212 (pull_request), success; "732 passed, 24 skipped"; "228 logs: chain ok". The commit after it adds only this result to this file |

Not run, not merged: CI on main; the README diagram on GitHub. Both are after-merge checks, as in the ruling.

`docs/report.md` row 2 carries neither phrase, as the addendum says; the file did not change. In `docs/gaps.md`, the lines that changed are 20, 137 and 193; in the README, line 72. In `docs/replay/index.html` and `docs/site/runs.html`, the one line.

## `git diff --stat`, against `79d4504`

```
 CHANGELOG.md                                       |  1 +
 README.md                                          |  2 +-
 docs/gaps.md                                       |  6 +++---
 docs/replay/index.html                             |  2 +-
 docs/report-back/2026-11-04-task-48-addendum-2-built.md | new
 docs/site/gaps.html                                |  2 +-
 docs/site/runs.html                                |  2 +-
 onyx/data/gaps.json                                |  4 ++--
 onyx/replay_viewer.py                              |  2 +-
 tests/test_gaps.py                                 | 11 ++++++++++-
 tests/test_report.py                               | 10 +++++++---
```

## The new gap-2 `"gap"`, as it stands in `onyx/data/gaps.json`

Consent elicited by an AI: the CPR accepts spoken consent if it can be stored (4.7.2) and sets the consent safeguard by sales medium: a recording of the Subscriber giving verbal consent on a call to the call centre (4.17.3), a 'no' default on yes/no screens in the Licensee App (4.22.3), 2FA for each online purchase (4.23.2), and 2FA in all digital applications unless objectively justified or expressly specified otherwise (4.10); none names an AI channel, so the safeguard an agent must meet follows the channel the operator embeds it in (a voice agent on the call-centre line reads as 4.17, a chat agent in the app as 4.22 or 4.10, a web chat as 4.23), not what the agent does; the PDPL permits the processing the contract needs without consent (4(9)) and wants any further processing consented 'in writing or electronically' (6(1)(b)); a spoken 'yes' buys the service once the channel's own safeguard is met (4.17.3, 4.22.3, 4.23.2 or 4.10) and consents to nothing beyond it, and whether a 'yes' the agent itself heard and interpreted is the Subscriber's positive affirmative action taken freely (4.7.1), or consent in writing or electronically under 6(1)(b), is unsaid.

## The new gap-2 `"uae_position"`, as it stands in `onyx/data/gaps.json`

No CPR sales medium names a conversational agent; Mizan reads the agent as inheriting the medium it is embedded in, so whether an AI-elicited purchase needs an OTP depends on where the operator puts it. The processing the contract needs is lawful without consent (4(9)); a spoken consent through the agent is consent to the purchase (4.7.2), not to a processing purpose beyond the contract, which 6(1)(b) wants in writing or electronically. Mizan takes the strict reading (4.10 plus OTP, 4.11).

## The new replay line, as it stands at `onyx/replay_viewer.py` line 286

`<p class="meta">Rule quotes on this page are checked word for word against their stored clauses on every push; in a governed run the gate must find the agent's quote verbatim in a cited clause before it can allow a proposal, and "Without the gates" shows proposals no gate checked; an "Elsewhere" quote is checked against its source file where that file is on disk; <code>kb verify</code> checks each stored source against the issuer's file by SHA-256 where the file is on disk; to check a run's log chain yourself: <a href="../site/verify.html">verify</a>.</p>`

It appears once each in `docs/replay/index.html` and `docs/site/runs.html`.

## Open

Iyas's read of the three texts above, and his word on the merge.
