# Task 49: eight wording fixes in the register and README (hq, Opus, 2026-11-05)

For a build session, Opus, in `D:\Projects\engineering\onyx-hackathon-build`. Start with `git switch main`, `git pull`, then a new branch `task-49`, draft PR. Findings came from a Fable read of the unreviewed parts of `docs/gaps.md` and the README on main at 5bbd68a; hq confirmed the strings and their counts on main. A separate full audit is still running: its findings, if any, come as a later order. Do not wait for it.

Allowed sources: the repo and this file. No web reads, no new knowledge-base row, no manifest change, nothing under `onyx/data/keys/`, `runs/` or `onyx/prompts/`.

`docs/gaps.md`, the README gap table and `docs/site/gaps.html` are generated: edit `onyx/data/gaps.json`, then regenerate (`python -m onyx gaps`, the site, the report build).

## Rulings on stop 1 (hq, 2026-11-05)

Answers `docs/report-back/2026-11-05-task-49-stop-1.md`. Build everything below with no further question from that stop.

1. Item 1 passes: eight pages plus one link out to the repository. `six pages` becomes `eight pages`.
2. The filed order stays under `docs/work-orders/`, named in the report-back as the one extra file. Refile this revised version.
3. The three test pins you listed (`tests/test_gaps.py` lines 630, 716, 718) are updated to the new strings.
4. Item 8's `page` is 15, as you confirmed.
5. **New item 9, the same form and the same condition as item 8.** Add one `searched` line to gap-11: `clause` `tdra-cpr-v2-en:4.19.3`, `file` `kb/sources/tdra-cpr-v2-en.pdf`, `page` the PDF page where it stands, `says` `SMS or USSD purchase: agreement by a separate step on the same channel; nothing on a channel that interprets free words.`, `quote` copied from the stored text, starting "the purchase procedure shall necessitate" and ending "(e.g. SMS or USSD)". If the tests cannot take it without changing how other lines are checked, leave it out and say so.

## Task

**1. `README.md` line 122.** `six pages` becomes `eight pages`. First count the links in the site's nav, and stop if it is not eight.

**2. `onyx/data/gaps.json`, two places (lines 86 and 429 on main; gaps 2 and 11).** Replace both:
`The operator's own code sells through an automated IVR with immediate binding effect; no OTP, no read-back, no AI named.`
becomes
`The operator's own code describes subscription through its IVR as binding with immediate effect; the code names no OTP, read-back or AI; what the sale must include is set by the CPR, not by the code.`

**3. `onyx/data/gaps.json`, gap-10, `qos-v3-en:9.5` `says`.**
`All 43 QoS chunks searched for language, Arabic, English and لغة: no hit.`
becomes
`The QoS Policy v3.0 was searched for language, Arabic, English and لغة: no hit; one chunk (9.5, Annex A) is held.`
First count the lines of `kb/chunks/qos-v3-en.jsonl`, and stop if it is not one.

**4. `README.md` line 137.**
`no recorded run, C3 or C5, cites CPR 17.4 or 17.4.1.`
becomes
`no recorded S1 run, C3 or C5, cites CPR 17.4 or 17.4.1.`
hq found `tdra-cpr-v2-en:17.4` in `runs/c5/S3/ar/run1.jsonl` and `run2.jsonl` and none under `runs/c5/S1`. hq did not check C3's S1 runs: search every S1 run folder and print the result. Stop if an S1 run cites it.

**5. `onyx/data/gaps.json`, two `cabinet-56-2024-en:5(6)` `says` lines.** The clause ends "in accordance with the provisions of this resolution".
`Automated systems may market; no duty to disclose the machine.`
becomes
`Automated communication systems may market, in accordance with the resolution; no duty to disclose the machine.`
and
`Automated systems may market. A permission.`
becomes
`Automated communication systems may market, in accordance with the resolution. A permission.`

**6. The Air Canada amount, two places: `onyx/data/gaps.json` gap-7 `note` and `docs/annex.md` line 259.**
`(CAD 812.02)`
becomes
`(ordered to pay CAD 812.02 in all, CAD 650.88 of it damages)`
First read both figures in the stored decision (`ca-bccrt-2024-149-moffatt`, para 44), and stop if they differ.

**7. `onyx/data/gaps.json`, gap-7, the two `says` lines (`du-code-of-practice-en:Annex 1` and `eand-code-of-practice-en:1`).** Replace both:
`The only UAE texts naming an operator chatbot are the operators' own non-contractual codes; neither sets a conduct standard.`
becomes
`The only UAE texts naming an operator chatbot are the operators' own codes of practice; neither sets a conduct standard (e&'s says it forms no contract).`

**8. Gap-6 names AI Ethics guideline 3.3.2.2 but quotes it nowhere.** Add one `searched` line at the end of gap-6's list, in the same form as the other lines that carry `file` and `page`:
- `clause`: `mocai-ai-ethics-2022:3.3.2.2`
- `file`: the document's stored file under `kb/sources/`
- `page`: the page where the clause stands (Fable read it on p. 15; confirm)
- `says`: `Non-binding: an AI that can pass as a human should say it is an AI first. The only federal text that says it.`
- `quote`: copy from the stored text, not from here. It starts "If an AI system can convincingly impersonate a human being" and ends "that it is an AI system".

The manifest already holds this document, so this is not a new row. If the tests cannot take this line without changing how other lines are checked, leave item 8 out, say so, and build the other seven.

## Check only, change nothing

CPR 4.18 to 4.21 are not in `kb/chunks/`, so nobody has tested gap-11's claim that no text says what a voice or chat channel must do against them. Read them in the stored CPR text and print them in the report-back, with one line each on whether they touch that claim. Mark that line as your inference.

## Done means (show each output in the report-back)

1. Each "first" check above, with its output.
2. `git grep` for each old string on the branch: hits only in `docs/report-back/`, `docs/work-orders/`, `docs/sources/` and archive files.
3. Full suite passes; name every test whose pin changed and every test added.
4. `kb verify`, `check-data`, `selftest`: 108 / 100 / 5 / 3; 161 chunks.
5. Page script: 5 main pages, page 5 ends with "Limits and next steps"; total pages printed. Item 6 touches the annex: say whether the total moved from 12.
6. `git diff --stat`: only `onyx/data/gaps.json`, `README.md`, `docs/annex.md`, what regenerates, the tests, `CHANGELOG.md` and the report-back; nothing under `kb/manifest.csv`, `onyx/data/keys/`, `runs/`, `onyx/prompts/`.
7. Print every changed line as it stands in the files.
8. CI "reproduce" green on the head commit; paste the run id.

Then stop for hq's check and Iyas's word on the merge. Do not merge.

## Limits (the seven layers)

No prompt, gate, mandate, retrieval or model change, so versioned prompt, grounding, gated tools, identity, injection defence, cost cap and trace are untouched; no eval rerun owed. Never imply e& or du breaks a law or code.

## Stop and ask when

A string above is found a different number of times than stated. A "first" check fails. A test pins a figure or a clause this order does not name. The main report's page count changes, or page 5 no longer ends with "Limits and next steps". Reading 4.18 to 4.21 shows gap-11's claim is false (report it; do not fix it).
