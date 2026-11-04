# Task 45: 11-04 sweep fixes (text and three knowledge-base rows)

Written on Fable, 2026-11-04, from `D:\Projects\hq\uni\ai-for-good-hackathon\sweep-2026-11-04-fable.md` (sections 5,
7 to 14). Build on Opus. Start: `git pull` on main (61e26e4 or later), branch `task-45`. Text changes and three
manifest rows; no figure, no run, no prompt, no gate, no key, no frozen file. About 2 hours.

Before any edit, list every number the report, annex, README, datasheet and site state about the knowledge base (rows,
VERIFIED, REFERENCED, UNVERIFIED, UAE instruments, announcements, foreign texts, "84 instruments") with file and line,
in the report-back. The count check at the end covers that list, not only the lines this task touches.

## Task

1. **Gazette line, dated.** The sentence "The federal Official Gazette (Ministry of Justice, elaws.moj.gov.ae) was
   unreachable on 2026-11-02 and 2026-11-03 (curl, and Chrome from hq); ..." becomes:
   "The federal Official Gazette (Ministry of Justice, elaws.moj.gov.ae) was unreachable on 2026-11-02, 2026-11-03 and
   2026-11-04 (curl and Chrome from hq, GitHub answering as the control), so its issues were not swept; the legislation
   portal, which lists each law's Gazette number and its regulations, is the official check, and it publishes no issue
   archive; the newest issue the portal names is No. 833 of 14 October 2026 (entry 4660, read 2026-11-04)." Two
   hand-written sources: `onyx/gaps.py` (line 70 to 72 area; `docs/gaps.md` and `docs/site/gaps.html` are generated)
   and `README.md` line 65. Change both, regenerate.
2. **csc row note.** In `kb/manifest.csv` row `csc-ai-security-policy-v1-1`, "Host unreachable from Amman 2026-10-17
   and 2026-10-30" becomes "Host unreachable from Amman 2026-10-17, 2026-10-30 and 2026-11-04 (TLS handshake failed,
   GitHub as control); described at u.ae, page updated 2026-07-02". Same string in `kb/DATASHEET.md` line 119,
   `docs/site/kb.html` and `tests/test_kb.py` if it asserts it. Do not run `kb fetch` over the whole kb; a manifest
   changed only by a fetch is never committed.
3. **Five criteria on the README's first screen.** The event page lists five evaluation criteria (knowledge base
   quality; agent capability; policy, strategy, standards gap identification; auditability; alignment with ITU
   standards; read 2026-11-04). `README.md` line 9 "The four published criteria" becomes "The five published
   criteria", and the table's second row splits in two: "Agent capability in error scenarios" (evidence:
   `docs/replay/index.html`; check: the `why` command) and "Policy, strategy and standards gaps" (evidence: the gap
   register below and `docs/gaps.md`, `docs/replay/whatif-S2-gap-1.md`; check: the command that verifies the register,
   else "open `docs/gaps.md`"). Update `tests/test_report.py` line 275 and any README layout test. The report's text
   is not touched.
4. **PDPL regulations tab, re-checked.** Every "checked 2026-11-02" that refers to the portal's Regulation Table of
   Decree-Law 45/2021 (gaps 5, 13 and 14 in `onyx/data/gaps.json`; `kb/DATASHEET.md` line 118 on
   `pdpl-executive-regulations`) gains "and 2026-11-04 (Arabic regulations tab, Chrome from hq: «لم يتم العثور على
   أية بيانات»)". The README and register gap-3 row "portal and TDRA site checked 2026-11-02" becomes "checked
   2026-11-02 and 2026-11-04". Regenerate.
5. **Row: WAM article of 2026-08-21, VERIFIED.** Id `wam-2026-08-21-agentic-ai-guide`, in the shape of
   `wam-2026-06-14-ai-data-authority` (announcement, advisory, UAE, SRC): title "National Committee for Agentic AI
   launches a unified guide for designing government services with agentic AI (WAM, 21 August 2026)", title_ar
   «اللجنة الوطنية للذكاء الاصطناعي المساعد تطلق دليلاً موحداً لتصميم خدمات حكومية مدعومة بالذكاء الاصطناعي المساعد»,
   issuer "WAM (Emirates News Agency)", language ar, URL `https://www.wam.ae/ar/article/c1uggxh`. Fetch that one
   document only (`kb fetch wam-2026-08-21-agentic-ai-guide` or the single-document form the CLI has), record
   sha256, bytes, dates. Chunk it as one document; diff `kb/chunks/` before committing (trap: a whole-kb chunk rewrites
   hand-fixed files). Three chunks, the sentences below, ids `consent`, `handover`, `objection`.
6. **Row: the guide itself, REFERENCED.** Id `agentic-ai-gov-guide-2026-08-21`, in the shape of
   `itu-t-f-aiap-work-item` (REFERENCED): title "Practical Guide for Government Entities on Designing Government
   Services with Agentic AI (National Committee for Agentic AI, launched 21 August 2026)", title_ar «دليل تصميم
   التجارب الحكومية بالذكاء الاصطناعي المساعد», issuer "National Committee for Agentic AI", advisory, UAE, ar, source_type
   guidance, URL `https://uaemodel.egsep.ae/agentic_ai_guide_website.html`. Note: "Linked from u.ae 'Agentic AI for
   Government Services' (updated 2026-09-30), 'available in Arabic only'; the site served its table of contents once on
   2026-11-04 then answered 403 (Cloudflare) to every fetch from Amman; text not held; quoted only through the WAM
   announcement row. Guidance for federal government entities; binds no licensee." No chunks.
7. **Row: DoH Responsible AI Standard, VERIFIED.** Id `doh-responsible-ai-standard-v1-2025`, in the shape of
   `dha-ai-policy-2021` (policy, binding, UAE, en, SRC): title "Responsible AI Standard, DoH/ST/DDGO/RAI/V1/2025,
   version V1 (Department of Health, Abu Dhabi; published and effective October 2025)", issuer "Department of Health,
   Abu Dhabi", URL
   `https://www.doh.gov.ae/-/media/Feature/Resources/Standards/2025/Responsible-AI-Standard-V1.ashx` (hq fetched it
   2026-11-04: HTTP 200, 490,537 bytes, 15 pages). Fetch that one document, chunk it as one document, two chunks:
   `3.1.1.2.2` (p. 5) and `3.1.6.1.1` (p. 8; confirm pages from the file). Note: "One emirate, one sector: binds the
   DoH and licensed healthcare entities in Abu Dhabi (its 1.2); names 'agents' in scope; never a rule for a telecom
   licensee."
8. **Searched lines in `onyx/data/gaps.json`**, each in the shape of the `uae-ai-charter-2024-en:6` line (clause, file,
   page, says, quote), Arabic quotes word for word from the fetched page:
   - gap-1, `wam-2026-08-21-agentic-ai-guide:handover`: says "Searched, non-binding, government services only: the
     National Committee for Agentic AI's guide (WAM, 21 Aug 2026) wants a smooth transfer to a competent employee with
     the full request and the steps done; guidance for federal entities, no TDRA counterpart for a licensee's agent."
     quote «ضمان الانتقال السلس إلى موظف مختص عند الحاجة، مع نقل كامل تفاصيل الطلب والخطوات المنجزة، حتى لا يضطر
     المتعامل لإعادة شرح طلبه من جديد».
   - gap-2, `:consent`: says "Searched, non-binding, government services only: the guide wants the customer's
     approval before any action; nothing on which sales medium an AI channel is." quote «والحصول على موافقته قبل اتخاذ
     أي إجراء».
   - gap-7, `:handover`: says "Searched, non-binding, government services only: the only UAE text setting conduct
     standards for an agentic AI dealing with the public (approval before any action, hand-over with the full request,
     a route to ask, correct or object) is guidance for federal government services; none binds a licensee." Same quote
     as gap-1.
   - gap-11, `:objection`: says "Searched, non-binding, government services only: the guide gives the customer a route
     to ask, correct or object after the result; no read-back rule for a licensee's agent." quote «وتمكينه من السؤال أو
     التصحيح أو الاعتراض».
   - gap-6, `doh-responsible-ai-standard-v1-2025:3.1.6.1.1`: says "Sector line, with the DHA row: the Abu Dhabi
     Department of Health binds its licensed entities to tell patients when AI contributes to a decision (Oct 2025);
     one emirate, health sector; no TDRA text does the same for a licensee." quote "All healthcare AI systems must
     include mechanisms to inform patients, clinicians, and relevant stakeholders when AI contributes to clinical or
     operational decisions, specifying its function, limitations, and intended outcomes."
   - gap-7, `doh-responsible-ai-standard-v1-2025:3.1.1.2.2`: says "Sector line, with the DHA row: two emirate health
     regulators bind their licensees to human oversight and escalation for AI systems, 'agents' named in scope (DoH
     1.2); TDRA binds its licensees to neither." quote "AI systems must always function under human oversight. Clear
     escalation protocols shall be established within AI systems, outlining specific actions and decision points based
     on varying risk levels to involve human oversight effectively."
   The gap-6 and gap-7 UAE-position sentences that name the DHA policy as the sector line now name both ("the DHA
   policy (Dubai, 2021) and the DoH standard (Abu Dhabi, 2025)"). Nothing else in the positions changes.
9. **TRAI row note.** `india-trai-tccrr-4th-amendment-2026` note gains: "Mirror while trai.gov.in is unreachable from
   Amman (2026-11-02 to 11-04): Press Information Bureau, Government of India, Release ID 2331704, posted 02 Nov 2026,
   `https://www.pib.gov.in/PressReleasePage.aspx?PRID=2331704`: 'Human assistance shall be available for at least
   sixteen hours daily. Technology-based solutions shall function with appropriate human oversight.' Gazette date
   still not found; notified, not in force."
10. **Every count.** From the list made before the edits: rows 105 to 108; VERIFIED 98 to 100; REFERENCED 4 to 5;
    UNVERIFIED 3; UAE instruments 34 to 36 (the guide and the DoH standard; the WAM article is a third announcement:
    Annex A "two announcements" becomes "three announcements", and its parenthesis names "the DHA AI policy, the DoH
    standard and the UAE AI Charter"); datasheet "84 instruments" to 86; foreign texts 38 unchanged; chunk and
    document counts in Annex A ("156 committed chunks across 19 documents") move by what `kb chunk` reports. `python -m
    onyx kb verify` decides the status counts; the report-back shows its output beside every changed line. Report,
    annex, README, datasheet, site, tests.

## Done means

- `grep -rn "four published" README.md docs/ tests/` prints nothing; `grep -rn "2026-11-04" README.md docs/gaps.md
  kb/manifest.csv kb/DATASHEET.md` prints the new lines (Gazette, csc, PDPL tab, the three rows).
- `uv run python -m onyx kb verify` prints 100 / 5 / 3; the chunk check passes on the five new chunks (quote found word
  for word); `python -m onyx gaps` leaves `docs/gaps.md` unchanged on a second run.
- `uv run pytest -q` passes; the test count is in the report-back.
- Word page check (`scripts/report_pages.ps1`): the report still 5 pages, the PDF rebuilt and its page count stated.
- `git diff --stat kb/chunks/` shows only the two new chunk files.
- PR to main, CI "reproduce" green, report-back `docs/report-back/2026-11-04-task-45-sweep-fixes.md` with: the
  number list, the grep outputs, the verify output, the test count, the page count.
- Before the PR is marked ready: Iyas eye-checks the three Arabic quotes of item 8 against
  `https://www.wam.ae/ar/article/c1uggxh` in Chrome (the report-back says "eye-checked by Iyas 2026-11-0x" or "not
  yet"; the PR waits on it).

## Limits

Text and three rows. No scored figure, prompt, gate, key, run or frozen file changes. No whole-kb `kb fetch` or `kb
chunk`. Not taken, by hq ruling (sweep file section 10): Brazil Decreto 13.135/2026 (unreachable from Amman),
California AB 1609 (exempts regulated telecom), UK DUAA 2025 s. 80, TRAI's draft AI guidelines, Cabinet 55/2026 and
173/2026, the Québec charter, the ITU SG20 work items, the TDRA consumer guide. Seven layers (versioned prompt,
grounding, gated tools, identity, injection defence and masking, cost cap and router, trace and evals): unchanged by
this task; the 10-29 and 10-30 rulings stand (masking, cache/router, identity deferred; nothing due before 11-09).

## Stop and ask when

A README layout test needs more than the row split; any test outside `test_report.py`, `test_kb.py` and the register
tests fails; `kb fetch` of the DoH file returns a different sha256 on two runs (a dynamic URL); the WAM page's text
layer lacks one of the three sentences word for word (then quote only the ones found and say which is missing); the
report grows past 5 pages; a count the list did not foresee changes.
