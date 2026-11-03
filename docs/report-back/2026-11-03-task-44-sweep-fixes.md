# Task 44 and addendum done: TRAI 2026, F.AIAP, the Charter, dates, checked lines (2026-11-03, Opus build session)

Order: `D:\Projects\hq\uni\ai-for-good-hackathon\task-44-sweep-fixes-order-2026-11-02.md`, with
`task-44-addendum-2026-11-03.md` and the answers `task-44-stop-1-answers-2026-11-03.md`. Branch `task-36`, PR #13.
Stop file: `docs/report-back/2026-11-03-task-44-stop-1.md` (what was built before stop 1, and the decisions taken).

## What was built after stop 1

- TRAI 2026 (order 1a): row `india-trai-tccrr-4th-amendment-2026`, VERIFIED on the PDF, sha256 be1b743d...cba880
  (the order's value), 46 pages. Iyas eye-checked the five quotes on 2026-11-03 in this session and gave three fixes,
  all applied to the extract's PAGE TRANSCRIPTION section: quote 2 ends "human oversight:" (colon); quote 3 has a
  "[…]" line between "provides options for –" and "(d)"; quote 4 starts "[…] (b)". The bytes are hq's 2026-11-02 copy;
  TRAI refused connections from this machine on 2026-11-03.
- Register: gap 1 gains new 3(9)(d), 3(9)(e) and 3(3) first proviso with the order's `says`; gap 6 gains 3(3) second
  proviso; gap 7 gains 3(3) third proviso and 3(9)(d). Every line's document reads "notified 2026-11-02, not in
  force". Gap 7's May draft now says "Draft, not law, superseded by the notified text of 2026-11-02" (answer 5).
- Annex F: one dated sentence on the Fourth Amendment, "notified 2026-11-02, not in force (ninety days after Gazette
  publication)". Main text: no TRAI sentence (see page measure below).

## Addendum items, one output line each

- A1: `tdra-cpr-v2-en:2.1.16` "Out-of-bundle Period", English p. 7 and Arabic p. 6, searched clause on candidate 4-4.
- A2: outcome (a). Clauses that set a bill's language or form: CPR 3.2.2 (Arabic or English as the consumer prefers)
  and 18.4.2 ("be in writing"), searched 2026-11-03. Candidate line: "the CPR sets the bill's language; no text says
  whether a chat transcript that states a charge is a bill". Still a candidate.
- B1: `tdra-dispute-service-page` VERIFIED (bb3747ab7cde...), `fed-ai-data-authority-2026-06-14` VERIFIED
  (90fece26eafb...), both fetched 2026-11-03; it and the WAM row name each other.
- B2: README "Knowledge base:" line, `docs/annex.md` Annex A, `kb/DATASHEET.md` reworded; README line 169 too
  (answer 4). Report line 25 left as it is: the main text has no room (answer 4's condition). `kb verify`:
  "VERIFIED 98  REFERENCED 4  UNVERIFIED 3  HISTORICAL 0", "every fetched source matches its sha256".
- C1: found. `uae-ai-charter-2024-en`, advisory, VERIFIED: `https://ai.gov.ae/wp-content/uploads/2024/07/UAEAI-Methaq-Jul-EN.pdf`,
  HTTP 200, 10,523,602 bytes, "%PDF-1.6", 6 pages, sha256 77a3c549...fa17. Downloaded with Iyas's yes, through his
  Chrome (the viewer's download button; a scripted save was blocked). English only (hq: Arabic name 403). The PDF has
  no text layer, so principles 5 (Transparency) and 6 (Human Oversight), page 4, were transcribed and eye-checked by
  Iyas. Gap 6 searched: principle 5; gap 7 searched: principle 6; both "Searched, non-binding". No report change.
- C2: datasheet line "GCC: Qatar, Kuwait and Saudi Arabia searched; Oman and Bahrain not searched."
- D1: the u.ae data-protection page says nothing on the Executive Regulations (English and Arabic). No change.
- D2: "unreachable" line, dates 2026-11-02 and 2026-11-03 only (answer 3; the 11-04 sweep adds 11-04 if it retries).
- E1: neither README nor annex said what "unseen" means. The sentence went to README (under the scenario table) and
  Annex C (Design): written before the first scored run, bytes fixed by commit 93a7d40 (2026-10-21) and unchanged
  since, never sent to a model. Checked: `git log -- onyx/data/scenarios/unseen/` shows only 93a7d40; it is an ancestor
  of d85871d, the first commit holding runs; no file in `runs/` names a U scenario. Not in the main text: one added
  line there moved the annex to page 7 (measured, then reverted).
- F1 to F4: as in the stop file (F4: "Exposed by: S2-3 (the complaint hand-over, CPR 26.7.2)").
- G: csc row note "Unreachable again 2026-11-03 (Chrome)"; Gazette as D2.

## Done checks (order), each run

1. `pytest`: 713 passed.
2. `python -m onyx gaps`: 15 gaps, 2 candidates (ids unchanged).
3. `eval` live: 60 runs read; `eval/`, `runs/` and `onyx/data/keys/` byte-identical (`git status` empty for them);
   "All hash chains verify: yes. Every run_start carries the current key hashes: yes." (live and scripted).
   `selftest`: "figures match a fresh eval of runs/".
4. Word (`scripts/report_pages.ps1`): pages 5, words 2373, annex starts on page 6, total pages 12, total words 6839.
   `scripts/report_pdf.ps1`: word pages 12, pdf pages 12, finds "Annex A", "Limits and next steps", "Annex F": True.
   Same page counts as Task 43.
5. `git grep -n "as amended 2013"` over the order's live paths: no hit.
6. Every gaps.json line with "in force" and TRAI (lines 53, 54, 55, 238, 277, 284, 285) carries "notified 2026-11-02"
   and "not in force" or "ninety days after Gazette publication".
7. `check_kb_counts`: report [] and annex []. Report: holds 105 documents, **SRC-2** 105, 98 are verified,
   thirty-eight foreign texts, thirty other UAE texts, the 34 UAE instruments. Annex A: 105 documents, 34 UAE
   instruments, 38 foreign texts, 98 VERIFIED, 4 REFERENCED, 3 UNVERIFIED. README: 105 rows; 98 / 4 / 3.
8. CI on PR #13: `reproduce` pass on `48e0ae1` (runs 41721369344 and 41721378385).

## Differs from the order

- The UAE instruments count is 34, not hq's expected 33: the Charter (a policy row) counts as an instrument.
- Annex A's description now names three web pages, two announcements and a news report as not instruments, "6 ITU
  texts (one a work-programme page)", and the DHA policy, the enforcement decision and the Charter among instruments.
- Fix outside the order: `docs/build_report.py` `_number("thirty")` returned nothing, so "thirty other UAE texts"
  failed the count check whatever the manifest said. It now reads a round tens word. Test first (red, then green).
- Gap 7's TRAI 2026 lines are appended last (after DIFC), as every task's entries are, not next to the 2012 rows.
- hq copies: `report-draft-2026-10-23.md` and `report-annex-2026-11-02.md` replaced, `.bak-2026-11-03-task-44`
  backups beside them (the replaced copies equalled the last commit). sha256: report 0fbb3e0f...b636, annex
  ef4f98c9...961d (both copies each).

## Open

- Nothing from the build. The 11-04 Gazette retry is hq's.
