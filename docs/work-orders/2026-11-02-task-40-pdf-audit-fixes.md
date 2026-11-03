# Work order: Task 40, two fixes from the Fable audit of report.pdf (2026-11-02, hq on Fable)

Model for the build: Opus 5.5. Repo `D:\Projects\engineering\onyx-hackathon-build`, branch `task-36`, on top of
1a588b7. Report wording only; no figure, gap, rule, key, prompt, gate or scenario changes. About 30 minutes.

Fable read all 10 pages of `docs/report.pdf` as text and rendered pages 1, 3, 4 and 8, and checked every count against
the repo: 88 = 50 UAE + 34 foreign + 4 international rows; 83 / 2 / 3 statuses; 109 rules over 13 documents; mandate
document counts 27 / 40 / 18 / 22 / 8; 16 verbs; 13 gate functions; 54 gate tests (pytest collects 54); 156 chunks over
19 documents; 74 with `text_ar`; 23 manifest columns; 60 C3 runs; 2.33 / 2.13; USD 5.3767 / 20 = 0.27; the Annex A
retrieval sentence equals the pooled lines in `eval/results.md` (186, 166, 160, 23, 36); 10 pages, Annex A on page 6;
figures and the Arabic in Annex B render; the title matches the ITU template. Two things did not hold.

## Fix 1: gap 12, "at ITU's request" is not what ITU wrote

Report gap table, row 12, last sentence: "Left open at ITU's request (2026-10-30)." ITU's words (Jiaying, 2026-10-30,
`hq/uni/ai-for-good-hackathon/itu-gap12-reply-2026-10-30.md`): "You can present it as an open gap now." That is
permission, not a request, and the reader of this PDF is the person who wrote it. Change to:
"Left open with ITU's agreement (2026-10-30)." Same change in `docs/report.md` and any site page or README line that
repeats it (`grep -rn "ITU's request"`; show the hits).

## Fix 2: "32 UAE instruments" against 33 UAE ids in the manifest

`kb/manifest.csv` has 50 UAE rows; stripping `-en` / `-ar` gives 33 ids (list: Fable's audit, in
`task-40-pdf-audit-fixes-2026-11-02.md`'s source note below). The report says 32 three times: `docs/report.md` line
22 ("twenty-eight other UAE texts", with the four named = 32), line 131 ("the 32 UAE instruments"), and
`docs/annex.md` line 27 ("32 UAE instruments"). State the counting rule that gives 32 (for example: the TDRA dispute
service page is a web page, not an instrument) and put it where a reader can find it, in one clause in Annex A's
"The documents" paragraph ("32 instruments; one service page"), or change all three to 33 and keep "texts". Either
way the three places agree, and a test pins the number to the manifest with the stated rule, so the next manifest
change moves it. Show the rule and the test.

Source note, the 33 ids: ai-deepfake-guide-2021, cabinet-56-2024, cabinet-57-2024, cabinet-66-2023,
cabinet-agentic-ai-framework-2026-05-18, cabres-106-2026, cabres-200-2025, cabres-28-2023, cabres-52-2024,
child-digital-safety-26-2025, consumer-law-15-2020, csc-ai-security-policy-v1-1, cybercrimes-34-2021, decision-16-2026,
du-code-of-practice, eand-code-of-practice, etransactions-46-2021, executive-order-3-2004,
fed-ai-data-authority-2026-06-14, instructions-1-2014, law-14-2023, licence-2-2026, licence-3-2026,
mocai-ai-ethics-2022, pdpl-45-2021, pdpl-executive-regulations, qos-v3, spam-calls-v4, spam-sms-2022, tdra-cpr-v2,
tdra-dispute-service-page, tdra-registration-policy-2011, telecom-law-3-2003.

## Done means (show each output)

1. `grep -rn "ITU's request" docs/ README.md` prints nothing; the new sentence shown from `docs/report.md`.
2. The 32-or-33 rule, the three lines after the change, and the new test's name and result.
3. `scripts/report_pages.ps1`: `pages: 5`, `annex starts on page: 6`, `total pages: 10`; `report_pdf.ps1` output.
4. `uv run pytest` green; pushed to `task-36`; CI on PR #13 green.
5. hq copy: `D:\Projects\hq\uni\ai-for-good-hackathon\report-draft-2026-10-23.md` equals `docs/report.md`,
   `report-annex-2026-11-02.md` equals `docs/annex.md` (sha256 of each pair).

## Stop and ask when

Either fix adds a page; the gap 12 cell wraps onto page 6; the 32 count has no rule that a test can state.
