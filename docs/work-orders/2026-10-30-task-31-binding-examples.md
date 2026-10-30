# Task 31: binding global examples for gaps 2, 7 and 12 (written 2026-10-30, hq uni, Fable)

Repo: `D:\Projects\engineering\onyx-hackathon-build`. Start from `main` after PR #6 is merged and `task-30` is
tagged. Branch `task-31`, one PR. Build on Opus. Pattern: Task 30 (`docs/work-orders/2026-10-30-task-30-global-examples.md`).
Source of the texts and words: `D:\Projects\hq\uni\ai-for-good-hackathon\perplexity-2026-10-30\global-examples-narrow-read-2026-10-30-fable.md`
(sections 2 and 4). Fetch every text yourself from the route given there; hq's read is the check, not the source.

## Why

Gaps 2, 7 and 12 cite guidance (IMDA) or an industry standard (SAE J3016) as global examples; the other nine cite
binding law. Four binding texts and one tribunal ruling were found and read at the primary on 2026-10-30.

## Part A: knowledge base (five extracts, all `foreign`, `extract`, `binding` except Moffatt)

1. `sg-eta-2010-s15`: Singapore Electronic Transactions Act 2010, s. 15, current version as at 30 Oct 2026, from
   sso.agc.gov.sg. Language `en`.
2. `us-utah-13-77-102`: Utah Code 13-77-102, effective 2026-05-06, from le.utah.gov (PDF, one page). `en`.
3. `ca-bccrt-2024-149-moffatt`: Moffatt v. Air Canada, 2024 BCCRT 149, paragraphs 1 to 6, 14 to 17, 24 to 32 and 44,
   from decisions.civilresolutionbc.ca. Kind: tribunal decision, not statute; if the manifest's `binding` field has
   no value for a decision, add `decision` to the schema's allowed values and say so in the report-back. `en`.
4. `eu-roaming-2022-612-art14`: Regulation (EU) 2022/612, Articles 14 and 24, from EUR-Lex (CELEX 32022R0612). `en`.
5. `eu-ai-act-2026-07-27-art14-26`: Regulation (EU) 2024/1689 consolidated 2026-07-27, Articles 14 and 26, same
   URL as the existing `eu-ai-act-2026-07-27` row (Art 50 and 113). New row, not an edit of the old one. `en`.
   Notes field: "High-risk systems only. Chapter III Sections 1 to 3 apply from 2027-12-02 (Annex III) and
   2028-08-02 (Annex I), Regulation (EU) 2026/1744 Art 1(40)(b)."

Each row: source URL, fetch date, status code, SHA-256, size, VERIFIED. Expected after Part A: 59 documents,
55 VERIFIED, 17 foreign. If the counts come out otherwise, stop and say why.

## Part B: gap register (`onyx/data/gaps.json`, `docs/gaps.md`)

- gap-2: add one `global_examples` entry (Singapore s. 15, the full sentence). Note: "Singapore, like UAE
  Electronic Transactions 46/2021 Art 12(2), validates the automated contract; neither names the sales medium."
  Recommendation unchanged.
- gap-7: replace the two IMDA `global_examples` entries with Utah 13-77-102 (quote the whole section) and Moffatt
  para 27 (from "While a chatbot has an interactive component" to "or a chatbot.") and para 28 first sentence.
  Keep IMDA in the recommendation sentence as it is. Note: "Utah bars the 'the AI said it' defence; the BC
  tribunal held Air Canada to its chatbot's words (CAD 812.02). The UAE has the general duty (CPR 3.3) and no
  AI-specific one."
- gap-12: keep the SAE J3016 entries; add roaming Art 14(4) (the "If the roaming customer does not respond"
  sentence and the "within one working day" clause) and AI Act Art 14(4)(e) (the stop-button sentence). The AI
  Act entry's `says` field carries the caveat word for word from Part A item 5. Recommendation unchanged.
- Every quote must be found word for word in the stored text (the existing test).

## Part C: report and README

- `docs/report.md` gap table: row 7 global-example cell names "Utah Code 13-77-102; Moffatt v. Air Canada 2024 BCCRT
  149"; row 12 names "EU Roaming Reg 2022/612 Art 14(4); EU AI Act Art 14(4)(e) (high-risk, from 2027)". Row 2 adds
  "Singapore ETA s. 15" only if the report stays at 5 pages; otherwise leave row 2 and say so.
- Count sentences: "54 documents", "50 are verified", "twelve foreign texts" become 59, 55, seventeen, wherever the
  count check reads them (report, README, datasheet). Run the count check.
- No sentence may say or imply that e& or du breaks any of these rules.

## Part D: the flagged gap explains itself (added 2026-10-30, Fable; Iyas asked whether the agent can say "not in UAE
law, but in X")

Today a judge opening a run sees `Gap flagged: gap-1` as a bare id (`onyx/replay_viewer.py` abstain branch, about
line 138; `onyx/replay_page.py` about line 155). Render-only change, read from `onyx/data/gaps.json` at render time:

- Replay viewer, abstain block: after the id, the gap's `line` (the one-liner the adviser prompt uses), then one line
  "Elsewhere: <first global example's label>" with its quote in English, then a link to `docs/site/gaps.html#<id>`.
  Where `global_examples` is empty (gap-8), write "Elsewhere: none found; this recommendation is the example."
  Candidate ids (`candidate-...`) show their line only.
- Step markdown (`docs/replay/S*.md`): the same text in plain markdown under the Abstention line.
- The subscriber-facing reply does not change. No prompt, log, key, gate or eval change. The recorded logs replay as
  recorded; the hash chain is untouched.
- Rebuild the replay pages and the site twice; identical.

## Done means

- Part D: open `docs/replay/index.html` run S2 step 3 in Chrome, screenshot the abstain block showing gap-1's line and
  "Elsewhere: Spain Ley 10/2025 Art 8(2)" (file the screenshot in `docs/site/screenshots/`); S3 step 3 shows gap-5
  with GDPR Art 28(3)(a); every `Elsewhere` quote is found word for word in the stored text (existing check).
- `kb verify`: VERIFIED 55, REFERENCED 1, UNVERIFIED 3, all hashes match (show output).
- Quote-in-stored-text check passes for every new quote (show count).
- Data check passes; register and site rebuilt twice, identical.
- Full test suite passes; CI green on the PR.
- Report 5 pages (Word count, as in Task 30).
- hq copy: `report-draft-2026-10-23.md` in hq matches `docs/report.md` (same step as Task 30).
- Report-back at `docs/report-back/2026-10-30-task-31-binding-examples.md`, with the table of checks.

## Limits

No change to gates, keys, runs, prompts or eval (Part D touches render code only). No other gap rows. No China or South Africa text. USD 0 model
spend. Every change done before 2026-11-06.

## Stop and ask when

- A fetched text differs from the words in the read file.
- EUR-Lex, SSO or the CRT site will not serve the text by the route given (do not substitute a law-firm or
  CanLII copy).
- The report leaves 5 pages after dropping the row 2 addition.
- The manifest schema needs a change beyond the `decision` value.
- Part D cannot be done without touching the log, a prompt or a key.
