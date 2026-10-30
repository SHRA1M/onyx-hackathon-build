# Task 33: the three 10-30 searches enter the KB and register (written 2026-10-30, hq uni, Fable)

Repo: `D:\Projects\engineering\onyx-hackathon-build`. Start from `main` after Task 32 (`task-32` tagged). Branch
`task-33`, one PR. Build on Opus. Pattern: Tasks 30 to 32. Sources of the words, all in
`D:\Projects\hq\uni\ai-for-good-hackathon\perplexity-2026-10-30\`:

- `none-rows-read-2026-10-30-fable.md` (gap 8 and candidate-4-4 examples)
- `foreign-currency-read-2026-10-30-fable.md` (Wales re-hold, Spain and AI Act notes, the 17-row re-fetch)
- `uae-unread-read-2026-10-30-fable.md` (Executive Order, Cabinet 200/2025, Cabinet 52/2024, the Data Office)

Fetch every text yourself from the URL in the read file and compare the SHA-256 with hq's copy in
`D:\Projects\hq\uni\ai-for-good-hackathon\standards-text\`; hq's copy is the check, not the source. The uaelegislation.gov.ae
files are the exception: the portal refuses non-browser clients, so take hq's copies as local sources the way the
other portal rows do, record the portal URL, and note "fetched through a browser 2026-10-30" in notes. Every quote in a
`searched` or `global_examples` entry must be found word for word in the stored text (the existing test; a quote from a
file that is not chunked is checked locally, Task 32's mechanism).

## Why

The KB, datasheet and gaps.md say the Executive Order 3/2004 is unpublished. It is published in full on tdra.gov.ae,
English and Arabic. A TDRA judge would catch that in a minute; it is fixed here. The two Cabinet fine schedules the
10-17 session could not read are now read and sharpen gaps 1 and 2 and candidate-79bis-2. The Data Office, addressee
of gaps 2, 4 and 5, is being folded into a new federal authority (announced 2026-06-14); the register says so once.
Gap 8 and candidate-4-4 lose their "none" cells for two sister-standard and two binding examples.

## Part A: knowledge base (eleven rows; ids are yours to adjust to the existing style, say what you chose)

Foreign, from `none-rows-read` (URLs, hashes, hq copies and verbatim text there):

1. `3gpp-ts-28-535-v19`: ETSI TS 128 535 V19.0.0 (2025-10), 3GPP TS 28.535. `method`, `foreign`, `en`,
   `source_type` standard, country `EU` or `INT` as the schema allows. Notes: "Global example; design basis only, never a
   deciding clause. Clause 4.2.3 read the same in V18.2.0."
2. `etsi-gs-zsm-009-1-v1-1-1`: ETSI GS ZSM 009-1 V1.1.1 (2021-06). Same fields.
3. `eu-eecc-2018-1972-art105`: Directive (EU) 2018/1972, Article 105 (extract), from legislation.gov.uk's adopted text.
   `binding`, `foreign`, `en`, `extract`, `EU`. Try EUR-Lex first (CELEX 32018L1972 or consolidated 02018L1972-20241018);
   hold it if it answers, else the legislation.gov.uk copy with a note saying EUR-Lex refused.
4. `de-tkg-2021-para-56`: Telekommunikationsgesetz 2021, § 56, gesetze-im-internet.de. `binding`, `foreign`, `de`,
   `extract`, `DE`. Notes: "German original; no official translation; the row's English gloss is ours."

UAE, from `uae-unread-read`:

5. `executive-order-3-2004-en`: the existing `executive-order-3-2004` row, renamed if the style wants the suffix. URL
   `https://tdra.gov.ae/-/media/About/Legal-References/LAW/LAW-English/Decision-of-the-Supreme-Committee-for-the-Supervision-of-the-Telecommunications-Sector-No-3-of-2004.ashx`,
   28 pages, expected SHA-256 `23f3e4022033142fac09fb7e37281225c2c216fac8cd8c54f02b0e2d6945f2e5`. Status VERIFIED,
   `binding`, `UAE`, `en`, `is_official_translation` "yes (cover: Arabic prevails)", `source_type` executive order.
   Text extract: hq's `standards-text/executive-order-3-2004-en.txt` (pypdf, page markers) or your own, splitter
   `article`. Notes: "Official Gazette 421, October 2004; amended by Supreme Committee Resolutions 4/2005 and 2/2006 (two
   footnotes). The 10-17 fetch saw only a cover page; the full order was served 2026-10-30." Delete the old note.
6. `executive-order-3-2004-ar`: Arabic, URL
   `https://tdra.gov.ae/-/media/About/Legal-References/LAW/LAW-Arabic/Decision-of-the-Supreme-Committee-for-the-Supervision-of-the-Telecommunications-Sector-No-3-of-2004A.ashx`,
   33 pages, expected SHA-256 `99cb1e43df2633fb7c3fbc56e2fb643f709036b44d16963f641fc122fee1ab8f`. VERIFIED,
   `binding`, `ar`, original. Image only: no text extract, not chunked, like the other Arabic law rows.
7. `cabres-200-2025-en`: Cabinet Resolution No. 200 of 2025 Regarding the Schedule of Administrative Violations and
   Penalties for Acts Committed in Violation of Federal Decree-Law No. 14 of 2023. Portal
   `https://uaelegislation.gov.ae/en/legislations/3989` (download `/download`), 9 pages, local source
   `standards-text/modern-tech-trade-penalties-cabinet-200-2025-en.pdf`, SHA-256
   `cdff987ad304ef162852be32e693634dfae79dddbf0144e63b24b1561a26972d`, text `...-en.txt`, splitter `article`. Issuer
   UAE Cabinet, instrument `cabres-200-2025`, `binding`, `UAE`, `en`. Notes: "Issued 2025-11-27; in force the day after
   Gazette publication (Art 7; take the Gazette date from the portal record). Under Decree-Law 14/2023; the Ministry of
   Economy imposes. Portal: the Arabic text prevails."
8. `cabres-200-2025-ar`: Arabic, portal `/ar/legislations/3989`, local source
   `standards-text/modern-tech-trade-penalties-cabinet-200-2025-ar.pdf`, 6 pages, SHA-256
   `ad851801ec71e97c5ba855da5b3c35e1ff72c3d313428b03e7346f0a769ace5f`. VERIFIED, `ar`, original, image only, no text.
9. `cabres-52-2024-ar`: Cabinet Resolution No. 52 of 2024 Concerning the Administrative Penalties for Violating Federal
   Decree-Law No. 46 of 2021 (Electronic Transactions and Trust Services) and its Executive Regulations. Portal
   `https://uaelegislation.gov.ae/ar/legislations/2585`, local source
   `standards-text/etransactions-penalties-cabinet-52-2024-ar.pdf`, 6 pages with the annex, text layer, SHA-256
   `32c667ed631031cb33a25d3ed746904b62ba2d0e4bd2097c3990202404e46693`, text `...-ar.txt`. VERIFIED, `binding`, `ar`,
   original, instrument `cabres-52-2024`. Notes: "Issued 2024-05-15, in force 2024-06-01, Gazette 776 of 2024-05-31.
   TDRA imposes. Binds trust service providers, not telecom licensees."
10. `cabres-52-2024-en`: the portal page's English article text, `https://uaelegislation.gov.ae/en/legislations/2585`,
    held as page text the way `cabres-106-2026-en` is (fetch it through a browser or take the text from the read file's
    source; say which). VERIFIED, `en`, translation ("the Arabic text will prevail"). Notes: "Articles 1 to 8 only; the
    annex is a separate portal page, not held; see the Arabic row."
11. `fed-ai-data-authority-2026-06-14`: announcement, "Mohammed bin Rashid approves establishing the Federal Authority
    for Artificial Intelligence and Data", UAE Digital Government / WAM, 2026-06-14,
    `https://dgov.tdra.gov.ae/ar/media-hub/news/mohammed-bin-rashid-approves-establishing-artificial-intelligence-and-data-authority`.
    Status REFERENCED (opened, text not held), `binding_status` advisory, `UAE`, `ar`, `source_type` announcement
    (add the value if absent). Notes: "Announcement, not a law: the Data Office's competences move to the new
    authority; no decree number or transfer date published. The PDPL still names the Data Office."

Expected after Part A, on top of Task 32's 64 / 59 / 4 / 1 / 17 / 29: **74 documents, 69 VERIFIED, 3 UNVERIFIED,
2 REFERENCED, 21 foreign, 31 UAE instruments** (the announcement is not an instrument). If the counts come out
otherwise, stop and say why. No chunks for any new row: the agents do not retrieve them, no run changes.

## Part B: the 17 foreign rows (from `foreign-currency-read`)

1. Re-fetch every foreign row from its manifest URL with the original extraction and compare SHA-256 to the manifest.
   Report one table: row, fetched date, hash equal or not. A differing hash is a stop-and-ask (show the diff); never
   commit a manifest changed only by access dates.
2. Wales: re-hold `wales-wls-no1-2015-sch1` and the reg 3 row from the current text, not `/made`:
   `https://www.legislation.gov.uk/wsi/2015/996/schedule/1/data.xht?view=snippet&wrap=true` and
   `/regulation/3/data.xht?view=snippet&wrap=true`. Title drops "as made"; notes name S.I. 2021/1352 (2021-12-03, reg
   3(1)) and S.I. 2025/339 (2025-03-28, reg 3(3)). Standards 15, 22, 60 quotes unchanged: the quote test proves it.
3. Spain: `es-ley-10-2025` notes and gap-1's Spain example note gain "In force 2025-12-28; companies have until
   2026-12-28 to adapt (disposición transitoria única)".
4. AI Act row notes gain: "Regulation (EU) 2026/1744 (OJ 2026-07-24) is inside this consolidation; it does not touch
   Art 50(1) or 50(5)."
5. For the four EUR-Lex consolidations (AI Act, GDPR, CRD, e-Commerce) open the CELEX record page, record the latest
   consolidation date in the report-back; hold a newer one only if it changes a quoted article (then stop and ask).

## Part C: gap register (`onyx/data/gaps.json`, `docs/gaps.md`); recommendations unchanged unless named

- **gap-8:** `global_examples` gains two entries, `global_none` emptied. (a) 3GPP TS 28.535 §4.2.3, quote "The
  management system collects, analyses and presents the data to the human operator or other management entity, but
  the human operator or other management entity decides which action to take." (b) ETSI GS ZSM 009-1 §7.2.2.4, quote
  "The customization flow may be used to configure the CL, monitor its continuous operations, approve/reject
  recommendations, explain the CL operation and decisions". Prose line after the examples: "Neither names a withheld
  output routed to a named person with its own reference point; the recommendation stands as the fuller version." Say
  they are method texts, like Y.3172; never that they outrank it.
- **candidate-4-4-fixed-term-bundle:** `global_examples` gains EECC Art 105(3) (quote from "Before the contract is
  automatically prolonged" to "means by which to terminate the contract.") and TKG § 56(3) (a continuous run, for
  example from "kann der Endnutzer" to "kündigen."; our English gloss in `says`, marked ours). `global_none` emptied.
  Recommendation gains: "and, if 4.4, require the warning before and the one-month exit after".
- **gap-1:** two `searched` entries. `executive-order-3-2004-en:32`, says "the licensee reports complaint numbers and
  the procedures taken to TDRA on request; a reporting duty, nothing on the hand-over or its timing", quote the article.
  `cabres-200-2025-en:Schedule row 7`, says "where 14/2023 applies, no complaints mechanism is fined (warning, then
  AED 2,000 to 20,000 and twenty days' closure); still no stop, hand-over or clock", quote "Failure to allocate a
  mechanism for handling complaints."
- **gap-2:** `cabres-200-2025-en:Schedule row 1`, says "where 14/2023 applies, failing to verify the offer and
  acceptance is fined (AED 2,000 up to 100,000 and closure); what verifies a spoken 'yes' through an AI channel is
  unsaid", quote from "failure to verify the offer and acceptance" to "validity of the contract."
- **candidate-79bis-2-fine-schedule:** gap text gains one sentence: "The Cabinet has issued itemised schedules under
  three neighbouring laws (57/2024 telemarketing, 52/2024 trust services, 200/2025 digital trade); none under 79 bis
  (2)." `searched` gains `cabres-52-2024-ar:2(2)` (doubling on repetition within a year; Arabic quote from the stored
  text, English gloss from the portal page in `says`), `cabres-200-2025-en:3(3)` (the Ministry may skip the gradation
  for a serious violation), and `executive-order-3-2004-en:42`, says "a fine power for apparatus authorisations, no
  amount; not the licensee schedule". Addressee unchanged.
- **The "Executive Order unpublished" section of docs/gaps.md** (and its data) is rewritten: "The Executive Order,
  read in full (75 articles, English; the Arabic prevails): Art 30 directives, Art 32 complaint reporting, Art 42
  apparatus fines, Art 47 quality-of-service reporting. Nothing on an automated channel, consent, a hand-over or a
  licensee fine amount." Keep the licence 16.2 cite.
- **Data Office, once:** where the register introduces addressees (or in gap-2's addressee note, your choice; say
  where), one sentence: "The PDPL names the UAE Data Office (Art 24); its competences move to the Federal Authority
  for Artificial Intelligence and Data (announced 2026-06-14, `fed-ai-data-authority-2026-06-14`); the register keeps
  the statutory name." Addressee fields unchanged.

## Part D: report, README, datasheet, site

- Counts: "64 documents" to 74, "59 are verified" to 69, "seventeen foreign texts" to twenty-one, SRC-2's count, and
  the UAE-instrument count wherever stated to 31. "fifteen other UAE laws, resolutions and TDRA instruments" is
  recounted now (31 instruments minus the four named in the sentence; show the arithmetic), not left to submission day.
  Run the count check over every number the report states.
- Report line 26: "three unpublished texts back no claim" becomes "two unpublished texts and one unreachable one back
  no claim" (UNVERIFIED rows: the Cabinet agentic framework, the PDPL executive regulations, the CSC policy).
- Report gap table: row 8's example cell becomes "3GPP TS 28.535 §4.2.3; ETSI ZSM 009-1 §7.2.2.4". No other table
  change unless 5 pages hold; if they do, row 1's UAE cell may gain "no fine for a missing hand-over (200/2025 row 7
  fines only a missing mechanism)".
- Report: the Data Office sentence from Part C once, in the KB paragraph or as a table note, if 5 pages hold;
  otherwise README only, and say so.
- Datasheet line for the Executive Order goes with the row; the manifest note is the new one. README's "UNVERIFIED
  rows" line and the site's counts rebuild from the data.
- No sentence may say or imply that e& or du breaks any rule, law or its own code.

## Done means

- `kb verify`: VERIFIED 69, REFERENCED 2, UNVERIFIED 3, all hashes match (show output); every hq SHA-256 named above
  matches the file you hold.
- Part B table: 17 rows, every hash equal (or a stop).
- Quote-in-stored-text check passes for every new `searched` and `global_examples` quote (show count).
- Data check passes; register, site and datasheet rebuilt twice, identical.
- Recorded runs replay as recorded; `verify-log` passes on every stored log.
- Full test suite passes; CI green on the PR.
- Report 5 pages (Word count, as in Task 30); hq's `report-draft-2026-10-23.md` updated to match `docs/report.md`
  byte for byte (say which file you copied to which).
- Count check output listed in the report-back, every number.
- Report-back at `docs/report-back/2026-10-30-task-33-three-searches.md` with the table of checks.

## Limits

No change to gates, keys, runs, prompts, chunks or eval. Seven layers (`D:\Projects\hq\_reference\llm-agents.md`):
unchanged from Task 32, nothing shipped or deferred by this task, no agent code touched. No other gap rows, no new
gaps, no new recommendations beyond the candidate-4-4 clause. USD 0 model spend. Every change done before 2026-11-06.

## Stop and ask when

- Any foreign row's re-fetched hash differs from the manifest, or any hq SHA-256 above differs from the file you fetch.
- A newer EUR-Lex consolidation changes an article we quote.
- The counts after Part A are not 74 / 69 / 3 / 2 / 21 / 31.
- The report will not hold 5 pages with the row 8 cell and the "two unpublished" sentence (those two are required;
  the row 1 cell and the Data Office sentence are the ones to drop first).
- The schema needs a value beyond `executive order`, `announcement`, `extract` or a `de` language code.
- A quote in this order is not found word for word in the stored text: do not trim it to fit; report the mismatch.
