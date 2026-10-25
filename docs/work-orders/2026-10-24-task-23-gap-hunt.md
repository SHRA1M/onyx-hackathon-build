# Task 23: four gap rows corrected, gap 11 (a misheard order) added, three UAE texts and six global extracts into the KB (2026-10-24)

Repo: `D:\Projects\engineering\onyx-hackathon-build`. Builds on the head after Task 22 (1aeb31a or later; name it). No model
calls, USD 0. Words and data only: no gate, rule, key, prompt, scorer or run changes. Source of every decision:
`D:\Projects\hq\uni\ai-for-good-hackathon\perplexity-2026-10-24\gap-hunt-read-2026-10-24-fable.md` (hq, Fable).

Why: a Perplexity audit, checked by hq against the texts, found that rows 2, 4, 6 and 9 of the report's gap table can be
pushed back on by a judge who knows the CPR and the PDPL (CPR 4.7.2 accepts stored spoken consent; PDPL 24 gives a complaint
route to the Data Office; ET 11(2) is not "sales only"; Resolution 106/2026 exists). It also surfaced a gap stronger than gap 7
for a TDRA judge: nothing tells a voice or chat channel to read back the order it understood before the OTP.

## Part A: knowledge base

A1. Add these documents with `kb fetch` (or the same steps by hand), file on disk, SHA-256, status VERIFIED, binding_status
and notes as given. Do not commit a manifest whose only change in an existing row is a refreshed `url_accessed`.

| document_id | title | url | notes |
|---|---|---|---|
| law-14-2023-en | Federal Decree-Law No. 14 of 2023 Concerning the Modern Technology-Based Trade | https://uaelegislation.gov.ae/en/legislations/2150/download | binding; Ministry of Economy; applies to the sale of goods and services through modern technology (Art 2); whether a licensee's care channel is "trade" under it is an interpretation. Arabic prevails. |
| law-14-2023-ar | Federal Decree-Law No. 14 of 2023, Arabic | https://uaelegislation.gov.ae/ar/legislations/2150/download | as above |
| cabres-28-2023-en | Cabinet Resolution No. 28 of 2023, Executive Regulations of Federal Decree-Law 46/2021 | https://uaelegislation.gov.ae/en/legislations/2199/download | binding; trust service providers; Art 15(9), 24(3) |
| tdra-registration-policy-2011-en | TDRA Regulatory Policy: Registration Requirements for Mobile Consumers, v1.0 (2011-09-27) | https://tdra.gov.ae/-/media/About/regulations-and-ruling/EN/Registration-Requirements-for-Mobile-Consumers-Policy-pdf.ashx | binding regulatory policy; registration-time identity checks (6.1) |

If uaelegislation.gov.ae refuses the download to a script (it serves a challenge page, 5 KB of HTML), do not work around it.
Look in `D:\Projects\hq\uni\ai-for-good-hackathon\perplexity-2026-10-24\fetched-2026-10-24\` for `law-14-2023-en.pdf`,
`law-14-2023-ar.pdf`, `cabres-28-2023-en.pdf` of PDF type (`%PDF` header). If they are there, use them and record the portal URL
as the source. If not, stop and ask.

A2. Add these global extracts under `kb/sources/global/` the way `coppa-16cfr312-5.txt` was made (fetched text, the articles
named, URL, date, SHA-256), status VERIFIED, `license_note` as for the existing EU rows:

| document_id | text and articles | url |
|---|---|---|
| eu-dsa-2022-2065-art12-20 | Regulation (EU) 2022/2065 (DSA), Articles 12 and 20 | https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32022R2065 |
| eu-crd-2011-83-art8 | Directive 2011/83/EU (Consumer Rights), Article 8, consolidated | https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:02011L0083-20260927 |
| eu-ecommerce-2000-31-art10-11 | Directive 2000/31/EC (e-Commerce), Articles 10 and 11, consolidated | https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:02000L0031-20240217 |
| gdpr-art12-28-33 | Regulation (EU) 2016/679, Articles 12, 28 and 33 | https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:02016R0679-20160504 |
| us-47cfr-64-2010 | 47 CFR 64.2010, Safeguards on the disclosure of CPNI | https://www.ecfr.gov/current/title-47/chapter-I/subchapter-B/part-64/subpart-U/section-64.2010 |
| ca-ola-s22-27 | Canada, Official Languages Act, ss. 22 to 27 | https://laws-lois.justice.gc.ca/eng/acts/O-3.01/page-3.html (if the section is on another page of the Act, use that page and record it) |

Then paste into the report-back, verbatim from the fetched files, these clauses so hq can read them: DSA 12(1) and 20(6);
CRD 8(2); e-Commerce 11(2); GDPR 12(3), 12(4), 28(2), 33(1); 47 CFR 64.2010(b); OLA ss. 22, 26, 27. If a fetched text does
not contain a clause the table below cites, stop and ask before the report changes.

## Part B: the register (`onyx/data/gaps.json`; regenerate `docs/gaps.md` and the README table as Task 9 did)

B1. New entry `gap-11`, same fields as the others:
- `line`: "a misheard order"
- `gap`: "A misheard or misread order: the CPR defaults an on-screen yes/no to 'no' to avoid an accidental 'yes' (4.22.3, 4.23.3), requires an OTP for each online purchase (4.23.2) and a recording of verbal consent on telephone sales (4.17.3); no text says what a voice or chat channel must do when it interprets the subscriber's words itself, so 'don't add it' heard as 'add it' reaches the OTP step without being read back."
- `kind`: "standards"; `category`: "standards gap"; `addressee`: ["TDRA"]
- `searched`: CPR 4.7.1 (positive affirmative action), 4.10 (no single click, multi-step), 4.11 (default 2FA is OTP), 4.17.3, 4.22.3, 4.23.2, 4.23.3, each with its quote from `tdra-cpr-v2-en` and the Arabic from `tdra-cpr-v2-ar`; ET Law 12(7) ("an error has occurred in the Electronic Document as a result of a technical failure during transmission") and 11(2); Trade Law 14/2023 Art 5(5) and 6(7) (once in the KB).
- `uae_position`: "The CPR already knows the problem on a screen: the safe default is 'no' (4.22.3, 4.23.3) and a purchase needs a second factor (4.23.2). On a voice or chat channel the system, not the subscriber, decides what was said; the OTP then confirms that the subscriber wants something, not that the channel understood the right thing. ET 12(7) reaches transmission errors only. No published TDRA text requires the channel to state the service, price and term it understood and take a correction before the second factor."
- `global_examples`: e-Commerce Directive 2000/31 Art 11(2) and CRD 2011/83 Art 8(2), quotes copied from the fetched extracts (Part A2), status VERIFIED.
- `recommendation`: "TDRA: on a voice or chat channel, before the 2FA step, the channel states the service, price and term it understood and accepts a correction; the read-back is logged with the consent record (sub-article 3.9)."
- `exposed_by`: "mapping (P); S1 step 3 (bundle offered, hold until the OTP and the consent form) is the step where the rule would apply; not in a recorded run."
- `competitor`: "not read"; `competitor_basis`: "order 2026-10-24 Task 23".

B2. Reword existing entries (the `gap` field; keep everything else, extend `searched` where named):
- gap-2 `gap`: "Consent elicited by an AI: the CPR accepts spoken consent if it can be stored (4.7.2) and decides by sales medium (4.10, 4.17, 4.22) whether an OTP is needed, naming no AI channel; the PDPL wants consent to the data processing 'in writing or electronically' (6(1)(b)); one spoken 'yes' can buy the service and still not permit the data use, and nobody has said which medium an AI chat or voice agent is." Add CPR 4.7.2 and Trade Law 14/2023 Art 13(2) to `searched`.
- gap-4 `gap`: "Automated disconnection: the PDPL 18(4) human review has no procedure or deadline; the only route is a complaint to the Data Office (Art 24), which has no clock either (Art 25's 30 days apply to grievances against the Office's own decisions)." Add PDPL 24(1), 24(2), 25 to `searched`.
- gap-6 `gap`: "AI disclosure: no general duty to tell a consumer they are talking to an AI; Electronic Transactions 11(2) asks only that the person 'knows, or is supposed to know, that such system will make or execute the contract automatically'." Add Trade Law 14/2023 Art 1 ("Modern Technology") to `searched`.
- gap-7 `gap`: "No binding UAE text sets conduct standards specific to an AI agent dealing with a consumer: CPR 3.3's duty of fairness and accurate information is general; Trade Law 14/2023 names AI in its definition (Art 1) and bars misleading dealing (Art 5(7)); nothing names disclosure, limits, escalation or a hand-over for an automated agent." Add CPR 3.3 and Trade Law Art 1, 5(7) to `searched`.
- gap-9 `gap`: "A child on the line: the caregiver signs the terms (Child Digital Safety Law 26/2025, 11(1)(b)) and under-13 data needs verified caregiver consent (7(1)); the Art 11 instructions to providers and the Art 16 penalties are unpublished, and Cabinet Resolution 106/2026's age checks reach social media platforms only (Art 2); nothing says how a telecom channel learns the person is a child."
- gap-1 `searched`: add Trade Law 14/2023 Art 6(7) ("always available without interruption with qualified staff"): a staffed complaint channel, no stop, hand-over or clock for an AI chat.
- gap-3 `searched`: add Registration Policy 6.1.1, 6.1.2 and Cabinet Resolution 28/2023 Art 15(9), 24(3), with the note that both address other events (registration; qualified certificates) and neither maps a telecom-care act to a trust level.

B3. Two new `candidates`, same shape as the existing ones, from the Perplexity read: breach-notification clock (PDPL 9(1), 9(2)
delegate the period to the unissued Executive Regulations; GDPR 33(1) as the example) and sub-processor authorisation (PDPL 7(5),
8(1), 8(10); GDPR 28(2) as the example). Short entries; hq will finish them after the shortlist.

## Part C: the report (`docs/report.md`), exact text

Old text quoted exactly; a line break inside a quoted sentence may differ. Anything else that differs: stop and ask.

C1. Row 2, old:
```
| 2 | Consent elicited by an AI: the CPR sales-medium classification (4.10, 4.17, 4.22) decides whether an OTP is needed; PDPL 6(1)(b) names written or electronic consent, not spoken | coordination | TDRA, UAE Data Office | EU AI Act Art 50(1); IMDA 2.2.2 |
```
new:
```
| 2 | Consent elicited by an AI: the CPR accepts stored spoken consent (4.7.2) and sets the OTP need by sales medium (4.10, 4.17, 4.22), naming no AI channel; the PDPL wants the data consent written or electronic (6(1)(b)), so one spoken "yes" can buy the service and still not permit the data use | coordination | TDRA, UAE Data Office | CRD 2011/83 Art 8(2); IMDA 2.2.2 |
```

C2. Row 4, old:
```
| 4 | Automated disconnection: the PDPL 18(4) human review has no procedure, deadline or regulator; a subscriber who contests it has nothing to wait for and nobody to turn to | responsibilities | UAE Data Office | GDPR Art 22(3) |
```
new:
```
| 4 | Automated disconnection: the PDPL 18(4) human review has no procedure or deadline, and the complaint route to the Data Office (Art 24) has no clock either, so a subscriber who contests it has nothing to wait for | responsibilities | UAE Data Office | GDPR Art 22(3), 12(3) |
```

C3. Row 6, old:
```
| 6 | AI disclosure: no general duty to tell a consumer they are talking to an AI; Electronic Transactions 11(2) makes it a validity condition for sales only | legislative | Cabinet | EU AI Act Art 50(1), 50(5) |
```
new:
```
| 6 | AI disclosure: no general duty to tell a consumer they are talking to an AI; Electronic Transactions 11(2) asks only that the person "knows, or is supposed to know" the system contracts automatically | legislative | Cabinet | EU AI Act Art 50(1), 50(5) |
```

C4. Row 7, old:
```
| 7 | No binding UAE text sets conduct standards for an AI agent dealing with a consumer | standards | TDRA | IMDA 2.1.2 |
```
Delete it. In its place (same position, after row 6 and before row 8) insert:
```
| 11 | A misheard order: the CPR defaults an on-screen answer to "no" to avoid an accidental "yes" (4.22.3, 4.23.3) and wants an OTP per purchase (4.23.2); nothing says what a voice or chat channel must do when it interprets the words itself, so "don't add it" heard as "add it" reaches the OTP unread back | standards | TDRA | E-Commerce Dir. 2000/31 Art 11(2) |
```

C5. Row 9, old:
```
| 9 | A child on the line: the caregiver signs the terms (Child Digital Safety Law 26/2025, 11(1)(b)) and under-13 data needs verified caregiver consent (7(1)); the implementing texts (Arts 6, 11, 16) are unpublished; nothing says how an automated channel learns the person is a child | legislative | TDRA, Cabinet | US COPPA Rule, 16 CFR 312.5(a)(1), (b)(1) |
```
new:
```
| 9 | A child on the line: the caregiver signs the terms (Child Digital Safety Law 26/2025, 11(1)(b)) and under-13 data needs verified caregiver consent (7(1)); the Art 11 instructions and Art 16 penalties are unpublished, and Resolution 106/2026's age checks reach social media only (Art 2); nothing says how a telecom channel learns the person is a child | legislative | TDRA, Cabinet | US COPPA Rule, 16 CFR 312.5(a)(1), (b)(1) |
```

C6. Gap section intro. After the sentence ending `The addressee is the body whose text would close it.` append, same paragraph:
```
 Gap 7 and four candidates stay in the register.
```

C7. Recommendations. Old: `conduct standards for AI agents in consumer care (7);` new:
```
a read-back of the understood order before the OTP on voice and chat channels (11);
```

C8. Introduction, KB paragraph. After Part A the counts change. Old: `The knowledge base holds 40 documents:` and
`four foreign texts used only as global examples. 36 are verified:`. Replace 40, "four" and 36 with the manifest's new totals
(documents; foreign global-example texts; VERIFIED rows), written as words where the old text used words. State the three
numbers and how you counted them in the report-back.

C9. Rebuild `report.docx`, count pages in Word as before.

Five pages: finish.

Six pages, one step at a time, recount after each, stop at the first five:
1. Row 2 becomes: `| 2 | Consent elicited by an AI: the CPR accepts stored spoken consent (4.7.2) and sets the OTP need by sales medium (4.10, 4.17, 4.22), naming no AI channel; the PDPL wants the data consent written or electronic (6(1)(b)) | coordination | TDRA, UAE Data Office | CRD 2011/83 Art 8(2); IMDA 2.2.2 |`
2. Row 4: drop `, so a subscriber who contests it has nothing to wait for`.
3. Row 11: drop `, so "don't add it" heard as "add it" reaches the OTP unread back`.
4. Drop the C6 sentence.
Still six: stop and report the count and the first sentence on page 6.

## Sources

Only: the fetched files of Part A, `docs/report.md`, `onyx/data/gaps.json`, `kb/manifest.csv`, and this order. Quotes for the
register come from the KB text files, never from this order's paraphrases: where this order paraphrases a clause, copy the
clause from the file.

## Done means (hq checks; show each output)

1. `git diff --stat <base>` lists only: `kb/manifest.csv`, new files under `kb/sources/`, `onyx/data/gaps.json`, `docs/gaps.md`,
   `README.md` (table only), `docs/report.md`, `docs/report.docx`, `CHANGELOG.md`, the filed order, the report-back.
2. `git diff <base> -- kb/manifest.csv` shows added rows only; no existing row changed.
3. Every new manifest row: file present, SHA-256 matches, status VERIFIED. Print `document_id, status, sha256[:12]` for each.
4. The register: `gap-11` present with every field filled; gaps 1, 2, 3, 4, 6, 7, 9 changed as in Part B; two new candidates; the
   count line in `docs/gaps.md` says 11 gaps.
5. Report diff shows C1 to C8 and nothing else; `git diff <base> -- docs/report.md | grep -E '^[-+].*\[C[35]'` prints nothing.
6. `git diff c5cea32 -- onyx/gate.py onyx/data/rules.json onyx/data/keys onyx/data/mandates.json onyx/eval.py runs/` prints nothing.
7. `eval` recomputed from the logs: `git diff -- eval/results.md eval/results.json` prints nothing.
8. Pages 5 (Word count stated), ladder steps named.
9. Tests pass, CI green, committed, pushed; report-back at `docs/report-back/2026-10-24-task-23-gap-hunt.md` carrying the
   verbatim clauses of Part A2.

## Limits

- No change to gates, rules, keys, mandates, prompts, scorer, runs, figures or tagged paragraphs.
- No other entry's name in any tracked file.
- Stop and ask: a blocked download with no file in the hq folder; a fetched text missing a cited clause; any quoted old text not
  found; the ladder running out; `eval` output changing.
