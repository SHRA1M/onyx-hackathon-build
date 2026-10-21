# Report back: keys after hq review, licence splitter, Task 4, quote audit, 2026-10-21 (Opus)

For `D:\Projects\hq\uni\ai-for-good-hackathon`. Order: `docs/work-orders/2026-10-17-onyx-mizan.md`, Task 4, plus the hq keys review of 2026-10-21.

## Summary

The four key edits are in and re-hashed. The licence splitter reads the new pypdf text. Task 4 (hash-chained audit log, `verify-log`, replay store) is complete. A quote audit against pdftotext found five quotes for hq to decide.

## Evidence

check-data ok (107 rules, 16 verbs, 40 manifest rows); pytest 41 passed; `verify-log` printed 'chain ok', then 'first broken seq 2' after one line was edited. Commits 7cb7900, 2a3af77, ec000e3, all pushed.

## Differs from the order

- Addendum 17's override tests (`test_override_release_logs_approver_name`, `test_override_refused_on_block`) are named for Tasks 4 and 6. They need the gate's hold and block, so they move to Task 6; the log already carries `actor` and `reason` for them.
- `verify(path)` returns a bool as ordered; `first_break(path)` names the line.

## Decisions taken

- Hash: `sha256(prev_hash + canonical_json(event without 'hash'))`, sorted keys, compact, UTF-8; first prev_hash 64 zeros; run_start holds the sha256 of each key file as it is on disk.
- The licence chunks stay as committed: a rebuild brings two pypdf errors ('pur suant', 'billin g') along with the right 9.3 wording.

## Open questions for hq

1. **licence-9-3.** The PDF (page 24) reads 'the TDRA may resolve the issues between the parties in accordance with the Telecommunications Law'. The rule quote and the committed chunk lack both 'the'. Correct the quote? Then the licence chunks can be rebuilt, with 'pursuant' and 'billing' fixed from a checked file.
2. **Four more quotes not verbatim in the PDF text** (pdftotext, whitespace collapsed only):

| Rule id | What pdftotext has |
|---|---|
| cpr-4-7-3 | '...failed to optout, or failed to remove...'; the quote has 'opt- out'. PDF page 15 prints 'opt-' at a line end, then 'out'. |
| cpr-24-7 | '...marketing purposes or anticompetitive practices.'; the quote has 'anti- competitive'. PDF page 60 prints 'anti-' at a line end. |
| cpr-3-9-recordings | 'Recordings- voice/video/screen recordings, Shall be retained for at least 2 etc. years' (table cells interleaved) |
| cpr-3-9-notices | 'Notifications and warnings that Licensees Shall be retained for at least 2 and/or their Partners are obligated to send years by sms (or other electronic means).' (table cells interleaved) |

   Eight more did not match for layout only and match once that is removed: licence 3.4.1, 9.1, 9.2.4, 9.4.3 (Arabic column interleaved), PDPL 6(1)(b), 13(2)(g), 23(1)(a) (page footer), CPR 17.2 Arabic (bidi marks). The three transcribed quotes (licence-9-1 Arabic, d16-4-17, d16-4-18) match their hq checked files.
3. **Keys' 'frozen' line.** Each key still says 'Never edited after HASHES.txt is committed'; S1, S2 and S5 were edited by this review. Reword?
4. **'hq plan, S2'** (S2 key, steps 3 and 4 notes). No plan file labels a scenario S2. The words cited ('the controversy', 'collaboration, not substitution') are in `domain-problem-scores-2026-10-14.md` section 3.1, Scenarios, S2, which is not in the order's sources table. Repoint the reference, or add the file to the sources?
