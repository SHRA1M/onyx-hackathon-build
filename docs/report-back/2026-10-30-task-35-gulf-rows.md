# Report-back: Task 35, Gulf telecom regulations into the KB and register (2026-10-30)

Order: `docs/work-orders/2026-10-30-task-35-gulf-rows.md` (hq, Fable, 2026-10-30), base order plus Addendum A
(Saudi CST 552/1445 and Qatar 16/2010). Base `main` 462a4ea, branch `task-35`. Opus 5.5, one session. USD 0: no
model call.

**Limits:** KB manifest rows, local-sources, datasheet, export, intent, the register (`onyx/data/gaps.json`, its
renderers in `onyx/gaps.py` and `onyx/site.py`), `docs/gaps.md`, the site, the README, the report's three count
lines, tests, CHANGELOG. Fetched only the five PDF URLs and the Al Meezan URL the order names. No chunks, no runs, no
gate, rule, mandate, prompt, eval, model or agent file (`git diff --stat main -- runs onyx/gate.py onyx/agents eval
kb/chunks onyx/data/rules.json onyx/data/mandates.json onyx/data/keys onyx/data/scenarios onyx/model.py`: empty).
Seven layers: unchanged from Task 34; nothing shipped or deferred. Owner of any failure: Iyas.

## Summary

The register can now say "no GCC telecom regulator has written it", not only "the UAE lacks it". Six binding Gulf
texts are KB rows (VERIFIED, foreign, never a gate basis, no chunks). Gaps 1, 2, 3 and 11 gain a Gulf global example;
gaps 1, 2, 3, 6, 10, 11 and 12 gain 20 `searched` entries; the GCC sentence is in the register's preamble, the site and
the README. The report changes only in its three count lines: both cell additions pushed it to 6 pages, so neither went
in. Still 5 pages.

## What differs from the order, and why

1. **Qatar 16/2010 is VERIFIED, not REFERENCED.** A1 says REFERENCED only if the schema has no extract kind. It has
   one: `source_type` "extract", already used by the eIDAS, COPPA, GDPR and EECC rows. Hash = the filed extract file
   (`505cb4cd...`); the fetch check is the URL returning 200 (it does, with the JS shell, `db51a8b7...`).
2. **Neither report cell changed.** Gap 1 with "; Saudi CST 552/1445 §13.1, 26.5.2": 6 pages, 2,197 words. Gap 3 with
   "; Qatar CCPR 2024 §1.2": 6 pages, 2,196 words. Both times the first sentence on page 6 was "Before the final: the
   seven unseen scenarios run cold, ...". A3: "If neither fits, leave both." Both left.
3. **Report count lines moved** (77 to 83 documents, twice; 72 to 78 verified; twenty-three to twenty-nine foreign). The
   base order said "Report: unchanged"; A4's count check needs these three, and the build refuses otherwise. The hq copy
   `report-draft-2026-10-23.md` was updated to equal `docs/report.md` (backup `.bak-2026-10-30-task-35`).
4. **`kb fetch` was not run whole.** It rewrites `url_accessed` on all 78 VERIFIED rows. Its own `_download` and hash
   logic ran on the six new rows only (output below); the manifest diff is the six added lines.
5. **Existing test pins extended, not loosened.** "Any test outside the ones named fails" is a stop. These failed only
   because they pin exact counts or lists, as Task 34's did ("the pin follows the counts", Iyas): the KB count pin
   (`test_kb.py`), the gap 10 and gap 12 `searched` lists, gap 2's "last example is Singapore", the Task 32 "which rows
   hold file-quoted entries" list, the Task 33 slice, and the report's count strings (`test_report.py`). Each still
   checks what it checked before; Task 35's entries are named, not ignored.
6. **Three small renderer additions** (no wording change elsewhere): a global example may print its PDF page, an
   Arabic example quote gets an `AR:` label, and an English example may carry its Arabic beside it (`quote_ar`,
   `file_ar`, `page_ar`). Needed for "Arabic beside them (AR label)" on gap 1 and "(p. 14, 29)".

## Decisions taken in the build

- Kuwait's decision (English) and regulation (Arabic) are two instruments (`kw-citra-res-69-2022`,
  `kw-citra-users-rights`): one instrument would list them in the datasheet as one text in two languages, which they
  are not. Saudi en and ar share `sa-cst-552-1445`; Qatar CCPR is `en,ar` in one file.
- `is_official_translation` is "not stated" on all six: none of the texts read says which language prevails.
- Saudi `searched` entries quote the English PDF, which has a readable text layer, except gap 6's 5.1.4, which the
  order wants in Arabic. That one and the three Arabic quotes beside gap 1's example are copied from the read file's
  table and checked against it. Nothing was transcribed by the build.
- The global-example quotes are checked against three derived texts in `kb/sources/global/` (local only, gitignored,
  as for 3GPP 28.535): Qatar CCPR (hq's pypdf text, page markers), Saudi English (hq's pdftotext, a page marker at
  each form feed), Qatar 16/2010 (the extract, unchanged). Each starts with its `Source:` line. Pages are computed
  from the markers, not typed.
- Some `says` lines carry a phrase from the read files beyond the order's short gloss. Gap 1's 26.4 has "a clock on
  resolution, not on reaching a person". Gap 3's 23.1 has "no verification level named for any of them". hq may
  trim either.

## Done means

`kb verify` (counts up by 6 VERIFIED; foreign up by 6 in the datasheet):

```
VERIFIED 78  REFERENCED 2  UNVERIFIED 3  HISTORICAL 0
  every fetched source matches its sha256
```

Datasheet: `83 manifest rows, one per document, 62 instruments`; jurisdiction `foreign | 29` (was 23).

Fresh fetch of every URL, compared with the filed copy (curl, then `kb._download` again for the six rows):

```
200  fresh c8a04d663cad  filed c8a04d663cad  manifest c8a04d663cad  downloaded, equal              qatar-cra-ccpr-2024
200  fresh 4c9f2e4d7469  filed 4c9f2e4d7469  manifest 4c9f2e4d7469  downloaded, equal              kuwait-citra-res-69-2022-en
200  fresh 5107d9d0eafc  filed 5107d9d0eafc  manifest 5107d9d0eafc  downloaded, equal              kuwait-citra-users-rights-ar
200  fresh 113cc118ff4e  filed 113cc118ff4e  manifest 113cc118ff4e  downloaded, equal              saudi-cst-user-protection-552-1445-en
200  fresh eaa4035d46b5  filed eaa4035d46b5  manifest eaa4035d46b5  downloaded, equal              saudi-cst-user-protection-552-1445-ar
200  fresh db51a8b7f086  filed 505cb4cdae5f  manifest 505cb4cdae5f  local copy (URL bytes differ)  qatar-decree-law-16-2010-ar
```

No hash mismatch on any PDF, so no stop. The last line is the expected one: Al Meezan returns the JS shell.

Renders on `docs/gaps.md` and the site, Arabic RTL. `test_task_35_entries_render_on_the_register_and_the_site_arabic_rtl`
passes. The served site (`docs/site/gaps.html`, Playwright, http on 127.0.0.1) showed:

```
gulfItems 29 (20 searched + 9 example quotes), arabicQuotes 12, allRtl true, preamble true
per gap: gap-1 6, gap-2 5, gap-3 4, gap-6 3, gap-10 3, gap-11 5, gap-12 3
```

The only console error was `favicon.ico` 404 from the local test server.

Count check and pages (`docs/build_report.py`, then `scripts/report_pages.ps1`):

```
docs/report.docx
pages: 5
words: 2192
```

`check-data`: `check-data ok: every quote verbatim, every rule cites a clause`.

Full suite: `621 passed in 136.12s` (Task 34: 614; seven new). New tests: `test_task_35_six_rows_are_verified_
foreign_binding_with_no_chunks`, `test_task_35_row_notes_carry_the_orders_caveats`, `test_task_35_counts`,
`test_task_35_examples_are_appended_and_the_leads_stay` (gap 1, 2, 3, 11 examples; Spain and eIDAS still lead),
`test_task_35_searched_entries_are_appended_last` (one or more per touched gap), `test_task_35_quotes_are_verbatim_
in_the_stored_text` (29 quotes, and each example's page), `test_task_35_entries_render_...`.

CI's generators (datasheet, intent, gaps, replay-page, model-down, report build, site) were rerun locally: no file
changed after them. CI on PR #11 (https://github.com/SHRA1M/onyx-hackathon-build/pull/11): `reproduce pass` (runs
41138192632 and 41138269899, push and pull request). Not merged, not tagged.

## Merge danger and blast radius

Two-way door: data rows, register entries and three count lines, all regenerated from the manifest and `gaps.json`.
Nothing in a run, a gate or a key moves; replay verdicts are untouched. A revert of the branch restores Task 34
exactly.

## Open questions for hq

1. The Saudi Arabic quotes (gap 1's three, gap 6's 5.1.4) rest on two image readings, not a person's eye-check;
   the row note and the gap 6 `says` say so. The 11-02 sweep could eye-check one.
2. Qatar CCPR's complaint chapter (§7 to §9) was not read (gulf read file, "Not read"); it may carry a clock for gap 1.
3. The report still names no Gulf text. If hq wants one, it needs a cut elsewhere: about five words push it to page 6.
4. The datasheet's "Which language prevails" table does not list the six new rows: it reads only notes phrased
   "Authoritative language". Their notes say "not stated" in other words.
