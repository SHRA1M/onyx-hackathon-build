# Report-back: Task 24, the three UAE texts into the KB and the register (2026-10-25)

Order: `docs/work-orders/2026-10-24-task-24-uae-texts.md` (copy of hq's `task-24-uae-texts-order-2026-10-24.md`). Base: cc7b73b (Task 23 merged, report-back filed). Branch: `task-24`. No model calls, USD 0.

## Status: done, report 5 pages, 2,181 words

## What was built

- **KB rows:** `law-14-2023-en`, `law-14-2023-ar`, `cabres-28-2023-en` added after `tdra-registration-policy-2011-en` in `kb/manifest.csv`, VERIFIED, full sha256, portal URL as source, accessed and fetched 2026-10-24, http_status 403 (the portal's answer to a script), notes as Task 23 Part A plus "PDF saved by hq from a browser". PDFs copied from hq's `fetched-2026-10-24/` into `kb/sources/` (gitignored, as every full text); not re-downloaded.
- **Text extracts:** made with pypdf (PyMuPDF is not installed here) into `kb/sources/law-14-2023-en.txt` and `kb/sources/cabres-28-2023-en.txt`, with `===== PAGE n =====` markers as the hq texts carry, and the running page headers removed (each carries its page number, so the splitter could not drop them). The Arabic law, as every Arabic law row, has no text extract and is not chunked.
- **Departure from the order:** it says the extracts go in `standards-text/` like the other UAE texts. That folder is in hq, and this repo's rules write nothing outside it. The extracts sit in `kb/sources/` and `kb/local-sources.json` points to them from hq's folder (`../../../engineering/onyx-hackathon-build/kb/sources/...`), the way Task 23's global extracts are pointed to. The PDFs are pointed to in hq's `perplexity-2026-10-24/fetched-2026-10-24/`, as the registration policy is. If hq wants them in `standards-text/`, copying the two `.txt` files there and changing two paths is the whole move.
- **Chunks:** `kb/chunks/law-14-2023-en.jsonl` (Art 1, 5(7), 6(7), 13(2)) and `kb/chunks/cabres-28-2023-en.jsonl` (15(9), 24(3)). `kb chunk` rewrites every chunk file; the CPR and licence files it changed were restored (hand fixes kept), so only the two new files are added. 144 cited clauses in 18 documents.
- **Register** (`onyx/data/gaps.json`, `searched`, after the existing entries): gap-1 Art 6(7); gap-2 Art 13(2); gap-3 Cabinet 28/2023 15(9), 24(3), each with the note that it addresses another event and maps no telecom-care act to a trust level; gap-6 Art 1 ("Modern Technology"); gap-7 Art 1, 5(7); gap-11 Art 6(7). Each quote occurs once, verbatim, in the extract and in its chunk. Quotes avoid the words the text layer splits ("T rust", "th e"). `docs/gaps.md` regenerated; the README table does not show `searched`, so it is unchanged. `kb/export/InputDocs/Inputs.md` regenerated (UAE_Binding 32 files).
- **Art 5(5) left out of gap-11.** Its text (below) has the trader publish the terms, stages and prices, and makes the purchase itself count as acceptance. It does not support "a safe default against a mistaken order"; if anything it cuts the other way.

## Counts (from `kb/manifest.csv`)

- Documents = manifest rows: **50** (was 47). Foreign = rows with `jurisdiction` "foreign": **9** (unchanged). Verified = rows with status VERIFIED: **46** (was 43). `kb verify`: VERIFIED 46, REFERENCED 1, UNVERIFIED 3, HISTORICAL 0.
- Changed in `docs/report.md` (Introduction "50 documents", "46 are verified"; SRC-2 "50 documents"), `README.md` ("50 rows", "46 VERIFIED"), and the two tests pinned to them.
- **"Other UAE laws, resolutions and TDRA instruments": now "fifteen", was "eleven". Please check.** Counted as distinct UAE `instrument` values with binding_status binding and status VERIFIED, other than the four the sentence names (Telecom Law, CPR, Licence, PDPL). That rule gives 15 now, and gave 13 on the Task 23 manifest, so the old "eleven" was already two short by it. The fifteen: Cabinet 56/2024, 57/2024, 66/2023, 28/2023; Child Digital Safety 26/2025; Consumer Law 15/2020; Cybercrimes 34/2021; Decision 16/2026; Electronic Transactions 46/2021; Instructions 1/2014; Trade Law 14/2023; QoS v3; Spam Calls v4; Spam SMS 2022; Registration Policy. If hq counts otherwise (say, without the TDRA policies), it is one word on report line 23.

## Checks run

1. `git diff cc7b73b -- onyx/gate.py onyx/data/rules.json onyx/data/keys onyx/data/mandates.json onyx/eval.py runs/`: empty.
2. `git diff cc7b73b -- docs/report.md | grep -E '^[-+].*\[C[35]'`: empty.
3. `eval` recomputed (60 runs); `git diff -- eval/results.md eval/results.json`: empty.
4. The three rows VERIFIED; manifest sha256 equals `sha256sum kb/sources/<id>.pdf` for each: a52f4dcc2315..., 4769f8f1af60..., 89ab2b52d9d5... (full values in the manifest). The PDFs are not committed (`kb/sources/` is gitignored: "Full text not redistributed").
5. `docs/gaps.md` lists `law-14-2023-en:6(7)` (gap-1, gap-11), `:13(2)` (gap-2), `cabres-28-2023-en:15(9)`, `:24(3)` (gap-3), `law-14-2023-en:1` (gap-6, gap-7), `:5(7)` (gap-7).
6. Report 5 pages, 2,181 words (`scripts/report_pages.ps1`).
7. `uv run pytest`: 386 passed. `check-data`: ok. CI: named in the report to hq.
8. `git diff cc7b73b -- kb/manifest.csv`: 3 added lines, 0 removed.

## Clauses, verbatim from the PDFs

**Decree-Law 14/2023, English** (`kb/sources/law-14-2023-en.pdf`, text layer by pypdf; line breaks joined, running headers removed; split words such as "obtain ed" are the PDF text layer's)

*Art 1, "Modern Technology-Based Trade"*

> Modern Technology- Based Trade : The sale and purchase of goods, services and relevant data through technological platforms or modern technology, including, inter alia, the websites, e -platforms or smart applications, including the transactions carried out through electronic or digital commerce or social media platforms. This includes non -digital goods and services that are obtain ed physically or virtually through modern digital technology or technological platforms.

*Art 1, "Modern Technology"*

> Modern Technology : Any technological platforms used for Modern Technology -Based Trade, whether electronic, digital, biometric, artificial intelligence technology, blockchain technology, or in technological platforms, whether by accessing websites or through smart applications.

*Art 2(2)(b)*

> b. The data, platforms and smart applications used for purposes other than Modern Technology-Based Trade.

*Art 5(5)*

> 5. Determining the terms, conditions and details of the multiple stages regarding the sale of goods and services through Modern Technology, including specifying the price of goods and services, fees and prices for logistics services and digital payment services, in addition to making the same publicly available on the website, application or other Modern Technology for the digital trader and making the digital contract or terms and conditions available in such regard if there is no digital contract, provided that the purchase of goods and services shall be deemed acceptance by the consumer of the digital contract or these terms and conditions.

*Art 5(7)*

> 7. Refraining from dealing in a misleading manner or provide incorrect data that does not give the true description of the good or service.

*Art 6(7)*

> 7. Designate numbers and means of communication regarding complaints, which shall be always available without interruption with qualified staff, as well as a mechanism to follow up on the complaints and communicate with a clear address, in addition to updating the same periodically in a way that is easily accessible, whether through the website or through any other means or method

*Art 13(2)*

> 2. The validity of the contract shall be subject to the terms and conditions specified in the legislation in force in the State, as follows: a. Fulfillment of the capacity of contracting parties upon satisfying the requirements and conditions of the new digital identity through modern technology that enable the verification of the identity of contracting parties. b. Fulfillment of the offer and acceptance and the contractual relationship executed upon satisfying the requirements of the digital identity and digital signature.

**Cabinet Resolution 28/2023, English** (`kb/sources/cabres-28-2023-en.pdf`, same extraction)

*Art 15(9)*

> 9. Notifying the party relying on T rust Services or Qualified Trust Services of levels of security and trust of the used Digital Identity as part of the service provision.

*Art 24(3)*

> 3. Where the Qualified Trust Service Provider uses a procedure equivalent to the appearance in person to verify the identity and capacity of the Person to whom a Qualified Electronic Signature/Seal Auth entication Certificate will issue, pursuant to Clause (4) of Artic le (34) of the Decree -Law, the TDRA may, in addition to th e Compliance Assessment report, ascertain that such procedures is equivalent to the appearance in person, pursuant to the controls issued by the TDRA in this regard.

