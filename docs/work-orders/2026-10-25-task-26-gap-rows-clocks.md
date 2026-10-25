# Task 26: rows 1 and 2 pre-empt the CPR clocks and PDPL 4(9); searched lists extended (2026-10-25)

Repo: `D:\Projects\engineering\onyx-hackathon-build`. Builds on `main` at 746c2bd or later (name it). No model calls, USD 0.
Words and data only: no gate, rule, key, scenario, prompt, scorer, run or KB change. Source of every decision:
`D:\Projects\hq\uni\ai-for-good-hackathon\perplexity-2026-10-25\gap-hunt-2-read-2026-10-25-fable.md` (hq, Fable).

Why: a second Perplexity audit, checked by hq against the texts, found two rows a judge can push back on. Row 1 says the
complaint hand-over has no clock; CPR 26.13.3 and 26.14.2 are clocks for the complaint, and the report's own D row cites
26.13.2 and 26.13.3. Row 2 says a spoken "yes" does not permit the data use; PDPL 4(9) permits the processing the contract
needs without consent. Both gaps stand, narrower. Four searched lists gain the clauses Perplexity raised.

## Part A: the register (`onyx/data/gaps.json`; regenerate `docs/gaps.md`, the README table and `docs/site/gaps.html` the
way Tasks 9, 23 and 25 did)

Every added `searched` entry has the same three fields as the existing ones: `clause`, `says`, `quote`. The English quote
is given here; take it verbatim from `kb/chunks-full/<document_id>.jsonl` (not from this file) and add the Arabic from
`tdra-cpr-v2-ar` or `pdpl-45-2021-ar` where the existing entries of that gap carry Arabic. hq found all thirteen in
`chunks-full`; seven are not in `kb/chunks` (CPR 26.2, 26.14.1; PDPL 4(9), 11(1)(b), 12(2); ET 12(4)(c), 13(5)). If any test
or selftest checks register quotes against `kb/chunks`, do not add chunks: stop and ask. If a quote below is not found
verbatim in `chunks-full`, stop and ask.

A1. gap-1.
- `gap`: "Complaint hand-over: the trigger and the human are sourced (CPR 2.1.7, 26.7.2, licence 9.1) and the complaint has clocks (acknowledge at once by telephone, 26.13.3; conclude in twenty business days, 26.14.2); the transfer has none: what the agent does when the conversation turns, when the human is in it, whether the time is recorded. QoS T1(2a) measures only the wait after the IVR choice."
- `uae_position`: "The human requirement is binding (26.7.2, licence 9.1) and Mizan enforces it. The CPR wants first-contact resolution (26.14.1) and bars the machine from the conversation (26.7.2); nothing joins the two: no text says what an automated channel must do at the moment a conversation becomes a complaint, or how fast the human must take over. The acknowledgement clock (26.13.3) names telephone, visit and written complaints, not chat or app, and a reference number is not a conversation."
- `searched`, add after 26.13.1:
  - `tdra-cpr-v2-en:26.2`, says "Complaints resolved properly and promptly; no step for the moment an automated conversation turns into one.", quote "investigate and resolve Consumer Complaints properly and promptly"
  - `tdra-cpr-v2-en:26.6`, says "Trained people respond in a timely and prompt manner; no time stated.", quote "receive, process, and respond to Consumer Complaints in a timely and prompt manner"
  - `tdra-cpr-v2-en:26.13.2`, says "Acknowledgement with a reference number and an indicative time-frame; nothing on who or what issues it on an automated channel.", quote "acknowledge the receipt of each Consumer Complaint by providing the complainant with a reference number for the complaint and the indicative time-frame"
  - `tdra-cpr-v2-en:26.13.3`, says "The acknowledgement clock: at once by telephone or visit, one business day for a written complaint. Chat and app are not named; an acknowledgement is not a hand-over.", quote "immediately in the case of complaints submitted by telephone or personal visit, and within one (1) business day in the case of a written complaint"
  - `tdra-cpr-v2-en:26.14.1`, says "Resolve on first contact where possible; with 26.7.2 the first contact on an automated channel cannot be the one that resolves.", quote "Where possible, Licensees shall seek to resolve a Consumer Complaint on first contact."
  - `tdra-cpr-v2-en:26.14.2`, says "The conclusion clock: twenty business days. A clock for the complaint, not for the transfer to a person.", quote "conclude Consumer Complaints within twenty (20) business days after receipt or as soon as practical in all circumstances"
- Everything else unchanged.

A2. gap-2.
- `gap`: "Consent elicited by an AI: the CPR accepts spoken consent if it can be stored (4.7.2) and decides by sales medium (4.10, 4.17, 4.22) whether an OTP is needed, naming no AI channel; the PDPL permits the processing the contract needs without consent (4(9)) and wants any further processing consented 'in writing or electronically' (6(1)(b)); one spoken 'yes' buys the service and consents to nothing beyond it, and nobody has said which medium an AI chat or voice agent is."
- `uae_position`: "No CPR sales medium names a conversational agent, so whether an AI-elicited purchase needs an OTP depends on a classification no text makes. The processing the contract needs is lawful without consent (4(9)); a spoken consent through the agent covers the purchase (4.7.2) but not a processing purpose beyond the contract, which 6(1)(b) wants in writing or electronically. Mizan takes the strict reading (4.10 plus OTP, 4.11)."
- `searched`, add before `pdpl-45-2021-en:6(1)`:
  - `pdpl-45-2021-en:4(9)`, says "Processing the contract needs is permitted without consent; the seam is only for processing beyond it.", quote "If the processing is necessary to perform a contract to which the Data Subject is a party, or to take measures at the request of the Data Subject with the aim of concluding, amending or terminating a contract."
- Everything else unchanged.

A3. gap-4, `searched`, add after `pdpl-45-2021-en:18(4)`:
  - `pdpl-45-2021-en:11(1)(b)`, says "The Data Protection Officer receives requests and complaints: an internal route, no deadline.", quote "Receiving requests and complaints related to Personal Data in accordance with provisions of this Decree-Law and its Executive Regulations."
  - `pdpl-45-2021-en:12(2)`, says "The data subject may go straight to the DPO; no response time.", quote "The Data Subject may communicate directly with the Data Protection Officer about all matters relating to his/ her personal data processing"

A4. gap-5: no field change. In the report-back, state what the manifest records for the Executive Regulations search
(row `pdpl-executive-regulations`, its date) and whether any row records a search for the Article 22 country list. Do not
add a row.

A5. gap-10, `searched`, add:
  - `tdra-cpr-v2-en:26.2`, says "An unqualified standard, 'properly and promptly', that applies to Arabic as to English; no measure per language.", quote "investigate and resolve Consumer Complaints properly and promptly"
  - `tdra-cpr-v2-en:26.6`, says "'Properly trained' personnel; nothing on the language they answer in or how well.", quote "an adequate number of properly trained personal to receive, process, and respond to Consumer Complaints"
  (The CPR's own spelling "personal" stays in the quote.)

A6. gap-11, `searched`, add after `etransactions-46-2021-en:12(7)`:
  - `etransactions-46-2021-en:12(4)(c)`, says "An addressee may not rely on a document it is unreasonable to attribute to the originator; a transcript of the subscriber's words is the operator's own system's output, not a document the subscriber issued.", quote "If it is unreasonable for the Addressee to consider the Electronic Document to be issued by the Originator or to act on this basis."
  - `etransactions-46-2021-en:13(5)`, says "The law separates receipt from content; it imposes no read-back of the content understood.", quote "an acknowledgment of receipt does not mean acknowledgment of the content of the Electronic Document."

## Part B: the report (`docs/report.md`, then `docs/report.docx` as before), exact text

Old text quoted exactly; a line break inside a quoted sentence may differ. Anything else that differs: stop and ask.

B1. Row 1, old:
```
| 1 | Complaint hand-over: the bar and the human are sourced (CPR 2.1.7, 26.7.2, licence 9.1); the stop, the hand-over and its clock are not, so the subscriber stays with the machine and no record shows when it stopped | standards | TDRA | IMDA 2.2.2, 2.4.2 |
```
new:
```
| 1 | Complaint hand-over: the bar and the human are sourced (CPR 2.1.7, 26.7.2, licence 9.1) and the complaint has clocks (acknowledge at once by telephone, 26.13.3; conclude in twenty business days, 26.14.2); the transfer has none: what the agent does when the conversation turns, when the human is in it, whether the time is recorded | standards | TDRA | IMDA 2.2.2, 2.4.2 |
```

B2. Row 2, old:
```
| 2 | Consent elicited by an AI: the CPR accepts stored spoken consent (4.7.2) and sets the OTP need by sales medium (4.10, 4.17, 4.22), naming no AI channel; the PDPL wants the data consent written or electronic (6(1)(b)) | coordination | TDRA, UAE Data Office | CRD 2011/83 Art 8(2); IMDA 2.2.2 |
```
new:
```
| 2 | Consent elicited by an AI: the CPR accepts stored spoken consent (4.7.2) and sets the OTP need by sales medium (4.10, 4.17, 4.22), naming no AI channel; the PDPL exempts what the contract needs (4(9)) and wants any further data use consented in writing or electronically (6(1)(b)), so a spoken "yes" buys the service and consents to nothing beyond it | coordination | TDRA, UAE Data Office | CRD 2011/83 Art 8(2); IMDA 2.2.2 |
```

B3. Row 5, old text contains:
```
the machinery (Art 22 list, 23(2), 8(11)) was never issued, so an operator
```
new:
```
the machinery (Art 22 list, 23(2), 8(11)) has not been issued, so an operator
```
If the row reads differently, stop and ask.

B4. Page count. The report must stay at five pages (Word count stated in the report-back). If B1 and B2 push it over, cut, in
this order, and name each cut: (1) in row 1, ", whether the time is recorded"; (2) in row 2, " and consents to nothing beyond
it". If still over, stop and ask.

B5. `docs/site/gaps.html` shows the new row text for gaps 1 and 2 after regeneration; the D row of the mapping table is
unchanged (it already cites 26.13.2 and 26.13.3 and now agrees with row 1).

## Done means (hq checks; show each output)

1. `git diff --stat <base>` lists only: `onyx/data/gaps.json`, `docs/gaps.md`, `README.md` (table only), `docs/site/gaps.html`,
   `docs/report.md`, `docs/report.docx`, `CHANGELOG.md`, the filed order, the report-back.
2. The register: gaps 1, 2 reworded as A1, A2; searched counts before and after for gaps 1, 2, 4, 10, 11 (expected +6, +1,
   +2, +2, +2); every added entry has `clause`, `says`, `quote`; the count line in `docs/gaps.md` still says 11 gaps.
3. Each added quote found verbatim in `kb/chunks-full/<document_id>.jsonl`: print `clause, file, chunk id` for the 13 entries.
4. Report diff shows B1, B2, B3 and nothing else; `git diff <base> -- docs/report.md | grep -E '^[-+].*\[C[35]'` prints nothing.
5. `git diff <base> -- onyx/gate.py onyx/data/rules.json onyx/data/keys onyx/data/scenarios onyx/data/mandates.json onyx/eval.py runs/ kb/` prints nothing.
6. `eval` recomputed from the logs: `git diff -- eval/results.md eval/results.json` prints nothing.
7. Pages 5 (Word count stated), cuts named or "none".
8. A4's manifest statement in the report-back.
9. Tests pass, CI green, committed, pushed; report-back at `docs/report-back/2026-10-25-task-26-gap-rows-clocks.md`.

## Limits

- No change to gates, rules, keys, scenarios, mandates, prompts, scorer, runs, figures, the KB or tagged paragraphs.
- No other entry's name in any tracked file.
- Stop and ask: a quote not found verbatim in the KB file; any quoted old text not found; the cut ladder running out; `eval`
  output changing.
