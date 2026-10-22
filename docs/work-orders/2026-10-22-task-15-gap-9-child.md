# Order: Task 15, gap-9 (a child on the line) and one candidate row (hq, Fable, 2026-10-22)

Build model: Opus 5.5. No model calls; USD 0. Starts after Task 14 is pushed. Copy this file into
`docs/work-orders/` first. **Final (hq, Fable, 2026-10-22):** both searches are in and the primaries are opened
(section "Second search and primaries" below). No instrument under Child Digital Safety Arts 6, 11 or 16 exists.
The order runs as written here; item 2 was amended on 2026-10-22 and this file is the current text.

Decision (hq, Fable, 2026-10-22, from the 2026-10-17 law file section 6 item 9 and section 8): the candidate "a
child on the line" becomes gap-9. The law is binding and in force (26/2025, Art 20); it puts the duty on the
operator (11(1)(b): the caregiver signs the service terms where the beneficiary is a child; 7(1): verified caregiver
consent for under-13 data); the instruments that would let an agent apply it are unpublished. Exposed by the mapping
(SRC and P nodes: no age signal reaches the gate) and by drill U2 of the unseen bank, which has not been run; the row
says both.

## Sources allowed, and nothing else

`kb/chunks-full/child-digital-safety-26-2025-en.jsonl` (7(1), 9(2), 10(1)(g), 11(1), 11(2)); the Arabic text of
Article 11 in `standards-text/child-digital-safety-law-26-2025-ar.txt` (hq copies it to `docs/sources/`); the
2026-10-17 law file already in `docs/sources/`; two texts hq opened on 2026-10-22 and copies to `docs/sources/`:
`standards-text/cabinet-resolution-106-2026-children-social-media-en.txt` (Arts 1, 2, 3(4)(c), 4(2), 4(3), 7(1),
7(2), 7(5)) and `standards-text/tdra-telecom-for-minors-page-2026-10-22-en.txt`; one fetch, below. Nothing else is
fetched. The quotes in item 2 are verified verbatim against those two files, as Task 9 did.

## Items

1. **One fetch, global example**: 16 CFR 312.5 (COPPA Rule, "Parental consent"), from ecfr.gov only, saved as
   `kb/sources/global/coppa-16cfr312-5.txt` with the source URL, fetch date and the section text only, the same shape
   as the eur-lex files. Quote 312.5(a)(1) ("obtain verifiable parental consent before any collection, use, or
   disclosure of personal information from children") and 312.5(b)(1) (a method "reasonably calculated, in light of
   available technology, to ensure that the person providing consent is the child's parent"). Verify the quotes
   verbatim against the fetched text as Task 9 did. If the fetch fails, stop and ask; do not substitute another text.
2. **Row gap-9** in `onyx/data/gaps.json`, generated into `docs/gaps.md` and the README register:
   - `gap`: "A child on the line: the Child Digital Safety Law 26/2025 makes the caregiver sign the service terms
     where the beneficiary is a child (11(1)(b)) and requires verified caregiver consent for under-13 data (7(1)),
     but the Cabinet classification (Art 6), the TDRA instructions to providers (Art 11) and the penalties (Art 16)
     are unpublished, and no text addressed to a telecom provider says how an automated channel learns that the
     person is a child."
   - `kind` method; `category` legislative gap; `addressee` TDRA, Cabinet; `global example` 16 CFR 312.5(a)(1),
     312.5(b)(1); `exposed by` "mapping (SRC, P); U2 (drill bank, not run)".
   - Searched rows: 7(1), 9(2), 10(1)(g), 11(1), 11(2), each with one line of what it says from the chunk text, Arabic
     for 11(1) from the source file. Add a searched row for CPR 4.3 and 4.7 (no age condition on a sale) from the KB.
   - UAE position (amended 2026-10-22; the two quoted documents are the nearest published texts and neither closes
     the gap): "The duty is the law's own words; the operator's licence 3.2 makes it a licence condition; the
     instruments that would set the age signal, the caregiver check and the penalties do not exist yet (searched
     2026-10-16 and 2026-10-22, both languages). Two published texts come near and neither reaches a telecom
     channel. Cabinet Resolution 106/2026 (issued 2026-06-17, in force 2026-06-30) 'shall apply to all Social Media
     Platforms whose services are made available within the State or directed at users therein' (Art 2); it lists
     age-verification mechanisms for those platforms (Art 4(2)) and says 'Self-declaration of age ... shall not be
     recognized' (Art 4(3)), but its standards are still to be 'approved by the Child Digital Safety Council upon the
     proposal of the Telecommunications and Digital Government Regulatory Authority' (Arts 3(4)(c), 4(1)(h), 4(2)(d))
     and its penalties are those 'prescribed under the list of administrative penalties issued pursuant to the
     provisions of the Decree by Law' (Art 7(1), 7(2)), the Art 16 list that is not published. TDRA's 'Telecom for
     Minors' page (consumer hub, updated 2026-10-01) describes an initiative launched 'in collaboration with licensed
     telecommunications service providers' that 'Supports the goals of the UAE child digital safety law'; its terms
     'are determined by each service provider', the links 'are provided for consumer information only', and it is
     not on the TDRA Regulations and Ruling register."
   - Recommendation (amended 2026-10-22): "TDRA to issue the Art 11 instructions with the caregiver check an
     automated channel must run before activating or changing a service, and the consent method for under-13 data.
     Resolution 106 Art 4(2) already lists acceptable age-verification mechanisms for social media platforms, and
     16 CFR 312.5(b) lists acceptable consent methods; the Art 11 instructions can name a list of the same shape for
     telecom channels."
   The "A child on the line" entry leaves the Candidates section.
3. **Candidate row** `candidate-79bis-2-fine-schedule`: "The Cabinet schedule of licensee violations and fines
   promised by Telecom Law 79 bis (2) is not published; a CPR breach by an automated channel falls under 79 bis (1)
   and licence 16.3.2 (AED 50,000 to 200,000) with no schedule above it." Kind absence, addressee Cabinet, no global
   example, exposed by "mapping (P)". Searched rows: `telecom-law-3-2003-en` 79 bis (1) and (2), `licence-2-2026`
   16.3.2, from the KB chunks.
4. The adviser's register (its prompt lists the gap ids) adds gap-9 and the candidate; label stays v5, unscored, one
   docstring line. Recorded runs replay as recorded.
5. Tests fail first then pass: gap-9's clauses resolve to chunks; both COPPA quotes are verbatim in the fetched file;
   the README register has ten rows plus candidates; `gaps` byte-identical on a second run. Full suite, CI green,
   commit, push. Report under 15 lines to `docs/report-back/2026-10-2X-task-15-gap-9.md`.

## Stop and ask when

- The fetch fails or the text differs from the quotes above.
- A chunk does not say what this order claims it says.
- Anything needs a model call or a change to keys, `rules.json` or `kb/chunks/` beyond the searched rows.

## The 2026-10-22 search (hq, before this order starts)

Perplexity, both languages: TDRA instructions or policy under Child Digital Safety Law 26/2025 Art 11; a Cabinet
resolution classifying digital content or services under Art 6; a penalties regulation under Art 16; TDRA's
regulations register 2026. Result pasted here by hq with the date. Found: this order is rewritten (the gap becomes a
method gap or is dropped). Not found: the order runs as written.

### Result, 2026-10-22 (Perplexity, pasted by Iyas; sources not yet opened by hq)

- Art 11: no TDRA instrument found. Nearby, not Art 11 instruments: TDRA Internet Access Management policy (pre-dates
  the law); TDRA consumer hub page "Telecom for Minors" (خدمات الاتصالات للقُصَّر, 2026-07-23), an initiative with
  licensees (safe packages, parental controls) that "supports the objectives" of the law; a "Children's Communication
  Services Programme" in press only (GDN Online, 2026-10-21).
- Art 6: no general classification resolution. Cabinet Resolution 106/2026 (children's access to social media,
  uaelegislation.gov.ae/en/legislations/4506, English download reported available) is scoped to social media
  platforms; u.ae still describes the classification in the future tense.
- Art 16: no penalties regulation; press fine figures have no published instrument behind them.

hq reading (Opus, 2026-10-22, superseded by the section below): the gap holds; a Fable session opens the two
primaries and amends item 2.

### Second search and primaries, 2026-10-22 (Fable; sources opened by hq)

Second deep search (Perplexity, "UAE Child Digital Safety: Implementing Instruments Status Check", saved as
`perplexity-2026-10-22/uae-child-safety-instruments-status-check.txt`): nothing new under Arts 6, 11 or 16. It
checked the TDRA Regulations and Ruling register in both languages, the TDRA 2026 press archive, uaelegislation.gov.ae
(law 3912 and its related-legislations page, Resolution 4506), three MOJ pages and three u.ae pages. Its only
instrument is Resolution 106, which it says "should not be relabelled as the Article 6 classification resolution".
New facts it adds, all confirmed on the official page: issued 2026-06-17, in force 2026-06-30, Official Gazette 826
of 2026-06-29. It did not find the Telecom for Minors page. It reports the English `/download` as unverified.

Primaries opened by hq on 2026-10-22 (scrapling), saved under `standards-text/` with URL and date:
- `cabinet-resolution-106-2026-children-social-media-en.txt`: full nine articles from the official English page. The
  `/download` endpoint returned an empty body to two fetchers; the page text is used. Scope is social media platforms
  only (Art 1 definition, Art 2); telecom providers and ISPs are not addressed; its standards wait on the Child
  Digital Safety Council (Arts 3(4)(c), 4(1)(h), 4(2)(d), 7(5)) and its penalties on the Art 16 list (Art 7(1), (2)).
- `tdra-telecom-for-minors-page-2026-10-22-en.txt` and `-ar.txt`: an initiative page, no instrument number, no legal
  basis clause, no obligation on licensees; the English page is dated 2026-10-01, the Arabic 2026-07-23.

Decision (Fable, 2026-10-22): the gap holds. It narrows only in wording: a published UAE text now says how a
social media platform learns a user's age (Resolution 106 Art 4), so the row says "no text addressed to a telecom
provider" rather than "no text". Kind stays method, category stays legislative gap, addressees stay TDRA and Cabinet.
The row quotes both documents so a judge's "there must be some document" is answered in the row itself.
Not opened: the u.ae children's digital safety page, the eca.gov.ae announcement and the Detectivision article the
second search cites; nothing from them enters the order.
