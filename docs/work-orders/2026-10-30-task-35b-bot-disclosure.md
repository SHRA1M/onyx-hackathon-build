# Work order: Task 35, two Gulf telecom regulations into the KB and register (2026-10-30, hq on Fable)

Model: Opus 5.5. Repo: `D:\Projects\engineering\onyx-hackathon-build`. Branch `task-35` from `main` after Task 34
merges. Decided by hq; read file `ai-for-good-hackathon/perplexity-2026-10-30/gulf-examples-read-2026-10-30-fable.md`.
Build this order; do not re-decide it. About 2 hours. Before 2026-11-06.

## Task

1. **Three KB rows**, VERIFIED, jurisdiction `foreign`, binding (they bind licensees in their own state; never a
   gate basis), from the files in `D:\Projects\hq\uni\ai-for-good-hackathon\standards-text\gulf-2026-10-30\`:
   - `qatar-cra-ccpr-2024.pdf` (69 pp, EN and AR in one file): Qatar CRA, Communications Consumer Protection
     Regulation, CRA President's Decision 39/2024, CRACA/2024/10/02, October 2024. URL:
     `https://www.cra.gov.qa/-/media/System/C/3/F/C/C3FC33E54B585B91A7134F7C9786FD17/COMMUNICATIONS-CONSUMER-PROTECTION-REGULATION-FINAL.ashx?download=1`.
     Notes: in-force date not read (the issuing decision is image-only); "which language prevails" not stated in
     the pages read.
   - `kuwait-citra-res-69-2022-en.pdf` (2 pp): Kuwait CITRA Resolution 69/2022, issuing decision, English. URL
     `https://www.citra.gov.kw/sites/en/LegalReferences/Resolution-No-69(2022)-The-Regulation-of-Protecting-Communications-and-Information-Technology-Services-Users-Rights.pdf`.
     Art 1 applies the regulation to licensees; Art 4 in force on Gazette publication (date not found).
   - `kuwait-citra-users-rights-ar.pdf` (18 pp, Arabic, "نسخة رقم 1.3", undated version): the regulation itself.
     URL `https://www.citra.gov.kw/sites/ar/LegalReferences/protection.pdf`. Note the version caveat: the file is
     the current text; whether every clause stood on 2022-04-21 is not known.
   Re-fetch each from its URL, hash, compare with the stored copy; a mismatch is a stop. Chunk nothing.

2. **Register (`onyx/data/gaps.json`, then `docs/gaps.md` and the site render):**
   - gap-3: add a global example "Qatar CCPR 2024 §1.2 (Customer Consent)" with the quote of routes (b), (c) and (d)
     in English as printed, and `says`: named verification routes for a remote consent, no assurance level.
     eIDAS stays lead.
   - gap-1: `searched` entry for Kuwait regulation §9 items 2.9, 4.9, 5.9 (quote 5.9 in Arabic as printed, label
     AR) with `says`: a 3-minute average wait on the complaints line and a dedicated department; no bot-to-human
     hand-over rule.
   - gap-2: `searched` entries for Qatar §1.2 (consent routes name no AI channel) and Kuwait §3-1 (quote the
     Arabic sentence allowing written, oral or electronic consent; label AR): spoken consent allowed, AI channel
     unnamed.
   - One sentence in the register's preamble (and the README's gap paragraph if it has one): the two GCC telecom
     consumer regulations read (Qatar 2024, Kuwait 2022) name no AI channel, hand-over, disclosure or Arabic
     quality measure either.

3. **Report:** unchanged, unless gap 3's cell "eIDAS Art 8(1), 8(3)(c)" can become "eIDAS Art 8(1), 8(3)(c); Qatar
   CCPR 2024 §1.2" and Word still says 5 pages. If it goes to 6, leave the cell.

4. Counts, datasheet, count check, tests (KB rows and counts; the three new rows; the gap-3 example and the three
   searched entries), CHANGELOG, PR (no merge or tag until Iyas says so), hq copy of the report only if it
   changed, report-back `docs/report-back/2026-10-30-task-35-gulf-rows.md`.

## Done means (show each output)

- `python -m onyx kb verify`: counts up by 3 VERIFIED, foreign up by 3; the three hashes match a fresh fetch.
- The gap-3 example and three `searched` entries render on `docs/gaps.md` and the site, Arabic quotes RTL.
- Count check passes on every number the report states; 5-page check passes.
- Full suite passes; CI green.

## Limits

No chunks, no runs, no gate, rule, mandate, prompt, eval, model or agent file; no other wording. Seven layers:
unchanged from Task 34; nothing shipped or deferred. Sources rule: only the three URLs above; nothing else fetched.

## Stop and ask when

A fresh fetch hashes differently from the stored copy; the report goes to 6 pages with the cell swap (then leave
the cell and continue); any test outside the ones named fails.

---

# Addendum A (2026-10-30 night, hq on Fable): Saudi CST 552/1445 and Qatar 16/2010

Read files: `perplexity-2026-10-30/saudi-cst-552-read-2026-10-30-fable.md` (findings table a to g, verdict) and
`standards-text/gulf-2026-10-30/qatar-decree-law-16-2010-ar-extract.md`. Same branch, same PR, same 2-hour budget
plus about 1 hour. Gap ids below are the register's (`onyx/data/gaps.json`); the Saudi read file's "gap 5" means
register gap-11.

## A1. Three more KB rows, VERIFIED, `foreign`, binding in their state, never a gate basis

- `standards-text/saudi-cst-user-protection-552-1445-en.pdf` (34 pp, text layer): CST, Regulations of User Rights
  Protection Rules, RC05, second version, February 2024. URL `https://www.cst.gov.sa/-/media/D372076E57474D16915514D5C2B32C84.pdf`.
- `standards-text/saudi-cst-user-protection-552-1445-ar.pdf` (32 pp, image-only text layer): same, Arabic. URL
  `https://www.cst.gov.sa/-/media/44F95AD6EA7D4781A57976B9DCAA5B91.pdf`. Row note: "text layer unreadable; quotes
  transcribed from page images, two independent readings agree; not eye-checked by a person".
- Both rows: issuing decision 552/1445 of 08/02/2024, replaces 423/1441; in force 90 days after approval (CST
  decision page `https://www.cst.gov.sa/regulations-and-licenses/decisions/Regulation-1499`, read 2026-10-30; the
  PDFs print no decision number). Note the date as "2024-05-08 (computed from the 90 days; not printed)".
- `standards-text/gulf-2026-10-30/qatar-decree-law-16-2010-ar-extract.md`: Qatar Decree-Law 16/2010, Electronic
  Transactions and Commerce Law, Arabic, articles 1 (one definition), 2, 19, 27, 53 to 57 only, copied from
  `https://almeezan.qa/legislations/decree-law/2010/16/general` (Official Gazette 9, 2010-09-28; Art 3 amended
  2019). Row kind: extract (the portal is a JS app; curl gets a shell). Hash the extract file, not the URL: the
  fetch check is "URL returns 200" only. REFERENCED if the schema has no extract kind; say which in the report-back.

## A2. Register

- **gap-1**, global example "Saudi CST 552/1445 §13.1.1, 13.1.2, 26.5.2": English quotes as printed (p. 14, 29),
  Arabic beside them (AR label) from the read file; `says`: a voice route and an electronic route to an employee,
  and a qualified employee handles the complaint; no clock on the hand-over, no bot named. `searched` line for 26.4
  (five days to resolve) and 13.1.3 (KPIs, no minute figure). Spain Ley 10/2025 stays lead.
- **gap-2**, global example "Saudi CST 552/1445 §5.1.2, 5.1.3": call recorded, recipient's identity checked on a
  sales call; `says`: recording and identity check, the sale documented "according to what CST issues" (10.3), no
  AI channel named. `searched`: 9.5 (burden of proving consent on the provider).
- **gap-3**, global example "Saudi CST 552/1445 §10.7": OTP to the primary SIM before a secondary becomes primary;
  `says`: one named method for one named change, no general assurance level. `searched`: 9.6, 23.1.
- **gap-6**, `searched`: 5.1.4 (a representative gives name, employer, reason at the start of a telemarketing call;
  a human caller's duty, none for an automated one); Qatar 16/2010 Art 53(2) (a commercial electronic
  communication identifies the person on whose behalf it is sent; not that a machine sends it), Art 27 (a contract
  formed with an automated message system is valid without a natural person's review; nothing on telling the
  consumer). Arabic quotes, AR label.
- **gap-10**, `searched`: 552/1445 §9.2.2, 16.4, 26.6 (Arabic and English offered; no per-language quality measure;
  13.1.3 KPIs not split by language).
- **gap-11**, global example "Qatar 16/2010 Art 56(1)" (means to identify and correct an input error before the
  order is placed; a GCC mirror of e-Commerce Directive Art 11(2)) and Art 19 (the natural person may withdraw the
  wrongly entered part when the automated system gave no chance to correct it, if reported at once and nothing was
  used). `searched`: 552/1445 §10.3, 10.4, 23.6 (consent before, a document after; no read-back).
- **gap-12**, `searched`: 552/1445 §30.2 (written steps may be executed by automated systems, conditions deferred to
  CST); Qatar 16/2010 Art 1 "نظام الرسائل الآلي" and Art 27 (the law recognises the automated system acting without
  review; it never asks when it must stop).
- Preamble sentence from the base order becomes: the three GCC telecom consumer regulations read (Saudi 2024, Qatar
  2024, Kuwait 2022) name no AI channel, hand-over clock, machine disclosure or Arabic quality measure either; Saudi
  552/1445 comes nearest, requiring a route to an employee and a qualified employee on every complaint.

## A3. Report

Unchanged unless gap 1's cell can take "; Saudi CST 552/1445 §13.1, 26.5.2" and Word still says 5 pages. Try gap 1
before gap 3; if only one fits, gap 1 wins (it is the headline gap). If neither fits, leave both.

## A4. Done means, added

- `kb verify`: counts up by 6 VERIFIED (or 5 plus 1 REFERENCED), foreign up by 6; fresh fetch of the two CST PDFs
  hashes equal; Qatar extract hash equal to the filed file.
- Every new example and `searched` entry renders on `docs/gaps.md` and the site, Arabic RTL.
- Tests: the six rows and counts; gap-1, gap-2, gap-3, gap-11 examples; one `searched` entry per touched gap.
- Count check on every number the report states (the report's "foreign" count line, if any, moves by 6).

## Limits, added

No chunks for the new rows. No Saudi Arabic quote enters the register unless it is in the read file's table or the
transcription file; nothing transcribed fresh by the build. Nothing fetched beyond the three CST URLs and the Al Meezan
URL. Seven layers unchanged.

## Stop and ask, added

The CST PDFs hash differently from the filed copies; the KB schema has no place for an extract-only source; the
report moves to 6 pages with either cell (leave the cell, continue).

---

# Addendum B (2026-10-30 night, hq on Fable): bot-disclosure statutes, four rows, gaps 1, 6, 7

Read file: `perplexity-2026-10-30/bot-disclosure-statutes-read-2026-10-30-fable.md` (its Verdict section is the
spec; quotes come from its table, nothing retyped). Files in `standards-text/bot-disclosure-2026-10-30/`. Own
branch `task-35b` from `main` after PR #11 merges, own PR, own report-back
`docs/report-back/2026-10-30-task-35b-bot-disclosure.md` (changed 2026-10-30: the first build did base plus A only).
About 2 hours.

1. **Rows, VERIFIED, `foreign`, binding in their state, never a gate basis:** Maine 10 M.R.S. §1500-DD
   (`maine-1500-DD.html`, URL `https://legislature.maine.gov/statutes/10/title10sec1500-DD-1.html`; the "-1" is
   right: hq fetched it 2026-10-30, 200, sha256 equal to the stored file; without "-1" is 404); India TRAI TCCRR 2012 (`india-trai-tccrr-2012.pdf`, URL
   `https://trai.gov.in/sites/default/files/2024-09/CA_05012012.pdf`); Texas Bus. & Com. Code ch. 552
   (`texas-bcc-552.html`, URL `https://statutes.capitol.texas.gov/GetStatute.aspx?Code=BC&Value=552`). California
   BPC §17940-17943 and HSC §1339.75: leginfo refuses curl, so file each as an extract `.txt` carrying exactly the
   quoted text in the read file's table, with the leginfo URL, kind extract (or REFERENCED if the schema has no
   extract kind; same choice as Addendum A's Qatar row). URLs (hq loaded both in a browser 2026-10-30, 200, text
   shown): BPC `https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=BPC&sectionNum=17941`;
   HSC `https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=HSC&sectionNum=1339.75`.
   Dates: print only what the page prints (BPC "Effective January 1, 2019. Operative July 1, 2019"; HSC "Effective
   January 1, 2025" (AB 3030, Stats. 2024, Ch. 848); Texas "eff. January 1, 2026"); Maine in-force date "not on the
   statute page".
2. **Register:** gap-6 examples: Maine §1500-DD(2) lead, California §17941(a), (b) second (`says` carries the intent
   caveat), AI Act Art 50 third; `searched`: Texas §552.051(b), (c); Korea Art 31(1) (KLRI URL
   `https://elaw.klri.re.kr/eng_service/lawView.do?hseq=73499&lang=ENG`: hq fetched it 2026-10-30, 200, title
   "FRAMEWORK ACT ON THE DEVELOPMENT OF ARTIFICIAL INTELLIGENCE AND THE CREATION OF A FOUNDATION FOR TRUST"; the
   article text loads by script, so check the quote against the stored `korea-ai-basic-act-klri-en.html`, not the
   URL bytes; "English is a reference translation; in-force date unverified"). gap-7 examples: India reg 3(9); California HSC §1339.75(a)(1)(C)
   and (a)(2). gap-1 example: India reg 3(9) (`says`: a regulator orders the automated channel to offer a person;
   no clock); `searched`: HSC §1339.75(a)(2). Preamble: one sentence from the read file's item 5: companion laws
   carve out customer service. Nothing on Brazil (dropped by Iyas 2026-10-30). One `searched` line on gap-7 for the TRAI
   2026 draft Fourth Amendment, labelled draft, URL `https://trai.gov.in/sites/default/files/2026-05/Regulation_07052026.pdf`.
3. **Report:** gap 6 cell may become "Maine §1500-DD; EU AI Act Art 50(1)"; gap 7 may gain a table row. Order of
   tries if pages are tight: gap 1 (Addendum A), gap 6, gap 7, gap 3. Each only while Word says 5 pages.
4. Done means: `kb verify` counts up by 5 (or 3 VERIFIED plus 2 extract/REFERENCED), foreign up by 5; the examples
   and `searched` lines render, site too; tests for the five rows, the gap-6 order, gap-7 and gap-1 examples; count
   check; full suite; CI green. Limits and stop rules as Addendum A.
