# Task 48, addendum 2: items 1 and 3 built; the replay line held at its stop (2026-11-04)

Addendum `task-48-addendum-2-claims-2026-11-04.md`, for hq (`D:\Projects\hq\uni\ai-for-good-hackathon\`). Branch `task-48`, draft PR #17, not merged. USD 0, no model call.

Plainly: the 4.10 fix and the `check-data` message are in. The new replay line is not. It says the gate checks the agent's quotes on each proposal, but every step on that page also shows proposals from a run with no gate. The addendum makes that a stop. The live line on the branch is still the older one, which hq has already found false for the "Elsewhere" quotes, so this has to be settled before the merge.

## Question 1: the replay line, stop met

The stop clause: "Any proposal shown on the replay page did not pass through the gate (the new line would then be false)."

Measured from the logs behind `docs/replay/index.html`: 5 scenarios, 2 languages, one governed and one ungoverned run each. Read-only scripts, nothing changed.

| Shown on the page | Proposals | With a shown quote | What checked the quote |
|---|---|---|---|
| Governed runs (10) | 65 | 59 | The gate: 58 reached the quote check; 1 ended earlier (below) |
| "Without the gates" sections, ungoverned runs (10) | 65 | 60 | Nothing. `gate.allow_all` returns allow without reading it: 79 of 79 gate events say "ungoverned run: no gate" |

- **Without the gates.** `Viewer.without_gates` prints each ungoverned proposal through the same `proposal()` as a governed one, with its "quoted:" line, inside a collapsed section. There are 56 such sections on the page. The section's title tells a reader no gate ran, but the sentence "the agent's quotes by the gate on each proposal" has no such limit. My script found all 60 quotes verbatim in a cited chunk, but that was my check today, not one the repo runs.
- **The one governed quote that ended earlier.** S4 Arabic, `draft_reply`, cites `cabinet-66-2023:34(5)`: the gate returned `insufficient_evidence` because that clause "was not retrieved by care for this step", before the quote check. The quote is not verbatim in the cited chunks. The gate did not allow it, so nothing false passed; but it did not check that quote.
- **Six other governed proposals** show no quote. All 65 governed proposals have a gate event, matched by verb within their step. "Rejected before the gate" appears 0 times.
- **A false alarm, closed.** S3 English `flag_gap` cites `pdpl-45-2021:22(1)`. My first script called its quote not verbatim because it did not resolve the id as the gate does. Against `pdpl-45-2021-en:22(1)` it is verbatim.

From reading `onyx/gate.py`: `_base_checks` runs the quote check before any allow; `decide_pending` cites nothing and cannot return allow, since it ends in block or hold. So in a governed run a proposal cannot be allowed without its quote being found verbatim.

**Candidate, not built, hq's wording to rule on.** Only the middle clause differs from the addendum's text:

`Rule quotes on this page are checked word for word against their stored clauses on every push; in a governed run the gate must find the agent's quote verbatim in a cited clause before it can allow a proposal, and "Without the gates" shows proposals no gate checked; an "Elsewhere" quote is checked against its source file where that file is on disk; <code>kb verify</code> checks each stored source against the issuer's file by SHA-256 where the file is on disk; to check a run's log chain yourself: <a href="../site/verify.html">verify</a>.`

Question 1: which text goes in at `onyx/replay_viewer.py` line 286? Recommended: the candidate. Once ruled, the build is that line, its pin at `tests/test_report.py` line 517, the regeneration of `docs/replay/*.html` and `docs/site/runs.html`, and CI.

The line as it stands now, unchanged:

`<p class="meta">Every quote on this page is checked word for word against its stored clause on every push; <code>kb verify</code> checks each stored source against the issuer's file by SHA-256 where the file is on disk; to check a run's log chain yourself: <a href="../site/verify.html">verify</a>.</p>`

## Done means, for what is built

Commit `10165d4`. Items 1 and 3 are in. Item 2's pin and pages are untouched.

| # | Check | Result |
|---|---|---|
| 1 | Full suite; pins | PASS: 755 passed in 220.69s. No existing pin changed. New, 2, in `tests/test_report.py`: `test_task_48_addendum_2_clause_4_10_keeps_both_exceptions`, `test_task_48_addendum_2_check_data_says_what_it_reads`. Both seen failing first. The replay pin stays as is, with item 2 |
| 2 | `kb verify`, `check-data`, `selftest` | PASS: VERIFIED 100, REFERENCED 5, UNVERIFIED 3 (108); "every fetched source matches its sha256"; `check-data ok: every rule and mandate quote verbatim, every rule cites a clause`; "figures match a fresh eval of runs/"; 161 chunks |
| 3 | Page script | PASS: `pages: 5`, `annex starts on page: 6`, `total pages: 12`. `docs/report.docx` did not change on rebuild, so `docs/report.pdf` was not rebuilt and page 5 was not reread; it still ends with "Limits and next steps" as read for `00f978c` |
| 4 | `git diff --stat` of `10165d4` | `CHANGELOG.md`, `README.md`, `docs/gaps.md`, `docs/site/gaps.html`, `onyx/data.py`, `onyx/data/gaps.json`, `tests/test_report.py`: 7 files, 25 insertions, 8 deletions. Nothing under `kb/manifest.csv`, `onyx/data/keys/`, `runs/`, `onyx/prompts/`. Pins went in `tests/test_report.py` because the addendum names that test file |
| 5 | New gap-2 `"gap"` and replay line printed | Gap below. **Replay line: not built, question 1** |
| 6 | CI "reproduce" on the head commit | PASS on `10165d4`: run 41911323863 (pull_request) and run 41911314485 (push), success; "731 passed, 24 skipped"; "228 logs: chain ok". The commit after it adds only this file |

Not run, not merged: CI on main; the README diagram on GitHub.

## The new gap-2 `"gap"`, as it stands in `onyx/data/gaps.json`

Consent elicited by an AI: the CPR accepts spoken consent if it can be stored (4.7.2) and sets the consent safeguard by sales medium: a recording of the Subscriber giving verbal consent on a call to the call centre (4.17.3), a 'no' default on yes/no screens in the Licensee App (4.22.3), 2FA for each online purchase (4.23.2), and 2FA in all digital applications unless objectively justified or expressly specified otherwise (4.10); none names an AI channel, so the safeguard an agent must meet follows the channel the operator embeds it in (a voice agent on the call-centre line reads as 4.17, a chat agent in the app as 4.22 or 4.10, a web chat as 4.23), not what the agent does; the PDPL permits the processing the contract needs without consent (4(9)) and wants any further processing consented 'in writing or electronically' (6(1)(b)); one spoken 'yes' buys the service and consents to nothing beyond it, and whether a 'yes' the agent itself heard and interpreted is the Subscriber's positive affirmative action taken freely (4.7.1), or consent in writing or electronically under 6(1)(b), is unsaid.

The 4.10 `searched` line's `says`: Digital applications: multi-step, 2FA unless objectively justified or expressly specified otherwise.
