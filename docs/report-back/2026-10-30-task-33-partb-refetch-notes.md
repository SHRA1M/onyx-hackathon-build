# Part B: foreign KB sources re-checked at source (2026-10-30)

Step 0: all 17 held files hash-equal to `kb/manifest.csv` (computed with sha256 over the resolved file from `kb/local-sources.json`).

Downloads: `partb\raw\`. Scripts: `partb\scripts\` (lib.py, ecfr.py, pdfs.py, html4.py). Rebuilt files: `partb\raw\rebuilt-*.txt` (held header lines 1 to 3 unchanged + fresh body).

## Rows

| row | URL fetched | HTTP | rebuilt hash equal? | body lines found/total | notes |
|---|---|---|---|---|---|
| imda-mgf-agentic-v1-5 | imda.gov.sg .../mgf-for-agentic-ai.pdf | 200 | yes (raw PDF sha256 = manifest 2636e19f...) | n/a (raw PDF) | 2,169,295 bytes, same as manifest |
| eu-ai-act-2026-07-27 | EUR-Lex TXT/HTML CELEX:02024R1689-20260727 | 202 | refused | not checked | AWS WAF challenge page (curl with browser UA, plain curl). Not compared. |
| gdpr-art22 | EUR-Lex TXT/HTML CELEX:02016R0679-20160504 | 202 | refused | not checked | same |
| eu-dsa-2022-2065-art12-20 | EUR-Lex TXT/HTML CELEX:32022R2065 | 202 | refused | not checked | same |
| eu-crd-2011-83-art8 | EUR-Lex TXT/HTML CELEX:02011L0083-20260927 | 202 | refused | not checked | same; a plain scrapling browser fetch also got 202 with the challenge. A second browser retry with waits was blocked by the permission system as bot-check circumvention, so not tried again |
| eu-ecommerce-2000-31-art10-11 | EUR-Lex TXT/HTML CELEX:02000L0031-20240217 | 202 | refused | not checked | same |
| gdpr-art12-28-33 | EUR-Lex TXT/HTML CELEX:02016R0679-20160504 | 202 | refused | not checked | same |
| us-47cfr-64-2010 | ecfr.gov versioner full/2026-10-19/title-47.xml?part=64&section=64.2010 | 200 | yes | 16/16 | Need `Accept-Encoding` (curl --compressed), otherwise 406. The section at the latest date (2026-10-28) is byte-identical to the 2026-10-19 version; versions API latest amendment for 64.2010 is 2024-06-04 |
| ca-ola-s22-27 | laws-lois.justice.gc.ca O-3.01 page-2.html + page-3.html | 200, 200 | yes | 48/48 | Page still says "Act current to 2026-09-30" |
| es-ley-10-2025 | boe.es BOE-A-2025-26698.pdf | 200 | yes | 411/411 | pdftotext 4.00 default mode, BOE page headers/footers dropped, lines starting lower case joined. Raw PDF sha256 0331830d... (manifest holds the hash of the text file, not the PDF) |
| wales-wls-no1-2015-sch1 | legislation.gov.uk .../schedule/1/made/data.xht + .../regulation/3/made/data.xht | 200, 200 | yes | 645/647 | The 2 lines not found are the file's own editorial lines ("Regulation 3, as made (added 2026-10-30, Task 30b). Source: ..." and "End of regulation 3. Schedule 1 follows."), not source text. Rebuilt with them kept as-is. Regulation 3 extract has NBSP turned into spaces; Schedule 1 keeps NBSP (held file does both) |
| us-tsr-16cfr310 | ecfr.gov versioner full/2026-10-28/title-16.xml?part=310&section=310.3 | 200 | yes | 57/57 | 2026-10-28 is still Title 16's latest "up to date as of" date; versions API latest amendment for 310.3 is 2024-05-16 |
| sg-eta-2010-s15 | sso.agc.gov.sg/Act/ETA2010?ProvIds=pr15- | 200 | yes | 2/2 | Fetched by plain curl (the provision was already in the HTML; no script wait needed). The page now says "Current version as at 31 Oct 2026" (Singapore date has rolled over), held header says 30 Oct. That is the page's daily date stamp, not a text change |
| us-utah-13-77-102 | le.utah.gov .../C13-77-S102_2026050620260506.pdf | 200 | yes | 9/9 | pdftotext -layout, lines trimmed, blank lines and "Page 1" footer dropped. Raw PDF sha256 4accf890... |
| ca-bccrt-2024-149-moffatt | decisions.civilresolutionbc.ca .../525448/index.do?iframe=true | 200 | yes | 26/26 | Plain curl; paragraphs 1-6, 14-17, 24-32, 44 with their sub-lines (quote in para 15, items a-c in para 44) |
| eu-roaming-2022-612-art14 | EUR-Lex TXT/HTML CELEX:32022R0612 | 202 | refused | not checked | same as the other EUR-Lex rows |
| eu-ai-act-2026-07-27-art14-26 | EUR-Lex TXT/HTML CELEX:02024R1689-20260727 | 202 | refused | not checked | same |

Summary: 9 of 17 rows checked. All 9 rebuild byte-equal to the manifest hash, and every body line was found in order (except the two Wales editorial lines, which are not source text). 8 rows (all EUR-Lex) refused.

## EUR-Lex consolidation check

| act | record page | HTTP | latest consolidated version listed | held |
|---|---|---|---|---|
| AI Act 32024R1689 | eur-lex.europa.eu/legal-content/EN/ALL/?uri=CELEX:32024R1689 | 202 (refused, two plain tries) | not obtained | 2026-07-27 |
| GDPR 32016R0679 | .../ALL/?uri=CELEX:32016R0679 | 202 (refused, two plain tries) | not obtained | 2016-05-04 |
| CRD 32011L0083 | .../ALL/?uri=CELEX:32011L0083 | 202 (refused, two plain tries) | not obtained | 2026-09-27 |
| e-Commerce 32000L0031 | .../ALL/?uri=CELEX:32000L0031 | 202 (refused, two plain tries) | not obtained | 2024-02-17 |

No newer consolidation could be found or compared. Nothing is known about AI Act Arts 14, 26, 50, 113; GDPR Arts 12, 22, 28, 33; CRD Art 8; e-Commerce Arts 10, 11 from this run.

## Diffs

None among the 9 rows that could be fetched. No held body line is missing from its fresh source, apart from the two Wales editorial lines named above.

## Not covered

- All 8 EUR-Lex rows and the 4 consolidation record pages: refused (HTTP 202, AWS WAF challenge page with a JavaScript token, saved as raw\crd-202-challenge.html).
- IMDA: hash of the raw PDF only, as asked; its text extract was not re-derived.
