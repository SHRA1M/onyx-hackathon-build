# Task 32: the operators' codes, 106/2026 and the CSC policy enter the KB (written 2026-10-30, hq uni, Fable)

Repo: `D:\Projects\engineering\onyx-hackathon-build`. Start from `main` after Task 31's PR is merged and `task-31` is
tagged. Branch `task-32`, one PR. Build on Opus. Pattern: Task 30 and 31. Source of the words:
`D:\Projects\hq\uni\ai-for-good-hackathon\perplexity-2026-10-30\uae-recheck-read-2026-10-30-fable.md`. Fetch the two
operator PDFs yourself from the URLs there and compare the SHA-256 with hq's; hq's copies in
`D:\Projects\hq\uni\ai-for-good-hackathon\standards-text\` are the check, not the source. The 106/2026 texts come from
hq's files as local sources, the way the other uaelegislation.gov.ae rows do (the portal refuses non-browser clients).

## Why

Gap 9 cites Cabinet Resolution 106/2026 and the KB has no row for it. The operators' own codes of practice name chatbot
and IVR channels and set no rule for them: the strongest UAE-side line for gaps 1, 2, 7 and 10, and a line no rival
has. A UAE AI security policy exists that we could not read; the datasheet should say so rather than omit it.

## Part A: knowledge base (four rows)

1. `eand-code-of-practice-en`: e& "Code of Practice regarding customer affairs", 13 pages,
   `https://eand.com/en/system/com/assets/docs/general/code-of-practice-for-customer-affairs.pdf`, expected SHA-256
   `4b6383a7523a3e2b6122dc923199583be7a1f15cbf26c6e6172f39fa31d05ddd`. Issuer "e& (Etisalat)". `UAE`, `en`,
   `binding_status` `advisory`, `source_type` `operator code` (add the value to the schema if absent and say so).
   Notes: "§1: not a contract or part of one. No version or date printed."
2. `du-code-of-practice-en`: du / EITC "Code of Practice", 5 pages, `https://www.du.ae/files/1430740188355`, expected
   SHA-256 `8f8014d981c1a407715a03ddb6fbd28192b81d52f414150a3f64b68d42e8e34d`. Issuer "EITC (du)". Same fields.
   Notes: "§1: approved by the TDRA; not a contract or part of one. No date printed. Covers du and Virgin Mobile UAE."
3. `cabres-106-2026-ar` and `cabres-106-2026-en`: Cabinet Resolution No. 106 of 2026 Regarding the Regulation of
   Children's Access to Social Media Platforms. Issued 2026-06-17, effective 2026-06-30, Official Gazette 826 of
   2026-06-29 (portal page read 2026-10-30). URLs `https://uaelegislation.gov.ae/ar/legislations/4506` and `/en/`.
   Local sources: `standards-text/cabinet-resolution-106-2026-children-social-media-ar.pdf` (7 pages) and
   `cabinet-resolution-106-2026-children-social-media-en.txt` (page text fetched 2026-10-22; its header lines say so).
   `binding`, `UAE`. Notes on the en row: "Portal: the Arabic text prevails."
4. `csc-ai-security-policy-v1-1`: "The National Cyber Security Policy for Artificial Intelligence", v1.1, UAE Cyber
   Security Council. URL
   `https://csc.gov.ae/documents/38662/1042755/National+Cyber+Security+Policy+for+Artificial+Intelligence_v1.1.pdf/aeca22fd-f413-f1ac-a01f-14446e62f982`.
   Status `UNVERIFIED`, `binding_status` `advisory` (unknown; say so in notes), `UAE`, `en`. Notes: "Host unreachable
   from Amman 2026-10-17 and 2026-10-30; no Internet Archive copy. Described at u.ae (page updated 2026-07-02): six
   chapters, Governance, Infrastructure and Application Security, Algorithm Security, Operational Safety, Adversarial AI
   Attacks, AI Monitoring and Response. Not read." If `standards-text/csc-ai-security-policy-v1-1.pdf` exists when you
   start, stop and say so: hq reads it first.

Expected after Part A, on top of Task 31's 59 / 55 / 3 / 1: **64 documents, 59 VERIFIED, 4 UNVERIFIED, 1 REFERENCED,
17 foreign, 29 UAE instruments.** If the counts come out otherwise, stop and say why.

No chunks for the four rows: they do not enter `kb_main`, the agents do not retrieve them, no run changes.

## Part B: gap register (`onyx/data/gaps.json`, `docs/gaps.md`), `searched` entries only, recommendations unchanged

- gap-1: du §10 (the "acknowledge your complaint immediately" sentence and the "within 20 business days" sentence),
  says: "CPR 26.13.3 and 26.14.2 restated as 'will try'; no hand-over clause." du Annex 1, the line "Chatbot", says:
  "the code names a chatbot as a complaint channel and sets no rule for it." e& §7, "We aim to rectify your problems
  as soon as possible." sentence, says: "no deadline, no hand-over, no AI named."
- gap-2 and gap-11: e& §4, the sentence from "For customer convenience" to "with immediate effect", says: "the
  operator's own code sells through an automated IVR with immediate binding effect; no OTP, no read-back, no AI named."
- gap-7: du Annex 1 "Chatbot" line and e& §1 non-contract sentence, says: "the only UAE texts naming an operator chatbot
  are the operators' own non-contractual codes; neither sets a conduct standard."
- gap-9: the existing 106/2026 cites now point at `cabres-106-2026-ar` (Arabic prevails) with the English row beside.
- gap-10: du Annex 1 languages sentence ("in Arabic, English, Hindi, Bengali and Malayalam"), says: "languages for human
  care; nothing on the chatbot's languages or quality."
- Every quote must be found word for word in the stored text (the existing test). Both codes say they are not
  contracts: every `says` field that leans on them keeps the word "code", never "rule" or "law".

## Part C: report, README, datasheet

- Count sentences: "59 documents", "55 are verified" become 64 and 59; "twelve/seventeen foreign texts" unchanged;
  wherever the UAE instrument count is stated it becomes 29. Run the count check. "fifteen other UAE laws" is fixed at
  the submission-day count check, not here, unless the count check already reads it.
- Report gap table: if 5 pages hold, row 1's UAE-side cell gains "du's code names a chatbot channel and sets no
  hand-over rule"; otherwise leave the table and say so. No other report wording changes.
- No sentence may say or imply that e& or du breaks any rule, law or its own code.

## Done means

- `kb verify`: VERIFIED 59, REFERENCED 1, UNVERIFIED 4, all hashes match (show output); the two operator SHA-256 match
  hq's.
- Quote-in-stored-text check passes for every new `searched` quote (show count).
- Data check passes; register, site and datasheet rebuilt twice, identical.
- Recorded runs replay as recorded; `verify-log` passes on every stored log.
- Full test suite passes; CI green on the PR.
- Report 5 pages (Word count, as in Task 30). hq copy `report-draft-2026-10-23.md` matches `docs/report.md`.
- Report-back at `docs/report-back/2026-10-30-task-32-operator-codes.md`, with the table of checks.

## Limits

No change to gates, keys, runs, prompts, chunks or eval. Seven layers (`engineering/_reference/llm-agents.md`):
unchanged from Task 31, nothing shipped or deferred by this task, no agent code touched. No other gap rows. USD 0 model
spend. Every change done before 2026-11-06.

## Stop and ask when

- Either operator PDF's SHA-256 differs from hq's (the operator may have republished; do not take hq's copy).
- The pipeline will not accept hq's 106/2026 files as local sources.
- The report leaves 5 pages after dropping the row 1 addition.
- `csc-ai-security-policy-v1-1.pdf` exists in hq's `standards-text/` when you start.
- The schema needs a change beyond the `operator code` value.
