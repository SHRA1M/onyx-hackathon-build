# Report-back: Task 23, gap hunt (DRAFT, paused 2026-10-24)

Order: `docs/work-orders/2026-10-24-task-23-gap-hunt.md` (filed 7c9b32b). Base: d770363 (after Task 22's 1aeb31a).
Branch: `task-23-wip` (not merged to main). No model calls, USD 0.

## Status: paused at the page limit

- Report: **6 pages, 2,286 words** (Word, `scripts/report_pages.ps1`). **Ladder exhausted.** hq decides the 5-page cut.
- First sentence on page 6: "What ITU can reuse: the Arabic clause chunks and runs, for the Sandbox Network for Arabic-AI (SNAI); the manifest and the 43 verified records, for the call for domain-specific open knowledge bases; the five agent manifests, for the global open repository of AI agents and metadata."
- **Task 24** (`D:\Projects\hq\uni\ai-for-good-hackathon\task-24-uae-texts-order-2026-10-24.md`) waits until Task 23 is merged.

| Build | Pages | Words | Page 6 starts |
| --- | --- | --- | --- |
| C1 to C8 | 6 | 2,334 | "Before the final: the seven unseen scenarios run cold..." |
| ladder 1 (row 2 shortened) | 6 | 2,319 | "Before the final..." |
| ladder 2 (row 4 tail dropped) | 6 | 2,308 | "Before the final..." |
| ladder 3 (row 11 tail dropped) | 6 | 2,295 | "What ITU can reuse..." |
| ladder 4 (C6 sentence dropped) | 6 | 2,286 | "What ITU can reuse..." |

All four ladder steps stay applied in `docs/report.md` on the branch.

## Iyas's answers before the build (2026-10-24)

1. The three UAE texts were blocked (uaelegislation.gov.ae: 403, a 5,495-byte HTML challenge page; the hq copies `law-14-2023-en.pdf` and `cabres-28-2023-en.pdf` are that same HTML page; no `law-14-2023-ar.pdf`). Build without them: no Trade Law 14/2023 or Cabinet 28/2023 searched entries. Task 24 adds them.
2. gap-11 `kind`: the order's "standards" is not a kind (`onyx/gaps.py` KINDS: method, scope, absence, currency); Iyas chose **method**. Category stays "standards gap".
3. Every count the new manifest changes is updated, not only C8: report lines 25 ("eleven other UAE laws", one TDRA instrument added to "ten"), 47 ("SRC-2 47 documents"), 147 ("43 verified records"); README "47 rows", "43 VERIFIED", "Eleven rows".
4. Files outside the done-means list, allowed: `kb/chunks/` (new cited clauses), `kb/local-sources.json`, `kb/export/InputDocs/Inputs.md`, `onyx/gaps.py` (two labels), tests pinned to old wording or counts.

## What was built

- **A1:** `tdra-registration-policy-2011-en` downloaded from tdra.gov.ae (200, 282,605 bytes, 17 pages, byte-identical to hq's copy), chunked; 6.1.1 and 6.1.2 cited. The other three A1 rows: not built (answer 1).
- **A2:** six extracts under `kb/sources/global/` (scrapling for EUR-Lex, eCFR versioner API for 47 CFR, curl for Justice Laws), each with source line, date and SHA-256 in the manifest. OLA ss. 22 to 26 are on `page-2.html`, s. 27 on `page-3.html` (not page-3 alone as the order guessed); the row records page-2 and the notes name page-3.
- **C8 counts, how counted:** documents = manifest rows (47); foreign texts = rows with `jurisdiction` "foreign" (9); verified = rows with status VERIFIED (43). Before this task the same rule gave 3 foreign rows, not the "four" the report said.
- **B:** gap-11 added; gaps 2, 4, 6, 7, 9 `gap` text replaced verbatim; `searched` extended: gap-3 (registration 6.1.1, 6.1.2), gap-4 (PDPL 24(1), 24(2), 25), gap-7 (CPR 3.3). Gap-2 already searched CPR 4.7.2. Two candidates (see point 2 below).
- **C:** C1 to C8 applied, then ladder steps 1 to 4. C9: `docs/report.docx` rebuilt.
- Chunks: 138 cited clauses in 16 documents (was 130 in 15); added lines only; CPR and licence files restored after `kb chunk` (hand fixes kept).

## Things hq should know

1. **Gap-11 changes the adviser's prompt.** The adviser lists the register from `gaps.json`, so gap-11 sits at line 11 and the candidates move to lines 12 and 13. Tasks 15 and 20 did the same; followed them: a dated note in `onyx/agents/base.py`, label stays v5, recorded runs replay as recorded. `eval` output unchanged.
2. **Breach-notification candidate extended, not duplicated.** The register already held "Breach notification without a period" (PDPL 9(1)). It gains PDPL 9(2) and the GDPR 33(1) example; "Sub-processor authorisation" (PDPL 7(5), 8(1), 8(10); GDPR 28(2)) is new. That makes the four named candidates C6 counts (Arabic records, breach, Executive Order, sub-processor).
3. **Gap-7's new wording cites the Trade Law** (Art 1, 5(7)), which is not in the KB until Task 24.
4. **Register and report name different examples for gaps 2 and 4.** B2 says keep everything but `gap`, so the register keeps EU AI Act 50(1) and IMDA 2.2.2 (gap 2) and GDPR 22(3) (gap 4); the report now cites CRD 8(2) (row 2) and GDPR 12(3) (row 4).
5. **`docs/gaps.md` has no count line**, so done-means check 4 ("count line says 11 gaps") cannot run as written. The README's "Ten rows" sentence now says "Eleven rows".

## Checks run (on the working tree before the commit)

- `uv run pytest`: 386 passed.
- `python -m onyx check-data`: ok, every quote verbatim.
- `python -m onyx kb verify`: VERIFIED 43, REFERENCED 1, UNVERIFIED 3, HISTORICAL 0; every fetched source matches its sha256.
- `git diff -- kb/manifest.csv`: 7 added rows, 0 removed lines.
- `git diff c5cea32 -- onyx/gate.py onyx/data/rules.json onyx/data/keys onyx/data/mandates.json onyx/eval.py runs/`: empty.
- `eval` recomputed (60 runs); `git diff -- eval/results.md eval/results.json`: empty.
- Report diff `grep -E '^[-+].*\[C[35]'`: empty.
- Not run: CI on the branch, the page count at 5 (not reached).

| document_id | status | sha256[:12] |
| --- | --- | --- |
| tdra-registration-policy-2011-en | VERIFIED | 5108ee3e9f20 |
| eu-dsa-2022-2065-art12-20 | VERIFIED | 1d5517ad09d2 |
| eu-crd-2011-83-art8 | VERIFIED | 4e475ce16077 |
| eu-ecommerce-2000-31-art10-11 | VERIFIED | 484dd3dc2a5e |
| gdpr-art12-28-33 | VERIFIED | af51a747069e |
| us-47cfr-64-2010 | VERIFIED | 8d8f50f5a9bf |
| ca-ola-s22-27 | VERIFIED | 47b831156cb3 |

## Open for hq

- The 5-page cut.
- Answers 2 and 4 above, and points 2, 4 and 5: confirm or rule.
- Task 24 after the merge.

## Part A2 clauses, verbatim from the fetched files

**DSA Art 12(1)** (`kb/sources/global/eu-dsa-2022-2065-art12-20.txt`)

> 1.   Providers of intermediary services shall designate a single point of contact to enable recipients of the service to communicate directly and rapidly with them, by electronic means and in a user-friendly manner, including by allowing recipients of the service to choose the means of communication, which shall not solely rely on automated tools.

**DSA Art 20(6)** (`kb/sources/global/eu-dsa-2022-2065-art12-20.txt`)

> 6.   Providers of online platforms shall ensure that the decisions, referred to in paragraph 5, are taken under the supervision of appropriately qualified staff, and not solely on the basis of automated means.

**CRD Art 8(2)** (`kb/sources/global/eu-crd-2011-83-art8.txt`)

> ►M4
> If a distance contract to be concluded by electronic means places the consumer under an obligation to pay, the trader shall make the consumer aware in a clear and prominent manner, and directly before the consumer places his order, of the information provided for in Article 6(1), points (a), (e), (la), (o) and (p).
> ◄
> The trader shall ensure that the consumer, when placing his order, explicitly acknowledges that the order implies an obligation to pay. If placing an order entails activating a button or a similar function, the button or similar function shall be labelled in an easily legible manner only with the words ‘order with obligation to pay’ or a corresponding unambiguous formulation indicating that placing the order entails an obligation to pay the trader. If the trader has not complied with this subparagraph, the consumer shall not be bound by the contract or order.

**e-Commerce Art 11(2)** (`kb/sources/global/eu-ecommerce-2000-31-art10-11.txt`)

> Member States shall ensure that, except when otherwise agreed by parties who are not consumers, the service provider makes available to the recipient of the service appropriate, effective and accessible technical means allowing him to identify and correct input errors, prior to the placing of the order.

**GDPR Art 12(3)** (`kb/sources/global/gdpr-art12-28-33.txt`)

> The controller shall provide information on action taken on a request under Articles 15 to 22 to the data subject without undue delay and in any event within one month of receipt of the request. That period may be extended by two further months where necessary, taking into account the complexity and number of the requests. The controller shall inform the data subject of any such extension within one month of receipt of the request, together with the reasons for the delay. Where the data subject makes the request by electronic form means, the information shall be provided by electronic means where possible, unless otherwise requested by the data subject.

**GDPR Art 12(4)** (`kb/sources/global/gdpr-art12-28-33.txt`)

> If the controller does not take action on the request of the data subject, the controller shall inform the data subject without delay and at the latest within one month of receipt of the request of the reasons for not taking action and on the possibility of lodging a complaint with a supervisory authority and seeking a judicial remedy.

**GDPR Art 28(2)** (`kb/sources/global/gdpr-art12-28-33.txt`)

> The processor shall not engage another processor without prior specific or general written authorisation of the controller. In the case of general written authorisation, the processor shall inform the controller of any intended changes concerning the addition or replacement of other processors, thereby giving the controller the opportunity to object to such changes.

**GDPR Art 33(1)** (`kb/sources/global/gdpr-art12-28-33.txt`)

> In the case of a personal data breach, the controller shall without undue delay and, where feasible, not later than 72 hours after having become aware of it, notify the personal data breach to the supervisory authority competent in accordance with Article 55, unless the personal data breach is unlikely to result in a risk to the rights and freedoms of natural persons. Where the notification to the supervisory authority is not made within 72 hours, it shall be accompanied by reasons for the delay.

**47 CFR 64.2010(b)** (`kb/sources/global/us-47cfr-64-2010.txt`)

> (b) Telephone access to CPNI. Telecommunications carriers may only disclose call detail information over the telephone, based on customer-initiated telephone contact, if the customer first provides the carrier with a password, as described in paragraph (e) of this section, that is not prompted by the carrier asking for readily available biographical information, or account information. If the customer does not provide a password, the telecommunications carrier may only disclose call detail information by sending it to the customer's address of record, or by calling the customer at the telephone number of record. If the customer is able to provide call detail information to the telecommunications carrier during a customer-initiated call without the telecommunications carrier's assistance, then the telecommunications carrier is permitted to discuss the call detail information provided by the customer.

**OLA s. 22** (`kb/sources/global/ca-ola-s22-27.txt`)

> 22 Every federal institution has the duty to ensure that any member of the public can communicate with and obtain available services from its head or central office in either official language, and has the same duty with respect to any of its other offices or facilities
> (a) within the National Capital Region; or
> (b) in Canada or elsewhere, where there is significant demand for communications with and services from that office or facility in that language.

**OLA s. 26** (`kb/sources/global/ca-ola-s22-27.txt`)

> 26 Every federal institution that regulates persons or organizations with respect to any of their activities that relate to the health, safety or security of members of the public has the duty to ensure, through its regulation of those persons or organizations, wherever it is reasonable to do so in the circumstances, that members of the public can communicate with and obtain available services from those persons or organizations in relation to those activities in both official languages.

**OLA s. 27** (`kb/sources/global/ca-ola-s22-27.txt`)

> 27 Wherever in this Part there is a duty in respect of communications and services in both official languages, the duty applies in respect of oral and written communications and in respect of any documents or activities that relate to those communications or services.
