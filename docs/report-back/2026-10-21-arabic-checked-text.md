# Report back: checked Arabic texts and the lam-alef fix, 2026-10-21

For `D:\Projects\hq\uni\ai-for-good-hackathon`. Order: `docs/work-orders/2026-10-17-onyx-mizan.md` (Task 3), with Iyas's instructions in session on 2026-10-21.

## Summary

Every Arabic quote the gates rely on now traces to a checked text. Decision 16/2026 4.17 and 4.18 come from `decision-16-2026-ar-4.17-4.18-checked.txt`, and the 4.18 rule covers both two-hour limits: ours (block and notify, from receipt of the report) and the other licensee's (block, from receipt of our notice). Licence 9.1's Arabic comes from `licence-2-2026-ar-9.1-checked.txt`. The CPR Arabic chunks no longer carry the reversed lam-alef: 38 of 52 Arabic chunks had it, now 0, and `check-data` fails if it comes back.

## Evidence

- `check-data`: ok, rules 94, mandate verbs 16, manifest rows 40; it lists d16-4-17, d16-4-18 and licence-9-1 with their checked files, none pending.
- pytest: 27 passed, 1 skipped (answer keys not written). The new lam-alef test failed on 38 chunks before the re-chunk.
- Broken lam-alef count in the CPR Arabic PDF: hq .txt 1,417; pypdf 0; PyMuPDF 1,417; pdfminer 486; pdfium 1,401; pdftotext 0. Full table for every Arabic source in the repo archive (2026-10-21 entry).
- Re-chunk: same clause ids, English text unchanged, 46 CPR chunks changed.
- CI `reproduce` green on 79e74fc, fb71bd7, 6ae7419 and 5c020e8.

## Differs from the order

- New rule field `transcription` {from, field, checked_file}. A quote from page images or scanned text is valid only with an hq `-checked.txt`, and the KB text must be copied from it, not from the note the quote came from.
- `kb/extracts/` holds copies of hq checked files; a paired extract (`pair_of`) fills `text_ar` of a document chunked from its text layer.
- The CPR Arabic is read from the PDF with pypdf, not from the hq .txt (PyMuPDF output).
- `quote_ar` of cpr-17-2 ("بمدة لا تقل عن ثمان وعشرون يوماً") and cpr-26-7-2 ("يستثنى أو يستبعد منها استخدام وكلاء غير بشريين") now hold the correct words.

## Decisions taken in the build

- pypdf over pdftotext (both 0 on the CPR): pypdf is already a dependency; pdftotext inserts bidi control marks.
- The detector flags only shapes correct Arabic never has, plus broken words already seen; no swap rule (Iyas).

## Open questions for hq

1. The hq .txt files for Arabic sources are PyMuPDF output and keep the reversed lam-alef. Any Arabic quoted in the research notes from them needs a re-check.
2. Telecom Law and Cabinet 57/2024 Arabic show about 95 to 136 hits under every extractor. Not read; not chunked.
3. Decision 16/2026 4.19 still has no checked text.
