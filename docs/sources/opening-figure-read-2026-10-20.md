# Opening figure: sources read and the pick (2026-10-20, Fable)

Input: `uae-telecom-evidence-brief-v1.1-2026-10-20.docx` (Perplexity, "Decision-Team Evidence Brief", research cut-off
2026-10-20; text in the `.txt` beside it). Every source it cites was opened here, not taken from the brief. Work order
item 25 is settled from this file.

## What was opened

| # | Source | How read | Verdict |
|---|---|---|---|
| 1 | e&, *Sustainability Report Appendices 2025*, PDF | Downloaded, `pdftotext`, page 7 read | Primary. Figures match the brief exactly. |
| 2 | TDRA press release 2024-04-02, English and Arabic | Page text fetched | Primary. Quotes match. |
| 3 | Etisalat's Virtual Assistant page (eand.ae) | Page text fetched | Primary. Quotes match. |
| 4 | Al Bayan 2025-04-02 (brief says 04-03 from metadata; the page shows الأربعاء 2/4/2025 2:11 م) | Page text fetched | Secondary. TDRA's own table not found. |
| 5 | Emarat Al Youm 2023-11-11 | Page text fetched | Secondary. TDRA's own report not found. |
| 6 | du sustainability reports 2024, 2025 | Not opened (brief: GRI 418-1 "Not disclosed – confidentiality"; no total) | Not needed for the pick. |
| 7 | TDRA open data, data-sets page | Fetch timed out after 120 s, once | Not read. The brief found no populated export either. |

## 1. e& (primary): the figure

File: `../standards-text/eand-sustainability-report-appendices-2025.pdf`, text beside it.
SHA-256: `f461044ff85b670d7861470a6f84564e4e5a0a0c36c5487c21d62b256a27b91c`.
URL: https://www.eand.com/content/dam/eand/assets/docs/sustainability/2025/eand-sustainability-report-appendices.pdf
Page: PDF page 7 (printed 6), Appendix 1 "Performance data", block "Responsible commercialisation", column header
"YoY data (UAE data)", years 2023, 2024, 2025.

| Row (verbatim label) | 2023 | 2024 | 2025 |
|---|---|---|---|
| Number of customer complaints | 411,752 | 389,387 | 371,476 |
| Percentage of customer complaints resolved (%) | 94 | 91 | 88 |
| Percentage of first call resolution (%) | 73 | 78 | 81 |

Also on PDF page 6, block "Data privacy", UAE data: 0 (2023), 0 (2024), "NA*" (2025), footnote "*Data is unavailable at
the time of publication". A breach row, not a complaint count.

Cover text: "We have retained trend-based reporting for UAE performance, offering clear year-on-year consumption data
across a three-year period." No publication date printed; reporting year 2025.

## 2. TDRA release 2024-04-02 (primary)

EN: https://tdra.gov.ae/en/media/press-release/2024/new-press-release (page footer "Last updated 02/04/2024 14:13").
AR: https://tdra.gov.ae/ar/media/press-release/2024/new-press-release.
Section "Dispute Resolutions with Service Providers". Verbatim EN: "Statistics show that approximately 70% of customer
disputes have been resolved upon the initial contact ... Introducing artificial intelligence into the service
implementation stages has revolutionized the process, enabling precise classification of disputes and accurate
estimation of resolution times." Satisfaction for the service "from 84% to 89%". Steps cut from four to one, form to
one field, zero documents.
Verbatim AR: "وقد تم إدخال الذكاء الاصطناعي ضمن مراحل تنفيذ الخدمة بهدف تصنيف المشكلة وإرسال الوقت المتوقع لحلها بشكل دقيق".
This is TDRA's own dispute service, not a licensee's care channel. No annual complaint count in the release.

## 3. Etisalat's Virtual Assistant (primary)

https://www.eand.ae/en/c/etisalat-virtual-assistant.html, read 2026-10-20. Verbatim: "Our AI (Artificial Intelligence)
powered Virtual Assistant is at your service 24*7." "You can speak/ chat naturally with Etisalat's Virtual Assistant in
English or Arabic". Channels: My Etisalat UAE App, www.etisalat.ae/support, "Or call 101". Jobs listed: "Account
management related help such as changing your language settings or your email address settings, adding or deleting
services, changing of packages etc."; "Billing related clarifications and technical support"; "50+ products and
services related inquiries". Also on the page: "Our virtual assistant is easier and quicker than speaking to a human".
No launch date. Nothing says generative or agentic.

## 4 and 5. Press figures attributed to TDRA (secondary)

Al Bayan, https://www.albayan.ae/economy/business/uae-economy/36938: TDRA received 2,900 complaints in Q1 2025 "بالتنسيق مع
المشغلين", down 34% year on year; 95% resolved; about 3,300 in Q4 2024; 951 in March 2025; operators closed 93 to 95%;
mobile is the largest share against 22.2 million mobile subscribers and 2.4 million fixed; satisfaction 95 to 99%
against 84 to 86% a year earlier; resolution cap 5 working days.
Emarat Al Youm, https://www.emaratalyoum.com/business/local/2023-11-11-1.1798956: 20,427 complaints to TDRA January to
October 2023 (e& 6,670; du 13,757), against 21,499 the year before.
Neither article links TDRA's table. Not for the opening; footnote at most, labelled "press report citing TDRA".

## The pick

Opening figure: **e& UAE, 371,476 customer complaints in 2025**, 88% resolved, 81% first-call resolution (source 1).
Paired in the same paragraph with source 3: the operator's care channel is an AI assistant, 24/7, English or Arabic, whose
listed jobs include adding or deleting services, changing packages and billing. The two together make the headline
concrete: hundreds of thousands of care conversations a year at one operator, and the first contact is an AI that can
change what the subscriber pays for.

Why not the others: no TDRA publication with a count was found (item 25's first preference); the press figures are
secondary and the brief's own rules forbid annualising them; the TDRA release has no count and is about the regulator's
own service, so it goes in the "existing solutions" paragraph as evidence that AI already sits in the complaint
pipeline on the regulator's side, which makes the operator-side rule (CPR 26.7.2) the interesting boundary.

Wording rules, each one a judge's likely push-back:
- "e& reported ... in its UAE operations for the 2025 reporting year". Never "the UAE sector", never "TDRA received",
  never a per-day or per-minute conversion, never "unique customers".
- Complaints fell 411,752 to 371,476 while the resolved share fell 94 to 88 and first-call resolution rose 73 to 81. State
  none of this as an AI effect. The table gives no cause.
- The assistant: "AI-powered", the page's words. Not "agent", not "generative", no launch date.
- du: GRI 418-1 withheld; no total. Virgin Mobile UAE: no standalone figure. Do not rank operators.

Not done: TDRA open data (one fetch, timed out); du PDFs not opened; no e& publication date found.

## Second round, same day: TDRA's own counts (Fable, 2026-10-20 afternoon)

Input: `tdra-official-complaint-statistics-2020-2026.docx` (Perplexity, from the prompt written this morning; text beside
it). Every figure below was opened here, not taken from the brief.

### TDRA Sustainability Report 2023 (primary): the regulator's count

EN: https://tdra.gov.ae/-/media/Media/Press-Kit/Sustainability-Report/EN/Sustainability-report-2023-English.ashx,
file `../standards-text/tdra-sustainability-report-2023-en.pdf`, SHA-256
`0ac6aa6c704a9e4284fa03ad58fd4c3761edc4f08c12b6bc67a6647697f0a1fa`, full text beside it.
AR: https://tdra.gov.ae/-/media/Media/Press-Kit/Sustainability-Report/AR/Sustainability-Report-2023-Ar.ashx, SHA-256
`96ae946b248cdc74d1280060456cdb815a40fd3f5d99d6fba1db3eeed4132721`, pages 33 to 36 text in
`../standards-text/tdra-sustainability-report-2023-ar-p33-36.txt` (PDF not kept, 19 MB).
PDF page 34, heading "Consumer complaints", verbatim: "In 2023, the Authority dealt with 23,464 complaints submitted by
business and home subscribers regarding licensees". Series: 2020 32,998; 2021 29,727; 2022 26,745; 2023 23,464. The
Arabic page 34 carries the same four values. No publication date inside the PDF; TDRA's catalogue shows 01/01/2024.
PDF page 35, dispute resolution service: "Reduction of dispute resolution requests" 9103 (2022), 6549 (2023), unit not
stated, do not use; "Percentage of closed requests ... on time" 35% Q4 2022, 63% Q4 2023, 85% Q1 2024; turnaround
14.9 days (Q4 2022) to 10.5 (Q4 2023); satisfaction 84% (Q1 2022) to 89% (Q1 2023).
Checked here: the 2024 and 2025 English sustainability reports (same catalogue) contain the word "complaint" only in a
system name ("Complaints Handling"), no count. So 2023 is the latest count TDRA has published.

### TDRA posts of 2026-04-01 (primary, social): telemarketing complaints

Instagram https://www.instagram.com/p/DWmJE3fDOo9/ (shows "April 1") and LinkedIn
https://www.linkedin.com/posts/tdra_marketingcalls-digitalsafety-activity-7445146615436402688-bAKf, identical text:
"TDRA Efforts in Implementing UAE Cabinet Resolutions No. 56 and 57 of 2024. During 2025, TDRA undertook several
actions related to violations committed by individuals, resulting in the following outcomes: Total complaints received:
334,116 complaints; Total reported numbers: 48,519 numbers; Total violations recorded: 2,725 violations; Total fines
imposed: AED 15,320,000." The matching tdra.gov.ae press release URL in the brief returns 404. Scope: individuals'
telemarketing violations, not complaints against licensees.

### Press (secondary), not for the report

Emarat Al Youm 2024-01-02 (https://www.emaratalyoum.com/business/local/2024-01-02-1.1813704): 23,335 complaints in 2023
(e& 7,371; du 15,964), closure 98.6% and 96.9%, satisfaction 74.3% and 79.8%; earlier years 26,095 / 27,864 / 32,534.
The newspaper's 2023 total differs from TDRA's own 23,464; TDRA's per-operator report is not online. Tempting and
forbidden: dividing e&'s 411,752 (2023) by the press's 7,371 to get an escalation rate.

### The pick, revised

Opening, two sentences, both primary: lead with e& UAE 371,476 complaints in 2025 (the care workload where the AI
sits, the newest figure), then TDRA: "the regulator itself dealt with 23,464 complaints about licensees in 2023, the
latest count it has published". Different years and receivers: no ratio, no "of which". Then the AI channel sentence
(Etisalat's Virtual Assistant) and the harm. The TDRA figure answers the "one operator only" push-back and shows the
escalation path the system models (care, complaint, regulator).
334,116 (2025) is not for the opening: it counts individuals' marketing-call violations, not operator care. It goes
beside Cabinet 56/2024 wherever the report cites the telemarketing rule, as the scale of that problem, with the scope
stated. Page 35's dispute-service figures join the 2024-04-02 release in the "existing solutions" paragraph.
Why not lead with TDRA: 2023 will be three years old at the Dubai final; e& is 2025 and sits where the AI acts.
Checked later the same day: the Arabic 2024 (Sustainability-report-2024-Arabic-V2-1.ashx) and 2025
(Sustainability-Report-2025-Arabic1.ashx) reports carry the same five-digit figures as the English and no complaint
count; thin text layer (766 and 1,004 words), but every number matches. Bonus from the 2024 English report, page 25,
"Telemarketing and Messaging": "Intrusive SMS Marketing: Total blocked messages: 27,474,205", a candidate beside
Cabinet 56/2024 with the 334,116 figure. Not done: the TDRA open-data transaction files (2020 32,998 matches, 2021
29,300 differs from 29,727; the brief notes it, not needed).
